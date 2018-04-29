# -*- coding: utf-8 -*-
#
# File: TRAgvSIGi18nTool_HTTP.py
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
"""HTTP Request services  Boundary methods (facade).

"""



class TRAgvSIGi18nTool_HTTP:
    """HTTP services: Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations..
    
    """


    security = ClassSecurityInfo()
             
        
    security.declarePublic( 'fHTTPRequest_get')
    def fHTTPRequest_get( self, 
        theContextualElement    = None,
        theRequestParameterName = None,
        theDefaultValue         = None,):
        
        if theContextualElement == None:
            return None
        

        return theContextualElement.fHTTPRequest_get( 
            theRequestParameterName = theRequestParameterName,
            theDefaultValue         = theDefaultValue,
        )
    
    
    
        
    
    security.declarePublic( 'fHTTPRequest_form_get')
    def fHTTPRequest_form_get( self, 
        theContextualElement    = None,
        theFormFieldName        = None,
        theDefaultValue         = None,):
        
        if theContextualElement == None:
            return None
        
        return theContextualElement.fHTTPRequest_form_get( 
            theFormFieldName = theFormFieldName,
            theDefaultValue  = theDefaultValue,
        )
    
    
    
    
    
    security.declarePublic( 'pHTTPResponse_headers_set')
    def pHTTPResponse_headers_set( self, 
        theContextualElement    = None,
        theHeaderName           = None,
        theHeaderValue          = None,):
            
        if theContextualElement == None:
            return self
        

        theContextualElement.pHTTPResponse_headers_set( 
            theHeaderName     = theHeaderName,
            theHeaderValue    = theHeaderValue,
        )

        return self
    
    
    
    
    
    security.declarePublic( 'pHTTPResponse_headers_add')
    def pHTTPResponse_headers_add( self, 
        theContextualElement    = None,
        theHeaderName           = None,
        theHeaderValue          = None,):
            
        if theContextualElement == None:
            return self
        

        theContextualElement.pHTTPResponse_headers_add(
            theHeaderName      = theHeaderName,
            theHeaderValue     = theHeaderValue,
        )

        return self
    
    
    
    
    
        
    security.declarePublic( 'pHTTPResponse_write')
    def pHTTPResponse_write( self, 
        theContextualElement    = None,
        theTextToWrite          = None,):
            
        if theContextualElement == None:
            return self
        

        theContextualElement.pHTTPResponse_write( 
            theTextToWrite          = theTextToWrite,
        )

        return self
    
    
    
    
        
    security.declarePublic( 'pHTTPResponse_redirect')
    def pHTTPResponse_redirect( self, 
        theContextualElement    = None,
        theURLToRedirect        = None,):
            
        if theContextualElement == None:
            return self
        

        theContextualElement.pHTTPResponse_redirect( 
            theURLToRedirect        = theURLToRedirect,
        )

        return self    
    