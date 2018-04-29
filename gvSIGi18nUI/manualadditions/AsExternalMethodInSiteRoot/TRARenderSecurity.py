# -*- coding: utf-8 -*-
#
# File: TRARenderSecurity.py
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


from StringIO import StringIO

from Products.CMFCore.utils import getToolByName

from Products.gvSIGi18n.TRAElemento_Constants                 import *
from Products.gvSIGi18n.TRAElemento_Constants_Activity        import *
from Products.gvSIGi18n.TRAElemento_Constants_Configurations  import *
from Products.gvSIGi18n.TRAElemento_Constants_Dates           import *
from Products.gvSIGi18n.TRAElemento_Constants_Encoding        import *
from Products.gvSIGi18n.TRAElemento_Constants_Import          import *
from Products.gvSIGi18n.TRAElemento_Constants_Languages       import *
from Products.gvSIGi18n.TRAElemento_Constants_Logging         import *
from Products.gvSIGi18n.TRAElemento_Constants_Modules         import *
from Products.gvSIGi18n.TRAElemento_Constants_Profiling       import *
from Products.gvSIGi18n.TRAElemento_Constants_Progress        import *
from Products.gvSIGi18n.TRAElemento_Constants_String          import *
from Products.gvSIGi18n.TRAElemento_Constants_StringRequests  import *
from Products.gvSIGi18n.TRAElemento_Constants_Translate       import *
from Products.gvSIGi18n.TRAElemento_Constants_Translation     import *
from Products.gvSIGi18n.TRAElemento_Constants_TypeNames       import *
from Products.gvSIGi18n.TRAElemento_Constants_Views           import *
from Products.gvSIGi18n.TRAElemento_Constants_Vocabularies    import *
from Products.gvSIGi18n.TRAUtils                              import *

from Products.gvSIGi18n.TRAElemento_Permission_Definitions import cPreferredPermissions, cPreferredRolesOrder, cTRAPreferredUserGroupsOrder

from Products.gvSIGi18n.TRAElemento_Permission_Definitions import cRuleAssessmentMessages, cPermissionRuleNameDefault

from Products.gvSIGi18n.TRAElemento_Permission_Definitions import cUseCaseRuleMode_ForAll, cUseCaseRuleMode_Filter, cUseCaseRuleMode_EmptyOrAll, cUseCaseRuleMode_EmptyOrAny

from Products.gvSIGi18n.TRAElemento_Permission_Definitions_UseCaseNames import cTRAUseCaseNames


from Products.gvSIGi18nTool.TRAgvSIGi18nTool_Constants import cTRAgvSIGi18nToolId

from Products.ModelDDvlPloneTool.ModelDDvlPloneToolLoadConstants import cModelDDvlPloneToolId





# ##################################################################################



def TRARenderPermissionDefinitions( theContextualObject, theCollapsible=False, theCollapse=True):
    """Render Permission Definitions.
    
    """

    if theContextualObject == None:
        return "Parameter missing: contextual object"
   
    aTRAgvSIGi18n_tool = getToolByName( theContextualObject, cTRAgvSIGi18nToolId, None)
    if aTRAgvSIGi18n_tool == None:
        return "Internal error: no TRAgvSIGi18n_tool"
         
    aMDDModelDDvlPlone_tool = getToolByName( theContextualObject, cModelDDvlPloneToolId, None)
    if aMDDModelDDvlPlone_tool == None:
        return "Internal error: no MDDModelDDvlPlone_tool"
        
    
    aPortalURL   = aMDDModelDDvlPlone_tool.fPortalURL()   
    
    
    unasPermissionsByElementType = aTRAgvSIGi18n_tool.fPermissionsByElementType( 
        theContextualElement=theContextualObject,
    )
    if not unasPermissionsByElementType:
        return "Configuration missing: PermissionsByElementType"
 
    
    
    # #################################################
    """Prepare HTML string with a header row for all roles.
    
    """
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
        \n""" % aPortalURL

    unForbiddenBlock ="""
        <img alt="Forbidden" src="%s/tra_prohibida.gif" title="Forbidden" />
        \n""" % aPortalURL

    
    
    
    
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

    











# ##################################################################################



def TRARenderLoggedUsedHere( theContextualObject, theCollapsible=False, theCollapse=True):
    """Render Logged Used Here.
    
    """

    if theContextualObject == None:
        return "Parameter missing: contextual object"
   
    aTRAgvSIGi18n_tool = getToolByName( theContextualObject, cTRAgvSIGi18nToolId, None)
    if aTRAgvSIGi18n_tool == None:
        return "Internal error: no TRAgvSIGi18n_tool"
         
    aMDDModelDDvlPlone_tool = getToolByName( theContextualObject, cModelDDvlPloneToolId, None)
    if aMDDModelDDvlPlone_tool == None:
        return "Internal error: no MDDModelDDvlPlone_tool"
        
    
    aPortalURL   = aMDDModelDDvlPlone_tool.fPortalURL()   
          
    
    
    unBasicInfo = aTRAgvSIGi18n_tool.fBasicInfo( theContextualElement = theContextualObject)
    
    unElementPath       = unBasicInfo.get( 'path', '').replace('/', ' / ')
    unElementClassName  = unBasicInfo.get( 'meta_type', '')
    anElementURL        = unBasicInfo.get( 'absolute_url', '')    
    
    
    unUserName = aTRAgvSIGi18n_tool.fGetMemberId( 
        theContextualElement = theContextualObject,
    )

        
    unosRoles = aTRAgvSIGi18n_tool.fGetRequestingUserRoles(
        theContextualElement    = theContextualObject,
    )

    
    

    somePermissions = sorted( cPreferredPermissions)
        
    aPermissionsPermittedReport = aTRAgvSIGi18n_tool.fPermissionsPermittedReport( 
        theContextualElement  =theContextualObject,
        thePermissionsToCheck =somePermissions,
    )
    
    
    

    someUseCaseNames = sorted( cTRAUseCaseNames)    
    
    unosUseCaseResults = aTRAgvSIGi18n_tool.fUseCaseAssessment_AvailableUseCasesOn( 
        theContextualElement        =theContextualObject,
        theUseCaseNamesToAssess     =cTRAUseCaseNames, 
        theRulesToCollect           =[],
        thePermissionsCache         =None,
        theRolesCache               =None,
        theParentExecutionRecord    =None,
    ) 

    
    
    

    

    
    unPermittedBlock ="""
        <img alt="Permitted" src="%s/tra_permitida.gif" title="Permitted" />
        \n""" % aPortalURL

    unForbiddenBlock ="""
        <img alt="Forbidden" src="%s/tra_prohibida.gif" title="Forbidden" />
        \n""" % aPortalURL    
    
    
 

    
    
  
          
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

    for unaPermissionIndex in range( len( somePermissions)):
        
        unaPermission = somePermissions[ unaPermissionIndex]
        aPermitted    = aPermissionsPermittedReport.get( unaPermission, False)
        
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
                    <td align="left">
                        <a title="Use Case Assessment %(use-case-name)s summary"  
                            id="cid_TRAUseCaseAssessment_%(use-case-name)s_summary"
                            href="%(anElementURL)s/TRASeguridadUsuarioConectado/#cid_TRAUseCaseAssessment_%(use-case-name)s" >
                            %(use-case-name)s
                        </a>
                    </td>
                    <td align="center">%(permitted-block)s</td>    
                    <td align="center">%(duration)s</td>             </tr>
                \n""" % {
                'row-class':        unasClassesRow[ unUseCaseIndex % 2],
                'use-case-name':    unUseCaseName,
                'permitted-block':  ( unUseCaseResult.get( 'success', False) and unPermittedBlock)  or  unForbiddenBlock,
                'duration':         unaDurationString,
                'anElementURL':     anElementURL,
            })
    
    unOutput.write( """
            </tbody>
         </table>
         <br/>
        \n"""
    )
        
    
    pTRARenderUseCaseAsssessments( 
        theOutput             =unOutput, 
        theContextualObject   =theContextualObject, 
        theUseCaseResults     =unosUseCaseResults,
        theTRAgvSIGi18n_tool  =aTRAgvSIGi18n_tool,
        thePortalURL          =aPortalURL,
        theElementURL         =anElementURL,
    )

    
    
                             
    unRolesRendering = unOutput.getvalue()
    
    if not theCollapsible:
        return unRolesRendering
    
    return fRenderCollapsible( unRolesRendering, "Logged User Security", 'csect_LoggedUserPermissionsHere', theCollapse)

    


    



def pTRARenderUseCaseAsssessments( 
    theOutput            =None, 
    theContextualObject  =None, 
    theUseCaseResults    =None,
    theTRAgvSIGi18n_tool =None,
    thePortalURL         ='',
    theElementURL        ='',):

    
    def fJoinObjectsInfo( theObjects=None):
        if theTRAgvSIGi18n_tool == None:
            return ''
        
        if not theObjects:
            return ''
        
        someObjectsStrings = []

        for anObject in theObjects:
            anObjectBasicInfo = theTRAgvSIGi18n_tool.fBasicInfo( theContextualElement=anObject)
            
            anObjectString = '<strong>%s</strong><br/>%s' % ( anObjectBasicInfo.get( 'meta_type', ''), anObjectBasicInfo.get( 'path', '').replace( '/', ' / '),)

            someObjectsStrings.append( anObjectString)
            
        aJoinedObjectsInfo = '\n<br/>\n'.join( someObjectsStrings)
        
        return aJoinedObjectsInfo
    
    
    

    if theContextualObject == None:
        return "Parameter missing: contextual object"
    
    if theTRAgvSIGi18n_tool == None:
        return "Parameter missing: TRAgvSIGi18n_tool"
    
    if  not theUseCaseResults:
        return "No use case results to render"


    unBasicInfo = theTRAgvSIGi18n_tool.fBasicInfo( theContextualElement = theContextualObject)
    
    unElementPath       = unBasicInfo.get( 'path', '').replace('/', ' / ')
    unElementClassName  = unBasicInfo.get( 'meta_type', '')
        
               

   
    unPermittedBlock ="""
        <img alt="Permitted" src="%s/tra_permitida.gif" title="Passed" />
        \n""" % thePortalURL

    unForbiddenBlock ="""
        <img alt="Forbidden" src="%s/tra_prohibida.gif" title="Failed" />
        \n""" % thePortalURL    
    

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
                <tr id="cid_TRAUseCaseAssessment_%(use-case-name)s" >
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
                            <th colspan="3" align="left">
                                <a title="Use Case Assessment %(use-case-name)s detail"  
                                    id="cid_TRAUseCaseAssessment_%(use-case-name)s"
                                    href="%(anElementURL)s/TRASeguridadUsuarioConectado/#cid_TRAUseCaseAssessment_%(use-case-name)s_summary" >
                                    <font size="2"><strong>%(use-case-name)s</strong></font>                               
                                </a>
                            </th>
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
                            'anElementURL':       theElementURL,
                            'use-case-name':      unUseCaseName,
                            'permitted-block' :   ( unUseCaseResult.get( 'success', False) and unPermittedBlock)  or  unForbiddenBlock,
                            'permitted-word' :    ( unUseCaseResult.get( 'success', False) and 'Permitted')  or  'Forbidden',
                            'permitted-color' :   ( unUseCaseResult.get( 'success', False) and 'green')  or  'red',
                    })
                    unHeaderWritten = True
                   
                    
                    
                unaRule         = unAssessment.get( 'rule', None)

                
                unaFullConstraintString = ""
                unRuleTitle = ""
                    
                if unaRule:                            
           
                    unObjectPathString      = ''
                    unObjectClassString = ''
                    unObject =  unAssessment.get( 'object', '')
                    if unObject:
                        unObjectBasicInfo = theTRAgvSIGi18n_tool.fBasicInfo( theContextualElement = unObject)
                        
                        unObjectPathString   = unObjectBasicInfo.get( 'path', '').replace('/', ' / ')
                        unObjectClassString  = unObjectBasicInfo.get( 'meta_type', '')
        

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
                        'initial-accepted-objects': fJoinObjectsInfo( unAssessment.get( 'accepted_initial_objects', [])),
                        'initial-rejected-objects': fJoinObjectsInfo( unAssessment.get( 'rejected_initial_objects', [])),
                        'final-accepted-objects':   fJoinObjectsInfo( unAssessment.get( 'accepted_final_objects',   [])),
                        'final-rejected-objects':   fJoinObjectsInfo( unAssessment.get( 'rejected_final_objects',   [])),
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





# ##################################################################################


def TRARenderGroupsRolesHere( 
    theContextualObject, 
    theCollapsible=False, 
    theCollapse=True):
    """Render Groups Roles Here.
    
    """

    if theContextualObject == None:
        return "Parameter missing: contextual object"
 
    aTRAgvSIGi18n_tool = getToolByName( theContextualObject, cTRAgvSIGi18nToolId, None)
    if aTRAgvSIGi18n_tool == None:
        return "Internal error: no TRAgvSIGi18n_tool"
             
    aMDDModelDDvlPlone_tool = getToolByName( theContextualObject, cModelDDvlPloneToolId, None)
    if aMDDModelDDvlPlone_tool == None:
        return "Internal error: no MDDModelDDvlPlone_tool"

    aPortalURL   = aMDDModelDDvlPlone_tool.fPortalURL()   
          
    unBasicInfo = aTRAgvSIGi18n_tool.fBasicInfo( theContextualElement = theContextualObject)
    
    unElementPath       = unBasicInfo.get( 'path', '').replace('/', ' / ')
    unElementClassName  = unBasicInfo.get( 'meta_type', '')
        
        
    unPermittedBlock ="""
        <img alt="Permitted" src="%s/tra_permitida.gif" title="Permitted" />
        \n""" % aPortalURL

    unForbiddenBlock ="""
        <img alt="Forbidden" src="%s/tra_prohibida.gif" title="Forbidden" />
        \n""" % aPortalURL    
    
    
    

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
    
    
    
    pTRARenderGroupsRolesHere_forAGroupLevel( 
        unOutput                  =unOutput, 
        theContextualObject       =theContextualObject, 
        theGroupsKind             ='Global', 
        theGroupIdResolver_lambda =lambda theGroupName: theContextualObject.getCatalogo().fUserGroupIdEnCatalogoFor(theGroupName), 
        unElementClassName        =unElementClassName, 
        unElementPath             =unElementPath, 
        unRolesHeaderBlock        =unRolesHeaderBlock, 
        unPermittedBlock          =unPermittedBlock, 
        unForbiddenBlock          =unForbiddenBlock,
        aTRAgvSIGi18n_tool        =aTRAgvSIGi18n_tool
    )

    
    
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
    
    
    


def pTRARenderGroupsRolesHere_forAGroupLevel( 
    unOutput                   =None, 
    theContextualObject        =None, 
    theGroupsKind              =None, 
    theGroupIdResolver_lambda  =None, 
    unElementClassName         =None, 
    unElementPath              =None, 
    unRolesHeaderBlock         =None, 
    unPermittedBlock           =None, 
    unForbiddenBlock           =None,
    aTRAgvSIGi18n_tool         =None,):

    if aTRAgvSIGi18n_tool == None:
        return self
    
    
    
    aIsLocalRoleAcquired = aTRAgvSIGi18n_tool.fIsLocalRoleAcquired( 
        theContextualElement = theContextualObject,
    )
    
    someAcquiredRoles = aTRAgvSIGi18n_tool.fInheritedLocalRoles( 
        theContextualElement = theContextualObject,
    )  
    
    
    
    
    
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
        
        unosGroupLocalRolesHere = aTRAgvSIGi18n_tool.fLocalRolesForUserId( 
            theContextualElement =theContextualObject, 
            theUserId            =unGroupId,
        )
        
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

    
    

    
    












    
def fRenderCollapsible( theString, theCollapsibleTitle, theCollapsibleId, theLambda, theCollapse=True):
    """Rendering utility to wrap an HTML block in a collapsible section, offering the User the option to show or hide the HTML.
    
    """
            
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
