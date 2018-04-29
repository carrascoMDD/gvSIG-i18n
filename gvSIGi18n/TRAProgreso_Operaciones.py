# -*- coding: utf-8 -*-
#
# File: TRAProgreso_Operaciones.py
#
# Copyright (c) 2008, 2009, 2010 by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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




##code-section module-header #fill in your manual code here


import sys
import traceback
import logging
import transaction


from StringIO                   import StringIO


from AccessControl          import ClassSecurityInfo

from Products.CMFCore       import permissions



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

from TRAArquetipo import TRAArquetipo

from TRAElemento_Permission_Definitions import cBoundObject
from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_ViewResultsTRAProgreso, cUseCase_ConfigureTRAProgreso, cUseCase_ControlTRAProgreso


from TRACatalogo_Globales       import TRACatalogo_Globales


from TRAArquetipo import TRAArquetipo




class TRAProgreso_Operaciones:
    """Operations specifically defined on persistent elements that store the progress information about a long-lived process.
    
    """
    security = ClassSecurityInfo()
     

    
    
            
    
    security.declarePublic( 'fExtraLinks')    
    def fExtraLinks( self):
        
        unosExtraLinks = TRAArquetipo.fExtraLinks( self)
        if not unosExtraLinks:
            unosExtraLinks = [ ]
        
        unaURL = self.absolute_url()
        if not unaURL:
            return unosExtraLinks
        
        
        
        if self.fUseCaseCheckDoable( cUseCase_ViewResultsTRAProgreso):


            unExtraLink = self.fNewVoidExtraLink()
            unExtraLink.update( {
                'label'   : self.fTranslateI18N( 'plone', 'Process Input Parameters', 'Parameters-',),
                'href'    : '%s/TRAProcessInputParameters/' % unaURL,
                'icon'    : '',
                'domain'  : 'plone',
                'msgid'   : 'Process Input Parameters',
            })
            unosExtraLinks.append( unExtraLink)
            
            unExtraLink = self.fNewVoidExtraLink()
            unExtraLink.update( {
                'label'   : self.fTranslateI18N( 'plone', 'Progress Results', 'Results-',),
                'href'    : '%s/TRAProgressResults/' % unaURL,
                'icon'    : '',
                'domain'  : 'plone',
                'msgid'   : 'Progress Results',
            })
            unosExtraLinks.append( unExtraLink)
            
            
        if not self.fIsOverProgressHandler():
            if self.fUseCaseCheckDoable( 'Control_TRAProgreso'):
    
                unExtraLink = self.fNewVoidExtraLink()
                unExtraLink.update( {
                    'label'   : self.fTranslateI18N( 'plone', 'Control Progress', 'Control-',),
                    'href'    : '%s/TRAControlProgress_action/' % unaURL,
                    'icon'    : '',
                    'domain'  : 'plone',
                    'msgid'   : 'Control Progress',
                })
                unosExtraLinks.append( unExtraLink)
                
                
                
            if self.fUseCaseCheckDoable( 'Configure_TRAProgreso'):
    
                unExtraLink = self.fNewVoidExtraLink()
                unExtraLink.update( {
                    'label'   : self.fTranslateI18N( 'plone', 'Configure Progress', 'Configure-',),
                    'href'    : '%s/TRAConfigureProgress_action/' % unaURL,
                    'icon'    : '',
                    'domain'  : 'plone',
                    'msgid'   : 'Configure Progress',
                })
                unosExtraLinks.append( unExtraLink)
                
            
                            
        unElementoEspecificacionProgreso = self.fDeriveElementoEspecificacionProceso()
        if not ( unElementoEspecificacionProgreso == None):
            unExtraLink = self.fNewVoidExtraLink()
            unExtraLink.update( {
                'label'   : self.fTranslateI18N( 'plone', 'Process specification', 'Process specification-',),
                'href'    : '%s/Tabular/' % unElementoEspecificacionProgreso.absolute_url(),
                'icon'    : 'traimportacion.gif',
                'domain'  : 'plone',
                'msgid'   : 'ProcessSpecification',
            })
            unosExtraLinks.append( unExtraLink)

        return unosExtraLinks
    
            
    
    
    
    
    


    security.declarePrivate( 'pAllSubElements_into')    
    def pAllSubElements_into( self, theCollection, theAdditionalParams=None):
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

    
    
    
    
    
        

    # ###########################################################
    """Key to identify the progress handler associated with this TRAProgreso element.
    
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
        
            

    
    
    # ###########################################################
    """Progress control command structure.
    
    """
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
        theAdditionalParams          =None,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None): 
        """Process request to launch, terminate, pause, or resume a long-lived process, with a progress control handler registered in TRACatalogo_Globales.gTRAProgressHandlers.
        
        """

        # ##################################################################
        """Record execution and chain in the trace and profiling history/stack.
        
        """
        unExecutionRecord = self.fStartExecution( 'method', 'fService_ProcessControl', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }, None) 

        try:
            unResult = self.fProcessControl( 
                theProcessControlAction     = theProcessControlAction,
                theAdditionalParams         = theAdditionalParams,
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
        theAdditionalParams          =None,
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
            
            # ##################################################################
            """No action if service request action unknown.
            
            """
            if not ( theProcessControlAction in cTRAProcessControl_Actions):
                return unResult
           

            # ##################################################################
            """Include service request parameters in service result.
            
            """
            
            unResult.update( {
                'translations_catalog_root_path': self.fPathDelRaiz(),   
                'progress_element_UID':           self.UID(),                
            })
            
            
            
            # ##################################################################
            """Initialize permissions and roles cache if not already supplied by service caller.
            
            """
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
            
            
            
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
                    return unResult
            
                unBrowseStart       = self.fMillisecondsNow()
                try:
                    
                    unProgressHandler = self.fObtenerProgressHandler()
                    if not unProgressHandler:
                        return unResult
                    
                    unMemberId = self.fGetMemberId()
                    unTimestamp = self.fDateTimeNowTextual()
                    
                    aControlRequest = None
                    
                    if theProcessControlAction == cTRAProcessControl_Action_Execute:
                    
                        anExecuteResult =  unProgressHandler.fExecute(
                            theContextualElement    =self,
                            theAdditionalParams      =None,  
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
                            theAdditionalParams      =None,  
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
                            theAdditionalParams      =None,  
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
                            theAdditionalParams      =None,  
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
                            'parameter_changes': theAdditionalParams,
                        })
                        aControlRequestResult =  unProgressHandler.fReceiveControlRequest(
                            theContextualElement    =self,
                            theControlRequest       = aControlRequest,
                            theAdditionalParams      =None,  
                            thePermissionsCache     =unPermissionsCache, 
                            theRolesCache           =unRolesCache, 
                            theParentExecutionRecord=unExecutionRecord)
            
                        unResult[ 'control_request_result'] = aControlRequestResult
                    
                        aMustWaitAfterConfigure = True
                     

                finally:
                    unResult[ 'duration'] = self.fMillisecondsNow() - unBrowseStart
                    if unResult.get( 'execute_result', None) and unResult.get( 'execute_result', None).get('success', False):
                        unResult[ 'success']  = True
                    else:
                        unResult[ 'success']  = False
                     
                    return unResult
    
            
                            
            except:
                # ################################################################
                """Handle and report conditions when something went exceptionally wrong.
                
                """
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fProcessControl\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
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
    """Management and access for the global registered Progress Handlers for all long-lived processes.
    
    """
            

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
                        
    
        
    
      
    
    
    
                     
   
  
    # #######################################################
    """Management and access for the Progress Handler associated with this TRAProgreso element.
    
    """
    
    
    security.declareProtected( permissions.View, 'fProgressHandlerKey')
    def fProgressHandlerKey( self,):   

        aKey = self.fNewVoidProgressHandlerKey()
        aKey.update( {
            'translations_catalog_root_path':  self.fPathDelRaiz(),
            'progress_element_UID':            self.UID(),            
            'progress_element_title':          self.Title(),
            'progress_element_description':    self.Description(),
            'progress_element_URL':            self.absolute_url(), 
            'progress_element_id':             self.getId(),
        })
        return aKey  
    
    
        
    
    
    
    security.declareProtected( permissions.View, 'fIsStandByProgressHandler')
    def fIsStandByProgressHandler( self,):
        
        aProgressHandler = self.fObtenerProgressHandler()
        if not aProgressHandler:
            return False
        
        aIsStandBy = aProgressHandler.fIsStandBy()
        return aIsStandBy
    
    
    
   
        
    security.declareProtected( permissions.View, 'fIsActiveProgressHandler')
    def fIsActiveProgressHandler( self,):
        
        aProgressHandler = self.fObtenerProgressHandler()
        if not aProgressHandler:
            return False
        
        aIsActive = aProgressHandler.fIsActive()
        return aIsActive
    
    
    
    
    
    security.declareProtected( permissions.View, 'fIsOverProgressHandler')
    def fIsOverProgressHandler( self,):
        
        aProgressHandler = self.fObtenerProgressHandler()
        if not aProgressHandler:
            return True
        
        aIsOver = aProgressHandler.fIsOver()
        return aIsOver
        
     
    
    
    
    security.declareProtected( permissions.View, 'fObtenerProgressHandler')
    def fObtenerProgressHandler( self,):
        aKey = self.fProgressHandlerKey()
        if not aKey:
            return None
        
        aProgressHandler = self.fObtenerProgressHandlerByKey( aKey)
        return aProgressHandler
    
    
        
    
    
    security.declareProtected( permissions.View, 'fHasProgressHandler')
    def fHasProgressHandler( self,):
        aProgressHandler = self.fObtenerProgressHandler( )
        aHasProgressHandler = not( aProgressHandler == None)
        return aHasProgressHandler
    
    
        
              

    
    
    
    
    

    # #######################################################
    """Accessors to derived information in TRAProgreso element.
    
    """
        
    security.declarePrivate( 'fDeriveElementoEspecificacionProceso')
    def fDeriveElementoEspecificacionProceso( self):
        """When this TRAProgreso element has associated an Import as the progress specification element, this retrives the Import element.
        
        """
        
        unProcessElementId = self.getIdentificadorElementoProceso()
        if not unProcessElementId:
            return None
        
        unProcessElementType = self.getTipoElementoProceso()
        if not unProcessElementType:
            return None
        
        unCatalogo = self.getCatalogo()
        if ( unCatalogo == None):
            return None
        
        if unProcessElementType == cNombreTipoTRAImportacion:
            
            unaColeccionImportaciones = unCatalogo.fObtenerColeccionImportaciones()
            if ( unaColeccionImportaciones == None):
                return None
            
            unElementoProgreso = unaColeccionImportaciones.getElementoPorID( unProcessElementId)
            return unElementoProgreso
        
            
        return None
        
        
    
           
    
    
    
    
    
    

    
    
    security.declareProtected( permissions.View, 'fEstadoControl')
    def fEstadoControl( self,):
        aProgressHandler = self.fObtenerProgressHandler( )
        if not aProgressHandler:
            return { }
        
        aEstadoControlProgreso = aProgressHandler.fEstadoControl()
        if not aEstadoControlProgreso:
            return aEstadoControlProgreso
        
        aEstadoControlProgreso = aEstadoControlProgreso.copy()
        aEstadoControlProgreso[ 'timestamp'] = self.fDateTimeNowTextual()
        
        return aEstadoControlProgreso
    
    
        
    
    
        
    security.declareProtected( permissions.View, 'fDatosResultado')
    def fDatosResultado( self,):                        
        """Create objects structure from the runtime support object, of from the text representation stored as the content of a string field.
        
        """
        
        aProgressHandler = self.fObtenerProgressHandler( )
        if aProgressHandler:
            
            aProgressHandler.pAccumulateElementsByType()
            
            unResult = aProgressHandler.vResult
            if unResult:
                
                unosDatosResultadoString = None
                try:
                    unosDatosResultadoString = self.fReprAsString( unResult)
                except:
                    None
                if unosDatosResultadoString:
                    
                    unosDatosResultado = None
                    try:
                        unosDatosResultado = self.fEvalString( unosDatosResultadoString)
                    except:
                        None
                    if unosDatosResultado:
                        unosDatosResultado[ 'from_progress_handler'] = True
                        unosDatosResultado[ 'timestamp'] = self.fDateTimeNowTextual()
                        return unosDatosResultado

        unosDatosResultadoString = self.getDatosResultado()
        if not unosDatosResultadoString:
            return None
                
        unosDatosResultado = None
        try:
            unosDatosResultado = self.fEvalString( unosDatosResultadoString)
        except:
            None
            
        if not ( unosDatosResultado == None):
            unosDatosResultado[ 'from_progress_handler'] = False
            
        return unosDatosResultado
        
    

    

        
    security.declareProtected( permissions.ModifyPortalContent, 'pSetDatosResultado')
    def pSetDatosResultado( self, theResult):                        
        """Store string representation of objects structure as the content of a string field.
        
        """
        
        unosDatosResultadoString = None
        if theResult:
            unResult = theResult.copy()
            unResult[ 'from_progress_handler'] = False
            unResult[ 'timestamp'] = self.fDateTimeNowTextual()
                
            try:
                unosDatosResultadoString = self.fReprAsString( unResult)
            except:
                None
            
        self.setDatosResultado( unosDatosResultadoString)
                
        return self
        
    

    



        
    security.declareProtected( permissions.View, 'fParametrosEntrada')
    def fParametrosEntrada( self,):                        
        """Create objects structure from the text representation stored as the content of a string field.
        
        """
        
        unosParametrosEntradaString = self.getParametrosEntrada()
        if not unosParametrosEntradaString:
            return None
                
        unosParametrosEntrada = None
        try:
            unosParametrosEntrada = self.fEvalString( unosParametrosEntradaString)
        except:
            None
            
        return unosParametrosEntrada
        
    

    

        
    security.declareProtected( permissions.ModifyPortalContent, 'pSetParametrosEntrada')
    def pSetParametrosEntrada( self, theInputParameters):                        
        """Store string representation of objects structure as the content of a string field.
        
        """
        
        unosParametrosEntradaString = None
        if theInputParameters:
            try:
                unosParametrosEntradaString = self.fReprAsString( theInputParameters)
            except:
                None
            
        self.setParametrosEntrada( unosParametrosEntradaString)
                
        return self
        
    



        
    security.declareProtected( permissions.View, 'fParametrosControl')
    def fParametrosControl( self,):                        
        """Create objects structure from the text representation stored as the content of a string field.
        
        """
        
        aProgressHandler = self.fObtenerProgressHandler( )
        if aProgressHandler:
                        
            unosParameters = aProgressHandler.vProgressControlParameters
            if unosParameters:
                
                unosParametrosControlString = None
                try:
                    unosParametrosControlString = self.fReprAsString( unosParameters)
                except:
                    None
                if unosParametrosControlString:
                    
                    unosParametrosControl = None
                    try:
                        unosParametrosControl = self.fEvalString( unosParametrosControlString)
                    except:
                        None
                    if unosParametrosControl:
                        unosParametrosControl[ 'from_progress_handler'] = True
                        unosParametrosControl[ 'timestamp'] = self.fDateTimeNowTextual()
                        return unosParametrosControl
                    
                    
        unosParametrosControlString = self.getParametrosControl()
        if not unosParametrosControlString:
            return None
                
        unosParametrosControl = None
        try:
            unosParametrosControl = self.fEvalString( unosParametrosControlString)
        except:
            None
            
        if not ( unosParametrosControl == None):
            unosParametrosControl[ 'from_progress_handler'] = False
            
        return unosParametrosControl
        
    

    

        
    security.declareProtected( permissions.ModifyPortalContent, 'pSetParametrosControl')
    def pSetParametrosControl( self, theParameters):                        
        """Store string representation of objects structure as the content of a string field.
        
        """
        
        unosParametrosControlString = None
        if theParameters:
            someParameters = theParameters.copy()
            someParameters[ 'from_progress_handler'] = False
            someParameters[ 'timestamp'] = self.fDateTimeNowTextual()
            try:
                unosParametrosControlString = self.fReprAsString( someParameters)
            except:
                None
            
        self.setParametrosControl( unosParametrosControlString)
                
        return self
        
    
    
    

        
    security.declareProtected( permissions.View, 'fContadoresControl')
    def fContadoresControl( self,):                        
        """Create objects structure from the text representation stored as the content of a string field.
        
        """
        aProgressHandler = self.fObtenerProgressHandler( )
        if aProgressHandler:
                        
            uosCounters = aProgressHandler.vProgressControlCounters
            if uosCounters:
                
                unosContadoresControlString = None
                try:
                    unosContadoresControlString = self.fReprAsString( uosCounters)
                except:
                    None
                if unosContadoresControlString:
                    
                    unosContadoresControl = None
                    try:
                        unosContadoresControl = self.fEvalString( unosContadoresControlString)
                    except:
                        None
                    if unosContadoresControl:
                        unosContadoresControl[ 'from_progress_handler'] = True
                        unosContadoresControl[ 'timestamp'] = self.fDateTimeNowTextual()
                        return unosContadoresControl
        
        unosContadoresControlString = self.getContadoresControl()
        if not unosContadoresControlString:
            return None
                
        unosContadoresControl = None
        try:
            unosContadoresControl = self.fEvalString( unosContadoresControlString)
        except:
            None
            
        if not ( unosContadoresControl == None):
            unosContadoresControl[ 'from_progress_handler'] = False
            
        return unosContadoresControl
        
    

    

        
    security.declareProtected( permissions.ModifyPortalContent, 'pSetContadoresControl')
    def pSetContadoresControl( self, theCounters):                        
        """Store string representation of objects structure as the content of a string field.
        
        """
        
        unosContadoresControlString = None
        if theCounters:
            someCounters = theCounters.copy()
            someCounters[ 'from_progress_handler'] = False
            someCounters[ 'timestamp'] = self.fDateTimeNowTextual()
            try:
                unosContadoresControlString = self.fReprAsString( someCounters)
            except:
                None
            
        self.setContadoresControl( unosContadoresControlString)
                
        return self
    
    
    
    
    
    
    
    
    
    
   
    
  
    # ####################################
    """Reports optionally generated before and after the process execution.
    
    """
    
    

     
    security.declareProtected( permissions.View, 'fObtenerTodosInformes')
    def fObtenerTodosInformes( self, ):
   
        unosElementos = self.fObjectValues( cNombreTipoTRAInforme) 
        return unosElementos
           
     
    
        


    security.declarePrivate( 'fInformeEstadoAntes')    
    def fInformeEstadoAntes( self):
        unInforme = self.getElementoPorID(cTRAProgress_ReportBefore_Id)
                    
        return unInforme


    

    security.declarePrivate( 'fInformeEstadoDespues')    
    def fInformeEstadoDespues( self):
        unInforme = self.getElementoPorID(cTRAProgress_ReportAfter_Id)
                    
        return unInforme
    
    
    

      

    security.declarePrivate( 'fEliminarInformesEstado')    
    def fEliminarInformesEstado( self,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):

        unExecutionRecord = self.fStartExecution( 'method',  'fEliminarInformesEstado', theParentExecutionRecord,  False) 
         
        try:
          
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
                
            unosInformesEstado = self.fObtenerTodosInformes()
            
            someIdsToDelete = [ unInformeEstado.getId() for unInformeEstado in unosInformesEstado]
            
            self.manage_delObjects( someIdsToDelete)
                
            unNumDeletedReports = len( someIdsToDelete)
            
            return unNumDeletedReports

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
        
        
    
            
            


    security.declarePrivate( 'fCrearInformeEstado')    
    def fCrearInformeEstado( self, 
        theTituloInformeEstado,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):

        unExecutionRecord = self.fStartExecution( 'method',  'fCrearInformeEstado', theParentExecutionRecord,  False) 
        
        try:
         
            if not theTituloInformeEstado:
                return None
                
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
                
                
            unInformeEstado = None
            try:
                unInformeEstado = self[ theTituloInformeEstado]
            except:
                None
            
            if not unInformeEstado:
                unaIdNuevoInforme = ''
                try:
                    unaIdNuevoInforme  = self.invokeFactory(  cNombreTipoTRAInforme, theTituloInformeEstado,  title=theTituloInformeEstado )            
                except:
                    None
                
                if not unaIdNuevoInforme:
                    return None
    
                unInformeEstado = self.getElementoPorID( unaIdNuevoInforme)
                if not unInformeEstado:
                    return None
    
                unInformeEstado.manage_fixupOwnershipAfterAdd()
                unInformeEstado.pSetPermissions()
                
            if ( unInformeEstado == None):
                return None
            
            
            unInformeEstado.fElaborarInforme( 
                theUseCaseQueryResult       =None,
                theForceEllaboration        =True, 
                theCheckPermissions         =False,
                thePermissionsCache         =unPermissionsCache, 
                theRolesCache               =unRolesCache, 
                theParentExecutionRecord    =unExecutionRecord
            )
                
            return unInformeEstado

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
        
        
      


    
        
    
            
            
            
            
            
       
    # ############################################################3
    """Produce a string representation of progress results, for example to write to the log.
    
    """
    
    security.declarePrivate( 'fProgressResult_dump')
    def fProgressResult_dump( self, theResult):
        
        if not theResult:
            return 'NO Result'
        
        aStringIO = StringIO()
        
        try: 
       
            aStringIO.write( """Process %s Result for element %s %s at %s\n""" % ( theResult .get( 'process_type', ''), theResult .get( 'element_type', ''),  theResult .get( 'element_title', ''),theResult .get( 'element_path', '')))
            
            aStringIO.write( """from_progress_handler %s\n""" %                   theResult .get( 'from_progress_handler', False))
    
            aStringIO.write( """User %s\n""" %                                    theResult .get( 'member_id', ''))
            
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
            
            aStringIO.write( """Error:\n%s\n\n""" %                               theResult .get( 'error_message', False))
            aStringIO.write( """Error details:\n%s\n""" %                         theResult .get( 'error_details', False))
            aStringIO.write( """Error traceback:\n%s\n\n""" %                     theResult .get( 'error_traceback', False))
    
            aStringIO.write( """Exception report:\n%s\n""" %                      theResult .get( 'exception_report', False))
            aStringIO.write( """Exception traceback:\n%s\n\n""" %                 theResult .get( 'exception_traceback', False))
            
            
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
            
            
        except:
            unaExceptionInfo = sys.exc_info()
            unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))

            unInformeExcepcion = ''
            try:
                unInformeExcepcion += 'Exception during fProgressResult_dump'
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
                         
            aStringIO.write( unInformeExcepcion)
            
        aDumpString = aStringIO.getvalue()
        return aDumpString
                  
     
    
        
    
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
    
    
    
    
                    