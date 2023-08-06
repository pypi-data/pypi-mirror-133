# makemakef
Command to create a Makefile to build nicely written Fortran code.


## Usage
```
# For build .exe
makemakef -rc -s .F90 -n main.exe -fc gfortran

# For build .a
makemakef -rc -s .F90 -n libname.a -fc gfortran -lib

# Run make
make builddir  # create directories for build
make all  # or make test if test code exists
```
