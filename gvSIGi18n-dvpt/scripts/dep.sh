#! /bin/bash


source ./set_paths.sh


rm -r ${MDDwork_path}/gvSIGi18n_dep_sec
sudo cp -r "${MDDzopeinstance_path}/Products/gvSIGi18n" ${MDDwork_path}/gvSIGi18n_dep_sec    
sudo chown -R $MDDuserid:$MDDgroupid  ${MDDwork_path}/gvSIGi18n_dep_sec
sudo rm -r "${MDDzopeinstance_path}/Products/gvSIGi18n"
source ./deplight.sh
