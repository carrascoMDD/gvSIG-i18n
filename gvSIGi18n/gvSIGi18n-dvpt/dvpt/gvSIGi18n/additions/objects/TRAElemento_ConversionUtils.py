# -*- coding: utf-8 -*-
#
# File: TRAElemento_ConversonUtils.py
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


import cgi

import sys
import traceback

import logging

import transaction

import time  


from logging import ERROR as cLoggingLevel_ERROR

from codecs                     import lookup   as CODECS_Lookup

from DateTime                   import DateTime

from StringIO                   import StringIO

from AccessControl              import ClassSecurityInfo

from Acquisition                import aq_inner, aq_parent


from OFS.CopySupport            import CopyContainer


from Products.Archetypes.utils  import shasattr

from Products.CMFCore           import permissions

from Products.CMFCore.utils     import getToolByName


from Products.Archetypes.atapi  import OrderedBaseFolder, BaseBTreeFolder

from Products.PloneLanguageTool import availablelanguages as PloneLanguageToolAvailableLanguages


from TRAElemento_Constants                 import *
from TRAElemento_Constants_Activity        import *
from TRAElemento_Constants_Configurations  import *
from TRAElemento_Constants_Dates           import *
from TRAElemento_Constants_Encoding        import *
from TRAElemento_Constants_Import          import *
from TRAElemento_Constants_Languages       import *
from TRAElemento_Constants_Logging         import *
from TRAElemento_Constants_Modules         import *
from TRAElemento_Constants_Profiling       import *
from TRAElemento_Constants_Progress        import *
from TRAElemento_Constants_String          import *
from TRAElemento_Constants_StringRequests  import *
from TRAElemento_Constants_Translate       import *
from TRAElemento_Constants_Translation     import *
from TRAElemento_Constants_TypeNames       import *
from TRAElemento_Constants_Views           import *
from TRAElemento_Constants_Vocabularies    import *
from TRAUtils                              import *



        



from TRACatalogo_Globales    import TRACatalogo_Globales


   
            
            
            
    
            
# ########################################################################################################
    
class TRAElemento_ConversionUtils:
    """Class with responsibility to convert between objects and their string representations.
        
    """
    
    security = ClassSecurityInfo()


      

    
    
    security.declarePublic( 'fAsCollection')    
    def fAsCollection( self, theObject):
        
        if theObject == None:
            return []
        
        if isinstance( theObject, list):
            return theObject
        
        if isinstance( theObject, tuple):
            return list ( theObject)
        
        if isinstance( theObject, set):
            return list ( theObject)
        
        return [ theObject,]
    

     

    
    #security.declarePublic( 'fIsCollection')    
    #def fIsCollection( self, theObject):
        #if theObject == None:
            #return False
        #return isinstance( theObject, type( [])) or isinstance( theObject, type( (1,2))) or isinstance( theObject, type( set())) 
    
         
    
    
    
    
    

    security.declarePublic( 'fDefaultEvalStringGlobalsDict')    
    def fDefaultEvalStringGlobalsDict(self, ):
        return { '__builtins__':None, 'True': True, 'False': False, 'None': None, 'DateTime': DateTime,}.copy()
        
    
    
    security.declarePrivate( 'fEvalString')
    def fEvalString(self, theString, theExtraGlobals={}):
        """Safe evaluation of strings as data structures.
        
        """
        if not theString:
            return None
        
        unGlobalsDict = self.fDefaultEvalStringGlobalsDict()
        if not unGlobalsDict:
            unGlobalsDict = { '__builtins__':None, }
            
        unGlobalsDict = unGlobalsDict.copy()
        if theExtraGlobals:
            unGlobalsDict.update( theExtraGlobals)
            
        unValue = None
        try:
            unValue = eval( theString, unGlobalsDict)
        except:
            unGlobalsString = str( unGlobalsDict.keys()).replace( '[', '').replace( ']', '')
            logging.getLogger( 'gvSIGi18n').error( 'fEvalString( "%s", { %s })' % ( str( theString), unGlobalsString))
            
        return unValue
     
    
    
    
    
    security.declarePublic( 'fReprAsString')        
    def fReprAsString( self, theObject):
        """Representation of data structures as strings.
        
        """
        
        from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fReprAsString
        return fReprAsString( theObject)
    
    

    
    
    
    
    