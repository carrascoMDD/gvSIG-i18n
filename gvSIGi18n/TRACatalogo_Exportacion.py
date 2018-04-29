# -*- coding: utf-8 -*-
#
# File: TRACatalogo_Exportacion.py
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

import sys
import traceback
import logging

from codecs                 import lookup           as CODECS_Lookup
from codecs                 import EncodedFile      as CODECS_EncodedFile


from AccessControl          import ClassSecurityInfo

from Products.CMFCore       import permissions

from Products.CMFCore.utils import getToolByName


##code-section module-header #fill in your manual code here


from StringIO import StringIO

from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED



from TRAElemento_Constants                 import *
from TRAElemento_Constants_Activity        import *
from TRAElemento_Constants_Configurations  import *
from TRAElemento_Constants_Contributions   import *
from TRAElemento_Constants_Contributions   import *
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
from TRAImportarExportar_Constants import *
from TRAImportarExportar_Constants_Encodings import *
from TRAImportarExportar_Constants_GNUgettextPO import *
from TRAImportarExportar_Constants_JavaProperties import *

from TRAElemento_Permission_Definitions import cBoundObject

from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_ImportTRAImportacion, cUseCase_Export, cUseCase_Backup_TRACatalogo, cUseCase_ExportGvSIG_TRAIdioma, cUseCase_ExportGvSIG_All_TRAIdioma


from TRACatalogo_Exportacion_GNUgettextPO   import TRACatalogo_Exportacion_GNUgettextPO
from TRACatalogo_Exportacion_JavaProperties import TRACatalogo_Exportacion_JavaProperties




##/code-section module-header


##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema



##code-section after-schema #fill in your manual code here


##/code-section after-schema

class TRACatalogo_Exportacion( TRACatalogo_Exportacion_GNUgettextPO, TRACatalogo_Exportacion_JavaProperties):
    """
    """
    security = ClassSecurityInfo()


    ##code-section class-header #fill in your manual code here
    


          


    
    


    security.declarePrivate( 'fExportTypeConfigsChosen')
    def fExportTypeConfigsChosen( self,
        theAllExportTypeConfigs                 =None,
        theExportarTRACatalogo                  =None,
        theExportarTRAConfiguraciones           =None,           
        theExportarTRAParametrosControlProgreso =None,
        theExportarTRAIdiomas                   =None,                
        theExportarTRAModulos                   =None,                  
        theExportarTRAInformes                  =None,                  
        theExportarTRASolicitudesCadenas        =None,):
        
        if not theAllExportTypeConfigs:
            return {}
        
        
    
        someTypeConfigFilters = [ ]
        
        # ########################################################
        """Attributes to export for all configs.
        
        """
        aBaseTypeConfigFilter = cExportarXMLTypeConfigFilters.get( 'base', [])
        if aBaseTypeConfigFilter:
            someTypeConfigFilters.extend( aBaseTypeConfigFilter)
        
            
        # ########################################################
        """Element sets chosen to be exported: Root catalog, configurations, process control parameters, languages, modules, reports, imports, progresses, string requests.
        
        """    
        if theExportarTRACatalogo:
            aTypeConfigFilter =  cExportarXMLTypeConfigFilters.get( 'TRACatalogo', [])
            if aTypeConfigFilter:
                someTypeConfigFilters.extend( aTypeConfigFilter)
        
        
        if theExportarTRAConfiguraciones:
            aTypeConfigFilter =  cExportarXMLTypeConfigFilters.get( 'TRAConfiguraciones', [])
            if aTypeConfigFilter:
                someTypeConfigFilters.extend( aTypeConfigFilter)
                
        
        if theExportarTRAParametrosControlProgreso:
            aTypeConfigFilter =  cExportarXMLTypeConfigFilters.get( 'TRAParametrosControlProgreso', [])
            if aTypeConfigFilter:
                someTypeConfigFilters.extend( aTypeConfigFilter)
                
        
        if theExportarTRAIdiomas:
            aTypeConfigFilter =  cExportarXMLTypeConfigFilters.get( 'TRAIdiomas', [])
            if aTypeConfigFilter:
                someTypeConfigFilters.extend( aTypeConfigFilter)
                
        if theExportarTRAModulos:
            aTypeConfigFilter =  cExportarXMLTypeConfigFilters.get( 'TRAModulos', [])
            if aTypeConfigFilter:
                someTypeConfigFilters.extend( aTypeConfigFilter)
                
                
        if theExportarTRAInformes:
            aTypeConfigFilter =  cExportarXMLTypeConfigFilters.get( 'TRAInformes', [])
            if aTypeConfigFilter:
                someTypeConfigFilters.extend( aTypeConfigFilter)
                                                                                
        if theExportarTRASolicitudesCadenas:
            aTypeConfigFilter =  cExportarXMLTypeConfigFilters.get( 'TRASolicitudesCadenas', [])
            if aTypeConfigFilter:
                someTypeConfigFilters.extend( aTypeConfigFilter)
         
                
                
                
                
        # ########################################################
        """Merge selection of element types, attributes and traversals to be exported.
        
        """    
            
        aMergedTypeConfigFilter = { }
        
        for aTypeConfigFilter in someTypeConfigFilters:
            aPortalType = aTypeConfigFilter.get( 'portal_type', '')
            if aPortalType:
                
                aMergedTypeConfigFilterForType = aMergedTypeConfigFilter.get( aPortalType, None)
                if aMergedTypeConfigFilterForType == None:
                    aMergedTypeConfigFilterForType = { 
                        'portal_type': aPortalType, 
                        'attrs':       set(), 
                        'traversals':  set(),
                    }
                    aMergedTypeConfigFilter[ aPortalType] = aMergedTypeConfigFilterForType
                    
                someAttrs = aTypeConfigFilter.get( 'attrs', [])
                if someAttrs:
                    aMergedTypeConfigFilterForType[ 'attrs'].update( set( someAttrs))
                                                                     
                someTraversals = aTypeConfigFilter.get( 'traversals', [])
                if someTraversals:
                    aMergedTypeConfigFilterForType[ 'traversals'].update( set( someTraversals))
                                                                     
            
        
               
        # ########################################################
        """ Build a traversal config by filtering the overall traversal config for all the elements with the types, attributes and traversals chosen above.
        
        """    
                    
        aTypeConfigsChosen = { }
        
        for aPortalType in theAllExportTypeConfigs.keys():
            
            aTypeConfig           = theAllExportTypeConfigs.get( aPortalType, None)
            if aTypeConfig:
                
                if ( aPortalType == cTRAImagePortalType) and theExportarTRAIdiomas:
                    
                    aTypeConfigsChosen [ aPortalType] = aTypeConfig.copy()
                    
                    
                    
                else:
                    
                
                    someConfigAttrs       = aTypeConfig.get( 'attrs',        [])
                    someConfigTraversals  = aTypeConfig.get( 'traversals',   [])
                    
                    aTypeConfigFilterForType = aMergedTypeConfigFilter.get( aPortalType, None)
                    if aTypeConfigFilterForType:
                        
                        someFilteredAttrs      = aTypeConfigFilterForType.get( 'attrs',      set())
                        someFilteredTraversals = aTypeConfigFilterForType.get( 'traversals', set())
                        
                        someChosenAttributeConfigs = cExportarXMLAnyTypeAttributeConfigs[:]
                        someChosenTraversalConfigs = [ ]
                        
                        aTypeConfig = {
                            'portal_types':    [ aPortalType,],
                            'attrs':           someChosenAttributeConfigs,
                            'traversals':      someChosenTraversalConfigs,
                        }
                
                        aTypeConfigsChosen [ aPortalType] = aTypeConfig
                        
                        for aConfigAttr in someConfigAttrs:
                            aConfigAttrName = aConfigAttr.get( 'name', '')
                            if aConfigAttrName and ( aConfigAttrName in someFilteredAttrs):
                                someChosenAttributeConfigs.append( aConfigAttr)
                                
                        for aConfigTraversal in someConfigTraversals:
                            aConfigTraversalName = aConfigTraversal.get( 'aggregation_name', aConfigTraversal.get( 'relation_name', ''))
                            if aConfigTraversalName and ( aConfigTraversalName in someFilteredTraversals):
                                someChosenTraversalConfigs.append( aConfigTraversal)
                                
                                
        return aTypeConfigsChosen
                
    
    
    

    
    security.declarePublic( 'fLabelModuloNoEspecificado')    
    def fLabelModuloNoEspecificado( self):
        unLabelModuloNoEspecificado = u' ? ' + self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_ModuloNoEspecificado_msgid',  'not specified' )
        aTranslationService = self.getTranslationServiceTool()
        if not aTranslationService:
            return ''
        return aTranslationService.encode( unLabelModuloNoEspecificado) 
         
    
    
    
    
    security.declarePrivate( 'fNewVoidProgressResult_Export')
    def fNewVoidProgressResult_Export( self, ):
        unResult = self.fNewVoidProgressResult()
        unResult.update( {
            'export_report':            { },
        })
        return unResult
                
      
    
    
    security.declarePrivate( 'fNewVoidInformeExportarTraducciones')    
    def fNewVoidInformeExportarTraducciones( self,):
        unInforme = {
            'success':                  False,
            'status':                   '',
            'exception':                '',
            'archive_type':             '',
            'export_format':            '',
            'include_manifest':         '',
            'include_localescsv':       '',
            'separate_modules':         False,
            'export_module_names':      False,
            'export_string_sources':    False,
            'export_translation_status':False,
            'export_contributions':     False,
            'languages_requested':      [],
            'reference_languages':      {},
            'languages_export_reports': [],
            'modules_requested':        [],
            'unspecified_module_requested': False,
            'exported_module_names':    [],
            'exported_unspecified_module': False,
            'download_filename':        '',
            'num_encoding_errors':      0,
        }
        return unInforme

      
    
    
    
    security.declarePrivate( 'fNewVoidInformeExportarTraduccionesDeIdioma')    
    def fNewVoidInformeExportarTraduccionesDeIdioma( self,):
        unInforme = {
            'language_code':            '',
            'success':                  False,
            'status':                   '',
            'exception':                '',
            'encoding':                 '',
            'reference_language_code':  '',
            'translations_exported':    0,
            'filename':                 '',
            'filename_properties':      '',
            'filename_po':              '',
            'modules_export_reports':   [],
            'export_result':            {},
        }
        return unInforme
    
    
    security.declarePrivate( 'fNewVoidInformeExportarTraduccionesDeIdioma')    
    def fNewVoidInformeExportarTraduccionesDeModulo( self,):
        unInforme = {
            'language_code':           '',
            'module_name':             '',
            'success':                  False,
            'status':                   '',
            'exception':                '',
            'translations_exported':    0,
            'filename':                 '',
            'filename_properties':      '',
            'filename_po':              '',
            'export_result':            {},
        }
        return unInforme
    
    

     
    security.declareProtected( permissions.View, 'fEncodingErrorHandleModes')    
    def fEncodingErrorHandleModes( self, ):
        return cTRAEncodingErrorHandleModes[:]
    
        
    
    
          
                
    
    security.declareProtected( permissions.View, 'fEstimarContenidoExportacion')    
    def fEstimarContenidoExportacion( self, 
        theParametersInput               = {},
        thePermissionsCache              = None,
        theRolesCache                    = None,
        theUseCaseAssessmentResultsCache = None,
        theParentExecutionRecord         = None):
        """Export Translations to the selected languages, including the selected reference languates, for the selected modules and/or the strings that specify no module, in the Java .properties or GNU gettext PO formats, possibly in separated modules, packaged in an archive of the specified name, and handling the encoding errors.
        
        """
  
        unExecutionRecord = self.fStartExecution( 'method',  'fExportarTraducciones', theParentExecutionRecord, False) 

        try:
            
            try:
                    
                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)

                
                
               # ##############################################################################
                """Shall return a report including the relevant request parameters.
                
                """
                unInforme = self.fNewVoidInformeExportarTraducciones()
                
                theCodigosIdiomas               = theParametersInput.get( 'theLanguagesToExport', [])
                theCodigosIdiomasReferencia     = theParametersInput.get( 'theCodigosIdiomaReferencia', {})
                theCodificacionesCaracteres     = theParametersInput.get( 'theCodificacionesCaracteres', {})
                theNombresModulos               = theParametersInput.get( 'theModulesToExport', [])
                theIncluirModuloNoEspecificado  = cModuloNoEspecificado_ValorNombre in theNombresModulos
                theExportFormat                 = theParametersInput.get( 'theExportFormat', '')
                theIncludeManifest              = theParametersInput.get( 'theIncludeManifest', '')    == ( theParametersInput.get( 'theIncludeManifest_vocabulary',  ['xXxXxXx',])[ 0])
                theIncludeLocalesCSV            = theParametersInput.get( 'theIncludeLocalesCSV', '')  == ( theParametersInput.get( 'theIncludeLocalesCSV_vocabulary',  ['xXxXxXx',])[ 0])
                theSeparatedModules             = theParametersInput.get( 'theSeparatedModules', '')   == ( theParametersInput.get( 'theSeparatedModules_vocabulary', ['xXxXxXx',])[ 0])
                theExportModuleNames            = theParametersInput.get( 'theExportModuleNames', '') == ( theParametersInput.get( 'theExportModuleNames_vocabulary', ['xXxXxXx',])[ 0])
                theExportContributions            = theParametersInput.get( 'theExportContributions', '') == ( theParametersInput.get( 'theExportContributions_vocabulary', ['xXxXxXx',])[ 0])
                theExportStringSources          = theParametersInput.get( 'theExportStringSources', '') == ( theParametersInput.get( 'theExportStringSources_vocabulary', ['xXxXxXx',])[ 0])
                theExportTranslationsStatus     = theParametersInput.get( 'theExportTranslationsStatus', '') == ( theParametersInput.get( 'theExportTranslationsStatus_vocabulary', ['xXxXxXx',])[ 0])
                theTipoArchivo                  = theParametersInput.get( 'theTipoArchivo', '')
                theDefaultLanguageCode          = theParametersInput.get( 'theDefaultLanguageCode', '')
                theDefaultModuleName            = theParametersInput.get( 'theDefaultModuleName', '')
                theDefaultDomain                = theParametersInput.get( 'theDefaultDomain', '')
                theEncodingErrorHandleMode      = theParametersInput.get( 'theEncodingErrorHandleMode', '')
                theFilenameForGvSIG             = theParametersInput.get( 'theFilenameForGvSIG', '')   == ( theParametersInput.get( 'theFilenameForGvSIG_vocabulary', ['xXxXxXx',])[ 0])
                theProductName                  = theParametersInput.get( 'theProductName', '')
                theProductVersion               = theParametersInput.get( 'theProductVersion', '')
                theL10NVersion                  = theParametersInput.get( 'theL10NVersion', '')
                theSpecificFilename             = theParametersInput.get( 'theSpecificFilename', '')
                
       
                 
                unInforme[ 'languages_requested'] = ( theCodigosIdiomas or [])[:]
                unInforme[ 'reference_languages']   = ( theCodigosIdiomasReferencia and theCodigosIdiomasReferencia.copy()) or {}
                unInforme[ 'modules_requested']   = ( theNombresModulos or [])[:]
                unInforme[ 'unspecified_module_requested'] = theIncluirModuloNoEspecificado
                
                
                # ##############################################################################
                """Cancel export if no languages requested.
                
                """
                if not theCodigosIdiomas:
                    unInforme.update( {
                        'success':              False,
                        'status':               cExportStatus_NoLanguagesRequestedForExport,
                    })
                    return unInforme
                
                
                        
                # ##############################################################################
                """Cancel export if no modules requested and not requested the strings with unspecified module.
                
                """
                if ( not theNombresModulos) and not theIncluirModuloNoEspecificado:
                    unInforme.update( {
                        'success':              False,
                        'status':               cExportStatus_NoModulesRequestedForExport,
                    })
                    return unInforme
                        
                         
                
                # ##############################################################################
                """Query for languages and modules accessible in the UseCase.
                
                """
                aUseCaseAssessmentResult = self.fUseCaseAssessment( 
                    theUseCaseName          = cUseCase_Export, 
                    theElementsBindings     = { cBoundObject: self,},
                    theRulesToCollect       = [ 'languages', 'modules',], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord,
                )
                
                
                
                
                # ##############################################################################
                """Check the user is authorized to exercise the UseCase.
                
                """
                if not aUseCaseAssessmentResult or not aUseCaseAssessmentResult.get( 'success', False):
                    unInforme.update( {
                        'success':              False,
                        'status':               cExportStatus_UseCaseAssessmentFailed,
                        'condition':            cUseCase_Export,
                    })
                    return unInforme
                
                
                
                            
        
                # ##############################################################################
                """Shall export as .properties and/or .PO, with .properties by default.
                
                """
                unArchiveType               = theTipoArchivo
                if not ( unArchiveType in cExportArchiveTypes):
                    unArchiveType = cZipFilePostfix
                unInforme[ 'archive_type']  = unArchiveType
                
                unExportAsJavaProperties   = theExportFormat  == cExportFormatOption_JavaProperties
                unExportAsGNUgettextPO     = theExportFormat  == cExportFormatOption_GNUgettextPO
                if not unExportAsJavaProperties and not unExportAsGNUgettextPO:
                    unExportAsJavaProperties = True
                unInforme[ 'export_format']    = ( unExportAsGNUgettextPO and cExportFormatOption_GNUgettextPO) or cExportFormatOption_JavaProperties
                    
                unIncludeManifest               = theIncludeManifest and True
                unInforme[ 'include_manifest']  = unIncludeManifest
                
                unIncludeLocalesCSV               = theIncludeLocalesCSV and True
                unInforme[ 'include_localescsv']  = unIncludeLocalesCSV
                
                unSeparatedModules              = theSeparatedModules and True           
                unInforme[ 'separate_modules']  = unSeparatedModules
            
                unExportModuleNames              = theExportModuleNames and True           
                unInforme[ 'export_module_names']= unExportModuleNames
                
                unExportContributions              = theExportContributions and True           
                unInforme[ 'export_contributions'] = unExportContributions
                
                unExportStringSources              = theExportStringSources and True           
                unInforme[ 'export_string_sources']= unExportStringSources
                
                unExportTranslationsStatus              = theExportTranslationsStatus and True           
                unInforme[ 'export_translation_status']= unExportTranslationsStatus
                                    
                
                
                # ##############################################################################
                """Scan the list of languages requested by the user to export for translation and as reference. Do not consider languages that are not accessible for the user.
                
                """
                unosCodigosIdiomasReferencia = set( )
                for unCodigoIdioma in theCodigosIdiomas:
                    unCodigoIdiomaReferencia = theCodigosIdiomasReferencia.get( unCodigoIdioma, '')
                    if unCodigoIdiomaReferencia:
                        unosCodigosIdiomasReferencia.add( unCodigoIdiomaReferencia)
                  
                unosIdiomasVisibles = aUseCaseAssessmentResult.get( 'collected_rule_assessments_by_name', {}).get( 'languages', {}).get( 'accepted_final_objects', [])
                 
                unosCodigosEIdiomasAExportar          = [ ]
                unosCodigosIdiomasAExportar           = set()
                unosCodigosIdiomasReferenciaAExportar = set()
                
                for unIdioma in unosIdiomasVisibles:
                    unCodigoIdioma = unIdioma.getCodigoIdiomaEnGvSIG()
                                        
                    if unCodigoIdioma in theCodigosIdiomas:
                        unosCodigosEIdiomasAExportar.append( [ unCodigoIdioma, unIdioma, ])
                        unosCodigosIdiomasAExportar.add( unCodigoIdioma)
                        
                        
                for unIdioma in unosIdiomasVisibles:
                    unCodigoIdioma = unIdioma.getCodigoIdiomaEnGvSIG()
                    
                    if ( unCodigoIdioma in unosCodigosIdiomasReferencia) and ( not( unCodigoIdioma in unosCodigosIdiomasAExportar)) and ( not ( unCodigoIdioma in unosCodigosIdiomasReferenciaAExportar)):
                        unosCodigosIdiomasReferenciaAExportar.add( unCodigoIdioma)
                        if unExportAsJavaProperties:
                            unosCodigosEIdiomasAExportar.append( [ unCodigoIdioma, unIdioma, ])
                                 

                unosCodigosEIdiomasOrdenados = sorted( unosCodigosEIdiomasAExportar, cmp=lambda uno, otro: cmp( uno[ 0], otro[ 0]))
                         

                
                
                # ##############################################################################
                """Cancel export if no languages allowed to export.
                
                """
                if not unosCodigosEIdiomasOrdenados:
                    unInforme.update( {
                        'success':              False,
                        'status':               cExportStatus_NoAvailableLanguagesToExport,
                    })
                    return unInforme
                 
                
                 
        
                # ##############################################################################
                """Do not consider modules that are not accessible for the user.
                
                """
                unosModulosVisibles = aUseCaseAssessmentResult.get( 'collected_rule_assessments_by_name', {}).get( 'modules', {}).get( 'accepted_final_objects', [])
                
                unosNombresModulosAExportar = []
                for unModulo in unosModulosVisibles:
                    unNombreModulo = unModulo.Title()
                    if ( unNombreModulo in theNombresModulos) and not ( unNombreModulo in unosNombresModulosAExportar):
                        unosNombresModulosAExportar.append( unNombreModulo)
                        
                unosNombresModulosOrdenados  = sorted( unosNombresModulosAExportar)
                
                
                
                
                        
                # ##############################################################################
                """Cancel export if no modules  allowed to export.
                
                """
                if ( not unosNombresModulosOrdenados) and not theIncluirModuloNoEspecificado:
                    unInforme.update( {
                        'success':              False,
                        'status':               cExportStatus_NoAvailableModulesToExport,
                    })
                    return unInforme
                        
                unInforme[ 'exported_module_names']        = unosNombresModulosOrdenados
                unInforme[ 'exported_unspecified_module']  = ( theIncluirModuloNoEspecificado and True) or False
                    

                
                
                
                
                # ##############################################################################
                """Make sure requested character encodings are known, or default to utf-8.
                
                """
                unasCodificacionesCaracteres = { }
                
                for unCodigoIdioma, unIdioma in unosCodigosEIdiomasOrdenados:
                    
                    unaCodificacionIdioma = ''
                    if unExportAsJavaProperties:
                        unaCodificacionIdioma   = unIdioma.getJuegoDeCaracteresParaJavaProperties()
                    else:
                        unaCodificacionIdioma   = unIdioma.getJuegoDeCaracteresParaPO()
                        
                    unaCodificacionIdiomaParametro = theCodificacionesCaracteres.get( unCodigoIdioma, '')
                         
                    if not unaCodificacionIdiomaParametro:
                        unaCodificacionIdiomaParametro = unaCodificacionIdioma
                        
                    unCodecInfo = None
                    try:
                        unCodecInfo = CODECS_Lookup( unaCodificacionIdiomaParametro)
                    except:
                        None
                    if unCodecInfo:
                        unasCodificacionesCaracteres[ unCodigoIdioma] = unaCodificacionIdiomaParametro
                    else:
                        unasCodificacionesCaracteres[ unCodigoIdioma] = cTRAEncodingUTF8
                     
            
                
                
                


                    
               
    
                    
                # ##############################################################################
                """Export each requested and allowed language.
                
                """
                unCodigoUltimoIdioma                              = None
                unosResultadosTraduccionesUltimoIdioma            = None
                unoCodigoUltimoIdiomaReferencia                   = None
                unosResultadosTraduccionesUltimoIdiomaReferencia  = None
                
                

                 
                

                
                
                unHayError = False
                
                
                for unCodigoEIdioma in unosCodigosEIdiomasOrdenados:
                    unCodigoIdioma  = unCodigoEIdioma[ 0]
                    unIdioma        = unCodigoEIdioma[ 1]
                    
                    unInformeExportarIdioma = self.fNewVoidInformeExportarTraduccionesDeIdioma()
                    
                    
                    unInformeExportarIdioma[ 'language_code'] = unCodigoIdioma
                    unInforme[ 'languages_export_reports'].append( unInformeExportarIdioma)
                    
                    unaCodificacionCaracteres = unasCodificacionesCaracteres.get( unCodigoIdioma, cTRAEncodingUTF8)
                    unInformeExportarIdioma[ 'encoding'] = unaCodificacionCaracteres
                    
                    unCodigoIdiomaReferencia = theCodigosIdiomasReferencia.get( unCodigoIdioma, '')
                    if unCodigoIdiomaReferencia in unosCodigosIdiomasReferenciaAExportar:
                        unInformeExportarIdioma[ 'reference_language_code'] = unCodigoIdiomaReferencia
                    else:
                        unCodigoIdiomaReferencia  = ''
                        
                    
                    if unSeparatedModules:
                        # ##############################################################################
                        """Export translations into the language with the strings in each requested module on its own output file, iterating over each named requested module and the not-specified module if requested.
                        
                        """
                        
                        unInformeExportarIdioma[ 'separate_modules'] = True
                        
                        for unNombreModulo in unosNombresModulosOrdenados:
                            
                            unInformeExportarModulo = self.fNewVoidInformeExportarTraduccionesDeModulo()
                            unInformeExportarModulo[ 'language_code'] = unCodigoIdioma
                            unInformeExportarModulo[ 'module_name']   = unNombreModulo
                            unInformeExportarIdioma[ 'modules_export_reports'].append( unInformeExportarModulo)
        
                            unFileNameProperties = ''
                            unFileNamePO         = ''
                            
                            if unExportAsJavaProperties:
                                unDirName  = "%s%s" % ( unNombreModulo, cZipPathSeparator,)
                                
                                # #####################
                                """Always include language code in the filename when exporting a backup.
                                
                                """
                                aCodigoIdiomaPorDefectoAUsar = ''
                                if not( theParametersInput.get( 'process_type', '') == cTRAProgress_ProcessType_Backup):
                                    aCodigoIdiomaPorDefectoAUsar = theDefaultLanguageCode
                                    
                                unFileNameProperties = "%s%s%s%s" % ( unDirName, cFilenamePropertiesBase, self.fPropertiesFilenameIdiomaPostfix( unCodigoIdioma, aCodigoIdiomaPorDefectoAUsar), cPropertiesFilePostfix,)
                                unInformeExportarModulo[ 'filename_properties'] = unFileNameProperties
                                unInformeExportarModulo[ 'filename']            = unFileNameProperties
                                 
                            if unExportAsGNUgettextPO:
                                unFileNamePO = "%s%s%s%s" % ( unNombreModulo,  cPOFileCharBeforeLanguage, unCodigoIdioma, cPOFilePostfix, )
                                unInformeExportarModulo[ 'filename_po'] = unFileNamePO
                                unInformeExportarModulo[ 'filename']    = unFileNamePO
                            
                            unosSimbolosCadenasEnModulo = self.fListaSimbolosCadenasOrdenadosEnModulo( unNombreModulo, unExecutionRecord)
                            unInformeExportarModulo[ 'translations_exported'] =  len( unosSimbolosCadenasEnModulo)
                            unInformeExportarIdioma[ 'translations_exported'] += len( unosSimbolosCadenasEnModulo)
                                
                   
                        if ( theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]) and ( unInformeExportarIdioma.get( 'num_encoding_errors', 0) > 0):
                            break
        
                        if theIncluirModuloNoEspecificado:
                            # ##############################################################################
                            """Export the strings for which no module has been specified .
                            
                            """
                            unInformeExportarModulo = self.fNewVoidInformeExportarTraduccionesDeModulo()
                            unInformeExportarModulo[ 'language_code'] = unCodigoIdioma
                            unInformeExportarModulo[ 'module_name']   = cNombreModuloNoEspecificadoInputValue
                            unInformeExportarIdioma[ 'modules_export_reports'].append( unInformeExportarModulo)
                            
                            unFileNameProperties = ''
                            unFileNamePO         = ''
                            
                            if unExportAsJavaProperties:
                                
                                # #####################
                                """Always include language code in the filename when exporting a backup.
                                
                                """
                                aCodigoIdiomaPorDefectoAUsar = ''
                                if not( theParametersInput.get( 'process_type', '') == cTRAProgress_ProcessType_Backup):
                                    aCodigoIdiomaPorDefectoAUsar = theDefaultLanguageCode
                                    
                                unDirName  = "%s%s" % ( theDefaultModuleName, cZipPathSeparator,)
                                unFileNameProperties = "%s%s%s%s" % ( unDirName, cFilenamePropertiesBase, self.fPropertiesFilenameIdiomaPostfix( unCodigoIdioma, aCodigoIdiomaPorDefectoAUsar), cPropertiesFilePostfix,)
                                unInformeExportarModulo[ 'filename_properties'] = unFileNameProperties
                                unInformeExportarModulo[ 'filename']            = unFileNameProperties
                                 
                            if unExportAsGNUgettextPO:
                                unFileNamePO = "%s%s%s%s" % ( theDefaultModuleName,  cPOFileCharBeforeLanguage, unCodigoIdioma, cPOFilePostfix, )
                                unInformeExportarModulo[ 'filename_po'] = unFileNamePO
                                unInformeExportarModulo[ 'filename']    = unFileNamePO

                            unosSimbolosCadenasEnModuloNoEspecificado = self.fListaSimbolosCadenasOrdenadosModuloNoEspecificado( unExecutionRecord)
                            unInformeExportarModulo[ 'translations_exported'] =  len( unosSimbolosCadenasEnModuloNoEspecificado)
                            unInformeExportarIdioma[ 'translations_exported'] += len( unosSimbolosCadenasEnModuloNoEspecificado)
                                
                                        
                        if ( theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]) and ( unInformeExportarIdioma.get( 'num_encoding_errors', 0) > 0):
                            break
                                
                        
                        
                        
                        
                        
                    else: # not unSeparatedModules
                        # ##############################################################################
                        """Export translations into the language in a single file with the strings in all modules and the not-specified module if requested.
                        
                        """
                        unInformeExportarIdioma[ 'separate_modules'] = False
        
                        unFileNameProperties = ''
                        unFileNamePO         = ''
                        
                        if unExportAsJavaProperties:
                            
                            # #####################
                            """Always include language code in the filename when exporting a backup.
                            
                            """
                            aCodigoIdiomaPorDefectoAUsar = ''
                            if not( theParametersInput.get( 'process_type', '') == cTRAProgress_ProcessType_Backup):
                                aCodigoIdiomaPorDefectoAUsar = theDefaultLanguageCode
                            
                            unFileNameProperties = "%s%s%s" % ( cFilenamePropertiesBase, self.fPropertiesFilenameIdiomaPostfix( unCodigoIdioma, aCodigoIdiomaPorDefectoAUsar), cPropertiesFilePostfix,)
                            unInformeExportarIdioma[ 'filename_properties'] = unFileNameProperties
                            unInformeExportarIdioma[ 'filename']            = unFileNameProperties
                             
                        if unExportAsGNUgettextPO:
                            unFileNamePO = "%s%s%s%s" % ( cPONoSeparateModulesFileNamePrefix,  cPOFileCharBeforeLanguage, unCodigoIdioma, cPOFilePostfix, )
                            unInformeExportarIdioma[ 'filename_po'] = unFileNamePO
                            unInformeExportarIdioma[ 'filename']    = unFileNamePO
        
        
                        unosSimbolosCadenasEnModulos = self.fListaSimbolosCadenasEnVariosModulosStrictly( unosNombresModulosOrdenados, theIncluirModuloNoEspecificado, unExecutionRecord)
                        unInformeExportarIdioma[ 'translations_exported'] += len( unosSimbolosCadenasEnModulos)
                            
                  
                if theSpecificFilename:
                    unNombreArchivoDescarga = theSpecificFilename
                elif theFilenameForGvSIG:
                    unNombreArchivoDescarga = self.fNombreArchivoExportacion_ForGvSIG( sorted( theCodigosIdiomas)[ 0], theProductName, theProductVersion, theL10NVersion, theTipoArchivo)
                else:
                    unNombreArchivoDescarga = self.fNombreArchivoExportacion( [ unCodigoEIdioma[ 0] for unCodigoEIdioma in unosCodigosEIdiomasOrdenados], unosNombresModulosOrdenados, theIncluirModuloNoEspecificado, theTipoArchivo)
                
                unInforme[ 'download_filename'] = unNombreArchivoDescarga
                
                
                if unHayError and ( theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError, cTRAEncodingErrorHandleMode_CountAllErrorsAndCancel]):
                    return unInforme
                                
                    
                unInforme.update( {
                    'success':              True,
                })
                return unInforme
    
            except:
                    
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fExportarTraducciones\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   

                unInforme.update( {
                    'success':              False,
                    'status':               cExportStatus_Exception,
                    'exception':            unInformeExcepcion,
                })
                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                    
                return unInforme                 
    
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
                      
   
            
            
            
            
    security.declarePrivate( 'fNombreArchivoExportacion_ForGvSIG')    
    def fNombreArchivoExportacion_ForGvSIG( self, theCodigoIdioma, theProductName, theProductVersion, theL10NVersion, theTipoArchivo):
        
        unArchivePostfix = theTipoArchivo
        if not ( unArchivePostfix in cOutputFilePostfixes):
            unArchivePostfix = cZipFilePostfix    

        unNombreArchivoExportacion = '%s_%s-language-v%s-%s%s' % ( 
            theProductName,
            theProductVersion,
            theL10NVersion,
            theCodigoIdioma,
            unArchivePostfix
        )

        return unNombreArchivoExportacion
        
        
        
    
    security.declarePrivate( 'fNombreArchivoExportacion')    
    def fNombreArchivoExportacion( self, theCodigosIdioma, theNombresModulos, theIncluirModuloNoEspecificado, theTipoArchivo):
        if not theIncluirModuloNoEspecificado:
            return self.fNombreArchivoExportacion_ConNombresModulos( theCodigosIdioma, theNombresModulos, theIncluirModuloNoEspecificado, theTipoArchivo)
            
        todosModulos = self.fObtenerTodosModulos()
        unExportarTodosModulos = True
        for unModulo in todosModulos:
            unNombreModulo = unModulo.Title()
            if not ( unNombreModulo in theNombresModulos):
                unExportarTodosModulos = False
                break
        if not unExportarTodosModulos:
            return self.fNombreArchivoExportacion_ConNombresModulos( theCodigosIdioma, theNombresModulos, theIncluirModuloNoEspecificado, theTipoArchivo)
        
        return self.fNombreArchivoExportacion_ConNombresModulos( theCodigosIdioma, [ 'AllModules',], False, theTipoArchivo)
    
    
    
    security.declarePrivate( 'fNombreArchivoExportacion_ConNombresModulos')    
    def fNombreArchivoExportacion_ConNombresModulos( self, theCodigosIdioma, theNombresModulos, theIncluirModuloNoEspecificado, theTipoArchivo):

        unosCodigosIdiomasNombreArchivo = cOutputFileNameLanguageSeparator.join( theCodigosIdioma)
        if len( unosCodigosIdiomasNombreArchivo) > cMaxLenIdiomasOutputFileName:
            unosCodigosIdiomasNombreArchivo = '%s%s%s' % (unosCodigosIdiomasNombreArchivo[ 0:cMaxLenIdiomasOutputFileName], cOutputFileNameModuleSeparator, cOutputFileNameModuleSeparator, )
            
        unMaxLen = 0
        if not theNombresModulos:
            unMaxLen = len( cNombreModuloNoEspecificadoInputValue)
        else:
            unMaxLen = max( len( cNombreModuloNoEspecificadoInputValue), max( [ len( unNombreModulo) for unNombreModulo in theNombresModulos]))

        unLastNombresModulosNombreArchivo = ''
        while True:
            unosNombresModulosParaNombreArchivo = []
            for unNombreModulo in theNombresModulos:
                unShortenedNombreModulo = unNombreModulo[:unMaxLen]
                if unShortenedNombreModulo:
                    unosNombresModulosParaNombreArchivo.append( unShortenedNombreModulo)
    
            if theIncluirModuloNoEspecificado:
                unShortenedNombreModulo = cNombreModuloNoEspecificadoInputValue[:unMaxLen]
                if unShortenedNombreModulo:
                    unosNombresModulosParaNombreArchivo.append( unShortenedNombreModulo)
            
            unosNombresModulosNombreArchivo = cOutputFileNameModuleSeparator.join( unosNombresModulosParaNombreArchivo)
            if unosNombresModulosNombreArchivo:
                unLastNombresModulosNombreArchivo = unosNombresModulosNombreArchivo
                if len( unosNombresModulosNombreArchivo) > cMaxLenModulosOutputFileName:
                    unMaxLen -= 1
                else:
                    break
            else:
                break
                

        if len( unLastNombresModulosNombreArchivo) > cMaxLenModulosOutputFileName:
            unLastNombresModulosNombreArchivo = '%s%s%s' % ( unLastNombresModulosNombreArchivo[ 0:cMaxLenModulosOutputFileName], cOutputFileNameModuleSeparator, cOutputFileNameModuleSeparator, )
        
        unArchivePostfix = theTipoArchivo
        if not ( unArchivePostfix in cOutputFilePostfixes):
            unArchivePostfix = cZipFilePostfix    
  
        unNow = self.fDateTimeNow()
        unTimestamp = '%4.4d%02d%02d%02d%02d%02d' % ( unNow.year(), unNow.month(), unNow.day(), unNow.hour(), unNow.minute(), unNow.second())    
        
        unNombreProducto = self.getNombreProducto()
        if not unNombreProducto:
            unNombreProducto = ''
            
        unNombreArchivoExportacion = '%s%s%s%s%s%s%s%s%s%s' % ( cExportZipFileNamePrefix, cOutputFileNameProduct_Separator, unNombreProducto, cOutputFileNameLanguageSeparator, unosCodigosIdiomasNombreArchivo, cOutputFileNameModuleSeparator, unLastNombresModulosNombreArchivo, cOutputFileNameModuleSeparator, unTimestamp, unArchivePostfix)
        
        return unNombreArchivoExportacion
    
    
    
    
    
    
    security.declarePrivate( 'pWriteManifestEntriesForIdioma')    
    def pWriteManifestEntriesForIdioma( self, 
        theBuffer, 
        theCodigoIdioma, 
        theWriteEntry, 
        theWriteReferenceEntry, 
        theWriteJavaProperties, 
        theFileNameProperties, 
        theWriteGNUgettextPO, 
        theFileNamePO):

        if not theCodigoIdioma:
            return self
        
        if not ( theWriteEntry or theWriteReferenceEntry):
            return self
        
        unLanguage, unCountry, unaVariation = self.fLanguageAndCountryAndVariationIdioma( theCodigoIdioma)
        
        if theWriteEntry:
                       
            if theWriteJavaProperties:
                if unCountry:
                    theBuffer.write("\n%s %s\n%s %s\n%s %s\n" % ( cManifestEntryStartLinePrefix, theFileNameProperties, cManifestLocaleCountryStartLinePrefix,            unCountry, cManifestLocaleLanguageStartLinePrefix, unLanguage, ) )   
                else:
                    theBuffer.write("\n%s %s\n%s %s\n"        % ( cManifestEntryStartLinePrefix, theFileNameProperties, cManifestLocaleLanguageStartLinePrefix,           unLanguage, ) )   
        
            if theWriteGNUgettextPO:
                if unCountry:
                    theBuffer.write("\n%s %s\n%s %s\n%s %s\n"  % ( cManifestEntryStartLinePrefix, theFileNamePO,        cManifestLocaleCountryStartLinePrefix,            unCountry, cManifestLocaleLanguageStartLinePrefix, unLanguage, ) )   
                else:
                    theBuffer.write("\n%s %s\n%s %s\n"         % ( cManifestEntryStartLinePrefix, theFileNamePO,        cManifestLocaleLanguageStartLinePrefix,           unLanguage, ) )   
        
        if theWriteReferenceEntry:
            
            if theWriteJavaProperties:                            
                if unCountry:
                    theBuffer.write("\n%s %s\n%s %s\n%s %s\n" % ( cManifestEntryStartLinePrefix, theFileNameProperties, cManifestReferenceLocaleCountryStartLinePrefix,   unCountry, cManifestReferenceLocaleLanguageStartLinePrefix, unLanguage, ) )   
                else:
                    theBuffer.write("\n%s %s\n%s %s\n"        % ( cManifestEntryStartLinePrefix, theFileNameProperties, cManifestReferenceLocaleLanguageStartLinePrefix,  unLanguage, ) )   
        
            if theWriteGNUgettextPO:                               
                if unCountry:
                    theBuffer.write("\n%s %s\n%s %s\n%s %s\n" % ( cManifestEntryStartLinePrefix, theFileNamePO,        cManifestReferenceLocaleCountryStartLinePrefix,    unCountry, cManifestReferenceLocaleLanguageStartLinePrefix, unLanguage, ) )   
                else:
                    theBuffer.write("\n%s %s\n%s %s\n"        % ( cManifestEntryStartLinePrefix, theFileNamePO,        cManifestReferenceLocaleLanguageStartLinePrefix,   unLanguage, ) )   
     
        return self
    

    
    

    

    
    security.declarePrivate( 'pWriteLocalesCSVEntriesForIdioma')    
    def pWriteLocalesCSVEntriesForIdioma( self, 
        theBuffer, 
        theCodigoIdioma, 
        theWriteEntry, 
        theWriteReferenceEntry, 
        theWriteJavaProperties, 
        theFileNameProperties, 
        theWriteGNUgettextPO, 
        theFileNamePO):

        if not theCodigoIdioma:
            return self
        
        if not ( theWriteEntry or theWriteReferenceEntry):
            return self

        unLanguage, unCountry, unaVariation = self.fLanguageAndCountryAndVariationIdioma( theCodigoIdioma)
        
        if theWriteEntry:
                       
            if theWriteJavaProperties:
                theBuffer.write("%s,%s,%s,%s,false\n"     % ( theFileNameProperties, unLanguage,unCountry, unaVariation) )   
       
            if theWriteGNUgettextPO:
                theBuffer.write("%s,%s,%s,%s,false\n"     % ( theFileNamePO,         unLanguage,unCountry, unaVariation) )   
          
                
        if theWriteReferenceEntry:
            
            if theWriteJavaProperties:
                theBuffer.write("%s,%s,%s,%s,true\n"      % ( theFileNameProperties, unLanguage,unCountry, unaVariation) )   
       
            if theWriteGNUgettextPO:
                theBuffer.write("%s,%s,%s,%s,true\n"      % ( theFileNamePO,         unLanguage,unCountry, unaVariation) )   
     
        return self
    

    
    
    
    
    
    
    
    
    
    
    
    # ####################################################
    """Retrieval methods.
    
    """

    
    security.declarePrivate( 'fResultadosTraduccionesExportacionIdiomaReferencia')    
    def fResultadosTraduccionesExportacionIdiomaReferencia( self, theCodigoIdiomaReferencia, theResultadosTraducciones, theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fResultadosTraduccionesExportacionIdiomaReferencia', theParentExecutionRecord, False, None, 'language:%s ' % theCodigoIdiomaReferencia) 
        try:
            if not theCodigoIdiomaReferencia or not theResultadosTraducciones:
                return []
            
            unosSimbolosCadenas = [ unResultado[ 'getSimbolo'] for unResultado in theResultadosTraducciones]
             
            if not unosSimbolosCadenas:
                return []
            
            aCatalog = self.fCatalogFiltroTraduccionesParaIdiomaPorCodigo( theCodigoIdiomaReferencia) 
            if not aCatalog:
                return []
            
            unaBusqueda = { 
                'getCodigoIdiomaEnGvSIG' :  theCodigoIdiomaReferencia,  
                'getSimbolo':               unosSimbolosCadenas,
                'sort_on':                  'getSimbolo',  
                'sort_order':               'ascending',            
            }
            unosResultadosBusquedaTraducciones      = aCatalog.searchResults(**unaBusqueda)
        
            return unosResultadosBusquedaTraducciones
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
                      
        
    
    
  
    security.declarePrivate( 'fResultadosTraduccionesExportacionIdiomaModulo')    
    def fResultadosTraduccionesExportacionIdiomaModulo( self, theIdioma, theNombreModulo, theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fResultadosTraduccionesExportacionIdiomaModulo', theParentExecutionRecord, False, None, 'language:%s    module: %s' % ( theIdioma.getCodigoIdiomaEnGvSIG(), theNombreModulo,)) 
        try:
            
            if not theIdioma or not theNombreModulo:
                return []
            
            unosSimbolosCadenasEnModulo = self.fListaSimbolosCadenasOrdenadosEnModulo( theNombreModulo, theParentExecutionRecord)
             
            if not unosSimbolosCadenasEnModulo:
                return[]
            
            aCatalog = self.fCatalogFiltroTraduccionesParaIdioma( theIdioma) 
            if ( aCatalog == None):
                return []
            
            unaBusqueda = { 
                'getCodigoIdiomaEnGvSIG' :  theIdioma.getCodigoIdiomaEnGvSIG(),  
                'getSimbolo':               unosSimbolosCadenasEnModulo,
                'sort_on':                  'getSimbolo',  
                'sort_order':               'ascending',            
            }
            unosResultadosBusquedaTraducciones      = aCatalog.searchResults(**unaBusqueda)
            return unosResultadosBusquedaTraducciones
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
                      
           
    
    
    
   
    security.declarePrivate( 'fResultadosTraduccionesExportacionIdiomaModuloNoEspecificado')    
    def fResultadosTraduccionesExportacionIdiomaModuloNoEspecificado( self, theIdioma, theParentExecutionRecord=None):
            
        unExecutionRecord = self.fStartExecution( 'method',  'fResultadosTraduccionesExportacionIdiomaModuloNoEspecificado', theParentExecutionRecord, False, None, 'language:%s' % theIdioma.getCodigoIdiomaEnGvSIG())
        try:
            if not theIdioma:
                return []
                    
            unosSimbolosCadenasEnModulo = self.fListaSimbolosCadenasOrdenadosModuloNoEspecificado( theParentExecutionRecord)
             
            if not unosSimbolosCadenasEnModulo:
                return []
            
            aCatalog = self.fCatalogFiltroTraduccionesParaIdioma( theIdioma) 
            if ( aCatalog == None):
                return []
            
            unaBusqueda = { 
                'getSimbolo':               unosSimbolosCadenasEnModulo,
                'sort_on':                  'getSimbolo',  
                'sort_order':               'ascending',            
            }
            unosResultadosBusquedaTraducciones      = aCatalog.searchResults(**unaBusqueda)
            return unosResultadosBusquedaTraducciones
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
         
       
    
            
            


    security.declarePrivate( 'fResultadosTraduccionesExportacionIdiomaAlgunosModulos')    
    def fResultadosTraduccionesExportacionIdiomaAlgunosModulos( self, 
        theIdioma,   
        theNombresModulosOrdenados,
        theIncluirModuloNoEspecificado,
        theParentExecutionRecord):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fResultadosTraduccionesExportacionIdiomaAlgunosModulos', theParentExecutionRecord, False, None, 'language: %s    modules: %s    include_unspecified_module: %s' % ( theIdioma.getCodigoIdiomaEnGvSIG(), ' '.join( theNombresModulosOrdenados), str( (theIncluirModuloNoEspecificado and True) or False)))

        try:
            if not theIdioma:
                return []
            
            unosSimbolosCadenasEnModulos = self.fListaSimbolosCadenasEnVariosModulosStrictly( theNombresModulosOrdenados, theIncluirModuloNoEspecificado, theParentExecutionRecord)
            if not unosSimbolosCadenasEnModulos:
                return []
                        
            aCatalog = self.fCatalogFiltroTraduccionesParaIdioma( theIdioma) 
            if ( aCatalog == None):
                return []
            
            unaBusqueda = { 
                'getSimbolo':               unosSimbolosCadenasEnModulos,
                'sort_on':                  'getSimbolo',  
                'sort_order':               'ascending',            
            }
            unosResultadosBusquedaTraducciones      = aCatalog.searchResults(**unaBusqueda)
            return unosResultadosBusquedaTraducciones
    
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
         
   
    
            
            
        
    security.declarePrivate( 'fResultadosTraduccionesExportacionIdiomaTodosModulos')    
    def fResultadosTraduccionesExportacionIdiomaTodosModulos( self, 
        theIdioma, 
        theParentExecutionRecord):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fResultadosTraduccionesExportacionIdiomaTodosModulos', theParentExecutionRecord, False, None, 'language:%s' % theIdioma.getCodigoIdiomaEnGvSIG())

        try:
            if not theIdioma:
                return []
                        
            aCatalog = self.fCatalogFiltroTraduccionesParaIdioma( theIdioma) 
            if ( aCatalog == None):
                return []
            
            unaBusqueda = { 
                'sort_on':                  'getSimbolo',  
                'sort_order':               'ascending',            
            }
            unosResultadosBusquedaTraducciones      = aCatalog.searchResults(**unaBusqueda)
            return unosResultadosBusquedaTraducciones
    
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
         
   
            
            
            
            
            
            
            
            
            
    
    # ####################################################
    """Encoding methods.
    
    """            
   
    
    security.declarePrivate( 'fFromSystemEncodingToUnicodeToUTF8')    
    def fFromSystemEncodingToUnicodeToUTF8( self, theString, theTranslationService, theSystemToUnicodeErrorsMode,  theUnicodeToUTF8ErrorsMode):
        
        if not theTranslationService:
            return ( '', cResultCondition_Internal_MissingParameter,)
        
        if not theString:
            return ( '', '',)
        
             
        unStringUnicode  = ''
        try:
            unStringUnicode = theTranslationService.asunicodetype( theString, errors=theSystemToUnicodeErrorsMode)
        except:
            return ( '', cResultCondition_Encoding_FailureFromSystemToUnicode,)
        
        unStringUTF8 = ''
        try:
            unStringUTF8 = theTranslationService.encode( unStringUnicode, cTRAEncodingUTF8, errors=theUnicodeToUTF8ErrorsMode)
        except:
            return ( '', cResultCondition_Encoding_FailureFromUnicodeToUTF8,)

        return ( unStringUTF8, '')

                
    
        
    
    security.declarePrivate( 'fFromSystemEncodingToUnicodeEscape')    
    def fFromSystemEncodingToUnicodeEscape( self, theString, theTranslationService, theSystemToUnicodeErrorsMode,):
        
        if not theTranslationService:
            return ( '', cResultCondition_Internal_MissingParameter,)
        
        if not theString:
            return ( '', '',)
        
             
        unStringUnicode  = ''
        try:
            unStringUnicode = theTranslationService.asunicodetype( theString, errors=theSystemToUnicodeErrorsMode)
        except:
            return ( '', cResultCondition_Encoding_FailureFromSystemToUnicode,)
        
        unStringEscaped = ''
        
        for unUnicodeChar in unStringUnicode:
            unCharOrdinal = ord( unUnicodeChar)
            
            if unCharOrdinal <= cMaxUnescapedCharOrdinal:
                unStringEscaped += chr( unCharOrdinal)
            else:
                unCharEscaped = '\\u'
                # ACV 20091004 Unicode escape at least 4 digits, not just two
                #if unCharOrdinal < 256:
                    #unCharEscaped += '%02x' % unCharOrdinal
                #elif unCharOrdinal < (256 * 256):
                if unCharOrdinal < (256 * 256):
                    unCharEscaped += '%04x' % unCharOrdinal
                elif unCharOrdinal < (256 * 256 * 256):
                    unCharEscaped += '%06x' % unCharOrdinal
                elif unCharOrdinal < (256 * 256 * 256 * 256):
                    unCharEscaped += '%08x' % unCharOrdinal
                else:
                    return ( unStringEscaped ,cResultCondition_Encoding_FailureFromSystemToUnicodeEscape,)
                
                unStringEscaped += unCharEscaped        
                
        return ( unStringEscaped, '')
    
    
    
    

     
            
            
            
    security.declarePrivate( 'fEncodedFileErrorsMode')    
    def fEncodedFileErrorsMode( self, theEncodingErrorHandleMode):  
        return cEncodedFileErrorsModeByEncodingErrorHandleMode.get( theEncodingErrorHandleMode, cDefaultEncodedFileErrorsMode)
    
        
        
            
    security.declarePrivate( 'fSystemToUnicodeErrorsMode')    
    def fSystemToUnicodeErrorsMode( self, theEncodingErrorHandleMode):  
        return cSystemToUnicodeErrorsModeByEncodingErrorHandleMode.get( theEncodingErrorHandleMode, cDefaultSystemToUnicodeErrorsMode)
    
        
            
    security.declarePrivate( 'fUnicodeToUTF8ErrorsMode')    
    def fUnicodeToUTF8ErrorsMode( self, theEncodingErrorHandleMode):  
        return cUnicodeToUTF8ErrorsModeByEncodingErrorHandleMode.get( theEncodingErrorHandleMode, cDefaultUnicodeToUTF8ErrorsMode)
    

    
    
    
    
    
    
    
    

 
    # ####################################################
    """Exported file storage and retrieval methods.
    
    """            
   
    
  
    security.declarePrivate( 'fStoreExportedFile')    
    def fStoreExportedFile( self, theFileName, theFileContent):
        """Store export contents as a file system file at the pre-configured path.
            
        """
        
        if not theFileName:
            return [ '', '',]
        
        # ###################################################
        """Make sure that exported files store folder exists.
            
        """
        aExportedFilesPath = self.fExportedFilesDiskPath()
                            
        aExportedFilesPathExist = False
        try:
            aExportedFilesPathExist = os.path.exists( aExportedFilesPath)
        except:
            None
        if not aExportedFilesPathExist:
            try:
                os.makedirs( aExportedFilesPath)
            except:
                None
            try:
                aExportedFilesPathExist = os.path.exists( aExportedFilesPath)
            except:
                None
            if not aExportedFilesPathExist:
                return [ '', '',]

            
        # ###################################################
        """Make sure that exported files store folder for the root translations catalog exists in the exported files store folder.
            
        """
        unRootElementUID = self.UID()
        
        aRootUIDPath = os.path.join( aExportedFilesPath, unRootElementUID)
        aRootUIDPathExist = False
        try:
            aRootUIDPathExist = os.path.exists( aRootUIDPath)
        except:
            None
        if not aRootUIDPathExist:
            try:
                os.mkdir( aRootUIDPath, cTRAExportedFiles_FolderCreateMode_RootUID)
            except:
                None
            try:
                aRootUIDPathExist = os.path.exists( aRootUIDPath)
            except:
                None
            if not aRootUIDPathExist:
                return [ '', '',]
                    

        
            
            
        # ###########################################################
        """Write the exported content on disk file into the exported files store folder for the root translations catalog.
            
        """
        aStoreFilePath      = os.path.join( aRootUIDPath, theFileName)

        aWritten = False
        try:
            aStoreFile  = None
            try:
                aStoreFile = open( aStoreFilePath, cTRAExportedFiles_FileOpenWriteMode, cTRAExportedFiles_FileOpenWriteBuffering)
                aStoreFile.write( theFileContent)
            finally:
                if aStoreFile:
                    aStoreFile.close()
            aWritten = True
        except IOError:
            None
  
        if not aWritten:
            return [ '', '',]
        
        return [ aStoreFilePath, theFileName, ]
    
        
    
    
    
    
    security.declareProtected( permissions.View, 'fExportedFilesDiskPath')
    def fExportedFilesDiskPath( self, ):
        """Path to store and retrieve export contents in the file system.
            
        """
        aConfiguration = getConfiguration()
        if not aConfiguration:
            return ''
        
        aClientHome = aConfiguration.clienthome
        if not aClientHome:
            return ''
            
        aExportedFilesDiskPath   = os.path.join( aClientHome, cTRAExportedFilesFolderName)
        return aExportedFilesDiskPath
    
    
    
    
    
    
    security.declareProtected( permissions.View, 'fExportedFileContents')
    def fExportedFileContents( self, theFileName,):
        """Retrieve the export contents  Stored as a file system file at the pre-configured path.
            
        """
        
        if not theFileName:
            return None
        
        # ###################################################
        """Make sure that exported files store folder exists.
            
        """
        aExportedFilesPath = self.fExportedFilesDiskPath()
                            
        aExportedFilesPathExist = False
        try:
            aExportedFilesPathExist = os.path.exists( aExportedFilesPath)
        except:
            None
        if not aExportedFilesPathExist:
            return None

            
        # ###################################################
        """Make sure that exported files store folder for the root translations catalog exists in the exported files store folder.
            
        """
        unRootElementUID = self.UID()
        
        aRootUIDPath = os.path.join( aExportedFilesPath, unRootElementUID)
        aRootUIDPathExist = False
        try:
            aRootUIDPathExist = os.path.exists( aRootUIDPath)
        except:
            None
        if not aRootUIDPathExist:
            return None
                   

        
            
            
        # ###########################################################
        """Read the exported content from a disk file in the exported files store folder for the root translations catalog.
            
        """
        aStoreFilePath      = os.path.join( aRootUIDPath, theFileName)

        aRead = False
        aFileContent = None
        try:
            aStoreFile  = None
            try:
                aStoreFile = open( aStoreFilePath, cTRAExportedFiles_FileOpenReadMode, cTRAExportedFiles_FileOpenReadBuffering)
                aFileContent = aStoreFile.read( )
            finally:
                if aStoreFile:
                    aStoreFile.close()
            aRead = True
        except IOError:
            None
  
        if not aRead:
            return None
        
        return aFileContent
    
            
    
    
    

 
    
    
    
    
    
    
    
    
    
    
    
    
    
    

 
    # ####################################################
    """Factory methods foro long-lived export processes.
    
    """            
       
    
    
    security.declareProtected( permissions.View, 'fCreateProgressHandlerFor_Backup')
    def fCreateProgressHandlerFor_Backup( self, 
        theAdditionalParams      =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Request creation of a Backup long-lived process control handler, to be executed later.
        
        """

         
        unExecutionRecord = self.fStartExecution( 'method',  'fCreateProgressHandlerFor_Backup', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }, ) 
        
        aThereWasException = False
        
        try:
  
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
                
            aResult = self.fNewVoidCreateProgressHandlerResult()
            
            try:
                
                aBackupResult = self.fNewVoidProgressResult_Export()
                
                aProgressElement = None
                aProgressHandler = None
           
                unCatalogoRaiz = self
                
                unaColeccionProgresos = unCatalogoRaiz.fObtenerColeccionProgresos()
                if unaColeccionProgresos == None:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_internal_Missing_progresses_collection', "Internal error: missing progresses collection-."),
                    })
                    return aResult
    
                
                unosIdiomas = unCatalogoRaiz.fObtenerTodosIdiomas()
                if not unosIdiomas:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_no_languages_to_backup', "There are no languages to export. You can not backup without any languages. Backup canceller-."),
                    })
                
                unosCodigosIdiomas = [ unIdioma.getCodigoIdiomaEnGvSIG() for unIdioma in unosIdiomas]
    
                
                unosModulos = unCatalogoRaiz.fObtenerTodosModulos()
                unosNombresModulos = [ unModulo.Title() for unModulo in unosModulos]
                unosNombresModulos.append( cModuloNoEspecificado_ValorNombre)
    
    
                
                unMemberId = self.fGetMemberId()
                unaFechaYHora = self.fDateTimeNowTextual()                  
                
                aMetaType = 'UnknownType'
                try:
                    aMetaType = self.meta_type
                except:
                    aMetaType = self.__class__.__name
                if not aMetaType:
                    aMetaType = 'UnknownType'
                
                aStartDateTimeNowTextual                 = unaFechaYHora
                aBackupResult[ 'process_type']           = cTRAProgress_ProcessType_Backup
                aBackupResult[ 'start_date_time_string'] = aStartDateTimeNowTextual
                aBackupResult[ 'date_time_now_string']   = aStartDateTimeNowTextual
                
                aBackupResult[ 'TRACatalogo_title']      = unCatalogoRaiz.Title()
                aBackupResult[ 'TRACatalogo_path' ]      = unCatalogoRaiz.fPathDelRaiz()
                aBackupResult[ 'TRACatalogo_UID' ]       = unCatalogoRaiz.UID()
                                
                aBackupResult[ 'element_type']           = aMetaType
                aBackupResult[ 'element_title']          = self.Title()
                aBackupResult[ 'element_path' ]          = self.fPhysicalPathString()
                aBackupResult[ 'element_UID' ]           = self.UID()
                
                aBackupResult[ 'last_element_type']      = ''
                aBackupResult[ 'last_element_title']     = ''
                aBackupResult[ 'last_element_path']      = ''
                aBackupResult[ 'last_element_UID']       = ''
                
                aMemberId = self.fGetMemberId()
                aBackupResult[ 'member_id'] = aMemberId
                
                    
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_Backup_TRACatalogo, 
                    theElementsBindings     = { cBoundObject: self,},
                    theRulesToCollect       = [ ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord
                )
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_no_permission_ToBackup', "You do not have permission to Backup-."),
                    })
                    return aResult
                
                aUseCaseAssessmentResultsCache = {
                    cUseCase_Backup_TRACatalogo: unUseCaseQueryResult,
                }
                                
                unaConfiguracion = self.fObtenerConfiguracion( cTRAConfiguracionAspecto_Backup)
                if unaConfiguracion == None:
                    aResult.update( {
                        'success':     False,
                        'condition':   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_internal_Missing_Backup_configuration', "Internal error: Backup configuration missing-."),
                    })
                    return aResult
                
                unaConfigurationDict = unaConfiguracion.fConfigurationDict()
                
                
                someConfiguracionMetaAndValues = unaConfiguracion.fConfigurationMetaAndValues( )
                
                someConfiguracionMetaAndValuesDict = { }
                for aMetaAndValue in someConfiguracionMetaAndValues:
                    if len( aMetaAndValue) > 1:
                        anAttributeName  = aMetaAndValue[ 0]
                        if anAttributeName:
                            someConfiguracionMetaAndValuesDict[ anAttributeName] = aMetaAndValue
            
                 
                unInformeIdiomasYModulos = self.fInformeTitulosIdiomasConIdiomaReferenciaYModulosPermitidos( 
                    theUseCaseName           =cUseCase_Backup_TRACatalogo, 
                    thePermissionsCache      =unPermissionsCache, 
                    theRolesCache            =unRolesCache, 
                    theParentExecutionRecord =unExecutionRecord,
                )
                if unInformeIdiomasYModulos:
                    if unInformeIdiomasYModulos.has_key( 'use_case_query_results'):
                        unInformeIdiomasYModulos.pop( 'use_case_query_results')
         
                unNombreProducto = unCatalogoRaiz.getNombreProducto()
                if not unNombreProducto:
                    unNombreProducto = ''
                                                    
                someInputParameters = {
                    'process_type'                    : cTRAProgress_ProcessType_Backup,
                    'informe_idiomas_y_modulos'       : unInformeIdiomasYModulos,
                    
                    'theLanguagesToExport'            : unosCodigosIdiomas,
                    'theCodigosIdiomaReferencia'      : {}, # No reference language
                    'theCodificacionesCaracteres'     : dict( [ ( unCodigo, cTRAEncodingUnicodeEscape,) for unCodigo in unosCodigosIdiomas]), 
                    'theModulesToExport'              : unosNombresModulos,
                    'theExportFormat'                 : unaConfigurationDict.get( 'formatoExportacionPorDefecto', cExportFormatOption_JavaProperties),
                    'theExportFormat_vocabulary'      : someConfiguracionMetaAndValuesDict.get( 'formatoExportacionPorDefecto', [ '',] * 9)[ 7],
                    'theExportFormat_vocabulary_msgids': someConfiguracionMetaAndValuesDict.get( 'formatoExportacionPorDefecto', [ '',] * 9)[ 8],
                    'theIncludeManifest'              : unaConfigurationDict.get( 'incluirManifestPorDefecto', cTRABooleanNo),
                    'theIncludeManifest_vocabulary'   : cTRABooleanVocabulary,
                    'theIncludeManifest_vocabulary_msgids': cTRABooleanVocabulary_msgids,
                    'theIncludeLocalesCSV'            : unaConfigurationDict.get( 'incluirLocalesCSVPorDefecto', cTRABooleanSi),
                    'theIncludeLocalesCSV_vocabulary' : cTRABooleanVocabulary,
                    'theIncludeLocalesCSV_vocabulary_msgids' : cTRABooleanVocabulary_msgids,
                    'theSeparatedModules'             : unaConfigurationDict.get( 'modulosPorSeparadoPorDefecto', cTRABooleanNo),
                    'theSeparatedModules_vocabulary'  : cTRABooleanVocabulary,
                    'theSeparatedModules_vocabulary_msgids'  : cTRABooleanVocabulary_msgids,
                    'theExportModuleNames'            : unaConfigurationDict.get( 'exportarNombresModulosPorDefecto', cTRABooleanSi),
                    'theExportModuleNames_vocabulary' : cTRABooleanVocabulary,
                    'theExportModuleNames_vocabulary_msgids' : cTRABooleanVocabulary_msgids,
                    'theExportContributions'            : unaConfigurationDict.get( 'exportarContribucionesPorDefecto', cTRABooleanSi),
                    'theExportContributions_vocabulary' : cTRABooleanVocabulary,
                    'theExportContributions_vocabulary_msgids' : cTRABooleanVocabulary_msgids,
                    'theExportStringSources'          : unaConfigurationDict.get( 'exportarFuentesPorDefecto', cTRABooleanSi),
                    'theExportStringSources_vocabulary': cTRABooleanVocabulary,
                    'theExportStringSources_vocabulary_msgids': cTRABooleanVocabulary_msgids,
                    'theExportTranslationsStatus'     : unaConfigurationDict.get( 'exportarEstadoTraduccionesPorDefecto', cTRABooleanSi),
                    'theExportTranslationsStatus_vocabulary' : cTRABooleanVocabulary,
                    'theExportTranslationsStatus_vocabulary_msgids' : cTRABooleanVocabulary_msgids,
                    'theTipoArchivo'                  : unaConfigurationDict.get( 'tipoArchivoExportacionPorDefecto', cZipFilePostfix),
                    'theTipoArchivo_vocabulary':        someConfiguracionMetaAndValuesDict.get( 'tipoArchivoExportacionPorDefecto', [ '',] * 9)[ 7],
                    'theTipoArchivo_vocabulary_msgids': someConfiguracionMetaAndValuesDict.get( 'tipoArchivoExportacionPorDefecto', [ '',] * 9)[ 8],
                    'theEncodingErrorHandleMode'      : unaConfigurationDict.get( 'modoGestionErrorCodificacionExportacionPorDefecto', cTRAEncodingErrorHandleMode_BackslashReplaceAndContinue),
                    'theEncodingErrorHandleMode_vocabulary': someConfiguracionMetaAndValuesDict.get( 'modoGestionErrorCodificacionExportacionPorDefecto', [ '',] * 9)[ 7],
                    'theEncodingErrorHandleMode_vocabulary_msgids': someConfiguracionMetaAndValuesDict.get( 'modoGestionErrorCodificacionExportacionPorDefecto', [ '',] * 9)[ 8],
                    'theFilenameForGvSIG'             : cTRABooleanNo,
                    'theFilenameForGvSIG_vocabulary'  : cTRABooleanVocabulary,
                    'theFilenameForGvSIG_vocabulary_msgids'  : cTRABooleanVocabulary_msgids,
                    'theDefaultLanguageCode'          : unaConfigurationDict.get( 'codigoIdiomaPorDefecto', ''),
                    'theDefaultModuleName'            : '',
                    'theDefaultDomain'                : unaConfigurationDict.get( 'dominioPorDefecto', ''),
                    'theProductName'                  : unNombreProducto,
                    'theProductVersion'               : '',
                    'theL10NVersion'                  : '',
                    'theSpecificFilename'             : '%s%s%s%s%s%s%s.zip' % ( cExportBackupFileNamePrefix, cExportBackupFileNameSeparator, unNombreProducto, cExportBackupFileNameSeparator, unaFechaYHora.replace( ' ', '_').replace( ':', '-'), cExportBackupFileNameSeparator, unMemberId),
                    'theConfiguration'                : unaConfigurationDict,
                    
                    'theExportarTRACatalogo':         cTRABooleanSi,
                    'theExportarTRACatalogo_vocabulary': cTRABooleanVocabulary,
                    'theExportarTRACatalogo_vocabulary_msgids': cTRABooleanVocabulary_msgids,
                    
                    'theExportarTRAConfiguraciones':         cTRABooleanSi,
                    'theExportarTRAConfiguraciones_vocabulary': cTRABooleanVocabulary,
                    'theExportarTRAConfiguraciones_vocabulary_msgids': cTRABooleanVocabulary_msgids,
                    
                    'theExportarTRAParametrosControlProgreso':         cTRABooleanSi,
                    'theExportarTRAParametrosControlProgreso_vocabulary': cTRABooleanVocabulary,
                    'theExportarTRAParametrosControlProgreso_vocabulary_msgids': cTRABooleanVocabulary_msgids,
                    
                    'theExportarTRAIdiomas':         cTRABooleanSi,
                    'theExportarTRAIdiomas_vocabulary': cTRABooleanVocabulary,
                    'theExportarTRAIdiomas_vocabulary_msgids': cTRABooleanVocabulary_msgids,
                    
                    'theExportarTRASolicitudesCadenas':         cTRABooleanSi,
                    'theExportarTRASolicitudesCadenas_vocabulary': cTRABooleanVocabulary,
                    'theExportarTRASolicitudesCadenas_vocabulary_msgids': cTRABooleanVocabulary_msgids,
                    
                    'theExportarTRAModulos':         cTRABooleanSi,
                    'theExportarTRAModulos_vocabulary': cTRABooleanVocabulary,
                    'theExportarTRAModulos_vocabulary_msgids': cTRABooleanVocabulary_msgids,
                    
                    'theExportarTRAInformes':         cTRABooleanSi,
                    'theExportarTRAInformes_vocabulary': cTRABooleanVocabulary,
                    'theExportarTRAInformes_vocabulary_msgids': cTRABooleanVocabulary_msgids,
                    
                    
                }
                
                                

                anExportEstimationResult = self.fEstimarContenidoExportacion(
                    theParametersInput               = someInputParameters,
                    thePermissionsCache              = unPermissionsCache,
                    theRolesCache                    = unRolesCache,
                    theUseCaseAssessmentResultsCache = aUseCaseAssessmentResultsCache,
                    theParentExecutionRecord         = unExecutionRecord,
                )                
                
                                      
                someInputParameters.update( {
                    'export_estimation_result'        : anExportEstimationResult,   
                })
                
                
                
                
                
                
                
                
                aProgressHandlerCreationResult = unaColeccionProgresos.fCreateNewProgressAndHandlerForElement(  
                    theInitialElement       =self, 
                    theProcessType          =cTRAProgress_ProcessType_Backup, 
                    theInputParameters      =someInputParameters,
                    theTimestamp            =aStartDateTimeNowTextual,
                    theResult               =aBackupResult, 
                    theInitializeLambda     =fExportInitialize_lambda,
                    theElementLambda        =None, 
                    theLoopLambda           =fExportLoop_lambda,
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
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorProgressElementNotKnownByImportProcessElement', "Progress element is not known by progress handler-"),
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
                    unInformeExcepcion += 'Exception during fCreateProgressHandlerFor_Backup of element %s %s at %s\n'  % (  self.meta_type(), self.Title(), self.fPhysicalPathString())
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
                
                aBackupResult[ 'success'] = False
                aBackupResult[ 'exception_date_time_string'] = self.fDateTimeNowTextual()
                aBackupResultDump = ''
                try:
                    aBackupResultDump = self.fProgressResult_dump( aBackupResult)
                except:
                    None
                if aBackupResultDump:
                    unInformeExcepcion += aBackupResultDump
                
                aBackupResult[ 'exception_report'] = unInformeExcepcionWOResult

                
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
           
                
            
            
            
            
            
            
            
            
            
            
            
 

    security.declareProtected( permissions.View, 'fCreateProgressHandlerFor_ExportGvSIG')
    def fCreateProgressHandlerFor_ExportGvSIG( self, 
        theAdditionalParams      =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Request creation of a Export for gvSIG long-lived process control handler, to be executed later.
        
        """

         
        unExecutionRecord = self.fStartExecution( 'method',  'fCreateProgressHandlerFor_ExportGvSIG', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }, ) 
        
        aThereWasException = False
        
        try:
                
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
 
            aResult = self.fNewVoidCreateProgressHandlerResult()
            
            try:
                
                
                anExportResult = self.fNewVoidProgressResult_Export()
                               
                
                aProgressElement = None
                aProgressHandler = None
                
                
                unCatalogoRaiz = self
                
                unaColeccionProgresos = unCatalogoRaiz.fObtenerColeccionProgresos()
                if unaColeccionProgresos == None:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_internal_Missing_progresses_collection', "Internal error: missing progresses collection-."),
                    })
                    return aResult

                
                unCodigoIdioma = theAdditionalParams.get( 'theCodigoIdioma', '')
                if not unCodigoIdioma:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_Parameter_missing_Must_Specify_A_Language_To_Export_For_GvSIG', "Required Parameter missing. You Must Specify A Language To Export For GvSIG-."),
                    })
                    return aResult
                
                
                unIdiomaAExportar = self.fGetIdiomaPorCodigo( unCodigoIdioma)
                if unIdiomaAExportar == None:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_Parameter_The_Specified_Language_To_Export_For_GvSIG_Does_Not_exists', "Parameter Language Specified To Export For GvSIG Does Not Exists-."),
                    })
                    return aResult
                

                unMemberId = self.fGetMemberId()
                unaFechaYHora = self.fDateTimeNowTextual()     
                  
                unProductName  = theAdditionalParams.get( 'theProductName', '')
                if not unProductName:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_RequiredParameter_theProductName', "Required Parameter missing: you must specify  a Product Name-."),
                    })
                    return aResult
                
                unProductVersion  = theAdditionalParams.get( 'theProductVersion', '')
                if not unProductVersion:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_RequiredParameter_theProductVersion', "Required Parameter missing: you must specify  a Product Version-."),
                    })
                    return aResult
                
                unL10NVersion  = theAdditionalParams.get( 'theL10NVersion', '')
                if not unL10NVersion:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_RequiredParameter_theL10NVersion', "Required Parameter missing: you must specify  a Localization Version-."),
                    })
                    return aResult

                
                
                aMetaType = 'UnknownType'
                try:
                    aMetaType = unIdiomaAExportar.meta_type
                except:
                    aMetaType = unIdiomaAExportar.__class__.__name
                if not aMetaType:
                    aMetaType = 'UnknownType'
                
                aStartDateTimeNowTextual = self.fDateTimeNowTextual()
                anExportResult[ 'process_type']           = cTRAProgress_ProcessType_ExportGvSIG
                anExportResult[ 'start_date_time_string'] = aStartDateTimeNowTextual
                anExportResult[ 'date_time_now_string']   = aStartDateTimeNowTextual
                anExportResult[ 'element_type']           = aMetaType
                anExportResult[ 'element_title']          = unIdiomaAExportar.Title()
                anExportResult[ 'element_path' ]          = unIdiomaAExportar.fPhysicalPathString()
                anExportResult[ 'element_UID' ]           = unIdiomaAExportar.UID()
                anExportResult[ 'last_element_type']      = ''
                anExportResult[ 'last_element_title']     = ''
                anExportResult[ 'last_element_path']      = ''
                anExportResult[ 'last_element_UID']       = ''
                
                aMemberId = self.fGetMemberId()
                anExportResult[ 'member_id'] = aMemberId
                
                unCatalogoRaiz = self          
                anExportResult[ 'TRACatalogo_title']      = unCatalogoRaiz.Title()
                anExportResult[ 'TRACatalogo_path' ]      = unCatalogoRaiz.fPathDelRaiz()
                anExportResult[ 'TRACatalogo_UID' ]       = unCatalogoRaiz.UID()
                
                    
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_ExportGvSIG_TRAIdioma, 
                    theElementsBindings     = { cBoundObject: unIdiomaAExportar,},
                    theRulesToCollect       = [ ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord
                )
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_no_permission_ToExportForGvSIG', "You do not have permission to Export for GvSIG-."),
                    })
                    return aResult
                
                aUseCaseAssessmentResultsCache = {
                    cUseCase_ExportGvSIG_TRAIdioma: unUseCaseQueryResult,
                }
                
                
                unaConfiguracion = self.fObtenerConfiguracion( cTRAConfiguracionAspecto_ExportarParaGvSIG)
                if unaConfiguracion == None:
                    aResult.update( {
                        'success':     False,
                        'condition':   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_internal_Missing_ExportForGvSIG_configuration', "Internal error: Export for GvSIG configuration missing-."),
                    })
                    return aResult
                  
                
                
                unosModulesToExport = theAdditionalParams.get( 'theModulesToExport', [])[:]
                if not unosModulesToExport:
                    unosModulesToExport = [ unModulo.Title() for unModulo in unCatalogoRaiz.fObtenerTodosModulos()] + [ cModuloNoEspecificado_ValorNombre,]
 
                
                
                unosCodigosIdiomas           = [ unCodigoIdioma,]
                unCodigoIdiomaReferencia     = unIdiomaAExportar.getCodigoIdiomaReferencia()
                if not unCodigoIdiomaReferencia:
                    unCodigoIdiomaReferencia = cTRAReferenceLanguageCodesForLanguages.get( unCodigoIdioma, cTRADefaultReferenceLanguageCode)
                    
                unosCodigosIdiomasReferencia = { unCodigoIdioma : unCodigoIdiomaReferencia,}
                
                unosCodigosIdiomasYReferencia = unosCodigosIdiomas[:]
                unosCodigosIdiomasYReferencia.append( unCodigoIdiomaReferencia)
                            
                unaConfigurationDict = unaConfiguracion.fConfigurationDict()
                
                someConfiguracionMetaAndValues = unaConfiguracion.fConfigurationMetaAndValues( )
                
                someConfiguracionMetaAndValuesDict = { }
                for aMetaAndValue in someConfiguracionMetaAndValues:
                    if len( aMetaAndValue) > 1:
                        anAttributeName  = aMetaAndValue[ 0]
                        if anAttributeName:
                            someConfiguracionMetaAndValuesDict[ anAttributeName] = aMetaAndValue
            
                 
                unInformeIdiomasYModulos = self.fInformeTitulosIdiomasConIdiomaReferenciaYModulosPermitidos( 
                    theUseCaseName           =cUseCase_Export, 
                    thePermissionsCache      =unPermissionsCache, 
                    theRolesCache            =unRolesCache, 
                    theParentExecutionRecord =unExecutionRecord,
                )
                if unInformeIdiomasYModulos:
                    if unInformeIdiomasYModulos.has_key( 'use_case_query_results'):
                        unInformeIdiomasYModulos.pop( 'use_case_query_results')
         

                                    
                someInputParameters = {
                    'process_type'                    : cTRAProgress_ProcessType_ExportGvSIG,
                    'informe_idiomas_y_modulos'       : unInformeIdiomasYModulos,

                    'theLanguagesToExport'            : unosCodigosIdiomas,
                    'theCodigosIdiomaReferencia'      : unosCodigosIdiomasReferencia, # No reference language
                    'theCodificacionesCaracteres'     : dict( [ ( unCodigo, cTRAEncodingUnicodeEscape,) for unCodigo in unosCodigosIdiomasYReferencia]), 
                    'theModulesToExport'              : unosModulesToExport,
                    'theExportFormat'                 : unaConfigurationDict.get( 'formatoExportacionPorDefecto', cExportFormatOption_JavaProperties),
                    'theExportFormat_vocabulary'      : someConfiguracionMetaAndValuesDict.get( 'formatoExportacionPorDefecto', [ '',] * 9)[ 7],
                    'theExportFormat_vocabulary_msgids': someConfiguracionMetaAndValuesDict.get( 'formatoExportacionPorDefecto', [ '',] * 9)[ 8],
                    'theIncludeManifest'              : unaConfigurationDict.get( 'incluirManifestPorDefecto', cTRABooleanNo),
                    'theIncludeManifest_vocabulary'   : cTRABooleanVocabulary,
                    'theIncludeManifest_vocabulary_msgids'   : cTRABooleanVocabulary_msgids,
                    'theIncludeLocalesCSV'            : unaConfigurationDict.get( 'incluirLocalesCSVPorDefecto', cTRABooleanSi),
                    'theIncludeLocalesCSV_vocabulary' : cTRABooleanVocabulary,
                    'theIncludeLocalesCSV_vocabulary_msgids' : cTRABooleanVocabulary_msgids,
                    'theSeparatedModules'             : unaConfigurationDict.get( 'modulosPorSeparadoPorDefecto', cTRABooleanNo),
                    'theSeparatedModules_vocabulary'  : cTRABooleanVocabulary,
                    'theSeparatedModules_vocabulary_msgids'  : cTRABooleanVocabulary_msgids,
                    'theExportModuleNames'            : unaConfigurationDict.get( 'exportarNombresModulosPorDefecto', cTRABooleanSi),
                    'theExportModuleNames_vocabulary' : cTRABooleanVocabulary,
                    'theExportModuleNames_vocabulary_msgids' : cTRABooleanVocabulary_msgids,
                    'theExportContributions'            : theAdditionalParams.get( 'theExportContributions', cTRABooleanSi),
                    'theExportContributions_vocabulary' : cTRABooleanVocabulary,
                    'theExportContributions_vocabulary_msgids' : cTRABooleanVocabulary_msgids,
                    'theExportStringSources'          : unaConfigurationDict.get( 'exportarFuentesPorDefecto', cTRABooleanSi),
                    'theExportStringSources_vocabulary': cTRABooleanVocabulary,
                    'theExportStringSources_vocabulary_msgids': cTRABooleanVocabulary_msgids,
                    'theExportTranslationsStatus'     : unaConfigurationDict.get( 'exportarEstadoTraduccionesPorDefecto', cTRABooleanSi),
                    'theExportTranslationsStatus_vocabulary' : cTRABooleanVocabulary,
                    'theExportTranslationsStatus_vocabulary_msgids' : cTRABooleanVocabulary_msgids,
                    'theTipoArchivo'                  : unaConfigurationDict.get( 'tipoArchivoExportacionPorDefecto', cZipFilePostfix),
                    'theTipoArchivo_vocabulary':        someConfiguracionMetaAndValuesDict.get( 'tipoArchivoExportacionPorDefecto', [ '',] * 9)[ 7],
                    'theTipoArchivo_vocabulary_msgids': someConfiguracionMetaAndValuesDict.get( 'tipoArchivoExportacionPorDefecto', [ '',] * 9)[ 8],
                    'theEncodingErrorHandleMode'      : unaConfigurationDict.get( 'modoGestionErrorCodificacionExportacionPorDefecto', cTRAEncodingErrorHandleMode_BackslashReplaceAndContinue),
                    'theEncodingErrorHandleMode_vocabulary': someConfiguracionMetaAndValuesDict.get( 'modoGestionErrorCodificacionExportacionPorDefecto', [ '',] * 9)[ 7],
                    'theEncodingErrorHandleMode_vocabulary_msgids': someConfiguracionMetaAndValuesDict.get( 'modoGestionErrorCodificacionExportacionPorDefecto', [ '',] * 9)[ 8],
                    'theFilenameForGvSIG'             : cTRABooleanSi,
                    'theFilenameForGvSIG_vocabulary'  : cTRABooleanVocabulary,
                    'theFilenameForGvSIG_vocabulary_msgids'  : cTRABooleanVocabulary_msgids,
                    'theDefaultLanguageCode'          : unaConfigurationDict.get( 'codigoIdiomaPorDefecto', ''),
                    'theDefaultModuleName'            : '',
                    'theDefaultDomain'                : unaConfigurationDict.get( 'dominioPorDefecto', ''),
                    'theProductName'                  : unProductName,
                    'theProductVersion'               : unProductVersion,
                    'theL10NVersion'                  : unL10NVersion,
                    'theSpecificFilename'             : '',
                    'theConfiguration'                : unaConfigurationDict,
                    

                    'theExportarTRACatalogo':         cTRABooleanNo,
                    'theExportarTRACatalogo_vocabulary': cTRABooleanVocabulary,
                    'theExportarTRACatalogo_vocabulary_msgids': cTRABooleanVocabulary_msgids,
                    
                    'theExportarTRAConfiguraciones':         cTRABooleanNo,
                    'theExportarTRAConfiguraciones_vocabulary': cTRABooleanVocabulary,
                    'theExportarTRAConfiguraciones_vocabulary_msgids': cTRABooleanVocabulary_msgids,
                    
                    'theExportarTRAParametrosControlProgreso':         cTRABooleanNo,
                    'theExportarTRAParametrosControlProgreso_vocabulary': cTRABooleanVocabulary,
                    'theExportarTRAParametrosControlProgreso_vocabulary_msgids': cTRABooleanVocabulary_msgids,
                    
                    'theExportarTRAIdiomas':         cTRABooleanNo,
                    'theExportarTRAIdiomas_vocabulary': cTRABooleanVocabulary,
                    'theExportarTRAIdiomas_vocabulary_msgids': cTRABooleanVocabulary_msgids,
                    
                    'theExportarTRASolicitudesCadenas':         cTRABooleanNo,
                    'theExportarTRASolicitudesCadenas_vocabulary': cTRABooleanVocabulary,
                    'theExportarTRASolicitudesCadenas_vocabulary_msgids': cTRABooleanVocabulary_msgids,                    

                    'theExportarTRAModulos':         cTRABooleanNo,
                    'theExportarTRAModulos_vocabulary': cTRABooleanVocabulary,
                    'theExportarTRAModulos_vocabulary_msgids': cTRABooleanVocabulary_msgids,
                    
                    'theExportarTRAInformes':         cTRABooleanNo,
                    'theExportarTRAInformes_vocabulary': cTRABooleanVocabulary,
                    'theExportarTRAInformes_vocabulary_msgids': cTRABooleanVocabulary_msgids,
                    
                }
                
                
                anExportEstimationResult = self.fEstimarContenidoExportacion(
                    theParametersInput               = someInputParameters,
                    thePermissionsCache              = unPermissionsCache,
                    theRolesCache                    = unRolesCache,
                    theUseCaseAssessmentResultsCache = aUseCaseAssessmentResultsCache,
                    theParentExecutionRecord         = unExecutionRecord,
                )
                
                someInputParameters.update( {
                    'export_estimation_result'        : anExportEstimationResult,
                })
             
                
                aProgressHandlerCreationResult = unaColeccionProgresos.fCreateNewProgressAndHandlerForElement(  
                    theInitialElement       =unIdiomaAExportar, 
                    theProcessType          =cTRAProgress_ProcessType_ExportGvSIG, 
                    theInputParameters      =someInputParameters,
                    theTimestamp            =aStartDateTimeNowTextual,
                    theResult               =anExportResult, 
                    theInitializeLambda     =fExportInitialize_lambda,
                    theElementLambda        =None, 
                    theLoopLambda           =fExportLoop_lambda,
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
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorProgressElementNotKnownByImportProcessElement', "Progress element is not known by progress handler-"),
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
                    unInformeExcepcion += 'Exception during fCreateProgressHandlerFor_ExportGvSIG of element %s %s at %s\n'  % (  self.meta_type(), self.Title(), self.fPhysicalPathString())
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
                
                anExportResult[ 'success'] = False
                anExportResult[ 'exception_date_time_string'] = self.fDateTimeNowTextual()
                aExportGvSIGResultDump = ''
                try:
                    aExportGvSIGResultDump = self.fProgressResult_dump( anExportResult)
                except:
                    None
                if aExportGvSIGResultDump:
                    unInformeExcepcion += aExportGvSIGResultDump
                
                anExportResult[ 'exception_report'] = unInformeExcepcionWOResult

                
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
           
                
            
                    
            
            
            
            
            
            
            
    
            
            

 

    security.declareProtected( permissions.View, 'fCreateProgressHandlerFor_ExportGvSIG_All')
    def fCreateProgressHandlerFor_ExportGvSIG_All( self, 
        theAdditionalParams      =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Request creation of a Export for gvSIG long-lived process control handler, to be executed later.
        
        """

         
        unExecutionRecord = self.fStartExecution( 'method',  'fCreateProgressHandlerFor_ExportGvSIG', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }, ) 
        
        aThereWasException = False
        
        try:
                
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
 
            aResult = self.fNewVoidCreateProgressHandlerResult()
            
            try:
                
                
                anExportResult = self.fNewVoidProgressResult_Export()
                               
                
                aProgressElement = None
                aProgressHandler = None
                
                
                unCatalogoRaiz = self
                
                unaColeccionProgresos = unCatalogoRaiz.fObtenerColeccionProgresos()
                if unaColeccionProgresos == None:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_internal_Missing_progresses_collection', "Internal error: missing progresses collection-."),
                    })
                    return aResult

                

                

                unMemberId = self.fGetMemberId()
                unaFechaYHora = self.fDateTimeNowTextual()     
                  
                unProductName  = theAdditionalParams.get( 'theProductName', '')
                if not unProductName:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_RequiredParameter_theProductName', "Required Parameter missing: you must specify  a Product Name-."),
                    })
                    return aResult
                
                unProductVersion  = theAdditionalParams.get( 'theProductVersion', '')
                if not unProductVersion:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_RequiredParameter_theProductVersion', "Required Parameter missing: you must specify  a Product Version-."),
                    })
                    return aResult
                
                unL10NVersion  = theAdditionalParams.get( 'theL10NVersion', '')
                if not unL10NVersion:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_RequiredParameter_theL10NVersion', "Required Parameter missing: you must specify  a Localization Version-."),
                    })
                    return aResult

                
                
                aMetaType = 'UnknownType'
                try:
                    aMetaType = unCatalogoRaiz.meta_type
                except:
                    aMetaType = unCatalogoRaiz.__class__.__name
                if not aMetaType:
                    aMetaType = 'UnknownType'
                
                aStartDateTimeNowTextual = self.fDateTimeNowTextual()
                anExportResult[ 'process_type']           = cTRAProgress_ProcessType_ExportGvSIG
                anExportResult[ 'start_date_time_string'] = aStartDateTimeNowTextual
                anExportResult[ 'date_time_now_string']   = aStartDateTimeNowTextual
                anExportResult[ 'element_type']           = aMetaType
                anExportResult[ 'element_title']          = unCatalogoRaiz.Title()
                anExportResult[ 'element_path' ]          = unCatalogoRaiz.fPhysicalPathString()
                anExportResult[ 'element_UID' ]           = unCatalogoRaiz.UID()
                anExportResult[ 'last_element_type']      = ''
                anExportResult[ 'last_element_title']     = ''
                anExportResult[ 'last_element_path']      = ''
                anExportResult[ 'last_element_UID']       = ''
                
                aMemberId = self.fGetMemberId()
                anExportResult[ 'member_id'] = aMemberId
                
                unCatalogoRaiz = self          
                anExportResult[ 'TRACatalogo_title']      = unCatalogoRaiz.Title()
                anExportResult[ 'TRACatalogo_path' ]      = unCatalogoRaiz.fPathDelRaiz()
                anExportResult[ 'TRACatalogo_UID' ]       = unCatalogoRaiz.UID()
                
                    
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_ExportGvSIG_All_TRAIdioma, 
                    theElementsBindings     = { cBoundObject: unCatalogoRaiz,},
                    theRulesToCollect       = [ ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord
                )
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_no_permission_ToExportForGvSIG', "You do not have permission to Export for GvSIG-."),
                    })
                    return aResult
                
                aUseCaseAssessmentResultsCache = {
                    cUseCase_ExportGvSIG_TRAIdioma: unUseCaseQueryResult,
                }
                
                
  
                
                
                
                unaConfiguracion = self.fObtenerConfiguracion( cTRAConfiguracionAspecto_ExportarParaGvSIG)
                if unaConfiguracion == None:
                    aResult.update( {
                        'success':     False,
                        'condition':   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_internal_Missing_ExportForGvSIG_configuration', "Internal error: Export for GvSIG configuration missing-."),
                    })
                    return aResult
                  
                
                
                unosModulesToExport = theAdditionalParams.get( 'theModulesToExport', [])[:]
                if not unosModulesToExport:
                    unosModulesToExport = [ unModulo.Title() for unModulo in unCatalogoRaiz.fObtenerTodosModulos()] + [ cModuloNoEspecificado_ValorNombre,]
 
                
                unosIdiomasAccesibles = self.getCatalogo().fObtenerTodosIdiomas()
                if not unosIdiomasAccesibles:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_No_Available_Languages_To_Export_All_For_GvSIG', "There are no available Languages To Export All of them for GvSIG-."),
                    })
                    return aResult
                
                unosCodigosIdiomas            = [ ]
                unosCodigosIdiomasReferencia  = { }
                unosCodigosIdiomasYReferencia = [ ]
                
                for unIdioma in unosIdiomasAccesibles:
                    unCodigoIdioma =  unIdioma.getCodigoIdiomaEnGvSIG() 
                    if unCodigoIdioma:
                        unosCodigosIdiomas.append( unCodigoIdioma)
                        if not ( unCodigoIdioma in unosCodigosIdiomasYReferencia):
                            unosCodigosIdiomasYReferencia.append( unCodigoIdioma)
                        
                        unCodigoIdiomaReferencia     = unIdioma.getCodigoIdiomaReferencia()
                        if not unCodigoIdiomaReferencia:
                            unCodigoIdiomaReferencia = cTRAReferenceLanguageCodesForLanguages.get( unCodigoIdioma, cTRADefaultReferenceLanguageCode)
                        if unCodigoIdiomaReferencia:
                            unosCodigosIdiomasReferencia[ unCodigoIdioma] = unCodigoIdiomaReferencia
                            
                            if not ( unCodigoIdiomaReferencia in unosCodigosIdiomasYReferencia):
                                unosCodigosIdiomasYReferencia.append( unCodigoIdiomaReferencia)
                                
                

                unaConfigurationDict = unaConfiguracion.fConfigurationDict()
                
                someConfiguracionMetaAndValues = unaConfiguracion.fConfigurationMetaAndValues( )
                
                someConfiguracionMetaAndValuesDict = { }
                for aMetaAndValue in someConfiguracionMetaAndValues:
                    if len( aMetaAndValue) > 1:
                        anAttributeName  = aMetaAndValue[ 0]
                        if anAttributeName:
                            someConfiguracionMetaAndValuesDict[ anAttributeName] = aMetaAndValue
            
                 
                unInformeIdiomasYModulos = self.fInformeTitulosIdiomasConIdiomaReferenciaYModulosPermitidos( 
                    theUseCaseName           =cUseCase_Export, 
                    thePermissionsCache      =unPermissionsCache, 
                    theRolesCache            =unRolesCache, 
                    theParentExecutionRecord =unExecutionRecord,
                )
                if unInformeIdiomasYModulos:
                    if unInformeIdiomasYModulos.has_key( 'use_case_query_results'):
                        unInformeIdiomasYModulos.pop( 'use_case_query_results')
         

                                    
                someInputParameters = {
                    'process_type'                    : cTRAProgress_ProcessType_ExportGvSIG,
                    'informe_idiomas_y_modulos'       : unInformeIdiomasYModulos,

                    'theLanguagesToExport'            : unosCodigosIdiomas,
                    'theCodigosIdiomaReferencia'      : unosCodigosIdiomasReferencia, 
                    'theCodificacionesCaracteres'     : dict( [ ( unCodigo, cTRAEncodingUnicodeEscape,) for unCodigo in unosCodigosIdiomasYReferencia]), 
                    'theModulesToExport'              : unosModulesToExport,
                    'theExportFormat'                 : unaConfigurationDict.get( 'formatoExportacionPorDefecto', cExportFormatOption_JavaProperties),
                    'theExportFormat_vocabulary'      : someConfiguracionMetaAndValuesDict.get( 'formatoExportacionPorDefecto', [ '',] * 9)[ 7],
                    'theExportFormat_vocabulary_msgids': someConfiguracionMetaAndValuesDict.get( 'formatoExportacionPorDefecto', [ '',] * 9)[ 8],
                    'theIncludeManifest'              : unaConfigurationDict.get( 'incluirManifestPorDefecto', cTRABooleanNo),
                    'theIncludeManifest_vocabulary'   : cTRABooleanVocabulary,
                    'theIncludeManifest_vocabulary_msgids'   : cTRABooleanVocabulary_msgids,
                    'theIncludeLocalesCSV'            : unaConfigurationDict.get( 'incluirLocalesCSVPorDefecto', cTRABooleanSi),
                    'theIncludeLocalesCSV_vocabulary' : cTRABooleanVocabulary,
                    'theIncludeLocalesCSV_vocabulary_msgids' : cTRABooleanVocabulary_msgids,
                    'theSeparatedModules'             : unaConfigurationDict.get( 'modulosPorSeparadoPorDefecto', cTRABooleanNo),
                    'theSeparatedModules_vocabulary'  : cTRABooleanVocabulary,
                    'theSeparatedModules_vocabulary_msgids'  : cTRABooleanVocabulary_msgids,
                    'theExportModuleNames'            : unaConfigurationDict.get( 'exportarNombresModulosPorDefecto', cTRABooleanSi),
                    'theExportModuleNames_vocabulary' : cTRABooleanVocabulary,
                    'theExportModuleNames_vocabulary_msgids' : cTRABooleanVocabulary_msgids,
                    'theExportContributions'            : theAdditionalParams.get( 'theExportContributions', cTRABooleanSi),
                    'theExportContributions_vocabulary' : cTRABooleanVocabulary,
                    'theExportContributions_vocabulary_msgids' : cTRABooleanVocabulary_msgids,
                    'theExportStringSources'          : unaConfigurationDict.get( 'exportarFuentesPorDefecto', cTRABooleanSi),
                    'theExportStringSources_vocabulary': cTRABooleanVocabulary,
                    'theExportStringSources_vocabulary_msgids': cTRABooleanVocabulary_msgids,
                    'theExportTranslationsStatus'     : unaConfigurationDict.get( 'exportarEstadoTraduccionesPorDefecto', cTRABooleanSi),
                    'theExportTranslationsStatus_vocabulary' : cTRABooleanVocabulary,
                    'theExportTranslationsStatus_vocabulary_msgids' : cTRABooleanVocabulary_msgids,
                    'theTipoArchivo'                  : unaConfigurationDict.get( 'tipoArchivoExportacionPorDefecto', cZipFilePostfix),
                    'theTipoArchivo_vocabulary':        someConfiguracionMetaAndValuesDict.get( 'tipoArchivoExportacionPorDefecto', [ '',] * 9)[ 7],
                    'theTipoArchivo_vocabulary_msgids': someConfiguracionMetaAndValuesDict.get( 'tipoArchivoExportacionPorDefecto', [ '',] * 9)[ 8],
                    'theEncodingErrorHandleMode'      : unaConfigurationDict.get( 'modoGestionErrorCodificacionExportacionPorDefecto', cTRAEncodingErrorHandleMode_BackslashReplaceAndContinue),
                    'theEncodingErrorHandleMode_vocabulary': someConfiguracionMetaAndValuesDict.get( 'modoGestionErrorCodificacionExportacionPorDefecto', [ '',] * 9)[ 7],
                    'theEncodingErrorHandleMode_vocabulary_msgids': someConfiguracionMetaAndValuesDict.get( 'modoGestionErrorCodificacionExportacionPorDefecto', [ '',] * 9)[ 8],
                    'theFilenameForGvSIG'             : cTRABooleanSi,
                    'theFilenameForGvSIG_vocabulary'  : cTRABooleanVocabulary,
                    'theFilenameForGvSIG_vocabulary_msgids'  : cTRABooleanVocabulary_msgids,
                    'theDefaultLanguageCode'          : unaConfigurationDict.get( 'codigoIdiomaPorDefecto', ''),
                    'theDefaultModuleName'            : '',
                    'theDefaultDomain'                : unaConfigurationDict.get( 'dominioPorDefecto', ''),
                    'theProductName'                  : unProductName,
                    'theProductVersion'               : unProductVersion,
                    'theL10NVersion'                  : unL10NVersion,
                    'theSpecificFilename'             : '',
                    'theConfiguration'                : unaConfigurationDict,
                    

                    'theExportarTRACatalogo':         cTRABooleanNo,
                    'theExportarTRACatalogo_vocabulary': cTRABooleanVocabulary,
                    'theExportarTRACatalogo_vocabulary_msgids': cTRABooleanVocabulary_msgids,
                    
                    'theExportarTRAConfiguraciones':         cTRABooleanNo,
                    'theExportarTRAConfiguraciones_vocabulary': cTRABooleanVocabulary,
                    'theExportarTRAConfiguraciones_vocabulary_msgids': cTRABooleanVocabulary_msgids,
                    
                    'theExportarTRAParametrosControlProgreso':         cTRABooleanNo,
                    'theExportarTRAParametrosControlProgreso_vocabulary': cTRABooleanVocabulary,
                    'theExportarTRAParametrosControlProgreso_vocabulary_msgids': cTRABooleanVocabulary_msgids,
                    
                    'theExportarTRAIdiomas':         cTRABooleanNo,
                    'theExportarTRAIdiomas_vocabulary': cTRABooleanVocabulary,
                    'theExportarTRAIdiomas_vocabulary_msgids': cTRABooleanVocabulary_msgids,
                    
                    'theExportarTRASolicitudesCadenas':         cTRABooleanNo,
                    'theExportarTRASolicitudesCadenas_vocabulary': cTRABooleanVocabulary,
                    'theExportarTRASolicitudesCadenas_vocabulary_msgids': cTRABooleanVocabulary_msgids,                    

                    'theExportarTRAModulos':         cTRABooleanNo,
                    'theExportarTRAModulos_vocabulary': cTRABooleanVocabulary,
                    'theExportarTRAModulos_vocabulary_msgids': cTRABooleanVocabulary_msgids,
                    
                    'theExportarTRAInformes':         cTRABooleanNo,
                    'theExportarTRAInformes_vocabulary': cTRABooleanVocabulary,
                    'theExportarTRAInformes_vocabulary_msgids': cTRABooleanVocabulary_msgids,
                    
                }
                
                
                anExportEstimationResult = self.fEstimarContenidoExportacion(
                    theParametersInput               = someInputParameters,
                    thePermissionsCache              = unPermissionsCache,
                    theRolesCache                    = unRolesCache,
                    theUseCaseAssessmentResultsCache = aUseCaseAssessmentResultsCache,
                    theParentExecutionRecord         = unExecutionRecord,
                )
                
                someInputParameters.update( {
                    'export_estimation_result'        : anExportEstimationResult,
                })
             
                
                aProgressHandlerCreationResult = unaColeccionProgresos.fCreateNewProgressAndHandlerForElement(  
                    theInitialElement       =unCatalogoRaiz, 
                    theProcessType          =cTRAProgress_ProcessType_ExportGvSIG, 
                    theInputParameters      =someInputParameters,
                    theTimestamp            =aStartDateTimeNowTextual,
                    theResult               =anExportResult, 
                    theInitializeLambda     =fExportInitialize_lambda,
                    theElementLambda        =None, 
                    theLoopLambda           =fExportLoop_lambda,
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
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorProgressElementNotKnownByImportProcessElement', "Progress element is not known by progress handler-"),
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
                    unInformeExcepcion += 'Exception during fCreateProgressHandlerFor_ExportGvSIG of element %s %s at %s\n'  % (  self.meta_type(), self.Title(), self.fPhysicalPathString())
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
                
                anExportResult[ 'success'] = False
                anExportResult[ 'exception_date_time_string'] = self.fDateTimeNowTextual()
                aExportGvSIGResultDump = ''
                try:
                    aExportGvSIGResultDump = self.fProgressResult_dump( anExportResult)
                except:
                    None
                if aExportGvSIGResultDump:
                    unInformeExcepcion += aExportGvSIGResultDump
                
                anExportResult[ 'exception_report'] = unInformeExcepcionWOResult

                
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
           
                
            
                    
            
            
            
            
            
                        
            
            
            
            
 

    security.declareProtected( permissions.View, 'fCreateProgressHandlerFor_Export')
    def fCreateProgressHandlerFor_Export( self, 
        theAdditionalParams      =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Request creation of a Export long-lived process control handler, to be executed later.
        
        """

         
        unExecutionRecord = self.fStartExecution( 'method',  'fCreateProgressHandlerFor_Export', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }, ) 
        
        aThereWasException = False
        
        try:
            
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)

            aResult = self.fNewVoidCreateProgressHandlerResult()

            try:
                
                
                aExportResult = self.fNewVoidProgressResult_Export()
                            
                aProgressElement = None
                aProgressHandler = None   
                
                unCatalogoRaiz = self
                
                unaColeccionProgresos = unCatalogoRaiz.fObtenerColeccionProgresos()
                if unaColeccionProgresos == None:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_internal_Missing_progresses_collection', "Internal error: missing progresses collection-."),
                    })
                    return aResult
                
                
                aMemberId = self.fGetMemberId()
                aExportResult[ 'member_id'] = aMemberId
                
                aMetaType = 'UnknownType'
                try:
                    aMetaType = self.meta_type
                except:
                    aMetaType = self.__class__.__name
                if not aMetaType:
                    aMetaType = 'UnknownType'
                
                aStartDateTimeNowTextual = self.fDateTimeNowTextual()
                aExportResult[ 'process_type']           = cTRAProgress_ProcessType_Export
                aExportResult[ 'start_date_time_string'] = aStartDateTimeNowTextual
                aExportResult[ 'date_time_now_string']   = aStartDateTimeNowTextual
                aExportResult[ 'TRACatalogo_title']      = unCatalogoRaiz.Title()
                aExportResult[ 'TRACatalogo_path' ]      = unCatalogoRaiz.fPathDelRaiz()
                aExportResult[ 'TRACatalogo_UID' ]       = unCatalogoRaiz.UID()
                
                aExportResult[ 'element_type']           = aMetaType
                aExportResult[ 'element_title']          = self.Title()
                aExportResult[ 'element_path' ]          = self.fPhysicalPathString()
                aExportResult[ 'element_UID' ]           = self.UID()
                
                aExportResult[ 'last_element_type']      = ''
                aExportResult[ 'last_element_title']     = ''
                aExportResult[ 'last_element_path']      = ''
                aExportResult[ 'last_element_UID']       = ''
                
                    
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_Export, 
                    theElementsBindings     = { cBoundObject: self,},
                    theRulesToCollect       = [ ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord
                )
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    aResult.update( {
                        'success':     False,
                        'condition':   'gvSIGi18n_no_permission_ToExport',
                    })
                    return aResult
                
                aUseCaseAssessmentResultsCache = {
                    cUseCase_Export: unUseCaseQueryResult,
                }
                
                
                
                unaConfiguracion = self.fObtenerConfiguracion( cTRAConfiguracionAspecto_Exportacion)
                if unaConfiguracion == None:
                    aResult.update( {
                        'success':     False,
                        'condition':   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_internal_Missing_Export_configuration', "Internal error: Export configuration missing-."),
                    })
                    return aResult
                
                unaConfigurationDict = unaConfiguracion.fConfigurationDict()
                
                
                unosModulesToExport = theAdditionalParams.get( 'theModulesToExport', [])[:]
                if not unosModulesToExport:
                    unosModulesToExport = [ unModulo.Title() for unModulo in unCatalogoRaiz.fObtenerTodosModulos()] + [ cModuloNoEspecificado_ValorNombre,]
 
                unInformeIdiomasYModulos = theAdditionalParams.get( 'informe_idiomas_y_modulos', {})
                if unInformeIdiomasYModulos.has_key( 'use_case_query_results'):
                    unInformeIdiomasYModulos.pop( 'use_case_query_results')
                    
                someAdditionalParams = theAdditionalParams
                if not someAdditionalParams:
                    someAdditionalParams = { }
                someAdditionalParams[ 'process_type'] = cTRAProgress_ProcessType_Export
                    
                anExportEstimationResult = self.fEstimarContenidoExportacion(
                    theParametersInput               = someAdditionalParams,
                    thePermissionsCache              = unPermissionsCache,
                    theRolesCache                    = unRolesCache,
                    theUseCaseAssessmentResultsCache = aUseCaseAssessmentResultsCache,
                    theParentExecutionRecord         = unExecutionRecord,
                )
                                    
                someInputParameters = {
                    'process_type'                    : cTRAProgress_ProcessType_Export,
                    'informe_idiomas_y_modulos'       : unInformeIdiomasYModulos,
                    'export_estimation_result'        : anExportEstimationResult,
                    
                    'theLanguagesToExport'            : theAdditionalParams.get( 'theLanguagesToExport', [])[:],
                    'theCodigosIdiomaReferencia'      : theAdditionalParams.get( 'theCodigosIdiomaReferencia', {}).copy(),
                    'theCodificacionesCaracteres'     : theAdditionalParams.get( 'theCodificacionesCaracteres', {}).copy(),
                    'theModulesToExport'              : unosModulesToExport,
                    'theExportFormat'                 : theAdditionalParams.get( 'theExportFormat', cExportFormatOption_JavaProperties),
                    'theExportFormat_vocabulary'      : theAdditionalParams.get( 'theExportFormat_vocabulary', [])[:],
                    'theExportFormat_vocabulary_msgids'      : theAdditionalParams.get( 'theExportFormat_vocabulary_msgids', [])[:],
                    'theIncludeManifest'              : theAdditionalParams.get( 'theIncludeManifest', cTRABooleanNo),
                    'theIncludeManifest_vocabulary'   : theAdditionalParams.get( 'theIncludeManifest_vocabulary', [])[:],
                    'theIncludeManifest_vocabulary_msgids'   : theAdditionalParams.get( 'theIncludeManifest_vocabulary_msgids', [])[:],
                    'theIncludeLocalesCSV'            : theAdditionalParams.get( 'theIncludeLocalesCSV', cTRABooleanSi),
                    'theIncludeLocalesCSV_vocabulary' : theAdditionalParams.get( 'theIncludeLocalesCSV_vocabulary', [])[:],
                    'theIncludeLocalesCSV_vocabulary_msgids' : theAdditionalParams.get( 'theIncludeLocalesCSV_vocabulary_msgids', [])[:],
                    'theSeparatedModules'             : theAdditionalParams.get( 'theSeparatedModules', cTRABooleanNo),
                    'theSeparatedModules_vocabulary'  : theAdditionalParams.get( 'theSeparatedModules_vocabulary', [])[:],
                    'theSeparatedModules_vocabulary_msgids'  : theAdditionalParams.get( 'theSeparatedModules_vocabulary_msgids', [])[:],
                    'theExportModuleNames'            : theAdditionalParams.get( 'theExportModuleNames', cTRABooleanSi),
                    'theExportModuleNames_vocabulary' : theAdditionalParams.get( 'theExportModuleNames_vocabulary', [])[:],
                    'theExportModuleNames_vocabulary_msgids' : theAdditionalParams.get( 'theExportModuleNames_vocabulary_msgids', [])[:],
                    'theExportContributions'            : theAdditionalParams.get( 'theExportContributions', cTRABooleanSi),
                    'theExportContributions_vocabulary' : theAdditionalParams.get( 'theExportContributions_vocabulary', [])[:],
                    'theExportContributions_vocabulary_msgids' : theAdditionalParams.get( 'theExportContributions_vocabulary_msgids', [])[:],
                    'theExportStringSources'            : theAdditionalParams.get( 'theExportStringSources', cTRABooleanSi),
                    'theExportStringSources_vocabulary' : theAdditionalParams.get( 'theExportStringSources_vocabulary', [])[:],
                    'theExportStringSources_vocabulary_msgids' : theAdditionalParams.get( 'theExportStringSources_vocabulary_msgids', [])[:],
                    'theExportTranslationsStatus'            : theAdditionalParams.get( 'theExportTranslationsStatus', cTRABooleanSi),
                    'theExportTranslationsStatus_vocabulary' : theAdditionalParams.get( 'theExportTranslationsStatus_vocabulary', [])[:],
                    'theExportTranslationsStatus_vocabulary_msgids' : theAdditionalParams.get( 'theExportTranslationsStatus_vocabulary_msgids', [])[:],
                    'theTipoArchivo'                  : theAdditionalParams.get( 'theTipoArchivo', cZipFilePostfix),
                    'theTipoArchivo_vocabulary'         : theAdditionalParams.get( 'theTipoArchivo_vocabulary', [])[:],
                    'theTipoArchivo_vocabulary_msgids'  : theAdditionalParams.get( 'theTipoArchivo_vocabulary_msgids', [])[:],
                    'theDefaultLanguageCode'          : theAdditionalParams.get( 'theDefaultLanguageCode', cTRALanguageCode_English),
                    'theDefaultModuleName'            : theAdditionalParams.get( 'theDefaultModuleName', cTRAADefaultModuleName),
                    'theDefaultDomain'                : theAdditionalParams.get( 'theDefaultDomain', cTRAADefaultDomainName),
                    'theEncodingErrorHandleMode'      : theAdditionalParams.get( 'theEncodingErrorHandleMode', cTRAEncodingErrorHandleMode_BackslashReplaceAndContinue),
                    'theEncodingErrorHandleMode_vocabulary'         : theAdditionalParams.get( 'theEncodingErrorHandleMode_vocabulary', [])[:],
                    'theEncodingErrorHandleMode_vocabulary_msgids'  : theAdditionalParams.get( 'theEncodingErrorHandleMode_vocabulary_msgids', [])[:],
                    'theFilenameForGvSIG'             : theAdditionalParams.get( 'theFilenameForGvSIG', cTRABooleanNo),
                    'theFilenameForGvSIG_vocabulary'  : theAdditionalParams.get( 'theFilenameForGvSIG_vocabulary', [])[:],
                    'theFilenameForGvSIG_vocabulary_msgids'  : theAdditionalParams.get( 'theFilenameForGvSIG_vocabulary_msgids', [])[:],
                    'theProductName'                  : theAdditionalParams.get( 'theProductName', ''),
                    'theProductVersion'               : theAdditionalParams.get( 'theProductVersion', ''),
                    'theL10NVersion'                  : theAdditionalParams.get( 'theL10NVersion', ''),
                    'theSpecificFilename'             : theAdditionalParams.get( 'theSpecificFilename', ''),
                    'theConfiguration'                : unaConfigurationDict,
                    
                    
                    'theExportarTRACatalogo':         theAdditionalParams.get( 'theExportarTRACatalogo', cTRABooleanNo),
                    'theExportarTRACatalogo_vocabulary': theAdditionalParams.get( 'theExportarTRACatalogo_vocabulary', [])[:],
                    'theExportarTRACatalogo_vocabulary_msgids': theAdditionalParams.get( 'theExportarTRACatalogo_vocabulary_msgids', [])[:],
                    
                    'theExportarTRAConfiguraciones':         theAdditionalParams.get( 'theExportarTRAConfiguraciones', cTRABooleanNo),
                    'theExportarTRAConfiguraciones_vocabulary': theAdditionalParams.get( 'theExportarTRAConfiguraciones_vocabulary', [])[:],
                    'theExportarTRAConfiguraciones_vocabulary_msgids': theAdditionalParams.get( 'theExportarTRAConfiguraciones_vocabulary_msgids', [])[:],
                    
                    'theExportarTRAParametrosControlProgreso':         theAdditionalParams.get( 'theExportarTRAParametrosControlProgreso', cTRABooleanNo),
                    'theExportarTRAParametrosControlProgreso_vocabulary': theAdditionalParams.get( 'theExportarTRAParametrosControlProgreso_vocabulary', [])[:],
                    'theExportarTRAParametrosControlProgreso_vocabulary_msgids': theAdditionalParams.get( 'theExportarTRAParametrosControlProgreso_vocabulary_msgids', [])[:],
                    
                    'theExportarTRAIdiomas':         theAdditionalParams.get( 'theExportarTRAIdiomas', cTRABooleanNo),
                    'theExportarTRAIdiomas_vocabulary': theAdditionalParams.get( 'theExportarTRAIdiomas_vocabulary', [])[:],
                    'theExportarTRAIdiomas_vocabulary_msgids': theAdditionalParams.get( 'theExportarTRAIdiomas_vocabulary_msgids', [])[:],
                    
                    'theExportarTRASolicitudesCadenas':         theAdditionalParams.get( 'theExportarTRASolicitudesCadenas', cTRABooleanNo),
                    'theExportarTRASolicitudesCadenas_vocabulary': theAdditionalParams.get( 'theExportarTRASolicitudesCadenas_vocabulary', [])[:],
                    'theExportarTRASolicitudesCadenas_vocabulary_msgids': theAdditionalParams.get( 'theExportarTRASolicitudesCadenas_vocabulary_msgids', [])[:],
                    
                    'theExportarTRAModulos':         theAdditionalParams.get( 'theExportarTRAModulos', cTRABooleanNo),
                    'theExportarTRAModulos_vocabulary': theAdditionalParams.get( 'theExportarTRAModulos_vocabulary', [])[:],
                    'theExportarTRAModulos_vocabulary_msgids': theAdditionalParams.get( 'theExportarTRAModulos_vocabulary_msgids', [])[:],
                    
                    'theExportarTRAInformes':         theAdditionalParams.get( 'theExportarTRAInformes', cTRABooleanNo),
                    'theExportarTRAInformes_vocabulary': theAdditionalParams.get( 'theExportarTRAInformes_vocabulary', [])[:],
                    'theExportarTRAInformes_vocabulary_msgids': theAdditionalParams.get( 'theExportarTRAInformes_vocabulary_msgids', [])[:],
                    
                }
                
                

                
                
                aProgressHandlerCreationResult = unaColeccionProgresos.fCreateNewProgressAndHandlerForElement(  
                    theInitialElement       =self, 
                    theProcessType          =cTRAProgress_ProcessType_Export, 
                    theInputParameters      =someInputParameters,
                    theTimestamp            =aStartDateTimeNowTextual,
                    theResult               =aExportResult, 
                    theInitializeLambda     =fExportInitialize_lambda,
                    theElementLambda        =None, 
                    theLoopLambda           =fExportLoop_lambda,
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
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorProgressElementNotKnownByImportProcessElement', "Progress element is not known by progress handler-"),
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
                    unInformeExcepcion += 'Exception during fCreateProgressHandlerFor_Export of element %s %s at %s\n'  % (  self.meta_type(), self.Title(), self.fPhysicalPathString())
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
                
                aExportResult[ 'success'] = False
                aExportResult[ 'exception_date_time_string'] = self.fDateTimeNowTextual()
                aExportResultDump = ''
                try:
                    aExportResultDump = self.fProgressResult_dump( aExportResult)
                except:
                    None
                if aExportResultDump:
                    unInformeExcepcion += aExportResultDump
                
                aExportResult[ 'exception_report'] = unInformeExcepcionWOResult

                
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
           
                
            
                    
            
            
            
            
            
            
            
            
            
            
            
    
    ##/code-section class-header

    # Methods
# end of class TRACatalogo_Exportacion

##code-section module-footer #fill in your manual code here



     
            
 






        
def fExportInitialize_lambda( theContextualElement, theProcessControlManager, theAdditionalParmsHere):  

    if theContextualElement == None:
        return None
    
    if not theProcessControlManager:
        return None
    
    if not theProcessControlManager.vInputParameters:
        return None


    someExportParameters = theProcessControlManager.vInputParameters.copy()
        
    unosInitializedObjects = {
        'export_parameters': someExportParameters,
    }
                
    theProcessControlManager.pAddInitializedObjects( unosInitializedObjects)
    
    return None        
            
 


    
def fExportLoop_lambda( theInitialElement, theProcessControlManager, theAdditionalParmsHere):  
    
    if theInitialElement == None:
        return None
    
    unExecutionRecord = theInitialElement.fStartExecution( 'method',  'fExportLoop_lambda', None, False) 

    try:
    
        
        if not theProcessControlManager:
            return None
           
        if not theProcessControlManager.vInitializedObjects:
            return None
           
        if theProcessControlManager.vCatalogoRaiz == None:
            return None            
    

        
        
        someExportParameters = theProcessControlManager.vInitializedObjects.get( 'export_parameters', None)
        if someExportParameters == None:
            return None

        
        
       # ##############################################################################
        """Shall return a report including the relevant request parameters.
        
        """
        unInforme = theProcessControlManager.vCatalogoRaiz.fNewVoidInformeExportarTraducciones()            
        theProcessControlManager.vResult[ 'export_report'] = unInforme
        
        
        theCodigosIdiomas               = someExportParameters.get( 'theLanguagesToExport', [])
        theCodigosIdiomasReferencia     = someExportParameters.get( 'theCodigosIdiomaReferencia', {})
        theCodificacionesCaracteres     = someExportParameters.get( 'theCodificacionesCaracteres', {})
        theNombresModulos               = someExportParameters.get( 'theModulesToExport', [])
        theIncluirModuloNoEspecificado  = cModuloNoEspecificado_ValorNombre in theNombresModulos
        theExportFormat                 = someExportParameters.get( 'theExportFormat', '')
        theIncludeManifest              = someExportParameters.get( 'theIncludeManifest', '')            == ( someExportParameters.get( 'theIncludeManifest_vocabulary',  ['xXxXxXx',])[ 0])
        theIncludeLocalesCSV            = someExportParameters.get( 'theIncludeLocalesCSV', '')          == ( someExportParameters.get( 'theIncludeLocalesCSV_vocabulary',  ['xXxXxXx',])[ 0])
        theSeparatedModules             = someExportParameters.get( 'theSeparatedModules', '')           == ( someExportParameters.get( 'theSeparatedModules_vocabulary', ['xXxXxXx',])[ 0])
        theExportModuleNames            = someExportParameters.get( 'theExportModuleNames', '')          == ( someExportParameters.get( 'theExportModuleNames_vocabulary', ['xXxXxXx',])[ 0])
        theExportContributions          = someExportParameters.get( 'theExportContributions', '')        == ( someExportParameters.get( 'theExportContributions_vocabulary', ['xXxXxXx',])[ 0])
        theExportStringSources          = someExportParameters.get( 'theExportStringSources', '')        == ( someExportParameters.get( 'theExportStringSources_vocabulary', ['xXxXxXx',])[ 0])
        theExportTranslationsStatus     = someExportParameters.get( 'theExportTranslationsStatus', '')   == ( someExportParameters.get( 'theExportTranslationsStatus_vocabulary', ['xXxXxXx',])[ 0])
        theTipoArchivo                  = someExportParameters.get( 'theTipoArchivo', '')
        theDefaultLanguageCode          = someExportParameters.get( 'theDefaultLanguageCode', '')
        theDefaultModuleName            = someExportParameters.get( 'theDefaultModuleName', '')
        theDefaultDomain                = someExportParameters.get( 'theDefaultDomain', '')
        theEncodingErrorHandleMode      = someExportParameters.get( 'theEncodingErrorHandleMode', '')
        theFilenameForGvSIG             = someExportParameters.get( 'theFilenameForGvSIG', '')           == ( someExportParameters.get( 'theFilenameForGvSIG_vocabulary', ['xXxXxXx',])[ 0])
        theProductName                  = someExportParameters.get( 'theProductName', '')
        theProductVersion               = someExportParameters.get( 'theProductVersion', '')
        theL10NVersion                  = someExportParameters.get( 'theL10NVersion', '')
        theSpecificFilename             = someExportParameters.get( 'theSpecificFilename', '')
        
        theProcessType                  = someExportParameters.get( 'process_type', '')
        
        theExportarTRACatalogo                  = someExportParameters.get( 'theExportarTRACatalogo', )                    == ( someExportParameters.get( 'theExportarTRACatalogo_vocabulary',  ['xXxXxXx',])[ 0])
        theExportarTRAConfiguraciones           = someExportParameters.get( 'theExportarTRAConfiguraciones', '')           == ( someExportParameters.get( 'theExportarTRAConfiguraciones_vocabulary',  ['xXxXxXx',])[ 0])
        theExportarTRAParametrosControlProgreso = someExportParameters.get( 'theExportarTRAParametrosControlProgreso', '') == ( someExportParameters.get( 'theExportarTRAParametrosControlProgreso_vocabulary',  ['xXxXxXx',])[ 0])
        theExportarTRAIdiomas                   = someExportParameters.get( 'theExportarTRAIdiomas', '')                   == ( someExportParameters.get( 'theExportarTRAIdiomas_vocabulary',  ['xXxXxXx',])[ 0])
        theExportarTRAModulos                   = someExportParameters.get( 'theExportarTRAModulos', '')                   == ( someExportParameters.get( 'theExportarTRAModulos_vocabulary',  ['xXxXxXx',])[ 0])
        theExportarTRAInformes                  = someExportParameters.get( 'theExportarTRAInformes', '')                  == ( someExportParameters.get( 'theExportarTRAInformes_vocabulary',  ['xXxXxXx',])[ 0])
        theExportarTRASolicitudesCadenas        = someExportParameters.get( 'theExportarTRASolicitudesCadenas', '')        == ( someExportParameters.get( 'theExportarTRASolicitudesCadenas_vocabulary',  ['xXxXxXx',])[ 0])
        
 
        anExportXML = theExportarTRACatalogo or \
            theExportarTRAConfiguraciones or \
            theExportarTRAParametrosControlProgreso or \
            theExportarTRAIdiomas or \
            theExportarTRAModulos or \
            theExportarTRAInformes or \
            theExportarTRASolicitudesCadenas
               
        
        
        aModelDDvlPloneTool          = None
        someAllExportTypeConfigs     = []
        
        
        
        if anExportXML:

            aModelDDvlPloneTool = theProcessControlManager.vCatalogoRaiz.fModelDDvlPloneTool()
            if aModelDDvlPloneTool == None:        
                unInforme.update( {
                    'success':              False,
                    'status':               cExportStatus_NoModelDDvlPloneTool,
                })
                return None
                
            someAllExportTypeConfigs =  aModelDDvlPloneTool.fModelDDvlPloneTool_Retrieval( theProcessControlManager.vCatalogoRaiz).getAllTypeExportConfigs( theProcessControlManager.vCatalogoRaiz)        
            if not someAllExportTypeConfigs:
                theProcessControlManager.vResult[ 'success']   = False
                theProcessControlManager.vResult[ 'condition'] = cExportStatus_NoExportTypeConfigsForObject
                unInforme.update( {
                    'success':              False,
                    'status':               cExportStatus_NoExportTypeConfigsForObject,
                })
                return None                

            someExportTypeConfigsChosen = theProcessControlManager.vCatalogoRaiz.fExportTypeConfigsChosen( 
                theAllExportTypeConfigs                 =someAllExportTypeConfigs,
                theExportarTRACatalogo                  =theExportarTRACatalogo,
                theExportarTRAConfiguraciones           =theExportarTRAConfiguraciones,           
                theExportarTRAParametrosControlProgreso =theExportarTRAParametrosControlProgreso,
                theExportarTRAIdiomas                   =theExportarTRAIdiomas,                
                theExportarTRAModulos                   =theExportarTRAModulos,                  
                theExportarTRAInformes                  =theExportarTRAInformes,                  
                theExportarTRASolicitudesCadenas        =theExportarTRASolicitudesCadenas,
            )
            if not someExportTypeConfigsChosen:
                theProcessControlManager.vResult[ 'success']   = False
                theProcessControlManager.vResult[ 'condition'] = cExportStatus_NoExportTypeConfigsChosenForObject
                unInforme.update( {
                    'success':              False,
                    'status':               cExportStatus_NoExportTypeConfigsChosenForObject,
                })
                return None                
                                
            
            
    
        unInforme[ 'languages_requested'] = ( theCodigosIdiomas or [])[:]
        unInforme[ 'reference_languages'] = ( theCodigosIdiomasReferencia and theCodigosIdiomasReferencia.copy()) or {}
        unInforme[ 'modules_requested']   = ( theNombresModulos or [])[:]
        unInforme[ 'unspecified_module_requested'] = theIncluirModuloNoEspecificado
        
        #theProcessControlManager.vResult[ 'languages_requested']            = unInforme[ 'languages_requested'] 
        #theProcessControlManager.vResult[ 'reference_languages']            = unInforme[ 'reference_languages'] 
        #theProcessControlManager.vResult[ 'modules_requested']              = unInforme[ 'modules_requested'] 
        #theProcessControlManager.vResult[ 'unspecified_module_requested']   = unInforme[ 'unspecified_module_requested'] 
        
        # ##############################################################################
        """Cancel export if no languages requested.
        
        """
        if not theCodigosIdiomas:
            theProcessControlManager.vResult[ 'success']   = False
            theProcessControlManager.vResult[ 'condition'] = cExportStatus_NoLanguagesRequestedForExport
            unInforme.update( {
                'success':              False,
                'status':               cExportStatus_NoLanguagesRequestedForExport,
            })
            return None
        
        
                
        # ##############################################################################
        """Cancel export if no modules requested and not requested the strings with unspecified module.
        
        """
        if ( not theNombresModulos) and not theIncluirModuloNoEspecificado:
            theProcessControlManager.vResult[ 'success']   = False
            theProcessControlManager.vResult[ 'condition'] = cExportStatus_NoModulesRequestedForExport
            unInforme.update( {
                'success':              False,
                'status':               cExportStatus_NoModulesRequestedForExport,
            })
            return None
                
                 
        
        # ##############################################################################
        """Query for languages and modules accessible in the UseCase.
        
        """
        aUseCaseAssessmentResult = theProcessControlManager.vCatalogoRaiz.fUseCaseAssessment( 
            theUseCaseName          = cUseCase_Export, 
            theElementsBindings     = { cBoundObject: theProcessControlManager.vCatalogoRaiz,},
            theRulesToCollect       = [ 'languages', 'modules',], 
            thePermissionsCache     = { }, 
            theRolesCache           = { }, 
            theParentExecutionRecord= unExecutionRecord,
        )
        
        
        
        
        # ##############################################################################
        """Check the user is authorized to exercise the UseCase.
        
        """
        if not aUseCaseAssessmentResult or not aUseCaseAssessmentResult.get( 'success', False):
            theProcessControlManager.vResult[ 'success']   = False
            theProcessControlManager.vResult[ 'condition'] = cExportStatus_UseCaseAssessmentFailed
            unInforme.update( {
                'success':              False,
                'status':               cExportStatus_UseCaseAssessmentFailed,
                'condition':            cUseCase_Export,
            })
            return None
        
        
        
                    
    
        # ##############################################################################
        """Shall export as .properties and/or .PO, with .properties by default.
        
        """
        unArchiveType               = theTipoArchivo
        if not ( unArchiveType in cExportArchiveTypes):
            unArchiveType = cZipFilePostfix
        unInforme[ 'archive_type']    = unArchiveType
                    
        unExportAsJavaProperties   = theExportFormat  == cExportFormatOption_JavaProperties
        unExportAsGNUgettextPO     = theExportFormat  == cExportFormatOption_GNUgettextPO
        if ( not unExportAsJavaProperties) and (not unExportAsGNUgettextPO):
            unExportAsJavaProperties = True
        unInforme[ 'export_format']    = ( unExportAsGNUgettextPO and cExportFormatOption_GNUgettextPO) or cExportFormatOption_JavaProperties
            
        unIncludeManifest               = theIncludeManifest and True
        unInforme[ 'include_manifest']  = unIncludeManifest
        
        unIncludeLocalesCSV               = theIncludeLocalesCSV and True
        unInforme[ 'include_localescsv']  = unIncludeLocalesCSV
        
        unSeparatedModules              = theSeparatedModules and True           
        unInforme[ 'separate_modules']  = unSeparatedModules
    
        unExportModuleNames              = theExportModuleNames and True           
        unInforme[ 'export_module_names']= unExportModuleNames
    
        unExportContributions              = theExportContributions and True           
        unInforme[ 'export_contributions']= unExportContributions
    
        unExportStringSources              = theExportStringSources and True           
        unInforme[ 'export_string_sources']= unExportStringSources
    
        unExportTranslationsStatus       = theExportTranslationsStatus and True           
        unInforme[ 'export_translation_status']= unExportTranslationsStatus
        
             
        theProcessControlManager.vResult[ 'archive_type']                = unInforme[ 'archive_type'] 
        theProcessControlManager.vResult[ 'export_format']               = unInforme[ 'export_format'] 
        theProcessControlManager.vResult[ 'include_manifest']            = unInforme[ 'include_manifest'] 
        theProcessControlManager.vResult[ 'include_localescsv']          = unInforme[ 'include_localescsv'] 
        theProcessControlManager.vResult[ 'separate_modules']            = unInforme[ 'separate_modules'] 
        theProcessControlManager.vResult[ 'export_module_names']         = unInforme[ 'export_module_names'] 
        theProcessControlManager.vResult[ 'export_translation_status']   = unInforme[ 'export_translation_status'] 
        theProcessControlManager.vResult[ 'export_contributions']        = unInforme[ 'export_contributions'] 
        
            
        
        
        # ##############################################################################
        """Scan the list of languages requested by the user to export for translation and as reference. Do not consider languages that are not accessible for the user.
        
        """
        unosCodigosIdiomasReferencia = set( )
        for unCodigoIdioma in theCodigosIdiomas:
            unCodigoIdiomaReferencia = theCodigosIdiomasReferencia.get( unCodigoIdioma, '')
            if unCodigoIdiomaReferencia:
                unosCodigosIdiomasReferencia.add( unCodigoIdiomaReferencia)
          
        unosIdiomasVisibles = aUseCaseAssessmentResult.get( 'collected_rule_assessments_by_name', {}).get( 'languages', {}).get( 'accepted_final_objects', [])
         
        unosCodigosEIdiomasAExportar          = [ ]
        unosCodigosIdiomasAExportar           = set()
        unosCodigosIdiomasReferenciaAExportar = set()
        

        for unIdioma in unosIdiomasVisibles:
            unCodigoIdioma = unIdioma.getCodigoIdiomaEnGvSIG()
                                
            if unCodigoIdioma in theCodigosIdiomas:
                unosCodigosEIdiomasAExportar.append( [ unCodigoIdioma, unIdioma, ])
                unosCodigosIdiomasAExportar.add( unCodigoIdioma)
                
                
        for unIdioma in unosIdiomasVisibles:
            unCodigoIdioma = unIdioma.getCodigoIdiomaEnGvSIG()
            
            if ( unCodigoIdioma in unosCodigosIdiomasReferencia) and ( not( unCodigoIdioma in unosCodigosIdiomasAExportar)) and ( not ( unCodigoIdioma in unosCodigosIdiomasReferenciaAExportar)):
                unosCodigosIdiomasReferenciaAExportar.add( unCodigoIdioma)
                if unExportAsJavaProperties:
                    unosCodigosEIdiomasAExportar.append( [ unCodigoIdioma, unIdioma, ])
                                 
    
        unosCodigosEIdiomasOrdenados = sorted( unosCodigosEIdiomasAExportar, cmp=lambda uno, otro: cmp( uno[ 0], otro[ 0]))
                 
    
        
        
        # ##############################################################################
        """Cancel export if no languages allowed to export.
        
        """
        if not unosCodigosEIdiomasOrdenados:
            theProcessControlManager.vResult[ 'success']   = False
            theProcessControlManager.vResult[ 'condition'] = cExportStatus_NoAvailableLanguagesToExport
            unInforme.update( {
                'success':              False,
                'status':               cExportStatus_NoAvailableLanguagesToExport,
            })
            return None
         
        
         
    
        # ##############################################################################
        """Do not consider modules that are not accessible for the user.
        
        """
        unosModulosVisibles = aUseCaseAssessmentResult.get( 'collected_rule_assessments_by_name', {}).get( 'modules', {}).get( 'accepted_final_objects', [])
        
        unosNombresModulosAExportar = []
        for unModulo in unosModulosVisibles:
            unNombreModulo = unModulo.Title()
            if ( unNombreModulo in theNombresModulos) and not ( unNombreModulo in unosNombresModulosAExportar):
                unosNombresModulosAExportar.append( unNombreModulo)
                
        unosNombresModulosOrdenados  = sorted( unosNombresModulosAExportar)
        
        
        
        
                
        # ##############################################################################
        """Cancel export if no modules  allowed to export.
        
        """
        if ( not unosNombresModulosOrdenados) and not theIncluirModuloNoEspecificado:
            theProcessControlManager.vResult[ 'success']   = False
            theProcessControlManager.vResult[ 'condition'] = cExportStatus_NoAvailableModulesToExport
            unInforme.update( {
                'success':              False,
                'status':               cExportStatus_NoAvailableModulesToExport,
            })
            return None
                
        unInforme[ 'exported_module_names']        = unosNombresModulosOrdenados
        unInforme[ 'exported_unspecified_module']  = ( theIncluirModuloNoEspecificado and True) or False
            
    
        theProcessControlManager.vResult[ 'exported_module_names']       = unInforme[ 'exported_module_names'] 
        theProcessControlManager.vResult[ 'exported_unspecified_module'] = unInforme[ 'exported_unspecified_module'] 
        
        
        
        
        # ##############################################################################
        """Make sure requested character encodings are known, or default to utf-8.
        
        """
        unasCodificacionesCaracteres = { }
        
        for unCodigoIdioma, unIdioma in unosCodigosEIdiomasOrdenados:
            
            unaCodificacionIdioma = ''
            if unExportAsJavaProperties:
                unaCodificacionIdioma   = unIdioma.getJuegoDeCaracteresParaJavaProperties()
            else:
                unaCodificacionIdioma   = unIdioma.getJuegoDeCaracteresParaPO()
                
            unaCodificacionIdiomaParametro = theCodificacionesCaracteres.get( unCodigoIdioma, '')
                 
            if not unaCodificacionIdiomaParametro:
                unaCodificacionIdiomaParametro = unaCodificacionIdioma
                
            unCodecInfo = None
            try:
                unCodecInfo = CODECS_Lookup( unaCodificacionIdiomaParametro)
            except:
                None
            if unCodecInfo:
                unasCodificacionesCaracteres[ unCodigoIdioma] = unaCodificacionIdiomaParametro
            else:
                unasCodificacionesCaracteres[ unCodigoIdioma] = cTRAEncodingUTF8
             
    
        
        
        
        # ##############################################################################
        """Create in-memory zip file for exported content, to be sent back to the user in the HTTP request response.
        
        """
        unZipBuffer = None
        unZipFile   = None
        
        unZipBuffer      = StringIO()
        unZipFile        = None
        try:
            unZipFile = ZipFile( unZipBuffer, "w", compression=ZIP_DEFLATED)
        except:
            None
        if not unZipFile:
            unZipFile = ZipFile( unZipBuffer, "w", compression=ZIP_STORED)
            
        if not unZipFile:
            theProcessControlManager.vResult[ 'success']   = False
            theProcessControlManager.vResult[ 'condition'] = cExportStatus_CanNotCreateZipFile
            unInforme.update( {
                'success':              False,
                'status':               cExportStatus_CanNotCreateZipFile,
            })
            return None
        
        
        
        # ##############################################################################
        """Create in-memory buffer for the manifest file.
        
        """
        unManifestBuffer = None
        if unIncludeManifest:  
            unManifestBuffer = StringIO()
        
            
       
        # ##############################################################################
        """Create in-memory buffer for the locales csv file.
        
        """
        unLocalesCSVBuffer = None
        if unIncludeLocalesCSV:  
            unLocalesCSVBuffer = StringIO()
        
            
        # ##############################################################################
        """Export each requested and allowed language.
        
        """
        unCodigoUltimoIdioma                              = None
        unosResultadosTraduccionesUltimoIdioma            = None
        unoCodigoUltimoIdiomaReferencia                   = None
        unosResultadosTraduccionesUltimoIdiomaReferencia  = None
        
        
        
        
    
        # ##############################################################################
        """the Translation Service to use to convert to all encodings 
        
        """
        aTranslationService = theProcessControlManager.vCatalogoRaiz.getTranslationServiceTool()     
        
                
        
        
        # ##############################################################################
        """How to handle encoding errors.
        
        """
        anEncodedFileErrorsMode     = theProcessControlManager.vCatalogoRaiz.fEncodedFileErrorsMode(      theEncodingErrorHandleMode)
        aSystemToUnicodeErrorsMode  = theProcessControlManager.vCatalogoRaiz.fSystemToUnicodeErrorsMode(  theEncodingErrorHandleMode)
        aUnicodeToUTF8ErrorsMode    = theProcessControlManager.vCatalogoRaiz.fUnicodeToUTF8ErrorsMode(    theEncodingErrorHandleMode)
        
        
        
        
        
        unHayError = False
        
        unosSourcesCadenasPorSimbolo = { }
        unosModulosCadenasPorSimbolo = { }
        
        for unCodigoEIdioma in unosCodigosEIdiomasOrdenados:
            unCodigoIdioma  = unCodigoEIdioma[ 0]
            unIdioma        = unCodigoEIdioma[ 1]
            
            unInformeExportarIdioma = theProcessControlManager.vCatalogoRaiz.fNewVoidInformeExportarTraduccionesDeIdioma()
            
            
            unInformeExportarIdioma[ 'language_code'] = unCodigoIdioma
            unInforme[ 'languages_export_reports'].append( unInformeExportarIdioma)
            
            unaCodificacionCaracteres = unasCodificacionesCaracteres.get( unCodigoIdioma, cTRAEncodingUTF8)
            unInformeExportarIdioma[ 'encoding'] = unaCodificacionCaracteres
            
            unCodigoIdiomaReferencia = theCodigosIdiomasReferencia.get( unCodigoIdioma, '')
            if unCodigoIdiomaReferencia in unosCodigosIdiomasReferenciaAExportar:
                unInformeExportarIdioma[ 'reference_language_code'] = unCodigoIdiomaReferencia
            else:
                unCodigoIdiomaReferencia  = ''
                
            
            if unSeparatedModules:
                # ##############################################################################
                """Export translations into the language with the strings in each requested module on its own output file, iterating over each named requested module and the not-specified module if requested.
                
                """
                
                unInformeExportarIdioma[ 'separate_modules'] = True
                
                for unNombreModulo in unosNombresModulosOrdenados:
                    
                    unInformeExportarModulo = theProcessControlManager.vCatalogoRaiz.fNewVoidInformeExportarTraduccionesDeModulo()
                    unInformeExportarModulo[ 'language_code'] = unCodigoIdioma
                    unInformeExportarModulo[ 'module_name']   = unNombreModulo
                    unInformeExportarIdioma[ 'modules_export_reports'].append( unInformeExportarModulo)
    
                    unFileNameProperties = ''
                    unFileNamePO         = ''
                    
                    if unExportAsJavaProperties:
                        
                        # #####################
                        """Always include language code in the filename when exporting a backup.
                        
                        """
                        aCodigoIdiomaPorDefectoAUsar = ''
                        if not( theProcessType == cTRAProgress_ProcessType_Backup):
                            aCodigoIdiomaPorDefectoAUsar = theDefaultLanguageCode
                                                
                        unDirName  = "%s%s" % ( unNombreModulo, cZipPathSeparator,)
                        unFileNameProperties = "%s%s%s%s" % ( unDirName, cFilenamePropertiesBase, theProcessControlManager.vCatalogoRaiz.fPropertiesFilenameIdiomaPostfix( unCodigoIdioma, aCodigoIdiomaPorDefectoAUsar), cPropertiesFilePostfix,)
                        unInformeExportarModulo[ 'filename_properties'] = unFileNameProperties
                        unInformeExportarModulo[ 'filename']            = unFileNameProperties
                         
                    if unExportAsGNUgettextPO:
                        unFileNamePO = "%s%s%s%s" % ( unNombreModulo,  cPOFileCharBeforeLanguage, unCodigoIdioma, cPOFilePostfix, )
                        unInformeExportarModulo[ 'filename_po'] = unFileNamePO
                        unInformeExportarModulo[ 'filename']    = unFileNamePO
                    

                    unosResultadosTraducciones = theProcessControlManager.vCatalogoRaiz.fResultadosTraduccionesExportacionIdiomaModulo( 
                        unIdioma, 
                        unNombreModulo, 
                        unExecutionRecord
                    )
                    unInformeExportarModulo[ 'translations_exported'] =  len( unosResultadosTraducciones)
                    unInformeExportarIdioma[ 'translations_exported'] += len( unosResultadosTraducciones)

                    unosResultadosTraduccionesReferencia = None
                    if unCodigoIdiomaReferencia and unExportAsGNUgettextPO:
                        unosResultadosTraduccionesReferencia = theProcessControlManager.vCatalogoRaiz.fResultadosTraduccionesExportacionIdiomaReferencia( 
                            unCodigoIdiomaReferencia, 
                            unosResultadosTraducciones, 
                            unExecutionRecord
                        )    
                        
                    if unIncludeManifest:  
                        theProcessControlManager.vCatalogoRaiz.pWriteManifestEntriesForIdioma( 
                            theBuffer               = unManifestBuffer, 
                            theCodigoIdioma         = unCodigoIdioma, 
                            theWriteEntry           = unCodigoIdioma in unosCodigosIdiomasAExportar, 
                            theWriteReferenceEntry  = unCodigoIdioma in unosCodigosIdiomasReferenciaAExportar, 
                            theWriteJavaProperties  = unExportAsJavaProperties, 
                            theFileNameProperties   = unFileNameProperties, 
                            theWriteGNUgettextPO    = unExportAsGNUgettextPO, 
                            theFileNamePO           = unFileNamePO,
                        )
                        
                    if unIncludeLocalesCSV:  
                        theProcessControlManager.vCatalogoRaiz.pWriteLocalesCSVEntriesForIdioma( 
                            theBuffer               = unLocalesCSVBuffer, 
                            theCodigoIdioma         = unCodigoIdioma, 
                            theWriteEntry           = unCodigoIdioma in unosCodigosIdiomasAExportar, 
                            theWriteReferenceEntry  = unCodigoIdioma in unosCodigosIdiomasReferenciaAExportar, 
                            theWriteJavaProperties  = unExportAsJavaProperties, 
                            theFileNameProperties   = unFileNameProperties, 
                            theWriteGNUgettextPO    = unExportAsGNUgettextPO, 
                            theFileNamePO           = unFileNamePO,
                        )
                        
                    if unFileNameProperties:
                        unResultFicheroExportacion = theProcessControlManager.vCatalogoRaiz.fContenidoFicheroExportacionIdiomaModulo_JavaProperties( 
                            theIdioma                      =unIdioma, 
                            theNombreModulo                =unNombreModulo, 
                            theCodificacionCaracteres      =unaCodificacionCaracteres, 
                            theResultadosTraducciones      =unosResultadosTraducciones, 
                            theSourcesCadenasPorSimbolo    =unosSourcesCadenasPorSimbolo,
                            theExportModuleNames           =unExportModuleNames,
                            theExportStringSources         =unExportStringSources,
                            theExportTranslationsStatus    =unExportTranslationsStatus,
                            theExportContributions         =unExportContributions,
                            theModulosCadenasPorSimbolo    =unosModulosCadenasPorSimbolo,
                            theEncodingErrorHandleMode     =theEncodingErrorHandleMode,
                            theEncodedFileErrorsMode       =anEncodedFileErrorsMode,
                            theSystemToUnicodeErrorsMode   =aSystemToUnicodeErrorsMode,
                            theUnicodeToUTF8ErrorsMode     =aUnicodeToUTF8ErrorsMode,
                            theTranslationService          =aTranslationService,
                            theParentExecutionRecord       =unExecutionRecord,                            
                        )
                        unInformeExportarModulo[ 'export_result'] = unResultFicheroExportacion
                        if ( not unResultFicheroExportacion) or  ( not unResultFicheroExportacion.get( 'success', False)):
                            unHayError = True
                            if not unResultFicheroExportacion.get( 'success', False):
                                if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                    break
                                if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CountAllErrorsAndCancel,]:
                                    continue
                        if unResultFicheroExportacion:
                            unContenidoFicheroExportacion = unResultFicheroExportacion.get( 'contenido', '')
                            unZipFile.writestr( unFileNameProperties, unContenidoFicheroExportacion)
                            unResultFicheroExportacion[ 'contenido'] = cTRAContenidoExportacionEliminado
                        
                         
                    if unFileNamePO:
                        unResultFicheroExportacion = theProcessControlManager.vCatalogoRaiz.fContenidoFicheroExportacionIdiomaModulo_GNUgettextPO(   
                            theIdioma                            =unIdioma, 
                            theDomainName                        =unNombreModulo,
                            theCodificacionCaracteres            =unaCodificacionCaracteres, 
                            theResultadosTraducciones            =unosResultadosTraducciones,
                            theResultadosTraduccionesReferencia  =unosResultadosTraduccionesReferencia, 
                            theSourcesCadenasPorSimbolo          =unosSourcesCadenasPorSimbolo,
                            theExportModuleNames                 =unExportModuleNames,
                            theExportStringSources               =unExportStringSources,
                            theExportTranslationsStatus          =unExportTranslationsStatus,
                            theExportContributions               =unExportContributions,
                            theModulosCadenasPorSimbolo          =unosModulosCadenasPorSimbolo,
                            theEncodingErrorHandleMode           =theEncodingErrorHandleMode,
                            theEncodedFileErrorsMode             =anEncodedFileErrorsMode,
                            theSystemToUnicodeErrorsMode         =aSystemToUnicodeErrorsMode,
                            theUnicodeToUTF8ErrorsMode           =aUnicodeToUTF8ErrorsMode,
                            theTranslationService                =aTranslationService,
                            theParentExecutionRecord             =unExecutionRecord,                                
                        )
                        unInformeExportarModulo[ 'export_result'] = unResultFicheroExportacion
                        if ( not unResultFicheroExportacion) or  ( not unResultFicheroExportacion.get( 'success', False)):
                            unHayError = True
                            if not unResultFicheroExportacion.get( 'success', False):
                                if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                    break
                                if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CountAllErrorsAndCancel,]:
                                    continue
                        if unResultFicheroExportacion:
                            unContenidoFicheroExportacion = unResultFicheroExportacion.get( 'contenido', '')
                            unZipFile.writestr( unFileNamePO, unContenidoFicheroExportacion)
                            unResultFicheroExportacion[ 'contenido'] = cTRAContenidoExportacionEliminado

                            
                            
                    unNumTranslationsTraversed = len( unosResultadosTraducciones)
                    if unosResultadosTraduccionesReferencia and unFileNamePO:
                        unNumTranslationsTraversed += len( unosResultadosTraduccionesReferencia)
                    aNumElementsOfTypeRead = {
                        cNombreTipoTRAIdioma: 1,
                        cNombreTipoTRAModulo: 1,
                        cNombreTipoTRATraduccion : unNumTranslationsTraversed,
                    }
                    theProcessControlManager.pProcessStep( unIdioma, aNumElementsOfTypeRead, None)
                    
                    
           
                if ( theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]) and ( unInformeExportarIdioma.get( 'num_encoding_errors', 0) > 0):
                    break
    
                if theIncluirModuloNoEspecificado:
                    # ##############################################################################
                    """Export the strings for which no module has been specified .
                    
                    """
                    unInformeExportarModulo = theProcessControlManager.vCatalogoRaiz.fNewVoidInformeExportarTraduccionesDeModulo()
                    unInformeExportarModulo[ 'language_code'] = unCodigoIdioma
                    unInformeExportarModulo[ 'module_name']   = cNombreModuloNoEspecificadoInputValue
                    unInformeExportarIdioma[ 'modules_export_reports'].append( unInformeExportarModulo)
                    
                    unFileNameProperties = ''
                    unFileNamePO         = ''
                    
                    if unExportAsJavaProperties:
                        
                        # #####################
                        """Always include language code in the filename when exporting a backup.
                        
                        """
                        aCodigoIdiomaPorDefectoAUsar = ''
                        if not( theProcessType == cTRAProgress_ProcessType_Backup):
                            aCodigoIdiomaPorDefectoAUsar = theDefaultLanguageCode
                        
                        unDirName  = "%s%s" % ( theDefaultModuleName, cZipPathSeparator,)
                        unFileNameProperties = "%s%s%s%s" % ( unDirName, cFilenamePropertiesBase, theProcessControlManager.vCatalogoRaiz.fPropertiesFilenameIdiomaPostfix( unCodigoIdioma, aCodigoIdiomaPorDefectoAUsar), cPropertiesFilePostfix,)
                        unInformeExportarModulo[ 'filename_properties'] = unFileNameProperties
                        unInformeExportarModulo[ 'filename']            = unFileNameProperties
                         
                    if unExportAsGNUgettextPO:
                        unFileNamePO = "%s%s%s%s" % ( theDefaultModuleName,  cPOFileCharBeforeLanguage, unCodigoIdioma, cPOFilePostfix, )
                        unInformeExportarModulo[ 'filename_po'] = unFileNamePO
                        unInformeExportarModulo[ 'filename']    = unFileNamePO
    

                    unosResultadosTraducciones = theProcessControlManager.vCatalogoRaiz.fResultadosTraduccionesExportacionIdiomaModuloNoEspecificado( unIdioma, unExecutionRecord)

                    unInformeExportarModulo[ 'translations_exported'] =  len( unosResultadosTraducciones)
                    unInformeExportarIdioma[ 'translations_exported'] += len( unosResultadosTraducciones)
                    
                    if len( unosResultadosTraducciones) > 0 or ( not unosNombresModulosOrdenados):
                        
                        unosResultadosTraduccionesReferencia = None
                        if unCodigoIdiomaReferencia and unExportAsGNUgettextPO:
                            unosResultadosTraduccionesReferencia = theProcessControlManager.vCatalogoRaiz.fResultadosTraduccionesExportacionIdiomaReferencia( 
                                unCodigoIdiomaReferencia, 
                                unosResultadosTraducciones, 
                                unExecutionRecord
                            )    
                                         
                        if unIncludeManifest:  
                            theProcessControlManager.vCatalogoRaiz.pWriteManifestEntriesForIdioma( 
                                theBuffer               = unManifestBuffer, 
                                theCodigoIdioma         = unCodigoIdioma, 
                                theWriteEntry           = unCodigoIdioma in unosCodigosIdiomasAExportar, 
                                theWriteReferenceEntry  = unCodigoIdioma in unosCodigosIdiomasReferenciaAExportar, 
                                theWriteJavaProperties  = unExportAsJavaProperties, 
                                theFileNameProperties   = unFileNameProperties, 
                                theWriteGNUgettextPO    = unExportAsGNUgettextPO, 
                                theFileNamePO           = unFileNamePO,
                            )
        
                        if unIncludeLocalesCSV:  
                            theProcessControlManager.vCatalogoRaiz.pWriteLocalesCSVEntriesForIdioma( 
                                theBuffer               = unLocalesCSVBuffer, 
                                theCodigoIdioma         = unCodigoIdioma, 
                                theWriteEntry           = unCodigoIdioma in unosCodigosIdiomasAExportar, 
                                theWriteReferenceEntry  = unCodigoIdioma in unosCodigosIdiomasReferenciaAExportar, 
                                theWriteJavaProperties  = unExportAsJavaProperties, 
                                theFileNameProperties   = unFileNameProperties, 
                                theWriteGNUgettextPO    = unExportAsGNUgettextPO, 
                                theFileNamePO           = unFileNamePO,
                            )
        
                        if unFileNameProperties:
                            unResultFicheroExportacion = theProcessControlManager.vCatalogoRaiz.fContenidoFicheroExportacionIdiomaModuloNoEspecificado_JavaProperties( 
                                theIdioma                      =unIdioma, 
                                theNombreModulo                =theDefaultModuleName, 
                                theCodificacionCaracteres      =unaCodificacionCaracteres, 
                                theResultadosTraducciones      =unosResultadosTraducciones, 
                                theSourcesCadenasPorSimbolo    =unosSourcesCadenasPorSimbolo,
                                theExportModuleNames           =unExportModuleNames,
                                theExportStringSources         =unExportStringSources,
                                theExportTranslationsStatus    =unExportTranslationsStatus,
                                theExportContributions         =unExportContributions,
                                theModulosCadenasPorSimbolo    =unosModulosCadenasPorSimbolo,
                                theEncodingErrorHandleMode     =theEncodingErrorHandleMode,
                                theEncodedFileErrorsMode       =anEncodedFileErrorsMode,
                                theSystemToUnicodeErrorsMode   =aSystemToUnicodeErrorsMode,
                                theUnicodeToUTF8ErrorsMode     =aUnicodeToUTF8ErrorsMode,
                                theTranslationService          =aTranslationService,
                                theParentExecutionRecord       =unExecutionRecord,                            
                            )
                            unInformeExportarModulo[ 'export_result'] = unResultFicheroExportacion
                            if ( not unResultFicheroExportacion) or  ( not unResultFicheroExportacion.get( 'success', False)):
                                unHayError = True
                                if not unResultFicheroExportacion.get( 'success', False):
                                    if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                        break
                                    if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CountAllErrorsAndCancel,]:
                                        continue
                                 
                            if unResultFicheroExportacion:
                                unContenidoFicheroExportacion = unResultFicheroExportacion.get( 'contenido', '')
                                unZipFile.writestr( unFileNameProperties, unContenidoFicheroExportacion)
                                unResultFicheroExportacion[ 'contenido'] = cTRAContenidoExportacionEliminado
                                
                                
                                
                                
                        if unFileNamePO:
                            unResultFicheroExportacion = theProcessControlManager.vCatalogoRaiz.fContenidoFicheroExportacionIdiomaModuloNoEspecificado_GNUgettextPO(   
                                theIdioma                            =unIdioma, 
                                theDomainName                        =theDefaultDomain,
                                theCodificacionCaracteres            =unaCodificacionCaracteres, 
                                theResultadosTraducciones            =unosResultadosTraducciones,
                                theResultadosTraduccionesReferencia  =unosResultadosTraduccionesReferencia, 
                                theSourcesCadenasPorSimbolo          =unosSourcesCadenasPorSimbolo,
                                theExportModuleNames                 =unExportModuleNames,
                                theExportStringSources               =unExportStringSources,
                                theExportTranslationsStatus          =unExportTranslationsStatus,
                                theModulosCadenasPorSimbolo          =unosModulosCadenasPorSimbolo,
                                theEncodingErrorHandleMode           =theEncodingErrorHandleMode,
                                theEncodedFileErrorsMode             =anEncodedFileErrorsMode,
                                theSystemToUnicodeErrorsMode         =aSystemToUnicodeErrorsMode,
                                theUnicodeToUTF8ErrorsMode           =aUnicodeToUTF8ErrorsMode,
                                theTranslationService                =aTranslationService,
                                theParentExecutionRecord             =unExecutionRecord,                                
                            )
                            unInformeExportarModulo[ 'export_result'] = unResultFicheroExportacion
                            if ( not unResultFicheroExportacion) or  ( not unResultFicheroExportacion.get( 'success', False)):
                                unHayError = True
                                if not unResultFicheroExportacion.get( 'success', False):
                                    if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                        break
                                    if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CountAllErrorsAndCancel,]:
                                        continue
                            if unResultFicheroExportacion:
                                unContenidoFicheroExportacion = unResultFicheroExportacion.get( 'contenido', '')
                                unZipFile.writestr( unFileNamePO, unContenidoFicheroExportacion)
                                unResultFicheroExportacion[ 'contenido'] = cTRAContenidoExportacionEliminado
                                
                                
                        

                        unNumTranslationsTraversed = len( unosResultadosTraducciones)
                        if unosResultadosTraduccionesReferencia and unFileNamePO:
                            unNumTranslationsTraversed += len( unosResultadosTraduccionesReferencia)
                        aNumElementsOfTypeRead = {
                            cNombreTipoTRAIdioma: 1,
                            cNombreTipoTRATraduccion : unNumTranslationsTraversed,
                        }
                        theProcessControlManager.pProcessStep( unIdioma, aNumElementsOfTypeRead, None)
                                
                if ( theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]) and ( unInformeExportarIdioma.get( 'num_encoding_errors', 0) > 0):
                    break
                        
                
                
                
                
                
            else: # not unSeparatedModules
                # ##############################################################################
                """Export translations into the language in a single file with the strings in all modules and the not-specified module if requested.
                
                """
                unInformeExportarIdioma[ 'separate_modules'] = False
    
                unFileNameProperties = ''
                unFileNamePO         = ''
                
                if unExportAsJavaProperties:
                    
                    # #####################
                    """Always include language code in the filename when exporting a backup.
                    
                    """
                    aCodigoIdiomaPorDefectoAUsar = ''
                    if not( theProcessType == cTRAProgress_ProcessType_Backup):
                        aCodigoIdiomaPorDefectoAUsar = theDefaultLanguageCode
                                                
                    unFileNameProperties = "%s%s%s" % ( cFilenamePropertiesBase, theProcessControlManager.vCatalogoRaiz.fPropertiesFilenameIdiomaPostfix( unCodigoIdioma, aCodigoIdiomaPorDefectoAUsar), cPropertiesFilePostfix,)
                    unInformeExportarIdioma[ 'filename_properties'] = unFileNameProperties
                    unInformeExportarIdioma[ 'filename']            = unFileNameProperties
                     
                if unExportAsGNUgettextPO:
                    unFileNamePO = "%s%s%s%s" % ( cPONoSeparateModulesFileNamePrefix,  cPOFileCharBeforeLanguage, unCodigoIdioma, cPOFilePostfix, )
                    unInformeExportarIdioma[ 'filename_po'] = unFileNamePO
                    unInformeExportarIdioma[ 'filename']    = unFileNamePO
    
    
                unosResultadosTraducciones = theProcessControlManager.vCatalogoRaiz.fResultadosTraduccionesExportacionIdiomaAlgunosModulos( 
                    unIdioma, 
                    unosNombresModulosOrdenados,
                    theIncluirModuloNoEspecificado,
                    unExecutionRecord
                )

                unInformeExportarIdioma[ 'translations_exported'] = len( unosResultadosTraducciones)
                
                unosResultadosTraduccionesReferencia = None
                if unCodigoIdiomaReferencia and unExportAsGNUgettextPO:
                    unosResultadosTraduccionesReferencia = theProcessControlManager.vCatalogoRaiz.fResultadosTraduccionesExportacionIdiomaReferencia( 
                        unCodigoIdiomaReferencia, 
                        unosResultadosTraducciones, 
                        unExecutionRecord
                    )    
                
                if unIncludeManifest:  
                    theProcessControlManager.vCatalogoRaiz.pWriteManifestEntriesForIdioma( 
                        theBuffer               = unManifestBuffer, 
                        theCodigoIdioma         = unCodigoIdioma, 
                        theWriteEntry           = unCodigoIdioma in unosCodigosIdiomasAExportar, 
                        theWriteReferenceEntry  = unCodigoIdioma in unosCodigosIdiomasReferenciaAExportar, 
                        theWriteJavaProperties  = unExportAsJavaProperties, 
                        theFileNameProperties   = unFileNameProperties, 
                        theWriteGNUgettextPO    = unExportAsGNUgettextPO, 
                        theFileNamePO           = unFileNamePO,
                    )
    
                if unIncludeLocalesCSV:  
                    theProcessControlManager.vCatalogoRaiz.pWriteLocalesCSVEntriesForIdioma( 
                        theBuffer               = unLocalesCSVBuffer, 
                        theCodigoIdioma         = unCodigoIdioma, 
                        theWriteEntry           = unCodigoIdioma in unosCodigosIdiomasAExportar, 
                        theWriteReferenceEntry  = unCodigoIdioma in unosCodigosIdiomasReferenciaAExportar, 
                        theWriteJavaProperties  = unExportAsJavaProperties, 
                        theFileNameProperties   = unFileNameProperties, 
                        theWriteGNUgettextPO    = unExportAsGNUgettextPO, 
                        theFileNamePO           = unFileNamePO,
                    )
    
                if unFileNameProperties:
                    unResultFicheroExportacion  = theProcessControlManager.vCatalogoRaiz.fContenidoFicheroExportacionIdiomaTodosModulos_JavaProperties( 
                        theIdioma                      =unIdioma, 
                        theNombreModulo                =theDefaultModuleName, 
                        theCodificacionCaracteres      =unaCodificacionCaracteres, 
                        theResultadosTraducciones      =unosResultadosTraducciones, 
                        theSourcesCadenasPorSimbolo    =unosSourcesCadenasPorSimbolo,
                        theExportModuleNames           =unExportModuleNames,
                        theExportStringSources         =unExportStringSources,
                        theExportTranslationsStatus    =unExportTranslationsStatus,
                        theExportContributions         =unExportContributions,
                        theModulosCadenasPorSimbolo    =unosModulosCadenasPorSimbolo,
                        theEncodingErrorHandleMode     =theEncodingErrorHandleMode,
                        theEncodedFileErrorsMode       =anEncodedFileErrorsMode,
                        theSystemToUnicodeErrorsMode   =aSystemToUnicodeErrorsMode,
                        theUnicodeToUTF8ErrorsMode     =aUnicodeToUTF8ErrorsMode,
                        theTranslationService          =aTranslationService,
                        theParentExecutionRecord       =unExecutionRecord,                            
                    )
                    unInformeExportarIdioma[ 'export_result'] = unResultFicheroExportacion
                    if ( not unResultFicheroExportacion) or  ( not unResultFicheroExportacion.get( 'success', False)):
                        unHayError = True
                        if not unResultFicheroExportacion.get( 'success', False):
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                break
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CountAllErrorsAndCancel,]:
                                continue
                    if unResultFicheroExportacion:
                        unContenidoFicheroExportacion = unResultFicheroExportacion.get( 'contenido', '')
                        unZipFile.writestr( unFileNameProperties, unContenidoFicheroExportacion)
                        unResultFicheroExportacion[ 'contenido'] = cTRAContenidoExportacionEliminado
                        
                        
                        
                if unFileNamePO:
                    unResultFicheroExportacion = theProcessControlManager.vCatalogoRaiz.fContenidoFicheroExportacionIdiomaTodosModulos_GNUgettextPO(   
                        theIdioma                            =unIdioma, 
                        theDomainName                        =theDefaultDomain,
                        theCodificacionCaracteres            =unaCodificacionCaracteres, 
                        theResultadosTraducciones            =unosResultadosTraducciones,
                        theResultadosTraduccionesReferencia  =unosResultadosTraduccionesReferencia, 
                        theSourcesCadenasPorSimbolo          =unosSourcesCadenasPorSimbolo,
                        theExportModuleNames                 =unExportModuleNames,
                        theExportStringSources               =unExportStringSources,
                        theExportTranslationsStatus          =unExportTranslationsStatus,
                        theExportContributions               =unExportContributions,
                        theModulosCadenasPorSimbolo          =unosModulosCadenasPorSimbolo,
                        theEncodingErrorHandleMode           =theEncodingErrorHandleMode,
                        theEncodedFileErrorsMode             =anEncodedFileErrorsMode,
                        theSystemToUnicodeErrorsMode         =aSystemToUnicodeErrorsMode,
                        theUnicodeToUTF8ErrorsMode           =aUnicodeToUTF8ErrorsMode,
                        theTranslationService                =aTranslationService,
                        theParentExecutionRecord             =unExecutionRecord,                                
                    )
                    unInformeExportarIdioma[ 'export_result'] = unResultFicheroExportacion
                    if ( not unResultFicheroExportacion) or  ( not unResultFicheroExportacion.get( 'success', False)):
                        unHayError = True
                        if not unResultFicheroExportacion.get( 'success', False):
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                break
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CountAllErrorsAndCancel,]:
                                continue
                    if unResultFicheroExportacion:
                        unContenidoFicheroExportacion = unResultFicheroExportacion.get( 'contenido', '')
                        unZipFile.writestr( unFileNamePO, unContenidoFicheroExportacion)
                        unResultFicheroExportacion[ 'contenido'] = cTRAContenidoExportacionEliminado
                        
                        
                unNumTranslationsTraversed = len( unosResultadosTraducciones)
                if unosResultadosTraduccionesReferencia and unFileNamePO:
                    unNumTranslationsTraversed += len( unosResultadosTraduccionesReferencia)
                aNumElementsOfTypeRead = {
                    cNombreTipoTRAIdioma: 1,
                    cNombreTipoTRAModulo: len( unosNombresModulosOrdenados),
                    cNombreTipoTRATraduccion : unNumTranslationsTraversed,
                }
                theProcessControlManager.pProcessStep( unIdioma, aNumElementsOfTypeRead, None)
                
          
        if theSpecificFilename:
            unNombreArchivoDescarga = theSpecificFilename
        elif theFilenameForGvSIG:
            unNombreArchivoDescarga = theProcessControlManager.vCatalogoRaiz.fNombreArchivoExportacion_ForGvSIG( sorted( theCodigosIdiomas)[ 0], theProductName, theProductVersion, theL10NVersion, theTipoArchivo)
        else:
            unNombreArchivoDescarga = theProcessControlManager.vCatalogoRaiz.fNombreArchivoExportacion( [ unCodigoEIdioma[ 0] for unCodigoEIdioma in unosCodigosEIdiomasOrdenados], unosNombresModulosOrdenados, theIncluirModuloNoEspecificado, theTipoArchivo)
        
        unInforme[ 'download_filename'] = unNombreArchivoDescarga
        theProcessControlManager.vResult[ 'download_filename']       = unInforme[ 'download_filename'] 
        
        
        if unHayError and ( theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError, cTRAEncodingErrorHandleMode_CountAllErrorsAndCancel]):
            theProcessControlManager.vResult[ 'success']   = False
            theProcessControlManager.vResult[ 'condition'] = 'EncodingErrorsDuringExport'
            return None
                        
        if unIncludeManifest:  
            unZipFile.writestr( cManifestFileFullName, unManifestBuffer.getvalue())
            
        if unIncludeLocalesCSV:  
            unZipFile.writestr( cLocalesCSVFileFullName, unLocalesCSVBuffer.getvalue())
            
            
            
            
            
            
        # #############################################
        """Export Translations catalog contents, like configurations and process control parameters, as an XML file added to the export achive file.
        
        """
        if  anExportXML:
            
            someAdditionalParms = {
                'theExcludeUsers'       :True,
                'theExcludeCounters'    :True,
                'theExcludeDates'       :True,
                'theExcludeUIDs'        :False,
                'theExcludeFiles'       :False,
                'theExcludeEmpty'       :False,
                'theSortByIds'          :False,
                'theForceRootId'        :False,
                'theArchiveFormat'      :'none',
            }
            
            # ##############################
            """Retrieve export contents using a framework service based on model traversal.
            
            """
            anExportResult = aModelDDvlPloneTool.fExport( 
                theTimeProfilingResults     =None,
                theObject                   =theProcessControlManager.vCatalogoRaiz, 
                theAllExportTypeConfigs     =someExportTypeConfigsChosen,
                theOutputEncoding           =cTRAEncodingUTF8,
                theReturnXML                =True,
                theAdditionalParams         =someAdditionalParms,
            )
            if anExportResult and anExportResult.get( 'success', False):
                
                
                # ##############################
                """If successful, write export contents XML file, and any included binary files (i.e. images used as flags for languages not-well-known by Plone.
                
                """
                
                anExportFileName  = anExportResult.get( 'filename', '')
                anExportXMLString = anExportResult.get( 'xml_string', '')
                
                if anExportFileName:
                    if not anExportXMLString:
                        anExportXMLString = ''
                        
                    unZipFile.writestr( anExportFileName, anExportXMLString)
                        
                    
                    
                someFileNamesAndContent = anExportResult.get( 'file_names_and_content', [])
                if someFileNamesAndContent:
                    for aFileNameAndContent in someFileNamesAndContent:
                        
                        aFileName    = aFileNameAndContent[ 0]
                        aFileContent = aFileNameAndContent[ 1]
                        if aFileName:
                            unZipFile.writestr( aFileName, aFileContent)
                            
             

        unZipFile.close()  
        
        unStoreFilePath, unStoreFileName = theProcessControlManager.vCatalogoRaiz.fStoreExportedFile( unNombreArchivoDescarga, unZipBuffer.getvalue())
        if not ( unStoreFilePath and unStoreFileName):
            theProcessControlManager.vResult[ 'success']   = False
            theProcessControlManager.vResult[ 'condition'] = cExportStatus_CanNotStoreExportedFile
            unInforme.update( {
                'success':              False,
                'status':               cExportStatus_CanNotStoreExportedFile,
            })
            return None
            
        unInforme.update( {
            'store_file_path':      unStoreFilePath,
            'store_file_name':      unStoreFileName,
        })
        
        theProcessControlManager.vResult[ 'store_file_path']       = unInforme[ 'store_file_path'] 
        theProcessControlManager.vResult[ 'store_file_name']       = unInforme[ 'store_file_name'] 
        
        
        theProcessControlManager.vResult[ 'success']   = True
        unInforme.update( {
            'success':              True,
        })
        return None
    
    finally:
        unExecutionRecord and unExecutionRecord.pEndExecution()
     
                    
        

    


##/code-section module-footer



