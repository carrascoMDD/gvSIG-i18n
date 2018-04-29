# -*- coding: utf-8 -*-
#
# File: TRAContenidoXML.py
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
from TRAContenidoXML_Operaciones import TRAContenidoXML_Operaciones
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from TRAElemento_Operaciones import TRAElemento_Operaciones

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
            label_msgid='gvSIGi18n_TRAContenidoXML_attr_excluirDeImportacion_label',
            description_msgid='gvSIGi18n_TRAContenidoXML_attr_excluirDeImportacion_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Verdadero, entonces este contenido de intercambio no se incluye en la importacion, ni en el sumario of vista detallada.",
        duplicates="0",
        label2="Exclude from Import",
        ea_localid="2045",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If True, then this translations interchange contents will not be included in the import process, the summary or the detailed view.",
        ea_guid="{CAB5B084-02B6-4ace-AB82-81B7CA0466B5}",
        scale="0",
        default="False",
        label="Excluir de Importacion",
        length="0",
        containment="Not Specified",
        position="1",
        owner_class_name="TRAContenidoXML"
    ),

    StringField(
        name='usuarioContribuidor',
        widget=StringWidget(
            label="Usuario Contribuidor",
            label2="Contributor User",
            description="Usuario que ha subido al servidor el archivo o fichero con contenido de intercambio de traducciones de cadenas a idiomas.",
            description2="User who uploaded the interchange content file or archive with string translations into languages.",
            label_msgid='gvSIGi18n_TRAContenidoXML_attr_usuarioContribuidor_label',
            description_msgid='gvSIGi18n_TRAContenidoXML_attr_usuarioContribuidor_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Usuario que ha subido al servidor el archivo o fichero con contenido de intercambio de traducciones de cadenas a idiomas.",
        duplicates="0",
        label2="Contributor User",
        ea_localid="2041",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="User who uploaded the interchange content file or archive with string translations into languages.",
        ea_guid="{6EBF6E5E-6714-437b-96F8-C9E812CBF10F}",
        read_only="True",
        scale="0",
        label="Usuario Contribuidor",
        length="0",
        containment="Not Specified",
        position="4",
        owner_class_name="TRAContenidoXML"
    ),

    DateTimeField(
        name='fechaContenido',
        widget=CalendarWidget(
            label="Fecha y Hora de Carga",
            label2="Upload Date and Time",
            description="Fecha y hora en que  completo o termino el proceso de carga del contenido de intercambio de traducciones.",
            description2="Date and Time when the process to  analise translations interchange archives was completed or terminated.",
            label_msgid='gvSIGi18n_TRAContenidoXML_attr_fechaContenido_label',
            description_msgid='gvSIGi18n_TRAContenidoXML_attr_fechaContenido_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Fecha y hora en que  completo o termino el proceso de carga del contenido de intercambio de traducciones.",
        duplicates="0",
        label2="Upload Date and Time",
        ea_localid="2040",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Date and Time when the process to  analise translations interchange archives was completed or terminated.",
        ea_guid="{6D3E313E-C9ED-48fe-80F6-F038BA70D1AB}",
        read_only="True",
        scale="0",
        label="Fecha y Hora de Carga",
        length="0",
        containment="Not Specified",
        position="2",
        owner_class_name="TRAContenidoXML"
    ),

    StringField(
        name='ficheroLeido',
        widget=StringWidget(
            label="Fichero leido",
            label2="File read",
            description="El nombre del fichero de intercambio del contenido de traducciones de cadenas a idiomas.",
            description2="The name of the interchange content file with string translations into languages.",
            label_msgid='gvSIGi18n_TRAContenidoXML_attr_ficheroLeido_label',
            description_msgid='gvSIGi18n_TRAContenidoXML_attr_ficheroLeido_help',
            i18n_domain='gvSIGi18n',
        ),
        containment="Not Specified",
        description="El nombre del fichero de intercambio del contenido de traducciones de cadenas a idiomas.",
        duplicates="0",
        label2="File read",
        ea_localid="2047",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="The name of the interchange content file with string translations into languages.",
        ea_guid="{19A4678A-2DB3-45a1-9F46-73B4A4306DFD}",
        read_only="True",
        scale="0",
        label="Fichero leido",
        length="0",
        default_method="fGetMemberId_safe",
        position="3",
        owner_class_name="TRAContenidoXML"
    ),

    TextField(
        name='contenidoBinario',
        widget=TextAreaWidget(
            label="Contenido Binario (imagenes de banderas)",
            label2="Binary Contents (flag images)",
            description="Contenidos binarios como imagenes de banderas de idiomas, leidos desde una copia de seguridad de un catalogo de traducciones .",
            description2="Binary contents, like images for language flags, read from a backup file of a translations catalog.",
            label_msgid='gvSIGi18n_TRAContenidoXML_attr_contenidoBinario_label',
            description_msgid='gvSIGi18n_TRAContenidoXML_attr_contenidoBinario_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Contenidos binarios como imagenes de banderas de idiomas, leidos desde una copia de seguridad de un catalogo de traducciones .",
        duplicates="0",
        label2="Binary Contents (flag images)",
        ea_localid="2056",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Binary contents, like images for language flags, read from a backup file of a translations catalog.",
        ea_guid="{729F61B4-4046-4c19-A3ED-F92975554BD1}",
        read_only="True",
        scale="0",
        label="Contenido Binario (imagenes de banderas)",
        length="0",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        position="1",
        owner_class_name="TRAContenidoXML"
    ),

    TextField(
        name='contenidoXML',
        widget=TextAreaWidget(
            label="Contenido XML",
            label2="XML Contents",
            description="Contenido del fichero XML leido desde una copia de seguridad de un catalogo de traducciones .",
            description2="Contents of an XML file read from a backup of a translations catalog.",
            label_msgid='gvSIGi18n_TRAContenidoXML_attr_contenidoXML_label',
            description_msgid='gvSIGi18n_TRAContenidoXML_attr_contenidoXML_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Contenido del fichero XML leido desde una copia de seguridad de un catalogo de traducciones .",
        duplicates="0",
        label2="XML Contents",
        ea_localid="2055",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Contents of an XML file read from a backup of a translations catalog.",
        ea_guid="{70960AF6-6B99-4273-B136-2D4EADD3AA4A}",
        read_only="True",
        scale="0",
        label="Contenido XML",
        length="0",
        exclude_from_traversalconfig="True",
        containment="Not Specified",
        position="0",
        owner_class_name="TRAContenidoXML"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAContenidoXML_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAArquetipo, 'schema', Schema(())).copy() + \
    getattr(TRAConRegistroActividad, 'schema', Schema(())).copy() + \
    getattr(TRAContenidoXML_Operaciones, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAContenidoXML(OrderedBaseFolder, TRAArquetipo, TRAConRegistroActividad, TRAContenidoXML_Operaciones):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAArquetipo,'__implements__',()),) + (getattr(TRAConRegistroActividad,'__implements__',()),) + (getattr(TRAContenidoXML_Operaciones,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Contenido XML'

    meta_type = 'TRAContenidoXML'
    portal_type = 'TRAContenidoXML'


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

    allowed_content_types = [] + list(getattr(TRAArquetipo, 'allowed_content_types', [])) + list(getattr(TRAConRegistroActividad, 'allowed_content_types', [])) + list(getattr(TRAContenidoXML_Operaciones, 'allowed_content_types', []))
    filter_content_types             = 1
    global_allow                     = 0
    content_icon = 'tracontenidoxml.gif'
    immediate_view                   = 'Tabular'
    default_view                     = 'Tabular'
    suppl_views                      = ['Tabular',]
    typeDescription                  = "Contenido importado de un fichero XML de copia de seguridad de un catalogo de traducciones."
    typeDescMsgId                    =  'gvSIGi18n_TRAContenidoXML_help'
    archetype_name2                  = 'XML Content'
    typeDescription2                 = '''Contents imported from an XML backup file from a translations catalog.'''
    archetype_name_msgid             = 'gvSIGi18n_TRAContenidoXML_label'
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


       {'action': "string:${object_url}/TRAContenidoXML",
        'category': "object",
        'id': 'TRAContenidoXML',
        'name': 'XML Data',
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

    schema = TRAContenidoXML_schema

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
        
        return TRAContenidoXML_Operaciones.fExtraLinks( self)

    security.declarePublic('manage_afterAdd')
    def manage_afterAdd(self,item,container):
        """
        """
        
        return TRAContenidoXML_Operaciones.pHandle_manage_afterAdd( self, item, container)
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata', 'sharing', 'folderContents']:
            a['visible'] = 0
    return fti

registerType(TRAContenidoXML, PROJECTNAME)
# end of class TRAContenidoXML

##code-section module-footer #fill in your manual code here
##/code-section module-footer



