set buildstring=build%DATE:~6,4%%DATE:~3,2%%DATE:~0,2%%TIME:~0,2%%TIME:~3,2%
REM set buildstring=build%DATE:~0,4%%DATE:~5,2%%DATE:~8,2%%TIME:~0,2%%TIME:~3,2%
copy ..\sources\additions\objects\version_base.txt ..\sources\additions\objects\version.txt
echo %buildstring% >>..\sources\additions\objects\version.txt

xcopy ..\sources\additions\objects\*.*              .\gvSIGi18n /E /Y /I

copy /B .\gvSIGi18n\i18n\gvSIGi18n-es_justgen.po + ..\sources\additions\i18n\gvSIGi18n-es_handcrafted.po .\gvSIGi18n\i18n\gvSIGi18n-es.po /Y 
copy /B .\gvSIGi18n\i18n\gvSIGi18n-en_justgen.po + ..\sources\additions\i18n\gvSIGi18n-en_handcrafted.po .\gvSIGi18n\i18n\gvSIGi18n-en.po /Y 

copy /B .\gvSIGi18n\i18n\plone-gvSIGi18n-es_justgen.po + ..\sources\additions\i18n\plone-gvSIGi18n-es_handcrafted.po .\gvSIGi18n\i18n\plone-gvSIGi18n-es.po /Y 
copy /B .\gvSIGi18n\i18n\plone-gvSIGi18n-en_justgen.po + ..\sources\additions\i18n\plone-gvSIGi18n-en_handcrafted.po .\gvSIGi18n\i18n\plone-gvSIGi18n-en.po /Y 

copy ..\sources\additions\i18n\gvSIGi18n_credits-en.po .\gvSIGi18n\i18n\ /Y 
copy ..\sources\additions\i18n\gvSIGi18n_credits-es.po .\gvSIGi18n\i18n\ /Y 



xcopy ..\sources\additions\skins\icons\*.*          .\gvSIGi18n\skins\gvSIGi18n /E /Y /I
xcopy ..\sources\additions\skins\grids_i18n\*.*     .\gvSIGi18n\skins\gvSIGi18n /E /Y /I
xcopy ..\sources\additions\skins\vistas\*.*         .\gvSIGi18n\skins\gvSIGi18n /E /Y /I
xcopy ..\sources\additions\skins\styles\*.*         .\gvSIGi18n\skins\gvSIGi18n /E /Y /I
xcopy ..\sources\additions\skins\scripts\*.*        .\gvSIGi18n\skins\gvSIGi18n /E /Y /I
xcopy ..\sources\additions\skins\interactions\*.*   .\gvSIGi18n\skins\gvSIGi18n /E /Y /I

xcopy ..\sources\manualadditions\*.*                .\gvSIGi18n\manualadditions /E /Y /I

call sou.bat

del /S /Q .\gvSIGi18n\*.bak

attrib +R /S .\gvSIGi18n\*.*



