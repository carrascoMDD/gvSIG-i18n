#! /bin/bash


source ./set_paths.sh

echo
echo "deplight.sh"
echo

chmod -R o+r ${MDDwork_path}/gvSIGi18n/*
sudo -u zopei18n  cp -r ${MDDwork_path}/gvSIGi18n  "${MDDzopeinstance_path}/Products/gvSIGi18n"   
