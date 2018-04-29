
attrib .\dvpt -R /S

rmdir /S /Q .\dvpt

mkdir .\dvpt
mkdir .\dvpt\gvSIGi18nUI
mkdir .\dvpt\scripts

xcopy ..\sources\gvSIGi18nUI\additions\*.*          .\dvpt\gvSIGi18nUI\additions\ /E /Y /I
xcopy ..\sources\gvSIGi18nUI\manualadditions\*.*    .\dvpt\gvSIGi18nUI\manualadditions\ /E /Y /I

xcopy .\*.bat   .\dvpt\scripts  /Y /I


attrib .\gvSIGi18nUI\gvSIGi18nUI-dvpt.zip -R

del /Q .\gvSIGi18nUI\gvSIGi18nUI-dvpt.zip

"C:\Program Files\7-Zip\7z" a -r -y  .\gvSIGi18nUI\gvSIGi18nUI-dvpt.zip .\dvpt

attrib .\gvSIGi18nUI\gvSIGi18nUI-dvpt.zip +R


REM leave to review. Shall be deleted at the beginning of the next execution of this script rmdir /S /Q .\dvpt