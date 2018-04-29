# -*- coding: utf-8 -*-
#
# File: TRAElemento_Profiling.py
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


import cgi
import logging

import time  


from StringIO                   import StringIO

from AccessControl              import ClassSecurityInfo


from Products.CMFCore           import permissions


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

from TRACatalogo_Globales import TRACatalogo_Globales

from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_ConfigureExecutionProfilingEnablement_Global, cUseCase_ConfigureExecutionProfilingEnablement_TRACatalogo
            
from TRAExecutionRecord import TRAExecutionRecord

            


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
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
            
            
            
            try: 
                
                unCatalogoRaiz = self.getCatalogo()
                if unCatalogoRaiz == None:
                    return unResult
                
                unaConfiguracion = unCatalogo.fObtenerConfiguracion( cTRAConfiguracionAspecto_PerfilEjecucion)
                if unaConfiguracion == None:
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
                                unaConfiguracion.setPerfilDeEjecucionHabilitado( aNewValue)
                                
                            elif aConfigurationPropertyName == 'execution_timestamping_enabled':
                                unaConfiguracion.setTiemposDeEjecucionHabilitado( aNewValue)
                                
                            elif aConfigurationPropertyName == 'execution_auto_root_record_enabled':
                                unaConfiguracion.setRegistroRaizDeEjecucionAutomaticoHabilitado( aNewValue)
                                
                            elif aConfigurationPropertyName == 'execution_logging_enabled':
                                unaConfiguracion.setEscrituraEnDiscoDeRegistroDeEjecucionHabilitado( aNewValue)
                                
                            elif aConfigurationPropertyName == 'execution_logging_detailed_enabled':    
                                unaConfiguracion.setEscrituraEnDiscoDeRegistroDeEjecucionDetalladoHabilitado( aNewValue)
                                
                            elif aConfigurationPropertyName == 'execution_rendering_enabled':           
                                unaConfiguracion.setPresentacionEnPaginasDeRegistroDeEjecucionHabilitado( aNewValue)
                                
                            elif aConfigurationPropertyName == 'timestamp_rendering_enabled':           
                                unaConfiguracion.setPresentacionEnPaginasDeTiempoDeEjecucionHabilitado( aNewValue),
                
                                
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
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
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
                anExecutionProfilingEnablementConfigurationForRoot[ 'execution_profiling_enabled'] = anExecutionProfilingEnablementConfigurationForRoot.get( 'execution_profiling_enabled', False)

            if anExecutionProfilingEnablementConfiguration.get( 'execution_timestamping_enabled', False):                
                anExecutionProfilingEnablementConfigurationForRoot[ 'execution_timestamping_enabled'] = anExecutionProfilingEnablementConfigurationForRoot.get( 'execution_timestamping_enabled', False)
            
            if anExecutionProfilingEnablementConfiguration.get( 'execution_auto_root_record_enabled', False):                
                anExecutionProfilingEnablementConfigurationForRoot[ 'execution_auto_root_record_enabled'] = anExecutionProfilingEnablementConfigurationForRoot.get( 'execution_auto_root_record_enabled', False)
            
            if anExecutionProfilingEnablementConfiguration.get( 'execution_logging_enabled', False):                
                anExecutionProfilingEnablementConfigurationForRoot[ 'execution_logging_enabled'] = anExecutionProfilingEnablementConfigurationForRoot.get( 'execution_logging_enabled', False)

            if anExecutionProfilingEnablementConfiguration.get( 'execution_logging_detailed_enabled', False):                
                anExecutionProfilingEnablementConfigurationForRoot[ 'execution_logging_detailed_enabled'] = anExecutionProfilingEnablementConfigurationForRoot.get( 'execution_logging_detailed_enabled', False)
            
            if anExecutionProfilingEnablementConfiguration.get( 'execution_rendering_enabled', False):                
                anExecutionProfilingEnablementConfigurationForRoot[ 'execution_rendering_enabled'] = anExecutionProfilingEnablementConfigurationForRoot.get( 'execution_rendering_enabled', False)
            
            if anExecutionProfilingEnablementConfiguration.get( 'timestamp_rendering_enabled', False):                
                anExecutionProfilingEnablementConfigurationForRoot[ 'timestamp_rendering_enabled'] = anExecutionProfilingEnablementConfigurationForRoot.get( 'timestamp_rendering_enabled', False)
                
                
            
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
        anExecutionProfilingEnablementConfigurationForRoot = self.fNewVoidExecutionProfilingEnablementConfiguration()
        
        unCatalogo = self.getCatalogo()
        if unCatalogo == None:
            return anExecutionProfilingEnablementConfigurationForRoot
        
        unaConfiguracion = unCatalogo.fObtenerConfiguracion( cTRAConfiguracionAspecto_PerfilEjecucion)
        if unaConfiguracion == None:
            return anExecutionProfilingEnablementConfigurationForRoot
        
        
        unPathDelRaiz = unCatalogo.fPathDelRaiz()
        if not unPathDelRaiz:
            return anExecutionProfilingEnablementConfigurationForRoot
                
        
        anExecutionProfilingEnablementConfigurationForRoot.update( {
            'root_path':                             unPathDelRaiz,          
            'execution_profiling_enabled':           unaConfiguracion.getPerfilDeEjecucionHabilitado(),
            'execution_timestamping_enabled':        unaConfiguracion.getTiemposDeEjecucionHabilitado(),
            'execution_auto_root_record_enabled':    unaConfiguracion.getRegistroRaizDeEjecucionAutomaticoHabilitado(),
            'execution_logging_enabled':             unaConfiguracion.getEscrituraEnDiscoDeRegistroDeEjecucionHabilitado(),
            'execution_logging_detailed_enabled':    unaConfiguracion.getEscrituraEnDiscoDeRegistroDeEjecucionDetalladoHabilitado(),
            'execution_rendering_enabled':           unaConfiguracion.getPresentacionEnPaginasDeRegistroDeEjecucionHabilitado(),
            'timestamp_rendering_enabled':           unaConfiguracion.getPresentacionEnPaginasDeTiempoDeEjecucionHabilitado(),
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
        """A new execution context is created. If so configured and allowed, Instantiate a new record to manage the execution of the current context .
        
        """
        
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
        """The current execution context is about to be exited.
        
        """
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
       
               
                     
         
    
 

    
            
     