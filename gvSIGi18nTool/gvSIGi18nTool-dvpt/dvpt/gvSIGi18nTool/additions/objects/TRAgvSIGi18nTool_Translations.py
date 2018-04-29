# -*- coding: utf-8 -*-
#
# File: TRAgvSIGi18nTool_Translations.py
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


from TRAgvSIGi18nTool_Constants import *




class TRAgvSIGi18nTool_Translations:
    """Translations services: Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations..
    
    """

        
    security = ClassSecurityInfo()
    
    
    security.declareProtected( permissions.View, 'fNewVoidChangeAndBrowseTraslationsRequest')
    def fNewVoidChangeAndBrowseTraslationsRequest(self, 
        theContextualElement     =None,):

        if theContextualElement == None:
            return {}
            
        return theContextualElement.fNewVoidChangeAndBrowseTraslationsRequest( )
        
        
    
    


    
    
        
    security.declareProtected( permissions.View, 'fChangeAndBrowseTranslations')
    def fChangeAndBrowseTranslations(self, 
        theContextualElement        =None,
        theServiceRequest           =None, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None): 
        """Process change request and retrieve translations to browse.
        
        """

        if theContextualElement == None:
            return []
            
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return []
        
        return unCatalogo.fChangeAndBrowseTranslations(
            theServiceRequest           =theServiceRequest, 
            thePermissionsCache         =thePermissionsCache, 
            theRolesCache               =theRolesCache, 
            theParentExecutionRecord    =theParentExecutionRecord,
        )
        
     
        
        
            
  
    security.declarePublic( 'fService_ChangeTranslation')
    def fService_ChangeTranslation( self, 
        theContextualElement        =None,
        theChangeRequestParameters  ={}, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None): 
        """Process Asynchronous change request.
        
        """
    
        if theContextualElement == None:
            return {
                'success':    False,
            }
        
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return {
                'success':    False,
            }
        
        
        return unCatalogo.fService_ChangeTranslation(  
            theChangeRequestParameters  =theChangeRequestParameters, 
            thePermissionsCache         =thePermissionsCache, 
            theRolesCache               =theRolesCache, 
            theParentExecutionRecord    =theParentExecutionRecord,
        )
    
    
    
    
 

    security.declareProtected( permissions.View, 'fCreateProgressHandlerFor_CopyTranslations')
    def fCreateProgressHandlerFor_CopyTranslations( self, 
        theContextualElement        =None,
        theAdditionalParams         =None,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None): 
        """Request creation of a DeleteModule long-lived process control handler, to be executed later.
        
        """
    
        if theContextualElement == None:
            return {
                'success':   False,
                'condition': cTRAToolCondition_NoContextualElement,
            }
        
        if not ( theContextualElement.meta_type == 'TRAIdioma'):
            return {
                'success':   False,
                'condition': cTRAToolCondition_ContextualElementOfWrongType,
            }
        
        return theContextualElement.fCreateProgressHandlerFor_CopyTranslations( 
            theAdditionalParams         =theAdditionalParams,
            thePermissionsCache         =thePermissionsCache, 
            theRolesCache               =theRolesCache, 
            theParentExecutionRecord    =theParentExecutionRecord,
        )
        
    
    
        
