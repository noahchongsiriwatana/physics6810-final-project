#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <Python.h>
#include "WellSolver.h"
#include <iostream>

namespace py = pybind11;
using namespace std;

py::array_t<double> solve(int a, int b) {
	cout << "test_noah" << endl;
	double *data = new double[2];
	data[0] = 1.;
	data[1] = 2.;
	py::capsule free_func(data, [](void *f) {
		double *data = reinterpret_cast<double *>(f);
		delete[] data;
	});
	auto result = py::array_t<double>(
		{2},
		{sizeof(double)},
		data,
		free_func
	);
	return result;
}

PYBIND11_MODULE(WellSolver, m) {
	m.doc() = "Python binding for WellSolver.";
	m.def("solve", &solve, "solve a 2D Well problem numerically.");
	//return m.ptr();
}
