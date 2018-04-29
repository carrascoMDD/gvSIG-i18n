
attrib .\dvpt -R /S

rmdir /S /Q .\dvpt

mkdir .\dvpt
mkdir .\dvpt\gvSIGi18n
mkdir .\dvpt\gvSIGi18n\model
mkdir .\dvpt\scripts



xcopy ..\sources\gvSIGi18n\additions\*.*            .\dvpt\gvSIGi18n\additions\ /E /Y /I

copy  ..\sources\gvSIGi18n\model\gvSIGi18n.EAP      .\dvpt\gvSIGi18n\model\gvSIGi18n.EAP
copy  ..\sources\gvSIGi18n\model\gvSIGi18n.xmi      .\dvpt\gvSIGi18n\model\gvSIGi18n.xmi

copy  ..\sources\gvSIGi18n\model\gvSIGi18n-HTML.zip .\dvpt\gvSIGi18n\model\gvSIGi18n-HTML.zip 

xcopy .\*.bat   .\dvpt\scripts  /Y /I




copy "D:\Works\MDD\Plone\ArchGenXML152ACV\ArchGenXML152ACV15wksp\distros\ArchGenXML152ACV15b20091202.zip" .\dvpt\
copy "D:\Works\MDD\Plone\gvSIGi18n\TRA0103wk\ThirdParty\distros\CJKSplitter073.zip" .\dvpt\
copy "D:\Works\MDD\Plone\gvSIGi18n\TRA0103wk\ThirdParty\distros\ZopeChinaPak082.zip" .\dvpt\

copy "D:\Works\MDD\Plone\ModelDDvlPlone\DVL0401wk\generation\ModelDDvlPlone.zip" .\dvpt\
copy "D:\Works\MDD\Plone\ModelDDvlPlone\DVL0401wk\generation\ModelDDvlPloneTool.zip" .\dvpt\
copy "D:\Works\MDD\Plone\ModelDDvlPlone\DVL0401wk\generation\ModelDDvlPloneConfiguration.zip" .\dvpt\


attrib .\gvSIGi18n\gvSIGi18n-dvpt.zip -R

del /Q .\gvSIGi18n\gvSIGi18n-dvpt.zip

"C:\Program Files\7-Zip\7z" a -r -y  .\gvSIGi18n\gvSIGi18n-dvpt.zip .\dvpt

attrib .\gvSIGi18n\gvSIGi18n-dvpt.zip +R


REM leave to review. Shall be deleted at the beginning of the next execution of this script rmdir /S /Q .\dvpt