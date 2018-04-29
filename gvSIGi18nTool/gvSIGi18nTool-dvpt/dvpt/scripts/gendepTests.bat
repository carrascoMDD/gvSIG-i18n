attrib .\gvSIGi18nTests\*.* -R /S
attrib .\gvSIGi18nTests_dep_sec -R /S
del /Q /S /F .\gvSIGi18nTests\*.*
REM not for Tests product call genonlyTests.bat
call overrideTests.bat
call depTests.bat
Time /T