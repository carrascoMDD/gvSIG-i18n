# -*- coding: utf-8 -*-
#
# File: TRAColeccionCadenas.py
#
# Copyright (c) 2009 by Conselleria de Infraestructuras y Transporte de la
# Generalidad Valenciana
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
from Products.gvSIGi18n.TRAColeccionArquetipos import TRAColeccionArquetipos
from Products.gvSIGi18n.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    ComputedField(
        name='cadenas',
        widget=ComputedWidget(
            label="Cadenas a traducir",
            label2="Strings to translate",
            description="Cadenas para ser traducidas a los varios idiomas.",
            description2="Strings to translate to the various languages.",
            label_msgid='gvSIGi18n_TRAColeccionCadenas_contents_cadenas_label',
            description_msgid='gvSIGi18n_TRAColeccionCadenas_contents_cadenas_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=False,
        label2='Strings to translate',
        additional_columns=['simbolo', 'estadoCadena', 'fechaCreacionTextual', 'usuarioCreador', 'fechaCancelacionTextual'],
        label='Cadenas a traducir',
        represents_aggregation=True,
        description2='Strings to translate to the various languages.',
        multiValued=1,
        owner_class_name="TRAColeccionCadenas",
        expression="context.objectValues(['TRACadena'])",
        computed_types=['TRACadena'],
        non_framework_elements=False,
        description='Cadenas para ser traducidas a los varios idiomas.'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAColeccionCadenas_schema = BaseBTreeFolderSchema.copy() + \
    getattr(TRAColeccionArquetipos, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAColeccionCadenas(BaseBTreeFolder, TRAColeccionArquetipos):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseBTreeFolder,'__implements__',()),) + (getattr(TRAColeccionArquetipos,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Coleccion de Cadenas'

    meta_type = 'TRAColeccionCadenas'
    portal_type = 'TRAColeccionCadenas'


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



    use_folder_tabs = 0

    allowed_content_types = ['TRACadena'] + list(getattr(TRAColeccionArquetipos, 'allowed_content_types', []))
    filter_content_types = 1
    global_allow = 0
    #content_icon = 'TRAColeccionCadenas.gif'
    immediate_view = 'Tabular'
    default_view = 'Tabular'
    suppl_views = ['Tabular',]
    typeDescription = "Coleccion de cadenas a traducir a los varios idiomas."
    typeDescMsgId =  'gvSIGi18n_TRAColeccionCadenas_help'
    archetype_name2 = 'Strings collection'
    typeDescription2 = '''Collection of strings to translate to a number of languages.'''
    archetype_name_msgid = 'gvSIGi18n_TRAColeccionCadenas_label'
    factory_methods = None
    factory_enablers = None
    allow_discussion = False


    actions =  (


       {'action': "string:${object_url}/folder_listing",
        'category': "folder",
        'id': 'folderlisting',
        'name': 'Folder Listing',
        'permissions': ("View",),
        'condition': """python:0"""
       },


       {'action': "string:${object_url}/reference_graph",
        'category': "object",
        'id': 'references',
        'name': 'References',
        'permissions': ("Modify portal content",),
        'condition': """python:0"""
       },


       {'action': "string:${object_url}/Tabular",
        'category': "object",
        'id': 'view',
        'name': 'View',
        'permissions': ("View",),
        'condition': """python:1"""
       },


       {'action': "string:$object_url/Editar",
        'category': "object",
        'id': 'edit',
        'name': 'Edit',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fAllowWrite()"""
       },


       {'action': "string:${object_url}/sharing",
        'category': "object",
        'id': 'local_roles',
        'name': 'Sharing',
        'permissions': ("Manage properties",),
        'condition': """python:0"""
       },


       {'action': "string:${object_url}/TRASeguridadUsuarioConectado",
        'category': "object_buttons",
        'id': 'TRA_SeguridadUsuarioConectado',
        'name': 'Permissions',
        'permissions': ("View",),
        'condition': """python:1"""
       },


       {'action': "string:$object_url/content_status_history",
        'category': "object",
        'id': 'content_status_history',
        'name': 'State',
        'permissions': ("View",),
        'condition': """python:0"""
       },


    )

    _at_rename_after_creation = True

    schema = TRAColeccionCadenas_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('cb_isMoveable')
    def cb_isMoveable(self):
        """
        """
        
        return False

    security.declarePublic('manage_beforeDelete')
    def manage_beforeDelete(self,item,container):
        """
        """
        
        return TRAColeccionArquetipos.manage_beforeDelete( self, item, container)

    security.declarePublic('displayContentsTab')
    def displayContentsTab(self):
        """
        """
        
        return False

    security.declarePublic('manage_afterAdd')
    def manage_afterAdd(self,item,container):
        """
        """
        
        return TRAColeccionArquetipos.manage_afterAdd( self, item, container)

    security.declarePublic('cb_isCopyable')
    def cb_isCopyable(self):
        """
        """
        
        return False

    security.declarePublic('manage_pasteObjects')
    def manage_pasteObjects(self,cb_copy_data,REQUEST):
        """
        """
        
        return self.pHandle_manage_pasteObjects( cb_copy_data, REQUEST)
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata', 'sharing', 'folderContents']:
            a['visible'] = 0
    return fti

registerType(TRAColeccionCadenas, PROJECTNAME)
# end of class TRAColeccionCadenas

##code-section module-footer #fill in your manual code here
##/code-section module-footer



