# -*- coding: utf-8 -*-
#
# File: TRAColeccionArquetipos.py
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
from Products.gvSIGi18n.TRAElemento import TRAElemento
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    ComputedField(
        name='pathDelRaiz',
        widget=ComputedField._properties['widget'](
            label="Path del Raiz",
            label2="Root's Path",
            description="Path del Catalogo raiz de este elemento.",
            description2="This element's root Catalog path.",
            label_msgid='gvSIGi18n_TRAColeccionArquetipos_attr_pathDelRaiz_label',
            description_msgid='gvSIGi18n_TRAColeccionArquetipos_attr_pathDelRaiz_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Path del Catalogo raiz de este elemento.",
        duplicates="0",
        label2="Root's Path",
        ea_localid="1153",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="This element's root Catalog path.",
        ea_guid="{B7179848-3F34-4d34-853D-337C1259FDD4}",
        scale="0",
        expression="context.fPathDelRaiz()",
        label="Path del Raiz",
        length="0",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        position="0",
        owner_class_name="TRAColeccionArquetipos",
        exclude_from_views="[ 'Textual', 'Tabular',  ]"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAColeccionArquetipos_schema = getattr(TRAElemento, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAColeccionArquetipos(TRAElemento):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(TRAElemento,'__implements__',()),)

    allowed_content_types = [] + list(getattr(TRAElemento, 'allowed_content_types', []))

    actions =  (


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
        'condition': 'python:0'
       },


       {'action': "string:${object_url}/sharing",
        'category': "object",
        'id': 'local_roles',
        'name': 'Sharing',
        'permissions': ("Manage properties",),
        'condition': 'python:0'
       },


       {'action': "string:$object_url/content_status_history",
        'category': "object",
        'id': 'content_status_history',
        'name': 'State',
        'permissions': ("View",),
        'condition': 'python:0'
       },


    )

    _at_rename_after_creation = True

    schema = TRAColeccionArquetipos_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('getEsColeccion')
    def getEsColeccion(self):
        """
        """
        
        return True

    security.declarePublic('manage_afterAdd')
    def manage_afterAdd(self,item,container):
        """
        """
        
        return TRAElemento.manage_afterAdd( self, item, container)

    security.declarePublic('manage_beforeDelete')
    def manage_beforeDelete(self,item,container):
        """
        """
        
        return TRAElemento.manage_beforeDelete( self, item, container)
# end of class TRAColeccionArquetipos

##code-section module-footer #fill in your manual code here
##/code-section module-footer



