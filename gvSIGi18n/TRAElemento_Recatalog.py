# -*- coding: utf-8 -*-
#
# File: TRAElemento_Recatalog.py
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
# Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana (Spain) <gvSIGi18n@gvSIG.org>  
# Model Driven Development sl  Valencia (Spain) <http://www.ModelDD.org> 
# Antonio Carrasco Valero                       <carrasco@ModelDD.org>
#
#
__author__ = """Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana <gvSIGi18n@gvSIG.org>, 
Model Driven Development sl <gvSIGi18n@ModelDD.org>, 
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'


import sys
import traceback
import logging
import transaction

import cgi





from DateTime                   import DateTime

from AccessControl              import ClassSecurityInfo

from Products.CMFCore           import permissions

from Products.CMFCore.utils     import getToolByName




from TRAElemento_Constants                 import *
from TRAElemento_Constants_Activity        import *
from TRAElemento_Constants_Configurations  import *
from TRAElemento_Constants_Dates           import *
from TRAElemento_Constants_Encoding        import *
from TRAElemento_Constants_Import          import *
from TRAElemento_Constants_Languages       import *
from TRAElemento_Constants_Logging         import *
from TRAElemento_Constants_Modules         import *
from TRAElemento_Constants_Profiling       import *
from TRAElemento_Constants_Progress        import *
from TRAElemento_Constants_String          import *
from TRAElemento_Constants_StringRequests  import *
from TRAElemento_Constants_Translate       import *
from TRAElemento_Constants_Translation     import *
from TRAElemento_Constants_TypeNames       import *
from TRAElemento_Constants_Views           import *
from TRAElemento_Constants_Vocabularies    import *
from TRAUtils                              import *

from TRAElemento_Permission_Definitions import cBoundObject
from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_ReCatalogTRAElemento


    
    
    
            
# ########################################################################################################
    
class TRAElemento_Recatalog:
    """CLASS: role class in support of responsibility of performing an inventory for all application elements.
        
    """
    
    security = ClassSecurityInfo()

         
        

    security.declareProtected( permissions.ManagePortal, 'fCreateProgressHandlerFor_Recatalog')
    def fCreateProgressHandlerFor_Recatalog( self, 
        theAdditionalParams      =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Request creation of an Recatalog long-lived process control handler, to be executed later.
        
        """


        
        
        def fRecatalogInitialize_lambda( theContextualElement, theProcessControlManager, theAdditionalParmsHere):  
        
            if theContextualElement == None:
                return None
            
            if not theProcessControlManager:
                return None
            
            unCatalogoRaiz  = theContextualElement.getCatalogo()
            
            unPortalCatalog = theContextualElement.getPortalCatalogTool()
    
            unCatalogBusquedaCadenas       = unCatalogoRaiz.fCatalogBusquedaCadenas() 
            unCatalogFiltroCadenas         = unCatalogoRaiz.fCatalogFiltroCadenas() 
            unCatalogTextoCadenas          = unCatalogoRaiz.fCatalogTextoCadenas() 
        
            todosIdiomas = [ ]
            unasColeccionesIdiomas = unCatalogoRaiz.fObtenerTodasColeccionesIdiomas()
            if unasColeccionesIdiomas:
                for unaColeccionIdiomas in unasColeccionesIdiomas:
                    unosIdiomas = unaColeccionIdiomas.fObtenerTodosIdiomas()
                    if unosIdiomas:
                        todosIdiomas.extend( unosIdiomas)
                    
            unosCatalogsBusquedaTraduccionesPorIdioma = { }
            unosCatalogsFiltroTraduccionesPorIdioma   = { }
            unosCatalogsTextoTraduccionesPorIdioma    = { }
            for unIdioma in todosIdiomas:
                if not( unIdioma == None):
                    unCodigoIdioma = unIdioma.getCodigoIdiomaEnGvSIG()
                    if unCodigoIdioma:
                        unosCatalogsBusquedaTraduccionesPorIdioma[ unCodigoIdioma] = unCatalogoRaiz.fCatalogBusquedaTraduccionesParaIdioma( unIdioma)
                        unosCatalogsFiltroTraduccionesPorIdioma[   unCodigoIdioma] = unCatalogoRaiz.fCatalogFiltroTraduccionesParaIdioma(   unIdioma)
                        unosCatalogsTextoTraduccionesPorIdioma[    unCodigoIdioma] = unCatalogoRaiz.fCatalogTextoTraduccionesParaIdioma(    unIdioma)
                
            unosInitializedObjects = {
                'catalogs': {
                    'PortalCatalog':        unPortalCatalog,
                    'BusquedaCadenas':      unCatalogBusquedaCadenas,
                    'FiltroCadenas':        unCatalogFiltroCadenas,
                    'TextoCadenas':         unCatalogTextoCadenas,
                    'BusquedaTraducciones': unosCatalogsBusquedaTraduccionesPorIdioma,
                    'FiltroTraducciones':   unosCatalogsFiltroTraduccionesPorIdioma,
                    'TextoTraducciones':    unosCatalogsTextoTraduccionesPorIdioma,
                },
            }
            
            theProcessControlManager.pAddInitializedObjects( unosInitializedObjects)
            
            return None        
                    


        
        
        def fRecatalogFinalize_lambda( 
            theElement               =None, 
            theProcessControlManager =None, 
            theAdditionalParmsHere   =None, 
            theTerminationRequested  =False, 
            theThereWasException     =False):
            
            if theElement == None:
                return None
            
            if not theProcessControlManager:
                return None       
            
            if not ( theProcessControlManager.vStarted and theProcessControlManager.vCompleted):
                return None
            
            
            anInitialElement = theProcessControlManager.vInitialElement
            if anInitialElement == None:
                return None
            
            anInitialElementMetaType  = ''
            try:
                anInitialElementMetaType = anInitialElement.meta_type 
            except:
                None
        
            if not( anInitialElementMetaType == cNombreTipoTRACatalogo):
                return None
            
            if anInitialElement.getDebeRecatalogar():
                anInitialElement.setDebeRecatalogar( False)
                
            return None
                
            
        
            
        def fRecatalogElement_lambda( theElement, theProcessControlManager, theAdditionalParmsHere):  
            
            if theElement == None:
                return None
            
            if not theProcessControlManager:
                return None
            
            someCatalogs = theProcessControlManager.fGetInitializedObjects( 'catalogs')

            aMetaType = 'UnknownType'
            try:
                aMetaType = theElement.meta_type
            except:
                aMetaType = theElement.__class__.__name
            if not aMetaType:
                aMetaType = 'UnknownType'
                
            
            if aMetaType == cNombreTipoTRATraduccion:
                unCodigoIdioma = theElement.getCodigoIdiomaEnGvSIG()
                theElement.pAddToCatalogs( someCatalogs.get( 'BusquedaTraducciones', {}).get( unCodigoIdioma),  someCatalogs.get( 'FiltroTraducciones', {}).get( unCodigoIdioma),  someCatalogs.get( 'TextoTraducciones', {}).get( unCodigoIdioma), None)
                
            elif aMetaType == cNombreTipoTRACadena:
                theElement.pAddToCatalogs( someCatalogs.get( 'BusquedaCadenas', None),  someCatalogs.get( 'FiltroCadenas', None),  someCatalogs.get( 'TextoCadenas', None),)
                
            else:
                theElement.reindexObject()
            
            anElementsByType = { aMetaType: 1,}
            
            theProcessControlManager.pProcessStep( theElement, anElementsByType, anElementsByType)
                
            return None        

        
        
            
        def fRecatalogElementPlone_lambda( theElement, theProcessControlManager, theAdditionalParmsHere):  
            
            if theElement == None:
                return None
            
            if not theProcessControlManager:
                return None
            

            aMetaType = 'UnknownType'
            try:
                aMetaType = theElement.meta_type
            except:
                aMetaType = theElement.__class__.__name
            if not aMetaType:
                aMetaType = 'UnknownType'
                
            if not( aMetaType in cTRAPloneTypeNames):
                return None
            
            theElement.reindexObject()
            
            anElementsByType = { aMetaType: 1,}
            
            theProcessControlManager.pProcessStep( theElement, anElementsByType, anElementsByType)
                
            return None        

        
        
        
        
        unExecutionRecord = self.fStartExecution( 'method',  'fCreateProgressHandlerFor_Recatalog', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }, ) 
        
        aThereWasException = False
        
        try:
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
            
            aResult = self.fNewVoidCreateProgressHandlerResult()

            try:
                
                
                unCatalogoRaiz = self.getCatalogo()           
                if unCatalogoRaiz == None:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_internal_Missing_RootCatalog', "Internal error: missing root translations catalog-."),
                    })
                    return aResult
                
                unaColeccionProgresos = unCatalogoRaiz.fObtenerColeccionProgresos()
                if unaColeccionProgresos == None:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_internal_Missing_progresses_collection', "Internal error: missing progresses collection-."),
                    })
                    return aResult
                            
                
                aRecatalogResult = self.fNewVoidProgressResult()
                
                
                aProgressElement = None
                aProgressHandler = None
            
                aMetaType = 'UnknownType'
                try:
                    aMetaType = self.meta_type
                except:
                    aMetaType = self.__class__.__name
                if not aMetaType:
                    aMetaType = 'UnknownType'
                
                aStartDateTimeNowTextual = self.fDateTimeNowTextual()
                aRecatalogResult[ 'process_type']           = cTRAProgress_ProcessType_ReCatalog
                aRecatalogResult[ 'start_date_time_string'] = aStartDateTimeNowTextual
                aRecatalogResult[ 'date_time_now_string']   = aStartDateTimeNowTextual
                aRecatalogResult[ 'element_type']           = aMetaType
                aRecatalogResult[ 'element_title']          = self.Title()
                aRecatalogResult[ 'element_path' ]          = self.fPhysicalPathString()
                aRecatalogResult[ 'element_UID' ]           = self.UID()
                aRecatalogResult[ 'last_element_type']      = ''
                aRecatalogResult[ 'last_element_title']     = ''
                aRecatalogResult[ 'last_element_path']      = ''
                aRecatalogResult[ 'last_element_UID']       = ''
                
                aMemberId = self.fGetMemberId()
                aRecatalogResult[ 'member_id'] = aMemberId
                
                aRecatalogResult[ 'TRACatalogo_title']      = unCatalogoRaiz.Title()
                aRecatalogResult[ 'TRACatalogo_path' ]      = unCatalogoRaiz.fPathDelRaiz()
                aRecatalogResult[ 'TRACatalogo_UID' ]       = unCatalogoRaiz.UID()
                
                    
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_ReCatalogTRAElemento, 
                    theElementsBindings     = { cBoundObject: self,},
                    theRulesToCollect       = [ ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord
                )
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_no_permission_ToRecatalog', "You do not have permission to Re-Catalog-."),
                    })
                    return aResult
                
                

                aProgressHandlerCreationResult = unaColeccionProgresos.fCreateNewProgressAndHandlerForElement(  
                    theInitialElement       =self, 
                    theProcessType          =cTRAProgress_ProcessType_ReCatalog, 
                    theTimestamp            =aStartDateTimeNowTextual,
                    theResult               =aRecatalogResult, 
                    theElementLambda        =fRecatalogElement_lambda,
                    theElementPloneLambda   =fRecatalogElementPlone_lambda,
                    theInitializeLambda     =fRecatalogInitialize_lambda,
                    theFinalizeLambda       =fRecatalogFinalize_lambda,
                    theLockCatalog          =True,
                    thePermissionsCache     =unPermissionsCache, 
                    theRolesCache           =unRolesCache, 
                    theParentExecutionRecord=unExecutionRecord,)
                if ( not aProgressHandlerCreationResult) or not aProgressHandlerCreationResult.get( 'success', False):
                    aResult.update( {
                        'success':    False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_TRAProgress_not_created_for_TRAImportacion_msgid', "Error creating Progress element for Import element-."),
                    })
                    return aResult     
                
                
                aProgressElement = aProgressHandlerCreationResult.get( 'progress_element', None)
                if ( aProgressElement == None):
                    aResult = { 
                        'success':   False, 
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorProgressElementNotKnownByImportProcessElement', "Progress element is not known by import process element-"),
                    }
                    return aResult
                
                aProgressHandler = aProgressHandlerCreationResult.get( 'progress_handler', None)
                if not aProgressHandler:
                    aResult = { 
                        'success':   False, 
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorImportProgressHandlerNotFound', "Import Progress Handler has not been found-"),
                    }
                    return aResult

                aProgressHandlerKey = aProgressHandlerCreationResult.get( 'progress_handler_key', None)
                if not aProgressHandlerKey:
                    aResult = { 
                        'success':   False, 
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorImport_NoProgressHandlerKey', "Import has no Progress Handler Key-"),
                    }
                    return aResult

                
                aResult.update( {
                    'success':               True,
                    'condition':             '',
                    'progress_element':      aProgressElement,
                    'progress_handler':      aProgressHandler,
                    'progress_handler_key':  aProgressHandlerKey,
                })
                
                return aResult
            
            
            
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                aThereWasException = True
                unInformeExcepcion = ''
                try:
                    unInformeExcepcion += 'Exception during fCreateProgressHandlerFor_Recatalog of element %s %s at %s\n'  % (  self.meta_type(), self.Title(), self.fPhysicalPathString())
                except:
                    None
                try:
                    unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                except:
                    None
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                try:
                    unInformeExcepcion += unaExceptionFormattedTraceback   
                except:
                    None
                
                unInformeExcepcionWOResult = unInformeExcepcion[:]
                
                aRecatalogResult[ 'success'] = False
                aRecatalogResult[ 'exception_date_time_string'] = self.fDateTimeNowTextual()
                aRecatalogResultDump = ''
                try:
                    aRecatalogResultDump = self.fProgressResult_dump( aRecatalogResult)
                except:
                    None
                if aRecatalogResultDump:
                    unInformeExcepcion += aRecatalogResultDump
                
                aRecatalogResult[ 'exception_report'] = unInformeExcepcionWOResult

                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
    
                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                aResult = { 
                    'success':    False, 
                    'condition':  '%s\n%s' % (   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_Exception_msgid', "Exception.-"), unInformeExcepcion, ),
                }
                return aResult
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
           
        
       
            
            
            
        
       
                        
            
    
    