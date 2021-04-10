MAIN = WellSolver
SUFFIX := $(shell python3-config --extension-suffix)
HEADERS = $(shell python3-config --includes)

all: main

main:
	g++ -O3 -Wall -shared -std=c++11 -undefined dynamic_lookup -I ${HEADERS} ${MAIN}.cpp -o ${MAIN}${SUFFIX}

clean:
	rm *.so
