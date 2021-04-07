import cffi
import invoke
import pathlib
		
@invoke.task()
def build_well_solver(c):
	ffi = cffi.FFI()
	current_dir = pathlib.Path().absolute()
	h_file_name = current_dir / "WellSolver.h"
	with open(h_file_name) as h_file:
		ffi.cdef(h_file.read())
	ffi.set_source(
		"WellSolver",
		'#include "WellSolver.h"',
		libraries=["WellSolver"],
		library_dirs=[current_dir.as_posix()],
		extra_link_args=["-Wl,-rpath,."]
	)
	ffi.compile()
