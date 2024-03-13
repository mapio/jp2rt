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

# Get some example data

To provide some example of execution of `jp²rt`, we'll use a small curated
dataset, namely the [PlaSMA](http://plasma.riken.jp/) dataset that can be freely
download from the network.

The dataset is provided in NIST MS format (`.msp`), so we'll write a `msp2tsv`
function to convert such format to the *tab separated values* (`.tsv`) used to
compute the molecular descriptors. During the conversion, only entries with an
InChiKey, the SMILES and with positive ionization mode are kept.

We can preserve how many information we want from the original file, provided
that:

* the file is in *tab separated values* format,
* the first field is the *retention time*,
* the last field is the *SMILES*.

Since the computation of the molecular descriptors is performed in parallel, the
output file is not guaranteed to have the same order as the input file, for this
reason it can be a good idea to preserve at least the InChIKey to be able to
match the original data with the one with computed molecular descriptors.

```{eval-rst} 
.. literalinclude:: msp2tsv.py
```

We can use the above function to save a `.tsv` file while downloading the
original dataset directly from the PlaSMA
[download](http://plasma.riken.jp/menta.cgi/plasma/plant_chemical_diversity_download)
page: 

```python 
PLASMA__DATASET_URL = 'http://plasma.riken.jp/menta.cgi/plasma/get_msp_all'
```

There is actually non need to save the `.msp` on the local disk, the `.tsv` can
be produced on the fly:

```python
from urllib.request import urlopen

with urlopen(PLASMA__DATASET_URL) as msp_src, open('plasma.tsv', mode = 'w') as tsv_dst:
  src = msp_src.read().decode('utf-8').splitlines()
  msp2tsv(src, tsv_dst)
```

We can check the number of downloaded lines:

```bash
$ wc -l plasma.tsv
```

```{code-cell} ipython3
:tags: [remove-input]
! wc -l plasma.tsv
```