# -*- coding: utf-8 -*-
#
# File: TRAgvSIGi18nTool_Status.py
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
"""Status services Boundary methods (facade).

"""
        


class TRAgvSIGi18nTool_Status:
    """Status services: Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations..
    
    """

    security = ClassSecurityInfo()
        
      
    security.declareProtected( permissions.View, 'fElaborarInformeIdiomas')
    def fElaborarInformeIdiomas(self, 
        theContextualElement    =None,
        theCheckPermissions         =True, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):
        """Generate Report By Languages

        """        
        
        if theContextualElement == None:
            return {
                'error':    cTRAToolCondition_NoContextualElement,   
            } 
            
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return {
                'error':    cTRAToolCondition_NoCatalogElement,   
            }
        
        return unCatalogo.fElaborarInformeIdiomas(
            theCheckPermissions         =theCheckPermissions, 
            thePermissionsCache         =thePermissionsCache, 
            theRolesCache               =theRolesCache, 
            theParentExecutionRecord    =theParentExecutionRecord,
        )
    
    
        
        
        
    
    
    security.declareProtected( permissions.View, 'fInvalidateObsoleteStatusReportByLanguages')
    def fInvalidateObsoleteStatusReportByLanguages(self,
        theContextualElement        =None,):
        
        if theContextualElement == None:
            return {
                'invalidated':    False,   
            } 
            
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return {
                'invalidated':    False,   
            }
        
        return unCatalogo.fInvalidateObsoleteStatusReportByLanguages()
        
        
    
        
    
    

    
    security.declareProtected( permissions.View, 'fElaborarInformeModulos')
    def fElaborarInformeModulos(self, 
        theContextualElement    =None,
        theCheckPermissions         =True, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):
        """Generate Report By Languages

        """        
        
        if theContextualElement == None:
            return {
                'error':    cTRAToolCondition_NoContextualElement,   
            } 
            
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return {
                'error':    cTRAToolCondition_NoCatalogElement,   
            }
        
        return unCatalogo.fElaborarInformeModulos( 
            theCheckPermissions         =theCheckPermissions, 
            thePermissionsCache         =thePermissionsCache, 
            theRolesCache               =theRolesCache, 
            theParentExecutionRecord    =theParentExecutionRecord,
        )
    
    
    




    security.declareProtected( permissions.View, 'fElaborarInformeModulos')
    def fInvalidateObsoleteStatusReportByModulesAndLanguages(self,
        theContextualElement        =None,):
        
        if theContextualElement == None:
            return {
                'invalidated':    False,   
            } 
            
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return {
                'invalidated':    False,   
            }
        
        return unCatalogo.fInvalidateObsoleteStatusReportByModulesAndLanguages()
        
    
    
    
    
    


    
    security.declareProtected( permissions.View, 'fElaborarInformeActividad')
    def fElaborarInformeActividad(self, 
        theContextualElement        =None,
        theCheckPermissions         =True, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):
        """Generate Activity Report

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
        
        return unCatalogo.fElaborarInformeActividad(
            theCheckPermissions         =theCheckPermissions, 
            thePermissionsCache         =thePermissionsCache, 
            theRolesCache               =theRolesCache, 
            theParentExecutionRecord    =theParentExecutionRecord,
        )
    
    
        
    
    security.declareProtected( permissions.View, 'fInvalidateObsoleteActivityReport')
    def fInvalidateObsoleteActivityReport(self, 
       theContextualElement    =None,):
        
        if theContextualElement == None:
            return {
                'invalidated':    False,   
            }
        
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return {
                'invalidated':    False,   
            }
        
        return unCatalogo.fInvalidateObsoleteActivityReport()
        
        
    
        

    
    