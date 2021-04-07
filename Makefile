main = WellSolver

all: main

main:
	g++ ${main}.cpp -c -o ${main}.o
	g++ -dynamiclib -fPIC -o lib${main}.dylib ${main}.o
	invoke build-well-solver
