# 2dwell

Visualization tool for 2D infinite square well with variable boundary conditions.

## Overview of Files

- README.md contains high level documentation and instructions.
- WellSolver.cpp/WellSolver.h build to a c++ library which can be used as a Python module. This functionality is provided using the Pybind11 code.
- Makefile is used to build all c++ dependencies.
- 2dwell.py is a wrapper script to run the program.
- wellgraphics.py contains classes and module imports.

## Prerequisites

These are some requirements which may be necessary on clean machines.

- [Git version 2](https://git-scm.com/download/mac)
- [Homebrew version 3](https://brew.sh/)
- [Python version 3](https://opensource.com/article/19/5/python-3-default-mac)
- [Pip version 21](https://pip.pypa.io/en/stable/installing/)

## Dependencies/Installation

1. Install necessary Python libraries:
```bash
pip3 install matplotlib
pip3 install seaborn
brew install pybind11
brew install tcl-tk
```
2. Clone repository:
```bash
git clone https://github.com/noahchongsiriwatana/physics6810-final-project.git
```
3. Clean environment, then build C++ libraries:
```bash
make clean
make
```

## Running 2dwell

```bash
python 2dwell.py
```

## Notes

Make sure ```python``` resolves to ```python3``` in your path. The tutorial link for Python should be helpful with this.


