# -*- coding: utf-8 -*-
#
# File: gvSIGi18n.py
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


# There are three ways to inject custom code here:
#
#   - To set global configuration variables, create a file AppConfig.py.
#       This will be imported in config.py, which in turn is imported in
#       each generated class and in this file.
#   - To perform custom initialisation after types have been registered,
#       use the protected code section at the bottom of initialize().
#   - To register a customisation policy, create a file CustomizationPolicy.py
#       with a method register(context) to register the policy.

import logging
logger = logging.getLogger('gvSIGi18n')
logger.info('Installing Product')

try:
    import CustomizationPolicy
except ImportError:
    CustomizationPolicy = None

import os, os.path
from Globals import package_home
from Products.CMFCore import utils as cmfutils

try: # New CMF
    from Products.CMFCore import permissions as CMFCorePermissions 
except: # Old CMF
    from Products.CMFCore import CMFCorePermissions

from Products.CMFCore import DirectoryView
from Products.CMFPlone.utils import ToolInit
from Products.Archetypes.atapi import *
from Products.Archetypes import listTypes
from Products.Archetypes.utils import capitalize
from config import *

DirectoryView.registerDirectory('skins', product_globals)
DirectoryView.registerDirectory('skins/gvSIGi18n',
                                    product_globals)


##code-section custom-init-head #fill in your manual code here
##/code-section custom-init-head


def initialize(context):
    ##code-section custom-init-top #fill in your manual code here
    ##/code-section custom-init-top

    # imports packages and types for registration



    import TRAConfiguracion

    import TRAColeccionInformes

    import TRAArquetipo

    import TRAModulo

    import TRAColeccionCadenas

    import TRAProgreso

    import TRAInforme

    import TRAColeccionArquetipos

    import TRAParametrosControlProgreso

    import TRAContenidoXML

    import TRAColeccionImportaciones

    import TRACadena

    import TRAColeccionSolicitudesCadenas

    import TRAElemento

    import TRAConfiguracionSolicitudesCadenas

    import TRAConfiguracionPaginaTraducciones

    import TRASimbolosOrdenados

    import TRACatalogo

    import TRAColeccionIdiomas

    import TRAConfiguracionInvalidacionInformes

    import TRAConfiguracionVarios

    import TRAContenidoIntercambio

    import TRAConfiguracionImportacion

    import TRAConfiguracionExportacion

    import TRAConRegistroActividad

    import TRAImportacion

    import TRAIdioma

    import TRAColeccionModulos

    import TRATraduccion

    import TRAColeccionContribuciones

    import TRAColeccionProgresos

    import TRAConfiguracionPermisos

    import TRAContribuciones

    import TRAConfiguracionPerfilEjecucion

    import TRASolicitudCadena



    # Initialize portal content

    all_content_types, all_constructors, all_ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = all_content_types,
        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = all_constructors,
        fti                = all_ftis,
        ).initialize(context)

    # Give it some extra permissions to control them on a per class limit
    for i in range(0,len(all_content_types)):
        klassname=all_content_types[i].__name__
        if not klassname in ADD_CONTENT_PERMISSIONS:
            continue

        context.registerClass(meta_type   = all_ftis[i]['meta_type'],
                              constructors= (all_constructors[i],),
                              permission  = ADD_CONTENT_PERMISSIONS[klassname])


    # Apply customization-policy, if theres any
    if CustomizationPolicy and hasattr(CustomizationPolicy, 'register'):
        CustomizationPolicy.register(context)
        print 'Customization policy for gvSIGi18n installed'

    ##code-section custom-init-bottom #fill in your manual code here
    ##/code-section custom-init-bottom

