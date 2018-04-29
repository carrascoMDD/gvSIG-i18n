# -*- coding: utf-8 -*-
#
# File: TRAColeccionModulos_Operaciones.py
#
# Copyright (c) 2008, 2009,2010 by Conselleria de Infraestructuras y Transporte de la
# Generalidad Valenciana
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



from TRAImportarExportar_Constants import *

from TRAElemento_Permission_Definitions import cUseCase_CreateTRAModulo, cUseCase_DeleteTRAModulo
from TRAElemento_Permission_Definitions import cBoundObject



class TRAColeccionModulos_Operaciones:
    """
    """
    security = ClassSecurityInfo()
     




    security.declarePrivate( 'pAllSubElements_into')    
    def pAllSubElements_into( self, theCollection, theAdditionalParms=None):
        if theCollection == None:
            return self
        theCollection.append( self)
        
        
        unosElementos = self.fObtenerTodosModulos()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pAllSubElements_into( theCollection,theAdditionalParms=theAdditionalParms)
        
        return self
        

    


    security.declarePrivate( 'pForAllElementsDo_recursive')    
    def pForAllElementsDo_recursive( self, theLambda):
        if not theLambda:
            return self
        
        theLambda( self)

        unosElementos = self.fObtenerTodosModulos()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda)
        
        return self
        

          
    
    
    security.declareProtected( permissions.View, 'fObtenerTodosModulos')
    def fObtenerTodosModulos( self, ):
        """Retrieve all contained elements of type TRAModulo.
        
        """
        unosElementos = self.objectValues( cNombreTipoTRAModulo) 
        return unosElementos
         

    
    

    

    
    security.declarePrivate( 'fCrearModulo')    
    def fCrearModulo( self,
        theTimeProfilingResults =None, # 
        theModelDDvlPloneTool_Mutators   =None, 
        theNewTypeName          ='', 
        theNewOneTitle          ='', 
        theNewOneDescription    ='', 
        theAdditionalParams     =None,
        thePermissionsCache     =None,
        theRolesCache           =None,
        theParentExecutionRecord=None):
        """Create a new instance of TRAModulo through an import process. Ceate an instance of TRAImportacion with a TRAContenidoIntercambio that will create the module when the import is executed.
        
        """
    
        unExecutionRecord = self.fStartExecution( 'method',  'fCrearModulo', None, True, { 'log_what': 'details', 'log_when': True, })

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators import ModelDDvlPloneTool_Mutators,cModificationKind_CreateSubElement, cModificationKind_Create

        try:
            unasDescripcionesContenidosCreados = []
            try:
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_CreateTRAModulo, 
                    theElementsBindings     = { cBoundObject: self,}, 
                    theRulesToCollect       = [ 'modules', ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord,
                )
              
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_no_permission_ToCreateModule_msgid', "User does not have permission to create modules (as an import process).-"), }
                    return anActionReport  
                            
                aModelDDvlPlone_tool = self.fModelDDvlPloneTool()
                             
                
                 
                aNewNombreModulo       = theAdditionalParams.get( 'theNewModuleName',          '')
                if not aNewNombreModulo:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Modulo_missingParameter_Nombre_warning_msgid', "The Module name is missing. The Module name is required to create a new Module.-"), }
                    return anActionReport  
                
                aNewNombreModulo = aNewNombreModulo.replace(',', ' ')
                somePartsNewNombreModulo = aNewNombreModulo.strip().split( cTRAModuleNameSeparator)
                if not somePartsNewNombreModulo:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Modulo_missingParameter_Nombre_warning_msgid', "The Module name is missing. The Module name is required to create a new Module.-"), }
                    return anActionReport  
                aNewNombreModulo = somePartsNewNombreModulo[0 ]
                if not aNewNombreModulo:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Modulo_missingParameter_Nombre_warning_msgid', "The Module name is missing. The Module name is required to create a new Module.-"), }
                    return anActionReport  

                unCatalogo = self.getCatalogo()
                
                if not unCatalogo:
                    anActionReport = { 'effect': 'error', 'failure':  'InternalError: gvSIGi18n_errorCreating_Modulo_Missing_TRACatalogo_error_msgid', }
                    return anActionReport  
                
                
                unModuloPorNombre = unCatalogo.fGetModuloPorNombre( aNewNombreModulo)
                if not ( unModuloPorNombre == None):
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Modulo_ModuleNameAlreadyExists_warning_msgid', "A module with same name already exists in the translations catalog.-"), }
                    return anActionReport  

                
                unaColeccionImportaciones = unCatalogo.fObtenerColeccionImportaciones()
                if not unaColeccionImportaciones:
                    anActionReport = { 'effect': 'error', 'failure':  'InternalError: gvSIGi18n_errorCreating_Modulo_Missing_TRAColeccionImportaciones_error_msgid', }
                    return anActionReport  
                
                     
                unMemberId = self.fGetMemberId()
                unaFechaYHora = self.fDateTimeNowTextual()

                aPloneUtilsTool = self.getPloneUtilsToolForNormalizeString()  
               
                unTitleImportacion = '%s %s %s %s' % ( self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_crearModulo_Importacion_prefix', "To Create Module"), aNewNombreModulo, unMemberId, unaFechaYHora, )
                aNewIdImportacion = unTitleImportacion.lower().replace( ' ', '-')
                if aPloneUtilsTool:
                    aNewIdImportacion = aPloneUtilsTool.normalizeString( aNewIdImportacion)
 
                anAttrsDictImportacion = { 
                    'title':         unTitleImportacion,
                    'description':   '',
                }
                
                unaColeccionImportaciones.pFlushCachedTemplates_All()                            

                unaIdNuevaImportacion = unaColeccionImportaciones.invokeFactory( cNombreTipoTRAImportacion, aNewIdImportacion, **anAttrsDictImportacion)
                if not unaIdNuevaImportacion:
                    anActionReport = { 'effect': 'error', 'failure': '%s' %   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Modulo_TRAImportacion_NotCreated_msgid', "Error creating module: import not created.-"), }
                    return anActionReport     
                                
                
                
                
                
                unaNuevaImportacion = unaColeccionImportaciones.getElementoPorID( unaIdNuevaImportacion)
                if not unaNuevaImportacion:
                    anActionReport = { 'effect': 'error', 'failure': '%s' %  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Modulo_TRAImportacion_Created_TRAImportacion_NotFound_msgid', "Could not find import just created-."), }
                    return anActionReport     
                
                
                unaNuevaImportacion.setCodigoIdiomaPorDefecto( '')
                unaNuevaImportacion.setNombreModuloPorDefecto( aNewNombreModulo)
                

                
                unTitleContenidoIntercambio = '%s %s by %s on %s' % ( self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_crearModulo_Importacion_prefix', "To Create Module"), aNewNombreModulo, unMemberId, unaFechaYHora,)
                aNewIdContenidoIntercambio = unTitleContenidoIntercambio.lower().replace( ' ', '-')
                if aPloneUtilsTool:
                    aNewIdContenidoIntercambio = aPloneUtilsTool.normalizeString( aNewIdContenidoIntercambio)
 
                
                

                anAttrsDictContenidoIntercambio = { 
                    'title':         unTitleContenidoIntercambio,
                    'description':   '',
                    'nombreModulo':  aNewNombreModulo,
                }                
                
                unaIdNuevoContenidoIntercambio = unaNuevaImportacion.invokeFactory( cNombreTipoTRAContenidoIntercambio, aNewIdContenidoIntercambio, **anAttrsDictContenidoIntercambio)
                if not unaIdNuevoContenidoIntercambio:
                    anActionReport = { 'effect': 'error', 'failure': '%s' %   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Modulo_TRAContenidoIntercambio_NotCreated_msgid', "Error creating module: import not created.-"), }
                    return anActionReport     
                                
                
                unNuevoContenidoIntercambio = unaNuevaImportacion.getElementoPorID( unaIdNuevoContenidoIntercambio)
                if not unNuevoContenidoIntercambio:
                    anActionReport = { 'effect': 'error', 'failure': '%s' %  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Modulo_Created_TRAContenidoIntercambio_NotFound_msgid', "Could not find interchange contents just created-."), }
                    return anActionReport     
                
                unContenidoConModulo = { 
                    'modules':         [ aNewNombreModulo, ], 
                }
                unNuevoContenidoIntercambio.pSetContenido( unContenidoConModulo)
                
                
                
                
                
                
          

                unTimeProfilingResults = { }
                unResultadoNuevaImportacion = aModelDDvlPlone_tool.fRetrieveTypeConfig( 
                    theTimeProfilingResults     =unTimeProfilingResults,
                    theElement                  =unaNuevaImportacion, 
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
                    theCheckedPermissionsCache  =None,
                    theAdditionalParams         =None                
                )
                if not unResultadoNuevaImportacion:
                    anActionReport = { 'effect': 'error', 'failure': 'retrieval_failure', }
                    return anActionReport     
 
                unModuloCreationReport = { 'effect': 'created', 'new_object_result': unResultadoNuevaImportacion, }
                        
            
                aModelDDvlPloneTool_Mutators = ModelDDvlPloneTool_Mutators()
                    
                aCreateElementReport = aModelDDvlPloneTool_Mutators.fNewVoidCreateElementReport()
                aCreateElementReport.update( { 'effect': 'created', 'new_object_result': unResultadoNuevaImportacion, })
                
                someFieldReports    = aCreateElementReport[ 'field_reports']
                aFieldReportsByName = aCreateElementReport[ 'field_reports_by_name']
                
                aReportForField = { 'attribute_name': 'id',    'effect': 'changed', 'new_value': unaIdNuevoContenidoIntercambio, 'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                
                aReportForField = { 'attribute_name': 'title', 'effect': 'changed', 'new_value': unTitleContenidoIntercambio,    'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                
                                   
                aModelDDvlPloneTool_Mutators.pSetAudit_Creation( unaColeccionImportaciones, cModificationKind_CreateSubElement, aCreateElementReport, theUseCounter=True)       
                aModelDDvlPloneTool_Mutators.pSetAudit_Creation( unaNuevaImportacion,       cModificationKind_Create,  aCreateElementReport)       
                
                
                aContenidoIntercambioTraversalResult = None
                for aTraversalResult in unResultadoNuevaImportacion.get( 'traversals', []):
                    if aTraversalResult.get( 'traversal_name', '') == cNombreTraversal_Importacion_ContenidosIntercambio:
                        aContenidoIntercambioTraversalResult = aTraversalResult
                        break
                if aContenidoIntercambioTraversalResult: 
                    someContenidoIntercambioResults = aContenidoIntercambioTraversalResult.get( 'elements', [])
                    
                    for aContenidoIntercambioResult in someContenidoIntercambioResults:
                        
                        unNuevoContenidoIntercambioElement = aContenidoIntercambioResult.get( 'object', None)
                        if not ( unNuevoContenidoIntercambioElement == None):
                        
                            unNuevoContenidoIntercambioElement.pFlushCachedTemplates_All()                            
                            
                            aCreateElementReport = aModelDDvlPloneTool_Mutators.fNewVoidCreateElementReport()
                            aCreateElementReport.update( { 'effect': 'created', 'new_object_result': aContenidoIntercambioResult, })
                            
                            someFieldReports    = aCreateElementReport[ 'field_reports']
                            aFieldReportsByName = aCreateElementReport[ 'field_reports_by_name']
                            
                            aReportForField = { 'attribute_name': 'id',     'effect': 'changed', 'new_value': aContenidoIntercambioResult.get( 'id', ''),     'previous_value': '',}
                            someFieldReports.append( aReportForField)            
                            aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                            
                            aReportForField = { 'attribute_name': 'title',  'effect': 'changed', 'new_value': aContenidoIntercambioResult.get( 'title', ''),  'previous_value': '',}
                            someFieldReports.append( aReportForField)            
                            
                            aModelDDvlPloneTool_Mutators.pSetAudit_Creation( unaNuevaImportacion,                cModificationKind_CreateSubElement, aCreateElementReport, theUseCounter=True)       
                            aModelDDvlPloneTool_Mutators.pSetAudit_Creation( unNuevoContenidoIntercambioElement, cModificationKind_Create,           aCreateElementReport)       
                
                            
                unaColeccionImportaciones.pFlushCachedTemplates_All()                            
                            
                return unModuloCreationReport
                
 
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fCrearModulo\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                                         
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                anActionReport = { 'effect': 'error', 'failure': '%s\n%s' % (   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Modulo_Exception_msgid', "Exception while creating new Module.-"), unInformeExcepcion, ) }
                return anActionReport     
              
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

        
            
            
            
    
    
    
    
    
    
    

        

    security.declareProtected( permissions.ManagePortal, 'fRequestNewDeleteModule')
    def fRequestNewDeleteModule( self, 
        theAdditionalParms      =None,  
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

        
        
        
        
        
        unExecutionRecord = self.fStartExecution( 'method',  'fRequestNewDeleteModule', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }, ) 
        
        
        try:
            
            
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                
            aDeleteModuleResult = self.fNewVoidProgressResult()
            
            
            aProgressElement = None
            aThereWasException = False
            aProgressHandler = None
            
            try:
                
                aModuleUID = theAdditionalParms.get( 'module_uid', '')
                if not aModuleUID:
                    return None
                
                unModulo = self.fElementoPorUID( aModuleUID)
                if unModulo == None:
                    return None
               
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
                
                unCatalogoRaiz = self.getCatalogo()           
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
                    aDeleteModuleResult[ 'success']   =  False
                    aDeleteModuleResult[ 'condition'] = 'gvSIGi18n_no_permission_ToDeleteModule'
                    aDeleteModuleResult[ 'date_time_now_string']   = self.fDateTimeNowTextual()
                    return None
                
                 
                
                aModulesCollectionUID = self.UID()
                
                
                someInputParameters = { 
                    'modules_collection_UID':  aModulesCollectionUID,
                    'module_UID':              aModuleUID,
                }

                aProgressHandler, aProgressElement = self.fCreateNewProgressAndHandlerForElement(  
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
                if ( not aProgressHandler) or ( aProgressElement == None):
                    return None
                
                aProgressHandler_Key = aProgressHandler.fKey()
                
                return aProgressHandler_Key
            
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                aThereWasException = True
                unInformeExcepcion = ''
                try:
                    unInformeExcepcion += 'Exception during fRequestNewDeleteModule of element %s %s at %s\n'  % (  self.meta_type(), self.Title(), self.fPhysicalPathString())
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
                
                return None
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
           
            