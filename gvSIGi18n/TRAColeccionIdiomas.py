# -*- coding: utf-8 -*-
#
# File: TRAColeccionIdiomas.py
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
from TRAColeccionIdiomas_Operaciones import TRAColeccionIdiomas_Operaciones
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from TRAElemento_Operaciones import TRAElemento_Operaciones

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    ComputedField(
        name='idiomas',
        widget=ComputedWidget(
            label="Idiomas",
            label2="Languages",
            description="Idiomas a los que se desea traducir las cadena.",
            description2="Languages to translate the strings into.",
            label_msgid='gvSIGi18n_TRAColeccionIdiomas_contents_idiomas_label',
            description_msgid='gvSIGi18n_TRAColeccionIdiomas_contents_idiomas_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=False,
        label2='Languages',
        additional_columns=['codigoIdiomaEnGvSIG', 'codigoInternacionalDeIdioma', 'nombreNativoDeIdioma'],
        label='Idiomas',
        represents_aggregation=True,
        description2='Languages to translate the strings into.',
        multiValued=1,
        owner_class_name="TRAColeccionIdiomas",
        expression="context.objectValues(['TRAIdioma'])",
        computed_types=['TRAIdioma'],
        non_framework_elements=False,
        description='Idiomas a los que se desea traducir las cadena.'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAColeccionIdiomas_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAColeccionArquetipos, 'schema', Schema(())).copy() + \
    getattr(TRAColeccionIdiomas_Operaciones, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAColeccionIdiomas(OrderedBaseFolder, TRAColeccionArquetipos, TRAColeccionIdiomas_Operaciones):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAColeccionArquetipos,'__implements__',()),) + (getattr(TRAColeccionIdiomas_Operaciones,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Coleccion de Idiomas'

    meta_type = 'TRAColeccionIdiomas'
    portal_type = 'TRAColeccionIdiomas'


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



    allowed_content_types = ['TRAIdioma'] + list(getattr(TRAColeccionArquetipos, 'allowed_content_types', [])) + list(getattr(TRAColeccionIdiomas_Operaciones, 'allowed_content_types', []))
    filter_content_types             = 1
    global_allow                     = 0
    #content_icon = 'TRAColeccionIdiomas.gif'
    immediate_view                   = 'Tabular'
    default_view                     = 'Tabular'
    suppl_views                      = ['Tabular',]
    typeDescription                  = "Coleccion de idiomas a los que se desea traducir las cadenas."
    typeDescMsgId                    =  'gvSIGi18n_TRAColeccionIdiomas_help'
    archetype_name2                  = 'Languages collection'
    typeDescription2                 = '''Collection of languages to translate the strings into.'''
    archetype_name_msgid             = 'gvSIGi18n_TRAColeccionIdiomas_label'
    factory_methods                  = { 'TRAIdioma' : 'fCrearIdioma',}
    factory_enablers                 = { 'TRAIdioma' : [ 'fUseCaseCheckDoableFactory', 'Create_TRAIdioma',]}
    propagate_delete_impact_to       = None
    allow_discussion = False


    actions =  (


       {'action': "string:${object_url}/sharing",
        'category': "object",
        'id': 'local_roles',
        'name': 'Sharing',
        'permissions': ("Manage properties",),
        'condition': """python:object.fAllowWrite() and object.fRoleQuery_IsManagerOrCoordinator()"""
       },


       {'action': "string:${object_url}/TRACrear_Idioma",
        'category': "object_buttons",
        'id': 'CreateLanguage',
        'name': 'Create Language',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fUseCaseCheckDoable( 'Create_TRAIdioma')"""
       },


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

    schema = TRAColeccionIdiomas_schema

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

    security.declarePublic('manage_pasteObjects')
    def manage_pasteObjects(self,cb_copy_data,REQUEST):
        """
        """
        
        return self.pHandle_manage_pasteObjects( cb_copy_data, REQUEST)

    security.declarePublic('displayContentsTab')
    def displayContentsTab(self):
        """
        """
        
        return False

    security.declarePublic('fExtraLinks')
    def fExtraLinks(self):
        """
        """
        
        return TRAElemento_Operaciones.fExtraLinks( self)
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata', 'folderContents']:
            a['visible'] = 0
    return fti

registerType(TRAColeccionIdiomas, PROJECTNAME)
# end of class TRAColeccionIdiomas

##code-section module-footer #fill in your manual code here
##/code-section module-footer



