# -*- coding: utf-8 -*-
#
# File: TRAgvSIGi18nTool_Languages.py
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
                


class TRAgvSIGi18nTool_Languages:
    """Languages services: Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations..
    
    """

        
    
    security = ClassSecurityInfo()



    security.declareProtected( permissions.View, 'fNonExistingKnownIdiomasCodesAndDisplayNames')
    def fNonExistingKnownIdiomasCodesAndDisplayNames(self, 
        theContextualElement     =None,):
        
        if theContextualElement == None:
            return []
            
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return []
        
        return unCatalogo.fNonExistingKnownIdiomasCodesAndDisplayNames( )
        
     
    
    
    
    
    security.declareProtected( permissions.View, 'fKnownIdiomaCodeAndDisplayName')
    def fKnownIdiomaCodeAndDisplayName(self, 
        theContextualElement     =None,
        theCodigoIdioma          =None):
        
        if theContextualElement == None:
            return []
            
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return []
        
        return unCatalogo.fKnownIdiomaCodeAndDisplayName( theCodigoIdioma)
        
           
   
    
    
    
    
    security.declareProtected( permissions.View, 'fTodosIdiomasCodesAndDisplayNames')
    def fTodosIdiomasCodesAndDisplayNames(self, 
        theContextualElement     =None,):
        
        if theContextualElement == None:
            return []
            
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return []
        
        return unCatalogo.fTodosIdiomasCodesAndDisplayNames( )
        
    
    
    
    
    

    
    security.declareProtected( permissions.View, 'fInformeTitulosIdiomasYModulosPermitidos')
    def fInformeTitulosIdiomasYModulosPermitidos( self, 
        theContextualElement     =None,
        theUseCaseName           ='', 
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None): 
        """Report the titles of all languages and modules for which the user has permission to involve in exercising theUseCaseName.

        Output Values of type string returned in unicode.
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
        

        return unCatalogo.fInformeTitulosIdiomasYModulosPermitidos(
            theUseCaseName              =theUseCaseName, 
            thePermissionsCache         =thePermissionsCache, 
            theRolesCache               =theRolesCache, 
            theParentExecutionRecord    =theParentExecutionRecord,
        )
            
        
        
    
    
    
    


   
    security.declareProtected( permissions.View, 'fInformeTitulosIdiomasConIdiomaReferenciaYModulosPermitidos')
    def fInformeTitulosIdiomasConIdiomaReferenciaYModulosPermitidos( self, 
        theContextualElement     =None,
        theUseCaseName           ='', 
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None): 
        """Report the titles of all languages and modules for which the user has permission to involve in exercising theUseCaseName.

        Output Values of type string returned in unicode.
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
        

        return unCatalogo.fInformeTitulosIdiomasConIdiomaReferenciaYModulosPermitidos(
            theUseCaseName              =theUseCaseName, 
            thePermissionsCache         =thePermissionsCache, 
            theRolesCache               =theRolesCache, 
            theParentExecutionRecord    =theParentExecutionRecord,
        )
            
       
        


    
         
    security.declareProtected( permissions.View, 'fCodigoIdiomaEnGvSIG')
    def fCodigoIdiomaEnGvSIG( self , 
        theContextualElement    =None,):
    
        if theContextualElement == None:
            return ''
        
        if not ( theContextualElement.meta_type == 'TRAIdioma'):
            return ''            
        
        return theContextualElement.getCodigoIdiomaEnGvSIG()
    
    
    
    
    
    
    security.declareProtected( permissions.View, 'fOtrosIdiomasCodesAndDisplayNames')
    def fOtrosIdiomasCodesAndDisplayNames( self , 
        theContextualElement    =None,):
    
        if theContextualElement == None:
            return []
        
        if not ( theContextualElement.meta_type == 'TRAIdioma'):
            return []            
        
        return theContextualElement.fOtrosIdiomasCodesAndDisplayNames()
       
    
    
    
    
    
    
    
    security.declareProtected( permissions.View, 'fBloquearIdioma')
    def fBloquearIdioma( self , 
        theContextualElement    =None,
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
    
    
        if theContextualElement == None:
            return False
        
        if not ( theContextualElement.meta_type == 'TRAIdioma'):
            return False            
        
        return theContextualElement.fBloquearIdioma(
            thePermissionsCache     =thePermissionsCache, 
            theRolesCache           =theRolesCache, 
            theParentExecutionRecord=theParentExecutionRecord,
        )
    
    
    
      
    

    
    security.declareProtected( permissions.View, 'fDesbloquearIdioma')
    def fDesbloquearIdioma( self , 
        theContextualElement    =None,
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
    
    
        if theContextualElement == None:
            return False
        
        if not ( theContextualElement.meta_type == 'TRAIdioma'):
            return False            
        
        return theContextualElement.fDesbloquearIdioma(
            thePermissionsCache     =thePermissionsCache, 
            theRolesCache           =theRolesCache, 
            theParentExecutionRecord=theParentExecutionRecord,
        )
    
        
    
    
      


        
    
    security.declareProtected( permissions.View, 'fCreateProgressHandlerFor_CreateLanguage')
    def fCreateProgressHandlerFor_CreateLanguage( self, 
        theContextualElement        =None,
        theAdditionalParams         =None,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None): 
        """Create a new instance of TRAIdioma through an import process. Create an instance of TRAImportacion with a TRAContenidoIntercambio that will create the language when the import is executed.
        
        """
    
        if theContextualElement == None:
            return {
                'success':   False,
                'condition': cTRAToolCondition_NoContextualElement,
            }
        
        
        if not ( theContextualElement.meta_type == 'TRAColeccionIdiomas'):
            return {
                'success':   False,
                'condition': cTRAToolCondition_ContextualElementOfWrongType,
            }
        
        return theContextualElement.fCreateProgressHandlerFor_CreateLanguage( 
            theAdditionalParams         =theAdditionalParams,
            thePermissionsCache         =thePermissionsCache, 
            theRolesCache               =theRolesCache, 
            theParentExecutionRecord    =theParentExecutionRecord,
        )
    
    
        
    
    
        


    security.declareProtected( permissions.View, 'fCreateProgressHandlerFor_DeleteLanguage')
    def fCreateProgressHandlerFor_DeleteLanguage( self, 
        theContextualElement        =None,
        theAdditionalParams         =None,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None): 
        """Request creation of a DeleteLanguage long-lived process control handler, to be executed later.
        
        """
    
        if theContextualElement == None:
            return {
                'success':   False,
                'condition': cTRAToolCondition_NoContextualElement,
            }
        
        if not ( theContextualElement.meta_type == 'TRAColeccionIdiomas'):
            return {
                'success':   False,
                'condition': cTRAToolCondition_ContextualElementOfWrongType,
            }
        
        return theContextualElement.fCreateProgressHandlerFor_DeleteLanguage( 
            theAdditionalParams         =theAdditionalParams,
            thePermissionsCache         =thePermissionsCache, 
            theRolesCache               =theRolesCache, 
            theParentExecutionRecord    =theParentExecutionRecord,
        )
        
    
            
        
            