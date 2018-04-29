set buildstring=build%DATE:~6,4%%DATE:~3,2%%DATE:~0,2%%TIME:~0,2%%TIME:~3,2%
REM set buildstring=build%DATE:~0,4%%DATE:~5,2%%DATE:~8,2%%TIME:~0,2%%TIME:~3,2%
copy ..\sources\gvSIGi18n\additions\objects\version_base.txt ..\sources\gvSIGi18n\additions\objects\version.txt
echo %buildstring% >>..\sources\gvSIGi18n\additions\objects\version.txt

xcopy ..\sources\gvSIGi18n\additions\objects\*.*              .\gvSIGi18n /E /Y /I

xcopy ..\sources\gvSIGi18n\additions\skins\icons\*.*          .\gvSIGi18n\skins\gvSIGi18n /E /Y /I


call sou.bat

del /S /Q .\gvSIGi18n\*.bak

attrib +R /S .\gvSIGi18n\*.*



