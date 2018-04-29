# -*- coding: utf-8 -*-
#
# File: TRAElemento_Inventory.py
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

from TRAElemento_Permission_Definitions import cUseCase_InventoryTRAElemento, cBoundObject

from TRACatalogo_Globales       import TRACatalogo_Globales


    
    
    
            
# ########################################################################################################
    
class TRAElemento_Inventory:
    """CLASS: role class in support of responsibility of performing an inventory for all application elements.
        
    """
    
    security = ClassSecurityInfo()

         
        

    security.declareProtected( permissions.ManagePortal, 'fRequestNewInventory')
    def fRequestNewInventory( self, 
        theAdditionalParms      =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Request creation of an Inventory long-lived process control handler, to be executed later.
        
        """


            
        def fInventoryElement_lambda( theElement, theProcessControlManager, theAdditionalParmsHere):        
                    
            theProcessControlManager.pProcessStep( theElement, { theElement.meta_type: 1,}, None)
            
            return None        

    
        
        
        
        
        unExecutionRecord = self.fStartExecution( 'method',  'fRequestNewInventory', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }, ) 
        
        
        try:
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                
            aInventoryResult = self.fNewVoidProgressResult()
            
            
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
                aInventoryResult[ 'process_type']           = cTRAProgress_ProcessType_Inventory
                aInventoryResult[ 'start_date_time_string'] = aStartDateTimeNowTextual
                aInventoryResult[ 'date_time_now_string']   = aStartDateTimeNowTextual
                aInventoryResult[ 'element_type']           = aMetaType
                aInventoryResult[ 'element_title']          = self.Title()
                aInventoryResult[ 'element_path' ]          = self.fPhysicalPathString()
                aInventoryResult[ 'element_UID' ]           = self.UID()
                aInventoryResult[ 'last_element_type']      = ''
                aInventoryResult[ 'last_element_title']     = ''
                aInventoryResult[ 'last_element_path']      = ''
                aInventoryResult[ 'last_element_UID']       = ''
                
                aMemberId = self.fGetMemberId()
                aInventoryResult[ 'member_id'] = aMemberId
                
                unCatalogoRaiz = self.getCatalogo()           
                aInventoryResult[ 'TRACatalogo_title']      = unCatalogoRaiz.Title()
                aInventoryResult[ 'TRACatalogo_path' ]      = unCatalogoRaiz.fPathDelRaiz()
                aInventoryResult[ 'TRACatalogo_UID' ]       = unCatalogoRaiz.UID()
                
                    
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_InventoryTRAElemento, 
                    theElementsBindings     = { cBoundObject: self,},
                    theRulesToCollect       = [ ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord
                )
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    aInventoryResult[ 'success']   =  False
                    aInventoryResult[ 'condition'] = 'user_can_NOT_InventoryElementsIn_TRACatalogo'
                    aInventoryResult[ 'date_time_now_string']   = self.fDateTimeNowTextual()
                    return None
                


                aProgressHandler, aProgressElement = self.fCreateNewProgressAndHandlerForElement(  
                    theInitialElement       =self, 
                    theProcessType          =cTRAProgress_ProcessType_Inventory, 
                    theTimestamp            =aStartDateTimeNowTextual,
                    theResult               =aInventoryResult, 
                    theElementLambda        =fInventoryElement_lambda,
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
                    unInformeExcepcion += 'Exception during fRequestNewInventory of element %s %s at %s\n'  % (  self.meta_type(), self.Title(), self.fPhysicalPathString())
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
                
                aInventoryResult[ 'success'] = False
                aInventoryResult[ 'exception_date_time_string'] = self.fDateTimeNowTextual()
                try:
                    aInventoryResultDump = self.fProgressResult_dump( aInventoryResult)
                except:
                    None
                if aInventoryResultDump:
                    unInformeExcepcion += aInventoryResultDump
                
                aInventoryResult[ 'exception_report'] = unInformeExcepcionWOResult

                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
    
                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return None
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
           
        

    