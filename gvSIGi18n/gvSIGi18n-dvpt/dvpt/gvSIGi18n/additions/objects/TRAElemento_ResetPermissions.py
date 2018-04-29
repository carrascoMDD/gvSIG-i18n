# -*- coding: utf-8 -*-
#
# File: TRAElemento_ResetPermissions.py
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

from TRAElemento_Permission_Definitions import cUseCase_ResetPermissionsTRAElemento, cBoundObject

from TRACatalogo_Globales       import TRACatalogo_Globales


    
    
    
            
# ########################################################################################################
    
class TRAElemento_ResetPermissions:
    """CLASS: role class in support of responsibility of performing an inventory for all application elements.
        
    """
    
    security = ClassSecurityInfo()

         
        

    security.declareProtected( permissions.ManagePortal, 'fRequestNewResetPermissions')
    def fRequestNewResetPermissions( self, 
        theAdditionalParms      =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Request creation of an ResetPermissions long-lived process control handler, to be executed later.
        
        """


        
        
        def fResetPermissionsInitialize_lambda( theContextualElement, theProcessControlManager, theAdditionalParmsHere):  
 
            return None        
                    
         
        
            
        def fResetPermissionsElement_lambda( theElement, theProcessControlManager, theAdditionalParmsHere):  
            
            if theElement == None:
                return None
            
            if not theProcessControlManager:
                return None
            
            
            anElementsByTypeRead    = { theElement.meta_type: 1,}
            anElementsByTypeChanged = None
            
            if theElement.fSetPermissions( theAdditionalParms=theAdditionalParmsHere):
                anElementsByTypeChanged = { theElement.meta_type: 1,}
               
            
            theProcessControlManager.pProcessStep( theElement, anElementsByTypeRead, anElementsByTypeChanged)
            
            return None        

        
        
        
        unExecutionRecord = self.fStartExecution( 'method',  'fRequestNewResetPermissions', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }, ) 
        
        
        try:
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                
            aResetPermissionsResult = self.fNewVoidProgressResult()
            
            
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
                aResetPermissionsResult[ 'process_type']           = cTRAProgress_ProcessType_ResetPermissions
                aResetPermissionsResult[ 'start_date_time_string'] = aStartDateTimeNowTextual
                aResetPermissionsResult[ 'date_time_now_string']   = aStartDateTimeNowTextual
                aResetPermissionsResult[ 'element_type']           = aMetaType
                aResetPermissionsResult[ 'element_title']          = self.Title()
                aResetPermissionsResult[ 'element_path' ]          = self.fPhysicalPathString()
                aResetPermissionsResult[ 'element_UID' ]           = self.UID()
                aResetPermissionsResult[ 'last_element_type']      = ''
                aResetPermissionsResult[ 'last_element_title']     = ''
                aResetPermissionsResult[ 'last_element_path']      = ''
                aResetPermissionsResult[ 'last_element_UID']       = ''
                
                aMemberId = self.fGetMemberId()
                aResetPermissionsResult[ 'member_id'] = aMemberId
                
                unCatalogoRaiz = self.getCatalogo()           
                aResetPermissionsResult[ 'TRACatalogo_title']      = unCatalogoRaiz.Title()
                aResetPermissionsResult[ 'TRACatalogo_path' ]      = unCatalogoRaiz.fPathDelRaiz()
                aResetPermissionsResult[ 'TRACatalogo_UID' ]       = unCatalogoRaiz.UID()
                
                    
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_ResetPermissionsTRAElemento, 
                    theElementsBindings     = { cBoundObject: self,},
                    theRulesToCollect       = [ ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord
                )
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    aResetPermissionsResult[ 'success']   =  False
                    aResetPermissionsResult[ 'condition'] = 'user_can_NOT_ResetPermissionsElementsIn_TRACatalogo'
                    aResetPermissionsResult[ 'date_time_now_string']   = self.fDateTimeNowTextual()
                    return None
                
                

                aProgressHandler, aProgressElement = self.fCreateNewProgressAndHandlerForElement(  
                    theInitialElement       =self, 
                    theProcessType          =cTRAProgress_ProcessType_ResetPermissions, 
                    theTimestamp            =aStartDateTimeNowTextual,
                    theResult               =aResetPermissionsResult, 
                    theElementLambda        =fResetPermissionsElement_lambda,
                    theInitializeLambda     =fResetPermissionsInitialize_lambda,
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
                    unInformeExcepcion += 'Exception during fRequestNewResetPermissions of element %s %s at %s\n'  % (  self.meta_type(), self.Title(), self.fPhysicalPathString())
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
                
                aResetPermissionsResult[ 'success'] = False
                aResetPermissionsResult[ 'exception_date_time_string'] = self.fDateTimeNowTextual()
                try:
                    aResetPermissionsResultDump = self.fProgressResult_dump( aResetPermissionsResult)
                except:
                    None
                if aResetPermissionsResultDump:
                    unInformeExcepcion += aResetPermissionsResultDump
                
                aResetPermissionsResult[ 'exception_report'] = unInformeExcepcionWOResult

                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
    
                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return None
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
           
        
       
            
            
            
        
       
                        
            
    
    