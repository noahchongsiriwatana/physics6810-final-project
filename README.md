# 2dwell

Visualization tool for 2D infinite square well with variable boundary conditions.

## Prerequisites

These are some requirements which may be necessary on clean machines.

- [Git version 2](https://git-scm.com/download/mac)
- [Homebrew version 3](https://brew.sh/)
- [Python version 3](https://opensource.com/article/19/5/python-3-default-mac)
- [Pip version 21](https://pip.pypa.io/en/stable/installing/)

## Dependencies/Installation

- matplotlib

1. Install necessary Python libraries:
```bash
pip3 install matplotlib
brew install pybind11
brew install tcl-tk
```
2. Clean environment, then build C++ libraries:
```bash
make clean
make
```

## Running 2dwell

```bash
python 2dwell
```

## Notes

Make sure ```python``` resolves to ```python3``` in your path. The tutorial link for Python should be helpful with this.


