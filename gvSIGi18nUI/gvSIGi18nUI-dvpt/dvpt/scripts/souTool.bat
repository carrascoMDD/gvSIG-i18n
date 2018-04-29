
attrib .\dvpt -R /S

rmdir /S /Q .\dvpt

mkdir .\dvpt
mkdir .\dvpt\gvSIGi18nTool
mkdir .\dvpt\gvSIGi18nTool\scripts

xcopy ..\sources\gvSIGi18nTool\additions\*.*          .\dvpt\gvSIGi18nTool\additions\ /E /Y /I
xcopy ..\sources\gvSIGi18nTool\manualadditions\*.*    .\dvpt\gvSIGi18nTool\manualadditions\ /E /Y /I

xcopy .\*.bat   .\dvpt\scripts  /Y /I


attrib .\gvSIGi18nTool\gvSIGi18nTool-dvpt.zip -R

del /Q .\gvSIGi18nTool\gvSIGi18nTool-dvpt.zip

"C:\Program Files\7-Zip\7z" a -r -y  .\gvSIGi18nTool\gvSIGi18nTool-dvpt.zip .\dvpt

attrib .\gvSIGi18nTool\gvSIGi18nTool-dvpt.zip +R


REM leave to review. Shall be deleted at the beginning of the next execution of this script rmdir /S /Q .\dvpt