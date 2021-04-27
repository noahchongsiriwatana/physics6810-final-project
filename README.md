# 2DWell

Visualization tool for 2D infinite square well with variable boundary conditions.

I chose this project to give myself a chance to try integrating the different tools we learned in class into a cohesive application. At the highest level, I built a simple event based GUI using Python, and integrated it with plotting using Matplotlib. This GUI then spoke with a C++ program to get the different eigenstates desired. These solutions were found pseudo analytically by borrowing the solutions from a similar problem, namely, the 2d infinite square well. In the future, I would like to try and solve this numerically by using the methods described in session 16 for solving partial differential equations. I feel like this problem would work well with the relaxation method, so hopefully I get a chance to try that later. I also tried to solve this problem following the numerical methods from [this document](https://etd.ohiolink.edu/apexprod/rws_etd/send_file/send?accession=oberlin1497568215606295&disposition=inline), but it was beyond the scope of my current capabilities.

Regardless, this project gave me a chance to build upon and explore more deeply the topics in class. I really enjoyed digging into Pybind11 and seeing how to write C++ libraries which can not only be called from a Python script as learned in class, but to be imported directly into the Python code as a module. This required some hairy investigations of how Python handled memory vs. C++, as well as how to properly create data in C++ to be compatible with Python.

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
brew install boost --with-python
brew install boost-python
```
2. Clone repository:
```bash
git clone https://github.com/noahchongsiriwatana/physics6810-final-project.git
```
3. Clean environment, then build C++ libraries:
```bash
make clean
```
If building on Linux run:
```bash
make
```
If building on MacOS run:
```bash
make macos
```

## Running 2dwell

```bash
python 2dwell.py
```

## Notes

Make sure ```python``` resolves to ```python3``` in your path. The tutorial link for Python should be helpful with this.
