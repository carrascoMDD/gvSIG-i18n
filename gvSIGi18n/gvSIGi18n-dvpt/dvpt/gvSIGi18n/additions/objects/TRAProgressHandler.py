# -*- coding: utf-8 -*-
#
# File: TRAProgressHandler.py
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
import transaction
import threading



from DateTime                   import DateTime

from AccessControl              import ClassSecurityInfo

from Products.Archetypes.utils  import shasattr

from Products.CMFCore           import permissions

from Products.CMFCore.utils     import getToolByName


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

    
from TRAProcessErrorException       import TRAProcessErrorException
from TRAProcessTerminationException import TRAProcessTerminationException

            
# ########################################################################################################
    
class TRAProgressHandler:
    """CLASS: manager class dealing with progress of long-lived processes .
        
    """

    
    def __init__( self, 
        theInitialElement, 
        theProgressElement, 
        theInputParameters,
        theProgressControlParameters, 
        theProgressControlCounters, 
        theResult,
        theInitializeLambda,
        theLoopLambda,
        theElementLambda,
        theElementPloneLambda,
        theFinalizeLambda,
        theLockCatalog,
        theTimestamp):
        
        
        # #######################################################
        """To enforce Exclusive access to progress handler variables
        
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.vMutex = threading.Lock()
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
         
        self.vStarted                   = False
        self.vPaused                    = False
        self.vCompleted                 = False
        self.vTerminated                = False
        
        self.vError                     = False
        self.vErrorMessage              = ''
        self.vErrorDetails              = ''
        self.vErrorTraceback            = ''
        
        self.vException                 = False
        self.vExceptionReport           = ''
        self.vExceptionTraceback        = ''
        
        self.vCatalogoRaizUID           = ''
        self.vPathDelRaiz               = ''
        self.vCatalogoRaiz              = None
        
        self.vInitialElementURL         = ''
        self.vInitialElementUID         = ''
        self.vInitialElement            = None
        
        self.vProgressElementUID        = ''
        self.vProgressElementURL        = ''
        self.vProgressElementId         = ''
        self.vProgressElementTitle      = ''
        self.vProgressElementDescription= ''
        self.vProgressElement           = None
        
        self.vInputParameters           = theInputParameters
        self.vProgressControlParameters = theProgressControlParameters
        self.vProgressControlCounters   = theProgressControlCounters
        
        self.vResult                    = theResult
        
        self.vInitializeLambda          = theInitializeLambda
        self.vLoopLambda                = theLoopLambda
        self.vElementLambda             = theElementLambda
        self.vElementPloneLambda        = theElementPloneLambda
        self.vFinalizeLambda            = theFinalizeLambda

        self.vLockCatalog               = theLockCatalog == True
        
        
        self.vCreationTimestamp         = theTimestamp

        self.vTimestamp                 = theTimestamp
                
        self.vKey                       = None
        
        self.vPendingControlRequests    = [ ]
        
        self.vPerformedControlRequests  = [ ]
        
        self.vInitializedObjects        = { }
        
        
        if not ( theInitialElement == None):
            
            self.vMemberId           = theInitialElement.fGetMemberId()
            
            self.vInitialElementURL  = theInitialElement.absolute_url()
            self.vInitialElementUID  = theInitialElement.UID()
            
            unCatalogoRaiz          = theInitialElement.getCatalogo()
            self.vCatalogoRaizUID   = unCatalogoRaiz.UID()
            self.vPathDelRaiz       = unCatalogoRaiz.fPhysicalPathString()
            
        
        if not ( theProgressElement == None):
            aKey = theProgressElement.fProgressHandlerKey()
            if aKey:
                self.vKey = aKey
                self.vProgressElementUID         = aKey.get( 'progress_element_UID', '')
                self.vProgressElementTitle       = aKey.get( 'progress_element_title', '')
                self.vProgressElementDescription = aKey.get( 'progress_element_description', '')
                self.vProgressElementURL         = aKey.get( 'progress_element_URL', '')
                self.vProgressElementId          = aKey.get( 'progress_element_id', '')

        
        
        
    
        
   
    def pAcquireLock(self,):
        """Reserve access to progress control variables, by acquiring and releasing a lock on a mutual exclussion (mutex) semaphore, held here to protect critical sections and make them thread-safe.
        
        """
        
        # #################
        """MUTEX LOCK. 
        
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.vMutex.acquire()
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return self
    



    
    def pReleaseLock(self, ):
        """Release access to progress control variables, by acquiring and releasing a lock on a mutual exclussion (mutex) semaphore, held here to protect critical sections and make them thread-safe.
        
        """


        # #################
        """MUTEX UNLOCK. 
        
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.vMutex.release()
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return self
    
        

    
    def fNewVoidEstadoControlResult( self,):
        aResult = {
            'started':     False,
            'paused':      False,
            'completed':   False,
            'terminated':  False,
            'error':       False,
            'error_message': '',
            'error_details': '',
            'error_traceback':'',
            'exception':   False,
            'exception_report':  '',
            'exception_traceback': '',
            'pending_control_requests': [],
            'performed_control_requests': [],
        }
        return aResult
 

    
    def fIsStandBy( self,):
        return not self.vStarted
        
     
    def fIsActive( self,):
        return not self.fIsStandBy() and not ( self.vCompleted or self.vTerminated or self.vError or self.vException)
        
        
    def fIsOver( self,):
        return not self.fIsStandBy() and not self.fIsActive()
        
        
                
            
    def fEstadoControl( self,):
        aEstadoControlResult = self.fNewVoidEstadoControlResult()
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireLock()
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            aEstadoControlResult.update( {
                'started':             self.vStarted    == True,
                'paused':              self.vPaused     == True,
                'completed':           self.vCompleted  == True,
                'terminated':          self.vTerminated == True,
                'error':               self.vError      == True,
                'error_message':       self.vErrorMessage,
                'error_details':       self.vErrorDetails,
                'error_traceback':     self.vErrorTraceback,
                'exception':           self.vException  == True,
                'exception_report':    self.vExceptionReport,
                'exception_traceback': self.vExceptionTraceback,
            })
            
            somePendingControlRequestActions = []
            if self.vPendingControlRequests:
                for aControlRequest in self.vPendingControlRequests:
                    somePendingControlRequestActions.append( aControlRequest.copy())
                if somePendingControlRequestActions:
                    aEstadoControlResult[ 'pending_control_requests'] = somePendingControlRequestActions

            somePerformedControlRequestActions = []
            if self.vPerformedControlRequests:
                for aControlRequest in self.vPerformedControlRequests:
                    somePerformedControlRequestActions.append( aControlRequest.copy())
                if somePerformedControlRequestActions:
                    aEstadoControlResult[ 'performed_control_requests'] = somePerformedControlRequestActions
                    
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseLock()
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
        return aEstadoControlResult
        
    
    
    
    
    
        
    def pAddInitializedObjects( self, theInitializedObjects):
        
        if not theInitializedObjects:
            return self
        
        self.vInitializedObjects.update( theInitializedObjects)
        
        return self
    
    
    
    
    
        
    def fGetInitializedObjects( self, theInitializedObjectsKey):
        
        if not theInitializedObjectsKey:
            return None
        
        someInitializedObjects = self.vInitializedObjects.get( theInitializedObjectsKey, None)
        
        return someInitializedObjects
    
    
        
        

    
    def fKey( self,):
        """Identifier for the Progress Control Handler, such that it can be referenced indirectly (i.e. from user interface).
        
        """
        return self.vKey.copy()
        

            
    
    

    def fExecute( self, 
        theContextualElement    =None,
        theAdditionalParams      =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Execute long-lived process.
        
        """

        if theContextualElement == None:
            return self.vResult
        
        unExecutionRecord = theContextualElement.fStartExecution( 'method',  'TRAProgressHandler.fExecute', theParentExecutionRecord,  False, None, ) 
        
        
        try:
            
            
            aFirstExecuteResult = self.fExecute_OneProcess(
                theContextualElement    =theContextualElement,
                theAdditionalParams      =theAdditionalParams,  
                thePermissionsCache     =thePermissionsCache, 
                theRolesCache           =theRolesCache, 
                theParentExecutionRecord=theParentExecutionRecord)
            
            aLastProgressHandlerKey = self.vKey
            aLastExecuteResult      = aFirstExecuteResult
            
            while aLastProgressHandlerKey:    
                
                aProgressHandlerToRunAfter = theContextualElement.fObtenerProgressHandlerToRunAfterKey( aLastProgressHandlerKey)
                if aProgressHandlerToRunAfter:
                    
                    aLastProgressHandlerKey = aProgressHandlerToRunAfter.vKey
                    
                    aLastExecuteResult = aProgressHandlerToRunAfter.fExecute_OneProcess(
                        theContextualElement    =theContextualElement,
                        theAdditionalParams      =theAdditionalParams,  
                        thePermissionsCache     =thePermissionsCache, 
                        theRolesCache           =theRolesCache, 
                        theParentExecutionRecord=theParentExecutionRecord)
                    
                else:
                    aLastProgressHandlerKey = None
                
                    
            return aLastExecuteResult
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
           

            
            
            
            
    
    

    def fExecute_OneProcess( self, 
        theContextualElement    =None,
        theAdditionalParams      =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Execute long-lived process.
        
        """

        if theContextualElement == None:
            return self.vResult
        
        unExecutionRecord = theContextualElement.fStartExecution( 'method',  'TRAProgressHandler.fExecute_OneProcess', theParentExecutionRecord,  False, None, ) 

        unPermissionsCache = fDictOrNew( thePermissionsCache)
        unRolesCache       = fDictOrNew( theRolesCache)
        
        try:
            
            # ####################################################
            """CRITICAL SECTION: verify progress handler state is not started, and set as started.
            
            """
            unWasAlreadyStarted = False
            try:
                # #################
                """MUTEX LOCK. 
                
                """
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                self.pAcquireLock()
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                
                unWasAlreadyStarted = self.vStarted
                if not unWasAlreadyStarted:
                    self.vStarted = True
                    
            finally:
                # #################
                """MUTEX UNLOCK. 
                
                """
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                self.pReleaseLock()
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                
                
                
                
                
            # ####################################################
            """Do not execute if the progress was already started.
            
            """
            if unWasAlreadyStarted:
                self.vResult[ 'condition'] = 'Was_Already_Started'
                return self.vResult                
                
                
            
            
            # ####################################################
            """Execute process.
            
            """
            aThereWasException     = False
            unTerminationRequested = False
            unErrorReported        = False
            
            try:       
                
                try:
                    
                    
                    # ####################################################
                    """Initialze progress. Delegate to the supplied callable lambda, if any.
                    
                    """
                    aInitializeLambda = self.vInitializeLambda
                    if aInitializeLambda:
                        aInitializeLambda( theContextualElement, self, theAdditionalParams)                    
                    
                    aStartDateTimeNowTextual = theContextualElement.fDateTimeNowTextual()
                    self.vResult[ 'start_date_time_string'] = aStartDateTimeNowTextual
                    self.vResult[ 'date_time_now_string']   = aStartDateTimeNowTextual
                    
                    
                    
                    
                    
                    # ####################################################
                    """Verify that essential element UIDs have a value, and retrieve essential elements.
                    
                    """
                    if not self.vInitialElementUID:
                        self.vResult[ 'condition'] = 'No_Initial_Element_UID'
                        return self.vResult
                    
                    if not self.vProgressElementUID:
                        self.vResult[ 'condition'] = 'No_Progress_Element_UID'
                        return self.vResult
                    
                    anInitialElement = theContextualElement.fElementoPorUID( self.vInitialElementUID)
                    if anInitialElement == None:
                        self.vResult[ 'condition'] = 'Initial_Element_NotFound_by_UID'
                        return self.vResult
                    
                    self.vInitialElement = anInitialElement
                    
                    unCatalogoRaiz = self.vInitialElement.getCatalogo()
                    if unCatalogoRaiz == None:
                        self.vResult[ 'condition'] = 'Initial_Element_without_RootCatalog'
                        return self.vResult
                    
                    self.vCatalogoRaiz = unCatalogoRaiz
                    self.vPathDelRaiz  = unCatalogoRaiz.fPhysicalPathString()
                    
                    
                    aProgressElement = theContextualElement.fElementoPorUID( self.vProgressElementUID)
                    if aProgressElement == None:
                        self.vResult[ 'condition'] = 'Progress_Element_NotFound_by_UID'
                        return self.vResult
                    
                    self.vProgressElement = aProgressElement
                    
                    
                    
                    
                    # ####################################################
                    """Set status and info variables of the progress handler.
                    
                    """
                    self.vPaused                    = False
                    self.vCompleted                 = False
                    self.vTerminated                = False
                    
                    self.vError                     = False
                    self.vErrorMessage              = ''
                    self.vErrorDetails              = ''
                    self.vErrorTraceback            = ''

                    self.vException                 = False
                    self.vExceptionReport           = ''
                    self.vExceptionTraceback        = ''
                    
                    
                    
                    
                    # ####################################################
                    """Give a chance to respond to pending control requests.
                    
                    """
                    self.pHandleControlRequests()
                    
                    
                    
                    
                    # ####################################################
                    """If the process requires the catalog to be locked before hand, verify that the catalog is already locked, or lock the catalog.
                    
                    """
                    aCatalogWasLocked = not unCatalogoRaiz.getPermiteModificar()
                    aCatalogIsLocked  = False      
                    
                    try:
                        if self.vLockCatalog:
                            if aCatalogWasLocked:
                                aCatalogIsLocked = True
                            else:
                                aCatalogIsLocked = unCatalogoRaiz.fBloquearCatalogo( theCheckPermissions=False, thePermissionsCache=unPermissionsCache, theRolesCache=unRolesCache, theParentExecutionRecord=unExecutionRecord)
                            if not aCatalogIsLocked:
                                self.vResult[ 'success']   =  False
                                self.vResult[ 'condition'] = 'TRACatalogo_could_not_be_locked'
                                return self.vResult
                            
                           
                               
                            
                            
                        
                        self.pProcessStarted( )
                        
                        
                        

                
                        try:
                            try:
                                
                        
                                # ####################################################
                                """Delete any reports already contained by the progress element.
                                i.e. from a previus run - althoug currently progress elements are not reused ever.
                                
                                """
                                aNumDeletedReports = aProgressElement.fEliminarInformesEstado( 
                                    thePermissionsCache         =unPermissionsCache, 
                                    theRolesCache               =unRolesCache, 
                                    theParentExecutionRecord    =unExecutionRecord,
                                )
                                if aNumDeletedReports:    
                                    transaction.commit( )
                                                        
                                    logging.getLogger( 'gvSIGi18n').info("COMMIT while IMPORT: after eliminating status reports already existing in the progress element %s" , self.Title()) 
                                    
                                    aProgressElement.pFlushCachedTemplates_All()
                                    
                                    #self.pProcessStep( aProgressElement, { aProgressElement.meta_type: 1, cNombreTipoTRAInforme: aNumDeletedReports,}, { aProgressElement.meta_type: 1, cNombreTipoTRAInforme: aNumDeletedReports,})
                                    
                                    
                                    
                                # ####################################################
                                """If so requested, Create a report of the languages, modules, strings and translations state, before executing the process.
                                
                                """
                                aCreateReportBefore = self.vProgressControlParameters.get( 'CreateReportBefore', False)
                                if aCreateReportBefore:
                                    unNuevoInformeAntes = aProgressElement.fCrearInformeEstado( 
                                        cTRAProgress_ReportBefore_Id, 
                                        thePermissionsCache=unPermissionsCache, 
                                        theRolesCache=unRolesCache, 
                                        theParentExecutionRecord=unExecutionRecord
                                    )                            
                                    if not ( unNuevoInformeAntes == None):
                                        transaction.commit( )
                                        logging.getLogger( 'gvSIGi18n').info("COMMIT while process: SUCCESS Create Report Before")        
                            
                                        #self.pProcessStep( aProgressElement, {  aProgressElement.meta_type: 1,} , {  aProgressElement.meta_type: 1, unNuevoInformeAntes.meta_type: 1,})
                                        
                                    else:
                                        logging.getLogger( 'gvSIGi18n').error("While process: FAILURE when create Report Before")        
                                        
                                        raise TRAProcessErrorException( 'gvSIGi18n_Progress_CreateReportBefore_error_msgid', '')
                                        
                                    aProgressElement.pFlushCachedTemplates_All()
                                
                                
                                    
                                    
                                # ####################################################
                                """Execute core process loop.
                                
                                """
                                if not self.vLoopLambda:
                                    if self.vElementLambda:
                                        if self.vElementPloneLambda:
                                            
                                            self.vInitialElement.pForAllElementsDo( lambda theElement: self.vElementLambda( theElement, self, theAdditionalParams), lambda theElement: self.vElementPloneLambda( theElement, self, theAdditionalParams))

                                        else:
                                            self.vInitialElement.pForAllElementsDo( lambda theElement: self.vElementLambda( theElement, self, theAdditionalParams))
                                            
                                
                                else:
                                    
                                    self.vLoopLambda( self.vInitialElement, self, theAdditionalParams)
                                    
                                    
                                    
                                    
                        
                                # ####################################################
                                """If so requested, Create a report of the languages, modules, strings and translations state, after executing the process.
                                
                                """
                                aCreateReportAfter = self.vProgressControlParameters.get( 'CreateReportAfter', False)
                                if aCreateReportAfter:
                                    unNuevoInformeDespues = aProgressElement.fCrearInformeEstado( 
                                        cTRAProgress_ReportAfter_Id, 
                                        thePermissionsCache=unPermissionsCache, 
                                        theRolesCache=unRolesCache, 
                                        theParentExecutionRecord=unExecutionRecord
                                    )
                                    if not ( unNuevoInformeDespues == None):
                                        transaction.commit( )
                                        logging.getLogger( 'gvSIGi18n').info("COMMIT while process: SUCCESS create Report After")        
                            
                                        #self.pProcessStep( aProgressElement, {  aProgressElement.meta_type: 1,} , {  aProgressElement.meta_type: 1, unNuevoInformeDespues.meta_type: 1,})
                                        
                                    else:
                                        logging.getLogger( 'gvSIGi18n').error("While process: FAILURE when create Report After")        
                                        
                                        raise TRAProcessErrorException( 'gvSIGi18n_Progress_CreateReportAfter_error_msgid', '')
                                    
                                    aProgressElement.pFlushCachedTemplates_All()
                        
                                    
                                    
                                    
                                self.vResult[ 'success']   = True
                                    
                                
                                
                                # ####################################################
                                """Return result, when process completed ok.
                                
                                """
                                return self.vResult
                                
                            
                            
                            
                            
                            except TRAProcessErrorException:
                                # ####################################################
                                """Stop the process with an error state, because an process error was encountered during the process loop.
                                
                                """
                                
                                unaExceptionInfo = sys.exc_info()
                                self.vError      = True
                                
                                self.vResult[ 'success']   = False
                                self.vResult[ 'condition'] = 'Process_Error'                        
                                
                                if len( unaExceptionInfo) > 1:
                                    unaExceptionInstance = unaExceptionInfo[ 1]
                                    if unaExceptionInstance:
                                        self.vErrorMessage = unaExceptionInstance.vErrorMessage
                                        self.vErrorDetails = unaExceptionInstance.vErrorDetails
                                        
                                        self.vResult[ 'error_message'] = self.vErrorMessage
                                        self.vResult[ 'error_details'] = self.vErrorDetails
                                        
                                self.vErrorTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                                
                                self.vResult[ 'error_traceback'] = self.vErrorTraceback
                                
                                unErrorReported = True

                                
                                
                                
                                
                        except TRAProcessTerminationException:
                            # ####################################################
                            """Terminate the process because of User termination request handled within the process loop.
                            
                            """
                            
                            self.vTerminated = True
                            self.vPaused     = False
                            
                            self.vResult[ 'success']   = False
                            self.vResult[ 'condition'] = 'Process_Terminated_by_User_request_before_process_completion'    
                            
                            unTerminationRequested = True
                         
                            
                            
                            
                            
                    finally:
                        # ####################################################
                        """If the process was locked in this progress run, unlock the catalog.
                        
                        """
                        if self.vLockCatalog:
                            if aCatalogIsLocked and ( not aCatalogWasLocked):
                                if not ( unCatalogoRaiz == None):
                                    aCatalogIsUnlocked = unCatalogoRaiz.fDesbloquearCatalogo( theCheckPermissions=False, thePermissionsCache=unPermissionsCache, theRolesCache=unRolesCache, theParentExecutionRecord=unExecutionRecord)
                                    if not aCatalogIsUnlocked:
                                        
                                        self.vError = True
                                        self.vResult[ 'success']   =  False
                                        self.vResult[ 'condition'] = 'TRACatalogo_could_not_be_unlocked'
                                        unErrorReported = True
                        
                                        
                                        
                
                except:
                    # ####################################################
                    """Handle program exceptions not handled within the process loop.
                    
                    """
                    unaExceptionInfo = sys.exc_info()

                    self.vException = True
                    
                    self.vResult[ 'success']   = False
                    self.vResult[ 'exception'] = True
                    
                    unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                    
                    self.vExceptionTraceback = unaExceptionFormattedTraceback
                    self.vResult[ 'exception_traceback'] = self.vExceptionTraceback
                    
                    aThereWasException = True
                    unInformeExcepcion = ''
                    try:
                        unInformeExcepcion += 'Exception during fExecute progress of long-lived process, with key %s\non element %s %s at %s\n'  % (  repr( self.vKey), ( self.vInitialElement and self.vInitialElement.meta_type) or '?', ( self.vInitialElement and self.vInitialElement.Title()) or '?', ( self.vInitialElement and self.vInitialElement.fPhysicalPathString()) or '?',)
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
                    
                    self.vExceptionReport = unInformeExcepcion[:]
                    self.vResult[ 'exception_report']     = self.vExceptionReport
                    
                    
                    aResultDump = ''
                    if not ( self.vProgressElement == None):
                        try:
                            aResultDump = self.vProgressElement.fProgressResult_dump( self.vResult)
                        except:
                            None
                    if aResultDump:
                        unInformeExcepcion = '%s %s' % ( unInformeExcepcion, aResultDump, )
                    
                        
                    unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
        
                    if cLogExceptions:
                        logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                    
                    # ####################################################
                    """Return result, when exception.
                    
                    """
                    return self.vResult
            
                
                
            finally:
                # ####################################################
                """Take actions based upon process termination condition.
                
                """
                if aThereWasException:
                    
                    self.pProcessException( )                    
                    
                else:
                    
                    if unErrorReported:
                        self.pProcessError()
                        
                    elif unTerminationRequested:
                        self.pProcessTerminated()

                    else:
                        self.pProcessEnded( )
                        
                        
                        
                # ####################################################
                """Execute supplied finalization callable lambda, if any.
                
                """                        
                if self.vFinalizeLambda:
                    self.vFinalizeLambda( 
                        self.vInitialElement, 
                        self, 
                        theAdditionalParams, 
                        unTerminationRequested, 
                        aThereWasException
                    )
                        

                self.vInitialElement     = None
                self.vCatalogoRaiz       = None
                self.vProgressElement    = None
                self.vInitializedObjects = { }
                
                
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
        

            
 
            
            

                    
                    

    def fReceiveControlRequest( self, 
        theContextualElement    =None,
        theControlRequest       =None,
        theAdditionalParams      =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Register a request to control a long-lived process.
        
        """

        if theContextualElement == None:
            return self.vResult

        
        unExecutionRecord = theContextualElement.fStartExecution( 'method',  'TRAProgressHandler.fReceiveControlRequest', theParentExecutionRecord,  False, None, ) 
        
        
        try:
            
            if not theControlRequest:
                return False  
            
            anAction = theControlRequest.get( 'action', '')
            if not( anAction in cTRAProcessControl_Actions):
                return False  
            
            unAlreadyStarted = False
                               
            try:
                # #################
                """MUTEX LOCK. 
                
                """
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                self.pAcquireLock()
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                
                self.vPendingControlRequests.append( theControlRequest)
                
                unAlreadyStarted = self.vStarted
                    
            finally:
                # #################
                """MUTEX UNLOCK. 
                
                """
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                self.pReleaseLock()
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
            if not unAlreadyStarted:
                try:
                    self.pHandleControlRequests( theContextualElement)
                except TRAProcessTerminationException:
                    None
                
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
           
             
                
        
            
            
            
            
            
            
            
    def pHandleControlRequests( self, theContextualElement=None):
        """Execute actions requested to control a long-lived process.
        
        """

            
        
        unHayMasControlRequests  = True
        
        while unHayMasControlRequests:
            
            unControlRequestToHandle = None
            
            try:
                # #################
                """MUTEX LOCK. 
                
                """
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                self.pAcquireLock()
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                
                if self.vPendingControlRequests:
                    
                    unTryControlRequestToHandle = self.vPendingControlRequests[ 0]
                    self.vPendingControlRequests = self.vPendingControlRequests[ 1:]
                    unHayMasControlRequests = len( self.vPendingControlRequests) > 0
                    
                    anAction = unTryControlRequestToHandle.get( 'action', '')
                    if anAction in cTRAProcessControl_Actions:
                        unControlRequestToHandle = unTryControlRequestToHandle.copy()
                        self.vPerformedControlRequests.append( unControlRequestToHandle)

                else:
                    unHayMasControlRequests = False
                    
            finally:
                # #################
                """MUTEX UNLOCK. 
                
                """
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                self.pReleaseLock()
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                
                
                
            if unControlRequestToHandle:
                
                aTimestamp = ''
                if not ( self.vInitialElement == None):
                    aTimestamp = self.vInitialElement.fDateTimeNowTextual()
                elif not ( theContextualElement == None):
                    aTimestamp = theContextualElement.fDateTimeNowTextual()
                
                unControlRequestToHandle[ 'performed_timestamp'] = aTimestamp
                
                
                if anAction == cTRAProcessControl_Action_Terminate:
                    
                    unControlRequestToHandle[ 'changes_applied'].append( cTRAProcessControl_Action_Terminate)
                    
                    raise TRAProcessTerminationException()
                
                
                
                elif anAction == cTRAProcessControl_Action_Pause:
                    if not ( self.vInitialElement == None):
                        self.vPaused = True
                        
                        unControlRequestToHandle[ 'changes_applied'].append( cTRAProcessControl_Action_Pause)
                        
                        if cTRAProgress_LogLongLivedProcess:
                            if not ( self.vProgressElement == None):
                                aResultDump = self.vProgressElement.fProgressResult_dump( self.vResult)
                            
                                aLogger = logging.getLogger( 'gvSIGi18n')
                                aLogger.info( 'PAUSED % s' % aResultDump)
                        
                        self.vInitialElement.pSleepMilliseconds( cTRAProgress_PauseMilliseconds)
        
                        
                        
                elif anAction == cTRAProcessControl_Action_Resume:
                    self.vPaused = False
                    
                    aMillisecondsNow = self.vInitialElement.fMillisecondsNow()
                   
                    aStoreResults_Counters   = self.vProgressControlCounters.get( cTRAProgress_SupportKind_StoreResults, {})
                    aStoreResults_Counters[ 'milliseconds_when_last'] = aMillisecondsNow
                    aStoreResults_Counters[ 'elements_traversed_since_last'] = 0
                    aStoreResults_Counters[ 'elements_changed_since_last'] = 0
                         
                    aTransactional_Counters   = self.vProgressControlCounters.get( cTRAProgress_SupportKind_Transactional, {})
                    aTransactional_Counters[ 'milliseconds_when_last'] = aMillisecondsNow
                    aTransactional_Counters[ 'elements_traversed_since_last'] = 0
                    aTransactional_Counters[ 'elements_changed_since_last'] = 0
                            
                    aYieldProcessor_Counters   = self.vProgressControlCounters.get( cTRAProgress_SupportKind_YieldProcessor, {})
                    aYieldProcessor_Counters[ 'milliseconds_when_last'] = aMillisecondsNow
                    aYieldProcessor_Counters[ 'elements_traversed_since_last'] = 0
                    aYieldProcessor_Counters[ 'elements_changed_since_last'] = 0
                            
                    aStoreResults_Logging   = self.vProgressControlCounters.get( cTRAProgress_SupportKind_Logging, {})
                    aStoreResults_Logging[ 'milliseconds_when_last'] = aMillisecondsNow
                    aStoreResults_Logging[ 'elements_traversed_since_last'] = 0
                    aStoreResults_Logging[ 'elements_changed_since_last'] = 0
                   
                    unControlRequestToHandle[ 'changes_applied'].append( cTRAProcessControl_Action_Resume)
                    
                    if cTRAProgress_LogLongLivedProcess:
                        if not ( self.vProgressElement == None):
                            aResultDump = self.vProgressElement.fProgressResult_dump( self.vResult)
                        
                            aLogger = logging.getLogger( 'gvSIGi18n')
                            aLogger.info( 'RESUMED % s' % aResultDump)
                    
                    
                    
                    
                elif anAction == cTRAProcessControl_Action_ChangeParameters:
                    
                    unThereAreControlParameterChanges = False
                    
                    unChangedParameters = [ ]
                    
                    unosParameterChanges = unControlRequestToHandle.get( 'parameter_changes', { })
                    if unosParameterChanges:

                        for aYesNOPropertyName in cTRAProgress_Control_YesNoPropertyNames:
                            
                            if unosParameterChanges.has_key( aYesNOPropertyName):
                                
                                aChangedValue = unosParameterChanges.get( aYesNOPropertyName, False)
                                
                                if not ( aChangedValue == None) and not ( aChangedValue == ''):
                                    
                                    if aChangedValue in [ True, False,]:
                                        pass
                                    elif aChangedValue.__class__.__name__ in [ 'str', 'unicode',]:
                                        if aChangedValue == cTRAProgress_Control_Yes:
                                            aChangedValue = True
                                        elif aChangedValue == cTRAProgress_Control_No:
                                            aChangedValue = False
                                        else:
                                            aChangedValue = False
                                                                        
                                    aCurrentValue = self.vProgressControlParameters.get( aYesNOPropertyName, False)
                                    
                                    if not ( aChangedValue == aCurrentValue):
                                        
                                        self.vProgressControlParameters[ aYesNOPropertyName] = aChangedValue 
                                        unThereAreControlParameterChanges = True
                                     
                                        unChangedParameters.append( [ cTRAProcessControl_Action_ChangeParameters, aYesNOPropertyName, aCurrentValue, aChangedValue])                              
                            
                            
                                        
                        for aProgressSupportKind in cTRAProgress_SupportKinds_Configurable:
                        
                            unosParameterChangesToSupportKind = unosParameterChanges.get( aProgressSupportKind,  {})
                            if unosParameterChangesToSupportKind:
                                    
                                aCurrentControlParametersForSupportKind = self.vProgressControlParameters.get( aProgressSupportKind, {})
                                if aCurrentControlParametersForSupportKind:
                                        
                                    
                                    for aChangedKey in unosParameterChangesToSupportKind.keys():
                                        
                                        if aCurrentControlParametersForSupportKind.has_key( aChangedKey):
                                            
                                            aChangedValue = unosParameterChangesToSupportKind.get( aChangedKey, None)
                                            
                                            if not ( aChangedValue == None) and not ( aChangedValue == ''):
                                            
                                                if ( aProgressSupportKind == cTRAProgress_SupportKind_YieldProcessor) and ( aChangedKey == 'only_between_transactions'):
                                                
                                                    aChangedValue = unosParameterChangesToSupportKind.get( aChangedKey, False)
                                                    if aChangedValue in [ True, False,]:
                                                        pass
                                                    elif aChangedValue.__class__.__name__ in [ 'str', 'unicode',]:
                                                        if aChangedValue == cTRAProgress_Control_Yes:
                                                            aChangedValue = True
                                                        elif aChangedValue == cTRAProgress_Control_No:
                                                            aChangedValue = False
                                                        else:
                                                            aChangedValue = False
                                                                                        
                                                    aCurrentValue = aCurrentControlParametersForSupportKind.get( aChangedKey, None)
                                                    if not ( aChangedValue == aCurrentValue):
                                                        
                                                        aCurrentControlParametersForSupportKind[ aChangedKey] = aChangedValue 
                                                        unThereAreControlParameterChanges = True
                                                        unChangedParameters.append( [ cTRAProcessControl_Action_ChangeParameters, aProgressSupportKind, aChangedKey, aCurrentValue, aChangedValue])                              
                                                    
                                                    
    
                                                else:
                                                    if aChangedValue in [ True, False,]:
                                                        pass
                                                    
                                                    elif aChangedValue.__class__.__name__ in [ 'str', 'unicode',]:
                                                        if aChangedValue == str( True):
                                                            aChangedValue = True
                                                        elif aChangedValue == str( False):
                                                            aChangedValue = False
                                                        else:
                                                            aNewChangedValue = None
                                                            try:
                                                                aNewChangedValue = int( aChangedValue)
                                                            except:
                                                                None
                                                            if not ( aNewChangedValue == None):
                                                                aChangedValue = aNewChangedValue
                                                            
                                                    
                                                    aCurrentValue = aCurrentControlParametersForSupportKind.get( aChangedKey, None)
                                                    if not ( aChangedValue == aCurrentValue):
                                                        
                                                        aCurrentControlParametersForSupportKind[ aChangedKey] = aChangedValue 
                                                        unThereAreControlParameterChanges = True
                                                        unChangedParameters.append( [ cTRAProcessControl_Action_ChangeParameters, aProgressSupportKind, aChangedKey, aCurrentValue, aChangedValue])                              
                                                    
                                                    
                    if unThereAreControlParameterChanges:
                        
                        unControlRequestToHandle[ 'changes_applied'].extend( unChangedParameters)
                        
                        aProgressElement = self.vProgressElement
                        if aProgressElement == None:
                            if not ( theContextualElement == None):
                                aProgressElement = theContextualElement.fElementoPorUID( self.vProgressElementUID)
                            
                        if not ( aProgressElement == None):
                        
                            aDateTimeNow        = aProgressElement.fDateTimeNow()
                            
                            aProgressElement.pSetParametrosControl( self.vProgressControlParameters)
                            aProgressElement.pSetContadoresControl( self.vProgressControlCounters)
                            aProgressElement.pSetDatosResultado(    self.vResult)
                            aProgressElement.setFechaUltimoInformeProgreso( aDateTimeNow)
                        
                            transaction.commit()
            
                            aCatalogoRaiz = self.vCatalogoRaiz
                            if aCatalogoRaiz == None:
                                if not ( theContextualElement == None):
                                    aCatalogoRaiz = theContextualElement.fElementoPorUID( self.vCatalogoRaizUID)

                            if not ( aCatalogoRaiz == None):
                                aCatalogoRaiz.pFlushCachedTemplates_All()
                         
                        
                            if cTRAProgress_LogLongLivedProcess:
                                
                                if not ( self.vProgressElement == None):
                                    aResultDump = aProgressElement.fProgressResult_dump( self.vResult)
                                    
                                    aLogger = logging.getLogger( 'gvSIGi18n')
                                    aLogger.info( 'CHANGED PROGRESS CONTROL PARAMETERS % s' % aResultDump)            
                                
                                
                                
                else:
                    unControlRequestToHandle[ 'changes_applied'].append( cTRAProgress_ControlRequest_Ignored)
                    
            
        return self
    
    
    
            
    
    
    
    
    def pAccumulateElementsByType( self,):
        if not self.vResult:
            return self
        
        self.vResult[ 'elements_by_type'] = [ ]
        someMetaTypes =  self.vResult[ 'elements_by_type_dict'].keys()
        someMetaTypes = sorted( someMetaTypes)
        for aMType in someMetaTypes:
            self.vResult[ 'elements_by_type'].append( [ aMType, self.vResult[ 'elements_by_type_dict'][ aMType],])

        self.vResult[ 'elements_changed_by_type'] = [ ]
        someMetaTypes =  self.vResult[ 'elements_changed_by_type_dict'].keys()
        someMetaTypes = sorted( someMetaTypes)
        for aMType in someMetaTypes:
            self.vResult[ 'elements_changed_by_type'].append( [ aMType, self.vResult[ 'elements_changed_by_type_dict'][ aMType],])

        return self
    
    
    
    
    
    
    def pProcessStarted( self,):
        
        self.vCompleted  = False
        self.vTerminated = False
        self.vPaused     = False
        self.vError      = False
        self.vException  = False

        aDateTimeNow        = self.vInitialElement.fDateTimeNow()
        aDateTimeNowTextual = self.vInitialElement.fDateToStoreString( aDateTimeNow)
        aMillisecondsNow    = aDateTimeNow.millis()
        
        
        self.vResult[ 'start_date_time']        = aDateTimeNow
        self.vResult[ 'start_date_time_string'] = aDateTimeNowTextual
        
        self.vResult[ 'date_time_now']          = aDateTimeNow
        self.vResult[ 'date_time_now_string']   = aDateTimeNowTextual
        
        
        
        # ######################################################
        """Set initial milliseconds on each counters structure.
        
        """
                
        aStoreResults_Counters   = self.vProgressControlCounters.get( cTRAProgress_SupportKind_StoreResults, {})
        aStoreResults_Counters[ 'milliseconds_when_last'] = aMillisecondsNow
        aStoreResults_Counters[ 'elements_traversed_since_last'] = 0
        aStoreResults_Counters[ 'elements_changed_since_last'] = 0
             
        aTransactional_Counters   = self.vProgressControlCounters.get( cTRAProgress_SupportKind_Transactional, {})
        aTransactional_Counters[ 'elements_traversed_since_last'] = 0
        aTransactional_Counters[ 'elements_changed_since_last'] = 0
        aTransactional_Counters[ 'milliseconds_when_last'] = aMillisecondsNow
                
        aYieldProcessor_Counters   = self.vProgressControlCounters.get( cTRAProgress_SupportKind_YieldProcessor, {})
        aYieldProcessor_Counters[ 'milliseconds_when_last'] = aMillisecondsNow
        aYieldProcessor_Counters[ 'elements_traversed_since_last'] = 0
        aYieldProcessor_Counters[ 'elements_changed_since_last'] = 0
                
        aStoreResults_Logging   = self.vProgressControlCounters.get( cTRAProgress_SupportKind_Logging, {})
        aStoreResults_Logging[ 'milliseconds_when_last'] = aMillisecondsNow
        aStoreResults_Logging[ 'elements_traversed_since_last'] = 0
        aStoreResults_Logging[ 'elements_changed_since_last'] = 0
        
        
        
        
        
        
        # ######################################################
        """Record initial element and root catalog.
        
        """
        
        
        aMetaType = 'UnknownType'
        try:
            aMetaType = self.vInitialElement.meta_type
        except:
            aMetaType = self.vInitialElement.__class__.__name
        if not aMetaType:
            aMetaType = 'UnknownType'
            
        self.vResult[ 'element_type']           = aMetaType
        self.vResult[ 'element_title']          = self.vInitialElement.Title()
        self.vResult[ 'element_path']           = self.vInitialElement.fPhysicalPathString()
        self.vResult[ 'element_UID']            = self.vInitialElement.UID()
        
        self.vResult[ 'TRACatalogo_title']      = self.vCatalogoRaiz.Title()
        self.vResult[ 'TRACatalogo_path' ]      = self.vCatalogoRaiz.fPathDelRaiz()
        self.vResult[ 'TRACatalogo_UID' ]       = self.vCatalogoRaiz.UID()
        
        aMemberId = self.vInitialElement.fGetMemberId()
        self.vResult[ 'member_id'] = aMemberId    
        
        
        
        
        # ######################################################
        """Record into progress element, and persist.
        
        """
        
            
        if not ( self.vProgressElement == None):
            self.vProgressElement.setEstadoProceso( cTRAProgreso_EstadoProceso_Activo)
            self.vProgressElement.setHaComenzado( True)
            self.vProgressElement.setHaCompletadoConExito( False)
            self.vProgressElement.setFechaComienzoProceso( aDateTimeNow)
        
            self.vProgressElement.pSetParametrosControl(         self.vProgressControlParameters)
            self.vProgressElement.pSetContadoresControl(         self.vProgressControlCounters)
            self.vProgressElement.pSetDatosResultado(            self.vResult)
            self.vProgressElement.setFechaUltimoInformeProgreso( aDateTimeNow)
            
            transaction.commit()

            if not ( self.vCatalogoRaiz == None):
                self.vCatalogoRaiz.pFlushCachedTemplates_All()
             
            
                
                
        if cTRAProgress_LogLongLivedProcess:
            
            if not ( self.vProgressElement == None):

                aResultDump = self.vProgressElement.fProgressResult_dump( self.vResult)
                
                aLogger = logging.getLogger( 'gvSIGi18n')
                aLogger.info( 'STARTED % s' % aResultDump)
            
        return self
       
    

    
    
    
    def pProcessStep( self, theElement, theElementTypesRead, theElementTypesModified,):
        """Record step on the current element. Invoked from long-lived process loop for each visited or element.
        
        """
        
        self.pHandleControlRequests()
        
        while self.vPaused:
            
            self.pHandleControlRequests()
            
            if self.vPaused:
                if not ( self.vInitialElement == None):
                    self.vInitialElement.pSleepMilliseconds( cTRAProgress_PauseMilliseconds)
        
        
        aLogging_ActionRequired        = False
        aStoreResults_ActionRequired   = False
        aYieldProcessor_ActionRequired = False
        aTransactional_ActionRequired  = False
        aMillisecondsToYield           = 0
        
        aDateTimeNow        = self.vInitialElement.fDateTimeNow()
        aDateTimeNowTextual = self.vInitialElement.fDateToStoreString( aDateTimeNow)
        aMillisecondsNow    = aDateTimeNow.millis()
        
        self.vResult[ 'date_time_now']          = aDateTimeNow
        self.vResult[ 'date_time_now_string']   = aDateTimeNowTextual
        
        
        
        
        anElementTitle = theElement.Title()
        anElementPath  = theElement.fPhysicalPathString()
        anElementUID   = theElement.UID()
        anElementMetaType = 'UnknownType'
        try:
            anElementMetaType = theElement.meta_type
        except:
            anElementMetaType = theElement.__class__.__name
        if not anElementMetaType:
            anElementMetaType = 'UnknownType'
        
        self.vResult[ 'last_element_type']      = anElementMetaType
        self.vResult[ 'last_element_title']     = anElementTitle
        self.vResult[ 'last_element_path']      = anElementPath
        self.vResult[ 'last_element_UID']       = anElementUID

                
           
                     
        # ######################################################
        """Accumulate number of elements by type, read and changed
        
        """
        
        aNumElementsRead = 0
        if theElementTypesRead:
            
            anElementsOfTypeDict = self.vResult.get( 'elements_by_type_dict', None)
            if not ( anElementsOfTypeDict == None):
                
                for anElementType in theElementTypesRead.keys():
                    aNumElementsOfTypeAlreadyRead = anElementsOfTypeDict.get( anElementType, 0)
                    aNumElementsOfTypeRead = theElementTypesRead.get( anElementType, 0)
                    if aNumElementsOfTypeRead:
                        aNumElementsRead += aNumElementsOfTypeRead
                        anElementsOfTypeDict[ anElementType] = aNumElementsOfTypeAlreadyRead + aNumElementsOfTypeRead
                        
        if aNumElementsRead:
            self.vResult[ 'total_elements_traversed'] += aNumElementsRead
            
            
            
             
        aNumElementsModified = 0        
        if theElementTypesModified:
            
            anElementsChangedOfTypeDict = self.vResult.get( 'elements_changed_by_type_dict', None)
            if not ( anElementsChangedOfTypeDict == None):
                
                for anElementType in theElementTypesModified.keys():
                    aNumElementsOfTypeAlreadyModified = anElementsChangedOfTypeDict.get( anElementType, 0)
                    aNumElementsOfTypeModified = theElementTypesModified.get( anElementType, 0)
                    if aNumElementsOfTypeModified:
                        aNumElementsModified += aNumElementsOfTypeModified
                        anElementsChangedOfTypeDict[ anElementType] = aNumElementsOfTypeAlreadyModified + aNumElementsOfTypeModified
            
        if aNumElementsModified:
            self.vResult[ 'total_elements_changed']   += aNumElementsModified

        
            
                        
            
         
        # ######################################################
        """Determine which process progress management actions shall be undertaken.
        
        """
        
        aStoreResults_Parms    = self.vProgressControlParameters.get( cTRAProgress_SupportKind_StoreResults, {})
        aStoreResults_Enabled  = aStoreResults_Parms.get( 'enabled', False)
        aStoreResults_Counters =None
        
        if aStoreResults_Enabled:
            
            aStoreResults_Counters   = self.vProgressControlCounters.get( cTRAProgress_SupportKind_StoreResults, {})
            
            if aNumElementsRead:
                aStoreResults_Counters[ 'elements_traversed_since_last'] += aNumElementsRead
                
            if aNumElementsModified:
                aStoreResults_Counters[ 'elements_changed_since_last']   += aNumElementsModified
            
            aStoreResults_Parm_MaxMilliseconds  = aStoreResults_Parms.get( 'max_milliseconds', 0)
            if aStoreResults_Parm_MaxMilliseconds:
                aStoreResults_Counter_MillisecondsWhenLast = aStoreResults_Counters.get( 'milliseconds_when_last', 0)
                aStoreResults_Counter_MillisecondsSinceLast = aMillisecondsNow - aStoreResults_Counter_MillisecondsWhenLast
                aStoreResults_Counters[ 'milliseconds_since_last'] = aStoreResults_Counter_MillisecondsSinceLast
                if aStoreResults_Counter_MillisecondsSinceLast >= aStoreResults_Parm_MaxMilliseconds:
                    aStoreResults_ActionRequired = True
        
            if not aStoreResults_ActionRequired:
                
                aStoreResults_Parm_MaxElementsTraversed  = aStoreResults_Parms.get( 'max_elements_traversed', 0)
                if aStoreResults_Parm_MaxElementsTraversed:
                    aStoreResultsCounters_ElementsTraversedSinceLast = aStoreResults_Counters.get( 'elements_traversed_since_last', 0)
                    if aStoreResultsCounters_ElementsTraversedSinceLast >= aStoreResults_Parm_MaxElementsTraversed:
                        aStoreResults_ActionRequired = True
                
                        
            if not aStoreResults_ActionRequired:
                
                aStoreResults_Parm_MaxElementsChanged  = aStoreResults_Parms.get( 'max_elements_changed', 0)
                if aStoreResults_Parm_MaxElementsChanged:
                    aStoreResultsCounters_ElementsChangedSinceLast = aStoreResults_Counters.get( 'elements_changed_since_last', 0)
                    if aStoreResultsCounters_ElementsChangedSinceLast >= aStoreResults_Parm_MaxElementsChanged:
                        aStoreResults_ActionRequired = True
                   
                        
                        
                        
                        
        aTransactional_Parms    = self.vProgressControlParameters.get( cTRAProgress_SupportKind_Transactional, {})
        aTransactional_Enabled  = aTransactional_Parms.get( 'enabled', False)
        aTransactional_Counters = None
        
        if aTransactional_Enabled:
            
            aTransactional_Counters   = self.vProgressControlCounters.get( cTRAProgress_SupportKind_Transactional, {})
            
            if aNumElementsRead:
                aTransactional_Counters[ 'elements_traversed_since_last'] += aNumElementsRead
                
            if aNumElementsModified:
                aTransactional_Counters[ 'elements_changed_since_last']   += aNumElementsModified
                
            if False and aTransactional_Enabled and ( not aTransactional_ActionRequired) and aStoreResults_ActionRequired:
                """Do not couple the two facilities.
                
                """
                aTransactional_ActionRequired = True
            
            else:
                
                aTransactional_Parm_MaxMilliseconds  = aTransactional_Parms.get( 'max_milliseconds', 0)
                if aTransactional_Parm_MaxMilliseconds:
                    aTransactional_Counter_MillisecondsWhenLast = aTransactional_Counters.get( 'milliseconds_when_last', 0)
                    aTransactional_Counter_MillisecondsSinceLast = aMillisecondsNow - aTransactional_Counter_MillisecondsWhenLast
                    aTransactional_Counters[ 'milliseconds_since_last'] = aTransactional_Counter_MillisecondsSinceLast
                    if aTransactional_Counter_MillisecondsSinceLast >= aTransactional_Parm_MaxMilliseconds:
                        aTransactional_ActionRequired = True
                
                if not aTransactional_ActionRequired:
                    
                    aTransactional_Parm_MaxElementsTraversed  = aTransactional_Parms.get( 'max_elements_traversed', 0)
                    if aTransactional_Parm_MaxElementsTraversed:
                        aTransactionalCounters_ElementsTraversedSinceLast = aTransactional_Counters.get( 'elements_traversed_since_last', 0)
                        if aTransactionalCounters_ElementsTraversedSinceLast >= aTransactional_Parm_MaxElementsTraversed:
                            aTransactional_ActionRequired = True
                    
                            
                if not aTransactional_ActionRequired:
                    
                    aTransactional_Parm_MaxElementsChanged  = aTransactional_Parms.get( 'max_elements_changed', 0)
                    if aTransactional_Parm_MaxElementsChanged:
                        aTransactionalCounters_ElementsChangedSinceLast = aTransactional_Counters.get( 'elements_changed_since_last', 0)
                        if aTransactionalCounters_ElementsChangedSinceLast >= aTransactional_Parm_MaxElementsChanged:
                            aTransactional_ActionRequired = True
                                      
                
            if False and aStoreResults_Enabled and ( not aStoreResults_ActionRequired) and aTransactional_ActionRequired:                
                """Do not couple the two facilities.
                
                """
                aStoreResults_ActionRequired = True            
                 
                
                
                        
        aLogging_Parms    = self.vProgressControlParameters.get( cTRAProgress_SupportKind_Logging, {})
        aLogging_Enabled  = cTRAProgress_LogLongLivedProcess and aLogging_Parms.get( 'enabled', False)
        aLogging_Counters = None
        
        if aLogging_Enabled:
            
            aLogging_Counters   = self.vProgressControlCounters.get( cTRAProgress_SupportKind_Logging, {})
            if aNumElementsRead:
                aLogging_Counters[ 'elements_traversed_since_last'] += aNumElementsRead
                
            if aNumElementsModified:
                aLogging_Counters[ 'elements_changed_since_last']   += aNumElementsModified
             
            if aTransactional_ActionRequired:
                    
                aLogging_Counters[ 'transactions_committed_since_last'] += 1
                
                aLogging_Parm_EveryNthTransactions  = aLogging_Parms.get( 'log_every_nth_transactions', 0)
                if aLogging_Parm_EveryNthTransactions:
                    aTransactionalCounters_TransactionsCommittedSinceLast = aLogging_Counters.get( 'transactions_committed_since_last', 0)
                    if aTransactionalCounters_TransactionsCommittedSinceLast >= aLogging_Parm_EveryNthTransactions:
                        aLogging_ActionRequired = True

                        
            if False and ( not aLogging_ActionRequired) and aStoreResults_ActionRequired:
                """Do not couple the two facilities.
                
                """
                aLogging_ActionRequired = True
            
                
            if not aLogging_ActionRequired:
                
                aLogging_Parm_MaxMilliseconds  = aLogging_Parms.get( 'max_milliseconds', 0)
                if aLogging_Parm_MaxMilliseconds:
                    aLogging_Counter_MillisecondsWhenLast = aLogging_Counters.get( 'milliseconds_when_last', 0)
                    aLogging_Counter_MillisecondsSinceLast = aMillisecondsNow - aLogging_Counter_MillisecondsWhenLast
                    aLogging_Counters[ 'milliseconds_since_last'] = aLogging_Counter_MillisecondsSinceLast
                    if aLogging_Counter_MillisecondsSinceLast >= aLogging_Parm_MaxMilliseconds:
                        aLogging_ActionRequired = True
                
                if not aLogging_ActionRequired:
                    
                    aLogging_Parm_MaxElementsTraversed  = aLogging_Parms.get( 'max_elements_traversed', 0)
                    if aLogging_Parm_MaxElementsTraversed:
                        aLoggingCounters_ElementsTraversedSinceLast = aLogging_Counters.get( 'elements_traversed_since_last', 0)
                        if aLoggingCounters_ElementsTraversedSinceLast >= aLogging_Parm_MaxElementsTraversed:
                            aLogging_ActionRequired = True
                    
                            
                if not aLogging_ActionRequired:
                    
                    aLogging_Parm_MaxElementsChanged  = aLogging_Parms.get( 'max_elements_changed', 0)
                    if aLogging_Parm_MaxElementsChanged:
                        aLoggingCounters_ElementsChangedSinceLast = aLogging_Counters.get( 'elements_changed_since_last', 0)
                        if aLoggingCounters_ElementsChangedSinceLast >= aLogging_Parm_MaxElementsChanged:
                            aLogging_ActionRequired = True
                                      
                                                    
                            
              
                            
                            
        aYieldProcessor_Parms  = self.vProgressControlParameters.get( cTRAProgress_SupportKind_YieldProcessor, {})
        aYieldProcessor_Enabled  = cTRAYieldProcessorEnabled and aYieldProcessor_Parms.get( 'enabled', False)
        aYieldProcessor_Counters = None   
        aYieldProcessor_MillisecondsActiveSinceLast = 0
        
        if aYieldProcessor_Enabled:
            
            aYieldProcessor_Counters   = self.vProgressControlCounters.get( cTRAProgress_SupportKind_YieldProcessor, {})
            
            aYieldProcessor_MillisecondsActiveSinceLast = 0
            aYieldProcessor_Counter_MillisecondsWhenLast = aYieldProcessor_Counters.get( 'milliseconds_when_last', 0)
            if aYieldProcessor_Counter_MillisecondsWhenLast:
                aYieldProcessor_MillisecondsActiveSinceLast = aMillisecondsNow - aYieldProcessor_Counter_MillisecondsWhenLast
            
            aYieldProcessor_OnlyBetweenTransactions = aTransactional_Enabled and aYieldProcessor_Parms.get( 'only_between_transactions', False)
            
            if aYieldProcessor_OnlyBetweenTransactions:
                if aTransactional_ActionRequired:
                    aYieldProcessor_ActionRequired = True
                else:
                    None
                
            else:
                
                if aNumElementsRead:
                    aYieldProcessor_Counters[ 'elements_traversed_since_last'] += aNumElementsRead
                    
                if aNumElementsModified:
                    aYieldProcessor_Counters[ 'elements_changed_since_last']   += aNumElementsModified
                    
                
    
                if False and ( not aYieldProcessor_ActionRequired) and aTransactional_ActionRequired:
                    """Do not couple the two facilities.
                    
                    """
                    aYieldProcessor_ActionRequired = True
                
                else:
                    aYieldProcessor_Parm_MaxMilliseconds  = aYieldProcessor_Parms.get( 'max_milliseconds', 0)
                    if aYieldProcessor_Parm_MaxMilliseconds:
                        aYieldProcessor_Counters[ 'milliseconds_since_last'] = aYieldProcessor_MillisecondsActiveSinceLast
                        if aYieldProcessor_MillisecondsActiveSinceLast >= aYieldProcessor_Parm_MaxMilliseconds:
                            aYieldProcessor_ActionRequired = True
                    
                            
                    if not aYieldProcessor_ActionRequired:
                        
                        aYieldProcessor_Parm_MaxElementsTraversed  = aYieldProcessor_Parms.get( 'max_elements_traversed', 0)
                        if aYieldProcessor_Parm_MaxElementsTraversed:
                            aYieldProcessorCounters_ElementsTraversedSinceLast = aYieldProcessor_Counters.get( 'elements_traversed_since_last', 0)
                            if aYieldProcessorCounters_ElementsTraversedSinceLast >= aYieldProcessor_Parm_MaxElementsTraversed:
                                aYieldProcessor_ActionRequired = True
                        
                                
                    if not aYieldProcessor_ActionRequired:
                        
                        aYieldProcessor_Parm_MaxElementsChanged  = aYieldProcessor_Parms.get( 'max_elements_changed', 0)
                        if aYieldProcessor_Parm_MaxElementsChanged:
                            aYieldProcessorCounters_ElementsChangedSinceLast = aYieldProcessor_Counters.get( 'elements_changed_since_last', 0)
                            if aYieldProcessorCounters_ElementsChangedSinceLast >= aYieldProcessor_Parm_MaxElementsChanged:
                                aYieldProcessor_ActionRequired = True
            

            if aYieldProcessor_ActionRequired:
                if aYieldProcessor_MillisecondsActiveSinceLast:
                    aYieldProcessor_Parm_PercentActiveTime = min( 100, aYieldProcessor_Parms.get( 'percent_active_time', 50))
                    if aYieldProcessor_Parm_PercentActiveTime:
                        
                        aMillisecondsToYield =  int( ( aYieldProcessor_MillisecondsActiveSinceLast * min( cTRAProgress_MaxTimePercentageToYield, ( 100 -  aYieldProcessor_Parm_PercentActiveTime))) / aYieldProcessor_Parm_PercentActiveTime)
                        aMillisecondsToYield =  min( max( aMillisecondsToYield, 0), cTRAProgress_MaxMillisecondsToYield)
                
            if aYieldProcessor_ActionRequired:
                if aMillisecondsToYield:
                    aYieldProcessor_Counters[ 'total_activity_time'] += aYieldProcessor_MillisecondsActiveSinceLast        
                     
                    
                    
                    
        someActions = [ ]                    
        if aLogging_ActionRequired:
            someActions.append( cTRAProgress_SupportKind_Logging)
            
        if aStoreResults_ActionRequired:
            someActions.append( cTRAProgress_SupportKind_StoreResults)
            
        if aTransactional_ActionRequired:
            someActions.append( cTRAProgress_SupportKind_Transactional)
            
        if aYieldProcessor_ActionRequired and aMillisecondsToYield:
            someActions.append( cTRAProgress_SupportKind_YieldProcessor)
          
        self.vResult[ 'last_actions'] = someActions

        
        
        
                
        
        
        # ######################################################
        """Perform process progress management actions determined above.
        
        """
        
        
        if aStoreResults_ActionRequired:
            if aStoreResults_Counters:
                aStoreResults_Counters[ 'total_actions']   += 1
                aStoreResults_Counters[ 'milliseconds_when_last'] = aMillisecondsNow
             
        if aTransactional_ActionRequired:
            if aTransactional_Counters:
                aTransactional_Counters[ 'total_actions']  += 1
                aTransactional_Counters[ 'milliseconds_when_last'] = aMillisecondsNow
            if aLogging_Counters:
                aLogging_Counters[ 'transactions_committed_since_last'] += 1
        
        if aLogging_ActionRequired:
            if aLogging_Counters:
                aLogging_Counters[ 'total_actions']    += 1
                aLogging_Counters[ 'milliseconds_when_last'] = aMillisecondsNow
            
        if aYieldProcessor_ActionRequired:
            if aMillisecondsToYield:
                if aYieldProcessor_Counters:
                    aYieldProcessor_Counters[ 'total_actions'] += 1
                    aYieldProcessor_Counters[ 'milliseconds_when_last'] = aMillisecondsNow
                
                
            
            
                            
        if aStoreResults_ActionRequired:
            
            self.vProgressElement.pSetContadoresControl(         self.vProgressControlCounters)
            self.vProgressElement.pSetDatosResultado(            self.vResult)
            self.vProgressElement.setFechaUltimoInformeProgreso( aDateTimeNow)
                
            
                       
                
                
                            
        if aTransactional_ActionRequired:

            transaction.commit()
            
            self.vCatalogoRaiz.pFlushCachedTemplates_All()

                                    
            
                        
                
                            
        if aLogging_ActionRequired:
            
            if not ( self.vProgressElement == None):
                aResultDump = self.vProgressElement.fProgressResult_dump( self.vResult)
                
                aLogger = logging.getLogger( 'gvSIGi18n')
                aLogger.info( 'STEP % s' % aResultDump)
            
                        
                

        if aYieldProcessor_ActionRequired:

            if aMillisecondsToYield:
                self.vInitialElement.pSleepMilliseconds( aMillisecondsToYield)
                       
                aYieldProcessor_Counters[ 'total_yield_time'] += aMillisecondsToYield        
                
                
                
                
                
        aMillisecondsWhenStepDone = self.vInitialElement.fMillisecondsNow()
        
        if aStoreResults_ActionRequired:
            if aStoreResults_Counters:
                aStoreResults_Counters[ 'elements_traversed_since_last'] = 0
                aStoreResults_Counters[ 'elements_changed_since_last'] = 0
                aStoreResults_Counters[ 'milliseconds_when_last'] = aMillisecondsWhenStepDone
             
        if aTransactional_ActionRequired:
            if aTransactional_Counters:
                aTransactional_Counters[ 'elements_traversed_since_last'] = 0
                aTransactional_Counters[ 'elements_changed_since_last'] = 0
                aTransactional_Counters[ 'milliseconds_when_last'] = aMillisecondsWhenStepDone
        
        if aLogging_ActionRequired:
            if aLogging_Counters:
                aLogging_Counters[ 'elements_traversed_since_last'] = 0
                aLogging_Counters[ 'elements_changed_since_last'] = 0
                aLogging_Counters[ 'transactions_committed_since_last'] = 0
                aLogging_Counters[ 'milliseconds_when_last'] = aMillisecondsWhenStepDone
            
        if aYieldProcessor_ActionRequired:
            if aYieldProcessor_MillisecondsActiveSinceLast:
                if aYieldProcessor_Counters:
                    aYieldProcessor_Counters[ 'elements_traversed_since_last'] = 0
                    aYieldProcessor_Counters[ 'elements_changed_since_last'] = 0
                    aYieldProcessor_Counters[ 'milliseconds_when_last'] = aMillisecondsWhenStepDone
                
                
        return self
    
    
        
    
    
    


    def pProcessException( self,):

        self.vCompleted  = False
        self.vTerminated = False
        self.vPaused     = False
        self.vError      = False
        self.vException  = True
                
        aDateTimeNow        = self.vInitialElement.fDateTimeNow()
        aDateTimeNowTextual = self.vInitialElement.fDateToStoreString( aDateTimeNow)
        aMillisecondsNow    = aDateTimeNow.millis()
        
        
        self.vResult[ 'end_date_time']        = aDateTimeNow
        self.vResult[ 'end_date_time_string'] = aDateTimeNowTextual
        
        self.vResult[ 'exception_date_time']        = aDateTimeNow
        self.vResult[ 'exception_date_time_string'] = aDateTimeNowTextual
        
        self.vResult[ 'date_time_now']          = aDateTimeNow
        self.vResult[ 'date_time_now_string']   = aDateTimeNowTextual
        

        self.pAccumulateElementsByType()
        
        # ######################################################
        """Record into progress element, and persist.
        
        """
        
            
        if not ( self.vProgressElement == None):

            self.vProgressElement.setEstadoProceso( cTRAProgreso_EstadoProceso_Inactivo)
            self.vProgressElement.setHaCompletadoConExito( False)
            self.vProgressElement.setInformeExcepcion( self.vExceptionReport)
            self.vProgressElement.setFechaFinProceso( aDateTimeNow)
        
            self.vProgressElement.pSetDatosResultado( self.vResult)
            self.vProgressElement.pSetContadoresControl( self.vProgressControlCounters)
            self.vProgressElement.setFechaUltimoInformeProgreso( aDateTimeNow)

            transaction.commit()

            if not ( self.vCatalogoRaiz == None):
                self.vCatalogoRaiz.pFlushCachedTemplates_All()
             
            
        if cTRAProgress_LogLongLivedProcess:
            
            if not ( self.vProgressElement == None):
                aResultDump = self.vProgressElement.fProgressResult_dump( self.vResult)
                
                aLogger = logging.getLogger( 'gvSIGi18n')
                aLogger.error( 'EXCEPTION % s' % aResultDump)
            
        return self
       

     
     
     
    
    
    def pProcessEnded( self, ):
    
        self.vCompleted  = True
        self.vTerminated = False
        self.vPaused     = False
        self.vError      = False
        self.vException  = False
        
        aDateTimeNow        = self.vInitialElement.fDateTimeNow()
        aDateTimeNowTextual = self.vInitialElement.fDateToStoreString( aDateTimeNow)
        aMillisecondsNow    = aDateTimeNow.millis()
        
        
        self.vResult[ 'end_date_time']        = aDateTimeNow
        self.vResult[ 'end_date_time_string'] = aDateTimeNowTextual
        
        self.vResult[ 'date_time_now']          = aDateTimeNow
        self.vResult[ 'date_time_now_string']   = aDateTimeNowTextual
        
        self.pAccumulateElementsByType()
       
        
        # ######################################################
        """Record into progress element, and persist.
        
        """
        
            
        if not ( self.vProgressElement == None):

            self.vProgressElement.setEstadoProceso( cTRAProgreso_EstadoProceso_Inactivo)
            self.vProgressElement.setHaCompletadoConExito( True)
            self.vProgressElement.setFechaFinProceso( aDateTimeNow)
        
            self.vProgressElement.pSetDatosResultado( self.vResult)
            self.vProgressElement.pSetContadoresControl( self.vProgressControlCounters)
            self.vProgressElement.setFechaUltimoInformeProgreso( aDateTimeNow)

            transaction.commit()

            if not ( self.vCatalogoRaiz == None):
                self.vCatalogoRaiz.pFlushCachedTemplates_All()
             
            
        if cTRAProgress_LogLongLivedProcess:
            
            if not ( self.vProgressElement == None):
                aResultDump = self.vProgressElement.fProgressResult_dump( self.vResult)
                
                aLogger = logging.getLogger( 'gvSIGi18n')
                aLogger.info( 'ENDED % s' % aResultDump)
            
        return self
       


     
     
     
          

    
    def pProcessTerminated( self, ):
    
        self.vTerminated = True
        self.vPaused     = False
        self.vError      = False
        self.vException  = False
        
        aDateTimeNow        = self.vInitialElement.fDateTimeNow()
        aDateTimeNowTextual = self.vInitialElement.fDateToStoreString( aDateTimeNow)
        aMillisecondsNow    = aDateTimeNow.millis()
        
        
        self.vResult[ 'end_date_time']        = aDateTimeNow
        self.vResult[ 'end_date_time_string'] = aDateTimeNowTextual
        
        self.vResult[ 'date_time_now']          = aDateTimeNow
        self.vResult[ 'date_time_now_string']   = aDateTimeNowTextual
        
        self.pAccumulateElementsByType()
       
        
        # ######################################################
        """Record into progress element, and persist.
        
        """
        
            
        if not ( self.vProgressElement == None):

            self.vProgressElement.setEstadoProceso( cTRAProgreso_EstadoProceso_Inactivo)
            self.vProgressElement.setHaCompletadoConExito( False)
            self.vProgressElement.setFechaFinProceso( aDateTimeNow)
        
            self.vProgressElement.pSetDatosResultado( self.vResult)
            self.vProgressElement.pSetContadoresControl( self.vProgressControlCounters)
            self.vProgressElement.setFechaUltimoInformeProgreso( aDateTimeNow)

            transaction.commit()

            if not ( self.vCatalogoRaiz == None):
                self.vCatalogoRaiz.pFlushCachedTemplates_All()
             
            
        if cTRAProgress_LogLongLivedProcess:
            
            if not ( self.vProgressElement == None):
                aResultDump = self.vProgressElement.fProgressResult_dump( self.vResult)
                
                aLogger = logging.getLogger( 'gvSIGi18n')
                aLogger.info( 'TERMINATED % s' % aResultDump)
            
        return self
       

     
     

    
    def pProcessError( self, ):
    
        self.vCompleted  = False
        self.vTerminated = False
        self.vPaused     = False
        self.vError      = True
        self.vException  = False
        
        aDateTimeNow        = self.vInitialElement.fDateTimeNow()
        aDateTimeNowTextual = self.vInitialElement.fDateToStoreString( aDateTimeNow)
        aMillisecondsNow    = aDateTimeNow.millis()
        
        
        self.vResult[ 'end_date_time']        = aDateTimeNow
        self.vResult[ 'end_date_time_string'] = aDateTimeNowTextual
        
        self.vResult[ 'date_time_now']          = aDateTimeNow
        self.vResult[ 'date_time_now_string']   = aDateTimeNowTextual
        
        self.pAccumulateElementsByType()
       
        
        # ######################################################
        """Record into progress element, and persist.
        
        """
        
            
        if not ( self.vProgressElement == None):

            self.vProgressElement.setEstadoProceso( cTRAProgreso_EstadoProceso_Inactivo)
            self.vProgressElement.setHaCompletadoConExito( False)
            self.vProgressElement.setFechaFinProceso( aDateTimeNow)
        
            self.vProgressElement.pSetDatosResultado( self.vResult)
            self.vProgressElement.pSetContadoresControl( self.vProgressControlCounters)
            self.vProgressElement.setFechaUltimoInformeProgreso( aDateTimeNow)

            transaction.commit()

            if not ( self.vCatalogoRaiz == None):
                self.vCatalogoRaiz.pFlushCachedTemplates_All()
             
            
        if cTRAProgress_LogLongLivedProcess:
            
            if not ( self.vProgressElement == None):
                aResultDump = self.vProgressElement.fProgressResult_dump( self.vResult)
                
                aLogger = logging.getLogger( 'gvSIGi18n')
                aLogger.error( 'ERROR % s' % aResultDump)
            
        return self
       


    

    
    
    
        
    
    