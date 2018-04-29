# -*- coding: utf-8 -*-
#
# File: TRAConRegistroActividad.py
#
# Copyright (c) 2008, 2009, 2010, 2011 Conselleria de Infraestructuras y
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

__author__ = """acv <gvSIGi18n@gvSIG.org>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.gvSIGi18n.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    DateTimeField(
        name='fechaCreacion',
        widget=CalendarWidget(
            label="Fecha de Creacion",
            label2="Creation Date",
            description="Fecha en que se creo el elemento.",
            description2="Date when the element was created.",
            label_msgid='gvSIGi18n_TRAConRegistroActividad_attr_fechaCreacion_label',
            description_msgid='gvSIGi18n_TRAConRegistroActividad_attr_fechaCreacion_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Fecha en que se creo el elemento.",
        duplicates="0",
        label2="Creation Date",
        ea_localid="1552",
        derived="0",
        precision=0,
        collection="false",
        styleex="IsLiteral=0;volatile=0;",
        is_modification_date=False,
        description2="Date when the element was created.",
        is_creator_user=False,
        is_modificator_user=False,
        ea_guid="{93F03B12-1918-49d7-96BA-251FE45BCE50}",
        is_creation_date=True,
        read_only="True",
        scale="0",
        label="Fecha de Creacion",
        length="0",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        position="0",
        owner_class_name="TRAConRegistroActividad",
        exclude_from_copyconfig="True"
    ),

    StringField(
        name='usuarioCreador',
        widget=StringWidget(
            label="Usuario Creador",
            label2="Creator User",
            description="Usuario que creo el elemento.",
            description2="User who created the element.",
            label_msgid='gvSIGi18n_TRAConRegistroActividad_attr_usuarioCreador_label',
            description_msgid='gvSIGi18n_TRAConRegistroActividad_attr_usuarioCreador_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Usuario que creo el elemento.",
        searchable=0,
        duplicates="0",
        label2="Creator User",
        ea_localid="1553",
        derived="0",
        precision=0,
        collection="false",
        styleex="IsLiteral=0;volatile=0;",
        description2="User who created the element.",
        ea_guid="{84256C18-E30C-49a3-B344-7EC4FB3ED0B9}",
        is_creation_user="True",
        read_only="True",
        scale="0",
        label="Usuario Creador",
        length="0",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        position="1",
        owner_class_name="TRAConRegistroActividad",
        exclude_from_copyconfig="True"
    ),

    DateTimeField(
        name='fechaModificacion',
        widget=CalendarWidget(
            label="Fecha de Modificacion",
            label2="Modification Date",
            description="Fecha en que se modifico el elemento.",
            description2="Date when the element was modified.",
            label_msgid='gvSIGi18n_TRAConRegistroActividad_attr_fechaModificacion_label',
            description_msgid='gvSIGi18n_TRAConRegistroActividad_attr_fechaModificacion_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Fecha en que se modifico el elemento.",
        duplicates="0",
        label2="Modification Date",
        ea_localid="1554",
        derived="0",
        precision=0,
        collection="false",
        styleex="IsLiteral=0;volatile=0;",
        is_modification_date="True",
        description2="Date when the element was modified.",
        ea_guid="{AF6FF801-E86C-42db-BB78-04220A5F3761}",
        read_only="True",
        scale="0",
        label="Fecha de Modificacion",
        length="0",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        position="2",
        owner_class_name="TRAConRegistroActividad",
        exclude_from_copyconfig="True"
    ),

    StringField(
        name='usuarioModificador',
        widget=StringWidget(
            label="Usuario Modificador",
            label2="Modification User",
            description="Usuario que modifico el elemento.",
            description2="User who modified the element.",
            label_msgid='gvSIGi18n_TRAConRegistroActividad_attr_usuarioModificador_label',
            description_msgid='gvSIGi18n_TRAConRegistroActividad_attr_usuarioModificador_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Usuario que modifico el elemento.",
        searchable=0,
        duplicates="0",
        label2="Modification User",
        ea_localid="1555",
        derived="0",
        precision=0,
        collection="false",
        styleex="IsLiteral=0;volatile=0;",
        description2="User who modified the element.",
        ea_guid="{ED62B198-E1A8-46de-92F9-F7C1FD88224F}",
        read_only="True",
        scale="0",
        is_modification_user="True",
        label="Usuario Modificador",
        length="0",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        position="3",
        owner_class_name="TRAConRegistroActividad",
        exclude_from_copyconfig="True"
    ),

    DateTimeField(
        name='fechaEliminacion',
        widget=CalendarWidget(
            label="Fecha de Eliminacion",
            label2="Deletion Date",
            description="Fecha en que se elimino el elemento.",
            description2="Date when the element was deleted.",
            label_msgid='gvSIGi18n_TRAConRegistroActividad_attr_fechaEliminacion_label',
            description_msgid='gvSIGi18n_TRAConRegistroActividad_attr_fechaEliminacion_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Fecha en que se elimino el elemento.",
        duplicates="0",
        derived="0",
        label2="Deletion Date",
        ea_localid="1556",
        is_deletion_date="True",
        precision=0,
        collection="false",
        styleex="IsLiteral=0;volatile=0;",
        description2="Date when the element was deleted.",
        ea_guid="{6C4C994A-1ACD-4b95-9C02-F69AD5A4DE05}",
        read_only="True",
        scale="0",
        label="Fecha de Eliminacion",
        length="0",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        position="4",
        owner_class_name="TRAConRegistroActividad",
        exclude_from_copyconfig="True"
    ),

    StringField(
        name='usuarioEliminador',
        is_deletion_user="True",
        widget=StringWidget(
            label="Usuario Eliminador",
            label2="Deletion User",
            description="Usuario que elimino el elemento.",
            description2="User who deleted the element.",
            label_msgid='gvSIGi18n_TRAConRegistroActividad_attr_usuarioEliminador_label',
            description_msgid='gvSIGi18n_TRAConRegistroActividad_attr_usuarioEliminador_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Usuario que elimino el elemento.",
        searchable=0,
        duplicates="0",
        label2="Deletion User",
        ea_localid="1557",
        derived="0",
        precision=0,
        collection="false",
        styleex="IsLiteral=0;volatile=0;",
        description2="User who deleted the element.",
        ea_guid="{DF736BA9-7CE3-4cfa-9638-E57D1EB055BE}",
        read_only="True",
        scale="0",
        label="Usuario Eliminador",
        length="0",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        position="5",
        owner_class_name="TRAConRegistroActividad",
        exclude_from_copyconfig="True"
    ),

    TextField(
        name='registroDeCambios',
        widget=TextAreaWidget(
            label="Historia de Cambios",
            label2="Change Log",
            description="Regitro de los cambios efectuados sobre el elemento a lo largo del tiempo por diferentes usuarios.",
            description2="Record of changes made to the element over time by different users.",
            label_msgid='gvSIGi18n_TRAConRegistroActividad_attr_registroDeCambios_label',
            description_msgid='gvSIGi18n_TRAConRegistroActividad_attr_registroDeCambios_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Regitro de los cambios efectuados sobre el elemento a lo largo del tiempo por diferentes usuarios.",
        searchable=0,
        duplicates="0",
        label2="Change Log",
        ea_localid="1559",
        derived="0",
        precision=0,
        collection="false",
        styleex="IsLiteral=0;volatile=0;",
        description2="Record of changes made to the element over time by different users.",
        position="7",
        ea_guid="{1F9CBE23-20FF-447c-8344-E6C477166CD4}",
        read_only="True",
        scale="0",
        label="Historia de Cambios",
        length="0",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        is_change_log=True,
        owner_class_name="TRAConRegistroActividad",
        exclude_from_copyconfig="True"
    ),

    IntegerField(
        name='contadorCambios',
        widget=IntegerField._properties['widget'](
            label="Contador de Cambios",
            label2="Change Counter",
            description="Contador de cambios realizados a lo largo del tiempo. Util para descubrir si han tenido lugar cambios desde que se leyeron los datos del elemento.",
            description2="Counter of changes over time. Useful to learn if any changes happened since the reading of the element information.",
            label_msgid='gvSIGi18n_TRAConRegistroActividad_attr_contadorCambios_label',
            description_msgid='gvSIGi18n_TRAConRegistroActividad_attr_contadorCambios_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Contador de cambios realizados a lo largo del tiempo. Util para descubrir si han tenido lugar cambios desde que se leyeron los datos del elemento.",
        duplicates="0",
        label2="Change Counter",
        ea_localid="1560",
        derived="0",
        precision=0,
        collection="false",
        styleex="IsLiteral=0;volatile=0;",
        description2="Counter of changes over time. Useful to learn if any changes happened since the reading of the element information.",
        ea_guid="{AA23EC39-C703-4726-A01E-3C3C3379D9D0}",
        read_only="True",
        scale="0",
        default="0",
        label="Contador de Cambios",
        length="0",
        is_change_counter="True",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        position="8",
        owner_class_name="TRAConRegistroActividad",
        exclude_from_copyconfig="True"
    ),

    BooleanField(
        name='estaInactivo',
        widget=BooleanField._properties['widget'](
            label="El Elemento esta Inactivo",
            label2="Element is Inactive",
            description="Si Verdadero, entonces el elemento esta inactivo porque ha sido eliminado. Los elementos eliminados no se presentan a los usuario en los usos normales de la aplicacion, y se reservan a funciones especiales de administracion.",
            description2="If True, then the element is inactive because it has been delete. Deleted elements are not presented to users in the usual application use cases, and reserved for specialized administration functions.",
            label_msgid='gvSIGi18n_TRAConRegistroActividad_attr_estaInactivo_label',
            description_msgid='gvSIGi18n_TRAConRegistroActividad_attr_estaInactivo_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si Verdadero, entonces el elemento esta inactivo porque ha sido eliminado. Los elementos eliminados no se presentan a los usuario en los usos normales de la aplicacion, y se reservan a funciones especiales de administracion.",
        duplicates="0",
        label2="Element is Inactive",
        ea_localid="1558",
        derived="0",
        precision=0,
        collection="false",
        styleex="IsLiteral=0;volatile=0;",
        description2="If True, then the element is inactive because it has been delete. Deleted elements are not presented to users in the usual application use cases, and reserved for specialized administration functions.",
        ea_guid="{62764C1E-2CA4-446d-8E59-38426ED89399}",
        read_only="True",
        scale="0",
        default="0",
        label="El Elemento esta Inactivo",
        length="0",
        is_inactive_state="True",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        position="6",
        owner_class_name="TRAConRegistroActividad",
        exclude_from_copyconfig="True"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAConRegistroActividad_schema = schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAConRegistroActividad:
    """
    """
    security = ClassSecurityInfo()



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



    allowed_content_types = []
    _at_rename_after_creation = True

    schema = TRAConRegistroActividad_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
# end of class TRAConRegistroActividad

##code-section module-footer #fill in your manual code here
##/code-section module-footer



