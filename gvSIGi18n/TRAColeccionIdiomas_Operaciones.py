# -*- coding: utf-8 -*-
#
# File: TRAColeccionIdiomas_Operaciones.py
#
# Copyright (c) 2009 by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.gvSIGi18n.config import *

##code-section module-header #fill in your manual code here


import sys
import traceback
import logging

from Products.CMFCore        import permissions
from Products.CMFCore.utils  import getToolByName


from Products.ModelDDvlPloneTool.ModelDDvlPloneTool          import ModelDDvlPloneTool

from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators import ModelDDvlPloneTool_Mutators,cModificationKind_CreateSubElement, cModificationKind_Create


from TRAElemento_Constants import *

from TRAImportarExportar_Constants import *

from TRAElemento_Permission_Definitions import cUseCase_CreateTRAIdioma
from TRAElemento_Permission_Definitions import cBoundObject



##/code-section module-header



##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAColeccionIdiomas_Operaciones:
    """
    """
    security = ClassSecurityInfo()


    ##code-section class-header #fill in your manual code here
    

    # ###################################################################
    #   Parent and children access
    # ###############################                  
    


    

                                
                
    security.declareProtected( permissions.View, 'fObtenerTodosIdiomas')
    def fObtenerTodosIdiomas( self, ):
        """Retrieve all contained elements of type TRAIdioma.
        
        """
        unosElementos = self.objectValues( cNombreTipoTRAIdioma) 
        return unosElementos
         
          
    
    

    

    security.declarePrivate( 'fUseCaseCheckDoable_CreateTRAIdioma')    
    def fUseCaseCheckDoable_CreateTRAIdioma( self, theTypeName, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):   

 
        unExecutionRecord = self.fStartExecution( 'method',  'fUseCaseCheckDoable_CreateTRAIdioma', theParentExecutionRecord, False) 
        
        try:
            try:
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                    
                unUseCaseAssessmentResult = self.fUseCaseAssessment( 
                    theUseCaseName          = cUseCase_CreateTRAIdioma, 
                    theElementsBindings     = { cBoundObject : self,},
                    theRulesToCollect       = None, 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord)
                
                unResult = unUseCaseAssessmentResult and unUseCaseAssessmentResult.get( 'success', False)
                return unResult 
    
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fUseCaseCheckDoable_CreateTRAIdioma\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
    
                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return False

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
     
        

    
    security.declarePrivate( 'fCrearIdioma')    
    def fCrearIdioma( self,
        theTimeProfilingResults =None, # invoked from ModelDDvlPloneTool still using previous style of time profiling, thus the parameter is not theParentExecutionRecord =None, 
        theModelDDvlPloneTool_Mutators   =None, 
        theNewTypeName          ='', 
        theNewOneTitle          ='', 
        theNewOneDescription    ='', 
        theAdditionalParams     =None,
        thePermissionsCache     =None,
        theRolesCache           =None,
        theParentExecutionRecord=None):
        """Create a new instance of TRAIdioma through an import process. Ceate an instance of TRAImportacion with a TRAContenidoIntercambio that will create the language when the import is executed.
        
        """
    
        unExecutionRecord = self.fStartExecution( 'method',  'fCrearIdioma', None, True, { 'log_what': 'details', 'log_when': True, }) # invoked from ModelDDvlPloneTool still using previous style of time profiling, thus the parameter is not theParentExecutionRecord =None, 

        try:
            unasDescripcionesContenidosCreados = []
            try:
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_CreateTRAIdioma, 
                    theElementsBindings     = { cBoundObject: self,}, 
                    theRulesToCollect       = [ 'languages', ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord,
                )
              
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_no_permission_ToCreateLanguage_msgid', "User does not have permission to create languages (as an import process).-"), }
                    return anActionReport  
                            
                aModelDDvlPlone_tool = self.fModelDDvlPloneTool()
                             
                
                 
                aNewCodigoIdiomaEnGvSIG       = theAdditionalParams.get( 'theCodigoIdiomaEnGvSIG',          '')
                aCodigoInternacionalDeIdioma  = theAdditionalParams.get( 'theCodigoInternacionalDeIdioma',  '')
                aNewEnglishName               = theAdditionalParams.get( 'theEnglishName',                  '')
                aNewNombreNativoDeIdioma      = theAdditionalParams.get( 'theNombreNativoDeIdioma',         '')
                
                
        
                if not aNewCodigoIdiomaEnGvSIG:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Idioma_missingParameter_CodigoIdiomaEnGvSIG_warning_msgid', "The code in gvSIG for the new language is missing. Can not create a new language without a language code.-"), }
                    return anActionReport  

                if not aNewEnglishName:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Idioma_missingParameter_NewEnglishName_warning_msgid', "The language name expressed in english is missing. Can not create a new string request without a language name expressed in english .-"), }
                    return anActionReport  
                

                unCatalogo = self.getCatalogo()
                
                if not unCatalogo:
                    anActionReport = { 'effect': 'error', 'failure':  'InternalError: gvSIGi18n_errorCreating_Idioma_Missing_TRACatalogo_error_msgid', }
                    return anActionReport  
                
                
                unIdiomaPorCodigo = unCatalogo.fGetIdiomaPorCodigo( aNewCodigoIdiomaEnGvSIG)
                if not ( unIdiomaPorCodigo == None):
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Idioma_LanguageCodeAlreadyExists_warning_msgid', "A language with same code already exists in the translations catalog.-"), }
                    return anActionReport  

                someExistingKnownIdiomasCodesAndNames = unCatalogo.fNonExistingKnownIdiomasCodesAndNames()  
                for unCodigoIdioma, unNombreInglesDeIdioma, unNombreNativoDeIdioma in someExistingKnownIdiomasCodesAndNames:
                    if unCodigoIdioma == aNewCodigoIdiomaEnGvSIG:
                        aCodigoInternacionalDeIdioma    = unCodigoIdioma
                        aNewEnglishName                 = unNombreInglesDeIdioma
                        aNewNombreNativoDeIdioma    = unNombreNativoDeIdioma
                        break
                
                unaColeccionImportaciones = unCatalogo.fObtenerColeccionImportaciones()
                if not unaColeccionImportaciones:
                    anActionReport = { 'effect': 'error', 'failure':  'InternalError: gvSIGi18n_errorCreating_Idioma_Missing_TRAColeccionImportaciones_error_msgid', }
                    return anActionReport  
                
                     
                unMemberId = self.fGetMemberId()
                unaFechaYHora = self.fDateTimeNowTextual()

                aPloneUtilsTool = self.getPloneUtilsToolForNormalizeString()  
               
                unTitleImportacion = '%s %s %s %s %s' % ( self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_crearIdioma_Importacion_prefix', "To Create Language"), aNewCodigoIdiomaEnGvSIG, aNewEnglishName, unMemberId, unaFechaYHora, )
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
                    anActionReport = { 'effect': 'error', 'failure': '%s' %   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Idioma_TRAImportacion_NotCreated_msgid', "Error creating language: import not created.-"), }
                    return anActionReport     
                                
                
                
                
                
                unaNuevaImportacion = unaColeccionImportaciones.getElementoPorID( unaIdNuevaImportacion)
                if not unaNuevaImportacion:
                    anActionReport = { 'effect': 'error', 'failure': '%s' %  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Idioma_TRAImportacion_Created_TRAImportacion_NotFound_msgid', "Could not find import just created-."), }
                    return anActionReport     

                unMemberId = self.fGetMemberId()
                unaFechaYHora = self.fDateTimeNowTextual()
                
                unTitleContenidoIntercambio = '%s %s by %s on %s' % ( self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_crearIdioma_Importacion_prefix', "To Create Language"), aNewCodigoIdiomaEnGvSIG, unMemberId, unaFechaYHora,)
                aNewIdContenidoIntercambio = unTitleContenidoIntercambio.lower().replace( ' ', '-')
                if aPloneUtilsTool:
                    aNewIdContenidoIntercambio = aPloneUtilsTool.normalizeString( aNewIdContenidoIntercambio)
 
                anAttrsDictContenidoIntercambio = { 
                    'title':         unTitleContenidoIntercambio,
                    'description':   '',
                }
                
                unaNuevaImportacion.setCodigoIdiomaPorDefecto( aNewCodigoIdiomaEnGvSIG)
                unaNuevaImportacion.setNombreModuloPorDefecto( '')
                
                
                unaIdNuevoContenidoIntercambio = unaNuevaImportacion.invokeFactory( cNombreTipoTRAContenidoIntercambio, aNewIdContenidoIntercambio, **anAttrsDictContenidoIntercambio)
                if not unaIdNuevoContenidoIntercambio:
                    anActionReport = { 'effect': 'error', 'failure': '%s' %   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Idioma_TRAContenidoIntercambio_NotCreated_msgid', "Error creating language: import not created.-"), }
                    return anActionReport     
                                
                
                
                unNuevoContenidoIntercambio = unaNuevaImportacion.getElementoPorID( unaIdNuevoContenidoIntercambio)
                if not unNuevoContenidoIntercambio:
                    anActionReport = { 'effect': 'error', 'failure': '%s' %  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Idioma_Created_TRAContenidoIntercambio_NotFound_msgid', "Could not find interchange contents just created-."), }
                    return anActionReport     
                
                unContenidoConIdioma = { 
                    'languages':         [ aNewCodigoIdiomaEnGvSIG, ], 
                    'languages_details': { 
                        aNewCodigoIdiomaEnGvSIG: {
                            'codigo_internacional_idioma': aCodigoInternacionalDeIdioma, 
                            'english_name':                aNewEnglishName, 
                            'nombre_nativo_de_idioma':     aNewNombreNativoDeIdioma,
                        },
                    },
                }
                unNuevoContenidoIntercambio.pSetContenido( unContenidoConIdioma)
                
                
                
                
                
                
                
                
                
                
                aCopyFromLanguageCode         = theAdditionalParams.get( 'theCopyFromLanguageCode',         '')
                if aCopyFromLanguageCode and not ( aCopyFromLanguageCode == '---'):
                    aCopiarTraduccionesReport = self.fCopiarTraduccionesEnNuevoIdioma( 
                        theNewLanguageCode          = aNewCodigoIdiomaEnGvSIG,
                        theCopyFromLanguageCode     = aCopyFromLanguageCode,
                        theSourceStatesToCopy       = None,
                        theNuevaImportacion         = unaNuevaImportacion,
                        theUseCaseQueryResult       = unUseCaseQueryResult,
                        theParentExecutionRecord    = unExecutionRecord)                
                
                    if ( not aCopiarTraduccionesReport) or not ( aCopiarTraduccionesReport.get( 'effect', '') == 'created'):
                        anActionReport = { 
                            'effect': 'error', 
                            'failure': '%s %s' %  ( 
                                self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Idioma_Error_Creating_TRAContenidoIntercambio_ToCopyTranslations', "Could not create contents to copy translations-."),
                                aCopiarTraduccionesReport.get( 'failure', ''),
                            )
                        }
                        return anActionReport     
                    
                   
        

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
 
                unIdiomaCreationReport = { 'effect': 'created', 'new_object_result': unResultadoNuevaImportacion, }
                        
            
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
                unaNuevaImportacion.pFlushCachedTemplates_All()                            
                            
                return unIdiomaCreationReport
                
 
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fCrearIdioma\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                                         
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                anActionReport = { 'effect': 'error', 'failure': '%s\n%s' % (   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Idioma_Exception_msgid', "Exception while creating new string request.-"), unInformeExcepcion, ) }
                return anActionReport     
              
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

        
            
            
            
            
            
            
            
            

    

    
    security.declarePrivate( 'fCopiarTraduccionesEnNuevoIdioma')    
    def fCopiarTraduccionesEnNuevoIdioma( self,
        theNewLanguageCode          = '',
        theCopyFromLanguageCode     = '',
        theSourceStatesToCopy       = [],
        theNuevaImportacion         = None,
        theUseCaseQueryResult       = None,
        theParentExecutionRecord    = None):
        """Create interchange contents to create into the new language Translations from the Language with the specified code. If Source States is specified, only copy source translations on those states. If Target States is specified.
        
        """
    
        unExecutionRecord = self.fStartExecution( 'method',  'fCopiarTraduccionesEnNuevoIdioma', None, True, { 'log_what': 'details', 'log_when': True, }) # invoked from ModelDDvlPloneTool still using previous style of time profiling, thus the parameter is not theParentExecutionRecord =None, 

        try:
            unasDescripcionesContenidosCreados = []
            try:
                
                if not theNewLanguageCode:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_action_missingParameter_NewLanguageCode', "Parameter Error: Missing parameter: New Language Code to copy Translations into.-"), }
                    return anActionReport  
                
                if ( not theCopyFromLanguageCode) or ( theCopyFromLanguageCode == '---'):
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_action_missingParameter_CopyFromLanguageCode', "Parameter Error: Missing parameter: source Language Code to copy Translations from.-"), }
                    return anActionReport  
                
                if ( theNuevaImportacion == None):
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_action_missingParameter_theNuevaImportacion', "Parameter Error: Missing parameter: theNuevaImportacion import to create language and copy translations insto.-"), }
                    return anActionReport  
                
                
                
                if theNewLanguageCode == theCopyFromLanguageCode:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_action_warning_CanNotCopyTranslationsFromSameLanguage', "You can not copy Translations from the same Language.-"), }
                    return anActionReport  
                 
                if not theUseCaseQueryResult or not theUseCaseQueryResult.get( 'success', False):
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_no_permission_ToCopyTranslations_msgid', "User does not have permission to copy Translations from other language.-"), }
                    return anActionReport  
                                
                unosIdiomasAccesibles = theUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'languages', {}).get( 'accepted_final_objects', [])
                if not unosIdiomasAccesibles:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_action_warning_NoAvailableLanguagesToCopyFrom', "You can not copy Translations, there are no available Languages to copy from.-"), }
                    return anActionReport  
                            
                unSourceIdioma = None
                for unIdioma in unosIdiomasAccesibles:
                    if unIdioma.getCodigoIdiomaEnGvSIG() == theCopyFromLanguageCode:
                        unSourceIdioma = unIdioma
                        break
                if not unSourceIdioma:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_action_warning_SelectedSourceLanguageIsNotAvailable', "You can not copy Translations from the selected source Language because it is not available.-"), }
                    return anActionReport  
                
                unCatalogo = self.getCatalogo()
                if not unCatalogo:
                    anActionReport = { 'effect': 'error', 'failure':  'InternalError: gvSIGi18n_copyTranslations_internalError_Missing_TRACatalogo_error_msgid', }
                    return anActionReport  

                unCatalogBusquedaTraduccionesInSourceIdioma = unCatalogo.fCatalogBusquedaTraduccionesParaIdioma( unSourceIdioma)
                if ( unCatalogBusquedaTraduccionesInSourceIdioma == None):
                    anActionReport = { 'effect': 'error', 'failure':  'InternalError: gvSIGi18n_copyTranslations_internalError_Missing_CatalogBusquedaTraducciones_SourceLanguage', }
                    return anActionReport  
               
                
                unaBusqueda = {   'getEstadoCadena' :     cEstadoCadenaActiva, }
                
                someSourceStatesToCopy = [ ]
                if theSourceStatesToCopy:
                    for unEstado in [ cEstadoTraduccionTraducida, cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva]:
                        if unEstado in theSourceStatesToCopy:
                            someSourceStatesToCopy.append( unEstado)
                else:
                    someSourceStatesToCopy = [ cEstadoTraduccionTraducida, cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva]
                    
                if someSourceStatesToCopy:
                    unaBusqueda.update( {   'getEstadoTraduccion' :     someSourceStatesToCopy, })
                    
                           
                unosResultadosBusqueda      = unCatalogBusquedaTraduccionesInSourceIdioma.searchResults(**unaBusqueda)
                
                unasTraduccionesACopiar = [ ]
                for unResultadoBusqueda in unosResultadosBusqueda:
                    unaTraducccion = unResultadoBusqueda.getObject()
                    if unaTraducccion:
                        unaCadenaTraducida = unaTraducccion.getCadenaTraducida()
                        if unaCadenaTraducida:
                            unasTraduccionesACopiar.append( unaTraducccion)
                        
                if not unasTraduccionesACopiar:
                    if theSourceStatesToCopy:
                        anActionReport = { 'effect': 'warning', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_action_warning_NoTranslationsInSourceLanguageInSpecifiedStates', "There are no Translations in the selected source Language in the specified states.-"), }
                    else:
                        anActionReport = { 'effect': 'warning', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_action_warning_NoTranslationsInSourceLanguage', "There are no Translations in the selected source Language.-"), }
                    return anActionReport  

                        
                
                aModelDDvlPlone_tool = self.fModelDDvlPloneTool()
                             

                unMemberId    = self.fGetMemberId()
                unaFechaYHora = self.fDateTimeNowTextual()

                aPloneUtilsTool = self.getPloneUtilsToolForNormalizeString()  
               

                unTitleContenidoIntercambio = '%s %s->%s ' % ( self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_Importacion_prefix', "To Copy Translations from Language to Language"), theCopyFromLanguageCode, theNewLanguageCode, )
                aNewIdContenidoIntercambio = unTitleContenidoIntercambio.lower().replace( ' ', '-')
                if aPloneUtilsTool:
                    aNewIdContenidoIntercambio = aPloneUtilsTool.normalizeString( aNewIdContenidoIntercambio)
 
                anAttrsDictContenidoIntercambio = { 
                    'title':         unTitleContenidoIntercambio,
                    'description':   '',
                }
                
                unaIdNuevoContenidoIntercambio = theNuevaImportacion.invokeFactory( cNombreTipoTRAContenidoIntercambio, aNewIdContenidoIntercambio, **anAttrsDictContenidoIntercambio)
                if not unaIdNuevoContenidoIntercambio:
                    anActionReport = { 'effect': 'error', 'failure': '%s' %   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Idioma_TRAContenidoIntercambio_NotCreated_msgid', "Error creating language: import not created.-"), }
                    return anActionReport     
                                
                unNuevoContenidoIntercambio = theNuevaImportacion.getElementoPorID( unaIdNuevoContenidoIntercambio)
                if not unNuevoContenidoIntercambio:
                    anActionReport = { 'effect': 'error', 'failure': '%s' %  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Idioma_Created_TRAContenidoIntercambio_NotFound_msgid', "Could not find interchange contents just created-."), }
                    return anActionReport     
                
                
                someStringsAndTranslations = { }
                
                for unaTraduccion in unasTraduccionesACopiar:
                    unSimboloCadena                     = unaTraduccion.getSimbolo()
                    unaCadenaTraducida                  = unaTraduccion.getCadenaTraducida()
                    if unaCadenaTraducida:
                        unasTraduccionesCadena = { theNewLanguageCode: unaCadenaTraducida,}
                        someStringsAndTranslations[ unSimboloCadena] = unasTraduccionesCadena
                                        
                
                unContenidoConCadenas = { 'strings_and_translations': someStringsAndTranslations, }
                unNuevoContenidoIntercambio.pSetContenido( unContenidoConCadenas)
                
                unStringsCreationReport = { 'effect': 'created', 'new_object_result': { 'object': unNuevoContenidoIntercambio,}, }
                        
                return unStringsCreationReport
                
 
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fCopiarTraduccionesEnNuevoIdioma\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                                         
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                anActionReport = { 'effect': 'error', 'failure': '%s\n%s' % (   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Cadeas_Exception_msgid', "Exception while creating Strings (as import process).-"), unInformeExcepcion, ) }
                return anActionReport     
              
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

                    
                            
            
            
            
            
            
            
            
                
                    
    
    ##/code-section class-header

    # Methods

# end of class TRAColeccionIdiiomas_Operaciones

##code-section module-footer #fill in your manual code here
##/code-section module-footer



