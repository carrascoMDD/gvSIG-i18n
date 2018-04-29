# -*- coding: utf-8 -*-
#
# File: TRAElemento_Permission_Definitions.py
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

from Products.CMFCore       import permissions

from Products.PluggableAuthService.permissions import ManageGroups                  as perm_ManageGroups
from AccessControl.Permissions                 import access_contents_information   as perm_AccessContentsInformation


from TRARoles               import *
from TRAElemento_Constants  import *





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
cTRAReviewers_group      = "TRAReviewers"
cTRATranslators_group    = "TRATranslators"
cTRAVisitors_group       = "TRAVisitors"


cTRAPreferredUserGroupsOrder = [
    cTRAManagers_group,     
    cTRACoordinators_group, 
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
    [ cTRAReviewers_group,      [ cTRAReviewer_role,      ], ],
    [ cTRATranslators_group,    [ cTRATranslator_role,    ], ],
    [ cTRAVisitors_group,       [ cTRAVisitor_role,       ], ],
]

cTRAUserGroups_Catalogo_AuthorizedOnCatalogo = [ unGrAndRs[ 0] for unGrAndRs in cTRAUserGroups_Catalogo] 

cTRAUserGroups_Catalogo_AuthorizedOnIndividualIdiomas = [
    cTRAManagers_group,
    cTRACoordinators_group,
]

cTRAUserGroups_Catalogo_AuthorizedOnIndividualModulos = [
    cTRAManagers_group,
    cTRACoordinators_group,
]


cTRAUserGroups_AllIdiomas = [
    [ cTRACoordinators_group,   [ cTRACoordinator_role,   ], ],
    [ cTRAReviewers_group,      [ cTRAReviewer_role,      ], ],
    [ cTRATranslators_group,    [ cTRATranslator_role,    ], ],
    [ cTRAVisitors_group,       [ cTRAVisitor_role,       ], ],
]

cTRAUserGroups_AllIdiomas_AuthorizedOnColeccionIdiomas  = [ unGrAndRs[ 0] for unGrAndRs in cTRAUserGroups_AllIdiomas] 
cTRAUserGroups_AllIdiomas_AuthorizedOnIndividualIdiomas = [ unGrAndRs[ 0] for unGrAndRs in cTRAUserGroups_AllIdiomas] 



cTRAUserGroups_AllModulos = [
    [ cTRACoordinators_group,   [ cTRACoordinator_role,   ], ],
    [ cTRAReviewers_group,      [ cTRAReviewer_role,      ], ],
    [ cTRATranslators_group,    [ cTRATranslator_role,    ], ],
    [ cTRAVisitors_group,       [ cTRAVisitor_role,       ], ],
]

cTRAUserGroups_AllModulos_AuthorizedOnColeccionModulos = [ unGrAndRs[ 0] for unGrAndRs in cTRAUserGroups_AllModulos] 




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
TRAColeccionIdiomas does not acquire.
TRAIdioma shall cut if the language is to be managged by language specific groups

The configuration for language becoming managed by its specific group
is controlled by a management function of the application.

"""
cTypesAcquiringRoleAssignments =  [
    cNombreTipoTRACatalogo,               
    cNombreTipoTRAIdioma,                 
    cNombreTipoTRAColeccionModulos, # To be removed to enable module management by specific user groups
    cNombreTipoTRAModulo,                 
    cNombreTipoTRAColeccionCadenas,       
    cNombreTipoTRACadena,                 
    cNombreTipoTRATraduccion,             
    cNombreTipoTRAColeccionImportaciones, 
    cNombreTipoTRAImportacion, 
    cNombreTipoTRAContenidoIntercambio,   
    cNombreTipoTRAColeccionInformes,      
    cNombreTipoTRAInforme,                
]








# ##########################################################################
"""Types that shall acquire permissions : None
Permissions are obtained in each element by being explicitely granted to roles

"""
cTypesAcquiringPermissions = []









# ##########################################################################
""" Rules to control which Status changes are allowed for users in roles

"""


cStateChangeActionRoles = {
    cEstadoTraduccionPendiente: {
        cEstadoTraduccionPendiente:  None,
        cEstadoTraduccionTraducida:  [ cTRATranslator_role, cTRAReviewer_role, ] +  cUbiquitousWriterRoles,
        cEstadoTraduccionRevisada:   None,
        cEstadoTraduccionDefinitiva: None,
    },
    cEstadoTraduccionTraducida: {
        cEstadoTraduccionPendiente:  [ cTRATranslator_role, cTRAReviewer_role, ] +  cUbiquitousWriterRoles,
        cEstadoTraduccionTraducida:  [ cTRATranslator_role, cTRAReviewer_role, ] +  cUbiquitousWriterRoles,
        cEstadoTraduccionRevisada:   [ cTRAReviewer_role,    ] +  cUbiquitousWriterRoles,
        cEstadoTraduccionDefinitiva: None,
    },
    cEstadoTraduccionRevisada: {
        cEstadoTraduccionPendiente:  [ cTRAReviewer_role,    ] +  cUbiquitousWriterRoles,
        cEstadoTraduccionTraducida:  [ cTRAReviewer_role,    ] +  cUbiquitousWriterRoles,
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
     








# ##########################################################################
"""Use Cases

"""
 
cUseCase_VerifyTRACatalogo              = 'Verify_TRACatalogo'   
cUseCase_InitializeTRACatalogo          = 'Initialize_TRACatalogo'   
cUseCase_CreateMissingTRATraduccion     = 'Create_missing_TRATraduccion'   
cUseCase_ConfigureTRACatalogo           = 'Configure_TRACatalogo'   
cUseCase_CreateTRAImportacion           = 'Create_TRAImportacion'
cUseCase_DeleteTRAImportacion           = 'Delete_TRAImportacion'
cUseCase_CreateTRAContenidoIntercambio  = 'Create_TRAContenidoIntercambio'
cUseCase_DeleteTRAContenidoIntercambio  = 'Delete_TRAContenidoIntercambio'
cUseCase_ImportTRAImportacion           = 'Import_TRAImportacion'
cUseCase_Export                         = 'Export'
cUseCase_GenerateTRAInformeLanguages    = 'Generate_TRAInforme_by_Languages'
cUseCase_GenerateTRAInformeModules      = 'Generate_TRAInforme_by_Modules_and_Languages'
cUseCase_CreateAndDeleteTRAInformeInTRAImportacion = 'Generate_TRAInforme_before_and_after_import'
cUseCase_DeleteTRAInforme               = 'Delete_TRAInforme'
cUseCase_View                           = 'View_any_TRA_element'
cUseCase_AdvancedView                   = 'Advanced_View_on_any_TRA_element'
cUseCase_ListLanguagesAndModules        = 'List_Languages_And_Modules'
cUseCase_BrowseTranslations             = 'Browse_Translations'
cUseCase_TRATraduccionStateChange       = 'Change_TRATraduccion_State'
cUseCase_TRATraduccionComment           = 'Comment_on_TRATraduccion'
cUseCase_ReviewUsersAuthorizations      = 'Review_Users_Authorizations'
cUseCase_AuthorizeUsers                 = 'Authorize_Users'

                                                                
cTRAUseCaseNames = [
    cUseCase_VerifyTRACatalogo,
    cUseCase_InitializeTRACatalogo,  
    cUseCase_CreateMissingTRATraduccion,
    cUseCase_ConfigureTRACatalogo,
    cUseCase_CreateTRAImportacion,   
    cUseCase_DeleteTRAImportacion,
    cUseCase_CreateTRAContenidoIntercambio,
    cUseCase_DeleteTRAContenidoIntercambio,
    cUseCase_ImportTRAImportacion,         
    cUseCase_Export,                        
    cUseCase_GenerateTRAInformeLanguages,   
    cUseCase_GenerateTRAInformeModules,  
    cUseCase_CreateAndDeleteTRAInformeInTRAImportacion,
    cUseCase_View,
    cUseCase_AdvancedView,
    cUseCase_ListLanguagesAndModules,
    cUseCase_BrowseTranslations,
    cUseCase_TRATraduccionStateChange,      
    cUseCase_TRATraduccionComment,
]









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
]

cPreferredPermissionAbbreviations = [ unAbbrYPerm[ 0] for unAbbrYPerm in cPermissionsAndAbbreviations]
cPreferredPermissions             = [ unAbbrYPerm[ 1] for unAbbrYPerm in cPermissionsAndAbbreviations]

cPermissionsByAbbreviation = dict( cPermissionsAndAbbreviations)


cPermissionsAbbreviatedFor_ViewElement             = [   'VIE', 'ACI', ]

cPermissionsAbbreviatedFor_ViewElementAndChildren  = [   'VIE', 'ACI', 'LFC', ]











# ##########################################################################
"""Accessors used by their abbreviated name

"""

#cTraversalAccessorsSpecificacions = [
    #[ cAllTypes,        'catalogo',          'method',      'getCatalogo'],  
    #[ [ 'TRACatalogo',  'modulos', 'method', 'fObtenerTodosModulos', None, 'TRAModulo', [0, 'n'], ], # None is for no parameters
    
    #[ 'coleccionCadenas',           'TRACatalogo', 'method', 'fObtenerColeccionCadenas:TRAColeccionCadenas'],              
    #[ 'coleccionIdiomas',           'TRACatalogo', 'method', 'fObtenerColeccionIdiomas:TRAColeccionIdiomas'],              
    #[ 'coleccionModulos',           'TRACatalogo', 'method', 'fObtenerColeccionModulos:TRAColeccionModulos'],              
    #[ 'coleccionInformes',          'TRACatalogo', 'method', 'fObtenerColeccionInformes:TRAColeccionInformes'],              
    #[ 'coleccionImportaciones',     'TRACatalogo', 'method', 'fObtenerColeccionImportaciones:TRAColeccionImportaciones'],              
    #[ 'coleccionIdiomas',           'TRACatalogo', 'method', 'fObtenerColeccionIdiomas:TRAColeccionIdiomas'],              
    #[ 'modulos',                    'TRACatalogo', 'method', 'fObtenerModulos:TRAModulos'],              
    #[ 'informes',                   'TRACatalogo', 'method', 'fObtenerInformes:TRAInformes'],              
    #[ 'importaciones',              'TRACatalogo', 'method', 'fObtenerImportaciones:TRAImportaciones'],              
      
#]









# ##########################################################################
"""Use Case Driven security specificaction with Use cases, roles, types and required Plone permissions

"""

cTRAUseCasesWithAbbreviatedPermissions =  {
  'void_useCase_toImpose_View_And_ListFolderContents' : [ 
        [   {   'title':  'Objects without children can be viewed',
                'root':   cTodosNombresTiposWithoutChildren, 
                'path':   [ 'object',], 
                'types':  cTodosNombresTiposWithoutChildren,     
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement,                 
            },
            {   'title':  'Objects without children allow to view their children',
                'root':   cTodosNombresTiposWithChildren, 
                'path':   [ 'object',], 
                'types':  cTodosNombresTiposWithChildren,     
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
        ],
        [
             # extras go here like: [ [ 
                #cNombreTipoTRAColeccionCadenas]         ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF',  'MPC',  ],              [ cTRACoordinator_role,] +  cUbiquitousWriterRoles,],         
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
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, # ListFolderContents is not required for TRATraducion that will never have contents,but we force it set just in case Plone would throw out to login screen even managers, if hitting the tab contents, or even trying
            },
        ],  
        [
             # extras go here like: [ [ 
                #cNombreTipoTRAColeccionCadenas]         ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF',  'MPC',  ],              [ cTRACoordinator_role,] +  cUbiquitousWriterRoles,],         
        ],                                                                                           
    ],                                                                                                    
    'void_useCase_toImpose_ManageGroups_Permission' : [ 
        [   {   'path':   [ 'object', ],  
                'types':  cTodosNombresTipos,    
                'roles':  [ cTRAManager_role, ] +  cUbiquitousWriterRoles, 
                'perms':  [ 'MGR', ], 
            },
        ],  
        [
            # extras go here like: [ [ 
                #cNombreTipoTRAColeccionCadenas]         ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF',  'MPC',  ],              [ cTRACoordinator_role,] +  cUbiquitousWriterRoles,],         
        ],                                                                                           
    ],                                                                                                  
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
                'roles':  [ cTRAManager_role,] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
        ],  
        [
            [ cTodosNombresTiposColecciones          ,cPermissionsAbbreviatedFor_ViewElementAndChildren ,      [ cTRAManager_role,] +  cUbiquitousReaderRoles,],         
        ],                                                                                           
    ],   
    cUseCase_ConfigureTRACatalogo : [ 
        [   {   'title':  'Es TRACatalogo',
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'MPC',], 
            },
        ],  
        [
            [ cTodosNombresTiposColecciones          ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'DOB', 'MPC', ],      [ cTRAManager_role,] +  cUbiquitousWriterRoles,],         
        ],                                                                                           
    ],   
    cUseCase_ReviewUsersAuthorizations : [ 
        [   {   'title':  'Es TRACatalogo',
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, ] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
        ],  
        [
            # [ cTodosNombresTiposColecciones          ,cPermissionsAbbreviatedFor_ViewElementAndChildren ,      [ cTRAManager_role,] +  cUbiquitousReaderRoles,],         
        ],                                                                                           
    ],   
    cUseCase_AuthorizeUsers : [ 
        [   {   'title':  'Es TRACatalogo',
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role, cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'MGR',], 
            },
        ],  
        [
            # [ cTodosNombresTiposColecciones          ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'DOB', 'MPC', ],      [ cTRAManager_role,] +  cUbiquitousWriterRoles,],         
        ],                                                                                           
    ],   
    cUseCase_InitializeTRACatalogo : [ 
        [   {   'title':  'Es TRACatalogo',
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'DOB', 'MPC','ADC','MGR',], 
            },
        ],  
        [
            [ cTodosNombresTiposColecciones          ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'DOB', 'MPC', ],      [ cTRAManager_role,] +  cUbiquitousWriterRoles,],         
        ],                                                                                           
    ],  
    cUseCase_CreateMissingTRATraduccion : [ 
        [   {   'title':  'Es TRAImportacion',
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRAImportacion,],    
                'roles':  [ cTRAManager_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC',], 
            },
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRAManager_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Accessible TRAColeccionCadenas',
                'path':   [ 'object', 'fObtenerColeccionCadenas', ],  
                'types':  [ cNombreTipoTRAColeccionCadenas,],    
                'roles':  [ cTRAManager_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Filtro TRAIdioma accesibles',
                'name':   'languages',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosIdiomas', ],  
                'types':  [ cNombreTipoTRAIdioma,],    
                'roles':  [ cTRAManager_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC', ], 
            },
            {   'title':  'Filtro TRAModulo accesibles',
                'name':   'modules',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosModulos', ],  
                'types':  [ cNombreTipoTRAModulo,],    
                'roles':  [ cTRAManager_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC', ], 
            },
        ],  
        [
            [ [ cNombreTipoTRACadena,]                  ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC', ],         [ cTRAManager_role,] +  cUbiquitousWriterRoles,],         
            [ [ cNombreTipoTRATraduccion,]              ,cPermissionsAbbreviatedFor_ViewElement + [                          'MPC', ],         [ cTRAManager_role,] +  cUbiquitousWriterRoles,],
       ],                                                                                           
    ],  
    cUseCase_CreateTRAImportacion: [ 
        [   {   'title':  'Es TRACatalogo o TRAColeccionImportaciones',
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRACatalogo, cNombreTipoTRAColeccionImportaciones],    
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Accessible TRAColeccionImportaciones desde TRACatalogo',
                'path':   [ 'object', 'getCatalogo','fObtenerColeccionImportaciones'],
                'types':  [ cNombreTipoTRAColeccionImportaciones,],     
                'roles':  [  cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC',  ],
            }, 
        ],  
        [         
            [ [ cNombreTipoTRAImportacion,]         ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'DOB', 'MPC',  ],  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles,],
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
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'MPC', 'DOB', ],
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
                'roles':  [  cTRACoordinator_role, cTRATranslator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC',  ],
            }, 
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role, cTRATranslator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            },
            {   'title':  'Accessible TRAColeccionImportaciones',
                'path':   [ 'object', 'getContenedor', ],
                'types':  [ cNombreTipoTRAColeccionImportaciones,],     
                'roles':  [  cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            }, 
        ],  
        [
            [ [ cNombreTipoTRAContenidoIntercambio,]   ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'MPC', ],  [ cTRACoordinator_role, cTRATranslator_role,] +  cUbiquitousWriterRoles,], 
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
            [ [ cNombreTipoTRAColeccionImportaciones,] ,cPermissionsAbbreviatedFor_ViewElementAndChildren,                                [ cTRACoordinator_role, cTRATranslator_role,] +  cUbiquitousWriterRoles,],
            [ [ cNombreTipoTRAContenidoIntercambio,]   ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'DOB', 'MPC',  ],  [ cTRACoordinator_role, cTRATranslator_role,] +  cUbiquitousWriterRoles,], 
        ],                                                                                           
    ],                                                                                                  
    cUseCase_ImportTRAImportacion: [ 
        [   {   'title':  'Es TRAImportacion',
                'path':   [ 'object', ],
                'types':  [ cNombreTipoTRAImportacion,],     
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
            {   'title':  'Without any TRAContenidoIntercambio or all Accessible',
                'mode':   cUseCaseRuleMode_EmptyOrAll,
                'path':   [ 'object', 'getContenido',],
                'types':  [ cNombreTipoTRAContenidoIntercambio,],     
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            }, 
            {   'title':  'Without TRAInforme before import or can be deleted',
                'mode':   cUseCaseRuleMode_EmptyOrAll,
                'path':   [ 'object', 'getInformeEstadoIdiomasAntes',],
                'types':  [ cNombreTipoTRAInforme,],     
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'DOB', 'MPC',],
            }, 
            {   'title':  'Without TRAInforme after import or can be deleted',
                'mode':   cUseCaseRuleMode_EmptyOrAll,
                'path':   [ 'object', 'getInformeEstadoIdiomasDespues',],
                'types':  [ cNombreTipoTRAInforme,],     
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'DOB', 'MPC',],
            }, 
            {   'title':  'Accessible TRAColeccionImportaciones',
                'path':   [ 'object', 'getContenedor', ],
                'types':  [ cNombreTipoTRAColeccionImportaciones,],     
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,
            }, 
            {   'title':  'Accessible TRAColeccionCadenas',
                'path':   [ 'object', 'getCatalogo', 'fObtenerColeccionCadenas', ],  
                'types':  [ cNombreTipoTRAColeccionCadenas,],    
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC',], 
            },
            {   'title':  'Filtro TRAIdioma accesibles',
                'name':   'languages',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosIdiomas', ],  
                'types':  [ cNombreTipoTRAIdioma,],    
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC', ], 
            },
            {   'title':  'Filtro TRAModulo accesibles',
                'name':   'modules',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosModulos', ],  
                'types':  [ cNombreTipoTRAModulo,],    
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC', ], 
            },
        ],  
        [
            [ [ cNombreTipoTRACadena,
                cNombreTipoTRAInforme,]                 ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC', ],         [ cTRACoordinator_role,] +  cUbiquitousWriterRoles,],         
            [ [ cNombreTipoTRAInforme,]                 ,cPermissionsAbbreviatedFor_ViewElement + [        'APF',        'MPC', ],         [ cTRACoordinator_role,] +  cUbiquitousWriterRoles,],         
            [ [ cNombreTipoTRACadena,]                  ,cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC', ],         [ cTRACoordinator_role,] +  cUbiquitousWriterRoles,],         
            [ [ cNombreTipoTRATraduccion,]              ,cPermissionsAbbreviatedFor_ViewElement + [                      'MPC', ],         [ cTRACoordinator_role,] +  cUbiquitousWriterRoles,],
          ],                                                                                           
    ],                                                                                                  
    cUseCase_Export: [    
        [   {   'title':  'Es TRACatalogo',
                'path':   [ 'object',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Filter TRAIdioma todos los accesibles',
                'name':   'languages',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosIdiomas', ],  
                'types':  [ cNombreTipoTRAIdioma,],    
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Filter TRAModulo todos los accesibles',
                'name':   'modules',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosModulos', ],  
                'types':  [ cNombreTipoTRAModulo,],    
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
         ],  
        [
            [ [ cNombreTipoTRACadena]                    ,cPermissionsAbbreviatedFor_ViewElementAndChildren,     [ cTRACoordinator_role,] +  cUbiquitousReaderRoles,],         
            [ [ cNombreTipoTRATraduccion,]               ,cPermissionsAbbreviatedFor_ViewElement + [ ],          [ cTRACoordinator_role,] +  cUbiquitousReaderRoles,],
        ],                                                                                           
    ],                                                                                                  
    cUseCase_GenerateTRAInformeLanguages: [   
        [   {   'title':  'Si TRACatalogo',
                'root':   [ cNombreTipoTRACatalogo],
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren , 
            },
            {   'title':  'Si TRAColeccionInformes',
                'root':   [ cNombreTipoTRAColeccionInformes],
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRAColeccionInformes],    
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC',], 
            },
            {   'title':  'Accesible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Filtro TRAIdioma accesibles',
                'name':   'languages',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosIdiomas', ],  
                'types':  [ cNombreTipoTRAIdioma,],    
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] +  cUbiquitousReaderRoles,    
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
        ],  
        [
            [ [ cNombreTipoTRAInforme,]                  ,cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', 'DOB',],           [ cTRACoordinator_role] +  cUbiquitousReaderRoles,], 
            [ [ cNombreTipoTRACadena,]                   ,cPermissionsAbbreviatedFor_ViewElementAndChildren,                [ cTRACoordinator_role,] +  cUbiquitousReaderRoles,],         
            [ [ cNombreTipoTRATraduccion,]               ,cPermissionsAbbreviatedFor_ViewElement,                         [ cTRACoordinator_role,] +  cUbiquitousReaderRoles,], 
        ],                                                                                           
    ],                                                                                                  
    cUseCase_GenerateTRAInformeModules: [     
        [   {   'title':  'Si TRACatalogo',
                'root':   [ cNombreTipoTRACatalogo],
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren , 
            },
            {   'title':  'Si TRAColeccionInformes',
                'root':   [ cNombreTipoTRAColeccionInformes],
                'path':   [ 'object', ],  
                'types':  [ cNombreTipoTRAColeccionInformes],    
                'roles':  [ cTRACoordinator_role, ] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC',], 
            },
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Filtro TRAIdioma accesibles',
                'name':   'languages',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosIdiomas', ],  
                'types':  [ cNombreTipoTRAIdioma,],    
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Filtro TRAModulo accesibles',
                'name':   'modules',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosModulos', ],  
                'types':  [ cNombreTipoTRAModulo,],    
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
        ],  
        [
            [ [ cNombreTipoTRAInforme,]                  ,cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', 'DOB',],           [ cTRACoordinator_role] +  cUbiquitousReaderRoles,], 
            [ [ cNombreTipoTRACadena,]                   ,cPermissionsAbbreviatedFor_ViewElementAndChildren,                [ cTRACoordinator_role,] +  cUbiquitousReaderRoles,],         
            [ [ cNombreTipoTRATraduccion,]               ,cPermissionsAbbreviatedFor_ViewElement,                         [ cTRACoordinator_role,] +  cUbiquitousReaderRoles,], 
          ],                                                                                           
    ],                                                                                                                                                   
    cUseCase_CreateAndDeleteTRAInformeInTRAImportacion: [     
        [   {   'title':  'Es TRAImportacion',
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAImportacion,],    
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC'], 
            },
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',],  
                'types':  [ cNombreTipoTRACatalogo,],    
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Filter accessible TRAInforme',
                'name':   'informes',
                'mode':   cUseCaseRuleMode_Filter ,
                'path':   [ 'object', 'getInformesEstado',],  
                'types':  [ cNombreTipoTRAInforme,],    
                'roles':  [ cTRACoordinator_role,] +  cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'APC', 'APF', 'MPC','DOB',], 
            },
        ],  
        [
            [ [ cNombreTipoTRAInforme,]                  ,cPermissionsAbbreviatedFor_ViewElement + [ 'MPC', 'DOB',],           [ cTRACoordinator_role] +  cUbiquitousReaderRoles,], 
            [ [ cNombreTipoTRACadena,]                   ,cPermissionsAbbreviatedFor_ViewElementAndChildren,                [ cTRACoordinator_role,] +  cUbiquitousReaderRoles,],         
            [ [ cNombreTipoTRATraduccion,]               ,cPermissionsAbbreviatedFor_ViewElement,                         [ cTRACoordinator_role,] +  cUbiquitousReaderRoles,], 
          ],                                                                                           
    ],                                                                                                                                                   
    cUseCase_ListLanguagesAndModules: [                      
        [   
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',], 
                'types':  [ cNombreTipoTRACatalogo,],     
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role, cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'Filter TRAIdioma',
                'name':   'languages',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosIdiomas',],  
                'types':  [ cNombreTipoTRAIdioma,],    
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role, cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Filter TRAModulo',
                'name':   'modules',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosModulos', ],  
                'types':  [ cNombreTipoTRAModulo,],    
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role, cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
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
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'If TRACatalogo',
                'root':   [ cNombreTipoTRACatalogo,],
                'path':   [ 'object',], 
                'types':  [ cNombreTipoTRACatalogo,],     
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'If TRAColeccionIdiomas',
                'root':   [ cNombreTipoTRAColeccionIdiomas,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAColeccionIdiomas,],     
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'If TRAIdioma',
                'root':   [ cNombreTipoTRAIdioma,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAIdioma,],     
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'If TRAColeccionModulos',
                'root':   [ cNombreTipoTRAColeccionModulos,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAColeccionModulos,],     
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'If TRAModulo',
                'root':   [ cNombreTipoTRAModulo,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAModulo,],     
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'If TRAColeccionCadenas',
                'root':   [ cNombreTipoTRAColeccionCadenas,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAColeccionCadenas,],     
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'If TRACadena',
                'root':   [ cNombreTipoTRACadena,],
                'path':   [ 'object', ],   
                'types':  [ cNombreTipoTRACadena,],       
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,    
            },
            {   'title':  'If TRACadena accesible TRAColeccionCadenas',
                'root':   [ cNombreTipoTRACadena,],
                'path':   [ 'object', 'getContenedor',],   
                'types':  [ cNombreTipoTRAColeccionCadenas,],       
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,    
            },
            {   'title':  'If TRACadena accesible TRAColeccionCadenas desde TRACatalogo',
                'root':   [ cNombreTipoTRACadena,],
                'path':   [ 'object', 'getCatalogo', 'fObtenerColeccionCadenas', ],  
                'types':  [ cNombreTipoTRAColeccionCadenas,],    
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'If TRACadena Filter No TRAModulo or at least one accesible TRAModulo',
                'root':   [ cNombreTipoTRACadena,],
                'mode':   cUseCaseRuleMode_EmptyOrAny,
                'path':   [ 'object', 'getModulos',],   
                'types':  [ cNombreTipoTRAModulo,], 
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,    
            },
            {   'title':  'If TRATraduccion',
                'root':   [ cNombreTipoTRATraduccion,],
                'path':   [ 'object',],   
                'types':  [ cNombreTipoTRATraduccion,],       
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement,    
            },
            {   'title':  'If TRATraduccion accesible TRACadena',
                'root':   [ cNombreTipoTRATraduccion,],
                'path':   [ 'object', 'getContenedor',],   
                'types':  [ cNombreTipoTRACadena,],       
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,    
            },
            {   'title':  'If TRATraduccion accesible TRAColeccionCadenas',
                'root':   [ cNombreTipoTRATraduccion,],
                'path':   [ 'object', 'getContenedor','getContenedor',],   
                'types':  [ cNombreTipoTRAColeccionCadenas,],       
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,    
            },
            {   'title':  'If TRATraduccion accesible TRAColeccionCadenas desde TRACatalogo',
                'root':   [ cNombreTipoTRATraduccion,],
                'path':   [ 'object', 'getCatalogo', 'fObtenerColeccionCadenas', ],  
                'types':  [ cNombreTipoTRAColeccionCadenas,],    
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'If TRATraduccion Filter No TRAModulo or at least one accesible TRAModulo',
                'root':   [ cNombreTipoTRATraduccion,],
                'mode':   cUseCaseRuleMode_EmptyOrAny,
                'path':   [ 'object', 'getCadena', 'getModulos',],   
                'types':  [ cNombreTipoTRAModulo,], 
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,    
            }, 
            {   'title':  'If TRATraduccion accesible TRAIdioma',
                'root':   [ cNombreTipoTRATraduccion,],
                'path':   [ 'object', 'getIdioma',],   
                'types':  [ cNombreTipoTRAIdioma,],       
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,    
            },
            {   'title':  'If TRAColeccionImportaciones',
                'root':   [ cNombreTipoTRAColeccionImportaciones,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAColeccionImportaciones,],     
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'If TRAImportacion',
                'root':   [ cNombreTipoTRAImportacion,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAImportacion,],     
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'IF TRAImportacion accesible TRAColeccionImportaciones',
                'root':   [ cNombreTipoTRAImportacion,],
                'path':   [ 'object', 'getContenedor',],  
                'types':  [ cNombreTipoTRAColeccionImportaciones,],    
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'IF TRAImportacion accesible TRAColeccionImportaciones desde TRACatalogo',
                'root':   [ cNombreTipoTRAImportacion,],
                'path':   [ 'object', 'getCatalogo', 'fObtenerColeccionImportaciones', ],  
                'types':  [ cNombreTipoTRAColeccionImportaciones,],    
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'If TRAContenidoIntercambio',
                'root':   [ cNombreTipoTRAContenidoIntercambio,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAContenidoIntercambio,],     
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement,                 
            },
            {   'title':  'IF TRAContenidoIntercambio accesible TRAImportacion',
                'root':   [ cNombreTipoTRAContenidoIntercambio,],
                'path':   [ 'object', 'getContenedor',],  
                'types':  [ cNombreTipoTRAImportacion,],    
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'If TRAColeccionInformes',
                'root':   [ cNombreTipoTRAColeccionInformes,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAColeccionInformes,],     
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'If TRAInforme',
                'root':   [ cNombreTipoTRAInforme,],
                'path':   [ 'object', ], 
                'types':  [ cNombreTipoTRAInforme,],     
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElement,                 
            },
            {   'title':  'IF TRAInforme accesible TRAColeccionInformes',
                'root':   [ cNombreTipoTRAInforme,],
                'path':   [ 'object', 'getContenedor',],  
                'types':  [ cNombreTipoTRAColeccionInformes,],    
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'IF TRAInforme accesible TRAColeccionInformes desde TRACatalogo',
                'root':   [ cNombreTipoTRAInforme,],
                'path':   [ 'object', 'getCatalogo', 'fObtenerColeccionInformes', ],  
                'types':  [ cNombreTipoTRAColeccionInformes,],    
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,cTRAVisitor_role, ] + cUbiquitousReaderRoles, 
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
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role, cTRAVisitor_role, ] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,    
            },
            {   'title':  'Filtro TRAIdioma accesibles',
                'name':   'languages',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosIdiomas', ],  
                'types':  [ cNombreTipoTRAIdioma,],    
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role, cTRAVisitor_role, ] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
            {   'title':  'Filtro TRAModulo accesibles',
                'name':   'modules',
                'mode':   cUseCaseRuleMode_Filter,
                'path':   [ 'object', 'getCatalogo', 'fObtenerTodosModulos', ],  
                'types':  [ cNombreTipoTRAModulo,],    
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role, cTRAVisitor_role, ] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren, 
            },
        ],
        [
           #[ [ cNombreTipoTRAColeccionIdiomas,
               #cNombreTipoTRAColeccionModulos,
               #cNombreTipoTRAColeccionCadenas]           ,cPermissionsAbbreviatedFor_ViewElementAndChildren,                             [  cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,] +  cUbiquitousWriterRoles,],         
        ],                                                                                 
    ],                                                                                         
    cUseCase_TRATraduccionStateChange: [                     
        [   {   'title':  'Es TRATraduccion',
                'name':   'traduccion',
                'path':   [ 'object', ],   
                'types':  [ cNombreTipoTRATraduccion,],       
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',],    
            },
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',], 
                'types':  [ cNombreTipoTRACatalogo,],     
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,] + cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'Accessible TRACadena',
                'name':   'cadena',
                'path':   [ 'object', 'getCadena',],   
                'types':  [ cNombreTipoTRACadena,],       
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,    
            },
            {   'title':  'Accessible TRAIdioma',
                'name':   'idioma',
                'path':   [ 'object', 'getIdioma',],   
                'types':  [ cNombreTipoTRAIdioma,],       
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'MPC',],    
            },
            {   'title':  'TRACadena Without any TRAModulo or at least one accessible',
                'name':   'modulos',
                'mode':   cUseCaseRuleMode_EmptyOrAny,
                'path':   [ 'object', 'getCadena','getModulos',],   
                'types':  [ cNombreTipoTRAModulo,], 
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'MPC',],    
            },
        ],
        [
           #[ [ cNombreTipoTRAColeccionIdiomas,
               #cNombreTipoTRAColeccionModulos,
               #cNombreTipoTRAColeccionCadenas]           ,cPermissionsAbbreviatedFor_ViewElementAndChildren,                             [  cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,] +  cUbiquitousWriterRoles,],         
        ],                                                                                 
    ],                                                                                         
    cUseCase_TRATraduccionComment: [                     
        [   {   'title':  'Es TRATraduccion',
                'name':   'traduccion',
                'path':   [ 'object', ],   
                'types':  [ cNombreTipoTRATraduccion,],       
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElement + [ 'MPC',],    
            },
            {   'title':  'Accessible TRACatalogo',
                'name':   'catalogo',
                'path':   [ 'object', 'getCatalogo',], 
                'types':  [ cNombreTipoTRACatalogo,],     
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,] + cUbiquitousWriterRoles, 
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,                 
            },
            {   'title':  'Accessible TRACadena',
                'name':   'cadena',
                'path':   [ 'object', 'getCadena',],   
                'types':  [ cNombreTipoTRACadena,],       
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren,    
            },
            {   'title':  'Accessible TRAIdioma',
                'name':   'idioma',
                'path':   [ 'object', 'getIdioma',],   
                'types':  [ cNombreTipoTRAIdioma,],       
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'MPC',],    
            },
            {   'title':  'TRACadena Without any TRAModulo or at least one accessible',
                'name':   'modulos',
                'mode':   cUseCaseRuleMode_EmptyOrAny,
                'path':   [ 'object', 'getCadena','getModulos',],   
                'types':  [ cNombreTipoTRAModulo,], 
                'roles':  [ cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,] + cUbiquitousWriterRoles,
                'perms':  cPermissionsAbbreviatedFor_ViewElementAndChildren + [ 'MPC',],    
            },
        ],
        [
           #[ [ cNombreTipoTRAColeccionIdiomas,
               #cNombreTipoTRAColeccionModulos,
               #cNombreTipoTRAColeccionCadenas]           ,cPermissionsAbbreviatedFor_ViewElementAndChildren,                             [  cTRACoordinator_role, cTRAReviewer_role, cTRATranslator_role,] +  cUbiquitousWriterRoles,],         
        ],                                                                                 
    ],                                                                                         
}


cTRAUseCasesWithAbbreviatedPermissions[ cUseCase_AdvancedView] = cTRAUseCasesWithAbbreviatedPermissions[ cUseCase_View][:]











    
    

