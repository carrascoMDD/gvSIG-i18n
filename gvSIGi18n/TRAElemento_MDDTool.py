# -*- coding: utf-8 -*-
#
# File: TRAElemento_MDDTool.py
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


import sys
import traceback

import logging

import transaction

import time  



from AccessControl              import ClassSecurityInfo

from Products.CMFCore           import permissions

from Products.CMFCore.utils     import getToolByName




from TRAElemento_Constants              import *




    
            
# ########################################################################################################
    
class TRAElemento_MDDTool:
    """Class with responsibility dealing with the access to the singleton tool supplying services by the ModelDDvlPlone framework.
        
    """
    
    security = ClassSecurityInfo()

    
   
    security.declarePublic( 'fModelDDvlPloneTool')
    def fModelDDvlPloneTool( self, theAllowCreation=False):
        """Retrieve or create an instance of ModelDDvlPloneTool.
        
        """
        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Inicializacion_Constants import cModelDDvlPloneToolId   
        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool import ModelDDvlPloneTool
        
        try:
                
            aModelDDvlPloneTool = getToolByName( self, 'ModelDDvlPlone_tool', None)
            
            if aModelDDvlPloneTool:
                return aModelDDvlPloneTool
            
            if not ( theAllowCreation and cInitializeAllow_CreateModelDDvlPloneTool):
                return None
     
            unPortalRoot = self.fPortalRoot()
            if not unPortalRoot:
                return None
             
            unaNuevaTool = ModelDDvlPloneTool( ) 
            unPortalRoot._setObject( cModelDDvlPloneToolId,  unaNuevaTool)
            aModelDDvlPloneTool = None
            
            aModelDDvlPloneTool = getToolByName( self, 'ModelDDvlPlone_tool', None)
            if not aModelDDvlPloneTool:
                return None
            
            transaction.commit()
                        
            return aModelDDvlPloneTool
        
        except:
            unaExceptionInfo = sys.exc_info()
            unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
            
            unInformeExcepcion = 'Exception during Lazy Initialization operation fModelDDvlPloneTool\n' 
            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
            unInformeExcepcion += unaExceptionFormattedTraceback   
                     
     
            if cLogExceptions:
                logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
    
            return None
             

        