# -*- coding: utf-8 -*-
#
# File: TRACatalogo_SearchCatalogs.py
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



from TRACatalogo_Inicializacion import cNombreCatalogoBusquedaCadenas, cNombreCatalogoFiltroCadenas, cNombreCatalogoTextoCadenas, cNombreCatalogoBusquedaTraducciones, cNombreCatalogoFiltroTraducciones, cNombreCatalogoTextoTraducciones




from TRAElemento_Permission_Definitions import cBoundObject
from TRAElemento_Permission_Definitions import cTRAUserGroups_Catalogo, cTRAUserGroups_Catalogo_AuthorizedOnIndividualIdiomas, cTRAUserGroups_Catalogo_AuthorizedOnIndividualModulos

from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_LockTRACatalogo, cUseCase_UnlockTRACatalogo, cUseCase_EllaborateInformeActividad, cUseCase_EllaborateInformeLanguages, cUseCase_EllaborateInformeModulesAndLanguages






class TRACatalogo_SearchCatalogs:
    """
    """
    security = ClassSecurityInfo()

    
    
    

    
      
    # #############################################################
    """Catalog accessors
    
    """
    
   
         
    security.declarePrivate('fCatalogNamed')
    def fCatalogNamed(self, theCatalogOwner, theCatalogName):
        if not theCatalogOwner or not theCatalogName:
            return None  
        
        aCatalog = None
        try:
            aCatalog = aq_get( theCatalogOwner, theCatalogName, None, 1)
        except:
            None        
        return aCatalog
        
        
    
    security.declarePrivate('fCatalogBusquedaCadenas')
    def fCatalogBusquedaCadenas(self):
        return self.fCatalogNamed( self, cNombreCatalogoBusquedaCadenas)
    
    
    
    security.declarePrivate('fCatalogFiltroCadenas')
    def fCatalogFiltroCadenas(self):
        return self.fCatalogNamed( self, cNombreCatalogoFiltroCadenas)
    
     
    security.declarePrivate('fCatalogTextoCadenas')
    def fCatalogTextoCadenas(self):
        return self.fCatalogNamed( self, cNombreCatalogoTextoCadenas)
    
    
    
         
        

    security.declarePrivate('fCatalogBusquedaTraduccionesParaIdioma')
    def fCatalogBusquedaTraduccionesParaIdioma(self, theIdioma):
        if not theIdioma:
            return None
        return self.fCatalogNamed( theIdioma, cNombreCatalogoBusquedaTraducciones)
    
    
    
    security.declarePrivate('fCatalogFiltroTraduccionesParaIdioma')
    def fCatalogFiltroTraduccionesParaIdioma(self, theIdioma):
        if not theIdioma:
            return None
        return self.fCatalogNamed( theIdioma, cNombreCatalogoFiltroTraducciones)

    
    
    
    security.declareProtected( permissions.View, 'fCatalogFiltroTraduccionesParaIdiomaPorCodigo')    
    def fCatalogFiltroTraduccionesParaIdiomaPorCodigo(self, theCodigoIdioma):
        if not theCodigoIdioma:
            return []
        
        unIdioma = self.fGetIdiomaPorCodigo( theCodigoIdioma)
        if not unIdioma:
            return None
        return self.fCatalogFiltroTraduccionesParaIdioma( unIdioma)    
      
  
    
        
    security.declarePrivate('fCatalogTextoTraduccionesParaIdioma')
    def fCatalogTextoTraduccionesParaIdioma(self, theIdioma):
        if not theIdioma:
            return None
        return self.fCatalogNamed( theIdioma, cNombreCatalogoTextoTraducciones)
 
    

    
 