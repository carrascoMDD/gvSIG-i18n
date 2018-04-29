#! /bin/bash

attrib ./gvSIGi18nTests/*.* -R /S

REM attrib ./gvSIGi18nTests_dep_sec/*.* -R /S

source ./overrideTests.sh

source ./deplightTests.sh

date