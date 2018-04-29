# -*- coding: utf-8 -*-
#
# File: TRASolicitudCadena.py
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
from Products.gvSIGi18n.TRACadena_Operaciones import TRACadena_Operaciones
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
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
        scale="0",
        description="El simbolo que identifica la Cadena que se solicita crear.",
        duplicates="0",
        label2="Symbol",
        ea_localid="1516",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="The symbol identifying the string requested to be created,",
        containment="Not Specified",
        ea_guid="{C13920DA-0B81-4b5e-82F9-B5202CB599CE}",
        position="0",
        owner_class_name="TRASolicitudCadena",
        label="Simbolo"
    ),

    StringField(
        name='estadoSolicitudCadena',
        widget=SelectionWidget(
            label="Estado de la Solicitud de Cadena",
            label2="String Request Status",
            description="Estado de la Solicitud de Cadena, como Dendiente, Descartada o Creada.",
            description2="String Request Status as Pending, Discarded, or Created.",
            label_msgid='gvSIGi18n_TRASolicitudCadena_attr_estadoSolicitudCadena_label',
            description_msgid='gvSIGi18n_TRASolicitudCadena_attr_estadoSolicitudCadena_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Estado de la Solicitud de Cadena, como Dendiente, Descartada o Creada.",
        vocabulary=['Pendiente','Descartada','Creada',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRASolicitudCadena_attr_estadoSolicitudCadena_option_Pendiente', 'gvSIGi18n_TRASolicitudCadena_attr_estadoSolicitudCadena_option_Descartada', 'gvSIGi18n_TRASolicitudCadena_attr_estadoSolicitudCadena_option_Creada'],
        label2="String Request Status",
        ea_localid="1525",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="String Request Status as Pending, Discarded, or Created.",
        ea_guid="{F3F7D328-9FB0-4ef3-95A8-1EA079E3DEF8}",
        vocabulary2=['Pending', 'Discarded', 'Created',],
        scale="0",
        default='Pendiente',
        label="Estado de la Solicitud de Cadena",
        length="0",
        containment="Not Specified",
        position="2",
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
        scale="0",
        description="Representacion textual de la fecha en que se creo la cadena a traducir.",
        duplicates="0",
        label2="Creation Date as text",
        ea_localid="1522",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="Textual representation of the date when the String was first created.",
        containment="Not Specified",
        ea_guid="{4F88BD50-4984-4d81-A80B-2FA459EFAE9D}",
        position="3",
        owner_class_name="TRASolicitudCadena",
        label="Fecha de Creacion como texto"
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
        scale="0",
        description="Usuario que creo o importo la cadena a traducir.",
        duplicates="0",
        label2="Creator user",
        ea_localid="1518",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="User who created or imported the string to be translated.",
        containment="Not Specified",
        ea_guid="{CB2AC430-C5CC-4bf0-B6B7-4C11B9D9EC95}",
        position="4",
        owner_class_name="TRASolicitudCadena",
        label="Usuario Creador"
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
        scale="0",
        description="La fecha en que la cadena fue cancelada, de forma que no vuelva a ser considerada para su traduccion.",
        duplicates="0",
        label2="Cancelation Date",
        ea_localid="1523",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="The date when the String was cancelled, such that the string won't be considered again for translation.",
        containment="Not Specified",
        ea_guid="{EA940557-4C2D-4e06-ACF4-AB6E2113B24F}",
        position="5",
        owner_class_name="TRASolicitudCadena",
        label="Fecha de Cancelacion"
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
        scale="0",
        description="Nombres de los Modulos en los que se usa esta cadena.",
        duplicates="0",
        label2="Modules",
        ea_localid="1519",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="Names of the Modules using this String.",
        containment="Not Specified",
        ea_guid="{DFD0DBFA-CCA5-45db-8E87-DCF27224F871}",
        position="6",
        owner_class_name="TRASolicitudCadena",
        label="Modulos"
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
        position="7",
        owner_class_name="TRASolicitudCadena",
        label="Referencias a fuentes"
    ),

    StringField(
        name='codigoIdiomaPrincipal',
        widget=StringWidget(
            label="Codigo de Idioma Principal",
            label2="Main Language code",
            description="Codigo de Idioma Principal para el que el desarrollador proporciona una traducción.",
            description2="Main Language code for which the developer supplies a translation.",
            label_msgid='gvSIGi18n_TRASolicitudCadena_attr_codigoIdiomaPrincipal_label',
            description_msgid='gvSIGi18n_TRASolicitudCadena_attr_codigoIdiomaPrincipal_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Codigo de Idioma Principal para el que el desarrollador proporciona una traducción.",
        duplicates="0",
        label2="Main Language code",
        ea_localid="1530",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="Main Language code for which the developer supplies a translation.",
        containment="Not Specified",
        ea_guid="{E14EFE05-76A1-4432-9B81-B98CB8DE66DE}",
        position="8",
        owner_class_name="TRASolicitudCadena",
        label="Codigo de Idioma Principal"
    ),

    StringField(
        name='cadenaTraducidaAIdiomaPrincipal',
        widget=StringWidget(
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
        position="9",
        owner_class_name="TRASolicitudCadena",
        label="Traduccion al Idioma Principal"
    ),

    StringField(
        name='codigoIdiomaReferencia',
        widget=StringWidget(
            label="Codigo de Idioma de referencia",
            label2="Reference Language code",
            description="Codigo de Idioma de referencia para el que el desarrollador proporciona una traducción.",
            description2="Reference Language code for which the developer supplies a translation.",
            label_msgid='gvSIGi18n_TRASolicitudCadena_attr_codigoIdiomaReferencia_label',
            description_msgid='gvSIGi18n_TRASolicitudCadena_attr_codigoIdiomaReferencia_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Codigo de Idioma de referencia para el que el desarrollador proporciona una traducción.",
        duplicates="0",
        label2="Reference Language code",
        ea_localid="1527",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="Reference Language code for which the developer supplies a translation.",
        containment="Not Specified",
        ea_guid="{D20AAA93-7307-43f5-A043-24EA875BF767}",
        position="10",
        owner_class_name="TRASolicitudCadena",
        label="Codigo de Idioma de referencia"
    ),

    StringField(
        name='cadenaTraducidaAIdiomaReferencia',
        widget=StringWidget(
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
        position="11",
        owner_class_name="TRASolicitudCadena",
        label="Traduccion al idioma de referencia"
    ),

    StringField(
        name='pathDelRaiz',
        widget=StringWidget(
            label="Path del Raiz",
            label2="Root's Path",
            description="Path del Catalogo raiz de este elemento.",
            description2="This element's root Catalog path.",
            label_msgid='gvSIGi18n_TRASolicitudCadena_attr_pathDelRaiz_label',
            description_msgid='gvSIGi18n_TRASolicitudCadena_attr_pathDelRaiz_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Path del Catalogo raiz de este elemento.",
        duplicates="0",
        label2="Root's Path",
        ea_localid="1520",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="This element's root Catalog path.",
        ea_guid="{E82F252E-2521-4c31-AA7E-2A8BCE07BD36}",
        scale="0",
        label="Path del Raiz",
        length="0",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        position="1",
        owner_class_name="TRASolicitudCadena",
        exclude_from_views="[ 'Textual', 'Tabular',  ]"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRASolicitudCadena_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAArquetipo, 'schema', Schema(())).copy() + \
    getattr(TRACadena_Operaciones, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRASolicitudCadena(OrderedBaseFolder, TRAArquetipo, TRACadena_Operaciones):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAArquetipo,'__implements__',()),) + (getattr(TRACadena_Operaciones,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Solicitud Creacion Cadena'

    meta_type = 'TRASolicitudCadena'
    portal_type = 'TRASolicitudCadena'
    allowed_content_types = [] + list(getattr(TRAArquetipo, 'allowed_content_types', [])) + list(getattr(TRACadena_Operaciones, 'allowed_content_types', []))
    filter_content_types = 1
    global_allow = 0
    content_icon = 'trasolicitudcadena.gif'
    immediate_view = 'Tabular'
    default_view = 'Tabular'
    suppl_views = ['Tabular',]
    typeDescription = "Una solicitud para crear una nueva cadena del producto a traducir, identificada por su simbolo, y opcionalmente con traducciones al idioma principal e idioma de referencia."
    typeDescMsgId =  'gvSIGi18n_TRASolicitudCadena_help'
    archetype_name2 = 'String creation request'
    typeDescription2 = '''A request to create a new string to translate, identified by a string symbol, and optionally with translations into the main and reference language'''
    archetype_name_msgid = 'gvSIGi18n_TRASolicitudCadena_label'
    factory_methods = None
    allow_discussion = 0


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
        'condition': 'python:object.fRoleQuery_IsCoordinatorOrDeveloper()'
       },


    )

    _at_rename_after_creation = True

    schema = TRASolicitudCadena_schema

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
        if a['id'] in ['metadata', 'sharing']:
            a['visible'] = 0
    return fti

registerType(TRASolicitudCadena, PROJECTNAME)
# end of class TRASolicitudCadena

##code-section module-footer #fill in your manual code here
##/code-section module-footer



