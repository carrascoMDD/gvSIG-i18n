#! /bin/bash

echo
echo "deplightUI.sh"
echo

source ./set_paths.sh

echo
echo "deplightTool.sh"
echo

chmod -R go+r ${MDDwork_path}/gvSIGi18nTool
sudo -u zopei18n  cp -r ${MDDwork_path}/gvSIGi18nTool  "${MDDzopeinstance_path}/Products/gvSIGi18nTool"   
sudo -u zopei18n  cp ${MDDwork_path}/gvSIGi18nTool/manualadditions/AsExternalMethodInSiteRoot/TRA*.py  "${MDDzopeinstance_path}/Extensions"    
