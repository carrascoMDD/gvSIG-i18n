# -*- coding: utf-8 -*-
#
# File: TRAColeccionContribuciones_Operaciones.py
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
#

__author__ = """Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana <gvSIGi18n@gvSIG.org>, 
Model Driven Development sl <gvSIGi18n@ModelDD.org>,
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.gvSIGi18n.config import *

##code-section module-header #fill in your manual code here

import sys
import traceback
import logging

import transaction

from Products.CMFCore       import permissions
from Products.CMFCore.utils  import getToolByName



from TRAElemento_Constants                 import *
from TRAElemento_Constants_Activity        import *
from TRAElemento_Constants_Configurations  import *
from TRAElemento_Constants_Contributions   import *
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

from TRAImportarExportar_Constants import *

from TRAElemento_Permission_Definitions import cBoundObject
from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_CreateTRAContribuciones

from TRAProcessErrorException import TRAProcessErrorException


##/code-section module-header



##code-section after-local-schema #fill in your manual code here



##/code-section after-local-schema



##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAColeccionContribuciones_Operaciones:
    """
    """
    security = ClassSecurityInfo()

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    
    

                    

    security.declarePrivate( 'pAllSubElements_into')    
    def pAllSubElements_into( self, theCollection, theAdditionalParams=None):
        if theCollection == None:
            return self
        theCollection.append( self)
        
        
        unosElementos = self.fObtenerTodasContribuciones()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pAllSubElements_into( theCollection,theAdditionalParams=theAdditionalParams)
        
        return self
            
    
    



    security.declarePrivate( 'pForAllElementsDo_recursive')    
    def pForAllElementsDo_recursive( self, theLambda=None, thePloneLambda=None,):
        if not theLambda:
            return self
        
        theLambda( self)

        unosElementos = self.fObtenerTodasContribuciones()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda, thePloneLambda)
                
        if thePloneLambda:
            self.pForAllElementsPloneDo( thePloneLambda)
        
        return self
            
            
        
        
        
    
    security.declareProtected( permissions.View, 'fObtenerTodasContribuciones')
    def fObtenerTodasContribuciones( self, ):
        """Retrieve all contained elements of type TRAContribuciones.
        
        """
        unosElementos = self.fObjectValues( cNombreTipoTRAContribuciones) 
        return unosElementos
         
          
    
    

    
    
    
    security.declarePrivate( 'fNewVoidProgressResult_Contributions')
    def fNewVoidProgressResult_Contributions( self, ):
        unResult = self.fNewVoidProgressResult()
        unResult.update( {
            'elemento_contribuciones_meta_type':      '',
            'elemento_contribuciones_title':          '',
            'elemento_contribuciones_description':    '',
            'elemento_contribuciones_path':           '',
            'elemento_contribuciones_URL':            '',
            'elemento_contribuciones_UID':            '',
        })
        return unResult
                
             
        

    security.declareProtected( permissions.ManagePortal, 'fCreateProgressHandlerFor_Contributions')
    def fCreateProgressHandlerFor_Contributions( self, 
        theAdditionalParams     =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Request creation of a report Contributions long-lived process control handler, to be executed later.
        
        """


         

            
        def fContributionsLoop_lambda( theElement, theProcessControlManager, theAdditionalParmsHere):        
                    
            aCatalogo = theElement.getCatalogo()
            if aCatalogo == None:
                return None
            
            unaColeccionContribuciones = aCatalogo.fObtenerColeccionContribuciones()
            if unaColeccionContribuciones == None:
                return None
            
                    
            unaColeccionContribuciones.fCrearContribuciones(
                theProcessControlManager =theProcessControlManager,
                thePermissionsCache      =None, 
                theRolesCache            =None, 
                theParentExecutionRecord =None
            )
            
            return None        

    
        
        
        
        unExecutionRecord = self.fStartExecution( 'method',  'fCreateProgressHandlerFor_Contributions', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }, ) 
                
        aThereWasException = False
        
        try:
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)

            aResult = self.fNewVoidCreateProgressHandlerResult()
                
            try:
                
                
                unCatalogoRaiz = self.getCatalogo()           
                if unCatalogoRaiz == None:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_internal_Missing_RootCatalog', "Internal error: missing root translations catalog-."),
                    })
                    return aResult
                
                unaColeccionProgresos = unCatalogoRaiz.fObtenerColeccionProgresos()
                if unaColeccionProgresos == None:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_internal_Missing_progresses_collection', "Internal error: missing progresses collection-."),
                    })
                    return aResult
                            
                aContributionsResult = self.fNewVoidProgressResult_Contributions()

                
                aProgressElement = None
                aProgressHandler = None
            
                aMetaType = 'UnknownType'
                try:
                    aMetaType = self.meta_type
                except:
                    aMetaType = self.__class__.__name
                if not aMetaType:
                    aMetaType = 'UnknownType'
                
                aStartDateTimeNowTextual = self.fDateTimeNowTextual()
                aContributionsResult[ 'process_type']           = cTRAProgress_ProcessType_Contributions
                aContributionsResult[ 'start_date_time_string'] = aStartDateTimeNowTextual
                aContributionsResult[ 'date_time_now_string']   = aStartDateTimeNowTextual
                aContributionsResult[ 'element_type']           = aMetaType
                aContributionsResult[ 'element_title']          = self.Title()
                aContributionsResult[ 'element_path' ]          = self.fPhysicalPathString()
                aContributionsResult[ 'element_UID' ]           = self.UID()
                aContributionsResult[ 'last_element_type']      = ''
                aContributionsResult[ 'last_element_title']     = ''
                aContributionsResult[ 'last_element_path']      = ''
                aContributionsResult[ 'last_element_UID']       = ''
                
                aMemberId = self.fGetMemberId()
                aContributionsResult[ 'member_id'] = aMemberId
                
                aContributionsResult[ 'TRACatalogo_title']      = unCatalogoRaiz.Title()
                aContributionsResult[ 'TRACatalogo_path' ]      = unCatalogoRaiz.fPathDelRaiz()
                aContributionsResult[ 'TRACatalogo_UID' ]       = unCatalogoRaiz.UID()
                
                    
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_CreateTRAContribuciones, 
                    theElementsBindings     = { cBoundObject: self,},
                    theRulesToCollect       = [ ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord
                )
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    aResult.update( {
                        'success':     False,
                        'condition':   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_user_can_NOT_ReportContributions', "You can not request a report of Contributionns by users.-."),
                    })
                    return aResult

                


                aProgressHandlerCreationResult = unaColeccionProgresos.fCreateNewProgressAndHandlerForElement(  
                    theInitialElement       =self, 
                    theProcessType          =cTRAProgress_ProcessType_Contributions, 
                    theTimestamp            =aStartDateTimeNowTextual,
                    theResult               =aContributionsResult, 
                    theLoopLambda           =fContributionsLoop_lambda,
                    theElementLambda        =None,
                    theElementPloneLambda   =None,
                    theFinalizeLambda       =None,
                    theLockCatalog          =True,
                    thePermissionsCache     =unPermissionsCache, 
                    theRolesCache           =unRolesCache, 
                    theParentExecutionRecord=unExecutionRecord,)
                if ( not aProgressHandlerCreationResult) or not aProgressHandlerCreationResult.get( 'success', False):
                    aResult.update( {
                        'success':    False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_TRAProgress_not_created_for_TRAContribucion_msgid', "Error creating Progress element for Contributions report-."),
                    })
                    return aResult     
                
                
                aProgressElement = aProgressHandlerCreationResult.get( 'progress_element', None)
                if ( aProgressElement == None):
                    aResult = { 
                        'success':   False, 
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorProgressElementNotKnownByImportProcessElement', "Progress element is not known by progress handler-"),
                    }
                    return aResult
                
                aProgressHandler = aProgressHandlerCreationResult.get( 'progress_handler', None)
                if not aProgressHandler:
                    aResult = { 
                        'success':   False, 
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorImportProgressHandlerNotFound', "Import Progress Handler has not been found-"),
                    }
                    return aResult

                aProgressHandlerKey = aProgressHandlerCreationResult.get( 'progress_handler_key', None)
                if not aProgressHandlerKey:
                    aResult = { 
                        'success':   False, 
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorImport_NoProgressHandlerKey', "Import has no Progress Handler Key-"),
                    }
                    return aResult

                
                aResult.update( {
                    'success':               True,
                    'condition':             '',
                    'progress_element':      aProgressElement,
                    'progress_handler':      aProgressHandler,
                    'progress_handler_key':  aProgressHandlerKey,
                })
                
                return aResult
            
            
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                aThereWasException = True
                unInformeExcepcion = ''
                try:
                    unInformeExcepcion += 'Exception during fCreateProgressHandlerFor_Contributions of element %s %s at %s\n'  % (  self.meta_type(), self.Title(), self.fPhysicalPathString())
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
                
                aContributionsResult[ 'success'] = False
                aContributionsResult[ 'exception_date_time_string'] = self.fDateTimeNowTextual()
                aContributionsResultDump = ''
                try:
                    aContributionsResultDump = self.fProgressResult_dump( aContributionsResult)
                except:
                    None
                if aContributionsResultDump:
                    unInformeExcepcion += aContributionsResultDump
                
                aContributionsResult[ 'exception_report'] = unInformeExcepcionWOResult

                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
    
                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                aResult = { 
                    'success':    False, 
                    'condition':  '%s\n%s' % (   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_Exception_msgid', "Exception.-"), unInformeExcepcion, ),
                }
                return aResult
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
           
            
    
    
    
    

    security.declarePrivate( 'fCrearContribuciones')
    def fCrearContribuciones( self, 
        theProcessControlManager =None,
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):
        """Create a new instance of TRAContribuciones, capturing a summary of contributing users and dates, for each language and in total.
        
        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fCrearContribuciones', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }, ) 
        
        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators import cModificationKind_CreateSubElement, cModificationKind_Create
        
        try:
            
            unImportResult = theProcessControlManager.vResult
            if not unImportResult:
                return None
            
            
            unCatalogo = self.getCatalogo()
            if unCatalogo == None:
                if theProcessControlManager:
                    raise TRAProcessErrorException( 'gvSIGi18n_MissingParameters_internal_error_msgid', 'getCatalogo == None',)
                return None
                                    
        
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
            
            
            unUseCaseQueryResult = self.fUseCaseAssessment(  
                theUseCaseName          = cUseCase_CreateTRAContribuciones, 
                theElementsBindings     = { cBoundObject: self,},
                thePredicateOverrides   = { unCatalogo.UID(): { 'fAllowWrite': True, }, self.UID(): { 'fAllowWrite': True,},},
                thePermissionsCache     = unPermissionsCache, 
                theRolesCache           = unRolesCache, 
                theParentExecutionRecord= unExecutionRecord
            ) 
            if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                if theProcessControlManager:
                    raise TRAProcessErrorException( 'gvSIGi18n_error_user_can_NOT_ReportContributions', cUseCase_CreateTRAContribuciones,)
                return None

           
            
            transaction.commit( )
            
            
            unInformeContribuciones = unCatalogo.fElaborarInformeContribuciones( 
                theProcessControlManager    =theProcessControlManager,
                thePermissionsCache         =unPermissionsCache, 
                theRolesCache               =unRolesCache, 
                theParentExecutionRecord    =unExecutionRecord,
            )
            transaction.commit( )
            
            
            if not unInformeContribuciones:
                if theProcessControlManager:
                    raise TRAProcessErrorException( 'gvSIGi18n_error_FailureEllaboratingContributionsReport', '',)
                return None
            
            
            if not unInformeContribuciones.get( 'success', False):
                if theProcessControlManager:
                    unErrorMessage = unInformeContribuciones.get( 'error', '')
                    if not unErrorMessage:
                        unErrorMessage = 'Error'
                        
                    unErrorDetails = unInformeContribuciones.get( 'exception', '')
                    if not unErrorDetails:
                        unErrorDetails = ''
                        
                    raise TRAProcessErrorException( unErrorMessage, unErrorDetails,)
                return None
            
        
            unaFechaInforme  = unInformeContribuciones.get( 'report_date', '')
            unUsuarioInforme = unInformeContribuciones.get( 'reporting_user', '')
            
            unaIdElementoProgreso = theProcessControlManager.vProgressElementId
            
                
            aReport = self.fModelDDvlPloneTool().fModelDDvlPloneTool_Mutators( self).fNewVoidCreateElementReport()
            
            
            unAhoraString = self.fDateTimeNowTextual()
            unAhoraParaId = unAhoraString.replace( ':', '-').replace( ' ', '-')
            unMemberId    = self.fGetMemberId()
            
            
            unTitleContribucionesACrear = '%s by %s' % ( unAhoraString, unMemberId,)
            unIdContribucionesACrear    = '%s-%s'    % ( unAhoraParaId, unMemberId,)
      
            unContribucionesExistente = self.getElementoPorID( unIdContribucionesACrear)
            unCountIds = 0
            while not ( unContribucionesExistente == None):
                unCountIds += 1
                unTitleContribucionesACrear = '%s by %s (%d)' % ( unAhoraString, unMemberId, unCountIds)
                unIdContribucionesACrear    = '%s-%s-%d'      % ( unAhoraParaId, unMemberId, unCountIds)
                
                unContribucionesExistente = self.getElementoPorID( unIdContribucionesACrear)

            unInformeContribucionesString = self.fReprAsString( unInformeContribuciones)    
                
            aNewContribucionesAttrsDict = { 
                'title':                          unTitleContribucionesACrear,
                'informeContribuciones':          unInformeContribucionesString, 
                'fechaFinProceso':                unaFechaInforme,     
                'usuarioInformador':              unUsuarioInforme,
                'identificadorElementoProgreso':  unaIdElementoProgreso,
            }
            
            unaIdNuevoContribuciones = self.invokeFactory( cNombreTipoTRAContribuciones, unIdContribucionesACrear, **aNewContribucionesAttrsDict)
            if not unaIdNuevoContribuciones:
                if theProcessControlManager:
                    raise TRAProcessErrorException( 'creation_failure', cNombreTipoTRAContribuciones,)
                return None
            
            unNuevoContribuciones = self.getElementoPorID( unaIdNuevoContribuciones)
            if not unNuevoContribuciones:
                if theProcessControlManager:
                    raise TRAProcessErrorException( 'new_element_not_found', unaIdNuevoContribuciones,)
                return None

            
            unNuevoContribuciones.manage_fixupOwnershipAfterAdd()
          
            unNuevoContribuciones.pSetPermissions()
            
            transaction.commit()
            
            theProcessControlManager.pProcessStep( self, { cNombreTipoTRAColeccionContribuciones: 1,}, { cNombreTipoTRAColeccionContribuciones: 1, cNombreTipoTRAContribuciones: 1,})

            
            unResultadoNuevoContribuciones = self.fModelDDvlPloneTool().fRetrieveTypeConfig( 
                theTimeProfilingResults     =None,
                theElement                  =unNuevoContribuciones, 
                theParent                   =None,
                theParentTraversalName      ='',
                theTypeConfig               =None, 
                theAllTypeConfigs           =None, 
                theViewName                 ='', 
                theRetrievalExtents         =[ 'traversals', ],
                theWritePermissions         =None,
                theFeatureFilters           ={ 'attrs': [ 'title',], 'aggregations': [], 'relations': [], 'do_not_recurse_collections': True,}, 
                theInstanceFilters          =None,
                theTranslationsCaches       =None,
                theCheckedPermissionsCache  =unPermissionsCache,
                theAdditionalParams         =None                
            )
            if ( not unResultadoNuevoContribuciones) or ( unResultadoNuevoContribuciones.get( 'object', None) == None):
                if theProcessControlManager:
                    raise TRAProcessErrorException( 'new_element_retrieval_failed', unaIdNuevoContribuciones,)
                return None

            unImportResult[ 'elemento_contribuciones_meta_type']   = unResultadoNuevoContribuciones.get( 'meta_type', '')
            unImportResult[ 'elemento_contribuciones_title']       = unResultadoNuevoContribuciones.get( 'title', '')
            unImportResult[ 'elemento_contribuciones_description'] = unResultadoNuevoContribuciones.get( 'description', '')
            unImportResult[ 'elemento_contribuciones_path']        = unResultadoNuevoContribuciones.get( 'path', '')
            unImportResult[ 'elemento_contribuciones_URL']         = unResultadoNuevoContribuciones.get( 'url', '')
            unImportResult[ 'elemento_contribuciones_UID']         = unResultadoNuevoContribuciones.get( 'UID', '')
            
            
            
            
             
            aModelDDvlPloneTool_Mutators = self.fModelDDvlPloneTool().fModelDDvlPloneTool_Mutators( self)
                
            aCreateElementReport = aModelDDvlPloneTool_Mutators.fNewVoidCreateElementReport()
            aCreateElementReport.update( { 'effect': 'created', 'new_object_result': unResultadoNuevoContribuciones, })
            
            someFieldReports    = aCreateElementReport[ 'field_reports']
            aFieldReportsByName = aCreateElementReport[ 'field_reports_by_name']
            
            aReportForField = { 'attribute_name': 'id',          'effect': 'changed', 'new_value': unaIdNuevoContribuciones, 'previous_value': '',}
            someFieldReports.append( aReportForField)            
            aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
            
            aReportForField = { 'attribute_name': 'title',       'effect': 'changed', 'new_value': unTitleContribucionesACrear,           'previous_value': '',}
            someFieldReports.append( aReportForField)            
            aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField

            aModelDDvlPloneTool_Mutators.pSetAudit_Creation( self,           cModificationKind_CreateSubElement, aCreateElementReport, theUseCounter=True)       
            aModelDDvlPloneTool_Mutators.pSetAudit_Creation( unNuevoContribuciones, cModificationKind_Create,           aCreateElementReport)       
         
            self.pFlushCachedTemplates()   
            unNuevoContribuciones.pFlushCachedTemplates()   
                
            unCatalogo = self.getCatalogo()
            if not ( unCatalogo == None):
                unCatalogo.pFlushCachedTemplates()            
                        
            aReport.update( { 'effect': 'created', 'new_object_result': unResultadoNuevoContribuciones, })

            transaction.commit( )

            logging.getLogger( 'gvSIGi18n').info("COMMIT") 
            
            return aReport
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
           
        
     
                             
    
    
    
                                

# end of class TRAColeccionContribuciones_Operaciones

##code-section module-footer #fill in your manual code here
##/code-section module-footer



