# -*- coding: utf-8 -*-
#
# File: TRACatalogo_Mutators.py
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




from TRAElemento_Permission_Definitions import cBoundObject
from TRAElemento_Permission_Definitions import cTRAUserGroups_Catalogo, cTRAUserGroups_Catalogo_AuthorizedOnIndividualIdiomas, cTRAUserGroups_Catalogo_AuthorizedOnIndividualModulos

from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_LockTRACatalogo, cUseCase_UnlockTRACatalogo



  



class TRACatalogo_Mutators:
    """
    """
    security = ClassSecurityInfo()

    
        
    

    
    security.declareProtected( permissions.ModifyPortalContent, 'fBloquearCatalogo')
    def fBloquearCatalogo( self , 
        theCheckPermissions      =True, 
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fBloquearCatalogo', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators import cModificationKind_CreateSubElement, cModificationKind_Create, cModificationKind_ChangeValues
        
        try:
            
            try:
                
                if theCheckPermissions:
                
                    unPermissionsCache = fDictOrNew( thePermissionsCache)
                    unRolesCache       = fDictOrNew( theRolesCache)
                
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
                    
                    
                    aModelDDvlPloneTool_Mutators = self.fModelDDvlPloneTool().fModelDDvlPloneTool_Mutators( self)
                   
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
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   

                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return False
        
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

            
 
    

    
    security.declareProtected( permissions.ModifyPortalContent, 'fDesbloquearCatalogo')
    def fDesbloquearCatalogo( self , 
        theCheckPermissions=True, 
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fDesbloquearCatalogo', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators import cModificationKind_CreateSubElement, cModificationKind_Create, cModificationKind_ChangeValues

        try:
            
            try:
                
                if theCheckPermissions:
                
                    unPermissionsCache = fDictOrNew( thePermissionsCache)
                    unRolesCache       = fDictOrNew( theRolesCache)
                
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
                    
                    aModelDDvlPloneTool_Mutators = self.fModelDDvlPloneTool().fModelDDvlPloneTool_Mutators( self)
                   
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
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   

                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return False
        
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

            
 
        
    
            
            
            
            
            

    
    
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
            
  
  
            

    security.declarePrivate( 'fCambiarNombresModulosCadena')    
    def fCambiarNombresModulosCadena( self, 
        theSimboloCadena, 
        theNombresModulos, 
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
                
            unResultado = unaCadena.fCambiarNombresModulos(  
                theNombresModulos, 
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
            
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
            
             
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
                
                unosExistingGroupRoles    = list( theIdioma.fLocalRolesForUserId( unUserGroupId))[:]
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
                
                unosExistingGroupRoles    = list( theModulo.fLocalRolesForUserId( unUserGroupId))[:]
                unosNonExistingGroupRoles = list( set( unosRolesToSet) - set( unosExistingGroupRoles))
                
                if unosNonExistingGroupRoles:
                         
                    theModulo.manage_addLocalRoles( unUserGroupId, tuple( unosNonExistingGroupRoles))
                    # ACV 200903212354 learned from Products.CMFCore.MembershipTool.MembershipTool.setLocalRoles()                     
                    theModulo.reindexObjectSecurity()
                    
        return True                        
                   
        
    
    
    
    
    
                
 