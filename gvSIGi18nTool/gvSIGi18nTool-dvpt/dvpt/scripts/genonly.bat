del archgenxml.log

attrib .\gvSIGi18n\models -R /S
attrib .\gvSIGi18n\models\gvSIGi18n.EAP -R /S
attrib .\gvSIGi18n\models\gvSIGi18n.xmi -R /S
attrib .\gvSIGi18n\models\gvSIGi18n-HTML.zip -R /S


"D:\dvpt\Python24\python.exe" "D:\dvpt\ArchGenXML152ACV15\ArchGenXML.py" ..\sources\gvSIGi18n\model\gvSIGi18n.xmi
del .\gvSIGi18n\i18n\generated.pot

"C:\Program Files\7-Zip\7z" a -r -y  ..\sources\gvSIGi18n\model\gvSIGi18n-HTML.zip ..\sources\gvSIGi18n\model\HTML
