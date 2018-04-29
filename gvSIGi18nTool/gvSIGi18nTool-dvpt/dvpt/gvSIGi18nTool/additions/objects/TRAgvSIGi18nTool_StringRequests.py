# -*- coding: utf-8 -*-
#
# File: TRAgvSIGi18nTool_StringRequests.py
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
"""String Requests services Boundary methods (facade).

"""
    


class TRAgvSIGi18nTool_StringRequests:
    """String Requests services: Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations..
    
    """

        
    security = ClassSecurityInfo()
    

    
    security.declareProtected( permissions.View, 'fHaySolicitudesCadenasPendientes')
    def fHaySolicitudesCadenasPendientes( self , 
        theContextualElement    =None,):
    
        if theContextualElement == None:
            return False
        
        if not ( theContextualElement.meta_type == 'TRAColeccionSolicitudesCadenas'):
            return False
        
        return theContextualElement.fHaySolicitudesCadenasPendientes( )
    
                    
    
    
    
    
    
    security.declareProtected( permissions.View, 'fHaySolicitudesCadenasYaProcesadas')
    def fHaySolicitudesCadenasYaProcesadas( self , 
        theContextualElement    =None,):
    
        if theContextualElement == None:
            return False
        
        if not ( theContextualElement.meta_type == 'TRAColeccionSolicitudesCadenas'):
            return False
        
        return theContextualElement.fHaySolicitudesCadenasYaProcesadas( )
        
    
    
    

   
    
    
    
    security.declareProtected( permissions.View, 'fNewStringSymbolAcceptedReport')
    def fNewStringSymbolAcceptedReport( self, 
        theContextualElement    =None,        
        theNewStringSymbol      =None,):

        if theContextualElement == None:
            return [ False, cTRAToolCondition_NoContextualElement,]
    
        if not ( theContextualElement.meta_type == 'TRAColeccionSolicitudesCadenas'):
            return [ False, cTRAToolCondition_ContextualElementOfWrongType,]
        
        return theContextualElement.fNewStringSymbolAcceptedReport( 
            theNewStringSymbol     =theNewStringSymbol,
        )
        
               
    

    
    

    security.declareProtected( permissions.View, 'fCrearSolicitudCadena')
    def fCrearSolicitudCadena( self, 
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
        """Create a new instance of TRASolicitudCadena.
        
        """
        
        if theContextualElement == None:
            return {
                'effect':  'error', 
                'failure': cTRAToolCondition_NoContextualElement,
            }
        
        
        if not ( theContextualElement.meta_type == 'TRAColeccionSolicitudesCadenas'):
            return {
                'effect':  'error', 
                'failure': cTRAToolCondition_ContextualElementOfWrongType,
            }
    
        return theContextualElement.fCrearSolicitudCadena(
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
                         
    
    
    
    security.declareProtected( permissions.View, 'fCrearImportarYLimpiarCadenas')
    def fCrearImportarYLimpiarCadenas( self, 
        theContextualElement    =None,        
        thePermissionsCache     =None,
        theRolesCache           =None,
        theParentExecutionRecord=None):

        
        if theContextualElement == None:
            return {}
    
        if not ( theContextualElement.meta_type == 'TRAColeccionSolicitudesCadenas'):
            return {}
        
        return theContextualElement.fCrearImportarYLimpiarCadenas( 
            thePermissionsCache     =thePermissionsCache,
            theRolesCache           =theRolesCache,
            theParentExecutionRecord=theParentExecutionRecord,
        )
        
           
        
    

    
                
    security.declareProtected( permissions.View, 'fLimpiarCadenas')
    def fLimpiarCadenas( self, 
        theContextualElement    =None,
        thePermissionsCache     =None,
        theRolesCache           =None,
        theParentExecutionRecord=None):
        """Delete instances of TRASolicitudCadena not in Pending status, or for which there exist an instance of TRACadena with same string symbol.
        
        """
        
        if theContextualElement == None:
            return { 'effect': 'error', 'failure':  cTRAToolCondition_NoContextualElement, }
    
        if not ( theContextualElement.meta_type == 'TRAColeccionSolicitudesCadenas'):
            return { 'effect': 'error', 'failure':  cTRAToolCondition_ContextualElementOfWrongType, }
        
        return theContextualElement.fLimpiarCadenas( 
            thePermissionsCache      =thePermissionsCache,
            theRolesCache            =theRolesCache,
            theParentExecutionRecord =theParentExecutionRecord,
        )
    
    