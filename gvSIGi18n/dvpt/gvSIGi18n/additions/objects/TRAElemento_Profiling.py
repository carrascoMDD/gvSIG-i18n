# -*- coding: utf-8 -*-
#
# File: TRAElemento_Profiling.py
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


import cgi
import logging

import time  


from StringIO                   import StringIO

from AccessControl              import ClassSecurityInfo


from Products.CMFCore           import permissions


from TRAElemento_Constants              import *

from TRACatalogo_Globales import TRACatalogo_Globales
            
            
# ########################################################################################################
    
class TRAElemento_Profiling:
    """Class with responsibility dealing with execution profiling and logging.
        
    """
    
    security = ClassSecurityInfo()

    
    
    security.declarePrivate( 'fNewVoidExecutionProfilingEnablementConfigurationsGlobalAndFromPersistentRoot')
    def fNewVoidExecutionProfilingEnablementConfigurationsGlobalAndFromPersistentRoot(self,):
        aConfig = {
            'global':                        None,
            'for_persistent_root':           None,
        }
        return aConfig


    
    
    
    security.declarePrivate( 'fNewVoidExecutionProfilingEnablementConfiguration')
    def fNewVoidExecutionProfilingEnablementConfiguration(self,):
        aConfig = {
            'root_path':                             '',
            'execution_profiling_enabled':           cTRAExecutionProfilingEnabled,
            'execution_timestamping_enabled':        cTRAExecutionTimestampingEnabled,
            'execution_auto_root_record_enabled':    cTRAExecutionAutoRootRecordEnabled,
            'execution_logging_enabled':             cTRAExecutionLoggingEnabled,
            'execution_logging_detailed_enabled':    cTRAExecutionLoggingDetailedEnabled,
            'execution_rendering_enabled':           cTRAExecutionRenderingEnabled,
            'timestamp_rendering_enabled':           cTRATimestampRenderingEnabled,
        }
        return aConfig
        

    
    
    
    security.declarePrivate( 'fNewVoidConfigureExecutionProfilingEnablementResult')
    def fNewVoidConfigureExecutionProfilingEnablementResult(self,):
        aConfig = {
            'success':                      False,
            'condition':                    None,
            'exception':                    None,
            'root_catalog_path_or_globals': None,
            'requested_configuration':      None,
            'previous_configuration':       None,
            'changes':                      [],
            'new_configuration':            None,
        }
        return aConfig
    
    
    
    
    

    security.declareProtected( permissions.View, 'fExecutionProfilingEnablementConfigurationsGlobalAndFromPersistentRoot')
    def fExecutionProfilingEnablementConfigurationsGlobalAndFromPersistentRoot(self,):
        
        someExecutionProfilingEnablementConfigurations = self.fNewVoidExecutionProfilingEnablementConfigurationsGlobalAndFromPersistentRoot()
        
        someExecutionProfilingEnablementConfigurations[ 'global'] = self.fExecutionProfilingEnablementConfigurationGlobal()
        
        someExecutionProfilingEnablementConfigurations[ 'from_persistent_root'] = self.fExecutionProfilingEnablementConfigurationFromPersistentRoot()

        return someExecutionProfilingEnablementConfigurations
    
    
    
    
  
    security.declareProtected( permissions.ManagePortal, 'fConfigureExecutionProfilingEnablement')
    def fConfigureExecutionProfilingEnablement( self, 
        theRootCatalogPathOrGlobals =None,
        theExecutionProfilingEnablementConfiguration  =None,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None): 
        """Change the configuration of execution profiling enablement, applicable to all translations catalogs (global), or to a specific translations catalog.
        
        """

        # ##################################################################
        """Record execution and chain in the trace and profiling history/stack.
        
        """
        unExecutionRecord = self.fStartExecution( 'method', 'fConfigureExecutionProfilingEnablement', theParentExecutionRecord, False, None, ) 

        aMustWaitAfterConfigure = False

        try:
            
            unResult = self.fNewVoidConfigureExecutionProfilingEnablementResult()
            unResult[ 'root_catalog_path_or_globals'] = theRootCatalogPathOrGlobals
            unResult[ 'requested_configuration']      = theExecutionProfilingEnablementConfiguration
            
            if not theRootCatalogPathOrGlobals:
                return unResult
           
            
            # ##################################################################
            """Initialize permissions and roles cache if not already supplied by service caller.
            
            """
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
            
            
            try: 
                
                unCatalogoRaiz = self.getCatalogo()
                if unCatalogoRaiz == None:
                    return unResult
                
                unPathDelRaiz = unCatalogo.fPathDelRaiz()
                if not unPathDelRaiz:
                    return None
                        
                aUseCaseName = ''
                if theRootCatalogPathOrGlobals == cTRAExecutionProfilingEnablementConfiguration_Global:
                    aUseCaseName = cUseCase_ConfigureExecutionProfilingEnablement_Global
                else:
                    aUseCaseName = cUseCase_ConfigureExecutionProfilingEnablement_TRACatalogo
                    
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = aUseCaseName,        
                    theElementsBindings     = { cBoundObject: unCatalogoRaiz,},                                    
                    theRulesToCollect       = None,                                                      
                    thePermissionsCache     = unPermissionsCache,                                        
                    theRolesCache           = unRolesCache,                                              
                    theParentExecutionRecord= unExecutionRecord,                                          
                )                    
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    unResult.update({
                        'success': False,
                        'condition': 'UseCase_assessment_failed: %s' % aUseCaseName,
                    })
                    return aResult
            
                
                if theRootCatalogPathOrGlobals == cTRAExecutionProfilingEnablementConfiguration_Global:
                    aCurrentConfiguration = self.fExecutionProfilingEnablementConfigurationGlobal()
                else:
                    aCurrentConfiguration = self.fExecutionProfilingEnablementConfigurationFromPersistentRoot()
                    
                unResult[ 'previous_configuration'] = aCurrentConfiguration
                
                someChanges = [ ]
                unResult[ 'changes'] = someChanges
                
                aConfigurationUpdates = { }
                
                for aConfigurationPropertyName in cTRAExecutionProfilingEnablementConfiguration_PropertyNames:
                    aCurrentPropertyValue   = aCurrentConfiguration.get( aConfigurationPropertyName, None)
                    aRequestedPropertyValue = theExecutionProfilingEnablementConfiguration.get( aConfigurationPropertyName, None)
                    
                    if not ( aCurrentPropertyValue == None):
                        if not ( aCurrentPropertyValue == aRequestedPropertyValue):
                            aConfigurationUpdates[ aConfigurationPropertyName] = aRequestedPropertyValue
                            someChanges.append( aConfigurationPropertyName)
                        
                if not someChanges:
                    unResult[ 'success'] = True
                    unResult[ 'condition'] = 'NoChanges'
                    return unResult
                
                
                        
                if theRootCatalogPathOrGlobals == cTRAExecutionProfilingEnablementConfiguration_Global:

                    try:
                        # #################
                        """MUTEX LOCK. 
                        
                        """
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        unCatalogo.pAcquireGlobalsLock( )
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        
                        aGlobalExecutionProfilingEnablementConfiguration = TRACatalogo_Globales.gTRAExecutionProfilingEnablementConfigurationGlobal
                        if not aGlobalExecutionProfilingEnablementConfiguration:
                            aGlobalExecutionProfilingEnablementConfiguration = self.fNewVoidExecutionProfilingEnablementConfiguration()
                            TRACatalogo_Globales.gTRAExecutionProfilingEnablementConfigurationGlobal = aGlobalExecutionProfilingEnablementConfiguration
                            
                        aGlobalExecutionProfilingEnablementConfiguration.update( aConfigurationUpdates)
                    
                    finally:
                        # #################
                        """MUTEX UNLOCK. 
                        
                        """
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        unCatalogo.pReleaseGlobalsLock( )
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    
                else:
                    
                    

                    try:
                        # #################
                        """MUTEX LOCK. 
                        
                        """
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        unCatalogo.pAcquireGlobalsLock( )
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        
            
                        someExecutionProfilingEnablementConfigurations = TRACatalogo_Globales.gTRAExecutionProfilingEnablementConfigurations
                        if someExecutionProfilingEnablementConfigurations == None:
                            someExecutionProfilingEnablementConfigurations = { }
                            TRACatalogo_Globales.gTRAExecutionProfilingEnablementConfigurations = someExecutionProfilingEnablementConfigurations
            
                        anExecutionProfilingEnablementConfigurationForRoot = someExecutionProfilingEnablementConfigurations.get( unPathDelRaiz, None)
                        
                        if anExecutionProfilingEnablementConfigurationForRoot == None:
                            anExecutionProfilingEnablementConfigurationForRoot = self.fExecutionProfilingEnablementConfigurationFromPersistentRoot()
                            someExecutionProfilingEnablementConfigurations[ unPathDelRaiz] = anExecutionProfilingEnablementConfigurationForRoot
                
                            
                        anExecutionProfilingEnablementConfigurationForRoot.update( aConfigurationUpdates)
                    
                    finally:
                        # #################
                        """MUTEX UNLOCK. 
                        
                        """
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        unCatalogo.pReleaseGlobalsLock( )
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                        
                    
                    
                    for aConfigurationPropertyName in cTRAExecutionProfilingEnablementConfiguration_PropertyNames:
                        if aConfigurationUpdates.has_key( aConfigurationPropertyName):
                            aNewValue = aConfigurationUpdates.get( aConfigurationPropertyName, None)
                
                            if aConfigurationPropertyName == 'execution_profiling_enabled':           
                                unCatalogo.setPerfilDeEjecucionHabilitado( aNewValue)
                                
                            elif aConfigurationPropertyName == 'execution_timestamping_enabled':
                                unCatalogo.setTiemposDeEjecucionHabilitado( aNewValue)
                                
                            elif aConfigurationPropertyName == 'execution_auto_root_record_enabled':
                                unCatalogo.setRegistroRaizDeEjecucionAutomaticoHabilitado( aNewValue)
                                
                            elif aConfigurationPropertyName == 'execution_logging_enabled':
                                unCatalogo.setEscrituraEnDiscoDeRegistroDeEjecucionHabilitado( aNewValue)
                                
                            elif aConfigurationPropertyName == 'execution_logging_detailed_enabled':    
                                unCatalogo.setEscrituraEnDiscoDeRegistroDeEjecucionDetalladoHabilitado( aNewValue)
                                
                            elif aConfigurationPropertyName == 'execution_rendering_enabled':           
                                unCatalogo.setPresentacionEnPaginasDeRegistroDeEjecucionHabilitado( aNewValue)
                                
                            elif aConfigurationPropertyName == 'timestamp_rendering_enabled':           
                                unCatalogo.setPresentacionEnPaginasDeTiempoDeEjecucionHabilitado( aNewValue),
                
                                
                if theRootCatalogPathOrGlobals == cTRAExecutionProfilingEnablementConfiguration_Global:
                    aNewConfiguration = self.fExecutionProfilingEnablementConfigurationGlobal()
                else:
                    aNewConfiguration = self.fExecutionProfilingEnablementConfigurationFromPersistentRoot()
                    
                unResult[ 'new_configuration'] = aNewConfiguration
                
                
                return unResult
    
            
                            
            except:
                # ################################################################
                """Handle and report conditions when something went exceptionally wrong.
                
                """
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fConfigureExecutionProfilingEnablement\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                unResult[ 'success']   = False
                unResult[ 'condition'] = cResultCondition_Internal_Exception
                unResult[ 'exception'] = unInformeExcepcion
                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                    
                return unResult
            
             
        finally:
            
            unExecutionRecord and unExecutionRecord.pEndExecution()
                      
            if aMustWaitAfterConfigure:
                self.pSleepMilliseconds( cTRAProgress_WaitAfterConfigureProcess_Milliseconds)

        
       
    
    security.declarePrivate( 'fExecutionProfilingEnablementConfigurationForRoot')
    def fExecutionProfilingEnablementConfigurationForRoot(self, ):
        """Retrieve from global dictionary the enablement configuration for execution profiling, or create a global one from fields in the root catalog.
        
        """
        
        unCatalogo = self.getCatalogo()
        if unCatalogo == None:
            return None
        
        unPathDelRaiz = unCatalogo.fPathDelRaiz()
        if not unPathDelRaiz:
            return None
        
      
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            unCatalogo.pAcquireGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            anExecutionProfilingEnablementConfiguration = { }
            
            
            aGlobalExecutionProfilingEnablementConfiguration = TRACatalogo_Globales.gTRAExecutionProfilingEnablementConfigurationGlobal
            if not aGlobalExecutionProfilingEnablementConfiguration:
                aGlobalExecutionProfilingEnablementConfiguration = self.fNewVoidExecutionProfilingEnablementConfiguration()
                TRACatalogo_Globales.gTRAExecutionProfilingEnablementConfigurationGlobal = aGlobalExecutionProfilingEnablementConfiguration
                
            anExecutionProfilingEnablementConfiguration.update( aGlobalExecutionProfilingEnablementConfiguration)

            
            someExecutionProfilingEnablementConfigurations = TRACatalogo_Globales.gTRAExecutionProfilingEnablementConfigurations
            if someExecutionProfilingEnablementConfigurations == None:
                someExecutionProfilingEnablementConfigurations = { }
                TRACatalogo_Globales.gTRAExecutionProfilingEnablementConfigurations = someExecutionProfilingEnablementConfigurations

            anExecutionProfilingEnablementConfigurationForRoot = someExecutionProfilingEnablementConfigurations.get( unPathDelRaiz, None)
            
            if anExecutionProfilingEnablementConfigurationForRoot == None:
                anExecutionProfilingEnablementConfigurationForRoot = self.fExecutionProfilingEnablementConfigurationFromPersistentRoot()
                someExecutionProfilingEnablementConfigurations[ unPathDelRaiz] = anExecutionProfilingEnablementConfigurationForRoot
                
                
            if anExecutionProfilingEnablementConfiguration.get( 'execution_profiling_enabled', False):                
                anExecutionProfilingEnablementConfiguration[ 'execution_profiling_enabled'] = anExecutionProfilingEnablementConfigurationForRoot.get( 'execution_profiling_enabled', False)

            if anExecutionProfilingEnablementConfiguration.get( 'execution_timestamping_enabled', False):                
                anExecutionProfilingEnablementConfiguration[ 'execution_timestamping_enabled'] = anExecutionProfilingEnablementConfigurationForRoot.get( 'execution_timestamping_enabled', False)
            
            if anExecutionProfilingEnablementConfiguration.get( 'execution_auto_root_record_enabled', False):                
                anExecutionProfilingEnablementConfiguration[ 'execution_auto_root_record_enabled'] = anExecutionProfilingEnablementConfigurationForRoot.get( 'execution_auto_root_record_enabled', False)
            
            if anExecutionProfilingEnablementConfiguration.get( 'execution_logging_enabled', False):                
                anExecutionProfilingEnablementConfiguration[ 'execution_logging_enabled'] = anExecutionProfilingEnablementConfigurationForRoot.get( 'execution_logging_enabled', False)

            if anExecutionProfilingEnablementConfiguration.get( 'execution_logging_detailed_enabled', False):                
                anExecutionProfilingEnablementConfiguration[ 'execution_logging_detailed_enabled'] = anExecutionProfilingEnablementConfigurationForRoot.get( 'execution_logging_detailed_enabled', False)
            
            if anExecutionProfilingEnablementConfiguration.get( 'execution_rendering_enabled', False):                
                anExecutionProfilingEnablementConfiguration[ 'execution_rendering_enabled'] = anExecutionProfilingEnablementConfigurationForRoot.get( 'execution_rendering_enabled', False)
            
            if anExecutionProfilingEnablementConfiguration.get( 'timestamp_rendering_enabled', False):                
                anExecutionProfilingEnablementConfiguration[ 'timestamp_rendering_enabled'] = anExecutionProfilingEnablementConfigurationForRoot.get( 'timestamp_rendering_enabled', False)
                
                
            
            return anExecutionProfilingEnablementConfiguration
            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            unCatalogo.pReleaseGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        return self
            
        
    
  
    
    security.declarePrivate( 'fExecutionProfilingEnablementConfigurationGlobal')
    def fExecutionProfilingEnablementConfigurationGlobal(self, ):
        """Retrieve the global enablement configuration for execution, applicable to all root catalogs.
        
        """
        
      
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            unCatalogo.pAcquireGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
            
            aGlobalExecutionProfilingEnablementConfiguration = TRACatalogo_Globales.gTRAExecutionProfilingEnablementConfigurationGlobal
            if not aGlobalExecutionProfilingEnablementConfiguration:
                aGlobalExecutionProfilingEnablementConfiguration = self.fNewVoidExecutionProfilingEnablementConfiguration()
                aGlobalExecutionProfilingEnablementConfiguration[ 'root_path'] = cTRAExecutionProfilingEnablementConfiguration_Global          

                TRACatalogo_Globales.gTRAExecutionProfilingEnablementConfigurationGlobal = aGlobalExecutionProfilingEnablementConfiguration.copy()
            
            aGlobalExecutionProfilingEnablementConfigurationCopy = aGlobalExecutionProfilingEnablementConfiguration.copy()
            
            return aGlobalExecutionProfilingEnablementConfigurationCopy
            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            unCatalogo.pReleaseGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        return self
            
        
        

       
    
    security.declarePrivate( 'fExecutionProfilingEnablementConfigurationFromPersistentRoot')
    def fExecutionProfilingEnablementConfigurationFromPersistentRoot(self, ):
        """Retrieve the enablement configuration for execution profiling from fields in the root catalog.
        
        """
        
        unCatalogo = self.getCatalogo()
        if unCatalogo == None:
            return None
        
        unPathDelRaiz = unCatalogo.fPathDelRaiz()
        if not unPathDelRaiz:
            return None
                
        
        anExecutionProfilingEnablementConfigurationForRoot = self.fNewVoidExecutionProfilingEnablementConfiguration()
        anExecutionProfilingEnablementConfigurationForRoot.update( {
            'root_path':                             unPathDelRaiz,          
            'execution_profiling_enabled':           unCatalogo.getPerfilDeEjecucionHabilitado(),
            'execution_timestamping_enabled':        unCatalogo.getTiemposDeEjecucionHabilitado(),
            'execution_auto_root_record_enabled':    unCatalogo.getRegistroRaizDeEjecucionAutomaticoHabilitado(),
            'execution_logging_enabled':             unCatalogo.getEscrituraEnDiscoDeRegistroDeEjecucionHabilitado(),
            'execution_logging_detailed_enabled':    unCatalogo.getEscrituraEnDiscoDeRegistroDeEjecucionDetalladoHabilitado(),
            'execution_rendering_enabled':           unCatalogo.getPresentacionEnPaginasDeRegistroDeEjecucionHabilitado(),
            'timestamp_rendering_enabled':           unCatalogo.getPresentacionEnPaginasDeTiempoDeEjecucionHabilitado(),
        })

        return anExecutionProfilingEnablementConfigurationForRoot
          
    
    
    
    
    
    
 

    # ######################################################################
    """METHODS: Time Profiling
    
    """
      
    
    security.declarePublic( 'fStartExecution')    
    def fStartExecution( self, 
        theExecutedKind, 
        theExecutedName, 
        theParentExecutionRecord=None, 
        theIsRoot               =False, 
        theProfilingConfig      ={},
        theExtraExecutionInfo   =''):
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None

        anExecutionProfilingEnablementConfiguration = None
        
        if theParentExecutionRecord:
            anExecutionProfilingEnablementConfiguration = theParentExecutionRecord.vEnablementConfiguration
            
        else:
            anExecutionProfilingEnablementConfiguration = self.fExecutionProfilingEnablementConfigurationForRoot()
            if not anExecutionProfilingEnablementConfiguration:
                return None
            
            if not theIsRoot:
                return None
            
            if not anExecutionProfilingEnablementConfiguration.get( 'execution_auto_root_record_enabled', False):
                return None
            

        if not anExecutionProfilingEnablementConfiguration:
            return None
        
        unExecutionRecord = TRAExecutionRecord( 
            anExecutionProfilingEnablementConfiguration,
            self, 
            theExecutedKind             =theExecutedKind, 
            theExecutedName             =theExecutedName, 
            theParentExecutionRecord    =theParentExecutionRecord, 
            theProfilingConfig          =theProfilingConfig, 
            theExtraExecutionInfo       =theExtraExecutionInfo
        )
        if not unExecutionRecord or unExecutionRecord.vIsExcluded:
            return None
        
        return unExecutionRecord
     
    
    
    
    
    
    security.declarePublic( 'pEndExecution')    
    def pEndExecution( self, theExecutionRecord):
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        if not theExecutionRecord:
            return self
        return theExecutionRecord.pEndExecution()
      
    
    
    
    
    
    security.declarePublic( 'pLogPerformance')    
    def pLogPerformance(self, theExecutionRecord):
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        if not theExecutionRecord:
            return self
        return theExecutionRecord.pLogPerformance()
        

    
    
    
    security.declarePublic( 'fPrintExecutionRecordString')    
    def fPrintExecutionRecordString(self, theExecutionRecord):
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        if not theExecutionRecord:
            return self
        return theExecutionRecord.fPrintExecutionRecordString()
      
    
    
        
    security.declarePublic( 'fPrintExecutionRecordStringDots')    
    def fPrintExecutionRecordStringDots(self, theExecutionRecord):
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        if not theExecutionRecord:
            return self
        return theExecutionRecord.fPrintExecutionRecordStringDots()
      
    
    
    
    security.declarePublic( 'fPrintExecutionRecordStringDetails')    
    def fPrintExecutionRecordStringDetails(self, theExecutionRecord):
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        if not theExecutionRecord:
            return self
        return theExecutionRecord.fPrintExecutionRecordStringDetails()      
    
    
    
    
    
    security.declarePublic( 'fPrintExecutionRecordStringDots_HTML')    
    def fPrintExecutionRecordStringDots_HTML(self, theExecutionRecord):
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        if not theExecutionRecord:
            return self
        return theExecutionRecord.fPrintExecutionRecordStringDots_HTML()      
    
        
    
    
    
    security.declarePublic( 'fPrintExecutionRecordStringDetails_HTML')    
    def fPrintExecutionRecordStringDetails_HTML(self, theExecutionRecord):
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        if not theExecutionRecord:
            return self
        return theExecutionRecord.fPrintExecutionRecordStringDetails_HTML()      
    
    
    
    
  
    security.declarePublic( 'pClearLoggedAll')    
    def pClearLoggedAll(self, theExecutionRecord):
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        if not theExecutionRecord:
            return self
        return theExecutionRecord.pClearLoggedAll()      
        
        
        
        
    

    security.declarePublic( 'fCGIescape')
    def fCGIescape(self, theString, quote=1):
        if not theString:
            return ''
        return cgi.escape( theString, quote=quote)
    
    
        


    
    security.declarePrivate( 'fPrettyPrintProfilingResultHTML')
    def fPrettyPrintProfilingResultHTML(self, theProfilingResult):
        """Rendering as HTML of OLD STYLE of Time Profiling  (still used in ModelDDvlPlone)

        """
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        
        if not theProfilingResult:
            return ''
    
        aResult = self.fPrettyPrintProfilingResult( theProfilingResult)
        if not aResult:
            return ''
        return self.fText2HTML( aResult)
    

        
        
        
    security.declarePrivate( 'fPrettyPrintProfilingResult')
    def fPrettyPrintProfilingResult(self, theProfilingResult):
        """Rendering as plain text of OLD STYLE of Time Profiling  (still used in ModelDDvlPlone)

        """
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        
        if not theProfilingResult:
            return ''

        anOutput = StringIO()
        
        self.pPrettyPrintProfilingResult( anOutput, theProfilingResult, 0)
        aResult = anOutput.getvalue()
        
        return aResult
 
 
        

        
        

    security.declarePrivate( 'pPrettyPrintProfilingResult')
    def pPrettyPrintProfilingResult(self, theOutput, theProfilingResult, theIndentLevel, theMaxTimeWidth=0):
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        if not theProfilingResult:
            return self
            
        if theIndentLevel:
            theOutput.write(  cIndent *  theIndentLevel)
                    
        unMethodName    = theProfilingResult[ 0]
        unExecTime      = theProfilingResult[ 1]
        someSubResults  = theProfilingResult[ 2]

        unTimeFiller = ''
        unaLenTime = len( str( unExecTime))
        if unaLenTime < theMaxTimeWidth:
            unTimeFiller = ' ' * ( theMaxTimeWidth - unaLenTime)
            
        if not someSubResults:
            theOutput.write( '[%s%d %s]\n' % ( unTimeFiller, unExecTime, unMethodName))            
        else:
            theOutput.write( '[%s%d %s\n' % ( unTimeFiller, unExecTime, unMethodName)) 
            
            unosSubTiempos = [ unSub[ 1] for unSub in someSubResults]
            unaSumaTiempos = sum( unosSubTiempos)
            unMaxSubTiempo = max( [ ( unExecTime - unaSumaTiempos) > 0,] + unosSubTiempos)
            
            if unaSumaTiempos < unExecTime:
                if theIndentLevel:
                    theOutput.write(  cIndent *  ( theIndentLevel + 1))
                theOutput.write( ' %s%d -own-\n' % ( ' ' * ( theMaxTimeWidth - len( str( unExecTime - unaSumaTiempos))), unExecTime - unaSumaTiempos))            
             
            for aSubProfilingResult in someSubResults:                       
                self.pPrettyPrintProfilingResult( theOutput, aSubProfilingResult, theIndentLevel + 1, len( str( unMaxSubTiempo)))
                
            if theIndentLevel:
                theOutput.write(  cIndent *  theIndentLevel)
            theOutput.write( ']\n')            
        
        return self      
       
               
                     
         
    
 

    

       

            
# ########################################################################################################
            
class TRAExecutionRecord:
    """Record the execution of each relevant template or method.
        
    """
    
    def __init__( self,
        theEnablementConfiguration,
        theContextualObject, 
        theExecutedKind, 
        theExecutedName, 
        theParentExecutionRecord, 
        theProfilingConfig={}, 
        theExtraExecutionInfo=''):
        
        self.vEnablementConfiguration = theEnablementConfiguration
        self.vInitialized           = False
        self.vIsExcluded            = False
        self.vExtraExecutionInfo    = None
        self.vContextualObject      = None
        self.vContextualObjectClassName = None
        self.vContextualObjectPath = None
        self.vContextualObjectTitle = None
        self.vExecutedKind          = None
        self.vExecutedName          = None
        self.vDetailLevel           = None
        self.vExecutionStartTime    = None
        self.vExecutionEndTime      = None
        self.vParent                = None
        
        self.vChildren              = None
        self.vProfilingConfig       = None
        self.vExceptions            = None
        self.vLogged                = False
        self.vExceptionsInChildren  = False
        
        
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
                
        
        try:
            if self.vEnablementConfiguration.get( 'execution_profiling_enabled', False) or self.vEnablementConfiguration.get( 'execution_timestamping_enabled', False):
                
                self.vInitialized           = True

                self.vIsExcluded            = False
                
                self.vExtraExecutionInfo    = []
                if theExtraExecutionInfo:
                    self.vExtraExecutionInfo.append( str( theExtraExecutionInfo))
                
                self.vContextualObject      = theContextualObject
                if not ( theContextualObject == None):
                    self.vContextualObjectClassName = theContextualObject.__class__.__name__
                    self.vContextualObjectPath      = theContextualObject.fDisplayPathString()
                    try:
                        self.vContextualObjectTitle = theContextualObject.Title()
                    except:
                        None
                else:
                    self.vContextualObjectClassName = 'unknown contextual object'
                    self.vContextualObjectPath      = 'unknown contextual object'
                    self.vContextualObjectTitle     = 'unknown contextual object'
                    
                self.vExecutedKind          = '' # method or template
                self.vExecutedName          = ''
                self.vDetailLevel           = -1
                self.vExecutionStartTime    = 0
                self.vExecutionEndTime      = 0
                self.vParent                = None
                
                self.vChildren              = [ ]
                self.vProfilingConfig       = { }
                self.vExceptions            = [ ]
                self.vLogged                = False
                self.vExceptionsInChildren  = False


            if self.vEnablementConfiguration.get( 'execution_timestamping_enabled', False):
                self.vExecutionStartTime    = int( time.time() * 1000)
            
            if self.vEnablementConfiguration.get( 'execution_profiling_enabled', False):
                
                if not theParentExecutionRecord or not theParentExecutionRecord.vIsExcluded:
                    
                    if theExecutedName in self.vProfilingConfig.get( 'excluded', []):
                        self.vIsExcluded = True       
                    else:
                        if theParentExecutionRecord:
                            aIsExecutionRecord = False
                            try:
                                aIsExecutionRecord = theParentExecutionRecord.fIsExecutionRecord()                            
                            except:
                                None
                                
                            if aIsExecutionRecord:
                                theParentExecutionRecord.addChild( self)
                                if ( theParentExecutionRecord.vProfilingConfig or {}).get( 'log_what', ''):
                                    self.vProfilingConfig[ 'log_what'] =  theParentExecutionRecord.vProfilingConfig[ 'log_what']   
                            
                        self.vExecutedKind          = theExecutedKind
                        self.vExecutedName          = theExecutedName
                        
                        if theProfilingConfig and ( theProfilingConfig.__class__.__name__ == 'dict'):
                            self.vProfilingConfig.update( theProfilingConfig)
                                 
            return None
        
        except:
            None
    

            
            
            
            
    def fIsExecutionRecord( self,):
        return True
    
    
    
    
    def addExtraInfo( self, theExtraExecutionInfo):
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        if not self.vInitialized or not theExtraExecutionInfo:
            return self
        
        if self.vExtraExecutionInfo == None:
            self.vExtraExecutionInfo = [ ]
        
        self.vExtraExecutionInfo.append( theExtraExecutionInfo)
        
        return self 
    

    
    
    def addChild( self, theChild):
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        if not self.vInitialized or not theChild:
            return self
        
        if self.vChildren == None:
            self.vChildren = [ ]
        
        self.vChildren.append( theChild)
        theChild.vParent = self
        
        return self
    
        
        

    
        
    def pEndExecution( self,  ):
        """Pop stack and write log.
        """
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        
        try:
            if not self.vInitialized:
                return self
            
            if  self.vEnablementConfiguration.get( 'execution_timestamping_enabled', False):
                self.vExecutionEndTime  =  int( time.time() * 1000)
            
            if  self.vEnablementConfiguration.get( 'execution_profiling_enabled', False):
                self.pLogPerformance( )
                    
            return self   
        
        except:
            None


    def pRecordExceptionInChildren( self):
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        self.vExceptionsInChildren = True
        if self.vParent:
            self.vParent.pRecordExceptionInChildren()
        return self
    
        
    
    
    def pRecordException( self,  theExceptionReport):
        """Record an exception report trapped in this execution.
        """
        
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        try:
            
            if self.vParent:
                self.vParent.pRecordExceptionInChildren()
            
            if not theExceptionReport:
                return None
            
            if not self.vExceptions:
                self.vExceptions = [ ]
                
            self.vExceptions.append( theExceptionReport)
            
            return self   
        
        except:
            None
          
        return self
    
    
            
          
    def pLogPerformance( self, ):
        """Write to the log a representation of this ExecutionRecord and its children.
        
        theWhenToLog optional values in [
            None or False == do not log,
            True == log now,
            'root' == log if element has no parent
        ]
        
        """
        
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        try:
            if not self.vInitialized:
                return self
            
            unPrintString          = ''
            unTimestampPrintString = ''
            unLogPrintString       = ''
            
            if self.vEnablementConfiguration.get( 'execution_profiling_enabled', False):
                
                if self.vEnablementConfiguration.get( 'execution_timestamping_enabled', False):
                    aWhenToLog = self.vProfilingConfig.get( 'log_when', False)
                    if aWhenToLog == True or ( ( aWhenToLog == 'root') and not self.vParent):
                        unTimestampPrintString = self.fPrintExecutionTimestampString( )
                    
                    
                    
                if self.vEnablementConfiguration.get( 'execution_logging_enabled', False):
                    
                    aWhenToLog = self.vProfilingConfig.get( 'log_when', False)
                    if aWhenToLog == True or ( ( aWhenToLog == 'root') and not self.vParent):
                        
                        if self.vProfilingConfig.get( 'log_what', '') == 'details' and self.vEnablementConfiguration.get( 'execution_logging_detailed_enabled', False):
                            unLogPrintString = self.fPrintExecutionRecordStringDetails( True)
                            
                        elif self.vEnablementConfiguration.get( 'execution_logging_detailed_enabled', False) and self.vProfilingConfig.get( 'log_what', '') == 'dots':
                            unLogPrintString = self.fPrintExecutionRecordStringDots( True)
                            
                        else:
                            unLogPrintString = self.fPrintExecutionRecordString( )
        

                if unTimestampPrintString and unLogPrintString:
                    unPrintString = '\n%s\%s' %  ( unTimestampPrintString, unLogPrintString,)
                    
                elif unTimestampPrintString:
                    unPrintString = unTimestampPrintString
                    
                elif unLogPrintString:
                    unPrintString = unLogPrintString
                    
                    
                    
            if unPrintString:       
                unEncodedString = self.vContextualObject.fEncodeLogString( unPrintString)
                logging.getLogger( 'gvSIGi18n').info( unEncodedString)
                
                self.setLoggedRecursive( True)
                        
    
            return self
        
        except:
            None

    
    

    
    
    
    
    
    
    def setLoggedRecursive( self, theLogged=True):

        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        try:
            if not self.vInitialized:
                return self
            
            if self.vLogged:
                return self
            
            self.vLogged = theLogged == True
            for unChild in ( self.vChildren or []):
                unChild.setLoggedRecursive( theLogged == True)
            
            return self
        
        except:
            None

    
        
    
    
    def pClearLoggedAll( self,):

        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        try:
            if not self.vInitialized:
                return self
            
            self.vLogged = False
            for unChild in ( self.vChildren or []):
                unChild.pClearLoggedAll( )
            
            return self
        
        except:
            None

    

    def fPrintExecutionTimestampString( self,):
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        try:
            if self.vInitialized:
                return '%d ms (start %s  -  end %s) %s %s %s %s %s' % (      
                    self.vExecutionEndTime - self.vExecutionStartTime,
                    self.vContextualObject.fDateTimeFromMillisecondsTextual( self.vExecutionStartTime),
                    self.vContextualObject.fDateTimeFromMillisecondsTextual( self.vExecutionEndTime),                    
                    self.vExecutedKind or '', 
                    self.vExecutedName or '', 
                    self.vContextualObjectClassName or '',
                    self.vContextualObjectTitle or '',
                    self.vContextualObjectPath   or '',
                )
        except:
            return 'exception printing execution timestamp'
        
        return ''
    
    
    
    

    def fPrintExecutionRecordString(self, ):

        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        try:
            if self.vInitialized:
                return '%d ms  (start %s end %s) %s %s %s %s %s %s %s' % (      
                    self.vExecutionEndTime - self.vExecutionStartTime, 
                    self.vContextualObject.fDateTimeFromMillisecondsTextual( self.vExecutionStartTime),
                    self.vContextualObject.fDateTimeFromMillisecondsTextual( self.vExecutionEndTime),                    
                    ( self.vExceptions and '!!!') or '',
                    self.vExecutedKind or 'unknown_executed_kind', 
                    self.vExecutedName or 'unknown_executed_name', 
                    self.vContextualObjectClassName or 'unknown_object_class_name',
                    self.vContextualObjectTitle or 'unknown_object_title',
                    self.vContextualObjectPath   or 'unknown_object_path',
                    ' '.join( self.vExtraExecutionInfo or []),
                )
        except:
            return 'exception printing execution record'
    
        return ''
            

    
    def fPrintExecutionRecordStringDots(self,):

        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        try:
            if not self.vInitialized:
                return self
            
            theOutput = StringIO()
            
            self.pPrintExecutionRecordDotsOn( theOutput,)
       
            unString = theOutput.getvalue()
            return unString
        
        except:
            None

        return ''
    
    
    
    
    def fPrintExecutionRecordStringDetails(self, theIsForLog=False):

        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        try:
            if not self.vInitialized:
                return self
            
            theOutput = StringIO()
            
            unaTimeWidth = len( str( ( self.vExecutionEndTime or  self.vExecutionStartTime) - self.vExecutionStartTime))
            self.pPrintExecutionRecordDetailsOn( theOutput, theIsForLog, '', unaTimeWidth)
       
            unString = theOutput.getvalue()
            return unString
        
        except:
            None

        return '' 
            

            
      
    
    

    def pPrintExecutionRecordDotsOn(self, theOutput):
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        if not self.vInitialized:
            return self
        
        theOutput.write( '.')
        for unChild in ( self.vChildren or []):
            unChild.pPrintExecutionRecordDotsOn( theOutput)
        return self      
       
    
              
            
            
                 
    
    def pPrintExecutionRecordDetailsOn(self, theOutput,  theIsForLog=False, theIndentString='', theMaxTimeWidth=0):
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        if not self.vInitialized:
            return self
        
        if theIsForLog and self.vLogged:
            return self
       
        if theIndentString:
            theOutput.write(  theIndentString)
        
            
        unExecutedKind    = self.vExecutedKind or 'unknown_executed_kind'
        unExecutedName    = self.vExecutedName or 'unknown_executed_name'
        unExecTime        = self.vExecutionEndTime - self.vExecutionStartTime
        someSubResults    = self.vChildren or []

        unTimeFiller = ' ' * ( theMaxTimeWidth - len( str( unExecTime)))
            
        if not someSubResults:
            if not self.vExceptions:
                theOutput.write( '[%s%s]\n' % ( unTimeFiller, self.fPrintExecutionRecordString())) 
            else:
                theOutput.write( '[%s%s\n' % ( unTimeFiller, self.fPrintExecutionRecordString())) 
                for unaException in self.vExceptions:
                    theOutput.write( '%s%s%s\n' % ( theIndentString, str( unaException))) 
                    
                
        else:
            theOutput.write( '[%s%s\n' % ( unTimeFiller, self.fPrintExecutionRecordString()))     
            
            if self.vExceptions:
                for unaException in self.vExceptions:
                    theOutput.write( '%s%s%s\n' % ( theIndentString, str( unaException))) 
                
            
            unAllChildrenAlreadyLogged = len( [ aChild for aChild in someSubResults if aChild.vLogged ]) == len( someSubResults)
            
            if unAllChildrenAlreadyLogged:
                theOutput.write( "Children already logged before")
                
            unosSubTiempos = [ unSub.vExecutionEndTime - unSub.vExecutionStartTime for unSub in someSubResults]
            unaSumaTiempos = sum( unosSubTiempos)
            unMaxSubTiempo = max( [ ( unExecTime - unaSumaTiempos),] + unosSubTiempos)
            unaLenSubTiempos = len( str( unMaxSubTiempo))
            
            unIndentString = theIndentString + ( ' ' * ( theMaxTimeWidth + 1))

            if unaSumaTiempos < unExecTime:
                theOutput.write(  unIndentString)
                unOwnTimeFiller = ' ' * (( theMaxTimeWidth - len( str( unExecTime - unaSumaTiempos))) + 1)
                theOutput.write( '%s%d ms -own-\n' % ( unOwnTimeFiller, unExecTime - unaSumaTiempos))            
                         
            for aSubProfilingResult in someSubResults:                       
                aSubProfilingResult.pPrintExecutionRecordDetailsOn( theOutput, theIsForLog, unIndentString, unaLenSubTiempos)
                
            if theIndentString:
                theOutput.write(  theIndentString)
            theOutput.write( ']\n')            
        
        return self      
       
               
                     


 
            
     