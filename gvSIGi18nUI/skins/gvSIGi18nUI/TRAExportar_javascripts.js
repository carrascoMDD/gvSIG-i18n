/*
# File: TRAExportar_javascripts.js
#
# Copyright (c) 2008, 2009, 2010 by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
# Authors: 
# Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana 
# Model Driven Development sl  Valencia (Spain) www.ModelDD.org 
# Antonio Carrasco Valero                       carrasco@ModelDD.org
#
#
*/

// $Id: TRAExportar_javascripts.js 30984 2009-04-30 10:00:00Z carrasco $



/* #################################################################
Scripts to be executed by user agent (WebBrowser)
################################################################# */



function pTRASelectEncodingToExportLanguage( theEncodingUseToSelect) {

    if ( !theEncodingUseToSelect) {
        return false;
    }
    
    if ( theEncodingUseToSelect == 'Java .properties') {
        unEncodingUseToSelect = 'JavaProperties';
    }
    else {
        unEncodingUseToSelect = 'PO';
    }
    
    for( unIdCounter=0; unIdCounter < 10000; unIdCounter++) {
        var unEncodingValueHolderElement = document.getElementById( 'cid_EncodingToExportLanguage_' + unEncodingUseToSelect + '_' + unIdCounter);
        if ( !unEncodingValueHolderElement) {
            break;
        }
        unEncodingValue = '';
        if ( unEncodingValueHolderElement.firstChild) {
            unEncodingValue = unEncodingValueHolderElement.firstChild.data;
        }
        for( unOptionIdCounter=0; unOptionIdCounter < 10000; unOptionIdCounter++) {
            var unEncodingOptionElement = document.getElementById( 'cid_EncodingToExportLanguage_' + unIdCounter + '_' + unOptionIdCounter);
            if ( !unEncodingOptionElement) {
                break;
            }
            unEncodingOptionValue = unEncodingOptionElement.value;
            if ( unEncodingOptionValue == unEncodingValue) {
                unEncodingOptionElement.selected = true;
            }
            else {
                unEncodingOptionElement.selected = false;
            }
        }
    }
    return true;
}

                             
 
 
 

function pTRAToggleAllLanguages() {
    var unElementAllLanguages = document.getElementById( 'cid_TRAToggleAllLanguages')
    if ( !unElementAllLanguages) {
        return false;
    }
    var unNewValueForAllLanguages = unElementAllLanguages.checked;
    for( unIdCounter=0; unIdCounter < 10000; unIdCounter++) {

        var unCheckBox = document.getElementById( 'cid_LanguageToExport-' + unIdCounter );
        if ( !unCheckBox) {
            break;
        }
        unCheckBox.checked = unNewValueForAllLanguages
    }
    return true;
}




function pTRAToggleAllModules() {
    var unElementAllModules = document.getElementById( 'cid_TRAToggleAllModules')
    if ( !unElementAllModules) {
        return false;
    }
    var unNewValueForAllModules = unElementAllModules.checked;
    for( unIdCounter=0; unIdCounter < 10000; unIdCounter++) {

        var unCheckBox = document.getElementById( 'cid_ModuleToExport-' + unIdCounter );
        if ( !unCheckBox) {
            break;
        }
        unCheckBox.checked = unNewValueForAllModules;
    }
    var unCheckBox = document.getElementById( 'mod-ModuloNoEspecificado' );
    if ( unCheckBox) {
        unCheckBox.checked = unNewValueForAllModules;
    }
    return true;
}




function fTRASelectedCommonEncoding() {
    return false;
}




function pTRASetEncodingsToCommon() {
    var unElementCommonEncoding = document.getElementById( 'cid_TRASetToCommonEncoding')
    if ( !unElementCommonEncoding) {
        return false;
    }
    
    var unSelectedEncodingOptionElement = null;
    var unValueCommonEncoding = '';
    
    for( unOptionIdCounter=0; unOptionIdCounter < 10000; unOptionIdCounter++) {
        var unEncodingOptionElement = document.getElementById( 'cid_TRASetToCommonEncoding_' + unOptionIdCounter);
        if ( !unEncodingOptionElement) {
            break;
        }
        if ( unEncodingOptionElement.selected) {
            unSelectedEncodingOptionElement = unEncodingOptionElement;
            unValueCommonEncoding = unEncodingOptionElement.value;
            break;
        }
    }
    
    if ( (!unSelectedEncodingOptionElement) || ( !unValueCommonEncoding) || ( unValueCommonEncoding.length < 1)) {
        return false;
    }
    unSelectedEncodingOptionElement.selected =  false;
    
    for( unIdCounter=0; unIdCounter < 10000; unIdCounter++) {
        for( unOptionIdCounter=0; unOptionIdCounter < 10000; unOptionIdCounter++) {
            var unEncodingOptionElement = document.getElementById( 'cid_EncodingToExportLanguage_' + unIdCounter + '_' + unOptionIdCounter);
            if ( !unEncodingOptionElement) {
                break;
            }
            unEncodingOptionValue = unEncodingOptionElement.value;
            if ( unEncodingOptionValue == unValueCommonEncoding) {
                unEncodingOptionElement.selected = true;
            }
            else {
                unEncodingOptionElement.selected = false;
            }
        }
    }
    return true;
}


