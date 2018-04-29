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

from Products.CMFCore       import permissions

from Products.ModelDDvlPloneTool.ModelDDvlPloneTool import ModelDDvlPloneTool

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
    

    security.declareProtected( permissions.View, 'getCatalogo')
    def getCatalogo( self):
        """Retrieve container element (shall be of type TRACatalogo).
        
        """
        return self.getContenedor()
        
        
    

                                
                
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
                    theRulesToCollect       = None, 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord,
                )
              
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_no_permission_ToCreateLanguage_msgid', "User does not have permission to create languages (as an import process).-"), }
                    return anActionReport  
                            
                aModelDDvlPlone_tool = ModelDDvlPloneTool()
                             
                
                 
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
                
                unaIdNuevaImportacion = unaColeccionImportaciones.invokeFactory( cNombreTipoTRAImportacion, aNewIdImportacion, **anAttrsDictImportacion)
                if not unaIdNuevaImportacion:
                    anActionReport = { 'effect': 'error', 'failure': '%s' %   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Idioma_TRAImportacion_NotCreated_msgid', "Error creating language: import not created.-"), }
                    return anActionReport     
                                
                unaNuevaImportacion = unaColeccionImportaciones.getElementoPorID( unaIdNuevaImportacion)
                if not unaNuevaImportacion:
                    anActionReport = { 'effect': 'error', 'failure': '%s' %  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Idioma_TRAImportacion_Created_TRAImportacion_NotFound_msgid', "Could not find import just created-."), }
                    return anActionReport     

                unTitleContenidoIntercambio = '%s %s' % ( self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_crearIdioma_Importacion_prefix', "To Create Language"), aNewCodigoIdiomaEnGvSIG, )
                aNewIdContenidoIntercambio = unTitleContenidoIntercambio.lower().replace( ' ', '-')
                if aPloneUtilsTool:
                    aNewIdContenidoIntercambio = aPloneUtilsTool.normalizeString( aNewIdContenidoIntercambio)
 
                anAttrsDictContenidoIntercambio = { 
                    'title':         unTitleContenidoIntercambio,
                    'description':   '',
                }
                
                unaIdNuevoContenidoIntercambio = unaNuevaImportacion.invokeFactory( cNombreTipoTRAContenidoIntercambio, aNewIdContenidoIntercambio, **anAttrsDictContenidoIntercambio)
                if not unaIdNuevoContenidoIntercambio:
                    anActionReport = { 'effect': 'error', 'failure': '%s' %   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Idioma_TRAContenidoIntercambio_NotCreated_msgid', "Error creating language: import not created.-"), }
                    return anActionReport     
                                
                unNuevoContenidoIntercambio = unaNuevaImportacion.getElementoPorID( unaIdNuevoContenidoIntercambio)
                if not unNuevoContenidoIntercambio:
                    anActionReport = { 'effect': 'error', 'failure': '%s' %  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Idioma_Created_TRAContenidoIntercambio_NotFound_msgid', "Could not find interchange contents just created-."), }
                    return anActionReport     
                
                unContenidoConIdioma = { 'languages': [ aNewCodigoIdiomaEnGvSIG, ], }
                unNuevoContenidoIntercambio.pSetContenido( unContenidoConIdioma)
                
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

        
                
                    
    
    ##/code-section class-header

    # Methods

# end of class TRAColeccionIdiiomas_Operaciones

##code-section module-footer #fill in your manual code here
##/code-section module-footer



