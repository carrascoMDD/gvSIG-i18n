# -*- coding: utf-8 -*-
#
# File: TRAElemento_Log.py
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




import logging


from AccessControl              import ClassSecurityInfo


from Products.CMFCore           import permissions



from TRAElemento_Constants              import *


       
            
            
    
            
# ########################################################################################################
    
class TRAElemento_Log:
    """Class with responsibility dealing with writting entries to the Plone log.
        
    """
    
    
    security = ClassSecurityInfo()

      
    
    security.declarePublic( 'pLog')    
    def pLog( self, theMessage):
                
        logging.getLogger( 'gvSIGi18n').info( self.fReprAsString( theMessage))
        
        return self
    
    
 
        
     
    
    security.declarePrivate( 'pLogChange')    
    def pLogChange( self, theChangeDescriptionString, theEncoding='', theTranslationService=None):
        if not theChangeDescriptionString:
            return self
        
        unEncodedString = self.fEncodeLogString( theChangeDescriptionString)
 
        logging.getLogger( 'gvSIGi18n').info( unEncodedString)
        return self
    
       

    
    
    
    
    security.declarePrivate( 'pLogHTTPRequest')    
    def pLogHTTPRequest( self, theLogRequesterLabel ):
        
        anHTTPRequest = self.REQUEST
        if not anHTTPRequest:
            return self
        
        unDumpBuffer = StringIO()
        unaForm = anHTTPRequest.form
        if not unaForm:
            logging.getLogger( theLogRequesterLabel).info( "theRequest: NO FORM\n")
            return self

        unasFormKeys = unaForm.keys()
        unMaxKeyLen = max( [ len( unaKey) for unaKey in unasFormKeys])
        for unaFormKey in unasFormKeys:
            unDumpBuffer.write( '%s%s %s\n' % ( unaFormKey, '' * ( unMaxKeyLen - len( unaFormKey)), unaForm.get( unaFormKey, ''),))

        logging.getLogger( theLogRequesterLabel).info( "theRequest:\n%s\n" % unDumpBuffer.getvalue())
        
        return self

       

   
    
    

    