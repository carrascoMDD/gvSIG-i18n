# -*- coding: utf-8 -*-
#
# File: TRARenderProfiling.py
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
import logging


from StringIO import StringIO

from Products.CMFCore.utils import getToolByName

cLogRenderProfilingExceptions = True



# #########################################
#   Rendering utilities
# #########################################



cCollapsibleBlock_open = """
            
    <!-- ######### Start collapsible  section ######### 
    # positional parameters: id, title, content 
    --> 
    <dl id="%s" class="collapsible inline collapsedInlineCollapsible">
        <dt class="collapsibleHeader">
            <strong>%s</strong>
        </dt>
        <dd class="collapsibleContent">   
   \n"""  


cCollapsibleBlock_forTimeProfiling_open = """
            
    <!-- ######### Start collapsible  section ######### 
    # positional parameters: id, title, content 
    --> 
    <dl id="%s" class="collapsible inline collapsedInlineCollapsible TRA_timeProfileWithchildren_refinePlone_dt_collapsibleHeader">
        <dt class="collapsibleHeader">
            <strong>%s</strong>
        </dt>
        <dd class="collapsibleContent">   
   \n"""  

cCollapsibleBlock_close = """
       </dd>
    </dl>
    <br/>
    <!-- ######### End collapsible  section ######### --> 
    \n"""  

# positional parameters: id, title, content 
cCollapsibleBlock = '%s%%s%s' % ( cCollapsibleBlock_open, cCollapsibleBlock_close,) 




cHTMLIndentLength = 3
cHTMLIndentUnit = '&nbsp;'
cHTMLIndent = cHTMLIndentUnit * cHTMLIndentLength

cHTMLDurationFiller = '&nbsp;'
cHTMLTitleFiller    = '&nbsp;'


        
def fExecutionRecordPrintString( theExecutionRecord, ):

    if not theExecutionRecord:
        return ''
    
    try:
        if theExecutionRecord.vInitialized:
            return '%d ms %s %s %s %s %s %s %s' % (      
                theExecutionRecord.vExecutionEndTime - theExecutionRecord.vExecutionStartTime, 
                ( theExecutionRecord.vExceptions and '!!!') or '',
                theExecutionRecord.vExecutedKind or 'unknown_executed_kind', 
                theExecutionRecord.vExecutedName or 'unknown_executed_name', 
                theExecutionRecord.vContextualObjectClassName or 'unknown_object_class_name',
                theExecutionRecord.vContextualObjectTitle or 'unknown_object_title',
                theExecutionRecord.vContextualObjectPath   or 'unknown_object_path',
                ' '.join( theExecutionRecord.vExtraExecutionInfo or []),                
            )
    except:
        None    
    
    return 'exception printing execution record'
    


def TRARenderExecutionDetails( theExecutionRecord,):
    """Render Performance profiling information.
    
    """

    try:
        if not theExecutionRecord.vInitialized:
            return 'TRARenderExecutionDetails error: Missing parameter theExecutionRecord'
 
        if not theExecutionRecord.vInitialized:
            return 'TRARenderExecutionDetails error: theExecutionRecord not initialized'
        
        
        theOutput = StringIO()
        
        unDuration = theExecutionRecord.vExecutionEndTime - theExecutionRecord.vExecutionStartTime
        
        pWriteStylesForExecutionRecordPrintString(  theOutput)
        
        pWriteScriptsForExecutionRecordPrintString( theOutput)
        
        theOutput.write( cCollapsibleBlock_open % ( 'TRAExecutionProfiling_id', '%d ms. - Execution Profile' % unDuration,))
            
        
        theOutput.write( """
            <br/>
            <table cellspacing="0" cellpadding="1" border="0" >
            \n"""
        )

        pWriteExecutionRecordTableHeader(          theOutput)
                
        theOutput.write( """
            <tbody>
            \n"""
        )
        pRenderExecutionDetailsOn_HTML(            theOutput, theExecutionRecord, 0, len( str( unDuration)), "TRAxrecid", '')
        
        theOutput.write( """
                </tbody>
            </table>
            \n"""
        )
        
        theOutput.write( cCollapsibleBlock_close)
        
        unString = theOutput.getvalue()
        return unString
    
    except:
        unaExceptionInfo = sys.exc_info()
        unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
        
        unInformeExcepcion = 'Exception during TRARenderExecutionDetails\n' 
        unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
        unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
        unInformeExcepcion += unaExceptionFormattedTraceback   
                     
        if cLogRenderProfilingExceptions:
            logging.getLogger( 'gvSIGi18n TRARenderExecutionDetails').error( unInformeExcepcion)
            
        return '<br/><p>%s</p><br/>' % unInformeExcepcion.replace( '\n', '<br/>').replace( ' ', '&ensp;')

    
        
        
        
        
def pWriteStylesForExecutionRecordPrintString( theOutput, ):
     
    theOutput.write( """
        
        <style type="text/css" >
            tr.TRAstyle_NoDisplay {
                display: none;
            }
            tr.TRAstyle_Display {
                display: table-row;
            }
            tr.TRAstyle_Collapsed {
                font-size: 100%;
                font-family: "Courier New", Courier;
                line-height: 12pt;
                cursor: pointer;
                border-collapse:collapse;
                border-spacing:0;
                font-weight: 900;
            }
            tr.TRAstyle_Expanded {
                font-size: 100%;
                font-family: "Courier New", Courier;
                line-height: 12pt;
                cursor: pointer;
                border-collapse:collapse;
                border-spacing:0;
                font-weight: 400;                
            }
            tr.TRAstyle_Own {
                font-size: 100%;
                font-family: "Courier New", Courier;
                line-height: 12pt;
                cursor: auto;
                border-collapse:collapse;
                border-spacing:0;
                font-weight: 300;                
            }
            tr.TRAstyle_WOChildren {
                font-size: 100%;
                font-family: "Courier New", Courier;
                line-height: 12pt;
                cursor: auto;
                border-collapse:collapse;
                border-spacing:0;
                font-weight: 300;                
            }
            tr.TRAstyle_Exception {
                font-size: 100%;
                font-family: "Courier New", Courier;
                line-height: 12pt;
                cursor: auto;
                border-collapse:collapse;
                border-spacing:0;
            }
            asremainderofcodewritten.dl.collapsible p.TRA_timeProfileWOchildren_likePlone_dt_collapsibleHeader {
                background: transparent none no-repeat scroll 0 0;
                cursor: auto;
                display: inline;
                float: none;
                line-height: normal;
                padding: 0 0 0 23px;
                position: static;
                font-size: 100%;
                top: -0.6rm;
                vertical-align: middle;
                width: auto;
                border-collapse: collapse;
                border-spacing: 0;
                color: black;
                font-family: "Courier New", Courier;
                font-size-adjust: none;
                font-style: normal;
                font-weight: bold;
                font-variant: normal;
            }
            asremainderofcodewritten.dl.collapsible dt.collapsibleHeader.TRA_timeProfileWithchildren_refinePlone_dt_collapsibleHeader {
                font-family: "Courier New", Courier;
            }
        </style>
        \n"""
    )
    return None



        
        
def pWriteScriptsForExecutionRecordPrintString( theOutput, ):
    if not theOutput:
        return None
    
    theOutput.write( """
        

        <!-- #################################################################
         SECTION: Scripts to control display of execution profiling records
         ################################################################# -->
        <script>
             function pTRAExpandOrCollapseDirectChildren( theElementId) {
                // this function toggles the display of execution profiling records
                
                var unElement = document.getElementById( theElementId);

                if ( unElement) {

                    if ( hasClassName( unElement, 'TRAstyle_Collapsed')) {
                        replaceClassName( unElement, 'TRAstyle_Collapsed', 'TRAstyle_Expanded');
                    }
                    else {
                        if ( hasClassName( unElement, 'TRAstyle_Expanded')) {  
                            replaceClassName( unElement, 'TRAstyle_Expanded', 'TRAstyle_Collapsed');
                        }
                    }
                    var unRowClassCounter = 0
                    if ( hasClassName( unElement,  'even')) {
                        unRowClassCounter = 1
                    }
                    else {
                        if ( hasClassName( unElement,  'odd')) {
                            unRowClassCounter = 0
                        }
                    }
                    fTRAApplyDisplay( unElement, unRowClassCounter);
                }
                return true;
            }
        </script>
        <script>
             function pTRAExpandOrCollapseAllChildren( theElementId) {
                // this function toggles the display of execution profiling records
                
                var unElement = document.getElementById( theElementId);

                if ( unElement) {

                    if ( hasClassName( unElement, 'TRAstyle_Collapsed')) {
                        replaceClassName( unElement, 'TRAstyle_Collapsed', 'TRAstyle_Expanded');
                        pTRAChangeClassInChildren( unElement, 'TRAstyle_Collapsed', 'TRAstyle_Expanded', true);
                        
                    }
                    else {
                        if ( hasClassName( unElement, 'TRAstyle_Expanded')) {  
                            replaceClassName( unElement, 'TRAstyle_Expanded', 'TRAstyle_Collapsed');
                            pTRAChangeClassInChildren( unElement, 'TRAstyle_Expanded', 'TRAstyle_Collapsed', true);
                        }
                    }
                    
                    var unRowClassCounter = 0
                    if ( hasClassName( unElement,  'even')) {
                        unRowClassCounter = 1
                    }
                    else {
                        if ( hasClassName( unElement,  'odd')) {
                            unRowClassCounter = 0
                        }
                    }
                    fTRAApplyDisplay( unElement, unRowClassCounter);
                }
                return true;
            }
        </script>
        <script>
            function fTRAApplyDisplay( theElement, theRowClassCounter) {
                // Set class as Display for children of expanded elements and NoDisplay for children of collapsed elements
                
                var unRowClassCounter = theRowClassCounter
                
                 
                if ( hasClassName( theElement, 'TRAstyle_Collapsed')) {  
                
                    pTRAChangeClassInChildren( theElement, 'TRAstyle_Display', 'TRAstyle_NoDisplay', true);
                     
                }
                else {
                    if ( hasClassName( theElement, 'TRAstyle_Expanded')) {  
                              
                        unSubElement = document.getElementById( theElement.id + '_own' );
                        if ( unSubElement) {
                            if ( hasClassName( unSubElement,  'TRAstyle_NoDisplay')) {
                                replaceClassName( unSubElement,  'TRAstyle_NoDisplay',  'TRAstyle_Display');
                            }  
                            if ( (unRowClassCounter % 2) == 1) {
                                if ( hasClassName( unSubElement,  'even')) {
                                    replaceClassName( unSubElement,  'even',  'odd');
                                }
                            }
                            else {
                                if ( hasClassName( unSubElement,  'odd')) {
                                    replaceClassName( unSubElement,  'odd',  'even');
                                }
                            }
                            unRowClassCounter += 1
                        }
                        for( var unIdCounter=0; unIdCounter < 10000; unIdCounter++) {
                            
                            unSubElement = document.getElementById( theElement.id + '_exception_' + unIdCounter );
                            
                            if ( unSubElement) {
                                if ( hasClassName( unSubElement,  'TRAstyle_NoDisplay')) {
                                    replaceClassName( unSubElement,  'TRAstyle_NoDisplay',  'TRAstyle_Display');  
                                }  
                                if ( (unRowClassCounter % 2) == 1) {
                                    if ( hasClassName( unSubElement,  'even')) {
                                        replaceClassName( unSubElement,  'even',  'odd');
                                    }
                                }
                                else {
                                    if ( hasClassName( unSubElement,  'odd')) {
                                        replaceClassName( unSubElement,  'odd',  'even');
                                    }
                                }
                                unRowClassCounter += 1
                            }
                            else {
                                break;
                            }
                            
                            unRowClassCounter = fTRAApplyDisplay( unSubElement, unRowClassCounter);
                        } 
                        
                        for( var unIdCounter=0; unIdCounter < 10000; unIdCounter++) {
                            
                            unSubElement = document.getElementById( theElement.id + '_' + unIdCounter );
                            
                            if ( unSubElement) {
                                if ( hasClassName( unSubElement,  'TRAstyle_NoDisplay')) {
                                    replaceClassName( unSubElement,  'TRAstyle_NoDisplay',  'TRAstyle_Display');
                                }  
                                if ( (unRowClassCounter % 2) == 1) {
                                    if ( hasClassName( unSubElement,  'even')) {
                                        replaceClassName( unSubElement,  'even',  'odd');
                                    }
                                }
                                else {
                                    if ( hasClassName( unSubElement,  'odd')) {
                                        replaceClassName( unSubElement,  'odd',  'even');
                                    }
                                }
                                unRowClassCounter += 1
                            }
                            else {
                                break;
                            }
                            
                            unRowClassCounter = fTRAApplyDisplay( unSubElement, unRowClassCounter);
                        } 
                    }
                }                    
                return unRowClassCounter;
            }
        </script>
        <script>
            function pTRAChangeClassInChildren( theElement, theExistingClass, theNewClass, theRecurse) {
                // changes element's children class, optionally recursively
                
                unSubElement = document.getElementById( theElement.id + '_own');
                if ( unSubElement) {
                    if ( hasClassName( unSubElement, theExistingClass)) {
                        replaceClassName( unSubElement, theExistingClass, theNewClass);
                    }                            
                    if ( theRecurse) {
                        pTRAChangeClassInChildren( unSubElement, theExistingClass, theNewClass, theRecurse);
                    }
                }
                
                for( var unIdCounter=0; unIdCounter < 10000; unIdCounter++) {
                    
                    unSubElement = document.getElementById( theElement.id + '_' + unIdCounter );
                    
                    if ( unSubElement) {
                        if ( hasClassName( unSubElement, theExistingClass)) {
                            replaceClassName( unSubElement, theExistingClass, theNewClass);
                        }                            
                        if ( theRecurse) {
                            pTRAChangeClassInChildren( unSubElement, theExistingClass, theNewClass, theRecurse);
                        }
                    }
                    else {
                        break;
                    }
                }   
                
                for( var unIdCounter=0; unIdCounter < 10000; unIdCounter++) {
                    
                    unSubElement = document.getElementById( theElement.id + '_exception_' + unIdCounter );
                    
                    if ( unSubElement) {
                        if ( hasClassName( unSubElement, theExistingClass)) {
                            replaceClassName( unSubElement, theExistingClass, theNewClass);
                        }                            
                        if ( theRecurse) {
                            pTRAChangeClassInChildren( unSubElement, theExistingClass, theNewClass, theRecurse);
                        }
                    }
                    else {
                        break;
                    }
                }   
                
                return true;
            }
        </script>
         \n"""
    )
    return None





        
def pWriteExecutionRecordTableHeader( theOutput, ):
    if not theOutput:
        return None
    
    theOutput.write( """
            <thead>
                <tr>
                    <th align="left" valign="top">ms.<br>+-</th>
                    <th align="center" valign="top">exc&nbsp;<br/>!</th>
                    <th align="left" valign="top">name<br>+- all</th>
                    <th align="left" valign="top">kind</th>
                    <th align="left" valign="top">class</th>
                    <th align="left" valign="top">title</th>
                    <th align="left" valign="top">path</th>
                    <th align="left" valign="top">...</th>                    
                </tr>
            </thead>        
        \n"""
    )
    return None









def pRenderExecutionDetailsOn_HTML( theOutput, theExecutionRecord, theNestingLevel=0, theMaxDurationLen=0, theElementId="TRAxredid", theIndentBlock=''):
    if not theExecutionRecord.vInitialized:
        return theExecutionRecord
    
    pWriteExecutionRecordRow(       theOutput, theExecutionRecord, theNestingLevel, theMaxDurationLen, theElementId, theIndentBlock)
    
    if theExecutionRecord.vExceptions:
        pWriteExceptionInfoRows(     theOutput, theExecutionRecord, theNestingLevel + 1, theElementId)
        
        
    unosSubExecutionRecords = theExecutionRecord.vChildren or []
    if not unosSubExecutionRecords:
        return None
    
    unaSubsMaxDurationLen = max( [ len( str( unSubRecord.vExecutionEndTime - unSubRecord.vExecutionStartTime)) for unSubRecord in unosSubExecutionRecords])
    unaSubsDurationSum = sum( [  (unSubRecord.vExecutionEndTime - unSubRecord.vExecutionStartTime) for unSubRecord in unosSubExecutionRecords])
    unaDuration = theExecutionRecord.vExecutionEndTime - theExecutionRecord.vExecutionStartTime
    unaOwnDuration = unaDuration - unaSubsDurationSum
    unaOwnDurationLen = len( str( unaOwnDuration))
    if unaOwnDurationLen > unaSubsMaxDurationLen:
        unaSubsMaxDurationLen = unaOwnDurationLen
        
    unIndentBlock = theIndentBlock        
    unIndentBlock = '%s<font color="gray">|</font>%s' % ( unIndentBlock, cHTMLIndentUnit * theMaxDurationLen )
   
    pWriteOwnExecutionTimeRow( theOutput, theExecutionRecord, theNestingLevel + 1, unaSubsMaxDurationLen, theElementId, unIndentBlock)
    
    for unSubExecutionRecordIndex in range( len( unosSubExecutionRecords)):
        aSubExecutionRecord = unosSubExecutionRecords[ unSubExecutionRecordIndex]
        pRenderExecutionDetailsOn_HTML( theOutput, aSubExecutionRecord, theNestingLevel + 1, unaSubsMaxDurationLen, '%s_%d' % ( theElementId, unSubExecutionRecordIndex), unIndentBlock)

    return None      
   
               



   
    
def pWriteExecutionRecordRow( theOutput, theExecutionRecord, theNestingLevel, theMaxDurationLen, theElementId, theIndentBlock):
    if not theOutput or not theExecutionRecord:
        return None
    
    if not theExecutionRecord.vInitialized:
        return None
    
    
    unaDuration = theExecutionRecord.vExecutionEndTime - theExecutionRecord.vExecutionStartTime
    
    unDurationFiller = ''
    if theMaxDurationLen:
        unDurationFiller = cHTMLDurationFiller * max( 0, theMaxDurationLen - len( str( unaDuration)))
        
    unShowOrHideClass       = ( theNestingLevel and 'TRAstyle_NoDisplay') or  'TRAstyle_Display'
    
    unCollapsedOrWOChildren = ''
    unClickDirectChildren = ''
    unClickAllChildren = ''
    if  theExecutionRecord.vChildren or []:      
        unCollapsedOrWOChildren = 'TRAstyle_Collapsed'
        unClickDirectChildren = """onclick="pTRAExpandOrCollapseDirectChildren( '%s')" """ % theElementId
        unClickAllChildren = """onclick="pTRAExpandOrCollapseAllChildren( '%s')" """% theElementId
    else:
        unCollapsedOrWOChildren = 'TRAstyle_WOChildren'

    
    theOutput.write( """
        <tr id="%(row_id)s" class="TRAExecutionRecord %(collapsed_or_wo_children)s %(show_or_hide_class)s  even">
            <td align="left" valign="top" %(click_direct_children)s >%(time_indent)s%(duration_filler)s%(exec_time)d</td>
            <td align="center" valign="top" ><font color="red"><strong>%(exception_flag)s</strong></font></td>
            <td align="left" valign="top" %(click_all_children)s >%(name_indent)s%(executed_name)s</td>
            <td align="left" valign="top">%(executed_kind)s</td>
            <td align="left" valign="top">%(object_class)s</td>
            <td align="left" valign="top">%(object_title)s</td>
            <td align="left" valign="top">%(object_path)s</td>
            <td align="left" valign="top">%(extra_info)s</td>                    
        </tr>
        \n""" % {
        'url':              theExecutionRecord.vContextualObject.absolute_url(),
        'show_or_hide_class': unShowOrHideClass,
        'time_indent':      theIndentBlock,
        'duration_filler':  unDurationFiller,
        'name_indent':      theIndentBlock,
        'row_id':           theElementId,
        'exec_time':        unaDuration,
        'exception_flag':   ( ( theExecutionRecord.vExceptions or theExecutionRecord.vExceptionsInChildren) and '!') or '',
        'executed_kind':    theExecutionRecord.vExecutedKind or '',
        'executed_name':    theExecutionRecord.vExecutedName or '',
        'object_class':     theExecutionRecord.vContextualObjectClassName or '',
        'object_title':     theExecutionRecord.vContextualObjectTitle or '',
        'object_path':      theExecutionRecord.vContextualObjectPath or '',
        'extra_info':       (' '.join( theExecutionRecord.vExtraExecutionInfo or [])).replace('/', ' '),
        'collapsed_or_wo_children': unCollapsedOrWOChildren,
        'click_direct_children':    unClickDirectChildren,
        'click_all_children':       unClickAllChildren,
        
    })
    return None


    
    




    
def pWriteOwnExecutionTimeRow( theOutput, theExecutionRecord, theNestingLevel, theMaxDurationLen, theElementId, theIndentBlock):
    if not theOutput or not theExecutionRecord:
        return None
    
    if not theExecutionRecord.vInitialized:
        return None
    
    unosSubExecutionRecords = theExecutionRecord.vChildren or []
    if not unosSubExecutionRecords:
        return None
    
    unaDuration = theExecutionRecord.vExecutionEndTime - theExecutionRecord.vExecutionStartTime
    
    unaSubsDurationSum = sum( [  (unSubRecord.vExecutionEndTime - unSubRecord.vExecutionStartTime) for unSubRecord in unosSubExecutionRecords])
    unaOwnDuration = unaDuration - unaSubsDurationSum
    if unaOwnDuration <= 0:
        return None

    
    unDurationFiller = ''
    if theMaxDurationLen:
        unDurationFiller = cHTMLDurationFiller * max( 0, theMaxDurationLen - len( str( unaOwnDuration)))
            
    theOutput.write( """
        <tr class="TRAstyle_Own TRAstyle_NoDisplay" id="%(row_id)s_own" class="TRAExecutionRecord TRAstyle_NoDisplay even">
            <td align="left" valign="top" >%(time_indent)s%(duration_filler)s%(exec_time)d</td>
            <td colspan="7" align="left" valign="top"" >%(name_indent)s--own--</td>
         </tr>
        \n""" % {
        'url':              theExecutionRecord.vContextualObject.absolute_url(),
        'time_indent':      theIndentBlock,
        'duration_filler':  unDurationFiller,
        'name_indent':      cHTMLIndent * theNestingLevel,
        'row_id':           theElementId,
        'exec_time':        unaOwnDuration,
    })
    return None


    

    
def pWriteExceptionInfoRows( theOutput, theExecutionRecord, theNestingLevel, theElementId):
    if not theOutput or not theExecutionRecord:
        return None
    
    if not theExecutionRecord.vInitialized:
        return None
    
    if not theExecutionRecord.vExceptions:
        return None

    
    for unaExceptionIndex in range( len( theExecutionRecord.vExceptions)):
        unaExceptionInfo = theExecutionRecord.vExceptions[ unaExceptionIndex]
        theOutput.write( """
            <tr class="TRAstyle_Exception TRAstyle_NoDisplay  even"  id="%s_exception_%d">
                <td/>
                <td align="left" valign="top" colspan="7">%s</td>
            </tr>
            \n""" % ( theElementId, unaExceptionIndex, unaExceptionInfo.replace( '\n', '<br/>' ))
        )
    
    return None

 




 
    



    
    

 


def fPrintStringDots_HTML( theExecutionRecord,):

    try:
        if not theExecutionRecord.vInitialized:
            return theExecutionRecord
        
        anOutput = StringIO()
        
        pPrintDotsOn_HTML( theExecutionRecord, anOutput)
   
        unString = anOutput.getvalue()
        return unString
    
    except:
        None

    

def pPrintStringDots_HTML(theExecutionRecord, theOutput,):
    if not theExecutionRecord.vInitialized:
        return theExecutionRecord
            
    unTitle = unicode( theExecutionRecord.fPrintString())
    
    unaId   = unTitle.replace( u' ', u'-')
     
    theOutput.write( cCollapsibleBlock_open % ( unaId, unTitle,))
    
    self.pPrintDotsOn( theExecutionRecord, theOutput)

    theOutput.write( cCollapsibleBlock_close)
    
    return theExecutionRecord      
   


def pPrintDotsOn(theExecutionRecord, theOutput):
    if not theExecutionRecord.vInitialized:
        return theExecutionRecord
    
    theOutput.write( '.')
    for unChild in ( theExecutionRecord.vChildren or []):
        unChild.pPrintDotsOn( theOutput)
    return theExecutionRecord      
   


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    










# ######################################
# Rendering utilities
# ######################################




    
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
