#! /bin/bash

# file: depprod_gvsigi18n.sh

# ###################
# Scripted deployment
# for ModelDDvlPlone
# run as user zopei18n

ZopeInstancePath="/var/lib/zope2.9/instance/zgvsigi18n"
export ZopeInstancePath

DeliveriesPath="/home/zopei18n/Deliveries"
export DeliveriesPath

ExtractPath="/home/zopei18n/Extract"
export ExtractPath

gvSIGi18nName="gvSIGi18n-2.2.0b201305081955"
export gvSIGi18nName

mkdir $ExtractPath

cp "${DeliveriesPath}/${gvSIGi18nName}.tar.gz" $ExtractPath


pushd $ExtractPath


rm ${gvSIGi18nName}.tar
rm -r -f ${gvSIGi18nName}

echo
echo "unpack archive"
gunzip "${gvSIGi18nName}.tar.gz"

echo
echo "Extract from tar"
tar -xf "${gvSIGi18nName}.tar"


echo
echo "After extract from tar"
ls


# Plone products already installed
echo
echo "#########################"
echo "Products: Before delete current"
echo
ls -l $ZopeInstancePath/Products/

# Remove current products

rm -r -f $ZopeInstancePath/Products/ZopeChinaPak
rm -r -f $ZopeInstancePath/Products/CJKSplitter
rm -r -f $ZopeInstancePath/Products/gvSIGi18n
rm -r -f $ZopeInstancePath/Products/gvSIGi18nUI
rm -r -f $ZopeInstancePath/Products/gvSIGi18nTool

# Plone products  after removal
echo
echo "#########################"
echo "Products: After delete current"
echo
ls -l $ZopeInstancePath/Products/


# Install new releases of products

cp -r "${ExtractPath}/${gvSIGi18nName}/To_Plone_instance_Products/ZopeChinaPak" $ZopeInstancePath/Products

cp -r "${ExtractPath}/${gvSIGi18nName}/To_Plone_instance_Products/CJKSplitter" $ZopeInstancePath/Products

cp -r "${ExtractPath}/${gvSIGi18nName}/To_Plone_instance_Products/gvSIGi18n" $ZopeInstancePath/Products

cp -r "${ExtractPath}/${gvSIGi18nName}/To_Plone_instance_Products/gvSIGi18nUI" $ZopeInstancePath/Products

cp -r "${ExtractPath}/${gvSIGi18nName}/To_Plone_instance_Products/gvSIGi18nTool" $ZopeInstancePath/Products


# Plone products after copy
echo
echo "#########################"
echo "Products: After install new release"
echo
ls -l $ZopeInstancePath/Products/



# ##########################
# ExternalMethods and other files must be made available to Extensions folder of each instance,


# Files in the external methods directory, before copying
echo
echo "#########################"
echo "Extensions: Before delete current"
echo
ls -l $ZopeInstancePath/Extensions


# Remove current extensions
echo
echo "#########################"
echo "Extensions: After delete current"
echo
rm -f $ZopeInstancePath/Extensions/TRA*.py

# Files in the external methods directory, after removal
ls -l $ZopeInstancePath/Extensions

#  Ext methods from Components for gvSIGi18n application

cp $ZopeInstancePath/Products/gvSIGi18nUI/manualadditions/AsExternalMethodInSiteRoot/* $ZopeInstancePath/Extensions

cp $ZopeInstancePath/Products/gvSIGi18nTool/manualadditions/AsExternalMethodInSiteRoot/* $ZopeInstancePath/Extensions



# Files in the external methods directory, AFTER copying
echo
echo "#########################"
echo "Extensions: After install new release"
echo
ls -l $ZopeInstancePath/Extensions

popd

