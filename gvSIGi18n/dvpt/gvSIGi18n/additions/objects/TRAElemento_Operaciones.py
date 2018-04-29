# -*- coding: utf-8 -*-
#
# File: TRAElemento_Operaciones.py
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



from AccessControl              import ClassSecurityInfo

from Products.CMFCore           import permissions



from TRAElemento_Constants              import *



  
    
            
# ########################################################################################################
    
class TRAElemento_Operaciones:
    """CLASS: base class for all application elements, with commonly used behaviours aand service access points
        
    """
    
    security = ClassSecurityInfo()

    

    
    security.declarePublic( 'fExtraLinks')    
    def fExtraLinks( self):
        
        unosExtraLinks = [ ]
        
        unaURL = self.getCatalogo().absolute_url()
        if not unaURL:
            return unosExtraLinks
        
        unExtraLink = self.fNewVoidExtraLink()
        unExtraLink.update( {
            'label'   : self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_GoTo_Root', 'Go Root',),
            'href'    : '%s/TRACatalogo/' % unaURL,
            'icon'    : 'tra_root.gif',
            'domain'  : 'gvSIGi18n',
            'msgid'   : 'gvSIGi18n_GoTo_Root',
        })
        unosExtraLinks.append( unExtraLink)
                            
        return unosExtraLinks
    
    
  




    # #############################################################
    """Metainfo access methods not directly available on instances from templates or scripts.
    
    """


    security.declarePublic('getModule')
    def getModule(self):
        return __module__
        



    security.declarePublic('getClassName')
    def getClassName(self):
        return self.__class__.__name__
        
        
        
    security.declarePublic('getMethods')
    def getMethods(self):
        return dir(self)
        
        
    security.declarePublic('getDoc')
    def getDoc(self):
        return self.__doc__
        
        




    
    
    
    

    