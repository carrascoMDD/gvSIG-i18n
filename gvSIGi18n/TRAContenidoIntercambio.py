# -*- coding: utf-8 -*-
#
# File: TRAContenidoIntercambio.py
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
from Products.gvSIGi18n.TRAContenidoIntercambio_Operaciones import TRAContenidoIntercambio_Operaciones
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    BooleanField(
        name='excluirDeImportacion',
        widget=BooleanField._properties['widget'](
            label="Excluir de Importacion",
            label2="Exclude from Import",
            description="Si es Verdadero, entonces este contenido de intercambio no se incluye en la importacion, ni en el sumario of vista detallada.",
            description2="If True, then this translations interchange contents will not be included in the import process, the summary or the detailed view.",
            label_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_excluirDeImportacion_label',
            description_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_excluirDeImportacion_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces este contenido de intercambio no se incluye en la importacion, ni en el sumario of vista detallada.",
        duplicates="0",
        label2="Exclude from Import",
        ea_localid="1463",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then this translations interchange contents will not be included in the import process, the summary or the detailed view.",
        ea_guid="{40D3DB8B-5D70-4027-932D-755A54899745}",
        scale="0",
        default="0",
        label="Excluir de Importacion",
        length="0",
        containment="Not Specified",
        position="1",
        owner_class_name="TRAContenidoIntercambio"
    ),

    StringField(
        name='nombreModulo',
        widget=StringWidget(
            label="Modulo",
            label2="Module",
            description="Nombre del Modulo en que se usa o resuelve esta cadena (base por defecto).",
            description2="Name of the Module where this String is used or resolved (base, by default).",
            label_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_nombreModulo_label',
            description_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_nombreModulo_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Nombre del Modulo en que se usa o resuelve esta cadena (base por defecto).",
        duplicates="0",
        label2="Module",
        ea_localid="984",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Name of the Module where this String is used or resolved (base, by default).",
        ea_guid="{23643564-462C-4376-BD6A-053471FFF4EA}",
        scale="0",
        default="base",
        label="Modulo",
        length="0",
        containment="Not Specified",
        position="0",
        owner_class_name="TRAContenidoIntercambio"
    ),

    StringField(
        name='usuarioContribuidor',
        widget=StringWidget(
            label="Usuario Contribuidor",
            label2="Contributor User",
            description="Usuario que ha subido al servidor el archivo de intercambio del contenido de traducciones de cadenas a idiomas.",
            description2="User who uploaded the interchange archive content string translations into languages.",
            label_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_usuarioContribuidor_label',
            description_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_usuarioContribuidor_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Usuario que ha subido al servidor el archivo de intercambio del contenido de traducciones de cadenas a idiomas.",
        duplicates="0",
        label2="Contributor User",
        ea_localid="956",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="User who uploaded the interchange archive content string translations into languages.",
        ea_guid="{E444AD8A-CE91-417c-8488-F7C9A8BD6CE0}",
        read_only=True,
        scale="0",
        label="Usuario Contribuidor",
        length="0",
        containment="Not Specified",
        position="2",
        owner_class_name="TRAContenidoIntercambio"
    ),

    DateTimeField(
        name='fechaContenido',
        widget=CalendarWidget(
            label="Fecha y Hora de Carga",
            label2="Upload Date and Time",
            description="Fecha y hora en que  completo o termino el proceso de carga del contenido de intercambio de traducciones.",
            description2="Date and Time when the process to  analise translations interchange archives was completed or terminated.",
            label_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_fechaContenido_label',
            description_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_fechaContenido_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Fecha y hora en que  completo o termino el proceso de carga del contenido de intercambio de traducciones.",
        duplicates="0",
        label2="Upload Date and Time",
        ea_localid="948",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Date and Time when the process to  analise translations interchange archives was completed or terminated.",
        ea_guid="{47A5578E-D8DD-40b4-9C13-E58B10354525}",
        read_only=True,
        scale="0",
        label="Fecha y Hora de Carga",
        length="0",
        containment="Not Specified",
        position="4",
        owner_class_name="TRAContenidoIntercambio"
    ),

    ComputedField(
        name='sumarioContenido',
        widget=ComputedField._properties['widget'](
            label="Sumario del contenido",
            label2="Contents summary",
            description="Sumario del contenido, con el Numero de Cadenas en el contenido de intercambio de cadenas. y los idiomas incluidos",
            description2="Contents summary with the Number of strings in the translations interchange content, and the Languages included.",
            label_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_sumarioContenido_label',
            description_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_sumarioContenido_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Sumario del contenido, con el Numero de Cadenas en el contenido de intercambio de cadenas. y los idiomas incluidos",
        duplicates="0",
        label2="Contents summary",
        ea_localid="969",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Contents summary with the Number of strings in the translations interchange content, and the Languages included.",
        ea_guid="{EE87E802-C6A1-4ab9-B83E-8FB97921838D}",
        exclude_from_values_form="True",
        scale="0",
        expression="context.fSumarioContenidoIntercambio()",
        label="Sumario del contenido",
        length="0",
        containment="Not Specified",
        position="7",
        owner_class_name="TRAContenidoIntercambio",
        exclude_from_views="[ 'Textual', 'Tabular',  ]"
    ),

    ComputedField(
        name='informeContenido',
        widget=ComputedField._properties['widget'](
            label="Contenido Intercambio de Traducciones",
            label2="Content in Trasnslations Interchange",
            description="Contenidos de los Archivos de intercambio de traducciones  incluyendo un numero de directorios de modulo con ficheros de cadenas y traducciones a un numero de idiomas,",
            description2="Contents of translations interchange Archive files, including a number of module directories with files with strings and translations to a number of languages.",
            label_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_informeContenido_label',
            description_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_informeContenido_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Contenidos de los Archivos de intercambio de traducciones  incluyendo un numero de directorios de modulo con ficheros de cadenas y traducciones a un numero de idiomas,",
        duplicates="0",
        label2="Content in Trasnslations Interchange",
        ea_localid="993",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Contents of translations interchange Archive files, including a number of module directories with files with strings and translations to a number of languages.",
        ea_guid="{6E839E35-1227-4081-9397-0F4CF172D96A}",
        exclude_from_values_form="True",
        scale="0",
        exclude_from_views="[ 'Textual', 'Tabular', ]",
        label="Contenido Intercambio de Traducciones",
        length="0",
        expression="context.fInformeContenidoIntercambio()",
        containment="Not Specified",
        position="6",
        owner_class_name="TRAContenidoIntercambio",
        custom_presentation_view="TRAContenidoIntercambioTraducciones_i18n_view",
        computed_types="text"
    ),

    TextField(
        name='contenido',
        widget=TextAreaWidget(
            label="Contenido",
            label2="Contents",
            description="Contenido ya analizado del intercambio de traducciones de cadenas a idiomas.",
            description2="Already analised contents of the interchange of string translations into languages.",
            label_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_contenido_label',
            description_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_contenido_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Contenido ya analizado del intercambio de traducciones de cadenas a idiomas.",
        duplicates="0",
        label2="Contents",
        ea_localid="964",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Already analised contents of the interchange of string translations into languages.",
        ea_guid="{711B544F-FEA0-403e-8D74-D691687CFE9C}",
        read_only=True,
        scale="0",
        label="Contenido",
        length="0",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        position="5",
        owner_class_name="TRAContenidoIntercambio"
    ),

    ComputedField(
        name='pathDelRaiz',
        widget=ComputedField._properties['widget'](
            label="Path del Raiz",
            label2="Root's Path",
            description="Path del Catalogo raiz de este elemento.",
            description2="This element's root Catalog path.",
            label_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_pathDelRaiz_label',
            description_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_pathDelRaiz_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Path del Catalogo raiz de este elemento.",
        duplicates="0",
        label2="Root's Path",
        ea_localid="1145",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="This element's root Catalog path.",
        ea_guid="{F52AD924-7BAB-4339-8FFE-B7DDE391DC1F}",
        scale="0",
        expression="context.fPathDelRaiz()",
        label="Path del Raiz",
        length="0",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        position="3",
        owner_class_name="TRAContenidoIntercambio",
        exclude_from_views="[ 'Textual', 'Tabular',  ]"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAContenidoIntercambio_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAArquetipo, 'schema', Schema(())).copy() + \
    getattr(TRAContenidoIntercambio_Operaciones, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAContenidoIntercambio(OrderedBaseFolder, TRAArquetipo, TRAContenidoIntercambio_Operaciones):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAArquetipo,'__implements__',()),) + (getattr(TRAContenidoIntercambio_Operaciones,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Contenido de Intercambio'

    meta_type = 'TRAContenidoIntercambio'
    portal_type = 'TRAContenidoIntercambio'
    use_folder_tabs = 0

    allowed_content_types = [] + list(getattr(TRAArquetipo, 'allowed_content_types', [])) + list(getattr(TRAContenidoIntercambio_Operaciones, 'allowed_content_types', []))
    filter_content_types = 1
    global_allow = 0
    content_icon = 'tracontenidointercambio.gif'
    immediate_view = 'Tabular'
    default_view = 'Tabular'
    suppl_views = ['Tabular',]
    typeDescription = "Contenido de un intercambio, bien Importacion o Exportacion, de traducciones de cadenas a uno o mas idiomas."
    typeDescMsgId =  'gvSIGi18n_TRAContenidoIntercambio_help'
    archetype_name2 = 'Interchange Content'
    typeDescription2 = '''Contents of an Import or Export interchange of string translations to a number od languages'''
    archetype_name_msgid = 'gvSIGi18n_TRAContenidoIntercambio_label'
    factory_methods = None
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


       {'action': "string:$object_url/Editar",
        'category': "object",
        'id': 'edit',
        'name': 'Edit',
        'permissions': ("Modify portal content",),
        'condition': 'python:1'
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


       {'action': "string:${object_url}/TRAInformeContenidoIntercambio_action",
        'category': "object",
        'id': 'ContenidoIntercambio',
        'name': 'Data',
        'permissions': ("View",),
        'condition': 'python:1'
       },


    )

    _at_rename_after_creation = True

    schema = TRAContenidoIntercambio_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('manage_beforeDelete')
    def manage_beforeDelete(self,item,container):
        """
        """
        
        return TRAArquetipo.manage_beforeDelete( self, item, container)

    security.declarePublic('manage_afterAdd')
    def manage_afterAdd(self,item,container):
        """
        """
        
        return TRAArquetipo.manage_beforeDelete( self, item, container)
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata']:
            a['visible'] = 0
    return fti

registerType(TRAContenidoIntercambio, PROJECTNAME)
# end of class TRAContenidoIntercambio

##code-section module-footer #fill in your manual code here
##/code-section module-footer



