attrib .\gvSIGi18nTool\*.* -R /S
attrib .\gvSIGi18nTool_dep_sec -R /S
del /Q /S /F .\gvSIGi18nTool\*.*
call overrideTool.bat
call depTool.bat
Time /T