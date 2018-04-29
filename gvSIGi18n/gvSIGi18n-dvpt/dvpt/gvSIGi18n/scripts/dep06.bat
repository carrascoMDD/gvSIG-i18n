TIME /T
REM ******************
REM gvSIGi18n
REM ******************
attrib -R /S \\ACVP06\dvpt\Plone251\Data\Products\gvSIGi18n\*.*
del /S /Q \\ACVP06\dvpt\Plone251\Data\Products\gvSIGi18n\*.*
rmdir /Q /S \\ACVP06\dvpt\Plone251\Data\Products\gvSIGi18n
xcopy .\gvSIGi18n  \\ACVP06\dvpt\Plone251\Data\Products\gvSIGi18n /E /Y /I
attrib  +R /S \\ACVP06\dvpt\Plone251\Data\Products\gvSIGi18n\*.*
REM ******************
REM Extensions from gvSIGi18n
REM ******************
attrib -R /S \\ACVP06\dvpt\Plone251\Data\Extensions\*.*
xcopy .\gvSIGi18n\manualadditions\AsExternalMethodInSiteRoot  \\ACVP06\dvpt\Plone251\Data\\Extensions /E /Y /I /K
attrib  +R /S \\ACVP06\dvpt\Plone251\Data\Extensions\*.*
TIME /T
