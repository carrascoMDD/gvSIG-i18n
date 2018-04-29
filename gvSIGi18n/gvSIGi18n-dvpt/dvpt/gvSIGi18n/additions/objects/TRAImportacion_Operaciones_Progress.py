# -*- coding: utf-8 -*-
#
# File: TRAImportacion_Operaciones_Progress.py
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


from AccessControl import ClassSecurityInfo



import sys
import traceback


import logging


from Products.CMFCore       import permissions




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

from TRAImportarExportar_Constants import *

from TRAElemento_Permission_Definitions import cBoundObject
from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_ImportTRAImportacion, cUseCase_ImportTRAImportacion_ToCreateCadenas


from TRAProcessErrorException import TRAProcessErrorException




class TRAImportacion_Operaciones_Progress:
    """
    """
    security = ClassSecurityInfo()
     


    
    
    
    
    security.declarePrivate( 'fNewVoidProgressResult_Import')
    def fNewVoidProgressResult_Import( self, ):
        unResult = self.fNewVoidProgressResult()
        unResult.update( {
            'import_contents_report':    {},
        })
        return unResult
                
            
    
   
        

    security.declareProtected( permissions.ManagePortal, 'fCreateProgressHandlerFor_Import')
    def fCreateProgressHandlerFor_Import( self, 
        theAdditionalParams      =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Request creation of an Import long-lived process control handler, to be executed later.
        
        """

   
        
        def fRecatalogInitialize_lambda( theContextualElement, theProcessControlManager, theAdditionalParmsHere):  
        
            if theContextualElement == None:
                return None
            
            if not theProcessControlManager:
                return None
            
            unosParametrosEntrada = theProcessControlManager.vInputParameters
            if not unosParametrosEntrada:
                return None
            
            unImportElementId = unosParametrosEntrada.get( 'import_element_id', '')
            if not unImportElementId:
                return None
            
            unCatalogoRaiz = theContextualElement.getCatalogo()
            if unCatalogoRaiz == None:
                return None
            
            unaColeccionImportaciones = unCatalogoRaiz.fObtenerColeccionImportaciones()
            if unaColeccionImportaciones == None:
                return None
             
            unImportElement = unaColeccionImportaciones.getElementoPorID( unImportElementId)
            if unImportElement == None:
                return None
             
            unosInitializedObjects = {
                'import_element': unImportElement,
            }
            
            theProcessControlManager.pAddInitializedObjects( unosInitializedObjects)
            
            return None        
                    
        
        
         
            
        def fImportLoop_lambda( theElement, theProcessControlManager, theAdditionalParmsHere):        
                    
            anImportElement = theProcessControlManager.fGetInitializedObjects( 'import_element')
            if anImportElement == None:
                return None

            
            
            
            # ###########################################
            """When the Import process is to create requested new strings, retrieve the UIDs of String Creation Requests for each requested symbol, such that the import process can mark the String Requests as already created.
            
            """
            aIsToCreateCadenas = False
            someSolicitudesCadenasUIDsPorSimbolo = {}
            
            if theProcessControlManager.vInputParameters:
                aIsToCreateCadenas = theProcessControlManager.vInputParameters.get( 'is_to_create_cadenas', False)
                if aIsToCreateCadenas:
                    someSolicitudesCadenasUIDsPorSimbolo = theProcessControlManager.vInputParameters.get( 'string_creation_request_UIDs_by_string_symbol', {})
                    
                    
                    
                    
                    
            anImportElement.fImportarContenidosIntercambio(
                theProcessControlManager =theProcessControlManager,
                theIsToCreateCadenas     =aIsToCreateCadenas,
                theSolicitudesCadenasUIDsPorSimbolo =someSolicitudesCadenasUIDsPorSimbolo,
                thePermissionsCache      =None, 
                theRolesCache            =None, 
                theParentExecutionRecord =None
            )
            
            
            return None        


        
        
        
        unExecutionRecord = self.fStartExecution( 'method',  'fCreateProgressHandlerFor_Import', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }, ) 
        
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
                
                aImportResult = self.fNewVoidProgressResult_Import()
                
                unInformeImportarContenidos = self.fNewVoidInformeImportarContenidos()
                aImportResult[ 'import_contents_report'] = unInformeImportarContenidos
                
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
                aImportResult[ 'process_type']           = cTRAProgress_ProcessType_Import
                aImportResult[ 'start_date_time_string'] = aStartDateTimeNowTextual
                aImportResult[ 'date_time_now_string']   = aStartDateTimeNowTextual
                aImportResult[ 'element_type']           = aMetaType
                aImportResult[ 'element_title']          = self.Title()
                aImportResult[ 'element_path' ]          = self.fPhysicalPathString()
                aImportResult[ 'element_UID' ]           = self.UID()
                aImportResult[ 'last_element_type']      = ''
                aImportResult[ 'last_element_title']     = ''
                aImportResult[ 'last_element_path']      = ''
                aImportResult[ 'last_element_UID']       = ''
                
                aMemberId = self.fGetMemberId()
                aImportResult[ 'member_id'] = aMemberId
                
                
                aImportResult[ 'TRACatalogo_title']      = unCatalogoRaiz.Title()
                aImportResult[ 'TRACatalogo_path' ]      = unCatalogoRaiz.fPathDelRaiz()
                aImportResult[ 'TRACatalogo_UID' ]       = unCatalogoRaiz.UID()
                
                aIsToCreateCadenas = False
                someSolicitudesCadenasUIDsPorSimbolo = {}
                
                if theAdditionalParams:
                    aIsToCreateCadenas = theAdditionalParams.get( 'theIsToCreateCadenas', False)
                    if aIsToCreateCadenas:
                        someSolicitudesCadenasUIDsPorSimbolo = theAdditionalParams.get( 'theSolicitudesCadenasUIDsPorSimbolo', {})
                    
                        
                        
                        
                aUseCaseNameToAssess = cUseCase_ImportTRAImportacion
                if aIsToCreateCadenas:
                    aUseCaseNameToAssess  = cUseCase_ImportTRAImportacion_ToCreateCadenas
                    
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = aUseCaseNameToAssess, 
                    theElementsBindings     = { cBoundObject: self,},
                    theRulesToCollect       = [ ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord
                )
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_no_permission_ToImport', "You do not have permission to Import-."),
                    })
                    return aResult
                

                someInputParameters = { 
                    'is_to_create_cadenas':  aIsToCreateCadenas,
                    'import_element_id':     self.getId(),
                    'string_creation_request_UIDs_by_string_symbol': someSolicitudesCadenasUIDsPorSimbolo,
                }


                                
                
                aProgressHandlerCreationResult = unaColeccionProgresos.fCreateNewProgressAndHandlerForElement(  
                    theInitialElement       =self, 
                    theProcessType          =cTRAProgress_ProcessType_Import, 
                    theInputParameters      =someInputParameters,
                    theTimestamp            =aStartDateTimeNowTextual,
                    theResult               =aImportResult, 
                    theInitializeLambda     =fRecatalogInitialize_lambda,
                    theLoopLambda           =fImportLoop_lambda,
                    theElementLambda        =None,
                    theFinalizeLambda       =None,
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

            
                                
                self.setIdentificadorElementoProgreso( aProgressElement.getId())
                
                unCatalogoRaiz.pFlushCachedTemplates_All()
                
                
                aProgressElement.setTipoElementoProceso( self.meta_type)
                aProgressElement.setIdentificadorElementoProceso( self.getId())
                
                aProgressElement.pFlushCachedTemplates_All()

                

                
                return aResult
            
                        
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                aThereWasException = True
                unInformeExcepcion = ''
                try:
                    unInformeExcepcion += 'Exception during fCreateProgressHandlerFor_Import of element %s %s at %s\n'  % (  self.meta_type(), self.Title(), self.fPhysicalPathString())
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
                
                aImportResult[ 'success'] = False
                aImportResult[ 'exception_date_time_string'] = self.fDateTimeNowTextual()
                aImportResultDump = 'No Import Result Dump: empty or error during conversion of result as a string'
                try:
                    aImportResultDump = self.fProgressResult_dump( aImportResult)
                except:
                    None
                if aImportResultDump:
                    unInformeExcepcion += aImportResultDump
                
                aImportResult[ 'exception_report'] = unInformeExcepcionWOResult

                
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
           
        
       
            
            
                
    security.declarePrivate( 'fHasProgressElementAlreadyExecuted')
    def fHasProgressElementAlreadyExecuted( self):
        unElementoProgreso = self.fDeriveElementoProgreso()
        if unElementoProgreso == None:
            return False
        
        unHaComenzadoElementoProceso = unElementoProgreso.getHaComenzado()
        return unHaComenzadoElementoProceso
        
        

        
        
    security.declarePrivate( 'fHasNoProgressElementOrNotExecuted')
    def fHasNoProgressElementOrNotExecuted( self):
        unElementoProgreso = self.fDeriveElementoProgreso()
        if unElementoProgreso == None:
            return True
        
        unHaComenzadoElementoProceso = unElementoProgreso.getHaComenzado()
        return not unHaComenzadoElementoProceso
    
    


    
    
    security.declarePrivate( 'fDeriveElementoProgreso')
    def fDeriveElementoProgreso( self):
        
        unProgressElementId = self.getIdentificadorElementoProgreso()
        if not unProgressElementId:
            return None
        
        unCatalogo = self.getCatalogo()
        if ( unCatalogo == None):
            return None
        
        unaColeccionProgresos = unCatalogo.fObtenerColeccionProgresos()
        if ( unaColeccionProgresos == None):
            return None
        
        unElementoProgreso = unaColeccionProgresos.getElementoPorID( unProgressElementId)
        return unElementoProgreso
        
    
    
    
    
    