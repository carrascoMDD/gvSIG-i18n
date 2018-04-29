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
        position="23",
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
        position="17",
        owner_class_name="TRACatalogo"
    ),

    StringField(
        name='codigoIdiomaPorDefecto',
        widget=StringWidget(
            label="Codigo de Idioma por defecto",
            label2="Default Language Code",
            description="Codigo del lenguage para el que los ficheros de importacion o exportacion Java .properties no incorporan el codigo del lenguage como sufijo en el nombre del fichero.",
            description2="Code of the language whose Java .properties import or export files do not contain the language code in the file name as a suffix.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_codigoIdiomaPorDefecto_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_codigoIdiomaPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Codigo del lenguage para el que los ficheros de importacion o exportacion Java .properties no incorporan el codigo del lenguage como sufijo en el nombre del fichero.",
        duplicates="0",
        label2="Default Language Code",
        ea_localid="1483",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Code of the language whose Java .properties import or export files do not contain the language code in the file name as a suffix.",
        ea_guid="{84BF218C-5DDA-47cd-A2A3-4B5322591B7E}",
        scale="0",
        default="en",
        label="Codigo de Idioma por defecto",
        length="0",
        containment="Not Specified",
        position="0",
        owner_class_name="TRACatalogo"
    ),

    StringField(
        name='codigoIdiomaRequeridoSolicitudesNuevasCadenas',
        widget=StringWidget(
            label="Codigo de Idioma para Solicitudes de Nuevas Cadenas",
            label2="Language Code  for new String Requests",
            description="Codigo del lenguage en el que se requiere una traduccion cuando se solicitan nuevas cadenas.",
            description2="Code of the language for which a translation is requiered when requesting creation of new strings.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_codigoIdiomaRequeridoSolicitudesNuevasCadenas_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_codigoIdiomaRequeridoSolicitudesNuevasCadenas_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Codigo del lenguage en el que se requiere una traduccion cuando se solicitan nuevas cadenas.",
        duplicates="0",
        label2="Language Code  for new String Requests",
        ea_localid="1532",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Code of the language for which a translation is requiered when requesting creation of new strings.",
        ea_guid="{02CB334C-305D-4804-B97A-43CDEC5F1405}",
        scale="0",
        default="en",
        label="Codigo de Idioma para Solicitudes de Nuevas Cadenas",
        length="0",
        containment="Not Specified",
        position="2",
        owner_class_name="TRACatalogo"
    ),

    StringField(
        name='codigoIdiomaReferenciaSolicitudesNuevasCadenas',
        widget=StringWidget(
            label="Codigo de Idioma de Referencia  para Solicitudes de Nuevas Cadenas",
            label2="Reference Language Code for new String Requests",
            description="Codigo del lenguage para el que el desarrollador puede proporcionar una traduccion de referencia, cuando se solicitan nuevas cadenas.",
            description2="Code of the language for which the developer may provide a reference  translation when requesting creation of new strings.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_codigoIdiomaReferenciaSolicitudesNuevasCadenas_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_codigoIdiomaReferenciaSolicitudesNuevasCadenas_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Codigo del lenguage para el que el desarrollador puede proporcionar una traduccion de referencia, cuando se solicitan nuevas cadenas.",
        duplicates="0",
        label2="Reference Language Code for new String Requests",
        ea_localid="1533",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Code of the language for which the developer may provide a reference  translation when requesting creation of new strings.",
        ea_guid="{0418F0A6-AA65-426b-A999-1ED5326C7BBD}",
        scale="0",
        default="es",
        label="Codigo de Idioma de Referencia  para Solicitudes de Nuevas Cadenas",
        length="0",
        containment="Not Specified",
        position="1",
        owner_class_name="TRACatalogo"
    ),

    StringField(
        name='nombreModuloPorDefecto',
        widget=StringWidget(
            label="Nombre de Modulo por defecto",
            label2="Default Module Name",
            description="Cuando se exporta un fichero para cada modulo, es el nombre a utilizar en los nombres de archivos GNUgettext PO, o para las carpetas contenedoras de ficheros Java .properties, para las cadenas para las que no se ha especificado modulo.",
            description2="When exporting a separate file for each module, it is the name to use in a GNUgettext .PO file name, or for the folder containing a Java .properties file.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_nombreModuloPorDefecto_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_nombreModuloPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Cuando se exporta un fichero para cada modulo, es el nombre a utilizar en los nombres de archivos GNUgettext PO, o para las carpetas contenedoras de ficheros Java .properties, para las cadenas para las que no se ha especificado modulo.",
        duplicates="0",
        label2="Default Module Name",
        ea_localid="1484",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="When exporting a separate file for each module, it is the name to use in a GNUgettext .PO file name, or for the folder containing a Java .properties file.",
        ea_guid="{C8C5CA58-25BD-4974-8A9F-881BE3A1CAD4}",
        scale="0",
        default="gvSIG",
        label="Nombre de Modulo por defecto",
        length="0",
        containment="Not Specified",
        position="16",
        owner_class_name="TRACatalogo"
    ),

    StringField(
        name='dominioPorDefecto',
        widget=StringWidget(
            label="Dominio para cadenas sin modulo",
            label2="Domain for strings not in a module",
            description="Dato que aparece en los ficheros de exportacion de tipo GNUgettext PO, cuando se exportan separadamente en su propio fichero cadenas que no pertenecen a un modulo, para identificar la aplicacion o modulo a que se aplican las traducciones.",
            description2="Iinformation that appears in the exported files of GNUgettext PO format, when exporting separately in its own file strings that do not pertain to any module,  to indicate the application or module to which the translations apply.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_dominioPorDefecto_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_dominioPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Dato que aparece en los ficheros de exportacion de tipo GNUgettext PO, cuando se exportan separadamente en su propio fichero cadenas que no pertenecen a un modulo, para identificar la aplicacion o modulo a que se aplican las traducciones.",
        duplicates="0",
        label2="Domain for strings not in a module",
        ea_localid="1482",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Iinformation that appears in the exported files of GNUgettext PO format, when exporting separately in its own file strings that do not pertain to any module,  to indicate the application or module to which the translations apply.",
        ea_guid="{F9D57218-C3F9-4a24-804F-1CBB941BE9EA}",
        scale="0",
        default="gvSIGi18n",
        label="Dominio para cadenas sin modulo",
        length="0",
        containment="Not Specified",
        position="3",
        owner_class_name="TRACatalogo"
    ),

    IntegerField(
        name='maximoRegistrosExplorados',
        widget=IntegerField._properties['widget'](
            label="Numero maximo de registros de traduccion por pagina por defecto",
            label2="Default Maximum number of translations records per page",
            description="Numero maximo por defecto de Traducciones a presentar en las paginas de exploracion de traducciones, incluyendo traducciones al idioma a traducir y los idiomas de referencia.",
            description2="Default maximum  number of Translations to display in the Browse Translations page, including the language to translate and the reference languages.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_maximoRegistrosExplorados_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_maximoRegistrosExplorados_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Numero maximo por defecto de Traducciones a presentar en las paginas de exploracion de traducciones, incluyendo traducciones al idioma a traducir y los idiomas de referencia.",
        duplicates="0",
        label2="Default Maximum number of translations records per page",
        ea_localid="1473",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Default maximum  number of Translations to display in the Browse Translations page, including the language to translate and the reference languages.",
        ea_guid="{67D9B63D-C0D9-415d-A897-ED577D4B403B}",
        scale="0",
        default="1000",
        label="Numero maximo de registros de traduccion por pagina por defecto",
        length="0",
        containment="Not Specified",
        position="11",
        owner_class_name="TRACatalogo"
    ),

    IntegerField(
        name='traduccionesPorPaginaPorDefecto',
        widget=IntegerField._properties['widget'](
            label="Numero de Traducciones en pagina por defecto",
            label2="Default Translations per page",
            description="Numero de Traducciones por defecto a presentar en las paginas de exploracion sin contar las traducciones a los idiomas de referencia.",
            description2="Default number of Translations to display in the Browse Translations page, not counting the translations into the reference languages.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_traduccionesPorPaginaPorDefecto_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_traduccionesPorPaginaPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Numero de Traducciones por defecto a presentar en las paginas de exploracion sin contar las traducciones a los idiomas de referencia.",
        duplicates="0",
        label2="Default Translations per page",
        ea_localid="1472",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Default number of Translations to display in the Browse Translations page, not counting the translations into the reference languages.",
        ea_guid="{45B4E6BA-E3C6-4711-8AAF-EBB8AFBE2E51}",
        scale="0",
        default="40",
        label="Numero de Traducciones en pagina por defecto",
        length="0",
        containment="Not Specified",
        position="35",
        owner_class_name="TRACatalogo"
    ),

    IntegerField(
        name='segundosParaConfirmarImportacion',
        widget=IntegerField._properties['widget'](
            label="Tiempo en segundos para confirmar Importacion",
            label2="Time in seconds to confirm Import process",
            description="Tiempo en segundos del que dispone el Usuario para confirmar lanzamiento de proceso de Importacion. Si no confirma en este tiempo, y desea importar, el Usuario debera volver a solicitar la importacion.",
            description2="Time in seconds for the User to confirm launching the Import process. If the User does not confirm in this period of time, and he wishes to perform the import, the user shall request Import again.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_segundosParaConfirmarImportacion_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_segundosParaConfirmarImportacion_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Tiempo en segundos del que dispone el Usuario para confirmar lanzamiento de proceso de Importacion. Si no confirma en este tiempo, y desea importar, el Usuario debera volver a solicitar la importacion.",
        duplicates="0",
        label2="Time in seconds to confirm Import process",
        ea_localid="1481",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Time in seconds for the User to confirm launching the Import process. If the User does not confirm in this period of time, and he wishes to perform the import, the user shall request Import again.",
        ea_guid="{76EBC4E2-29D0-454a-81D5-6CFB778DA50E}",
        scale="0",
        default="300",
        label="Tiempo en segundos para confirmar Importacion",
        length="0",
        containment="Not Specified",
        position="31",
        owner_class_name="TRACatalogo"
    ),

    StringField(
        name='formatoExportacionPorDefecto',
        widget=SelectionWidget(
            label="Formato de exportacion por defecto",
            label2="Default Export format",
            description="Formato de los ficheros de exportacion de traducciones como Java .properties, o GNUtettext PO.",
            description2="Format for the translations export files, as Java .properties or GNUgettext .PO.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_formatoExportacionPorDefecto_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_formatoExportacionPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Formato de los ficheros de exportacion de traducciones como Java .properties, o GNUtettext PO.",
        vocabulary=['Java .properties','GNU gettext PO',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRACatalogo_attr_formatoExportacionPorDefecto_option_Java .properties', 'gvSIGi18n_TRACatalogo_attr_formatoExportacionPorDefecto_option_GNU gettext PO'],
        label2="Default Export format",
        ea_localid="1485",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Format for the translations export files, as Java .properties or GNUgettext .PO.",
        ea_guid="{C6606610-C3A2-4570-B1AB-BB1EA6440D72}",
        vocabulary2=['Java .properties','GNU gettext PO',],
        scale="0",
        default="Java .properties",
        label="Formato de exportacion por defecto",
        length="0",
        containment="Not Specified",
        position="7",
        owner_class_name="TRACatalogo"
    ),

    StringField(
        name='incluirLocalesCSVPorDefecto',
        widget=SelectionWidget(
            label="Incluir fichero locales.csv",
            label2="Include locales.csv file",
            description="Incluir en el archivo descargable un fichero locales.csv declarando los ficheros de traducciones contenidos en el archivo (usado por gvSIG).",
            description2="Include in the downloadable archive, a locales.csv file declaring the translations files contained in the archive (used by gvSIG).",
            label_msgid='gvSIGi18n_TRACatalogo_attr_incluirLocalesCSVPorDefecto_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_incluirLocalesCSVPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Incluir en el archivo descargable un fichero locales.csv declarando los ficheros de traducciones contenidos en el archivo (usado por gvSIG).",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRACatalogo_attr_incluirLocalesCSVPorDefecto_option_Si', 'gvSIGi18n_TRACatalogo_attr_incluirLocalesCSVPorDefecto_option_No'],
        label2="Include locales.csv file",
        ea_localid="1490",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Include in the downloadable archive, a locales.csv file declaring the translations files contained in the archive (used by gvSIG).",
        ea_guid="{72E1D590-624C-4811-BB31-C20DD511A15D}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Incluir fichero locales.csv",
        length="0",
        containment="Not Specified",
        position="8",
        owner_class_name="TRACatalogo"
    ),

    StringField(
        name='incluirManifestPorDefecto',
        widget=SelectionWidget(
            label="Incluir fichero MANIFEST.MF",
            label2="Include MANIFEST.MF file",
            description="Incluir en el archivo descargable un fichero MANIFEST.MF declarando los ficheros de traducciones contenidos en el archivo.",
            description2="Include in the downloadable archive, a MANIFEST.MF file declaring the translations files contained in the archive.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_incluirManifestPorDefecto_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_incluirManifestPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Incluir en el archivo descargable un fichero MANIFEST.MF declarando los ficheros de traducciones contenidos en el archivo.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRACatalogo_attr_incluirManifestPorDefecto_option_Si', 'gvSIGi18n_TRACatalogo_attr_incluirManifestPorDefecto_option_No'],
        label2="Include MANIFEST.MF file",
        ea_localid="1486",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Include in the downloadable archive, a MANIFEST.MF file declaring the translations files contained in the archive.",
        ea_guid="{BB4A760D-1F44-4825-852C-FE565C027E97}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Incluir fichero MANIFEST.MF",
        length="0",
        containment="Not Specified",
        position="9",
        owner_class_name="TRACatalogo"
    ),

    StringField(
        name='modulosPorSeparadoPorDefecto',
        widget=SelectionWidget(
            label="Exportar modulos por separado",
            label2="Export separated modules",
            description="Exportar cada modulo por separado en su propio fichero, todos ellos incluidos en el archivo descargable.",
            description2="Exprot each module in its own file, with all of them packed in the downloadable archive.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_modulosPorSeparadoPorDefecto_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_modulosPorSeparadoPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Exportar cada modulo por separado en su propio fichero, todos ellos incluidos en el archivo descargable.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRACatalogo_attr_modulosPorSeparadoPorDefecto_option_Si', 'gvSIGi18n_TRACatalogo_attr_modulosPorSeparadoPorDefecto_option_No'],
        label2="Export separated modules",
        ea_localid="1487",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Exprot each module in its own file, with all of them packed in the downloadable archive.",
        ea_guid="{238F900C-0D19-4a2d-96B6-1D26B987CACC}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Exportar modulos por separado",
        length="0",
        containment="Not Specified",
        position="14",
        owner_class_name="TRACatalogo"
    ),

    StringField(
        name='tipoArchivoExportacionPorDefecto',
        widget=SelectionWidget(
            label="Tipo de archivo descargable por defecto",
            label2="Default downladable archive kind",
            description="Tipo de archivo en que se descargan el modulo o modulos exportados. Puede ser .jar o .zip.",
            description2="Type of the archive used to pack the module or modules for download.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_tipoArchivoExportacionPorDefecto_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_tipoArchivoExportacionPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Tipo de archivo en que se descargan el modulo o modulos exportados. Puede ser .jar o .zip.",
        vocabulary=['.jar','.zip',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRACatalogo_attr_tipoArchivoExportacionPorDefecto_option_.jar', 'gvSIGi18n_TRACatalogo_attr_tipoArchivoExportacionPorDefecto_option_.zip'],
        label2="Default downladable archive kind",
        ea_localid="1488",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Type of the archive used to pack the module or modules for download.",
        ea_guid="{93F813BD-34E0-4e2e-956F-EDF70D324A35}",
        vocabulary2=['.jar','.zip',],
        scale="0",
        default=".zip",
        label="Tipo de archivo descargable por defecto",
        length="0",
        containment="Not Specified",
        position="34",
        owner_class_name="TRACatalogo"
    ),

    StringField(
        name='modoGestionErrorCodificacionExportacionPorDefecto',
        widget=SelectionWidget(
            label="Modo de gestion de errores de codificacion",
            label2="Encoding errors handling mode",
            description="Como reaccionar ante la ocurrencia de errores de codificacion de caracteres durante la exportacion de traducciones.",
            description2="How to react upon occurences of encoding errors errors during the translations export process.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_modoGestionErrorCodificacionExportacionPorDefecto_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_modoGestionErrorCodificacionExportacionPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Como reaccionar ante la ocurrencia de errores de codificacion de caracteres durante la exportacion de traducciones.",
        vocabulary=[ 'Cancelar al primer error', 'Contar todos los errores y cancelar', 'Ignorar y continuar', 'Sustituir y continuar', 'Sustituir por XML y continuar', 'Sustituir por escape y continuar',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRACatalogo_attr_modoGestionErrorCodificacionExportacionPorDefecto_option_Cancelar al primer error', 'gvSIGi18n_TRACatalogo_attr_modoGestionErrorCodificacionExportacionPorDefecto_option_Contar todos los errores y cancelar', 'gvSIGi18n_TRACatalogo_attr_modoGestionErrorCodificacionExportacionPorDefecto_option_Ignorar y continuar', 'gvSIGi18n_TRACatalogo_attr_modoGestionErrorCodificacionExportacionPorDefecto_option_Sustituir y continuar', 'gvSIGi18n_TRACatalogo_attr_modoGestionErrorCodificacionExportacionPorDefecto_option_Sustituir por XML y continuar', 'gvSIGi18n_TRACatalogo_attr_modoGestionErrorCodificacionExportacionPorDefecto_option_Sustituir por escape y continuar'],
        label2="Encoding errors handling mode",
        ea_localid="1489",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="How to react upon occurences of encoding errors errors during the translations export process.",
        ea_guid="{FBE6DB96-51E1-45bd-BD8A-ED2B319AAFDD}",
        vocabulary2=[ 'Cancel on first error', 'Count all errors and cancel', 'Ignore and continue', 'Replace and continue', 'XML replace and continue', 'Backslash replace and continue',],
        scale="0",
        default="Sustituir por escape y continuar",
        label="Modo de gestion de errores de codificacion",
        length="0",
        containment="Not Specified",
        position="12",
        owner_class_name="TRACatalogo"
    ),

    StringField(
        name='exportarNombreFicheroParaGvSIGPorDefecto',
        widget=SelectionWidget(
            label="Export File for gvSIGby default",
            label2="Exportar Fichero para gvSIGpor defecto",
            description="Exportar Fichero con nombre segun el estandar de gvSIG para ficheros de distribucion de localizaciones.",
            description2="Export File with name according to the gvSIG standard for distribution of localization files.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_exportarNombreFicheroParaGvSIGPorDefecto_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_exportarNombreFicheroParaGvSIGPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Exportar Fichero con nombre segun el estandar de gvSIG para ficheros de distribucion de localizaciones.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRACatalogo_attr_exportarNombreFicheroParaGvSIGPorDefecto_option_Si', 'gvSIGi18n_TRACatalogo_attr_exportarNombreFicheroParaGvSIGPorDefecto_option_No'],
        label2="Exportar Fichero para gvSIGpor defecto",
        ea_localid="1592",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Export File with name according to the gvSIG standard for distribution of localization files.",
        ea_guid="{652CFFA7-EAE4-47d3-9288-0F78EC6E3877}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Export File for gvSIGby default",
        length="0",
        containment="Not Specified",
        position="6",
        owner_class_name="TRACatalogo"
    ),

    IntegerField(
        name='numeroDeActividadesAnularInformeActividad',
        widget=IntegerField._properties['widget'](
            label="Cambios para Anular Informe Actividad",
            label2="Changes to invalidate Activity Report",
            description="Numero de Actividades que causan la anulacion del Informe de Actividad, incluso aunque no haya expirado el plazo de retencion del informe.",
            description2="Number of Activities that shall cause the invalidation of the Activity Report, even if the minimum retention time has not lapsed yet.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_numeroDeActividadesAnularInformeActividad_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_numeroDeActividadesAnularInformeActividad_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Numero de Actividades que causan la anulacion del Informe de Actividad, incluso aunque no haya expirado el plazo de retencion del informe.",
        duplicates="0",
        label2="Changes to invalidate Activity Report",
        ea_localid="1600",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Number of Activities that shall cause the invalidation of the Activity Report, even if the minimum retention time has not lapsed yet.",
        ea_guid="{48B86632-5CF5-4034-8ADA-ACE2F48763DB}",
        scale="0",
        default="3",
        label="Cambios para Anular Informe Actividad",
        length="0",
        containment="Not Specified",
        position="18",
        owner_class_name="TRACatalogo"
    ),

    IntegerField(
        name='segundosMinimosRetencionInformeActividad',
        widget=IntegerField._properties['widget'](
            label="Minimo Tiempo en segundos que se retiene el Informe de Actividad",
            label2="Minimum Time in seconds to retain the Activity Report",
            description="Tiempo en segundos que se retendra el Informe deActividad, aunque sus resultados sean inexactos por alguna modificacion del estado de traducciones, para evitar recalculo excesivo por cambios poco relevantes.",
            description2="Time in seconds that the Activity Report shall be retained, even if the results have become inaccurate because of any modification of translations status. To avoid excessive recalculation for barely relevant changes.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_segundosMinimosRetencionInformeActividad_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_segundosMinimosRetencionInformeActividad_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Tiempo en segundos que se retendra el Informe deActividad, aunque sus resultados sean inexactos por alguna modificacion del estado de traducciones, para evitar recalculo excesivo por cambios poco relevantes.",
        duplicates="0",
        label2="Minimum Time in seconds to retain the Activity Report",
        ea_localid="1599",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Time in seconds that the Activity Report shall be retained, even if the results have become inaccurate because of any modification of translations status. To avoid excessive recalculation for barely relevant changes.",
        ea_guid="{6B95C9E7-2D6C-4ca2-B5A3-1C3357F87D5C}",
        scale="0",
        default="60",
        label="Minimo Tiempo en segundos que se retiene el Informe de Actividad",
        length="0",
        containment="Not Specified",
        position="27",
        owner_class_name="TRACatalogo"
    ),

    IntegerField(
        name='segundosMinimosRetencionInformeIdiomas',
        widget=IntegerField._properties['widget'](
            label="Minimo Tiempo en segundos que se retiene el Informe de Estado por Idiomas",
            label2="Minimum Time in seconds to retain Status Report by Languages",
            description="Tiempo en segundos que se retendra el Informe de Estado por Idiomas, aunque sus resultados sean inexactos por alguna modificacion del estado de traducciones, para evitar recalculo excesivo por cambios poco relevantes.",
            description2="Time in seconds that the Status Report by Languages shall be retained, even if the results have become inaccurate because of any modification of translations status. To avoid excessive recalculation for barely relevant changes.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_segundosMinimosRetencionInformeIdiomas_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_segundosMinimosRetencionInformeIdiomas_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Tiempo en segundos que se retendra el Informe de Estado por Idiomas, aunque sus resultados sean inexactos por alguna modificacion del estado de traducciones, para evitar recalculo excesivo por cambios poco relevantes.",
        duplicates="0",
        label2="Minimum Time in seconds to retain Status Report by Languages",
        ea_localid="1583",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Time in seconds that the Status Report by Languages shall be retained, even if the results have become inaccurate because of any modification of translations status. To avoid excessive recalculation for barely relevant changes.",
        ea_guid="{46E6C4B5-2AD9-4d59-BD9A-C93ECB3C9265}",
        scale="0",
        default="120",
        label="Minimo Tiempo en segundos que se retiene el Informe de Estado por Idiomas",
        length="0",
        containment="Not Specified",
        position="28",
        owner_class_name="TRACatalogo"
    ),

    IntegerField(
        name='numeroDeCambiosAnularInformeIdiomas',
        widget=IntegerField._properties['widget'](
            label="Cambios para Anular Informe Idiomas",
            label2="Changes to invalidate Report by Languages",
            description="Numero de cambios de estado de Traducciones que causan la anulacion del Informe de Estado por Idiomas, incluso aunque no haya expirado el plazo de retencion del informe.",
            description2="Number of Translation status changes that shall cause the invalidation of the Status Report by Languages, even if the minimum retention time has not lapsed yet.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_numeroDeCambiosAnularInformeIdiomas_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_numeroDeCambiosAnularInformeIdiomas_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Numero de cambios de estado de Traducciones que causan la anulacion del Informe de Estado por Idiomas, incluso aunque no haya expirado el plazo de retencion del informe.",
        duplicates="0",
        label2="Changes to invalidate Report by Languages",
        ea_localid="1584",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Number of Translation status changes that shall cause the invalidation of the Status Report by Languages, even if the minimum retention time has not lapsed yet.",
        ea_guid="{72EA73A3-2DEC-4fbb-973D-A40573168F6C}",
        scale="0",
        default="5",
        label="Cambios para Anular Informe Idiomas",
        length="0",
        containment="Not Specified",
        position="19",
        owner_class_name="TRACatalogo"
    ),

    IntegerField(
        name='segundosMinimosRetencionInformeModulosEIdiomas',
        widget=IntegerField._properties['widget'](
            label="Minimo Tiempo en segundos que se retiene el Informe de Estado por Modulos e Idiomas",
            label2="Minimum Time in seconds to retain Status Report by Modules and Languages",
            description="Tiempo en segundos que se retendra el Informe de Estado por Modulos e Idiomas, aunque sus resultados sean inexactos por alguna modificacion del estado de traducciones, para evitar recalculo excesivo por cambios poco relevantes.",
            description2="Time in seconds that the Status Report by Modules and Languages shall be retained, even if the results have become inaccurate because of any modification of translations status. To avoid excessive recalculation for barely relevant changes.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_segundosMinimosRetencionInformeModulosEIdiomas_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_segundosMinimosRetencionInformeModulosEIdiomas_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Tiempo en segundos que se retendra el Informe de Estado por Modulos e Idiomas, aunque sus resultados sean inexactos por alguna modificacion del estado de traducciones, para evitar recalculo excesivo por cambios poco relevantes.",
        duplicates="0",
        label2="Minimum Time in seconds to retain Status Report by Modules and Languages",
        ea_localid="1587",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Time in seconds that the Status Report by Modules and Languages shall be retained, even if the results have become inaccurate because of any modification of translations status. To avoid excessive recalculation for barely relevant changes.",
        ea_guid="{D8B188A2-0626-40cd-B2BA-8759F7283616}",
        scale="0",
        default="300",
        label="Minimo Tiempo en segundos que se retiene el Informe de Estado por Modulos e Idiomas",
        length="0",
        containment="Not Specified",
        position="29",
        owner_class_name="TRACatalogo"
    ),

    IntegerField(
        name='numeroDeCambiosAnularInformeModulosEIdiomas',
        widget=IntegerField._properties['widget'](
            label="Cambios para Anular Informe Modulos e Idiomas",
            label2="Changes to invalidate Report by Modules and Languages",
            description="Numero de cambios de estado de Traducciones que causan la anulacion del Informe de Estado por Modulos e Idiomas, incluso aunque no haya expirado el plazo de retencion del informe.",
            description2="Number of Translation status changes that shall cause the invalidation of the Status Report by Modules and Languages, even if the minimum retention time has not lapsed yet.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_numeroDeCambiosAnularInformeModulosEIdiomas_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_numeroDeCambiosAnularInformeModulosEIdiomas_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Numero de cambios de estado de Traducciones que causan la anulacion del Informe de Estado por Modulos e Idiomas, incluso aunque no haya expirado el plazo de retencion del informe.",
        duplicates="0",
        label2="Changes to invalidate Report by Modules and Languages",
        ea_localid="1586",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Number of Translation status changes that shall cause the invalidation of the Status Report by Modules and Languages, even if the minimum retention time has not lapsed yet.",
        ea_guid="{88EC54C8-424B-4a1e-B0B8-9BADC4E3BFCF}",
        scale="0",
        default="20",
        label="Cambios para Anular Informe Modulos e Idiomas",
        length="0",
        containment="Not Specified",
        position="20",
        owner_class_name="TRACatalogo"
    ),

    IntegerField(
        name='maximoNumeroCambiosRecientes',
        widget=IntegerField._properties['widget'](
            label="Maximo numero de Cambios Recientes",
            label2="Maximum number of Recent Changes",
            description="El sistema recordara cambios recientes de estados de traducciones, hasta este maximo, despreciando los cambios mas antiguos cuando se exceda el maximo.",
            description2="The system shall record recent Translation status changes, up to this maximum, discarding the oldest ones when the maximum is exceeded,",
            label_msgid='gvSIGi18n_TRACatalogo_attr_maximoNumeroCambiosRecientes_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_maximoNumeroCambiosRecientes_help',
            i18n_domain='gvSIGi18n',
        ),
        description="El sistema recordara cambios recientes de estados de traducciones, hasta este maximo, despreciando los cambios mas antiguos cuando se exceda el maximo.",
        duplicates="0",
        label2="Maximum number of Recent Changes",
        ea_localid="1585",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="The system shall record recent Translation status changes, up to this maximum, discarding the oldest ones when the maximum is exceeded,",
        ea_guid="{FA1DD245-141B-46df-8764-2ACDE92809D2}",
        scale="0",
        default="5000",
        label="Maximo numero de Cambios Recientes",
        length="0",
        containment="Not Specified",
        position="10",
        owner_class_name="TRACatalogo"
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

    BooleanField(
        name='perfilDeEjecucionHabilitado',
        widget=BooleanField._properties['widget'](
            label="Perfil de Ejecucion Habilitado",
            label2="Execution Profiling Enabled",
            description="Si Verdadero, el sistema registrara el perfil de la ejecucion, como secuencias anidadas de plantillas y metodos ejecutados.",
            description2="When True, the System shall record the execution profile, as nested sequences of executed templates and methods.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_perfilDeEjecucionHabilitado_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_perfilDeEjecucionHabilitado_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, el sistema registrara el perfil de la ejecucion, como secuencias anidadas de plantillas y metodos ejecutados.",
        duplicates="0",
        label2="Execution Profiling Enabled",
        ea_localid="1710",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="When True, the System shall record the execution profile, as nested sequences of executed templates and methods.",
        ea_guid="{53AA8DDC-878D-4084-8E8D-21E0CA662C25}",
        scale="0",
        default="False",
        label="Perfil de Ejecucion Habilitado",
        length="0",
        containment="Not Specified",
        position="22",
        owner_class_name="TRACatalogo"
    ),

    BooleanField(
        name='tiemposDeEjecucionHabilitado',
        widget=BooleanField._properties['widget'](
            label="Tiempos de Ejecucion Habilitado",
            label2="Execution Timestamping Enabled",
            description="Si Verdadero, el sistema registrara el tiempo utilizado en la ejecucion, de plantillas y metodos.",
            description2="When True, the System shall record the time to execute templates and methods.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_tiemposDeEjecucionHabilitado_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_tiemposDeEjecucionHabilitado_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, el sistema registrara el tiempo utilizado en la ejecucion, de plantillas y metodos.",
        duplicates="0",
        label2="Execution Timestamping Enabled",
        ea_localid="1711",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="When True, the System shall record the time to execute templates and methods.",
        ea_guid="{A01EA392-A20F-4f09-AF50-A7AEF85D5B7D}",
        scale="0",
        default="False",
        label="Tiempos de Ejecucion Habilitado",
        length="0",
        containment="Not Specified",
        position="33",
        owner_class_name="TRACatalogo"
    ),

    BooleanField(
        name='registroRaizDeEjecucionAutomaticoHabilitado',
        widget=BooleanField._properties['widget'](
            label="Registro Raiz de Ejecucion Automatico Habilitado",
            label2="Execution auto root record Enabled",
            description="Si Verdadero, el sistema creara un registro de ejecucion raiz, cuando la plantilla o metodo que invoca no haya suministrado uno.",
            description2="If True, the system shall create a root execution record, when the caller template or method does not supply one.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_registroRaizDeEjecucionAutomaticoHabilitado_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_registroRaizDeEjecucionAutomaticoHabilitado_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, el sistema creara un registro de ejecucion raiz, cuando la plantilla o metodo que invoca no haya suministrado uno.",
        duplicates="0",
        label2="Execution auto root record Enabled",
        ea_localid="1712",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="If True, the system shall create a root execution record, when the caller template or method does not supply one.",
        ea_guid="{D291273D-8B6B-49d7-A21C-1B506AA55090}",
        scale="0",
        default="False",
        label="Registro Raiz de Ejecucion Automatico Habilitado",
        length="0",
        containment="Not Specified",
        position="26",
        owner_class_name="TRACatalogo"
    ),

    BooleanField(
        name='escrituraEnDiscoDeRegistroDeEjecucionHabilitado',
        widget=BooleanField._properties['widget'](
            label="Escritura en Disco de Perfil de Ejecucion Habilitado",
            label2="Log Execution Profile to Disc Enabled",
            description="Si Verdadero, el sistema escribira el perfil de ejecucion en fichero de log en disco.",
            description2="If True, the system shall write the execution profile to the log.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_escrituraEnDiscoDeRegistroDeEjecucionHabilitado_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_escrituraEnDiscoDeRegistroDeEjecucionHabilitado_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, el sistema escribira el perfil de ejecucion en fichero de log en disco.",
        duplicates="0",
        label2="Log Execution Profile to Disc Enabled",
        ea_localid="1713",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="If True, the system shall write the execution profile to the log.",
        ea_guid="{933CC6B5-A0EE-4909-9FB5-3FFDDD6F0B23}",
        scale="0",
        default="False",
        label="Escritura en Disco de Perfil de Ejecucion Habilitado",
        length="0",
        containment="Not Specified",
        position="5",
        owner_class_name="TRACatalogo"
    ),

    BooleanField(
        name='escrituraEnDiscoDeRegistroDeEjecucionDetalladoHabilitado',
        widget=BooleanField._properties['widget'](
            label="Escritura en Disco de Perfil Detallado de Ejecucion Habilitado",
            label2="Log Detailed Execution Profile to Disc Enabled",
            description="Si Verdadero, el sistema escribira detalladamente el perfil de ejecucion en  fichero de log en disco.",
            description2="If True, the system shall write the execution profile to the log in a detailed form.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_escrituraEnDiscoDeRegistroDeEjecucionDetalladoHabilitado_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_escrituraEnDiscoDeRegistroDeEjecucionDetalladoHabilitado_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, el sistema escribira detalladamente el perfil de ejecucion en  fichero de log en disco.",
        duplicates="0",
        label2="Log Detailed Execution Profile to Disc Enabled",
        ea_localid="1714",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="If True, the system shall write the execution profile to the log in a detailed form.",
        ea_guid="{BCA930B7-404D-421e-A338-6BC9BB56BDAC}",
        scale="0",
        default="False",
        label="Escritura en Disco de Perfil Detallado de Ejecucion Habilitado",
        length="0",
        containment="Not Specified",
        position="4",
        owner_class_name="TRACatalogo"
    ),

    BooleanField(
        name='presentacionEnPaginasDeRegistroDeEjecucionHabilitado',
        widget=BooleanField._properties['widget'](
            label="Presentacion en Paginas de Perfil de Ejecucion Habilitado",
            label2="Render Execution Profile in Pages Enabled",
            description="Si Verdadero, el sistema presentara en las paginas el perfil de ejecucion.",
            description2="If True, the system shall present in pages the execution profile.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_presentacionEnPaginasDeRegistroDeEjecucionHabilitado_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_presentacionEnPaginasDeRegistroDeEjecucionHabilitado_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, el sistema presentara en las paginas el perfil de ejecucion.",
        duplicates="0",
        label2="Render Execution Profile in Pages Enabled",
        ea_localid="1715",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="If True, the system shall present in pages the execution profile.",
        ea_guid="{FF2655B6-37DE-4bf4-BC46-2A7CCB15E703}",
        scale="0",
        default="False",
        label="Presentacion en Paginas de Perfil de Ejecucion Habilitado",
        length="0",
        containment="Not Specified",
        position="24",
        owner_class_name="TRACatalogo"
    ),

    BooleanField(
        name='presentacionEnPaginasDeTiempoDeEjecucionHabilitado',
        widget=BooleanField._properties['widget'](
            label="Presentacion en Paginas de Tiempo de Ejecucion Habilitado",
            label2="Render Execution Time in Pages Enabled",
            description="Si Verdadero, el sistema presentara en las paginas el tiempo de ejecucion.",
            description2="If True, the system shall present in pages the execution time.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_presentacionEnPaginasDeTiempoDeEjecucionHabilitado_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_presentacionEnPaginasDeTiempoDeEjecucionHabilitado_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, el sistema presentara en las paginas el tiempo de ejecucion.",
        duplicates="0",
        label2="Render Execution Time in Pages Enabled",
        ea_localid="1716",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="If True, the system shall present in pages the execution time.",
        ea_guid="{74A16EEE-AE7E-44a9-92BC-FD9AA763B394}",
        scale="0",
        default="False",
        label="Presentacion en Paginas de Tiempo de Ejecucion Habilitado",
        length="0",
        containment="Not Specified",
        position="25",
        owner_class_name="TRACatalogo"
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

    StringField(
        name='modoInteraccionPorDefecto',
        widget=SelectionWidget(
            label="Modo de Interaccion con el Servidor por defecto",
            label2="Default Server Interaction mode",
            description="Cuando sea Asincrono el navegador de internet enviara los cambios al servidor sin refrescar toda la pagina, permitiendo continuar el trabajo en la pagina actual. Cuando Sincrono, enviara cambios al servidor cargando una pagina completamente nueva.",
            description2="When Asynchronous the internet browser will send changes to server without refreshing the whole page, allowing continuation of work in the current page. When Synchronous the internet browser will send changes to server by loading a completely new page.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_modoInteraccionPorDefecto_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_modoInteraccionPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Cuando sea Asincrono el navegador de internet enviara los cambios al servidor sin refrescar toda la pagina, permitiendo continuar el trabajo en la pagina actual. Cuando Sincrono, enviara cambios al servidor cargando una pagina completamente nueva.",
        vocabulary=['Asincrono','Sincrono',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRACatalogo_attr_modoInteraccionPorDefecto_option_Asincrono', 'gvSIGi18n_TRACatalogo_attr_modoInteraccionPorDefecto_option_Sincrono'],
        label2="Default Server Interaction mode",
        ea_localid="1474",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="When Asynchronous the internet browser will send changes to server without refreshing the whole page, allowing continuation of work in the current page. When Synchronous the internet browser will send changes to server by loading a completely new page.",
        ea_guid="{91F167D6-FD4A-4bc6-B459-84FB38E33705}",
        vocabulary2=['Asynchronous','Syncronous',],
        scale="0",
        default="Asincrono",
        label="Modo de Interaccion con el Servidor por defecto",
        length="0",
        containment="Not Specified",
        position="13",
        owner_class_name="TRACatalogo"
    ),

    TextField(
        name='modulosYSimbolosCadenasOrdenados',
        widget=TextAreaWidget(
            label="Modulos y Simbolos Cadenas ordenados",
            label2="Module names and Sorted String symbols",
            description="Nombres de Modulos y los Simbolos de las cadenas a traducir en el modulo, ordenados.",
            description2="Module names and the Symbols of strings to be translated in the module, sorted.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_modulosYSimbolosCadenasOrdenados_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_modulosYSimbolosCadenasOrdenados_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Nombres de Modulos y los Simbolos de las cadenas a traducir en el modulo, ordenados.",
        duplicates="0",
        label2="Module names and Sorted String symbols",
        ea_localid="885",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Module names and the Symbols of strings to be translated in the module, sorted.",
        ea_guid="{0151EBEF-7A6C-4482-863B-4CE43ABC1EBD}",
        scale="0",
        label="Modulos y Simbolos Cadenas ordenados",
        length="0",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        position="15",
        owner_class_name="TRACatalogo"
    ),

    ComputedField(
        name='parametrosControlProgreso',
        widget=ComputedWidget(
            label="Parametros control progreso",
            label2="Progress control parameters",
            description="Parametros controlando la gestion del progreso de procesos de larga duracion, incluyendo registro, transacciones, guardar resultados y ceder procesador.",
            description2="Parameters controlling the management of the progress of long-lived processes, including logging, transactions, store results and yield processor.",
            label_msgid='gvSIGi18n_TRACatalogo_contents_parametrosControlProgreso_label',
            description_msgid='gvSIGi18n_TRACatalogo_contents_parametrosControlProgreso_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=False,
        label2='Progress control parameters',
        label='Parametros control progreso',
        represents_aggregation=True,
        description2='Parameters controlling the management of the progress of long-lived processes, including logging, transactions, store results and yield processor.',
        multiValued=1,
        owner_class_name="TRACatalogo",
        expression="context.objectValues(['TRAParametrosControlProgreso'])",
        computed_types=['TRAParametrosControlProgreso'],
        non_framework_elements=False,
        description='Parametros controlando la gestion del progreso de procesos de larga duracion, incluyendo registro, transacciones, guardar resultados y ceder procesador.'
    ),

    IntegerField(
        name='segundosParaConfirmarAccion',
        widget=IntegerField._properties['widget'](
            label="Tiempo en segundos para confirmar Accion",
            label2="Time in seconds to confirm launch of a long process",
            description="Tiempo en segundos del que dispone el Usuario para confirmar lanzamiento de procesos de larga duracion. Si no confirma en este tiempo, el Usuario debera volver a solicitar la accion.",
            description2="Time in seconds for the User to confirm the launch of a long process. If the User does not confirm in this period of time, the user shall request the action again.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_segundosParaConfirmarAccion_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_segundosParaConfirmarAccion_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Tiempo en segundos del que dispone el Usuario para confirmar lanzamiento de procesos de larga duracion. Si no confirma en este tiempo, el Usuario debera volver a solicitar la accion.",
        duplicates="0",
        label2="Time in seconds to confirm launch of a long process",
        ea_localid="1605",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Time in seconds for the User to confirm the launch of a long process. If the User does not confirm in this period of time, the user shall request the action again.",
        ea_guid="{EA7AA3DF-5BD4-4644-A3D4-F42F915299A1}",
        scale="0",
        default="120",
        label="Tiempo en segundos para confirmar Accion",
        length="0",
        containment="Not Specified",
        position="30",
        owner_class_name="TRACatalogo"
    ),

    TextField(
        name='simbolosCadenasOrdenados',
        widget=TextAreaWidget(
            label="Simbolos Cadenas ordenados",
            label2="Sorted String symbols",
            description="Simbolos de las cadenas a traducir, ordenados.",
            description2="Symbols of strings to be translated, sorted.",
            label_msgid='gvSIGi18n_TRACatalogo_attr_simbolosCadenasOrdenados_label',
            description_msgid='gvSIGi18n_TRACatalogo_attr_simbolosCadenasOrdenados_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Simbolos de las cadenas a traducir, ordenados.",
        duplicates="0",
        label2="Sorted String symbols",
        ea_localid="304",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Symbols of strings to be translated, sorted.",
        ea_guid="{2DEB38F4-8102-464c-9DA0-02070A9777D2}",
        scale="0",
        label="Simbolos Cadenas ordenados",
        length="0",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        position="32",
        owner_class_name="TRACatalogo"
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



    allowed_content_types = ['TRAColeccionInformes', 'TRAColeccionCadenas', 'TRAParametrosControlProgreso', 'TRAColeccionImportaciones', 'TRAColeccionSolicitudesCadenas', 'TRAColeccionIdiomas', 'TRAColeccionProgresos', 'TRAColeccionModulos'] + list(getattr(TRAArquetipo, 'allowed_content_types', [])) + list(getattr(TRACatalogo_Inicializacion, 'allowed_content_types', [])) + list(getattr(TRACatalogo_Informes, 'allowed_content_types', [])) + list(getattr(TRACatalogo_Globales, 'allowed_content_types', [])) + list(getattr(TRACatalogo_Operaciones, 'allowed_content_types', [])) + list(getattr(TRACatalogo_CursorTraducciones, 'allowed_content_types', [])) + list(getattr(TRACatalogo_Actividad, 'allowed_content_types', [])) + list(getattr(TRACatalogo_Exportacion, 'allowed_content_types', [])) + list(getattr(TRAConRegistroActividad, 'allowed_content_types', []))
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
        'condition': """python:True or object.fUseCaseCheckDoable( 'EllaborateInformeActividad')"""
       },


       {'action': "string:${object_url}/Tabular/",
        'category': "object",
        'id': 'TRA_advanced',
        'name': 'Details',
        'permissions': ("View",),
        'condition': """python:object.fUseCaseCheckDoable( 'Advanced_View_on_any_TRA_element')"""
       },


       {'action': "string:${object_url}/TRAConfirmarBloquearCatalogo",
        'category': "object_buttons",
        'id': 'TRA_bloquear_catalogo',
        'name': 'Lock Catalog',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fUseCaseCheckDoable( 'Lock_TRACatalogo')"""
       },


       {'action': "string:${object_url}/Editar",
        'category': "object_buttons",
        'id': 'TRA_configurar',
        'name': 'Configure',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fUseCaseCheckDoable( 'Configure_TRACatalogo')"""
       },


       {'action': "string:${object_url}/TRABackup_action",
        'category': "object_buttons",
        'id': 'TRA_export_backup',
        'name': 'Export Backup',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fUseCaseCheckDoable( 'Backup_TRACatalogo')"""
       },


       {'action': "string:${object_url}/idiomas/TRACrear_Idioma",
        'category': "object_buttons",
        'id': 'TRACreateLanguage',
        'name': 'Create Language',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fObtenerColeccionIdiomas() and object.fObtenerColeccionIdiomas().fUseCaseCheckDoable( 'Create_TRAIdioma')"""
       },


       {'action': "string:${object_url}/informes/TRACrear_Informe",
        'category': "object_buttons",
        'id': 'TRACreateInforme',
        'name': 'Create Report',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fObtenerColeccionInformes() and object.fObtenerColeccionInformes().fUseCaseCheckDoable( 'Create_TRAInforme')"""
       },


       {'action': "string:${object_url}/modulos/TRACrear_Modulo",
        'category': "object_buttons",
        'id': 'TRACreateModule',
        'name': 'Create Module',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fObtenerColeccionModulos() and object.fObtenerColeccionModulos().fUseCaseCheckDoable( 'Create_TRAModulo')"""
       },


       {'action': "string:${object_url}/solicitudescadenas/TRACrear_SolicitudCadena/?theNewTypeName=TRASolicitudCadena&theAggregationName=solicitudesCadenas",
        'category': "object_buttons",
        'id': 'TRACreateSolicitudCadena',
        'name': 'Create New String Request',
        'permissions': ("View",),
        'condition': """python:object.fObtenerColeccionSolicitudesCadenas() and object.fObtenerColeccionSolicitudesCadenas().fUseCaseCheckDoable( 'Create_TRASolicitudCadena')"""
       },


       {'action': "string:${object_url}/TRAConfirmarDesbloquearCatalogo",
        'category': "object_buttons",
        'id': 'TRA_desbloquear_catalogo',
        'name': 'Unlock Catalog',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fUseCaseCheckDoable( 'Unlock_TRACatalogo')"""
       },


       {'action': "string:${object_url}/TRACatalogoDetalle",
        'category': "object",
        'id': 'TRA_detalle',
        'name': 'Report',
        'permissions': ("View",),
        'condition': """python:object.fUseCaseCheckDoable( 'EllaborateInformeModulesAndLanguages')"""
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
        'condition': """python:object.fUseCaseCheckDoable( 'Export')"""
       },


       {'action': "string:${object_url}/TRACatalogoInforme",
        'category': "object",
        'id': 'TRA_informe',
        'name': 'Summary',
        'permissions': ("View",),
        'condition': """python:object.fUseCaseCheckDoable( 'EllaborateInformeLanguages')"""
       },


       {'action': "string:${object_url}/TRAInicializar_action",
        'category': "object_buttons",
        'id': 'TRA_inicializar',
        'name': 'Initialize',
        'permissions': ("View",),
        'condition': """python:object.fUseCaseCheckDoable( 'Initialize_TRACatalogo')"""
       },


       {'action': "string:${object_url}/TRAVerificar_action",
        'category': "object_buttons",
        'id': 'TRA_verificar',
        'name': 'Verify',
        'permissions': ("View",),
        'condition': """python:object.fUseCaseCheckDoable( 'Verify_TRACatalogo')"""
       },


       {'action': "string:${object_url}/TRACatalogo",
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
        
        return TRAElemento_Operaciones.fExtraLinks( self)

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
        
        return self.pHandle_manage_pasteObjects( cb_copy_data, REQUEST)
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



