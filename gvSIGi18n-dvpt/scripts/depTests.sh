#! /bin/bash

attrib D:/dvpt/plone251/Data/Products/gvSIGi18nTests/*.* -R /S

source ./extensions-attrib.sh

del /Q /S /F D:/dvpt/plone251/Data/Products/gvSIGi18nTests/*.*

source ./deplightTests.sh
