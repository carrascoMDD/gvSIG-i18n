attrib .\gvSIGi18nTool\*.* -R /S
REM attrib .\gvSIGi18nTool_dep_sec -R /S
del /Q /S /F .\gvSIGi18nTool\*.*
call overrideTool.bat
call depTool.bat
Time /T