#ifndef WELLSOLVER_H
#define WELLSOLVER_H

double potential(double a, double b, double x, double y);
double wavefunction (double a, double b, double x, double y, int e1, int e2);
double x_length (double a, double b, double y);
double y_length (double a, double b, double x);
double radial (double a, double b, double r, double theta, int z, int l);
double angular (double theta, int l);

#endif
