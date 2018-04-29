#! /bin/bash

attrib ./gvSIGi18nTests/*.* -R /S
REM attrib ./gvSIGi18nTests_dep_sec -R /S
del /Q /S /F ./gvSIGi18nTests/*.*
REM not for Tests product source ./genonlyTests.sh
source ./overrideTests.sh
source ./depTests.sh
date