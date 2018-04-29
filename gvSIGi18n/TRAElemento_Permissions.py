# -*- coding: utf-8 -*-
#
# File: TRAElemento_Permissions.py
#
# Copyright (c) 2008, 2009 by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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


import  logging


from time                                   import time

from DateTime                               import DateTime

from StringIO                               import StringIO

from reStructuredText                       import HTML



from AccessControl                          import ClassSecurityInfo
from Acquisition                            import aq_inner, aq_parent




from Products.Archetypes.utils              import shasattr

from Products.CMFCore                       import permissions

from Products.CMFCore.utils                 import getToolByName


from Products.Archetypes.atapi              import OrderedBaseFolder





from TRAElemento_Constants                  import *

from TRAElemento_Permission_Definitions     import *
from TRAElemento_Permissions_SecuritySchemaDocumentation     import cSecuritySchemaDocumentation






class TRAElemento_Permissions:
    """
    """
    security = ClassSecurityInfo()

    
    
    
    
# #############################################################
# "Globals" to hold the security specifications as ready to be assessed
#   The structure in the source code is better suited
#   for the view point of the requirements specifier
#   and is re-structured and hashed as dictionaries for fast access.
#
# Some other information, as platform specific details,
#   on which types shall or shall not acquire permissions
#   or role assignments to users and user groups
#   are also integrated ducing pre-processing.
#
# The permissions are specified with abbreviated string names 
#   and are de-coded into their plone names during pre-processing
#
# #############################################################

    gPermissionsByElementType       = { }

    gUseCaseSpecificationsByName    = { }
 
        
    
    
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
    # Access Security configuration  specification 
    # #############################################################
        

    
    # #############################################################
    # Access documentation
    #    Security configuration  specification 
    # #############################################################
  
        
    security.declarePublic( 'fSecuritySchemaDocumentation')
    def fSecuritySchemaDocumentation(self,):
        return self.fAsUnicode( cSecuritySchemaDocumentation)
    
    
    security.declarePublic( 'fSecuritySchemaDocumentation_REST')
    def fSecuritySchemaDocumentation_REST(self,):
        return self.fSecuritySchemaDocumentation()
    
    
    
    security.declarePublic( 'fSecuritySchemaDocumentation_HTML')
    def fSecuritySchemaDocumentation_HTML(self, theContextualObject, theCollapsible=False, theCollapsed=True):
        anEditableBody = self.fSecuritySchemaDocumentation_REST()
        
        if not anEditableBody:
            return ''
        
        aCookedBody = HTML( anEditableBody, initial_header_level=1, input_encoding='utf-8', output_encoding='utf-8')
        if not aCookedBody:
            return ''
        
        anOutput = StringIO()
        anOutput.write( "\n<br/>\n")
        
        if not theCollapsible:
            anOutput.write( aCookedBody)
            aResult = anOutput.getvalue()
            return aResult
        
        self.pRenderCollapsible_Lambda( anOutput, "Security schema explained", "sect_Security_schema_explained", lambda : anOutput.write( self.fAsUnicode( aCookedBody)), theCollapsed)

        aResult = anOutput.getvalue()
        
        return aResult
    
    
    
    
        
        

    

        
        
        
    # #############################################################
    # Access and Lazy initialize Permissions by type
    #    Security configuration specification 
    # #############################################################    

    security.declarePrivate( 'fPermissionsForElement')
    def fPermissionsForElement(self, theElement=None):

        unElement = theElement
        if not fsISS( unElement):
            unElement = self

        unElementType = unElement.__class__.__name__
        
        return self.fPermissionsForElementType( unElementType)

    
    
    
    
    security.declarePrivate( 'fPermissionsForElementType')
    def fPermissionsForElementType(self, theElementType):

        if not theElementType:
            return {}
            
        somePermissionsSpecifications = self.fPermissionsByElementType()
 
        if not somePermissionsSpecifications:
            return {}
        
        return somePermissionsSpecifications.get( theElementType, None)     

    
    
    
    
    
    
    # #############################################################
    # Lazy initialize Access Security configuration specification 
    #   Use Cases
    # #############################################################

    security.declarePrivate( 'fPermissionsByElementType')
    def fPermissionsByElementType(self,):
        if not TRAElemento_Permissions.gPermissionsByElementType:
            TRAElemento_Permissions.gPermissionsByElementType = self.fInitValuePermissionsByElementType()

        return TRAElemento_Permissions.gPermissionsByElementType
    

    

    


   
    # #############################################################
    # Access and Lazy initialize Use Cases
    #    Security configuration specification 
    # #############################################################  
 
    
    security.declarePrivate( 'fUseCaseSpecification')
    def fUseCaseSpecification(self, theUseCaseName):

        if not theUseCaseName:
            return []
        
        unasUseCaseSpecifications = self.fUseCaseSpecificationsByName()
        if not unasUseCaseSpecifications:
            return []
        
        return unasUseCaseSpecifications.get( theUseCaseName, None)     
    
    
    
    security.declarePrivate( 'fUseCaseSpecificationsByName')
    def fUseCaseSpecificationsByName(self,):
        # ACV 200903221315 Force evaluation, caching on instance does not work as the instance persist the slot !        

        if not TRAElemento_Permissions.gUseCaseSpecificationsByName:
            TRAElemento_Permissions.gUseCaseSpecificationsByName = self.fInitValueUseCaseSpecificationsByName()

        return TRAElemento_Permissions.gUseCaseSpecificationsByName    

    
        
        
        
            
    
    
 
    
    
    # #############################################################
    # Lazy initialize Access Security configuration specification 
    #  Permissions by type
    # #############################################################

    security.declarePrivate( 'declarePrivate')
    def fNewVoidPermissionsSpec( self, theAcquirePermission, theRoles):
        unaSpec = {
            'acquire_permissions':  theAcquirePermission,
            'roles':                theRoles,
        }
        return unaSpec
    
    
    
    security.declarePrivate( 'fInitValuePermissionsByElementType')
    def fInitValuePermissionsByElementType( self,):
        
        unasPermissionsByType = { }
    
        for unUseCaseName in cTRAUseCasesWithAbbreviatedPermissions.keys():
            unUseCaseSpec     = cTRAUseCasesWithAbbreviatedPermissions[ unUseCaseName]
            unosVerificables  = unUseCaseSpec[ 0]
            unosAdicionales   = unUseCaseSpec[ 1]
            
            for unVerificable in unosVerificables:
                unPath      = unVerificable[ 'path']
                unosTypes   = unVerificable[ 'types']
                unosPerms   = unVerificable[ 'perms']
                unosRoles   = unVerificable[ 'roles']
    
                for unNombreTipo in unosTypes:
                    unasPermissionsDeTipo = unasPermissionsByType.get( unNombreTipo, None)
                    if not unasPermissionsDeTipo:
                        unasPermissionsDeTipo = { }
                        unasPermissionsByType[ unNombreTipo] = unasPermissionsDeTipo
                    for unaPermAbbreviation in unosPerms:    
                        unaPermission = cPermissionsByAbbreviation.get( unaPermAbbreviation, '')
                        if unaPermission:
                            unaConfiguracionPermision = unasPermissionsDeTipo.get( unaPermission, None)
                            if not unaConfiguracionPermision:
                                unaConfiguracionPermision = self.fNewVoidPermissionsSpec( unNombreTipo in cTypesAcquiringPermissions, set( unosRoles[:]))
                                unasPermissionsDeTipo[ unaPermission] = unaConfiguracionPermision
                            else:
                                unaConfiguracionPermision[ 'roles'] = unaConfiguracionPermision[ 'roles'].union( unosRoles) 
                            
            for unAdicional in unosAdicionales:
                unosTypes   = unAdicional[ 0]
                unosPerms   = unAdicional[ 1]
                unosRoles   = unAdicional[ 2]
    
                for unNombreTipo in unosTypes:
                    unasPermissionsDeTipo = unasPermissionsByType.get( unNombreTipo, None)
                    if not unasPermissionsDeTipo:
                        unasPermissionsDeTipo = { }
                        unasPermissionsByType[ unNombreTipo] = unasPermissionsDeTipo
                    for unaPermAbbreviation in unosPerms:    
                        unaPermission = cPermissionsByAbbreviation.get( unaPermAbbreviation, '')
                        if unaPermission:
                            unaConfiguracionPermision = unasPermissionsDeTipo.get( unaPermission, None)
                            if not unaConfiguracionPermision:
    
                                unaConfiguracionPermision = self.fNewVoidPermissionsSpec( unNombreTipo in cTypesAcquiringPermissions, set( unosRoles[:])) 
                      
                                unasPermissionsDeTipo[ unaPermission] = unaConfiguracionPermision
                            else:
                                unaConfiguracionPermision[ 'roles'] = unaConfiguracionPermision[ 'roles'].union( unosRoles) 
    
        for unNombreTipo in cTodosNombresTipos:
            unasPermissionsDeTipo = unasPermissionsByType.get( unNombreTipo, None)
            if not ( unasPermissionsDeTipo):
                unasPermissionsByType[ unNombreTipo] =  dict( [ ( unaPermission,  self.fNewVoidPermissionsSpec( unNombreTipo in cTypesAcquiringPermissions, set( )), ) for unaPermission in cPreferredPermissions] )
            else:
                for unaPermission in cPreferredPermissions:
                    unaConfiguracionPermision = unasPermissionsDeTipo.get( unaPermission, None)
                    if not unaConfiguracionPermision:
                        unasPermissionsDeTipo[ unaPermission] = self.fNewVoidPermissionsSpec( unNombreTipo in cTypesAcquiringPermissions, set( ))
                   
                        
        return  unasPermissionsByType                       
        

       
    
    
    
   
    
     
    
    # #############################################################
    # Lazy initialize Access Security configuration specification 
    #   Use Cases
    # #############################################################
 
    
    def fInitValueUseCaseSpecificationsByName( self,):
        
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
     
        
        return unosNewUseCases
    





    
    # #############################################################
    # Access acquisition of Role assignment to users and groups 
    #    Security configuration specification 
    # #############################################################  

       
  
    security.declarePrivate( 'fAcquireRoleAssignmentsElement')
    def fAcquireRoleAssignmentsElement(self, theElement=None):

        unElement = theElement
        if not fsISS( unElement):
            unElement = self

        unType = unElement.__class__.__name__
        
        return self.fAcquireRoleAssignmentsElementType( unType)

    
    
    
    
    security.declarePrivate( 'fAcquireRoleAssignmentsElementType')
    def fAcquireRoleAssignmentsElementType(self, theElementType):

        if not theElementType:
            return False
            
        if cTypesAcquiringRoleAssignments == None:
            return False
        
        return theElementType in cTypesAcquiringRoleAssignments
   
    
    
    security.declarePrivate( 'fIsAcquiringRoleAssignments')
    def fIsAcquiringRoleAssignments(self, theElement=None):
            
        unElement = theElement
        if not fsISS( unElement):
            unElement = self
            
        aPloneUtilsTool = self.getPloneUtilsToolForRoleAcquisition()
        if not aPloneUtilsTool:
            return False
        
        return aPloneUtilsTool.isLocalRoleAcquired( unElement)    
    
    
    security.declarePrivate( 'fSetAcquiringRoleAssignments')
    def fSetAcquiringRoleAssignments(self, theElement=None, theMustAcquire=True):
            
        unElement = theElement
        if not fsISS( unElement):
            unElement = self
            
        aPloneUtilsTool = self.getPloneUtilsToolForRoleAcquisition()
        if not aPloneUtilsTool:
            return False
        
        return aPloneUtilsTool.acquireLocalRoles( unElement, theMustAcquire)    
    
    
    
    
    
    # #############################################################
    # Security configuration  
    #   Initialize an object's permissions upon creation
    #      according to the permissions specification
    # Shall be invoked from the manage_afterAdd delegation of 
    #   all objects except TRACadena and TRATraduccion
    #
    #   Not to be used with TRACadena and TRATraduccion
    #      that are set up during import, where the permissions to set 
    #      are known beforehand for the thousandas of instances to create
    #   
    # #############################################################

    
    
    security.declarePrivate( 'pSetPermissions')
    def pSetPermissions(self):
 
        unasPermissionsSpec = self.getCatalogo().fPermissionsForElement( self)   
        if not unasPermissionsSpec:
            return self
        
        for unaPermission in unasPermissionsSpec.keys():
            unaPermissionSpec        = unasPermissionsSpec[ unaPermission]
            unAcquire                = unaPermissionSpec[ 'acquire_permissions'] 
            unosRoles                = list( unaPermissionSpec[ 'roles'])
            
            if unaPermission:
                self.manage_permission( unaPermission, roles=unosRoles, acquire=unAcquire)
                
    
            aAcquireRoleAssignments       = self.fAcquireRoleAssignmentsElement( self)
            aIsAcquiringRoleAssignments   = self.fIsAcquiringRoleAssignments(    self)
            
            if aAcquireRoleAssignments:
                if aIsAcquiringRoleAssignments:
                    pass # it's already ok 
                else:
                    self.fSetAcquiringRoleAssignments( self, True)
                    
                    if self.fIsAcquiringRoleAssignments( self):                                
                        pass # has been set ok
                    else:
                        pass # error setting role assignment acquisition                 
            else:
                if aIsAcquiringRoleAssignments:
                    self.fSetAcquiringRoleAssignments( self, False)
                    
                    if self.fIsAcquiringRoleAssignments( self):                                
                        pass # error setting role assignment acquisition
                    else:
                        pass # has been set ok                
                else:
                    pass # it's already ok 
                                
                
        return self
    
    

    
    
    

    
        
 
    # #############################################################
    # Security check utility : Roles
    #   Has the user ALL of the specified permissions ?
    # #############################################################
    
     

    security.declarePrivate( 'fCheckElementPermission')
    def fCheckElementPermission(self, theObject, thePermissionsToCheck, thePermissionsCache=None ):
        if not fsISS( theObject):
            return False
        
        if not thePermissionsToCheck:
            return True
        
        aPermissionsToCheck = thePermissionsToCheck
        
        if not ( aPermissionsToCheck.__class__.__name__ in [ 'list', 'tuple', 'set',]):
            aPermissionsToCheck = [ [ aPermissionsToCheck, ], ]
        else:
            aPermissionsToCheck = [ ]
            for aPermission in thePermissionsToCheck:
                if aPermission.__class__.__name__ in [ 'list', 'tuple', 'set',]:
                    aPermissionsToCheck.append( list( aPermission))
                else:
                    aPermissionsToCheck.append( [ aPermission,])
        

        unaObjectKey = theObject.UID()
        
        unCachedPermissions = None
        if thePermissionsCache:
            if thePermissionsCache.has_key( unaObjectKey):
                unCachedPermissions = thePermissionsCache.get( unaObjectKey, None)
            if unCachedPermissions == None:
                unCachedPermissions = {  }
                thePermissionsCache[ unaObjectKey] = unCachedPermissions
        else:
                unCachedPermissions = { }
        
        aPortalMembershipTool = None
                     
        for aPermissionsBlock in aPermissionsToCheck:
            unPermitted = True
            if aPermissionsBlock:
                for aPermission in aPermissionsBlock:
                    if unCachedPermissions and unCachedPermissions.has_key( aPermission):
                        aPermitted = unCachedPermissions.get( aPermission, False)
                    else:
                        if not aPortalMembershipTool:
                            aPortalMembershipTool = getToolByName( self, 'portal_membership') 
                            if not aPortalMembershipTool:
                                return False
                                
                        aPermitted = aPortalMembershipTool.checkPermission( aPermission, theObject)
                        if not( unCachedPermissions == None):
                            unCachedPermissions[ aPermission] = aPermitted
                        if not aPermitted:
                            break
                if unPermitted:
                    return True
        return False

       
    
    

    
 
    
    
    
    
    
    
    

    
    

    
    # #######################################
    # Rendering utilities
    # #######################################
    
    
    def fRenderPermissionsByElementType(self,):
        unOutput = StringIO()
        
        unosTypesNames = sorted( TRAElemento_Permissions.gPermissionsByElementType.keys())   
        
        unOutput.write( "\n\nRender Permissions By Element Type for %d types\n" % len( unosTypesNames))
        
        for unTypeName in unosTypesNames:
            unOutput.write( "\n%sType %s\n" % ( cIndent, unTypeName, ))
    
            unasPermissionsSpec = TRAElemento_Permissions.gPermissionsByElementType.get(unTypeName, None)   
            if unasPermissionsSpec:
            
                for unaPermission in unasPermissionsSpec.keys():
                    unaPermissionSpec = unasPermissionsSpec[ unaPermission]
                    unAcquire     = unaPermissionSpec[ 'acquire'] 
                    unosRoles     = list( sorted( unaPermissionSpec[ 'roles']))
                    
                    unOutput.write( "%s%s %s roles: %s\n" % ( 
                        cIndent * 2, 
                        unaPermission,
                        ( unAcquire and 'Acquire') or 'NO acquire',
                        ' '.join( unosRoles), ))
                   
        unOutput.write( "\n\n" )
        return unOutput.getvalue()
        
    
    
    
    
    
    
    
    
    # #############################################################
    # Security configuration rendering utility 
    # #############################################################
    
    
    
    security.declareProtected( permissions.View, 'fRenderUserAndRoles_HTMLcollapsible')
    def fRenderUserRolesAndPermissions_HTMLcollapsible(self, theCollapse=True):
        return self.fText2HTML_collapsible( self.fRenderUserRolesAndPermissions(), 'User, Roles and Permissions', 'csect_UserRolesAndPermissions', theCollapse)
    
    
       
    security.declareProtected( permissions.View, 'fRenderUserRolesAndPermissions')
    def fRenderUserRolesAndPermissions(self, theCollapse=True):
        
        unUser    = self.fGetRequestingUserObject()
        unosRoles = self.fGetRolesForUserObject( unUser, self)

        aPortalMembershipTool = getToolByName( self, 'portal_membership') 
        
        unOutput = StringIO()

        if unUser:
            unUserName = unUser.getUserName()
        else:
            unUserName = 'unknown'
            
        unOutput.write( "\n\nUser %s at element %s\n" % ( unUserName, '/'.join( self.getPhysicalPath()),))

        unOutput.write( "%sroles %s\n%s" % ( cIndent, ' '.join( unosRoles), cIndent,))
        
        for aPermission in cPreferredPermissions:
            aPermitted = aPortalMembershipTool.checkPermission( aPermission, self)
            unOutput.write( "%s %s%s" % (  aPermission, (aPermission and 'YES') or 'NO ', cIndent, ))
            
        unOutput.write( "\n\n")
                                 
        return unOutput.getvalue()
    
    
    
        


   
    
    
    
    # ####################################
    #  Role queries: 
    #      is the connected user in a/some specific role/s ?
    # ####################################
        
 
        
    security.declareProtected( permissions.View, 'fRoleQuery_IsManager')
    def fRoleQuery_IsManager(self, theElement=None):
        return self.fRoleQuery_IsAnyRol( cManagerRoles, theElement)
      
    
    security.declareProtected( permissions.View, 'fRoleQuery_IsCoordinator')
    def fRoleQuery_IsCoordinator(self, theElement=None):
        return self.fRoleQuery_IsAnyRol( cTRACoordinator_role, theElement)
      
    security.declareProtected( permissions.View, 'fRoleQuery_IsCoordinatorOrDeveloper')
    def fRoleQuery_IsCoordinatorOrDeveloper(self, theElement=None):
        return self.fRoleQuery_IsAnyRol( [ cTRACoordinator_role , cTRADeveloper_role, ], theElement)
      
    security.declareProtected( permissions.View, 'fRoleQuery_IsDeveloper')
    def fRoleQuery_IsDeveloper(self, theElement=None):
        return self.fRoleQuery_IsAnyRol( cTRADeveloper_role, theElement)
      
        
        
    security.declareProtected( permissions.View, 'fRoleQuery_IsManagerOrCoordinator')
    def fRoleQuery_IsManagerOrCoordinator(self, theElement=None):
        return self.fRoleQuery_IsAnyRol( cManagerRoles + [ cTRACoordinator_role, ], theElement)
      
        
    security.declareProtected( permissions.View, 'fRoleQuery_IsReviewer')
    def fRoleQuery_IsReviewer(self, theElement=None):
        return self.fRoleQuery_IsAnyRol( cTRAReviewer_role, theElement)
      
    
    security.declareProtected( permissions.View, 'fRoleQuery_IsTranslator')
    def fRoleQuery_IsTranslator(self, theElement=None):
        return self.fRoleQuery_IsAnyRol( cTRATranslator_role, theElement)
      
    
    security.declareProtected( permissions.View, 'fRoleQuery_IsVisitor')
    def fRoleQuery_IsVisitor(self, theElement=None):
        return self.fRoleQuery_IsAnyRol( cTRAVisitor_role, theElement)
      
      
    
    
    
    
    
    
    security.declarePrivate( 'fGetElementRoles')
    def fGetElementRoles(self, theObject, theRolesCache=None ):
        """Get the roles held by the connected user at theObject.
        
        """
      
        if not fsISS( theObject):
            return False
           
        unUser = self.fGetRequestingUserObject()
        if not unUser:
            return []
        
        unaObjectKey = theObject.UID()
        
        unCachedRoles = None
        
        unosCachedRoles    = None
        if not ( theRolesCache == None):        
            """Attempt to retrieve from cache roles held by the user.
            
            """
            if theRolesCache.has_key( unaObjectKey):
                unosCachedRoles = theRolesCache.get( unaObjectKey, None)  
                return unosCachedRoles
            else:
                unosCachedRoles = set( )
                theRolesCache[ unaObjectKey] = unosCachedRoles    
      
        
        """Query Plone for roles held by the user.
        
        """
        someRolesForUserObject = self.fGetRolesForUserObject( unUser, theObject)
        if not someRolesForUserObject:
            return set()
        
        if not ( unosCachedRoles == None):
            unosCachedRoles.update( someRolesForUserObject)
                
            
        return set( someRolesForUserObject)

       
    
  
       
            

    
         

    security.declarePrivate( 'fCheckElementRoles')
    def fCheckElementRoles(self, theObject, theRolesToCheck, theRolesCache=None ):
        """Check security Roles: Has the user ANY of the specified roles ?
        
        """
        
        if not fsISS( theObject):
            return False
        
        if not theRolesToCheck:
            return True
        
        aRolesToCheck = theRolesToCheck
        
        # ############################
        """Shall check on a list of alternative lists of roles. The user shall hold all roles in at least one list of roles.
        
        If argument is a single string or a list, build a list of lists.
        """
        if not ( theRolesToCheck.__class__.__name__ in [ 'list', 'tuple', 'set',]):
            aRolesToCheck = [ set( [ aRolesToCheck, ]), ]
        else:
            aRolesToCheck = [ ]
            for aRole in theRolesToCheck:
                if aRole.__class__.__name__ in [ 'list', 'tuple', 'set',]:
                    aRolesToCheck.append( set( aRole))
                else:
                    aRolesToCheck.append( set( [ aRole,]))
                    
                    
        unUser = self.fGetRequestingUserObject()
        if not unUser:
            return []
        
        unaObjectKey = theObject.UID()
        
        
        unosCachedRoles    = None
        unosHeldRoles      = None
        if not ( theRolesCache == None):        
            """Attempt to retrieve from cache roles held by the user.
            
            """
            if theRolesCache.has_key( unaObjectKey):
                unosCachedRoles = theRolesCache.get( unaObjectKey, None) 
                unosHeldRoles   =  unosCachedRoles
            else:
                unosCachedRoles = set( )
                theRolesCache[ unaObjectKey] = unosCachedRoles    
      
        
        if ( unosHeldRoles == None):
            """Query Plone for roles held by the user.
            
            """
            someRolesForUserObject = self.fGetRolesForUserObject( unUser, theObject)
            if someRolesForUserObject:
                unosHeldRoles = set( someRolesForUserObject) 
                
                if not ( unosCachedRoles == None):
                    unosCachedRoles.update( unosHeldRoles)
            else:
                unosHeldRoles = set()
      
        for aRolesBlock in aRolesToCheck:
            aRolesBlockSet = set( aRolesBlock)
            if not aRolesBlockSet - unosHeldRoles:
                return True
            
        return False

    
    
       
    
    
    
    
    
    
    
    
    
    
    
           

    security.declareProtected( permissions.View, 'fRoleQuery_IsAnyRol')
    def fRoleQuery_IsAnyRol( self, theRolesUsuario, theElement=None):
        return len( self.fWhichRoles( theRolesUsuario, theElement)) > 0
  
    
    
    

    
    security.declarePublic( 'fIsRoles')
    def fWhichRoles( self, theRolesUsuario, theElement=None):
        if not theRolesUsuario:
            return { }
        
        unosRolesUsuario = theRolesUsuario
        if not ( unosRolesUsuario.__class__.__name__ in [ 'list', 'tuple', ]):
            unosRolesUsuario = [ unosRolesUsuario,]
            
        todosRolesPoseidos = set( self.fGetRequestingUserRoles())
        
        unosRoles = set( theRolesUsuario).intersection(  todosRolesPoseidos)
        
        return unosRoles
    
              
              


    security.declarePublic( 'fGetRequestingUserRoles')
    def fGetRequestingUserRoles(self, theElement=None):
        unElement = theElement
        if not fsISS( unElement):
            unElement = self
        
        unUser = self.fGetRequestingUserObject()
        if not unUser:
            return []
        
        unosRoles = self.fGetRolesForUserObject( unUser, unElement)
        return unosRoles
    

    
    security.declarePrivate( 'fGetRequestingUserObject')
    def fGetRequestingUserObject(self):
        unaRequest = self.REQUEST
        if not unaRequest:
            return None
        
        unUser = unaRequest.get("AUTHENTICATED_USER", None)
        return unUser

    
    
    security.declarePrivate( 'fGetRolesForUserObject')
    def fGetRolesForUserObject(self, theUserObject, theElement):
        if not theUserObject or not fsISS( theElement):
            return set()
        unosRoles = theUserObject.getRolesInContext( theElement)
        if not unosRoles:
            return set()
        return set( unosRoles)
    


    
    
    
    
    
    
    
    


        
    
    
    security.declarePublic( 'fGetMemberId')
    def fGetMemberId(self ):
        """Connected user Membership 
        
        """
    
        aMembershipTool = getToolByName( self, 'portal_membership', None)
        if not aMembershipTool:
            return ''
        
        unMember = aMembershipTool.getAuthenticatedMember()   

        if not unMember:
            return ''
        
        unMemberId = unMember.getMemberId()           
        return unMemberId
        
    
    
    
    
    
    
     
    
    
    
    security.declareProtected( permissions.View, 'fUseCaseAssessment_TranslationStateChange')
    def fUseCaseAssessment_TranslationStateChange(self, theTraduccion, theTargetState, thePermissionsCache, theRolesCache, theParentExecutionRecord ):  
        if not theTraduccion or not theTargetState:
            return False
        unaCadena = theTraduccion.getCadena()
        if not unaCadena:
            return False
        unIdioma = theTraduccion.fObtenerIdioma()
        if not unIdioma:
            return False
        unosModulos = theTraduccion.fObtenerModulos()
        
        unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
        unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
        
        aUseCaseAssessmentResult = self.fUseCaseAssessment( 
            theUseCaseName          = cUseCase_TranslationStateChange, 
            theElementsBindings     = { cBoundObject: theTraduccion,},
            theRulesToCollect       = [ ], 
            thePermissionsCache     = unPermissionsCache, 
            theRolesCache           = unRolesCache, 
            theParentExecutionRecord= unExecutionRecord,
        )
        if not aUseCaseAssessmentResult or not aUseCaseAssessmentResult.get( 'success', False):
            return False
        
        return theTraduccion.fCanChangeToNuevoEstadoTraduccion( theTargetState)
    
      
    

    
    


    
    
    
    
    
    
    
  
# ####################################
#  General Use Case queries: 
#    Is the Use Case available for the connected user
#    on the specified element ?
# ####################################
              
    

    security.declarePrivate( 'fUseCaseAssementReuse')
    def fUseCaseAssementReuse(self, 
        theAlreadyQueriedUseCaseResults,
        theUseCaseName, 
        theElementsBindings, 
        theRulesToCollect=False, 
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):  

    
        if not theAlreadyQueriedUseCaseResults:
            return self.fUseCaseAssessment( 
                theUseCaseName, 
                theElementsBindings, 
                theRulesToCollect=False, 
                thePermissionsCache=None, 
                theRolesCache=None, 
                theParentExecutionRecord=None)
        
        for aUseCaseQueryResult in theAlreadyQueriedUseCaseResults:
            if ( aUseCaseQueryResult.get( 'use_case_name', '')      == theUseCaseName) and \
               ( aUseCaseQueryResult.get( 'report_details', '')     == theRulesToCollect):
            
                unosElementsBindings = aUseCaseQueryResult.get( 'elements_bindings', '')
                if not unosElementsBindings and not theElementsBindings:
                    return aUseCaseQueryResult
                
                if unosElementsBindings.keys().intersection(  theElementsBindings.keys()):
                    if len( [ unaBindingKey for unaBindingKey in theElementsBindings.keys() if unosElementsBindings.get( unaBindingKey, None) ==  theElementsBindings.get( unaBindingKey, None)]) == len( theElementsBindings):
                        return aUseCaseQueryResult
                     
        return self.fUseCaseAssessment( 
            theUseCaseName, 
            theElementsBindings, 
            theRulesToCollect=False, 
            thePermissionsCache=None, 
            theRolesCache=None, 
            theParentExecutionRecord=None)

    
    
    
    
    
    
    
            
            
            
            
            
            
            
            

 
    security.declarePrivate( 'fUseCaseAssessment')
    def fUseCaseAssessment(self, 
        theUseCaseName, 
        theElementsBindings, 
        theRulesToCollect       =False, 
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
                
        
                 
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                   
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
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
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
        
        unRuleModeHandler = TRAElemento_Permissions.gUseCaseRuleModeHandlers.get( unUseCaseRuleMode, None)
        if not unRuleModeHandler:
            return None
                     
        
        return unRuleModeHandler(
            self,
            theUseCaseName,
            theUseCaseRule, 
            theRuleName,
            theUseCaseAssessment,
            theMustCollect          = theMustCollect,
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
                
                
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                    

                unosRejectedObjects = theUseCaseAssessment.get( 'rejected_objects', [])
                
                unosTypes       = theUseCaseRule.get( 'types', [])
                unasPerms       = theUseCaseRule.get( 'perms', [])
                unosRoles       = theUseCaseRule.get( 'roles', [])
                
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
                """Assess rule constraints against each retrieved, non previously rejected object.
                
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
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
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
                
                
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                    
                unosRejectedObjects = theUseCaseAssessment.get( 'rejected_objects', [])
                
                unosTypes       = theUseCaseRule.get( 'types', [])
                unasPerms       = theUseCaseRule.get( 'perms', [])
                unosRoles       = theUseCaseRule.get( 'roles', [])
                
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
                """Assess rule constraints against each retrieved, non previously rejected object.
                
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
 
                            
                    if not unObjectPassed:
                        unosRejectedObjects.add( unObjectToCheck)                                
            
                        if theMustCollect:
                            if not ( unInitialObject in unosRejectedInitialObjects):
                                unosRejectedInitialObjects.append( unInitialObject)                            
                            if not ( unInitialObject in unosRejectedFinalObjects):
                                unosRejectedFinalObjects.append(   unObjectToCheck)                            
                    
                    else:
                        if not ( unObjectPassed in unosRejectedObjects):
                            unosAcceptedInitialObjects.append( unInitialObject)                            
                            unosAcceptedFinalObjects.append(   unObjectToCheck)                            
                            
                
                unUseCaseRuleAssessment[ 'success'] = True
                unUseCaseRuleAssessment[ 'status']     = cRuleAssessment_Passed
                 
                return unUseCaseRuleAssessment
                    
            except:
                    
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fUseCaseRuleAssessment_Filter\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
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
                
                
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                    
                unosRejectedObjects = theUseCaseAssessment.get( 'rejected_objects', [])
                
                unosTypes       = theUseCaseRule.get( 'types', [])
                unasPerms       = theUseCaseRule.get( 'perms', [])
                unosRoles       = theUseCaseRule.get( 'roles', [])
                
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
                """Assess rule constraints against each retrieved, non previously rejected object.
                
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
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
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
                
                
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                    
                unosRejectedObjects = theUseCaseAssessment.get( 'rejected_objects', [])
                
                unosTypes       = theUseCaseRule.get( 'types', [])
                unasPerms       = theUseCaseRule.get( 'perms', [])
                unosRoles       = theUseCaseRule.get( 'roles', [])
                
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
                """Assess rule constraints against each retrieved, non previously rejected object.
                
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
 
                            
                    if not unObjectPassed:
                        unosRejectedObjects.add( unObjectToCheck)                                
            
                        if theMustCollect:
                            if not ( unInitialObject in unosRejectedInitialObjects):
                                unosRejectedInitialObjects.append( unInitialObject)                            
                            if not ( unInitialObject in unosRejectedFinalObjects):
                                unosRejectedFinalObjects.append(   unObjectToCheck)                            
                   
                    else:
                        if not( unObjectPassed in unosRejectedObjects):
                            if theMustCollect:
                                unosAcceptedInitialObjects.append( unInitialObject)                            
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
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
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
                                if unNextObject or ( unNextObject.__class__.__name__ == 'TRAColeccionCadenas'):
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
                
                """From the objects obtained by traversing the whole path, discard the ones that may have been discarded in a previous rule.
                 
                 Note that only rules of special modes may reject objects without 
                 making fail the use case assessment, and therefore allow the case
                 of retrieving for assessment in the initial step of a rule, 
                 objects rejected by previous rules: normal rules will fail and stop us case assessment.
                 """
                
                return unosObjectsPassingLastStep
         
            except:
                    
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fUseCaseRuleAssessment_ObjectsRetrieval %s%s\n'  % (
                    ( unLastStep and ( 'Last step: %s' % unLastStep)) or '',
                    ( ( unLastObject or ( unNextObject.__class__.__name__ == 'TRAColeccionCadenas')) and ( 'Last object: %s' % str( unLastObject))) or '',
                )
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
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
        theElement, 
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
    
            if not theElement:
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
                    unUseCaseName,  
                    { cBoundObject: theElement,}, 
                    theRulesToCollect, 
                    unPermissionsCache, 
                    unRolesCache, 
                    unExecutionRecord
                )
                
                if unUseCaseQueryResult:
                    unosUseCasesResultsDict[ unUseCaseName] = unUseCaseQueryResult
    
            return unosUseCasesResultsDict
                
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
    
   

    # #############################################################
    """Global to hold the rule handler jump table on rule mode.
    
    """    
    gUseCaseRuleModeHandlers = { 
        cUseCaseRuleMode_ForAll:                    fUseCaseRuleAssessment_ForAll,
        cUseCaseRuleMode_Filter:                    fUseCaseRuleAssessment_Filter,
        cUseCaseRuleMode_EmptyOrAll:           fUseCaseRuleAssessment_EmptyOrAll,
        cUseCaseRuleMode_EmptyOrAny:    fUseCaseRuleAssessment_EmptyOrAny,
    }       
    
         
            