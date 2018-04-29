# -*- coding: utf-8 -*-
#
# File: TRAImportacion_Operaciones.py
#
# Copyright (c) 2008, 2009 by Conselleria de Infraestructuras y Transporte de la
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



import sys
import traceback



import os
import logging

import time

import transaction

from math import floor

from DateTime import DateTime


from StringIO import StringIO

from zipfile import ZipFile


from Products.Archetypes.utils import shasattr

from Products.CMFCore.utils import getToolByName


from Products.CMFCore       import permissions

from Products.gvSIGi18n.TRATraduccion_Operaciones import cMarcaDeComentarioSinCambios

from Products.Archetypes.utils import getRelURL







from TRAElemento_Constants import *

from TRAImportarExportar_Constants import *

from TRAElemento_Permission_Definitions import cUseCase_CreateTRAContenidoIntercambio, cUseCase_DeleteTRAContenidoIntercambio
from TRAElemento_Permission_Definitions import cUseCase_ImportTRAImportacion, cUseCase_CreateMissingTRATraduccion, cUseCase_ReuseTRAImportacion
from TRAElemento_Permission_Definitions import cUseCase_ImportTRAImportacion_ToCreateCadenas, cBoundObject

from TRAElemento_Permission_Definitions import cPermissionsToDenyEverywhereToEverybody

from TRAElemento_Operaciones            import TRAElemento_Operaciones

from TRAElemento import TRAElemento


cLogEachExecution_fCombinedContenidosIntercambio = True



class TRAImportacion_Operaciones:
    """
    """
    security = ClassSecurityInfo()
     

    
        
    # ####################################
    #  Complete initialization after creation
    # ####################################
        
        
    
    security.declarePrivate('pHandle_manage_afterAdd')
    def pHandle_manage_afterAdd(self, theItem, theContainer):   
        
        TRAElemento.manage_afterAdd(  self, theItem, theContainer)
        
        # Check for Premature_initialization (may not not yet be hooked under TRACatalog instance)
        #if not self.Title(): # 'portal_factory' in self.getPhysicalPath(): 
            #return self
        
        self.pInitDefaultNombreModuloFromCatalog(  theItem, theContainer)
                
        return self
    
    
    
    security.declarePrivate('fDefaultNombreModuloFromCatalog')
    def fDefaultNombreModuloFromCatalog(self,):   
        unCatalog = None
        try:
            unCatalog = self.getCatalogo()
        except:
            None
        if not unCatalog:
            return None
        
        unNombreModuloPorDefecto = unCatalog.getNombreModuloPorDefecto()
        return unNombreModuloPorDefecto
    
         
    
    security.declarePrivate('pInitDefaultNombreModuloFromCatalog')
    def pInitDefaultNombreModuloFromCatalog(self, theItem, theContainer):   

        unNombreModuloPorDefecto = self.fDefaultNombreModuloFromCatalog()
        
        self.setNombreModuloPorDefecto( unNombreModuloPorDefecto)
        
        return self
    
    
    security.declarePrivate( 'pAllSubElements_into')    
    def pAllSubElements_into( self, theCollection, theAdditionalParms=None):
        if theCollection == None:
            return self
        theCollection.append( self)
        
        
        unosElementos = self.fObtenerTodosContenidosIntercambio()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pAllSubElements_into( theCollection, theAdditionalParms=theAdditionalParms)
        
        return self
           
    
    
    


    security.declarePrivate( 'pForAllElementsDo_recursive')    
    def pForAllElementsDo_recursive( self, theLambda):
        if not theLambda:
            return self
        
        theLambda( self)        
    
        unosElementos = self.fObtenerTodosContenidosIntercambio()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda)
        
        return self
           
    
        
    
    
    security.declarePrivate( 'fNewVoidUploadedEntry')    
    def fNewVoidUploadedEntry( self,):
        unUploadedEntry = {
            'in_zip':                                  False,
            'module':                                  '',
            'file_name':                               '',
            'file_kind':                               '',
            'is_reference':                            False,
            'language':                                '',
            'country':                                 '',
            'language_and_country':                    '',
            'charset':                                 '',
            'is_fallback_for':                         '',
            'domain':                                  '',
            'is_pot_file':                             False,
            'exceeded_max_number_of_lines':           False,
        }
        return unUploadedEntry
    
 

    
    
    
    security.declarePrivate( 'fNewVoidCombinedContent')    
    def fNewVoidCombinedContent( self,):
        unUploadedContent = {
            'languages':                              [],
            'modules':                                [],
            'strings_modules_and_translations':       {},
        }
        return unUploadedContent
    
                  


    
    security.declarePrivate( 'fNewVoidImportCursor')    
    def fNewVoidImportCursor( self,):
        unCursor = {
            'file_kind':                '',
            'language':                 '',
            'content_lines':            [],
            'num_lines':                0,
            'next_line_index':          0,
            'num_possible_records':     0,
            'timestamp':                '',
            'error':                    '',
            'error_detail':             '',
            'charset':                  '',
            'exceeded_max_number_of_lines': False,
        }
        return unCursor
    
    
    
    
    security.declarePrivate( 'fNewVoidCursorRecord')    
    def fNewVoidCursorRecord( self):
        unRecord = {
            'string_symbol':        '',
            'unicode_symbol':        '',
            'symbol_error':         '',
            'raw_translation':      '',
            'unicode_translation':  u'',
            'encoded_translation':  '',
            'translation_error':    '',
            'unicode_default':      '',
            'encoded_default':      '',
            'default_error':        '',
            'sources':              '',
            'flags':                '',
            'comment':              '',
        }
        return unRecord
    
    security.declarePrivate( 'fNewVoidInformeImportarContenidos')    
    def fNewVoidInformeImportarContenidos( self):
        unInforme = {
            'valid':                    True,
            'start_date':               '',
            'end_date':                 '',
            'fecha_informe':            '',
            'modules_to_create':        0,
            'module_creations':         0,
            'languages_to_create':      0,
            'language_creations':       0,
            'strings_to_process':       0,
            'processed_strings':        0,
            'translations_to_process':  0,
            'processed_translations':   0,
            'strings_to_create':        0,
            'string_creations':         0,
            'string_module_changes':    0,
            'translation_creations':    0,
            'translation_creations_as_pending':    0,
            'translation_changes':      0,
            'translations_unchanged':   0,
            'translations_ignored':     0,
            'strings_to_complete':      0,
            'strings_completed':        0,
            'translations_completed':   0,
            'total_changes':            0,
            'expected_operations':      0,
            'operations_done':          0,
            'error':                    '',
            'error_detail':             '',
            'translations_to_create_in_new_languages_for_preexisting_strings': 0,
            'translations_created_in_new_languages_for_preexisting_strings': 0,
            'missing_translations_creation':    self.fNewVoidInformeCrearTraduccionesQueFaltan(),
        }
        return unInforme

    
    

    
    
    security.declarePrivate( 'fVoidPOHeader')    
    def fVoidPOHeader( self):
        unPOHeader = {
            'language_code':             '',
            'language_name':             '',
            'country':                   '',
            'language_and_country':      '',
            'charset':                   '',
            'is_fallback_for':           '',
            'domain':                    '',
            'last_line_number':          -1,
        }
        return unPOHeader
        
         
    
  
    
    security.declarePrivate( 'fNewVoidInformeCrearTraduccionesQueFaltan')    
    def fNewVoidInformeCrearTraduccionesQueFaltan( self):
        unInforme = {
            'valid':                    True,
            'fecha_informe':            '',
            'start_date':               '',
            'end_date':                 '',
            'strings_to_complete':      0,
            'strings_completed':        0,
            'translations_created':     0,
            'expected_operations':      0,
            'operations_done':          0,
            'error':                    '',
            'error_detail':             '',
        }
        return unInforme

        
       
        
    
       
              
    security.declarePrivate( 'fNoHaComenzadoOEnDevelopmentODebug')    
    def fNoHaComenzadoOEnDevelopmentODebug( self,):
        if cUnderDevelopmentOrDebug:
            return True
        return not ( self.getHaComenzado() == True)
    
    
    
   
    security.declarePrivate( 'fCodigoIdiomaPorDefecto')
    def fCodigoIdiomaPorDefecto( self, ):
        unCodigoIdioma = self.getCodigoIdiomaPorDefecto()
        if not unCodigoIdioma:
            unCodigoIdioma = cDefaultLanguage
            
        return unCodigoIdioma
    
        
    
    security.declarePrivate( 'fNombreModuloPorDefecto')
    def fNombreModuloPorDefecto( self, ):
        unNombreModulo = self.getNombreModuloPorDefecto()
        if not unNombreModulo:
            unNombreModulo = cDefaultModule
            
        return unNombreModulo
    
        
    security.declarePrivate( 'fMaximoLineasAImportarPO')
    def fMaximoLineasAImportarPO( self, ):
        unMaximo = self.getMaximoLineasAImportarGNUgettextPO()
        if not unMaximo:
            unMaximo = cGNUgettextPOMaxLinesToScan
            
        return unMaximo
    
        
    security.declarePrivate( 'fMaximoLineasAImportarProperties')
    def fMaximoLineasAImportarProperties( self, ):
        unMaximo = self.getMaximoLineasAImportarJavaProperties()
        if not unMaximo:
            unMaximo = cPropertiesMaxLinesToScan
            
        return unMaximo
    
                                     
        
# ###################################################################
#   Contenidos intercambio access
#
                                
                
                
                
    security.declareProtected( permissions.View, 'fObtenerTodosContenidosIntercambio')
    def fObtenerTodosContenidosIntercambio( self, ):
   
        unosElementos = self.objectValues( cNombreTipoTRAContenidoIntercambio) 
        return unosElementos
         
  
    
    
    security.declareProtected( permissions.View, 'fObtenerTodosContenidosIntercambioNoExcluidos')
    def fObtenerTodosContenidosIntercambioNoExcluidos( self, ):
               
        unosContenidosIntercambio = self.fObtenerTodosContenidosIntercambio()
        unosContenidosIntercambioNoExcluidos = [ unContenidoIntercambio for unContenidoIntercambio in unosContenidosIntercambio if not unContenidoIntercambio.getExcluirDeImportacion()]
        return unosContenidosIntercambioNoExcluidos   
             
                
# ################################################################
#   Add and remove content to be imported
# ###############################                  
        


    
    security.declarePrivate( 'fCrearContenidoIntercambio')    
    def fCrearContenidoIntercambio( self,
        theTimeProfilingResults =None,
        theModelDDvlPloneTool_Mutators   =None, 
        theNewTypeName          ='', 
        theNewOneTitle          ='', 
        theNewOneDescription    ='', 
        theAdditionalParams     =None,
        thePermissionsCache     =None,
        theRolesCache           =None,
        theParentExecutionRecord=None):
    
    
        unExecutionRecord = self.fStartExecution( 'method',  'fCrearContenidoIntercambio', None, True, { 'log_what': 'details', 'log_when': True, }) 

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators  import ModelDDvlPloneTool_Mutators, cModificationKind_CreateSubElement, cModificationKind_Create, cModificationKind_ChangeValues

        try:
            unasDescripcionesContenidosCreados = []
            try:
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_CreateTRAContenidoIntercambio, 
                    theElementsBindings     = { cBoundObject: self,}, 
                    theRulesToCollect       = None, 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord,
                )
              
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_no_permission_msgid', "User does not have permission to create interchange contents.-"), }
                    return anActionReport  
                            
                aModelDDvlPlone_tool = self.fModelDDvlPloneTool()
                             
                
                unNewTypeName = theNewTypeName
                if not unNewTypeName:
                    unNewTypeName = cNombreTipoTRAContenidoIntercambio
                
                aDefaultLanguage       = theAdditionalParams.get( 'theDefaultLanguage', None)
                unUploadedFile         = theAdditionalParams.get( 'theUploadedFile',    None)
        
                
                if not unUploadedFile:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorcreacioncontenidointercambio_faltafichero_warning_msgid', "Can not create an interchange contents element without an uploaded file.-"), }
                    return anActionReport  
                
                unosContenidos = self.fContenidosDeUploadedFile( theParentExecutionRecord , unUploadedFile, aDefaultLanguage, theAdditionalParams)
                
                if not unosContenidos:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorcreacioncontenidointercambio_ficherosincontenidovalido_warning_msgid', "Invalid interchange file contents. Can not create an interchange contents element without an uploaded file with valid contents.-"), }
                    return anActionReport  
                
                unContenidoIntercambioCreationReport = None
                 
                unosClavesYContenidosParaOrdenar = [ [ '%s|||%s' % ( unUploadedContent.get( 'module', ''), '|'.join( sorted( unUploadedContent.get('languages',[]))), ), unUploadedContent] for unUploadedContent in unosContenidos]
                unosClavesYContenidosOrdenados = sorted( unosClavesYContenidosParaOrdenar, lambda unC, otroC : cmp( unC[ 0] , otroC[ 0]) )
                
                aPloneUtilsTool = self.getPloneUtilsToolForNormalizeString()  
                
                for unaClavesYUploadedContent in unosClavesYContenidosOrdenados:  
                    
                    unUploadedContent = unaClavesYUploadedContent[ 1]
                    
                    unSubExecutionRecord = self.fStartExecution( 'method',  'fCrearContenidoIntercambio::subSection for one Uploaded Content with module|||languages:', unExecutionRecord, False, { 'log_what': 'details', 'log_when': True, }, unaClavesYUploadedContent[ 0]) 
                    
                    try:
                        unModulo    = unUploadedContent.get( 'module', '')
                        
                        if not unModulo:
                            unModulo = self.fNombreModuloPorDefecto()
                    
                        unosLenguages = sorted( unUploadedContent[ 'languages'])
                        unLenguagesString = ', '.join( [ ('[%s]' % unLenguage) for unLenguage in unosLenguages ])
                        unBaseTitle = '%s %s' % ( unModulo, unLenguagesString, )
                        
                        unasUploadedEntries = unUploadedContent.get( 'uploaded_entries', [])
                        unasDescripciones = [ 'file: %(file_name)s, kind: %(file_kind)s, ref: %(is_reference)d, language: %(language)s, country: %(country)s, charset: %(charset)s, fallback for: %(is_fallback_for)s, domain: %(domain)s,'  % unUploadedEntry for unUploadedEntry in unasUploadedEntries]
                        unaDescripcion = 'Module %s in languages %s' % ( unModulo, unLenguagesString, )
                        unTexto = '\n'.join( [ unaDescripcion] + unasDescripciones)
                               
                        unFilename = ''
                        try:
                            unFilename = unUploadedFile.filename
                        except:
                            None
                        if not unFilename:
                            unFilename = 'DefaultFile_%s.%s' %  ( unLenguagesString, unUploadedFile.get( 'file_kind', 'unknown'), )
                            
                        someContenidosIntercambio = self.fObtenerTodosContenidosIntercambio()
                        someTitles = [ unContInter.Title() for unContInter in someContenidosIntercambio]
                        someIds = [ unContInter.getId() for unContInter in someContenidosIntercambio]
                        
   
                        
                                 
                        unTitle = unBaseTitle
                        
                        aNewId = unTitle.lower().replace( ' ', '-')
                        if aPloneUtilsTool:
                            aNewId = aPloneUtilsTool.normalizeString( aNewId)
                            
                        unCounter = 0 
                        
                        while ( unTitle in someTitles) or ( aNewId in someIds):
                            unCounter += 1
                            unTitle = '%s-%d' % ( unBaseTitle, unCounter, )
                            aNewId = unTitle.lower().replace( ' ', '-')
                            if aPloneUtilsTool:
                                aNewId = aPloneUtilsTool.normalizeString( aNewId)
        
                            
                        unMemberId = self.fGetMemberId()
        
                        anAttrsDict = { 
                            'title':                    unTitle,
                            'description':              unaDescripcion,
                            'text':                     unTexto,
                            'usuarioContribuidor':      unMemberId,
                            'nombreModulo':             unModulo,
                            'excluirDeImportacion':     False,
                        }
                        
                        unaIdNuevoContenidoIntercambio = self.invokeFactory( cNombreTipoTRAContenidoIntercambio, aNewId, **anAttrsDict)
                        if not unaIdNuevoContenidoIntercambio:
                            anActionReport = { 'effect': 'error', 'failure': '%s module %s' % (   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorcreacioncontenidointercambio_errorencreacion', "No se ha podido crear Contenido de Intercambio."), unModulo, ) }
                            return anActionReport     
                                        
                        unNuevoContenidoIntercambio = self.getElementoPorID( unaIdNuevoContenidoIntercambio)
                        if not unNuevoContenidoIntercambio:
                            anActionReport = { 'effect': 'error', 'failure': '%s module %s' % (   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorcreacioncontenidointercambio_errorencreacion', "No se ha podido crear Contenido de Intercambio."), unModulo, ) }
                            return anActionReport     
    
                        unNuevoContenidoIntercambio.pSetContenido( unUploadedContent)   
                        
                        unasDescripcionesContenidosCreados.append( unaDescripcion)
                        
                        unResultadoNuevoContenidoIntercambio = aModelDDvlPlone_tool.fRetrieveTypeConfig( 
                            theTimeProfilingResults     =None,
                            theElement                  =unNuevoContenidoIntercambio, 
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
                        if not unResultadoNuevoContenidoIntercambio:
                            anActionReport = { 'effect': 'error', 'failure': 'retrieval_failure', }
                            return anActionReport     
         
                        unContenidoIntercambioCreationReport = { 'effect': 'created', 'new_object_result': unResultadoNuevoContenidoIntercambio, }
                             
                        aModelDDvlPloneTool_Mutators = theModelDDvlPloneTool_Mutators
                        if not aModelDDvlPloneTool_Mutators:
                            aModelDDvlPloneTool_Mutators = ModelDDvlPloneTool_Mutators()
                            
                        aCreateElementReport = aModelDDvlPloneTool_Mutators.fNewVoidCreateElementReport()
                        aCreateElementReport.update( { 'effect': 'created', 'new_object_result': unResultadoNuevoContenidoIntercambio, })
                        
                        someFieldReports    = aCreateElementReport[ 'field_reports']
                        aFieldReportsByName = aCreateElementReport[ 'field_reports_by_name']
                        
                        aReportForField = { 'attribute_name': 'id',          'effect': 'changed', 'new_value': aNewId, 'previous_value': '',}
                        someFieldReports.append( aReportForField)            
                        aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                        
                        aReportForField = { 'attribute_name': 'title',       'effect': 'changed', 'new_value': unTitle,           'previous_value': '',}
                        someFieldReports.append( aReportForField)            
                        aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                        
                        aReportForField = { 'attribute_name': 'description', 'effect': 'changed', 'new_value': unaDescripcion,    'previous_value': '',}
                        someFieldReports.append( aReportForField)            
                        aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                                           
                        aReportForField = { 'attribute_name': 'text', 'effect': 'changed', 'new_value': unTexto,    'previous_value': '',}
                        someFieldReports.append( aReportForField)            
                        aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                                           
                        aReportForField = { 'attribute_name': 'nombreModulo', 'effect': 'changed', 'new_value': unModulo,    'previous_value': '',}
                        someFieldReports.append( aReportForField)            
                        aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                                           
                        aReportForField = { 'attribute_name': 'usuarioContribuidor', 'effect': 'changed', 'new_value': unMemberId,    'previous_value': '',}
                        someFieldReports.append( aReportForField)            
                        aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                                           
                        aModelDDvlPloneTool_Mutators.pSetAudit_Creation( self,                        cModificationKind_CreateSubElement, aCreateElementReport, theUseCounter=True)       
                        aModelDDvlPloneTool_Mutators.pSetAudit_Creation( unNuevoContenidoIntercambio, cModificationKind_Create,           aCreateElementReport)       

                        self.pFlushCachedTemplates_All()                            
                        
                        transaction.commit()
                        
                        
                        logging.getLogger( 'gvSIGi18n::fCrearContenidoIntercambio').info("COMMIT new %s %s with module %s description\n%s\nand text:\n%s\n" % ( unNewTypeName, unTitle,  unModulo, unaDescripcion, unTexto, )) 
        
                    finally:
                        unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                        unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
                        
                        
                if unContenidoIntercambioCreationReport:
                    return unContenidoIntercambioCreationReport
                
                anActionReport = { 'effect': 'error', 'failure': 'Error after already created %s\n%s' % ( '\n'.join( unasDescripcionesContenidosCreados), self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorcreacioncontenidointercambio_ningunocreado', "No se ha creado ningun Contenido de Intercambio."), ) }
                return anActionReport     

            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fCrearContenidoIntercambio\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                if hasattr( unaExceptionInfo[1], 'args'):
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                                         
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                anActionReport = { 'effect': 'error', 'failure': 'Error after already created %s\n%s' % ( '\n'.join( unasDescripcionesContenidosCreados), self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorcreacioncontenidointercambio_ningunocreado', "No se ha creado ningun Contenido de Intercambio."), ) }
                return anActionReport     
              
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

        
                
                
                
            
            
            
    security.declareProtected( permissions.DeleteObjects, 'fEliminarContenidoIntercambio')    
    def fEliminarContenidoIntercambio( self, theContenidoIntercambio, theUseCaseQueryResult=None, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fEliminarContenidoIntercambio', theParentExecutionRecord, False) 
        
        try:
            if not theContenidoIntercambio:
                return False
            
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                
            unUseCaseQueryResult = theUseCaseQueryResult
            if not theUseCaseQueryResult or not ( theUseCaseQueryResult.get( 'use_case_name', '') == cUseCase_DeleteTRAContenidoIntercambio):
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_DeleteTRAContenidoIntercambio,             
                    theElementsBindings     = { cBoundObject: self,},                    
                    theRulesToCollect       = None,                                      
                    thePermissionsCache     = unPermissionsCache,    
                    theRolesCache           = unRolesCache,                
                    theParentExecutionRecord= unExecutionRecord,
                )
            if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                return False
                                                
            unosContenidosIntercambio = self.fObtenerTodosContenidosIntercambio()
            
            if not ( theContenidoIntercambio in unosContenidosIntercambio):
                return False
            
            self.manage_delObjects( [ theContenidoIntercambio.getId(), ])
                
            return True
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

        
     
    
            
            
            
            
            
            
                
                                
        
# ###################################################################
#   SCAN, ANALYZE AND STORE RAW CONTENT TO BE IMPORTED
#
                
                         

    
    security.declarePrivate( 'fContenidosDeUploadedFile')    
    def fContenidosDeUploadedFile( self,
        theParentExecutionRecord =None, 
        theUploadedFile         =None, 
        theDefaultLanguage      ='',
        theAdditionalParams     =None):
                                  
         
        unExecutionRecord = self.fStartExecution( 'method',  'fContenidosDeUploadedFile', theParentExecutionRecord, False) 

        try:
            todosContenidos = [ ]

            if not theUploadedFile:
                return unosContenidos
                        
            # Determine if theUploadedFile is a zip or jar archive content
            unIsZip = False
            unZipFile = None
            try:
                unZipFile = ZipFile( theUploadedFile)  
            except:
                None
            if unZipFile:
                # Error if True
                if not( unZipFile.testzip()):
                    unIsZip = True
            
            if not unIsZip:
                return self.fContenidosDeUploadedFile_NoNestedZips( 
                    theParentExecutionRecord=unExecutionRecord, 
                    theUploadedFile         =theUploadedFile, 
                    theDefaultLanguage      =theDefaultLanguage,
                    theAdditionalParams     =theAdditionalParams)
            
            aMustProcessWholeZipAsSingleFile = False
            
            someFileNames = unZipFile.namelist()
            for aFullFileName in someFileNames:
                
                aBaseName = os.path.basename( aFullFileName)
                if aBaseName:
                    aBaseNameLower = aBaseName.lower()
                    aBaseNamePostfix = os.path.splitext(  aBaseNameLower)[ 1]
                    if not( aBaseNamePostfix == cZipFilePostfix.lower()):
                        aMustProcessWholeZipAsSingleFile = True
                    else:
                        unContentData = unZipFile.read( aFullFileName)                            
                        if unContentData:
                            unZipBuffer      = StringIO( unContentData)
                            someContenidos = self.fContenidosDeUploadedFile_NoNestedZips( 
                                theParentExecutionRecord=unExecutionRecord, 
                                theUploadedFile         =unZipBuffer, 
                                theDefaultLanguage      =theDefaultLanguage,
                                theAdditionalParams     =theAdditionalParams)
                            if someContenidos:
                                todosContenidos.extend( someContenidos)
                
            if aMustProcessWholeZipAsSingleFile:
                someContenidos = self.fContenidosDeUploadedFile_NoNestedZips( 
                    theParentExecutionRecord=unExecutionRecord, 
                    theUploadedFile         =theUploadedFile, 
                    theDefaultLanguage      =theDefaultLanguage,
                    theAdditionalParams     =theAdditionalParams)
                if someContenidos:
                    todosContenidos.extend( someContenidos)
                            
            return todosContenidos
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()


                
                


                         

    
    security.declarePrivate( 'fContenidosDeUploadedFile_NoNestedZips')    
    def fContenidosDeUploadedFile_NoNestedZips( self,
        theParentExecutionRecord =None, 
        theUploadedFile         =None, 
        theDefaultLanguage      ='',
        theAdditionalParams     =None):
                                  
         
        unExecutionRecord = self.fStartExecution( 'method',  'fContenidosDeUploadedFile_NoNestedZips', theParentExecutionRecord, False) 

        try:
            unosContenidos = [ ]

            if not theUploadedFile:
                return unosContenidos
                        
            # Determine if theUploadedFile is a zip or jar archive content
            unIsZip = False
            unZipFile = None
            try:
                unZipFile = ZipFile( theUploadedFile)  
            except:
                None
            if unZipFile:
                # Error if True
                if not( unZipFile.testzip()):
                    unIsZip = True
            
            someUploadedEntries = []
            if unIsZip:
                someUploadedEntries = self.fUploadedEntriesFromZipFileManifest(      theParentExecutionRecord , unZipFile, theAdditionalParams)
                if not someUploadedEntries:
                    someUploadedEntries = self.fUploadedEntriesFromZipFileLocalesCSV(      theParentExecutionRecord , unZipFile, theAdditionalParams)
                    if not someUploadedEntries:
                        someUploadedEntries = self.fUploadedEntriesFromZipFileDirectory( theParentExecutionRecord , unZipFile, theDefaultLanguage, theAdditionalParams)
            else:        
                anUploadedEntry = self.fUploadedEntryFromNonZipFile( theParentExecutionRecord , theUploadedFile, theAdditionalParams)
                if anUploadedEntry:
                    someUploadedEntries = [ anUploadedEntry, ]   
                    
                        
            for unUploadedEntry in someUploadedEntries:
                
                if ( unUploadedEntry[ 'file_kind'] == cPropertiesFilePostfix) and unUploadedEntry[ 'is_reference']:
                    continue
                
                
                # #########################################
                """ACV 20091206 Remove reuse of content objects of same module name, to Force One Content Per File, such that they can be individually configured (module name), deleted or excluded from import.
                
                """
                # ACV 20091206 Was:
                #unUploadedContent = None

                #unFileName = unUploadedEntry[ 'file_name']
                #unBaseName = os.path.basename( unFileName)
                #unDirName  = os.path.dirname(  unFileName)
                #unModuleName = unUploadedEntry.get( 'module', '')
                #if ( not unModuleName) and unDirName:
                    #unModuleName = unDirName
                
                #if unModuleName:
                    #for unContenido in unosContenidos:
                        #if unModuleName == unContenido.get( 'module', ''):
                            #unUploadedContent = unContenido
                            #break
                #if not unUploadedContent:
                    #unUploadedContent = self.fNewVoidUploadedContent( )
                    #unUploadedContent[ 'module'] = unModuleName
                    #unosContenidos.append( unUploadedContent)
                    
                    
                if unUploadedEntry[ 'file_kind'] == cPropertiesFilePostfix:
                    #if unUploadedEntry[ 'is_reference']:                    
                        #unUploadedContent [ 'reference_uploaded_entries'].append( unUploadedEntry)
                    #else:
                    
                    unUploadedContent = self.fNewVoidUploadedContent( )
                    unFileName = unUploadedEntry[ 'file_name']
                    unDirName  = os.path.dirname(  unFileName)
                    if unDirName:
                        unUploadedContent[ 'module'] = unDirName
                    else:
                        unUploadedContent[ 'module'] = unUploadedEntry.get( 'module', '')
                    unosContenidos.append( unUploadedContent)
                    
                    unUploadedContent [ 'uploaded_entries'].append( unUploadedEntry)
                    if not ( unUploadedEntry[ 'language_and_country'] in unUploadedContent [ 'languages']):
                        unUploadedContent [ 'languages'].append( unUploadedEntry[ 'language_and_country'])                                
                    self.pScanTranslationsProperties( theParentExecutionRecord , theUploadedFile, unZipFile, unUploadedContent, unUploadedEntry, theAdditionalParams)

                elif unUploadedEntry[ 'file_kind'] == cPOFilePostfix:
                    unUploadedContent = self.fNewVoidUploadedContent( )
                    unUploadedContent[ 'module'] = unUploadedEntry.get( 'module', '')
                    unosContenidos.append( unUploadedContent)
                    
                    unUploadedContent [ 'uploaded_entries'].append( unUploadedEntry)
                    if not ( unUploadedEntry[ 'language_and_country'] in unUploadedContent [ 'languages']):
                        unUploadedContent [ 'languages'].append( unUploadedEntry[ 'language_and_country'])   
                    if unUploadedEntry[ 'domain']:
                        unUploadedContent[ 'module'] = unUploadedEntry[ 'domain']                              
                    self.pScanTranslationsPO( theParentExecutionRecord, theUploadedFile, unZipFile, unUploadedContent, unUploadedEntry, theAdditionalParams)
                                         
            return unosContenidos
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()


                
                
                
            
                
    security.declarePrivate( 'fUploadedEntriesFromZipFileManifest')    
    def fUploadedEntriesFromZipFileManifest( self,
        theParentExecutionRecord =None, 
        theZipFile              =None, 
        theUploadedContent      =None,
        theAdditionalParams     =None):
                
        unExecutionRecord = self.fStartExecution( 'method',  'fUploadedEntriesFromZipFileManifest', theParentExecutionRecord, False) 

        try:
                
            if not theZipFile or not theUploadedContent:
                return []
            
            if not( cManifestFileFullName in theZipFile.namelist()):
                return []

            unContentData = None
            unReadError = False
            try:
                unContentData = theZipFile.read( cManifestFileFullName)
            except:
                return []
            
            if not unContentData:
                return []
        
            someLines = unContentData.splitlines()            
            unNumLines = len( someLines)
                    
            if unNumLines < 1:
                return []

            someUploadedEntries = []
            
            aDefaultModule = self.fNombreModuloPorDefecto()
            
            unLineIndex = 0
            unUploadedEntry = None
            while unLineIndex < unNumLines:
                unaLine =  someLines[ unLineIndex].strip()
                unLineIndex += 1     
                if not unaLine:
                    unUploadedEntry = None
                    continue
         
                if unaLine.startswith( cManifestEntryStartLinePrefix):
                    unFileName = unaLine[ len( cManifestEntryStartLinePrefix):].strip()
                    if unFileName:
                        if not( unFileName.lower().endswith( cPropertiesFilePostfix.lower()) or unFileName.lower().endswith( cPOFilePostfix.lower()) or unFileName.lower().endswith( cPOTFilePostfix.lower())):
                            unUploadedEntry = None
                        else:
                            unUploadedEntry = self.fNewVoidUploadedEntry()
                            someUploadedEntries.append( unUploadedEntry)
                            unUploadedEntry[ 'file_name']       = unFileName
                            unUploadedEntry[ 'in_zip']          = True
                            
                            if unFileName.lower().endswith( cPropertiesFilePostfix.lower()):
                                unUploadedEntry[ 'file_kind'] = cPropertiesFilePostfix
                                unModuleName, aVoidLanguage, aVoidCountry = self.fModuleLocaleLanguageAndCountryFromPropertiesFileName( unFileName, aDefaultModule, '')
                                if  unModuleName:
                                    unUploadedEntry[ 'module'] = unModuleName
                            elif unFileName.lower().endswith( cPOFilePostfix.lower()):
                                unUploadedEntry[ 'file_kind'] = cPOFilePostfix
                            elif unFileName.lower().endswith( cPOTFilePostfix.lower()):
                                unUploadedEntry[ 'file_kind']   = cPOFilePostfix
                                unUploadedEntry[ 'is_pot_file'] = True
                                unUploadedEntry[ 'language']    = self.fCodigoIdiomaPorDefecto()
                                unUploadedEntry[ 'country']     = ''
                                unUploadedEntry[ 'language_and_country']  = self.fCodigoIdiomaPorDefecto()
                                
                                
                elif unUploadedEntry:
                    if unaLine.startswith( cManifestLocaleLanguageStartLinePrefix):
                        unLocaleLanguage = unaLine[ len( cManifestLocaleLanguageStartLinePrefix):].strip()
                        if unLocaleLanguage:
                            unUploadedEntry[ 'is_reference']    = False
                            unUploadedEntry[ 'language']        = unLocaleLanguage
                            if unUploadedEntry[ 'country']:
                                unUploadedEntry[ 'language_and_country']         = '%s-%s' % ( unLocaleLanguage, unUploadedEntry[ 'country'], )
                            else:
                                unUploadedEntry[ 'language_and_country']         = unLocaleLanguage
                    elif unaLine.startswith( cManifestLocaleCountryStartLinePrefix):
                        unLocaleCountry = unaLine[ len( cManifestLocaleCountryStartLinePrefix):].strip()
                        if unLocaleCountry:
                            unUploadedEntry[ 'country'] = unLocaleCountry
                            if unUploadedEntry[ 'language']:
                                unUploadedEntry[ 'language_and_country']         = '%s-%s' % ( unUploadedEntry[ 'language'], unLocaleCountry, )
                            else:
                                unUploadedEntry[ 'language_and_country'] = '-%s' % unLocaleCountry
                    elif unaLine.startswith( cManifestReferenceLocaleLanguageStartLinePrefix):
                        unReferenceLocaleLanguage = unaLine[ len( cManifestReferenceLocaleLanguageStartLinePrefix):].strip()
                        if unReferenceLocaleLanguage:
                            unUploadedEntry[ 'is_reference']    = True
                            unUploadedEntry[ 'language']        = unReferenceLocaleLanguage
                            if unUploadedEntry[ 'country']:
                                unUploadedEntry[ 'language_and_country']         = '%s-%s' % ( unReferenceLocaleLanguage, unUploadedEntry[ 'country'], )
                            else:
                                unUploadedEntry[ 'language_and_country'] = unReferenceLocaleLanguage
                            
                    elif unaLine.startswith( cManifestReferenceLocaleCountryStartLinePrefix):
                        unReferenceLocaleCountry = unaLine[ len( cManifestReferenceLocaleCountryStartLinePrefix):].strip()
                        if unReferenceLocaleCountry:
                            unUploadedEntry[ 'is_reference']    = True
                            unUploadedEntry[ 'country'] = unReferenceLocaleCountry
                            if unUploadedEntry[ 'language']:
                                unUploadedEntry[ 'language_and_country']         = '%s-%s' % ( unUploadedEntry[ 'language'], unReferenceLocaleCountry, )
                            else:
                                unUploadedEntry[ 'language_and_country'] = '-%s' % unReferenceLocaleCountry
                       
                    
            
            return someUploadedEntries
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()



               
            
                
    security.declarePrivate( 'fUploadedEntriesFromZipFileLocalesCSV')    
    def fUploadedEntriesFromZipFileLocalesCSV( self,
        theParentExecutionRecord =None, 
        theZipFile              =None, 
        theUploadedContent      =None,
        theAdditionalParams     =None):
                
        unExecutionRecord = self.fStartExecution( 'method',  'fUploadedEntriesFromZipFileLocalesCSV', theParentExecutionRecord, False) 

        try:
                
            if not theZipFile or not theUploadedContent:
                return []
            
            if not( cLocalesCSVFileFullName in theZipFile.namelist()):
                return []

            unContentData = None
            unReadError = False
            try:
                unContentData = theZipFile.read( cLocalesCSVFileFullName)
            except:
                return []
            
            if not unContentData:
                return []
        
            someLines = unContentData.splitlines()            
            unNumLines = len( someLines)
                    
            if unNumLines < 1:
                return []

            someUploadedEntries = []
            
            aDefaultModule = self.fNombreModuloPorDefecto()
            
            unLineIndex = 0
            while unLineIndex < unNumLines:
                unaLine =  someLines[ unLineIndex].strip()
                unLineIndex += 1     
                if not unaLine:
                    continue
                
                unFileName        = ''
                unLocaleLanguage  = ''
                unLocaleCountry   =  ''
                unLocaleVariation = ''
                unIsReference     = False
                
                unosLineFields = unaLine.split( ',')
                unNumFields = len( unosLineFields)
                if unNumFields > 0:
                    unFileName = unosLineFields[ 0]
                    if unFileName:
                        if not( unFileName.lower().endswith( cPropertiesFilePostfix.lower()) or unFileName.lower().endswith( cPOFilePostfix.lower()) or unFileName.lower().endswith( cPOTFilePostfix.lower())):
                            continue
                        else:
                            
                            if unNumFields > 0:
                                unLocaleLanguage  = unosLineFields[ 1].lower()  
                            if unNumFields > 1:
                                unLocaleCountry  = unosLineFields[ 2].lower()  
                            if unNumFields > 2:
                                unLocaleVariation  = unosLineFields[ 3].lower()  
                            if unNumFields > 3:
                                unIsReferenceString  = unosLineFields[ 4]  
                                unIsReference = unIsReferenceString.lower() == cLocalesCSVIsReferenceFile.lower()
                            
                            if not unLocaleLanguage:
                                continue
                            else:
                                unUploadedEntry = self.fNewVoidUploadedEntry()
                                someUploadedEntries.append( unUploadedEntry)
                                
                                unModuleName, aVoidLanguage, aVoidCountry = self.fModuleLocaleLanguageAndCountryFromPropertiesFileName( unFileName, aDefaultModule, '')
                                
                                unUploadedEntry[ 'file_name']       = unFileName
                                unUploadedEntry[ 'in_zip']          = True
                                unUploadedEntry[ 'is_reference']    = unIsReference
                                unUploadedEntry[ 'language']        = unLocaleLanguage
                                unUploadedEntry[ 'country']         = unLocaleCountry
                                if unModuleName:
                                    unUploadedEntry[ 'module']      = unModuleName
                                
                                if unLocaleCountry:
                                    unUploadedEntry[ 'language_and_country']  = '%s-%s' % ( unLocaleLanguage, unLocaleCountry,)
                                else:
                                    unUploadedEntry[ 'language_and_country']  = '%s' % unLocaleLanguage
                                    
                                if unFileName.lower().endswith( cPropertiesFilePostfix.lower()):
                                    unUploadedEntry[ 'file_kind'] = cPropertiesFilePostfix
                                elif unFileName.lower().endswith( cPOFilePostfix.lower()):
                                    unUploadedEntry[ 'file_kind'] = cPOFilePostfix
                                elif unFileName.lower().endswith( cPOTFilePostfix.lower()):
                                    unUploadedEntry[ 'file_kind']   = cPOFilePostfix
                                    unUploadedEntry[ 'is_pot_file'] = True
                                    
                                
            
            return someUploadedEntries
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()



        
     
                
                
                
    security.declarePrivate( 'fUploadedEntriesFromZipFileDirectory')    
    def fUploadedEntriesFromZipFileDirectory( self,
        theParentExecutionRecord =None, 
        theZipFile              =None, 
        theDefaultLanguage      ='',
        theAdditionalParams     =None):
                
        unExecutionRecord = self.fStartExecution( 'method',  'fUploadedEntriesFromZipFileDirectory', theParentExecutionRecord, False) 

        try:
                
            if not theZipFile:
                return []
            
            aDefaultLanguage = theDefaultLanguage
            if not aDefaultLanguage:
                aDefaultLanguage = self.fCodigoIdiomaPorDefecto()
                
            aDefaultModule = self.fNombreModuloPorDefecto()

            someUploadedEntries = []
            
            someFileNames = theZipFile.namelist()
            for aFullFileName in someFileNames:
                
                unUploadedEntry = None
                unLocaleLanguage = ''
                unLocaleCountry = ''
                
                aBaseName = os.path.basename( aFullFileName)
                if aBaseName:
                    aBaseNameLower = aBaseName.lower()
                    aBaseNamePostfix = os.path.splitext(  aBaseNameLower)[ 1]
                    if not ( aBaseNameLower in [ cManifestFileFullName.lower(), cLocalesCSVFileFullName.lower(),]):
                         
                        if aBaseNamePostfix == cPropertiesFilePostfix.lower():

                            aModuleName, unLocaleLanguage, unLocaleCountry = self.fModuleLocaleLanguageAndCountryFromPropertiesFileName( aBaseName, aDefaultModule, aDefaultLanguage)
   
                            #if aBaseNameLower == cDefaultLanguagePropertiesFileName:
                                #unLocaleLanguage = aDefaultLanguage
                                #unLocaleCountry = ''
                            #else:
                                
                                #if aBaseNameLower.startswith( cFilenamePropertiesBase):
                                    #unLocaleLanguage, unLocaleCountry = self.fLocaleLanguageAndCountryFromPropertiesFileName(  aBaseName, aDefaultLanguage)   
                                #else:                        
                                    #unLocaleLanguage, unLocaleCountry = self.fLocaleLanguageAndCountryFromNonDefaultPropertiesFileName(  aBaseName, aDefaultLanguage)   
                                
                                #if not unLocaleLanguage:
                                    #unLocaleLanguage, unLocaleCountry = self.fLocaleLanguageAndCountryFromZipPropertiesFile( theParentExecutionRecord, theZipFile, aFullFileName)   
                                
                            if unLocaleLanguage:
                                unUploadedEntry = self.fNewVoidUploadedEntry()
                                unUploadedEntry[ 'in_zip']    = True
                                unUploadedEntry[ 'file_name'] = aFullFileName
                                unUploadedEntry[ 'file_kind'] = cPropertiesFilePostfix
                                if aModuleName:
                                    unUploadedEntry[ 'module']    = aModuleName
                                unUploadedEntry[ 'language']  = unLocaleLanguage.lower()
                                if unLocaleCountry:
                                    unUploadedEntry[ 'country']                 = unLocaleCountry.lower()
                                    unUploadedEntry[ 'language_and_country']    = '%s-%s' % ( unLocaleLanguage.lower(), unLocaleCountry.lower(), )
                                else:
                                    unUploadedEntry[ 'country']                 = ''
                                    unUploadedEntry[ 'language_and_country']    = unLocaleLanguage.lower()
                                      
                        elif aBaseNamePostfix in [  cPOFilePostfix.lower(), cPOTFilePostfix.lower(),]:
                      
                            unPOHeader = self.fPOHeaderFromZipPOFile( theParentExecutionRecord, theZipFile, aFullFileName) 
                            
                            if unPOHeader:
                                
                                unHeaderLastLineNumber = unPOHeader.get( 'last_line_number', -1)
                                unLocaleLanguage = unPOHeader.get( 'language_code', '')
                                unLocaleCountry  = unPOHeader.get( 'country', '')
                                unCharset        = unPOHeader.get( 'charset', '')
                                unIsFallbackFor  = unPOHeader.get( 'is_fallback_for', '')
                                unDomain         = unPOHeader.get( 'domain', '')
                                
                                if not unLocaleLanguage:
                                    unLocaleLanguage = aDefaultLanguage.lower()
                                    
                                if not unDomain:
                                    unDomain = self.fNombreModuloPorDefecto().lower()
                                    
                                if unCharset:
                                    unCharSetExists = True
                                    try:
                                        aVoid = ''.decode( unCharset )
                                    except:
                                        unCharSetExists = False
                                        
                                    if not unCharSetExists:
                                        unCharset = 'utf-8'
                                else:
                                    unCharset = 'utf-8'
                                    
                                if unLocaleLanguage:
                                    unUploadedEntry = self.fNewVoidUploadedEntry()
                                    unUploadedEntry[ 'in_zip']          = True                                
                                    unUploadedEntry[ 'file_name']       = aFullFileName
                                    unUploadedEntry[ 'file_kind']       = cPOFilePostfix
                                    unUploadedEntry[ 'charset']         = unCharset
                                    unUploadedEntry[ 'is_fallback_for'] = unIsFallbackFor
                                    unUploadedEntry[ 'domain']          = unDomain
                                    unUploadedEntry[ 'last_header_line_number']        = unHeaderLastLineNumber
                                    if unLocaleCountry:
                                        unUploadedEntry[ 'country']                 = unLocaleCountry
                                        unUploadedEntry[ 'language_and_country']    = '%s-%s' % ( unLocaleLanguage, unLocaleCountry, )
                                    else:
                                        unUploadedEntry[ 'country']                 = ''
                                        unUploadedEntry[ 'language_and_country']    = unLocaleLanguage

                                    if aBaseNamePostfix == cPOTFilePostfix.lower():
                                        unUploadedEntry[ 'is_pot_file'] = True
                                        unUploadedEntry[ 'language']    = self.getCodigoIdiomaPorDefecto() or cDefaultLanguage
                                        unUploadedEntry[ 'country']     = ''
                                        unUploadedEntry[ 'language_and_country']  = unLocaleLanguage or self.getCodigoIdiomaPorDefecto() or cDefaultLanguage
                                        
                                        
                        
                if unUploadedEntry:
                    someUploadedEntries.append( unUploadedEntry)
                        
            return someUploadedEntries
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

                

            
            


    security.declarePrivate( 'fModuleLocaleLanguageAndCountryFromPropertiesFileName')    
    def fModuleLocaleLanguageAndCountryFromPropertiesFileName( self, theFileName, theDefaultModule, theDefaultLanguage):
        
        if not theFileName :
            return (  None, None, None, )
        
        aFileNameLower = theFileName.lower()
 
        if aFileNameLower in [ cManifestFileFullName.lower(), cLocalesCSVFileFullName.lower(),]:
            return (  None, None, None, )
             
        if aFileNameLower == cDefaultLanguagePropertiesFileName:
            return ( theDefaultModule, theDefaultLanguage, None)
        
        aFileNameWOPostfix, aFileNamePostfix = os.path.splitext(  theFileName)
        
        if not( aFileNamePostfix.lower() == cPropertiesFilePostfix.lower()):
            return (  None, None, None, )
        
        unModule = ''
        unLocaleLanguage = ''
        unLocaleCountry  = ''
        
        aFileNameWOPostfixLower = aFileNameWOPostfix.lower()

        if aFileNameWOPostfixLower.startswith( cFilenamePropertiesBase):
            unModule = theDefaultModule
            unIndexCharBeforeLanguage = len( cFilenamePropertiesBase)

        else:
            unIndexCharBeforeLanguage = aFileNameWOPostfixLower.find( cPropertiesFileCharBeforeLanguage, 0)
            if not ( unIndexCharBeforeLanguage >= 0):
                unModule = aFileNameWOPostfix
                return ( unModule, theDefaultLanguage, None)
            else:
                unModule = aFileNameWOPostfix[:unIndexCharBeforeLanguage]
            
        unIndexCharBeforeCountry = aFileNameWOPostfixLower.find( cPropertiesFileCharBeforeCountry, unIndexCharBeforeLanguage + 1)
        if unIndexCharBeforeCountry >= 0:
            unLocaleLanguage = aFileNameWOPostfixLower[ unIndexCharBeforeLanguage + len( cPropertiesFileCharBeforeLanguage):unIndexCharBeforeCountry].lower()   
            unLocaleCountry  = aFileNameWOPostfixLower[  unIndexCharBeforeCountry + len( cPropertiesFileCharBeforeCountry):].lower()   
        else:
            unLocaleLanguage = aFileNameWOPostfixLower[ unIndexCharBeforeLanguage + len( cPropertiesFileCharBeforeLanguage):].lower()   
            unLocaleCountry = ''
                
        return ( unModule, unLocaleLanguage, unLocaleCountry, )       
                
    
    
                            
            
            
                

    #security.declarePrivate( 'fLocaleLanguageAndCountryFromPropertiesFileName')    
    #def fLocaleLanguageAndCountryFromPropertiesFileName( self, theFileName, theDefaultLanguage):
        
        #if not theFileName :
            #return ( None, None, )
 
        #aFileNameLower = theFileName.lower()
        #if not aFileNameLower.startswith( cFilenamePropertiesBase):
            #return ( None, None, )
        
        #unLocaleLanguage = ''
        #unLocaleCountry  = ''
        
        #aFileNameWOPostfix, aFileNamePostfix = os.path.splitext(  theFileName)
        #if not aFileNamePostfix.lower() == cPropertiesFilePostfix:
            #return ( None, None, )
        
        #unIndexCharBeforeLanguage = aFileNameWOPostfix.find( cPropertiesFileCharBeforeLanguage, 0)
        
        #if not( unIndexCharBeforeLanguage >= 0):
            #return ( theDefaultLanguage, None)
        
        #unIndexCharBeforeCountry = aFileNameWOPostfix.find( cPropertiesFileCharBeforeCountry, unIndexCharBeforeLanguage + 1)
        #if unIndexCharBeforeCountry >= 0:
            #unLocaleLanguage = aFileNameWOPostfix[ unIndexCharBeforeLanguage + len( cPropertiesFileCharBeforeLanguage):unIndexCharBeforeCountry].lower()   
            #unLocaleCountry  = aFileNameWOPostfix[  unIndexCharBeforeCountry + len( cPropertiesFileCharBeforeCountry):].lower()   
        #else:
            #unLocaleLanguage = aFileNameWOPostfix[ unIndexCharBeforeLanguage + len( cPropertiesFileCharBeforeLanguage):].lower()   
            #unLocaleCountry = ''
                
        #return ( unLocaleLanguage, unLocaleCountry, )       
                
    
    

    #security.declarePrivate( 'fLocaleLanguageAndCountryFromNonDefaultPropertiesFileName')    
    #def fLocaleLanguageAndCountryFromNonDefaultPropertiesFileName( self, theFileName, theDefaultLanguage):
        
        #if not theFileName :
            #return ( None, None, )
        
        #aFileNameLower = theFileName.lower()
 
        #if aFileNameLower in [ cManifestFileFullName.lower(), cLocalesCSVFileFullName.lower(),]:
            #return ( None, None, )
             
        #if aFileNameLower == cDefaultLanguagePropertiesFileName:
            #return ( theDefaultLanguage, None)
        
        #if aFileNameLower.startswith( cFilenamePropertiesBase):
            #return self.fLocaleLanguageAndCountryFromPropertiesFileName( theFileName, theDefaultLanguage)

        #aFileNameWOPostfix, aFileNamePostfix = os.path.splitext(  aFileNameLower)
        #if not( aFileNamePostfix == cPropertiesFilePostfix.lower()):
            #return ( None, None, )
        

        #unLocaleLanguage = ''
        #unLocaleCountry  = ''
        
        #unIndexCharBeforeLanguage = aFileNameWOPostfix.find( cPropertiesFileCharBeforeLanguage, 0)
        #if not ( unIndexCharBeforeLanguage >= 0):
            #return ( theDefaultLanguage, None)
        
        #unIndexCharBeforeCountry = aFileNameWOPostfix.find( cPropertiesFileCharBeforeCountry, unIndexCharBeforeLanguage + 1)
        #if unIndexCharBeforeCountry >= 0:
            #unLocaleLanguage = aFileNameWOPostfix[ unIndexCharBeforeLanguage + len( cPropertiesFileCharBeforeLanguage):unIndexCharBeforeCountry].lower()   
            #unLocaleCountry  = aFileNameWOPostfix[  unIndexCharBeforeCountry + len( cPropertiesFileCharBeforeCountry):].lower()   
        #else:
            #unLocaleLanguage = aFileNameWOPostfix[ unIndexCharBeforeLanguage + len( cPropertiesFileCharBeforeLanguage):].lower()   
            #unLocaleCountry = ''
                
        #return ( unLocaleLanguage, unLocaleCountry, )       
                
    
    
                
                  
  
    
    
    security.declarePrivate( 'fZipFileElementContent')    
    def fZipFileElementContent( self, theZipFile, theFileName):
  
        if not theFileName or not theZipFile:
            return None
        
        unContent = None
        try:
            unContent = theZipFile.read( theFileName)
        except:
            return None
        return unContent
    
    
    
    
    
    #security.declarePrivate( 'fLocaleLanguageAndCountryFromZipPropertiesFile')    
    #def fLocaleLanguageAndCountryFromZipPropertiesFile( self, theParentExecutionRecord, theZipFile, theFileName):
        
        #if not theFileName or not theZipFile:
            #return ( None, None, )
        
        #if not ( theFileName.lower().endswith( cPropertiesFilePostfix.lower())):
            #return ( None, None, )

        #unContentData = self.fZipFileElementContent( theZipFile, theFileName)
        #if not unContentData:
            #return ( None, None, )
        
        #return self.fLocaleLanguageAndCountryFromPropertiesContent( theParentExecutionRecord, unContentData)
            
     

    
                
    security.declarePrivate( 'fLocaleLanguageAndCountryFromPropertiesContent')    
    def fLocaleLanguageAndCountryFromPropertiesContent( self, theParentExecutionRecord, theContent):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fLocaleLanguageAndCountryFromPropertiesContent', theParentExecutionRecord, False) 

        try:

            if not theContent:
                return ( None, None, )
            
            someLines = theContent.splitlines()
            
            unNumLines = len( someLines)
                    
            if unNumLines < 1:
                return ( None, None, )
    
            if not ( someLines[ 0].startswith( cPrefixLineaLenguaje)):
                return ( None, None, )
                
            unLocaleLanguage = ''
            unLocaleCountry  = ''
            
            unLenguage = someLines[0][len(cPrefixLineaLenguaje):]
            unBracketIndex = unLenguage.find( ']')
            if unBracketIndex >= 0:
                unLenguageAndCountry = unLenguage[:unBracketIndex]
                 
                unIndexCharBeforeCountry = unLenguageAndCountry.find( cLanguageSeparatorCountry, 0)
                if unIndexCharBeforeCountry >= 0:
                    unLocaleLanguage = unLenguageAndCountry[ :unIndexCharBeforeCountry].lower()  
                    unLocaleCountry  = unLenguageAndCountry[  unIndexCharBeforeCountry + len( cLanguageSeparatorCountry) :].lower()
                else:
                    unLocaleLanguage = unLenguageAndCountry.lower()
                    unLocaleCountry = ''
                     
            return ( unLocaleLanguage, unLocaleCountry, )
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

                     
                
                
    
                
    security.declarePrivate( 'fPOHeaderFromZipPOFile')    
    def fPOHeaderFromZipPOFile( self, theParentExecutionRecord, theZipFile, theFileName):
        
        if not theFileName or not theZipFile:
            return self.fVoidPOHeader()
        
        if not ( theFileName.lower().endswith( cPOFilePostfix.lower()) or theFileName.lower().endswith( cPOTFilePostfix.lower())):
            return self.fVoidPOHeader()

        unContentData = self.fZipFileElementContent( theZipFile, theFileName)
        if not unContentData:
            return self.fVoidPOHeader()
        
        return self.fPOHeaderFromPOContent( theParentExecutionRecord, unContentData)
            
     
    
    

    
    
    security.declarePrivate( 'fPOHeaderFromPOContent')    
    def fPOHeaderFromPOContent( self, theParentExecutionRecord ,theContent):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fPOHeaderFromPOContent', theParentExecutionRecord, False) 

        try:

            if not theContent:
                return None
            
            someLines = theContent.splitlines()
            
            unNumLines = len( someLines)
                    
            if unNumLines < 1:
                return None
    
            unPOHeader = self.fVoidPOHeader()
            unKeysFound = set()
            unKeysToFind = set( [ 'language_code', 'language_name', 'charset', 'country', 'is_fallback_for', 'domain',])
            unLineIndex = 0
            while unLineIndex < unNumLines:
                unaLine =  someLines[ unLineIndex].strip()
                unLineIndex += 1  
                if not unaLine or unaLine.startswith( cTranslationEntryDefaultPrefix) or unaLine.startswith( cTranslationEntrySourcesPrefix):
                    break
                
                if unLineIndex >= cPOMaxLinesToScanTryingToGetHeader:
                    break
                    
                unaLineLower = unaLine.lower()
                
                if unaLineLower.startswith( cPOHeaderPrefix_LanguageCode.lower()):
                    unPOHeader[ 'last_line_number'] = unLineIndex
                    unLocaleLanguage = ''
                    unLocaleCountry = ''
                    unValue = unaLine[ len( cPOHeaderPrefix_LanguageCode):].replace( '\\n', '').strip()
                    unQuoteIndex = unValue.find( '"', 0)  
                    if unQuoteIndex >= 0:
                        unValue = unValue[:unQuoteIndex] 
                        if unValue:
                            unIndexCharBeforeCountry = unValue.find( cLanguageSeparatorCountry, 0)
                            if unIndexCharBeforeCountry >= 0:
                                unLocaleLanguage = unValue[ :unIndexCharBeforeCountry]   
                                unLocaleCountry  = unValue[  unIndexCharBeforeCountry + len( cLanguageSeparatorCountry):] 
                            else:
                                unLocaleLanguage = unValue
                                unLocaleCountry  = '' 
                              
                    if unLocaleLanguage:
                        unPOHeader[ 'language_code'] = unLocaleLanguage.lower()
                        unKeysFound.add( 'language_code')
                    if unLocaleCountry:
                        unPOHeader[ 'country']       = unLocaleCountry.lower()
                        unKeysFound.add( 'country')
                            
                elif unaLineLower.startswith( cPOHeaderPrefix_LanguageName.lower()):
                    unPOHeader[ 'last_line_number'] = unLineIndex
                    unValue = unaLine[ len( cPOHeaderPrefix_LanguageName):].replace( '\\n', '').strip()
                    unQuoteIndex = unValue.find( '"', 0)  
                    if unQuoteIndex >= 0:
                        unValue = unValue[:unQuoteIndex] 
                    if unValue:
                        unPOHeader[ 'language_name'] = unValue.lower()
                        unKeysFound.add( 'language_name')
                        
                elif unaLineLower.startswith( cPOHeaderPrefix_ContentType.lower()):
                    unPOHeader[ 'last_line_number'] = unLineIndex
                    unCharset = ''
                    unValue = unaLine[ len( cPOHeaderPrefix_ContentType):].replace( '\\n', '').strip()
                    unQuoteIndex = unValue.find( '"', 0)  
                    if unQuoteIndex >= 0:
                        unValue = unValue[:unQuoteIndex] 
                    if unValue:
                        unIndexCharBeforeCharset = unValue.find( cPOHeaderPrefix_Charset, 0)
                        if unIndexCharBeforeCharset >= 0:
                            unCharset = unValue[ unIndexCharBeforeCharset + len( cPOHeaderPrefix_Charset):]   
                    if unCharset:
                        unCharset = unCharset.lower()
                        unCharSetExists = True
                        try:
                            aVoid = ''.decode( unCharset )
                        except:
                            unCharSetExists = False
                            
                        if not unCharSetExists:
                            unCharset = 'utf-8'
                        
                        unPOHeader[ 'charset'] = unCharset
                        unKeysFound.add( 'charset')
                        
                elif unaLineLower.startswith( cPOHeaderPrefix_IsFallbackFor.lower()):
                    unPOHeader[ 'last_line_number'] = unLineIndex
                    unValue = unaLine[ len( cPOHeaderPrefix_IsFallbackFor):].replace( '\\n', '').strip()
                    unQuoteIndex = unValue.find( '"', 0)  
                    if unQuoteIndex >= 0:
                        unValue = unValue[:unQuoteIndex] 
                    if unValue:
                        unPOHeader[ 'is_fallback_for'] = unValue.lower()
                        unKeysFound.add( 'is_fallback_for')
                        
                elif unaLineLower.startswith( cPOHeaderPrefix_Domain.lower()):
                    unPOHeader[ 'last_line_number'] = unLineIndex
                    unValue = unaLine[ len( cPOHeaderPrefix_Domain):].replace( '\\n', '').strip()
                    unQuoteIndex = unValue.find( '"', 0)  
                    if unQuoteIndex>= 0:
                        unValue = unValue[:unQuoteIndex] 
                    if unValue:
                        unPOHeader[ 'domain'] = unValue
                        unKeysFound.add( 'domain')
                
                if unKeysFound == unKeysToFind:
                    return unPOHeader
                    

            if not unKeysFound.intersection( set( [ 'language_code', 'language_name', 'charset', ])):
                return None
            
            return unPOHeader
       
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()


    
                
                
    

    
                
                
        
    security.declarePrivate( 'fUploadedEntryFromNonZipFile')    
    def fUploadedEntryFromNonZipFile( self,
        theParentExecutionRecord =None, 
        theUploadedFile         =None, 
        theAdditionalParams     =None):
                    
        unExecutionRecord = self.fStartExecution( 'method',  'fUploadedEntryFromNonZipFile', theParentExecutionRecord, False) 

        try:

            theUploadedFile.seek( 0)
            unContent = theUploadedFile.read()
            
            unPOHeader = self.fPOHeaderFromPOContent( theParentExecutionRecord, unContent)        
            if unPOHeader:
                unLocaleLanguage = unPOHeader.get( 'language_code', '')
                if not unLocaleLanguage:
                    unLocaleLanguage = self.fCodigoIdiomaPorDefecto()
                    
                unLocaleCountry  = unPOHeader.get( 'country', '')
                unCharset        = unPOHeader.get( 'charset', '')
                unCharSetExists = True
                try:
                    aVoid = ''.decode( unCharset )
                except:
                    unCharSetExists = False
                    
                if not unCharSetExists:
                    unCharset = 'utf-8'
                    
                
                unIsFallbackFor  = unPOHeader.get( 'is_fallback_for', '')
                unDomain         = unPOHeader.get( 'domain', '')
                unHeaderLastLineNumber = unPOHeader.get( 'last_line_number', -1)
                
                aFileName = ''
                try:
                    aFileName = theUploadedFile.filename
                except:
                    None
                if not aFileName:
                    aFileName = cPOUnknownFileName      
                
                                

                if unLocaleLanguage:
                    
                    unUploadedEntry = self.fNewVoidUploadedEntry()
                    
                    if aFileName.lower().endswith( cPOTFilePostfix.lower()):
                        unUploadedEntry[ 'is_pot_file'] = True

                    unUploadedEntry[ 'in_zip']          = False                                
                    unUploadedEntry[ 'file_name']       = aFileName
                    unUploadedEntry[ 'file_kind']       = cPOFilePostfix
                    unUploadedEntry[ 'charset']         = unCharset
                    unUploadedEntry[ 'is_fallback_for'] = unIsFallbackFor
                    unUploadedEntry[ 'domain']          = unDomain
                    unUploadedEntry[ 'language']        = unLocaleLanguage
                    unUploadedEntry[ 'last_header_line_number']        = unHeaderLastLineNumber
                    
                    if unLocaleCountry:
                        unUploadedEntry[ 'country']                 = unLocaleCountry
                        unUploadedEntry[ 'language_and_country']    = '%s-%s' % ( unLocaleLanguage, unLocaleCountry, )
                    else:
                        unUploadedEntry[ 'country']                 = ''
                        unUploadedEntry[ 'language_and_country']    = unLocaleLanguage
                    return unUploadedEntry
            
            
                
            aFileName = ''
            try:
                aFileName = theUploadedFile.filename
            except:
                None
            if not aFileName:
                aFileName = cPropertiesUnknownFileName  
            
            aDefaultModule   = self.fNombreModuloPorDefecto()
            aDefaultLanguage = self.fCodigoIdiomaPorDefecto()
                
            aModuleName, unLocaleLanguage, unLocaleCountry = self.fModuleLocaleLanguageAndCountryFromPropertiesFileName( aFileName, aDefaultModule, aDefaultLanguage)                
            if not unLocaleLanguage:
                unLocaleLanguage, unLocaleCountry = self.fLocaleLanguageAndCountryFromPropertiesContent( theParentExecutionRecord, unContent)   
            
            if not unLocaleLanguage:
                return None
                
            unUploadedEntry = self.fNewVoidUploadedEntry()
            unUploadedEntry[ 'in_zip']    = False
            unUploadedEntry[ 'file_name'] = aFileName
            unUploadedEntry[ 'file_kind'] = cPropertiesFilePostfix
            unUploadedEntry[ 'module']    = aModuleName
            unUploadedEntry[ 'language']  = unLocaleLanguage
            if unLocaleCountry:
                unUploadedEntry[ 'country']                 = unLocaleCountry
                unUploadedEntry[ 'language_and_country']    = '%s-%s' % ( unLocaleLanguage, unLocaleCountry, )
            else:
                unUploadedEntry[ 'country']                 = ''
                unUploadedEntry[ 'language_and_country']    = unLocaleLanguage
            return unUploadedEntry
    
              
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

       
                                 

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            

    security.declarePrivate( 'pScanTranslationsProperties')    
    def pScanTranslationsProperties( self,
        theParentExecutionRecord =None, 
        theUploadedFile         =None, 
        theZipFile              =None, 
        theUploadedContent       =None,
        theUploadedEntry        =None,
        theAdditionalParams     =None):
                
        unExecutionRecord = self.fStartExecution( 'method',  'pScanTranslationsProperties', theParentExecutionRecord, False) 

        try:
                
            if not theUploadedContent or not theUploadedEntry:
                return self
           
            unFileName = theUploadedEntry[ 'file_name']
            if not unFileName:
                return self
            
            unLenguage = theUploadedEntry[ 'language_and_country']
            if not unLenguage:
                return self
            
            unInZip = theUploadedEntry.get( 'in_zip', False)
            if unInZip:
                if not theZipFile:
                    return self
                
                unContentData = None
                try:
                    unContentData = theZipFile.read( unFileName)
                except:
                    None
                if not unContentData:
                    return self
                unasContentLines = unContentData.splitlines()
                unFicheroImportCursor = self.fFicheroImportCursorProperties( unasContentLines)
                if unFicheroImportCursor:
                    unFicheroImportCursor[ 'language'] = theUploadedEntry[ 'language_and_country']
                    if unFicheroImportCursor.get( 'exceeded_max_number_of_lines', False):
                        theUploadedEntry[ 'exceeded_max_number_of_lines'] = True
            else:
                theUploadedFile.seek( 0)
                unasContentLines = theUploadedFile.readlines()
                if not unasContentLines:
                    return self
                unFicheroImportCursor = self.fFicheroImportCursorProperties( unasContentLines)
                if unFicheroImportCursor:
                    if unFicheroImportCursor.get( 'exceeded_max_number_of_lines', False):
                        theUploadedEntry[ 'exceeded_max_number_of_lines'] = True
          
            if not ( unFicheroImportCursor and unFicheroImportCursor[ 'num_lines']):
                return self
            
            unasStringsAndTranslations   = theUploadedContent[ 'strings_and_translations']
            unasStringsAndEncodingErrors = theUploadedContent[ 'strings_with_encoding_errors']
                        
            unCursorRecord = self.fNextCursorRecordProperties( unFicheroImportCursor)
            while unCursorRecord:
                unSimbolo = unCursorRecord[ 'string_symbol']
                if unSimbolo:
                    
                    unaEncodedTranslation = unCursorRecord.get( 'encoded_translation', '')
                    unTranslationError = unCursorRecord.get( 'translation_error')
                    
                    if unTranslationError:
                        if not unasStringsAndTranslations.has_key( unSimbolo):
                            unasStringTranslations = { }
                            unasStringsAndTranslations[ unSimbolo] = unasStringTranslations
                        if not unasStringsAndEncodingErrors.has_key( unSimbolo):
                            unasStringEncodingErrorLanguages = [ unLenguage, ]
                            unasStringsAndEncodingErrors[ unSimbolo] = unasStringEncodingErrorLanguages
                        else: 
                            unasStringEncodingErrorLanguages = unasStringsAndEncodingErrors[ unSimbolo]
                            if not ( unLenguage in unasStringEncodingErrorLanguages):
                                unasStringEncodingErrorLanguages.append( unLenguage)
                    else:

                        unasStringTranslations = unasStringsAndTranslations.get( unSimbolo, None)
                        if unasStringTranslations == None:
                            unasStringTranslations = { }
                            unasStringsAndTranslations[ unSimbolo] = unasStringTranslations
                        if unaEncodedTranslation:
                            unasStringTranslations[ unLenguage] = unaEncodedTranslation
                        
                unCursorRecord = self.fNextCursorRecordProperties( unFicheroImportCursor)
                 
            return self
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

                                           
                
                
                

   
    
    security.declarePrivate( 'fFicheroImportCursorProperties')    
    def fFicheroImportCursorProperties( self, theContentLines):
        if not theContentLines:
            return None
        
        unCursor = self.fNewVoidImportCursor()
        unCursor[ 'file_kind'] = cPropertiesFilePostfix
        
        aTranslationService = getToolByName( self, 'translation_service', None)
        unCursor[ 'translation_service'] = aTranslationService
 
        unCursor[ 'content_lines']  = theContentLines
        
        unNumLines = len( theContentLines)
        
        unMaximoLineas = self.fMaximoLineasAImportarProperties()
        if unNumLines > unMaximoLineas:
            unNumLines = unMaximoLineas
            unCursor[ 'content_lines']  = theContentLines[:unMaximoLineas + cPropertiesMaxLinesToScanTryingToGetCadena]
            unCursor[ 'exceeded_max_number_of_lines'] = True
         
        unCursor[ 'num_lines']      = unNumLines
                
        if unNumLines < 1:
            unCursor[ 'error'] = "gvSIGi18n_NoContentLines_error_msgid"
            unCursor[ 'error_detail'] = theFileName                    
            return None

        unCursor[ 'next_line_index'] = 0
        if ( theContentLines[ 0].startswith(cPrefixLineaLenguaje)):
            unCursor[ 'next_line_index'] += 1
            unLenguage = theContentLines[0][len(cPrefixLineaLenguaje):]
            unBracketIndex = unLenguage.find( ']')
            if unBracketIndex >= 0:
                unLenguage = unLenguage[:unBracketIndex]
            if unLenguage:
                unCursor[ 'language'] = unLenguage
        
        unaPosibleLineaTimestamp = theContentLines[ unCursor[ 'next_line_index']]
        if unaPosibleLineaTimestamp and ( unaPosibleLineaTimestamp[ 0] == cPrefixLineaTimestamp):
            unCursor[ 'next_line_index'] += 1
        
        unCursor[ 'num_possible_records'] = unNumLines - unCursor[ 'next_line_index']
        
        if unCursor[ 'next_line_index'] >= unCursor[ 'num_lines']:
            return None
        
        return unCursor
           

    
    
    
    
    
    
   
    security.declarePrivate( 'fNextCursorRecordProperties')    
    def fNextCursorRecordProperties( self, theCursor):
        if not theCursor:
            return None
        
        aTranslationService = theCursor[ 'translation_service']
        if not aTranslationService:
            return None
        unRecord = self.fNewVoidCursorRecord()

        
        if not theCursor[ 'file_kind'] == cPropertiesFilePostfix:
            return None
                    
        unNumeroLineasIntentadas = 0
                
        while True:

            unNextLineIndex = theCursor[ 'next_line_index']
            
            if ( unNextLineIndex >= theCursor[ 'num_lines']):
                return None
            
            unNumeroLineasIntentadas += 1

            theCursor[ 'next_line_index'] += 1
            unaLinea = theCursor[ 'content_lines'][ unNextLineIndex].strip()
            if not unaLinea:
                continue
            
            if unaLinea.startswith( cPropertiesLine_CommentPrefix):
                continue
            
            unSeparatorIndex = unaLinea.find( '=', 0) 
            if unSeparatorIndex >= 0:
                unSimboloCadena     = unaLinea[ : unSeparatorIndex].strip()
                if unSimboloCadena:    
                    
                    unSimboloCadenaUnicode = u''
                    try:
                        unSimboloCadenaUnicode = unSimboloCadena.decode( cRawUnicodeEscapeEncoding )
                    except UnicodeDecodeError:
                        unRecord[ 'symbol_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError raw_unicode_escape on symbol in .properties'  
                        
                    if unSimboloCadenaUnicode:
                        unRecord[ 'unicode_default'] = unSimboloCadenaUnicode
                        unSimboloCadenaEncoded  = ''
                        try:
                            unSimboloCadenaEncoded =  aTranslationService.encode( unSimboloCadenaUnicode)      
                        except:
                            unRecord[ 'translation_error'] = 'gvSIGi18n ERROR: aTranslationService EncodingError on symbol in .properties'  
                            
                        if unSimboloCadenaEncoded:    
                        
                            unRecord[ 'string_symbol'] = unSimboloCadenaEncoded
                            unRecord[ 'encoded_default'] = unSimboloCadenaEncoded
                    
                            unaCadenaTraducida  = unaLinea[ unSeparatorIndex + 1:].strip()
                            
                            unaTraduccionEncoded = ''

                            if unaCadenaTraducida:
                                unRecord[ 'raw_translation'] = unaCadenaTraducida
                                
                                unaTraduccionUnicode = u''
                                try:
                                    unaTraduccionUnicode = unaCadenaTraducida.decode( cRawUnicodeEscapeEncoding)
                                except UnicodeDecodeError:
                                    unRecord[ 'translation_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError raw_unicode_escape on translation in .properties'   
                                    
                                if unaTraduccionUnicode:
                                    unRecord[ 'unicode_translation'] = unaTraduccionUnicode
                                    unaTraduccionEncoded  = ''
                                    try:
                                        unaTraduccionEncoded =  aTranslationService.encode( unaTraduccionUnicode)      
                                    except:
                                        unRecord[ 'translation_error'] = 'gvSIGi18n ERROR: aTranslationService EncodingError on translation in .properties'   
                                    if unaTraduccionEncoded:    
                                        unRecord[ 'encoded_translation'] = unaTraduccionEncoded
                            return unRecord           
             
        return None
   
    
    
                    
 

                
                
                
                
                
                
      
                    
             
      
        
            

    security.declarePrivate( 'pScanTranslationsPO')    
    def pScanTranslationsPO( self,
        theParentExecutionRecord =None, 
        theUploadedFile         =None, 
        theZipFile              =None, 
        theUploadedContent       =None,
        theUploadedEntry        =None,
        theAdditionalParams     =None):
                
        unExecutionRecord = self.fStartExecution( 'method',  'pScanTranslationsPO', theParentExecutionRecord, False) 

        try:
                
            if not theUploadedContent or not theUploadedEntry:
                return self
           
            unFileName = theUploadedEntry[ 'file_name']
            if not unFileName:
                return self
            
            unLenguage = theUploadedEntry[ 'language_and_country']
            if not unLenguage:
                return self
            
            unInZip = theUploadedEntry.get( 'in_zip', False)
            if unInZip:
                unContentData = None
                try:
                    if theZipFile:
                        unContentData = theZipFile.read( unFileName)
                except:
                    None
                if not unContentData:
                    return self
                
                unFicheroImportCursor = self.fFicheroImportCursorPO( theUploadedEntry, unContentData)
                if unFicheroImportCursor:
                    if unFicheroImportCursor.get( 'exceeded_max_number_of_lines', False):
                        theUploadedEntry[ 'exceeded_max_number_of_lines'] = True
            else:
                theUploadedFile.seek( 0)
                unContent = theUploadedFile.read()
                if not unContent:
                    return self
                unFicheroImportCursor = self.fFicheroImportCursorPO( theUploadedEntry, unContent)
                if unFicheroImportCursor:
                    if unFicheroImportCursor.get( 'exceeded_max_number_of_lines', False):
                        theUploadedEntry[ 'exceeded_max_number_of_lines'] = True
          
            if not ( unFicheroImportCursor and unFicheroImportCursor[ 'num_lines']):
                return self
            
            unFicheroImportCursor[ 'language'] = theUploadedEntry[ 'language_and_country']
            unFicheroImportCursor[ 'charset']  = theUploadedEntry[ 'charset']
            
            unEsPOTfile = theUploadedEntry[ 'is_pot_file']
 
            unasStringsAndTranslations   = theUploadedContent[ 'strings_and_translations']
            unasStringsAndEncodingErrors = theUploadedContent[ 'strings_with_encoding_errors']
            unasStringsSources           = theUploadedContent[ 'strings_sources']
                        
            unCursorRecord = self.fNextCursorRecordPO( unFicheroImportCursor)
            
            while unCursorRecord:
                unSimbolo = unCursorRecord[ 'string_symbol']
                if unSimbolo:

                    unaEncodedTranslation = ''
                    unTranslationError = ''
                    
                                
                    unSources = unCursorRecord.get( 'sources', '')
                    if unSources:
                        unaStringSources = unasStringsSources.get( unSimbolo, [])
                        if not unaStringSources:
                            unaStringSources = [ unSources, ]
                        else:
                            if not unSources in unaStringSources:
                                unaStringSources.append( unSources)
                                
                        if unaStringSources:
                            unasStringsSources[ unSimbolo] = unaStringSources 
                                
                    
                    if unEsPOTfile:
                        unaEncodedTranslation = unCursorRecord.get( 'encoded_default', '')
                        unTranslationError    = unCursorRecord.get( 'symbol_error', '') or unCursorRecord.get( 'default_error', '')
                    else:
                        unaEncodedTranslation = unCursorRecord.get( 'encoded_translation', '')
                        unTranslationError    = unCursorRecord.get( 'symbol_error', '') or unCursorRecord.get( 'translation_error', '')
                    
                    if unTranslationError:
                        if not unasStringsAndTranslations.has_key( unSimbolo):
                            unasStringTranslations = { }
                            unasStringsAndTranslations[ unSimbolo] = unasStringTranslations
                        if not unasStringsAndEncodingErrors.has_key( unSimbolo):
                            unasStringEncodingErrorLanguages = [ unLenguage, ]
                            unasStringsAndEncodingErrors[ unSimbolo] = unasStringEncodingErrorLanguages
                        else: 
                            unasStringEncodingErrorLanguages = unasStringsAndEncodingErrors[ unSimbolo]
                            if not ( unLenguage in unasStringEncodingErrorLanguages):
                                unasStringEncodingErrorLanguages.append( unLenguage)

                    else:
                        unasStringTranslations = unasStringsAndTranslations.get( unSimbolo, None)
                        if unasStringTranslations == None:
                            unasStringTranslations = { }
                            unasStringsAndTranslations[ unSimbolo] = unasStringTranslations
                        if unaEncodedTranslation:
                            unasStringTranslations[ unLenguage] = unaEncodedTranslation
                         
                        
                unCursorRecord = self.fNextCursorRecordPO( unFicheroImportCursor)
                 
            return self
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

                                           
                
                  

   
    
    security.declarePrivate( 'fFicheroImportCursorPO')    
    def fFicheroImportCursorPO( self, theUploadedEntry, theContent):
        if not theContent:
            return None
        
        unCursor = self.fNewVoidImportCursor()
        unCursor[ 'file_kind'] = cPOFilePostfix
        
        aTranslationService = getToolByName( self, 'translation_service', None)
        unCursor[ 'translation_service'] = aTranslationService
 
        someLines = theContent.splitlines()
        unCursor[ 'content_lines']  = someLines
        
        unNumLines = len( someLines)
       
        unMaximoLineas = self.fMaximoLineasAImportarPO()
        if unNumLines > unMaximoLineas:
            unNumLines = unMaximoLineas
            unCursor[ 'content_lines']  = someLines[:unMaximoLineas + cPOMaxLinesToScanTryingToGetCadena]
            unCursor[ 'exceeded_max_number_of_lines'] = True
 
        unCursor[ 'num_lines']      = unNumLines
        unCursor[ 'next_line_index'] = 0
                
        if unNumLines < 1:
            unCursor[ 'error'] = "gvSIGi18n_NoContentLines_error_msgid"
            unCursor[ 'error_detail'] = theFileName                    
            return None

        
        unLastHeaderLineIndex = theUploadedEntry.get( 'last_header_line_number', -1)
        unCursor[ 'next_line_index'] = unLastHeaderLineIndex
               
        unCursor[ 'num_possible_records'] = unNumLines / 5
        
        if unCursor[ 'next_line_index'] >= unCursor[ 'num_lines']:
            return None
        
        return unCursor
           

    
    
    
    
    
    
   
    security.declarePrivate( 'fNextCursorRecordPO')    
    def fNextCursorRecordPO( self, theCursor):
        if not theCursor:
            return None
        
        aTranslationService = theCursor[ 'translation_service']
        if not aTranslationService:
            return None
        

        if not theCursor[ 'file_kind'] == cPOFilePostfix:
            return None
            
        unosDatosCadenaActual = {}
        unNumeroLineasIntentadas = 0

        unMaxNumeroLineas = self.fMaximoLineasAImportarPO() + cPOMaxLinesToScanTryingToGetCadena
        
        while True:
            unNextLineIndex = theCursor[ 'next_line_index']
            if ( unNextLineIndex >= theCursor[ 'num_lines']) or ( unNextLineIndex >= unMaxNumeroLineas) or ( unNumeroLineasIntentadas >= cPOMaxLinesToScanTryingToGetCadena):
                return None
            
            theCursor[ 'next_line_index'] += 1
            unaLinea = theCursor[ 'content_lines'][ unNextLineIndex].strip()
            if not unaLinea:
                unosDatosCadenaActual = {}
                continue
        
            if unaLinea.startswith( cTranslationEntryDefaultPrefix):
                unDefaultString = unaLinea[ len( cTranslationEntryDefaultPrefix):].replace( '"', '').strip()
                unDefaultString = unDefaultString.replace( '"', '').strip()
                
                unDefaultEncoded = ''
                if unDefaultString:
                    unImportedCharSet = theCursor[ 'charset']
                    if not unImportedCharSet:
                        unImportedCharSet = 'utf-8'
                        
                    unDefaultUnicode = u''
                    try:
                        unDefaultUnicode = unDefaultString.decode( unImportedCharSet)
                    except UnicodeDecodeError:
                        unosDatosCadenaActual[ 'default_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .PO' % unImportedCharSet  
                    if unDefaultUnicode:
                        unosDatosCadenaActual[ 'unicode_default'] = unDefaultUnicode
                        unDefaultEncoded  = ''
                        try:
                            unDefaultEncoded =  aTranslationService.encode( unDefaultUnicode)      
                        except:
                            unosDatosCadenaActual[ 'default_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .PO'   
                        if unDefaultEncoded:    
                            unosDatosCadenaActual[ 'encoded_default'] = unDefaultEncoded
                continue   
            
            
            elif unaLinea.startswith( cTranslationEntrySourcesPrefix):
                if unosDatosCadenaActual:
                    unosDatosCadenaActual[ 'sources'] = unaLinea[ len( cTranslationEntrySourcesPrefix):].replace( '"', '').strip()
                continue    
            
            
            elif unaLinea.startswith( cTranslationEntryFlagsPrefix):
                if unosDatosCadenaActual:
                    unosDatosCadenaActual[ 'flags'] = unaLinea[ len( cTranslationEntrySourcesPrefix):].replace( '"', '').strip()
                continue    
            
            
            
            elif unaLinea.startswith( cPOTranslationEntryMsgidPrefix):
                unMsgidString = unaLinea[ len( cPOTranslationEntryMsgidPrefix):].replace( '"', '').strip()
                unMsgidString = unMsgidString.replace( '"', '').strip()
                if unMsgidString:
                    
                    unImportedCharSet = theCursor[ 'charset']
                    if not unImportedCharSet:
                        unImportedCharSet = 'utf-8'
                    unMsgidCharset = unImportedCharSet 
                    
                    unMsgidStringUnicode = u''
                    try:
                        unMsgidStringUnicode = unMsgidString.decode( unMsgidCharset )
                    except UnicodeDecodeError:
                        unRecord[ 'symbol_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .PO' % unMsgidCharset   
                    if unMsgidStringUnicode:
                        unosDatosCadenaActual[ 'unicode_symbol'] = unMsgidStringUnicode
                        unMsgidStringEncoded  = ''
                        try:
                            unMsgidStringEncoded =  aTranslationService.encode( unMsgidStringUnicode)      
                        except:
                            unRecord[ 'symbol_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .PO'   
       
                        if unMsgidStringEncoded:    
                            unosDatosCadenaActual[ 'encoded_symbol'] = unMsgidStringEncoded
                continue    
            
            
            
            elif unaLinea.startswith( cPOTranslationEntryMsgstrPrefix):
                if unosDatosCadenaActual:
                    if not unosDatosCadenaActual.get( 'encoded_symbol', ''):
                        unosDatosCadenaActual = {}
                    else:
                        unMsgstrString = unaLinea[ len( cPOTranslationEntryMsgstrPrefix):].replace( '"', '').strip()
                        unosDatosCadenaActual[ 'msgstr'] = unMsgstrString
    
                        unRecord = self.fNewVoidCursorRecord()
                        
                        unRecord[ 'string_symbol']      = unosDatosCadenaActual.get( 'encoded_symbol', '')
                        unRecord[ 'symbol_error']       = unosDatosCadenaActual.get( 'symbol_error', '')
                        unRecord[ 'unicode_default']    = unosDatosCadenaActual.get( 'unicode_default', u'')
                        unRecord[ 'encoded_default']    = unosDatosCadenaActual.get( 'encoded_default', '')
                        if not unRecord[ 'encoded_default']:
                            unRecord[ 'unicode_default'] = unosDatosCadenaActual.get( 'unicode_symbol', '')
                            unRecord[ 'encoded_default'] = unosDatosCadenaActual.get( 'encoded_symbol', '')
                        unRecord[ 'default_error']      = unosDatosCadenaActual.get( 'default_error', '')
                        unRecord[ 'sources']            = unosDatosCadenaActual.get( 'sources', '')
                        
                        unaTraduccionEncoded = ''
                        if unMsgstrString:
                            unImportedCharSet= theCursor[ 'charset']
                            if not unImportedCharSet:
                                unImportedCharSet = 'utf-8'
                            
                            unaTraduccionUnicode = u''
                            try:
                                unaTraduccionUnicode = unMsgstrString.decode( unImportedCharSet)
                            except UnicodeDecodeError:
                                unRecord[ 'translation_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .PO' % unImportedCharSet  
                            if unaTraduccionUnicode:
                                unRecord[ 'unicode_translation'] = unaTraduccionUnicode
                                unaTraduccionEncoded  = ''
                                try:
                                    unaTraduccionEncoded =  aTranslationService.encode( unaTraduccionUnicode)      
                                except:
                                    unRecord[ 'translation_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .PO'   
                                if unaTraduccionEncoded:    
                                    unRecord[ 'encoded_translation'] = unaTraduccionEncoded
                        return unRecord    
                    
                    
            elif unaLinea.startswith( cTranslationEntryCommentPrefix):
                if unosDatosCadenaActual:
                    unosDatosCadenaActual[ 'comment'] = unaLinea[ len( cTranslationEntrySourcesPrefix):].replace( '"', '').strip()
                continue    
                

        return None
   
    
    
                    
 

                
                
                
                
                 
                
                
                    
       
    
                
    security.declarePrivate( 'fCombinedContenidosIntercambio')    
    def fCombinedContenidosIntercambio( self, theParentExecutionRecord=None):
        
        if cLogEachExecution_fCombinedContenidosIntercambio:
            unExecutionRecord = self.fStartExecution( 'method',  'fCombinedContenidosIntercambio', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }) 
        else:
            unExecutionRecord = self.fStartExecution( 'method',  'fCombinedContenidosIntercambio', theParentExecutionRecord,  False) 
        
        try:
            
            unCombinedContenidos = self.fNewVoidCombinedContent()
            
            unosCombinedLanguages                      = set()
            unosCombinedModules                        = set()        
            unasCombinedStringsModulesAndTranslations  = unCombinedContenidos[ 'strings_modules_and_translations']
      
            unosContenidosIntercambio = self.fObtenerTodosContenidosIntercambioNoExcluidos()
            
            if not unosContenidosIntercambio:
                return unCombinedContenidos
            
            for unContenidoIntercambio in unosContenidosIntercambio:
                
                unNombreModulo = unContenidoIntercambio.getNombreModulo()
                unosCombinedModules.add( unNombreModulo)
                    
                unContenido = unContenidoIntercambio.fContenido( 
                    theParentExecutionRecord= unExecutionRecord
                )
                
                if unContenido:
                    unosLenguages = unContenido[ 'languages']
                    
                    unosCombinedLanguages.update( unosLenguages)
                    
                    unasStringsAndEncodingErrors = unContenido[ 'strings_with_encoding_errors']
                    unasStringsAndTranslations   = unContenido[ 'strings_and_translations']
                    unasStringsSources           = unContenido[ 'strings_sources']
                    
                    if unasStringsAndTranslations:
                    
                        unasStrings = unasStringsAndTranslations.keys()
                       
                        for unaString in unasStrings:
                            if not unasCombinedStringsModulesAndTranslations.has_key( unaString):
                                unaCombinedStringModulesAndTranslations = { 'modules': set(), 'translations': {}, 'encoding_errors': set(), 'sources': [], 'translations_flags': {}, 'translations_comments': {},}
                                unasCombinedStringsModulesAndTranslations[ unaString] = unaCombinedStringModulesAndTranslations
                            else: 
                                unaCombinedStringModulesAndTranslations = unasCombinedStringsModulesAndTranslations[ unaString]
                                
                            unasStringTranslations   = unasStringsAndTranslations[ unaString]
                            unosStringEncodingErrors = unasStringsAndEncodingErrors.get( unaString, [])
    
                            unosLenguagesInString = unasStringTranslations.keys()
                            unosCombinedLanguages.update( unosLenguagesInString)
                            
                            for unLenguage in unosLenguagesInString:
                                     
                                if ( unLenguage in unosStringEncodingErrors):
                                    unaCombinedStringModulesAndTranslations[ 'encoding_errors'].add( unLenguage)    
                                else:
                                    unaTraduccion =  unasStringTranslations.get( unLenguage, '')
                                    if unaTraduccion:
                                        unaCombinedStringModulesAndTranslations[ 'translations'][ unLenguage] = unaTraduccion    
                                        
                                        
                                    
                            unaCombinedStringModulesAndTranslations[ 'modules'].add( unNombreModulo)   
                            
                            unSources = unasStringsSources.get( unaString, [])
                            if unSources:
                                unaStringSources = unaCombinedStringModulesAndTranslations.get( 'sources', [])
                                if not unaStringSources:
                                    unaStringSources = unSources
                                else:
                                    for unSource in unSources:
                                        if not unSource in unaStringSources:
                                            unaStringSources.append( unSource)
                                        
                                if unaStringSources:
                                    unaCombinedStringModulesAndTranslations[ 'sources'] = unaStringSources 
                                    
            unCombinedContenidos[ 'languages'] = sorted( unosCombinedLanguages)
            unCombinedContenidos[ 'modules']   = sorted( unosCombinedModules)
                         
            return unCombinedContenidos
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            if cLogEachExecution_fCombinedContenidosIntercambio:
                unExecutionRecord and unExecutionRecord.pClearLoggedAll()

                                           
                                

    
    
    
    
    
    
    security.declareProtected( permissions.View, 'fInformeContenidosImportacion')    
    def fInformeContenidosImportacion( self, theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fInformeContenidosImportacion', theParentExecutionRecord,  False, ) 
        
        try:
            
            unInforme = self.fNewVoidContenidoIntercambioReport()
            
            unInforme[ 'language_names_and_flags'] = self.fLanguagesNamesAndFlagsPorCodigo() 

            unContenido = self.fCombinedContenidosIntercambio( unExecutionRecord)
            if not unContenido:
                return unInforme
            
            unasStringsModulesAndTranslations = unContenido[ 'strings_modules_and_translations']
            if not unasStringsModulesAndTranslations:
                return unInforme
            
            unasStrings = unasStringsModulesAndTranslations.keys()
            unNumStrings = len( unasStrings)
            unInforme[ 'num_strings'] = unNumStrings
           
            unosNumTranslationsByLanguage = unInforme[ 'num_translated_by_language']
            unosNumEncodingErrorsByLanguage = unInforme[ 'num_encoding_errors_by_language']
            for unLanguage in unContenido[ 'languages']:
                unosNumTranslationsByLanguage[ unLanguage] = 0    
                unosNumEncodingErrorsByLanguage[ unLanguage] = 0    
    
            for unaString in unasStrings:
                unasTranslations               = unasStringsModulesAndTranslations[ unaString][ 'translations']
                unosLenguagesConEncodingErrors = unasStringsModulesAndTranslations[ unaString][ 'encoding_errors']
                unosLenguages = unasTranslations.keys()
                for unLenguage in unosLenguages:
                    if (not unLenguage in unosLenguagesConEncodingErrors):
                        unosNumTranslationsByLanguage[ unLenguage] = unosNumTranslationsByLanguage.get( unLenguage, 0) + 1  
                    else:
                        unosNumEncodingErrorsByLanguage[ unLanguage] = unosNumEncodingErrorsByLanguage.get( unLenguage, 0) + 1
                        
            unosLenguages =  sorted( unosNumTranslationsByLanguage.keys())
            unInforme[ 'languages'] = unosLenguages
            
            for unLenguage in unosLenguages:
                unNumeroTraducciones = unosNumTranslationsByLanguage[ unLenguage]
                if not unNumeroTraducciones:
                    unPercentPending     = 100
                    unPercentTranslated  = 0
                    unPercentEncodingErrors = 0
                else:
                    unPercentTranslated = int( ( ( 0.0 + unNumeroTraducciones) / unNumStrings) * 100)
                    if not unPercentTranslated:
                        unPercentTranslated = 1
                    unPercentPending = 100 - unPercentTranslated
                    unPercentEncodingErrors = int( ( ( 0.0 + unosNumEncodingErrorsByLanguage[ unLenguage]) / unNumStrings) * 100)
                    
                unInforme[ 'num_pending_by_language'][        unLenguage] = unNumStrings - unNumeroTraducciones
                unInforme[ 'percent_pending_by_language'][    unLenguage] = unPercentPending
                unInforme[ 'percent_translated_by_language'][ unLenguage] = unPercentTranslated
                unInforme[ 'num_encoding_errors_by_language'][unLenguage] = unosNumEncodingErrorsByLanguage[ unLenguage]
                unInforme[ 'percent_encoding_errors_by_language'][ unLenguage] = unPercentEncodingErrors
                
            return unInforme
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

              
                
                    
            
            
     
    
    
    
    
    security.declareProtected( permissions.AddPortalContent, 'fImportarContenidosIntercambio')    
    def fImportarContenidosIntercambio( self, 
        theJustEstimateCost      =True, 
        theIsToCreateCadenas     =False,
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):
        
  
        unExecutionRecord = self.fStartExecution( 'method',  'fImportarContenidosIntercambio', theParentExecutionRecord, False) 

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators  import ModelDDvlPloneTool_Mutators, cModificationKind_CreateSubElement, cModificationKind_Create, cModificationKind_ChangeValues
        from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fDateTimeNow
        
        try:

            unSubExecutionRecord = self.fStartExecution( 'block',  'fImportarContenidosIntercambio-SubExecution to retrieve TRACatalog and accessible languages and modules', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
            
            unAlInicio_PermiteModificar = False
            unCambiado_PermiteModificar = False
            
            try:
                
                unInformeImportarContenidos = self.fNewVoidInformeImportarContenidos()
                
                unCrearInformeAntes   = self.getCrearInformeAntes()
                unCrearInformeDespues = self.getCrearInformeDespues()
                
                unInformeImportarContenidos[ 'start_date'] =self.fDateTimeNowTextual()
                
                unCatalogo = self.getCatalogo()
                if not unCatalogo:
                    unInformeImportarContenidos[ 'end_date'] =self.fDateTimeNowTextual()
                    return unInformeImportarContenidos
                
                unAlInicio_PermiteModificar =  unCatalogo.getPermiteModificar( )
                unCambiado_PermiteModificar = False
                
                if not theJustEstimateCost:
                    if unAlInicio_PermiteModificar:
                        
                        unCatalogo.setPermiteModificar( False)
                        unCambiado_PermiteModificar = True
                        
                        
                        aModelDDvlPloneTool_Mutators = ModelDDvlPloneTool_Mutators()
                        
                        aSetPermiteModificarChangeReport = aModelDDvlPloneTool_Mutators.fNewVoidChangeValuesReport()
                        
                        someFieldReports    = aSetPermiteModificarChangeReport.get( 'field_reports')
                        aFieldReportsByName = aSetPermiteModificarChangeReport.get( 'field_reports_by_name')
                                                
                        aReportForField = { 'attribute_name': 'permiteModificar',  'effect': 'changed', 'new_value': False, 'previous_value': True,}
                        someFieldReports.append( aReportForField)            
                        aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                        
                        aModelDDvlPloneTool_Mutators.pSetAudit_Modification( unCatalogo, cModificationKind_ChangeValues, aSetPermiteModificarChangeReport)       
                        
                        unCatalogo.pFlushCachedTemplates_All()
                        
                        transaction.commit( )            
                        logging.getLogger( 'gvSIGi18n::Importar').info("COMMIT at the begining to change translations catalog allow write flag to False")        
                
                try:
                     
                    if not self.fNoHaComenzadoOEnDevelopmentODebug():
                        unInformeImportarContenidos[ 'error'] = "gvSIGi18n_ImportAlreadyStarted_error_msgid"
                        unInformeImportarContenidos[ 'end_date'] = fDateTimeNow()
                        return unInformeImportarContenidos
            
                      
                    unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                    unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                        
                    aUseCaseNameToAssess = cUseCase_ImportTRAImportacion
                    if theIsToCreateCadenas:
                        aUseCaseNameToAssess  = cUseCase_ImportTRAImportacion_ToCreateCadenas
                    
                    unUseCaseQueryResult = self.fUseCaseAssessment(  
                        theUseCaseName          = aUseCaseNameToAssess, 
                        theElementsBindings     = { cBoundObject: self,}, 
                        theRulesToCollect       = ['languages', 'modules',], 
                        thePredicateOverrides   = { self.getCatalogo().UID(): { 'fAllowWrite': True, }, },
                        thePermissionsCache     = unPermissionsCache, 
                        theRolesCache           = unRolesCache, 
                        theParentExecutionRecord= unExecutionRecord
                    )
                                    
                                    
                    if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                        unInformeImportarContenidos[ 'error'] = "gvSIGi18n_NoPermission_error_msgid"
                        unInformeImportarContenidos[ 'end_date'] =self.fDateTimeNowTextual()
                        return unInformeImportarContenidos
                                    
                    unosIdiomasAccesibles = unUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'languages', {}).get( 'accepted_final_objects', [])
                    unosModulosAccesibles = unUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'modules', {}).get( 'accepted_final_objects', [])
            
    
                    unDebeCrearTraduccionesQueFaltan = self.getDebeCrearTraduccionesQueFaltan()
                    
                    unUseCaseQueryResult_CrearTraduccionesQueFaltan = None
                    if unDebeCrearTraduccionesQueFaltan:
                        unUseCaseQueryResult_CrearTraduccionesQueFaltan = self.fUseCaseAssessment(  
                            theUseCaseName          = cUseCase_CreateMissingTRATraduccion, 
                            theElementsBindings     = { cBoundObject: self,}, 
                            theRulesToCollect       = None, 
                            thePredicateOverrides   = { self.getCatalogo().UID(): { 'fAllowWrite': True, }, },
                            thePermissionsCache     = unPermissionsCache, 
                            theRolesCache           = unRolesCache, 
                            theParentExecutionRecord= unExecutionRecord
                        )
                        
                        
                finally:
                    unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                    unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
                    
              
                     
                unSubExecutionRecord = self.fStartExecution( 'block',  'fImportarContenidosIntercambio-SubExecution to retrieve translations interchange contents', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
                try:
                    unContenido = self.fCombinedContenidosIntercambio( 
                        theParentExecutionRecord= unExecutionRecord
                    )
                    if not unContenido:
                        unInformeImportarContenidos[ 'end_date'] =self.fDateTimeNowTextual()
                        return unInformeImportarContenidos
                    
                finally:
                    unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                    unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
                    
              
                unSubExecutionRecord = self.fStartExecution( 'block',  'fImportarContenidosIntercambio-SubExecution to create status report before import and to set the first import progress report.', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
                try:
                 
                    unaColeccionCadenas = unCatalogo.fObtenerColeccionCadenas()
                    if ( unaColeccionCadenas == None):
                        unInformeImportarContenidos[ 'end_date'] =self.fDateTimeNowTextual()
                        return unInformeImportarContenidos
            
            
            
                    unMemberId = self.fGetMemberId()
                    unIdNumber = unCatalogo.getHighestCadenaIdNumber()
                    unIdNumberHolder = [ unIdNumber, ]
                    
                    aPloneUtilsTool = self.getPloneUtilsToolForNormalizeString()  
                           
                    unAhora = fDateTimeNow()
                    
                    unInformeImportarContenidos[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
    
                    if not theJustEstimateCost:
                                                
                        self.setHaComenzado( True)
                        self.setEstadoProceso( 'Activo')
                        self.setUsuarioImportador( unMemberId)
                        self.setFechaComienzoProceso( unAhora)
                        self.setHaCompletadoConExito( False)
                        
                        self.setInformeProgreso( str( unInformeImportarContenidos))
                        self.setFechaUltimoInformeProgreso( unAhora)
                        self.setFechaFinProceso( None)
                        self.setInformeFinal(    '')
                        self.setInformeExcepcion(    '')

                        unCatalogo.setUltimaImportacion( self)
                        
                        self.pEliminarInformesEstado( 
                            unUseCaseQueryResult, 
                            False, 
                            thePermissionsCache=unPermissionsCache, 
                            theRolesCache=unRolesCache, 
                            theParentExecutionRecord=unExecutionRecord
                        )
                    
                        transaction.commit( )
                        logging.getLogger( 'gvSIGi18n::Importar').info("COMMIT after initial setup, and eliminating status reports already existing in the import %s" , self.Title()) 
                         
                        if unCrearInformeAntes:
                            self.pCrearInformeEstado( 
                                'antes', 
                                unUseCaseQueryResult, 
                                False, 
                                thePermissionsCache=unPermissionsCache, 
                                theRolesCache=unRolesCache, 
                                theParentExecutionRecord=unExecutionRecord
                            )
            
                            transaction.commit( )
                            logging.getLogger( 'gvSIGi18n::Importar').info("COMMIT INITIAL report")        

                       
                        
                        aModelDDvlPloneTool_Mutators = ModelDDvlPloneTool_Mutators()
                        
                         
                        aImportStatusChangeReport = aModelDDvlPloneTool_Mutators.fNewVoidChangeValuesReport()
                        
                        someFieldReports    = aImportStatusChangeReport.get( 'field_reports')
                        aFieldReportsByName = aImportStatusChangeReport.get( 'field_reports_by_name')
                                                
                        aReportForField = { 'attribute_name': 'haComenzado',  'effect': 'changed', 'new_value': True, 'previous_value': False,}
                        someFieldReports.append( aReportForField)            
                        aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                                                
                        aReportForField = { 'attribute_name': 'estadoProceso',  'effect': 'changed', 'new_value': 'Activo', 'previous_value': 'Inactivo',}
                        someFieldReports.append( aReportForField)            
                        aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                        
                        aReportForField = { 'attribute_name': 'usuarioImportador',  'effect': 'changed', 'new_value': unMemberId, 'previous_value': None,}
                        someFieldReports.append( aReportForField)            
                        aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                                                
                        aReportForField = { 'attribute_name': 'fechaComienzoProceso',  'effect': 'changed', 'new_value': unAhora, 'previous_value': None,}
                        someFieldReports.append( aReportForField)            
                        aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                                                
                        aReportForField = { 'attribute_name': 'haCompletadoConExito',  'effect': 'changed', 'new_value': False, 'previous_value': False,}
                        someFieldReports.append( aReportForField)            
                        aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                        
                        aModelDDvlPloneTool_Mutators.pSetAudit_Modification( self, cModificationKind_ChangeValues, aImportStatusChangeReport)       
                    
                        transaction.commit( )
            
                        logging.getLogger( 'gvSIGi18n::Importar').info("COMMIT audit modification record.") 
                    
                        
                        unCatalogo.pFlushCachedTemplates_All()
                        
                finally:
                    unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                    unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
                    
                unaExceptionInfo = None
                try:
                    try:
                        self.pImportarContenidosIntercambio( 
                            theJustEstimateCost         =theJustEstimateCost,
                            theCatalogo                 =unCatalogo, 
                            theUseCaseQueryResult       =unUseCaseQueryResult, 
                            theUseCaseQueryResult_CrearTraduccionesQueFaltan=unUseCaseQueryResult_CrearTraduccionesQueFaltan,
                            theIdiomasAccesibles        =unosIdiomasAccesibles, 
                            theModulosAccesibles        =unosModulosAccesibles, 
                            theColeccionCadenas         =unaColeccionCadenas, 
                            theIdNumberHolder           =unIdNumberHolder, 
                            theMemberId                 =unMemberId, 
                            theContenido                =unContenido, 
                            theInformeImportarContenidos=unInformeImportarContenidos, 
                            thePloneUtilsTool           =aPloneUtilsTool,
                            thePermissionsCache         =unPermissionsCache, 
                            theRolesCache               =unRolesCache, 
                            theParentExecutionRecord    =unExecutionRecord,
                        )
                    except:
                        unaExceptionInfo = sys.exc_info()
                        unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                        
                        unInformeExcepcion = 'Exception during Import operation\n' 
                        unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                        unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                        unInformeExcepcion += unaExceptionFormattedTraceback   
                        
                        unaFechaString =self.fDateTimeNowTextual()
                        unInformeImportarContenidos[ 'fecha_informe'] = unaFechaString
                        unInformeImportarContenidos[ 'end_date']      = unaFechaString
                        unInformeImportarContenidos[ 'valid'] = False
                        unInformeImportarContenidos[ 'error'] = 'exception'
                        unInformeImportarContenidos[ 'error_detail'] = unInformeExcepcion
    
                        unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
                        
                        if not theJustEstimateCost:
                            self.setInformeFinal(      str( unInformeImportarContenidos))
                            self.setInformeExcepcion(  unInformeExcepcion)
                            
                            unCatalogo.pFlushCachedTemplates_All()                            
                        
                            transaction.commit( )
                            logging.getLogger( 'gvSIGi18n::Importar').info("COMMIT ON EXCEPTION changes") 
                        
                        logging.getLogger( 'gvSIGi18n::Importar').info("EXCEPTION: exception details follow:\n%s\n" % unInformeExcepcion) 
                                
                        return unInformeImportarContenidos
                                
                    
                    
                finally:
                    
                    unSubExecutionRecord = self.fStartExecution( 'block',  'fImportarContenidosIntercambio-SubExecution to create status report after import and to clear the import progress report.', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
                    try:
                        if not theJustEstimateCost:

                            unCatalogo.pFlushCachedTemplates_All()                            
                            
                            transaction.commit( )
                        
                            logging.getLogger( 'gvSIGi18n::Importar').info("COMMIT FINAL changes")        
            
                        unAhora = fDateTimeNow()
                        
                        unInformeImportarContenidos[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                        unInformeImportarContenidos[ 'end_date']      = self.fDateToStoreString( unAhora)
                        
                        if not theJustEstimateCost:
                            
                            if unaExceptionInfo:
                                self.setHaCompletadoConExito( False)
                            else:
                                self.setHaCompletadoConExito( True)
                            
                        
                            self.setEstadoProceso(  'Inactivo')
                            self.setInformeFinal(    str( unInformeImportarContenidos))
                            self.setFechaFinProceso( unAhora)
                            self.setInformeProgreso( '')
                            self.setFechaUltimoInformeProgreso( None)                
                    
                            transaction.commit( )
                            logging.getLogger( 'gvSIGi18n::Importar').info("COMMIT import status as finished.")        
                            
                            aModelDDvlPloneTool_Mutators = ModelDDvlPloneTool_Mutators()
                            
                              
                            
                            
                            aImportStatusChangeReport = aModelDDvlPloneTool_Mutators.fNewVoidChangeValuesReport()
                            
                            someFieldReports    = aImportStatusChangeReport.get( 'field_reports')
                            aFieldReportsByName = aImportStatusChangeReport.get( 'field_reports_by_name')
                                                    
                            aReportForField = { 'attribute_name': 'estadoProceso',  'effect': 'changed', 'new_value': 'Inactivo', 'previous_value': 'Activo',}
                            someFieldReports.append( aReportForField)            
                            aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                                                     
                            aReportForField = { 'attribute_name': 'haCompletadoConExito',  'effect': 'changed', 'new_value': True, 'previous_value': False,}
                            someFieldReports.append( aReportForField)            
                            aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                            
                            aModelDDvlPloneTool_Mutators.pSetAudit_Modification( self, cModificationKind_ChangeValues, aImportStatusChangeReport)       
                                                                                
                            transaction.commit( )
                            logging.getLogger( 'gvSIGi18n::Importar').info("COMMIT FINAL audit modification record.")        
                         
                            if unCrearInformeDespues:
                                self.pCrearInformeEstado( 
                                    'despues', 
                                    unUseCaseQueryResult, 
                                    False, 
                                    thePermissionsCache=unPermissionsCache, 
                                    theRolesCache=unRolesCache, 
                                    theParentExecutionRecord=unExecutionRecord
                                )                                                        
                            
                                transaction.commit( )
                                logging.getLogger( 'gvSIGi18n::Importar').info("COMMIT FINAL report")        

                            unCatalogo.pFlushCachedTemplates_All()
            
                        if not theJustEstimateCost:
                            unCatalogo.pInvalidateSimbolosCadenasOrdenados()  
                            
                            unCatalogo.pFlushCachedTemplates_All()                            
                            
                            transaction.commit( )            
                            logging.getLogger( 'gvSIGi18n::Importar').info("COMMIT pInvalidateSimbolosCadenasOrdenados")        
            
                        unInformeImportarContenidos[ 'end_date'] =self.fDateTimeNowTextual()
                        
                        return unInformeImportarContenidos
                    
                    finally:
                        unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                        unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
                        
            finally:
                
                if not theJustEstimateCost:
                    unaColeccionImportaciones = self.getContenedor()
                    if unaColeccionImportaciones:
                        
                        unasImportaciones = unaColeccionImportaciones.objectValues( 'TRAImportacion')
                        
                        unaSiguienteImportacionAEjecutar = None
                        
                        for unaSiguienteImportacion in unasImportaciones:
                            
                            if ( not unaSiguienteImportacion == self):
                                if ( not unaSiguienteImportacion.getHaComenzado()) and unaSiguienteImportacion.getComenzarAlFinalizarAnterior():
                                    unaSiguienteImportacionAEjecutar = unaSiguienteImportacion
                                    break
                        
                        if unaSiguienteImportacionAEjecutar:
                            unaSiguienteImportacionAEjecutar.fImportarContenidosIntercambio( 
                                theJustEstimateCost      =theJustEstimateCost, 
                                theIsToCreateCadenas     =theIsToCreateCadenas,
                                thePermissionsCache      =thePermissionsCache, 
                                theRolesCache            =theRolesCache, 
                                theParentExecutionRecord =unExecutionRecord
                            )

                
                            

                if not theJustEstimateCost:
                    if unCambiado_PermiteModificar:
                        unCatalogo.setPermiteModificar( unAlInicio_PermiteModificar)
                        
                        
                        
                        aModelDDvlPloneTool_Mutators = ModelDDvlPloneTool_Mutators()
                        
                        aSetPermiteModificarChangeReport = aModelDDvlPloneTool_Mutators.fNewVoidChangeValuesReport()
                        
                        someFieldReports    = aSetPermiteModificarChangeReport.get( 'field_reports')
                        aFieldReportsByName = aSetPermiteModificarChangeReport.get( 'field_reports_by_name')
                        
                        aSetPermiteModificarChangeReport.update( { 'effect': 'changed', 'new_object_result': None, })
                        
                        aReportForField = { 'attribute_name': 'permiteModificar',   'effect': 'changed', 'new_value': unAlInicio_PermiteModificar, 'previous_value': not unAlInicio_PermiteModificar,}
                        someFieldReports.append( aReportForField)            
                        aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                        
                        aModelDDvlPloneTool_Mutators.pSetAudit_Modification( unCatalogo, cModificationKind_ChangeValues, aSetPermiteModificarChangeReport)       
                        
                        unCatalogo.pFlushCachedTemplates_All()
                        
                        transaction.commit( )            
                        logging.getLogger( 'gvSIGi18n::Importar').info("COMMIT at the end to change translations catalog allow write flag to %s" % str( unAlInicio_PermiteModificar))        
    
                        
 
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
     
    
                
                
        
       
        
        
        
        
        
        
        
        
        
        
        
        
# ###################################################################
#   IMPORT PROCESS
#
                
                
    
    security.declarePrivate( 'pImportarContenidosIntercambio')    
    def pImportarContenidosIntercambio( self, 
        theJustEstimateCost,
        theCatalogo, 
        theUseCaseQueryResult, 
        theUseCaseQueryResult_CrearTraduccionesQueFaltan,
        theIdiomasAccesibles, 
        theModulosAccesibles, 
        theColeccionCadenas, 
        theIdNumberHolder, 
        theMemberId, 
        theContenido, 
        theInformeImportarContenidos, 
        thePloneUtilsTool,
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):
        """Import translations.
        
        Main loops to create languages, modules, strings and translations.
        
        """
        unExecutionRecord = self.fStartExecution( 'method',  'pImportarContenidosIntercambio', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }) 

        from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fMillisecondsNow        
        from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fDateTimeNow

        try:
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                
                
            if not theUseCaseQueryResult or not theUseCaseQueryResult.get( 'success', False):
                return self    
    
            if not theCatalogo or not theContenido or not theInformeImportarContenidos:
                return self
            
            unSubExecutionRecord = self.fStartExecution( 'block',  'pImportarContenidosIntercambio-SubExecution to determine elements to create (languages, modules, strings) and count the number of translations to process.', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
            try:
            
                unCurrentChangesHolder = [ 0, 0, 0, ] # Changes since last commit, changes since last log, 
                unaEsperaEntreTransaccionesEnSegundos = self.getEsperaEntreTransaccionesEnSegundos()
                unIntervaloRefrescoEnMinutos          = self.getIntervaloRefrescoEnMinutos()
                unIntervaloRefrescoEnNumeroEscrituras = self.getIntervaloRefrescoEnNumeroEscrituras()
                unaEsperaEntreTransaccionesEnSegundos = self.getEsperaEntreTransaccionesEnSegundos()
                unCurrentCommitsHolder = [ 0,]
                unNumeroDeRefrescosPorEscrituraEnLog  = self.getNumeroDeRefrescosPorEscrituraEnLog()
                
                unNumeroOperacionesAntesDeCederProcesador   = self.getNumeroOperacionesAntesDeCederProcesador()
                unaEsperaTrasOperacionesEnSegundos          = self.getEsperaTrasOperacionesEnSegundos()
                unPeriodoActividadSinEsperaEnMilisegundos   = self.getPeriodoActividadSinEsperaEnMilisegundos()
                
                unMillisecondsFinUltimaEspera               = fMillisecondsNow()           
                unOperationsDoneTrasUltimaEspera            = 0
                
                
                unaFechaUltimoInformeProgresoHolder   = [ self.getFechaUltimoInformeProgreso(), ]
    

                # ######################################################
                """Determine Modules to Create.
                
                """
                todosModulos  = theCatalogo.fObtenerTodosModulos()
                
                todosNombresModulos          = [ unModulo.Title() for unModulo in todosModulos]
                unosNombresModulosAccesibles = [ unModulo.Title() for unModulo in theModulosAccesibles] 
                
                unosNombresModulosAIgnorar = []
                unosNombresModulosACrear   = []
                
                unosNombresModulos = theContenido[ 'modules']
              
                for unNombreModulo in unosNombresModulos:
                    if unNombreModulo:
                        if unNombreModulo in todosNombresModulos:
                            if not ( unNombreModulo in unosNombresModulosAccesibles):
                                unosNombresModulosAIgnorar.append( unNombreModulo)   
                        else:
                            unosNombresModulosACrear.append( unNombreModulo)
                        
                theInformeImportarContenidos[ 'modules_to_create'] = len( unosNombresModulosACrear)
                theInformeImportarContenidos[ 'expected_operations'] += len( unosNombresModulosACrear)
        
        
                # ######################################################
                """Determine Languages to Create.
                
                """
                todosIdiomas                 = theCatalogo.fObtenerTodosIdiomas()
                todosCodigosIdiomas          = [ unIdioma.getCodigoIdiomaEnGvSIG() for unIdioma in todosIdiomas]
                unosCodigosIdiomasAccesibles = [ unIdioma.getCodigoIdiomaEnGvSIG() for unIdioma in theIdiomasAccesibles] 
                todosCodigosIdiomasInicial   = todosCodigosIdiomas[:]
         
                unosCodigosIdiomasAIgnorar      = []
                unosCodigosIdiomasACrear        = []
                unosCodigosIdiomasAImportar     = []
                
                unosCodigosIdiomas  = theContenido[ 'languages']
                todosDetallesIdiomas = theContenido.get( 'languages_details', {})
                
                for unCodigoIdioma in unosCodigosIdiomas:
                    if unCodigoIdioma in todosCodigosIdiomas:
                        if not ( unCodigoIdioma in unosCodigosIdiomasAccesibles):
                            unosCodigosIdiomasAIgnorar.append( unCodigoIdioma)   
                        else:
                            unosCodigosIdiomasAImportar.append( unCodigoIdioma) 
                    else:
                        unosCodigosIdiomasACrear.append( unCodigoIdioma)
                        
                theInformeImportarContenidos[ 'languages_to_create'] = len( unosCodigosIdiomasACrear)
                theInformeImportarContenidos[ 'expected_operations']   += len( unosCodigosIdiomasACrear)
                
                unSetCodigosIdiomasACrear = set( unosCodigosIdiomasACrear)
                     
                
                # ######################################################
                """Determine Strings to Create and process.
                
                """
                unosSimbolosCadenasExistentes = theCatalogo.fObtenerSimbolosTodasCadenasSinOrdenar()
                unSetSimbolosExistentes = set( unosSimbolosCadenasExistentes)
                
                unosSimbolosAImportar       = theContenido[ 'strings_modules_and_translations'].keys()
                unSetSimbolosAImportar      = set( unosSimbolosAImportar)
                unSetSimbolosACrear         = unSetSimbolosAImportar - unSetSimbolosExistentes
                unSetSimbolosNoImportados   = unSetSimbolosExistentes - unSetSimbolosAImportar
                
                theInformeImportarContenidos[ 'strings_to_create']     = len( unSetSimbolosACrear)
                theInformeImportarContenidos[ 'expected_operations']   += len( unSetSimbolosACrear)
                
                theInformeImportarContenidos[ 'strings_to_process']    = len( unosSimbolosAImportar)
        
                
                theInformeImportarContenidos[ 'translations_to_create_in_new_languages_for_preexisting_strings'] = len( unSetSimbolosNoImportados) * len( unosCodigosIdiomasACrear)
                theInformeImportarContenidos[ 'expected_operations']   += len( unSetSimbolosNoImportados) * len( unosCodigosIdiomasACrear)
                
                theInformeImportarContenidos[ 'expected_operations']   += len( unosSimbolosAImportar) * len( set( todosCodigosIdiomas).union( set( unosCodigosIdiomasACrear)))
                
                 
                
                # ######################################################
                """Count Translations to process.
                
                """
                for unSimboloCadena in unosSimbolosAImportar:        
                    unaImportedCadenaModulesAndTranslations = theContenido[ 'strings_modules_and_translations'][ unSimboloCadena]
                    unasImportedTraduccionesPorIdioma       = unaImportedCadenaModulesAndTranslations[ 'translations']
                    theInformeImportarContenidos[ 'translations_to_process'] += len( unasImportedTraduccionesPorIdioma.keys())
                
            finally:
                unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
 
            if self.getDebeCrearTraduccionesQueFaltan():
                unInformeCrearTraduccionesQueFaltan = theInformeImportarContenidos[ 'missing_translations_creation'] 
                unInformeCrearTraduccionesQueFaltan[ 'strings_to_complete']  = ( len( unosSimbolosCadenasExistentes) + len( unosSimbolosAImportar)) 
                unInformeCrearTraduccionesQueFaltan[ 'expected_operations']  = ( len( unosSimbolosCadenasExistentes) + len( unosSimbolosAImportar)) * len( set( todosCodigosIdiomas).union( set( unosCodigosIdiomasACrear)))
                
                theInformeImportarContenidos[ 'expected_operations']   += ( len( unosSimbolosCadenasExistentes) + len( unosSimbolosAImportar)) * len( set( todosCodigosIdiomas).union( set( unosCodigosIdiomasACrear)))
 
            if theJustEstimateCost:
                return self
             
             
            # ######################################################
            """Create Modules as determined above.
            
            """
            unSubExecutionRecord = self.fStartExecution( 'block',  'pImportarContenidosIntercambio-SubExecution to create modules (TRAModule).', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
            try:
            
                for unNombreModulo in unosNombresModulosACrear:
                    unSubSubExecutionRecord = self.fStartExecution( 'block',  'pImportarContenidosIntercambio-SubExecution to create one module (TRAModule).', unSubExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }, 'module name: %s' % unNombreModulo) 
                    try:
                    
                        unNuevoModulo =  theCatalogo.fCrearModulo( 
                            theUseCaseQueryResult, 
                            unNombreModulo,
                            unPermissionsCache,
                            unRolesCache,
                            unSubSubExecutionRecord,                            
                        )
                     
                        if unNuevoModulo:
                            theInformeImportarContenidos[ 'module_creations'] += 1
                            unCurrentChangesHolder[ 0] += 1
                            theInformeImportarContenidos[ 'operations_done']   += 1
                            
                            unOperationsDoneTrasUltimaEspera += 1
                            
                            if ( unaEsperaTrasOperacionesEnSegundos >= 0.1) and ( unNumeroOperacionesAntesDeCederProcesador > 0) and ( unOperationsDoneTrasUltimaEspera >= unNumeroOperacionesAntesDeCederProcesador):
                                unMustSleep = True
                                if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                    unMillisecondsComienzoEspera = fMillisecondsNow()
                                    if ( unMillisecondsComienzoEspera - unMillisecondsFinUltimaEspera) < unPeriodoActividadSinEsperaEnMilisegundos:
                                        unMustSleep = False

                                if unMustSleep:                                    
                                    time.sleep( unaEsperaTrasOperacionesEnSegundos )

                                    unOperationsDoneTrasUltimaEspera = 0
                                    
                                    if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                        unMillisecondsFinUltimaEspera = fMillisecondsNow()
                            
                            
                            self.pPeriodicCommit( 
                                theCatalogo, 
                                theInformeImportarContenidos, 
                                unIntervaloRefrescoEnNumeroEscrituras, 
                                unIntervaloRefrescoEnMinutos, 
                                unaEsperaEntreTransaccionesEnSegundos,
                                unNumeroDeRefrescosPorEscrituraEnLog,
                                unCurrentChangesHolder, unCurrentCommitsHolder, 
                                unaFechaUltimoInformeProgresoHolder, 
                                True,
                                thePermissionsCache         =unPermissionsCache, 
                                theRolesCache               =unRolesCache, 
                                theParentExecutionRecord    =unSubSubExecutionRecord,
                            )


                        if not unNuevoModulo:
                            unAhora = fDateTimeNow()
                            theInformeImportarContenidos[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                            theInformeImportarContenidos[ 'error'] = "gvSIGi18n_ModuleCreationError_error_msgid"
                            theInformeImportarContenidos[ 'error_detail'] = unNombreModulo            
                            return self
                    finally:
                        unSubSubExecutionRecord and unSubSubExecutionRecord.pEndExecution()
                        unSubSubExecutionRecord and unSubSubExecutionRecord.pClearLoggedAll()
                
            finally:
                unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
              
                
                
                
            # ######################################################
            """"Retrieve well-known language information
            
            """
            unosIntlLanguagesNamesAndFlagsPorCodigo = theCatalogo.fLanguagesNamesAndFlagsPorCodigo( ) # Was fLanguagesNamesAndFlagsPorCodigo_AvailableInPlone( )
            
            
            
            
            # ######################################################
            """Create Languages as determined above
            
            """
            unSubExecutionRecord = self.fStartExecution( 'block',  'pImportarContenidosIntercambio-SubExecution to create languages (TRAIdioma).', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
            try:
                     
                for unCodigoIdioma in unosCodigosIdiomasACrear:
                    
                    unosDetallesIdioma = todosDetallesIdiomas.get( unCodigoIdioma, {})
                    
                    unSubSubExecutionRecord = self.fStartExecution( 'block',  'pImportarContenidosIntercambio-SubExecution to create one language (TRAIdioma).', unSubExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }, 'language_code: %s' % unCodigoIdioma) 
                    try:
                    
                        unCodigoInternacionalIdioma = unCodigoIdioma
                        unNombreEnglishIdioma       = unCodigoIdioma
                        unNombreNativoIdioma        = unCodigoIdioma
                        
                        if unosDetallesIdioma:
                            unCodigoInternacionalIdioma = unosDetallesIdioma.get( 'codigo_internacional_idioma', '')
                            unNombreEnglishIdioma       = unosDetallesIdioma.get( 'english_name', '')
                            unNombreNativoIdioma        = unosDetallesIdioma.get( 'nombre_nativo_de_idioma', '')
                        else:
                            unosIntlDatosIdioma     = unosIntlLanguagesNamesAndFlagsPorCodigo.get( unCodigoIdioma, { 'english': unCodigoIdioma, 'native': unCodigoIdioma, 'flag': cTRAFlagIdiomaDesconocida,})
                            unNombreEnglishIdioma   = unosIntlDatosIdioma.get( 'english', '')
                            unNombreNativoIdioma    = unosIntlDatosIdioma.get( 'native', '')
            
                      
                        unNuevoIdioma =  theCatalogo.fCrearIdioma(  
                            theUseCaseQueryResult, 
                            unCodigoIdioma, 
                            unCodigoInternacionalIdioma,
                            unNombreEnglishIdioma, 
                            unNombreEnglishIdioma, 
                            unNombreNativoIdioma,
                            unPermissionsCache,
                            unRolesCache,
                            unSubSubExecutionRecord
                        )
                        
                        if unNuevoIdioma:
                            todosCodigosIdiomas.append( unCodigoIdioma)
                            theInformeImportarContenidos[ 'language_creations'] += 1
                            unCurrentChangesHolder[ 0] += 1
                            theInformeImportarContenidos[ 'operations_done']   += 1
                            
                            unOperationsDoneTrasUltimaEspera += 1
                            
                            if ( unaEsperaTrasOperacionesEnSegundos >= 0.1) and ( unNumeroOperacionesAntesDeCederProcesador > 0) and ( unOperationsDoneTrasUltimaEspera >= unNumeroOperacionesAntesDeCederProcesador):
                                unMustSleep = True
                                if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                    unMillisecondsComienzoEspera = fMillisecondsNow()
                                    if ( unMillisecondsComienzoEspera - unMillisecondsFinUltimaEspera) < unPeriodoActividadSinEsperaEnMilisegundos:
                                        unMustSleep = False

                                if unMustSleep:                                    
                                    time.sleep( unaEsperaTrasOperacionesEnSegundos )

                                    unOperationsDoneTrasUltimaEspera = 0
                                    
                                    if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                        unMillisecondsFinUltimaEspera = fMillisecondsNow()
                            
                            
                            self.pPeriodicCommit( 
                                theCatalogo, 
                                theInformeImportarContenidos, 
                                unIntervaloRefrescoEnNumeroEscrituras, 
                                unIntervaloRefrescoEnMinutos, 
                                unaEsperaEntreTransaccionesEnSegundos,
                                unNumeroDeRefrescosPorEscrituraEnLog,
                                unCurrentChangesHolder, unCurrentCommitsHolder, 
                                unaFechaUltimoInformeProgresoHolder, 
                                True,
                                thePermissionsCache         =unPermissionsCache, 
                                theRolesCache               =unRolesCache, 
                                theParentExecutionRecord    =unSubSubExecutionRecord,
                            )
                            
                        if not unNuevoIdioma:
                            # ######################################################
                            """Exit with error condition.
                            
                            """
                            unAhora = fDateTimeNow()  
                            theInformeImportarContenidos[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                            theInformeImportarContenidos[ 'error'] = "gvSIGi18n_TRAIdiomaCreationFailure_error_msgid"
                            theInformeImportarContenidos[ 'error_detail'] = unCodigoIdioma
                            return self      
                        
                    finally:
                        unSubSubExecutionRecord and unSubSubExecutionRecord.pEndExecution()
                        unSubSubExecutionRecord and unSubSubExecutionRecord.pClearLoggedAll()
                        
            finally:
                unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
            
            unSetTodosCodigosIdiomas        = set( todosCodigosIdiomas)
            unSetTodosCodigosIdiomasInicial = set( todosCodigosIdiomasInicial)
            
            
            
            
            
            
            # ######################################################
            """Get permissions and roles specifications to add to new instances of TRACadena and TRATraduccion.
            
            """
            unSubExecutionRecord = self.fStartExecution( 'block',  'pImportarContenidosIntercambio-SubExecution to gather permissions and roles specifications.', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
            try:
    
                someCadenaPermissionsSpecs          = self.getCatalogo().fPermissionsForElementType(    cNombreTipoTRACadena)     
                aCadenaAcquireRoleAssignments       = self.fAcquireRoleAssignmentsElementType(          cNombreTipoTRACadena)
                
                someTraduccionPermissionsSpecs      = self.getCatalogo().fPermissionsForElementType(    cNombreTipoTRATraduccion)     
                aTraduccionAcquireRoleAssignments   = self.fAcquireRoleAssignmentsElementType(          cNombreTipoTRATraduccion) 
                
            finally:
                unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
                
                
                
                
                
                
            # ######################################################
            """Get Catalogs to add new instances to.
            
            """
            unSubExecutionRecord = self.fStartExecution( 'block',  'pImportarContenidosIntercambio-SubExecution to get the Zcatalogs to which to add instances during import loop.', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
            try:
                unCatalogoRaiz = self.getCatalogo()           
                unCatalogBusquedaCadenas       = unCatalogoRaiz.fCatalogBusquedaCadenas() 
                unCatalogFiltroCadenas         = unCatalogoRaiz.fCatalogFiltroCadenas() 
                unCatalogTextoCadenas          = unCatalogoRaiz.fCatalogTextoCadenas() 
                
                unosCatalogsBusquedaTraduccionesPorIdioma = { }
                unosCatalogsFiltroTraduccionesPorIdioma   = { }
                unosCatalogsTextoTraduccionesPorIdioma    = { }
                for unCodigoIdioma in todosCodigosIdiomas:
                    unIdioma = self.getCatalogo().fGetIdiomaPorCodigo( unCodigoIdioma)
                    if unIdioma:
                        unosCatalogsBusquedaTraduccionesPorIdioma[ unCodigoIdioma] = unCatalogoRaiz.fCatalogBusquedaTraduccionesParaIdioma( unIdioma)
                        unosCatalogsFiltroTraduccionesPorIdioma[   unCodigoIdioma] = unCatalogoRaiz.fCatalogFiltroTraduccionesParaIdioma(   unIdioma)
                        unosCatalogsTextoTraduccionesPorIdioma[    unCodigoIdioma] = unCatalogoRaiz.fCatalogTextoTraduccionesParaIdioma(    unIdioma)

            finally:
                unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
                
                    
                
                
             
                    
            # ######################################################
            """Create Strings as determined above.
            
            """
            unSubExecutionRecord = self.fStartExecution( 'block',  'pImportarContenidosIntercambio-SubExecution to create strings (TRACadena).', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
            try:
                unCacheCadenasCreadas = { }        
                for unSimboloCadena in unSetSimbolosACrear:
        
                    
                    unaImportedCadenaModulesAndTranslations = theContenido[ 'strings_modules_and_translations'][ unSimboloCadena]
                    unosNombresModulos                      = unaImportedCadenaModulesAndTranslations[ 'modules']
                    unosImportedSources                     = unaImportedCadenaModulesAndTranslations[ 'sources']

                    unPrevIdNumber = theIdNumberHolder[ 0]   
                    
                    unaCadenaEIdNumber = self.fCrearCadenaImportada( 
                        theCatalogo, 
                        theColeccionCadenas, 
                        unSimboloCadena, 
                        unosNombresModulos, 
                        unosImportedSources,
                        unPrevIdNumber, 
                        theMemberId, 
                        thePloneUtilsTool, 
                        unCatalogBusquedaCadenas, 
                        unCatalogFiltroCadenas, 
                        unCatalogTextoCadenas,
                        someCadenaPermissionsSpecs,
                        aCadenaAcquireRoleAssignments,
                        thePermissionsCache         =unPermissionsCache, 
                        theRolesCache               =unRolesCache, 
                        theParentExecutionRecord    =unExecutionRecord,
                    )
        
                    if not unaCadenaEIdNumber:
                        unAhora = fDateTimeNow()  # SALIENDO EN CONDICION DE ERROR
                        theInformeImportarContenidos[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                        theInformeImportarContenidos[ 'error'] = "gvSIGi18n_TRACadenaCreationError_error_msgid"
                        theInformeImportarContenidos[ 'error_detail'] = unSimboloCadena            
                        self.pPeriodicCommit( 
                            theCatalogo, 
                            theInformeImportarContenidos, 
                            unIntervaloRefrescoEnNumeroEscrituras, 
                            unIntervaloRefrescoEnMinutos, 
                            unaEsperaEntreTransaccionesEnSegundos,
                            unNumeroDeRefrescosPorEscrituraEnLog,
                            unCurrentChangesHolder, unCurrentCommitsHolder, 
                            unaFechaUltimoInformeProgresoHolder, 
                            True,
                            thePermissionsCache         =unPermissionsCache, 
                            theRolesCache               =unRolesCache, 
                            theParentExecutionRecord    =unExecutionRecord,
                        )
                        return self
                    
                    theInformeImportarContenidos[ 'string_creations'] += 1
                    theInformeImportarContenidos[ 'operations_done']  += 1
                    
                    unOperationsDoneTrasUltimaEspera += 1
                    
                    if ( unaEsperaTrasOperacionesEnSegundos >= 0.1) and ( unNumeroOperacionesAntesDeCederProcesador > 0) and ( unOperationsDoneTrasUltimaEspera >= unNumeroOperacionesAntesDeCederProcesador):
                        unMustSleep = True
                        if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                            unMillisecondsComienzoEspera = fMillisecondsNow()
                            if ( unMillisecondsComienzoEspera - unMillisecondsFinUltimaEspera) < unPeriodoActividadSinEsperaEnMilisegundos:
                                unMustSleep = False

                        if unMustSleep:                                    
                            time.sleep( unaEsperaTrasOperacionesEnSegundos )

                            unOperationsDoneTrasUltimaEspera = 0
                            
                            if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                unMillisecondsFinUltimaEspera = fMillisecondsNow()
                        
                        
                    
                    unaCadena   = unaCadenaEIdNumber[ 0]
                    unIdNumber  = unaCadenaEIdNumber[ 1]
                    theIdNumberHolder[ 0] = unIdNumber
                    
                    unSetSimbolosExistentes.add( unSimboloCadena)
                    unCacheCadenasCreadas[ unSimboloCadena] = unaCadena
                     
                    
                    unCurrentChangesHolder[ 0] += 1
                    
                    
                    self.pPeriodicCommit( 
                        theCatalogo, 
                        theInformeImportarContenidos, 
                        unIntervaloRefrescoEnNumeroEscrituras, 
                        unIntervaloRefrescoEnMinutos, 
                        unaEsperaEntreTransaccionesEnSegundos,
                        unNumeroDeRefrescosPorEscrituraEnLog,
                        unCurrentChangesHolder, unCurrentCommitsHolder, 
                        unaFechaUltimoInformeProgresoHolder, 
                        False,
                        thePermissionsCache         =unPermissionsCache, 
                        theRolesCache               =unRolesCache, 
                        theParentExecutionRecord    =unExecutionRecord,
                    )
                    
                self.pPeriodicCommit( 
                    theCatalogo, 
                    theInformeImportarContenidos, 
                    unIntervaloRefrescoEnNumeroEscrituras, 
                    unIntervaloRefrescoEnMinutos, 
                    unaEsperaEntreTransaccionesEnSegundos,
                    unNumeroDeRefrescosPorEscrituraEnLog,
                    unCurrentChangesHolder, unCurrentCommitsHolder,
                    unaFechaUltimoInformeProgresoHolder, 
                    True,
                    thePermissionsCache         =unPermissionsCache, 
                    theRolesCache               =unRolesCache, 
                    theParentExecutionRecord    =unExecutionRecord,            
                )
                    
            finally:
                unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
                
                    
                
                
    
                
             
     
    
            aTranslationService = getToolByName( self, 'translation_service', None)
            
            
    
            # ######################################################
            """Process translations, for all Strings to process
            
            """
            unSubExecutionRecord = self.fStartExecution( 'block',  'pImportarContenidosIntercambio-SubExecution to import translations (TRATraduccion).', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
            try:
            
                for unSimboloCadena in unosSimbolosAImportar:        
                    unaImportedCadenaModulesAndTranslations = theContenido[ 'strings_modules_and_translations'][ unSimboloCadena]
                    unosImportedNombresModulos              = unaImportedCadenaModulesAndTranslations[ 'modules']
                    unosImportedSources                     = unaImportedCadenaModulesAndTranslations[ 'sources']
                    unasImportedTraduccionesPorIdioma       = unaImportedCadenaModulesAndTranslations[ 'translations']
                    unosImportedIdiomasTraducciones         = unasImportedTraduccionesPorIdioma.keys()
                    
                    unosNombresModulosToAppend = set( unosImportedNombresModulos) - set( unosNombresModulosAIgnorar)
                    
                    # ACV 20090419 was
                    # if unosImportedIdiomasTraducciones or unosImportedNombresModulos:
                    if True or unosImportedIdiomasTraducciones or unosImportedNombresModulos:
                        unaEsCadenaRecienCreada = False
                        unasTraduccionesExistentes = { }
                        unosCodigosIdiomasTraduccionesCreadas  = set()
                        unosCodigosIdiomasTraduccionesEncontradas = set()
                        
                        unaCadena = unCacheCadenasCreadas.get( unSimboloCadena, None)
                        if unaCadena:            
                            unasTraduccionesExistentes = { }
                            unaEsCadenaRecienCreada = True
                        else:
                            unaEsCadenaRecienCreada = False
                            unaCadena = theCatalogo.fGetCadenaPorSimbolo( unSimboloCadena)
                            if not unaCadena: 
                                # ######################################################
                                """Exit with error condition.
                                
                                """
                                theInformeImportarContenidos[  'fecha_informe'] = self.fDateToStoreString( unAhora)
                                theInformeImportarContenidos[ 'error'] = "gvSIGi18n_TRACadena_failedSearchBySimbolo_error_msgid"
                                theInformeImportarContenidos[ 'error_detail'] = unSimboloCadena        
                                self.pPeriodicCommit( 
                                    theCatalogo, 
                                    theInformeImportarContenidos, 
                                    unIntervaloRefrescoEnNumeroEscrituras, 
                                    unIntervaloRefrescoEnMinutos, 
                                    unCurrentChangesHolder, unCurrentCommitsHolder, 
                                    unaEsperaEntreTransaccionesEnSegundos,
                                    unNumeroDeRefrescosPorEscrituraEnLog,
                                    unaFechaUltimoInformeProgresoHolder, 
                                    True,
                                    thePermissionsCache         =unPermissionsCache, 
                                    theRolesCache               =unRolesCache, 
                                    theParentExecutionRecord    =unExecutionRecord,            
                                )
                                return self
                            
                            
                            unasTraduccionesExistentes  = unaCadena.fTraduccionesPorIdiomas( unosImportedIdiomasTraducciones, thePloneUtilsTool) 
        
                            unAlreadyChangedCadena = False
                            if unosNombresModulosToAppend:
                                if unaCadena.fAppendNombresModulos( unosNombresModulosToAppend):
                                    unAlreadyChangedCadena = True

                                    unCurrentChangesHolder[ 0] += 1
                                    unaCadena.pRecatalogCadena()
                                    unNumeroCambios = unaCadena.fPropagarCambioNombresModulosATraducciones()
                                    unCurrentChangesHolder[ 0] += unNumeroCambios
        
                            
                            if unosImportedSources:
                                if unaCadena.fAppendSources( unosImportedSources):
                                    if not unAlreadyChangedCadena:
                                        unAlreadyChangedCadena = True
                                        unCurrentChangesHolder[ 0] += 1
                                    
                                    
                        unaIdCadena = unaCadena.getId()
                        unosNombresModulos = unaCadena.getNombresModulos()
        
                        
                        
                        # ######################################################
                        """Process String Translations, for each language 
                        
                        """
                        for unCodigoIdioma in unosImportedIdiomasTraducciones:
                            if not ( unCodigoIdioma in unosCodigosIdiomasAIgnorar):
                                
                                unaTraduccionEncoded   = unasImportedTraduccionesPorIdioma[ unCodigoIdioma]
                                if unaTraduccionEncoded:
                                    
                                    unaTraduccionExistente  = unasTraduccionesExistentes.get( unCodigoIdioma, None)
                                    
                                    if not unaTraduccionExistente:
            
                                        # ######################################################
                                        """Create Translation, possibly translated.
                                        
                                        """
                                        unaNuevaTraduccion = self.fCrearTraduccionImportada( 
                                            theCodigoIdioma                     =unCodigoIdioma, 
                                            theCadena                           =unaCadena,
                                            theSimboloCadena                    =unSimboloCadena,
                                            theIdCadena                         =unaIdCadena, 
                                            theTraduccionEncoded                =unaTraduccionEncoded, 
                                            theNombresModulos                   =unosNombresModulos, 
                                            theMemberId                         =theMemberId, 
                                            thePloneUtilsTool                   =thePloneUtilsTool, 
                                            theCatalogBusquedaTraducciones      =unosCatalogsBusquedaTraduccionesPorIdioma[ unCodigoIdioma], 
                                            theCatalogFiltroTraducciones        =unosCatalogsFiltroTraduccionesPorIdioma[   unCodigoIdioma], 
                                            theCatalogTextoTraducciones         =unosCatalogsTextoTraduccionesPorIdioma[    unCodigoIdioma],
                                            theTraduccionPermissionsSpecs       =someTraduccionPermissionsSpecs,
                                            theTraduccionAcquireRoleAssignments =aTraduccionAcquireRoleAssignments,
                                            thePermissionsCache                 =unPermissionsCache, 
                                            theRolesCache                       =unRolesCache, 
                                            theParentExecutionRecord            =unExecutionRecord,
                                        )
                                        if unaNuevaTraduccion:
                                            unosCodigosIdiomasTraduccionesCreadas.add( unCodigoIdioma)
                                            unCurrentChangesHolder[ 0] += 1
                                            theInformeImportarContenidos[ 'translation_creations'] += 1 
                                            theInformeImportarContenidos[ 'operations_done']   += 1
                                            
                                            unOperationsDoneTrasUltimaEspera += 1
                                            
                                            if ( unaEsperaTrasOperacionesEnSegundos >= 0.1) and ( unNumeroOperacionesAntesDeCederProcesador > 0) and ( unOperationsDoneTrasUltimaEspera >= unNumeroOperacionesAntesDeCederProcesador):
                                                unMustSleep = True
                                                if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                                    unMillisecondsComienzoEspera = fMillisecondsNow()
                                                    if ( unMillisecondsComienzoEspera - unMillisecondsFinUltimaEspera) < unPeriodoActividadSinEsperaEnMilisegundos:
                                                        unMustSleep = False
                
                                                if unMustSleep:                                    
                                                    time.sleep( unaEsperaTrasOperacionesEnSegundos )
                
                                                    unOperationsDoneTrasUltimaEspera = 0
                                                    
                                                    if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                                        unMillisecondsFinUltimaEspera = fMillisecondsNow()
                        
                                            
                                        else:
                                            # ######################################################
                                            """Exit with error condition.
                                            
                                            """
                                            theInformeImportarContenidos[ 'fecha_informe'] =self.fDateTimeNowTextual()
                                            theInformeImportarContenidos[ 'error'] = "gvSIGi18n_TRACadena_failedTranslationCreation_error_msgid"
                                            theInformeImportarContenidos[ 'error_detail'] = '%s %s' % ( unCodigoIdioma, unSimboloCadena , )
                                            self.pPeriodicCommit( 
                                                theCatalogo, 
                                                theInformeImportarContenidos, 
                                                unIntervaloRefrescoEnNumeroEscrituras, 
                                                unIntervaloRefrescoEnMinutos, 
                                                unaEsperaEntreTransaccionesEnSegundos,
                                                unNumeroDeRefrescosPorEscrituraEnLog,
                                                unCurrentChangesHolder, unCurrentCommitsHolder,
                                                unaFechaUltimoInformeProgresoHolder, 
                                                True,
                                                thePermissionsCache         =unPermissionsCache, 
                                                theRolesCache               =unRolesCache, 
                                                theParentExecutionRecord    =unExecutionRecord,                       
                                            )
                                            return self
                                            
                                    else:
                                        # ######################################################
                                        """Update existing Translation, according to current state  and current and new translation.
                                        
                                        """
                                        unosCodigosIdiomasTraduccionesEncontradas.add( unCodigoIdioma)
                                        unEstadoTraduccion = unaTraduccionExistente.getEstadoTraduccion()
                                        unaCadenaTraducida = unaTraduccionExistente.getCadenaTraducida()
                                        
                                        
                                        if ( unEstadoTraduccion == cEstadoTraduccionPendiente) or ( not unaCadenaTraducida):
                                            
                                            unAhoraStoreString =self.fDateTimeNowTextual()
    
                                            unaTraduccionExistente.setCadenaTraducida(          unaTraduccionEncoded)
                                            unaTraduccionExistente.setEstadoTraduccion(         cEstadoTraduccionTraducida)    
                                            unaTraduccionExistente.setUsuarioTraductor(         theMemberId)   
                                            unaTraduccionExistente.setFechaTraduccionTextual(   unAhoraStoreString)    
                                            unaTraduccionExistente.setUsuarioRevisor(           None)  
                                            unaTraduccionExistente.setFechaRevisionTextual(            None)
                                            unaTraduccionExistente.setFechaDefinitivoTextual(          None)
                                            unaTraduccionExistente.pRegistrarHistoria( 
                                                theAccion                   = cTranslationHistoryAction_Importar, 
                                                theFechaAccionTextual       = unAhoraStoreString, 
                                                theUsuarioActor             = theMemberId, 
                                                theEstadoTraduccion         = cEstadoTraduccionTraducida, 
                                                theFechaTraduccionTextual   = unAhoraStoreString, 
                                                theUsuarioTraductor         = theMemberId, 
                                                theCadenaTraducida          = unaTraduccionEncoded, 
                                                theFechaRevisionTextual     = None, 
                                                theUsuarioRevisor           = None, 
                                                theFechaDefinitivoTextual   = None, 
                                                theUsuarioCoordinador       = None,
                                                theComentario               = cMarcaDeComentarioSinCambios,                                            
                                            )
                                            
                                            unaTraduccionExistente.pAddToCatalogs( 
                                                unosCatalogsBusquedaTraduccionesPorIdioma[ unCodigoIdioma], 
                                                unosCatalogsFiltroTraduccionesPorIdioma[   unCodigoIdioma], 
                                                unosCatalogsTextoTraduccionesPorIdioma[    unCodigoIdioma],
                                            )
                
                                            theInformeImportarContenidos[ 'translation_changes'] += 1 
                                            theInformeImportarContenidos[ 'operations_done']   += 1
                                            
                                            unCurrentChangesHolder[ 0] += 1                            
                                                                    
                                            unOperationsDoneTrasUltimaEspera += 1
                                                            
                                            if ( unaEsperaTrasOperacionesEnSegundos >= 0.1) and ( unNumeroOperacionesAntesDeCederProcesador > 0) and ( unOperationsDoneTrasUltimaEspera >= unNumeroOperacionesAntesDeCederProcesador):
                                                unMustSleep = True
                                                if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                                    unMillisecondsComienzoEspera = fMillisecondsNow()
                                                    if ( unMillisecondsComienzoEspera - unMillisecondsFinUltimaEspera) < unPeriodoActividadSinEsperaEnMilisegundos:
                                                        unMustSleep = False
                
                                                if unMustSleep:                                    
                                                    time.sleep( unaEsperaTrasOperacionesEnSegundos )
                
                                                    unOperationsDoneTrasUltimaEspera = 0
                                                    
                                                    if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                                        unMillisecondsFinUltimaEspera = fMillisecondsNow()
                        
                
                                        elif ( unEstadoTraduccion == cEstadoTraduccionTraducida):
                                            
                                            if unaTraduccionEncoded == unaCadenaTraducida:
                                                theInformeImportarContenidos[ 'translations_unchanged'] += 1 
                                                theInformeImportarContenidos[ 'operations_done']   += 1
                                                
                                                unOperationsDoneTrasUltimaEspera += 1
                                                
                                                if ( unaEsperaTrasOperacionesEnSegundos >= 0.1) and ( unNumeroOperacionesAntesDeCederProcesador > 0) and ( unOperationsDoneTrasUltimaEspera >= unNumeroOperacionesAntesDeCederProcesador):
                                                    unMustSleep = True
                                                    if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                                        unMillisecondsComienzoEspera = fMillisecondsNow()
                                                        if ( unMillisecondsComienzoEspera - unMillisecondsFinUltimaEspera) < unPeriodoActividadSinEsperaEnMilisegundos:
                                                            unMustSleep = False
                    
                                                    if unMustSleep:                                    
                                                        time.sleep( unaEsperaTrasOperacionesEnSegundos )
                    
                                                        unOperationsDoneTrasUltimaEspera = 0
                                                        
                                                        if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                                            unMillisecondsFinUltimaEspera = fMillisecondsNow()
                        
                                                
                                                
                                            else:
                                                
                                                unAhoraStoreString =self.fDateTimeNowTextual()
                                                
                                                unaTraduccionExistente.setCadenaTraducida(   unaTraduccionEncoded)
                                                unaTraduccionExistente.setEstadoTraduccion(  cEstadoTraduccionTraducida)    
                                                unaTraduccionExistente.setUsuarioTraductor(  theMemberId)   
                                                unaTraduccionExistente.setFechaTraduccionTextual(   unAhoraStoreString)    
                                                unaTraduccionExistente.setUsuarioRevisor(    None)  
                                                unaTraduccionExistente.setFechaRevisionTextual(     None)
                                                unaTraduccionExistente.setFechaDefinitivoTextual(   None)
                                                unaTraduccionExistente.pRegistrarHistoria( 
                                                    theAccion                   = cTranslationHistoryAction_Importar, 
                                                    theFechaAccionTextual       = unAhoraStoreString, 
                                                    theUsuarioActor             = theMemberId, 
                                                    theEstadoTraduccion         = cEstadoTraduccionTraducida, 
                                                    theFechaTraduccionTextual   = unAhoraStoreString, 
                                                    theUsuarioTraductor         = theMemberId, 
                                                    theCadenaTraducida          = unaTraduccionEncoded, 
                                                    theFechaRevisionTextual     = None, 
                                                    theUsuarioRevisor           = None, 
                                                    theFechaDefinitivoTextual   = None, 
                                                    theUsuarioCoordinador       = None,
                                                    theComentario               = cMarcaDeComentarioSinCambios, 
                                                )
    
                                                
                                                # unaTraduccionExistente.reindexObject()
                                                unaTraduccionExistente.pAddToCatalogs( 
                                                    unosCatalogsBusquedaTraduccionesPorIdioma[ unCodigoIdioma], 
                                                    unosCatalogsFiltroTraduccionesPorIdioma[   unCodigoIdioma], 
                                                    unosCatalogsTextoTraduccionesPorIdioma[    unCodigoIdioma],
                                                )
                                                
                                                theInformeImportarContenidos[ 'translation_changes'] += 1 
                                                theInformeImportarContenidos[ 'operations_done']   += 1
                                                
                                                unCurrentChangesHolder[ 0] += 1                            
                
                                                unOperationsDoneTrasUltimaEspera += 1
                                                
                                                if ( unaEsperaTrasOperacionesEnSegundos >= 0.1) and ( unNumeroOperacionesAntesDeCederProcesador > 0) and ( unOperationsDoneTrasUltimaEspera >= unNumeroOperacionesAntesDeCederProcesador):
                                                    unMustSleep = True
                                                    if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                                        unMillisecondsComienzoEspera = fMillisecondsNow()
                                                        if ( unMillisecondsComienzoEspera - unMillisecondsFinUltimaEspera) < unPeriodoActividadSinEsperaEnMilisegundos:
                                                            unMustSleep = False
                    
                                                    if unMustSleep:                                    
                                                        time.sleep( unaEsperaTrasOperacionesEnSegundos )
                    
                                                        unOperationsDoneTrasUltimaEspera = 0
                                                        
                                                        if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                                            unMillisecondsFinUltimaEspera = fMillisecondsNow()
                        
                                                
                                                
                                        elif ( unEstadoTraduccion == cEstadoTraduccionRevisada):
                                        
                                            if unaTraduccionEncoded == unaCadenaTraducida:
                                                theInformeImportarContenidos[ 'translations_unchanged'] += 1 
                                                theInformeImportarContenidos[ 'operations_done']   += 1
                                                
                                                unOperationsDoneTrasUltimaEspera += 1
                                                
                                                if ( unaEsperaTrasOperacionesEnSegundos >= 0.1) and ( unNumeroOperacionesAntesDeCederProcesador > 0) and ( unOperationsDoneTrasUltimaEspera >= unNumeroOperacionesAntesDeCederProcesador):
                                                    unMustSleep = True
                                                    if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                                        unMillisecondsComienzoEspera = fMillisecondsNow()
                                                        if ( unMillisecondsComienzoEspera - unMillisecondsFinUltimaEspera) < unPeriodoActividadSinEsperaEnMilisegundos:
                                                            unMustSleep = False
                    
                                                    if unMustSleep:                                    
                                                        time.sleep( unaEsperaTrasOperacionesEnSegundos )
                    
                                                        unOperationsDoneTrasUltimaEspera = 0
                                                        
                                                        if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                                            unMillisecondsFinUltimaEspera = fMillisecondsNow()
                       
                                                
                                            else:
                                                unAhoraStoreString =self.fDateTimeNowTextual()
                                                
                                                unaTraduccionExistente.pRegistrarHistoria( 
                                                   theAccion                    = cTranslationHistoryAction_Ignorar, 
                                                    theFechaAccionTextual       = unAhoraStoreString, 
                                                    theUsuarioActor             = theMemberId, 
                                                    theEstadoTraduccion         = cEstadoTraduccionRevisada, 
                                                    theFechaTraduccionTextual   = unAhoraStoreString, 
                                                    theUsuarioTraductor         = theMemberId, 
                                                    theCadenaTraducida          = unaTraduccionEncoded, 
                                                    theFechaRevisionTextual     = None, 
                                                    theUsuarioRevisor           = None, 
                                                    theFechaDefinitivoTextual   = None, 
                                                    theUsuarioCoordinador       = None,
                                                    theComentario               = cMarcaDeComentarioSinCambios, 
                                                )
                
                                                unCurrentChangesHolder[ 0] += 1                            
                                                theInformeImportarContenidos[ 'operations_done']   += 1
                
                                                theInformeImportarContenidos[ 'translations_ignored'] += 1 
                
                                                unOperationsDoneTrasUltimaEspera += 1
                                                                    
                                                if ( unaEsperaTrasOperacionesEnSegundos >= 0.1) and ( unNumeroOperacionesAntesDeCederProcesador > 0) and ( unOperationsDoneTrasUltimaEspera >= unNumeroOperacionesAntesDeCederProcesador):
                                                    unMustSleep = True
                                                    if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                                        unMillisecondsComienzoEspera = fMillisecondsNow()
                                                        if ( unMillisecondsComienzoEspera - unMillisecondsFinUltimaEspera) < unPeriodoActividadSinEsperaEnMilisegundos:
                                                            unMustSleep = False
                    
                                                    if unMustSleep:                                    
                                                        time.sleep( unaEsperaTrasOperacionesEnSegundos )
                    
                                                        unOperationsDoneTrasUltimaEspera = 0
                                                        
                                                        if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                                            unMillisecondsFinUltimaEspera = fMillisecondsNow()
                                           
                                                
                                                
                                        elif ( unEstadoTraduccion == cEstadoTraduccionDefinitiva):
                                            if unaTraduccionEncoded == unaCadenaTraducida:
                
                                                theInformeImportarContenidos[ 'translations_unchanged'] += 1 
                                                theInformeImportarContenidos[ 'operations_done']   += 1
                                                
                                                unOperationsDoneTrasUltimaEspera += 1
                                                
                                                if ( unaEsperaTrasOperacionesEnSegundos >= 0.1) and ( unNumeroOperacionesAntesDeCederProcesador > 0) and ( unOperationsDoneTrasUltimaEspera >= unNumeroOperacionesAntesDeCederProcesador):
                                                    unMustSleep = True
                                                    if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                                        unMillisecondsComienzoEspera = fMillisecondsNow()
                                                        if ( unMillisecondsComienzoEspera - unMillisecondsFinUltimaEspera) < unPeriodoActividadSinEsperaEnMilisegundos:
                                                            unMustSleep = False
                    
                                                    if unMustSleep:                                    
                                                        time.sleep( unaEsperaTrasOperacionesEnSegundos )
                    
                                                        unOperationsDoneTrasUltimaEspera = 0
                                                        
                                                        if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                                            unMillisecondsFinUltimaEspera = fMillisecondsNow()
                        
                                                
                                            else:
                
                                                theInformeImportarContenidos[ 'translations_ignored'] += 1 
                                                theInformeImportarContenidos[ 'operations_done']   += 1
                                                
                                                
                                                unOperationsDoneTrasUltimaEspera += 1
                                                
                                                if ( unaEsperaTrasOperacionesEnSegundos >= 0.1) and ( unNumeroOperacionesAntesDeCederProcesador > 0) and ( unOperationsDoneTrasUltimaEspera >= unNumeroOperacionesAntesDeCederProcesador):
                                                    unMustSleep = True
                                                    if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                                        unMillisecondsComienzoEspera = fMillisecondsNow()
                                                        if ( unMillisecondsComienzoEspera - unMillisecondsFinUltimaEspera) < unPeriodoActividadSinEsperaEnMilisegundos:
                                                            unMustSleep = False
                    
                                                    if unMustSleep:                                    
                                                        time.sleep( unaEsperaTrasOperacionesEnSegundos )
                    
                                                        unOperationsDoneTrasUltimaEspera = 0
                                                        
                                                        if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                                            unMillisecondsFinUltimaEspera = fMillisecondsNow()
                        
                                                
                                    theInformeImportarContenidos[ 'processed_translations'] += 1
        
                                            
                        # ######################################################
                        """Create String Translations for Languages missing in the import content.
                        
                        """
                        if unaEsCadenaRecienCreada:                    
                            unosCodigosIdiomasTraduccionesQueFaltan =  unSetTodosCodigosIdiomas  - unosCodigosIdiomasTraduccionesCreadas
                        else:
                            unosCodigosIdiomasTraduccionesAComprobar   = unSetTodosCodigosIdiomasInicial.difference( unosCodigosIdiomasTraduccionesCreadas).difference( unosCodigosIdiomasTraduccionesEncontradas)
                            unasTraduccionesAComprobar                 = unaCadena.fTraduccionesPorIdiomas( unosCodigosIdiomasTraduccionesAComprobar, thePloneUtilsTool) 
                            unosCodigosIdiomasTraduccionesNoExistentes = set( [ unCodIdioma  for  unCodIdioma in unosCodigosIdiomasTraduccionesAComprobar if not unasTraduccionesAComprobar.has_key( unCodIdioma)])
                            unosCodigosIdiomasTraduccionesQueFaltan    = unSetCodigosIdiomasACrear.difference( unosCodigosIdiomasTraduccionesCreadas).union( unosCodigosIdiomasTraduccionesNoExistentes)
                             
                            unOperationsJustDone = len( set( todosCodigosIdiomas).union( set( unosCodigosIdiomasACrear)).difference( set( unosCodigosIdiomasTraduccionesQueFaltan)).difference( unosCodigosIdiomasTraduccionesEncontradas).difference( unosCodigosIdiomasTraduccionesCreadas))
                            theInformeImportarContenidos[ 'operations_done']   += unOperationsJustDone

                            unOperationsDoneTrasUltimaEspera += unOperationsJustDone
                            
                            if ( unaEsperaTrasOperacionesEnSegundos >= 0.1) and ( unNumeroOperacionesAntesDeCederProcesador > 0) and ( unOperationsDoneTrasUltimaEspera >= unNumeroOperacionesAntesDeCederProcesador):
                                unMustSleep = True
                                if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                    unMillisecondsComienzoEspera = fMillisecondsNow()
                                    if ( unMillisecondsComienzoEspera - unMillisecondsFinUltimaEspera) < unPeriodoActividadSinEsperaEnMilisegundos:
                                        unMustSleep = False

                                if unMustSleep:                                    
                                    time.sleep( unaEsperaTrasOperacionesEnSegundos )

                                    unOperationsDoneTrasUltimaEspera = 0
                                    
                                    if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                        unMillisecondsFinUltimaEspera = fMillisecondsNow()
                        
                            
                            
                        for unCodigoIdiomaQueFalta in  unosCodigosIdiomasTraduccionesQueFaltan:
                            unaNuevaTraduccion = self.fCrearTraduccionPendiente( 
                                theCodigoIdioma                     =unCodigoIdiomaQueFalta, 
                                theCadena                           =unaCadena, 
                                theSimboloCadena                    =unSimboloCadena,  
                                theIdCadena                         =unaIdCadena, 
                                theNombresModulos                   =unosNombresModulos, 
                                theMemberId                         =theMemberId, 
                                thePloneUtilsTool                   =thePloneUtilsTool, 
                                theCatalogBusquedaTraducciones      =unosCatalogsBusquedaTraduccionesPorIdioma[  unCodigoIdiomaQueFalta], 
                                theCatalogFiltroTraducciones        =unosCatalogsFiltroTraduccionesPorIdioma[    unCodigoIdiomaQueFalta], 
                                theCatalogTextoTraducciones         =unosCatalogsTextoTraduccionesPorIdioma[     unCodigoIdiomaQueFalta],
                                theTraduccionPermissionsSpecs       =someTraduccionPermissionsSpecs,
                                theTraduccionAcquireRoleAssignments =aTraduccionAcquireRoleAssignments,
                                thePermissionsCache                 =unPermissionsCache, 
                                theRolesCache                       =unRolesCache, 
                                theParentExecutionRecord            =unExecutionRecord,
                            )
                            if unaNuevaTraduccion:
                                theInformeImportarContenidos[ 'translation_creations_as_pending'] += 1 
                                unCurrentChangesHolder[ 0] += 1
                                theInformeImportarContenidos[ 'operations_done']   += 1
                                
                                unOperationsDoneTrasUltimaEspera += 1
                                
                                if ( unaEsperaTrasOperacionesEnSegundos >= 0.1) and ( unNumeroOperacionesAntesDeCederProcesador > 0) and ( unOperationsDoneTrasUltimaEspera >= unNumeroOperacionesAntesDeCederProcesador):
                                    unMustSleep = True
                                    if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                        unMillisecondsComienzoEspera = fMillisecondsNow()
                                        if ( unMillisecondsComienzoEspera - unMillisecondsFinUltimaEspera) < unPeriodoActividadSinEsperaEnMilisegundos:
                                            unMustSleep = False
    
                                    if unMustSleep:                                    
                                        time.sleep( unaEsperaTrasOperacionesEnSegundos )
    
                                        unOperationsDoneTrasUltimaEspera = 0
                                        
                                        if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                            unMillisecondsFinUltimaEspera = fMillisecondsNow()
                                
                            else:
                                # ######################################################
                                """Exit with error condition.
                                
                                """
                                theInformeImportarContenidos[ 'fecha_informe'] =self.fDateTimeNowTextual()
                                theInformeImportarContenidos[ 'error'] = "gvSIGi18n_TRACadena_failedTranslationCreation_error_msgid"
                                theInformeImportarContenidos[ 'error_detail'] = '%s %s' % ( unCodigoIdiomaQueFalta, unSimboloCadena , )
                                self.pPeriodicCommit( 
                                    theCatalogo, 
                                    theInformeImportarContenidos, 
                                    unIntervaloRefrescoEnNumeroEscrituras, 
                                    unIntervaloRefrescoEnMinutos, 
                                    unCurrentChangesHolder, unCurrentCommitsHolder, 
                                    unaEsperaEntreTransaccionesEnSegundos,
                                    unNumeroDeRefrescosPorEscrituraEnLog,
                                    unaFechaUltimoInformeProgresoHolder, 
                                    True,
                                    thePermissionsCache         =unPermissionsCache, 
                                    theRolesCache               =unRolesCache, 
                                    theParentExecutionRecord    =unExecutionRecord,                       
                                )
                                return self
                                
                         
                        theInformeImportarContenidos[ 'processed_strings'] += 1
                        
                    
                            
                    self.pPeriodicCommit( 
                        theCatalogo, 
                        theInformeImportarContenidos, 
                        unIntervaloRefrescoEnNumeroEscrituras, 
                        unIntervaloRefrescoEnMinutos, 
                        unaEsperaEntreTransaccionesEnSegundos,
                        unNumeroDeRefrescosPorEscrituraEnLog,
                        unCurrentChangesHolder, unCurrentCommitsHolder, 
                        unaFechaUltimoInformeProgresoHolder, 
                        False,
                        thePermissionsCache         =unPermissionsCache, 
                        theRolesCache               =unRolesCache, 
                        theParentExecutionRecord    =unExecutionRecord,                
                    )  

                self.pPeriodicCommit( 
                    theCatalogo, 
                    theInformeImportarContenidos, 
                    unIntervaloRefrescoEnNumeroEscrituras, 
                    unIntervaloRefrescoEnMinutos, 
                    unaEsperaEntreTransaccionesEnSegundos,
                    unNumeroDeRefrescosPorEscrituraEnLog,
                    unCurrentChangesHolder, unCurrentCommitsHolder,
                    unaFechaUltimoInformeProgresoHolder, 
                    True,
                    thePermissionsCache         =unPermissionsCache, 
                    theRolesCache               =unRolesCache, 
                    theParentExecutionRecord    =unExecutionRecord,                
                )  
                    
            finally:
                unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
        
            
            # ######################################################
            """Create Translations into the Languages just created for all previously existing Strings.
              
            """
            if unSetSimbolosNoImportados and unosCodigosIdiomasACrear:
                
                unSubExecutionRecord = self.fStartExecution( 'block',  'pImportarContenidosIntercambio-SubExecution to create translations (TRATraduccion) into the Languages just created for all previously existing Strings.', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
                try:
                
                    for unSimboloCadena in unSetSimbolosNoImportados:        
                        unaCadena = theCatalogo.fGetCadenaPorSimbolo( unSimboloCadena)
                        if not unaCadena: 
                            # ######################################################
                            """Exit with error condition.
                            
                            """
                            theInformeImportarContenidos[ 'fecha_informe'] =self.fDateTimeNowTextual()
                            theInformeImportarContenidos[ 'error'] = "gvSIGi18n_TRACadena_failedSearchBySimbolo_error_msgid"
                            theInformeImportarContenidos[ 'error_detail'] = unSimboloCadena        
                            self.pPeriodicCommit( 
                                theCatalogo, 
                                theInformeImportarContenidos, 
                                unIntervaloRefrescoEnNumeroEscrituras, 
                                unIntervaloRefrescoEnMinutos, 
                                unaEsperaEntreTransaccionesEnSegundos,
                                unNumeroDeRefrescosPorEscrituraEnLog,
                                unCurrentChangesHolder, unCurrentCommitsHolder, 
                                unaFechaUltimoInformeProgresoHolder, 
                                True,
                                thePermissionsCache         =unPermissionsCache, 
                                theRolesCache               =unRolesCache, 
                                theParentExecutionRecord    =unExecutionRecord,                       
                            )
                            return self
                                        
                        unaIdCadena = unaCadena.getId()
                        unosNombresModulos = unaCadena.getNombresModulos()
                        for unCodigoIdioma in unosCodigosIdiomasACrear:
                            
                            unaTraduccionEncontrada = unaCadena.fObtenerTraduccionPorCodigoIdioma( unCodigoIdioma,thePloneUtilsTool=thePloneUtilsTool)
                            if not( unaTraduccionEncontrada == None):
                                
                                theInformeImportarContenidos[ 'translations_unchanged'] += 1 
                                theInformeImportarContenidos[ 'operations_done']   += 1
                                
                                theInformeImportarContenidos[ 'translations_to_create_in_new_languages_for_preexisting_strings']   -= 1
                                
                                
                                unOperationsDoneTrasUltimaEspera += 1
                                
                                if ( unaEsperaTrasOperacionesEnSegundos >= 0.1) and ( unNumeroOperacionesAntesDeCederProcesador > 0) and ( unOperationsDoneTrasUltimaEspera >= unNumeroOperacionesAntesDeCederProcesador):
                                    unMustSleep = True
                                    if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                        unMillisecondsComienzoEspera = fMillisecondsNow()
                                        if ( unMillisecondsComienzoEspera - unMillisecondsFinUltimaEspera) < unPeriodoActividadSinEsperaEnMilisegundos:
                                            unMustSleep = False
    
                                    if unMustSleep:                                    
                                        time.sleep( unaEsperaTrasOperacionesEnSegundos )
    
                                        unOperationsDoneTrasUltimaEspera = 0
                                        
                                        if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                            unMillisecondsFinUltimaEspera = fMillisecondsNow()
                         
                            else:
                                unaNuevaTraduccion = self.fCrearTraduccionPendiente( 
                                    theCodigoIdioma                     =unCodigoIdioma, 
                                    theCadena                           =unaCadena, 
                                    theSimboloCadena                    =unSimboloCadena,  
                                    theIdCadena                         =unaIdCadena, 
                                    theNombresModulos                   =unosNombresModulos, 
                                    theMemberId                         =theMemberId, 
                                    thePloneUtilsTool                   =thePloneUtilsTool, 
                                    theCatalogBusquedaTraducciones      =unosCatalogsBusquedaTraduccionesPorIdioma[  unCodigoIdioma], 
                                    theCatalogFiltroTraducciones        =unosCatalogsFiltroTraduccionesPorIdioma[    unCodigoIdioma],
                                    theCatalogTextoTraducciones         =unosCatalogsTextoTraduccionesPorIdioma[     unCodigoIdioma],
                                    theTraduccionPermissionsSpecs       =someTraduccionPermissionsSpecs,
                                    theTraduccionAcquireRoleAssignments =aTraduccionAcquireRoleAssignments,
                                    thePermissionsCache                 =unPermissionsCache, 
                                    theRolesCache                       =unRolesCache, 
                                    theParentExecutionRecord            =unExecutionRecord,
                                )
                                if unaNuevaTraduccion:
                                    theInformeImportarContenidos[ 'translation_creations_as_pending'] += 1 
                                    unCurrentChangesHolder[ 0] += 1
                                    
                                    theInformeImportarContenidos[ 'translations_created_in_new_languages_for_preexisting_strings'] += 1
                                    theInformeImportarContenidos[ 'operations_done']   += 1
                                    
                                    unOperationsDoneTrasUltimaEspera += 1
                                    
                                    if ( unaEsperaTrasOperacionesEnSegundos >= 0.1) and ( unNumeroOperacionesAntesDeCederProcesador > 0) and ( unOperationsDoneTrasUltimaEspera >= unNumeroOperacionesAntesDeCederProcesador):
                                        unMustSleep = True
                                        if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                            unMillisecondsComienzoEspera = fMillisecondsNow()
                                            if ( unMillisecondsComienzoEspera - unMillisecondsFinUltimaEspera) < unPeriodoActividadSinEsperaEnMilisegundos:
                                                unMustSleep = False
        
                                        if unMustSleep:                                    
                                            time.sleep( unaEsperaTrasOperacionesEnSegundos )
        
                                            unOperationsDoneTrasUltimaEspera = 0
                                            
                                            if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                                unMillisecondsFinUltimaEspera = fMillisecondsNow()
                                    
                                else:
                                    # ######################################################
                                    """Exit with error condition.
                                    
                                    """
                                    theInformeImportarContenidos[ 'fecha_informe'] =self.fDateTimeNowTextual()
                                    theInformeImportarContenidos[ 'error'] = "gvSIGi18n_TRACadena_failedTranslationCreation_error_msgid"
                                    theInformeImportarContenidos[ 'error_detail'] = '%s %s' % ( unCodigoIdioma, unSimboloCadena , )
                                    self.pPeriodicCommit( 
                                        theCatalogo, 
                                        theInformeImportarContenidos, 
                                        unIntervaloRefrescoEnNumeroEscrituras, 
                                        unIntervaloRefrescoEnMinutos, 
                                        unaEsperaEntreTransaccionesEnSegundos,
                                        unNumeroDeRefrescosPorEscrituraEnLog,
                                        unCurrentChangesHolder, unCurrentCommitsHolder, 
                                        unaFechaUltimoInformeProgresoHolder, 
                                        True,
                                        thePermissionsCache         =unPermissionsCache, 
                                        theRolesCache               =unRolesCache, 
                                        theParentExecutionRecord    =unExecutionRecord,                       
                                    )
                                    return self
                                
                                
                                
                        self.pPeriodicCommit( 
                            theCatalogo, 
                            theInformeImportarContenidos, 
                            unIntervaloRefrescoEnNumeroEscrituras, 
                            unIntervaloRefrescoEnMinutos, 
                            unaEsperaEntreTransaccionesEnSegundos,
                            unNumeroDeRefrescosPorEscrituraEnLog,
                            unCurrentChangesHolder, unCurrentCommitsHolder, 
                            unaFechaUltimoInformeProgresoHolder, 
                            False,
                            thePermissionsCache         =unPermissionsCache, 
                            theRolesCache               =unRolesCache, 
                            theParentExecutionRecord    =unExecutionRecord,
                        )       
                        
                    self.pPeriodicCommit( 
                        theCatalogo, 
                        theInformeImportarContenidos, 
                        unIntervaloRefrescoEnNumeroEscrituras, 
                        unIntervaloRefrescoEnMinutos, 
                        unaEsperaEntreTransaccionesEnSegundos,
                        unNumeroDeRefrescosPorEscrituraEnLog,
                        unCurrentChangesHolder, unCurrentCommitsHolder, 
                        unaFechaUltimoInformeProgresoHolder, 
                        True,
                        thePermissionsCache         =unPermissionsCache, 
                        theRolesCache               =unRolesCache, 
                        theParentExecutionRecord    =unExecutionRecord,
                    )
                        
                finally:
                    unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                    unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
            
                    
            
            # ######################################################
            """Create in all strings the Translations missing in any existing language.
              
            """
            if self.getDebeCrearTraduccionesQueFaltan():
                
                 
                
                unSubExecutionRecord = self.fStartExecution( 'block',  'pImportarContenidosIntercambio-SubExecution to create missing translations in all strings and languages (TRATraduccion) into the Languages just created for all previously existing Strings.', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
                try:
    
                    unAhoraString =self.fDateTimeNowTextual()
                    
                    unInformeCrearTraduccionesQueFaltan.update( {
                        'fecha_Informe': unAhoraString,
                        'start_date': unAhoraString,
                    })                
                    if not theUseCaseQueryResult_CrearTraduccionesQueFaltan or not theUseCaseQueryResult_CrearTraduccionesQueFaltan.get( 'success', False):
                        unInformeCrearTraduccionesQueFaltan[ 'error'] = "gvSIGi18n_NoPermission_error_msgid"
                        unInformeCrearTraduccionesQueFaltan[ 'end_date'] =self.fDateTimeNowTextual()
                        return theInformeImportarContenidos
                                
                        
                    unosSimbolosCadenasExistentes       = theCatalogo.fObtenerSimbolosTodasCadenasSinOrdenar()
                    unosIdiomasExistentes               = theCatalogo.fObtenerTodosIdiomas()
                    unosCodigosIdiomasExistentes        = [ unIdioma.getCodigoIdiomaEnGvSIG() for unIdioma in unosIdiomasExistentes]
                
                    for unSimboloCadena in unosSimbolosCadenasExistentes:        
                        unaCadena = theCatalogo.fGetCadenaPorSimbolo( unSimboloCadena)
                        if not unaCadena: 
                            # ######################################################
                            """Exit with error condition.
                            
                            """
                            unInformeCrearTraduccionesQueFaltan[ 'fecha_informe'] =self.fDateTimeNowTextual()
                            unInformeCrearTraduccionesQueFaltan[ 'error'] = "gvSIGi18n_TRACadena_failedSearchBySimbolo_error_msgid"
                            unInformeCrearTraduccionesQueFaltan[ 'error_detail'] = unSimboloCadena        
                            theInformeImportarContenidos[ 'fecha_informe'] =self.fDateTimeNowTextual()
                            theInformeImportarContenidos[ 'error'] = "gvSIGi18n_TRACadena_failedSearchBySimbolo_error_msgid"
                            theInformeImportarContenidos[ 'error_detail'] = unSimboloCadena        
                            self.pPeriodicCommit( 
                                theCatalogo, 
                                theInformeImportarContenidos, 
                                unIntervaloRefrescoEnNumeroEscrituras, 
                                unIntervaloRefrescoEnMinutos, 
                                unaEsperaEntreTransaccionesEnSegundos,
                                unNumeroDeRefrescosPorEscrituraEnLog,
                                unCurrentChangesHolder, unCurrentCommitsHolder, 
                                unaFechaUltimoInformeProgresoHolder, 
                                True,
                                thePermissionsCache         =unPermissionsCache, 
                                theRolesCache               =unRolesCache, 
                                theParentExecutionRecord    =unExecutionRecord,                       
                            )
                            return self
                                        
                        unasTraduccionesExistentes      = unaCadena.fTraduccionesPorIdiomas( unosCodigosIdiomasExistentes, thePloneUtilsTool) 

                        unaIdCadena = unaCadena.getId()                        
                        unosNombresModulos = unaCadena.getNombresModulos()
                        
                        for unCodigoIdioma in unosCodigosIdiomasExistentes:
                            unaTraduccionExistente = unasTraduccionesExistentes.get( unCodigoIdioma, None)
                            
                            if unaTraduccionExistente:
                                unInformeCrearTraduccionesQueFaltan[ 'operations_done']   += 1
                                theInformeImportarContenidos[ 'operations_done']   += 1
                                
                                unOperationsDoneTrasUltimaEspera += 1
                                
                                if ( unaEsperaTrasOperacionesEnSegundos >= 0.1) and ( unNumeroOperacionesAntesDeCederProcesador > 0) and ( unOperationsDoneTrasUltimaEspera >= unNumeroOperacionesAntesDeCederProcesador):
                                    unMustSleep = True
                                    if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                        unMillisecondsComienzoEspera = fMillisecondsNow()
                                        if ( unMillisecondsComienzoEspera - unMillisecondsFinUltimaEspera) < unPeriodoActividadSinEsperaEnMilisegundos:
                                            unMustSleep = False
    
                                    if unMustSleep:                                    
                                        time.sleep( unaEsperaTrasOperacionesEnSegundos )
    
                                        unOperationsDoneTrasUltimaEspera = 0
                                        
                                        if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                            unMillisecondsFinUltimaEspera = fMillisecondsNow()
                                
                                
                            else:
                            
                                unaNuevaTraduccion = self.fCrearTraduccionPendiente( 
                                    theCodigoIdioma                     =unCodigoIdioma, 
                                    theCadena                           =unaCadena, 
                                    theSimboloCadena                    =unSimboloCadena,  
                                    theIdCadena                         =unaIdCadena, 
                                    theNombresModulos                   =unosNombresModulos, 
                                    theMemberId                         =theMemberId, 
                                    thePloneUtilsTool                   =thePloneUtilsTool, 
                                    theCatalogBusquedaTraducciones      =unosCatalogsBusquedaTraduccionesPorIdioma[  unCodigoIdioma], 
                                    theCatalogFiltroTraducciones        =unosCatalogsFiltroTraduccionesPorIdioma[    unCodigoIdioma],
                                    theCatalogTextoTraducciones         =unosCatalogsTextoTraduccionesPorIdioma[     unCodigoIdioma],
                                    theTraduccionPermissionsSpecs       =someTraduccionPermissionsSpecs,
                                    theTraduccionAcquireRoleAssignments =aTraduccionAcquireRoleAssignments,
                                    thePermissionsCache                 =unPermissionsCache, 
                                    theRolesCache                       =unRolesCache, 
                                    theParentExecutionRecord            =unExecutionRecord,
                                )
                                if unaNuevaTraduccion:
                                    unInformeCrearTraduccionesQueFaltan[ 'translations_created'] += 1 
                                    unInformeCrearTraduccionesQueFaltan[ 'operations_done'] += 1 
                                    unCurrentChangesHolder[ 0] += 1
                                    
                                    theInformeImportarContenidos[ 'operations_done']   += 1
                                    
                                    unOperationsDoneTrasUltimaEspera += 1
                                    
                                    if ( unaEsperaTrasOperacionesEnSegundos >= 0.1) and ( unNumeroOperacionesAntesDeCederProcesador > 0) and ( unOperationsDoneTrasUltimaEspera >= unNumeroOperacionesAntesDeCederProcesador):
                                        unMustSleep = True
                                        if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                            unMillisecondsComienzoEspera = fMillisecondsNow()
                                            if ( unMillisecondsComienzoEspera - unMillisecondsFinUltimaEspera) < unPeriodoActividadSinEsperaEnMilisegundos:
                                                unMustSleep = False
        
                                        if unMustSleep:                                    
                                            time.sleep( unaEsperaTrasOperacionesEnSegundos )
        
                                            unOperationsDoneTrasUltimaEspera = 0
                                            
                                            if unPeriodoActividadSinEsperaEnMilisegundos > 0:
                                                unMillisecondsFinUltimaEspera = fMillisecondsNow()
                                    
                                else:
                                    # ######################################################
                                    """Exit with error condition.
                                    
                                    """
                                    unInformeCrearTraduccionesQueFaltan[ 'fecha_informe'] =self.fDateTimeNowTextual()
                                    unInformeCrearTraduccionesQueFaltan[ 'error'] = "gvSIGi18n_TRACadena_failedTranslationCreation_error_msgid"
                                    unInformeCrearTraduccionesQueFaltan[ 'error_detail'] = '%s %s' % ( unCodigoIdioma, unSimboloCadena , )
                                    theInformeImportarContenidos[ 'fecha_informe'] =self.fDateTimeNowTextual()
                                    theInformeImportarContenidos[ 'error'] = "gvSIGi18n_TRACadena_failedTranslationCreation_error_msgid"
                                    theInformeImportarContenidos[ 'error_detail'] = '%s %s' % ( unCodigoIdioma, unSimboloCadena , )
                                    self.pPeriodicCommit( 
                                        theCatalogo, 
                                        theInformeImportarContenidos, 
                                        unIntervaloRefrescoEnNumeroEscrituras, 
                                        unIntervaloRefrescoEnMinutos, 
                                        unaEsperaEntreTransaccionesEnSegundos,
                                        unNumeroDeRefrescosPorEscrituraEnLog,
                                        unCurrentChangesHolder, unCurrentCommitsHolder, 
                                        unaFechaUltimoInformeProgresoHolder, 
                                        True,
                                        thePermissionsCache         =unPermissionsCache, 
                                        theRolesCache               =unRolesCache, 
                                        theParentExecutionRecord    =unExecutionRecord,                       
                                    )
                                    return self
                                
                                
                                
                        self.pPeriodicCommit( 
                            theCatalogo, 
                            theInformeImportarContenidos, 
                            unIntervaloRefrescoEnNumeroEscrituras, 
                            unIntervaloRefrescoEnMinutos, 
                            unaEsperaEntreTransaccionesEnSegundos,
                            unNumeroDeRefrescosPorEscrituraEnLog,
                            unCurrentChangesHolder, unCurrentCommitsHolder, 
                            unaFechaUltimoInformeProgresoHolder, 
                            False,
                            thePermissionsCache         =unPermissionsCache, 
                            theRolesCache               =unRolesCache, 
                            theParentExecutionRecord    =unExecutionRecord,
                        )       
                        
                    self.pPeriodicCommit( 
                        theCatalogo, 
                        theInformeImportarContenidos, 
                        unIntervaloRefrescoEnNumeroEscrituras, 
                        unIntervaloRefrescoEnMinutos, 
                        unaEsperaEntreTransaccionesEnSegundos,
                        unNumeroDeRefrescosPorEscrituraEnLog,
                        unCurrentChangesHolder, unCurrentCommitsHolder, 
                        unaFechaUltimoInformeProgresoHolder, 
                        True,
                        thePermissionsCache         =unPermissionsCache, 
                        theRolesCache               =unRolesCache, 
                        theParentExecutionRecord    =unExecutionRecord,
                    )
                        
                    unInformeCrearTraduccionesQueFaltan[ 'fecha_informe'] =self.fDateTimeNowTextual()
                    
                finally:
                    unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                    unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
            
                    
     
            return self
    
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
 

              

    
    
    
    
    
    
    
    
    
    security.declarePrivate( 'pPeriodicCommit')    
    def pPeriodicCommit( self, 
        theCatalogo,  
        theInformeImportarContenidos, 
        theIntervaloRefrescoEnNumeroEscrituras, 
        theIntervaloRefrescoEnMinutos, 
        theEsperaEntreTransaccionesEnSegundos,
        theNumeroDeRefrescosPorEscrituraEnLog,
        theCurrentChangesHolder, 
        theCurrentCommitsHolder,
        theFechaUltimoInformeProgresoHolder, 
        theForceCommit,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):
        
        from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fMillisecondsNow, fDateTimeNow
        
        unosMillisNow = fMillisecondsNow()
        if not ( theForceCommit or ( theCurrentChangesHolder[ 0] >= theIntervaloRefrescoEnNumeroEscrituras) or ( int(( unosMillisNow - theFechaUltimoInformeProgresoHolder[ 0].millis()) / 60000) >= theIntervaloRefrescoEnMinutos)):
            return self
        
        unExecutionRecord = self.fStartExecution( 'block',  'pPeriodicCommit', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }, '%d changes (total %d)' % (theCurrentChangesHolder[ 0], theCurrentChangesHolder[ 0]+theInformeImportarContenidos[ 'total_changes'], )) 
        try:
            
            aNumLastChanges   = theCurrentChangesHolder[ 0]
            theCurrentChangesHolder[ 0] = 0
            
            theInformeImportarContenidos[ 'total_changes'] += aNumLastChanges
            
            theCurrentChangesHolder[ 1] += aNumLastChanges
            theCurrentCommitsHolder[ 0] += 1
            
            
                
    
            # ################################################################
            """If so configured,write to the log every certain number of commits, not at every commit.
            
            """
            if theForceCommit or ( theNumeroDeRefrescosPorEscrituraEnLog <= 1) or ( theCurrentCommitsHolder[ 0] >= theNumeroDeRefrescosPorEscrituraEnLog):

                
                unAhora = fDateTimeNow()
                theFechaUltimoInformeProgresoHolder[ 0] = unAhora
                
                theInformeImportarContenidos[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                self.setInformeProgreso( str( theInformeImportarContenidos))
                self.setFechaUltimoInformeProgreso( unAhora)
    
                
                # ################################################################
                """If so configured, shall Go to sleep to give a change to execute to other processes and user requests. 
                
                """
                unaEsperaEntreTransaccionesEnSegundos = 0
                if theEsperaEntreTransaccionesEnSegundos:
                    unaEsperaEntreTransaccionesEnSegundos = min( theEsperaEntreTransaccionesEnSegundos, cMaxWaitBetweenTransactions)
                    if not ( unaEsperaEntreTransaccionesEnSegundos > cMinWaitBetweenTransactions):
                        unaEsperaEntreTransaccionesEnSegundos = 0
                
                unSleepSentence = ''
                if unaEsperaEntreTransaccionesEnSegundos > cMinWaitBetweenTransactions:
                    unSleepSentence = 'Going to sleep %.1f' % unaEsperaEntreTransaccionesEnSegundos
                
                logging.getLogger( 'gvSIGi18n::Importar').info("%d COMMITS after %d changes (total changes %d)   %s" % ( theCurrentCommitsHolder[ 0], theCurrentChangesHolder[ 1], theInformeImportarContenidos[ 'total_changes'], unSleepSentence) )        

                theCurrentChangesHolder[ 1] = 0
                theCurrentCommitsHolder[ 0] = 0
                
                
                
                theCatalogo.pFlushCachedTemplates_All()                            
                
                # ACV OJO 200912161030 This was outside of theForceCommit .... condition above, committing every time !!! Now moved under the condition
                # ################################################################
                """COMMIT NOW
                
                """
                transaction.commit( )
                
                
            
            
                # ACV OJO 200912161030 This was outside of theForceCommit .... condition above, committing every time !!! Now moved under the condition
                # ################################################################
                """If so configured, Go to sleep NOW. Abort on wake-up to refresh the view on the object network.
                
                """
                if unaEsperaEntreTransaccionesEnSegundos > cMinWaitBetweenTransactions:
                    
                    time.sleep( unaEsperaEntreTransaccionesEnSegundos * 1.0)
                    
                    transaction.abort( )
                
                
            return self
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
 

   
    


    

    

    security.declarePrivate( 'fCrearCadenaImportada')    
    def fCrearCadenaImportada( self, 
        theCatalogo, 
        theColeccionCadenas, 
        theSimboloCadena, 
        theNombresModulos, 
        theSources,
        theIdNumber, 
        theMemberId, 
        thePloneUtilsTool, 
        theCatalogBusquedaCadenas, 
        theCatalogFiltroCadenas, 
        theCatalogTextoCadenas,
        theCadenaPermissionsSpecs,
        theCadenaAcquireRoleAssignments,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):
        
        if not theSimboloCadena:
            return None
            
        unIdNumber = theIdNumber + 1
        
        aNewIdWithCounter = "%s%s" % ( cCadenaIdPrefix, str( unIdNumber))
        aRetry = True
        while aRetry:
            aRetry = False
            unaCadenaPorId= self.getCadenaPorID( aNewIdWithCounter)
            if unaCadenaPorId:
                unIdNumber = unIdNumber + 1
                aNewIdWithCounter = "%s%s" % ( cCadenaIdPrefix, str( unIdNumber))
                aRetry = True
            else:
                break

        if thePloneUtilsTool:
            aNewIdWithCounter = thePloneUtilsTool.normalizeString( aNewIdWithCounter)
            
        anAttrsDict = { 
# ACV 20090814 
#   EATR01 Remove Attribute pathDelRaiz from all entities; 	
#   EATR02 Remove the Type attribute from catalog schemas
#            'pathDelRaiz':              theCatalogo.fPathDelRaiz(),
            'title':                    theSimboloCadena,
            'description':              '',
            'simbolo':                  theSimboloCadena,
            'estadoCadena':             cEstadoCadenaActiva,  
            'fechaCreacionTextual':    self.fDateTimeNowTextual(),
            'usuarioCreador':           theMemberId,
            'fechaCancelacion':         None,
            'nombresModulos':           '\n'.join( theNombresModulos),
            'referenciasFuentes':      theSources,
        }
        
        unaIdNuevaCadena = theColeccionCadenas.invokeFactory( cNombreTipoTRACadena, aNewIdWithCounter, **anAttrsDict)
        if not unaIdNuevaCadena:
            return None
            
        unaNuevaCadena = theColeccionCadenas.getElementoPorID( unaIdNuevaCadena)
        if not unaNuevaCadena:
            return None

        self.pAfterAddNuevaCadena( 
            unaNuevaCadena,
            theCatalogBusquedaCadenas, 
            theCatalogFiltroCadenas, 
            theCatalogTextoCadenas,
            theCadenaPermissionsSpecs,
            theCadenaAcquireRoleAssignments,
            thePermissionsCache         =thePermissionsCache, 
            theRolesCache               =thePermissionsCache, 
            theParentExecutionRecord    =thePermissionsCache,
            )
             
        return [ unaNuevaCadena, unIdNumber, ]
        
        
    
    
    
    
    security.declarePrivate('pAfterAddNuevaCadena')
    def pAfterAddNuevaCadena( self, 
        theNuevaCadena, 
        theCatalogBusquedaCadenas, 
        theCatalogFiltroCadenas, 
        theCatalogTextoCadenas,
        theCadenaPermissionsSpecs,
        theCadenaAcquireRoleAssignments,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):
        
        if not theNuevaCadena:
            return self
        
        theNuevaCadena.pAddToCatalogs( theCatalogBusquedaCadenas, theCatalogFiltroCadenas, theCatalogTextoCadenas)       
            
        theNuevaCadena.manage_fixupOwnershipAfterAdd()
        
        for unaPermission in cPermissionsToDenyEverywhereToEverybody:
            theNuevaCadena.manage_permission( unaPermission, roles=[], acquire=False)
        
        if theCadenaPermissionsSpecs:
            for unaPermission in theCadenaPermissionsSpecs.keys():
                unaPermissionSpec   = theCadenaPermissionsSpecs[ unaPermission]
                unAcquire           = unaPermissionSpec[ 'acquire_permissions'] 
                unosRoles           = list( unaPermissionSpec[ 'roles'])
                
                if unaPermission:
                    theNuevaCadena.manage_permission( unaPermission, roles=unosRoles, acquire=unAcquire)
                    
                    
        self.fSetAcquiringRoleAssignments( theNuevaCadena, True)
                            
        return self
 

    
    
    
    

    security.declarePrivate('fCrearTraduccionImportada')
    def fCrearTraduccionImportada( self, 
        theCodigoIdioma, 
        theCadena, 
        theSimboloCadena, 
        theIdCadena, 
        theTraduccionEncoded, 
        theNombresModulos, 
        theMemberId, 
        thePloneUtilsTool, 
        theCatalogBusquedaTraducciones, 
        theCatalogFiltroTraducciones, 
        theCatalogTextoTraducciones,
        theTraduccionPermissionsSpecs,
        theTraduccionAcquireRoleAssignments,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):

        if not theCadena or not theCodigoIdioma or not theIdCadena or not theSimboloCadena:
            return None
            
        unTitulo = '%s-%s' % ( theSimboloCadena, theCodigoIdioma)
        aNewId = theCadena.fIdTraduccionEnLenguage( theCodigoIdioma, thePloneUtilsTool)

        unDateStoreString =self.fDateTimeNowTextual()
        
        unEstadoTraduccion = cEstadoTraduccionPendiente
        unUsuarioTraductor = ''
        unaFechaTraduccion = ''
        if theTraduccionEncoded:
            unEstadoTraduccion = cEstadoTraduccionTraducida
            unUsuarioTraductor = theMemberId
            unaFechaTraduccion = unDateStoreString

                    
        anAttrsDict = { 
# ACV 20090814 
#   EATR01 Remove Attribute pathDelRaiz from all entities; 	
#   EATR02 Remove the Type attribute from catalog schemas
#            'pathDelRaiz':          theCadena.fPathDelRaiz(),
            'title':                unTitulo,
            'description':          '',
            'simbolo':              theSimboloCadena,
            'codigoIdiomaEnGvSIG':  theCodigoIdioma, 
            'estadoCadena':         cEstadoCadenaActiva,
            'idCadena':             theIdCadena,
            'nombresModulos':       theNombresModulos,
            'estadoTraduccion'   :  unEstadoTraduccion,
            'cadenaTraducida'    :  theTraduccionEncoded,
            'usuarioCreador':       theMemberId, 
            'fechaCreacionTextual': unDateStoreString,  
            'usuarioTraductor':     unUsuarioTraductor, 
            'fechaTraduccionTextual':      unaFechaTraduccion,  
            'usuarioRevisor':       None, 
            'fechaRevisionTextual': None,  
            'usuarioCoordinador':   None, 
            'fechaDefinitivoTextual':      None,  
            'comentario':           '',   
            'historia':             '',  
        }
        
        unaIdNuevaTraduccion = theCadena.invokeFactory( cNombreTipoTRATraduccion, aNewId, **anAttrsDict)
        if not unaIdNuevaTraduccion:
            return None
        unaNuevaTraduccion = theCadena.getElementoPorID( unaIdNuevaTraduccion)
        if not unaNuevaTraduccion:
            return None
            
        self.pAfterAddNuevaTraduccion( 
            unaNuevaTraduccion,
            theCatalogBusquedaTraducciones, 
            theCatalogFiltroTraducciones, 
            theCatalogTextoTraducciones,
            theTraduccionPermissionsSpecs,
            theTraduccionAcquireRoleAssignments,
            thePermissionsCache         =thePermissionsCache, 
            theRolesCache               =thePermissionsCache, 
            theParentExecutionRecord    =thePermissionsCache,
            )
        
        return unaNuevaTraduccion
        
        
    
    
    


    
    
    

    security.declarePrivate('fCrearTraduccionPendiente')
    def fCrearTraduccionPendiente( self, 
        theCodigoIdioma, 
        theCadena, 
        theSimboloCadena, 
        theIdCadena, 
        theNombresModulos, 
        theMemberId, 
        thePloneUtilsTool, 
        theCatalogBusquedaTraducciones, 
        theCatalogFiltroTraducciones, 
        theCatalogTextoTraducciones,
        theTraduccionPermissionsSpecs,
        theTraduccionAcquireRoleAssignments,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):
        
        if not theCadena or not theCodigoIdioma:
            return None
            
        unTitulo = '%s-%s' % ( theSimboloCadena, theCodigoIdioma)
        aNewId = theCadena.fIdTraduccionEnLenguage( theCodigoIdioma, thePloneUtilsTool)
        
        unDateStoreString =self.fDateTimeNowTextual()

        anAttrsDict = { 
# ACV 20090814 
#   EATR01 Remove Attribute pathDelRaiz from all entities; 	
#   EATR02 Remove the Type attribute from catalog schemas
#            'pathDelRaiz':          theCadena.fPathDelRaiz(),
            'title':                unTitulo,
            'description':          '',
            'simbolo':              theSimboloCadena,
            'codigoIdiomaEnGvSIG':  theCodigoIdioma, 
            'estadoCadena':         cEstadoCadenaActiva,
            'idCadena':             theIdCadena,
            'nombresModulos':       theNombresModulos,
            'estadoTraduccion'   :  cEstadoTraduccionPendiente,
            'cadenaTraducida'    :  '',
            'usuarioCreador':       theMemberId, 
            'fechaCreacionTextual': unDateStoreString,  
            'usuarioTraductor':     '', 
            'fechaTraduccionTextual':      None,  
            'usuarioRevisor':       None, 
            'fechaRevisionTextual': None,  
            'usuarioCoordinador':   None, 
            'fechaDefinitivoTextual':      None,  
            'comentario':           "",   
            'historia':             "",            
        }
        
        unaIdNuevaTraduccion = theCadena.invokeFactory( cNombreTipoTRATraduccion, aNewId, **anAttrsDict)
        if not unaIdNuevaTraduccion:
            return None
        unaNuevaTraduccion   = theCadena.getElementoPorID( unaIdNuevaTraduccion)
        if not unaNuevaTraduccion:
            return None
            
        self.pAfterAddNuevaTraduccion( 
            unaNuevaTraduccion,
            theCatalogBusquedaTraducciones, 
            theCatalogFiltroTraducciones, 
            theCatalogTextoTraducciones,
            theTraduccionPermissionsSpecs,
            theTraduccionAcquireRoleAssignments,
            thePermissionsCache         =thePermissionsCache, 
            theRolesCache               =thePermissionsCache, 
            theParentExecutionRecord    =thePermissionsCache,
            )
                
        return unaNuevaTraduccion


        


    
    
    
    
    
    security.declarePrivate('pAfterAddNuevaTraduccion')
    def pAfterAddNuevaTraduccion( self, 
        theNuevaTraduccion, 
        theCatalogBusquedaTraducciones, 
        theCatalogFiltroTraducciones, 
        theCatalogTextoTraducciones,
        theTraduccionPermissionsSpecs,
        theTraduccionAcquireRoleAssignments,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):
        
        if not theNuevaTraduccion:
            return self
        
        theNuevaTraduccion.pAddToCatalogs( theCatalogBusquedaTraducciones, theCatalogFiltroTraducciones, theCatalogTextoTraducciones)        
        
        theNuevaTraduccion.manage_fixupOwnershipAfterAdd()
        
        if theTraduccionPermissionsSpecs:
            for unaPermission in theTraduccionPermissionsSpecs.keys():
                unaPermissionSpec   = theTraduccionPermissionsSpecs[ unaPermission]
                unAcquire           = unaPermissionSpec[ 'acquire_permissions'] 
                unosRoles           = list( unaPermissionSpec[ 'roles'])
                
                if unaPermission:
                    theNuevaTraduccion.manage_permission( unaPermission, roles=unosRoles, acquire=unAcquire)
        
        for unaPermission in cPermissionsToDenyEverywhereToEverybody:
            theNuevaTraduccion.manage_permission( unaPermission, roles=[], acquire=False)
        
        self.fSetAcquiringRoleAssignments( theNuevaTraduccion, True)
        
        return self
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    security.declareProtected( permissions.View, 'fInformeProgreso')    
    def fInformeProgreso( self,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):
        
        if not self.getHaComenzado():
            return None
        
        unInformeString = self.getInformeProgreso()
        if not unInformeString:
            return None
        
        unInforme = self.fEvalString( unInformeString)
        return unInforme
    
    



    
    security.declareProtected( permissions.View, 'fInformeFinal')    
    def fInformeFinal( self,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):
        
        if not self.getHaComenzado():
            return None
        
        unInformeString = self.getInformeFinal()
        if not unInformeString:
            return None
        
        unInforme = self.fEvalString( unInformeString)
        return unInforme
    
    
    
    
    
 
    security.declareProtected( permissions.View, 'fInformeExcepcion')    
    def fInformeExcepcion( self,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):
        
        if not self.getHaComenzado():
            return None
        
        unInformeString = self.getInformeExcepcion()
        if not unInformeString:
            return None
        
        unInforme = self.fEvalString( unInformeString)
        return unInforme
        
    
       

    
    
    
    
    
    
    
    
    
    
    

    security.declarePrivate( 'pEliminarInformesEstado')    
    def pEliminarInformesEstado( self,
        theUseCaseQueryResult       =None,
        theCheckPermissions         =False,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):

        unExecutionRecord = self.fStartExecution( 'method',  'pEliminarInformesEstado', theParentExecutionRecord,  False) 
         
        try:
          
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                
            if theCheckPermissions:
                unUseCaseQueryResult = theUseCaseQueryResult
                if not unUseCaseQueryResult or not ( unUseCaseQueryResult.get( 'use_case_name', '') == cUseCase_ImportTRAImportacion):
                    unUseCaseQueryResult = self.fUseCaseAssessment(  
                        theUseCaseName          = cUseCase_CreateAndDeleteTRAInformeInTRAImportacion,        
                        theElementsBindings     = { cBoundObject: self,},                                    
                        theRulesToCollect       = None,                                                      
                        thePredicateOverrides   = { self.getCatalogo().UID(): { 'fAllowWrite': True, }, },
                        thePermissionsCache     = unPermissionsCache,                                        
                        theRolesCache           = unRolesCache,                                              
                        theParentExecutionRecord= unExecutionRecord,                                          
                    )
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    return self
        
            unosInformesEstado = self.fObtenerTodosInformes()
            
            someIdsToDelete = [ unInformeEstado.getId() for unInformeEstado in unosInformesEstado]
            
            self.manage_delObjects( someIdsToDelete)
                
            return self

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
        
    

    
    
    


    security.declarePrivate( 'pCrearInformeEstado')    
    def pCrearInformeEstado( self, 
        theTituloInformeEstado,
        theUseCaseQueryResult       =None,
        theCheckPermissions         =False,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):

        unExecutionRecord = self.fStartExecution( 'method',  'pCrearInformeEstado', theParentExecutionRecord,  False) 
        
        try:
         
            if not theTituloInformeEstado:
                return self
                
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                
            if theCheckPermissions:
                unUseCaseQueryResult = theUseCaseQueryResult
                if not unUseCaseQueryResult or not ( unUseCaseQueryResult.get( 'use_case_name', '') == cUseCase_CreateAndDeleteTRAInformeInTRAImportacion):
                    unUseCaseQueryResult = self.fUseCaseAssessment(  
                        theUseCaseName          = cUseCase_CreateAndDeleteTRAInformeInTRAImportacion,        
                        theElementsBindings     = { cBoundObject: self,},                                    
                        theRulesToCollect       = [ 'languages', 'modules',],                                                      
                        thePredicateOverrides   = { self.getCatalogo().UID(): { 'fAllowWrite': True, }, },
                        thePermissionsCache     = unPermissionsCache,                                        
                        theRolesCache           = unRolesCache,                                              
                        theParentExecutionRecord= unExecutionRecord,                                          
                    )
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    return self

                
            unInformeEstado = None
            try:
                unInformeEstado = self[ theTituloInformeEstado]
            except:
                None
            
            if not unInformeEstado:
                unaIdNuevoInforme = ''
                try:
                    unaIdNuevoInforme  = self.invokeFactory(  cNombreTipoTRAInforme, theTituloInformeEstado,  title=theTituloInformeEstado )            
                except:
                    None
                
                if not unaIdNuevoInforme:
                    return None
    
                unInformeEstado = self.getElementoPorID( unaIdNuevoInforme)
                if not unInformeEstado:
                    return None
    
                unInformeEstado.manage_fixupOwnershipAfterAdd()
                unInformeEstado.pSetPermissions()
                
            if not unInformeEstado:
                return None
            
            
            unInformeEstado.fElaborarInforme( 
                theUseCaseQueryResult       =None,
                theForceEllaboration        =True, 
                theCheckPermissions         =False,
                thePermissionsCache         =unPermissionsCache, 
                theRolesCache               =unRolesCache, 
                theParentExecutionRecord    =unExecutionRecord
            )
                
            return self

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
        
        
      


    
    
    
  
# ####################################
#  Accessors : Informes
#
     
    security.declareProtected( permissions.View, 'fObtenerTodosInformes')
    def fObtenerTodosInformes( self, ):
   
        unosElementos = self.objectValues ( cNombreTipoTRAInforme) #
        return unosElementos
           
     
    
        


    security.declarePrivate( 'fInformeEstadoAntes')    
    def fInformeEstadoAntes( self):
        unosInformesEstado = self.fObtenerTodosInformes()
        if not unosInformesEstado:
            return None
            
        return unosInformesEstado[ 0]


    

    security.declarePrivate( 'fInformeEstadoDespues')    
    def fInformeEstadoDespues( self):
        unosInformesEstado = self.fObtenerTodosInformes()
        if not unosInformesEstado or ( len( unosInformesEstado) < 2):
            return None
            
        return unosInformesEstado[ 1]
    
    
    





    
    


    security.declarePrivate( 'fDeriveInformeEstadoIdiomasAntes')    
    def fDeriveInformeEstadoIdiomasAntes( self):
        unInformeEstadoAntes = self.fInformeEstadoAntes()
        if not unInformeEstadoAntes :
            return ''
        
        unInformeIdiomas = unInformeEstadoAntes.getInformeIdiomas()
        return unInformeIdiomas
    
    
    

    security.declarePrivate( 'fDeriveInformeEstadoModulosAntes')    
    def fDeriveInformeEstadoModulosAntes( self):
        unInformeEstadoAntes = self.fInformeEstadoAntes()
        if not unInformeEstadoAntes :
            return ''
        
        unInformeModulos = unInformeEstadoAntes.getInformeModulos()
        return unInformeModulos
    
    
    
    security.declarePrivate( 'fDeriveInformeEstadoIdiomasDespues')    
    def fDeriveInformeEstadoIdiomasDespues( self):
        unInformeEstadoDespues = self.fInformeEstadoDespues()
        if not unInformeEstadoDespues :
            return ''
        
        unInformeIdiomas = unInformeEstadoDespues.getInformeIdiomas()
        return unInformeIdiomas
    
    
    

    security.declarePrivate( 'fDeriveInformeEstadoModulosDespues')    
    def fDeriveInformeEstadoModulosDespues( self):
        unInformeEstadoDespues = self.fInformeEstadoDespues()
        if not unInformeEstadoDespues :
            return ''
        
        unInformeModulos = unInformeEstadoDespues.getInformeModulos()
        return unInformeModulos
    
        

        

    security.declareProtected( permissions.View, 'fInformeEstadoModulosAntes')
    def fInformeEstadoModulosAntes( self):

        unInformeString = self.fDeriveInformeEstadoModulosAntes()
        if not unInformeString:
            return None
            
        unInforme = self.fEvalString( unInformeString)
        return unInforme
         
    
    
    
    security.declareProtected( permissions.View, 'fInformeEstadoIdiomasAntes')
    def fInformeEstadoIdiomasAntes( self):

        unInformeString = self.fDeriveInformeEstadoIdiomasAntes()
        if not unInformeString:
            return None
            
        unInforme = self.fEvalString( unInformeString)
        return unInforme
         
 
        
    
    security.declareProtected( permissions.View, 'fInformeEstadoModulosDespues')
    def fInformeEstadoModulosDespues( self):

        unInformeString = self.fDeriveInformeEstadoModulosDespues()
        if not unInformeString:
            return None
            
        unInforme = self.fEvalString( unInformeString)
        return unInforme
         
    
    
    
    security.declareProtected( permissions.View, 'fInformeEstadoIdiomasDespues')
    def fInformeEstadoIdiomasDespues( self):

        unInformeString = self.fDeriveInformeEstadoIdiomasDespues()
        if not unInformeString:
            return None
            
        unInforme = self.fEvalString( unInformeString)
        return unInforme
    
    
   

    
    

    
    security.declareProtected( permissions.ModifyPortalContent, 'fReutilizarImportacion')
    def fReutilizarImportacion( self , thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fReutilizarImportacion', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators  import ModelDDvlPloneTool_Mutators, cModificationKind_CreateSubElement, cModificationKind_Create, cModificationKind_ChangeValues

        try:
            
            try:
                
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_ReuseTRAImportacion, 
                    theElementsBindings     = { cBoundObject: self,},
                    theRulesToCollect       = [ ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord
                )
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    return False
                        
                                    
                unHaComenzado = self.getHaComenzado()
                
                if unHaComenzado:
                    self.setHaComenzado( False)
                    
                    aModelDDvlPloneTool_Mutators = ModelDDvlPloneTool_Mutators()
                   
                    aReport = aModelDDvlPloneTool_Mutators.fNewVoidChangeValuesReport()
                    someFieldReports    = aReport.get( 'field_reports')
                    aFieldReportsByName = aReport.get( 'field_reports_by_name')       

                    aReportForField = { 'attribute_name': 'haComenzado', 'effect': 'changed', 'new_value': False, 'previous_value': True,}                                                                                                                        
                    
                    someFieldReports.append( aReportForField)
                    aFieldReportsByName[ 'haComenzado'] = aReportForField
                    
                    aModelDDvlPloneTool_Mutators.pSetAudit_Modification( self, cModificationKind_ChangeValues, aReport)  
                    
                    self.pFlushCachedTemplates_All()                            
                
                    transaction.commit()
                    logging.getLogger( 'gvSIGi18n').info( "COMMIT TRAImportacion::fReutilizarImportacion %s" % '/'.join( self.getPhysicalPath()))
                    
                return True
            
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during TRAIdioma::fReutilizarImportacion %s \n'  % '/'.join( self.getPhysicalPath())
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   

                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return False
        
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

                            
        
            
    
    security.declarePublic( 'fExtraLinks')    
    def fExtraLinks( self):
        
        unosExtraLinks = TRAElemento_Operaciones.fExtraLinks( self)
        if not unosExtraLinks:
            unosExtraLinks = [ ]
        
        unaURL = self.absolute_url()
        if not unaURL:
            return unosExtraLinks
        

        unExtraLink = self.fNewVoidExtraLink()
        unExtraLink.update( {
            'label'   : self.fTranslateI18N( 'plone', 'Summary', 'Summary-',),
            'href'    : '%s/TRAImportacionContenidosSumario/' % unaURL,
            'icon'    : '',
            'domain'  : 'plone',
            'msgid'   : 'Summary',
        })
        unosExtraLinks.append( unExtraLink)
                            
        unExtraLink = self.fNewVoidExtraLink()
        unExtraLink.update( {
            'label'   : self.fTranslateI18N( 'plone', 'Details', 'Details-',),
            'href'    : '%s/TRAImportacionContenidosDetalle/' % unaURL,
            'icon'    : '',
            'domain'  : 'plone',
            'msgid'   : 'Details',
        })
        unosExtraLinks.append( unExtraLink)
                            
                            
        unExtraLink = self.fNewVoidExtraLink()
        unExtraLink.update( {
            'label'   : self.fTranslateI18N( 'plone', 'Progress', 'Progress-',),
            'href'    : '%s/TRAImportacionProgreso/' % unaURL,
            'icon'    : '',
            'domain'  : 'plone',
            'msgid'   : 'Progress',
        })
        unosExtraLinks.append( unExtraLink)

        return unosExtraLinks
    
    