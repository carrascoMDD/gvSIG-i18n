set buildstring=build%DATE:~6,4%%DATE:~3,2%%DATE:~0,2%%TIME:~0,2%%TIME:~3,2%
REM set buildstring=build%DATE:~0,4%%DATE:~5,2%%DATE:~8,2%%TIME:~0,2%%TIME:~3,2%
copy ..\sources\gvSIGi18nTool\additions\objects\version_base.txt ..\sources\gvSIGi18nTool\additions\objects\version.txt
echo %buildstring% >>..\sources\gvSIGi18nTool\additions\objects\version.txt



xcopy ..\sources\gvSIGi18nTool\additions\objects\*.*              .\gvSIGi18nTool /E /Y /I

xcopy ..\sources\gvSIGi18nTool\additions\skins\icons\*.*          .\gvSIGi18nTool\skins /E /Y /I


xcopy ..\sources\gvSIGi18nTool\manualadditions\*.*                .\gvSIGi18nTool\manualadditions /E /Y /I


call souTool.bat

del /S /Q .\gvSIGi18nTool\*.bak

attrib +R /S .\gvSIGi18nTool\*.*



