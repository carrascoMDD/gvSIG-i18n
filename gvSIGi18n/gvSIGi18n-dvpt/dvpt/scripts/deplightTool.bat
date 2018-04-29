attrib D:\dvpt\plone251\Data\Products\gvSIGi18nTool\*.* -R /S

call extensions-attrib.bat

xcopy "D:\dvpt\plone251\Data\Products\gvSIGi18nTool" .\gvSIGi18nTool_dep_sec  /E /Y /I /K

xcopy .\gvSIGi18nTool  "D:\dvpt\plone251\Data\Products\gvSIGi18nTool" /E /Y /I /K
xcopy .\gvSIGi18nTool\manualadditions\AsExternalMethodInSiteRoot  "D:\dvpt\plone251\Data\Extensions" /E /Y /I /K

del /Q /S /F D:\dvpt\plone251\Data\Products\gvSIGi18nTool\*.bak
del /Q /S /F D:\dvpt\plone251\Data\Products\Extensions\*.bak