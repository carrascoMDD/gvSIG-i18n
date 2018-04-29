# -*- coding: utf-8 -*-
#
# File: TRAgvSIGi18nTool.py
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




from AccessControl import ClassSecurityInfo


from Products.CMFCore                    import permissions


from Products.CMFCore.utils              import UniqueObject
from OFS.PropertyManager                 import PropertyManager
from OFS                                 import SimpleItem
from Products.CMFCore.ActionProviderBase import ActionProviderBase


from Products.PageTemplates.PageTemplateFile import PageTemplateFile


from TRAgvSIGi18nTool_Constants import *


from TRAgvSIGi18nTool_Cache           import TRAgvSIGi18nTool_Cache
from TRAgvSIGi18nTool_Catalog         import TRAgvSIGi18nTool_Catalog
from TRAgvSIGi18nTool_Configurations  import TRAgvSIGi18nTool_Configurations
from TRAgvSIGi18nTool_Contributions   import TRAgvSIGi18nTool_Contributions
from TRAgvSIGi18nTool_Credits         import TRAgvSIGi18nTool_Credits
from TRAgvSIGi18nTool_Dates           import TRAgvSIGi18nTool_Dates
from TRAgvSIGi18nTool_Element         import TRAgvSIGi18nTool_Element
from TRAgvSIGi18nTool_Encoding        import TRAgvSIGi18nTool_Encoding
from TRAgvSIGi18nTool_Export          import TRAgvSIGi18nTool_Export
from TRAgvSIGi18nTool_HTTP            import TRAgvSIGi18nTool_HTTP
from TRAgvSIGi18nTool_Import          import TRAgvSIGi18nTool_Import
from TRAgvSIGi18nTool_Languages       import TRAgvSIGi18nTool_Languages
from TRAgvSIGi18nTool_Localization    import TRAgvSIGi18nTool_Localization
from TRAgvSIGi18nTool_Maintenance     import TRAgvSIGi18nTool_Maintenance
from TRAgvSIGi18nTool_Modules         import TRAgvSIGi18nTool_Modules
from TRAgvSIGi18nTool_Permissions     import TRAgvSIGi18nTool_Permissions
from TRAgvSIGi18nTool_Plone           import TRAgvSIGi18nTool_Plone
from TRAgvSIGi18nTool_Profiling       import TRAgvSIGi18nTool_Profiling
from TRAgvSIGi18nTool_Progress        import TRAgvSIGi18nTool_Progress
from TRAgvSIGi18nTool_Reports         import TRAgvSIGi18nTool_Reports
from TRAgvSIGi18nTool_Status          import TRAgvSIGi18nTool_Status
from TRAgvSIGi18nTool_StringRequests  import TRAgvSIGi18nTool_StringRequests
from TRAgvSIGi18nTool_Translations    import TRAgvSIGi18nTool_Translations
from TRAgvSIGi18nTool_Utils           import TRAgvSIGi18nTool_Utils




# #######################################################
"""Tool permissions to be set upon instantiation of the tool,  not restricting the access of anonymous users.

"""         
cTRAgvSIGi18nToolPermissions = [                                                                                                                                     
    { 'permission': permissions.ManagePortal,         'acquire': True,  'roles': [              'Manager', ], },                             
    { 'permission': permissions.ManageProperties,     'acquire': True,  'roles': [              'Authenticated', ], }, 
    { 'permission': permissions.DeleteObjects,        'acquire': True,  'roles': [              'Authenticated', ], }, 
    { 'permission': permissions.View,                 'acquire': True,  'roles': [ 'Anonymous', 'Authenticated', ], },  
    { 'permission': perm_AccessContentsInformation,   'acquire': True,  'roles': [ 'Anonymous', 'Authenticated', ], },  
]





class TRAgvSIGi18nTool( UniqueObject, PropertyManager, SimpleItem.SimpleItem, ActionProviderBase, \
    TRAgvSIGi18nTool_Cache, \
    TRAgvSIGi18nTool_Catalog, \
    TRAgvSIGi18nTool_Configurations, \
    TRAgvSIGi18nTool_Contributions, \
    TRAgvSIGi18nTool_Credits, \
    TRAgvSIGi18nTool_Dates, \
    TRAgvSIGi18nTool_Element, \
    TRAgvSIGi18nTool_Encoding, \
    TRAgvSIGi18nTool_Export, \
    TRAgvSIGi18nTool_HTTP, \
    TRAgvSIGi18nTool_Import, \
    TRAgvSIGi18nTool_Languages, \
    TRAgvSIGi18nTool_Localization, \
    TRAgvSIGi18nTool_Maintenance, \
    TRAgvSIGi18nTool_Modules, \
    TRAgvSIGi18nTool_Permissions, \
    TRAgvSIGi18nTool_Plone, \
    TRAgvSIGi18nTool_Profiling, \
    TRAgvSIGi18nTool_Progress, \
    TRAgvSIGi18nTool_Reports, \
    TRAgvSIGi18nTool_Status, \
    TRAgvSIGi18nTool_StringRequests, \
    TRAgvSIGi18nTool_Translations, \
    TRAgvSIGi18nTool_Utils,\
    ):
    """Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations..
    
    """

              
        
    
    "The TRAgvSIGi18nTool"

    meta_type = 'TRAgvSIGi18nTool'

    id = cTRAgvSIGi18nToolId

    manage_options = PropertyManager.manage_options + \
                     SimpleItem.SimpleItem.manage_options + (
    	{'label': 'View', 'action': 'index_html',},
    )

    _properties = (
        {'id':'title', 'type':'string', 'mode':'w'},
    )

    # Standard security settings
    security = ClassSecurityInfo()


    security.declareProtected('Manage properties', 'index_html')
    index_html = PageTemplateFile('skins/index_html', globals())

    


    
    
    # ##########################################################
    """Initialization methods for the tool singleton.
    
    """

    
    
    security.declarePublic('manage_afterAdd')
    def manage_afterAdd(self,item,container):
        """Initialization of the tool.
        
        """        
        self.pSetPermissions()
                
        return self
    

    
    
    
    
    security.declarePrivate( 'pSetPermissions')
    def pSetPermissions(self):
        """Set tool permissions upon instantiation of the tool, according to a specification ( usually not restricting the access of anonymous users).
        
        """         
        for unaPermissionSpec in cTRAgvSIGi18nToolPermissions:
            unaPermission = unaPermissionSpec[ 'permission']
            unAcquire     = unaPermissionSpec[ 'acquire'] 
            unosRoles     = unaPermissionSpec[ 'roles']
            
            if unaPermission:
                self.manage_permission( unaPermission, roles=unosRoles, acquire=unAcquire)
        
        return self
        
   
    
    
    
    
    
    # ##########################################################
    """Boundary methods (facade) implemented in TRAgvSIGi18n_Xxxx super classes.
    
    """

    
    
 
    
     

# ####################################################
"""Constructor methods, only used when adding class to objectManager.

"""

def manage_addAction(self, REQUEST=None):
    "Add tool instance to parent ObjectManager"
    id = TRAgvSIGi18nTool.id
    self._setObject(id, TRAgvSIGi18nTool())
    if REQUEST is not None:
        return self.manage_main(self, REQUEST)

constructors = (manage_addAction,)



