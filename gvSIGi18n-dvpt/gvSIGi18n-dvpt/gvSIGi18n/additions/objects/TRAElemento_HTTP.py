# -*- coding: utf-8 -*-
#
# File: TRAElemento_HTTP.py
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


import sys
import traceback

import logging

import transaction

import time  



from AccessControl              import ClassSecurityInfo

from Products.CMFCore           import permissions

from Products.CMFCore.utils     import getToolByName




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




            
# ########################################################################################################
    
class TRAElemento_HTTP:
    """Class with responsibility dealing with the HTTP request and response.
        
    """
    
    security = ClassSecurityInfo()

    
    
    
   
    security.declarePublic( 'fHTTPRequest')
    def fHTTPRequest( self,):
        
        aRequest = None
        try:
            aRequest = self.REQUEST
        except:
            None
        
        return aRequest
        
    
    

    
                 
   
    security.declarePublic( 'fHTTPRequest_get')
    def fHTTPRequest_get( self, 
        theRequestParameterName = None,
        theDefaultValue         = None,):
        
        if not theRequestParameterName:
            return None
        
        aHTTPRequest = self.fHTTPRequest()
        if aHTTPRequest == None:
            return None        
        
        aParameterValue = theDefaultValue
        try:
            aParameterValue = aHTTPRequest.get( theRequestParameterName, theDefaultValue)
        except:
            None
            
        return aParameterValue
        
    
    
    
             
    security.declarePublic( 'fHTTPRequest_form')
    def fHTTPRequest_form( self,):
        
        aHTTPRequest = self.fHTTPRequest()
        if aHTTPRequest == None:
            return {}        
        
        aForm = {}
        try:
            aForm = aHTTPRequest.form
        except:
            None
            
        return aForm
        
    
    
  
    security.declarePublic( 'fHTTPRequest_form_get')
    def fHTTPRequest_form_get( self, 
        theFormFieldName        = None,
        theDefaultValue         = None,):
        
        if not theFormFieldName:
            return None
        
        aHTTPForm = self.fHTTPRequest_form()
        if not aHTTPForm:
            return None        
        
        aFormFieldValue = theDefaultValue
        try:
            aFormFieldValue = aHTTPForm.get( theFormFieldName, theDefaultValue)
        except:
            None
            
        return aFormFieldValue
        
        

    
    
    
    security.declarePublic( 'fHTTPRequest_HTTP_ACCEPT_CHARSET')
    def fHTTPRequest_HTTP_ACCEPT_CHARSET( self, ):
        
        aHTTPRequest = self.fHTTPRequest()
        if aHTTPRequest == None:
            return ''        
        
        
        aHTTP_ACCEPT_CHARSET = None
        try:
            aHTTP_ACCEPT_CHARSET = aHTTPRequest.HTTP_ACCEPT_CHARSET
        except:
            None
            
        if not aHTTP_ACCEPT_CHARSET:
            return ''
        
        return aHTTP_ACCEPT_CHARSET
        
    
    
    
              
 
             
    security.declarePublic( 'fHTTPResponse')
    def fHTTPResponse( self,):
        
        aHTTPRequest = self.fHTTPRequest()
        if aHTTPRequest == None:
            return None        
        
        aResponse = None
        try:
            aResponse = aHTTPRequest.response
        except:
            None
            
        return aResponse

    
    

             
    security.declarePublic( 'fHTTPResponse_headers')
    def fHTTPResponse_headers( self,):

        aHTTPResponse = self.fHTTPResponse()
        if aHTTPResponse == None:
            return {}        
        
        someHeaders = None
        try:
            someHeaders = aHTTPResponse.headers
        except:
            None
            
        return someHeaders
    
    
    

    security.declarePublic( 'fHTTPResponse_headers_get')
    def fHTTPResponse_headers_get( self, 
        theHeaderName           = None,
        theDefaultValue         = None,):
        
        if not theHeaderName:
            return None
        
        someHeaders = self.fHTTPResponse_headers()
        if not someHeaders:
            return None        
        
        aHeaderValue = theDefaultValue
        try:
            aHeaderValue = someHeaders.get( theHeaderName, theDefaultValue)
        except:
            None
            
        return aHeaderValue
    
   
    
    

    security.declarePublic( 'pHTTPResponse_headers_set')
    def pHTTPResponse_headers_set( self, 
        theHeaderName           = None,
        theHeaderValue          = None,):
        
        if not theHeaderName:
            return None
        
        aHTTPResponse = self.fHTTPResponse()
        if aHTTPResponse == None:
            return self        
        
        try:
            aHTTPResponse.setHeader( theHeaderName, theHeaderValue)
        except:
            None
            
        return self
    
    
   

    security.declarePublic( 'pHTTPResponse_headers_add')
    def pHTTPResponse_headers_add( self, 
        theHeaderName           = None,
        theHeaderValue          = None,):
        
        if not theHeaderName:
            return None
        
        aHTTPResponse = self.fHTTPResponse()
        if aHTTPResponse == None:
            return self        
        
        try:
            aHTTPResponse.addHeader( theHeaderName, theHeaderValue)
        except:
            None
            
        return self
        
    
    
    
    
    
    security.declarePublic( 'pHTTPResponse_write')
    def pHTTPResponse_write( self, 
        theTextToWrite          = None,):
        
        if not theTextToWrite:
            return None
        
        aHTTPResponse = self.fHTTPResponse()
        if aHTTPResponse == None:
            return self        
        
        try:
            aHTTPResponse.write( theTextToWrite)
        except:
            None
            
        return self

            
    
    
     
    
    
    
    security.declarePublic( 'pHTTPResponse_redirect')
    def pHTTPResponse_redirect( self, 
        theURLToRedirect        = None,):
        
        if not theURLToRedirect:
            return None
        
        aHTTPResponse = self.fHTTPResponse()
        if aHTTPResponse == None:
            return self        
        
        try:
            aHTTPResponse.redirect( theURLToRedirect)
        except:
            None
            
        return self

            
    
        
    
    