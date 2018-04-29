#! /bin/bash

source ./set_paths.sh

echo 
echo "deliver.sh"
echo

buildstring=`date +%Y%m%d%H%M`
export buildstring


rm -r  "${MDDdeliverwork_path}/gvSIGi18n"
mkdir "${MDDdeliverwork_path}/gvSIGi18n"
mkdir "${MDDdeliverwork_path}/gvSIGi18n/To_Plone_instance_Products"
mkdir "${MDDdeliverwork_path}/gvSIGi18n/To_Plone_instance_Extensions"


rsync  -r --exclude=.svn  --exclude="*.bak" $MDDbase_path/generation/gvSIGi18n              ${MDDdeliverwork_path}/gvSIGi18n/To_Plone_instance_Products
rsync  -r --exclude=.svn  --exclude="*.bak" $MDDbase_path/generation/gvSIGi18nTool          ${MDDdeliverwork_path}/gvSIGi18n/To_Plone_instance_Products
rsync  -r --exclude=.svn  --exclude="*.bak" $MDDbase_path/generation/gvSIGi18nUI ${MDDdeliverwork_path}/gvSIGi18n/To_Plone_instance_Products

rsync  -r --exclude=.svn  --exclude="*.bak"  $MDDbase_path/generation/gvSIGi18nTool/manualadditions/AsExternalMethodInSiteRoot/       ${MDDdeliverwork_path}/gvSIGi18n/To_Plone_instance_Extensions
rsync  -r --exclude=.svn  --exclude="*.bak"  $MDDbase_path/generation/gvSIGi18nUI/manualadditions/AsExternalMethodInSiteRoot/       ${MDDdeliverwork_path}/gvSIGi18n/To_Plone_instance_Extensions

rsync  -r --exclude=.svn  --exclude="*.bak" $MDDbase_path/ThirdParty/CJKSplitter          ${MDDdeliverwork_path}/gvSIGi18n/To_Plone_instance_Products
rsync  -r --exclude=.svn  --exclude="*.bak" $MDDbase_path/ThirdParty/ZopeChinaPak          ${MDDdeliverwork_path}/gvSIGi18n/To_Plone_instance_Products


cp $MDDbase_path/generation/gvSIGi18n-dvpt.zip          ${MDDdeliverwork_path}/gvSIGi18n

cp ${MDDdeliverwork_path}/gvSIGi18n/To_Plone_instance_Products/gvSIGi18n/version_base.txt ${MDDdeliverwork_path}/gvSIGi18n/To_Plone_instance_Products/gvSIGi18n/version.txt
printf "b%s" $buildstring >>"${MDDdeliverwork_path}/gvSIGi18n/To_Plone_instance_Products/gvSIGi18n/version.txt"

cp ${MDDdeliverwork_path}/gvSIGi18n/To_Plone_instance_Products/gvSIGi18nTool/version_base.txt ${MDDdeliverwork_path}/gvSIGi18n/To_Plone_instance_Products/gvSIGi18nTool/version.txt
printf "b%s" $buildstring >>"${MDDdeliverwork_path}/gvSIGi18n/To_Plone_instance_Products/gvSIGi18nTool/version.txt"

cp ${MDDdeliverwork_path}/gvSIGi18n/To_Plone_instance_Products/gvSIGi18nUI/version_base.txt ${MDDdeliverwork_path}/gvSIGi18n/To_Plone_instance_Products/gvSIGi18nUI/version.txt
printf "b%s" $buildstring >>"${MDDdeliverwork_path}/gvSIGi18n/To_Plone_instance_Products/gvSIGi18nUI/version.txt"

MDDversion=`cat ${MDDdeliverwork_path}/gvSIGi18n/To_Plone_instance_Products/gvSIGi18n/version.txt`
export MDDversion


mv ${MDDdeliverwork_path}/gvSIGi18n ${MDDdeliverwork_path}/gvSIGi18n-${MDDversion}


pushd ${MDDdeliverwork_path} > /dev/null
rm gvSIGi18n-${MDDversion}.zip
zip -r -q gvSIGi18n-${MDDversion}.zip gvSIGi18n-${MDDversion}
cp gvSIGi18n-${MDDversion}.zip $MDDbase_path/delivery

rm gvSIGi18n-${MDDversion}.tar
tar -cvf gvSIGi18n-${MDDversion}.tar gvSIGi18n-${MDDversion}
gzip gvSIGi18n-${MDDversion}.tar
cp gvSIGi18n-${MDDversion}.tar.gz $MDDbase_path/delivery

popd > /dev/null
