# -*- coding: utf-8 -*-
#
# File: TRAElemento_Permission_Definitions.py
#
# Copyright (c) 2008, 2009, 2010, 2011  by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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

from TRAElemento_Constants                 import *
from TRAElemento_Constants_Activity        import *
from TRAElemento_Constants_Configurations  import *
from TRAElemento_Constants_Dates           import *
from TRAElemento_Constants_Encoding        import *
from TRAElemento_Constants_Import          import *
from TRAElemento_Constants_Languages       import *
from TRAElemento_Constants_Logging         import *
from TRAElemento_Constants_Modules         import *
from TRAElemento_Constants_Profiling       import *
from TRAElemento_Constants_Progress        import *
from TRAElemento_Constants_String          import *
from TRAElemento_Constants_StringRequests  import *
from TRAElemento_Constants_Translate       import *
from TRAElemento_Constants_Translation     import *
from TRAElemento_Constants_TypeNames       import *
from TRAElemento_Constants_Views           import *
from TRAElemento_Constants_Vocabularies    import *
from TRAUtils                              import *





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
    [   'ACI', perm_AccessContentsInformation,],
    [   'APC', permissions.AddPortalContent,],  
    [   'APF', permissions.AddPortalFolders,],  
    [   'CHP', permissions.ChangePermissions,],
    [   'DOB', permissions.DeleteObjects,],     
    [   'LFC', permissions.ListFolderContents,],
    [   'MGR', perm_ManageGroups, ],
    [   'MPR', permissions.ManageProperties,], 
    [   'MPC', permissions.ModifyPortalContent,],
    [   'VIE', permissions.View,],              
    [   'ADC', cPermission_gvSIGi18nAddTRACatalogo,],
]

cPreferredPermissionAbbreviations = [ unAbbrYPerm[ 0] for unAbbrYPerm in cPermissionsAndAbbreviations]
cPreferredPermissions             = [ unAbbrYPerm[ 1] for unAbbrYPerm in cPermissionsAndAbbreviations]



cPermissionsToReset = [ unAbbrYPerm[ 1] for unAbbrYPerm in cPermissionsAndAbbreviations[1:]]



cPermissionsByAbbreviation = dict( cPermissionsAndAbbreviations)


cPermissionsAbbreviatedFor_ViewElement             = [   'VIE', 'ACI', ]

cPermissionsAbbreviatedFor_ViewElementAndChildren  = [   'VIE', 'ACI', 'LFC', ]







# ##########################################################################
"""Classification of roles into a subset of role kinds, for the cache to figure out whther to serve a cached page generic for the role kind, or specific to the user.

"""


cTRAApplicationRolesAndRoleKinds = [
    [ [ 'Manager', ],           cRoleKind_UserSpecific],
    [ [ 'Owner', ],             cRoleKind_UserSpecific],
    [ [ cTRACreator_role, ],    cRoleKind_UserSpecific],
    [ [ cTRAManager_role, ],    cRoleKind_UserSpecific],
    [ [ cTRACoordinator_role,], cRoleKind_UserSpecific],
    [ [ cTRADeveloper_role,],   cRoleKind_UserSpecific],
    [ [ cTRAReviewer_role, ],   cRoleKind_UserSpecific],
    [ [ cTRATranslator_role, ], cRoleKind_UserSpecific],
    [ [ cTRAVisitor_role,],     cRoleKind_UserSpecific],
]









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

cTRAUbiquitousWriterRoles = [ cTRACreator_role, cTRAManager_role,]
cTRAUbiquitousReaderRoles = cTRAUbiquitousWriterRoles

cTRAManagerRoles          = [ cTRAManager_role,]

cPreferredRolesOrder   = cZopeRoles_list + TRARoles_list









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
    cNombreTipoTRAContenidoXML,
    cNombreTipoTRAColeccionInformes,      
    cNombreTipoTRAInforme,      
    cNombreTipoTRAColeccionSolicitudesCadenas,
    cNombreTipoTRASolicitudCadena,
    cNombreTipoTRAColeccionProgresos,      
    cNombreTipoTRAProgreso,   
    cNombreTipoTRAColeccionContribuciones,
    cNombreTipoTRAContribuciones,
    cNombreTipoTRAParametrosControlProgreso,
    cNombreTipoTRAConfiguracionImportacion,
    cNombreTipoTRAConfiguracionExportacion,
    cNombreTipoTRAConfiguracionSolicitudesCadenas,
    cNombreTipoTRAConfiguracionInvalidacionInformes,
    cNombreTipoTRAConfiguracionPaginaTraducciones,
    cNombreTipoTRAConfiguracionPerfilEjecucion,
    cNombreTipoTRAConfiguracionVarios,
    cNombreTipoTRAConfiguracionPermisos,
    cNombreTipoTRASimbolosOrdenados,    
]









# ##########################################################################
""" Rules to control which Status changes are allowed for users in roles

"""


cStateChangeActionRoles = {
    cEstadoTraduccionPendiente: {
        cEstadoTraduccionPendiente:  None,
        cEstadoTraduccionTraducida:  [ cTRATranslator_role, cTRAReviewer_role,  cTRACoordinator_role,] +  cTRAUbiquitousWriterRoles,
        cEstadoTraduccionRevisada:   None,
        cEstadoTraduccionDefinitiva: None,
    },
    cEstadoTraduccionTraducida: {
        cEstadoTraduccionPendiente:  [ cTRATranslator_role, cTRAReviewer_role,  cTRACoordinator_role,] +  cTRAUbiquitousWriterRoles,
        cEstadoTraduccionTraducida:  [ cTRATranslator_role, cTRAReviewer_role,  cTRACoordinator_role,] +  cTRAUbiquitousWriterRoles,
        cEstadoTraduccionRevisada:   [ cTRAReviewer_role,  cTRACoordinator_role,   ] +  cTRAUbiquitousWriterRoles,
        cEstadoTraduccionDefinitiva: None,
    },
    cEstadoTraduccionRevisada: {
        cEstadoTraduccionPendiente:  [ cTRAReviewer_role,  cTRACoordinator_role, ] +  cTRAUbiquitousWriterRoles,
        cEstadoTraduccionTraducida:  [ cTRAReviewer_role,  cTRACoordinator_role, ] +  cTRAUbiquitousWriterRoles,
        cEstadoTraduccionRevisada:   None,
        cEstadoTraduccionDefinitiva: [ cTRACoordinator_role, ] +  cTRAUbiquitousWriterRoles,
    },
    cEstadoTraduccionDefinitiva: {
        cEstadoTraduccionPendiente:  [ cTRACoordinator_role, ] +  cTRAUbiquitousWriterRoles,
        cEstadoTraduccionTraducida:  [ cTRACoordinator_role, ] +  cTRAUbiquitousWriterRoles,
        cEstadoTraduccionRevisada:   [ cTRACoordinator_role, ] +  cTRAUbiquitousWriterRoles,
        cEstadoTraduccionDefinitiva: None,
    },
}    
     


cInvalidateStringTranslationsRoles = [ cTRACoordinator_role, cTRADeveloper_role, ] +  cTRAUbiquitousWriterRoles


cDeactivateStringsRoles            = [ cTRACoordinator_role, ] +  cTRAUbiquitousWriterRoles
cActivateStringsRoles              = cDeactivateStringsRoles

cChangeStringsModulesRoles         = [ cTRACoordinator_role, cTRADeveloper_role,] +  cTRAUbiquitousWriterRoles
cRemoveStringsModulesRoles         = [ cTRACoordinator_role,] +  cTRAUbiquitousWriterRoles




# ##########################################################################
"""Types that shall acquire permissions : None
Permissions are obtained in each element by being explicitely granted to roles

"""
cTypesAcquiringPermissions = []
























    
    

