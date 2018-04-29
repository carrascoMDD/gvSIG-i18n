# -*- coding: utf-8 -*-
#
# File: TRAElemento_Permission_Definitions_UseCaseNames.py
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





# ##########################################################################
"""Use Case Names

"""
 
cUseCase_CreateTRACatalogo              = 'Create_TRACatalogo' 
cUseCase_InitializeTRACatalogo          = 'Initialize_TRACatalogo'   
cUseCase_CacheStatus                    = 'CacheStatus_on_any_TRA_element'
cUseCase_View                           = 'View_any_TRA_element'
cUseCase_AdvancedView                   = 'Advanced_View_on_any_TRA_element'
cUseCase_Permissions                    = 'Permissions_on_any_TRA_element'
cUseCase_Changes                        = 'Changes_on_any_TRA_element'
cUseCase_ListLanguagesAndModules        = 'List_Languages_And_Modules'
cUseCase_VerifyTRACatalogo              = 'Verify_TRACatalogo'  
cUseCase_ConfigureTRACatalogo           = 'Configure_TRACatalogo'
cUseCase_ConfigureTRAConfiguracion      = 'Configure_TRAConfiguracion'   
cUseCase_ActivateTRAConfiguracionPermisos= 'Activate_TRAConfiguracion_Permisos'   
cUseCase_EditTRAParametrosControlProgreso= 'Edit_TRAParametrosControlProgreso'
cUseCase_ConfigureTRAProgreso           = 'Configure_TRAProgreso'   
cUseCase_ControlTRAProgreso             = 'Control_TRAProgreso'   
#cUseCase_EditTRAProgreso                = 'Edit_TRAProgreso'
cUseCase_ViewResultsTRAProgreso         = 'ViewResults_TRAProgreso'
cUseCase_InventoryTRAElemento           = 'Inventory_TRAElemento'  
cUseCase_VerifyPermissionsTRAElemento   = 'VerifyPermissions_TRAElemento'
cUseCase_ResetPermissionsTRAElemento    = 'ResetPermissions_TRAElemento'   
cUseCase_ReCatalogTRAElemento           = 'ReCatalog_TRAElemento'   
cUseCase_LockTRACatalogo                = 'Lock_TRACatalogo'   
cUseCase_UnlockTRACatalogo              = 'Unlock_TRACatalogo'   
cUseCase_CreateTRAImportacion           = 'Create_TRAImportacion'
cUseCase_CreateTRAImportacion_RestoreBackup = 'Create_TRAImportacion_RestoreBackup'
cUseCase_DeleteTRAImportacion           = 'Delete_TRAImportacion'
cUseCase_CreateTRAContenidoIntercambio  = 'Create_TRAContenidoIntercambio'
cUseCase_CreateTRAContenidoXML          = 'Create_TRAContenidoXML'
cUseCase_DeleteTRAContenidoIntercambio  = 'Delete_TRAContenidoIntercambio'
cUseCase_EditTRAContenidoIntercambio    = 'Edit_TRAContenidoIntercambio'
cUseCase_CreateMissingTRATraduccion     = 'Create_missing_TRATraduccion'   
cUseCase_EstimateTRAImportacion         = 'Estimate_TRAImportacion'
cUseCase_ImportTRAImportacion           = 'Import_TRAImportacion'
cUseCase_ImportTRAImportacion_ToCreateCadenas = 'Import_TRAImportacion_ToCreateCadenas'
cUseCase_Restore_TRACatalogo            = 'Restore_TRACatalogo'
cUseCase_Export                         = 'Export'
cUseCase_ExportGvSIG_TRAIdioma          = 'ExportGvSIG_TRAIdioma'
cUseCase_ExportGvSIG_All_TRAIdioma      = 'ExportGvSIG_All_TRAIdioma'
cUseCase_Backup_TRACatalogo             = 'Backup_TRACatalogo'
cUseCase_EllaborateInformeActividad     = 'EllaborateInformeActividad'
cUseCase_EllaborateInformeLanguages     = 'EllaborateInformeLanguages'
cUseCase_EllaborateInformeModulesAndLanguages = 'EllaborateInformeModulesAndLanguages'
cUseCase_DeleteTRAInforme               = 'Delete_TRAInforme'
cUseCase_CreateTRASolicitudCadena       = 'Create_TRASolicitudCadena'
cUseCase_EditTRASolicitudCadena         = 'Edit_TRASolicitudCadena'
cUseCase_CreateTRAIdioma                = 'Create_TRAIdioma'
cUseCase_DeleteTRAIdioma                = 'Delete_TRAIdioma'
cUseCase_EditTRAIdioma                  = 'Edit_TRAIdioma'
cUseCase_LockTRAIdioma                  = 'Lock_TRAIdioma'
cUseCase_UnlockTRAIdioma                = 'Unlock_TRAIdioma'
cUseCase_CreateTRAModulo                = 'Create_TRAModulo'
cUseCase_DeleteTRAModulo                = 'Delete_TRAModulo'
cUseCase_RenameTRAModulo                = 'Rename_TRAModulo'
cUseCase_EditTRAModulo                  = 'Edit_TRAModulo'
cUseCase_CreateTRACadena                = 'Create_TRACadena'
cUseCase_CleanupTRAColeccionSolicitudesCadenas = 'Cleanup_TRAColeccionSolicitudesCadenas'
cUseCase_Copy_Translations              = 'Copy_Translations'
cUseCase_DeactivateTRACadena            = 'Deactivate_TRACadena'
cUseCase_ActivateTRACadena              = 'Activate_TRACadena'
cUseCase_EditTRAImportacion             = 'Edit_TRAImportacion'
cUseCase_ReuseTRAImportacion            = 'Reuse_TRAImportacion'
cUseCase_CreateTRAInforme               = 'Create_TRAInforme'
cUseCase_EditTRAInforme                 = 'Edit_TRAInforme'
cUseCase_AddModulesToTRACadena          = 'Add_Modules_To_TRACadena'
cUseCase_RemoveModulesFromTRACadena     = 'Remove_Modules_From_TRACadena'
cUseCase_BrowseTranslations             = 'Browse_Translations'
cUseCase_TRATraduccionStateChange       = 'Change_TRATraduccion_State'
cUseCase_TRATraduccionComment           = 'Comment_on_TRATraduccion'
cUseCase_InvalidateStringTranslations   = 'Invalidate_String_Translations'
cUseCase_ConfigureExecutionProfilingEnablement_Global = 'Configure_ExecutionProfilingEnablement_Global'
cUseCase_ConfigureExecutionProfilingEnablement_TRACatalogo = 'Configure_ExecutionProfilingEnablement_TRACatalogo'
cUseCase_CreateTRAContribuciones        = 'Create_TRAContribuciones'
cUseCase_EditTRAContribuciones          = 'Edit_TRAContribuciones'


                                                                
cTRAUseCaseNames = [
    cUseCase_CreateTRACatalogo,
    cUseCase_InitializeTRACatalogo,  
    cUseCase_VerifyTRACatalogo,
    cUseCase_ConfigureTRACatalogo,
    cUseCase_ConfigureTRAConfiguracion,
    cUseCase_ActivateTRAConfiguracionPermisos,
    cUseCase_InventoryTRAElemento,
    cUseCase_VerifyPermissionsTRAElemento,
    cUseCase_ResetPermissionsTRAElemento,
    cUseCase_ReCatalogTRAElemento,
    cUseCase_LockTRACatalogo,
    cUseCase_UnlockTRACatalogo,
    cUseCase_CreateMissingTRATraduccion,
    cUseCase_CreateTRAImportacion,   
    cUseCase_CreateTRAImportacion_RestoreBackup,
    cUseCase_DeleteTRAImportacion,
    cUseCase_CreateTRAContenidoIntercambio,
    cUseCase_CreateTRAContenidoXML,
    cUseCase_DeleteTRAContenidoIntercambio,
    cUseCase_EditTRAContenidoIntercambio,
    cUseCase_EstimateTRAImportacion,
    cUseCase_ImportTRAImportacion,   
    cUseCase_ImportTRAImportacion_ToCreateCadenas,
    cUseCase_Restore_TRACatalogo,
    cUseCase_Export, 
    cUseCase_ExportGvSIG_TRAIdioma,
    cUseCase_ExportGvSIG_All_TRAIdioma,
    cUseCase_Backup_TRACatalogo,
    cUseCase_EllaborateInformeActividad,
    cUseCase_EllaborateInformeLanguages,   
    cUseCase_EllaborateInformeModulesAndLanguages,  
    cUseCase_View,
    cUseCase_AdvancedView,
    cUseCase_Permissions,
    cUseCase_Changes,
    cUseCase_CacheStatus,
    cUseCase_ListLanguagesAndModules,
    cUseCase_BrowseTranslations,
    cUseCase_TRATraduccionStateChange,      
    cUseCase_TRATraduccionComment,
    cUseCase_CreateTRASolicitudCadena,
    cUseCase_EditTRASolicitudCadena,
    cUseCase_InvalidateStringTranslations,
    cUseCase_CreateTRAIdioma,
    cUseCase_DeleteTRAIdioma,
    cUseCase_CreateTRAModulo,
    cUseCase_DeleteTRAModulo,
    cUseCase_CreateTRACadena,
    cUseCase_CleanupTRAColeccionSolicitudesCadenas,
    cUseCase_Copy_Translations,
    cUseCase_DeactivateTRACadena,
    cUseCase_ActivateTRACadena,
    cUseCase_EditTRAIdioma,
    cUseCase_LockTRAIdioma,
    cUseCase_UnlockTRAIdioma,
    cUseCase_EditTRAModulo,
    cUseCase_EditTRAImportacion,
    cUseCase_ReuseTRAImportacion,
    cUseCase_CreateTRAInforme,
    cUseCase_EditTRAInforme,
    cUseCase_AddModulesToTRACadena,
    cUseCase_RemoveModulesFromTRACadena,
    #cUseCase_ConfigureExecutionProfilingEnablement_Global,
    #cUseCase_ConfigureExecutionProfilingEnablement_TRACatalogo,
    cUseCase_EditTRAParametrosControlProgreso,
    cUseCase_ControlTRAProgreso,
    cUseCase_ConfigureTRAProgreso,
    #cUseCase_EditTRAProgreso,
    cUseCase_ViewResultsTRAProgreso,
    cUseCase_CreateTRAContribuciones,
]






