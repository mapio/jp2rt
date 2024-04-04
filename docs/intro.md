# A Package to Predict Retention Times

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-blue.svg)](http://creativecommons.org/licenses/by-sa/4.0/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10846234.svg)](https://doi.org/10.5281/zenodo.10846234)
[![Stars](https://img.shields.io/github/stars/mapio/jp2rt?style=social)](https://github.com/mapio/jp2rt)

The `jp²rt` package is a modern reimplementation of the
[Retip](https://www.retip.app/) application described in

> "Retip: Retention Time Prediction for Compound Annotation in Untargeted
> Metabolomics" by Paolo Bonini, Tobias Kind, Hiroshi Tsugawa, Dinesh Kumar
> Barupal, and Oliver Fiehn, Analytical Chemistry 2020 92 (11), 7515-7522 —
> [10.1021/acs.analchem.9b05765](https://doi.org/10.1021/acs.analchem.9b05765).

The basic idea of Retip is to train a *machine learning regression model* based
on *features* that can be computed given the molecular structure (the [molecular
descriptors](https://egonw.github.io/cdkbook/descriptor.html)) on a *reasonably
small* set of compounds for which the *retention time* is *experimentally* know,
and then use such model to predict the retention time of a potentially *very
large* set of new compounds.

With respect to the original implementation, the present one optimizes the
computation of *features*, thanks to a robust native Java parallel
implementation (see the [API
overview](https://mapio.github.io/jp2rt/javadoc/it/unimi/di/jp2rt/package-summary.html)
for more details) and replaces the somehow outdated R machine learning code
(based on external dependencies that nowadays can be difficult to compile and
run) with the modern Python state of the art machine learning stack. More in
detail, this software has two components:
 
* the `jp²rt` Java package, allowing fast and reliable computation of molecular
  descriptors based on the [Chemistry Development Kit](https://cdk.github.io/),

* the `jp²rt` Python package, allowing model estimation and prediction, based on
  [scikit-learn](https://scikit-learn.org/)  machine learning library.

As shown in the following documentation, both components can be used from the
*command line*, or *programmatically* via the API that they expose.

This documentation consists of several key sections:

- **Install**: Instructions for software installation.
- **A Worked Out Example**: Guidance on *selecting*, *estimating* models, and
  using them for *predicting* retention times.
- **Reference**: Detailed information about `jp²rt` (including Java and Python
  APIs).

## How to cite `jp²rt`

If you find this packge useful, please cite it as follows:

> "jp²rt: A Java and Python package to Predict Retention Times" by [Marianna
> Iorio](https://www.linkedin.com/in/marianna-iorio-744b6421/)<sup>†</sup>, [Sonia
> Maffioli](https://www.linkedin.com/in/sonia-ilaria-maffioli-b028901/)<sup>†</sup>,
> [Massimo Santini](https://santini.di.unimi.it/)<sup>‡</sup>, and [Matteo
> Simone](https://www.linkedin.com/in/matteo-simone-7b8151123/)<sup>†</sup>  —
> [10.5281/zenodo.10846234](https://doi.org/10.5281/zenodo.10846234).

This work has been partially supported by Grant No. DM60066 from the Italian
Ministry of University and Research to Naicons<sup>†</sup> srl.