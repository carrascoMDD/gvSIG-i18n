# -*- coding: utf-8 -*-
#
# File: TRAConfiguracionImportacion.py
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
from Products.gvSIGi18n.TRAConfiguracion import TRAConfiguracion
from TRAConfiguracionImportacion_Operaciones import TRAConfiguracionImportacion_Operaciones
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from TRAElemento_Operaciones import TRAElemento_Operaciones

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='nombreModuloPorDefecto',
        widget=StringWidget(
            label="Nombre de Modulo por defecto",
            label2="Default Module Name",
            description="Nombre del modulo a utilizar cuando Importar usando nombre de modulo configurado, o no se puede obtener, bien del nombre del dominio en ficheros GNU gettext .PO, o de la estructura de carpetas si el contenido a importar es una archivo .jar o .zip.",
            description2="Name of the Module to use when no module name can be obtained, whether from domain name in the GNUgettext .POfile header, or from the folder structure if the uploaded content is a .jar or .zip archive file.",
            label_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_nombreModuloPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_nombreModuloPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Nombre del modulo a utilizar cuando Importar usando nombre de modulo configurado, o no se puede obtener, bien del nombre del dominio en ficheros GNU gettext .PO, o de la estructura de carpetas si el contenido a importar es una archivo .jar o .zip.",
        duplicates="0",
        label2="Default Module Name",
        ea_localid="1955",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Name of the Module to use when no module name can be obtained, whether from domain name in the GNUgettext .POfile header, or from the folder structure if the uploaded content is a .jar or .zip archive file.",
        ea_guid="{075D57BC-7B14-4b7a-9F29-E9E7C435B737}",
        scale="0",
        default="gvSIG",
        label="Nombre de Modulo por defecto",
        length="0",
        containment="Not Specified",
        position="6",
        owner_class_name="TRAConfiguracionImportacion"
    ),

    StringField(
        name='codigoIdiomaPorDefecto',
        widget=StringWidget(
            label="Codigo de Idioma por defecto",
            label2="Default Language Code",
            description="Codigo del lenguage para importar plantillas de traduccion GNUgettext .POT, o para Java .properties que no tienen el codigo del lenguage como sufijo en el nombre del fichero.",
            description2="Code of the language to import GNU gettext .POT translation templates whose Java .properties import or export files do not contain the language code in the file name as a suffix.",
            label_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_codigoIdiomaPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_codigoIdiomaPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Codigo del lenguage para importar plantillas de traduccion GNUgettext .POT, o para Java .properties que no tienen el codigo del lenguage como sufijo en el nombre del fichero.",
        duplicates="0",
        label2="Default Language Code",
        ea_localid="1954",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Code of the language to import GNU gettext .POT translation templates whose Java .properties import or export files do not contain the language code in the file name as a suffix.",
        ea_guid="{9351B483-BBCC-4368-B835-38F699157B8B}",
        scale="0",
        default="es",
        label="Codigo de Idioma por defecto",
        length="0",
        containment="Not Specified",
        position="0",
        owner_class_name="TRAConfiguracionImportacion"
    ),

    IntegerField(
        name='segundosParaConfirmarImportacion',
        widget=IntegerField._properties['widget'](
            label="Tiempo en segundos para confirmar Importacion",
            label2="Time in seconds to confirm Import process",
            description="Tiempo en segundos del que dispone el Usuario para confirmar lanzamiento de proceso de Importacion. Si no confirma en este tiempo, y desea importar, el Usuario debera volver a solicitar la importacion.",
            description2="Time in seconds for the User to confirm launching the Import process. If the User does not confirm in this period of time, and he wishes to perform the import, the user shall request Import again.",
            label_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_segundosParaConfirmarImportacion_label',
            description_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_segundosParaConfirmarImportacion_help',
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
        position="8",
        owner_class_name="TRAConfiguracionImportacion"
    ),

    IntegerField(
        name='numeroMaximoLineasAExplorar',
        widget=IntegerField._properties['widget'](
            label="Numero Maximo de Lineas a Explorar",
            label2="Maximum Number of Lines to Scan",
            description="Cuando se lea un fichero de intercambio de traducciones, se exploraran hasta este numero maximo de lineas.",
            description2="When scanning a translations interchange file, the system shall scan up to this maximum number of lines.",
            label_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_numeroMaximoLineasAExplorar_label',
            description_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_numeroMaximoLineasAExplorar_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Cuando se lea un fichero de intercambio de traducciones, se exploraran hasta este numero maximo de lineas.",
        duplicates="0",
        label2="Maximum Number of Lines to Scan",
        ea_localid="1968",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="When scanning a translations interchange file, the system shall scan up to this maximum number of lines.",
        ea_guid="{4E1946AD-4C9D-4175-9B0B-4DB5A6D370B6}",
        scale="0",
        default="100000",
        label="Numero Maximo de Lineas a Explorar",
        length="0",
        containment="Not Specified",
        position="7",
        owner_class_name="TRAConfiguracionImportacion"
    ),

    BooleanField(
        name='importarConNombreModuloConfiguradoPorDefecto',
        widget=BooleanField._properties['widget'](
            label="Importar usando nombre de modulo configurado",
            label2="Import using configured module name",
            description="Importar usando el nombre de modulo configurado para la importacion o el contenido de intercambio",
            description2="Import using the module name configured for the import or the interchange contents",
            label_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarConNombreModuloConfiguradoPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarConNombreModuloConfiguradoPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Importar usando el nombre de modulo configurado para la importacion o el contenido de intercambio",
        duplicates="0",
        label2="Import using configured module name",
        ea_localid="1927",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import using the module name configured for the import or the interchange contents",
        ea_guid="{4C075F78-C973-404b-84C7-550079B8BB9E}",
        scale="0",
        default="True",
        label="Importar usando nombre de modulo configurado",
        length="0",
        containment="Not Specified",
        position="1",
        owner_class_name="TRAConfiguracionImportacion"
    ),

    BooleanField(
        name='importarNombresModulosDesdeComentariosPorDefecto',
        widget=BooleanField._properties['widget'](
            label="Importar nombres de modulos desde comentarios",
            label2="Import module names from comments",
            description="Importar los nombres de modulos de cada cadena, desde sus comentarios en el fichero .properties o GNUgettextPO.",
            description2="Import the names of modules for each string, from its comments in the .properties or GNUgettextPO file.",
            label_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarNombresModulosDesdeComentariosPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarNombresModulosDesdeComentariosPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Importar los nombres de modulos de cada cadena, desde sus comentarios en el fichero .properties o GNUgettextPO.",
        duplicates="0",
        label2="Import module names from comments",
        ea_localid="1930",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import the names of modules for each string, from its comments in the .properties or GNUgettextPO file.",
        ea_guid="{93FEF7EF-F237-4f36-95EC-AFE83AAE799A}",
        scale="0",
        default="True",
        label="Importar nombres de modulos desde comentarios",
        length="0",
        containment="Not Specified",
        position="4",
        owner_class_name="TRAConfiguracionImportacion"
    ),

    BooleanField(
        name='importarNombreModuloDesdeDominioONombreFicheroPorDefecto',
        widget=BooleanField._properties['widget'](
            label="Importar modulo de nombre de fichero o domino PO",
            label2="Import module from file name or PO Domain",
            description="Importar nombre de modulo del nombre de fichero o linea de domino del fichero GNU gettext PO",
            description2="Import module name from the file name or GNU gettext PO header Domain line",
            label_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarNombreModuloDesdeDominioONombreFicheroPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarNombreModuloDesdeDominioONombreFicheroPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Importar nombre de modulo del nombre de fichero o linea de domino del fichero GNU gettext PO",
        duplicates="0",
        label2="Import module from file name or PO Domain",
        ea_localid="1929",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import module name from the file name or GNU gettext PO header Domain line",
        ea_guid="{28404054-55A6-4594-B3EB-8509136E0225}",
        scale="0",
        default="True",
        label="Importar modulo de nombre de fichero o domino PO",
        length="0",
        containment="Not Specified",
        position="3",
        owner_class_name="TRAConfiguracionImportacion"
    ),

    BooleanField(
        name='importarFuentesDesdeComentariosPorDefecto',
        widget=BooleanField._properties['widget'](
            label="Importar fuentes desde comentarios",
            label2="Import sources from comments",
            description="Importar los nombres de ficheros fuentes que donde aparece cada cadena, desde sus comentarios en el fichero .properties o GNUgettextPO.",
            description2="Import the names of source files where each string appears, from its comments in the .properties or GNUgettextPO file.",
            label_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarFuentesDesdeComentariosPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarFuentesDesdeComentariosPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Importar los nombres de ficheros fuentes que donde aparece cada cadena, desde sus comentarios en el fichero .properties o GNUgettextPO.",
        duplicates="0",
        label2="Import sources from comments",
        ea_localid="1928",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import the names of source files where each string appears, from its comments in the .properties or GNUgettextPO file.",
        ea_guid="{5322ACC9-6F7C-473c-8A7C-0862CE674858}",
        scale="0",
        default="True",
        label="Importar fuentes desde comentarios",
        length="0",
        containment="Not Specified",
        position="2",
        owner_class_name="TRAConfiguracionImportacion"
    ),

    BooleanField(
        name='importarStatusDesdeComentariosPorDefecto',
        widget=BooleanField._properties['widget'](
            label="Importar estado de traduciones de comentarios",
            label2="Import translations status from comments",
            description="Importar el estado de cada traduccion, desde sus comentarios en el fichero .properties o GNUgettextPO.",
            description2="Import the status of each translation, from its comments in the .properties or GNUgettextPO file.",
            label_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarStatusDesdeComentariosPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarStatusDesdeComentariosPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Importar el estado de cada traduccion, desde sus comentarios en el fichero .properties o GNUgettextPO.",
        duplicates="0",
        label2="Import translations status from comments",
        ea_localid="1931",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import the status of each translation, from its comments in the .properties or GNUgettextPO file.",
        ea_guid="{E9FDEF24-9560-4f3f-B352-7A91ABA4A835}",
        scale="0",
        default="True",
        label="Importar estado de traduciones de comentarios",
        length="0",
        containment="Not Specified",
        position="5",
        owner_class_name="TRAConfiguracionImportacion"
    ),

    BooleanField(
        name='importarXMLTRACatalogoPorDefecto',
        widget=BooleanField._properties['widget'](
            label="Importar propiedades TRACatalogo desde XML",
            label2="Import propertiesTRACatalogo in XML",
            description="Importar propiedades del catalogo raiz de traducciones desde fichero XML.",
            description2="Import properties of the root translations catalog from an XML file.",
            label_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarXMLTRACatalogoPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarXMLTRACatalogoPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Importar propiedades del catalogo raiz de traducciones desde fichero XML.",
        vocabulary=['Si','No',],
        duplicates="0",
        label2="Import propertiesTRACatalogo in XML",
        ea_localid="2021",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import properties of the root translations catalog from an XML file.",
        ea_guid="{88DA7EDD-22EE-4a3f-B513-6C4A9165D81D}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="False",
        label="Importar propiedades TRACatalogo desde XML",
        length="0",
        containment="Not Specified",
        position="10",
        owner_class_name="TRAConfiguracionImportacion"
    ),

    BooleanField(
        name='importarXMLTRAConfiguracionesPorDefecto',
        widget=BooleanField._properties['widget'](
            label="Importar las TRAConfiguracion desde XML",
            label2="Import the TRAConfiguracion from XML",
            description="Importar las configuraciones desde fichero XML.",
            description2="Import the configurations from an XML file.",
            label_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarXMLTRAConfiguracionesPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarXMLTRAConfiguracionesPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Importar las configuraciones desde fichero XML.",
        vocabulary=['Si','No',],
        duplicates="0",
        label2="Import the TRAConfiguracion from XML",
        ea_localid="2022",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import the configurations from an XML file.",
        ea_guid="{2A577FD7-1224-4c41-87C6-E441973A97FB}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="False",
        label="Importar las TRAConfiguracion desde XML",
        length="0",
        containment="Not Specified",
        position="12",
        owner_class_name="TRAConfiguracionImportacion"
    ),

    BooleanField(
        name='importarXMLTRAParametrosControlProgresoPorDefecto',
        widget=BooleanField._properties['widget'](
            label="Importar los TRAParametrosControlProgreso desde XML",
            label2="Import the TRAParametrosControlProgreso from XML",
            description="Importar los parametros control de progreso de procesos de larga duracion desde fichero XML.",
            description2="Import the long-lived progress control parameters from an XML file.",
            label_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarXMLTRAParametrosControlProgresoPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarXMLTRAParametrosControlProgresoPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Importar los parametros control de progreso de procesos de larga duracion desde fichero XML.",
        vocabulary=['Si','No',],
        duplicates="0",
        label2="Import the TRAParametrosControlProgreso from XML",
        ea_localid="2023",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import the long-lived progress control parameters from an XML file.",
        ea_guid="{96D47123-5E6D-4892-B3ED-EDCA44E129C9}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="False",
        label="Importar los TRAParametrosControlProgreso desde XML",
        length="0",
        containment="Not Specified",
        position="14",
        owner_class_name="TRAConfiguracionImportacion"
    ),

    BooleanField(
        name='importarXMLTRAIdiomasPorDefecto',
        widget=BooleanField._properties['widget'](
            label="Importar los TRAIdioma desde XML",
            label2="Import the TRAIdioma from XML",
            description="Importar los idiomas, y en su caso nombres de idioma y banderas asociadas, desde fichero XML.",
            description2="Import the languages, and when applicable the langusage names and flag, from an XML file.",
            label_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarXMLTRAIdiomasPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarXMLTRAIdiomasPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Importar los idiomas, y en su caso nombres de idioma y banderas asociadas, desde fichero XML.",
        vocabulary=['Si','No',],
        duplicates="0",
        label2="Import the TRAIdioma from XML",
        ea_localid="2024",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import the languages, and when applicable the langusage names and flag, from an XML file.",
        ea_guid="{CD9E4637-F1B3-46f6-BB17-4D4B26ED1D02}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="False",
        label="Importar los TRAIdioma desde XML",
        length="0",
        containment="Not Specified",
        position="16",
        owner_class_name="TRAConfiguracionImportacion"
    ),

    BooleanField(
        name='importarXMLTRASolicitudesCadenasPorDefecto',
        widget=BooleanField._properties['widget'](
            label="Importar los TRASolicitudCadena desde XML",
            label2="Import the TRASolicitudCadena from XML",
            description="Importar las solicitudes de nuevas cadenas desde fichero XML.",
            description2="Importar the new string requests from an XML file.",
            label_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarXMLTRASolicitudesCadenasPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarXMLTRASolicitudesCadenasPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Importar las solicitudes de nuevas cadenas desde fichero XML.",
        vocabulary=['Si','No',],
        duplicates="0",
        label2="Import the TRASolicitudCadena from XML",
        ea_localid="2029",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Importar the new string requests from an XML file.",
        ea_guid="{7C5A358B-3627-4a70-BF3B-8F53B4E77B11}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="False",
        label="Importar los TRASolicitudCadena desde XML",
        length="0",
        containment="Not Specified",
        position="18",
        owner_class_name="TRAConfiguracionImportacion"
    ),

    BooleanField(
        name='importarXMLTRAModulosPorDefecto',
        widget=BooleanField._properties['widget'](
            label="Importar los TRAModulo desde XML",
            label2="Import the TRAModulo from XML",
            description="Importar los modulos, desde fichero XML.",
            description2="Import the modules, from an XML file.",
            label_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarXMLTRAModulosPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarXMLTRAModulosPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Importar los modulos, desde fichero XML.",
        vocabulary=['Si','No',],
        duplicates="0",
        label2="Import the TRAModulo from XML",
        ea_localid="2025",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import the modules, from an XML file.",
        ea_guid="{3A3AD876-AF27-499b-8B06-0CF03F5ABCFA}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="False",
        label="Importar los TRAModulo desde XML",
        length="0",
        containment="Not Specified",
        position="21",
        owner_class_name="TRAConfiguracionImportacion"
    ),

    BooleanField(
        name='importarXMLTRAInformesPorDefecto',
        widget=BooleanField._properties['widget'](
            label="Importar los TRAInforme desde XML",
            label2="Import the TRAInforme from XML",
            description="Importar los informes, desde fichero XML.",
            description2="Import the reports, from an XML file.",
            label_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarXMLTRAInformesPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarXMLTRAInformesPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Importar los informes, desde fichero XML.",
        vocabulary=['Si','No',],
        duplicates="0",
        label2="Import the TRAInforme from XML",
        ea_localid="2026",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import the reports, from an XML file.",
        ea_guid="{69B84D9E-2232-42e9-8A0C-203B960F0CFC}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="False",
        label="Importar los TRAInforme desde XML",
        length="0",
        containment="Not Specified",
        position="22",
        owner_class_name="TRAConfiguracionImportacion"
    ),

    BooleanField(
        name='importarXMLTRAImportacionesPorDefecto',
        widget=BooleanField._properties['widget'](
            label="Importar las TRAImportacion desde XML",
            label2="Import the TRAImportacion from XML",
            description="Importar las importaciones desde fichero XML.",
            description2="Import the imports from an XML file.",
            label_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarXMLTRAImportacionesPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarXMLTRAImportacionesPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Importar las importaciones desde fichero XML.",
        vocabulary=['Si','No',],
        duplicates="0",
        label2="Import the TRAImportacion from XML",
        ea_localid="2027",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import the imports from an XML file.",
        ea_guid="{900E6BA1-9583-4d19-B7B5-A4E905BFB400}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="False",
        label="Importar las TRAImportacion desde XML",
        length="0",
        containment="Not Specified",
        position="24",
        owner_class_name="TRAConfiguracionImportacion"
    ),

    BooleanField(
        name='importarXMLTRAProgresosPorDefecto',
        widget=BooleanField._properties['widget'](
            label="Importar los TRAProgreso desde XML",
            label2="Import the TRAProgreso from XML",
            description="Importar los progresos y resultados de procesos de larga duracion desde fichero XML.",
            description2="Import the progresses and results of long-lived processes from an XML file.",
            label_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarXMLTRAProgresosPorDefecto_label',
            description_msgid='gvSIGi18n_TRAConfiguracionImportacion_attr_importarXMLTRAProgresosPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Importar los progresos y resultados de procesos de larga duracion desde fichero XML.",
        vocabulary=['Si','No',],
        duplicates="0",
        label2="Import the TRAProgreso from XML",
        ea_localid="2028",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import the progresses and results of long-lived processes from an XML file.",
        ea_guid="{196FE0D3-DF1D-43ba-9B9A-2BD2F5F8039B}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="False",
        label="Importar los TRAProgreso desde XML",
        length="0",
        containment="Not Specified",
        position="25",
        owner_class_name="TRAConfiguracionImportacion"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAConfiguracionImportacion_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAConfiguracion, 'schema', Schema(())).copy() + \
    getattr(TRAConfiguracionImportacion_Operaciones, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAConfiguracionImportacion(OrderedBaseFolder, TRAConfiguracion, TRAConfiguracionImportacion_Operaciones):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAConfiguracion,'__implements__',()),) + (getattr(TRAConfiguracionImportacion_Operaciones,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Configuracion Importacion'

    meta_type = 'TRAConfiguracionImportacion'
    portal_type = 'TRAConfiguracionImportacion'


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



    allowed_content_types = [] + list(getattr(TRAConfiguracion, 'allowed_content_types', [])) + list(getattr(TRAConfiguracionImportacion_Operaciones, 'allowed_content_types', []))
    filter_content_types             = 1
    global_allow                     = 0
    content_icon = 'traconfiguracion.gif'
    immediate_view                   = 'Tabular'
    default_view                     = 'Tabular'
    suppl_views                      = ['Tabular',]
    typeDescription                  = "Configuracion del catalogo de traducciones, con parametros controlando las operaciones de importacion sobre el catalogo."
    typeDescMsgId                    =  'gvSIGi18n_TRAConfiguracionImportacion_help'
    archetype_name2                  = 'Import Configuration'
    typeDescription2                 = '''Translations catalog configuration, with parameters controlling import operations on the catalog.'''
    archetype_name_msgid             = 'gvSIGi18n_TRAConfiguracionImportacion_label'
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

    schema = TRAConfiguracionImportacion_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata', 'sharing', 'folderContents']:
            a['visible'] = 0
    return fti

registerType(TRAConfiguracionImportacion, PROJECTNAME)
# end of class TRAConfiguracionImportacion

##code-section module-footer #fill in your manual code here
##/code-section module-footer



