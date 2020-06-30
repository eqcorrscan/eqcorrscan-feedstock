echo on

set "INCLUDE=%LIBRARY_INC%;%INCLUDE%"
set "LIB=%LIBRARY_LIB%;%LIB%"
copy %LIBRARY_LIB%\fftw3.lib %PREFIX%\lib\libfftw3-3.lib
copy %LIBRARY_LIB%\fftw3f.lib %PREFIX%\lib\libfftw3f-3.lib

%PYTHON% setup.py build
%PYTHON% setup.py install --single-version-externally-managed --record=record.txt
