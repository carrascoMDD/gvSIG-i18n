# -*- coding: utf-8 -*-
#
# File: TRAColeccionInformes_Operaciones.py
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
from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_CreateTRAInforme


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
    def pAllSubElements_into( self, theCollection, theAdditionalParams=None):
        if theCollection == None:
            return self
        theCollection.append( self)
        
        
        unosElementos = self.fObtenerTodosInformes()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pAllSubElements_into( theCollection,theAdditionalParams=theAdditionalParams)
        
        return self
            
    
    



    security.declarePrivate( 'pForAllElementsDo_recursive')    
    def pForAllElementsDo_recursive( self, theLambda=None, thePloneLambda=None,):
        if not theLambda:
            return self
        
        theLambda( self)

        unosElementos = self.fObtenerTodosInformes()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda, thePloneLambda)
                
        if thePloneLambda:
            self.pForAllElementsPloneDo( thePloneLambda)
        
        return self
            
            
        
        
        
    
    security.declareProtected( permissions.View, 'fObtenerTodosInformes')
    def fObtenerTodosInformes( self, ):
        """Retrieve all contained elements of type TRAInforme.
        
        """
        unosElementos = self.fObjectValues( cNombreTipoTRAInforme) 
        return unosElementos
         
          
    

    security.declareProtected( permissions.AddPortalContent, 'fCrearInforme')
    def fCrearInforme( self, 
        theUseCaseQueryResult   =None,
        theCheckPermissions     =True,
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Create a new instance of TRAInforme, capturing a summary of translations by languages and detailed report by modules and languages.
        
        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fCrearInforme', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }, ) 
        
        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators import cModificationKind_CreateSubElement, cModificationKind_Create
        
        try:
        
            aReport = self.fModelDDvlPloneTool().fModelDDvlPloneTool_Mutators( self).fNewVoidCreateElementReport()
            
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
            
            
            unUseCaseQueryResult = self.fUseCaseAssessment(  
                theUseCaseName          = cUseCase_CreateTRAInforme, 
                theElementsBindings     = { cBoundObject: self,},
                theRulesToCollect       = [ 'languages', 'modules',], 
                thePermissionsCache     = unPermissionsCache, 
                theRolesCache           = unRolesCache, 
                theParentExecutionRecord= unExecutionRecord
            ) 
            if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
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
            
            
            aModelDDvlPloneTool_Mutators = self.fModelDDvlPloneTool().fModelDDvlPloneTool_Mutators( self)
                
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
                unCatalogo.pFlushCachedTemplates()            
                        
            aReport.update( { 'effect': 'created', 'new_object_result': unResultadoNuevoInforme, })

            transaction.commit( )

            logging.getLogger( 'gvSIGi18n').info("COMMIT") 
            
            return aReport
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
           
        
     
                             
    
    
    
                                

# end of class TRAColeccionInformes_Operaciones

##code-section module-footer #fill in your manual code here
##/code-section module-footer



