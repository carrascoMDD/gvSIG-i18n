# -*- coding: utf-8 -*-
#
# File: TRAColeccionImportaciones_Operaciones.py
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
from TRAImportarExportar_Constants_GNUgettextPO   import *
from TRAImportarExportar_Constants_JavaProperties import *


from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_CreateTRAImportacion_RestoreBackup

from TRAElemento_Permission_Definitions import cBoundObject


class TRAColeccionImportaciones_Operaciones:
    """
    """
    security = ClassSecurityInfo()
     




    security.declarePrivate( 'pAllSubElements_into')    
    def pAllSubElements_into( self, theCollection, theAdditionalParams=None):
        if theCollection == None:
            return self
        theCollection.append( self)
        
        
        unosElementos = self.fObtenerTodasImportaciones()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pAllSubElements_into( theCollection,theAdditionalParams=theAdditionalParams)
        
        return self
        



    security.declarePrivate( 'pForAllElementsDo_recursive')    
    def pForAllElementsDo_recursive( self, theLambda=None, thePloneLambda=None,):
        if not theLambda:
            return self
        
        theLambda( self)
                                    
        unosElementos = self.fObtenerTodasImportaciones()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda, thePloneLambda)
                
        if thePloneLambda:
            self.pForAllElementsPloneDo( thePloneLambda)
        
        return self
        
    
    
    
    
    security.declareProtected( permissions.View, 'fObtenerTodasImportaciones')
    def fObtenerTodasImportaciones( self, ):
        """Retrieve all contained elements of type TRAImportacion.
        
        """
        unosElementos = self.fObjectValues( cNombreTipoTRAImportacion) 
        return unosElementos
         
          
    
    
    
    
    
    security.declareProtected( permissions.AddPortalContent, 'fCreateProgressHandlerFor_ImportToRestoreBackup')
    def fCreateProgressHandlerFor_ImportToRestoreBackup( self,  
        theUploadedFile                  =None, 
        thePermissionsCache              =None,
        theRolesCache                    =None,
        theParentExecutionRecord         =None,):
    

        unExecutionRecord = self.fStartExecution( 'method',  'fCreateProgressHandlerFor_ImportToRestoreBackup', None, True, { 'log_what': 'details', 'log_when': True, }) 

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators  import cModificationKind_CreateSubElement, cModificationKind_Create, cModificationKind_ChangeValues

        try:
            unasDescripcionesContenidosCreados = []
            try:
        
                aResult = self.fNewVoidCreateProgressHandlerResult()
                
                # ##################################################
                """Check essential parameters.
                
                """        
                if not theUploadedFile:
                    aResult.update( {
                        'success': False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_ErrorCreacionImportacionParaRecuperarCopiaSeguridad_FaltaFichero_warning_msgid', "Can not create an import element to restore a translations catalog backup, without an uploaded backup file.-"), 
                    })
                    return aResult  

                
                
                # ##################################################
                """Security Assessment.
                
                """        
                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)
                
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_CreateTRAImportacion_RestoreBackup, 
                    theElementsBindings     = { cBoundObject: self,}, 
                    theRulesToCollect       = None, 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord,
                )
              
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    aResult.update( {
                        'success': False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_no_permission_msgid', "User does not have permission to create interchange contents.-"), 
                    })
                    return aResult  
                            


                
                
                # ##################################################
                """Retrieve root translations catalog
                
                """
                unCatalogo = self.getCatalogo()
                
                if unCatalogo == None:
                    aResult.update( {
                        'success': False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_internal_Missing_RootCatalog', "Internal error: missing root translations catalog-."), 
                    })
                    return aResult
                

                               
                
                                    
                # ##################################################
                """Obtain tools.
                
                """        
                aModelDDvlPlone_tool = self.fModelDDvlPloneTool()
                if aModelDDvlPlone_tool == None:
                    aResult.update( {
                        'success': False,
                        'condition': 'No_ModelDDvlPlone_tool', 
                    })
                    return aResult     

                aPloneUtilsTool      = self.getPloneUtilsToolForNormalizeString()  
                if aPloneUtilsTool == None:
                    aResult.update( {
                        'success': False,
                        'condition': 'No_PloneUtilsToolForNormalizeString', 
                    })
                    return aResult     
                             
            
                
                
        
                # ##################################################
                """Scan archive for XML file and relevant binary files.
                
                """        
                anXMLSource             = None
                anXMLFileName             = None
                someFilesDataByFileName = { }
                
                aScanUploadedFileResult = aModelDDvlPlone_tool.fScanXMLAndBinariesFromUploadedFile(
                    theTimeProfilingResults        =None,
                    theContextualElement           =self, 
                    theUploadedFile                =theUploadedFile,
                    theAcceptedXMLRootNodeName     =cNombreTipoTRACatalogo,
                    theExcludedFullFileNames       =[ cLocalesCSVFileFullName, cManifestFileFullName,],
                    theExcludedFilePostfixes       =[ cPOFilePostfix, cPOTFilePostfix, cPropertiesFilePostfix,],
                    theAdditionalParams            =None,
                )
                if aScanUploadedFileResult and aScanUploadedFileResult.get( 'success', False):
                    
                    anXMLFileName           = aScanUploadedFileResult.get( 'xml_full_filename', None)
                    anXMLSource             = aScanUploadedFileResult.get( 'xml_source', None)
                    someFilesDataByFileName = aScanUploadedFileResult.get( 'files_whole_data_by_full_name', None)
                    
                    if not anXMLSource:
                        aResult.update( {
                            'success': False,
                            'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_ErrorCreacionImportacionParaRecuperarCopiaSeguridad_NoXMLFile_msgid', "Can not restore a translations catalog backup, without an XML file in the uploaded backup file.-"), 
                        })
                        return aResult  
                        
                    
                

                unMemberId        = self.fGetMemberId_safe()
                aFechaHoraTextual = self.fDateTimeNowString()

                # ##################################################
                """Generate unique title and id for new import element.
                
                """        
                unBaseTitle    = 'Import to Restore Backup by %s on %s' % ( unMemberId, aFechaHoraTextual )
                unaDescripcion = unBaseTitle[:]
                unTexto        = unBaseTitle[:]
                       

                someImports = self.fObtenerTodasImportaciones()
                
                
                someTitles = [ unImport.Title() for unImport in someImports]
                someIds    = [ unImport.getId() for unImport in someImports]
                
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


                # ##################################################
                """Create instance of new import element.
                
                """        
                anAttrsDict = { 
                    'title':                    unTitle,
                    'description':              unaDescripcion,
                    'text':                     unTexto,
                    'usuarioImportador':        unMemberId,
                    'esRecuperacion':           True,
                }
                
                unaIdNuevaImportacion = self.invokeFactory( cNombreTipoTRAImportacion, aNewId, **anAttrsDict)
                if not unaIdNuevaImportacion:
                    aResult.update( {
                        'success': False,
                        'condition': '%s ' %   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_ErrorCreacionImportacionParaRecuperarCopiaSeguridad_errorencreacion', "No se ha podido crear Importacion para Recuperar Copia de Seguridad.-"),
                    })
                    return aResult     
                                
                unaNuevaImportacion = self.getElementoPorID( unaIdNuevaImportacion)
                if not unaNuevaImportacion:
                    aResult.update( {
                        'success': False,
                        'condition': '%s' %   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_ErrorCreacionImportacionParaRecuperarCopiaSeguridad_ElementoEncontradoNotFound', "No se encuentra la Importacion creada para Recuperar Copia de Seguridad.-"), 
                    })
                    return aResult     

                unaNuevaImportacion.pInitDefaultAttributesFromConfiguration()

                
                
                
                
                
                # ##################################################
                """Retrieve created instance of new import element.
                
                """                        
                unResultadoNuevaImportacion = aModelDDvlPlone_tool.fRetrieveTypeConfig( 
                    theTimeProfilingResults     =None,
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
                    aResult.update( {
                        'success': False,
                        'condition': 'retrieval_failure', 
                    })
                    return aResult     
 
                unaImportacionCreationReport = { 'effect': 'created', 'new_object_result': unResultadoNuevaImportacion, }
                     

                
                
                # ##################################################
                """Record change of creating new import element.
                
                """                        
                aModelDDvlPloneTool_Mutators = aModelDDvlPlone_tool.fModelDDvlPloneTool_Mutators( self)
                    
                aCreateElementReport = aModelDDvlPloneTool_Mutators.fNewVoidCreateElementReport()
                aCreateElementReport.update( { 'effect': 'created', 'new_object_result': unResultadoNuevaImportacion, })
                                                           
                aModelDDvlPloneTool_Mutators.pSetAudit_Creation( self,                        cModificationKind_CreateSubElement, aCreateElementReport, theUseCounter=True)       
                aModelDDvlPloneTool_Mutators.pSetAudit_Creation( unaNuevaImportacion,         cModificationKind_Create,           aCreateElementReport)       

                
                
                # ##################################################
                """COMMIT creation of new import element.
                
                """                        
                transaction.commit()
                
                logging.getLogger( 'gvSIGi18n').info("COMMIT new %s %s with description\n%s\nand text:\n%s\n" % ( cNombreTipoTRAImportacion, unTitle,  unaDescripcion, unTexto, )) 
                
                
                
                
                
                # ##################################################
                """Flush all cached pages in the translations catalog, such that new user requests to view pages reflect the elements about to be created.
                
                """                        
                unCatalogo.pFlushCachedTemplates_All()                            
                
        
                
                

                # ##################################################
                """Read interchange contents from archive, and create elements to contain the strings and translations read.
                
                """                                        
       
                aCrearContenidoIntercambioAdditionalParams = {
                    'theUploadedFile':                         theUploadedFile,
                    'theDefaultLanguage':                      unaNuevaImportacion.getCodigoIdiomaPorDefecto(),
                    'theDefaultModule':                        unaNuevaImportacion.getNombreModuloPorDefecto(),
                    'theImportWithConfiguredModuleName':       unaNuevaImportacion.getImportarConNombreModuloConfigurado(),
                    'theImportModuleNameFromDomainOrFilename': unaNuevaImportacion.getImportarNombreModuloDesdeDominioONombreFichero(),
                    'theImportModuleNamesFromComment':         unaNuevaImportacion.getImportarContribucionesDesdeComentarios(),
                    'theImportContributionsFromComment':       unaNuevaImportacion.getImportarContribucionesDesdeComentarios(),
                    'theImportSourcesFromComment':             unaNuevaImportacion.getImportarFuentesDesdeComentarios(),
                    'theImportStatusFromComment':              unaNuevaImportacion.getImportarStatusDesdeComentarios(),
                    'theMaxLinesToScan':                       unaNuevaImportacion.getNumeroMaximoLineasAExplorar(),
                }
            

                    
                aCrearContenidoIntercambioResult = unaNuevaImportacion.fCrearContenidoIntercambio(
                    theTimeProfilingResults =None,
                    theModelDDvlPloneTool_Mutators =aModelDDvlPloneTool_Mutators, 
                    theNewTypeName          =cNombreTipoTRAContenidoIntercambio, 
                    theNewOneTitle          ='', 
                    theNewOneDescription    ='', 
                    theAdditionalParams     =aCrearContenidoIntercambioAdditionalParams,
                    thePermissionsCache     =unPermissionsCache,
                    theRolesCache           =unRolesCache,
                    theParentExecutionRecord=unExecutionRecord,
                )
                
                
                
                
                # ##################################################
                """Create XML and Binary content element to hold the data read.
                
                """                                                        
                someContenidosBinarios = [ ]
                for aFullFileName in someFilesDataByFileName.keys():
                    
                    aFileWholeData = someFilesDataByFileName.get( aFullFileName, '')
                    aNewContenidoBinario = {
                        'file_full_name':  aFullFileName,
                        'file_whole_data': aFileWholeData,
                    }
                    someContenidosBinarios.append( aNewContenidoBinario)
                        
                                      
                aCrearContenidoXMLResult = unaNuevaImportacion.fCrearContenidoXML(
                    theTimeProfilingResults =None,
                    theModelDDvlPloneTool_Mutators =aModelDDvlPloneTool_Mutators, 
                    theFileName             =anXMLFileName, 
                    theXMLSource            =anXMLSource, 
                    theContenidoBinario     =someContenidosBinarios, 
                    theAdditionalParams     =None,
                    thePermissionsCache     =unPermissionsCache,
                    theRolesCache           =unRolesCache,
                    theParentExecutionRecord=unExecutionRecord,
                )
                if not ( aCrearContenidoXMLResult and ( aCrearContenidoXMLResult.get( 'effect', '') == 'created') and not( aCrearContenidoXMLResult.get( 'new_object_result', {}).get( 'object', None) == None)):
                    aResult.update( {
                        'success': False,
                        'condition': 'CrearContenidoXML_failure', 
                    })
                    return aResult     
                               
                    
 
                        
                    

                    
                    
                # ##################################################
                """Create a TRAProgreso element to control the progress of the long living import process, and save the results. 
                
                """
                   
                aProgressHandlerCreationResult = unaNuevaImportacion.fCreateProgressHandlerFor_Import( 
                    theAdditionalParams     ={},
                    thePermissionsCache     =unPermissionsCache,
                    theRolesCache           =unRolesCache,
                    theParentExecutionRecord=unExecutionRecord,
                )
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
                                
                
                # ##################################################
                """Flush all cached pages in the translations catalog, such that new user requests to view pages reflect the elements about to be created.
                
                """
                unCatalogo.pFlushCachedTemplates_All()           
                                    
                    
                return aResult
            
            
                
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fCreateProgressHandlerFor_ImportToRestoreBackup\n' 
                try:
                    unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                except:
                    None
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   
                                         
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                aResult.update( {
                    'success': False,
                    'condition': 'Error creating Import to Restore Backup',
                })
                return aResult     
              
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

        
                
                
                    

