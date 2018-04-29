# -*- coding: utf-8 -*-
#
# File: TRARoles.py
#
# Copyright (c) 2008, 2009, 2010 by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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

# #########################################
"""Creation of new instances of TRACatalogo (the root element) requires the user to have been granted the 
"gvSIGi18n: Add TRACatalogo" permission on the containing folder.
This is achieved by granting to the TRACreator role 
    through the Zope Management Interface security tab of the containing folder  
    the permissions below:
    [   'ACI', perm_AccessContentsInformation,],
    [   'APC', permissions.AddPortalContent,],  
    [   'APF', permissions.AddPortalFolders,],  
    [   'CHP', permissions.ChangePermissions,],
    [   'DOB', permissions.DeleteObjects,],     
    [   'LFC', permissions.ListFolderContents,],
    [   'MGR', perm_ManageGroups, ],
    [   'MPR', permissions.ManageProperties,], 
    [   'MPC', permissions.ModifyPortalContent,],
    [   'VIE', permissions.View,],              
    [   'ADC', cPermission_gvSIGi18nAddTRACatalogo,],

The user that shall be able to create root catalogs in the containing folder
shall be assigned the in the containing folder the local role TRACreator 
by using the Plone sharing tab in the containing folder (must be logged as Manager).

"""


security.declarePublic('cTRACreator_role')
security.declarePublic('cTRAManager_role')
security.declarePublic('cTRACoordinator_role')
security.declarePublic('cTRAVisitor_role')
security.declarePublic('cTRATranslator_role')
security.declarePublic('cTRAReviewer_role')
security.declarePublic('TRARoles_list')


cTRACreator_role        = 'TRACreator'
cTRAManager_role        = 'TRAManager'
cTRACoordinator_role    = 'TRACoordinator'
cTRADeveloper_role      = 'TRADeveloper'
cTRAReviewer_role       = 'TRAReviewer'
cTRATranslator_role     = 'TRATranslator'
cTRAVisitor_role        = 'TRAVisitor'


TRARoles_list = [
    cTRACreator_role,
    cTRAManager_role,
    cTRACoordinator_role,    
    cTRADeveloper_role,
    cTRAReviewer_role,
    cTRATranslator_role,
    cTRAVisitor_role,
]



cZopeAnonymous_role     = 'Anonymous'
cZopeAuthenticated_role = 'Authenticated'
cZopeMember_role        = 'Member'
cZopeReviewer_role      = 'Reviewer'
cZopeOwner_role         = 'Owner'
cZopeManager_role       = 'Manager'


cZopeRoles_list = [
    cZopeManager_role,
    cZopeOwner_role,
    cZopeReviewer_role,
    cZopeMember_role,    
    cZopeAuthenticated_role,
    cZopeAnonymous_role,
]


cZopeManagerAndOwnerRoles = [ cZopeManager_role, cZopeOwner_role,]
