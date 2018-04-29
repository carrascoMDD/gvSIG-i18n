#! /bin/bash

source ./set_paths.sh


timestampstring=`date +%Y%m%d%H%M`
export timestampstring



pushd $MDDwork_path > /dev/null
rm ./archgenxml.log

rm -r ./gvSIGi18n

python $MDDagx_path/ArchGenXML.py $MDDsources_path/gvSIGi18n/model/gvSIGi18n.xmi
rm ./gvSIGi18n/i18n/generated.pot

pushd $MDDsources_path/gvSIGi18n/model > /dev/null
mv HTML gvSIGi18n-HTML
zip -r -q gvSIGi18n-HTML.zip gvSIGi18n-HTML
cp gvSIGi18n-HTML.zip $MDDwork_path/gvSIGi18n
rm -r gvSIGi18n-HTML
popd > /dev/null


popd > /dev/null
