# -*- coding: utf-8 -*-
#
# File: TRAElemento_Constants_Translate.py
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





# ##############################################################################
"""Default values for configurable properties for translation browsing and edition.

"""


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





# #######################################
"""Interaction modes for the translations page.

"""
cInteractionMode_Asynchronous       = 'Asincrono'
cInteractionMode_Synchronous        = 'Sincrono'




"""# #######################################
Default Interaction mode.
The user may change this value from the options section of the translations browser

"""
cInteractionMode_Default            = cInteractionMode_Asynchronous






# #######################################
"""Browse Translations service constants

"""
cTRABrowseTranslations_Desplazar_UnaPagina  = 'Pagina'
cTRABrowseTranslations_Desplazar_UnRegistro = 'Registro'


cTRABrowseTranslations_ModoDesplazamiento_SymbolIndex        = 'SymbolIndex'
cTRABrowseTranslations_ModoDesplazamiento_PageIndex          = 'PageIndex'
cTRABrowseTranslations_ModoDesplazamiento_SymbolStartingWith = 'SymbolStartingWith'

cTRABrowseTranslations_ModoDesplazamiento_First              = 'First'
cTRABrowseTranslations_ModoDesplazamiento_Previous           = 'Previous'
cTRABrowseTranslations_ModoDesplazamiento_Next               = 'Next'
cTRABrowseTranslations_ModoDesplazamiento_Last               = 'Last'




# #######################################
"""UI actions

"""
cAccion_Traducir                     = 'Traducir'
cAccion_InvalidarTraduccionesCadena  = 'InvalidarTraduccionesCadena'
cAccion_DesactivarCadena             = 'DesactivarCadena'
cAccion_ActivarCadena                = 'ActivarCadena'
cAccion_ChangeStringModules          = 'ChangeStringModules'






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
cRequestedChangeKind_ChangeStringModules= 'ChangeStringModules'

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





# #######################################
# Condition codes for change and browse translations
#

cResultCondition_Internal_MissingParameter                      = 'gvSIGi18n_ResultCondition_Internal_MissingParameter'
cResultCondition_Internal_Exception                             = 'gvSIGi18n_ResultCondition_Internal_Exception'

cResultCondition_MissingParameter                               = 'gvSIGi18n_ResultCondition_MissingParameter'
cResultCondition_MissingParameter_CodigoIdioma                  = 'gvSIGi18n_ResultCondition_MissingParameter_CodigoIdioma'
cResultCondition_MissingParameter_IdCadena                      = 'gvSIGi18n_ResultCondition_MissingParameter_IdCadena'

cResultCondition_ErrorInternal_Missing_TranslationServiceTool   = 'gvSIGi18n_ResultCondition_ErrorInternal_Missing_TranslationServiceTool'

cResultCondition_ErrorInternal_Missing_ModelDDvlPloneTool       = 'gvSIGi18n_ResultCondition_ErrorInternal_Missing_ModelDDvlPloneTool'
cResultCondition_ErrorInternal_Missing_TRAgvSIGi18nTool         = 'gvSIGi18n_ResultCondition_ErrorInternal_Missing_TRAgvSIGi18nTool'
cResultCondition_MissingParameter_Request                       = 'gvSIGi18n_ResultCondition_MissingParameter_Request'
cResultCondition_MissingParameter_Catalogo                      = 'gvSIGi18n_ResultCondition_MissingParameter_Catalogo'
cResultCondition_MissingParameter_ServiceRequest                = 'gvSIGi18n_ResultCondition_MissingParameter_ServiceRequest'

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










