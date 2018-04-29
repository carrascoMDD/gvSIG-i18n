# -*- coding: utf-8 -*-
#
# File: TRAElemento_Constants_Progress.py
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





from TRAElemento_Constants_TypeNames import *




# #############################################################
"""Ids and Titles of the progress control parameters singleton elements.

"""
cTRAParametrosControlProgreso_Verificar_Id               = "parametros-control-progreso-verificar"
cTRAParametrosControlProgreso_Verificar_Title            = "Verify Progress Control Parameters"
cTRAParametrosControlProgreso_Inicializar_Id             = "parametros-control-progreso-inicializar"
cTRAParametrosControlProgreso_Inicializar_Title          = "Initialize Progress Control Parameters"
cTRAParametrosControlProgreso_Inventario_Id              = "parametros-control-progreso-inventario"
cTRAParametrosControlProgreso_Inventario_Title           = "Inventory Progress Control Parameters"
cTRAParametrosControlProgreso_Recatalogar_Id             = "parametros-control-progreso-recatalogar"
cTRAParametrosControlProgreso_Recatalogar_Title          = "ReCatalog Progress Control Parameters"
cTRAParametrosControlProgreso_VerificarPermisos_Id       = "parametros-control-progreso-verificarpermisos"
cTRAParametrosControlProgreso_VerificarPermisos_Title    = "Verify Permissions Progress Control Parameters"
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


cTRAProgress_ReportBefore_Id   = 'before'
cTRAProgress_ReportAfter_Id    = 'after'


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
cTRAProgress_ProcessType_Verify           = 'Verificar'
cTRAProgress_ProcessType_Initialize       = 'Inicializar'
cTRAProgress_ProcessType_Inventory        = 'Inventario'
cTRAProgress_ProcessType_ReCatalog        = 'ReCatalogar'
cTRAProgress_ProcessType_VerifyPermissions= 'Verificar_Permisos'
cTRAProgress_ProcessType_ResetPermissions = 'ReEstablecer_Permisos'
cTRAProgress_ProcessType_DeleteModule     = 'Eliminar_Modulo'
cTRAProgress_ProcessType_DeleteLanguage   = 'Eliminar_Idioma'
cTRAProgress_ProcessType_Backup           = 'Copia_Seguridad'
cTRAProgress_ProcessType_ExportGvSIG      = 'Exportar_para_gvSIG'
cTRAProgress_ProcessType_Export           = 'Exportar'
cTRAProgress_ProcessType_Import           = 'Importar'

cTRAProgress_ProcessTypes_NonVoid = [
    cTRAProgress_ProcessType_Verify,
    cTRAProgress_ProcessType_Initialize,
    cTRAProgress_ProcessType_Inventory,
    cTRAProgress_ProcessType_ReCatalog,
    cTRAProgress_ProcessType_VerifyPermissions,  
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
    cTRAProgress_ProcessType_Verify:           cTRAParametrosControlProgreso_Verificar_Id,
    cTRAProgress_ProcessType_Initialize:       cTRAParametrosControlProgreso_Inicializar_Id,
    cTRAProgress_ProcessType_Inventory:        cTRAParametrosControlProgreso_Inventario_Id,
    cTRAProgress_ProcessType_ReCatalog:        cTRAParametrosControlProgreso_Recatalogar_Id,
    cTRAProgress_ProcessType_VerifyPermissions:cTRAParametrosControlProgreso_VerificarPermisos_Id,
    cTRAProgress_ProcessType_ResetPermissions: cTRAParametrosControlProgreso_ReestablecerPermisos_Id,
    cTRAProgress_ProcessType_DeleteModule:     cTRAParametrosControlProgreso_DeleteModule_Id,
    cTRAProgress_ProcessType_DeleteLanguage:   cTRAParametrosControlProgreso_DeleteLanguage_Id,   
    cTRAProgress_ProcessType_Backup:           cTRAParametrosControlProgreso_Backup_Id,
    cTRAProgress_ProcessType_ExportGvSIG:      cTRAParametrosControlProgreso_ExportGvSIG_Id,
    cTRAProgress_ProcessType_Export:           cTRAParametrosControlProgreso_Export_Id,
    cTRAProgress_ProcessType_Import:           cTRAParametrosControlProgreso_Import_Id,
}



cTRAProgress_ControlRequest_Ignored = 'Ignored'

cTRAProgress_Control_RunAfterPrevious     = 'RunAfterPrevious'
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
    cTRAProgress_ProcessType_Verify: [                                                                                                                                                       
        { 'types': cTodosNombresTipos,                               'support_kinds': [ cTRAProgress_SupportKind_Persistent, ],},
    ],
    cTRAProgress_ProcessType_Initialize: [                                                                                                                                                       
        { 'types': cTodosNombresTipos,                               'support_kinds': [ cTRAProgress_SupportKind_Persistent, ],},
    ],
    cTRAProgress_ProcessType_Inventory: [
        { 'types': cTodosNombresTiposWithPotentiallyManyChildren,    'support_kinds': [ cTRAProgress_SupportKind_Persistent, cTRAProgress_SupportKind_StoreResults, cTRAProgress_SupportKind_Logging, cTRAProgress_SupportKind_Transactional, cTRAProgress_SupportKind_YieldProcessor, ],},
        { 'types': cTodosNombresTiposWithoutPotentiallyManyChildren, 'support_kinds': [ cTRAProgress_SupportKind_Persistent, cTRAProgress_SupportKind_StoreResults, cTRAProgress_SupportKind_Logging,                                                                                  ],},        
    ],                                                                                                                                                                                                
    cTRAProgress_ProcessType_ReCatalog: [                                                                                                                                                             
        { 'types': cTodosNombresTiposWithPotentiallyManyChildren,    'support_kinds': [ cTRAProgress_SupportKind_Persistent, cTRAProgress_SupportKind_StoreResults, cTRAProgress_SupportKind_Logging, cTRAProgress_SupportKind_Transactional, cTRAProgress_SupportKind_YieldProcessor, ],},
        { 'types': cTodosNombresTiposWithoutPotentiallyManyChildren, 'support_kinds': [ cTRAProgress_SupportKind_Persistent, cTRAProgress_SupportKind_StoreResults, cTRAProgress_SupportKind_Logging,                                                                                  ],},        
    ],                                                                                                                                                                                                
    cTRAProgress_ProcessType_VerifyPermissions: [                                                                                                                                                       
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

