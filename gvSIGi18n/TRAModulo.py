# -*- coding: utf-8 -*-
#
# File: TRAModulo.py
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
from Products.gvSIGi18n.TRAArquetipo import TRAArquetipo
from Products.gvSIGi18n.TRAConRegistroActividad import TRAConRegistroActividad
from TRAModulo_Operaciones import TRAModulo_Operaciones
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    BooleanField(
        name='permiteLeer',
        widget=BooleanField._properties['widget'](
            label="Permite ver Modulo",
            label2="Allow to see Module",
            description="Si Verdadero, entonces el usuario puede ver el modulo. Si Falso, entonces no puede ver el modulo. Puede ocurrir durante  procesos de importacion largos, o por indicacion del coordinador.",
            description2="If True, then the user may see  the module. If False, then the user can not see  the module. This may happen during long import processes or by coordinator request.",
            label_msgid='gvSIGi18n_TRAModulo_attr_permiteLeer_label',
            description_msgid='gvSIGi18n_TRAModulo_attr_permiteLeer_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, entonces el usuario puede ver el modulo. Si Falso, entonces no puede ver el modulo. Puede ocurrir durante  procesos de importacion largos, o por indicacion del coordinador.",
        duplicates="0",
        label2="Allow to see Module",
        ea_localid="1577",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="If True, then the user may see  the module. If False, then the user can not see  the module. This may happen during long import processes or by coordinator request.",
        ea_guid="{6607BD0C-0619-492e-B4EC-1BD206122B87}",
        read_only="True",
        scale="0",
        default="True",
        label="Permite ver Modulo",
        length="0",
        containment="Not Specified",
        position="3",
        owner_class_name="TRAModulo",
        exclude_from_exportconfig="True",
        exclude_from_copyconfig="True"
    ),

    BooleanField(
        name='permiteModificar',
        widget=BooleanField._properties['widget'](
            label="Permite Modificar Modulo",
            label2="Allow Changes to Module",
            description="Si Verdadero, entonces el usuario puede realizar los cambios a los que permite sus roles en el modulo. Si Falso, entonces no puede realizar cambios en el modulo. Puede ocurrir durante  procesos de importacion largos, o por indicacion del coordinador.",
            description2="If True, then the user may perform  the changes authorized by the roles held on the module. If False, then the user can not make changes to the module. This may happen during long import processe.",
            label_msgid='gvSIGi18n_TRAModulo_attr_permiteModificar_label',
            description_msgid='gvSIGi18n_TRAModulo_attr_permiteModificar_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, entonces el usuario puede realizar los cambios a los que permite sus roles en el modulo. Si Falso, entonces no puede realizar cambios en el modulo. Puede ocurrir durante  procesos de importacion largos, o por indicacion del coordinador.",
        duplicates="0",
        label2="Allow Changes to Module",
        ea_localid="1575",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="If True, then the user may perform  the changes authorized by the roles held on the module. If False, then the user can not make changes to the module. This may happen during long import processe.",
        ea_guid="{C9E9AD96-7852-49a3-BC7D-45130F8C9816}",
        read_only="True",
        scale="0",
        default="True",
        label="Permite Modificar Modulo",
        length="0",
        containment="Not Specified",
        position="2",
        owner_class_name="TRAModulo",
        exclude_from_exportconfig="True",
        exclude_from_copyconfig="True"
    ),

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
        description="Dato que aparece en los ficheros de exportacion de tipo GNUgettext PO, para identificar la aplicacion o modulo a que se aplican las traducciones.",
        searchable=0,
        duplicates="0",
        label2="Domain",
        ea_localid="1170",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Iinformation that appears in the exported files of GNUgettext PO format, to indicate the application or module to which the translations apply.",
        ea_guid="{70C5AFBA-F231-4944-BC58-D108311B4B10}",
        scale="0",
        label="Dominio",
        length="0",
        containment="Not Specified",
        position="1",
        owner_class_name="TRAModulo"
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
        position="0",
        owner_class_name="TRAModulo",
        exclude_from_views="[ 'Textual', 'Tabular',  'General', ]"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAModulo_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAArquetipo, 'schema', Schema(())).copy() + \
    getattr(TRAConRegistroActividad, 'schema', Schema(())).copy() + \
    getattr(TRAModulo_Operaciones, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAModulo(OrderedBaseFolder, TRAArquetipo, TRAConRegistroActividad, TRAModulo_Operaciones):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAArquetipo,'__implements__',()),) + (getattr(TRAConRegistroActividad,'__implements__',()),) + (getattr(TRAModulo_Operaciones,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Modulo'

    meta_type = 'TRAModulo'
    portal_type = 'TRAModulo'


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

    allowed_content_types = [] + list(getattr(TRAArquetipo, 'allowed_content_types', [])) + list(getattr(TRAConRegistroActividad, 'allowed_content_types', [])) + list(getattr(TRAModulo_Operaciones, 'allowed_content_types', []))
    filter_content_types             = 1
    global_allow                     = 0
    content_icon = 'tramodulo.gif'
    immediate_view                   = 'Tabular'
    default_view                     = 'Tabular'
    suppl_views                      = ['Tabular',]
    typeDescription                  = "Uno de los Modulos del producto a traducir."
    typeDescMsgId                    =  'gvSIGi18n_TRAModulo_help'
    archetype_name2                  = 'Module'
    typeDescription2                 = '''One of the Modules in the product to translate.'''
    archetype_name_msgid             = 'gvSIGi18n_TRAModulo_label'
    factory_methods                  = None
    factory_enablers                 = None
    propagate_delete_impact_to       = None
    allow_discussion = False


    actions =  (


       {'action': "string:${object_url}/TRARenombrar_Modulo",
        'category': "object_buttons",
        'id': 'TRARenameModule',
        'name': 'Rename Module',
        'permissions': ("Modify portal content",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Rename_TRAModulo')"""
       },


       {'action': "string:${object_url}/TRAEliminar_Modulo",
        'category': "object_buttons",
        'id': 'TRADeleteModule',
        'name': 'Delete Module',
        'permissions': ("Delete objects",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Delete_TRAModulo')"""
       },


       {'action': "string:$object_url/Editar",
        'category': "object",
        'id': 'edit',
        'name': 'Edit',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fUseCaseCheckDoable( 'Edit_TRAModulo')"""
       },


       {'action': "string:${object_url}/sharing",
        'category': "object",
        'id': 'local_roles',
        'name': 'Sharing',
        'permissions': ("Manage properties",),
        'condition': """python:object.fAllowWrite() and object.TRAgvSIGi18n_tool.fRoleQuery_IsAnyRol( object, [ 'Manager', 'Owner', 'TRACreator', 'TRAManager', 'TRACoordinator',])"""
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

    schema = TRAModulo_schema

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

    security.declarePublic('fAllowRead')
    def fAllowRead(self):
        """
        """
        
        return self.getPermiteLeer() and self.getCatalogo().fAllowRead()

    security.declarePublic('fAllowWrite')
    def fAllowWrite(self):
        """
        """
        
        return self.fAllowRead() and self.getPermiteModificar() and self.getCatalogo().fAllowWrite()

    security.declarePublic('fExtraLinks')
    def fExtraLinks(self):
        """
        """
        
        return TRAModulo_Operaciones.fExtraLinks( self)

    security.declarePublic('fIsCacheable')
    def fIsCacheable(self):
        """
        """
        
        return True

    security.declarePublic('fIsLocked')
    def fIsLocked(self):
        """
        """
        
        return not self.getPermiteModificar()

    security.declarePublic('fIsUnLocked')
    def fIsUnLocked(self):
        """
        """
        
        return self.getPermiteModificar()

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

    security.declarePublic('manage_pasteObjects')
    def manage_pasteObjects(self,cb_copy_data,REQUEST):
        """
        """
        
        return self
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata', 'folderContents']:
            a['visible'] = 0
    return fti

registerType(TRAModulo, PROJECTNAME)
# end of class TRAModulo

##code-section module-footer #fill in your manual code here
##/code-section module-footer



