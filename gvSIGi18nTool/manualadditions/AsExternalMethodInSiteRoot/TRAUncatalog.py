# -*- coding: utf-8 -*-
#
# File: TRAUncatalog.py
#
# Copyright (c) 2008,2009,2010 by Model Driven Development sl and Antonio Carrasco Valero
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
# Model Driven Development sl  Valencia (Spain) www.ModelDD.org 
# Antonio Carrasco Valero                       carrasco@ModelDD.org
#

__author__ = """Model Driven Development sl <ModelDDvlPlone@ModelDD.org>,
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'

import sys
import traceback
import logging



from Products.CMFCore.utils              import getToolByName





_cTRATodosNombresTiposDesCatalogables_DePortalCatalog = [
    "ZCatalog",
    "TRACatalogo",                       
    "TRAIdioma",                         
    "TRAModulo",                         
    "TRAImportacion",                    
    "TRAContenidoIntercambio",           
    "TRAContenidoXML",                   
    "TRAInforme",                        
    "TRASolicitudCadena",                
    "TRAProgreso",                       
    "TRAParametrosControlProgreso",      
    "TRAConfiguracionImportacion",       
    "TRAConfiguracionExportacion",       
    "TRAConfiguracionSolicitudesCadenas",
    "TRAConfiguracionInvalidacionInformes",    
    "TRAConfiguracionPaginaTraducciones",
    "TRAConfiguracionPerfilEjecucion",   
    "TRAConfiguracionVarios",            
    "TRAConfiguracionPermisos",          
    "TRASimbolosOrdenados",              
    "TRAColeccionIdiomas",               
    "TRAColeccionModulos",               
    "TRAColeccionCadenas",               
    "TRAColeccionInformes",              
    "TRAColeccionImportaciones",         
    "TRAColeccionSolicitudesCadenas",    
    "TRAColeccionProgresos",
    "ATImage",
    "ATNewsItem",
    "ATDocument",
    "ATLink",
    "ATFolder",
]



_cTRATodosNombresTiposCatalogables_ChildrenExcluidosDePortalCatalog = [
    "TRAColeccionCadenas",               
]

_cTRATodosNombresTiposNODesCatalogables_DeUIDCatalog = [ 'ZCatalog',]




def _fNewVoidTypesToUncatalogReport():
    aReport = {
        'types_to_uncatalog_from_portal_catalog':  [],
        'types_to_uncatalog_children_excluded':    [],
        'types_not_to_uncatalog_from_uid_catalog': [],
     }
    return aReport
    


def _fNewVoidUncatalogReport():
    aReport = {
        'success':     False,
        'status':      '',
        'condition':   '',
        'initial_id':  '',
        
        'types_to_uncatalog': {},
        
        'total_num_elements':      0,
        'types_and_num_elements':  [],
        'elements_by_type':        {},
        
        'uid_total_num_elements':      0,
        'uid_types_and_num_elements':  [],
        'uid_elements_by_type':        {},
        
        
        'failed_total_num_elements':      0,
        'failed_types_and_num_elements':  [],
        'failed_elements_by_type':        {},
        
        'failed_uid_total_num_elements':      0,
        'failed_uid_types_and_num_elements':  [],
        'failed_uid_elements_by_type':        {},
    }
    return aReport
    




    
    
    

def TRAUncatalog( 
    theContextualElement     =None, 
    theInitialId             ='',
    theJustReportTypes       =False):
    """Exposed as an ExternalMethod.
    
    """
    
    aUncatalogReport = _fNewVoidUncatalogReport()
    
    aTypesToUncatalogReport = _fNewVoidTypesToUncatalogReport()
    aTypesToUncatalogReport.update( {
        'types_to_uncatalog_from_portal_catalog':  sorted( ( _cTRATodosNombresTiposDesCatalogables_DePortalCatalog               and _cTRATodosNombresTiposDesCatalogables_DePortalCatalog[:])               or []),
        'types_to_uncatalog_children_excluded':    sorted( ( _cTRATodosNombresTiposCatalogables_ChildrenExcluidosDePortalCatalog and _cTRATodosNombresTiposCatalogables_ChildrenExcluidosDePortalCatalog[:]) or []),
        'types_not_to_uncatalog_from_uid_catalog': sorted( ( _cTRATodosNombresTiposNODesCatalogables_DeUIDCatalog                and _cTRATodosNombresTiposNODesCatalogables_DeUIDCatalog[:])                or []),     
    })
    aUncatalogReport[ 'types_to_uncatalog'] = aTypesToUncatalogReport
    
    if theJustReportTypes:
        aUncatalogReport.update( {
            'success':     True,
            'status':      'JustReportTypes',
            'condition':   '',
        })
        return aUncatalogReport
        
    
    
    
    if theContextualElement == None:
        aUncatalogReport.update( {
            'success':     False,
            'status':      'MissingParameter',
            'condition':   'theContextualElement',
        })
        return aUncatalogReport

    
    anInitialId = theInitialId
    if anInitialId:
        anInitialId = anInitialId.strip()
        
   
    
    if not anInitialId:
        aUncatalogReport.update( {
            'success':     False,
            'status':      'MissingParameter',
            'condition':   'anInitialId',
        })
        return aUncatalogReport
    
    aUncatalogReport[ 'initial_id'] = anInitialId

   
    if not _fCheckHasRole( theContextualElement, 'Manager'):
        aUncatalogReport.update( {
            'success':     False,
            'status':      'User without required role',
            'condition':   'Manager',
        })
        return aUncatalogReport


    
    
    aInitialElementToUncatalog = None
    
    someContentElements = theContextualElement.objectValues()
    if someContentElements:
        for aContentElement in someContentElements:
            anElementId = aContentElement.getId()
            if anElementId:
                if anElementId == anInitialId:
                    aInitialElementToUncatalog = aContentElement
                    break
                
    
    anUIDCatalog = getToolByName( theContextualElement, 'uid_catalog', None)
                
    if not ( aInitialElementToUncatalog == None):
        _TRAUncatalog_recursive(
            theInitialElement        =aInitialElementToUncatalog, 
            theUncatalogReport       =aUncatalogReport,
            theUIDCatalog            =anUIDCatalog,
        )
        
        
    someTypesAndNumElements = [ ]
    aTotalNumElements = 0
    
    someElementsByType = aUncatalogReport.get( 'elements_by_type', {})
    if not ( someElementsByType == None):   
        someMetaTypes = someElementsByType.keys()
        someMetaTypes = sorted( someMetaTypes)
        
        for aMetaType in someMetaTypes:
            aNumElementsOfType = someElementsByType.get( aMetaType, 0)
            someTypesAndNumElements.append( [ aMetaType, aNumElementsOfType, ])
            aTotalNumElements += aNumElementsOfType
            
            
    aUncatalogReport[ 'types_and_num_elements'] = someTypesAndNumElements
    
        
    someFailedTypesAndNumElements = [ ]
    aFailedTotalNumElements = 0
    
    someFailedElementsByType = aUncatalogReport.get( 'failed_elements_by_type', {})
    if not ( someFailedElementsByType == None):   
        someMetaTypes = someFailedElementsByType.keys()
        someMetaTypes = sorted( someMetaTypes)
        
        for aMetaType in someMetaTypes:
            aNumElementsOfType = someFailedElementsByType.get( aMetaType, 0)
            someFailedTypesAndNumElements.append( [ aMetaType, aNumElementsOfType, ])
            aFailedTotalNumElements += aNumElementsOfType
            
            
    aUncatalogReport[ 'types_and_num_elements'] = someTypesAndNumElements
    
      
    
    someUIDTypesAndNumElements = [ ]    
    aUIDTotalNumElements = 0
    
    someUIDElementsByType = aUncatalogReport.get( 'uid_elements_by_type', {})
    if not ( someUIDElementsByType == None):   
        someUIDMetaTypes = someUIDElementsByType.keys()
        someUIDMetaTypes = sorted( someUIDMetaTypes)
        
        for aMetaType in someUIDMetaTypes:
            aUIDNumElementsOfType = someUIDElementsByType.get( aMetaType, 0)
            someUIDTypesAndNumElements.append( [ aMetaType, aUIDNumElementsOfType, ])
            aUIDTotalNumElements += aUIDNumElementsOfType
            

    someFailedUIDTypesAndNumElements = [ ]    
    aFailedUIDTotalNumElements = 0
    
    someFailedUIDElementsByType = aUncatalogReport.get( 'failed_uid_elements_by_type', {})
    if not ( someFailedUIDElementsByType == None):   
        someUIDMetaTypes = someFailedUIDElementsByType.keys()
        someUIDMetaTypes = sorted( someUIDMetaTypes)
        
        for aMetaType in someUIDMetaTypes:
            aUIDNumElementsOfType = someFailedUIDElementsByType.get( aMetaType, 0)
            someFailedUIDTypesAndNumElements.append( [ aMetaType, aUIDNumElementsOfType, ])
            aFailedUIDTotalNumElements += aUIDNumElementsOfType
            
        
    aUncatalogReport.update( {
        'success':     True,
        
        'total_num_elements':         aTotalNumElements,
        'types_and_num_elements':     someTypesAndNumElements,
        'uid_total_num_elements':     aUIDTotalNumElements,
        'uid_types_and_num_elements': someUIDTypesAndNumElements,
        
        'failed_total_num_elements':         aFailedTotalNumElements,
        'failed_types_and_num_elements':     someFailedTypesAndNumElements,
        'failed_uid_total_num_elements':     aFailedUIDTotalNumElements,
        'failed_uid_types_and_num_elements': someFailedUIDTypesAndNumElements
        
    })
    
    return aUncatalogReport

    
    


def _TRAUncatalog_recursive( 
    theInitialElement        =None, 
    theUncatalogReport       =None,
    theUIDCatalog            =None):
    """Recursively remove from theCatalogs theInitialElement and recursive content elements except the contents of the specified types, recording results in theUncatalogReport.
    
    """
    
    if theInitialElement == None:
        return None

    if theUncatalogReport == None:
        return None


    aMetaType = ''
    try:
        aMetaType = theInitialElement.meta_type
    except:
        None
    if not aMetaType:
        return None
    
    if not ( aMetaType in _cTRATodosNombresTiposDesCatalogables_DePortalCatalog):
        return None
    
        
    if not( aMetaType in _cTRATodosNombresTiposCatalogables_ChildrenExcluidosDePortalCatalog):
        someContentElements = theInitialElement.objectValues()
        if someContentElements:
            for aContentElement in someContentElements:
                _TRAUncatalog_recursive(
                    theInitialElement        =aContentElement, 
                    theUncatalogReport       =theUncatalogReport,
                    theUIDCatalog            =theUIDCatalog,
                )            
                  
    
    aIsUncatalogged = False
    try:
        theInitialElement.unindexObject()
        aIsUncatalogged = True
    except:
        None
        
    if aIsUncatalogged:
        if aMetaType:
            someElementsByType = theUncatalogReport.get( 'elements_by_type', {})
            if not ( someElementsByType == None):
                someElementsByType[ aMetaType] = someElementsByType.get( aMetaType, 0) + 1
        
                
    else:
        if aMetaType:
            someFailedElementsByType = theUncatalogReport.get( 'failed_elements_by_type', {})
            if not ( someFailedElementsByType == None):
                someFailedElementsByType[ aMetaType] = someFailedElementsByType.get( aMetaType, 0) + 1
        
        
                
    if not ( theUIDCatalog == None):
        if aMetaType:
            if not ( aMetaType in _cTRATodosNombresTiposNODesCatalogables_DeUIDCatalog):
                aIsUIDUncatalogged = False
                try:
                    aInitialElementURL = theInitialElement._getURL()
                    if aInitialElementURL:
                        theUIDCatalog.uncatalog_object(aInitialElementURL)
                        aIsUIDUncatalogged = True
                except:
                    None
                
                if aIsUIDUncatalogged:
                    if aMetaType:
                        someElementsByType = theUncatalogReport.get( 'uid_elements_by_type', {})
                        if not ( someElementsByType == None):
                            someElementsByType[ aMetaType] = someElementsByType.get( aMetaType, 0) + 1
                else:
                    if aMetaType:
                        someFailedElementsByType = theUncatalogReport.get( 'failed_uid_elements_by_type', {})
                        if not ( someFailedElementsByType == None):
                            someFailedElementsByType[ aMetaType] = someFailedElementsByType.get( aMetaType, 0) + 1
            
    
    
    return None

    




def _fCheckHasRole( theContextualElement=None, theRole=''):
    if ( theContextualElement == None):
        return False
    
    if not theRole:
        return False
       
    unaRequest = theContextualElement.REQUEST
    if not unaRequest:
        return None
    
    unUserObject = unaRequest.get("AUTHENTICATED_USER", None)
    
    unosRoles = unUserObject.getRolesInContext( theContextualElement)
    if not unosRoles:
        return False
    
    aHasRole = theRole in unosRoles
    
    return aHasRole


