# -*- coding: utf-8 -*-
#
# File: TRAColeccionModulos_Operaciones.py
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



##code-section module-header #fill in your manual code here


import sys
import traceback


import logging

import transaction

from math import floor


from StringIO import StringIO


from Products.CMFCore.utils import getToolByName


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



from TRAImportarExportar_Constants                import *
from TRAImportarExportar_Constants_Encodings      import *
from TRAImportarExportar_Constants_GNUgettextPO   import *
from TRAImportarExportar_Constants_JavaProperties import *

from TRAElemento_Permission_Definitions import cBoundObject
from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_CreateTRAModulo, cUseCase_DeleteTRAModulo



class TRAColeccionModulos_Operaciones:
    """
    """
    security = ClassSecurityInfo()
     




    security.declarePrivate( 'pAllSubElements_into')    
    def pAllSubElements_into( self, theCollection, theAdditionalParams=None):
        if theCollection == None:
            return self
        theCollection.append( self)
        
        
        unosElementos = self.fObtenerTodosModulos()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pAllSubElements_into( theCollection,theAdditionalParams=theAdditionalParams)
        
        return self
        

    


    security.declarePrivate( 'pForAllElementsDo_recursive')    
    def pForAllElementsDo_recursive( self, theLambda=None, thePloneLambda=None,):
        if not theLambda:
            return self
        
        theLambda( self)

        unosElementos = self.fObtenerTodosModulos()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda, thePloneLambda)
                
        if thePloneLambda:
            self.pForAllElementsPloneDo( thePloneLambda)
        
        return self
        

          
    
    
    security.declareProtected( permissions.View, 'fObtenerTodosModulos')
    def fObtenerTodosModulos( self, ):
        """Retrieve all contained elements of type TRAModulo.
        
        """
        unosElementos = self.fObjectValues( cNombreTipoTRAModulo) 
        return unosElementos
         

    
    

    

    
    security.declarePrivate( 'fCrearModulo')    
    def fCrearModulo( self,
        theTimeProfilingResults =None, 
        theModelDDvlPloneTool_Mutators   =None, 
        theNewTypeName          ='', 
        theNewOneTitle          ='', 
        theNewOneDescription    ='', 
        theAdditionalParams     =None,
        thePermissionsCache     =None,
        theRolesCache           =None,
        theParentExecutionRecord=None):
        """Create a new instance of TRAModulo, immediately, without import process.
        
        """
    
        unExecutionRecord = self.fStartExecution( 'method',  'fCrearModulo', None, True, { 'log_what': 'details', 'log_when': True, })

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators import cModificationKind_CreateSubElement, cModificationKind_Create

        try:
            unasDescripcionesContenidosCreados = []
            try:
                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)
                
                unasRulesToBypass = []
                if theAdditionalParams:
                    unasRulesToBypass = theAdditionalParams.get( 'rules_to_bypass', [])
                    
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_CreateTRAModulo, 
                    theElementsBindings     = { cBoundObject: self,}, 
                    theRulesToCollect       = [ 'modules', ], 
                    theRulesToBypass        = unasRulesToBypass,
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord,
                )
              
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_no_permission_ToCreateModule_msgid', "User does not have permission to create modules (as an import process).-"), }
                    return anActionReport  
                            
                aModelDDvlPlone_tool = self.fModelDDvlPloneTool()
                             
                
                 
                aNewNombreModulo       = theNewOneTitle
                if not aNewNombreModulo:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Modulo_missingParameter_Nombre_warning_msgid', "The Module name is missing. The Module name is required to create a new Module.-"), }
                    return anActionReport  
                
                aNewNombreModulo = aNewNombreModulo.replace(',', ' ')
                somePartsNewNombreModulo = aNewNombreModulo.strip().split( cTRAModuleNameSeparator)
                if not somePartsNewNombreModulo:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Modulo_missingParameter_Nombre_warning_msgid', "The Module name is missing. The Module name is required to create a new Module.-"), }
                    return anActionReport  
                aNewNombreModulo = somePartsNewNombreModulo[ 0]
                if not aNewNombreModulo:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Modulo_missingParameter_Nombre_warning_msgid', "The Module name is missing. The Module name is required to create a new Module.-"), }
                    return anActionReport  

                
                
                unCatalogo = self.getCatalogo()
                
                if unCatalogo == None:
                    anActionReport = { 'effect': 'error', 'failure':  'InternalError: gvSIGi18n_errorCreating_Modulo_Missing_TRACatalogo_error_msgid', }
                    return anActionReport  
                
                
                unModuloPorNombre = unCatalogo.fGetModuloPorNombre( aNewNombreModulo)
                if not ( unModuloPorNombre == None):
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Modulo_ModuleNameAlreadyExists_warning_msgid', "A module with same name already exists in the translations catalog.-"), }
                    return anActionReport  

                
                
                
                
                

                unaIdModulo = unCatalogo.fModuloIdDesdeNombre( aNewNombreModulo)
                
                aNewModuloAttrsDict = { 
                    'title': aNewNombreModulo,
                }
                
                unaIdNuevoModulo = self.invokeFactory( cNombreTipoTRAModulo, unaIdModulo, **aNewModuloAttrsDict)
                if not unaIdNuevoModulo:
                    anActionReport = { 'effect': 'error', 'failure': self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Modulo_InvokeFactoryError_msgid', "Error in module factory in the translations catalog.-"), }
                    return anActionReport     
                         
                unNuevoModulo = self.getElementoPorID( unaIdNuevoModulo)
                if unNuevoModulo == None:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Modulo_CrearModuleError_msgid', "Failure creating module in the translations catalog.-"), }
                    return anActionReport  
                
                unNuevoModulo.manage_fixupOwnershipAfterAdd()
              
                unNuevoModulo.pSetPermissions()
               
                # ACV 20090914 Simpler security schema: no user groups for languages or modules, shall assign local roles to users directly on the language or module element
                if not unCatalogo.fSetLocalRolesEnModuloForCatalogUserGroups( unNuevoModulo):
                    return None
                
                unNuevoModulo.setPermiteLeer( True)
                unNuevoModulo.setPermiteModificar( True)
                                
                
                
                unosModulos = self.fObtenerTodosModulos()
                unosNombresModulo = [ unModulo.Title() for unModulo in unosModulos]
                unNumModulos = len( unosNombresModulo)
                      
                unIndexModuloAnterior = -1
                for unIndexModulo in range( unNumModulos):
                    unNombreModulo = unosNombresModulo[ unIndexModulo]
                    if unNombreModulo < aNewNombreModulo:
                        unIndexModuloAnterior = unIndexModulo    
                    else:
                        break
                    
                if unIndexModuloAnterior < 0:
                    self.moveObjectsToTop( [ unaIdNuevoModulo,])
                else:
                    if not ( unIndexModuloAnterior == ( unNumModulos - 1)):
                        if unIndexModuloAnterior < ( unNumModulos - 1):
                            unDelta = ( unIndexModuloAnterior + 2) - unNumModulos 
                            self.moveObjectsByDelta( [ unaIdNuevoModulo,], unDelta)
                    
                    
                    
                
                unResultadoNuevoModulo = self.fModelDDvlPloneTool().fRetrieveTypeConfig( 
                    theTimeProfilingResults     =theTimeProfilingResults,
                    theElement                  =unNuevoModulo, 
                    theParent                   =None,
                    theParentTraversalName      ='',
                    theTypeConfig               =None, 
                    theAllTypeConfigs           =None, 
                    theViewName                 ='', 
                    theRetrievalExtents         =[ 'traversals', ],
                    theWritePermissions         =None,
                    theFeatureFilters           ={ 'attrs': [ 'title',], 'relations': [], 'do_not_recurse_collections': True,}, 
                    theInstanceFilters          =None,
                    theTranslationsCaches       =None,
                    theCheckedPermissionsCache  =thePermissionsCache,
                    theAdditionalParams         =None                
                )
                if not unResultadoNuevoModulo:
                    anActionReport = { 'effect': 'error', 'failure': 'retrieval_failure', }
                    return anActionReport     
                
                
                aModelDDvlPloneTool_Mutators = self.fModelDDvlPloneTool().fModelDDvlPloneTool_Mutators( self)
                    
                aCreateElementReport = aModelDDvlPloneTool_Mutators.fNewVoidCreateElementReport()
                aCreateElementReport.update( { 'effect': 'created', 'new_object_result': unResultadoNuevoModulo, })
                
                someFieldReports    = aCreateElementReport[ 'field_reports']
                aFieldReportsByName = aCreateElementReport[ 'field_reports_by_name']
                
                aReportForField = { 'attribute_name': 'id',          'effect': 'changed', 'new_value': unaIdModulo, 'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                
                aReportForField = { 'attribute_name': 'title',       'effect': 'changed', 'new_value': aNewNombreModulo,           'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField

                aModelDDvlPloneTool_Mutators.pSetAudit_Creation( self, cModificationKind_CreateSubElement, aCreateElementReport, theUseCounter=True)       
                aModelDDvlPloneTool_Mutators.pSetAudit_Creation( unNuevoModulo,       cModificationKind_Create,           aCreateElementReport)       
                 
                
                
                
                unCatalogo.pFlushCachedTemplates_All()         
                
                
                
                unModuloCreationReport = { 'effect': 'created', 'new_object_result': unResultadoNuevoModulo, }
                        
                            
                return unModuloCreationReport
                
 
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fCrearModulo\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   
                                         
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                anActionReport = { 'effect': 'error', 'failure': '%s\n%s' % (   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Modulo_Exception_msgid', "Exception while creating new Module.-"), unInformeExcepcion, ) }
                return anActionReport     
              
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

        
            
            
            
    
    
    
    
    
    
    

        

    security.declareProtected( permissions.ManagePortal, 'fCreateProgressHandlerFor_DeleteModule')
    def fCreateProgressHandlerFor_DeleteModule( self, 
        theAdditionalParams      =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Request creation of a DeleteModule long-lived process control handler, to be executed later.
        
        """

        
        
        def fDeleteModuleInitialize_lambda( theContextualElement, theProcessControlManager, theAdditionalParmsHere):  
        
            if theContextualElement == None:
                return None
            
            if not theProcessControlManager:
                return None
            
            someInputParameters = theProcessControlManager.vInputParameters
            if not someInputParameters:
                return None
            
            aModulesCollectionUID = someInputParameters.get( 'modules_collection_UID', '')
            if not aModulesCollectionUID:
                return None
            unaColeccionModulos = theContextualElement.fElementoPorUID( aModulesCollectionUID)
            if unaColeccionModulos == None:
                return None
            
            aModuleUID = someInputParameters.get( 'module_UID', '')
            if not aModuleUID:
                return None
            unModulo = theContextualElement.fElementoPorUID( aModuleUID)
            if unModulo == None:
                return None
            
            aModuleName = unModulo.Title()
            someModuleNames = [ aModuleName,]
            
            unosInitializedObjects = {
                'modules_collection': unaColeccionModulos,
                'module':             unModulo,
                'module_names':       someModuleNames,
            }
                        
            theProcessControlManager.pAddInitializedObjects( unosInitializedObjects)
            
            return None        
                    
         
        
        
        
        
            
        def fDeleteModuleLoop_lambda( theInitialElement, theProcessControlManager, theAdditionalParmsHere):  
            
            if theInitialElement == None:
                return None
            
            if not theProcessControlManager:
                return None
               
            if not theProcessControlManager.vInitializedObjects:
                return None
               
            unaColeccionModulos = theProcessControlManager.vInitializedObjects.get( 'modules_collection', None)
            if unaColeccionModulos == None:
                return None
            
            unModulo = theProcessControlManager.vInitializedObjects.get( 'module', None)
            if unModulo == None:
                return None
            
            unosNombresModulos = theProcessControlManager.vInitializedObjects.get( 'module_names', None)
            if not unosNombresModulos:
                return None
            
            if theProcessControlManager.vCatalogoRaiz == None:
                return None            
            
            unasColeccionesCadenas = theProcessControlManager.vCatalogoRaiz.fObtenerTodasColeccionesCadenas()
            for unaColeccionCadenas in unasColeccionesCadenas:
                
                unasCadenas = unaColeccionCadenas.fObtenerTodasCadenas()
                for unaCadena in unasCadenas:
                    
                    theProcessControlManager.vElementLambda( unaCadena, theProcessControlManager, theAdditionalParmsHere)
            
                    
            aNumElementsOfType = { 
                cNombreTipoTRAModulo: 1,
            }
            theProcessControlManager.pProcessStep( unModulo, aNumElementsOfType, aNumElementsOfType)
                    
            
            unaColeccionModulos.manage_delObjects( [ unModulo.getId(), ])
            
            aNumElementsOfType = { 
                cNombreTipoTRAColeccionModulos: 1,
            }
            theProcessControlManager.pProcessStep( unaColeccionModulos, aNumElementsOfType, aNumElementsOfType)
            
            theProcessControlManager.vCatalogoRaiz.pInvalidateSimbolosCadenasOrdenados()
                        
            return None        
                    
            
            
        
        
        
            
        def fDeleteModuleElement_lambda( theElement, theProcessControlManager, theAdditionalParmsHere):  
            
            if theElement == None:
                return None
            
            if not theProcessControlManager:
                return None
            
            if not ( theElement.meta_type == cNombreTipoTRACadena):
                return None
            
            unosNombresModulos = theProcessControlManager.vInitializedObjects.get( 'module_names', None)
            if not unosNombresModulos:
                return None
            
            
            unNumCadenasChanged = 0
            unNumTranslationsReadAndChanged = 0
            if theElement.fRemoveNombresModulos( unosNombresModulos):
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

        
        
        
        
        
        unExecutionRecord = self.fStartExecution( 'method',  'fCreateProgressHandlerFor_DeleteModule', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }, ) 
        
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
                    
                aDeleteModuleResult = self.fNewVoidProgressResult()
                
                
                aProgressElement = None
                aProgressHandler = None
                
                aModuleUID = theAdditionalParams.get( 'module_uid', '')
                if not aModuleUID:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_Missing_Parameter_ModuleUID', "Required Parameter Missing: Module UID-."),
                    })
                    return aResult
                
                unModulo = self.fElementoPorUID( aModuleUID)
                if unModulo == None:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_Parameter_ModuleNoFoundByUID', "Module not found by UID-."),
                    })
                    return aResult
               
                aMetaType = 'UnknownType'
                try:
                    aMetaType = unModulo.meta_type
                except:
                    aMetaType = unModulo.__class__.__name
                if not aMetaType:
                    aMetaType = 'UnknownType'
                
                aStartDateTimeNowTextual = self.fDateTimeNowTextual()
                aDeleteModuleResult[ 'process_type']           = cTRAProgress_ProcessType_DeleteModule
                aDeleteModuleResult[ 'start_date_time_string'] = aStartDateTimeNowTextual
                aDeleteModuleResult[ 'date_time_now_string']   = aStartDateTimeNowTextual
                aDeleteModuleResult[ 'element_type']           = aMetaType
                aDeleteModuleResult[ 'element_title']          = unModulo.Title()
                aDeleteModuleResult[ 'element_path' ]          = unModulo.fPhysicalPathString()
                aDeleteModuleResult[ 'element_UID' ]           = unModulo.UID()
                aDeleteModuleResult[ 'last_element_type']      = ''
                aDeleteModuleResult[ 'last_element_title']     = ''
                aDeleteModuleResult[ 'last_element_path']      = ''
                aDeleteModuleResult[ 'last_element_UID']       = ''
                
                aMemberId = self.fGetMemberId()
                aDeleteModuleResult[ 'member_id'] = aMemberId
                
                aDeleteModuleResult[ 'TRACatalogo_title']      = unCatalogoRaiz.Title()
                aDeleteModuleResult[ 'TRACatalogo_path' ]      = unCatalogoRaiz.fPathDelRaiz()
                aDeleteModuleResult[ 'TRACatalogo_UID' ]       = unCatalogoRaiz.UID()
                
                    
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_DeleteTRAModulo, 
                    theElementsBindings     = { cBoundObject: unModulo,},
                    theRulesToCollect       = [ ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord
                )
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_no_permission_ToDeleteModule', "You do not have permission to Delete Module-."),
                    })
                    return aResult
                
                 
                
                aModulesCollectionUID = self.UID()
                
                
                someInputParameters = { 
                    'modules_collection_UID':  aModulesCollectionUID,
                    'module_UID':              aModuleUID,
                }

                aProgressHandlerCreationResult = unaColeccionProgresos.fCreateNewProgressAndHandlerForElement(  
                    theInitialElement       =unModulo, 
                    theProcessType          =cTRAProgress_ProcessType_DeleteModule, 
                    theInputParameters      =someInputParameters,
                    theTimestamp            =aStartDateTimeNowTextual,
                    theResult               =aDeleteModuleResult, 
                    theInitializeLambda     =fDeleteModuleInitialize_lambda,
                    theElementLambda        =fDeleteModuleElement_lambda,
                    theLoopLambda           =fDeleteModuleLoop_lambda,
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
                    unInformeExcepcion += 'Exception during fCreateProgressHandlerFor_DeleteModule of element %s %s at %s\n'  % (  self.meta_type(), self.Title(), self.fPhysicalPathString())
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
                
                aDeleteModuleResult[ 'success'] = False
                aDeleteModuleResult[ 'exception_date_time_string'] = self.fDateTimeNowTextual()
                aDeleteModuleResultDump = ''
                try:
                    aDeleteModuleResultDump = self.fProgressResult_dump( aDeleteModuleResult)
                except:
                    None
                if aDeleteModuleResultDump:
                    unInformeExcepcion += aDeleteModuleResultDump
                
                aDeleteModuleResult[ 'exception_report'] = unInformeExcepcionWOResult

                
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
           
            