attrib .\gvSIGi18nTests\*.* -R /S

attrib .\gvSIGi18nTests_dep_sec\*.* -R /S

call overrideTests.bat

call deplightTests.bat

Time /T