# -*- coding: utf-8 -*-
#
# File: TRASolicitudCadena.py
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
from Products.gvSIGi18n.TRAConRegistroActividad import TRAConRegistroActividad
from TRASolicitudCadena_Operaciones import TRASolicitudCadena_Operaciones
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from TRAElemento_Operaciones import TRAElemento_Operaciones
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='simbolo',
        widget=StringWidget(
            label="Simbolo",
            label2="Symbol",
            description="El simbolo que identifica la Cadena que se solicita crear.",
            description2="The symbol identifying the string requested to be created,",
            label_msgid='gvSIGi18n_TRASolicitudCadena_attr_simbolo_label',
            description_msgid='gvSIGi18n_TRASolicitudCadena_attr_simbolo_help',
            i18n_domain='gvSIGi18n',
        ),
        description="El simbolo que identifica la Cadena que se solicita crear.",
        duplicates="0",
        label2="Symbol",
        ea_localid="1516",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="The symbol identifying the string requested to be created,",
        ea_guid="{C13920DA-0B81-4b5e-82F9-B5202CB599CE}",
        read_only="True",
        scale="0",
        label="Simbolo",
        length="0",
        containment="Not Specified",
        position="9",
        owner_class_name="TRASolicitudCadena"
    ),

    StringField(
        name='estadoSolicitudCadena',
        widget=SelectionWidget(
            label="Estado de la Solicitud de Cadena",
            label2="String Request Status",
            description="Estado de la Solicitud de Cadena, como Pendiente, Ignorada, o Creada.",
            description2="String Request Status as Pending, Ignored, or Created.",
            label_msgid='gvSIGi18n_TRASolicitudCadena_attr_estadoSolicitudCadena_label',
            description_msgid='gvSIGi18n_TRASolicitudCadena_attr_estadoSolicitudCadena_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Estado de la Solicitud de Cadena, como Pendiente, Ignorada, o Creada.",
        vocabulary=['Pendiente','Ignorada','Creada',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRASolicitudCadena_attr_estadoSolicitudCadena_option_Pendiente', 'gvSIGi18n_TRASolicitudCadena_attr_estadoSolicitudCadena_option_Ignorada', 'gvSIGi18n_TRASolicitudCadena_attr_estadoSolicitudCadena_option_Creada'],
        label2="String Request Status",
        ea_localid="1525",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="String Request Status as Pending, Ignored, or Created.",
        ea_guid="{F3F7D328-9FB0-4ef3-95A8-1EA079E3DEF8}",
        vocabulary2=['Pending','Ignored', 'Created',],
        scale="0",
        default='Pendiente',
        label="Estado de la Solicitud de Cadena",
        length="0",
        containment="Not Specified",
        position="4",
        owner_class_name="TRASolicitudCadena"
    ),

    StringField(
        name='fechaCreacionTextual',
        widget=StringWidget(
            label="Fecha de Creacion como texto",
            label2="Creation Date as text",
            description="Representacion textual de la fecha en que se creo la cadena a traducir.",
            description2="Textual representation of the date when the String was first created.",
            label_msgid='gvSIGi18n_TRASolicitudCadena_attr_fechaCreacionTextual_label',
            description_msgid='gvSIGi18n_TRASolicitudCadena_attr_fechaCreacionTextual_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Representacion textual de la fecha en que se creo la cadena a traducir.",
        duplicates="0",
        label2="Creation Date as text",
        ea_localid="1522",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Textual representation of the date when the String was first created.",
        ea_guid="{4F88BD50-4984-4d81-A80B-2FA459EFAE9D}",
        read_only="True",
        scale="0",
        label="Fecha de Creacion como texto",
        length="0",
        containment="Not Specified",
        position="6",
        owner_class_name="TRASolicitudCadena"
    ),

    StringField(
        name='usuarioCreador',
        widget=StringWidget(
            label="Usuario Creador",
            label2="Creator user",
            description="Usuario que creo o importo la cadena a traducir.",
            description2="User who created or imported the string to be translated.",
            label_msgid='gvSIGi18n_TRASolicitudCadena_attr_usuarioCreador_label',
            description_msgid='gvSIGi18n_TRASolicitudCadena_attr_usuarioCreador_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Usuario que creo o importo la cadena a traducir.",
        duplicates="0",
        label2="Creator user",
        ea_localid="1518",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="User who created or imported the string to be translated.",
        ea_guid="{CB2AC430-C5CC-4bf0-B6B7-4C11B9D9EC95}",
        read_only="True",
        scale="0",
        label="Usuario Creador",
        length="0",
        containment="Not Specified",
        position="10",
        owner_class_name="TRASolicitudCadena"
    ),

    StringField(
        name='fechaCancelacionTextual',
        widget=StringWidget(
            label="Fecha de Cancelacion",
            label2="Cancelation Date",
            description="La fecha en que la cadena fue cancelada, de forma que no vuelva a ser considerada para su traduccion.",
            description2="The date when the String was cancelled, such that the string won't be considered again for translation.",
            label_msgid='gvSIGi18n_TRASolicitudCadena_attr_fechaCancelacionTextual_label',
            description_msgid='gvSIGi18n_TRASolicitudCadena_attr_fechaCancelacionTextual_help',
            i18n_domain='gvSIGi18n',
        ),
        description="La fecha en que la cadena fue cancelada, de forma que no vuelva a ser considerada para su traduccion.",
        duplicates="0",
        label2="Cancelation Date",
        ea_localid="1523",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="The date when the String was cancelled, such that the string won't be considered again for translation.",
        ea_guid="{EA940557-4C2D-4e06-ACF4-AB6E2113B24F}",
        read_only="True",
        scale="0",
        label="Fecha de Cancelacion",
        length="0",
        containment="Not Specified",
        position="5",
        owner_class_name="TRASolicitudCadena"
    ),

    StringField(
        name='nombresModulos',
        widget=StringWidget(
            label="Modulos",
            label2="Modules",
            description="Nombres de los Modulos en los que se usa esta cadena.",
            description2="Names of the Modules using this String.",
            label_msgid='gvSIGi18n_TRASolicitudCadena_attr_nombresModulos_label',
            description_msgid='gvSIGi18n_TRASolicitudCadena_attr_nombresModulos_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Nombres de los Modulos en los que se usa esta cadena.",
        duplicates="0",
        label2="Modules",
        ea_localid="1534",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Names of the Modules using this String.",
        ea_guid="{E9755386-21D5-472e-960E-C6D8A6BC1887}",
        read_only="True",
        scale="0",
        label="Modulos",
        length="0",
        containment="Not Specified",
        position="7",
        owner_class_name="TRASolicitudCadena"
    ),

    StringField(
        name='referenciasFuentes',
        widget=StringWidget(
            label="Referencias a fuentes",
            label2="Source references",
            description="Referencias a codigo fuente donde aparece esta cadena.",
            description2="References to source code where the string is used.",
            label_msgid='gvSIGi18n_TRASolicitudCadena_attr_referenciasFuentes_label',
            description_msgid='gvSIGi18n_TRASolicitudCadena_attr_referenciasFuentes_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Referencias a codigo fuente donde aparece esta cadena.",
        duplicates="0",
        label2="Source references",
        ea_localid="1524",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="References to source code where the string is used.",
        containment="Not Specified",
        ea_guid="{63018342-F0CE-44a1-9EDC-734730A9FC5E}",
        position="8",
        owner_class_name="TRASolicitudCadena",
        label="Referencias a fuentes"
    ),

    StringField(
        name='codigoIdiomaPrincipal',
        widget=SelectionWidget(
            label="Codigo de Idioma Principal",
            label2="Main Language code",
            description="Codigo de Idioma Principal para el que el desarrollador proporciona una traducción.",
            description2="Main Language code for which the developer supplies a translation.",
            label_msgid='gvSIGi18n_TRASolicitudCadena_attr_codigoIdiomaPrincipal_label',
            description_msgid='gvSIGi18n_TRASolicitudCadena_attr_codigoIdiomaPrincipal_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Codigo de Idioma Principal para el que el desarrollador proporciona una traducción.",
        vocabulary='fVocabulary_CodigoIdiomaPrincipal',
        duplicates="0",
        label2="Main Language code",
        ea_localid="1530",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Main Language code for which the developer supplies a translation.",
        ea_guid="{E14EFE05-76A1-4432-9B81-B98CB8DE66DE}",
        read_only="True",
        scale="0",
        label="Codigo de Idioma Principal",
        length="0",
        containment="Not Specified",
        position="2",
        owner_class_name="TRASolicitudCadena"
    ),

    TextField(
        name='cadenaTraducidaAIdiomaPrincipal',
        widget=TextAreaWidget(
            label="Traduccion al Idioma Principal",
            label2="Translation into the main language",
            description="Cadena traducida al Idioma principal, suministrada por el desarrollador.",
            description2="String translated to the main Language, supplied by the developer.",
            label_msgid='gvSIGi18n_TRASolicitudCadena_attr_cadenaTraducidaAIdiomaPrincipal_label',
            description_msgid='gvSIGi18n_TRASolicitudCadena_attr_cadenaTraducidaAIdiomaPrincipal_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Cadena traducida al Idioma principal, suministrada por el desarrollador.",
        duplicates="0",
        label2="Translation into the main language",
        ea_localid="1528",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="String translated to the main Language, supplied by the developer.",
        containment="Not Specified",
        ea_guid="{5D47B672-17A5-46c0-8C08-F72075FB49E4}",
        position="0",
        owner_class_name="TRASolicitudCadena",
        label="Traduccion al Idioma Principal"
    ),

    StringField(
        name='codigoIdiomaReferencia',
        widget=SelectionWidget(
            label="Codigo de Idioma de referencia",
            label2="Reference Language code",
            description="Codigo de Idioma de referencia para el que el desarrollador proporciona una traducción.",
            description2="Reference Language code for which the developer supplies a translation.",
            label_msgid='gvSIGi18n_TRASolicitudCadena_attr_codigoIdiomaReferencia_label',
            description_msgid='gvSIGi18n_TRASolicitudCadena_attr_codigoIdiomaReferencia_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Codigo de Idioma de referencia para el que el desarrollador proporciona una traducción.",
        vocabulary='fVocabulary_CodigoIdiomaReferencia',
        duplicates="0",
        label2="Reference Language code",
        ea_localid="1527",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Reference Language code for which the developer supplies a translation.",
        ea_guid="{D20AAA93-7307-43f5-A043-24EA875BF767}",
        scale="0",
        label="Codigo de Idioma de referencia",
        length="0",
        containment="Not Specified",
        position="3",
        owner_class_name="TRASolicitudCadena"
    ),

    TextField(
        name='cadenaTraducidaAIdiomaReferencia',
        widget=TextAreaWidget(
            label="Traduccion al idioma de referencia",
            label2="Translation into the reference language",
            description="Cadena traducida al Idioma de referencia, suministrada por el desarrollador.",
            description2="String translated to the reference Language, supplied by the developer.",
            label_msgid='gvSIGi18n_TRASolicitudCadena_attr_cadenaTraducidaAIdiomaReferencia_label',
            description_msgid='gvSIGi18n_TRASolicitudCadena_attr_cadenaTraducidaAIdiomaReferencia_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Cadena traducida al Idioma de referencia, suministrada por el desarrollador.",
        duplicates="0",
        label2="Translation into the reference language",
        ea_localid="1529",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="String translated to the reference Language, supplied by the developer.",
        containment="Not Specified",
        ea_guid="{ED296F39-B610-4e7b-AE4D-FE9C68BD947F}",
        position="1",
        owner_class_name="TRASolicitudCadena",
        label="Traduccion al idioma de referencia"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRASolicitudCadena_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAArquetipo, 'schema', Schema(())).copy() + \
    getattr(TRAConRegistroActividad, 'schema', Schema(())).copy() + \
    getattr(TRASolicitudCadena_Operaciones, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRASolicitudCadena(OrderedBaseFolder, TRAArquetipo, TRAConRegistroActividad, TRASolicitudCadena_Operaciones):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAArquetipo,'__implements__',()),) + (getattr(TRAConRegistroActividad,'__implements__',()),) + (getattr(TRASolicitudCadena_Operaciones,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Solicitud Creacion Cadena'

    meta_type = 'TRASolicitudCadena'
    portal_type = 'TRASolicitudCadena'


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



    allowed_content_types = [] + list(getattr(TRAArquetipo, 'allowed_content_types', [])) + list(getattr(TRAConRegistroActividad, 'allowed_content_types', [])) + list(getattr(TRASolicitudCadena_Operaciones, 'allowed_content_types', []))
    filter_content_types             = 1
    global_allow                     = 0
    content_icon = 'trasolicitudcadena.gif'
    immediate_view                   = 'Tabular'
    default_view                     = 'Tabular'
    suppl_views                      = ['Tabular',]
    typeDescription                  = "Una solicitud para crear una nueva cadena del producto a traducir, identificada por su simbolo, y opcionalmente con traducciones al idioma principal e idioma de referencia."
    typeDescMsgId                    =  'gvSIGi18n_TRASolicitudCadena_help'
    archetype_name2                  = 'String creation request'
    typeDescription2                 = '''A request to create a new string to translate, identified by a string symbol, and optionally with translations into the main and reference language'''
    archetype_name_msgid             = 'gvSIGi18n_TRASolicitudCadena_label'
    factory_methods                  = None
    factory_enablers                 = None
    propagate_delete_impact_to       = None
    allow_discussion = 0


    actions =  (


       {'action': "string:$object_url/Editar",
        'category': "object",
        'id': 'edit',
        'name': 'Edit',
        'permissions': ("Modify portal content",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Edit_TRASolicitudCadena')"""
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

    schema = TRASolicitudCadena_schema

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

    security.declarePublic('fVocabulary_CodigoIdiomaPrincipal')
    def fVocabulary_CodigoIdiomaPrincipal(self):
        """
        """
        
        return self.getCatalogo().fTodosIdiomasVocabulary()

    security.declarePublic('fVocabulary_CodigoIdiomaReferencia')
    def fVocabulary_CodigoIdiomaReferencia(self):
        """
        """
        
        return self.getCatalogo().fTodosIdiomasVocabulary()

    security.declarePublic('fVocabulary_NombresModulos')
    def fVocabulary_NombresModulos(self):
        """
        """
        
        return self.getCatalogo().fTodosModulosVocabulary()

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
        if a['id'] in ['metadata', 'sharing', 'folderContents']:
            a['visible'] = 0
    return fti

registerType(TRASolicitudCadena, PROJECTNAME)
# end of class TRASolicitudCadena

##code-section module-footer #fill in your manual code here
##/code-section module-footer



