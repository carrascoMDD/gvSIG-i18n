# -*- coding: utf-8 -*-
#
# File: TRAgvSIGi18nTool_Import.py
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
"""Import access Boundary methods (facade).

"""
        

class TRAgvSIGi18nTool_Import:
    """Import services: Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations..
    
    """

    security = ClassSecurityInfo()
        
    
   
    security.declareProtected( permissions.View, 'fInitialParameters_CrearContenidoIntercambio')
    def fInitialParameters_CrearContenidoIntercambio( self, 
        theContextualElement    =None,):
        """Parameters to initialize the dialog with the user when creating a translations interchange contents element.
        
        """
    
        if theContextualElement == None:
            return {}
        
        if not ( theContextualElement.meta_type == 'TRAImportacion'):
            return {}
        
        return theContextualElement.fInitialParameters_CrearContenidoIntercambio()
                
    
    
    
    
    
    

    security.declareProtected( permissions.View, 'fCrearContenidoIntercambio')
    def fCrearContenidoIntercambio( self, 
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
        """Create a new instance of TRAContenidoIntercambio, immediately, without import process.
        
        """
        
        if theContextualElement == None:
            return {
                'effect':  'error', 
                'failure': cTRAToolCondition_NoContextualElement,
            }
        
        
        if not ( theContextualElement.meta_type == 'TRAImportacion'):
            return {
                'effect':  'error', 
                'failure': cTRAToolCondition_ContextualElementOfWrongType,
            }
    
        return theContextualElement.fCrearContenidoIntercambio(
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
                         

    
    



    security.declareProtected( permissions.View, 'fCreateProgressHandlerFor_ImportToRestoreBackup')
    def fCreateProgressHandlerFor_ImportToRestoreBackup( self, 
        theContextualElement             =None,
        theUploadedFile                  =None, 
        thePermissionsCache              =None,
        theRolesCache                    =None,
        theParentExecutionRecord         =None):
        """Create a new instance of TRAImportacion to restore a translations catalog backup, immediately, without import process.
        
        """
        
        if theContextualElement == None:
            return {
                'effect':  'error', 
                'failure': cTRAToolCondition_NoContextualElement,
            }
        
        
        if not ( theContextualElement.meta_type in [ 'TRACatalogo', 'TRAColeccionImportaciones',]):
            return {
                'effect':  'error', 
                'failure': cTRAToolCondition_ContextualElementOfWrongType,
            }
    
        
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return {
                'effect':  'error', 
                'failure': cTRAToolCondition_NoCatalogElement,
            }
        
        unaColeccionImportaciones = unCatalogo.fObtenerColeccionImportaciones()
        if unaColeccionImportaciones == None:
            return {
                'effect':  'error', 
                'failure': cTRAToolCondition_NoImportsCollectionElement,
            }
        
            
        return unaColeccionImportaciones.fCreateProgressHandlerFor_ImportToRestoreBackup(
            theUploadedFile                  =theUploadedFile, 
            thePermissionsCache              =thePermissionsCache,
            theRolesCache                    =theRolesCache,
            theParentExecutionRecord         =theParentExecutionRecord,
        )
                         

    
    
    
    
    
    
    
    
    security.declareProtected( permissions.View, 'fInformeCambios')
    def fInformeCambios( self, 
        theContextualElement    =None,
        theParentExecutionRecord=None):
        
        if theContextualElement == None:
            return {}
    
        if not ( theContextualElement.meta_type == 'TRAImportacion'):
            return {}
        
        return theContextualElement.fInformeCambios( theParentExecutionRecord)
    
    
    
    
    
        

    
    security.declareProtected( permissions.View, 'fInformeContenidosImportacion')
    def fInformeContenidosImportacion( self, 
        theContextualElement    =None,
        theParentExecutionRecord=None):
        
        if theContextualElement == None:
            return {}
    
        if not ( theContextualElement.meta_type == 'TRAImportacion'):
            return {}
        
        return theContextualElement.fInformeContenidosImportacion( theParentExecutionRecord)
    
    
    
    
    
    
    
    
    security.declareProtected( permissions.View, 'fInformesTodosContenidosIntercambio')
    def fInformesTodosContenidosIntercambio( self, 
        theContextualElement    =None,
        theParentExecutionRecord=None):
        
        if theContextualElement == None:
            return []
    
        if not ( theContextualElement.meta_type == 'TRAImportacion'):
            return []
        
        return theContextualElement.fInformesTodosContenidosIntercambio( theParentExecutionRecord)
        
       
        
    
    

        
    security.declareProtected( permissions.View, 'fInformeContenidoIntercambio')
    def fInformeContenidoIntercambio( self, 
        theContextualElement    =None,
        theParentExecutionRecord=None):
        
        if theContextualElement == None:
            return {}
    
        if not ( theContextualElement.meta_type == 'TRAContenidoIntercambio'):
            return {}
        
        return theContextualElement.fInformeContenidoIntercambio( theParentExecutionRecord)
        
           
    
    
           
    

    
    
    
    security.declareProtected( permissions.View, 'fReutilizarImportacion')
    def fReutilizarImportacion( self , 
        theContextualElement    =None,
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
    
    
        if theContextualElement == None:
            return False
    
        if not ( theContextualElement.meta_type == 'TRAImportacion'):
            return False
        
        return theContextualElement.fReutilizarImportacion(
            thePermissionsCache     =thePermissionsCache, 
            theRolesCache           =theRolesCache, 
            theParentExecutionRecord=theParentExecutionRecord,
        )
    
    
    
    


    
    security.declareProtected( permissions.View, 'fEstimarCosteImportacion')    
    def fEstimarCosteImportacion( self,  
        theContextualElement     =None,
        theIsToCreateCadenas     =False,
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):
        """Estimate the number of operations of various kinds that would be performed during the execution of an import process in the TRAImportacion contents.
        
        """
        

        if theContextualElement == None:
            return {
                'valid':  False,
                'error':  cTRAToolCondition_NoContextualElement,
            }
        
        if not ( theContextualElement.meta_type == 'TRAImportacion'):
            return {
                'valid':  False,
                'error':  cTRAToolCondition_ContextualElementOfWrongType,
            }
        
        return theContextualElement.fEstimarCosteImportacion(
            theIsToCreateCadenas     =theIsToCreateCadenas,
            thePermissionsCache      =thePermissionsCache, 
            theRolesCache            =theRolesCache, 
            theParentExecutionRecord =theParentExecutionRecord,
        )
                
            
    
    
            
    
    security.declareProtected( permissions.View, 'fCreateProgressHandlerFor_Import')
    def fCreateProgressHandlerFor_Import( self, 
        theContextualElement    =None,
        theAdditionalParams     =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Request creation of an Import long-lived process control handler, to be executed later.
        
        """
    
        if theContextualElement == None:
            return {
                'success':   False,
                'condition': cTRAToolCondition_NoContextualElement,
            }
        
        if not ( theContextualElement.meta_type == 'TRAImportacion'):
            return {
                'success':   False,
                'condition': cTRAToolCondition_ContextualElementOfWrongType,
            }
        
        return theContextualElement.fCreateProgressHandlerFor_Import(
            theAdditionalParams     =theAdditionalParams,  
            thePermissionsCache     =thePermissionsCache, 
            theRolesCache           =theRolesCache, 
            theParentExecutionRecord=theParentExecutionRecord,
        )
                
        
    
        