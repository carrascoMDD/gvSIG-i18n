# -*- coding: utf-8 -*-
#
# File: TRAgvSIGi18nTool_Permissions.py
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


from AccessControl import ClassSecurityInfo



from Products.CMFCore                    import permissions


from TRAgvSIGi18nTool_Constants import *

    
# ##########################################################
"""Permissions and Security services Boundary methods (facade).

"""
    


class TRAgvSIGi18nTool_Permissions:
    """Permissions services: Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations..
    
    """

        
    
    security = ClassSecurityInfo()
    

    
    
    security.declareProtected( permissions.View, 'fGetMemberId')
    def fGetMemberId( self,
        theContextualElement    =None,):
        """Retrieve the member identifier of the connected user . 
        
        """
        
        if theContextualElement == None:
            return ''
        
        return theContextualElement.fGetMemberId()
         
    
        

    security.declareProtected( permissions.View, 'fInheritedLocalRoles')
    def fInheritedLocalRoles( self,
        theContextualElement    =None,):
        
        if theContextualElement == None:
            return []
        
        return theContextualElement.fInheritedLocalRoles( )
                     
                
    
    
    
    security.declareProtected( permissions.View, 'fIsLocalRoleAcquired')
    def fIsLocalRoleAcquired( self,
        theContextualElement    =None,):
        
        if theContextualElement == None:
            return False
        
        return theContextualElement.fIsLocalRoleAcquired( )
                     
        
    
    
    

    security.declareProtected( permissions.View, 'fLocalRolesForUserId')
    def fLocalRolesForUserId( self, 
        theContextualElement    =None,
        theUserId               =None):
        
        if theContextualElement == None:
            return []
        
        return theContextualElement.fLocalRolesForUserId( theUserId)
             
    
    

    
    
    
    
    security.declareProtected( permissions.View, 'fPermissionsPermittedReport')
    def fPermissionsPermittedReport( self,
        theContextualElement    =None,
        thePermissionsToCheck   =None,):
        
        if theContextualElement == None:
            return False
        
        return theContextualElement.fPermissionsPermittedReport(
            thePermissionsToCheck   =thePermissionsToCheck,
        )
         

    
    
    
    
    security.declareProtected( permissions.View, 'fGetRequestingUserRoles')
    def fGetRequestingUserRoles( self,
        theContextualElement    =None,):
        
        if theContextualElement == None:
            return False
        
        return theContextualElement.fGetRequestingUserRoles()
         
    
    
    security.declareProtected( permissions.View, 'fPermissionsByElementType')
    def fPermissionsByElementType( self,
        theContextualElement    =None,):
        
        if theContextualElement == None:
            return False
        
        return theContextualElement.fPermissionsByElementType( )
         
    
    
    
    security.declareProtected( permissions.View, 'fRoleQuery_IsAnyRol')
    def fRoleQuery_IsAnyRol( self,
        theContextualElement    =None,
        theRolesUsuario         =None, 
        theElement              =None):
        
        if theContextualElement == None:
            return False
        
        return theContextualElement.fRoleQuery_IsAnyRol(
            theRolesUsuario    =theRolesUsuario,
            theElement         =theElement,
        )
         
    
    
    
    
    security.declareProtected( permissions.View, 'fUseCaseCheckDoable')
    def fUseCaseCheckDoable(self, 
        theContextualElement     =None,
        theUseCaseName           =None, 
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):     
    
        if theContextualElement == None:
            return False
        
        
        return theContextualElement.fUseCaseCheckDoable(
            theUseCaseName           =theUseCaseName, 
            thePermissionsCache      =thePermissionsCache, 
            theRolesCache            =theRolesCache, 
            theParentExecutionRecord =theParentExecutionRecord,
        )
        
    
        
        
    
    security.declareProtected( permissions.View, 'fUseCaseAssessment')
    def fUseCaseAssessment(self, 
        theContextualElement    =None,
        theUseCaseName          ='', 
        theElementsBindings     ={}, 
        theRulesToCollect       =False, 
        theRulesToBypass        =[],
        thePredicateOverrides   ={},
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):  
        """Assess the security rules specified for theUseCaseName against objects obtained from theElementBindings retrieving the elements accepted by the rules in theRulesToCollect and optionally gathering the result of every rule assessment.

        """
        
        if theContextualElement == None:
            return {
                'success':           False,
                'condition':         cTRAToolCondition_NoContextualElement,
            }
        
        return theContextualElement.fUseCaseAssessment(
            theUseCaseName          =theUseCaseName, 
            theElementsBindings     =theElementsBindings, 
            theRulesToCollect       =theRulesToCollect, 
            theRulesToBypass        =theRulesToBypass,
            thePredicateOverrides   =thePredicateOverrides,
            thePermissionsCache     =thePermissionsCache, 
            theRolesCache           =theRolesCache, 
            theParentExecutionRecord=theParentExecutionRecord,
        )

    
    
    
    security.declareProtected( permissions.View, 'fUseCaseAssessment')
    def fUseCaseAssessment_AvailableUseCasesOn(self, 
        theContextualElement    =None,
        theUseCaseNamesToAssess =None, 
        theRulesToCollect       =None,
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):  
        """Determine which Use Cases are available for the connected user to exercise on the current object, including the Use Cases with names supplied as parameter or all the existing Use Cases if no Use Case name was requested.
                
        """    
    
        if theContextualElement == None:
            return {}
        
        return theContextualElement.fUseCaseAssessment_AvailableUseCasesOn(
            theElement              =theContextualElement, 
            theUseCaseNamesToAssess =theUseCaseNamesToAssess, 
            theRulesToCollect       =theRulesToCollect,
            theRolesCache           =theRolesCache, 
            theParentExecutionRecord=theParentExecutionRecord,
        )

            
            
            