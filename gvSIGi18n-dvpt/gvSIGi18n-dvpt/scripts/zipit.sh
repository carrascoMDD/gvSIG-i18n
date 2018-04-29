#! /bin/bash

REM set MDDtimestamp=_%DATE:~0,4%%DATE:~5,2%%DATE:~8,2%%TIME:~0,2%%TIME:~3,2%
set MDDtimestamp=_%DATE:~6,4%%DATE:~3,2%%DATE:~0,2%%TIME:~0,2%%TIME:~3,2%%1%
echo "%MDDtimestamp%"
"C:/Program Files/7-Zip/7z" a -r -y  ../../TRA0200wk"%MDDtimestamp%".zip ../*.*
date

