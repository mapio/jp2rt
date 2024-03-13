import importlib
import io
import zipfile
from pathlib import Path

from jp2rt import HAS_PLOT

if HAS_PLOT:
  import matplotlib.pyplot as plt
  import seaborn as sns

import joblib
import numpy as np
from packaging.version import Version, parse
from scipy.stats.mstats import mquantiles
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import PredictionErrorDisplay
from sklearn.model_selection import cross_val_predict, cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from tabulate import tabulate

from jp2rt import __version__

MANIFEST_VERSION = Version('1.0')
JP2RT_VERSION = parse(__version__)
MANIFEST = f'Manifest-Version: {MANIFEST_VERSION}\nJP2RT-Version: {JP2RT_VERSION}\n'
ENSEMBLE_REGRESSOR_MODULE = importlib.import_module('sklearn.ensemble')


def save_model(model, path):
  """
  Saves a model to a file.

  Args:
    model (:obj:`sklearn.base.BaseEstimator`): The model to save.
    path (:obj:`str`): The path of the file to save the model to.
  Returns:
    :obj:`int`: The number of bytes written to the file.
  """
  if not isinstance(path, Path):
    path = Path(path)
  mbuf = io.BytesIO()
  joblib.dump(model, mbuf)
  mbuf.flush()
  zbuf = io.BytesIO()
  with zipfile.ZipFile(zbuf, 'a', zipfile.ZIP_DEFLATED, True) as ouf:
    ouf.writestr(f'{path.stem}/MANIFEST.txt', MANIFEST.encode('utf-8'))
    ouf.writestr(f'{path.stem}/model.joblib', mbuf.getvalue())
  return path.with_suffix('.jp2rt').write_bytes(zbuf.getvalue())


def load_model(path):
  """
  Loads a model from a file.

  Args:
    path (:obj:`str`): The path of the file to load the model from.
  Returns:
    :obj:`sklearn.base.BaseEstimator`: The loaded model.
  """
  if not isinstance(path, Path):
    path = Path(path)
  zbuf = io.BytesIO(path.with_suffix('.jp2rt').read_bytes())
  with zipfile.ZipFile(zbuf, 'r') as inf:
    manifest = inf.read(f'{path.stem}/MANIFEST.txt').decode('utf-8')
    with inf.open(f'{path.stem}/model.joblib') as mbuf:
      model = joblib.load(mbuf)
  manifest = dict(line.strip().split(': ') for line in manifest.splitlines() if line)
  if 'Manifest-Version' not in manifest:
    raise ValueError('Invalid model file, manifest missing Manifest-Version')
  if parse(manifest['Manifest-Version']) > MANIFEST_VERSION:
    raise ValueError('Invalid model file, manifest version too high')
  if 'JP2RT-Version' not in manifest:
    raise ValueError('Invalid model file, manifest missing JP2RT-Version')
  if parse(manifest['JP2RT-Version']) > JP2RT_VERSION:
    raise ValueError('Invalid model file, jp2rt version too high')
  return model


def load_retention_times(path):
  """Loads retention times values from a file and returns them as a numpy array.

  The input file must be in tab separated format, must not have an header, and the
  retention time must be the first field on every row.

  Args:
    path (:obj:`str`): The path of the tab separated file to read.

  Returns:
    :obj:`numpy.array`: the retention times values.
  """
  return np.genfromtxt(path, delimiter='\t', comments=None, usecols=(0,))


def load_descriptors(path):
  """Loads molecular descriptors values from a file and returns them as a numpy array.

  The input file must be in tab separated format, must not have an header, and the
  descriptors must be the last fields of every row and must be preceded by a non
  numeric field (for instance a SMILES) on every row.

  Args:
    path (:obj:`str`): The path of the tab separated file to read.

  Returns:
    :obj:`numpy.array`: the descriptor values.
  """
  with open(path) as inf:
    first_line = inf.readline()
  fields = first_line.split('\t')
  n_fields = len(fields)
  for n_descriptors, field in enumerate(reversed(fields)):  # noqa: B007
    try:
      float(field)
    except ValueError:
      break
  return np.genfromtxt(path, delimiter='\t', comments=None, usecols=range(n_fields - n_descriptors, n_fields))


def list_ensemble_models():
  """Lists the available ensemble models names."""
  res = []
  for regressor in ENSEMBLE_REGRESSOR_MODULE.__all__:
    if not regressor.endswith('Regressor'):
      continue
    try:
      getattr(ENSEMBLE_REGRESSOR_MODULE, regressor)()
      res.append(regressor.removesuffix('Regressor'))
    except TypeError:
      pass
  return sorted(res)


def simple_ensemble_model_estimate(regressor_name, X, y):
  """
  Trains a simple ensemble model using the given regressor and the input data.

  Args:
    regressor_name (:obj:`str`): The name of the regressor to use.
    X (:obj:`numpy.array`): The input data.
    y (:obj:`numpy.array`): The target values.
  Returns:
    :obj:`sklearn.base.BaseEstimator`: The trained model.
  """
  if regressor_name not in list_ensemble_models():
    raise ValueError(f'Invalid regressor name: {regressor_name}')
  regressor = getattr(ENSEMBLE_REGRESSOR_MODULE, regressor_name + 'Regressor')()
  all_nan_cols = [i for i, x in enumerate(X.T) if all(np.isnan(x))]
  drop_all_nan_cols = ColumnTransformer([('drop_all_nan_cols', 'drop', all_nan_cols)], remainder='passthrough')
  imputer = SimpleImputer(strategy='mean')
  scaler = StandardScaler()
  model = make_pipeline(drop_all_nan_cols, imputer, scaler, regressor)
  model.fit(X, y)
  return model


def evaluate_model(model, X, y, n_splits=5, prob=0.95):
  """Evaluates a model using cross validation and visual inspection.

  Args:
    model (:obj:`sklearn.base.BaseEstimator`): The model to evaluate.
    X (:obj:`numpy.array`): The input data.
    y (:obj:`numpy.array`): The target values.
    n_splits (:obj:`int`, optional): The number of splits to use for cross validation. Defaults to 5.
    prob (:obj:`float`, optional): The confidence interval to use for the residuals distribution plot. Defaults to 0.95.

  Returns:
    :obj:`dict`: A dictionary with the evaluation results.
  """
  cv = cross_validate(model, X, y, cv=n_splits, n_jobs=-1, scoring=['neg_root_mean_squared_error', 'r2'])
  y_pred = cross_val_predict(model, X, y, cv=n_splits, n_jobs=-1)
  residuals = y - y_pred
  q0, q1 = mquantiles(residuals, prob=[1 - prob, prob])

  if HAS_PLOT:
    fig, axs = plt.subplots(ncols=3, figsize=(12, 4))
    axs[0].set_title('Actual vs. Predicted values')
    PredictionErrorDisplay.from_predictions(
      y, y_pred=y_pred, kind='actual_vs_predicted', ax=axs[0], scatter_kwargs={'s': 1}
    )
    axs[1].set_title('Residuals vs. Predicted Values')
    PredictionErrorDisplay.from_predictions(
      y, y_pred=y_pred, kind='residual_vs_predicted', ax=axs[1], scatter_kwargs={'s': 1}
    )
    axs[2].set_title('Residuals distribution')
    sns.histplot(residuals, ax=axs[2], bins=50, kde=True)
    axs[2].axvspan(q0, q1, alpha=0.2)
    plt.tight_layout()
    plt.close(fig)  # to avid displaying it
  metrics = {
    'r2 mean': cv['test_r2'].mean(),
    'r2 std': cv['test_r2'].std(),
    'rmse mean': -cv['test_neg_root_mean_squared_error'].mean(),
    'rmse std': cv['test_neg_root_mean_squared_error'].std(),
    'q0': q0,
    'q1': q1,
  }
  return {
    'args': {'n_splits': n_splits, 'prob': prob},
    'details': {'r2': cv['test_r2'], 'rmse': -cv['test_neg_root_mean_squared_error']},
    'metrics': metrics,
    'plot': fig if HAS_PLOT else None,
    'table': tabulate(metrics.items(), tablefmt='outline', floatfmt='.4f'),
  }
