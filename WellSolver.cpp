#include <pybind11/pybind11.h>
#include <Python.h>
#include "WellSolver.h"
#include <iostream>

namespace py = pybind11;
using namespace std;

int test_function() {
	cout << "test_noah" << endl;
	return 0;
}

PYBIND11_MODULE(WellSolver, m) {
	m.doc() = "Python binding for WellSolver.";
	m.def("test_function", &test_function, "test function");
}
