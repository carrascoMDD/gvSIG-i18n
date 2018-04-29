# -*- coding: utf-8 -*-
#
# File: TRAElemento_Permissions.py
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
from TRAElemento_Permission_Definitions_UseCaseNames     import *
from TRAElemento_Permission_Definitions_UseCases         import cTRAUseCasesWithAbbreviatedPermissions

from TRAElemento_Permissions_UseCases       import TRAElemento_Permissions_UseCases





class TRAElemento_Permissions( TRAElemento_Permissions_UseCases):
    """Class with responsibility to deal with permissions to access elements and execute Use Cases.
    
    """
    
    security = ClassSecurityInfo()

    
    
    
    
    


    
    
    # #############################################################
    """Globals to hold the security specifications as ready to be assessed
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

    gPermissionsForTRACatalogsByElementType = { }

    gStateChangeActionRoles                 = { }
   

        
        
        
    # #############################################################
    """Access and Lazy initialize Permissions by type
        Security configuration specification 
    """
    
    security.declarePrivate( 'fPermissionsForElement')
    def fPermissionsForElement(self, theElement=None):

        unElement = theElement
        if unElement == None:
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


    security.declarePrivate( 'fPermissionsByElementType')
    def fPermissionsByElementType(self,):
        """Lazy initialize Access Security configuration specification by Type names.
        
        """
        
        unPathDelRaiz = self.fPathDelRaiz()
        if not unPathDelRaiz:
            return { }
        
        
        unasPermissionsForTRACatalogsByElementType = TRAElemento_Permissions.gPermissionsForTRACatalogsByElementType
        
        if not unasPermissionsForTRACatalogsByElementType:
            
            unasPermissionsForTRACatalogsByElementType = { }
            
            TRAElemento_Permissions.gPermissionsForTRACatalogsByElementType = unasPermissionsForTRACatalogsByElementType
            
            

        unasPermissionsByElementType = unasPermissionsForTRACatalogsByElementType.get( unPathDelRaiz, None)
        
        if not unasPermissionsByElementType:
            
            unasPermissionsByElementType = self.fPermissionsByElementType_Computed()
            
            unasPermissionsForTRACatalogsByElementType[ unPathDelRaiz] = unasPermissionsByElementType
            
            
        return unasPermissionsByElementType
    

    
    
    # #############################################################


    security.declarePrivate( 'pClearPermissionsByElementType')
    def pClearPermissionsByElementType(self,):
        """Clear Security configuration specification by Type names.
        
        """
        
        unPathDelRaiz = self.fPathDelRaiz()
        if not unPathDelRaiz:
            return self
        
        
        unasPermissionsForTRACatalogsByElementType = TRAElemento_Permissions.gPermissionsForTRACatalogsByElementType
        
        if not unasPermissionsForTRACatalogsByElementType:
            return self
            
        try:    
            unasPermissionsForTRACatalogsByElementType.pop( unPathDelRaiz)
        except:
            None
            
        return self
    
    
    
    

    security.declarePrivate( 'pClearStateChangeActionRoles')
    def pClearStateChangeActionRoles(self,):
        """Clear Security configuration specification by Type names.
        
        """
        
        unPathDelRaiz = self.fPathDelRaiz()
        if not unPathDelRaiz:
            return self
        
        
        unasStateChangeActionRolesForTRACatalogs = TRAElemento_Permissions.gStateChangeActionRoles
        
        if not unasStateChangeActionRolesForTRACatalogs:
            return self
            
        try:    
            unasStateChangeActionRolesForTRACatalogs.pop( unPathDelRaiz)
        except:
            None
            
        return self
        
    

    
    

         
    
    
    # #############################################################
    """Lazy initialize Access Security configuration specification 
       Permissions by type
    
    """
       
    security.declarePrivate( 'fNewVoidPermissionsSpec')
    def fNewVoidPermissionsSpec( self, theAcquirePermission, theRoles):
        unaSpec = {
            'acquire_permissions':  theAcquirePermission,
            'roles':                theRoles,
        }
        return unaSpec
    
    
    
    
    
    security.declarePrivate( 'fPermissionsByElementType_Computed')
    def fPermissionsByElementType_Computed( self,):
        
        unCatalogo = self.getCatalogo()
        if unCatalogo == None:
            return {}
        
        
        
        unosAdditionalZopeRolesForTRARoles = { }
        
        unaConfiguracionPermissions = unCatalogo.fObtenerConfiguracion( cTRAConfiguracionAspecto_Permisos)
        if not( unaConfiguracionPermissions == None):
            unosAdditionalZopeRolesForTRARoles = unaConfiguracionPermissions.fAdditionalZopeRolesForTRARoles( )
       
            
            
        unasPermissionsByType = { }
    
        for unUseCaseName in cTRAUseCasesWithAbbreviatedPermissions.keys():
            unUseCaseSpec     = cTRAUseCasesWithAbbreviatedPermissions[ unUseCaseName]
            unosVerificables  = unUseCaseSpec[ 0]
            unosAdicionales   = unUseCaseSpec[ 1]
            
            for unVerificable in unosVerificables:
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
                   
                        
                        
        self.pOverridePermissionsByElementTypeWithConfiguration( unasPermissionsByType)
                        
        return  unasPermissionsByType                       
        

       
    
    
    
   
    
    
    security.declarePrivate( 'pOverridePermissionsByElementTypeWithConfiguration')
    def pOverridePermissionsByElementTypeWithConfiguration( self, thePermissionsByElementType=None):
        
        if not thePermissionsByElementType:
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
            
        unosNombresTipos = thePermissionsByElementType.keys()
        for unNombreTipo in unosNombresTipos:
            
            unasPermissionsForType = thePermissionsByElementType.get( unNombreTipo, None)
            if unasPermissionsForType:
                
                unasPermissions = unasPermissionsForType.keys()
                for unaPermission in unasPermissions:
                    
                    unaPermissionSpec = unasPermissionsForType.get( unaPermission, None)
                    
                    if unaPermissionSpec:
                        
                        unosRoles = unaPermissionSpec.get( 'roles', None)
                        if unosRoles:
                            
                            unosNuevosRoles = unosRoles.copy()
                            
                            for unRol in unosRoles:
                                
                                unosRolesAdicionales = unosAdditionalZopeRolesForTRARoles.get( unRol, None)
                                if unosRolesAdicionales:
                                    
                                    unosNuevosRoles = unosNuevosRoles.union( set( unosRolesAdicionales))
            
                            if not ( unosNuevosRoles == unosRoles):
                                unaPermissionSpec[ 'roles'] = unosNuevosRoles
                                
        return self
    
    
    
    
    
    
    
    
    
    
    
    
    # #############################################################
    """Translation Status Changes and roles allowed to transition Translations to the target Status
       Security configuration specification 

    """    



    security.declarePrivate( 'fStateChangeActionRoles')
    def fStateChangeActionRoles(self,):
        """Lazy initialize Access Security configuration specification by Type names.
        
        """
        
        unPathDelRaiz = self.fPathDelRaiz()
        if not unPathDelRaiz:
            return { }
        
        
        unasStateChangeActionRolesForTRACatalogs = TRAElemento_Permissions.gStateChangeActionRoles
        
        if not unasStateChangeActionRolesForTRACatalogs:
            
            unasStateChangeActionRolesForTRACatalogs = { }
            
            TRAElemento_Permissions.gStateChangeActionRoles = unasStateChangeActionRolesForTRACatalogs
            
            

        unasStateChangeActionRoles = unasStateChangeActionRolesForTRACatalogs.get( unPathDelRaiz, None)
        
        if not unasStateChangeActionRoles:
            
            unasStateChangeActionRoles = self.fStateChangeActionRoles_Computed()
            
            unasStateChangeActionRolesForTRACatalogs[ unPathDelRaiz] = unasStateChangeActionRoles
            
            
        return unasStateChangeActionRoles
    
    
    
    
    def fStateChangeActionRoles_Computed( self,):
        
        
        someStateChangeActionRoles = cStateChangeActionRoles.copy()

        for aSourceState in someStateChangeActionRoles.keys():
            
            someTargetStatesAndRoles = someStateChangeActionRoles.get( aSourceState, None)
            if someTargetStatesAndRoles:
                someTargetStatesAndRoles = someTargetStatesAndRoles.copy()
                someStateChangeActionRoles[ aSourceState] = someTargetStatesAndRoles
            
            
                for aTargetState in someTargetStatesAndRoles.keys():
                    someRoles = someTargetStatesAndRoles.get( aTargetState, None)
                    if someRoles:
                        someRoles = someRoles[:]
                        someTargetStatesAndRoles[ aTargetState] = someRoles
                

        self.pOverrideStateChangeActionRolesWithConfiguration( someStateChangeActionRoles)
        
        return someStateChangeActionRoles
        
    
    
        
    
    security.declarePrivate( 'pOverrideStateChangeActionRolesWithConfiguration')
    def pOverrideStateChangeActionRolesWithConfiguration( self, theStateChangeActionRoles=None):
        
        if not theStateChangeActionRoles:
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
            
        
        for aSourceState in theStateChangeActionRoles.keys():
            
            someTargetStatesAndRoles = theStateChangeActionRoles.get( aSourceState, None)
            if someTargetStatesAndRoles:

                for aTargetState in someTargetStatesAndRoles.keys():
                    someRoles = someTargetStatesAndRoles.get( aTargetState, None)
                    if someRoles:
                            
                        someRolesSet    = set( someRoles)
                        unosNuevosRoles = someRolesSet.copy()
                        
                        for unRol in someRoles:
                            
                            unosRolesAdicionales = unosAdditionalZopeRolesForTRARoles.get( unRol, None)
                            if unosRolesAdicionales:
                                
                                unosNuevosRoles = unosNuevosRoles.union( set( unosRolesAdicionales))
        
                        if not ( unosNuevosRoles == someRolesSet):
                            someTargetStatesAndRoles[ aTargetState] = list( unosNuevosRoles)
                                
        return self
    
    
    
    
    
    
    
    
    
    
    
        
    
    

   
    


    
    # #############################################################
    """Access acquisition of Role assignment to users and groups 
       Security configuration specification 

    """
       
  
    security.declarePrivate( 'fAcquireRoleAssignmentsElement')
    def fAcquireRoleAssignmentsElement(self, theElement=None):

        unElement = theElement
        if unElement == None:
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
    def fIsAcquiringRoleAssignments(self, theElement=None, thePloneUtilsTool=None):
            
        unElement = theElement
        if  unElement == None:
            unElement = self
            
        aPloneUtilsTool = thePloneUtilsTool
        if aPloneUtilsTool == None:
            aPloneUtilsTool = self.getPloneUtilsToolForRoles()
        if aPloneUtilsTool == None:
            return False
        
        return aPloneUtilsTool.isLocalRoleAcquired( unElement)    
    
    
    
    
    
    security.declarePrivate( 'fSetAcquiringRoleAssignments')
    def fSetAcquiringRoleAssignments(self, theElement=None, theMustAcquire=True):
            
        unElement = theElement
        if  unElement == None:
            unElement = self
            
        aPloneUtilsTool = self.getPloneUtilsToolForRoles()
        if not aPloneUtilsTool:
            return False
        
        return aPloneUtilsTool.acquireLocalRoles( unElement, theMustAcquire)    
    
    
    
        
    

    
    # #############################################################
    """Security configuration  
       Initialize an object's permissions upon creation
          according to the permissions specification
     Shall be invoked from the manage_afterAdd delegation of 
       all objects except TRACadena and TRATraduccion
    
       Not to be used with TRACadena and TRATraduccion
          that are set up during import, where the permissions to set 
          are known beforehand for the thousandas of instances to create
       
    """
                

    
    security.declarePrivate( 'pSetPermissions')
    def pSetPermissions(self, theAdditionalParams=None):
        self.fSetPermissions( theAdditionalParams=theAdditionalParams)
        return self
    
    
    
    security.declarePrivate( 'fSetPermissions')
    def fSetPermissions(self, theAdditionalParams=None, thePermissionsForElement=None):
 
        unasPermissionsSpec = thePermissionsForElement   
        if not unasPermissionsSpec:
            unasPermissionsSpec = self.fPermissionsForElement( self)   
        if not unasPermissionsSpec:
            return False
        
        # It is used to unset the 'Copy or Move' permission
        # but it is cheked when the id of the temporary element is changed upon saving the id/title imput form.
        # We must detect whether the object is temporaty
        #
        #if not ( 'portal_factory' in self.getPhysicalPath()):    
            #for unaPermission in cPermissionsToDenyEverywhereToEverybody:
                #self.manage_permission( unaPermission, roles=[], acquire=False)
            
            
        for unaPermission in unasPermissionsSpec.keys():
            if unaPermission:
                
                unaPermissionSpec        = unasPermissionsSpec[ unaPermission]
                unAcquire                = unaPermissionSpec[ 'acquire_permissions'] 
                unosRoles                = list( unaPermissionSpec[ 'roles'])
            
                self.manage_permission( unaPermission, roles=unosRoles, acquire=unAcquire)
                
                
                
        unasPermissionsToReset = ( theAdditionalParams or {}).get( 'permissions_to_reset', [])
        if unasPermissionsToReset:     
            for unaPermission in unasPermissionsToReset:
                if unaPermission:
                    if not unasPermissionsSpec.has_key( unaPermission):
                        self.manage_permission( unaPermission, roles=[], acquire=False)
                    
                
    
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
                                
                
        return True
    
    

    
    
    

    
        
 
    # #############################################################

        
         
    security.declarePrivate( 'fCheckPermissionSpecificationCompliance')
    def fCheckPermissionSpecificationCompliance(self, 
        theElement                =None, 
        theElementPermissionsSpec =None,):
        
        anElement = theElement
        if anElement == None:
            anElement = self
        
        anElementPermissionsSpec = theElementPermissionsSpec
        if anElementPermissionsSpec == None:
            anElementPermissionsSpec = self.fPermissionsForElement( self)

        
        
        unasPermissionSettings = anElement.permission_settings() # Defined in Zope/lib/python/AccessControl/Role.py
        if not unasPermissionSettings:
            return False
        unasPermissionSettingsDict = dict( [ [aPermSetting.get( 'name', ''), aPermSetting,] for aPermSetting in unasPermissionSettings] )
        
        unosValidRoles = anElement.valid_roles() # Defined in Zope/lib/python/AccessControl/Role.py
        if not unosValidRoles:
            return False
        unosValidRoles = list( unosValidRoles)
        unosValidRolesSet = set( unosValidRoles)
        unosValidRolesIndexes = dict( [ [ unosValidRoles[ unValidRoleIndex], unValidRoleIndex ] for unValidRoleIndex  in  range( len( unosValidRoles))])
        
        
        somePermissions = anElementPermissionsSpec.keys()
        for aPermission in somePermissions:
            
            aPermissionSpec = anElementPermissionsSpec.get( aPermission, None)
            if not aPermissionSpec:
                return False
            
            aMustAcquirePermission = aPermissionSpec.get( 'acquire_permissions', False)
            someRoles           = aPermissionSpec.get( 'roles',               None)
            
            if set( someRoles).difference( unosValidRolesSet):
                return False   
            

            aPermissionSetting = unasPermissionSettingsDict.get( aPermission, None)
            if not aPermissionSetting:
                return False
            
            aPermissionSettingAcquire = aPermissionSetting.get( 'acquire', None) == 'CHECKED'
            if( aMustAcquirePermission and not aPermissionSettingAcquire) or ( ( not aMustAcquirePermission)  and aPermissionSettingAcquire):
                return False
            
            
            
            aPermissionSettingRoles = aPermissionSetting.get( 'roles', None)
            
            for unRol in cPreferredRolesOrder:
                unIndexRol = unosValidRolesIndexes.get( unRol, -1)
                if unIndexRol < 0:
                    return False
                
                unRoleSetting = aPermissionSettingRoles[ unIndexRol]
                
                unPermissionGrantedToRole = unRoleSetting.get( 'checked', '') == 'CHECKED'
                unMustBeGrantedToRole = unRol in someRoles
                
                if( unMustBeGrantedToRole and not unPermissionGrantedToRole) or ( ( not unMustBeGrantedToRole)  and unPermissionGrantedToRole):
                    return False
                
                
        aMustAcquireRoleAssignments   = self.fAcquireRoleAssignmentsElement( anElement)
        aIsAcquiringRoleAssignments   = self.fIsAcquiringRoleAssignments(    anElement, ) 
        
        if( aMustAcquireRoleAssignments and not aIsAcquiringRoleAssignments) or ( ( not aMustAcquireRoleAssignments)  and aIsAcquiringRoleAssignments):
            return False
            
        return True
    
    
    
    
    
    
    
    security.declarePrivate( 'fPermissionsPermittedReport')
    def fPermissionsPermittedReport(self, 
        thePermissionsToCheck =None, ):
        """Security reporting utility : Has the user the specified permissions ?.
        
        """
        aPermissionsPermittedReport = { }

        if not thePermissionsToCheck:
            return aPermissionsPermittedReport

        aPortalMembershipTool = self.getPortalMembershipTool()
        if aPortalMembershipTool == None:
            return aPermissionsPermittedReport        
                
        for aPermission in thePermissionsToCheck:
            
            aPermitted = aPortalMembershipTool.checkPermission( aPermission, self)      
            
            aPermissionsPermittedReport[ aPermission] = aPermitted
        
        return aPermissionsPermittedReport
        
     
    
    
    

    security.declarePrivate( 'fCheckElementPermission')
    def fCheckElementPermission(self, theObject, thePermissionsToCheck, thePermissionsCache=None, thePortalMembershipTool=None ):
        """Security check utility : Has the user ALL of the specified permissions ?.
        
        """
        if theObject == None:
            return False
        
        if not thePermissionsToCheck:
            return True
        
        aPortalMembershipTool = thePortalMembershipTool
        aPermissionsToCheck   = thePermissionsToCheck
        
        if not ( aPermissionsToCheck.__class__.__name__ in [ 'list', 'tuple', 'set',]):
            aPermissionsToCheck = [ [ aPermissionsToCheck, ], ]
        else:
            aPermissionsToCheck = [ ]
            for aPermission in thePermissionsToCheck:
                if aPermission.__class__.__name__ in [ 'list', 'tuple', 'set',]:
                    aPermissionsToCheck.append( list( aPermission))
                else:
                    aPermissionsToCheck.append( [ aPermission,])
        

        unaObjectKey = None
        try:
            unaObjectKey = theObject.UID()
        except:
            None
        
        unCachedPermissions = None
        if thePermissionsCache and unaObjectKey:
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
                            aPortalMembershipTool = self.getPortalMembershipTool()
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
    """Rendering utilities

    """
    
    def fRenderPermissionsByElementType(self,):
        unOutput = StringIO()
        
        unasPermissionsByElementType = self.fPermissionsByElementType()
        
        unosTypesNames = sorted( unasPermissionsByElementType.keys())   
        
        unOutput.write( "\n\nRender Permissions By Element Type for %d types\n" % len( unosTypesNames))
        
        for unTypeName in unosTypesNames:
            unOutput.write( "\n%sType %s\n" % ( cIndent, unTypeName, ))
    
            unasPermissionsSpec = unasPermissionsByElementType.get(unTypeName, None)   
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
    """Security configuration rendering utility 

    """
    
    
    security.declareProtected( permissions.View, 'fRenderUserAndRoles_HTMLcollapsible')
    def fRenderUserRolesAndPermissions_HTMLcollapsible(self, theCollapse=True):
        return self.fText2HTML_collapsible( self.fRenderUserRolesAndPermissions(), 'User, Roles and Permissions', 'csect_UserRolesAndPermissions', theCollapse)
    
    
    
       
    security.declareProtected( permissions.View, 'fRenderUserRolesAndPermissions')
    def fRenderUserRolesAndPermissions(self, theCollapse=True):
        
        unUser    = self.fGetRequestingUserObject()
        unosRoles = self.fGetRolesForUserObject( unUser, self)

        aPortalMembershipTool = self.getPortalMembershipTool() 
        
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
    
    
    
        


   
    
    
    
    # ########################################################################
    """Role queries:  is the connected user in a/some specific role/s ?

    """
    
    
    
    security.declareProtected( permissions.View, 'fOverrideRolesWithConfiguration')
    def fOverrideRolesWithConfiguration(self, theRoles):
        
        if not theRoles:
            return set()
        
        unosInitialManagerRoles = set( theRoles).copy()
        
        unosOverrideManagerRoles = unosInitialManagerRoles.copy()
        
        unCatalogo = self.getCatalogo()
        if not( unCatalogo == None):
        
            unosAdditionalZopeRolesForTRARoles = { }
            
            unaConfiguracionPermissions = unCatalogo.fObtenerConfiguracion( cTRAConfiguracionAspecto_Permisos)
            if not( unaConfiguracionPermissions == None):
            
                unosAdditionalZopeRolesForTRARoles = unaConfiguracionPermissions.fAdditionalZopeRolesForTRARoles( )
                if unosAdditionalZopeRolesForTRARoles:
                    
                    for unRol in unosInitialManagerRoles:
                        unosAdditionalRoles = unosAdditionalZopeRolesForTRARoles.get( unRol, None)
                        if unosAdditionalRoles:
                            unosOverrideManagerRoles = unosOverrideManagerRoles.union( set( unosAdditionalRoles))
                            
        return unosOverrideManagerRoles
      
            
 
        
    security.declareProtected( permissions.View, 'fRoleQuery_IsManager')
    def fRoleQuery_IsManager(self, theElement=None):
        
        unosRoles = self.fOverrideRolesWithConfiguration( cTRAManagerRoles)
        
        return self.fRoleQuery_IsAnyRol( unosRoles, theElement)
      
    
    
    
    
    security.declareProtected( permissions.View, 'fRoleQuery_IsCoordinator')
    def fRoleQuery_IsCoordinator(self, theElement=None):
        
        unosRoles = self.fOverrideRolesWithConfiguration( [ cTRACoordinator_role,])
        
        return self.fRoleQuery_IsAnyRol( unosRoles, theElement)
      
    
    
    security.declareProtected( permissions.View, 'fRoleQuery_IsCoordinatorOrDeveloper')
    def fRoleQuery_IsCoordinatorOrDeveloper(self, theElement=None):
        
        unosRoles = self.fOverrideRolesWithConfiguration( [ cTRACoordinator_role , cTRADeveloper_role, ])
        
        return self.fRoleQuery_IsAnyRol( unosRoles, theElement)
      
    
    
    security.declareProtected( permissions.View, 'fRoleQuery_IsDeveloper')
    def fRoleQuery_IsDeveloper(self, theElement=None):
        
        unosRoles = self.fOverrideRolesWithConfiguration( [ cTRADeveloper_role,])
        
        return self.fRoleQuery_IsAnyRol( unosRoles, theElement)
      
    
        
        
    security.declareProtected( permissions.View, 'fRoleQuery_IsManagerOrCoordinator')
    def fRoleQuery_IsManagerOrCoordinator(self, theElement=None):
        
        unosRoles = self.fOverrideRolesWithConfiguration( cTRAManagerRoles + [ cTRACoordinator_role, ])
        
        return self.fRoleQuery_IsAnyRol( unosRoles, theElement)
      
        
    
    
    security.declareProtected( permissions.View, 'fRoleQuery_IsCreatorOrManagerOrCoordinator')
    def fRoleQuery_IsCreatorOrManagerOrCoordinator(self, theElement=None):
        
        unosRoles = self.fOverrideRolesWithConfiguration( cTRAManagerRoles + [ cTRACreator_role, cTRACoordinator_role, ])
        
        return self.fRoleQuery_IsAnyRol( unosRoles, theElement)
      
                
    
    
    security.declareProtected( permissions.View, 'fRoleQuery_IsReviewer')
    def fRoleQuery_IsReviewer(self, theElement=None):
        
        unosRoles = self.fOverrideRolesWithConfiguration( [ cTRAReviewer_role,])
        
        return self.fRoleQuery_IsAnyRol( unosRoles, theElement)
     
    
    
    
    security.declareProtected( permissions.View, 'fRoleQuery_IsTranslator')
    def fRoleQuery_IsTranslator(self, theElement=None):
        
        unosRoles = self.fOverrideRolesWithConfiguration( [ cTRATranslator_role,])
        
        return self.fRoleQuery_IsAnyRol( unosRoles, theElement)
      
    
    security.declareProtected( permissions.View, 'fRoleQuery_IsVisitor')
    def fRoleQuery_IsVisitor(self, theElement=None):
        
        unosRoles = self.fOverrideRolesWithConfiguration( [ cTRAVisitor_role,])
        
        return self.fRoleQuery_IsAnyRol( unosRoles, theElement)
      
      
    
    
    
    
    
    
    security.declarePrivate( 'fGetElementRoles')
    def fGetElementRoles(self, theObject, theRolesCache=None ):
        """Get the roles held by the connected user at theObject.
        
        """
      
        if theObject == None:
            return False
           
        unUser = self.fGetRequestingUserObject()
        if not unUser:
            return []
        
        unaObjectKey = None
        try:
            unaObjectKey = theObject.UID()
        except:
            None
        
        unCachedRoles = None
        
        unosCachedRoles    = None
        if not ( theRolesCache == None) and unaObjectKey:        
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
        
        if theObject == None:
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
        
        unaObjectKey = None
        try:
            unaObjectKey = theObject.UID()
        except:
            None
            
        
        
        unosCachedRoles    = None
        unosHeldRoles      = None
        if not ( theRolesCache == None) and unaObjectKey:        
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

    
    
       
    
    

    security.declareProtected( permissions.View, 'fInheritedLocalRoles')
    def fInheritedLocalRoles( self,):
    
        aPloneUtilsTool = self.getPloneUtilsToolForRoles()
        if aPloneUtilsTool == None:
            return False
    
        return aPloneUtilsTool.getInheritedLocalRoles( self)
        

    
    
    security.declareProtected( permissions.View, 'fIsLocalRoleAcquired')
    def fIsLocalRoleAcquired( self,):
    
        aPloneUtilsTool = self.getPloneUtilsToolForRoles()
        if aPloneUtilsTool == None:
            return False
    
        return aPloneUtilsTool.isLocalRoleAcquired( self)
    
    
    
    

    security.declareProtected( permissions.View, 'fLocalRolesForUserId')
    def fLocalRolesForUserId( self, theUserId=None):
        if not theUserId:
            return []
        
        return self.get_local_roles_for_userid( theUserId)
  
    
    
           

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
            
        todosRolesPoseidos = set( self.fGetRequestingUserRoles( theElement))
        
        unosRoles = set( unosRolesUsuario).intersection(  todosRolesPoseidos)
        
        return unosRoles
    
              
              


    security.declarePublic( 'fGetRequestingUserRoles')
    def fGetRequestingUserRoles(self, theElement=None):
        unElement = theElement
        if unElement == None:
            unElement = self
        
        unUser = self.fGetRequestingUserObject()
        if not unUser:
            return []
        
        unosRoles = self.fGetRolesForUserObject( unUser, unElement)
        return unosRoles
    

    
    security.declarePrivate( 'fGetRequestingUserObject')
    def fGetRequestingUserObject(self):

        unUser = self.fHTTPRequest_get( "AUTHENTICATED_USER", None)
        return unUser

    
    
    security.declarePrivate( 'fGetRolesForUserObject')
    def fGetRolesForUserObject(self, theUserObject, theElement):
        if not theUserObject or ( theElement == None):
            return set()
        unosRoles = theUserObject.getRolesInContext( theElement)
        if not unosRoles:
            return set()
        return set( unosRoles)
    


    
    
    
    
    
        
    security.declarePrivate( 'fApplicationRolesAndRoleKinds')
    def fApplicationRolesAndRoleKinds(self, ):
        """Deep copy the array, to avoid clients modifiying the constant.
        
        """
        
        if not cTRAApplicationRolesAndRoleKinds:
            return []
        
        unosRolesAndKinds = [ ]
        for someRolesAndKind in cTRAApplicationRolesAndRoleKinds:
            unosRolesAndKinds.append( [ someRolesAndKind[0][:], someRolesAndKind[1],])

        return unosRolesAndKinds
    
    
    
    
   