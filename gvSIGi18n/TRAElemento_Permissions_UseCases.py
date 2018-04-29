# -*- coding: utf-8 -*-
#
# File: TRAElemento_Permissions_UseCases.py
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


import sys
import traceback
import logging

from StringIO                               import StringIO

from reStructuredText                       import HTML


from AccessControl                          import ClassSecurityInfo


from Products.CMFCore                       import permissions




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

from TRAElemento_Permission_Definitions     import *

from TRAElemento_Permission_Definitions_UseCases     import cTRAUseCasesWithAbbreviatedPermissions
from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_TRATraduccionStateChange




class TRAElemento_Permissions_UseCases:
    """Class with responsibility to deal with permissions to access elements and execute Use Cases.
    
    """
    
    security = ClassSecurityInfo()

    
    
 
    # #############################################################
    """Globals to hold the security specifications for Use Cases as ready to be assessed
       The structure in the source code is better suited
       for the view point of the requirements specifier
       and is re-structured and hashed as dictionaries for fast access.
    
     Some other information, as platform specific details,
       on which types shall or shall not acquire permissions
       or role assignments to users and user groups
       are also integrated ducing pre-processing.
    
     The permissions are specified with abbreviated string names 
       and are de-coded into their plone names during pre-processing
    
    """


    gUseCaseSpecificationsForTRACatalogsByName    = { }
 
        
    
    
    
    # #############################################################
    """Global to hold the rule handler jump table on rule mode.
    
    """
    gUseCaseRuleModeHandlers = { }
      
    
    
    
   
    # #############################################################
    """Use Case Query results structures
    
    """
    

    security.declarePrivate( 'fNewVoidUseCaseAssssment')
    def fNewVoidUseCaseAssssment(self, ):    
        unResult = {
            'use_case_name':            '',
            'elements_bindings':        None,
            'rules_to_collect':         False,
            'success':                  False,
            'status':                   '',
            'condition':                '',
            'exception':                '',
            'duration':                 0,
            'rule_assessments':         [ ],
            'rejected_objects':         set(),
            'collected_rule_assessments_by_name':          { },
        }
        return unResult
    
        

    security.declarePrivate( 'fNewVoidUseCaseRuleAssessment')
    def fNewVoidUseCaseRuleAssessment(self, ):    
        unResult = {
            'use_case_name':            '',
            'rule':                     '',  
            'path':                     [ ],
            'success':                  False,
            'status':                   '',
            'condition':                '',
            'exception':                '',
            'accepted_initial_objects': [ ],
            'accepted_final_objects':   [ ],
            'rejected_initial_objects': [ ],
            'rejected_final_objects':   [ ],
        }
        return unResult
    
     
    
    security.declarePrivate( 'fNewUseCaseRuleAssessment')
    def fNewUseCaseRuleObjectAssessment(self, theSuccess, theUseCaseName, theRule, theFailureAssessment, theObject, theAdditionalParamters=None):  
        anAssessment = {
            'success':                  theSuccess,    
            'use_case':                 theUseCaseName,    
            'rule':                     theRule,    
            'assessment':               theFailureAssessment,    
            'object':                   theObject,  
            'additional_parameters':    theAdditionalParamters,
        }
        return anAssessment

    
    


    

    
    # #############################################################


    security.declarePrivate( 'pClearUseCaseSpecificationsForTRACatalogsByName')
    def pClearUseCaseSpecificationsForTRACatalogsByName(self,):
        """Clear Use Cases Security configuration specification.
        
        """
        
        unPathDelRaiz = self.fPathDelRaiz()
        if not unPathDelRaiz:
            return self
        
        unosUseCaseSpecificationsForTRACatalogsByName = TRAElemento_Permissions_UseCases.gUseCaseSpecificationsForTRACatalogsByName
        
        if not unosUseCaseSpecificationsForTRACatalogsByName:
            return self
            
        try:    
            unosUseCaseSpecificationsForTRACatalogsByName.pop( unPathDelRaiz)
        except:
            None
            
        return self
    



    
    security.declarePrivate( 'fUseCaseSpecification')
    def fUseCaseSpecification(self, theUseCaseName):
        """Access and Lazy initialize Use Cases Security configuration specification .
        
        """

        if not theUseCaseName:
            return []
        
        unasUseCaseSpecifications = self.fUseCaseSpecificationsByName()
        if not unasUseCaseSpecifications:
            return []
        
        return unasUseCaseSpecifications.get( theUseCaseName, None)     
    
    
    
    
    
    
    
    security.declarePrivate( 'fUseCaseSpecificationsByName')
    def fUseCaseSpecificationsByName(self,):

        
        unPathDelRaiz = self.fPathDelRaiz()
        if not unPathDelRaiz:
            return { }
        
        
        unasUseCaseSpecificationsForTRACatalogsByElementType = TRAElemento_Permissions_UseCases.gUseCaseSpecificationsForTRACatalogsByName
        
        if not unasUseCaseSpecificationsForTRACatalogsByElementType:
            
            unasUseCaseSpecificationsForTRACatalogsByElementType = { }
            
            TRAElemento_Permissions_UseCases.gUseCaseSpecificationsForTRACatalogsByName = unasUseCaseSpecificationsForTRACatalogsByElementType
            
            

        unasUseCaseSpecifications = unasUseCaseSpecificationsForTRACatalogsByElementType.get( unPathDelRaiz, None)
        
        if not unasUseCaseSpecifications:
            
            unasUseCaseSpecifications = self.fUseCaseSpecificationsByName_Computed()
            
            unasUseCaseSpecificationsForTRACatalogsByElementType[ unPathDelRaiz] = unasUseCaseSpecifications
            
                    

        return unasUseCaseSpecifications    

    
        
        
        
            
    
    

    
     
    
    # #############################################################
    # #############################################################
 
    
    security.declarePrivate( 'fUseCaseSpecificationsByName_Computed')
    def fUseCaseSpecificationsByName_Computed( self,):
        """Lazy initialize Use Cases Access Security configuration specification 
    
        """
        unosNewUseCases = { }
    
        for unUseCaseName in cTRAUseCasesWithAbbreviatedPermissions.keys():
            
            unUseCaseSpec     = cTRAUseCasesWithAbbreviatedPermissions[ unUseCaseName]
            unosVerificables  = unUseCaseSpec[ 0]
            unosAdicionales   = unUseCaseSpec[ 1]
            
            unosNewVerificables = []
            unosNewAdicionales = []
            unNewUseCaseSpec = [ unosNewVerificables, unosNewAdicionales,]
            unosNewUseCases[ unUseCaseName] = unNewUseCaseSpec
             
            
            for unVerificable in unosVerificables:
                unosPerms   = unVerificable[ 'perms']
                unosRoles   = unVerificable[ 'roles']
                
                unNewVerificable = unVerificable.copy()
                unosNewVerificables.append( unNewVerificable)
                unasNewPerms = []
                unNewVerificable[ 'perms'] = [ unasNewPerms, ]                                      # to be an 'and' block of permissions in a one-element series of 'or' blocks
                unNewVerificable[ 'roles'] = [ [ unRol, ] for unRol in unosRoles ] # to be an 'and' block of roles in a one-element series of 'or' blocks
                
                for unaPermAbbreviation in unosPerms:    
                    unaPermission = cPermissionsByAbbreviation.get( unaPermAbbreviation, '')
                    if unaPermission:
                        unasNewPerms.append( unaPermission)
                        
                
     
            for unAdicional in unosAdicionales:
                unosTypes   = unAdicional[ 0]
                unosPerms   = unAdicional[ 1]
                unosRoles   = unAdicional[ 2]
    
                unosPerms   = unVerificable[ 'perms']
                
                unNewAdicional = unAdicional[:]
                unosNewAdicionales.append( unNewAdicional)
                unasNewPerms = []
                unNewAdicional[ 1] = [ unasNewPerms, ]                     # to be an 'and' block of permissions in a one-element series of 'or' blocks
                unNewAdicional[ 2] = [ [ unRol, ] for unRol in unosRoles ] # to be an 'and' block of roles in a one-element series of 'or' blocks
                
                for unaPermAbbreviation in unosPerms:    
                    unaPermission = cPermissionsByAbbreviation.get( unaPermAbbreviation, '')
                    if unaPermission:
                        unasNewPerms.append( unaPermission)
     
                        
        self.pOverrideUseCaseSpecificationsByNameWithConfiguration( unosNewUseCases)
        
        return unosNewUseCases
    



    
    
    

    
    security.declarePrivate( 'pOverrideUseCaseSpecificationsByNameWithConfiguration')
    def pOverrideUseCaseSpecificationsByNameWithConfiguration( self, theUseCases=None):
        
        if not theUseCases:
            return self
        
        
        unCatalogo = self.getCatalogo()
        if unCatalogo == None:
            return self
        
        
        unosAdditionalZopeRolesForTRARoles = { }
        
        unaConfiguracionPermissions = unCatalogo.fObtenerConfiguracion( cTRAConfiguracionAspecto_Permisos)
        if unaConfiguracionPermissions == None:
            return self
        
        unosAdditionalZopeRolesForTRARoles = unaConfiguracionPermissions.fAdditionalZopeRolesForTRARoles( )
        if not unosAdditionalZopeRolesForTRARoles:
            return self
            
        
        unosNombresUseCases = theUseCases.keys()
        for unNombreUseCase in unosNombresUseCases:

            unUseCaseSpec = theUseCases.get( unNombreUseCase, None)
            if unUseCaseSpec:

                unosVerificables  = unUseCaseSpec[ 0]
                unosAdicionales   = unUseCaseSpec[ 1]            
            
                for unVerificable in unosVerificables:

                    unosGruposRolesIniciales   = unVerificable[ 'roles']
                    
                    unosRolesTodosGrupos = set( )
                    
                    for unGrupoRoles in unosGruposRolesIniciales:
                        if unGrupoRoles:
                            if isinstance( unGrupoRoles, list) or  isinstance( unGrupoRoles, set) or isinstance( unGrupoRoles, tuple):
                                unosRolesTodosGrupos.update( unGrupoRoles)
                            else:
                                unosRolesTodosGrupos.add( unGrupoRoles)
                                
                                
                    unosRolesConAdicionales = unosRolesTodosGrupos.copy()
                    for unRol in unosRolesTodosGrupos:
                        unosRoles = unosAdditionalZopeRolesForTRARoles.get( unRol, None)
                        if unosRoles:
                            unosRolesConAdicionales.update( set( unosRoles))
                            
                    unosRolesAdicionales = unosRolesConAdicionales.difference( unosRolesTodosGrupos)    
                    if unosRolesAdicionales:
                        for unRolAdicional in unosRolesAdicionales:                            
                            unVerificable[ 'roles'].append( [ unRolAdicional,])
                    
            
                            
                            

                for unAdicional in unosAdicionales:

                    unosGruposRolesIniciales   = unAdicional[ 2]
                    
                    unosRolesTodosGrupos = set( )
                    
                    for unGrupoRoles in unosGruposRolesIniciales:
                        if unGrupoRoles:
                            if isinstance( unGrupoRoles, list) or  isinstance( unGrupoRoles, set) or isinstance( unGrupoRoles, tuple):
                                unosRolesTodosGrupos.update( unGrupoRoles)
                            else:
                                unosRolesTodosGrupos.add( unGrupoRoles)
                                
                                
                    unosRolesConAdicionales = unosRolesTodosGrupos.copy()
                    for unRol in unosRolesTodosGrupos:
                        unosRoles = unosAdditionalZopeRolesForTRARoles.get( unRol, None)
                        if unosRoles:
                            unosRolesConAdicionales.update( set( unosRoles))
                            
                    unosRolesAdicionales = unosRolesConAdicionales.difference( unosRolesTodosGrupos)    
                    if unosRolesAdicionales:
                        for unRolAdicional in unosRolesAdicionales:                            
                            unAdicional[ 2].append( [ unRolAdicional,])
                     
                    
 
        return self
    
    
         
    
    
    
    
    

     
    
    
    
    #security.declareProtected( permissions.View, 'fUseCaseAssessment_TranslationStateChange')
    #def fUseCaseAssessment_TranslationStateChange(self, theTraduccion, theTargetState, thePermissionsCache, theRolesCache, theParentExecutionRecord ):  
        #if not theTraduccion or not theTargetState:
            #return False
        #unaCadena = theTraduccion.getCadena()
        #if not unaCadena:
            #return False
        #unIdioma = theTraduccion.fObtenerIdioma()
        #if not unIdioma:
            #return False
        #unosModulos = theTraduccion.fObtenerModulos()
        
        #unPermissionsCache = fDictOrNew( thePermissionsCache)
        #unRolesCache       = fDictOrNew( theRolesCache)
        
        #aUseCaseAssessmentResult = self.fUseCaseAssessment( 
            #theUseCaseName          = cUseCase_TRATraduccionStateChange, 
            #theElementsBindings     = { cBoundObject: theTraduccion,},
            #theRulesToCollect       = [ ], 
            #thePermissionsCache     = unPermissionsCache, 
            #theRolesCache           = unRolesCache, 
            #theParentExecutionRecord= unExecutionRecord,
        #)
        #if not aUseCaseAssessmentResult or not aUseCaseAssessmentResult.get( 'success', False):
            #return False
        
        #return theTraduccion.fCanChangeToNuevoEstadoTraduccion( theTargetState)
    
      
    

    
    
            
            
            

    security.declarePublic('fUseCaseCheckDoableFactory')
    def fUseCaseCheckDoableFactory(self, theTypeName, theUseCaseName, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):     
        return self.fUseCaseCheckDoable( 
            theUseCaseName           = theUseCaseName,
            thePermissionsCache      = thePermissionsCache,
            theRolesCache            = theRolesCache,
            theParentExecutionRecord = theParentExecutionRecord
        )
    
        
        
    
        
    security.declarePublic('fUseCaseCheckDoable')
    def fUseCaseCheckDoable(self, 
        theUseCaseName           =None, 
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None):     

        unExecutionRecord = self.fStartExecution( 'method',  'fUseCaseCheckDoable', theParentExecutionRecord, False) 
        
        try:
            try:
                if not theUseCaseName:
                    return False
                
                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)
                    
                unUseCaseAssessmentResult = self.fUseCaseAssessment( 
                    theUseCaseName          = theUseCaseName, 
                    theElementsBindings     = { 'object': self,},
                    theRulesToCollect       = None, 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord)
                
                unResult = unUseCaseAssessmentResult and unUseCaseAssessmentResult.get( 'success', False)
                return unResult 
    
    
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fUseCaseCheckDoable for UseCase named: %s\n'  % str( theUseCaseName)
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
     
        
                
            
            
            
            

 
    security.declarePrivate( 'fUseCaseAssessment')
    def fUseCaseAssessment(self, 
        theUseCaseName, 
        theElementsBindings     ={}, 
        theRulesToCollect       =False, 
        theRulesToBypass        =[],
        thePredicateOverrides   ={},
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):  
        """Assess the security rules specified for theUseCaseName against objects obtained from theElementBindings retrieving the elements accepted by the rules in theRulesToCollect and optionally gathering the result of every rule assessment.

        """        
        
        unExecutionRecord = self.fStartExecution( 'method',  'fUseCaseAssessment', theParentExecutionRecord, False, None, 'usecase %s' % (theUseCaseName or 'unknown')) 

        unStartTime = self.fMillisecondsNow() 
        unUseCaseAssesment = None

        try:
               
            unaLastUseCaseRule = None
            try:
                
                unUseCaseAssesment = self.fNewVoidUseCaseAssssment()
 
                if not theUseCaseName:
                    unUseCaseAssesment[ 'status']     = 'fUseCaseAssessment_Missing_parameter_UseCaseName'
                    return unUseCaseAssesment
                
                if not theElementsBindings:
                    unUseCaseAssesment[ 'status']     = 'fUseCaseAssessment_NoBindings'
                    unUseCaseAssesment[ 'condition']  = theUseCaseName
                    return unUseCaseAssesment

                unUseCaseAssesment[ 'use_case_name'] = theUseCaseName
                
                
                someElementsBindings = theElementsBindings   
                if not someElementsBindings:
                    # ##################################################################
                    """Because the use case assessment request specified no element bindings,
                    build a bindings dictionary binding this element as the default binding.
                    
                    """
                    someElementsBindings = { cBoundObject: self, }

                unUseCaseAssesment[ 'elements_bindings'] = someElementsBindings
                
        
                 
                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)
                   
                # ##################################################################
                """Obtain Use Case security specification by its name

                """
                unUseCaseSpec = self.getCatalogo().fUseCaseSpecification( theUseCaseName)
                
                if not unUseCaseSpec:
                    unUseCaseAssesment[ 'status']     = 'fUseCaseAssessment_NoUseCase'
                    unUseCaseAssesment[ 'condition']  = theUseCaseName
                    return unUseCaseAssesment
                       
                
                unasUseCaseRules  = unUseCaseSpec[ 0]
                unosUsedUseCaseRuleNames = set()

                unasRulesToCollect = set()
                
                if theRulesToCollect:
                    if theRulesToCollect == True:
                        unasRulesToCollect = set( [ unaUseCaseRule.get( 'name', cPermissionRuleNameDefault) for unaUseCaseRule in unasUseCaseRules])
                    else:
                        if theRulesToCollect.__class__.__name__ in [ 'list', 'tuple', 'set',]:
                            unasRulesToCollect = set( theRulesToCollect)
                        else:
                            unasRulesToCollect = set( [ theRulesToCollect, ])
                                     
                
                unasRuleAssessments                = unUseCaseAssesment[ 'rule_assessments']
                unasCollectedRuleAssessmentsByName = unUseCaseAssesment[ 'collected_rule_assessments_by_name']
                
                for unaUseCaseRule in unasUseCaseRules:
                    
                    unaLastUseCaseRule = unaUseCaseRule
                                       
                    # ##################################################################
                    """Check all the rules one after the other
                    If any rule fails the use case shall fail.
                    
                    """
                    
                    
                    unBaseRuleName  = unaUseCaseRule.get( 'name',  cPermissionRuleNameDefault)    
                    
                    if theRulesToBypass and unBaseRuleName and ( unBaseRuleName in theRulesToBypass):
                        continue
                    
                    unRuleName = unBaseRuleName
                    unNameCounter = 0
                    while unRuleName in unosUsedUseCaseRuleNames:
                        unNameCounter += 1
                        unRuleName = '%s-%d' % ( unBaseRuleName, unNameCounter,)
                    unosUsedUseCaseRuleNames.add( unRuleName)        
                    
                    unRuleAssessement = self.fUseCaseRuleAssessment( 
                        theUseCaseName          = theUseCaseName,
                        theUseCaseRule          = unaUseCaseRule, 
                        theRuleName             = unRuleName,
                        theUseCaseAssessment    = unUseCaseAssesment,
                        theMustCollect          = unBaseRuleName in unasRulesToCollect,
                        thePredicateOverrides   = thePredicateOverrides,
                        thePermissionsCache     = unPermissionsCache, 
                        theRolesCache           = unRolesCache, 
                        theParentExecutionRecord= unExecutionRecord)
                    
                    if unRuleAssessement:
                        unasRuleAssessments.append( unRuleAssessement)
                        
                        if unBaseRuleName in unasRulesToCollect:
                            unasCollectedRuleAssessmentsByName[ unBaseRuleName] = unRuleAssessement
        
                    if not unRuleAssessement or not unRuleAssessement.get( 'success', False):
                        unUseCaseAssesment[ 'success']    = False
                        unUseCaseAssesment[ 'status']     = 'fUseCaseAssessment_RuleFailed'
                        unUseCaseAssesment[ 'condition']  = unaUseCaseRule.get( 'name', cPermissionRuleNameDefault)
                        
                        return unUseCaseAssesment
   
                unaUseCaseRule = None
                
                unUseCaseAssesment[ 'success']     = True
                return unUseCaseAssesment
            
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fUseCaseAssessment %s.\n'  % ( unaLastUseCaseRule and ( 'While assessing rule %s' % unaLastUseCaseRule.get( 'name', cPermissionRuleNameDefault))) or  ''
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   
                    
                if unUseCaseAssesment:
                    unUseCaseAssesment[ 'success']   = False   
                    unUseCaseAssesment[ 'status']     = 'fUseCaseAssessment_Exception'
                    unUseCaseAssesment[ 'exception'] =   unInformeExcepcion
                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return unUseCaseAssesment
                 
                
        finally:
            unEndTime = self.fMillisecondsNow() 
            if unUseCaseAssesment:
                unUseCaseAssesment[ 'duration']  = unEndTime - unStartTime
 
            unExecutionRecord and unExecutionRecord.pEndExecution()
            
 
                
            
  
            
            
     
            
 
    security.declarePrivate( 'fUseCaseRuleAssessment')
    def fUseCaseRuleAssessment(self, 
        theUseCaseName,
        theUseCaseRule, 
        theRuleName,
        theUseCaseAssessment,
        theMustCollect          =False,
        thePredicateOverrides   ={},
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):  
        """Assess the rule: result is a boolean meaning that the rule has passed.
        
        Dispatch to algorithms for specific modes of tool assessment:
            ForAll, Filter, NoneOrAtLeastOne, NoneOrAll 
         
        """
            
        if not theUseCaseName or not theUseCaseRule or not theUseCaseAssessment:
            return None
    
            
        unUseCaseRuleMode  = theUseCaseRule.get( 'mode',  cUseCaseRuleMode_ForAll)
        if not ( unUseCaseRuleMode in cUseCaseRuleModes):
            return None
        
        unRuleModeHandler = TRAElemento_Permissions_UseCases.gUseCaseRuleModeHandlers.get( unUseCaseRuleMode, None)
        if not unRuleModeHandler:
            return None
                     
        
        return unRuleModeHandler(
            self,
            theUseCaseName,
            theUseCaseRule, 
            theRuleName,
            theUseCaseAssessment,
            theMustCollect          = theMustCollect,
            thePredicateOverrides   = thePredicateOverrides,
            thePermissionsCache     = thePermissionsCache, 
            theRolesCache           = theRolesCache, 
            theParentExecutionRecord= theParentExecutionRecord)
         
                    
            


    
    
    
 
    security.declarePrivate( 'fUseCaseRuleAssessment_ForAll')
    def fUseCaseRuleAssessment_ForAll(self, 
        theUseCaseName,
        theUseCaseRule, 
        theRuleName,
        theUseCaseAssessment,
        theMustCollect          =False,
        thePredicateOverrides   = {},
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):  
        """Assess the rule: shall pass if all the objects retrieved for assessement match all the rule constraints.
                 
        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fUseCaseRuleAssessment_ForAll', theParentExecutionRecord, False, None, 'rule=%s' % ( theUseCaseRule.get( 'title', theRuleName or 'unknown')))
                
        unosAcceptedInitialObjects  = []
        unosAcceptedFinalObjects    = []
        unosRejectedInitialObjects  = []
        unosRejectedFinalObjects    = []
        unUseCaseRuleAssessment     = {}

        try:
            
            unUseCaseRuleAssessment = self.fNewVoidUseCaseRuleAssessment()
            unUseCaseRuleAssessment[ 'use_case_name'] = theUseCaseName
            unUseCaseRuleAssessment[ 'rule'] = theUseCaseRule

            
            try:
                    
                if not theUseCaseRule or not theRuleName or not theUseCaseAssessment:
                    unUseCaseRuleAssessment[ 'status']     = 'fUseCaseRuleAssessment_Missing_parameters'
                    return unUseCaseRuleAssessment
                
                
                aPath = theUseCaseRule.get( 'path', '')
                if not  aPath:
                    # ##################################################################
                    """Because the rule specified no path,
                    build a path to retrieve the object against which to the assess the rule, 
                    that shall be the object or collection of objects bound with the default binding name.
                    
                    """
                    aPath = [ cBoundObject, ]
                    
                unUseCaseRuleAssessment[ 'path'] = aPath
                
                
                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)
                    

                unosRejectedObjects = theUseCaseAssessment.get( 'rejected_objects', [])
                
                unosTypes       = theUseCaseRule.get( 'types', [])
                unasPerms       = theUseCaseRule.get( 'perms', [])
                unosRoles       = theUseCaseRule.get( 'roles', [])
                unosPredicates  = theUseCaseRule.get( 'pred',  [])
                
                unosRetrievedObjects = self.fUseCaseRuleAssessment_ObjectsRetrieval( 
                    theUseCaseAssessment     = theUseCaseAssessment,
                    theUseCaseRule          = theUseCaseRule,
                    theUseCaseRuleAssessment= unUseCaseRuleAssessment,
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord)
                
                if unosRetrievedObjects == None:
                    """Exit not passing the rule because there was an error trying to retrieve objects to assess. 
                    If no object found or matching root types, the result is an empty list.
                    
                    """
                    unUseCaseRuleAssessment[ 'status']     = cRuleAssessment_Failed
                    return unUseCaseRuleAssessment 
                
                
                
                # ##################################################################
                """Reject the objects rejected previously in the use case assessment.
                
                Note that only rules of special modes may reject objects without 
                making fail the use case assessment, and therefore allow the case
                of retrieving for assessment in the initial step of a rule, 
                objects rejected by previous rules: normal rules will fail and stop us case assessment.
                
                """
                unosRejectedObjects = theUseCaseAssessment.get( 'rejected_objects', set())
                unosNotPreviouslyRejectedObjects = [ unObject for unObject in unosRetrievedObjects if not ( unObject in unosRejectedObjects) ]
            

                
                # ##################################################################
                """Shall collect the objects that match all constraints, or fail in any.
                
                If the rule's path has just the initial binding lookup name, then initial and final object is the same.
                If the rule's path has more steps, then for each initial object there may be more than one object to assess.
                
                """
                unosAcceptedInitialObjects  = unUseCaseRuleAssessment.get( 'accepted_initial_objects', [])
                unosAcceptedFinalObjects    = unUseCaseRuleAssessment.get( 'accepted_final_objects', [])
                unosRejectedInitialObjects  = unUseCaseRuleAssessment.get( 'rejected_initial_objects', [])
                unosRejectedFinalObjects    = unUseCaseRuleAssessment.get( 'rejected_final_objects', [])
                
                
                # ##################################################################
                """Assess rule constraints against each retrieved, non previously rejected object .
                
                """
                
                for unInitialObject, unObjectToCheck in unosNotPreviouslyRejectedObjects:

                    unObjectPassed  = True
                    
                    if ( unObjectToCheck in unosRejectedObjects):
                        unObjectPassed  = False
                        unNonPassingReason = cRuleAssessment_Failure_ObjectAlreadyRejected
                     
                    if unObjectPassed and unosTypes and ( not unObjectToCheck.__class__.__name__ in unosTypes):
                        unObjectPassed  = False
                        unNonPassingReason = cRuleAssessment_Failure_NotOfTargetType
                            
                    if unObjectPassed and unosRoles and not self.fCheckElementRoles( unObjectToCheck, unosRoles, unRolesCache):
                        unObjectPassed  = False
                        unNonPassingReason = cRuleAssessment_Failure_UserWithoutRole
                             
                    if unObjectPassed and unasPerms and not self.fCheckElementPermission( unObjectToCheck, unasPerms, unPermissionsCache):
                        unObjectPassed  = False
                        unNonPassingReason = cRuleAssessment_Failure_UserWithoutPermissions
                        
                    if unosPredicates:
                        unPassedAllPredicates = True
                        
                        unaObjectToCheckUID = unObjectToCheck.UID()

                        for aPredicateSpec in unosPredicates:
                            
                            aPredicate = aPredicateSpec
                            unNegatePredicateResult = False
                            
                            if aPredicateSpec.startswith( 'not:'):
                                unNegatePredicateResult = True
                                aPredicate = aPredicateSpec[ len( 'not:'):].strip()
                                
                            
                            unPredicateResult = None
                            
                            if thePredicateOverrides and thePredicateOverrides.has_key( unaObjectToCheckUID) and thePredicateOverrides.get( unaObjectToCheckUID, {}).has_key( aPredicate):

                                unPredicateResult = thePredicateOverrides.get( unaObjectToCheckUID, {}).get( aPredicate, False)
                                    
                            else:
                                unMethod = None
                                try:
                                    unMethod = unObjectToCheck[ aPredicate]
                                except:
                                    None
                                if unMethod:
                                    try:
                                        unPredicateResult =  unMethod()   
                                    except:
                                        None
                            if not unPredicateResult:
                                if unNegatePredicateResult:
                                    continue
                                else:
                                    unPassedAllPredicates = False
                                    break
                            else:
                                if unNegatePredicateResult:
                                    unPassedAllPredicates = False
                                    break
                                else:
                                    continue
                        
                        if not unPassedAllPredicates:       
                            unObjectPassed  = False
                            unNonPassingReason = cRuleAssessment_Failure_Predicate
                                                                    
 
                            
                    if not unObjectPassed:
                        unosRejectedObjects.add( unObjectToCheck)                                
                        unUseCaseRuleAssessment[ 'status']     = unNonPassingReason or 'fUseCaseRuleAssessment_ObjectNotPassed'
            
                        if theMustCollect:
                            if not ( unInitialObject in unosRejectedInitialObjects):
                                unosRejectedInitialObjects.append( unInitialObject)                            
                            if not ( unInitialObject in unosRejectedFinalObjects):
                                unosRejectedFinalObjects.append(   unObjectToCheck)                            
                                
                        return unUseCaseRuleAssessment   
                    
                    else:
                        if not ( unObjectPassed in unosRejectedObjects):
                            if theMustCollect:
                                if not ( unInitialObject in unosAcceptedInitialObjects):
                                    unosAcceptedInitialObjects.append( unInitialObject)                            
                                if not ( unInitialObject in unosAcceptedFinalObjects):
                                    unosAcceptedFinalObjects.append(   unObjectToCheck)                            
                            
                
                unUseCaseRuleAssessment[ 'success'] = True
                unUseCaseRuleAssessment[ 'status']  = cRuleAssessment_Passed
                 
                return unUseCaseRuleAssessment
                    
            except:
                    
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fUseCaseRuleAssessment_ForAll\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   
                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                    
                return unUseCaseRuleAssessment                 
                
                
        finally:       
            unExecutionRecord and unExecutionRecord.addExtraInfo( (( unUseCaseRuleAssessment and unUseCaseRuleAssessment.get( 'success', False)) and 'passed') or 'failed')
            unExecutionRecord and unExecutionRecord.addExtraInfo( '[objs +%d -%d // +%d -%d ]' % (
                len( unosAcceptedInitialObjects), len( unosRejectedInitialObjects), len( unosAcceptedFinalObjects), len( unosRejectedFinalObjects),   
            ))
            unExecutionRecord and unExecutionRecord.pEndExecution()
    
                
          
            
            
            
            

            
            
          
            
                
            
            
            
            

    
 
    security.declarePrivate( 'fUseCaseRuleAssessment_Filter')
    def fUseCaseRuleAssessment_Filter(self, 
        theUseCaseName,
        theUseCaseRule, 
        theRuleName,
        theUseCaseAssessment,
        theMustCollect          =False,
        thePredicateOverrides   = {},
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):  
        """Assess the rule: shall pass whenever there is not an execution error and assess all objects. It is always considered set to collect to return the collection of objects that pass the rule. 
                 
        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fUseCaseRuleAssessment_Filter', theParentExecutionRecord, False, None, 'theRuleName=%s' % (theRuleName or 'unknown'))
        
        unosAcceptedInitialObjects  = []
        unosAcceptedFinalObjects    = []
        unosRejectedInitialObjects  = []
        unosRejectedFinalObjects    = []
        unUseCaseRuleAssessment     = {}
        
        try:
            
            unUseCaseRuleAssessment = self.fNewVoidUseCaseRuleAssessment()
            unUseCaseRuleAssessment[ 'use_case_name'] = theUseCaseName
            unUseCaseRuleAssessment[ 'rule'] = theUseCaseRule
            
            try:
                    
                if not theUseCaseRule or not theRuleName or not theUseCaseAssessment:
                    unUseCaseRuleAssessment[ 'status']     = 'fUseCaseRuleAssessment_Missing_parameters'
                    return unUseCaseRuleAssessment
                
                
                aPath = theUseCaseRule.get( 'path', '')
                if not  aPath:
                    # ##################################################################
                    """Because the rule specified no path,
                    build a path to retrieve the object against which to the assess the rule, 
                    that shall be the object or collection of objects bound with the default binding name.
                    
                    """
                    aPath = [ cBoundObject, ]
                    
                unUseCaseRuleAssessment[ 'path'] = aPath
                
                
                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)
                    
                unosRejectedObjects = theUseCaseAssessment.get( 'rejected_objects', [])
                
                unosTypes       = theUseCaseRule.get( 'types', [])
                unasPerms       = theUseCaseRule.get( 'perms', [])
                unosRoles       = theUseCaseRule.get( 'roles', [])
                unosPredicates  = theUseCaseRule.get( 'pred',  [])
                
                unosRetrievedObjects = self.fUseCaseRuleAssessment_ObjectsRetrieval( 
                    theUseCaseAssessment     = theUseCaseAssessment,
                    theUseCaseRule          = theUseCaseRule,
                    theUseCaseRuleAssessment= unUseCaseRuleAssessment,
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord)
                
                if unosRetrievedObjects == None:
                    """Exit not passing the rule because there was an error trying to retrieve objects to assess. 
                    If no object found or matching root types, the result is an empty list.
                    
                    """
                    unUseCaseRuleAssessment[ 'status']     = cRuleAssessment_Failed
                    return unUseCaseRuleAssessment
                
                
                # ##################################################################
                """Reject the objects rejected previously in the use case assessment.
                
                Note that only rules of special modes may reject objects without 
                making fail the use case assessment, and therefore allow the case
                of retrieving for assessment in the initial step of a rule, 
                objects rejected by previous rules: normal rules will fail and stop us case assessment.
                
                """
                unosRejectedObjects = theUseCaseAssessment.get( 'rejected_objects', set())
                unosNotPreviouslyRejectedObjects = [ unObject for unObject in unosRetrievedObjects if unObject not in unosRejectedObjects]
            

                
                # ##################################################################
                """Shall collect the objects that match all constraints, or fail in any.
                
                If the rule's path has just the initial binding lookup name, then initial and final object is the same.
                If the rule's path has more steps, then for each initial object there may be more than one object to assess.
                
                """
                unosAcceptedInitialObjects  = unUseCaseRuleAssessment.get( 'accepted_initial_objects', [])
                unosAcceptedFinalObjects    = unUseCaseRuleAssessment.get( 'accepted_final_objects', [])
                unosRejectedInitialObjects  = unUseCaseRuleAssessment.get( 'rejected_initial_objects', [])
                unosRejectedFinalObjects    = unUseCaseRuleAssessment.get( 'rejected_initial_objects', [])
                
                
                # ##################################################################
                """Assess rule constraints against each retrieved, non previously rejected object .
                
                """
                for unInitialObject, unObjectToCheck in unosNotPreviouslyRejectedObjects:

                    unObjectPassed  = True
                    
                    if ( unObjectToCheck in unosRejectedObjects):
                        unObjectPassed  = False
                        unNonPassingReason = cRuleAssessment_Failure_ObjectAlreadyRejected
                     
                    if unObjectPassed and unosTypes and ( not unObjectToCheck.__class__.__name__ in unosTypes):
                        unObjectPassed  = False
                        unNonPassingReason = cRuleAssessment_Failure_NotOfTargetType
                            
                    if unObjectPassed and unosRoles and not self.fCheckElementRoles( unObjectToCheck, unosRoles, unRolesCache):
                        unObjectPassed  = False
                        unNonPassingReason = cRuleAssessment_Failure_UserWithoutRole
                             
                    if unObjectPassed and unasPerms and not self.fCheckElementPermission( unObjectToCheck, unasPerms, unPermissionsCache):
                        unObjectPassed  = False
                        unNonPassingReason = cRuleAssessment_Failure_UserWithoutPermissions
 
                    if unosPredicates:
                        unPassedAllPredicates = True

                        unaObjectToCheckUID = unObjectToCheck.UID()

                        for aPredicate in unosPredicates:
                            
                            unPredicateResult = None
                            
                            if thePredicateOverrides and thePredicateOverrides.has_key( unaObjectToCheckUID):
                                unPredicateValues = thePredicateOverrides.get( unaObjectToCheckUID, False)
                                if unPredicateValues:
                                    unPredicateResult = unPredicateValues.get( aPredicate, False)
                                    
                            else:
                                unMethod = None
                                try:
                                    unMethod = unObjectToCheck[ aPredicate]
                                except:
                                    None
                                if unMethod:
                                    try:
                                        unPredicateResult =  unMethod()   
                                    except:
                                        None
                            if not unPredicateResult:
                                unPassedAllPredicates = False
                                break
                        
                        if not unPassedAllPredicates:       
                            unObjectPassed  = False
                            unNonPassingReason = cRuleAssessment_Failure_Predicate
                            
                    if not unObjectPassed:
                        unosRejectedObjects.add( unObjectToCheck)                                
            
                        if theMustCollect:
                            if not ( unInitialObject in unosRejectedInitialObjects):
                                unosRejectedInitialObjects.append( unInitialObject)                            
                            if not ( unInitialObject in unosRejectedFinalObjects):
                                unosRejectedFinalObjects.append(   unObjectToCheck)                            
                    
                    else:
                        if not ( unObjectPassed in unosRejectedObjects):
                            if not ( unInitialObject in unosAcceptedInitialObjects):
                                unosAcceptedInitialObjects.append( unInitialObject)                            
                            if not ( unObjectToCheck in unosAcceptedFinalObjects):
                                unosAcceptedFinalObjects.append(   unObjectToCheck)                            
                            
                
                unUseCaseRuleAssessment[ 'success'] = True
                unUseCaseRuleAssessment[ 'status']     = cRuleAssessment_Passed
                 
                return unUseCaseRuleAssessment
                    
            except:
                    
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fUseCaseRuleAssessment_Filter\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   
                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                    
                return unUseCaseRuleAssessment                 
                
                
        finally:       
            unExecutionRecord and unExecutionRecord.addExtraInfo( '[objs +%d -%d // +%d -%d ]' % (
                len( unosAcceptedInitialObjects), len( unosRejectedInitialObjects), len( unosAcceptedFinalObjects), len( unosRejectedFinalObjects),   
            ))
                                            
            unExecutionRecord and unExecutionRecord.pEndExecution()
    
                
          
            
            
            
            

            
            
          
    
 
    security.declarePrivate( 'fUseCaseRuleAssessment_EmptyOrAll')
    def fUseCaseRuleAssessment_EmptyOrAll(self, 
        theUseCaseName,
        theUseCaseRule, 
        theRuleName,
        theUseCaseAssessment,
        theMustCollect          =False,
        thePredicateOverrides   = {},
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):  
        """Assess the rule: shall pass if there is no object to test, or all of them match all the rule constraints. 
                 
        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fUseCaseRuleAssessment_EmptyOrAll', theParentExecutionRecord, False, None, 'theRuleName=%s' % (theRuleName or 'unknown')) 
        
        unosAcceptedInitialObjects  = []
        unosAcceptedFinalObjects    = []
        unosRejectedInitialObjects  = []
        unosRejectedFinalObjects    = []
        unUseCaseRuleAssessment     = {}
        
        try:
            
            unUseCaseRuleAssessment = self.fNewVoidUseCaseRuleAssessment()
            unUseCaseRuleAssessment[ 'use_case_name'] = theUseCaseName
            unUseCaseRuleAssessment[ 'rule'] = theUseCaseRule
            
            try:
                    
                if not theUseCaseRule or not theRuleName or not theUseCaseAssessment:
                    unUseCaseRuleAssessment[ 'status']     = 'fUseCaseRuleAssessment_Missing_parameters'
                    return unUseCaseRuleAssessment
                
                
                aPath = theUseCaseRule.get( 'path', '')
                if not  aPath:
                    # ##################################################################
                    """Because the rule specified no path,
                    build a path to retrieve the object against which to the assess the rule, 
                    that shall be the object or collection of objects bound with the default binding name.
                    
                    """
                    aPath = [ cBoundObject, ]
                    
                unUseCaseRuleAssessment[ 'path'] = aPath
                
                
                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)
                    
                unosRejectedObjects = theUseCaseAssessment.get( 'rejected_objects', [])
                
                unosTypes       = theUseCaseRule.get( 'types', [])
                unasPerms       = theUseCaseRule.get( 'perms', [])
                unosRoles       = theUseCaseRule.get( 'roles', [])
                unosPredicates  = theUseCaseRule.get( 'pred',  [])
                
                unosRetrievedObjects = self.fUseCaseRuleAssessment_ObjectsRetrieval(
                    theUseCaseAssessment     = theUseCaseAssessment,
                    theUseCaseRule          = theUseCaseRule,
                    theUseCaseRuleAssessment= unUseCaseRuleAssessment,
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord)
                
                if unosRetrievedObjects == None:
                    """Exit not passing the rule because there was an error trying to retrieve objects to assess. 
                    If no object found or matching root types, the result is an empty list.
                    
                    """
                    unUseCaseRuleAssessment[ 'status']     = cRuleAssessment_Failed
                    return unUseCaseRuleAssessment
                
                 # ##################################################################
                """Reject the objects rejected previously in the use case assessment.
                
                Note that only rules of special modes may reject objects without 
                making fail the use case assessment, and therefore allow the case
                of retrieving for assessment in the initial step of a rule, 
                objects rejected by previous rules: normal rules will fail and stop us case assessment.
                
                """
                unosRejectedObjects = theUseCaseAssessment.get( 'rejected_objects', set())
                unosNotPreviouslyRejectedObjects = [ unObject for unObject in unosRetrievedObjects if unObject not in unosRejectedObjects]
            
                
                if not unosRetrievedObjects:
                    """Exit passing the rule because there was not retrieved objects to assess. 
                    
                    """
                    unUseCaseRuleAssessment[ 'success'] = True
                    unUseCaseRuleAssessment[ 'status']  = cRuleAssessment_Passed
                    return unUseCaseRuleAssessment
                
                

                
                # ##################################################################
                """Shall collect the objects that match all constraints, or fail in any.
                
                If the rule's path has just the initial binding lookup name, then initial and final object is the same.
                If the rule's path has more steps, then for each initial object there may be more than one object to assess.
                
                """
                unosAcceptedInitialObjects  = unUseCaseRuleAssessment.get( 'accepted_initial_objects', [])
                unosAcceptedFinalObjects    = unUseCaseRuleAssessment.get( 'accepted_final_objects', [])
                unosRejectedInitialObjects  = unUseCaseRuleAssessment.get( 'rejected_initial_objects', [])
                unosRejectedFinalObjects    = unUseCaseRuleAssessment.get( 'rejected_initial_objects', [])
                
                
                # ##################################################################
                """Assess rule constraints against each retrieved, non previously rejected object .
                
                """
                for unInitialObject, unObjectToCheck in unosNotPreviouslyRejectedObjects:

                    unObjectPassed  = True
                    
                    if ( unObjectToCheck in unosRejectedObjects):
                        unObjectPassed  = False
                        unNonPassingReason = cRuleAssessment_Failure_ObjectAlreadyRejected
                     
                    if unObjectPassed and unosTypes and ( not unObjectToCheck.__class__.__name__ in unosTypes):
                        unObjectPassed  = False
                        unNonPassingReason = cRuleAssessment_Failure_NotOfTargetType
                            
                    if unObjectPassed and unosRoles and not self.fCheckElementRoles( unObjectToCheck, unosRoles, unRolesCache):
                        unObjectPassed  = False
                        unNonPassingReason = cRuleAssessment_Failure_UserWithoutRole
                             
                    if unObjectPassed and unasPerms and not self.fCheckElementPermission( unObjectToCheck, unasPerms, unPermissionsCache):
                        unObjectPassed  = False
                        unNonPassingReason = cRuleAssessment_Failure_UserWithoutPermissions
 
                    if unosPredicates:
                        unPassedAllPredicates = True

                        unaObjectToCheckUID = unObjectToCheck.UID()

                        for aPredicate in unosPredicates:
                            
                            unPredicateResult = None
                            
                            if thePredicateOverrides and thePredicateOverrides.has_key( unaObjectToCheckUID):
                                unPredicateValues = thePredicateOverrides.get( unaObjectToCheckUID, False)
                                if unPredicateValues:
                                    unPredicateResult = unPredicateValues.get( aPredicate, False)
                                    
                            else:
                                unMethod = None
                                try:
                                    unMethod = unObjectToCheck[ aPredicate]
                                except:
                                    None
                                if unMethod:
                                    try:
                                        unPredicateResult =  unMethod()   
                                    except:
                                        None
                            if not unPredicateResult:
                                unPassedAllPredicates = False
                                break

                        
                        if not unPassedAllPredicates:       
                            unObjectPassed  = False
                            unNonPassingReason = cRuleAssessment_Failure_Predicate
                            
                    if not unObjectPassed:
                        unosRejectedObjects.add( unObjectToCheck)                                
            
                        unUseCaseRuleAssessment[ 'status']     = unNonPassingReason or 'fUseCaseRuleAssessment_ObjectNotPassed'
            
                        if theMustCollect:
                            if not ( unInitialObject in unosRejectedInitialObjects):
                                unosRejectedInitialObjects.append( unInitialObject)                            
                            if not ( unInitialObject in unosRejectedFinalObjects):
                                unosRejectedFinalObjects.append(   unObjectToCheck)                            
                                
                        return unUseCaseRuleAssessment   
                        
                    
                    else:
                        if unObjectPassed in unosRejectedObjects:
                            unUseCaseRuleAssessment[ 'status']     = unNonPassingReason or 'fUseCaseRuleAssessment_ObjectNotPassed'
                
                            if theMustCollect:
                                unosRejectedInitialObjects.append( unInitialObject)                            
                                unosRejectedFinalObjects.append(   unObjectToCheck)                            
                                    
                            return unUseCaseRuleAssessment   
                            
                        else:
                            if theMustCollect:
                                unosAcceptedInitialObjects.append( unInitialObject)                            
                                unosAcceptedFinalObjects.append(   unObjectToCheck)                            
                            
                
                unUseCaseRuleAssessment[ 'success'] = True
                unUseCaseRuleAssessment[ 'status']  = cRuleAssessment_Passed
                 
                return unUseCaseRuleAssessment
                    
            except:
                    
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fUseCaseRuleAssessment_EmptyOrAll\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   
                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                    
                return unUseCaseRuleAssessment                 
                
                
        finally:       
            unExecutionRecord and unExecutionRecord.addExtraInfo( (( unUseCaseRuleAssessment and unUseCaseRuleAssessment.get( 'success', False)) and 'passed') or 'failed')
            unExecutionRecord and unExecutionRecord.addExtraInfo( '[objs +%d -%d // +%d -%d ]' % (
                len( unosAcceptedInitialObjects), len( unosRejectedInitialObjects), len( unosAcceptedFinalObjects), len( unosRejectedFinalObjects),   
            ))
            unExecutionRecord and unExecutionRecord.pEndExecution()
    
                
          
            
            
             
                
            
                
          
            
            
            
            

            
            
          
    
 
    security.declarePrivate( 'fUseCaseRuleAssessment_EmptyOrAny')
    def fUseCaseRuleAssessment_EmptyOrAny(self, 
        theUseCaseName,
        theUseCaseRule, 
        theRuleName,
        theUseCaseAssessment,
        theMustCollect          =False,
        thePredicateOverrides   = {},
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):  
        """Assess the rule: shall pass if there is no object to test, or any of them match all the rule constraints. 
                 
        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fUseCaseRuleAssessment_EmptyOrAny', theParentExecutionRecord, False, None, 'theRuleName=%s' % (theRuleName or 'unknown')) 
        
        unosAcceptedInitialObjects  = []
        unosAcceptedFinalObjects    = []
        unosRejectedInitialObjects  = []
        unosRejectedFinalObjects    = []
        unUseCaseRuleAssessment     = {}
         
        try:
            
            unUseCaseRuleAssessment = self.fNewVoidUseCaseRuleAssessment()
            unUseCaseRuleAssessment[ 'use_case_name'] = theUseCaseName
            unUseCaseRuleAssessment[ 'rule'] = theUseCaseRule
            
            try:
                    
                if not theUseCaseRule or not theRuleName or not theUseCaseAssessment:
                    unUseCaseRuleAssessment[ 'status']     = 'fUseCaseRuleAssessment_Missing_parameters'
                    return unUseCaseRuleAssessment
                
                
                aPath = theUseCaseRule.get( 'path', '')
                if not  aPath:
                    # ##################################################################
                    """Because the rule specified no path,
                    build a path to retrieve the object against which to the assess the rule, 
                    that shall be the object or collection of objects bound with the default binding name.
                    
                    """
                    aPath = [ cBoundObject, ]
                    
                unUseCaseRuleAssessment[ 'path'] = aPath
                
                
                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)
                    
                unosRejectedObjects = theUseCaseAssessment.get( 'rejected_objects', [])
                
                unosTypes       = theUseCaseRule.get( 'types', [])
                unasPerms       = theUseCaseRule.get( 'perms', [])
                unosRoles       = theUseCaseRule.get( 'roles', [])
                unosPredicates  = theUseCaseRule.get( 'pred',  [])
                
                unosRetrievedObjects = self.fUseCaseRuleAssessment_ObjectsRetrieval( 
                    theUseCaseAssessment    = theUseCaseAssessment,
                    theUseCaseRule          = theUseCaseRule,
                    theUseCaseRuleAssessment= unUseCaseRuleAssessment,
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord)
                
                if unosRetrievedObjects == None:
                    """Exit not passing the rule because there was an error trying to retrieve objects to assess. 
                    If no object found or matching root types, the result is an empty list.
                    
                    """
                    unUseCaseRuleAssessment[ 'status']     = cRuleAssessment_Failed
                    return unUseCaseRuleAssessment
                
                 # ##################################################################
                """Reject the objects rejected previously in the use case assessment.
                
                Note that only rules of special modes may reject objects without 
                making fail the use case assessment, and therefore allow the case
                of retrieving for assessment in the initial step of a rule, 
                objects rejected by previous rules: normal rules will fail and stop us case assessment.
                
                """
                unosRejectedObjects = theUseCaseAssessment.get( 'rejected_objects', set())
                unosNotPreviouslyRejectedObjects = [ unObject for unObject in unosRetrievedObjects if unObject not in unosRejectedObjects]
            
                
                if not unosRetrievedObjects:
                    """Exit passing the rule because there was not retrieved objects to assess. 
                    
                    """
                    unUseCaseRuleAssessment[ 'success'] = True
                    unUseCaseRuleAssessment[ 'status']  = cRuleAssessment_Passed
                    return unUseCaseRuleAssessment
                
                

                
                # ##################################################################
                """Shall collect the objects that match all constraints, or fail in any.
                
                If the rule's path has just the initial binding lookup name, then initial and final object is the same.
                If the rule's path has more steps, then for each initial object there may be more than one object to assess.
                
                """
                unosAcceptedInitialObjects  = unUseCaseRuleAssessment.get( 'accepted_initial_objects', [])
                unosAcceptedFinalObjects    = unUseCaseRuleAssessment.get( 'accepted_final_objects', [])
                unosRejectedInitialObjects  = unUseCaseRuleAssessment.get( 'rejected_initial_objects', [])
                unosRejectedFinalObjects    = unUseCaseRuleAssessment.get( 'rejected_final_objects', [])
                
                
                # ##################################################################
                """Assess rule constraints against each retrieved, non previously rejected object .
                
                """
                for unInitialObject, unObjectToCheck in unosNotPreviouslyRejectedObjects:

                    unObjectPassed  = True
                    
                    if ( unObjectToCheck in unosRejectedObjects):
                        unObjectPassed  = False
                        unNonPassingReason = cRuleAssessment_Failure_ObjectAlreadyRejected
                     
                    if unObjectPassed and unosTypes and ( not unObjectToCheck.__class__.__name__ in unosTypes):
                        unObjectPassed  = False
                        unNonPassingReason = cRuleAssessment_Failure_NotOfTargetType
                            
                    if unObjectPassed and unosRoles and not self.fCheckElementRoles( unObjectToCheck, unosRoles, unRolesCache):
                        unObjectPassed  = False
                        unNonPassingReason = cRuleAssessment_Failure_UserWithoutRole
                             
                    if unObjectPassed and unasPerms and not self.fCheckElementPermission( unObjectToCheck, unasPerms, unPermissionsCache):
                        unObjectPassed  = False
                        unNonPassingReason = cRuleAssessment_Failure_UserWithoutPermissions
 
                    if unosPredicates:
                        unPassedAllPredicates = True

                        unaObjectToCheckUID = unObjectToCheck.UID()

                        for aPredicate in unosPredicates:
                            
                            unPredicateResult = None
                            
                            if thePredicateOverrides and thePredicateOverrides.has_key( unaObjectToCheckUID):
                                unPredicateValues = thePredicateOverrides.get( unaObjectToCheckUID, False)
                                if unPredicateValues:
                                    unPredicateResult = unPredicateValues.get( aPredicate, False)
                                    
                            else:
                                unMethod = None
                                try:
                                    unMethod = unObjectToCheck[ aPredicate]
                                except:
                                    None
                                if unMethod:
                                    try:
                                        unPredicateResult =  unMethod()   
                                    except:
                                        None
                            if not unPredicateResult:
                                unPassedAllPredicates = False
                                break

                        
                        if not unPassedAllPredicates:       
                            unObjectPassed  = False
                            unNonPassingReason = cRuleAssessment_Failure_Predicate
                            
                    if not unObjectPassed:
                        unosRejectedObjects.add( unObjectToCheck)                                
            
                        if theMustCollect:
                            if not ( unInitialObject in unosRejectedInitialObjects):
                                unosRejectedInitialObjects.append( unInitialObject)                            
                            if not ( unInitialObject in unosRejectedFinalObjects):
                                unosRejectedFinalObjects.append(   unObjectToCheck)                            
                   
                    else:
                        if theMustCollect:
                            if not( unObjectPassed in unosRejectedObjects):
                                if not( unInitialObject in unosAcceptedInitialObjects):
                                    unosAcceptedInitialObjects.append( unInitialObject)                            
                                if not( unObjectToCheck in unosAcceptedFinalObjects):
                                    unosAcceptedFinalObjects.append(   unObjectToCheck)     
                            
                            
                            unUseCaseRuleAssessment[ 'success'] = True
                            unUseCaseRuleAssessment[ 'status']  = cRuleAssessment_Passed
                             
                            return unUseCaseRuleAssessment
                            
                
                unUseCaseRuleAssessment[ 'status']  = cRuleAssessment_NotPassed
                 
                return unUseCaseRuleAssessment
                    
            except:
                    
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fUseCaseRuleAssessment_EmptyOrAny\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   
                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                    
                return unUseCaseRuleAssessment                 
                
                
        finally:       
            unExecutionRecord and unExecutionRecord.addExtraInfo( (( unUseCaseRuleAssessment and unUseCaseRuleAssessment.get( 'success', False)) and 'passed') or 'failed')
            unExecutionRecord and unExecutionRecord.addExtraInfo( '[objs +%d -%d // +%d -%d ]' % (
                len( unosAcceptedInitialObjects), len( unosRejectedInitialObjects), len( unosAcceptedFinalObjects), len( unosRejectedFinalObjects),   
            ))
            
            unExecutionRecord and unExecutionRecord.pEndExecution()
    
                
            
                        
            
            
            
            
            
            
            
            
                
            
            
       
        
        
    
 
    security.declarePrivate( 'fUseCaseRuleAssessment_ObjectsRetrieval')
    def fUseCaseRuleAssessment_ObjectsRetrieval(self, 
        theUseCaseAssessment    =None,
        theUseCaseRule          =None,
        theUseCaseRuleAssessment=None,
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):  
        """Retrieve  all the objects against wich to assess the rule by matching the rule constraints.
        
        Returns a possibly empty list of objects. On error returns None.
        
        """
        unExecutionRecord = self.fStartExecution( 'method',  'fUseCaseRuleAssessment_ObjectsRetrieval', theParentExecutionRecord, False) 
        
        try:
            
            unLastStep    = ''
            unLastObject  = None

            try:
                if not theUseCaseAssessment or not theUseCaseRule:
                    return None

                someElementsBindings = theUseCaseAssessment.get( 'elements_bindings',  {})   
                if not someElementsBindings:
                    return None

                aPath = theUseCaseRuleAssessment.get( 'path', '')
                if not  aPath:
                    # ##################################################################
                    """Because the rule specified no path,
                    build a path to retrieve the object against which to the assess the rule, 
                    that shall be the object or collection of objects bound with the default binding name.
                    
                    """
                    aPath = [ cBoundObject, ]
                    
                
                # ##################################################################
                """Get, if any, the types of objects to be assessed by this rule.
                                
                """
                someRootTypes = theUseCaseRule.get( 'root', [])
                
                 # ##################################################################
                """Get the objects rejected previously in the use case assessment.
                
                Note that only rules of special modes may reject objects without 
                making fail the use case assessment, and therefore allow the case
                of retrieving for assessment in the initial step of a rule, 
                objects rejected by previous rules: normal rules will fail and stop us case assessment.
                
                """
                unosRejectedObjects = theUseCaseAssessment.get( 'rejected_objects', set())
                
                    
                # ##################################################################
                """Retrieve the objects against which to the assess the rule, by traversing the path specified by the rule,
                
                """
                unosInitialObjects  = [ ]
                unNumSteps = len( aPath)
                unosObjectsPassingLastStep = [ ]
                
                
                for unPathStepIndex in range( 0, unNumSteps):
                    
                    unLastObject  = None
                    
                    unPathStep = aPath[ unPathStepIndex]
                    unLastStep = unPathStep
    
                    if unPathStepIndex == 0:
                        # ##################################################################
                        """Because this is the first path traversal step, 
                        resolve the first objects in the path traversal by looking up in theElementsBindings.
                        
                        """
                        unInitialObject = someElementsBindings.get( unPathStep, None)
                        if ( not unInitialObject) and not ( unInitialObject.__class__.__name__ == 'TRAColeccionCadenas'):
                            return None
                            
                        if unInitialObject.__class__.__name__ in [ 'list', 'tuple', 'set', ]:
                            unosInitialObjects = unInitialObject
                        else:
                            # ##################################################################
                            """Wrap as a list if not already, because the rule assessment mechanism operates on collections of objects
                            
                            """
                            unosInitialObjects = [ unInitialObject, ]
    
                                    
                        unosObjectsToConsiderNextStep = []
                        # ##################################################################
                        """If the rule specifies a roots constraint, 
                        then filter which of the objects resolved as initial for the path traversal
                        match one of the types specified as possible roots for the rule.
                        Discard the objects that may have been discarded in a previous rule.
                        
                        """
                        
                        for unInitialObject in unosInitialObjects:
                            unObjectClassName = unInitialObject.__class__.__name__
                            if not someRootTypes or ( unObjectClassName in someRootTypes):
                                if not ( unInitialObject in unosRejectedObjects):
                                    unosObjectsToConsiderNextStep.append( ( unInitialObject, unInitialObject, ))
                                    
                                    
                                      
                    else:
                       # ##################################################################
                        """Process next step traversing from all obtained in previous step.
                        
                        """
                        unosObjectsToConsiderNextStep = [] 
                        
                        for unInitialObject, unObject in unosObjectsPassingLastStep:
                            unLastObject = unObject
                            
                            unMethod = None
                            try:
                                unMethod = unObject[ unPathStep]
                            except:
                                None
                            if unMethod:
                                unNextObject = None
                                try:
                                    unNextObject =  unMethod()   
                                except:
                                    None
                                if not ( unNextObject == None):
                                    if not ( unNextObject.__class__.__name__ in [ 'list', 'tuple', 'set', ]):
                                        unosObjectsRetrievedThisObject = [ ( unInitialObject, unNextObject, ), ]
                                    else:
                                        unosObjectsRetrievedThisObject = [ ( unInitialObject,  unOtherObject, ) for unOtherObject in unNextObject]
                                    unosObjectsToConsiderNextStep.extend( unosObjectsRetrievedThisObject)
                    
                        unLastObject = None

                    unosObjectsPassingLastStep = unosObjectsToConsiderNextStep             
                
                unLastStep = ''
                if not unosObjectsPassingLastStep:
                    return []
                
                return unosObjectsPassingLastStep

            except:
                    
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fUseCaseRuleAssessment_ObjectsRetrieval %s%s\n'  % (
                    ( unLastStep and ( 'Last step: %s' % unLastStep)) or '',
                    ( ( unLastObject or ( unNextObject.__class__.__name__ == 'TRAColeccionCadenas')) and ( 'Last object: %s' % str( unLastObject))) or '',
                )
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   
                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return None                 
                
        finally:
            unExecutionRecord and unExecutionRecord.addExtraInfo( '[objs %d]' % len( unosObjectsPassingLastStep))
    
            unExecutionRecord and unExecutionRecord.pEndExecution()
   

    
    
            
            
            
            
            
            
            
            


    
    
  
# ####################################
#  General Use Case queries: 
#    Which Use Cases are available for the connected user
#    to enact on the specified element ?
#    
# ####################################
              
    
     
    security.declareProtected( permissions.View, 'fUseCaseAssessment_AvailableUseCasesOn')
    def fUseCaseAssessment_AvailableUseCasesOn(self, 
        theElement              =None, 
        theUseCaseNamesToAssess =None, 
        theRulesToCollect       =None,
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):  
        """Determine which Use Cases are available for the connected user to exercise on the current object, including the Use Cases with names supplied as parameter or all the existing Use Cases if no Use Case name was requested.
                
        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fUseCaseAssessment_AvailableUseCasesOn', theParentExecutionRecord, False) 
        
        try:
            unosUseCasesResultsDict = { }
    
            if theElement == None:
                return unosUseCasesResultsDict
            
            unosUseCaseNames = theUseCaseNamesToAssess
            if not unosUseCaseNames:
                unosUseCaseNames = cTRAUseCaseNames
                            
            unPermissionsCache = thePermissionsCache
            if not unPermissionsCache:
                unPermissionsCache = { }
                
            unRolesCache = theRolesCache
            if not unRolesCache:
                unRolesCache = { }
                
            
            for unUseCaseName in unosUseCaseNames:
                unUseCaseQueryResult = self.fUseCaseAssessment( 
                    theUseCaseName          = unUseCaseName, 
                    theElementsBindings     = { cBoundObject: theElement,},
                    theRulesToCollect       = theRulesToCollect, 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord,
                )
                
                if unUseCaseQueryResult:
                    unosUseCasesResultsDict[ unUseCaseName] = unUseCaseQueryResult
    
            return unosUseCasesResultsDict
                
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
    
   

            
            
            
            
            
            
             
            
            
    # #############################################################
    """Initialization of Global to hold the rule handler jump table on rule mode.
    
    """    
    gUseCaseRuleModeHandlers = { 
        cUseCaseRuleMode_ForAll:        fUseCaseRuleAssessment_ForAll,
        cUseCaseRuleMode_Filter:        fUseCaseRuleAssessment_Filter,
        cUseCaseRuleMode_EmptyOrAll:    fUseCaseRuleAssessment_EmptyOrAll,
        cUseCaseRuleMode_EmptyOrAny:    fUseCaseRuleAssessment_EmptyOrAny,
    }       
    
         
            

    
    
    
    
    
    
   