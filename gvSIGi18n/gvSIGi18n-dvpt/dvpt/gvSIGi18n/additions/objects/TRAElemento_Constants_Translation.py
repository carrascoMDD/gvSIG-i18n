# -*- coding: utf-8 -*-
#
# File: TRAElemento_Constants_Translation.py
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




# #################################################
"""Constants used by TRATraduccion (translation) elements.

"""




cEstadoTraduccionPendiente  = 'Pendiente'
cEstadoTraduccionTraducida  = 'Traducida'
cEstadoTraduccionRevisada   = 'Revisada'
cEstadoTraduccionDefinitiva = 'Definitiva'

cTodosEstados = [ cEstadoTraduccionPendiente, cEstadoTraduccionTraducida, cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva, ]



cMarcaDeFinDeRegistroDeHistoria   = "_*F*I*N*"
cMarcaDeComentarioSinCambios      = "=="







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




# ######################################
"""Constants for storage of translation changes into a field of TRATraduccion elements.

"""
cTRAHistory_ActionKind      = 'act'
cTRAHistory_ActionDate      = 'acd'
cTRAHistory_User            = 'use'
cTRAHistory_Status          = 'sta'
cTRAHistory_Translation     = 'tra'
cTRAHistory_TranslationDate = 'trd'
cTRAHistory_Translator      = 'tra'
cTRAHistory_RevisionDate    = 'red'
cTRAHistory_Reviewer        = 'rev'
cTRAHistory_DefinitiveDate  = 'ded'
cTRAHistory_Coordinator     = 'coo'
cTRAHistory_Comment         = 'cmt'



