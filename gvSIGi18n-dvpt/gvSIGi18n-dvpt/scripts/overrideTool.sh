#! /bin/bash

source ./set_paths.sh

echo
echo "overrideTool.sh"
echo

buildstring=`date +%Y%m%d%H%M`
export buildstring


rm -r $MDDwork_path/gvSIGi18nTool



mkdir "${MDDwork_path}/gvSIGi18nTool"
mkdir "${MDDwork_path}/gvSIGi18nTool/i18n"
mkdir "${MDDwork_path}/gvSIGi18nTool/skins"
mkdir "${MDDwork_path}/gvSIGi18nTool/manualadditions"

cp ${MDDsources_path}/gvSIGi18nTool/additions/i18n/*.po ${MDDwork_path}/gvSIGi18nTool/i18n

rsync  -r --exclude=.svn  --exclude="*.bak" ${MDDsources_path}/gvSIGi18nTool/additions/objects/               ${MDDwork_path}/gvSIGi18nTool
rsync  -r --exclude=.svn  --exclude="*.bak" ${MDDsources_path}/gvSIGi18nTool/additions/skins/icons/            ${MDDwork_path}/gvSIGi18nTool/skins
rsync  -r --exclude=.svn  --exclude="*.bak" ${MDDsources_path}/gvSIGi18nTool/manualadditions                  ${MDDwork_path}/gvSIGi18nTool

cp "${MDDwork_path}/gvSIGi18nTool/version_base.txt" "${MDDwork_path}/gvSIGi18nTool/version.txt"
printf "build%s" $buildstring >>"${MDDwork_path}/gvSIGi18nTool/version.txt"




pushd ${MDDwork_path} > /dev/null
zip -r -q gvSIGi18nTool.zip gvSIGi18nTool
cp gvSIGi18nTool.zip "gvSIGi18nTool-${buildstring}.zip"
cp gvSIGi18nTool.zip $MDDbase_path/generation
popd > /dev/null


mkdir $MDDbase_path/generation/gvSIGi18nTool
rsync  -r --exclude=.svn  --exclude="*.bak" ${MDDwork_path}/gvSIGi18nTool/  $MDDbase_path/generation/gvSIGi18nTool

source ./sou.sh








