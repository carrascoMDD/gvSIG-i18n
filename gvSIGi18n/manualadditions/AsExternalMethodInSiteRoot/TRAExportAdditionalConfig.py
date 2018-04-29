# -*- coding: utf-8 -*-
#
# File: TRAExportAdditionalConfig.py
#
# Copyright (c) 2008, 2009 by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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
# Authors: 
# Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana (Spain) <gvSIGi18n@gvSIG.org>  
# Model Driven Development sl  Valencia (Spain) <http://www.ModelDD.org> 
# Antonio Carrasco Valero                       <carrasco@ModelDD.org>
#
#
__author__ = """Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana <gvSIGi18n@gvSIG.org>, 
Model Driven Development sl <gvSIGi18n@ModelDD.org>, 
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'


from StringIO import StringIO

from Products.CMFCore.utils import getToolByName


from Acquisition import aq_get


# #######################################
"""BEGIN ACV patch for v.1.2.1 20110125
The file has been created speficically for this patch, and should not be present in any 2.x version.

"""



def TRAExportAdditionalConfig( theContextualElement=None):

    if theContextualElement == None:
        return None
    
    anExportAdditionalConfig = {
        'export_status':         True,
        'export_modules':        True,
        'export_contributions':  True,
        'module_replacements': {
            'base':           'gvSIGdesktop',
            'gvSIG':          'gvSIGdesktop',
            'Czech_cs':       '',
            'Romanian_(ro)':  '',
            'instalador':     'gvSIGdesktopInstaller',
            'installer':      'gvSIGdesktopInstaller',
        },
        'user_replacements':   {
            'mcarrera':      'mcarrera',
            'vacevedo':      'mcarrera',
            'tcarrasco':     'mcarrera',
            'carrascoMDDsl': 'mcarrera',
        },
    }
    
    return anExportAdditionalConfig


# #######################################
"""END ACV patch 20110125

"""
