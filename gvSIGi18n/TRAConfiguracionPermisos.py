# -*- coding: utf-8 -*-
#
# File: TRAConfiguracionPermisos.py
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
from TRAConfiguracionPermisos_Operaciones import TRAConfiguracionPermisos_Operaciones
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from TRAElemento_Operaciones import TRAElemento_Operaciones

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='esAnonymousTRAManager',
        widget=SelectionWidget(
            label="Anonimos son TRAManager",
            label2="Anonymous are TRAManager",
            description="Si es Verdadero, entonces los Usuarios Anonimos pueden operar como TRAManager.",
            description2="If True, then Anonymous Users can operate as TRAManager.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esAnonymousTRAManager_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esAnonymousTRAManager_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Anonimos pueden operar como TRAManager.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esAnonymousTRAManager_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esAnonymousTRAManager_option_No'],
        label2="Anonymous are TRAManager",
        ea_localid="1976",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Anonymous Users can operate as TRAManager.",
        ea_guid="{A24CFD57-3452-479c-87F7-6D3E59D891BE}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Anonimos son TRAManager",
        length="0",
        containment="Not Specified",
        position="0",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esAnonymousTRACoordinator',
        widget=SelectionWidget(
            label="Anonimos son TRACoordinator",
            label2="Anonymous are TRACoordinator",
            description="Si es Verdadero, entonces los Usuarios Anonimos pueden operar como sonTRACoordinator.",
            description2="If True, then Anonymous Users can operate as sonTRACoordinator.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esAnonymousTRACoordinator_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esAnonymousTRACoordinator_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Anonimos pueden operar como sonTRACoordinator.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esAnonymousTRACoordinator_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esAnonymousTRACoordinator_option_No'],
        label2="Anonymous are TRACoordinator",
        ea_localid="1977",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Anonymous Users can operate as sonTRACoordinator.",
        ea_guid="{C5D954A4-8F2F-47e1-AAF9-1010816030F6}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Anonimos son TRACoordinator",
        length="0",
        containment="Not Specified",
        position="5",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esAnonymousTRADeveloper',
        widget=SelectionWidget(
            label="Anonimos son TRADeveloper",
            label2="Anonymous are TRADeveloper",
            description="Si es Verdadero, entonces los Usuarios Anonimos pueden operar como TRADeveloper.",
            description2="If True, then Anonymous Users can operate as TRADeveloper.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esAnonymousTRADeveloper_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esAnonymousTRADeveloper_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Anonimos pueden operar como TRADeveloper.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esAnonymousTRADeveloper_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esAnonymousTRADeveloper_option_No'],
        label2="Anonymous are TRADeveloper",
        ea_localid="1978",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Anonymous Users can operate as TRADeveloper.",
        ea_guid="{3A172EDC-414C-4f7d-9B24-684CA59B4E29}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Anonimos son TRADeveloper",
        length="0",
        containment="Not Specified",
        position="11",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esAnonymousTRAReviewer',
        widget=SelectionWidget(
            label="Anonimos son TRAReviewer",
            label2="Anonymous are TRAReviewer",
            description="Si es Verdadero, entonces los Usuarios Anonimos pueden operar como TRAReviewer.",
            description2="If True, then Anonymous Users can operate as TRAReviewer.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esAnonymousTRAReviewer_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esAnonymousTRAReviewer_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Anonimos pueden operar como TRAReviewer.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esAnonymousTRAReviewer_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esAnonymousTRAReviewer_option_No'],
        label2="Anonymous are TRAReviewer",
        ea_localid="1979",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Anonymous Users can operate as TRAReviewer.",
        ea_guid="{7C64253A-A093-45d2-A3F5-1B9FC37A0561}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Anonimos son TRAReviewer",
        length="0",
        containment="Not Specified",
        position="17",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esAnonymousTRATranslator',
        widget=SelectionWidget(
            label="Anonimos son TRATranslator",
            label2="Anonymous are TRATranslator",
            description="Si es Verdadero, entonces los Usuarios Anonimos pueden operar como TRATranslator.",
            description2="If True, then Anonymous Users can operate as TRATranslator.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esAnonymousTRATranslator_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esAnonymousTRATranslator_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Anonimos pueden operar como TRATranslator.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esAnonymousTRATranslator_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esAnonymousTRATranslator_option_No'],
        label2="Anonymous are TRATranslator",
        ea_localid="1980",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Anonymous Users can operate as TRATranslator.",
        ea_guid="{1D02A209-0A1E-4262-935C-F45C616FB47D}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Anonimos son TRATranslator",
        length="0",
        containment="Not Specified",
        position="22",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esAnonymousTRAVisitor',
        widget=SelectionWidget(
            label="Anonimos son TRAVisitor",
            label2="Anonymous are TRAVisitor",
            description="Si es Verdadero, entonces los Usuarios Anonimos pueden operar como TRAVisitor.",
            description2="If True, then Anonymous Users can operate as TRAVisitor.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esAnonymousTRAVisitor_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esAnonymousTRAVisitor_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Anonimos pueden operar como TRAVisitor.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esAnonymousTRAVisitor_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esAnonymousTRAVisitor_option_No'],
        label2="Anonymous are TRAVisitor",
        ea_localid="1981",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Anonymous Users can operate as TRAVisitor.",
        ea_guid="{577366B9-5AE7-46a4-8626-F1EA6898D73B}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Anonimos son TRAVisitor",
        length="0",
        containment="Not Specified",
        position="28",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esAuthenticatedTRAManager',
        widget=SelectionWidget(
            label="Autentificados son TRAManager",
            label2="Authenticated are TRAManager",
            description="Si es Verdadero, entonces los Usuarios Autentificados pueden operar como TRAManager.",
            description2="If True, then Authenticated Users can operate as TRAManager.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esAuthenticatedTRAManager_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esAuthenticatedTRAManager_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Autentificados pueden operar como TRAManager.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esAuthenticatedTRAManager_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esAuthenticatedTRAManager_option_No'],
        label2="Authenticated are TRAManager",
        ea_localid="1982",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Authenticated Users can operate as TRAManager.",
        ea_guid="{5E06B488-DFED-4800-B702-625760ECC152}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Autentificados son TRAManager",
        length="0",
        containment="Not Specified",
        position="1",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esAuthenticatedTRACoordinator',
        widget=SelectionWidget(
            label="Autentificados son TRACoordinator",
            label2="Authenticated are TRACoordinator",
            description="Si es Verdadero, entonces los Usuarios Autentificados pueden operar como sonTRACoordinator.",
            description2="If True, then Authenticated Users can operate as sonTRACoordinator.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esAuthenticatedTRACoordinator_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esAuthenticatedTRACoordinator_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Autentificados pueden operar como sonTRACoordinator.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esAuthenticatedTRACoordinator_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esAuthenticatedTRACoordinator_option_No'],
        label2="Authenticated are TRACoordinator",
        ea_localid="1983",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Authenticated Users can operate as sonTRACoordinator.",
        ea_guid="{5A8289A1-8D58-47ff-BC41-8879EB379277}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Autentificados son TRACoordinator",
        length="0",
        containment="Not Specified",
        position="6",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esAuthenticatedTRADeveloper',
        widget=SelectionWidget(
            label="Autentificados son TRADeveloper",
            label2="Authenticated are TRADeveloper",
            description="Si es Verdadero, entonces los Usuarios Autentificados pueden operar como TRADeveloper.",
            description2="If True, then Authenticated Users can operate as TRADeveloper.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esAuthenticatedTRADeveloper_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esAuthenticatedTRADeveloper_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Autentificados pueden operar como TRADeveloper.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esAuthenticatedTRADeveloper_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esAuthenticatedTRADeveloper_option_No'],
        label2="Authenticated are TRADeveloper",
        ea_localid="1984",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Authenticated Users can operate as TRADeveloper.",
        ea_guid="{B4065F1A-8D2E-4171-89B2-DE71B4FE17E0}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Autentificados son TRADeveloper",
        length="0",
        containment="Not Specified",
        position="12",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esAuthenticatedTRAReviewer',
        widget=SelectionWidget(
            label="Autentificados son TRAReviewer",
            label2="Authenticated are TRAReviewer",
            description="Si es Verdadero, entonces los Usuarios Autentificados pueden operar como TRAReviewer.",
            description2="If True, then Authenticated Users can operate as TRAReviewer.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esAuthenticatedTRAReviewer_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esAuthenticatedTRAReviewer_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Autentificados pueden operar como TRAReviewer.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esAuthenticatedTRAReviewer_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esAuthenticatedTRAReviewer_option_No'],
        label2="Authenticated are TRAReviewer",
        ea_localid="1985",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Authenticated Users can operate as TRAReviewer.",
        ea_guid="{08AD6E90-1DF0-4bc2-B0D3-74724AB3303C}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Autentificados son TRAReviewer",
        length="0",
        containment="Not Specified",
        position="18",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esAuthenticatedTRATranslator',
        widget=SelectionWidget(
            label="Autentificados son TRATranslator",
            label2="Authenticated are TRATranslator",
            description="Si es Verdadero, entonces los Usuarios Autentificados pueden operar como TRATranslator.",
            description2="If True, then Authenticated Users can operate as TRATranslator.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esAuthenticatedTRATranslator_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esAuthenticatedTRATranslator_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Autentificados pueden operar como TRATranslator.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esAuthenticatedTRATranslator_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esAuthenticatedTRATranslator_option_No'],
        label2="Authenticated are TRATranslator",
        ea_localid="1986",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Authenticated Users can operate as TRATranslator.",
        ea_guid="{2051C54E-CA2B-43b7-98B9-7943E6CA263F}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Autentificados son TRATranslator",
        length="0",
        containment="Not Specified",
        position="23",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esAuthenticatedTRAVisitor',
        widget=SelectionWidget(
            label="Autentificados son TRAVisitor",
            label2="Authenticated are TRAVisitor",
            description="Si es Verdadero, entonces los Usuarios Autentificados pueden operar como TRAVisitor.",
            description2="If True, then Authenticated Users can operate as TRAVisitor.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esAuthenticatedTRAVisitor_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esAuthenticatedTRAVisitor_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Autentificados pueden operar como TRAVisitor.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esAuthenticatedTRAVisitor_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esAuthenticatedTRAVisitor_option_No'],
        label2="Authenticated are TRAVisitor",
        ea_localid="1987",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Authenticated Users can operate as TRAVisitor.",
        ea_guid="{D6CF3BFF-9E3C-47d9-A66A-FC8506F2E299}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Autentificados son TRAVisitor",
        length="0",
        containment="Not Specified",
        position="29",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esMemberTRAManager',
        widget=SelectionWidget(
            label="Miembros son TRAManager",
            label2="Members are TRAManager",
            description="Si es Verdadero, entonces los Usuarios Miembros pueden operar como TRAManager.",
            description2="If True, then Members Users can operate as TRAManager.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esMemberTRAManager_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esMemberTRAManager_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Miembros pueden operar como TRAManager.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esMemberTRAManager_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esMemberTRAManager_option_No'],
        label2="Members are TRAManager",
        ea_localid="1988",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Members Users can operate as TRAManager.",
        ea_guid="{3DA01D5A-D4B1-4286-B3FE-5C7602AA3345}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Miembros son TRAManager",
        length="0",
        containment="Not Specified",
        position="8",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esMemberTRACoordinator',
        widget=SelectionWidget(
            label="Miembros son TRACoordinator",
            label2="Members are sonTRACoordinator",
            description="Si es Verdadero, entonces los Usuarios Miembros pueden operar como sonTRACoordinator.",
            description2="If True, then Members Users can operate as sonTRACoordinator.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esMemberTRACoordinator_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esMemberTRACoordinator_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Miembros pueden operar como sonTRACoordinator.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esMemberTRACoordinator_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esMemberTRACoordinator_option_No'],
        label2="Members are sonTRACoordinator",
        ea_localid="1989",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Members Users can operate as sonTRACoordinator.",
        ea_guid="{CDC487B4-6126-4cd9-B600-5CEB05AFCBD4}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Miembros son TRACoordinator",
        length="0",
        containment="Not Specified",
        position="14",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esMemberTRADeveloper',
        widget=SelectionWidget(
            label="Miembros son TRADeveloper",
            label2="Members are TRADeveloper",
            description="Si es Verdadero, entonces los Usuarios Miembros pueden operar como TRADeveloper.",
            description2="If True, then Members Users can operate as TRADeveloper.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esMemberTRADeveloper_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esMemberTRADeveloper_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Miembros pueden operar como TRADeveloper.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esMemberTRADeveloper_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esMemberTRADeveloper_option_No'],
        label2="Members are TRADeveloper",
        ea_localid="1990",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Members Users can operate as TRADeveloper.",
        ea_guid="{05DEF259-6500-45fb-8B18-9F97F7987132}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Miembros son TRADeveloper",
        length="0",
        containment="Not Specified",
        position="25",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esMemberTRAReviewer',
        widget=SelectionWidget(
            label="Miembros son TRAReviewer",
            label2="Members are TRAReviewer",
            description="Si es Verdadero, entonces los Usuarios Miembros pueden operar como TRAReviewer.",
            description2="If True, then Members Users can operate as TRAReviewer.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esMemberTRAReviewer_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esMemberTRAReviewer_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Miembros pueden operar como TRAReviewer.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esMemberTRAReviewer_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esMemberTRAReviewer_option_No'],
        label2="Members are TRAReviewer",
        ea_localid="1991",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Members Users can operate as TRAReviewer.",
        ea_guid="{8CA3CE0D-259D-4412-93DA-882A6539C0E3}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Miembros son TRAReviewer",
        length="0",
        containment="Not Specified",
        position="33",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esMemberTRATranslator',
        widget=SelectionWidget(
            label="Miembros son TRATranslator",
            label2="Members are TRATranslator",
            description="Si es Verdadero, entonces los Usuarios Miembros pueden operar como TRATranslator.",
            description2="If True, then Members Users can operate as TRATranslator.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esMemberTRATranslator_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esMemberTRATranslator_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Miembros pueden operar como TRATranslator.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esMemberTRATranslator_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esMemberTRATranslator_option_No'],
        label2="Members are TRATranslator",
        ea_localid="1992",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Members Users can operate as TRATranslator.",
        ea_guid="{6A5FCF1A-300E-4b4e-8DBB-C611D324D4D0}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Miembros son TRATranslator",
        length="0",
        containment="Not Specified",
        position="34",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esMemberTRAVisitor',
        widget=SelectionWidget(
            label="Miembros son TRAVisitor",
            label2="Members are TRAVisitor",
            description="Si es Verdadero, entonces los Usuarios Miembros pueden operar como TRAVisitor.",
            description2="If True, then Members Users can operate as TRAVisitor.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esMemberTRAVisitor_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esMemberTRAVisitor_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Miembros pueden operar como TRAVisitor.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esMemberTRAVisitor_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esMemberTRAVisitor_option_No'],
        label2="Members are TRAVisitor",
        ea_localid="1993",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Members Users can operate as TRAVisitor.",
        ea_guid="{D4D2B5B7-0A98-47da-81F6-61BD0F32DCAB}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Miembros son TRAVisitor",
        length="0",
        containment="Not Specified",
        position="35",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esReviewerTRAManager',
        widget=SelectionWidget(
            label="Revisores son TRAManager",
            label2="Reviewers are TRAManager",
            description="Si es Verdadero, entonces los Usuarios Revisores pueden operar como TRAManager.",
            description2="If True, then Reviewers Users can operate as TRAManager.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esReviewerTRAManager_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esReviewerTRAManager_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Revisores pueden operar como TRAManager.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esReviewerTRAManager_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esReviewerTRAManager_option_No'],
        label2="Reviewers are TRAManager",
        ea_localid="1994",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Reviewers Users can operate as TRAManager.",
        ea_guid="{B3CCED7A-E1DC-46b9-82E2-42E63232D7D4}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Revisores son TRAManager",
        length="0",
        containment="Not Specified",
        position="4",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esReviewerTRACoordinator',
        widget=SelectionWidget(
            label="Revisores son TRACoordinator",
            label2="Reviewers are TRACoordinator",
            description="Si es Verdadero, entonces los Usuarios Revisores pueden operar como sonTRACoordinator.",
            description2="If True, then Reviewers Users can operate as sonTRACoordinator.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esReviewerTRACoordinator_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esReviewerTRACoordinator_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Revisores pueden operar como sonTRACoordinator.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esReviewerTRACoordinator_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esReviewerTRACoordinator_option_No'],
        label2="Reviewers are TRACoordinator",
        ea_localid="1995",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Reviewers Users can operate as sonTRACoordinator.",
        ea_guid="{16715403-3288-4ea3-B9B9-7F719868B2AE}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Revisores son TRACoordinator",
        length="0",
        containment="Not Specified",
        position="10",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esReviewerTRADeveloper',
        widget=SelectionWidget(
            label="Revisores son TRADeveloper",
            label2="Reviewers are TRADeveloper",
            description="Si es Verdadero, entonces los Usuarios Revisores pueden operar como TRADeveloper.",
            description2="If True, then Reviewers Users can operate as TRADeveloper.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esReviewerTRADeveloper_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esReviewerTRADeveloper_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Revisores pueden operar como TRADeveloper.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esReviewerTRADeveloper_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esReviewerTRADeveloper_option_No'],
        label2="Reviewers are TRADeveloper",
        ea_localid="1996",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Reviewers Users can operate as TRADeveloper.",
        ea_guid="{1C1F908C-E974-480d-8328-B159B009B854}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Revisores son TRADeveloper",
        length="0",
        containment="Not Specified",
        position="16",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esReviewerTRAReviewer',
        widget=SelectionWidget(
            label="Revisores son TRAReviewer",
            label2="Reviewers are TRAReviewer",
            description="Si es Verdadero, entonces los Usuarios Revisores pueden operar como TRAReviewer.",
            description2="If True, then Reviewers Users can operate as TRAReviewer.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esReviewerTRAReviewer_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esReviewerTRAReviewer_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Revisores pueden operar como TRAReviewer.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esReviewerTRAReviewer_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esReviewerTRAReviewer_option_No'],
        label2="Reviewers are TRAReviewer",
        ea_localid="1997",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Reviewers Users can operate as TRAReviewer.",
        ea_guid="{C67CCBDF-5C04-4dea-BB54-7769F3B04F72}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Revisores son TRAReviewer",
        length="0",
        containment="Not Specified",
        position="21",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esReviewerTRATranslator',
        widget=SelectionWidget(
            label="Revisores son TRATranslator",
            label2="Reviewers are TRATranslator",
            description="Si es Verdadero, entonces los Usuarios Revisores pueden operar como TRATranslator.",
            description2="If True, then Reviewers Users can operate as TRATranslator.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esReviewerTRATranslator_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esReviewerTRATranslator_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Revisores pueden operar como TRATranslator.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esReviewerTRATranslator_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esReviewerTRATranslator_option_No'],
        label2="Reviewers are TRATranslator",
        ea_localid="1998",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Reviewers Users can operate as TRATranslator.",
        ea_guid="{6FC1C568-3AC5-4a25-BE65-728347096EA4}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="No",
        label="Revisores son TRATranslator",
        length="0",
        containment="Not Specified",
        position="27",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esReviewerTRAVisitor',
        widget=SelectionWidget(
            label="Revisores son TRAVisitor",
            label2="Reviewers are TRAVisitor",
            description="Si es Verdadero, entonces los Usuarios Revisores pueden operar como TRAVisitor.",
            description2="If True, then Reviewers Users can operate as TRAVisitor.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esReviewerTRAVisitor_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esReviewerTRAVisitor_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Revisores pueden operar como TRAVisitor.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esReviewerTRAVisitor_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esReviewerTRAVisitor_option_No'],
        label2="Reviewers are TRAVisitor",
        ea_localid="1999",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Reviewers Users can operate as TRAVisitor.",
        ea_guid="{AA32A493-6571-42c5-9DE2-CCFC8C26A6AC}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Revisores son TRAVisitor",
        length="0",
        containment="Not Specified",
        position="32",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esOwnerTRAManager',
        widget=SelectionWidget(
            label="Propietarios son TRAManager",
            label2="Owners are TRAManager",
            description="Si es Verdadero, entonces los Usuarios Propietarios pueden operar como TRAManager.",
            description2="If True, then Owners Users can operate as TRAManager.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esOwnerTRAManager_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esOwnerTRAManager_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Propietarios pueden operar como TRAManager.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esOwnerTRAManager_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esOwnerTRAManager_option_No'],
        label2="Owners are TRAManager",
        ea_localid="2000",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Owners Users can operate as TRAManager.",
        ea_guid="{9549222C-3F48-4a82-8E47-B8907715D10C}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Propietarios son TRAManager",
        length="0",
        containment="Not Specified",
        position="3",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esOwnerTRACoordinator',
        widget=SelectionWidget(
            label="Propietarios son TRACoordinator",
            label2="Owners are TRACoordinator",
            description="Si es Verdadero, entonces los Usuarios Propietarios pueden operar como sonTRACoordinator.",
            description2="If True, then Owners Users can operate as sonTRACoordinator.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esOwnerTRACoordinator_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esOwnerTRACoordinator_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Propietarios pueden operar como sonTRACoordinator.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esOwnerTRACoordinator_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esOwnerTRACoordinator_option_No'],
        label2="Owners are TRACoordinator",
        ea_localid="2001",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Owners Users can operate as sonTRACoordinator.",
        ea_guid="{1DD0C4CC-3379-4e36-8B68-C49BA92D954E}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Propietarios son TRACoordinator",
        length="0",
        containment="Not Specified",
        position="9",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esOwnerTRADeveloper',
        widget=SelectionWidget(
            label="Propietarios son TRADeveloper",
            label2="Owners are TRADeveloper",
            description="Si es Verdadero, entonces los Usuarios Propietarios pueden operar como TRADeveloper.",
            description2="If True, then Owners Users can operate as TRADeveloper.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esOwnerTRADeveloper_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esOwnerTRADeveloper_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Propietarios pueden operar como TRADeveloper.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esOwnerTRADeveloper_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esOwnerTRADeveloper_option_No'],
        label2="Owners are TRADeveloper",
        ea_localid="2002",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Owners Users can operate as TRADeveloper.",
        ea_guid="{7FD003EE-69E5-4c4f-BAD0-A5A8D0B18956}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Propietarios son TRADeveloper",
        length="0",
        containment="Not Specified",
        position="15",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esOwnerTRAReviewer',
        widget=SelectionWidget(
            label="Propietarios son TRAReviewer",
            label2="Owners are TRAReviewer",
            description="Si es Verdadero, entonces los Usuarios Propietarios pueden operar como TRAReviewer.",
            description2="If True, then Owners Users can operate as TRAReviewer.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esOwnerTRAReviewer_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esOwnerTRAReviewer_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Propietarios pueden operar como TRAReviewer.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esOwnerTRAReviewer_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esOwnerTRAReviewer_option_No'],
        label2="Owners are TRAReviewer",
        ea_localid="2003",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Owners Users can operate as TRAReviewer.",
        ea_guid="{5302587A-4B38-4cf7-833B-40C2058BC5AA}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Propietarios son TRAReviewer",
        length="0",
        containment="Not Specified",
        position="20",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esOwnerTRATranslator',
        widget=SelectionWidget(
            label="Propietarios son TRATranslator",
            label2="Owners are TRATranslator",
            description="Si es Verdadero, entonces los Usuarios Propietarios pueden operar como TRATranslator.",
            description2="If True, then Owners Users can operate as TRATranslator.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esOwnerTRATranslator_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esOwnerTRATranslator_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Propietarios pueden operar como TRATranslator.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esOwnerTRATranslator_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esOwnerTRATranslator_option_No'],
        label2="Owners are TRATranslator",
        ea_localid="2004",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Owners Users can operate as TRATranslator.",
        ea_guid="{13C09DB5-B481-4088-9AEA-B1BB6DAFD87F}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Propietarios son TRATranslator",
        length="0",
        containment="Not Specified",
        position="26",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esOwnerTRAVisitor',
        widget=SelectionWidget(
            label="Propietarios son TRAVisitor",
            label2="Owners are TRAVisitor",
            description="Si es Verdadero, entonces los Usuarios Propietarios pueden operar como TRAVisitor.",
            description2="If True, then Owners Users can operate as TRAVisitor.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esOwnerTRAVisitor_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esOwnerTRAVisitor_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Propietarios pueden operar como TRAVisitor.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esOwnerTRAVisitor_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esOwnerTRAVisitor_option_No'],
        label2="Owners are TRAVisitor",
        ea_localid="2005",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Owners Users can operate as TRAVisitor.",
        ea_guid="{32D32002-E5FA-435f-A1BC-978145026570}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Propietarios son TRAVisitor",
        length="0",
        containment="Not Specified",
        position="31",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esManagerTRAManager',
        widget=SelectionWidget(
            label="Managers son TRAManager",
            label2="Managers are TRAManager",
            description="Si es Verdadero, entonces los Usuarios Managers pueden operar como TRAManager.",
            description2="If True, then Managers Users can operate as TRAManager.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esManagerTRAManager_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esManagerTRAManager_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Managers pueden operar como TRAManager.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esManagerTRAManager_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esManagerTRAManager_option_No'],
        label2="Managers are TRAManager",
        ea_localid="2006",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Managers Users can operate as TRAManager.",
        ea_guid="{EE991588-D233-4104-BB7F-93316E09E87F}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Managers son TRAManager",
        length="0",
        containment="Not Specified",
        position="2",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esManagerTRACoordinator',
        widget=SelectionWidget(
            label="Managers son TRACoordinator",
            label2="Managers are TRACoordinator",
            description="Si es Verdadero, entonces los Usuarios Managers pueden operar como sonTRACoordinator.",
            description2="If True, then Managers Users can operate as sonTRACoordinator.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esManagerTRACoordinator_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esManagerTRACoordinator_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Managers pueden operar como sonTRACoordinator.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esManagerTRACoordinator_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esManagerTRACoordinator_option_No'],
        label2="Managers are TRACoordinator",
        ea_localid="2007",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Managers Users can operate as sonTRACoordinator.",
        ea_guid="{9FDAEC1B-9513-4898-AF90-717433370741}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Managers son TRACoordinator",
        length="0",
        containment="Not Specified",
        position="7",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esManagerTRADeveloper',
        widget=SelectionWidget(
            label="Managers son TRADeveloper",
            label2="Managers are TRADeveloper",
            description="Si es Verdadero, entonces los Usuarios Managers pueden operar como TRADeveloper.",
            description2="If True, then Managers Users can operate as TRADeveloper.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esManagerTRADeveloper_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esManagerTRADeveloper_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Managers pueden operar como TRADeveloper.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esManagerTRADeveloper_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esManagerTRADeveloper_option_No'],
        label2="Managers are TRADeveloper",
        ea_localid="2008",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Managers Users can operate as TRADeveloper.",
        ea_guid="{E23B7489-BD6A-4fca-9E3E-889F62F61C23}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Managers son TRADeveloper",
        length="0",
        containment="Not Specified",
        position="13",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esManagerTRAReviewer',
        widget=SelectionWidget(
            label="Managers son TRAReviewer",
            label2="Managers are TRAReviewer",
            description="Si es Verdadero, entonces los Usuarios Managers pueden operar como TRAReviewer.",
            description2="If True, then Managers Users can operate as TRAReviewer.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esManagerTRAReviewer_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esManagerTRAReviewer_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Managers pueden operar como TRAReviewer.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esManagerTRAReviewer_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esManagerTRAReviewer_option_No'],
        label2="Managers are TRAReviewer",
        ea_localid="2009",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Managers Users can operate as TRAReviewer.",
        ea_guid="{F0C68D96-2956-41ab-A68C-C70426D6924A}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Managers son TRAReviewer",
        length="0",
        containment="Not Specified",
        position="19",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esManagerTRATranslator',
        widget=SelectionWidget(
            label="Managers son TRATranslator",
            label2="Managers are TRATranslator",
            description="Si es Verdadero, entonces los Usuarios Managers pueden operar como TRATranslator.",
            description2="If True, then Managers Users can operate as TRATranslator.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esManagerTRATranslator_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esManagerTRATranslator_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Managers pueden operar como TRATranslator.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esManagerTRATranslator_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esManagerTRATranslator_option_No'],
        label2="Managers are TRATranslator",
        ea_localid="2010",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Managers Users can operate as TRATranslator.",
        ea_guid="{E50E9161-C59D-48cb-BB2E-761EABC2623D}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Managers son TRATranslator",
        length="0",
        containment="Not Specified",
        position="24",
        owner_class_name="TRAConfiguracionPermisos"
    ),

    StringField(
        name='esManagerTRAVisitor',
        widget=SelectionWidget(
            label="Managers son TRAVisitor",
            label2="Managers are TRAVisitor",
            description="Si es Verdadero, entonces los Usuarios Managers pueden operar como TRAVisitor.",
            description2="If True, then Managers Users can operate as TRAVisitor.",
            label_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esManagerTRAVisitor_label',
            description_msgid='gvSIGi18n_TRAConfiguracionPermisos_attr_esManagerTRAVisitor_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces los Usuarios Managers pueden operar como TRAVisitor.",
        vocabulary=['Si','No',],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAConfiguracionPermisos_attr_esManagerTRAVisitor_option_Si', 'gvSIGi18n_TRAConfiguracionPermisos_attr_esManagerTRAVisitor_option_No'],
        label2="Managers are TRAVisitor",
        ea_localid="2011",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then Managers Users can operate as TRAVisitor.",
        ea_guid="{460BBF74-C5AE-4aeb-BD8B-F0D003C0533D}",
        vocabulary2=['Yes','No',],
        scale="0",
        default="Si",
        label="Managers son TRAVisitor",
        length="0",
        containment="Not Specified",
        position="30",
        owner_class_name="TRAConfiguracionPermisos"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAConfiguracionPermisos_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAConfiguracion, 'schema', Schema(())).copy() + \
    getattr(TRAConfiguracionPermisos_Operaciones, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAConfiguracionPermisos(OrderedBaseFolder, TRAConfiguracion, TRAConfiguracionPermisos_Operaciones):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAConfiguracion,'__implements__',()),) + (getattr(TRAConfiguracionPermisos_Operaciones,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Configuracion Permisos'

    meta_type = 'TRAConfiguracionPermisos'
    portal_type = 'TRAConfiguracionPermisos'


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



    allowed_content_types = [] + list(getattr(TRAConfiguracion, 'allowed_content_types', [])) + list(getattr(TRAConfiguracionPermisos_Operaciones, 'allowed_content_types', []))
    filter_content_types             = 1
    global_allow                     = 0
    content_icon = 'traconfiguracion.gif'
    immediate_view                   = 'Tabular'
    default_view                     = 'Tabular'
    suppl_views                      = ['Tabular',]
    typeDescription                  = "Configuracion del catalogo de traducciones, con parametros controlando los permisos de las operaciones sobre el catalogo."
    typeDescMsgId                    =  'gvSIGi18n_TRAConfiguracionPermisos_help'
    archetype_name2                  = 'Permissions Configuration'
    typeDescription2                 = '''Translations catalog configuration, with parameters controlling the permissions of operations on the catalog.'''
    archetype_name_msgid             = 'gvSIGi18n_TRAConfiguracionPermisos_label'
    factory_methods                  = None
    factory_enablers                 = None
    propagate_delete_impact_to       = None
    allow_discussion = False


    actions =  (


       {'action': "string:${object_url}/TRAActivatePermissionsConfiguration_action",
        'category': "object_buttons",
        'id': 'TRAActivateConfiguracionPermisos',
        'name': 'Activate Permissions Configuration',
        'permissions': ("View",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Activate_TRAConfiguracion_Permisos')"""
       },


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

    schema = TRAConfiguracionPermisos_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata', 'sharing', 'folderContents']:
            a['visible'] = 0
    return fti

registerType(TRAConfiguracionPermisos, PROJECTNAME)
# end of class TRAConfiguracionPermisos

##code-section module-footer #fill in your manual code here
##/code-section module-footer



