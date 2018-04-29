# -*- coding: utf-8 -*-
#
# File: TRAElemento.py
#
# Copyright (c) 2009 by Conselleria de Infraestructuras y Transporte de la
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
from Products.gvSIGi18n.TRAElemento_MappingConfig import TRAElemento_MappingConfig
from Products.gvSIGi18n.TRAElemento_ExportConfig import TRAElemento_ExportConfig
from Products.gvSIGi18n.TRAElemento_CopyConfig import TRAElemento_CopyConfig
from TRAElemento_Meta import TRAElemento_Meta
from TRAElemento_TraversalConfig import TRAElemento_TraversalConfig
from TRAElemento_Operaciones import TRAElemento_Operaciones
from Products.ATContentTypes.content.base import ATCTMixin
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Acquisition  import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName
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
        expression="context.objectValues(['File'])",
        computed_types=['File'],
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
        expression="context.objectValues(['Document'])",
        computed_types=['Document'],
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
        expression="context.objectValues(['Link'])",
        computed_types=['Link'],
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
        expression="context.objectValues(['Image'])",
        computed_types=['Image'],
        non_framework_elements=False,
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
        expression="context.objectValues(['News_Item'])",
        computed_types=['News_Item'],
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
    getattr(TRAElemento_ExportConfig, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_CopyConfig, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_Meta, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_TraversalConfig, 'schema', Schema(())).copy() + \
    getattr(TRAElemento_Operaciones, 'schema', Schema(())).copy() + \
    getattr(ATCTMixin, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAElemento(TRAElemento_MappingConfig, TRAElemento_ExportConfig, TRAElemento_CopyConfig, TRAElemento_Meta, TRAElemento_TraversalConfig, TRAElemento_Operaciones, ATCTMixin):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(TRAElemento_MappingConfig,'__implements__',()),) + (getattr(TRAElemento_ExportConfig,'__implements__',()),) + (getattr(TRAElemento_CopyConfig,'__implements__',()),) + (getattr(TRAElemento_Meta,'__implements__',()),) + (getattr(TRAElemento_TraversalConfig,'__implements__',()),) + (getattr(TRAElemento_Operaciones,'__implements__',()),) + (getattr(ATCTMixin,'__implements__',()),)

    allowed_content_types = ['Image', 'Document', 'File', 'Link', 'News Item'] + list(getattr(TRAElemento_MappingConfig, 'allowed_content_types', [])) + list(getattr(TRAElemento_ExportConfig, 'allowed_content_types', [])) + list(getattr(TRAElemento_CopyConfig, 'allowed_content_types', [])) + list(getattr(TRAElemento_Meta, 'allowed_content_types', [])) + list(getattr(TRAElemento_TraversalConfig, 'allowed_content_types', [])) + list(getattr(TRAElemento_Operaciones, 'allowed_content_types', [])) + list(getattr(ATCTMixin, 'allowed_content_types', []))
    _at_rename_after_creation = True

    schema = TRAElemento_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('CookedBody')
    def CookedBody(self,setlevel=0,stx_level=None):
        """
        """
        
        return getToolByName( self, 'ModelDDvlPlone_tool').fCookedBodyForElement( None, self, stx_level, setlevel, None)

    security.declarePublic('fAllowPaste')
    def fAllowPaste(self):
        """
        """
        
        return False

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
        
        return TRAElemento_Operaciones.pHandle_manage_afterAdd( self, item, container)

    security.declarePublic('manage_beforeDelete')
    def manage_beforeDelete(self,item,container):
        """
        """
        
        return TRAElemento_Operaciones.pHandle_manage_beforeDelete( self, item, container)
# end of class TRAElemento

##code-section module-footer #fill in your manual code here
##/code-section module-footer



