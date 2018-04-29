# -*- coding: utf-8 -*-
#
# File: TRAImportarExportar_Constants.py
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

import os


from App.config import getConfiguration



from TRAElemento_Constants                 import *
from TRAElemento_Constants_TypeNames       import *
from TRAElemento_Constants_Languages       import *




cManifestFolderName         = 'META-INF'
cManifestFileName           = 'MANIFEST.MF'

cZipPathSeparator  = '/'
cManifestFileFullName       = cManifestFolderName +  cZipPathSeparator + cManifestFileName


cManifestEntryStartLinePrefix                   = 'Name:'
cManifestLocaleLanguageStartLinePrefix          = 'locale-language:'
cManifestLocaleCountryStartLinePrefix           = 'locale-country:'
cManifestReferenceLocaleLanguageStartLinePrefix = 'reference-locale-language:'
cManifestReferenceLocaleCountryStartLinePrefix  = 'reference-locale-country:'



cLocalesCSVFileName           = 'locales.csv'
cLocalesCSVFileFullName       = cLocalesCSVFileName

cLocalesCSVIsReferenceFile    = 'true'


 
# ##############################################
"""Persistence of exported content as file system files.

"""
cTRADefaultReferenceLanguageCode  = cTRALanguageCode_English

cTRAReferenceLanguageCodesForLanguages = {
   cTRALanguageCode_English:     cTRALanguageCode_Spanish,
}




# ##############################################
"""Persistence of exported content as file system files.

"""
cTRAExportedFilesFolderName = 'tra_exports'

cTRAExportedFiles_FolderCreateMode_RootUID   = 077
cTRAExportedFiles_FileOpenReadMode           = 'rb'
cTRAExportedFiles_FileOpenReadBuffering      = 0
cTRAExportedFiles_FileOpenWriteMode          = 'wb'
cTRAExportedFiles_FileOpenWriteBuffering     = 0


cMinWaitBetweenTransactions = 0.1 # seconds

cMaxWaitBetweenTransactions = 60.0 # seconds







# ##############################################
"""Status names for export errors.

"""
cExportStatus_NoModelDDvlPloneTool          = 'gvSIGi18n_ExportStatus_NoModelDDvlPloneTool'
cExportStatus_CanNotStoreExportedFile       = 'gvSIGi18n_ExportStatus_CanNotStoreExportedFile'
cExportStatus_NoExportTypeConfigsChosenForObject  = 'gvSIGi18n_ExportStatus_NoExportTypeConfigsChosenForObject'

cExportStatus_NoLanguagesRequestedForExport = 'gvSIGi18n_ExportStatus_NoLanguagesRequestedForExport'
cExportStatus_NoModulesRequestedForExport   = 'gvSIGi18n_ExportStatus_NoModulesRequestedForExport'
cExportStatus_Exception                     = 'gvSIGi18n_ExportStatus_Exception'
cExportStatus_UseCaseAssessmentFailed       = 'gvSIGi18n_ExportStatus_UseCaseAssessmentFailed'
cExportStatus_NoAvailableLanguagesToExport  = 'gvSIGi18n_ExportStatus_NoAvailableLanguagesToExport'
cExportStatus_NoAvailableModulesToExport    = 'gvSIGi18n_ExportStatus_NoAvailableModulesToExport'
cExportStatus_CanNotCreateZipFile           = 'gvSIGi18n_ExportStatus_CanNotCreateZipFile'







cModuloNoEspecificado_ValorNombre = 'mod-ModuloNoEspecificado'
cModuloNoEspecificado_msgid = 'gvSIGi18n_ModuloNoEspecificado_msgid'
cModuloNoEspecificado_ForArchiveFileName ='unspecified'



cZipFilePostfix  = '.zip'
cJarFilePostfix  = '.jar'
cExportArchiveTypes = [ cZipFilePostfix, cJarFilePostfix, ]

cOutputFilePostfixes = [ cZipFilePostfix, cJarFilePostfix, ]

cOutputFileNameLanguageSeparator = '-'
cOutputFileNameProduct_Separator = '-'
cOutputFileNameModuleSeparator   = '-'

cMaxLenIdiomasOutputFileName = 40
cMaxLenModulosOutputFileName = 68

cExportZipFileNamePrefix       = 'EXPORT'
cExportBackupFileNamePrefix    = 'BACKUP'
cExportBackupFileNameSeparator = '_'



cTRAContenidoExportacionEliminado = ''

cTRAImagePortalType = 'ATImage'



cExportarXMLAnyTypeAttributeConfigs = [
    {   'name': 'title',
                'type': 'String',
    },
    {   'name': 'description',
        'type': 'Text',
    },
    {   'name': 'text',
        'type': 'Text',
    },
]




cExportarXMLTypeConfigFilters = {

    'base':        [
        {   'portal_type': 'TRACatalogo',
        },
    ],
    
    'TRACatalogo':  [
        {   'portal_type': 'TRACatalogo',
            'attrs':       [ 'nombreProducto',],
            'traversals':  [ 'imagenes','archivos','documentos','noticias','enlaces',],
        },
    ],
    
    'TRAConfiguraciones':  [
        {   'portal_type': 'TRACatalogo',
            'traversals':  [ 'configuraciones',],
        },
        {   'portal_type': 'TRAConfiguracionAlmacenPaginas',
            'attrs':       [
                'aspectoConfiguracion', 
                'segundosMinimosRetencionInformeIdiomas', 
                'numeroDeCambiosAnularInformeIdiomas', 
                'segundosMinimosRetencionInformeModulosEIdiomas', 
                'numeroDeCambiosAnularInformeModulosEIdiomas', 
                'numeroDeActividadesAnularInformeActividad', 
                'segundosMinimosRetencionInformeActividad', 
            ],
            'traversals':  [ 'imagenes','archivos','documentos','noticias','enlaces',],
        },
        {   'portal_type': 'TRAConfiguracionImportacion',
            'attrs':       [
                'aspectoConfiguracion', 
                'nombreModuloPorDefecto', 
                'codigoIdiomaPorDefecto', 
                'segundosParaConfirmarImportacion', 
                'importarConNombreModuloConfiguradoPorDefecto', 
                'importarNombresModulosDesdeComentariosPorDefecto', 
                'importarContribucionesDesdeComentariosPorDefecto', 
                'importarNombreModuloDesdeDominioONombreFicheroPorDefecto', 
                'importarFuentesDesdeComentariosPorDefecto', 
                'importarStatusDesdeComentariosPorDefecto', 
                'importarXMLTRACatalogoPorDefecto',
                'importarXMLTRAAConfiguracionesPorDefecto',
                'importarXMLTRAParametrosControlProgresoPorDefecto',
                'importarXMLTRAIdiomasPorDefecto',
                'importarXMLTRASolicitudesCadenasPorDefecto',
                'importarXMLTRAModulosPorDefecto',
                'importarXMLTRAInformesPorDefecto',
                #'importarXMLTRAImportacionesPorDefecto',
                #'importarXMLTRAProgresosPorDefecto',
            ],
            'traversals':  [ 'imagenes','archivos','documentos','noticias','enlaces',],
        },
        {   'portal_type': 'TRAConfiguracionExportacion',
            'attrs':       [
                'aspectoConfiguracion', 
                'nombreModuloPorDefecto', 
                'codigoIdiomaPorDefecto', 
                'formatoExportacionPorDefecto', 
                'incluirLocalesCSVPorDefecto', 
                'incluirManifestPorDefecto', 
                'modulosPorSeparadoPorDefecto', 
                'exportarNombresModulosPorDefecto', 
                'exportarContribucionesPorDefecto', 
                'exportarEstadoTraduccionesPorDefecto', 
                'exportarFuentesPorDefecto', 
                'tipoArchivoExportacionPorDefecto', 
                'modoGestionErrorCodificacionExportacionPorDefecto', 
                'exportarNombreFicheroParaGvSIGPorDefecto', 
                'exportarTRACatalogoPorDefecto',
                'exportarTRAConfiguracionesPorDefecto',
                'exportarTRAParametrosControlProgresoPorDefecto',
                'exportarTRAIdiomasPorDefecto',
                'exportarTRASolicitudesCadenasPorDefecto',
                'exportarTRAModulosPorDefecto',
                'exportarTRAInformesPorDefecto',
            ],
            'traversals':  [ 'imagenes','archivos','documentos','noticias','enlaces',],
        },
        {   'portal_type': 'TRAConfiguracionPaginaTraducciones',
            'attrs':       [
                'aspectoConfiguracion', 
                'traduccionesPorPaginaPorDefecto', 
                'maximoRegistrosExplorados', 
            ],
            'traversals':  [ 'imagenes','archivos','documentos','noticias','enlaces',],
        },
        {   'portal_type': 'TRAConfiguracionPerfilEjecucion',
            'attrs':       [
                'aspectoConfiguracion', 
                'perfilDeEjecucionHabilitado', 
                'tiemposDeEjecucionHabilitado', 
                'registroRaizDeEjecucionAutomaticoHabilitado', 
                'escrituraEnDiscoDeRegistroDeEjecucionHabilitado', 
                'escrituraEnDiscoDeRegistroDeEjecucionDetalladoHabilitado', 
                'presentacionEnPaginasDeRegistroDeEjecucionHabilitado', 
                'presentacionEnPaginasDeTiempoDeEjecucionHabilitado', 
            ],
            'traversals':  [ 'imagenes','archivos','documentos','noticias','enlaces',],
        },
        {   'portal_type': 'TRAConfiguracionPermisos',
            'attrs':       [
                'aspectoConfiguracion', 
                'esAnonymousTRAManager', 
                'esAnonymousTRACoordinator', 
                'esAnonymousTRADeveloper', 
                'esAnonymousTRAReviewer', 
                'esAnonymousTRATranslator', 
                'esAnonymousTRAVisitor', 

                'esAuthenticatedTRAManager', 
                'esAuthenticatedTRACoordinator', 
                'esAuthenticatedTRADeveloper', 
                'esAuthenticatedTRAReviewer', 
                'esAuthenticatedTRATranslator', 
                'esAuthenticatedTRAVisitor', 

                'esMemberTRAManager', 
                'esMemberTRACoordinator', 
                'esMemberTRADeveloper', 
                'esMemberTRAReviewer', 
                'esMemberTRATranslator', 
                'esMemberTRAVisitor', 

                'esReviewerTRAManager', 
                'esReviewerTRACoordinator', 
                'esReviewerTRADeveloper', 
                'esReviewerTRAReviewer', 
                'esReviewerTRATranslator', 
                'esReviewerTRAVisitor', 

                'esOwnerTRAManager', 
                'esOwnerTRACoordinator', 
                'esOwnerTRADeveloper', 
                'esOwnerTRAReviewer', 
                'esOwnerTRATranslator', 
                'esOwnerTRAVisitor', 

                'esManagerTRAManager', 
                'esManagerTRACoordinator', 
                'esManagerTRADeveloper', 
                'esManagerTRAReviewer', 
                'esManagerTRATranslator', 
                'esManagerTRAVisitor', 
                
            ],
            'traversals':  [ 'imagenes','archivos','documentos','noticias','enlaces',],
        },
        {   'portal_type': 'TRAConfiguracionSolicitudesCadenas',
            'attrs':       [
                'aspectoConfiguracion', 
                'codigoIdiomaRequeridoSolicitudesNuevasCadenas', 
                'codigoIdiomaReferenciaSolicitudesNuevasCadenas', 
            ],
            'traversals':  [ 'imagenes','archivos','documentos','noticias','enlaces',],
        },
        {   'portal_type': 'TRAConfiguracionVarios',
            'attrs':       [
                'aspectoConfiguracion', 
                'maximoNumeroCambiosRecientes', 
                'segundosParaConfirmarAccion', 
            ],
            'traversals':  [ 'imagenes','archivos','documentos','noticias','enlaces',],
        },
    ],    


    'TRAParametrosControlProgreso': [
        {   'portal_type': 'TRACatalogo',
            'traversals':  [ 'parametrosControlProgreso',],
        },
        {   'portal_type': 'TRAParametrosControlProgreso',
            'attrs':       [
                'aspectoConfiguracion', 
                'crearInformeAntes', 
                'crearInformeDespues', 
                
                'guardarResultados_habilitado', 
                'guardarResultados_maximoElementosLeidos', 
                'guardarResultados_maximoElementosModificados', 
                'guardarResultados_maximoMilisegundos', 
                
                'transacciones_habilitado', 
                'transacciones_maximoElementosLeidos', 
                'transacciones_maximoElementosModificados', 
                'transacciones_maximoMilisegundos', 
                
                'registro_habilitado', 
                'registro_maximoElementosLeidos', 
                'registro_maximoElementosModificados', 
                'registro_maximoMilisegundos', 
                'registro_maximoTransacciones', 
                
                'cederProcesador_habilitado', 
                'cederProcesador_porcentajeTiempoActividad', 
                'cederProcesador_maximoElementosLeidos', 
                'cederProcesador_maximoElementosModificados', 
                'cederProcesador_maximoMilisegundos', 
            ],
            'traversals':  [ 'imagenes','archivos','documentos','noticias','enlaces',],
        },
    ],
 
    'TRAIdiomas': [
        {   'portal_type': 'TRACatalogo',
            'traversals':  [ 'coleccionIdiomas',],
        },
        {   'portal_type': 'TRAColeccionIdiomas',
            'traversals':       [ 'idiomas', 'imagenes','archivos','documentos','noticias','enlaces',],
        },
        {   'portal_type': 'TRAIdioma',
            'attrs':       [
                'codigoIdiomaEnGvSIG', 
                'codigoInternacionalDeIdioma', 
                'nombreEnInglesDeIdioma', 
                'nombreNativoDeIdioma', 
                'modoSeleccionBandera', 
                'iconoBanderaIdioma', 
                'codigoIdiomaReferencia', 
                'ambitoDelIdioma', 
                'fallbackDeIdiomas', 
                'equipoTraductor', 
                'juegoDeCaracteresParaJavaProperties', 
                'juegoDeCaracteresParaPO', 
                'codificacionTransferenciaContenido', 
                'formasPlurales', 
                'codificacionesPreferidas', 
                'esIdiomaPrincipal', 
            ],
            'traversals': [ 'imagenes','archivos','documentos','noticias','enlaces',],
        },
    ],

    'TRAModulos': [
        {   'portal_type': 'TRACatalogo',
            'traversals':  [ 'coleccionModulos',],
        },
        {   'portal_type': 'TRAColeccionModulos',
            'traversals':       [ 'modulos', 'imagenes','archivos','documentos','noticias','enlaces',],
        },
        {   'portal_type': 'TRAModulo',
            'attrs':       [
                'dominio', 
                'esModuloPrincipal', 
            ],
            'traversals':  [ 'imagenes','archivos','documentos','noticias','enlaces',],
        },
    ],   

    'TRAInformes': [
        {   'portal_type': 'TRACatalogo',
            'traversals':  [ 'coleccionInformes',],
        },
        {   'portal_type': 'TRAColeccionInformes',
            'traversals':       [ 'informes', 'imagenes','archivos','documentos','noticias','enlaces',],
        },
        {   'portal_type': 'TRAInforme',
            'attrs':       [
                'estadoProceso', 
                'haComenzado', 
                'usuarioInformador', 
                'haCompletadoConExito', 
                'fechaComienzoProceso', 
                'fechaFinProceso', 
                'informeExcepcion', 
                'informeIdiomas', 
                'informeExcepcionIdiomas', 
                'informeModulos', 
                'informeExcepcionModulos', 
            ],
            'traversals':  [ 'imagenes','archivos','documentos','noticias','enlaces',],
        },
    ],    
    
    #'TRAImportaciones':  [
        #{   'portal_type': 'TRACatalogo',
            #'traversals':  [ 'coleccionImportaciones',],
        #},
        #{   'portal_type': 'TRAColeccionImportaciones',
            #'traversals':       [ 'importaciones', 'imagenes','archivos','documentos','noticias','enlaces',],
        #},
        #{   'portal_type': 'TRAImportacion',
            #'attrs':       [
                #'esRecuperacion',
                #'codigoIdiomaPorDefecto', 
                #'nombreModuloPorDefecto', 
                #'importarConNombreModuloConfigurado', 
                #'importarNombreModuloDesdeDominioONombreFichero', 
                #'importarNombresModulosDesdeComentarios', 
                #'importarFuentesDesdeComentarios', 
                #'importarStatusDesdeComentarios', 
                #'numeroMaximoLineasAExplorar', 
                #'importarXMLTRACatalogo',
                #'importarXMLTRAAConfiguraciones',
                #'importarXMLTRAParametrosControlProgreso',
                #'importarXMLTRAIdiomas',
                #'importarXMLTRASolicitudesCadenas',
                #'importarXMLTRAModulos',
                #'importarXMLTRAInformes',
                #'importarXMLTRAImportaciones',
                #'importarXMLTRAProgresos',
            #],
            #'traversals': [ 'contenidos', 'contenidoXML', 'imagenes','archivos','documentos','noticias','enlaces',],
        #},
        #{   'portal_type': 'TRAContenidoIntercambio',
            #'attrs':       [
                #'excluirDeImportacion', 
                #'usuarioContribuidor', 
                #'fechaContenido', 
                #'ficheroLeido', 
                #'codigoIdiomaPorDefecto', 
                #'nombreModuloPorDefecto', 
                #'importarConNombreModuloConfigurado', 
                #'importarNombreModuloDesdeDominioONombreFichero', 
                #'importarNombresModulosDesdeComentarios', 
                #'importarFuentesDesdeComentarios', 
                #'importarStatusDesdeComentarios', 
                #'numeroMaximoLineasAExplorar', 
                #'contenido',
            #],
            #'traversals':  [ 'imagenes','archivos','documentos','noticias','enlaces',],
        #},
        #{   'portal_type': 'TRAContenidoXML',
            #'attrs':       [
                #'excluirDeImportacion', 
                #'usuarioContribuidor', 
                #'fechaContenido', 
                #'ficheroLeido', 
                #'contenidoBinario',
                #'contenidoXML',
            #],
            #'traversals':  [ 'imagenes','archivos','documentos','noticias','enlaces',],
        #},
    #],    

    #'TRAProgresos':  [
        #{   'portal_type': 'TRACatalogo',
            #'traversals':  [ 'coleccionProgresos',],
        #},
        #{   'portal_type': 'TRAColeccionProgresos',
            #'traversals':       [ 'progresos', 'imagenes','archivos','documentos','noticias','enlaces',],
        #},
        #{   'portal_type': 'TRAProgreso',
            #'attrs':       [
                #'tipoProceso', 
                #'usuarioSolicitante', 
                #'estadoProceso', 
                #'haComenzado', 
                #'haCompletadoConExito', 
                #'fechaComienzoProceso', 
                #'fechaFinProceso', 
                #'direccionServidorEjecutor', 
                #'tipoElementoProceso', 
                #'identificadorElementoProceso', 
                #'clasesSoporte', 
                #'comienzoTipo', 
                #'comienzoTitulo', 
                #'comienzoUID', 
                #'parametrosEntrada', 
                #'parametrosControl', 
                #'contadoresControl', 
                #'datosResultado', 
                #'informeExcepcion', 
            #],
            #'traversals':  [ 'imagenes','archivos','documentos','noticias','enlaces',],
        #},
    #],        
    
    'TRASolicitudesCadenas':  [
        {   'portal_type': 'TRACatalogo',
            'traversals':  [ 'coleccionSolicitudesCadenas',],
        },
        {   'portal_type': 'TRAColeccionSolicitudesCadenas',
            'traversals':       [ 'solicitudesCadenas', 'imagenes','archivos','documentos','noticias','enlaces',],
        },
        {   'portal_type': 'TRASolicitudCadena',
            'attrs':       [
                'simbolo', 
                'estadoSolicitudCadena', 
                'fechaCreacionTextual', 
                'usuarioCreador', 
                'fechaCancelacionTextual', 
                'nombresModulos', 
                'referenciasFuentes', 
                'codigoIdiomaPrincipal', 
                'cadenaTraducidaAIdiomaPrincipal', 
                'codigoIdiomaReferencia', 
                'cadenaTraducidaAIdiomaReferencia', 
            ],
            'traversals':  [ 'imagenes','archivos','documentos','noticias','enlaces',],
        },
    ],        
    
    
           
    
    
    
}


           




# ##############################################
"""Keys for string representation of content read from an interchange file, to be stored in a field in instances of TRAContenidoIntercambio.

"""

cScannedKeys_String_Symbol  = 's'
cScannedKeys_String_Errors  = 'e'
cScannedKeys_String_Modules = 'm'
cScannedKeys_String_Sources = 'so'
cScannedKeys_String_Translations = 't'


cScannedKeys_Translation_Translation = 't'
cScannedKeys_Translation_Errors      = 'e'
cScannedKeys_Translation_Status      = 's'
cScannedKeys_Translation_Flags       = 'f'
cScannedKeys_Translation_Comment     = 'c'


cScannedKeys_Translation_CreationDate    = 'crd'
cScannedKeys_Translation_Creator         = 'ctr'
cScannedKeys_Translation_TranslationDate = 'trd'
cScannedKeys_Translation_Translator      = 'ttr'      
cScannedKeys_Translation_ReviewDate      = 'red'
cScannedKeys_Translation_Reviewer        = 'rwr'      
cScannedKeys_Translation_DefinitiveDate  = 'ded'
cScannedKeys_Translation_Coordinator     = 'ctr'      



cScanError_String_Modules     = 'm'
cScanError_String_Sources     = 's'

cScanError_Translation_Translation = 't'
cScanError_Translation_Status      = 's'
cScanError_Translation_Flags       = 'f'
cScanError_Translation_Comment     = 'c'

cScanError_Translation_CreationDate    = 'crd'
cScanError_Translation_Creator         = 'ctr'
cScanError_Translation_TranslationDate = 'trd'
cScanError_Translation_Translator      = 'ttr'      
cScanError_Translation_ReviewDate      = 'red'
cScanError_Translation_Reviewer        = 'rwr'      
cScanError_Translation_DefinitiveDate  = 'ded'
cScanError_Translation_Coordinator     = 'ctr'      






