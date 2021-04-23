#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <Python.h>
#include "WellSolver.h"
#include <limits>
#include <iostream>
#include <math.h>
#include <random>

namespace py = pybind11;
using namespace std;

py::array_t<double> solve(double a, double b, int n, int e1, int e2) {
	random_device rand;
	default_random_engine eng(rand());
	uniform_real_distribution<double> dist_a(-a, a);
	uniform_real_distribution<double> dist_b(-b, b);
	double h = 1000.;
	double hx = 2*a/h;
	double hy = 2*b*h/n;
	int precision = 10;

	double *data = new double[n*2*precision];
	
	for (int i = 0; i < 2*n*precision; ++i) {
		data[i] = dist_a(eng);
		data[i+1] = dist_b(eng);
	}

	int i = 0;
	for (int x_index = 0; x_index < 2*a/hx; ++x_index) {
		for (int y_index = 0; y_index < 2*b/hy; ++y_index) {
			double x = -a + x_index*hx;
			double y = -b + y_index*hy;
			if (potential(a, b, x, y) < 1) {
				double weight = wavefunction(a, b, x, y, e1, e2);
				double prob_density = weight * weight;
				for (int j = 0; j < precision; ++j) {
					if (double(j)/double(precision) < prob_density && i < 2*n*precision) {
						data[i] = x;
						data[i+1] = y;
						i += 2;
					}
				}
			}
		}
	}

	/*for (int i = 0; i < n; i+=2) {
		data[i] = a*sin(double(i));
		data[i+1] = b*sin(double(i) / 2.);
	}*/

	py::capsule free_when_done(data, [](void *f) {
		double *data = reinterpret_cast<double *>(f);
		delete[] data;
	});
	
	auto result = py::array_t<double>(
		{n, 2*precision},
		{2*precision*sizeof(double), sizeof(double)},
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

double potential(double a, double b, double x, double y) {
	if (x*x/double(a*a)+y*y/double(b*b) < 1.) {
		return 0;
	}
	return numeric_limits<double>::max();
}

double wavefunction (double a, double b, double x, double y, int e1, int e2) {
	return sin(e1*M_PI*x/x_length(a, b, y))*sin(e2*M_PI*y/y_length(a, b, x));
}

double x_length (double a, double b, double y) {
	return a*sqrt(1-y*y/(b*b));
}

double y_length (double a, double b, double x) {
	return b*sqrt(1-x*x/(a*a));
}
