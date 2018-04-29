# -*- coding: utf-8 -*-
#
# File: TRAElemento_Progress.py
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
import threading


import cgi

from StringIO                   import StringIO


from DateTime                   import DateTime

from AccessControl              import ClassSecurityInfo

from Products.Archetypes.utils  import shasattr

from Products.CMFCore           import permissions

from Products.CMFCore.utils     import getToolByName




from TRAElemento_Constants      import *

from TRACatalogo_Globales       import TRACatalogo_Globales

from TRAElemento_Permission_Definitions import cBoundObject, cUseCase_ConfigureTRAProgreso, cUseCase_ControlTRAProgreso
   
    
class TRAProcessErrorException( Exception):
    pass
        
    
    
class TRAProcessTerminationException( Exception):
    pass
    

# ##############################################

#class TRAProgreso_NoPersistente:
    #"""Non-persistent object to store the progress information about a long-lived process.
    
    #"""
    
    #def __init__( self, theAttrsDict={}):
        
        #self.vTitle         =  theAttrsDict.get( 'title', '')
        #self.vDescription   =  theAttrsDict.get( 'description', '')
        #self.vTipoProceso   =  theAttrsDict.get( 'tipoProceso', '')
        #self.vClasesSoporte =  theAttrsDict.get( 'clasesSoporte', '')
        #self.vComienzoUID   =  theAttrsDict.get( 'comienzoUID', '')
        
        #self.vEstadoProceso              = cTRAProgreso_EstadoProceso_Inactivo
        
        #self.vFechaComienzoProceso       = None
        #self.vFechaUltimoInformeProgreso = None
        #self.vFechaFinProceso            = None
        #self.vDatosResultado             = None
        #self.vInformeExcepcion           = None
        
        
        
        
    #def fDateTimeNow(self):   
        #return DateTime()
    
    
    
    #def fReprAsString( theObject):
        #return repr( theObject)



        
    
    
    
    
    
    
    
    
    
    
            
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
        
        self.vException                 = False
        self.vExceptionReport           = ''
        
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
            'exception':   False,
            'pending_control_requests': [],
            'performed_control_requests': [],
        }
        return aResult
    
    
    
        
            
    def fEstadoControl( self,):
        aEstadoControlResult = self.fNewVoidEstadoControlResult()
        try:
            self.pAcquireLock()
            
            aEstadoControlResult.update( {
                'started':     self.vStarted    == True,
                'paused':      self.vPaused     == True,
                'completed':   self.vCompleted  == True,
                'terminated':  self.vTerminated == True,
                'exception':   self.vException  == True,
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
            self.pReleaseLock()
            
            
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
        theAdditionalParms      =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Execute long-lived process.
        
        """

        if theContextualElement == None:
            return self.vResult

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators  import ModelDDvlPloneTool_Mutators, cModificationKind_ChangeValues
        
        unExecutionRecord = theContextualElement.fStartExecution( 'method',  'TRAProgressHandler.fExecute', theParentExecutionRecord,  False, None, ) 
        
        
        try:
            
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
                
                
            if unWasAlreadyStarted:
                self.vResult[ 'condition'] = 'Was_Already_Started'
                return self.vResult                
                
                
            aThereWasException     = False
            unTerminationRequested = False
            unErrorReported        = False
            
            try:       
                
                try:
                    
                    
                    
                    aInitializeLambda = self.vInitializeLambda
                    if aInitializeLambda:
                        aInitializeLambda( theContextualElement, self, theAdditionalParms)                    
                    
                    aStartDateTimeNowTextual = theContextualElement.fDateTimeNowTextual()
                    self.vResult[ 'start_date_time_string'] = aStartDateTimeNowTextual
                    self.vResult[ 'date_time_now_string']   = aStartDateTimeNowTextual
                    
                    
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
                    
                    
                    self.vPaused                    = False
                    self.vCompleted                 = False
                    self.vTerminated                = False
                    
                    self.vException                 = False
                    self.vExceptionReport           = ''
                    
                    
                    self.pHandleControlRequests()
                    
                    
                    aCatalogWasLocked = not unCatalogoRaiz.getPermiteModificar()
                    aCatalogIsLocked  = False      
                    
                    try:
                        if self.vLockCatalog:
                            if aCatalogWasLocked:
                                aCatalogIsLocked = True
                            else:
                                aCatalogIsLocked = unCatalogoRaiz.fBloquearCatalogo( theCheckPermissions=False, thePermissionsCache=thePermissionsCache, theRolesCache=theRolesCache, theParentExecutionRecord=unExecutionRecord)
                            if not aCatalogIsLocked:
                                self.vResult[ 'success']   =  False
                                self.vResult[ 'condition'] = 'TRACatalogo_could_not_be_locked'
                                return self.vResult
                            
                           
                                
                                
                        
                        self.pProcessStarted( )
                        
                        
                        try:
                            try:
                                
                                if not self.vLoopLambda:
                                    if self.vElementLambda:
                                    
                                        self.vInitialElement.pForAllElementsDo( lambda theElement: self.vElementLambda( theElement, self, theAdditionalParms))
                                
                                else:
                                    
                                    self.vLoopLambda( self.vInitialElement, self, theAdditionalParms)
                                    
                            except TRAProcessErrorException:
                                unErrorReported = True
                                
                        except TRAProcessTerminationException:
                            unTerminationRequested = True
                         
                            
                            
                    finally:
                        
                        if self.vLockCatalog:
                            if aCatalogIsLocked and ( not aCatalogWasLocked):
                                if not ( unCatalogoRaiz == None):
                                    aCatalogIsUnlocked = unCatalogoRaiz.fDesbloquearCatalogo( theCheckPermissions=False, thePermissionsCache=thePermissionsCache, theRolesCache=theRolesCache, theParentExecutionRecord=unExecutionRecord)
                                    if not aCatalogIsUnlocked:
                                        aRecatalogResult[ 'success']   =  False
                                        aRecatalogResult[ 'condition'] = 'TRACatalogo_could_not_be_unlocked'
                                        return self.vResult
                        
                        
                    if unErrorReported:
                        self.vResult[ 'success']   = False
                        self.vResult[ 'condition'] = 'Process_Error'                        
                        
                    elif unTerminationRequested:
                        self.vResult[ 'success']   = False
                        self.vResult[ 'condition'] = 'Process_Terminated_by_User_request_before_process_completion'    
                        
                    else:
                        self.vResult[ 'success']   = True
                
                        
                        
                    return self.vResult
                
                
                
                except:
                    unaExceptionInfo = sys.exc_info()
                    unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                    
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
                    
                    unInformeExcepcionWOResult = unInformeExcepcion[:]
                    
                    self.vResult[ 'success'] = False
                    self.vResult[ 'exception_date_time_string'] = self.vCatalogoRaiz.fDateTimeNowTextual()
                    aResultDump = ''
                    try:
                        aResultDump = self.vCatalogoRaiz.fProgressResult_dump( self.vResult)
                    except:
                        None
                    if aResultDump:
                        unInformeExcepcion += aResultDump
                    
                        
                    self.pProcessException( unInformeExcepcionWOResult)
                    
                    
                    unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
        
                    if cLogExceptions:
                        logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                    
                    return self.vResult
            
            finally:
                if not aThereWasException:
                    
                    if unErrorReported:
                        self.pProcessError()
                        
                    elif unTerminationRequested:
                        self.pProcessTerminated()

                    else:
                        self.pProcessEnded( )
                        
                if self.vTerminateLambda:
                    self.vTerminateLambda( self.vInitialElement, self, theAdditionalParms, unTerminationRequested, aThereWasException)
                        

                self.vInitialElement     = None
                self.vCatalogoRaiz       = None
                self.vProgressElement    = None
                self.vInitializedObjects = { }
                
                
                
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
           
            if not ( theContextualElement == None):
                aProgressHandlerToRunAfter = theContextualElement.fObtenerProgressHandlerToRunAfterKey( self.vKey)
                if aProgressHandlerToRunAfter:
                    aProgressHandlerToRunAfter.fExecute(
                        theContextualElement    =theContextualElement,
                        theAdditionalParms      =theAdditionalParms,  
                        thePermissionsCache     =thePermissionsCache, 
                        theRolesCache           =theRolesCache, 
                        theParentExecutionRecord=theParentExecutionRecord)
            
            
            
            


    def fReceiveControlRequest( self, 
        theContextualElement    =None,
        theControlRequest       =None,
        theAdditionalParms      =None,  
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
                            aResultDump = self.vInitialElement.fProgressResult_dump( self.vResult)
                        
                            aLogger = logging.getLogger( 'gvSIGi18n')
                            aLogger.info( 'PAUSED % s' % aResultDump)
                        
                        self.vInitialElement.pSleepMilliseconds( cTRAProgress_PauseMilliseconds)
        
                        
                        
                elif anAction == cTRAProcessControl_Action_Resume:
                    self.vPaused = False
                    
                    unControlRequestToHandle[ 'changes_applied'].append( cTRAProcessControl_Action_Resume)
                    
                    if cTRAProgress_LogLongLivedProcess:
                        if not ( self.vInitialElement == None):
                            aResultDump = self.vInitialElement.fProgressResult_dump( self.vResult)
                        
                            aLogger = logging.getLogger( 'gvSIGi18n')
                            aLogger.info( 'RESUMED % s' % aResultDump)
                    
                    
                    
                    
                elif anAction == cTRAProcessControl_Action_ChangeParameters:
                    
                    unThereAreControlParameterChanges = False
                    
                    unChangedParameters = [ ]
                    
                    unosParameterChanges = unControlRequestToHandle.get( 'parameter_changes', { })
                    if unosParameterChanges:

                        if unosParameterChanges.has_key( cTRAProgress_Control_RunAfterPrevious):
                            aChangedValue = unosParameterChanges.get( cTRAProgress_Control_RunAfterPrevious, False)
                            if aChangedValue in [ True, False,]:
                                pass
                            elif aChangedValue.__class__.__name__ in [ 'str', 'unicode',]:
                                if aChangedValue == cTRAProgress_Control_RunAfterPrevious_Yes:
                                    aChangedValue = True
                                elif aChangedValue == cTRAProgress_Control_RunAfterPrevious_No:
                                    aChangedValue = False
                                else:
                                    aChangedValue = False
                                                                
                            aCurrentValue = self.vProgressControlParameters.get( cTRAProgress_Control_RunAfterPrevious, False)
                            
                            if not ( aChangedValue == aCurrentValue):
                                
                                self.vProgressControlParameters[ cTRAProgress_Control_RunAfterPrevious] = aChangedValue 
                                unThereAreControlParameterChanges = True
                             
                                unChangedParameters.append( [ cTRAProcessControl_Action_ChangeParameters, cTRAProgress_Control_RunAfterPrevious, aCurrentValue, aChangedValue])                              
                            
                            
                        for aProgressSupportKind in cTRAProgress_SupportKinds_Configurable:
                        
                            unosParameterChangesToSupportKind = unosParameterChanges.get( aProgressSupportKind,  {})
                            if unosParameterChangesToSupportKind:
                                    
                                aCurrentControlParametersForSupportKind = self.vProgressControlParameters.get( aProgressSupportKind, {})
                                if aCurrentControlParametersForSupportKind:
                                    
                                    for aChangedKey in unosParameterChangesToSupportKind.keys():
                                        
                                        if aCurrentControlParametersForSupportKind.has_key( aChangedKey):
                                            
                                            aChangedValue = unosParameterChangesToSupportKind.get( aChangedKey, None)
                                            if not ( aChangedValue == None) and not ( aChangedValue == ''):
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
            
            aResultDump = self.vInitialElement.fProgressResult_dump( self.vResult)
            
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
                if ( aMillisecondsNow - aStoreResults_Counter_MillisecondsWhenLast) >= aStoreResults_Parm_MaxMilliseconds:
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
                
            if aStoreResults_ActionRequired:
                aTransactional_ActionRequired = True
            
            else:
                
                aTransactional_Parm_MaxMilliseconds  = aTransactional_Parms.get( 'max_milliseconds', 0)
                if aTransactional_Parm_MaxMilliseconds:
                    aTransactional_Counter_MillisecondsWhenLast = aTransactional_Counters.get( 'milliseconds_when_last', 0)
                    if ( aMillisecondsNow - aTransactional_Counter_MillisecondsWhenLast) >= aTransactional_Parm_MaxMilliseconds:
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
                                      
                
            if ( not aStoreResults_ActionRequired) and aStoreResults_Enabled and aTransactional_ActionRequired:                
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

                        
            if ( not aLogging_ActionRequired) and aStoreResults_ActionRequired:
                aLogging_ActionRequired = True
            
                
            if not aLogging_ActionRequired:
                
                aLogging_Parm_MaxMilliseconds  = aLogging_Parms.get( 'max_milliseconds', 0)
                if aLogging_Parm_MaxMilliseconds:
                    aLogging_Counter_MillisecondsWhenLast = aLogging_Counters.get( 'milliseconds_when_last', 0)
                    if ( aMillisecondsNow - aLogging_Counter_MillisecondsWhenLast) >= aLogging_Parm_MaxMilliseconds:
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
            
            if aNumElementsRead:
                aYieldProcessor_Counters[ 'elements_traversed_since_last'] += aNumElementsRead
                
            if aNumElementsModified:
                aYieldProcessor_Counters[ 'elements_changed_since_last']   += aNumElementsModified
                
            aYieldProcessor_MillisecondsActiveSinceLast = 0
            aYieldProcessor_Counter_MillisecondsWhenLast = aYieldProcessor_Counters.get( 'milliseconds_when_last', 0)
            if aYieldProcessor_Counter_MillisecondsWhenLast:
                aYieldProcessor_MillisecondsActiveSinceLast = aMillisecondsNow - aYieldProcessor_Counter_MillisecondsWhenLast
            

            if aTransactional_ActionRequired:
                aYieldProcessor_ActionRequired = True
            
            else:
                aYieldProcessor_Parm_MaxMilliseconds  = aYieldProcessor_Parms.get( 'max_milliseconds', 0)
                if aYieldProcessor_Parm_MaxMilliseconds:
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
            
            aResultDump = self.vInitialElement.fProgressResult_dump( self.vResult)
            
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
    
    
        
    
    
    


    def pProcessException( self, theExceptionReport):

        self.vException               = True
        self.vExceptionReport         = theExceptionReport
        
        self.vResult[ 'exception_report']     = theExceptionReport
        
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
            self.vProgressElement.setInformeExcepcion( theExceptionReport)
            self.vProgressElement.setFechaFinProceso( aDateTimeNow)
        
            self.vProgressElement.pSetDatosResultado( self.vResult)
            self.vProgressElement.pSetContadoresControl( self.vProgressControlCounters)
            self.vProgressElement.setFechaUltimoInformeProgreso( aDateTimeNow)

            transaction.commit()

            if not ( self.vCatalogoRaiz == None):
                self.vCatalogoRaiz.pFlushCachedTemplates_All()
             
            
        if cTRAProgress_LogLongLivedProcess:
            
            aResultDump = self.vInitialElement.fProgressResult_dump( self.vResult)
            
            aLogger = logging.getLogger( 'gvSIGi18n')
            aLogger.info( 'EXCEPTION % s' % aResultDump)
            
        return self
       

     
     
     
    
    
    def pProcessEnded( self, ):
    
        self.vCompleted  = True
        self.vTerminated = False
        self.vPaused     = False
        
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
            
            aResultDump = self.vInitialElement.fProgressResult_dump( self.vResult)
            
            aLogger = logging.getLogger( 'gvSIGi18n')
            aLogger.info( 'ENDED % s' % aResultDump)
            
        return self
       


     
     
     
          

    
    def pProcessTerminated( self, ):
    
        self.vTerminated = True
        self.vPaused     = False
        
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
            
            aResultDump = self.vInitialElement.fProgressResult_dump( self.vResult)
            
            aLogger = logging.getLogger( 'gvSIGi18n')
            aLogger.info( 'TERMINATED % s' % aResultDump)
            
        return self
       

     
     

    
    def pProcessError( self, ):
    
        self.vTerminated = False
        self.vPaused     = False
        self.vError      = True
        
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
            
            aResultDump = self.vInitialElement.fProgressResult_dump( self.vResult)
            
            aLogger = logging.getLogger( 'gvSIGi18n')
            aLogger.info( 'ERROR % s' % aResultDump)
            
        return self
       

     
     
# ########################################################################################################
    
class TRAElemento_Progress:
    """CLASS: role class in support of responsibility to deal with progress of long-lived processes for all application elements.
        
    """
    
    security = ClassSecurityInfo()

    # ###########################################################
    """Results obtained periodically during the progress of long-lived processes, and at the end of the processes.
    
    """

        
    security.declarePrivate( 'fNewVoidProgressHandlerKey')
    def fNewVoidProgressHandlerKey( self,):
        """Identifier for the Progress Control Handler, such that it can be referenced indirectly (i.e. from user interface).
        
        """
        aNewKey = {
            'translations_catalog_root_path':  '',
            'progress_element_UID':            '',            
            'progress_element_title':          '',
            'progress_element_description':    '',
            'progress_element_URL':            '',
            'progress_element_id':             '',
        }
        return aNewKey
        
            
    
    security.declarePrivate( 'fNewVoidProgressControlRequest')
    def fNewVoidProgressControlRequest( self,):
        aNewRequest = {
            'action':              '', 
            'member_id':           '',
            'requested_timestamp':   None,
            'parameter_changes':   None,   
            'performed_timestamp': None,
            'changes_applied':     [ ],
        }
        return aNewRequest
    
            
 
                
    
    security.declarePrivate( 'fNewVoidProgressResult')
    def fNewVoidProgressResult( self, ):
        unResult = {
            'from_progress_handler':    False,
            'process_type':             '',
            'progress_support_kinds':   '',
            'member_id':                '',
            'success':                  False,
            'condition':                '',
            'exception_report':         '',            
            'start_date_time':          None,
            'start_date_time_string':   '',
            'date_time_now_':           None,
            'date_time_now_string':     '',
            'exception_date_time':      None,
            'exception_date_time_string':'',
            'end_date_time':            None,
            'end_date_time_string':     '',
            'TRACatalogo_title':        '',
            'TRACatalogo_path':         '',
            'TRACatalogo_UID':          '',
            'element_type':             '',
            'element_title':            '',
            'element_path':             '',
            'element_UID':              '',
            'last_element_type':        '',
            'last_element_title':       '',
            'last_element_path':        '',
            'last_element_UID':         '',
            'last_actions':             [],
            'total_elements_traversed': 0,
            'total_elements_changed':   0,
            'elements_by_type_dict':    { },
            'elements_by_type':         [ ],
            'elements_changed_by_type_dict': { },
            'elements_changed_by_type': [ ],
            'progress_parameters':      { },
            'progress_counters':        { },
        }
        return unResult
                
        
    
    
   

    security.declarePrivate( 'fProgressResult_dump')
    def fProgressResult_dump( self, theResult):
        
        if not theResult:
            return 'NO Result'
        
        aStringIO = StringIO()
   
        aStringIO.write( """Process %s Result for element %s %s at %s\n""" % ( theResult .get( 'process_type', ''), theResult .get( 'element_type', ''),  theResult .get( 'element_title', ''),theResult .get( 'element_path', '')))
        
        aStringIO.write( """from_progress_handler %s\n""" %                   theResult .get( 'from_progress_handler', False))

        aStringIO.write( """Now %s\n""" %                                     theResult .get( 'date_time_now_string', ''))
        aStringIO.write( """start %s\n""" %                                   theResult .get( 'start_date_time_string', ''))
        aStringIO.write( """end %s\n\n""" %                                   theResult .get( 'end_date_time_string', ''))
        
        aStringIO.write( """Initial element type %s\n""" %                    theResult .get( 'element_type', ''))
        aStringIO.write( """Initial element title %s\n""" %                   theResult .get( 'element_title', ''))
        aStringIO.write( """Initial element path %s\n""" %                    theResult .get( 'element_path', ''))
        aStringIO.write( """Initial element UID %s\n\n""" %                   theResult .get( 'element_UID', ''))

        aStringIO.write( """TRACatalogo title %s\n""" %                       theResult .get( 'TRACatalogo_title', ''))
        aStringIO.write( """TRACatalogo path %s\n""" %                        theResult .get( 'TRACatalogo_path', ''))
        aStringIO.write( """TRACatalogo UID %s\n\n""" %                         theResult .get( 'TRACatalogo_UID', ''))

        aStringIO.write( """Last element type %s\n""" %                       theResult .get( 'last_element_type', ''))
        aStringIO.write( """Last element title %s\n""" %                      theResult .get( 'last_element_title', ''))
        aStringIO.write( """Last element path %s\n""" %                       theResult .get( 'last_element_path', ''))
        aStringIO.write( """Last element UID %s\n\n""" %                      theResult .get( 'last_element_UID', ''))
        
        aStringIO.write( """Last actions %s\n\n""" %                          ( ( theResult .get( 'last_actions', []) and ' '.join( theResult .get( 'last_actions', []))) or ''))
        
        aStringIO.write( """Success: %s\n""" %                                theResult .get( 'success', False))
        aStringIO.write( """Condition: %s\n""" %                              theResult .get( 'condition', False))
        aStringIO.write( """Exception:\n%s\n\n""" %                           theResult .get( 'exception_report', False))
        
        aStringIO.write( """total_elements_traversed: %s\n""" %               theResult .get( 'total_elements_traversed', 0))
        aStringIO.write( """total_elements_changed: %s\n"""   %               theResult .get( 'total_elements_changed', 0))

        aStringIO.write( """\n\n""")
        
        
        
        someElementsByTypeDict = theResult.get( 'elements_by_type_dict', {})
        if not someElementsByTypeDict:
            aStringIO.write( """\nNo accumulators for Elements traversed, classified by Type\n""")
        else:   
            aStringIO.write( """\nElements traversed by Type\n""")
            for aMetaType in sorted( someElementsByTypeDict.keys()):
                aNumElements = someElementsByTypeDict.get( aMetaType, 0)
                aStringIO.write( """%s : %d\n""" % ( aMetaType, aNumElements))
                
            aStringIO.write( """\n\n""")
            
            
        
        someElementsChangedByTypeDict = theResult.get( 'elements_changed_by_type_dict', [])
        if not someElementsChangedByTypeDict:
            aStringIO.write( """\nNo accumulators for Elements changed, classified by Type\n""")
        else:   
            aStringIO.write( """\nElements changed by Type\n""")
            for aMetaType in sorted( someElementsChangedByTypeDict.keys()):
                aNumElements = someElementsChangedByTypeDict.get( aMetaType, 0)
                aStringIO.write( """%s : %d\n""" % ( aMetaType, aNumElements))
                
            aStringIO.write( """\n\n""")
            
            
 
            
        aProgressParameters = theResult.get( 'progress_parameters', None)
        aStringIO.write( self.fProgressParameters_dump( aProgressParameters))
                  
        
        aProgressCounters = theResult.get( 'progress_counters', None)
        aStringIO.write( self.fProgressCounters_dump( aProgressCounters))
                         
        aStringIO.write( """\n\n\n""")
            
        aDumpString = aStringIO.getvalue()
        return aDumpString
                  
     
    
    
    
    
 
    
    # ###########################################################
    """Parameters controlling capabilities serviced during the progress of long-lived processes.
    
    """  

    security.declarePrivate( 'fNewVoidProgressControlParms_General')
    def fNewVoidProgressControlParms_General( self,):
        someProcessControlParms = {
            'enabled':                  False,
            'max_milliseconds':         0,
            'max_elements_traversed':   0,
            'max_elements_changed':     0,            
        }
        
        return someProcessControlParms
    
    
    security.declarePrivate( 'fNewVoidProgressControlParms_Logging')
    def fNewVoidProgressControlParms_Logging( self,):
        someProcessControlParms = self.fNewVoidProgressControlParms_General()
        someProcessControlParms.update( {
            'log_every_nth_transactions':        0,
        })
        
        return someProcessControlParms
    
        
    
    security.declarePrivate( 'fNewVoidProgressControlParms_StoreResults')
    def fNewVoidProgressControlParms_StoreResults( self,):
        someProcessControlParms = self.fNewVoidProgressControlParms_General()
        
        return someProcessControlParms
    
    
    
    security.declarePrivate( 'fNewVoidProgressControlParms_YieldProcessor')
    def fNewVoidProgressControlParms_YieldProcessor( self,):
        someProcessControlParms = self.fNewVoidProgressControlParms_General()
        someProcessControlParms.update( {
            'percent_active_time':                0,
        })
                                
        
        return someProcessControlParms
    
    
    
    security.declarePrivate( 'fNewVoidProgressControlParms_Transactional')
    def fNewVoidProgressControlParms_Transactional( self,):
        someProcessControlParms = self.fNewVoidProgressControlParms_General()
        
        return someProcessControlParms
            

        
        
    security.declarePublic( 'fNewVoidProgressControlParms_All')
    def fNewVoidProgressControlParms_All( self,):
        someProcessControlParms = {
            cTRAProgress_Control_RunAfterPrevious:   False,
            cTRAProgress_SupportKind_Logging:        self.fNewVoidProgressControlParms_Logging(),
            cTRAProgress_SupportKind_StoreResults:   self.fNewVoidProgressControlParms_StoreResults(),
            cTRAProgress_SupportKind_YieldProcessor: self.fNewVoidProgressControlParms_YieldProcessor(),
            cTRAProgress_SupportKind_Transactional:  self.fNewVoidProgressControlParms_Transactional(),
        }
        
        return someProcessControlParms
    


    security.declarePublic( 'fNewVoidProgressControlParms_ToChange')
    def fNewVoidProgressControlParms_ToChange( self,):
        someProcessControlParms = {
            cTRAProgress_SupportKind_Logging:        {},
            cTRAProgress_SupportKind_StoreResults:   {},
            cTRAProgress_SupportKind_YieldProcessor: {},
            cTRAProgress_SupportKind_Transactional:  {},
        }
        
        return someProcessControlParms
    

    
    
    security.declarePrivate( 'fProgressParameters_dump')    
    def fProgressParameters_dump( self, theProgressParameters):
        
        if not theProgressParameters:
            return 'NO ProgressParameters'
        
        aStringIO = StringIO()
         
        aStringIO.write( """\nProgress PARAMETERS\n""")
        
        aRunAfterPrevious = theProgressParameters.get( cTRAProgress_Control_RunAfterPrevious, False)
        aStringIO.write( """    %s %s\n\n""" % ( cTRAProgress_Control_RunAfterPrevious, ( aRunAfterPrevious and 'YES') or 'NO'))
        
        for aProgress_SupportKind in cTRAProgress_SupportKinds_ToDump:
            someProgressParms = theProgressParameters.get( aProgress_SupportKind, None)
            if not ( someProgressParms == None):
                aEnabled = someProgressParms.get( 'enabled', False)
                aStringIO.write( """    %s %s\n""" % ( aProgress_SupportKind, ( aEnabled and 'ENABLED') or 'DISABLED'))
                
                if aEnabled:
                    aStringIO.write( """        max_milliseconds %d\n"""       % someProgressParms.get( 'max_milliseconds', 0))
                    aStringIO.write( """        max_elements_traversed %d\n""" % someProgressParms.get( 'max_elements_traversed', 0))
                    aStringIO.write( """        max_elements_changed %d\n"""   % someProgressParms.get( 'max_elements_changed', 0))
                    
                    if aProgress_SupportKind == cTRAProgress_SupportKind_Logging:
                        aStringIO.write( """        log_every_nth_transactions %d\n""" % someProgressParms.get( 'log_every_nth_transactions', 0))
                                     
                    if aProgress_SupportKind == cTRAProgress_SupportKind_YieldProcessor:
                        aStringIO.write( """        percent_active_time %d\n""" % someProgressParms.get( 'percent_active_time', 0))
            
                    aStringIO.write( """\n""")
                
        aStringIO.write( """\n""")
            
        aDumpString = aStringIO.getvalue()
        return aDumpString
                  
     
        
    
                  
     
        
        
    # ###########################################################
    """Counters to control capabilities serviced during the progress of long-lived processes.
    
    """
        
    security.declarePrivate( 'fNewVoidProgressControlCounters')
    def fNewVoidProgressControlCounters_General( self,):
        someProcessControlCounters = {
            'milliseconds_when_last':             0,
            'elements_traversed_since_last':      0,
            'elements_changed_since_last':        0,
            'total_actions':                      0,
        }
        
        return someProcessControlCounters
        
    
    
    
    security.declarePrivate( 'fNewVoidProgressControlCounters_Logging')
    def fNewVoidProgressControlCounters_Logging( self,):
        someProcessControlCounters = self.fNewVoidProgressControlCounters_General()
        someProcessControlCounters.update( {
            'transactions_committed_since_last':        0,
        })
        
        return someProcessControlCounters
              
     
    
    
    security.declarePrivate( 'fNewVoidProgressControlCounters_StoreResults')
    def fNewVoidProgressControlCounters_StoreResults( self,):
        someProcessControlCounters = self.fNewVoidProgressControlCounters_General()
        
        return someProcessControlCounters
              
     
        
    
    security.declarePrivate( 'fNewVoidProgressControlCounters_YieldProcessor')
    def fNewVoidProgressControlCounters_YieldProcessor( self,):
        someProcessControlCounters = self.fNewVoidProgressControlCounters_General()
        someProcessControlCounters.update( {
            'total_activity_time':        0,
            'total_yield_time':           0,
        })
        
        return someProcessControlCounters
              
     
        
    
    security.declarePrivate( 'fNewVoidProgressControlCounters_Transactional')
    def fNewVoidProgressControlCounters_Transactional( self,):
        someProcessControlCounters = self.fNewVoidProgressControlCounters_General()
        
        return someProcessControlCounters
              
     
        
    
    security.declarePrivate( 'fNewVoidProgressControlCounters')
    def fNewVoidProgressControlCounters( self,):
        someProcessControlCounters = {
            cTRAProgress_SupportKind_Logging:        self.fNewVoidProgressControlCounters_Logging(),
            cTRAProgress_SupportKind_StoreResults:   self.fNewVoidProgressControlCounters_StoreResults(),
            cTRAProgress_SupportKind_YieldProcessor: self.fNewVoidProgressControlCounters_YieldProcessor(),
            cTRAProgress_SupportKind_Transactional:  self.fNewVoidProgressControlCounters_Transactional(),
        }
        
        return someProcessControlCounters
    

    

    
    
    security.declarePrivate( 'fProgressCounters_dump')    
    def fProgressCounters_dump( self, theProgressCounters):
        
        if not theProgressCounters:
            return 'NO ProgressCounters'
        
        aStringIO = StringIO()
         
        aStringIO.write( """\nProgress COUNTERS\n""" )
        
        for aProgress_SupportKind in cTRAProgress_SupportKinds_ToDump:
            someProgressCounters = theProgressCounters.get( aProgress_SupportKind, None)
            if not ( someProgressCounters == None):
                aStringIO.write( """    %s\n""" % aProgress_SupportKind)
                aStringIO.write( """        total_actions %d\n"""                 % someProgressCounters.get( 'total_actions', 0))
                aStringIO.write( """        milliseconds_when_last %d\n"""        % someProgressCounters.get( 'milliseconds_when_last', 0))
                aStringIO.write( """        elements_traversed_since_last %d\n""" % someProgressCounters.get( 'elements_traversed_since_last', 0))
                aStringIO.write( """        elements_changed_since_last %d\n"""   % someProgressCounters.get( 'elements_changed_since_last', 0))
                
                if aProgress_SupportKind == cTRAProgress_SupportKind_Logging:
                    aStringIO.write( """        transactions_committed_since_last %d\n""" % someProgressCounters.get( 'transactions_committed_since_last', 0))
                
                if aProgress_SupportKind == cTRAProgress_SupportKind_YieldProcessor:
                    aStringIO.write( """        total_activity_time %d\n""" % someProgressCounters.get( 'total_activity_time', 0))
                    aStringIO.write( """        total_yield_time %d\n"""    % someProgressCounters.get( 'total_yield_time', 0))
                                     
                aStringIO.write( """\n""")
                
        aStringIO.write( """\n""")
            
        aDumpString = aStringIO.getvalue()
        return aDumpString
    
    
    
    
    
    
    
    # ###########################################################
    """Instantiate control object structures for the progress of a long-lived process.
    
    """      
    
    security.declarePrivate( 'fCreateNewProgressAndHandlerForElement')
    def fCreateNewProgressAndHandlerForElement( self, 
        theInitialElement       =None, 
        theProcessType          ='', 
        theInputParameters      =None,
        theTimestamp            ='',
        theResult               =None,     
        theInitializeLambda     =None,
        theLoopLambda           =None,
        theElementLambda        =None,
        theFinalizeLambda       =None,
        theLockCatalog          =False,
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None,):

        unExecutionRecord = self.fStartExecution( 'method',  'fCreateNewProgressAndHandlerForElement', theParentExecutionRecord,  False, None, ) 
    
        try:
            if ( theInitialElement == None):
                return ( None, None,)
            
            if not theProcessType:
                return ( None, None,)
            
            if not theResult:
                return ( None, None,)      
            
            
            unCatalogoRaiz = theInitialElement.getCatalogo()
            if ( unCatalogoRaiz == None):
                return ( None, None,)
            
        
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache

            
            someProgressControlParms = self.fNewProgressControlParmsForProcessType( theProcessType, self)
            if not someProgressControlParms:
                return ( None, None,)
            
            theResult[ 'progress_parameters'] = someProgressControlParms
            
            someProgressControlCounters = self.fNewVoidProgressControlCounters( )
            theResult[ 'progress_counters'] = someProgressControlCounters

    
            aProgressElement = self.fNewProgressElement( 
                theProcessType               =theProcessType, 
                theElement                   =theInitialElement, 
                theInputParameters           =theInputParameters,
                theProgressControlParameters =someProgressControlParms, 
                theProgressControlCounters   =someProgressControlCounters, 
                theResult                    =theResult,
                theTimestamp                 =theTimestamp,
                thePermissionsCache          =thePermissionsCache, 
                theRolesCache                =theRolesCache, 
                theParentExecutionRecord     =unExecutionRecord,
            )
            if aProgressElement == None:
                return ( None, None,)
            

            theResult[ 'progress_support_kinds'] = aProgressElement.getClasesSoporte()
                        
    
            aProgressHandler = TRAProgressHandler( 
                theInitialElement, 
                aProgressElement, 
                theInputParameters,
                someProgressControlParms, 
                someProgressControlCounters, 
                theResult,
                theInitializeLambda,
                theLoopLambda,
                theElementLambda,
                theFinalizeLambda,
                theLockCatalog,
                theTimestamp,
            )
            if not aProgressHandler:
                return ( None, None,)

            
            if not self.fRegisterProgressHandler( aProgressHandler):
                return ( None, None,)
            
            
                        
            return ( aProgressHandler, aProgressElement, )
               
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
           
        
       

            
        
            
            
            
            
            
    #security.declarePublic( 'fObtenerProgressControlParametersByKey')
    #def fObtenerProgressControlParametersByKey( self, theProgressHandlerKey=None):            
            
        #unProgressHandler = self.fObtenerProgressHandlerByKey( theProgressHandlerKey)
        #if not unProgressHandler:
            #return None
        
        #someProgressControlParameters = unProgressHandler.vProgressControlParameters
        #if not someProgressControlParameters:
            #return None
        #return someProgressControlParameters.copy()
    
              

    


        
        
    security.declarePrivate( 'fNewProgressControlParmsForProcessType')
    def fNewProgressControlParmsForProcessType( self, theProcessType, theElement):
        if not theProcessType:
            return {}
        
        if theElement == None:
            return {}
        
        if not ( theProcessType in cTRAProgress_ProcessTypes_NonVoid):
            return {}
        
        unaIdElementoParametrosControlProgreso = cTRAParametrosControlProgresoIDs_forProcessTypes.get( theProcessType, '')
        if not unaIdElementoParametrosControlProgreso:
            return {}
        
        
        unCatalogoRaiz = self.getCatalogo()    
        if unCatalogoRaiz == None:
            return {}
        
        
        unElementoParametrosControlProgreso = unCatalogoRaiz.getElementoPorID( unaIdElementoParametrosControlProgreso)
        if unElementoParametrosControlProgreso == None:
            return {}
     
        someProgressControlParms = self.fNewVoidProgressControlParms_All()

        unElementoParametrosControlProgreso.pInitDefaultProcessControlParms( theProcessType, someProgressControlParms, theElement)
        
        return someProgressControlParms
        

    
    
           
                    
    
    
      
    security.declarePrivate( 'fProgressSupportKindsForProcessTypeOnTarget')
    def fProgressSupportKindsForProcessTypeOnTarget( self, theProcessType, theElement):
        """Determines which capabilities are serviced to the progress of a long-lived process.
        
        """
        
        if not theProcessType:
            return []
        
        if not ( theProcessType in cTRAProgress_ProcessTypes):
            return []
        
        if theElement == None:
            return []
        
        anElement_MetaType = ''
        try:
            anElement_MetaType = theElement.meta_type
        except:
            None
        if not anElement_MetaType:
            return []
        
        someElementTypesAndSupportKinds = cTRAProgress_SupportKinds_ForProcessTypes.get( theProcessType, None)
        if not someElementTypesAndSupportKinds:
            return []

        aSupportKindsSet = set( )
        
        for anElementTypesAndSupportKinds in someElementTypesAndSupportKinds:
            someTypes = anElementTypesAndSupportKinds.get( 'types', [])
            if anElement_MetaType in someTypes:
                aSupportKinds = anElementTypesAndSupportKinds.get( 'support_kinds', [])
                if aSupportKinds:
                    aSupportKindsSet = aSupportKindsSet.union( set( aSupportKinds))
                
        
        someSupportKinds = sorted( aSupportKindsSet)
        
        return someSupportKinds
    
        
    

    

        
        
        
        
        
      
    security.declarePrivate( 'fNewProgressElement')
    def fNewProgressElement( self, 
        theProcessType               ='', 
        theElement                   =None, 
        theInputParameters           =None,
        theProgressControlParameters =None, 
        theProgressControlCounters   =None, 
        theResult                    =None,
        theTimestamp                 ='',
        thePermissionsCache          =None, 
        theRolesCache                =None, 
        theParentExecutionRecord     =None,):
        """Instantiates a new persistent element to store the progress information about a long-lived process.
        
        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fNewProgressElement', theParentExecutionRecord,  False, None, ) 
        
        try:
                
            if not theProcessType:
                return None
            
            if not ( theProcessType in cTRAProgress_ProcessTypes):
                return None
            
            if theElement == None:
                return None

            unElementTitle = theElement.Title()
            unElementPath  = theElement.fPhysicalPathString()
            unElementUID   = theElement.UID()
            
            unElementMetaType = 'UnknownType'
            try:
                unElementMetaType = theElement.meta_type
            except:
                unElementMetaType = theElement.__class__.__name
            if not unElementMetaType:
                unElementMetaType = 'UnknownType'
            
                
            aMemberId = self.fGetMemberId()
   
                
            unNuevoTitle       = '%s on %s (%s) by %s at %s' % ( theProcessType, unElementTitle, unElementPath, aMemberId, theTimestamp, )
            unNuevoDescription = 'Progress on %s process\n on element %s\n with path %s\n by %s\n started at %s' % ( theProcessType, unElementTitle, unElementPath, aMemberId, theTimestamp, )
            
            unaNuevaId = unNuevoTitle.lower()
            unaNuevaId = unaNuevaId.replace(" ", "-")
            unaNuevaId = unaNuevaId.replace(":", "-")
    
            aPloneTool = self.getPloneUtilsToolForNormalizeString()
            if aPloneTool:
                unaNuevaId = aPloneTool.normalizeString( unaNuevaId)  
            
            unNuevoTitleACrear = unNuevoTitle
            unaNuevaIdACrear   = unaNuevaId
            
            
            someProgressSupportKinds = self.fProgressSupportKindsForProcessTypeOnTarget( theProcessType, theElement)
            if not someProgressSupportKinds:
                return None
            
            
            aNewProgresoAttrsDict = { 
                'title':             unNuevoTitleACrear,
                'description':       unNuevoDescription,
                'tipoProceso':       theProcessType,
                'clasesSoporte':     ' '.join( someProgressSupportKinds),
                'comienzoTipo':      unElementMetaType,
                'comienzoTitulo':    unElementTitle,
                'comienzoUID':       unElementUID,
                'comienzoRuta':      unElementPath,
                'usuarioInformador': aMemberId,
                'estadoProceso':     cTRAProgreso_EstadoProceso_Inactivo,
                'haComenzado':       False,
                'haCompletadoConExito': False,
                'fechaComienzoProceso': None,
                'fechaUltimoInformeProgreso': None,
            }
            
            
            if not ( cTRAProgress_SupportKind_Persistent in someProgressSupportKinds):
                # aProgressElement = TRAProgreso_NoPersistente( aNewProgresoAttrsDict)
                return None
                
            unCatalogoRaiz = self.getCatalogo()           
            if unCatalogoRaiz == None:
                return None
        
            unaColeccionProgresos = unCatalogoRaiz.fObtenerColeccionProgresos()
            if unaColeccionProgresos == None:
                return None
            
                
            unProgresoExistente = unaColeccionProgresos.getElementoPorID( unaNuevaIdACrear)
            unCountIds = 0
            while not ( unProgresoExistente == None):
                unCountIds += 1
                unNuevoTitleACrear = '%s-%d' % ( unNuevoTitle, unCountIds)
                unaNuevaIdACrear = '%s-%d'   % ( unaNuevaId, unCountIds)
                
                unProgresoExistente = unaColeccionProgresos.getElementoPorID( unaNuevaIdACrear)
                
                
            aNewProgresoAttrsDict.update( { 
                'title':         unNuevoTitleACrear,
            })
            
            unaIdNuevoProgreso = unaColeccionProgresos.invokeFactory( cNombreTipoTRAProgreso, unaNuevaIdACrear, **aNewProgresoAttrsDict)
            if not unaIdNuevoProgreso:
                return None
                     
            unNuevoProgreso = unaColeccionProgresos.getElementoPorID( unaIdNuevoProgreso)
            if  unNuevoProgreso == None:
                return None

            
            unNuevoProgreso.manage_fixupOwnershipAfterAdd()
          
            unNuevoProgreso.pSetPermissions()
            
            unNuevoProgreso.pSetParametrosEntrada( theInputParameters)
            unNuevoProgreso.pSetDatosResultado(    theResult)
            unNuevoProgreso.pSetParametrosControl( theProgressControlParameters)
            unNuevoProgreso.pSetContadoresControl( theProgressControlCounters)
            
                        
            transaction.commit()
            
            unCatalogoRaiz.pFlushCachedTemplates_All()

            if cTRAProgress_LogLongLivedProcess:                
                aLogger = logging.getLogger( 'gvSIGi18n')
                aLogger.info( '\n\nCreated %s %s (%s) UID=%s\n' % ( unNuevoProgreso.meta_type, unNuevoProgreso.Title(), unNuevoProgreso.fPhysicalPathString(), unNuevoProgreso.UID(),))
                
            return unNuevoProgreso
   
                    
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
           
                
         
            
            
            
            
 
    

    
    
    

    

    
    security.declarePrivate( 'fNewVoidProcessControlServiceResult')
    def fNewVoidProcessControlServiceResult( self):
        aResult = {
            'action':                          '',
            'success':                         False,
            'condition':                       '',
            'exception':                       '',
            'translations_catalog_root_path':  '',
            'progress_element_UID':            '',
        }
        return aResult
    
    
    
  
    security.declarePublic( 'fService_ProcessControl')
    def fService_ProcessControl( self, 
        theProcessControlAction     =None,
        theProgressHandlerKey       =None, 
        theAdditionalParms          =None,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None): 
        """Process request to launch, terminate, pause, or resume a long-lived process, with a progress control handler registered in TRACatalogo_Globales.gTRAProgressHandlers.
        
        """

        # ##################################################################
        """Record execution and chain in the trace and profiling history/stack.
        
        """
        unExecutionRecord = self.fStartExecution( 'method', 'fService_ProcessControl', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }, str( theProgressHandlerKey or 'no_parameters')) 

        try:
            unResult = self.fProcessControl( 
                theProcessControlAction     = theProcessControlAction,
                theProgressHandlerKey       = theProgressHandlerKey,
                theAdditionalParms          = theAdditionalParms,
                thePermissionsCache         = thePermissionsCache,
                theRolesCache               = theRolesCache,
                theParentExecutionRecord    = unExecutionRecord,
                
            )
            return unResult
            
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
                      
                
                                            

            

    
  
    security.declarePublic( 'fProcessControl')
    def fProcessControl( self, 
        theProcessControlAction     =None,
        theProgressHandlerKey =None, 
        theAdditionalParms          =None,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None): 
        """Process request to launch, terminate, pause, or resume a long-lived process, with a progress control handler registered in TRACatalogo_Globales.gTRAProgressHandlers.
        
        """

        # ##################################################################
        """Record execution and chain in the trace and profiling history/stack.
        
        """
        unExecutionRecord = self.fStartExecution( 'method', 'fProcessControl', theParentExecutionRecord, False, None, ) 

        aMustWaitAfterConfigure = False

        try:
            
            unResult = self.fNewVoidProcessControlServiceResult()
            unResult[ 'action'] = theProcessControlAction
            
            if not ( theProcessControlAction in cTRAProcessControl_Actions):
                return unResult
           
            # ##################################################################
            """Pass if no service request.
            
            """
            
            if not theProgressHandlerKey:
                return unResult

            
            # ##################################################################
            """Include service request parameters in service result.
            
            """
            
            unResult.update( {
                'translations_catalog_root_path': theProgressHandlerKey.get( 'translations_catalog_root_path', ''),   
                'progress_element_UID':           theProgressHandlerKey.get( 'progress_element_UID',           ''),                
            })
            
            
            
            # ##################################################################
            """Initialize permissions and roles cache if not already supplied by service caller.
            
            """
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
            
            
            try: 
                aUseCaseName = ''
                if theProcessControlAction == cTRAProcessControl_Action_ChangeParameters:
                    aUseCaseName = cUseCase_ConfigureTRAProgreso
                else:
                    aUseCaseName = cUseCase_ControlTRAProgreso
                    
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = aUseCaseName,        
                    theElementsBindings     = { cBoundObject: self,},                                    
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
            
                unBrowseStart       = self.fMillisecondsNow()
                try:
                    
                    unCatalogoRaiz = self.getCatalogo()
                    if unCatalogoRaiz == None:
                        return unResult
                    
                    unPathDelRaiz = unCatalogoRaiz.fPhysicalPathString()
                    if not unPathDelRaiz:
                        return unResult
                    
                    
                    if not ( unPathDelRaiz == theProgressHandlerKey.get( 'translations_catalog_root_path', '')):
                        return unResult
            
                    unProgressElementUID = theProgressHandlerKey.get( 'progress_element_UID', '')
                    if not unProgressElementUID:
                        return unResult
                    
                    unaProgressHandlerKey = {
                        'translations_catalog_root_path':  unPathDelRaiz,
                        'progress_element_UID':            unProgressElementUID,            
                    }

                    unProgressHandler = self.fObtenerProgressHandlerByKey( unaProgressHandlerKey)
                    if not unProgressHandler:
                        return unResult
                    
                    unMemberId = self.fGetMemberId()
                    unTimestamp = self.fDateTimeNowTextual()
                    
                    aControlRequest = None
                    
                    if theProcessControlAction == cTRAProcessControl_Action_Execute:
                    
                        anExecuteResult =  unProgressHandler.fExecute(
                            theContextualElement    =self,
                            theAdditionalParms      =None,  
                            thePermissionsCache     =unPermissionsCache, 
                            theRolesCache           =unRolesCache, 
                            theParentExecutionRecord=unExecutionRecord)
            
                        unResult[ 'execute_result'] = anExecuteResult
                        
                        
                    elif  theProcessControlAction == cTRAProcessControl_Action_Terminate:
                        
                        aControlRequest       = self.fNewVoidProgressControlRequest()
                        aControlRequest.update({ 
                            'action':     cTRAProcessControl_Action_Terminate,
                            'member_id':  unMemberId,
                            'requested_timestamp':  unTimestamp,
                        })
                        aControlRequestResult =  unProgressHandler.fReceiveControlRequest(
                            theContextualElement    =self,
                            theControlRequest       =aControlRequest,
                            theAdditionalParms      =None,  
                            thePermissionsCache     =unPermissionsCache, 
                            theRolesCache           =unRolesCache, 
                            theParentExecutionRecord=unExecutionRecord)
            
                        unResult[ 'control_request_result'] = aControlRequestResult
                    
                        aMustWaitAfterConfigure = True
                        
                        
                    elif  theProcessControlAction == cTRAProcessControl_Action_Pause:
                        aControlRequest       = self.fNewVoidProgressControlRequest()
                        aControlRequest.update({ 
                            'action':     cTRAProcessControl_Action_Pause,
                            'member_id':  unMemberId,
                            'requested_timestamp':  unTimestamp,
                        })
                        aControlRequestResult =  unProgressHandler.fReceiveControlRequest(
                            theContextualElement    =self,
                            theControlRequest       = aControlRequest,
                            theAdditionalParms      =None,  
                            thePermissionsCache     =unPermissionsCache, 
                            theRolesCache           =unRolesCache, 
                            theParentExecutionRecord=unExecutionRecord)
            
                        unResult[ 'control_request_result'] = aControlRequestResult
                    
                     
                        aMustWaitAfterConfigure = True
                        
                        
                        
                    elif  theProcessControlAction == cTRAProcessControl_Action_Resume:
                        aControlRequest       = self.fNewVoidProgressControlRequest()
                        aControlRequest.update({ 
                            'action':     cTRAProcessControl_Action_Resume,
                            'member_id':  unMemberId,
                            'requested_timestamp':  unTimestamp,
                        })
                        aControlRequestResult =  unProgressHandler.fReceiveControlRequest(
                            theContextualElement    =self,
                            theControlRequest       = aControlRequest,
                            theAdditionalParms      =None,  
                            thePermissionsCache     =unPermissionsCache, 
                            theRolesCache           =unRolesCache, 
                            theParentExecutionRecord=unExecutionRecord)
            
                        unResult[ 'control_request_result'] = aControlRequestResult
                    
                        aMustWaitAfterConfigure = True
                     

                        
                        
                    elif  theProcessControlAction == cTRAProcessControl_Action_ChangeParameters:
                        aControlRequest       = self.fNewVoidProgressControlRequest()
                        aControlRequest.update({ 
                            'action':     cTRAProcessControl_Action_ChangeParameters,
                            'member_id':  unMemberId,
                            'requested_timestamp':  unTimestamp,
                            'parameter_changes': theAdditionalParms,
                        })
                        aControlRequestResult =  unProgressHandler.fReceiveControlRequest(
                            theContextualElement    =self,
                            theControlRequest       = aControlRequest,
                            theAdditionalParms      =None,  
                            thePermissionsCache     =unPermissionsCache, 
                            theRolesCache           =unRolesCache, 
                            theParentExecutionRecord=unExecutionRecord)
            
                        unResult[ 'control_request_result'] = aControlRequestResult
                    
                        aMustWaitAfterConfigure = True
                     

                finally:
                    unResult[ 'duration'] = self.fMillisecondsNow() - unBrowseStart
                    unResult[ 'success']  = unResult.get( 'execute_result', None) and unResult.get( 'execute_result', None).get('success', False)
                     
                    return unResult
    
            
                            
            except:
                # ################################################################
                """Handle and report conditions when something went exceptionally wrong.
                
                """
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fProcessControl\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                unResult[ 'success']   = False
                unResult[ 'condition'] = cResultCondition_Internal_Exception
                unResult[ 'exception'] = unInformeExcepcion
                unResult[ 'result_string']   = """[ 'success', 'false']"""
                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                    
                return unResult
            
             
        finally:
            
            unExecutionRecord and unExecutionRecord.pEndExecution()
                      
            if aMustWaitAfterConfigure:
                self.pSleepMilliseconds( cTRAProgress_WaitAfterConfigureProcess_Milliseconds)

                
                                       
            
            
            
            
            
            
            
            
            
            
  
    # #######################################################
    # #######################################################
    """Accessors for the global registered Progress Handlers for long-lived processes.
    
    """
        

    
    security.declarePrivate( 'fObtenerProgressHandlerByKey')
    def fObtenerProgressHandlerByKey( self, theProgressHandlerKey=None):

        if not theProgressHandlerKey:
            return None
        
        aProgressHandler_PathDelRaiz = theProgressHandlerKey.get( 'translations_catalog_root_path', '')
        if not aProgressHandler_PathDelRaiz:
            return None
        
        
        aProgressHandler_UID = theProgressHandlerKey.get( 'progress_element_UID', '')
        if not aProgressHandler_UID:
            return None
        
        unCatalogoRaiz = self.getCatalogo()
        if unCatalogoRaiz == None:
            return None
        
         
        aProgressHandler = None

        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            unCatalogoRaiz.pAcquireGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            someHandlersInRoot = TRACatalogo_Globales.gTRAProgressHandlers.get( aProgressHandler_PathDelRaiz, None)
            if someHandlersInRoot:
                aProgressHandler = someHandlersInRoot.get( aProgressHandler_UID, None)

        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            unCatalogoRaiz.pReleaseGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        if not aProgressHandler:
            return None
        
        return aProgressHandler
                        
    
    

    
    
    security.declarePrivate( 'fObtenerProgressHandlerToRunAfterKey')
    def fObtenerProgressHandlerToRunAfterKey( self, theProgressHandlerKey=None):

        if not theProgressHandlerKey:
            return None
        
        aProgressHandler_PathDelRaiz = theProgressHandlerKey.get( 'translations_catalog_root_path', '')
        if not aProgressHandler_PathDelRaiz:
            return None
        
        
        aProgressHandler_UID = theProgressHandlerKey.get( 'progress_element_UID', '')
        if not aProgressHandler_UID:
            return None
        
        unCatalogoRaiz = self.getCatalogo()
        if unCatalogoRaiz == None:
            return None
        
         
        aProgressHandlerToRunAfter = None

        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            unCatalogoRaiz.pAcquireGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            someProgressHandlersToRunAfter = [ ]
            
            someHandlersInRoot = TRACatalogo_Globales.gTRAProgressHandlers.get( aProgressHandler_PathDelRaiz, None)
            if someHandlersInRoot:
                aProgressHandler = someHandlersInRoot.get( aProgressHandler_UID, None)
                
                if aProgressHandler:
                    
                    someHandlersByUserNotStarted = [ ]
                    
                    for otherProgressHandler in someHandlersInRoot.values():
                        
                        if not otherProgressHandler.vStarted:
                            
                            if otherProgressHandler.vProgressControlParameters and otherProgressHandler.vProgressControlParameters.get( cTRAProgress_Control_RunAfterPrevious, False):
                                
                                if otherProgressHandler.vMemberId == aProgressHandler.vMemberId:
                                    someProgressHandlersToRunAfter.append( otherProgressHandler)
                                
            if someProgressHandlersToRunAfter:
                someSortedProgressHandlersToRunAfter = sorted( someProgressHandlersToRunAfter, lambda aPH, otherPH: cmp( aPH.vCreationTimestamp, otherPH.vCreationTimestamp))
                aProgressHandlerToRunAfter = someSortedProgressHandlersToRunAfter[ 0]
                
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            unCatalogoRaiz.pReleaseGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        if not aProgressHandlerToRunAfter:
            return None
        
        return aProgressHandlerToRunAfter
                        
    
    
    
    #security.declarePublic( 'fObtenerTodasProgressHandlerKeys')
    #def fObtenerTodasProgressHandlerKeys(self, ):
        
        #allProgressHandlerKeys = [ ]
        #for aPathDelRaiz in sorted( TRACatalogo_Globales.gTRAProgressHandlers.keys()):
            #someHandlersInRoot = TRACatalogo_Globales.gTRAProgressHandlers.get( aPathDelRaiz, None)
            #if someHandlersInRoot:
                #allProgressHandlerKeys.extend( someHandlersInRoot.keys())

        #allProgressHandlerKeys = sorted( allProgressHandlerKeys, lambda unH, otroH: cmp( unH.get( 'progress_element_title', ''), otroH.get( 'progress_element_title', '')))
                                               
        #return allProgressHandlerKeys
    

      
    #security.declarePublic( 'fObtenerTodosProgressHandlers')
    #def fObtenerTodosProgressHandlers(self, ):
        
        #allProgressHandlers = { }
        #for aPathDelRaiz in TRACatalogo_Globales.gTRAProgressHandlers.keys():
            #someHandlersInRoot = TRACatalogo_Globales.gTRAProgressHandlers.get( aPathDelRaiz, None)
            #if someHandlersInRoot:
                #allProgressHandlers[ aPathDelRaiz] = someHandlersInRoot.copy()
        
        #return allProgressHandlers
    

    
    
    
        
    
    

    security.declarePublic( 'fRegisterProgressHandler')
    def fRegisterProgressHandler(self, theProgressHandler):
        if not theProgressHandler:
            return False
        
        aProgressHandlerKey = theProgressHandler.fKey()
        if not aProgressHandlerKey:
            return False
        
        aProgressHandler_PathDelRaiz = aProgressHandlerKey.get( 'translations_catalog_root_path', '')
        if not aProgressHandler_PathDelRaiz:
            return False
        
        
        aProgressHandler_UID = aProgressHandlerKey.get( 'progress_element_UID', '')
        if not aProgressHandler_UID:
            return False
            
        unCatalogoRaiz = self.getCatalogo()
        if unCatalogoRaiz == None:
            return False
        
        unRegistered = False
        
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            unCatalogoRaiz.pAcquireGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
            someHandlersInRoot = TRACatalogo_Globales.gTRAProgressHandlers.get( aProgressHandler_PathDelRaiz, None)
            if someHandlersInRoot == None:
                someHandlersInRoot = { }
                TRACatalogo_Globales.gTRAProgressHandlers[ aProgressHandler_PathDelRaiz] = someHandlersInRoot
                
            anExistingProgressHandler = someHandlersInRoot.get( aProgressHandler_UID, None)
            if not anExistingProgressHandler:
                someHandlersInRoot[ aProgressHandler_UID] = theProgressHandler
                unRegistered = True
            
    
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            unCatalogoRaiz.pReleaseGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    
        return unRegistered
        
    

    security.declarePublic( 'fUnregisterProgressHandler')
    def fUnregisterProgressHandler(self, theProgressHandler):
        if not theProgressHandler:
            return False
        
        aProgressHandlerKey = theProgressHandler.fKey()
        if not aProgressHandlerKey:
            return False


        aProgressHandler_PathDelRaiz = aProgressHandlerKey.get( 'translations_catalog_root_path', '')
        if not aProgressHandler_PathDelRaiz:
            return False
        
        
        aProgressHandler_UID = aProgressHandlerKey.get( 'progress_element_UID', '')
        if not aProgressHandler_UID:
            return False
        
        unCatalogoRaiz = self.getCatalogo()
        if unCatalogoRaiz == None:
            return False
        
        
        unUnRegistered = False
        
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            unCatalogoRaiz.pAcquireGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            someHandlersInRoot = TRACatalogo_Globales.gTRAProgressHandlers.get( aProgressHandler_PathDelRaiz, None)
            if someHandlersInRoot:            
                
                anExistingProgressHandler = someHandlersInRoot.get( aProgressHandler_UID, None)
                if anExistingProgressHandler:
            
                    someHandlersInRoot.pop( aProgressHandler_UID)
                    unUnRegistered = True
    
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            unCatalogoRaiz.pReleaseGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      
        return unUnRegistered
            
    
    