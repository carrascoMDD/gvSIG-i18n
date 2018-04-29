# -*- coding: utf-8 -*-
#
# File: TRAConfiguracionPaginaTraducciones.py
#
# Copyright (c) 2011 by 2008, 2009, 2010 Conselleria de Infraestructuras y
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
from TRAConfiguracionPaginaTraducciones_Operaciones import TRAConfiguracionPaginaTraducciones_Operaciones
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from TRAElemento_Operaciones import TRAElemento_Operaciones

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    IntegerField(
        name='traduccionesPorPaginaPorDefecto',
        widget=IntegerField._properties['widget'](
            label="Numero de Traducciones en pagina por defecto",
            label2="Default Translations per page",
            description="Numero de Traducciones por defecto a presentar en las paginas de exploracion sin contar las traducciones a los idiomas de referencia.",
            description2="Default number of Translations to display in the Browse Translations page, not counting the translations into the reference languages.",
            label_msgid='gvSIGi18n_TRAConfiguracionPaginaTraducciones_attr_traduccionesPorPaginaPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPaginaTraducciones_attr_traduccionesPorPaginaPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Numero de Traducciones por defecto a presentar en las paginas de exploracion sin contar las traducciones a los idiomas de referencia.",
        duplicates="0",
        label2="Default Translations per page",
        ea_localid="1948",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Default number of Translations to display in the Browse Translations page, not counting the translations into the reference languages.",
        ea_guid="{E7F27387-A6A7-4840-AFEA-E54168EC7E41}",
        scale="0",
        default="40",
        label="Numero de Traducciones en pagina por defecto",
        length="0",
        containment="Not Specified",
        position="35",
        owner_class_name="TRAConfiguracionPaginaTraducciones"
    ),

    IntegerField(
        name='maximoRegistrosExplorados',
        widget=IntegerField._properties['widget'](
            label="Numero maximo de registros de traduccion por pagina por defecto",
            label2="Default Maximum number of translations records per page",
            description="Numero maximo por defecto de Traducciones a presentar en las paginas de exploracion de traducciones, incluyendo traducciones al idioma a traducir y los idiomas de referencia.",
            description2="Default maximum  number of Translations to display in the Browse Translations page, including the language to translate and the reference languages.",
            label_msgid='gvSIGi18n_TRAConfiguracionPaginaTraducciones_attr_maximoRegistrosExplorados_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPaginaTraducciones_attr_maximoRegistrosExplorados_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Numero maximo por defecto de Traducciones a presentar en las paginas de exploracion de traducciones, incluyendo traducciones al idioma a traducir y los idiomas de referencia.",
        duplicates="0",
        label2="Default Maximum number of translations records per page",
        ea_localid="1949",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Default maximum  number of Translations to display in the Browse Translations page, including the language to translate and the reference languages.",
        ea_guid="{6A752551-39A6-4bd1-9A90-27AA70F7A791}",
        scale="0",
        default="1000",
        label="Numero maximo de registros de traduccion por pagina por defecto",
        length="0",
        containment="Not Specified",
        position="12",
        owner_class_name="TRAConfiguracionPaginaTraducciones"
    ),

    StringField(
        name='modoInteraccionPorDefecto',
        widget=SelectionWidget(
            label="Modo de Interaccion con el Servidor por defecto",
            label2="Default Server Interaction mode",
            description="Cuando sea Asincrono el navegador de internet enviara los cambios al servidor sin refrescar toda la pagina, permitiendo continuar el trabajo en la pagina actual. Cuando Sincrono, enviara cambios al servidor cargando una pagina completamente nueva.",
            description2="When Asynchronous the internet browser will send changes to server without refreshing the whole page, allowing continuation of work in the current page. When Synchronous the internet browser will send changes to server by loading a completely new page.",
            label_msgid='gvSIGi18n_TRAConfiguracionPaginaTraducciones_attr_modoInteraccionPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPaginaTraducciones_attr_modoInteraccionPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Cuando sea Asincrono el navegador de internet enviara los cambios al servidor sin refrescar toda la pagina, permitiendo continuar el trabajo en la pagina actual. Cuando Sincrono, enviara cambios al servidor cargando una pagina completamente nueva.",
        vocabulary=['Asincrono','Sincrono',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPaginaTraducciones_attr_modoInteraccionPorDefecto_option_Asincrono', 'gvSIGi18n_TRAConfiguracionPaginaTraducciones_attr_modoInteraccionPorDefecto_option_Sincrono'],
        label2="Default Server Interaction mode",
        ea_localid="1935",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="When Asynchronous the internet browser will send changes to server without refreshing the whole page, allowing continuation of work in the current page. When Synchronous the internet browser will send changes to server by loading a completely new page.",
        ea_guid="{E2B4929F-AFC5-4c80-BF7E-D052DDCA9258}",
        vocabulary2=['Asynchronous','Syncronous',],
        scale="0",
        default="Asincrono",
        label="Modo de Interaccion con el Servidor por defecto",
        length="0",
        containment="Not Specified",
        position="14",
        owner_class_name="TRAConfiguracionPaginaTraducciones"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAConfiguracionPaginaTraducciones_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAConfiguracion, 'schema', Schema(())).copy() + \
    getattr(TRAConfiguracionPaginaTraducciones_Operaciones, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAConfiguracionPaginaTraducciones(OrderedBaseFolder, TRAConfiguracion, TRAConfiguracionPaginaTraducciones_Operaciones):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAConfiguracion,'__implements__',()),) + (getattr(TRAConfiguracionPaginaTraducciones_Operaciones,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Configuracion Pagina Traducciones'

    meta_type = 'TRAConfiguracionPaginaTraducciones'
    portal_type = 'TRAConfiguracionPaginaTraducciones'


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



    allowed_content_types = [] + list(getattr(TRAConfiguracion, 'allowed_content_types', [])) + list(getattr(TRAConfiguracionPaginaTraducciones_Operaciones, 'allowed_content_types', []))
    filter_content_types             = 1
    global_allow                     = 0
    content_icon = 'traconfiguracion.gif'
    immediate_view                   = 'Tabular'
    default_view                     = 'Tabular'
    suppl_views                      = ['Tabular',]
    typeDescription                  = "Configuracion del catalogo de traducciones, con parametros controlando la operacion de la pagina de traducciones del catalogo."
    typeDescMsgId                    =  'gvSIGi18n_TRAConfiguracionPaginaTraducciones_help'
    archetype_name2                  = 'Translations Page Configuration'
    typeDescription2                 = '''Translations catalog configuration, with parameters controlling operation of the translations page in the catalog.'''
    archetype_name_msgid             = 'gvSIGi18n_TRAConfiguracionPaginaTraducciones_label'
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

    schema = TRAConfiguracionPaginaTraducciones_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata', 'sharing', 'folderContents']:
            a['visible'] = 0
    return fti

registerType(TRAConfiguracionPaginaTraducciones, PROJECTNAME)
# end of class TRAConfiguracionPaginaTraducciones

##code-section module-footer #fill in your manual code here
##/code-section module-footer



