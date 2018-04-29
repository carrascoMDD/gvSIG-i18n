#! /bin/bash

echo
echo "depTool.sh"
echo

source ./set_paths.sh


rm -r ${MDDwork_path}/gvSIGi18nTool_dep_sec
sudo cp -r "${MDDzopeinstance_path}/Products/gvSIGi18nTool" ${MDDwork_path}/gvSIGi18nTool_dep_sec    
sudo chown -R $MDDuserid:$MDDgroupid  ${MDDwork_path}/gvSIGi18nTool_dep_sec
sudo rm -r "${MDDzopeinstance_path}/Products/gvSIGi18nTool"
source ./deplightTool.sh

