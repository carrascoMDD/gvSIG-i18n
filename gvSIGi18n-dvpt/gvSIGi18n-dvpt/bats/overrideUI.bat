set buildstring=build%DATE:~6,4%%DATE:~3,2%%DATE:~0,2%%TIME:~0,2%%TIME:~3,2%
REM set buildstring=build%DATE:~0,4%%DATE:~5,2%%DATE:~8,2%%TIME:~0,2%%TIME:~3,2%
copy ..\sources\gvSIGi18nUI\additions\objects\version_base.txt ..\sources\gvSIGi18nUI\additions\objects\version.txt
echo %buildstring% >>..\sources\gvSIGi18nUI\additions\objects\version.txt



xcopy ..\sources\gvSIGi18nUI\additions\objects\*.*              .\gvSIGi18nUI /E /Y /I

xcopy ..\sources\gvSIGi18nUI\additions\i18n\*.po                .\gvSIGi18nUI\i18n\ /E /Y /I

xcopy ..\sources\gvSIGi18nUI\additions\skins\icons\*.*          .\gvSIGi18nUI\skins\gvSIGi18nUI /E /Y /I
xcopy ..\sources\gvSIGi18nUI\additions\skins\grids_i18n\*.*     .\gvSIGi18nUI\skins\gvSIGi18nUI /E /Y /I
xcopy ..\sources\gvSIGi18nUI\additions\skins\vistas\*.*         .\gvSIGi18nUI\skins\gvSIGi18nUI /E /Y /I
xcopy ..\sources\gvSIGi18nUI\additions\skins\styles\*.*         .\gvSIGi18nUI\skins\gvSIGi18nUI /E /Y /I
xcopy ..\sources\gvSIGi18nUI\additions\skins\scripts\*.*        .\gvSIGi18nUI\skins\gvSIGi18nUI /E /Y /I
xcopy ..\sources\gvSIGi18nUI\additions\skins\interactions\*.*   .\gvSIGi18nUI\skins\gvSIGi18nUI /E /Y /I

xcopy ..\sources\gvSIGi18nUI\manualadditions\*.*                .\gvSIGi18nUI\manualadditions /E /Y /I

call souUI.bat

del /S /Q .\gvSIGi18nUI\*.bak

attrib +R /S .\gvSIGi18nUI\*.*



