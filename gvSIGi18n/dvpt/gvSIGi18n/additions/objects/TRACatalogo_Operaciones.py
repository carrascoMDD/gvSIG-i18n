# -*- coding: utf-8 -*-
#
# File: TRACatalogo_Operaciones.py
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





from TRAElemento_Constants import *

from TRACatalogo_Inicializacion import cNombreCatalogoBusquedaCadenas, cNombreCatalogoFiltroCadenas, cNombreCatalogoTextoCadenas, cNombreCatalogoBusquedaTraducciones, cNombreCatalogoFiltroTraducciones, cNombreCatalogoTextoTraducciones

from TRAElemento import TRAElemento

from TRAElemento_Permission_Definitions import cUseCase_VerifyTRACatalogo, cUseCase_InitializeTRACatalogo, cUseCase_Export, cUseCase_ConfigureTRACatalogo
from TRAElemento_Permission_Definitions import cUseCase_LockTRACatalogo, cUseCase_UnlockTRACatalogo, cUseCase_CreateTRAInforme
# ACV 20090924 Unused, REmoved
#
#from TRAElemento_Permission_Definitions import cUseCase_AuthorizeUsers, cUseCase_ReviewUsersAuthorizations

from TRAElemento_Permission_Definitions import cBoundObject, cTRAUserGroups_Catalogo
from TRAElemento_Permission_Definitions import cTRAUserGroups_Catalogo_AuthorizedOnIndividualIdiomas, cTRAUserGroups_Catalogo_AuthorizedOnIndividualModulos



from TRACatalogo_Inicializacion_Constants import cTRACatalogsDetailsParaIdioma



cBusquedaTodasCadenasOrdenadasPorSimbolo = { 
        'getEstadoCadena':  cEstadoCadenaActiva, 
        'sort_on':          'getSimbolo',  
        'sort_order':       'ascending',
}           

cBusquedaCadenasInactivasOrdenadasPorSimbolo = { 
        'getEstadoCadena':  cEstadoCadenaInactiva, 
        'sort_on':          'getSimbolo',  
        'sort_order':       'ascending',
}           

cModuleStartLine = '===---==='       


cLogInicializarSimbolosCadenasOrdenados = True

  



class TRACatalogo_Operaciones:
    """
    """
    security = ClassSecurityInfo()

    
    security.declarePrivate( 'pAllSubElements_into')        
    def pAllSubElements_into( self, theCollection, theAdditionalParms=None):
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
    
        return self
    

    
    
    security.declarePrivate( 'pForAllElementsDo_recursive')        
    def pForAllElementsDo_recursive( self, theLambda):
        if not theLambda:
            return self
        
        theLambda( self)
        
        
        unosElementos = self.fObtenerTodasColeccionesIdiomas()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda)
                
        unosElementos = self.fObtenerTodasColeccionesModulos()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda)
                
        unosElementos = self.fObtenerTodasColeccionesCadenas()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda)
                
        unosElementos = self.fObtenerTodasColeccionesSolicitudesCadenas()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda)
                
        unosElementos = self.fObtenerTodasColeccionesImportaciones()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda)
                
        unosElementos = self.fObtenerTodasColeccionesInformes()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda)
                
        unosElementos = self.fObtenerTodasColeccionesProgresos()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda)
                
        unosElementos = self.fObtenerTodosParametrosControlProgeso()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda)
                
        return self    
      
    
# ####################################
#  Destroy before deletion
#
        
    
    security.declarePrivate('pHandle_manage_beforeDelete')
    def pHandle_manage_beforeDelete(self, theItem, theContainer):
        """Disable ZCatalog logging while deleting contents to avoid flooding the log with catalog messages complaining about keys not found. 
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
        
    
    
    
    
    

    
    security.declareProtected( permissions.ModifyPortalContent, 'fBloquearCatalogo')
    def fBloquearCatalogo( self , theCheckPermissions=True, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fBloquearCatalogo', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators import ModelDDvlPloneTool_Mutators,cModificationKind_CreateSubElement, cModificationKind_Create, cModificationKind_ChangeValues
        
        try:
            
            try:
                
                if theCheckPermissions:
                
                    unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                    unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                
                    unUseCaseQueryResult = self.fUseCaseAssessment(  
                        theUseCaseName          = cUseCase_LockTRACatalogo, 
                        theElementsBindings     = { cBoundObject: self,},
                        theRulesToCollect       = [ ], 
                        thePermissionsCache     = unPermissionsCache, 
                        theRolesCache           = unRolesCache, 
                        theParentExecutionRecord= unExecutionRecord
                    )
                    if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                        return False
                            
                                    
                unPermiteModificar = self.getPermiteModificar()
                
                if unPermiteModificar:
                    self.setPermiteModificar( False)
                    
                    self.pFlushCachedTemplates_All()                            
                    
                    
                    aModelDDvlPloneTool_Mutators = ModelDDvlPloneTool_Mutators()
                   
                    aReport = aModelDDvlPloneTool_Mutators.fNewVoidChangeValuesReport()
                    someFieldReports    = aReport.get( 'field_reports')
                    aFieldReportsByName = aReport.get( 'field_reports_by_name')       

                    aReportForField = { 'attribute_name': 'permiteModificar', 'effect': 'changed', 'new_value': False, 'previous_value': True,}                                                                                                                        
                    
                    someFieldReports.append( aReportForField)
                    aFieldReportsByName[ 'permiteModificar'] = aReportForField
                    
                    aModelDDvlPloneTool_Mutators.pSetAudit_Modification( self, cModificationKind_ChangeValues, aReport)       
                    
                    transaction.commit()
                    logging.getLogger( 'gvSIGi18n').info( "COMMIT TRACatalogo::fBloquearCatalogo %s" % '/'.join( self.getPhysicalPath()))
                    
                return True
            
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during TRACatalogo::fBloquearCatalogo %s \n'  % '/'.join( self.getPhysicalPath())
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   

                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return False
        
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

            
 
    

    
    security.declareProtected( permissions.ModifyPortalContent, 'fDesbloquearCatalogo')
    def fDesbloquearCatalogo( self , theCheckPermissions=True, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fDesbloquearCatalogo', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators import ModelDDvlPloneTool_Mutators,cModificationKind_CreateSubElement, cModificationKind_Create, cModificationKind_ChangeValues

        try:
            
            try:
                
                if theCheckPermissions:
                
                    unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                    unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                
                    unUseCaseQueryResult = self.fUseCaseAssessment(  
                        theUseCaseName          = cUseCase_UnlockTRACatalogo, 
                        theElementsBindings     = { cBoundObject: self,},
                        theRulesToCollect       = [ ], 
                        thePermissionsCache     = unPermissionsCache, 
                        theRolesCache           = unRolesCache, 
                        theParentExecutionRecord= unExecutionRecord
                    )
                    if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                        return False
                        
                                    
                unPermiteModificar = self.getPermiteModificar()
                
                if not unPermiteModificar:
                    self.setPermiteModificar( True)
                    
                    self.pFlushCachedTemplates_All()                            
                    
                    aModelDDvlPloneTool_Mutators = ModelDDvlPloneTool_Mutators()
                   
                    aReport = aModelDDvlPloneTool_Mutators.fNewVoidChangeValuesReport()
                    someFieldReports    = aReport.get( 'field_reports')
                    aFieldReportsByName = aReport.get( 'field_reports_by_name')       

                    aReportForField = { 'attribute_name': 'permiteModificar', 'effect': 'changed', 'new_value': True, 'previous_value': False,}                                                                                                                        
                    
                    someFieldReports.append( aReportForField)
                    aFieldReportsByName[ 'permiteModificar'] = aReportForField
                    
                    aModelDDvlPloneTool_Mutators.pSetAudit_Modification( self, cModificationKind_ChangeValues, aReport)       
                    
                    transaction.commit()
                    logging.getLogger( 'gvSIGi18n').info( "COMMIT TRACatalogo::fDesbloquearCatalogo %s" % '/'.join( self.getPhysicalPath()))
                    
                return True
            
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during TRACatalogo::fDesbloquearCatalogo %s \n'  % '/'.join( self.getPhysicalPath())
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   

                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return False
        
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

            
 
        
    

    
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
        # ACV 20100721 Do not default to any module name (used to be 'base')
        # if not unNombreModulo:
        #    unNombreModulo = cDefaultModule
            
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
    
    
        
    
    
    # ACV 20090924 Invocations substituted by invocations of generic method with parameter object.fUseCaseCheckDoable( 'Verify_TRACatalogo')
    #security.declarePublic('fUseCaseCheckDoable_VerifyTRACatalogo')
    #def fUseCaseCheckDoable_VerifyTRACatalogo(self, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):   

 
        #unExecutionRecord = self.fStartExecution( 'method',  'fUseCaseCheckDoable_VerifyTRACatalogo', theParentExecutionRecord, False) 
        
        #try:
            #try:
                #unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                #unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                    
                #unUseCaseAssessmentResult = self.fUseCaseAssessment( 
                    #theUseCaseName          = cUseCase_VerifyTRACatalogo, 
                    #theElementsBindings     = { 'object': self,},
                    #theRulesToCollect       = None, 
                    #thePermissionsCache     = unPermissionsCache, 
                    #theRolesCache           = unRolesCache, 
                    #theParentExecutionRecord= unExecutionRecord)
                
                #unResult = unUseCaseAssessmentResult and unUseCaseAssessmentResult.get( 'success', False)
                #return unResult 
    
    
            #except:
                #unaExceptionInfo = sys.exc_info()
                #unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                #unInformeExcepcion = 'Exception during fUseCaseCheckDoable_VerifyTRACatalogo\n' 
                #unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                #unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                #unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                #unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
    
                #if cLogExceptions:
                    #logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                #return False

        #finally:
            #unExecutionRecord and unExecutionRecord.pEndExecution()
     
        
    
    

    
    
    # ACV 20090924 Invocations substituted by invocations of generic method with parameter object.fUseCaseCheckDoable( 'Configure_TRACatalogo')
    #security.declarePublic('fUseCaseCheckDoable_ConfigureTRACatalogo')
    #def fUseCaseCheckDoable_ConfigureTRACatalogo(self, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):   

 
        #unExecutionRecord = self.fStartExecution( 'method',  'fUseCaseCheckDoable_ConfigureTRACatalogo', theParentExecutionRecord, False) 
        
        #try:
            #try:
                #unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                #unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                    
                #unUseCaseAssessmentResult = self.fUseCaseAssessment( 
                    #theUseCaseName          = cUseCase_ConfigureTRACatalogo, 
                    #theElementsBindings     = { 'object': self,},
                    #theRulesToCollect       = None, 
                    #thePermissionsCache     = unPermissionsCache, 
                    #theRolesCache           = unRolesCache, 
                    #theParentExecutionRecord= unExecutionRecord)
                
                #unResult = unUseCaseAssessmentResult and unUseCaseAssessmentResult.get( 'success', False)
                #return unResult 
    
    
            #except:
                #unaExceptionInfo = sys.exc_info()
                #unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                #unInformeExcepcion = 'Exception during fUseCaseCheckDoable_ConfigureTRACatalogo\n' 
                #unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                #unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                #unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                #unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
    
                #if cLogExceptions:
                    #logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                #return False

        #finally:
            #unExecutionRecord and unExecutionRecord.pEndExecution()
     
        
    
    
    
   # ACV 20090924 Unused. Removed. Checks for the use case are done programmatically, and using the results, therefore there are no stand alone doability invocations for the use case.
    #security.declarePublic('fUseCaseCheckDoable_InitializeTRACatalogo')
    #def fUseCaseCheckDoable_InitializeTRACatalogo(self, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):   

 
        #unExecutionRecord = self.fStartExecution( 'method',  'fUseCaseCheckDoable_InitializeTRACatalogo', theParentExecutionRecord, False) 
        
        #try:
     
            #try: 
                #unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                #unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                    
                #unUseCaseAssessmentResult = self.fUseCaseAssessment( 
                    #theUseCaseName          = cUseCase_InitializeTRACatalogo, 
                    #theElementsBindings     = { 'object': self,},
                    #theRulesToCollect       = None, 
                    #thePermissionsCache     = unPermissionsCache, 
                    #theRolesCache           = unRolesCache, 
                    #theParentExecutionRecord= unExecutionRecord)
                
                #unResult = unUseCaseAssessmentResult and unUseCaseAssessmentResult.get( 'success', False)
                #return unResult 
    
    
            #except:
                #unaExceptionInfo = sys.exc_info()
                #unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                #unInformeExcepcion = 'Exception during fUseCaseCheckDoable_InitializeTRACatalogo\n' 
                #unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                #unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                #unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                #unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
    
                #if cLogExceptions:
                    #logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                #return False

        #finally:
            #unExecutionRecord and unExecutionRecord.pEndExecution()
     
        
    

    # ACV 20090924 Invocations substituted by invocations of generic method with parameter object.fUseCaseCheckDoable( 'Export')
    #security.declarePublic('fUseCaseCheckDoable_Export')
    #def fUseCaseCheckDoable_Export(self, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):   

 
        #unExecutionRecord = self.fStartExecution( 'method',  'fUseCaseCheckDoable_Export', theParentExecutionRecord, False) 
        
        #try:
     
            #try: 
                #unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                #unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                    
                #unUseCaseAssessmentResult = self.fUseCaseAssessment( 
                    #theUseCaseName          = cUseCase_Export, 
                    #theElementsBindings     = { 'object': self,},
                    #theRulesToCollect       = None, 
                    #thePermissionsCache     = unPermissionsCache, 
                    #theRolesCache           = unRolesCache, 
                    #theParentExecutionRecord= unExecutionRecord)
                
                #unResult = unUseCaseAssessmentResult and unUseCaseAssessmentResult.get( 'success', False)
                #return unResult 
    
    
            #except:
                #unaExceptionInfo = sys.exc_info()
                #unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                #unInformeExcepcion = 'Exception during fUseCaseCheckDoable_Export\n' 
                #unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                #unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                #unInformeExcepcion += unaExceptionFormattedTraceback   
                
                #unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
    
                #if cLogExceptions:
                    #logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                #return False

        #finally:
            #unExecutionRecord and unExecutionRecord.pEndExecution()
     

            
            
            
    
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
     
        
            
            
            
            
    # ACV 20090924 Unused, removed
    #
    #security.declarePublic('fUseCaseCheckDoable_AuthorizeUsers')
    #def fUseCaseCheckDoable_AuthorizeUsers(self, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):   

 
        #unExecutionRecord = self.fStartExecution( 'method',  'fUseCaseCheckDoable_AuthorizeUsers', theParentExecutionRecord, False) 
        
        #try:
            #try:
                #unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                #unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                    
                #unUseCaseAssessmentResult = self.fUseCaseAssessment( 
                    #theUseCaseName          = cUseCase_AuthorizeUsers, 
                    #theElementsBindings     = { 'object': self,},
                    #theRulesToCollect       = None, 
                    #thePermissionsCache     = unPermissionsCache, 
                    #theRolesCache           = unRolesCache, 
                    #theParentExecutionRecord= unExecutionRecord)
                
                #unResult = unUseCaseAssessmentResult and unUseCaseAssessmentResult.get( 'success', False)
                #return unResult 
    
    
            #except:
                #unaExceptionInfo = sys.exc_info()
                #unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                #unInformeExcepcion = 'Exception during fUseCaseCheckDoable_AuthorizeUsers\n' 
                #unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                #unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                #unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                #unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
    
                #if cLogExceptions:
                    #logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                #return False

        #finally:
            #unExecutionRecord and unExecutionRecord.pEndExecution()
     
        
                
        
    # ####################################
    #  Complete initialization after creation
    # ####################################
        
        
    
    security.declarePrivate('pHandle_manage_afterAdd')
    def pHandle_manage_afterAdd(self, theItem, theContainer):   
        
        TRAElemento.manage_afterAdd(  self, theItem, theContainer)
        
        unInforme = self.fVerifyOrInitialize( 
            theAllowInitialization  =True, 
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
         
  
    
    security.declareProtected( permissions.View, 'fObtenerTodasColeccionesIdiomas')
    def fObtenerTodasColeccionesIdiomas( self, ):
   
        unasColecciones = self.objectValues( cNombreTipoTRAColeccionIdiomas) #
        if not unasColecciones:
            return []
        return unasColecciones
                 
    
    

    
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
         
    
    security.declareProtected( permissions.View, 'fObtenerTodasColeccionesModulos')
    def fObtenerTodasColeccionesModulos( self, ):
   
        unasColecciones = self.objectValues( cNombreTipoTRAColeccionModulos) #
        if not unasColecciones:
            return []
        return unasColecciones
         
           

    security.declareProtected( permissions.View, 'fObtenerTodosModulos')
    def fObtenerTodosModulos( self, ):
   
        unaColeccion = self.fObtenerColeccionModulos()
        if not unaColeccion:
            return []
        
        unosElementos= unaColeccion.objectValues ( cNombreTipoTRAModulo) #
        return unosElementos
           
     

    security.declareProtected( permissions.View, 'fObtenerTodosNombresModulos')
    def fObtenerTodosNombresModulos( self, ):
        
        someModulos = self.fObtenerTodosModulos()
        if not someModulos:
            return []
        
        someNombresModulos = [ unModulo.Title() for unModulo in someModulos]
        return someNombresModulos
    
    
  

       
    
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
  

    
    
    
    
    
    
         

    security.declareProtected( permissions.View, 'fTodosModulosVocabulary')
    def fTodosModulosVocabulary(self,):
        
        unDisplayList = DisplayList()
        
        unDisplayList.add( 
            '',
            self.fModelDDvlPloneTool().fTranslateI18N( self, 'gvSIGi18n', cNombreModuloNoEspecificadoLabel_MsgId, cNombreModuloNoEspecificadoInputValue),
        )      
        
        unosNombresModulos = self.fObtenerTodosNombresModulos()
        if not unosNombresModulos:
            return unDisplayList
        
        for unNombreModulo in unosNombresModulos:
            unDisplayList.add( 
                unNombreModulo,
                unNombreModulo,
            )      
        return unDisplayList
    
           
    
    
    
        
    # ####################################
    """TRACadena accessors
    
    """

        
    security.declareProtected( permissions.View, 'fObtenerColeccionCadenas')
    def fObtenerColeccionCadenas( self, ):
   
        unasColecciones = self.objectValues( cNombreTipoTRAColeccionCadenas)
        if not unasColecciones:
            return None
        return unasColecciones[ 0]
         
    
    
         
    security.declareProtected( permissions.View, 'fObtenerTodasColeccionesCadenas')
    def fObtenerTodasColeccionesCadenas( self, ):
   
        unasColecciones = self.objectValues( cNombreTipoTRAColeccionCadenas)
        if not unasColecciones:
            return []
        return unasColecciones
    
    
    
    
            
    security.declareProtected( permissions.View, 'fObtenerColeccionSolicitudesCadenas')
    def fObtenerColeccionSolicitudesCadenas( self, ):
   
        unasColecciones = self.objectValues( cNombreTipoTRAColeccionSolicitudesCadenas)
        if not unasColecciones:
            return None
        return unasColecciones[ 0]
         
    
    
    
    
    security.declareProtected( permissions.View, 'fObtenerTodasColeccionesSolicitudesCadenas')
    def fObtenerTodasColeccionesSolicitudesCadenas( self, ):
   
        unasColecciones = self.objectValues( cNombreTipoTRAColeccionSolicitudesCadenas)
        if not unasColecciones:
            return []
        return unasColecciones
         
            
    
    
    
    
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
        if ( unCatalog == None):
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
        if ( unCatalog == None):
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
        if ( unCatalog == None):
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
        if ( unCatalog == None):
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
        
        

    
    
    
        
    security.declareProtected( permissions.View, 'fGetCadenaInactivaPorSimbolo')    
    def fGetCadenaInactivaPorSimbolo(self, theSimboloCadena):
        if not theSimboloCadena:
            return None                   

        unCatalog = self.fCatalogBusquedaCadenas() 
        if ( unCatalog == None):
            return None
        unaBusqueda = { 
            'getSimbolo' :      theSimboloCadena,
            'getEstadoCadena':  cEstadoCadenaInactiva
        }
            
        unosResultadosBusqueda = unCatalog.searchResults(**unaBusqueda)
        if len( unosResultadosBusqueda) < 1:
            return None

        unaCadena = unosResultadosBusqueda[ 0].getObject() 
        return unaCadena
                
    
    
    
    
            
    security.declarePrivate( 'getHighestCadenaIdNumber')    
    def getHighestCadenaIdNumber( self):
        
        unCatalog = self.fCatalogBusquedaCadenas() 
        if ( unCatalog == None):
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
   
        unasColecciones = self.fObtenerTodasColeccionesInformes( ) #
        if not unasColecciones:
            return None
        return unasColecciones[ 0]
    


     
    security.declareProtected( permissions.View, 'fObtenerTodasColeccionesInformes')
    def fObtenerTodasColeccionesInformes( self, ):
   
        unasColecciones = self.objectValues( cNombreTipoTRAColeccionInformes) #
        if not unasColecciones:
            return []
        return unasColecciones
            

    security.declareProtected( permissions.View, 'fObtenerTodosInformes')
    def fObtenerTodosInformes( self, ):
   
        unaColeccion = self.fObtenerColeccionInformes()
        if not unaColeccion:
            return []
        
        unosElementos = unaColeccion.objectValues ( cNombreTipoTRAInforme) #
        return unosElementos
           
     
    
   
           
    # ####################################
    """TRAProgreso accessors
    
    """    
    
    security.declareProtected( permissions.View, 'fObtenerColeccionProgresos')
    def fObtenerColeccionProgresos( self, ):
   
        unasColecciones = self.fObtenerTodasColeccionesProgresos( ) #
        if not unasColecciones:
            return None
        return unasColecciones[ 0]
    

    
     
    security.declareProtected( permissions.View, 'fObtenerTodasColeccionesProgresos')
    def fObtenerTodasColeccionesProgresos( self, ):
   
        unasColecciones = self.objectValues( cNombreTipoTRAColeccionProgresos) #
        if not unasColecciones:
            return []
        return unasColecciones
            

    security.declareProtected( permissions.View, 'fObtenerTodosProgresos')
    def fObtenerTodosProgresos( self, ):
   
        unaColeccion = self.fObtenerColeccionProgresos()
        if not unaColeccion:
            return []
        
        unosElementos = unaColeccion.objectValues ( cNombreTipoTRAProgreso) #
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
    
             
    security.declareProtected( permissions.View, 'fObtenerTodasColeccionesImportaciones')
    def fObtenerTodasColeccionesImportaciones( self, ):
   
        unasColecciones = self.objectValues( cNombreTipoTRAColeccionImportaciones) #
        if not unasColecciones:
            return []
        return unasColecciones
    
        

    
    
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

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators import ModelDDvlPloneTool_Mutators,cModificationKind_CreateSubElement, cModificationKind_Create, cModificationKind_ChangeValues

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
            
            self.fVerifyOrInitializeCatalogsEIndicesParaIdioma( 
                theEspecificacionesCatalogs =cTRACatalogsDetailsParaIdioma,
                theAllowInitialization  = True, 
                theIdioma               = unNuevoIdioma,  
                theCheckPermissions     = False, 
                thePermissionsCache     = unPermissionsCache, 
                theRolesCache           = unRolesCache, 
                theParentExecutionRecord= unExecutionRecord
            )
           
    
            # ACV 20090914 Simpler security schema: no user groups for languages or modules, shall assign local roles to users directly on the language or module element
            #self.fLazyCrearUserGroupsParaIdioma(
                #theAllowCreation        = True, 
                #theIdioma               = unNuevoIdioma,  
                #theCheckPermissions     = False, 
                #thePermissionsCache     = unPermissionsCache, 
                #theRolesCache           = unRolesCache, 
                #theParentExecutionRecord= unExecutionRecord
            #)
                         
            # ACV 20090914 Simpler security schema: no user groups for languages or modules, shall assign local roles to users directly on the language or module element
            if not self.fSetLocalRolesEnIdiomaForCatalogUserGroups( unNuevoIdioma):
                return None
            
            
            unResultadoNuevoIdioma = self.fModelDDvlPloneTool().fRetrieveTypeConfig( 
                theTimeProfilingResults     =None,
                theElement                  =unNuevoIdioma, 
                theParent                   =None,
                theParentTraversalName      ='',
                theTypeConfig               =None, 
                theAllTypeConfigs           =None, 
                theViewName                 ='', 
                theRetrievalExtents         =[ 'traversals', ],
                theWritePermissions         =None,
                theFeatureFilters           ={ 'attrs': [ 'title',], 'relations': [], 'do_not_recurse_collections': True,}, 
                theInstanceFilters          =None,
                theTranslationsCaches       =None,
                theCheckedPermissionsCache  =thePermissionsCache,
                theAdditionalParams         =None                
            )
            if unResultadoNuevoIdioma:
            
                aModelDDvlPloneTool_Mutators = ModelDDvlPloneTool_Mutators()
                    
                aCreateElementReport = aModelDDvlPloneTool_Mutators.fNewVoidCreateElementReport()
                aCreateElementReport.update( { 'effect': 'created', 'new_object_result': unResultadoNuevoIdioma, })
                
                someFieldReports    = aCreateElementReport[ 'field_reports']
                aFieldReportsByName = aCreateElementReport[ 'field_reports_by_name']
                
                aReportForField = { 'attribute_name': 'id',          'effect': 'changed', 'new_value': unaIdIdioma, 'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                
                aReportForField = { 'attribute_name': 'title',       'effect': 'changed', 'new_value': unTitle,           'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                
                aReportForField = { 'attribute_name': 'codigoIdiomaEnGvSIG', 'effect': 'changed', 'new_value': theCodigoIdiomaEnGvSIG,    'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                                   
                aReportForField = { 'attribute_name': 'codigoInternacionalDeIdioma', 'effect': 'changed', 'new_value': theCodigoInternacionalDeIdioma,    'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                                   
                aReportForField = { 'attribute_name': 'nombreNativoDeIdioma', 'effect': 'changed', 'new_value': unNombreNativoIdioma,    'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                                   
                aModelDDvlPloneTool_Mutators.pSetAudit_Creation( unaColeccionIdiomas, cModificationKind_CreateSubElement, aCreateElementReport, theUseCounter=True)       
                aModelDDvlPloneTool_Mutators.pSetAudit_Creation( unNuevoIdioma,       cModificationKind_Create,           aCreateElementReport)       
             
            
            
                                                             
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
                
            unNuevoIdioma.setPermiteLeer( True)
            unNuevoIdioma.setPermiteModificar( True)
            
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
        
        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators import ModelDDvlPloneTool_Mutators,cModificationKind_CreateSubElement, cModificationKind_Create, cModificationKind_ChangeValues

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
           
            # ACV 20090914 Simpler security schema: no user groups for languages or modules, shall assign local roles to users directly on the language or module element
            # Method invoked below fLazyCrearUserGroupsParaModulo was never implemented
            # self.fLazyCrearUserGroupsParaModulo(       unNuevoModulo, False)

            
            # ACV 20090914 Simpler security schema: no user groups for languages or modules, shall assign local roles to users directly on the language or module element
            if not self.fSetLocalRolesEnModuloForCatalogUserGroups( unNuevoModulo):
                return None
            
            
            
            unResultadoNuevoModulo = self.fModelDDvlPloneTool().fRetrieveTypeConfig( 
                theTimeProfilingResults     =None,
                theElement                  =unNuevoModulo, 
                theParent                   =None,
                theParentTraversalName      ='',
                theTypeConfig               =None, 
                theAllTypeConfigs           =None, 
                theViewName                 ='', 
                theRetrievalExtents         =[ 'traversals', ],
                theWritePermissions         =None,
                theFeatureFilters           ={ 'attrs': [ 'title',], 'relations': [], 'do_not_recurse_collections': True,}, 
                theInstanceFilters          =None,
                theTranslationsCaches       =None,
                theCheckedPermissionsCache  =thePermissionsCache,
                theAdditionalParams         =None                
            )
            if unResultadoNuevoModulo:
            
                aModelDDvlPloneTool_Mutators = ModelDDvlPloneTool_Mutators()
                    
                aCreateElementReport = aModelDDvlPloneTool_Mutators.fNewVoidCreateElementReport()
                aCreateElementReport.update( { 'effect': 'created', 'new_object_result': unResultadoNuevoModulo, })
                
                someFieldReports    = aCreateElementReport[ 'field_reports']
                aFieldReportsByName = aCreateElementReport[ 'field_reports_by_name']
                
                aReportForField = { 'attribute_name': 'id',          'effect': 'changed', 'new_value': unaIdModulo, 'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                
                aReportForField = { 'attribute_name': 'title',       'effect': 'changed', 'new_value': theNombreModulo,           'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField

                aModelDDvlPloneTool_Mutators.pSetAudit_Creation( unaColeccionModulos, cModificationKind_CreateSubElement, aCreateElementReport, theUseCounter=True)       
                aModelDDvlPloneTool_Mutators.pSetAudit_Creation( unNuevoModulo,       cModificationKind_Create,           aCreateElementReport)       
             
            
           
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
                
            unNuevoModulo.setPermiteLeer( True)
            unNuevoModulo.setPermiteModificar( True)
            
            return unNuevoModulo
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
           
        
     
 


    security.declarePrivate( 'fSetLocalRolesEnIdiomaForCatalogUserGroups')
    def fSetLocalRolesEnIdiomaForCatalogUserGroups( self, theIdioma):
        if not theIdioma:
            return False
        
        someUserGroupsNamesAndRolesCatalogo = cTRAUserGroups_Catalogo
        someUserGroupsToSetRolesEnIdioma     = cTRAUserGroups_Catalogo_AuthorizedOnIndividualIdiomas
 
        for unUserGroupToSetRoles in someUserGroupsToSetRolesEnIdioma:
            unosRolesToSet = []
            for unUserGroupNameAndRoles in someUserGroupsNamesAndRolesCatalogo:
                unUserGroupName = unUserGroupNameAndRoles[ 0]
                if unUserGroupName == unUserGroupToSetRoles:
                    unosRolesToSet = unUserGroupNameAndRoles[ 1]
                    break
                
            if unosRolesToSet:
                
                unUserGroupId = self.fUserGroupIdEnCatalogoFor( unUserGroupToSetRoles)
                
                unosExistingGroupRoles    = list( theIdioma.get_local_roles_for_userid( unUserGroupId))[:]
                unosNonExistingGroupRoles = list( set( unosRolesToSet) - set( unosExistingGroupRoles))
                
                if unosNonExistingGroupRoles:
                         
                    theIdioma.manage_addLocalRoles( unUserGroupId, tuple( unosNonExistingGroupRoles))
                    # ACV 200903212354 learned from Products.CMFCore.MembershipTool.MembershipTool.setLocalRoles()                     
                    theIdioma.reindexObjectSecurity()
                    
        return True                        
                        
                        
                        
                        

 


    security.declarePrivate( 'fSetLocalRolesEnModuloForCatalogUserGroups')
    def fSetLocalRolesEnModuloForCatalogUserGroups( self, theModulo):
        if not theModulo:
            return False
        
        someUserGroupsNamesAndRolesCatalogo  = cTRAUserGroups_Catalogo
        someUserGroupsToSetRolesEnModulo     = cTRAUserGroups_Catalogo_AuthorizedOnIndividualModulos
 
        for unUserGroupToSetRoles in someUserGroupsToSetRolesEnModulo:
            unosRolesToSet = []
            for unUserGroupNameAndRoles in someUserGroupsNamesAndRolesCatalogo:
                unUserGroupName = unUserGroupNameAndRoles[ 0]
                if unUserGroupName == unUserGroupToSetRoles:
                    unosRolesToSet = unUserGroupNameAndRoles[ 1]
                    break
                
            if unosRolesToSet:
                
                unUserGroupId = self.fUserGroupIdEnCatalogoFor( unUserGroupToSetRoles)
                
                unosExistingGroupRoles    = list( theModulo.get_local_roles_for_userid( unUserGroupId))[:]
                unosNonExistingGroupRoles = list( set( unosRolesToSet) - set( unosExistingGroupRoles))
                
                if unosNonExistingGroupRoles:
                         
                    theModulo.manage_addLocalRoles( unUserGroupId, tuple( unosNonExistingGroupRoles))
                    # ACV 200903212354 learned from Products.CMFCore.MembershipTool.MembershipTool.setLocalRoles()                     
                    theModulo.reindexObjectSecurity()
                    
        return True                        
                   
        
    
    
    
    
    
    
    
    
    
    
    
    # ################################################################
    """Translation state change methods.
    
    """

     
        
    security.declarePrivate( 'fIntentarTraducirCadena')    
    def fIntentarTraducirCadena( self, 
        theSimboloCadena, 
        theCodigoIdioma, 
        theCadenaTraducida, 
        theComentario, 
        theAdditionalParams      =None,
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):
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
                theIdioma                =unIdioma, 
                theCadenaTraducida       =theCadenaTraducida, 
                theComentario            =theComentario, 
                theAdditionalParams      =theAdditionalParams,
                theRegistrarHistoria     =True, 
                thePermissionsCache      =thePermissionsCache, 
                theRolesCache            =theRolesCache, 
                theParentExecutionRecord =unExecutionRecord,
            )
                
            return unResultado
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            
           

            
        
       
    security.declarePrivate( 'fComentarTraduccionCadena')    
    def fComentarTraduccionCadena( self, 
        theSimboloCadena, 
        theCodigoIdioma, 
        theComentario, 
        theAdditionalParams         =None,
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
                theIdioma                =unIdioma, 
                theComentario            =theComentario, 
                theAdditionalParams      =theAdditionalParams,
                theRegistrarHistoria     =True, 
                thePermissionsCache      =thePermissionsCache, 
                theRolesCache            =theRolesCache, 
                theParentExecutionRecord =unExecutionRecord,
            )
                 
            return unResultado        
               
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            


         
        
        
        
        
    security.declarePrivate( 'fHacerPendienteTraduccionCadena')    
    def fHacerPendienteTraduccionCadena( self, 
        theSimboloCadena, 
        theCodigoIdioma, 
        theComentario, 
        theAdditionalParams         =None,
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
                theIdioma                =unIdioma, 
                theComentario            =theComentario, 
                theAdditionalParams      =theAdditionalParams,
                theRegistrarHistoria     =True, 
                thePermissionsCache      =thePermissionsCache, 
                theRolesCache            =theRolesCache, 
                theParentExecutionRecord =unExecutionRecord,
            )
                 
            return unResultado        
       
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            
         
         
         
         
         

    security.declarePrivate( 'fHacerTraducidaTraduccionCadena')    
    def fHacerTraducidaTraduccionCadena( self, 
        theSimboloCadena, 
        theCodigoIdioma, 
        theComentario, 
        theAdditionalParams         =None,
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
                theIdioma                =unIdioma, 
                theComentario            =theComentario, 
                theAdditionalParams      =theAdditionalParams,
                theRegistrarHistoria     =True, 
                thePermissionsCache      =thePermissionsCache, 
                theRolesCache            =theRolesCache, 
                theParentExecutionRecord =unExecutionRecord,
            )
                            
            return unResultado                 
       
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            
       
       
       
       
       


    security.declarePrivate( 'fHacerRevisadaTraduccionCadena')    
    def fHacerRevisadaTraduccionCadena( self, 
        theSimboloCadena, 
        theCodigoIdioma, 
        theComentario, 
        theAdditionalParams         =None,
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
                theIdioma                =unIdioma, 
                theComentario            =theComentario, 
                theAdditionalParams      =theAdditionalParams,
                theRegistrarHistoria     =True, 
                thePermissionsCache      =thePermissionsCache, 
                theRolesCache            =theRolesCache, 
                theParentExecutionRecord =unExecutionRecord,
            )
            
            return unResultado        
       
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            
         






    security.declarePrivate( 'fHacerDefinitivaTraduccionCadena')    
    def fHacerDefinitivaTraduccionCadena( self, 
        theSimboloCadena, 
        theCodigoIdioma, 
        theComentario, 
        theAdditionalParams         =None,
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
                theIdioma                =unIdioma, 
                theComentario            =theComentario, 
                theAdditionalParams      =theAdditionalParams,
                theRegistrarHistoria     =True, 
                thePermissionsCache      =thePermissionsCache, 
                theRolesCache            =theRolesCache, 
                theParentExecutionRecord =unExecutionRecord,
            )
                 
            return unResultado        
       
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            
  



    security.declarePrivate( 'fInvalidarTraduccionesCadenas')    
    def fInvalidarTraduccionesCadenas( self, 
        theSimboloCadena, 
        theComentario, 
        theAdditionalParams         =None,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord=None):

        unExecutionRecord = self.fStartExecution( 'method',  'fInvalidarTraduccionesCadenas', theParentExecutionRecord, False) 
        
        try:
            if  not theSimboloCadena:
                return self.fNewVoidChangeTranslationResult()
                
            unaCadena = self.fGetCadenaPorSimbolo( theSimboloCadena)
            if not unaCadena:
                return self.fNewVoidChangeTranslationResult()
                
            unResultado = unaCadena.fInvalidarTraducciones(  
                theComentario, 
                theAdditionalParams     =theAdditionalParams,
                theRegistrarHistoria    =True, 
                thePermissionsCache     =thePermissionsCache, 
                theRolesCache           =theRolesCache, 
                theParentExecutionRecord=unExecutionRecord
            )
                 
            return unResultado        
       
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            
  
  



    security.declarePrivate( 'fDesactivarCadena')    
    def fDesactivarCadena( self, 
        theSimboloCadena, 
        theComentario, 
        theAdditionalParams         =None,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord=None):

        unExecutionRecord = self.fStartExecution( 'method',  'fDesactivarCadena', theParentExecutionRecord, False) 
        
        try:
            if  not theSimboloCadena:
                return self.fNewVoidChangeTranslationResult()
                
            unaCadena = self.fGetCadenaPorSimbolo( theSimboloCadena)
            if not unaCadena:
                return self.fNewVoidChangeTranslationResult()
                
            unResultado = unaCadena.fDesactivar(  
                theComentario, 
                theAdditionalParams     =theAdditionalParams,
                theRegistrarHistoria    =True, 
                thePermissionsCache     =thePermissionsCache, 
                theRolesCache           =theRolesCache, 
                theParentExecutionRecord=unExecutionRecord
            )
                 
            return unResultado        
       
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            
  





    security.declarePrivate( 'fActivarCadena')    
    def fActivarCadena( self, 
        theSimboloCadena, 
        theComentario, 
        theAdditionalParams         =None,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord=None):

        unExecutionRecord = self.fStartExecution( 'method',  'fActivarCadena', theParentExecutionRecord, False) 
        
        try:
            if  not theSimboloCadena:
                return self.fNewVoidChangeTranslationResult()
                
            unaCadena = self.fGetCadenaInactivaPorSimbolo( theSimboloCadena)
            if not unaCadena:
                return self.fNewVoidChangeTranslationResult()
                
            unResultado = unaCadena.fActivar(  
                theComentario, 
                theAdditionalParams     =theAdditionalParams,
                theRegistrarHistoria    =True, 
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
        theAdditionalParams         =None,
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
            
             
            for unaIdCadenaAndCounter in theBatchIds_Traducida:
                if unaIdCadenaAndCounter and (len( unaIdCadenaAndCounter) > 1):
                    unaIdCadena       = unaIdCadenaAndCounter[ 0]
                    unChangeCounter   = unaIdCadenaAndCounter[ 1]
                    
                    if unaIdCadena:
                        unaCadena = self.getCadenaPorID( unaIdCadena)
                        if unaCadena:
                            
                            unResultado = unaCadena.fHacerTraducidaTraduccion(  
                                theIdioma                =unIdioma, 
                                theComentario            ='', 
                                theAdditionalParams      ={ 'theContadorCambios': unChangeCounter,},
                                theRegistrarHistoria     =True, 
                                thePermissionsCache      =unPermissionsCache, 
                                theRolesCache            =unRolesCache, 
                                theParentExecutionRecord =unExecutionRecord,
                            )
                             
                            if unResultado.get( 'success', False):
                                unNumSucceeded += 1
                                if unResultado.get( 'changed', False):
                                    unNumChanged += 1
                                
                            else:
                                unNumFailed += 1
                        
                                
                                
                                
                                
                                
            for unaIdCadenaAndCounter in theBatchIds_Revisada:
                
                if unaIdCadenaAndCounter and (len( unaIdCadenaAndCounter) > 1):
                    unaIdCadena       = unaIdCadenaAndCounter[ 0]
                    unChangeCounter   = unaIdCadenaAndCounter[ 1]
                    
                    if unaIdCadena:
                        unaCadena = self.getCadenaPorID( unaIdCadena)
                        if unaCadena:
                            
                            unResultado = unaCadena.fHacerRevisadaTraduccion(  
                                theIdioma                =unIdioma, 
                                theComentario            ='', 
                                theAdditionalParams      ={ 'theContadorCambios': unChangeCounter,},
                                theRegistrarHistoria     =True, 
                                thePermissionsCache      =unPermissionsCache, 
                                theRolesCache            =unRolesCache, 
                                theParentExecutionRecord =unExecutionRecord,
                            )
                             
                            if unResultado.get( 'success', False):
                                unNumSucceeded += 1
                                if unResultado.get( 'changed', False):
                                    unNumChanged += 1
                                
                            else:
                                unNumFailed += 1
                            
                                
                                
                                
                                
            for unaIdCadenaAndCounter in theBatchIds_Definitiva:
                
                if unaIdCadenaAndCounter and (len( unaIdCadenaAndCounter) > 1):
                    unaIdCadena       = unaIdCadenaAndCounter[ 0]
                    unChangeCounter   = unaIdCadenaAndCounter[ 1]
                    
                    if unaIdCadena:
                        unaCadena = self.getCadenaPorID( unaIdCadena)
                        if unaCadena:
                            
                            unResultado = unaCadena.fHacerDefinitivaTraduccion(  
                                theIdioma                =unIdioma, 
                                theComentario            ='', 
                                theAdditionalParams      ={ 'theContadorCambios': unChangeCounter,},
                                theRegistrarHistoria     =True, 
                                thePermissionsCache      =unPermissionsCache, 
                                theRolesCache            =unRolesCache, 
                                theParentExecutionRecord =unExecutionRecord,
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
            
   
            
              
            
        
       

    
    
    
        
    # #######################################################################
    #   Simbolos cadenas in Inactive state
    #   not cached
    #
    # #######################################################################

     

    security.declarePrivate( 'fListaSimbolosCadenasInactivasOrdenados')
    def fListaSimbolosCadenasInactivasOrdenados( self,theParentExecutionRecord=None):
        

        unExecutionRecord = self.fStartExecution( 'method',  'fListaSimbolosCadenasInactivasOrdenados', theParentExecutionRecord, False) 

        if cLogInicializarSimbolosCadenasOrdenados:
            unStartTime = self.fMillisecondsNow()
        
        try:
            unaBusqueda = cBusquedaCadenasInactivasOrdenadasPorSimbolo.copy()

            unCatalogBusquedaCadenas = self.fCatalogBusquedaCadenas()
            if ( unCatalogBusquedaCadenas == None):
                return self
            unosDatosCadenas = unCatalogBusquedaCadenas.searchResults( **unaBusqueda ) 
            
            if not unosDatosCadenas or len( unosDatosCadenas) < 1:
                return [ ]
            
            unosSimbolos = [ ]
            
            for unosDatosCadena in unosDatosCadenas:
                unSimbolo =  unosDatosCadena[ 'getSimbolo']
                if unSimbolo:
                    unosSimbolos.append( unSimbolo)
                    
            return unosSimbolos

        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()


    
    
            
            
        
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
            
            unCatalogFiltroCadenas = self.fCatalogFiltroCadenas()
            if ( unCatalogFiltroCadenas == None):
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
                
                unosNombresModulosString = unosDatosCadena[ 'getNombresModulos']
                unosNombresModulosString = unosNombresModulosString.strip()
                unosNombresModulosString = unosNombresModulosString.replace( '\n', cTRAModuleNameSeparator)
                unosNombresModulosString = unosNombresModulosString.replace( '\r', cTRAModuleNameSeparator)
                unosNombresModulosString = unosNombresModulosString.strip()
                if unosNombresModulosString:
                    unosNombresModulos = unosNombresModulosString.split( cTRAModuleNameSeparator)
                    if unosNombresModulos:
                        for unNombreModulo in unosNombresModulos:
                            if unNombreModulo:
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

     
        

   
        
    security.declareProtected( permissions.View, 'fObtenerTodosParametrosControlProgeso')
    def fObtenerTodosParametrosControlProgeso( self, ):
   
        unosParametrosControlProgreso = self.objectValues( cNombreTipoTRAParametrosControlProgreso)

        return unosParametrosControlProgreso
         
                  

