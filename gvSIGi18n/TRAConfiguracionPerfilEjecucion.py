# -*- coding: utf-8 -*-
#
# File: TRAConfiguracionPerfilEjecucion.py
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
from TRAConfiguracionPerfilEjecucion_Operaciones import TRAConfiguracionPerfilEjecucion_Operaciones
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from TRAElemento_Operaciones import TRAElemento_Operaciones

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    BooleanField(
        name='perfilDeEjecucionHabilitado',
        widget=BooleanField._properties['widget'](
            label="Perfil de Ejecucion Habilitado",
            label2="Execution Profiling Enabled",
            description="Si Verdadero, el sistema registrara el perfil de la ejecucion, como secuencias anidadas de plantillas y metodos ejecutados.",
            description2="When True, the System shall record the execution profile, as nested sequences of executed templates and methods.",
            label_msgid='gvSIGi18n_TRAConfiguracionPerfilEjecucion_attr_perfilDeEjecucionHabilitado_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPerfilEjecucion_attr_perfilDeEjecucionHabilitado_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, el sistema registrara el perfil de la ejecucion, como secuencias anidadas de plantillas y metodos ejecutados.",
        duplicates="0",
        label2="Execution Profiling Enabled",
        ea_localid="1710",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="When True, the System shall record the execution profile, as nested sequences of executed templates and methods.",
        ea_guid="{53AA8DDC-878D-4084-8E8D-21E0CA662C25}",
        scale="0",
        default="False",
        label="Perfil de Ejecucion Habilitado",
        length="0",
        containment="Not Specified",
        position="2",
        owner_class_name="TRAConfiguracionPerfilEjecucion"
    ),

    BooleanField(
        name='tiemposDeEjecucionHabilitado',
        widget=BooleanField._properties['widget'](
            label="Tiempos de Ejecucion Habilitado",
            label2="Execution Timestamping Enabled",
            description="Si Verdadero, el sistema registrara el tiempo utilizado en la ejecucion, de plantillas y metodos.",
            description2="When True, the System shall record the time to execute templates and methods.",
            label_msgid='gvSIGi18n_TRAConfiguracionPerfilEjecucion_attr_tiemposDeEjecucionHabilitado_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPerfilEjecucion_attr_tiemposDeEjecucionHabilitado_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, el sistema registrara el tiempo utilizado en la ejecucion, de plantillas y metodos.",
        duplicates="0",
        label2="Execution Timestamping Enabled",
        ea_localid="1946",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="When True, the System shall record the time to execute templates and methods.",
        ea_guid="{0E02EAA8-385D-4fac-8965-09006CB04CA2}",
        scale="0",
        default="False",
        label="Tiempos de Ejecucion Habilitado",
        length="0",
        containment="Not Specified",
        position="6",
        owner_class_name="TRAConfiguracionPerfilEjecucion"
    ),

    BooleanField(
        name='registroRaizDeEjecucionAutomaticoHabilitado',
        widget=BooleanField._properties['widget'](
            label="Registro Raiz de Ejecucion Automatico Habilitado",
            label2="Execution auto root record Enabled",
            description="Si Verdadero, el sistema creara un registro de ejecucion raiz, cuando la plantilla o metodo que invoca no haya suministrado uno.",
            description2="If True, the system shall create a root execution record, when the caller template or method does not supply one.",
            label_msgid='gvSIGi18n_TRAConfiguracionPerfilEjecucion_attr_registroRaizDeEjecucionAutomaticoHabilitado_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPerfilEjecucion_attr_registroRaizDeEjecucionAutomaticoHabilitado_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, el sistema creara un registro de ejecucion raiz, cuando la plantilla o metodo que invoca no haya suministrado uno.",
        duplicates="0",
        label2="Execution auto root record Enabled",
        ea_localid="1942",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="If True, the system shall create a root execution record, when the caller template or method does not supply one.",
        ea_guid="{9D1E1A37-0653-491e-A15B-94111E391280}",
        scale="0",
        default="False",
        label="Registro Raiz de Ejecucion Automatico Habilitado",
        length="0",
        containment="Not Specified",
        position="5",
        owner_class_name="TRAConfiguracionPerfilEjecucion"
    ),

    BooleanField(
        name='escrituraEnDiscoDeRegistroDeEjecucionHabilitado',
        widget=BooleanField._properties['widget'](
            label="Escritura en Disco de Perfil de Ejecucion Habilitado",
            label2="Log Execution Profile to Disc Enabled",
            description="Si Verdadero, el sistema escribira el perfil de ejecucion en fichero de log en disco.",
            description2="If True, the system shall write the execution profile to the log.",
            label_msgid='gvSIGi18n_TRAConfiguracionPerfilEjecucion_attr_escrituraEnDiscoDeRegistroDeEjecucionHabilitado_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPerfilEjecucion_attr_escrituraEnDiscoDeRegistroDeEjecucionHabilitado_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, el sistema escribira el perfil de ejecucion en fichero de log en disco.",
        duplicates="0",
        label2="Log Execution Profile to Disc Enabled",
        ea_localid="1713",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="If True, the system shall write the execution profile to the log.",
        ea_guid="{933CC6B5-A0EE-4909-9FB5-3FFDDD6F0B23}",
        scale="0",
        default="False",
        label="Escritura en Disco de Perfil de Ejecucion Habilitado",
        length="0",
        containment="Not Specified",
        position="1",
        owner_class_name="TRAConfiguracionPerfilEjecucion"
    ),

    BooleanField(
        name='escrituraEnDiscoDeRegistroDeEjecucionDetalladoHabilitado',
        widget=BooleanField._properties['widget'](
            label="Escritura en Disco de Perfil Detallado de Ejecucion Habilitado",
            label2="Log Detailed Execution Profile to Disc Enabled",
            description="Si Verdadero, el sistema escribira detalladamente el perfil de ejecucion en  fichero de log en disco.",
            description2="If True, the system shall write the execution profile to the log in a detailed form.",
            label_msgid='gvSIGi18n_TRAConfiguracionPerfilEjecucion_attr_escrituraEnDiscoDeRegistroDeEjecucionDetalladoHabilitado_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPerfilEjecucion_attr_escrituraEnDiscoDeRegistroDeEjecucionDetalladoHabilitado_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, el sistema escribira detalladamente el perfil de ejecucion en  fichero de log en disco.",
        duplicates="0",
        label2="Log Detailed Execution Profile to Disc Enabled",
        ea_localid="1714",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="If True, the system shall write the execution profile to the log in a detailed form.",
        ea_guid="{BCA930B7-404D-421e-A338-6BC9BB56BDAC}",
        scale="0",
        default="False",
        label="Escritura en Disco de Perfil Detallado de Ejecucion Habilitado",
        length="0",
        containment="Not Specified",
        position="0",
        owner_class_name="TRAConfiguracionPerfilEjecucion"
    ),

    BooleanField(
        name='presentacionEnPaginasDeRegistroDeEjecucionHabilitado',
        widget=BooleanField._properties['widget'](
            label="Presentacion en Paginas de Perfil de Ejecucion Habilitado",
            label2="Render Execution Profile in Pages Enabled",
            description="Si Verdadero, el sistema presentara en las paginas el perfil de ejecucion.",
            description2="If True, the system shall present in pages the execution profile.",
            label_msgid='gvSIGi18n_TRAConfiguracionPerfilEjecucion_attr_presentacionEnPaginasDeRegistroDeEjecucionHabilitado_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPerfilEjecucion_attr_presentacionEnPaginasDeRegistroDeEjecucionHabilitado_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, el sistema presentara en las paginas el perfil de ejecucion.",
        duplicates="0",
        label2="Render Execution Profile in Pages Enabled",
        ea_localid="1940",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="If True, the system shall present in pages the execution profile.",
        ea_guid="{2099719C-A346-494f-A54F-43F494863CF5}",
        scale="0",
        default="False",
        label="Presentacion en Paginas de Perfil de Ejecucion Habilitado",
        length="0",
        containment="Not Specified",
        position="3",
        owner_class_name="TRAConfiguracionPerfilEjecucion"
    ),

    BooleanField(
        name='presentacionEnPaginasDeTiempoDeEjecucionHabilitado',
        widget=BooleanField._properties['widget'](
            label="Presentacion en Paginas de Tiempo de Ejecucion Habilitado",
            label2="Render Execution Time in Pages Enabled",
            description="Si Verdadero, el sistema presentara en las paginas el tiempo de ejecucion.",
            description2="If True, the system shall present in pages the execution time.",
            label_msgid='gvSIGi18n_TRAConfiguracionPerfilEjecucion_attr_presentacionEnPaginasDeTiempoDeEjecucionHabilitado_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPerfilEjecucion_attr_presentacionEnPaginasDeTiempoDeEjecucionHabilitado_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, el sistema presentara en las paginas el tiempo de ejecucion.",
        duplicates="0",
        label2="Render Execution Time in Pages Enabled",
        ea_localid="1941",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="If True, the system shall present in pages the execution time.",
        ea_guid="{C401D477-783D-47ef-B3A5-977C0E748F85}",
        scale="0",
        default="False",
        label="Presentacion en Paginas de Tiempo de Ejecucion Habilitado",
        length="0",
        containment="Not Specified",
        position="4",
        owner_class_name="TRAConfiguracionPerfilEjecucion"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAConfiguracionPerfilEjecucion_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAConfiguracion, 'schema', Schema(())).copy() + \
    getattr(TRAConfiguracionPerfilEjecucion_Operaciones, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAConfiguracionPerfilEjecucion(OrderedBaseFolder, TRAConfiguracion, TRAConfiguracionPerfilEjecucion_Operaciones):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAConfiguracion,'__implements__',()),) + (getattr(TRAConfiguracionPerfilEjecucion_Operaciones,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Configuracion Perfil Ejecucion'

    meta_type = 'TRAConfiguracionPerfilEjecucion'
    portal_type = 'TRAConfiguracionPerfilEjecucion'


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



    allowed_content_types = [] + list(getattr(TRAConfiguracion, 'allowed_content_types', [])) + list(getattr(TRAConfiguracionPerfilEjecucion_Operaciones, 'allowed_content_types', []))
    filter_content_types             = 1
    global_allow                     = 0
    content_icon = 'traconfiguracion.gif'
    immediate_view                   = 'Tabular'
    default_view                     = 'Tabular'
    suppl_views                      = ['Tabular',]
    typeDescription                  = "Configuracion del catalogo de traducciones, con parametros controlando el perfilado de la ejecucion de las operaciones sobre el catalogo."
    typeDescMsgId                    =  'gvSIGi18n_TRAConfiguracionPerfilEjecucion_help'
    archetype_name2                  = 'Execution Profile Configuration'
    typeDescription2                 = '''Translations catalog configuration, with parameters controlling the executin profiling of operations on the catalog.'''
    archetype_name_msgid             = 'gvSIGi18n_TRAConfiguracionPerfilEjecucion_label'
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

    schema = TRAConfiguracionPerfilEjecucion_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata', 'sharing', 'folderContents']:
            a['visible'] = 0
    return fti

registerType(TRAConfiguracionPerfilEjecucion, PROJECTNAME)
# end of class TRAConfiguracionPerfilEjecucion

##code-section module-footer #fill in your manual code here
##/code-section module-footer



