# -*- coding: utf-8 -*-
#
# File: TRAProgreso.py
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
from TRAProgreso_Operaciones import TRAProgreso_Operaciones
from Products.gvSIGi18n.TRAConRegistroActividad import TRAConRegistroActividad
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from TRAElemento_Operaciones import TRAElemento_Operaciones

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    #Inactivo
    StringField(
        name='tipoProceso',
        widget=SelectionWidget(
            label="Tipo del Proceso",
            label2="Process Type",
            description="""Inactivo
            El tipo del proceso del cual este elemento mantiene su progreso.""",
            description2="Type of the process whose progress is maintained by this element.",
            label_msgid='gvSIGi18n_TRAProgreso_attr_tipoProceso_label',
            description_msgid='gvSIGi18n_TRAProgreso_attr_tipoProceso_help',
            i18n_domain='gvSIGi18n',
        ),
        description="""Inactivo
        El tipo del proceso del cual este elemento mantiene su progreso.""",
        vocabulary=['Vacio','Inventario','Re-Catalogar','Re-Establecer Permisos','Eliminar Modulo', 'Eliminar Idioima','Copia Seguridad',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAProgreso_attr_tipoProceso_option_Vacio', 'gvSIGi18n_TRAProgreso_attr_tipoProceso_option_Inventario', 'gvSIGi18n_TRAProgreso_attr_tipoProceso_option_Re-Catalogar', 'gvSIGi18n_TRAProgreso_attr_tipoProceso_option_Re-Establecer Permisos', 'gvSIGi18n_TRAProgreso_attr_tipoProceso_option_Eliminar Modulo', 'gvSIGi18n_TRAProgreso_attr_tipoProceso_option_Eliminar Idioima', 'gvSIGi18n_TRAProgreso_attr_tipoProceso_option_Copia Seguridad'],
        label2="Process Type",
        ea_localid="1665",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Type of the process whose progress is maintained by this element.",
        ea_guid="{9CD241D5-3AB9-4c21-A108-00E8610D46A5}",
        vocabulary2=['Empty','Inventory','Re-Catalog','Reset Permissions','Delete Module','Delete Language','Export Backup',],
        read_only="True",
        scale="0",
        label="Tipo del Proceso",
        length="0",
        containment="Not Specified",
        position="18",
        owner_class_name="TRAProgreso"
    ),

    StringField(
        name='usuarioInformador',
        widget=StringWidget(
            label="Usuario Solicitante",
            label2="Requesting User",
            description="Usuario que ha solicitado creado el Informe.",
            description2="User who requested the ellaboration of the report.",
            label_msgid='gvSIGi18n_TRAProgreso_attr_usuarioInformador_label',
            description_msgid='gvSIGi18n_TRAProgreso_attr_usuarioInformador_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Usuario que ha solicitado creado el Informe.",
        duplicates="0",
        label2="Requesting User",
        ea_localid="1615",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="User who requested the ellaboration of the report.",
        ea_guid="{67F0AB35-6D4E-4a9a-A4D7-C3F95F5833A3}",
        read_only="True",
        scale="0",
        label="Usuario Solicitante",
        length="0",
        containment="Not Specified",
        position="19",
        owner_class_name="TRAProgreso"
    ),

    #Inactivo
    StringField(
        name='estadoProceso',
        widget=SelectionWidget(
            label="Estado del Proceso",
            label2="Process State",
            description="""Inactivo
            El estado del proceso de larga duracion, como activo o inactivo.""",
            description2="The state of the long-lived process, as active or inactive.",
            label_msgid='gvSIGi18n_TRAProgreso_attr_estadoProceso_label',
            description_msgid='gvSIGi18n_TRAProgreso_attr_estadoProceso_help',
            i18n_domain='gvSIGi18n',
        ),
        description="""Inactivo
        El estado del proceso de larga duracion, como activo o inactivo.""",
        vocabulary=['Inactivo','Activo', ],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAProgreso_attr_estadoProceso_option_Inactivo', 'gvSIGi18n_TRAProgreso_attr_estadoProceso_option_Activo'],
        label2="Process State",
        ea_localid="1609",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="The state of the long-lived process, as active or inactive.",
        ea_guid="{7456EDD4-9B3C-4f8c-96DB-BF424E2D26F0}",
        vocabulary2=['Inactive', 'Active', ],
        read_only="True",
        scale="0",
        label="Estado del Proceso",
        length="0",
        containment="Not Specified",
        position="8",
        owner_class_name="TRAProgreso"
    ),

    BooleanField(
        name='haComenzado',
        widget=BooleanField._properties['widget'](
            label="Comenzo a ejecutar",
            label2="Begun execution",
            description="Si el proceso de larga duracion ha comenzado alguna vez a ejecutarse.",
            description2="Whether the long-lived process has ever started to execute.",
            label_msgid='gvSIGi18n_TRAProgreso_attr_haComenzado_label',
            description_msgid='gvSIGi18n_TRAProgreso_attr_haComenzado_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si el proceso de larga duracion ha comenzado alguna vez a ejecutarse.",
        duplicates="0",
        label2="Begun execution",
        ea_localid="1613",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Whether the long-lived process has ever started to execute.",
        ea_guid="{2D2648F3-91C5-44f2-8378-AA66D8E8B0F3}",
        read_only="True",
        scale="0",
        default="False",
        label="Comenzo a ejecutar",
        length="0",
        containment="Not Specified",
        position="12",
        owner_class_name="TRAProgreso"
    ),

    BooleanField(
        name='haCompletadoConExito',
        widget=BooleanField._properties['widget'](
            label="Exito?",
            label2="Success?",
            description="Si el proceso de larga duracion ha completado exitosamente su ejecucion.",
            description2="Whether the long-lived process has sucessfully completed execution.",
            label_msgid='gvSIGi18n_TRAProgreso_attr_haCompletadoConExito_label',
            description_msgid='gvSIGi18n_TRAProgreso_attr_haCompletadoConExito_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si el proceso de larga duracion ha completado exitosamente su ejecucion.",
        duplicates="0",
        label2="Success?",
        ea_localid="1616",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Whether the long-lived process has sucessfully completed execution.",
        ea_guid="{76347E4D-0729-44da-8C71-7A289241AB5D}",
        read_only="True",
        scale="0",
        default="False",
        label="Exito?",
        length="0",
        containment="Not Specified",
        position="13",
        owner_class_name="TRAProgreso"
    ),

    DateTimeField(
        name='fechaComienzoProceso',
        widget=CalendarWidget(
            label="Fecha y Hora de Comienzo",
            label2="Startup Date and time",
            description="Fecha y hora en que se comenzo el proceso de larga duracion.",
            description2="Date and time when the long-lived process started.",
            label_msgid='gvSIGi18n_TRAProgreso_attr_fechaComienzoProceso_label',
            description_msgid='gvSIGi18n_TRAProgreso_attr_fechaComienzoProceso_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Fecha y hora en que se comenzo el proceso de larga duracion.",
        duplicates="0",
        label2="Startup Date and time",
        ea_localid="1611",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Date and time when the long-lived process started.",
        ea_guid="{6B14F15E-4BAD-4557-A77C-4D089435CB9B}",
        read_only="True",
        scale="0",
        label="Fecha y Hora de Comienzo",
        length="0",
        containment="Not Specified",
        position="9",
        owner_class_name="TRAProgreso"
    ),

    DateTimeField(
        name='fechaFinProceso',
        widget=CalendarWidget(
            label="Fecha y Hora de Fin",
            label2="End Date and Time",
            description="Fecha y hora en que termino el proceso de larga duracion.",
            description2="Date and Time when the long-lived process was terminated.",
            label_msgid='gvSIGi18n_TRAProgreso_attr_fechaFinProceso_label',
            description_msgid='gvSIGi18n_TRAProgreso_attr_fechaFinProceso_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Fecha y hora en que termino el proceso de larga duracion.",
        duplicates="0",
        label2="End Date and Time",
        ea_localid="1612",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Date and Time when the long-lived process was terminated.",
        ea_guid="{04E9DB04-3E60-4ac4-B8A2-2AF94F14C342}",
        read_only="True",
        scale="0",
        label="Fecha y Hora de Fin",
        length="0",
        containment="Not Specified",
        position="10",
        owner_class_name="TRAProgreso"
    ),

    StringField(
        name='tipoElementoProceso',
        widget=StringWidget(
            label="Tipo del elemento que especifica el Proceso",
            label2="Process specification element Type",
            description="Tipo del elemento que especifica el proceso a ejecutar (por ejemplo, Importacion).",
            description2="Type of the element specifying the process to execute (for example, Import).",
            label_msgid='gvSIGi18n_TRAProgreso_attr_tipoElementoProceso_label',
            description_msgid='gvSIGi18n_TRAProgreso_attr_tipoElementoProceso_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Tipo del elemento que especifica el proceso a ejecutar (por ejemplo, Importacion).",
        duplicates="0",
        label2="Process specification element Type",
        ea_localid="1707",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Type of the element specifying the process to execute (for example, Import).",
        ea_guid="{330815DA-5205-4171-92BA-5519B03B9745}",
        read_only="True",
        scale="0",
        label="Tipo del elemento que especifica el Proceso",
        length="0",
        containment="Not Specified",
        position="11",
        owner_class_name="TRAProgreso"
    ),

    StringField(
        name='identificadorElementoProceso',
        widget=StringWidget(
            label="Identificador del elemento que especifica el Proceso",
            label2="Process specification element Identifier",
            description="Identificador del elemento que especifica el proceso a ejecutar (por ejemplo, una Importacion).",
            description2="Identifier of the element specifying the process to execute (for example, an Import).",
            label_msgid='gvSIGi18n_TRAProgreso_attr_identificadorElementoProceso_label',
            description_msgid='gvSIGi18n_TRAProgreso_attr_identificadorElementoProceso_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Identificador del elemento que especifica el proceso a ejecutar (por ejemplo, una Importacion).",
        duplicates="0",
        label2="Process specification element Identifier",
        ea_localid="1706",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Identifier of the element specifying the process to execute (for example, an Import).",
        ea_guid="{7CF036A3-FA00-4d0a-BF35-345D1DA6A45F}",
        read_only="True",
        scale="0",
        label="Identificador del elemento que especifica el Proceso",
        length="0",
        containment="Not Specified",
        position="14",
        owner_class_name="TRAProgreso"
    ),

    ComputedField(
        name='elementoEspecificacionProceso',
        widget=ReferenceBrowserWidget(
            label="Elemento que especifica el Proceso (solo para Importaciones)",
            label2="Process specification element (only for Imports)",
            description="Elemento que especifica el proceso a ejecutar (por ejemplo, una Importacion).",
            description2="Element specifying the process to execute (for example, an Import).",
            label_msgid='gvSIGi18n_TRAProgreso_attr_elementoEspecificacionProceso_label',
            description_msgid='gvSIGi18n_TRAProgreso_attr_elementoEspecificacionProceso_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Elemento que especifica el proceso a ejecutar (por ejemplo, una Importacion).",
        duplicates="0",
        label2="Process specification element (only for Imports)",
        ea_localid="1709",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Element specifying the process to execute (for example, an Import).",
        ea_guid="{BC6DA151-500D-4954-ACE8-A3C897B24C28}",
        allowed_types=['TRAImportacion'],
        read_only="True",
        scale="0",
        additional_columns=['estadoProceso', 'haCompletadoConExito'],
        label="Elemento que especifica el Proceso (solo para Importaciones)",
        length="0",
        multiValued=0,
        containment="Not Specified",
        position="33",
        owner_class_name="TRAProgreso",
        expression="context.fDeriveElementoEspecificacionProceso()",
        computed_types="['TRAImportacion', ]"
    ),

    StringField(
        name='clasesSoporte',
        widget=StringWidget(
            label="Clases de Soporte al Progreso",
            label2="Progress Support Kinds",
            description="Los servicios de gestion del progreso que se proporcional al proceso: persistencia, transaccionalidad, liberar procesador y registro.",
            description2="Services supplied to manage the progress of the process: persistency, transaction, processor yield and logging.",
            label_msgid='gvSIGi18n_TRAProgreso_attr_clasesSoporte_label',
            description_msgid='gvSIGi18n_TRAProgreso_attr_clasesSoporte_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Los servicios de gestion del progreso que se proporcional al proceso: persistencia, transaccionalidad, liberar procesador y registro.",
        duplicates="0",
        label2="Progress Support Kinds",
        ea_localid="1667",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Services supplied to manage the progress of the process: persistency, transaction, processor yield and logging.",
        ea_guid="{12CBF653-DCDB-4434-8227-AD9F351A8561}",
        read_only="True",
        scale="0",
        label="Clases de Soporte al Progreso",
        length="0",
        containment="Not Specified",
        position="0",
        owner_class_name="TRAProgreso"
    ),

    StringField(
        name='comienzoTipo',
        widget=StringWidget(
            label="Tipo del elemento de comienzo",
            label2="Start element Type",
            description="Tipo del elemento en que se comienza el proceso cuyo progreso se gestiona.",
            description2="Type of the element where starts the process whose progress is managed here.",
            label_msgid='gvSIGi18n_TRAProgreso_attr_comienzoTipo_label',
            description_msgid='gvSIGi18n_TRAProgreso_attr_comienzoTipo_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Tipo del elemento en que se comienza el proceso cuyo progreso se gestiona.",
        duplicates="0",
        label2="Start element Type",
        ea_localid="1702",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Type of the element where starts the process whose progress is managed here.",
        ea_guid="{49CF4C61-3F96-4c51-BA6B-3CFEB094F527}",
        read_only="True",
        scale="0",
        label="Tipo del elemento de comienzo",
        length="0",
        containment="Not Specified",
        position="2",
        owner_class_name="TRAProgreso"
    ),

    StringField(
        name='comienzoTitulo',
        widget=StringWidget(
            label="Titulo del elemento de comienzo",
            label2="Start element Title",
            description="Titulo del elemento en que se comienza el proceso cuyo progreso se gestiona.",
            description2="Title of the element where starts the process whose progress is managed here.",
            label_msgid='gvSIGi18n_TRAProgreso_attr_comienzoTitulo_label',
            description_msgid='gvSIGi18n_TRAProgreso_attr_comienzoTitulo_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Titulo del elemento en que se comienza el proceso cuyo progreso se gestiona.",
        duplicates="0",
        label2="Start element Title",
        ea_localid="1700",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Title of the element where starts the process whose progress is managed here.",
        ea_guid="{9D3FA3BF-15B6-4e9c-9ED0-5FE8CBF8D3A8}",
        read_only="True",
        scale="0",
        label="Titulo del elemento de comienzo",
        length="0",
        containment="Not Specified",
        position="3",
        owner_class_name="TRAProgreso"
    ),

    StringField(
        name='comienzoUID',
        widget=StringWidget(
            label="UID del elemento de comienzo",
            label2="Start element UID",
            description="Identificador unico interno del elemento en que se comienza el proceso cuyo progreso se gestiona.",
            description2="Internal unique identifier of the element where starts the process whose progress is managed here.",
            label_msgid='gvSIGi18n_TRAProgreso_attr_comienzoUID_label',
            description_msgid='gvSIGi18n_TRAProgreso_attr_comienzoUID_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Identificador unico interno del elemento en que se comienza el proceso cuyo progreso se gestiona.",
        duplicates="0",
        label2="Start element UID",
        ea_localid="1668",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Internal unique identifier of the element where starts the process whose progress is managed here.",
        ea_guid="{C05A183E-928F-4fbc-9884-AC4079F7CAA4}",
        read_only="True",
        scale="0",
        label="UID del elemento de comienzo",
        length="0",
        containment="Not Specified",
        position="4",
        owner_class_name="TRAProgreso"
    ),

    ComputedField(
        name='estadoControl',
        widget=ComputedField._properties['widget'](
            label="Estado de Control del Progreso",
            label2="Progress Control Status",
            description="Resume el estado del control del progreso, del proceso de larga duracion.",
            description2="Summary of the state of progress control for this long-lived process.",
            label_msgid='gvSIGi18n_TRAProgreso_attr_estadoControl_label',
            description_msgid='gvSIGi18n_TRAProgreso_attr_estadoControl_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Resume el estado del control del progreso, del proceso de larga duracion.",
        duplicates="0",
        label2="Progress Control Status",
        ea_localid="1704",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Summary of the state of progress control for this long-lived process.",
        ea_guid="{AC04D72D-F9A0-4266-80BA-F82E2E831639}",
        read_only="True",
        scale="0",
        exclude_from_views="[ 'Tabular', 'Textual',  'General', ]",
        label="Estado de Control del Progreso",
        length="0",
        expression="context.fEstadoControl()",
        containment="Not Specified",
        position="7",
        owner_class_name="TRAProgreso",
        custom_presentation_view="TRAProgreso_EstadoControl_CustomView",
        computed_types="object"
    ),

    TextField(
        name='parametrosEntrada',
        widget=TextAreaWidget(
            label="Parametros de Entrada",
            label2="Input Parameters",
            description="Almacena los parametros que guian el proceso de larga duracion.",
            description2="Stores the parameters driving the long-lived process.",
            label_msgid='gvSIGi18n_TRAProgreso_attr_parametrosEntrada_label',
            description_msgid='gvSIGi18n_TRAProgreso_attr_parametrosEntrada_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Almacena los parametros que guian el proceso de larga duracion.",
        duplicates="0",
        label2="Input Parameters",
        ea_localid="1666",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Stores the parameters driving the long-lived process.",
        ea_guid="{B328BCCA-4947-4663-BDE1-ECE0AB1C2D10}",
        read_only="True",
        scale="0",
        custom_presentation_view="TRAProgreso_ParametrosEntrada_CustomView",
        label="Parametros de Entrada",
        length="0",
        containment="Not Specified",
        position="17",
        owner_class_name="TRAProgreso",
        exclude_from_views="[ 'Tabular','Textual',  'General', ]"
    ),

    TextField(
        name='parametrosControl',
        widget=TextAreaWidget(
            label="Parametros de Control",
            label2="Control Parameters",
            description="Almacena los parametros que controlan la gestion del proceso de larga duracion.",
            description2="Stores the parameters controlling the management of the progress of the long-lived process.",
            label_msgid='gvSIGi18n_TRAProgreso_attr_parametrosControl_label',
            description_msgid='gvSIGi18n_TRAProgreso_attr_parametrosControl_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Almacena los parametros que controlan la gestion del proceso de larga duracion.",
        duplicates="0",
        label2="Control Parameters",
        ea_localid="1699",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Stores the parameters controlling the management of the progress of the long-lived process.",
        ea_guid="{E633BBFB-E5EB-4ee4-BCCE-79C043F6F4A8}",
        read_only="True",
        scale="0",
        exclude_from_views="['Tabular', 'Textual',  'General', ]",
        label="Parametros de Control",
        length="0",
        containment="Not Specified",
        position="16",
        owner_class_name="TRAProgreso",
        custom_presentation_view="TRAProgreso_ParametrosControl_CustomView"
    ),

    TextField(
        name='contadoresControl',
        widget=TextAreaWidget(
            label="Contadores de Control",
            label2="Control Counters",
            description="Almacena los contadores que controlan la gestion del proceso de larga duracion.",
            description2="Stores the counters controlling the management of the progress of the long-lived process.",
            label_msgid='gvSIGi18n_TRAProgreso_attr_contadoresControl_label',
            description_msgid='gvSIGi18n_TRAProgreso_attr_contadoresControl_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Almacena los contadores que controlan la gestion del proceso de larga duracion.",
        duplicates="0",
        label2="Control Counters",
        ea_localid="1703",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Stores the counters controlling the management of the progress of the long-lived process.",
        ea_guid="{755CFE75-EACD-40d7-8EC2-143A2A57761B}",
        read_only="True",
        scale="0",
        exclude_from_views="['Tabular', 'Textual',  'General', ]",
        label="Contadores de Control",
        length="0",
        containment="Not Specified",
        position="5",
        owner_class_name="TRAProgreso",
        custom_presentation_view="TRAProgreso_ContadoresControl_CustomView"
    ),

    TextField(
        name='datosResultado',
        widget=TextAreaWidget(
            label="Datos Resultado",
            label2="Result Data",
            description="Almacena los datos resultantes del proceso de larga duracion.",
            description2="Stores the data resulting from the long-lived process.",
            label_msgid='gvSIGi18n_TRAProgreso_attr_datosResultado_label',
            description_msgid='gvSIGi18n_TRAProgreso_attr_datosResultado_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Almacena los datos resultantes del proceso de larga duracion.",
        duplicates="0",
        label2="Result Data",
        ea_localid="1664",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Stores the data resulting from the long-lived process.",
        ea_guid="{AAD72C9B-C9E8-44f6-BDDB-2294A3F3D6E6}",
        read_only="True",
        scale="0",
        exclude_from_views="['Tabular', 'Textual',  'General', ]",
        label="Datos Resultado",
        length="0",
        containment="Not Specified",
        position="6",
        owner_class_name="TRAProgreso",
        custom_presentation_view="TRAProgreso_DatosResultado_CustomView"
    ),

    TextField(
        name='informeExcepcion',
        widget=TextAreaWidget(
            label="Excepcion",
            label2="Exception",
            description="Cuando la ejecucion del proceso de larga duracion finaliza con una condicion de error, contiene el informe del error de la aplicacion.",
            description2="When the long-lived process terminates with an error, contains the applicacion exception report.",
            label_msgid='gvSIGi18n_TRAProgreso_attr_informeExcepcion_label',
            description_msgid='gvSIGi18n_TRAProgreso_attr_informeExcepcion_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Cuando la ejecucion del proceso de larga duracion finaliza con una condicion de error, contiene el informe del error de la aplicacion.",
        duplicates="0",
        label2="Exception",
        ea_localid="1610",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="When the long-lived process terminates with an error, contains the applicacion exception report.",
        ea_guid="{7B3969F8-E276-42c6-9763-333D87F1275C}",
        read_only="True",
        scale="0",
        label="Excepcion",
        length="0",
        containment="Not Specified",
        position="15",
        owner_class_name="TRAProgreso"
    ),

    StringField(
        name='comienzoRuta',
        widget=StringWidget(
            label="Ruta del elemento de comienzo",
            label2="Start element Path",
            description="Ruta de acceso al elemento en que se comienza el proceso cuyo progreso se gestiona.",
            description2="Path to  the element where starts the process whose progress is managed here.",
            label_msgid='gvSIGi18n_TRAProgreso_attr_comienzoRuta_label',
            description_msgid='gvSIGi18n_TRAProgreso_attr_comienzoRuta_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Ruta de acceso al elemento en que se comienza el proceso cuyo progreso se gestiona.",
        duplicates="0",
        label2="Start element Path",
        ea_localid="1701",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Path to  the element where starts the process whose progress is managed here.",
        ea_guid="{349C6A3F-16ED-483b-BF87-AF5FD099EAE8}",
        read_only="True",
        scale="0",
        label="Ruta del elemento de comienzo",
        length="0",
        containment="Not Specified",
        position="1",
        owner_class_name="TRAProgreso"
    ),

    DateTimeField(
        name='fechaUltimoInformeProgreso',
        widget=CalendarWidget(
            label="Fecha y Hora del ultimo informe de Progreso",
            label2="Last Progress report Date and time",
            description="Fecha y hora en que se refresco al ultimo informe de progreso.",
            description2="Date and time when last progress report was updated.",
            label_msgid='gvSIGi18n_TRAProgreso_attr_fechaUltimoInformeProgreso_label',
            description_msgid='gvSIGi18n_TRAProgreso_attr_fechaUltimoInformeProgreso_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Fecha y hora en que se refresco al ultimo informe de progreso.",
        duplicates="0",
        label2="Last Progress report Date and time",
        ea_localid="1647",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Date and time when last progress report was updated.",
        ea_guid="{DD0FCF89-DFF0-488b-9611-F4A43FD48181}",
        read_only="True",
        scale="0",
        label="Fecha y Hora del ultimo informe de Progreso",
        length="0",
        containment="Not Specified",
        position="11",
        owner_class_name="TRAProgreso"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAProgreso_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAArquetipo, 'schema', Schema(())).copy() + \
    getattr(TRAProgreso_Operaciones, 'schema', Schema(())).copy() + \
    getattr(TRAConRegistroActividad, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAProgreso(OrderedBaseFolder, TRAArquetipo, TRAProgreso_Operaciones, TRAConRegistroActividad):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAArquetipo,'__implements__',()),) + (getattr(TRAProgreso_Operaciones,'__implements__',()),) + (getattr(TRAConRegistroActividad,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Progreso'

    meta_type = 'TRAProgreso'
    portal_type = 'TRAProgreso'


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

    allowed_content_types = [] + list(getattr(TRAArquetipo, 'allowed_content_types', [])) + list(getattr(TRAProgreso_Operaciones, 'allowed_content_types', [])) + list(getattr(TRAConRegistroActividad, 'allowed_content_types', []))
    filter_content_types             = 1
    global_allow                     = 0
    content_icon = 'traprogreso.gif'
    immediate_view                   = 'Tabular'
    default_view                     = 'Tabular'
    suppl_views                      = ['Tabular',]
    typeDescription                  = "Informe de Progreso acerca de un Proceso de larga duracion"
    typeDescMsgId                    =  'gvSIGi18n_TRAProgreso_help'
    archetype_name2                  = 'Progress'
    typeDescription2                 = '''Progress report about a long-lived process'''
    archetype_name_msgid             = 'gvSIGi18n_TRAProgreso_label'
    factory_methods                  = None
    factory_enablers                 = None
    propagate_delete_impact_to       = None
    allow_discussion = False


    actions =  (


       {'action': "string:${object_url}/TRAConfigureProgress_action",
        'category': "object",
        'id': 'TRAConfigureProgress',
        'name': 'Configure Progress',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fUseCaseCheckDoable( 'Configure_TRAProgreso') and object.fHasProgressHandler()"""
       },


       {'action': "string:${object_url}/TRAControlProgress_action",
        'category': "object",
        'id': 'TRAControlProgress',
        'name': 'Control Progress',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fUseCaseCheckDoable( 'Control_TRAProgreso') and object.fHasProgressHandler()"""
       },


       {'action': "string:$object_url/Editar",
        'category': "object",
        'id': 'edit',
        'name': 'Edit',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fAllowWrite()"""
       },


       {'action': "string:${object_url}/TRAProgressResults_action",
        'category': "object",
        'id': 'TRAProgressResults',
        'name': 'Progress Results',
        'permissions': ("View",),
        'condition': """python:1"""
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

    schema = TRAProgreso_schema

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
        
        return TRAProgreso_Operaciones.fExtraLinks( self)

    security.declarePublic('fIsCacheable')
    def fIsCacheable(self):
        """
        """
        
        return True

    security.declarePublic('manage_afterAdd')
    def manage_afterAdd(self,item,container):
        """
        """
        
        return TRAArquetipo.manage_afterAdd( self, item, container)

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
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata', 'sharing', 'folderContents']:
            a['visible'] = 0
    return fti

registerType(TRAProgreso, PROJECTNAME)
# end of class TRAProgreso

##code-section module-footer #fill in your manual code here
##/code-section module-footer



