# -*- coding: utf-8 -*-
#
# File: TRAColeccionInformes_Operaciones.py
#
# Copyright (c) 2009 by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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



from TRAElemento_Constants import *

from TRAImportarExportar_Constants import *

from TRAElemento_Permission_Definitions import cUseCase_CreateTRAInforme
from TRAElemento_Permission_Definitions import cBoundObject


##/code-section module-header



##code-section after-local-schema #fill in your manual code here



##/code-section after-local-schema



##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAColeccionInformes_Operaciones:
    """
    """
    security = ClassSecurityInfo()

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    
    
        

    security.declarePrivate( 'pAllSubElements_into')    
    def pAllSubElements_into( self, theCollection, theAdditionalParms=None):
        if theCollection == None:
            return self
        theCollection.append( self)
        
        
        unosElementos = self.fObtenerTodosInformes()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pAllSubElements_into( theCollection,theAdditionalParms=theAdditionalParms)
        
        return self
            
    
    



    security.declarePrivate( 'pForAllElementsDo_recursive')    
    def pForAllElementsDo_recursive( self, theLambda):
        if not theLambda:
            return self
        
        theLambda( self)

        unosElementos = self.fObtenerTodosInformes()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda)
        
        return self
            
            
        
        
        
    
    security.declareProtected( permissions.View, 'fObtenerTodosInformes')
    def fObtenerTodosInformes( self, ):
        """Retrieve all contained elements of type TRAInforme.
        
        """
        unosElementos = self.objectValues( cNombreTipoTRAInforme) 
        return unosElementos
         
          
    

    security.declareProtected( permissions.AddPortalContent, 'fCrearInforme')
    def fCrearInforme( self, 
        theUseCaseQueryResult   =None,
        theCheckPermissions     =True,
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """TRAInforme private factory method that does not check security constraints, that must have laready been checked by caller.
        
        """
        unExecutionRecord = self.fStartExecution( 'method',  'fCrearInforme', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }, ) 
        
        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators import ModelDDvlPloneTool_Mutators,cModificationKind_CreateSubElement, cModificationKind_Create
        
        try:
        
            aReport = ModelDDvlPloneTool_Mutators().fNewVoidCreateElementReport()
            
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
            
            unUseCaseQueryResult = theUseCaseQueryResult
            if theCheckPermissions or not unUseCaseQueryResult or not ( unUseCaseQueryResult.get( 'use_case_name', '') == cUseCase_CreateTRAInforme):
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_CreateTRAInforme, 
                    theElementsBindings     = { cBoundObject: self,},
                    theRulesToCollect       = [ 'languages', 'modules',], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord
                ) 

            if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                return unInforme

            
            
            if not theUseCaseQueryResult or not theUseCaseQueryResult.get( 'success', False):
                aReport.update( { 'effect': 'error', 'failure': 'use_case_query_failed', })
                return aReport    
            
            
            unAhoraString = self.fDateTimeNowTextual()
            unAhoraParaId = unAhoraString.replace( ':', '-').replace( ' ', '-')
            unMemberId    = self.fGetMemberId()
            
            
            unTitleInformeACrear = '%s by %s' % ( unAhoraString, unMemberId,)
            unIdInformeACrear    = '%s-%s'    % ( unAhoraParaId, unMemberId,)
      
            unInformeExistente = self.getElementoPorID( unIdInformeACrear)
            unCountIds = 0
            while not ( unInformeExistente == None):
                unCountIds += 1
                unTitleInformeACrear = '%s by %s (%d)' % ( unAhoraString, unMemberId, unCountIds)
                unIdInformeACrear    = '%s-%s-%d'      % ( unAhoraParaId, unMemberId, unCountIds)
                
                unInformeExistente = self.getElementoPorID( unIdInformeACrear)
                
                
            aNewInformeAttrsDict = { 
                'title': unTitleInformeACrear,
            }
            
            unaIdNuevoInforme = self.invokeFactory( cNombreTipoTRAInforme, unIdInformeACrear, **aNewInformeAttrsDict)
            if not unaIdNuevoInforme:
                aReport.update( { 'effect': 'error', 'failure': 'creation_failure', })
                return aReport
                     
            unNuevoInforme = self.getElementoPorID( unaIdNuevoInforme)
            if not unNuevoInforme:
                aReport.update( { 'effect': 'error', 'failure': 'new_element_not_found', })
                return aReport
            
            unNuevoInforme.manage_fixupOwnershipAfterAdd()
          
            unNuevoInforme.pSetPermissions()

            
            unResultadoNuevoInforme = self.fModelDDvlPloneTool().fRetrieveTypeConfig( 
                theTimeProfilingResults     =None,
                theElement                  =unNuevoInforme, 
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
            if ( not unResultadoNuevoInforme) or ( unResultadoNuevoInforme.get( 'object', None) == None):
                aReport.update( { 'effect': 'error', 'failure': 'new_element_retrieval_failed', })
                return aReport
            
            
                
        
            unNuevoInforme.fElaborarInforme(                
                theUseCaseQueryResult       =unUseCaseQueryResult,
                theForceEllaboration        =True, 
                theCheckPermissions         =False, 
                thePermissionsCache         =unPermissionsCache, 
                theRolesCache               =unRolesCache, 
                theParentExecutionRecord    =unExecutionRecord,
            )
            
            
            aModelDDvlPloneTool_Mutators = ModelDDvlPloneTool_Mutators()
                
            aCreateElementReport = aModelDDvlPloneTool_Mutators.fNewVoidCreateElementReport()
            aCreateElementReport.update( { 'effect': 'created', 'new_object_result': unResultadoNuevoInforme, })
            
            someFieldReports    = aCreateElementReport[ 'field_reports']
            aFieldReportsByName = aCreateElementReport[ 'field_reports_by_name']
            
            aReportForField = { 'attribute_name': 'id',          'effect': 'changed', 'new_value': unaIdNuevoInforme, 'previous_value': '',}
            someFieldReports.append( aReportForField)            
            aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
            
            aReportForField = { 'attribute_name': 'title',       'effect': 'changed', 'new_value': unTitleInformeACrear,           'previous_value': '',}
            someFieldReports.append( aReportForField)            
            aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField

            aModelDDvlPloneTool_Mutators.pSetAudit_Creation( self,           cModificationKind_CreateSubElement, aCreateElementReport, theUseCounter=True)       
            aModelDDvlPloneTool_Mutators.pSetAudit_Creation( unNuevoInforme, cModificationKind_Create,           aCreateElementReport)       
         
            self.pFlushCachedTemplates()   
            unNuevoInforme.pFlushCachedTemplates()   
                
            unCatalogo = self.getCatalogo()
            if not ( unCatalogo == None):
                unCatalogo.setUltimoInforme( unNuevoInforme)
                unCatalogo.pFlushCachedTemplates()            
                        
            aReport.update( { 'effect': 'created', 'new_object_result': unResultadoNuevoInforme, })

            transaction.commit( )

            logging.getLogger( 'gvSIGi18n::fCrearInforme').info("COMMIT") 
            
            return aReport
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
           
        
     
                             
    
    
    
                                

# end of class TRAColeccionSolicitudesCadenas_Operaciones

##code-section module-footer #fill in your manual code here
##/code-section module-footer



