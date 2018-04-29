#! /bin/bash

source ./set_paths.sh

echo
echo "overrideUI.sh"
echo

buildstring=`date +%Y%m%d%H%M`
export buildstring


rm -r $MDDwork_path/gvSIGi18nUI



mkdir "${MDDwork_path}/gvSIGi18nUI"
mkdir "${MDDwork_path}/gvSIGi18nUI/Extensions"
mkdir "${MDDwork_path}/gvSIGi18nUI/i18n"
mkdir "${MDDwork_path}/gvSIGi18nUI/skins"
mkdir "${MDDwork_path}/gvSIGi18nUI/skins/gvSIGi18nUI"
mkdir "${MDDwork_path}/gvSIGi18nUI/manualadditions"

cp ${MDDsources_path}/gvSIGi18nUI/additions/i18n/*.po ${MDDwork_path}/gvSIGi18nUI/i18n

rsync  -r --exclude=.svn  --exclude="*.bak" ${MDDsources_path}/gvSIGi18nUI/additions/objects/               ${MDDwork_path}/gvSIGi18nUI
rsync  -r --exclude=.svn  --exclude="*.bak" ${MDDsources_path}/gvSIGi18nUI/additions/skins/grids_i18n/      ${MDDwork_path}/gvSIGi18nUI/skins/gvSIGi18nUI
rsync  -r --exclude=.svn  --exclude="*.bak" ${MDDsources_path}/gvSIGi18nUI/additions/skins/icons/           ${MDDwork_path}/gvSIGi18nUI/skins/gvSIGi18nUI
rsync  -r --exclude=.svn  --exclude="*.bak" ${MDDsources_path}/gvSIGi18nUI/additions/skins/vistas/          ${MDDwork_path}/gvSIGi18nUI/skins/gvSIGi18nUI
rsync  -r --exclude=.svn  --exclude="*.bak" ${MDDsources_path}/gvSIGi18nUI/additions/skins/styles/          ${MDDwork_path}/gvSIGi18nUI/skins/gvSIGi18nUI
rsync  -r --exclude=.svn  --exclude="*.bak" ${MDDsources_path}/gvSIGi18nUI/additions/skins/scripts/         ${MDDwork_path}/gvSIGi18nUI/skins/gvSIGi18nUI
rsync  -r --exclude=.svn  --exclude="*.bak" ${MDDsources_path}/gvSIGi18nUI/additions/skins/interactions/    ${MDDwork_path}/gvSIGi18nUI/skins/gvSIGi18nUI
rsync  -r --exclude=.svn  --exclude="*.bak" ${MDDsources_path}/gvSIGi18nUI/manualadditions                  ${MDDwork_path}/gvSIGi18nUI

cp "${MDDwork_path}/gvSIGi18nUI/version_base.txt" "${MDDwork_path}/gvSIGi18nUI/version.txt"
printf "build%s" $buildstring >>"${MDDwork_path}/gvSIGi18nUI/version.txt"




pushd ${MDDwork_path} > /dev/null
zip -r -q gvSIGi18nUI.zip gvSIGi18nUI
cp gvSIGi18nUI.zip "gvSIGi18nUI-${buildstring}.zip"
cp gvSIGi18nUI.zip $MDDbase_path/generation
popd > /dev/null


mkdir $MDDbase_path/generation/gvSIGi18nUI
rsync  -r --exclude=.svn  --exclude="*.bak" ${MDDwork_path}/gvSIGi18nUI/  $MDDbase_path/generation/gvSIGi18nUI


source ./sou.sh








