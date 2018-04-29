# -*- coding: utf-8 -*-
#
# File: TRAElemento_UsersAndGroupsUtils.py
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
    
class TRAElemento_UsersAndGroupsUtils:
    """Class with responsibility supplying some utilities to deal with users and groups.
        
    """
    
    security = ClassSecurityInfo()

    

       
    security.declarePrivate( 'fUserGroupIdEnCatalogoFor')
    def fUserGroupIdEnCatalogoFor(self, theGroupName):
        return '%s_%s' % ( self.fPrefijoUserGroupsEnCatalogo(), theGroupName, )
 
     
    
    
    
    security.declarePrivate( 'fPrefijoUserGroupsEnCatalogo')
    def fPrefijoUserGroupsEnCatalogo(self, ):
        return 'TRA_%s' % '_'.join( self.getCatalogo().getPhysicalPath()[2:])
 

    

    security.declarePublic( 'fGetMemberId_safe')
    def fGetMemberId_safe(self ):
        """Retrieve the member identifier of the connected user trapping any exceptions that may occur during the retrieval. 
        
        """
        aMemberId = ''
        try:
            aMemberId = self.fGetMemberId()
        except:
            None
        
        return aMemberId
    
    
    

    
    security.declarePublic( 'fGetMemberId')
    def fGetMemberId(self ):
        """Retrieve the member identifier of the connected user . 
        
        """
    
        aMembershipTool = self.getPortalMembershipTool()
        if not aMembershipTool:
            return ''
        
        unMember = aMembershipTool.getAuthenticatedMember()   

        if not unMember:
            return ''
        
        if unMember.getUserName() ==  cTRAMemberIdAnonymousUser:
            unMemberId = cTRAMemberIdAnonymousUser
        else:
            unMemberId = unMember.getMemberId()   

        return unMemberId
        
   
    

    
    
    security.declarePrivate( 'fUsersInGroupId')
    def fUsersInGroupId(self, theGroupId):
        if not theGroupId:
            return []
        
        unPortalGroupsTool = self.getGroupsTool()
        if not unPortalGroupsTool:
            return unInforme
        
        unosGroupMembers = unPortalGroupsTool.getGroupMembers( theGroupId)
        return unosGroupMembers
    
    
    

    