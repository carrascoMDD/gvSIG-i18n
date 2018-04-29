attrib D:\dvpt\plone251\Data\Products\gvSIGi18n\*.* -R /S

call extensions-attrib.bat

xcopy "D:\dvpt\plone251\Data\Products\gvSIGi18n" .\gvSIGi18n_dep_sec  /E /Y /I /K

xcopy .\gvSIGi18n  "D:\dvpt\plone251\Data\Products\gvSIGi18n" /E /Y /I /K


del /Q /S /F D:\dvpt\plone251\Data\Products\gvSIGi18n\*.bak
del /Q /S /F D:\dvpt\plone251\Data\Products\Extensions\*.bak