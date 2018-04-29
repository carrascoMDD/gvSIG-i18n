# -*- coding: utf-8 -*-
#
# File: TRARenderSecurity.py
#
# Copyright (c) 2008, 2009,2010 by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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


from StringIO import StringIO

from Products.CMFCore.utils import getToolByName

from Products.gvSIGi18n.TRAElemento_Constants import *

from Products.gvSIGi18n.TRAElemento_Permission_Definitions import cPreferredPermissions, cPreferredRolesOrder, cTRAPreferredUserGroupsOrder

from Products.gvSIGi18n.TRAElemento_Permission_Definitions import cTRAUseCaseNames, cRuleAssessmentMessages, cPermissionRuleNameDefault

from Products.gvSIGi18n.TRAElemento_Permission_Definitions import cUseCaseRuleMode_ForAll, cUseCaseRuleMode_Filter, cUseCaseRuleMode_EmptyOrAll, cUseCaseRuleMode_EmptyOrAny



# #########################################
#   Rendering utilities
# #########################################






# #########################################
#   Render Permission Definitions
# #########################################



def TRARenderPermissionDefinitions( theContextualObject, theCollapsible=False, theCollapse=True):

    if not theContextualObject:
        return "Parameter missing: contextual object"
    
    unasPermissionsByElementType = theContextualObject.getCatalogo().fPermissionsByElementType()
    if not unasPermissionsByElementType:
        return "Configuration missing: PermissionsByElementType"
 
      
    unOutput = StringIO()
    
    unOutput.write( """
        <tr>
            <th colspan="3" />
            <th colspan="%d" align="center"><strong>Roles</strong></th>
        </tr>
        <tr>
            <th align="left">Type</th>
            <th align="left">Permission</th>
            <th align="center">Acquire</th>
        \n""" % len( cPreferredRolesOrder)
    )
    for unRole in cPreferredRolesOrder:
        unOutput.write( """
            <th align="center">%s</th>
            \n""" % unRole
        )
    unOutput.write( """
        </tr>            
        \n"""
    )
    unHeadersRow = unOutput.getvalue()
    
    unPermittedBlock ="""
        <img alt="Permitted" src="%s/tra_permitida.gif" title="Permitted" />
        \n""" % theContextualObject.absolute_url()

    unForbiddenBlock ="""
        <img alt="Forbidden" src="%s/tra_prohibida.gif" title="Forbidden" />
        \n""" % theContextualObject.absolute_url()

    
    unOutput = StringIO()

    unasClassesRow =[ 'odd', 'even', ]

    unOutput.write( """
        <br/>
        <table class="listing nosort"  id="sect_PermissionDefinitions" summary="Permissions By Element Type">
            <thead>
                <tr>
                    <th colspan="%d" align="left">
                        <strong>Permission Specifications for %d types</strong>
                        <p class="formHelp">Permissions that "SHOULD" be granted, as specified - to compare with actual permissions held by connected users, according to the roles held at each given element.</p>
                    </th>
                </tr>
                %s
            </thead>
            <tbody>
        \n""" % ( 
            3 + len( cPreferredRolesOrder),
            len( cPreferredTypesOrder), 
            unHeadersRow)
        )

    someSortedPermissions = sorted( cPreferredPermissions)
    
    for unTypeName in cPreferredTypesOrder:
        if not unTypeName == cPreferredTypesOrder[ 0]:
            unOutput.write( """
                %s
                \n""" % (
                unHeadersRow,
            ))
            
        unOutput.write( """
            <tr class="%s">
                <td align="left">%s</td>
                \n""" % (
            unasClassesRow[ 0],
            unTypeName,
        ))

        unasPermissionsSpec = unasPermissionsByElementType.get( unTypeName, None)   
        if not unasPermissionsSpec:
            unOutput.write( """
                <td colspan ="%d">---</td>
                \n""" %
                2+ len( cPreferredRolesOrder)   
             )
        else:
            unRowIndex = 1
            for unaPermissionIndex in range( len( someSortedPermissions)):
                unaPermission = someSortedPermissions[ unaPermissionIndex]
                if not( unaPermission == someSortedPermissions[ 0]):
                    unOutput.write( """
                        <tr class="%s">
                            <td/>
                        \n""" % 
                        unasClassesRow[ unaPermissionIndex % 2],
                    )
                unaPermissionSpec = unasPermissionsSpec.get( unaPermission, None)
                if not unaPermissionSpec:
                    unOutput.write( """
                            <td >%s</td>
                            <td colspan ="%d">---</td>
                        </tr>
                        \n""" % (
                        unaPermission,
                        1+ len( cPreferredRolesOrder)
                    ))
                else:
                    unAcquire         = unaPermissionSpec[ 'acquire_permissions'] 
                    unosRoles         = unaPermissionSpec[ 'roles']
     
                    unOutput.write( """
                        <td align="left">%s</td>
                        \n""" % unaPermission
                    )
                    
                    
                    unOutput.write( """
                        <td align="center">
                            %s
                        </td>
                        \n""" % ( ( unAcquire and unPermittedBlock) or unForbiddenBlock)
                    )
                    for unRole in cPreferredRolesOrder:
                        unOutput.write( """
                            <td align="center">
                                %s
                            </td>
                            \n""" % (( ( unRole in unosRoles) and unPermittedBlock) or unForbiddenBlock)
                        )
               
                    unOutput.write( """
                        </tr>
                        \n""" 
                    )
            
            
    unOutput.write( """
            </tbody>
        </table>
        <br/>
        \n""" 
    )
    
    
    unPermissionsRendering = unOutput.getvalue()
    
    if not theCollapsible:
        return unPermissionsRendering
    
    return fRenderCollapsible( unPermissionsRendering, "Expected permission specifications by element Type", 'csect_PermissionsByElementType', theCollapse)

    











# #########################################
#   Render Logged Used Here
# #########################################



def TRARenderLoggedUsedHere( theContextualObject, theCollapsible=False, theCollapse=True):

    if not theContextualObject:
        return "Parameter missing: contextual object"
      
    unaRequest = theContextualObject.REQUEST
    if not unaRequest:
        return 'No HTTP Request ! Can not learn about currently logged user.'
    
    unOutput = StringIO()
      
    unUser    = unaRequest.get("AUTHENTICATED_USER", None)
    unosRoles = unUser.getRolesInContext( theContextualObject)

    aPortalMembershipTool = getToolByName( theContextualObject, 'portal_membership') 
    

    
    unPermittedBlock ="""
        <img alt="Permitted" src="%s/tra_permitida.gif" title="Permitted" />
        \n""" % theContextualObject.absolute_url()

    unForbiddenBlock ="""
        <img alt="Forbidden" src="%s/tra_prohibida.gif" title="Forbidden" />
        \n""" % theContextualObject.absolute_url()    
    
    
 
    if unUser:
        unUserName = unUser.getUserName()
    else:
        unUserName = 'unknown'
        
    unElementPath       = '/'.join( theContextualObject.getPhysicalPath()[2:])
    unElementClassName  = theContextualObject.__class__.__name__
    

    
    
    
    unOutput = StringIO()
    
    unOutput.write( """
        <br/>
        <p><strong>Logged User %s</strong></p>
        \n""" % unUserName
    )
    
    unOutput.write( """
        <br/>
        <p><strong>Is Acquiring Role Assignments at %s %s: %s</strong></p>
        \n""" % ( unElementClassName, unElementPath, ( theContextualObject.fIsAcquiringRoleAssignments(    theContextualObject) and 'True') or 'False')
    )
     
    unOutput.write( """
        <!-- =====================================
        SECTION Logged User Roles Here
        ===================================== 
        -->
        
        <table class="listing nosort"  id="sect_LoggedUserRolesHere" summary="Logged User Roles Here">
            <thead>
                <tr><th colspan="%d" align="left"><font size="2"><strong>Roles held at %s<br/>%s</strong></font></th></tr>

        \n""" % ( len( cPreferredRolesOrder), unElementClassName, unElementPath,))
        
    unOutput.write( """
        <tr>
        \n""")
    for unRole in cPreferredRolesOrder:
        unOutput.write( """
            <th align="center"><strong>%s</strong></th>
            \n""" % unRole
        )
    unOutput.write( """
            </tr>            
        </thead>
        <tbody>
        \n"""
    )
                
        
    for unRole in cPreferredRolesOrder:
        unOutput.write( """
            <td align="center">
                %s
            </td>
            \n""" % (( ( unRole in unosRoles) and unPermittedBlock) or unForbiddenBlock)
        )

    unOutput.write( """
        </tr>
        \n""" 
    )
            
            
    unOutput.write( """
            </tbody>
        </table>
        \n""" 
    )
            
    
    
    
    
       
    unOutput.write( """
        <br/>
        <!-- =====================================
        SECTION Logged User Permissions Here
        ===================================== 
        -->
        
        <table class="listing nosort"  id="sect_LoggedUserPermissionsHere" summary="Logged User Permissions Here">
            <thead>
                <tr><th colspan="2" align="left"><font size="2"><strong>Permissions at %s<br/>%s</strong></font></th></tr>                
                <tr>
                    <th  align="left"><strong>Permission</strong></th>
                    <th  align="center"><strong>Permitted</strong></th>
                </tr>
            </thead>
            <tbody>
        \n"""  % ( 
        unElementClassName, 
        unElementPath,
    ))
    
    unasClassesRow =[ 'odd', 'even', ]

    somePermissions = sorted( cPreferredPermissions)
    
    for unaPermissionIndex in range( len( somePermissions)):
        unaPermission = somePermissions[ unaPermissionIndex]
        aPermitted = aPortalMembershipTool.checkPermission( unaPermission, theContextualObject)
        unOutput.write( """
            <tr class="%(row-class)s">
                <td align="left">%(permission)s</td>
                <td align="center">%(permitted-block)s</td>    
            </tr>
            \n""" % {
            'row-class':        unasClassesRow[ unaPermissionIndex % 2],
            'permission':       unaPermission,
            'permitted-block':  ( aPermitted and unPermittedBlock)  or  unForbiddenBlock,
        })
    
    unOutput.write( """
            </tbody>
         </table>
        \n"""
    )
    
    
    
    
    
    
    
    
      
    unOutput.write( """
        <br/>
        <!-- =====================================
        SECTION Logged User    Use Cases Here
        ===================================== 
        -->
        
        <table class="listing nosort"  id="sect_LoggedUserUseCasesHere" summary="Logged User Use Cases Here">
            <thead>
                <tr><th colspan="3" align="left"><font size="2"><strong>Use Cases available at %s<br/>%s</strong></font></th></tr>                
                <tr>
                    <th  align="left"><strong>Use Case</strong></th>
                    <th  align="center"><strong>Permitted</strong></th>
                    <th  align="center"><strong>time to assess</strong></th>
                </tr>
            </thead>
            <tbody>
        \n"""  % ( 
        unElementClassName, 
        unElementPath,
    ))
    
    unasClassesRow =[ 'odd', 'even', ]

    
    unosUseCaseResults = theContextualObject.fUseCaseAssessment_AvailableUseCasesOn( 
        theContextualObject, 
        theUseCaseNamesToAssess     = [], 
        theRulesToCollect           = True,
        thePermissionsCache         = None,
        theRolesCache               = None,
        theParentExecutionRecord    = None,
    ) 

    someUseCaseNames = sorted( cTRAUseCaseNames)
    for unUseCaseIndex in range( len( someUseCaseNames)):
        unUseCaseName = someUseCaseNames[ unUseCaseIndex]
        unUseCaseResult = unosUseCaseResults.get( unUseCaseName, None) 
        if not unUseCaseResult:
            unOutput.write( """
                <tr class="%(row-class)s">
                    <td align="left">%(use-case-name)s</td>
                    <td colspan="2" align="center">- unknown -</td>    
                </tr>
                \n""" % {
                'row-class':           unasClassesRow[ unUseCaseIndex % 2],
                'use-case-name':       unUseCase,
                'permitted-block':     unForbiddenBlock,
            })
        else:
            if unUseCaseResult.has_key( 'duration'):
                unaDurationString = '%.3f ms' % unUseCaseResult[ 'duration']
            else:
                unaDurationString = '?'
                
            unOutput.write( """
                <tr class="%(row-class)s">
                    <td align="left">%(use-case-name)s</td>
                    <td align="center">%(permitted-block)s</td>    
                    <td align="center">%(duration)s</td>             </tr>
                \n""" % {
                'row-class':        unasClassesRow[ unUseCaseIndex % 2],
                'use-case-name':    unUseCaseName,
                'permitted-block':  ( unUseCaseResult.get( 'success', False) and unPermittedBlock)  or  unForbiddenBlock,
                'duration':         unaDurationString,
            })
    
    unOutput.write( """
            </tbody>
         </table>
         <br/>
        \n"""
    )
        
    
    TRARenderUseCaseAsssessments( unOutput, theContextualObject, unosUseCaseResults)    
    
                             
    unRolesRendering = unOutput.getvalue()
    
    if not theCollapsible:
        return unRolesRendering
    
    return fRenderCollapsible( unRolesRendering, "Logged User Security", 'csect_LoggedUserPermissionsHere', theCollapse)

    
    



def TRARenderUseCaseAsssessments( theOutput, theContextualObject, theUseCaseResults, theCollapsible=False, theCollapse=True):

    if not theContextualObject :
        return "Parameter missing: contextual object"
      
    if  not theUseCaseResults:
        return "Parameter missing: use case results"
      
   
    unPermittedBlock ="""
        <img alt="Permitted" src="%s/tra_permitida.gif" title="Passed" />
        \n""" % theContextualObject.absolute_url()

    unForbiddenBlock ="""
        <img alt="Forbidden" src="%s/tra_prohibida.gif" title="Failed" />
        \n""" % theContextualObject.absolute_url()    
    
    unElementPath       = '/'.join( theContextualObject.getPhysicalPath()[2:])
    unElementClassName  = theContextualObject.__class__.__name__
    
    if theOutput:
        unOutput = theOutput
    else:
        unOutput = StringIO()
        
      
    unOutput.write( """
        <br/>
        <!-- =====================================
        SECTION Logged User Use Cases Here
        ===================================== 
        -->
        
        <table class="listing nosort"  id="sect_UseCaseAsssessments" summary="Use Case Asssessments">
            <thead>
                <tr><th colspan="14" align="left"><font size="2"><strong>Assessment of Use Cases availability at %s<br/>%s</strong></font></th></tr>                
             </thead>
            <tbody>
        \n"""  % ( 
        unElementClassName, 
        unElementPath,
    ))
    
    unasClassesRow =[ 'odd', 'even', ]
    
    someUseCaseNames = sorted( cTRAUseCaseNames)
    for unUseCaseName in someUseCaseNames:
        unHeaderWritten = False
        unRowIndex = 0
 
        unUseCaseResult = theUseCaseResults.get( unUseCaseName, None) 
        
        if not unUseCaseResult:
            unOutput.write( """
                <tr>
                    <td colspan="14" bgcolor="silver" height="4"/>
                </tr>
                <tr>
                   <th><strong>?</strong></th>
                   <th colspan="7"><strong>%(use-case-name)s</strong></th>
                   <th colspan="6"><strong>not assessed</strong></th>
                </tr>   
                \n""" %unUseCaseName
            )
            continue
        
        unosAssessments = unUseCaseResult.get( 'rule_assessments', [])
        
        for unAssessment in unosAssessments:

            unAssessmentUseCaseName = unAssessment.get( 'use_case_name', '')

            if unAssessmentUseCaseName == unUseCaseName:

                unRowIndex += 1
                
                if not unHeaderWritten:
                    unOutput.write( """
                        <tr>
                            <td colspan="14" bgcolor="silver" height="4"/>
                        </tr>            
                        <tr>
                            <th align="left">%(permitted-block)s</th>
                            <th colspan="3" align="left"><font size="2"><strong>%(use-case-name)s</strong></font><strong></th>
                            <th colspan="10" align="left"><font color="%(permitted-color)s">&emsp;%(permitted-word)s</font></strong></th>
                        </tr>            
                        <tr>
                            <th  align="left"><strong>Pass</strong></th>
                            <th  align="left"><strong>Exception?</strong></th>
                            <th  align="left"><strong>Rule</strong></th>
                            <th  align="left"><strong>Mode</strong></th>
                            <th  align="left"><strong>Initial&ensp; ACCEPTED</strong></th>
                            <th  align="left"><strong>Final&ensp;ACCEPTED</strong></th>
                            <th  align="left"><strong>Initial&ensp;REJECTED</strong></th>
                            <th  align="left"><strong>Final&ensp;REJECTED</strong></th>
                            <th  align="left"><strong>Root types</strong></th>
                            <th  align="left"><strong>Path</strong></th>
                            <th  align="left"><strong>Expected Types</strong></th>
                            <th  align="left"><strong>Roles</strong></th>
                            <th  align="left"><strong>Permissions</strong></th>
                            <th  align="left"><strong>Exception</strong></th>
                            </tr>\n"""  % {
                            'use-case-name':       unUseCaseName,
                            'permitted-block' :   ( unUseCaseResult.get( 'success', False) and unPermittedBlock)  or  unForbiddenBlock,
                            'permitted-word' :    ( unUseCaseResult.get( 'success', False) and 'Permitted')  or  'Forbidden',
                            'permitted-color' :   ( unUseCaseResult.get( 'success', False) and 'green')  or  'red',
                    })
                    unHeaderWritten = True
                   
                    
                    
                unaRule         = unAssessment.get( 'rule', None)

                
                unaFullConstraintString = ""
                unRuleTitle = ""
                    
                if unaRule:                            
           
                    unObjectString      = ''
                    unObjectClassString = ''
                    unObject =  unAssessment.get( 'object', '')
                    if unObject:
                        unObjectString      =  '/'.join( unObject.getPhysicalPath()[2:])
                        unObjectClassString =  unObject.__class__.__name__
                            
                            
                    unAssessmentString = unAssessment.get( 'assessment', '')
                    if cRuleAssessmentMessages.has_key( unAssessmentString):
                        unAssessmentString = cRuleAssessmentMessages[ unAssessmentString]
                        
                    unOutput.write( """
                        <tr class="%(row-class)s">
                            <td align="left" valign="baseline">%(permitted-block)s</th>
                            <td align="left" valign="baseline"><font color="red"><strong>%(hay-exception)s</strong></font></td>
                            <td align="left" valign="baseline">%(rule-name)s</td>
                            <td align="left" valign="baseline">%(rule-mode)s</td>
                            <td align="left" valign="baseline">%(initial-accepted-objects)s</td>
                            <td align="left" valign="baseline">%(final-accepted-objects)s</td>
                            <td align="left" valign="baseline">%(initial-rejected-objects)s</td>
                            <td align="left" valign="baseline">%(final-rejected-objects)s</td>
                            <td align="left" valign="baseline">%(root-types)s</td>
                            <td align="left" valign="baseline">%(path)s</td>
                            <td align="left" valign="baseline">%(expected-types)s</td>
                            <td align="left" valign="baseline">%(roles)s</td>
                            <td align="left" valign="baseline">%(permissions)s</td>
                            <td align="left" valign="baseline"><font color="red">%(exception)s</font></td>
                        </tr>
                        \n""" % {
                        'permitted-block' :     ( unAssessment.get( 'success', False) and unPermittedBlock)  or  unForbiddenBlock,
                        'hay-exception':        (unaRule.get( 'exception', '') and '!!!') or '',
                        'passed' :              ( unAssessment.get( 'success', False) and 'Passed')  or  'Failed',
                        'row-class':            unasClassesRow[ unRowIndex % 2],
                        'rule-name':            unaRule.get( 'title', unaRule.get( 'name', cPermissionRuleNameDefault)),
                        'rule-mode':            unaRule.get( 'mode', cUseCaseRuleMode_ForAll),
                        'root-types':           ' '.join( unaRule.get( 'root', [])),
                        'path':                 ' '.join( unaRule.get( 'path', [])),
                        'expected-types':       ' '.join( unaRule.get( 'types', [])),
                        'roles':                ' '.join( [ '['+' '.join( unosRoles) +'] ' for unosRoles in unaRule.get( 'roles', [])]),
                        'permissions':          ' '.join( [ '[' + ' '.join( [ ("'%s'" % unaPerm) for unaPerm in unasPerms] ) +'] ' for unasPerms in unaRule.get( 'perms', [])]),
                        'exception':            unaRule.get( 'exception', ''),
                        'initial-accepted-objects': ', '.join( [ '%s&nbsp;%s' % ( unObject.__class__.__name__, '/'.join( unObject.getPhysicalPath()[2:]),) for unObject in unAssessment.get( 'accepted_initial_objects', [])  ]),
                        'initial-rejected-objects': ', '.join( [ '%s&nbsp;%s' % ( unObject.__class__.__name__, '/'.join( unObject.getPhysicalPath()[2:]),) for unObject in unAssessment.get( 'rejected_initial_objects', [])  ]),
                        'final-accepted-objects': ', '.join( [ '%s&nbsp;%s' % ( unObject.__class__.__name__, '/'.join( unObject.getPhysicalPath()[2:]),) for unObject in unAssessment.get( 'accepted_final_objects', [])  ]),
                        'final-rejected-objects': ', '.join( [ '%s&nbsp;%s' % ( unObject.__class__.__name__, '/'.join( unObject.getPhysicalPath()[2:]),) for unObject in unAssessment.get( 'rejected_final_objects', [])  ]),
                    })
                
                
        if not unHeaderWritten:
            unOutput.write( """
                <tr>
                    <td colspan="6" bgcolor="silver" height="4"/>
                </tr>
                 <tr>
                    <th align="left">%(permitted-block)s</th>
                    <th colspan="3" align="left"><font size="2"><strong>%(use-case-name)s</strong></font></th>
                    <th colspan="10" align="left">
                        <font size="2" color="%(permitted-color)s"><strong>%(permitted-word)s</strong></font>
                        &ensp;
                        <font size="2"><strong>without assessments</strong></font>
                    </th>
                 </tr>            
                \n""" % {
                'use-case-name':      unUseCaseName,
                'permitted-block' :   ( unUseCaseResult.get( 'success', False) and unPermittedBlock)  or  unForbiddenBlock,
                'permitted-word' :    ( unUseCaseResult.get( 'success', False) and 'Permitted')       or  'Forbidden',
                'permitted-color' :   ( unUseCaseResult.get( 'success', False) and 'green')  or  'red',
            })
            

    unOutput.write( """
            </tbody>
         </table>
         <br/>
        \n"""
    )
        
    
    if theOutput:
        return None
    
    unRendering = unOutput.getvalue()        
    return unRendering





# #########################################
#   Render Groups Roles Here
# #########################################




def TRARenderGroupsRolesHere( theContextualObject, theCollapsible=False, theCollapse=True):

    if not theContextualObject:
        return "Parameter missing: contextual object"

    
    unElementPath       = '/'.join( theContextualObject.getPhysicalPath()[2:])
    unElementClassName  = theContextualObject.__class__.__name__
    
    unPermittedBlock ="""
        <img alt="Permitted" src="%s/tra_permitida.gif" title="Permitted" />
        \n""" % theContextualObject.absolute_url()

    unForbiddenBlock ="""
        <img alt="Forbidden" src="%s/tra_prohibida.gif" title="Forbidden" />
        \n""" % theContextualObject.absolute_url()    
    
    
    

    unOutput = StringIO()    
    unOutput.write( """
        <tr>
            <th align="left">
                <strong>Groups %%s</strong>
            </th>
            <th colspan="%(num-columns-roles)d" align="center"><strong>Roles  Inherited (inh) and Local (loc)</strong></th>
        </tr>
        <tr>
           <th/>
            \n""" % {
        'num-columns-roles':  2 * len( cPreferredRolesOrder),
     })    
    for unRole in cPreferredRolesOrder:
        unOutput.write( """
           <th colspan="2" align="center" valign="bottom"><strong>%s</strong></th>
             \n"""  % unRole
        )   
    unOutput.write( """
            </tr>            
        \n"""
    )    
    unOutput.write( """
         <tr>
            <th/>
            \n""" % {
     })    
    for unRole in cPreferredRolesOrder:
        unOutput.write( """
            <th align="left" valign="bottom"><strong>inh</strong></th>
            <th align="left" valign="bottom"><strong>loc</strong></th>
            \n"""
        )   
    unOutput.write( """
            </tr>            
        \n"""
    )    
    unRolesHeaderBlock =  unOutput.getvalue()

 
    
    unOutput = StringIO()
    
    unOutput.write( """
        <br/>
        <table class="listing nosort"  id="sect_GroupsRolesHere" summary="Group Roles Here">
            <thead>
                <tr><th colspan="%(num-columns)d" align="left"><font size="2"><strong>Group Roles at %(class-name)s<br/>%(element-path)s</strong></font></th></tr>                
            </thead>
            <tbody>
        \n""" % {
        'num-columns':        1 + ( 2 * len( cPreferredRolesOrder)),  
        'class-name':         unElementClassName,
        'element-path':       unElementPath,
     })
    
    TRARenderGroupsRolesHere_forAGroupLevel( 
        unOutput, 
        theContextualObject,     
        'Global',  
        lambda theGroupName: theContextualObject.getCatalogo().fUserGroupIdEnCatalogoFor(theGroupName),            
        unElementClassName, 
        unElementPath, 
        unRolesHeaderBlock, 
        unPermittedBlock, 
        unForbiddenBlock,
    )

    # ACV 20090928 Simpler security model now does not use user groups for languages or modules (all or specific).
    #
    #Users get access to all languages by being added to he global user groups for application roles. 
    #There is no need anymore to use the "_All" user groups.
    #
    #Rather, users are given language or module specific local roles directly on the language or module.
    #Because the languages and modules do not contain  elements (translations are under strings, elsewhere),
    #assigning local roles to users ar languages and modules do not have a performance penalty 
    #(as it has on elements with lots of contained elements).
    #
    #TRARenderGroupsRolesHere_forAGroupLevel( unOutput, theContextualObject,     'AllLanguages', lambda theGroupName: theContextualObject.getCatalogo().fUserGroupIdAllIdiomasFor(theGroupName),            unElementClassName, unElementPath, unRolesHeaderBlock, unPermittedBlock, unForbiddenBlock)
    
    #unosIdiomas = theContextualObject.getCatalogo().fObtenerTodosIdiomas()
    #for unIdioma in unosIdiomas:
        #TRARenderGroupsRolesHere_forAGroupLevel( unOutput, theContextualObject, 'Language %s' % unIdioma.getCodigoIdiomaEnGvSIG(), lambda theGroupName: theContextualObject.fUserGroupIdIdiomaFor( theGroupName, unIdioma),     unElementClassName, unElementPath, unRolesHeaderBlock, unPermittedBlock, unForbiddenBlock)
    
    #unosModulos = theContextualObject.getCatalogo().fObtenerTodosModulos()
    #for unModulo in unosModulos:
        #TRARenderGroupsRolesHere_forAGroupLevel( unOutput, theContextualObject, 'Module %s' % unModulo.Title(),  lambda theGroupName: theContextualObject.fUserGroupIdModuloFor( theGroupName, unModulo),     unElementClassName, unElementPath, unRolesHeaderBlock, unPermittedBlock, unForbiddenBlock)
    
    unOutput.write( """
            </tbody>
        </table>        
        \n"""
    )
        
        
    unRendering = unOutput.getvalue()
    
    if not theCollapsible:
        return unRolesRendering
    
    return fRenderCollapsible( unRendering, "User Groups Security", 'csect_GroupsRolesHere', theCollapse)

    




    # ACV 20090321 
    # See CMFPlone/skins/plone_forms/folder_localrole_form.pt
    # See CMFPlone/skins/plone_scripts/computeRoleMap.py
    # putils.isLocalRoleAcquired(here)
    # tal:repeat="entry  entry here/computeRoleMap
    # tal:repeat="role entry/acquired">

def TRARenderGroupsRolesHere_forAGroupLevel( unOutput, theContextualObject, theGroupsKind, theGroupIdResolver_lambda, unElementClassName, unElementPath, unRolesHeaderBlock, unPermittedBlock, unForbiddenBlock):
    
    unOutput.write( """
            %(role-headers)s
             \n""" % {
        'groups-kind':        theGroupsKind,
        'num-columns':        1 + len( cPreferredRolesOrder),
        'num-columns-roles':  len( cPreferredRolesOrder),
        'class-name':         unElementClassName,
        'element-path':       unElementPath,
        'role-headers':       unRolesHeaderBlock % theGroupsKind,
    })
    
    unasClassesRow =[ 'odd', 'even', ]
        
    aPloneUtilsTool = getToolByName( theContextualObject, 'plone_utils', None)
    if not aPloneUtilsTool:
        return None
    
    aIsLocalRoleAcquired = aPloneUtilsTool.isLocalRoleAcquired( theContextualObject)
    
    someAcquiredRoles = aPloneUtilsTool.getInheritedLocalRoles( theContextualObject)    
    someAcquiredRolesByGroupId = { }
    for anAcquiredRole in someAcquiredRoles:
        aName       = anAcquiredRole[ 0]
        someRoles   = anAcquiredRole[ 1]
        aType       = anAcquiredRole[ 2]
        anId        = anAcquiredRole[ 3]
        
        if aType == 'group' and anId and someRoles:
            someAcquiredRolesByGroupId[ anId] = someRoles    
                               
                               
  
    for unGroupIndex in range( len( cTRAPreferredUserGroupsOrder)):
        unGroup = cTRAPreferredUserGroupsOrder[ unGroupIndex]
        
        unGroupId = theGroupIdResolver_lambda( unGroup)
        
        unOutput.write( """
            <tr class="%(row-class)s">
                <td align="left">%(group-name)s</th>
            \n""" % {
            'row-class':     unasClassesRow[ unGroupIndex % 2],
            'group-name':    unGroup,
        })

        unosGroupAcquiredRolesHere = someAcquiredRolesByGroupId.get( unGroupId, [])
        unosGroupLocalRolesHere = theContextualObject.get_local_roles_for_userid( unGroupId)
        for unRole in cPreferredRolesOrder:
            unOutput.write( """
                <td align="center">%(acquired-role-block)s</th>
                <td align="center">%(local-role-block)s</th>
                \n""" % {
                'acquired-role-block' : (( ( aIsLocalRoleAcquired and ( unRole in unosGroupAcquiredRolesHere)) and unPermittedBlock) or unForbiddenBlock),
                'local-role-block' :    ((( unRole in unosGroupLocalRolesHere)    and unPermittedBlock) or unForbiddenBlock)
            })
        unOutput.write( """
            </tr>            
            \n"""
        )        
    return None

    
    

    
    










 #######################################
# Rendering utilities
#




    
def fRenderCollapsible( theString, theCollapsibleTitle, theCollapsibleId, theLambda, theCollapse=True):
            
    unCollapsedOrExpanded = ( theCollapse and 'collapsed') or 'expanded'
    
    anOutput = StringIO()
    
    anOutput.write( u"""  
        
        <!-- ######### Start collapsible  section ######### --> 
        <dl id="%(pCollapsibleId)s" class="collapsible inline %(unCollapsedOrExpanded)sInlineCollapsible">
            <dt class="collapsibleHeader">
                <strong>%(pCollapsibleTitle)s</strong>
            </dt>
            <dd class="collapsibleContent">    
            \n""" % {
        'unCollapsedOrExpanded':  unCollapsedOrExpanded,
        'pCollapsibleTitle':      theCollapsibleTitle,
        'pCollapsibleId':         theCollapsibleId,
    })
    
    anOutput.write( unicode( theString))  
     
    anOutput.write( u"""  
            </dd>
        </dl>
        <!-- ######### End collapsible  section ######### --> 
        \n"""
    )
    
    return anOutput.getvalue()        
