# -*- coding: utf-8 -*-
#
# File: TRATraduccion.py
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
from TRATraduccion_Operaciones import TRATraduccion_Operaciones
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
            description="El simbolo original que identifica la Cadena a traducir.",
            description2="The original symbol identifying the string to be translated.",
            label_msgid='gvSIGi18n_TRATraduccion_attr_simbolo_label',
            description_msgid='gvSIGi18n_TRATraduccion_attr_simbolo_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="El simbolo original que identifica la Cadena a traducir.",
        duplicates="0",
        label2="Symbol",
        ea_localid="307",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="The original symbol identifying the string to be translated.",
        containment="Not Specified",
        ea_guid="{9601C385-3396-492f-BC82-10FC4DED739A}",
        position="0",
        owner_class_name="TRATraduccion",
        label="Simbolo"
    ),

    StringField(
        name='codigoIdiomaEnGvSIG',
        widget=StringWidget(
            label="Codigo de Idioma en gvSIG",
            label2="Language code in gvSIG",
            description="Codigo de Idioma en gvSIG, que soporta algunos idiomas para los que no existe (todavia) un codigo internacional.",
            description2="Language code in gvSIG, as gvSIG supports some languages for which there is no international code (yet).",
            label_msgid='gvSIGi18n_TRATraduccion_attr_codigoIdiomaEnGvSIG_label',
            description_msgid='gvSIGi18n_TRATraduccion_attr_codigoIdiomaEnGvSIG_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Codigo de Idioma en gvSIG, que soporta algunos idiomas para los que no existe (todavia) un codigo internacional.",
        duplicates="0",
        label2="Language code in gvSIG",
        ea_localid="308",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="Language code in gvSIG, as gvSIG supports some languages for which there is no international code (yet).",
        containment="Not Specified",
        ea_guid="{084C77CD-8E2C-4ba3-ABAE-502699EF3196}",
        position="1",
        owner_class_name="TRATraduccion",
        label="Codigo de Idioma en gvSIG"
    ),

    StringField(
        name='cadenaTraducida',
        widget=StringWidget(
            label="Traduccion",
            label2="Translation",
            description="Cadena traducida al Idioma.",
            description2="String translated to the Language.",
            label_msgid='gvSIGi18n_TRATraduccion_attr_cadenaTraducida_label',
            description_msgid='gvSIGi18n_TRATraduccion_attr_cadenaTraducida_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Cadena traducida al Idioma.",
        duplicates="0",
        label2="Translation",
        ea_localid="311",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="String translated to the Language.",
        containment="Not Specified",
        ea_guid="{E3340BC4-DCC7-49a3-AB41-C4EB29E64EC1}",
        position="5",
        owner_class_name="TRATraduccion",
        label="Traduccion"
    ),

    StringField(
        name='estadoTraduccion',
        widget=SelectionWidget(
            label="Estado de Traduccion",
            label2="Translation State",
            description="El estado de la Traduccion, como Pendiente, Traducida, Revisada o Definitiva.",
            description2="Translation State, as Pending, Translated, Reviewed or Definitive.",
            label_msgid='gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label',
            description_msgid='gvSIGi18n_TRATraduccion_attr_estadoTraduccion_help',
            i18n_domain='gvSIGi18n',
        ),
        description="El estado de la Traduccion, como Pendiente, Traducida, Revisada o Definitiva.",
        vocabulary=['Pendiente','Traducida','Revisada','Definitiva',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Pendiente', 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Traducida', 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Revisada', 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Definitiva'],
        label2="Translation State",
        ea_localid="310",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Translation State, as Pending, Translated, Reviewed or Definitive.",
        ea_guid="{D681AA6B-2793-4d66-9BF7-1762AAA81CA5}",
        vocabulary2=['Pending','Translated','Reviewed','Definitive',],
        scale="0",
        label="Estado de Traduccion",
        length="0",
        containment="Not Specified",
        position="3",
        owner_class_name="TRATraduccion"
    ),

    StringField(
        name='fechaTraduccionTextual',
        widget=StringWidget(
            label="Fecha de Traduccion",
            label2="Translation Date",
            description="La fecha en que la Cadena fue traducida al Idioma.",
            description2="Date when the String was translated to the Language.",
            label_msgid='gvSIGi18n_TRATraduccion_attr_fechaTraduccionTextual_label',
            description_msgid='gvSIGi18n_TRATraduccion_attr_fechaTraduccionTextual_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="La fecha en que la Cadena fue traducida al Idioma.",
        duplicates="0",
        label2="Translation Date",
        ea_localid="1335",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="Date when the String was translated to the Language.",
        containment="Not Specified",
        ea_guid="{B62B3CB4-0EAC-4e31-8FA4-E06046DEDB9E}",
        position="8",
        owner_class_name="TRATraduccion",
        label="Fecha de Traduccion"
    ),

    StringField(
        name='usuarioTraductor',
        widget=StringWidget(
            label="Traductor",
            label2="Translator",
            description="Usuario que ha traducido la Cadena al Idioma.",
            description2="User who translated this string into this language.",
            label_msgid='gvSIGi18n_TRATraduccion_attr_usuarioTraductor_label',
            description_msgid='gvSIGi18n_TRATraduccion_attr_usuarioTraductor_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Usuario que ha traducido la Cadena al Idioma.",
        duplicates="0",
        label2="Translator",
        ea_localid="313",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="User who translated this string into this language.",
        containment="Not Specified",
        ea_guid="{E6E7E23E-C722-4324-A8B1-0DC4DA6B6EB6}",
        position="10",
        owner_class_name="TRATraduccion",
        label="Traductor"
    ),

    StringField(
        name='fechaRevisionTextual',
        widget=StringWidget(
            label="Fecha de Revision",
            label2="Review Date",
            description="La fecha en que reviso la Traduccion de la Cadena al Idioma.",
            description2="The date when the String Translation to the Language was reviewed.",
            label_msgid='gvSIGi18n_TRATraduccion_attr_fechaRevisionTextual_label',
            description_msgid='gvSIGi18n_TRATraduccion_attr_fechaRevisionTextual_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="La fecha en que reviso la Traduccion de la Cadena al Idioma.",
        duplicates="0",
        label2="Review Date",
        ea_localid="1336",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="The date when the String Translation to the Language was reviewed.",
        containment="Not Specified",
        ea_guid="{F3E84661-ADAA-427f-B5CD-729A33244458}",
        position="11",
        owner_class_name="TRATraduccion",
        label="Fecha de Revision"
    ),

    StringField(
        name='usuarioRevisor',
        widget=StringWidget(
            label="Revisor",
            label2="Reviewer",
            description="Usuario que reviso la Traduccion de la Cadena al Idioma.",
            description2="User who reviewd the String Translation to the Language.",
            label_msgid='gvSIGi18n_TRATraduccion_attr_usuarioRevisor_label',
            description_msgid='gvSIGi18n_TRATraduccion_attr_usuarioRevisor_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Usuario que reviso la Traduccion de la Cadena al Idioma.",
        duplicates="0",
        label2="Reviewer",
        ea_localid="315",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="User who reviewd the String Translation to the Language.",
        containment="Not Specified",
        ea_guid="{6BFF5745-AFFD-468a-A2DC-6520395136A8}",
        position="12",
        owner_class_name="TRATraduccion",
        label="Revisor"
    ),

    StringField(
        name='fechaDefinitivoTextual',
        widget=StringWidget(
            label="Fecha Definitiva",
            label2="Definitive Date",
            description="""La fecha en que la Traduccion al Idioma se bloqueo como definitiva.
            The date when the translation into the Language was locked as definitive.""",
            label_msgid='gvSIGi18n_TRATraduccion_attr_fechaDefinitivoTextual_label',
            description_msgid='gvSIGi18n_TRATraduccion_attr_fechaDefinitivoTextual_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="""La fecha en que la Traduccion al Idioma se bloqueo como definitiva.
        The date when the translation into the Language was locked as definitive.""",
        duplicates="0",
        label2="Definitive Date",
        ea_localid="1337",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        containment="Not Specified",
        ea_guid="{140F4C12-633E-499d-BAF7-6AC9AE8791EB}",
        position="13",
        owner_class_name="TRATraduccion",
        label="Fecha Definitiva"
    ),

    StringField(
        name='usuarioCoordinador',
        widget=StringWidget(
            label="Coordinador",
            label2="Coordinator",
            description="Usuario con capacidades de Coordinador que hizo Definitiva la traduccion de la cadena al idioma.",
            description2="User with Coordinator capabilities, who made Definitive the string translation into the language.",
            label_msgid='gvSIGi18n_TRATraduccion_attr_usuarioCoordinador_label',
            description_msgid='gvSIGi18n_TRATraduccion_attr_usuarioCoordinador_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Usuario con capacidades de Coordinador que hizo Definitiva la traduccion de la cadena al idioma.",
        duplicates="0",
        label2="Coordinator",
        ea_localid="1331",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="User with Coordinator capabilities, who made Definitive the string translation into the language.",
        containment="Not Specified",
        ea_guid="{075407C5-F759-47ec-AA8C-FFDB360AF510}",
        position="15",
        owner_class_name="TRATraduccion",
        label="Coordinador"
    ),

    StringField(
        name='idCadena',
        widget=StringWidget(
            label="Id Cadena",
            label2="String Id",
            description="El identificador (interno) de la Cadena a traducir.",
            description2="The (internal) identifier of the String to translate.",
            label_msgid='gvSIGi18n_TRATraduccion_attr_idCadena_label',
            description_msgid='gvSIGi18n_TRATraduccion_attr_idCadena_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="El identificador (interno) de la Cadena a traducir.",
        duplicates="0",
        label2="String Id",
        ea_localid="319",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="The (internal) identifier of the String to translate.",
        containment="Not Specified",
        ea_guid="{0039F177-5DA5-4244-91D1-4C9899F8C166}",
        position="17",
        owner_class_name="TRATraduccion",
        label="Id Cadena"
    ),

    StringField(
        name='estadoCadena',
        widget=SelectionWidget(
            label="Estado de la Cadena",
            label2="String State",
            description="Estado de la Cadena, como Activa o Inactiva.",
            description2="String State, as Active or Inactive.",
            label_msgid='gvSIGi18n_TRATraduccion_attr_estadoCadena_label',
            description_msgid='gvSIGi18n_TRATraduccion_attr_estadoCadena_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Estado de la Cadena, como Activa o Inactiva.",
        vocabulary=['Inactiva','Activa',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRATraduccion_attr_estadoCadena_option_Inactiva', 'gvSIGi18n_TRATraduccion_attr_estadoCadena_option_Activa'],
        label2="String State",
        ea_localid="309",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="String State, as Active or Inactive.",
        ea_guid="{0F959494-7D71-40cc-92E4-1E244CAFA363}",
        vocabulary2=['Inactive','Active',],
        scale="0",
        label="Estado de la Cadena",
        length="0",
        containment="Not Specified",
        position="2",
        owner_class_name="TRATraduccion"
    ),

    StringField(
        name='nombresModulos',
        widget=StringWidget(
            label="Modulos",
            label2="Modules",
            description="Nombres de los Modulos en los que se usa esta cadena.",
            description2="Names of the Modules using this String.",
            label_msgid='gvSIGi18n_TRATraduccion_attr_nombresModulos_label',
            description_msgid='gvSIGi18n_TRATraduccion_attr_nombresModulos_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Nombres de los Modulos en los que se usa esta cadena.",
        duplicates="0",
        label2="Modules",
        ea_localid="725",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="Names of the Modules using this String.",
        containment="Not Specified",
        ea_guid="{F0B3B52D-CCE4-44df-AA40-8BE97DFA8BE1}",
        position="4",
        owner_class_name="TRATraduccion",
        label="Modulos"
    ),

    TextField(
        name='comentario',
        widget=TextAreaWidget(
            label="Comentario",
            label2="Comment",
            description="Comentarios acerca de esta traduccion.",
            description2="Comments to this translation.",
            label_msgid='gvSIGi18n_TRATraduccion_attr_comentario_label',
            description_msgid='gvSIGi18n_TRATraduccion_attr_comentario_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Comentarios acerca de esta traduccion.",
        duplicates="0",
        label2="Comment",
        ea_localid="693",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="Comments to this translation.",
        containment="Not Specified",
        ea_guid="{49F28A8C-A23F-4328-AAD5-494C2832C49A}",
        position="14",
        owner_class_name="TRATraduccion",
        label="Comentario"
    ),

    StringField(
        name='indicadoresPO',
        widget=StringWidget(
            label="Indicadores para GNU gettext PO",
            label2="GNU gettext PO flags",
            description="Indicadores utilizados por GNU gettext PO , como fuzzy e indicacion que la cadena de una cadena de formateo de un lenguage de programacion especifico.",
            description2="Flags used by GNU gettext PO, like fuzzy and indicators that the string is a formatting string in a specific programming language.",
            label_msgid='gvSIGi18n_TRATraduccion_attr_indicadoresPO_label',
            description_msgid='gvSIGi18n_TRATraduccion_attr_indicadoresPO_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Indicadores utilizados por GNU gettext PO , como fuzzy e indicacion que la cadena de una cadena de formateo de un lenguage de programacion especifico.",
        duplicates="0",
        label2="GNU gettext PO flags",
        ea_localid="1492",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="Flags used by GNU gettext PO, like fuzzy and indicators that the string is a formatting string in a specific programming language.",
        containment="Not Specified",
        ea_guid="{7836B327-05EE-4df9-8F0C-EF4CBE063312}",
        position="9",
        owner_class_name="TRATraduccion",
        label="Indicadores para GNU gettext PO"
    ),

    TextField(
        name='historia',
        widget=TextAreaWidget(
            label="Historia",
            label2="History",
            description="Historia de cambios a la traduccion de la cadena al idioma.",
            description2="History of changes to the string's translation into the Language.",
            label_msgid='gvSIGi18n_TRATraduccion_attr_historia_label',
            description_msgid='gvSIGi18n_TRATraduccion_attr_historia_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Historia de cambios a la traduccion de la cadena al idioma.",
        duplicates="0",
        label2="History",
        ea_localid="318",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="History of changes to the string's translation into the Language.",
        containment="Not Specified",
        ea_guid="{A6F66985-751D-423f-98CF-635384D8ABD4}",
        position="16",
        owner_class_name="TRATraduccion",
        label="Historia"
    ),

    IntegerField(
        name='contadorCambios',
        widget=IntegerField._properties['widget'](
            label="Contador de Cambios",
            label2="Change Counter",
            description="Contador de cambios realizados a lo largo del tiempo. Util para descubrir si han tenido lugar cambios desde que se leyeron los datos del elemento.",
            description2="Counter of changes over time. Useful to learn if any changes happened since the reading of the element information.",
            label_msgid='gvSIGi18n_TRATraduccion_attr_contadorCambios_label',
            description_msgid='gvSIGi18n_TRATraduccion_attr_contadorCambios_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Contador de cambios realizados a lo largo del tiempo. Util para descubrir si han tenido lugar cambios desde que se leyeron los datos del elemento.",
        duplicates="0",
        label2="Change Counter",
        ea_localid="1582",
        derived="0",
        precision=0,
        collection="false",
        styleex="IsLiteral=0;volatile=0;",
        description2="Counter of changes over time. Useful to learn if any changes happened since the reading of the element information.",
        ea_guid="{21C32FA2-F89A-439b-9D80-587F1A7F34F1}",
        read_only="True",
        scale="0",
        default="0",
        label="Contador de Cambios",
        length="0",
        is_change_counter="True",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        position="8",
        owner_class_name="TRATraduccion",
        exclude_from_copyconfig="True"
    ),

    StringField(
        name='fechaCreacionTextual',
        widget=StringWidget(
            label="Fecha de Creacion",
            label2="Creation Date",
            description="La fecha en que la Traduccion al lenguage fue creada, bien como Traducida o como Pendiente.",
            description2="Date when the translation into the Language was created, either in Translated or Pending state.",
            label_msgid='gvSIGi18n_TRATraduccion_attr_fechaCreacionTextual_label',
            description_msgid='gvSIGi18n_TRATraduccion_attr_fechaCreacionTextual_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="La fecha en que la Traduccion al lenguage fue creada, bien como Traducida o como Pendiente.",
        duplicates="0",
        label2="Creation Date",
        ea_localid="1470",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="Date when the translation into the Language was created, either in Translated or Pending state.",
        containment="Not Specified",
        ea_guid="{38A791EF-7F1A-4824-86D9-4C670C7643C9}",
        position="6",
        owner_class_name="TRATraduccion",
        label="Fecha de Creacion"
    ),

    StringField(
        name='usuarioCreador',
        widget=StringWidget(
            label="Creador",
            label2="Creator",
            description="Usuario que creo la traduccion al lenguage, bien en estado Traducida o Pendiente, durante un proceso de importaciono creacion de lenguage.",
            description2="User who created the translation into the language in Translated or Pending state, during an import or language creation process.",
            label_msgid='gvSIGi18n_TRATraduccion_attr_usuarioCreador_label',
            description_msgid='gvSIGi18n_TRATraduccion_attr_usuarioCreador_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Usuario que creo la traduccion al lenguage, bien en estado Traducida o Pendiente, durante un proceso de importaciono creacion de lenguage.",
        duplicates="0",
        label2="Creator",
        ea_localid="1471",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="User who created the translation into the language in Translated or Pending state, during an import or language creation process.",
        containment="Not Specified",
        ea_guid="{E2D4ACFF-A4BB-4dc9-A8B8-149E7033FB14}",
        position="7",
        owner_class_name="TRATraduccion",
        label="Creador"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRATraduccion_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAArquetipo, 'schema', Schema(())).copy() + \
    getattr(TRATraduccion_Operaciones, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRATraduccion(OrderedBaseFolder, TRAArquetipo, TRATraduccion_Operaciones):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAArquetipo,'__implements__',()),) + (getattr(TRATraduccion_Operaciones,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Traduccion'

    meta_type = 'TRATraduccion'
    portal_type = 'TRATraduccion'


    # Change Audit fields

    change_counter_field = 'contadorCambios'



    use_folder_tabs = 0

    allowed_content_types = [] + list(getattr(TRAArquetipo, 'allowed_content_types', [])) + list(getattr(TRATraduccion_Operaciones, 'allowed_content_types', []))
    filter_content_types             = 1
    global_allow                     = 0
    content_icon = 'tratraduccion.gif'
    immediate_view                   = 'Tabular'
    default_view                     = 'Tabular'
    suppl_views                      = ['Tabular',]
    typeDescription                  = "Traduccion de una de las Cadenas a uno de los Idiomas."
    typeDescMsgId                    =  'gvSIGi18n_TRATraduccion_help'
    archetype_name2                  = 'Translation'
    typeDescription2                 = '''Translation of one of the strings into one of the languages.'''
    archetype_name_msgid             = 'gvSIGi18n_TRATraduccion_label'
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
        'condition': """python:1"""
       },


       {'action': "string:${object_url}/MDDCacheStatus/",
        'category': "object_buttons",
        'id': 'mddcachestatus',
        'name': 'Cache',
        'permissions': ("View",),
        'condition': """python:1"""
       },


       {'action': "string:${object_url}/MDDChanges",
        'category': "object_buttons",
        'id': 'mddchanges',
        'name': 'Changes',
        'permissions': ("View",),
        'condition': """python:1"""
       },


       {'action': "string:${object_url}/TRAConfigureProfiling_action",
        'category': "object_buttons",
        'id': 'TRA_configure_profiling',
        'name': 'Configure Profiling',
        'permissions': ("ManagePortal",),
        'condition': """python:object.fUseCaseCheckDoable( 'Configure_ExecutionProfilingEnablement_TRACatalogo')"""
       },


       {'action': "string:$object_url/content_status_history",
        'category': "object",
        'id': 'content_status_history',
        'name': 'State',
        'permissions': ("View",),
        'condition': """python:0"""
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
        'condition': """python:object.fUseCaseCheckDoable( 'Inventory_TRAElemento')"""
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
        'condition': """python:object.fUseCaseCheckDoable( 'ReCatalog_TRAElemento')"""
       },


       {'action': "string:${object_url}/TRAResetPermissions_action",
        'category': "object_buttons",
        'id': 'TRA_reestablecerpermisos',
        'name': 'Reset Permissions',
        'permissions': ("View",),
        'condition': """python:object.fUseCaseCheckDoable( 'ResetPermissions_TRAElemento')"""
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
        'condition': """python:object.fUseCaseCheckDoable( 'Permissions_on_any_TRA_element')"""
       },


    )

    _at_rename_after_creation = True

    schema = TRATraduccion_schema

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

    security.declarePublic('manage_afterAdd')
    def manage_afterAdd(self,item,container):
        """
        """
        
        return TRATraduccion_Operaciones.pHandle_manage_afterAdd( self, item, container)

    security.declarePublic('manage_beforeDelete')
    def manage_beforeDelete(self,item,container):
        """
        """
        
        return TRAArquetipo.manage_beforeDelete( self, item, container)

    security.declarePublic('manage_pasteObjects')
    def manage_pasteObjects(self,cb_copy_data,REQUEST):
        """
        """
        
        return self.pHandle_manage_pasteObjects( cb_copy_data, REQUEST)

    security.declarePublic('reindexObject')
    def reindexObject(self,idxs=[]):
        """
        """
        
        return TRATraduccion_Operaciones.pHandle_reindexObject( self, idxs)
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata', 'sharing', 'folderContents']:
            a['visible'] = 0
    return fti

registerType(TRATraduccion, PROJECTNAME)
# end of class TRATraduccion

##code-section module-footer #fill in your manual code here
##/code-section module-footer



