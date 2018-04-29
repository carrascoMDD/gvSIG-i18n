# -*- coding: utf-8 -*-
#
# File: TRAConfiguracionSolicitudesCadenas.py
#
# Copyright (c) 2013 by 2008, 2009, 2010, 2011 Conselleria de Infraestructuras
# y Transporte de la Generalidad Valenciana
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
from TRAConfiguracionSolicitudesCadenas_Operaciones import TRAConfiguracionSolicitudesCadenas_Operaciones
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from TRAElemento_Operaciones import TRAElemento_Operaciones
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='codigoIdiomaRequeridoSolicitudesNuevasCadenas',
        widget=StringWidget(
            label="Codigo de Idioma para Solicitudes de Nuevas Cadenas",
            label2="Language Code  for new String Requests",
            description="Codigo del lenguage en el que se requiere una traduccion cuando se solicitan nuevas cadenas.",
            description2="Code of the language for which a translation is requiered when requesting creation of new strings.",
            label_msgid='gvSIGi18n_TRAConfiguracionSolicitudesCadenas_attr_codigoIdiomaRequeridoSolicitudesNuevasCadenas_label',
            description_msgid='gvSIGi18n_TRAConfiguracionSolicitudesCadenas_attr_codigoIdiomaRequeridoSolicitudesNuevasCadenas_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Codigo del lenguage en el que se requiere una traduccion cuando se solicitan nuevas cadenas.",
        searchable=0,
        duplicates="0",
        label2="Language Code  for new String Requests",
        ea_localid="1921",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Code of the language for which a translation is requiered when requesting creation of new strings.",
        ea_guid="{E3A15617-4E79-46c4-B98F-7631A464DE20}",
        scale="0",
        default="en",
        label="Codigo de Idioma para Solicitudes de Nuevas Cadenas",
        length="0",
        containment="Not Specified",
        position="2",
        owner_class_name="TRAConfiguracionSolicitudesCadenas"
    ),

    StringField(
        name='codigoIdiomaReferenciaSolicitudesNuevasCadenas',
        widget=StringWidget(
            label="Codigo de Idioma de Referencia  para Solicitudes de Nuevas Cadenas",
            label2="Reference Language Code for new String Requests",
            description="Codigo del lenguage para el que el desarrollador puede proporcionar una traduccion de referencia, cuando se solicitan nuevas cadenas.",
            description2="Code of the language for which the developer may provide a reference  translation when requesting creation of new strings.",
            label_msgid='gvSIGi18n_TRAConfiguracionSolicitudesCadenas_attr_codigoIdiomaReferenciaSolicitudesNuevasCadenas_label',
            description_msgid='gvSIGi18n_TRAConfiguracionSolicitudesCadenas_attr_codigoIdiomaReferenciaSolicitudesNuevasCadenas_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Codigo del lenguage para el que el desarrollador puede proporcionar una traduccion de referencia, cuando se solicitan nuevas cadenas.",
        searchable=0,
        duplicates="0",
        label2="Reference Language Code for new String Requests",
        ea_localid="1920",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Code of the language for which the developer may provide a reference  translation when requesting creation of new strings.",
        ea_guid="{044DA7EB-479B-4eb0-A47F-495247410A68}",
        scale="0",
        default="es",
        label="Codigo de Idioma de Referencia  para Solicitudes de Nuevas Cadenas",
        length="0",
        containment="Not Specified",
        position="1",
        owner_class_name="TRAConfiguracionSolicitudesCadenas"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAConfiguracionSolicitudesCadenas_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAConfiguracion, 'schema', Schema(())).copy() + \
    getattr(TRAConfiguracionSolicitudesCadenas_Operaciones, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAConfiguracionSolicitudesCadenas(OrderedBaseFolder, TRAConfiguracion, TRAConfiguracionSolicitudesCadenas_Operaciones):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAConfiguracion,'__implements__',()),) + (getattr(TRAConfiguracionSolicitudesCadenas_Operaciones,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Configuracion Solicitudes Cadenas'

    meta_type = 'TRAConfiguracionSolicitudesCadenas'
    portal_type = 'TRAConfiguracionSolicitudesCadenas'


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



    allowed_content_types = [] + list(getattr(TRAConfiguracion, 'allowed_content_types', [])) + list(getattr(TRAConfiguracionSolicitudesCadenas_Operaciones, 'allowed_content_types', []))
    filter_content_types             = 1
    global_allow                     = 0
    content_icon = 'traconfiguracion.gif'
    immediate_view                   = 'Tabular'
    default_view                     = 'Tabular'
    suppl_views                      = ['Tabular',]
    typeDescription                  = "Configuracion del catalogo de traducciones, con parametros controlando las operaciones sobre solicitudes de cadenas para el catalogo."
    typeDescMsgId                    =  'gvSIGi18n_TRAConfiguracionSolicitudesCadenas_help'
    archetype_name2                  = 'New String Requests Configuration'
    typeDescription2                 = '''Translations catalog configuration, with parameters controlling string requests operations for the catalog.'''
    archetype_name_msgid             = 'gvSIGi18n_TRAConfiguracionSolicitudesCadenas_label'
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

    schema = TRAConfiguracionSolicitudesCadenas_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata', 'sharing', 'folderContents']:
            a['visible'] = 0
    return fti

registerType(TRAConfiguracionSolicitudesCadenas, PROJECTNAME)
# end of class TRAConfiguracionSolicitudesCadenas

##code-section module-footer #fill in your manual code here
##/code-section module-footer



