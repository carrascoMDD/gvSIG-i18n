# -*- coding: utf-8 -*-
#
# File: TRAColeccionSolicitudesCadenas_Operaciones.py
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

from TRAElemento_Permission_Definitions import cUseCase_CreateTRASolicitudCadena, cUseCase_CreateTRACadena, cUseCase_CleanupTRAColeccionSolicitudesCadenas
from TRAElemento_Permission_Definitions import cBoundObject


##/code-section module-header



##code-section after-local-schema #fill in your manual code here


cEstadoSolicitudCadena_Pending = 'Pendiente'

##/code-section after-local-schema



##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAColeccionSolicitudesCadenas_Operaciones:
    """
    """
    security = ClassSecurityInfo()

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    
    
        
# ###################################################################
#   Parent and children access
# ###############################                  
    

    security.declareProtected( permissions.View, 'getCatalogo')
    def getCatalogo( self):
        """Retrieve container element (shall be of type TRACatalogo).
        
        """
        return self.getContenedor()
        
        
    

                                
                
    security.declareProtected( permissions.View, 'fObtenerTodasSolicitudesCadenas')
    def fObtenerTodasSolicitudesCadenas( self, ):
        """Retrieve all contained elements of type TRASolicitudCadena.
        
        """
        someSolicitudesCadenas = self.objectValues( cNombreTipoTRASolicitudCadena) 
        return someSolicitudesCadenas
         
      
    
    

                
    security.declareProtected( permissions.View, 'fObtenerSolicitudesCadenasPendientes')
    def fObtenerSolicitudesCadenasPendientes( self, ):
        """Retrieve all contained elements of type TRASolicitudCadena, which are in pending status.
        
        """
        someSolicitudesCadenas = self.fObtenerTodasSolicitudesCadenas()
        
        somePendingSolicitudesCadenas = []
        
        for unaSolicitudCadena in someSolicitudesCadenas:
            unEstadoSolicitudCadena = unaSolicitudCadena.getEstadoSolicitudCadena() 
            if ( not unEstadoSolicitudCadena) or ( unEstadoSolicitudCadena == cEstadoSolicitudCadena_Pending):
                somePendingSolicitudesCadenas.append( unaSolicitudCadena)
                
        return somePendingSolicitudesCadenas
         
      
    
    



    
    security.declarePrivate( 'fCrearSolicitudCadena')    
    def fCrearSolicitudCadena( self,
        theTimeProfilingResults =None, # invoked from ModelDDvlPloneTool still using previous style of time profiling, thus the parameter is not theParentExecutionRecord =None, 
        theModelDDvlPloneTool_Mutators   =None, 
        theNewTypeName          ='', 
        theNewOneTitle          ='', 
        theNewOneDescription    ='', 
        theAdditionalParams     =None,
        thePermissionsCache     =None,
        theRolesCache           =None,
        theParentExecutionRecord=None):
        """Create a new instance of TRASolicitudCadena.
        
        """
    
        unExecutionRecord = self.fStartExecution( 'method',  'fCrearSolicitudCadena', None, True, { 'log_what': 'details', 'log_when': True, }) # invoked from ModelDDvlPloneTool still using previous style of time profiling, thus the parameter is not theParentExecutionRecord =None, 

        try:
            unasDescripcionesContenidosCreados = []
            try:
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_CreateTRASolicitudCadena, 
                    theElementsBindings     = { cBoundObject: self,}, 
                    theRulesToCollect       = None, 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord,
                )
              
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_no_permission_ToCreateNewStringRequest_msgid', "User does not have permission to create new string requests.-"), }
                    return anActionReport  
                            
                aModelDDvlPlone_tool = ModelDDvlPloneTool()
                             
                
                unNewTypeName = theNewTypeName
                if not unNewTypeName:
                    unNewTypeName = cNombreTipoTRASolicitudCadena
                
                aNewSymbol                          = theAdditionalParams.get( 'theNewSymbol', None)
                aMainlanguage                       = theAdditionalParams.get( 'theMainLanguage',    None)
                aTranslationIntoMainLanguage        = theAdditionalParams.get( 'theTranslationIntoMainLanguage',    None)
                aReferenceLanguage                  = theAdditionalParams.get( 'theReferenceLanguage',    None)
                aTranslationIntoReferenceLanguage   = theAdditionalParams.get( 'theTranslationIntoReferenceLanguage',    None)
        
                if not aNewSymbol:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_SolicitudCadena_missingParameter_Symbol_warning_msgid', "The new string symbol is missing. Can not create a new string request without a string symbol.-"), }
                    return anActionReport  

                if not aTranslationIntoMainLanguage:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_SolicitudCadena_missingParameter_TranslationIntoMainLanguage_warning_msgid', "The translation into the main language is missing. Can not create a new string request without a translation into the main language.-"), }
                    return anActionReport  
                

                unCatalogo = self.getCatalogo()
                unaCadenaPorSimbolo = unCatalogo.fGetCadenaPorSimbolo( aNewSymbol)
                if not ( unaCadenaPorSimbolo == None):
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_SolicitudCadena_NewStringSymbolAlreadyExists_warning_msgid', "The requested string symbol already exists in the translations catalog.-"), }
                    return anActionReport  

                
                unSolicitudCadenaCreationReport = None
                 
                someSolicitudesCadenas = self.fObtenerTodasSolicitudesCadenas()
                someSymbols = [ unaSolicitudCadena.getSimbolo() for unaSolicitudCadena in someSolicitudesCadenas]
                
                if ( aNewSymbol in someSymbols):
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_SolicitudCadena_NewStringSymbolAlreadyRequested_warning_msgid', "The new string symbol has already been recently requested for translation.-"), }
                    return anActionReport  

                someTitles  = [ unaSolicitudCadena.Title()      for unaSolicitudCadena in someSolicitudesCadenas]
                someIds     = [ unaSolicitudCadena.getId()      for unaSolicitudCadena in someSolicitudesCadenas]

                unMaxIdNumber = 0
                for unaId in someIds:
                    if unaId.startswith( cSolicitudCadenaIdPrefix):
                        unNumberString = unaId[ len( cSolicitudCadenaIdPrefix):]
                        if len( unNumberString) > 0:
                            unNumber = 0
                            try:
                                unNumber = int( unNumberString)
                            except ValueError:
                                None
                            
                            if unNumber > unMaxIdNumber:
                                unMaxIdNumber = unNumber
                
                aNewId   = '%s%d' % ( cSolicitudCadenaIdPrefix, unMaxIdNumber + 1, )
                unNewTitle   = aNewSymbol

                unCounter = 0 
                unBaseTitle = unNewTitle
                
                while ( unNewTitle in someTitles):
                    unCounter += 1
                    unNewTitle = '%s-%d' % ( unBaseTitle, unCounter, )
 
                    
                unMemberId = self.fGetMemberId()

                anAttrsDict = { 
                    'title':                            unNewTitle,
                    'description':                      '',
                    'simbolo':                          aNewSymbol,
                    'usuarioCreador':                   unMemberId,
                    'fechaCreacionTextual':             self.fDateTimeNowTextual(),
                    'codigoIdiomaPrincipal':            aMainlanguage,
                    'cadenaTraducidaAIdiomaPrincipal':  aTranslationIntoMainLanguage,
                    'codigoIdiomaReferencia':           aReferenceLanguage,
                    'cadenaTraducidaAIdiomaReferencia': aTranslationIntoReferenceLanguage,
                }
                
                unaIdNuevaSolicitudCadena = self.invokeFactory( cNombreTipoTRASolicitudCadena, aNewId, **anAttrsDict)
                if not unaIdNuevaSolicitudCadena:
                    anActionReport = { 'effect': 'error', 'failure': '%s' %   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_SolicitudCadena_errorencreacion', "No se ha podido crear Contenido de Intercambio."), }
                    return anActionReport     
                                
                unaNuevaSolicitudCadena = self.getElementoPorID( unaIdNuevaSolicitudCadena)
                if not unaNuevaSolicitudCadena:
                    anActionReport = { 'effect': 'error', 'failure': '%s' %  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_SolicitudCadena_errorencreacion', "No se ha podido crear Contenido de Intercambio."), }
                    return anActionReport     

                 
                unTimeProfilingResults = { }
                unResultadoNuevaSolicitudCadena = aModelDDvlPlone_tool.fRetrieveTypeConfig( 
                    theTimeProfilingResults     =unTimeProfilingResults,
                    theElement                  =unaNuevaSolicitudCadena, 
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
                if not unResultadoNuevaSolicitudCadena:
                    anActionReport = { 'effect': 'error', 'failure': 'retrieval_failure', }
                    return anActionReport     
 
                unSolicitudCadenaCreationReport = { 'effect': 'created', 'new_object_result': unResultadoNuevaSolicitudCadena, }
                        
                return unSolicitudCadenaCreationReport
                
 
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fCrearSolicitudCadena\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                                         
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                anActionReport = { 'effect': 'error', 'failure': '%s\n%s' % (   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_SolicitudCadena_exceptionDuringCreation', "Exception while creating new string request.-"), unInformeExcepcion, ) }
                return anActionReport     
              
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

        
                
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            

    
    security.declarePrivate( 'fCrearCadenas')    
    def fCrearCadenas( self,
        theTimeProfilingResults =None, # invoked from ModelDDvlPloneTool still using previous style of time profiling, thus the parameter is not theParentExecutionRecord =None, 
        theModelDDvlPloneTool_Mutators   =None, 
        theNewTypeName          ='', 
        theNewOneTitle          ='', 
        theNewOneDescription    ='', 
        theAdditionalParams     =None,
        thePermissionsCache     =None,
        theRolesCache           =None,
        theParentExecutionRecord=None):
        """Create new instances of TRACadena through an import process. Ceate an instance of TRAImportacion with a TRAContenidoIntercambio that will create the language when the import is executed.
        
        """
    
        unExecutionRecord = self.fStartExecution( 'method',  'fCrearCadenas', None, True, { 'log_what': 'details', 'log_when': True, }) # invoked from ModelDDvlPloneTool still using previous style of time profiling, thus the parameter is not theParentExecutionRecord =None, 

        try:
            unasDescripcionesContenidosCreados = []
            try:
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_CreateTRACadena, 
                    theElementsBindings     = { cBoundObject: self,}, 
                    theRulesToCollect       = None, 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord,
                )
              
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_no_permission_ToCreateStrings_msgid', "User does not have permission to create new strings (as an import process built from new string requests).-"), }
                    return anActionReport  
                            
                aModelDDvlPlone_tool = ModelDDvlPloneTool()
                             
                
                someSolicitudesCadenasPendientes = self.fObtenerSolicitudesCadenasPendientes()
                if not someSolicitudesCadenasPendientes:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_warningCreating_Strings_NoPendingNewStringRequests_msgid', "There are no Pending requests to create new strings. No Import process created.-"), }
                    return anActionReport  
               
 
                unCatalogo = self.getCatalogo()
                
                if not unCatalogo:
                    anActionReport = { 'effect': 'error', 'failure':  'InternalError: gvSIGi18n_errorCreating_Idioma_Missing_TRACatalogo_error_msgid', }
                    return anActionReport  
                
                
                someSolicitudesCadenasACrear = [ ]
                someLanguagesEnCadenasACrear = set()
                
                for unaSolicitudCadenaPendiente in someSolicitudesCadenasPendientes:
                    unSimboloCadena = unaSolicitudCadenaPendiente.getSimbolo()
                    if unSimboloCadena:
                        unCodigoIdiomaPrincipal = unaSolicitudCadenaPendiente.getCodigoIdiomaPrincipal()
                        if unCodigoIdiomaPrincipal:
                            unaCadenaTraducidaAIdiomaPrincipal = unaSolicitudCadenaPendiente.getCadenaTraducidaAIdiomaPrincipal()
                            if unaCadenaTraducidaAIdiomaPrincipal and unaCadenaTraducidaAIdiomaPrincipal.strip():
                                unaCadenaPorSimbolo = unCatalogo.fGetCadenaPorSimbolo( unSimboloCadena)
                                if unaCadenaPorSimbolo == None:
                                    someSolicitudesCadenasACrear.append( unaSolicitudCadenaPendiente)
                                    someLanguagesEnCadenasACrear.add( unCodigoIdiomaPrincipal)
                                
                                    unCodigoIdiomaReferencia = unaSolicitudCadenaPendiente.getCodigoIdiomaReferencia()
                                    if unCodigoIdiomaReferencia:
                                        unaCadenaTraducidaAIdiomaReferencia = unaSolicitudCadenaPendiente.getCadenaTraducidaAIdiomaReferencia()
                                        if unaCadenaTraducidaAIdiomaReferencia:
                                            someLanguagesEnCadenasACrear.add( unCodigoIdiomaReferencia)
                    
                            
                            
                            
                unaColeccionImportaciones = unCatalogo.fObtenerColeccionImportaciones()
                if not unaColeccionImportaciones:
                    anActionReport = { 'effect': 'error', 'failure':  'InternalError: gvSIGi18n_errorCreating_Idioma_Missing_TRAColeccionImportaciones_error_msgid', }
                    return anActionReport  
                
                     
                unMemberId = self.fGetMemberId()
                unaFechaYHora = self.fDateTimeNowTextual()

                aPloneUtilsTool = self.getPloneUtilsToolForNormalizeString()  
               
                unTitleImportacion = '%s %s %s' % ( self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_crearCadeas_Importacion_prefix', "To Create Strings"), unMemberId, unaFechaYHora, )
                aNewIdImportacion = unTitleImportacion.lower().replace( ' ', '-')
                if aPloneUtilsTool:
                    aNewIdImportacion = aPloneUtilsTool.normalizeString( aNewIdImportacion)
 
                anAttrsDictImportacion = { 
                    'title':         unTitleImportacion,
                    'description':   '',
                }
                
                unaIdNuevaImportacion = unaColeccionImportaciones.invokeFactory( cNombreTipoTRAImportacion, aNewIdImportacion, **anAttrsDictImportacion)
                if not unaIdNuevaImportacion:
                    anActionReport = { 'effect': 'error', 'failure': '%s' %   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Strings_TRAImportacion_NotCreated_msgid', "Error creating strings: import not created.-"), }
                    return anActionReport     
                                
                unaNuevaImportacion = unaColeccionImportaciones.getElementoPorID( unaIdNuevaImportacion)
                if not unaNuevaImportacion:
                    anActionReport = { 'effect': 'error', 'failure': '%s' %  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Strings_TRAImportacion_Created_TRAImportacion_NotFound_msgid', "Could not find import just created-."), }
                    return anActionReport     

                unTitleContenidoIntercambio = '%s' % ( self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_crearStrings_Importacion_prefix', "To Create Strings"), )
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
                
                
                someStringsAndTranslations = { }
                
                for unaSolicitudCadena in someSolicitudesCadenasACrear:
                    unSimboloCadena                     = unaSolicitudCadena.getSimbolo()
                    unCodigoIdiomaPrincipal             = unaSolicitudCadena.getCodigoIdiomaPrincipal()
                    unaCadenaTraducidaAIdiomaPrincipal  = unaSolicitudCadena.getCadenaTraducidaAIdiomaPrincipal().strip()
                    unCodigoIdiomaReferencia            = unaSolicitudCadena.getCodigoIdiomaReferencia()
                    unaCadenaTraducidaAIdiomaReferencia = unaSolicitudCadenaPendiente.getCadenaTraducidaAIdiomaReferencia()
                    if unaCadenaTraducidaAIdiomaReferencia:
                        unaCadenaTraducidaAIdiomaReferencia = unaCadenaTraducidaAIdiomaReferencia.strip()
                    
                    unasTraduccionesCadena = { }
                    someStringsAndTranslations[ unSimboloCadena] = unasTraduccionesCadena
                    
                    unasTraduccionesCadena[ unCodigoIdiomaPrincipal] = unaCadenaTraducidaAIdiomaPrincipal 
                    if unCodigoIdiomaReferencia and unaCadenaTraducidaAIdiomaReferencia:
                        unasTraduccionesCadena[ unCodigoIdiomaReferencia] = unaCadenaTraducidaAIdiomaReferencia 
                    
                
                unContenidoConCadenas = { 'strings_and_translations': someStringsAndTranslations, }
                unNuevoContenidoIntercambio.pSetContenido( unContenidoConCadenas)
                
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
 
                unStringsCreationReport = { 'effect': 'created', 'new_object_result': unResultadoNuevaImportacion, }
                        
                return unStringsCreationReport
                
 
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fCrearCadenas\n' 
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

                    
                
                    
            
            
            
            
            

            
            

    
    security.declarePrivate( 'fLimpiarCadenas')    
    def fLimpiarCadenas( self,
        theTimeProfilingResults =None, # invoked from ModelDDvlPloneTool still using previous style of time profiling, thus the parameter is not theParentExecutionRecord =None, 
        theModelDDvlPloneTool_Mutators   =None, 
        theNewTypeName          ='', 
        theNewOneTitle          ='', 
        theNewOneDescription    ='', 
        theAdditionalParams     =None,
        thePermissionsCache     =None,
        theRolesCache           =None,
        theParentExecutionRecord=None):
        """Delete instances of TRASolicitudCadena not in Pending status, or for which there exist an instance of TRACadena with same string symbol.
        
        """
    
        unExecutionRecord = self.fStartExecution( 'method',  'fLimpiarCadenas', None, True, { 'log_what': 'details', 'log_when': True, }) # invoked from ModelDDvlPloneTool still using previous style of time profiling, thus the parameter is not theParentExecutionRecord =None, 

        try:
            unasDescripcionesContenidosCreados = []
            try:
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_CleanupTRAColeccionSolicitudesCadenas, 
                    theElementsBindings     = { cBoundObject: self,}, 
                    theRulesToCollect       = None, 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord,
                )
              
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_no_permission_ToCleanUpnewStringRequests_msgid', "User does not have permission to clean up new string requests.-"), }
                    return anActionReport  
                            
                aModelDDvlPlone_tool = ModelDDvlPloneTool()
                             
                
                someSolicitudesCadenas = self.fObtenerTodasSolicitudesCadenas()
                if not someSolicitudesCadenas:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_warningCleaningUpNewStringRequests_NoNewStringRequestsToCleanUp_msgid', "There are no Pending requests to create new strings. No Import process created.-"), }
                    return anActionReport  
               
 
                unCatalogo = self.getCatalogo()
                
                if not unCatalogo:
                    anActionReport = { 'effect': 'error', 'failure':  'InternalError: gvSIGi18n_errorCreating_Idioma_Missing_TRACatalogo_error_msgid', }
                    return anActionReport  
                
                
                someSolicitudesCadenasAEliminar = [ ]
                
                for unaSolicitudCadena in someSolicitudesCadenas:
                    unEstadoSolicitudCadena = unaSolicitudCadena.getEstadoSolicitudCadena() 
                    if unEstadoSolicitudCadena and not ( unEstadoSolicitudCadena == cEstadoSolicitudCadena_Pending):
                        someSolicitudesCadenasAEliminar.append( unaSolicitudCadena)
                    else:
                        unSimboloCadena = unaSolicitudCadena.getSimbolo()
                        if not unSimboloCadena:
                            someSolicitudesCadenasAEliminar.append( unaSolicitudCadena)
                        else:
                            unCodigoIdiomaPrincipal = unaSolicitudCadena.getCodigoIdiomaPrincipal()
                            if not unCodigoIdiomaPrincipal:
                                someSolicitudesCadenasAEliminar.append( unaSolicitudCadena)
                            else:
                                unaCadenaTraducidaAIdiomaPrincipal = unaSolicitudCadena.getCadenaTraducidaAIdiomaPrincipal()
                                if not( unaCadenaTraducidaAIdiomaPrincipal and unaCadenaTraducidaAIdiomaPrincipal.strip()):
                                    someSolicitudesCadenasAEliminar.append( unaSolicitudCadena)
                                else:    
                                    unaCadenaPorSimbolo = unCatalogo.fGetCadenaPorSimbolo( unSimboloCadena)
                                    if not( unaCadenaPorSimbolo == None):
                                        someSolicitudesCadenasAEliminar.append( unaSolicitudCadena)
                    

                unasIdsSolicitudesCadenasAEliminar = []
                
                for unaSolicitudCadena in someSolicitudesCadenasAEliminar:
                    unaIdSolicitudCadena = unaSolicitudCadena.getId()
                    if unaIdSolicitudCadena:
                        unasIdsSolicitudesCadenasAEliminar.append( unaIdSolicitudCadena)
                    
                    
                if unasIdsSolicitudesCadenasAEliminar: 
                    self.manage_delObjects( unasIdsSolicitudesCadenasAEliminar)
                
 
                unStringsRequestDeletionReport = { 'effect': 'deleted', 'ids': unasIdsSolicitudesCadenasAEliminar, }
                        
                return unStringsRequestDeletionReport
                
 
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fLimpiarCadenas\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                                         
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                anActionReport = { 'effect': 'error', 'failure': '%s\n%s' % (   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCleaningUpSolicitudesCadenas_Exception_msgid', "Exception while cleaning up new string requests.-"), unInformeExcepcion, ) }
                return anActionReport     
              
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

                                

# end of class TRAColeccionSolicitudesCadenas_Operaciones

##code-section module-footer #fill in your manual code here
##/code-section module-footer



