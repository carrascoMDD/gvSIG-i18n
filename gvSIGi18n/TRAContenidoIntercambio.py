# -*- coding: utf-8 -*-
#
# File: TRAContenidoIntercambio.py
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
from TRAContenidoIntercambio_Operaciones import TRAContenidoIntercambio_Operaciones
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from TRAElemento_Operaciones import TRAElemento_Operaciones
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
        default="False",
        label="Excluir de Importacion",
        length="0",
        containment="Not Specified",
        position="2",
        owner_class_name="TRAContenidoIntercambio"
    ),

    StringField(
        name='usuarioContribuidor',
        widget=StringWidget(
            label="Usuario Contribuidor",
            label2="Contributor User",
            description="Usuario que ha subido al servidor el archivo o fichero con contenido de intercambio de traducciones de cadenas a idiomas.",
            description2="User who uploaded the interchange content file or archive with string translations into languages.",
            label_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_usuarioContribuidor_label',
            description_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_usuarioContribuidor_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Usuario que ha subido al servidor el archivo o fichero con contenido de intercambio de traducciones de cadenas a idiomas.",
        duplicates="0",
        label2="Contributor User",
        ea_localid="956",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="User who uploaded the interchange content file or archive with string translations into languages.",
        ea_guid="{E444AD8A-CE91-417c-8488-F7C9A8BD6CE0}",
        read_only="True",
        scale="0",
        label="Usuario Contribuidor",
        length="0",
        containment="Not Specified",
        position="14",
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
        read_only="True",
        scale="0",
        label="Fecha y Hora de Carga",
        length="0",
        containment="Not Specified",
        position="3",
        owner_class_name="TRAContenidoIntercambio"
    ),

    StringField(
        name='ficheroLeido',
        widget=StringWidget(
            label="Fichero leido",
            label2="File read",
            description="El nombre del fichero de intercambio del contenido de traducciones de cadenas a idiomas.",
            description2="The name of the interchange content file with string translations into languages.",
            label_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_ficheroLeido_label',
            description_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_ficheroLeido_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="El nombre del fichero de intercambio del contenido de traducciones de cadenas a idiomas.",
        duplicates="0",
        label2="File read",
        ea_localid="1972",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="The name of the interchange content file with string translations into languages.",
        ea_guid="{A4497386-9882-4628-952C-004CFB017BD4}",
        read_only="True",
        scale="0",
        label="Fichero leido",
        length="0",
        default_method="fGetMemberId_safe",
        position="13",
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
        expression="context.fSumarioContenido()",
        label="Sumario del contenido",
        length="0",
        containment="Not Specified",
        position="12",
        owner_class_name="TRAContenidoIntercambio",
        exclude_from_views="[ 'Textual', 'Tabular',  ]"
    ),

    ComputedField(
        name='informeContenido',
        exclude_from_views="[ 'Textual', 'Tabular', ]",
        widget=ComputedField._properties['widget'](
            label="Contenido Intercambio de Traducciones",
            label2="Content in Translations Interchange",
            description="Infome acerca de ls contenidos de los Archivos de intercambio de traducciones  incluyendo  cadenas (posiblemente asociadas a modulos)  y traducciones a un numero de idiomas,",
            description2="Report on the contents of translations interchange Archive files, including strings (possibly associated with modules) and translations to a number of languages.",
            label_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_informeContenido_label',
            description_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_informeContenido_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Infome acerca de ls contenidos de los Archivos de intercambio de traducciones  incluyendo  cadenas (posiblemente asociadas a modulos)  y traducciones a un numero de idiomas,",
        duplicates="0",
        label2="Content in Translations Interchange",
        ea_localid="993",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Report on the contents of translations interchange Archive files, including strings (possibly associated with modules) and translations to a number of languages.",
        ea_guid="{6E839E35-1227-4081-9397-0F4CF172D96A}",
        exclude_from_values_form="True",
        scale="0",
        expression="context.fInformeContenidoIntercambio()",
        computed_types="text",
        label="Contenido Intercambio de Traducciones",
        length="0",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        position="9",
        owner_class_name="TRAContenidoIntercambio",
        custom_presentation_view="TRAContenidoIntercambioDatos_NoHeaderNoFooter",
        exclude_from_exportconfig="True",
        exclude_from_copyconfig="True"
    ),

    StringField(
        name='nombreModuloPorDefecto',
        widget=StringWidget(
            label="Nombre de Modulo por defecto",
            label2="Default Module Name",
            description="Nombre del modulo a utilizar cuando Importar usando nombre de modulo configurado, o no se puede obtener, bien del nombre del dominio en ficheros GNU gettext .PO, o de la estructura de carpetas si el contenido a importar es una archivo .jar o .zip.",
            description2="Name of the Module to use when Import using configured module name, or can not be obtained, whether from domain name in the GNUgettext .POfile header, or from the folder structure if the uploaded content is a .jar or .zip archive file.",
            label_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_nombreModuloPorDefecto_label',
            description_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_nombreModuloPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Nombre del modulo a utilizar cuando Importar usando nombre de modulo configurado, o no se puede obtener, bien del nombre del dominio en ficheros GNU gettext .PO, o de la estructura de carpetas si el contenido a importar es una archivo .jar o .zip.",
        duplicates="0",
        label2="Default Module Name",
        ea_localid="1740",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Name of the Module to use when Import using configured module name, or can not be obtained, whether from domain name in the GNUgettext .POfile header, or from the folder structure if the uploaded content is a .jar or .zip archive file.",
        ea_guid="{7A8863D3-29F6-4469-8C54-5AD776D0B669}",
        read_only="True",
        scale="0",
        label="Nombre de Modulo por defecto",
        length="0",
        default_method="fInitial_NombreModuloPorDefecto",
        position="10",
        owner_class_name="TRAContenidoIntercambio"
    ),

    StringField(
        name='codigoIdiomaPorDefecto',
        widget=StringWidget(
            label="Codigo de Idioma por defecto",
            label2="Default Language Code",
            description="Codigo del lenguage para importar plantillas de traduccion GNUgettext .POT, o para Java .properties que no tienen el codigo del lenguage como sufijo en el nombre del fichero.",
            description2="Code of the language to import translations interchange content file in Java .properties format, when the file name does not contain the language code.",
            label_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_codigoIdiomaPorDefecto_label',
            description_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_codigoIdiomaPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Codigo del lenguage para importar plantillas de traduccion GNUgettext .POT, o para Java .properties que no tienen el codigo del lenguage como sufijo en el nombre del fichero.",
        duplicates="0",
        label2="Default Language Code",
        ea_localid="1969",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Code of the language to import translations interchange content file in Java .properties format, when the file name does not contain the language code.",
        ea_guid="{ADE94CD1-82FE-4ab3-9DFC-D2263C467BB3}",
        read_only="True",
        scale="0",
        default="es",
        label="Codigo de Idioma por defecto",
        length="0",
        default_method="fInitial_CodigoIdiomaPorDefecto",
        position="0",
        owner_class_name="TRAContenidoIntercambio"
    ),

    BooleanField(
        name='importarConNombreModuloConfigurado',
        widget=BooleanField._properties['widget'](
            label="Importar usando nombre de modulo configurado",
            label2="Import using configured module name",
            description="Importar usando el nombre de modulo configurado para la importacion o el contenido de intercambio",
            description2="Import strings as used in the module with the name configured for the import or the interchange contents.",
            label_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_importarConNombreModuloConfigurado_label',
            description_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_importarConNombreModuloConfigurado_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Importar usando el nombre de modulo configurado para la importacion o el contenido de intercambio",
        duplicates="0",
        label2="Import using configured module name",
        ea_localid="1730",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import strings as used in the module with the name configured for the import or the interchange contents.",
        ea_guid="{6283CC5C-F727-46b1-A1CD-24CB8BA308F7}",
        read_only="True",
        scale="0",
        default="True",
        label="Importar usando nombre de modulo configurado",
        length="0",
        default_method="fInitial_ImportarConNombreModuloConfigurado",
        position="4",
        owner_class_name="TRAContenidoIntercambio"
    ),

    BooleanField(
        name='importarNombreModuloDesdeDominioONombreFichero',
        widget=BooleanField._properties['widget'](
            label="Importar modulo de nombre de fichero o domino PO",
            label2="Import module from file name or PO Domain",
            description="Importar nombre de modulo del nombre de fichero o linea de domino del fichero GNU gettext PO.",
            description2="Import module name from the file name or from the GNU gettext PO header Domain line.",
            label_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_importarNombreModuloDesdeDominioONombreFichero_label',
            description_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_importarNombreModuloDesdeDominioONombreFichero_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Importar nombre de modulo del nombre de fichero o linea de domino del fichero GNU gettext PO.",
        duplicates="0",
        label2="Import module from file name or PO Domain",
        ea_localid="1732",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import module name from the file name or from the GNU gettext PO header Domain line.",
        ea_guid="{1AE31D12-2996-413b-A2E8-5D8AA68E49EC}",
        read_only="True",
        scale="0",
        default="True",
        label="Importar modulo de nombre de fichero o domino PO",
        length="0",
        default_method="fInitial_ImportarNombreModuloDesdeDominioONombreFichero",
        position="6",
        owner_class_name="TRAContenidoIntercambio"
    ),

    BooleanField(
        name='importarNombresModulosDesdeComentarios',
        widget=BooleanField._properties['widget'](
            label="Importar nombres de modulos desde comentarios",
            label2="Import module names from comments",
            description="Importar los nombres de modulos de cada cadena, desde sus comentarios en el fichero .properties o GNUgettextPO.",
            description2="Import the names of modules for each string, from its comments in the .properties or GNUgettextPO file.",
            label_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_importarNombresModulosDesdeComentarios_label',
            description_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_importarNombresModulosDesdeComentarios_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Importar los nombres de modulos de cada cadena, desde sus comentarios en el fichero .properties o GNUgettextPO.",
        duplicates="0",
        label2="Import module names from comments",
        ea_localid="1733",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import the names of modules for each string, from its comments in the .properties or GNUgettextPO file.",
        ea_guid="{0D7F7FCB-F5D9-423e-BB7A-A6E4E62C5248}",
        read_only="True",
        scale="0",
        default="True",
        label="Importar nombres de modulos desde comentarios",
        length="0",
        default_method="fInitial_ImportarNombresModulosDesdeComentarios",
        position="7",
        owner_class_name="TRAContenidoIntercambio"
    ),

    BooleanField(
        name='importarFuentesDesdeComentarios',
        widget=BooleanField._properties['widget'](
            label="Importar fuentes desde comentarios",
            label2="Import sources from comments",
            description="Importar los nombres de ficheros fuentes que donde aparece cada cadena, desde sus comentarios en el fichero .properties o GNUgettextPO.",
            description2="Import the names of source files where each string appears, from its comments in the .properties or GNUgettextPO file.",
            label_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_importarFuentesDesdeComentarios_label',
            description_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_importarFuentesDesdeComentarios_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Importar los nombres de ficheros fuentes que donde aparece cada cadena, desde sus comentarios en el fichero .properties o GNUgettextPO.",
        duplicates="0",
        label2="Import sources from comments",
        ea_localid="1731",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import the names of source files where each string appears, from its comments in the .properties or GNUgettextPO file.",
        ea_guid="{E1EA8D68-8F9D-428a-95DB-4F1BC5AE87CD}",
        read_only="True",
        scale="0",
        default="True",
        label="Importar fuentes desde comentarios",
        length="0",
        default_method="fInitial_ImportarFuentesDesdeComentarios",
        position="5",
        owner_class_name="TRAContenidoIntercambio"
    ),

    BooleanField(
        name='importarStatusDesdeComentarios',
        widget=BooleanField._properties['widget'](
            label="Importar estado de traduciones de comentarios",
            label2="Import translations status from comments",
            description="Importar el estado de cada traduccion, desde sus comentarios en el fichero .properties o GNUgettextPO.",
            description2="Import the status of each translation, from its comments in the .properties or GNUgettextPO file.",
            label_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_importarStatusDesdeComentarios_label',
            description_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_importarStatusDesdeComentarios_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Importar el estado de cada traduccion, desde sus comentarios en el fichero .properties o GNUgettextPO.",
        duplicates="0",
        label2="Import translations status from comments",
        ea_localid="1734",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import the status of each translation, from its comments in the .properties or GNUgettextPO file.",
        ea_guid="{EB1E753C-36A5-4dc3-81AD-12C6C5197C51}",
        read_only="True",
        scale="0",
        default="True",
        label="Importar estado de traduciones de comentarios",
        length="0",
        default_method="fInitial_ImportarStatusDesdeComentarios",
        position="8",
        owner_class_name="TRAContenidoIntercambio"
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
        read_only="True",
        scale="0",
        label="Contenido",
        length="0",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        position="1",
        owner_class_name="TRAContenidoIntercambio"
    ),

    BooleanField(
        name='importarContribucionesDesdeComentarios',
        widget=BooleanField._properties['widget'](
            label="Importar fechas y usuarios contribuidores desde comentarios",
            label2="Import contributing dates and user names from comments",
            description="Importar desde comentarios de cada traduccion las fechas y nombres de usuario que la crearon, tradujeron, revisaron o marcaron como definitiva.",
            description2="Import from each translation comments the dates and user names that created, translated, reviewed or marked it as definitive.",
            label_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_importarContribucionesDesdeComentarios_label',
            description_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_importarContribucionesDesdeComentarios_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Importar desde comentarios de cada traduccion las fechas y nombres de usuario que la crearon, tradujeron, revisaron o marcaron como definitiva.",
        duplicates="0",
        label2="Import contributing dates and user names from comments",
        ea_localid="2061",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import from each translation comments the dates and user names that created, translated, reviewed or marked it as definitive.",
        ea_guid="{B4CCFA6A-641F-482a-955A-5BDBAF37381A}",
        read_only="True",
        scale="0",
        default="True",
        label="Importar fechas y usuarios contribuidores desde comentarios",
        length="0",
        default_method="fInitial_ImportarContribucionesDesdeComentarios",
        position="9",
        owner_class_name="TRAContenidoIntercambio"
    ),

    IntegerField(
        name='numeroMaximoLineasAExplorar',
        widget=IntegerField._properties['widget'](
            label="Numero Maximo de Lineas a Explorar",
            label2="Maximum Number of Lines to Scan",
            description="Cuando se lea un fichero de intercambio de traducciones, se exploraran hasta este numero maximo de lineas.",
            description2="When scanning a translations interchange file, the system shall scan up to this maximum number of lines.",
            label_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_numeroMaximoLineasAExplorar_label',
            description_msgid='gvSIGi18n_TRAContenidoIntercambio_attr_numeroMaximoLineasAExplorar_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Cuando se lea un fichero de intercambio de traducciones, se exploraran hasta este numero maximo de lineas.",
        duplicates="0",
        label2="Maximum Number of Lines to Scan",
        ea_localid="1971",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="When scanning a translations interchange file, the system shall scan up to this maximum number of lines.",
        ea_guid="{10910F46-FF4F-4b22-82EF-D1C10A8BD015}",
        read_only="True",
        scale="0",
        default="100000",
        label="Numero Maximo de Lineas a Explorar",
        length="0",
        default_method="fInitial_NumeroMaximoLineasAExplorar",
        position="11",
        owner_class_name="TRAContenidoIntercambio"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAContenidoIntercambio_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAArquetipo, 'schema', Schema(())).copy() + \
    getattr(TRAConRegistroActividad, 'schema', Schema(())).copy() + \
    getattr(TRAContenidoIntercambio_Operaciones, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAContenidoIntercambio(OrderedBaseFolder, TRAArquetipo, TRAConRegistroActividad, TRAContenidoIntercambio_Operaciones):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAArquetipo,'__implements__',()),) + (getattr(TRAConRegistroActividad,'__implements__',()),) + (getattr(TRAContenidoIntercambio_Operaciones,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Contenido de Intercambio'

    meta_type = 'TRAContenidoIntercambio'
    portal_type = 'TRAContenidoIntercambio'


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

    allowed_content_types = [] + list(getattr(TRAArquetipo, 'allowed_content_types', [])) + list(getattr(TRAConRegistroActividad, 'allowed_content_types', [])) + list(getattr(TRAContenidoIntercambio_Operaciones, 'allowed_content_types', []))
    filter_content_types             = 1
    global_allow                     = 0
    content_icon = 'tracontenidointercambio.gif'
    immediate_view                   = 'Tabular'
    default_view                     = 'Tabular'
    suppl_views                      = ['Tabular',]
    typeDescription                  = "Contenido de un intercambio de Importacion de traducciones de cadenas a uno o mas idiomas."
    typeDescMsgId                    =  'gvSIGi18n_TRAContenidoIntercambio_help'
    archetype_name2                  = 'Interchange Content'
    typeDescription2                 = '''Contents of an Import interchange of string translations to a number od languages'''
    archetype_name_msgid             = 'gvSIGi18n_TRAContenidoIntercambio_label'
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
        'condition': """python:object.fUseCaseCheckDoable( 'Edit_TRAContenidoIntercambio')"""
       },


       {'action': "string:${object_url}/Tabular",
        'category': "object",
        'id': 'view',
        'name': 'View',
        'permissions': ("View",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'View_any_TRA_element')"""
       },


       {'action': "string:${object_url}/TRAContenidoIntercambioDatos",
        'category': "object",
        'id': 'TRAContenidoIntercambioDatos',
        'name': 'Data',
        'permissions': ("View",),
        'condition': """python:1"""
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

    schema = TRAContenidoIntercambio_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('manage_beforeDelete')
    def manage_beforeDelete(self,item,container):
        """
        """
        
        return TRAArquetipo.manage_beforeDelete( self, item, container)

    security.declarePublic('fIsCacheable')
    def fIsCacheable(self):
        """
        """
        
        return True

    security.declarePublic('displayContentsTab')
    def displayContentsTab(self):
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
        
        return TRAContenidoIntercambio_Operaciones.fExtraLinks( self)

    security.declarePublic('manage_afterAdd')
    def manage_afterAdd(self,item,container):
        """
        """
        
        return TRAContenidoIntercambio_Operaciones.pHandle_manage_afterAdd( self, item, container)
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata', 'sharing', 'folderContents']:
            a['visible'] = 0
    return fti

registerType(TRAContenidoIntercambio, PROJECTNAME)
# end of class TRAContenidoIntercambio

##code-section module-footer #fill in your manual code here
##/code-section module-footer



