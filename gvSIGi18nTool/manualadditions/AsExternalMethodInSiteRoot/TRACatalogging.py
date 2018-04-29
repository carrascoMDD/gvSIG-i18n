# -*- coding: utf-8 -*-
#
# File: TRACatalogging.py
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

import transaction


from time import time


from Products.CMFCore.utils              import getToolByName


cTRAMaxElementsPerTransaction    = 1000



cTRACataloggingAction_DoCatalog = 'DoCatalog'
cTRACataloggingAction_UnCatalog = 'UnCatalog'

cTRACataloggingActions = [ cTRACataloggingAction_DoCatalog, cTRACataloggingAction_UnCatalog,]


_cBPDTodosNombresTiposEnPortalCatalog = [
    "BPDArtefacto",
    "BPDCaracteristica",
    "BPDColeccionArtefactos",
    "BPDColeccionEntradas",
    "BPDColeccionHerramientas",
    "BPDColeccionPasos",
    "BPDColeccionPerfiles",
    "BPDColeccionPoliticasDeNegocio",
    "BPDColeccionProcesosDeNegocio",
    "BPDColeccionReglasDeNegocio",
    "BPDColeccionSalidas",
    "BPDColeccionUnidadesOrganizacionales",
    "BPDDecision",
    "BPDEntrada",
    "BPDEnvio",
    "BPDExitoFinal",
    "BPDExtensionProceso",
    "BPDFracasoFinal",
    "BPDHerramienta",
    "BPDOrganizacion",
    "BPDPasoGestorExcepciones",
    "BPDPasoSimple",
    "BPDPerfil",
    "BPDPlazo",
    "BPDPoliticaDeNegocio",
    "BPDProcesoDeNegocioSimple",
    "BPDPuntoExtension",
    "BPDRecepcion",
    "BPDReferenciaCualificada",
    "BPDReglaDeNegocio",
    "BPDSalida",
    "BPDSubProceso",
    "BPDUnidadOrganizacional",
    "BPDUsoArtefacto",
    "BPDUsoCaracteristica",
]




_cTRATodosNombresTiposEnPortalCatalog = [
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



_cTodosNombresTiposEnPortalCatalog = _cTRATodosNombresTiposEnPortalCatalog+ _cBPDTodosNombresTiposEnPortalCatalog



_cTodosNombresTiposEnPortalCatalog_ChildrenExcluidos = [
    "TRAColeccionCadenas",               
]

_cTRATodosNombresTiposNOEnUIDCatalog = [ 'ZCatalog',]




def _fNewVoidTypesEnCataloggingReport():
    aReport = {
        'types_in_portal_catalog':  [],
        'types_in_portal_catalog_children_excluded':    [],
        'types_not_en_uid_catalog': [],
     }
    return aReport
    


def _fNewVoidCataloggingReport():
    aReport = {
        'action':      '',
        'confirmation_value': '',
        'success':     False,
        'status':      '',
        'condition':   '',
        'initial_id':  '',
        
        'types_in_portal_catalog_reports': {},
        
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
    




    
    
    

def TRACatalogging( 
    theContextualElement     =None, 
    theInitialId             ='',
    theJustReportTypes       =False,
    theCataloggingAction     =False,):
    """Exposed as an ExternalMethod.
    
    """
    
    aCataloggingReport = _fNewVoidCataloggingReport()
    
    aCataloggingReport[ 'action'] = theCataloggingAction
    
    
    if theContextualElement == None:
        aCataloggingReport.update( {
            'success':     False,
            'status':      'MissingParameter',
            'condition':   'theContextualElement',
        })
        return aCataloggingReport

    
    if not _fCheckHasRole( theContextualElement, 'Manager'):
        aCataloggingReport.update( {
            'success':     False,
            'status':      'User without required role',
            'condition':   'Manager',
        })
        return aCataloggingReport
        
    aCataloggingReport[ 'confirmation_value'] = str( int( time() * 1000))
    
    
    aTypesEnCataloggingReport = _fNewVoidTypesEnCataloggingReport()
    aTypesEnCataloggingReport.update( {
        'types_in_portal_catalog':  sorted( ( _cTodosNombresTiposEnPortalCatalog               and _cTodosNombresTiposEnPortalCatalog[:])               or []),
        'types_in_portal_catalog_children_excluded':    sorted( ( _cTodosNombresTiposEnPortalCatalog_ChildrenExcluidos and _cTodosNombresTiposEnPortalCatalog_ChildrenExcluidos[:]) or []),
        'types_not_en_uid_catalog': sorted( ( _cTRATodosNombresTiposNOEnUIDCatalog                and _cTRATodosNombresTiposNOEnUIDCatalog[:])                or []),     
    })
    aCataloggingReport[ 'types_in_portal_catalog_reports'] = aTypesEnCataloggingReport
    
    if theJustReportTypes:
        aCataloggingReport.update( {
            'success':     True,
            'status':      'JustReportTypes',
            'condition':   '',
        })
        return aCataloggingReport
        
    
    
    if ( not theCataloggingAction) or not ( theCataloggingAction in cTRACataloggingActions):
        aCataloggingReport.update( {
            'success':     False,
            'status':      'theCataloggingAction is not one of %s %s' % (cTRACataloggingAction_DoCatalog, cTRACataloggingAction_UnCatalog),
            'condition':   '',
        })
        return aCataloggingReport
            

    
    anInitialId = theInitialId
    if anInitialId:
        anInitialId = anInitialId.strip()
        
   
    
    if not anInitialId:
        aCataloggingReport.update( {
            'success':     False,
            'status':      'MissingParameter',
            'condition':   'anInitialId',
        })
        return aCataloggingReport
    
    aCataloggingReport[ 'initial_id'] = anInitialId

   


    
    
    aInitialElementEnCatalogging = None
    
    someContentElements = theContextualElement.objectValues()
    if someContentElements:
        for aContentElement in someContentElements:
            anElementId = aContentElement.getId()
            if anElementId:
                if anElementId == anInitialId:
                    aInitialElementEnCatalogging = aContentElement
                    break
                
    
    anUIDCatalog = getToolByName( theContextualElement, 'uid_catalog', None)
                
    if not ( aInitialElementEnCatalogging == None):
        
        aTransactionCounterHolder = [ 0,]
        
        _TRACatalogging_recursive(
            theInitialElement        =aInitialElementEnCatalogging, 
            theCataloggingReport     =aCataloggingReport,
            theUIDCatalog            =anUIDCatalog,
            theCataloggingAction     =theCataloggingAction,
            theTransactionCounterHolder=aTransactionCounterHolder,
        )
        
        transaction.commit()
        
        
        
    someTypesAndNumElements = [ ]
    aTotalNumElements = 0
    
    someElementsByType = aCataloggingReport.get( 'elements_by_type', {})
    if not ( someElementsByType == None):   
        someMetaTypes = someElementsByType.keys()
        someMetaTypes = sorted( someMetaTypes)
        
        for aMetaType in someMetaTypes:
            aNumElementsOfType = someElementsByType.get( aMetaType, 0)
            someTypesAndNumElements.append( [ aMetaType, aNumElementsOfType, ])
            aTotalNumElements += aNumElementsOfType
            
            
    aCataloggingReport[ 'types_and_num_elements'] = someTypesAndNumElements
    
        
    someFailedTypesAndNumElements = [ ]
    aFailedTotalNumElements = 0
    
    someFailedElementsByType = aCataloggingReport.get( 'failed_elements_by_type', {})
    if not ( someFailedElementsByType == None):   
        someMetaTypes = someFailedElementsByType.keys()
        someMetaTypes = sorted( someMetaTypes)
        
        for aMetaType in someMetaTypes:
            aNumElementsOfType = someFailedElementsByType.get( aMetaType, 0)
            someFailedTypesAndNumElements.append( [ aMetaType, aNumElementsOfType, ])
            aFailedTotalNumElements += aNumElementsOfType
            
            
    aCataloggingReport[ 'types_and_num_elements'] = someTypesAndNumElements
    
      
    
    someUIDTypesAndNumElements = [ ]    
    aUIDTotalNumElements = 0
    
    someUIDElementsByType = aCataloggingReport.get( 'uid_elements_by_type', {})
    if not ( someUIDElementsByType == None):   
        someUIDMetaTypes = someUIDElementsByType.keys()
        someUIDMetaTypes = sorted( someUIDMetaTypes)
        
        for aMetaType in someUIDMetaTypes:
            aUIDNumElementsOfType = someUIDElementsByType.get( aMetaType, 0)
            someUIDTypesAndNumElements.append( [ aMetaType, aUIDNumElementsOfType, ])
            aUIDTotalNumElements += aUIDNumElementsOfType
            

    someFailedUIDTypesAndNumElements = [ ]    
    aFailedUIDTotalNumElements = 0
    
    someFailedUIDElementsByType = aCataloggingReport.get( 'failed_uid_elements_by_type', {})
    if not ( someFailedUIDElementsByType == None):   
        someUIDMetaTypes = someFailedUIDElementsByType.keys()
        someUIDMetaTypes = sorted( someUIDMetaTypes)
        
        for aMetaType in someUIDMetaTypes:
            aUIDNumElementsOfType = someFailedUIDElementsByType.get( aMetaType, 0)
            someFailedUIDTypesAndNumElements.append( [ aMetaType, aUIDNumElementsOfType, ])
            aFailedUIDTotalNumElements += aUIDNumElementsOfType
            
        
    aCataloggingReport.update( {
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
    
    return aCataloggingReport

    
    


def _TRACatalogging_recursive( 
    theInitialElement        =None, 
    theCataloggingReport     =None,
    theUIDCatalog            =None,
    theCataloggingAction     ='',
    theTransactionCounterHolder=None,):
    """Recursively add or remove from the Catalogs theInitialElement and recursive content elements except the contents of the specified types, recording results in theCataloggingReport.
    
    """
    
    if theInitialElement == None:
        return None

    if theCataloggingReport == None:
        return None

    if ( not theCataloggingAction) or not ( theCataloggingAction in cTRACataloggingActions):
        return None

    
    aMetaType = ''
    try:
        aMetaType = theInitialElement.meta_type
    except:
        None
    if not aMetaType:
        return None
    
    if not ( aMetaType in _cTodosNombresTiposEnPortalCatalog):
        return None
    
        
    if not( aMetaType in _cTodosNombresTiposEnPortalCatalog_ChildrenExcluidos):
        
        someContentElements = theInitialElement.objectValues()
        if someContentElements:

            for aContentElement in someContentElements:

                _TRACatalogging_recursive(
                    theInitialElement        =aContentElement, 
                    theCataloggingReport     =theCataloggingReport,
                    theUIDCatalog            =theUIDCatalog,
                    theCataloggingAction     =theCataloggingAction,
                    theTransactionCounterHolder=theTransactionCounterHolder,
                )            

                
                
                
    
    aIsCatalogged    = False
    aIsUIDCatalogged = False
    
    
    
    try:
        if theCataloggingAction == cTRACataloggingAction_DoCatalog:

            theInitialElement.reindexObject()
            aIsCatalogged = True
            
            
        elif theCataloggingAction == cTRACataloggingAction_UnCatalog:

            theInitialElement.unindexObject()            
            aIsCatalogged = True
    except:
        None

        

        
        
    if aIsCatalogged:
        if aMetaType:
            someElementsByType = theCataloggingReport.get( 'elements_by_type', {})
            if not ( someElementsByType == None):
                someElementsByType[ aMetaType] = someElementsByType.get( aMetaType, 0) + 1
        
                
    else:
        if aMetaType:
            someFailedElementsByType = theCataloggingReport.get( 'failed_elements_by_type', {})
            if not ( someFailedElementsByType == None):
                someFailedElementsByType[ aMetaType] = someFailedElementsByType.get( aMetaType, 0) + 1
        
        
                
    if not ( theUIDCatalog == None):
        if aMetaType:
            if not ( aMetaType in _cTRATodosNombresTiposNOEnUIDCatalog):

                
                try:
                    aInitialElementURL = theInitialElement._getURL()
                    if aInitialElementURL:

                        if theCataloggingAction == cTRACataloggingAction_DoCatalog: 
                            
                            theUIDCatalog.catalog_object( theInitialElement, aInitialElementURL)
                            aIsUIDCatalogged = True

                        elif  theCataloggingAction == cTRACataloggingAction_UnCatalog:
                            
                            theUIDCatalog.uncatalog_object( aInitialElementURL)
                            aIsUIDCatalogged = True
                        
                except:
                    None
                
                    
                    
                if aIsUIDCatalogged:
                    if aMetaType:
                        someElementsByType = theCataloggingReport.get( 'uid_elements_by_type', {})
                        if not ( someElementsByType == None):
                            someElementsByType[ aMetaType] = someElementsByType.get( aMetaType, 0) + 1
                else:
                    if aMetaType:
                        someFailedElementsByType = theCataloggingReport.get( 'failed_uid_elements_by_type', {})
                        if not ( someFailedElementsByType == None):
                            someFailedElementsByType[ aMetaType] = someFailedElementsByType.get( aMetaType, 0) + 1
            
    
                            
                            
    if theTransactionCounterHolder and ( aIsCatalogged or aIsUIDCatalogged):
        
        if aIsCatalogged:
            theTransactionCounterHolder[ 0] += 1
            
        if aIsUIDCatalogged:
            theTransactionCounterHolder[ 0] += 1

        if theTransactionCounterHolder[ 0] >= cTRAMaxElementsPerTransaction:
            transaction.commit()
            theTransactionCounterHolder[ 0] = 0
            
            
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


