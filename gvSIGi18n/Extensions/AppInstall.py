# -*- coding: utf-8 -*-
#
# File: Install.py
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



from StringIO import StringIO

from Products.CMFCore.utils import getToolByName

from Products.gvSIGi18n.TRARoles                            import TRARoles_list
from Products.gvSIGi18n.TRAArchetypesNotInPortalCatalog     import cTRAArchetypeNames_NotInPortalCatalog

def install(self):
    unOutput = StringIO()

    """#########################################
    Create application specific roles
    """
    unPortalTool = getToolByName(self,'portal_url', None)
    if not unPortalTool:
        unOutput.write( 'ERROR: Could not find tool portal_url\n' )
    else:
        unPortal = unPortalTool.getPortalObject()
        if not unPortal:
            unOutput.write( 'ERROR: Could not find portal object\n' )
        else:
            someExistingRoles = unPortal.userdefined_roles()
            #someExistingRoles = list( unPortal.__ac_roles__)    
            someNewRoles      = list( someExistingRoles)[:]  
            someAddedRoles    = []
            
            unRolesChanged = False
            for unRol in TRARoles_list:
                if not ( unRol in someExistingRoles):
                    someNewRoles.append(unRol)
                    someAddedRoles.append(unRol)
                    unPortal._addRole( unRol)
                    unRolesChanged = True
                    
            if unRolesChanged:
                #unPortal.__ac_roles__ = tuple( someNewRoles)
                unOutput.write( 'Existing Roles: %s\nAdded Roles: %s\n' % ( ' '.join( someExistingRoles), ' '.join( someAddedRoles)))
            else:
                unOutput.write( 'Existing Roles: %s\n' % ' '.join( someExistingRoles))
                 
        
    """# #########################################
    Configure archetpe_tool to avoid including certain classes when portal_catalog is reconstructed
    """
    someArchetypeNamesAlreadyUnmappedFromPortalCatalog = []
    someArchetypeNamesUnmappedFromPortalCatalog = []
    
    unArchetypeTool = getToolByName( self, 'archetype_tool', None)
    if not unArchetypeTool:
        unOutput.write( 'ERROR: Could not find tool archetype_tool\n' )
    else:
        if cTRAArchetypeNames_NotInPortalCatalog:
            for unArchetypeName in cTRAArchetypeNames_NotInPortalCatalog:
                someCatalogsForType = unArchetypeTool.getCatalogsByType( unArchetypeName) 
                if someCatalogsForType:
                    unArchetypeTool.setCatalogsByType( unArchetypeName, [])
                    someArchetypeNamesUnmappedFromPortalCatalog.append( unArchetypeName)
                else:
                    someArchetypeNamesAlreadyUnmappedFromPortalCatalog.append( unArchetypeName)

            if someArchetypeNamesAlreadyUnmappedFromPortalCatalog:
                unOutput.write( 'Types Already unmapped from portal_catalog %s\n' % ' '.join( someArchetypeNamesAlreadyUnmappedFromPortalCatalog))
                
            if someArchetypeNamesUnmappedFromPortalCatalog:
                unOutput.write( 'Types Just unmapped from portal_catalog %s\n' % ' '.join( someArchetypeNamesUnmappedFromPortalCatalog))
        else:
            unOutput.write( 'No Types to unmap from portal_catalog\n')
            
    return unOutput.getvalue()







#def install(self):
    #unOutput = StringIO()

    #"""#########################################
    #Create application specific roles
    #"""
    #unPortalTool = getToolByName(self,'portal_url', None)
    #if not unPortalTool:
        #unOutput.write( 'ERROR: Could not find tool portal_url\n' )
    #else:
        #unPortal = unPortalTool.getPortalObject()
        #if not unPortal:
            #unOutput.write( 'ERROR: Could not find portal object\n' )
        #else:
            #someExistingRoles = list( unPortal.__ac_roles__)    
            #someNewRoles      = list( someExistingRoles)[:]  
            #someAddedRoles    = []
            
            #unRolesChanged = False
            #for unRol in TRARoles_list:
                #if not ( unRol in someExistingRoles):
                    #someNewRoles.append(unRol)
                    #someAddedRoles.append(unRol)
                    #unRolesChanged = True
                    
            #if unRolesChanged:
                #unPortal.__ac_roles__ = tuple( someNewRoles)
                #unOutput.write( 'Existing Roles: %s\nAdded Roles: %s\n' % ( ' '.join( someExistingRoles), ' '.join( someAddedRoles)))
            #else:
                #unOutput.write( 'Existing Roles: %s\n' % ' '.join( someExistingRoles))
                 
        
    #"""# #########################################
    #Configure archetpe_tool to avoid including certain classes when portal_catalog is reconstructed
    #"""
    #someArchetypeNamesAlreadyUnmappedFromPortalCatalog = []
    #someArchetypeNamesUnmappedFromPortalCatalog = []
    
    #unArchetypeTool = getToolByName( self, 'archetype_tool', None)
    #if not unArchetypeTool:
        #unOutput.write( 'ERROR: Could not find tool archetype_tool\n' )
    #else:
        #if cTRAArchetypeNames_NotInPortalCatalog:
            #for unArchetypeName in cTRAArchetypeNames_NotInPortalCatalog:
                #someCatalogsForType = unArchetypeTool.getCatalogsByType( unArchetypeName) 
                #if someCatalogsForType:
                    #unArchetypeTool.setCatalogsByType( unArchetypeName, [])
                    #someArchetypeNamesUnmappedFromPortalCatalog.append( unArchetypeName)
                #else:
                    #someArchetypeNamesAlreadyUnmappedFromPortalCatalog.append( unArchetypeName)

            #if someArchetypeNamesAlreadyUnmappedFromPortalCatalog:
                #unOutput.write( 'Types Already unmapped from portal_catalog %s\n' % ' '.join( someArchetypeNamesAlreadyUnmappedFromPortalCatalog))
                
            #if someArchetypeNamesUnmappedFromPortalCatalog:
                #unOutput.write( 'Types Just unmapped from portal_catalog %s\n' % ' '.join( someArchetypeNamesUnmappedFromPortalCatalog))
        #else:
            #unOutput.write( 'No Types to unmap from portal_catalog\n')
            
    #return unOutput.getvalue()

