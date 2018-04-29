# -*- coding: utf-8 -*-
#
# File: TRAContribuciones_Operaciones.py
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



##code-section module-header #fill in your manual code here


import sys
import traceback


import logging

import transaction

from math import floor


from StringIO import StringIO


from Products.CMFCore.utils import getToolByName


from Products.CMFCore       import permissions


from TRAElemento_Constants                 import *
from TRAElemento_Constants_Activity        import *
from TRAElemento_Constants_Configurations  import *
from TRAElemento_Constants_Contributions   import *
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

from TRAElemento_Permission_Definitions import cBoundObject
from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_CreateTRAContribuciones

from TRAArquetipo import TRAArquetipo


class TRAContribuciones_Operaciones:
    """
    """
    security = ClassSecurityInfo()
     



    security.declarePrivate( 'pAllSubElements_into')    
    def pAllSubElements_into( self, theCollection, theAdditionalParams=None):
        if theCollection == None:
            return self
        theCollection.append( self)
        
         
        return self
        
    

    security.declarePrivate( 'pForAllElementsDo_recursive')    
    def pForAllElementsDo_recursive( self, theLambda=None, thePloneLambda=None,):
        if not theLambda:
            return self
        
        theLambda( self)        
                
        if thePloneLambda:
            self.pForAllElementsPloneDo( thePloneLambda)
    
        return self

    
    
    
        
        
    security.declareProtected( permissions.View, 'fInformeContribuciones')
    def fInformeContribuciones( self,):
        """Obtain report objects structure from the instance stored internally as the content of a string field.
        
        """
                         
        unInformeContribucionesString = self.getInformeContribuciones()
                
        unInformeContribuciones = self.fEvalString( unInformeContribucionesString)
        return unInformeContribuciones
        
             
                 
    
    
    


    security.declarePublic( 'fExtraLinks')    
    def fExtraLinks( self):
        
        unosExtraLinks = TRAArquetipo.fExtraLinks( self)
        if not unosExtraLinks:
            unosExtraLinks = [ ]
        
                       
        unElementoProgreso = self.fDeriveElementoProgreso()
        if not ( unElementoProgreso == None):
            unExtraLink = self.fNewVoidExtraLink()
            unExtraLink.update( {
                'label'   : self.fTranslateI18N( 'plone', 'Progress', 'Progress-',),
                'href'    : '%s/TRAProgressResults/' % unElementoProgreso.absolute_url(),
                'icon'    : 'traprogreso.gif',
                'domain'  : 'plone',
                'msgid'   : 'Progress',
            })
            unosExtraLinks.append( unExtraLink)        

        return unosExtraLinks
    
    
    


    security.declarePrivate( 'fDeriveElementoProgreso')
    def fDeriveElementoProgreso( self):
        
        unProgressElementId = self.getIdentificadorElementoProgreso()
        if not unProgressElementId:
            return None
        
        unCatalogo = self.getCatalogo()
        if ( unCatalogo == None):
            return None
        
        unaColeccionProgresos = unCatalogo.fObtenerColeccionProgresos()
        if ( unaColeccionProgresos == None):
            return None
        
        unElementoProgreso = unaColeccionProgresos.getElementoPorID( unProgressElementId)
        return unElementoProgreso
        
    