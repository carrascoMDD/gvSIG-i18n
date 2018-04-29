# -*- coding: utf-8 -*-
#
# File: TRAElemento_Permission_Definitions.py
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

from StringIO import StringIO

from Products.CMFCore       import permissions

from Products.PluggableAuthService.permissions import ManageGroups                  as perm_ManageGroups
from AccessControl.Permissions                 import access_contents_information   as perm_AccessContentsInformation
from AccessControl.Permissions                 import copy_or_move                  as perm_CopyOrMove


from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache import cRoleKind_UserSpecific


from TRARoles               import *
from TRAElemento_Constants  import *






# ##########################################################################
"""Classification of roles into a subset of role kinds, for the cache to figure out whther to serve a cached page generic for the role kind, or specific to the user.

"""


cTRAApplicationRolesAndRoleKinds = [
    [ [ cTRAManager_role, ],    cRoleKind_UserSpecific],
    [ [ cTRACoordinator_role,], cRoleKind_UserSpecific],
    [ [ cTRADeveloper_role,],   cRoleKind_UserSpecific],
    [ [ cTRAReviewer_role, ],   cRoleKind_UserSpecific],
    [ [ cTRATranslator_role, ], cRoleKind_UserSpecific],
    [ [ cTRAVisitor_role,],     cRoleKind_UserSpecific],
]




# #######################################################
"""Configuration of views that require private caches for qualified users.
   For example all users may not have access to all languages.

"""
cTRAPrivateCacheViewsForQualifiedUsers = [ 'TRACatalogo', 'TRACatalogo_NoHeaderNoFooter', 'TRACatalogoInforme', 'TRACatalogoInforme_NoHeaderNoFooter', 'TRACatalogoDetalle', 'TRACatalogoDetalle_NoHeaderNoFooter',]








# ##########################################################################
"""Failure assessments

"""
 
cRuleAssessment_Passed                              = "RulePassed"
cRuleAssessment_Failed                              = "RuleFailed"
cRuleAssessment_ObjectNotPassed                     = "ObjectFailed"
cRuleAssessment_Filter_Discard                      = "Rule_Filter_Discard"
cRuleAssessment_EmptyOrAny_Discard                  = "Rule_EmptyOrAny_Discard"
cRuleAssessment_Failure_NotOfTargetType             = "RuleFailure_NotOfTargetType"                        
cRuleAssessment_Failure_UserWithoutRole             = "RuleFailure_UserWithoutRole"
cRuleAssessment_Failure_UserWithoutPermissions      = "RuleFailure_UserWithoutPermissions"
cRuleAssessment_Failure_Mode_EmptyOrAny             = "RuleFailure_Mode_EmptyOrAny"
cRuleAssessment_Failure_Mode_EmptyOrAll             = "RuleFailure_Mode_EmptyOrAll"
cRuleAssessment_Failure_ObjectAlreadyRejected       = "RuleFailure_Mode_ObjectAlreadyRejected" 
cRuleAssessment_Failure_ObjectRejectedInPreviousRule= "RuleFailure_ObjectRejectedInPreviousRule"
cRuleAssessment_Failure_Predicate                   = "RuleFailure_Predicate"


cRuleAssessmentMessages = {
    cRuleAssessment_Passed                              : "Passed",
    cRuleAssessment_Failed                              : "Failed",
    cRuleAssessment_ObjectNotPassed                     : "Object nor passed rule",
    cRuleAssessment_Filter_Discard                      : "Object Discarded in Filter",
    cRuleAssessment_EmptyOrAny_Discard                  : "Optional Object Discarded",
    cRuleAssessment_Failure_NotOfTargetType             : "Discarded Object of wrong Type",                      
    cRuleAssessment_Failure_UserWithoutRole             : "User without any authorized Role",
    cRuleAssessment_Failure_UserWithoutPermissions      : "User without all the required Permissions",
    cRuleAssessment_Failure_Mode_EmptyOrAny             : "No object consired matched the rule",
    cRuleAssessment_Failure_Mode_EmptyOrAll             : "Not all objects consired matched the rule",
    cRuleAssessment_Failure_ObjectAlreadyRejected       : "Object has been rejected",
    cRuleAssessment_Failure_ObjectRejectedInPreviousRule: "Object was rejected by a previous Rule",
}







# ##########################################################################
""" special identifiers and modes.

"""


cBoundObject  = 'object' 
cPermissionRuleNameDefault    = 'default' 

cUseCaseRuleMode_ForAll     = 'ForAll' 
cUseCaseRuleMode_Filter     = 'Filter' 
cUseCaseRuleMode_EmptyOrAll = 'EmptyOrAll' 
cUseCaseRuleMode_EmptyOrAny = 'EmptyOrAny' 


cUseCaseRuleModes = [
    cUseCaseRuleMode_ForAll,
    cUseCaseRuleMode_Filter,                
    cUseCaseRuleMode_EmptyOrAll,
    cUseCaseRuleMode_EmptyOrAny,
]




# ##########################################################################
"""Roles used  (names defined and TRARoles.py)

"""

cUbiquitousWriterRoles = [ 'Manager', 'Owner', cTRAManager_role,]
cUbiquitousReaderRoles = cUbiquitousWriterRoles + [ 'Anonymous', 'Member',]

cManagerRoles          = [ 'Manager', 'Owner', cTRAManager_role,]

cPreferredRolesOrder   = [ 'Manager', 'Owner',] + TRARoles_list









# ##########################################################################
"""Groups to create for management of the catalog and Roles 

"""


cTRAManagers_group       = "TRAManagers"
cTRACoordinators_group   = "TRACoordinators"
cTRADevelopers_group     = "TRADevelopers"
cTRAReviewers_group      = "TRAReviewers"
cTRATranslators_group    = "TRATranslators"
cTRAVisitors_group       = "TRAVisitors"


cTRAPreferredUserGroupsOrder = [
    cTRAManagers_group,     
    cTRACoordinators_group, 
    cTRADevelopers_group,
    cTRAReviewers_group,    
    cTRATranslators_group,  
    cTRAVisitors_group,     
]

cTRATodosUserGroups = cTRAPreferredUserGroupsOrder




cTRAUsersGroup_AllLanguages_postfix       = "la_All"


# ##########################################################################
"""Assignment of Roles to user groups

"""

cTRAUserGroups_Catalogo = [
    [ cTRAManagers_group,       [ cTRAManager_role,       ], ],
    [ cTRACoordinators_group,   [ cTRACoordinator_role,   ], ],
    [ cTRADevelopers_group,     [ cTRADeveloper_role,     ], ],
    [ cTRAReviewers_group,      [ cTRAReviewer_role,      ], ],
    [ cTRATranslators_group,    [ cTRATranslator_role,    ], ],
    [ cTRAVisitors_group,       [ cTRAVisitor_role,       ], ],
]

cTRAUserGroups_Catalogo_AuthorizedOnCatalogo = [ unGrAndRs[ 0] for unGrAndRs in cTRAUserGroups_Catalogo] 

cTRAUserGroups_Catalogo_AuthorizedOnIndividualIdiomas = [
    cTRAManagers_group,
    cTRACoordinators_group,
    cTRADevelopers_group,
]

cTRAUserGroups_Catalogo_AuthorizedOnIndividualModulos = [
    cTRAManagers_group,
    cTRACoordinators_group,
    cTRADevelopers_group,
]




cTRAUserGroups_Idioma = [
    [ cTRACoordinators_group,   [ cTRACoordinator_role,   ], ],
    [ cTRAReviewers_group,      [ cTRAReviewer_role,      ], ],
    [ cTRATranslators_group,    [ cTRATranslator_role,    ], ],
    [ cTRAVisitors_group,       [ cTRAVisitor_role,       ], ],
]

cTRAUserGroups_Idioma_AuthorizedOnCatalogo = [] 
cTRAUserGroups_Idioma_AuthorizedOnIdioma   = [ unGrAndRs[ 0] for unGrAndRs in cTRAUserGroups_Idioma] 



cTRAUserGroups_Modulo = cTRAUserGroups_Idioma[:]

cTRAUserGroups_Modulo_AuthorizedOnCatalogo = [] 
cTRAUserGroups_Modulo_AuthorizedOnModulo   = [ unGrAndRs[ 0] for unGrAndRs in cTRAUserGroups_Modulo] 






# ##########################################################################
"""Types that shall acquire Role assignments to users and groups
A manager or coordinator may set TRAIdioma to not acquire
such that the roles for the language 
must be set on the language for each authorized individual user.


"""
# ACV 20090914 Simpler security schema: no user groups for languages or modules, shall assign local roles to users directly on the language or module element
cTypesAcquiringRoleAssignments =  [
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









# ##########################################################################
""" Rules to control which Status changes are allowed for users in roles

"""


cStateChangeActionRoles = {
    cEstadoTraduccionPendiente: {
        cEstadoTraduccionPendiente:  None,
        cEstadoTraduccionTraducida:  [ cTRATranslator_role, cTRAReviewer_role,  cTRACoordinator_role,] +  cUbiquitousWriterRoles,
        cEstadoTraduccionRevisada:   None,
        cEstadoTraduccionDefinitiva: None,
    },
    cEstadoTraduccionTraducida: {
        cEstadoTraduccionPendiente:  [ cTRATranslator_role, cTRAReviewer_role,  cTRACoordinator_role,] +  cUbiquitousWriterRoles,
        cEstadoTraduccionTraducida:  [ cTRATranslator_role, cTRAReviewer_role,  cTRACoordinator_role,] +  cUbiquitousWriterRoles,
        cEstadoTraduccionRevisada:   [ cTRAReviewer_role,  cTRACoordinator_role,   ] +  cUbiquitousWriterRoles,
        cEstadoTraduccionDefinitiva: None,
    },
    cEstadoTraduccionRevisada: {
        cEstadoTraduccionPendiente:  [ cTRAReviewer_role,  cTRACoordinator_role, ] +  cUbiquitousWriterRoles,
        cEstadoTraduccionTraducida:  [ cTRAReviewer_role,  cTRACoordinator_role, ] +  cUbiquitousWriterRoles,
        cEstadoTraduccionRevisada:   None,
        cEstadoTraduccionDefinitiva: [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles,
    },
    cEstadoTraduccionDefinitiva: {
        cEstadoTraduccionPendiente:  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles,
        cEstadoTraduccionTraducida:  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles,
        cEstadoTraduccionRevisada:   [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles,
        cEstadoTraduccionDefinitiva: None,
    },
}    
     


cInvalidateStringTranslationsRoles = [ cTRACoordinator_role, cTRADeveloper_role, ] +  cUbiquitousWriterRoles


cDeactivateStringsRoles            = [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles
cActivateStringsRoles              = cDeactivateStringsRoles



# ##########################################################################
"""Use Cases

"""
 
cUseCase_ConfigureTRAProgreso           = 'Configure_TRAProgreso'   
cUseCase_ControlTRAProgreso             = 'Control_TRAProgreso'   
cUseCase_VerifyTRACatalogo              = 'Verify_TRACatalogo'  
cUseCase_InventoryTRAElemento           = 'Inventory_TRAElemento'   
cUseCase_InitializeTRACatalogo          = 'Initialize_TRACatalogo'   
cUseCase_ResetPermissionsTRAElemento    = 'ResetPermissions_TRAElemento'   
cUseCase_ReCatalogTRAElemento           = 'ReCatalog_TRAElemento'   
cUseCase_LockTRACatalogo                = 'Lock_TRACatalogo'   
cUseCase_UnlockTRACatalogo              = 'Unlock_TRACatalogo'   
cUseCase_CreateMissingTRATraduccion     = 'Create_missing_TRATraduccion'   
cUseCase_ConfigureTRACatalogo           = 'Configure_TRACatalogo'   
cUseCase_CreateTRAImportacion           = 'Create_TRAImportacion'
cUseCase_DeleteTRAImportacion           = 'Delete_TRAImportacion'
cUseCase_CreateTRAContenidoIntercambio  = 'Create_TRAContenidoIntercambio'
cUseCase_DeleteTRAContenidoIntercambio  = 'Delete_TRAContenidoIntercambio'
cUseCase_ImportTRAImportacion           = 'Import_TRAImportacion'
cUseCase_ImportTRAImportacion_ToCreateCadenas = 'Import_TRAImportacionn_ToCreateCadenas'
cUseCase_Export                         = 'Export'
cUseCase_ExportGvSIG_TRAIdioma          = 'ExportGvSIG_TRAIdioma'
cUseCase_Backup_TRACatalogo             = 'Backup_TRACatalogo'
cUseCase_EllaborateInformeActividad     = 'EllaborateInformeActividad'
cUseCase_EllaborateInformeLanguages     = 'EllaborateInformeLanguages'
cUseCase_EllaborateInformeModulesAndLanguages      = 'EllaborateInformeModulesAndLanguages'
cUseCase_CreateAndDeleteTRAInformeInTRAImportacion = 'Generate_TRAInforme_before_and_after_import'
cUseCase_DeleteTRAInforme               = 'Delete_TRAInforme'
cUseCase_View                           = 'View_any_TRA_element'
cUseCase_AdvancedView                   = 'Advanced_View_on_any_TRA_element'
cUseCase_Permissions                    = 'Permissions_on_any_TRA_element'
cUseCase_ListLanguagesAndModules        = 'List_Languages_And_Modules'
cUseCase_BrowseTranslations             = 'Browse_Translations'
cUseCase_TRATraduccionStateChange       = 'Change_TRATraduccion_State'
cUseCase_TRATraduccionComment           = 'Comment_on_TRATraduccion'
cUseCase_CreateTRASolicitudCadena       = 'Create_TRASolicitudCadena'
cUseCase_InvalidateStringTranslations   = 'Invalidate_String_Translations'
cUseCase_CreateTRAIdioma                = 'Create_TRAIdioma'
cUseCase_DeleteTRAIdioma                = 'Delete_TRAIdioma'
cUseCase_CreateTRAModulo                = 'Create_TRAModulo'
cUseCase_DeleteTRAModulo                = 'Delete_TRAModulo'
cUseCase_CreateTRACadena                = 'Create_TRACadena'
cUseCase_CleanupTRAColeccionSolicitudesCadenas = 'Cleanup_TRAColeccionSolicitudesCadenas'
cUseCase_Copy_Translations              = 'Copy_Translations'
cUseCase_DeactivateTRACadena            = 'Deactivate_TRACadena'
cUseCase_ActivateTRACadena              = 'Activate_TRACadena'
cUseCase_LockTRAIdioma                  = 'Lock_TRAIdioma'
cUseCase_UnlockTRAIdioma                = 'Unlock_TRAIdioma'
cUseCase_ReuseTRAImportacion            = 'Reuse_TRAImportacion'
cUseCase_CreateTRAInforme               = 'Create_TRAInforme'
cUseCase_AddModulesToTRACadena          = 'Add_Modules_To_TRACadena'
cUseCase_RemoveModulesFromTRACadena     = 'Remove_Modules_From_TRACadena'
cUseCase_ConfigureExecutionProfilingEnablement_Global = 'Configure_ExecutionProfilingEnablement_Global'
cUseCase_ConfigureExecutionProfilingEnablement_TRACatalogo = 'Configure_ExecutionProfilingEnablement_TRACatalogo'

                                                                
cTRAUseCaseNames = [
    cUseCase_ControlTRAProgreso,
    cUseCase_ConfigureTRAProgreso,
    cUseCase_VerifyTRACatalogo,
    cUseCase_InventoryTRAElemento,
    cUseCase_InitializeTRACatalogo,  
    cUseCase_ResetPermissionsTRAElemento,
    cUseCase_ReCatalogTRAElemento,
    cUseCase_LockTRACatalogo,
    cUseCase_UnlockTRACatalogo,
    cUseCase_CreateMissingTRATraduccion,
    cUseCase_ConfigureTRACatalogo,
    cUseCase_CreateTRAImportacion,   
    cUseCase_DeleteTRAImportacion,
    cUseCase_CreateTRAContenidoIntercambio,
    cUseCase_DeleteTRAContenidoIntercambio,
    cUseCase_ImportTRAImportacion,   
    cUseCase_ImportTRAImportacion_ToCreateCadenas,
    cUseCase_Export, 
    cUseCase_ExportGvSIG_TRAIdioma,
    cUseCase_Backup_TRACatalogo,
    cUseCase_EllaborateInformeActividad,
    cUseCase_EllaborateInformeLanguages,   
    cUseCase_EllaborateInformeModulesAndLanguages,  
    cUseCase_CreateAndDeleteTRAInformeInTRAImportacion,
    cUseCase_View,
    cUseCase_AdvancedView,
    cUseCase_Permissions,
    cUseCase_ListLanguagesAndModules,
    cUseCase_BrowseTranslations,
    cUseCase_TRATraduccionStateChange,      
    cUseCase_TRATraduccionComment,
    cUseCase_CreateTRASolicitudCadena,
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
    cUseCase_LockTRAIdioma,
    cUseCase_UnlockTRAIdioma,
    cUseCase_ReuseTRAImportacion,
    cUseCase_CreateTRAInforme,
    cUseCase_AddModulesToTRACadena,
    cUseCase_RemoveModulesFromTRACadena,
    cUseCase_ConfigureExecutionProfilingEnablement_Global,
    cUseCase_ConfigureExecutionProfilingEnablement_TRACatalogo,
]










# ##########################################################################
"""Types that shall acquire permissions : None
Permissions are obtained in each element by being explicitely granted to roles

"""
cTypesAcquiringPermissions = []






# ##########################################################################
"""Permissions that are not to be granted to any role in any object

"""
cPermissionsToDenyEverywhereToEverybody = [ perm_CopyOrMove,]




# ##########################################################################
"""Special application permission used to control who can create and properly initialize a TRACatalogo

"""


cPermission_gvSIGi18nAddTRACatalogo = 'gvSIGi18n: Add TRACatalogo'


# ##########################################################################
"""Permissions used, and abbreviations

"""


cPermissionsAndAbbreviations = [
    [   'ADC', cPermission_gvSIGi18nAddTRACatalogo,],
    [   'VIE', permissions.View,],              
    [   'ACI', perm_AccessContentsInformation,],
    [   'LFC', permissions.ListFolderContents,],
    [   'APC', permissions.AddPortalContent,],  
    [   'APF', permissions.AddPortalFolders,],  
    [   'DOB', permissions.DeleteObjects,],     
    [   'MPC', permissions.ModifyPortalContent,],
    [   'MPR', permissions.ManageProperties,], 
    [   'MGR', perm_ManageGroups, ],
    [   'PER', permissions.ChangePermissions,],
]

cPreferredPermissionAbbreviations = [ unAbbrYPerm[ 0] for unAbbrYPerm in cPermissionsAndAbbreviations]
cPreferredPermissions             = [ unAbbrYPerm[ 1] for unAbbrYPerm in cPermissionsAndAbbreviations]



cPermissionsToReset = [ unAbbrYPerm[ 1] for unAbbrYPerm in cPermissionsAndAbbreviations[1:]]



cPermissionsByAbbreviation = dict( cPermissionsAndAbbreviations)


cPermissionsAbbreviatedFor_ViewElement             = [   'VIE', 'ACI', ]

cPermissionsAbbreviatedFor_ViewElementAndChildren  = [   'VIE', 'ACI', 'LFC', ]

















# ##########################################################################
"""Use Case Driven security specificaction with Use cases, roles, types and required Plone permissions

"""

cTRAUseCasesWithAbbreviatedPermissions =  {
  'void_useCase_toImpose_View_And_ListFolderContents' : [ 
        [   {   'title':  'Objects without children can be viewed',
                'root':   cTodosNombresTiposWithoutChildren, 
                'path':   [ 'object',], 
                'types':  cTodosNombresTiposWithoutChildren,     
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement,                 
            },
            {   'title':  'Objects with children allow to view their children',
                'root':   cTodosNombresTiposWithChildren, 
                'path':   [ 'object',], 
                'types':  cTodosNombresTiposWithChildren,     
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
        ],
        [
             # extras go here like: [ [ 
                #cNombreTipoTRAColeccionCadenas]         ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF',  'MPC',  ],              [ cTRACoordinator_role,] +  cUbiquitousWriterRoles,],         
        ],                                                                                           
    ],                                                                                                    
  'void_useCase_toImpose_ListFolderContents_On_WithChildrenOrRelationsOrPloneElements' : [ 
        [   {   'title':  'Objects that may have children or relations or plone elements allow to view their children or related elements',
                'root':   cTodosNombresTiposWithChildrenOrRelationsOrPloneElements, 
                'path':   [ 'object',], 
                'types':  cTodosNombresTiposWithChildrenOrRelationsOrPloneElements,     
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
        ],
        [
        ],                                                                                           
    ],                                                                                                    
    'void_useCase_toImpose_All_Permissions_to_Managers' : [ 
        [   {   'path':   [ 'object', ],  
                'types':  cTodosNombresTiposWithChildren,    
                'roles':  [ cTRAManager_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'DOB', 'MPC', 'MPR', ], 
            },
            {   'path':   [ 'object', ],  
                'types':  cTodosNombresTiposWithoutChildren,    
                'roles':  [ cTRAManager_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'DOB', 'MPC', 'MPR', ], 
            },
            {   'path':   [ 'object', ],  
                'types':  cTodosNombresTiposWithChildren,    
                'roles':  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'path':   [ 'object', ],  
                'types':  cTodosNombresTiposWithoutChildren,    
                'roles':  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement, # ListFolderContents is not required for TRATraducion that will never have contents,but we force it set just in case Plone would throw out to login screen even managers, if hitting the tab contents, or even trying
            },
        ],  
        [
             # extras go here like: [ [ 
                #cNombreTipoTRAColeccionCadenas]         ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF',  'MPC',  ],              [ cTRACoordinator_role,] +  cUbiquitousWriterRoles,],         
        ],                                                                                           
    ],                                                                                                    
    #'void_useCase_toImpose_ManageGroups_Permission' : [ 
        #[   {   'path':   [ 'object', ],  
                #'types':  cTodosNombresTipos,    
                #'roles':  [ cTRAManager_role, ] +  cUbiquitousWriterRoles, 
                #'perms':  [ 'MGR', ], 
            #},
        #],  
        #[
            ## extras go here like: [ [ 
                ##cNombreTipoTRAColeccionCadenas]         ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF',  'MPC',  ],              [ cTRACoordinator_role,] +  cUbiquitousWriterRoles,],         
        #],                                                                                           
    #],                                                                                                  
    'void_useCase_toImpose_ManageProperties_Permission' : [ 
        [   {   'path':   [ 'object', ],  
                'types':  cTodosNombresTipos,    
                'roles':  [ cTRAManager_role, cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  [ 'MPR', ], 
            },
        ],  
        [
            # extras go here like: [ [ 
                #cNombreTipoTRAColeccionCadenas]         ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF',  'MPC',  ],              [ cTRACoordinator_role,] +  cUbiquitousWriterRoles,],         
        ],                                                                                           
    ],                                                                                                  
    cUseCase_VerifyTRACatalogo : [ 
        [   {   'title':  'Es TRACatalogo',
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role,cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
        ],  
        [
            [ cTodosNombresTiposWithChildren      ,cPermissionsAbbreviatedFor_ViewElementAndChildren ,   [ cTRAManager_role,cTRACoordinator_role,] + cUbiquitousWriterRoles,],         
            [ cTodosNombresTiposWithoutChildren   ,cPermissionsAbbreviatedFor_ViewElement ,              [ cTRAManager_role,cTRACoordinator_role,] + cUbiquitousWriterRoles,],         
        ],                                                                                           
    ],   
    cUseCase_ConfigureExecutionProfilingEnablement_Global: [ 
        [   {   'title':  'Manager on TRACatalogo ',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [  cNombreTipoTRACatalogo,],    
                'roles':  [ 'Manager',], 
                'perms':  [ 'VIE', ], 
            },
        ],  
        [
        ],                                                                                           
    ],  
    cUseCase_ConfigureExecutionProfilingEnablement_TRACatalogo: [ 
        [   {   'title':  'TRAManager on Accesible, Modifiable TRACatalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [  cNombreTipoTRACatalogo,],    
                'roles':  [ 'Manager', cTRAManager_role,] +  cUbiquitousWriterRoles, 
                'perms':  [ 'VIE', 'MPC',], 
            },
        ],  
        [
        ],                                                                                           
    ],  
    cUseCase_InitializeTRACatalogo : [ 
        [   {   'title':  'Es TRACatalogo',
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'PER', 'APC', 'APF', 'DOB', 'MPC','ADC',], 
            },
            {   'title':  'Modifiable TRACatalogo',
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRAManager_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Add TRACatalogo',
                'path':   [ 'object', 'getContenedor', ],  
                'types':  [ ],    
                'roles':  [ cTRAManager_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'ADC',], 
            },
        ],  
        [
            [ cTodosNombresTiposColecciones ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'DOB', 'MPC', ],      [ cTRAManager_role,] +  cUbiquitousWriterRoles,],         
            [ [ cNombreTipoTRAParametrosControlProgreso,] ,cPermissionsAbbreviatedFor_ViewElement + [ 'APC', 'APF', 'DOB', 'MPC', ],   [ cTRAManager_role,] +  cUbiquitousWriterRoles,],         
        ],                                                                                           
    ],  
    cUseCase_ControlTRAProgreso:  [
        [   {   'title':  'Es TRAProgreso',
                'path':   [ 'object', ], 
                'types':  [  cNombreTipoTRAProgreso,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + ['MPC',], 
            },
            {   'title':  'Accesible TRACatalogo',
                'path':   [ 'object', 'getCatalogo'],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren , 
            },
        ],  
        [
        ],                                                                                           
    ],
    cUseCase_ConfigureTRAProgreso: [
        [   {   'title':  'Es TRAProgreso',
                'path':   [ 'object', ], 
                'types':  [  cNombreTipoTRAProgreso,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + ['MPC',], 
            },
            {   'title':  'Accesible TRACatalogo',
                'path':   [ 'object', 'getCatalogo'],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren , 
            },
        ],  
        [
        ],                                                                                           
    ],
    cUseCase_InventoryTRAElemento : [
        [   {   'title':  'Es elemento de traducciones',
                'path':   [ 'object', ], 
                'types':  cTodosNombresTipos,    
                'roles':  [ cTRAManager_role, cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
            {   'title':  'Accesible TRACatalogo',
                'path':   [ 'object', 'getCatalogo'],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren , 
            },
            {   'title':  'Accesible collection of TRAProgreso',
                'path':   [ 'object', 'getCatalogo', 'fObtenerColeccionProgresos',],  
                'types':  [ cNombreTipoTRAColeccionProgresos,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [  'MPC', 'APC',], 
            },
        ],  
        [
            [ cTodosNombresTiposWithChildren      ,cPermissionsAbbreviatedFor_ViewElementAndChildren ,   [ cTRAManager_role, cTRACoordinator_role,] + cUbiquitousWriterRoles,],         
            [ cTodosNombresTiposWithoutChildren   ,cPermissionsAbbreviatedFor_ViewElement ,              [ cTRAManager_role, cTRACoordinator_role,] + cUbiquitousWriterRoles,],         
            [ [ cNombreTipoTRAProgreso,]          ,cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', ],  [ cTRAManager_role, cTRACoordinator_role,] + cUbiquitousWriterRoles,], 
        ],                                                                                           
    ],
    cUseCase_ResetPermissionsTRAElemento : [
        [   {   'title':  'Es elemento de traducciones',
                'path':   [ 'object', ], 
                'types':  cTodosNombresTipos,    
                'roles':  [ cTRAManager_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', 'PER',], 
            },
            {   'title':  'Modifiable TRACatalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRAManager_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'MPC', 'PER',], 
            },
            {   'title':  'Accesible collection of TRAProgreso',
                'path':   [ 'object', 'getCatalogo', 'fObtenerColeccionProgresos',],  
                'types':  [ cNombreTipoTRAColeccionProgresos,],    
                'roles':  [ cTRAManager_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [  'MPC', 'APC',], 
            },
        ],  
        [
            [ cTodosNombresTiposWithChildren      ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'MPC', 'PER',],   [ cTRAManager_role,] + cUbiquitousWriterRoles,],         
            [ cTodosNombresTiposWithoutChildren   ,cPermissionsAbbreviatedFor_ViewElement            + [ 'MPC', 'PER',],   [ cTRAManager_role,] + cUbiquitousWriterRoles,],         
            [ [ cNombreTipoTRAProgreso,]          ,cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', ],                    [ cTRAManager_role,] + cUbiquitousWriterRoles,], 
        ],                                                                                           
    ],
    cUseCase_ReCatalogTRAElemento: [
        [   {   'title':  'Es elemento de traducciones',
                'path':   [ 'object', ], 
                'types':  cTodosNombresTipos,    
                'roles':  [ cTRAManager_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
            {   'title':  'Modifiable TRACatalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRAManager_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Accesible collection of TRAProgreso',
                'path':   [ 'object', 'getCatalogo', 'fObtenerColeccionProgresos',],  
                'types':  [ cNombreTipoTRAColeccionProgresos,],    
                'roles':  [ cTRAManager_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [  'MPC', 'APC',], 
            },
        ],  
        [
            [ cTodosNombresTiposWithChildren      ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'MPC', ],   [ cTRAManager_role,] + cUbiquitousWriterRoles,],         
            [ cTodosNombresTiposWithoutChildren   ,cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', ],              [ cTRAManager_role,] + cUbiquitousWriterRoles,],         
            [ [ cNombreTipoTRAProgreso,]          ,cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', ],              [ cTRAManager_role,] + cUbiquitousWriterRoles,], 
        ],                                                                                           
    ],
    cUseCase_ConfigureTRACatalogo : [ 
        [   {   'title':  'Es TRACatalogo',
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role,cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', 'ADC',], 
            },
            {   'title':  'Modifiable TRACatalogo',
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRAManager_role,cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
        ],  
        [
        ],                                                                                           
    ],   
    cUseCase_LockTRACatalogo : [ 
        [   {   'title':  'Es TRACatalogo',
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',], 
            },
            {   'title':  'Unlocked TRACatalogo',
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRAManager_role, cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [  'MPC',], 
            },
        ],  
        [
        ],                                                                                           
    ],  
    cUseCase_UnlockTRACatalogo : [ 
        [   {   'title':  'Es TRACatalogo',
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',], 
            },
            {   'title':  'Locked TRACatalogo',
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'pred':   [ 'not:fAllowWrite',],
                'roles':  [ cTRAManager_role, cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [  'MPC',], 
            },
        ],  
        [
        ],                                                                                           
    ],  
    # ACV 20090924 Unused, Removed
    #
    #cUseCase_ReviewUsersAuthorizations : [ 
        #[   {   'title':  'Es TRACatalogo',
                #'path':   [ 'object', ],  
                #'types':  [ cNombreTipoTRACatalogo,],    
                #'roles':  [ cTRAManager_role, cTRACoordinator_role, ] +  cUbiquitousReaderRoles, 
                #'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            #},
        #],  
        #[
            ## [ cTodosNombresTiposColecciones          ,cPermissionsAbbreviatedFor_ViewElementAndChildren ,      [ cTRAManager_role,] +  cUbiquitousReaderRoles,],         
        #],                                                                                           
    #],   
    #cUseCase_AuthorizeUsers : [ 
        #[   {   'title':  'Es TRACatalogo',
                #'path':   [ 'object', ],  
                #'pred':   [ 'fAllowWrite',],
                #'types':  [ cNombreTipoTRACatalogo,],    
                #'roles':  [ cTRAManager_role, cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                #'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'MGR',], 
            #},
        #],  
        #[
            ## [ cTodosNombresTiposColecciones          ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'DOB', 'MPC', ],      [ cTRAManager_role,] +  cUbiquitousWriterRoles,],         
        #],                                                                                           
    #],   
    cUseCase_CreateMissingTRATraduccion : [ 
        [   {   'title':  'Es TRAImportacion',
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRAImportacion,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC',], 
            },
            {   'title':  'TRAImportacion without bound progress element or with a progress element not executed yet',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAImportacion,],     
                'pred':   [ 'fHasNoProgressElementOrNotExecuted',],
                'roles':  [  cTRAManager_role, cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC', ],
            }, 
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Modifiable TRACatalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRAManager_role, cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Accessible TRAColeccionCadenas',
                'path':   [ 'object', 'fObtenerColeccionCadenas', ],  
                'types':  [ cNombreTipoTRAColeccionCadenas,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Filtro TRAIdioma accesibles',
                'name':   'languages',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosIdiomas', ],  
                'types':  [ cNombreTipoTRAIdioma,],    
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRAManager_role, cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', ], 
            },
            {   'title':  'Filtro TRAModulo accesibles',
                'name':   'modules',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosModulos', ],  
                'types':  [ cNombreTipoTRAModulo,],    
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRAManager_role, cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', ], 
            },
        ],  
        [
            [ [ cNombreTipoTRACadena,]                  ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC', ],         [ cTRAManager_role, cTRACoordinator_role,] +  cUbiquitousWriterRoles,],         
            [ [ cNombreTipoTRATraduccion,]              ,cPermissionsAbbreviatedFor_ViewElement + [                          'MPC', ],         [ cTRAManager_role, cTRACoordinator_role,] +  cUbiquitousWriterRoles,],
       ],                                                                                           
    ],  
    cUseCase_CreateTRAImportacion: [ 
        [   {   'title':  'Es TRACatalogo o TRAColeccionImportaciones',
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRACatalogo, cNombreTipoTRAColeccionImportaciones],    
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Modifiable TRACatalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Accessible TRAColeccionImportaciones desde TRACatalogo',
                'path':   [ 'object', 'getCatalogo','fObtenerColeccionImportaciones'],
                'types':  [ cNombreTipoTRAColeccionImportaciones,],     
                'roles':  [  cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC',  ],
            }, 
        ],  
        [         
            [ [ cNombreTipoTRAImportacion,]         ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'DOB', 'MPC',  ],  [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles,],
        ],                                                                                           
    ],                                                                                                  
    cUseCase_DeleteTRAImportacion: [ 
        [   {   'title':  'Es TRAImportacion',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAImportacion],     
                'roles':  [  cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'MPC', 'DOB', ],
            }, 
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Modifiable TRACatalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Accessible TRAColeccionImportaciones',
                'path':   [ 'object', 'getContenedor',],
                'types':  [ cNombreTipoTRAColeccionImportaciones,],     
                'roles':  [  cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'MPC', ],
            }, 
            {   'title':  'Without any TRAContenidoIntercambio or all Accessible',
                'path':   [ 'object', 'getContenido', ],
                'types':  [ cNombreTipoTRAContenidoIntercambio, ],     
                'mode':   cUseCaseRuleMode_EmptyOrAll,
                'roles':  [  cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', 'DOB', ],
            }, 
        ],  
        [      
            #extras
        ],                                                                                           
    ],                                                                                                  
    cUseCase_CreateTRAContenidoIntercambio: [ 
        [   {   'title':  'Es TRAImportacion',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAImportacion,],     
                'roles':  [  cTRACoordinator_role,  ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC',  ],
            }, 
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Modifiable TRACatalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Accessible TRAColeccionImportaciones',
                'path':   [ 'object', 'getContenedor', ],
                'types':  [ cNombreTipoTRAColeccionImportaciones,],     
                'roles':  [  cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            }, 
        ],  
        [
            [ [ cNombreTipoTRAContenidoIntercambio,]   ,cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', ],  [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles,], 
        ],                                                                                           
    ],                                                                                                  
    cUseCase_DeleteTRAContenidoIntercambio: [ 
        [   {   'title':  'Es TRAContenidoIntercambio',
                'path':   [ 'object',  ],
                'types':  [ cNombreTipoTRAContenidoIntercambio,],     
                'roles':  [  cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', 'DOB', ],
            }, 
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Modifiable TRACatalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Accessible TRAImportacion',
                'path':   [ 'object', 'getContenedor', ],
                'types':  [ cNombreTipoTRAImportacion,],     
                'roles':  [  cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'MPC', ],
            }, 
            {   'title':  'Accessible TRAColeccionImportaciones del TRAImportacion',
                'path':   [ 'object', 'getContenedor', 'getContenedor', ],
                'types':  [ cNombreTipoTRAColeccionImportaciones,],     
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            }, 
        ],  
        [
            [ [ cNombreTipoTRAContenidoIntercambio,]   ,cPermissionsAbbreviatedFor_ViewElement + [ 'DOB', 'MPC',  ],  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles,], 
        ],                                                                                           
    ],                                                                                                  
    cUseCase_ImportTRAImportacion: [ 
        [   {   'title':  'Es TRAImportacion',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAImportacion,],     
                'roles':  [  cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC', ],
            }, 
            {   'title':  'TRAImportacion without bound progress element or with a progress element not executed yet',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAImportacion,],     
                'pred':   [ 'fHasNoProgressElementOrNotExecuted',],
                'roles':  [  cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC', ],
            }, 
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Modifiable TRACatalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Without any TRAContenidoIntercambio or all Accessible',
                'mode':   cUseCaseRuleMode_EmptyOrAll,
                'path':   [ 'object', 'getContenido',],
                'types':  [ cNombreTipoTRAContenidoIntercambio,],     
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement,
            }, 
            {   'title':  'Without TRAInforme before import or can be deleted',
                'mode':   cUseCaseRuleMode_EmptyOrAll,
                'path':   [ 'object', 'fInformeEstadoAntes',],
                'types':  [ cNombreTipoTRAInforme,],     
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'DOB', 'MPC',],
            }, 
            {   'title':  'Without TRAInforme after import or can be deleted',
                'mode':   cUseCaseRuleMode_EmptyOrAll,
                'path':   [ 'object', 'fInformeEstadoDespues',],
                'types':  [ cNombreTipoTRAInforme,],     
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'DOB', 'MPC',],
            }, 
            {   'title':  'Accessible TRAColeccionImportaciones',
                'path':   [ 'object', 'getContenedor', ],
                'types':  [ cNombreTipoTRAColeccionImportaciones,],     
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            }, 
            {   'title':  'Accessible TRAColeccionCadenas',
                'path':   [ 'object', 'getCatalogo', 'fObtenerColeccionCadenas', ],  
                'types':  [ cNombreTipoTRAColeccionCadenas,],    
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC',], 
            },
            {   'title':  'Filtro TRAIdioma accesibles',
                'name':   'languages',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosIdiomas', ],  
                'types':  [ cNombreTipoTRAIdioma,],    
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', ], 
            },
            {   'title':  'Filtro TRAModulo accesibles',
                'name':   'modules',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosModulos', ],  
                'types':  [ cNombreTipoTRAModulo,],    
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', ], 
            },
            {   'title':  'Accesible collection of TRAProgreso',
                'path':   [ 'object', 'getCatalogo', 'fObtenerColeccionProgresos',],  
                'types':  [ cNombreTipoTRAColeccionProgresos,],    
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [  'MPC', 'APC',], 
            },
        ],  
        [
            [ [ cNombreTipoTRAInforme,]                 ,cPermissionsAbbreviatedFor_ViewElement + [           'MPC', ],                 [ cTRACoordinator_role,] +  cUbiquitousWriterRoles,],         
            [ [ cNombreTipoTRACadena,]                  ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC', ],  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles,],         
            [ [ cNombreTipoTRATraduccion,]              ,cPermissionsAbbreviatedFor_ViewElement + [           'MPC', ],                 [ cTRACoordinator_role,] +  cUbiquitousWriterRoles,],
            [ [ cNombreTipoTRAProgreso,]                ,cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',],                            [ cTRACoordinator_role,] +  cUbiquitousWriterRoles,],
        ],                                                                                           
    ],   
    cUseCase_ImportTRAImportacion_ToCreateCadenas: [ 
        [   {   'title':  'Es TRAImportacion',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAImportacion,],     
                'roles':  [  cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC', ],
            }, 
            {   'title':  'TRAImportacion without bound progress element or with a progress element not executed yet',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAImportacion,],     
                'pred':   [ 'fHasNoProgressElementOrNotExecuted',],
                'roles':  [  cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC', ],
            }, 
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Without any TRAContenidoIntercambio or all Accessible',
                'mode':   cUseCaseRuleMode_EmptyOrAll,
                'path':   [ 'object', 'getContenido',],
                'types':  [ cNombreTipoTRAContenidoIntercambio,],     
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement,
            }, 
            {   'title':  'Without TRAInforme before import or can be deleted',
                'mode':   cUseCaseRuleMode_EmptyOrAll,
                'path':   [ 'object', 'fInformeEstadoAntes',],
                'types':  [ cNombreTipoTRAInforme,],     
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'DOB', 'MPC',],
            }, 
            {   'title':  'Without TRAInforme after import or can be deleted',
                'mode':   cUseCaseRuleMode_EmptyOrAll,
                'path':   [ 'object', 'fInformeEstadoDespues',],
                'types':  [ cNombreTipoTRAInforme,],     
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'DOB', 'MPC',],
            }, 
            {   'title':  'Accessible TRAColeccionImportaciones',
                'path':   [ 'object', 'getContenedor', ],
                'types':  [ cNombreTipoTRAColeccionImportaciones,],     
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            }, 
            {   'title':  'Accessible TRAColeccionCadenas',
                'path':   [ 'object', 'getCatalogo', 'fObtenerColeccionCadenas', ],  
                'types':  [ cNombreTipoTRAColeccionCadenas,],    
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC',], 
            },
            {   'title':  'Filtro TRAIdioma accesibles',
                'name':   'languages',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosIdiomas', ],  
                'types':  [ cNombreTipoTRAIdioma,],    
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', ], 
            },
            {   'title':  'Filtro TRAModulo accesibles',
                'name':   'modules',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosModulos', ],  
                'types':  [ cNombreTipoTRAModulo,],    
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', ], 
            },
            {   'title':  'Accesible collection of TRAProgreso',
                'path':   [ 'object', 'getCatalogo', 'fObtenerColeccionProgresos',],  
                'types':  [ cNombreTipoTRAColeccionProgresos,],    
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [  'MPC', 'APC',], 
            },
        ],  
        [
            [ [ cNombreTipoTRAInforme,]                 ,cPermissionsAbbreviatedFor_ViewElement + [           'MPC', ],         [ cTRACoordinator_role,cTRADeveloper_role,] +  cUbiquitousWriterRoles,],         
            [ [ cNombreTipoTRACadena,]                  ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC', ],  [ cTRACoordinator_role,cTRADeveloper_role,] +  cUbiquitousWriterRoles,],         
            [ [ cNombreTipoTRATraduccion,]              ,cPermissionsAbbreviatedFor_ViewElement + [           'MPC', ],         [ cTRACoordinator_role,cTRADeveloper_role,] +  cUbiquitousWriterRoles,],
            [ [ cNombreTipoTRAProgreso,]                ,cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',],                    [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles,],
        ],                                                                                           
    ],   
    cUseCase_ReuseTRAImportacion: [ 
        [   {   'title':  'Es TRAImportacion',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAImportacion,],     
                'roles':  [  cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC', ],
            }, 
            {   'title':  'Modifiable TRAImportacion',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAImportacion,],     
                'pred':   [ 'fAllowWrite',],
                'roles':  [  cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC', ],
            }, 
            {   'title':  'TRAImportacion with already executed bound Progress element',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAImportacion,],     
                'pred':   [ 'fHasProgressElementAlreadyExecuted',],
                'roles':  [  cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC', ],
            }, 
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Modifiable TRACatalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
        ],  
        [
        ],                                                                                           
    ],    
    cUseCase_Export: [    
        [   {   'title':  'Es TRACatalogo o TRAIdioma',
                'path':   [ 'object',],  
                'types':  [ cNombreTipoTRACatalogo, cNombreTipoTRAIdioma,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role,cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
            {   'title':  'Si TRACatalogo',
                'root':   [ cNombreTipoTRACatalogo],
                'path':   [ 'object',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role,cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Si TRAIdioma',
                'root':   [ cNombreTipoTRAIdioma],
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role,cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
            {   'title':  'Filter TRAIdioma todos los accesibles',
                'name':   'languages',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosIdiomas', ],  
                'types':  [ cNombreTipoTRAIdioma,],    
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRAManager_role, cTRACoordinator_role,cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
            {   'title':  'Filter TRAModulo todos los accesibles',
                'name':   'modules',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosModulos', ],  
                'types':  [ cNombreTipoTRAModulo,],    
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRAManager_role, cTRACoordinator_role,cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
            {   'title':  'Accesible collection of TRAProgreso',
                'path':   [ 'object', 'getCatalogo', 'fObtenerColeccionProgresos',],  
                'types':  [ cNombreTipoTRAColeccionProgresos,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [  'MPC', 'APC',], 
            },
        ],  
        [
            [ [ cNombreTipoTRACadena]                    ,cPermissionsAbbreviatedFor_ViewElementAndChildren,     [ cTRAManager_role, cTRACoordinator_role,cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role, ] +  cUbiquitousWriterRoles,],         
            [ [ cNombreTipoTRATraduccion,]               ,cPermissionsAbbreviatedFor_ViewElement + [ ],          [ cTRAManager_role, cTRACoordinator_role,cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role, ] +  cUbiquitousWriterRoles,],
            [ [ cNombreTipoTRAProgreso,]                 ,cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',],          [ cTRAManager_role, cTRACoordinator_role,cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role, ] +  cUbiquitousWriterRoles,],
        ],                                                                                           
    ],       
    cUseCase_Backup_TRACatalogo: [    
        [   {   'title':  'Es TRACatalogo',
                'path':   [ 'object',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Filter TRAIdioma todos los accesibles',
                'name':   'languages',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosIdiomas', ],  
                'types':  [ cNombreTipoTRAIdioma,],    
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRAManager_role, cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
            {   'title':  'Filter TRAModulo todos los accesibles',
                'name':   'modules',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosModulos', ],  
                'types':  [ cNombreTipoTRAModulo,],    
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRAManager_role, cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
            {   'title':  'Accesible collection of TRAProgreso',
                'path':   [ 'object', 'getCatalogo', 'fObtenerColeccionProgresos',],  
                'types':  [ cNombreTipoTRAColeccionProgresos,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [  'MPC', 'APC',], 
            },
        ],  
        [
            [ [ cNombreTipoTRACadena]                    ,cPermissionsAbbreviatedFor_ViewElementAndChildren,     [ cTRAManager_role, cTRACoordinator_role, ] +  cUbiquitousWriterRoles,],         
            [ [ cNombreTipoTRATraduccion,]               ,cPermissionsAbbreviatedFor_ViewElement + [ ],          [ cTRAManager_role, cTRACoordinator_role, ] +  cUbiquitousWriterRoles,],
            [ [ cNombreTipoTRAProgreso,]                 ,cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',],          [ cTRAManager_role, cTRACoordinator_role, ] +  cUbiquitousWriterRoles,],
        ],                                                                                           
    ],       
    cUseCase_ExportGvSIG_TRAIdioma: [
        [   {   'title':  'Es TRAIdioma',
                'path':   [ 'object',],  
                'types':  [ cNombreTipoTRAIdioma,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role,cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Accessible TRAIdioma',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRAIdioma,],    
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRAManager_role, cTRACoordinator_role,cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
            {   'title':  'Filter TRAModulo todos los accesibles',
                'name':   'modules',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosModulos', ],  
                'types':  [ cNombreTipoTRAModulo,],    
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRAManager_role, cTRACoordinator_role,cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
            {   'title':  'Accesible collection of TRAProgreso',
                'path':   [ 'object', 'getCatalogo', 'fObtenerColeccionProgresos',],  
                'types':  [ cNombreTipoTRAColeccionProgresos,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role,cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [  'MPC', 'APC',], 
            },
        ],  
        [
            [ [ cNombreTipoTRACadena]                    ,cPermissionsAbbreviatedFor_ViewElementAndChildren,     [ cTRAManager_role, cTRACoordinator_role,cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] +  cUbiquitousWriterRoles,],         
            [ [ cNombreTipoTRATraduccion,]               ,cPermissionsAbbreviatedFor_ViewElement + [ ],          [ cTRAManager_role, cTRACoordinator_role,cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] +  cUbiquitousWriterRoles,],
            [ [ cNombreTipoTRAProgreso,]                 ,cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',],          [ cTRAManager_role, cTRACoordinator_role,cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] +  cUbiquitousWriterRoles,],
        ],                                                                                           
    ],               
    cUseCase_EllaborateInformeActividad: [
        [   {   'title':  'Es TRACatalogo',
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Filtro TRAIdioma accesibles',
                'name':   'languages',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosIdiomas', ],  
                'types':  [ cNombreTipoTRAIdioma,],    
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role, ] +  cUbiquitousReaderRoles,    
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
        ],  
        [
        ],                                                                                           
    ],                                                                                                  
    cUseCase_EllaborateInformeLanguages: [   
        [   {   'title':  'Es TRACatalogo o TRAInforme',
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRACatalogo, cNombreTipoTRAInforme,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role,  cTRATranslator_role, cTRAVisitor_role, ] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement , 
            },
            {   'title':  'Si TRACatalogo',
                'root':   [ cNombreTipoTRACatalogo],
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role,  cTRATranslator_role, cTRAVisitor_role, ] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren , 
            },
            {   'title':  'Si TRAInforme',
                'root':   [ cNombreTipoTRAInforme],
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRAInforme],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role,  cTRATranslator_role, cTRAVisitor_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',], 
            },
            {   'title':  'Accesible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role,  cTRATranslator_role, cTRAVisitor_role, ] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Modifiable TRACatalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'pred':   [ 'fAllowWrite',],
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role,  cTRATranslator_role, cTRAVisitor_role, ] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Filtro TRAIdioma accesibles',
                'name':   'languages',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosIdiomas', ],  
                'types':  [ cNombreTipoTRAIdioma,],    
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role,  cTRATranslator_role, cTRAVisitor_role, ] +  cUbiquitousReaderRoles,    
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
        ],  
        [
        ],                                                                                           
    ],                                                                                                  
    cUseCase_EllaborateInformeModulesAndLanguages: [     
        [   
            {   'title':  'Es TRACatalogo o TRAInforme',
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRACatalogo, cNombreTipoTRAInforme],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role,  cTRATranslator_role, cTRAVisitor_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },            
            {   'title':  'Si TRACatalogo',
                'root':   [ cNombreTipoTRACatalogo],
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role,  cTRATranslator_role, cTRAVisitor_role, ] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren , 
            },
            {   'title':  'Si TRAInforme',
                'root':   [ cNombreTipoTRAInforme],
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRAInforme],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role,  cTRATranslator_role, cTRAVisitor_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement+ [ 'MPC',], 
            },
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role,  cTRATranslator_role, cTRAVisitor_role, ] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Modifiable TRACatalogo',
                'name':   'Modifiable TRACatalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role,  cTRATranslator_role, cTRAVisitor_role, ] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Filtro TRAIdioma accesibles',
                'name':   'languages',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosIdiomas', ],  
                'types':  [ cNombreTipoTRAIdioma,],    
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role,  cTRATranslator_role, cTRAVisitor_role, ] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
            {   'title':  'Filtro TRAModulo accesibles',
                'name':   'modules',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosModulos', ],  
                'types':  [ cNombreTipoTRAModulo,],    
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role,  cTRATranslator_role, cTRAVisitor_role, ] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
        ],  
        [
        ],                                                                                           
    ],       
    cUseCase_CreateTRAInforme: [     
        [   {   'title':  'Es TRAColeccionInformes',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAColeccionInformes,],     
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'APC', 'APF', 'MPC',  ],
            }, 
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Modifiable TRACatalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Filtro TRAIdioma accesibles',
                'name':   'languages',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosIdiomas', ],  
                'types':  [ cNombreTipoTRAIdioma,],    
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role,] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
            {   'title':  'Filtro TRAModulo accesibles',
                'name':   'modules',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosModulos', ],  
                'types':  [ cNombreTipoTRAModulo,],    
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role,] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
        ],  
        [
            [ [ cNombreTipoTRAInforme,]                  ,cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', 'DOB',],           [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role,] +  cUbiquitousWriterRoles,], 
        ],                                                                                           
    ],       
    cUseCase_CreateAndDeleteTRAInformeInTRAImportacion: [     
        [   {   'title':  'Es TRAImportacion',
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAImportacion,],    
                'roles':  [ cTRACoordinator_role,cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'APC', 'APF', 'MPC'], 
            },
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role,cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Modifiable TRAImportacion',
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRAImportacion,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role,cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Filter accessible TRAInforme',
                'name':   'informes',
                'mode':   cUseCaseRuleMode_Filter ,
                'path':   [ 'object', 'getInformesEstado',],  
                'types':  [ cNombreTipoTRAInforme,],    
                'roles':  [ cTRACoordinator_role,cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC','DOB',], 
            },
            {   'title':  'Filtro TRAIdioma accesibles',
                'name':   'languages',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosIdiomas', ],  
                'types':  [ cNombreTipoTRAIdioma,],    
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
            {   'title':  'Filtro TRAModulo accesibles',
                'name':   'modules',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosModulos', ],  
                'types':  [ cNombreTipoTRAModulo,],    
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
        ],  
        [
            [ [ cNombreTipoTRAInforme,]                  ,cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', 'DOB',],     [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles,], 
          ],                                                                                           
    ],                                                                                                                                                   
    cUseCase_ListLanguagesAndModules: [                      
        [   
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',], 
                'types':  [ cNombreTipoTRACatalogo,],     
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role, cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'Filter TRAIdioma',
                'name':   'languages',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosIdiomas',],  
                'types':  [ cNombreTipoTRAIdioma,],    
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role, cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Filter TRAModulo',
                'name':   'modules',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosModulos', ],  
                'types':  [ cNombreTipoTRAModulo,],    
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role, cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
        ],
        [
            # extras
        ],                                                                                 
    ],                                                                                         
    cUseCase_View: [                      
        [   
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',], 
                'types':  [ cNombreTipoTRACatalogo,],     
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'If TRACatalogo',
                'root':   [ cNombreTipoTRACatalogo,],
                'path':   [ 'object',], 
                'types':  [ cNombreTipoTRACatalogo,],     
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'If TRAColeccionIdiomas',
                'root':   [ cNombreTipoTRAColeccionIdiomas,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAColeccionIdiomas,],     
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'If TRAIdioma',
                'root':   [ cNombreTipoTRAIdioma,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAIdioma,],     
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement,                 
            },
            {   'title':  'If TRAColeccionModulos',
                'root':   [ cNombreTipoTRAColeccionModulos,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAColeccionModulos,],     
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'If TRAModulo',
                'root':   [ cNombreTipoTRAModulo,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAModulo,],     
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement,                 
            },
            {   'title':  'If TRAColeccionCadenas',
                'root':   [ cNombreTipoTRAColeccionCadenas,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAColeccionCadenas,],     
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'If TRACadena',
                'root':   [ cNombreTipoTRACadena,],
                'path':   [ 'object', ],   
                'types':  [ cNombreTipoTRACadena,],       
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,    
            },
            {   'title':  'If TRACadena accesible TRAColeccionCadenas',
                'root':   [ cNombreTipoTRACadena,],
                'path':   [ 'object', 'getContenedor',],   
                'types':  [ cNombreTipoTRAColeccionCadenas,],       
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,    
            },
            {   'title':  'If TRACadena accesible TRAColeccionCadenas desde TRACatalogo',
                'root':   [ cNombreTipoTRACadena,],
                'path':   [ 'object', 'getCatalogo', 'fObtenerColeccionCadenas', ],  
                'types':  [ cNombreTipoTRAColeccionCadenas,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'If TRACadena Filter No TRAModulo or at least one accesible TRAModulo',
                'root':   [ cNombreTipoTRACadena,],
                'mode':   cUseCaseRuleMode_EmptyOrAny,
                'path':   [ 'object', 'getModulos',],   
                'types':  [ cNombreTipoTRAModulo,], 
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement,    
            },
            {   'title':  'If TRATraduccion',
                'root':   [ cNombreTipoTRATraduccion,],
                'path':   [ 'object',],   
                'types':  [ cNombreTipoTRATraduccion,],       
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement,    
            },
            {   'title':  'If TRATraduccion accesible TRACadena',
                'root':   [ cNombreTipoTRATraduccion,],
                'path':   [ 'object', 'getContenedor',],   
                'types':  [ cNombreTipoTRACadena,],       
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,    
            },
            {   'title':  'If TRATraduccion accesible TRAColeccionCadenas',
                'root':   [ cNombreTipoTRATraduccion,],
                'path':   [ 'object', 'getContenedor','getContenedor',],   
                'types':  [ cNombreTipoTRAColeccionCadenas,],       
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,    
            },
            {   'title':  'If TRATraduccion accesible TRAColeccionCadenas desde TRACatalogo',
                'root':   [ cNombreTipoTRATraduccion,],
                'path':   [ 'object', 'getCatalogo', 'fObtenerColeccionCadenas', ],  
                'types':  [ cNombreTipoTRAColeccionCadenas,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'If TRATraduccion Filter No TRAModulo or at least one accesible TRAModulo',
                'root':   [ cNombreTipoTRATraduccion,],
                'mode':   cUseCaseRuleMode_EmptyOrAny,
                'path':   [ 'object', 'getCadena', 'getModulos',],   
                'types':  [ cNombreTipoTRAModulo,], 
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement,    
            }, 
            {   'title':  'If TRATraduccion accesible TRAIdioma',
                'root':   [ cNombreTipoTRATraduccion,],
                'path':   [ 'object', 'getIdioma',],   
                'types':  [ cNombreTipoTRAIdioma,],       
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement,    
            },
            {   'title':  'If TRAColeccionImportaciones',
                'root':   [ cNombreTipoTRAColeccionImportaciones,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAColeccionImportaciones,],     
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'If TRAImportacion',
                'root':   [ cNombreTipoTRAImportacion,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAImportacion,],     
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'IF TRAImportacion accesible TRAColeccionImportaciones',
                'root':   [ cNombreTipoTRAImportacion,],
                'path':   [ 'object', 'getContenedor',],  
                'types':  [ cNombreTipoTRAColeccionImportaciones,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'IF TRAImportacion accesible TRAColeccionImportaciones desde TRACatalogo',
                'root':   [ cNombreTipoTRAImportacion,],
                'path':   [ 'object', 'getCatalogo', 'fObtenerColeccionImportaciones', ],  
                'types':  [ cNombreTipoTRAColeccionImportaciones,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'If TRAContenidoIntercambio',
                'root':   [ cNombreTipoTRAContenidoIntercambio,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAContenidoIntercambio,],     
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement,                 
            },
            {   'title':  'IF TRAContenidoIntercambio accesible TRAImportacion',
                'root':   [ cNombreTipoTRAContenidoIntercambio,],
                'path':   [ 'object', 'getContenedor',],  
                'types':  [ cNombreTipoTRAImportacion,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
            {   'title':  'If TRAColeccionInformes',
                'root':   [ cNombreTipoTRAColeccionInformes,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAColeccionInformes,],     
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'If TRAInforme',
                'root':   [ cNombreTipoTRAInforme,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAInforme,],     
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement,                 
            },
            {   'title':  'IF TRAInforme accesible TRAColeccionInformes',
                'root':   [ cNombreTipoTRAInforme,],
                'path':   [ 'object', 'getContenedor',],  
                'types':  [ cNombreTipoTRAColeccionInformes,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
            {   'title':  'IF TRAInforme accesible TRAColeccionInformes desde TRACatalogo',
                'root':   [ cNombreTipoTRAInforme,],
                'path':   [ 'object', 'getCatalogo', 'fObtenerColeccionInformes', ],  
                'types':  [ cNombreTipoTRAColeccionInformes,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
            {   'title':  'If TRAColeccionSolicitudesCadenas',
                'root':   [ cNombreTipoTRAColeccionSolicitudesCadenas,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAColeccionSolicitudesCadenas,],     
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'If TRASolicitudCadena',
                'root':   [ cNombreTipoTRASolicitudCadena,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRASolicitudCadena,],     
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement,                 
            },
            {   'title':  'IF TRASolicitudCadena accesible TRAColeccionSolicitudesCadenas',
                'root':   [ cNombreTipoTRASolicitudCadena,],
                'path':   [ 'object', 'getContenedor',],  
                'types':  [ cNombreTipoTRAColeccionSolicitudesCadenas,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'IF TRASolicitudCadena accesible TRAColeccionSolicitudesCadenas desde TRACatalogo',
                'root':   [ cNombreTipoTRASolicitudCadena,],
                'path':   [ 'object', 'getCatalogo', 'fObtenerColeccionSolicitudesCadenas', ],  
                'types':  [ cNombreTipoTRAColeccionSolicitudesCadenas,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'If TRAColeccionProgresos',
                'root':   [ cNombreTipoTRAColeccionProgresos,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAColeccionProgresos,],     
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'If TRAProgreso',
                'root':   [ cNombreTipoTRAProgreso,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAProgreso,],     
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement,                 
            },
            {   'title':  'IF TRAProgreso accesible TRAColeccionProgresos',
                'root':   [ cNombreTipoTRAProgreso,],
                'path':   [ 'object', 'getContenedor',],  
                'types':  [ cNombreTipoTRAColeccionProgresos,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'IF TRAProgreso accesible TRAColeccionProgresos desde TRACatalogo',
                'root':   [ cNombreTipoTRAProgreso,],
                'path':   [ 'object', 'getCatalogo', 'fObtenerColeccionProgresos', ],  
                'types':  [ cNombreTipoTRAColeccionProgresos,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'If TRAParametrosControlProgreso',
                'root':   [ cNombreTipoTRAParametrosControlProgreso,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAParametrosControlProgreso,],     
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement,                 
            },
            {   'title':  'IF TRAParametrosControlProgreso accesible TRACatalogo',
                'root':   [ cNombreTipoTRAParametrosControlProgreso,],
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
        ],
        [
            # extras
        ],                                                                                 
    ],                                                                                         
    cUseCase_BrowseTranslations: [                     
        [   {   'title':  'Es TRACatalogo',
                'path':   [ 'object', ],   
                'types':  [ cNombreTipoTRACatalogo,],       
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role, cTRAVisitor_role, ] + cUbiquitousReaderRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,    
            },
            {   'title':  'Filtro TRAIdioma accesibles',
                'name':   'languages',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosIdiomas', ],  
                'types':  [ cNombreTipoTRAIdioma,],    
                'pred':   [ 'fAllowRead',],
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role, cTRAVisitor_role, ] + cUbiquitousReaderRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
            {   'title':  'Filtro TRAIdioma modificables',
                'name':   'changeable_languages',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosIdiomas', ],  
                'types':  [ cNombreTipoTRAIdioma,],    
                'pred':   [ 'fAllowRead', 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role, cTRAVisitor_role, ] + cUbiquitousReaderRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
            {   'title':  'Filtro TRAModulo accesibles',
                'name':   'modules',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosModulos', ],  
                'types':  [ cNombreTipoTRAModulo,],    
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role, cTRAVisitor_role, ] + cUbiquitousReaderRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
            {   'title':  'Filtro TRAModulo modificables',
                'name':   'changeable_modules',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosModulos', ],  
                'types':  [ cNombreTipoTRAModulo,],    
                'pred':   [ 'fAllowRead', 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role, cTRAVisitor_role, ] + cUbiquitousReaderRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
        ],
        [
        ],                                                                                 
    ],                                                                                         
    cUseCase_DeactivateTRACadena: [                     
        [   {   'title':  'Es TRACadena',
                'name':   'cadena',
                'path':   [ 'object', ],   
                'types':  [ cNombreTipoTRACadena,],       
                'roles':  [ cTRACoordinator_role, ] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',],    
            },
            {   'title':  'Active TRACadena',
                'path':   [ 'object', ],   
                'types':  [ cNombreTipoTRACadena,],       
                'pred':   [ 'fIsActive',],
                'roles':  [ cTRACoordinator_role, ] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',],    
            },
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',], 
                'types':  [ cNombreTipoTRACatalogo,],     
                'roles':  [ cTRACoordinator_role, ] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'Modifiable TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',], 
                'types':  [ cNombreTipoTRACatalogo,],     
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, ] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
        ],
        [
        ],                                                                                 
    ],            
    cUseCase_ActivateTRACadena: [                     
        [   {   'title':  'Es TRACadena',
                'name':   'cadena',
                'path':   [ 'object', ],   
                'types':  [ cNombreTipoTRACadena,],       
                'roles':  [ cTRACoordinator_role, ] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',],    
            },
            {   'title':  'Inactive TRACadena',
                'path':   [ 'object', ],   
                'types':  [ cNombreTipoTRACadena,],       
                'pred':   [ 'fIsInactive',],
                'roles':  [ cTRACoordinator_role, ] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',],    
            },
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',], 
                'types':  [ cNombreTipoTRACatalogo,],     
                'roles':  [ cTRACoordinator_role, ] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'Modifiable TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',], 
                'types':  [ cNombreTipoTRACatalogo,],     
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, ] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
        ],
        [
        ],                                                                                 
    ],            
    cUseCase_TRATraduccionStateChange: [                     
        [   {   'title':  'Es TRATraduccion',
                'name':   'traduccion',
                'path':   [ 'object', ],   
                'types':  [ cNombreTipoTRATraduccion,],       
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',],    
            },
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',], 
                'types':  [ cNombreTipoTRACatalogo,],     
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] + cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'Modifiable TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',], 
                'types':  [ cNombreTipoTRACatalogo,],     
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] + cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'Accessible TRACadena',
                'name':   'cadena',
                'path':   [ 'object', 'getCadena',],   
                'types':  [ cNombreTipoTRACadena,],       
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,    
            },
            {   'title':  'Accessible TRAIdioma',
                'name':   'idioma',
                'path':   [ 'object', 'getIdioma',],   
                'types':  [ cNombreTipoTRAIdioma,],       
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',],    
            },
            {   'title':  'Modificable TRAIdioma',
                'name':   'idioma',
                'path':   [ 'object', 'getIdioma',],   
                'types':  [ cNombreTipoTRAIdioma,],       
                'pred':   [ 'fAllowRead', 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',],    
            },
            {   'title':  'TRACadena Without any TRAModulo or at least one accessible',
                'name':   'modulos',
                'mode':   cUseCaseRuleMode_EmptyOrAny,
                'path':   [ 'object', 'getCadena','getModulos',],   
                'types':  [ cNombreTipoTRAModulo,], 
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',],    
            },
        ],
        [
        ],                                                                                 
    ],            
    cUseCase_InvalidateStringTranslations: [                     
        [   {   'title':  'Es TRACadena',
                'name':   'cadena',
                'path':   [ 'object', ],   
                'types':  [ cNombreTipoTRACadena,],       
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',],    
            },
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',], 
                'types':  [ cNombreTipoTRACatalogo,],     
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'Modifiable TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',], 
                'types':  [ cNombreTipoTRACatalogo,],     
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'Filtro TRAIdioma modificables',
                'name':   'changeable_languages',
                'path':   [ 'object', 'getIdioma',],   
                'types':  [ cNombreTipoTRAIdioma,],       
                'pred':   [ 'fAllowRead', 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',],    
            },
            {   'title':  'TRACadena Without any TRAModulo or at least one accessible',
                'name':   'modulos',
                'mode':   cUseCaseRuleMode_EmptyOrAny,
                'path':   [ 'object', 'getCadena','getModulos',],   
                'types':  [ cNombreTipoTRAModulo,], 
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',],    
            },
        ],
        [
        ],                                                                                 
    ],            
    cUseCase_TRATraduccionComment: [                     
        [   {   'title':  'Es TRATraduccion',
                'name':   'traduccion',
                'path':   [ 'object', ],   
                'types':  [ cNombreTipoTRATraduccion,],       
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',],    
            },
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',], 
                'types':  [ cNombreTipoTRACatalogo,],     
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] + cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'Modifiable TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',], 
                'types':  [ cNombreTipoTRACatalogo,],     
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] + cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'Accessible TRACadena',
                'name':   'cadena',
                'path':   [ 'object', 'getCadena',],   
                'types':  [ cNombreTipoTRACadena,],       
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,    
            },
            {   'title':  'Accessible TRAIdioma',
                'name':   'idioma',
                'path':   [ 'object', 'getIdioma',],   
                'types':  [ cNombreTipoTRAIdioma,],       
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',],    
            },
            {   'title':  'Modificable TRAIdioma',
                'name':   'idioma',
                'path':   [ 'object', 'getIdioma',],   
                'types':  [ cNombreTipoTRAIdioma,],       
                'pred':   [ 'fAllowRead', 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',],    
            },
            {   'title':  'TRACadena Without any TRAModulo or at least one accessible',
                'name':   'modulos',
                'mode':   cUseCaseRuleMode_EmptyOrAny,
                'path':   [ 'object', 'getCadena','getModulos',],   
                'types':  [ cNombreTipoTRAModulo,], 
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, cTRAReviewer_role, cTRATranslator_role,] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',],    
            },
        ],
        [
        ],                                                                                 
    ],                                                                                         
    cUseCase_CreateTRASolicitudCadena: [ 
        [   {   'title':  'Es TRAColeccionSolicitudesCadena',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAColeccionSolicitudesCadenas,],     
                'roles':  [  cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC',  ],
            }, 
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Modifiable TRAColeccionSolicitudesCadena',
                'path':   [ 'object',],  
                'types':  [ cNombreTipoTRAColeccionSolicitudesCadenas,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC',  ],
            },
        ],  
        [
            [ [ cNombreTipoTRASolicitudCadena,]  ,cPermissionsAbbreviatedFor_ViewElement + [ 'APC', 'MPC', ],  [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles,], 
        ],                                                                                           
    ],                                                                                                  
    cUseCase_CreateTRAIdioma: [ 
        [   {   'title':  'Es TRAColeccionIdiomas',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAColeccionIdiomas,],     
                'roles':  [  cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC',  ],
            }, 
            {   'title':  'Filtro todos TRAIdioma accesibles',
                'name':   'languages',
                'mode':   cUseCaseRuleMode_Filter,                
                'path':   [ 'object', 'fObtenerTodosIdiomas',],
                'types':  [ cNombreTipoTRAIdioma,],     
                'roles':  [  cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement,
            }, 
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Modifiable TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
        ],  
        [
            [ [ cNombreTipoTRAIdioma,]  ,cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', ],  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles,], 
        ],                                                                                           
    ],      
    cUseCase_DeleteTRAIdioma : [
        [   {   'title':  'Es TRAIdioma',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAIdioma,],     
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'DOB', 'MPC',  ],
            }, 
            {   'title':  'Modifiable TRAColeccionIdiomas',
                'path':   [ 'object', 'getContenedor()', ],
                'types':  [ cNombreTipoTRAColeccionIdiomas,],     
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'MPC',  ],
            }, 
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Modifiable TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Accesible collection of TRAProgreso',
                'path':   [ 'object', 'getCatalogo', 'fObtenerColeccionProgresos',],  
                'types':  [ cNombreTipoTRAColeccionProgresos,],    
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [  'MPC', 'APC',], 
            },
        ],  
        [
            [ [ cNombreTipoTRACadena,]  ,  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'MPC', ],        [ cTRACoordinator_role,] +  cUbiquitousWriterRoles,], 
            [ [ cNombreTipoTRAIdioma,]  ,  cPermissionsAbbreviatedFor_ViewElement            + [ 'MPC', 'DOB',],  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles,], 
            [ [ cNombreTipoTRATraduccion,],cPermissionsAbbreviatedFor_ViewElement            + [ 'MPC', 'DOB',],  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles,], 
            [ [ cNombreTipoTRAProgreso,],  cPermissionsAbbreviatedFor_ViewElement            + [ 'MPC', ],        [ cTRACoordinator_role,] +  cUbiquitousWriterRoles,], 
        ],                                                                                           
    ],    
    cUseCase_CreateTRAModulo: [ 
        [   {   'title':  'Es TRAColeccionModulos',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAColeccionModulos,],     
                'roles':  [  cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC',  ],
            }, 
            {   'title':  'Filtro todos TRAModulo accesibles',
                'name':   'languages',
                'mode':   cUseCaseRuleMode_Filter,                
                'path':   [ 'object', 'fObtenerTodosModulos',],
                'types':  [ cNombreTipoTRAModulo,],     
                'roles':  [  cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement,
            }, 
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Modifiable TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
        ],  
        [
            [ [ cNombreTipoTRAModulo,]  ,cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', ],  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles,], 
        ],                                                                                           
    ],
    cUseCase_DeleteTRAModulo : [
        [   {   'title':  'Es TRAModulo',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAModulo,],     
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'DOB', 'MPC',  ],
            }, 
            {   'title':  'Modifiable TRAColeccionModulos',
                'path':   [ 'object', 'getContenedor()', ],
                'types':  [ cNombreTipoTRAColeccionModulos,],     
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'MPC',  ],
            }, 
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Modifiable TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Accesible collection of TRAProgreso',
                'path':   [ 'object', 'getCatalogo', 'fObtenerColeccionProgresos',],  
                'types':  [ cNombreTipoTRAColeccionProgresos,],    
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [  'MPC', 'APC',], 
            },
        ],  
        [
            [ [ cNombreTipoTRACadena,]  ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'MPC', ],  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles,], 
            [ [ cNombreTipoTRAProgreso,],cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', ],             [ cTRACoordinator_role,] +  cUbiquitousWriterRoles,], 
        ],                                                                                           
    ],
    cUseCase_CreateTRACadena: [ 
        [   {   'title':  'Es TRAColeccionSolicitudesCadena',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAColeccionSolicitudesCadenas,],     
                'roles':  [  cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC',  ],
            }, 
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Modifiable TRAColeccionSolicitudesCadena',
                'path':   [ 'object',],  
                'types':  [ cNombreTipoTRAColeccionSolicitudesCadenas,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC',  ],
            },
        ],  
        [
            [ [ cNombreTipoTRACadena,]  ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC', ],  [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles,], 
        ],                                                                                           
    ],                                                                                                  
    cUseCase_CleanupTRAColeccionSolicitudesCadenas: [ 
        [   {   'title':  'Es TRAColeccionSolicitudesCadena',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAColeccionSolicitudesCadenas,],     
                'roles':  [  cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'MPC',  ],
            }, 
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Modifiable TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
             {  'title':  'Filtro TRASolicitudCadena accesibles',
                'name':   'solicitudesCadeaa',
                'mode':   cUseCaseRuleMode_EmptyOrAll,
                'path':   [ 'object', 'fObtenerTodasSolicitudesCadena', ],  
                'types':  [ cNombreTipoTRASolicitudCadena,],    
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', 'DOB', ], 
            },
        ],  
        [
        ],                                                                                           
    ],        
    cUseCase_Copy_Translations: [ 
        [   {   'title':  'Es TRAIdioma',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAIdioma,],     
                'roles':  [  cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC', ],
            }, 
            {   'title':  'Modificable TRAIdioma',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAIdioma,],   
                'pred':   [ 'fAllowRead', 'fAllowWrite',],                
                'roles':  [  cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', ],
            }, 
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Modifiable TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Filtro otros TRAIdioma accesibles',
                'name':   'languages',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'fObtenerOtrosIdiomas', ],  
                'types':  [ cNombreTipoTRAIdioma,],    
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement , 
            },
        ],  
        [
        ],  
    ],
    cUseCase_UnlockTRAIdioma: [ 
        [   {   'title':  'Es TRAIdioma',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAIdioma,],     
                'roles':  [  cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'MPC', ],
            }, 
            {   'title':  'Locked TRAIdioma',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAIdioma,],   
                'pred':   [ 'fIsLocked',],                
                'roles':  [  cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', ],
            }, 
            {   'title':  'Acessible TRAIdioma',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAIdioma,],   
                'pred':   [ 'fAllowRead',],                
                'roles':  [  cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', ],
            }, 
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Modifiable TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
        ],  
        [
        ],  
    ],
    cUseCase_LockTRAIdioma: [ 
        [   {   'title':  'Es TRAIdioma',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAIdioma,],     
                'roles':  [  cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC', ],
            }, 
            {   'title':  'Unlocked TRAIdioma',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAIdioma,],   
                'pred':   [ 'fIsUnlocked',],                
                'roles':  [  cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', ],
            }, 
            {   'title':  'Modificable TRAIdioma',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAIdioma,],   
                'pred':   [ 'fAllowRead', 'fAllowWrite',],                
                'roles':  [  cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', ],
            }, 
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Modifiable TRACatalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
        ],  
        [
        ],  
    ],
    cUseCase_AddModulesToTRACadena: [ 
        [   {   'title':  'Es TRACadena',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRACadena,],     
                'roles':  [  cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            }, 
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Modifiable TRACadena',
                'path':   [ 'object',],  
                'types':  [ cNombreTipoTRACadena,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'MPC',  ],
            },
            {   'title':  'Filtro TRAModulo accesibles',
                'name':   'modules',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosModulos', ],  
                'types':  [ cNombreTipoTRAModulo,],    
                'roles':  [ cTRACoordinator_role, cTRADeveloper_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
        ],  
        [
        ],     
    ],
    cUseCase_RemoveModulesFromTRACadena: [ 
        [   {   'title':  'Es TRACadena',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRACadena,],     
                'roles':  [  cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            }, 
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Modifiable TRACadena',
                'path':   [ 'object',],  
                'types':  [ cNombreTipoTRACadena,],    
                'pred':   [ 'fAllowWrite',],
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'MPC',  ],
            },
            {   'title':  'Filtro TRAModulo accesibles',
                'name':   'modules',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosModulos', ],  
                'types':  [ cNombreTipoTRAModulo,],    
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement, 
            },
        ],  
        [
        ],     
    ],
 }


cTRAUseCasesWithAbbreviatedPermissions[ cUseCase_AdvancedView] = cTRAUseCasesWithAbbreviatedPermissions[ cUseCase_View][:]
cTRAUseCasesWithAbbreviatedPermissions[ cUseCase_Permissions]  = cTRAUseCasesWithAbbreviatedPermissions[ cUseCase_View][:]











    
    

