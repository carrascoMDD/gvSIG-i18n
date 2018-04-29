# -*- coding: utf-8 -*-
#
# File: TRAColeccionProgresos.py
#
# Copyright (c) 2008, 2009, 2010, 2011 Conselleria de Infraestructuras y
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
from Products.gvSIGi18n.TRAColeccionArquetipos import TRAColeccionArquetipos
from TRAColeccionProgresos_Operaciones import TRAColeccionProgresos_Operaciones
from Products.gvSIGi18n.TRAConRegistroActividad import TRAConRegistroActividad
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from TRAElemento_Operaciones import TRAElemento_Operaciones

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    ComputedField(
        name='progresos',
        widget=ComputedWidget(
            label="Progresos",
            label2="Progresses",
            description="Informes de Progreso acerca de Procesos de larga duracion",
            description2="Progress reports about long-lived processes",
            label_msgid='gvSIGi18n_TRAColeccionProgresos_contents_progresos_label',
            description_msgid='gvSIGi18n_TRAColeccionProgresos_contents_progresos_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=False,
        label2='Progresses',
        additional_columns=['tipoProceso', 'estadoProceso', 'haComenzado', 'haCompletadoConExito'],
        label='Progresos',
        represents_aggregation=True,
        description2='Progress reports about long-lived processes',
        multiValued=1,
        factory_views={ 'TRAProgreso' : 'TRACrear_Progreso',},
        owner_class_name="TRAColeccionProgresos",
        expression="context.objectValues(['TRAProgreso'])",
        computed_types=['TRAProgreso'],
        non_framework_elements=False,
        description='Informes de Progreso acerca de Procesos de larga duracion'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAColeccionProgresos_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAColeccionArquetipos, 'schema', Schema(())).copy() + \
    getattr(TRAColeccionProgresos_Operaciones, 'schema', Schema(())).copy() + \
    getattr(TRAConRegistroActividad, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAColeccionProgresos(OrderedBaseFolder, TRAColeccionArquetipos, TRAColeccionProgresos_Operaciones, TRAConRegistroActividad):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAColeccionArquetipos,'__implements__',()),) + (getattr(TRAColeccionProgresos_Operaciones,'__implements__',()),) + (getattr(TRAConRegistroActividad,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Coleccion de Progresos'

    meta_type = 'TRAColeccionProgresos'
    portal_type = 'TRAColeccionProgresos'


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

    allowed_content_types = ['TRAProgreso'] + list(getattr(TRAColeccionArquetipos, 'allowed_content_types', [])) + list(getattr(TRAColeccionProgresos_Operaciones, 'allowed_content_types', [])) + list(getattr(TRAConRegistroActividad, 'allowed_content_types', []))
    filter_content_types             = 1
    global_allow                     = 0
    #content_icon = 'TRAColeccionProgresos.gif'
    immediate_view                   = 'Tabular'
    default_view                     = 'Tabular'
    suppl_views                      = ['Tabular',]
    typeDescription                  = "Coleccion de informes de Progreso acerca de Procesos de larga duracion"
    typeDescMsgId                    =  'gvSIGi18n_TRAColeccionProgresos_help'
    archetype_name2                  = 'Progresses Collection'
    typeDescription2                 = '''Collection of Progress reports about long-lived processes'''
    archetype_name_msgid             = 'gvSIGi18n_TRAColeccionProgresos_label'
    factory_methods                  = { 'TRAProgreso' : 'fCrearProgreso',}
    factory_enablers                 = { 'TRAProgreso' : [ 'fUseCaseCheckDoableFactory', 'Create_TRAProgreso',]}
    propagate_delete_impact_to       = None
    allow_discussion = False


    actions =  (


       {'action': "string:${object_url}/TRACrear_Informe",
        'category': "object_buttons",
        'id': 'TRACreateInforme',
        'name': 'Create Report',
        'permissions': ("Modify portal content",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Create_TRAInforme')"""
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
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'View_any_TRA_element')"""
       },


       {'action': "string:${object_url}/MDDChanges",
        'category': "object_buttons",
        'id': 'mddchanges',
        'name': 'Changes',
        'permissions': ("View",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Changes_on_any_TRA_element')"""
       },


       {'action': "string:$object_url/Editar",
        'category': "object",
        'id': 'edit',
        'name': 'Edit',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fAllowWrite() and object.TRAgvSIGi18n_tool.fRoleQuery_IsAnyRol( object, [ 'Manager', 'Owner', 'TRACreator', 'TRAManager', 'TRACoordinator',])"""
       },


       {'action': "string:${object_url}/TRAFlushCache_action",
        'category': "object_buttons",
        'id': 'tra_flushcache',
        'name': 'Flush',
        'permissions': ("View",),
        'condition': """python:object.TRAgvSIGi18n_tool.fRoleQuery_IsAnyRol( object, [ 'Manager', 'Owner', 'TRACreator', 'TRAManager', 'TRACoordinator',])"""
       },


       {'action': "string:${object_url}/TRAInventory_action",
        'category': "object_buttons",
        'id': 'TRA_inventario',
        'name': 'Inventory',
        'permissions': ("View",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Inventory_TRAElemento')"""
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
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Permissions_on_any_TRA_element')"""
       },


       {'action': "string:$object_url/content_status_history",
        'category': "object",
        'id': 'content_status_history',
        'name': 'State',
        'permissions': ("View",),
        'condition': """python:0"""
       },


       {'action': "string:${object_url}/TRARecatalog_action",
        'category': "object_buttons",
        'id': 'TRA_recatalogar',
        'name': 'ReCatalog',
        'permissions': ("View",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'ReCatalog_TRAElemento')"""
       },


       {'action': "string:${object_url}/MDDCacheStatus/",
        'category': "object_buttons",
        'id': 'mddcachestatus',
        'name': 'Cache',
        'permissions': ("View",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'CacheStatus_on_any_TRA_element')"""
       },


       {'action': "string:${object_url}/TRAResetPermissions_action",
        'category': "object_buttons",
        'id': 'TRA_reestablecerpermisos',
        'name': 'Reset Permissions',
        'permissions': ("View",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'ResetPermissions_TRAElemento')"""
       },


       {'action': "string:${object_url}/TRAVerifyPermissions_action",
        'category': "object_buttons",
        'id': 'TRA_verificarpermisos',
        'name': 'Verify Permissions',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'VerifyPermissions_TRAElemento')"""
       },


    )

    _at_rename_after_creation = True

    schema = TRAColeccionProgresos_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

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

    security.declarePublic('fIsCacheable')
    def fIsCacheable(self):
        """
        """
        
        return True

    security.declarePublic('manage_pasteObjects')
    def manage_pasteObjects(self,cb_copy_data,REQUEST):
        """
        """
        
        return self

    security.declarePublic('fExtraLinks')
    def fExtraLinks(self):
        """
        """
        
        return TRAElemento_Operaciones.fExtraLinks( self)

    security.declarePublic('cb_isCopyable')
    def cb_isCopyable(self):
        """
        """
        
        return False
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata', 'sharing', 'folderContents']:
            a['visible'] = 0
    return fti

registerType(TRAColeccionProgresos, PROJECTNAME)
# end of class TRAColeccionProgresos

##code-section module-footer #fill in your manual code here
##/code-section module-footer



