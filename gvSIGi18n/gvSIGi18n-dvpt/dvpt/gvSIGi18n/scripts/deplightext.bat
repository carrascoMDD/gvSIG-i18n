call extensions-attrib.bat

xcopy "D:\dvpt\plone251\Data\Products\gvSIGi18n\manualadditions\AsExternalMethodInSiteRoot" .\gvSIGi18n_dep_sec\manualadditions\AsExternalMethodInSiteRoot  /E /Y /I /K

xcopy .\gvSIGi18n\manualadditions\AsExternalMethodInSiteRoot  "D:\dvpt\plone251\Data\Extensions" /E /Y /I /K

del /Q /S /F D:\dvpt\plone251\Data\Products\Extensions\*.bak