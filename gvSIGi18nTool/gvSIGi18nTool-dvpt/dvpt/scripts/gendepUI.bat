attrib .\gvSIGi18nUI\*.* -R /S
REM attrib .\gvSIGi18nUI_dep_sec -R /S
del /Q /S /F .\gvSIGi18nUI\*.*
REM not for UI product call genonlyUI.bat
call overrideUI.bat
call depUI.bat
Time /T