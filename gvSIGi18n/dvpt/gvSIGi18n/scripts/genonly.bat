del archgenxml.log

attrib .\gvSIGi18n\models -R /S
attrib .\gvSIGi18n\models\gvSIGi18n.EAP -R /S
attrib .\gvSIGi18n\models\gvSIGi18n.xmi -R /S
attrib .\gvSIGi18n\models\gvSIGi18n-HTML.zip -R /S



"D:\dvpt\Python24\python.exe" "D:\dvpt\ArchGenXML152ACV15\ArchGenXML.py" ..\sources\model\gvSIGi18n.xmi
del .\gvSIGi18n\i18n\generated.pot

copy .\gvSIGi18n\i18n\gvSIGi18n-es.po .\gvSIGi18n\i18n\gvSIGi18n-es_justgen.po
copy .\gvSIGi18n\i18n\gvSIGi18n-en.po .\gvSIGi18n\i18n\gvSIGi18n-en_justgen.po

copy .\gvSIGi18n\i18n\plone-gvSIGi18n-es.po .\gvSIGi18n\i18n\plone-gvSIGi18n-es_justgen.po
copy .\gvSIGi18n\i18n\plone-gvSIGi18n-en.po .\gvSIGi18n\i18n\plone-gvSIGi18n-en_justgen.po

del .\gvSIGi18n\i18n\gvSIGi18n-es.po
del .\gvSIGi18n\i18n\gvSIGi18n-en.po

copy .\gvSIGi18n\i18n\plone-gvSIGi18n-es.po .\gvSIGi18n\i18n\plone-gvSIGi18n-es_justgen.po
copy .\gvSIGi18n\i18n\plone-gvSIGi18n-en.po .\gvSIGi18n\i18n\plone-gvSIGi18n-en_justgen.po

del .\gvSIGi18n\i18n\gvSIGi18n-es.po
del .\gvSIGi18n\i18n\gvSIGi18n-en.po

del ..\sources\model\gvSIGi18n-HTML.zip

"C:\Program Files\7-Zip\7z" a -r -y  ..\sources\model\gvSIGi18n-HTML.zip ..\sources\model\HTML
