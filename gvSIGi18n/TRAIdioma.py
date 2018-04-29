# -*- coding: utf-8 -*-
#
# File: TRAIdioma.py
#
# Copyright (c) 2010 by Conselleria de Infraestructuras y Transporte de la
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
from TRAIdioma_Operaciones import TRAIdioma_Operaciones
from Products.gvSIGi18n.TRAConRegistroActividad import TRAConRegistroActividad
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    BooleanField(
        name='permiteLeer',
        widget=BooleanField._properties['widget'](
            label="Permite ver Idioma",
            label2="Allow to see Language",
            description="Si Verdadero, entonces los usuarios puede ver el idioma. Puede ser Falso durante  procesos de importacion largos, o por indicacion del coordinador.",
            description2="If True, then the users may see  the language. It may be False during long import processes or by coordinator request.",
            label_msgid='gvSIGi18n_TRAIdioma_attr_permiteLeer_label',
            description_msgid='gvSIGi18n_TRAIdioma_attr_permiteLeer_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, entonces los usuarios puede ver el idioma. Puede ser Falso durante  procesos de importacion largos, o por indicacion del coordinador.",
        duplicates="0",
        label2="Allow to see Language",
        ea_localid="1576",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="If True, then the users may see  the language. It may be False during long import processes or by coordinator request.",
        ea_guid="{76F8837E-DEC9-4f32-B6CA-0F04ABE405F1}",
        read_only="True",
        scale="0",
        default="True",
        label="Permite ver Idioma",
        length="0",
        containment="Not Specified",
        position="18",
        owner_class_name="TRAIdioma",
        exclude_from_exportconfig="True",
        exclude_from_copyconfig="True"
    ),

    BooleanField(
        name='permiteModificar',
        widget=BooleanField._properties['widget'](
            label="Permite Modificar Idioma",
            label2="Allow Changes to Language",
            description="Si Verdadero, entonces el usuario puede realizar los cambios a los que permite sus roles en el idioma. Si Falso, entonces no puede realizar cambios en el idioma,  Puede ocurrir durante  procesos de importacion largos, o por indicacion del coordinador.",
            description2="If True, then the user may perform  the changes authorized by the roles held on the language. If False, then the user can not make changes to the language. This may happen during long import processes or coordinator request.",
            label_msgid='gvSIGi18n_TRAIdioma_attr_permiteModificar_label',
            description_msgid='gvSIGi18n_TRAIdioma_attr_permiteModificar_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, entonces el usuario puede realizar los cambios a los que permite sus roles en el idioma. Si Falso, entonces no puede realizar cambios en el idioma,  Puede ocurrir durante  procesos de importacion largos, o por indicacion del coordinador.",
        duplicates="0",
        label2="Allow Changes to Language",
        ea_localid="1573",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="If True, then the user may perform  the changes authorized by the roles held on the language. If False, then the user can not make changes to the language. This may happen during long import processes or coordinator request.",
        ea_guid="{45A11E6E-E5C8-405a-9702-9BF365FFD3DE}",
        read_only="True",
        scale="0",
        default="True",
        label="Permite Modificar Idioma",
        length="0",
        containment="Not Specified",
        position="16",
        owner_class_name="TRAIdioma",
        exclude_from_exportconfig="True",
        exclude_from_copyconfig="True"
    ),

    ComputedField(
        name='estaBloqueado',
        widget=ComputedField._properties['widget'](
            label="Bloqueado",
            label2="Locked",
            description="Si Verdadero, entonces el usuario no puede realizar los cambios a los que permite sus roles en el idioma. Si Falso, entonces puede realizar cambios en el idioma,  Puede ocurrir durante  procesos de importacion largos, o por indicacion del coordinador.",
            description2="If True, then the user may not  perform  the changes authorized by the roles held on the language. If False, then the user can make changes to the language. This may happen during long import processes or coordinator request.",
            label_msgid='gvSIGi18n_TRAIdioma_attr_estaBloqueado_label',
            description_msgid='gvSIGi18n_TRAIdioma_attr_estaBloqueado_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, entonces el usuario no puede realizar los cambios a los que permite sus roles en el idioma. Si Falso, entonces puede realizar cambios en el idioma,  Puede ocurrir durante  procesos de importacion largos, o por indicacion del coordinador.",
        duplicates="0",
        label2="Locked",
        ea_localid="1593",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="If True, then the user may not  perform  the changes authorized by the roles held on the language. If False, then the user can make changes to the language. This may happen during long import processes or coordinator request.",
        ea_guid="{665EC558-519B-4f00-95B1-E468BC7C365E}",
        scale="0",
        label="Bloqueado",
        length="0",
        containment="Not Specified",
        position="17",
        owner_class_name="TRAIdioma",
        expression="not context.fAllowWrite()",
        computed_types="boolean",
        exclude_from_copyconfig="True",
        exclude_from_exportconfig="True"
    ),

    StringField(
        name='codigoIdiomaEnGvSIG',
        widget=StringWidget(
            label="Codigo de Idioma en gvSIG",
            label2="Language code in gvSIG",
            description="Codigo de Idioma en gvSIG, que soporta algunos idiomas para los que no existe (todavia) un codigo internacional.",
            description2="Language code in gvSIG, as gvSIG supports some languages for which there is no international code (yet).",
            label_msgid='gvSIGi18n_TRAIdioma_attr_codigoIdiomaEnGvSIG_label',
            description_msgid='gvSIGi18n_TRAIdioma_attr_codigoIdiomaEnGvSIG_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Codigo de Idioma en gvSIG, que soporta algunos idiomas para los que no existe (todavia) un codigo internacional.",
        duplicates="0",
        label2="Language code in gvSIG",
        ea_localid="305",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="Language code in gvSIG, as gvSIG supports some languages for which there is no international code (yet).",
        containment="Not Specified",
        ea_guid="{C8E57D89-5CEC-48f0-B926-DA83FCDC9EAD}",
        position="0",
        owner_class_name="TRAIdioma",
        label="Codigo de Idioma en gvSIG"
    ),

    StringField(
        name='codigoInternacionalDeIdioma',
        widget=StringWidget(
            label="Codigo internacional de Idioma",
            label2="International language code",
            description="Codigo internacional estandard de Idioma, segun las convenciones I18N.",
            description2="Standard international language code,according to the I18N conventions.",
            label_msgid='gvSIGi18n_TRAIdioma_attr_codigoInternacionalDeIdioma_label',
            description_msgid='gvSIGi18n_TRAIdioma_attr_codigoInternacionalDeIdioma_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Codigo internacional estandard de Idioma, segun las convenciones I18N.",
        duplicates="0",
        label2="International language code",
        ea_localid="306",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="Standard international language code,according to the I18N conventions.",
        containment="Not Specified",
        ea_guid="{32F6E759-E25D-4145-8961-613BE5F817F3}",
        position="1",
        owner_class_name="TRAIdioma",
        label="Codigo internacional de Idioma"
    ),

    StringField(
        name='nombreEnInglesDeIdioma',
        widget=StringWidget(
            label="Nombre en ingles",
            label2="English name",
            description="Nombre del idioma, expresado en idioma ingles.",
            description2="Language name, expressed in english language.",
            label_msgid='gvSIGi18n_TRAIdioma_attr_nombreEnInglesDeIdioma_label',
            description_msgid='gvSIGi18n_TRAIdioma_attr_nombreEnInglesDeIdioma_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Nombre del idioma, expresado en idioma ingles.",
        duplicates="0",
        label2="English name",
        ea_localid="1531",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="Language name, expressed in english language.",
        containment="Not Specified",
        ea_guid="{B6FA4A49-ABED-41d7-B35E-4031AD105F59}",
        position="2",
        owner_class_name="TRAIdioma",
        label="Nombre en ingles"
    ),

    StringField(
        name='nombreNativoDeIdioma',
        widget=StringWidget(
            label="Nombre propio del idioma",
            label2="Native language name",
            description="Nombre del idioma expresado en su idioma.",
            description2="Language name expressed in the native language.",
            label_msgid='gvSIGi18n_TRAIdioma_attr_nombreNativoDeIdioma_label',
            description_msgid='gvSIGi18n_TRAIdioma_attr_nombreNativoDeIdioma_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Nombre del idioma expresado en su idioma.",
        duplicates="0",
        label2="Native language name",
        ea_localid="1163",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="Language name expressed in the native language.",
        containment="Not Specified",
        ea_guid="{27989BCF-643E-4730-87F2-939F42EA6F38}",
        position="3",
        owner_class_name="TRAIdioma",
        label="Nombre propio del idioma"
    ),

    StringField(
        name='modoSeleccionBandera',
        widget=SelectionWidget(
            label="Modo seleccion Bandera",
            label2="Flag selecction mode",
            description="Criterio para seleccion de la bandera especifica para este idioma: la bandera seleccionada por la plataforma Zope/Plone, una bandera Plone con nombre especifico, o una imagen adjunta.",
            description2="Criteria to select the flag to display for this language: the flag seleccted by the Zope/Plone platform, other Plone flag with a specified name, or an Image attachment.",
            label_msgid='gvSIGi18n_TRAIdioma_attr_modoSeleccionBandera_label',
            description_msgid='gvSIGi18n_TRAIdioma_attr_modoSeleccionBandera_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Criterio para seleccion de la bandera especifica para este idioma: la bandera seleccionada por la plataforma Zope/Plone, una bandera Plone con nombre especifico, o una imagen adjunta.",
        vocabulary=['Plone','Especifica','Adjunta',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAIdioma_attr_modoSeleccionBandera_option_Plone', 'gvSIGi18n_TRAIdioma_attr_modoSeleccionBandera_option_Especifica', 'gvSIGi18n_TRAIdioma_attr_modoSeleccionBandera_option_Adjunta'],
        label2="Flag selecction mode",
        ea_localid="1591",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Criteria to select the flag to display for this language: the flag seleccted by the Zope/Plone platform, other Plone flag with a specified name, or an Image attachment.",
        ea_guid="{A8A54230-C7CD-43d1-A5F4-CA882CC2B33A}",
        vocabulary2=['Plone','Specified','Attached',],
        scale="0",
        default="Plone",
        label="Modo seleccion Bandera",
        length="0",
        containment="Not Specified",
        position="5",
        owner_class_name="TRAIdioma"
    ),

    StringField(
        name='iconoBanderaIdioma',
        widget=StringWidget(
            label="Icono de la Bandera",
            label2="Flag Icon",
            description="Nombre de una bandera displonible en  la plataforma Zope/Plone, o la identidad de una imagen adjunta al lenguage, a utilizar como bandera para el idioma. Ha de ser de dimensiones iguales o menores a 16x16 pixels, preferentemente con fondo transparente.",
            description2="Name of a flag available in the Zope/Plone platform, or the id of an image attached to the language, to use as the flag for the language. Must have dimensions equal or smaller than 16 x 16 pixels, prefereably with transparent background.",
            label_msgid='gvSIGi18n_TRAIdioma_attr_iconoBanderaIdioma_label',
            description_msgid='gvSIGi18n_TRAIdioma_attr_iconoBanderaIdioma_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Nombre de una bandera displonible en  la plataforma Zope/Plone, o la identidad de una imagen adjunta al lenguage, a utilizar como bandera para el idioma. Ha de ser de dimensiones iguales o menores a 16x16 pixels, preferentemente con fondo transparente.",
        duplicates="0",
        label2="Flag Icon",
        ea_localid="1581",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="Name of a flag available in the Zope/Plone platform, or the id of an image attached to the language, to use as the flag for the language. Must have dimensions equal or smaller than 16 x 16 pixels, prefereably with transparent background.",
        containment="Not Specified",
        ea_guid="{288C7CCE-8ECB-48bb-89F3-C7A64259AFEB}",
        position="6",
        owner_class_name="TRAIdioma",
        label="Icono de la Bandera"
    ),

    StringField(
        name='codigoIdiomaReferencia',
        widget=SelectionWidget(
            label="Codigo de Idioma de referencia",
            label2="Reference Language code",
            description="Codigo de Idioma de referencia, que se incluira por defecto en exportaciones en formato Java .properties, y cuyas traducciones se incluyen como linea Default en exportaciones GNUgettext PO.",
            description2="Reference Language code, to be included by default when exporting as Java .properties, and to be included in the Default line when exporting GNUgettext PO.",
            label_msgid='gvSIGi18n_TRAIdioma_attr_codigoIdiomaReferencia_label',
            description_msgid='gvSIGi18n_TRAIdioma_attr_codigoIdiomaReferencia_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Codigo de Idioma de referencia, que se incluira por defecto en exportaciones en formato Java .properties, y cuyas traducciones se incluyen como linea Default en exportaciones GNUgettext PO.",
        vocabulary='fIdiomasReferenciaVocabulary',
        duplicates="0",
        label2="Reference Language code",
        ea_localid="1480",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Reference Language code, to be included by default when exporting as Java .properties, and to be included in the Default line when exporting GNUgettext PO.",
        ea_guid="{7E793C73-BE06-4e83-913D-FD9794AF12BC}",
        scale="0",
        default="en",
        label="Codigo de Idioma de referencia",
        length="0",
        containment="Not Specified",
        position="13",
        owner_class_name="TRAIdioma"
    ),

    StringField(
        name='ambitoDelIdioma',
        widget=SelectionWidget(
            label="Ambito",
            label2="Scope",
            description="Indica si el idioma es de uso general, o es un caso especial en de otro idioma en un Pais, o si es una variacion de otro idioma de un pais. Si no es de uso general, debera referenciar a un idioma base.",
            description2="Whether the language is of genral use, or is a special use of a language in a given country, or  a variation of a country specific Language.  If not of general use, the language must refer to a base language.",
            label_msgid='gvSIGi18n_TRAIdioma_attr_ambitoDelIdioma_label',
            description_msgid='gvSIGi18n_TRAIdioma_attr_ambitoDelIdioma_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Indica si el idioma es de uso general, o es un caso especial en de otro idioma en un Pais, o si es una variacion de otro idioma de un pais. Si no es de uso general, debera referenciar a un idioma base.",
        vocabulary=['General','Pais','Variacion',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAIdioma_attr_ambitoDelIdioma_option_General', 'gvSIGi18n_TRAIdioma_attr_ambitoDelIdioma_option_Pais', 'gvSIGi18n_TRAIdioma_attr_ambitoDelIdioma_option_Variacion'],
        label2="Scope",
        ea_localid="1185",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Whether the language is of genral use, or is a special use of a language in a given country, or  a variation of a country specific Language.  If not of general use, the language must refer to a base language.",
        ea_guid="{1998DD39-C104-403c-B6F5-31F7870D527D}",
        vocabulary2=['General','Country','Variation',],
        scale="0",
        default="General",
        label="Ambito",
        length="0",
        containment="Not Specified",
        position="4",
        owner_class_name="TRAIdioma"
    ),

    StringField(
        name='fallbackDeIdiomas',
        widget=StringWidget(
            label="Fallback de idiomas",
            label2="Is fall back for languages",
            description="Idiomas para los que este es una sustitucion aceptable, en ausencia de una traduccion propia. Este dato aparece en los ficheros exportados en formato GNUgettext PO.",
            description2="Languages for which this is an acceptable fallback, in case they lack their own tranlation. This information appears in the files exported as GNU gettext PO format.",
            label_msgid='gvSIGi18n_TRAIdioma_attr_fallbackDeIdiomas_label',
            description_msgid='gvSIGi18n_TRAIdioma_attr_fallbackDeIdiomas_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Idiomas para los que este es una sustitucion aceptable, en ausencia de una traduccion propia. Este dato aparece en los ficheros exportados en formato GNUgettext PO.",
        duplicates="0",
        label2="Is fall back for languages",
        ea_localid="1169",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="Languages for which this is an acceptable fallback, in case they lack their own tranlation. This information appears in the files exported as GNU gettext PO format.",
        containment="Not Specified",
        ea_guid="{9FF87A07-8C98-4b8b-9CD3-38DCC86A29D9}",
        position="14",
        owner_class_name="TRAIdioma",
        label="Fallback de idiomas"
    ),

    StringField(
        name='equipoTraductor',
        widget=StringWidget(
            label="Equipo del idioma",
            label2="Language team",
            description="Equipo a cargo de traducir al idioma. Este dato aparece en los ficheros de exportacion de tipo GNUgettext PO.",
            description2="Team in charge of translations to the language. This information appears in the exported files of GNUgettext PO format.",
            label_msgid='gvSIGi18n_TRAIdioma_attr_equipoTraductor_label',
            description_msgid='gvSIGi18n_TRAIdioma_attr_equipoTraductor_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Equipo a cargo de traducir al idioma. Este dato aparece en los ficheros de exportacion de tipo GNUgettext PO.",
        duplicates="0",
        label2="Language team",
        ea_localid="1158",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="Team in charge of translations to the language. This information appears in the exported files of GNUgettext PO format.",
        containment="Not Specified",
        ea_guid="{CD852AC8-F684-4a10-A1C9-9E3C5A72F7FE}",
        position="7",
        owner_class_name="TRAIdioma",
        label="Equipo del idioma"
    ),

    StringField(
        name='juegoDeCaracteresParaJavaProperties',
        widget=SelectionWidget(
            label="Juego de caracteres para exportacion como Java Properties",
            label2="Char set for export as Java Properties files",
            description="Juego de caracteres en que se han de codificar los ficheros exportados en formatoJava .properties.  Usualmente toma el valor=UTF-8",
            description2="Charset to be used to encode exported files in Java Properties format. Usually takes the value=UTF-8.",
            label_msgid='gvSIGi18n_TRAIdioma_attr_juegoDeCaracteresParaJavaProperties_label',
            description_msgid='gvSIGi18n_TRAIdioma_attr_juegoDeCaracteresParaJavaProperties_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Juego de caracteres en que se han de codificar los ficheros exportados en formatoJava .properties.  Usualmente toma el valor=UTF-8",
        vocabulary='fEncodingsForLanguageVocabulary',
        duplicates="0",
        label2="Char set for export as Java Properties files",
        ea_localid="1167",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Charset to be used to encode exported files in Java Properties format. Usually takes the value=UTF-8.",
        ea_guid="{74268AAB-89C3-41c4-9214-E0ADC26DCCB1}",
        scale="0",
        default="utf-8",
        label="Juego de caracteres para exportacion como Java Properties",
        length="0",
        containment="Not Specified",
        position="8",
        owner_class_name="TRAIdioma"
    ),

    StringField(
        name='juegoDeCaracteresParaPO',
        widget=SelectionWidget(
            label="Juego de caracteres para exportacion como GNU gettext PO",
            label2="Char set for export as PO files",
            description="Juego de caracteres en que se han de codificar los ficheros exportados en formato GNUgettet PO.  Usualmente toma el valor=UTF-8.",
            description2="Charset to be used to encode exported files in GNUgettext PO format. Usually takes the value=UTF-8",
            label_msgid='gvSIGi18n_TRAIdioma_attr_juegoDeCaracteresParaPO_label',
            description_msgid='gvSIGi18n_TRAIdioma_attr_juegoDeCaracteresParaPO_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Juego de caracteres en que se han de codificar los ficheros exportados en formato GNUgettet PO.  Usualmente toma el valor=UTF-8.",
        vocabulary='fEncodingsForLanguageVocabulary',
        duplicates="0",
        label2="Char set for export as PO files",
        ea_localid="1160",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Charset to be used to encode exported files in GNUgettext PO format. Usually takes the value=UTF-8",
        ea_guid="{D4D30879-EC3B-44d0-B1BC-9F41CD6AB3D4}",
        scale="0",
        default="utf-8",
        label="Juego de caracteres para exportacion como GNU gettext PO",
        length="0",
        containment="Not Specified",
        position="9",
        owner_class_name="TRAIdioma"
    ),

    StringField(
        name='codificacionTransferenciaContenido',
        widget=StringWidget(
            label="Codificacion de transferencia de contenido",
            label2="Content transfer encoding",
            description="Equipo a cargo de traducir al idioma. Este dato aparece en los ficheros de exportacion de tipo GNUgettext PO. Usualmente toma el valor=8bit",
            description2="Iinformation that appears in the exported files with GNUgettext PO format. Usually takes the value=8bit",
            label_msgid='gvSIGi18n_TRAIdioma_attr_codificacionTransferenciaContenido_label',
            description_msgid='gvSIGi18n_TRAIdioma_attr_codificacionTransferenciaContenido_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Equipo a cargo de traducir al idioma. Este dato aparece en los ficheros de exportacion de tipo GNUgettext PO. Usualmente toma el valor=8bit",
        duplicates="0",
        label2="Content transfer encoding",
        ea_localid="1165",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Iinformation that appears in the exported files with GNUgettext PO format. Usually takes the value=8bit",
        ea_guid="{D7F31A8B-9F9E-4c1d-BF6E-553B70A57151}",
        scale="0",
        default="8bit",
        label="Codificacion de transferencia de contenido",
        length="0",
        containment="Not Specified",
        position="10",
        owner_class_name="TRAIdioma"
    ),

    StringField(
        name='formasPlurales',
        widget=StringWidget(
            label="Formas plurales",
            label2="Plural forms",
            description="Dato que aparece en los ficheros de exportacion de tipo GNUgettext PO. Usualmente toma el valor=nplurals=1; plural=0",
            description2="Information to be included in the files exported with GNU gettext PO format.",
            label_msgid='gvSIGi18n_TRAIdioma_attr_formasPlurales_label',
            description_msgid='gvSIGi18n_TRAIdioma_attr_formasPlurales_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Dato que aparece en los ficheros de exportacion de tipo GNUgettext PO. Usualmente toma el valor=nplurals=1; plural=0",
        duplicates="0",
        label2="Plural forms",
        ea_localid="1166",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Information to be included in the files exported with GNU gettext PO format.",
        ea_guid="{7DF90A0A-0E1A-433d-98FF-ECAA60ABBB80}",
        scale="0",
        default="nplurals=1; plural=0",
        label="Formas plurales",
        length="0",
        containment="Not Specified",
        position="11",
        owner_class_name="TRAIdioma"
    ),

    StringField(
        name='codificacionesPreferidas',
        widget=StringWidget(
            label="Codificaciones preferidas",
            label2="Preferred encodings",
            description="Dato que aparece en los ficheros de exportacion de tipo GNUgettext PO. Usualmente toma el valor=latin1 utf-8",
            description2="Iinformation that appears in the exported files of GNUgettext PO format. Usually takes the value=latin1 utf-8",
            label_msgid='gvSIGi18n_TRAIdioma_attr_codificacionesPreferidas_label',
            description_msgid='gvSIGi18n_TRAIdioma_attr_codificacionesPreferidas_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Dato que aparece en los ficheros de exportacion de tipo GNUgettext PO. Usualmente toma el valor=latin1 utf-8",
        duplicates="0",
        label2="Preferred encodings",
        ea_localid="1168",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Iinformation that appears in the exported files of GNUgettext PO format. Usually takes the value=latin1 utf-8",
        ea_guid="{A96E91EA-4C36-4101-AAFA-58CF1C633269}",
        scale="0",
        default="latin1 utf-8",
        label="Codificaciones preferidas",
        length="0",
        containment="Not Specified",
        position="12",
        owner_class_name="TRAIdioma"
    ),

    BooleanField(
        name='esIdiomaPrincipal',
        widget=BooleanField._properties['widget'](
            label="Es Idioma Principal",
            label2="Is Main Language",
            description="Las traducciones del Idioma Principal se exportaran a un archivo sin sufijo de idioma, por ejemplo si el idioma principal es es, el nombre del fichero sera  text.properties y no text_es.properties.",
            description2="The translations to the main language will be exported to files without language postfix, for example if the main language is en, the filename will be text.properties but not text_en.properties.",
            label_msgid='gvSIGi18n_TRAIdioma_attr_esIdiomaPrincipal_label',
            description_msgid='gvSIGi18n_TRAIdioma_attr_esIdiomaPrincipal_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Las traducciones del Idioma Principal se exportaran a un archivo sin sufijo de idioma, por ejemplo si el idioma principal es es, el nombre del fichero sera  text.properties y no text_es.properties.",
        duplicates="0",
        label2="Is Main Language",
        ea_localid="902",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="The translations to the main language will be exported to files without language postfix, for example if the main language is en, the filename will be text.properties but not text_en.properties.",
        ea_guid="{2C338549-66B6-457d-ADDA-2D8E63333740}",
        scale="0",
        default="False",
        label="Es Idioma Principal",
        length="0",
        containment="Not Specified",
        position="15",
        owner_class_name="TRAIdioma"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAIdioma_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAArquetipo, 'schema', Schema(())).copy() + \
    getattr(TRAIdioma_Operaciones, 'schema', Schema(())).copy() + \
    getattr(TRAConRegistroActividad, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAIdioma(OrderedBaseFolder, TRAArquetipo, TRAIdioma_Operaciones, TRAConRegistroActividad):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAArquetipo,'__implements__',()),) + (getattr(TRAIdioma_Operaciones,'__implements__',()),) + (getattr(TRAConRegistroActividad,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Idioma'

    meta_type = 'TRAIdioma'
    portal_type = 'TRAIdioma'


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



    allowed_content_types = [] + list(getattr(TRAArquetipo, 'allowed_content_types', [])) + list(getattr(TRAIdioma_Operaciones, 'allowed_content_types', [])) + list(getattr(TRAConRegistroActividad, 'allowed_content_types', []))
    filter_content_types             = 1
    global_allow                     = 0
    content_icon = 'traidioma.gif'
    immediate_view                   = 'Tabular'
    default_view                     = 'Tabular'
    suppl_views                      = ['Tabular',]
    typeDescription                  = "Uno de los Idiomas a los que se han de traducir las cadenas."
    typeDescMsgId                    =  'gvSIGi18n_TRAIdioma_help'
    archetype_name2                  = 'Language'
    typeDescription2                 = '''One of the languages to translate the strings into.'''
    archetype_name_msgid             = 'gvSIGi18n_TRAIdioma_label'
    factory_methods                  = None
    factory_enablers                 = None
    propagate_delete_impact_to       = None
    allow_discussion = False


    actions =  (


       {'action': "string:${object_url}/TRAExportarGvSIG",
        'category': "object_buttons",
        'id': 'TRA_export_language_for_gvSIG',
        'name': 'Export for gvSIG',
        'permissions': ("View",),
        'condition': """python:object.fUseCaseCheckDoable( 'Export')"""
       },


       {'action': "string:${object_url}/TRAConfirmarBloquearIdioma",
        'category': "object_buttons",
        'id': 'TRA_bloquear_idioma',
        'name': 'Lock Language',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fUseCaseCheckDoable( 'Lock_TRAIdioma')"""
       },


       {'action': "string:${object_url}/TRAConfirmarDesbloquearIdioma",
        'category': "object_buttons",
        'id': 'TRA_desbloquear_idioma',
        'name': 'Unlock Language',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fUseCaseCheckDoable( 'Unlock_TRAIdioma')"""
       },


       {'action': "string:${object_url}/TRACopiar_Traducciones",
        'category': "object_buttons",
        'id': 'TRACopyTranslations',
        'name': 'Copy Translations',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fUseCaseCheckDoable( 'Copy_Translations')"""
       },


       {'action': "string:$object_url/Editar",
        'category': "object",
        'id': 'edit',
        'name': 'Edit',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fAllowWrite()"""
       },


       {'action': "string:${object_url}/sharing",
        'category': "object",
        'id': 'local_roles',
        'name': 'Sharing',
        'permissions': ("Manage properties",),
        'condition': """python:object.fAllowWrite() and object.fRoleQuery_IsManagerOrCoordinator()"""
       },


       {'action': "string:${object_url}/Tabular",
        'category': "object",
        'id': 'view',
        'name': 'View',
        'permissions': ("View",),
        'condition': """python:1"""
       },


       {'action': "string:${object_url}/folder_listing",
        'category': "folder",
        'id': 'folderlisting',
        'name': 'Folder Listing',
        'permissions': ("View",),
        'condition': """python:0"""
       },


       {'action': "string:${object_url}/MDDChanges",
        'category': "object_buttons",
        'id': 'mddchanges',
        'name': 'Changes',
        'permissions': ("View",),
        'condition': """python:1"""
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
        'condition': """python:1"""
       },


       {'action': "string:$object_url/content_status_history",
        'category': "object",
        'id': 'content_status_history',
        'name': 'State',
        'permissions': ("View",),
        'condition': """python:0"""
       },


       {'action': "string:${object_url}/MDDCacheStatus/",
        'category': "object_buttons",
        'id': 'mddcachestatus',
        'name': 'Cache',
        'permissions': ("View",),
        'condition': """python:1"""
       },


    )

    _at_rename_after_creation = True

    schema = TRAIdioma_schema

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

    security.declarePublic('manage_afterAdd')
    def manage_afterAdd(self,item,container):
        """
        """
        
        return TRAIdioma_Operaciones.pHandle_manage_afterAdd( self, item, container)

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

    security.declarePublic('fIsUnlocked')
    def fIsUnlocked(self):
        """
        """
        
        return self.getPermiteModificar()

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

    security.declarePublic('fExtraLinks')
    def fExtraLinks(self):
        """
        """
        
        return TRAIdioma_Operaciones.fExtraLinks( self)
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata', 'folderContents']:
            a['visible'] = 0
    return fti

registerType(TRAIdioma, PROJECTNAME)
# end of class TRAIdioma

##code-section module-footer #fill in your manual code here
##/code-section module-footer



