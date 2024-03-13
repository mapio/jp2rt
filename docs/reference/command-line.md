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

# Command line usage

## Compute the descriptors

Computing descriptors is the preliminary step for both retention time prediction
and model estimation. The related subcommand is

```bash
$ jp2rt compute-descriptors --help
```

```{code-cell} ipython3
:tags: [remove-input]
! jp2rt compute-descriptors --help
```

If you want to know the names of the computed descriptors (i.e. the names for
the columns added by the previous subcommand), you can use the subcommand

```bash
$ jp2rt list-descriptors
```

```{code-cell} ipython3
:tags: [remove-input]
! jp2rt list-descriptors
```


## Predict retention times

To predict the retention times you need a model and the descriptors; the
subcommand to run the prediction is

```bash
$ jp2rt predict-rt --help
```

```{code-cell} ipython3
:tags: [remove-input]
! jp2rt predict-rt --help
```

## Estimate the model

As explained in {doc}`../example/estimate` it is usually better to perform a
manual analysis of the estimation process, a convenient shortcut is given by the
subcommand

```bash
$ jp2rt estimate-model --help
```

```{code-cell} ipython3
:tags: [remove-input]
! jp2rt estimate-model --help
```

If you want to know the list of valid ensemble model names, just use the
subcommand

```bash
$ jp2rt list-models
```

```{code-cell} ipython3
:tags: [remove-input]
! jp2rt list-models
```

## Directly using the Java library

In case you need to avoid installing Python you can run the molecular
descriptors computation with the following command

```bash
java -jar jp2rt-all.jar INPUT.tsv OUTPUT.tsv
```

where {file}`INPUT.tsv` is the input file, {file}`OUTPUT.tsv` is the output
file, and {file}`jp2rt-all.jar` is the *uber jar* installed following the
{ref}`specific installation instructions <just-java>`.

You can also run 

```bash
java -jar jp2rt-all.jar --list-descriptors
```

to get a list of descriptors names.