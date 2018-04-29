# -*- coding: utf-8 -*-
#
# File: TRAElemento.py
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
from TRAElemento_MappingConfig import TRAElemento_MappingConfig
from TRAElemento_Rendering import TRAElemento_Rendering
from TRAElemento_ResetPermissions import TRAElemento_ResetPermissions
from TRAElemento_GenericAccessors import TRAElemento_GenericAccessors
from TRAElemento_ExportConfig import TRAElemento_ExportConfig
from TRAElemento_Permissions import TRAElemento_Permissions
from TRAElemento_Encoding import TRAElemento_Encoding
from TRAElemento_Cache import TRAElemento_Cache
from TRAElemento_Profiling import TRAElemento_Profiling
from TRAElemento_ContainmentTree import TRAElemento_ContainmentTree
from TRAElemento_VoidResults import TRAElemento_VoidResults
from TRAElemento_Internationalization import TRAElemento_Internationalization
from TRAElemento_ConversionUtils import TRAElemento_ConversionUtils
from TRAElemento_MDDTool import TRAElemento_MDDTool
from TRAElemento_DatesAndTime import TRAElemento_DatesAndTime
from TRAElemento_Credits import TRAElemento_Credits
from TRAElemento_CopyConfig import TRAElemento_CopyConfig
from TRAElemento_VerifyPermissions import TRAElemento_VerifyPermissions
from TRAElemento_PloneTools import TRAElemento_PloneTools
from TRAElemento_Meta import TRAElemento_Meta
from TRAElemento_HTTP import TRAElemento_HTTP
from TRAElemento_Inventory import TRAElemento_Inventory
from TRAElemento_TraversalConfigurations import TRAElemento_TraversalConfigurations
from TRAElemento_UsersAndGroupsUtils import TRAElemento_UsersAndGroupsUtils
from TRAElemento_TraversalConfig import TRAElemento_TraversalConfig
from TRAElemento_Log import TRAElemento_Log
from TRAElemento_Operaciones import TRAElemento_Operaciones
from TRAElemento_FactoryUtils import TRAElemento_FactoryUtils
from Products.ATContentTypes.content.base import ATCTMixin
from TRAElemento_LanguagesUtils import TRAElemento_LanguagesUtils
from TRAElemento_PloneHandlers import TRAElemento_PloneHandlers
from TRAElemento_Recatalog import TRAElemento_Recatalog
from Products.ATContentTypes.content.document import ATDocument
from Products.ATContentTypes.content.base import updateAliases
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Acquisition  import aq_inner, aq_parent
from Products.CMFCore.utils  import getToolByName

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    ComputedField(
        name='archivos',
        widget=ComputedWidget(
            label="Ficheros",
            label2="Files",
            description="Elementos Plone convencionales conteniendo un Fichero de contenido arbitrario.",
            description2="Conventional Plone elements containing a File of arbitrary contents.",
            label_msgid='gvSIGi18n_TRAElemento_contents_archivos_label',
            description_msgid='gvSIGi18n_TRAElemento_contents_archivos_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=False,
        label2='Files',
        label='Ficheros',
        represents_aggregation=True,
        description2='Conventional Plone elements containing a File of arbitrary contents.',
        multiValued=1,
        owner_class_name="TRAElemento",
        expression="context.objectValues(['ATFile'])",
        computed_types=['ATFile'],
        non_framework_elements=False,
        description='Elementos Plone convencionales conteniendo un Fichero de contenido arbitrario.'
    ),

    ComputedField(
        name='documentos',
        widget=ComputedWidget(
            label="Documentos",
            label2="Documents",
            description="Elementos del tipo documento convencional en Plone.",
            description2="Elements of the Plone Document type.",
            label_msgid='gvSIGi18n_TRAElemento_contents_documentos_label',
            description_msgid='gvSIGi18n_TRAElemento_contents_documentos_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=False,
        label2='Documents',
        label='Documentos',
        represents_aggregation=True,
        description2='Elements of the Plone Document type.',
        multiValued=1,
        owner_class_name="TRAElemento",
        expression="context.objectValues(['ATDocument'])",
        computed_types=['ATDocument'],
        non_framework_elements=False,
        description='Elementos del tipo documento convencional en Plone.'
    ),

    ComputedField(
        name='enlaces',
        widget=ComputedWidget(
            label="Enlace",
            label2="Link",
            description="Elementos Plone conteniendo una referencia a una pagina Web (URLs como http://www.gvSIG.org)",
            description2="Plone Elements containing a reference to a Web page (URLs like http://www.gvSIG.org)",
            label_msgid='gvSIGi18n_TRAElemento_contents_enlaces_label',
            description_msgid='gvSIGi18n_TRAElemento_contents_enlaces_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=False,
        label2='Link',
        label='Enlace',
        represents_aggregation=True,
        description2='Plone Elements containing a reference to a Web page (URLs like http://www.gvSIG.org)',
        multiValued=1,
        owner_class_name="TRAElemento",
        expression="context.objectValues(['ATLink'])",
        computed_types=['ATLink'],
        non_framework_elements=False,
        description='Elementos Plone conteniendo una referencia a una pagina Web (URLs como http://www.gvSIG.org)'
    ),

    ComputedField(
        name='imagenes',
        widget=ComputedWidget(
            label="Imagenes",
            label2="Images",
            description="Elementos Plone convencionales conteniendo una Imagen.",
            description2="Conventional Plone elements containing an Image.",
            label_msgid='gvSIGi18n_TRAElemento_contents_imagenes_label',
            description_msgid='gvSIGi18n_TRAElemento_contents_imagenes_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=False,
        label2='Images',
        label='Imagenes',
        represents_aggregation=True,
        description2='Conventional Plone elements containing an Image.',
        multiValued=1,
        owner_class_name="TRAElemento",
        expression="context.objectValues(['ATImage'])",
        computed_types=['ATImage'],
        non_framework_elements=True,
        description='Elementos Plone convencionales conteniendo una Imagen.'
    ),

    ComputedField(
        name='noticias',
        widget=ComputedWidget(
            label="Noticias",
            label2="News Items",
            description="Elementos de Plone conteniendo una Noticia.",
            description2="Plone Elements containing a news posting.",
            label_msgid='gvSIGi18n_TRAElemento_contents_noticias_label',
            description_msgid='gvSIGi18n_TRAElemento_contents_noticias_help',
            i18n_domain='gvSIGi18n',
        ),
        contains_collections=False,
        label2='News Items',
        label='Noticias',
        represents_aggregation=True,
        description2='Plone Elements containing a news posting.',
        multiValued=1,
        owner_class_name="TRAElemento",
        expression="context.objectValues(['ATNewsItem'])",
        computed_types=['ATNewsItem'],
        non_framework_elements=False,
        description='Elementos de Plone conteniendo una Noticia.'
    ),

    TextField(
        name='text',
        widget=TextAreaWidget(
            label="Texto",
            label2="Text",
            description="Una descripcion textual extensa del elemento.",
            description2="Extended textual description of the element.",
            label_msgid='gvSIGi18n_TRAElemento_attr_text_label',
            description_msgid='gvSIGi18n_TRAElemento_attr_text_help',
            i18n_domain='gvSIGi18n',
        ),
        scale="0",
        description="Una descripcion textual extensa del elemento.",
        duplicates="0",
        label2="Text",
        ea_localid="248",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        length="0",
        description2="Extended textual description of the element.",
        containment="Not Specified",
        ea_guid="{EEA3C90B-1EF9-4097-9764-5F5C490F47B8}",
        position="0",
        owner_class_name="TRAElemento",
        label="Texto"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAElemento_schema = getattr(TRAElemento_MappingConfig, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_Rendering, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_ResetPermissions, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_GenericAccessors, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_ExportConfig, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_Permissions, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_Encoding, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_Cache, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_Profiling, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_ContainmentTree, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_VoidResults, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_Internationalization, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_ConversionUtils, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_MDDTool, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_DatesAndTime, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_Credits, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_CopyConfig, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_VerifyPermissions, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_PloneTools, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_Meta, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_HTTP, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_Inventory, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_TraversalConfigurations, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_UsersAndGroupsUtils, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_TraversalConfig, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_Log, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_Operaciones, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_FactoryUtils, 'schema', Schema(())).copy() + \
    getattr(ATCTMixin, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_LanguagesUtils, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_PloneHandlers, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_Recatalog, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAElemento(TRAElemento_MappingConfig, TRAElemento_Rendering, TRAElemento_ResetPermissions, TRAElemento_GenericAccessors, TRAElemento_ExportConfig, TRAElemento_Permissions, TRAElemento_Encoding, TRAElemento_Cache, TRAElemento_Profiling, TRAElemento_ContainmentTree, TRAElemento_VoidResults, TRAElemento_Internationalization, TRAElemento_ConversionUtils, TRAElemento_MDDTool, TRAElemento_DatesAndTime, TRAElemento_Credits, TRAElemento_CopyConfig, TRAElemento_VerifyPermissions, TRAElemento_PloneTools, TRAElemento_Meta, TRAElemento_HTTP, TRAElemento_Inventory, TRAElemento_TraversalConfigurations, TRAElemento_UsersAndGroupsUtils, TRAElemento_TraversalConfig, TRAElemento_Log, TRAElemento_Operaciones, TRAElemento_FactoryUtils, ATCTMixin, TRAElemento_LanguagesUtils, TRAElemento_PloneHandlers, TRAElemento_Recatalog):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(TRAElemento_MappingConfig,'__implements__',()),) + (getattr(TRAElemento_Rendering,'__implements__',()),) + (getattr(TRAElemento_ResetPermissions,'__implements__',()),) + (getattr(TRAElemento_GenericAccessors,'__implements__',()),) + (getattr(TRAElemento_ExportConfig,'__implements__',()),) + (getattr(TRAElemento_Permissions,'__implements__',()),) + (getattr(TRAElemento_Encoding,'__implements__',()),) + (getattr(TRAElemento_Cache,'__implements__',()),) + (getattr(TRAElemento_Profiling,'__implements__',()),) + (getattr(TRAElemento_ContainmentTree,'__implements__',()),) + (getattr(TRAElemento_VoidResults,'__implements__',()),) + (getattr(TRAElemento_Internationalization,'__implements__',()),) + (getattr(TRAElemento_ConversionUtils,'__implements__',()),) + (getattr(TRAElemento_MDDTool,'__implements__',()),) + (getattr(TRAElemento_DatesAndTime,'__implements__',()),) + (getattr(TRAElemento_Credits,'__implements__',()),) + (getattr(TRAElemento_CopyConfig,'__implements__',()),) + (getattr(TRAElemento_VerifyPermissions,'__implements__',()),) + (getattr(TRAElemento_PloneTools,'__implements__',()),) + (getattr(TRAElemento_Meta,'__implements__',()),) + (getattr(TRAElemento_HTTP,'__implements__',()),) + (getattr(TRAElemento_Inventory,'__implements__',()),) + (getattr(TRAElemento_TraversalConfigurations,'__implements__',()),) + (getattr(TRAElemento_UsersAndGroupsUtils,'__implements__',()),) + (getattr(TRAElemento_TraversalConfig,'__implements__',()),) + (getattr(TRAElemento_Log,'__implements__',()),) + (getattr(TRAElemento_Operaciones,'__implements__',()),) + (getattr(TRAElemento_FactoryUtils,'__implements__',()),) + (getattr(ATCTMixin,'__implements__',()),) + (getattr(TRAElemento_LanguagesUtils,'__implements__',()),) + (getattr(TRAElemento_PloneHandlers,'__implements__',()),) + (getattr(TRAElemento_Recatalog,'__implements__',()),)

    allowed_content_types = ['Image', 'Document', 'File', 'Link', 'News Item'] + list(getattr(TRAElemento_MappingConfig, 'allowed_content_types', [])) + list(getattr(TRAElemento_Rendering, 'allowed_content_types', [])) + list(getattr(TRAElemento_ResetPermissions, 'allowed_content_types', [])) + list(getattr(TRAElemento_GenericAccessors, 'allowed_content_types', [])) + list(getattr(TRAElemento_ExportConfig, 'allowed_content_types', [])) + list(getattr(TRAElemento_Permissions, 'allowed_content_types', [])) + list(getattr(TRAElemento_Encoding, 'allowed_content_types', [])) + list(getattr(TRAElemento_Cache, 'allowed_content_types', [])) + list(getattr(TRAElemento_Profiling, 'allowed_content_types', [])) + list(getattr(TRAElemento_ContainmentTree, 'allowed_content_types', [])) + list(getattr(TRAElemento_VoidResults, 'allowed_content_types', [])) + list(getattr(TRAElemento_Internationalization, 'allowed_content_types', [])) + list(getattr(TRAElemento_ConversionUtils, 'allowed_content_types', [])) + list(getattr(TRAElemento_MDDTool, 'allowed_content_types', [])) + list(getattr(TRAElemento_DatesAndTime, 'allowed_content_types', [])) + list(getattr(TRAElemento_Credits, 'allowed_content_types', [])) + list(getattr(TRAElemento_CopyConfig, 'allowed_content_types', [])) + list(getattr(TRAElemento_VerifyPermissions, 'allowed_content_types', [])) + list(getattr(TRAElemento_PloneTools, 'allowed_content_types', [])) + list(getattr(TRAElemento_Meta, 'allowed_content_types', [])) + list(getattr(TRAElemento_HTTP, 'allowed_content_types', [])) + list(getattr(TRAElemento_Inventory, 'allowed_content_types', [])) + list(getattr(TRAElemento_TraversalConfigurations, 'allowed_content_types', [])) + list(getattr(TRAElemento_UsersAndGroupsUtils, 'allowed_content_types', [])) + list(getattr(TRAElemento_TraversalConfig, 'allowed_content_types', [])) + list(getattr(TRAElemento_Log, 'allowed_content_types', [])) + list(getattr(TRAElemento_Operaciones, 'allowed_content_types', [])) + list(getattr(TRAElemento_FactoryUtils, 'allowed_content_types', [])) + list(getattr(ATCTMixin, 'allowed_content_types', [])) + list(getattr(TRAElemento_LanguagesUtils, 'allowed_content_types', [])) + list(getattr(TRAElemento_PloneHandlers, 'allowed_content_types', [])) + list(getattr(TRAElemento_Recatalog, 'allowed_content_types', []))

    aliases = updateAliases( ATDocument, {'folder_factories':'Tabular','cut':'Tabular','object_cut':'Tabular','delete_confirmation': 'Eliminar','object_rename': 'Editar','content_status_modify':'Tabular','content_status_history':'Tabular','placeful_workflow_configuration': 'Tabular',})

    _at_rename_after_creation = True

    schema = TRAElemento_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('CookedBody')
    def CookedBody(self,setlevel=0,stx_level=None):
        """
        """
        
        return getToolByName( self, 'MDDModelDDvlPlone_tool').fCookedBodyForElement( None, self, stx_level, setlevel, None)

    security.declarePublic('fAllowEditId')
    def fAllowEditId(self):
        """
        """
        
        return False

    security.declarePublic('fAllowPaste')
    def fAllowPaste(self):
        """
        """
        
        return False

    security.declarePublic('fAllowRead')
    def fAllowRead(self):
        """
        """
        
        return True

    security.declarePublic('fIsCacheable')
    def fIsCacheable(self):
        """
        """
        
        return False

    security.declarePublic('fAllowWrite')
    def fAllowWrite(self):
        """
        """
        
        return self.fAllowRead() and self.getCatalogo().getPermiteModificar()

    security.declarePublic('getContenedor')
    def getContenedor(self):
        """
        """
        
        return aq_parent( aq_inner( self))

    security.declarePublic('getContenedorContenedor')
    def getContenedorContenedor(self):
        """
        """
        
        return aq_parent( aq_parent( aq_inner( self)))

    security.declarePublic('getEditableBody')
    def getEditableBody(self):
        """
        """
        
        return getToolByName( self, 'ModelDDvlPlone_tool').fEditableBodyForElement( None, self, None)

    security.declarePublic('getEsColeccion')
    def getEsColeccion(self):
        """
        """
        
        return False

    security.declarePublic('getEsRaiz')
    def getEsRaiz(self):
        """
        """
        
        return not aq_parent( aq_inner( self)) or (self.meta_type == "TRACatalogo")

    security.declarePublic('getNombreProyecto')
    def getNombreProyecto(self):
        """
        """
        
        return 'gvSIGi18n'

    security.declarePublic('getProductPrefix')
    def getProductPrefix(self):
        """
        """
        
        return "TRA"

    security.declarePublic('manage_afterAdd')
    def manage_afterAdd(self,item,container):
        """
        """
        
        return TRAElemento_PloneHandlers.pHandle_manage_afterAdd( self, item, container)

    security.declarePublic('manage_beforeDelete')
    def manage_beforeDelete(self,item,container):
        """
        """
        
        return TRAElemento_PloneHandlers.pHandle_manage_beforeDelete( self, item, container)

    security.declarePublic('getAddableTypesInMenu')
    def getAddableTypesInMenu(self,theTypes):
        """
        """
        
        return []
# end of class TRAElemento

##code-section module-footer #fill in your manual code here
##/code-section module-footer



