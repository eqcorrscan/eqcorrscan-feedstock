echo on

set C_INCLUDE_PATH="%PREFIX%\include"
set STATIC_FFTW_DIR="%LIBRARY_LIB%\lib"

set "INCLUDE=%LIBRARY_INC%;%INCLUDE%"
set "LIB=%LIBRARY_LIB%;%LIB%"
copy %LIBRARY_LIB%\fftw3.lib %LIBRARY_LIB%\libfftw3-3.lib
copy %LIBRARY_LIB%\fftw3f.lib %LIBRARY_LIB%\libfftw3f-3.lib

echo %C_INCLUDE_PATH%
echo %STATIC_FFTW_DIR%
echo %LIB%
echo %INCLUDE%

%PYTHON% setup.py build
%PYTHON% setup.py install --single-version-externally-managed --record=record.txt
