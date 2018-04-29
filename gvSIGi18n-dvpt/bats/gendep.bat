attrib .\gvSIGi18n\*.* -R /S
REM  attrib .\gvSIGi18n_dep_sec -R /S
del /Q /S /F .\gvSIGi18n\*.*
call genonly.bat
call override.bat
call dep.bat
Time /T