# -*- coding: utf-8 -*-
#
# File: TRAgvSIGi18nTool_Contributions.py
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
"""Languages services Boundary methods (facade).

"""    
                


class TRAgvSIGi18nTool_Contributions:
    """Languages services: Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations..
    
    """

        
    
    security = ClassSecurityInfo()



    security.declareProtected( permissions.View, 'fCreateProgressHandlerFor_Contributions')
    def fCreateProgressHandlerFor_Contributions( self, 
        theContextualElement    =None,
        theAdditionalParams     =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Request creation of a report Contributions long-lived process control handler, to be executed later.
        
        """
    
        if theContextualElement == None:
            return {
                'success':   False,
                'condition': cTRAToolCondition_NoContextualElement,
            }
        
        if not ( theContextualElement.meta_type == 'TRAColeccionContribuciones',):
            return {
                'success':   False,
                'condition': cTRAToolCondition_ContextualElementOfWrongType,
            }
        
        
        return theContextualElement.fCreateProgressHandlerFor_Contributions(
            theAdditionalParams     =theAdditionalParams,  
            thePermissionsCache     =thePermissionsCache, 
            theRolesCache           =theRolesCache, 
            theParentExecutionRecord=theParentExecutionRecord,
        )
        
    
            
        
            