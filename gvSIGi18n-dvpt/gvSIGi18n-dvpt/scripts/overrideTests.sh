#! /bin/bash

set buildstring=build%DATE:~6,4%%DATE:~3,2%%DATE:~0,2%%TIME:~0,2%%TIME:~3,2%
REM set buildstring=build%DATE:~0,4%%DATE:~5,2%%DATE:~8,2%%TIME:~0,2%%TIME:~3,2%
copy ../sources/gvSIGi18nTests/additions/objects/version_base.txt ../sources/gvSIGi18nTests/additions/objects/version.txt
echo %buildstring% >>../sources/gvSIGi18nTests/additions/objects/version.txt

xcopy ../sources/gvSIGi18nTests/additions/objects/*.*              ./gvSIGi18nTests /E /Y /I

xcopy ../sources/gvSIGi18nTests/additions/skins/*.*          ./gvSIGi18nTests/skins/gvSIGi18nTests /E /Y /I


source ./souTests.sh

del /S /Q ./gvSIGi18nTests/*.bak

attrib +R /S ./gvSIGi18nTests/*.*



