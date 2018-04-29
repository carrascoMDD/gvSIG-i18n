# -*- coding: utf-8 -*-
#
# File: TRAgvSIGi18nTool_Modules.py
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





# ##########################################################
"""Modules services Boundary methods (facade).

"""    



class TRAgvSIGi18nTool_Modules:
    """Modules services: Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations..
    
    """


    security = ClassSecurityInfo()
        
             

    security.declareProtected( permissions.View, 'fTodosNombresModulos')
    def fTodosNombresModulos( self, 
        theContextualElement     =None):
        
        if theContextualElement == None:
            return []
            
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return []
        
        return unCatalogo.fTodosNombresModulos()
        
    
    

    
    


    security.declareProtected( permissions.View, 'fCreateProgressHandlerFor_DeleteModule')
    def fCreateProgressHandlerFor_DeleteModule( self, 
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
        
        
        if not ( theContextualElement.meta_type == 'TRAColeccionModulos'):
            return {
                'success':   False,
                'condition': cTRAToolCondition_ContextualElementOfWrongType,
            }
        
        return theContextualElement.fCreateProgressHandlerFor_DeleteModule( 
            theAdditionalParams         =theAdditionalParams,
            thePermissionsCache         =thePermissionsCache, 
            theRolesCache               =theRolesCache, 
            theParentExecutionRecord    =theParentExecutionRecord,
        )
        
        
    
    
        

    security.declareProtected( permissions.View, 'fCrearModulo')
    def fCrearModulo( self, 
        theContextualElement             =None,
        theTimeProfilingResults          =None, 
        theModelDDvlPloneTool_Mutators   =None, 
        theNewTypeName                   ='', 
        theNewOneTitle                   ='', 
        theNewOneDescription             ='', 
        theAdditionalParams              =None,
        thePermissionsCache              =None,
        theRolesCache                    =None,
        theParentExecutionRecord         =None):
        """Create a new instance of TRAModulo, immediately, without import process.
        
        """
        
        if theContextualElement == None:
            return {
                'effect':  'error', 
                'failure': cTRAToolCondition_NoContextualElement,
            }
        
        
        if not ( theContextualElement.meta_type == 'TRAColeccionModulos'):
            return {
                'effect':  'error', 
                'failure': cTRAToolCondition_ContextualElementOfWrongType,
            }
    
        return theContextualElement.fCrearModulo(
            theTimeProfilingResults          =theTimeProfilingResults, 
            theModelDDvlPloneTool_Mutators   =theModelDDvlPloneTool_Mutators, 
            theNewTypeName                   =theNewTypeName, 
            theNewOneTitle                   =theNewOneTitle, 
            theNewOneDescription             =theNewOneDescription, 
            theAdditionalParams              =theAdditionalParams,
            thePermissionsCache              =thePermissionsCache,
            theRolesCache                    =theRolesCache,
            theParentExecutionRecord         =theParentExecutionRecord,
        )
                     
    
        