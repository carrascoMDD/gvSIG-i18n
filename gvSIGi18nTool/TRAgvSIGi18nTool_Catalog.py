# -*- coding: utf-8 -*-
#
# File: TRAgvSIGi18nTool_Catalog.py
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




class TRAgvSIGi18nTool_Catalog:
    """Catalog services: Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations..
    
    """

        
    
    security = ClassSecurityInfo()


    
    
    
    # ##########################################################
    """TRACatalogo basic access Boundary methods (facade).
    
    """
        
    
    
    security.declareProtected( permissions.View, 'fCatalogo')
    def fCatalogo(self, 
        theContextualElement    =None,):
        
        if theContextualElement == None:
            return None
        
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return None
        
        return unCatalogo
        

    
    
    security.declareProtected( permissions.View, 'fCatalogoTitle')
    def fCatalogoTitle(self, 
        theContextualElement    =None,):
        
        if theContextualElement == None:
            return ''
        
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return ''
        
        return unCatalogo.Title()
        

    

    
    security.declareProtected( permissions.View, 'fCatalogoDescription')
    def fCatalogoDescription(self, 
        theContextualElement    =None,):
        
        if theContextualElement == None:
            return ''
        
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return ''
        
        return unCatalogo.Description()
            
    
    
    
    
    security.declareProtected( permissions.View, 'fCatalogoAbsoluteURL')
    def fCatalogoAbsoluteURL(self, 
        theContextualElement    =None,):
        
        if theContextualElement == None:
            return ''
        
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return ''
        
        return unCatalogo.absolute_url()
        

    
    
    security.declareProtected( permissions.View, 'fCatalogoNombreProducto')
    def fCatalogoNombreProducto(self, 
        theContextualElement    =None,):
        
        if theContextualElement == None:
            return ''
        
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return ''
        
        return unCatalogo.getNombreProducto()
        


    
    
    
    
   
    # ##########################################################
    """TRACatalogo access test Boundary methods (facade).
    
    """       
              
     
    security.declareProtected( permissions.View, 'fCatalogoAllowWrite')
    def fCatalogoAllowWrite(self,
        theContextualElement    =None,):
        
        if theContextualElement == None:
            return False
        
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return False
        
        return unCatalogo.fAllowWrite()
    
    
           
    
    
    security.declareProtected( permissions.View, 'fLabelModuloNoEspecificado')
    def fLabelModuloNoEspecificado(self,
        theContextualElement    =None,):
        
        if theContextualElement == None:
            return ''
        
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return ''
        
        return unCatalogo.fLabelModuloNoEspecificado()
    
            
    
    
    

   
    # ##########################################################
    """TRACatalogo access protection Boundary methods (facade).
    
    """       
                
    
    security.declareProtected( permissions.View, 'fBloquearCatalogo')
    def fBloquearCatalogo( self , 
        theContextualElement     =None,
        theCheckPermissions      =True, 
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):
    
        if theContextualElement == None:
            return False
        
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return False
        
        return unCatalogo.fBloquearCatalogo(        
            theCheckPermissions      =theCheckPermissions, 
            thePermissionsCache      =thePermissionsCache, 
            theRolesCache            =theRolesCache, 
            theParentExecutionRecord =theParentExecutionRecord,
        )
        
        
        
    
        

    security.declareProtected( permissions.View, 'fDesbloquearCatalogo')
    def fDesbloquearCatalogo( self , 
        theContextualElement     =None,
        theCheckPermissions      =True, 
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):
    
        if theContextualElement == None:
            return False
        
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return False
        
        return unCatalogo.fDesbloquearCatalogo(        
            theCheckPermissions      =theCheckPermissions, 
            thePermissionsCache      =thePermissionsCache, 
            theRolesCache            =theRolesCache, 
            theParentExecutionRecord =theParentExecutionRecord,
        )
        
        
        
        