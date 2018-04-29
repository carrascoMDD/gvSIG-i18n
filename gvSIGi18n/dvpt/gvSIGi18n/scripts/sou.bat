
attrib .\gvSIGi18n\dvpt -R /S

rmdir /S /Q .\gvSIGi18n\dvpt

mkdir .\gvSIGi18n\dvpt
mkdir .\gvSIGi18n\dvpt\gvSIGi18n
mkdir .\gvSIGi18n\dvpt\gvSIGi18n\model
mkdir .\gvSIGi18n\dvpt\gvSIGi18n\scripts

xcopy ..\sources\additions\*.*          .\gvSIGi18n\dvpt\gvSIGi18n\additions\ /E /Y /I
xcopy ..\sources\manualadditions\*.*    .\gvSIGi18n\dvpt\gvSIGi18n\manualadditions\ /E /Y /I

copy ..\sources\model\gvSIGi18n.EAP .\gvSIGi18n\dvpt\gvSIGi18n\model\gvSIGi18n.EAP
copy ..\sources\model\gvSIGi18n.xmi .\gvSIGi18n\dvpt\gvSIGi18n\model\gvSIGi18n.xmi

copy  ..\sources\model\gvSIGi18n-HTML.zip .\gvSIGi18n\dvpt\gvSIGi18n\model\gvSIGi18n-HTML.zip 


xcopy .\*.bat   .\gvSIGi18n\dvpt\gvSIGi18n\scripts  /Y /I


copy "D:\Works\MDD\Plone\ArchGenXML152ACV\ArchGenXML152ACV15wksp\ArchGenXML152ACV15b20091202.zip" .\gvSIGi18n\dvpt\ArchGenXML152ACV15b20091202.zip 

"C:\Program Files\7-Zip\7z" a -r -y  .\gvSIGi18n\gvSIGi18n-dvpt.zip .\gvSIGi18n\dvpt

rmdir /S /Q .\gvSIGi18n\dvpt