# -*- coding: utf-8 -*-
#
# File: TRAElemento_Constants.py
#
# Copyright (c) 2008, 2009,2010 by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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


# #######################################
"""Obsolete: now done with try:except: To deliver a build compatible with MDD version 1.0.2,
and locate key pieces of code changed for MDD versions 1.0.3 and after
"""
#cMDDVersionBackwardsCompatible_102 = True





cNewStringSymbol_AcceptableNonAlphanumericChars = '-_'


cInitializeAllow_CreateModelDDvlPloneTool          = True
cInitializeAllow_CreateModelDDvlPloneConfiguration = True


# #######################################
"""Initial value of global to ignore all profiling service requests.

"""
cTRAExecutionProfilingIgnored       = False

"""Names of configuration properties of execution profile capture, rendering and logging. 

"""   
cTRAExecutionProfilingEnablementConfiguration_PropertyNames = [
    'execution_profiling_enabled',
    'execution_timestamping_enabled',
    'execution_auto_root_record_enabled',
    'execution_logging_enabled',
    'execution_logging_detailed_enabled',
    'execution_rendering_enabled',
    'timestamp_rendering_enabled',
]


"""Initial values for configuration of the GLOBAL execution profile capture, rendering and logging. Set to False for production.

"""
cTRAExecutionProfilingEnabled       = True
cTRAExecutionTimestampingEnabled    = True
cTRAExecutionAutoRootRecordEnabled  = True
cTRAExecutionLoggingEnabled         = True
cTRAExecutionLoggingDetailedEnabled = True
cTRAExecutionRenderingEnabled       = True
cTRATimestampRenderingEnabled       = True


"""Key for global execution profiling enablement configuration.

"""
cTRAExecutionProfilingEnablementConfiguration_Global    = '::ExecutionProfilingEnablementConfiguration_Global::'




# #######################################
"""Configuration of detailed execution logging.
When true, the execution time profiling will be logged.
Note that when enabled, the log file will grow very fast.
"""

cLogTranslationChanges           = False
cLogExceptions                   = True
cTimeStampingEnabled             = True
cTimeProfilingEnabled            = True





cLogResetPermissionsProgress         = True
cLogResetPermissionsProgressInterval = 5000
cLogResetPermissionsResult           = True


cLogRecatalogProgress                = True
cLogRecatalogProgressInterval        = 5000
cLogRecatalogResult                  = True



cLogDeleteModuleProgress             = True
cLogDeleteModuleInterval             = 5000
cLogDeleteModuleResult               = True




"""# #######################################
Default values for configurable properties 
to be set by manager at runtime on the root TRACAtalogo instance...
The values for new instances are specified with same values as here
in the TRACatalogo schema fields as the fields' initialValue 
Because the schema is generated from a model, please modify the  model and regenerate
"""

"""# #######################################
When true, some restrictions are not enforced, to facilitate the developpers or debuggers work
    For example, 
       when true, import operations are allowed on an import process that did already start sometime in the past,
       on the developper's or debugger's responsibility of not launching an on-going process,
       (while import is not allowed when not in develoment of debug, for import processes that started already).

"""
cUnderDevelopmentOrDebug = False



"""# #######################################
Default Block size : number of translations of the main language to retrieve in a single page

"""
cDefaultTraduccionesPorPagina       = 40



"""# #######################################
Maximum number of records retrieved 
The  maximum number of translations of the main language to retrieve in a single page
is this number divided by the number of selected reference languages + 1
i.e., if there is no reference language slected, then a page can contain up to 1000 tranlations in the main language
# if there are 4 reference languages selected, then a page can contain up to 1000 / ( 4 + 1) = 1000 / 5 = 200 tranlations of the main language

"""
cMaximoRegistrosExplorados   = 1000




"""# #######################################
Character used to separate multiple module names in TRACadena and TRASolicitudCadena, usually an space character

"""
cTRAModuleNameSeparator = ' ' # A string with just a space character 


"""# #######################################
Zope/Plone Anonymous user id 

"""
cTRAMemberIdAnonymousUser = 'Anonymous User'



# #######################################
# Interaction modes
#

cInteractionMode_Asynchronous       = 'Asincrono'
cInteractionMode_Synchronous        = 'Sincrono'


"""# #######################################
Default Interaction mode.
The user may change this value from the options section of the translations browser

"""
cInteractionMode_Default            = cInteractionMode_Asynchronous


"""# #######################################
Default Language Code.
Code of the language whose Java .properties import or export files do not contain the language code in the file name as a suffix.
The value is set in the class schema field initial value

"""
cDefaultLanguage = "es"



# ACV 20100721 Do not default to any module name (used to be 'base')
#"""# #######################################
#Module name to use as default when importing files where no module name can be obtained, 
#If the domain is not specified in the GNU gettext .PO file header
#If the uploaded file is not an archive, or a .properties file in the archive is not within a folder to use as module name
#The value is set in the class schema field initial value
#"""
#cDefaultModule = "base"

   
"""# ##############################################
Max number of lines in imported Java .properties  files

"""
cPropertiesMaxLinesToScan = 10000



"""# ##############################################
 Max number of lines in imported  GNU gettext PO  files

"""
cPOMaxLinesToScan = 50000




# #######################################
# END Configurable properties to be set by manager at runtime ...






cCookieName_RenderConnectedUserAssessment = "TRAcookie_RenderConnectedUserAssessment"


cCookieName_RenderExecutionProfile        = "TRAcookie_RenderExecutionProfile"









# #######################################
# Keys used to supply specific language information when creating languages not well-known to Plone
#   
cAcceptedLanguageDetailKeys   = [
    'codigo_internacional_idioma',
    'english_name',
    'nombre_nativo_de_idioma',
]
   

# #######################################
# UI actions
#
cAccion_Traducir                     = 'Traducir'
cAccion_InvalidarTraduccionesCadena  = 'InvalidarTraduccionesCadena'
cAccion_DesactivarCadena             = 'DesactivarCadena'
cAccion_ActivarCadena                = 'ActivarCadena'




# #######################################
# Condition codes for change and browse translations
#

cResultCondition_Internal_MissingParameter                      = 'gvSIGi18n_ResultCondition_Internal_MissingParameter'
cResultCondition_Internal_Exception                             = 'gvSIGi18n_ResultCondition_Internal_Exception'

cResultCondition_MissingParameter                               = 'gvSIGi18n_ResultCondition_MissingParameter'
cResultCondition_MissingParameter_CodigoIdioma                  = 'gvSIGi18n_ResultCondition_MissingParameter_CodigoIdioma'
cResultCondition_MissingParameter_IdCadena                      = 'gvSIGi18n_ResultCondition_MissingParameter_IdCadena'

cResultCondition_UseCaseAssessmentFailure_BrowseTranslations    = 'gvSIGi18n_ResultCondition_UseCaseAssessmentFailure_BrowseTranslations'

cResultCondition_LanguageNotAccessible                          = 'gvSIGi18n_ResultCondition_LanguageNotAccessible'

cResultCondition_NoModulesAccessible                            = 'gvSIGi18n_ResultCondition_NoModulesAccessible'

cResultCondition_NoMatchingTranslationsFound                    = 'gvSIGi18n_ResultCondition_NoMatchingTranslationsFound'

cResultCondition_SomeEncodingErrors                             = 'gvSIGi18n_ResultCondition_SomeEncodingErrors'
cResultCondition_Encoding_NotAvailable                          = 'gvSIGi18n_ResultCondition_Encoding_NotAvailable'
cResultCondition_Encoding_ErrorInHeader                         = 'gvSIGi18n_ResultCondition_Encoding_ErrorInHeader'
cResultCondition_Encoding_ErrorInTranslations                   = 'gvSIGi18n_ResultCondition_Encoding_ErrorInTranslations'
cResultCondition_Encoding_FailureFromSystemToUnicode            = 'gvSIGi18n_ResultCondition_Encoding_FromSystemToUnicode'
cResultCondition_Encoding_FailureFromUnicodeToUTF8              = 'gvSIGi18n_ResultCondition_Encoding_FromUnicodeToUTF8'

cResultCondition_NoTranslationsToExport                         = 'gvSIGi18n_ResultCondition_NoTranslationsToExport'


cEncodingASCII= 'ascii'
cEncodingUTF8   = 'utf-8'
cEncodingUTF16  = 'utf-16'
cEncodingLatin  = 'ISO-8859-1'

cEncodingUnicodeEscape   = 'unicode_escape'

cMaxUnescapedCharOrdinal = 126





cTranslationStatus_DifferentChangeCounter = 'DifferentChangeCounter'

cRequestedChangeKind_IntentarTraducir   = 'TryToTranslate'
cRequestedChangeKind_Comentar           = 'Comment'
cRequestedChangeKind_HacerPendiente     = 'ChangeToPending'
cRequestedChangeKind_HacerTraducida     = 'ChangeToTranslated'
cRequestedChangeKind_HacerRevisada      = 'ChangeToReviewed'
cRequestedChangeKind_HacerDefinitiva    = 'ChangeToLocked'
cRequestedChangeKind_BatchCambioEstado  = 'BatchStatusChange'
cRequestedChangeKind_InvalidarTraduccionesCadena = 'InvalidarTraduccionesCadena'
cRequestedChangeKind_DesactivarCadena   = 'DesactivarCadena'
cRequestedChangeKind_ActivarCadena      = 'ActivarCadena'

cRequestedChangeKinds = [
    cRequestedChangeKind_IntentarTraducir,  
    cRequestedChangeKind_Comentar,          
    cRequestedChangeKind_HacerPendiente,    
    cRequestedChangeKind_HacerTraducida,    
    cRequestedChangeKind_HacerRevisada,     
    cRequestedChangeKind_HacerDefinitiva,     
    cRequestedChangeKind_InvalidarTraduccionesCadena,       
    cRequestedChangeKind_DesactivarCadena,
    cRequestedChangeKind_ActivarCadena,
]


cI18NDomainPlone =  'plone'
cI18NDomainDefault = cI18NDomainPlone

cSystemFileTextEncoding_Unix        = cEncodingUTF8
cSystemFileTextEncoding_Innombrable = cEncodingLatin

cSystemFileTextEncoding          = cSystemFileTextEncoding_Innombrable
cProgramTextEncoding             = cSystemFileTextEncoding_Unix

cDefaultTextEncoding             = cProgramTextEncoding


cTRAFlagIdiomaDesconocida = 'tra_flag-ninguna.gif'
 


cNombreTipoTRACatalogo                  = "TRACatalogo"
cNombreTipoTRAIdioma                    = "TRAIdioma"
cNombreTipoTRAModulo                    = "TRAModulo"
cNombreTipoTRACadena                    = "TRACadena"
cNombreTipoTRATraduccion                = "TRATraduccion"
cNombreTipoTRAImportacion               = "TRAImportacion"
cNombreTipoTRAContenidoIntercambio      = "TRAContenidoIntercambio"
cNombreTipoTRAInforme                   = "TRAInforme"
cNombreTipoTRASolicitudCadena           = "TRASolicitudCadena"
cNombreTipoTRAProgreso                  = "TRAProgreso"
cNombreTipoTRAParametrosControlProgreso = "TRAParametrosControlProgreso"
cNombreTipoTRAColeccionIdiomas          = "TRAColeccionIdiomas"
cNombreTipoTRAColeccionModulos          = "TRAColeccionModulos"
cNombreTipoTRAColeccionCadenas          = "TRAColeccionCadenas"
cNombreTipoTRAColeccionInformes         = "TRAColeccionInformes"
cNombreTipoTRAColeccionImportaciones    = "TRAColeccionImportaciones"
cNombreTipoTRAColeccionSolicitudesCadenas= "TRAColeccionSolicitudesCadenas"
cNombreTipoTRAColeccionProgresos        = "TRAColeccionProgresos"

# cNombreTipo_cualquiera   = '--AnyType--'

cPreferredTypesOrder = [
    cNombreTipoTRACatalogo,               
    cNombreTipoTRAColeccionIdiomas,       
    cNombreTipoTRAIdioma,                 
    cNombreTipoTRAColeccionModulos,       
    cNombreTipoTRAModulo,                 
    cNombreTipoTRAColeccionCadenas,       
    cNombreTipoTRACadena,                 
    cNombreTipoTRATraduccion,             
    cNombreTipoTRAColeccionImportaciones, 
    cNombreTipoTRAImportacion, 
    cNombreTipoTRAContenidoIntercambio,   
    cNombreTipoTRAColeccionInformes,      
    cNombreTipoTRAInforme,      
    cNombreTipoTRAColeccionSolicitudesCadenas,
    cNombreTipoTRASolicitudCadena,
    cNombreTipoTRAColeccionProgresos,
    cNombreTipoTRAProgreso,
    cNombreTipoTRAParametrosControlProgreso,
]


cTodosNombresTiposCacheables = [
    cNombreTipoTRACatalogo,               
    cNombreTipoTRAColeccionIdiomas,       
    cNombreTipoTRAIdioma,                 
    cNombreTipoTRAColeccionModulos,       
    cNombreTipoTRAModulo,                 
    cNombreTipoTRAColeccionCadenas,       
    cNombreTipoTRAColeccionImportaciones, 
    cNombreTipoTRAImportacion, 
    cNombreTipoTRAContenidoIntercambio,   
    cNombreTipoTRAColeccionInformes,      
    cNombreTipoTRAInforme,      
    cNombreTipoTRAColeccionSolicitudesCadenas,
    cNombreTipoTRASolicitudCadena,
    cNombreTipoTRAColeccionProgresos,
    cNombreTipoTRAProgreso,
    cNombreTipoTRAParametrosControlProgreso,
]


cTodosNombresTiposColecciones = [
    cNombreTipoTRAColeccionIdiomas,       
    cNombreTipoTRAColeccionModulos,       
    cNombreTipoTRAColeccionCadenas,       
    cNombreTipoTRAColeccionInformes,      
    cNombreTipoTRAColeccionImportaciones, 
    cNombreTipoTRAColeccionSolicitudesCadenas,
    cNombreTipoTRAColeccionProgresos,
]


cTodosNombresTiposCompuestos = [
    cNombreTipoTRACatalogo,               
    cNombreTipoTRAIdioma,                 
    cNombreTipoTRAModulo,                 
    cNombreTipoTRACadena,                 
    cNombreTipoTRAImportacion, 
]

cTodosNombresTiposWithChildren = cTodosNombresTiposColecciones + cTodosNombresTiposCompuestos

cTodosNombresTiposWithoutChildren = [
    cNombreTipoTRATraduccion,             
    cNombreTipoTRAContenidoIntercambio,   
    cNombreTipoTRAInforme,    
    cNombreTipoTRASolicitudCadena,
    cNombreTipoTRAProgreso,
    cNombreTipoTRAParametrosControlProgreso,
 ]



cTodosNombresTipos = cPreferredTypesOrder


cTodosNombresTiposWithPotentiallyManyChildren = [
    cNombreTipoTRACatalogo,               
    cNombreTipoTRAColeccionCadenas,       
    cNombreTipoTRAColeccionImportaciones, 
]


cTodosNombresTiposWithoutPotentiallyManyChildren = [ aTypeName for aTypeName in cPreferredTypesOrder if not ( aTypeName in cTodosNombresTiposWithPotentiallyManyChildren)]


cTodosNombresTiposWithChildrenOrRelationsOrPloneElements = cTodosNombresTiposWithChildren + [
    cNombreTipoTRAContenidoIntercambio,   
    cNombreTipoTRAInforme,    
    cNombreTipoTRASolicitudCadena,
    cNombreTipoTRAInforme,
    cNombreTipoTRAProgreso,
    cNombreTipoTRAParametrosControlProgreso,
]







cNombreTraversal_Importacion_ContenidosIntercambio = 'contenido'




cCadenaIdPrefix = 'ca-'
cIdiomaIdPrefix = 'la-'
cModuloIdPrefix = 'mo-'
cSolicitudCadenaIdPrefix = 'sc-'

cEstadoCadenaActiva         = 'Activa'
cEstadoCadenaInactiva       = 'Inactiva'

cTodosEstadosCadena = [ cEstadoCadenaActiva, cEstadoCadenaInactiva, ]


cEstadoTraduccionPendiente  = 'Pendiente'
cEstadoTraduccionTraducida  = 'Traducida'
cEstadoTraduccionRevisada   = 'Revisada'
cEstadoTraduccionDefinitiva = 'Definitiva'

cTodosEstados = [ cEstadoTraduccionPendiente, cEstadoTraduccionTraducida, cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva, ]




cEstadoSolicitudCadenaPendiente   = 'Pendiente'
cEstadoSolicitudCadenaDescartada  = 'Descartada'
cEstadoSolicitudCadenaCreada      = 'Creada'

cTodosEstadosSolicitudCadena = [ cEstadoSolicitudCadenaPendiente, cEstadoSolicitudCadenaDescartada, cEstadoSolicitudCadenaCreada, ]





cNombreModuloNoEspecificadoLabel_MsgId  = 'gvSIGi18n_ModuloNoEspecificado_msgid'

cNombreModuloNoEspecificadoInputValue   = '--unspecified--'

cNombreModuloNoEspecificadoSentinel     = ' unspecified'


cLanguageSeparatorCountry = '-'



cIndent = " " * 4




cISOStringFechaYHoraSeparator = ' '
cISOStringFechaYMDSeparator   = '-'
cISOStringHoraHMSSeparator   = ':'
cISOStringEarliestDayTime    = '00:00:00'
cISOStringLatestDayTime      = '23:59:59'
cFirstYearForSearches        = 1000
cLastYearForSearches         = 9999
cFirstMonthForSearches       = 1
cLastMonthForSearches        = 12
cFirstDayForSearches         = 1
cFirstHourForSearches        = 0
cLastHourForSearches         = 23
cFirstMinuteForSearches      = 0
cLastMinuteForSearches       = 59
cFirstSecondForSearches      = 0
cLastSecondForSearches       = 59









# ##############################################
"""Actions recorded in the history of changes of each translation.

"""
cTranslationHistoryAction_Importar       = 'Importar'
cTranslationHistoryAction_Ignorar        = 'Ignorar'
cTranslationHistoryAction_Traducir       = 'Traducir'
cTranslationHistoryAction_Comentar       = 'Comentar'
cTranslationHistoryAction_HacerPendiente = 'HacerPendiente'
cTranslationHistoryAction_HacerTraducida = 'HacerTraducida'
cTranslationHistoryAction_HacerRevisada  = 'HacerRevisada'
cTranslationHistoryAction_HacerDefinitiva= 'HacerDefinitiva'
cTranslationHistoryAction_Invalidar      = 'Invalidar'
cTranslationHistoryAction_IntentarTraducirDifferentCounter       = 'IntentarTraducirDifferentCounter'

cTranslationHistoryActions = [
    cTranslationHistoryAction_Importar,       
    cTranslationHistoryAction_Ignorar ,       
    cTranslationHistoryAction_Traducir,       
    cTranslationHistoryAction_Comentar,       
    cTranslationHistoryAction_HacerPendiente, 
    cTranslationHistoryAction_HacerTraducida, 
    cTranslationHistoryAction_HacerRevisada,  
    cTranslationHistoryAction_HacerDefinitiva,
    cTranslationHistoryAction_Invalidar,      
]





# ##############################################
"""Actions recorded in the global list of recent changes 

"""
cRecentActivity_Date      = 'Date'
cRecentActivity_User      = 'User'
cRecentActivity_Language  = 'Lang'
cRecentActivity_Symbol    = 'Symb'
cRecentActivity_Action    = 'Actn'
cRecentActivity_Commented = 'Cmnt'
cRecentActivity_Counter   = 'Cntr'

cTranslationRecentChanges = [
    cRecentActivity_Date,       
    cRecentActivity_User ,       
    cRecentActivity_Language,       
    cRecentActivity_Symbol,       
    cRecentActivity_Action, 
    cRecentActivity_Commented, 
    cRecentActivity_Counter,
]


cActivityReport_Period_Today             = 'Today'
cActivityReport_Period_Yesterday         = 'Yesterday'
cActivityReport_Period_Last7Days         = 'Last7Days'
cActivityReport_Period_Last30Days        = 'Last30Days'
cActivityReport_Period_Before30Days      = 'Before30Days'

cActivityReport_Periods = [
    cActivityReport_Period_Today,
    cActivityReport_Period_Yesterday,
    cActivityReport_Period_Last7Days,
    cActivityReport_Period_Last30Days,
    cActivityReport_Period_Before30Days,
]







# #############################################################
"""Ids and Titles of the progress control parameters singleton elements.

"""
cTRAParametrosControlProgreso_Inventario_Id              = "parametros-control-progreso-inventario"
cTRAParametrosControlProgreso_Inventario_Title           = "Inventory Progress Control Parameters"
cTRAParametrosControlProgreso_Recatalogar_Id             = "parametros-control-progreso-recatalogar"
cTRAParametrosControlProgreso_Recatalogar_Title          = "ReCatalog Progress Control Parameters"
cTRAParametrosControlProgreso_ReestablecerPermisos_Id    = "parametros-control-progreso-reestablecerpermisos"
cTRAParametrosControlProgreso_ReestablecerPermisos_Title = "Reset Permissions Progress Control Parameters"
cTRAParametrosControlProgreso_DeleteModule_Id            = "parametros-control-progreso-deletemodule"
cTRAParametrosControlProgreso_DeleteModule_Title         = "Delete Module Progress Control Parameters"
cTRAParametrosControlProgreso_DeleteLanguage_Id          = "parametros-control-progreso-deletelanguage"
cTRAParametrosControlProgreso_DeleteLanguage_Title       = "Delete Language Progress Control Parameters"
cTRAParametrosControlProgreso_Backup_Id                  = "parametros-control-progreso-backup"
cTRAParametrosControlProgreso_Backup_Title               = "Backup Progress Control Parameters"
cTRAParametrosControlProgreso_ExportGvSIG_Id             = "parametros-control-progreso-exportgvsig"
cTRAParametrosControlProgreso_ExportGvSIG_Title          = "Export for gvSIG Progress Control Parameters"
cTRAParametrosControlProgreso_Export_Id                  = "parametros-control-progreso-export"
cTRAParametrosControlProgreso_Export_Title               = "Export Progress Control Parameters"
cTRAParametrosControlProgreso_Import_Id                  = "parametros-control-progreso-import"
cTRAParametrosControlProgreso_Import_Title               = "Import Progress Control Parameters"




# ##############################################
"""Progress Process types, and progress support conditions for target element types.
A Long lived process of the given type shall be supported by a persistent instance of TRAProgreso when the condition is met.
Conditions are currently expressed as predicates on the type of the element given as root target for the long-lived process.

"""

# ##############################################

"""Configurable parameters for long-lived process progress support 

"""
cTRAProgress_LogLongLivedProcess   = True

cTRAYieldProcessorEnabled           = True

cTRAProgress_MaxTimePercentageToYield = 95
cTRAProgress_MaxMillisecondsToYield   = 5000

cTRAProgress_PauseMilliseconds        = 1000

cTRAProgress_WaitAfterConfigureProcess_Milliseconds  = 2 * cTRAProgress_PauseMilliseconds




# ######################################
"""Allowed progress states.

"""
cTRAProgreso_EstadoProceso_Activo   = 'Activo'
cTRAProgreso_EstadoProceso_Inactivo = 'Inactivo'

cTRAProgreso_EstadoProcesos = [
    cTRAProgreso_EstadoProceso_Activo,
    cTRAProgreso_EstadoProceso_Inactivo,
]



# ######################################
"""Process types.

"""

cTRAProgress_ProcessType_Void             = 'Vacio'
cTRAProgress_ProcessType_Inventory        = 'Inventario'
cTRAProgress_ProcessType_ReCatalog        = 'Re-Catalogar'
cTRAProgress_ProcessType_ResetPermissions = 'Re-Establecer Permisos'
cTRAProgress_ProcessType_DeleteModule     = 'Eliminar Modulo'
cTRAProgress_ProcessType_DeleteLanguage   = 'Eliminar Idioma'
cTRAProgress_ProcessType_Backup           = 'Copia Seguridad'
cTRAProgress_ProcessType_ExportGvSIG      = 'Exportar para gvSIG'
cTRAProgress_ProcessType_Export           = 'Exportar'
cTRAProgress_ProcessType_Import           = 'Importar'

cTRAProgress_ProcessTypes_NonVoid = [
    cTRAProgress_ProcessType_Inventory,
    cTRAProgress_ProcessType_ReCatalog,
    cTRAProgress_ProcessType_ResetPermissions,  
    cTRAProgress_ProcessType_DeleteModule,
    cTRAProgress_ProcessType_DeleteLanguage,
    cTRAProgress_ProcessType_Backup,
    cTRAProgress_ProcessType_ExportGvSIG,
    cTRAProgress_ProcessType_Export,
    cTRAProgress_ProcessType_Import,
]

cTRAProgress_ProcessTypes = [ cTRAProgress_ProcessType_Void,] + cTRAProgress_ProcessTypes_NonVoid 


cTRAParametrosControlProgresoIDs_forProcessTypes = {
    cTRAProgress_ProcessType_Inventory:        cTRAParametrosControlProgreso_Inventario_Id,
    cTRAProgress_ProcessType_ReCatalog:        cTRAParametrosControlProgreso_Recatalogar_Id,
    cTRAProgress_ProcessType_ResetPermissions: cTRAParametrosControlProgreso_ReestablecerPermisos_Id,
    cTRAProgress_ProcessType_DeleteModule:     cTRAParametrosControlProgreso_DeleteModule_Id,
    cTRAProgress_ProcessType_DeleteLanguage:   cTRAParametrosControlProgreso_DeleteLanguage_Id,   
    cTRAProgress_ProcessType_Backup:           cTRAParametrosControlProgreso_Backup_Id,
    cTRAProgress_ProcessType_ExportGvSIG:      cTRAParametrosControlProgreso_ExportGvSIG_Id,
    cTRAProgress_ProcessType_Export:           cTRAParametrosControlProgreso_Export_Id,
    cTRAProgress_ProcessType_Import:           cTRAParametrosControlProgreso_Import_Id,
}



cTRAProgress_ControlRequest_Ignored = 'Ignored'

cTRAProgress_Control_RunAfterPrevious = 'RunAfterPrevious'
cTRAProgress_Control_RunAfterPrevious_Yes = 'Yes'
cTRAProgress_Control_RunAfterPrevious_No  = 'No'

cTRAProgress_SupportKind_None           = 'None'
cTRAProgress_SupportKind_Persistent     = 'Persistent'
cTRAProgress_SupportKind_Logging        = 'Logging'
cTRAProgress_SupportKind_StoreResults   = 'StoreResults'
cTRAProgress_SupportKind_YieldProcessor = 'YieldProcessor'
cTRAProgress_SupportKind_Transactional  = 'Transactional'

cTRAProgress_SupportKinds = [
    cTRAProgress_SupportKind_None,           
    cTRAProgress_SupportKind_Persistent,     
    cTRAProgress_SupportKind_Logging,            
    cTRAProgress_SupportKind_StoreResults,   
    cTRAProgress_SupportKind_YieldProcessor, 
    cTRAProgress_SupportKind_Transactional,  
]



cTRAProgress_SupportKinds_Configurable = [
    cTRAProgress_SupportKind_StoreResults,   
    cTRAProgress_SupportKind_Transactional,  
    cTRAProgress_SupportKind_Logging,            
    cTRAProgress_SupportKind_YieldProcessor, 
]

cTRAProgress_SupportKinds_ToDump = [
    cTRAProgress_SupportKind_StoreResults,   
    cTRAProgress_SupportKind_Transactional,  
    cTRAProgress_SupportKind_Logging,            
    cTRAProgress_SupportKind_YieldProcessor, 
]


cTRAProgress_SupportKinds_ForProcessTypes = {
    cTRAProgress_ProcessType_Void:      [],
    cTRAProgress_ProcessType_Inventory: [
        { 'types': cTodosNombresTiposWithPotentiallyManyChildren,    'support_kinds': [ cTRAProgress_SupportKind_Persistent, cTRAProgress_SupportKind_StoreResults, cTRAProgress_SupportKind_Logging, cTRAProgress_SupportKind_Transactional, cTRAProgress_SupportKind_YieldProcessor, ],},
        { 'types': cTodosNombresTiposWithoutPotentiallyManyChildren, 'support_kinds': [ cTRAProgress_SupportKind_Persistent, cTRAProgress_SupportKind_StoreResults, cTRAProgress_SupportKind_Logging,                                                                                  ],},        
    ],                                                                                                                                                                                                
    cTRAProgress_ProcessType_ReCatalog: [                                                                                                                                                             
        { 'types': cTodosNombresTiposWithPotentiallyManyChildren,    'support_kinds': [ cTRAProgress_SupportKind_Persistent, cTRAProgress_SupportKind_StoreResults, cTRAProgress_SupportKind_Logging, cTRAProgress_SupportKind_Transactional, cTRAProgress_SupportKind_YieldProcessor, ],},
        { 'types': cTodosNombresTiposWithoutPotentiallyManyChildren, 'support_kinds': [ cTRAProgress_SupportKind_Persistent, cTRAProgress_SupportKind_StoreResults, cTRAProgress_SupportKind_Logging,                                                                                  ],},        
    ],                                                                                                                                                                                                
    cTRAProgress_ProcessType_ResetPermissions: [                                                                                                                                                       
        { 'types': cTodosNombresTiposWithPotentiallyManyChildren,    'support_kinds': [ cTRAProgress_SupportKind_Persistent, cTRAProgress_SupportKind_StoreResults, cTRAProgress_SupportKind_Logging, cTRAProgress_SupportKind_Transactional, cTRAProgress_SupportKind_YieldProcessor, ],},
        { 'types': cTodosNombresTiposWithoutPotentiallyManyChildren, 'support_kinds': [ cTRAProgress_SupportKind_Persistent, cTRAProgress_SupportKind_StoreResults, cTRAProgress_SupportKind_Logging,                                                                                  ],},        
    ],
    cTRAProgress_ProcessType_DeleteModule: [                                                                                                                                                       
        { 'types': cTodosNombresTipos,                               'support_kinds': [ cTRAProgress_SupportKind_Persistent, cTRAProgress_SupportKind_StoreResults, cTRAProgress_SupportKind_Logging, cTRAProgress_SupportKind_Transactional, cTRAProgress_SupportKind_YieldProcessor, ],},
    ],
    cTRAProgress_ProcessType_DeleteLanguage: [                                                                                                                                                       
        { 'types': cTodosNombresTipos,                               'support_kinds': [ cTRAProgress_SupportKind_Persistent, cTRAProgress_SupportKind_StoreResults, cTRAProgress_SupportKind_Logging, cTRAProgress_SupportKind_Transactional, cTRAProgress_SupportKind_YieldProcessor, ],},
    ],
    cTRAProgress_ProcessType_Backup: [                                                                                                                                                       
        { 'types': cTodosNombresTipos,                               'support_kinds': [ cTRAProgress_SupportKind_Persistent, cTRAProgress_SupportKind_StoreResults, cTRAProgress_SupportKind_Logging, cTRAProgress_SupportKind_Transactional, cTRAProgress_SupportKind_YieldProcessor, ],},
    ],
    cTRAProgress_ProcessType_ExportGvSIG: [                                                                                                                                                       
        { 'types': cTodosNombresTipos,                               'support_kinds': [ cTRAProgress_SupportKind_Persistent, cTRAProgress_SupportKind_StoreResults, cTRAProgress_SupportKind_Logging, cTRAProgress_SupportKind_Transactional, cTRAProgress_SupportKind_YieldProcessor, ],},
    ],
    cTRAProgress_ProcessType_Export: [                                                                                                                                                       
        { 'types': cTodosNombresTipos,                               'support_kinds': [ cTRAProgress_SupportKind_Persistent, cTRAProgress_SupportKind_StoreResults, cTRAProgress_SupportKind_Logging, cTRAProgress_SupportKind_Transactional, cTRAProgress_SupportKind_YieldProcessor, ],},
    ],
    cTRAProgress_ProcessType_Import: [                                                                                                                                                       
        { 'types': cTodosNombresTipos,                               'support_kinds': [ cTRAProgress_SupportKind_Persistent, cTRAProgress_SupportKind_StoreResults, cTRAProgress_SupportKind_Logging, cTRAProgress_SupportKind_Transactional, cTRAProgress_SupportKind_YieldProcessor, ],},
    ],
    
}




cTRAProcessControl_Action_Execute          = 'Execute'
cTRAProcessControl_Action_Terminate        = 'Terminate'
cTRAProcessControl_Action_Pause            = 'Pause'
cTRAProcessControl_Action_Resume           = 'Resume'
cTRAProcessControl_Action_ChangeParameters = 'ChangeParameters'

cTRAProcessControl_Actions = [
    cTRAProcessControl_Action_Execute,
    cTRAProcessControl_Action_Terminate,
    cTRAProcessControl_Action_Pause,
    cTRAProcessControl_Action_Resume,
    cTRAProcessControl_Action_ChangeParameters,
]

