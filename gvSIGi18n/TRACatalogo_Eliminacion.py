# -*- coding: utf-8 -*-
#
# File: TRACatalogo_Eliminacion.py
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

from Products.CJKSplitter.CJKSplitter import CJKSplitter

from Products.CMFCore               import permissions
from Products.CMFCore.utils         import getToolByName
from Products.CMFCore.utils         import SimpleRecord



from Products.ModelDDvlPloneTool.ModelDDvlPloneTool import cModelDDvlPloneToolName, ModelDDvlPloneTool



from TRAElemento_Constants import *


from TRACatalogo_Inicializacion_Constants import *


from TRAElemento_Permission_Definitions import cTRAUserGroups_Catalogo, cTRAUserGroups_AllIdiomas, cTRAUserGroups_Idioma, cTRAUserGroups_Modulo
from TRAElemento_Permission_Definitions import cUseCase_InitializeTRACatalogo, cBoundObject
from TRAElemento_Permission_Definitions import cTRAUserGroups_Catalogo_AuthorizedOnCatalogo
from TRAElemento_Permission_Definitions import cTRAUserGroups_Catalogo_AuthorizedOnIndividualIdiomas, cTRAUserGroups_Catalogo_AuthorizedOnIndividualModulos
from TRAElemento_Permission_Definitions import cTRAUserGroups_AllIdiomas_AuthorizedOnColeccionIdiomas
from TRAElemento_Permission_Definitions import cTRAUserGroups_AllModulos_AuthorizedOnColeccionModulos
from TRAElemento_Permission_Definitions import cTRAUserGroups_Idioma_AuthorizedOnCatalogo, cTRAUserGroups_Idioma_AuthorizedOnIdioma
from TRAElemento_Permission_Definitions import cTRAUserGroups_Modulo_AuthorizedOnCatalogo, cTRAUserGroups_Modulo_AuthorizedOnModulo




##/code-section module-header

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema


##code-section after-schema #fill in your manual code here



cLogInformeBeforeDelete     = True



cBeforeDeleteExternalMethod       = True
cBeforeDeleteModelDDvlPloneTool   = True
cBeforeDeleteCollections          = True
cBeforeDeleteCatalogs             = True
cBeforeDeleteIndexes              = True
cBeforeDeleteLexicons             = True    
cBeforeDeleteSchemaFields         = True
cBeforeDeleteUserGroups           = True
cBeforeDeleteSetLocalRoles        = True
cBeforeDeleteSetAcquireRoleAssignments = True
cLazyAddGroupToGroup            = True




##/code-section after-schema

class TRACatalogo_Eliminacion:
    """
    """
    security = ClassSecurityInfo()


    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
# end of class TRACatalogo_Eliminacion

##code-section module-footer #fill in your manual code here



   

    


        
            
    
    security.declarePrivate('fNewVoidInformeBeforeDelete')
    def fNewVoidInformeBeforeDelete( self):
        unInforme = { 
            'allow_creation':   False,
            'success':           False,
            'condition':         '',
            'exception':         '',
            'title':             '',
            'path':              '',
            'ModelDDvlPloneTool':{},
            'colecciones':       {},
            'catalogs_cadenas':  {}, 
            'catalogs_idiomas':  [],
            'user_groups_catalogo':  {},
            'user_groups_idiomas':   {},
            'user_groups_modulos':   {},
        }
        return unInforme
    
    

   
    security.declarePrivate('fNewVoidInformeBeforeDeleteTodosExternalMethods')
    def fNewVoidInformeBeforeDeleteTodosExternalMethods( self):
        unInforme = {
            'type':         'external_methods',
            'methods':      [],
            'success':      False,
        }
        return unInforme    
    
    
    
    
    
    security.declarePrivate('fNewVoidInformeBeforeDeleteCollection')
    def fNewVoidInformeBeforeDeleteExternalMethod( self):
        unInforme = { 
            'type':                      'external_method',   
            'success':                   False,
            'status':                    '',           
            'committed':    False,
           ' ext_method_id':             '',
            'ext_method_title':          '',
            'ext_method_module':         '',
            'ext_method_function':       '',
         }
        return unInforme

    
        
    
    security.declarePrivate('fNewVoidInformeBeforeDeleteTool')
    def fNewVoidInformeBeforeDeleteTool( self):
        unInforme = { 
            'type':                      'tool',   
            'success':                   False,
            'status':                    '',           
            'committed':                 False,
            'tool_id':                   '',
            'tool_class_name':           '',
        }
        return unInforme

        
    
    security.declarePrivate('fNewVoidInformeBeforeDeleteTodasCollections')
    def fNewVoidInformeBeforeDeleteTodasCollections( self):
        unInforme = {
            'type':         'collections',
            'collections':  [],
            'success':      False,
        }
        return unInforme    
    
    
    
    
    security.declarePrivate('fNewVoidInformeBeforeDeleteCollection')
    def fNewVoidInformeBeforeDeleteCollection( self):
        unInforme = { 
            'type':                      'collection',   
            'container_type':            '',
            'container_title':           '',
            'container_path':            '',
            'success':                   False,
            'status':                    '',           
            'committed':                 False,
            'tipo_coleccion':            '',
            'id_coleccion':              '',
            'titulo_coleccion':          '',
            'acquire_role_assignments_success': False,
            'acquire_role_assignments_status':  '',
            'acquire_role_assignments':  None,
        }
        return unInforme

    
    
    
    security.declarePrivate('fNewVoidInformeBeforeDeleteTodosCatalogs')
    def fNewVoidInformeBeforeDeleteTodosCatalogs( self):
        unInforme = { 
            'committed':                 False,
            'catalogs':                  [],
            'success':                   False,
            'container_type':            '',
            'container_title':           '',
            'container_path':            '',
        }
        return unInforme
     
    
    
    
    security.declarePrivate('fNewVoidInformeBeforeDeleteCatalog')
    def fNewVoidInformeBeforeDeleteCatalog( self):
        unInforme = { 
            'type':                    'catalog',
            'container_type':          '',
            'container_title':         '',
            'container_path':          '',
            'catalog_name':            '',
            'success':                 False,
            'status':                  '',
            'exception':               '',
            'catalog_refreshed':       False,
            'indexes':                 [],
            'schemas':                 [],
            'lexicons':                [],
        }
        return unInforme

    
    
    
    
    security.declarePrivate('fNewVoidInformeBeforeDeleteIndex')
    def fNewVoidInformeBeforeDeleteIndex( self, theCatalogInforme):
        unInforme = theCatalogInforme.copy()
        unInforme.update( { 
            'type':                     'index',
            'success':                  False,
            'status':                   '',
            'index_name':               '',
            'index_type':               '',
            'current_index_type':       '',
        })
        
        return unInforme
    
    
    
    security.declarePrivate('fNewVoidInformeBeforeDeleteLexicon')
    def fNewVoidInformeBeforeDeleteLexicon( self, theCatalogInforme):
        unInforme = theCatalogInforme.copy()
        unInforme.update( { 
            'type':                    'lexicon',
            'success':                  False,
            'status':                   '',
            'lexicon_name':             '',
            'pipeline':                '',
        })
        
        return unInforme

    
    
    security.declarePrivate('fNewVoidInformeBeforeDeleteSchema')
    def fNewVoidInformeBeforeDeleteSchema( self, theCatalogInforme):
        unInforme = theCatalogInforme.copy()
        unInforme.update( { 
            'type':                     'schema',
            'success':                  False,
            'status':                   '',
            'schema_field_name':        '',
         })
        
        return unInforme
    
    
                                

    
    
    security.declarePrivate('fNewVoidInformeBeforeDeleteTodosUserGroups')
    def fNewVoidInformeBeforeDeleteTodosUserGroups( self):
        unInforme = { 
            'type':                     'user_groups',
            'committed':                 False,
            'groups':                    [],
            'success':                   False,
         }
        return unInforme
     
    
    

        
    security.declarePrivate('fNewVoidInformeBeforeDeleteUserGroup')
    def fNewVoidInformeBeforeDeleteUserGroup( self):
        unInforme = { 
            'type':                     'user_group',
            'name':                     [],
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
            'element_type':            '',
            'element_title':           '',
            'element_path':            '',
            'success':                 False,
            'status':                  '',
            'previous_roles':          [],
            'new_roles':               [],
            'failed_roles':            [],
            'committed':               False,
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

      
    
    
# #########################################################3
# Lazy initialization of collections and catalogs
#
# #########################################################3
    
    
    security.declareProtected( permissions.AddPortalFolders, 'fBeforeDeleteHTML')
    def fBeforeDeleteHTML( self, theAllowDeletion=False, theCheckPermissions=True, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):

        unExecutionRecord = self.fStartExecution( 'method',  'fBeforeDeleteHTML', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
        try:
            unInforme = self.fBeforeDelete( theAllowDeletion, theCheckPermissions, thePermissionsCache, theRolesCache, unExecutionRecord)
            
            unHTMLString = self.fPrettyPrintBeforeDeletionResultHTML( unInforme, unExecutionRecord)
    
            return unHTMLString
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
    
  
    
    
    security.declareProtected( permissions.AddPortalFolders, 'fBeforeDelete')
    def fBeforeDelete( self , theAllowDeletion=False, theCheckPermissions=True,  thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fBeforeDelete', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 

        try:

            unInforme = self.fNewVoidInformeBeforeDelete()
            
            try:
                
                unInforme[ 'allow_creation'] =  ( theAllowDeletion and True) or False
                unInforme[ 'type'] =  'TRACatalogo (root)'
                unInforme[ 'title'] =  self.Title()
                unInforme[ 'path']  =  '/'.join( self.getPhysicalPath())

                if not self.Title():
                    unInforme[ 'success']   =  False
                    unInforme[ 'condition'] = 'Premature_initialization'
                    return unInforme
                
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
                if theCheckPermissions:
                    
                    unUseCaseQueryResult = self.fUseCaseAssessment(  
                        theUseCaseName          = cUseCase_InitializeTRACatalogo, 
                        theElementsBindings     = { cBoundObject: self,},
                        theRulesToCollect       = [ ], 
                        thePermissionsCache     = unPermissionsCache, 
                        theRolesCache           = unRolesCache, 
                        theParentExecutionRecord= unExecutionRecord
                    )
                    if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                        unInforme[ 'success']   =  False
                        unInforme[ 'condition'] = 'user_can_NOT_initialize_TRACatalogo'
                        return unInforme
                                    
                                
                unInforme[ 'ModelDDvlPloneTool']               = self.fBeforeDeleteModelDDvlPloneTool(            theAllowDeletion, False, unPermissionsCache, unRolesCache, unExecutionRecord)
                unInforme[ 'external_methods']                 = self.fBeforeDeleteTodosExternalMethods(          theAllowDeletion, False, unPermissionsCache, unRolesCache, unExecutionRecord)
                unInforme[ 'colecciones']                      = self.fBeforeDeleteCollections(                   theAllowDeletion, False, unPermissionsCache, unRolesCache, unExecutionRecord)
                unInforme[ 'catalogs_cadenas']                 = self.fBeforeDeleteCatalogsEIndicesEnCatalogo(    theAllowDeletion, False, unPermissionsCache, unRolesCache, unExecutionRecord)
                unInforme[ 'catalogs_idiomas']                 = self.fBeforeDeleteCatalogsEIndicesTodosIdiomas(  theAllowDeletion, False, unPermissionsCache, unRolesCache, unExecutionRecord) 
                unInforme[ 'user_groups_catalogo']             = self.fBeforeDeleteUserGroupsCatalogo(            theAllowDeletion, False, unPermissionsCache, unRolesCache, unExecutionRecord)
                unInforme[ 'user_groups_all_idiomas']          = self.fBeforeDeleteUserGroupsAllIdiomas(          theAllowDeletion, False, unPermissionsCache, unRolesCache, unExecutionRecord)
                # unInforme[ 'user_groups_all_modulos']          = self.fBeforeDeleteUserGroupsAllModulos(          theAllowDeletion, False, unPermissionsCache, unRolesCache, unExecutionRecord)
                unInforme[ 'user_groups_idiomas']              = self.fBeforeDeleteUserGroupsIdiomas(             theAllowDeletion, False, unPermissionsCache, unRolesCache, unExecutionRecord)
                # unInforme[ 'user_groups_modulos']             = self.fBeforeDeleteUserGroupsModulos(             theAllowDeletion, False, unPermissionsCache, unRolesCache, unExecutionRecord)
                
                unInforme[ 'success'] = \
                    unInforme[ 'ModelDDvlPloneTool']            and unInforme[ 'ModelDDvlPloneTool'][ 'success'] and  \
                    unInforme[ 'external_methods']              and unInforme[ 'external_methods'][ 'success'] and  \
                    unInforme[ 'colecciones']                   and unInforme[ 'colecciones'][ 'success']  and  \
                    unInforme[ 'catalogs_cadenas']              and unInforme[ 'catalogs_cadenas'][ 'success'] and \
                    (( not unInforme[ 'catalogs_idiomas'])      or len( [ unInformeCatalogs for unInformeCatalogs in unInforme[ 'catalogs_idiomas'] if unInformeCatalogs[ 'success']]) == len( unInforme[ 'catalogs_idiomas'])) and \
                    unInforme[ 'user_groups_catalogo']          and unInforme[ 'user_groups_catalogo'][ 'success'] and \
                    unInforme[ 'user_groups_all_idiomas']       and unInforme[ 'user_groups_all_idiomas'][ 'success'] and \
                    (( not unInforme[ 'user_groups_idiomas'])   or len( [ unInformeGroups for unInformeGroups in unInforme[ 'user_groups_idiomas'] if unInformeGroups[ 'success']]) == len( unInforme[ 'user_groups_idiomas'])) # and
                    # unInforme[ 'user_groups_all_modulos']       and unInforme[ 'user_groups_all_modulos'][ 'success'] and  \
                    # (( not unInforme[ 'user_groups_modulos'])  or len( [ unInformeGroups for unInformeGroups in unInforme[ 'user_groups_modulos'] if unInformeGroups[ 'success']]) == len( unInforme[ 'user_groups_modulos'])) # and
            
                return unInforme
            
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during Lazy Initialization operation fBeforeDelete\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
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

            
 
 
 
    
    
    
        
        
# #############################################################
# TRAChangeAndBrowseTranslations ExternalMethod creation
#
# #############################################################
    
    
    
    security.declarePrivate( 'fBeforeDeleteTodosExternalMethods')
    def fBeforeDeleteTodosExternalMethods( self,  theAllowDeletion=False, theCheckPermissions=True, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):
       
        unExecutionRecord = self.fStartExecution( 'method',  'fBeforeDeleteTodosExternalMethods', theParentExecutionRecord, False) 

        try:

            unInforme = self.fNewVoidInformeBeforeDeleteTodosExternalMethods()
            
            try:
                if not self.Title():
                    unInforme[ 'success']   =  False
                    unInforme[ 'condition'] = 'Premature_initialization'
                    return unInforme

                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                    
                if theCheckPermissions:
                    
                    unUseCaseQueryResult = self.fUseCaseAssessment(  
                        theUseCaseName          = cUseCase_InitializeTRACatalogo, 
                        theElementsBindings     = { cBoundObject: self,},
                        theRulesToCollect       = [ ], 
                        thePermissionsCache     = unPermissionsCache, 
                        theRolesCache           = unRolesCache, 
                        theParentExecutionRecord= unExecutionRecord
                    )
                    if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                        unInforme[ 'success']   =  False
                        unInforme[ 'condition'] = 'user_can_NOT_initialize_TRACatalogo'
                        return unInforme

                someExternalMethodDefinitions = cExternalMetodDefinitions
                    
                for anExtMethodDefinition in someExternalMethodDefinitions:
                    aModuleName = anExtMethodDefinition[ 0]
                    someFunctionDefinitions = anExtMethodDefinition[ 1:]
                    for aFunctionDefinition in someFunctionDefinitions:
                        unInformeExtMethod = self.fBeforeDeleteExternalMethod( theAllowDeletion, aFunctionDefinition[1], aFunctionDefinition[2], aModuleName, aFunctionDefinition[0], False, thePermissionsCache=unPermissionsCache, theRolesCache=unRolesCache, theParentExecutionRecord=unExecutionRecord)
                        if unInformeExtMethod:    
                            unInforme[ 'methods'].append( unInformeExtMethod)
                       
                unInforme[ 'success'] = len( [ unInf for unInf in unInforme[ 'methods'] if unInf[ 'success']]) == len( unInforme[ 'methods'])
                
                return unInforme
            
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during Lazy Initialization operation fBeforeDeleteTodosExternalMethods\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
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

                
            
                
                
                
                
                
         
    security.declarePrivate( 'fBeforeDeleteExternalMethod')
    def fBeforeDeleteExternalMethod( self, theAllowDeletion=False, theExtMethodId='', theExtMethodTitle='', theModuleName='', theFunctionName='',  theCheckPermissions=True, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):
       
        unExecutionRecord = self.fStartExecution( 'method',  'fBeforeDeleteExternalMethod', theParentExecutionRecord, False, None, 'id= %s, title=%s, module=%s, function=%s' % ( theExtMethodId or '', theExtMethodTitle or '', theModuleName or '', theFunctionName or '')) 

        try:
                 
            unInforme = self.fNewVoidInformeBeforeDeleteTodosExternalMethods( )
            
            try:
                unInforme.update( {
                    'ext_method_module':         theModuleName,
                    'ext_method_function':       theFunctionName,
                    'ext_method_id':             theExtMethodId,
                    'ext_method_title':          theExtMethodTitle,
                })
                
                if not self.Title():
                    unInforme[ 'success']   =  False
                    unInforme[ 'condition'] = 'Premature_initialization'
                    return unInforme

                if not theExtMethodId or not theExtMethodTitle or not theModuleName or not theFunctionName:
                    unInforme[ 'success']   =  False
                    unInforme[ 'condition'] = 'MISSING_parameters'
                    return unInforme
                
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache

                if theCheckPermissions:
                    
                    unUseCaseQueryResult = self.fUseCaseAssessment(  
                        theUseCaseName          = cUseCase_InitializeTRACatalogo, 
                        theElementsBindings     = { cBoundObject: self,},
                        theRulesToCollect       = [ ], 
                        thePermissionsCache     = unPermissionsCache, 
                        theRolesCache           = unRolesCache, 
                        theParentExecutionRecord= unExecutionRecord
                    )
                    if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                        unInforme[ 'success']   =  False
                        unInforme[ 'condition'] = 'user_can_NOT_initialize_TRACatalogo'
                        return unInforme
                    
                unPortalRoot = self.fPortalRoot()
                if not unPortalRoot:
                    unInforme[ 'success']   =  False
                    unInforme[ 'condition'] = 'FAILURE_accessing_portal_root"'
                    return unInforme
                
                unExternalMethod = None
                try:
                    unExternalMethod = aq_get( unPortalRoot, theExtMethodId, None, 1)
                except:
                    None  
                if unExternalMethod:
                    unInforme[ 'success'] = True
                    unInforme[ 'status']  = 'exists'
                    return unInforme
                
                if not ( theAllowDeletion and cBeforeDeleteExternalMethod):
                    unInforme[ 'success'] = False
                    unInforme[ 'status'] = 'missing'         
                    return unInforme
                
                unNewExternalMethod = None
                try:
                    unNewExternalMethod = ExternalMethod(
                        theExtMethodId,
                        theExtMethodTitle,
                        theModuleName,
                        theFunctionName,
                    )
                except:
                    unaExceptionInfo = sys.exc_info()
                    unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                    
                    unInformeExcepcion = 'Exception during Lazy Initialization operation fBeforeDeleteExternalMethod\n' 
                    unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                    unInformeExcepcion += unaExceptionFormattedTraceback   
                             
                    unInforme[ 'success'] = False
                    unInforme[ 'condition'] = 'exception'
                    unInforme[ 'exception'] = unInformeExcepcion
                    
                    unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
    
                    if cLogExceptions:
                        logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                    
                    return unInforme
                
                if not unNewExternalMethod:
                    unInforme[ 'success'] = False
                    unInforme[ 'status']  = 'creation_failed'
                    return unInforme
                    
                unPortalRoot._setObject( theExtMethodId,  unNewExternalMethod)
                unExternalMethod = None
                try:
                    unExternalMethod = aq_get( unPortalRoot, theExtMethodId, None, 1)
                except:
                    None  
                if not unExternalMethod:
                    unInforme[ 'success'] = False
                    unInforme[ 'status']  = 'creation_failed'
                    return unInforme
                               
                unInforme[ 'success'] = True
                unInforme[ 'status']  = 'created'

                transaction.commit()
                unInforme[ 'committed'] = True
                
                return unInforme

            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during Lazy Initialization operation fBeforeDeleteExternalMethod\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
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

            
        



    
# #############################################################
# ModelDDvlPloneTool creation
#
# #############################################################
    

   
    security.declarePrivate( 'fBeforeDeleteModelDDvlPloneTool')
    def fBeforeDeleteModelDDvlPloneTool( self, theAllowDeletion=False, theCheckPermissions=True, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):
       
        unExecutionRecord = self.fStartExecution( 'method',  'fBeforeDeleteModelDDvlPloneTool', theParentExecutionRecord, False) 

        try:
            unInforme = self.fNewVoidInformeBeforeDeleteTool()
                
            try:
        
                if not self.Title():
                    unInforme[ 'success']   =  False
                    unInforme[ 'condition'] = 'Premature_initialization'
                    return unInforme
                    
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache

                if theCheckPermissions:
            
                    unUseCaseQueryResult = self.fUseCaseAssessment(  
                        theUseCaseName          = cUseCase_InitializeTRACatalogo, 
                        theElementsBindings     = { cBoundObject: self,},
                        theRulesToCollect       = [ ], 
                        thePermissionsCache     = unPermissionsCache, 
                        theRolesCache           = unRolesCache, 
                        theParentExecutionRecord= unExecutionRecord
                    )
                    if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                        unInforme[ 'success']   =  False
                        unInforme[ 'condition'] = 'user_can_NOT_initialize_TRACatalogo'
                        return unInforme    
                    
                    
                unPortalRoot = self.fPortalRoot()
                if not unPortalRoot:
                    unInforme[ 'success']   =  False
                    unInforme[ 'condition'] = 'No_portal_root'
                    return unInforme
                
                unInforme.update({
                    'tool_id':          cModelDDvlPloneToolName,
                    'tool_class_name':  'ModelDDvlPloneTool',
                })
                
                aModelDDvlPloneTool = None
                try:
                    aModelDDvlPloneTool = aq_get( unPortalRoot, cModelDDvlPloneToolName, None, 1)
                except:
                    None  
                if aModelDDvlPloneTool:
                    unInforme[ 'success'] = True
                    unInforme[ 'status']  = 'exists'
                    return unInforme
                
                if not ( theAllowDeletion and cBeforeDeleteModelDDvlPloneTool):
                    unInforme[ 'success'] = False
                    unInforme[ 'status'] = 'missing'         
                    return unInforme
         
                
                unaNuevaTool = ModelDDvlPloneTool( ) 
                unPortalRoot._setObject( cModelDDvlPloneToolName,  unaNuevaTool)
                aModelDDvlPloneTool = None
                try:
                    aModelDDvlPloneTool = aq_get( unPortalRoot, cModelDDvlPloneToolName, None, 1)
                except:
                    None  
                if not aModelDDvlPloneTool:
                    unInforme[ 'success'] = False
                    unInforme[ 'status']  = 'creation_failed'
                    return unInforme
                
                unInforme[ 'success'] = True
                unInforme[ 'status']  = 'created'
                
                return unInforme
            
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during Lazy Initialization operation fBeforeDeleteModelDDvlPloneTool\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
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

         

        
        

 
    
    
    # #############################################################
    # Collections creation
    #
    # #############################################################
    

    security.declarePrivate( 'fBeforeDeleteCollections')
    def fBeforeDeleteCollections( self, theAllowDeletion=False, theCheckPermissions=True, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):
       
        unExecutionRecord = self.fStartExecution( 'method',  'fBeforeDeleteCollections', theParentExecutionRecord, False) 

        try:
                
            unInforme = self.fNewVoidInformeBeforeDeleteTodasCollections()
            
            try:
                someCollectionEntries =  unInforme[ 'collections']
                
                    
                if not self.Title():
                    unInforme[ 'success']   =  False
                    unInforme[ 'condition'] = 'Premature_initialization'
                    return unInforme
                    
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache

                if theCheckPermissions:
            
                    unUseCaseQueryResult = self.fUseCaseAssessment(  
                        theUseCaseName          = cUseCase_InitializeTRACatalogo, 
                        theElementsBindings     = { cBoundObject: self,},
                        theRulesToCollect       = [ ], 
                        thePermissionsCache     = unPermissionsCache, 
                        theRolesCache           = unRolesCache, 
                        theParentExecutionRecord= unExecutionRecord
                    )
                    if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                        unInforme[ 'success']   =  False
                        unInforme[ 'condition'] = 'user_can_NOT_initialize_TRACatalogo'
                        return unInforme
                
                unContainerType = self.__class__.__name__
                unContainerTitle = self.Title()
                unContainerPath = '/'.join( self.getPhysicalPath())
                                
                for unaEspecificacionColeccion in cEspecificacionesColecciones:
                    unHayCambio = False
                    
                    unTipoColeccion    = unaEspecificacionColeccion[ 0]
                    unaIdColeccion     = unaEspecificacionColeccion[ 1]
                    unTituloColeccion  = unaEspecificacionColeccion[ 2]
                    
                    unCollectionReportEntry = self.fNewVoidInformeBeforeDeleteCollection()
                    unCollectionReportEntry.update( {            
                        'container_type':            unContainerType,
                        'container_title':           unContainerTitle,
                        'container_path':            unContainerPath,
                        'tipo_coleccion':            unTipoColeccion,
                        'id_coleccion':              unaIdColeccion,
                        'titulo_coleccion':          unTituloColeccion,
                        'success':                   False,
                        'status':                   '',
                    })
                    someCollectionEntries.append( unCollectionReportEntry)
                    # ACV 20090527 Found with victor unaCollection referenced before defined
                    unaCollection = None
                    unasCollections = self.objectValues(   unTipoColeccion)
                    if unasCollections: 
                        unaCollection = unasCollections[ 0]
                        unCollectionReportEntry[ 'status'] = 'exists'
                        unCollectionReportEntry[ 'success'] = True
        
                    else:
                        if not ( theAllowDeletion and cBeforeDeleteCollections):
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
                    
                    if unaCollection:
                        
                        if self.fLazySetAcquireRoleAssignments( 
                            theAllowDeletion,
                            unaCollection,
                            unCollectionReportEntry,
                            thePermissionsCache     = unPermissionsCache, 
                            theRolesCache           = unRolesCache, 
                            theParentExecutionRecord= unExecutionRecord):
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
                
                unInformeExcepcion = 'Exception during Lazy Initialization operation fBeforeDeleteCollections\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
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
    def fLazySetAcquireRoleAssignments( self, theAllowDeletion=False, theElement=None, theReport= {}, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):
       
        unExecutionRecord = self.fStartExecution( 'method',  'fLazySetAcquireRoleAssignments', theParentExecutionRecord, False, None, 'element: %s' % ( (theElement and '/'.join( theElement.getPhysicalPath())) or '')) 

        try:
            if not theElement:
                return theReport
            
            aAcquireRoleAssignments       = self.fAcquireRoleAssignmentsElement( theElement)
            aIsAcquiringRoleAssignments   = self.fIsAcquiringRoleAssignments(    theElement)
            
            if aAcquireRoleAssignments:
                if aIsAcquiringRoleAssignments:
                    theReport[ 'acquire_role_assignments']         = True
                    theReport[ 'acquire_role_assignments_success'] = True
                    theReport[ 'acquire_role_assignments_status']  = 'was_set'
                    return False
                else:
                    if ( theAllowDeletion and cBeforeDeleteSetAcquireRoleAssignments):
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
                    if ( theAllowDeletion and cBeforeDeleteSetAcquireRoleAssignments):
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

    

    
    
    # #############################################################
    # Catalogs and indexes creation
    #
    # #############################################################
    
                
 
    security.declarePrivate( 'fBeforeDeleteCatalogsEIndicesTodosIdiomas')
    def fBeforeDeleteCatalogsEIndicesTodosIdiomas( self, theAllowDeletion=False, theCheckPermissions=True, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):
        unExecutionRecord = self.fStartExecution( 'method',  'fBeforeDeleteCatalogsEIndicesTodosIdiomas', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 

        try:
            unosIdiomas = self.fObtenerTodosIdiomas()
            unosInformesIdiomas = []
            for unIdioma in unosIdiomas:
                unInforme = self.fBeforeDeleteCatalogsEIndicesParaIdioma(  
                    theAllowDeletion, 
                    unIdioma,
                    theCheckPermissions, 
                    thePermissionsCache, 
                    theRolesCache, 
                    unExecutionRecord
                )
                if unInforme:
                    unosInformesIdiomas.append( unInforme)
         
            return unosInformesIdiomas
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
    
       
    
    
    
    
        
 
    security.declarePrivate( 'fBeforeDeleteCatalogsEIndicesParaIdioma')
    def fBeforeDeleteCatalogsEIndicesParaIdioma( self, 
        theAllowDeletion=False, 
        theIdioma=None,  
        theCheckPermissions=True, 
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):
       
        unExecutionRecord = self.fStartExecution( 'method',  'fBeforeDeleteCatalogsEIndicesParaIdioma', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 

        try:
            try:

                if not self.Title():
                    unInforme = self.fNewVoidInformeBeforeDeleteTodosCatalogs()
                    unInforme[ 'success']   =  False
                    unInforme[ 'condition'] = 'Premature_initialization'
                    return unInforme

                if not theIdioma:
                    return self.fNewVoidInformeBeforeDeleteTodosCatalogs()
                
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
                if theCheckPermissions:
                    
                    unUseCaseQueryResult = self.fUseCaseAssessment(  
                        theUseCaseName          = cUseCase_InitializeTRACatalogo, 
                        theElementsBindings     = { cBoundObject: self,},
                        theRulesToCollect       = [ ], 
                        thePermissionsCache     = unPermissionsCache, 
                        theRolesCache           = unRolesCache, 
                        theParentExecutionRecord= unExecutionRecord
                    )
                    if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                        unInforme = self.fNewVoidInformeBeforeDeleteTodosCatalogs()
                        unInforme[ 'success']   =  False
                        unInforme[ 'condition'] = 'user_can_NOT_initialize_TRACatalogo'
                        return unInforme
                
                unSpecialPipelineSpec = None
                unCodigoIdioma = theIdioma.getCodigoIdiomaEnGvSIG()
                if not unCodigoIdioma:
                    return self.fNewVoidInformeBeforeDeleteTodosCatalogs()
                
                unLanguage, unCountry, unaVariation = self.fLanguageAndCountryAndVariationIdioma( unCodigoIdioma)
                if not unLanguage:
                    return self.fNewVoidInformeBeforeDeleteTodosCatalogs()
         
                if unLanguage in cLanguagesWithChineseJapaneseKoreanLexicon:
                    unSpecialPipelineSpec = cLexiconPipelineChineseJapaneseKorean[:]
                    
                return  self.fBeforeDeleteCatalogsEIndicesEnContenedor( 
                    theAllowDeletion, 
                    theIdioma, 
                    cCatalogsDetailsParaIdioma, 
                    theSpecialPipelineSpec=unSpecialPipelineSpec, 
                    theCheckPermissions=False, 
                    thePermissionsCache=unPermissionsCache, 
                    theRolesCache=unRolesCache, 
                    theParentExecutionRecord=unExecutionRecord
                )
    
    
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during Lazy Initialization operation fBeforeDeleteCatalogsEIndicesParaIdioma\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                unInforme = self.fNewVoidInformeBeforeDeleteTodosCatalogs()
                unInforme.update( {
                    'container_type':            theContenedor.__class__.__name__,
                    'container_title':           theContenedor.Title(),
                    'container_path':            '/'.join( theContenedor.getPhysicalPath()),
                    'committed':                 False,
                    'success':                   False,
                    'exception':                 unInformeExcepcion,
                })          

                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return unInforme
            
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

   
                
                
                
    security.declarePrivate( 'fBeforeDeleteCatalogsEIndicesEnCatalogo')
    def fBeforeDeleteCatalogsEIndicesEnCatalogo( self, theAllowDeletion=False, theCheckPermissions=True, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):
        unExecutionRecord = self.fStartExecution( 'method',  'fBeforeDeleteCatalogsEIndicesEnCatalogo', theParentExecutionRecord, False) 

        try:
            return self.fBeforeDeleteCatalogsEIndicesEnContenedor( 
                theAllowDeletion,
                self, 
                cCatalogsDetailsParaCadenas, 
                None, 
                theCheckPermissions, 
                thePermissionsCache, 
                theRolesCache, 
                unExecutionRecord
            )   
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
                
                
                

    security.declarePrivate( 'fBeforeDeleteCatalogsEIndicesEnContenedor')
    def fBeforeDeleteCatalogsEIndicesEnContenedor( self, 
        theAllowDeletion                    =False, 
        theContenedor                       = None, 
        theEspecificacionCatalogoEIndice    = None, 
        theSpecialPipelineSpec              =None, 
        theCheckPermissions                 =True, 
        thePermissionsCache                 =None, 
        theRolesCache                       =None, 
        theParentExecutionRecord            =None):
       
        unExecutionRecord = self.fStartExecution( 'method',  'fBeforeDeleteCatalogsEIndicesEnContenedor', theParentExecutionRecord, False, None, 'container: %s  spec: %s' % ( theContenedor and '/'.join( theContenedor.getPhysicalPath()), str( theEspecificacionCatalogoEIndice))) 

        try:
            
            unInformeEliminarCatalogs = self.fNewVoidInformeBeforeDeleteTodosCatalogs()

            try:
                if not self.Title():
                    unInformeEliminarCatalogs[ 'success']   =  False
                    unInformeEliminarCatalogs[ 'condition'] = 'Premature_initialization'
                    return unInformeEliminarCatalogs
                
                if not theContenedor or not theEspecificacionCatalogoEIndice:
                    unInformeEliminarCatalogs[ 'success']   =  False
                    unInformeEliminarCatalogs[ 'condition'] = 'MISSIG_parameters'
                    return unInformeEliminarCatalogs
        
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
                if theCheckPermissions:
                    unUseCaseQueryResult = self.fUseCaseAssessment(  
                        theUseCaseName          = cUseCase_InitializeTRACatalogo, 
                        theElementsBindings     = { cBoundObject: self,},
                        theRulesToCollect       = [ ], 
                        thePermissionsCache     = unPermissionsCache, 
                        theRolesCache           = unRolesCache, 
                        theParentExecutionRecord= unExecutionRecord
                    )
                    if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                        return unInformeEliminarCatalogs
                
                someReportEntries = unInformeEliminarCatalogs[ 'catalogs']
                
                unContainerType  = theContenedor.__class__.__name__
                unContainerTitle = theContenedor.Title()
                unContainerPath  = '/'.join( theContenedor.getPhysicalPath())
                unInformeEliminarCatalogs.update( {
                    'container_type':            unContainerType,
                    'container_title':           unContainerTitle,
                    'container_path':            unContainerPath,
                    'committed':                 False,
                    'success':                   False,
                })
                
                unCatalogsChanged = False
                
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
        
                    unCatalogReportEntry = self.fNewVoidInformeBeforeDeleteCatalog()
                    unCatalogReportEntry.update( {            
                        'container_type':            unContainerType,
                        'container_title':           unContainerTitle,
                        'container_path':            unContainerPath,
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
                            if not ( theAllowDeletion and cBeforeDeleteCatalogs):
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
                                
                                # special case for Chinese Japanese Korean indexing
                                if theSpecialPipelineSpec:
                                    unosPipelineElementNames = theSpecialPipelineSpec
        
                                unLexiconReportEntry = self.fNewVoidInformeBeforeDeleteLexicon( unCatalogReportEntry)
                                unLexiconReportEntry.update( {            
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
                                    if not ( theAllowDeletion and cBeforeDeleteLexicons):
                                        unLexiconReportEntry[ 'status'] = 'missing',
                                    else:
                                     
                                        unosPipelineElements     = []
                                     
                                        
                                        for unPipelineElementName in unosPipelineElementNames:
                                            if unPipelineElementName == 'Splitter':
                                                unosPipelineElements.append( Splitter())  
                                            elif unPipelineElementName == 'CaseNormalizer':
                                                unosPipelineElements.append( CaseNormalizer())  
                                            elif unPipelineElementName == 'StopWordRemover':
                                                unosPipelineElements.append( StopWordRemover())  
                                            elif unPipelineElementName == 'CJKSplitter':
                                                unosPipelineElements.append( CJKSplitter())  
                                        if not unosPipelineElements:
                                            unLexiconReportEntry.update( {
                                                'status':                               'empty_pipeline',           
                                                'success':                              False,
                                            }) 
                                        else:    
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
                                unIndexName     = unIndexSpec[ 0]
                                unIndexType     = unIndexSpec[ 1]
                                unIndexExtras   = None
                                if len( unIndexSpec) > 2:
                                    unIndexExtras= unIndexSpec[ 2]
                                
                                unLastIndexName = unIndexName
                                
                                unIndexReportEntry = self.fNewVoidInformeBeforeDeleteIndex( unCatalogReportEntry)
                                unIndexReportEntry.update( {            
                                    'type':                     'index',
                                    'index_name':               unIndexName,
                                    'index_type':               unIndexType,
                                    'current_index_type':       '',
                                    'status':                   '',
                                })
                                unosIndexesEntries.append( unIndexReportEntry)
                                
                                
                                if ( unIndexName in unosIndexesExistentes):    
                                    # ACV OJO 200903080425 should also check for the extras: if ZCTextIndex should have the lexicons specified
                                    unExistingIndexClassName = unCatalog.Indexes[ unIndexName].__class__.__name__
                                    if unExistingIndexClassName == unIndexType:
                                        unIndexReportEntry.update( {
                                            'status':                               'exists',           
                                            'success':                              True,
                                        }) 
                                    else:
                                        if not ( theAllowDeletion and cBeforeDeleteIndexes):
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
                                    if not ( theAllowDeletion and cBeforeDeleteIndexes):
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
        
                                unSchemaReportEntry = self.fNewVoidInformeBeforeDeleteSchema( unCatalogReportEntry)
                                unSchemaReportEntry[ 'schema_field_name'] = unSchemaFieldName
                                unosSchemaEntries.append( unSchemaReportEntry)
                                
                                if unSchemaFieldName in unosSchemaFieldsExistentes:
                                    unSchemaReportEntry[ 'status'] = 'exists'
                                    unSchemaReportEntry[ 'success'] = True                                    
                                    
                                else:
                                    if not ( theAllowDeletion and cBeforeDeleteSchemaFields):    
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
            
                            if unIndexesOrSchemasOrLexiconsAdded and not unCatalogJustCreated:
                                unCatalogsChanged = True
                                
                                unStartTime = self.fMillisecondsNow()
                                
                                unCatalog.refreshCatalog()
            
                                unEndTime = self.fMillisecondsNow()
                                unCatalogReportEntry[ 'catalog_refreshed'] = True
                                unCatalogReportEntry[ 'catalog_refresh_duration'] = unEndTime - unStartTime
                                
                            
                        if ( len( [ unaIndexEntry for unaIndexEntry in unCatalogReportEntry[ 'indexes']  if unaIndexEntry[ 'success'] ]) == len( unCatalogReportEntry[ 'indexes'])) and \
                           ( len( [ unSchemaEntry for unSchemaEntry in unCatalogReportEntry[ 'schemas']  if unSchemaEntry[ 'success'] ]) == len( unCatalogReportEntry[ 'schemas'])) and \
                           ( len( [ unSchemaEntry for unSchemaEntry in unCatalogReportEntry[ 'lexicons'] if unSchemaEntry[ 'success'] ]) == len( unCatalogReportEntry[ 'lexicons'])):
                            unCatalogReportEntry[ 'success'] = True
                            
                                
                    except:
                        unaExceptionInfo = sys.exc_info()
                        unInformeExcepcion = 'Exception during catalog initialization operation of catalog %s in %s. Lst index %s. Last schema %s\n' % ( unCatalogName, unContainerPath, unLastIndexName, unLastSchemaFieldName, ) 
                        unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                        unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                        unInformeExcepcion += ''.join(traceback.format_exception( *unaExceptionInfo))   
                        unCatalogReportEntry[ 'success'] = False
                        unCatalogReportEntry[ 'exception'] = unInformeExcepcion
         
                if unCatalogsChanged:
                    transaction.commit()
                    unInformeEliminarCatalogs[ 'committed'] = True
                    
                unInformeEliminarCatalogs[ 'success'] = len( [ unCatalogReportEntry for unCatalogReportEntry in someReportEntries if unCatalogReportEntry[ 'success']]) == len( someReportEntries)
                        
                return unInformeEliminarCatalogs
            
    
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during Lazy Initialization operation fBeforeDeleteCatalogsEIndicesEnContenedor\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                unInformeEliminarCatalogs[ 'success'] = False
                unInformeEliminarCatalogs[ 'condition'] = 'exception'
                unInformeEliminarCatalogs[ 'exception'] = unInformeExcepcion
                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                    
                return unInformeEliminarCatalogs
              
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()


    
    
  
   
    security.declarePrivate( 'fBeforeDeleteUserGroupsCatalogo')
    def fBeforeDeleteUserGroupsCatalogo(self, theAllowDeletion=False, theCheckPermissions=True, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):
        unExecutionRecord = self.fStartExecution( 'method',  'fBeforeDeleteUserGroupsCatalogo', theParentExecutionRecord, False) 

        try:
            return self.fBeforeDeleteUserGroups(  
                theAllowDeletion,
                cTRAUserGroups_Catalogo, 
                lambda theGroupName: self.fUserGroupIdEnCatalogoFor( theGroupName), 
                [ 
                    [ cTRAUserGroups_Catalogo_AuthorizedOnCatalogo,             [ self,], ], 
                    # ACV 20090403 Global catalogs not assigned roles in specific languages 
                    #[ cTRAUserGroups_Catalogo_AuthorizedOnIndividualIdiomas,    self.fObtenerTodosIdiomas(), ], 
                    # [ cTRAUserGroups_Catalogo_AuthorizedOnIndividualModulos,  [] + self.fObtenerTodosModulos(), ], 
                ], 
                None,
                theCheckPermissions,
                thePermissionsCache,
                theRolesCache,
                unExecutionRecord
            )    
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
    
   
    

 
   
    security.declarePrivate( 'fBeforeDeleteUserGroupsAllIdiomas')
    def fBeforeDeleteUserGroupsAllIdiomas(self, theAllowDeletion=False, theCheckPermissions=True, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):
        unExecutionRecord = self.fStartExecution( 'method',  'fBeforeDeleteUserGroupsAllIdiomas', theParentExecutionRecord, False) 

        try:
            return self.fBeforeDeleteUserGroups(
                theAllowDeletion,
                cTRAUserGroups_AllIdiomas, 
                lambda theGroupName: self.fUserGroupIdAllIdiomasFor( theGroupName), 
                [ 
                    [ cTRAUserGroups_AllIdiomas_AuthorizedOnColeccionIdiomas,        [ self.fObtenerColeccionIdiomas(),], ], 
                #    [ cTRAUserGroups_AllIdiomas_AuthorizedOnIndividualIdiomas,       [ self.fObtenerColeccionIdiomas(),], ],  # ACV 200904040208 Added
                ], 
                lambda theGroupName: self.fUserGroupIdEnCatalogoFor( theGroupName), 
                theCheckPermissions,
                thePermissionsCache,
                theRolesCache,
                unExecutionRecord
            )    
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
    
   
    
   
    security.declarePrivate( 'fBeforeDeleteUserGroupsAllModulos')
    def fBeforeDeleteUserGroupsAllModulos(self, theAllowDeletion=False, theCheckPermissions=True, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):
        unExecutionRecord = self.fStartExecution( 'method',  'fBeforeDeleteUserGroupsAllModulos', theParentExecutionRecord, False) 

        try:
            return self.fBeforeDeleteUserGroups(
                theAllowDeletion,
                cTRAUserGroups_AllModulos, 
                lambda theGroupName: self.fUserGroupIdAllModulosFor( theGroupName), 
                [ 
                    [ cTRAUserGroups_AllModulos_AuthorizedOnColeccionModulos,          [ self.fObtenerColeccionModulos(),], ], 
                ], 
                None,
                theCheckPermissions,
                thePermissionsCache,
                theRolesCache,
                unExecutionRecord
            )    
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
    
   
    

    
    
    
   
    security.declarePrivate( 'fBeforeDeleteUserGroupsIdiomas')
    def fBeforeDeleteUserGroupsIdiomas(self, 
        theAllowDeletion=False, 
        theCheckPermissions=True, 
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fBeforeDeleteUserGroupsIdiomas', theParentExecutionRecord, False) 

        try:
            unosIdiomas = self.fObtenerTodosIdiomas()
            unosInformesIdiomas = []
            for unIdioma in unosIdiomas:
                unInforme = self.fBeforeDeleteUserGroupsParaIdioma(  
                    theAllowDeletion, 
                    unIdioma, 
                    theCheckPermissions, 
                    thePermissionsCache, 
                    theRolesCache, 
                    unExecutionRecord
                )    
                if unInforme:
                    unosInformesIdiomas.append( unInforme)
         
            return unosInformesIdiomas
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
    
  
    
    
    security.declarePrivate( 'fBeforeDeleteUserGroupsParaIdioma')
    def fBeforeDeleteUserGroupsParaIdioma(self, 
        theAllowDeletion=False, 
        theIdioma=None, 
        theCheckPermissions=True, 
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fBeforeDeleteUserGroupsParaIdioma', theParentExecutionRecord, False, None, 'language: %s' %  theIdioma or 'unknown') 

        try:
            if not theIdioma:
                return []
            
            return self.fBeforeDeleteUserGroups(  
                theAllowDeletion, 
                cTRAUserGroups_Idioma, 
                lambda theGroupName: self.fUserGroupIdIdiomaFor( theGroupName, theIdioma), 
                [ 
                    [ cTRAUserGroups_Idioma_AuthorizedOnCatalogo,             [ self,], ], 
                    [ cTRAUserGroups_Idioma_AuthorizedOnIdioma,               [ theIdioma,], ], 
                ], 
                lambda theGroupName: self.fUserGroupIdEnCatalogoFor( theGroupName), 
                theCheckPermissions, 
                thePermissionsCache,
                theRolesCache,
                unExecutionRecord
            )  
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
  
    
    
    
    
  
    
   
    security.declarePrivate( 'fBeforeDeleteUserGroupsModulos')
    def fBeforeDeleteUserGroupsModulos(self, theAllowDeletion=False, theCheckPermissions=True, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):
        unExecutionRecord = self.fStartExecution( 'method',  'fBeforeDeleteUserGroupsModulos', theParentExecutionRecord, False) 

        try:
            unosModulos = self.fObtenerTodosModulos()
            unosInformesModulos = []
            for unModulo in unosModulos:
                unInforme = self.fBeforeDeleteUserGroupsParaModulo(  
                    theAllowDeletion, 
                    unModulo, 
                    theCheckPermissions, 
                    thePermissionsCache, 
                    theRolesCache, 
                    unExecutionRecord
                )    
                if unInforme:
                    unosInformesModulos.append( unInforme)
         
            return unosInformesModulos
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
    
    
    
        
        
    security.declarePrivate( 'fBeforeDeleteUserGroupsParaModulo')
    def fBeforeDeleteUserGroupsParaModulo(self, 
        theAllowDeletion=False, 
        theModulo=None, 
        theCheckPermissions=True, 
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fBeforeDeleteUserGroupsParaModulo', theParentExecutionRecord, False) 

        try:
            if not theModulo:
                return []
            
            return self.fBeforeDeleteUserGroups( 
                theAllowDeletion, 
                cTRAUserGroups_Modulo, 
                lambda theGroupName: self.fUserGroupIdModuloFor( theGroupName, theModulo), 
                [  
                    [ cTRAUserGroups_Modulo_AuthorizedOnCatalogo,             [ self,], ], 
                    [ cTRAUserGroups_Modulo_AuthorizedOnModulo,               [ theModulo,], ], 
                ], 
                None,
                theCheckPermissions, 
                thePermissionsCache,
                theRolesCache,
                unExecutionRecord
            )  
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
    
  
    
      
    
    

    security.declarePrivate( 'fBeforeDeleteUserGroups')
    def fBeforeDeleteUserGroups(self, 
        theAllowDeletion=False, 
        theGroupsSpec=None, 
        theGroupIdResolver_lambda=None, 
        theGroupsNamesAndElementsToSetRoles=None, 
        theGroupIdToAddGroupToResolver_lambda=None,
        theCheckPermissions=True, 
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fBeforeDeleteUserGroups', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }, 'spec: %s' % str( theGroupsSpec or '')) 

        try:
            try:
                unInforme = self.fNewVoidInformeBeforeDeleteTodosUserGroups()
                
                if not self.Title():
                    unInforme[ 'success']   =  False
                    unInforme[ 'condition'] = 'Premature_initialization'
                    return unInforme
                
                if not theGroupsSpec or not theGroupIdResolver_lambda:
                    unInforme[ 'success']   =  False
                    unInforme[ 'condition'] = 'MISSIG_parameters'
                    return unInforme
                
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
                
                if theCheckPermissions:
                    unUseCaseQueryResult = self.fUseCaseAssessment(  
                        theUseCaseName          = cUseCase_InitializeTRACatalogo, 
                        theElementsBindings     = { cBoundObject: self,},
                        theRulesToCollect       = [ ], 
                        thePermissionsCache     = unPermissionsCache, 
                        theRolesCache           = unRolesCache, 
                        theParentExecutionRecord= unExecutionRecord
                    )
                    if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                        return unInforme
        
                unaGroupsTool = self.getGroupsTool()
                if not unaGroupsTool:
                    return unInforme
                                
                unHaHabidoCambio = False
        
                unosInformesGroup = unInforme[ 'groups']
                
                
                for unGroupSpec in theGroupsSpec:
                    
                    unGroupName     = unGroupSpec[ 0]
                    unGroupRoles    = unGroupSpec[ 1]
                    
                    unGroupExists   = False   
                    
                    unInformeUserGroup = self.fNewVoidInformeBeforeDeleteUserGroup()
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
                        if not ( theAllowDeletion and cBeforeDeleteUserGroups):
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
                                                theAllowDeletion, 
                                                unElementToSetRole, 
                                                unGroupId, 
                                                unGroupRoles, 
                                                False, 
                                                thePermissionsCache     =unPermissionsCache, 
                                                theRolesCache           =unRolesCache, 
                                                theParentExecutionRecord=unExecutionRecord
                                            )

                                            unosInformesRoles.append( unInformeRoles)
                                            unInformeUserGroup[ 'success'] = unInformeUserGroup[ 'success'] and unInformeRoles[ 'success']   
                                            
                                             
                        if theGroupIdToAddGroupToResolver_lambda:
                            unGroupIdToAddGroupTo = theGroupIdToAddGroupToResolver_lambda( unGroupName)
                            if unGroupIdToAddGroupTo:
                                unInformeAddGroupToGroup = self.fLazyAddGroupToGroup( 
                                    theAllowDeletion,
                                    unGroupId, 
                                    unGroupIdToAddGroupTo, 
                                    unExecutionRecord
                                ) 
                                if unInformeAddGroupToGroup:
                                    unInformeUserGroup[ 'add_group_to_group_result'] = unInformeAddGroupToGroup
                                    if not unInformeAddGroupToGroup[ 'success']:
                                        unInformeUserGroup[ 'success'] = False
                                        
                    
                if unHaHabidoCambio:
                    transaction.commit()
                    unInforme[ 'committed'] = True
                    
                if len( [ unInformeUserGroup for unInformeUserGroup in unosInformesGroup if unInformeUserGroup[ 'success'] ]) == len( unosInformesGroup):
                    unInforme[ 'success'] = True
        
                return unInforme
    
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during Lazy Initialization operation fBeforeDeleteUserGroups\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
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
        theAllowDeletion        =False, 
        theElement              =None, 
        theUserGroupId          ='', 
        theLocalRolesToSet      =[], 
        theCheckPermissions     =False, 
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
       
        unExecutionRecord = self.fStartExecution( 'method',  'fLazySetLocalRolesForElement', theParentExecutionRecord, False, None, 'element: %s    roles_to_set: %s' % (( theElement and '/'.join( theElement.getPhysicalPath())) or 'unknown', ' '.join( theLocalRolesToSet or []))) 

        try:
            try:
                unInforme = self.fNewVoidInformeLazySetLocalRoles()
                
                if not self.Title():
                    unInforme[ 'success']   =  False
                    unInforme[ 'condition'] = 'Premature_initialization'
                    return unInforme
                
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
                if theCheckPermissions:
                    unUseCaseQueryResult = self.fUseCaseAssessment(  
                        theUseCaseName          = cUseCase_InitializeTRACatalogo, 
                        theElementsBindings     = { cBoundObject: self,},
                        theRulesToCollect       = [ ], 
                        thePermissionsCache     = unPermissionsCache, 
                        theRolesCache           = unRolesCache, 
                        theParentExecutionRecord= unExecutionRecord
                    )
                    if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                        return unInforme
                
                
                unElementType  = theElement.__class__.__name__
                unElementTitle = theElement.Title()
                unElementPath  = '/'.join( theElement.getPhysicalPath())
                unInforme.update( {            
                   'element_type':            unElementType,
                   'element_title':           unElementTitle,
                   'element_path':            unElementPath,
                })
                unosExistingGroupRoles = list( theElement.get_local_roles_for_userid( theUserGroupId))[:]
                unInforme[ 'previous_roles'] = unosExistingGroupRoles[:]
                

                unosNonExistingGroupRoles = list( set( theLocalRolesToSet) - set( unosExistingGroupRoles))
                if not unosNonExistingGroupRoles:
                    unInforme.update({
                        'success':          True,
                        'status':           'all existing',
                    })
                else:
                    if not ( theAllowDeletion and cBeforeDeleteSetLocalRoles):
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
                        
                        unosNewExistingGroupRoles = list( theElement.get_local_roles_for_userid( theUserGroupId))[:]
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
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
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
        theAllowDeletion        =False,
        theGroupIdToAdd         ='', 
        theContainerGroupId     ='', 
        theParentExecutionRecord=None):
       
        unExecutionRecord = self.fStartExecution( 'method',  'fLazyAddGroupToGroup', theParentExecutionRecord, False, None, 'container group: %s     group to add: %s' % ( theContainerGroupId or 'unknown', theGroupIdToAdd or 'unknown', )) 

        try:
            try:
                
                unInforme = self.fNewVoidInformeAddGroupToGroup()
                
                if not theGroupIdToAdd or not theContainerGroupId:
                    return unInforme
                
                unInforme[ 'member_group_id'] = theGroupIdToAdd
                unInforme[ 'container_group_id'] = theContainerGroupId
                
                unPortalGroupsTool = self.getGroupsTool()
                if not unPortalGroupsTool:
                    return unInforme
                
                unCurrentContainerGroupMembers = unPortalGroupsTool.getGroupMembers( theContainerGroupId)
                if theGroupIdToAdd in unCurrentContainerGroupMembers:
                    unInforme[ 'success'] = True
                    unInforme[ 'status'] = 'was_member'
                else:
                    if not ( theAllowDeletion and cLazyAddGroupToGroup):
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
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
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

            

    # ##################################################################
    # Rendering of Lazy creation results 
    #        

    security.declarePrivate( 'pWriteLine')
    def pWriteLine( self, theOutput, theString, theIndentLevel):
        if not theOutput or not theOutput:
            return self
        unIndentLevel = theIndentLevel
        if unIndentLevel < 0:
            unIndentLevel = 0
        theOutput.write( '%s%s\n' % ( cIndent * unIndentLevel, theString))   
        return self
    
    
    
    
    security.declarePrivate( 'fPrettyPrintBeforeDeletionResult')
    def fPrettyPrintBeforeDeletionResult( self, theInforme):
        
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
                    self.pWriteLine( anOutput,  'id: %s     title: %s     module: %s      function: %s' % (   aExtMethodResult.get( 'ext_method_id', ''), aExtMethodResult.get( 'ext_method_title', ''), aExtMethodResult.get( 'ext_method_module', ''), aExtMethodResult.get( 'ext_method_function', ''), ), 2)    
                    self.pWriteLine( anOutput,  'committed: %s status %s ' % (  aExtMethodResult.get( 'committed', False), aExtMethodResult.get( 'status', ''), ), 3)    
                    if aExtMethodResult.get( 'exception', ''):
                        self.pWriteLine( anOutput,  'exception:\n%s\n\n' % aExtMethodResult.get( 'exception', ''), 2)
            
                self.pWriteLine( anOutput,  '\n', 1)
                                                                                             
            
            
            unResultadoUserGroups = theInforme.get( 'user_groups_catalogo', {})  
            self.fPrettyPrintLazyUserGroupsCreationResult_AtLevel( anOutput, unResultadoUserGroups, 'TRACatalogo')

            unResultadoUserGroups = theInforme.get( 'user_groups_all_idiomas', {})  
            self.fPrettyPrintLazyUserGroupsCreationResult_AtLevel( anOutput, unResultadoUserGroups, 'TRACatalogo_AllIdiomas')

            unosResultadosUserGroupsIdiomas = theInforme.get( 'user_groups_idiomas', [])  
            for unResultadoUserGroups in unosResultadosUserGroupsIdiomas:
                self.fPrettyPrintLazyUserGroupsCreationResult_AtLevel( anOutput, unResultadoUserGroups, 'TRAIdioma')

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
            unInformeExcepcion = 'Exception during printing of BeforeDeletion\n'  
            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
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
            
                
                
        if theCatalogReport.get( 'catalog_refreshed', False):
            self.pWriteLine( theOutput,  'Refreshed', theIndentLevel)
            self.pWriteLine( theOutput,  'Refresh duration: %d milliseconds' % theCatalogReport.get( 'catalog_refresh_duration', 0), theIndentLevel)
            
            
            
            
            
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
    
    
    
    

    security.declarePrivate( 'fPrettyPrintBeforeDeletionResultHTML')
    def fPrettyPrintBeforeDeletionResultHTML(self, theBeforeDeletionResult, theParentExecutionRecord):
       
        unExecutionRecord = self.fStartExecution( 'method',  'fPrettyPrintBeforeDeletionResultHTML', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
        try:
            if not theBeforeDeletionResult:
                return ''
        
            aResult = self.fPrettyPrintBeforeDeletionResult( theBeforeDeletionResult)
            if not aResult:
                return ''
            
            anHTMLResult = '<p>%s</p>' % aResult.replace('\n', '\n<br/>\n').replace( cIndent, '&nbsp; ' * len( cIndent)).replace( ' ', '&nbsp;')
            return anHTMLResult
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
        
         
    
    
    
            
    
    


##/code-section module-footer



