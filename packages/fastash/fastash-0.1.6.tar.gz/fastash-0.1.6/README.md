# FastASH
Fast Averaged Shifted Histograms.

Density estimation which approximate a triangular Kernel Density Estimation (KDE.
Cython inside.

## Install

If Cython is installed, the sources files in '.pyx' are used. Otherwise, the '.cpp' files are directly used.

### From PyPi

Simply use the Pypi command (numpy is mandatorry to achieve the installation due to cython components) :

```bash
pip install numpy
pip install fastash 
```

### From Source

Simply use the install command :

```bash
make install
```

This command is usefull during the developpement work.

## Build and deploy

To build the package :
```bash
make build
```

Then, the procedure to deploy is the following (version number need to be incremented) :
```bash
make dist
make deploy
```

## Getting Started

exemple usage in test/test_2d.py

## help for packaging

script files are based on the package https://github.com/cmcqueen/simplerandom .
