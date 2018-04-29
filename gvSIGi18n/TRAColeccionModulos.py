# -*- coding: utf-8 -*-
#
# File: TRAColeccionModulos.py
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

__author__ = """Antonio Carrasco Valero (Model Driven Development sl) <gvSIGi18n@gvSIG.org>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.gvSIGi18n.TRAColeccionArquetipos import TRAColeccionArquetipos
from Products.gvSIGi18n.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    ComputedField(
        name='modulos',
        widget=ComputedWidget(
            label="Modulos",
            label2="Modules",
            description="Modulos en el Producto a traducir.",
            description2="Modules in the Product to translate.",
            label_msgid='gvSIGi18n_TRAColeccionModulos_contents_modulos_label',
            description_msgid='gvSIGi18n_TRAColeccionModulos_contents_modulos_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=False,
        label2='Modules',
        additional_columns=['esModuloPrincipal'],
        label='Modulos',
        represents_aggregation=True,
        description2='Modules in the Product to translate.',
        multiValued=1,
        owner_class_name="TRAColeccionModulos",
        expression="context.objectValues(['TRAModulo'])",
        computed_types=['TRAModulo'],
        non_framework_elements=False,
        description='Modulos en el Producto a traducir.'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAColeccionModulos_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAColeccionArquetipos, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAColeccionModulos(OrderedBaseFolder, TRAColeccionArquetipos):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAColeccionArquetipos,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Coleccion de Modulos'

    meta_type = 'TRAColeccionModulos'
    portal_type = 'TRAColeccionModulos'
    allowed_content_types = ['TRAModulo'] + list(getattr(TRAColeccionArquetipos, 'allowed_content_types', []))
    filter_content_types = 1
    global_allow = 0
    #content_icon = 'TRAColeccionModulos.gif'
    immediate_view = 'Tabular'
    default_view = 'Tabular'
    suppl_views = ['Tabular',]
    typeDescription = "Colecicon de Modulos en el producto a traducir."
    typeDescMsgId =  'gvSIGi18n_TRAColeccionModulos_help'
    archetype_name2 = 'Modules collection'
    typeDescription2 = '''Collection of Modules in the product to translate.'''
    archetype_name_msgid = 'gvSIGi18n_TRAColeccionModulos_label'
    factory_methods = None
    factory_enablers = None
    allow_discussion = False


    actions =  (


       {'action': "string:$object_url/content_status_history",
        'category': "object",
        'id': 'content_status_history',
        'name': 'State',
        'permissions': ("View",),
        'condition': 'python:0'
       },


       {'action': "string:$object_url/Editar",
        'category': "object",
        'id': 'edit',
        'name': 'Edit',
        'permissions': ("Modify portal content",),
        'condition': 'python:0'
       },


       {'action': "string:${object_url}/folder_listing",
        'category': "folder",
        'id': 'folderlisting',
        'name': 'Folder Listing',
        'permissions': ("View",),
        'condition': 'python:0'
       },


       {'action': "string:${object_url}/sharing",
        'category': "object",
        'id': 'local_roles',
        'name': 'Sharing',
        'permissions': ("Manage properties",),
        'condition': 'python:0'
       },


       {'action': "string:${object_url}/reference_graph",
        'category': "object",
        'id': 'references',
        'name': 'References',
        'permissions': ("Modify portal content",),
        'condition': 'python:0'
       },


       {'action': "string:${object_url}/Tabular",
        'category': "object",
        'id': 'view',
        'name': 'View',
        'permissions': ("View",),
        'condition': 'python:1'
       },


       {'action': "string:${object_url}/sharing",
        'category': "object",
        'id': 'local_roles',
        'name': 'Sharing',
        'permissions': ("Manage properties",),
        'condition': 'python:object.fRoleQuery_IsCoordinator()'
       },


    )

    _at_rename_after_creation = True

    schema = TRAColeccionModulos_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('cb_isCopyable')
    def cb_isCopyable(self):
        """
        """
        
        return False

    security.declarePublic('manage_afterAdd')
    def manage_afterAdd(self,item,container):
        """
        """
        
        return TRAColeccionArquetipos.manage_afterAdd( self, item, container)

    security.declarePublic('manage_beforeDelete')
    def manage_beforeDelete(self,item,container):
        """
        """
        
        return TRAColeccionArquetipos.manage_beforeDelete( self, item, container)

    security.declarePublic('manage_pasteObjects')
    def manage_pasteObjects(self,cb_copy_data,REQUEST):
        """
        """
        
        return self.pHandle_manage_pasteObjects( cb_copy_data, REQUEST)
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata', 'sharing']:
            a['visible'] = 0
    return fti

registerType(TRAColeccionModulos, PROJECTNAME)
# end of class TRAColeccionModulos

##code-section module-footer #fill in your manual code here
##/code-section module-footer



