
attrib .\dvpt -R /S

rmdir /S /Q .\dvpt

mkdir .\dvpt
mkdir .\dvpt\gvSIGi18nTests
mkdir .\dvpt\scripts

xcopy ..\sources\gvSIGi18nTests\additions\*.*            .\dvpt\gvSIGi18nTests\additions\ /E /Y /I
xcopy ..\sources\gvSIGi18nTests\manualadditions\*.*      .\dvpt\gvSIGi18nTests\manualadditions\ /E /Y /I

xcopy .\*.bat   .\dvpt\scripts  /Y /I


attrib .\gvSIGi18nTests\gvSIGi18nTests-dvpt.zip -R

del /Q .\gvSIGi18nTests\gvSIGi18nTests-dvpt.zip

"C:\Program Files\7-Zip\7z" a -r -y  .\gvSIGi18nTests\gvSIGi18nTests-dvpt.zip .\dvpt

attrib .\gvSIGi18nTests\gvSIGi18nTests-dvpt.zip +R


REM leave to review. Shall be deleted at the beginning of the next execution of this script rmdir /S /Q .\dvpt