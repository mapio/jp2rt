# Python API

The Python code is organized in two packages: {mod}`jp2rt.ml` and
{mod}`jp2rt.java` that will be described in the following sections.

## Machine learning related functions

```{eval-rst}
.. module:: jp2rt.ml
```

The {mod}`jp2rt.ml` module contains functions related to machine learning
aspects.

### Data I/O

This package relies on *tab separated values* format; for this reason two
functions are provided to load *molecular descriptors* and *retention times*
from files in such format. The following convention is assumed:

* the files do not contain any header (but can have a different number of fields
  per row)
* the **retention time** is the first field of the row,
* the **SMILES** value (if needed) is the last *non numeric* field of the row
  (that is, a value for which the conversion with {class}`float` raises
  {class}`ValueError`),
* the **molecular descriptors** (if present) are the last fields of the row and
  are preceded by a *non numeric* value (for example, the SMILES value).

The following function is needed both in {doc}`estimating a model <../example/estimate>`,
and {doc}`predicting the retention times <../example/predict>`. Since molecular descriptors
values are usually added using {func}`~jp2rt.java.add_descriptors_via_tsv` (or
its command line equivalent) the above mentioned convention is satisfied.

```{eval-rst}
.. autofunction:: jp2rt.ml.load_descriptors
```
On the other hand, if the retention times are to be loaded as in
{doc}`estimating a model <../example/estimate>` the following function is used.

```{eval-rst}
.. autofunction:: jp2rt.ml.load_retention_times
```

### Model I/O

The following two functions can be used, respectively, to load and save a model.

By model in `jp²rt` we usually mean any instance of a [Supervised
learning](https://scikit-learn.org/stable/supervised_learning.html) model, or in
a broader sense a class implementing the [scikit-learn estimator
interface](https://scikit-learn.org/stable/developers/develop.html) (a condition
that can be checked using the
{func}`~sklearn.utils.estimator_checks.check_estimator` function).

Models are saved in a compressed archive (as defined in [PKZIP Application
Note](https://pkwaredownloads.blob.core.windows.net/pkware-general/Documentation/APPNOTE-6.3.9.TXT));
the archive contains the model itself (as serialized by
[Joblib](https://joblib.readthedocs.io/)) and a *manifest* file that allows to
check that the refers to the correct `jp²rt` version.

The following function is usually required when {doc}`predicting the retention
times <../example/predict>`.

```{eval-rst}
.. autofunction:: jp2rt.ml.load_model
```

On the other hand, the following function is usually required at the end of the
{doc}`model estimation <../example/estimate>` process.

```{eval-rst}
.. autofunction:: jp2rt.ml.save_model
```

### Model estimation and evaluation

Model validation is usually performed using [cross
validation](https://scikit-learn.org/stable/modules/cross_validation.html) and
[visual
inspection](https://scikit-learn.org/stable/auto_examples/model_selection/plot_cv_predict.html).

As shown in {doc}`../example/estimate` the following function is used to assist in the
validation and hence selection process.

```{eval-rst}
.. autofunction:: jp2rt.ml.evaluate_model
```

Performing model definition, evaluation and training can be a complex task. The following convenience function is provided to simplify the process.

```{eval-rst}
.. autofunction:: jp2rt.ml.simple_ensemble_model_estimate
```

As the name suggests, the function considers just [ensemble
models](https://scikit-learn.org/stable/modules/ensemble.html); you can get a list of valid values for the `regressor_name` parameter using the following function

```{eval-rst}
.. autofunction:: jp2rt.ml.list_ensemble_models
```

## Java bridge functions

```{eval-rst}
.. module:: jp2rt.java
```

The {mod}`jp2rt.java` module contains functions that help bridging the Java
implementation with the Python code. Java code execution in Python is made
possible by [`SciJava`](https://github.com/scijava/) that in turn is built on
[JPype](https://jpype.readthedocs.io/.

For *bulk* operations it is better to avoid a Python/Java conversion of data for
each molecule; for this reason the following function works by reading and
writing the data from *tab separated values* files.

```{eval-rst}
.. autofunction:: jp2rt.java.add_descriptors_via_tsv
```

The above function computes a subset of the molecular descriptors available in
CDK (for a discussion on how such descriptors are selected, see the [dedicated
appendix section](which-descriptors)); the class and value names of the
considered descriptors are returned by the following function.

```{eval-rst}
.. autofunction:: jp2rt.java.descriptors
```

If one is interested in computing the set of descriptors for a single molecule, given its SMILES, the following function can be used.

```{eval-rst}
.. autofunction:: jp2rt.java.compute_descriptors
```

In case one needs to compute a single descriptor (whatever the descriptor is, even if it does not belong to the selected ones) the following function can be used.

```{eval-rst}
.. autofunction:: jp2rt.java.compute_single_descriptor
```

More detailed information about the Java code can be found in the [Java API documentation](https://mapio.github.io/jp2rt/javadoc/it/unimi/di/jp2rt/package-summary.html).
