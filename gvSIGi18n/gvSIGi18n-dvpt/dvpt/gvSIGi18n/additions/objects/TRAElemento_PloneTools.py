# -*- coding: utf-8 -*-
#
# File: TRAElemento_PloneTools.py
#
# Copyright (c) 2008, 2009, 2010, 2011  by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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


from AccessControl              import ClassSecurityInfo


from Products.Archetypes.utils  import shasattr

from Products.CMFCore.utils     import getToolByName


           
from Products.gvSIGi18nTool.TRAgvSIGi18nTool_Constants import cTRAgvSIGi18nToolId
            
            
    
from TRAElemento_Constants                 import *
from TRAElemento_Constants_Activity        import *
from TRAElemento_Constants_Configurations  import *
from TRAElemento_Constants_Dates           import *
from TRAElemento_Constants_Encoding        import *
from TRAElemento_Constants_Import          import *
from TRAElemento_Constants_Languages       import *
from TRAElemento_Constants_Logging         import *
from TRAElemento_Constants_Modules         import *
from TRAElemento_Constants_Profiling       import *
from TRAElemento_Constants_Progress        import *
from TRAElemento_Constants_String          import *
from TRAElemento_Constants_StringRequests  import *
from TRAElemento_Constants_Translate       import *
from TRAElemento_Constants_Translation     import *
from TRAElemento_Constants_TypeNames       import *
from TRAElemento_Constants_Views           import *
from TRAElemento_Constants_Vocabularies    import *
from TRAUtils                              import *

  
            
 
            
# ########################################################################################################
    
class TRAElemento_PloneTools:
    """Class with responsibility to provide access to Plone tool singletons.
        
    """
    
    security = ClassSecurityInfo()

    

    security.declarePublic('fHasTRAtool')
    def fHasTRAtool(self, ):
        
        aTRAgvSIGi18nTool = getToolByName(self, cTRAgvSIGi18nToolId, None)
        
        if aTRAgvSIGi18nTool == None:
            return False
    
        return True
    
    

        
        
    security.declarePublic('getPortalURLTool')
    def getPortalURLTool(self, ):
        
        aTool = getToolByName(self, 'portal_url', None)
        return aTool

            
     
    security.declarePublic( 'getPloneUtilsToolForNormalizeString')
    def getPloneUtilsToolForNormalizeString(self):
        """Utility tool accessor.
        
        """
        
        aTool = getToolByName(self, 'plone_utils', None)
        if not shasattr( aTool, 'normalizeString'):
            return None 
        return aTool

    
    
           
    
    
    security.declarePublic( 'getPloneUtilsToolForRoles')
    def getPloneUtilsToolForRoles(self):
    
        aTool = getToolByName(self, 'plone_utils', None)
        return aTool

    
    
           
 
    security.declarePublic( 'getGroupsTool')
    def getGroupsTool(self):
    
        aTool = getToolByName(self, 'portal_groups', None)
        return aTool

    
    
           
    security.declarePublic( 'getPloneLanguageTool')
    def getPloneLanguageTool(self):
    
        aTool = getToolByName(self, 'portal_languages', None)
        return aTool

    
    
           
    
           
    security.declarePublic( 'getPortalMembershipTool')
    def getPortalMembershipTool(self):
    
        aTool = getToolByName(self, 'portal_membership', None)
        return aTool

    
         
     




    security.declarePublic( 'getTranslationServiceTool')
    def getTranslationServiceTool( self, ):
        return getToolByName( self, 'translation_service', None)
    
    
               
    
    security.declarePublic( 'getPortalCatalogTool')
    def getPortalCatalogTool( self, ):
        return getToolByName( self, 'portal_catalog', None)
    


    
               
    
    security.declarePublic( 'getUIDCatalogTool')
    def getUIDCatalogTool( self, ):
        return getToolByName( self, 'uid_catalog', None)
    


    
        



