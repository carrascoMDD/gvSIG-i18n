# -*- coding: utf-8 -*-
#
# File: TRAColeccionSolicitudesCadenas.py
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
from Products.gvSIGi18n.TRAColeccionSolicitudesCadenas_Operaciones import TRAColeccionSolicitudesCadenas_Operaciones
from Products.gvSIGi18n.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    ComputedField(
        name='solicitudesCadenas',
        widget=ComputedWidget(
            label="Solicitudes de creacion de Cadenas",
            label2="String creation Requests",
            description="Solicitudes realizadas por los desarrolladores, para crear nuevas cadenas.",
            description2="Requests by developers to create new strings.",
            label_msgid='gvSIGi18n_TRAColeccionSolicitudesCadenas_contents_solicitudesCadenas_label',
            description_msgid='gvSIGi18n_TRAColeccionSolicitudesCadenas_contents_solicitudesCadenas_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=False,
        label2='String creation Requests',
        additional_columns=['simbolo', 'estadoSolicitudCadena', 'codigoIdiomaPrincipal', 'cadenaTraducidaAIdiomaPrincipal', 'codigoIdiomaReferencia', 'cadenaTraducidaAIdiomaReferencia'],
        label='Solicitudes de creacion de Cadenas',
        description2='Requests by developers to create new strings.',
        multiValued=1,
        factory_views={ 'TRASolicitudCadena' : 'TRACrear_SolicitudCadena',},
        owner_class_name="TRAColeccionSolicitudesCadenas",
        expression="context.objectValues(['TRASolicitudCadena'])",
        computed_types=['TRASolicitudCadena'],
        represents_aggregation=True,
        description='Solicitudes realizadas por los desarrolladores, para crear nuevas cadenas.'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAColeccionSolicitudesCadenas_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAColeccionArquetipos, 'schema', Schema(())).copy() + \
    getattr(TRAColeccionSolicitudesCadenas_Operaciones, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAColeccionSolicitudesCadenas(OrderedBaseFolder, TRAColeccionArquetipos, TRAColeccionSolicitudesCadenas_Operaciones):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAColeccionArquetipos,'__implements__',()),) + (getattr(TRAColeccionSolicitudesCadenas_Operaciones,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Coleccion de Solicitudes de creacion de Cadenas'

    meta_type = 'TRAColeccionSolicitudesCadenas'
    portal_type = 'TRAColeccionSolicitudesCadenas'
    allowed_content_types = ['TRASolicitudCadena'] + list(getattr(TRAColeccionArquetipos, 'allowed_content_types', [])) + list(getattr(TRAColeccionSolicitudesCadenas_Operaciones, 'allowed_content_types', []))
    filter_content_types = 1
    global_allow = 0
    #content_icon = 'TRAColeccionSolicitudesCadenas.gif'
    immediate_view = 'Tabular'
    default_view = 'Tabular'
    suppl_views = ['Tabular',]
    typeDescription = "Coleccion de solicitudes realizadas por los desarrolladores, para crear nuevas cadenas."
    typeDescMsgId =  'gvSIGi18n_TRAColeccionSolicitudesCadenas_help'
    archetype_name2 = 'Strings creation request collection'
    typeDescription2 = '''Collection of requests by developers to create new strings.'''
    archetype_name_msgid = 'gvSIGi18n_TRAColeccionSolicitudesCadenas_label'
    factory_methods = { 'TRASolicitudCadena' : 'fCrearSolicitudCadena',}
    factory_enablers = None
    allow_discussion = False


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


       {'action': "string:${object_url}/sharing",
        'category': "object",
        'id': 'local_roles',
        'name': 'Sharing',
        'permissions': ("Manage properties",),
        'condition': 'python:0'
       },


    )

    _at_rename_after_creation = True

    schema = TRAColeccionSolicitudesCadenas_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('manage_beforeDelete')
    def manage_beforeDelete(self,item,container):
        """
        """
        
        return TRAColeccionArquetipos.manage_beforeDelete( self, item, container)

    security.declarePublic('manage_afterAdd')
    def manage_afterAdd(self,item,container):
        """
        """
        
        return TRAColeccionArquetipos.manage_afterAdd( self, item, container)
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata', 'sharing']:
            a['visible'] = 0
    return fti

registerType(TRAColeccionSolicitudesCadenas, PROJECTNAME)
# end of class TRAColeccionSolicitudesCadenas

##code-section module-footer #fill in your manual code here
##/code-section module-footer


