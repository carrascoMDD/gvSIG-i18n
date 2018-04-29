attrib .\gvSIGi18n\*.* -R /S

del /Q /S /F .\gvSIGi18n\*.*

call genonly.bat

call override.bat
