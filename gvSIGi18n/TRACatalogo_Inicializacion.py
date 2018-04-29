# -*- coding: utf-8 -*-
#
# File: TRACatalogo_Inicializacion.py
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

##code-section module-header #fill in your manual code here


import sys
import traceback


from StringIO                       import StringIO


import logging

import transaction

from Acquisition                    import aq_get



from Products.ExternalMethod.ExternalMethod import ExternalMethod

from Products.ZCatalog.ZCatalog     import ZCatalog
from Products.ZCTextIndex.ZCTextIndex import PLexicon
from Products.ZCTextIndex.Lexicon   import CaseNormalizer
from Products.ZCTextIndex.Lexicon   import Splitter
from Products.ZCTextIndex.Lexicon   import StopWordRemover


from TRASplitter import TRASplitter



gCJKSplitter = None
try:
    from Products.CJKSplitter.CJKSplitter import CJKSplitter as gCJKSplitter
except:
    None
    
    



from Products.CMFCore               import permissions
from Products.CMFCore.utils         import getToolByName



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








from TRACatalogo_Inicializacion_Constants import *


from TRAElemento_Permission_Definitions import cBoundObject, cTRAUserGroups_Catalogo
from TRAElemento_Permission_Definitions import cTRAUserGroups_Catalogo_AuthorizedOnCatalogo, cTRAUserGroups_Catalogo_AuthorizedOnIndividualIdiomas, cTRAUserGroups_Catalogo_AuthorizedOnIndividualModulos

from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_InitializeTRACatalogo, cUseCase_VerifyTRACatalogo

# ACV 20090914 NOW approach: Simpler security schema: no user groups for languages or modules, shall assign local roles to users directly on the language or module element
# from TRAElemento_Permission_Definitions import cTRAUserGroups_AllIdiomas, cTRAUserGroups_Idioma, cTRAUserGroups_Modulo
# from TRAElemento_Permission_Definitions import cTRAUserGroups_AllIdiomas_AuthorizedOnColeccionIdiomas
# from TRAElemento_Permission_Definitions import cTRAUserGroups_AllModulos_AuthorizedOnColeccionModulos
# from TRAElemento_Permission_Definitions import cTRAUserGroups_Idioma_AuthorizedOnCatalogo, cTRAUserGroups_Idioma_AuthorizedOnIdioma
# from TRAElemento_Permission_Definitions import cTRAUserGroups_Modulo_AuthorizedOnCatalogo, cTRAUserGroups_Modulo_AuthorizedOnModulo




##/code-section module-header

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema


##code-section after-schema #fill in your manual code here



cLogInformeVerifyOrInit     = True



cTRAErrorMsgId_user_can_NOT_initialize_TRACatalogo  = 'user_can_NOT_initialize_TRACatalogo'

cTRAErrorMsgId_user_can_NOT_verify_TRACatalogo      = 'user_can_NOT_verify_TRACatalogo'





##/code-section after-schema

class TRACatalogo_Inicializacion:
    """
    """
    security = ClassSecurityInfo()


    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
# end of class TRACatalogo_Inicializacion

##code-section module-footer #fill in your manual code here




    
    security.declarePrivate( 'fNewVoidProgressResult_VerifyOrInitialize')
    def fNewVoidProgressResult_VerifyOrInitialize( self, ):
        unResult = self.fNewVoidProgressResult()
        unResult.update( {
            'verify_or_init_report':            { },
        })
        return unResult
                
      
    
    
    
                
    
    security.declarePrivate('fNewVoidInformeVerifyOrInit')
    def fNewVoidInformeVerifyOrInit( self):
        unInforme =  { 
            'process_type':            '',
            'translated_process_type': '',
            'allow_initialization':    False,
            'check_permissions':       False,
            'success':                 False,
            'condition':               '',
            'exception':               '',
            'ModelDDvlPlone':          {},
            'gvSIGi18nUI':             {},
            'gvSIGi18nTool':           {},
            'catalog':                 {},
            'progress_element_basic_info': {},
        }
        return unInforme
    
    
    
    security.declarePrivate('fNewVoidInformeVerifyOrInit_Catalog')
    def fNewVoidInformeVerifyOrInit_Catalog( self):
        unInforme = { 
            'success':              False,
            'condition':            '',
            'must_run_recatalog_elements': False,
            'allow_initialization': False,
            'check_permissions':    False,
            'element_meta_type':    '',
            'element_title':        '',
            'element_path':         '',
            'colecciones':          {},
            'singletons':           {},
            'catalogs_cadenas':     {}, 
            'catalogs_idiomas':     [],
            'user_groups_catalogo': {},
            # ACV 20090914 Simpler security schema: no user groups for languages or modules, shall assign local roles to users directly on the language or module element
            #'user_groups_all_idiomas':   {},
            #'user_groups_all_modulos':   {},
            #'user_groups_idiomas':   {},
            #'user_groups_modulos':   {},
        }
        return unInforme
    
    
   
    


        
    
    security.declarePrivate('fNewVoidInformeVerifyOrInitTodasCollections')
    def fNewVoidInformeVerifyOrInitTodasCollections( self):
        unInforme = {
            'type':         'collections',
            'success':      False,
            'container_type':            '',
            'container_title':           '',
            'container_path':            '',
            'collections':  [],
        }
        return unInforme    
    
    
    
    
    security.declarePrivate('fNewVoidInformeVerifyOrInitCollection')
    def fNewVoidInformeVerifyOrInitCollection( self):
        unInforme = { 
            'type':                      'collection',   
            'success':                   False,
            'status':                    '',           
            'committed':                 False,
            'tipo_coleccion':            '',
            'id_coleccion':              '',
            'titulo_coleccion':          '',
            'acquire_role_assignments':  None,
            'acquire_role_assignments_success': False,
            'acquire_role_assignments_status':  '',
        }
        return unInforme

    
    

        
    
    security.declarePrivate('fNewVoidInformeVerifyOrInitTodosSingletons')
    def fNewVoidInformeVerifyOrInitTodosSingletons( self):
        unInforme = {
            'type':         'singletons',
            'success':      False,
            'container_type':            '',
            'container_title':           '',
            'container_path':            '',
            'singletons':  [],
        }
        return unInforme    
    
    
    
    
    security.declarePrivate('fNewVoidInformeVerifyOrInitSingleton')
    def fNewVoidInformeVerifyOrInitSingleton( self):
        unInforme = { 
            'type':                      'collection',   
            'success':                   False,
            'status':                    '',           
            'committed':                 False,
            'tipo_singleton':            '',
            'id_singleton':              '',
            'titulo_singleton':          '',
            'acquire_role_assignments':  None,
            'acquire_role_assignments_success': False,
            'acquire_role_assignments_status':  '',
        }
        return unInforme

    
    
    
    security.declarePrivate('fNewVoidInformeVerifyOrInitTodosCatalogs')
    def fNewVoidInformeVerifyOrInitTodosCatalogs( self):
        unInforme = { 
            'type':                      'catalogs',
            'title':                     '',
            'success':                   False,
            'must_run_recatalog_elements': False,
            'container_type':            '',
            'container_title':           '',
            'container_path':            '',
            'catalogs':                  [],
        }
        return unInforme
     
    
    
    
    security.declarePrivate('fNewVoidInformeVerifyOrInitCatalog')
    def fNewVoidInformeVerifyOrInitCatalog( self):
        unInforme = { 
            'type':                    'catalog',
            'catalog_name':            '',
            'success':                 False,
            'status':                  '',
            'committed':               False,
            'exception':               '',
            'must_run_recatalog_elements': False,
            'indexes':                 [],
            'schemas':                 [],
            'lexicons':                [],
        }
        return unInforme

    
    
    
    
    security.declarePrivate('fNewVoidInformeVerifyOrInitIndex')
    def fNewVoidInformeVerifyOrInitIndex( self, ):
        unInforme = { }
        unInforme.update( { 
            'type':                     'index',
            'success':                  False,
            'status':                   '',
            'current_index_type':       '',
            'index_name':               '',
            'index_type':               '',
            'index_extras':             '',
        })
        
        return unInforme
    
    
    
    security.declarePrivate('fNewVoidInformeVerifyOrInitLexicon')
    def fNewVoidInformeVerifyOrInitLexicon( self, ):
        unInforme = { }
        unInforme.update( { 
            'type':                    'lexicon',
            'success':                  False,
            'status':                   '',
            'lexicon_name':             '',
            'pipeline':                '',
        })
        
        return unInforme

    
    
    security.declarePrivate('fNewVoidInformeVerifyOrInitSchema')
    def fNewVoidInformeVerifyOrInitSchema( self, ):
        unInforme = { }
        unInforme.update( { 
            'type':                     'schema',
            'success':                  False,
            'status':                   '',
            'schema_field_name':        '',
         })
        
        return unInforme
    
    
                                

    
    
    security.declarePrivate('fNewVoidInformeVerifyOrInitTodosUserGroups')
    def fNewVoidInformeVerifyOrInitTodosUserGroups( self):
        unInforme = { 
            'type':                     'user_groups',
            'committed':                 False,
            'groups':                    [],
            'success':                   False,
            'condition':                 '',
            'exception':                 '',
         }
        return unInforme
     
    
    

        
    security.declarePrivate('fNewVoidInformeVerifyOrInitUserGroup')
    def fNewVoidInformeVerifyOrInitUserGroup( self):
        unInforme = { 
            'type':                     'user_group',
            'name':                     '',
            'success':                   False,
            'status':                   '',
            'condition':                '',
            'roles':                    [],
            'add_group_to_group_result': None,
         }
        return unInforme

            
    
    security.declarePrivate('fNewVoidInformeLazySetLocalRoles')
    def fNewVoidInformeLazySetLocalRoles( self):
        unInforme = { 
            'type':                    'local_roles',
            'success':                 False,
            'status':                  '',
            'condition':               '',
            'committed':               False,
            'element_type':            '',
            'element_title':           '',
            'element_path':            '',
            'previous_roles':          [],
            'new_roles':               [],
            'failed_roles':            [],
         }
        return unInforme
     
         
    

    security.declarePrivate('fNewVoidInformeAddGroupToGroup')
    def fNewVoidInformeAddGroupToGroup( self):
        unInforme = { 
            'type':                     'add_group_to_group',
            'success':                   False,
            'status':                   '',
            'condition':                '',
            'container_group_id':       [],
            'member_group_id':          [],
         }
        return unInforme

      
    
    
    
    
    
    
    
    
    # #########################################################
    """Lazy initialization of framework, applications and translations catalog.
    
    """
    
    
    security.declareProtected( permissions.View, 'fCheckVerifyOrInitializePermissions')
    def fCheckVerifyOrInitializePermissions( self , 
        theAllowInitialization   =False,  
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):
        """Check if the connected user can perform a Verification or initialization of the gvSIG-i18n application and the ModelDDvlPlone framework.
        
        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fCheckVerifyOrInitializePermissions', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 

        try:

            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
        
            aUseCaseName = cUseCase_VerifyTRACatalogo
            if theAllowInitialization:
                aUseCaseName = cUseCase_InitializeTRACatalogo
            
            unUseCaseQueryResult = self.fUseCaseAssessment(  
                theUseCaseName          = cUseCase_InitializeTRACatalogo, 
                theElementsBindings     = { cBoundObject: self,},
                theRulesToCollect       = [ ], 
                thePermissionsCache     = unPermissionsCache, 
                theRolesCache           = unRolesCache, 
                theParentExecutionRecord= unExecutionRecord
            )
            if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                return False

            return True   
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

                        
            
            
            
            
            
    security.declareProtected( permissions.View, 'fVerifyOrInitialize')
    def fVerifyOrInitialize( self , 
        theAllowInitialization   =False, 
        theCheckPermissions      =True,  
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):
        """Verification and initialization of the gvSIG-i18n application and the ModelDDvlPlone framework.
        SHALL BE INVOKED DIRECTLY ON TRACatalogo ROOT CATALOG INSTANCE, AS THE the use case tries to determine whether TRAgvSIGi18n_tool singleton exists, among other initializations. 
        
        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fVerifyOrInitialize', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 

        try:
            
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)

            unInforme = self.fNewVoidInformeVerifyOrInit()
            
            try:
                aProcessType = cTRAProgress_ProcessType_Verify
                if theAllowInitialization:
                    aProcessType = cTRAProgress_ProcessType_Initialize
            
                aTranslatedProcessType = self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_ProcessType_%s_msgid' % aProcessType, aProcessType)
                
                
                unInforme.update( {
                    'process_type':                aProcessType,
                    'translated_process_type':     aTranslatedProcessType,
                    'allow_initialization':        ( theAllowInitialization and True) or False,
                    'check_permissions':           ( theCheckPermissions and True) or False,
                    'element_meta_type':           self.meta_type,
                    'element_title':               self.Title(),
                    'element_path':                '/'.join( self.getPhysicalPath()),
                })
                
                if not self.Title(): # 'portal_factory' in self.getPhysicalPath(): 
                    unInforme[ 'success']   =  False
                    unInforme[ 'condition'] = 'Premature_initialization'
                    return unInforme
                
            

                
                
                # #########################################################
                """If so requested, check connected user permissions to perform a verification or initialzation.
                
                """
                if theCheckPermissions:
                    
                    
                    aUseCasePermitted = self.fCheckVerifyOrInitializePermissions( 
                        theAllowInitialization   =theAllowInitialization,  
                        thePermissionsCache      =unPermissionsCache, 
                        theRolesCache            =unRolesCache, 
                        theParentExecutionRecord =unExecutionRecord
                    )
                    if not aUseCasePermitted:
                        
                        unInforme[ 'success']   =  False
                        if theAllowInitialization:
                            unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_initialize_TRACatalogo
                        else:
                            unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_verify_TRACatalogo

                        return unInforme

                    
                    
                    
                    
                # #########################################################
                """If about to initialize, flush all cached pages from translations catalog elements.
                
                """
                if theAllowInitialization:
                    
                    self.pFlushCachedTemplates_All()
                        
                        
                    
                    

                # #########################################################
                """Verify or initialize ModelDDvlPlone framework.
                
                """
                unInforme[ 'ModelDDvlPlone'] = self.fVerifyOrInitialize_ModelDDvlPlone( 
                    theAllowInitialization   =theAllowInitialization, 
                    theCheckPermissions      =False,  
                    thePermissionsCache      =unPermissionsCache, 
                    theRolesCache            =unRolesCache,
                    theParentExecutionRecord =unExecutionRecord
                )

                
                
                # #########################################################
                """Verify or initialize gvSIG-i18n UI.
                
                """
                unInforme[ 'gvSIGi18nUI'] = self.fVerifyOrInitialize_gvSIGi18nUI( 
                    theAllowInitialization   =theAllowInitialization, 
                    theCheckPermissions      =False,  
                    thePermissionsCache      =unPermissionsCache, 
                    theRolesCache            =unRolesCache,
                    theParentExecutionRecord =unExecutionRecord
                )
                
                
                
                
                # #########################################################
                """Verify or initialize gvSIG-i18n Tool.
                
                """
                unInforme[ 'gvSIGi18nTool'] = self.fVerifyOrInitialize_gvSIGi18nTool( 
                    theAllowInitialization   =theAllowInitialization, 
                    theCheckPermissions      =False,  
                    thePermissionsCache      =unPermissionsCache, 
                    theRolesCache            =unRolesCache,
                    theParentExecutionRecord =unExecutionRecord
                )
                 
                
                
                
                # #########################################################
                """Verify or initialize Translations catalog.
                
                """
                unInforme[ 'catalog'] = self.fVerifyOrInitialize_catalog( 
                    theAllowInitialization   =theAllowInitialization, 
                    theCheckPermissions      =False,  
                    thePermissionsCache      =unPermissionsCache, 
                    theRolesCache            =unRolesCache,
                    theParentExecutionRecord =unExecutionRecord
                )
                              
                # ACV 20090914 Simpler security schema: no user groups for languages or modules, shall assign local roles to users directly on the language or module element
                # unInforme[ 'user_groups_all_idiomas']          = self.fVerifyOrInitializeUserGroupsAllIdiomas(          theAllowInitialization, False, unPermissionsCache, unRolesCache, unExecutionRecord)
                # unInforme[ 'user_groups_all_modulos']          = self.fVerifyOrInitializeUserGroupsAllModulos(          theAllowInitialization, False, unPermissionsCache, unRolesCache, unExecutionRecord)
                # unInforme[ 'user_groups_idiomas']              = self.fVerifyOrInitializeUserGroupsIdiomas(             theAllowInitialization, False, unPermissionsCache, unRolesCache, unExecutionRecord)
                # unInforme[ 'user_groups_modulos']              = self.fVerifyOrInitializeUserGroupsModulos(             theAllowInitialization, False, unPermissionsCache, unRolesCache, unExecutionRecord)
                
                unInforme[ 'success'] = ( \
                    unInforme[ 'ModelDDvlPlone']       and unInforme[ 'ModelDDvlPlone'][ 'success']  and  \
                    unInforme[ 'catalog']              and unInforme[ 'catalog'][ 'success'] and \
                    unInforme[ 'gvSIGi18nUI']          and unInforme[ 'gvSIGi18nUI'][ 'success'] and \
                    unInforme[ 'gvSIGi18nTool']        and unInforme[ 'gvSIGi18nTool'][ 'success']) or False
                
                
                
                unElementoProgreso = self.fCreateNewProgressForVerifyOrInit( 
                    theVerifyOrInitReport    =unInforme,
                    thePermissionsCache      =unPermissionsCache, 
                    theRolesCache            =unRolesCache, 
                    theParentExecutionRecord =unExecutionRecord,
                )
                if not ( unElementoProgreso == None):
                    
                    unElementoProgresoBasicInfo = unElementoProgreso.fBasicInfo()
                    if unElementoProgresoBasicInfo:
                        unInforme[ 'progress_element_basic_info'] = unElementoProgresoBasicInfo


                transaction.commit()
                    
                        
                # #########################################################
                """If about to initialize, flush all cached pages from translations catalog elements.
                
                """
                if theAllowInitialization:
                    self.pFlushCachedTemplates_All()
                    
                return unInforme
            
            
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during TRACatalogo Initialization operation fVerifyOrInitialize\n' 
                try:
                    unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                except:
                    None
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                unInforme[ 'success'] = False
                unInforme[ 'condition'] = 'exception'
                unInforme[ 'exception'] = unInformeExcepcion

                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return unInforme
        
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

            
            
            
 
 
    security.declarePrivate( 'fCreateNewProgressForVerifyOrInit')
    def fCreateNewProgressForVerifyOrInit(self,
        theVerifyOrInitReport   = None,
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None,):

        unExecutionRecord = self.fStartExecution( 'method',  'fCreateNewProgressForVerifyOrInit', theParentExecutionRecord, False,) 

        try:
        
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
            
            
            if not theVerifyOrInitReport:
                return None
            
            unaColeccionProgresos = self.fObtenerColeccionProgresos()
            if unaColeccionProgresos == None:
                return None

            unProcessType = cTRAProgress_ProcessType_Verify
            if theVerifyOrInitReport.get( 'allow_initialization', False):
                unProcessType = cTRAProgress_ProcessType_Initialize
                            
            aMemberId = self.fGetMemberId()
            
            aDateTimeNow        = self.fDateTimeNow ()
            aDateTimeNowTextual = self.fDateToStoreString( aDateTimeNow)

            unProgressResult = self.fNewVoidProgressResult_VerifyOrInitialize()
            unProgressResult[ 'verify_or_init_report'] = theVerifyOrInitReport
            
            unProgressResult[ 'success']                = True
            unProgressResult[ 'process_type']           = unProcessType
            unProgressResult[ 'start_date_time_string'] = aDateTimeNowTextual
            unProgressResult[ 'date_time_now_string']   = aDateTimeNowTextual

            unProgressResult[ 'element_type']           = self.meta_type
            unProgressResult[ 'element_title']          = self.Title()
            unProgressResult[ 'element_path' ]          = self.fPhysicalPathString()
            unProgressResult[ 'element_UID' ]           = self.UID()
            unProgressResult[ 'last_element_type']      = self.meta_type
            unProgressResult[ 'last_element_title']     = self.Title()
            unProgressResult[ 'last_element_path']      = self.fPhysicalPathString()
            unProgressResult[ 'last_element_UID']       = self.UID()
            
            unProgressResult[ 'member_id'] = aMemberId
            
            unProgressResult[ 'TRACatalogo_title']      = self.Title()
            unProgressResult[ 'TRACatalogo_path' ]      = self.fPathDelRaiz()
            unProgressResult[ 'TRACatalogo_UID' ]       = self.UID()
                
            unProgressResult[ 'end_date_time']        = aDateTimeNow
            unProgressResult[ 'end_date_time_string'] = aDateTimeNowTextual
            
            unProgressResult[ 'date_time_now']          = aDateTimeNow
            unProgressResult[ 'date_time_now_string']   = aDateTimeNowTextual
        
           

                
            unNuevoProgresoCreationResult = unaColeccionProgresos.fCreateNewProgressForElement( 
                theInitialElement       =self, 
                theProcessType          =unProcessType, 
                theInputParameters      =None,
                theTimestamp            =aDateTimeNowTextual,
                theResult               =unProgressResult,     
                thePermissionsCache     =unPermissionsCache, 
                theRolesCache           =unRolesCache, 
                theParentExecutionRecord=unExecutionRecord,)   
            if ( not unNuevoProgresoCreationResult) or not unNuevoProgresoCreationResult.get( 'success', False):
                return None
            
            unNuevoProgreso = unNuevoProgresoCreationResult.get( 'progress_element', None)
            
            if unNuevoProgreso == None:
                return None
            
            unNuevoProgreso.setHaComenzado( True)
            unNuevoProgreso.setEstadoProceso( cTRAProgreso_EstadoProceso_Inactivo)
            unNuevoProgreso.setHaCompletadoConExito( True)
            unNuevoProgreso.setFechaComienzoProceso( aDateTimeNow)
            unNuevoProgreso.setFechaFinProceso( aDateTimeNow)
            unNuevoProgreso.setFechaUltimoInformeProgreso( aDateTimeNow)

            transaction.commit()
            
            self.pFlushCachedTemplates_All()            
            
            return unNuevoProgreso
        
    
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()        
        

            
            
    
    security.declarePrivate( 'fVerifyOrInitialize_ModelDDvlPlone')
    def fVerifyOrInitialize_ModelDDvlPlone( self, 
        theAllowInitialization   =False, 
        theCheckPermissions      =True,  
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):
        """Delegate on framework verification or initializacion.
       
        """
        unExecutionRecord = self.fStartExecution( 'method',  'fVerifyOrInitialize_ModelDDvlPlone', theParentExecutionRecord, False) 

        try:
            
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)

            
            # #########################################################
            """If so requested, check connected user permissions to perform a verification or initialzation.
            
            """
            if theCheckPermissions:
                
                aUseCasePermitted = self.fCheckVerifyOrInitializePermissions( 
                    theAllowInitialization   =theAllowInitialization,  
                    thePermissionsCache      =unPermissionsCache, 
                    theRolesCache            =unRolesCache, 
                    theParentExecutionRecord =unExecutionRecord
                )
                if not aUseCasePermitted:
                    unInforme = { }
                    unInforme[ 'success']   =  False
                    if theAllowInitialization:
                        unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_initialize_TRACatalogo
                    else:
                        unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_verify_TRACatalogo

                    return unInforme
            
                
                
            from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Inicializacion import ModelDDvlPloneTool_Inicializacion

            unInforme = ModelDDvlPloneTool_Inicializacion().fVerifyOrInitialize_ModelDDvlPloneFramework( 
                theContextualElement     =self, 
                theAllowInitialization   =theAllowInitialization,
            )
             
            return unInforme  
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

                
                
    
    
    
    

    
    security.declarePrivate( 'fVerifyOrInitialize_gvSIGi18nUI')
    def fVerifyOrInitialize_gvSIGi18nUI( self, 
        theAllowInitialization   =False, 
        theCheckPermissions      =True,  
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):
        """Delegate on framework verification or initializacion.
       
        """
        unExecutionRecord = self.fStartExecution( 'method',  'fVerifyOrInitialize_gvSIGi18nUI', theParentExecutionRecord, False) 

        try:
            
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)

            
            # #########################################################
            """If so requested, check connected user permissions to perform a verification or initialzation.
            
            """
            if theCheckPermissions:
                
                aUseCasePermitted = self.fCheckVerifyOrInitializePermissions( 
                    theAllowInitialization   =theAllowInitialization,  
                    thePermissionsCache      =unPermissionsCache, 
                    theRolesCache            =unRolesCache, 
                    theParentExecutionRecord =unExecutionRecord
                )
                if not aUseCasePermitted:
                    unInforme = { }
                    unInforme[ 'success']   =  False
                    if theAllowInitialization:
                        unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_initialize_TRACatalogo
                    else:
                        unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_verify_TRACatalogo

                    return unInforme

                
                                                
            from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Inicializacion import ModelDDvlPloneTool_Inicializacion

            unInforme = ModelDDvlPloneTool_Inicializacion().fVerifyOrInitialize( 
                theInitializationSpecification =cTRAUIInitializationDefinitions, 
                theContextualElement           =self, 
                theAllowInitialization         =theAllowInitialization,
            )
             
            return unInforme  
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

                
                
    
    
    


    
    security.declarePrivate( 'fVerifyOrInitialize_gvSIGi18nTool')
    def fVerifyOrInitialize_gvSIGi18nTool( self, 
        theAllowInitialization   =False, 
        theCheckPermissions      =True,  
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):
        """Delegate on framework verification or initializacion.
       
        """
        unExecutionRecord = self.fStartExecution( 'method',  'fVerifyOrInitialize_gvSIGi18nTool', theParentExecutionRecord, False) 

        try:
            
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)

            # #########################################################
            """If so requested, check connected user permissions to perform a verification or initialzation.
            
            """
            if theCheckPermissions:
                
                aUseCasePermitted = self.fCheckVerifyOrInitializePermissions( 
                    theAllowInitialization   =theAllowInitialization,  
                    thePermissionsCache      =unPermissionsCache, 
                    theRolesCache            =unRolesCache, 
                    theParentExecutionRecord =unExecutionRecord
                )
                if not aUseCasePermitted:
                    unInforme = { }
                    unInforme[ 'success']   =  False
                    if theAllowInitialization:
                        unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_initialize_TRACatalogo
                    else:
                        unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_verify_TRACatalogo

                    return unInforme

                
                                            
            from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Inicializacion import ModelDDvlPloneTool_Inicializacion

            unInforme = ModelDDvlPloneTool_Inicializacion().fVerifyOrInitialize( 
                theInitializationSpecification =cTRAToolInitializationDefinitions, 
                theContextualElement           =self, 
                theAllowInitialization         =theAllowInitialization,
            )
            
            return unInforme  
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

                
                
                
    
    
    
    



    
    security.declarePrivate( 'fVerifyOrInitialize_catalog')
    def fVerifyOrInitialize_catalog( self, 
        theAllowInitialization   =False, 
        theCheckPermissions      =True,  
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):
        """Verify or initialize elements pertaining to the translations catalog (TRACatalogo instance).
       
        """
        unExecutionRecord = self.fStartExecution( 'method',  'fVerifyOrInitialize_catalog', theParentExecutionRecord, False) 

        unInforme = None
        try:
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
            
            unInforme  = self.fNewVoidInformeVerifyOrInit_Catalog()
            
            unInforme.update( {
                'allow_initialization':        ( theAllowInitialization and True) or False,
                'check_permissions':           ( theCheckPermissions and True) or False,
                'element_meta_type':           self.meta_type,
                'element_title':               self.Title(),
                'element_path':                '/'.join( self.getPhysicalPath()),
            })



            if theAllowInitialization:
                self.pSetInitialPermissions()
            
            
            
            # #########################################################
            """Verify or initialize Early singleton elements that must be contained by this TRACatalog object .
            
            """
            unInforme[ 'early_singletons'] = self.fVerifyOrInitializeSingletons( 
                theEspecificacionesSingletons  =cTRAEspecificacionesEarlySingletons, 
                theAllowInitialization         =theAllowInitialization, 
                theCheckPermissions            =False, 
                thePermissionsCache            =unPermissionsCache, 
                theRolesCache                  =unRolesCache, 
                theParentExecutionRecord       =unExecutionRecord,
            )
            
            self.pClearPermissionsByElementType()
            self.pClearUseCaseSpecificationsForTRACatalogsByName()
            self.pClearStateChangeActionRoles()
              
            if theAllowInitialization:
                self.pSetPermissions()
                someElements = self.fObjectValues( cTodosNombresTipos)
                for anElement in someElements:
                    anElement.pSetPermissions()
                    
                    
                    
                    
               
            # #########################################################
            """If so requested, check connected user permissions to perform a verification or initialzation.
            
            """
            if theCheckPermissions:
                
                aUseCasePermitted = self.fCheckVerifyOrInitializePermissions( 
                    theAllowInitialization   =theAllowInitialization,  
                    thePermissionsCache      =unPermissionsCache, 
                    theRolesCache            =unRolesCache, 
                    theParentExecutionRecord =unExecutionRecord
                )
                if not aUseCasePermitted:
                    
                    unInforme[ 'success']   =  False
                    if theAllowInitialization:
                        unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_initialize_TRACatalogo
                    else:
                        unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_verify_TRACatalogo

                    return unInforme

                                
                
            
            # #########################################################
            """Verify or initialize collection elements that must be contained by this TRACatalog object .
            
            """
            unInforme[ 'colecciones'] = self.fVerifyOrInitializeCollections( 
                theEspecificacionesColecciones =cTRAEspecificacionesColecciones, 
                theAllowInitialization         =theAllowInitialization, 
                theCheckPermissions            =False, 
                thePermissionsCache            =unPermissionsCache, 
                theRolesCache                  =unRolesCache, 
                theParentExecutionRecord       =unExecutionRecord,
            )

            
            
            
            # #########################################################
            """Verify or initialize singleton elements that must be contained by this TRACatalog object .
            
            """
            unInforme[ 'singletons'] = self.fVerifyOrInitializeSingletons( 
                theEspecificacionesSingletons  =cTRAEspecificacionesSingletons, 
                theAllowInitialization         =theAllowInitialization, 
                theCheckPermissions            =False, 
                thePermissionsCache            =unPermissionsCache, 
                theRolesCache                  =unRolesCache, 
                theParentExecutionRecord       =unExecutionRecord,
            )

            
            
            
            # #########################################################
            """Verify or initialize catalogs and indexes, owned by the TRACatalog, to index instances of TRACadena (string to be translated).
            
            """
            unInformeCatalogosCadenas = self.fVerifyOrInitializeCatalogsEIndicesEnCatalogo(
                theEspecificacionesCatalogs    =cTRACatalogsDetailsParaCadenas, 
                theAllowInitialization         =theAllowInitialization, 
                theCheckPermissions            =False, 
                thePermissionsCache            =unPermissionsCache, 
                theRolesCache                  =unRolesCache, 
                theParentExecutionRecord       =unExecutionRecord,
            )
            unInforme[ 'catalogs_cadenas'] = unInformeCatalogosCadenas
            
            if unInformeCatalogosCadenas:
                if unInformeCatalogosCadenas.get( 'must_run_recatalog_elements', False):
                    unInforme[ 'must_run_recatalog_elements'] = True
                

            
            # #########################################################
            """Verify or initialize catalogs and indexes, owned by each of the languages the TRACatalog, to index instances of TRATraduccion (translation).
            
            """
            unosInformeCatalogosIdiomas  = self.fVerifyOrInitializeCatalogsEIndicesTodosIdiomas( 
                theEspecificacionesCatalogs    =cTRACatalogsDetailsParaIdioma, 
                theAllowInitialization         =theAllowInitialization, 
                theCheckPermissions            =False, 
                thePermissionsCache            =unPermissionsCache, 
                theRolesCache                  =unRolesCache, 
                theParentExecutionRecord       =unExecutionRecord,
            ) 
            unInforme[ 'catalogs_idiomas'] = unosInformeCatalogosIdiomas
            if unosInformeCatalogosIdiomas:
                for unInformeCatalogosIdioma in unosInformeCatalogosIdiomas:
                    if unInformeCatalogosIdioma:
                        if unInformeCatalogosIdioma.get( 'must_run_recatalog_elements', False):
                            unInforme[ 'must_run_recatalog_elements'] = True
                        
                    
            
            
            
            # #########################################################
            """Verify or initialize user groups, specific to this TRACatalog, for each of the roles that users may play when interacting with this TRACatalogo.
            
            """
            unInforme[ 'user_groups_catalogo']  = self.fVerifyOrInitializeUserGroupsCatalogo(   
                theAllowInitialization         =theAllowInitialization, 
                theCheckPermissions            =False, 
                thePermissionsCache            =unPermissionsCache, 
                theRolesCache                  =unRolesCache, 
                theParentExecutionRecord       =unExecutionRecord,
            )

            
            
            
            unInforme[ 'success'] = \
                ( unInforme[ 'colecciones']          and unInforme[ 'colecciones'].get(          'success', False)) and \
                ( unInforme[ 'singletons']           and unInforme[ 'singletons'].get(           'success', False)) and \
                ( unInforme[ 'catalogs_cadenas']     and unInforme[ 'catalogs_cadenas'].get(     'success', False)) and \
                ( len( unInforme[ 'catalogs_idiomas']) == len( [ unInformeCatalogIdioma for unInformeCatalogIdioma in unInforme[ 'catalogs_idiomas'] if unInformeCatalogIdioma.get( 'success', False)])) and \
                ( unInforme[ 'user_groups_catalogo'] and unInforme[ 'user_groups_catalogo'].get( 'success', False)) and \
                True
            
            
            
            return unInforme  
                
                          
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

                
                
                
    
    
    
    
    


    security.declarePrivate( 'fVerifyOrInitializeCollections')
    def fVerifyOrInitializeCollections( self, 
        theEspecificacionesColecciones =None, 
        theAllowInitialization         =False, 
        theCheckPermissions            =True, 
        thePermissionsCache            =None, 
        theRolesCache                  =None, 
        theParentExecutionRecord       =None):
        """Verify and create Collections.
        
        """
        unExecutionRecord = self.fStartExecution( 'method',  'fVerifyOrInitializeCollections', theParentExecutionRecord, False) 

        try:
            
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)

                
            unInforme = self.fNewVoidInformeVerifyOrInitTodasCollections()
            
                
            unContainerType = self.__class__.__name__
            unContainerTitle = self.Title()
            unContainerPath = '/'.join( self.getPhysicalPath())
            
            unInforme.update( {
                'container_type':            unContainerType,
                'container_title':           unContainerTitle,
                'container_path':            unContainerPath,
            })
            
            
            if not theEspecificacionesColecciones:
                return unInforme
            
            
            try:
                someCollectionEntries =  unInforme[ 'collections']
                
                    
                if not self.Title():
                    unInforme[ 'success']   =  False
                    unInforme[ 'condition'] = 'Premature_initialization'
                    return unInforme
                    

                   
                # #########################################################
                """If so requested, check connected user permissions to perform a verification or initialzation.
                
                """
                if theCheckPermissions:
                    
                    aUseCasePermitted = self.fCheckVerifyOrInitializePermissions( 
                        theAllowInitialization   =theAllowInitialization,  
                        thePermissionsCache      =unPermissionsCache, 
                        theRolesCache            =unRolesCache, 
                        theParentExecutionRecord =unExecutionRecord
                    )
                    if not aUseCasePermitted:
                        
                        unInforme[ 'success']   =  False
                        if theAllowInitialization:
                            unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_initialize_TRACatalogo
                        else:
                            unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_verify_TRACatalogo
    
                        return unInforme

                    
                for unaEspecificacionColeccion in theEspecificacionesColecciones:
                    unHayCambio = False
                    
                    unTipoColeccion    = unaEspecificacionColeccion[ 0]
                    unaIdColeccion     = unaEspecificacionColeccion[ 1]
                    unTituloColeccion  = unaEspecificacionColeccion[ 2]
                    
                    unCollectionReportEntry = self.fNewVoidInformeVerifyOrInitCollection()
                    unCollectionReportEntry.update( {            
                        'tipo_coleccion':            unTipoColeccion,
                        'id_coleccion':              unaIdColeccion,
                        'titulo_coleccion':          unTituloColeccion,
                        'success':                   False,
                        'status':                   '',
                    })
                    someCollectionEntries.append( unCollectionReportEntry)
                    # ACV 20090527 Found with victor unaCollection referenced before defined
                    unaCollection = None
                    unasCollections = self.fObjectValues(   unTipoColeccion)
                    if unasCollections: 
                        unaCollection = unasCollections[ 0]
                        unCollectionReportEntry[ 'status'] = 'exists'
                        unCollectionReportEntry[ 'success'] = True
        
                    else:
                        if not ( theAllowInitialization and cInitializeAllow_CreateCollections):
                            unCollectionReportEntry[ 'status'] = 'missing'         
                        else:                
                            aIdNuevaColeccion = self.invokeFactory( unTipoColeccion, unaIdColeccion, title=unTituloColeccion ) 
                            unaNuevaColeccion = self.getElementoPorID( aIdNuevaColeccion)
                            
                            if ( unaNuevaColeccion == None):
                                unCollectionReportEntry[ 'status'] = 'creation_failed'
                            else:
                                unCollectionReportEntry[ 'status'] = 'created'
                                unCollectionReportEntry[ 'success'] = True
            
                                unaNuevaColeccion.manage_fixupOwnershipAfterAdd()
             
                                unaNuevaColeccion.pSetPermissions()

                                unaCollection = unaNuevaColeccion
                                unHayCambio   = True
                    
                    if not ( unaCollection == None):
                        
                        if self.fLazySetAcquireRoleAssignments( 
                            theAllowInitialization     =theAllowInitialization, 
                            theCheckPermissions        =False, 
                            theElement                 =unaCollection, 
                            theReport                  =unCollectionReportEntry, 
                            thePermissionsCache        =unPermissionsCache, 
                            theRolesCache              =unRolesCache, 
                            theParentExecutionRecord   =unExecutionRecord):
                            
                            unHayCambio = True
                       
                        if unHayCambio:
                            transaction.commit()
                            unCollectionReportEntry[ 'committed'] = True
                        
        
                if len( [ unaCollectionEntry for unaCollectionEntry in someCollectionEntries if unaCollectionEntry[ 'success'] ]) == len( someCollectionEntries):
                    unInforme[ 'success'] = True
                    
                return unInforme
            
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during Lazy Initialization operation fVerifyOrInitializeCollections\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                unInforme[ 'success'] = False
                unInforme[ 'condition'] = 'exception'
                unInforme[ 'exception'] = unInformeExcepcion
                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return unInforme
              
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

    
            
            
    


            
    


    security.declarePrivate( 'fVerifyOrInitializeSingletons')
    def fVerifyOrInitializeSingletons( self, 
        theEspecificacionesSingletons  =None, 
        theAllowInitialization         =False, 
        theCheckPermissions            =True, 
        thePermissionsCache            =None, 
        theRolesCache                  =None, 
        theParentExecutionRecord       =None):
        """Verify and create Singletons.
        
        """
        unExecutionRecord = self.fStartExecution( 'method',  'fVerifyOrInitializeSingletons', theParentExecutionRecord, False) 

        try:
            
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)

                
            unInforme = self.fNewVoidInformeVerifyOrInitTodosSingletons()

                
            unContainerType = self.__class__.__name__
            unContainerTitle = self.Title()
            unContainerPath = '/'.join( self.getPhysicalPath())
            
            unInforme.update( {
                'container_type':            unContainerType,
                'container_title':           unContainerTitle,
                'container_path':            unContainerPath,
            })
            
            if not theEspecificacionesSingletons:
                return unInforme
            
            
            try:
                someSingletonEntries =  unInforme[ 'singletons']
                
                    
                if not self.Title():
                    unInforme[ 'success']   =  False
                    unInforme[ 'condition'] = 'Premature_initialization'
                    return unInforme
                    

                                  
                # #########################################################
                """If so requested, check connected user permissions to perform a verification or initialzation.
                
                """
                if theCheckPermissions:
                    
                    aUseCasePermitted = self.fCheckVerifyOrInitializePermissions( 
                        theAllowInitialization   =theAllowInitialization,  
                        thePermissionsCache      =unPermissionsCache, 
                        theRolesCache            =unRolesCache, 
                        theParentExecutionRecord =unExecutionRecord
                    )
                    if not aUseCasePermitted:
                        
                        unInforme[ 'success']   =  False
                        if theAllowInitialization:
                            unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_initialize_TRACatalogo
                        else:
                            unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_verify_TRACatalogo
    
                        return unInforme

                                
                for unaEspecificacionSingleton in theEspecificacionesSingletons:
                    unHayCambio = False
                    
                    unTipoSingleton       = unaEspecificacionSingleton[ 0]
                    unaIdSingleton        = unaEspecificacionSingleton[ 1]
                    unTituloSingleton     = unaEspecificacionSingleton[ 2]
                    unosValoresSingleton  =(( len( unaEspecificacionSingleton) > 3) and unaEspecificacionSingleton[ 3]) or {}
                    
                    unSingletonReportEntry = self.fNewVoidInformeVerifyOrInitSingleton()
                    unSingletonReportEntry.update( {            
                        'tipo_singleton':            unTipoSingleton,
                        'id_singleton':              unaIdSingleton,
                        'titulo_singleton':          unTituloSingleton,
                        'success':                   False,
                        'status':                   '',
                    })
                    someSingletonEntries.append( unSingletonReportEntry)

                    unaSingleton = None
                    unasSingletons = self.fObjectValues(   unTipoSingleton)
                    unSingletonExists = False
                    if unasSingletons: 
                        for otroSingleton in unasSingletons:
                            otroSingletonId = otroSingleton.getId()
                            if otroSingletonId == unaIdSingleton:
                                unaSingleton = otroSingleton
                                unSingletonExists = True
                                break
        
                    else:
                        unSingletonExists = False
                     
                    if unSingletonExists:
                        unSingletonReportEntry[ 'status'] = 'exists'
                        unSingletonReportEntry[ 'success'] = True
                    else:
                        if not ( theAllowInitialization and cInitializeAllow_CreateSingletons):
                            unSingletonReportEntry[ 'status'] = 'missing'         
                        else:     
                            anAttrsDict = {'title': unTituloSingleton, }
                            if unosValoresSingleton:
                                anAttrsDict.update( unosValoresSingleton)
                                
                            aIdNuevaSingleton = self.invokeFactory( unTipoSingleton, unaIdSingleton, **anAttrsDict ) 
                            
                            unaNuevaSingleton = self.getElementoPorID( aIdNuevaSingleton)
                            
                            if ( unaNuevaSingleton == None):
                                unSingletonReportEntry[ 'status'] = 'creation_failed'
                            else:
                                unSingletonReportEntry[ 'status'] = 'created'
                                unSingletonReportEntry[ 'success'] = True
            
                                unaNuevaSingleton.manage_fixupOwnershipAfterAdd()
             
                                unaNuevaSingleton.pSetPermissions()

                                unaSingleton = unaNuevaSingleton
                                unHayCambio   = True
                    
                    if not ( unaSingleton == None):
                        
                        if self.fLazySetAcquireRoleAssignments( 
                            theAllowInitialization     =theAllowInitialization, 
                            theCheckPermissions        =False, 
                            theElement                 =unaSingleton, 
                            theReport                  =unSingletonReportEntry, 
                            thePermissionsCache        =unPermissionsCache, 
                            theRolesCache              =unRolesCache, 
                            theParentExecutionRecord   =unExecutionRecord):

                            unHayCambio = True
                       
                        if unHayCambio:
                            transaction.commit()
                            unSingletonReportEntry[ 'committed'] = True
                        
        
                if len( [ unaSingletonEntry for unaSingletonEntry in someSingletonEntries if unaSingletonEntry[ 'success'] ]) == len( someSingletonEntries):
                    unInforme[ 'success'] = True
                    
                return unInforme
            
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during Lazy Initialization operation fVerifyOrInitializeSingletons\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                unInforme[ 'success'] = False
                unInforme[ 'condition'] = 'exception'
                unInforme[ 'exception'] = unInformeExcepcion
                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return unInforme
              
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

    
            
            
            
            
            
            
            
            
            

    security.declarePrivate( 'fLazySetAcquireRoleAssignments')
    def fLazySetAcquireRoleAssignments( self, 
        theAllowInitialization     =False, 
        theCheckPermissions        =True, 
        theElement                 =None, 
        theReport                  ={}, 
        thePermissionsCache        =None, 
        theRolesCache              =None, 
        theParentExecutionRecord   =None):
       
        unExecutionRecord = self.fStartExecution( 'method',  'fLazySetAcquireRoleAssignments', theParentExecutionRecord, False, None, 'element: %s' % ( (theElement and '/'.join( theElement.getPhysicalPath())) or '')) 

        try:
            
                                
            if ( theElement == None):
                return False
            
    
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)

                        
            # #########################################################
            """If so requested, check connected user permissions to perform a verification or initialzation.
            
            """
            if theCheckPermissions:
                
                aUseCasePermitted = self.fCheckVerifyOrInitializePermissions( 
                    theAllowInitialization   =theAllowInitialization,  
                    thePermissionsCache      =unPermissionsCache, 
                    theRolesCache            =unRolesCache, 
                    theParentExecutionRecord =unExecutionRecord
                )
                if not aUseCasePermitted:
                    
                    theReport[ 'success']   =  False
                    if theAllowInitialization:
                        theReport[ 'condition'] = cTRAErrorMsgId_user_can_NOT_initialize_TRACatalogo
                    else:
                        theReport[ 'condition'] = cTRAErrorMsgId_user_can_NOT_verify_TRACatalogo

                    return False

                
            aAcquireRoleAssignments       = self.fAcquireRoleAssignmentsElement( theElement)
            aIsAcquiringRoleAssignments   = self.fIsAcquiringRoleAssignments(    theElement)
            
            if aAcquireRoleAssignments:
                if aIsAcquiringRoleAssignments:
                    theReport[ 'acquire_role_assignments']         = True
                    theReport[ 'acquire_role_assignments_success'] = True
                    theReport[ 'acquire_role_assignments_status']  = 'was_set'
                    return False
                else:
                    if ( theAllowInitialization and cInitializeAllow_CreateSetAcquireRoleAssignments):
                        self.fSetAcquiringRoleAssignments( theElement, True)
                        
                        if self.fIsAcquiringRoleAssignments( theElement):                                
                            theReport[ 'acquire_role_assignments']         = True
                            theReport[ 'acquire_role_assignments_success'] = True
                            theReport[ 'acquire_role_assignments_status']  = 'set'
                            return True
                            
                        else:
                            theReport[ 'success']         = False
                            theReport[ 'status']          = 'role_acquisition_failure'
                            theReport[ 'acquire_role_assignments']         = True
                            theReport[ 'acquire_role_assignments_success'] = False
                            theReport[ 'acquire_role_assignments_status']  = 'set_error'
                            return False
                    else:
                        theReport[ 'success']         = False
                        theReport[ 'status']          = 'role_acquisition_failure'
                        theReport[ 'acquire_role_assignments']         = True
                        theReport[ 'acquire_role_assignments_success'] = False
                        theReport[ 'acquire_role_assignments_status']  = 'wrong_value'
                        return False
                    
                        
            else:
                
                if aIsAcquiringRoleAssignments:
                    if ( theAllowInitialization and cInitializeAllow_CreateSetAcquireRoleAssignments):
                        self.fSetAcquiringRoleAssignments( theElement, False)
                        
                        if self.fIsAcquiringRoleAssignments( theElement):                                
                            theReport[ 'success']         = False
                            theReport[ 'status']          = 'role_acquisition_failure'
                            theReport[ 'acquire_role_assignments']         = False
                            theReport[ 'acquire_role_assignments_success'] = False
                            theReport[ 'acquire_role_assignments_status']  = 'set_error'
                            return False
                        else:
                            theReport[ 'acquire_role_assignments']         = False
                            theReport[ 'acquire_role_assignments_success'] = True
                            theReport[ 'acquire_role_assignments_status']  = 'set'
                            return True
                            
                    else:
                        theReport[ 'success']         = False
                        theReport[ 'status']          = 'role_acquisition_failure'
                        theReport[ 'acquire_role_assignments']         = False
                        theReport[ 'acquire_role_assignments_success'] = False
                        theReport[ 'acquire_role_assignments_status']  = 'wrong_value'
                        return False
                
                else:
                    theReport[ 'acquire_role_assignments']         = False
                    theReport[ 'acquire_role_assignments_success'] = True
                    theReport[ 'acquire_role_assignments_status']  = 'was_set'
                    return False
                    
            return False
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

    

    
    
 
                
 
    security.declarePrivate( 'fVerifyOrInitializeCatalogsEIndicesTodosIdiomas')
    def fVerifyOrInitializeCatalogsEIndicesTodosIdiomas( self, 
        theEspecificacionesCatalogs =None, 
        theAllowInitialization      =False, 
        theCheckPermissions         =True, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):
        """Verify or initialize catalogs and indexes, owned by each of the languages the TRACatalog, to index instances of TRATraduccion (translation).
        
        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fVerifyOrInitializeCatalogsEIndicesTodosIdiomas', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 

        try:
            
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
            

            # #########################################################
            """If so requested, check connected user permissions to perform a verification or initialzation.
            
            """
            if theCheckPermissions:
                
                aUseCasePermitted = self.fCheckVerifyOrInitializePermissions( 
                    theAllowInitialization   =theAllowInitialization,  
                    thePermissionsCache      =unPermissionsCache, 
                    theRolesCache            =unRolesCache, 
                    theParentExecutionRecord =unExecutionRecord
                )
                if not aUseCasePermitted:
                    
                    unInforme = self.fNewVoidInformeVerifyOrInitTodosCatalogs()
                    
                    unInforme[ 'success']   =  False
                    if theAllowInitialization:
                        unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_initialize_TRACatalogo
                    else:
                        unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_verify_TRACatalogo

                    return unInforme            
                
                
                
            unosIdiomas = self.fObtenerTodosIdiomas()
            unosInformesIdiomas = []
            for unIdioma in unosIdiomas:
                unInforme = self.fVerifyOrInitializeCatalogsEIndicesParaIdioma( 
                    theEspecificacionesCatalogs =theEspecificacionesCatalogs,
                    theAllowInitialization      =theAllowInitialization, 
                    theIdioma                   =unIdioma,  
                    theCheckPermissions         =False, 
                    thePermissionsCache         =unPermissionsCache, 
                    theRolesCache               =unRolesCache, 
                    theParentExecutionRecord    =unExecutionRecord,
                )
                if unInforme:
                    unosInformesIdiomas.append( unInforme)
         
            return unosInformesIdiomas
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
    
       
    
    
    
    
        
 
    security.declarePrivate( 'fVerifyOrInitializeCatalogsEIndicesParaIdioma')
    def fVerifyOrInitializeCatalogsEIndicesParaIdioma( self, 
        theEspecificacionesCatalogs =None,
        theAllowInitialization      =False, 
        theIdioma                   =None,  
        theCheckPermissions         =True, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):
        """Verify and create Catalogs and indexes for one language.
        
        """
       
        unExecutionRecord = self.fStartExecution( 'method',  'fVerifyOrInitializeCatalogsEIndicesParaIdioma', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 

        try:
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)


            if not self.Title():
                unInforme = self.fNewVoidInformeVerifyOrInitTodosCatalogs()
                unInforme[ 'success']   =  False
                unInforme[ 'condition'] = 'Premature_initialization'
                return unInforme

            if not theIdioma:
                return self.fNewVoidInformeVerifyOrInitTodosCatalogs()
            
           
            # #########################################################
            """If so requested, check connected user permissions to perform a verification or initialzation.
            
            """
            if theCheckPermissions:
                
                aUseCasePermitted = self.fCheckVerifyOrInitializePermissions( 
                    theAllowInitialization   =theAllowInitialization,  
                    thePermissionsCache      =unPermissionsCache, 
                    theRolesCache            =unRolesCache, 
                    theParentExecutionRecord =unExecutionRecord
                )
                if not aUseCasePermitted:
                    
                    unInforme = self.fNewVoidInformeVerifyOrInitTodosCatalogs()
                    unInforme[ 'success']   =  False
                    if theAllowInitialization:
                        unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_initialize_TRACatalogo
                    else:
                        unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_verify_TRACatalogo

                    return unInforme
            
                
                
            unSpecialPipelineSpec = None
            unCodigoIdioma = theIdioma.getCodigoIdiomaEnGvSIG()
            if not unCodigoIdioma:
                return self.fNewVoidInformeVerifyOrInitTodosCatalogs()
            
            unLanguage, unCountry, unaVariation = self.fLanguageAndCountryAndVariationIdioma( unCodigoIdioma)
            if not unLanguage:
                return self.fNewVoidInformeVerifyOrInitTodosCatalogs()
     
            unDisplayTitleIdioma = theIdioma.fDisplayTitleAsUnicode()

            if ( cLanguagesWithSpecialLexiconPipelines.has_key( unLanguage)):
                unSpecialPipelineSpec = cLanguagesWithSpecialLexiconPipelines.get( unLanguage, None)
     
            return  self.fVerifyOrInitializeCatalogsEIndicesEnContenedor( 
                theCatalogsTitle                    =unDisplayTitleIdioma,
                theAllowInitialization              =theAllowInitialization, 
                theContenedor                       =theIdioma, 
                theEspecificacionCatalogoEIndice    =theEspecificacionesCatalogs, 
                theSpecialPipelineSpec              =unSpecialPipelineSpec, 
                theCheckPermissions                 =False, 
                thePermissionsCache                 =unPermissionsCache, 
                theRolesCache                       =unRolesCache, 
                theParentExecutionRecord            =unExecutionRecord,
                
            )
    
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

   
            
            
            
                
                
                
    security.declarePrivate( 'fVerifyOrInitializeCatalogsEIndicesEnCatalogo')
    def fVerifyOrInitializeCatalogsEIndicesEnCatalogo( self, 
        theEspecificacionesCatalogs    =None, 
        theAllowInitialization         =False, 
        theCheckPermissions            =True, 
        thePermissionsCache            =None, 
        theRolesCache                  =None, 
        theParentExecutionRecord       =None):
        """Verify or initialize catalogs and indexes, owned by the TRACatalog, to index instances of TRACadena (string to be translated).
        
        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fVerifyOrInitializeCatalogsEIndicesEnCatalogo', theParentExecutionRecord, False) 

        try:
            
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)

            # #########################################################
            """If so requested, check connected user permissions to perform a verification or initialzation.
            
            """
            if theCheckPermissions:
                
                aUseCasePermitted = self.fCheckVerifyOrInitializePermissions( 
                    theAllowInitialization   =theAllowInitialization,  
                    thePermissionsCache      =unPermissionsCache, 
                    theRolesCache            =unRolesCache, 
                    theParentExecutionRecord =unExecutionRecord
                )
                if not aUseCasePermitted:
                    
                    unInforme = self.fNewVoidInformeVerifyOrInitTodosCatalogs()
                    
                    unInforme[ 'success']   =  False
                    if theAllowInitialization:
                        unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_initialize_TRACatalogo
                    else:
                        unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_verify_TRACatalogo

                    return unInforme        
                
                
            return self.fVerifyOrInitializeCatalogsEIndicesEnContenedor( 
                theCatalogsTitle                    ='Catalogs for Strings to be Translated to all languages',
                theAllowInitialization              =theAllowInitialization, 
                theContenedor                       =self, 
                theEspecificacionCatalogoEIndice    =theEspecificacionesCatalogs, 
                theSpecialPipelineSpec              =None, 
                theCheckPermissions                 =False, 
                thePermissionsCache                 =unPermissionsCache, 
                theRolesCache                       =unRolesCache, 
                theParentExecutionRecord            =unExecutionRecord,
            )
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
                
                
            
            
            
                

    security.declarePrivate( 'fVerifyOrInitializeCatalogsEIndicesEnContenedor')
    def fVerifyOrInitializeCatalogsEIndicesEnContenedor( self, 
        theCatalogsTitle                    ='',
        theAllowInitialization              =False, 
        theContenedor                       =None, 
        theEspecificacionCatalogoEIndice    =None, 
        theSpecialPipelineSpec              =None, 
        theCheckPermissions                 =True, 
        thePermissionsCache                 =None, 
        theRolesCache                       =None, 
        theParentExecutionRecord            =None):
        """Verify and create Catalogs and indexes on a container (used for global and language specific catalogs).
        
        """
       
        unExecutionRecord = self.fStartExecution( 'method',  'fVerifyOrInitializeCatalogsEIndicesEnContenedor', theParentExecutionRecord, False, None, 'container: %s  spec: %s' % ( theContenedor and '/'.join( theContenedor.getPhysicalPath()), str( theEspecificacionCatalogoEIndice))) 

        try:
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
            
            unInforme = self.fNewVoidInformeVerifyOrInitTodosCatalogs()

            try:
                if not self.Title():
                    unInforme[ 'success']   =  False
                    unInforme[ 'condition'] = 'Premature_initialization'
                    return unInforme
                
                if ( theContenedor == None) or not theEspecificacionCatalogoEIndice:
                    unInforme[ 'success']   =  False
                    unInforme[ 'condition'] = 'MISSING_parameters'
                    return unInforme
        
            
 
                               
                # #########################################################
                """If so requested, check connected user permissions to perform a verification or initialzation.
                
                """
                if theCheckPermissions:
                    
                    aUseCasePermitted = self.fCheckVerifyOrInitializePermissions( 
                        theAllowInitialization   =theAllowInitialization,  
                        thePermissionsCache      =unPermissionsCache, 
                        theRolesCache            =unRolesCache, 
                        theParentExecutionRecord =unExecutionRecord
                    )
                    if not aUseCasePermitted:
                        
                        unInforme[ 'success']   =  False
                        if theAllowInitialization:
                            unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_initialize_TRACatalogo
                        else:
                            unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_verify_TRACatalogo
    
                        return unInforme
                              
                    
                                  
                    
                someReportEntries = unInforme[ 'catalogs']
                
                unContainerType  = theContenedor.__class__.__name__
                unContainerTitle = theContenedor.Title()
                unContainerPath  = '/'.join( theContenedor.getPhysicalPath())
                unInforme.update( {
                    'title':                     theCatalogsTitle,
                    'container_type':            unContainerType,
                    'container_title':           unContainerTitle,
                    'container_path':            unContainerPath,
                    'committed':                 False,
                    'success':                   False,
                })
                
                
                for unCatalogDetails in theEspecificacionCatalogoEIndice:
                    unCatalogName           = unCatalogDetails[ 'name']
                    unCatalogIndexes        = unCatalogDetails[ 'indexes']
                    unCatalogSchemaFields   = unCatalogDetails[ 'schema_fields']
                    unosCatalogLexicons     = unCatalogDetails[ 'lexicons']
                    
                    
                    unLastIndexName       = ''
                    unLastSchemaFieldName = ''
                    
                    unCatalogJustCreated       = False
                    unIndexesOrSchemasOrLexiconsAdded    = False
                    unCatalogReportEntry       = None
        
                    unCatalogReportEntry = self.fNewVoidInformeVerifyOrInitCatalog()
                    unCatalogReportEntry.update( {            
                        'catalog_name':              unCatalogName,
                        'type':                     '',
                        'success':                  False,
                        'status':                   '',
                    })
                    
                    someReportEntries.append( unCatalogReportEntry)
                    
                    try:
                        unCatalog = self.fCatalogNamed( theContenedor, unCatalogName)
                        if not ( unCatalog == None):
                            unCatalogReportEntry[ 'status'] = 'exists'         
                        else:
                            if not ( theAllowInitialization and cInitializeAllow_CreateCatalogs):
                                unCatalogReportEntry[ 'status'] = 'missing'         
                            else:
                                unNewCatalog = ZCatalog( unCatalogName, unCatalogName) 
                                theContenedor._setObject( unCatalogName,  unNewCatalog)
                                unCatalog = self.fCatalogNamed( theContenedor, unCatalogName)
                                if not ( unCatalog == None):
                                    unCatalogJustCreated = True
                                    unCatalogReportEntry[ 'status'] = 'created'     
                                    
                                else:
                                    unCatalogReportEntry[ 'status'] = 'creation_failed'         
                         
        
                        
                        if not ( unCatalog == None):
                            
                            unosLexiconsEntries = unCatalogReportEntry[ 'lexicons']
                            
                            for unLexiconSpec in unosCatalogLexicons:
                                unNombreLexicon          = unLexiconSpec[ 0]
                                unosPipelineElementNames = unLexiconSpec[ 1]
                                
                                # special case for Chinese Japanese Korean, english indexing
                                if theSpecialPipelineSpec:
                                    unosPipelineElementNames = theSpecialPipelineSpec
                                            
                                unLexiconReportEntry = self.fNewVoidInformeVerifyOrInitLexicon( )
                                unLexiconReportEntry.update( {            
                                    'catalog_name':             unCatalogReportEntry.get( 'catalog_name', ''),
                                    'type':                     'lexicon',
                                    'lexicon_name':             unNombreLexicon,
                                    'pipeline':                 ' '.join( unosPipelineElementNames),
                                    'status':                   '',
                                    'success':                  False,
                                })
                                unosLexiconsEntries.append( unLexiconReportEntry)
                                
                                unLexiconExistente = None
                                try:
                                    unLexiconExistente = unCatalog[ unNombreLexicon]
                                except:
                                    None
                                    
                                if not( unLexiconExistente == None):
                                    unLexiconReportEntry.update( {
                                        'status':                               'exists',           
                                        'success':                              True,
                                    }) 
                                else:    
                                    if not ( theAllowInitialization and cInitializeAllow_CreateLexicons):
                                        unLexiconReportEntry[ 'status'] = 'missing',
                                    else:
                                     
                                        unosPipelineElements     = [ ]
                                     
                                        
                                        for unPipelineElementName in unosPipelineElementNames:
                                            if unPipelineElementName == 'Splitter':
                                                unosPipelineElements.append( Splitter())  
                                            elif unPipelineElementName == 'CaseNormalizer':
                                                unosPipelineElements.append( CaseNormalizer())  
                                            elif unPipelineElementName == 'StopWordRemover':
                                                unosPipelineElements.append( StopWordRemover())  
                                            elif unPipelineElementName == 'CJKSplitter':
                                                if gCJKSplitter:
                                                    unosPipelineElements.append( gCJKSplitter())  
                                                else:
                                                    unosPipelineElements = [ ]
                                                    unosPipelineElements.append( Splitter())  
                                                    unosPipelineElements.append( CaseNormalizer())  
                                                    unosPipelineElements.append( StopWordRemover())                                                      
                                            elif unPipelineElementName == 'TRASplitter':
                                                unosPipelineElements.append( TRASplitter())  
                                                 
                                                
                                        if not unosPipelineElements:
                                            unLexiconReportEntry.update( {
                                                'status':                               'empty_pipeline',           
                                                'success':                              False,
                                            }) 
                                        else:    
                                            # ACV 20091105 Found in ZopeChinaPak::utils::modifyCatalogTextIndexToSupportChinese
                                            # a call to method that may be better to add the lexicon to the catalog
                                            #   ZCTextIndex.manage_addLexicon(catalog, 'CJKLexicon', 'Default Lexicon', elem)

                                            unLexicon = PLexicon( unNombreLexicon, unNombreLexicon, *unosPipelineElements)    
                                            unCatalog._setObject( unNombreLexicon, unLexicon)    
                                                                            
                                            unIndexesOrSchemasOrLexiconsAdded = True                            
            
                                            unLexiconExistente = None
                                            try:
                                                unLexiconExistente = unCatalog[ unNombreLexicon]
                                            except:
                                                None
                                            if not( unLexiconExistente == None):
                                                unLexiconReportEntry.update( {
                                                    'status':                               'created',           
                                                    'success':                              True,
                                                }) 
                                            else:
                                                unLexiconReportEntry.update( {
                                                    'status':                               'creation_failed',           
                                                    'success':                              False,
                                                }) 
                                                
                                    
                                        
                                
                            
                
            
                            unosIndexesEntries = unCatalogReportEntry[ 'indexes']
                            
                            unosIndexesExistentes       = unCatalog.indexes()
                            
                            for unIndexSpec in unCatalogIndexes:

                                unIndexReportEntry = self.fNewVoidInformeVerifyOrInitIndex( )

                                unIndexName     = unIndexSpec[ 0]
                                unIndexType     = unIndexSpec[ 1]
                                
                                unLastIndexName = unIndexName
                                
                                unIndexReportEntry.update( {            
                                    'catalog_name':             unCatalogReportEntry.get( 'catalog_name', ''),
                                    'type':                     'index',
                                    'index_name':               unIndexName,
                                    'index_type':               unIndexType,
                                    'current_index_type':       '',
                                    'status':                   '',
                                })
                                unosIndexesEntries.append( unIndexReportEntry)
                                
                                unIndexExtras   = None
                                if len( unIndexSpec) > 2:
                                    unIndexExtras= unIndexSpec[ 2]
                                    unIndexExtrasString = ''
                                    if isinstance( unIndexExtras, SimpleRecord):
                                        try:
                                            unIndexExtrasString = 'lexicon_id=%s, index_type=%s' % ( unIndexExtras.lexicon_id, unIndexExtras.index_type,)
                                        except:
                                            None
                                            
                                    if not unIndexExtrasString:
                                        unIndexExtrasString =  repr( unIndexExtras)
                                        
                                    unIndexReportEntry.update( {            
                                        'index_extras': unIndexExtrasString,
                                    })
                                
                                
                                if ( unIndexName in unosIndexesExistentes):    
                                    # ACV OJO 200903080425 should also check for the extras: if ZCTextIndex should have the lexicons specified
                                    unExistingIndexClassName = unCatalog.Indexes[ unIndexName].__class__.__name__
                                    if unExistingIndexClassName == unIndexType:
                                        unIndexReportEntry.update( {
                                            'status':                               'exists',           
                                            'success':                              True,
                                            'current_index_type':                   unExistingIndexClassName,
                                        }) 
                                    else:
                                        if not ( theAllowInitialization and cInitializeAllow_CreateIndexes):
                                            unIndexReportEntry.update( {
                                                'status':                           'wrong_type',           
                                                'current_index_type':               unExistingIndexClassName,
                                            }) 
                                        else:
                                            unCatalog.delIndex( unIndexName)
                                            unosIndexesExistentes = unCatalog.indexes()
                                            if ( unIndexName in unosIndexesExistentes):    
                                                unIndexReportEntry.update( {
                                                    'status':                       'deletion_failed',           
                                                    'current_index_type':           unExistingIndexClassName,
                                                }) 
                                            else:
                                                if unIndexExtras:
                                                    unCatalog.addIndex( unIndexName, unIndexType, extra=unIndexExtras) 
                                                else:
                                                    unCatalog.addIndex( unIndexName, unIndexType) 
                                                    
                                                unosIndexesExistentes = unCatalog.indexes()
                                                if not ( unIndexName in unosIndexesExistentes):    
                                                    unIndexReportEntry.update( {
                                                        'status':                   'recreation_failed',           
                                                        'current_index_type':       unExistingIndexClassName,
                                                    }) 
                                                else:
                                                    unIndexesOrSchemasOrLexiconsAdded = True                            
                                                    unIndexReportEntry.update( {
                                                        'status':                   'recreated',           
                                                        'current_index_type':       unExistingIndexClassName,
                                                        'success':                  True,
                                                    }) 
                                                    
                                else:       
                                    if not ( theAllowInitialization and cInitializeAllow_CreateIndexes):
                                        unIndexReportEntry[ 'status'] = 'missing',
                                    else:
                                        if unIndexExtras:
                                            unCatalog.addIndex( unIndexName, unIndexType, extra=unIndexExtras) 
                                        else:
                                            unCatalog.addIndex( unIndexName, unIndexType) 
                                        unIndexesOrSchemasOrLexiconsAdded = True
                                        unosIndexesExistentes = unCatalog.indexes()
                                        if unIndexName in unosIndexesExistentes:
                                            unIndexReportEntry.update( {
                                                'status':                   'created',           
                                                'success':                  True,
                                            }) 
                                            
                                        else:
                                            unIndexReportEntry[ 'status'] = 'creation_failed',
                                             
                        
                                        
                                            
                                            
                                        
                            unosSchemaFieldsExistentes  = unCatalog.schema()
                            unosSchemaEntries = unCatalogReportEntry[ 'schemas']
            
                            for unSchemaFieldName in unCatalogSchemaFields:
                            
                                unLastSchemaFieldName = unSchemaFieldName
        
                                unSchemaReportEntry = self.fNewVoidInformeVerifyOrInitSchema( )
                                
                                unSchemaReportEntry.update( {
                                    'catalog_name':        unCatalogReportEntry.get( 'catalog_name', ''),
                                    'schema_field_name':   unSchemaFieldName,
                                })
                                unosSchemaEntries.append( unSchemaReportEntry)
                                
                                if unSchemaFieldName in unosSchemaFieldsExistentes:
                                    unSchemaReportEntry[ 'status'] = 'exists'
                                    unSchemaReportEntry[ 'success'] = True                                    
                                    
                                else:
                                    if not ( theAllowInitialization and cInitializeAllow_CreateSchemaFields):    
                                        unSchemaReportEntry[ 'status'] = 'missing',
                                    else:
                                        unCatalog.addColumn( unSchemaFieldName) 
                                        unosSchemaFieldsExistentes  = unCatalog.schema()
                                        if unSchemaFieldName in unosSchemaFieldsExistentes:
                                            unIndexesOrSchemasOrLexiconsAdded = True
                                            unSchemaReportEntry[ 'status'] = 'created'
                                            unSchemaReportEntry[ 'success'] = True                                                                        
                                        else:
                                            unSchemaReportEntry[ 'status'] = 'creation_failed'           
            
                                            
                            if unCatalogJustCreated or unIndexesOrSchemasOrLexiconsAdded:
                                unCatalogReportEntry[ 'must_run_recatalog_elements'] = True
                                            

                                 
                                                 
  
                        if ( not ( unCatalog == None)) and\
                           ( len( [ unaIndexEntry for unaIndexEntry in unCatalogReportEntry[ 'indexes']  if unaIndexEntry[ 'success'] ]) == len( unCatalogReportEntry[ 'indexes'])) and \
                           ( len( [ unSchemaEntry for unSchemaEntry in unCatalogReportEntry[ 'schemas']  if unSchemaEntry[ 'success'] ]) == len( unCatalogReportEntry[ 'schemas'])) and \
                           ( len( [ unSchemaEntry for unSchemaEntry in unCatalogReportEntry[ 'lexicons'] if unSchemaEntry[ 'success'] ]) == len( unCatalogReportEntry[ 'lexicons'])):
                            unCatalogReportEntry[ 'success'] = True
                            
                            
                        if unCatalogReportEntry.get( 'must_run_recatalog_elements', False):
                            unInforme[ 'must_run_recatalog_elements'] = True
                            
                            
                        if unCatalogJustCreated or unIndexesOrSchemasOrLexiconsAdded:
                            
                            if not self.getDebeRecatalogar():
                                self.setDebeRecatalogar( True)
                                
                            transaction.commit()
                            unCatalogReportEntry[ 'committed'] = True
                                
                    except:
                        unaExceptionInfo = sys.exc_info()
                        unInformeExcepcion = 'Exception during catalog initialization operation of catalog %s in %s. Lst index %s. Last schema %s\n' % ( unCatalogName, unContainerPath, unLastIndexName, unLastSchemaFieldName, ) 
                        unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                        try:
                            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                        except:
                            None
                        unInformeExcepcion += ''.join(traceback.format_exception( *unaExceptionInfo))   
                        unCatalogReportEntry[ 'success'] = False
                        unCatalogReportEntry[ 'exception'] = unInformeExcepcion
         
                        
                        
                    
                unInforme[ 'success'] = len( [ unCatalogReportEntry for unCatalogReportEntry in someReportEntries if unCatalogReportEntry[ 'success']]) == len( someReportEntries)
                        
                return unInforme
            
    
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during Lazy Initialization operation fVerifyOrInitializeCatalogsEIndicesEnContenedor\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                unInforme[ 'success'] = False
                unInforme[ 'condition'] = 'exception'
                unInforme[ 'exception'] = unInformeExcepcion
                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                    
                return unInforme
              
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()


    
    
  
   
    security.declarePrivate( 'fVerifyOrInitializeUserGroupsCatalogo')
    def fVerifyOrInitializeUserGroupsCatalogo(self, 
        theAllowInitialization         =False, 
        theCheckPermissions            =True, 
        thePermissionsCache            =None, 
        theRolesCache                  =None, 
        theParentExecutionRecord       =None):
        """Verify or initialize user groups, specific to this TRACatalog, for each of the roles that users may play when interacting with this TRACatalogo.
        
        """
        unExecutionRecord = self.fStartExecution( 'method',  'fVerifyOrInitializeUserGroupsCatalogo', theParentExecutionRecord, False) 

        try:
            
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
            
      
            # #########################################################
            """If so requested, check connected user permissions to perform a verification or initialzation.
            
            """
            if theCheckPermissions:
                
                aUseCasePermitted = self.fCheckVerifyOrInitializePermissions( 
                    theAllowInitialization   =theAllowInitialization,  
                    thePermissionsCache      =unPermissionsCache, 
                    theRolesCache            =unRolesCache, 
                    theParentExecutionRecord =unExecutionRecord
                )
                if not aUseCasePermitted:
                    
                    unInforme = self.fNewVoidInformeVerifyOrInitTodosUserGroups()
                    
                    unInforme[ 'success']   =  False
                    if theAllowInitialization:
                        unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_initialize_TRACatalogo
                    else:
                        unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_verify_TRACatalogo

                    return unInforme
                
                                          
            return self.fVerifyOrInitializeUserGroups(  
                theAllowInitialization                =theAllowInitialization, 
                theGroupsSpec                         =cTRAUserGroups_Catalogo, 
                theGroupIdResolver_lambda             =lambda theGroupName: self.fUserGroupIdEnCatalogoFor( theGroupName), 
                theGroupsNamesAndElementsToSetRoles   =[ 
                    [ cTRAUserGroups_Catalogo_AuthorizedOnCatalogo,             [ self,], ], 
                    # ACV 20090403 NOW discarded: Global catalogs not assigned roles in specific languages 
                    # ACV 20090914 NOW approach: Simpler security schema: no user groups for languages or modules, shall assign local roles to users directly on the language or module element
                    [ cTRAUserGroups_Catalogo_AuthorizedOnIndividualIdiomas,    self.fObtenerTodosIdiomas(), ], 
                    [ cTRAUserGroups_Catalogo_AuthorizedOnIndividualModulos,  [] + self.fObtenerTodosModulos(), ], 
                ], 
                theGroupIdToAddGroupToResolver_lambda =None,
                theCheckPermissions                   =False, 
                thePermissionsCache                   =unPermissionsCache, 
                theRolesCache                         =unRolesCache, 
                theParentExecutionRecord              =unExecutionRecord,
            )
   
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
    
   
    
    
    

    security.declarePrivate( 'fVerifyOrInitializeUserGroups')
    def fVerifyOrInitializeUserGroups(self, 
        theAllowInitialization                =False, 
        theGroupsSpec                         =None, 
        theGroupIdResolver_lambda             =None, 
        theGroupsNamesAndElementsToSetRoles   =None, 
        theGroupIdToAddGroupToResolver_lambda =None,
        theCheckPermissions                   =True, 
        thePermissionsCache                   =None, 
        theRolesCache                         =None, 
        theParentExecutionRecord              =None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fVerifyOrInitializeUserGroups', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }, 'spec: %s' % str( theGroupsSpec or '')) 

        try:
                
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
            
            try:
                unInforme = self.fNewVoidInformeVerifyOrInitTodosUserGroups()
                
                if not self.Title():
                    unInforme[ 'success']   =  False
                    unInforme[ 'condition'] = 'Premature_initialization'
                    return unInforme
                
                if not theGroupsSpec or not theGroupIdResolver_lambda:
                    unInforme[ 'success']   =  False
                    unInforme[ 'condition'] = 'MISSING_parameters'
                    return unInforme
                
                
                
                                    
                # #########################################################
                """If so requested, check connected user permissions to perform a verification or initialzation.
                
                """
                if theCheckPermissions:
                    
                    aUseCasePermitted = self.fCheckVerifyOrInitializePermissions( 
                        theAllowInitialization   =theAllowInitialization,  
                        thePermissionsCache      =unPermissionsCache, 
                        theRolesCache            =unRolesCache, 
                        theParentExecutionRecord =unExecutionRecord
                    )
                    if not aUseCasePermitted:
                        
                        unInforme[ 'success']   =  False
                        if theAllowInitialization:
                            unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_initialize_TRACatalogo
                        else:
                            unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_verify_TRACatalogo
    
                        return unInforme
                              
                    
        
                unaGroupsTool = self.getGroupsTool()
                if not unaGroupsTool:
                    return unInforme
                                
        
                unosInformesGroup = unInforme[ 'groups']
                
                
                for unGroupSpec in theGroupsSpec:
                    
                    unHaHabidoCambio = False
                    
                    unGroupName     = unGroupSpec[ 0]
                    unGroupRoles    = unGroupSpec[ 1]
                    
                    unGroupExists   = False   
                    
                    unInformeUserGroup = self.fNewVoidInformeVerifyOrInitUserGroup()
                    unGroupId = theGroupIdResolver_lambda( unGroupName)
                    unInformeUserGroup.update({
                        'name':     unGroupId,
                    })
                    unosInformesGroup.append( unInformeUserGroup)
                    
                    unosExistingGroups = unaGroupsTool.getGroupIds()
                    
                    if ( unGroupId in unosExistingGroups):
                        unInformeUserGroup.update({
                           'success':     True,
                           'status':      'existing',
                        })
                        unGroupExists = True
                    else:   
                        if not ( theAllowInitialization and cInitializeAllow_CreateUserGroups):
                            unInformeUserGroup[ 'success'] = False
                            unInformeUserGroup[ 'status'] = 'missing'         
                        else:
                            if unaGroupsTool.addGroup( unGroupId):  
                                
                                unHaHabidoCambio = True
    
                                unosExistingGroups = unaGroupsTool.getGroupIds()
                                if ( unGroupId in unosExistingGroups):
                                    unInformeUserGroup.update({
                                       'success':     True,
                                       'status':      'created',
                                    })
                                    unGroupExists = True
                                else:
                                    unInformeUserGroup.update({
                                       'success':     False,
                                       'status':      'creation_failure',
                                    })
                            else:
                                unInformeUserGroup.update({
                                    'success':     False,
                                    'status':      'creation_failure',
                                 })
                            
                    if unHaHabidoCambio:
                        transaction.commit()
                        unInforme[ 'committed'] = True
                    
                    if unGroupExists:
                        unosInformesRoles = unInformeUserGroup[ 'roles']
                        if theGroupsNamesAndElementsToSetRoles:
                            
                            for unGroupsNamesAndElementsToSetRoles in theGroupsNamesAndElementsToSetRoles:

                                unosGroupsNames = unGroupsNamesAndElementsToSetRoles[ 0]
                                if unGroupName in unosGroupsNames:
                                    unosElementsToSetRoles = unGroupsNamesAndElementsToSetRoles[ 1]
                                    if unosElementsToSetRoles:
                                        
                                        for unElementToSetRole in unosElementsToSetRoles:

                                            unInformeRoles = self.fLazySetLocalRolesForElement( 
                                                theAllowInitialization  =theAllowInitialization, 
                                                theElement              =unElementToSetRole, 
                                                theUserGroupId          =unGroupId, 
                                                theLocalRolesToSet      =unGroupRoles, 
                                                theCheckPermissions     =False, 
                                                thePermissionsCache     =unPermissionsCache, 
                                                theRolesCache           =unRolesCache, 
                                                theParentExecutionRecord=unExecutionRecord,
                                            )

                                            unosInformesRoles.append( unInformeRoles)
                                            unInformeUserGroup[ 'success'] = unInformeUserGroup[ 'success'] and unInformeRoles[ 'success']   
                                            
                                             
                        if theGroupIdToAddGroupToResolver_lambda:
                            unGroupIdToAddGroupTo = theGroupIdToAddGroupToResolver_lambda( unGroupName)
                            if unGroupIdToAddGroupTo:
                                unInformeAddGroupToGroup = self.fLazyAddGroupToGroup( 
                                    theAllowInitialization  =theAllowInitialization,
                                    theGroupIdToAdd         =unGroupId, 
                                    theContainerGroupId     =unGroupIdToAddGroupTo, 
                                    theCheckPermissions     =False, 
                                    thePermissionsCache     =unPermissionsCache, 
                                    theRolesCache           =unRolesCache, 
                                    theParentExecutionRecord=unExecutionRecord,                                    
                                ) 
                                if unInformeAddGroupToGroup:
                                    unInformeUserGroup[ 'add_group_to_group_result'] = unInformeAddGroupToGroup
                                    if not unInformeAddGroupToGroup[ 'success']:
                                        unInformeUserGroup[ 'success'] = False
                                        
                    
                if len( [ unInformeUserGroup for unInformeUserGroup in unosInformesGroup if unInformeUserGroup[ 'success'] ]) == len( unosInformesGroup):
                    unInforme[ 'success'] = True
        
                return unInforme
    
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during Lazy Initialization operation fVerifyOrInitializeUserGroups\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                unInforme[ 'success'] = False
                unInforme[ 'condition'] = 'exception'
                unInforme[ 'exception'] = unInformeExcepcion
               
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                    
                return unInforme
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

     
                    
        
            
             
    
    security.declarePrivate( 'fLazySetLocalRolesForElement')
    def fLazySetLocalRolesForElement(self, 
        theAllowInitialization  =False, 
        theElement              =None, 
        theUserGroupId          ='', 
        theLocalRolesToSet      =[], 
        theCheckPermissions     =True, 
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
       
        unExecutionRecord = self.fStartExecution( 'method',  'fLazySetLocalRolesForElement', theParentExecutionRecord, False, None, 'element: %s    roles_to_set: %s' % (( theElement and '/'.join( theElement.getPhysicalPath())) or 'unknown', ' '.join( theLocalRolesToSet or []))) 

        try:
                
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
                           
            try:
                unInforme = self.fNewVoidInformeLazySetLocalRoles()
                
                if not self.Title():
                    unInforme[ 'success']   =  False
                    unInforme[ 'condition'] = 'Premature_initialization'
                    return unInforme
                
                
                # #########################################################
                """If so requested, check connected user permissions to perform a verification or initialzation.
                
                """
                if theCheckPermissions:
                    
                    aUseCasePermitted = self.fCheckVerifyOrInitializePermissions( 
                        theAllowInitialization   =theAllowInitialization,  
                        thePermissionsCache      =unPermissionsCache, 
                        theRolesCache            =unRolesCache, 
                        theParentExecutionRecord =unExecutionRecord
                    )
                    if not aUseCasePermitted:
                        
                        unInforme[ 'success']   =  False
                        if theAllowInitialization:
                            unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_initialize_TRACatalogo
                        else:
                            unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_verify_TRACatalogo
    
                        return unInforme

                
                
                unElementType  = theElement.__class__.__name__
                unElementTitle = theElement.Title()
                unElementPath  = '/'.join( theElement.getPhysicalPath())
                unInforme.update( {            
                   'element_type':            unElementType,
                   'element_title':           unElementTitle,
                   'element_path':            unElementPath,
                })
                unosExistingGroupRoles = list( theElement.fLocalRolesForUserId( theUserGroupId))[:]
                unInforme[ 'previous_roles'] = unosExistingGroupRoles[:]
                

                unosNonExistingGroupRoles = list( set( theLocalRolesToSet) - set( unosExistingGroupRoles))
                if not unosNonExistingGroupRoles:
                    unInforme.update({
                        'success':          True,
                        'status':           'all existing',
                    })
                else:
                    if not ( theAllowInitialization and cInitializeAllow_CreateSetLocalRoles):
                        unInforme.update({
                            'success':       False,
                            'status':        'missing',
                            'new_roles':     [],
                            'failed_roles':  list( unosNonExistingGroupRoles)[:],
                        })
                         
                    else:
                        
                        theElement.manage_addLocalRoles( theUserGroupId, tuple( unosNonExistingGroupRoles))
                        # ACV 200903212354 learned from Products.CMFCore.MembershipTool.MembershipTool.setLocalRoles()                     
                        theElement.reindexObjectSecurity()
                        
                        unosNewExistingGroupRoles = list( theElement.fLocalRolesForUserId( theUserGroupId))[:]
                        unosNewNonExistingGroupRoles = list( set( theLocalRolesToSet) - set( unosNewExistingGroupRoles))
                        if unosNewNonExistingGroupRoles:
                            unInforme.update({
                                'success':       False,
                                'status':        'failure_adding_roles_to_existing',
                                'new_roles':     list( set( unosNewExistingGroupRoles) - set( unosExistingGroupRoles))[:],
                                'failed_roles':  list( unosNewNonExistingGroupRoles)[:],
                            })
                        else:
                            unInforme.update({
                                'success':       True,
                                'status':        'added_roles_to_existing',
                                'new_roles':     list( set( unosNewExistingGroupRoles) - set( unosExistingGroupRoles))[:],
                            })
        
                        transaction.commit()
                        unInforme[ 'committed'] = True
                    
                return unInforme
            
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during Lazy Initialization operation fLazySetLocalRolesForElement\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                unInforme[ 'success'] = False
                unInforme[ 'condition'] = 'exception'
                unInforme[ 'exception'] = unInformeExcepcion
            
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)

                return unInforme
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

         
     
    
    

            
    
    security.declarePrivate( 'fLazyAddGroupToGroup')
    def fLazyAddGroupToGroup(self, 
        theAllowInitialization  =False,
        theGroupIdToAdd         ='', 
        theContainerGroupId     ='', 
        theCheckPermissions     =True, 
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
       
        unExecutionRecord = self.fStartExecution( 'method',  'fLazyAddGroupToGroup', theParentExecutionRecord, False, None, 'container group: %s     group to add: %s' % ( theContainerGroupId or 'unknown', theGroupIdToAdd or 'unknown', )) 

        try:
                
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
                           
            try:
                
                unInforme = self.fNewVoidInformeAddGroupToGroup()
                
                if not theGroupIdToAdd or not theContainerGroupId:
                    return unInforme
                
                unInforme[ 'member_group_id'] = theGroupIdToAdd
                unInforme[ 'container_group_id'] = theContainerGroupId
                
                
               
                # #########################################################
                """If so requested, check connected user permissions to perform a verification or initialzation.
                
                """
                if theCheckPermissions:
                    
                    aUseCasePermitted = self.fCheckVerifyOrInitializePermissions( 
                        theAllowInitialization   =theAllowInitialization,  
                        thePermissionsCache      =unPermissionsCache, 
                        theRolesCache            =unRolesCache, 
                        theParentExecutionRecord =unExecutionRecord
                    )
                    if not aUseCasePermitted:
                        
                        unInforme[ 'success']   =  False
                        if theAllowInitialization:
                            unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_initialize_TRACatalogo
                        else:
                            unInforme[ 'condition'] = cTRAErrorMsgId_user_can_NOT_verify_TRACatalogo
    
                        return unInforme
                
                
                unPortalGroupsTool = self.getGroupsTool()
                if not unPortalGroupsTool:
                    return unInforme
                
                unCurrentContainerGroupMembers = unPortalGroupsTool.getGroupMembers( theContainerGroupId)
                if theGroupIdToAdd in unCurrentContainerGroupMembers:
                    unInforme[ 'success'] = True
                    unInforme[ 'status'] = 'was_member'
                else:
                    if not ( theAllowInitialization and cInitializeAllow_AddGroupToGroup):
                        unInforme[ 'success'] = False
                        unInforme[ 'status'] = 'missing'         
                    else:
                        unPortalGroupsTool.addPrincipalToGroup( theGroupIdToAdd, theContainerGroupId)
                        unNewContainerGroupMembers = unPortalGroupsTool.getGroupMembers( theContainerGroupId)
                        if theGroupIdToAdd in unNewContainerGroupMembers:
                            transaction.commit()
                            unInforme[ 'success'] = True
                            unInforme[ 'status'] = 'added'
                            unInforme[ 'committed'] = True
                        else:
                            unInforme[ 'success'] = False
                            unInforme[ 'status'] = 'add_error'
            
                return unInforme
            
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during Lazy Initialization operation fLazyAddGroupToGroup\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                unInforme[ 'success'] = False
                unInforme[ 'condition'] = 'exception'
                unInforme[ 'exception'] = unInformeExcepcion
            
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)

                return unInforme
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

            
            
            
            
            
            
            
            
            
            
         
    
    security.declarePrivate( 'pSetInitialPermissions')
    def pSetInitialPermissions(self,):
        
        # Add to logged user the TRACreator local role at the catalog
        #
        #
    
        aMemberId = self.fGetMemberId_safe()
        if aMemberId:
            unosLocalRolesForUser = self.fLocalRolesForUserId( aMemberId)
            if not ( cTRACreator_role in unosLocalRolesForUser):
                
                self.manage_addLocalRoles( aMemberId, tuple( [ cTRACreator_role,]))
                self.reindexObjectSecurity()
        
        self.fSetPermissions( 
            theAdditionalParams=None, 
            thePermissionsForElement=cTRACatalogoInitialPermissions,
        )

        return self
    
    
        
        
            
            
            

    # ##################################################################
       

    security.declarePrivate( 'pWriteLine')
    def pWriteLine( self, theOutput, theString, theIndentLevel):
        """Rendering of Lazy creation results.
        
        """
        if not theOutput or not theOutput:
            return self
        unIndentLevel = theIndentLevel
        if unIndentLevel < 0:
            unIndentLevel = 0
        theOutput.write( '%s%s\n' % ( cIndent * unIndentLevel, theString))   
        return self
    
    
    
    
    
    security.declarePrivate( 'fPrettyPrintLazyCreationResult')
    def fPrettyPrintLazyCreationResult( self, theInforme):
        
        if not theInforme:
            return ''
    
        try:
            
            anOutput= StringIO()
            anIndent = 0
            
            if not theInforme:
                self.pWriteLine( anOutput,  'No Report', 0)
                return anOutput.getvalue()
            
 
            self.pWriteLine( anOutput,  '\n\n%s\n\n' % ( ( theInforme.get( 'allow_creation', False) and 'Initializing translations catalog if necessary') or 'Verifying translations catalog initialization'), 0)     
 
            self.pWriteLine( anOutput,  'TRACatalogo title: %s' % theInforme.get( 'title', ''), 0)     
            self.pWriteLine( anOutput,  'TRACatalogo path:  %s\n'  % theInforme.get( 'path', ''), 0)  
            
            if theInforme.get( 'success', False):
                self.pWriteLine( anOutput,  'success\n', 0)
            else:
                self.pWriteLine( anOutput,  'failure: %s\n' % theInforme.get( 'condition', ''), 0)
                if theInforme.get( 'exception', ''):
                    self.pWriteLine( anOutput,  'exception:\n%s\n\n' % theInforme.get( 'exception', ''), 0)
                    
            self.pWriteLine( anOutput,  '\n', 0)
                        
                
                       
                
                
            unResultadoModelDDvlPloneTool = theInforme.get( 'ModelDDvlPloneTool', {})        
            if not unResultadoModelDDvlPloneTool:
                self.pWriteLine( anOutput,  'no ModelDDvlPloneTool initialization\n\n', 1)
            else:
                if unResultadoModelDDvlPloneTool.get( 'success', False):
                    self.pWriteLine( anOutput,  'success ModelDDvlPloneTool status: %s' % unResultadoModelDDvlPloneTool.get( 'status', ''), 1)    
                else:
                    self.pWriteLine( anOutput,  'FAILURE ModelDDvlPloneTool status: %s' % unResultadoModelDDvlPloneTool.get( 'status', ''), 1)    
                    if unResultadoModelDDvlPloneTool.get( 'exception', ''):
                        self.pWriteLine( anOutput,  'exception:\n%s\n\n' % unResultadoModelDDvlPloneTool.get( 'exception', ''), 1)

                self.pWriteLine( anOutput,  '\n', 1)
                
                
                
                
            unResultadoModelDDvlPloneConfiguration = theInforme.get( 'ModelDDvlPloneConfiguration', {})        
            if not unResultadoModelDDvlPloneConfiguration:
                self.pWriteLine( anOutput,  'no ModelDDvlPloneConfiguration initialization\n\n', 1)
            else:
                if unResultadoModelDDvlPloneConfiguration.get( 'success', False):
                    self.pWriteLine( anOutput,  'success ModelDDvlPloneConfiguration status: %s' % unResultadoModelDDvlPloneConfiguration.get( 'status', ''), 1)    
                else:
                    self.pWriteLine( anOutput,  'FAILURE ModelDDvlPloneConfiguration status: %s' % unResultadoModelDDvlPloneConfiguration.get( 'status', ''), 1)    
                    if unResultadoModelDDvlPloneConfiguration.get( 'exception', ''):
                        self.pWriteLine( anOutput,  'exception:\n%s\n\n' % unResultadoModelDDvlPloneConfiguration.get( 'exception', ''), 1)

                self.pWriteLine( anOutput,  '\n', 1)
                                
               
            unResultadoExtMethods = theInforme.get( 'external_methods', {})        
            if not unResultadoExtMethods:
                self.pWriteLine( anOutput,  'NO external_methods initializations\n\n', 1)
            else:
                if unResultadoExtMethods.get( 'success', False):
                    self.pWriteLine( anOutput,  'success external_methods', 1)    
                else:
                    self.pWriteLine( anOutput,  'FAILURE external_methods', 1)    
                    self.pWriteLine( anOutput,  'status % s' % unResultadoExtMethods.get( 'status', ''), 1)  
                    if unResultadoExtMethods.get( 'exception', ''):
                        self.pWriteLine( anOutput,  'exception:\n%s\n\n' % unResultadoExtMethods.get( 'exception', ''), 1)
                    
                self.pWriteLine( anOutput,  'external_methods initialization:', 1)
          
                for aExtMethodResult in unResultadoExtMethods.get( 'methods', []):
                    self.pWriteLine( anOutput,  'success: %s    id: %s     title: %s     module: %s      function: %s' % (  aExtMethodResult.get( 'success', False),  aExtMethodResult.get( 'ext_method_id', ''), aExtMethodResult.get( 'ext_method_title', ''), aExtMethodResult.get( 'ext_method_module', ''), aExtMethodResult.get( 'ext_method_function', ''), ), 2)    
                    self.pWriteLine( anOutput,  'committed: %s status %s ' % (  aExtMethodResult.get( 'committed', False), aExtMethodResult.get( 'status', ''), ), 3)    
                    if aExtMethodResult.get( 'exception', ''):
                        self.pWriteLine( anOutput,  'exception:\n%s\n\n' % aExtMethodResult.get( 'exception', ''), 2)
            
                self.pWriteLine( anOutput,  '\n', 1)
                                                                                             
            
            
            unResultadoUserGroups = theInforme.get( 'user_groups_catalogo', {})  
            self.fPrettyPrintLazyUserGroupsCreationResult_AtLevel( anOutput, unResultadoUserGroups, 'TRACatalogo')

            # ACV 20090914 Simpler security schema: no user groups for languages or modules, shall assign local roles to users directly on the language or module element
            #unResultadoUserGroups = theInforme.get( 'user_groups_all_idiomas', {})  
            #self.fPrettyPrintLazyUserGroupsCreationResult_AtLevel( anOutput, unResultadoUserGroups, 'TRACatalogo_AllIdiomas')

            #unosResultadosUserGroupsIdiomas = theInforme.get( 'user_groups_idiomas', [])  
            #for unResultadoUserGroups in unosResultadosUserGroupsIdiomas:
                #self.fPrettyPrintLazyUserGroupsCreationResult_AtLevel( anOutput, unResultadoUserGroups, 'TRAIdioma')

            #unosResultadosUserGroupsModulos = theInforme.get( 'user_groups_modulos', [])  
            #for unResultadoUserGroups in unosResultadosUserGroupsModulos:
                #self.fPrettyPrintLazyUserGroupsCreationResult_AtLevel( anOutput, unResultadoUserGroups, 'TRAModulo')
            
            
            unResultadoColecciones = theInforme.get( 'colecciones', {})        
            if not unResultadoColecciones:
                self.pWriteLine( anOutput,  'NO colecciones initializations\n\n', 1)
            else:
                if unResultadoColecciones.get( 'success', False):
                    self.pWriteLine( anOutput,  'success colecciones', 1)    
                else:
                    self.pWriteLine( anOutput,  'FAILURE colecciones', 1)    
                    self.pWriteLine( anOutput,  'status % s' % unResultadoColecciones.get( 'status', ''), 1)  
                    if unResultadoColecciones.get( 'exception', ''):
                        self.pWriteLine( anOutput,  'exception:\n%s\n\n' % unResultadoColecciones.get( 'exception', ''), 1)
                    
                self.pWriteLine( anOutput,  'colecciones initialization:', 1)
          
                for aColeccionReport in unResultadoColecciones.get( 'collections', []):
                    self.pWriteLine( anOutput,  'committed: %s %s %s %s %s' % (  aColeccionReport.get( 'committed', False), aColeccionReport.get( 'status', ''), aColeccionReport.get( 'tipo_coleccion', ''), aColeccionReport.get( 'id_coleccion', ''), aColeccionReport.get( 'titulo_coleccion', ''), ), 2)    
                    self.pWriteLine( anOutput,  'acquire_role_assignments_success: %s   must_acquire: %s   status: %s ' % (  aColeccionReport.get( 'acquire_role_assignments_success', False), str( aColeccionReport.get( 'acquire_role_assignments', '')), aColeccionReport.get( 'acquire_role_assignments_status', ''), ), 3)    
                     
                    if aColeccionReport.get( 'exception', ''):
                        self.pWriteLine( anOutput,  'exception:\n%s\n\n' % aColeccionReport.get( 'exception', ''), 3)
                        
                self.pWriteLine( anOutput,  '\n', 1)
                        
                
                
            unResultadoCatalogsCadenas = theInforme.get( 'catalogs_cadenas', {})        
            if not unResultadoCatalogsCadenas:
                self.pWriteLine( anOutput,  'NO catalogs_cadenas initializations\n\n', 1)
            else:
                if unResultadoCatalogsCadenas.get( 'success', False):
                    self.pWriteLine( anOutput,  'success catalogs_cadenas', 1)    
                else:
                    self.pWriteLine( anOutput,  'FAILURE catalogs_cadenas', 1)    
                if not ( unResultadoCatalogsCadenas.get( 'committed', False)):
                    self.pWriteLine( anOutput,  'NOT Committed catalogs_cadenas changes', 1)
                else:
                    self.pWriteLine( anOutput,  'COMMITTED catalogs cadenas  changes', 1)
                if not unResultadoCatalogsCadenas.get('catalogs', []):
                    self.pWriteLine( anOutput,  'no catalogos cadenas\n', 1)
                else:
                    self.pWriteLine( anOutput,  'catalogs cadenas initialization:', 1)
                    for aCatalogReport in unResultadoCatalogsCadenas.get('catalogs', []):
                        self.pPrettyPrintLazyCatalogCreationResult( anOutput, aCatalogReport, 2)
                        if aCatalogReport.get( 'exception', ''):
                            self.pWriteLine( anOutput,  'exception:\n%s\n\n' % aCatalogReport.get( 'exception', ''), 2)
                            
                self.pWriteLine( anOutput,  '\n', 0)    
            
            
            
            
            todosResultadosCatalogsIdiomas = theInforme.get( 'catalogs_idiomas', {})   
            if not unResultadoCatalogsCadenas:
                self.pWriteLine( anOutput,  'NO catalogs_idiomas initializations\n', 1)
            else:
                self.pWriteLine( anOutput,  'catalogs_idiomas initializations\n', 1)
                for unResultadoCatalogsIdioma in todosResultadosCatalogsIdiomas:
                    self.pWriteLine( anOutput,  'TRAIdioma type:     %s' % unResultadoCatalogsIdioma.get( 'container_type', ''), 2)
                    self.pWriteLine( anOutput,  'Container title:    %s' % unResultadoCatalogsIdioma.get( 'container_title', ''), 2)
                    self.pWriteLine( anOutput,  'Container path:     %s' % unResultadoCatalogsIdioma.get( 'container_path', ''), 2)
    
                    if unResultadoCatalogsIdioma.get( 'success', False):
                        self.pWriteLine( anOutput,  'success catalogs idioma', 2)    
                    else:
                        self.pWriteLine( anOutput,  'FAILURE catalogs idioma', 2)    
                    if not ( unResultadoCatalogsIdioma.get( 'committed', False)):
                        self.pWriteLine( anOutput,  'NOT Committed catalogs idioma changes', 2)
                    else:
                        self.pWriteLine( anOutput,  'COMMITTED catalogs idioma  changes', 2)
                    if not unResultadoCatalogsIdioma.get('catalogs', []):
                        self.pWriteLine( anOutput,  'no catalogos idiomas\n', 2)
                    else:
                        self.pWriteLine( anOutput,  'catalogs idioma initialization:', 2)
                  
                        for aCatalogReport in unResultadoCatalogsIdioma.get('catalogs', []):
                            self.pPrettyPrintLazyCatalogCreationResult( anOutput, aCatalogReport, 3)
                            if aCatalogReport.get( 'exception', ''):
                                self.pWriteLine( anOutput,  'exception:\n%s\n\n' % aCatalogReport.get( 'exception', ''), 3)
                            
                self.pWriteLine( anOutput,  '\n', 1)
                     
            
             
            aResult = anOutput.getvalue()
           
            return aResult
        except:
            unaExceptionInfo = sys.exc_info()
            unInformeExcepcion = 'Exception during printing of LazyCreation\n'  
            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
            try:
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
            except:
                None
            unInformeExcepcion += ''.join(traceback.format_exception( *unaExceptionInfo))   
            
            if cLogExceptions:
                logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                 
            return 'Error printing lazy creation result\nPartial print and exception traceback follows:\n%s\n%s\n' % ( anOutput.getvalue(), unInformeExcepcion, )
    
     
    
    
    security.declarePrivate('pPrettyPrintLazyCatalogCreationResult')
    def pPrettyPrintLazyCatalogCreationResult( self, theOutput, theCatalogReport, theIndentLevel):
        if not theOutput or not theCatalogReport:
            return self
        
        self.pWriteLine( theOutput,  'Container type:     %s' % theCatalogReport.get( 'container_type', ''), theIndentLevel)
        self.pWriteLine( theOutput,  'Container title:    %s' % theCatalogReport.get( 'container_title', ''), theIndentLevel)
        self.pWriteLine( theOutput,  'Container path:     %s' % theCatalogReport.get( 'container_path', ''), theIndentLevel)
        self.pWriteLine( theOutput,  'Catalog name:       %s' % theCatalogReport.get( 'catalog_name', ''), theIndentLevel)
        self.pWriteLine( theOutput,  'Catalog name:       %s' % theCatalogReport.get( 'catalog_name', ''), theIndentLevel)
        if theCatalogReport.get( 'success', False):
            self.pWriteLine( theOutput,  'Success', theIndentLevel)            
        else:
            self.pWriteLine( theOutput,  'Failure', theIndentLevel)
        
        
        self.pWriteLine( theOutput,  'Creation status:    %s' % theCatalogReport.get( 'status', ''), theIndentLevel)
        
        
        
        
        if theCatalogReport.get( 'exception', ''):
            self.pWriteLine( theOutput,  'Creation exception:', theIndentLevel)
            for unaExceptionLine in theCatalogReport.get( 'exception', '').splitlines():
                self.pWriteLine( theOutput,  '%s' % unaExceptionLine, theIndentLevel + 1)
            
                
                
        if theCatalogReport.get( 'must_run_recatalog_elements', False):
            self.pWriteLine( theOutput,  'Must Run Recatalog Elements', theIndentLevel)
            
            
            
            
        someIndexesReports = theCatalogReport.get( 'indexes', [])
        if not someIndexesReports:
            self.pWriteLine( theOutput,  'no indexes initialization', theIndentLevel)
        else:
            self.pWriteLine( theOutput,  'indexes initialization:', theIndentLevel)
            for anIndexReport in someIndexesReports:
                if anIndexReport.get( 'current_index_type', ''):
                    self.pWriteLine( theOutput,  'success: %s;   status: %s;   index name: %s;   index type: %s;   current index type: %s' % ( anIndexReport.get( 'success', ''), anIndexReport.get( 'status', ''), anIndexReport.get( 'index_name', ''), anIndexReport.get( 'index_type', ''), anIndexReport.get( 'current_index_type', ''), ), theIndentLevel + 1)    
                else:
                    self.pWriteLine( theOutput,  'success: %s;   status: %s;   index name: %s;   index type: %s' % ( anIndexReport.get( 'success', ''), anIndexReport.get( 'status', ''), anIndexReport.get( 'index_name', ''), anIndexReport.get( 'index_type', ''), ), theIndentLevel + 1)    

                    
                    
                    
                    
                    
                    
        someLexiconsReports = theCatalogReport.get( 'lexicons', [])
        if not someLexiconsReports:
            self.pWriteLine( theOutput,  'no lexicons initialization', theIndentLevel)
        else:
            self.pWriteLine( theOutput,  'lexicons initialization:', theIndentLevel)
            for anLexiconReport in someLexiconsReports:
                self.pWriteLine( theOutput,  'success: %s;   status: %s;   lexicon name: %s;   pipeline: %s' % ( anLexiconReport.get( 'success', ''), anLexiconReport.get( 'status', ''), anLexiconReport.get( 'lexicon_name', ''), anLexiconReport.get( 'pipeline', ''), ), theIndentLevel + 1)    

                
                
                
                
        someSchemasReports = theCatalogReport.get( 'schemas', [])
        if not someIndexesReports:
            self.pWriteLine( theOutput,  'no schemas initialization', theIndentLevel)
        else:
            self.pWriteLine( theOutput,  'schemas initialization:', theIndentLevel)
            for aSchemaReport in someSchemasReports:
                self.pWriteLine( theOutput,  'success: %s;   status: %s;   schema name: %s' % ( anIndexReport.get( 'success', ''), aSchemaReport.get( 'status', ''), aSchemaReport.get( 'schema_field_name', ''), ), theIndentLevel + 1)    
        
                
        self.pWriteLine( theOutput,  '\n\n' , 0)

        return self
    
    
    

          
    
    security.declarePrivate( 'fPrettyPrintLazyUserGroupsCreationResult_AtLevel')
    def fPrettyPrintLazyUserGroupsCreationResult_AtLevel(self, anOutput, theResultadoUserGroups, theLevelName):

        if not theResultadoUserGroups:
            return self
    
        unLevelName = theLevelName
        if not unLevelName:
            unLevelName = "unknown"
                        
        if not theResultadoUserGroups:
            self.pWriteLine( anOutput,  'NO User Groups initializations at %s level\n\n' % unLevelName, 1)
        else:
            if theResultadoUserGroups.get( 'success', False):
                self.pWriteLine( anOutput,  'success User Groups initializations at %s level' % unLevelName, 1)    
            else:
                self.pWriteLine( anOutput,  'FAILURE User Groups initializations at %s level' % unLevelName, 1)    
                self.pWriteLine( anOutput,  'status % s' % theResultadoUserGroups.get( 'status', ''), 1)  
                if theResultadoUserGroups.get( 'exception', ''):
                    self.pWriteLine( anOutput,  'exception:\n%s\n\n' % theResultadoUserGroups.get( 'exception', ''), 1)

            if not theResultadoUserGroups.get( 'committed', False):
                self.pWriteLine( anOutput,  'NOT Committed User Groups at %s level changes' % unLevelName, 1)
            else:
                self.pWriteLine( anOutput,  'COMMITTED User Groups at %s levelchanges' % unLevelName, 1)
                
            self.pWriteLine( anOutput,  'User Groups initialization at %s level:' % unLevelName, 1)
      
            for aUserGroupReport in theResultadoUserGroups.get( 'groups', []):
                self.pWriteLine( anOutput,  'name=%s    %s    status %s    condition: %s ' % ( aUserGroupReport.get( 'name', ''), ( aUserGroupReport.get( 'success', False) and 'success') or 'failure', aUserGroupReport.get( 'status', ''), aUserGroupReport.get( 'condition', ''), ), 2)   
                if aUserGroupReport.get( 'exception', ''):
                    self.pWriteLine( anOutput,  'exception:\n%s\n\n' % aUserGroupReport.get( 'exception', ''), 2)
                
                self.pWriteLine( anOutput,  'Roles for User Group at %s level' % unLevelName, 2)                        
                for aUserGroupRolesReport in aUserGroupReport[ 'roles']:
                    self.pWriteLine( anOutput,  'element_type: %s'  % aUserGroupRolesReport.get( 'element_type', ''), 3)
                    self.pWriteLine( anOutput,  'element_title: %s' % aUserGroupRolesReport.get( 'element_title', ''), 3)
                    self.pWriteLine( anOutput,  'element_path: %s'  % aUserGroupRolesReport.get( 'element_path', ''), 3)

                    if aUserGroupRolesReport.get( 'success', False):
                        self.pWriteLine( anOutput,  'success User Group Roles intialization at %s level' % unLevelName, 4)    
                        self.pWriteLine( anOutput,  'status % s' % aUserGroupRolesReport.get( 'status', ''), 4)  
                    else:
                        self.pWriteLine( anOutput,  'FAILURE User Group Roles initializations at %s level' % unLevelName, 4)    
                        self.pWriteLine( anOutput,  'status % s' % aUserGroupRolesReport.get( 'status', ''), 4)  
                        if aUserGroupRolesReport.get( 'exception', ''):
                            self.pWriteLine( anOutput,  'exception:\n%s\n\n' % aUserGroupRolesReport.get( 'exception', ''), 4)
                            
                    if not theResultadoUserGroups.get( 'committed', False):
                        self.pWriteLine( anOutput,  'NOT Committed User Group Roles at %s level' % unLevelName,  4)
                    else:
                        self.pWriteLine( anOutput,  'COMMITTED User Group Roles at %s level' % unLevelName,  4)
                    
                    self.pWriteLine( anOutput,  'previous_roles: %s' % ( ' '.join( aUserGroupRolesReport.get( 'previous_roles', []))), 4)
                    self.pWriteLine( anOutput,  'new_roles: %s'      % ( ' '.join( aUserGroupRolesReport.get( 'new_roles', []))), 4)
                    self.pWriteLine( anOutput,  'failed_roles: %s'   % ( ' '.join( aUserGroupRolesReport.get( 'failed_roles', []))), 4)

                anAddGroupToGroupReport = aUserGroupReport.get( 'add_group_to_group_result', None)
                if not anAddGroupToGroupReport:
                    pass # self.pWriteLine( anOutput,  'Adding group to group: No AddGroupToGroupReport', 3)
                else:
                    self.pWriteLine( anOutput,  'Adding group to group: %s   status: %s    container_group_id: %s    member_group_id: %s' % ( ( anAddGroupToGroupReport.get( 'success', False) and 'SUCCESS') or 'FAILED' , anAddGroupToGroupReport.get( 'status', ''), anAddGroupToGroupReport.get( 'container_group_id', ''), anAddGroupToGroupReport.get( 'member_group_id', '')), 3)
 

            self.pWriteLine( anOutput,  '\n', 1)
                        
                
        return self           
    
    
    
    
    
    
    

    
        
    


 
    # ACV 20090914 Simpler security schema: no user groups for languages or modules, shall assign local roles to users directly on the language or module element
    #security.declarePrivate( 'fVerifyOrInitializeUserGroupsAllIdiomas')
    #def fVerifyOrInitializeUserGroupsAllIdiomas(self, theAllowInitialization=False, theCheckPermissions=True, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):
        #unExecutionRecord = self.fStartExecution( 'method',  'fVerifyOrInitializeUserGroupsAllIdiomas', theParentExecutionRecord, False) 

        #try:
            #return self.fVerifyOrInitializeUserGroups(
                #theAllowInitialization,
                #cTRAUserGroups_AllIdiomas, 
                #lambda theGroupName: self.fUserGroupIdAllIdiomasFor( theGroupName), 
                #[ 
                    #[ cTRAUserGroups_AllIdiomas_AuthorizedOnColeccionIdiomas,        [ self.fObtenerColeccionIdiomas(),], ], 
                ##    [ cTRAUserGroups_AllIdiomas_AuthorizedOnIndividualIdiomas,       [ self.fObtenerColeccionIdiomas(),], ],  # ACV 200904040208 Added
                #], 
                #lambda theGroupName: self.fUserGroupIdEnCatalogoFor( theGroupName), 
                #theCheckPermissions,
                #thePermissionsCache,
                #theRolesCache,
                #unExecutionRecord
            #)    
        #finally:
            #unExecutionRecord and unExecutionRecord.pEndExecution()
    
   
    
   
    #security.declarePrivate( 'fVerifyOrInitializeUserGroupsAllModulos')
    #def fVerifyOrInitializeUserGroupsAllModulos(self, theAllowInitialization=False, theCheckPermissions=True, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):
        #unExecutionRecord = self.fStartExecution( 'method',  'fVerifyOrInitializeUserGroupsAllModulos', theParentExecutionRecord, False) 

        #try:
            #return self.fVerifyOrInitializeUserGroups(
                #theAllowInitialization,
                #cTRAUserGroups_AllModulos, 
                #lambda theGroupName: self.fUserGroupIdAllModulosFor( theGroupName), 
                #[ 
                    #[ cTRAUserGroups_AllModulos_AuthorizedOnColeccionModulos,          [ self.fObtenerColeccionModulos(),], ], 
                #], 
                #None,
                #theCheckPermissions,
                #thePermissionsCache,
                #theRolesCache,
                #unExecutionRecord
            #)    
        #finally:
            #unExecutionRecord and unExecutionRecord.pEndExecution()
    
   
    

    
    
    
   
    #security.declarePrivate( 'fVerifyOrInitializeUserGroupsIdiomas')
    #def fVerifyOrInitializeUserGroupsIdiomas(self, 
        #theAllowInitialization=False, 
        #theCheckPermissions=True, 
        #thePermissionsCache=None, 
        #theRolesCache=None, 
        #theParentExecutionRecord=None):
        
        #unExecutionRecord = self.fStartExecution( 'method',  'fVerifyOrInitializeUserGroupsIdiomas', theParentExecutionRecord, False) 

        #try:
            #unosIdiomas = self.fObtenerTodosIdiomas()
            #unosInformesIdiomas = []
            #for unIdioma in unosIdiomas:
                #unInforme = self.fVerifyOrInitializeUserGroupsParaIdioma(  
                    #theAllowInitialization, 
                    #unIdioma, 
                    #theCheckPermissions, 
                    #thePermissionsCache, 
                    #theRolesCache, 
                    #unExecutionRecord
                #)    
                #if unInforme:
                    #unosInformesIdiomas.append( unInforme)
         
            #return unosInformesIdiomas
        #finally:
            #unExecutionRecord and unExecutionRecord.pEndExecution()
    
  
    
    
    #security.declarePrivate( 'fVerifyOrInitializeUserGroupsParaIdioma')
    #def fVerifyOrInitializeUserGroupsParaIdioma(self, 
        #theAllowInitialization=False, 
        #theIdioma=None, 
        #theCheckPermissions=True, 
        #thePermissionsCache=None, 
        #theRolesCache=None, 
        #theParentExecutionRecord=None):
        
        #unExecutionRecord = self.fStartExecution( 'method',  'fVerifyOrInitializeUserGroupsParaIdioma', theParentExecutionRecord, False, None, 'language: %s' %  theIdioma or 'unknown') 

        #try:
            #if not theIdioma:
                #return []
            
            #return self.fVerifyOrInitializeUserGroups(  
                #theAllowInitialization, 
                #cTRAUserGroups_Idioma, 
                #lambda theGroupName: self.fUserGroupIdIdiomaFor( theGroupName, theIdioma), 
                #[ 
                    #[ cTRAUserGroups_Idioma_AuthorizedOnCatalogo,             [ self,], ], 
                    #[ cTRAUserGroups_Idioma_AuthorizedOnIdioma,               [ theIdioma,], ], 
                #], 
                #lambda theGroupName: self.fUserGroupIdEnCatalogoFor( theGroupName), 
                #theCheckPermissions, 
                #thePermissionsCache,
                #theRolesCache,
                #unExecutionRecord
            #)  
        #finally:
            #unExecutionRecord and unExecutionRecord.pEndExecution()
  
    
    
    
    
  
    
   
    #security.declarePrivate( 'fVerifyOrInitializeUserGroupsModulos')
    #def fVerifyOrInitializeUserGroupsModulos(self, theAllowInitialization=False, theCheckPermissions=True, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):
        #unExecutionRecord = self.fStartExecution( 'method',  'fVerifyOrInitializeUserGroupsModulos', theParentExecutionRecord, False) 

        #try:
            #unosModulos = self.fObtenerTodosModulos()
            #unosInformesModulos = []
            #for unModulo in unosModulos:
                #unInforme = self.fVerifyOrInitializeUserGroupsParaModulo(  
                    #theAllowInitialization, 
                    #unModulo, 
                    #theCheckPermissions, 
                    #thePermissionsCache, 
                    #theRolesCache, 
                    #unExecutionRecord
                #)    
                #if unInforme:
                    #unosInformesModulos.append( unInforme)
         
            #return unosInformesModulos
        #finally:
            #unExecutionRecord and unExecutionRecord.pEndExecution()
    
    
    
        
        
    #security.declarePrivate( 'fVerifyOrInitializeUserGroupsParaModulo')
    #def fVerifyOrInitializeUserGroupsParaModulo(self, 
        #theAllowInitialization=False, 
        #theModulo=None, 
        #theCheckPermissions=True, 
        #thePermissionsCache=None, 
        #theRolesCache=None, 
        #theParentExecutionRecord=None):
        
        #unExecutionRecord = self.fStartExecution( 'method',  'fVerifyOrInitializeUserGroupsParaModulo', theParentExecutionRecord, False) 

        #try:
            #if not theModulo:
                #return []
            
            #return self.fVerifyOrInitializeUserGroups( 
                #theAllowInitialization, 
                #cTRAUserGroups_Modulo, 
                #lambda theGroupName: self.fUserGroupIdModuloFor( theGroupName, theModulo), 
                #[  
                    #[ cTRAUserGroups_Modulo_AuthorizedOnCatalogo,             [ self,], ], 
                    #[ cTRAUserGroups_Modulo_AuthorizedOnModulo,               [ theModulo,], ], 
                #], 
                #None,
                #theCheckPermissions, 
                #thePermissionsCache,
                #theRolesCache,
                #unExecutionRecord
            #)  
        #finally:
            #unExecutionRecord and unExecutionRecord.pEndExecution()
    
  
    
          

##/code-section module-footer



