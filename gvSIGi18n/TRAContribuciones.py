# -*- coding: utf-8 -*-
#
# File: TRAContribuciones.py
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
from TRAContribuciones_Operaciones import TRAContribuciones_Operaciones
from Products.gvSIGi18n.TRAArquetipo import TRAArquetipo
from Products.gvSIGi18n.TRAConRegistroActividad import TRAConRegistroActividad
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from TRAElemento_Operaciones import TRAElemento_Operaciones
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='usuarioInformador',
        widget=StringWidget(
            label="Usuario Informador",
            label2="Reporting User",
            description="Usuario que ha solicitado creado el Informe.",
            description2="User who requested the ellaboration of the report.",
            label_msgid='gvSIGi18n_TRAContribuciones_attr_usuarioInformador_label',
            description_msgid='gvSIGi18n_TRAContribuciones_attr_usuarioInformador_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Usuario que ha solicitado creado el Informe.",
        duplicates="0",
        label2="Reporting User",
        ea_localid="2070",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="User who requested the ellaboration of the report.",
        ea_guid="{0A28F6AD-0E44-4b6e-9128-359810BF2FFD}",
        read_only="True",
        scale="0",
        label="Usuario Informador",
        length="0",
        containment="Not Specified",
        position="2",
        owner_class_name="TRAContribuciones"
    ),

    DateTimeField(
        name='fechaFinProceso',
        widget=CalendarWidget(
            label="Fecha y Hora de Fin",
            label2="End Date and Time",
            description="Fecha y hora en que termino la elaboracion del informe de contribuciones.",
            description2="Date and Time when the ellaboration of the contributions report was terminated.",
            label_msgid='gvSIGi18n_TRAContribuciones_attr_fechaFinProceso_label',
            description_msgid='gvSIGi18n_TRAContribuciones_attr_fechaFinProceso_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Fecha y hora en que termino la elaboracion del informe de contribuciones.",
        duplicates="0",
        label2="End Date and Time",
        ea_localid="2067",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Date and Time when the ellaboration of the contributions report was terminated.",
        ea_guid="{BDE9E861-3B59-4ad7-A7D2-8B58B1A2B77E}",
        read_only="True",
        scale="0",
        label="Fecha y Hora de Fin",
        length="0",
        containment="Not Specified",
        position="0",
        owner_class_name="TRAContribuciones"
    ),

    StringField(
        name='identificadorElementoProgreso',
        widget=StringWidget(
            label="Identificador del elemento de Control del Progreso",
            label2="Progress Control element Identifier",
            description="Identificador del elemento utilizado para controlar el progreso del proceso de larga duración.",
            description2="Identifier of the element used to control the progress of the long-lived process.",
            label_msgid='gvSIGi18n_TRAContribuciones_attr_identificadorElementoProgreso_label',
            description_msgid='gvSIGi18n_TRAContribuciones_attr_identificadorElementoProgreso_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Identificador del elemento utilizado para controlar el progreso del proceso de larga duración.",
        duplicates="0",
        label2="Progress Control element Identifier",
        ea_localid="2076",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Identifier of the element used to control the progress of the long-lived process.",
        ea_guid="{3F96459F-013F-46d3-9F81-70B3D3349401}",
        read_only="True",
        scale="0",
        label="Identificador del elemento de Control del Progreso",
        length="0",
        containment="Not Specified",
        position="3",
        owner_class_name="TRAContribuciones"
    ),

    ComputedField(
        name='elementoProgreso',
        widget=ReferenceBrowserWidget(
            label="Elemento de Progreso y Resultados",
            label2="Progress and Results element",
            description="Elemento para control del Progreso de la creacion del informe y almacenamiento de los resultados durante el proceso.",
            description2="Element to control the Progress of the report process, and storage of import results during the process.",
            label_msgid='gvSIGi18n_TRAContribuciones_attr_elementoProgreso_label',
            description_msgid='gvSIGi18n_TRAContribuciones_attr_elementoProgreso_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Elemento para control del Progreso de la creacion del informe y almacenamiento de los resultados durante el proceso.",
        duplicates="0",
        label2="Progress and Results element",
        ea_localid="2075",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Element to control the Progress of the report process, and storage of import results during the process.",
        ea_guid="{7345AAE8-084E-4649-B4F8-B9E7F7E5765D}",
        allowed_types=['TRAProgreso'],
        read_only="True",
        scale="0",
        additional_columns=['estadoProceso', 'haCompletadoConExito'],
        label="Elemento de Progreso y Resultados",
        length="0",
        multiValued=0,
        containment="Not Specified",
        position="4",
        owner_class_name="TRAContribuciones",
        expression="context.fDeriveElementoProgreso()",
        computed_types="['TRAProgreso', ]"
    ),

    TextField(
        name='informeContribuciones',
        widget=TextAreaWidget(
            label="Informe de Contribuciones",
            label2="Contributions report",
            description="Informe de Contribuciones por Usuarios que traducen el catalogo,",
            description2="Report or the Contributions by Users translating the catalog.",
            label_msgid='gvSIGi18n_TRAContribuciones_attr_informeContribuciones_label',
            description_msgid='gvSIGi18n_TRAContribuciones_attr_informeContribuciones_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Informe de Contribuciones por Usuarios que traducen el catalogo,",
        duplicates="0",
        label2="Contributions report",
        ea_localid="2069",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Report or the Contributions by Users translating the catalog.",
        ea_guid="{E19682D8-03A3-40c2-A5D6-52F088221EEC}",
        read_only="True",
        scale="0",
        exclude_from_views="[ 'Textual',   'General', ]",
        label="Informe de Contribuciones",
        length="0",
        containment="Not Specified",
        position="1",
        owner_class_name="TRAContribuciones",
        custom_presentation_view="TRAInformeContribuciones_CustomView"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAContribuciones_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAContribuciones_Operaciones, 'schema', Schema(())).copy() + \
    getattr(TRAArquetipo, 'schema', Schema(())).copy() + \
    getattr(TRAConRegistroActividad, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAContribuciones(OrderedBaseFolder, TRAContribuciones_Operaciones, TRAArquetipo, TRAConRegistroActividad):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAContribuciones_Operaciones,'__implements__',()),) + (getattr(TRAArquetipo,'__implements__',()),) + (getattr(TRAConRegistroActividad,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Informe de Contribuciones'

    meta_type = 'TRAContribuciones'
    portal_type = 'TRAContribuciones'


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

    allowed_content_types = [] + list(getattr(TRAContribuciones_Operaciones, 'allowed_content_types', [])) + list(getattr(TRAArquetipo, 'allowed_content_types', [])) + list(getattr(TRAConRegistroActividad, 'allowed_content_types', []))
    filter_content_types             = 1
    global_allow                     = 0
    content_icon = 'tracontribuciones.gif'
    immediate_view                   = 'Tabular'
    default_view                     = 'Tabular'
    suppl_views                      = ['Tabular',]
    typeDescription                  = "Informe de Contribuciones por Usuarios a la traduccion del catalogo"
    typeDescMsgId                    =  'gvSIGi18n_TRAContribuciones_help'
    archetype_name2                  = 'Contributions Report'
    typeDescription2                 = '''Report on Contributions by Users  to the translation of the catalog'''
    archetype_name_msgid             = 'gvSIGi18n_TRAContribuciones_label'
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
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Edit_TRAContribuciones')"""
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

    schema = TRAContribuciones_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

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

    security.declarePublic('fExtraLinks')
    def fExtraLinks(self):
        """
        """
        
        return TRAContribuciones_Operaciones.fExtraLinks( self)

    security.declarePublic('cb_isCopyable')
    def cb_isCopyable(self):
        """
        """
        
        return False
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata', 'sharing', 'folderContents']:
            a['visible'] = 0
    return fti

registerType(TRAContribuciones, PROJECTNAME)
# end of class TRAContribuciones

##code-section module-footer #fill in your manual code here
##/code-section module-footer



