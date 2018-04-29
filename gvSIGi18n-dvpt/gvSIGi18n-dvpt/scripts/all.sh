#! /bin/bash

# for f in *.bat; do mv $f `basename $f .sh`.sh; done;

./gendep.sh
./gendepUI.sh
./gendepTool.sh
date