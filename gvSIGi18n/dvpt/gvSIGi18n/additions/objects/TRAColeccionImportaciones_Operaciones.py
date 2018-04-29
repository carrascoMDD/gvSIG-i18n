# -*- coding: utf-8 -*-
#
# File: TRAColeccionImportaciones_Operaciones.py
#
# Copyright (c) 2008, 2009,2010 by Conselleria de Infraestructuras y Transporte de la
# Generalidad Valenciana
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



##code-section module-header #fill in your manual code here


import sys
import traceback


import logging

import transaction

from math import floor


from StringIO import StringIO


from Products.CMFCore.utils import getToolByName


from Products.CMFCore       import permissions



from TRAImportarExportar_Constants import *


class TRAColeccionImportaciones_Operaciones:
    """
    """
    security = ClassSecurityInfo()
     




    security.declarePrivate( 'pAllSubElements_into')    
    def pAllSubElements_into( self, theCollection, theAdditionalParms=None):
        if theCollection == None:
            return self
        theCollection.append( self)
        
        
        unosElementos = self.fObtenerTodasImportaciones()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pAllSubElements_into( theCollection,theAdditionalParms=theAdditionalParms)
        
        return self
        



    security.declarePrivate( 'pForAllElementsDo_recursive')    
    def pForAllElementsDo_recursive( self, theLambda):
        if not theLambda:
            return self
        
        theLambda( self)
                                    
        unosElementos = self.fObtenerTodasImportaciones()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda)
        
        return self
        
    
    
    security.declareProtected( permissions.View, 'fObtenerTodasImportaciones')
    def fObtenerTodasImportaciones( self, ):
        """Retrieve all contained elements of type TRAImportacion.
        
        """
        unosElementos = self.objectValues( cNombreTipoTRAImportacion) 
        return unosElementos
         
          
    

