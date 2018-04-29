#! /bin/bash

source ./set_paths.sh

echo
echo "sou.sh"
echo

soustring=`date +%Y%m%d%H%M`
export soustring


rm -r "${MDDwork_path}/gvSIGi18n-dvpt"

mkdir  "${MDDwork_path}/gvSIGi18n-dvpt"
mkdir  "${MDDwork_path}/gvSIGi18n-dvpt/gvSIGi18n"
mkdir  "${MDDwork_path}/gvSIGi18n-dvpt/gvSIGi18n/model"
mkdir  "${MDDwork_path}/gvSIGi18n-dvpt/gvSIGi18n/i18n"
mkdir  "${MDDwork_path}/gvSIGi18n-dvpt/gvSIGi18nUI"
mkdir  "${MDDwork_path}/gvSIGi18n-dvpt/gvSIGi18nTool"
mkdir  "${MDDwork_path}/gvSIGi18n-dvpt/scripts"
mkdir  "${MDDwork_path}/gvSIGi18n-dvpt/bats"




rsync  -r --exclude=.svn --exclude="*.bak" ${MDDsources_path}/gvSIGi18n/additions           ${MDDwork_path}/gvSIGi18n-dvpt/gvSIGi18n

cp ${MDDsources_path}/gvSIGi18n/model/gvSIGi18n.EAP      ${MDDwork_path}/gvSIGi18n-dvpt/gvSIGi18n/model
cp ${MDDsources_path}/gvSIGi18n/model/gvSIGi18n.xmi      ${MDDwork_path}/gvSIGi18n-dvpt/gvSIGi18n/model
cp ${MDDsources_path}/gvSIGi18n/model/gvSIGi18n-HTML.zip ${MDDwork_path}/gvSIGi18n-dvpt/gvSIGi18n/model

rsync  -r --exclude=.svn --exclude="*.bak" ${MDDsources_path}/gvSIGi18nUI/additions           ${MDDwork_path}/gvSIGi18n-dvpt/gvSIGi18nUI
rsync  -r --exclude=.svn --exclude="*.bak" ${MDDsources_path}/gvSIGi18nUI/manualadditions     ${MDDwork_path}/gvSIGi18n-dvpt/gvSIGi18nUI
rsync  -r --exclude=.svn --exclude="*.bak" ${MDDsources_path}/gvSIGi18nTool/additions         ${MDDwork_path}/gvSIGi18n-dvpt/gvSIGi18nTool
rsync  -r --exclude=.svn --exclude="*.bak" ${MDDsources_path}/gvSIGi18nTool/manualadditions   ${MDDwork_path}/gvSIGi18n-dvpt/gvSIGi18nTool

cp ./*.sh    "${MDDwork_path}/gvSIGi18n-dvpt/scripts"
cp ${MDDbase_path}/generation/*.bat    "${MDDwork_path}/gvSIGi18n-dvpt/bats"



cp "${MDDagx_path}/../ArchGenXML152ACV15.zip" ${MDDwork_path}/gvSIGi18n-dvpt/
cp "${MDDthirdparty_path}/CJKSplitter073.zip" ${MDDwork_path}/gvSIGi18n-dvpt/
cp "${MDDthirdparty_path}/ZopeChinaPak082.zip" ${MDDwork_path}/gvSIGi18n-dvpt/

rm "${MDDwork_path}/gvSIGi18n-dvpt.zip"
rm "${MDDwork_path}/gvSIGi18n-dvpt-${soustring}.zip"

pushd "${MDDwork_path}" > /dev/null
zip -r -q gvSIGi18n-dvpt.zip gvSIGi18n-dvpt
cp gvSIGi18n-dvpt.zip "gvSIGi18n-dvpt-${soustring}.zip"
cp gvSIGi18n-dvpt.zip $MDDbase_path/generation
cp ./gvSIGi18n/gvSIGi18n-HTML.zip $MDDbase_path/generation

popd > /dev/null




