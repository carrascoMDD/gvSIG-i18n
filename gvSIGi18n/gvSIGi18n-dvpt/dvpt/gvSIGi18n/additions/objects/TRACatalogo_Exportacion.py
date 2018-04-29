# -*- coding: utf-8 -*-
#
# File: TRACatalogo_Exportacion.py
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



from TRAElemento_Constants         import *
from TRAImportarExportar_Constants import *
from TRAElemento_Permission_Definitions import cUseCase_ImportTRAImportacion, cUseCase_Export, cUseCase_Backup_TRACatalogo, cUseCase_ExportGvSIG_TRAIdioma, cBoundObject


##/code-section module-header


##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema



##code-section after-schema #fill in your manual code here


##/code-section after-schema

class TRACatalogo_Exportacion:
    """
    """
    security = ClassSecurityInfo()


    
    
    
    
    ##code-section class-header #fill in your manual code here
    

    
    
    security.declarePublic( 'fLabelModuloNoEspecificado')    
    def fLabelModuloNoEspecificado( self):
        unLabelModuloNoEspecificado = u' ? ' + self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_ModuloNoEspecificado_msgid',  'not specified' )
        aTranslationService = self.getTranslationServiceTool()
        if not aTranslationService:
            return ''
        return aTranslationService.encode( unLabelModuloNoEspecificado) 
         
    
    
    

    security.declarePrivate( 'fPropertiesFilenameIdiomaPostfix')    
    def fPropertiesFilenameIdiomaPostfix( self, theCodigoIdioma, theCodigoIdiomaPorDefecto):
        if not theCodigoIdioma:
            return ''
        
        if theCodigoIdioma == theCodigoIdiomaPorDefecto:
            return  ''
        
        return '_' + theCodigoIdioma.replace( cLanguageSeparatorCountry, cPropertiesFileCharBeforeCountry)
        
    
    
    
    
    security.declarePrivate( 'fNewVoidInformeExportarTraducciones')    
    def fNewVoidInformeExportarTraducciones( self,):
        unInforme = {
            'success':                  False,
            'status':                   '',
            'exception':                '',
            'export_format':            '',
            'include_manifest':         '',
            'include_localescsv':       '',
            'separate_modules':         False,
            'languages_requested':      [],
            'reference_languages':      {},
            'languages_export_reports': [],
            'modules_requested':        [],
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
        return cEncodingErrorHandleModes[:]
    
        
    
    
    def fNewVoidResultFicheroExportacionGNUgettextPO( self,):
        unResult = self.fNewVoidResultFicheroExportacionProperties().copy()
        unResult.update({
            'file_kind':                                                 '.PO',
            'traduccionesReferencia_error_codificacion_SystemToUnicode':  [],
            'traduccionesReferencia_error_codificacion_UnicodeToUTF':     [],
            'traduccionesReferencia_error_codificacion_Export':           [],
        })
        return unResult
    
    
    def fNewVoidResultFicheroExportacionProperties( self,):
        unResult = {
            'file_kind':                                        '.properties',
            'success':                                          False,
            'status':                                           '',
            'encoding':                                         '',
            'encoding_error_handle_mode':                       '',
            'encoded_file_errors_mode':                         '',
            'system_to_unicode_errors_mode':                    '',
            'unicode_to_utf8_errors_mode':                      '',
            'contenido':                                        '',
            'total_encoding_errors':                            0,
            'header_error_codificacion_SystemToUnicode':        False,
            'header_error_codificacion_UnicodeToUTF':           False,
            'header_error_codificacion_Export':                 False,
            'simbolos_error_codificacion_SystemToUnicode':      [],
            'simbolos_error_codificacion_UnicodeToUTF':         [],
            'simbolos_error_codificacion_Export':               [],
            'traducciones_error_codificacion_SystemToUnicode':  [],
            'traducciones_error_codificacion_UnicodeToUTF':     [],
            'traducciones_error_codificacion_Export':           [],
            'sources_error_codificacion_SystemToUnicode':       [],
            'sources_error_codificacion_UnicodeToUTF':          [],
            'sources_error_codificacion_Export':                [],
            'modules_error_codificacion_SystemToUnicode':       [],
            'modules_error_codificacion_UnicodeToUTF':          [],
            'modules_error_codificacion_Export':                [],
        }
        return unResult
    

    

    
                
    #security.declareProtected( permissions.View, 'fExportarIdiomaParaGvSIG')    
    #def fExportarIdiomaParaGvSIG( self, 
        #theIdioma                        = None,
        #someExportParameters               = None,
        #thePermissionsCache              = None,
        #theRolesCache                    = None,
        #theParentExecutionRecord         = None):
        #"""Export Translations into the selected languages, in any Module, with the parameters prefered for gvSIG. 
        
        #"""
  
        #unExecutionRecord = self.fStartExecution( 'method',  'fExportarIdiomaParaGvSIG', theParentExecutionRecord, False) 

        #try:
            
            #try:
                #unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                #unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache

                
                #if ( theIdioma == None):
                    #return None
                
                #unCodigoIdioma = theIdioma.getCodigoIdiomaEnGvSIG()
                #if not unCodigoIdioma:
                    #return None
                    
                #unosCodigosIdiomas           = [ unCodigoIdioma,]
                #unosCodigosIdiomasReferencia = dict( [ ( unCodigoIdioma, (( unCodigoIdioma == 'en') and 'es') or 'en',)])
                
                #someModulesToExport = someExportParameters.get( 'theModulesToExport', [])
                #if not someModulesToExport:
                    #someModulesToExport = [ unModulo.Title() for unModulo in self.fObtenerTodosModulos()] + [ cModuloNoEspecificado_ValorNombre,]
                    
                
                #someExportParameters = {
                    #'theLanguagesToExport':         unosCodigosIdiomas,
                    #'theCodigosIdiomaReferencia':   unosCodigosIdiomasReferencia,
                    #'theCodificacionesCaracteres':  dict( [ ( unCodigo, cEncodingUnicodeEscape,) for unCodigo in unosCodigosIdiomas]), 
                    #'theModulesToExport':           someModulesToExport,
                    #'theExportFormat':              cExportFormatOption_JavaProperties,
                    #'theIncludeManifest':           'No',
                    #'theIncludeManifest_vocabulary': ['Si', 'No',],
                    #'theIncludeLocalesCSV':         'Si',
                    #'theIncludeLocalesCSV_vocabulary': ['Si', 'No',],
                    #'theSeparatedModules':          'No',
                    #'theSeparatedModules_vocabulary': ['Si', 'No',],
                    #'theDefaultLanguageCode':       'es',
                    #'theTipoArchivo':               cZipFilePostfix,
                    #'theEncodingErrorHandleMode':   cEncodingErrorHandleMode_BackslashReplaceAndContinue,
                    #'theFilenameForGvSIG':          'Si',
                    #'theFilenameForGvSIG_vocabulary': ['Si', 'No',],
                    #'theProductName':               someExportParameters.get( 'theProductName',    self.getNombreProducto()),
                    #'theProductVersion':            someExportParameters.get( 'theProductVersion', '1'),
                    #'theL10NVersion':               someExportParameters.get( 'theL10NVersion',    '1'),
                    #'theSpecificFilename':          None,
                #}
                
                #anExportReport = self.fExportarTraducciones( 
                    #False, 
                    #someExportParameters, 
                    #unPermissionsCache, 
                    #unRolesCache, 
                    #None, 
                    #unExecutionRecord,
                #)
                #return anExportReport
            
   
            #except:
                    
                #unaExceptionInfo = sys.exc_info()
                #unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                #unInformeExcepcion = 'Exception during fExportarIdiomaParaGvSIG\n' 
                #unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                #unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                #unInformeExcepcion += unaExceptionFormattedTraceback   

                #unInforme= {
                    #'success':              False,
                    #'status':               cExportStatus_Exception,
                    #'exception':            unInformeExcepcion,
                #}
                
                #unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
                #if cLogExceptions:
                    #logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                    
                #return unInforme                 
    
        #finally:
            #unExecutionRecord and unExecutionRecord.pEndExecution()
                      
   
                             
     
    
                
    #security.declareProtected( permissions.View, 'fExportarBackup')    
    #def fExportarBackup( self, 
        #thePermissionsCache              = None,
        #theRolesCache                    = None,
        #theParentExecutionRecord         = None):
        #"""Export all Translations of all Strings into all languages, in any Module, such that importing the export result shall recreate the translations catalog, except the history of changes. 
        
        #"""
  
        #unExecutionRecord = self.fStartExecution( 'method',  'fExportarBackup', theParentExecutionRecord, False) 

        #try:
            
            #try:
                    
                #unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                #unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache

                #unosCodigosIdiomas = [ unIdioma.getCodigoIdiomaEnGvSIG() for unIdioma in self.fObtenerTodosIdiomas()]
                #someExportParameters = {
                    #'theLanguagesToExport':         unosCodigosIdiomas,
                    #'theCodigosIdiomaReferencia':   {}, # No reference language
                    #'theCodificacionesCaracteres':  dict( [ ( unCodigo, cDefaultExportEncodingName_GNUgettextPO,) for unCodigo in unosCodigosIdiomas]), 
                    #'theModulesToExport':           [ unModulo.Title() for unModulo in self.fObtenerTodosModulos()] + [ cModuloNoEspecificado_ValorNombre,],
                    #'theExportFormat':              cExportFormatOption_GNUgettextPO,
                    #'theIncludeManifest':           'Si',
                    #'theIncludeManifest_vocabulary': ['Si', 'No',],
                    #'theIncludeLocalesCSV':         'Si',
                    #'theIncludeLocalesCSV_vocabulary': ['Si', 'No',],
                    #'theSeparatedModules':          'No',
                    #'theSeparatedModules_vocabulary': ['Si', 'No',],
                    #'theTipoArchivo':               cZipFilePostfix,
                    #'theEncodingErrorHandleMode':   cEncodingErrorHandleMode_BackslashReplaceAndContinue,
                    #'theFilenameForGvSIG':          'No',
                    #'theFilenameForGvSIG_vocabulary': ['Si', 'No',],
                    #'theProductName':               self.getNombreProducto(),
                    #'theProductVersion':            '',
                    #'theL10NVersion':               '',
                    #'theSpecificFilename':          '%s_BACKUP_%s_%s.zip' % ( self.getNombreProducto(), self.fDateTimeNowTextual().replace( ' ', '_'), self.fGetMemberId())
                #}
                
                #anExportReport = self.fExportarTraducciones( 
                    #False, 
                    #someExportParameters, 
                    #unPermissionsCache, 
                    #unRolesCache, 
                    #None, 
                    #unExecutionRecord,
                #)
                #return anExportReport
            
   
            #except:
                    
                #unaExceptionInfo = sys.exc_info()
                #unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                #unInformeExcepcion = 'Exception during fExportarBackup\n' 
                #unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                #unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                #unInformeExcepcion += unaExceptionFormattedTraceback   

                #unInforme= {
                    #'success':              False,
                    #'status':               cExportStatus_Exception,
                    #'exception':            unInformeExcepcion,
                #}
                
                #unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
                #if cLogExceptions:
                    #logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                    
                #return unInforme                 
    
        #finally:
            #unExecutionRecord and unExecutionRecord.pEndExecution()
                      
   
                            
                
    
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
                    
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache

                
                
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
                theTipoArchivo                  = theParametersInput.get( 'theTipoArchivo', '')
                theDefaultLanguageCode          = theParametersInput.get( 'theDefaultLanguageCode', '')
                theDefaultModuleName            = theParametersInput.get( 'theDefaultModuleName', '')
                theEncodingErrorHandleMode      = theParametersInput.get( 'theEncodingErrorHandleMode', '')
                theFilenameForGvSIG             = theParametersInput.get( 'theFilenameForGvSIG', '')   == ( theParametersInput.get( 'theFilenameForGvSIG_vocabulary', ['xXxXxXx',])[ 0])
                theProductName                  = theParametersInput.get( 'theProductName', '')
                theProductVersion               = theParametersInput.get( 'theProductVersion', '')
                theL10NVersion                  = theParametersInput.get( 'theL10NVersion', '')
                theSpecificFilename             = theParametersInput.get( 'theSpecificFilename', '')
                
       
                 
                unInforme[ 'languages_requested'] = ( theCodigosIdiomas or [])[:]
                unInforme[ 'modules_requested']   = ( theNombresModulos or [])[:]
                unInforme[ 'reference_languages']   = ( theCodigosIdiomasReferencia and theCodigosIdiomasReferencia.copy()) or {}
                
                
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
                        
                    if unCodigoIdioma in unosCodigosIdiomasReferencia:
                        unosCodigosIdiomasReferenciaAExportar.add( unCodigoIdioma)
                        if unExportAsJavaProperties:
                            if not( unCodigoIdioma in unosCodigosIdiomasAExportar):
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
                        unasCodificacionesCaracteres[ unCodigoIdioma] = cEncodingUTF8
                     
            
                
                
                
                # ##############################################################################
                """Create in-memory zip file for exported content, to be sent back to the user in the HTTP request response.
                
                """
                unZipBuffer = None
                unZipFile   = None
                
                # ##############################################################################
                """Create in-memory buffer for the manifest file.
                
                """
                unManifestBuffer = None
                
                    
               
                # ##############################################################################
                """Create in-memory buffer for the locales csv file.
                
                """
                unLocalesCSVBuffer = None
                
                    
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
                aTranslationService = self.getTranslationServiceTool()       
                
                
                
                # ##############################################################################
                """How to handle encoding errors.
                
                """
                anEncodedFileErrorsMode     = self.fEncodedFileErrorsMode(      theEncodingErrorHandleMode)
                aSystemToUnicodeErrorsMode  = self.fSystemToUnicodeErrorsMode(  theEncodingErrorHandleMode)
                aUnicodeToUTF8ErrorsMode    = self.fUnicodeToUTF8ErrorsMode(    theEncodingErrorHandleMode)

                
                
                unHayError = False
                
                
                for unCodigoEIdioma in unosCodigosEIdiomasOrdenados:
                    unCodigoIdioma  = unCodigoEIdioma[ 0]
                    unIdioma        = unCodigoEIdioma[ 1]
                    
                    unInformeExportarIdioma = self.fNewVoidInformeExportarTraduccionesDeIdioma()
                    
                    
                    unInformeExportarIdioma[ 'language_code'] = unCodigoIdioma
                    unInforme[ 'languages_export_reports'].append( unInformeExportarIdioma)
                    
                    unaCodificacionCaracteres = unasCodificacionesCaracteres.get( unCodigoIdioma, cEncodingUTF8)
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
                                unFileNameProperties = "%s%s%s%s" % ( unDirName, cFilenamePropertiesBase, self.fPropertiesFilenameIdiomaPostfix( unCodigoIdioma, theDefaultLanguageCode or self.fCodigoIdiomaPorDefecto()), cPropertiesFilePostfix,)
                                unInformeExportarModulo[ 'filename_properties'] = unFileNameProperties
                                unInformeExportarModulo[ 'filename']            = unFileNameProperties
                                 
                            if unExportAsGNUgettextPO:
                                unFileNamePO = "%s%s%s%s" % ( unNombreModulo,  cPOFileCharBeforeLanguage, unCodigoIdioma, cPOFilePostfix, )
                                unInformeExportarModulo[ 'filename_po'] = unFileNamePO
                                unInformeExportarModulo[ 'filename']    = unFileNamePO
                            
                            unosSimbolosCadenasEnModulo = self.fListaSimbolosCadenasOrdenadosEnModulo( unNombreModulo, unExecutionRecord)
                            unInformeExportarModulo[ 'translations_exported'] =  len( unosSimbolosCadenasEnModulo)
                            unInformeExportarIdioma[ 'translations_exported'] += len( unosSimbolosCadenasEnModulo)
                                
                   
                        if ( theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]) and ( unInformeExportarIdioma.get( 'num_encoding_errors', 0) > 0):
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
                                unFileNameProperties = "%s%s%s" % ( cFilenamePropertiesBase, self.fPropertiesFilenameIdiomaPostfix( unCodigoIdioma, theDefaultLanguageCode or self.fCodigoIdiomaPorDefecto()), cPropertiesFilePostfix,)
                                unInformeExportarModulo[ 'filename_properties'] = unFileNameProperties
                                unInformeExportarModulo[ 'filename']            = unFileNameProperties
                                 
                            if unExportAsGNUgettextPO:
                                unFileNamePO = "%s%s%s%s" % ( theDefaultModuleName or self.fNombreModuloPorDefecto(),  cPOFileCharBeforeLanguage, unCodigoIdioma, cPOFilePostfix, )
                                unInformeExportarModulo[ 'filename_po'] = unFileNamePO
                                unInformeExportarModulo[ 'filename']    = unFileNamePO

                            unosSimbolosCadenasEnModuloNoEspecificado = self.fListaSimbolosCadenasOrdenadosModuloNoEspecificado( unExecutionRecord)
                            unInformeExportarModulo[ 'translations_exported'] =  len( unosSimbolosCadenasEnModuloNoEspecificado)
                            unInformeExportarIdioma[ 'translations_exported'] += len( unosSimbolosCadenasEnModuloNoEspecificado)
                                
                                        
                        if ( theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]) and ( unInformeExportarIdioma.get( 'num_encoding_errors', 0) > 0):
                            break
                                
                        
                        
                        
                        
                        
                    else: # not unSeparatedModules
                        # ##############################################################################
                        """Export translations into the language in a single file with the strings in all modules and the not-specified module if requested.
                        
                        """
                        unInformeExportarIdioma[ 'separate_modules'] = False
        
                        unFileNameProperties = ''
                        unFileNamePO         = ''
                        
                        if unExportAsJavaProperties:
                            unFileNameProperties = "%s%s%s" % ( cFilenamePropertiesBase, self.fPropertiesFilenameIdiomaPostfix( unCodigoIdioma, theDefaultLanguageCode or self.fCodigoIdiomaPorDefecto()), cPropertiesFilePostfix,)
                            unInformeExportarIdioma[ 'filename_properties'] = unFileNameProperties
                            unInformeExportarIdioma[ 'filename']            = unFileNameProperties
                             
                        if unExportAsGNUgettextPO:
                            unFileNamePO = "%s%s%s%s" % ( cNoSeparateModulesFileNamePrefix,  cPOFileCharBeforeLanguage, unCodigoIdioma, cPOFilePostfix, )
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
                
                
                if unHayError and ( theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError, cEncodingErrorHandleMode_CountAllErrorsAndCancel]):
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
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
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
        
        unNombreArchivoExportacion = '%s%s%s%s%s%s%s%s' % ( cExportZipFileNamePrefix, cOutputFileNameLanguageSeparator, unosCodigosIdiomasNombreArchivo, cOutputFileNameModuleSeparator, unLastNombresModulosNombreArchivo, cOutputFileNameModuleSeparator, unTimestamp, unArchivePostfix)
        
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
#  Retrieval methods
# ####################################################

    
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
            unStringUTF8 = theTranslationService.encode( unStringUnicode, cEncodingUTF8, errors=theUnicodeToUTF8ErrorsMode)
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
    
    
    
    
    
# ####################################################
#  Java Properties output
# ####################################################
    
    
    security.declarePrivate( 'fWriteHeader_JavaProperties')    
    def fWriteHeader_JavaProperties( self, 
        theBuffer, 
        theResult,
        theIdioma, 
        theNombreModulo, 
        theCodificacionCaracteres,
        theEncodingErrorHandleMode, 
        theSystemToUnicodeErrorsMode,
        theUnicodeToUTF8ErrorsMode,
        theTranslationService):

        if not theResult:
            return False

        if not theIdioma or not theBuffer:
            theResult[ 'status'] = cResultCondition_Internal_MissingParameter    
            return False

        unCodigoIdioma = theIdioma.getCodigoIdiomaEnGvSIG()
        
        from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fDateTimeNow

        unaStringToWrite  = '%s%s]\n%s%s\n' % ( 
            cPrefixLineaLenguaje,  
            unCodigoIdioma,
            cPrefixLineaTimestamp, 
            str( self.fDateTimeNow()),
        )
        
        if theCodificacionCaracteres == cEncodingUnicodeEscape:
            unStringToWriteEncoded, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                unaStringToWrite, 
                theTranslationService, 
                theSystemToUnicodeErrorsMode, 
            )
            
            if unEncodingErrorCondition:
                if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                    theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
                return False
        else: 
            unStringToWriteEncoded, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                unaStringToWrite, 
                theTranslationService, 
                theSystemToUnicodeErrorsMode, 
                theUnicodeToUTF8ErrorsMode
            )
            
            if unEncodingErrorCondition:
                if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                    theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
                elif unEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                    theResult[ 'header_error_codificacion_UnicodeToUTF'] = True    
                return False
            
        
        try:    
            theBuffer.write( unStringToWriteEncoded)
        except:
            theResult[ 'header_error_codificacion_Export'] = True 
            return False
           
        return True
    
    
                
    
    
          
            
    security.declarePrivate( 'fWriteTranslationResults_JavaProperties')    
    def fWriteTranslationResults_JavaProperties( self, 
        theBuffer, 
        theResult,
        theResultadosTraducciones, 
        theSourcesCadenasPorSimbolo,
        theModulosCadenasPorSimbolo,
        theCodificacionCaracteres,
        theEncodingErrorHandleMode, 
        theSystemToUnicodeErrorsMode, 
        theUnicodeToUTF8ErrorsMode, 
        theTranslationService):


        if not theResult:
            return False

        if not theBuffer:
            theResult[ 'status'] = cResultCondition_Internal_MissingParameter    
            return False
        
        unCatalogo = self.getCatalogo()
                
        # ######################################################################
        """Retrieve sources and module names for string symbols to export.
        
        """
        if ( not theSourcesCadenasPorSimbolo) or ( not theModulosCadenasPorSimbolo):
            
            for otroResultadoTraduccion in theResultadosTraducciones:
                otroSimboloCadena   = otroResultadoTraduccion[ 'getSimbolo']
                if otroSimboloCadena:
                    unaCadena = unCatalogo.fGetCadenaPorSimbolo( otroSimboloCadena)
                    if unaCadena:
                        unosSourcesCadena = unaCadena.getReferenciasFuentes()
                        theSourcesCadenasPorSimbolo[ otroSimboloCadena] = unosSourcesCadena

                        unosNombresModulosCadena = unaCadena.getNombresModulos()
                        theModulosCadenasPorSimbolo[ otroSimboloCadena] = unosNombresModulosCadena
        
        
        unHayError = False
        
        # ######################################################################
        """Loop over all string symbols to export.
        
        """
        for unResultadoTraduccion in theResultadosTraducciones:

            unHayErrorSimbolo        = False
            unHayErrorTraduccion     = False
            unHayErrorSources        = False
            unHayErrorSimbolo2       = False
            unHayErrorNombresModulos = False
            unHayErrorSimbolo3       = False
            
            
            unSimboloCadena   = unResultadoTraduccion[ 'getSimbolo']
            unSimboloCadenaEncoded = ''
            
            if not unSimboloCadena:
                unHayErrorSimbolo = True
                continue
            
            # ######################################################################
            """Encode string symbol.
            
            """              
            if theCodificacionCaracteres == cEncodingUnicodeEscape:
                unSimboloCadenaEncoded, unSimboloCadenaEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                    unSimboloCadena, 
                    theTranslationService, 
                    theSystemToUnicodeErrorsMode, 
                )
                
                if unSimboloCadenaEncodingErrorCondition or not unSimboloCadenaEncoded:
                    if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                        theResult[ 'simbolos_error_codificacion_SystemToUnicode'] = True    
                    return False
            else: 
                unSimboloCadenaEncoded, unSimboloCadenaEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                    unSimboloCadena, 
                    theTranslationService, 
                    theSystemToUnicodeErrorsMode, 
                    theUnicodeToUTF8ErrorsMode, 
                )
                if unSimboloCadenaEncodingErrorCondition or not unSimboloCadenaEncoded:
                    
                    if unSimboloCadenaEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                        theResult[ 'simbolos_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
                        
                    elif unSimboloCadenaEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                        theResult[ 'simbolos_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                
                    if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                        return ( unosSimbolosErroresCodificacion, unasTraduccionesErroresCodificacion,) 
                    else:
                        unHayErrorSimbolo = True
                        unHayError = True
                        
                        
            # ######################################################################
            """Encode translation into main language.
            
            """
            unaCadenaTraducida     = unResultadoTraduccion[ 'getCadenaTraducida']
            unaCadenaTraducidaEncoded = ''
            
            if unaCadenaTraducida:
                if theCodificacionCaracteres == cEncodingUnicodeEscape:
                    unaCadenaTraducidaEncoded, unaCadenaTraducidaEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                        unaCadenaTraducida, 
                        theTranslationService, 
                        theSystemToUnicodeErrorsMode, 
                    )
                    
                    if unaCadenaTraducidaEncodingErrorCondition or not unaCadenaTraducidaEncoded:
                        if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                            theResult[ 'simbolos_error_codificacion_SystemToUnicode'] = True    
                        return False
                else: 
                    
                    unaCadenaTraducidaEncoded, unaCadenaTraducidaEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                        unaCadenaTraducida, 
                        theTranslationService, 
                        theSystemToUnicodeErrorsMode, 
                        theUnicodeToUTF8ErrorsMode, 
                    )
                    if unaCadenaTraducidaEncodingErrorCondition or not unaCadenaTraducidaEncoded:
                        
                        if unaCadenaTraducidaEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                            theResult[ 'traducciones_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
        
                        elif unaCadenaTraducidaEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                            theResult[ 'traducciones_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                    
                        if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False
                        else:
                            unHayErrorTraduccion = True
                            unHayError =  True
             
                
                            

                        
            # ######################################################################
            """Encode sources.
            
            """
            unosSources = ''
            unosSourcesEncoded = ''
            
            unosSources        = theSourcesCadenasPorSimbolo.get( unSimboloCadena, '')
            if unosSources:
                
                if theCodificacionCaracteres == cEncodingUnicodeEscape:
                    unosSourcesEncoded, unosSourcesEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                        unosSources, 
                        theTranslationService, 
                        theSystemToUnicodeErrorsMode, 
                    )
                    
                    if unosSourcesEncodedEncodingErrorCondition or not unosSourcesEncoded:
                        if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                            theResult[ 'sources_error_codificacion_SystemToUnicode'] = True    
                        return False
                else: 
                
                    unosSourcesEncoded, unosSourcesEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                        unosSources, 
                        theTranslationService, 
                        theSystemToUnicodeErrorsMode, 
                        theUnicodeToUTF8ErrorsMode, 
                    )
                    if unosSourcesEncodedEncodingErrorCondition:
                        
                        unHayErrorSources = True
                        unHayError =  True
                        
                        if unosSourcesEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                            theResult[ 'sources_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
        
                        elif unosSourcesEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                            theResult[ 'sources_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                    
                        if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False                   
                                    
                
                
                
            # ######################################################################
            """Encode module names.
            
            """
            unosNombresModulos = ''
            unosNombresModulosEncoded = ''
            
            unosNombresModulos        = theModulosCadenasPorSimbolo.get( unSimboloCadena, '')
            if unosNombresModulos:
                
                if theCodificacionCaracteres == cEncodingUnicodeEscape:
                    unosNombresModulosEncoded, unosNombresModulosEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                        unosNombresModulos, 
                        theTranslationService, 
                        theSystemToUnicodeErrorsMode, 
                    )
                    
                    if unosNombresModulosEncodedEncodingErrorCondition or not unosNombresModulosEncoded:
                        if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                            theResult[ 'modules_error_codificacion_SystemToUnicode'] = True    
                        return False
                else: 
                
                    unosNombresModulosEncoded, unosNombresModulosEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                        unosNombresModulos, 
                        theTranslationService, 
                        theSystemToUnicodeErrorsMode, 
                        theUnicodeToUTF8ErrorsMode, 
                    )
                    if unosNombresModulosEncodedEncodingErrorCondition:
                        
                        unHayErrorNombresModulos = True
                        unHayError =  True
                        
                        if unosNombresModulosEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                            theResult[ 'modules_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
        
                        elif unosNombresModulosEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                            theResult[ 'modules_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                    
                        if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False                   
                                    
                                            
                            
                            
                
            # ######################################################################
            """Write line with string symbol and translation.
            
            """                        
            if ( not unHayErrorSimbolo) and unSimboloCadenaEncoded:
                
                try:    
                    theBuffer.write( unSimboloCadenaEncoded)
                except:
                    theResult[ 'simbolos_error_codificacion_Export'].append( unSimboloCadena)    
                    if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                        return False
                    else:
                        unHayErrorSimbolo = True
                        unHayError =  True
                    
                theBuffer.write( cPropertyNameValueSeparator )
                        
                if ( not unHayErrorTraduccion) and unaCadenaTraducidaEncoded:
                    try:    
                        theBuffer.write( unaCadenaTraducidaEncoded)
                    except:
                        theResult[ 'traducciones_error_codificacion_Export'].append( unSimboloCadena)    
                        if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False
                        else:
                            unHayErrorTraduccion = True
                            unHayError =  True
                
                theBuffer.write( "\n" )
                
                
                
                
                

            
                # ######################################################################
                """Write modules line with module names.
                
                """                        
                if ( not unHayErrorSimbolo) and ( not unHayErrorNombresModulos) and unosNombresModulosEncoded:
                    unHayErrorNombresModulosLabel = False
                    try:    
                        theBuffer.write( cPropertiesModulesLinePrefix)
                        
                    except:
                        if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False
                        else:
                            unHayErrorNombresModulosLabel = True
                            unHayError =  True
                            
                    if not unHayErrorNombresModulosLabel:
                        
                        try:    
                            theBuffer.write( unSimboloCadenaEncoded)
                        except:
                            theResult[ 'simbolos_error_codificacion_Export'].append( unSimboloCadena)    
                            if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False
                            else:
                                unHayErrorSimbolo2 = True
                                unHayError =  True
                        
                                
                        if not unHayErrorSimbolo2:        
                                
                            theBuffer.write( cPropertyNameValueSeparator )
    
                            
                            try:    
                                theBuffer.write( unosNombresModulos)
                                
                            except:
                                unHayErrorNombresModulos = True
                                if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                                    return False
                                else:
                                    unHayErrorNombresModulos = True
                                    unHayError =  True
                                    
                    theBuffer.write( cGNUgettextPOEntryLabel_AfterModules)
                    
                        
             
                                
                    
                # ######################################################################
                """Write sources line with module names.
                
                """                        
                if ( not unHayErrorSimbolo) and ( not unHayErrorSources) and unosSourcesEncoded:
                    unHayErrorSourcesLabel = False
                    try:    
                        theBuffer.write( cPropertiesSourcesLinePrefix)
                        
                    except:
                        if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False
                        else:
                            unHayErrorSourcesLabel = True
                            unHayError =  True
                            
                    if not unHayErrorSourcesLabel:
                        
                        try:    
                            theBuffer.write( unSimboloCadenaEncoded)
                        except:
                            theResult[ 'simbolos_error_codificacion_Export'].append( unSimboloCadena)    
                            if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False
                            else:
                                unHayErrorSimbolo3 = True
                                unHayError =  True
                        
                        if not unHayErrorSimbolo3:     
                            
                            theBuffer.write( cPropertyNameValueSeparator )
    
                            
                            try:    
                                theBuffer.write( unosSources)
                                
                            except:
                                unHayErrorSources = True
                                if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                                    return False
                                else:
                                    unHayErrorSources = True
                                    unHayError =  True
                                
                    theBuffer.write( cGNUgettextPOEntryLabel_AfterSourceFileNames)
                                
                
                

        return not unHayError        
    
    
    

     
    security.declarePrivate( 'fContenidoFicheroExportacionIdiomaModulo_JavaProperties')    
    def fContenidoFicheroExportacionIdiomaModulo_JavaProperties( self, 
        theIdioma, 
        theNombreModulo, 
        theCodificacionCaracteres, 
        theResultadosTraducciones, 
        theSourcesCadenasPorSimbolo,
        theModulosCadenasPorSimbolo,
        theEncodingErrorHandleMode,
        theEncodedFileErrorsMode,
        theSystemToUnicodeErrorsMode,
        theUnicodeToUTF8ErrorsMode,
        theTranslationService,
        theParentExecutionRecord    =None):
        

        unExecutionRecord = self.fStartExecution( 'method',  'fContenidoFicheroExportacionIdiomaModulo_JavaProperties', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True,}, 'Language %s     Module %s' % (((theIdioma and theIdioma.getCodigoIdiomaEnGvSIG()) or '?'),  theNombreModulo or '?'))
        try:
            unResult = self.fNewVoidResultFicheroExportacionProperties()
            unResult[ 'encoding']                       = theCodificacionCaracteres
            unResult[ 'encoding_error_handle_mode']     = theEncodingErrorHandleMode
            unResult[ 'encoded_file_errors_mode']       = theEncodedFileErrorsMode
            unResult[ 'system_to_unicode_errors_mode']  = theSystemToUnicodeErrorsMode
            unResult[ 'unicode_to_utf8_errors_mode']    = theUnicodeToUTF8ErrorsMode
            
            try:
                
                 
                if not theIdioma or not theCodificacionCaracteres:
                    unResult[ 'status'] = cResultCondition_Internal_MissingParameter
                    return unResult
                
                unBufferResultado = StringIO()
                        
                unaCodificacionCaracteres = theCodificacionCaracteres
                unaCodificacionEntrada    = cEncodingUTF8
                
                if unaCodificacionCaracteres == cEncodingUnicodeEscape:
                    unaCodificacionCaracteres = cEncodingASCII
                    unaCodificacionEntrada    = cEncodingASCII
                    
                
                unEncodedFile = None
                try:
                    unEncodedFile = CODECS_EncodedFile( unBufferResultado, unaCodificacionEntrada, unaCodificacionCaracteres, errors=theEncodedFileErrorsMode)
                except:
                    None
                
                if not unEncodedFile:
                    unResult[ 'status'] = cResultCondition_Encoding_NotAvailable
                    return unResult
        
                anErrorInFile = False
                
                if not self.fWriteHeader_JavaProperties( 
                    unEncodedFile, 
                    unResult,
                    theIdioma, 
                    theNombreModulo, 
                    theCodificacionCaracteres,
                    theEncodingErrorHandleMode, 
                    theSystemToUnicodeErrorsMode,
                    theUnicodeToUTF8ErrorsMode,
                    theTranslationService):
    
                    anErrorInFile = True
                    
                    unResult[ 'status'] = cResultCondition_Encoding_ErrorInHeader
                    if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                        unResult.update( {
                            'contenido':                    unBufferResultado.getvalue(),
                        })
                        return unResult
                    
                    
                if not theResultadosTraducciones:
                    unResult[ 'success'] = True
                    unResult[ 'status'] = cResultCondition_NoTranslationsToExport
                    unResult.update( {
                        'contenido':                    unBufferResultado.getvalue(),
                    })
                    return unResult
                
                
                if not self.fWriteTranslationResults_JavaProperties( 
                    unEncodedFile, 
                    unResult,
                    theResultadosTraducciones,
                    theSourcesCadenasPorSimbolo,
                    theModulosCadenasPorSimbolo,
                    theCodificacionCaracteres,
                    theEncodingErrorHandleMode,
                    theSystemToUnicodeErrorsMode,
                    theUnicodeToUTF8ErrorsMode,
                    theTranslationService):
                    
                    anErrorInFile = True
                    
                    if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                        unResult[ 'status'] = cResultCondition_Encoding_ErrorInTranslations
                        unResult.update( {
                            'contenido':                    unBufferResultado.getvalue(),
                        })
                        return unResult
                
                
                 
                unResult.update( {
                    'success':    ( not anErrorInFile) or ( theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_IgnoreAndContinue, cEncodingErrorHandleMode_ReplaceAndContinue, cEncodingErrorHandleMode_XMLReplaceAndContinue , cEncodingErrorHandleMode_BackslashReplaceAndContinue,]), 
                    'contenido':  unBufferResultado.getvalue(),
                })

                
                return unResult  
            
            finally:
                unResult[ 'total_encoding_errors']  = \
                    (( unResult.get( 'header_error_codificacion_SystemToUnicode', False) and 1) or 0) + \
                    (( unResult.get( 'header_error_codificacion_UnicodeToUTF', False) and 1) or 0) + \
                    (( unResult.get( 'header_error_codificacion_Export', False) and 1) or 0) + \
                    len( unResult.get( 'simbolos_error_codificacion_SystemToUnicode', [])) + \
                    len( unResult.get( 'simbolos_error_codificacion_UnicodeToUTF', [])) + \
                    len( unResult.get( 'simbolos_error_codificacion_Export', [])) + \
                    len( unResult.get( 'traducciones_error_codificacion_SystemToUnicode', [])) + \
                    len( unResult.get( 'traducciones_error_codificacion_UnicodeToUTF', [])) + \
                    len( unResult.get( 'traducciones_error_codificacion_Export', []))
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

           



     
    security.declarePrivate( 'fContenidoFicheroExportacionIdiomaModuloNoEspecificado_JavaProperties')    
    def fContenidoFicheroExportacionIdiomaModuloNoEspecificado_JavaProperties( self, 
        theIdioma, 
        theNombreModulo, 
        theCodificacionCaracteres, 
        theResultadosTraducciones, 
        theSourcesCadenasPorSimbolo,
        theModulosCadenasPorSimbolo,
        theEncodingErrorHandleMode,
        theEncodedFileErrorsMode,
        theSystemToUnicodeErrorsMode,
        theUnicodeToUTF8ErrorsMode,
        theTranslationService,
        theParentExecutionRecord    =None):

        unExecutionRecord = self.fStartExecution( 'method',  'fContenidoFicheroExportacionIdiomaModuloNoEspecificado_JavaProperties', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True,}, 'language %s    unspecified Module' % ((theIdioma and theIdioma.getCodigoIdiomaEnGvSIG()) or '?'))
        try:
            unResult = self.fContenidoFicheroExportacionIdiomaModulo_JavaProperties( 
                theIdioma, 
                theNombreModulo, 
                theCodificacionCaracteres, 
                theResultadosTraducciones, 
                theSourcesCadenasPorSimbolo,
                theModulosCadenasPorSimbolo,
                theEncodingErrorHandleMode,
                theEncodedFileErrorsMode,
                theSystemToUnicodeErrorsMode,
                theUnicodeToUTF8ErrorsMode,
                theTranslationService,
                theParentExecutionRecord    =unExecutionRecord
            )
            return unResult  
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
        
            

     
    security.declarePrivate( 'fContenidoFicheroExportacionIdiomaTodosModulos_JavaProperties')    
    def fContenidoFicheroExportacionIdiomaTodosModulos_JavaProperties( self, 
        theIdioma, 
        theNombreModulo, 
        theCodificacionCaracteres, 
        theResultadosTraducciones, 
        theSourcesCadenasPorSimbolo,
        theModulosCadenasPorSimbolo,
        theEncodingErrorHandleMode,
        theEncodedFileErrorsMode,
        theSystemToUnicodeErrorsMode,
        theUnicodeToUTF8ErrorsMode,
        theTranslationService,
        theParentExecutionRecord    =None):

        unExecutionRecord = self.fStartExecution( 'method',  'fContenidoFicheroExportacionIdiomaTodosModulos_JavaProperties', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True,}, 'idioma %s    all modules' % ((theIdioma and theIdioma.getCodigoIdiomaEnGvSIG()) or '?'))
        try:
            unResult = self.fContenidoFicheroExportacionIdiomaModulo_JavaProperties( 
                theIdioma, 
                theNombreModulo, 
                theCodificacionCaracteres, 
                theResultadosTraducciones, 
                theSourcesCadenasPorSimbolo,
                theModulosCadenasPorSimbolo,
                theEncodingErrorHandleMode,
                theEncodedFileErrorsMode,
                theSystemToUnicodeErrorsMode,
                theUnicodeToUTF8ErrorsMode,
                theTranslationService,
                theParentExecutionRecord    =unExecutionRecord
            )
            return unResult  
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
        
                        
     
     
    
    
    
    # ####################################################
    #  GNUgettextPO output
    # ####################################################
 
   
    security.declarePrivate( 'fWriteHeader_GNUgettextPO')    
    def fWriteHeader_GNUgettextPO( self, 
        theBuffer, 
        theResult,
        theIdioma, 
        theNombreModulo, 
        theEncodingName, 
        theEncodingErrorHandleMode, 
        theSystemToUnicodeErrorsMode,
        theUnicodeToUTF8ErrorsMode,
        theTranslationService):
        
        if theEncodingName == cEncodingUnicodeEscape:
            return self.fWriteHeader_GNUgettextPO_UnicodeEscape( 
                theBuffer, 
                theResult,
                theIdioma, 
                theNombreModulo, 
                theEncodingName, 
                theEncodingErrorHandleMode, 
                theSystemToUnicodeErrorsMode,
                theUnicodeToUTF8ErrorsMode,
                theTranslationService,
            )
   
        return self.fWriteHeader_GNUgettextPO_Encoding( 
            theBuffer, 
            theResult,
            theIdioma, 
            theNombreModulo, 
            theEncodingName, 
            theEncodingErrorHandleMode, 
            theSystemToUnicodeErrorsMode,
            theUnicodeToUTF8ErrorsMode,
            theTranslationService,
        )

    
    
    
    
    security.declarePrivate( 'fWriteHeader_GNUgettextPO_Encoding')    
    def fWriteHeader_GNUgettextPO_Encoding( self, 
        theBuffer, 
        theResult,
        theIdioma, 
        theNombreModulo, 
        theEncodingName, 
        theEncodingErrorHandleMode, 
        theSystemToUnicodeErrorsMode,
        theUnicodeToUTF8ErrorsMode,
        theTranslationService):


        if not theResult:
            return False

        if not theIdioma or not theBuffer:
            theResult[ 'status'] = cResultCondition_Internal_MissingParameter    
            return False

        
        unErrorEnHeader = False
        
        unCodigoIdioma = theIdioma.getCodigoIdiomaEnGvSIG()
        
        
        unAhora = self.fDateTimeNow()
        unOffset = int( unAhora.tzoffset() / 3600)
        unOffsetSign = '+'
        if unOffset < 0:
            unOffsetSign = '-'
    
        unPOTimestampUTF8 = ''
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
            '%4.4d-%02d-%02d %02d:%02d%s%02d00' % ( unAhora.year(), unAhora.month(), unAhora.day(), unAhora.hour(), unAhora.minute(), unOffsetSign, unOffset, ), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
            theUnicodeToUTF8ErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            elif unEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                theResult[ 'header_error_codificacion_UnicodeToUTF'] = True    
            if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unPOTimestampUTF8 = unEncodedString
        
            
        unNombreProductoUTF8 = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
            self.fQuoteForGNUgettextPO( self.getNombreProducto()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
            theUnicodeToUTF8ErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            elif unEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                theResult[ 'header_error_codificacion_UnicodeToUTF'] = True    
            if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unNombreProductoUTF8 = unEncodedString
            
            
        unLastTranslatorUTF8 = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
            self.fQuoteForGNUgettextPO( theIdioma.getEquipoTraductor()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
            theUnicodeToUTF8ErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            elif unEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                theResult[ 'header_error_codificacion_UnicodeToUTF'] = True    
            if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unLastTranslatorUTF8 = unEncodedString
            
        unLanguageTeamUTF8 = unLastTranslatorUTF8
            
        unCharSetUTF8 = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
            self.fQuoteForGNUgettextPO( theEncodingName), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
            theUnicodeToUTF8ErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            elif unEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                theResult[ 'header_error_codificacion_UnicodeToUTF'] = True    
            if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unCharSetUTF8  = unEncodedString
            
                 
            
        unaCodificacionTransferenciaContenidoUTF8 = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
            self.fQuoteForGNUgettextPO( theIdioma.getCodificacionTransferenciaContenido()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
            theUnicodeToUTF8ErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            elif unEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                theResult[ 'header_error_codificacion_UnicodeToUTF'] = True    
            if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unaCodificacionTransferenciaContenidoUTF8 = unEncodedString
            
        unasFormasPluralesUTF8 = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
            self.fQuoteForGNUgettextPO( theIdioma.getFormasPlurales()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
            theUnicodeToUTF8ErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            elif unEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                theResult[ 'header_error_codificacion_UnicodeToUTF'] = True    
            if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unasFormasPluralesUTF8 = unEncodedString
            
        unCodigoIdiomaUTF8 = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
            unCodigoIdioma, 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
            theUnicodeToUTF8ErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            elif unEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                theResult[ 'header_error_codificacion_UnicodeToUTF'] = True    
            if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unCodigoIdiomaUTF8 = unEncodedString
            
        unNombreNativoIdiomaUTF8 = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
            self.fQuoteForGNUgettextPO( theIdioma.getNombreNativoDeIdioma()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
            theUnicodeToUTF8ErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            elif unEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                theResult[ 'header_error_codificacion_UnicodeToUTF'] = True    
            if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unNombreNativoIdiomaUTF8 = unEncodedString
            
             
        unasCodificacionesPreferidasUTF8 = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
            self.fQuoteForGNUgettextPO( theIdioma.getCodificacionesPreferidas()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
            theUnicodeToUTF8ErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            elif unEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                theResult[ 'header_error_codificacion_UnicodeToUTF'] = True    
            if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unasCodificacionesPreferidasUTF8 = unEncodedString
             
        unDominioUTF8 = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
            self.fQuoteForGNUgettextPO( theNombreModulo or self.getDominioPorDefecto()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
            theUnicodeToUTF8ErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            elif unEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                theResult[ 'header_error_codificacion_UnicodeToUTF'] = True    
            if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unDominioUTF8 = unEncodedString
            
        unFallbackUTF8 = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
            self.fQuoteForGNUgettextPO( theIdioma.getFallbackDeIdiomas()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
            theUnicodeToUTF8ErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            elif unEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                theResult[ 'header_error_codificacion_UnicodeToUTF'] = True    
            if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unFallbackUTF8 = unEncodedString
               
            
            
        try:    
            theBuffer.write( cGNUgettextPOHeaderTemplateString_Top)
        except:
            theResult[ 'header_error_codificacion_Export'] = True    
            if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                return False
            
        
        theBuffer.write( cGNUgettextPOHeaderLabel_ProjectIdVersion)
        if unNombreProductoUTF8:
            try:    
                theBuffer.write( unNombreProductoUTF8)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
            
        theBuffer.write( cGNUgettextPOHeaderLabel_POTCreationDate)
        if unPOTimestampUTF8:
            try:    
                theBuffer.write( unPOTimestampUTF8)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)

        theBuffer.write( cGNUgettextPOHeaderLabel_PORevisionDate)
        if unPOTimestampUTF8:
            try:    
                theBuffer.write( unPOTimestampUTF8)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
        
        theBuffer.write( cGNUgettextPOHeaderLabel_LastTranslator)
        if unLastTranslatorUTF8:
            try:    
                theBuffer.write( unLastTranslatorUTF8)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
        
        theBuffer.write( cGNUgettextPOHeaderLabel_LanguageTeam)
        if unLanguageTeamUTF8:
            try:    
                theBuffer.write( unLanguageTeamUTF8)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
        
        theBuffer.write( cGNUgettextPOHeaderLabel_MIMEVersion)
        theBuffer.write( cGNUgettextPOHeader_AfterValue)

        theBuffer.write( cGNUgettextPOHeaderLabel_ContentType)
        if unCharSetUTF8:
            try:    
                theBuffer.write( unCharSetUTF8)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
             
        theBuffer.write( cGNUgettextPOHeaderLabel_ContentTransferEncoding)
        if unaCodificacionTransferenciaContenidoUTF8:
            try:    
                theBuffer.write( unaCodificacionTransferenciaContenidoUTF8)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
             
        theBuffer.write( cGNUgettextPOHeaderLabel_PluralForms)
        if unasFormasPluralesUTF8:
            try:    
                theBuffer.write( unasFormasPluralesUTF8)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
             
        theBuffer.write( cGNUgettextPOHeaderLabel_LanguageCode)
        if unCodigoIdiomaUTF8:
            try:    
                theBuffer.write( unCodigoIdiomaUTF8)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
             
        theBuffer.write( cGNUgettextPOHeaderLabel_LanguageName)
        if unNombreNativoIdiomaUTF8:
            try:    
                theBuffer.write( unNombreNativoIdiomaUTF8)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
             
        theBuffer.write( cGNUgettextPOHeaderLabel_PreferredEncodings)
        if unasCodificacionesPreferidasUTF8:
            try:    
                theBuffer.write( unasCodificacionesPreferidasUTF8)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
             
        theBuffer.write( cGNUgettextPOHeaderLabel_Domain)
        if unDominioUTF8:
            try:    
                theBuffer.write( unDominioUTF8)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)

        theBuffer.write( '\n')
             
        return not unErrorEnHeader

            

     

    security.declarePrivate( 'fWriteHeader_GNUgettextPO_UnicodeEscape')    
    def fWriteHeader_GNUgettextPO_UnicodeEscape( self, 
        theBuffer, 
        theResult,
        theIdioma, 
        theNombreModulo, 
        theEncodingName, 
        theEncodingErrorHandleMode, 
        theSystemToUnicodeErrorsMode,
        theUnicodeToUTF8ErrorsMode,
        theTranslationService):


        if not theResult:
            return False

        if not theIdioma or not theBuffer:
            theResult[ 'status'] = cResultCondition_Internal_MissingParameter    
            return False

        
        unErrorEnHeader = False
        
        unCodigoIdioma = theIdioma.getCodigoIdiomaEnGvSIG()
                
        unAhora = self.fDateTimeNow()
        unOffset = int( unAhora.tzoffset() / 3600)
        unOffsetSign = '+'
        if unOffset < 0:
            unOffsetSign = '-'
    
        unPOTimestampEncoded = ''
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
            '%4.4d-%02d-%02d %02d:%02d%s%02d00' % ( unAhora.year(), unAhora.month(), unAhora.day(), unAhora.hour(), unAhora.minute(), unOffsetSign, unOffset, ), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unPOTimestampEncoded = unEncodedString
        
            
        unNombreProductoEncoded = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
            self.fQuoteForGNUgettextPO( self.getNombreProducto()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unNombreProductoEncoded = unEncodedString
            
            
        unLastTranslatorEncoded = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
            self.fQuoteForGNUgettextPO( theIdioma.getEquipoTraductor()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unLastTranslatorEncoded = unEncodedString
            
        unLanguageTeamEncoded = unLastTranslatorEncoded
            
        #unCharSetEncoded = '' 
        #unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
            #self.fQuoteForGNUgettextPO( theEncodingName), 
            #theTranslationService, 
            #theSystemToUnicodeErrorsMode, 
        #)
        #if unEncodingErrorCondition:
            #unErrorEnHeader = True
            #if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                #theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            #if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                #return False
        #else:    
            #unCharSetEncoded  = unEncodedString
            
                 
            
        unaCodificacionTransferenciaContenidoEncoded = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
            self.fQuoteForGNUgettextPO( theIdioma.getCodificacionTransferenciaContenido()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unaCodificacionTransferenciaContenidoEncoded = unEncodedString
            
        unasFormasPluralesEncoded = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
            self.fQuoteForGNUgettextPO( theIdioma.getFormasPlurales()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unasFormasPluralesEncoded = unEncodedString
            
        unCodigoIdiomaEncoded = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
            unCodigoIdioma, 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unCodigoIdiomaEncoded = unEncodedString
            
        unNombreNativoIdiomaEncoded = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
            self.fQuoteForGNUgettextPO( theIdioma.getNombreNativoDeIdioma()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unNombreNativoIdiomaEncoded = unEncodedString
            
             
        unasCodificacionesPreferidasEncoded = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
            self.fQuoteForGNUgettextPO( theIdioma.getCodificacionesPreferidas()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unasCodificacionesPreferidasEncoded = unEncodedString
             
        unDominioEncoded = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
            self.fQuoteForGNUgettextPO( theNombreModulo or self.getDominioPorDefecto()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unDominioEncoded = unEncodedString
            
        unFallbackEncoded = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
            self.fQuoteForGNUgettextPO( theIdioma.getFallbackDeIdiomas()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unFallbackEncoded = unEncodedString
               
            
            
        try:    
            theBuffer.write( cGNUgettextPOHeaderTemplateString_Top)
        except:
            theResult[ 'header_error_codificacion_Export'] = True    
            if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                return False
            
        
        theBuffer.write( cGNUgettextPOHeaderLabel_ProjectIdVersion)
        if unNombreProductoEncoded:
            try:    
                theBuffer.write( unNombreProductoEncoded)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
            
        theBuffer.write( cGNUgettextPOHeaderLabel_POTCreationDate)
        if unPOTimestampEncoded:
            try:    
                theBuffer.write( unPOTimestampEncoded)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)

        theBuffer.write( cGNUgettextPOHeaderLabel_PORevisionDate)
        if unPOTimestampEncoded:
            try:    
                theBuffer.write( unPOTimestampEncoded)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
        
        theBuffer.write( cGNUgettextPOHeaderLabel_LastTranslator)
        if unLastTranslatorEncoded:
            try:    
                theBuffer.write( unLastTranslatorEncoded)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
        
        theBuffer.write( cGNUgettextPOHeaderLabel_LanguageTeam)
        if unLanguageTeamEncoded:
            try:    
                theBuffer.write( unLanguageTeamEncoded)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
        
        theBuffer.write( cGNUgettextPOHeaderLabel_MIMEVersion)
        theBuffer.write( cGNUgettextPOHeader_AfterValue)

        theBuffer.write( cGNUgettextPOHeaderLabel_ContentType)
        try:    
            theBuffer.write( cEncodingASCII)
        except:
            theResult[ 'header_error_codificacion_Export'] = True    
            if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
             
        theBuffer.write( cGNUgettextPOHeaderLabel_ContentTransferEncoding)
        if unaCodificacionTransferenciaContenidoEncoded:
            try:    
                theBuffer.write( unaCodificacionTransferenciaContenidoEncoded)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
             
        theBuffer.write( cGNUgettextPOHeaderLabel_PluralForms)
        if unasFormasPluralesEncoded:
            try:    
                theBuffer.write( unasFormasPluralesEncoded)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
             
        theBuffer.write( cGNUgettextPOHeaderLabel_LanguageCode)
        if unCodigoIdiomaEncoded:
            try:    
                theBuffer.write( unCodigoIdiomaEncoded)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
             
        theBuffer.write( cGNUgettextPOHeaderLabel_LanguageName)
        if unNombreNativoIdiomaEncoded:
            try:    
                theBuffer.write( unNombreNativoIdiomaEncoded)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
             
        theBuffer.write( cGNUgettextPOHeaderLabel_PreferredEncodings)
        if unasCodificacionesPreferidasEncoded:
            try:    
                theBuffer.write( unasCodificacionesPreferidasEncoded)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
             
        theBuffer.write( cGNUgettextPOHeaderLabel_Domain)
        if unDominioEncoded:
            try:    
                theBuffer.write( unDominioEncoded)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)

        theBuffer.write( '\n')
             
        return not unErrorEnHeader

    
    
    
    
    security.declarePrivate( 'fQuoteForGNUgettextPO')    
    def fQuoteForGNUgettextPO( self, theString):
        if not theString:
            return ''
        return theString.replace( '"', '\"')
    
   
    
  
    security.declarePrivate( 'fWriteTranslationResults_GNUgettextPO')    
    def fWriteTranslationResults_GNUgettextPO( self, 
        theBuffer, 
        theResult,
        theResultadosTraducciones, 
        theResultadosTraduccionesReferencia, 
        theSourcesCadenasPorSimbolo,
        theModulosCadenasPorSimbolo,
        theCodificacionCaracteres,
        theEncodingErrorHandleMode, 
        theSystemToUnicodeErrorsMode, 
        theUnicodeToUTF8ErrorsMode, 
        theTranslationService):


        if not theResult:
            return False

        if not theBuffer:
            theResult[ 'status'] = cResultCondition_Internal_MissingParameter    
            return False
        
        
        unCatalogo = self.getCatalogo()
        
        # ######################################################################
        """Retrieve translations to reference language for string symbols to export.
        
        """
        unosResultadosTraduccionesReferencia = { }
        if theResultadosTraduccionesReferencia:
            for unResultadoTraduccionReferencia in theResultadosTraduccionesReferencia:
                unSimboloCadena           = unResultadoTraduccionReferencia[ 'getSimbolo']
                unosResultadosTraduccionesReferencia[ unSimboloCadena] = unResultadoTraduccionReferencia

                
                
                
        # ######################################################################
        """Retrieve sources and module names for string symbols to export.
        
        """
        if ( not theSourcesCadenasPorSimbolo) or ( not theModulosCadenasPorSimbolo):
            
            for otroResultadoTraduccion in theResultadosTraducciones:
                otroSimboloCadena   = otroResultadoTraduccion[ 'getSimbolo']
                if otroSimboloCadena:
                    unaCadena = unCatalogo.fGetCadenaPorSimbolo( otroSimboloCadena)
                    if unaCadena:
                        unosSourcesCadena = unaCadena.getReferenciasFuentes()
                        theSourcesCadenasPorSimbolo[ otroSimboloCadena] = unosSourcesCadena

                        unosNombresModulosCadena = unaCadena.getNombresModulos()
                        theModulosCadenasPorSimbolo[ otroSimboloCadena] = unosNombresModulosCadena
              
                        
                        
        unHayError = False
                        
        # ######################################################################
        """Loop over all string symbols to export.
        
        """
        for unResultadoTraduccion in theResultadosTraducciones:

            unHayErrorSimbolo               = False
            unHayErrorTraduccion            = False
            unHayErrorTraduccionReferencia  = False
            unHayErrorSources               = False
            unHayErrorNombresModulos        = False
            
            
            unSimboloCadena   = unResultadoTraduccion[ 'getSimbolo']
            unSimboloCadenaEncoded = ''
            
            if not unSimboloCadena:
                unHayErrorSimbolo = True
                continue
            
            # ######################################################################
            """Encode string symbol.
            
            """              
            if theCodificacionCaracteres == cEncodingUnicodeEscape:
                unSimboloCadenaEncoded, unSimboloCadenaEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                    unSimboloCadena, 
                    theTranslationService, 
                    theSystemToUnicodeErrorsMode, 
                )
                
                if unSimboloCadenaEncodingErrorCondition or not unSimboloCadenaEncoded:
                    if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                        theResult[ 'simbolos_error_codificacion_SystemToUnicode'] = True    
                    return False
            else: 
                unSimboloCadenaEncoded, unSimboloCadenaEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                    unSimboloCadena, 
                    theTranslationService, 
                    theSystemToUnicodeErrorsMode, 
                    theUnicodeToUTF8ErrorsMode, 
                )
                if unSimboloCadenaEncodingErrorCondition or not unSimboloCadenaEncoded:
                    
                    unHayErrorSimbolo = True
                    unHayError        = True
                    
                    if unSimboloCadenaEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                        theResult[ 'simbolos_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
                        
                    elif unSimboloCadenaEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                        theResult[ 'simbolos_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                
                    if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                        return ( unosSimbolosErroresCodificacion, unasTraduccionesErroresCodificacion,) 

                         
            # ######################################################################
            """Encode translation into main language.
            
            """
            unaCadenaTraducida     = unResultadoTraduccion[ 'getCadenaTraducida']
            unaCadenaTraducidaEncoded = ''
            
            if unaCadenaTraducida:
                if theCodificacionCaracteres == cEncodingUnicodeEscape:
                    unaCadenaTraducidaEncoded, unaCadenaTraducidaEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                        unaCadenaTraducida, 
                        theTranslationService, 
                        theSystemToUnicodeErrorsMode, 
                    )
                    
                    if unaCadenaTraducidaEncodingErrorCondition or not unaCadenaTraducidaEncoded:
                        if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                            theResult[ 'simbolos_error_codificacion_SystemToUnicode'] = True    
                        return False
                else: 
                    unaCadenaTraducidaEncoded, unaCadenaTraducidaEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                        unaCadenaTraducida, 
                        theTranslationService, 
                        theSystemToUnicodeErrorsMode, 
                        theUnicodeToUTF8ErrorsMode, 
                    )
                    if unaCadenaTraducidaEncodingErrorCondition or not unaCadenaTraducidaEncoded:
                        
                        unHayErrorTraduccion = True
                        unHayError =  True
                        
                        if unaCadenaTraducidaEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                            theResult[ 'traduccionesRefrencia_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
        
                        elif unaCadenaTraducidaEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                            theResult[ 'traduccionesReferencia_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                    
                        if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False

             
            # ######################################################################
            """Encode translation into reference language.
            
            """
            unaCadenaTraducidaReferencia = ''
            unaCadenaTraducidaReferenciaEncoded = ''
            
            unResultadoTraduccionReferencia  = unosResultadosTraduccionesReferencia.get( unSimboloCadena, {})
            if unResultadoTraduccionReferencia:
                unaCadenaTraducidaReferencia     = unResultadoTraduccionReferencia[ 'getCadenaTraducida']
                if unaCadenaTraducidaReferencia:
                    
                    if theCodificacionCaracteres == cEncodingUnicodeEscape:
                        unaCadenaTraducidaReferenciaEncoded, unaCadenaTraducidaReferenciaEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                            unaCadenaTraducidaReferencia, 
                            theTranslationService, 
                            theSystemToUnicodeErrorsMode, 
                        )
                        
                        if unaCadenaTraducidaReferenciaEncodingErrorCondition or not unaCadenaTraducidaReferenciaEncoded:
                            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                                theResult[ 'traducciones_error_codificacion_SystemToUnicode'] = True    
                            return False
                    else: 
                    
                        unaCadenaTraducidaReferenciaEncoded, unaCadenaTraducidaReferenciaEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                            unaCadenaTraducidaReferencia, 
                            theTranslationService, 
                            theSystemToUnicodeErrorsMode, 
                            theUnicodeToUTF8ErrorsMode, 
                        )
                        if unaCadenaTraducidaReferenciaEncodingErrorCondition:
                            
                            unHayErrorTraduccionReferencia = True
                            unHayError =  True
                            
                            if unaCadenaTraducidaReferenciaEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                                theResult[ 'traducciones_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
            
                            elif unaCadenaTraducidaReferenciaEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                                theResult[ 'traducciones_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                        
                            if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False                   
                        
                        
            # ######################################################################
            """Encode sources.
            
            """
            unosSources = ''
            unosSourcesEncoded = ''
            
            unosSources        = theSourcesCadenasPorSimbolo.get( unSimboloCadena, '')
            if unosSources:
                
                if theCodificacionCaracteres == cEncodingUnicodeEscape:
                    unosSourcesEncoded, unosSourcesEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                        unosSources, 
                        theTranslationService, 
                        theSystemToUnicodeErrorsMode, 
                    )
                    
                    if unosSourcesEncodedEncodingErrorCondition or not unosSourcesEncoded:
                        if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                            theResult[ 'sources_error_codificacion_SystemToUnicode'] = True    
                        return False
                else: 
                
                    unosSourcesEncoded, unosSourcesEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                        unosSources, 
                        theTranslationService, 
                        theSystemToUnicodeErrorsMode, 
                        theUnicodeToUTF8ErrorsMode, 
                    )
                    if unosSourcesEncodedEncodingErrorCondition:
                        
                        unHayErrorSources = True
                        unHayError =  True
                        
                        if unosSourcesEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                            theResult[ 'sources_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
        
                        elif unosSourcesEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                            theResult[ 'sources_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                    
                        if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False                   
                                    
                
                
                
            # ######################################################################
            """Encode module names.
            
            """
            unosNombresModulos = ''
            unosNombresModulosEncoded = ''
            
            unosNombresModulos        = theModulosCadenasPorSimbolo.get( unSimboloCadena, '')
            if unosNombresModulos:
                
                if theCodificacionCaracteres == cEncodingUnicodeEscape:
                    unosNombresModulosEncoded, unosNombresModulosEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                        unosNombresModulos, 
                        theTranslationService, 
                        theSystemToUnicodeErrorsMode, 
                    )
                    
                    if unosNombresModulosEncodedEncodingErrorCondition or not unosNombresModulosEncoded:
                        if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                            theResult[ 'modules_error_codificacion_SystemToUnicode'] = True    
                        return False
                else: 
                
                    unosNombresModulosEncoded, unosNombresModulosEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                        unosNombresModulos, 
                        theTranslationService, 
                        theSystemToUnicodeErrorsMode, 
                        theUnicodeToUTF8ErrorsMode, 
                    )
                    if unosNombresModulosEncodedEncodingErrorCondition:
                        
                        unHayErrorNombresModulos = True
                        unHayError =  True
                        
                        if unosNombresModulosEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                            theResult[ 'modules_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
        
                        elif unosNombresModulosEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                            theResult[ 'modules_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                    
                        if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False                   
                                    
                
                         
                        
                        
            
            # ######################################################################
            """Write Default line with translation into reference language.
            
            """                        
            unHayErrorDefaultLabel = False        
            try:    
                theBuffer.write( cGNUgettextPOEntryLabel_Default)
            except:
                unHayErrorDefaultLabel = True
                if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                    return False
                else:
                    unHayError =  True
                    
            if ( not unHayErrorDefaultLabel) and ( not unHayErrorTraduccionReferencia) and unaCadenaTraducidaReferenciaEncoded:
                try:    
                    theBuffer.write( unaCadenaTraducidaReferenciaEncoded)
                except:
                    theResult[ 'traduccionesReferencia_error_codificacion_Export'].append( unSimboloCadena)    
                    if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                        return False
                    else:
                        unHayErrorTraduccionReferencia = True
                        unHayError =  True
                     
            theBuffer.write( cGNUgettextPOEntryLabel_AfterDefault)
                    
            
            
            
            
            # ######################################################################
            """Write modules line with module names.
            
            """                        
            if ( not unHayErrorNombresModulos) and  unosNombresModulosEncoded:
                unHayErrorNombresModulosLabel = False
                try:    
                    theBuffer.write( cGNUgettextPOEntryLabel_Modules)
                    
                except:
                    if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                        return False
                    else:
                        unHayErrorNombresModulosLabel = True
                        unHayError =  True
                        
                if not unHayErrorNombresModulosLabel:
                    try:    
                        theBuffer.write( unosNombresModulos)
                        
                    except:
                        unHayErrorNombresModulos = True
                        if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False
                        else:
                            unHayErrorNombresModulos = True
                            unHayError =  True
                            
                    theBuffer.write( cGNUgettextPOEntryLabel_AfterModules)
                
                    
         
                            
                
            # ######################################################################
            """Write sources line with module names.
            
            """                        
            if ( not unHayErrorSources) and unosSourcesEncoded:
                unHayErrorSourcesLabel = False
                try:    
                    theBuffer.write( cGNUgettextPOEntryLabel_SourceFileNames)
                    
                except:
                    if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                        return False
                    else:
                        unHayErrorSourcesLabel = True
                        unHayError =  True
                        
                if not unHayErrorSourcesLabel:
                    try:    
                        theBuffer.write( unosSources)
                        
                    except:
                        unHayErrorSources = True
                        if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False
                        else:
                            unHayErrorSources = True
                            unHayError =  True
                            
                    theBuffer.write( cGNUgettextPOEntryLabel_AfterSourceFileNames)
                            
            
                    
                    
            # ######################################################################
            """Write string symbol line.
            
            """                        
            unHayErrorSimboloLabel = False   
            try:    
                theBuffer.write( cGNUgettextPOEntryLabel_msgid)
            except:
                unHayErrorSimboloLabel = True
                if  unHayErrorSimbolo in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                    return False
                else:
                    unHayError =  True

            if ( not unHayErrorSimboloLabel) and ( not unHayErrorSimbolo) and unSimboloCadenaEncoded:
                try:    
                    theBuffer.write( unSimboloCadenaEncoded)
                except:
                    theResult[ 'simbolos_error_codificacion_Export'].append( unSimboloCadena)    
                    if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                        return False
                    else:
                        unHayErrorSimbolo = True
                        unHayError =  True
                          
            theBuffer.write( cGNUgettextPOEntryLabel_AfterMsgid)
                        
            
            
            # ######################################################################
            """Write translation line.
            
            """                        
            unHayErrorCadenaTraducidaLabel = False        
            try:    
                theBuffer.write( cGNUgettextPOEntryLabel_msgstr)
            except:
                unHayErrorCadenaTraducidaLabel = True
                if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                    return False
                else:
                    unHayError =  True
                    
            if ( not unHayErrorCadenaTraducidaLabel) and  ( not unHayErrorTraduccion) and unaCadenaTraducidaEncoded:
                try:    
                    theBuffer.write( unaCadenaTraducidaEncoded)
                except:
                    theResult[ 'traducciones_error_codificacion_Export'].append( unSimboloCadena)    
                    if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                        return False
                    else:
                        unHayErrorTraduccion = True
                        unHayError =  True
            theBuffer.write( cGNUgettextPOEntryLabel_AfterMsgstr)
              
            try:    
                theBuffer.write( '\n')
            except:
                None
                
        return not unHayError        
    

        
        
        

    

    
    security.declarePrivate( 'fContenidoFicheroExportacionIdiomaModulo_GNUgettextPO')    
    def fContenidoFicheroExportacionIdiomaModulo_GNUgettextPO( self, 
        theIdioma, 
        theNombreModulo, 
        theCodificacionCaracteres, 
        theResultadosTraducciones,
        theResultadosTraduccionesReferencia, 
        theSourcesCadenasPorSimbolo,
        theModulosCadenasPorSimbolo,
        theEncodingErrorHandleMode,
        theEncodedFileErrorsMode,
        theSystemToUnicodeErrorsMode,
        theUnicodeToUTF8ErrorsMode,
        theTranslationService,
        theParentExecutionRecord    =None):
         
        unExecutionRecord = self.fStartExecution( 'method',  'fContenidoFicheroExportacionIdiomaModulo_GNUgettextPO', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True,},)
        try:
         
            unResult = self.fNewVoidResultFicheroExportacionGNUgettextPO()
            unResult[ 'encoding']                       = theCodificacionCaracteres
            unResult[ 'encoding_error_handle_mode']     = theEncodingErrorHandleMode
            unResult[ 'encoded_file_errors_mode']       = theEncodedFileErrorsMode
            unResult[ 'system_to_unicode_errors_mode']  = theSystemToUnicodeErrorsMode
            unResult[ 'unicode_to_utf8_errors_mode']    = theUnicodeToUTF8ErrorsMode
                
            try:
                if not theIdioma or not theCodificacionCaracteres:
                    unResult[ 'status'] = cResultCondition_Internal_MissingParameter
                    return unResult
                
               
                unBufferResultado = StringIO()
                
                unaCodificacionCaracteres = theCodificacionCaracteres
                unaCodificacionEntrada    = cEncodingUTF8
                
                if unaCodificacionCaracteres == cEncodingUnicodeEscape:
                    unaCodificacionCaracteres = cEncodingASCII
                    unaCodificacionEntrada    = cEncodingASCII
                    
                unEncodedFile = None
                try:
                    unEncodedFile = CODECS_EncodedFile( unBufferResultado, unaCodificacionEntrada, unaCodificacionCaracteres, errors=theEncodedFileErrorsMode)
                except:
                    None
                
                if not unEncodedFile:
                    unResult[ 'status'] = cResultCondition_Encoding_NotAvailable
                    return unResult
        
                anErrorInFile = False
                
                if not self.fWriteHeader_GNUgettextPO( 
                    unEncodedFile, 
                    unResult,
                    theIdioma, 
                    theNombreModulo, 
                    theCodificacionCaracteres,
                    theEncodingErrorHandleMode, 
                    theSystemToUnicodeErrorsMode,
                    theUnicodeToUTF8ErrorsMode,
                    theTranslationService):
    
                    anErrorInFile = True
                    
                    unResult[ 'status'] = cResultCondition_Encoding_ErrorInHeader
                    if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                        unResult.update( {
                            'contenido':                    unBufferResultado.getvalue(),
                        })
                        return unResult
                    
                    
                    
                    
                if not theResultadosTraducciones:
                    unResult[ 'success'] = not anErrorInFile
                    unResult[ 'status'] = cResultCondition_NoTranslationsToExport
                    unResult.update( {
                        'contenido':                    unBufferResultado.getvalue(),
                    })
                    return unResult
                
                
                if not self.fWriteTranslationResults_GNUgettextPO( 
                    unEncodedFile, 
                    unResult,
                    theResultadosTraducciones,
                    theResultadosTraduccionesReferencia,
                    theSourcesCadenasPorSimbolo,
                    theModulosCadenasPorSimbolo,
                    theCodificacionCaracteres,
                    theEncodingErrorHandleMode,
                    theSystemToUnicodeErrorsMode,
                    theUnicodeToUTF8ErrorsMode,
                    theTranslationService):
                    
                    anErrorInFile = True
                    
                    if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                        unResult[ 'status'] = cResultCondition_Encoding_ErrorInTranslations
                        unResult.update( {
                            'contenido':                    unBufferResultado.getvalue(),
                        })
                        return unResult
                
                
                 
                unResult.update( {
                    'success':    not anErrorInFile, 
                    'contenido':  unBufferResultado.getvalue(),
                })
                
                return unResult  

            finally:
                unResult[ 'total_encoding_errors']  = \
                    (( unResult.get( 'header_error_codificacion_SystemToUnicode', False) and 1) or 0) + \
                    (( unResult.get( 'header_error_codificacion_UnicodeToUTF', False) and 1) or 0) + \
                    (( unResult.get( 'header_error_codificacion_Export', False) and 1) or 0) + \
                    len( unResult.get( 'simbolos_error_codificacion_SystemToUnicode', [])) + \
                    len( unResult.get( 'simbolos_error_codificacion_UnicodeToUTF', [])) + \
                    len( unResult.get( 'simbolos_error_codificacion_Export', [])) + \
                    len( unResult.get( 'traducciones_error_codificacion_SystemToUnicode', [])) + \
                    len( unResult.get( 'traducciones_error_codificacion_UnicodeToUTF', [])) + \
                    len( unResult.get( 'traducciones_error_codificacion_Export', []))

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
    
 

    
    
    
    security.declarePrivate( 'fContenidoFicheroExportacionIdiomaModuloNoEspecificado_GNUgettextPO')    
    def fContenidoFicheroExportacionIdiomaModuloNoEspecificado_GNUgettextPO( self, 
        theIdioma, 
        theNombreModulo, 
        theCodificacionCaracteres, 
        theResultadosTraducciones,
        theResultadosTraduccionesReferencia, 
        theSourcesCadenasPorSimbolo,
        theModulosCadenasPorSimbolo,
        theEncodingErrorHandleMode,
        theEncodedFileErrorsMode,
        theSystemToUnicodeErrorsMode,
        theUnicodeToUTF8ErrorsMode,
        theTranslationService,
        theParentExecutionRecord    =None):
         
        unExecutionRecord = self.fStartExecution( 'method',  'fContenidoFicheroExportacionIdiomaModulo_GNUgettextPO', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True,},) 
        try:
         
            unResult = self.fContenidoFicheroExportacionIdiomaModulo_GNUgettextPO(  
                theIdioma, 
                theNombreModulo, 
                theCodificacionCaracteres, 
                theResultadosTraducciones,
                theResultadosTraduccionesReferencia, 
                theSourcesCadenasPorSimbolo,
                theModulosCadenasPorSimbolo,
                theEncodingErrorHandleMode,
                theEncodedFileErrorsMode,
                theSystemToUnicodeErrorsMode,
                theUnicodeToUTF8ErrorsMode,
                theTranslationService,
                unExecutionRecord)

            return unResult  

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
    
 

    

    
    security.declarePrivate( 'fContenidoFicheroExportacionIdiomaTodosModulos_GNUgettextPO')    
    def fContenidoFicheroExportacionIdiomaTodosModulos_GNUgettextPO( self, 
        theIdioma, 
        theNombreModulo, 
        theCodificacionCaracteres, 
        theResultadosTraducciones,
        theResultadosTraduccionesReferencia, 
        theSourcesCadenasPorSimbolo,
        theModulosCadenasPorSimbolo,
        theEncodingErrorHandleMode,
        theEncodedFileErrorsMode,
        theSystemToUnicodeErrorsMode,
        theUnicodeToUTF8ErrorsMode,
        theTranslationService,
        theParentExecutionRecord    =None):
         
        unExecutionRecord = self.fStartExecution( 'method',  'fContenidoFicheroExportacionIdiomaModulo_GNUgettextPO', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True,},)
        try:
         
            unResult = self.fContenidoFicheroExportacionIdiomaModulo_GNUgettextPO(  
                theIdioma, 
                theNombreModulo, 
                theCodificacionCaracteres, 
                theResultadosTraducciones,
                theResultadosTraduccionesReferencia, 
                theSourcesCadenasPorSimbolo,
                theModulosCadenasPorSimbolo,
                theEncodingErrorHandleMode,
                theEncodedFileErrorsMode,
                theSystemToUnicodeErrorsMode,
                theUnicodeToUTF8ErrorsMode,
                theTranslationService,
                unExecutionRecord)

            return unResult  

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
    
 
            
            
            
            
            
            
    security.declarePrivate( 'fEncodedFileErrorsMode')    
    def fEncodedFileErrorsMode( self, theEncodingErrorHandleMode):  
        return cEncodedFileErrorsModeByEncodingErrorHandleMode.get( theEncodingErrorHandleMode, cDefaultEncodedFileErrorsMode)
    
        
        
            
    security.declarePrivate( 'fSystemToUnicodeErrorsMode')    
    def fSystemToUnicodeErrorsMode( self, theEncodingErrorHandleMode):  
        return cSystemToUnicodeErrorsModeByEncodingErrorHandleMode.get( theEncodingErrorHandleMode, cDefaultSystemToUnicodeErrorsMode)
    
        
            
    security.declarePrivate( 'fUnicodeToUTF8ErrorsMode')    
    def fUnicodeToUTF8ErrorsMode( self, theEncodingErrorHandleMode):  
        return cUnicodeToUTF8ErrorsModeByEncodingErrorHandleMode.get( theEncodingErrorHandleMode, cDefaultUnicodeToUTF8ErrorsMode)
    

    
    
    
    
    


    security.declarePrivate( 'fStoreExportedFile')    
    def fStoreExportedFile( self, theFileName, theFileContent):
        """Store export contents as a file system file at the pre-configured path.
            
        """
        
        if not theFileName:
            return [ '', '',]
        
        # ###################################################
        """Make sure that exported files store folder exists.
            
        """
        aExportedFilesPath = cTRAExportedFilesDiskPath
                            
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
    
        
    
    
    
    
    security.declareProtected( permissions.View, 'fExportedFileContents')
    def fExportedFileContents( self, theFileName,):
        """Retrieve the export contents  Stored as a file system file at the pre-configured path.
            
        """
        
        if not theFileName:
            return None
        
        # ###################################################
        """Make sure that exported files store folder exists.
            
        """
        aExportedFilesPath = cTRAExportedFilesDiskPath
                            
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
    
            
    
    
    

        

    security.declareProtected( permissions.View, 'fRequestNewBackup')
    def fRequestNewBackup( self, 
        theAdditionalParms      =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Request creation of a Backup long-lived process control handler, to be executed later.
        
        """

         
        unExecutionRecord = self.fStartExecution( 'method',  'fRequestNewBackup', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }, ) 
        
        
        try:
            
            
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                
            aBackupResult = self.fNewVoidProgressResult()
            
            
            aProgressElement = None
            aThereWasException = False
            aProgressHandler = None
            
            try:
                
                aMetaType = 'UnknownType'
                try:
                    aMetaType = self.meta_type
                except:
                    aMetaType = self.__class__.__name
                if not aMetaType:
                    aMetaType = 'UnknownType'
                
                aStartDateTimeNowTextual = self.fDateTimeNowTextual()
                aBackupResult[ 'process_type']           = cTRAProgress_ProcessType_Backup
                aBackupResult[ 'start_date_time_string'] = aStartDateTimeNowTextual
                aBackupResult[ 'date_time_now_string']   = aStartDateTimeNowTextual
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
                
                unCatalogoRaiz = self          
                aBackupResult[ 'TRACatalogo_title']      = unCatalogoRaiz.Title()
                aBackupResult[ 'TRACatalogo_path' ]      = unCatalogoRaiz.fPathDelRaiz()
                aBackupResult[ 'TRACatalogo_UID' ]       = unCatalogoRaiz.UID()
                
                    
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_Backup_TRACatalogo, 
                    theElementsBindings     = { cBoundObject: self,},
                    theRulesToCollect       = [ ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord
                )
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    aBackupResult[ 'success']   =  False
                    aBackupResult[ 'condition'] = 'gvSIGi18n_no_permission_ToBackup'
                    aBackupResult[ 'date_time_now_string']   = self.fDateTimeNowTextual()
                    return None
                
                 
                

                
                aProgressHandler, aProgressElement = self.fCreateNewProgressAndHandlerForElement(  
                    theInitialElement       =self, 
                    theProcessType          =cTRAProgress_ProcessType_Backup, 
                    theInputParameters      =None,
                    theTimestamp            =aStartDateTimeNowTextual,
                    theResult               =aBackupResult, 
                    theInitializeLambda     =fBackupInitialize_lambda,
                    theElementLambda        =fExportElement_lambda,
                    theLoopLambda           =fExportLoop_lambda,
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
                    unInformeExcepcion += 'Exception during fRequestNewBackup of element %s %s at %s\n'  % (  self.meta_type(), self.Title(), self.fPhysicalPathString())
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
                
                return None
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
           
                
            
            
            
            
            
            
            
            
            
            
            
 

    security.declareProtected( permissions.View, 'fRequestNewExportGvSIG')
    def fRequestNewExportGvSIG( self, 
        theAdditionalParms      =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Request creation of a Export for gvSIG long-lived process control handler, to be executed later.
        
        """

         
        unExecutionRecord = self.fStartExecution( 'method',  'fRequestNewExportGvSIG', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }, ) 
        
        
        try:
            
            unCodigoIdioma = theAdditionalParms.get( 'theCodigoIdioma', '')
            if not unCodigoIdioma:
                return None
            
            unIdioma = self.fGetIdiomaPorCodigo( unCodigoIdioma)
            if unIdioma == None:
                return None
            
            
            unosModulesToExport  = theAdditionalParms.get( 'theModulesToExport', '')
            if not unosModulesToExport:
                return None
              
            unProductName  = theAdditionalParms.get( 'theProductName', '')
            if not unProductName:
                return None
            
            unProductVersion  = theAdditionalParms.get( 'theProductVersion', '')
            if not unProductVersion:
                return None
            
            unL10NVersion  = theAdditionalParms.get( 'theL10NVersion', '')
            if not unL10NVersion:
                return None
            
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                
            aExportGvSIGResult = self.fNewVoidProgressResult()
            
            
            aProgressElement = None
            aThereWasException = False
            aProgressHandler = None
            
            try:
                
                aMetaType = 'UnknownType'
                try:
                    aMetaType = unIdioma.meta_type
                except:
                    aMetaType = unIdioma.__class__.__name
                if not aMetaType:
                    aMetaType = 'UnknownType'
                
                aStartDateTimeNowTextual = self.fDateTimeNowTextual()
                aExportGvSIGResult[ 'process_type']           = cTRAProgress_ProcessType_ExportGvSIG
                aExportGvSIGResult[ 'start_date_time_string'] = aStartDateTimeNowTextual
                aExportGvSIGResult[ 'date_time_now_string']   = aStartDateTimeNowTextual
                aExportGvSIGResult[ 'element_type']           = aMetaType
                aExportGvSIGResult[ 'element_title']          = unIdioma.Title()
                aExportGvSIGResult[ 'element_path' ]          = unIdioma.fPhysicalPathString()
                aExportGvSIGResult[ 'element_UID' ]           = unIdioma.UID()
                aExportGvSIGResult[ 'last_element_type']      = ''
                aExportGvSIGResult[ 'last_element_title']     = ''
                aExportGvSIGResult[ 'last_element_path']      = ''
                aExportGvSIGResult[ 'last_element_UID']       = ''
                
                aMemberId = self.fGetMemberId()
                aExportGvSIGResult[ 'member_id'] = aMemberId
                
                unCatalogoRaiz = self          
                aExportGvSIGResult[ 'TRACatalogo_title']      = unCatalogoRaiz.Title()
                aExportGvSIGResult[ 'TRACatalogo_path' ]      = unCatalogoRaiz.fPathDelRaiz()
                aExportGvSIGResult[ 'TRACatalogo_UID' ]       = unCatalogoRaiz.UID()
                
                    
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_ExportGvSIG_TRAIdioma, 
                    theElementsBindings     = { cBoundObject: unIdioma,},
                    theRulesToCollect       = [ ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord
                )
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    aExportGvSIGResult[ 'success']   =  False
                    aExportGvSIGResult[ 'condition'] = 'gvSIGi18n_no_permission_ToExportGvSIG'
                    aExportGvSIGResult[ 'date_time_now_string']   = self.fDateTimeNowTextual()
                    return None
                
                
                someInputParameters = {
                    'theCodigoIdioma':     unCodigoIdioma,
                    'theModulesToExport':  unosModulesToExport,
                    'theProductName':      unProductName,
                    'theProductVersion':   unProductVersion,
                    'theL10NVersion':      unL10NVersion,
                }
                
                
                aProgressHandler, aProgressElement = self.fCreateNewProgressAndHandlerForElement(  
                    theInitialElement       =unIdioma, 
                    theProcessType          =cTRAProgress_ProcessType_ExportGvSIG, 
                    theInputParameters      =someInputParameters,
                    theTimestamp            =aStartDateTimeNowTextual,
                    theResult               =aExportGvSIGResult, 
                    theInitializeLambda     =fExportGvSIGInitialize_lambda,
                    theElementLambda        =fExportElement_lambda,
                    theLoopLambda           =fExportLoop_lambda,
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
                    unInformeExcepcion += 'Exception during fRequestNewExportGvSIG of element %s %s at %s\n'  % (  self.meta_type(), self.Title(), self.fPhysicalPathString())
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
                
                aExportGvSIGResult[ 'success'] = False
                aExportGvSIGResult[ 'exception_date_time_string'] = self.fDateTimeNowTextual()
                try:
                    aExportGvSIGResultDump = self.fProgressResult_dump( aExportGvSIGResult)
                except:
                    None
                if aExportGvSIGResultDump:
                    unInformeExcepcion += aExportGvSIGResultDump
                
                aExportGvSIGResult[ 'exception_report'] = unInformeExcepcionWOResult

                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
    
                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return None
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
           
                
            
                    
            
            
            
            
            
            
            
    
            
            
            
 

    security.declareProtected( permissions.View, 'fRequestNewExport')
    def fRequestNewExport( self, 
        theAdditionalParms      =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Request creation of a Export for gvSIG long-lived process control handler, to be executed later.
        
        """

         
        unExecutionRecord = self.fStartExecution( 'method',  'fRequestNewExport', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }, ) 
        
        
        try:
            
            
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                
            aExportResult = self.fNewVoidProgressResult()
            
            
            aProgressElement = None
            aThereWasException = False
            aProgressHandler = None
            
            try:
                
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
                aExportResult[ 'element_type']           = aMetaType
                aExportResult[ 'element_title']          = self.Title()
                aExportResult[ 'element_path' ]          = self.fPhysicalPathString()
                aExportResult[ 'element_UID' ]           = self.UID()
                aExportResult[ 'last_element_type']      = ''
                aExportResult[ 'last_element_title']     = ''
                aExportResult[ 'last_element_path']      = ''
                aExportResult[ 'last_element_UID']       = ''
                
                aMemberId = self.fGetMemberId()
                aExportResult[ 'member_id'] = aMemberId
                
                unCatalogoRaiz = self          
                aExportResult[ 'TRACatalogo_title']      = unCatalogoRaiz.Title()
                aExportResult[ 'TRACatalogo_path' ]      = unCatalogoRaiz.fPathDelRaiz()
                aExportResult[ 'TRACatalogo_UID' ]       = unCatalogoRaiz.UID()
                
                    
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_Export, 
                    theElementsBindings     = { cBoundObject: self,},
                    theRulesToCollect       = [ ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord
                )
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    aExportResult[ 'success']   =  False
                    aExportResult[ 'condition'] = 'gvSIGi18n_no_permission_ToExport'
                    aExportResult[ 'date_time_now_string']   = self.fDateTimeNowTextual()
                    return None
                
                
                someInputParameters = {
                    'theLanguagesToExport'            : theAdditionalParms.get( 'theLanguagesToExport', [])[:],
                    'theCodigosIdiomaReferencia'      : theAdditionalParms.get( 'theCodigosIdiomaReferencia', {}).copy(),
                    'theCodificacionesCaracteres'     : theAdditionalParms.get( 'theCodificacionesCaracteres', {}).copy(),
                    'theModulesToExport'              : theAdditionalParms.get( 'theModulesToExport', [])[:],
                    'theExportFormat'                 : theAdditionalParms.get( 'theExportFormat', ''),
                    'theIncludeManifest'              : theAdditionalParms.get( 'theIncludeManifest', ''),
                    'theIncludeManifest_vocabulary'   : theAdditionalParms.get( 'theIncludeManifest_vocabulary', [])[:],
                    'theIncludeLocalesCSV'            : theAdditionalParms.get( 'theIncludeLocalesCSV', ''),
                    'theIncludeLocalesCSV_vocabulary' : theAdditionalParms.get( 'theIncludeLocalesCSV_vocabulary', [])[:],
                    'theSeparatedModules'             : theAdditionalParms.get( 'theSeparatedModules', ''),
                    'theSeparatedModules_vocabulary'  : theAdditionalParms.get( 'theSeparatedModules_vocabulary', [])[:],
                    'theTipoArchivo'                  : theAdditionalParms.get( 'theTipoArchivo', ''),
                    'theDefaultLanguageCode'          : theAdditionalParms.get( 'theDefaultLanguageCode', ''),
                    'theDefaultModuleName'            : theAdditionalParms.get( 'theDefaultModuleName', ''),
                    'theEncodingErrorHandleMode'      : theAdditionalParms.get( 'theEncodingErrorHandleMode', ''),
                    'theFilenameForGvSIG'             : theAdditionalParms.get( 'theFilenameForGvSIG', ''),
                    'theFilenameForGvSIG_vocabulary'  : theAdditionalParms.get( 'theFilenameForGvSIG_vocabulary', [])[:],
                    'theProductName'                  : theAdditionalParms.get( 'theProductName', ''),
                    'theProductVersion'               : theAdditionalParms.get( 'theProductVersion', ''),
                    'theL10NVersion'                  : theAdditionalParms.get( 'theL10NVersion', ''),
                    'theSpecificFilename'             : theAdditionalParms.get( 'theSpecificFilename', ''),
                }
                
                aProgressHandler, aProgressElement = self.fCreateNewProgressAndHandlerForElement(  
                    theInitialElement       =self, 
                    theProcessType          =cTRAProgress_ProcessType_Export, 
                    theInputParameters      =someInputParameters,
                    theTimestamp            =aStartDateTimeNowTextual,
                    theResult               =aExportResult, 
                    theInitializeLambda     =fExportInitialize_lambda,
                    theElementLambda        =fExportElement_lambda,
                    theLoopLambda           =fExportLoop_lambda,
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
                    unInformeExcepcion += 'Exception during fRequestNewExport of element %s %s at %s\n'  % (  self.meta_type(), self.Title(), self.fPhysicalPathString())
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
                
                return None
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
           
                
            
                    
            
            
            
            
            
            
            
            
            
            
            
    
    ##/code-section class-header

    # Methods
# end of class TRACatalogo_Exportacion

##code-section module-footer #fill in your manual code here




        
def fBackupInitialize_lambda( theContextualElement, theProcessControlManager, theAdditionalParmsHere):  

    if theContextualElement == None:
        return None
    
    if not theProcessControlManager:
        return None
    

    unosCodigosIdiomas = [ unIdioma.getCodigoIdiomaEnGvSIG() for unIdioma in theContextualElement.getCatalogo().fObtenerTodosIdiomas()]
    someExportParameters = {
        'theLanguagesToExport':         unosCodigosIdiomas,
        'theCodigosIdiomaReferencia':   {}, # No reference language
        'theCodificacionesCaracteres':  dict( [ ( unCodigo, cDefaultExportEncodingName_GNUgettextPO,) for unCodigo in unosCodigosIdiomas]), 
        'theModulesToExport':           [ unModulo.Title() for unModulo in theContextualElement.getCatalogo().fObtenerTodosModulos()] + [ cModuloNoEspecificado_ValorNombre,],
        'theExportFormat':              cExportFormatOption_GNUgettextPO,
        'theIncludeManifest':           'Si',
        'theIncludeManifest_vocabulary': ['Si', 'No',],
        'theIncludeLocalesCSV':         'Si',
        'theIncludeLocalesCSV_vocabulary': ['Si', 'No',],
        'theSeparatedModules':          'No',
        'theSeparatedModules_vocabulary': ['Si', 'No',],
        'theTipoArchivo':               cZipFilePostfix,
        'theEncodingErrorHandleMode':   cEncodingErrorHandleMode_BackslashReplaceAndContinue,
        'theFilenameForGvSIG':          'No',
        'theFilenameForGvSIG_vocabulary': ['Si', 'No',],
        'theProductName':               theContextualElement.getCatalogo().getNombreProducto(),
        'theProductVersion':            '',
        'theL10NVersion':               '',
        'theSpecificFilename':          '%s_BACKUP_%s_%s.zip' % ( theContextualElement.getCatalogo().getNombreProducto(), theContextualElement.fDateTimeNowTextual().replace( ' ', '_').replace( ':', '-'), theContextualElement.fGetMemberId())
    }
                
    
    unosInitializedObjects = {
        'export_parameters': someExportParameters,
    }
                
    theProcessControlManager.pAddInitializedObjects( unosInitializedObjects)
    
    return None        
            
 




        
def fExportGvSIGInitialize_lambda( theContextualElement, theProcessControlManager, theAdditionalParmsHere):  

    if theContextualElement == None:
        return None
    
    if not theProcessControlManager:
        return None
    
    if not theProcessControlManager.vInputParameters:
        return None

    unCodigoIdioma = theProcessControlManager.vInputParameters.get( 'theCodigoIdioma', '')
    if not unCodigoIdioma:
        return None
    
    unCatalogoRaiz = theContextualElement.getCatalogo()
    if unCatalogoRaiz == None:
        return None
     
    unIdioma = unCatalogoRaiz.fGetIdiomaPorCodigo( unCodigoIdioma)
    if ( unIdioma == None):
        return None
    
        
    unosCodigosIdiomas           = [ unCodigoIdioma,]
    unosCodigosIdiomasReferencia = dict( [ ( unCodigoIdioma, (( unCodigoIdioma == 'en') and 'es') or 'en',)])
    
    someModulesToExport = theProcessControlManager.vInputParameters.get( 'theModulesToExport', [])
    if not someModulesToExport:
        someModulesToExport = [ unModulo.Title() for unModulo in unCatalogoRaiz.fObtenerTodosModulos()] + [ cModuloNoEspecificado_ValorNombre,]
        
    
    someExportParameters = {
        'theLanguagesToExport':         unosCodigosIdiomas,
        'theCodigosIdiomaReferencia':   unosCodigosIdiomasReferencia,
        'theCodificacionesCaracteres':  dict( [ ( unCodigo, cEncodingUnicodeEscape,) for unCodigo in unosCodigosIdiomas]), 
        'theModulesToExport':           someModulesToExport,
        'theExportFormat':              cExportFormatOption_JavaProperties,
        'theIncludeManifest':           'No',
        'theIncludeManifest_vocabulary': ['Si', 'No',],
        'theIncludeLocalesCSV':         'Si',
        'theIncludeLocalesCSV_vocabulary': ['Si', 'No',],
        'theSeparatedModules':          'No',
        'theSeparatedModules_vocabulary': ['Si', 'No',],
        'theDefaultLanguageCode':       'es',
        'theTipoArchivo':               cZipFilePostfix,
        'theEncodingErrorHandleMode':   cEncodingErrorHandleMode_BackslashReplaceAndContinue,
        'theFilenameForGvSIG':          'Si',
        'theFilenameForGvSIG_vocabulary': ['Si', 'No',],
        'theProductName':               theProcessControlManager.vInputParameters.get( 'theProductName',    unCatalogoRaiz.getNombreProducto()),
        'theProductVersion':            theProcessControlManager.vInputParameters.get( 'theProductVersion', '1'),
        'theL10NVersion':               theProcessControlManager.vInputParameters.get( 'theL10NVersion',    '1'),
        'theSpecificFilename':          None,
    }
        
   
    unosInitializedObjects = {
        'export_parameters': someExportParameters,
    }
                
    theProcessControlManager.pAddInitializedObjects( unosInitializedObjects)
    
    return None        
            
 






        
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
        
        
        theCodigosIdiomas               = someExportParameters.get( 'theLanguagesToExport', [])
        theCodigosIdiomasReferencia     = someExportParameters.get( 'theCodigosIdiomaReferencia', {})
        theCodificacionesCaracteres     = someExportParameters.get( 'theCodificacionesCaracteres', {})
        theNombresModulos               = someExportParameters.get( 'theModulesToExport', [])
        theIncluirModuloNoEspecificado  = cModuloNoEspecificado_ValorNombre in theNombresModulos
        theExportFormat                 = someExportParameters.get( 'theExportFormat', '')
        theIncludeManifest              = someExportParameters.get( 'theIncludeManifest', '')    == ( someExportParameters.get( 'theIncludeManifest_vocabulary',  ['xXxXxXx',])[ 0])
        theIncludeLocalesCSV            = someExportParameters.get( 'theIncludeLocalesCSV', '')  == ( someExportParameters.get( 'theIncludeLocalesCSV_vocabulary',  ['xXxXxXx',])[ 0])
        theSeparatedModules             = someExportParameters.get( 'theSeparatedModules', '')   == ( someExportParameters.get( 'theSeparatedModules_vocabulary', ['xXxXxXx',])[ 0])
        theTipoArchivo                  = someExportParameters.get( 'theTipoArchivo', '')
        theDefaultLanguageCode          = someExportParameters.get( 'theDefaultLanguageCode', '')
        theDefaultModuleName            = someExportParameters.get( 'theDefaultModuleName', '')
        theEncodingErrorHandleMode      = someExportParameters.get( 'theEncodingErrorHandleMode', '')
        theFilenameForGvSIG             = someExportParameters.get( 'theFilenameForGvSIG', '')   == ( someExportParameters.get( 'theFilenameForGvSIG_vocabulary', ['xXxXxXx',])[ 0])
        theProductName                  = someExportParameters.get( 'theProductName', '')
        theProductVersion               = someExportParameters.get( 'theProductVersion', '')
        theL10NVersion                  = someExportParameters.get( 'theL10NVersion', '')
        theSpecificFilename             = someExportParameters.get( 'theSpecificFilename', '')
        
    
        unInforme[ 'languages_requested'] = ( theCodigosIdiomas or [])[:]
        unInforme[ 'modules_requested']   = ( theNombresModulos or [])[:]
        unInforme[ 'reference_languages'] = ( theCodigosIdiomasReferencia and theCodigosIdiomasReferencia.copy()) or {}
        
        theProcessControlManager.vResult[ 'languages_requested'] = unInforme[ 'languages_requested'] 
        theProcessControlManager.vResult[ 'modules_requested']   = unInforme[ 'modules_requested'] 
        theProcessControlManager.vResult[ 'reference_languages'] = unInforme[ 'reference_languages'] 
        
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
    
             
        theProcessControlManager.vResult[ 'export_format']      = unInforme[ 'export_format'] 
        theProcessControlManager.vResult[ 'include_manifest']   = unInforme[ 'include_manifest'] 
        theProcessControlManager.vResult[ 'include_localescsv'] = unInforme[ 'include_localescsv'] 
        theProcessControlManager.vResult[ 'separate_modules']   = unInforme[ 'separate_modules'] 
        
            
        
        
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
                
            if unCodigoIdioma in unosCodigosIdiomasReferencia:
                unosCodigosIdiomasReferenciaAExportar.add( unCodigoIdioma)
                if unExportAsJavaProperties:
                    if not( unCodigoIdioma in unosCodigosIdiomasAExportar):
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
                unasCodificacionesCaracteres[ unCodigoIdioma] = cEncodingUTF8
             
    
        
        
        
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
            
            unaCodificacionCaracteres = unasCodificacionesCaracteres.get( unCodigoIdioma, cEncodingUTF8)
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
                        unDirName  = "%s%s" % ( unNombreModulo, cZipPathSeparator,)
                        unFileNameProperties = "%s%s%s%s" % ( unDirName, cFilenamePropertiesBase, theProcessControlManager.vCatalogoRaiz.fPropertiesFilenameIdiomaPostfix( unCodigoIdioma, theDefaultLanguageCode or theProcessControlManager.vCatalogoRaiz.fCodigoIdiomaPorDefecto()), cPropertiesFilePostfix,)
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
                            theWriteReferenceEntry  = unCodigoIdioma in unosCodigosIdiomasReferencia, 
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
                            theWriteReferenceEntry  = unCodigoIdioma in unosCodigosIdiomasReferencia, 
                            theWriteJavaProperties  = unExportAsJavaProperties, 
                            theFileNameProperties   = unFileNameProperties, 
                            theWriteGNUgettextPO    = unExportAsGNUgettextPO, 
                            theFileNamePO           = unFileNamePO,
                        )
                        
                    if unFileNameProperties:
                        unResultFicheroExportacion = theProcessControlManager.vCatalogoRaiz.fContenidoFicheroExportacionIdiomaModulo_JavaProperties( 
                            unIdioma, 
                            unNombreModulo, 
                            unaCodificacionCaracteres, 
                            unosResultadosTraducciones,
                            unosSourcesCadenasPorSimbolo,
                            unosModulosCadenasPorSimbolo,
                            theEncodingErrorHandleMode,
                            anEncodedFileErrorsMode,
                            aSystemToUnicodeErrorsMode,
                            aUnicodeToUTF8ErrorsMode,
                            aTranslationService,
                            unExecutionRecord,
                        )
                        unInformeExportarModulo[ 'export_result'] = unResultFicheroExportacion
                        if ( not unResultFicheroExportacion) or  ( not unResultFicheroExportacion.get( 'success', False)):
                            unHayError = True
                            if not unResultFicheroExportacion.get( 'success', False):
                                if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                                    break
                                if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CountAllErrorsAndCancel,]:
                                    continue
                        if unResultFicheroExportacion:
                            unContenidoFicheroExportacion = unResultFicheroExportacion.get( 'contenido', '')
                            unZipFile.writestr( unFileNameProperties, unContenidoFicheroExportacion)
                        
                         
                    if unFileNamePO:
                        unResultFicheroExportacion = theProcessControlManager.vCatalogoRaiz.fContenidoFicheroExportacionIdiomaModulo_GNUgettextPO(   
                            unIdioma, 
                            unNombreModulo, 
                            unaCodificacionCaracteres, 
                            unosResultadosTraducciones, 
                            unosResultadosTraduccionesReferencia,
                            unosSourcesCadenasPorSimbolo,
                            unosModulosCadenasPorSimbolo,
                            theEncodingErrorHandleMode,
                            anEncodedFileErrorsMode,
                            aSystemToUnicodeErrorsMode,
                            aUnicodeToUTF8ErrorsMode,
                            aTranslationService,
                            unExecutionRecord,
                        )
                        unInformeExportarModulo[ 'export_result'] = unResultFicheroExportacion
                        if ( not unResultFicheroExportacion) or  ( not unResultFicheroExportacion.get( 'success', False)):
                            unHayError = True
                            if not unResultFicheroExportacion.get( 'success', False):
                                if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                                    break
                                if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CountAllErrorsAndCancel,]:
                                    continue
                        if unResultFicheroExportacion:
                            unContenidoFicheroExportacion = unResultFicheroExportacion.get( 'contenido', '')
                            unZipFile.writestr( unFileNamePO, unContenidoFicheroExportacion)
                            
                    unNumTranslationsTraversed = len( unosResultadosTraducciones)
                    if unosResultadosTraduccionesReferencia and unFilenamePO:
                        unNumTranslationsTraversed += len( unosResultadosTraduccionesReferencia)
                    aNumElementsOfTypeRead = {
                        cNombreTipoTRAIdioma: 1,
                        cNombreTipoTRAModulo: 1,
                        cNombreTipoTRATraduccion : unNumTranslationsTraversed,
                    }
                    theProcessControlManager.pProcessStep( unIdioma, aNumElementsOfTypeRead, None)
                    
                    
           
                if ( theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]) and ( unInformeExportarIdioma.get( 'num_encoding_errors', 0) > 0):
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
                        unFileNameProperties = "%s%s%s" % ( cFilenamePropertiesBase, theProcessControlManager.vCatalogoRaiz.fPropertiesFilenameIdiomaPostfix( unCodigoIdioma, theDefaultLanguageCode or theProcessControlManager.vCatalogoRaiz.fCodigoIdiomaPorDefecto()), cPropertiesFilePostfix,)
                        unInformeExportarModulo[ 'filename_properties'] = unFileNameProperties
                        unInformeExportarModulo[ 'filename']            = unFileNameProperties
                         
                    if unExportAsGNUgettextPO:
                        unFileNamePO = "%s%s%s%s" % ( theDefaultModuleName or theProcessControlManager.vCatalogoRaiz.fNombreModuloPorDefecto(),  cPOFileCharBeforeLanguage, unCodigoIdioma, cPOFilePostfix, )
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
                                theWriteReferenceEntry  = unCodigoIdioma in unosCodigosIdiomasReferencia, 
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
                                theWriteReferenceEntry  = unCodigoIdioma in unosCodigosIdiomasReferencia, 
                                theWriteJavaProperties  = unExportAsJavaProperties, 
                                theFileNameProperties   = unFileNameProperties, 
                                theWriteGNUgettextPO    = unExportAsGNUgettextPO, 
                                theFileNamePO           = unFileNamePO,
                            )
        
                        if unFileNameProperties:
                            unResultFicheroExportacion = theProcessControlManager.vCatalogoRaiz.fContenidoFicheroExportacionIdiomaModuloNoEspecificado_JavaProperties( 
                                unIdioma, 
                                theDefaultModuleName,
                                unaCodificacionCaracteres, 
                                unosResultadosTraducciones,
                                unosSourcesCadenasPorSimbolo,
                                unosModulosCadenasPorSimbolo,
                                theEncodingErrorHandleMode,
                                anEncodedFileErrorsMode,
                                aSystemToUnicodeErrorsMode,
                                aUnicodeToUTF8ErrorsMode,
                                aTranslationService,
                                unExecutionRecord,
                            )
                            unInformeExportarModulo[ 'export_result'] = unResultFicheroExportacion
                            if ( not unResultFicheroExportacion) or  ( not unResultFicheroExportacion.get( 'success', False)):
                                unHayError = True
                                if not unResultFicheroExportacion.get( 'success', False):
                                    if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                                        break
                                    if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CountAllErrorsAndCancel,]:
                                        continue
                                 
                            if unResultFicheroExportacion:
                                unContenidoFicheroExportacion = unResultFicheroExportacion.get( 'contenido', '')
                                unZipFile.writestr( unFileNameProperties, unContenidoFicheroExportacion)
                                
                        if unFileNamePO:
                            unResultFicheroExportacion = theProcessControlManager.vCatalogoRaiz.fContenidoFicheroExportacionIdiomaModuloNoEspecificado_GNUgettextPO(   
                                unIdioma, 
                                theDefaultModuleName,
                                unaCodificacionCaracteres, 
                                unosResultadosTraducciones, 
                                unosResultadosTraduccionesReferencia,
                                unosSourcesCadenasPorSimbolo,
                                unosModulosCadenasPorSimbolo,
                                theEncodingErrorHandleMode,
                                anEncodedFileErrorsMode,
                                aSystemToUnicodeErrorsMode,
                                aUnicodeToUTF8ErrorsMode,
                                aTranslationService,
                                unExecutionRecord,
                            )
                            unInformeExportarModulo[ 'export_result'] = unResultFicheroExportacion
                            if ( not unResultFicheroExportacion) or  ( not unResultFicheroExportacion.get( 'success', False)):
                                unHayError = True
                                if not unResultFicheroExportacion.get( 'success', False):
                                    if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                                        break
                                    if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CountAllErrorsAndCancel,]:
                                        continue
                            if unResultFicheroExportacion:
                                unContenidoFicheroExportacion = unResultFicheroExportacion.get( 'contenido', '')
                                unZipFile.writestr( unFileNamePO, unContenidoFicheroExportacion)
                                
                                
                        

                        unNumTranslationsTraversed = len( unosResultadosTraducciones)
                        if unosResultadosTraduccionesReferencia and unFilenamePO:
                            unNumTranslationsTraversed += len( unosResultadosTraduccionesReferencia)
                        aNumElementsOfTypeRead = {
                            cNombreTipoTRAIdioma: 1,
                            cNombreTipoTRATraduccion : unNumTranslationsTraversed,
                        }
                        theProcessControlManager.pProcessStep( unIdioma, aNumElementsOfTypeRead, None)
                                
                if ( theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]) and ( unInformeExportarIdioma.get( 'num_encoding_errors', 0) > 0):
                    break
                        
                
                
                
                
                
            else: # not unSeparatedModules
                # ##############################################################################
                """Export translations into the language in a single file with the strings in all modules and the not-specified module if requested.
                
                """
                unInformeExportarIdioma[ 'separate_modules'] = False
    
                unFileNameProperties = ''
                unFileNamePO         = ''
                
                if unExportAsJavaProperties:
                    unFileNameProperties = "%s%s%s" % ( cFilenamePropertiesBase, theProcessControlManager.vCatalogoRaiz.fPropertiesFilenameIdiomaPostfix( unCodigoIdioma, theDefaultLanguageCode or theProcessControlManager.vCatalogoRaiz.fCodigoIdiomaPorDefecto()), cPropertiesFilePostfix,)
                    unInformeExportarIdioma[ 'filename_properties'] = unFileNameProperties
                    unInformeExportarIdioma[ 'filename']            = unFileNameProperties
                     
                if unExportAsGNUgettextPO:
                    unFileNamePO = "%s%s%s%s" % ( cNoSeparateModulesFileNamePrefix,  cPOFileCharBeforeLanguage, unCodigoIdioma, cPOFilePostfix, )
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
                        theWriteReferenceEntry  = unCodigoIdioma in unosCodigosIdiomasReferencia, 
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
                        theWriteReferenceEntry  = unCodigoIdioma in unosCodigosIdiomasReferencia, 
                        theWriteJavaProperties  = unExportAsJavaProperties, 
                        theFileNameProperties   = unFileNameProperties, 
                        theWriteGNUgettextPO    = unExportAsGNUgettextPO, 
                        theFileNamePO           = unFileNamePO,
                    )
    
                if unFileNameProperties:
                    unResultFicheroExportacion  = theProcessControlManager.vCatalogoRaiz.fContenidoFicheroExportacionIdiomaTodosModulos_JavaProperties( 
                        unIdioma, 
                        theDefaultModuleName,
                        unaCodificacionCaracteres, 
                        unosResultadosTraducciones,
                        unosSourcesCadenasPorSimbolo,
                        unosModulosCadenasPorSimbolo,
                        theEncodingErrorHandleMode,
                        anEncodedFileErrorsMode,
                        aSystemToUnicodeErrorsMode,
                        aUnicodeToUTF8ErrorsMode,
                        aTranslationService,
                        unExecutionRecord,
                    )
                    unInformeExportarIdioma[ 'export_result'] = unResultFicheroExportacion
                    if ( not unResultFicheroExportacion) or  ( not unResultFicheroExportacion.get( 'success', False)):
                        unHayError = True
                        if not unResultFicheroExportacion.get( 'success', False):
                            if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                                break
                            if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CountAllErrorsAndCancel,]:
                                continue
                    if unResultFicheroExportacion:
                        unContenidoFicheroExportacion = unResultFicheroExportacion.get( 'contenido', '')
                        unZipFile.writestr( unFileNameProperties, unContenidoFicheroExportacion)
                        
                if unFileNamePO:
                    unResultFicheroExportacion = theProcessControlManager.vCatalogoRaiz.fContenidoFicheroExportacionIdiomaTodosModulos_GNUgettextPO(   
                        unIdioma, 
                        theDefaultModuleName,
                        unaCodificacionCaracteres, 
                        unosResultadosTraducciones,
                        unosResultadosTraduccionesReferencia,
                        unosSourcesCadenasPorSimbolo,
                        unosModulosCadenasPorSimbolo,
                        theEncodingErrorHandleMode,
                        anEncodedFileErrorsMode,
                        aSystemToUnicodeErrorsMode,
                        aUnicodeToUTF8ErrorsMode,
                        aTranslationService,
                        unExecutionRecord,
                    )
                    unInformeExportarIdioma[ 'export_result'] = unResultFicheroExportacion
                    if ( not unResultFicheroExportacion) or  ( not unResultFicheroExportacion.get( 'success', False)):
                        unHayError = True
                        if not unResultFicheroExportacion.get( 'success', False):
                            if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError,]:
                                break
                            if theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CountAllErrorsAndCancel,]:
                                continue
                    if unResultFicheroExportacion:
                        unContenidoFicheroExportacion = unResultFicheroExportacion.get( 'contenido', '')
                        unZipFile.writestr( unFileNamePO, unContenidoFicheroExportacion)
                        
                        
                unNumTranslationsTraversed = len( unosResultadosTraducciones)
                if unosResultadosTraduccionesReferencia and unFilenamePO:
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
        
        
        if unHayError and ( theEncodingErrorHandleMode in [ cEncodingErrorHandleMode_CancelOnFirstError, cEncodingErrorHandleMode_CountAllErrorsAndCancel]):
            theProcessControlManager.vResult[ 'success']   = False
            theProcessControlManager.vResult[ 'condition'] = 'EncodingErrorsDuringExport'
            return None
                        
        if unIncludeManifest:  
            unZipFile.writestr( cManifestFileFullName, unManifestBuffer.getvalue())
            
        if unIncludeLocalesCSV:  
            unZipFile.writestr( cLocalesCSVFileFullName, unLocalesCSVBuffer.getvalue())

        unZipFile.close()  
        
        unStoreFilePath, unStoreFileName = theProcessControlManager.vCatalogoRaiz.fStoreExportedFile( unNombreArchivoDescarga, unZipBuffer.getvalue())
        if not ( unStoreFilePath and unStoreFileName):
            theProcessControlManager.vResult[ 'success']   = False
            theProcessControlManager.vResult[ 'condition'] = 'CanNotStoreExportedFile'
            unInforme.update( {
                'success':              False,
                'status':               'CanNotStoreExportedFile',
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
     
                    
            



                    
            
            
 
            
        
        
          
def fExportElement_lambda( theElement, theProcessControlManager, theAdditionalParmsHere):  
    
    return None        







##/code-section module-footer



