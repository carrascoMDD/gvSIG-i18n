# -*- coding: utf-8 -*-
#
# File: TRAImportacion.py
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
from TRAImportacion_Operaciones import TRAImportacion_Operaciones
from Products.gvSIGi18n.TRAConRegistroActividad import TRAConRegistroActividad
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from TRAElemento_Operaciones import TRAElemento_Operaciones

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='usuarioImportador',
        widget=StringWidget(
            label="Usuario Importador",
            label2="Importer User",
            description="Usuario que ha realizado la importacion.",
            description2="User who performed the import operation.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_usuarioImportador_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_usuarioImportador_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Usuario que ha realizado la importacion.",
        duplicates="0",
        label2="Importer User",
        ea_localid="602",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="User who performed the import operation.",
        ea_guid="{FD6A0BBC-E2F5-4e26-8D9C-EE4A84C26E7E}",
        read_only="True",
        scale="0",
        label="Usuario Importador",
        length="0",
        default_method="fGetMemberId_safe",
        position="23",
        owner_class_name="TRAImportacion"
    ),

    BooleanField(
        name='debeCrearTraduccionesQueFaltan',
        widget=BooleanField._properties['widget'](
            label="Debe crear Traducciones que falten",
            label2="Must create missing Translations",
            description="Crear las Traducciones que faltan para las cadenas e idiomas existentes, quiza por interrupcion indeseada de procesos de importacion anteriores.",
            description2="Create missing Translations in the existing strings and languages, may be because of unintended interruption of past import processes.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_debeCrearTraduccionesQueFaltan_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_debeCrearTraduccionesQueFaltan_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Crear las Traducciones que faltan para las cadenas e idiomas existentes, quiza por interrupcion indeseada de procesos de importacion anteriores.",
        duplicates="0",
        label2="Must create missing Translations",
        ea_localid="1479",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Create missing Translations in the existing strings and languages, may be because of unintended interruption of past import processes.",
        ea_guid="{1C34370F-12D2-476e-8D1B-F64F98B76BA5}",
        scale="0",
        default="False",
        label="Debe crear Traducciones que falten",
        length="0",
        containment="Not Specified",
        position="2",
        owner_class_name="TRAImportacion"
    ),

    StringField(
        name='versionDelProducto',
        widget=StringWidget(
            label="Version del producto",
            label2="Product Version",
            description="Version del Producto que se importa en este proceso. Cuando se ejecute la importacion, este dato se establecera como el valor de la Ultima Version importada del producto, en el catalogo de traducciones.",
            description2="Product Version imported in this process. When the import executes, this data will be set as the value of the Last Imported Product Version in the translations catalog.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_versionDelProducto_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_versionDelProducto_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Version del Producto que se importa en este proceso. Cuando se ejecute la importacion, este dato se establecera como el valor de la Ultima Version importada del producto, en el catalogo de traducciones.",
        duplicates="0",
        label2="Product Version",
        ea_localid="419",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="Product Version imported in this process. When the import executes, this data will be set as the value of the Last Imported Product Version in the translations catalog.",
        containment="Not Specified",
        ea_guid="{4D88E1D8-7FDA-43fd-87C0-BA2A7D756AF3}",
        position="24",
        owner_class_name="TRAImportacion",
        label="Version del producto"
    ),

    StringField(
        name='buildDelProducto',
        widget=StringWidget(
            label="Identificador del Build",
            label2="Product Build identifier",
            description="Identificador del Build del Producto que se importa en este proceso. Cuando se ejecute la importacion, este dato se establecera como el valor del Identificador del Ultimo Build Importado, en el catalogo de traducciones.",
            description2="Product Build identifier imported in this process. When the import executes, this data will be set as the value of the Last Imported Product Build identifier  in the translations catalog.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_buildDelProducto_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_buildDelProducto_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Identificador del Build del Producto que se importa en este proceso. Cuando se ejecute la importacion, este dato se establecera como el valor del Identificador del Ultimo Build Importado, en el catalogo de traducciones.",
        duplicates="0",
        label2="Product Build identifier",
        ea_localid="432",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="Product Build identifier imported in this process. When the import executes, this data will be set as the value of the Last Imported Product Build identifier  in the translations catalog.",
        containment="Not Specified",
        ea_guid="{4A1EF8CC-9271-41a5-A444-5F92D60663CA}",
        position="0",
        owner_class_name="TRAImportacion",
        label="Identificador del Build"
    ),

    StringField(
        name='codigoIdiomaPorDefecto',
        widget=StringWidget(
            label="Codigo de Idioma por defecto",
            label2="Default Language Code",
            description="Codigo del lenguage para importar plantillas de traduccion GNUgettext .POT, o para Java .properties que no tienen el codigo del lenguage como sufijo en el nombre del fichero.",
            description2="Code of the language to import GNU gettext .POT translation templates whose Java .properties import or export files do not contain the language code in the file name as a suffix.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_codigoIdiomaPorDefecto_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_codigoIdiomaPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Codigo del lenguage para importar plantillas de traduccion GNUgettext .POT, o para Java .properties que no tienen el codigo del lenguage como sufijo en el nombre del fichero.",
        duplicates="0",
        label2="Default Language Code",
        ea_localid="1475",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Code of the language to import GNU gettext .POT translation templates whose Java .properties import or export files do not contain the language code in the file name as a suffix.",
        ea_guid="{BB3EE64B-208F-4d42-8813-9AC4632A1535}",
        scale="0",
        label="Codigo de Idioma por defecto",
        length="0",
        default_method="fInitial_CodigoIdiomaPorDefecto",
        position="1",
        owner_class_name="TRAImportacion"
    ),

    StringField(
        name='nombreModuloPorDefecto',
        widget=StringWidget(
            label="Nombre de Modulo por defecto",
            label2="Default Module Name",
            description="Nombre del modulo a utilizar cuando Importar usando nombre de modulo configurado, o no se puede obtener, bien del nombre del dominio en ficheros GNU gettext .PO, o de la estructura de carpetas si el contenido a importar es una archivo .jar o .zip.",
            description2="Name of the Module to use when no module name can be obtained, whether from domain name in the GNUgettext .POfile header, or from the folder structure if the uploaded content is a .jar or .zip archive file.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_nombreModuloPorDefecto_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_nombreModuloPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Nombre del modulo a utilizar cuando Importar usando nombre de modulo configurado, o no se puede obtener, bien del nombre del dominio en ficheros GNU gettext .PO, o de la estructura de carpetas si el contenido a importar es una archivo .jar o .zip.",
        duplicates="0",
        label2="Default Module Name",
        ea_localid="1476",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Name of the Module to use when no module name can be obtained, whether from domain name in the GNUgettext .POfile header, or from the folder structure if the uploaded content is a .jar or .zip archive file.",
        ea_guid="{1303B58A-C358-415e-A2AB-58A07B04C5A2}",
        scale="0",
        label="Nombre de Modulo por defecto",
        length="0",
        default_method="fInitial_NombreModuloPorDefecto",
        position="21",
        owner_class_name="TRAImportacion"
    ),

    IntegerField(
        name='numeroMaximoLineasAExplorar',
        widget=IntegerField._properties['widget'](
            label="Numero Maximo de Lineas a Explorar",
            label2="Maximum Number of Lines to Scan",
            description="Cuando se lea un fichero de intercambio de traducciones, se exploraran hasta este numero maximo de lineas.",
            description2="When scanning a translations interchange file, the system shall scan up to this maximum number of lines.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_numeroMaximoLineasAExplorar_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_numeroMaximoLineasAExplorar_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Cuando se lea un fichero de intercambio de traducciones, se exploraran hasta este numero maximo de lineas.",
        duplicates="0",
        label2="Maximum Number of Lines to Scan",
        ea_localid="1970",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="When scanning a translations interchange file, the system shall scan up to this maximum number of lines.",
        ea_guid="{23F5C125-A255-4324-A244-01154A9C24FD}",
        scale="0",
        label="Numero Maximo de Lineas a Explorar",
        length="0",
        default_method="fInitial_NumeroMaximoLineasAExplorar",
        position="22",
        owner_class_name="TRAImportacion"
    ),

    ComputedField(
        name='contenidos',
        widget=ComputedWidget(
            label="Contenido Intercambio Traducciones",
            label2="Translations Interchange Contents",
            description="Contiene cadenas y traducciones contribuidas por un usuario, para su importacion.",
            description2="Contains strings and translations contributed by a user, and to be imported.",
            label_msgid='gvSIGi18n_TRAImportacion_contents_contenidos_label',
            description_msgid='gvSIGi18n_TRAImportacion_contents_contenidos_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=False,
        label2='Translations Interchange Contents',
        additional_columns=['excluirDeImportacion', 'ficheroLeido'],
        label='Contenido Intercambio Traducciones',
        represents_aggregation=True,
        description2='Contains strings and translations contributed by a user, and to be imported.',
        multiValued=1,
        factory_views={ 'TRAContenidoIntercambio' : 'TRACrear_ContenidoIntercambio',},
        owner_class_name="TRAImportacion",
        expression="context.objectValues(['TRAContenidoIntercambio'])",
        computed_types=['TRAContenidoIntercambio'],
        non_framework_elements=False,
        description='Contiene cadenas y traducciones contribuidas por un usuario, para su importacion.'
    ),

    ComputedField(
        name='contenidoXML',
        widget=ComputedWidget(
            label="Contenido XML",
            label2="XML Contents",
            description="Contenido importado de un fichero XML de copia de seguridad de un catalogo de traducciones.",
            description2="Contents imported from an XML backup file from a translations catalog.",
            label_msgid='gvSIGi18n_TRAImportacion_contents_contenidoXML_label',
            description_msgid='gvSIGi18n_TRAImportacion_contents_contenidoXML_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=False,
        label2='XML Contents',
        label='Contenido XML',
        represents_aggregation=True,
        description2='Contents imported from an XML backup file from a translations catalog.',
        multiValued=1,
        owner_class_name="TRAImportacion",
        multiplicity_higher=1,
        expression="context.objectValues(['TRAContenidoXML'])",
        computed_types=['TRAContenidoXML'],
        non_framework_elements=False,
        description='Contenido importado de un fichero XML de copia de seguridad de un catalogo de traducciones.'
    ),

    StringField(
        name='identificadorElementoProgreso',
        widget=StringWidget(
            label="Identificador del elemento de Control del Progreso",
            label2="Progress Control element Identifier",
            description="Identificador del elemento utilizado para controlar el progreso del proceso de larga duración.",
            description2="Identifier of the element used to control the progress of the long-lived process.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_identificadorElementoProgreso_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_identificadorElementoProgreso_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Identificador del elemento utilizado para controlar el progreso del proceso de larga duración.",
        duplicates="0",
        label2="Progress Control element Identifier",
        ea_localid="1705",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Identifier of the element used to control the progress of the long-lived process.",
        ea_guid="{382328D2-90E8-4929-8E7D-5930E63A7540}",
        read_only="True",
        scale="0",
        label="Identificador del elemento de Control del Progreso",
        length="0",
        containment="Not Specified",
        position="4",
        owner_class_name="TRAImportacion"
    ),

    ComputedField(
        name='elementoProgreso',
        widget=ReferenceBrowserWidget(
            label="Elemento de Progreso y Resultados",
            label2="Progress and Results element",
            description="Elemento para control del Progreso de la importacion, y almacenamiento de los resultados de la importacion, durante y al final del proceso.",
            description2="Element to control the Progress of the import process, and storage of import results, during and after the import process.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_elementoProgreso_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_elementoProgreso_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Elemento para control del Progreso de la importacion, y almacenamiento de los resultados de la importacion, durante y al final del proceso.",
        duplicates="0",
        label2="Progress and Results element",
        ea_localid="1708",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Element to control the Progress of the import process, and storage of import results, during and after the import process.",
        ea_guid="{F2A04018-F016-4113-871D-44DD359B7D51}",
        allowed_types=['TRAProgreso'],
        read_only="True",
        scale="0",
        additional_columns=['estadoProceso', 'haCompletadoConExito'],
        label="Elemento de Progreso y Resultados",
        length="0",
        multiValued=0,
        containment="Not Specified",
        position="3",
        owner_class_name="TRAImportacion",
        expression="context.fDeriveElementoProgreso()",
        computed_types="['TRAProgreso', ]"
    ),

    BooleanField(
        name='importarConNombreModuloConfigurado',
        widget=BooleanField._properties['widget'](
            label="Importar usando nombre de modulo configurado",
            label2="Import using configured module name",
            description="Importar usando el nombre de modulo configurado para la importacion o el contenido de intercambio",
            description2="Import strings as used in the module with the name configured for the import or the interchange contents.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_importarConNombreModuloConfigurado_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_importarConNombreModuloConfigurado_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Importar usando el nombre de modulo configurado para la importacion o el contenido de intercambio",
        duplicates="0",
        label2="Import using configured module name",
        ea_localid="1729",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import strings as used in the module with the name configured for the import or the interchange contents.",
        ea_guid="{ED12A898-3143-4f5c-A730-EAC6B09BE9D2}",
        scale="0",
        label="Importar usando nombre de modulo configurado",
        length="0",
        default_method="fInitial_ImportarConNombreModuloConfigurado",
        position="5",
        owner_class_name="TRAImportacion"
    ),

    BooleanField(
        name='importarNombreModuloDesdeDominioONombreFichero',
        widget=BooleanField._properties['widget'](
            label="Importar modulo de nombre de fichero o domino PO",
            label2="Import module from file name or PO Domain",
            description="Importar nombre de modulo del nombre de fichero o linea de domino del fichero GNU gettext PO",
            description2="Import module name from the file name or GNU gettext PO header Domain line",
            label_msgid='gvSIGi18n_TRAImportacion_attr_importarNombreModuloDesdeDominioONombreFichero_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_importarNombreModuloDesdeDominioONombreFichero_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Importar nombre de modulo del nombre de fichero o linea de domino del fichero GNU gettext PO",
        duplicates="0",
        label2="Import module from file name or PO Domain",
        ea_localid="1728",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import module name from the file name or GNU gettext PO header Domain line",
        ea_guid="{049E7311-DA11-457a-8927-FF10B5F58DA7}",
        scale="0",
        label="Importar modulo de nombre de fichero o domino PO",
        length="0",
        default_method="fInitial_ImportarNombreModuloDesdeDominioONombreFichero",
        position="8",
        owner_class_name="TRAImportacion"
    ),

    BooleanField(
        name='importarNombresModulosDesdeComentarios',
        widget=BooleanField._properties['widget'](
            label="Importar nombres de modulos desde comentarios",
            label2="Import module names from comments",
            description="Importar los nombres de modulos de cada cadena, desde sus comentarios en el fichero .properties o GNUgettextPO.",
            description2="Import the names of modules for each string, from its comments in the .properties or GNUgettextPO file.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_importarNombresModulosDesdeComentarios_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_importarNombresModulosDesdeComentarios_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Importar los nombres de modulos de cada cadena, desde sus comentarios en el fichero .properties o GNUgettextPO.",
        duplicates="0",
        label2="Import module names from comments",
        ea_localid="1722",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import the names of modules for each string, from its comments in the .properties or GNUgettextPO file.",
        ea_guid="{EDF8DAA4-E273-410f-9588-1E3834025631}",
        scale="0",
        label="Importar nombres de modulos desde comentarios",
        length="0",
        default_method="fInitial_ImportarNombresModulosDesdeComentarios",
        position="9",
        owner_class_name="TRAImportacion"
    ),

    BooleanField(
        name='importarFuentesDesdeComentarios',
        widget=BooleanField._properties['widget'](
            label="Importar fuentes desde comentarios",
            label2="Import sources from comments",
            description="Importar los nombres de ficheros fuentes que donde aparece cada cadena, desde sus comentarios en el fichero .properties o GNUgettextPO.",
            description2="Import the names of source files where each string appears, from its comments in the .properties or GNUgettextPO file.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_importarFuentesDesdeComentarios_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_importarFuentesDesdeComentarios_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Importar los nombres de ficheros fuentes que donde aparece cada cadena, desde sus comentarios en el fichero .properties o GNUgettextPO.",
        duplicates="0",
        label2="Import sources from comments",
        ea_localid="1726",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import the names of source files where each string appears, from its comments in the .properties or GNUgettextPO file.",
        ea_guid="{3BD85B55-BAC1-43c4-A99D-F378D69E35AC}",
        scale="0",
        label="Importar fuentes desde comentarios",
        length="0",
        default_method="fInitial_ImportarFuentesDesdeComentarios",
        position="7",
        owner_class_name="TRAImportacion"
    ),

    BooleanField(
        name='importarStatusDesdeComentarios',
        widget=BooleanField._properties['widget'](
            label="Importar estado de traduciones de comentarios",
            label2="Import translations status from comments",
            description="Importar el estado de cada traduccion, desde sus comentarios en el fichero .properties o GNUgettextPO.",
            description2="Import the status of each translation, from its comments in the .properties or GNUgettextPO file.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_importarStatusDesdeComentarios_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_importarStatusDesdeComentarios_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Importar el estado de cada traduccion, desde sus comentarios en el fichero .properties o GNUgettextPO.",
        duplicates="0",
        label2="Import translations status from comments",
        ea_localid="1727",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import the status of each translation, from its comments in the .properties or GNUgettextPO file.",
        ea_guid="{22FF03B7-44F1-443e-9365-CA7053FB28E0}",
        scale="0",
        label="Importar estado de traduciones de comentarios",
        length="0",
        default_method="fInitial_ImportarStatusDesdeComentarios",
        position="10",
        owner_class_name="TRAImportacion"
    ),

    BooleanField(
        name='importarContribucionesDesdeComentarios',
        widget=BooleanField._properties['widget'](
            label="Importar fechas y usuarios contribuidores desde comentarios",
            label2="Import contributing dates and user names from comments",
            description="Importar desde comentarios de cada traduccion las fechas y nombres de usuario que la crearon, tradujeron, revisaron o marcaron como definitiva.",
            description2="Import from each translation comments the dates and user names that created, translated, reviewed or marked it as definitive.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_importarContribucionesDesdeComentarios_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_importarContribucionesDesdeComentarios_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Importar desde comentarios de cada traduccion las fechas y nombres de usuario que la crearon, tradujeron, revisaron o marcaron como definitiva.",
        duplicates="0",
        label2="Import contributing dates and user names from comments",
        ea_localid="2060",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import from each translation comments the dates and user names that created, translated, reviewed or marked it as definitive.",
        ea_guid="{BE805526-0906-4707-A5B6-9210757EBE47}",
        scale="0",
        default="True",
        label="Importar fechas y usuarios contribuidores desde comentarios",
        length="0",
        default_method="fInitial_ImportarContribucionesDesdeComentarios",
        position="11",
        owner_class_name="TRAImportacion"
    ),

    BooleanField(
        name='esRecuperacion',
        widget=BooleanField._properties['widget'](
            label="Importar para Recuperar copia de seguridad",
            label2="Import to Restore Backup",
            description="El proceso de importación recuperara contenido desde una copia de seguridad de catalogo de traducciones.",
            description2="The Import process shall restore contents from a backup of a translations catalog.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_esRecuperacion_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_esRecuperacion_help',
            i18n_domain='gvSIGi18n',
        ),
        description="El proceso de importación recuperara contenido desde una copia de seguridad de catalogo de traducciones.",
        duplicates="0",
        label2="Import to Restore Backup",
        ea_localid="2039",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="The Import process shall restore contents from a backup of a translations catalog.",
        ea_guid="{18A3AC25-634F-4199-A0ED-B8F4DFA005D5}",
        read_only="True",
        scale="0",
        default="False",
        label="Importar para Recuperar copia de seguridad",
        length="0",
        containment="Not Specified",
        position="2",
        owner_class_name="TRAImportacion"
    ),

    BooleanField(
        name='importarXMLTRACatalogo',
        widget=BooleanField._properties['widget'](
            label="Importar propiedades TRACatalogo desde XML",
            label2="Import propertiesTRACatalogo in XML",
            description="Importar propiedades del catalogo raiz de traducciones desde fichero XML.",
            description2="Import properties of the root translations catalog from an XML file.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_importarXMLTRACatalogo_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_importarXMLTRACatalogo_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Importar propiedades del catalogo raiz de traducciones desde fichero XML.",
        duplicates="0",
        label2="Import propertiesTRACatalogo in XML",
        ea_localid="2030",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import properties of the root translations catalog from an XML file.",
        ea_guid="{DA720A8C-6EB7-416f-839E-20FEBE797A50}",
        scale="0",
        label="Importar propiedades TRACatalogo desde XML",
        length="0",
        default_method="fInitial_ImportarXMLTRACatalogo",
        position="12",
        owner_class_name="TRAImportacion"
    ),

    BooleanField(
        name='importarXMLTRAConfiguraciones',
        widget=BooleanField._properties['widget'](
            label="Importar las TRAConfiguracion desde XML",
            label2="Import the TRAConfiguracion from XML",
            description="Importar las configuraciones desde fichero XML.",
            description2="Import the configurations from an XML file.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_importarXMLTRAConfiguraciones_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_importarXMLTRAConfiguraciones_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Importar las configuraciones desde fichero XML.",
        duplicates="0",
        label2="Import the TRAConfiguracion from XML",
        ea_localid="2031",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import the configurations from an XML file.",
        ea_guid="{D058E6AE-FD21-48a9-A8FD-F61EF1A2CD58}",
        scale="0",
        label="Importar las TRAConfiguracion desde XML",
        length="0",
        default_method="fInitial_ImportarXMLTRAConfiguraciones",
        position="11",
        owner_class_name="TRAImportacion"
    ),

    BooleanField(
        name='importarXMLTRAParametrosControlProgreso',
        widget=BooleanField._properties['widget'](
            label="Importar los TRAParametrosControlProgreso desde XML",
            label2="Import the TRAParametrosControlProgreso from XML",
            description="Importar los parametros control de progreso de procesos de larga duracion desde fichero XML.",
            description2="Import the long-lived progress control parameters from an XML file.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_importarXMLTRAParametrosControlProgreso_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_importarXMLTRAParametrosControlProgreso_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Importar los parametros control de progreso de procesos de larga duracion desde fichero XML.",
        duplicates="0",
        label2="Import the TRAParametrosControlProgreso from XML",
        ea_localid="2032",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import the long-lived progress control parameters from an XML file.",
        ea_guid="{59B402BE-4E7E-4cb8-A561-C474C5D03DCA}",
        scale="0",
        label="Importar los TRAParametrosControlProgreso desde XML",
        length="0",
        default_method="fInitial_ImportarXMLTRAParametrosControl",
        position="12",
        owner_class_name="TRAImportacion"
    ),

    BooleanField(
        name='importarXMLTRAIdiomas',
        widget=BooleanField._properties['widget'](
            label="Importar los TRAIdioma desde XML",
            label2="Import the TRAIdioma from XML",
            description="Importar los idiomas, y en su caso nombres de idioma y banderas asociadas, desde fichero XML.",
            description2="Import the languages, and when applicable the langusage names and flag, from an XML file.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_importarXMLTRAIdiomas_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_importarXMLTRAIdiomas_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Importar los idiomas, y en su caso nombres de idioma y banderas asociadas, desde fichero XML.",
        duplicates="0",
        label2="Import the TRAIdioma from XML",
        ea_localid="2033",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import the languages, and when applicable the langusage names and flag, from an XML file.",
        ea_guid="{7C46DAF1-4617-46cf-8B45-92347B2A12BB}",
        scale="0",
        label="Importar los TRAIdioma desde XML",
        length="0",
        default_method="fInitial_ImportarXMLTRAIdiomas",
        position="13",
        owner_class_name="TRAImportacion"
    ),

    BooleanField(
        name='importarXMLTRASolicitudesCadenas',
        widget=BooleanField._properties['widget'](
            label="Importar los TRASolicitudCadena desde XML",
            label2="Import the TRASolicitudCadena from XML",
            description="Importar las solicitudes de nuevas cadenas desde fichero XML.",
            description2="Importar the new string requests from an XML file.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_importarXMLTRASolicitudesCadenas_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_importarXMLTRASolicitudesCadenas_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Importar las solicitudes de nuevas cadenas desde fichero XML.",
        duplicates="0",
        label2="Import the TRASolicitudCadena from XML",
        ea_localid="2034",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Importar the new string requests from an XML file.",
        ea_guid="{4FB0780C-FC36-4320-843D-191809633C16}",
        scale="0",
        label="Importar los TRASolicitudCadena desde XML",
        length="0",
        default_method="fInitial_ImportarXMLTRASolicitudesCadenas",
        position="14",
        owner_class_name="TRAImportacion"
    ),

    BooleanField(
        name='importarXMLTRAModulos',
        widget=BooleanField._properties['widget'](
            label="Importar los TRAModulo desde XML",
            label2="Import the TRAModulo from XML",
            description="Importar los modulos, desde fichero XML.",
            description2="Import the modules, from an XML file.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_importarXMLTRAModulos_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_importarXMLTRAModulos_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Importar los modulos, desde fichero XML.",
        duplicates="0",
        label2="Import the TRAModulo from XML",
        ea_localid="2035",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import the modules, from an XML file.",
        ea_guid="{63C40DCD-FA1B-4075-922C-629764A668A2}",
        scale="0",
        label="Importar los TRAModulo desde XML",
        length="0",
        default_method="fInitial_ImportarXMLTRAModulos",
        position="15",
        owner_class_name="TRAImportacion"
    ),

    BooleanField(
        name='importarXMLTRAInformes',
        widget=BooleanField._properties['widget'](
            label="Importar los TRAInforme desde XML",
            label2="Import the TRAInforme from XML",
            description="Importar los informes, desde fichero XML.",
            description2="Import the reports, from an XML file.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_importarXMLTRAInformes_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_importarXMLTRAInformes_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Importar los informes, desde fichero XML.",
        duplicates="0",
        label2="Import the TRAInforme from XML",
        ea_localid="2036",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import the reports, from an XML file.",
        ea_guid="{063C66F6-134A-49d3-B66E-F9A70431B32F}",
        scale="0",
        label="Importar los TRAInforme desde XML",
        length="0",
        default_method="fInitial_ImportarXMLTRAInformes",
        position="16",
        owner_class_name="TRAImportacion"
    ),

    ComputedField(
        name='informeContenidosImportacion',
        exclude_from_views="[ 'Textual', 'Tabular', ]",
        widget=ComputedField._properties['widget'](
            label="Contenidos Importacion",
            label2="Import contents",
            description="Informe de lenguajes, cadenas y traducciones en los archivos de intercambio de traducciones.",
            description2="Report with languages, strings and translations in the translations interchange archives.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_informeContenidosImportacion_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_informeContenidosImportacion_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Informe de lenguajes, cadenas y traducciones en los archivos de intercambio de traducciones.",
        duplicates="0",
        label2="Import contents",
        ea_localid="1005",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Report with languages, strings and translations in the translations interchange archives.",
        ea_guid="{E334DFD5-961C-4b12-8949-2FD10D84E453}",
        exclude_from_values_form="True",
        scale="0",
        expression="context.fInformeContenidosImportacion()",
        label="Contenidos Importacion",
        length="0",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        position="20",
        owner_class_name="TRAImportacion",
        custom_presentation_view="TRAInformeContenidosImportacion_CustomView",
        computed_types="text",
        exclude_from_copyconfig="True",
        exclude_from_exportconfig="True"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAImportacion_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAArquetipo, 'schema', Schema(())).copy() + \
    getattr(TRAImportacion_Operaciones, 'schema', Schema(())).copy() + \
    getattr(TRAConRegistroActividad, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAImportacion(OrderedBaseFolder, TRAArquetipo, TRAImportacion_Operaciones, TRAConRegistroActividad):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAArquetipo,'__implements__',()),) + (getattr(TRAImportacion_Operaciones,'__implements__',()),) + (getattr(TRAConRegistroActividad,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Importacion'

    meta_type = 'TRAImportacion'
    portal_type = 'TRAImportacion'


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



    allowed_content_types = ['TRAContenidoXML', 'TRAContenidoIntercambio'] + list(getattr(TRAArquetipo, 'allowed_content_types', [])) + list(getattr(TRAImportacion_Operaciones, 'allowed_content_types', [])) + list(getattr(TRAConRegistroActividad, 'allowed_content_types', []))
    filter_content_types             = 1
    global_allow                     = 0
    content_icon = 'traimportacion.gif'
    immediate_view                   = 'Tabular'
    default_view                     = 'Tabular'
    suppl_views                      = ['Tabular',]
    typeDescription                  = "Conjunto de datos para importar, a partir de uno o mas archivos o ficheros, con contenido para intercambio de traducciones."
    typeDescMsgId                    =  'gvSIGi18n_TRAImportacion_help'
    archetype_name2                  = 'Import process'
    typeDescription2                 = '''Data set to be imported, from one or more archives or files, with translations interchange contents.'''
    archetype_name_msgid             = 'gvSIGi18n_TRAImportacion_label'
    factory_methods                  = { 'TRAContenidoIntercambio' : 'fCrearContenidoIntercambio',}
    factory_enablers                 = { 'TRAContenidoIntercambio' : [ 'fUseCaseCheckDoableFactory', 'Create_TRAContenidoIntercambio',]}
    propagate_delete_impact_to       = None
    allow_discussion = False


    actions =  (


       {'action': "string:${object_url}/TRAImportacionContenidosSumario",
        'category': "object",
        'id': 'TRASumarioContenidosImportacion',
        'name': 'Summary',
        'permissions': ("View",),
        'condition': """python:1"""
       },


       {'action': "string:${object_url}/TRAImportacionContenidosDetalle",
        'category': "object",
        'id': 'TRADetalleContenidosImportacion',
        'name': 'Details',
        'permissions': ("View",),
        'condition': """python:1"""
       },


       {'action': "string:${object_url}/contenidoxml/TRAContenidoXML",
        'category': "object",
        'id': 'TRAContenidoXML',
        'name': 'XML Contents',
        'permissions': ("View",),
        'condition': """python:object.fHasContenidoXML()"""
       },


       {'action': "string:${object_url}/TRAEstimarImportacion_action",
        'category': "object_buttons",
        'id': 'TRAEstimarImportacion_action',
        'name': 'Estimate Import',
        'permissions': ("View",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Estimate_TRAImportacion')"""
       },


       {'action': "string:${object_url}/TRAReutilizar_action",
        'category': "object_buttons",
        'id': 'TRAReuse',
        'name': 'Reuse',
        'permissions': ("Modify portal content",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Reuse_TRAImportacion')"""
       },


       {'action': "string:${object_url}/TRAImportar_action",
        'category': "object_buttons",
        'id': 'TRAImport',
        'name': 'Import',
        'permissions': ("Modify portal content",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Import_TRAImportacion')"""
       },


       {'action': "string:${object_url}/TRARecuperar_action",
        'category': "object_buttons",
        'id': 'TRARestoreTRACatalogo',
        'name': 'Restore Backup',
        'permissions': ("Modify portal content",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Restore_TRACatalogo')"""
       },


       {'action': "string:$object_url/Editar",
        'category': "object",
        'id': 'edit',
        'name': 'Edit',
        'permissions': ("Modify portal content",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Edit_TRAImportacion')"""
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

    schema = TRAImportacion_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('displayContentsTab')
    def displayContentsTab(self):
        """
        """
        
        return False

    security.declarePublic('fExtraLinks')
    def fExtraLinks(self):
        """
        """
        
        return TRAImportacion_Operaciones.fExtraLinks( self)

    security.declarePublic('fIsCacheable')
    def fIsCacheable(self):
        """
        """
        
        return True

    security.declarePublic('manage_afterAdd')
    def manage_afterAdd(self,item,container):
        """
        """
        
        return TRAImportacion_Operaciones.pHandle_manage_afterAdd( self, item, container)

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

registerType(TRAImportacion, PROJECTNAME)
# end of class TRAImportacion

##code-section module-footer #fill in your manual code here
##/code-section module-footer



