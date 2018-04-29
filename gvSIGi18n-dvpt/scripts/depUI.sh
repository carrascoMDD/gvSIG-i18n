#! /bin/bash

echo
echo "depUI.sh"
echo

source ./set_paths.sh


rm -r ${MDDwork_path}/gvSIGi18nUI_dep_sec
sudo cp -r "${MDDzopeinstance_path}/Products/gvSIGi18nUI" ${MDDwork_path}/gvSIGi18nUI_dep_sec    
sudo chown -R $MDDuserid:$MDDgroupid  ${MDDwork_path}/gvSIGi18nUI_dep_sec
sudo rm -r "${MDDzopeinstance_path}/Products/gvSIGi18nUI"
source ./deplightUI.sh
