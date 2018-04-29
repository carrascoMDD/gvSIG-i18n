# -*- coding: utf-8 -*-
#
# File: TRAElemento_TraversalConfigurations.py
#
# Copyright (c) 2008, 2009,2010 by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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


from AccessControl              import ClassSecurityInfo


from Products.CMFCore           import permissions



from TRAElemento_Constants              import *

            
    


            
# ########################################################################################################
    
class TRAElemento_TraversalConfigurations:
    """Class with responsibility dealing with the retrieval of traversal specifications.
        
    """
    
    security = ClassSecurityInfo()

    


           

      
    security.declarePublic('getTraversalConfig')
    def getTraversalConfig(self):
        """Traversal config accessor.
        
        """

        unEditableConfigScriptName = self.traversalConfigScriptName()
        if unEditableConfigScriptName:
            unaConfig = self.traversalConfig_FromScript( unEditableConfigScriptName)
            if unaConfig:
                return unaConfig

        unRaiz = self.getRaiz()
        if not unRaiz:
            return None
       
        unaConfig = None
        try:
            unaConfig = unRaiz.traversalConfig()
        except:
            None
        return unaConfig
           



   



    security.declarePublic('traversalConfigScriptName')
    def traversalConfigScriptName(self):
        unRaiz = self.getRaiz()
        if not unRaiz:
            return None
         
        unTraversalConfigScriptName =  "%s_TraversalConfig_FromScript" % unRaiz.meta_type
        return unTraversalConfigScriptName






    security.declarePublic('TraversalConfig_FromScript')
    def traversalConfig_FromScript( self, theTraversalConfigName):
        if theTraversalConfigName is None or len( theTraversalConfigName) < 1:
            return None        

        aScript   = None
        try:
            aScript = self.unrestrictedTraverse(theTraversalConfigName)
        except:
            None
            
        if not aScript:
            return None

        aContext          = aq_inner(self)  
        if not aContext:
            return None
                     
        aScriptInContext  = aScript.__of__(aContext)
        if not aScriptInContext:
            return None
        
        anTraversalConfig = aScriptInContext()       
        if anTraversalConfig is None or len( anTraversalConfig) < 1:
            return None 
                   
        return anTraversalConfig

    

          




