# -*- coding: utf-8 -*-
#
# File: TRAElemento_CopyConfig.py
#
# Copyright (c) 2010 by 2008, 2009, 2010 Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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
# Authors: 
# Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana, Model Driven Development sl, Antonio Carrasco Valero
#
#

__author__ = """Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana <gvSIGi18n@gvSIG.org>, 
Model Driven Development sl <gvSIGi18n@ModelDD.org>,
Antonio Carrasco Valero <carrasco@ModelDD.org>"""

__docformat__ = 'plaintext'

from AccessControl                  import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.gvSIGi18n.config import *



class TRAElemento_CopyConfig:            

    """
    """
    security = ClassSecurityInfo()
    
    
    security.declarePublic('copyConfig')
    def copyConfig( self):
        return []
    
    
    