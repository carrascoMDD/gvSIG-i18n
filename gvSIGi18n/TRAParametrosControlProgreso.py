# -*- coding: utf-8 -*-
#
# File: TRAParametrosControlProgreso.py
#
# Copyright (c) 2013 by 2008, 2009, 2010, 2011 Conselleria de Infraestructuras
# y Transporte de la Generalidad Valenciana
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
from TRAParametrosControlProgreso_Operaciones import TRAParametrosControlProgreso_Operaciones
from Products.gvSIGi18n.TRAConRegistroActividad import TRAConRegistroActividad
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from TRAElemento_Operaciones import TRAElemento_Operaciones
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='tipoProceso',
        widget=StringWidget(
            label="Tipo del Proceso",
            label2="Process Type",
            description="El tipo del proceso del cual este elemento mantiene los parametros iniciales de control de su progreso.",
            description2="Type of the process whose initial progress control parameters are maintained by this element.",
            label_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_tipoProceso_label',
            description_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_tipoProceso_help',
            i18n_domain='gvSIGi18n',
        ),
        description="El tipo del proceso del cual este elemento mantiene los parametros iniciales de control de su progreso.",
        searchable=0,
        duplicates="0",
        label2="Process Type",
        ea_localid="1720",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Type of the process whose initial progress control parameters are maintained by this element.",
        ea_guid="{F00ECEC8-547E-4162-A49D-894BEFFA10CE}",
        read_only="True",
        scale="0",
        label="Tipo del Proceso",
        length="0",
        containment="Not Specified",
        position="0",
        owner_class_name="TRAParametrosControlProgreso"
    ),

    BooleanField(
        name='crearInformeAntes',
        widget=BooleanField._properties['widget'](
            label="Crear Informe Antes",
            label2="Create Report Before",
            description="Cuendo sea verdadero, se creara un informe detallado de estado antes de ejecutar proceso.",
            description2="When true, a detailed status report shall be created before executing the process.",
            label_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_crearInformeAntes_label',
            description_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_crearInformeAntes_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Cuendo sea verdadero, se creara un informe detallado de estado antes de ejecutar proceso.",
        duplicates="0",
        label2="Create Report Before",
        ea_localid="1597",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="When true, a detailed status report shall be created before executing the process.",
        ea_guid="{4DED20F9-F187-48d5-A220-7EA18D0E0C6A}",
        scale="0",
        default="False",
        label="Crear Informe Antes",
        length="0",
        containment="Not Specified",
        position="1",
        owner_class_name="TRAParametrosControlProgreso"
    ),

    BooleanField(
        name='crearInformeDespues',
        widget=BooleanField._properties['widget'](
            label="Crear Informe Despues",
            label2="Create Report After",
            description="Cuendo sea verdadero, se creara un informe detallado de estado despues de ejecutar el proceso.",
            description2="When true, a detailed status report shall be created after executing the process.",
            label_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_crearInformeDespues_label',
            description_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_crearInformeDespues_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Cuendo sea verdadero, se creara un informe detallado de estado despues de ejecutar el proceso.",
        duplicates="0",
        label2="Create Report After",
        ea_localid="1598",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="When true, a detailed status report shall be created after executing the process.",
        ea_guid="{E3B22B84-2CB3-46d5-99DF-AD3B00CD02C2}",
        scale="0",
        default="False",
        label="Crear Informe Despues",
        length="0",
        containment="Not Specified",
        position="2",
        owner_class_name="TRAParametrosControlProgreso"
    ),

    BooleanField(
        name='guardarResultados_habilitado',
        widget=BooleanField._properties['widget'](
            label="Guardar Resultados Habilitado",
            label2="Store Results Enabled",
            description="Si Verdadero, entonces el sistema guardara resultados durante el control del progreso del proceso de larga duracion de este tipo.",
            description2="If True, then the system shall store results during the progress of long-lived processes of the type.",
            label_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_guardarResultados_habilitado_label',
            description_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_guardarResultados_habilitado_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, entonces el sistema guardara resultados durante el control del progreso del proceso de larga duracion de este tipo.",
        duplicates="0",
        label2="Store Results Enabled",
        ea_localid="1695",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="If True, then the system shall store results during the progress of long-lived processes of the type.",
        ea_guid="{945D1825-2387-4a40-A64A-4E82C9BEFE59}",
        scale="0",
        default="True",
        label="Guardar Resultados Habilitado",
        length="0",
        containment="Not Specified",
        position="8",
        owner_class_name="TRAParametrosControlProgreso"
    ),

    IntegerField(
        name='guardarResultados_maximoElementosLeidos',
        widget=IntegerField._properties['widget'](
            label="Guardar Resultados Maximo Elementos Leidos",
            label2="Store Results Max Traversed Elements",
            description="Para Guardar Resultados: cuando se lea este numero de elementos desde la ultima vez que se guardaron los resultados, el sistema guardara los resultados del proceso.",
            description2="For Logging: when this number of elements has been read since the process results were last stored, the system shall store the process results.",
            label_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_guardarResultados_maximoElementosLeidos_label',
            description_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_guardarResultados_maximoElementosLeidos_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Para Guardar Resultados: cuando se lea este numero de elementos desde la ultima vez que se guardaron los resultados, el sistema guardara los resultados del proceso.",
        duplicates="0",
        label2="Store Results Max Traversed Elements",
        ea_localid="1684",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="For Logging: when this number of elements has been read since the process results were last stored, the system shall store the process results.",
        ea_guid="{91A8B41F-6089-4aab-8F8A-C1F8F9D0432E}",
        scale="0",
        default="3000",
        label="Guardar Resultados Maximo Elementos Leidos",
        length="0",
        containment="Not Specified",
        position="9",
        owner_class_name="TRAParametrosControlProgreso"
    ),

    IntegerField(
        name='guardarResultados_maximoElementosModificados',
        widget=IntegerField._properties['widget'](
            label="Guardar Resultados Maximo Elementos Modificados",
            label2="Store Results Max Modified Elements",
            description="Para Guardar Resultados: cuando se modifique este numero de elementos desde la ultima vez que se guardaron los resultados, el sistema guardara los resultados del proceso.",
            description2="For Logging: when this number of elements has been modified since the process results were last stored, the system shall store the process results.",
            label_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_guardarResultados_maximoElementosModificados_label',
            description_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_guardarResultados_maximoElementosModificados_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Para Guardar Resultados: cuando se modifique este numero de elementos desde la ultima vez que se guardaron los resultados, el sistema guardara los resultados del proceso.",
        duplicates="0",
        label2="Store Results Max Modified Elements",
        ea_localid="1685",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="For Logging: when this number of elements has been modified since the process results were last stored, the system shall store the process results.",
        ea_guid="{90DE7552-6474-46f5-B826-C61BFED264ED}",
        scale="0",
        default="3000",
        label="Guardar Resultados Maximo Elementos Modificados",
        length="0",
        containment="Not Specified",
        position="10",
        owner_class_name="TRAParametrosControlProgreso"
    ),

    IntegerField(
        name='guardarResultados_maximoMilisegundos',
        widget=IntegerField._properties['widget'](
            label="Guardar Resultados Maximo Milisegundos",
            label2="Store Results Max Milliseconds",
            description="Para Guardar Resultados: cuando haya transcurrido este numero de milisegundos desde la ultima vez que se guardaron los resultados, el sistema guardara los resultados del proceso.",
            description2="For Logging: when this number of milliseconds has lapsed since the process results were last stored, the system shall store the process results.",
            label_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_guardarResultados_maximoMilisegundos_label',
            description_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_guardarResultados_maximoMilisegundos_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Para Guardar Resultados: cuando haya transcurrido este numero de milisegundos desde la ultima vez que se guardaron los resultados, el sistema guardara los resultados del proceso.",
        duplicates="0",
        label2="Store Results Max Milliseconds",
        ea_localid="1686",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="For Logging: when this number of milliseconds has lapsed since the process results were last stored, the system shall store the process results.",
        ea_guid="{4EA6DABF-6D4A-4b08-947E-0614B90C7185}",
        scale="0",
        default="5000",
        label="Guardar Resultados Maximo Milisegundos",
        length="0",
        containment="Not Specified",
        position="11",
        owner_class_name="TRAParametrosControlProgreso"
    ),

    BooleanField(
        name='transacciones_habilitado',
        widget=BooleanField._properties['widget'](
            label="Transacciones Habilitado",
            label2="Transactions Enabled",
            description="Si Verdadero, entonces el sistema creara transacciones durante el control del progreso del proceso de larga duracion de este tipo.",
            description2="If True, then the system shall create transactions during the progress of long-lived processes of the type.",
            label_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_transacciones_habilitado_label',
            description_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_transacciones_habilitado_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, entonces el sistema creara transacciones durante el control del progreso del proceso de larga duracion de este tipo.",
        duplicates="0",
        label2="Transactions Enabled",
        ea_localid="1697",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="If True, then the system shall create transactions during the progress of long-lived processes of the type.",
        ea_guid="{DB2FC7B2-15C9-4061-95ED-148DAAE1AFF4}",
        scale="0",
        default="True",
        label="Transacciones Habilitado",
        length="0",
        containment="Not Specified",
        position="18",
        owner_class_name="TRAParametrosControlProgreso"
    ),

    IntegerField(
        name='transacciones_maximoElementosLeidos',
        widget=IntegerField._properties['widget'](
            label="Transacciones Maximo Elementos Leidos",
            label2="Transactions Max Traversed Elements",
            description="Para Transacciones: cuando se lea este numero de elementos desde la ultima transaccion, el sistema creara una nueva transaccion.",
            description2="For Transactions: when this number of elements has been read since the last transaction, the system shall create a new transacion.",
            label_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_transacciones_maximoElementosLeidos_label',
            description_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_transacciones_maximoElementosLeidos_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Para Transacciones: cuando se lea este numero de elementos desde la ultima transaccion, el sistema creara una nueva transaccion.",
        duplicates="0",
        label2="Transactions Max Traversed Elements",
        ea_localid="1690",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="For Transactions: when this number of elements has been read since the last transaction, the system shall create a new transacion.",
        ea_guid="{7544156B-6191-43bc-AD11-D65ACB0148F6}",
        scale="0",
        default="3000",
        label="Transacciones Maximo Elementos Leidos",
        length="0",
        containment="Not Specified",
        position="18",
        owner_class_name="TRAParametrosControlProgreso"
    ),

    IntegerField(
        name='transacciones_maximoElementosModificados',
        widget=IntegerField._properties['widget'](
            label="Transacciones Maximo Elementos Modificados",
            label2="Transactions Max Modified Elements",
            description="Para Transacciones: cuando se modifique este numero de elementos desde la ultima transaccion, el sistema creara una nueva transaccion.",
            description2="For Transactions: when this number of elements has been modified since the last transaction, the system shall create a new transacion.",
            label_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_transacciones_maximoElementosModificados_label',
            description_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_transacciones_maximoElementosModificados_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Para Transacciones: cuando se modifique este numero de elementos desde la ultima transaccion, el sistema creara una nueva transaccion.",
        duplicates="0",
        label2="Transactions Max Modified Elements",
        ea_localid="1691",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="For Transactions: when this number of elements has been modified since the last transaction, the system shall create a new transacion.",
        ea_guid="{CAE2513D-F10F-4886-89F5-C5D77894E9F0}",
        scale="0",
        default="3000",
        label="Transacciones Maximo Elementos Modificados",
        length="0",
        containment="Not Specified",
        position="19",
        owner_class_name="TRAParametrosControlProgreso"
    ),

    IntegerField(
        name='transacciones_maximoMilisegundos',
        widget=IntegerField._properties['widget'](
            label="Transacciones Maximo Milisegundos",
            label2="Transactions Max Milliseconds",
            description="Para Transacciones: cuando haya transcurrido este numero de milisegundos desde la ultima transaccion, el sistema creara una nueva transaccion.",
            description2="For Transactions: when this number of milliseconds has lapsed since the last transaction, the system shall create a new transacion.",
            label_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_transacciones_maximoMilisegundos_label',
            description_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_transacciones_maximoMilisegundos_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Para Transacciones: cuando haya transcurrido este numero de milisegundos desde la ultima transaccion, el sistema creara una nueva transaccion.",
        duplicates="0",
        label2="Transactions Max Milliseconds",
        ea_localid="1692",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="For Transactions: when this number of milliseconds has lapsed since the last transaction, the system shall create a new transacion.",
        ea_guid="{2E5FB8E1-1750-47b2-B30E-2BFC87E0A753}",
        scale="0",
        default="5000",
        label="Transacciones Maximo Milisegundos",
        length="0",
        containment="Not Specified",
        position="20",
        owner_class_name="TRAParametrosControlProgreso"
    ),

    BooleanField(
        name='registro_habilitado',
        widget=BooleanField._properties['widget'](
            label="Registro Habilitado",
            label2="Logging Enabled",
            description="Si Verdadero, entonces el sistema escribira entradas de registro durante el control del progreso del proceso de larga duracion de este tipo.",
            description2="If True, then the system shall write log entries during the progress of long-lived processes of the type.",
            label_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_registro_habilitado_label',
            description_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_registro_habilitado_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, entonces el sistema escribira entradas de registro durante el control del progreso del proceso de larga duracion de este tipo.",
        duplicates="0",
        label2="Logging Enabled",
        ea_localid="1696",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="If True, then the system shall write log entries during the progress of long-lived processes of the type.",
        ea_guid="{7D87F2E7-E660-4222-9EC3-6416C4255796}",
        scale="0",
        default="True",
        label="Registro Habilitado",
        length="0",
        containment="Not Specified",
        position="12",
        owner_class_name="TRAParametrosControlProgreso"
    ),

    IntegerField(
        name='registro_maximoElementosLeidos',
        widget=IntegerField._properties['widget'](
            label="Registro Maximo Elementos Leidos",
            label2="Logging Max Traversed Elements",
            description="Para Registro: cuando se lea este numero de elementos desde la ultima entrada de registro, el sistema escribira una nueva entrada en el registro (log)",
            description2="For Logging: when this number of elements has been read since last log entry, the system shall write a new log entry.",
            label_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_registro_maximoElementosLeidos_label',
            description_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_registro_maximoElementosLeidos_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Para Registro: cuando se lea este numero de elementos desde la ultima entrada de registro, el sistema escribira una nueva entrada en el registro (log)",
        duplicates="0",
        label2="Logging Max Traversed Elements",
        ea_localid="1681",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="For Logging: when this number of elements has been read since last log entry, the system shall write a new log entry.",
        ea_guid="{2441543C-7002-44ee-AF83-938A50F44708}",
        scale="0",
        default="3000",
        label="Registro Maximo Elementos Leidos",
        length="0",
        containment="Not Specified",
        position="13",
        owner_class_name="TRAParametrosControlProgreso"
    ),

    IntegerField(
        name='registro_maximoElementosModificados',
        widget=IntegerField._properties['widget'](
            label="Registro Maximo Elementos Modificados",
            label2="Logging Max Modified Elements",
            description="Para Registro: cuando se modifique este numero de elementos desde la ultima entrada de registro, el sistema escribira una nueva entrada en el registro (log)",
            description2="For Logging: when this number of elements has been modified since last log entry, the system shall write a new log entry.",
            label_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_registro_maximoElementosModificados_label',
            description_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_registro_maximoElementosModificados_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Para Registro: cuando se modifique este numero de elementos desde la ultima entrada de registro, el sistema escribira una nueva entrada en el registro (log)",
        duplicates="0",
        label2="Logging Max Modified Elements",
        ea_localid="1682",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="For Logging: when this number of elements has been modified since last log entry, the system shall write a new log entry.",
        ea_guid="{1E7EFB08-D451-4539-B13D-5A0FB9C79EE9}",
        scale="0",
        default="3000",
        label="Registro Maximo Elementos Modificados",
        length="0",
        containment="Not Specified",
        position="14",
        owner_class_name="TRAParametrosControlProgreso"
    ),

    IntegerField(
        name='registro_maximoMilisegundos',
        widget=IntegerField._properties['widget'](
            label="Registro Maximo Milisegundos",
            label2="Logging Max Milliseconds",
            description="Para Registro: cuando haya transcurrido este numero de milisegundos desde la ultima entrada de registro, el sistema escribira una nueva entrada en el registro (log)",
            description2="For Logging: when this number of milliseconds has lapsed since las log entry, the system shall write a new log entry.",
            label_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_registro_maximoMilisegundos_label',
            description_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_registro_maximoMilisegundos_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Para Registro: cuando haya transcurrido este numero de milisegundos desde la ultima entrada de registro, el sistema escribira una nueva entrada en el registro (log)",
        duplicates="0",
        label2="Logging Max Milliseconds",
        ea_localid="1680",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="For Logging: when this number of milliseconds has lapsed since las log entry, the system shall write a new log entry.",
        ea_guid="{57A22F05-3E44-477b-94FB-3BA78E998915}",
        scale="0",
        default="5000",
        label="Registro Maximo Milisegundos",
        length="0",
        containment="Not Specified",
        position="15",
        owner_class_name="TRAParametrosControlProgreso"
    ),

    IntegerField(
        name='registro_maximoTransacciones',
        widget=IntegerField._properties['widget'](
            label="Registro Maximo Transacciones",
            label2="Logging Max Transactions",
            description="Para Registro: cuando se hayan guardado este numero de transacciones desde la ultima entrada de registro, el sistema escribira una nueva entrada en el registro (log)",
            description2="For Logging: when this number of transactions have been committed since las log entry, the system shall write a new log entry.",
            label_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_registro_maximoTransacciones_label',
            description_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_registro_maximoTransacciones_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Para Registro: cuando se hayan guardado este numero de transacciones desde la ultima entrada de registro, el sistema escribira una nueva entrada en el registro (log)",
        duplicates="0",
        label2="Logging Max Transactions",
        ea_localid="1683",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="For Logging: when this number of transactions have been committed since las log entry, the system shall write a new log entry.",
        ea_guid="{EDDD4564-6803-4e1a-A8D3-9416C7169243}",
        scale="0",
        default="10",
        label="Registro Maximo Transacciones",
        length="0",
        containment="Not Specified",
        position="17",
        owner_class_name="TRAParametrosControlProgreso"
    ),

    BooleanField(
        name='cederProcesador_habilitado',
        widget=BooleanField._properties['widget'](
            label="Ceder Procesador Habilitado",
            label2="Yield Processor Enabled",
            description="Si Verdadero, entonces el sistema gestionara la cesion de procesador durante el control del progreso del proceso de larga duracion de este tipo.",
            description2="If True, then the system shall manage yielding the processor during the progress of long-lived processes of the type.",
            label_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_cederProcesador_habilitado_label',
            description_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_cederProcesador_habilitado_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, entonces el sistema gestionara la cesion de procesador durante el control del progreso del proceso de larga duracion de este tipo.",
        duplicates="0",
        label2="Yield Processor Enabled",
        ea_localid="1693",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="If True, then the system shall manage yielding the processor during the progress of long-lived processes of the type.",
        ea_guid="{C30BC469-AEFE-4ad4-B571-D03836E444C4}",
        scale="0",
        default="True",
        label="Ceder Procesador Habilitado",
        length="0",
        containment="Not Specified",
        position="3",
        owner_class_name="TRAParametrosControlProgreso"
    ),

    BooleanField(
        name='cederProcesador_soloEntreTransacciones',
        widget=BooleanField._properties['widget'](
            label="Solo entre Transaciones",
            label2="Only between Transactions",
            description="Si Verdadero, entonces el sistema solo cedera el procesador entre transacciones, si las transaciones estan habilitadas.",
            description2="If True, then the system shall yield the processor only between transactions, if transactions are enabled.",
            label_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_cederProcesador_soloEntreTransacciones_label',
            description_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_cederProcesador_soloEntreTransacciones_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, entonces el sistema solo cedera el procesador entre transacciones, si las transaciones estan habilitadas.",
        duplicates="0",
        label2="Only between Transactions",
        ea_localid="2078",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;IsLiteral=0;",
        description2="If True, then the system shall yield the processor only between transactions, if transactions are enabled.",
        ea_guid="{0435EF09-8907-40db-8CFC-FC7D5B672BDF}",
        scale="0",
        default="True",
        label="Solo entre Transaciones",
        length="0",
        containment="Not Specified",
        position="3",
        owner_class_name="TRAParametrosControlProgreso"
    ),

    IntegerField(
        name='cederProcesador_porcentajeTiempoActividad',
        widget=IntegerField._properties['widget'](
            label="Ceder Procesador Porcentaje Tiempo Actividad",
            label2="Yield Processor Activity Time Percentage",
            description="Para Ceder Procesador: el sistema limitara a este porcentaje el tiempo de actividad de este proceso, cediendo el procesador para que atienda otros procesos.",
            description2="For Yield Processor: the system shall limit the activity of processes of this kind, to this percentage of time, by yielding control of the processor to be used by other processes.",
            label_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_cederProcesador_porcentajeTiempoActividad_label',
            description_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_cederProcesador_porcentajeTiempoActividad_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Para Ceder Procesador: el sistema limitara a este porcentaje el tiempo de actividad de este proceso, cediendo el procesador para que atienda otros procesos.",
        duplicates="0",
        label2="Yield Processor Activity Time Percentage",
        ea_localid="1698",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="For Yield Processor: the system shall limit the activity of processes of this kind, to this percentage of time, by yielding control of the processor to be used by other processes.",
        ea_guid="{8FE0838C-86BB-4668-8642-782EE6D10242}",
        scale="0",
        default="50",
        label="Ceder Procesador Porcentaje Tiempo Actividad",
        length="0",
        containment="Not Specified",
        position="7",
        owner_class_name="TRAParametrosControlProgreso"
    ),

    IntegerField(
        name='cederProcesador_maximoElementosLeidos',
        widget=IntegerField._properties['widget'](
            label="Ceder Procesador Maximo Elementos Leidos",
            label2="Yield Processor Max Traversed Elements",
            description="Para Ceder Procesador: cuando se lea este numero de elementos desde la ultima vez que se cedio el procesador, el sistema cedera el procesador para que atienda otros procesos.",
            description2="For Yield Processor: when this number of elements has been read since the processor was last yield, the system shall yield the processor to be used by other processes.",
            label_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_cederProcesador_maximoElementosLeidos_label',
            description_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_cederProcesador_maximoElementosLeidos_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Para Ceder Procesador: cuando se lea este numero de elementos desde la ultima vez que se cedio el procesador, el sistema cedera el procesador para que atienda otros procesos.",
        duplicates="0",
        label2="Yield Processor Max Traversed Elements",
        ea_localid="1687",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="For Yield Processor: when this number of elements has been read since the processor was last yield, the system shall yield the processor to be used by other processes.",
        ea_guid="{BD79B12A-59AB-4e06-A37B-7814C41BB340}",
        scale="0",
        default="3000",
        label="Ceder Procesador Maximo Elementos Leidos",
        length="0",
        containment="Not Specified",
        position="4",
        owner_class_name="TRAParametrosControlProgreso"
    ),

    IntegerField(
        name='cederProcesador_maximoElementosModificados',
        widget=IntegerField._properties['widget'](
            label="Ceder Procesador Maximo Elementos Modificados",
            label2="Yield Processor Max Modified Elements",
            description="Para Ceder Procesador: cuando se modifique este numero de elementos desde la ultima vez que se cedio el procesador, el sistema cedera el procesador para que atienda otros procesos.",
            description2="For Yield Processor: when this number of elements has been modified since the processor was last yield, the system shall yield the processor to be used by other processes.",
            label_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_cederProcesador_maximoElementosModificados_label',
            description_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_cederProcesador_maximoElementosModificados_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Para Ceder Procesador: cuando se modifique este numero de elementos desde la ultima vez que se cedio el procesador, el sistema cedera el procesador para que atienda otros procesos.",
        duplicates="0",
        label2="Yield Processor Max Modified Elements",
        ea_localid="1688",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="For Yield Processor: when this number of elements has been modified since the processor was last yield, the system shall yield the processor to be used by other processes.",
        ea_guid="{9EE6F168-869F-4c40-80A7-B102E65CD8B3}",
        scale="0",
        default="3000",
        label="Ceder Procesador Maximo Elementos Modificados",
        length="0",
        containment="Not Specified",
        position="5",
        owner_class_name="TRAParametrosControlProgreso"
    ),

    IntegerField(
        name='cederProcesador_maximoMilisegundos',
        widget=IntegerField._properties['widget'](
            label="Ceder Procesador Maximo Milisegundos",
            label2="Yield Processor Max Milliseconds",
            description="Para Ceder Procesador: cuando haya transcurrido este numero de milisegundos desde la ultima vez que se cedio el procesador, el sistema cedera el procesador para que atienda otros procesos.",
            description2="For Yield Processor: when this number of milliseconds has lapsed since the processor was last yield, the system shall yield the processor to be used by other processes.",
            label_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_cederProcesador_maximoMilisegundos_label',
            description_msgid='gvSIGi18n_TRAParametrosControlProgreso_attr_cederProcesador_maximoMilisegundos_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Para Ceder Procesador: cuando haya transcurrido este numero de milisegundos desde la ultima vez que se cedio el procesador, el sistema cedera el procesador para que atienda otros procesos.",
        duplicates="0",
        label2="Yield Processor Max Milliseconds",
        ea_localid="1689",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="For Yield Processor: when this number of milliseconds has lapsed since the processor was last yield, the system shall yield the processor to be used by other processes.",
        ea_guid="{B334F134-1257-4f6c-B1C1-C50CDEA5B4FF}",
        scale="0",
        default="1000",
        label="Ceder Procesador Maximo Milisegundos",
        length="0",
        containment="Not Specified",
        position="6",
        owner_class_name="TRAParametrosControlProgreso"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAParametrosControlProgreso_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAArquetipo, 'schema', Schema(())).copy() + \
    getattr(TRAParametrosControlProgreso_Operaciones, 'schema', Schema(())).copy() + \
    getattr(TRAConRegistroActividad, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAParametrosControlProgreso(OrderedBaseFolder, TRAArquetipo, TRAParametrosControlProgreso_Operaciones, TRAConRegistroActividad):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAArquetipo,'__implements__',()),) + (getattr(TRAParametrosControlProgreso_Operaciones,'__implements__',()),) + (getattr(TRAConRegistroActividad,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Parametros Control de Progreso'

    meta_type = 'TRAParametrosControlProgreso'
    portal_type = 'TRAParametrosControlProgreso'


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



    allowed_content_types = [] + list(getattr(TRAArquetipo, 'allowed_content_types', [])) + list(getattr(TRAParametrosControlProgreso_Operaciones, 'allowed_content_types', [])) + list(getattr(TRAConRegistroActividad, 'allowed_content_types', []))
    filter_content_types             = 1
    global_allow                     = 0
    content_icon = 'traparametroscontrolprogreso.gif'
    immediate_view                   = 'Tabular'
    default_view                     = 'Tabular'
    suppl_views                      = ['Tabular',]
    typeDescription                  = "Parametros que controlan la gestion del progreso de procesos de larga duracion, incluyendo el registro, transacciones, guardar resultados y ceder procesador."
    typeDescMsgId                    =  'gvSIGi18n_TRAParametrosControlProgreso_help'
    archetype_name2                  = 'Progress Control Parameters'
    typeDescription2                 = '''Parameters controlling the management of the progress of long-lived processes, including logging, transactions, store results and yield processor.'''
    archetype_name_msgid             = 'gvSIGi18n_TRAParametrosControlProgreso_label'
    factory_methods                  = None
    factory_enablers                 = None
    propagate_delete_impact_to       = None
    allow_discussion = 0


    actions =  (


       {'action': "string:$object_url/Editar",
        'category': "object",
        'id': 'edit',
        'name': 'Edit',
        'permissions': ("Modify portal content",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Edit_TRAParametrosControlProgreso')"""
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

    schema = TRAParametrosControlProgreso_schema

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
        
        return self
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata', 'sharing', 'folderContents']:
            a['visible'] = 0
    return fti

registerType(TRAParametrosControlProgreso, PROJECTNAME)
# end of class TRAParametrosControlProgreso

##code-section module-footer #fill in your manual code here
##/code-section module-footer



