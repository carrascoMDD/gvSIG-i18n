# -*- coding: utf-8 -*-
#
# File: TRAModulo_Operaciones.py
#
# Copyright (c) 2009 by Conselleria de Infraestructuras y Transporte de la
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
#

__author__ = """Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana <gvSIGi18n@gvSIG.org>, 
Model Driven Development sl <gvSIGi18n@ModelDD.org>, 
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo

##code-section module-header #fill in your manual code here

from Products.CMFCore       import permissions


##/code-section module-header


##code-section after-local-schema #fill in your manual code here

from TRAElemento_Constants         import *

from TRAElemento_Operaciones  import TRAElemento_Operaciones



##/code-section after-local-schema


##code-section after-schema #fill in your manual code here


##/code-section after-schema

class TRAModulo_Operaciones:
    """
    """

    security = ClassSecurityInfo()    


    ##code-section class-header #fill in your manual code here
    

    

    security.declarePrivate( 'pAllSubElements_into')    
    def pAllSubElements_into( self, theCollection, theAdditionalParms=None):
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

                       
    
    security.declarePublic( 'fExtraLinks')    
    def fExtraLinks( self):
        
        unosExtraLinks = TRAElemento_Operaciones.fExtraLinks( self)
        if not unosExtraLinks:
            unosExtraLinks = [ ]
        
        unaURL = self.getCatalogo().absolute_url()
        if not unaURL:
            return unosExtraLinks
        
        unTitle = self.Title()
        if not unTitle:
            return unosExtraLinks
        
        unExtraLink = self.fNewVoidExtraLink()
        unExtraLink.update( {
            'label'   : self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_Translate', 'Translate',),
            'href'    : '%s/TRATraducir/?theCodigoIdiomaCursor=es&theSearchNombresModulos=%s&theMostrarInforme=on&theMostrarLista=on&theIdiomasReferencia=en ' % ( unaURL, unTitle,),
            'icon'    : 'tratraduccion.gif',
            'domain'  : 'gvSIGi18n',
            'msgid'   : 'gvSIGi18n_GoTo_Root',
        })
        unosExtraLinks.append( unExtraLink)
                            
        return unosExtraLinks
     
        
    
    
    
    
    
    ##/code-section class-header

    # Methods
# end of class TRAModulo_Operaciones

##code-section module-footer #fill in your manual code here
##/code-section module-footer



