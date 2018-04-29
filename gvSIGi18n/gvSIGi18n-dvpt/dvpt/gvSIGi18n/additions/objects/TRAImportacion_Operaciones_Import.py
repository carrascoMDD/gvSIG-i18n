# -*- coding: utf-8 -*-
#
# File: TRAImportacion_Operaciones_Import.py
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



import os
import logging

import time

import transaction


from Products.CMFCore       import permissions

from TRAElemento_Constants_Translation import cMarcaDeComentarioSinCambios






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

from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_ImportTRAImportacion, cUseCase_CreateMissingTRATraduccion, cUseCase_ImportTRAImportacion_ToCreateCadenas, cUseCase_EstimateTRAImportacion, cUseCase_Restore_TRACatalogo

from TRAElemento_Permission_Definitions import cBoundObject, cPermissionsToDenyEverywhereToEverybody


from TRACatalogo_Inicializacion_Constants import cTRACatalogsDetailsParaCadenas, cTRACatalogsDetailsParaIdioma


from TRAColeccionSolicitudesCadenas_Operaciones import cEstadoSolicitudCadena_Pending

from TRAProcessErrorException import TRAProcessErrorException



class TRAImportacion_Operaciones_Import:
    """
    """
    security = ClassSecurityInfo()
     


    
 
    
    
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
            'string_sources_changes':    0,
            'translation_status_changes':    0,
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

    


    
    security.declarePrivate( 'fNewVoidInformeImportarXML')    
    def fNewVoidInformeImportarXML( self):
        unInforme = {
            'valid':                      True,
            'error':                      '',
            'error_detail':               '',
            'start_date':                 '',
            'end_date':                   '',
            'fecha_informe':              '',
            'total_changes':              0,
            'expected_num_nodes':         0,
            'expected_num_nodes_by_type': { },
            'imported_num_nodes':         0,
            'imported_num_nodes_by_type': { },
            'binary_file_names':          [ ],
            'catalogs_cadenas':           None,
            'catalogs_idiomas':           None,
            'must_run_recatalog_elements': False,
            
        }
        return unInforme

    

    
    
    
    security.declarePrivate( 'fNewVoidEstimarImportacionResult')    
    def fNewVoidEstimarImportacionResult( self):
        unInforme = {
            'success':                   False,
            'status':                    '',
            'exception':                 '',
            'import_contents_report':    self.fNewVoidInformeImportarContenidos(),
            'import_XML_report':         self.fNewVoidInformeImportarXML(),
        }   
        return unInforme
    
    
    
    
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

            
    
    
    
    

                         
                
            
            
            
            
    
    security.declareProtected( permissions.AddPortalContent, 'fEstimarCosteImportacion')    
    def fEstimarCosteImportacion( self, 
        theIsToCreateCadenas     =False,
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):
        """Estimate the number of operations of various kinds that would be performed during the execution of an import process with the TRAImportacion contents.
        
        """
  
        unExecutionRecord = self.fStartExecution( 'method',  'fEstimarCosteImportacion', theParentExecutionRecord, False) 

        
        unEstimarCosteImportacionResult = self.fNewVoidEstimarImportacionResult()
        
        
        
        unCatalogo = self.getCatalogo()
        if unCatalogo == None:
            unEstimarCosteImportacionResult.update( {
                'success':   False,
                'status':    'gvSIGi18n_Internal_Missing_TRACatalogo',
            })
            return unEstimarCosteImportacionResult
        
        
        

        unosIdiomasAccesibles = None
        unosModulosAccesibles = None
        
        
        try:

            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
                
            
            unUseCaseQueryResult = self.fUseCaseAssessment(  
                theUseCaseName          = cUseCase_EstimateTRAImportacion, 
                theElementsBindings     = { cBoundObject: self,}, 
                theRulesToCollect       = ['languages', 'modules',], 
                thePredicateOverrides   = { self.getCatalogo().UID(): { 'fAllowWrite': True, }, },
                thePermissionsCache     = unPermissionsCache, 
                theRolesCache           = unRolesCache, 
                theParentExecutionRecord= unExecutionRecord
            )
                            
                            
            if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                unEstimarCosteImportacionResult.update( {
                    'success':   False,
                    'status':    'gvSIGi18n_NoPermission_error_msgid',
                })
                return unEstimarCosteImportacionResult
                            
            unosIdiomasAccesibles = unUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'languages', {}).get( 'accepted_final_objects', [])
            unosModulosAccesibles = unUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'modules', {}).get( 'accepted_final_objects', [])
                    

            
            
            

            unContenido = self.fCombinedContenidosIntercambio( 
                theParentExecutionRecord= unExecutionRecord
            )


                
                
                
        
            aContenidoXML = self.fObtenerContenidoXML()
            
            
            
            
        
            if not( aContenidoXML == None):

                aModelDDvlPlone_tool = self.fModelDDvlPloneTool()
                if aModelDDvlPlone_tool == None:
                    unEstimarCosteImportacionResult.update( {
                        'success':   False,
                        'status':    'gvSIGi18n_Missing_ModelDDvlPlone_tool_internal_error_msgid',
                    })
                    return unEstimarCosteImportacionResult
                    
                
                aModelDDvlPloneTool_Import = aModelDDvlPlone_tool.fModelDDvlPloneTool_Import( unCatalogo)
                if aModelDDvlPloneTool_Import == None:
                    unEstimarCosteImportacionResult.update( {
                        'success':   False,
                        'status':    'gvSIGi18n_Missing_ModelDDvlPloneTool_Import_internal_error_msgid',
                    })
                    return unEstimarCosteImportacionResult
            
                            

    
    
            unMemberId = self.fGetMemberId()
            unIdNumber = unCatalogo.getHighestCadenaIdNumber()
            unIdNumberHolder = [ unIdNumber, ]
            
                   
            


            # #########################################
            """Estimate cost to import XML, if any.
            
            """
            if not( aContenidoXML == None):
                try:
                    try:
                        unInformeImportarXML   = unEstimarCosteImportacionResult.get( 'import_XML_report', {})
                        
                        unAhora = self.fDateTimeNow()
                        unInformeImportarXML[ 'start_date']    = self.fDateToStoreString( unAhora)
                        unInformeImportarXML[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                        
                        self.pImportarContenidoXML( 
                            theProcessControlManager    =None,
                            theJustEstimateCost         =True,
                            theCatalogo                 =unCatalogo, 
                            theUseCaseQueryResult       =unUseCaseQueryResult, 
                            theMemberId                 =unMemberId, 
                            theInformeImportarContenidoXML=unInformeImportarXML, 
                            theModelDDvlPlone_tool      =aModelDDvlPlone_tool,
                            theModelDDvlPloneTool_Import=aModelDDvlPloneTool_Import,
                            theContenidoXML             =aContenidoXML,
                            thePermissionsCache         =unPermissionsCache, 
                            theRolesCache               =unRolesCache, 
                            theParentExecutionRecord    =unExecutionRecord,
                        )

                        
                    except:
                        unaExceptionInfo = sys.exc_info()
                        unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                        
                        unInformeExcepcion = 'Exception during Estimate Cost of Import XML operation\n' 
                        try:
                            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                        except:
                            None
                        try:
                            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                        except:
                            None
                        unInformeExcepcion += unaExceptionFormattedTraceback   
                        
                        unEstimarCosteImportacionResult.update( {
                            'success':   False,
                            'status':    'Exception',
                            'exception': unInformeExcepcion,
                        })
    
                        unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
                        
                        logging.getLogger( 'gvSIGi18n').info("EXCEPTION: exception details follow:\n%s\n" % unInformeExcepcion) 
                                
                        return unEstimarCosteImportacionResult
                                
                    
                    
                finally:
                    unAhora = self.fDateTimeNow()
                    unAhoraString = self.fDateToStoreString( unAhora)
                    unInformeImportarXML[ 'fecha_informe'] = unAhoraString
                    unInformeImportarXML[ 'end_date']      = unAhoraString
                
            
                
                
                
                
            
            # #########################################
            """Estimate cost to import contents, if any.
            
            """
            if unContenido:
                aPloneUtilsTool = self.getPloneUtilsToolForNormalizeString()  
                try:
                    try:
                        unInformeImportarContenidos = unEstimarCosteImportacionResult.get( 'import_contents_report', {})
                        
                        unAhora = self.fDateTimeNow()
                        unAhoraString = self.fDateToStoreString( unAhora)
                        unInformeImportarContenidos[ 'start_date']    = unAhoraString
                        unInformeImportarContenidos[ 'fecha_informe'] = unAhoraString
                    
                 
                        unaColeccionCadenas = unCatalogo.fObtenerColeccionCadenas()
                        if not ( unaColeccionCadenas == None):
                            
                            self.pImportarContenidosIntercambio( 
                                theProcessControlManager    =None,
                                theJustEstimateCost         =True,
                                theCatalogo                 =unCatalogo, 
                                theUseCaseQueryResult       =unUseCaseQueryResult, 
                                theUseCaseQueryResult_CrearTraduccionesQueFaltan=None,
                                theIdiomasAccesibles        =unosIdiomasAccesibles, 
                                theModulosAccesibles        =unosModulosAccesibles, 
                                theColeccionCadenas         =unaColeccionCadenas, 
                                theIdNumberHolder           =unIdNumberHolder, 
                                theMemberId                 =unMemberId, 
                                theContenido                =unContenido, 
                                theSolicitudesCadenasUIDsPorSimbolo=None,
                                theInformeImportarContenidos=unInformeImportarContenidos, 
                                thePloneUtilsTool           =aPloneUtilsTool,
                                thePermissionsCache         =unPermissionsCache, 
                                theRolesCache               =unRolesCache, 
                                theParentExecutionRecord    =unExecutionRecord,
                            )
                    except:
                        unaExceptionInfo = sys.exc_info()
                        unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                        
                        unInformeExcepcion = 'Exception during Estimate Cost of Import Contents operation\n' 
                        try:
                            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                        except:
                            None
                        try:
                            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                        except:
                            None
                        unInformeExcepcion += unaExceptionFormattedTraceback   
                        
                        unEstimarCosteImportacionResult.update( {
                            'success':   False,
                            'status':    'Exception',
                            'exception': unInformeExcepcion,
                        })
    
                        unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
                        
                        logging.getLogger( 'gvSIGi18n').info("EXCEPTION: exception details follow:\n%s\n" % unInformeExcepcion) 
                                
                        return unEstimarCosteImportacionResult
                                
                    
                    
                finally:
                    unAhora = self.fDateTimeNow()
                    unAhoraString = self.fDateToStoreString( unAhora)
                    unInformeImportarContenidos[ 'fecha_informe'] = unAhoraString
                    unInformeImportarContenidos[ 'end_date']      = unAhoraString

                        
                
                
                
            unEstimarCosteImportacionResult.update( {
                'success':   True,
            })
            return unEstimarCosteImportacionResult
 
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
     
    
                
                            
     
    
    
    
    
    security.declareProtected( permissions.AddPortalContent, 'fImportarContenidoXMLeIntercambio')    
    def fImportarContenidoXMLeIntercambio( self, 
        theProcessControlManager =None,
        theIsToCreateCadenas     =False,
        theSolicitudesCadenasUIDsPorSimbolo =None,
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):
        
  
        unExecutionRecord = self.fStartExecution( 'method',  'fImportarContenidoXMLeIntercambio', theParentExecutionRecord, False) 

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators  import cModificationKind_CreateSubElement, cModificationKind_Create, cModificationKind_ChangeValues

        
        try:

            unSubExecutionRecord = self.fStartExecution( 'block',  'fImportarContenidoXMLeIntercambio-SubExecution to retrieve TRACatalog and accessible languages and modules', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
                        
            
            unImportResult = theProcessControlManager.vResult
            if not unImportResult:
                return None

            unInformeImportarXML = unImportResult.get( 'import_XML_report', {})
            unInformeImportarContenidos = unImportResult.get( 'import_contents_report', {})
            
            unCatalogo = self.getCatalogo()
            if unCatalogo == None:
                unInformeImportarContenidos[ 'error'] = "gvSIGi18n_NoRootCatalog_error_msgid"
                unInformeImportarContenidos[ 'end_date'] =self.fDateTimeNowTextual()
                return unInformeImportarContenidos
            
            #theProcessControlManager.pProcessStep( unCatalogo, { unCatalogo.meta_type: 1,}, { unCatalogo.meta_type: 1,})
            
            try:
                 
        
                  
                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)
                    
        
                aContenidoXML = self.fObtenerContenidoXML()
            
                
                aUseCaseNameToAssess = cUseCase_ImportTRAImportacion
                
                if not ( aContenidoXML == None):
                    aUseCaseNameToAssess = cUseCase_Restore_TRACatalogo
                    
                elif theIsToCreateCadenas:
                    aUseCaseNameToAssess  = cUseCase_ImportTRAImportacion_ToCreateCadenas
                    
                
                    
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = aUseCaseNameToAssess, 
                    theElementsBindings     = { cBoundObject: self,}, 
                    theRulesToCollect       = ['languages', 'modules',], 
                    thePredicateOverrides   = { self.getCatalogo().UID(): { 'fAllowWrite': True, }, self.UID(): { 'fHasNoProgressElementOrNotExecuted': True,},},
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
                        thePredicateOverrides   = { self.getCatalogo().UID(): { 'fAllowWrite': True, }, self.UID(): { 'fHasNoProgressElementOrNotExecuted': True,},},
                        thePermissionsCache     = unPermissionsCache, 
                        theRolesCache           = unRolesCache, 
                        theParentExecutionRecord= unExecutionRecord
                    )
                    if not unUseCaseQueryResult_CrearTraduccionesQueFaltan or not unUseCaseQueryResult_CrearTraduccionesQueFaltan.get( 'success', False):
                        unInformeImportarContenidos[ 'error'] = "gvSIGi18n_NoPermissionToCreateMissingTranslations_error_msgid"
                        unInformeImportarContenidos[ 'end_date'] =self.fDateTimeNowTextual()
                        return unInformeImportarContenidos
                    
                    
            finally:
                unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
                
          
                 
            unContenido = None
            unSubExecutionRecord = self.fStartExecution( 'block',  'fImportarContenidoXMLeIntercambio-SubExecution to retrieve translations interchange contents', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
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
                
          
                
                
                

    
    
            unMemberId = self.fGetMemberId()
            unIdNumber = unCatalogo.getHighestCadenaIdNumber()
            unIdNumberHolder = [ unIdNumber, ]
            
            aPloneUtilsTool = self.getPloneUtilsToolForNormalizeString()  
                   
            unAhora =self.fDateTimeNow()
            
            unInformeImportarContenidos[ 'fecha_informe'] = self.fDateToStoreString( unAhora)


          

                
                
                
                
            
            unSubExecutionRecord = self.fStartExecution( 'block',  'fImportarContenidoXMLeIntercambio-SubExecution Import XML contents.', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
            try:    
            
                if not ( aContenidoXML == None):
                    
                    aModelDDvlPlone_tool = self.fModelDDvlPloneTool()
                    if aModelDDvlPlone_tool == None:
                        unInformeImportarContenidos[ 'error'] = "gvSIGi18n_Missing_ModelDDvlPlone_tool_internal_error_msgid"
                        unInformeImportarContenidos[ 'end_date'] =self.fDateTimeNowTextual()
                        return unInformeImportarContenidos
                        
                    
                    aModelDDvlPloneTool_Import = aModelDDvlPlone_tool.fModelDDvlPloneTool_Import( unCatalogo)
                    if aModelDDvlPloneTool_Import == None:
                        unInformeImportarContenidos[ 'error'] = "gvSIGi18n_Missing_ModelDDvlPloneTool_Import_internal_error_msgid"
                        unInformeImportarContenidos[ 'end_date'] =self.fDateTimeNowTextual()
                        return unInformeImportarContenidos
                                    
                    
                    unInformeImportarXML[ 'start_date'] =self.fDateTimeNowTextual()
                    
                    self.pImportarContenidoXML(
                        theProcessControlManager =theProcessControlManager,
                        theJustEstimateCost         =False,
                        theCatalogo                 =unCatalogo, 
                        theUseCaseQueryResult       =unUseCaseQueryResult, 
                        theMemberId                 =unMemberId, 
                        theInformeImportarContenidoXML=unInformeImportarXML, 
                        theModelDDvlPlone_tool      =aModelDDvlPlone_tool,
                        theModelDDvlPloneTool_Import=aModelDDvlPloneTool_Import,
                        theContenidoXML             =aContenidoXML,
                        thePermissionsCache         =unPermissionsCache, 
                        theRolesCache               =unRolesCache, 
                        theParentExecutionRecord    =unExecutionRecord,
                    )
                    
                    unInformeImportarXML[ 'end_date'] =self.fDateTimeNowTextual()
       
                    if not unInformeImportarXML.get( 'valid', False):
                        unInformeImportarContenidos[ 'error'] = "gvSIGi18n_Import_Invalid_unInformeImportarXML_from_pImportarContenidoXML_failed_error_msgid"
                        unInformeImportarContenidos[ 'end_date'] =self.fDateTimeNowTextual()
                        return unInformeImportarContenidos
                    
                    
            finally:
                unCatalogo.pInvalidateSimbolosCadenasOrdenados()  
                                    
                transaction.commit( )

                unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
                
                logging.getLogger( 'gvSIGi18n').info("COMMIT XML import changes")  
                
                unCatalogo.pFlushCachedTemplates_All()                                 
                
                
                
            # ######################################
            """Retrieve UseCase assessment results after import, as there may be additional languages or modules.
            
            """
            unUseCaseQueryResult = self.fUseCaseAssessment(  
                theUseCaseName          = aUseCaseNameToAssess, 
                theElementsBindings     = { cBoundObject: self,}, 
                theRulesToCollect       = ['languages', 'modules',], 
                thePredicateOverrides   = { self.getCatalogo().UID(): { 'fAllowWrite': True, }, self.UID(): { 'fHasNoProgressElementOrNotExecuted': True,},},
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
                    thePredicateOverrides   = { self.getCatalogo().UID(): { 'fAllowWrite': True, }, self.UID(): { 'fHasNoProgressElementOrNotExecuted': True,},},
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord
                )
                if not unUseCaseQueryResult_CrearTraduccionesQueFaltan or not unUseCaseQueryResult_CrearTraduccionesQueFaltan.get( 'success', False):
                    unInformeImportarContenidos[ 'error'] = "gvSIGi18n_NoPermissionToCreateMissingTranslations_error_msgid"
                    unInformeImportarContenidos[ 'end_date'] =self.fDateTimeNowTextual()
                    return unInformeImportarContenidos
                
                
                
                
                
                
            # ###############################
            """Import translations interchange content.
            
            """
 
            unaColeccionCadenas = unCatalogo.fObtenerColeccionCadenas()
            if ( unaColeccionCadenas == None):
                unInformeImportarContenidos[ 'end_date'] =self.fDateTimeNowTextual()
                return unInformeImportarContenidos
                    
                
                
            unSubExecutionRecord = self.fStartExecution( 'block',  'fImportarContenidoXMLeIntercambio-SubExecution Import Languages, Modules, Strings and Translations contents.', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
            try:    
                unInformeImportarContenidos[ 'start_date'] =self.fDateTimeNowTextual()
                
                self.pImportarContenidosIntercambio( 
                    theProcessControlManager    =theProcessControlManager,
                    theJustEstimateCost         =False,
                    theCatalogo                 =unCatalogo, 
                    theUseCaseQueryResult       =unUseCaseQueryResult, 
                    theUseCaseQueryResult_CrearTraduccionesQueFaltan=unUseCaseQueryResult_CrearTraduccionesQueFaltan,
                    theIdiomasAccesibles        =unosIdiomasAccesibles, 
                    theModulosAccesibles        =unosModulosAccesibles, 
                    theColeccionCadenas         =unaColeccionCadenas, 
                    theIdNumberHolder           =unIdNumberHolder, 
                    theMemberId                 =unMemberId, 
                    theContenido                =unContenido, 
                    theSolicitudesCadenasUIDsPorSimbolo =theSolicitudesCadenasUIDsPorSimbolo,
                    theInformeImportarContenidos=unInformeImportarContenidos, 
                    thePloneUtilsTool           =aPloneUtilsTool,
                    thePermissionsCache         =unPermissionsCache, 
                    theRolesCache               =unRolesCache, 
                    theParentExecutionRecord    =unExecutionRecord,
                )
                
        
                
            finally:
                unCatalogo.pInvalidateSimbolosCadenasOrdenados()  

                transaction.commit( )
                
                unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
                
                logging.getLogger( 'gvSIGi18n').info("COMMIT FINAL changes")  
                
                unCatalogo.pFlushCachedTemplates_All() 
            
                
                
  
    
            unAhora =self.fDateTimeNow()
            
            unInformeImportarContenidos[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
            unInformeImportarContenidos[ 'end_date']      = self.fDateToStoreString( unAhora)
                
                
            return unInformeImportarContenidos
            

  
        finally:
            self.getCatalogo().pFlushCachedTemplates_All()        
            
            unExecutionRecord and unExecutionRecord.pEndExecution()
     
                
                
        
       
        
        
        
        
        
        

    
        

    
    
    
        
    # ###################################################################
    """IMPORT PROCESS
    
    """
                
                
    
    security.declarePrivate( 'pImportarContenidosIntercambio')    
    def pImportarContenidosIntercambio( self,
        theProcessControlManager                =None,
        theJustEstimateCost                     =None,
        theCatalogo                             =None, 
        theUseCaseQueryResult                   =None, 
        theUseCaseQueryResult_CrearTraduccionesQueFaltan =None,
        theIdiomasAccesibles                    =None, 
        theModulosAccesibles                    =None, 
        theColeccionCadenas                     =None,
        theIdNumberHolder                       =None, 
        theMemberId                             =None, 
        theContenido                            =None, 
        theSolicitudesCadenasUIDsPorSimbolo     =None,
        theInformeImportarContenidos            =None, 
        thePloneUtilsTool                       =None,
        thePermissionsCache                     =None, 
        theRolesCache                           =None, 
        theParentExecutionRecord                =None):
        """Import translations.
        
        Main loops to create languages, modules, strings and translations.
        
        """
        unExecutionRecord = self.fStartExecution( 'method',  'pImportarContenidosIntercambio', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }) 


        
        try:
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
                
            
            if not theInformeImportarContenidos:
                if theProcessControlManager:
                    raise TRAProcessErrorException( "gvSIGi18n_MissingParameters_internal_error_msgid", 'theInformeImportarContenidos',)
                return self
            
            
            if theCatalogo == None:
                unAhora =self.fDateTimeNow()
                theInformeImportarContenidos[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                theInformeImportarContenidos[ 'error'] = "gvSIGi18n_MissingParameters_internal_error_msgid"
                theInformeImportarContenidos[ 'error_detail'] = 'theCatalogo'
                if theProcessControlManager:
                    raise TRAProcessErrorException( theInformeImportarContenidos[ 'error'], theInformeImportarContenidos[ 'error_detail'],)
                return self
            
            
            if not theUseCaseQueryResult or not theUseCaseQueryResult.get( 'success', False):
                unAhora =self.fDateTimeNow()
                theInformeImportarContenidos[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                theInformeImportarContenidos[ 'error'] = "gvSIGi18n_UseCaseNotPermitted_error_msgid"
                if theUseCaseQueryResult:
                    theInformeImportarContenidos[ 'error_detail'] = theUseCaseQueryResult.get( 'use_case_name', '')       
                else:
                    theInformeImportarContenidos[ 'error_detail'] = ''
                    
                if theProcessControlManager:
                    raise TRAProcessErrorException( theInformeImportarContenidos[ 'error'], theInformeImportarContenidos[ 'error_detail'],)
                return self
    

            if not theContenido:
                unAhora =self.fDateTimeNow()
                theInformeImportarContenidos[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                theInformeImportarContenidos[ 'error'] = "gvSIGi18n_MissingParameters_internal_error_msgid"
                theInformeImportarContenidos[ 'error_detail'] = 'theContenido'
                if theProcessControlManager:
                    raise TRAProcessErrorException( theInformeImportarContenidos[ 'error'], theInformeImportarContenidos[ 'error_detail'],)
                return self
            
            
            unaColeccionIdiomas = theCatalogo.fObtenerColeccionIdiomas()
            if ( unaColeccionIdiomas == None):
                unAhora =self.fDateTimeNow()
                theInformeImportarContenidos[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                theInformeImportarContenidos[ 'error'] = "gvSIGi18n_Missing_ColeccionIdiomas_internal_error_msgid"
                theInformeImportarContenidos[ 'error_detail'] = ''
                if theProcessControlManager:
                    raise TRAProcessErrorException( theInformeImportarContenidos[ 'error'], theInformeImportarContenidos[ 'error_detail'],)
                return self
            
            
            unaColeccionModulos = theCatalogo.fObtenerColeccionModulos()
            if ( unaColeccionModulos == None):
                unAhora =self.fDateTimeNow()
                theInformeImportarContenidos[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                theInformeImportarContenidos[ 'error'] = "gvSIGi18n_Missing_ColeccionModulos_internal_error_msgid"
                theInformeImportarContenidos[ 'error_detail'] = ''
                if theProcessControlManager:
                    raise TRAProcessErrorException( theInformeImportarContenidos[ 'error'], theInformeImportarContenidos[ 'error_detail'],)
                return self
            
            
            
            aScannedData = theContenido.get( 'content_data', None)
            if not aScannedData:
                return self
            

            
            
            unSubExecutionRecord = self.fStartExecution( 'block',  'pImportarContenidosIntercambio-SubExecution to determine elements to create (languages, modules, strings) and count the number of translations to process.', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
            try:
            
    

                # ######################################################
                """Determine Modules to Create.
                
                """
                todosModulos  = theCatalogo.fObtenerTodosModulos()
                
                todosNombresModulos          = [ unModulo.Title() for unModulo in todosModulos]
                unosNombresModulosAccesibles = [ unModulo.Title() for unModulo in theModulosAccesibles] 
                
                unosNombresModulosAIgnorar = set()
                unosNombresModulosACrear   = set()
                
                unosNombresModulos = aScannedData[ 'modules']
              
                for unNombreModulo in unosNombresModulos:
                    if unNombreModulo:
                        if unNombreModulo in todosNombresModulos:
                            if not ( unNombreModulo in unosNombresModulosAccesibles):
                                unosNombresModulosAIgnorar.add( unNombreModulo)   
                        else:
                            unosNombresModulosACrear.add( unNombreModulo)
                            
                unosNombresModulosACrear = sorted( unosNombresModulosACrear)
                        
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
                
                unosCodigosIdiomas   = aScannedData[ 'languages']
                todosDetallesIdiomas = aScannedData.get( 'languages_details', {})
                
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
                
                unasCombinedStrings       = aScannedData[ 'symbols']
                unasCombinedStringsDict   = aScannedData[ 'symbols_dict']
                
                for unaCombinedString in unasCombinedStrings:
                    unSymbol = unaCombinedString.get( cScannedKeys_String_Symbol, '')
                    if unSymbol:
                        unasCombinedStringsDict[ unSymbol] = unaCombinedString
                
                unosSimbolosAImportar       = unasCombinedStringsDict.keys()
                unSetSimbolosAImportar      = set( unosSimbolosAImportar)
                unSetSimbolosACrear         = unSetSimbolosAImportar  - unSetSimbolosExistentes
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
                    unaCombinedString = unasCombinedStringsDict[ unSimboloCadena]
                    unasImportedTraduccionesPorIdioma        = unaCombinedString[ cScannedKeys_String_Translations]
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
                    
                        unModuloCreationReport = unaColeccionModulos.fCrearModulo( 
                            theTimeProfilingResults =None,  
                            theModelDDvlPloneTool_Mutators   =None, 
                            theNewTypeName          =unNombreModulo, 
                            theNewOneTitle          =unNombreModulo, 
                            theNewOneDescription    ='', 
                            theAdditionalParams     ={ 'rules_to_bypass': [ 'catalogo',],},
                            thePermissionsCache     =unPermissionsCache,
                            theRolesCache           =unRolesCache,
                            theParentExecutionRecord=unSubSubExecutionRecord)
                        
                        if ( not unModuloCreationReport) or ( not unModuloCreationReport.get( 'effect', '') == 'created') or ( not unModuloCreationReport.get( 'new_object_result', None)):
                            unAhora =self.fDateTimeNow()
                            theInformeImportarContenidos[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                            theInformeImportarContenidos[ 'error'] = "gvSIGi18n_ModuleCreationError_error_msgid"
                            
                            unErrorDetail = unNombreModulo
                            unActionFailure =  unModuloCreationReport.get( 'failure', '') 
                            if unActionFailure:
                                unErrorDetail = '%s %s' % ( unErrorDetail, unActionFailure,)
                            theInformeImportarContenidos[ 'error_detail'] = unErrorDetail
                            
                            raise TRAProcessErrorException( theInformeImportarContenidos[ 'error'], theInformeImportarContenidos[ 'error_detail'],)
                                              
                        unNuevoModulo = unModuloCreationReport.get( 'new_object_result', {}).get( 'object', None)
                        if unNuevoModulo == None:
                            unAhora =self.fDateTimeNow()
                            theInformeImportarContenidos[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                            theInformeImportarContenidos[ 'error'] = "gvSIGi18n_ModuleCreationError_error_msgid"
                            theInformeImportarContenidos[ 'error_detail'] = unNombreModulo            
                            raise TRAProcessErrorException( theInformeImportarContenidos[ 'error'], theInformeImportarContenidos[ 'error_detail'],)
                        
                        
                        theInformeImportarContenidos[ 'module_creations'] += 1
                        theInformeImportarContenidos[ 'operations_done']   += 1

                        theProcessControlManager.pProcessStep( unNuevoModulo, {}, { unNuevoModulo.meta_type: 1,})
                            
                        
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
            
                        
                        unNuevoIdioma =  unaColeccionIdiomas.fCrearIdioma(  
                            theUseCaseQueryResult         =theUseCaseQueryResult, 
                            theCodigoIdiomaEnGvSIG        =unCodigoIdioma, 
                            theCodigoInternacionalDeIdioma=unCodigoInternacionalIdioma, 
                            theTitle                      =unNombreEnglishIdioma, 
                            theNombreInglesIdioma         =unNombreEnglishIdioma, 
                            theNombreNativoIdioma         =unNombreNativoIdioma,
                            thePermissionsCache           =unPermissionsCache, 
                            theRolesCache                 =unRolesCache, 
                            theParentExecutionRecord      =unSubSubExecutionRecord,
                        )
                        
                        if not( unNuevoIdioma == None):
                            todosCodigosIdiomas.append( unCodigoIdioma)
                            theInformeImportarContenidos[ 'language_creations'] += 1
                            theInformeImportarContenidos[ 'operations_done']   += 1
                            
                            theProcessControlManager.pProcessStep( unNuevoIdioma, {}, { unNuevoIdioma.meta_type: 1,})

                            
                        else:
                            # ######################################################
                            """Exit with error condition.
                            
                            """
                            unAhora =self.fDateTimeNow()  
                            theInformeImportarContenidos[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                            theInformeImportarContenidos[ 'error'] = "gvSIGi18n_TRAIdiomaCreationFailure_error_msgid"
                            theInformeImportarContenidos[ 'error_detail'] = unCodigoIdioma
                            raise TRAProcessErrorException( theInformeImportarContenidos[ 'error'], theInformeImportarContenidos[ 'error_detail'],)
            
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
    
                someCadenaPermissionsSpecs          = self.fPermissionsForElementType(         cNombreTipoTRACadena)     
                aCadenaAcquireRoleAssignments       = self.fAcquireRoleAssignmentsElementType( cNombreTipoTRACadena)
                
                someTraduccionPermissionsSpecs      = self.fPermissionsForElementType(         cNombreTipoTRATraduccion)     
                aTraduccionAcquireRoleAssignments   = self.fAcquireRoleAssignmentsElementType( cNombreTipoTRATraduccion) 
                
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
                unNumNombresModulos = len( unosNombresModulos)
                unCacheCadenasCreadas = { }        
                for unSimboloCadena in unSetSimbolosACrear:
        
                    
                    unaCombinedString               = unasCombinedStringsDict[ unSimboloCadena]

                    unosImportedNombresModulos      = unaCombinedString.get( cScannedKeys_String_Modules, None)
                    unosImportedSourcesList         = unaCombinedString.get( cScannedKeys_String_Sources, None)

                    unosImportedSources = ''
                    if unosImportedSourcesList:
                        unosImportedSources = ' '.join( unosImportedSourcesList)
                        

                    unPrevIdNumber = theIdNumberHolder[ 0]   
                    
                    unaCadenaEIdNumber = self.fCrearCadenaImportada( 
                        theCatalogo, 
                        theColeccionCadenas, 
                        unSimboloCadena, 
                        unosImportedNombresModulos, 
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
                        unAhora =self.fDateTimeNow()  # SALIENDO EN CONDICION DE ERROR
                        theInformeImportarContenidos[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                        theInformeImportarContenidos[ 'error'] = "gvSIGi18n_TRACadenaCreationError_error_msgid"
                        theInformeImportarContenidos[ 'error_detail'] = unSimboloCadena            
                        raise TRAProcessErrorException()
                    
                    
                    unaCadena   = unaCadenaEIdNumber[ 0]
                    unIdNumber  = unaCadenaEIdNumber[ 1]
                    
                    unSolicitudCadenaChangedElements = { unaCadena.meta_type: 1,}
                    
                    if theSolicitudesCadenasUIDsPorSimbolo:
                        unaSolicitudCadenaUID = theSolicitudesCadenasUIDsPorSimbolo.get( unSimboloCadena, '')
                        if unaSolicitudCadenaUID:
                            
                            unaSolicitudCadena = self.fElementoPorUID( unaSolicitudCadenaUID)
                            
                            if not ( unaSolicitudCadena == None):
                                unEstadoSolicitudCadena = unaSolicitudCadena.getEstadoSolicitudCadena()
                                
                                if unEstadoSolicitudCadena == cEstadoSolicitudCadena_Pending:
                                    
                                    unaSolicitudCadena.setEstadoSolicitudCadena( cEstadoSolicitudCadena_Created)
                                    unSolicitudCadenaChangedElements.update(  { unaSolicitudCadena.meta_type: 1,})
                    
                                
                    theInformeImportarContenidos[ 'string_creations'] += 1
                    theInformeImportarContenidos[ 'operations_done']  += 1
                    
                    theProcessControlManager.pProcessStep( unaCadena, {}, unSolicitudCadenaChangedElements)

                    

                    theIdNumberHolder[ 0] = unIdNumber
                    
                    unSetSimbolosExistentes.add( unSimboloCadena)
                    unCacheCadenasCreadas[ unSimboloCadena] = unaCadena
                     
                    
                    
            finally:
                unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
                
                    
                
                
    
                
             
    
            # ######################################################
            """Process translations, for all Strings to process
            
            """
            unSubExecutionRecord = self.fStartExecution( 'block',  'pImportarContenidosIntercambio-SubExecution to import translations (TRATraduccion).', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
            try:
            
                for unSimboloCadena in unosSimbolosAImportar:        
                    unaCombinedString = unasCombinedStringsDict[ unSimboloCadena]
                                        
                    unosImportedNombresModulos      = unaCombinedString.get( cScannedKeys_String_Modules, None)
                    unImportedSourcesList           = unaCombinedString.get( cScannedKeys_String_Sources, None)
                    
                    unosImportedSources = ''
                    if unImportedSourcesList:
                        unosImportedSources = ' '.join( unImportedSourcesList)
                    
                    unasImportedTraduccionesPorIdioma       = unaCombinedString[ cScannedKeys_String_Translations]
                    unosImportedIdiomasTraducciones         = unasImportedTraduccionesPorIdioma.keys()
                    
                    unosNombresModulosToAppend = set()
                    if unosImportedNombresModulos:
                        unosNombresModulosToAppend = set( unosImportedNombresModulos).difference( unosNombresModulosAIgnorar)
                    
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
                            raise TRAProcessErrorException( theInformeImportarContenidos[ 'error'], theInformeImportarContenidos[ 'error_detail'],)
                        
                        
                        unasTraduccionesExistentes  = unaCadena.fTraduccionesPorIdiomas( unosImportedIdiomasTraducciones, thePloneUtilsTool) 
    
                        unAlreadyChangedCadena = False
                        
                    if unosNombresModulosToAppend:
                        if unaCadena.fAppendNombresModulos( unosNombresModulosToAppend):
                            unAlreadyChangedCadena = True
                            
                            theInformeImportarContenidos[ 'string_module_changes'] += 1 

                            unNumeroCambios = unaCadena.fPropagarCambioNombresModulosATraducciones()
                            
                            theProcessControlManager.pProcessStep( unaCadena, { unaCadena.meta_type: 1, cNombreTipoTRATraduccion: unNumeroCambios,}, { unaCadena.meta_type: 1, cNombreTipoTRATraduccion: unNumeroCambios,})

                    
                    if unosImportedSources:
                        if unaCadena.fAppendSources( unosImportedSources):
                            if not unAlreadyChangedCadena:
                                unAlreadyChangedCadena = True
                            
                                theInformeImportarContenidos[ 'string_sources_changes'] += 1 
                                
                                theProcessControlManager.pProcessStep( unaCadena, { unaCadena.meta_type: 1, }, { unaCadena.meta_type: 1, })
                               
                    unaIdCadena = unaCadena.getId()
                    unosNombresModulosCadena = unaCadena.getNombresModulos()
    
                    theProcessControlManager.pProcessStep( unaCadena, { unaCadena.meta_type: 1,}, {},)
                    
                    
                    # ######################################################
                    """Process String Translations, for each language 
                    
                    """
                    for unCodigoIdioma in unosImportedIdiomasTraducciones:
                        if not ( unCodigoIdioma in unosCodigosIdiomasAIgnorar):
                            
                            unaTraduccionScanned   = unasImportedTraduccionesPorIdioma[ unCodigoIdioma]
                            if unaTraduccionScanned:
                                
                                unaTraduccionEncoded            = unaTraduccionScanned[ cScannedKeys_Translation_Translation]
                                
                                unIndexOrStrEstadoTraduccionScanned       = unaTraduccionScanned.get( cScannedKeys_Translation_Status, None)
                                if isinstance( unIndexOrStrEstadoTraduccionScanned, str):
                                    unIndexEstadoTraduccionScanned = -1
                                    if unIndexOrStrEstadoTraduccionScanned:
                                        try:
                                            unIndexEstadoTraduccionScanned = int( unIndexOrStrEstadoTraduccionScanned)
                                        except:
                                            None
                                else:
                                    unIndexEstadoTraduccionScanned = unIndexOrStrEstadoTraduccionScanned
                                        
                                if ( unIndexEstadoTraduccionScanned < 0) or ( unIndexEstadoTraduccionScanned > len( cTodosEstados)):
                                    unEstadoTraduccionScanned = cEstadoTraduccionTraducida
                                
                                else:
                                    unEstadoTraduccionScanned  = cTodosEstados[ unIndexEstadoTraduccionScanned]

                                    
                                    
                                    
                                unComentarioTraduccionScanned   = unaTraduccionScanned.get( cScannedKeys_Translation_Comment, None)

                                
                                unCreationDateScanned     = unaTraduccionScanned.get( cScannedKeys_Translation_CreationDate,     None) or ''
                                unCreatorScanned          = unaTraduccionScanned.get( cScannedKeys_Translation_Creator,          None) or ''
                                unTranslationDateScanned  = unaTraduccionScanned.get( cScannedKeys_Translation_TranslationDate,  None) or ''
                                unTranslatorScanned       = unaTraduccionScanned.get( cScannedKeys_Translation_Translator,       None) or ''
                                unReviewDateScanned       = unaTraduccionScanned.get( cScannedKeys_Translation_ReviewDate,       None) or ''
                                unReviewerScanned         = unaTraduccionScanned.get( cScannedKeys_Translation_Reviewer,         None) or ''
                                unDefinitiveDateScanned   = unaTraduccionScanned.get( cScannedKeys_Translation_DefinitiveDate,   None) or ''
                                unCoordinatorScanned      = unaTraduccionScanned.get( cScannedKeys_Translation_Coordinator,      None) or ''
                                
                                
                                
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
                                            theNombresModulos                   =unosNombresModulosCadena,
                                            theEstadoTraduccion                 =unEstadoTraduccionScanned,
                                            theComment                          =unComentarioTraduccionScanned,
                                            theCreationDate                     =unCreationDateScanned,
                                            theCreator                          =unCreatorScanned,
                                            theTranslationDate                  =unTranslationDateScanned,
                                            theTranslator                       =unTranslatorScanned,
                                            theReviewDate                       =unReviewDateScanned,
                                            theReviewer                         =unReviewerScanned,
                                            theDefinitiveDate                   =unDefinitiveDateScanned,
                                            theCoordinator                      =unCoordinatorScanned,
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
                                        if not( unaNuevaTraduccion == None):
                                            unosCodigosIdiomasTraduccionesCreadas.add( unCodigoIdioma)
                                            theInformeImportarContenidos[ 'translation_creations'] += 1 
                                            theInformeImportarContenidos[ 'operations_done']   += 1
                                            
                                            theProcessControlManager.pProcessStep( unaNuevaTraduccion, {}, { unaNuevaTraduccion.meta_type: 1,})
    
                                        else:
                                            # ######################################################
                                            """Exit with error condition.
                                            
                                            """
                                            theInformeImportarContenidos[ 'fecha_informe'] =self.fDateTimeNowTextual()
                                            theInformeImportarContenidos[ 'error'] = "gvSIGi18n_TRACadena_failedTranslationCreation_error_msgid"
                                            theInformeImportarContenidos[ 'error_detail'] = '%s %s' % ( unCodigoIdioma, unSimboloCadena , )
                                            raise TRAProcessErrorException( theInformeImportarContenidos[ 'error'], theInformeImportarContenidos[ 'error_detail'],)
                                            
                                        
                                        
                                        
                                    else:
                                        # ######################################################
                                        """Update existing Translation, according to current state  and current and new translation.
                                        
                                        """
                                        
                                        unosCodigosIdiomasTraduccionesEncontradas.add( unCodigoIdioma)
                                        unEstadoTraduccion = unaTraduccionExistente.getEstadoTraduccion()
                                        unaCadenaTraducida = unaTraduccionExistente.getCadenaTraducida()
                                        
                                        
                                        unAhoraStoreString =self.fDateTimeNowTextual()
                                        
                                        
 
                                        
                                        if ( unEstadoTraduccion == cEstadoTraduccionPendiente) or ( not unaCadenaTraducida):
                                            # ######################################################
                                            """Existing Translation is pending: overwrite all information with values from new translations.
                                            
                                            """
                                            
    
                                            unaTraduccionExistente.setCadenaTraducida(            unaTraduccionEncoded)
                                            
                                            
                                            unUsuarioModificador = theMemberId
                                            unaFechaModificacion = unAhoraStoreString
                                            unUsuarioTraductor   = theMemberId
                                            unaFechaTraduccion   = unAhoraStoreString
                                            unUsuarioRevisor     = ''
                                            unaFechaRevision     = ''
                                            unUsuarioCoordinador = ''
                                            unaFechaDefinitivo   = ''
                                            
                                            if unTranslationDateScanned and unTranslatorScanned:
                                                unUsuarioTraductor   = unTranslatorScanned
                                                unaFechaTraduccion   = unTranslationDateScanned
                                                unUsuarioModificador = unTranslatorScanned
                                                unaFechaModificacion = unTranslationDateScanned
                                            else:
                                                unUsuarioTraductor   = theMemberId
                                                unaFechaTraduccion   = unAhoraStoreString
                                                unUsuarioModificador = theMemberId
                                                unaFechaModificacion = unAhoraStoreString
                                            
                                        
                                            unNuevoEstadoTraduccion = cEstadoTraduccionTraducida
                                            if unEstadoTraduccionScanned in [ cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva, ]:
                                                                        
                                                unNuevoEstadoTraduccion = unEstadoTraduccionScanned

                                                if unReviewDateScanned and unReviewerScanned:
                                                    unUsuarioRevisor     = unReviewerScanned
                                                    unaFechaRevision     = unReviewDateScanned
                                                    unUsuarioModificador = unReviewerScanned
                                                    unaFechaModificacion = unReviewDateScanned
                                                else:
                                                    unUsuarioRevisor     = theMemberId
                                                    unaFechaRevision     = unDateStoreString
                                                    unUsuarioModificador = theMemberId
                                                    unaFechaModificacion = unDateStoreString
                                                
                                    
                                                if unEstadoTraduccionScanned == cEstadoTraduccionDefinitiva:
                                                    if unDefinitiveDateScanned and unCoordinatorScanned:
                                                        unUsuarioCoordinador = unCoordinatorScanned
                                                        unaFechaDefinitivo   = unDefinitiveDateScanned
                                                        unUsuarioModificador = unCoordinatorScanned
                                                        unaFechaModificacion = unDefinitiveDateScanned
                                                    else:
                                                        unUsuarioCoordinador = theMemberId
                                                        unaFechaDefinitivo   = unDateStoreString
                                                        unUsuarioModificador = theMemberId
                                                        unaFechaModificacion = unDateStoreString
                                            
                                            
                                            unaTraduccionExistente.setEstadoTraduccion(           unNuevoEstadoTraduccion)    
                                            unaTraduccionExistente.setUsuarioModificador(         unUsuarioModificador)   
                                            unaTraduccionExistente.setFechaModificacionTextual(   unaFechaModificacion)                                                
                                            unaTraduccionExistente.setUsuarioTraductor(           unUsuarioTraductor)   
                                            unaTraduccionExistente.setFechaTraduccionTextual(     unaFechaTraduccion)    
                                            unaTraduccionExistente.setUsuarioRevisor(             unUsuarioRevisor)  
                                            unaTraduccionExistente.setFechaRevisionTextual(       unaFechaRevision)
                                            unaTraduccionExistente.setUsuarioCoordinador(         unUsuarioCoordinador)   
                                            unaTraduccionExistente.setFechaDefinitivoTextual(     unaFechaDefinitivo)
                                            
                                            unaTraduccionExistente.pRegistrarHistoria( 
                                                theAccion                   = cTranslationHistoryAction_Importar, 
                                                theFechaAccionTextual       = unaFechaModificacion, 
                                                theUsuarioActor             = unUsuarioModificador, 
                                                theEstadoTraduccion         = cEstadoTraduccionTraducida, 
                                                theFechaTraduccionTextual   = unaFechaTraduccion, 
                                                theUsuarioTraductor         = unUsuarioTraductor, 
                                                theCadenaTraducida          = unaTraduccionEncoded, 
                                                theFechaRevisionTextual     = unaFechaRevision, 
                                                theUsuarioRevisor           = unUsuarioRevisor, 
                                                theFechaDefinitivoTextual   = unaFechaDefinitivo, 
                                                theUsuarioCoordinador       = unUsuarioCoordinador,
                                                theComentario               = unComentarioTraduccionScanned or cMarcaDeComentarioSinCambios,                                            
                                            )
                                                                                

                                            unaTraduccionExistente.pAddToCatalogs( 
                                                unosCatalogsBusquedaTraduccionesPorIdioma[ unCodigoIdioma], 
                                                unosCatalogsFiltroTraduccionesPorIdioma[   unCodigoIdioma], 
                                                unosCatalogsTextoTraduccionesPorIdioma[    unCodigoIdioma],
                                            )
                
                                            theInformeImportarContenidos[ 'translation_changes'] += 1 
                                            theInformeImportarContenidos[ 'operations_done']   += 1
                                            
                                            theProcessControlManager.pProcessStep( unaTraduccionExistente, { unaTraduccionExistente.meta_type: 1,}, { unaTraduccionExistente.meta_type: 1,})
    
                        
                
                                        else:
                                            # ######################################################
                                            """Existing Translation is not pending: information to write depends on previous and new state.
                                            
                                            """
                                            
                                            unNuevoEstadoTraduccion = cEstadoTraduccionTraducida
                                            if unEstadoTraduccionScanned in [ cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva, ]:
                                                unNuevoEstadoTraduccion = unEstadoTraduccionScanned
                                                
                                            unIndexEstadoTraduccion        = cTodosEstados.index( unEstadoTraduccion)
                                            unIndexEstadoTraduccionScanned = cTodosEstados.index( unNuevoEstadoTraduccion)
                                            
                                            unUpdateCadenaTraducida = False
                                            unUpgradeToEstado       = None
                                            unTranslationIgnored    = False
                                            
                                            if unEstadoTraduccion == cEstadoTraduccionDefinitiva:
                                                unTranslationIgnored = True
                                            
                                            else:
                                                
                                                if unaTraduccionEncoded == unaCadenaTraducida:
                                                    """Translation is the same. Do not change translation. Just upgrade status if scanned status is higher.
                                                    
                                                    """
                                                    if not ( unNuevoEstadoTraduccion == unEstadoTraduccion):
                                                        
                                                        if ( unIndexEstadoTraduccionScanned > unIndexEstadoTraduccion):
                                                            unUpgradeToEstado = unNuevoEstadoTraduccion
                                                        else:
                                                            if ( unIndexEstadoTraduccionScanned < unIndexEstadoTraduccion):
                                                                unTranslationIgnored = True    
                                                                
                                                                
                                                else:
                                                    """Translation is not the same, but Ignore if current status higher than scanned status.
                                                    
                                                    """
                                                    if unIndexEstadoTraduccionScanned >= unIndexEstadoTraduccion:
                                                        unUpdateCadenaTraducida = True
                                                        
                                                        if unIndexEstadoTraduccionScanned > unIndexEstadoTraduccion:
                                                            unUpgradeToEstado = unNuevoEstadoTraduccion
                                                        
                                                    else:
                                                        unTranslationIgnored = True

                                                    
                                                    
                                            unaCadenaTraducidaACambiar = ''
                                            unEstadoTraduccionACambiar = ''
                                            
                                            unUsuarioModificadorACambiar=''
                                            unaFechaModificacionACambiar=''                                            
                                            unTraductorACambiar        = ''
                                            unaFechaTraduccionACambiar = ''
                                            unRevisorACambiar          = ''
                                            unaFechaRevisionACambiar   = ''
                                            unCoordinadorACambiar      = ''
                                            unaFechaDefinitivoACambiar = ''
                                            
                                                        
                                            if unUpdateCadenaTraducida:        
                                                
                                                unaTraduccionExistente.setCadenaTraducida(            unaTraduccionEncoded)
                                                unaCadenaTraducidaACambiar = unaTraduccionEncoded

                                                
                                            if unUpgradeToEstado:
                                                
                                                unaTraduccionExistente.setEstadoTraduccion(           unUpgradeToEstado) 
                                                unEstadoTraduccionACambiar = unUpgradeToEstado

                                                
                                                
                                                #if ( unUpgradeToEstado == cEstadoTraduccionTraducida)  and ( unEstadoTraduccion in [ cEstadoTraduccionTraducida,]):
                                            if ( ( unUpgradeToEstado in [ cEstadoTraduccionTraducida]) and ( unEstadoTraduccion in [ cEstadoTraduccionTraducida])) or \
                                               ( ( ( not unUpgradeToEstado) and unUpdateCadenaTraducida) and ( unEstadoTraduccion in [ cEstadoTraduccionTraducida]) ):
                                                
                                                if unTranslationDateScanned and unTranslatorScanned:
                                                    unTraductorACambiar          = unTranslatorScanned
                                                    unaFechaTraduccionACambiar   = unTranslationDateScanned
                                                    unUsuarioModificadorACambiar = unTranslatorScanned
                                                    unaFechaModificacionACambiar = unTranslationDateScanned
                                                else:
                                                    unTraductorACambiar          = theMemberId
                                                    unaFechaTraduccionACambiar   = unAhoraStoreString
                                                    unUsuarioModificadorACambiar = theMemberId
                                                    unaFechaModificacionACambiar = unAhoraStoreString
                                                
                                                unaTraduccionExistente.setUsuarioTraductor(         unTraductorACambiar)  
                                                unaTraduccionExistente.setFechaTraduccionTextual(   unaFechaTraduccionACambiar)
                                                                      
                                                
                                                    
                                                
                                                #if ( unUpgradeToEstado in [ cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva]) and ( unEstadoTraduccion in [ cEstadoTraduccionTraducida, cEstadoTraduccionRevisada]):
                                            if ( ( unUpgradeToEstado in [ cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva]) and ( unEstadoTraduccion in [ cEstadoTraduccionTraducida, cEstadoTraduccionRevisada])) or \
                                               ( ( ( not unUpgradeToEstado) and unUpdateCadenaTraducida) and ( unEstadoTraduccion in [ cEstadoTraduccionRevisada]) ):
                                                    
                                                if unReviewDateScanned and unReviewerScanned:
                                                    unRevisorACambiar            = unReviewerScanned
                                                    unaFechaRevisionACambiar     = unReviewDateScanned
                                                    unUsuarioModificadorACambiar = unReviewerScanned
                                                    unaFechaModificacionACambiar = unReviewDateScanned
                                                else:
                                                    unRevisorACambiar            = theMemberId
                                                    unaFechaRevisionACambiar     = unAhoraStoreString
                                                    unUsuarioModificadorACambiar = theMemberId
                                                    unaFechaModificacionACambiar = unAhoraStoreString

                                                unaTraduccionExistente.setUsuarioRevisor(         unRevisorACambiar)  
                                                unaTraduccionExistente.setFechaRevisionTextual(   unaFechaRevisionACambiar)

                                                
                                                    
                                                    
                                                #if ( unUpgradeToEstado == cEstadoTraduccionDefinitiva) and ( unEstadoTraduccion in [ cEstadoTraduccionTraducida, cEstadoTraduccionRevisada]):
                                            if ( ( unUpgradeToEstado in [ cEstadoTraduccionDefinitiva]) and ( unEstadoTraduccion in [ cEstadoTraduccionTraducida, cEstadoTraduccionRevisada])) or \
                                               ( ( ( not unUpgradeToEstado) and unUpdateCadenaTraducida) and ( unEstadoTraduccion in [ cEstadoTraduccionDefinitiva]) ):
                                                    
                                                if unDefinitiveDateScanned and unCoordinatorScanned:
                                                    unCoordinadorACambiar        = unCoordinatorScanned
                                                    unaFechaDefiniticoACambiar   = unDefinitiveDateScanned
                                                    unUsuarioModificadorACambiar = unCoordinatorScanned
                                                    unaFechaModificacionACambiar = unDefinitiveDateScanned
                                                else:
                                                    unCoordinadorACambiar        = theMemberId
                                                    unaFechaDefiniticoACambiar   = unAhoraStoreString
                                                    unUsuarioModificadorACambiar = theMemberId
                                                    unaFechaModificacionACambiar = unAhoraStoreString
                                                                                                    
                                                unaTraduccionExistente.setUsuarioCoordinador(     unCoordinadorACambiar)  
                                                unaTraduccionExistente.setFechaDefinitivoTextual( unaFechaDefiniticoACambiar)
                                                    
                                                    
                                                    
                                                    
                                            if unUpdateCadenaTraducida or unUpgradeToEstado:
                                                
                                                unaTraduccionExistente.setUsuarioModificador(         unUsuarioModificadorACambiar)   
                                                unaTraduccionExistente.setFechaModificacionTextual(   unaFechaModificacionACambiar)    
                                                
                                                
                                                unaTraduccionExistente.pRegistrarHistoria( 
                                                    theAccion                   = cTranslationHistoryAction_Importar, 
                                                    theFechaAccionTextual       = unaFechaModificacionACambiar, 
                                                    theUsuarioActor             = unUsuarioModificadorACambiar, 
                                                    theEstadoTraduccion         = unEstadoTraduccionACambiar, 
                                                    theFechaTraduccionTextual   = unaFechaTraduccionACambiar, 
                                                    theUsuarioTraductor         = unTraductorACambiar, 
                                                    theCadenaTraducida          = unaCadenaTraducidaACambiar, 
                                                    theFechaRevisionTextual     = unaFechaRevisionACambiar, 
                                                    theUsuarioRevisor           = unRevisorACambiar, 
                                                    theFechaDefinitivoTextual   = unaFechaDefinitivoACambiar, 
                                                    theUsuarioCoordinador       = unCoordinadorACambiar,
                                                    theComentario               = unComentarioTraduccionScanned or cMarcaDeComentarioSinCambios, 
                                                )                                                    
                                                

                                                                                       
                                                unaTraduccionExistente.pAddToCatalogs( 
                                                    unosCatalogsBusquedaTraduccionesPorIdioma[ unCodigoIdioma], 
                                                    unosCatalogsFiltroTraduccionesPorIdioma[   unCodigoIdioma], 
                                                    unosCatalogsTextoTraduccionesPorIdioma[    unCodigoIdioma],
                                                )
                    
                                                
                                                
                                                if unUpdateCadenaTraducida:
                                                    
                                                    theInformeImportarContenidos[ 'translation_changes'] += 1 
                                                    
                                                else:
                                                    
                                                    theInformeImportarContenidos[ 'translation_status_changes'] += 1 

                                                
                                                    
                                                theProcessControlManager.pProcessStep( unaTraduccionExistente, { unaTraduccionExistente.meta_type: 1,}, { unaTraduccionExistente.meta_type: 1,})
                                                 
                                                
                                                
                                            else:
                                                
                                                if unTranslationIgnored:
                                                    theInformeImportarContenidos[ 'translations_ignored'] += 1 
                                                    
                                                else:
                                                    theInformeImportarContenidos[ 'translations_unchanged'] += 1 
                                                    
                                                
                                                theProcessControlManager.pProcessStep( unaTraduccionExistente, { unaTraduccionExistente.meta_type: 1,}, { })

                                                
                                                
                                            theInformeImportarContenidos[ 'operations_done']   += 1
                                                    
                                                

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

                        
                        
                        
                    for unCodigoIdiomaQueFalta in  unosCodigosIdiomasTraduccionesQueFaltan:
                        unaNuevaTraduccion = self.fCrearTraduccionPendiente( 
                            theCodigoIdioma                     =unCodigoIdiomaQueFalta, 
                            theCadena                           =unaCadena, 
                            theSimboloCadena                    =unSimboloCadena,  
                            theIdCadena                         =unaIdCadena, 
                            theNombresModulos                   =unosNombresModulosCadena, 
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
                        if not ( unaNuevaTraduccion == None):
                            theInformeImportarContenidos[ 'translation_creations_as_pending'] += 1 
                            theInformeImportarContenidos[ 'operations_done']   += 1

                            theProcessControlManager.pProcessStep( unaNuevaTraduccion, { }, { unaNuevaTraduccion.meta_type: 1})                        
                           
                        else:
                            # ######################################################
                            """Exit with error condition.
                            
                            """
                            theInformeImportarContenidos[ 'fecha_informe'] =self.fDateTimeNowTextual()
                            theInformeImportarContenidos[ 'error'] = "gvSIGi18n_TRACadena_failedTranslationCreation_error_msgid"
                            theInformeImportarContenidos[ 'error_detail'] = '%s %s' % ( unCodigoIdiomaQueFalta, unSimboloCadena , )
                            raise TRAProcessErrorException( theInformeImportarContenidos[ 'error'], theInformeImportarContenidos[ 'error_detail'],)
                            
                     
                    theInformeImportarContenidos[ 'processed_strings'] += 1
                        
                    
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
                            raise TRAProcessErrorException( theInformeImportarContenidos[ 'error'], theInformeImportarContenidos[ 'error_detail'],)
                                        
                        unaIdCadena = unaCadena.getId()
                        unosNombresModulosCadena = unaCadena.getNombresModulos()
                        for unCodigoIdioma in unosCodigosIdiomasACrear:
                            
                            unaTraduccionEncontrada = unaCadena.fObtenerTraduccionPorCodigoIdioma( unCodigoIdioma,thePloneUtilsTool=thePloneUtilsTool)
                            if not( unaTraduccionEncontrada == None):
                                
                                theInformeImportarContenidos[ 'translations_unchanged'] += 1 
                                theInformeImportarContenidos[ 'operations_done']   += 1
                                
                                theInformeImportarContenidos[ 'translations_to_create_in_new_languages_for_preexisting_strings']   -= 1
                                
                                theProcessControlManager.pProcessStep( unaTraduccionEncontrada, { unaTraduccionEncontrada.meta_type: 1}, {})                        
                                
                             
                            else:
                                unaNuevaTraduccion = self.fCrearTraduccionPendiente( 
                                    theCodigoIdioma                     =unCodigoIdioma, 
                                    theCadena                           =unaCadena, 
                                    theSimboloCadena                    =unSimboloCadena,  
                                    theIdCadena                         =unaIdCadena, 
                                    theNombresModulos                   =unosNombresModulosCadena, 
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
                                if not ( unaNuevaTraduccion == None):
                                    theInformeImportarContenidos[ 'translation_creations_as_pending'] += 1 
                                    
                                    theInformeImportarContenidos[ 'translations_created_in_new_languages_for_preexisting_strings'] += 1
                                    theInformeImportarContenidos[ 'operations_done']   += 1
                                
                                    theProcessControlManager.pProcessStep( unaNuevaTraduccion, { }, { unaNuevaTraduccion.meta_type: 1})                        

                                    
                                else:
                                    # ######################################################
                                    """Exit with error condition.
                                    
                                    """
                                    theInformeImportarContenidos[ 'fecha_informe'] =self.fDateTimeNowTextual()
                                    theInformeImportarContenidos[ 'error'] = "gvSIGi18n_TRACadena_failedTranslationCreation_error_msgid"
                                    theInformeImportarContenidos[ 'error_detail'] = '%s %s' % ( unCodigoIdioma, unSimboloCadena , )
                                    raise TRAProcessErrorException( theInformeImportarContenidos[ 'error'], theInformeImportarContenidos[ 'error_detail'],)

                                
                                
                                
                        
                        
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
                            raise TRAProcessErrorException( theInformeImportarContenidos[ 'error'], theInformeImportarContenidos[ 'error_detail'],)
                                       
                        unasTraduccionesExistentes      = unaCadena.fTraduccionesPorIdiomas( unosCodigosIdiomasExistentes, thePloneUtilsTool) 

                        unaIdCadena = unaCadena.getId()                        
                        unosNombresModulosCadena = unaCadena.getNombresModulos()
                        
                        for unCodigoIdioma in unosCodigosIdiomasExistentes:
                            unaTraduccionExistente = unasTraduccionesExistentes.get( unCodigoIdioma, None)
                            
                            if unaTraduccionExistente:
                                unInformeCrearTraduccionesQueFaltan[ 'operations_done']   += 1
                                theInformeImportarContenidos[ 'operations_done']   += 1
                                
                                theProcessControlManager.pProcessStep( unaTraduccionExistente, { unaTraduccionExistente.meta_type: 1}, {})                        
                                
                              
                                
                            else:
                            
                                unaNuevaTraduccion = self.fCrearTraduccionPendiente( 
                                    theCodigoIdioma                     =unCodigoIdioma, 
                                    theCadena                           =unaCadena, 
                                    theSimboloCadena                    =unSimboloCadena,  
                                    theIdCadena                         =unaIdCadena, 
                                    theNombresModulos                   =unosNombresModulosCadena, 
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
                                if not( unaNuevaTraduccion == None):
                                    unInformeCrearTraduccionesQueFaltan[ 'translations_created'] += 1 
                                    unInformeCrearTraduccionesQueFaltan[ 'operations_done'] += 1 
                                    
                                    theInformeImportarContenidos[ 'operations_done']   += 1
                                    
                                    theProcessControlManager.pProcessStep( unaNuevaTraduccion, { }, { unaNuevaTraduccion.meta_type: 1})                        
                                                                    
                                    
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
                                    raise TRAProcessErrorException( theInformeImportarContenidos[ 'error'], theInformeImportarContenidos[ 'error_detail'],)
                                
                        unInformeCrearTraduccionesQueFaltan[ 'strings_completed'] += 1
                        
                    unInformeCrearTraduccionesQueFaltan[ 'fecha_informe'] =self.fDateTimeNowTextual()
                    
                finally:
                    unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                    unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
            
                    
     
            return self
    
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
 

              

    
    
    
    
    
    



    
    security.declarePrivate( 'pImportarContenidoXML')    
    def pImportarContenidoXML( self,
        theProcessControlManager       =None,
        theJustEstimateCost            =None,
        theCatalogo                    =None, 
        theUseCaseQueryResult          =None, 
        theMemberId                    =None, 
        theInformeImportarContenidoXML =None, 
        theModelDDvlPlone_tool         =None,
        theModelDDvlPloneTool_Import   =None,
        theContenidoXML                =None,
        thePermissionsCache            =None, 
        theRolesCache                  =None, 
        theParentExecutionRecord       =None):
        """Import XML from translations catalog backup.
               
        """
        unExecutionRecord = self.fStartExecution( 'method',  'pImportarContenidoXML', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }) 


        
        try:
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
                       
            
            if not theInformeImportarContenidoXML:
                if theProcessControlManager:
                    raise TRAProcessErrorException( "gvSIGi18n_MissingParameters_internal_error_msgid", 'theInformeImportarContenidoXML',)
                return self
            
            
            if theCatalogo == None:
                unAhora =self.fDateTimeNow()
                theInformeImportarContenidoXML[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                theInformeImportarContenidoXML[ 'error'] = "gvSIGi18n_MissingParameters_internal_error_msgid"
                theInformeImportarContenidoXML[ 'error_detail'] = 'theCatalogo'
                if theProcessControlManager:
                    raise TRAProcessErrorException( theInformeImportarContenidoXML[ 'error'], theInformeImportarContenidoXML[ 'error_detail'],)
                return self
            
            
            if theModelDDvlPlone_tool == None:
                unAhora =self.fDateTimeNow()
                theInformeImportarContenidoXML[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                theInformeImportarContenidoXML[ 'error'] = "gvSIGi18n_MissingParameters_internal_error_msgid"
                theInformeImportarContenidoXML[ 'error_detail'] = 'theModelDDvlPlone_tool'
                if theProcessControlManager:
                    raise TRAProcessErrorException( theInformeImportarContenidoXML[ 'error'], theInformeImportarContenidoXML[ 'error_detail'],)
                return self       
            
            
            if theModelDDvlPloneTool_Import == None:
                unAhora =self.fDateTimeNow()
                theInformeImportarContenidoXML[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                theInformeImportarContenidoXML[ 'error'] = "gvSIGi18n_MissingParameters_internal_error_msgid"
                theInformeImportarContenidoXML[ 'error_detail'] = 'theModelDDvlPloneTool_Import'
                if theProcessControlManager:
                    raise TRAProcessErrorException( theInformeImportarContenidoXML[ 'error'], theInformeImportarContenidoXML[ 'error_detail'],)
                return self       
            
            
            if not theUseCaseQueryResult or not theUseCaseQueryResult.get( 'success', False):
                unAhora =self.fDateTimeNow()
                theInformeImportarContenidoXML[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                theInformeImportarContenidoXML[ 'error'] = "gvSIGi18n_UseCaseNotPermitted_error_msgid"
                if theUseCaseQueryResult:
                    theInformeImportarContenidoXML[ 'error_detail'] = theUseCaseQueryResult.get( 'use_case_name', '')       
                else:
                    theInformeImportarContenidoXML[ 'error_detail'] = ''
                    
                if theProcessControlManager:
                    raise TRAProcessErrorException( theInformeImportarContenidoXML[ 'error'], theInformeImportarContenidoXML[ 'error_detail'],)
                return self
    
            
            
            if theContenidoXML == None:
                unAhora =self.fDateTimeNow()
                theInformeImportarContenidoXML[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                theInformeImportarContenidoXML[ 'error'] = "gvSIGi18n_MissingParameters_internal_error_msgid"
                theInformeImportarContenidoXML[ 'error_detail'] = 'theContenidoXML'
                if theProcessControlManager:
                    raise TRAProcessErrorException( theInformeImportarContenidoXML[ 'error'], theInformeImportarContenidoXML[ 'error_detail'],)
                return self

            
           
            aXMLSource = theContenidoXML.fContenidoXML()
            
            if not aXMLSource:
                unAhoraString =self.fDateTimeNowTextual()
                theInformeImportarContenidoXML.update( {
                    'valid':         True,
                    'end_date':      unAhoraString,
                    'fecha_Informe': unAhoraString,
                })
                return self
            
            
            
            

            someBinaryFileNames = theInformeImportarContenidoXML.get( 'binary_file_names', None)
            if someBinaryFileNames == None:
                someBinaryFileNames = [ ]
                theInformeImportarContenidoXML[ 'binary_file_names'] = someBinaryFileNames
                
                
            
                
            someContenidosBinarios = theContenidoXML.fContenidoBinario()
            
            someFilesAndData = {}
            for aContenidoBinario in someContenidosBinarios:
                if aContenidoBinario:
                    
                    aFileFullName  = aContenidoBinario.get( 'file_full_name',  '')
                    if aFileFullName:
                        
                        someBinaryFileNames.append( aFileFullName)
                        aWholeData = aContenidoBinario.get( 'file_whole_data', '')
                        someFilesAndData[ aFileFullName] = aWholeData
                        
                        
                        
                       
            
            # ############################################
            """Determine XML node names to count and import.
            
            """
            
            aModelDDvlPloneTool_Retrieval = theModelDDvlPlone_tool.fModelDDvlPloneTool_Retrieval( theCatalogo)
            if aModelDDvlPloneTool_Retrieval == None:
                unEstimarCosteImportacionResult.update( {
                    'success':   False,
                    'status':    'gvSIGi18n_Missing_ModelDDvlPloneTool_Retrieval_internal_error_msgid',
                })
                return unEstimarCosteImportacionResult
                            


            someAllExportTypeConfigs =  aModelDDvlPloneTool_Retrieval.getAllTypeExportConfigs( theCatalogo)        
            if not someAllExportTypeConfigs:
                theProcessControlManager.vResult[ 'success']   = False
                theProcessControlManager.vResult[ 'condition'] = cExportStatus_NoExportTypeConfigsForObject
                unEstimarCosteImportacionResult.update( {
                    'success':              False,
                    'status':               'gvSIGi18n_NoExportTypeConfigsForObject',
                })
                return unEstimarCosteImportacionResult
             
          
            someExportTypeConfigsChosen = self.fImportTypeConfigsChosen( 
                theCatalogo                             =theCatalogo,
                theAllExportTypeConfigs                 =someAllExportTypeConfigs,
                theImportarTRACatalogo                  =self.getImportarXMLTRACatalogo(),
                theImportarTRAConfiguraciones           =self.getImportarXMLTRAConfiguraciones(),           
                theImportarTRAParametrosControlProgreso =self.getImportarXMLTRAParametrosControlProgreso(),
                theImportarTRAIdiomas                   =self.getImportarXMLTRAIdiomas(),                
                theImportarTRASolicitudesCadenas        =self.getImportarXMLTRASolicitudesCadenas(),
                theImportarTRAModulos                   =self.getImportarXMLTRAModulos(),                  
                theImportarTRAInformes                  =self.getImportarXMLTRAInformes(),                  
            )
            if not someExportTypeConfigsChosen:
                unEstimarCosteImportacionResult.update( {
                    'success':              False,
                    'status':               'gvSIGi18n_NoExportTypeConfigsChosenForObject',
                })
                return unEstimarCosteImportacionResult                
                                
                                        
            someNombresTiposToCount = someExportTypeConfigsChosen.keys()[:]
            
            
                
            # ############################################
            """Delegate on tool to parse and scan XML contents.
            
            """
            aXMLContentsSummary = theModelDDvlPloneTool_Import.fXMLContentSummary(
                theTimeProfilingResults        =None,
                theContextualElement           =theCatalogo, 
                theXMLSource                   =aXMLSource,
                theAcceptedXMLRootNodeName     =cNombreTipoTRACatalogo,
                theXMLNodeNamesToCount         =someNombresTiposToCount,
                theAdditionalParams            =None,
            )           
            if not ( aXMLContentsSummary and aXMLContentsSummary.get( 'success', False)):
                theInformeImportarContenidoXML[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                theInformeImportarContenidoXML[ 'error']         = "gvSIGi18n_ParseXML_error_msgid"
                theInformeImportarContenidoXML[ 'error_detail']  = 'status: %s\ncondition: %s\nexception: %s' % ( aXMLContentsSummary.get( 'status', ''), aXMLContentsSummary.get( 'condition', ''), aXMLContentsSummary.get( 'exception', ''),)
                if theProcessControlManager:
                    raise TRAProcessErrorException( theInformeImportarContenidoXML[ 'error'], theInformeImportarContenidoXML[ 'error_detail'],)
                return self
            
            
            anXMLDocument = aXMLContentsSummary.get( 'xml_document', [])
            someXMLRoots  = aXMLContentsSummary.get( 'xml_roots', [])

             

            
            theInformeImportarContenidoXML.update( {
                'expected_num_nodes':         aXMLContentsSummary.get( 'num_nodes',         0),
                'expected_num_nodes_by_type': aXMLContentsSummary.get( 'num_nodes_by_type', {}).copy(),
            })
            
            
            if theJustEstimateCost:
                return self
            
        
            
            
            
            unSubExecutionRecord = self.fStartExecution( 'block',  'pImportarContenidoXML-SubExecution to import xml contents, creating or overwritting elements.', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
            try:
            
                # ################################################33
                """Retrieve process control parameters to yield processor."
                
                """    
                aMinimumTimeSlice   = None
                aYieldTimePercent   = None
                
                if theProcessControlManager:
                    
                    aYieldProcessor_Parms  = theProcessControlManager.vProgressControlParameters.get( cTRAProgress_SupportKind_YieldProcessor, {})
                    
                    if aYieldProcessor_Parms:
                        
                        aYieldProcessor_Enabled  = cTRAYieldProcessorEnabled and aYieldProcessor_Parms.get( 'enabled', False)
                        if aYieldProcessor_Enabled:
                           
                            aMinimumTimeSlice  = aYieldProcessor_Parms.get( 'max_milliseconds', None)
                            if not aMinimumTimeSlice:
                                aMinimumTimeSlice = None
                            else:
                                aMinimumTimeSlice  = min( aMinimumTimeSlice, cTRAProgress_MaxMillisecondsToYield)
                                
                            aPercentActiveTime  = aYieldProcessor_Parms.get( 'percent_active_time', None)
                            if not aPercentActiveTime:
                                aYieldTimePercent = None
                            else:
                                if aPercentActiveTime < 0:
                                    aPercentActiveTime = 0 - aPercentActiveTime
                                aYieldTimePercent = 100 - min( aPercentActiveTime, 100)
                                aYieldTimePercent = min( aYieldTimePercent, cTRAProgress_MaxTimePercentageToYield)
                    
                    
                                
                # ############################################
                """Retrieve translations catalog attributes to be restored after the import in case they are overwritten by the import process.
                
                """
                
                aOriginalMustRegatalog = theCatalogo.getDebeRecatalogar()
                                

                
                
                # ############################################
                """Retrieve existing progress elements in the translations catalog such that any imported progress element that is imported with the active attribute set to true (i.e., the one corresponding to the export process that created the restored backup file), can be set as non active after the import.
                
                """
                someOriginalProgressElements = theCatalogo.fObtenerTodosProgresos()
                
                
                
                
                                
                # ################################################33
                """Import into the translations catalog the XML contents, and any associated binary content."
                
                """    
                someAdditionalParams = {
                    'ignore_allow_write': True,
                }
                unImportReport = theModelDDvlPloneTool_Import.fImport_XMLDocumentAndBinaries( 
                    theTimeProfilingResults        =None,
                    theModelDDvlPloneTool          =theModelDDvlPlone_tool, 
                    theContainerObject             =theCatalogo, 
                    theXMLDocument                 =anXMLDocument,
                    theXMLRootElements             =someXMLRoots,
                    theFilesAndData                =someFilesAndData,
                    theMDDImportTypeConfigs        =someExportTypeConfigsChosen, 
                    thePloneImportTypeConfigs      =None, 
                    theMappingConfigs              =None, 
                    theMinimumTimeSlice            =aMinimumTimeSlice,
                    theYieldTimePercent            =aYieldTimePercent,        
                    theReuseIdsForTypes            =cTRATypesToReuseIdsOnRestoreBackup,
                    theAdditionalParams            =someAdditionalParams,
                )
                if not unImportReport:
                    theInformeImportarContenidoXML[ 'valid'] = False
                    theInformeImportarContenidoXML[ 'error'] = 'NoImportReport_fImport_XMLDocumentAndBinaries'
                
                else:
                    
                    if not unImportReport.get( 'success', False):
                        theInformeImportarContenidoXML[ 'valid'] = False
                        theInformeImportarContenidoXML[ 'error'] = unImportReport.get( 'status', '') or ''
                        theInformeImportarContenidoXML[ 'error_detail'] = '%s\n%s' % ( unImportReport.get( 'condition', '') or '', unImportReport.get( 'exception', '') or '',)
                                  
                    else:                        
                        theInformeImportarContenidoXML.update( {
                            'valid':                      True,
                            'imported_num_nodes':         unImportReport.get( 'num_elements_pasted', 0),
                            'imported_num_nodes_by_type': unImportReport.get( 'num_elements_imported_by_type', 0),
                        })
                        
                        
                        
                        
                            
                        
                        
                # #########################################################
                """Verify or initialize catalogs and indexes, owned by the TRACatalog, to index instances of TRACadena (string to be translated).
                
                """
                unInformeCatalogosCadenas = self.fVerifyOrInitializeCatalogsEIndicesEnCatalogo(
                    theEspecificacionesCatalogs    =cTRACatalogsDetailsParaCadenas, 
                    theAllowInitialization         =True, 
                    theCheckPermissions            =False, 
                    thePermissionsCache            =unPermissionsCache, 
                    theRolesCache                  =unRolesCache, 
                    theParentExecutionRecord       =unExecutionRecord,
                )
                if unInformeCatalogosCadenas:
                    theInformeImportarContenidoXML[ 'catalogs_cadenas'] = unInformeCatalogosCadenas
                    
                    if unInformeCatalogosCadenas.get( 'must_run_recatalog_elements', False):
                        theInformeImportarContenidoXML[ 'must_run_recatalog_elements'] = True
                
                    
                    
                    
                # #########################################################
                """Verify or initialize catalogs and indexes, owned by each of the languages the TRACatalog, to index instances of TRATraduccion (translation).
                
                """
                unosInformeCatalogosIdiomas  = theCatalogo.fVerifyOrInitializeCatalogsEIndicesTodosIdiomas( 
                    theEspecificacionesCatalogs    =cTRACatalogsDetailsParaIdioma, 
                    theAllowInitialization         =True, 
                    theCheckPermissions            =False, 
                    thePermissionsCache            =unPermissionsCache, 
                    theRolesCache                  =unRolesCache, 
                    theParentExecutionRecord       =unExecutionRecord,
                ) 
                if unosInformeCatalogosIdiomas:
                    theInformeImportarContenidoXML[ 'catalogs_idiomas'] = unosInformeCatalogosIdiomas
                    for unInformeCatalogosIdioma in unosInformeCatalogosIdiomas:
                        if unInformeCatalogosIdioma:
                            if unInformeCatalogosIdioma.get( 'must_run_recatalog_elements', False):
                                theInformeImportarContenidoXML[ 'must_run_recatalog_elements'] = True
                                                
                        
                                
                                

                    
                # #########################################################
                """Verify or initialize user groups, and their permissions on the languages and modules, because some languages and modules may have been created during the import.
                
                """
                unInformeUserGroupsCatalogo  = theCatalogo.fVerifyOrInitializeUserGroupsCatalogo(   
                    theAllowInitialization         =True, 
                    theCheckPermissions            =False, 
                    thePermissionsCache            =unPermissionsCache, 
                    theRolesCache                  =unRolesCache, 
                    theParentExecutionRecord       =unExecutionRecord,
                )                
                if unInformeUserGroupsCatalogo:
                    theInformeImportarContenidoXML[ 'user_groups'] = unInformeUserGroupsCatalogo
                                                
                        
                            
                    
                                
                # ############################################
                """Restore translations catalog attributes in case they have been overwritten by the import process.
                
                """
                
                aNewMustRegatalog = theCatalogo.getDebeRecatalogar()
                if not ( (( aNewMustRegatalog and True) or False) == (( aOriginalMustRegatalog and True) or False)):
                    theCatalogo.setDebeRecatalogar( aOriginalMustRegatalog)
                                
                    
                    
                    
                # ############################################
                """Set to False the active attribute of any progress elements just imported into the translations catalog that have been imported with their state attribute set to True (i.e., the one corresponding to the export process that created the restored backup file).
                
                """
                someNewProgressElements = theCatalogo.fObtenerTodosProgresos()
                for aProgressElement in someNewProgressElements:
                    if not ( aProgressElement in someOriginalProgressElements):
                        if aProgressElement.getEstadoProceso() == cTRAProgreso_EstadoProceso_Activo:
                            aProgressElement.setEstadoProceso( cTRAProgreso_EstadoProceso_Inactivo)
                
                
                    
               
            finally:
                unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
      
            return self
    
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
 

              

    
    
            
            

    security.declarePrivate( 'fImportTypeConfigsChosen')
    def fImportTypeConfigsChosen( self,
        theCatalogo                             =None,
        theAllExportTypeConfigs                 =None,
        theImportarTRACatalogo                  =None,
        theImportarTRAConfiguraciones           =None,           
        theImportarTRAParametrosControlProgreso =None,
        theImportarTRAIdiomas                   =None,                
        theImportarTRAModulos                   =None,                  
        theImportarTRAInformes                  =None,                  
        theImportarTRASolicitudesCadenas        =None,):
        
        if theCatalogo == None:
            return { }
        
        if not theAllExportTypeConfigs:
            return {}
                    
        someTypeConfigsChosen = theCatalogo.fExportTypeConfigsChosen( 
            theAllExportTypeConfigs                 =theAllExportTypeConfigs,
            theExportarTRACatalogo                  =theImportarTRACatalogo,
            theExportarTRAConfiguraciones           =theImportarTRAConfiguraciones,           
            theExportarTRAParametrosControlProgreso =theImportarTRAParametrosControlProgreso,
            theExportarTRAIdiomas                   =theImportarTRAIdiomas,                
            theExportarTRAModulos                   =theImportarTRAModulos,                  
            theExportarTRAInformes                  =theImportarTRAInformes,                  
            theExportarTRASolicitudesCadenas        =theImportarTRASolicitudesCadenas,)
        
        if not someTypeConfigsChosen:
            return {}
                            
        
        someImportTypeConfigsChosen = { }
        
        for aTypeName in someTypeConfigsChosen.keys():
            someImportTypeConfigsChosen[ aTypeName] = { 'Default': someTypeConfigsChosen[ aTypeName],}
            
        return someImportTypeConfigsChosen
    
                
            
            
            
            
            
            
            
            
            
            
            
            
            

    

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
            'title':                    theSimboloCadena,
            'description':              '',
            'simbolo':                  theSimboloCadena,
            'estadoCadena':             cEstadoCadenaActiva,  
            'fechaCreacionTextual':     self.fDateTimeNowTextual(),
            'usuarioCreador':           theMemberId,
            'fechaCancelacion':         None,
            'nombresModulos':           cTRAModuleNameSeparator.join( theNombresModulos),
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
        theEstadoTraduccion,
        theComment,
        theCreationDate,    
        theCreator,         
        theTranslationDate, 
        theTranslator,      
        theReviewDate,      
        theReviewer,        
        theDefinitiveDate,  
        theCoordinator,             
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
        
        if theEstadoTraduccion in cTodosEstados:
            unEstadoTraduccion = theEstadoTraduccion
        else:
            if theTraduccionEncoded:
                unEstadoTraduccion = cEstadoTraduccionTraducida
            else:
                unEstadoTraduccion = cEstadoTraduccionPendiente
  
                
        unUsuarioCreador     = ''
        unaFechaCreacion     = ''
            
        unUsuarioTraductor   = ''
        unaFechaTraduccion   = ''
            
        unUsuarioRevisor     = ''
        unaFechaRevision     = ''
            
        unUsuarioCoordinador = ''
        unaFechaDefinitivo   = ''
            
            
        if theCreationDate and theCreator:
            unUsuarioCreador = theCreator
            unaFechaCreacion = theCreationDate
        else:
            unUsuarioCreador = theMemberId
            unaFechaCreacion = unDateStoreString
            
                
        if unEstadoTraduccion in [ cEstadoTraduccionTraducida, cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva, ]:

            if theTranslationDate and theTranslator:
                unUsuarioTraductor   = theTranslator
                unaFechaTraduccion   = theTranslationDate
                unUsuarioModificador = theTranslator
                unaFechaModificacion = theTranslationDate
            else:
                unUsuarioTraductor   = theMemberId
                unaFechaTraduccion   = unDateStoreString
                unUsuarioModificador = theMemberId
                unaFechaModificacion = unDateStoreString

            if unEstadoTraduccion in [ cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva, ]:
                if theReviewDate and theReviewer:
                    unUsuarioRevisor     = theReviewer
                    unaFechaRevision     = theReviewDate
                    unUsuarioModificador = theReviewer
                    unaFechaModificacion = theReviewDate
                else:
                    unUsuarioRevisor     = theMemberId
                    unaFechaRevision     = unDateStoreString
                    unUsuarioModificador = theMemberId
                    unaFechaModificacion = unDateStoreString

            if unEstadoTraduccion == cEstadoTraduccionDefinitiva:
                if theDefinitiveDate and theCoordinator:
                    unUsuarioCoordinador = theCoordinator
                    unaFechaDefinitivo   = theDefinitiveDate
                    unUsuarioModificador = theCoordinator
                    unaFechaModificacion = theDefinitiveDate
                else:
                    unUsuarioCoordinador = theMemberId
                    unaFechaDefinitivo   = unDateStoreString
                    unUsuarioModificador = theMemberId
                    unaFechaModificacion = unDateStoreString
                

        anAttrsDict = { 
            'title':                unTitulo,
            'description':          '',
            'simbolo':              theSimboloCadena,
            'codigoIdiomaEnGvSIG':  theCodigoIdioma, 
            'estadoCadena':         cEstadoCadenaActiva,
            'idCadena':             theIdCadena,
            'nombresModulos':       theNombresModulos,
            'estadoTraduccion'   :  unEstadoTraduccion,
            'cadenaTraducida'    :  theTraduccionEncoded,
            'usuarioCreador':       unUsuarioCreador, 
            'fechaCreacionTextual': unaFechaCreacion,  
            'usuarioTraductor':     unUsuarioTraductor, 
            'fechaTraduccionTextual': unaFechaTraduccion,  
            'usuarioRevisor':       unUsuarioRevisor, 
            'fechaRevisionTextual': unaFechaRevision,  
            'usuarioCoordinador':   unUsuarioCoordinador, 
            'fechaDefinitivoTextual': unaFechaDefinitivo,  
            'fechaModificacionTextual': unaFechaModificacion,  
            'usuarioModificador':   unUsuarioModificador, 
            'comentario':           theComment,   
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
            'fechaModificacionTextual': unDateStoreString,  
            'usuarioModificador':     theMemberId, 
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
    
    
    
   
    
    
    
    


    
    
    


    
    

    
    