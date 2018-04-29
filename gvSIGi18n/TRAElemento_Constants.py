# -*- coding: utf-8 -*-
#
# File: TRAElemento_Constants.py
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



# #######################################
# Interaction modes
#

cInteractionMode_Asynchronous       = 'Asincrono'
cInteractionMode_Synchronous        = 'Sincrono'






"""# #######################################
Configuration of detailed execution logging.

When true, the execution time profiling will be logged.

Note that when enabled, the log file will grow very fast.
"""
cExecutionLoggingEnabled         = False


cLogTranslationChanges           = False


# ACV20090519 removed
#cLogTimeProfile       = True
cLogExceptions                   = True
cTimeStampingEnabled             = True
cTimeProfilingEnabled            = True
cDetailedExecutionLoggingEnabled = True







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
cUnderDevelopmentOrDebug = True



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



"""# #######################################
Default Language Code.
Module name to use as default when importing files where no module name can be obtained, 
If the domain is not specified in the GNU gettext .PO file header
If the uploaded file is not an archive, or a .properties file in the archive is not within a folder to use as module name
The value is set in the class schema field initial value
"""
cDefaultModule = "base"

   
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
# Ok, this is not a constant, but a function,
#  yet it comes handy to put it here
# as this is already imported all over the place
#
def fsIsSomethingOrNonEmptyStringOrSequence( theObject):
    if theObject:
        return True
    if theObject.__class__.__name__ == 'TRAColeccionCadenas':
        return True
    return False

fsISS = fsIsSomethingOrNonEmptyStringOrSequence
    




# cCodigoNingunIdiomaReferencia = ''
# cCodigoNingunIdiomaReferencia = '--no_reference_language--'




# #######################################
# UI actions
#
cAccion_Traducir = 'Traducir'





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




cRequestedChangeKind_IntentarTraducir   = 'TryToTranslate'
cRequestedChangeKind_Comentar           = 'Comment'
cRequestedChangeKind_HacerPendiente     = 'ChangeToPending'
cRequestedChangeKind_HacerTraducida     = 'ChangeToTranslated'
cRequestedChangeKind_HacerRevisada      = 'ChangeToReviewed'
cRequestedChangeKind_HacerDefinitiva    = 'ChangeToLocked'
cRequestedChangeKind_BatchCambioEstado  = 'BatchStatusChange'

cRequestedChangeKinds = [
    cRequestedChangeKind_IntentarTraducir,  
    cRequestedChangeKind_Comentar,          
    cRequestedChangeKind_HacerPendiente,    
    cRequestedChangeKind_HacerTraducida,    
    cRequestedChangeKind_HacerRevisada,     
    cRequestedChangeKind_HacerDefinitiva,         
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
cNombreTipoTRAColeccionIdiomas          = "TRAColeccionIdiomas"
cNombreTipoTRAColeccionModulos          = "TRAColeccionModulos"
cNombreTipoTRAColeccionCadenas          = "TRAColeccionCadenas"
cNombreTipoTRAColeccionInformes         = "TRAColeccionInformes"
cNombreTipoTRAColeccionImportaciones    = "TRAColeccionImportaciones"
cNombreTipoTRAColeccionSolicitudesCadenas    = "TRAColeccionSolicitudesCadenas"

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
]



cTodosNombresTiposColecciones = [
    cNombreTipoTRAColeccionIdiomas,       
    cNombreTipoTRAColeccionModulos,       
    cNombreTipoTRAColeccionCadenas,       
    cNombreTipoTRAColeccionInformes,      
    cNombreTipoTRAColeccionImportaciones, 
    cNombreTipoTRAColeccionSolicitudesCadenas,
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
 ]


cTodosNombresTipos = cPreferredTypesOrder


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