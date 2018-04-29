# -*- coding: utf-8 -*-
#
# File: TRACatalogo_Globales.py
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

import threading

from AccessControl                  import ClassSecurityInfo

from Products.CMFCore               import permissions


from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fMillisecondsNow


from TRAElemento_Constants import *






class TRACatalogo_Globales:
    """
    """
    security = ClassSecurityInfo()

    
    
    
    # #######################################################
    """To control logging of execution profiling. 
    Maintained through templates to change the enablemente state.
    Not maintained through thread-safe critical sections (this is not so critical)
    
    """

    gTRAExecutionLoggingEnabled         = cExecutionLoggingEnabled
    gTRADetailedExecutionLoggingEnabled = cDetailedExecutionLoggingEnabled
    gTRAAllowRootProfileExecution       = cAllowRootProfileExecution

 
    
    

    
    
    # #######################################################
    """To enforce Exclusive access to globals
    
    """
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    gTRACatalogoGlobalesMutex = threading.Lock()
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 
    
    
    
    # #######################################################
    """Globals
    
    """


    # #######################################################
    """For each TRACatalogo root path, holds the milliseconds of the last time the Status Report by Languages was generated.
    
    """
    
    gStatusReportByLanguagesTimeMillis           = { }
    gStatusReportByModulesAndLanguagesTimeMillis = { }
    

    # #######################################################
    """For each TRACatalogo root path, holds the number of Translation status changes since the last time the Status Report by Languages was generated.
    
    """
    gNumTranslationsStatusChangesSinceReportByLanguages             = { }
    gNumTranslationsStatusChangesSinceReportByModulesAndLanguages   = { }

    
    
    # #######################################################
    """For each TRACatalogo root path, holds information about the recent Translation status changes: time, language, user, symbol, change kind, new status.
    
    """
    gRecentTranslationsChanges             = { }
    
    
        
    


    
    # #######################################################
    # #######################################################
 
    
    
   
    security.declarePublic( 'fIsExecutionLoggingEnabled')
    def fIsExecutionLoggingEnabled(self,):
       
        return TRACatalogo_Globales.gTRAExecutionLoggingEnabled

    

   
    
    
    security.declareProtected( permissions.ManagePortal, 'pExecutionLogging_Enable')
    def pExecutionLogging_Enable(self,):
       
        TRACatalogo_Globales.gTRAExecutionLoggingEnabled = True
        return self
    
    

    
    
    
    security.declareProtected( permissions.ManagePortal, 'pExecutionLogging_Disable')
    def pExecutionLogging_Disable(self,):
       
        TRACatalogo_Globales.gTRAExecutionLoggingEnabled = False
        return self
    
    

     
  
    # #######################################################
    # #######################################################
 
    
    
   
    security.declarePublic( 'fIsDetailedExecutionLoggingEnabled')
    def fIsDetailedExecutionLoggingEnabled(self,):
       
        return TRACatalogo_Globales.gTRADetailedExecutionLoggingEnabled

    

   
    
    
    security.declareProtected( permissions.ManagePortal, 'pDetailedExecutionLogging_Enable')
    def pDetailedExecutionLogging_Enable(self,):
       
        TRACatalogo_Globales.gTRADetailedExecutionLoggingEnabled = True
        return self
    
    

    
    
    
    security.declareProtected( permissions.ManagePortal, 'pDetailedExecutionLogging_Disable')
    def pDetailedExecutionLogging_Disable(self,):
       
        TRACatalogo_Globales.gTRADetailedExecutionLoggingEnabled = False
        return self
    
    

         


    
    # #######################################################
    # #######################################################
 
    
    
   
    security.declarePublic( 'fIsRootProfileExecutionAllowed')
    def fIsRootProfileExecutionAllowed(self,):
       
        return TRACatalogo_Globales.gTRAAllowRootProfileExecution

    

   
    
    
    security.declareProtected( permissions.ManagePortal, 'pRootProfileExecution_Allow')
    def pRootProfileExecution_Allow(self,):
       
        TRACatalogo_Globales.gTRAAllowRootProfileExecution = True
        return self
    
    

    
    
    
    security.declareProtected( permissions.ManagePortal, 'pRootProfileExecution_Disallow')
    def pRootProfileExecution_Disallow(self,):
       
        TRACatalogo_Globales.gTRAAllowRootProfileExecution = False
        return self
    
    
    
    
    
    
    # #######################################################
    # #######################################################

   
    
 

 
   
    security.declarePrivate( 'pAcquireGlobalsLock')
    def pAcquireGlobalsLock(self,):
        """Reserve or release access to Globals and Globals control, by acquiring and releasing a lock on a mutual exclussion (mutex) semaphore, held here to protect critical sections and make them thread-safe.
        
        """
        
        # #################
        """MUTEX LOCK. 
        
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        TRACatalogo_Globales.gTRACatalogoGlobalesMutex.acquire()
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return self
    



    
    security.declarePrivate( 'pReleaseGlobalsLock')
    def pReleaseGlobalsLock(self, ):


        # #################
        """MUTEX UNLOCK. 
        
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        TRACatalogo_Globales.gTRACatalogoGlobalesMutex.release()
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return self
    

   

    
    # #######################################################
    # #######################################################
    
    # #######################################################
    # #######################################################



       
    
    security.declarePrivate( 'pTranslationHasChanged')
    def pTranslationHasChanged(self, theTranslationChange):
        """Record recent change, and increment the counter of changes since last generation of the Status Report by Languages.
        
        """
        
        
        unPathDelRaiz = self.fPathDelRaiz()
        if not unPathDelRaiz:
            return self
        
        if theTranslationChange:
            aTranslationChange = theTranslationChange.copy()
        else:
            aTranslationChange = { }
            
        aTranslationChange[ 'path_del_raiz'] = unPathDelRaiz
        
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
            
            
            
            # ####################################################################
            """Append change to the list of recent changes, discarding the oldest ones if the maximum is exceeded. 
            
            """
            if TRACatalogo_Globales.gRecentTranslationsChanges == None:
                TRACatalogo_Globales.gRecentTranslationsChanges = { }
                
            unosRecentTranslationChangesForRoot = TRACatalogo_Globales.gRecentTranslationsChanges.get( unPathDelRaiz, None)
            if unosRecentTranslationChangesForRoot == None:
                unosRecentTranslationChangesForRoot = [ ]
                TRACatalogo_Globales.gRecentTranslationsChanges[ unPathDelRaiz] = unosRecentTranslationChangesForRoot
                
            unMaxRecentTranslationChangesForRoot = self.getMaximoNumeroCambiosRecientes()
            if unMaxRecentTranslationChangesForRoot:
                if len( unosRecentTranslationChangesForRoot) > unMaxRecentTranslationChangesForRoot:
                    unosRecentTranslationChangesForRoot.remove( unosRecentTranslationChangesForRoot[ 0])
                    
            unosRecentTranslationChangesForRoot.append( aTranslationChange)
            
            
            
            
                        
            # ####################################################################
            """Increment the counter of changes since the last time the status report by languages, and by modules and languages were generated. 
            
            """
            
            if TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByLanguages == None:
                TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByLanguages = { }
                
            unNumTranslationsStatusChangesForRoot = TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByLanguages.get( unPathDelRaiz, None)
            if unNumTranslationsStatusChangesForRoot == None:
                unNumTranslationsStatusChangesForRoot = 0
                
            unNumTranslationsStatusChangesForRoot += 1
            TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByLanguages[ unPathDelRaiz] = unNumTranslationsStatusChangesForRoot
                  
            
            if TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByModulesAndLanguages == None:
                TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByModulesAndLanguages = { }
                
            unNumTranslationsStatusChangesForRoot = TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByModulesAndLanguages.get( unPathDelRaiz, None)
            if unNumTranslationsStatusChangesForRoot == None:
                unNumTranslationsStatusChangesForRoot = 0
                
            unNumTranslationsStatusChangesForRoot += 1
            TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByModulesAndLanguages[ unPathDelRaiz] = unNumTranslationsStatusChangesForRoot
            
            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        return self
            
    
    
        

      
    security.declareProtected( permissions.View, 'fNewVoidReportInvalidateObsoleteStatusReports')
    def fNewVoidReportInvalidateObsoleteStatusReports( self,):
        aReport = {
            'invalidated':        False,
            'path_del_raiz':      '',
            'changes_recorded':   0,
            'changes_threshold': -1,
            'seconds_lapsed':     0,
            'seconds_threshold': -1,
        }
        return aReport
        
            
       
    
    security.declarePrivate( 'fInvalidateObsoleteStatusReportByLanguages')
    def fInvalidateObsoleteStatusReportByLanguages(self, ):
        """If the Status Report by Languages is too old, or enough changes have been applied to translations in the catalog, invalidate the status report by languages for the catalog.
        
        """
        
        aReport = self.fNewVoidReportInvalidateObsoleteStatusReports()
        
        unPathDelRaiz = self.fPathDelRaiz()
        if not unPathDelRaiz:
            return aReport        
        aReport[ 'path_del_raiz'] = unPathDelRaiz
        
        
        unMustInvalidate              = False
        unVoteMustInvalidateByNumbers = False
        unVoteMustInvalidateByTime    = False
            
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
                
                       
            # ####################################################################
            """Check if the counter of changes since the last time the status report by languages was generated, is bigger than the maximum configured for the catalog. 
            
            """
            unNumeroDeCambiosAnularInformeIdiomas = self.getNumeroDeCambiosAnularInformeIdiomas()
            if not unNumeroDeCambiosAnularInformeIdiomas:
                unNumeroDeCambiosAnularInformeIdiomas = 0
                
            aReport[ 'changes_threshold'] = unNumeroDeCambiosAnularInformeIdiomas

            if TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByLanguages == None:
                TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByLanguages = { }
                
            unNumTranslationsStatusChangesForRoot = TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByLanguages.get( unPathDelRaiz, None)
            if unNumTranslationsStatusChangesForRoot == None:
                unNumTranslationsStatusChangesForRoot = 0
                
            aReport[ 'changes_recorded'] = unNumTranslationsStatusChangesForRoot
                
            if unNumTranslationsStatusChangesForRoot >= unNumeroDeCambiosAnularInformeIdiomas:
                unVoteMustInvalidateByNumbers = True
            
                        
            # ####################################################################
            """If not already decided to invalidate, and there was any change, Check if enough time has lapsed since the last time the status report by languages was generated. 
            
            """
            unSegundosMinimosRetencionInformeIdiomas = self.getSegundosMinimosRetencionInformeIdiomas()

            if not unSegundosMinimosRetencionInformeIdiomas:
                unSegundosMinimosRetencionInformeIdiomas = 0
                
            aReport[ 'seconds_threshold'] = unSegundosMinimosRetencionInformeIdiomas
                

            if TRACatalogo_Globales.gStatusReportByLanguagesTimeMillis == None:
                TRACatalogo_Globales.gStatusReportByLanguagesTimeMillis = { }
                
            unStatusReportByLanguagesTimeMillis = TRACatalogo_Globales.gStatusReportByLanguagesTimeMillis.get( unPathDelRaiz, None)
            if unStatusReportByLanguagesTimeMillis == None:
                unStatusReportByLanguagesTimeMillis = 0
                
            unosMillisecondsNow = fMillisecondsNow()
            
            unosSecondsLapsed =  int(( unosMillisecondsNow - unStatusReportByLanguagesTimeMillis) / 1000)
            aReport[ 'seconds_lapsed'] = unosSecondsLapsed

            if unosSecondsLapsed >= unSegundosMinimosRetencionInformeIdiomas:
                unVoteMustInvalidateByTime = True
                
            
            if unVoteMustInvalidateByNumbers:
                unMustInvalidate = True
            else:
                if unVoteMustInvalidateByTime and unNumTranslationsStatusChangesForRoot:
                    unMustInvalidate = True
                    
                
                
                
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            
            
        if unMustInvalidate:
            self.pFlushCachedTemplates( [ 'TRACatalogoInforme', 'TRACatalogoInforme_NoHeaderNoFooter',])
            aReport[ 'invalidated'] = True
            
        return aReport
            
    

    
    
    
    security.declarePrivate( 'pStatusReportByLanguagesJustGenerated')
    def pStatusReportByLanguagesJustGenerated(self, ):
        """Record the time now, and Reset the counter of changes since the report was generated.
        
        """
        
        
        unPathDelRaiz = self.fPathDelRaiz()
        if not unPathDelRaiz:
            return self
        
        unMustInvalidate = False
            
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
                        
            # ####################################################################
            """Record the current time as the status report generation time. 
            
            """
            if TRACatalogo_Globales.gStatusReportByLanguagesTimeMillis == None:
                TRACatalogo_Globales.gStatusReportByLanguagesTimeMillis = { }
                
            unosMillisecondsNow = fMillisecondsNow()

            TRACatalogo_Globales.gStatusReportByLanguagesTimeMillis[ unPathDelRaiz] = unosMillisecondsNow
                 
                
                
                       
            # ####################################################################
            """Reset the counter of changes since the status report was generated.
            
            """
              
            if TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByLanguages == None:
                TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByLanguages = { }
                
            TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByLanguages[ unPathDelRaiz] = 0
                
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


        return self
            
    
    
    
    
    
    
    

    
    security.declarePrivate( 'fInvalidateObsoleteStatusReportByModulesAndLanguages')
    def fInvalidateObsoleteStatusReportByModulesAndLanguages(self, ):
        """If the Status Report by Modules and Languages is too old, or enough changes have been applied to translations in the catalog, invalidate the status report by modules and languages for the catalog.
        
        """
        
        aReport = self.fNewVoidReportInvalidateObsoleteStatusReports()
        
        
        unPathDelRaiz = self.fPathDelRaiz()
        if not unPathDelRaiz:
            return aReport
        
        unMustInvalidate              = False
        unVoteMustInvalidateByNumbers = False
        unVoteMustInvalidateByTime    = False
            
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
                
                       
            # ####################################################################
            """Check if the counter of changes since the last time the status report by languages was generated, is bigger than the maximum configured for the catalog. 
            
            """
            unNumeroDeCambiosAnularInformeModulosEIdiomas = self.getNumeroDeCambiosAnularInformeModulosEIdiomas()
            if not unNumeroDeCambiosAnularInformeModulosEIdiomas:
                unNumeroDeCambiosAnularInformeModulosEIdiomas = 0

            aReport[ 'changes_threshold'] = unNumeroDeCambiosAnularInformeModulosEIdiomas
                
            if TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByModulesAndLanguages == None:
                TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByModulesAndLanguages = { }
                
            unNumTranslationsStatusChangesForRoot = TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByModulesAndLanguages.get( unPathDelRaiz, None)
            if unNumTranslationsStatusChangesForRoot == None:
                unNumTranslationsStatusChangesForRoot = 0
                
            aReport[ 'changes_recorded'] = unNumTranslationsStatusChangesForRoot
                
            if unNumTranslationsStatusChangesForRoot >= unNumeroDeCambiosAnularInformeModulosEIdiomas:
                unVoteMustInvalidateByNumbers = True
            
                        
            # ####################################################################
            """If not already decided to invalidate, and there was any change, Check if enough time has lapsed since the last time the status report by languages was generated. 
            
            """
            unSegundosMinimosRetencionInformeIdiomas = self.getSegundosMinimosRetencionInformeModulosEIdiomas()
            if not unSegundosMinimosRetencionInformeIdiomas:
                unSegundosMinimosRetencionInformeIdiomas = 0
                
            aReport[ 'seconds_threshold'] = unSegundosMinimosRetencionInformeIdiomas

            if TRACatalogo_Globales.gStatusReportByModulesAndLanguagesTimeMillis == None:
                TRACatalogo_Globales.gStatusReportByModulesAndLanguagesTimeMillis = { }
                
            unStatusReportByModulesAndLanguagesTimeMillis = TRACatalogo_Globales.gStatusReportByModulesAndLanguagesTimeMillis.get( unPathDelRaiz, None)
            if unStatusReportByModulesAndLanguagesTimeMillis == None:
                unStatusReportByModulesAndLanguagesTimeMillis = 0
                
            unosMillisecondsNow = fMillisecondsNow()
            
            unosSecondsLapsed =  int(( unosMillisecondsNow - unStatusReportByModulesAndLanguagesTimeMillis) / 1000)
            aReport[ 'seconds_lapsed'] = unosSecondsLapsed

            if unosSecondsLapsed >= unSegundosMinimosRetencionInformeIdiomas:
                unVoteMustInvalidateByTime = True
                
            
            if unVoteMustInvalidateByNumbers:
                unMustInvalidate = True
            else:
                if unVoteMustInvalidateByTime and unNumTranslationsStatusChangesForRoot:
                    unMustInvalidate = True
                    
                
                
                
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            
            
        if unMustInvalidate:
            self.pFlushCachedTemplates( [ 'TRACatalogoDetalle', 'TRACatalogoDetalle_NoHeaderNoFooter',])
            aReport[ 'invalidated'] = True
            
        return aReport
            
    

    
    
    
    security.declarePrivate( 'pStatusReportByModulesAndLanguagesJustGenerated')
    def pStatusReportByModulesAndLanguagesJustGenerated(self, ):
        """Record the time now, and Reset the counter of changes since the report was generated.
        
        """
        
        
        unPathDelRaiz = self.fPathDelRaiz()
        if not unPathDelRaiz:
            return self
        
        unMustInvalidate = False
            
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
                        
            # ####################################################################
            """Record the current time as the status report generation time. 
            
            """
            if TRACatalogo_Globales.gStatusReportByModulesAndLanguagesTimeMillis == None:
                TRACatalogo_Globales.gStatusReportByModulesAndLanguagesTimeMillis = { }
                
            unosMillisecondsNow = fMillisecondsNow()

            TRACatalogo_Globales.gStatusReportByModulesAndLanguagesTimeMillis[ unPathDelRaiz] = unosMillisecondsNow
                 
                
                
                       
            # ####################################################################
            """Reset the counter of changes since the status report was generated.
            
            """
              
            if TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByModulesAndLanguages == None:
                TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByModulesAndLanguages = { }
                
            TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByModulesAndLanguages[ unPathDelRaiz] = 0
                
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


        return self
            
    
                        
    
                    