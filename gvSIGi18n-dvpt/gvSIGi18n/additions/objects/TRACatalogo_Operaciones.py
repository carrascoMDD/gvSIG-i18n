# -*- coding: utf-8 -*-
#
# File: TRACatalogo_Operaciones.py
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


from TRACatalogo_Inicializacion_Constants import cTRACatalogsDetailsParaIdioma




  
from TRACatalogo_Mutators          import TRACatalogo_Mutators
from TRACatalogo_Retrieval         import TRACatalogo_Retrieval
from TRACatalogo_SearchCatalogs    import TRACatalogo_SearchCatalogs
from TRACatalogo_SimbolosOrdenados import TRACatalogo_SimbolosOrdenados


class TRACatalogo_Operaciones( TRACatalogo_Mutators, TRACatalogo_Retrieval, TRACatalogo_SearchCatalogs, TRACatalogo_SimbolosOrdenados):
    """
    """
    security = ClassSecurityInfo()

    
    
 
    security.declarePublic( 'fExtraLinks')    
    def fExtraLinks( self):
        
        unosExtraLinks = TRAArquetipo.fExtraLinks( self)
        if not unosExtraLinks:
            unosExtraLinks = [ ]
        
        unaURL = self.absolute_url()
        if not unaURL:
            return unosExtraLinks
        
        if True or self.fUseCaseCheckDoable( cUseCase_EllaborateInformeActividad):
        
            unExtraLink = self.fNewVoidExtraLink()
            unExtraLink.update( {
                'label'   : self.fTranslateI18N( 'plone', 'Activity', 'Activity',),
                'href'    : '%s/TRACatalogoActividad/' % unaURL,
                'icon'    : '',
                'domain'  : 'plone',
                'msgid'   : 'Activity',
            })
            unosExtraLinks.append( unExtraLink)
                      
            
        if self.fUseCaseCheckDoable( cUseCase_EllaborateInformeLanguages):
            unExtraLink = self.fNewVoidExtraLink()
            unExtraLink.update( {
                'label'   : self.fTranslateI18N( 'plone', 'Summary', 'Summary',),
                'href'    : '%s/TRACatalogoInforme/' % unaURL,
                'icon'    : '',
                'domain'  : 'plone',
                'msgid'   : 'Summary',
            })
            unosExtraLinks.append( unExtraLink)
                      
            
        if self.fUseCaseCheckDoable( cUseCase_EllaborateInformeModulesAndLanguages):
            unExtraLink = self.fNewVoidExtraLink()
            unExtraLink.update( {
                'label'   : self.fTranslateI18N( 'plone', 'Report', 'Report',),
                'href'    : '%s/TRACatalogoDetalle/' % unaURL,
                'icon'    : '',
                'domain'  : 'plone',
                'msgid'   : 'Report',
            })
            unosExtraLinks.append( unExtraLink)
                      
            
        return unosExtraLinks
     
    
    
    
    
    
    security.declarePrivate( 'pAllSubElements_into')        
    def pAllSubElements_into( self, theCollection, theAdditionalParams=None):
        if theCollection == None:
            return self
        theCollection.append( self)
        
        
        unosElementos = self.fObtenerTodasColeccionesIdiomas()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pAllSubElements_into( theCollection)
                
        unosElementos = self.fObtenerTodasColeccionesModulos()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pAllSubElements_into( theCollection)
                
        unosElementos = self.fObtenerTodasColeccionesCadenas()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pAllSubElements_into( theCollection)
                
        unosElementos = self.fObtenerTodasColeccionesSolicitudesCadenas()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pAllSubElements_into( theCollection)
                
        unosElementos = self.fObtenerTodasColeccionesImportaciones()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pAllSubElements_into( theCollection)
                
        unosElementos = self.fObtenerTodasColeccionesInformes()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pAllSubElements_into( theCollection)
                
        unosElementos = self.fObtenerTodasColeccionesProgresos()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pAllSubElements_into( theCollection)
    
        unosElementos = self.fObtenerTodasConfiguraciones()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pAllSubElements_into( theCollection)
                
        unElemento = self.fObtenerElementoSimbolosOrdenados()
        if not ( unElemento == None):
            unElemento.pAllSubElements_into( theCollection)
            
        return self
    

    
    
    security.declarePrivate( 'pForAllElementsDo_recursive')        
    def pForAllElementsDo_recursive( self, theLambda=None, thePloneLambda=None,):
        if not theLambda:
            return self
        
        theLambda( self)
        
        
        unosElementos = self.fObtenerTodasColeccionesIdiomas()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda, thePloneLambda)
                
        unosElementos = self.fObtenerTodasColeccionesModulos()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda, thePloneLambda)
                
        unosElementos = self.fObtenerTodasColeccionesCadenas()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda, thePloneLambda)
                
        unosElementos = self.fObtenerTodasColeccionesSolicitudesCadenas()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda, thePloneLambda)
                
        unosElementos = self.fObtenerTodasColeccionesImportaciones()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda, thePloneLambda)
                
        unosElementos = self.fObtenerTodasColeccionesInformes()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda, thePloneLambda)
                
        unosElementos = self.fObtenerTodasColeccionesContribuciones()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda, thePloneLambda)
                
        unosElementos = self.fObtenerTodasColeccionesProgresos()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda, thePloneLambda)
                
        unosElementos = self.fObtenerTodosParametrosControlProgeso()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda, thePloneLambda)
                
        unosElementos = self.fObtenerTodasConfiguraciones()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda, thePloneLambda)
                
        unElemento = self.fObtenerElementoSimbolosOrdenados()
        if not ( unElemento == None):
            unElemento.pForAllElementsDo_recursive( theLambda, thePloneLambda)
                
        if thePloneLambda:
            self.pForAllElementsPloneDo( thePloneLambda)
                
        return self    
      

        
    
    security.declarePrivate('pHandle_manage_beforeDelete')
    def pHandle_manage_beforeDelete(self, theItem, theContainer):
        """Destroy before deletion.
        Disable ZCatalog logging while deleting contents to avoid flooding the log with catalog messages complaining about keys not found. 
        Note that instances of TRACadena and TRATraduccion are not catalogged in the global ZCatalog, and therefore there are thousands of ZCatalog log entries complaining.
        This excessive logging slows down the server.
        
        """
        unResult = None
        unDisableLevelChanged = False
        try:
            aLoggerManager = logging.getLogger('Zope.ZCatalog').manager
            aDisableLevel = aLoggerManager.disable
            
            if not ( aDisableLevel == cLoggingLevel_ERROR):
                if aLoggerManager:
                    aLoggerManager.disable = cLoggingLevel_ERROR
                    unDisableLevelChanged = True
                
            unResult =  TRAArquetipo.manage_beforeDelete( self, theItem, theContainer)

        finally:
            if unDisableLevelChanged:
                if aLoggerManager:
                    aLoggerManager.disable = aDisableLevel

        return unResult
        
    
    
    
    
    


    
    security.declareProtected( permissions.View, 'getCatalogo')
    def getCatalogo( self):
        return self
        
    
    
 
 
    


    
   
    
    
    

    
        
                
        

        
    
    security.declarePrivate('pHandle_manage_afterAdd')
    def pHandle_manage_afterAdd(self, theItem, theContainer):   
        """Complete initialization after creation.
        
        """
        TRAArquetipo.manage_afterAdd(  self, theItem, theContainer)
        
        unInforme = self.fVerifyOrInitialize( 
            theAllowInitialization  =True, 
            theCheckPermissions     =False,  
            thePermissionsCache     =None, 
            theRolesCache           =None, 
            theParentExecutionRecord=None
        )
        
        return self
    
         

    
    

    

    
    
    
    
    
    

    
 