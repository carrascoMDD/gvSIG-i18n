attrib D:\dvpt\plone251\Data\Products\gvSIGi18nTests\*.* -R /S

call extensions-attrib.bat

del /Q /S /F D:\dvpt\plone251\Data\Products\gvSIGi18nTests\*.*

call deplightTests.bat
