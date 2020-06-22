set C_INCLUDE_PATH="%PREFIX%\include"
set STATIC_FFTW_DIR="%PREFIX%\lib"
copy %LIBRARY_LIB%\fftw3.lib %LIBRARY_LIB%\libfftw3-3.lib
copy %LIBRARY_LIB%\fftw3f.lib %LIBRARY_LIB%\libfftw3f-3.lib

%PYTHON% setup.py build
%PYTHON% setup.py install --single-version-externally-managed --record=record.txt
