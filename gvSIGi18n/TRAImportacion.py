# -*- coding: utf-8 -*-
#
# File: TRAImportacion.py
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
from TRAImportacion_Operaciones import TRAImportacion_Operaciones
from Products.gvSIGi18n.TRAConRegistroActividad import TRAConRegistroActividad
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from TRAElemento_Operaciones import TRAElemento_Operaciones

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    BooleanField(
        name='comenzarAlFinalizarAnterior',
        widget=BooleanField._properties['widget'](
            label="Comenzar cuando acabe el anterior",
            label2="Launch when previous one terminates",
            description="Si Verdadero, y el proceso aun no ha sido ejecutado, el proceso sera ejecutado cuando acaba de ejecutarse el anterior",
            description2="If True, and the process has not been executed, then the process shall be executed when the previous one terminates.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_comenzarAlFinalizarAnterior_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_comenzarAlFinalizarAnterior_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, y el proceso aun no ha sido ejecutado, el proceso sera ejecutado cuando acaba de ejecutarse el anterior",
        duplicates="0",
        label2="Launch when previous one terminates",
        ea_localid="1578",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, and the process has not been executed, then the process shall be executed when the previous one terminates.",
        ea_guid="{8A2FCC2C-C80B-4cfb-807F-9A91CB791B09}",
        scale="0",
        default="False",
        label="Comenzar cuando acabe el anterior",
        length="0",
        containment="Not Specified",
        position="0",
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
        position="3",
        owner_class_name="TRAImportacion"
    ),

    BooleanField(
        name='crearInformeAntes',
        widget=BooleanField._properties['widget'](
            label="Crear Informe de Estado ANTES",
            label2="Create Status Report BEFORE",
            description="Cuendo sea verdadero, se creara un informe detallado de estado, antes del proceso de importacion.",
            description2="When true, a detailed status report shall be created before the import process.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_crearInformeAntes_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_crearInformeAntes_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Cuendo sea verdadero, se creara un informe detallado de estado, antes del proceso de importacion.",
        duplicates="0",
        label2="Create Status Report BEFORE",
        ea_localid="1597",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="When true, a detailed status report shall be created before the import process.",
        ea_guid="{4DED20F9-F187-48d5-A220-7EA18D0E0C6A}",
        scale="0",
        default="False",
        label="Crear Informe de Estado ANTES",
        length="0",
        containment="Not Specified",
        position="1",
        owner_class_name="TRAImportacion"
    ),

    BooleanField(
        name='crearInformeDespues',
        widget=BooleanField._properties['widget'](
            label="Crear Informe de Estado DESPUES",
            label2="Create Status Report AFTER",
            description="Cuendo sea verdadero, se creara un informe detallado de estado, despues del proceso de importacion.",
            description2="When true, a detailed status report shall be created after the import process.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_crearInformeDespues_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_crearInformeDespues_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Cuendo sea verdadero, se creara un informe detallado de estado, despues del proceso de importacion.",
        duplicates="0",
        label2="Create Status Report AFTER",
        ea_localid="1598",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="When true, a detailed status report shall be created after the import process.",
        ea_guid="{E3B22B84-2CB3-46d5-99DF-AD3B00CD02C2}",
        scale="0",
        default="False",
        label="Crear Informe de Estado DESPUES",
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
        position="4",
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
        position="5",
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
        default="es",
        label="Codigo de Idioma por defecto",
        length="0",
        containment="Not Specified",
        position="6",
        owner_class_name="TRAImportacion"
    ),

    StringField(
        name='nombreModuloPorDefecto',
        widget=StringWidget(
            label="Nombre de Modulo por defecto",
            label2="Default Module Name",
            description="Nombre del modulo a utilizar cuando no se puede obtener, bien del nombre del dominio en ficheros GNU gettext .PO, o de la estructura de carpetas si el contenido a importar es una archivo .jar o .zip.",
            description2="Name of the Module to use when no module name can be obtained, whether from domain name in the GNUgettext .POfile header, or from the folder structure if the uploaded content is a .jar or .zip archive file.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_nombreModuloPorDefecto_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_nombreModuloPorDefecto_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="Nombre del modulo a utilizar cuando no se puede obtener, bien del nombre del dominio en ficheros GNU gettext .PO, o de la estructura de carpetas si el contenido a importar es una archivo .jar o .zip.",
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
        default_method="fDefaultNombreModuloFromCatalog",
        position="7",
        owner_class_name="TRAImportacion"
    ),

    IntegerField(
        name='maximoLineasAImportarGNUgettextPO',
        widget=IntegerField._properties['widget'](
            label="Max #  lineas .PO",
            label2="Max #  lines .PO",
            description="Limita el numero de lineas a importar de ficheros GNU gettext .PO para evitar procesos de importacion demasiado largos, quiza por errores en los archivos de entrada.",
            description2="Limits the number of lines to import from GNUgettext .PO files, to avoid excessively long import processes, may be because of errors in the input files.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_maximoLineasAImportarGNUgettextPO_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_maximoLineasAImportarGNUgettextPO_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Limita el numero de lineas a importar de ficheros GNU gettext .PO para evitar procesos de importacion demasiado largos, quiza por errores en los archivos de entrada.",
        duplicates="0",
        label2="Max #  lines .PO",
        ea_localid="1477",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Limits the number of lines to import from GNUgettext .PO files, to avoid excessively long import processes, may be because of errors in the input files.",
        ea_guid="{5F62F53D-156D-498a-9429-D85333DBB744}",
        scale="0",
        default="50000",
        label="Max #  lineas .PO",
        length="0",
        containment="Not Specified",
        position="8",
        owner_class_name="TRAImportacion"
    ),

    IntegerField(
        name='maximoLineasAImportarJavaProperties',
        widget=IntegerField._properties['widget'](
            label="Max #  lineas .properties",
            label2="Max #  lines .properties",
            description="Limita el numero de lineas a importar de ficheros Java .properties para evitar procesos de importacion demasiado largos, quiza por errores en los archivos de entrada.",
            description2="Limits the number of lines to import from Java .properties files, to avoid excessively long import processes, may be because of errors in the input files.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_maximoLineasAImportarJavaProperties_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_maximoLineasAImportarJavaProperties_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Limita el numero de lineas a importar de ficheros Java .properties para evitar procesos de importacion demasiado largos, quiza por errores en los archivos de entrada.",
        duplicates="0",
        label2="Max #  lines .properties",
        ea_localid="1478",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Limits the number of lines to import from Java .properties files, to avoid excessively long import processes, may be because of errors in the input files.",
        ea_guid="{D92A23D8-5613-4df9-AA4E-6C7DE001EC26}",
        scale="0",
        default="10000",
        label="Max #  lineas .properties",
        length="0",
        containment="Not Specified",
        position="9",
        owner_class_name="TRAImportacion"
    ),

    IntegerField(
        name='intervaloRefrescoEnMinutos',
        widget=IntegerField._properties['widget'](
            label="Intervalo de Refresco en Minutos",
            label2="Refresh Interval in Minutes",
            description="Intervalo de tiempo en minutos tras las que se requiere que se actualize el estado e informe de progreso.",
            description2="Time interval in minutes after which it is required to update the progress state and report.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_intervaloRefrescoEnMinutos_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_intervaloRefrescoEnMinutos_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Intervalo de tiempo en minutos tras las que se requiere que se actualize el estado e informe de progreso.",
        duplicates="0",
        label2="Refresh Interval in Minutes",
        ea_localid="545",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Time interval in minutes after which it is required to update the progress state and report.",
        ea_guid="{F3C2ADA7-C427-4a41-8557-C9FFFA6ED6A4}",
        scale="0",
        default="3",
        label="Intervalo de Refresco en Minutos",
        length="0",
        containment="Not Specified",
        position="11",
        owner_class_name="TRAImportacion"
    ),

    IntegerField(
        name='intervaloRefrescoEnNumeroEscrituras',
        widget=IntegerField._properties['widget'](
            label="Intervalo de Refresco en Numero de Escrituras",
            label2="Refresh Interval in number of Writes",
            description="Numero de escrituras de cadenas o traducciones tras las que se requiere que se actualize el estado e informe de progreso. Use valores bajos ( <100) y la Espera entre Transacciones no nula, para dejar procesador a otros procesos o usuarios.",
            description2="Number of string or translation writes after which it is required to update the progress state and report. Use low values (<100) and a not null Delay between Transactions, to yield processing power to other processes and users.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_intervaloRefrescoEnNumeroEscrituras_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_intervaloRefrescoEnNumeroEscrituras_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Numero de escrituras de cadenas o traducciones tras las que se requiere que se actualize el estado e informe de progreso. Use valores bajos ( <100) y la Espera entre Transacciones no nula, para dejar procesador a otros procesos o usuarios.",
        duplicates="0",
        label2="Refresh Interval in number of Writes",
        ea_localid="531",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Number of string or translation writes after which it is required to update the progress state and report. Use low values (<100) and a not null Delay between Transactions, to yield processing power to other processes and users.",
        ea_guid="{9FD839DA-B533-416e-BD80-8133BD448A13}",
        scale="0",
        default="500",
        label="Intervalo de Refresco en Numero de Escrituras",
        length="0",
        containment="Not Specified",
        position="12",
        owner_class_name="TRAImportacion"
    ),

    FloatField(
        name='esperaEntreTransaccionesEnSegundos',
        widget=DecimalWidget(
            label="Segundos de Espera entre Transacciones",
            label2="Delay Seconds between Transactions",
            description="Con decimales. Intervalo de espera al final de una transaccion, antes de comenzar la siguiente. Util con valores bajos ( <100) del Intervalo de Refresco en Numero de Escrituras, para dejar libre capacidad de procesamiento para otros procesos o usuarios.",
            description2="With float values. Time to wait at the end of a transaction, before starting the next one. Usefule with low values of Refresh Interval in number of Writes (<100), to free processing power for other processes or users.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_esperaEntreTransaccionesEnSegundos_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_esperaEntreTransaccionesEnSegundos_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Con decimales. Intervalo de espera al final de una transaccion, antes de comenzar la siguiente. Util con valores bajos ( <100) del Intervalo de Refresco en Numero de Escrituras, para dejar libre capacidad de procesamiento para otros procesos o usuarios.",
        duplicates="0",
        label2="Delay Seconds between Transactions",
        ea_localid="1579",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="With float values. Time to wait at the end of a transaction, before starting the next one. Usefule with low values of Refresh Interval in number of Writes (<100), to free processing power for other processes or users.",
        ea_guid="{70CD4589-53E9-432e-921B-7ECC742676A5}",
        scale="0",
        default="0.0",
        label="Segundos de Espera entre Transacciones",
        length="0",
        containment="Not Specified",
        position="10",
        owner_class_name="TRAImportacion"
    ),

    IntegerField(
        name='numeroDeRefrescosPorEscrituraEnLog',
        widget=IntegerField._properties['widget'](
            label="Numero de Refrescos por Escritura en Log",
            label2="Number of Refreshes in each Write to the Log",
            description="Para evitar escribir demasiado frecuentemente en el registro de actividad, cuando se usan valores bajos del Intervalo de Refresco en Numero de Escrituras, este valor puede configurarse a valores altos (>10, < 100).",
            description2="To avoid writting too often to the log, when using low values for Refresh Interval in number of Writes, this value can be configured to high values (>10, <100).",
            label_msgid='gvSIGi18n_TRAImportacion_attr_numeroDeRefrescosPorEscrituraEnLog_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_numeroDeRefrescosPorEscrituraEnLog_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Para evitar escribir demasiado frecuentemente en el registro de actividad, cuando se usan valores bajos del Intervalo de Refresco en Numero de Escrituras, este valor puede configurarse a valores altos (>10, < 100).",
        duplicates="0",
        label2="Number of Refreshes in each Write to the Log",
        ea_localid="1580",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="To avoid writting too often to the log, when using low values for Refresh Interval in number of Writes, this value can be configured to high values (>10, <100).",
        ea_guid="{B48C7682-B5EC-4d06-88DD-786F91C60C11}",
        scale="0",
        default="1",
        label="Numero de Refrescos por Escritura en Log",
        length="0",
        containment="Not Specified",
        position="13",
        owner_class_name="TRAImportacion"
    ),

    IntegerField(
        name='numeroOperacionesAntesDeCederProcesador',
        widget=IntegerField._properties['widget'](
            label="Numero de Operaciones antes de ceder procesador",
            label2="Number of Operations before yielding the procesor",
            description="Para evitar que el proceso de importacion consuma una gran parte de la capacidad de proceso, se cedera el procesador, tras este numero de operaciones realizadas, tanto de lectura como escritura.",
            description2="To avoid the import process consuming most processing capacidty, the processor is yield to other processes after this number of read or write operations.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_numeroOperacionesAntesDeCederProcesador_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_numeroOperacionesAntesDeCederProcesador_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Para evitar que el proceso de importacion consuma una gran parte de la capacidad de proceso, se cedera el procesador, tras este numero de operaciones realizadas, tanto de lectura como escritura.",
        duplicates="0",
        label2="Number of Operations before yielding the procesor",
        ea_localid="1594",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="To avoid the import process consuming most processing capacidty, the processor is yield to other processes after this number of read or write operations.",
        ea_guid="{6F50CED8-B274-41f3-80C3-B8732F1F9681}",
        scale="0",
        default="50",
        label="Numero de Operaciones antes de ceder procesador",
        length="0",
        containment="Not Specified",
        position="15",
        owner_class_name="TRAImportacion"
    ),

    IntegerField(
        name='periodoActividadSinEsperaEnMilisegundos',
        widget=IntegerField._properties['widget'](
            label="Milisegundos de Actividad antes de ceder procesador",
            label2="Activity Milliseconds before yielding the procesor",
            description="if the value es bigger than 0, then Processor control shall not be yield until the specific number of millseconds of activity, even if the Number of Operations to yield has been reached.",
            description2="Si el valor es mayor que cero, entonces no se cedera el control del procesador, hasta completar el numero especificado de milisegundos de actividad, aunque se haya alcanzado el numero de operaciones para ceder",
            label_msgid='gvSIGi18n_TRAImportacion_attr_periodoActividadSinEsperaEnMilisegundos_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_periodoActividadSinEsperaEnMilisegundos_help',
            i18n_domain='gvSIGi18n',
        ),
        description="if the value es bigger than 0, then Processor control shall not be yield until the specific number of millseconds of activity, even if the Number of Operations to yield has been reached.",
        duplicates="0",
        label2="Activity Milliseconds before yielding the procesor",
        ea_localid="1596",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Si el valor es mayor que cero, entonces no se cedera el control del procesador, hasta completar el numero especificado de milisegundos de actividad, aunque se haya alcanzado el numero de operaciones para ceder",
        ea_guid="{2B870488-C5CE-4978-8877-8835D62527CB}",
        scale="0",
        default="1000",
        label="Milisegundos de Actividad antes de ceder procesador",
        length="0",
        containment="Not Specified",
        position="16",
        owner_class_name="TRAImportacion"
    ),

    FloatField(
        name='esperaTrasOperacionesEnSegundos',
        widget=DecimalWidget(
            label="Segundos a ceder procesador",
            label2="Seconds to yield processor",
            description="Con decimales, los segundos que se cede el procesador a otros procesos.",
            description2="With float values, number of seconds to yield the processor to other processes.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_esperaTrasOperacionesEnSegundos_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_esperaTrasOperacionesEnSegundos_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Con decimales, los segundos que se cede el procesador a otros procesos.",
        duplicates="0",
        label2="Seconds to yield processor",
        ea_localid="1595",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="With float values, number of seconds to yield the processor to other processes.",
        ea_guid="{491CC78E-CAB0-4542-8CFD-02662A04A2CF}",
        scale="0",
        default="1.0",
        label="Segundos a ceder procesador",
        length="0",
        containment="Not Specified",
        position="14",
        owner_class_name="TRAImportacion"
    ),

    TextField(
        name='informeFinal',
        widget=TextAreaWidget(
            label="Informe de Final",
            label2="Final report",
            description="Cuando el proceso de importacion finaliza con una condicion de error, contiene el informe de idiomas, cadenas y traducciones cargados.",
            description2="When the import process terminates, contains a report about the loaded languages, strings and translations.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_informeFinal_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_informeFinal_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Cuando el proceso de importacion finaliza con una condicion de error, contiene el informe de idiomas, cadenas y traducciones cargados.",
        duplicates="0",
        label2="Final report",
        ea_localid="359",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="When the import process terminates, contains a report about the loaded languages, strings and translations.",
        ea_guid="{7AC90C2B-BEF7-4b27-9713-6C6444B45750}",
        read_only="True",
        scale="0",
        custom_presentation_view="TRAInformeFinal_CustomView",
        label="Informe de Final",
        length="0",
        containment="Not Specified",
        position="25",
        owner_class_name="TRAImportacion",
        exclude_from_views="[ 'Textual',   'General', ]"
    ),

    TextField(
        name='informeExcepcion',
        widget=TextAreaWidget(
            label="Informe de Excepcion",
            label2="Exception report",
            description="Cuando el proceso de importacion finaliza con una condicion de error, contiene el informe del error de la aplicacion.",
            description2="When the import process terminates with an error, contains the applicacion exception report.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_informeExcepcion_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_informeExcepcion_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Cuando el proceso de importacion finaliza con una condicion de error, contiene el informe del error de la aplicacion.",
        duplicates="0",
        label2="Exception report",
        ea_localid="350",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="When the import process terminates with an error, contains the applicacion exception report.",
        ea_guid="{15F2246C-1D97-4d22-B8C5-316929236962}",
        read_only="True",
        scale="0",
        label="Informe de Excepcion",
        length="0",
        containment="Not Specified",
        position="26",
        owner_class_name="TRAImportacion"
    ),

    ComputedField(
        name='informeEstadoAntes',
        widget=ComputedField._properties['widget'](
            label="Informe Antes de la Importacion.",
            label2="Report Before Import",
            description="Informe del estado de traduccion, antes de la Importacion.",
            description2="Report or the translation status, before the export operation.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_informeEstadoAntes_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_informeEstadoAntes_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Informe del estado de traduccion, antes de la Importacion.",
        duplicates="0",
        label2="Report Before Import",
        ea_localid="1572",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Report or the translation status, before the export operation.",
        ea_guid="{3DA494F3-CF31-4852-B0B3-3BF62D85A463}",
        read_only="True",
        scale="0",
        expression="context.fInformeEstadoAntes()",
        label="Informe Antes de la Importacion.",
        length="0",
        containment="Not Specified",
        position="28",
        owner_class_name="TRAImportacion",
        exclude_from_views="[ 'Textual', 'General', ]",
        computed_types="[ 'TRAInforme',]"
    ),

    ComputedField(
        name='informeEstadoIdiomasAntes',
        widget=ComputedField._properties['widget'](
            label="Informe por Idiomas Antes de la Importacion.",
            label2="Languages Report Before Import",
            description="Informe del estado de traduccion por idiomas, antes de la Importacion.",
            description2="Report or the translation status, summarized by languages, before the export operation.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_informeEstadoIdiomasAntes_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_informeEstadoIdiomasAntes_help',
            i18n_domain='gvSIGi18n',
        ),
        custom_presentation_view="TRAInformeEstadoIdiomasAntes_CustomView",
        description="Informe del estado de traduccion por idiomas, antes de la Importacion.",
        duplicates="0",
        label2="Languages Report Before Import",
        ea_localid="923",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Report or the translation status, summarized by languages, before the export operation.",
        ea_guid="{DC88F36F-DB90-4f49-86CE-4D3A34B90648}",
        read_only="True",
        scale="0",
        expression="context.fDeriveInformeEstadoIdiomasAntes()",
        label="Informe por Idiomas Antes de la Importacion.",
        length="0",
        containment="Not Specified",
        position="29",
        owner_class_name="TRAImportacion",
        exclude_from_views="[ 'Textual',    'Tabular', 'General', ]",
        computed_types="text"
    ),

    ComputedField(
        name='informeEstadoModulosAntes',
        exclude_from_views="[ 'Textual',   'Tabular',  'General', ]",
        widget=ComputedField._properties['widget'](
            label="Informe por Modulos e Idiomas Antes de Importar",
            label2="Modules and Languages Report Before Import",
            description="Informe del estado de traduccion por modulos y detallado por  idiomas, antes de la exportacion.",
            description2="Report or the translation status, summarized by modules and detailed by languages, before the import operation.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_informeEstadoModulosAntes_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_informeEstadoModulosAntes_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Informe del estado de traduccion por modulos y detallado por  idiomas, antes de la exportacion.",
        duplicates="0",
        label2="Modules and Languages Report Before Import",
        ea_localid="926",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Report or the translation status, summarized by modules and detailed by languages, before the import operation.",
        ea_guid="{9D37A306-2FBC-4270-99CA-483739FE7193}",
        read_only="True",
        scale="0",
        expression="context.fDeriveInformeEstadoModulosAntes()",
        label="Informe por Modulos e Idiomas Antes de Importar",
        length="0",
        containment="Not Specified",
        position="30",
        owner_class_name="TRAImportacion",
        custom_presentation_view="TRAInformeEstadoModulosAntes_CustomView"
    ),

    ComputedField(
        name='informeEstadoDespues',
        widget=ComputedField._properties['widget'](
            label="Informe Despues de Importar",
            label2="Report After Import",
            description="Informe del estado de traduccion, despues de la importacion.",
            description2="Report or the translation status, after the import operation.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_informeEstadoDespues_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_informeEstadoDespues_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Informe del estado de traduccion, despues de la importacion.",
        duplicates="0",
        label2="Report After Import",
        ea_localid="1571",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Report or the translation status, after the import operation.",
        ea_guid="{5BB2A961-9BE2-440c-862E-43D138081361}",
        read_only="True",
        scale="0",
        exclude_from_views="[ 'Textual',   'General', ]",
        label="Informe Despues de Importar",
        length="0",
        containment="Not Specified",
        position="31",
        owner_class_name="TRAImportacion",
        expression="context.fInformeEstadoDespues()",
        computed_types="[ 'TRAInforme',]"
    ),

    ComputedField(
        name='informeEstadoIdiomasDespues',
        widget=ComputedField._properties['widget'](
            label="Informe por Idiomas Despues de Importar",
            label2="Languages Report After Import",
            description="Informe del estado de traduccion por idiomas, despues de la importacion.",
            description2="Report or the translation status, summarized by languages, after the import operation.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_informeEstadoIdiomasDespues_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_informeEstadoIdiomasDespues_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Informe del estado de traduccion por idiomas, despues de la importacion.",
        duplicates="0",
        label2="Languages Report After Import",
        ea_localid="940",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Report or the translation status, summarized by languages, after the import operation.",
        ea_guid="{78448E9D-6A53-4be6-ABE6-A3A539B2E8BE}",
        read_only="True",
        scale="0",
        exclude_from_views="[ 'Textual',    'Tabular', 'General', ]",
        label="Informe por Idiomas Despues de Importar",
        length="0",
        expression="context.fDeriveInformeEstadoIdiomasDespues()",
        containment="Not Specified",
        position="32",
        owner_class_name="TRAImportacion",
        custom_presentation_view="TRAInformeEstadoIdiomasDespues_CustomView",
        computed_types="text"
    ),

    ComputedField(
        name='informeEstadoModulosDespues',
        widget=ComputedField._properties['widget'](
            label="Informe por Modulos e Idiomas Despues de Importar",
            label2="Modules and Languages Report After Import",
            description="Informe del estado de traduccion por modulos y detallado por  idiomas, despues de la importacion.",
            description2="Report or the translation status, summarized by modules and detailed by languages, after the import operation.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_informeEstadoModulosDespues_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_informeEstadoModulosDespues_help',
            i18n_domain='gvSIGi18n',
        ),
        custom_presentation_view="TRAInformeEstadoModulosDespues_CustomView",
        description="Informe del estado de traduccion por modulos y detallado por  idiomas, despues de la importacion.",
        duplicates="0",
        label2="Modules and Languages Report After Import",
        ea_localid="943",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Report or the translation status, summarized by modules and detailed by languages, after the import operation.",
        ea_guid="{EC4C31D0-740F-4b37-8523-8FF1A679FB85}",
        read_only="True",
        scale="0",
        expression="context.fDeriveInformeEstadoModulosDespues()",
        label="Informe por Modulos e Idiomas Despues de Importar",
        length="0",
        containment="Not Specified",
        position="33",
        owner_class_name="TRAImportacion",
        exclude_from_views="[ 'Textual',   'Tabular',  'General', ]"
    ),

    TextField(
        name='informeCambios',
        widget=TextAreaWidget(
            label="Informe de Cambios",
            label2="Changes report",
            description="Informa de los cambios realizados durante la importacion: idiomas, modulos y cadenas creados, y traducciones cambiadas.",
            description2="Reports the changes made during the import process: created languages, modules and strings, and changed translations.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_informeCambios_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_informeCambios_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Informa de los cambios realizados durante la importacion: idiomas, modulos y cadenas creados, y traducciones cambiadas.",
        duplicates="0",
        label2="Changes report",
        ea_localid="1601",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Reports the changes made during the import process: created languages, modules and strings, and changed translations.",
        ea_guid="{A25B0422-4440-4420-A414-2448CAD303CC}",
        read_only="True",
        scale="0",
        custom_presentation_view="TRAImportacionCambios_CustomView",
        label="Informe de Cambios",
        length="0",
        containment="Not Specified",
        position="20",
        owner_class_name="TRAImportacion",
        exclude_from_views="[ 'Textual',  'General', ]"
    ),

    ComputedField(
        name='contenido',
        widget=ComputedWidget(
            label="Contenido Intercambio Traducciones",
            label2="Translations Interchange Contents",
            description="Contiene cadenas y traducciones contribuidas por un usuario, para su importacion.",
            description2="Contains strings and translations contributed by a user, and to be imported.",
            label_msgid='gvSIGi18n_TRAImportacion_contents_contenido_label',
            description_msgid='gvSIGi18n_TRAImportacion_contents_contenido_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=False,
        label2='Translations Interchange Contents',
        additional_columns=['excluirDeImportacion', 'nombreModulo'],
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

    StringField(
        name='estadoProceso',
        widget=SelectionWidget(
            label="Estado del Proceso",
            label2="Process State",
            description="El estado del proceso de importacion, como activo o inactivo.",
            description2="Import process state, as active or inactive.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_estadoProceso_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_estadoProceso_help',
            i18n_domain='gvSIGi18n',
        ),
        description="El estado del proceso de importacion, como activo o inactivo.",
        vocabulary=['Inactivo','Activo', ],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAImportacion_attr_estadoProceso_option_Inactivo', 'gvSIGi18n_TRAImportacion_attr_estadoProceso_option_Activo'],
        label2="Process State",
        ea_localid="335",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import process state, as active or inactive.",
        ea_guid="{7D22DE63-C551-4212-800E-F02B46E7339A}",
        vocabulary2=['Inactive', 'Active', ],
        read_only="True",
        scale="0",
        default="Inactivo",
        label="Estado del Proceso",
        length="0",
        containment="Not Specified",
        position="17",
        owner_class_name="TRAImportacion"
    ),

    DateTimeField(
        name='fechaComienzoProceso',
        widget=CalendarWidget(
            label="Fecha y Hora de Comienzo",
            label2="Startup Date and time",
            description="Fecha y hora en que se comenzo a ejecutar el proceso de importacion.",
            description2="Date and time when the import process started.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_fechaComienzoProceso_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_fechaComienzoProceso_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Fecha y hora en que se comenzo a ejecutar el proceso de importacion.",
        duplicates="0",
        label2="Startup Date and time",
        ea_localid="456",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Date and time when the import process started.",
        ea_guid="{8A5A12D1-B66F-4809-A665-67D935165DD7}",
        read_only="True",
        scale="0",
        label="Fecha y Hora de Comienzo",
        length="0",
        containment="Not Specified",
        position="22",
        owner_class_name="TRAImportacion"
    ),

    DateTimeField(
        name='fechaFinProceso',
        widget=CalendarWidget(
            label="Fecha y Hora de Fin",
            label2="End Date and Time",
            description="Fecha y hora en que termino el proceso de importacion.",
            description2="Date and Time when the import process terminated.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_fechaFinProceso_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_fechaFinProceso_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Fecha y hora en que termino el proceso de importacion.",
        duplicates="0",
        label2="End Date and Time",
        ea_localid="458",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Date and Time when the import process terminated.",
        ea_guid="{DD475E0E-7DB7-443f-86D0-2A0C9196C8CE}",
        read_only="True",
        scale="0",
        label="Fecha y Hora de Fin",
        length="0",
        containment="Not Specified",
        position="24",
        owner_class_name="TRAImportacion"
    ),

    DateTimeField(
        name='fechaUltimoInformeProgreso',
        widget=CalendarWidget(
            label="Fecha y Hora del ultimo informe de Progreso",
            label2="Last Progress report Date and time",
            description="Fecha y hora en que se refreco al ultimo informe de progreso.",
            description2="Date and time when last progress report was updated.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_fechaUltimoInformeProgreso_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_fechaUltimoInformeProgreso_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Fecha y hora en que se refreco al ultimo informe de progreso.",
        duplicates="0",
        label2="Last Progress report Date and time",
        ea_localid="623",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Date and time when last progress report was updated.",
        ea_guid="{29206842-8FED-4bf3-AD8D-868FBA6FF99A}",
        read_only="True",
        scale="0",
        label="Fecha y Hora del ultimo informe de Progreso",
        length="0",
        containment="Not Specified",
        position="23",
        owner_class_name="TRAImportacion"
    ),

    BooleanField(
        name='haComenzado',
        widget=BooleanField._properties['widget'](
            label="Comenzo a ejecutar",
            label2="Begun execution",
            description="Si el proceso de importacion ha comenzado alguna vez a ejecutarse.",
            description2="Whether the import process has ever started to execute.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_haComenzado_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_haComenzado_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si el proceso de importacion ha comenzado alguna vez a ejecutarse.",
        duplicates="0",
        label2="Begun execution",
        ea_localid="344",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Whether the import process has ever started to execute.",
        ea_guid="{ECD12C48-78E8-4e32-B073-6DBDFFFF7378}",
        read_only="True",
        scale="0",
        default="False",
        label="Comenzo a ejecutar",
        length="0",
        containment="Not Specified",
        position="18",
        owner_class_name="TRAImportacion"
    ),

    BooleanField(
        name='haCompletadoConExito',
        widget=BooleanField._properties['widget'](
            label="Exito?",
            label2="Success?",
            description="Si el proceso de importacion ha completado exitosamente su ejecucion.",
            description2="Whether the import process has sucessfully completed execution.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_haCompletadoConExito_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_haCompletadoConExito_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si el proceso de importacion ha completado exitosamente su ejecucion.",
        duplicates="0",
        label2="Success?",
        ea_localid="348",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Whether the import process has sucessfully completed execution.",
        ea_guid="{1F96CE35-9E56-470b-B5CC-E76AF9555F43}",
        read_only="True",
        scale="0",
        default="False",
        label="Exito?",
        length="0",
        containment="Not Specified",
        position="20",
        owner_class_name="TRAImportacion"
    ),

    ComputedField(
        name='informeContenidosImportacion',
        widget=ComputedField._properties['widget'](
            label="Contenidos Importacion",
            label2="Import contents",
            description="Informe de lenguajes, cadenas y traducciones en los archivos de intercambio de traducciones.",
            description2="Report with languages, strings and translations in the translations interchange archives.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_informeContenidosImportacion_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_informeContenidosImportacion_help',
            i18n_domain='gvSIGi18n',
        ),
        custom_presentation_view="TRAInformeContenidosImportacion_CustomView",
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
        containment="Not Specified",
        position="27",
        owner_class_name="TRAImportacion",
        exclude_from_views="[ 'Textual', 'Tabular', ]",
        computed_types="text"
    ),

    TextField(
        name='informeProgreso',
        widget=TextAreaWidget(
            label="Informe de Progreso",
            label2="Progress report",
            description="Cuando el proceso de importacion se esta ejecutando, informa del progreso alcanzado.",
            description2="When the import process is executing, reports the progress made.",
            label_msgid='gvSIGi18n_TRAImportacion_attr_informeProgreso_label',
            description_msgid='gvSIGi18n_TRAImportacion_attr_informeProgreso_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Cuando el proceso de importacion se esta ejecutando, informa del progreso alcanzado.",
        duplicates="0",
        label2="Progress report",
        ea_localid="343",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="When the import process is executing, reports the progress made.",
        ea_guid="{01E91E85-97F0-4884-B54C-DC891B95C088}",
        read_only="True",
        scale="0",
        exclude_from_views="[ 'Textual',  'General', ]",
        label="Informe de Progreso",
        length="0",
        containment="Not Specified",
        position="19",
        owner_class_name="TRAImportacion",
        custom_presentation_view="TRAImportacionProgreso_CustomView"
    ),

    ComputedField(
        name='informesEstado',
        widget=ComputedWidget(
            label="Informes Estado Antes y Despues",
            label2="Status Reports Before and After",
            description="Informes del Estado del Catalogo, sus Idiomas, Modulos, Cadenas y Traducciones, al comenzar el proceso de importacion, y tras terminar el proceso de importacion.",
            description2="Catalog Status Reports, its Languages, Modules, Strings and Translations, at the beginning of the import process, and after termination of the process.",
            label_msgid='gvSIGi18n_TRAImportacion_contents_informesEstado_label',
            description_msgid='gvSIGi18n_TRAImportacion_contents_informesEstado_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=False,
        label2='Status Reports Before and After',
        additional_columns=['haCompletadoConExito'],
        label='Informes Estado Antes y Despues',
        represents_aggregation=True,
        description2='Catalog Status Reports, its Languages, Modules, Strings and Translations, at the beginning of the import process, and after termination of the process.',
        multiValued=1,
        owner_class_name="TRAImportacion",
        expression="context.objectValues(['TRAInforme'])",
        computed_types=['TRAInforme'],
        non_framework_elements=False,
        description='Informes del Estado del Catalogo, sus Idiomas, Modulos, Cadenas y Traducciones, al comenzar el proceso de importacion, y tras terminar el proceso de importacion.'
    ),

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
        containment="Not Specified",
        position="21",
        owner_class_name="TRAImportacion"
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



    allowed_content_types = ['TRAInforme', 'TRAContenidoIntercambio'] + list(getattr(TRAArquetipo, 'allowed_content_types', [])) + list(getattr(TRAImportacion_Operaciones, 'allowed_content_types', [])) + list(getattr(TRAConRegistroActividad, 'allowed_content_types', []))
    filter_content_types             = 1
    global_allow                     = 0
    content_icon = 'traimportacion.gif'
    immediate_view                   = 'Tabular'
    default_view                     = 'Tabular'
    suppl_views                      = ['Tabular',]
    typeDescription                  = "Instancia de Proceso de Importacion, a partir de un fichero de entrada."
    typeDescMsgId                    =  'gvSIGi18n_TRAImportacion_help'
    archetype_name2                  = 'Import process'
    typeDescription2                 = '''Import process instance, from a given input archive.'''
    archetype_name_msgid             = 'gvSIGi18n_TRAImportacion_label'
    factory_methods                  = { 'TRAContenidoIntercambio' : 'fCrearContenidoIntercambio',}
    factory_enablers                 = { 'TRAContenidoIntercambio' : [ 'fUseCaseCheckDoableFactory', 'Create_TRAContenidoIntercambio',]}
    propagate_delete_impact_to       = None
    allow_discussion = False


    actions =  (


       {'action': "string:${object_url}/Tabular",
        'category': "object",
        'id': 'view',
        'name': 'View',
        'permissions': ("View",),
        'condition': """python:1"""
       },


       {'action': "string:$object_url/Editar",
        'category': "object",
        'id': 'edit',
        'name': 'Edit',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fAllowWrite() and object.fRoleQuery_IsManagerOrCoordinator()"""
       },


       {'action': "string:${object_url}/TRAImportar",
        'category': "object_buttons",
        'id': 'TRAImport',
        'name': 'Import',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fUseCaseCheckDoable( 'Import_TRAImportacion')  and object.fNoHaComenzadoOEnDevelopmentODebug()"""
       },


       {'action': "string:${object_url}/TRAReutilizar_action",
        'category': "object_buttons",
        'id': 'TRAReuse',
        'name': 'Reuse',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fUseCaseCheckDoable( 'Reuse_TRAImportacion') and object.getHaComenzado()"""
       },


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


       {'action': "string:${object_url}/TRAImportacionCambios",
        'category': "object",
        'id': 'TRAInformeCambios',
        'name': 'Changes during Import',
        'permissions': ("View",),
        'condition': """python:object.fRoleQuery_IsManagerOrCoordinator()"""
       },


       {'action': "string:${object_url}/TRAImportacionProgreso",
        'category': "object",
        'id': 'TRAInformeProgreso',
        'name': 'Progress',
        'permissions': ("View",),
        'condition': """python:object.fRoleQuery_IsManagerOrCoordinator()"""
       },


       {'action': "string:${object_url}/sharing",
        'category': "object",
        'id': 'local_roles',
        'name': 'Sharing',
        'permissions': ("Manage properties",),
        'condition': """python:0"""
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

    schema = TRAImportacion_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('cb_isCopyable')
    def cb_isCopyable(self):
        """
        """
        
        return True

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
        
        return self.pHandle_manage_pasteObjects( cb_copy_data, REQUEST)

    security.declarePublic('manage_afterAdd')
    def manage_afterAdd(self,item,container):
        """
        """
        
        return TRAImportacion_Operaciones.pHandle_manage_afterAdd( self, item, container)

    security.declarePublic('fExtraLinks')
    def fExtraLinks(self):
        """
        """
        
        return TRAImportacion_Operaciones.fExtraLinks( self)
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



