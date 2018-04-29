# -*- coding: utf-8 -*-
#
# File: Catalogo_operations.py
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

import sys

import traceback

import logging

import transaction

from StringIO                       import StringIO

from Acquisition                    import aq_get

from AccessControl                  import ClassSecurityInfo

from Products.CMFCore               import permissions

from Products.Archetypes.utils      import shasattr
from Products.Archetypes.public     import DisplayList

from Products.CMFCore.utils         import getToolByName






from TRAElemento_Constants import *

from TRACatalogo_Inicializacion import cNombreCatalogoBusquedaCadenas, cNombreCatalogoFiltroCadenas, cNombreCatalogoTextoCadenas, cNombreCatalogoBusquedaTraducciones, cNombreCatalogoFiltroTraducciones, cNombreCatalogoTextoTraducciones

from TRAElemento import TRAElemento

from TRAElemento_Permission_Definitions import cUseCase_VerifyTRACatalogo, cUseCase_InitializeTRACatalogo, cUseCase_Export, cUseCase_ConfigureTRACatalogo
from TRAElemento_Permission_Definitions import cUseCase_AuthorizeUsers, cUseCase_ReviewUsersAuthorizations








cBusquedaTodasCadenasOrdenadasPorSimbolo = { 
        'getEstadoCadena':  cEstadoCadenaActiva, 
        'sort_on':          'getSimbolo',  
        'sort_order':       'ascending',
}           

cModuleStartLine = '===---==='       


cLogInicializarSimbolosCadenasOrdenados = True

  



class TRACatalogo_Operaciones:
    """
    """
    security = ClassSecurityInfo()

    

    
    
    

    
    security.declareProtected( permissions.View, 'getCatalogo')
    def getCatalogo( self):
        return self
        
    
    security.declarePrivate( 'fCodigoIdiomaPorDefecto')
    def fCodigoIdiomaPorDefecto( self, ):
        unCodigoIdioma = self.getCodigoIdiomaPorDefecto()
        if not unCodigoIdioma:
            unCodigoIdioma = cDefaultLanguage
            
        return unCodigoIdioma
        

    
    security.declarePrivate( 'fNombreModuloPorDefecto')
    def fNombreModuloPorDefecto( self, ):
        unNombreModulo = self.getNombreModuloPorDefecto()
        if not unNombreModulo:
            unNombreModulo = cDefaultModule
            
        return unNombreModulo
        
    
    security.declarePrivate( 'fModoInteraccionPorDefecto')
    def fModoInteraccionPorDefecto( self, ):
        unModoInteraccion = self.getModoInteraccionPorDefecto()
        if not unModoInteraccion:
            unModoInteraccion = cDefaultModoInteraccion
            
        return unModoInteraccion
    

    
    
    security.declarePrivate( 'fTraduccionesPorPaginaPorDefecto')
    def fTraduccionesPorPaginaPorDefecto( self, ):
        unasTraduccionesPorPagina = self.getTraduccionesPorPaginaPorDefecto()
        if not unasTraduccionesPorPagina:
            unasTraduccionesPorPagina = cDefaultTraduccionesPorPagina
            
        return unasTraduccionesPorPagina
    
    

    
   
    
    
    
    security.declarePrivate( 'fMaximoRegistrosExplorados')
    def fMaximoRegistrosExplorados( self, ):
        unMaximoRegistrosExplorados = self.getMaximoRegistrosExplorados()
        if not unMaximoRegistrosExplorados:
            unMaximoRegistrosExplorados = cMaximoRegistrosExplorados
            
        return unMaximoRegistrosExplorados
    
    
        
    
    
    security.declarePublic('fUseCaseCheckDoable_VerifyTRACatalogo')
    def fUseCaseCheckDoable_VerifyTRACatalogo(self, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):   

 
        unExecutionRecord = self.fStartExecution( 'method',  'fUseCaseCheckDoable_VerifyTRACatalogo', theParentExecutionRecord, False) 
        
        try:
            try:
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                    
                unUseCaseAssessmentResult = self.fUseCaseAssessment( 
                    theUseCaseName          = cUseCase_VerifyTRACatalogo, 
                    theElementsBindings     = { 'object': self,},
                    theRulesToCollect       = None, 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord)
                
                unResult = unUseCaseAssessmentResult and unUseCaseAssessmentResult.get( 'success', False)
                return unResult 
    
    
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fUseCaseCheckDoable_VerifyTRACatalogo\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
    
                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return False

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
     
        
    
    

    
    
    security.declarePublic('fUseCaseCheckDoable_ConfigureTRACatalogo')
    def fUseCaseCheckDoable_ConfigureTRACatalogo(self, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):   

 
        unExecutionRecord = self.fStartExecution( 'method',  'fUseCaseCheckDoable_ConfigureTRACatalogo', theParentExecutionRecord, False) 
        
        try:
            try:
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                    
                unUseCaseAssessmentResult = self.fUseCaseAssessment( 
                    theUseCaseName          = cUseCase_ConfigureTRACatalogo, 
                    theElementsBindings     = { 'object': self,},
                    theRulesToCollect       = None, 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord)
                
                unResult = unUseCaseAssessmentResult and unUseCaseAssessmentResult.get( 'success', False)
                return unResult 
    
    
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fUseCaseCheckDoable_ConfigureTRACatalogo\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
    
                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return False

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
     
        
    
    
    
    security.declarePublic('fUseCaseCheckDoable_InitializeTRACatalogo')
    def fUseCaseCheckDoable_InitializeTRACatalogo(self, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):   

 
        unExecutionRecord = self.fStartExecution( 'method',  'fUseCaseCheckDoable_InitializeTRACatalogo', theParentExecutionRecord, False) 
        
        try:
     
            try: 
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                    
                unUseCaseAssessmentResult = self.fUseCaseAssessment( 
                    theUseCaseName          = cUseCase_InitializeTRACatalogo, 
                    theElementsBindings     = { 'object': self,},
                    theRulesToCollect       = None, 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord)
                
                unResult = unUseCaseAssessmentResult and unUseCaseAssessmentResult.get( 'success', False)
                return unResult 
    
    
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fUseCaseCheckDoable_InitializeTRACatalogo\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
    
                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return False

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
     
        
    

    
    security.declarePublic('fUseCaseCheckDoable_Export')
    def fUseCaseCheckDoable_Export(self, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):   

 
        unExecutionRecord = self.fStartExecution( 'method',  'fUseCaseCheckDoable_Export', theParentExecutionRecord, False) 
        
        try:
     
            try: 
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                    
                unUseCaseAssessmentResult = self.fUseCaseAssessment( 
                    theUseCaseName          = cUseCase_Export, 
                    theElementsBindings     = { 'object': self,},
                    theRulesToCollect       = None, 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord)
                
                unResult = unUseCaseAssessmentResult and unUseCaseAssessmentResult.get( 'success', False)
                return unResult 
    
    
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fUseCaseCheckDoable_Export\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
    
                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return False

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
     

            
            
            
    
    security.declarePublic('fUseCaseCheckDoable_ReviewUsersAuthorizations')
    def fUseCaseCheckDoable_ReviewUsersAuthorizations(self, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):   

 
        unExecutionRecord = self.fStartExecution( 'method',  'fUseCaseCheckDoable_ReviewUsersAuthorizations', theParentExecutionRecord, False) 
        
        try:
            try:
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                    
                unUseCaseAssessmentResult = self.fUseCaseAssessment( 
                    theUseCaseName          = cUseCase_ReviewUsersAuthorizations, 
                    theElementsBindings     = { 'object': self,},
                    theRulesToCollect       = None, 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord)
                
                unResult = unUseCaseAssessmentResult and unUseCaseAssessmentResult.get( 'success', False)
                return unResult 
    
    
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fUseCaseCheckDoable_ReviewUsersAuthorizations\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
    
                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return False

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
     
        
            
            
            
            
    
    security.declarePublic('fUseCaseCheckDoable_AuthorizeUsers')
    def fUseCaseCheckDoable_AuthorizeUsers(self, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):   

 
        unExecutionRecord = self.fStartExecution( 'method',  'fUseCaseCheckDoable_AuthorizeUsers', theParentExecutionRecord, False) 
        
        try:
            try:
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                    
                unUseCaseAssessmentResult = self.fUseCaseAssessment( 
                    theUseCaseName          = cUseCase_AuthorizeUsers, 
                    theElementsBindings     = { 'object': self,},
                    theRulesToCollect       = None, 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord)
                
                unResult = unUseCaseAssessmentResult and unUseCaseAssessmentResult.get( 'success', False)
                return unResult 
    
    
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fUseCaseCheckDoable_AuthorizeUsers\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
    
                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return False

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
     
        
                
        
    # ####################################
    #  Complete initialization after creation
    # ####################################
        
        
    
    security.declarePrivate('pHandle_manage_afterAdd')
    def pHandle_manage_afterAdd(self, theItem, theContainer):   
        
        TRAElemento.manage_afterAdd(  self, theItem, theContainer)
        
        unInforme = self.fLazyCrear( 
            theAllowCreation        =True, 
            theCheckPermissions     =True,  
            thePermissionsCache     =None, 
            theRolesCache           =None, 
            theParentExecutionRecord=None
        )
        
        return self
    
         

    
    

    
    
        
    # ####################################
    """TRAIdioma accessors
    
    """

    
    security.declareProtected( permissions.View, 'fObtenerColeccionIdiomas')
    def fObtenerColeccionIdiomas( self, ):
   
        unasColecciones = self.objectValues( cNombreTipoTRAColeccionIdiomas) #
        if not unasColecciones:
            return None
        return unasColecciones[ 0]
         
  
        

    security.declarePrivate( 'fObtenerTodosIdiomas')
    def fObtenerTodosIdiomas( self, ):
   
        unaColeccion = self.fObtenerColeccionIdiomas()
        if not unaColeccion:
            return []
        
        unosElementos= unaColeccion.objectValues ( cNombreTipoTRAIdioma)  #
        return unosElementos
           
     


        

    security.declarePrivate( 'fObtenerTodosIdiomasOrdenados')
    def fObtenerTodosIdiomasOrdenados( self, ):
   
        unosIdiomas = self.fObtenerTodosIdiomas()
        unosCodigosEIdiomasAOrdenar = [ [ unIdioma.getCodigoIdiomaEnGvSIG(), unIdioma, ] for unIdioma in unosIdiomas ]
        
        unosCodigosEIdiomasOrdenados = sorted ( unosCodigosEIdiomasAOrdenar, lambda unCeI, otroCeI: cmp( unCeI[ 0], otroCeI[ 0]))
        unosIdiomasOrdenados = [ unCeI[ 1] for unCeI in unosCodigosEIdiomasOrdenados]
        return unosIdiomasOrdenados
           
     
    
    
    
    
         
        

    security.declareProtected( permissions.View, 'fTodosIdiomasVocabulary')
    def fTodosIdiomasVocabulary(self,):
        
        unDisplayList = DisplayList()
        
        unosCodigosYDisplayNames = self.fTodosIdiomasCodesAndDisplayNames()
        if not unosCodigosYDisplayNames:
            return unDisplayList
        
        for unCodigoIdioma, unDisplayName in unosCodigosYDisplayNames:
            unDisplayList.add( 
                unCodigoIdioma,
                unDisplayName,
                
            )      
        return unDisplayList
    
         
    

    
    security.declareProtected( permissions.View, 'fTodosIdiomasCodesAndDisplayNames')
    def fTodosIdiomasCodesAndDisplayNames(self,):
        
        unosCodesAndDisplayNames = []
        
        unosIdiomas = self.fObtenerTodosIdiomasOrdenados()
        if not unosIdiomas:
            return unosCodesAndDisplayNames
        
        for unIdioma in unosIdiomas:
            unosCodesAndDisplayNames.append( [ 
                self.fAsUnicode( unIdioma.getCodigoIdiomaEnGvSIG()),
                unIdioma.fDisplayTitleAsUnicode(),
            ])      
        return unosCodesAndDisplayNames
    
         
       
    security.declareProtected( permissions.View, 'fKnownIdiomaCodeAndNames')
    def fKnownIdiomaCodeAndNames(self, theCodigoIdioma):
        
        if not theCodigoIdioma:
            return []
         
        unosLanguagesNamesAndFlagsPorCodigo = self.fLanguagesNamesAndFlagsPorCodigo()
        unosNamesAndFlagForLanguage = unosLanguagesNamesAndFlagsPorCodigo.get( theCodigoIdioma, None)
        if not unosNamesAndFlagForLanguage:
            return []
         
 
        unNombreInglesDeIdioma = unosNamesAndFlagForLanguage.get( 'english', theCodigoIdioma)
        unNombreNativoDeIdioma = unosNamesAndFlagForLanguage.get( 'native', unNombreInglesDeIdioma)
        if not unNombreInglesDeIdioma:
            return []
        
        unCodeAndNames = [ 
            self.fAsUnicode( theCodigoIdioma),
            self.fAsUnicode( unNombreInglesDeIdioma), 
            self.fAsUnicode( unNombreNativoDeIdioma),
        ]
    
        return unCodeAndNames
   
     
  
    security.declareProtected( permissions.View, 'fKnownIdiomaCodeAndDisplayName')
    def fKnownIdiomaCodeAndDisplayName(self, theCodigoIdioma):
 
        unCodeAndNames = self.fKnownIdiomaCodeAndNames( theCodigoIdioma)
        if not unCodeAndNames:
            return []
        
        unCodeAndDisplayName =  [ 
            self.fAsUnicode( theCodigoIdioma),
            u'[%s] %s (%s)' % ( self.fAsUnicode( unCodeAndNames[ 0]),self.fAsUnicode( unCodeAndNames[ 1]), self.fAsUnicode( unCodeAndNames[ 2]), ),
        ]
    
        return unCodeAndDisplayName
  
    
    security.declareProtected( permissions.View, 'fKnownIdiomasCodesAndNames')
    def fKnownIdiomasCodesAndNames(self,):
 
        unosCodesAndNames = []
        
        unosLanguagesNamesAndFlagsPorCodigo = self.fLanguagesNamesAndFlagsPorCodigo()
        unosCodigosIdioma = sorted( unosLanguagesNamesAndFlagsPorCodigo.keys())

        for unCodigoIdioma in unosCodigosIdioma:
            unosDatosIdioma = unosLanguagesNamesAndFlagsPorCodigo.get( unCodigoIdioma, {})
            if unosDatosIdioma:
                unNombreInglesDeIdioma = unosDatosIdioma.get( 'english', unCodigoIdioma)
                unNombreNativoDeIdioma = unosDatosIdioma.get( 'native', unNombreInglesDeIdioma)
                if unNombreInglesDeIdioma:
                    unosCodesAndNames.append( [ 
                        self.fAsUnicode( unCodigoIdioma),
                        self.fAsUnicode( unNombreInglesDeIdioma), 
                        self.fAsUnicode( unNombreNativoDeIdioma),
                    ])
    
        return unosCodesAndNames
   
    
    
    security.declareProtected( permissions.View, 'fKnownIdiomasCodesAndDisplayNames')
    def fKnownIdiomasCodesAndDisplayNames(self,):
 
        unosCodesAndNames = self.fKnownIdiomasCodesAndNames()
        
        unosCodesAndDisplayNames = []
        
        for unCodigoIdioma, unNombreInglesDeIdioma, unNombreNativoDeIdioma in unosCodesAndNames:
            if unCodigoIdioma and unNombreInglesDeIdioma:
                unosCodesAndDisplayNames.append( [ 
                    self.fAsUnicode( unCodigoIdioma),
                    u'[%s] %s (%s)' % ( self.fAsUnicode( unCodigoIdioma),self.fAsUnicode( unNombreInglesDeIdioma), self.fAsUnicode( unNombreNativoDeIdioma), ),
                ])
    
        return unosCodesAndDisplayNames
   
    
    
        
    
    security.declareProtected( permissions.View, 'fNonExistingKnownIdiomasCodesAndNames')
    def fNonExistingKnownIdiomasCodesAndNames(self,):
        
        unosCodesAndNames = self.fKnownIdiomasCodesAndNames()

        if not unosCodesAndNames:
            return []
        
        unosIdiomas = self.fObtenerTodosIdiomas()
        unosCodigosIdioma = [ unIdioma.getCodigoIdiomaEnGvSIG() for unIdioma in unosIdiomas]
        
        unosNonExistingCodesAndNames = [ [ unCodigoIdioma, unNombreInglesDeIdioma, unNombreNativoDeIdioma] for unCodigoIdioma, unNombreInglesDeIdioma, unNombreNativoDeIdioma in unosCodesAndNames if not ( unCodigoIdioma in unosCodigosIdioma)]
        unosSortedNonExistingCodesAndNames = sorted ( unosNonExistingCodesAndNames, lambda unCeDN, otroCeDN: cmp( unCeDN[ 0], otroCeDN[ 0]))
        return unosSortedNonExistingCodesAndNames
        
    
          
      
    
    security.declareProtected( permissions.View, 'fNonExistingKnownIdiomasCodesAndDisplayNames')
    def fNonExistingKnownIdiomasCodesAndDisplayNames(self,):
 
        unosCodesAndNames = self.fNonExistingKnownIdiomasCodesAndNames()
        
        unosCodesAndDisplayNames = []
        
        for unCodigoIdioma, unNombreInglesDeIdioma, unNombreNativoDeIdioma in unosCodesAndNames:
            if unCodigoIdioma and unNombreInglesDeIdioma:
                unosCodesAndDisplayNames.append( [ 
                    self.fAsUnicode( unCodigoIdioma),
                    u'[%s] %s (%s)' % ( self.fAsUnicode( unCodigoIdioma),self.fAsUnicode( unNombreInglesDeIdioma), self.fAsUnicode( unNombreNativoDeIdioma), ),
                ])
    
        return unosCodesAndDisplayNames
     
    
    security.declareProtected( permissions.View, 'fGetIdiomaPorCodigo')
    def fGetIdiomaPorCodigo( self, theCodigoIdioma, thePloneUtilsTool=None):
        
        if not theCodigoIdioma:
            return None    

        unaIdIdioma = self.fIdiomaIdDesdeCodigo( theCodigoIdioma, thePloneUtilsTool)
        if not unaIdIdioma:
            return None    
        
        unIdioma = self.fGetIdiomaPorId( unaIdIdioma)
        return unIdioma


    
    
    security.declarePrivate( 'fIdiomaIdDesdeCodigo')
    def fIdiomaIdDesdeCodigo( self, theCodigoIdioma, thePloneUtilsTool=None):
        
        if not theCodigoIdioma:
            return None    

        unaIdIdioma = theCodigoIdioma.lower()
        unaIdIdioma.replace(" ", "-")
        unaIdIdioma.replace(".", "-")
        unaIdIdioma.replace("/", "-")
        unaIdIdioma.replace("\\", "-")
        unaIdIdioma ='%s%s' % ( cIdiomaIdPrefix, unaIdIdioma)
        
        aPloneUtilsTool = thePloneUtilsTool
        if not aPloneUtilsTool:
            aPloneUtilsTool = self.getPloneUtilsToolForNormalizeString()                
        if aPloneUtilsTool:
            unaIdIdioma = aPloneUtilsTool.normalizeString( unaIdIdioma)
            if not aPloneUtilsTool.good_id( unaIdIdioma):
                someBadChars = aPloneUtilsTool.bad_chars( unaIdIdioma)
                for aChar in someBadChars:
                    unaIdIdioma = unaIdIdioma.replace( aChar, '-')
        
        return unaIdIdioma

     
    
    
    
       
    security.declareProtected( permissions.View, 'fGetIdiomaPorId')    
    def fGetIdiomaPorId(self, theID):

        if not theID:
            return None

        unaColeccion = self.fObtenerColeccionIdiomas( )
        if not unaColeccion:
            return None
        
        unIdioma = None
        try:
            unIdioma = unaColeccion[ theID]
        except:
            None
        return unIdioma    
   
    
    
    
    
    
    
    
        
    # ####################################
    """TRAModulo accessors
    
    """


    
    security.declareProtected( permissions.View, 'fObtenerColeccionModulos')
    def fObtenerColeccionModulos( self, ):
   
        unasColecciones = self.objectValues( cNombreTipoTRAColeccionModulos) #
        if not unasColecciones:
            return None
        return unasColecciones[ 0]
         
    
        

    security.declareProtected( permissions.View, 'fObtenerTodosModulos')
    def fObtenerTodosModulos( self, ):
   
        unaColeccion = self.fObtenerColeccionModulos()
        if not unaColeccion:
            return []
        
        unosElementos= unaColeccion.objectValues ( cNombreTipoTRAModulo) #
        return unosElementos
           
     


       
    
    security.declareProtected( permissions.View, 'fGetModuloPorNombre')
    def fGetModuloPorNombre( self, theNombreModulo, thePloneUtilsTool=None):
        
        if not theNombreModulo:
            return None    

        unaIdModulo = self.fModuloIdDesdeNombre( theNombreModulo, thePloneUtilsTool)
        if not unaIdModulo:
            return None    
        
        unModulo = self.fGetModuloPorId( unaIdModulo)
        return unModulo


    
    
    security.declarePrivate( 'fModuloIdDesdeNombre')
    def fModuloIdDesdeNombre( self, theNombreModulo, thePloneUtilsTool=None):
        
        if not theNombreModulo:
            return None    

        unaIdModulo = theNombreModulo.lower()
        unaIdModulo.replace(" ", "-")
        unaIdModulo.replace(".", "-")
        unaIdModulo.replace("/", "-")
        unaIdModulo.replace("\\", "-")
        unaIdModulo ='%s%s' % ( cModuloIdPrefix, unaIdModulo)
        
        aPloneUtilsTool = thePloneUtilsTool
        if not aPloneUtilsTool:
            aPloneUtilsTool = self.getPloneUtilsToolForNormalizeString()     
            
        if aPloneUtilsTool:
            unaIdModulo = aPloneUtilsTool.normalizeString( unaIdModulo)
            if not aPloneUtilsTool.good_id( unaIdModulo):
                someBadChars = aPloneUtilsTool.bad_chars( unaIdModulo)
                for aChar in someBadChars:
                    unaIdModulo = unaIdModulo.replace( aChar, '-')
        
        return unaIdModulo

    
    
        

    security.declareProtected( permissions.View, 'fGetModuloPorId')
    def fGetModuloPorId( self, theModuloId):

        if not theModuloId:
            return None    

        unaColeccionModulos = self.fObtenerColeccionModulos()
        if not unaColeccionModulos:
            return None
        
        unModulo = None
        try:
            unModulo = unaColeccionModulos[ theModuloId] 
        except:
            None
        return unModulo
  

    
    
    
    
    
    
    
    
    
    
        
    # ####################################
    """TRACadena accessors
    
    """

        
    security.declareProtected( permissions.View, 'fObtenerColeccionCadenas')
    def fObtenerColeccionCadenas( self, ):
   
        unasColecciones = self.objectValues( cNombreTipoTRAColeccionCadenas) #
        if not unasColecciones:
            return None
        return unasColecciones[ 0]
         
    
    
    
    
    
    
    
    
    # ACV 200904121052 not used 
    # and it is better not to use it,
    # as it may fetch from DB thousands of TRACadenas
    #
    #security.declareProtected( permissions.View, 'fObtenerTodasCadenas')
    #def fObtenerTodasCadenas( self, ):
   
        #unaColeccion = self.fObtenerColeccionCadenas()
        #if ( unaColeccion == None):
            #return []
        
        #unosElementos = unaColeccion.objectValues ( cNombreTipoTRACadena) #
        #return unosElementos
           
        
    
    #security.declareProtected( permissions.View, 'fObtenerTodasCadenasIncluyendoInactivas')    
    #def fObtenerTodasCadenasIncluyendoInactivas(self):
        #return self.fObtenerTodasCadenas( )
        
    
    
    #security.declareProtected( permissions.View, 'fObtenerTodasCadenasActivas')    
    #def fObtenerTodasCadenasActivas(self):
        #return [ unaCadena for unaCadena in self.fObtenerTodasCadenasIncluyendoInactivas() if unaCadena.getEstadoCadena() == cEstadoCadenaActiva]
        
            

    
    
    security.declareProtected( permissions.View, 'fObtenerSimbolosTodasCadenasSinOrdenar')    
    def fObtenerSimbolosTodasCadenasSinOrdenar(self):
        unCatalog = self.fCatalogBusquedaCadenas()
        if not unCatalog:
            return []
        unaBusqueda = { 
            'getEstadoCadena': cEstadoCadenaActiva,
        }
        unosResultadosBusqueda = unCatalog.searchResults( **unaBusqueda)
        unosSimbolos = [ unResultado[ 'getSimbolo'] for unResultado in unosResultadosBusqueda]
        return unosSimbolos 
    


    security.declareProtected( permissions.View, 'fObtenerNumeroCadenas')    
    def fObtenerNumeroCadenas( self):
        unCatalog = self.fCatalogBusquedaCadenas()
        if not unCatalog:
            return 0
        unaBusqueda = { 
            'getEstadoCadena': cEstadoCadenaActiva,
        }
        unosResultadosBusqueda = unCatalog.searchResults( **unaBusqueda)
        return len( unosResultadosBusqueda)
     
    
    
        
    # ACV 20090404 was not used at the moment by anybody, 
    # but has been rewriten to use catalog search and avoid retrieving the collection contents    
    #security.declareProtected( permissions.View, 'getCadenaPorID')    
    #def getCadenaPorID(self, theID):
        #if not theID:
            #return None
        #unaColeccion = self.fObtenerColeccionCadenas()
        #unaCadena = None
        #try:
            #unaCadena = unaColeccion[ theID]
        #except:
            #None
        #return unaCadena    
            
    
        
        
    
    security.declareProtected( permissions.View, 'getCadenaPorID')    
    def getCadenaPorID(self, theID):
        if not theID:
            return None                   

        unCatalog = self.fCatalogBusquedaCadenas() 
        if not unCatalog:
            return None
        unaBusqueda = { 
            'getId' :      theID,
        }
            
        unosResultadosBusqueda = unCatalog.searchResults(**unaBusqueda)
        if len( unosResultadosBusqueda) < 1:
            return None

        unaCadena = unosResultadosBusqueda[ 0].getObject() 
        return unaCadena

    
    
        
    security.declareProtected( permissions.View, 'fGetCadenaPorSimbolo')    
    def fGetCadenaPorSimbolo(self, theSimboloCadena):
        if not theSimboloCadena:
            return None                   

        unCatalog = self.fCatalogBusquedaCadenas() 
        if not unCatalog:
            return None
        unaBusqueda = { 
            'getSimbolo' :      theSimboloCadena,
            'getEstadoCadena':  cEstadoCadenaActiva
        }
            
        unosResultadosBusqueda = unCatalog.searchResults(**unaBusqueda)
        if len( unosResultadosBusqueda) < 1:
            return None

        unaCadena = unosResultadosBusqueda[ 0].getObject() 
        return unaCadena
        
        
        
    
            
    security.declarePrivate( 'getHighestCadenaIdNumber')    
    def getHighestCadenaIdNumber( self):
        
        unCatalog = self.fCatalogBusquedaCadenas() 
        if not unCatalog:
            return 0
        unaBusqueda = {}
        unosResultadosBusqueda = unCatalog.searchResults(**unaBusqueda)
        if len( unosResultadosBusqueda) < 1:
            return 0
            
        unMaxIdNumber = 0
        for unResultadoBusqueda in unosResultadosBusqueda:
            unaId = unResultadoBusqueda.id
            if unaId.startswith( cCadenaIdPrefix):
                unNumberString = unaId[ len( cCadenaIdPrefix):]
                if len( unNumberString) > 0:
                    unNumber = 0
                    try:
                        unNumber = int( unNumberString)
                    except ValueError:
                        None
                    
                    if unNumber > unMaxIdNumber:
                        unMaxIdNumber = unNumber
        
        return unMaxIdNumber                        
    
 
    
    
    
    
    
    
    
    
    
    
        
    # ####################################
    """TRATraduccion accessors
    
    """

        
                     

    security.declareProtected( permissions.View, 'fObtenerDatosTodasTraduccionesAIdioma')    
    def fObtenerDatosTodasTraduccionesAIdioma(self, theCodigoIdioma):
        if not theCodigoIdioma:
            return []
        
        unIdioma = self.fGetIdiomaPorCodigo( theCodigoIdioma)
        if not unIdioma:
            return []
        aCatalog = self.fCatalogFiltroTraduccionesParaIdioma( unIdioma) 
        unaBusqueda = {}
        unosResultadosBusquedaTraducciones      = aCatalog.searchResults(**unaBusqueda)
        return unosResultadosBusquedaTraducciones    
      
  
    
   
    
    
    
    
    
    
    
    
           
    # ####################################
    """TRAInforme accessors
    
    """


     
    security.declareProtected( permissions.View, 'fObtenerColeccionInformes')
    def fObtenerColeccionInformes( self, ):
   
        unasColecciones = self.objectValues( cNombreTipoTRAColeccionInformes) #
        if not unasColecciones:
            return None
        return unasColecciones[ 0]
    
        

    security.declareProtected( permissions.View, 'fObtenerTodosInformes')
    def fObtenerTodosInformes( self, ):
   
        unaColeccion = self.fObtenerColeccionInformes()
        if not unaColeccion:
            return []
        
        unosElementos = unaColeccion.objectValues ( cNombreTipoTRAInforme) #
        return unosElementos
           
     
    
    
    
    
    
    
    
    
    
    
           
    # ####################################
    """TRAImportacion accessors
    
    """


     
    security.declareProtected( permissions.View, 'fObtenerColeccionImportaciones')
    def fObtenerColeccionImportaciones( self, ):
   
        unasColecciones = self.objectValues( cNombreTipoTRAColeccionImportaciones) #
        if not unasColecciones:
            return None
        return unasColecciones[ 0]
    
        

    security.declareProtected( permissions.View, 'fObtenerTodasImportaciones')
    def fObtenerTodasImportaciones( self, ):
   
        unaColeccion = self.fObtenerColeccionImportaciones()
        if not unaColeccion:
            return []
        
        unosElementos = unaColeccion.objectValues ( cNombreTipoTRAImportacion) #
        return unosElementos
           
     
    
        
    
    
    
    
    
    

    

    
    
    
    
    
    
    
    
    
    
     
    # ################################################################
    """Private Factories
    
    """
           
    security.declarePrivate( 'fCrearIdioma')
    def fCrearIdioma( self, 
        theUseCaseQueryResult, 
        theCodigoIdiomaEnGvSIG, 
        theCodigoInternacionalDeIdioma='', 
        theTitle='', 
        theNombreInglesIdioma='', 
        theNombreNativoIdioma='',
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):
        """TRAIdioma private factory method that does not check security constraints, that must have laready been checked by caller.
        
        """
        unExecutionRecord = self.fStartExecution( 'method',  'fCrearIdioma', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }, 'codigo_idioma: %s' % ( theCodigoIdiomaEnGvSIG or 'unknown')) 
        
        try:
        
            if not theUseCaseQueryResult or not theUseCaseQueryResult.get( 'success', False):
                return None    
            
            if not theCodigoIdiomaEnGvSIG:
                return None    
    
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
            unaIdIdioma         = self.fIdiomaIdDesdeCodigo( theCodigoIdiomaEnGvSIG)
            unIdiomaEncontrado  = self.fGetIdiomaPorId( unaIdIdioma)
    
            if unIdiomaEncontrado:
                return unIdiomaEncontrado
                            
            unaColeccionIdiomas = self.fObtenerColeccionIdiomas() 
            if not unaColeccionIdiomas:
                return None
            
            unosCodigosIdioma = [ unIdioma.getCodigoIdiomaEnGvSIG() for unIdioma in unaColeccionIdiomas.objectValues()]
            if theCodigoIdiomaEnGvSIG in unosCodigosIdioma:
                return None
    
            unTitle              = theTitle              
            unNombreInglesIdioma = theNombreInglesIdioma 
            unNombreNativoIdioma = theNombreNativoIdioma
            
            if not unTitle or not unNombreInglesIdioma or not unNombreNativoIdioma:
                unosIntlLanguagesNamesAndFlagsPorCodigo = self.fLanguagesNamesAndFlagsPorCodigo()
                
                unosIntlDatosIdioma     = unosIntlLanguagesNamesAndFlagsPorCodigo.get( theCodigoIdiomaEnGvSIG, {})
                if unosIntlDatosIdioma:
                    unNombreEnglishIdioma   = unosIntlDatosIdioma.get( 'english', '')
                    unNombreNativoIdioma    = unosIntlDatosIdioma.get( 'native', '')
            
    
            unCodigoInternacionalDeIdioma = theCodigoInternacionalDeIdioma
            if not unCodigoInternacionalDeIdioma:
                unCodigoInternacionalDeIdioma = theCodigoIdiomaEnGvSIG
            unNombreInglesIdioma = unNombreInglesIdioma or theCodigoIdiomaEnGvSIG
            unNombreNativoIdioma = unNombreNativoIdioma or unNombreInglesIdioma
            unTitle              = unTitle              or unNombreInglesIdioma
                    
            
            
            aNewIdiomaAttrsDict = { 
                'codigoIdiomaEnGvSIG':          theCodigoIdiomaEnGvSIG,
                'codigoInternacionalDeIdioma':  theCodigoInternacionalDeIdioma,
                'title':                        unTitle,
                'nombreNativoDeIdioma':         unNombreNativoIdioma,
            }
            
            unaIdNuevoIdioma = unaColeccionIdiomas.invokeFactory( cNombreTipoTRAIdioma,  unaIdIdioma, **aNewIdiomaAttrsDict)
            if not unaIdNuevoIdioma:
                return None
            unNuevoIdioma = unaColeccionIdiomas.getElementoPorID( unaIdNuevoIdioma)
            if not unNuevoIdioma:
                return None
            
            unNuevoIdioma.manage_fixupOwnershipAfterAdd()
           
            unNuevoIdioma.pSetPermissions()
            
            self.fLazyCrearCatalogsEIndicesParaIdioma( 
                theAllowCreation        = True, 
                theIdioma               = unNuevoIdioma,  
                theCheckPermissions     = False, 
                thePermissionsCache     = unPermissionsCache, 
                theRolesCache           = unRolesCache, 
                theParentExecutionRecord= unExecutionRecord
            )
    
            self.fLazyCrearUserGroupsParaIdioma(
                theAllowCreation        = True, 
                theIdioma               = unNuevoIdioma,  
                theCheckPermissions     = False, 
                thePermissionsCache     = unPermissionsCache, 
                theRolesCache           = unRolesCache, 
                theParentExecutionRecord= unExecutionRecord
            )
                         
            
            unIndexIdiomaAnterior = -1
            for unIndexIdioma in range( len( unosCodigosIdioma)):
                unCodigoIdioma = unosCodigosIdioma[ unIndexIdioma]
                if unCodigoIdioma < theCodigoIdiomaEnGvSIG:
                    unIndexIdiomaAnterior = unIndexIdioma    
                else:
                    break
                
            if unIndexIdiomaAnterior < 0:
                unaColeccionIdiomas.moveObjectsToTop( [ unaIdNuevoIdioma,])
            elif unIndexIdiomaAnterior < len( unosCodigosIdioma):
                unDelta = (unIndexIdiomaAnterior + 1) - len( unosCodigosIdioma) 
                unaColeccionIdiomas.moveObjectsByDelta( [ unaIdNuevoIdioma,], unDelta)
                
            return unNuevoIdioma
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
           
        


 


  
  
  



    security.declarePrivate(  'fCrearModulo')
    def fCrearModulo( self, 
        theUseCaseQueryResult,                       
        theNombreModulo,
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):
        """TRAModulo private factory method that does not check security constraints, that must have laready been checked by caller.
        
        """
        unExecutionRecord = self.fStartExecution( 'method',  'fCrearModulo', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }, 'nombre_modulo: %s' % ( theNombreModulo or 'unknown')) 
        
        try:
        

            if not theUseCaseQueryResult or not theUseCaseQueryResult.get( 'success', False):
                return None    
            
            if not theNombreModulo:
                return None    
            
            unModulo = self.fGetModuloPorNombre( theNombreModulo)
            if unModulo:
                return unModulo
            
            unaColeccionModulos = self.fObtenerColeccionModulos()
            
            unosNombresModulo = [ unModulo.Title() for unModulo in unaColeccionModulos.objectValues()]
            if theNombreModulo in unosNombresModulo:
                return None
      
            unaIdModulo = self.fModuloIdDesdeNombre( theNombreModulo)
            
            aNewModuloAttrsDict = { 
                'title': theNombreModulo,
            }
            
            unaIdNuevoModulo = unaColeccionModulos.invokeFactory( cNombreTipoTRAModulo, unaIdModulo, **aNewModuloAttrsDict)
            if not unaIdNuevoModulo:
                return None
                     
            unNuevoModulo = unaColeccionModulos.getElementoPorID( unaIdNuevoModulo)
            if not unNuevoModulo:
                return None
            
            unNuevoModulo.manage_fixupOwnershipAfterAdd()
          
            unNuevoModulo.pSetPermissions()
           
            # self.fLazyCrearUserGroupsParaModulo(       unNuevoModulo, False)

            
            
           
            unIndexModuloAnterior = -1
            for unIndexModulo in range( len( unosNombresModulo)):
                unNombreModulo = unosNombresModulo[ unIndexModulo]
                if unNombreModulo < theNombreModulo:
                    unIndexModuloAnterior = unIndexModulo    
                else:
                    break
                
            if unIndexModuloAnterior < 0:
                unaColeccionModulos.moveObjectsToTop( [ unaIdNuevoModulo,])
            elif unIndexModuloAnterior < len( unosNombresModulo):
                unDelta = (unIndexModuloAnterior + 1) - len( unosNombresModulo) 
                unaColeccionModulos.moveObjectsByDelta( [ unaIdNuevoModulo,], unDelta)
                
            
            return unNuevoModulo
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
           
        
     
 
    
    
    
    
    
    
    
    
    
    
    
    
    # ################################################################
    """Translation state change methods.
    
    """

     
        
    security.declarePrivate( 'fIntentarTraducirCadena')    
    def fIntentarTraducirCadena( self, 
        theSimboloCadena, 
        theCodigoIdioma, 
        theCadenaTraducida, 
        theComentario, 
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):
        """Service exposed to UI Set the string translation and change the state from pending to translated and comment to the supplied values. 

        Delegate in the TRACadena found by its symbol
        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fIntentarTraducirCadena', theParentExecutionRecord, False) 
    
        try:
            if  not theSimboloCadena or not theCodigoIdioma:
                return self.fNewVoidChangeTranslationResult()
                            
            unIdioma = self.fGetIdiomaPorCodigo(  theCodigoIdioma)
            if not unIdioma:
                return self.fNewVoidChangeTranslationResult()

            unaCadena = self.fGetCadenaPorSimbolo( theSimboloCadena)
            if not unaCadena:
                return self.fNewVoidChangeTranslationResult()
            
            unResultado = unaCadena.fIntentarTraducirTraduccion( 
                unIdioma, 
                theCadenaTraducida, 
                theComentario, 
                theRegistrarHistoria    = True, 
                thePermissionsCache     =thePermissionsCache, 
                theRolesCache           =theRolesCache, 
                theParentExecutionRecord=unExecutionRecord
            )
                
            return unResultado
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            
           

            
        
       
    security.declarePrivate( 'fComentarTraduccionCadena')    
    def fComentarTraduccionCadena( self, 
        theSimboloCadena, 
        theCodigoIdioma, 
        theComentario, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fComentarTraduccionCadena', theParentExecutionRecord, False) 
    
        try:
            if  not theSimboloCadena or not theCodigoIdioma:
                return self.fNewVoidChangeTranslationResult()
            
            unIdioma = self.fGetIdiomaPorCodigo(  theCodigoIdioma)
            if not unIdioma:
                return self.fNewVoidChangeTranslationResult()

            unaCadena = self.fGetCadenaPorSimbolo( theSimboloCadena)
            if not unaCadena:
                return self.fNewVoidChangeTranslationResult()
    
            unResultado = unaCadena.fComentarTraduccion( 
                unIdioma, 
                theComentario, 
                thePermissionsCache     =thePermissionsCache, 
                theRolesCache           =theRolesCache, 
                theParentExecutionRecord=unExecutionRecord
            )
                 
            return unResultado        
               
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            


         
        
        
        
        
    security.declarePrivate( 'fHacerPendienteTraduccionCadena')    
    def fHacerPendienteTraduccionCadena( self, 
        theSimboloCadena, 
        theCodigoIdioma, 
        theComentario, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord=None):

        unExecutionRecord = self.fStartExecution( 'method',  'fHacerPendienteTraduccionCadena', theParentExecutionRecord, False) 

        try:
            if  not theSimboloCadena or not theCodigoIdioma:
                return self.fNewVoidChangeTranslationResult()
                
            unIdioma = self.fGetIdiomaPorCodigo(  theCodigoIdioma)
            if not unIdioma:
                return self.fNewVoidChangeTranslationResult()

            unaCadena = self.fGetCadenaPorSimbolo( theSimboloCadena)
            if not unaCadena:
                return self.fNewVoidChangeTranslationResult()
                
            unResultado = unaCadena.fHacerPendienteTraduccion( 
                unIdioma, 
                theComentario, 
                thePermissionsCache     =thePermissionsCache, 
                theRolesCache           =theRolesCache, 
                theParentExecutionRecord=unExecutionRecord
            )
                 
            return unResultado        
       
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            
         
         
         
         
         

    security.declarePrivate( 'fHacerTraducidaTraduccionCadena')    
    def fHacerTraducidaTraduccionCadena( self, 
        theSimboloCadena, 
        theCodigoIdioma, 
        theComentario, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord=None):
 
        unExecutionRecord = self.fStartExecution( 'method',  'fHacerTraducidaTraduccionCadena', theParentExecutionRecord, False) 
        
        try:
            if  not theSimboloCadena or not theCodigoIdioma:
                return self.fNewVoidChangeTranslationResult()
                
            unIdioma = self.fGetIdiomaPorCodigo(  theCodigoIdioma)
            if not unIdioma:
                return self.fNewVoidChangeTranslationResult()

            unaCadena = self.fGetCadenaPorSimbolo( theSimboloCadena)
            if not unaCadena:
                return self.fNewVoidChangeTranslationResult()
                
            unResultado = unaCadena.fHacerTraducidaTraduccion( 
                unIdioma, 
                theComentario, 
                thePermissionsCache     =thePermissionsCache, 
                theRolesCache           =theRolesCache, 
                theParentExecutionRecord=unExecutionRecord
            )
                            
            return unResultado                 
       
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            
       
       
       
       
       


    security.declarePrivate( 'fHacerRevisadaTraduccionCadena')    
    def fHacerRevisadaTraduccionCadena( self, 
        theSimboloCadena, 
        theCodigoIdioma, 
        theComentario, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord=None):

        unExecutionRecord = self.fStartExecution( 'method',  'fHacerRevisadaTraduccionCadena', theParentExecutionRecord, False) 
        
        try:
            if  not theSimboloCadena or not theCodigoIdioma:
                return self.fNewVoidChangeTranslationResult()
                
            unIdioma = self.fGetIdiomaPorCodigo(  theCodigoIdioma)
            if not unIdioma:
                return self.fNewVoidChangeTranslationResult()

            unaCadena = self.fGetCadenaPorSimbolo( theSimboloCadena)
            if not unaCadena:
                return self.fNewVoidChangeTranslationResult()
                
            unResultado = unaCadena.fHacerRevisadaTraduccion( 
                unIdioma, 
                theComentario, 
                thePermissionsCache     =thePermissionsCache, 
                theRolesCache           =theRolesCache, 
                theParentExecutionRecord=unExecutionRecord
            )
            
            return unResultado        
       
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            
         






    security.declarePrivate( 'fHacerDefinitivaTraduccionCadena')    
    def fHacerDefinitivaTraduccionCadena( self, 
        theSimboloCadena, 
        theCodigoIdioma, 
        theComentario, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord=None):

        unExecutionRecord = self.fStartExecution( 'method',  'fHacerDefinitivaTraduccionCadena', theParentExecutionRecord, False) 
        
        try:
            if  not theSimboloCadena or not theCodigoIdioma:
                return self.fNewVoidChangeTranslationResult()
                
            unIdioma = self.fGetIdiomaPorCodigo(  theCodigoIdioma)
            if not unIdioma:
                return self.fNewVoidChangeTranslationResult()

            unaCadena = self.fGetCadenaPorSimbolo( theSimboloCadena)
            if not unaCadena:
                return self.fNewVoidChangeTranslationResult()
                
            unResultado = unaCadena.fHacerDefinitivaTraduccion(  
                unIdioma, 
                theComentario, 
                thePermissionsCache     =thePermissionsCache, 
                theRolesCache           =theRolesCache, 
                theParentExecutionRecord=unExecutionRecord
            )
                 
            return unResultado        
       
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            
  




    security.declarePrivate( 'fLoteCambiosEstadoTraduccionesCadenas')    
    def fLoteCambiosEstadoTraduccionesCadenas( self, 
        theBatchIds_Traducida, 
        theBatchIds_Revisada,
        theBatchIds_Definitiva,        
        theCodigoIdioma, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord=None):

        unExecutionRecord = self.fStartExecution( 'method',  'fLoteCambiosEstadoTraduccionesCadenas', theParentExecutionRecord, False) 
        
        try:
            if not theCodigoIdioma:
                return self.fNewVoidChangeTranslationResult()
                
            unIdioma = self.fGetIdiomaPorCodigo(  theCodigoIdioma)
            if not unIdioma:
                return self.fNewVoidChangeTranslationResult()
            
            unNumSucceeded = 0
            unNumChanged   = 0
            unNumFailed    = 0
            
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
             
            for unSimboloCadena in theBatchIds_Traducida:
                unaCadena = self.getCadenaPorID( unSimboloCadena)
                if unaCadena:
                    
                    unResultado = unaCadena.fHacerTraducidaTraduccion(  
                        unIdioma, 
                        '', 
                        thePermissionsCache     =unPermissionsCache, 
                        theRolesCache           =unRolesCache, 
                        theParentExecutionRecord=unExecutionRecord
                    )
                     
                    if unResultado.get( 'success', False):
                        unNumSucceeded += 1
                        if unResultado.get( 'changed', False):
                            unNumChanged += 1
                        
                    else:
                        unNumFailed += 1
                        
            for unSimboloCadena in theBatchIds_Revisada:
                unaCadena = self.getCadenaPorID( unSimboloCadena)
                if unaCadena:
                    
                    unResultado = unaCadena.fHacerRevisadaTraduccion(  
                        unIdioma, 
                        '', 
                        thePermissionsCache     =unPermissionsCache, 
                        theRolesCache           =unRolesCache, 
                        theParentExecutionRecord=unExecutionRecord
                    )
                     
                    if unResultado.get( 'success', False):
                        unNumSucceeded += 1
                        if unResultado.get( 'changed', False):
                            unNumChanged += 1
                        
                    else:
                        unNumFailed += 1
                        
            for unSimboloCadena in theBatchIds_Definitiva:
                unaCadena = self.getCadenaPorID( unSimboloCadena)
                if unaCadena:
                    
                    unResultado = unaCadena.fHacerDefinitivaTraduccion(  
                        unIdioma, 
                        '', 
                        thePermissionsCache     =unPermissionsCache, 
                        theRolesCache           =unRolesCache, 
                        theParentExecutionRecord=unExecutionRecord
                    )
                     
                    if unResultado.get( 'success', False):
                        unNumSucceeded += 1
                        if unResultado.get( 'changed', False):
                            unNumChanged += 1
                        
                    else:
                        unNumFailed += 1

            aChangesRequested = ( len( theBatchIds_Traducida) > 0) or ( len( theBatchIds_Revisada) > 0) or ( len( theBatchIds_Definitiva) > 0)
            unResultado =  self.fNewVoidChangeTranslationResult()
            unResultado.update({
                'success': ( not aChangesRequested) or ( unNumSucceeded > 0),
                'changed': unNumChanged > 0,
            })        
            
            return unResultado 
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            
   
            
              
            
        
        
    # #######################################
    """Derivation methods.
    
    """
                   
    
    
                        
    security.declarePrivate( 'fDeriveUltimaVersionImportada')    
    def fDeriveUltimaVersionImportada( self):
        unaUltimaImportacion = self.getUltimaImportacion()
        if not unaUltimaImportacion :
            return ''
        
        unaUltimaVersionImportada = unaUltimaImportacion.getVersionDelProducto()
        return unaUltimaVersionImportada
    
    
    
        
                        
    security.declarePrivate( 'fDeriveUltimoBuildImportado')    
    def fDeriveUltimoBuildImportado( self):
        unaUltimaImportacion = self.getUltimaImportacion()
        if not unaUltimaImportacion :
            return ''
        
        unaUltimoBuildImportado = unaUltimaImportacion.getBuildDelProducto()
        return unaUltimoBuildImportado
    
    
    
    
    security.declarePrivate( 'fDeriveFechaUltimoInforme')    
    def fDeriveFechaUltimoInforme( self):
        unUltimoInforme = self.getUltimoInforme()
        if not unUltimoInforme :
            return ''
        
        unaFechaUltimoInforme = unUltimoInforme.getFechaFinProceso()
        return unaFechaUltimoInforme
       
    
    
    security.declarePrivate( 'fDeriveFechaUltimaImportacion')    
    def fDeriveFechaUltimaImportacion( self):
        unaUltimaImportacion = self.getUltimaImportacion()
        if not unaUltimaImportacion :
            return ''
        
        unaFechaUltimaImportacion = unaUltimaImportacion.getFechaFinProceso()
        return unaFechaUltimaImportacion
       

    
    
    
    
         

    
    
        
    # #######################################################################
    #   Cached sorted simbolos cadenas
    #   and another cache grouped by module and also sorted by simbolo cadena
    #
    # #######################################################################

     

    security.declarePrivate( 'fListaSimbolosCadenasOrdenados')
    def fListaSimbolosCadenasOrdenados( self,theParentExecutionRecord=None):
        unTextoSimbolos = self.getSimbolosCadenasOrdenados().strip()
        if not unTextoSimbolos:
            self.pInicializarModulosYSimbolosCadenasOrdenados( theParentExecutionRecord)
            unTextoSimbolos = self.getSimbolosCadenasOrdenados().strip()
            
        unosSimbolos = unTextoSimbolos.splitlines()
        return unosSimbolos
        
        
    security.declarePrivate( 'fListaSimbolosCadenasOrdenadosEnModulo')
    def fListaSimbolosCadenasOrdenadosEnModulo( self, theNombreModulo,  theParentExecutionRecord=None):
        if not theNombreModulo:
            return self.fListaSimbolosCadenasOrdenados( theParentExecutionRecord)
        
        unTextoModulosYSimbolos = self.getModulosYSimbolosCadenasOrdenados()
        if not unTextoModulosYSimbolos:
            self.pInicializarModulosYSimbolosCadenasOrdenados(  theParentExecutionRecord)
            unTextoModulosYSimbolos = self.getModulosYSimbolosCadenasOrdenados()
            
        unosModulosYSimbolos = unTextoModulosYSimbolos.splitlines()
        unNumeroLineas = len( unosModulosYSimbolos)
        if not unNumeroLineas:
            return []        
        
        unIndexBusqueda = 0
        while unIndexBusqueda < unNumeroLineas:
            unIndexModuleStartLine = -1
            try:
                unIndexModuleStartLine = unosModulosYSimbolos.index( cModuleStartLine, unIndexBusqueda)
            except:
                return []
            if unIndexModuleStartLine < 0:
                return []
            if unIndexModuleStartLine >= ( unNumeroLineas - 2):
                return []
            unNombreModulo = unosModulosYSimbolos[ unIndexModuleStartLine + 1]            
            if unNombreModulo and ( unNombreModulo == theNombreModulo):
                unSiguienteIndexModuleStartLine = -1
                try:
                    unSiguienteIndexModuleStartLine = unosModulosYSimbolos.index( cModuleStartLine, unIndexModuleStartLine + 2)
                except:
                    None
                if unSiguienteIndexModuleStartLine < 0:
                    unosSimbolos = unosModulosYSimbolos[ unIndexModuleStartLine + 2:]
                    return unosSimbolos
                else:                
                    unosSimbolos = unosModulosYSimbolos[ unIndexModuleStartLine + 2:unSiguienteIndexModuleStartLine]
                    return unosSimbolos
            else:
                unIndexBusqueda = unIndexModuleStartLine + 2    

        return []
    
    
    
    
    
    
    
    security.declarePrivate( 'fListaSimbolosCadenasOrdenadosEnVariosModulos')
    def fListaSimbolosCadenasOrdenadosEnVariosModulos( self, theNombresModulos,  theIncludeModuloNoEspecificado, theParentExecutionRecord=None):
        if ( not theNombresModulos) and ( not theIncludeModuloNoEspecificado):
            return self.fListaSimbolosCadenasOrdenados( theParentExecutionRecord)
        
        if ( len( theNombresModulos) == 1) and ( not theIncludeModuloNoEspecificado):
            return self.fListaSimbolosCadenasOrdenadosEnModulo( theNombresModulos[ 0], theParentExecutionRecord)
        
        if not theNombresModulos:
            return self.fListaSimbolosCadenasOrdenadosModuloNoEspecificado( theParentExecutionRecord)
            
        unosNombresModulos = theNombresModulos[:]
        if theIncludeModuloNoEspecificado:
            unosNombresModulos.append( cNombreModuloNoEspecificadoSentinel)
            
        unosSimbolos = self.fListaSimbolosCadenasEnVariosModulos( unosNombresModulos,  theParentExecutionRecord)        

        unosSimbolosOrdenados = sorted( unosSimbolos)
        
        return unosSimbolos
    
   
    
    
    
    
    security.declarePrivate( 'fListaSimbolosCadenasEnVariosModulosStrictly')
    def fListaSimbolosCadenasEnVariosModulosStrictly( self, theNombresModulos,  theIncludeModuloNoEspecificado, theParentExecutionRecord=None):
        if ( not theNombresModulos) and ( not theIncludeModuloNoEspecificado):
            return []
        
        if ( len( theNombresModulos) == 1) and ( not theIncludeModuloNoEspecificado):
            return self.fListaSimbolosCadenasOrdenadosEnModulo( theNombresModulos[ 0], theParentExecutionRecord)
        
        if not theNombresModulos:
            return self.fListaSimbolosCadenasOrdenadosModuloNoEspecificado( theParentExecutionRecord)
        
        unosNombresModulos = theNombresModulos[:]
        if theIncludeModuloNoEspecificado:
            unosNombresModulos.append( cNombreModuloNoEspecificadoSentinel)
            
        unosSimbolos = self.fListaSimbolosCadenasEnVariosModulos( unosNombresModulos,  theParentExecutionRecord)  
        if not unosSimbolos:
            return []
        
        return list( unosSimbolos)
    
   
        
    
    
    security.declarePrivate( 'fListaSimbolosCadenasEnVariosModulos')
    def fListaSimbolosCadenasEnVariosModulos( self, theNombresModulos, theParentExecutionRecord=None):
        if not theNombresModulos:
            return self.fListaSimbolosCadenasOrdenados( theParentExecutionRecord)
        
        if len( theNombresModulos) == 1:
            return self.fListaSimbolosCadenasOrdenadosEnModulo( theNombresModulos[ 0], theParentExecutionRecord)
            
                
        unTextoModulosYSimbolos = self.getModulosYSimbolosCadenasOrdenados()
        if not unTextoModulosYSimbolos:
            
            self.pInicializarModulosYSimbolosCadenasOrdenados( theParentExecutionRecord)

            unTextoModulosYSimbolos = self.getModulosYSimbolosCadenasOrdenados()
            
        unosModulosYSimbolos = unTextoModulosYSimbolos.splitlines()
        unNumeroLineas = len( unosModulosYSimbolos)
        if not unNumeroLineas:
            return []
        
        todosSimbolos = set()
        
        for unNombreModulo in theNombresModulos:
            
            unIndexBusqueda = 0
            while unIndexBusqueda < unNumeroLineas:
                unIndexModuleStartLine = -1
                try:
                    unIndexModuleStartLine = unosModulosYSimbolos.index( cModuleStartLine, unIndexBusqueda)
                except:
                    break
                if unIndexModuleStartLine < 0:
                    break
                if unIndexModuleStartLine >= ( unNumeroLineas - 2):
                    break
                unNombreModuloHere = unosModulosYSimbolos[ unIndexModuleStartLine + 1]            
                if unNombreModuloHere and ( unNombreModuloHere == unNombreModulo):
                    unSiguienteIndexModuleStartLine = -1
                    try:
                        unSiguienteIndexModuleStartLine = unosModulosYSimbolos.index( cModuleStartLine, unIndexModuleStartLine + 2)
                    except:
                        None
                    if unSiguienteIndexModuleStartLine < 0:
                        todosSimbolos.update( unosModulosYSimbolos[ unIndexModuleStartLine + 2:])
                        break
                    else:                
                        todosSimbolos.update( unosModulosYSimbolos[ unIndexModuleStartLine + 2:unSiguienteIndexModuleStartLine])
                        break
                else:
                    unIndexBusqueda = unIndexModuleStartLine + 2    
        
        return todosSimbolos
    
    
    
    
    security.declarePrivate( 'fListaSimbolosCadenasOrdenadosModuloNoEspecificado')
    def fListaSimbolosCadenasOrdenadosModuloNoEspecificado( self,  theParentExecutionRecord=None):
        return self.fListaSimbolosCadenasOrdenadosEnModulo( cNombreModuloNoEspecificadoSentinel,  theParentExecutionRecord)
    

        
    security.declarePrivate( 'pInicializarModulosYSimbolosCadenasOrdenados')
    def pInicializarModulosYSimbolosCadenasOrdenados( self, theParentExecutionRecord=None):

        unExecutionRecord = self.fStartExecution( 'method',  'pInicializarModulosYSimbolosCadenasOrdenados', theParentExecutionRecord, False) 

        if cLogInicializarSimbolosCadenasOrdenados:
            unStartTime = self.fMillisecondsNow()
        
        try:
            unaBusqueda = cBusquedaTodasCadenasOrdenadasPorSimbolo.copy()

# ACV 20090814 
#   EATR01 Remove Attribute pathDelRaiz from all entities; 	
#   EATR02 Remove the Type attribute from catalog schemas
#            unaBusqueda[ 'getPathDelRaiz'] = self.getPathDelRaiz() 
            
            unCatalogFiltroCadenas = self.fCatalogFiltroCadenas()
            if not unCatalogFiltroCadenas:
                return self
            unosDatosCadenas = unCatalogFiltroCadenas.searchResults( **unaBusqueda ) 
            
            if not unosDatosCadenas or len( unosDatosCadenas) < 1:
                self.setSimbolosCadenasOrdenados( '')
                self.setModulosYSimbolosCadenasOrdenados( '')
                return self
            
            
            unosSimbolosCadenasOrdenadosString  = '\n'.join( [ unosDatosCadena[ 'getSimbolo'] for unosDatosCadena in unosDatosCadenas ])
            self.setSimbolosCadenasOrdenados( unosSimbolosCadenasOrdenadosString)
            
            unosModulosYSimbolosDict         = {}
            unosSimbolosModuloNoEspecificado = []

            for unosDatosCadena in unosDatosCadenas:
                unSimbolo =  unosDatosCadena[ 'getSimbolo']
                
                # ACV 200904101658 not used
                # furthermore, it is causing fault of object, and poosibly its container collection: removed
                # unaCadena = unosDatosCadena.getObject()
                unosNombresModulosString = unosDatosCadena[ 'getNombresModulos']
                unosNombresModulosString = unosNombresModulosString.strip()
                if unosNombresModulosString:
                    unosNombresModulos = unosNombresModulosString.splitlines()
                    if unosNombresModulos:
                        for unNombreModulo in unosNombresModulos:
                            unosSimbolosModulo = unosModulosYSimbolosDict.get( unNombreModulo, None)
                            if not unosSimbolosModulo:
                                unosModulosYSimbolosDict[ unNombreModulo] = [ unSimbolo,]
                            else:
                                unosSimbolosModulo.append( unSimbolo)
                else:
                    unosSimbolosModuloNoEspecificado.append( unSimbolo)
    
            todosNombresModulos = unosModulosYSimbolosDict.keys()
            todosNombresModulosOrdenados = sorted( todosNombresModulos)
            
            anOutput = StringIO()

            if unosSimbolosModuloNoEspecificado:
                anOutput.write( '%s\n%s\n%s\n' % ( cModuleStartLine, cNombreModuloNoEspecificadoSentinel, '\n'.join( unosSimbolosModuloNoEspecificado), ))
            else:
                anOutput.write( '%s\n%s\n' % ( cModuleStartLine, cNombreModuloNoEspecificadoSentinel, ))
            
            for unNombreModulo in todosNombresModulosOrdenados:
                unosSimbolosModulo = unosModulosYSimbolosDict[ unNombreModulo]
                if unosSimbolosModulo:
                    anOutput.write( '%s\n%s\n%s\n' % ( cModuleStartLine, unNombreModulo, '\n'.join( unosSimbolosModulo), ))
                else:
                    anOutput.write( '%s\n%s\n' % ( cModuleStartLine, unNombreModulo,  ))
                    
                
            unosModulosYSimbolosCadenasOrdenadosString  = anOutput.getvalue()
            self.setModulosYSimbolosCadenasOrdenados( unosModulosYSimbolosCadenasOrdenadosString)

        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

            if cLogInicializarSimbolosCadenasOrdenados:
                unEndTime = self.fMillisecondsNow()
                logging.getLogger( 'gvSIGi18n').info( 'pInicializarModulosYSimbolosCadenasOrdenados::TOTAL milliseconds=%d' % ( unEndTime - unStartTime))
        
        
        return self
            
    
        
        
        
    
    
    security.declareProtected( permissions.ModifyPortalContent, 'pInvalidateSimbolosCadenasOrdenados')    
    def pInvalidateSimbolosCadenasOrdenados( self):
        unTextoSimbolos = self.getSimbolosCadenasOrdenados().strip()
        if unTextoSimbolos:
            self.setSimbolosCadenasOrdenados( '')

        unTextoModulosYSimbolos = self.getModulosYSimbolosCadenasOrdenados().strip()
        if unTextoSimbolos:
            self.setModulosYSimbolosCadenasOrdenados( '')
        return self
            
    
    
    

    


 
    
    
    
      
# #############################################################
# Catalog accessors
#
# #############################################################
    
   
         
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

     
        
   
        
   

    
    
    
    
    
    
    
    
         
        
        
        
# ################################
#  Only used when migrating version that derived traduccion field from cadena
#  to the new implementation where traducciones hold storage for those values
    
    #security.declareProtected( permissions.ModifyPortalContent,  'pInitTraduccionesPreviouslyComputedFields')    
    #def pInitTraduccionesPreviouslyComputedFields( self):
        
 
        #unPathDelRaiz = self.fPathDelRaiz()
        
        #unCatalogBusquedaTraducciones = self.fCatalogBusquedaTraducciones()   
        #unaBusqueda = { 
            #'Type' :                   'Traduccion', 
        #}      
        #unosResultadosBusquedaTraducciones      = unCatalogBusquedaTraducciones.searchResults(**unaBusqueda)
        #for unResultadoTraduccion in unosResultadosBusquedaTraducciones:
            #unaTraduccion = unResultadoTraduccion.getObject()
            #unaTraduccion.setPathDelRaiz( unPathDelRaiz)

        #unCatalogBusquedaCadenas = self.fCatalogBusquedaCadenas()   
        #unaBusqueda = { 
            #'Type' :                   'Cadena', 
        #}            
        #unosResultadosBusquedaCadenas      = unCatalogBusquedaCadenas.searchResults(**unaBusqueda)
        #for unResultadoCadena in unosResultadosBusquedaCadenas:
            #unaCadena = unResultadoCadena.getObject()
            #unaCadena.setPathDelRaiz( unPathDelRaiz)
            
        #return self
    
        
        
        
            
            
            