# -*- coding: utf-8 -*-
#
# File: Cadena_operations.py
#
# Copyright (c) 2008, 2009 by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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

from Products.Archetypes.BaseObject     import BaseObject

from Products.Archetypes.atapi          import OrderedBaseFolder



from AccessControl      import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName
from Products.CMFCore       import permissions

from Products.Archetypes.utils import shasattr


from TRAElemento_Constants         import *


from TRAElemento import TRAElemento

cLogWhileImporting = True



  


class TRACadena_Operaciones:
    """
    """
    security = ClassSecurityInfo()




    
# ####################################
#  Derived accessors for dates stored as text
# ####################################

    
    security.declarePrivate('getFechaCreacion')
    def getFechaCreacion( self,): 
        return self.fFechaCreacionDesdeTextual()
          

    security.declarePrivate('fFechaCreacionDesdeTextual')
    def fFechaCreacionDesdeTextual( self, ): 
        unaString = self.getFechaCreacionTextual()
        unaDate = self.fStoreStringToDate( unaString)
        return unaDate
    
    
    security.declarePrivate('fFechaCancelacionDesdeTextual')
    def fFechaCancelacionDesdeTextual( self, ): 
        unaString = self.getFechaCancelacionTextual()
        unaDate = self.fStoreStringToDate( unaString)
        return unaDate
    
    
    
    security.declarePrivate('pSetFechaCreacion')
    def pSetFechaCreacion( self, theDate): 
        
        unaString = self.fDateToStoreString( theDate)
        if unaString:
            self.setFechaCreacionTextual( unaString)
        return self
    
    
    security.declarePrivate('setFechaCreacion')
    def setFechaCreacion( self, theDate): 
        return self.pSetFechaCreacion( theDate)
     
    
    security.declarePrivate('pSetFechaCancelacion')
    def pSetFechaCancelacion( self, theDate): 
        
        unaString = self.fDateToStoreString( theDate)
        if unaString:
            self.setFechaCancelacionTextual( unaString)
        return self
    
    
    security.declarePrivate('setFechaCancelacion')
    def setFechaCancelacion( self, theDate): 
        return self.pSetFechaCancelacion( theDate)
     
     
       



    
# ####################################
#  Derived accessors for related TRAModulo
# ####################################
     
    security.declarePrivate('fObtenerModulo')
    def fObtenerModulo( self, ):   
        unosModulos = self.fObtenerModulos()
        if not unosModulos:
            return None
        return unosModulos[ 0]
    
        
    
    
    security.declarePrivate('fObtenerModulos')
    def fObtenerModulos( self, ):   
        unCatalogo = self.getCatalogo()
        if not unCatalogo:
            return []
        unosNombresModulos = self.fListaNombresModulos()
        if not unosNombresModulos:
            return None
        
        unosModulos = [ ]
        for unNombreModulo in unosNombresModulos:
            unModulo = unCatalogo.fGetModuloPorNombre( unNombreModulo)
            if unModulo:
                unosModulos.append( unModulo)
    
        return unosModulos
    
    
    
    
   
   
    security.declarePrivate( 'fListaNombresModulos')    
    def fListaNombresModulos( self):
        
        unosNombresModulosString = self.getNombresModulos()
        if not unosNombresModulosString:
            return []
        unosNombresModulos = unosNombresModulosString.splitlines()
           
        return unosNombresModulos
    
    
    
    
    security.declarePrivate( 'fAppendNombresModulos')    
    def fAppendNombresModulos( self, theNombresModulos):
        if not theNombresModulos:
            return False
        
        unosNombresModulos = self.fListaNombresModulos()
           
        unosNuevosNombresModulos = unosNombresModulos[:] 
        unChanged = False    
        for unNombreModulo in theNombresModulos:
            if not( unNombreModulo in unosNombresModulos):
                unosNuevosNombresModulos.append( unNombreModulo)
                unChanged = True
         
        if not unChanged:
            return False
               
        unosNuevosNombresModulosString = '\n'.join( unosNuevosNombresModulos)
        self.setNombresModulos( unosNuevosNombresModulosString)       
        
        return True
    
    
    
    
    security.declarePrivate( 'fAppendSources')    
    def fAppendSources( self, theSources):
        if not theSources:
            return False
        
        unasReferenciasFuentes = self.getReferenciasFuentes()
        if not ( unasReferenciasFuentes.find( theSources) >=0):
            unasReferenciasFuentes = '%s %s' % ( unasReferenciasFuentes, theSources,)
            if unasReferenciasFuentes:
                self.setReferenciasFuentes( unasReferenciasFuentes)
                return True
    
        return False
    
    
# #########################################################################
#   Unique path for catalogs
# ################## 
    
    security.declarePrivate( 'fCatalogKey')
    def fCatalogKey( self):
        return '/'.join( self.getPhysicalPath())
    
   
    
# #########################################################################
#   Accessor for simbolo in fragments for textual search
# ##################    

  
    security.declarePrivate( 'fGetSimboloEnPalabras')
    def fGetSimboloEnPalabras(self):
        unSimbolo = self.getSimbolo()
        if not unSimbolo:
            return ''
        
        unSimboloConEspacios = unSimbolo
        for unChar in [ '_', '-', ',', '.', ':', '\n', '\r', '\t',]:
            unSimboloConEspacios = unSimboloConEspacios.replace( unChar, ' ')
        unSimboloEnPalabras = ' '.join( unSimboloConEspacios.split())
        return unSimboloEnPalabras
    
  
    

    
    
# ####################################
#  Complete initialization after creation
#
        
# let's see the delegation path through multiple inheritance...
# TRAElemento.manage_afterAdd
#   TRAElemento_Operaciones.pHandle_manage_afterAdd
#       OrderedBaseFolder. --- no method
#           BaseFolder -- no method
#               BaseFolderMixin.manage_afterAdd  
#                   BaseObject.manage_afterAdd
#                       Referenceable.manage_afterAdd
#                           deals with REFERENCE_CATALOG
#                       self.initializeLayers(item, container)
#                   CatalogMultiplex.manage_afterAdd (has no method)
#                       CMFCatalogAware.manage_afterAdd
#                            self.indexObject()
#                           self.__recurse('manage_afterAdd', item, container)
#               ExtensibleMetadata --- no called, no method
#                   Persistence.Persistent - just an indicator
#
#           OrderedContainer - just moves and interfaces
#
#  So, from TRACadena and TRATRaduccion,
#   that we don't want to get catalogged in the portal catalog      
#   let's try and see if we can delegate directly to BaseObject
#   adding to the catalogs and the permissions being invoked by import process
#
#  Well, the  TRACadena and TRATRaduccion still appear in the portal_catalog
#     must be some parent being reindexed, and the __recurse( 'manage_afterAdd',
#     adding them to the catalog ? No this can't be 
#
#  Must be some invocation from the factory code.
#   may be we should just remove from the catalog ...
#   but first we'll try and find where is it being added to the catalog
#
#  We found the invocation chain:
#   unaIdNuevaCadena = theColeccionCadenas.invokeFactory( cNombreTipoTRACadena, aNewIdWithCounter, **anAttrsDict)
#   Products.CMFCore.TypesTool.constructContent
#   Products.CMFCore.TypeInformation.constructInstance
#   Products.CMFCore.TypeInformation._finishConstruction( ob)
#   that calls ob.reindexObject()
#
#   The CatalogMultiplex ancestor of TRACadena and TRATraduccion
#   implements reindexObject() with comment:
#    """update indexes of this object in all registered catalogs.
#
#        Catalogs are registered per 'meta_type' in archetypes tool.
#
#        'idxs' are a list of index names. If this list is given only the given
#        indexes are refreshed. If a index does not exist in catalog its
#        silently ignored.
#        """
#   The CMFCatalogAware superclass of CatalogMultiplex, also implements reindexObject()
#       but CMFCatalogAware does not delegate on it
#    """
#            Reindex the object in the portal catalog.
#            If idxs is present, only those indexes are reindexed.
#            The metadata is always updated.
#
#            Also update the modification date of the object,
#            unless specific indexes were requested.
#        """    
#
#   There are no other (we find no other) significant implementation of reindexObject
#      in the multiple inheritance of TRACAdena and TRATraduccion
#      there are other implementors, like PortalFolder not in the inheritance chain, but just saying "pass"
#
# So what we can do is to implement reindexObject on the TRACadena and TRATraduccion concrete classes,
# do not delegate on 
# delegate on the corresponding _Operations class
# and there reindex only on the TRACAdena and TRATraduccion specific catalogs
#
   
    security.declarePrivate('pHandle_reindexObject')
    def pHandle_reindexObject(self, idxs=[]):  
        
        self.pRecatalogCadena( )

        return self
    
    
    
    
    
    security.declarePrivate('pHandle_manage_afterAdd')
    def pHandle_manage_afterAdd(self, theItem, theContainer):   
       
        # ACV 20090504 Avoid catalogging the TRATraduccion into the UID catalog,
        # by not delegating into Referenceable superclass,
        # BaseObject.manage_afterAdd( self, theItem, theContainer)
        
        BaseObject.initializeLayers( self, theItem, theContainer)

        
        return self
    
 
    
   
    

    
    
    
# ####################################
#  Destroy before deletion
#
        
    
    security.declarePrivate('pHandle_manage_beforeDelete')
    def pHandle_manage_beforeDelete(self, theItem, theContainer):   
 
        TRAElemento.manage_beforeDelete( self, theElement, theContainer)
         
        unCatalogoRaiz = self.getCatalogo()
        if unCatalogoRaiz:
            
            unCatalogKey = theElement.fCatalogKey()
            
            unCatalogBusquedaCadenas = unCatalogoRaiz.fCatalogBusquedaCadenas()
            if not( unCatalogBusquedaCadenas == None):
                unCatalogBusquedaCadenas.uncatalog_object( unCatalogKey)
             
            unCatalogFiltroCadenas   = unCatalogoRaiz.fCatalogFiltroCadenas()
            if not( unCatalogFiltroCadenas == None):
                unCatalogFiltroCadenas.uncatalog_object(   unCatalogKey)
    
            unCatalogTextoCadenas   = unCatalogoRaiz.fCatalogTextoCadenas()
            if not( unCatalogTextoCadenas == None):
                unCatalogTextoCadenas.uncatalog_object(    unCatalogKey)

        return self
     
    
    
   
    
# #########################################################################
#   Derivacion de referencias
# ##################    

         
    security.declarePrivate( 'getCatalogo')
    def getCatalogo( self):
        unCatalogo = self.getPropietario()
        if not (unCatalogo.__class__.__name__ == cNombreTipoTRACatalogo):
            return None
        return unCatalogo
        





    
    
    

    
# #########################################################################
#   Acceso a instancias de TRATraduccion de la TRACadena
# ##################    

    
    security.declarePrivate( 'fObtenerTodasTraducciones')
    def fObtenerTodasTraducciones( self, ):
   
        unasTraducciones = self.objectValues( cNombreTipoTRATraduccion) #
        return unasTraducciones
           
    
    

    security.declarePrivate( 'fObtenerTraduccionEnIdioma')
    def fObtenerTraduccionEnIdioma( self, theIdioma):
   
        if not theIdioma:
            return None

        unCodigoIdioma      = theIdioma.getCodigoIdiomaEnGvSIG()
                    
        aTraduccionId       = self.fIdTraduccionEnLenguage( unCodigoIdioma)

        unaTraduccionPorId = self.getTraduccionPorID( aTraduccionId)

        return unaTraduccionPorId         
        
           
        
        
     


    security.declarePrivate( 'fTraduccionesPorIdiomas')
    def fTraduccionesPorIdiomas( self, theCodigosIdiomas, thePloneUtilsTool):
        if not theCodigosIdiomas:
            return {}
        
        unasTraduccionesPorIdiomas = { }
        
        for unCodigoIdioma in theCodigosIdiomas:
            aTraduccionId = self.fIdTraduccionEnLenguage( unCodigoIdioma, thePloneUtilsTool)
            if aTraduccionId:
                unaTraduccionPorId = self.getTraduccionPorID( aTraduccionId)
                if unaTraduccionPorId:
                    unasTraduccionesPorIdiomas[ unCodigoIdioma] = unaTraduccionPorId
        
        return unasTraduccionesPorIdiomas
    
    
        

    
    
    
    
    
    
    
    
    
    
    # #########################################################################
    #   Factorias de  TRATraduccion
    # ##########################################################################
    

    #security.declarePrivate('fCrearTraduccionQueFalta')
    #def fCrearTraduccionSiFalta( self, 
        #theCodigoIdioma, 
        #theMemberId, 
        #thePloneUtilsTool, 
        #theCatalogBusquedaTraducciones, 
        #theCatalogFiltroTraducciones, 
        #theCatalogTextoTraducciones):
        #if not theCodigoIdioma:
            #return None
            
        #unSimboloCadena = self.getSimbolo()
        #unaIdCadena     = self.getId()
        #unTitulo = '%s-%s' % ( unSimboloCadena, theCodigoIdioma)
        #aNewId = self.fIdTraduccionEnLenguage( theCodigoIdioma, thePloneUtilsTool)
        
        #unaTraduccionExistente   = self.getElementoPorID( aNewId)
        #if unaNuevaTraduccion:
            #return [ 'exists', unaNuevaTraduccion, ]
        
        #anAttrsDict = { 
            #'pathDelRaiz':          self.fPathDelRaiz(),
            #'title':                unTitulo,
            #'description':          '',
            #'simbolo':              unSimboloCadena,
            #'codigoIdiomaEnGvSIG':  theCodigoIdioma, 
            #'estadoCadena':         cEstadoCadenaActiva,
            #'idCadena':             unaIdCadena,
            #'nombresModulos':       '',
            #'estadoTraduccion'   :  cEstadoTraduccionPendiente,
            #'cadenaTraducida'    :  '',
            #'usuarioTraductor':     '', 
            #'fechaTraduccion':      None,  
            #'usuarioRevisor':       None, 
            #'fechaRevision':        None,  
            #'fechaDefinitivo':      None,  
            #'comentario':           "",   
            #'historia':             "",            
        #}
        
        #unaIdNuevaTraduccion = self.invokeFactory( cNombreTipoTRATraduccion, aNewId, **anAttrsDict)
        #if not unaIdNuevaTraduccion:
            #return [ 'failed', None]
        #unaNuevaTraduccion   = self.getElementoPorID( unaIdNuevaTraduccion)
        #if not unaNuevaTraduccion:
            #return [ 'failed', None]
            
        #unaNuevaTraduccion.pAddToCatalogs( theCatalogBusquedaTraducciones, theCatalogFiltroTraducciones, theCatalogTextoTraducciones)        
        
        #unaNuevaTraduccion.manage_fixupOwnershipAfterAdd()
        #unaNuevaTraduccion.pSetPermissions()
                
        #return [ 'created', unaNuevaTraduccion]

    
    
    
        
          
 


    
        
    
    # #########################################################################
    #   Metodos para propagacion de la TRACadena a sus TRATraduccion
    # ##########################################################################
    


    
    # #########################################################################
    #   Propagacion de la TRACadena de cambio del estado de la cadena
    #   de activo a inactivo, a sus TRATraduccion
    # ##########################################################################
      
    security.declarePrivate('pPropagarCambioDeEstadoATraducciones')
    def pPropagarCambioDeEstadoATraducciones( self):
        unEstadoCadena = self.getEstadoCadena()
        
        unasTraducciones = self.fObtenerTodasTraducciones()
        for unaTraduccion in unasTraducciones:
            unaTraduccion.setEstadoCadena( unEstadoCadena)
            unaTraduccion.pRecatalogTraduccion()
        return self
      
    
    
    
    
    

    security.declarePrivate('fPropagarCambioNombresModulosATraducciones')
    def fPropagarCambioNombresModulosATraducciones( self):
        unosNombresModulos = self.getNombresModulos()
        
        unasTraducciones = self.fObtenerTodasTraducciones()
        for unaTraduccion in unasTraducciones:
            unaTraduccion.setNombresModulos( unosNombresModulos)
            unaTraduccion.pRecatalogTraduccion()
        return len( unasTraducciones)
      
    
    
    
    
    
    
    
    
    
        
    # #########################################################################
    #   Maintenance of TRACadena in indexed ZCatalogs
    # ##########################################################################
    

 
    
    
    
    
    security.declarePrivate( 'pRecatalogCadenaYTraducciones')    
    def pRecatalogCadenaYTraducciones( self, theCadena):        
        self.pRecatalogCadena()
            
        unasTraducciones = self.fObtenerTodasTraducciones()
        for unaTraduccion in unasTraducciones:
            unaTraduccion.pRecatalogTraduccion()
            
        return self
    
    
    
    
    
    
    
    
    

    security.declarePrivate( 'pRecatalogCadena')    
    def pRecatalogCadena( self,):
        self.pAddToCatalogs()
        return self
    
    
    
    
    
    security.declarePrivate('pAddToCatalogs')
    def pAddToCatalogs(self, theCatalogBusquedaCadenas=None, theCatalogFiltroCadenas=None, theCatalogTextoCadenas=None):
    
        unCatalogoRaiz = None
        if not theCatalogBusquedaCadenas or not theCatalogFiltroCadenas or not theCatalogTextoCadenas:
            unCatalogoRaiz = self.getCatalogo()
            if not unCatalogoRaiz:
                return self
             
        unCatalogKey = self.fCatalogKey()
        
        unCatalogBusquedaCadenas = theCatalogBusquedaCadenas
        if ( unCatalogBusquedaCadenas == None): 
            unCatalogBusquedaCadenas = unCatalogoRaiz.fCatalogBusquedaCadenas()
        if not ( unCatalogBusquedaCadenas == None):
            unCatalogBusquedaCadenas.catalog_object( self, unCatalogKey)
            
        unCataloFiltroCadenas = theCatalogFiltroCadenas
        if ( unCataloFiltroCadenas == None): 
            unCataloFiltroCadenas = unCatalogoRaiz.fCatalogFiltroCadenas()
        if not( unCataloFiltroCadenas == None):
            unCataloFiltroCadenas.catalog_object( self, unCatalogKey)
        
        unCataloTextoCadenas = theCatalogTextoCadenas
        if ( unCataloTextoCadenas == None): 
            unCataloTextoCadenas = unCatalogoRaiz.fCatalogTextoCadenas()
        if not( unCataloTextoCadenas == None):
            unCataloTextoCadenas.catalog_object( self, unCatalogKey)
    
        return self
 
    
    

    


    security.declarePrivate( 'getTraduccionPorID')
    def getTraduccionPorID(self, theTraduccionID):
        if not theTraduccionID:
            return None
            
        try:
            return self[ theTraduccionID]
        except KeyError:
            None
             
        return None    
        
        
        
    
    
    security.declarePrivate( 'fIdTraduccionEnLenguage')
    def fIdTraduccionEnLenguage( self, theCodigoIdioma, thePloneUtilsTool=None):
        if not theCodigoIdioma:
            return ''
        
        return self.fIdTraduccionDesdeIdCadenaYLenguage( self.getId(), theCodigoIdioma, thePloneUtilsTool)
    
    


    
    

    
    
    
    
    
    # #########################################################################
    """Translation state change request methods.
    
    """
    

       

    

    security.declarePrivate( 'fIntentarTraducirTraduccion')
    def fIntentarTraducirTraduccion( self, 
        theIdioma, 
        theCadenaTraducida, 
        theComentario, 
        theRegistrarHistoria=True, 
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):
        """Set the string translation and change the state from pending to translated and comment to the supplied values. 

        Delegate in the TRATraduccion for the supplied language
        """
         
        unExecutionRecord = self.fStartExecution( 'method',  'fIntentarTraducirTraduccion', theParentExecutionRecord, False) 
    
        try:
            if not theIdioma:
                return self.fNewVoidChangeTranslationResult()
                
            if not theCadenaTraducida:
                return self.fNewVoidChangeTranslationResult()
    
            unaCadenaTraducida = theCadenaTraducida.strip()
            if not unaCadenaTraducida:
                return self.fNewVoidChangeTranslationResult()
            
            unComentario = theComentario.strip()
    
            unaTraduccion = self.fObtenerTraduccionEnIdioma( theIdioma)
            if not unaTraduccion:            
                return self.fNewVoidChangeTranslationResult()
            
            return unaTraduccion.fIntentarTraducir( 
                unaCadenaTraducida, 
                unComentario, 
                theUseCaseQueryResult       =None,
                theRegistrarHistoria        =theRegistrarHistoria, 
                thePermissionsCache         =thePermissionsCache, 
                theRolesCache               =theRolesCache, 
                theParentExecutionRecord    =unExecutionRecord
            )
       
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()





    security.declarePrivate( 'fComentarTraduccion')
    def fComentarTraduccion( self, 
        theIdioma, 
        theComentario, 
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fComentarTraduccion', theParentExecutionRecord, False) 
        
        try:
            if not theIdioma:
                return self.fNewVoidChangeTranslationResult()
    
            unComentario = theComentario.strip()
                        
            unaTraduccion = self.fObtenerTraduccionEnIdioma( theIdioma)
            if not unaTraduccion:
                return self.fNewVoidChangeTranslationResult()
    
            return unaTraduccion.fComentar( 
                unComentario, 
                theUseCaseQueryResult       =None,
                thePermissionsCache         =thePermissionsCache, 
                theRolesCache               =theRolesCache, 
                theParentExecutionRecord    =unExecutionRecord
            )    
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

    
    


    security.declarePrivate( 'fHacerPendienteTraduccion')    
    def fHacerPendienteTraduccion( self, 
        theIdioma, 
        theComentario, 
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fHacerPendienteTraduccion', theParentExecutionRecord, False) 
        
        try:
            if not theIdioma:
                return self.fNewVoidChangeTranslationResult()
    
            unaTraduccion = self.fObtenerTraduccionEnIdioma( theIdioma)
            if not unaTraduccion:
                return self.fNewVoidChangeTranslationResult()
            
            return unaTraduccion.fHacerPendiente( 
                theComentario, 
                theUseCaseQueryResult       =None,
                thePermissionsCache         =thePermissionsCache, 
                theRolesCache               =theRolesCache, 
                theParentExecutionRecord    =unExecutionRecord
            )
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
         
         
         
         
         

    security.declarePrivate( 'fHacerTraducidaTraduccion')    
    def fHacerTraducidaTraduccion( self, 
        theIdioma, 
        theComentario, 
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fHacerTraducidaTraduccion', theParentExecutionRecord, False) 
        
        try:
            if not theIdioma:
                return self.fNewVoidChangeTranslationResult()
        
            unaTraduccion = self.fObtenerTraduccionEnIdioma( theIdioma)
            if not unaTraduccion:
                return self.fNewVoidChangeTranslationResult()
 
            return unaTraduccion.fHacerTraducida( 
                theComentario, 
                theUseCaseQueryResult       =None,
                thePermissionsCache     =thePermissionsCache, 
                theRolesCache           =theRolesCache, 
                theParentExecutionRecord=unExecutionRecord
            )
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
       
       
       
    
       

    security.declarePrivate( 'fHacerRevisadaTraduccion')    
    def fHacerRevisadaTraduccion( self, 
        theIdioma, 
        theComentario, 
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fHacerRevisadaTraduccion', theParentExecutionRecord, False) 
        
        try:
            if not theIdioma:
                return self.fNewVoidChangeTranslationResult()
     
            unaTraduccion = self.fObtenerTraduccionEnIdioma( theIdioma)
            if not unaTraduccion:
                return self.fNewVoidChangeTranslationResult()
    
            return unaTraduccion.fHacerRevisada( 
                theComentario, 
                theUseCaseQueryResult       =None,
                thePermissionsCache     =thePermissionsCache, 
                theRolesCache           =theRolesCache, 
                theParentExecutionRecord=unExecutionRecord
            )
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
         






    security.declarePrivate( 'fHacerDefinitivaTraduccion')    
    def fHacerDefinitivaTraduccion( self, 
        theIdioma, 
        theComentario, 
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fHacerDefinitivaTraduccion', theParentExecutionRecord, False) 
        
        try:
            if not theIdioma:
                return self.fNewVoidChangeTranslationResult()
     
            unaTraduccion = self.fObtenerTraduccionEnIdioma( theIdioma)
            if not unaTraduccion:
                return self.fNewVoidChangeTranslationResult()
    
            return unaTraduccion.fHacerDefinitiva(  
                theComentario, 
                theUseCaseQueryResult       =None,
                thePermissionsCache     =thePermissionsCache, 
                theRolesCache           =theRolesCache, 
                theParentExecutionRecord=unExecutionRecord
            )
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
         
        





    
# #########################################################################
#   Reseteo  de Historia de cambios de TRATraduccion
# ##################    
            
        
    # ACV 20090323 Unused. Removed.
    #security.declareProtected( permissions.ModifyPortalContent, 'pResetHistoriaYComentario(')
    #def pResetHistoriaYComentario( self, theUsuario, theDateTime):
 
        #if not self.fCanChangeCadena():
            #return self

        #if False:
            #return self          
            
        #self.setFechaCreacion(  theDateTime - ( 3600 * 24 * 30))
        #self.setUsuarioCreador( theUsuario)
        #return self
    
    


