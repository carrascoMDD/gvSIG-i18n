# -*- coding: utf-8 -*-
#
# File: TRATraduccion_Operationes.py
#
# Copyright (c) 2008, 2009 by Conselleria de Infraestructuras y Transporte de la
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



import logging

import transaction


from AccessControl      import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName
from Products.CMFCore       import permissions

from Products.Archetypes.BaseObject     import BaseObject

from Products.Archetypes.utils          import getRelURL




from TRAElemento_Constants         import *
from TRAImportarExportar_Constants import *

from TRAElemento import TRAElemento

from TRAElemento_Permission_Definitions import cUseCase_TRATraduccionStateChange, cStateChangeActionRoles, cBoundObject





cMarcaDeFinDeRegistroDeHistoria   = "_*F*I*N*"
cMarcaDeComentarioSinCambios      = "=="



class TRATraduccion_Operaciones:
    """
    """
    security = ClassSecurityInfo()

        
    

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

        
    security.declarePrivate('getFechaTraduccion')
    def getFechaTraduccion( self,): 
        return self.fFechaTraduccionDesdeTextual()
     
    
    security.declarePrivate('getFechaRevision')
    def getFechaRevision( self,): 
        return self.fFechaRevisionDesdeTextual()
     
  
    security.declarePrivate('getFechaDefinitivo')
    def getFechaDefinitivo( self,): 
        return self.fFechaDefinitivoDesdeTextual()
     
  
       
   
    
    

    
     
    security.declarePrivate('fFechaTraduccionDesdeTextual')
    def fFechaTraduccionDesdeTextual( self, ): 
        """Derived accessor for translation date stored as text.
        
        """
        unaString = self.getFechaTraduccionTextual()
        unaDate = self.fStoreStringToDate( unaString)
        return unaDate
    
    
    security.declarePrivate('fFechaRevisionDesdeTextual')
    def fFechaRevisionDesdeTextual( self, ): 
        """Derived accessor for review date stored as text.
        
        """
        unaString = self.getFechaRevisionTextual()
        unaDate = self.fStoreStringToDate( unaString)
        return unaDate
    
    
  
    security.declarePrivate('fFechaDefinitivoDesdeTextual')
    def fFechaDefinitivoDesdeTextual( self, ): 
        """Derived accessor for lock date stored as text.
        
        """
        unaString = self.getFechaDefinitivoTextual()
        unaDate = self.fStoreStringToDate( unaString)
        return unaDate
    
    
  
        
    security.declarePrivate('pSetFechaTraduccion')
    def pSetFechaTraduccion( self, theDate): 
        
        unaString = self.fDateToStoreString( theDate)
        if unaString:
            self.setFechaTraduccionTextual( unaString)
        return self
    
    
    
    security.declarePrivate('setFechaTraduccion')
    def setFechaTraduccion( self, theDate): 
        return self.pSetFechaTraduccion( theDate)
     
    
    
    security.declarePrivate('pSetFechaRevision')
    def pSetFechaRevision( self, theDate): 
        
        unaString = self.fDateToStoreString( theDate)
        if unaString:
            self.setFechaRevisionTextual( unaString)
        return self
    
    security.declarePrivate('setFechaRevision')
    def setFechaRevision( self, theDate): 
        return self.pSetFechaRevision( theDate)
     
    
    
    security.declarePrivate('pSetFechaDefinitivo')
    def pSetFechaDefinitivo( self, theDate): 
        
        unaString = self.fDateToStoreString( theDate)
        if unaString:
            self.setFechaDefinitivoTextual( unaString)
        return self
    
    
    security.declarePrivate('setFechaDefinitivo')
    def setFechaDefinitivo( self, theDate): 
        return self.pSetFechaDefinitivo( theDate)
     
       
       

    
    
    
    
    
# ####################################
#  Derived accessors for related TRAIdioma and TRAModulo
# ####################################
    

    security.declarePrivate('fObtenerIdioma')
    def fObtenerIdioma( self, ):   
        unCatalogo = self.getCatalogo()
        if not unCatalogo:
            return None
        return unCatalogo.fGetIdiomaPorCodigo( self.getCodigoIdiomaEnGvSIG())
    
    security.declarePrivate('fObtenerModulo')
    def fObtenerModulo( self, ):   
        unaCadena = self.getCadena()
        if not unaCadena:
            return None
        return unaCadena.fObtenerModulo()
    
    
    security.declarePrivate('fObtenerModulos')
    def fObtenerModulos( self, ):   
        unaCadena = self.getCadena()
        if not unaCadena:
            return None
        return unaCadena.fObtenerModulos()
    
    
      
    

    
    
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
        self.pAddToCatalogs( )
        return self
    
   
 
    security.declarePrivate('pHandle_manage_afterAdd')
    def pHandle_manage_afterAdd(self, theItem, theContainer):   
       
        # vaya_que_no_debe_pHandle_manage_afterAdd_TRATraduccion()
        # y debe impedir que se cataloge en el catalog del portal
        # TRAElemento.manage_afterAdd( self, theItem, theContainer)

        # self.pAddToCatalogs()
        
        # ACV 20090504 Avoid catalogging the TRATraduccion into the UID catalog,
        # by not delegating into Referenceable superclass,
        # BaseObject.manage_afterAdd( self, theItem, theContainer)
        
        BaseObject.initializeLayers( self, theItem, theContainer)

        return self
    
    
# #########################################################################
#   Manage delete
# ##################    

     
        
    security.declarePrivate('pHandle_manage_beforeDelete')
    def pHandle_manage_beforeDelete(self, theItem, theContainer):   
       
        try:
            unIdioma = self.getIdioma()
            if unIdioma:
                unCatalogoRaiz = self.getCatalogo()
                if unCatalogoRaiz:
                    
                    unCatalogKey = theElement.fCatalogKey()
                    
                    unCatalogBusquedaTraducciones = unCatalogoRaiz.fCatalogBusquedaTraduccionesParaIdioma( unIdioma)
                    if not( unCatalogBusquedaTraducciones == None):
                        unCatalogBusquedaTraducciones.uncatalog_object( unCatalogKey)
                     
                    unCatalogFiltroTraducciones   = unCatalogoRaiz.fCatalogFiltroTraduccionesParaIdioma( unIdioma)
                    if not( unCatalogFiltroTraducciones == None):
                        unCatalogFiltroTraducciones.uncatalog_object(   unCatalogKey)
            
                    unCatalogTextoTraducciones   = unCatalogoRaiz.fCatalogTextoTraduccionesParaIdioma( unIdioma)
                    if not( unCatalogTextoTraducciones == None):
                        unCatalogTextoTraducciones.uncatalog_object(   unCatalogKey)
        except:
            None
        
        TRAElemento.manage_beforeDelete( self, theElement, theContainer)
         
        return self
    

    
    
    
    def fCatalogKey( self):
        return '/'.join( self.getPhysicalPath())
    
                         
                         
    security.declarePrivate('pRecatalogTraduccion')
    def pRecatalogTraduccion(self, theParentExecutionRecord=None):
        self.pAddToCatalogs( 
            theCatalogBusquedaTraducciones  =None, 
            theCatalogFiltroTraducciones    =None, 
            theCatalogTextoTraducciones     =None, 
            theParentExecutionRecord        =theParentExecutionRecord)
        return  self
                         
    
    
                         
                         
    security.declarePrivate('pAddToCatalogs')
    def pAddToCatalogs(self, 
        theCatalogBusquedaTraducciones=None, 
        theCatalogFiltroTraducciones=None, 
        theCatalogTextoTraducciones=None, 
        theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'pAddToCatalogs', theParentExecutionRecord, False) 
        
        try:
            
            unIdioma = self.getIdioma()
            if not unIdioma:
                return self
            
            unCatalogoRaiz = None
            if not theCatalogBusquedaTraducciones or not theCatalogFiltroTraducciones or not theCatalogTextoTraducciones:
                unCatalogoRaiz = self.getCatalogo()
                if not unCatalogoRaiz:
                    return self
                    
            unCatalogKey = self.fCatalogKey()
            
            unCatalogBusquedaTraducciones = theCatalogBusquedaTraducciones
            if unCatalogBusquedaTraducciones == None:
                unCatalogBusquedaTraducciones = unCatalogoRaiz.fCatalogBusquedaTraduccionesParaIdioma( unIdioma)
            if not (unCatalogBusquedaTraducciones == None):
                unCatalogBusquedaTraducciones.catalog_object( self,  unCatalogKey )
             
            unCatalogFiltroTraducciones = theCatalogFiltroTraducciones
            if unCatalogFiltroTraducciones == None:
                unCatalogFiltroTraducciones   = unCatalogoRaiz.fCatalogFiltroTraduccionesParaIdioma( unIdioma)
            if not (unCatalogFiltroTraducciones == None):
                unCatalogFiltroTraducciones.catalog_object(   self,  unCatalogKey )
            
            unCatalogTextoTraducciones = theCatalogTextoTraducciones
            if unCatalogTextoTraducciones == None:
                unCatalogTextoTraducciones   = unCatalogoRaiz.fCatalogTextoTraduccionesParaIdioma( unIdioma)
            if not (unCatalogTextoTraducciones == None):
                unCatalogTextoTraducciones.catalog_object(   self,  unCatalogKey )
            
            return self
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
                      
                
                
                 
    
            
            
            
            
    
  

    security.declareProtected( permissions.View, 'getCadena')
    def getCadena( self):
        """Retrieve owner TRACadena.
        
        """
        unContenedor = self.getContenedor()
        return unContenedor
           
    
    
  

    
    
    security.declareProtected( permissions.View, 'getIdioma')
    def getIdioma( self):
        """Retrieve owner TRAIdioma.
        
        """
        unCatalogo = self.getCatalogo()
        if not unCatalogo:
            return None
            
        unCodigoIdiomaEnGvSIG = self.getCodigoIdiomaEnGvSIG()
        unIdioma = unCatalogo.fGetIdiomaPorCodigo( unCodigoIdiomaEnGvSIG)
        return unIdioma         


    
    
   
   
    security.declarePrivate('fDeriveEstadoCadena')
    def fDeriveEstadoCadena( self):
        """"Derive TRACadena state.
        
        """
        unaCadena = self.getCadena()
        if not unaCadena:
            return ""
       
        return unaCadena.getEstadoCadena()        
   
         
         
         
   
    security.declarePrivate('fDeriveNombresModulos')
    def fDeriveNombresModulos( self):
        """"Derive the names of the owner TRAModulo.
        
        """
        unaCadena = self.getCadena()
        if not unaCadena:
            return ""
       
        return unaCadena.getNombresModulos()        
   
          
          
          
          
          
    security.declarePrivate('fDeriveNombresModulosLegibles')
    def fDeriveNombresModulosLegibles( self):
        """"Derive the readable names of the owner TRAModulo.
        
        """
        unaCadena = self.getCadena()
        if not unaCadena:
            return ""
       
        return unaCadena.getNombresModulosLegibles()        
                     
                     
                     
                     
   
    security.declarePrivate('fDeriveSimboloCadena')
    def fDeriveSimboloCadena( self):
        unaCadena = self.getCadena()
        if not unaCadena:
            return ""
       
        return unaCadena.getSimbolo()        
   
         
         
   
    security.declarePrivate('fDeriveIdCadena')
    def fDeriveIdCadena( self):
        unaCadena = self.getCadena()
        if not unaCadena:
            return ""
       
        return unaCadena.getId()        
   
         
         
  
         
    
           
     
        
    
  
    
           
    # ##########################################
    """State change action request handlers
   
    """
    # method located in TRAElemento_Operationes
    #
    #security.declarePrivate( 'fNewVoidChangeTranslationResult')
    #def fNewVoidChangeTranslationResult( self,):
        #aResult = {
            #'success':                          False,
            #'exception':                        '',
            #'status':                           '',
            #'condition':                         '',
            #'found':                            False,
            #'changed':                          False,
            #'changed_comment':                  False,
            #'simboloCadena':                    '',
            #'idCadena':                         '',
            #'memberid':                         '',
            #'cadenaTraducida_previousValue':    '',
            #'cadenaTraducida_newValue':         '',
            #'estadoTraduccion_previousValue':   '',
            #'estadoTraduccion_newValue':        '',
            #'comentario_previousValue':         '',
            #'comentario_newValue':              '',
        #}
        #return aResult
        
    
 
    security.declarePrivate( 'fStripInnerBlanks')
    def fStripInnerBlanks( self, theString):
        
        if not theString:
            return ''
        
        unString = unString.strip()
        if not unString:
            return unString
        unString = ' '.join( [ unaLine.strip() for unaLine in unString.split( '\n')])
        if not unaNuevaCadenaTraducida:
            return unString
        unString = ' '.join( [ unaLine.strip() for unaLine in unString.split( '\r')])
        if not unString:
            return unString
        unString = ' '.join( [ unaLine.strip() for unaLine in unString.split( '\t')])

        return unString
        
    
    
    

    
    
    
    security.declarePrivate( 'fIntentarTraducir')
    def fIntentarTraducir( self, 
        theCadenaTraducida, 
        theComentario, 
        theAdditionalParams      =None,
        theUseCaseQueryResult    =None, 
        theRegistrarHistoria     =True, 
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):
        """Set the string translation and change the state from pending to translated and comment to the supplied values. 

        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fIntentarTraducir', theParentExecutionRecord,  False) 
        
        try:
            aResult = self.fNewVoidChangeTranslationResult()
            
            
            unContadorCambiosString = theAdditionalParams.get( 'theContadorCambios', None)
            if unContadorCambiosString:
                unContadorCambios = -1
                try:
                    unContadorCambios = int( unContadorCambiosString)
                except:
                    None
                if unContadorCambios >= 0:
                    unContadorCambiosActual = self.getContadorCambios()
                    if not( unContadorCambios == None):
                        if not ( unContadorCambios == unContadorCambiosActual):
                            return self.fResultForChangeCounterDetectedOverwrite(
                                theCadenaTraducida       =theCadenaTraducida, 
                                theComentario            =theComentario, 
                                theAdditionalParams      =theAdditionalParams,
                                theUseCaseQueryResult    =theUseCaseQueryResult, 
                                theRegistrarHistoria     =theRegistrarHistoria, 
                                thePermissionsCache      =thePermissionsCache, 
                                theRolesCache            =theRolesCache, 
                                theParentExecutionRecord =theParentExecutionRecord,
                            )
                
                
            
            unaCadena = self.getCadena()
            if not unaCadena:
                return aResult
            
            aResult.update({
                'simboloCadena': unaCadena.getSimbolo(),
                'idCadena':      unaCadena.getId(),
                   
            })
            aResult[ 'found'] = True
            
            if not theCadenaTraducida:
                return aResult      
            
            unaNuevaCadenaTraducida = theCadenaTraducida.strip().replace( '\n', ' ').replace( '\t', '').replace( '\r', ' ')
            if not unaNuevaCadenaTraducida:
                return aResult
                 
            unaCadenaTraducida          = self.getCadenaTraducida()            
            unComentarioTraduccion      = self.getComentario() 
            unaHistoriaTraduccion       = self.getHistoria()
            unEstadoTraduccion          = self.getEstadoTraduccion()  
            unaFechaTraduccionTextual   = self.getFechaTraduccionTextual()  
            unUsuarioTraductor          = self.getUsuarioTraductor()  
            unaFechaRevisionTextual     = self.getFechaRevisionTextual()  
            unUsuarioRevisor            = self.getUsuarioRevisor()  
            unaFechaDefinitivoTextual   = self.getFechaDefinitivoTextual()  
            unUsuarioCoordinador        = self.getUsuarioCoordinador()  
            
            aResult[ 'estadoTraduccion_previousValue'] = unEstadoTraduccion
            aResult[ 'cadenaTraducida_previousValue']  = unaCadenaTraducida
            
            aResult[ 'estadoTraduccion_newValue']      = unEstadoTraduccion
            aResult[ 'cadenaTraducida_newValue']       = unaCadenaTraducida


            
             
            aTranslationService = getToolByName( self, 'translation_service', None)            
            if not aTranslationService:
                aResult.update({
                    'status': 'No_TranslationService',
                })
                return aResult
                
            
            unaEncodedNuevaCadenaTraducida = aTranslationService.encode( unaNuevaCadenaTraducida)            
            
            
            
            
            
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                            
            unUseCaseQueryResult = theUseCaseQueryResult
            if not unUseCaseQueryResult or not ( unUseCaseQueryResult.get( 'use_case_name', '') == cUseCase_TRATraduccionStateChange):
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_TRATraduccionStateChange,        
                    theElementsBindings     = { cBoundObject: self,},                                    
                    theRulesToCollect       = None,                                                      
                    thePermissionsCache     = unPermissionsCache,                                        
                    theRolesCache           = unRolesCache,                                              
                    theParentExecutionRecord= unExecutionRecord,                                          
                )
            if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                aResult.update({
                    'status': 'UseCase_assessment_failed: %s' % cUseCase_TRATraduccionStateChange,
                })
                return aResult
                
            if not self.fCanChangeToNuevoEstadoTraduccion( 
                cEstadoTraduccionTraducida, 
                unUseCaseQueryResult, 
                thePermissionsCache=unPermissionsCache, 
                theRolesCache=unRolesCache, 
                theParentExecutionRecord=unExecutionRecord):
                aResult.update({
                    'status': 'fCanChangeToNuevoEstadoTraduccion_failed',
                })
                return aResult
            
    
            if not ( unEstadoTraduccion in [ cEstadoTraduccionPendiente, cEstadoTraduccionTraducida, ]):
                aResult.update({
                    'status': 'CurrentStateNot_Pendiente_or_Traducida',
                })
                return aResult            
    
            unNuevoComentario = theComentario
            if not unNuevoComentario:
                unNuevoComentario = ""            
            unNuevoComentario = unNuevoComentario.strip()            
            unComentarioParaHistoria = cMarcaDeComentarioSinCambios
    
            
                 
            aMembershipTool = getToolByName( self, 'portal_membership', None)
            unMember = aMembershipTool.getAuthenticatedMember()   
            if not unMember:
                aResult.update({
                    'status': 'authenticated_member_not_found',
                })
                return aResult                
            if unMember.getUserName() == 'Anonymous User':
                unMemberId = unMember.getUserName()
            else:
                unMemberId = unMember.getMemberId()   
            if not unMemberId:
                aResult.update({
                    'status': 'authenticated_member_id_missing',
                })
                return aResult
    
            aResult[ 'memberid'] = unMemberId
            
            
            
            unAhoraStoreString = self.fDateTimeNowTextual()
            
            unTranslationActivity = self.fNewVoidTranslationActivity()
            unTranslationActivity.update( { 
                cRecentActivity_Date:        unAhoraStoreString,
                cRecentActivity_User:        unMemberId,
                cRecentActivity_Language:    self.getCodigoIdiomaEnGvSIG(),
                cRecentActivity_Symbol:      self.getSimbolo(),
            })


            unHayCambio = False
            try:
                if not ( unNuevoComentario == unComentarioTraduccion):
                    unComentarioParaHistoria = unNuevoComentario
                    self.setComentario(  unNuevoComentario)       
                    unHayCambio = True
                    aResult.update({
                        'changed_comment':          True,
                        'comentario_previousValue': unComentarioTraduccion,
                        'comentario_newValue':      unNuevoComentario,
                    })
                    
                    unTranslationActivity[ cRecentActivity_Action]    = cTranslationHistoryAction_Comentar
                    unTranslationActivity[ cRecentActivity_Commented] = True
         

                if  ( unEstadoTraduccion and not  ( unEstadoTraduccion in [ cEstadoTraduccionPendiente, cEstadoTraduccionTraducida])):
                    aResult.update({
                        'status': 'CurrentStatePreventsChange',
                    })
                elif ( unaEncodedNuevaCadenaTraducida == unaCadenaTraducida):    
                    aResult.update({
                        'status': 'same_translation',
                    })
                else:     
                                          
                    if ( not unEstadoTraduccion) or ( unEstadoTraduccion == cEstadoTraduccionPendiente):
                        self.setEstadoTraduccion(  cEstadoTraduccionTraducida)    
                        aResult.update({
                            'estadoTraduccion_newValue':      cEstadoTraduccionTraducida,
                        })
                                 
                        unTranslationActivity[ cRecentActivity_Action]    = cTranslationHistoryAction_Traducir
                        
                    self.setCadenaTraducida(   unaEncodedNuevaCadenaTraducida) 
                    aResult.update({
                        'cadenaTraducida_newValue':      unaEncodedNuevaCadenaTraducida,
                    })
                    
                    unTranslationActivity[ cRecentActivity_Action]    = cTranslationHistoryAction_Traducir
                    
                    
                    
                    if  not ( unUsuarioTraductor == unMemberId):
                        self.setUsuarioTraductor(  unMemberId)   
                        
                    if  not ( unaFechaTraduccionTextual == unAhoraStoreString):
                        self.setFechaTraduccionTextual(   unAhoraStoreString)
                       
                    if  unUsuarioRevisor:
                        self.setUsuarioRevisor(  None)   
                        
                    if  unaFechaRevisionTextual:
                        self.setFechaRevisionTextual(   None)    
                        
                    if  unaFechaDefinitivoTextual:
                        self.setFechaDefinitivoTextual(   None)    
                                                            
                    if  unUsuarioCoordinador:
                        self.setUsuarioCoordinador(  None)  
                        
                    unContadorCambiosActual = self.getContadorCambios()
                    if not unContadorCambiosActual:
                        unContadorCambiosActual = 0

                    unNuevoContadorCambios = unContadorCambiosActual + 1
                    self.setContadorCambios( unNuevoContadorCambios)
                        
                    unTranslationActivity[ cRecentActivity_Counter] = unNuevoContadorCambios
                    
                    
                    
                    if theRegistrarHistoria:
                        self.pRegistrarHistoria( 
                            theAccion                   = cTranslationHistoryAction_Traducir, 
                            theFechaAccionTextual       = unAhoraStoreString, 
                            theUsuarioActor             = unMemberId, 
                            theEstadoTraduccion         = cEstadoTraduccionTraducida, 
                            theFechaTraduccionTextual   = unAhoraStoreString, 
                            theUsuarioTraductor         = unMemberId, 
                            theCadenaTraducida          = unaEncodedNuevaCadenaTraducida, 
                            theFechaRevisionTextual     = None, 
                            theUsuarioRevisor           = None, 
                            theFechaDefinitivoTextual   = None, 
                            theUsuarioCoordinador       = None, 
                            theComentario               = unComentarioParaHistoria,                            
                        )
                    
                    unHayCambio = True
                    aResult.update({
                        'success': True,
                        'changed': True,
                    })
                    return aResult
                   
                if not( unNuevoComentario == unComentarioTraduccion):
                    if theRegistrarHistoria:
                        self.pRegistrarHistoria( 
                            theAccion                   = cTranslationHistoryAction_Comentar, 
                            theFechaAccionTextual       = unAhoraStoreString, 
                            theUsuarioActor             = unMemberId, 
                            theEstadoTraduccion         = None, 
                            theFechaTraduccionTextual   = None, 
                            theUsuarioTraductor         = None, 
                            theCadenaTraducida          = None, 
                            theFechaRevisionTextual     = None, 
                            theUsuarioRevisor           = None, 
                            theFechaDefinitivoTextual   = None, 
                            theUsuarioCoordinador       = None, 
                            theComentario               = unComentarioParaHistoria,                            
                        )
                    aResult.update({
                        'comentario_previousValue': unComentarioTraduccion,
                        'comentario_newValue':      unNuevoComentario,
                        'changed_comment':          True,
                    })
       
                    return aResult # Do not set unHayCambio to True, to avoid re-cataloging the TRATraduccion
            
                return aResult
                
            finally:
                if unHayCambio:
                    self.pRecatalogTraduccion( unExecutionRecord)
                    
                    unCatalogo = self.getCatalogo()
                    if not ( unCatalogo == None):
                        unCatalogo.pTranslationActivityOccurred( unTranslationActivity)
                    
                    if cLogTranslationChanges:
                        logging.getLogger( 'gvSIGi18n::fIntentarTraducir').info( "CHANGED")               
            
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            
  
            
            
            
    
        
 
    security.declarePrivate( 'fResultForChangeCounterDetectedOverwrite')
    def fResultForChangeCounterDetectedOverwrite( self, 
        theAdditionalParams      =None,
        theUseCaseQueryResult    =None, 
        theRegistrarHistoria     =True, 
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):
        """The ChangeCounter received in the user requests, reflecting the moment in the history of changes to the translation, when the user received the string to translate.
        Can not Set the string translation and overwrite newer translation.
        Can not change the state-
        If the intended change is the same as the current translation (i.e., two users submitted the exactly same translation) we'll report the operation as sucessful, for the benefit of users interacting Asynchronously. 
        Translator user and translation date remains reflecting the user who trasnslated first.

        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fResultForChangeCounterDetectedOverwrite', theParentExecutionRecord,  False) 
        
        try:
            aResult = self.fNewVoidChangeTranslationResult()
            
            aResult.update( {
                'success': False,
                'status':  cTranslationStatus_DifferentChangeCounter,
            }) 
           
            unaCadena = self.getCadena()
            if not unaCadena:
                return aResult
            
            aResult.update({
                'simboloCadena': unaCadena.getSimbolo(),
                'idCadena':      unaCadena.getId(),
                   
            })
            aResult[ 'found'] = True
            

            unaCadenaTraducida          = self.getCadenaTraducida()            
            unComentarioTraduccion      = self.getComentario() 
            unaHistoriaTraduccion       = self.getHistoria()
            unEstadoTraduccion          = self.getEstadoTraduccion()  
            unaFechaTraduccionTextual   = self.getFechaTraduccionTextual()  
            unUsuarioTraductor          = self.getUsuarioTraductor()  
            unaFechaRevisionTextual     = self.getFechaRevisionTextual()  
            unUsuarioRevisor            = self.getUsuarioRevisor()  
            unaFechaDefinitivoTextual   = self.getFechaDefinitivoTextual()  
            unUsuarioCoordinador        = self.getUsuarioCoordinador()  
            
            aResult[ 'estadoTraduccion_previousValue'] = unEstadoTraduccion
            aResult[ 'cadenaTraducida_previousValue']  = unaCadenaTraducida
            
            aResult[ 'estadoTraduccion_newValue']      = unEstadoTraduccion
            aResult[ 'cadenaTraducida_newValue']       = unaCadenaTraducida

            aMembershipTool = getToolByName( self, 'portal_membership', None)
            unMember = aMembershipTool.getAuthenticatedMember()   
            if not unMember:
                return aResult                
            if unMember.getUserName() == 'Anonymous User':
                unMemberId = unMember.getUserName()
            else:
                unMemberId = unMember.getMemberId()   
            if not unMemberId:
                return aResult
    
            aResult[ 'memberid'] = unMemberId
            
            return aResult
            
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            
  
            
                
    
             

    security.declarePrivate( 'fComentar')
    def fComentar( self, 
        theComentario, 
        theAdditionalParams      =None,
        theUseCaseQueryResult    =None,         
        theRegistrarHistoria     =True, 
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):

        unExecutionRecord = self.fStartExecution( 'method',  'fComentar', theParentExecutionRecord, False) 
        
        try:
            aResult = self.fNewVoidChangeTranslationResult()
            
            # Allow to append to comments
            #
            #unContadorCambiosString = theAdditionalParams.get( 'theContadorCambios', None)
            #if unContadorCambiosString:
                #unContadorCambios = -1
                #try:
                    #unContadorCambios = int( unContadorCambiosString)
                #except:
                    #None
                #if unContadorCambios >= 0:
                    #unContadorCambiosActual = self.getContadorCambios()
                    #if not( unContadorCambios == None):
                        #if not ( unContadorCambios == unContadorCambiosActual):
                            #return self.fResultForChangeCounterDetectedOverwrite(
                                #theAdditionalParams      =theAdditionalParams,
                                #theUseCaseQueryResult    =theUseCaseQueryResult, 
                                #theRegistrarHistoria     =theRegistrarHistoria, 
                                #thePermissionsCache      =thePermissionsCache, 
                                #theRolesCache            =theRolesCache, 
                                #theParentExecutionRecord =theParentExecutionRecord,
                            #)

                        
            unaCadena = self.getCadena()
            if not unaCadena:
                return aResult
            
            aResult.update({
                'simboloCadena': unaCadena.getSimbolo(),
                'idCadena':      unaCadena.getId(),
                   
            })
            aResult[ 'found'] = True

            unHayCambio = False
            
            
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
                 
            unaCadenaTraducida          = self.getCadenaTraducida()            
            unComentarioTraduccion      = self.getComentario() 
            unEstadoTraduccion          = self.getEstadoTraduccion()  

            aResult[ 'estadoTraduccion_previousValue'] = unEstadoTraduccion
            aResult[ 'estadoTraduccion_newValue']      = unEstadoTraduccion

            unUseCaseQueryResult = theUseCaseQueryResult
            if not unUseCaseQueryResult or not ( unUseCaseQueryResult.get( 'use_case_name', '') == cUseCase_TRATraduccionStateChange):
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_TRATraduccionStateChange,        
                    theElementsBindings     = { cBoundObject: self,},                                    
                    theRulesToCollect       = None,                                                      
                    thePermissionsCache     = unPermissionsCache,                                        
                    theRolesCache           = unRolesCache,                                              
                    theParentExecutionRecord= unExecutionRecord,                                          
                )
            if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                aResult.update({
                    'status': 'UseCase_assessment_failed: %s' % cUseCase_TRATraduccionStateChange,
                })
                return aResult
                
    
            if not self.fCanChangeComment( 
                self, 
                unUseCaseQueryResult, 
                thePermissionsCache     =unPermissionsCache, 
                theRolesCache           =unRolesCache, 
                theParentExecutionRecord=unExecutionRecord ):
                
                aResult.update({
                    'status': 'fCanChangeComment_failed',
                })
                return aResult
    
    
            unNuevoComentario = theComentario
            if not unNuevoComentario:
                unNuevoComentario = ""            
            unNuevoComentario = unNuevoComentario.strip()            
    
            if unNuevoComentario == unComentarioTraduccion:                 
                aResult.update({
                    'status': 'same_comment_value',
                })
                return aResult
    
             
                 
            aMembershipTool = getToolByName( self, 'portal_membership', None)
            unMember = aMembershipTool.getAuthenticatedMember()   
            if not unMember:
                aResult.update({
                    'status': 'authenticated_member_not_found',
                })
                return aResult                
            if unMember.getUserName() == 'Anonymous User':
                unMemberId = unMember.getUserName()
            else:
                unMemberId = unMember.getMemberId()   
            if not unMemberId:
                aResult.update({
                    'status': 'authenticated_member_id_missing',
                })
                return aResult
    
            aResult[ 'memberid'] = unMemberId
         
     
            unAhoraStoreString = self.fDateTimeNowTextual()
        
           
            unTranslationActivity = self.fNewVoidTranslationActivity()
            unTranslationActivity.update( { 
                cRecentActivity_Date:        unAhoraStoreString,
                cRecentActivity_User:        unMemberId,
                cRecentActivity_Language:    self.getCodigoIdiomaEnGvSIG(),
                cRecentActivity_Symbol:      self.getSimbolo(),
            })
            
            unHayCambio = False
            try:
                self.setComentario(  unNuevoComentario)  
                    
                if theRegistrarHistoria:
                    self.pRegistrarHistoria( 
                        theAccion                   = cTranslationHistoryAction_Comentar, 
                        theFechaAccionTextual       = unAhoraStoreString, 
                        theUsuarioActor             = unMemberId, 
                        theEstadoTraduccion         = None, 
                        theFechaTraduccionTextual   = None, 
                        theUsuarioTraductor         = None, 
                        theCadenaTraducida          = None, 
                        theFechaRevisionTextual     = None, 
                        theUsuarioRevisor           = None, 
                        theFechaDefinitivoTextual   = None, 
                        theUsuarioCoordinador       = None, 
                        theComentario               = unNuevoComentario, 
                    )
                
                unHayCambio = True
                aResult.update({
                    'success':                  True,
                    'comentario_previousValue': unComentarioTraduccion,
                    'comentario_newValue':      unNuevoComentario,
                    'changed_comment':          True,
                })
                
                unTranslationActivity[ cRecentActivity_Action]    = cTranslationHistoryAction_Comentar
                unTranslationActivity[ cRecentActivity_Commented] = True
                
                
                return aResult
    
            finally:
                if unHayCambio:
                    # ACV 20090406 no recatalog for comment, as comment is not indexed 
                    # will enable if we ever index the comment
                    # self.pRecatalogTraduccion( unExecutionRecord)
                    unCatalogo = self.getCatalogo()
                    if not ( unCatalogo == None):
                        unCatalogo.pTranslationActivityOccurred( unTranslationActivity)
                        
                    if cLogTranslationChanges:
                        logging.getLogger( 'gvSIGi18n::fComentar').info( "CHANGED")               
                
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            
  

         
    


     
    security.declarePrivate( 'fInvalidar')
    def fInvalidar( self, 
        theComentario, 
        theAdditionalParams      =None,
        theRegistrarHistoria     =True, 
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):
    
        unExecutionRecord = self.fStartExecution( 'method',  'fHacerPendiente', theParentExecutionRecord,  False)  
        
        try:
            aResult = self.fNewVoidChangeTranslationResult()
            
            
            unContadorCambiosString = theAdditionalParams.get( 'theContadorCambios', None)
            if unContadorCambiosString:
                unContadorCambios = -1
                try:
                    unContadorCambios = int( unContadorCambiosString)
                except:
                    None
                if unContadorCambios >= 0:
                    unContadorCambiosActual = self.getContadorCambios()
                    if not( unContadorCambios == None):
                        if not ( unContadorCambios == unContadorCambiosActual):
                            return self.fResultForChangeCounterDetectedOverwrite(
                                theAdditionalParams      =theAdditionalParams,
                                theUseCaseQueryResult    =theUseCaseQueryResult, 
                                theRegistrarHistoria     =theRegistrarHistoria, 
                                thePermissionsCache      =thePermissionsCache, 
                                theRolesCache            =theRolesCache, 
                                theParentExecutionRecord =theParentExecutionRecord,
                            )

            unaCadena = self.getCadena()
            if not unaCadena:
                return aResult
            
            aResult.update({
                'simboloCadena': unaCadena.getSimbolo(),
                'idCadena':      unaCadena.getId(),
                   
            })
            aResult[ 'found'] = True
            
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
                
            unaCadenaTraducida          = self.getCadenaTraducida()            
            unComentarioTraduccion      = self.getComentario() 
            unaHistoriaTraduccion       = self.getHistoria()
            unEstadoTraduccion          = self.getEstadoTraduccion()  
            unaFechaTraduccionTextual   = self.getFechaTraduccionTextual()  
            unUsuarioTraductor          = self.getUsuarioTraductor()  
            unaFechaRevisionTextual     = self.getFechaRevisionTextual()  
            unUsuarioRevisor            = self.getUsuarioRevisor()  
            unaFechaDefinitivoTextual   = self.getFechaDefinitivoTextual()  
            unUsuarioCoordinador        = self.getUsuarioCoordinador()  
            
            aResult[ 'estadoTraduccion_previousValue'] = unEstadoTraduccion

            if self.getEstadoTraduccion() == cEstadoTraduccionPendiente:
             
                aResult.update({
                    'success': True,
                    'changed': False,
                    'estadoTraduccion_newValue': cEstadoTraduccionPendiente,
                })
                          
                return aResult
            
                 
            aMembershipTool = getToolByName( self, 'portal_membership', None)
            unMember = aMembershipTool.getAuthenticatedMember()   
            if not unMember:
                aResult.update({
                    'status': 'authenticated_member_not_found',
                })
                return aResult                
            if unMember.getUserName() == 'Anonymous User':
                unMemberId = unMember.getUserName()
            else:
                unMemberId = unMember.getMemberId()   
            if not unMemberId:
                aResult.update({
                    'status': 'authenticated_member_id_missing',
                })
                return aResult
    
            aResult[ 'memberid'] = unMemberId
         
            
            unAhoraStoreString = self.fDateTimeNowTextual()

            unTranslationActivity = self.fNewVoidTranslationActivity()
            unTranslationActivity.update( { 
                cRecentActivity_Action:      cTranslationHistoryAction_Invalidar,
                cRecentActivity_Date:        unAhoraStoreString,
                cRecentActivity_User:        unMemberId,
                cRecentActivity_Language:    self.getCodigoIdiomaEnGvSIG(),
                cRecentActivity_Symbol:      self.getSimbolo(),
            })
            
            unHayCambio = False
            try:
                self.setCadenaTraducida(   "") 
                self.setEstadoTraduccion(  cEstadoTraduccionPendiente)    
                
                aResult[ 'estadoTraduccion_newValue']      = cEstadoTraduccionPendiente
                
                if  unUsuarioTraductor:
                    self.setUsuarioTraductor(  None)   
                    
                if  unaFechaTraduccionTextual:
                    self.setFechaTraduccionTextual(   None)
                   
                if  unUsuarioRevisor:
                    self.setUsuarioRevisor(  None)   
                    
                if  unaFechaRevisionTextual:
                    self.setFechaRevisionTextual(   None)    
                    
                if  unaFechaDefinitivoTextual:
                    self.setFechaDefinitivoTextual(   None)    
                                                        
                if  unUsuarioCoordinador:
                    self.setUsuarioCoordinador(  None)   
                        
                
                                        
                unNuevoComentario = theComentario
                if not unNuevoComentario:
                    unNuevoComentario = ""            
                unNuevoComentario = unNuevoComentario.strip()
                unComentarioParaHistoria = cMarcaDeComentarioSinCambios
                if not ( unNuevoComentario == unComentarioTraduccion):
                    unComentarioParaHistoria = unNuevoComentario
                    self.setComentario(  unNuevoComentario)       
        
                    unTranslationActivity[ cRecentActivity_Commented] = True
        
                        
                unContadorCambiosActual = self.getContadorCambios()
                if not unContadorCambiosActual:
                    unContadorCambiosActual = 0

                unNuevoContadorCambios = unContadorCambiosActual + 1
                self.setContadorCambios( unNuevoContadorCambios)

                unTranslationActivity[ cRecentActivity_Counter] = unNuevoContadorCambios
                
                if theRegistrarHistoria:
                    self.pRegistrarHistoria( 
                        theAccion                   = cTranslationHistoryAction_Invalidar, 
                        theFechaAccionTextual       = unAhoraStoreString, 
                        theUsuarioActor             = unMemberId, 
                        theEstadoTraduccion         = cEstadoTraduccionPendiente, 
                        theFechaTraduccionTextual   = None, 
                        theUsuarioTraductor         = None, 
                        theCadenaTraducida          = unaCadenaTraducida, 
                        theFechaRevisionTextual     = None, 
                        theUsuarioRevisor           = None, 
                        theFechaDefinitivoTextual   = None, 
                        theUsuarioCoordinador       = None, 
                        theComentario               = unComentarioParaHistoria,                   
                    )
                                       
                unHayCambio = True
                aResult.update({
                    'success': True,
                    'changed': True,
                    'estadoTraduccion_newValue': cEstadoTraduccionPendiente,
                })
                return aResult
    
            finally:
                if unHayCambio:
                    self.pRecatalogTraduccion( unExecutionRecord)
                        
                    unCatalogo = self.getCatalogo()
                    if not ( unCatalogo == None):
                        unCatalogo.pTranslationActivityOccurred( unTranslationActivity)

                    if cLogTranslationChanges:
                        logging.getLogger( 'gvSIGi18n::fHacerPendiente').info( "CHANGED")               
       
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            
  

     
    
    
    
    

     
    security.declarePrivate( 'fHacerPendiente')
    def fHacerPendiente( self, 
        theComentario, 
        theAdditionalParams      =None,
        theUseCaseQueryResult    =None, 
        theRegistrarHistoria     =True, 
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):
    
        unExecutionRecord = self.fStartExecution( 'method',  'fHacerPendiente', theParentExecutionRecord,  False)  
        
        try:
            aResult = self.fNewVoidChangeTranslationResult()
            
            
            unContadorCambiosString = theAdditionalParams.get( 'theContadorCambios', None)
            if unContadorCambiosString:
                unContadorCambios = -1
                try:
                    unContadorCambios = int( unContadorCambiosString)
                except:
                    None
                if unContadorCambios >= 0:
                    unContadorCambiosActual = self.getContadorCambios()
                    if not( unContadorCambios == None):
                        if not ( unContadorCambios == unContadorCambiosActual):
                            return self.fResultForChangeCounterDetectedOverwrite(
                                theAdditionalParams      =theAdditionalParams,
                                theUseCaseQueryResult    =theUseCaseQueryResult, 
                                theRegistrarHistoria     =theRegistrarHistoria, 
                                thePermissionsCache      =thePermissionsCache, 
                                theRolesCache            =theRolesCache, 
                                theParentExecutionRecord =theParentExecutionRecord,
                            )
                        
            unaCadena = self.getCadena()
            if not unaCadena:
                return aResult
            
            aResult.update({
                'simboloCadena': unaCadena.getSimbolo(),
                'idCadena':      unaCadena.getId(),
                   
            })
            aResult[ 'found'] = True
            
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
                
            unaCadenaTraducida          = self.getCadenaTraducida()            
            unComentarioTraduccion      = self.getComentario() 
            unaHistoriaTraduccion       = self.getHistoria()
            unEstadoTraduccion          = self.getEstadoTraduccion()  
            unaFechaTraduccionTextual   = self.getFechaTraduccionTextual()  
            unUsuarioTraductor          = self.getUsuarioTraductor()  
            unaFechaRevisionTextual     = self.getFechaRevisionTextual()  
            unUsuarioRevisor            = self.getUsuarioRevisor()  
            unaFechaDefinitivoTextual   = self.getFechaDefinitivoTextual()  
            unUsuarioCoordinador        = self.getUsuarioCoordinador()  
            
            aResult[ 'estadoTraduccion_previousValue'] = unEstadoTraduccion

            unUseCaseQueryResult = theUseCaseQueryResult
            if not unUseCaseQueryResult or not ( unUseCaseQueryResult.get( 'use_case_name', '') == cUseCase_TRATraduccionStateChange):
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_TRATraduccionStateChange,        
                    theElementsBindings     = { cBoundObject: self,},                                    
                    theRulesToCollect       = None,                                                      
                    thePermissionsCache     = unPermissionsCache,                                        
                    theRolesCache           = unRolesCache,                                              
                    theParentExecutionRecord= unExecutionRecord,                                          
                )                    
            if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                aResult.update({
                    'status': 'UseCase_assessment_failed: %s' % cUseCase_TRATraduccionStateChange,
                })
                return aResult
                 
                
            if not self.fCanChangeToNuevoEstadoTraduccion( 
                cEstadoTraduccionPendiente, 
                unUseCaseQueryResult, 
                thePermissionsCache=unPermissionsCache, 
                theRolesCache=unRolesCache, 
                theParentExecutionRecord=unExecutionRecord):
                
                aResult.update({
                    'status': 'fCanChangeToNuevoEstadoTraduccion_failed',
                })
                return aResult
             
                          
            
                 
            aMembershipTool = getToolByName( self, 'portal_membership', None)
            unMember = aMembershipTool.getAuthenticatedMember()   
            if not unMember:
                aResult.update({
                    'status': 'authenticated_member_not_found',
                })
                return aResult                
            if unMember.getUserName() == 'Anonymous User':
                unMemberId = unMember.getUserName()
            else:
                unMemberId = unMember.getMemberId()   
            if not unMemberId:
                aResult.update({
                    'status': 'authenticated_member_id_missing',
                })
                return aResult
    
            aResult[ 'memberid'] = unMemberId
         
            
            unAhoraStoreString = self.fDateTimeNowTextual()
        
            
            unTranslationActivity = self.fNewVoidTranslationActivity()
            unTranslationActivity.update( { 
                cRecentActivity_Action:      cTranslationHistoryAction_HacerPendiente,
                cRecentActivity_Date:        unAhoraStoreString,
                cRecentActivity_User:        unMemberId,
                cRecentActivity_Language:    self.getCodigoIdiomaEnGvSIG(),
                cRecentActivity_Symbol:      self.getSimbolo(),
            })
            
            unHayCambio = False
            try:
                self.setCadenaTraducida(   "") 
                self.setEstadoTraduccion(  cEstadoTraduccionPendiente)    
                
                aResult[ 'estadoTraduccion_newValue']      = cEstadoTraduccionPendiente
                
                if  unUsuarioTraductor:
                    self.setUsuarioTraductor(  None)   
                    
                if  unaFechaTraduccionTextual:
                    self.setFechaTraduccionTextual(   None)
                   
                if  unUsuarioRevisor:
                    self.setUsuarioRevisor(  None)   
                    
                if  unaFechaRevisionTextual:
                    self.setFechaRevisionTextual(   None)    
                    
                if  unaFechaDefinitivoTextual:
                    self.setFechaDefinitivoTextual(   None)    
                                                        
                if  unUsuarioCoordinador:
                    self.setUsuarioCoordinador(  None)   
                        
                
                                        
                unNuevoComentario = theComentario
                if not unNuevoComentario:
                    unNuevoComentario = ""            
                unNuevoComentario = unNuevoComentario.strip()
                unComentarioParaHistoria = cMarcaDeComentarioSinCambios
                if not ( unNuevoComentario == unComentarioTraduccion):
                    unComentarioParaHistoria = unNuevoComentario
                    self.setComentario(  unNuevoComentario)       
                    
                    unTranslationActivity[ cRecentActivity_Commented] = True
        
                        
                unContadorCambiosActual = self.getContadorCambios()
                if not unContadorCambiosActual:
                    unContadorCambiosActual = 0

                unNuevoContadorCambios = unContadorCambiosActual + 1
                self.setContadorCambios( unNuevoContadorCambios)

                unTranslationActivity[ cRecentActivity_Counter] = unNuevoContadorCambios
        
                if theRegistrarHistoria:
                    self.pRegistrarHistoria( 
                        theAccion                   = cTranslationHistoryAction_HacerPendiente, 
                        theFechaAccionTextual       = unAhoraStoreString, 
                        theUsuarioActor             = unMemberId, 
                        theEstadoTraduccion         = cEstadoTraduccionPendiente, 
                        theFechaTraduccionTextual   = None, 
                        theUsuarioTraductor         = None, 
                        theCadenaTraducida          = unaCadenaTraducida, 
                        theFechaRevisionTextual     = None, 
                        theUsuarioRevisor           = None, 
                        theFechaDefinitivoTextual   = None, 
                        theUsuarioCoordinador       = None, 
                        theComentario               = unComentarioParaHistoria,                   
                    )
                                       
                unHayCambio = True
                aResult.update({
                    'success': True,
                    'changed': True,
                    'estadoTraduccion_newValue': cEstadoTraduccionPendiente,
                })
                return aResult
    
            finally:
                if unHayCambio:
                    self.pRecatalogTraduccion( unExecutionRecord)
                        
                        
                    unCatalogo = self.getCatalogo()
                    if not ( unCatalogo == None):
                        unCatalogo.pTranslationActivityOccurred( unTranslationActivity)

                    if cLogTranslationChanges:
                        logging.getLogger( 'gvSIGi18n::fHacerPendiente').info( "CHANGED")               
       
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            
  

 
    
   
    

     
   
     
    security.declarePrivate( 'fHacerTraducida')
    def fHacerTraducida( self, 
        theComentario, 
        theAdditionalParams      =None,
        theUseCaseQueryResult    =None,         
        theRegistrarHistoria     =True, 
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):
    
        unExecutionRecord = self.fStartExecution( 'method',  'fHacerTraducida', theParentExecutionRecord,  False) 
        
        try:
            aResult = self.fNewVoidChangeTranslationResult()
            
            
            unContadorCambiosString = theAdditionalParams.get( 'theContadorCambios', None)
            if unContadorCambiosString:
                unContadorCambios = -1
                try:
                    unContadorCambios = int( unContadorCambiosString)
                except:
                    None
                if unContadorCambios >= 0:
                    unContadorCambiosActual = self.getContadorCambios()
                    if not( unContadorCambios == None):
                        if not ( unContadorCambios == unContadorCambiosActual):
                            return self.fResultForChangeCounterDetectedOverwrite(
                                theAdditionalParams      =theAdditionalParams,
                                theUseCaseQueryResult    =theUseCaseQueryResult, 
                                theRegistrarHistoria     =theRegistrarHistoria, 
                                thePermissionsCache      =thePermissionsCache, 
                                theRolesCache            =theRolesCache, 
                                theParentExecutionRecord =theParentExecutionRecord,
                            )
                        
            unaCadena = self.getCadena()
            if not unaCadena:
                return aResult
            
            aResult.update({
                'simboloCadena': unaCadena.getSimbolo(),
                'idCadena':      unaCadena.getId(),
                   
            })
            aResult[ 'found'] = True
            
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache

            unaCadenaTraducida          = self.getCadenaTraducida()            
            unComentarioTraduccion      = self.getComentario() 
            unaHistoriaTraduccion       = self.getHistoria()
            unEstadoTraduccion          = self.getEstadoTraduccion()  
            unaFechaTraduccionTextual   = self.getFechaTraduccionTextual()  
            unUsuarioTraductor          = self.getUsuarioTraductor()  
            unaFechaRevisionTextual     = self.getFechaRevisionTextual()  
            unUsuarioRevisor            = self.getUsuarioRevisor()  
            unaFechaDefinitivoTextual   = self.getFechaDefinitivoTextual()  
            unUsuarioCoordinador        = self.getUsuarioCoordinador()  
            
            aResult[ 'estadoTraduccion_previousValue'] = unEstadoTraduccion

            
            if not unaCadenaTraducida:
                aResult.update({
                    'status': 'CanNotChangeStateWithEmptyCadenaTraducida',
                })
                return aResult
            
            unUseCaseQueryResult = theUseCaseQueryResult
            if not unUseCaseQueryResult or not ( unUseCaseQueryResult.get( 'use_case_name', '') == cUseCase_TRATraduccionStateChange):
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_TRATraduccionStateChange,        
                    theElementsBindings     = { cBoundObject: self,},                                    
                    theRulesToCollect       = None,                                                      
                    thePermissionsCache     = unPermissionsCache,                                        
                    theRolesCache           = unRolesCache,                                              
                    theParentExecutionRecord= unExecutionRecord,                                          
                )                    
                
            if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                aResult.update({
                    'status': 'UseCase_assessment_failed: %s' % cUseCase_TRATraduccionStateChange,
                })
                return aResult
                 
                
            if not self.fCanChangeToNuevoEstadoTraduccion( 
                cEstadoTraduccionTraducida, 
                unUseCaseQueryResult, 
                thePermissionsCache=unPermissionsCache, 
                theRolesCache=unRolesCache, 
                theParentExecutionRecord=unExecutionRecord):

                aResult.update({
                    'status': 'fCanChangeToNuevoEstadoTraduccion_failed',
                })
                return aResult

            
             
                 
            aMembershipTool = getToolByName( self, 'portal_membership', None)
            unMember = aMembershipTool.getAuthenticatedMember()   
            if not unMember:
                aResult.update({
                    'status': 'authenticated_member_not_found',
                })
                return aResult                
            if unMember.getUserName() == 'Anonymous User':
                unMemberId = unMember.getUserName()
            else:
                unMemberId = unMember.getMemberId()   
            if not unMemberId:
                aResult.update({
                    'status': 'authenticated_member_id_missing',
                })
                return aResult
    
            aResult[ 'memberid'] = unMemberId
         
            
            unAhoraStoreString = self.fDateTimeNowTextual()
            
            unTranslationActivity = self.fNewVoidTranslationActivity()
            unTranslationActivity.update( { 
                cRecentActivity_Action:      cTranslationHistoryAction_HacerTraducida,
                cRecentActivity_Date:        unAhoraStoreString,
                cRecentActivity_User:        unMemberId,
                cRecentActivity_Language:    self.getCodigoIdiomaEnGvSIG(),
                cRecentActivity_Symbol:      self.getSimbolo(),
            })
            
        
            unHayCambio = False
            try:
                self.setEstadoTraduccion(  cEstadoTraduccionTraducida)    
                self.setFechaTraduccionTextual(   unAhoraStoreString)
                
                aResult[ 'estadoTraduccion_newValue'] = cEstadoTraduccionTraducida
 
                if  unUsuarioRevisor:
                    self.setUsuarioRevisor(  None)   
                    
                if  unaFechaRevisionTextual:
                    self.setFechaRevisionTextual(   None)    
                    
                if  unaFechaDefinitivoTextual:
                    self.setFechaDefinitivoTextual(   None)    
                                                        
                if  unUsuarioCoordinador:
                    self.setUsuarioCoordinador(  None)   
                                        
                unNuevoComentario = theComentario
                if not unNuevoComentario:
                    unNuevoComentario = ""            
                unNuevoComentario = unNuevoComentario.strip()
                unComentarioParaHistoria = cMarcaDeComentarioSinCambios
                if not ( unNuevoComentario == unComentarioTraduccion):
                    unComentarioParaHistoria = unNuevoComentario
                    self.setComentario(  unNuevoComentario)       
                    
                    unTranslationActivity[ cRecentActivity_Commented] = True
        
        
                        
                unContadorCambiosActual = self.getContadorCambios()
                if not unContadorCambiosActual:
                    unContadorCambiosActual = 0

                unNuevoContadorCambios = unContadorCambiosActual + 1
                self.setContadorCambios( unNuevoContadorCambios)

                
                unTranslationActivity[ cRecentActivity_Counter] = unNuevoContadorCambios
                
                if theRegistrarHistoria:
                    self.pRegistrarHistoria( 
                        theAccion                   = cTranslationHistoryAction_HacerTraducida,      
                        theFechaAccionTextual       = unAhoraStoreString,         
                        theUsuarioActor             = unMemberId,                 
                        theEstadoTraduccion         = cEstadoTraduccionTraducida,  
                        theFechaTraduccionTextual   = unaFechaTraduccionTextual,  
                        theUsuarioTraductor         = unUsuarioTraductor,         
                        theCadenaTraducida          = unaCadenaTraducida ,        
                        theFechaRevisionTextual     = None,                       
                        theUsuarioRevisor           = None,                       
                        theFechaDefinitivoTextual   = None,                       
                        theUsuarioCoordinador       = None,                       
                        theComentario               = unComentarioParaHistoria,                   
                    )
                                       
                unHayCambio = True
                aResult.update({
                    'success': True,
                    'changed': True,
                    'estadoTraduccion_newValue': cEstadoTraduccionTraducida,
                })
                return aResult
    
            finally:
                if unHayCambio:
                    self.pRecatalogTraduccion( unExecutionRecord)
                        
                        
                    unCatalogo = self.getCatalogo()
                    if not ( unCatalogo == None):
                        unCatalogo.pTranslationActivityOccurred( unTranslationActivity)

                    if cLogTranslationChanges:
                        logging.getLogger( 'gvSIGi18n::fHacerTraducida').info( "CHANGED")    
                        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            
  

 
     
 



   
     
    security.declarePrivate( 'fHacerRevisada')
    def fHacerRevisada( self, 
        theComentario, 
        theAdditionalParams      =None,
        theUseCaseQueryResult    =None,         
        theRegistrarHistoria     =True, 
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):

        unExecutionRecord = self.fStartExecution( 'method',  'fHacerRevisada', theParentExecutionRecord,  False) 
        
        try:
            aResult = self.fNewVoidChangeTranslationResult()
            
            
            unContadorCambiosString = theAdditionalParams.get( 'theContadorCambios', None)
            if unContadorCambiosString:
                unContadorCambios = -1
                try:
                    unContadorCambios = int( unContadorCambiosString)
                except:
                    None
                if unContadorCambios >= 0:
                    unContadorCambiosActual = self.getContadorCambios()
                    if not( unContadorCambios == None):
                        if not ( unContadorCambios == unContadorCambiosActual):
                            return self.fResultForChangeCounterDetectedOverwrite(
                                theAdditionalParams      =theAdditionalParams,
                                theUseCaseQueryResult    =theUseCaseQueryResult, 
                                theRegistrarHistoria     =theRegistrarHistoria, 
                                thePermissionsCache      =thePermissionsCache, 
                                theRolesCache            =theRolesCache, 
                                theParentExecutionRecord =theParentExecutionRecord,
                            )
                        
            unaCadena = self.getCadena()
            if not unaCadena:
                return aResult
            
            aResult.update({
                'simboloCadena': unaCadena.getSimbolo(),
                'idCadena':      unaCadena.getId(),
                   
            })
            aResult[ 'found'] = True
            
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                 
            unaCadenaTraducida          = self.getCadenaTraducida()            
            unComentarioTraduccion      = self.getComentario() 
            unaHistoriaTraduccion       = self.getHistoria()
            unEstadoTraduccion          = self.getEstadoTraduccion()  
            unaFechaTraduccionTextual   = self.getFechaTraduccionTextual()  
            unUsuarioTraductor          = self.getUsuarioTraductor()  
            unaFechaRevisionTextual     = self.getFechaRevisionTextual()  
            unUsuarioRevisor            = self.getUsuarioRevisor()  
            unaFechaDefinitivoTextual   = self.getFechaDefinitivoTextual()  
            unUsuarioCoordinador        = self.getUsuarioCoordinador()  
           
            aResult[ 'estadoTraduccion_previousValue'] = unEstadoTraduccion

            if not unaCadenaTraducida:
                aResult.update({
                    'status': 'CanNotChangeStateWithEmptyCadenaTraducida',
                })
                return aResult
            
            unUseCaseQueryResult = theUseCaseQueryResult
            if not unUseCaseQueryResult or not ( unUseCaseQueryResult.get( 'use_case_name', '') == cUseCase_TRATraduccionStateChange):
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_TRATraduccionStateChange,        
                    theElementsBindings     = { cBoundObject: self,},                                    
                    theRulesToCollect       = None,                                                      
                    thePermissionsCache     = unPermissionsCache,                                        
                    theRolesCache           = unRolesCache,                                              
                    theParentExecutionRecord= unExecutionRecord,                                          
                )   
            if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                aResult.update({
                    'status': 'UseCase_assessment_failed: %s' % cUseCase_TRATraduccionStateChange,
                })
                return aResult
                 
                
            if not self.fCanChangeToNuevoEstadoTraduccion( 
                cEstadoTraduccionRevisada, 
                unUseCaseQueryResult, 
                thePermissionsCache=unPermissionsCache, 
                theRolesCache=unRolesCache, 
                theParentExecutionRecord=unExecutionRecord):

                aResult.update({
                    'status': 'fCanChangeToNuevoEstadoTraduccion_failed',
                })
                return aResult
    
                      
            
                 
            aMembershipTool = getToolByName( self, 'portal_membership', None)
            unMember = aMembershipTool.getAuthenticatedMember()   
            if not unMember:
                aResult.update({
                    'status': 'authenticated_member_not_found',
                })
                return aResult                
            if unMember.getUserName() == 'Anonymous User':
                unMemberId = unMember.getUserName()
            else:
                unMemberId = unMember.getMemberId()   
            if not unMemberId:
                aResult.update({
                    'status': 'authenticated_member_id_missing',
                })
                return aResult
    
            aResult[ 'memberid'] = unMemberId
         
            
            unAhoraStoreString = self.fDateTimeNowTextual()
            
            unTranslationActivity = self.fNewVoidTranslationActivity()
            unTranslationActivity.update( { 
                cRecentActivity_Action:      cTranslationHistoryAction_HacerRevisada,
                cRecentActivity_Date:        unAhoraStoreString,
                cRecentActivity_User:        unMemberId,
                cRecentActivity_Language:    self.getCodigoIdiomaEnGvSIG(),
                cRecentActivity_Symbol:      self.getSimbolo(),
            })
            
        
            
            unHayCambio = False
            try:
                                                                                    
                self.setEstadoTraduccion(  cEstadoTraduccionRevisada)    
                self.setUsuarioRevisor(     unMemberId)  
                self.setFechaRevisionTextual(   unAhoraStoreString)
                
                aResult[ 'estadoTraduccion_newValue'] = cEstadoTraduccionRevisada
                     
                if  unaFechaDefinitivoTextual:
                    self.setFechaDefinitivoTextual(   None)    
                                                        
                if  unUsuarioCoordinador:
                    self.setUsuarioCoordinador(  None)   
                                                        
                unNuevoComentario = theComentario
                if not unNuevoComentario:
                    unNuevoComentario = ""            
                unNuevoComentario = unNuevoComentario.strip()
                unComentarioParaHistoria = cMarcaDeComentarioSinCambios
                if not ( unNuevoComentario == unComentarioTraduccion):
                    unComentarioParaHistoria = unNuevoComentario
                    self.setComentario(  unNuevoComentario)       
        
                    unTranslationActivity[ cRecentActivity_Commented] = True
        
                        
                unContadorCambiosActual = self.getContadorCambios()
                if not unContadorCambiosActual:
                    unContadorCambiosActual = 0

                unNuevoContadorCambios = unContadorCambiosActual + 1
                self.setContadorCambios( unNuevoContadorCambios)
                
                unTranslationActivity[ cRecentActivity_Counter] = unNuevoContadorCambios
                

                if theRegistrarHistoria:
                    self.pRegistrarHistoria( 
                        theAccion                   = cTranslationHistoryAction_HacerRevisada, 
                        theFechaAccionTextual       = unAhoraStoreString, 
                        theUsuarioActor             = unMemberId, 
                        theEstadoTraduccion         = cEstadoTraduccionRevisada, 
                        theFechaTraduccionTextual   = unaFechaTraduccionTextual, 
                        theUsuarioTraductor         = unUsuarioTraductor, 
                        theCadenaTraducida          = unaCadenaTraducida, 
                        theFechaRevisionTextual     = unAhoraStoreString, 
                        theUsuarioRevisor           = unMemberId, 
                        theFechaDefinitivoTextual   = None, 
                        theUsuarioCoordinador       = None, 
                        theComentario               = unComentarioParaHistoria,
                    )
                    
                unHayCambio = True
                aResult.update({
                    'success': True,
                    'changed': True,
                    'estadoTraduccion_newValue': cEstadoTraduccionRevisada,
               })
                return aResult
    
            finally:
                if unHayCambio:
                    self.pRecatalogTraduccion( unExecutionRecord)
                        
                        
                    unCatalogo = self.getCatalogo()
                    if not ( unCatalogo == None):
                        unCatalogo.pTranslationActivityOccurred( unTranslationActivity)

                    if cLogTranslationChanges:
                        logging.getLogger( 'gvSIGi18n::fHacerRevisada').info( "CHANGED")               

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            
  


     
  
        
    
      
    security.declarePrivate( 'fHacerDefinitiva')
    def fHacerDefinitiva( self, 
        theComentario, 
        theAdditionalParams      =None,
        theUseCaseQueryResult    =None,         
        theRegistrarHistoria     =True, 
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):

        unExecutionRecord = self.fStartExecution( 'method',  'fHacerDefinitiva', theParentExecutionRecord,  False) 
        
        try:
            aResult = self.fNewVoidChangeTranslationResult()
            
            
            unContadorCambiosString = theAdditionalParams.get( 'theContadorCambios', None)
            if unContadorCambiosString:
                unContadorCambios = -1
                try:
                    unContadorCambios = int( unContadorCambiosString)
                except:
                    None
                if unContadorCambios >= 0:
                    unContadorCambiosActual = self.getContadorCambios()
                    if not( unContadorCambios == None):
                        if not ( unContadorCambios == unContadorCambiosActual):
                            return self.fResultForChangeCounterDetectedOverwrite(
                                theAdditionalParams      =theAdditionalParams,
                                theUseCaseQueryResult    =theUseCaseQueryResult, 
                                theRegistrarHistoria     =theRegistrarHistoria, 
                                thePermissionsCache      =thePermissionsCache, 
                                theRolesCache            =theRolesCache, 
                                theParentExecutionRecord =theParentExecutionRecord,
                            )
                        
            unaCadena = self.getCadena()
            if not unaCadena:
                return aResult
            
            aResult.update({
                'simboloCadena': unaCadena.getSimbolo(),
                'idCadena':      unaCadena.getId(),
                   
            })
            aResult[ 'found'] = True
            
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
                 
            unaCadenaTraducida          = self.getCadenaTraducida()            
            unComentarioTraduccion      = self.getComentario() 
            unaHistoriaTraduccion       = self.getHistoria()
            unEstadoTraduccion          = self.getEstadoTraduccion()  
            unaFechaTraduccionTextual   = self.getFechaTraduccionTextual()  
            unUsuarioTraductor          = self.getUsuarioTraductor()  
            unaFechaRevisionTextual     = self.getFechaRevisionTextual()  
            unUsuarioRevisor            = self.getUsuarioRevisor()  
            unaFechaDefinitivoTextual   = self.getFechaDefinitivoTextual()  
            unUsuarioCoordinador        = self.getUsuarioCoordinador()  
           
            aResult[ 'estadoTraduccion_previousValue'] = unEstadoTraduccion

            if not unaCadenaTraducida:
                aResult.update({
                    'status': 'CanNotChangeStateWithEmptyCadenaTraducida',
                })
                return aResult
            
            unUseCaseQueryResult = theUseCaseQueryResult
            if not unUseCaseQueryResult or not ( unUseCaseQueryResult.get( 'use_case_name', '') == cUseCase_TRATraduccionStateChange):
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_TRATraduccionStateChange,        
                    theElementsBindings     = { cBoundObject: self,},                                    
                    theRulesToCollect       = None,                                                      
                    thePermissionsCache     = unPermissionsCache,                                        
                    theRolesCache           = unRolesCache,                                              
                    theParentExecutionRecord= unExecutionRecord,                                          
                )   

            if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                aResult.update({
                    'status': 'UseCase_assessment_failed: %s' % cUseCase_TRATraduccionStateChange,
                })
                return aResult
                 
                
                
            if not self.fCanChangeToNuevoEstadoTraduccion( 
                cEstadoTraduccionDefinitiva, 
                unUseCaseQueryResult, 
                thePermissionsCache=unPermissionsCache, 
                theRolesCache=unRolesCache, 
                theParentExecutionRecord=unExecutionRecord):

                aResult.update({
                    'status': 'fCanChangeToNuevoEstadoTraduccion_failed',
                })
                return aResult
    
            
                 
            aMembershipTool = getToolByName( self, 'portal_membership', None)
            unMember = aMembershipTool.getAuthenticatedMember()   
            if not unMember:
                aResult.update({
                    'status': 'authenticated_member_not_found',
                })
                return aResult                
            if unMember.getUserName() == 'Anonymous User':
                unMemberId = unMember.getUserName()
            else:
                    unMemberId = unMember.getMemberId()   
            if not unMemberId:
                aResult.update({
                    'status': 'authenticated_member_id_missing',
                })
                return aResult
    
            aResult[ 'memberid'] = unMemberId
         
    
            unAhoraStoreString = self.fDateTimeNowTextual()
    

            unTranslationActivity = self.fNewVoidTranslationActivity()
            unTranslationActivity.update( { 
                cRecentActivity_Action:      cTranslationHistoryAction_HacerDefinitiva,
                cRecentActivity_Date:        unAhoraStoreString,
                cRecentActivity_User:        unMemberId,
                cRecentActivity_Language:    self.getCodigoIdiomaEnGvSIG(),
                cRecentActivity_Symbol:      self.getSimbolo(),
            })

            unHayCambio = False
            try:
                self.setEstadoTraduccion(         cEstadoTraduccionDefinitiva)    
                self.setFechaDefinitivoTextual(   unAhoraStoreString)
                self.setUsuarioCoordinador(       unMemberId)

                aResult[ 'estadoTraduccion_newValue'] = cEstadoTraduccionDefinitiva
                
                unNuevoComentario = theComentario
                if not unNuevoComentario:
                    unNuevoComentario = ""            
                unNuevoComentario = unNuevoComentario.strip()
                unComentarioParaHistoria = cMarcaDeComentarioSinCambios
                if not ( unNuevoComentario == unComentarioTraduccion):
                    unComentarioParaHistoria = unNuevoComentario        
                    self.setComentario(  unNuevoComentario)       
        
                    unTranslationActivity[ cRecentActivity_Commented] = True
        
        
                        
                unContadorCambiosActual = self.getContadorCambios()
                if not unContadorCambiosActual:
                    unContadorCambiosActual = 0

                unNuevoContadorCambios = unContadorCambiosActual + 1
                self.setContadorCambios( unNuevoContadorCambios)
                
                unTranslationActivity[ cRecentActivity_Counter] = unNuevoContadorCambios

                if theRegistrarHistoria:
                    self.pRegistrarHistoria( 
                        theAccion                   = cTranslationHistoryAction_HacerDefinitiva, 
                        theFechaAccionTextual       = unAhoraStoreString, 
                        theUsuarioActor             = unMemberId, 
                        theEstadoTraduccion         = cEstadoTraduccionDefinitiva, 
                        theFechaTraduccionTextual   = unaFechaTraduccionTextual, 
                        theUsuarioTraductor         = unUsuarioTraductor, 
                        theCadenaTraducida          = unaCadenaTraducida, 
                        theFechaRevisionTextual     = unaFechaRevisionTextual, 
                        theUsuarioRevisor           = unUsuarioRevisor, 
                        theFechaDefinitivoTextual   = unAhoraStoreString, 
                        theUsuarioCoordinador       = unMemberId, 
                        theComentario               = unComentarioParaHistoria               
                    )
               
                unHayCambio = True
                aResult.update({
                    'success': True,
                    'changed': True,
                    'estadoTraduccion_newValue': cEstadoTraduccionDefinitiva,
                })
                return aResult
    
            finally:
                if unHayCambio:
                    self.pRecatalogTraduccion( unExecutionRecord)
                        
                        
                    unCatalogo = self.getCatalogo()
                    if not ( unCatalogo == None):
                        unCatalogo.pTranslationActivityOccurred( unTranslationActivity)

                    if cLogTranslationChanges:
                        logging.getLogger( 'gvSIGi18n::fHacerDefinitiva').info( "CHANGED")               
    
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
        
        
      
        
    
    

    
            

    
     
    

    security.declarePrivate( 'fCanChangeToNuevoEstadoTraduccion')
    def fCanChangeToNuevoEstadoTraduccion( self, 
        theEstadoFinal, 
        theUseCaseQueryResult=None, 
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):
        """Query State Change Rules for permission to change from the current state to a new state.
        
        """
        
        if not theEstadoFinal:
            return False
        
        unEstadoTraduccion = self.getEstadoTraduccion()
        if not unEstadoTraduccion:
            return False
    
        return self.fCanChangeEstadoTraduccion( 
            unEstadoTraduccion, 
            theEstadoFinal, 
            theUseCaseQueryResult, 
            thePermissionsCache, 
            theRolesCache, 
            theParentExecutionRecord
        )
    
    
    
    
    
    
    
    
    
    security.declarePrivate( 'fCanChangeEstadoTraduccion')
    def fCanChangeEstadoTraduccion( self, 
        theEstadoInicial, 
        theEstadoFinal, 
        theUseCaseQueryResult=None, 
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):
        """Query State Change Rules for permission to change if the translation were in a given state to a new state.
        
        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fCanChangeEstadoTraduccion', theParentExecutionRecord,  False) 
        
        try:
            if not theEstadoInicial or not theEstadoFinal:
                return False
                    
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
            unUseCaseQueryResult = theUseCaseQueryResult
            if not unUseCaseQueryResult or not ( unUseCaseQueryResult.get( 'use_case_name', '') == cUseCase_TRATraduccionStateChange):
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_TRATraduccionStateChange,        
                    theElementsBindings     = { cBoundObject: self,},                                    
                    theRulesToCollect       = None,                                                      
                    thePermissionsCache     = unPermissionsCache,                                        
                    theRolesCache           = unRolesCache,                                              
                    theParentExecutionRecord= unExecutionRecord,                                          
                )   
            if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                return False
    
             
            unasStateChangeRules = cStateChangeActionRoles.get( theEstadoInicial, None)
            if not unasStateChangeRules:
                return False
            
            unosRolesParaTransicion = unasStateChangeRules.get( theEstadoFinal, None)
            if not unosRolesParaTransicion:
                return False
            
                
            unosOwnedRoles = self.fGetElementRoles( self, unRolesCache)

            if set( unosRolesParaTransicion).intersection( unosOwnedRoles):
                return True
                
            return  False
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
        
        

        
    
    
    
    
    security.declarePrivate( 'fCanChangeToAtLeastOneEstadoTraduccion')
    def fCanChangeToAtLeastOneEstadoTraduccion( self, 
        theUseCaseQueryResult=None, 
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):

        unExecutionRecord = self.fStartExecution( 'method',  'fCanChangeToAtLeastOneEstadoTraduccion', theParentExecutionRecord,  False) 
        
        try:
                    
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
            unUseCaseQueryResult = theUseCaseQueryResult
            if not unUseCaseQueryResult or not ( unUseCaseQueryResult.get( 'use_case_name', '') == cUseCase_TRATraduccionStateChange):
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_TRATraduccionStateChange,        
                    theElementsBindings     = { cBoundObject: self,},                                    
                    theRulesToCollect       = None,                                                      
                    thePermissionsCache     = unPermissionsCache,                                        
                    theRolesCache           = unRolesCache,                                              
                    theParentExecutionRecord= unExecutionRecord,                                          
                )    
            if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                return False
            
            unEstadoTraduccion = self.getEstadoTraduccion()
            if not unEstadoTraduccion:
                return False
            
            unasStateChangeRules = cStateChangeActionRoles.get( unEstadoTraduccion, None)
            if not unasStateChangeRules:
                return False
            
            unosEstadosFinales = unasStateChangeRules.keys()
            if not unosEstadosFinales:
                return False
    
            unosRolesParaTransicion = set()
            for unEstadoFinal in unosEstadosFinales:
                unosRoles = unasStateChangeRules.get( unEstadoFinal, None)
                if unosRoles:
                    unosRolesParaTransicion = unosRolesParaTransicion.union( unosRoles)
                    
            if not unosRolesParaTransicion:
                return False
            
            unosOwnedRoles = self.fGetElementRoles( self, unRolesCache)
 
            if set( unosRolesParaTransicion).intersection( unosOwnedRoles):
                return True
             
            return False
            
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
        

           
    
    
   
    
    security.declarePrivate( 'fCanChangeToWhichEstadosTraduccion')
    def fCanChangeToWhichEstadosTraduccion( self, 
        theUseCaseQueryResult=None, 
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):
    
        unExecutionRecord = self.fStartExecution( 'method',  'fCanChangeToWhichEstadosTraduccion', theParentExecutionRecord,  False) 
        
        try:
            
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
            unChangeStateUseCaseQueryResult = theUseCaseQueryResult
            if not unChangeStateUseCaseQueryResult or not ( unChangeStateUseCaseQueryResult.get( 'use_case_name', '') == cUseCase_TRATraduccionStateChange):

                unChangeStateUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_TRATraduccionStateChange, 
                    theElementsBindings     = { cBoundObject: self,},
                    theRulesToCollect       = None, 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord
                )    
                
                if not unChangeStateUseCaseQueryResult or not unChangeStateUseCaseQueryResult.get( 'success', False):
                    return []
            
            unEstadoTraduccion = self.getEstadoTraduccion()
            if not unEstadoTraduccion:
                return []
            
            unasStateChangeRules = cStateChangeActionRoles.get( unEstadoTraduccion, None)
            if not unasStateChangeRules:
                return []
            
            unosEstadosFinales = unasStateChangeRules.keys()
            if not unosEstadosFinales:
                return []
    
            unosEstadosFinalesPosibles = [ ]
            
            
            unosOwnedRoles = self.fGetElementRoles( self, unRolesCache)

            
            for unEstadoFinal in unosEstadosFinales:
                unosRoles = unasStateChangeRules.get( unEstadoFinal, None)
                if unosRoles:
                    if set( unosRoles).intersection( unosOwnedRoles):
                        unosEstadosFinalesPosibles.append( unEstadoFinal)

                        
            return unosEstadosFinalesPosibles
            
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
        

           
    
    
     
        
    
   
    
    
    security.declarePrivate( "fEmpaquetarRegistroHistoria")
    def fEmpaquetarRegistroHistoria( self, 
        theAccion, 
        theFechaAccionTextual, 
        theUsuarioActor, 
        theEstadoTraduccion, 
        theFechaTraduccionTextual, 
        theUsuarioTraductor, 
        theCadenaTraducida, 
        theFechaRevisionTextual, 
        theUsuarioRevisor, 
        theFechaDefinitivoTextual, 
        theUsuarioCoordinador, 
        theComentario):
        """Pack fields into a translation change history record string.
        
        """
       
        unRegistroHistoria = '\n'.join( [
            str( theAccion), 
            str( theFechaAccionTextual), 
            str( theUsuarioActor), 
            str( theEstadoTraduccion),
            ( theFechaTraduccionTextual and str( theFechaTraduccionTextual)) or '', 
            theUsuarioTraductor or '', 
            theCadenaTraducida or '', 
            ( theFechaRevisionTextual and str( theFechaRevisionTextual)) or '', 
            theUsuarioRevisor or '', 
            ( theFechaDefinitivoTextual and str( theFechaDefinitivoTextual)) or '', 
            theUsuarioCoordinador or '', 
            theComentario  or '',
        ])
        
        unRegistroHistoria = "%s\n%s\n" % ( unRegistroHistoria, cMarcaDeFinDeRegistroDeHistoria)
        
        return unRegistroHistoria   
 
 
 
 
    security.declarePrivate( "pRegistrarHistoria")
    def pRegistrarHistoria( self, 
        theAccion, 
        theFechaAccionTextual, 
        theUsuarioActor, 
        theEstadoTraduccion, 
        theFechaTraduccionTextual, 
        theUsuarioTraductor, 
        theCadenaTraducida, 
        theFechaRevisionTextual, 
        theUsuarioRevisor, 
        theFechaDefinitivoTextual, 
        theUsuarioCoordinador, 
        theComentario):
        """Append a new translation change history record.
        
        """
        
        unaHistoriaTraduccion = self.getHistoria()
        
        if not unaHistoriaTraduccion:
            unaHistoriaTraduccion = ""
        
        unRegistroHistoriaTraduccion = self.fEmpaquetarRegistroHistoria(  theAccion, theFechaAccionTextual, theUsuarioActor, theEstadoTraduccion, theFechaTraduccionTextual, theUsuarioTraductor, theCadenaTraducida, theFechaRevisionTextual, theUsuarioRevisor, theFechaDefinitivoTextual, theUsuarioCoordinador, theComentario)
        
        unaNuevaHistoriaTraduccion = unRegistroHistoriaTraduccion + unaHistoriaTraduccion
        
        self.setHistoria( unaNuevaHistoriaTraduccion)
        return self
    
    
    
    
    
    
    
    
    security.declarePrivate( 'getRegistrosHistoria')
    def getRegistrosHistoria( self):

        unosRegistrosHistoria = []

        unaHistoriaTraduccion = self.getHistoria()
        if not unaHistoriaTraduccion:
            return unosRegistrosHistoria
        
        unasLineasHistoria = unaHistoriaTraduccion.splitlines()
        unNumeroLineas = len( unasLineasHistoria)
        if unNumeroLineas < 1:
            return unosRegistrosHistoria
        
        unContadorLineas = 0
        
        unRegistroHistoria = { }
        
        while unContadorLineas < unNumeroLineas:
            unRegistroHistoria[ 'accion']                 = unasLineasHistoria[ unContadorLineas]
            unContadorLineas += 1
            if unContadorLineas < unNumeroLineas:
                unRegistroHistoria[ 'fechaAccion']        = unasLineasHistoria[ unContadorLineas]
                unContadorLineas += 1
            if unContadorLineas < unNumeroLineas:
                unRegistroHistoria[ 'usuarioActor']       = unasLineasHistoria[ unContadorLineas]
                unContadorLineas += 1
            if unContadorLineas < unNumeroLineas:
                unRegistroHistoria[ 'estadoTraduccion']   = unasLineasHistoria[ unContadorLineas]
                unContadorLineas += 1
            if unContadorLineas < unNumeroLineas:
                unRegistroHistoria[ 'fechaTraduccion']    = unasLineasHistoria[ unContadorLineas]
                unContadorLineas += 1
            if unContadorLineas < unNumeroLineas:
                unRegistroHistoria[ 'usuarioTraductor']   = unasLineasHistoria[ unContadorLineas]
                unContadorLineas += 1
            if unContadorLineas < unNumeroLineas:
                unRegistroHistoria[ 'cadenaTraducida']    = unasLineasHistoria[ unContadorLineas]
                unContadorLineas += 1
            if unContadorLineas < unNumeroLineas:
                unRegistroHistoria[ 'fechaRevision']      = unasLineasHistoria[ unContadorLineas]
                unContadorLineas += 1
            if unContadorLineas < unNumeroLineas:
                unRegistroHistoria[ 'usuarioRevisor']     = unasLineasHistoria[ unContadorLineas]
                unContadorLineas += 1
            if unContadorLineas < unNumeroLineas:
                unRegistroHistoria[ 'fechaDefinitivo']    = unasLineasHistoria[ unContadorLineas]
                unContadorLineas += 1
            if unContadorLineas < unNumeroLineas:
                unRegistroHistoria[ 'usuarioCoordinador'] = unasLineasHistoria[ unContadorLineas]
                unContadorLineas += 1
                
            unComentario = ""
            unRegistroHistoria[ 'comentario'] = unComentario
            while unContadorLineas < unNumeroLineas:
                unaLinea  = unasLineasHistoria[ unContadorLineas]
                unContadorLineas += 1
                if unaLinea == cMarcaDeFinDeRegistroDeHistoria:
                    if len( unComentario) > 0 and not( ''.join( unComentario.splitlines()).strip() == cMarcaDeComentarioSinCambios):
                        unRegistroHistoria[ 'comentario'] = unComentario
                        
                    unosRegistrosHistoria.append( unRegistroHistoria)
                    unRegistroHistoria = { }
                    break
                else:
                    unComentario = "%s\n%s" % ( unComentario, unaLinea)
                                        
        return unosRegistrosHistoria
        
                 
        





 
        




    security.declarePrivate( 'pResetHistoriaYComentario(')
    def pResetHistoriaYComentario( self, theUsuario, theDateTime):
        """Remove history and comment information. Set to Pending if no translated string.
 
        """
        
        if False:
            return self          

        if not self.fCanChange():
            return self

        if self.getCadenaTraducida().strip():
            self.setEstadoTraduccion( cEstadoTraduccionTraducida)
        else:
            self.setEstadoTraduccion( cEstadoTraduccionPendiente)
            
        self.setComentario("")
        self.setHistoria( "")        
        return self
    
    
    
    
    
    # ACV 20090322 Unused removed
    #security.declarePrivate( 'pInitPreviouslyComputedFields')    
    #def pInitPreviouslyComputedFields( self):
        #self.setSimbolo(        self.fDeriveSimboloCadena())
        #self.setEstadoCadena(   self.fDeriveEstadoCadena())
        #self.setIdCadena(       self.fDeriveIdCadena())
        
        #self.reindexObject()
       
    