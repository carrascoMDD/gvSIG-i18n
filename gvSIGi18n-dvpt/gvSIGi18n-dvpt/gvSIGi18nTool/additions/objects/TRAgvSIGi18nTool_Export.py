# -*- coding: utf-8 -*-
#
# File: TRAgvSIGi18nTool_Export.py
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
"""Export services Boundary methods (facade).

"""



class TRAgvSIGi18nTool_Export:
    """Export services: Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations..
    
    """

    
    security = ClassSecurityInfo()
    
    

    security.declareProtected( permissions.View, 'fNewVoidExportParametersCandidateValues')
    def fNewVoidExportParametersCandidateValues(self, 
        theContextualElement     =None,):

        if theContextualElement == None:
            return {}
            
        return theContextualElement.fNewVoidExportParametersCandidateValues( )
        
                
    
    
 
    security.declareProtected( permissions.View, 'fEstimarContenidoExportacion')
    def fEstimarContenidoExportacion( self,
        theContextualElement             =None,        
        theParametersInput               = {},
        thePermissionsCache              = None,
        theRolesCache                    = None,
        theUseCaseAssessmentResultsCache = None,
        theParentExecutionRecord         = None):
        """Export Translations to the selected languages, including the selected reference languates, for the selected modules and/or the strings that specify no module, in the Java .properties or GNU gettext PO formats, possibly in separated modules, packaged in an archive of the specified name, and handling the encoding errors.
        
        """
        if theContextualElement == None:
            return False
        
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return False
        
        return unCatalogo.fEstimarContenidoExportacion(         
            theParametersInput               =theParametersInput,
            thePermissionsCache              =thePermissionsCache,
            theRolesCache                    =theRolesCache,
            theUseCaseAssessmentResultsCache =theUseCaseAssessmentResultsCache,
            theParentExecutionRecord         =theParentExecutionRecord,
        )
            

    
    

    
    # ##########################################################
    """Export Long-lived process services Boundary methods (facade).
    
    """
        
    
    security.declareProtected( permissions.View, 'fCreateProgressHandlerFor_Export')
    def fCreateProgressHandlerFor_Export( self, 
        theContextualElement    =None,
        theAdditionalParams     =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Request creation of a Export long-lived process control handler, to be executed later.
        
        """
    
        if theContextualElement == None:
            return {
                'success':   False,
                'condition': cTRAToolCondition_NoContextualElement,
            }
        
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return {
                'success':   False,
                'condition': cTRAToolCondition_NoCatalogElement,
            }
        
        return unCatalogo.fCreateProgressHandlerFor_Export(
            theAdditionalParams     =theAdditionalParams,  
            thePermissionsCache     =thePermissionsCache, 
            theRolesCache           =theRolesCache, 
            theParentExecutionRecord=theParentExecutionRecord,
        )
                
       
    
    
    

    security.declareProtected( permissions.View, 'fCreateProgressHandlerFor_ExportGvSIG')
    def fCreateProgressHandlerFor_ExportGvSIG( self, 
        theContextualElement    =None,
        theAdditionalParams     =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Request creation of a Export for gvSIG long-lived process control handler, to be executed later.
        
        """
    
        if theContextualElement == None:
            return {
                'success':   False,
                'condition': cTRAToolCondition_NoContextualElement,
            }
        
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return {
                'success':   False,
                'condition': cTRAToolCondition_NoCatalogElement,
            }
        
        return unCatalogo.fCreateProgressHandlerFor_ExportGvSIG(
            theAdditionalParams     =theAdditionalParams,  
            thePermissionsCache     =thePermissionsCache, 
            theRolesCache           =theRolesCache, 
            theParentExecutionRecord=theParentExecutionRecord,
        )
    
    
    
    
    
      
    
    
    

    security.declareProtected( permissions.View, 'fCreateProgressHandlerFor_ExportGvSIG_All')
    def fCreateProgressHandlerFor_ExportGvSIG_All( self, 
        theContextualElement    =None,
        theAdditionalParams     =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Request creation of a Export for gvSIG long-lived process control handler, to be executed later.
        
        """
    
        if theContextualElement == None:
            return {
                'success':   False,
                'condition': cTRAToolCondition_NoContextualElement,
            }
        
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return {
                'success':   False,
                'condition': cTRAToolCondition_NoCatalogElement,
            }
        
        return unCatalogo.fCreateProgressHandlerFor_ExportGvSIG_All(
            theAdditionalParams     =theAdditionalParams,  
            thePermissionsCache     =thePermissionsCache, 
            theRolesCache           =theRolesCache, 
            theParentExecutionRecord=theParentExecutionRecord,
        )
    
    
        
    
    
    
    security.declareProtected( permissions.View, 'fCreateProgressHandlerFor_Backup')
    def fCreateProgressHandlerFor_Backup( self, 
        theContextualElement    =None,
        theAdditionalParams      =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Request creation of a Backup long-lived process control handler, to be executed later.
        
        """
    
        if theContextualElement == None:
            return {
                'success':   False,
                'condition': cTRAToolCondition_NoContextualElement,
            }
        
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return {
                'success':   False,
                'condition': cTRAToolCondition_NoCatalogElement,
            }
        
        return unCatalogo.fCreateProgressHandlerFor_Backup(
            theAdditionalParams      =theAdditionalParams,  
            thePermissionsCache     =thePermissionsCache, 
            theRolesCache           =theRolesCache, 
            theParentExecutionRecord=theParentExecutionRecord,
        )
    
    
    
    

    security.declareProtected( permissions.View, 'fExportedFileContents')
    def fExportedFileContents( self, 
        theContextualElement    =None,
        theFileName             =None, ):
        """Retrieve the export contents  Stored as a file system file at the pre-configured path.
            
        """
    
        if theContextualElement == None:
            return None
        
        unCatalogo = theContextualElement.getCatalogo()
        if unCatalogo == None:
            return None
        
        return unCatalogo.fExportedFileContents( theFileName)
    
    
    
           