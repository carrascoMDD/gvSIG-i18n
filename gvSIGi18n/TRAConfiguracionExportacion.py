# -*- coding: utf-8 -*-
#
# File: TRAConfiguracionExportacion.py
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
from Products.gvSIGi18n.TRAConfiguracion import TRAConfiguracion
from TRAConfiguracionExportacion_Operaciones import TRAConfiguracionExportacion_Operaciones
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from TRAElemento_Operaciones import TRAElemento_Operaciones

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='exportarNombresModulosPorDefecto',
        widget=SelectionWidget(
            label="Exportar nombres de modulos de cada cadena",
            label2="Export module names for each string",
            description="Exportar para cada cadena los nombres de sus modulos, como comentarios en el fichero .properties o GNUgettextPO.",
            description2="Export for each string, the names of its modules, as comments in the .properties or GNUgettextPO file.",
            label_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_exportarNombresModulosPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_exportarNombresModulosPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Exportar para cada cadena los nombres de sus modulos, como comentarios en el fichero .properties o GNUgettextPO.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionExportacion_attr_exportarNombresModulosPorDefecto_option_Si', 'gvSIGi18n_TRAConfiguracionExportacion_attr_exportarNombresModulosPorDefecto_option_No'],
        label2="Export module names for each string",
        ea_localid="1925",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Export for each string, the names of its modules, as comments in the .properties or GNUgettextPO file.",
        ea_guid="{7D0C7897-C87D-438d-8D51-A4608AAD9C3E}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Exportar nombres de modulos de cada cadena",
        length="0",
        containment="Not Specified",
        position="5",
        owner_class_name="TRAConfiguracionExportacion"
    ),

    StringField(
        name='exportarEstadoTraduccionesPorDefecto',
        widget=SelectionWidget(
            label="Exportar estado traducciones",
            label2="Export translations status",
            description="Exportar el estado de cada traduccion, como un comentario en el fichero .properties o GNUgettextPO.",
            description2="Export the translations status, as a comment in the .properties or GNUgettextPO file.",
            label_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_exportarEstadoTraduccionesPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_exportarEstadoTraduccionesPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Exportar el estado de cada traduccion, como un comentario en el fichero .properties o GNUgettextPO.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionExportacion_attr_exportarEstadoTraduccionesPorDefecto_option_Si', 'gvSIGi18n_TRAConfiguracionExportacion_attr_exportarEstadoTraduccionesPorDefecto_option_No'],
        label2="Export translations status",
        ea_localid="1924",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Export the translations status, as a comment in the .properties or GNUgettextPO file.",
        ea_guid="{065BF9CE-F960-4701-AA85-0CDF384C601A}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Exportar estado traducciones",
        length="0",
        containment="Not Specified",
        position="2",
        owner_class_name="TRAConfiguracionExportacion"
    ),

    StringField(
        name='exportarFuentesPorDefecto',
        widget=SelectionWidget(
            label="Exportar fuentes de cadenas",
            label2="Export string sources",
            description="Exportar para cada cadena los nombres de ficheros fuentes donde se usa la cadena, como comentarios en el fichero .properties o GNUgettextPO.",
            description2="Export for each string, the names  of the source files where the string is used, as comments in the .properties or GNUgettextPO file.",
            label_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_exportarFuentesPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_exportarFuentesPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Exportar para cada cadena los nombres de ficheros fuentes donde se usa la cadena, como comentarios en el fichero .properties o GNUgettextPO.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionExportacion_attr_exportarFuentesPorDefecto_option_Si', 'gvSIGi18n_TRAConfiguracionExportacion_attr_exportarFuentesPorDefecto_option_No'],
        label2="Export string sources",
        ea_localid="1956",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Export for each string, the names  of the source files where the string is used, as comments in the .properties or GNUgettextPO file.",
        ea_guid="{01553CF9-81F5-4919-9354-A8498FBF3E93}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Exportar fuentes de cadenas",
        length="0",
        containment="Not Specified",
        position="3",
        owner_class_name="TRAConfiguracionExportacion"
    ),

    StringField(
        name='tipoArchivoExportacionPorDefecto',
        widget=SelectionWidget(
            label="Tipo de archivo descargable por defecto",
            label2="Default downladable archive kind",
            description="Tipo de archivo en que se descargan el modulo o modulos exportados. Puede ser .jar o .zip.",
            description2="Type of the archive used to pack the module or modules for download. Options are .jar or .zip.",
            label_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_tipoArchivoExportacionPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_tipoArchivoExportacionPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Tipo de archivo en que se descargan el modulo o modulos exportados. Puede ser .jar o .zip.",
        vocabulary=['.jar','.zip',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionExportacion_attr_tipoArchivoExportacionPorDefecto_option_.jar', 'gvSIGi18n_TRAConfiguracionExportacion_attr_tipoArchivoExportacionPorDefecto_option_.zip'],
        label2="Default downladable archive kind",
        ea_localid="1947",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Type of the archive used to pack the module or modules for download. Options are .jar or .zip.",
        ea_guid="{909E9811-2853-4887-8FE2-D203AB2B4EF1}",
        vocabulary2=['.jar','.zip',],
        scale="0",
        default=".zip",
        label="Tipo de archivo descargable por defecto",
        length="0",
        containment="Not Specified",
        position="19",
        owner_class_name="TRAConfiguracionExportacion"
    ),

    StringField(
        name='modoGestionErrorCodificacionExportacionPorDefecto',
        widget=SelectionWidget(
            label="Modo de gestion de errores de codificacion",
            label2="Encoding errors handling mode",
            description="Como reaccionar ante la ocurrencia de errores de codificacion de caracteres durante la exportacion de traducciones.",
            description2="How to react upon occurences of encoding errors errors during the translations export process.",
            label_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_modoGestionErrorCodificacionExportacionPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_modoGestionErrorCodificacionExportacionPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Como reaccionar ante la ocurrencia de errores de codificacion de caracteres durante la exportacion de traducciones.",
        vocabulary=[ 'Cancelar al primer error', 'Contar todos los errores y cancelar', 'Ignorar y continuar', 'Sustituir y continuar', 'Sustituir por XML y continuar', 'Sustituir por escape y continuar',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionExportacion_attr_modoGestionErrorCodificacionExportacionPorDefecto_option_Cancelar al primer error', 'gvSIGi18n_TRAConfiguracionExportacion_attr_modoGestionErrorCodificacionExportacionPorDefecto_option_Contar todos los errores y cancelar', 'gvSIGi18n_TRAConfiguracionExportacion_attr_modoGestionErrorCodificacionExportacionPorDefecto_option_Ignorar y continuar', 'gvSIGi18n_TRAConfiguracionExportacion_attr_modoGestionErrorCodificacionExportacionPorDefecto_option_Sustituir y continuar', 'gvSIGi18n_TRAConfiguracionExportacion_attr_modoGestionErrorCodificacionExportacionPorDefecto_option_Sustituir por XML y continuar', 'gvSIGi18n_TRAConfiguracionExportacion_attr_modoGestionErrorCodificacionExportacionPorDefecto_option_Sustituir por escape y continuar'],
        label2="Encoding errors handling mode",
        ea_localid="1934",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="How to react upon occurences of encoding errors errors during the translations export process.",
        ea_guid="{64D5477C-352E-43a5-8275-BB15E42EB4C2}",
        vocabulary2=[ 'Cancel on first error', 'Count all errors and cancel', 'Ignore and continue', 'Replace and continue', 'XML replace and continue', 'Backslash replace and continue',],
        scale="0",
        default="Sustituir por escape y continuar",
        label="Modo de gestion de errores de codificacion",
        length="0",
        containment="Not Specified",
        position="16",
        owner_class_name="TRAConfiguracionExportacion"
    ),

    StringField(
        name='exportarNombreFicheroParaGvSIGPorDefecto',
        widget=SelectionWidget(
            label="Exportar Fichero para gvSIGpor defecto",
            label2="Export File for gvSIGby default",
            description="Exportar Fichero con nombre segun el estandar de gvSIG para ficheros de distribucion de localizaciones.",
            description2="Export File with name according to the gvSIG standard for distribution of localization files.",
            label_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_exportarNombreFicheroParaGvSIGPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_exportarNombreFicheroParaGvSIGPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Exportar Fichero con nombre segun el estandar de gvSIG para ficheros de distribucion de localizaciones.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionExportacion_attr_exportarNombreFicheroParaGvSIGPorDefecto_option_Si', 'gvSIGi18n_TRAConfiguracionExportacion_attr_exportarNombreFicheroParaGvSIGPorDefecto_option_No'],
        label2="Export File for gvSIGby default",
        ea_localid="1950",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Export File with name according to the gvSIG standard for distribution of localization files.",
        ea_guid="{C6F4C044-2E35-4c55-8747-809AC7B7EE93}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Exportar Fichero para gvSIGpor defecto",
        length="0",
        containment="Not Specified",
        position="4",
        owner_class_name="TRAConfiguracionExportacion"
    ),

    StringField(
        name='exportarTRACatalogoPorDefecto',
        widget=SelectionWidget(
            label="Exportar propiedades de TRACatalogo en XML",
            label2="Export TRACatalogo properties in XML",
            description="Exportar propiedades  del catalogo raiz de traducciones a un fichero XML.",
            description2="Export properties from the root translations catalog to an XML file.",
            label_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRACatalogoPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRACatalogoPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Exportar propiedades  del catalogo raiz de traducciones a un fichero XML.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRACatalogoPorDefecto_option_Si', 'gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRACatalogoPorDefecto_option_No'],
        label2="Export TRACatalogo properties in XML",
        ea_localid="2012",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Export properties from the root translations catalog to an XML file.",
        ea_guid="{DB009E05-FBA5-4621-88E0-2355A42B8AF3}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Exportar propiedades de TRACatalogo en XML",
        length="0",
        containment="Not Specified",
        position="6",
        owner_class_name="TRAConfiguracionExportacion"
    ),

    StringField(
        name='exportarTRAConfiguracionesPorDefecto',
        widget=SelectionWidget(
            label="Exportar las TRAConfiguracion en XML",
            label2="Export the TRAConfiguracion in XML",
            description="Exportar las configuraciones en fichero XML.",
            description2="Export the configurations in an XML file.",
            label_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRAConfiguracionesPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRAConfiguracionesPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Exportar las configuraciones en fichero XML.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRAConfiguracionesPorDefecto_option_Si', 'gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRAConfiguracionesPorDefecto_option_No'],
        label2="Export the TRAConfiguracion in XML",
        ea_localid="2013",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Export the configurations in an XML file.",
        ea_guid="{EA7DDE0D-35A4-4b7b-B0F4-2FCA47E902CF}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Exportar las TRAConfiguracion en XML",
        length="0",
        containment="Not Specified",
        position="7",
        owner_class_name="TRAConfiguracionExportacion"
    ),

    StringField(
        name='exportarTRAParametrosControlProgresoPorDefecto',
        widget=SelectionWidget(
            label="Exportar los TRAParametrosControlProgreso en XML",
            label2="Export the TRAParametrosControlProgreso in XML",
            description="Exportar los parametros control de progreso de procesos de larga duracion en fichero XML.",
            description2="Export the long-lived progress control parameters in an XML file.",
            label_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRAParametrosControlProgresoPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRAParametrosControlProgresoPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Exportar los parametros control de progreso de procesos de larga duracion en fichero XML.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRAParametrosControlProgresoPorDefecto_option_Si', 'gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRAParametrosControlProgresoPorDefecto_option_No'],
        label2="Export the TRAParametrosControlProgreso in XML",
        ea_localid="2014",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Export the long-lived progress control parameters in an XML file.",
        ea_guid="{60EB5BEF-3408-453a-84AC-14EEED6F14B4}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Exportar los TRAParametrosControlProgreso en XML",
        length="0",
        containment="Not Specified",
        position="8",
        owner_class_name="TRAConfiguracionExportacion"
    ),

    StringField(
        name='exportarTRAIdiomasPorDefecto',
        widget=SelectionWidget(
            label="Exportar los TRAIdioma en XML",
            label2="Export the TRAIdioma in XML",
            description="Exportar los idiomas, y en su caso nombres de idioma y banderas asociadas, en fichero XML.",
            description2="Export the languages, and when applicable the langusage names and flag, in an XML file.",
            label_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRAIdiomasPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRAIdiomasPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Exportar los idiomas, y en su caso nombres de idioma y banderas asociadas, en fichero XML.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRAIdiomasPorDefecto_option_Si', 'gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRAIdiomasPorDefecto_option_No'],
        label2="Export the TRAIdioma in XML",
        ea_localid="2017",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Export the languages, and when applicable the langusage names and flag, in an XML file.",
        ea_guid="{1A0F8435-8E40-499d-9596-284FBEED1110}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Exportar los TRAIdioma en XML",
        length="0",
        containment="Not Specified",
        position="12",
        owner_class_name="TRAConfiguracionExportacion"
    ),

    StringField(
        name='exportarTRASolicitudesCadenasPorDefecto',
        widget=SelectionWidget(
            label="Exportar los TRASolicitudCadena en XML",
            label2="Export the TRASolicitudCadena in XML",
            description="Exportar las solicitudes de nuevas cadenas en fichero XML.",
            description2="Export the new string requests in an XML file.",
            label_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRASolicitudesCadenasPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRASolicitudesCadenasPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Exportar las solicitudes de nuevas cadenas en fichero XML.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRASolicitudesCadenasPorDefecto_option_Si', 'gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRASolicitudesCadenasPorDefecto_option_No'],
        label2="Export the TRASolicitudCadena in XML",
        ea_localid="2020",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Export the new string requests in an XML file.",
        ea_guid="{744DE49C-1378-47ae-843E-BA385A3247E8}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Exportar los TRASolicitudCadena en XML",
        length="0",
        containment="Not Specified",
        position="9",
        owner_class_name="TRAConfiguracionExportacion"
    ),

    StringField(
        name='exportarTRAModulosPorDefecto',
        widget=SelectionWidget(
            label="Exportar los TRAModulo en XML",
            label2="Export the TRAModulo in XML",
            description="Exportar los modulos, en fichero XML.",
            description2="Export the modules, in an XML file.",
            label_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRAModulosPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRAModulosPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Exportar los modulos, en fichero XML.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRAModulosPorDefecto_option_Si', 'gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRAModulosPorDefecto_option_No'],
        label2="Export the TRAModulo in XML",
        ea_localid="2018",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Export the modules, in an XML file.",
        ea_guid="{AF276082-C00F-42f4-A3E3-D290B80B731E}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Exportar los TRAModulo en XML",
        length="0",
        containment="Not Specified",
        position="10",
        owner_class_name="TRAConfiguracionExportacion"
    ),

    StringField(
        name='exportarTRAInformesPorDefecto',
        widget=SelectionWidget(
            label="Exportar los TRAInforme en XML",
            label2="Export the TRAInforme in XML",
            description="Exportar los informes, en fichero XML.",
            description2="Export the reports, in an XML file.",
            label_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRAInformesPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRAInformesPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Exportar los informes, en fichero XML.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRAInformesPorDefecto_option_Si', 'gvSIGi18n_TRAConfiguracionExportacion_attr_exportarTRAInformesPorDefecto_option_No'],
        label2="Export the TRAInforme in XML",
        ea_localid="2019",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Export the reports, in an XML file.",
        ea_guid="{52A4AE70-92CA-4f01-AC1E-0B3BFBC4D212}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Exportar los TRAInforme en XML",
        length="0",
        containment="Not Specified",
        position="11",
        owner_class_name="TRAConfiguracionExportacion"
    ),

    StringField(
        name='codigoIdiomaPorDefecto',
        widget=StringWidget(
            label="Codigo de Idioma por defecto",
            label2="Default Language Code",
            description="Al exportar en formato Java .properties, los ficheros exportados para este idioma no incluiran el codigo de idioma en el nombre del fichero Java .properties.",
            description2="When exporting in Java .properties format, exported files for this language shall not include the language code in the Java .properties file name.",
            label_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_codigoIdiomaPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_codigoIdiomaPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Al exportar en formato Java .properties, los ficheros exportados para este idioma no incluiran el codigo de idioma en el nombre del fichero Java .properties.",
        duplicates="0",
        label2="Default Language Code",
        ea_localid="1953",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="When exporting in Java .properties format, exported files for this language shall not include the language code in the Java .properties file name.",
        ea_guid="{B54153C8-E540-46a6-817A-F49926D21760}",
        scale="0",
        default="es",
        label="Codigo de Idioma por defecto",
        length="0",
        containment="Not Specified",
        position="0",
        owner_class_name="TRAConfiguracionExportacion"
    ),

    StringField(
        name='dominioPorDefecto',
        widget=StringWidget(
            label="Dominio para cadenas sin modulo",
            label2="Domain for strings not in a module",
            description="Dato que aparece en los ficheros de exportacion de tipo GNU gettext PO, cuando se exportan separadamente en su propio fichero cadenas que no pertenecen a un modulo, para identificar la aplicacion o modulo a que se aplican las traducciones.",
            description2="Information that appears in the exported files with GNU gettext PO format, when exporting separately in its own file strings that do not pertain to any module,  to indicate the application or module to which the translations apply.",
            label_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_dominioPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_dominioPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Dato que aparece en los ficheros de exportacion de tipo GNU gettext PO, cuando se exportan separadamente en su propio fichero cadenas que no pertenecen a un modulo, para identificar la aplicacion o modulo a que se aplican las traducciones.",
        duplicates="0",
        label2="Domain for strings not in a module",
        ea_localid="1482",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Information that appears in the exported files with GNU gettext PO format, when exporting separately in its own file strings that do not pertain to any module,  to indicate the application or module to which the translations apply.",
        ea_guid="{F9D57218-C3F9-4a24-804F-1CBB941BE9EA}",
        scale="0",
        default="aDefaultDomainName",
        label="Dominio para cadenas sin modulo",
        length="0",
        containment="Not Specified",
        position="1",
        owner_class_name="TRAConfiguracionExportacion"
    ),

    StringField(
        name='formatoExportacionPorDefecto',
        widget=SelectionWidget(
            label="Formato de exportacion por defecto",
            label2="Default Export Format",
            description="Formato de los ficheros de exportacion de traducciones como Java .properties, o GNUtettext PO.",
            description2="Format for the translations export files, as Java .properties or GNUgettext .PO.",
            label_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_formatoExportacionPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_formatoExportacionPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Formato de los ficheros de exportacion de traducciones como Java .properties, o GNUtettext PO.",
        vocabulary=['Java .properties','GNU gettext PO',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionExportacion_attr_formatoExportacionPorDefecto_option_Java .properties', 'gvSIGi18n_TRAConfiguracionExportacion_attr_formatoExportacionPorDefecto_option_GNU gettext PO'],
        label2="Default Export Format",
        ea_localid="1926",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Format for the translations export files, as Java .properties or GNUgettext .PO.",
        ea_guid="{A2C8ACBE-E5AB-4cec-8404-F37494792B18}",
        vocabulary2=['Java .properties','GNU gettext PO',],
        scale="0",
        default="Java .properties",
        label="Formato de exportacion por defecto",
        length="0",
        containment="Not Specified",
        position="13",
        owner_class_name="TRAConfiguracionExportacion"
    ),

    StringField(
        name='incluirLocalesCSVPorDefecto',
        widget=SelectionWidget(
            label="Incluir fichero locales.csv",
            label2="Include locales.csv file",
            description="Incluir en el archivo descargable un fichero locales.csv declarando los ficheros de traducciones contenidos en el archivo (usado por gvSIG).",
            description2="Include in the downloadable archive, a locales.csv file declaring the translations files contained in the archive (used by gvSIG).",
            label_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_incluirLocalesCSVPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_incluirLocalesCSVPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Incluir en el archivo descargable un fichero locales.csv declarando los ficheros de traducciones contenidos en el archivo (usado por gvSIG).",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionExportacion_attr_incluirLocalesCSVPorDefecto_option_Si', 'gvSIGi18n_TRAConfiguracionExportacion_attr_incluirLocalesCSVPorDefecto_option_No'],
        label2="Include locales.csv file",
        ea_localid="1932",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Include in the downloadable archive, a locales.csv file declaring the translations files contained in the archive (used by gvSIG).",
        ea_guid="{ACDCD6C6-86A2-416d-BDEA-EAF0B2F19CBB}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Incluir fichero locales.csv",
        length="0",
        containment="Not Specified",
        position="14",
        owner_class_name="TRAConfiguracionExportacion"
    ),

    StringField(
        name='incluirManifestPorDefecto',
        widget=SelectionWidget(
            label="Incluir fichero MANIFEST.MF",
            label2="Include MANIFEST.MF file",
            description="Incluir en el archivo descargable un fichero MANIFEST.MF declarando los ficheros de traducciones contenidos en el archivo.",
            description2="Include in the downloadable archive, a MANIFEST.MF file declaring the translations files contained in the archive.",
            label_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_incluirManifestPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_incluirManifestPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Incluir en el archivo descargable un fichero MANIFEST.MF declarando los ficheros de traducciones contenidos en el archivo.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionExportacion_attr_incluirManifestPorDefecto_option_Si', 'gvSIGi18n_TRAConfiguracionExportacion_attr_incluirManifestPorDefecto_option_No'],
        label2="Include MANIFEST.MF file",
        ea_localid="1933",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Include in the downloadable archive, a MANIFEST.MF file declaring the translations files contained in the archive.",
        ea_guid="{54F6FDF8-FA97-4b3b-BD2A-AA5C4271AFD5}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Incluir fichero MANIFEST.MF",
        length="0",
        containment="Not Specified",
        position="15",
        owner_class_name="TRAConfiguracionExportacion"
    ),

    StringField(
        name='modulosPorSeparadoPorDefecto',
        widget=SelectionWidget(
            label="Exportar modulos por separado",
            label2="Export separated modules",
            description="Exportar cada modulo por separado en su propio fichero, todos ellos incluidos en el archivo descargable.",
            description2="Export each module in its own file, with all of them packed in the downloadable archive.",
            label_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_modulosPorSeparadoPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_modulosPorSeparadoPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Exportar cada modulo por separado en su propio fichero, todos ellos incluidos en el archivo descargable.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionExportacion_attr_modulosPorSeparadoPorDefecto_option_Si', 'gvSIGi18n_TRAConfiguracionExportacion_attr_modulosPorSeparadoPorDefecto_option_No'],
        label2="Export separated modules",
        ea_localid="1936",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Export each module in its own file, with all of them packed in the downloadable archive.",
        ea_guid="{5F9CF60D-7622-4f45-BB3E-C2D1FE88D81B}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Exportar modulos por separado",
        length="0",
        containment="Not Specified",
        position="17",
        owner_class_name="TRAConfiguracionExportacion"
    ),

    StringField(
        name='nombreModuloPorDefecto',
        widget=StringWidget(
            label="Nombre de Modulo por defecto",
            label2="Default Module Name",
            description="Cuando se exporta un fichero para cada modulo, es el nombre a utilizar en los nombres de archivos GNUgettext PO, o para las carpetas contenedoras de ficheros Java .properties, para las cadenas para las que no se ha especificado modulo.",
            description2="When exporting a separate file for each module, it is the name to use in a GNUgettext .PO file name, or for the folder containing a Java .properties file.",
            label_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_nombreModuloPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionExportacion_attr_nombreModuloPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Cuando se exporta un fichero para cada modulo, es el nombre a utilizar en los nombres de archivos GNUgettext PO, o para las carpetas contenedoras de ficheros Java .properties, para las cadenas para las que no se ha especificado modulo.",
        duplicates="0",
        label2="Default Module Name",
        ea_localid="1952",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="When exporting a separate file for each module, it is the name to use in a GNUgettext .PO file name, or for the folder containing a Java .properties file.",
        ea_guid="{E08F7190-751B-4c1a-A957-64DB05AD8D33}",
        scale="0",
        default="aDefaultModuleName",
        label="Nombre de Modulo por defecto",
        length="0",
        containment="Not Specified",
        position="18",
        owner_class_name="TRAConfiguracionExportacion"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAConfiguracionExportacion_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAConfiguracion, 'schema', Schema(())).copy() + \
    getattr(TRAConfiguracionExportacion_Operaciones, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAConfiguracionExportacion(OrderedBaseFolder, TRAConfiguracion, TRAConfiguracionExportacion_Operaciones):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAConfiguracion,'__implements__',()),) + (getattr(TRAConfiguracionExportacion_Operaciones,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Configuracion Exportacion'

    meta_type = 'TRAConfiguracionExportacion'
    portal_type = 'TRAConfiguracionExportacion'


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



    allowed_content_types = [] + list(getattr(TRAConfiguracion, 'allowed_content_types', [])) + list(getattr(TRAConfiguracionExportacion_Operaciones, 'allowed_content_types', []))
    filter_content_types             = 1
    global_allow                     = 0
    content_icon = 'traconfiguracion.gif'
    immediate_view                   = 'Tabular'
    default_view                     = 'Tabular'
    suppl_views                      = ['Tabular',]
    typeDescription                  = "Configuracion del catalogo de traducciones, con parametros controlando las operaciones de exportacion desde el catalogo."
    typeDescMsgId                    =  'gvSIGi18n_TRAConfiguracionExportacion_help'
    archetype_name2                  = 'Export Configuration'
    typeDescription2                 = '''Translations catalog configuration, with parameters controlling export operations from the catalog.'''
    archetype_name_msgid             = 'gvSIGi18n_TRAConfiguracionExportacion_label'
    factory_methods                  = None
    factory_enablers                 = None
    propagate_delete_impact_to       = None
    allow_discussion = False


    actions =  (


       {'action': "string:${object_url}/Editar",
        'category': "object_buttons",
        'id': 'TRA_configurar',
        'name': 'Configure',
        'permissions': ("Modify portal content",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Configure_TRAConfiguracion')"""
       },


       {'action': "string:$object_url/Editar",
        'category': "object",
        'id': 'edit',
        'name': 'Edit',
        'permissions': ("Modify portal content",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Configure_TRAConfiguracion')"""
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

    schema = TRAConfiguracionExportacion_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata', 'sharing', 'folderContents']:
            a['visible'] = 0
    return fti

registerType(TRAConfiguracionExportacion, PROJECTNAME)
# end of class TRAConfiguracionExportacion

##code-section module-footer #fill in your manual code here
##/code-section module-footer



