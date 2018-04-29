# -*- coding: utf-8 -*-
#
# File: TRAConfiguracionVarios.py
#
# Copyright (c) 2010 by 2008, 2009, 2010 Conselleria de Infraestructuras y
# Transporte de la Generalidad Valenciana
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

__author__ = """Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
<gvSIGi18n@gvSIG.org>, Model Driven Development sl <gvSIGi18n@ModelDD.org>,
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.gvSIGi18n.TRAConfiguracion import TRAConfiguracion
from TRAConfiguracionVarios_Operaciones import TRAConfiguracionVarios_Operaciones
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from TRAElemento_Operaciones import TRAElemento_Operaciones

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    IntegerField(
        name='maximoNumeroCambiosRecientes',
        widget=IntegerField._properties['widget'](
            label="Maximo numero de Cambios Recientes",
            label2="Maximum number of Recent Changes",
            description="El sistema recordara cambios recientes de estados de traducciones, hasta este maximo, despreciando los cambios mas antiguos cuando se exceda el maximo.",
            description2="The system shall record recent Translation status changes, up to this maximum, discarding the oldest ones when the maximum is exceeded,",
            label_msgid='gvSIGi18n_TRAConfiguracionVarios_attr_maximoNumeroCambiosRecientes_label',
            description_msgid='gvSIGi18n_TRAConfiguracionVarios_attr_maximoNumeroCambiosRecientes_help',
            i18n_domain='gvSIGi18n',
        ),
        description="El sistema recordara cambios recientes de estados de traducciones, hasta este maximo, despreciando los cambios mas antiguos cuando se exceda el maximo.",
        duplicates="0",
        label2="Maximum number of Recent Changes",
        ea_localid="1585",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="The system shall record recent Translation status changes, up to this maximum, discarding the oldest ones when the maximum is exceeded,",
        ea_guid="{FA1DD245-141B-46df-8764-2ACDE92809D2}",
        scale="0",
        default="5000",
        label="Maximo numero de Cambios Recientes",
        length="0",
        containment="Not Specified",
        position="0",
        owner_class_name="TRAConfiguracionVarios"
    ),

    IntegerField(
        name='segundosParaConfirmarAccion',
        widget=IntegerField._properties['widget'](
            label="Tiempo en segundos para confirmar Accion",
            label2="Time in seconds to confirm launch of a long process",
            description="Tiempo en segundos del que dispone el Usuario para confirmar lanzamiento de procesos de larga duracion. Si no confirma en este tiempo, el Usuario debera volver a solicitar la accion.",
            description2="Time in seconds for the User to confirm the launch of a long process. If the User does not confirm in this period of time, the user shall request the action again.",
            label_msgid='gvSIGi18n_TRAConfiguracionVarios_attr_segundosParaConfirmarAccion_label',
            description_msgid='gvSIGi18n_TRAConfiguracionVarios_attr_segundosParaConfirmarAccion_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Tiempo en segundos del que dispone el Usuario para confirmar lanzamiento de procesos de larga duracion. Si no confirma en este tiempo, el Usuario debera volver a solicitar la accion.",
        duplicates="0",
        label2="Time in seconds to confirm launch of a long process",
        ea_localid="1605",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Time in seconds for the User to confirm the launch of a long process. If the User does not confirm in this period of time, the user shall request the action again.",
        ea_guid="{EA7AA3DF-5BD4-4644-A3D4-F42F915299A1}",
        scale="0",
        default="120",
        label="Tiempo en segundos para confirmar Accion",
        length="0",
        containment="Not Specified",
        position="30",
        owner_class_name="TRAConfiguracionVarios"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAConfiguracionVarios_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAConfiguracion, 'schema', Schema(())).copy() + \
    getattr(TRAConfiguracionVarios_Operaciones, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAConfiguracionVarios(OrderedBaseFolder, TRAConfiguracion, TRAConfiguracionVarios_Operaciones):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAConfiguracion,'__implements__',()),) + (getattr(TRAConfiguracionVarios_Operaciones,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Configuracion Varios'

    meta_type = 'TRAConfiguracionVarios'
    portal_type = 'TRAConfiguracionVarios'


    # Change Audit fields

    creation_date_field = 'fechaCreacion'
    creation_user_field = 'usuarioCreador'
    modification_date_field = 'fechaModificacion'
    modification_user_field = 'usuarioModificador'
    deletion_date_field = 'fechaEliminacion'
    deletion_user_field = 'usuarioEliminador'
    is_inactive_field = 'estaInactivo'
    change_counter_field = 'contadorCambios'
    change_log_field = 'registroDeCambios'



    allowed_content_types = [] + list(getattr(TRAConfiguracion, 'allowed_content_types', [])) + list(getattr(TRAConfiguracionVarios_Operaciones, 'allowed_content_types', []))
    filter_content_types             = 1
    global_allow                     = 0
    content_icon = 'traconfiguracion.gif'
    immediate_view                   = 'Tabular'
    default_view                     = 'Tabular'
    suppl_views                      = ['Tabular',]
    typeDescription                  = "Configuracion del catalogo de traducciones, conparametros de varias operaciones sobre el catalogo."
    typeDescMsgId                    =  'gvSIGi18n_TRAConfiguracionVarios_help'
    archetype_name2                  = 'Various Configuration'
    typeDescription2                 = '''Translations catalog configuration, with parameters controlling various operations on the catalog.'''
    archetype_name_msgid             = 'gvSIGi18n_TRAConfiguracionVarios_label'
    factory_methods                  = None
    factory_enablers                 = None
    propagate_delete_impact_to       = None
    allow_discussion = False


    actions =  (


       {'action': "string:${object_url}/Editar",
        'category': "object_buttons",
        'id': 'TRA_configurar',
        'name': 'Configure',
        'permissions': ("Modify portal content",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Configure_TRAConfiguracion')"""
       },


       {'action': "string:$object_url/Editar",
        'category': "object",
        'id': 'edit',
        'name': 'Edit',
        'permissions': ("Modify portal content",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Configure_TRAConfiguracion')"""
       },


       {'action': "string:${object_url}/Tabular",
        'category': "object",
        'id': 'view',
        'name': 'View',
        'permissions': ("View",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'View_any_TRA_element')"""
       },


       {'action': "string:${object_url}/MDDCacheStatus/",
        'category': "object_buttons",
        'id': 'mddcachestatus',
        'name': 'Cache',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'CacheStatus_on_any_TRA_element')"""
       },


       {'action': "string:${object_url}/MDDChanges",
        'category': "object_buttons",
        'id': 'mddchanges',
        'name': 'Changes',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Changes_on_any_TRA_element')"""
       },


       {'action': "string:$object_url/content_status_history",
        'category': "object",
        'id': 'content_status_history',
        'name': 'State',
        'permissions': ("View",),
        'condition': """python:0"""
       },


       {'action': "string:${object_url}/TRAFlushCache_action",
        'category': "object_buttons",
        'id': 'tra_flushcache',
        'name': 'FlushCache',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fRoleQuery_IsAnyRol( object, [ 'Manager', 'Owner', 'TRACreator', 'TRAManager', 'TRACoordinator',])"""
       },


       {'action': "string:${object_url}/folder_listing",
        'category': "folder",
        'id': 'folderlisting',
        'name': 'Folder Listing',
        'permissions': ("View",),
        'condition': """python:0"""
       },


       {'action': "string:${object_url}/TRAInventory_action",
        'category': "object_buttons",
        'id': 'TRA_inventario',
        'name': 'Inventory',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Inventory_TRAElemento')"""
       },


       {'action': "string:${object_url}/sharing",
        'category': "object",
        'id': 'local_roles',
        'name': 'Sharing',
        'permissions': ("Manage properties",),
        'condition': """python:0"""
       },


       {'action': "string:${object_url}/TRARecatalog_action",
        'category': "object_buttons",
        'id': 'TRA_recatalogar',
        'name': 'ReCatalog',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'ReCatalog_TRAElemento')"""
       },


       {'action': "string:${object_url}/TRAResetPermissions_action",
        'category': "object_buttons",
        'id': 'TRA_reestablecerpermisos',
        'name': 'Reset Permissions',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'ResetPermissions_TRAElemento')"""
       },


       {'action': "string:${object_url}/TRAVerifyPermissions_action",
        'category': "object_buttons",
        'id': 'TRA_verificarpermisos',
        'name': 'Verify Permissions',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'VerifyPermissions_TRAElemento')"""
       },


       {'action': "string:${object_url}/reference_graph",
        'category': "object",
        'id': 'references',
        'name': 'References',
        'permissions': ("Modify portal content",),
        'condition': """python:0"""
       },


       {'action': "string:${object_url}/TRASeguridadUsuarioConectado",
        'category': "object_buttons",
        'id': 'TRA_SeguridadUsuarioConectado',
        'name': 'Permissions',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Permissions_on_any_TRA_element')"""
       },


    )

    _at_rename_after_creation = True

    schema = TRAConfiguracionVarios_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata', 'sharing', 'folderContents']:
            a['visible'] = 0
    return fti

registerType(TRAConfiguracionVarios, PROJECTNAME)
# end of class TRAConfiguracionVarios

##code-section module-footer #fill in your manual code here
##/code-section module-footer



