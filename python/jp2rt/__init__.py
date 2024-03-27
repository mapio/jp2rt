from importlib.util import find_spec

__version__ = '0.2.2a1'

HAS_PLOT = (find_spec('matplotlib') is not None) and (find_spec('seaborn') is not None)

from jp2rt.java import (  # noqa: E402
  add_descriptors_via_tsv,
  compute_descriptors,
  compute_single_descriptor,
  descriptors,
)
from jp2rt.ml import (  # noqa: E402
  evaluate_model,
  list_ensemble_models,
  load_descriptors,
  load_model,
  load_retention_times,
  save_model,
  simple_ensemble_model_estimate,
)

__all__ = [
  '__version__',
  'add_descriptors_via_tsv',
  'descriptors',
  'compute_single_descriptor',
  'compute_descriptors',
  'save_model',
  'load_model',
  'load_descriptors',
  'load_retention_times',
  'simple_ensemble_model_estimate',
  'list_ensemble_models',
  'evaluate_model',
]
