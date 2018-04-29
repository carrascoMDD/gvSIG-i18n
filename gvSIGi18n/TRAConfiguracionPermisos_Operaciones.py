# -*- coding: utf-8 -*-
#
# File: TRAConfiguracionPermisos_Operaciones.py
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


from TRARoles               import *

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


from TRAElemento_Permission_Definitions                import cBoundObject

from TRAElemento_Permission_Definitions_UseCaseNames   import cUseCase_ActivateTRAConfiguracionPermisos

##/code-section module-header



##code-section after-local-schema #fill in your manual code here



##/code-section after-local-schema



##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAConfiguracionPermisos_Operaciones:
    """
    """
    security = ClassSecurityInfo()

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    
    
    security.declarePrivate( 'fConfigurationAttributeNames')    
    def fConfigurationAttributeNames( self,):
        someAttributeNames = [
            'esAnonymousTRAManager',
            'esAnonymousTRACoordinator',
            'esAnonymousTRADeveloper',
            'esAnonymousTRAReviewer',
            'esAnonymousTRATranslator',
            'esAnonymousTRAVisitor',
            'esAuthenticatedTRAManager',
            'esAuthenticatedTRACoordinator',
            'esAuthenticatedTRADeveloper',
            'esAuthenticatedTRAReviewer',
            'esAuthenticatedTRATranslator',
            'esAuthenticatedTRAVisitor',
            'esMemberTRAManager',
            'esMemberTRACoordinator',
            'esMemberTRADeveloper',
            'esMemberTRAReviewer',
            'esMemberTRATranslator',
            'esMemberTRAVisitor',
            'esReviewerTRAManager',
            'esReviewerTRACoordinator',
            'esReviewerTRADeveloper',
            'esReviewerTRAReviewer',
            'esReviewerTRATranslator',
            'esReviewerTRAVisitor',
            'esOwnerTRAManager',
            'esOwnerTRACoordinator',
            'esOwnerTRADeveloper',
            'esOwnerTRAReviewer',
            'esOwnerTRATranslator',
            'esOwnerTRAVisitor',
            'esManagerTRAManager',
            'esManagerTRACoordinator',
            'esManagerTRADeveloper',
            'esManagerTRAReviewer',
            'esManagerTRATranslator',
            'esManagerTRAVisitor',
        ]
        return someAttributeNames
         
    
    
    
        
    
        
    

        

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
            
            
        
      
    security.declarePrivate( 'fAdditionalZopeRolesForTRARoles')    
    def fAdditionalZopeRolesForTRARoles( self,):
        
        someAdditionalRolesForTRARoles = { }
        
        someAdditionalRolesForTRAManager = [ ]
        someAdditionalRolesForTRARoles[ cTRAManager_role] = someAdditionalRolesForTRAManager
        
        someAdditionalRolesForTRACoordinator = [ ]
        someAdditionalRolesForTRARoles[ cTRACoordinator_role] = someAdditionalRolesForTRACoordinator
        
        someAdditionalRolesForTRADeveloper = [ ]
        someAdditionalRolesForTRARoles[ cTRADeveloper_role] = someAdditionalRolesForTRADeveloper
        
        someAdditionalRolesForTRAReviewer = [ ]
        someAdditionalRolesForTRARoles[ cTRAReviewer_role] = someAdditionalRolesForTRAReviewer
        
        someAdditionalRolesForTRATranslator = [ ]
        someAdditionalRolesForTRARoles[ cTRATranslator_role] = someAdditionalRolesForTRATranslator
        
        someAdditionalRolesForTRAVisitor = [ ]
        someAdditionalRolesForTRARoles[ cTRAVisitor_role] = someAdditionalRolesForTRAVisitor
        
            
            
        if self.getEsAnonymousTRAManager() == cTRABooleanSi:
            someAdditionalRolesForTRAManager.append( cZopeAnonymous_role)

        if self.getEsAnonymousTRACoordinator() == cTRABooleanSi:
            someAdditionalRolesForTRACoordinator.append( cZopeAnonymous_role)

        if self.getEsAnonymousTRADeveloper() == cTRABooleanSi:
            someAdditionalRolesForTRADeveloper.append( cZopeAnonymous_role)

        if self.getEsAnonymousTRAReviewer() == cTRABooleanSi:
            someAdditionalRolesForTRAReviewer.append( cZopeAnonymous_role)

        if self.getEsAnonymousTRATranslator() == cTRABooleanSi:
            someAdditionalRolesForTRATranslator.append( cZopeAnonymous_role)

        if self.getEsAnonymousTRAVisitor() == cTRABooleanSi:
            someAdditionalRolesForTRAVisitor.append( cZopeAnonymous_role)

            
        if self.getEsAuthenticatedTRAManager() == cTRABooleanSi:
            someAdditionalRolesForTRAManager.append( cZopeAuthenticated_role)

        if self.getEsAuthenticatedTRACoordinator() == cTRABooleanSi:
            someAdditionalRolesForTRACoordinator.append( cZopeAuthenticated_role)

        if self.getEsAuthenticatedTRADeveloper() == cTRABooleanSi:
            someAdditionalRolesForTRADeveloper.append( cZopeAuthenticated_role)

        if self.getEsAuthenticatedTRAReviewer() == cTRABooleanSi:
            someAdditionalRolesForTRAReviewer.append( cZopeAuthenticated_role)

        if self.getEsAuthenticatedTRATranslator() == cTRABooleanSi:
            someAdditionalRolesForTRATranslator.append( cZopeAuthenticated_role)

        if self.getEsAuthenticatedTRAVisitor() == cTRABooleanSi:
            someAdditionalRolesForTRAVisitor.append( cZopeAuthenticated_role)
            

        if self.getEsMemberTRAManager() == cTRABooleanSi:
            someAdditionalRolesForTRAManager.append( cZopeMember_role)

        if self.getEsMemberTRACoordinator() == cTRABooleanSi:
            someAdditionalRolesForTRACoordinator.append( cZopeMember_role)

        if self.getEsMemberTRADeveloper() == cTRABooleanSi:
            someAdditionalRolesForTRADeveloper.append( cZopeMember_role)

        if self.getEsMemberTRAReviewer() == cTRABooleanSi:
            someAdditionalRolesForTRAReviewer.append( cZopeMember_role)

        if self.getEsMemberTRATranslator() == cTRABooleanSi:
            someAdditionalRolesForTRATranslator.append( cZopeMember_role)

        if self.getEsMemberTRAVisitor() == cTRABooleanSi:
            someAdditionalRolesForTRAVisitor.append( cZopeMember_role)
            

        if self.getEsReviewerTRAManager() == cTRABooleanSi:
            someAdditionalRolesForTRAManager.append( cZopeReviewer_role)

        if self.getEsReviewerTRACoordinator() == cTRABooleanSi:
            someAdditionalRolesForTRACoordinator.append( cZopeReviewer_role)

        if self.getEsReviewerTRADeveloper() == cTRABooleanSi:
            someAdditionalRolesForTRADeveloper.append( cZopeReviewer_role)

        if self.getEsReviewerTRAReviewer() == cTRABooleanSi:
            someAdditionalRolesForTRAReviewer.append( cZopeReviewer_role)

        if self.getEsReviewerTRATranslator() == cTRABooleanSi:
            someAdditionalRolesForTRATranslator.append( cZopeReviewer_role)

        if self.getEsReviewerTRAVisitor() == cTRABooleanSi:
            someAdditionalRolesForTRAVisitor.append( cZopeReviewer_role)
            

        if self.getEsOwnerTRAManager() == cTRABooleanSi:
            someAdditionalRolesForTRAManager.append( cZopeOwner_role)

        if self.getEsOwnerTRACoordinator() == cTRABooleanSi:
            someAdditionalRolesForTRACoordinator.append( cZopeOwner_role)

        if self.getEsOwnerTRADeveloper() == cTRABooleanSi:
            someAdditionalRolesForTRADeveloper.append( cZopeOwner_role)

        if self.getEsOwnerTRAReviewer() == cTRABooleanSi:
            someAdditionalRolesForTRAReviewer.append( cZopeOwner_role)

        if self.getEsOwnerTRATranslator() == cTRABooleanSi:
            someAdditionalRolesForTRATranslator.append( cZopeOwner_role)

        if self.getEsOwnerTRAVisitor() == cTRABooleanSi:
            someAdditionalRolesForTRAVisitor.append( cZopeOwner_role)
            

        if self.getEsManagerTRAManager() == cTRABooleanSi:
            someAdditionalRolesForTRAManager.append( cZopeManager_role)

        if self.getEsManagerTRACoordinator() == cTRABooleanSi:
            someAdditionalRolesForTRACoordinator.append( cZopeManager_role)

        if self.getEsManagerTRADeveloper() == cTRABooleanSi:
            someAdditionalRolesForTRADeveloper.append( cZopeManager_role)

        if self.getEsManagerTRAReviewer() == cTRABooleanSi:
            someAdditionalRolesForTRAReviewer.append( cZopeManager_role)

        if self.getEsManagerTRATranslator() == cTRABooleanSi:
            someAdditionalRolesForTRATranslator.append( cZopeManager_role)

        if self.getEsManagerTRAVisitor() == cTRABooleanSi:
            someAdditionalRolesForTRAVisitor.append( cZopeManager_role)
            

        return someAdditionalRolesForTRARoles
    
    
    
    
                                
   
    security.declarePrivate( 'fActivatePermissionsConfiguration')    
    def fActivatePermissionsConfiguration( self,
        thePermissionsCache        =None,
        theRolesCache              =None,
        theParentExecutionRecord   =None,):
            
        
   
        unExecutionRecord = self.fStartExecution( 'method',  'pActivatePermissionsConfiguration', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }, ) 
        
        aThereWasException = False
        
        try:
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
            
            try:            
                
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_ActivateTRAConfiguracionPermisos, 
                    theElementsBindings     = { cBoundObject: self,},
                    theRulesToCollect       = [ ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord
                )
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    return False
                
                self.pClearPermissionsByElementType()
                self.pClearUseCaseSpecificationsForTRACatalogsByName()
                self.pClearStateChangeActionRoles()
                
            
                return True
            
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                aThereWasException = True
                unInformeExcepcion = ''
                try:
                    unInformeExcepcion += 'Exception during pActivatePermissionsConfiguration\n'  
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
                

                aRecatalogResult[ 'exception_report'] = unInformeExcepcion[:]

                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
    
                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                

                return False
            
            return True
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
           
        
                       
                            
            

# end of class TRAConfiguracionVarios_Operaciones

##code-section module-footer #fill in your manual code here
##/code-section module-footer



