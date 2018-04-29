# -*- coding: utf-8 -*-
#
# File: TRASimbolosOrdenados.py
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
from Products.gvSIGi18n.TRAArquetipo import TRAArquetipo
from TRASimbolosOrdenados_Operaciones import TRASimbolosOrdenados_Operaciones
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from TRAElemento_Operaciones import TRAElemento_Operaciones
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    TextField(
        name='modulosYSimbolosCadenasOrdenados',
        widget=TextAreaWidget(
            label="Modulos y Simbolos Cadenas ordenados",
            label2="Module names and Sorted String symbols",
            description="Nombres de Modulos y los Simbolos de las cadenas a traducir en el modulo, ordenados.",
            description2="Module names and the Symbols of strings to be translated in the module, sorted.",
            label_msgid='gvSIGi18n_TRASimbolosOrdenados_attr_modulosYSimbolosCadenasOrdenados_label',
            description_msgid='gvSIGi18n_TRASimbolosOrdenados_attr_modulosYSimbolosCadenasOrdenados_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Nombres de Modulos y los Simbolos de las cadenas a traducir en el modulo, ordenados.",
        duplicates="0",
        label2="Module names and Sorted String symbols",
        ea_localid="885",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Module names and the Symbols of strings to be translated in the module, sorted.",
        ea_guid="{0151EBEF-7A6C-4482-863B-4CE43ABC1EBD}",
        scale="0",
        label="Modulos y Simbolos Cadenas ordenados",
        length="0",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        position="1",
        owner_class_name="TRASimbolosOrdenados"
    ),

    TextField(
        name='simbolosCadenasOrdenados',
        widget=TextAreaWidget(
            label="Simbolos Cadenas ordenados",
            label2="Sorted String symbols",
            description="Simbolos de las cadenas a traducir, ordenados.",
            description2="Symbols of strings to be translated, sorted.",
            label_msgid='gvSIGi18n_TRASimbolosOrdenados_attr_simbolosCadenasOrdenados_label',
            description_msgid='gvSIGi18n_TRASimbolosOrdenados_attr_simbolosCadenasOrdenados_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Simbolos de las cadenas a traducir, ordenados.",
        duplicates="0",
        label2="Sorted String symbols",
        ea_localid="304",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Symbols of strings to be translated, sorted.",
        ea_guid="{2DEB38F4-8102-464c-9DA0-02070A9777D2}",
        scale="0",
        label="Simbolos Cadenas ordenados",
        length="0",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        position="2",
        owner_class_name="TRASimbolosOrdenados"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRASimbolosOrdenados_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAArquetipo, 'schema', Schema(())).copy() + \
    getattr(TRASimbolosOrdenados_Operaciones, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRASimbolosOrdenados(OrderedBaseFolder, TRAArquetipo, TRASimbolosOrdenados_Operaciones):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAArquetipo,'__implements__',()),) + (getattr(TRASimbolosOrdenados_Operaciones,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Simbolos Ordenados'

    meta_type = 'TRASimbolosOrdenados'
    portal_type = 'TRASimbolosOrdenados'
    use_folder_tabs = 0

    allowed_content_types = [] + list(getattr(TRAArquetipo, 'allowed_content_types', [])) + list(getattr(TRASimbolosOrdenados_Operaciones, 'allowed_content_types', []))
    filter_content_types             = 1
    global_allow                     = 0
    content_icon = 'trasimbolosordenados.gif'
    immediate_view                   = 'Tabular'
    default_view                     = 'Tabular'
    suppl_views                      = ['Tabular',]
    typeDescription                  = "Contiene la lisa ordenada de simbolos, agrupados por modulos."
    typeDescMsgId                    =  'gvSIGi18n_TRASimbolosOrdenados_help'
    archetype_name2                  = 'Ordered Symbols'
    typeDescription2                 = '''Stores the ordered list of symbols, grouped by modules.'''
    archetype_name_msgid             = 'gvSIGi18n_TRASimbolosOrdenados_label'
    factory_methods                  = None
    factory_enablers                 = None
    propagate_delete_impact_to       = None
    allow_discussion = False


    actions =  (


       {'action': "string:$object_url/Editar",
        'category': "object",
        'id': 'edit',
        'name': 'Edit',
        'permissions': ("Modify portal content",),
        'condition': """python:0"""
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

    schema = TRASimbolosOrdenados_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('cb_isCopyable')
    def cb_isCopyable(self):
        """
        """
        
        return False

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

    security.declarePublic('fIsCacheable')
    def fIsCacheable(self):
        """
        """
        
        return True

    security.declarePublic('manage_afterAdd')
    def manage_afterAdd(self,item,container):
        """
        """
        
        return TRAArquetipo.manage_afterAdd( self, item, container)

    security.declarePublic('fAllowExport')
    def fAllowExport(self):
        """
        """
        
        return False

    security.declarePublic('manage_beforeDelete')
    def manage_beforeDelete(self,item,container):
        """
        """
        
        return TRAArquetipo.manage_beforeDelete( self, item, container)

    security.declarePublic('manage_pasteObjects')
    def manage_pasteObjects(self,cb_copy_data,REQUEST):
        """
        """
        
        return self

    security.declarePublic('fAllowImport')
    def fAllowImport(self):
        """
        """
        
        return False
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata', 'folderContents']:
            a['visible'] = 0
    return fti

registerType(TRASimbolosOrdenados, PROJECTNAME)
# end of class TRASimbolosOrdenados

##code-section module-footer #fill in your manual code here
##/code-section module-footer



