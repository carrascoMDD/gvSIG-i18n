# -*- coding: utf-8 -*-
#
# File: TRAElemento_Cache.py
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



from AccessControl              import ClassSecurityInfo

from Products.CMFCore           import permissions


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
    
class TRAElemento_Cache:
    """Class with responsibility dealing with rendered page cache services.
        
    """
    
    security = ClassSecurityInfo()

    
     

    
    
    

    # #############################################################
    """Configuration methods.
    
    """
        
        
    security.declarePublic( 'fPaginaDefault')    
    def fPaginaDefault( self):
        
        aMetaType = self.meta_type
        
        aDefaultPage = cTRADefaultPagesForTypes.get( aMetaType, 'Tabular')
        return aDefaultPage
    
    
    
    
    security.declarePrivate( 'fIsPrivateCacheViewForNonAnonymousUsers')
    def fIsPrivateCacheViewForQualifiedUsers(self , theTemplateName):
        """Shall return true when the template name is for a view sensitive to write user permissions ( modify portal content, delete, add folders, ) on rendered objects, in addition to the permissions required by Zope/Plone to deliver data to the requester (view, list folder contents, access content information,).
        
        """
        return  theTemplateName in cTRAPrivateCacheViewsForQualifiedUsers
        
    
    
    
    
    

    # #############################################################
    """Cache flush methods.
    
    """
    
    security.declarePrivate('pFlushCachedTemplates')
    def pFlushCachedTemplates(self,  theViewsToFlush=[]):
        unModelDDvlPloneTool = self.fModelDDvlPloneTool()
        if not unModelDDvlPloneTool:
            return self
        
        unModelDDvlPloneTool.pFlushCachedTemplatesForImpactedElementsUIDs( self, [ self.UID(),], theViewsToFlush=theViewsToFlush)

        return self

           
    
    

    security.declarePublic('pFlushCachedTemplates_All')
    def pFlushCachedTemplates_All(self, theViewsToFlush=[]):
        """Remove from memory and disk cache all cached templates associated with this element and its contained elements, or optionally only those cached templates specified by name.
        
        """
        
        unModelDDvlPloneTool = self.fModelDDvlPloneTool()
        if not unModelDDvlPloneTool:
            return self

        someUIDs = self.fAllCacheableElementUIDs()
        if someUIDs:        
            unModelDDvlPloneTool.pFlushCachedTemplatesForImpactedElementsUIDs( self, someUIDs, theViewsToFlush=theViewsToFlush)

        return self
        
    

    

    
    security.declarePrivate('fAllCacheableElementUIDs')
    def fAllCacheableElementUIDs(self,):
       
        someUIDs = self.fAllElementUIDs( cTodosNombresTiposCacheables)        
        
        return someUIDs
        
        
    
    