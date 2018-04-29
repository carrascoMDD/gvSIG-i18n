# -*- coding: utf-8 -*-
#
# File: TRAElemento_Recatalog.py
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


import sys
import traceback
import logging
import transaction

import cgi





from DateTime                   import DateTime

from AccessControl              import ClassSecurityInfo

from Products.CMFCore           import permissions

from Products.CMFCore.utils     import getToolByName




from TRAElemento_Constants      import *

from TRAElemento_Permission_Definitions import cUseCase_ReCatalogTRAElemento, cBoundObject

from TRACatalogo_Globales       import TRACatalogo_Globales


    
    
    
            
# ########################################################################################################
    
class TRAElemento_Recatalog:
    """CLASS: role class in support of responsibility of performing an inventory for all application elements.
        
    """
    
    security = ClassSecurityInfo()

         
        

    security.declareProtected( permissions.ManagePortal, 'fRequestNewRecatalog')
    def fRequestNewRecatalog( self, 
        theAdditionalParms      =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Request creation of an Recatalog long-lived process control handler, to be executed later.
        
        """


        
        
        def fRecatalogInitialize_lambda( theContextualElement, theProcessControlManager, theAdditionalParmsHere):  
        
            if theContextualElement == None:
                return None
            
            if not theProcessControlManager:
                return None
            
            unCatalogoRaiz  = theContextualElement.getCatalogo()
            
            unPortalCatalog = theContextualElement.getPortalCatalogTool()
    
            unCatalogBusquedaCadenas       = unCatalogoRaiz.fCatalogBusquedaCadenas() 
            unCatalogFiltroCadenas         = unCatalogoRaiz.fCatalogFiltroCadenas() 
            unCatalogTextoCadenas          = unCatalogoRaiz.fCatalogTextoCadenas() 
        
            todosIdiomas = [ ]
            unasColeccionesIdiomas = unCatalogoRaiz.fObtenerTodasColeccionesIdiomas()
            if unasColeccionesIdiomas:
                for unaColeccionIdiomas in unasColeccionesIdiomas:
                    unosIdiomas = unaColeccionIdiomas.fObtenerTodosIdiomas()
                    if unosIdiomas:
                        todosIdiomas.extend( unosIdiomas)
                    
            unosCatalogsBusquedaTraduccionesPorIdioma = { }
            unosCatalogsFiltroTraduccionesPorIdioma   = { }
            unosCatalogsTextoTraduccionesPorIdioma    = { }
            for unIdioma in todosIdiomas:
                if not( unIdioma == None):
                    unCodigoIdioma = unIdioma.getCodigoIdiomaEnGvSIG()
                    if unCodigoIdioma:
                        unosCatalogsBusquedaTraduccionesPorIdioma[ unCodigoIdioma] = unCatalogoRaiz.fCatalogBusquedaTraduccionesParaIdioma( unIdioma)
                        unosCatalogsFiltroTraduccionesPorIdioma[   unCodigoIdioma] = unCatalogoRaiz.fCatalogFiltroTraduccionesParaIdioma(   unIdioma)
                        unosCatalogsTextoTraduccionesPorIdioma[    unCodigoIdioma] = unCatalogoRaiz.fCatalogTextoTraduccionesParaIdioma(    unIdioma)
                
            unosInitializedObjects = {
                'catalogs': {
                    'PortalCatalog':        unPortalCatalog,
                    'BusquedaCadenas':      unCatalogBusquedaCadenas,
                    'FiltroCadenas':        unCatalogFiltroCadenas,
                    'TextoCadenas':         unCatalogTextoCadenas,
                    'BusquedaTraducciones': unosCatalogsBusquedaTraduccionesPorIdioma,
                    'FiltroTraducciones':   unosCatalogsFiltroTraduccionesPorIdioma,
                    'TextoTraducciones':    unosCatalogsTextoTraduccionesPorIdioma,
                },
            }
            
            theProcessControlManager.pAddInitializedObjects( unosInitializedObjects)
            
            return None        
                    
         
        
            
        def fRecatalogElement_lambda( theElement, theProcessControlManager, theAdditionalParmsHere):  
            
            if theElement == None:
                return None
            
            if not theProcessControlManager:
                return None
            
            someCatalogs = theProcessControlManager.fGetInitializedObjects( 'catalogs')

            aMetaType = 'UnknownType'
            try:
                aMetaType = theElement.meta_type
            except:
                aMetaType = theElement.__class__.__name
            if not aMetaType:
                aMetaType = 'UnknownType'
                
            
            if aMetaType == cNombreTipoTRATraduccion:
                unCodigoIdioma = theElement.getCodigoIdiomaEnGvSIG()
                theElement.pAddToCatalogs( someCatalogs.get( 'BusquedaTraducciones', {}).get( unCodigoIdioma),  someCatalogs.get( 'FiltroTraducciones', {}).get( unCodigoIdioma),  someCatalogs.get( 'TextoTraducciones', {}).get( unCodigoIdioma), None)
                
            elif aMetaType == cNombreTipoTRACadena:
                theElement.pAddToCatalogs( someCatalogs.get( 'BusquedaCadenas', None),  someCatalogs.get( 'FiltroCadenas', None),  someCatalogs.get( 'TextoCadenas', None),)
                
            else:
                theElement.reindexObject()
            
            anElementsByType = { aMetaType: 1,}
            
            theProcessControlManager.pProcessStep( theElement, anElementsByType, anElementsByType)
                
            return None        

        
        
        
        unExecutionRecord = self.fStartExecution( 'method',  'fRequestNewRecatalog', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }, ) 
        
        
        try:
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                
            aRecatalogResult = self.fNewVoidProgressResult()
            
            
            aProgressElement = None
            aThereWasException = False
            aProgressHandler = None
            
            try:
                
                aMetaType = 'UnknownType'
                try:
                    aMetaType = self.meta_type
                except:
                    aMetaType = self.__class__.__name
                if not aMetaType:
                    aMetaType = 'UnknownType'
                
                aStartDateTimeNowTextual = self.fDateTimeNowTextual()
                aRecatalogResult[ 'process_type']           = cTRAProgress_ProcessType_ReCatalog
                aRecatalogResult[ 'start_date_time_string'] = aStartDateTimeNowTextual
                aRecatalogResult[ 'date_time_now_string']   = aStartDateTimeNowTextual
                aRecatalogResult[ 'element_type']           = aMetaType
                aRecatalogResult[ 'element_title']          = self.Title()
                aRecatalogResult[ 'element_path' ]          = self.fPhysicalPathString()
                aRecatalogResult[ 'element_UID' ]           = self.UID()
                aRecatalogResult[ 'last_element_type']      = ''
                aRecatalogResult[ 'last_element_title']     = ''
                aRecatalogResult[ 'last_element_path']      = ''
                aRecatalogResult[ 'last_element_UID']       = ''
                
                aMemberId = self.fGetMemberId()
                aRecatalogResult[ 'member_id'] = aMemberId
                
                unCatalogoRaiz = self.getCatalogo()           
                aRecatalogResult[ 'TRACatalogo_title']      = unCatalogoRaiz.Title()
                aRecatalogResult[ 'TRACatalogo_path' ]      = unCatalogoRaiz.fPathDelRaiz()
                aRecatalogResult[ 'TRACatalogo_UID' ]       = unCatalogoRaiz.UID()
                
                    
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_ReCatalogTRAElemento, 
                    theElementsBindings     = { cBoundObject: self,},
                    theRulesToCollect       = [ ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord
                )
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    aRecatalogResult[ 'success']   =  False
                    aRecatalogResult[ 'condition'] = 'user_can_NOT_RecatalogElementsIn_TRACatalogo'
                    aRecatalogResult[ 'date_time_now_string']   = self.fDateTimeNowTextual()
                    return None
                
                

                aProgressHandler, aProgressElement = self.fCreateNewProgressAndHandlerForElement(  
                    theInitialElement       =self, 
                    theProcessType          =cTRAProgress_ProcessType_ReCatalog, 
                    theTimestamp            =aStartDateTimeNowTextual,
                    theResult               =aRecatalogResult, 
                    theElementLambda        =fRecatalogElement_lambda,
                    theInitializeLambda     =fRecatalogInitialize_lambda,
                    theLockCatalog          =True,
                    thePermissionsCache     =unPermissionsCache, 
                    theRolesCache           =unRolesCache, 
                    theParentExecutionRecord=unExecutionRecord,)
                if ( not aProgressHandler) or ( aProgressElement == None):
                    return None
                
                aProgressHandler_Key = aProgressHandler.fKey()
                
                return aProgressHandler_Key
            
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                aThereWasException = True
                unInformeExcepcion = ''
                try:
                    unInformeExcepcion += 'Exception during fRequestNewRecatalog of element %s %s at %s\n'  % (  self.meta_type(), self.Title(), self.fPhysicalPathString())
                except:
                    None
                try:
                    unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                except:
                    None
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                try:
                    unInformeExcepcion += unaExceptionFormattedTraceback   
                except:
                    None
                
                unInformeExcepcionWOResult = unInformeExcepcion[:]
                
                aRecatalogResult[ 'success'] = False
                aRecatalogResult[ 'exception_date_time_string'] = self.fDateTimeNowTextual()
                try:
                    aRecatalogResultDump = self.fProgressResult_dump( aRecatalogResult)
                except:
                    None
                if aRecatalogResultDump:
                    unInformeExcepcion += aRecatalogResultDump
                
                aRecatalogResult[ 'exception_report'] = unInformeExcepcionWOResult

                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
    
                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return None
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
           
        
       
            
            
            
        
       
                        
            
    
    