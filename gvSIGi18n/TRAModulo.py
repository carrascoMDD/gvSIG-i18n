# -*- coding: utf-8 -*-
#
# File: TRAModulo.py
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
from Products.gvSIGi18n.TRAArquetipo import TRAArquetipo
from Products.gvSIGi18n.TRAModulo_Operaciones import TRAModulo_Operaciones
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='dominio',
        widget=StringWidget(
            label="Dominio",
            label2="Domain",
            description="Dato que aparece en los ficheros de exportacion de tipo GNUgettext PO, para identificar la aplicacion o modulo a que se aplican las traducciones.",
            description2="Iinformation that appears in the exported files of GNUgettext PO format, to indicate the application or module to which the translations apply.",
            label_msgid='gvSIGi18n_TRAModulo_attr_dominio_label',
            description_msgid='gvSIGi18n_TRAModulo_attr_dominio_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Dato que aparece en los ficheros de exportacion de tipo GNUgettext PO, para identificar la aplicacion o modulo a que se aplican las traducciones.",
        duplicates="0",
        label2="Domain",
        ea_localid="1170",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="Iinformation that appears in the exported files of GNUgettext PO format, to indicate the application or module to which the translations apply.",
        containment="Not Specified",
        ea_guid="{70C5AFBA-F231-4944-BC58-D108311B4B10}",
        position="6",
        owner_class_name="TRAModulo",
        label="Dominio"
    ),

    BooleanField(
        name='esModuloPrincipal',
        widget=BooleanField._properties['widget'](
            label="Es Modulo Principal",
            label2="Is Main Module",
            description="Si las traducciones en este Modulo pueden resolver las cadenas de mismo simbolo de otros modulos.",
            description2="Whether the translations in this Module may resolve the strings of same symbol in other modules.",
            label_msgid='gvSIGi18n_TRAModulo_attr_esModuloPrincipal_label',
            description_msgid='gvSIGi18n_TRAModulo_attr_esModuloPrincipal_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si las traducciones en este Modulo pueden resolver las cadenas de mismo simbolo de otros modulos.",
        duplicates="0",
        label2="Is Main Module",
        ea_localid="449",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Whether the translations in this Module may resolve the strings of same symbol in other modules.",
        ea_guid="{D0F2FC43-AAA2-4b9a-9A44-8E7AB7C5BAAA}",
        exclude_from_values_form="True",
        scale="0",
        default="False",
        label="Es Modulo Principal",
        length="0",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        position="1",
        owner_class_name="TRAModulo",
        exclude_from_views="[ 'Textual', 'Tabular',  'General', ]"
    ),

    ComputedField(
        name='pathDelRaiz',
        widget=ComputedField._properties['widget'](
            label="Path del Raiz",
            label2="Root's Path",
            description="Path del Catalogo raiz de este elemento.",
            description2="This element's root Catalog path.",
            label_msgid='gvSIGi18n_TRAModulo_attr_pathDelRaiz_label',
            description_msgid='gvSIGi18n_TRAModulo_attr_pathDelRaiz_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Path del Catalogo raiz de este elemento.",
        duplicates="0",
        label2="Root's Path",
        ea_localid="1141",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="This element's root Catalog path.",
        ea_guid="{4F03D47F-A548-417a-A689-7964B16214FC}",
        scale="0",
        expression="context.fPathDelRaiz()",
        label="Path del Raiz",
        length="0",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        position="0",
        owner_class_name="TRAModulo",
        exclude_from_views="[ 'Textual', 'Tabular',  ]"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAModulo_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAArquetipo, 'schema', Schema(())).copy() + \
    getattr(TRAModulo_Operaciones, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAModulo(OrderedBaseFolder, TRAArquetipo, TRAModulo_Operaciones):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAArquetipo,'__implements__',()),) + (getattr(TRAModulo_Operaciones,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Modulo'

    meta_type = 'TRAModulo'
    portal_type = 'TRAModulo'
    use_folder_tabs = 0

    allowed_content_types = [] + list(getattr(TRAArquetipo, 'allowed_content_types', [])) + list(getattr(TRAModulo_Operaciones, 'allowed_content_types', []))
    filter_content_types = 1
    global_allow = 0
    content_icon = 'tramodulo.gif'
    immediate_view = 'Tabular'
    default_view = 'Tabular'
    suppl_views = ['Tabular',]
    typeDescription = "Uno de los Modulos del producto a traducir."
    typeDescMsgId =  'gvSIGi18n_TRAModulo_help'
    archetype_name2 = 'Module'
    typeDescription2 = '''One of the Modules in the product to translate.'''
    archetype_name_msgid = 'gvSIGi18n_TRAModulo_label'
    factory_methods = None
    factory_enablers = None
    allow_discussion = False


    actions =  (


       {'action': "string:${object_url}/sharing",
        'category': "object",
        'id': 'local_roles',
        'name': 'Sharing',
        'permissions': ("Manage properties",),
        'condition': 'python:1'
       },


       {'action': "string:${object_url}/folder_listing",
        'category': "folder",
        'id': 'folderlisting',
        'name': 'Folder Listing',
        'permissions': ("View",),
        'condition': 'python:0'
       },


       {'action': "string:${object_url}/reference_graph",
        'category': "object",
        'id': 'references',
        'name': 'References',
        'permissions': ("Modify portal content",),
        'condition': 'python:0'
       },


       {'action': "string:$object_url/content_status_history",
        'category': "object",
        'id': 'content_status_history',
        'name': 'State',
        'permissions': ("View",),
        'condition': 'python:0'
       },


       {'action': "string:${object_url}/sharing",
        'category': "object",
        'id': 'local_roles',
        'name': 'Sharing',
        'permissions': ("Manage properties",),
        'condition': 'python:object.fRoleQuery_IsCoordinator()'
       },


       {'action': "string:${object_url}/Tabular",
        'category': "object",
        'id': 'view',
        'name': 'View',
        'permissions': ("View",),
        'condition': 'python:1'
       },


       {'action': "string:$object_url/Editar",
        'category': "object",
        'id': 'edit',
        'name': 'Edit',
        'permissions': ("Modify portal content",),
        'condition': 'python:1'
       },


    )

    _at_rename_after_creation = True

    schema = TRAModulo_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('manage_afterAdd')
    def manage_afterAdd(self,item,container):
        """
        """
        
        return TRAArquetipo.manage_afterAdd( self, item, container)

    security.declarePublic('manage_beforeDelete')
    def manage_beforeDelete(self,item,container):
        """
        """
        
        return TRAArquetipo.manage_beforeDelete( self, item, container)
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata']:
            a['visible'] = 0
    return fti

registerType(TRAModulo, PROJECTNAME)
# end of class TRAModulo

##code-section module-footer #fill in your manual code here
##/code-section module-footer



