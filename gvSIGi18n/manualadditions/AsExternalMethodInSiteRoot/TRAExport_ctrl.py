# -*- coding: utf-8 -*-
#
# File: TRAExport_ctrl.py
#
# Copyright (c) 2008, 2009 by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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


from StringIO import StringIO

from Products.CMFCore.utils import getToolByName

from Products.gvSIGi18n.TRAElemento_Constants import *

from Products.gvSIGi18n.TRAElemento_Permission_Definitions  import cBoundObject, cUseCase_Export

from Products.gvSIGi18n.TRAImportarExportar_Constants       import cExportFormatOption_JavaProperties, cModuloNoEspecificado_ValorNombre



cDefaultProductVersionForGvSIGExportFilename = '1'

cDefaultL10NVersionForGvSIGExportFilename    = '1'


# #########################################
#   Rendering utilities
# #########################################






# #########################################
#   Render Permission Definitions
# #########################################

def fNewVoidEditionParametersCandidateValues():
    unInforme = {
        'theLanguagesToExport':                   [],
        'theExportFormat':                        '',
        'theExportFormat_vocabulary':             [],
        'theExportFormat_vocabulary_msgids':      [],
        'theIncludeManifest':                     '',
        'theIncludeManifest_vocabulary':          [],
        'theIncludeManifest_vocabulary_msgids':   [],
        'theIncludeLocalesCSV':                   '',
        'theIncludeLocalesCSV_vocabulary':        [],
        'theIncludeLocalesCSV_vocabulary_msgids': [],
        'theSeparatedModules':                    '',
        'theSeparatedModules_vocabulary':         [],
        'theSeparatedModules_vocabulary_msgids':  [],
        'theTipoArchivo':                         '',
        'theTipoArchivo_vocabulary':              [],
        'theTipoArchivo_vocabulary_msgids':       [],
        'theDefaultLanguageCode':                 '',
        'theDefaultModuleName':                   '',
        'theEncodingErrorHandleMode':             '',
        'theEncodingErrorHandleMode_vocabulary':  [],
        'theEncodingErrorHandleMode_vocabulary_msgids': [],
        'encodings_by_language_code':   { },
        'informe_idiomas_y_modulos':    { },
        'theFilenameForGvSIG':          '',
        'theFilenameForGvSIG_vocabulary':         [],
        'theFilenameForGvSIG_vocabulary_msgids':  [],
        'theProductName':               '',
        'theProductVersion':            '',
        'theL10NVersions':              { },
    }
    return unInforme

     
        
def TRAExport_ParametersCandidateValues( 
    theContextualObject = None,
    theParametersInput               = {},
    thePermissionsCache              = None,
    theRolesCache                    = None,
    theUseCaseAssessmentResultsCache = None,
    theParentExecutionRecord         = None):

    unExecutionRecord = theContextualObject.fStartExecution( 'external method', 'TRAExport_ParametersCandidateValues', theParentExecutionRecord, False) 

    try:

        unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
        unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache

        unInforme = fNewVoidEditionParametersCandidateValues()
        
        unExportFormatMetaAndValue = theContextualObject.getCatalogo().getAttributeMetaAndValue( 'formatoExportacionPorDefecto')
        if unExportFormatMetaAndValue:
            unExportFormatVocabulary = unExportFormatMetaAndValue[ 7]
            unExportFormat = theParametersInput.get( 'theExportFormat', None)
            if not ( unExportFormat in unExportFormatVocabulary):
                unExportFormat = unExportFormatMetaAndValue[ 1]
            if not ( unExportFormat in unExportFormatVocabulary):
                unExportFormat = unExportFormatVocabulary[ 0]
            unInforme[ 'theExportFormat']                   = unExportFormat
            unInforme[ 'theExportFormat_vocabulary']        = unExportFormatVocabulary
            unInforme[ 'theExportFormat_vocabulary_msgids'] = unExportFormatMetaAndValue[ 8]
 
            
        unIncludeManifestMetaAndValue = theContextualObject.getCatalogo().getAttributeMetaAndValue( 'incluirManifestPorDefecto')
        if unIncludeManifestMetaAndValue:
            unIncludeManifestVocabulary = unIncludeManifestMetaAndValue[ 7]
            unIncludeManifest = theParametersInput.get( 'theIncludeManifest', None)
            if not ( unIncludeManifest in unIncludeManifestVocabulary):
                unIncludeManifest = unIncludeManifestMetaAndValue[ 1]
            if not ( unIncludeManifest in unIncludeManifestVocabulary):
                unIncludeManifest = unIncludeManifestVocabulary[ 0]
            unInforme[ 'theIncludeManifest']                    = unIncludeManifest
            unInforme[ 'theIncludeManifest_vocabulary']         = unIncludeManifestVocabulary
            unInforme[ 'theIncludeManifest_vocabulary_msgids']  = unIncludeManifestMetaAndValue[ 8]
         
        unIncludeLocalesCSVMetaAndValue = theContextualObject.getCatalogo().getAttributeMetaAndValue( 'incluirLocalesCSVPorDefecto')
        if unIncludeLocalesCSVMetaAndValue:
            unIncludeLocalesCSVVocabulary = unIncludeLocalesCSVMetaAndValue[ 7]
            unIncludeLocalesCSV = theParametersInput.get( 'theIncludeLocalesCSV', None)
            if not ( unIncludeLocalesCSV in unIncludeLocalesCSVVocabulary):
                unIncludeLocalesCSV = unIncludeLocalesCSVMetaAndValue[ 1]
            if not ( unIncludeLocalesCSV in unIncludeLocalesCSVVocabulary):
                unIncludeLocalesCSV = unIncludeLocalesCSVVocabulary[ 0]
            unInforme[ 'theIncludeLocalesCSV']                    = unIncludeLocalesCSV
            unInforme[ 'theIncludeLocalesCSV_vocabulary']         = unIncludeLocalesCSVVocabulary
            unInforme[ 'theIncludeLocalesCSV_vocabulary_msgids']  = unIncludeLocalesCSVMetaAndValue[ 8]
         
            
            
        unSeparatedModulesMetaAndValue = theContextualObject.getCatalogo().getAttributeMetaAndValue( 'modulosPorSeparadoPorDefecto')
        if unSeparatedModulesMetaAndValue:
            unSeparatedModulesVocabulary = unSeparatedModulesMetaAndValue[ 7]
            unSeparatedModules = theParametersInput.get( 'theSeparatedModules', None)
            if not ( unSeparatedModules in unSeparatedModulesVocabulary):
                unSeparatedModules = unSeparatedModulesMetaAndValue[ 1]
            if not ( unSeparatedModules in unSeparatedModulesVocabulary):
                unSeparatedModules = unSeparatedModulesVocabulary[ 0]
            unInforme[ 'theSeparatedModules']                   = unSeparatedModules
            unInforme[ 'theSeparatedModules_vocabulary']        = unSeparatedModulesVocabulary
            unInforme[ 'theSeparatedModules_vocabulary_msgids'] = unSeparatedModulesMetaAndValue[ 8]
 
            
        unTipoArchivoMetaAndValue = theContextualObject.getCatalogo().getAttributeMetaAndValue( 'tipoArchivoExportacionPorDefecto')
        if unTipoArchivoMetaAndValue:
            unTipoArchivoVocabulary = unTipoArchivoMetaAndValue[ 7]
            unTipoArchivo = theParametersInput.get( 'theTipoArchivo', None)
            if not ( unTipoArchivo in unTipoArchivoVocabulary):
                unTipoArchivo = unTipoArchivoMetaAndValue[ 1]
            if not ( unTipoArchivo in unTipoArchivoVocabulary):
                unTipoArchivo = unTipoArchivoVocabulary[ 0]
            unInforme[ 'theTipoArchivo']                    = unTipoArchivo
            unInforme[ 'theTipoArchivo_vocabulary']         = unTipoArchivoVocabulary
            unInforme[ 'theTipoArchivo_vocabulary_msgids']  = unTipoArchivoMetaAndValue[ 8]
        
        
        unDefaultLanguageCode = theParametersInput.get( 'theDefaultLanguageCode', None)
        if not unDefaultLanguageCode:
            unDefaultLanguageCode = theContextualObject.getCatalogo().getCodigoIdiomaPorDefecto()
        unInforme[ 'theDefaultLanguageCode'] = unDefaultLanguageCode
        

        unDefaultModuleName = theParametersInput.get( 'theDefaultModuleName', None)
        if not unDefaultModuleName:
            unDefaultModuleName = theContextualObject.getCatalogo().getNombreModuloPorDefecto()
        unInforme[ 'theDefaultModuleName'] = unDefaultModuleName
        

        unEncodingErrorHandleModeMetaAndValue = theContextualObject.getCatalogo().getAttributeMetaAndValue( 'modoGestionErrorCodificacionExportacionPorDefecto')
        if unEncodingErrorHandleModeMetaAndValue:
            unEncodingErrorHandleModeVocabulary = unEncodingErrorHandleModeMetaAndValue[ 7]
            unEncodingErrorHandleMode = theParametersInput.get( 'theEncodingErrorHandleMode', None)
            if not ( unEncodingErrorHandleMode in unEncodingErrorHandleModeVocabulary):
                unEncodingErrorHandleMode = unEncodingErrorHandleModeMetaAndValue[ 1]
            if not ( unEncodingErrorHandleMode in unEncodingErrorHandleModeVocabulary):
                unEncodingErrorHandleMode = unEncodingErrorHandleModeVocabulary[ 0]
            unInforme[ 'theEncodingErrorHandleMode']                    = unEncodingErrorHandleMode
            unInforme[ 'theEncodingErrorHandleMode_vocabulary']         = unEncodingErrorHandleModeVocabulary
            unInforme[ 'theEncodingErrorHandleMode_vocabulary_msgids']  = unEncodingErrorHandleModeMetaAndValue[ 8]
    
        unExportFilenameForGvSIGMetaAndValue = theContextualObject.getCatalogo().getAttributeMetaAndValue( 'exportarNombreFicheroParaGvSIGPorDefecto')
        if unExportFilenameForGvSIGMetaAndValue:
            unExportFilenameForGvSIGVocabulary = unExportFilenameForGvSIGMetaAndValue[ 7]
            unExportFilenameForGvSIG = theParametersInput.get( 'theFilenameForGvSIG', None)
            if not ( unExportFilenameForGvSIG in unExportFilenameForGvSIGVocabulary):
                unExportFilenameForGvSIG = unExportFilenameForGvSIGMetaAndValue[ 1]
            if not ( unExportFilenameForGvSIG in unExportFilenameForGvSIGVocabulary):
                unExportFilenameForGvSIG = unExportFilenameForGvSIGVocabulary[ 0]
            unInforme[ 'theFilenameForGvSIG']                    = unExportFilenameForGvSIG
            unInforme[ 'theFilenameForGvSIG_vocabulary']         = unExportFilenameForGvSIGVocabulary
            unInforme[ 'theFilenameForGvSIG_vocabulary_msgids']  = unExportFilenameForGvSIGMetaAndValue[ 8]
        
            
        unProductName = theParametersInput.get( 'theProductName', None)
        if not unProductName:
            unProductName = theContextualObject.getCatalogo().getNombreProducto()
        unInforme[ 'theProductName'] = unProductName
        
        unProductVersion = theParametersInput.get( 'theProductVersion', None)
        if not unProductVersion:
            unProductVersion = cDefaultProductVersionForGvSIGExportFilename
        unInforme[ 'theProductVersion'] = unProductVersion
        
        unL10NVersion = theParametersInput.get( 'theL10NVersion', None)
        if not unL10NVersion:
            unL10NVersion = cDefaultL10NVersionForGvSIGExportFilename
        unInforme[ 'theL10NVersion'] = unL10NVersion
            
            
        unInformeIdiomasYModulos = theContextualObject.getCatalogo().fInformeTitulosIdiomasConIdiomaReferenciaYModulosPermitidos( 
            cUseCase_Export, 
            thePermissionsCache         =unPermissionsCache, 
            theRolesCache               =unRolesCache, 
            theParentExecutionRecord    =unExecutionRecord
        )
        if not unInformeIdiomasYModulos:
            return unInforme
 
        unInforme[ 'informe_idiomas_y_modulos'] = unInformeIdiomasYModulos
                
        unInforme[ 'success'] = unInformeIdiomasYModulos.get( 'success', False)
        if not unInforme[ 'success']:
            return unInforme
                                
                                
         
        unosNombresModulosSolicitados = theParametersInput.get( 'theModulesToExport', [])
        unosNombresModulosAExportar= [ ]
        unInforme[ 'theModulesToExport'] = unosNombresModulosAExportar
        
        unosNombresModulos = unInformeIdiomasYModulos.get( 'modulos', [])
        for unNombreModulo in unosNombresModulos:
            if unNombreModulo in unosNombresModulosSolicitados:
                unosNombresModulosAExportar.append( unNombreModulo)
        if cModuloNoEspecificado_ValorNombre in unosNombresModulosSolicitados:
            unosNombresModulosAExportar.append( cModuloNoEspecificado_ValorNombre)
            
            
         
        unosCodigosIdiomasSolicitados = theParametersInput.get( 'theLanguagesToExport', [])
        unosCodigosIdiomasAExportar= [ ]
        unInforme[ 'theLanguagesToExport'] = unosCodigosIdiomasAExportar
        
        unosCodigosIdiomasReferenciaSolicitados = theParametersInput.get( 'theCodigosIdiomaReferencia', [])
        unosCodigosIdiomasReferencia = { }
        unInforme[ 'theCodigosIdiomaReferencia'] = unosCodigosIdiomasReferencia
        
        unosEncodingsSolicitados = theParametersInput.get( 'theCodificacionesCaracteres', [])
        unosEncodingsAUtilizar = { }
        unInforme[ 'theCodificacionesCaracteres'] = unosEncodingsAUtilizar
        
         

            
        unosEncodingsPorCodigoIdioma = { }
        unInforme[ 'encodings_by_language_code'] = unosEncodingsPorCodigoIdioma
        
        unosInformesIdiomas = unInformeIdiomasYModulos.get( 'idiomas', [])

        todosCodigosIdiomas = [ unInformeIdioma.get( 'codigoIdiomaEnGvSIG', '') for unInformeIdioma in unosInformesIdiomas if unInformeIdioma.get( 'codigoIdiomaEnGvSIG', '') ]
        
        for unInformeIdioma in unosInformesIdiomas:
            if unInformeIdioma:
                unCodigoIdioma = unInformeIdioma.get( 'codigoIdiomaEnGvSIG', '')
                if unCodigoIdioma:
                    
                    
                    if unCodigoIdioma in unosCodigosIdiomasSolicitados:
                        unosCodigosIdiomasAExportar.append( unCodigoIdioma)
                        
                       
                        
                    unCodigoIdiomaReferenciaSolicitado = unosCodigosIdiomasReferenciaSolicitados.get( unCodigoIdioma, '')
                    if not unCodigoIdiomaReferenciaSolicitado or not (  unCodigoIdiomaReferenciaSolicitado in todosCodigosIdiomas):
                        unCodigoIdiomaReferenciaSolicitado = unInformeIdioma.get( 'codigo_idioma_referencia', '')
                        
                    if unCodigoIdiomaReferenciaSolicitado and ( unCodigoIdiomaReferenciaSolicitado in todosCodigosIdiomas):
                        unosCodigosIdiomasReferencia[ unCodigoIdioma] = unCodigoIdiomaReferenciaSolicitado
                          
                        
                        
                    unosEncodingsForLanguage = theContextualObject.fEncodingsForLanguage( unCodigoIdioma)
                    unosEncodingsNamesForLanguage = []
                    if unosEncodingsForLanguage:
                        unosEncodingsPorCodigoIdioma[ unCodigoIdioma] = unosEncodingsForLanguage
                        unosEncodingsNamesForLanguage = [ unEncodingNameTitleAndAliases[ 0] for unEncodingNameTitleAndAliases in unosEncodingsForLanguage]

                    unEncodingSolicitado = unosEncodingsSolicitados.get( unCodigoIdioma, '')
                    if not unEncodingSolicitado or not ( unEncodingSolicitado in unosEncodingsNamesForLanguage):
                        if unExportFormat == cExportFormatOption_JavaProperties:
                            unEncodingSolicitado = unInformeIdioma.get( 'juego_caracteres_javaproperties', '').lower()
                        else:
                            unEncodingSolicitado = unInformeIdioma.get( 'juego_caracteres_po', '').lower()
                            
                    if not unEncodingSolicitado or not ( unEncodingSolicitado in unosEncodingsNamesForLanguage):
                        unEncodingSolicitado = cEncodingUTF8
                        
                    if unEncodingSolicitado and ( unEncodingSolicitado in unosEncodingsNamesForLanguage): 
                        unosEncodingsAUtilizar[ unCodigoIdioma] =  unEncodingSolicitado   
                                                 
                         
        return unInforme
         

    finally:
        unExecutionRecord and unExecutionRecord.pEndExecution()
                      
                
      


            



#def TRAExport_EstimateOrExportContent( 
    #theContextualObject = None,
    #theParametersInput               = {},
    #thePermissionsCache              = None,
    #theRolesCache                    = None,
    #theUseCaseAssessmentResultsCache = None,
    #theParentExecutionRecord         = None):

    #unExecutionRecord = theContextualObject.fStartExecution( 'external method', 'TRAExport_EstimateOrExportContent', theParentExecutionRecord, False) 

    #try:

        #unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
        #unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
        
        
        #return unInforme
         

    #finally:
        #unExecutionRecord and unExecutionRecord.pEndExecution()
                      
                
              