# -*- coding: utf-8 -*-
#
# File: TRACatalogo_Inicializacion_Constants.py
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
#

__author__ = """Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana <gvSIGi18n@gvSIG.org>, 
Model Driven Development sl <gvSIGi18n@ModelDD.org>, 
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo

##code-section module-header #fill in your manual code here


from Products.CMFCore               import permissions

from Products.CMFCore.utils         import SimpleRecord



from Products.PluggableAuthService.permissions import ManageGroups                  as perm_ManageGroups
from AccessControl.Permissions                 import access_contents_information   as perm_AccessContentsInformation
from AccessControl.Permissions                 import copy_or_move                  as perm_CopyOrMove


from Products.gvSIGi18nTool.TRAgvSIGi18nTool_Constants import cTRAgvSIGi18nToolId


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

from TRAImportarExportar_Constants                import *
from TRAImportarExportar_Constants_Encodings      import *
from TRAImportarExportar_Constants_GNUgettextPO   import *
from TRAImportarExportar_Constants_JavaProperties import *


from TRAElemento_Permission_Definitions import cPermission_gvSIGi18nAddTRACatalogo


from TRARoles       import *



##/code-section module-header

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema


##code-section after-schema #fill in your manual code here




# #######################################
"""Configured default values for Various Configuration 

"""
cMaximoNumeroCambiosRecientes   = 5000
cSegundosParaConfirmarAccion    = 120



cTRAInstallPath_PortalSkinsCustom = [ 'portal_skins', 'custom',]



# #############################################################
"""Control what to verify and initialize.

"""
cInitializeAllow_CreateExternalMethod       = True
cInitializeAllow_CreateCollections          = True
cInitializeAllow_CreateSingletons           = True
cInitializeAllow_CreateCatalogs             = True
cInitializeAllow_CreateIndexes              = True
cInitializeAllow_CreateLexicons             = True    
cInitializeAllow_CreateSchemaFields         = True
cInitializeAllow_CreateUserGroups           = True
cInitializeAllow_CreateSetLocalRoles        = True
cInitializeAllow_CreateSetAcquireRoleAssignments = True
cInitializeAllow_AddGroupToGroup            = True
cInitializeAllow_AddSchemaFields            = True



cTRACatalogoInitialPermissions = {
    perm_AccessContentsInformation: {
        'acquire_permissions':    False,
        'roles':    [ cTRACreator_role,],
                
    },
    permissions.AddPortalContent: {
        'acquire_permissions':    False,
        'roles':    [ cTRACreator_role,],
                
    },
    permissions.AddPortalFolders: {
        'acquire_permissions':    False,
        'roles':    [ cTRACreator_role,],
                
    },
    permissions.ChangePermissions: {
        'acquire_permissions':    False,
        'roles':    [ cTRACreator_role,],
                
    },
    permissions.DeleteObjects: {
        'acquire_permissions':    False,
        'roles':    [ cTRACreator_role,],
                
    },
    permissions.ListFolderContents: {
        'acquire_permissions':    False,
        'roles':    [ cTRACreator_role,],
                
    },
    perm_ManageGroups: {
        'acquire_permissions':    False,
        'roles':    [ cTRACreator_role,],
                
    },
    permissions.ManageProperties: {
        'acquire_permissions':    False,
        'roles':    [ cTRACreator_role,],
                
    },
    permissions.ModifyPortalContent: {
        'acquire_permissions':    False,
        'roles':    [ cTRACreator_role,],
                
    },
    permissions.View: {
        'acquire_permissions':    False,
        'roles':    [ cTRACreator_role,],
                
    },
    cPermission_gvSIGi18nAddTRACatalogo: {
        'acquire_permissions':    False,
        'roles':    [ cTRACreator_role,],
                
    },
}





# #############################################################
"""Specification of the collection elements to create under the root catalog.

"""
cColeccionCadenas_Id    = "cadenas"
cColeccionCadenas_Title = "Strings"
cColeccionIdiomas_Id    = "idiomas"
cColeccionIdiomas_Title = "Languages"
cColeccionModulos_Id    = "modulos"
cColeccionModulos_Title = "Modules"
cColeccionInformes_Id   = "informes"
cColeccionInformes_Title= "Reports"
cColeccionImportaciones_Id    = "importaciones"
cColeccionImportaciones_Title = "Imports"
cColeccionSolicitudesCadenas_Id    = "solicitudescadenas"
cColeccionSolicitudesCadenas_Title = "String Requests"
cColeccionProgresos_Id   = "progresos"
cColeccionProgresos_Title= "Progresses"

cTRAEspecificacionesColecciones = [ 
    [ cNombreTipoTRAColeccionIdiomas,              cColeccionIdiomas_Id,       cColeccionIdiomas_Title, ],
    [ cNombreTipoTRAColeccionModulos,              cColeccionModulos_Id,       cColeccionModulos_Title, ],
    [ cNombreTipoTRAColeccionCadenas,              cColeccionCadenas_Id,       cColeccionCadenas_Title, ],
    [ cNombreTipoTRAColeccionImportaciones,        cColeccionImportaciones_Id, cColeccionImportaciones_Title, ],
    [ cNombreTipoTRAColeccionInformes,             cColeccionInformes_Id,      cColeccionInformes_Title, ],
    [ cNombreTipoTRAColeccionSolicitudesCadenas,   cColeccionSolicitudesCadenas_Id,      cColeccionSolicitudesCadenas_Title, ],
    [ cNombreTipoTRAColeccionProgresos,            cColeccionProgresos_Id,      cColeccionProgresos_Title, ],
]






# #############################################################
"""Specification of the singleton elements to create under the root catalog.

"""

cTRAEspecificacionesEarlySingletons = [ 
    [ cNombreTipoTRAConfiguracionPermisos,               cTRAConfiguracion_Permisos_Id,               cTRAConfiguracion_Permisos_Title, 
        {   'aspectoConfiguracion':                                    cTRAConfiguracionAspecto_Permisos,
            
            'esAnonymousTRAManager':                                   cTRABooleanNo,
            'esAnonymousTRACoordinator':                               cTRABooleanNo,
            'esAnonymousTRADeveloper':                                 cTRABooleanNo,
            'esAnonymousTRAReviewer':                                  cTRABooleanNo,
            'esAnonymousTRATranslator':                                cTRABooleanNo,
            'esAnonymousTRAVisitor':                                   cTRABooleanSi,
            
            'esAuthenticatedTRAManager':                               cTRABooleanNo,
            'esAuthenticatedTRACoordinator':                           cTRABooleanNo,
            'esAuthenticatedTRADeveloper':                             cTRABooleanNo,
            'esAuthenticatedTRAReviewer':                              cTRABooleanNo,
            'esAuthenticatedTRATranslator':                            cTRABooleanNo,
            'esAuthenticatedTRAVisitor':                               cTRABooleanSi,
            
            'esMemberTRAManager':                                      cTRABooleanNo,
            'esMemberTRACoordinator':                                  cTRABooleanNo,
            'esMemberTRADeveloper':                                    cTRABooleanNo,
            'esMemberTRAReviewer':                                     cTRABooleanNo,
            'esMemberTRATranslator':                                   cTRABooleanNo,
            'esMemberTRAVisitor':                                      cTRABooleanSi,
            
            'esReviewerTRAManager':                                    cTRABooleanNo,
            'esReviewerTRACoordinator':                                cTRABooleanNo,
            'esReviewerTRADeveloper':                                  cTRABooleanNo,
            'esReviewerTRAReviewer':                                   cTRABooleanNo,
            'esReviewerTRATranslator':                                 cTRABooleanNo,
            'esReviewerTRAVisitor':                                    cTRABooleanSi,
            
            'esOwnerTRAManager':                                       cTRABooleanSi,
            'esOwnerTRACoordinator':                                   cTRABooleanSi,
            'esOwnerTRADeveloper':                                     cTRABooleanSi,
            'esOwnerTRAReviewer':                                      cTRABooleanSi,
            'esOwnerTRATranslator':                                    cTRABooleanSi,
            'esOwnerTRAVisitor':                                       cTRABooleanSi,
            
            'esManagerTRAManager':                                     cTRABooleanSi,
            'esManagerTRACoordinator':                                 cTRABooleanSi,
            'esManagerTRADeveloper':                                   cTRABooleanSi,
            'esManagerTRAReviewer':                                    cTRABooleanSi,
            'esManagerTRATranslator':                                  cTRABooleanSi,
            'esManagerTRAVisitor':                                     cTRABooleanSi,
        },
    ],
]




cTRAEspecificacionesSingletons = [ 
    
    [ cNombreTipoTRASimbolosOrdenados,                 cTRASimbolosOrdenados_Id,                  cTRASimbolosOrdenados_Title, 
        {  
        },
    ],
    
    
    [ cNombreTipoTRAParametrosControlProgreso, cTRAParametrosControlProgreso_Verificar_Id,           cTRAParametrosControlProgreso_Verificar_Title, 
        {   'tipoProceso':                                    cTRAProgress_ProcessType_Verify,
            'crearInformeAntes':                              False,
            'crearInformeDespues':                            False,
            'guardarResultados_habilitado':                   False,
            'guardarResultados_maximoMilisegundos':           0,
            'guardarResultados_maximoElementosLeidos':        0,
            'guardarResultados_maximoElementosModificados':   0,
            'transacciones_habilitado':                       False,
            'transacciones_maximoMilisegundos':               0,
            'transacciones_maximoElementosLeidos':            0,
            'transacciones_maximoElementosModificados':       0,
            'registro_habilitado':                            False,
            'registro_maximoMilisegundos':                    0,
            'registro_maximoElementosLeidos':                 0,
            'registro_maximoElementosModificados':            0,
            'registro_maximoTransacciones':                   0,
            'cederProcesador_habilitado':                     False,
            'cederProcesador_maximoMilisegundos':             0,
            'cederProcesador_maximoElementosLeidos':          0,
            'cederProcesador_maximoElementosModificados':     0,
            'cederProcesador_porcentajeTiempoActividad':      100,
        },
    ],
    [ cNombreTipoTRAParametrosControlProgreso, cTRAParametrosControlProgreso_Inicializar_Id,           cTRAParametrosControlProgreso_Inicializar_Title, 
        {   'tipoProceso':                                    cTRAProgress_ProcessType_Initialize,
            'crearInformeAntes':                              False,
            'crearInformeDespues':                            False,
            'guardarResultados_habilitado':                   False,
            'guardarResultados_maximoMilisegundos':           0,
            'guardarResultados_maximoElementosLeidos':        0,
            'guardarResultados_maximoElementosModificados':   0,
            'transacciones_habilitado':                       False,
            'transacciones_maximoMilisegundos':               0,
            'transacciones_maximoElementosLeidos':            0,
            'transacciones_maximoElementosModificados':       0,
            'registro_habilitado':                            False,
            'registro_maximoMilisegundos':                    0,
            'registro_maximoElementosLeidos':                 0,
            'registro_maximoElementosModificados':            0,
            'registro_maximoTransacciones':                   0,
            'cederProcesador_habilitado':                     False,
            'cederProcesador_maximoMilisegundos':             0,
            'cederProcesador_maximoElementosLeidos':          0,
            'cederProcesador_maximoElementosModificados':     0,
            'cederProcesador_porcentajeTiempoActividad':      100,
        },
    ],
    [ cNombreTipoTRAParametrosControlProgreso, cTRAParametrosControlProgreso_Inventario_Id,           cTRAParametrosControlProgreso_Inventario_Title, 
        {   'tipoProceso':                                    cTRAProgress_ProcessType_Inventory,
            'crearInformeAntes':                              False,
            'crearInformeDespues':                            False,
            'guardarResultados_habilitado':                   True,
            'guardarResultados_maximoMilisegundos':           60000,
            'guardarResultados_maximoElementosLeidos':        5000,
            'guardarResultados_maximoElementosModificados':   0,
            'transacciones_habilitado':                       True,
            'transacciones_maximoMilisegundos':               3000,
            'transacciones_maximoElementosLeidos':            5000,
            'transacciones_maximoElementosModificados':       0,
            'registro_habilitado':                            True,
            'registro_maximoMilisegundos':                    120000,
            'registro_maximoElementosLeidos':                 10000,
            'registro_maximoElementosModificados':            0,
            'registro_maximoTransacciones':                   10,
            'cederProcesador_habilitado':                     True,
            'cederProcesador_maximoMilisegundos':             1000,
            'cederProcesador_maximoElementosLeidos':          1000,
            'cederProcesador_maximoElementosModificados':     0,
            'cederProcesador_porcentajeTiempoActividad':      50,
        },
    ],
    [ cNombreTipoTRAParametrosControlProgreso, cTRAParametrosControlProgreso_Recatalogar_Id,          cTRAParametrosControlProgreso_Recatalogar_Title, 
        {   'tipoProceso':                                    cTRAProgress_ProcessType_ReCatalog,
            'crearInformeAntes':                              True,
            'crearInformeDespues':                            True,
            'guardarResultados_habilitado':                   True,
            'guardarResultados_maximoMilisegundos':           60000,
            'guardarResultados_maximoElementosLeidos':        5000,
            'guardarResultados_maximoElementosModificados':   5000,
            'transacciones_habilitado':                       True,
            'transacciones_maximoMilisegundos':               3000,
            'transacciones_maximoElementosLeidos':            5000,
            'transacciones_maximoElementosModificados':       5000,
            'registro_habilitado':                            True,
            'registro_maximoMilisegundos':                    120000,
            'registro_maximoElementosLeidos':                 10000,
            'registro_maximoElementosModificados':            10000,
            'registro_maximoTransacciones':                   10,
            'cederProcesador_habilitado':                     True,
            'cederProcesador_maximoMilisegundos':             1000,
            'cederProcesador_maximoElementosLeidos':          1000,
            'cederProcesador_maximoElementosModificados':     1000,
            'cederProcesador_porcentajeTiempoActividad':      50,
        },
    ],
    [ cNombreTipoTRAParametrosControlProgreso, cTRAParametrosControlProgreso_VerificarPermisos_Id,           cTRAParametrosControlProgreso_VerificarPermisos_Title, 
        {   'tipoProceso':                                    cTRAProgress_ProcessType_VerifyPermissions,
            'crearInformeAntes':                              False,
            'crearInformeDespues':                            False,
            'guardarResultados_habilitado':                   True,
            'guardarResultados_maximoMilisegundos':           60000,
            'guardarResultados_maximoElementosLeidos':        5000,
            'guardarResultados_maximoElementosModificados':   0,
            'transacciones_habilitado':                       True,
            'transacciones_maximoMilisegundos':               3000,
            'transacciones_maximoElementosLeidos':            5000,
            'transacciones_maximoElementosModificados':       0,
            'registro_habilitado':                            True,
            'registro_maximoMilisegundos':                    120000,
            'registro_maximoElementosLeidos':                 10000,
            'registro_maximoElementosModificados':            0,
            'registro_maximoTransacciones':                   10,
            'cederProcesador_habilitado':                     True,
            'cederProcesador_maximoMilisegundos':             1000,
            'cederProcesador_maximoElementosLeidos':          1000,
            'cederProcesador_maximoElementosModificados':     0,
            'cederProcesador_porcentajeTiempoActividad':      50,
        },
    ],
    [ cNombreTipoTRAParametrosControlProgreso, cTRAParametrosControlProgreso_ReestablecerPermisos_Id, cTRAParametrosControlProgreso_ReestablecerPermisos_Title, 
        {   'tipoProceso':                                    cTRAProgress_ProcessType_ResetPermissions,
            'crearInformeAntes':                              True,
            'crearInformeDespues':                            True,
            'guardarResultados_habilitado':                   True,
            'guardarResultados_maximoMilisegundos':           60000,
            'guardarResultados_maximoElementosLeidos':        5000,
            'guardarResultados_maximoElementosModificados':   5000,
            'transacciones_habilitado':                       True,
            'transacciones_maximoMilisegundos':               3000,
            'transacciones_maximoElementosLeidos':            5000,
            'transacciones_maximoElementosModificados':       5000,
            'registro_habilitado':                            True,
            'registro_maximoMilisegundos':                    120000,
            'registro_maximoElementosLeidos':                 10000,
            'registro_maximoElementosModificados':            10000,
            'registro_maximoTransacciones':                   10,
            'cederProcesador_habilitado':                     True,
            'cederProcesador_maximoMilisegundos':             1000,
            'cederProcesador_maximoElementosLeidos':          1000,
            'cederProcesador_maximoElementosModificados':     1000,
            'cederProcesador_porcentajeTiempoActividad':      50,
        },
    ],
    [ cNombreTipoTRAParametrosControlProgreso, cTRAParametrosControlProgreso_DeleteModule_Id,         cTRAParametrosControlProgreso_DeleteModule_Title, 
        {   'tipoProceso':                                    cTRAProgress_ProcessType_DeleteModule,
            'crearInformeAntes':                              True,
            'crearInformeDespues':                            True,
            'guardarResultados_habilitado':                   True,
            'guardarResultados_maximoMilisegundos':           60000,
            'guardarResultados_maximoElementosLeidos':        5000,
            'guardarResultados_maximoElementosModificados':   5000,
            'transacciones_habilitado':                       True,
            'transacciones_maximoMilisegundos':               3000,
            'transacciones_maximoElementosLeidos':            5000,
            'transacciones_maximoElementosModificados':       5000,
            'registro_habilitado':                            True,
            'registro_maximoMilisegundos':                    120000,
            'registro_maximoElementosLeidos':                 10000,
            'registro_maximoElementosModificados':            10000,
            'registro_maximoTransacciones':                   10,
            'cederProcesador_habilitado':                     True,
            'cederProcesador_maximoMilisegundos':             1000,
            'cederProcesador_maximoElementosLeidos':          1000,
            'cederProcesador_maximoElementosModificados':     1000,
            'cederProcesador_porcentajeTiempoActividad':      50,
        },
    ],
    [ cNombreTipoTRAParametrosControlProgreso, cTRAParametrosControlProgreso_RenameModule_Id,         cTRAParametrosControlProgreso_RenameModule_Title, 
        {   'tipoProceso':                                    cTRAProgress_ProcessType_RenameModule,
            'crearInformeAntes':                              True,
            'crearInformeDespues':                            True,
            'guardarResultados_habilitado':                   True,
            'guardarResultados_maximoMilisegundos':           60000,
            'guardarResultados_maximoElementosLeidos':        5000,
            'guardarResultados_maximoElementosModificados':   5000,
            'transacciones_habilitado':                       True,
            'transacciones_maximoMilisegundos':               3000,
            'transacciones_maximoElementosLeidos':            5000,
            'transacciones_maximoElementosModificados':       5000,
            'registro_habilitado':                            True,
            'registro_maximoMilisegundos':                    120000,
            'registro_maximoElementosLeidos':                 10000,
            'registro_maximoElementosModificados':            10000,
            'registro_maximoTransacciones':                   10,
            'cederProcesador_habilitado':                     True,
            'cederProcesador_maximoMilisegundos':             1000,
            'cederProcesador_maximoElementosLeidos':          1000,
            'cederProcesador_maximoElementosModificados':     1000,
            'cederProcesador_porcentajeTiempoActividad':      50,
        },
    ],
    [ cNombreTipoTRAParametrosControlProgreso, cTRAParametrosControlProgreso_DeleteLanguage_Id,       cTRAParametrosControlProgreso_DeleteLanguage_Title, 
        {   'tipoProceso':                                    cTRAProgress_ProcessType_DeleteLanguage,
            'crearInformeAntes':                              True,
            'crearInformeDespues':                            True,
            'guardarResultados_habilitado':                   True,
            'guardarResultados_maximoMilisegundos':           60000,
            'guardarResultados_maximoElementosLeidos':        5000,
            'guardarResultados_maximoElementosModificados':   5000,
            'transacciones_habilitado':                       True,
            'transacciones_maximoMilisegundos':               3000,
            'transacciones_maximoElementosLeidos':            5000,
            'transacciones_maximoElementosModificados':       5000,
            'registro_habilitado':                            True,
            'registro_maximoMilisegundos':                    120000,
            'registro_maximoElementosLeidos':                 10000,
            'registro_maximoElementosModificados':            10000,
            'registro_maximoTransacciones':                   10,
            'cederProcesador_habilitado':                     True,
            'cederProcesador_maximoMilisegundos':             1000,
            'cederProcesador_maximoElementosLeidos':          1000,
            'cederProcesador_maximoElementosModificados':     1000,
            'cederProcesador_porcentajeTiempoActividad':      50,
        },
    ],
    [ cNombreTipoTRAParametrosControlProgreso, cTRAParametrosControlProgreso_Backup_Id,               cTRAParametrosControlProgreso_Backup_Title, 
        {   'tipoProceso':                                    cTRAProgress_ProcessType_Backup,
            'crearInformeAntes':                              True,
            'crearInformeDespues':                            False,
            'guardarResultados_habilitado':                   True,
            'guardarResultados_maximoMilisegundos':           60000,
            'guardarResultados_maximoElementosLeidos':        5000,
            'guardarResultados_maximoElementosModificados':   0,
            'transacciones_habilitado':                       True,
            'transacciones_maximoMilisegundos':               3000,
            'transacciones_maximoElementosLeidos':            5000,
            'transacciones_maximoElementosModificados':       0,
            'registro_habilitado':                            True,
            'registro_maximoMilisegundos':                    120000,
            'registro_maximoElementosLeidos':                 10000,
            'registro_maximoElementosModificados':            0,
            'registro_maximoTransacciones':                   10,
            'cederProcesador_habilitado':                     True,
            'cederProcesador_maximoMilisegundos':             1000,
            'cederProcesador_maximoElementosLeidos':          1000,
            'cederProcesador_maximoElementosModificados':     0,
            'cederProcesador_porcentajeTiempoActividad':      50,
        },
    ],
    [ cNombreTipoTRAParametrosControlProgreso, cTRAParametrosControlProgreso_ExportGvSIG_Id,          cTRAParametrosControlProgreso_ExportGvSIG_Title, 
        {   'tipoProceso':                                    cTRAProgress_ProcessType_ExportGvSIG,
            'crearInformeAntes':                              True,
            'crearInformeDespues':                            False,
            'guardarResultados_habilitado':                   True,
            'guardarResultados_maximoMilisegundos':           60000,
            'guardarResultados_maximoElementosLeidos':        5000,
            'guardarResultados_maximoElementosModificados':   0,
            'transacciones_habilitado':                       True,
            'transacciones_maximoMilisegundos':               3000,
            'transacciones_maximoElementosLeidos':            5000,
            'transacciones_maximoElementosModificados':       0,
            'registro_habilitado':                            True,
            'registro_maximoMilisegundos':                    120000,
            'registro_maximoElementosLeidos':                 10000,
            'registro_maximoElementosModificados':            0,
            'registro_maximoTransacciones':                   10,
            'cederProcesador_habilitado':                     True,
            'cederProcesador_maximoMilisegundos':             1000,
            'cederProcesador_maximoElementosLeidos':          1000,
            'cederProcesador_maximoElementosModificados':     0,
            'cederProcesador_porcentajeTiempoActividad':      50,
        },
    ],
    [ cNombreTipoTRAParametrosControlProgreso, cTRAParametrosControlProgreso_Export_Id,               cTRAParametrosControlProgreso_Export_Title, 
        {   'tipoProceso':                                    cTRAProgress_ProcessType_Export,
            'crearInformeAntes':                              True,
            'crearInformeDespues':                            False,
            'guardarResultados_habilitado':                   True,
            'guardarResultados_maximoMilisegundos':           60000,
            'guardarResultados_maximoElementosLeidos':        5000,
            'guardarResultados_maximoElementosModificados':   0,
            'transacciones_habilitado':                       True,
            'transacciones_maximoMilisegundos':               3000,
            'transacciones_maximoElementosLeidos':            5000,
            'transacciones_maximoElementosModificados':       0,
            'registro_habilitado':                            True,
            'registro_maximoMilisegundos':                    120000,
            'registro_maximoElementosLeidos':                 10000,
            'registro_maximoElementosModificados':            0,
            'registro_maximoTransacciones':                   10,
            'cederProcesador_habilitado':                     True,
            'cederProcesador_maximoMilisegundos':             1000,
            'cederProcesador_maximoElementosLeidos':          1000,
            'cederProcesador_maximoElementosModificados':     0,
            'cederProcesador_porcentajeTiempoActividad':      50,
        },
    ],
    [ cNombreTipoTRAParametrosControlProgreso, cTRAParametrosControlProgreso_Import_Id,               cTRAParametrosControlProgreso_Import_Title, 
        {   'tipoProceso':                                    cTRAProgress_ProcessType_Import,
            'crearInformeAntes':                              True,
            'crearInformeDespues':                            True,
            'guardarResultados_habilitado':                   True,
            'guardarResultados_maximoMilisegundos':           60000,
            'guardarResultados_maximoElementosLeidos':        1000,
            'guardarResultados_maximoElementosModificados':   1000,
            'transacciones_habilitado':                       True,
            'transacciones_maximoMilisegundos':               2000,
            'transacciones_maximoElementosLeidos':            1000,
            'transacciones_maximoElementosModificados':       1000,
            'registro_habilitado':                            True,
            'registro_maximoMilisegundos':                    60000,
            'registro_maximoElementosLeidos':                 1000,
            'registro_maximoElementosModificados':            1000,
            'registro_maximoTransacciones':                   10,
            'cederProcesador_habilitado':                     True,
            'cederProcesador_maximoMilisegundos':             1000,
            'cederProcesador_maximoElementosLeidos':          1000,
            'cederProcesador_maximoElementosModificados':     1000,
            'cederProcesador_porcentajeTiempoActividad':      50,
        },
    ],
    
    
    
    [ cNombreTipoTRAConfiguracionImportacion, cTRAConfiguracion_Importacion_Id,               cTRAConfiguracion_Importacion_Title, 
        {   'aspectoConfiguracion':                                     cTRAConfiguracionAspecto_Importacion,
            'nombreModuloPorDefecto':                                   cTRAModuleName_gvSIG,
            'codigoIdiomaPorDefecto':                                   cTRALanguageCode_English,
            'importarConNombreModuloConfiguradoPorDefecto':             True,
            'importarFuentesDesdeComentariosPorDefecto':                True,
            'importarNombreModuloDesdeDominioONombreFicheroPorDefecto': True,
            'importarNombresModulosDesdeComentariosPorDefecto':         True,
            'importarStatusDesdeComentariosPorDefecto':                 True,
            'importarContribucionesDesdeComentariosPorDefecto':         True,
            'segundosParaConfirmarImportacion':                         300,
            'numeroMaximoLineasAExplorar':                              100000,
            'importarXMLTRACatalogoPorDefecto':                         False,
            'importarXMLTRAConfiguracionesPorDefecto':                  False,
            'importarXMLTRAParametrosControlProgresoPorDefecto':        False,
            'importarXMLTRAParametrosControlProgresoPorDefecto':        False,
            'importarXMLTRAIdiomasPorDefecto':                          False,
            'importarXMLTRASolicitudesCadenasPorDefecto':               False,
            'importarXMLTRAModulosPorDefecto':                          False,
            'importarXMLTRAInformesPorDefecto':                         False,
        },
    ],
    [ cNombreTipoTRAConfiguracionImportacion, cTRAConfiguracion_Restore_Id,               cTRAConfiguracion_Restore_Title, 
        {   'aspectoConfiguracion':                                     cTRAConfiguracionAspecto_Recuperar,
            'nombreModuloPorDefecto':                                   '',
            'codigoIdiomaPorDefecto':                                   '',
            'importarConNombreModuloConfiguradoPorDefecto':             False,
            'importarFuentesDesdeComentariosPorDefecto':                True,
            'importarNombreModuloDesdeDominioONombreFicheroPorDefecto': False,
            'importarNombresModulosDesdeComentariosPorDefecto':         True,
            'importarStatusDesdeComentariosPorDefecto':                 True,
            'importarContribucionesDesdeComentariosPorDefecto':         True,
            'segundosParaConfirmarImportacion':                         300,
            'numeroMaximoLineasAExplorar':                              1000000,
            'importarXMLTRACatalogoPorDefecto':                         True,
            'importarXMLTRAConfiguracionesPorDefecto':                  True,
            'importarXMLTRAParametrosControlProgresoPorDefecto':        True,
            'importarXMLTRAParametrosControlProgresoPorDefecto':        True,
            'importarXMLTRAIdiomasPorDefecto':                          True,
            'importarXMLTRASolicitudesCadenasPorDefecto':               True,
            'importarXMLTRAModulosPorDefecto':                          True,
            'importarXMLTRAInformesPorDefecto':                         True,
        },
    ],
    [ cNombreTipoTRAConfiguracionExportacion, cTRAConfiguracion_Exportacion_Id,               cTRAConfiguracion_Exportacion_Title, 
        {   'aspectoConfiguracion':                                    cTRAConfiguracionAspecto_Exportacion,
            'codigoIdiomaPorDefecto':                                  cTRALanguageCode_English,
            'dominioPorDefecto':                                       cTRAADefaultDomainName,
            'exportarEstadoTraduccionesPorDefecto':                    cTRABooleanSi,
            'exportarFuentesPorDefecto':                               cTRABooleanSi,
            'exportarNombreFicheroParaGvSIGPorDefecto':                cTRABooleanNo,
            'exportarNombresModulosPorDefecto':                        cTRABooleanSi,
            'exportarContribucionesPorDefecto':                        cTRABooleanSi,
            'formatoExportacionPorDefecto':                            cExportFormatOption_JavaProperties,
            'incluirLocalesCSVPorDefecto':                             cTRABooleanSi,
            'incluirManifestPorDefecto':                               cTRABooleanNo,
            'modoGestionErrorCodificacionExportacionPorDefecto':       cTRAEncodingErrorHandleMode_BackslashReplaceAndContinue,
            'modulosPorSeparadoPorDefecto':                            cTRABooleanNo,
            'nombreModuloPorDefecto':                                  cTRAADefaultModuleName,
            'tipoArchivoExportacionPorDefecto':                        cZipFilePostfix,
            'exportarTRACatalogoPorDefecto':                           cTRABooleanNo,
            'exportarTRAConfiguracionesPorDefecto':                    cTRABooleanNo,
            'exportarTRAParametrosControlProgresoPorDefecto':          cTRABooleanNo,
            'exportarTRAIdiomasPorDefecto':                            cTRABooleanNo,
            'exportarTRASolicitudesCadenasPorDefecto':                 cTRABooleanNo,
            'exportarTRAModulosPorDefecto':                            cTRABooleanNo,
            'exportarTRAInformesPorDefecto':                           cTRABooleanNo,
        },
    ],
    [ cNombreTipoTRAConfiguracionExportacion, cTRAConfiguracion_ExportacionParaGvSIG_Id,               cTRAConfiguracion_ExportacionParaGvSIG_Title, 
        {   'aspectoConfiguracion':                                    cTRAConfiguracionAspecto_ExportarParaGvSIG,
            'codigoIdiomaPorDefecto':                                  cTRALanguageCode_English,
            'dominioPorDefecto':                                       cTRAADefaultDomainName,
            'exportarEstadoTraduccionesPorDefecto':                    cTRABooleanSi,
            'exportarFuentesPorDefecto':                               cTRABooleanSi,
            'exportarNombreFicheroParaGvSIGPorDefecto':                cTRABooleanSi,
            'exportarNombresModulosPorDefecto':                        cTRABooleanSi,
            'exportarContribucionesPorDefecto':                        cTRABooleanSi,
            'formatoExportacionPorDefecto':                            cExportFormatOption_JavaProperties,
            'incluirLocalesCSVPorDefecto':                             cTRABooleanSi,
            'incluirManifestPorDefecto':                               cTRABooleanNo,
            'modoGestionErrorCodificacionExportacionPorDefecto':       cTRAEncodingErrorHandleMode_BackslashReplaceAndContinue,
            'modulosPorSeparadoPorDefecto':                            cTRABooleanNo,
            'nombreModuloPorDefecto':                                  cTRAModuleName_gvSIG,
            'tipoArchivoExportacionPorDefecto':                        cZipFilePostfix,
            'exportarTRACatalogoPorDefecto':                           cTRABooleanNo,
            'exportarTRAConfiguracionesPorDefecto':                    cTRABooleanNo,
            'exportarTRAParametrosControlProgresoPorDefecto':          cTRABooleanNo,
            'exportarTRAIdiomasPorDefecto':                            cTRABooleanNo,
            'exportarTRASolicitudesCadenasPorDefecto':                 cTRABooleanNo,
            'exportarTRAModulosPorDefecto':                            cTRABooleanNo,
            'exportarTRAInformesPorDefecto':                           cTRABooleanNo,
        },
    ],
    [ cNombreTipoTRAConfiguracionExportacion, cTRAConfiguracion_Backup_Id,               cTRAConfiguracion_Backup_Title, 
        {   'aspectoConfiguracion':                                    cTRAConfiguracionAspecto_Backup,
            'codigoIdiomaPorDefecto':                                  cTRALanguageCode_English,
            'dominioPorDefecto':                                       cTRAADefaultDomainName,
            'exportarEstadoTraduccionesPorDefecto':                    cTRABooleanSi,
            'exportarFuentesPorDefecto':                               cTRABooleanSi,
            'exportarNombreFicheroParaGvSIGPorDefecto':                cTRABooleanNo,
            'exportarNombresModulosPorDefecto':                        cTRABooleanSi,
            'exportarContribucionesPorDefecto':                        cTRABooleanSi,
            'formatoExportacionPorDefecto':                            cExportFormatOption_JavaProperties,
            'incluirLocalesCSVPorDefecto':                             cTRABooleanSi,
            'incluirManifestPorDefecto':                               cTRABooleanNo,
            'modoGestionErrorCodificacionExportacionPorDefecto':       cTRAEncodingErrorHandleMode_BackslashReplaceAndContinue,
            'modulosPorSeparadoPorDefecto':                            cTRABooleanNo,
            'nombreModuloPorDefecto':                                  cTRAADefaultModuleName,
            'tipoArchivoExportacionPorDefecto':                        cZipFilePostfix,
            'exportarTRACatalogoPorDefecto':                           cTRABooleanSi,
            'exportarTRAConfiguracionesPorDefecto':                    cTRABooleanSi,
            'exportarTRAParametrosControlProgresoPorDefecto':          cTRABooleanSi,
            'exportarTRAIdiomasPorDefecto':                            cTRABooleanSi,
            'exportarTRASolicitudesCadenasPorDefecto':                 cTRABooleanSi,
            'exportarTRAModulosPorDefecto':                            cTRABooleanSi,
            'exportarTRAInformesPorDefecto':                           cTRABooleanSi,
        },
    ],
    [ cNombreTipoTRAConfiguracionSolicitudesCadenas, cTRAConfiguracion_SolicitudesCadenas_Id,               cTRAConfiguracion_SolicitudesCadenas_Title, 
        {   'aspectoConfiguracion':                                     cTRAConfiguracionAspecto_SolicitudesCadenas,
            'codigoIdiomaReferenciaSolicitudesNuevasCadenas':           'es',
            'codigoIdiomaRequeridoSolicitudesNuevasCadenas':            cTRALanguageCode_English,
        },
    ],
    [ cNombreTipoTRAConfiguracionAlmacenPaginas, cTRAConfiguracion_AlmacenPaginas_Id,               cTRAConfiguracion_AlmacenPaginas_Title, 
        {   'aspectoConfiguracion':                                    cTRAConfiguracionAspecto_AlmacenPaginas,
            'numeroDeActividadesAnularInformeActividad':               3,
            'numeroDeCambiosAnularInformeIdiomas':                     5,
            'numeroDeCambiosAnularInformeModulosEIdiomas':             20,
            'segundosMinimosRetencionInformeActividad':                60,
            'segundosMinimosRetencionInformeIdiomas':                  120,
            'segundosMinimosRetencionInformeModulosEIdiomas':          300,
        },
    ],
    [ cNombreTipoTRAConfiguracionPaginaTraducciones, cTRAConfiguracion_PaginaTraducciones_Id,               cTRAConfiguracion_PaginaTraducciones_Title, 
        {   'aspectoConfiguracion':                                    cTRAConfiguracionAspecto_PaginaTraducciones,
            'maximoRegistrosExplorados':                               cMaximoRegistrosExplorados,
            'modoInteraccionPorDefecto':                               cInteractionMode_Asynchronous,
            'traduccionesPorPaginaPorDefecto':                         cDefaultTraduccionesPorPagina,
        },
    ],
    [ cNombreTipoTRAConfiguracionPerfilEjecucion, cTRAConfiguracion_PerfilEjecucion_Id,               cTRAConfiguracion_PerfilEjecucion_Title, 
        {   'aspectoConfiguracion':                                    cTRAConfiguracionAspecto_PerfilEjecucion,
            'escrituraEnDiscoDeRegistroDeEjecucionDetalladoHabilitado':False,
            'escrituraEnDiscoDeRegistroDeEjecucionHabilitado':         False,
            'perfilDeEjecucionHabilitado':                             False,
            'presentacionEnPaginasDeRegistroDeEjecucionHabilitado':    False,
            'presentacionEnPaginasDeTiempoDeEjecucionHabilitado':      False,
            'registroRaizDeEjecucionAutomaticoHabilitado':             False,
            'tiemposDeEjecucionHabilitado':                            False,
        },
    ],
    [ cNombreTipoTRAConfiguracionVarios,               cTRAConfiguracion_Varios_Id,                   cTRAConfiguracion_Varios_Title, 
        {   'aspectoConfiguracion':                                    cTRAConfiguracionAspecto_Varios,
            'maximoNumeroCambiosRecientes':                            cMaximoNumeroCambiosRecientes,
            'segundosParaConfirmarAccion':                             cSegundosParaConfirmarAccion,
        },
    ],
]   










# #############################################################
"""Specification of ZCatalog instances specific to strings and translations.

"""
cNombreCatalogoBusquedaCadenas      = 'TRACadenaBusqueda'
cNombreCatalogoFiltroCadenas        = 'TRACadenaFiltro'
cNombreCatalogoTextoCadenas         = 'TRACadenaTexto'
cNombreCatalogoBusquedaTraducciones = 'TRATraduccionBusqueda'
cNombreCatalogoFiltroTraducciones   = 'TRATraduccionFiltro'
cNombreCatalogoTextoTraducciones    = 'TRATraduccionTexto'




cLanguagesWithSpecialLexiconPipelines = {
    'zh':  [ 'CJKSplitter', ],
    'ja':  [ 'CJKSplitter', ],
    'ko':  [ 'CJKSplitter', ],
    # cTRALanguageCode_English:  [ 'Splitter', 'CaseNormalizer', 'StopWordRemover', ],
}








cIndexesCatalogoBusquedaCadenas  = [ 
    [ 'getId',              'FieldIndex',  ],
    [ 'getSimbolo',         'FieldIndex',  ],
    [ 'getEstadoCadena',    'KeywordIndex',],
]


cSchemaFieldsCatalogoBusquedaCadenas  = [ aIdxSpec[ 0] for aIdxSpec in cIndexesCatalogoBusquedaCadenas]








cIndexesCatalogoFiltroCadenas  = cIndexesCatalogoBusquedaCadenas + [ 
    [ 'getFechaCreacionTextual',    'FieldIndex',   ],
    [ 'getUsuarioCreador',          'FieldIndex',  ],
    [ 'getFechaCancelacionTextual', 'FieldIndex',   ],
]


cSchemaFieldsCatalogoFiltroCadenas  = [ aIdxSpec[ 0] for aIdxSpec in cIndexesCatalogoFiltroCadenas] + \
                                    [ 'getNombresModulos',]





cIndexesCatalogoTextoCadenas  = [ 
    [ 'getSimbolo',    'ZCTextIndex',   SimpleRecord( lexicon_id='plaintext_lexicon' , index_type='Okapi BM25 Rank')],
]


cSchemaFieldsCatalogoTextoCadenas  = [ 'getId', 'getSimbolo',]

# ACV20110117 in support of solution to error reportado por Mario CArrera
#cLexiconsCatalogoTextoCadenas  = [ 
    #[ 'plaintext_lexicon', [ 'Splitter', 'CaseNormalizer', 'StopWordRemover', ], ],
#]

cLexiconsCatalogoTextoCadenas  = [ 
    [ 'plaintext_lexicon', [ 'TRASplitter', ], ],
]





cTRACatalogsDetailsParaCadenas = [
    {   'name':             cNombreCatalogoBusquedaCadenas,
        'indexes':          cIndexesCatalogoBusquedaCadenas,
        'schema_fields':    cSchemaFieldsCatalogoBusquedaCadenas,
        'lexicons':         [],
        },
    {   'name':             cNombreCatalogoFiltroCadenas,
        'indexes':          cIndexesCatalogoFiltroCadenas,
        'schema_fields':    cSchemaFieldsCatalogoFiltroCadenas,
        'lexicons':         [],
        },
    {   'name':             cNombreCatalogoTextoCadenas,
        'indexes':          cIndexesCatalogoTextoCadenas,
        'schema_fields':    cSchemaFieldsCatalogoTextoCadenas,
        'lexicons':         cLexiconsCatalogoTextoCadenas,
        },
]











cIndexesCatalogoBusquedaTraducciones  = [ 
    [ 'getId',                  'FieldIndex',  ],
    [ 'getSimbolo',             'FieldIndex',  ],
    [ 'getEstadoCadena',        'KeywordIndex',],
    [ 'getIdCadena',            'FieldIndex',  ],
    [ 'getEstadoTraduccion',    'KeywordIndex',],
]


cSchemaFieldsCatalogoBusquedaTraducciones  = [ 'getCodigoIdiomaEnGvSIG', ] + \
                                           [ aIdxSpec[ 0] for aIdxSpec in cIndexesCatalogoBusquedaTraducciones]






cIndexesCatalogoFiltroTraducciones  = cIndexesCatalogoBusquedaTraducciones + [ 
    [ 'getFechaCreacionTextual',        'FieldIndex',     ],
    [ 'getUsuarioCreador',              'FieldIndex',     ],
    [ 'getFechaTraduccionTextual',      'FieldIndex',     ],
    [ 'getUsuarioTraductor',            'FieldIndex',     ],
    [ 'getFechaRevisionTextual',        'FieldIndex',     ],
    [ 'getUsuarioRevisor',              'FieldIndex',     ],
    [ 'getFechaDefinitivoTextual',      'FieldIndex',     ],
    [ 'getUsuarioCoordinador',          'FieldIndex',     ],
    [ 'getFechaModificacionTextual',    'FieldIndex',     ],
    [ 'getUsuarioModificador',          'FieldIndex',     ],
]
cSchemaFieldsCatalogoFiltroTraducciones  = [ 'Type', 'getCodigoIdiomaEnGvSIG', ] + \
                                         [ aIdxSpec[ 0] for aIdxSpec in cIndexesCatalogoFiltroTraducciones] + \
                                         [ 'getCadenaTraducida', 'getComentario', 'getNombresModulos', 'getContadorCambios',]





cIndexesCatalogoTextoTraducciones  = [ 
    [ 'getCadenaTraducida',  'ZCTextIndex',   SimpleRecord( lexicon_id='plaintext_lexicon' , index_type='Okapi BM25 Rank')],
]
cSchemaFieldsCatalogoTextoTraducciones  = [ 'getId', 'getIdCadena', 'getSimbolo', 'getCodigoIdiomaEnGvSIG',]


cLexiconsCatalogoTextoTraducciones  = [ 
    [ 'plaintext_lexicon', [ 'TRASplitter', ], ],
]








cTRACatalogsDetailsParaIdioma = [
    {   'name':             cNombreCatalogoBusquedaTraducciones,
        'indexes':          cIndexesCatalogoBusquedaTraducciones,
        'schema_fields':    cSchemaFieldsCatalogoBusquedaTraducciones,
        'lexicons':         [],
        },
    {   'name':             cNombreCatalogoFiltroTraducciones,
        'indexes':          cIndexesCatalogoFiltroTraducciones,
        'schema_fields':    cSchemaFieldsCatalogoFiltroTraducciones,
        'lexicons':         [],
        },   
    {   'name':             cNombreCatalogoTextoTraducciones,
        'indexes':          cIndexesCatalogoTextoTraducciones,
        'schema_fields':    cSchemaFieldsCatalogoTextoTraducciones,
        'lexicons':         cLexiconsCatalogoTextoTraducciones,
        },   
]







# #############################################################
"""gvSIGi18n User Interface application initialization specification

"""
cTRAExtMethod_ChangeAndBrowseTranslations           = "TRAChangeAndBrowseTranslations"
cTRAExtMethod_SizesIdioma                           = "TRASizesIdioma"
cTRAExtModule_TRARenderSecurity                     = "TRARenderSecurity"
cTRAExtMethod_RenderPermissionDefinitions           = "TRARenderPermissionDefinitions"
cTRAExtMethod_RenderLoggedUsedAndRolesHere          = "TRARenderLoggedUsedHere"
cTRAExtMethod_RenderGroupsRolesHere                 = "TRARenderGroupsRolesHere"
cTRAExtModule_TRARenderProfiling                    = "TRARenderProfiling"
cTRAExtMethod_RenderExecutionDetails                = "TRARenderExecutionDetails"
cTRAExtMethod_ParametersCandidateValues             = "TRAExport_ParametersCandidateValues"
cTRAExtModule_TRAExport_ctrl                        = "TRAExport_ctrl"




cTRAUIInitializationDefinitions = {
    'title':             'application gvSIG-i18n User Interface',
    'external_methods':  [
        {
            'ext_method_module':         cTRAExtMethod_ChangeAndBrowseTranslations,
            'ext_method_function':       cTRAExtMethod_ChangeAndBrowseTranslations,
            'ext_method_id':             cTRAExtMethod_ChangeAndBrowseTranslations,
            'ext_method_title':          cTRAExtMethod_ChangeAndBrowseTranslations,
            'install_path':              cTRAInstallPath_PortalSkinsCustom,
            'required':                  True,
            },
        {
            'ext_method_module':         cTRAExtMethod_ChangeAndBrowseTranslations,
            'ext_method_function':       cTRAExtMethod_SizesIdioma,
            'ext_method_id':             cTRAExtMethod_SizesIdioma,
            'ext_method_title':          cTRAExtMethod_SizesIdioma,
            'install_path':              cTRAInstallPath_PortalSkinsCustom,
            'required':                  True,
            },
        {
            'ext_method_module':         cTRAExtModule_TRARenderSecurity,
            'ext_method_function':       cTRAExtMethod_RenderPermissionDefinitions,
            'ext_method_id':             cTRAExtMethod_RenderPermissionDefinitions,
            'ext_method_title':          cTRAExtMethod_RenderPermissionDefinitions,
            'install_path':              cTRAInstallPath_PortalSkinsCustom,
            'required':                  True,
            },
        {
            'ext_method_module':         cTRAExtModule_TRARenderSecurity,
            'ext_method_function':       cTRAExtMethod_RenderLoggedUsedAndRolesHere,
            'ext_method_id':             cTRAExtMethod_RenderLoggedUsedAndRolesHere,
            'ext_method_title':          cTRAExtMethod_RenderLoggedUsedAndRolesHere,
            'install_path':              cTRAInstallPath_PortalSkinsCustom,
            'required':                  True,
            },
        {
            'ext_method_module':         cTRAExtModule_TRARenderSecurity,
            'ext_method_function':       cTRAExtMethod_RenderGroupsRolesHere,
            'ext_method_id':             cTRAExtMethod_RenderGroupsRolesHere,
            'ext_method_title':          cTRAExtMethod_RenderGroupsRolesHere,
            'install_path':              cTRAInstallPath_PortalSkinsCustom,
            'required':                  True,
            },
        {
            'ext_method_module':         cTRAExtModule_TRARenderProfiling,
            'ext_method_function':       cTRAExtMethod_RenderExecutionDetails,
            'ext_method_id':             cTRAExtMethod_RenderExecutionDetails,
            'ext_method_title':          cTRAExtMethod_RenderExecutionDetails,
            'install_path':              cTRAInstallPath_PortalSkinsCustom,
            'required':                  True,
            },    
        {
            'ext_method_module':         cTRAExtModule_TRAExport_ctrl,
            'ext_method_function':       cTRAExtMethod_ParametersCandidateValues,
            'ext_method_id':             cTRAExtMethod_ParametersCandidateValues,
            'ext_method_title':          cTRAExtMethod_ParametersCandidateValues,
            'install_path':              cTRAInstallPath_PortalSkinsCustom,
            'required':                  True,
            },    
    ],
    'tool_singletons':   None,
}







# #############################################################
"""gvSIGi18n boundary Tool application initialization specification

"""
cTRAToolInitializationDefinitions = {
    'title':             'application gvSIG-i18n Tool',
    'external_methods':  None,
    'tool_singletons':   [
        {
            'singleton_id': cTRAgvSIGi18nToolId, 
            'tool_module': 'Products.gvSIGi18nTool.TRAgvSIGi18nTool', 
            'tool_class':   'TRAgvSIGi18nTool', 
            'install_path': cTRAInstallPath_PortalSkinsCustom, 
            'required':     True, 
        },
    ],
}




##/code-section module-footer



