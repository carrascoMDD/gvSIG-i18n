#! /bin/bash


source ./set_paths.sh

echo
echo "override.sh"
echo

buildstring=`date +%Y%m%d%H%M`
export buildstring


mkdir "${MDDwork_path}/gvSIGi18n/Extensions"
mkdir "${MDDwork_path}/gvSIGi18n/i18n"
mkdir "${MDDwork_path}/gvSIGi18n/skins"
mkdir "${MDDwork_path}/gvSIGi18n/skins/gvSIGi18n"

rsync  -r --exclude=.svn  --exclude="*.bak" ${MDDsources_path}/gvSIGi18n/additions/objects/           ${MDDwork_path}/gvSIGi18n
rsync  -r --exclude=.svn  --exclude="*.bak" ${MDDsources_path}/gvSIGi18n/additions/objects/Extensions/        ${MDDwork_path}/gvSIGi18n/Extensions
rsync  -r --exclude=.svn  --exclude="*.bak" ${MDDsources_path}/gvSIGi18n/additions/skins/icons/       ${MDDwork_path}/gvSIGi18n/skins/gvSIGi18n


cp "${MDDwork_path}/gvSIGi18n/version_base.txt" "${MDDwork_path}/gvSIGi18n/version.txt"
printf "build%s" $buildstring >>"${MDDwork_path}/gvSIGi18n/version.txt"


pushd ${MDDwork_path} > /dev/null
zip -r -q gvSIGi18n.zip gvSIGi18n
cp gvSIGi18n.zip "gvSIGi18n-${buildstring}.zip"
cp gvSIGi18n.zip $MDDbase_path/generation
popd > /dev/null


mkdir $MDDbase_path/generation/gvSIGi18n
rsync  -r --exclude=.svn  --exclude="*.bak" ${MDDwork_path}/gvSIGi18n/  $MDDbase_path/generation/gvSIGi18n

source ./sou.sh





