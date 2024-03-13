# A Package to Predict Retention Times

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-blue.svg)](http://creativecommons.org/licenses/by-sa/4.0/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10846234.svg)](https://doi.org/10.5281/zenodo.10846234)
[![Stars](https://img.shields.io/github/stars/mapio/jp2rt?style=social)](https://github.com/mapio/jp2rt)

The `jp²rt` package is a modern reimplementation of the
[Retip](https://www.retip.app/) app described in

> "Retip: Retention Time Prediction for Compound Annotation in Untargeted
> Metabolomics" by Paolo Bonini, Tobias Kind, Hiroshi Tsugawa, Dinesh Kumar
> Barupal, and Oliver Fiehn, Analytical Chemistry 2020 92 (11), 7515-7522 —
> [10.1021/acs.analchem.9b05765](https://doi.org/10.1021/acs.analchem.9b05765).

This software has two components:
 
* the `jp²rt` Java package, allowing fast and reliable computation of molecular
  descriptors based on the [Chemistry Development Kit](https://cdk.github.io/),

* the `jp²rt` Python package, allowing model estimation and prediction, based on
  [scikit-learn](https://scikit-learn.org/)  machine learning library.

Both components can be used from the *command line*, or *programmatically* via
the API that they expose.

This documentation consists of several key sections:

- **Install**: Instructions for software installation.
- **A Worked Out Example**: Guidance on *selecting*, *estimating* models, and
  using them for *predicting* retention times.
- **Reference**: Detailed information about `jp²rt` (including Java and Python
  APIs).

## How to cite `jp²rt`

If you find this packge useful, please cite it as follows:

> "jp²rt: A Java and Python package to Predict Retention Times" by Marianna
> Iorio, Sonia Maffioli, Massimo Santini, Matteo Simone  —
> [10.5281/zenodo.10846234](https://doi.org/10.5281/zenodo.10846234).
