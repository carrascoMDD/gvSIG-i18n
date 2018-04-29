# -*- coding: utf-8 -*-
#
# File: TRAModulo_Operaciones.py
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
#

__author__ = """Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana <gvSIGi18n@gvSIG.org>, 
Model Driven Development sl <gvSIGi18n@ModelDD.org>, 
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'



import sys
import traceback

import logging

import transaction

from AccessControl import ClassSecurityInfo

##code-section module-header #fill in your manual code here

from Products.CMFCore       import permissions


##/code-section module-header


##code-section after-local-schema #fill in your manual code here

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

from TRAArquetipo  import TRAArquetipo

from TRAElemento_Permission_Definitions import cBoundObject
from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_RenameTRAModulo



##/code-section after-local-schema


##code-section after-schema #fill in your manual code here


##/code-section after-schema

class TRAModulo_Operaciones:
    """
    """

    security = ClassSecurityInfo()    


    ##code-section class-header #fill in your manual code here
    
    
    
    
    
    
    
    
    


    security.declareProtected( permissions.ManagePortal, 'fCreateProgressHandlerFor_RenameModule')
    def fCreateProgressHandlerFor_RenameModule( self, 
        theAdditionalParams      =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Request creation of a RenameModule long-lived process control handler, to be executed later.
        
        """

        
        
        def fRenameModuleInitialize_lambda( theContextualElement, theProcessControlManager, theAdditionalParmsHere):  
        
            if theContextualElement == None:
                return None
            
            if not theProcessControlManager:
                return None
            
            someInputParameters = theProcessControlManager.vInputParameters
            if not someInputParameters:
                return None
            
            aModuleUID = someInputParameters.get( 'module_UID', '')
            if not aModuleUID:
                return None
            unModulo = theContextualElement.fElementoPorUID( aModuleUID)
            if unModulo == None:
                return None
            
            
            
            aNewModuleName =  someInputParameters.get( 'new_module_name', '')
            if not aNewModuleName:
                return None
            
            aCurrentModuleName = unModulo.Title()
            if aNewModuleName == aCurrentModuleName:
                return None
            
            
            unosInitializedObjects = {
                'module':              unModulo,
                'current_module_name': aCurrentModuleName,
                'new_module_name':     aNewModuleName,
            }
                        
            theProcessControlManager.pAddInitializedObjects( unosInitializedObjects)
            
            return None        
                    
         
        
        
        
        
            
        def fRenameModuleLoop_lambda( theInitialElement, theProcessControlManager, theAdditionalParmsHere):  
            
            if theInitialElement == None:
                return None
            
            if not theProcessControlManager:
                return None
               
            if not theProcessControlManager.vInitializedObjects:
                return None

            
            unModulo = theProcessControlManager.vInitializedObjects.get( 'module', None)
            if unModulo == None:
                return None
            
            unNombreModuloActual = theProcessControlManager.vInitializedObjects.get( 'current_module_name', '')
            if not unNombreModuloActual:
                return None

            unNuevoNombreModulo = theProcessControlManager.vInitializedObjects.get( 'new_module_name', '')
            if not unNuevoNombreModulo:
                return None
            
            
            if unNuevoNombreModulo == unNombreModuloActual:
                return None
            
            
            if theProcessControlManager.vCatalogoRaiz == None:
                return None            
            
            unasColeccionesCadenas = theProcessControlManager.vCatalogoRaiz.fObtenerTodasColeccionesCadenas()
            for unaColeccionCadenas in unasColeccionesCadenas:
                
                unasCadenas = unaColeccionCadenas.fObtenerTodasCadenas()
                for unaCadena in unasCadenas:
                    
                    theProcessControlManager.vElementLambda( unaCadena, theProcessControlManager, theAdditionalParmsHere)
            
                    
                    
            transaction.commit()
            
            
            unModulo.setTitle( unNuevoNombreModulo)

            aNumElementsOfType = { 
                cNombreTipoTRAModulo: 1,
            }
            theProcessControlManager.pProcessStep( unModulo, aNumElementsOfType, aNumElementsOfType)
                    

            theProcessControlManager.vCatalogoRaiz.pInvalidateSimbolosCadenasOrdenados()
            
                        
                        
            return None        
                    
            
            
        
        
            
        def fRenameModuleElement_lambda( theElement, theProcessControlManager, theAdditionalParmsHere):  
            
            if theElement == None:
                return None
            
            if not theProcessControlManager:
                return None
            
            if not ( theElement.meta_type == cNombreTipoTRACadena):
                return None
            
            unNombreModuloActual = theProcessControlManager.vInitializedObjects.get( 'current_module_name', '')
            if not unNombreModuloActual:
                return None

            unNuevoNombreModulo = theProcessControlManager.vInitializedObjects.get( 'new_module_name', None)
            if not unNuevoNombreModulo:
                return None
            
            
            unNumCadenasChanged = 0
            unNumTranslationsReadAndChanged = 0
            if theElement.fRenameModulo( unNombreModuloActual, unNuevoNombreModulo):
                unNumCadenasChanged = 1                
                unNumTranslationsReadAndChanged = theElement.fPropagarCambioNombresModulosATraducciones()
            
                            
            aNumElementsOfTypeRead = { 
                cNombreTipoTRACadena: 1,
                cNombreTipoTRATraduccion: unNumTranslationsReadAndChanged,
            }
            aNumElementsOfTypeChanged = { 
                cNombreTipoTRACadena: unNumCadenasChanged,
                cNombreTipoTRATraduccion: unNumTranslationsReadAndChanged,
            }
            theProcessControlManager.pProcessStep( theElement, aNumElementsOfTypeRead, aNumElementsOfTypeChanged)
                
            
            return None        

        
        
        
        
        
        unExecutionRecord = self.fStartExecution( 'method',  'fCreateProgressHandlerFor_RenameModule', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }, ) 
        
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
                    
                aRenameModuleResult = self.fNewVoidProgressResult()
                
                
                aProgressElement = None
                aProgressHandler = None
                
                aNewModuleName = theAdditionalParams.get( 'new_module_name', '')
                if not aNewModuleName:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_MissingParameter_NewModuleName', "Missing Parameter: New Module Name-."),
                    })
                    return aResult
                    
                    
                aCurrentModuleName = self.Title()
                if aNewModuleName == aCurrentModuleName:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_RenameModule_SameModuleName', "New Module Name is the same as the current module name-."),
                    })
                    return aResult
                    
                
               
                aMetaType = 'UnknownType'
                try:
                    aMetaType = self.meta_type
                except:
                    aMetaType = self.__class__.__name
                if not aMetaType:
                    aMetaType = 'UnknownType'
                
                aStartDateTimeNowTextual = self.fDateTimeNowTextual()
                aRenameModuleResult[ 'process_type']           = cTRAProgress_ProcessType_RenameModule
                aRenameModuleResult[ 'start_date_time_string'] = aStartDateTimeNowTextual
                aRenameModuleResult[ 'date_time_now_string']   = aStartDateTimeNowTextual
                aRenameModuleResult[ 'element_type']           = aMetaType
                aRenameModuleResult[ 'element_title']          = self.Title()
                aRenameModuleResult[ 'element_path' ]          = self.fPhysicalPathString()
                aRenameModuleResult[ 'element_UID' ]           = self.UID()
                aRenameModuleResult[ 'last_element_type']      = ''
                aRenameModuleResult[ 'last_element_title']     = ''
                aRenameModuleResult[ 'last_element_path']      = ''
                aRenameModuleResult[ 'last_element_UID']       = ''
                
                aMemberId = self.fGetMemberId()
                aRenameModuleResult[ 'member_id'] = aMemberId
                
                aRenameModuleResult[ 'TRACatalogo_title']      = unCatalogoRaiz.Title()
                aRenameModuleResult[ 'TRACatalogo_path' ]      = unCatalogoRaiz.fPathDelRaiz()
                aRenameModuleResult[ 'TRACatalogo_UID' ]       = unCatalogoRaiz.UID()
                
                    
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_RenameTRAModulo, 
                    theElementsBindings     = { cBoundObject: self,},
                    theRulesToCollect       = [ ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord
                )
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_no_permission_ToRenameModule', "You do not have permission to Rename Module-."),
                    })
                    return aResult
                
                 
  
                
                someInputParameters = { 
                    'module_UID':              self.UID(),
                    'new_module_name':         aNewModuleName,
                }

                aProgressHandlerCreationResult = unaColeccionProgresos.fCreateNewProgressAndHandlerForElement(  
                    theInitialElement       =self, 
                    theProcessType          =cTRAProgress_ProcessType_RenameModule, 
                    theInputParameters      =someInputParameters,
                    theTimestamp            =aStartDateTimeNowTextual,
                    theResult               =aRenameModuleResult, 
                    theInitializeLambda     =fRenameModuleInitialize_lambda,
                    theElementLambda        =fRenameModuleElement_lambda,
                    theLoopLambda           =fRenameModuleLoop_lambda,
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
                
                return aResult
            
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                aThereWasException = True
                unInformeExcepcion = ''
                try:
                    unInformeExcepcion += 'Exception during fCreateProgressHandlerFor_RenameModule of element %s %s at %s\n'  % (  self.meta_type(), self.Title(), self.fPhysicalPathString())
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
                
                aRenameModuleResult[ 'success'] = False
                aRenameModuleResult[ 'exception_date_time_string'] = self.fDateTimeNowTextual()
                aRenameModuleResultDump = ''
                try:
                    aRenameModuleResultDump = self.fProgressResult_dump( aRenameModuleResult)
                except:
                    None
                if aRenameModuleResultDump:
                    unInformeExcepcion += aRenameModuleResultDump
                
                aRenameModuleResult[ 'exception_report'] = unInformeExcepcionWOResult

                
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
           
                
    
    
    
    
    
    
    
    
    
    
    
    
    

    

    security.declarePrivate( 'pAllSubElements_into')    
    def pAllSubElements_into( self, theCollection, theAdditionalParams=None):
        if theCollection == None:
            return self
        theCollection.append( self)
        
         
        return self
        
    

    security.declarePrivate( 'pForAllElementsDo_recursive')    
    def pForAllElementsDo_recursive( self, theLambda):
        if not theLambda:
            return self
        
        theLambda( self)        
    
        return self

                       
    
    security.declarePublic( 'fExtraLinks')    
    def fExtraLinks( self):
        
        unosExtraLinks = TRAArquetipo.fExtraLinks( self)
        if not unosExtraLinks:
            unosExtraLinks = [ ]
        
        return unosExtraLinks
     
        
    
    
    
    
    
    ##/code-section class-header

    # Methods
# end of class TRAModulo_Operaciones

##code-section module-footer #fill in your manual code here
##/code-section module-footer



