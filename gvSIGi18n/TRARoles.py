# -*- coding: utf-8 -*-
#
# File: TRARoles.py
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

__author__ = """Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana <gvSIGi18n@gvSIG.org>, 
Model Driven Development sl <gvSIGi18n@ModelDD.org>, 
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'



# ACV 200905280016 unused
#from Products.CMFCore.permissions import setDefaultRoles
from AccessControl import ModuleSecurityInfo


security = ModuleSecurityInfo('Products.gvSIGi18n.TRARoles')



security.declarePublic('cTRAManager_role')
security.declarePublic('cTRACoordinator_role')
security.declarePublic('cTRAVisitor_role')
security.declarePublic('cTRATranslator_role')
security.declarePublic('cTRAReviewer_role')
security.declarePublic('TRARoles_list')


cTRAManager_role        = 'TRAManager'
cTRACoordinator_role    = 'TRACoordinator'
cTRADeveloper_role      = 'TRADeveloper'
cTRAReviewer_role       = 'TRAReviewer'
cTRATranslator_role     = 'TRATranslator'
cTRAVisitor_role        = 'TRAVisitor'



TRARoles_list = [
    cTRAManager_role,
    cTRACoordinator_role,    
    cTRADeveloper_role,
    cTRAReviewer_role,
    cTRATranslator_role,
    cTRAVisitor_role,
]


