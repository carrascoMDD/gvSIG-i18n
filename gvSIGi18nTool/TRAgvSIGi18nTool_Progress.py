# -*- coding: utf-8 -*-
#
# File: TRAgvSIGi18nTool_Progress.py
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
"""Progress long-lived process progress management Boundary methods (facade).

"""

class TRAgvSIGi18nTool_Progress:
    """Progress services: Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations..
    
    """

        
    

    security = ClassSecurityInfo()
        
    
 
    security.declareProtected( permissions.View, 'fProgressHandlerKey')
    def fProgressHandlerKey( self, 
        theContextualElement    =None,):
        
        if theContextualElement == None:
            return {}
        
        if not ( theContextualElement.meta_type == 'TRAProgreso'):
            return {}
        
        return theContextualElement.fProgressHandlerKey()
    
    
        
    
    security.declareProtected( permissions.View, 'fNewVoidProgressControlParms_ToChange')
    def fNewVoidProgressControlParms_ToChange( self, 
        theContextualElement    =None,):
        
        if theContextualElement == None:
            return None
        
        if not ( theContextualElement.meta_type == 'TRAProgreso'):
            return None
        
        return theContextualElement.fNewVoidProgressControlParms_ToChange()
    
        
    
    
    security.declareProtected( permissions.View, 'fParametrosEntrada')
    def fParametrosEntrada( self, 
        theContextualElement    =None,):
        
        if theContextualElement == None:
            return {}
        
        if not ( theContextualElement.meta_type == 'TRAProgreso'):
            return {}
        
        return theContextualElement.fParametrosEntrada()
    
    
        
    
    
    security.declareProtected( permissions.View, 'fDatosResultado')
    def fDatosResultado( self, 
        theContextualElement    =None,):
        
        if theContextualElement == None:
            return {}
        
        if not ( theContextualElement.meta_type == 'TRAProgreso'):
            return {}
        
        return theContextualElement.fDatosResultado()
    
    
    
    
        
    
    
    security.declareProtected( permissions.View, 'fEstadoControl')
    def fEstadoControl( self, 
        theContextualElement    =None,):
        
        if theContextualElement == None:
            return {}
        
        if not ( theContextualElement.meta_type == 'TRAProgreso'):
            return {}
        
        return theContextualElement.fEstadoControl()
    
    
        
    
        
    
    
    security.declareProtected( permissions.View, 'fParametrosControl')
    def fParametrosControl( self, 
        theContextualElement    =None,):
        
        if theContextualElement == None:
            return {}
        
        if not ( theContextualElement.meta_type == 'TRAProgreso'):
            return {}
        
        return theContextualElement.fParametrosControl()
    
    
    
    
    
    
    
    security.declareProtected( permissions.View, 'fContadoresControl')
    def fContadoresControl( self, 
        theContextualElement    =None,):
        
        if theContextualElement == None:
            return {}
        
        if not ( theContextualElement.meta_type == 'TRAProgreso'):
            return {}
        
        return theContextualElement.fContadoresControl()
    
                
    
    
    
    

    
    
    
    
    security.declareProtected( permissions.View, 'fDeriveElementoEspecificacionProceso')
    def fDeriveElementoEspecificacionProceso( self, 
        theContextualElement    =None,):
        
        if theContextualElement == None:
            return None
        
        if not ( theContextualElement.meta_type == 'TRAProgreso'):
            return None
        
        return theContextualElement.fDeriveElementoEspecificacionProceso()
    
    
    
    
                
    
    security.declareProtected( permissions.View, 'fIsActiveProgressHandler')
    def fIsActiveProgressHandler( self, 
        theContextualElement    =None,):
        
        if theContextualElement == None:
            return False
        
        if not ( theContextualElement.meta_type == 'TRAProgreso'):
            return False
        
        return theContextualElement.fIsActiveProgressHandler()
    
    
    
    
    
    
    security.declareProtected( permissions.View, 'fIsOverProgressHandler')
    def fIsOverProgressHandler( self, 
        theContextualElement    =None,):
        
        if theContextualElement == None:
            return False
        
        if not ( theContextualElement.meta_type == 'TRAProgreso'):
            return False
        
        return theContextualElement.fIsOverProgressHandler()
    
    
        
    
    
    
    
  
    security.declareProtected( permissions.View, 'fService_ProcessControl')
    def fService_ProcessControl( self, 
        theContextualElement    =None,
        theProcessControlAction     =None,
        theAdditionalParams          =None,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None): 
        """Process request to launch, terminate, pause, or resume a long-lived process, with a progress control handler registered in TRACatalogo_Globales.gTRAProgressHandlers.
        
        """

        if theContextualElement == None:
            return {
                'success':       False,
                'condition':     cTRAToolCondition_NoContextualElement,
            }
        
        if not ( theContextualElement.meta_type == 'TRAProgreso'):
            return {
                'success':       False,
                'condition':     cTRAToolCondition_ContextualElementOfWrongType,
            }
        
        return theContextualElement.fService_ProcessControl(
            theProcessControlAction     =theProcessControlAction,
            theAdditionalParams          =theAdditionalParams,
            thePermissionsCache         =thePermissionsCache, 
            theRolesCache               =theRolesCache, 
            theParentExecutionRecord    =theParentExecutionRecord,
        )
    
    
    
    
    
    
    