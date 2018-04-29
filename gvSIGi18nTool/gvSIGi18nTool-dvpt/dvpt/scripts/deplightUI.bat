attrib D:\dvpt\plone251\Data\Products\gvSIGi18nUI\*.* -R /S

call extensions-attrib.bat

xcopy "D:\dvpt\plone251\Data\Products\gvSIGi18nUI" .\gvSIGi18nUI_dep_sec  /E /Y /I /K

xcopy .\gvSIGi18nUI  "D:\dvpt\plone251\Data\Products\gvSIGi18nUI" /E /Y /I /K
xcopy .\gvSIGi18nUI\manualadditions\AsExternalMethodInSiteRoot  "D:\dvpt\plone251\Data\Extensions" /E /Y /I /K

del /Q /S /F D:\dvpt\plone251\Data\Products\gvSIGi18nUI\*.bak
del /Q /S /F D:\dvpt\plone251\Data\Products\Extensions\*.bak