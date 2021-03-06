# -*- coding: utf-8 -*-
#
# File: TRACadena.py
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
from Products.gvSIGi18n.TRAArquetipo import TRAArquetipo
from TRACadena_Operaciones import TRACadena_Operaciones
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from TRAElemento_Operaciones import TRAElemento_Operaciones

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='simbolo',
        widget=StringWidget(
            label="Simbolo",
            label2="Symbol",
            description="El simbolo original que identifica la Cadena a traducir.",
            description2="The original symbol identifying the string to be translated.",
            label_msgid='gvSIGi18n_TRACadena_attr_simbolo_label',
            description_msgid='gvSIGi18n_TRACadena_attr_simbolo_help',
            i18n_domain='gvSIGi18n',
        ),
        description="El simbolo original que identifica la Cadena a traducir.",
        searchable=0,
        duplicates="0",
        label2="Symbol",
        ea_localid="297",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="The original symbol identifying the string to be translated.",
        ea_guid="{D7A26052-9642-4336-9E66-D7C7AAD9D7E6}",
        scale="0",
        label="Simbolo",
        length="0",
        containment="Not Specified",
        position="5",
        owner_class_name="TRACadena"
    ),

    StringField(
        name='estadoCadena',
        widget=SelectionWidget(
            label="Estado de la Cadena",
            label2="String State",
            description="Estado de la Cadena, como Activa o Inactiva.",
            description2="String State, as Active or Inactive.",
            label_msgid='gvSIGi18n_TRACadena_attr_estadoCadena_label',
            description_msgid='gvSIGi18n_TRACadena_attr_estadoCadena_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Estado de la Cadena, como Activa o Inactiva.",
        vocabulary=['Inactiva','Activa',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRACadena_attr_estadoCadena_option_Inactiva', 'gvSIGi18n_TRACadena_attr_estadoCadena_option_Activa'],
        label2="String State",
        ea_localid="298",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="String State, as Active or Inactive.",
        ea_guid="{C3189402-771A-40ed-89DA-0B48A0192124}",
        vocabulary2=['Inactive','Active',],
        scale="0",
        default='Activa',
        label="Estado de la Cadena",
        length="0",
        containment="Not Specified",
        position="0",
        owner_class_name="TRACadena"
    ),

    StringField(
        name='fechaCreacionTextual',
        widget=StringWidget(
            label="Fecha de Creacion como texto",
            label2="Creation Date as text",
            description="Representacion textual de la fecha en que se creo la cadena a traducir.",
            description2="Textual representation of the date when the String was first created.",
            label_msgid='gvSIGi18n_TRACadena_attr_fechaCreacionTextual_label',
            description_msgid='gvSIGi18n_TRACadena_attr_fechaCreacionTextual_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Representacion textual de la fecha en que se creo la cadena a traducir.",
        searchable=0,
        duplicates="0",
        label2="Creation Date as text",
        ea_localid="1334",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Textual representation of the date when the String was first created.",
        ea_guid="{37522DDE-9593-4f36-8686-C889D5C6B928}",
        scale="0",
        label="Fecha de Creacion como texto",
        length="0",
        containment="Not Specified",
        position="2",
        owner_class_name="TRACadena"
    ),

    StringField(
        name='usuarioCreador',
        widget=StringWidget(
            label="Usuario Creador",
            label2="Creator user",
            description="Usuario que creo o importo la cadena a traducir.",
            description2="User who created or imported the string to be translated.",
            label_msgid='gvSIGi18n_TRACadena_attr_usuarioCreador_label',
            description_msgid='gvSIGi18n_TRACadena_attr_usuarioCreador_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Usuario que creo o importo la cadena a traducir.",
        searchable=0,
        duplicates="0",
        label2="Creator user",
        ea_localid="300",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="User who created or imported the string to be translated.",
        ea_guid="{419A6822-511F-48d5-9D48-A75E8E596478}",
        scale="0",
        label="Usuario Creador",
        length="0",
        containment="Not Specified",
        position="6",
        owner_class_name="TRACadena"
    ),

    StringField(
        name='fechaCancelacionTextual',
        widget=StringWidget(
            label="Fecha de Cancelacion",
            label2="Cancelation Date",
            description="La fecha en que la cadena fue cancelada, de forma que no vuelva a ser considerada para su traduccion.",
            description2="The date when the String was cancelled, such that the string won't be considered again for translation.",
            label_msgid='gvSIGi18n_TRACadena_attr_fechaCancelacionTextual_label',
            description_msgid='gvSIGi18n_TRACadena_attr_fechaCancelacionTextual_help',
            i18n_domain='gvSIGi18n',
        ),
        description="La fecha en que la cadena fue cancelada, de forma que no vuelva a ser considerada para su traduccion.",
        searchable=0,
        duplicates="0",
        label2="Cancelation Date",
        ea_localid="1338",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="The date when the String was cancelled, such that the string won't be considered again for translation.",
        ea_guid="{897F7F5D-B75C-4084-8D79-B7639A72865C}",
        scale="0",
        label="Fecha de Cancelacion",
        length="0",
        containment="Not Specified",
        position="1",
        owner_class_name="TRACadena"
    ),

    StringField(
        name='nombresModulos',
        widget=StringWidget(
            label="Modulos",
            label2="Modules",
            description="Nombres de los Modulos en los que se usa esta cadena.",
            description2="Names of the Modules using this String.",
            label_msgid='gvSIGi18n_TRACadena_attr_nombresModulos_label',
            description_msgid='gvSIGi18n_TRACadena_attr_nombresModulos_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Nombres de los Modulos en los que se usa esta cadena.",
        searchable=0,
        duplicates="0",
        label2="Modules",
        ea_localid="757",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Names of the Modules using this String.",
        ea_guid="{0CFE460B-2B53-47e7-A1D9-72BDFAC41336}",
        scale="0",
        label="Modulos",
        length="0",
        containment="Not Specified",
        position="3",
        owner_class_name="TRACadena"
    ),

    StringField(
        name='referenciasFuentes',
        widget=StringWidget(
            label="Referencias a fuentes",
            label2="Source references",
            description="Referencias a codigo fuente donde aparece esta cadena.",
            description2="References to source code where the string is used.",
            label_msgid='gvSIGi18n_TRACadena_attr_referenciasFuentes_label',
            description_msgid='gvSIGi18n_TRACadena_attr_referenciasFuentes_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Referencias a codigo fuente donde aparece esta cadena.",
        searchable=0,
        duplicates="0",
        label2="Source references",
        ea_localid="1491",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="References to source code where the string is used.",
        ea_guid="{11E67965-20C0-4a3e-B113-5A320582937E}",
        scale="0",
        label="Referencias a fuentes",
        length="0",
        containment="Not Specified",
        position="4",
        owner_class_name="TRACadena"
    ),

    ComputedField(
        name='traducciones',
        widget=ComputedWidget(
            label="Traducciones",
            label2="Translations",
            description="Traducciones de una de las Cadenas los varios Idiomas.",
            description2="Translations of one string to the various languages.",
            label_msgid='gvSIGi18n_TRACadena_contents_traducciones_label',
            description_msgid='gvSIGi18n_TRACadena_contents_traducciones_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=False,
        label2='Translations',
        additional_columns=['codigoIdiomaEnGvSIG', 'estadoTraduccion', 'fechaTraduccion', 'usuarioTraductor', 'fechaRevision', 'usuarioRevisor', 'fechaDefinitivo', 'usuarioCoordinador'],
        label='Traducciones',
        represents_aggregation=True,
        description2='Translations of one string to the various languages.',
        multiValued=1,
        owner_class_name="TRACadena",
        expression="context.objectValues(['TRATraduccion'])",
        computed_types=['TRATraduccion'],
        non_framework_elements=False,
        description='Traducciones de una de las Cadenas los varios Idiomas.'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRACadena_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAArquetipo, 'schema', Schema(())).copy() + \
    getattr(TRACadena_Operaciones, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRACadena(OrderedBaseFolder, TRAArquetipo, TRACadena_Operaciones):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAArquetipo,'__implements__',()),) + (getattr(TRACadena_Operaciones,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Cadena'

    meta_type = 'TRACadena'
    portal_type = 'TRACadena'
    use_folder_tabs = 0

    allowed_content_types = ['TRATraduccion'] + list(getattr(TRAArquetipo, 'allowed_content_types', [])) + list(getattr(TRACadena_Operaciones, 'allowed_content_types', []))
    filter_content_types             = 1
    global_allow                     = 0
    content_icon = 'tracadena.gif'
    immediate_view                   = 'Tabular'
    default_view                     = 'Tabular'
    suppl_views                      = ['Tabular',]
    typeDescription                  = "Una de las cadenas originales del producto a traducir, identificada por el simbolo original."
    typeDescMsgId                    =  'gvSIGi18n_TRACadena_help'
    archetype_name2                  = 'String to translate'
    typeDescription2                 = '''One of the original product strings to translate, identified by a the original symbol string.'''
    archetype_name_msgid             = 'gvSIGi18n_TRACadena_label'
    factory_methods                  = None
    factory_enablers                 = None
    propagate_delete_impact_to       = None
    allow_discussion = 0


    actions =  (


       {'action': "string:${object_url}/Tabular",
        'category': "object",
        'id': 'view',
        'name': 'View',
        'permissions': ("View",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'View_any_TRA_element')"""
       },


       {'action': "string:$object_url/Editar",
        'category': "object",
        'id': 'edit',
        'name': 'Edit',
        'permissions': ("Modify portal content",),
        'condition': """python:0"""
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

    schema = TRACadena_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('at_post_edit_script')
    def at_post_edit_script(self):
        """
        """
        
        return self.pPropagarCambioDeEstadoATraducciones()

    security.declarePublic('cb_isCopyable')
    def cb_isCopyable(self):
        """
        """
        
        return False

    security.declarePublic('fIsActive')
    def fIsActive(self):
        """
        """
        
        return self.getEstadoCadena() =='Activa'

    security.declarePublic('fIsInactive')
    def fIsInactive(self):
        """
        """
        
        return self.getEstadoCadena() =='Inactiva'

    security.declarePublic('manage_afterAdd')
    def manage_afterAdd(self,item,container):
        """
        """
        
        return TRACadena_Operaciones.pHandle_manage_afterAdd( self, item, container)

    security.declarePublic('reindexObject')
    def reindexObject(self,idxs=[]):
        """
        """
        
        return TRACadena_Operaciones.pHandle_reindexObject( self, idxs)

    security.declarePublic('displayContentsTab')
    def displayContentsTab(self):
        """
        """
        
        return False

    security.declarePublic('fVocabulary_NombresModulos')
    def fVocabulary_NombresModulos(self):
        """
        """
        
        return self.getCatalogo().fTodosModulosVocabulary()

    security.declarePublic('manage_beforeDelete')
    def manage_beforeDelete(self,item,container):
        """
        """
        
        return TRAArquetipo.manage_beforeDelete( self, item, container)

    security.declarePublic('fAllowExport')
    def fAllowExport(self):
        """
        """
        
        return False

    security.declarePublic('fAllowImport')
    def fAllowImport(self):
        """
        """
        
        return False

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
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata', 'sharing', 'folderContents']:
            a['visible'] = 0
    return fti

registerType(TRACadena, PROJECTNAME)
# end of class TRACadena

##code-section module-footer #fill in your manual code here
##/code-section module-footer



