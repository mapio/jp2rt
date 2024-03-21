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

# Appendix

(which-descriptors)=
## Which descriptors are computed

The [Chemistry Development Kit](https://cdk.github.io/) provides a large list of
molecular descriptors, as API for the
[`org.openscience.cdk.qsar.descriptors.molecular`](https://cdk.github.io/cdk/2.9/docs/api/org/openscience/cdk/qsar/descriptors/molecular/package-summary.html)
package reports.

We can get the list of such descriptors by running the following code:

```{code-cell} ipython3
import re
from urllib.request import urlopen

API_URL = 'https://cdk.github.io/cdk/2.9/docs/api/org/openscience/cdk/qsar/descriptors/molecular/package-summary.html'
PATTERN = re.compile(r'href="(\w[^"]+).html" title="class in')

cdk_descriptors = set()
with urlopen(API_URL) as inf:
  for line in inf.read().decode('utf-8').splitlines():
    if m := PATTERN.search(line):
      cdk_descriptors.add(m.group(1))

cdk_descriptors
```

However, not all of these descriptors are computed by the `jp²rt` package, more
precisely, the set of not computed descriptors can be obtained by the
difference:

```{code-cell} ipython3
from jp2rt import descriptors

jp2rt_descriptors = set(descriptors())
not_computed = cdk_descriptors - jp2rt_descriptors

not_computed
```

The reason why such descriptors are not computed is that their computation
returns just NaN values or raise exceptions, as one can easily check with the
{func}`~jp2rt.java.compute_single_descriptor` function.

```{code-cell} ipython3
import numpy as np 
from jp2rt import compute_single_descriptor

smiles = 'O=C(O)C(N)CC1=CC=C(O)C=C1'

for descriptor in not_computed:
  print(descriptor, all(np.isnan(f) for f in compute_single_descriptor(descriptor, smiles)))
```

## How this documentation is produced

This documentation is generated using [Jupiter Book](https://jupyterbook.org/),
the source of the documentation is available in the `jp²rt` repository, in the
[`docs`](https://github.com/mapio/jp2rt/tree/master/docs) directory.

Every code sample (both in Python and shell) is executed during the build of the
documentation, so all the output present in the documentation is up-to-date and
corresponds exactly to the output produced by the current version of the
package.

If you want to run the code of this documentation besides the `jp²rt` package
(with `plot` dependencies included) you need to install [Jupiter
Book](https://jupyterbook.org/). Otherwise you can download a precompiled copy
of the documentation from the
[Releases](https://github.com/mapio/jp2rt/releases) page of the `jp²rt`
repository.

The following table reports the computation time of the various code samples for
every section of this documentation.

```{nb-exec-table}
```

## Changelog

You can find the
[CHANGELOG](https://github.com/mapio/jp2rt/blob/master/CHANGELOG.md) in the
`jp²rt` repository.
