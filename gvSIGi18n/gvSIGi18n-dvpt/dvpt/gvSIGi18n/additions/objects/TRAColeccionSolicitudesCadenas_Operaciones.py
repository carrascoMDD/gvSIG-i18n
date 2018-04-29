# -*- coding: utf-8 -*-
#
# File: TRAColeccionSolicitudesCadenas_Operaciones.py
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

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.gvSIGi18n.config import *

##code-section module-header #fill in your manual code here

import sys
import traceback
import logging

from Products.CMFCore       import permissions
from Products.CMFCore.utils  import getToolByName



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

from TRAImportarExportar_Constants import cScannedKeys_String_Symbol, cScannedKeys_String_Modules, cScannedKeys_Translation_Translation, cScannedKeys_String_Translations

from TRAElemento_Permission_Definitions import cBoundObject
from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_CreateTRASolicitudCadena, cUseCase_CreateTRACadena, cUseCase_CleanupTRAColeccionSolicitudesCadenas






##/code-section module-header



##code-section after-local-schema #fill in your manual code here



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
    
    
    
    
    
    
    
    security.declareProtected( permissions.View, 'fNewStringSymbolAcceptedReport')    
    def fNewStringSymbolAcceptedReport( self, theNewStringSymbol):
        
        if not theNewStringSymbol:
            return [ False, self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_Warning_NewStringSymbol_Empty', 'Can not be Empty',),]
        
        aNewStringSymbol = theNewStringSymbol.strip()
        if not aNewStringSymbol:
            return [ False, self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_Warning_NewStringSymbol_Empty', 'Can not be Empty',),]
        
        aNewStringSymbolLines = aNewStringSymbol.splitlines()
        if not aNewStringSymbolLines:
            return [ False, self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_Warning_NewStringSymbol_Empty', 'Can not be Empty',),]
         
        aNewStringSymbol = aNewStringSymbolLines[0]
        if not aNewStringSymbol:
            return [ False, self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_Warning_NewStringSymbol_Empty', 'Can not be Empty',),]
         
        if not ( aNewStringSymbol == aNewStringSymbol.replace( ' ', '').replace( '\t', '')):
            return [ False, self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_Warning_NewStringSymbol_BlanksNotAllowed', 'Blanks not allowed',),]
                 
        for aChar in aNewStringSymbol:
            if not ( aChar.isalnum() or ( aChar in cNewStringSymbol_AcceptableNonAlphanumericChars)):
                return [ False, '%s %s' % ( 
                    self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_Warning_NewStringSymbol_OnlyAlphanumerocCharsAnd', 'Only allowed alphanumeric chars and',),
                    '  '.join( [ '"%s"' % aC for aC in cNewStringSymbol_AcceptableNonAlphanumericChars]),
                )]
                
        return [ True, '',]       
                
        
        
        
        
        
    security.declarePrivate( 'pAllSubElements_into')    
    def pAllSubElements_into( self, theCollection, theAdditionalParams=None):
        if theCollection == None:
            return self
        theCollection.append( self)
        
        
        unosElementos = self.fObtenerTodasSolicitudesCadenas()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pAllSubElements_into( theCollection, theAdditionalParams=theAdditionalParams)
        
        return self
        


    


    security.declarePrivate( 'pForAllElementsDo_recursive')    
    def pForAllElementsDo_recursive( self, theLambda=None, thePloneLambda=None,):
        if not theLambda:
            return self
        
        theLambda( self)

        unosElementos = self.fObtenerTodasSolicitudesCadenas()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda, thePloneLambda)
                
        if thePloneLambda:
            self.pForAllElementsPloneDo( thePloneLambda)
        
        return self
        


                                
                
    security.declareProtected( permissions.View, 'fObtenerTodasSolicitudesCadenas')
    def fObtenerTodasSolicitudesCadenas( self, ):
        """Retrieve all contained elements of type TRASolicitudCadena.
        
        """
        someSolicitudesCadenas = self.fObjectValues( cNombreTipoTRASolicitudCadena) 
        return someSolicitudesCadenas
         
      
    
    

                
    security.declareProtected( permissions.View, 'fObtenerSolicitudesCadenasPendientes')
    def fObtenerSolicitudesCadenasPendientes( self, ):
        """Retrieve all contained elements of type TRASolicitudCadena, which are in pending status.
        
        """
        someSolicitudesCadenas = self.fObtenerTodasSolicitudesCadenas()
        
        somePendingSolicitudesCadenas = []
        
        for unaSolicitudCadena in someSolicitudesCadenas:
            unEstadoSolicitudCadena = unaSolicitudCadena.getEstadoSolicitudCadena() 
            if unEstadoSolicitudCadena == cEstadoSolicitudCadena_Pending:
                somePendingSolicitudesCadenas.append( unaSolicitudCadena)
                
        return somePendingSolicitudesCadenas
         
      
    
    

                
    security.declareProtected( permissions.View, 'fHaySolicitudesCadenasPendientes')
    def fHaySolicitudesCadenasPendientes( self, ):
        """Return True if there exist any contained elements of type TRASolicitudCadena, which are in pending status.
        
        """
        someSolicitudesCadenas = self.fObtenerTodasSolicitudesCadenas()
        
        
        for unaSolicitudCadena in someSolicitudesCadenas:
            unEstadoSolicitudCadena = unaSolicitudCadena.getEstadoSolicitudCadena() 
            if unEstadoSolicitudCadena == cEstadoSolicitudCadena_Pending:
                return True
                
        return False
         

    
    

                
    security.declareProtected( permissions.View, 'fHaySolicitudesCadenasYaProcesadas')
    def fHaySolicitudesCadenasYaProcesadas( self, ):
        """Return True if there exist any contained elements of type TRASolicitudCadena, which have already been processed: the ones which are NOT in pending status.
        
        """
        someSolicitudesCadenas = self.fObtenerTodasSolicitudesCadenas()
        
        
        for unaSolicitudCadena in someSolicitudesCadenas:
            unEstadoSolicitudCadena = unaSolicitudCadena.getEstadoSolicitudCadena() 
            if unEstadoSolicitudCadena == cEstadoSolicitudCadena_Created:
                return True
                
        return False
    
    


    
    security.declarePrivate( 'fCrearSolicitudCadena')    
    def fCrearSolicitudCadena( self,
        theTimeProfilingResults =None, 
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
    
        unExecutionRecord = self.fStartExecution( 'method',  'fCrearSolicitudCadena', None, True, { 'log_what': 'details', 'log_when': True, }) 

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators import cModificationKind_CreateSubElement, cModificationKind_Create
       
        try:
            unasDescripcionesContenidosCreados = []
            try:
                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)
                
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
                            
                aModelDDvlPlone_tool = self.fModelDDvlPloneTool()
                             
                
                unNewTypeName = theNewTypeName
                if not unNewTypeName:
                    unNewTypeName = cNombreTipoTRASolicitudCadena
                
                aNewSymbol                          = theAdditionalParams.get( 'theNewSymbol', None)
                aMainlanguage                       = theAdditionalParams.get( 'theMainLanguage',    None)
                aTranslationIntoMainLanguage        = theAdditionalParams.get( 'theTranslationIntoMainLanguage',    None)
                aReferenceLanguage                  = theAdditionalParams.get( 'theReferenceLanguage',    None)
                aTranslationIntoReferenceLanguage   = theAdditionalParams.get( 'theTranslationIntoReferenceLanguage',    None)
                someModuleNames                     = theAdditionalParams.get( 'theModuleNames',    None)
                
                aModuleNamesString = ''
                if isinstance( someModuleNames, list):
                    aModuleNamesString = cTRAModuleNameSeparator.join( someModuleNames)
                else:
                    aModuleNamesString = someModuleNames
                    
        
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

                unaFechaCreacion =self. fDateTimeNow()
                anAttrsDict = { 
                    'title':                            unNewTitle,
                    'description':                      '',
                    'simbolo':                          aNewSymbol,
                    'usuarioCreador':                   unMemberId,
                    'fechaCreacion':                    unaFechaCreacion,
                    'codigoIdiomaPrincipal':            aMainlanguage,
                    'cadenaTraducidaAIdiomaPrincipal':  aTranslationIntoMainLanguage,
                    'codigoIdiomaReferencia':           aReferenceLanguage,
                    'cadenaTraducidaAIdiomaReferencia': aTranslationIntoReferenceLanguage,
                    'nombresModulos':                   aModuleNamesString,
                }
                
                self.pFlushCachedTemplates_All()  
                self.getCatalogo().pFlushCachedTemplates_All()      
                for aSolicitudCadena in someSolicitudesCadenas:
                    aSolicitudCadena.pFlushCachedTemplates_All()
                
                
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
                        
                
            
                aModelDDvlPloneTool_Mutators = self.fModelDDvlPloneTool().fModelDDvlPloneTool_Mutators( self)
                    
                aCreateElementReport = aModelDDvlPloneTool_Mutators.fNewVoidCreateElementReport()
                aCreateElementReport.update( { 'effect': 'created', 'new_object_result': unResultadoNuevaSolicitudCadena, })
                
                someFieldReports    = aCreateElementReport[ 'field_reports']
                aFieldReportsByName = aCreateElementReport[ 'field_reports_by_name']
                
                aReportForField = { 'attribute_name': 'id',                              'effect': 'changed', 'new_value': unaIdNuevaSolicitudCadena, 'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                
                aReportForField = { 'attribute_name': 'title',                           'effect': 'changed', 'new_value': unNewTitle,           'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                
                
                aReportForField = { 'attribute_name': 'simbolo',                         'effect': 'changed', 'new_value': aNewSymbol,           'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                
                aReportForField = { 'attribute_name': 'usuarioCreador',                  'effect': 'changed', 'new_value': unMemberId,           'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                
                aReportForField = { 'attribute_name': 'fechaCreacion',                   'effect': 'changed', 'new_value': unaFechaCreacion,           'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                
                aReportForField = { 'attribute_name': 'codigoIdiomaPrincipal',           'effect': 'changed', 'new_value': aMainlanguage,           'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                
                aReportForField = { 'attribute_name': 'cadenaTraducidaAIdiomaPrincipal', 'effect': 'changed', 'new_value': aTranslationIntoMainLanguage,           'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                
                aReportForField = { 'attribute_name': 'codigoIdiomaReferencia',          'effect': 'changed', 'new_value': aReferenceLanguage,           'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                
                aReportForField = { 'attribute_name': 'cadenaTraducidaAIdiomaReferencia','effect': 'changed', 'new_value': aTranslationIntoReferenceLanguage,           'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                                   
                aModelDDvlPloneTool_Mutators.pSetAudit_Creation( self,                    cModificationKind_CreateSubElement, aCreateElementReport, theUseCounter=True)       
                aModelDDvlPloneTool_Mutators.pSetAudit_Creation( unaNuevaSolicitudCadena, cModificationKind_Create,           aCreateElementReport)       
                
                return unSolicitudCadenaCreationReport
                
 
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fCrearSolicitudCadena\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   
                                         
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                anActionReport = { 'effect': 'error', 'failure': '%s\n%s' % (   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_SolicitudCadena_exceptionDuringCreation', "Exception while creating new string request.-"), unInformeExcepcion, ) }
                return anActionReport     
              
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

        
                
            
            
            
            
            
            
            
            

    
    security.declarePrivate( 'fCrearImportarYLimpiarCadenas')    
    def fCrearImportarYLimpiarCadenas( self,
        thePermissionsCache     =None,
        theRolesCache           =None,
        theParentExecutionRecord=None):
        """Create new instances of TRACadena by executing an import process, then clean up the string requests. Ceate an instance of TRAImportacion with a TRAContenidoIntercambio that will create the language when the import is executed.
        
        """
    
        unExecutionRecord = self.fStartExecution( 'method',  'fCrearImportarYLimpiarCadenas', None, True, { 'log_what': 'details', 'log_when': True, }) 

        try:
             
            try:
                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)
                            
                aCreateImportReport = self.fCrearCadenas( unPermissionsCache, unRolesCache, unExecutionRecord,)
                if not aCreateImportReport.get( 'effect', '') == 'created':
                    aResult = { 
                        'effect': 'error', 
                        'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreatingImportProcessToCreateStrings', "Error creating import process to create strings-") + aCreateImportReport.get( 'failure', ''),
                    }
                    return aResult
                
                unNewObjectResult = aCreateImportReport.get( 'new_object_result', {})
                if not unNewObjectResult:
                    aResult = { 
                        'effect': 'error', 
                        'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorImportProcessToCreateStringsNotCreated', "Import process to create strings hast not been created-"),
                    }
                    return aResult
                    
                anImportElement = unNewObjectResult.get( 'object', None)
                if ( anImportElement == None):
                    aResult = { 
                        'effect': 'error', 
                        'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorImportProcessElementNotCreated', "Import process has not been created-"),
                    }
                    return aResult
                
                
                someSolicitudesCadenasUIDsPorSimbolo = aCreateImportReport.get( 'string_creation_request_UIDs_by_string_symbol', {})
                
                
                aProgressHandlerCreationResult = anImportElement.fCreateProgressHandlerFor_Import( 
                    theAdditionalParams      = { 'theIsToCreateCadenas': True, 'theSolicitudesCadenasUIDsPorSimbolo': someSolicitudesCadenasUIDsPorSimbolo,},  
                    thePermissionsCache     =unPermissionsCache, 
                    theRolesCache           =unRolesCache, 
                    theParentExecutionRecord=unExecutionRecord)
                if ( not aProgressHandlerCreationResult) or not aProgressHandlerCreationResult.get( 'success', False):
                    aResult = { 
                        'effect': 'error', 
                        'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorImportProgressHandlerNotCreated', "Import Progress Handler has not been created-"),
                    }
                    return aResult
                
                
                
                aProgressHandler = aProgressHandlerCreationResult.get( 'progress_handler', None)
                if not aProgressHandler:
                    aResult = { 
                        'effect': 'error', 
                        'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorImportProgressHandlerNotFound', "Import Progress Handler has not been found-"),
                    }
                    return aResult

                
                aProgressElement = aProgressHandlerCreationResult.get( 'progress_element', None)
                if ( aProgressElement == None):
                    aResult = { 
                        'effect': 'error', 
                        'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorProgressElementNotKnownByImportProcessElement', "Progress element is not known by import process element-"),
                    }
                    return aResult
                
                
                
                
                aProgressElement.fProcessControl( 
                    theProcessControlAction     =cTRAProcessControl_Action_Execute,
                    theAdditionalParams          =None,
                    thePermissionsCache         =unPermissionsCache, 
                    theRolesCache               =unRolesCache, 
                    theParentExecutionRecord    =unExecutionRecord,
                )
                
                    
                aProgressResult = aProgressHandler.vResult
                if not aProgressResult:
                    aResult = { 
                        'effect': 'error', 
                        'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorImportProgressNoResult', "Import Progress Result is  missing-"),
                    }
                    return aResult
                
                anImportExecutionReport = aProgressResult.get( 'import_contents_report', {})
                if not anImportExecutionReport:
                    aResult = { 
                        'effect': 'error', 
                        'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorImportContentsReportMissing', "Import Contents Report is  missing-"),
                    }
                    return aResult
                
                                
                anImportError       = anImportExecutionReport.get( 'error', '')
                anImportErrorDetail = anImportExecutionReport.get( 'error_detail', '')
                if anImportError:
                    aResult = { 
                        'effect': 'error', 
                        'failure':  '%s %s %s ' % (
                            self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorImportProcessFailed', "Import process failed-"),
                            self.fTranslateI18N( 'gvSIGi18n', anImportError, anImportError),
                            anImportErrorDetail,
                        ),
                    }
                    return aResult
                    
 
                
                
                aCleanUpStringsReport = self.fLimpiarCadenas( unPermissionsCache, unRolesCache, unExecutionRecord,)
                # TRADeveloper role can not clean up strings, as we want them to stay in the list for a coordinator to know.
                #if not aCleanUpStringsReport.get( 'effect', '') == 'deleted':
                    #aResult = { 
                        #'effect': 'error', 
                        #'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCleaningUpStringsRequests', "Error cleaning up strings requests-") + aCleanUpStringsReport.get( 'failure', ''),
                    #}
                    #return aResult
                
                aResult = { 
                    'effect': 'created',
                    'new_object_result': unNewObjectResult,
                    'progress_element':  aProgressElement,
                }
                
                return aResult
                
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fCrearImportarYLimpiarCadenas\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   
                                         
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                anActionReport = { 'effect': 'error', 'failure': '%s\n%s' % (   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Cadeas_Exception_msgid', "Exception while creating Strings (as import process).-"), unInformeExcepcion, ) }
                return anActionReport     
              
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

                    
                
                              
            
            
            
            

    
    security.declarePrivate( 'fCrearCadenas')    
    def fCrearCadenas( self,
        thePermissionsCache     =None,
        theRolesCache           =None,
        theParentExecutionRecord=None):
        """Create new instances of TRACadena through an import process. Ceate an instance of TRAImportacion with a TRAContenidoIntercambio that will create the language when the import is executed.
        
        """
    
        unExecutionRecord = self.fStartExecution( 'method',  'fCrearCadenas', None, False, { 'log_what': 'details', 'log_when': True, }) 

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators import cModificationKind_CreateSubElement, cModificationKind_Create

        try:
            unasDescripcionesContenidosCreados = []
            try:
                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)
                
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
                            
                aModelDDvlPlone_tool = self.fModelDDvlPloneTool()
                             
                
                someSolicitudesCadenasPendientes = self.fObtenerSolicitudesCadenasPendientes()
                if not someSolicitudesCadenasPendientes:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_warningCreating_Strings_NoPendingNewStringRequests_msgid', "There are no Pending requests to create new strings. No Import process created.-"), }
                    return anActionReport  
               
 
                unCatalogo = self.getCatalogo()
                
                if unCatalogo == None:
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
                    
                            
                if not someSolicitudesCadenasACrear:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_warningCreating_Strings_NoStringRequestsToCreate_msgid', "There are no New String requests to create. No Import process created.-"), }
                    return anActionReport  
                            
                                            
                            
                someSolicitudesCadenasUIDsPorSimbolo = { }
                for aSolicitudCadenaACrear in someSolicitudesCadenasACrear:
                    unSimboloCadena           = aSolicitudCadenaACrear.getSimbolo()
                    aSolicitudCadenaACrearUID = aSolicitudCadenaACrear.UID()
                    someSolicitudesCadenasUIDsPorSimbolo[ unSimboloCadena] = aSolicitudCadenaACrearUID
                    
                            
                unaColeccionImportaciones = unCatalogo.fObtenerColeccionImportaciones()
                if not unaColeccionImportaciones:
                    anActionReport = { 'effect': 'error', 'failure':  'InternalError: gvSIGi18n_errorCreating_Idioma_Missing_TRAColeccionImportaciones_error_msgid', }
                    return anActionReport  
                
                     
                unMemberId = self.fGetMemberId()
                unaFechaYHora =self.fDateTimeNowTextual()

                aPloneUtilsTool = self.getPloneUtilsToolForNormalizeString()  
               
                unTitleImportacion = '%s by %s on %s' % ( self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_crearCadeas_Importacion_prefix', "To Create Strings"), unMemberId, unaFechaYHora, )
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
                    anActionReport = { 'effect': 'error', 'failure': '%s' %   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Strings_TRAImportacion_NotCreated_msgid', "Error creating strings: import not created.-"), }
                    return anActionReport     
                                
                unaNuevaImportacion = unaColeccionImportaciones.getElementoPorID( unaIdNuevaImportacion)
                if not unaNuevaImportacion:
                    anActionReport = { 'effect': 'error', 'failure': '%s' %  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Strings_TRAImportacion_Created_TRAImportacion_NotFound_msgid', "Could not find import just created-."), }
                    return anActionReport     

                
                unaNuevaImportacion.pFlushCachedTemplates_All()                            
      
                    
                        
                unTitleContenidoIntercambio = '%s' % self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_crearStrings_Importacion_prefix', "To Create Strings")
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
                
                
                
                aScannedData = self.fNewVoidScannedData()
                
                someScannedStrings   = aScannedData[ 'symbols']
                someScannedLanguages = aScannedData[ 'languages']
                someScannedModules   = aScannedData[ 'modules']
                                
                for aSolicitudCadenaACrear in someSolicitudesCadenasACrear:
                    
                    unSimboloCadena                     = aSolicitudCadenaACrear.getSimbolo()
                    unCodigoIdiomaPrincipal             = aSolicitudCadenaACrear.getCodigoIdiomaPrincipal()
                    unaCadenaTraducidaAIdiomaPrincipal  = aSolicitudCadenaACrear.getCadenaTraducidaAIdiomaPrincipal()
                    unCodigoIdiomaReferencia            = aSolicitudCadenaACrear.getCodigoIdiomaReferencia()
                    unaCadenaTraducidaAIdiomaReferencia = aSolicitudCadenaACrear.getCadenaTraducidaAIdiomaReferencia()
                    unosNombresModulosString            = aSolicitudCadenaACrear.getNombresModulos()
                    
                    
                    unosNombresModulos                  = self.fParseNombresModulosString( unosNombresModulosString)
                    unosIndexesNombresModulos = [ ]
                    for unNombreModulo in unosNombresModulos:
                        
                        if unNombreModulo in someScannedModules:
                            unosIndexesNombresModulos.append( someScannedModules.index( unNombreModulo))
                        
                        else:
                            unosIndexesNombresModulos.append( len( someScannedModules))
                            someScannedModules.append( unNombreModulo)
                            
                            
                    if not ( unCodigoIdiomaPrincipal in someScannedLanguages):
                        someScannedLanguages.append( unCodigoIdiomaPrincipal)                        
                    
                    if not ( unCodigoIdiomaReferencia in someScannedLanguages):
                        someScannedLanguages.append( unCodigoIdiomaReferencia)
                    
                    if unaCadenaTraducidaAIdiomaPrincipal:
                        unaCadenaTraducidaAIdiomaPrincipal  = unaCadenaTraducidaAIdiomaPrincipal.strip()
                    
                    if unaCadenaTraducidaAIdiomaReferencia:
                        unaCadenaTraducidaAIdiomaReferencia = unaCadenaTraducidaAIdiomaReferencia.strip()
                    
                        
                        
                        
                    aScannedString = self.fNewVoidScannedString()
                    
                    aScannedString[ cScannedKeys_String_Symbol]  = unSimboloCadena
                    aScannedString[ cScannedKeys_String_Modules] = unosIndexesNombresModulos
                    
                    someScannedStrings.append( aScannedString)
                              
                    if unaCadenaTraducidaAIdiomaPrincipal:
                        aScannedTranslation = self.fNewVoidScannedTranslation()
                        aScannedTranslation[ cScannedKeys_Translation_Translation] = unaCadenaTraducidaAIdiomaPrincipal                  
                        aScannedString[ cScannedKeys_String_Translations][ unCodigoIdiomaPrincipal] = aScannedTranslation
                    
                    if unaCadenaTraducidaAIdiomaReferencia:
                        aScannedTranslation = self.fNewVoidScannedTranslation()
                        aScannedTranslation[ cScannedKeys_Translation_Translation] = unaCadenaTraducidaAIdiomaReferencia                  
                        aScannedString[ cScannedKeys_String_Translations][ unCodigoIdiomaReferencia] = aScannedTranslation
                        
                        

                unUploadedContent = self.fNewVoidUploadedContent()
                unUploadedContent[ 'content_data'] = aScannedData
                unNuevoContenidoIntercambio.pSetContenido( unUploadedContent)

                    
                    
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
 
                unStringsCreationReport = { 'effect': 'created', 'new_object_result': unResultadoNuevaImportacion, 
                    'string_creation_request_UIDs_by_string_symbol': someSolicitudesCadenasUIDsPorSimbolo
                }
                        
                
                
                unaColeccionImportaciones.pFlushCachedTemplates_All()                            
                unaNuevaImportacion.pFlushCachedTemplates_All()                            
                unNuevoContenidoIntercambio.pFlushCachedTemplates_All()                            
            
                aModelDDvlPloneTool_Mutators = self.fModelDDvlPloneTool().fModelDDvlPloneTool_Mutators( self)
                    
                aCreateElementReport = aModelDDvlPloneTool_Mutators.fNewVoidCreateElementReport()
                aCreateElementReport.update( { 'effect': 'created', 'new_object_result': unResultadoNuevaImportacion, })
                
                someFieldReports    = aCreateElementReport[ 'field_reports']
                aFieldReportsByName = aCreateElementReport[ 'field_reports_by_name']
                
                aReportForField = { 'attribute_name': 'id',     'effect': 'changed', 'new_value': unaIdNuevoContenidoIntercambio, 'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                
                aReportForField = { 'attribute_name': 'title',  'effect': 'changed', 'new_value': unTitleContenidoIntercambio,    'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                
                                   
                aModelDDvlPloneTool_Mutators.pSetAudit_Creation( unaColeccionImportaciones,  cModificationKind_CreateSubElement, aCreateElementReport, theUseCounter=True)       
                aModelDDvlPloneTool_Mutators.pSetAudit_Creation( unaNuevaImportacion,        cModificationKind_Create,           aCreateElementReport)       
                
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
                
                return unStringsCreationReport
                
 
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fCrearCadenas\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
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
        thePermissionsCache     =None,
        theRolesCache           =None,
        theParentExecutionRecord=None):
        """Delete instances of TRASolicitudCadena not in Pending status, or for which there exist an instance of TRACadena with same string symbol.
        
        """
    
        unExecutionRecord = self.fStartExecution( 'method',  'fLimpiarCadenas', None, True, { 'log_what': 'details', 'log_when': True, }) 

        try:
            unasDescripcionesContenidosCreados = []
            try:
                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)
                
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
                            
                aModelDDvlPlone_tool = self.fModelDDvlPloneTool()
                             
                
                someSolicitudesCadenas = self.fObtenerTodasSolicitudesCadenas()
                if not someSolicitudesCadenas:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_warningCleaningUpNewStringRequests_NoNewStringRequestsToCleanUp_msgid', "There are no Pending requests to create new strings. No Import process created.-"), }
                    return anActionReport  
               
 
                unCatalogo = self.getCatalogo()
                
                if unCatalogo == None:
                    anActionReport = { 'effect': 'error', 'failure':  'InternalError: gvSIGi18n_errorCreating_Idioma_Missing_TRACatalogo_error_msgid', }
                    return anActionReport  
                
                
                someSolicitudesCadenasAEliminar = [ ]
                
                for unaSolicitudCadena in someSolicitudesCadenas:
                    unEstadoSolicitudCadena = unaSolicitudCadena.getEstadoSolicitudCadena() 
                    
                    if unEstadoSolicitudCadena == cEstadoSolicitudCadena_Created:
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
                    
                    self.pFlushCachedTemplates_All()                            
                    
                    self.manage_delObjects( unasIdsSolicitudesCadenasAEliminar)
                
 
                unStringsRequestDeletionReport = { 'effect': 'deleted', 'ids': unasIdsSolicitudesCadenasAEliminar, }
                        
                return unStringsRequestDeletionReport
                
 
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fLimpiarCadenas\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
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



