---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Estimate the model

## Load the data

We can use the {func}`~jp2rt.ml.load_descriptors` and
{func}`~jp2rt.ml.load_retention_times` convenience functions that can load
data from *tab separated values* files provided that:

* the *retention times* are in the first column, and
* the *molecular descriptors* are in the last columns and follow at least one
  non numeric column (such as, for instance, the SMILES one).

```{code-cell} ipython3
from jp2rt import load_descriptors, load_retention_times

X = load_descriptors('plasma+descriptors.tsv')
y = load_retention_times('plasma+descriptors.tsv')
```

As a check we can verify that the number of rows in `X` is the same as the
number of rows in `y`:

```{code-cell} ipython3
X.shape, y.shape
```

## Use scikit-learn

To understand more in detail how model estimation and prediction works, in this
section we will use directly the [scikit-learn](https://scikit-learn.org)
package using the regression models of the {mod}`sklearn.ensemble` package; in
the following section we'll present an easier approach based on `jp²rt` that
summons the approach shown here.

### Clean the data

Before using the data we need to prepare it as detailed in [Preprocessing
data](https://scikit-learn.org/stable/modules/preprocessing.html).

The computation of the descriptors may have produced some NaNs, we'll follow two
approaches according to the fact that we have columns with just NaNs, or with
some NaNs and other valid values. First of all, we compute the columns
containing just NaNs:

```{code-cell} ipython3
import numpy as np

all_nan_cols = [i for i, x in enumerate(X.T) if all(np.isnan(x))]
all_nan_cols
```
We can take care of such columns using a
{class}`~sklearn.compose.ColumnTransformer` that will drop the columns
containing just NaNs (and pass through the other ones); the case of some NaNs
will be handled using a {class}`~sklearn.impute.SimpleImputer` that will replace
missing values with the mean of valid ones; moreover we'll scale the data using
a {class}`~sklearn.preprocessing.StandardScaler` to reduce the variance, a fact
that is usually beneficial to regression models.


```{code-cell} ipython3
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

drop_all_nan_cols = ColumnTransformer([('drop_all_nan_cols', 'drop', all_nan_cols)], remainder = 'passthrough')
simple_imputer = SimpleImputer()
standard_scaler = StandardScaler()
```

We'll put the column transformer, the imputer, and the scaler together with
various regressors (discussed in the coming subsections) in a *pipeline* using
the {func}`~sklearn.pipeline.make_pipeline` function.

### Model selection

To decide with ensemble model will best fit our data we'll use both [cross
validation](https://scikit-learn.org/stable/modules/cross_validation.html) and
[visual
inspection](https://scikit-learn.org/stable/auto_examples/model_selection/plot_cv_predict.html)
of the results via the convenience `jp²rt` function
{func}`~jp2rt.ml.evaluate_model` that returns a dictionary with various
information of interest.

#### Gradient Boosting

Let's start defining the model pipeline based on the
{class}`~sklearn.ensemble.GradientBoostingRegressor` and evaluating it:

```{code-cell} ipython3
from sklearn.ensemble import GradientBoostingRegressor
from jp2rt import evaluate_model

regressor = GradientBoostingRegressor()
model =  make_pipeline(drop_all_nan_cols, simple_imputer, standard_scaler, regressor)
evaluation = evaluate_model(model, X, y)
```

We keep track of this first evaluation in the `results` list, and we can inspect
the `plot` key of `evaluation`

```{code-cell} ipython3
result = []
result.append({'regressor': 'GradientBoosting'} | evaluation['metrics'])

evaluation['plot']
```

that depicts a some *residuals* (the difference between the true and the
predicted values) analysis; in a more quantitative way we can inspect the
`metrics` key, or the convenience version `table`:

```{code-cell} ipython3
print(evaluation['table'])
```

Since the *cross validation* runs a model estimation per split (in this example,
5 times, that is the default value for the evaluation function), we get the
*mean* and *std* (standard deviation) of two metrics of interest:

* the *coefficient of determination* ($R^2$) computed by
  {func}`~sklearn.metrics.r2_score`, and
* the *root mean squared error* (RMSE) computed by
  {func}`~sklearn.metrics.root_mean_squared_error`.

Moreover, the evaluation returns the values of the *empirical quantiles* of the
residual distribution (obtained using the {func}`~scipy.stats.mstats.mquantiles`
function) $q_0$ at 5% and $q_1$ at 95%. The interval $[q_0, q_1]$ is the shaded
box in the last of the three plots and represents the 90% of the residuals
according to the cross validated prediction (obtained using the
{func}`~sklearn.model_selection.cross_val_predict` function).

#### A more robust boosting model

The {class}`~sklearn.ensemble.HistGradientBoostingRegressor` is a more recent
implementation of the gradient boosting algorithm that is more efficient and can
handle larger datasets, taking care of NaNs; we can use it with a simpler
pipeline:

```{code-cell} ipython3
from sklearn.ensemble import HistGradientBoostingRegressor

regressor = HistGradientBoostingRegressor()
model =  make_pipeline(drop_all_nan_cols, regressor)
evaluation = evaluate_model(model, X, y)

result.append({'regressor': 'HistGradientBoosting'} | evaluation['metrics'])
evaluation['plot']
```

Quantitatively the results look promising:

```{code-cell} ipython3
print(evaluation['table'])
```

#### A more precise tree model

We conclude this part with the {class}`~sklearn.ensemble.ExtraTreesRegressor`
that seems to even even better performances.

```{code-cell} ipython3
from sklearn.ensemble import ExtraTreesRegressor

regressor = HistGradientBoostingRegressor()
model =  make_pipeline(drop_all_nan_cols, simple_imputer, standard_scaler, regressor)
evaluation = evaluate_model(model, X, y)

result.append({'regressor': 'ExtraTrees'} | evaluation['metrics'])
evaluation['plot']
```

Quantitatively the results are even better:

```{code-cell} ipython3
print(evaluation['table'])
```

### Choose, train and save the model

We can put together the quantitative results to help us choose the best model:

```{code-cell} ipython3
from tabulate import tabulate

print(tabulate([r.values() for r in result], headers = result[0].keys(), tablefmt = 'outline', floatfmt = '.4f'))
```

Suppose we choose the last (*ExtraTrees*) model, we can then *train* it with all the data at our disposal

```{code-cell} ipython3
from jp2rt import save_model

model.fit(X, y)
```

Finally we can save the trained model using the {func}`~jp2rt.ml.save_model` function:

```{code-cell} ipython3
from jp2rt import save_model

save_model(model, 'extratrees')
```

## Use `jp²rt`

Even if performing the above tasks allows for a more detailed understanding of
model estimation and can be personalized with further processing and analysis
steps to improve the quality of the model, sometimes can be a tedious and error
prone process, especially for beginners.

To facilitate the process we can use the
{func}`~jp2rt.ml.simple_ensemble_model_estimate` function that takes as input
the name of a regressor, valid names are returned by the
{func}`~jp2rt.ml.list_ensemble_models` function:

```{code-cell} ipython3
from jp2rt import list_ensemble_models

list_ensemble_models()
```
For example, we can see what we get using `AdaBoost`:

```{code-cell} ipython3
from jp2rt import simple_ensemble_model_estimate

model = simple_ensemble_model_estimate('AdaBoost', X, y)
evaluation = evaluate_model(model, X, y)
evaluation['plot']
```

### The command line

To make things even easier, we can use the command line interface of `jp²rt` to list the available models:

```bash
$ jp2rt list-models
```

```{code-cell} ipython3
:tags: [remove-input]

! jp2rt list-models
```

And to estimate (and evaluate) a model:

```bash
$ jp2rt estimate-model --evaluate Bagging docs/plasma+descriptors.tsv out
```

```{code-cell} ipython3
:tags: [remove-input]

! jp2rt estimate-model --evaluate Bagging plasma+descriptors.tsv bagging
```

that will create the {file}`bagging.jp2rt` containing the saved model, and
`bagging.png` the visual residual analysis.