# -*- coding: utf-8 -*-
#
# File: TRACatalogo.py
#
# Copyright (c) 2010 by 2008, 2009, 2010 Conselleria de Infraestructuras y
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
from TRACatalogo_Inicializacion import TRACatalogo_Inicializacion
from TRACatalogo_Informes import TRACatalogo_Informes
from TRACatalogo_Globales import TRACatalogo_Globales
from TRACatalogo_Operaciones import TRACatalogo_Operaciones
from TRACatalogo_CursorTraducciones import TRACatalogo_CursorTraducciones
from TRACatalogo_Actividad import TRACatalogo_Actividad
from TRACatalogo_Exportacion import TRACatalogo_Exportacion
from Products.gvSIGi18n.TRAConRegistroActividad import TRAConRegistroActividad
from Products.ATContentTypes.content.document import ATDocument
from Products.ATContentTypes.content.base import updateAliases
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from TRAElemento_Operaciones import TRAElemento_Operaciones

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    BooleanField(
        name='permiteModificar',
        widget=BooleanField._properties['widget'](
            label="Permite Modificar",
            label2="Allow Changes",
            description="Si Verdadero, entonces los usuarios puede realizar los cambios a los que permite sus roles en la aplicacion. Si Falso, entonces no puede realizar cambios,  Puede ocurrir durante  procesos de importacion largos.",
            description2="If True, then the users may perform the changes authorized by granted roles. If False, then the user can not make changes. This may happen during long import processe.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_permiteModificar_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_permiteModificar_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, entonces los usuarios puede realizar los cambios a los que permite sus roles en la aplicacion. Si Falso, entonces no puede realizar cambios,  Puede ocurrir durante  procesos de importacion largos.",
        duplicates="0",
        label2="Allow Changes",
        ea_localid="1561",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="If True, then the users may perform the changes authorized by granted roles. If False, then the user can not make changes. This may happen during long import processe.",
        ea_guid="{C371164E-3825-45fb-8A9B-19C539BD9E84}",
        read_only="True",
        scale="0",
        default="True",
        label="Permite Modificar",
        length="0",
        containment="Not Specified",
        position="2",
        owner_class_name="TRACatalogo",
        exclude_from_exportconfig="True",
        exclude_from_copyconfig="True"
    ),

    StringField(
        name='nombreProducto',
        widget=StringWidget(
            label="Producto",
            label2="Product",
            description="Nombre del Producto cuyas traducciones se manejan con este Catalogo.",
            description2="Name of the Product translated in this Catalog.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_nombreProducto_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_nombreProducto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Nombre del Producto cuyas traducciones se manejan con este Catalogo.",
        duplicates="0",
        label2="Product",
        ea_localid="421",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Name of the Product translated in this Catalog.",
        ea_guid="{EF50B352-9D2E-403c-9FB8-E2E53C88C377}",
        scale="0",
        default="gvSIG",
        label="Producto",
        length="0",
        containment="Not Specified",
        position="1",
        owner_class_name="TRACatalogo"
    ),

    ComputedField(
        name='configuraciones',
        widget=ComputedWidget(
            label="Configuraciones",
            label2="Configurations",
            description="Configuraciones del catalogo de traducciones, cada una con parametros controlando un aspecto del las operaciones sobre el catalogo.",
            description2="Translations catalog configurations, each one with parameters controlling an aspect of operations on the catalog.",
            label_msgid='gvSIGi18n_TRACatalogo_contents_configuraciones_label',
            description_msgid='gvSIGi18n_TRACatalogo_contents_configuraciones_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=False,
        label2='Configurations',
        additional_columns=['aspectoConfiguracion'],
        label='Configuraciones',
        represents_aggregation=True,
        description2='Translations catalog configurations, each one with parameters controlling an aspect of operations on the catalog.',
        multiValued=1,
        owner_class_name="TRACatalogo",
        expression="context.objectValues(['TRAConfiguracionAlmacenPaginas', 'TRAConfiguracionExportacion', 'TRAConfiguracionImportacion', 'TRAConfiguracionPaginaTraducciones', 'TRAConfiguracionPerfilEjecucion', 'TRAConfiguracionPermisos', 'TRAConfiguracionSolicitudesCadenas', 'TRAConfiguracionVarios'])",
        computed_types=['TRAConfiguracionAlmacenPaginas', 'TRAConfiguracionExportacion', 'TRAConfiguracionImportacion', 'TRAConfiguracionPaginaTraducciones', 'TRAConfiguracionPerfilEjecucion', 'TRAConfiguracionPermisos', 'TRAConfiguracionSolicitudesCadenas', 'TRAConfiguracionVarios'],
        non_framework_elements=False,
        description='Configuraciones del catalogo de traducciones, cada una con parametros controlando un aspecto del las operaciones sobre el catalogo.'
    ),

    ComputedField(
        name='parametrosControlProgreso',
        widget=ComputedWidget(
            label="Parametros Control Progreso",
            label2="Progress Control Parameters",
            description="Parametros controlando la gestion del progreso de procesos de larga duracion, incluyendo registro, transacciones, guardar resultados y ceder procesador.",
            description2="Parameters controlling the management of the progress of long-lived processes, including logging, transactions, store results and yield processor.",
            label_msgid='gvSIGi18n_TRACatalogo_contents_parametrosControlProgreso_label',
            description_msgid='gvSIGi18n_TRACatalogo_contents_parametrosControlProgreso_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=False,
        label2='Progress Control Parameters',
        additional_columns=['tipoProceso'],
        label='Parametros Control Progreso',
        represents_aggregation=True,
        description2='Parameters controlling the management of the progress of long-lived processes, including logging, transactions, store results and yield processor.',
        multiValued=1,
        owner_class_name="TRACatalogo",
        expression="context.objectValues(['TRAParametrosControlProgreso'])",
        computed_types=['TRAParametrosControlProgreso'],
        non_framework_elements=False,
        description='Parametros controlando la gestion del progreso de procesos de larga duracion, incluyendo registro, transacciones, guardar resultados y ceder procesador.'
    ),

    ComputedField(
        name='coleccionIdiomas',
        widget=ComputedWidget(
            label="Coleccion de Idiomas",
            label2="Languages collection",
            description="Coleccion de idiomas a los que se desea traducir las cadenas.",
            description2="Collection of languages to translate the strings into.",
            label_msgid='gvSIGi18n_TRACatalogo_contents_coleccionIdiomas_label',
            description_msgid='gvSIGi18n_TRACatalogo_contents_coleccionIdiomas_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=True,
        label2='Languages collection',
        label='Coleccion de Idiomas',
        represents_aggregation=True,
        description2='Collection of languages to translate the strings into.',
        multiValued=1,
        owner_class_name="TRACatalogo",
        multiplicity_higher=1,
        expression="context.objectValues(['TRAColeccionIdiomas'])",
        computed_types=['TRAColeccionIdiomas'],
        non_framework_elements=False,
        description='Coleccion de idiomas a los que se desea traducir las cadenas.'
    ),

    ComputedField(
        name='coleccionModulos',
        widget=ComputedWidget(
            label="Coleccion de Modulos",
            label2="Modules collection",
            description="Coleccion de Modulos en el Producto a traducir.",
            description2="Collection of Modules in the Product to Translate",
            label_msgid='gvSIGi18n_TRACatalogo_contents_coleccionModulos_label',
            description_msgid='gvSIGi18n_TRACatalogo_contents_coleccionModulos_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=True,
        label2='Modules collection',
        label='Coleccion de Modulos',
        represents_aggregation=True,
        description2='Collection of Modules in the Product to Translate',
        multiValued=1,
        owner_class_name="TRACatalogo",
        multiplicity_higher=1,
        expression="context.objectValues(['TRAColeccionModulos'])",
        computed_types=['TRAColeccionModulos'],
        non_framework_elements=False,
        description='Coleccion de Modulos en el Producto a traducir.'
    ),

    ComputedField(
        name='coleccionImportaciones',
        widget=ComputedWidget(
            label="Coleccion de Importaciones",
            label2="Import processes collection",
            description="Coleccion de procesos de Importacion para cargar modulos, idiomas, cadenas y traducciones.",
            description2="Collection of Import processes to load modules,  languages, strings and translations.",
            label_msgid='gvSIGi18n_TRACatalogo_contents_coleccionImportaciones_label',
            description_msgid='gvSIGi18n_TRACatalogo_contents_coleccionImportaciones_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=True,
        label2='Import processes collection',
        label='Coleccion de Importaciones',
        represents_aggregation=True,
        description2='Collection of Import processes to load modules,  languages, strings and translations.',
        multiValued=1,
        owner_class_name="TRACatalogo",
        multiplicity_higher=1,
        expression="context.objectValues(['TRAColeccionImportaciones'])",
        computed_types=['TRAColeccionImportaciones'],
        non_framework_elements=False,
        description='Coleccion de procesos de Importacion para cargar modulos, idiomas, cadenas y traducciones.'
    ),

    ComputedField(
        name='coleccionInformes',
        widget=ComputedWidget(
            label="Coleccion de Informes de Estado",
            label2="Status Reports collection",
            description="Coleccion de Informes del Estado de traducciones en Modulos e Idiomas.",
            description2="Collection of Status Reports of Translations to  Languages and Modules",
            label_msgid='gvSIGi18n_TRACatalogo_contents_coleccionInformes_label',
            description_msgid='gvSIGi18n_TRACatalogo_contents_coleccionInformes_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=True,
        label2='Status Reports collection',
        label='Coleccion de Informes de Estado',
        represents_aggregation=True,
        description2='Collection of Status Reports of Translations to  Languages and Modules',
        multiValued=1,
        owner_class_name="TRACatalogo",
        multiplicity_higher=1,
        expression="context.objectValues(['TRAColeccionInformes'])",
        computed_types=['TRAColeccionInformes'],
        non_framework_elements=False,
        description='Coleccion de Informes del Estado de traducciones en Modulos e Idiomas.'
    ),

    ComputedField(
        name='coleccionProgresos',
        widget=ComputedWidget(
            label="Coleccion de Progresos",
            label2="Progresses collection",
            description="Coleccion de informes de Progreso acerca de Procesos de larga duracion",
            description2="Collection of Progress reports about long-lived processes",
            label_msgid='gvSIGi18n_TRACatalogo_contents_coleccionProgresos_label',
            description_msgid='gvSIGi18n_TRACatalogo_contents_coleccionProgresos_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=True,
        label2='Progresses collection',
        label='Coleccion de Progresos',
        represents_aggregation=True,
        description2='Collection of Progress reports about long-lived processes',
        multiValued=1,
        owner_class_name="TRACatalogo",
        multiplicity_higher=1,
        expression="context.objectValues(['TRAColeccionProgresos'])",
        computed_types=['TRAColeccionProgresos'],
        non_framework_elements=False,
        description='Coleccion de informes de Progreso acerca de Procesos de larga duracion'
    ),

    ComputedField(
        name='coleccionCadenas',
        widget=ComputedWidget(
            label="Coleccion de Cadenas",
            label2="Strings collection",
            description="Coleccion de Cadenas a traducir a los varios idiomas.",
            description2="Collection of strings to translate to a number of languages.",
            label_msgid='gvSIGi18n_TRACatalogo_contents_coleccionCadenas_label',
            description_msgid='gvSIGi18n_TRACatalogo_contents_coleccionCadenas_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=True,
        label2='Strings collection',
        label='Coleccion de Cadenas',
        represents_aggregation=True,
        description2='Collection of strings to translate to a number of languages.',
        multiValued=1,
        owner_class_name="TRACatalogo",
        multiplicity_higher=1,
        expression="context.objectValues(['TRAColeccionCadenas'])",
        computed_types=['TRAColeccionCadenas'],
        non_framework_elements=False,
        description='Coleccion de Cadenas a traducir a los varios idiomas.'
    ),

    ComputedField(
        name='coleccionSolicitudesCadenas',
        widget=ComputedWidget(
            label="Coleccion de Solicitudes de Cadenas",
            label2="String Requests collection",
            description="Coleccion de solicitudes realizadas por los desarrolladores, para crear nuevas cadenas.",
            description2="Collection of requests by developers to create new strings.",
            label_msgid='gvSIGi18n_TRACatalogo_contents_coleccionSolicitudesCadenas_label',
            description_msgid='gvSIGi18n_TRACatalogo_contents_coleccionSolicitudesCadenas_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=True,
        label2='String Requests collection',
        label='Coleccion de Solicitudes de Cadenas',
        represents_aggregation=True,
        description2='Collection of requests by developers to create new strings.',
        multiValued=1,
        owner_class_name="TRACatalogo",
        multiplicity_higher=1,
        expression="context.objectValues(['TRAColeccionSolicitudesCadenas'])",
        computed_types=['TRAColeccionSolicitudesCadenas'],
        non_framework_elements=False,
        description='Coleccion de solicitudes realizadas por los desarrolladores, para crear nuevas cadenas.'
    ),

    BooleanField(
        name='debeRecatalogar',
        widget=BooleanField._properties['widget'](
            label="Debe Recatalogar",
            label2="Must Re-Catalog",
            description="Si Verdadero, entonces el Manager debe re-catalogar los elementos del catalog de traducciones, pues un proceso de inicializacion ha modificado la estructura de catalogos y/o indices.",
            description2="If True, then the Manager must recatalog the elements in the translations catalog, because an initialization process has modified the structure of catalogs or indexes.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_debeRecatalogar_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_debeRecatalogar_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, entonces el Manager debe re-catalogar los elementos del catalog de traducciones, pues un proceso de inicializacion ha modificado la estructura de catalogos y/o indices.",
        duplicates="0",
        label2="Must Re-Catalog",
        ea_localid="1973",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="If True, then the Manager must recatalog the elements in the translations catalog, because an initialization process has modified the structure of catalogs or indexes.",
        ea_guid="{D6CCC031-E837-44f0-AA3C-080B1D5C802D}",
        read_only="True",
        scale="0",
        default="False",
        label="Debe Recatalogar",
        length="0",
        containment="Not Specified",
        position="0",
        owner_class_name="TRACatalogo",
        exclude_from_exportconfig="True",
        exclude_from_copyconfig="True"
    ),

    ComputedField(
        name='simbolosOrdenados',
        widget=ComputedWidget(
            label="Simbolos Ordenados",
            label2="""Ordered Symbols
            Holds the ordered list of string symbols in the translations catalog, grouped by modules.""",
            description="Mantiene la lista ordenada de simbolos en el catalogo de traducciones, agrupadas por modulos.",
            label_msgid='gvSIGi18n_TRACatalogo_contents_simbolosOrdenados_label',
            description_msgid='gvSIGi18n_TRACatalogo_contents_simbolosOrdenados_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=False,
        label2='Ordered Symbols\nHolds the ordered list of string symbols in the translations catalog, grouped by modules.',
        label='Simbolos Ordenados',
        represents_aggregation=True,
        multiValued=1,
        owner_class_name="TRACatalogo",
        multiplicity_higher=1,
        expression="context.objectValues(['TRASimbolosOrdenados'])",
        computed_types=['TRASimbolosOrdenados'],
        non_framework_elements=False,
        description='Mantiene la lista ordenada de simbolos en el catalogo de traducciones, agrupadas por modulos.'
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRACatalogo_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAArquetipo, 'schema', Schema(())).copy() + \
    getattr(TRACatalogo_Inicializacion, 'schema', Schema(())).copy() + \
    getattr(TRACatalogo_Informes, 'schema', Schema(())).copy() + \
    getattr(TRACatalogo_Globales, 'schema', Schema(())).copy() + \
    getattr(TRACatalogo_Operaciones, 'schema', Schema(())).copy() + \
    getattr(TRACatalogo_CursorTraducciones, 'schema', Schema(())).copy() + \
    getattr(TRACatalogo_Actividad, 'schema', Schema(())).copy() + \
    getattr(TRACatalogo_Exportacion, 'schema', Schema(())).copy() + \
    getattr(TRAConRegistroActividad, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRACatalogo(OrderedBaseFolder, TRAArquetipo, TRACatalogo_Inicializacion, TRACatalogo_Informes, TRACatalogo_Globales, TRACatalogo_Operaciones, TRACatalogo_CursorTraducciones, TRACatalogo_Actividad, TRACatalogo_Exportacion, TRAConRegistroActividad):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAArquetipo,'__implements__',()),) + (getattr(TRACatalogo_Inicializacion,'__implements__',()),) + (getattr(TRACatalogo_Informes,'__implements__',()),) + (getattr(TRACatalogo_Globales,'__implements__',()),) + (getattr(TRACatalogo_Operaciones,'__implements__',()),) + (getattr(TRACatalogo_CursorTraducciones,'__implements__',()),) + (getattr(TRACatalogo_Actividad,'__implements__',()),) + (getattr(TRACatalogo_Exportacion,'__implements__',()),) + (getattr(TRAConRegistroActividad,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Catalogo de Traducciones'

    meta_type = 'TRACatalogo'
    portal_type = 'TRACatalogo'


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



    allowed_content_types = ['TRAColeccionInformes', 'TRAColeccionCadenas', 'TRAParametrosControlProgreso', 'TRAColeccionImportaciones', 'TRAColeccionSolicitudesCadenas', 'TRASimbolosOrdenados', 'TRAColeccionIdiomas', 'TRAColeccionProgresos', 'TRAColeccionModulos', 'TRAConfiguracionAlmacenPaginas', 'TRAConfiguracionExportacion', 'TRAConfiguracionSolicitudesCadenas', 'TRAConfiguracionImportacion', 'TRAConfiguracionPaginaTraducciones', 'TRAConfiguracionVarios', 'TRAConfiguracionPerfilEjecucion', 'TRAConfiguracionPermisos'] + list(getattr(TRAArquetipo, 'allowed_content_types', [])) + list(getattr(TRACatalogo_Inicializacion, 'allowed_content_types', [])) + list(getattr(TRACatalogo_Informes, 'allowed_content_types', [])) + list(getattr(TRACatalogo_Globales, 'allowed_content_types', [])) + list(getattr(TRACatalogo_Operaciones, 'allowed_content_types', [])) + list(getattr(TRACatalogo_CursorTraducciones, 'allowed_content_types', [])) + list(getattr(TRACatalogo_Actividad, 'allowed_content_types', [])) + list(getattr(TRACatalogo_Exportacion, 'allowed_content_types', [])) + list(getattr(TRAConRegistroActividad, 'allowed_content_types', []))
    filter_content_types             = 1
    global_allow                     = 1
    content_icon = 'tracatalogo.gif'
    immediate_view                   = 'TRACatalogo'
    default_view                     = 'TRACatalogo'
    suppl_views                      = ['TRACatalogo',]
    typeDescription                  = "Contiene los Idiomas, Cadenas y Traducciones de las cadenas a multiples idiomas."
    typeDescMsgId                    =  'gvSIGi18n_TRACatalogo_help'
    archetype_name2                  = 'Translations Catalog'
    typeDescription2                 = '''Containing a number of languages, strings to translate, and their translations to the the languages.'''
    archetype_name_msgid             = 'gvSIGi18n_TRACatalogo_label'
    factory_methods                  = None
    factory_enablers                 = None
    propagate_delete_impact_to       = None
    allow_discussion = False


    actions =  (


       {'action': "string:${object_url}/TRACatalogoActividad",
        'category': "object",
        'id': 'TRA_actividad',
        'name': 'Activity',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and (True or object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'EllaborateInformeActividad'))"""
       },


       {'action': "string:${object_url}/Tabular/",
        'category': "object",
        'id': 'TRA_advanced',
        'name': 'Details',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Advanced_View_on_any_TRA_element')"""
       },


       {'action': "string:${object_url}/TRAConfirmarBloquearCatalogo",
        'category': "object_buttons",
        'id': 'TRA_bloquear_catalogo',
        'name': 'Lock Catalog',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Lock_TRACatalogo')"""
       },


       {'action': "string:${object_url}/TRABackup_action",
        'category': "object_buttons",
        'id': 'TRA_export_backup',
        'name': 'Export Backup',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Backup_TRACatalogo')"""
       },


       {'action': "string:${object_url}/idiomas/TRACrear_Idioma",
        'category': "object_buttons",
        'id': 'TRACreateLanguage',
        'name': 'Create Language',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Create_TRAIdioma')"""
       },


       {'action': "string:${object_url}/importaciones/Crear/?theNewTypeName=TRAImportacion&theAggregationName=importaciones",
        'category': "object_buttons",
        'id': 'TRACreateImportacion',
        'name': 'Create Import',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable(object, 'Create_TRAImportacion')"""
       },


       {'action': "string:${object_url}/importaciones/TRACrearImportacion_RecuperarCopiaSeguridad",
        'category': "object_buttons",
        'id': 'TRARestoreBackup',
        'name': 'Create Import to Restore Backup',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable(object, 'Create_TRAImportacion_RestoreBackup')"""
       },


       {'action': "string:${object_url}/informes/TRACrear_Informe",
        'category': "object_buttons",
        'id': 'TRACreateInforme',
        'name': 'Create Report',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable(object, 'Create_TRAInforme')"""
       },


       {'action': "string:${object_url}/modulos/TRACrear_Modulo",
        'category': "object_buttons",
        'id': 'TRACreateModule',
        'name': 'Create Module',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable(object, 'Create_TRAModulo')"""
       },


       {'action': "string:${object_url}/solicitudescadenas/TRACrear_SolicitudCadena/?theNewTypeName=TRASolicitudCadena&theAggregationName=solicitudesCadenas",
        'category': "object_buttons",
        'id': 'TRACreateSolicitudCadena',
        'name': 'Create New String Request',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable(object, 'Create_TRASolicitudCadena')"""
       },


       {'action': "string:${object_url}/Editar",
        'category': "object_buttons",
        'id': 'TRA_configurar',
        'name': 'Configure',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Configure_TRACatalogo')"""
       },


       {'action': "string:${object_url}/TRAConfirmarDesbloquearCatalogo",
        'category': "object_buttons",
        'id': 'TRA_desbloquear_catalogo',
        'name': 'Unlock Catalog',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Unlock_TRACatalogo')"""
       },


       {'action': "string:${object_url}/TRACatalogoDetalle",
        'category': "object",
        'id': 'TRA_detalle',
        'name': 'Report',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'EllaborateInformeModulesAndLanguages')"""
       },


       {'action': "string:$object_url/base_edit",
        'category': "object",
        'id': 'edit',
        'name': 'Edit',
        'permissions': ("Modify portal content",),
        'condition': """python:'portal_factory' in object.getPhysicalPath()"""
       },


       {'action': "string:${object_url}/TRAExportar",
        'category': "object_buttons",
        'id': 'TRA_export_translations',
        'name': 'Export',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Export')"""
       },


       {'action': "string:${object_url}/TRACatalogoInforme",
        'category': "object",
        'id': 'TRA_informe',
        'name': 'Summary',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'EllaborateInformeLanguages')"""
       },


       {'action': "string:${object_url}/TRAInicializar_Direct_action",
        'category': "object_buttons",
        'id': 'TRA_inicializar_direct',
        'name': 'Initialize (w/o tool)',
        'permissions': ("View",),
        'condition': """python:not object.fHasTRAtool()"""
       },


       {'action': "string:${object_url}/TRAInicializar_action",
        'category': "object_buttons",
        'id': 'TRA_inicializar',
        'name': 'Initialize',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Initialize_TRACatalogo')"""
       },


       {'action': "string:${object_url}/TRAVerificar_Direct_action",
        'category': "object_buttons",
        'id': 'TRA_verificar_direct',
        'name': 'Verify (w/o tool)',
        'permissions': ("View",),
        'condition': """python:not object.fHasTRAtool()"""
       },


       {'action': "string:${object_url}/TRACatalogo",
        'category': "object",
        'id': 'view',
        'name': 'View',
        'permissions': ("View",),
        'condition': """python:True or (object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'View_any_TRA_element'))"""
       },


       {'action': "string:${object_url}/TRAVerificar_action",
        'category': "object_buttons",
        'id': 'TRA_verificar',
        'name': 'Verify',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Verify_TRACatalogo')"""
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


    aliases = updateAliases( ATDocument, {'folder_factories':'Tabular','cut':'Tabular','object_cut':'Tabular','delete_confirmation': 'Tabular','object_rename': 'Editar','content_status_modify':'Tabular','content_status_history':'Tabular','placeful_workflow_configuration': 'Tabular',})

    _at_rename_after_creation = True

    schema = TRACatalogo_schema

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
        
        return TRACatalogo_Operaciones.fExtraLinks( self)

    security.declarePublic('fIsCacheable')
    def fIsCacheable(self):
        """
        """
        
        return True

    security.declarePublic('getEsRaiz')
    def getEsRaiz(self):
        """
        """
        
        return True

    security.declarePublic('manage_afterAdd')
    def manage_afterAdd(self,item,container):
        """
        """
        
        return TRACatalogo_Operaciones.pHandle_manage_afterAdd( self, item, container)

    security.declarePublic('manage_beforeDelete')
    def manage_beforeDelete(self,item,container):
        """
        """
        
        return TRACatalogo_Operaciones.pHandle_manage_beforeDelete( self, item, container)

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

registerType(TRACatalogo, PROJECTNAME)
# end of class TRACatalogo

##code-section module-footer #fill in your manual code here
##/code-section module-footer



