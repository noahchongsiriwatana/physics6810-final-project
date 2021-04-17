#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <Python.h>
#include "WellSolver.h"
#include <limits>
#include <iostream>
#include <math.h>

namespace py = pybind11;
using namespace std;

py::array_t<double> solve(int a, int b, int n, int e) {
	double *data = new double[n*2];
	
	for (int i = 0; i < 2*n; ++i) {
		data[i] = 0.;
	}

	for (int i = 0; i < n; i+=2) {
		data[i] = sin(double(i));
		data[i+1] = sin(double(i) / 2.);
	}

	py::capsule free_when_done(data, [](void *f) {
		double *data = reinterpret_cast<double *>(f);
		delete[] data;
	});
	
	auto result = py::array_t<double>(
		{n, 2},
		{2*sizeof(double), sizeof(double)},
		data,
		free_when_done
	);
	return result;
}

PYBIND11_MODULE(WellSolver, m) {
	m.doc() = "Python binding for WellSolver.";
	m.def("solve", &solve, "solve a 2D Well problem numerically.");
	//return m.ptr();
}

double potential(int a, int b, double x, double y) {
	if (x*x/double(a*a)+y*y/double(b*b) < 1.) {
		return 0;
	}
	return numeric_limits<double>::max();
}
