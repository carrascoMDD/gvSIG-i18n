#! /bin/bash

echo
echo "deplightUI.sh"
echo

source ./set_paths.sh

chmod -R go+r ${MDDwork_path}/gvSIGi18nUI
sudo -u zopei18n  cp -r ${MDDwork_path}/gvSIGi18nUI  "${MDDzopeinstance_path}/Products/gvSIGi18nUI"   
sudo -u zopei18n  cp ${MDDwork_path}/gvSIGi18nUI/manualadditions/AsExternalMethodInSiteRoot/TRA*.py  "${MDDzopeinstance_path}/Extensions"    

