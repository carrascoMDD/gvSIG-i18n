# -*- coding: utf-8 -*-
#
# File: TRAExport_ctrl.py
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


from StringIO import StringIO

from Products.CMFCore.utils import getToolByName

from Products.gvSIGi18n.TRAElemento_Constants                 import *
from Products.gvSIGi18n.TRAElemento_Constants_Activity        import *
from Products.gvSIGi18n.TRAElemento_Constants_Configurations  import *
from Products.gvSIGi18n.TRAElemento_Constants_Dates           import *
from Products.gvSIGi18n.TRAElemento_Constants_Encoding        import *
from Products.gvSIGi18n.TRAElemento_Constants_Import          import *
from Products.gvSIGi18n.TRAElemento_Constants_Languages       import *
from Products.gvSIGi18n.TRAElemento_Constants_Logging         import *
from Products.gvSIGi18n.TRAElemento_Constants_Modules         import *
from Products.gvSIGi18n.TRAElemento_Constants_Profiling       import *
from Products.gvSIGi18n.TRAElemento_Constants_Progress        import *
from Products.gvSIGi18n.TRAElemento_Constants_String          import *
from Products.gvSIGi18n.TRAElemento_Constants_StringRequests  import *
from Products.gvSIGi18n.TRAElemento_Constants_Translate       import *
from Products.gvSIGi18n.TRAElemento_Constants_Translation     import *
from Products.gvSIGi18n.TRAElemento_Constants_TypeNames       import *
from Products.gvSIGi18n.TRAElemento_Constants_Views           import *
from Products.gvSIGi18n.TRAElemento_Constants_Vocabularies    import *
from Products.gvSIGi18n.TRAUtils                              import *

from Products.gvSIGi18n.TRAElemento_Permission_Definitions  import cBoundObject
from Products.gvSIGi18n.TRAElemento_Permission_Definitions_UseCaseNames  import cUseCase_Export

 


from Products.gvSIGi18n.TRAImportarExportar_Constants  import cModuloNoEspecificado_ValorNombre
from Products.gvSIGi18n.TRAImportarExportar_Constants_JavaProperties  import cExportFormatOption_JavaProperties


from Products.gvSIGi18nTool.TRAgvSIGi18nTool_Constants import cTRAgvSIGi18nToolId



cDefaultProductVersionForGvSIGExportFilename = '1'

cDefaultL10NVersionForGvSIGExportFilename    = '1'







        
def TRAExport_ParametersCandidateValues( 
    theContextualObject              = None,
    theParametersInput               = {},
    thePermissionsCache              = None,
    theRolesCache                    = None,
    theUseCaseAssessmentResultsCache = None,
    theParentExecutionRecord         = None):

    
    if theContextualObject == None:
        return {}
   
    aTRAgvSIGi18n_tool = getToolByName( theContextualObject, cTRAgvSIGi18nToolId, None)
    if aTRAgvSIGi18n_tool == None:
        return {}
         
    
    
    unExecutionRecord = aTRAgvSIGi18n_tool.fStartExecution( 
        theContextualElement    =theContextualObject,
        theExecutedKind         ='external method', 
        theExecutedName         ='TRAExport_ParametersCandidateValues', 
        theParentExecutionRecord=theParentExecutionRecord,
    )
      
    
    try:

        unPermissionsCache = fDictOrNew( thePermissionsCache)
        unRolesCache       = fDictOrNew( theRolesCache)

        unInforme = aTRAgvSIGi18n_tool.fNewVoidExportParametersCandidateValues( theContextualElement=theContextualObject)
        

        someConfiguracionMetaAndValues = aTRAgvSIGi18n_tool.fObtenerConfigurationMetaAndValues( 
            theContextualElement     =theContextualObject,
            theAspectoConfiguracion  =cTRAConfiguracionAspecto_Exportacion,
        )
        
        someConfiguracionMetaAndValuesDict = { }
        for aMetaAndValue in someConfiguracionMetaAndValues:
            if len( aMetaAndValue) > 1:
                anAttributeName  = aMetaAndValue[ 0]
                if anAttributeName:
                    someConfiguracionMetaAndValuesDict[ anAttributeName] = aMetaAndValue
            
                    
        
        unExportFormat = ''
        
        if someConfiguracionMetaAndValuesDict:
        
            unExportFormatMetaAndValue = someConfiguracionMetaAndValuesDict.get( 'formatoExportacionPorDefecto', None)
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
     

                
            unIncludeManifestMetaAndValue = someConfiguracionMetaAndValuesDict.get( 'incluirManifestPorDefecto', None)
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
                
                
             
            unIncludeLocalesCSVMetaAndValue = someConfiguracionMetaAndValuesDict.get( 'incluirLocalesCSVPorDefecto', None)
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
             
                
                
            unSeparatedModulesMetaAndValue = someConfiguracionMetaAndValuesDict.get( 'modulosPorSeparadoPorDefecto', None)
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
     
                
                
            unExportModuleNamesMetaAndValue = someConfiguracionMetaAndValuesDict.get( 'exportarNombresModulosPorDefecto', None)
            if unExportModuleNamesMetaAndValue:
                unExportModuleNamesVocabulary = unExportModuleNamesMetaAndValue[ 7]
                unExportModuleNames = theParametersInput.get( 'theExportModuleNames', None)
                if not ( unExportModuleNames in unExportModuleNamesVocabulary):
                    unExportModuleNames = unExportModuleNamesMetaAndValue[ 1]
                if not ( unExportModuleNames in unExportModuleNamesVocabulary):
                    unExportModuleNames = unExportModuleNamesVocabulary[ 0]
                unInforme[ 'theExportModuleNames']                   = unExportModuleNames
                unInforme[ 'theExportModuleNames_vocabulary']        = unExportModuleNamesVocabulary
                unInforme[ 'theExportModuleNames_vocabulary_msgids'] = unExportModuleNamesMetaAndValue[ 8]
     
                
                
            unExportStringSourcesMetaAndValue = someConfiguracionMetaAndValuesDict.get( 'exportarFuentesPorDefecto', None)
            if unExportStringSourcesMetaAndValue:
                unExportStringSourcesVocabulary = unExportStringSourcesMetaAndValue[ 7]
                unExportStringSources = theParametersInput.get( 'theExportStringSources', None)
                if not ( unExportStringSources in unExportStringSourcesVocabulary):
                    unExportStringSources = unExportStringSourcesMetaAndValue[ 1]
                if not ( unExportStringSources in unExportStringSourcesVocabulary):
                    unExportStringSources = unExportStringSourcesVocabulary[ 0]
                unInforme[ 'theExportStringSources']                   = unExportStringSources
                unInforme[ 'theExportStringSources_vocabulary']        = unExportStringSourcesVocabulary
                unInforme[ 'theExportStringSources_vocabulary_msgids'] = unExportStringSourcesMetaAndValue[ 8]
     
                

            unExportTranslationsStatusMetaAndValue = someConfiguracionMetaAndValuesDict.get( 'exportarEstadoTraduccionesPorDefecto', None)
            if unExportTranslationsStatusMetaAndValue:
                unExportTranslationsStatusVocabulary = unExportTranslationsStatusMetaAndValue[ 7]
                unExportTranslationsStatus = theParametersInput.get( 'theExportTranslationsStatus', None)
                if not ( unExportTranslationsStatus in unExportTranslationsStatusVocabulary):
                    unExportTranslationsStatus = unExportTranslationsStatusMetaAndValue[ 1]
                if not ( unExportTranslationsStatus in unExportTranslationsStatusVocabulary):
                    unExportTranslationsStatus = unExportTranslationsStatusVocabulary[ 0]
                unInforme[ 'theExportTranslationsStatus']                   = unExportTranslationsStatus
                unInforme[ 'theExportTranslationsStatus_vocabulary']        = unExportTranslationsStatusVocabulary
                unInforme[ 'theExportTranslationsStatus_vocabulary_msgids'] = unExportTranslationsStatusMetaAndValue[ 8]
     
                            
            unTipoArchivoMetaAndValue = someConfiguracionMetaAndValuesDict.get( 'tipoArchivoExportacionPorDefecto', None)
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
                unDefaultLanguageCode = ''
                unDefaultLanguageCodeMetaAndValue = someConfiguracionMetaAndValuesDict.get( 'codigoIdiomaPorDefecto', '')
                if unDefaultLanguageCodeMetaAndValue:
                    unDefaultLanguageCode = unDefaultLanguageCodeMetaAndValue[ 1]
            unInforme[ 'theDefaultLanguageCode'] = unDefaultLanguageCode
            
    
            unDefaultModuleName = theParametersInput.get( 'theDefaultModuleName', None)
            if not unDefaultModuleName:
                unDefaultModuleName = ''
                unDefaultModuleNameMetaAndValue = someConfiguracionMetaAndValuesDict.get( 'nombreModuloPorDefecto', '')
                if unDefaultModuleNameMetaAndValue:
                    unDefaultModuleName = unDefaultModuleNameMetaAndValue[ 1]
            unInforme[ 'theDefaultModuleName'] = unDefaultModuleName
            
            unDefaultDomain = theParametersInput.get( 'theDefaultDomain', None)
            if not unDefaultDomain:
                unDefaultDomain = ''
                unDefaultDomainMetaAndValue = someConfiguracionMetaAndValuesDict.get( 'dominioPorDefecto', '')
                if unDefaultDomainMetaAndValue:
                    unDefaultDomain = unDefaultDomainMetaAndValue[ 1]
            unInforme[ 'theDefaultDomain'] = unDefaultDomain
            
    
    
            unEncodingErrorHandleModeMetaAndValue = someConfiguracionMetaAndValuesDict.get( 'modoGestionErrorCodificacionExportacionPorDefecto', None)
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
                
                
        
            unExportFilenameForGvSIGMetaAndValue = someConfiguracionMetaAndValuesDict.get( 'exportarNombreFicheroParaGvSIGPorDefecto', None)
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
        
            
                
                
                
            unExportarTRACatalogoPorDefectoMetaAndValue = someConfiguracionMetaAndValuesDict.get( 'exportarTRACatalogoPorDefecto', None)
            if unExportarTRACatalogoPorDefectoMetaAndValue:
                unExportarTRACatalogoPorDefectoVocabulary = unExportarTRACatalogoPorDefectoMetaAndValue[ 7]
                unExportarTRACatalogoPorDefecto = theParametersInput.get( 'theExportarTRACatalogo', None)
                if not ( unExportarTRACatalogoPorDefecto in unExportarTRACatalogoPorDefectoVocabulary):
                    unExportarTRACatalogoPorDefecto = unExportarTRACatalogoPorDefectoMetaAndValue[ 1]
                if not ( unExportarTRACatalogoPorDefecto in unExportarTRACatalogoPorDefectoVocabulary):
                    unExportarTRACatalogoPorDefecto = unExportarTRACatalogoPorDefectoVocabulary[ 0]
                unInforme[ 'theExportarTRACatalogo']                    = unExportarTRACatalogoPorDefecto
                unInforme[ 'theExportarTRACatalogo_vocabulary']         = unExportarTRACatalogoPorDefectoVocabulary
                unInforme[ 'theExportarTRACatalogo_vocabulary_msgids']  = unExportarTRACatalogoPorDefectoMetaAndValue[ 8]
                
                
            unExportarTRAConfiguracionesPorDefectoMetaAndValue = someConfiguracionMetaAndValuesDict.get( 'exportarTRAConfiguracionesPorDefecto', None)
            if unExportarTRAConfiguracionesPorDefectoMetaAndValue:
                unExportarTRAConfiguracionesPorDefectoVocabulary = unExportarTRAConfiguracionesPorDefectoMetaAndValue[ 7]
                unExportarTRAConfiguracionesPorDefecto = theParametersInput.get( 'theExportarTRAConfiguraciones', None)
                if not ( unExportarTRAConfiguracionesPorDefecto in unExportarTRAConfiguracionesPorDefectoVocabulary):
                    unExportarTRAConfiguracionesPorDefecto = unExportarTRAConfiguracionesPorDefectoMetaAndValue[ 1]
                if not ( unExportarTRAConfiguracionesPorDefecto in unExportarTRAConfiguracionesPorDefectoVocabulary):
                    unExportarTRAConfiguracionesPorDefecto = unExportarTRAConfiguracionesPorDefectoVocabulary[ 0]
                unInforme[ 'theExportarTRAConfiguraciones']                    = unExportarTRAConfiguracionesPorDefecto
                unInforme[ 'theExportarTRAConfiguraciones_vocabulary']         = unExportarTRAConfiguracionesPorDefectoVocabulary
                unInforme[ 'theExportarTRAConfiguraciones_vocabulary_msgids']  = unExportarTRAConfiguracionesPorDefectoMetaAndValue[ 8]
                
            unExportarTRAParametrosControlProgresoPorDefectoMetaAndValue = someConfiguracionMetaAndValuesDict.get( 'exportarTRAParametrosControlProgresoPorDefecto', None)
            if unExportarTRAParametrosControlProgresoPorDefectoMetaAndValue:
                unExportarTRAParametrosControlProgresoPorDefectoVocabulary = unExportarTRAParametrosControlProgresoPorDefectoMetaAndValue[ 7]
                unExportarTRAParametrosControlProgresoPorDefecto = theParametersInput.get( 'theExportarTRAParametrosControlProgreso', None)
                if not ( unExportarTRAParametrosControlProgresoPorDefecto in unExportarTRAParametrosControlProgresoPorDefectoVocabulary):
                    unExportarTRAParametrosControlProgresoPorDefecto = unExportarTRAParametrosControlProgresoPorDefectoMetaAndValue[ 1]
                if not ( unExportarTRAParametrosControlProgresoPorDefecto in unExportarTRAParametrosControlProgresoPorDefectoVocabulary):
                    unExportarTRAParametrosControlProgresoPorDefecto = unExportarTRAParametrosControlProgresoPorDefectoVocabulary[ 0]
                unInforme[ 'theExportarTRAParametrosControlProgreso']                    = unExportarTRAParametrosControlProgresoPorDefecto
                unInforme[ 'theExportarTRAParametrosControlProgreso_vocabulary']         = unExportarTRAParametrosControlProgresoPorDefectoVocabulary
                unInforme[ 'theExportarTRAParametrosControlProgreso_vocabulary_msgids']  = unExportarTRAParametrosControlProgresoPorDefectoMetaAndValue[ 8]
                
  
            unExportarTRAIdiomasPorDefectoMetaAndValue = someConfiguracionMetaAndValuesDict.get( 'exportarTRAIdiomasPorDefecto', None)
            if unExportarTRAIdiomasPorDefectoMetaAndValue:
                unExportarTRAIdiomasPorDefectoVocabulary = unExportarTRAIdiomasPorDefectoMetaAndValue[ 7]
                unExportarTRAIdiomasPorDefecto = theParametersInput.get( 'theExportarTRAIdiomas', None)
                if not ( unExportarTRAIdiomasPorDefecto in unExportarTRAIdiomasPorDefectoVocabulary):
                    unExportarTRAIdiomasPorDefecto = unExportarTRAIdiomasPorDefectoMetaAndValue[ 1]
                if not ( unExportarTRAIdiomasPorDefecto in unExportarTRAIdiomasPorDefectoVocabulary):
                    unExportarTRAIdiomasPorDefecto = unExportarTRAIdiomasPorDefectoVocabulary[ 0]
                unInforme[ 'theExportarTRAIdiomas']                    = unExportarTRAIdiomasPorDefecto
                unInforme[ 'theExportarTRAIdiomas_vocabulary']         = unExportarTRAIdiomasPorDefectoVocabulary
                unInforme[ 'theExportarTRAIdiomas_vocabulary_msgids']  = unExportarTRAIdiomasPorDefectoMetaAndValue[ 8]
                  

            unExportarTRASolicitudesCadenasPorDefectoMetaAndValue = someConfiguracionMetaAndValuesDict.get( 'exportarTRASolicitudesCadenasPorDefecto', None)
            if unExportarTRASolicitudesCadenasPorDefectoMetaAndValue:
                unExportarTRASolicitudesCadenasPorDefectoVocabulary = unExportarTRASolicitudesCadenasPorDefectoMetaAndValue[ 7]
                unExportarTRASolicitudesCadenasPorDefecto = theParametersInput.get( 'theExportarTRASolicitudesCadenas', None)
                if not ( unExportarTRASolicitudesCadenasPorDefecto in unExportarTRASolicitudesCadenasPorDefectoVocabulary):
                    unExportarTRASolicitudesCadenasPorDefecto = unExportarTRASolicitudesCadenasPorDefectoMetaAndValue[ 1]
                if not ( unExportarTRASolicitudesCadenasPorDefecto in unExportarTRASolicitudesCadenasPorDefectoVocabulary):
                    unExportarTRASolicitudesCadenasPorDefecto = unExportarTRASolicitudesCadenasPorDefectoVocabulary[ 0]
                unInforme[ 'theExportarTRASolicitudesCadenas']                    = unExportarTRASolicitudesCadenasPorDefecto
                unInforme[ 'theExportarTRASolicitudesCadenas_vocabulary']         = unExportarTRASolicitudesCadenasPorDefectoVocabulary
                unInforme[ 'theExportarTRASolicitudesCadenas_vocabulary_msgids']  = unExportarTRASolicitudesCadenasPorDefectoMetaAndValue[ 8]
                              
                    
            unExportarTRAModulosPorDefectoMetaAndValue = someConfiguracionMetaAndValuesDict.get( 'exportarTRAModulosPorDefecto', None)
            if unExportarTRAModulosPorDefectoMetaAndValue:
                unExportarTRAModulosPorDefectoVocabulary = unExportarTRAModulosPorDefectoMetaAndValue[ 7]
                unExportarTRAModulosPorDefecto = theParametersInput.get( 'theExportarTRAModulos', None)
                if not ( unExportarTRAModulosPorDefecto in unExportarTRAModulosPorDefectoVocabulary):
                    unExportarTRAModulosPorDefecto = unExportarTRAModulosPorDefectoMetaAndValue[ 1]
                if not ( unExportarTRAModulosPorDefecto in unExportarTRAModulosPorDefectoVocabulary):
                    unExportarTRAModulosPorDefecto = unExportarTRAModulosPorDefectoVocabulary[ 0]
                unInforme[ 'theExportarTRAModulos']                    = unExportarTRAModulosPorDefecto
                unInforme[ 'theExportarTRAModulos_vocabulary']         = unExportarTRAModulosPorDefectoVocabulary
                unInforme[ 'theExportarTRAModulos_vocabulary_msgids']  = unExportarTRAModulosPorDefectoMetaAndValue[ 8]
              
                
            unExportarTRAInformesPorDefectoMetaAndValue = someConfiguracionMetaAndValuesDict.get( 'exportarTRAInformesPorDefecto', None)
            if unExportarTRAInformesPorDefectoMetaAndValue:
                unExportarTRAInformesPorDefectoVocabulary = unExportarTRAInformesPorDefectoMetaAndValue[ 7]
                unExportarTRAInformesPorDefecto = theParametersInput.get( 'theExportarTRAInformes', None)
                if not ( unExportarTRAInformesPorDefecto in unExportarTRAInformesPorDefectoVocabulary):
                    unExportarTRAInformesPorDefecto = unExportarTRAInformesPorDefectoMetaAndValue[ 1]
                if not ( unExportarTRAInformesPorDefecto in unExportarTRAInformesPorDefectoVocabulary):
                    unExportarTRAInformesPorDefecto = unExportarTRAInformesPorDefectoVocabulary[ 0]
                unInforme[ 'theExportarTRAInformes']                    = unExportarTRAInformesPorDefecto
                unInforme[ 'theExportarTRAInformes_vocabulary']         = unExportarTRAInformesPorDefectoVocabulary
                unInforme[ 'theExportarTRAInformes_vocabulary_msgids']  = unExportarTRAInformesPorDefectoMetaAndValue[ 8]
                          
                     
                
                
                
                
                
        unProductName = theParametersInput.get( 'theProductName', None)
        if not unProductName:
            unProductName = aTRAgvSIGi18n_tool.fCatalogoNombreProducto( 
                theContextualElement = theContextualObject,
            )
        unInforme[ 'theProductName'] = unProductName
        
        unProductVersion = theParametersInput.get( 'theProductVersion', None)
        if not unProductVersion:
            unProductVersion = cDefaultProductVersionForGvSIGExportFilename
        unInforme[ 'theProductVersion'] = unProductVersion
        
        unL10NVersion = theParametersInput.get( 'theL10NVersion', None)
        if not unL10NVersion:
            unL10NVersion = cDefaultL10NVersionForGvSIGExportFilename
        unInforme[ 'theL10NVersion'] = unL10NVersion
            
            
        unInformeIdiomasYModulos = aTRAgvSIGi18n_tool.fInformeTitulosIdiomasConIdiomaReferenciaYModulosPermitidos( 
            theContextualElement     =theContextualObject,
            theUseCaseName           =cUseCase_Export, 
            thePermissionsCache      =unPermissionsCache, 
            theRolesCache            =unRolesCache, 
            theParentExecutionRecord =unExecutionRecord,
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
        
        unosCodigosIdiomasReferenciaSolicitados = theParametersInput.get( 'theCodigosIdiomaReferencia', {})
        unosCodigosIdiomasReferencia = { }
        unInforme[ 'theCodigosIdiomaReferencia'] = unosCodigosIdiomasReferencia
        
        unosEncodingsSolicitados = theParametersInput.get( 'theCodificacionesCaracteres', {})
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
                          
                        
                        
                    unosEncodingsForLanguage = aTRAgvSIGi18n_tool.fEncodingsForLanguage( 
                        theContextualElement    =theContextualObject,
                        theCodigoIdioma         =unCodigoIdioma,
                    )
                     
                    unosEncodingsNamesForLanguage = []
                    if unosEncodingsForLanguage:
                        unosEncodingsPorCodigoIdioma[ unCodigoIdioma] = unosEncodingsForLanguage
                        unosEncodingsNamesForLanguage = [ unEncodingNameTitleAndAliases[ 0] for unEncodingNameTitleAndAliases in unosEncodingsForLanguage]

                    unEncodingSolicitado = unosEncodingsSolicitados.get( unCodigoIdioma, '')
                    if not unEncodingSolicitado or not ( unEncodingSolicitado in unosEncodingsNamesForLanguage):
                        if unExportFormat and ( unExportFormat == cExportFormatOption_JavaProperties):
                            unEncodingSolicitado = unInformeIdioma.get( 'juego_caracteres_javaproperties', '').lower()
                        else:
                            unEncodingSolicitado = unInformeIdioma.get( 'juego_caracteres_po', '').lower()
                            
                    if not unEncodingSolicitado or not ( unEncodingSolicitado in unosEncodingsNamesForLanguage):
                        unEncodingSolicitado = cTRAEncodingUTF8
                        
                    if unEncodingSolicitado and ( unEncodingSolicitado in unosEncodingsNamesForLanguage): 
                        unosEncodingsAUtilizar[ unCodigoIdioma] =  unEncodingSolicitado   
                                                 
                         
        return unInforme
         

    finally:
        unExecutionRecord and unExecutionRecord.pEndExecution()
                      
                
      


              