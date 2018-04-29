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

from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_ImportTRAImportacion, cUseCase_CreateMissingTRATraduccion, cUseCase_ImportTRAImportacion_ToCreateCadenas, cUseCase_EstimateTRAImportacion

from TRAElemento_Permission_Definitions import cBoundObject, cPermissionsToDenyEverywhereToEverybody


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
        """Estimate the number of operations of various kinds that would be performed during the execution of an import process in the TRAImportacion contents.
        
        """
  
        unExecutionRecord = self.fStartExecution( 'method',  'fEstimarCosteImportacion', theParentExecutionRecord, False) 

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators  import cModificationKind_CreateSubElement, cModificationKind_Create, cModificationKind_ChangeValues
        from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fDateTimeNow
        
        try:

            unSubExecutionRecord = self.fStartExecution( 'block',  'fEstimarCosteImportacion-SubExecution to retrieve TRACatalog and accessible languages and modules', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
            
            
                
            unInformeImportarContenidos = self.fNewVoidInformeImportarContenidos()
            
            unInformeImportarContenidos[ 'start_date'] =self.fDateTimeNowTextual()
            
            unCatalogo = self.getCatalogo()
            if unCatalogo == None:
                unInformeImportarContenidos[ 'end_date'] =self.fDateTimeNowTextual()
                return unInformeImportarContenidos
            
            
           
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
                    if not unUseCaseQueryResult_CrearTraduccionesQueFaltan or not unUseCaseQueryResult_CrearTraduccionesQueFaltan.get( 'success', False):
                        unInformeImportarContenidos[ 'error'] = "gvSIGi18n_NoPermissionToCreateMissingTranslations_error_msgid"
                        unInformeImportarContenidos[ 'end_date'] =self.fDateTimeNowTextual()
                        return unInformeImportarContenidos
                    
                    
            finally:
                unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
                

                 
            unSubExecutionRecord = self.fStartExecution( 'block',  'fEstimarCosteImportacion-SubExecution to retrieve translations interchange contents', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
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
                
          
            unSubExecutionRecord = self.fStartExecution( 'block',  'fEstimarCosteImportacion-SubExecution to create status report before import and to set the first import progress report.', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
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

                    
            finally:
                unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
                
            unaExceptionInfo = None
            try:
                try:
                    self.pImportarContenidosIntercambio( 
                        theProcessControlManager    =None,
                        theJustEstimateCost         =True,
                        theCatalogo                 =unCatalogo, 
                        theUseCaseQueryResult       =unUseCaseQueryResult, 
                        theUseCaseQueryResult_CrearTraduccionesQueFaltan=unUseCaseQueryResult_CrearTraduccionesQueFaltan,
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
                    
                    unInformeExcepcion = 'Exception during Estimate Import Cost operation\n' 
                    unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                    try:
                        unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                    except:
                        None
                    unInformeExcepcion += unaExceptionFormattedTraceback   
                    
                    unaFechaString =self.fDateTimeNowTextual()
                    unInformeImportarContenidos[ 'fecha_informe'] = unaFechaString
                    unInformeImportarContenidos[ 'end_date']      = unaFechaString
                    unInformeImportarContenidos[ 'valid'] = False
                    unInformeImportarContenidos[ 'error'] = 'exception'
                    unInformeImportarContenidos[ 'error_detail'] = unInformeExcepcion

                    unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
                    
                    logging.getLogger( 'gvSIGi18n').info("EXCEPTION: exception details follow:\n%s\n" % unInformeExcepcion) 
                            
                    return unInformeImportarContenidos
                            
                
                
            finally:
                
                unSubExecutionRecord = self.fStartExecution( 'block',  'fEstimarCosteImportacion-SubExecution to create status report after import and to clear the import progress report.', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
                try:
                    unAhora = fDateTimeNow()
                    
                    unInformeImportarContenidos[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                    unInformeImportarContenidos[ 'end_date']      = self.fDateToStoreString( unAhora)
                    
       
        
                    unInformeImportarContenidos[ 'end_date'] =self.fDateTimeNowTextual()
                    
                    return unInformeImportarContenidos
                
                finally:
                    unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                    unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
                        
 
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
     
    
                
                            
     
    
    
    
    
    security.declareProtected( permissions.AddPortalContent, 'fImportarContenidosIntercambio')    
    def fImportarContenidosIntercambio( self, 
        theProcessControlManager =None,
        theIsToCreateCadenas     =False,
        theSolicitudesCadenasUIDsPorSimbolo =None,
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):
        
  
        unExecutionRecord = self.fStartExecution( 'method',  'fImportarContenidosIntercambio', theParentExecutionRecord, False) 

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators  import cModificationKind_CreateSubElement, cModificationKind_Create, cModificationKind_ChangeValues
        from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fDateTimeNow
        
        try:

            unSubExecutionRecord = self.fStartExecution( 'block',  'fImportarContenidosIntercambio-SubExecution to retrieve TRACatalog and accessible languages and modules', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
                        
            
            unImportResult = theProcessControlManager.vResult
            if not unImportResult:
                return None
            
            unInformeImportarContenidos = unImportResult.get( 'import_contents_report', {})
            unInformeImportarContenidos[ 'start_date'] =self.fDateTimeNowTextual()
            
            unCatalogo = self.getCatalogo()
            if unCatalogo == None:
                unInformeImportarContenidos[ 'error'] = "gvSIGi18n_NoRootCatalog_error_msgid"
                unInformeImportarContenidos[ 'end_date'] =self.fDateTimeNowTextual()
                return unInformeImportarContenidos
            
            #theProcessControlManager.pProcessStep( unCatalogo, { unCatalogo.meta_type: 1,}, { unCatalogo.meta_type: 1,})
            
            try:
                 
        
                  
                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)
                    
                aUseCaseNameToAssess = cUseCase_ImportTRAImportacion
                if theIsToCreateCadenas:
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


          
                    
            finally:
                unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
                
               
            try:    
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
                    theSolicitudesCadenasUIDsPorSimbolo=theSolicitudesCadenasUIDsPorSimbolo,
                    theInformeImportarContenidos=unInformeImportarContenidos, 
                    thePloneUtilsTool           =aPloneUtilsTool,
                    thePermissionsCache         =unPermissionsCache, 
                    theRolesCache               =unRolesCache, 
                    theParentExecutionRecord    =unExecutionRecord,
                )
            finally:
                unCatalogo.pInvalidateSimbolosCadenasOrdenados()  
                                    
                transaction.commit( )
            
                logging.getLogger( 'gvSIGi18n').info("COMMIT FINAL changes")  
                
                unCatalogo.pFlushCachedTemplates_All() 
            
            
            unSubExecutionRecord = self.fStartExecution( 'block',  'fImportarContenidosIntercambio-SubExecution to create status report after import and to clear the import progress report.', unExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
            try:
    
                unAhora = fDateTimeNow()
                
                unInformeImportarContenidos[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                unInformeImportarContenidos[ 'end_date']      = self.fDateToStoreString( unAhora)
                
                
                return unInformeImportarContenidos
            
            finally:
                unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
                    
  
        finally:
            self.getCatalogo().pFlushCachedTemplates_All()        
            
            unExecutionRecord and unExecutionRecord.pEndExecution()
     
                
                
        
       
        
        
        
        
        
        
        
        
        

    
    
    
        
    # ###################################################################
    """IMPORT PROCESS
    
    """
                
                
    
    security.declarePrivate( 'pImportarContenidosIntercambio')    
    def pImportarContenidosIntercambio( self,
        theProcessControlManager,
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
        theSolicitudesCadenasUIDsPorSimbolo,
        theInformeImportarContenidos, 
        thePloneUtilsTool,
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):
        """Import translations.
        
        Main loops to create languages, modules, strings and translations.
        
        """
        unExecutionRecord = self.fStartExecution( 'method',  'pImportarContenidosIntercambio', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }) 

        from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fDateTimeNow

        try:
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
                
                
            if not theUseCaseQueryResult or not theUseCaseQueryResult.get( 'success', False):
                unAhora = fDateTimeNow()
                theInformeImportarContenidos[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                theInformeImportarContenidos[ 'error'] = "gvSIGi18n_UseCaseNotPermitted_error_msgid"
                if theUseCaseQueryResult:
                    theInformeImportarContenidos[ 'error_detail'] = theUseCaseQueryResult.get( 'use_case_name', '')       
                else:
                    theInformeImportarContenidos[ 'error_detail'] = ''
                    
                raise TRAProcessErrorException( theInformeImportarContenidos[ 'error'], theInformeImportarContenidos[ 'error_detail'],)
    
            if ( theCatalogo == None) or not theContenido or not theInformeImportarContenidos:
                unAhora = fDateTimeNow()
                theInformeImportarContenidos[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                theInformeImportarContenidos[ 'error'] = "gvSIGi18n_MissingParameters_internal_error_msgid"
                theInformeImportarContenidos[ 'error_detail'] = ''
                raise TRAProcessErrorException( theInformeImportarContenidos[ 'error'], theInformeImportarContenidos[ 'error_detail'],)
            
            unaColeccionIdiomas = theCatalogo.fObtenerColeccionIdiomas()
            if ( unaColeccionIdiomas == None):
                unAhora = fDateTimeNow()
                theInformeImportarContenidos[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                theInformeImportarContenidos[ 'error'] = "gvSIGi18n_Missing_ColeccionIdiomas_internal_error_msgid"
                theInformeImportarContenidos[ 'error_detail'] = ''
                raise TRAProcessErrorException( theInformeImportarContenidos[ 'error'], theInformeImportarContenidos[ 'error_detail'],)
            
            unaColeccionModulos = theCatalogo.fObtenerColeccionModulos()
            if ( unaColeccionModulos == None):
                unAhora = fDateTimeNow()
                theInformeImportarContenidos[ 'fecha_informe'] = self.fDateToStoreString( unAhora)
                theInformeImportarContenidos[ 'error'] = "gvSIGi18n_Missing_ColeccionModulos_internal_error_msgid"
                theInformeImportarContenidos[ 'error_detail'] = ''
                raise TRAProcessErrorException( theInformeImportarContenidos[ 'error'], theInformeImportarContenidos[ 'error_detail'],)
            
            
            
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
                            unAhora = fDateTimeNow()
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
                            unAhora = fDateTimeNow()
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
                            unAhora = fDateTimeNow()  
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
                        unAhora = fDateTimeNow()  # SALIENDO EN CONDICION DE ERROR
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
                                
                                theProcessControlManager.pProcessStep( unaCadena, {}, { unaCadena.meta_type: 1, }, { unaCadena.meta_type: 1, })
                               
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
                                
                                unIndexEstadoTraduccionScanned       = unaTraduccionScanned.get( cScannedKeys_Translation_Status, None)
                                
                                if ( unIndexEstadoTraduccionScanned < 0) or ( unIndexEstadoTraduccionScanned > len( cTodosEstados)):
                                    unEstadoTraduccionScanned = cEstadoTraduccionTraducida
                                
                                else:
                                    unEstadoTraduccionScanned  = cTodosEstados[ unIndexEstadoTraduccionScanned]

                                    
                                    
                                    
                                unComentarioTraduccionScanned   = unaTraduccionScanned.get( cScannedKeys_Translation_Comment, None)

                                
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
                                            unUsuarioRevisor     = ''
                                            unaFechaRevision     = ''
                                            unUsuarioCoordinador = ''
                                            unaFechaDefinitivo   = ''
                                        
                                            unNuevoEstadoTraduccion = cEstadoTraduccionTraducida
                                            if unEstadoTraduccionScanned in [ cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva, ]:
                                                                        
                                                unNuevoEstadoTraduccion = unEstadoTraduccionScanned

                                                unUsuarioRevisor = theMemberId
                                                unaFechaRevision = unAhoraStoreString
                                    
                                                if unEstadoTraduccionScanned == cEstadoTraduccionDefinitiva:
                                                    unUsuarioCoordinador = theMemberId
                                                    unaFechaDefinitivo = unAhoraStoreString
                                            
                                            
                                            unaTraduccionExistente.setEstadoTraduccion(           unNuevoEstadoTraduccion)    
                                            unaTraduccionExistente.setUsuarioModificador(         unUsuarioModificador)   
                                            unaTraduccionExistente.setFechaModificacionTextual(   unaFechaModificacion)                                                
                                            unaTraduccionExistente.setUsuarioTraductor(           theMemberId)   
                                            unaTraduccionExistente.setFechaTraduccionTextual(     unAhoraStoreString)    
                                            unaTraduccionExistente.setUsuarioRevisor(             unUsuarioRevisor)  
                                            unaTraduccionExistente.setFechaRevisionTextual(       unaFechaRevision)
                                            unaTraduccionExistente.setUsuarioCoordinador(         unUsuarioCoordinador)   
                                            unaTraduccionExistente.setFechaDefinitivoTextual(     unaFechaDefinitivo)
                                            
                                            unaTraduccionExistente.pRegistrarHistoria( 
                                                theAccion                   = cTranslationHistoryAction_Importar, 
                                                theFechaAccionTextual       = unAhoraStoreString, 
                                                theUsuarioActor             = theMemberId, 
                                                theEstadoTraduccion         = cEstadoTraduccionTraducida, 
                                                theFechaTraduccionTextual   = unAhoraStoreString, 
                                                theUsuarioTraductor         = theMemberId, 
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
                                                        
                                                    if not ( unNuevoEstadoTraduccion == unEstadoTraduccion):
                                                        
                                                        if ( unIndexEstadoTraduccionScanned > unIndexEstadoTraduccion):
                                                            unUpgradeToEstado = unNuevoEstadoTraduccion
                                                        else:
                                                            if ( unIndexEstadoTraduccionScanned < unIndexEstadoTraduccion):
                                                                unTranslationIgnored = True                                                                                                                                                
                                                else:
                                                    
                                                    if unIndexEstadoTraduccionScanned >= unIndexEstadoTraduccion:
                                                        unUpdateCadenaTraducida = True
                                                        
                                                        if unIndexEstadoTraduccionScanned > unIndexEstadoTraduccion:
                                                            unUpgradeToEstado = unNuevoEstadoTraduccion
                                                        
                                                    else:
                                                        unTranslationIgnored = True

                                                    
                                                    
                                            unaCadenaTraducidaACambiar = ''
                                            unEstadoTraduccionACambiar = ''
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

                                                
                                                if ( unUpgradeToEstado == cEstadoTraduccionTraducida)  and ( unEstadoTraduccion in [ cEstadoTraduccionTraducida,]):
                                                    
                                                    unaTraduccionExistente.setUsuarioTraductor(         theMemberId)  
                                                    unaTraduccionExistente.setFechaTraduccionTextual(   unAhoraStoreString)
                                                    
                                                    unTraductorACambiar        = theMemberId
                                                    unaFechaTraduccionACambiar = unAhoraStoreString
                                                                      
                                                
                                                
                                                if ( unUpgradeToEstado in [ cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva]) and ( unEstadoTraduccion in [ cEstadoTraduccionTraducida, cEstadoTraduccionRevisada]):
                                                    
                                                    unaTraduccionExistente.setUsuarioRevisor(         theMemberId)  
                                                    unaTraduccionExistente.setFechaRevisionTextual(   unAhoraStoreString)
                                                    
                                                    unRevisorACambiar        = theMemberId
                                                    unaFechaRevisionACambiar = unAhoraStoreString
                                                
                                                    
                                                    
                                                if ( unUpgradeToEstado == cEstadoTraduccionDefinitiva) and ( unEstadoTraduccion in [ cEstadoTraduccionTraducida, cEstadoTraduccionRevisada]):
                                                                                                        
                                                    unaTraduccionExistente.setUsuarioCoordinador(     theMemberId)  
                                                    unaTraduccionExistente.setFechaDefinitivoTextual( unAhoraStoreString)
                                                    
                                                    unCoordinadorACambiar      = theMemberId
                                                    unaFechaDefinitivoACambiar = unAhoraStoreString
                                                    
                                                    
                                                    
                                            if unUpdateCadenaTraducida or unUpgradeToEstado:
                                                
                                                unaTraduccionExistente.setUsuarioModificador(         theMemberId)   
                                                unaTraduccionExistente.setFechaModificacionTextual(   unAhoraStoreString)    
                                                
                                                
                                                unaTraduccionExistente.pRegistrarHistoria( 
                                                    theAccion                   = cTranslationHistoryAction_Importar, 
                                                    theFechaAccionTextual       = unAhoraStoreString, 
                                                    theUsuarioActor             = theMemberId, 
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
  
        unUsuarioTraductor = ''
        unaFechaTraduccion = ''
        unUsuarioRevisor = ''
        unaFechaRevision = ''
        unUsuarioCoordinador = ''
        unaFechaDefinitivo = ''
                
        if unEstadoTraduccion in [ cEstadoTraduccionTraducida, cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva, ]:

            unUsuarioTraductor = theMemberId
            unaFechaTraduccion = unDateStoreString

            if unEstadoTraduccion in [ cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva, ]:
                unUsuarioRevisor = theMemberId
                unaFechaRevision = unDateStoreString

            if unEstadoTraduccion == cEstadoTraduccionDefinitiva:
                unUsuarioCoordinador = theMemberId
                unaFechaDefinitivo = unDateStoreString
                
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
            'usuarioCreador':       theMemberId, 
            'fechaCreacionTextual': unDateStoreString,  
            'usuarioTraductor':     unUsuarioTraductor, 
            'fechaTraduccionTextual': unaFechaTraduccion,  
            'usuarioRevisor':       unUsuarioRevisor, 
            'fechaRevisionTextual': unaFechaRevision,  
            'usuarioCoordinador':   unUsuarioCoordinador, 
            'fechaDefinitivoTextual':  unaFechaDefinitivo,  
            'fechaModificacionTextual': unaFechaModificacion,  
            'usuarioModificador':     unUsuarioModificador, 
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
    
    
    
   
    
    
    
    


    
    
    


    
    

    
    