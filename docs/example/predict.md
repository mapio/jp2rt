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

# Predict the Retention Time

Now assume we have a list of compounds of which we know only the SMILES; since
we have no other data than the PlaSMA dataset, we'll take the fourth column of
the first 100 lines of {file}`plasma.tsv` file:

```bash
$ cut -f 4 plasma.tsv | head -n 100 > smiles.tsv
```

```{code-cell} ipython3
:tags: [remove-cell]
! cut -f 4 plasma.tsv | head -n 100 > smiles.tsv
```

So the steps we need to perform are:

* compute the molecular descriptors for each SMILES,
* load the model, and the descriptors,
* predict the retention time with the model.

## Use the API

Molecular descriptors can be added not only using the command line as shown in {doc}`descriptors`, but also using the {func}`~jp2rt.java.add_descriptors_via_tsv` function.

```{code-cell} ipython3
:tags: [hide-output]
from jp2rt import add_descriptors_via_tsv

add_descriptors_via_tsv('smiles.tsv', 'smiles+descriptors.tsv')
```

We are now ready to load the computed descriptors, the model we have estimated and saved and to use it to predict the retention time:

```{code-cell} ipython3
from jp2rt import load_model, load_descriptors

X = load_descriptors('smiles+descriptors.tsv')
model = load_model('extratrees')
y = model.predict(X)
```

## The command line

The same steps can be performed using the command line, we have already seen in {doc}`descriptors` how to add the descriptors, so we just need to predict the retention time:

```bash
$ jp2rt predict-rt extratrees.jp2rt smiles+descriptors.tsv rt+smiles+descriptors.tsv
```

```{code-cell} ipython3
:tags: [remove-input]
! jp2rt predict-rt extratrees.jp2rt smiles+descriptors.tsv rt+smiles+descriptors.tsv
```
