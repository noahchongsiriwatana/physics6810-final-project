/*
 * Author: Noah Chongsiriwatana
 *
 * Solves 2d infinite square well with elliptical boundary conditions.
 *
 * TODO: Use numerical methods to properly solve the elliptical boundary conditions,
 * 		Rather than by juxtaposing solutions to circular boundary conditions.
 * 		Try using boundary element method as described in link found in README.
 */

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <Python.h>
#include "WellSolver.h"
#include <limits>
#include <iostream>
#include <math.h>
#include <random>
#include <boost/math/special_functions/bessel.hpp>

namespace py = pybind11;
using namespace std;

/*
 * Porting function to generate points according to probability distribution.
 * 
 * Returns contiguous data and metadata to be interpreted by numpy.
 */
py::array_t<double> solve(double a, double b, int n, int e1, int e2) {
	
	/*
	 * Initialize data to random points.
	 * This is necessary because a variable number of points will be generated based on probability distribution,
	 * but pybind11 demands that a set memory structure be defined first.
	 */
	random_device rand;
	default_random_engine eng(rand());
	uniform_real_distribution<double> dist_a(-a, a);
	uniform_real_distribution<double> dist_b(-b, b);
	int precision = 10;

	/*
	 * Numpy compatible data must be carefully constructed as an array 
	 * with the size of the product of the shapes of the intended numpy array.
	 */
	double *data = new double[n*2*precision];
	
	for (int i = 0; i < 2*n*precision; ++i) {
		data[i] = dist_a(eng);
		data[i+1] = dist_b(eng);
	}

	/*
	 * Defines step sizes.
	 */
	double h = 1000.;
	double hx = 2*a/h;
	double hy = 2*b*h/n;	

	/*
	 * Generates points based on probability distribution.
	 */
	int i = 0;
	for (int x_index = 0; x_index < 2*a/hx; ++x_index) {
		for (int y_index = 0; y_index < 2*b/hy; ++y_index) {

			/*
			 * At each new (x, y) pair, generate points.
			 */
			double x = -a + x_index*hx;
			double y = -b + y_index*hy;
			if (potential(a, b, x, y) < 1) {
				
				/*
				 * Calculates probability density and generates associated number of points.
				 */
				double weight = wavefunction(a, b, x, y, e1, e2);
				double prob_density = weight * weight;
				for (int j = 0; j < precision; ++j) {
					if (double(j)/double(precision) < prob_density && i < 2*n*precision) {

						/*
						 * Every other value in array contains x and y values based on the shape definitions.
						 */
						data[i] = x;
						data[i+1] = y;
						i += 2;
					}
				}
			}
		}
	}

	/*
	 * Pybind11 requires explicit control over memory.
	 * This function is called when Python expects the garbage collector to free the numpy array.
	 */
	py::capsule free_when_done(data, [](void *f) {
		double *data = reinterpret_cast<double *>(f);
		delete[] data;
	});
	
	/*
	 * Stores and returns data, metadata, and destructor function to help python access/destroy memory.
	 */
	auto result = py::array_t<double>(
		{n, 2*precision},
		{2*precision*sizeof(double), sizeof(double)},
		data,
		free_when_done
	);
	return result;
}

/*
 * Binds some light documentation with the solve function to be exported as a python compatible module.
 */
PYBIND11_MODULE(WellSolver, m) {
	m.doc() = "Python binding for WellSolver.";
	m.def("solve", &solve, "solve a 2D Well problem numerically.");
}

/*
 * Represents infinite elliptical well with 0 inside and a large number outside.
 */
double potential(double a, double b, double x, double y) {
	if (x*x/double(a*a)+y*y/double(b*b) < 1.) {
		return 0;
	}
	return numeric_limits<double>::max();
}

/*
 * Calculates the wavefunction using the spherical harmonics and bessels functions.
 * 
 * This technique is imperfect for elliptical bounds, especially at high eccentricity.
 * TODO: Use numerical methods to properly solve this problem.
 */
double wavefunction (double a, double b, double x, double y, int e1, int e2) {
	double theta = atan2(y, x);
	return radial(a, b, sqrt(x*x+y*y), theta, e1, e2) * angular(theta, e2);
}

/*
 * Calculates the radial component of wavefunction.
 */
double radial (double a, double b, double r, double theta, int k, int l) {
	double x_rel = a*sin(theta);
	double y_rel = b*cos(theta);
	double r_rel = a*b/sqrt(x_rel*x_rel + y_rel*y_rel);
	double N = sqrt(k);
	double z = boost::math::cyl_bessel_j_zero(double(l), k);
	return N*jn(l, z*r/r_rel);
}

/*
 * Calculates angular component of wavefunction.
 */
double angular (double theta, int l) {
	double N = pow((l+1), 2.);
	return N*cos(theta*l);
}
