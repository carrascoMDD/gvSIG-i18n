# -*- coding: utf-8 -*-
#
# File: TRACatalogo_SimbolosOrdenados.py
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

from logging import ERROR as cLoggingLevel_ERROR

import transaction

from StringIO                       import StringIO

from Acquisition                    import aq_get

from AccessControl                  import ClassSecurityInfo

from Products.CMFCore               import permissions

from Products.Archetypes.utils      import shasattr
from Products.Archetypes.public     import DisplayList

from Products.CMFCore.utils         import getToolByName


from TRAArquetipo import TRAArquetipo


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







  



class TRACatalogo_SimbolosOrdenados:
    # #######################################################################
    """Methods to access Cached sorted simbolos cadenas, and another cache grouped by module and also sorted by simbolo cadena
    
    """
    security = ClassSecurityInfo()

    
    
    

    
    
    security.declareProtected( permissions.View, 'fObtenerElementoSimbolosOrdenados')
    def fObtenerElementoSimbolosOrdenados( self,):
        
        unElemento = self.getElementoPorID( cTRASimbolosOrdenados_Id)
        
        return unElemento
    
            
    
    
    

    security.declarePrivate( 'fListaSimbolosCadenasOrdenados')
    def fListaSimbolosCadenasOrdenados( self,theParentExecutionRecord=None):
        
        unElementoSimbolosOrdenados = self.fObtenerElementoSimbolosOrdenados()
        if unElementoSimbolosOrdenados == None:
            return []
        
        unosSimbolos = unElementoSimbolosOrdenados.fListaSimbolosCadenasOrdenados( 
            theParentExecutionRecord=theParentExecutionRecord,
        )
        
        return unosSimbolos
        
    
    
    
    
    
        
    security.declarePrivate( 'fListaSimbolosCadenasOrdenadosEnModulo')
    def fListaSimbolosCadenasOrdenadosEnModulo( self, theNombreModulo,  theParentExecutionRecord=None):

        unElementoSimbolosOrdenados = self.fObtenerElementoSimbolosOrdenados()
        if unElementoSimbolosOrdenados == None:
            return []
        
        unosSimbolos = unElementoSimbolosOrdenados.fListaSimbolosCadenasOrdenadosEnModulo( 
            theNombreModulo=theNombreModulo, 
            theParentExecutionRecord=theParentExecutionRecord,
        )

        return unosSimbolos
    
    
    
    
    
    
    
    security.declarePrivate( 'fListaSimbolosCadenasOrdenadosEnVariosModulos')
    def fListaSimbolosCadenasOrdenadosEnVariosModulos( self, theNombresModulos,  theIncludeModuloNoEspecificado, theParentExecutionRecord=None):
        
        unElementoSimbolosOrdenados = self.fObtenerElementoSimbolosOrdenados()
        if unElementoSimbolosOrdenados == None:
            return []
        
        unosSimbolos = unElementoSimbolosOrdenados.fListaSimbolosCadenasOrdenadosEnVariosModulos( 
            theNombresModulos              =theNombresModulos, 
            theIncludeModuloNoEspecificado = theIncludeModuloNoEspecificado,
            theParentExecutionRecord       =theParentExecutionRecord,
        )

        return unosSimbolos

    
   
    
    
    
    
    security.declarePrivate( 'fListaSimbolosCadenasEnVariosModulosStrictly')
    def fListaSimbolosCadenasEnVariosModulosStrictly( self, theNombresModulos,  theIncludeModuloNoEspecificado, theParentExecutionRecord=None):
        
        unElementoSimbolosOrdenados = self.fObtenerElementoSimbolosOrdenados()
        if unElementoSimbolosOrdenados == None:
            return []
        
        unosSimbolos = unElementoSimbolosOrdenados.fListaSimbolosCadenasEnVariosModulosStrictly( 
            theNombresModulos              =theNombresModulos, 
            theIncludeModuloNoEspecificado =theIncludeModuloNoEspecificado,
            theParentExecutionRecord       =theParentExecutionRecord,
        )
    
        return unosSimbolos
   

    
    
    
    security.declarePrivate( 'fListaSimbolosCadenasOrdenadosModuloNoEspecificado')
    def fListaSimbolosCadenasOrdenadosModuloNoEspecificado( self,  theParentExecutionRecord=None):
        
        unElementoSimbolosOrdenados = self.fObtenerElementoSimbolosOrdenados()
        if unElementoSimbolosOrdenados== None:
            return []
        
        unosSimbolos = unElementoSimbolosOrdenados.fListaSimbolosCadenasOrdenadosModuloNoEspecificado( 
            theParentExecutionRecord       =theParentExecutionRecord,
        )
    
        return unosSimbolos
    
             
            
        


     
    
    
    security.declareProtected( permissions.ModifyPortalContent, 'pInvalidateSimbolosCadenasOrdenados')    
    def pInvalidateSimbolosCadenasOrdenados( self):
        unElementoSimbolosOrdenados = self.fObtenerElementoSimbolosOrdenados()
        if unElementoSimbolosOrdenados == None:
            return self

        unElementoSimbolosOrdenados.pInvalidateSimbolosCadenasOrdenados()
        
        return self
            
    
    
    

    
 