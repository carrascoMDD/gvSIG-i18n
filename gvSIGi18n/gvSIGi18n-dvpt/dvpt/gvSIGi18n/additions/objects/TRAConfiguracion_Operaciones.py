# -*- coding: utf-8 -*-
#
# File: TRAConfiguracion_Operaciones.py
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
#

__author__ = """Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana <gvSIGi18n@gvSIG.org>, 
Model Driven Development sl <gvSIGi18n@ModelDD.org>,
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.gvSIGi18n.config import *

##code-section module-header #fill in your manual code here

import sys
import traceback
import logging

import transaction

from Products.CMFCore       import permissions
from Products.CMFCore.utils  import getToolByName



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



##/code-section module-header



##code-section after-local-schema #fill in your manual code here



##/code-section after-local-schema



##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAConfiguracion_Operaciones:
    """
    """
    security = ClassSecurityInfo()

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    
    
    
    
    

    #security.declarePrivate( 'fConfigurationAttributeNames')    
    #def fConfigurationAttributeNames( self,):
        #"""Virtual method. Refined in subclasses.
        
        #"""
        #return []
        

    
    
    
    
    security.declarePrivate( 'fConfigurationMetaAndValues')    
    def fConfigurationMetaAndValues( self,):
        someAttributeNames = self.fConfigurationAttributeNames()
        if not someAttributeNames:
            return []
        
        someMetaAndValues = self.getAttributesMetaAndValues( losNombresAttributes=someAttributeNames)
        return someMetaAndValues
    
    
    
    
    
    
    security.declarePrivate( 'fConfigurationDict')    
    def fConfigurationDict( self,):
        
        someValues = { }
        
        someMetaAndValues = self.fConfigurationMetaAndValues()
        
        for aMetaAndValue in someMetaAndValues:
            
            if len( aMetaAndValue) > 1:
                
                anAttributeName  = aMetaAndValue[ 0]
                if anAttributeName:
                    
                    anAttributeValue = aMetaAndValue[ 1]                    
                    someValues[ anAttributeName] = anAttributeValue

        return someValues
        
    
    
    
    
    
    
    
    
        

    security.declarePrivate( 'pAllSubElements_into')    
    def pAllSubElements_into( self, theCollection, theAdditionalParams=None):
        if theCollection == None:
            return self
        theCollection.append( self)
        
        
        return self
            
    
    



    security.declarePrivate( 'pForAllElementsDo_recursive')    
    def pForAllElementsDo_recursive( self, theLambda):
        if not theLambda:
            return self
        
        theLambda( self)
        
        return self
            
            
        
        
        

                             
    
    
    
                                

# end of class TRAConfiguracion_Operaciones

##code-section module-footer #fill in your manual code here
##/code-section module-footer



