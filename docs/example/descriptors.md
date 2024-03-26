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

# Compute the descriptors

The present implementation offers a particular advantage over the original Retip
application (that was based on R) in terms of speed and reliability. In `jp²rt`,
[molecular descriptors](https://egonw.github.io/cdkbook/descriptor.html) are
computed directly in Java, using *parallel streams* (exploiting all the
available CPUs).

In order to compute the descriptors you must prepare a *tab-separated* file
containing the
[SMILES](https://en.wikipedia.org/wiki/Simplified_molecular-input_line-entry_system)
of the compounds you want to analyze. The file must not contain any header, but
can contain any (possibly different) number of field per line, as long as the
SMILES is the last one (of every line). This is particularly convenient if you
want to include additional information about the compounds, such as the name,
the [InChiKey](https://en.wikipedia.org/wiki/International_Chemical_Identifier),
or any other property (that can occupy the first fields of every line). 

The computation being done in parallel does not guarantee that the order of the
lines in the output file will be the same as the input file, so adding an unique
identifier (such as a progressive number, or an InChIKey, as an additional
field) can be required to be able to sort the file back to the original order.

To compute the descriptors, you can use the `jp2rt` command line tool, as

```bash
$ jp2rt compute-descriptors input_file.tsv output_file.tsv
```

where `input_file.tsv` is the name of the file containing the SMILES (as the
last column), and `output_file.tsv` is the name of the produced file.

Observe that you will compute the descriptors both for the (usually small)
*training* dataset (containing experimental retention times) and for the
(possibly very large) dataset you want to predict the retention time.

## Example data

In the following we'll use the [PlaSMA](http://plasma.riken.jp/) dataset (follow
{doc}`example-data` to obtain it); we assume that the file {file}`plasma.tsv`
contains the following four columns:

* (experimental) *retention time* (in minutes),
* *InChiKey*,
* molecule *name*, and
* *SMILES*

```{code-cell} ipython3
:tags: [remove-cell]
from urllib.request import urlopen
from msp2tsv import msp2tsv

PLASMA__DATASET_URL = 'http://plasma.riken.jp/menta.cgi/plasma/get_msp_all'

with urlopen(PLASMA__DATASET_URL) as msp_src, open('plasma.tsv', mode = 'w') as tsv_dst:
  src = msp_src.read().decode('utf-8').splitlines()
  msp2tsv(src, tsv_dst)
```

hence, by running

```bash
$ jp2rt compute-descriptors plasma.tsv plasma+descriptors.tsv
```

```{code-cell} ipython3
:tags: [hide-output, remove-input]
! jp2rt compute-descriptors plasma.tsv plasma+descriptors.tsv
```

we will obtain the file {file}`plasma+descriptors.tsv` that contains the same
four columns, followed by the columns related to the computed *molecular
descriptors*.

## Computing the descriptors for a single molecule

The above approach is the one of choice for *bulk* operations on large datasets.
It is although desirable to be able to compute the descriptor values for a
single molecule and to know every value to exactly what descriptor it refers to.

Albeit in a much slower way, one can compute the descriptors for a single
molecule given its SMILES; take for example
[`O=C(O)C(N)CC1=CC=C(O)C=C1`](https://pubchem.ncbi.nlm.nih.gov/#query=O%3DC(O)C(N)CC1%3DCC%3DC(O)C%3DC1):

```{code-cell} ipython3
from jp2rt import compute_descriptors

smiles = 'O=C(O)C(N)CC1=CC=C(O)C=C1'
descriptors_values = compute_descriptors(smiles)
```

To understand the meaning of the computed values, you can use the function {func}`~jp2rt.java.descriptors` to get the list of the descriptors computed.

```{code-cell} ipython3
from jp2rt import descriptors

descriptors_names = descriptors()
```

Putting together the information returned by the two calls, you can get a better
understanding of the meaning of the computed values.

```{code-cell} ipython3
from tabulate import tabulate

print(tabulate(
  [(*dn, v) for dn, v in zip(
    [(d, n) for d in descriptors_names for n in descriptors_names[d]], 
    descriptors_values)
  ], headers=['Descriptor', 'Name', 'Value']
))
```