attrib D:\dvpt\plone251\Data\Products\gvSIGi18nTests\*.* -R /S

call extensions-attrib.bat

REM xcopy "D:\dvpt\plone251\Data\Products\gvSIGi18nTests" .\gvSIGi18nTests_dep_sec  /E /Y /I /K

xcopy .\gvSIGi18nTests  "D:\dvpt\plone251\Data\Products\gvSIGi18nTests" /E /Y /I /K


del /Q /S /F D:\dvpt\plone251\Data\Products\gvSIGi18nTests\*.bak
del /Q /S /F D:\dvpt\plone251\Data\Products\Extensions\*.bak