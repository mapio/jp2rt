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

# Install the software

We recommend using the latest version of Python and Java, `jp²rt` is tested
under Python 3.10 and Java 17; the Python package includes a precompiled version
of the Java package, so you don't need to install it separately.

## Virtual environments

It's suggested to use a *virtual environment* to manage Python dependencies:
virtual environments are independent groups of Python libraries, one for each
project; packages installed for one project will not affect other projects or
the operating system's packages.

### Create an environment

Python 3 comes bundled with the :mod:`venv` module to create virtual
environments. Create a project folder and a :file:`venv` folder within:

```bash
$ mkdir myproject
$ cd myproject
$ python3 -m venv venv
```

On Windows:

```bat
> py -3 -m venv venv
```

### Activate the environment

Every time you decide to use the library, activate the environment:


```bash
$ . venv/bin/activate
```

On Windows:

```bat
> venv\Scripts\activate
```

## Install the package

Within the activated environment, use the following command to install the full
version of the package:

```bash
$ pip install jp2rt[plot]
```

If you plan to use the package on a system with no graphic support (for
instance, on an headless high-performance computing cluster), you can install
the package without the optional dependencies for plotting as:

```bash
$ pip install jp2rt
```

To check the installation just run

```bash
$ jp2rt --help
```

it should print the help message, including the list of
available subcommands:

```{code-cell} ipython3
:tags: [remove-input]
! jp2rt --help
```

(just-java)=
## Install just the Java library

If you need to run just the descriptors computation on a system where it would
be difficult to setup a Python environment (for instance, on a high performance
computing cluster), you can install just the Java library as follows:

* manually downloading a *fat jar* (containing all the dependencies) from the
  [Releases](https://github.com/mapio/jp2rt/releases) page of the `jp²rt`
  repository, or
* using the [GitHub Apache Maven
  registry](https://github.com/mapio?tab=packages&repo_name=jp2rt) of the
  `jp²rt` repository; beware that authentication is needed, so please check the
  [instructions](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-apache-maven-registry#installing-a-package).

