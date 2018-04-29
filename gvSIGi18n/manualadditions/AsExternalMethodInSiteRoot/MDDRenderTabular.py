# -*- coding: utf-8 -*-
#
# File: MDDRenderTabular.py
#
# Copyright (c) 2008 by 2008 Model Driven Development sl and Antonio Carrasco Valero
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
# Model Driven Development sl  Valencia (Spain) www.ModelDD.org 
# Antonio Carrasco Valero                       carrasco@ModelDD.org
#

__author__ = """Model Driven Development sl <gvSIGwhys@ModelDD.org>,
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'

import cgi 


from StringIO import StringIO


from Products.CMFCore.utils import getToolByName


cParamsAccess_KeyNotFound_Sentinel = object()

cClasesFilas = [ 'odd','even',]

cNoValueBGColor = 'silver'





cTraversalNames_GeneralReferences_WithTypeColumn = [
    'referentes',
    'referidos',
    'relatedItems',  # ACV 20091204 As of today still not supported (it was, but the generic references view was made obsolete, before this rewrite. Must implement support.
    'todosRelacionados',
    #'referenciasCualificadas',
    #'referentesCualificados',
]



# #######################################################################
""" Utility to escape strings written as HTML.

"""
def fCGIE( theString, quote=1):
    if not theString:
        return theString
    return cgi.escape( theString, quote=quote)
    







        

# #######################################################################
""" PUBLIC VIEW METHOD for Tabular renderings, allowing manipulation of elements to authoried users.
Must be registered as an External method as:
    Id            MDDView_Tabular
    Title         MDDView_Tabular
    Module name   MDDRenderTabular
    Function name MDDView_Tabular

"""
            

    
def MDDView_Tabular( 
    theModelDDvlPloneTool,
    thePerformanceAnalysis  ={},
    theBrowsedElement       =None, 
    theTraversalName        = '',
    theRelationCursorName   = '',
    theCurrentElementUID    = '',
    theRequest              =None, 
    thePasteRequested       =False,
    theGroupAction          ='',
    theUIDs                 =[],
    theMovedElementID       = '',
    theMoveDirection        = '',
    theTranslationsCache    =None,
    thePermissionsCache     =None, 
    theRolesCache           =None,
    theParentExecutionRecord=None,
    theAdditionalParms      ={},):
    """Main service for rendering tabular views for manipulation of the objects network.
    
    Entry point invoked from a template.
    """

        
    if not theModelDDvlPloneTool:
        return pEmptyPageContents(  
            theBrowsedElement, 
            mfTranslateI18N( 'ModelDDvlPlone', cResultCondition_MissingParameter, cResultCondition_MissingParameter + '-'),
            'theModelDDvlPloneTool',
            None
        )
     
    if theBrowsedElement == None:
        return pEmptyPageContents(  
            theBrowsedElement, 
            mfTranslateI18N( 'ModelDDvlPlone', cResultCondition_MissingParameter, cResultCondition_MissingParameter + '-'),
            'theBrowsedElement',
            None
        )
    if not theRequest:
        return pEmptyPageContents(  
            theBrowsedElement, 
            mfTranslateI18N( 'ModelDDvlPlone', cResultCondition_MissingParameter, cResultCondition_MissingParameter + '-'),
            'theRequest',
            None
        ) 
       

    anExtraLinkHrefParams = ''
    if theRequest.get( 'theNoCache', ''):
        anExtraLinkHrefParams = 'theNoCache=1'
        

       
    # #################################################################
    """Initialize root view context structure. Initialize output streaming. Initialize caches if not supplied by service caller

    """
    anOutput = StringIO( u'')
    aModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool.fModelDDvlPloneTool_Retrieval( theBrowsedElement)
    
    aRdCtxt = theModelDDvlPloneTool.fNewRenderContext( 
        theBrowsedElement,
        {
            'theBeginTime':                 theModelDDvlPloneTool.fMillisecondsNow(),
            'theEndTime':                   None,
            'theActionsBeginTime':          None,
            'theActionsEndTime':            None,
            'theRetrievalBeginTime':        None,
            'theRetrievalEndTime':          None,
            'theRenderBeginTime':           None,
            'theRenderEndTime':             None,
            
            'theModelDDvlPloneTool':        theModelDDvlPloneTool,
            'thePerformanceAnalysis':       thePerformanceAnalysis,
            'theBrowsedElement':            theBrowsedElement,
            'theTraversalName':             theTraversalName,
            'theRelationCursorName':        theRelationCursorName,
            'theCurrentElementUID':         theCurrentElementUID,
            
            'theRequest':                   theRequest,
            'thePasteRequested':            thePasteRequested,
            'theGroupAction':               theGroupAction,
            'theUIDs':                      theUIDs,
            'theMovedElementID':            theMovedElementID,
            'theMoveDirection':             theMoveDirection,
    
            'output':                       anOutput,
            'pO':                           lambda theString: anOutput.write( theString),
            'pOL':                          lambda theString: anOutput.write( '%s\n' % theString),
            'pOS':                          lambda theString: anOutput.write( '%s\n' % '\n'.join( [ unaLine.strip() for unaLine in theString.splitlines()])),      
            
            'theMetaTranslationsCaches':    (( theTranslationsCache == None) and aModelDDvlPloneTool_Retrieval.fCreateTranslationsCaches())      or theTranslationsCache,
            'thePermissionsCache':          (( thePermissionsCache == None)  and aModelDDvlPloneTool_Retrieval.fCreateCheckedPermissionsCache()) or thePermissionsCache,
            'theRolesCache':                (( theRolesCache == None)        and aModelDDvlPloneTool_Retrieval.fCreateRolesCache())              or theRolesCache,
            'theUITranslations':            { },
            'theExtraLinkHrefParams':       anExtraLinkHrefParams,
        },
    )

    
    
    

    # #################################################################
    """Retrieve Presentation preferences

    """
    _MDDRetrieve_Preferences_Presentation_Tabular( aRdCtxt)
    
    
    
    

    # #################################################################
    """Manage actions requested, prior to retrieving information and rendering

    """
    aRdCtxt.pSP( 'theActionsBeginTime', theModelDDvlPloneTool.fMillisecondsNow(),)   
    
    _MDDManageActions_Tabular( aRdCtxt)
    
    aRdCtxt.pSP( 'theActionsEndTime', theModelDDvlPloneTool.fMillisecondsNow(),)      
    
    
    
    
    
    # #################################################################
    """Retrieve the information from the element, contents and related, to render the view.
    
    """
    aRdCtxt.pSP( 'theRetrievalBeginTime', theModelDDvlPloneTool.fMillisecondsNow(),)   

    _MDDRetrieve_Info_Tabular( aRdCtxt)
    
    aRdCtxt.pSP( 'theRetrievalEndTime', theModelDDvlPloneTool.fMillisecondsNow(),)      
    
    
    
    aRdCtxt.pOS( '<p>FAST RENDERING</p><br/>')
    
    
    
    # #################################################################
    """Render the view.
    
    """
    aRdCtxt.pSP( 'theRenderBeginTime', theModelDDvlPloneTool.fMillisecondsNow(),) 
    
    _MDDInitUITranslations(            aRdCtxt, cDomainsStringsAndDefaults)

    _MDDRender_ActionsResults_Tabular( aRdCtxt)

    if theRelationCursorName:
        _MDDRender_TabularCursor(    aRdCtxt)
    else:    
        _MDDRender_Tabular(            aRdCtxt)
    
    aRdCtxt.pSP( 'theRenderEndTime', theModelDDvlPloneTool.fMillisecondsNow(),) 
    
    
    aRdCtxt.pSP( 'theEndTime', theModelDDvlPloneTool.fMillisecondsNow())
    
    
    
    
    
    # #################################################################
    """Append profiling information, if so configured.
    
    """
    
    _MDDRender_Tabular_Profiling(      aRdCtxt)
        
    anOutputString = anOutput.getvalue()
    
    aNewOutputString = anOutputString.replace( "\n\n", "\n")
    
    while not ( aNewOutputString == anOutputString):
        anOutputString = aNewOutputString
        aNewOutputString = anOutputString.replace( "\n\n", "\n")
        
    
    return aNewOutputString
    

     
        

        
# #######################################################################
""" ACTION METHODS.

"""
    
     
def _MDDManageActions_Tabular( theRdCtxt):
    
    if theRdCtxt.fGP( 'thePasteRequested', False):
        _MDDManageActions_Tabular_Paste(        theRdCtxt)
    
    if theRdCtxt.fGP( 'theGroupAction',    False):
        _MDDManageActions_Tabular_GroupActions( theRdCtxt)
        
    _MDDManageActions_Tabular_Move(         theRdCtxt)
    
    return None



    
    
    
    
def _MDDManageActions_Tabular_Paste( theRdCtxt):
    
    if not theRdCtxt.fGP( 'thePasteRequested', False):
        return None

    aContainerObject = theRdCtxt.fGP( 'theBrowsedElement', None)
    if aContainerObject == None:
        return None
    
    aBeginTime  = here.ModelDDvlPlone_tool.fMillisecondsNow()
    
    aPasteReport = here.ModelDDvlPlone_tool.fObjectPaste( 
        theTimeProfilingResults =None,
        theContainerObject      =aContainerObject, 
        theAdditionalParams     =None,
    )
    
    anEndTime  = here.ModelDDvlPlone_tool.fMillisecondsNow()
    
    theRdCtxt.pAppendActionResult( {
        'action':       'Paste',
        'begin_time':   aBeginTime,
        'end_time':     anEndTime,
        'report':       aPasteReport,
    })
        
    return None
        
    





    
def _MDDManageActions_Tabular_GroupActions( theRdCtxt):

    aGroupAction         = theRdCtxt.fGP( 'theGroupAction', '')
    if not aGroupAction:
        return None
    
    someGroupUIDs        = theRdCtxt.fGP( 'theUIDs', [])
    if not someGroupUIDs:
        return None
    
    aContainerObject =     theRdCtxt.fGP( 'theBrowsedElement', None)
    if aContainerObject == None:
        return None
    
    aModelDDvlPloneTool =  theRdCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return None
    
    aBeginTime  = aModelDDvlPloneTool.fMillisecondsNow()
    
    aGroupActionReport   = here.ModelDDvlPlone_tool.fGroupAction( 
        theTimeProfilingResults =None,
        theContainerObject      =aContainerObject, 
        theGroupAction          =pGroupAction,
        theGroupUIDs            =pGroupUIDs,
        theAdditionalParams     =None, 
    )
    
    anEndTime  = aModelDDvlPloneTool.fMillisecondsNow()
    
    theRdCtxt.pAppendActionResult( {
        'action':       aGroupAction,
        'begin_time':   aBeginTime,
        'end_time':     anEndTime,
        'report':       aGroupActionReport,
    })
        
    return None

    
    
    
    
    
    
def _MDDManageActions_Tabular_Move( theRdCtxt):
    
    _MDDManageActions_Tabular_MoveElementos(      theRdCtxt)
    
    _MDDManageActions_Tabular_MoveReferencias(    theRdCtxt)
   
    _MDDManageActions_Tabular_MoveElementosPlone( theRdCtxt)
         
    return None





  
def _MDDManageActions_Tabular_MoveElementos( theRdCtxt):
    
    aContainerObject =     theRdCtxt.fGP( 'theBrowsedElement', None)
    if aContainerObject == None:
        return None
    
    aTraversalName =       theRdCtxt.fGP( 'theTraversalName', '')
    if not aTraversalName:
        return None
   
    aMovedElementID =      theRdCtxt.fGP( 'theMovedElementID', '')
    if not aMovedElementID:
        return None
  
    aMoveDirection =       theRdCtxt.fGP( 'theMoveDirection', '')
    if not aMoveDirection:
        return None
    
    aModelDDvlPloneTool =  theRdCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return None
    
    
    aBeginTime  = aModelDDvlPloneTool.fMillisecondsNow()
    
    aMoveResult = aModelDDvlPloneTool.fMoveSubObject( 
        theTimeProfilingResults =None,
        theContainerElement     =aContainerObject,  
        theTraversalName        =aTraversalName, 
        theMovedObjectId        =aMovedElementID, 
        theMoveDirection        =aMoveDirection, 
        theAdditionalParams     =None,
    )
    
    anEndTime  = aModelDDvlPloneTool.fMillisecondsNow()
       
    theRdCtxt.pAppendActionResult( {
        'action':       'Move',
        'begin_time':   aBeginTime,
        'end_time':     anEndTime,
        'report':       aMoveResult,
    })

    return None




        
      
   
def _MDDManageActions_Tabular_MoveReferencias( theRdCtxt):
    
    aContainerObject =      theRdCtxt.fGP( 'theBrowsedElement', None)
    if aContainerObject == None:
        return None

    aTraversalName =        theRdCtxt.fGP( 'theTraversalName', '')
    if not aTraversalName:
        return None
   
    aMovedReferenceUID =    theRdCtxt.fGP( 'theMovedReferenceUID', '')
    if not aMovedReferenceUID:
        return None
  
    aMoveDirection =        theRdCtxt.fGP( 'theMoveDirection', '')
    if not aMoveDirection:
        return None
    
    aModelDDvlPloneTool =  theRdCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return None
    
    
    aBeginTime  = aModelDDvlPloneTool.fMillisecondsNow()
    
    aMoveReferenceResult = aModelDDvlPloneTool.pMoveReferencedObject( 
        theTimeProfilingResults =None,
        theSourceElement        =aContainerObject,  
        theReferenceFieldName   =aTraversalName, 
        theMovedReferenceUID    =aMovedReferenceUID, 
        theMoveDirection        =aMoveDirection, 
        theAdditionalParams     =None,
    )
    
    anEndTime  = aModelDDvlPloneTool.fMillisecondsNow()
       
    theRdCtxt.pAppendActionResult( {
        'action':       'MoveReference',
        'begin_time':   aBeginTime,
        'end_time':     anEndTime,
        'report':       aMoveReferenceResult,
    })

    return None


                


   
def _MDDManageActions_Tabular_MoveElementosPlone( theRdCtxt):
    
    aContainerObject =     theRdCtxt.fGP( 'theBrowsedElement', None)
    if aContainerObject == None:
        return None

    
    aTraversalName =       theRdCtxt.fGP( 'theTraversalName', '')
    if not aTraversalName:
        return None
   
    aMovedObjectUID =      theRdCtxt.fGP( 'theMovedObjectUID', '')
    if not aMovedObjectUID:
        return None
  
    aMoveDirection =       theRdCtxt.fGP( 'theMoveDirection', '')
    if not aMoveDirection:
        return None
    
    aModelDDvlPloneTool =  theRdCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return None
    
    
    aBeginTime  = aModelDDvlPloneTool.fMillisecondsNow()
    
    aMoveReferenceResult = aModelDDvlPloneTool.pMoveReferencedObject( 
        theTimeProfilingResults =None,
        theContainerElement     =aContainerObject,  
        theReferenceFieldName   =aTraversalName, 
        theMovedObjectUID       =aMovedObjectUID, 
        theMoveDirection        =aMoveDirection, 
        theAdditionalParams     =None,
    )
    
    anEndTime  = aModelDDvlPloneTool.fMillisecondsNow()
       
    theRdCtxt.pAppendActionResult( {
        'action':       'MoveReference',
        'begin_time':   aBeginTime,
        'end_time':     anEndTime,
        'report':       aMoveReferenceResult,
    })

    return None


                






# #######################################################################
""" RETRIEVAL METHOD FOR PRESENTATION PREFERENCES.

"""
    
     
def _MDDRetrieve_Preferences_Presentation_Tabular( theRdCtxt):
    
    theRdCtxt.pSP( 'PREFS_PRES', {})

    if True:
        return {}

    aContainerObject =     theRdCtxt.fGP( 'theBrowsedElement', None)
    if aContainerObject == None:
        return None
    
    aModelDDvlPloneTool =  theRdCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return None
    
    aBeginTime  = aModelDDvlPloneTool.fMillisecondsNow()
    
    aPresentationPreferences = aModelDDvlPloneTool.fRetrievePreferences( 
        theTimeProfilingResults     =None,
        theElement                  =aContainerObject, 
        theTypeConfig               =None, 
        theAllTypeConfigs           =None, 
        theViewName                 ='Tabular', 
        thePreferencesExtents       = [ 'presentation'],
        theTranslationsCaches       =None,
        theCheckedPermissionsCache  =None,
        theAdditionalParams         =None
    )
    
    anEndTime  = aModelDDvlPloneTool.fMillisecondsNow()
       
    theRdCtxt.pSP( 'PREFS_PRES', aPresentationPreferences)
    
       
    theRdCtxt.pAppendRetrievalResult( {
        'subject':      'PREFS_PRES',
        'begin_time':   aBeginTime,
        'end_time':     anEndTime,
    })

    return aPresentationPreferences








# #######################################################################
""" RETRIEVAL METHOD FOR ELEMENTS TRAVERSAL DATA, METAINFO AND TRANSLATIONS.

"""
    
     
def _MDDRetrieve_Info_Tabular( theRdCtxt):
    
    
    aContainerObject =     theRdCtxt.fGP( 'theBrowsedElement', None)
    if aContainerObject == None:
        return None
    
    aModelDDvlPloneTool =  theRdCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return None
    
    aBeginTime  = aModelDDvlPloneTool.fMillisecondsNow()
    
    aSRES = aModelDDvlPloneTool.fRetrieveTypeConfig( 
        theTimeProfilingResults     =None,
        theElement                  =aContainerObject, 
        theParent                   =None,
        theParentTraversalName      ='',
        theTypeConfig               =None, 
        theAllTypeConfigs           =None, 
        theViewName                 ='Tabular', 
        theRetrievalExtents         =[ 'traversals', 'owner', 'cursor', 'extra_links',],
        theWritePermissions         =[ 'object', 'aggregations', 'relations', 'add', 'delete', 'add_collection', ],
        theFeatureFilters           =None, 
        theInstanceFilters          =None,
        theTranslationsCaches       =None,
        theCheckedPermissionsCache  =None,
        theAdditionalParams         =None
    )
    
    anEndTime  = aModelDDvlPloneTool.fMillisecondsNow()
       
    theRdCtxt.pSP( 'SRES', aSRES)
    
       
    theRdCtxt.pAppendRetrievalResult( {
        'subject':      'SRES',
        'begin_time':   aBeginTime,
        'end_time':     anEndTime,
    })

    return None

















# #######################################################################
""" LOCALIZATION SUPPORT METHODS.

"""



def _MDDInitUITranslations( theRdCtxt, theDomainsStringsAndDefaults):
    """Preload some translations to use during rendering.
    
    """
    
    aContainerObject = theRdCtxt.fGP( 'theBrowsedElement', None)
    if aContainerObject == None:
        return None
    
    someTranslations = theRdCtxt.fGP( 'theUITranslations', {})

    aModelDDvlPloneTool = theRdCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return None
    
    aModelDDvlPloneTool.fTranslateI18NManyIntoDict( aContainerObject, cDomainsStringsAndDefaults, someTranslations)
    
    for aTranslationKey in someTranslations.keys():
        
        aTranslation = someTranslations.get( aTranslationKey, u'')
        anEncodedTranslation = fCGIE( aTranslation)
        someTranslations[ aTranslationKey] = anEncodedTranslation
        
    return None

    

    
    









# #######################################################################
""" RENDERING METHODS.

"""

        
        
     
def _MDDRender_Tabular_Profiling( theRdCtxt):
    """Append profiling information, if so configured.
    
    """
    
    if theRdCtxt.fGP( 'thePerformanceAnalysis', {}).get( 'processing_times', False) or theRdCtxt.fGP( 'thePerformanceAnalysis', {}).get( 'retrieval_times', False):
        
        aDuration = '?'
        if theRdCtxt.fGP( 'theEndTime', 0) and theRdCtxt.fGP( 'theBeginTime', 0):
            aDuration  = str( theRdCtxt.fGP( 'theEndTime', 0) - theRdCtxt.fGP( 'theBeginTime', 0))

        anActionsDuration = '?'
        if theRdCtxt.fGP( 'theActionsEndTime', 0) and theRdCtxt.fGP( 'theActionsBeginTime', 0):
            anActionsDuration  = str( theRdCtxt.fGP( 'theActionsEndTime', 0) - theRdCtxt.fGP( 'theActionsBeginTime', 0))

        aRetrievalDuration = '?'
        if theRdCtxt.fGP( 'theRetrievalEndTime', 0) and theRdCtxt.fGP( 'theRetrievalBeginTime', 0):
            aRetrievalDuration  = str( theRdCtxt.fGP( 'theRetrievalEndTime', 0) - theRdCtxt.fGP( 'theRetrievalBeginTime', 0))
            
        aRenderDuration = '?'
        if theRdCtxt.fGP( 'theRenderEndTime', 0) and theRdCtxt.fGP( 'theRenderBeginTime', 0):
            aRenderDuration  = str( theRdCtxt.fGP( 'theRenderEndTime', 0) - theRdCtxt.fGP( 'theRenderBeginTime', 0))
    
             
        theRdCtxt.pOS("""
        <br/>
        <table cellspacing="2" cellpadding="2" frame="void">
            <thead>
                <tr>
                    <th>
                        Phase
                    </th>
                    <th>
                        Duration
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>
                        Total
                    </td>
                    <td align="right" >
                        %(Duration)s
                    </td>
                </tr>
                <tr>
                    <td>
                        Actions
                    </td>
                    <td align="right" >
                        %(Actions_Duration)s
                    </td>
                </tr>
                <tr>
                    <td>
                        Retrieval
                    </td>
                    <td align="right" >
                        %(Retrieval_Duration)s
                    </td>
                </tr>
                <tr>
                    <td>
                        Render
                    </td>
                    <td align="right" >
                        %(Render_Duration)s
                    </td>
                </tr>
            <tbody>
        </table>
        <br/>
        """ % {
            'Duration':            aDuration,
            'Actions_Duration':    anActionsDuration,
            'Retrieval_Duration':  aRetrievalDuration,
            'Render_Duration':     aRenderDuration,
        })
                
    return None



 




def _MDDRender_TabularCursor( theRdCtxt):
    """Render a tabular view with the header for an element and the detail of one of its related elements.
    
    """
    return None



    
         


def _MDDRender_Tabular( theRdCtxt):
    """Render a tabular view on an object.
    
    """
        
    # #################################################################
    """Cache some translations to be used in the rendering below

    """

   
    # #################################################################
    """Open Page
    
    """
    theRdCtxt.pOS( u"""     
                    
        <!-- #################################################################
        PAGE WITH CONTENT
        ################################################################# -->
    """)
        

    
    
    _MDDRender_Tabular_Cabecera(                theRdCtxt)
    
    _MDDRender_Tabular_Values(                  theRdCtxt)
    
    _MDDRender_Tabular_Texts(                   theRdCtxt)
    
    _MDDRender_Tabular_CustomPresentationViews( theRdCtxt)
    
    _MDDRender_Tabular_Traversals(  theRdCtxt)
    
    #_MDDRender_Tabular_GenericReferences(  theRdCtxt)
    
    #_MDDRender_Tabular_Plone(  theRdCtxt)
    
    return None





    
def _MDDRender_ActionsResults_Tabular( theRdCtxt):
    
    aTRs   = theRdCtxt.fGP( 'theUITranslations', {})
    someActionsResults = theRdCtxt.fActionResults()

    for anActionResult in someActionsResults:
        anAction = anActionResult.get( 'action', '')
        if anAction:
            
            anActionReport = anActionResult.get( 'report', {})
                
            if anAction == 'Copy':
                if anActionReport:
                    theRdCtxt.pOS("""
                    <div class="portalMessage" tal:content=" =  u'%s %d'/>
                    """ % ( 
                        theRdCtxt.fUITr( 'ModelDDvlPlone_NumElementsCopied'), 
                        anActionReport,
                    ))
                else:
                    theRdCtxt.pOS("""
                    <div class="portalMessage" tal:content=" =  u'%s'/>
                    """ % ( 
                        theRdCtxt.fUITr( 'ModelDDvlPlone_No_items_copied'), 
                        anActionReport,
                    ))
                   
            
            if anAction == 'Cut':
                if anActionReport:
                    theRdCtxt.pOS("""
                    <div class="portalMessage" tal:content=" =  u'%s %d' % ( aTRs( 'ModelDDvlPlone_NumElementsCut',), anActionReport, )" />
                    <div class="portalMessage" tal:content=" =  u'%s %d'/>
                    """ % ( 
                        theRdCtxt.fUITr( 'ModelDDvlPlone_NumElementsCut'), 
                        anActionReport,
                    ))
                else:
                    theRdCtxt.pOS("""
                    <div class="portalMessage" tal:content=" =  u'%s'/>
                    """ % ( 
                        theRdCtxt.fUITr( 'ModelDDvlPlone_No_items_cut'), 
                        anActionReport,
                    ))
 
            if anAction == 'Paste':
                _MDDRenderRefactorResultsDump( theRdCtxt, anActionResult)
                            
    return None

                
            
 
                
                
def _MDDRenderRefactorResultsDump( theRdCtxt, theRefactorReport):
    
    return None



            
            

    
def _MDDRender_Tabular_Cabecera( theRdCtxt):
    
    return None


    
  


    
def _MDDRender_Tabular_Values( theRdCtxt):
 
    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return None
    
    aExcludeTitle = theRdCtxt.fGP( 'ExcludeTitle', True)
    aExcludeID    = theRdCtxt.fGP( 'ExcludeId',    False)
    
    unosNonTextFieldsNames = aSRES.get( 'non_text_field_names', [])
    
    if aExcludeTitle and aExcludeID and ( not unosNonTextFieldsNames):
        return None
    
    theRdCtxt.pOS( u"""
    <table id="hidMDDValues" width="100%%" class="listing" summary="%(ModelDDvlPlone_caracteristicas_tabletitle)s"
        <thead>
            <tr>
                <th class="nosort" align="left">%(ModelDDvlPlone_caracteristicas_tabletitle)s</th>
                <th class="nosort" align="left">%(ModelDDvlPlone_valores_tabletitle)s</th>
            </tr>
        </thead>
        <tbody>
    """ %{
        'ModelDDvlPlone_caracteristicas_tabletitle': theRdCtxt.fUITr( 'ModelDDvlPlone_caracteristicas_tabletitle'),
        'ModelDDvlPlone_valores_tabletitle':         theRdCtxt.fUITr( 'ModelDDvlPlone_valores_tabletitle'),
    })
    

    unIndexClassFila = 0
    
    if not aExcludeID:
        theRdCtxt.pOS( u"""
        <tr id="hidMDDValues_Row_id" class="%(RowClass)s" 
            <td align="left">
                <strong id="hidMDDValores_Row_id_label">%(ModelDDvlPlone_id_label)s</strong>
                &emsp;
                <span   id="hidMDDValores_Row_id_help"class="formHelp">%(ModelDDvlPlone_id_help)s</span>                   
            </td>
            <td align="left" >%(SRES_id)s</td>
        """ %  {
            'RowClass':                                  cClasesFilas[ unIndexClassFila % 2],
            'ModelDDvlPlone_id_label':                   theRdCtxt.fUITr( 'ModelDDvlPlone_id_label'),
            'ModelDDvlPlone_id_help':                    theRdCtxt.fUITr( 'ModelDDvlPlone_id_help'),
            'SRES_id':                                   fCGIE( aSRES.get( 'id', '')),
        })
        
        unIndexClassFila += 1
        
       
    someValueResults = aSRES.get( 'values', [])
    
    for aATTRRES in someValueResults:
        
        if aATTRRES:
            
            unAttributeName = aATTRRES.get( 'attribute_name', '')
            unAttributeConfig = aATTRRES.get( 'attribute_config', '')
            
            if unAttributeName and ( not ( unAttributeName == 'id')) and \
               (( not ( unAttributeName == 'Title')) or ( not aExcludeTitle)) and \
               ( unAttributeName in unosNonTextFieldsNames) and \
               ( not unAttributeConfig.get('exclude_from_values_form', False)) and \
               (( not unAttributeConfig.has_key( 'custom_presentation_view') or not aATTRRES[ 'attribute_config'][ 'custom_presentation_view'])):
                   
                theRdCtxt.pOS( u"""
                <tr id="hidMDDValores_Row_%(attribute_name)s" class="%(RowClass)s" 
                    <td align="left">
                        <strong id="hidMDDValores_Row_%(attribute_name)s_label">%(attribute_label)s</strong>
                        &emsp;
                        <span   id="hidMDDValores_Row_%(attribute_name)s_help" class="formHelp">%(attribute_description)s</span>                   
                    </td>
                """ % {
                    'attribute_name':                            fCGIE( unAttributeName),
                    'attribute_label':                           fCGIE( aATTRRES.get( 'attribute_translations', {}).get( 'translated_label', '')),
                    'attribute_description':                     fCGIE( aATTRRES.get( 'attribute_translations', {}).get( 'translated_description', '')),
                    'RowClass':                                  cClasesFilas[ unIndexClassFila % 2],
                    'ModelDDvlPlone_id_label':                   theRdCtxt.fUITr( 'ModelDDvlPlone_id_label'),
                    'ModelDDvlPlone_id_help':                    theRdCtxt.fUITr( 'ModelDDvlPlone_id_help'),
                })
                
                
                if aATTRRES.get( 'read_permission', False):
                    
                    unAttributeValue = u''
                    if aATTRRES[ 'type'] in [ 'selection', 'boolean']:
                        unAttributeValue = aATTRRES.get( 'translated_value', u'')
                    else:
                        unAttributeValue = aATTRRES.get( 'uvalue', u'')
                        
                    theRdCtxt.pOS( u"""
                    <td id="hidMDDValores_Row_%(attribute_name)s_value" align="left" >%(attribute_value)s</td>
                    """ % {
                        'attribute_name':                        fCGIE( unAttributeName),
                        'attribute_value':                       fCGIE( unAttributeValue),
                    })
                else:
                    theRdCtxt.pOS( u"""
                    <td align="left" bgcolor="%s">&ensp;</td>
                    """ % cNoValueBGColor
                    )
                    
                theRdCtxt.pOS( u"""
                </tr>
                """)
                    
                    
                unIndexClassFila += 1
                        
    theRdCtxt.pOS( u"""
        </tbody>
    </table>
    """)

    return None


    
    
   




    
def _MDDRender_Tabular_Texts( theRdCtxt):
 
    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return None
    
    unosTextFieldsNames = aSRES.get( 'text_field_names', [])
    
    if not unosTextFieldsNames:
        return None
    
    someValueResults = aSRES.get( 'values', [])
    
    for aATTRRES in someValueResults:
        
        if aATTRRES:
            
            unAttributeName   = aATTRRES.get( 'attribute_name', '')
            unAttributeConfig = aATTRRES.get( 'attribute_config', '')
            
            if unAttributeName  and \
               ( unAttributeName in unosTextFieldsNames) and \
               ( not unAttributeConfig.get('exclude_from_values_form', False)) and \
               (( not unAttributeConfig.has_key( 'custom_presentation_view') or not aATTRRES[ 'attribute_config'][ 'custom_presentation_view'])):
                
                theRdCtxt.pOS( u"""
                <table id="hidMDDTexto_%(attribute_name)s_table" width="100%%" class="listing" summary="%(attribute_label)s"
                    <thead>
                        <tr>
                            <th class="nosort" align="left">
                                <strong id="hidMDDTexto_%(attribute_name)s_label">%(attribute_label)s</strong>
                                &emsp;
                                <span   id="hidMDDTexto_%(attribute_name)s_help" class="formHelp">%(attribute_description)s<span/>  
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="odd">
                """ % {
                    'attribute_name':                            fCGIE( unAttributeName),
                    'attribute_label':                           fCGIE( aATTRRES.get( 'attribute_translations', {}).get( 'translated_label', '')),
                    'attribute_description':                     fCGIE( aATTRRES.get( 'attribute_translations', {}).get( 'translated_description', '')),
                    'ModelDDvlPlone_id_label':                   theRdCtxt.fUITr( 'ModelDDvlPlone_id_label'),
                    'ModelDDvlPlone_id_help':                    theRdCtxt.fUITr( 'ModelDDvlPlone_id_help'),
                })
                
                
                if aATTRRES.get( 'read_permission', False):
                    
                    unAttributeValue = aATTRRES.get( 'translated_value', u'')
                    
                    theRdCtxt.pOS( u"""
                    <td>
                        <p id="hidMDDTexto_%(attribute_name)s_para">
                    """% {
                        'attribute_name':                            unAttributeName,
                    })
                    
                    if unAttributeValue:
                        
                        unasLineasTexto = unAttributeValue.splitlines()
                        unNumLineas     = len( unasLineasTexto)

                        unIndexLinea = 0
                        for unaLineaTexto in unasLineasTexto:
                            
                            unaLineaTextoStripped = fCGIE( unaLineaTexto.lstrip())
                            theRdCtxt.pOS( u"""
                            <span>%s%s</span>
                            """ % (  
                                '&ensp;' * ( len( unaLineaTexto) - len( unaLineaTextoStripped)), 
                                unaLineaTextoStripped,
                            ))
                            unIndexLinea += 1
                            if unIndexLinea < unNumLineas:
                                theRdCtxt.pOS( u"""<br/>""")

                                
                                
                    theRdCtxt.pOS( u"""
                        </td>
                    </p>""" )
                else:
                    theRdCtxt.pOS( u"""
                    <td bgcolor="%(cNoValueBGColor)s"><p id="hidMDDTexto_%(attribute_name)s_para" />&ensp;</td>
                    """ % {
                        'cNoValueBGColor':                           cNoValueBGColor,
                        'attribute_name':                            fCGIE( unAttributeName),
                    })
                
                    
                theRdCtxt.pOS( u"""
                    </tr>
                </table>
                <br/>""" )
                        
                        
    return None


    
    






    
def _MDDRender_Tabular_CustomPresentationViews( theRdCtxt):
 
    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return None

    unosTextFieldsNames = aSRES.get( 'text_field_names', [])
    
    if not unosTextFieldsNames:
        return None

    aModelDDvlPloneTool = theRdCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return None
    
    someValueResults = aSRES.get( 'values', [])
    
    for aATTRRES in someValueResults:
        
        if aATTRRES:
            
            unAttributeName   = aATTRRES.get( 'attribute_name', '')
            unAttributeConfig = aATTRRES.get( 'attribute_config', '')
            
            if unAttributeName  and \
               ( unAttributeName in unosTextFieldsNames) and \
               ( not unAttributeConfig.get('exclude_from_values_form', False)) and \
               (( unAttributeConfig.has_key( 'custom_presentation_view') and aATTRRES[ 'attribute_config'][ 'custom_presentation_view'])):
                
                unCustomViewRendering = aModelDDvlPloneTool.fRenderTemplate( aSRES[ 'object'], aATTRRES[ 'attribute_config'][ 'custom_presentation_view'])
                theRdCtxt.pO( unCustomViewRendering)
                
                
    return None









def _MDDRender_Tabular_Traversals( theRdCtxt):
    
 
    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return None
    
    unasTraversals = aSRES.get( 'traversals', [])
    
    if not unasTraversals:
        return None

    for aTRAVRES in unasTraversals:
        
        if aTRAVRES:
            
            aTraversalKind    = aTRAVRES.get( 'traversal_kind', '')
            
            if aTraversalKind == 'aggregation':
                
                aRdCtxt = theRdCtxt.fNewCtxt( {
                    'TRAVRES': aTRAVRES
                })
                
                anIsCollection = aTRAVRES.get( 'is_collection', False)
                
                if anIsCollection:
                    
                    _MDDRender_Tabular_Coleccion_Sola( aRdCtxt)
                    
                else:
                    
                    aContainsCollections = aTRAVRES.get( 'contains_collections', False)
                    
                    if aContainsCollections:
                    
                        _MDDRender_Tabular_ColeccionesEnTabla( aRdCtxt)
                    
                    else:
                        
                        _MDDRender_Tabular_SinColeccionEnTabla( aRdCtxt)
                 
                        
                        
                        
            elif aTraversalKind == 'relation':
                
                aRdCtxt = theRdCtxt.fNewCtxt( {
                    'TRAVRES': aTRAVRES
                })
                
                anIsMultiValued = aTRAVRES.get( 'is_multivalued', False)
                
                if anIsMultiValued:
                    
                    _MDDRender_Tabular_ReferenciasEnTabla( aRdCtxt)
                    
                else:
                    
                    pass #  _MDDRender_Tabular_ReferenciaEnTabla( aRdCtxt)
                    
                
    return None








def _MDDRender_Tabular_Coleccion_Sola( theRdCtxt):
    
 
    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return None
    
    aTRAVRES = theRdCtxt.fGP( 'TRAVRES', {})
    if not aTRAVRES:
        return None
    

    
    someElements = aTRAVRES.get( 'elements', [])
    
    unSiempre = theRdCtxt.fGP( 'theSiempre', True)
    
    
         
    if someElements or unSiempre:
        
        _MDDRender_Tabular_Tabla( theRdCtxt)
        
        
    return None


        


def _MDDRender_Tabular_SinColeccionEnTabla( theRdCtxt):
    
  
    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return None
    
    aTRAVRES = theRdCtxt.fGP( 'TRAVRES', {})
    if not aTRAVRES:
        return None
    
    someElements = aTRAVRES.get( 'elements', [])
    
    unSiempre = theRdCtxt.fGP( 'theSiempre', True)
         
    
    
    if someElements or unSiempre:
        
        theRdCtxt.pOS( u"""
        <h2 id="hidMDDAggr_%(traversal_name)s_label" >%(traversal_label)s</h2>
        <table id="hidMDDTraversal_%(traversal_name)s_table" width="100%%" cellspacing="0" cellpadding="0" frame="void">
            <tr>
                <td id="hidMDDTraversal_%(traversal_name)s_description" align="left" valign="baseline" class="formHelp">%(traversal_description)s</td>
                <td align="right" valign="baseline"> 
                </td>
            </tr>
        </table>
        """ % {
            'traversal_name':           fCGIE( aTRAVRES[ 'traversal_name']),        
            'traversal_label':          fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
            'traversal_description':    fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']),        
        })
        
        _MDDRender_Tabular_Tabla( theRdCtxt)
        
        
    return None

        
 





def _MDDRender_Tabular_ColeccionesEnTabla( theRdCtxt):
    """Render an aggregation traversal containing collections, rendering a header for the traversal, and rendering each contained collection with a header and a table with a row for each collection element.
 
    """
    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return None
    
    aTRAVRES = theRdCtxt.fGP( 'TRAVRES', {})
    if not aTRAVRES:
        return None
    
    aPREFS_PRES = theRdCtxt.fGP( 'PREFS_PRES', {})
    #if not aTRAVRES:
        #return None
    
    
    someElements = aTRAVRES.get( 'elements', [])
    unSiempre = theRdCtxt.fGP( 'theSiempre', True)

    if not( someElements or unSiempre):
        return None
    
    
    # ######################################################
    """Traversal name and description as a prominent header for multiple collections, each of them is rendered below with its own header and table.
    
    """
    theRdCtxt.pOS( u"""
    <h2 id="hidMDDTraversal_%(traversal_name)s_label" >%(traversal_label)s</h2>
    <table id="hidMDDTraversal_%(traversal_name)s_table" width="100%%" cellspacing="0" cellpadding="0" frame="void">
        <tbody>
            <tr>
                <td id="hidMDDTraversal_%(traversal_name)s_description" align="left" valign="baseline" class="formHelp">%(traversal_description)s</td>
                <td align="right" valign="baseline"> 
    """ % {
        'traversal_name':           fCGIE( aTRAVRES[ 'traversal_name']),        
        'traversal_label':          fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
        'traversal_description':    fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']),        
    })

    
    
    # ######################################################
    """Factories to create contained collections.
    
    """
    someFactories = aTRAVRES.get( 'factories', [])
    if someFactories:
    
        unPermiteCrearColecciones = aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
            aSRES[ 'add_permission'] and aSRES[ 'add_collection_permission'] and \
            aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission'] and \
            ( not aTRAVRES[ 'max_multiplicity_reached']) and \
            not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))
        
        if unPermiteCrearColecciones :
            
            if len( someFactories) == 1:
                
                theRdCtxt.pOS( u"""
                <a  id="hidMDDTraversal_%(traversal_name)s_Factory_%(theMetaType)s_Link"
                    href="%(url)sCrear/?theNewTypeName=%(theMetaType)s&theAggregationName=%(traversal_name)s"  
                    title="%(ModelDDvlPlone_crear_action_label)s %(translated_archetype_name)s: %(translated_type_description)s" >
                    
                    <img src="%(portal_url)s/add_icon.gif" id="hidMDDTraversal_%(traversal_name)s_Factory_%(theMetaType)s_Icon"
                        title="%(ModelDDvlPlone_crear_action_label)s %(translated_archetype_name)s: %(translated_type_description)s" 
                        alt="%(ModelDDvlPlone_crear_action_label)s" />
                """ % {
                    'ModelDDvlPlone_crear_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                    'translated_archetype_name':         fCGIE( aTRAVRES[ 'factories'][ 0][ 'type_translations'][ 'translated_archetype_name']),
                    'translated_type_description':       fCGIE( aTRAVRES[ 'factories'][ 0][ 'type_translations'][ 'translated_type_description']),
                    'url':                               aSRES[ 'url'],
                    'theMetaType':                       fCGIE( aTRAVRES[ 'factories'][ 0][ 'meta_type']),
                    'traversal_name':                    fCGIE( aTRAVRES[ 'traversal_name']),
                    'portal_url':                        aSRES[ 'portal_url'],
                })
                
                if aPREFS_PRES.get( 'DisplayActionLabels', False):
                    theRdCtxt.pOS( u"""
                        &nbsp;
                        %(ModelDDvlPlone_crear_action_label)s
                         &nbsp;
                        %(translated_archetype_name)s       
                    """ % {
                        'ModelDDvlPlone_crear_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                        'translated_archetype_name':         fCGIE( aTRAVRES[ 'factories'][ 0][ 'type_translations'][ 'translated_archetype_name']),
                    })
                    
                theRdCtxt.pOS( u"""
                </a>
                """)
                 
            else:
                
                theRdCtxt.pOS( u""" 
                <img src="%(portal_url)s/add_icon.gif" title="%(ModelDDvlPlone_crear_action_label)s " alt="%(ModelDDvlPlone_crear_action_label)s" />
                    &nbsp;
                    %(ModelDDvlPlone_crear_action_label)s
                """ % {
                    'ModelDDvlPlone_crear_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                    'url':                               aSRES[ 'url'],
                    'traversal_name':                    fCGIE( aTRAVRES[ 'traversal_name']),
                    'portal_url':                        aSRES[ 'portal_url'],
                })
                
                for aFactory in someFactories:
                    
                    theRdCtxt.pOS( u"""
                    <a  id="hidMDDTraversal_%(traversal_name)s_Factory_%(theMetaType)s_Link"
                        href="%(url)sCrear/?theNewTypeName=%(theMetaType)s&theAggregationName=%(traversal_name)s"  
                        title="%(ModelDDvlPlone_crear_action_label)s %(translated_archetype_name)s: %(translated_type_description)s" >
                        
                        <img src="%(portal_url)s/add_icon.gif" id="hidMDDTraversal_%(traversal_name)s_Factory_%(theMetaType)s_Icon"
                            title="%(ModelDDvlPlone_crear_action_label)s %(translated_archetype_name)s: %(translated_type_description)s" 
                            alt="%(ModelDDvlPlone_crear_action_label)s" />
                    </a>
                    """ % {
                        'ModelDDvlPlone_crear_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                        'translated_archetype_name':         fCGIE( aTRAVRES[ 'factories'][ 0][ 'type_translations'][ 'translated_archetype_name']),
                        'translated_type_description':       fCGIE( aFactory[ 'type_translations'][ 'translated_type_description']),
                        'url':                               aSRES[ 'url'],
                        'theMetaType':                       fCGIE( aFactory[ 'meta_type']),
                        'traversal_name':                    fCGIE( aTRAVRES[ 'traversal_name']),
                        'portal_url':                        aSRES[ 'portal_url'],
                    })
            
                    if False and aPREFS_PRES.get( 'DisplayActionLabels', False):
                        theRdCtxt.pOS( u"""
                            &nbsp;
                            %(ModelDDvlPlone_crear_action_label)s
                             &nbsp;
                            %(translated_archetype_name)s       
                        """ % {
                            'ModelDDvlPlone_crear_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                            'translated_archetype_name':         fCGIE( aTRAVRES[ 'factories'][ 0][ 'type_translations'][ 'translated_archetype_name']),
                        })
                        
                    theRdCtxt.pOS( u"""
                    </a>
                    """)
                    
                    
    theRdCtxt.pOS( u"""
                </td>
            </tr>
        </tbody>
    </table>
    """)
             
                
    if ( not someElements):
        theRdCtxt.pOS( u"""
        <br/>
        """)
        return None
    
     
                  
    # ######################################################
    """Iterate and drill-down into each contained collection, rendering for each one a title and a table with a row for each collection content element.
    
    """
     
    unIndex = 0
    for aSUBSRES in someElements:
        
        aSubRdCtxt = theRdCtxt.fNewCtxt( {
            'PARENT_SRES':    aSRES,
            'PARENT_TRAVRES': aTRAVRES,
            'SRES':           aSUBSRES,
            'index':          unIndex,
        })
       
        _MDDRender_Tabular_ColeccionEnTabla( aSubRdCtxt)
        
        unIndex += 1
        
    theRdCtxt.pOS( u"""
    <br/>
    """)
    
    return None           
        
        
        
        




        
def _MDDRender_Tabular_ColeccionEnTabla( theRdCtxt):
    """Render a collection, with a header and a table with a row for each collection element.
 
    """

    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return None
 
    
    _MDDRender_Tabular_ColeccionEnTabla_Header( theRdCtxt)
    
    
    someTraversalNames = aSRES.get( 'traversal_names', [])
    
    for aTraversalName in someTraversalNames: 
        """Collections usually have a single traversal for their aggregated contents, but may have many, as any other aggregation traversal config.
        
        """
        
        aTRAVRES = aSRES[ 'traversals_by_name'][ aTraversalName]

        aRdCtxt = theRdCtxt.fNewCtxt( {
            'TRAVRES': aTRAVRES,
        })
        
        _MDDRender_Tabular_Tabla(                  aRdCtxt)

    return None

        



def _MDDRender_Tabular_ColeccionEnTabla_Header( theRdCtxt):
 
    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return None
    
    aPARENT_SRES = theRdCtxt.fGP( 'PARENT_SRES', {})
    if not aPARENT_SRES:
        return None
    
    aTRAVRES = theRdCtxt.fGP( 'TRAVRES', {})
    if not aTRAVRES:
        return None
    
    aPREFS_PRES = theRdCtxt.fGP( 'PREFS_PRES', {})
    #if not aTRAVRES:
        #return None
    
    
    aNumCollections = len( aTRAVRES.get( 'elements', []))
    
    aSRESIndex = theRdCtxt.fGP( 'index', 0)
        
        
    theRdCtxt.pOS( u"""
    <table id="hidMDDCol_%(parent_traversal_name)s_Elem_%(SRES-id)s_Header" 
        width="100%%" cellspacing="0" cellpadding="0" frame="void">
        <tbody>
            <tr>
    """   % {
        'parent_traversal_name':             fCGIE( aTRAVRES[ 'traversal_name']),
        'SRES-id':                           fCGIE( aSRES[ 'id']),
    })
    
    
    
    
    unPermiteOrdenarColecciones = aPARENT_SRES[ 'read_permission'] and aPARENT_SRES[ 'write_permission'] and \
        aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission']
    
    if ( aNumCollections > 1) and unPermiteOrdenarColecciones:
        theRdCtxt.pOS( u"""
        <td align="left" valign="baseline" width="40" >
        """ )
    
        if aSRESIndex:
            theRdCtxt.pOS( u"""
            <a id="hidMDDTraversal_%(traversal_name)s_Elem_%(SRES-id)s_Subir_Link"
                title="%(ModelDDvlPlone_subir_action_label)s %(translated_archetype_name)s %(SRES-title)s"
                href="'%(PARENTSRES-url)sTabular/?theMovedElementID=%(SRES-UID)s&theMoveDirection=Up&theTraversalName=%(traversal_name)s&dd=%(millis)d%(theExtraLinkHrefParams)s#hidMDDElem__%(SRES-UID)s_title" >                
                <img id="hidMDDTraversal_%(traversal_name)s_Elem_%(SRES-id)s_Subir_Icon"
                   alt="%(ModelDDvlPlone_subir_action_label)s %(translated_archetype_name)s %(SRES-title)s" 
                    title="%(ModelDDvlPlone_subir_action_label)s %(translated_archetype_name)s %(SRES-title)s"
                    src="%(portal_url)s/arrowUp.gif" />
            """ % {
                'theExtraLinkHrefParams':              ( theRdCtxt.fGP( 'theExtraLinkHrefParams') and ('&%s' % theRdCtxt.fGP( 'theExtraLinkHrefParams'))) or '',
                'ModelDDvlPlone_subir_action_label':   theRdCtxt.fUITr( 'ModelDDvlPlone_subir_action_label'),
                'translated_archetype_name':           fCGIE( aSRES[ 'type_translations'][ 'translated_archetype_name']), 
                'SRES-title':                          fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                'SRES-id':                             fCGIE( aSRES[ 'id']),
                'PARENTSRES-url':                      aPARENT_SRES[ 'url'],
                'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                'millis':                              theRdCtxt.fGP( 'theModelDDvlPloneTool', None).fMillisecondsNow(), 
                'SRES-UID':                            fCGIE( aSRES[ 'UID']),
                'portal_url':                          aSRES[ 'portal_url'],
            })

        else:
                
            theRdCtxt.pOS( u"""
            <img   alt="Blank" title="Blank" id="icon-blank"  src="%(portal_url)s/arrowBlank.gif" />
            """ % {
                'portal_url':                          aSRES[ 'portal_url'],
            })

        theRdCtxt.pOS( u"""
        &nbsp;
        """ )
                                                                
            
        if not( aSRESIndex == ( aNumCollections - 1)):
            theRdCtxt.pOS( u"""
            <a id="hidMDDTraversal_%(traversal_name)s_Elem_%(SRES-UID)s_Bajar_Link"
                title="%(ModelDDvlPlone_bajar_action_label)s %(translated_archetype_name)s %(SRES-title)s"
                href="'%(PARENTSRES-url)sTabular/?theMovedElementID=%(SRES-UID)s&theMoveDirection=Down&theTraversalName=%(traversal_name)s&dd=%(millis)d%(theExtraLinkHrefParams)s#hidMDDElemento_%(SRES-UID)s_link" >                
                <img  id="hidMDDTraversal_%(traversal_name)s_Elem_%(SRES-UID)s_Bajar_Icon"
                    alt="%(ModelDDvlPlone_bajar_action_label)s %(translated_archetype_name)s %(SRES-title)s" 
                    title="%(ModelDDvlPlone_bajar_action_label)s %(translated_archetype_name)s %(SRES-title)s"
                    src="%(portal_url)s/arrowDown.gif" />
            """ % {
                'theExtraLinkHrefParams':              ( theRdCtxt.fGP( 'theExtraLinkHrefParams') and ('&%s' % theRdCtxt.fGP( 'theExtraLinkHrefParams'))) or '',
                'ModelDDvlPlone_bajar_action_label':   theRdCtxt.fUITr( 'ModelDDvlPlone_bajar_action_label'),
                'translated_archetype_name':           fCGIE( aSRES[ 'type_translations'][ 'translated_archetype_name']), 
                'SRES-title':                          fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                'SRES-id':                             fCGIE( aSRES[ 'id']),
                'PARENTSRES-url':                      aPARENT_SRES[ 'url'],
                'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                'millis':                              theRdCtxt.fGP( 'theModelDDvlPloneTool', None).fMillisecondsNow(), 
                'SRES-UID':                            fCGIE( aSRES[ 'UID']),
                'portal_url':                          aSRES[ 'portal_url'],
            })

        else:
                
            theRdCtxt.pOS( u"""
            <img   alt="Blank" title="Blank" id="icon-blank"  src="%(portal_url)s/arrowBlank.gif" />
            """ % {
                'portal_url':                          aSRES[ 'portal_url'],
            })
            
        theRdCtxt.pOS( u"""
        </td>
        """ )


    theRdCtxt.pOS( u"""
    <td align="left" valign="baseline">
    """ )
            
    aTitleForElement = aSRES[ 'values_by_name'][ 'title'][ 'uvalue']
    if ( aSRES[ 'values_by_name'][ 'title'][ 'uvalue'] == aSRES[ 'archetype_name']):
        aTitleForElement = aSRES[ 'type_translations'][ 'translated_archetype_name']
        
    theRdCtxt.pOS( u"""
    <td align="left" valign="baseline">
        <h3 > 
            <a name="hidMDDElemento_%(SRES-UID)s_link" 
                href="%(SRES-url)sTabular/%(theExtraLinkHrefParams)s" 
                title="%(ModelDDvlPlone_navegara_action_label)s %(translated_archetype_name)s %(Element-title)s" >
                <span id="hidMDDElemento_%(SRES-UID)s_title" class="state-visible">%(Element-title)s</span>
            </a>
        </h3>
    </td>        
    """ % {
        'theExtraLinkHrefParams':              ( theRdCtxt.fGP( 'theExtraLinkHrefParams') and ('?%s' % theRdCtxt.fGP( 'theExtraLinkHrefParams'))) or '',
        'ModelDDvlPlone_navegara_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_navegara_action_label'),
        'translated_archetype_name':           fCGIE( aSRES[ 'type_translations'][ 'translated_archetype_name']), 
        'Element-title':                       fCGIE( aTitleForElement),
        'SRES-id':                             fCGIE( aSRES[ 'id']),
        'PARENTSRES-url':                      aPARENT_SRES[ 'url'],
        'SRES-url':                            aSRES[ 'url'],
        'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
        'millis':                              theRdCtxt.fGP( 'theModelDDvlPloneTool', None).fMillisecondsNow(), 
        'SRES-UID':                            fCGIE( aSRES[ 'UID']),
        'portal_url':                          aSRES[ 'portal_url'],
    })
            

                        
            
    if aSRESIndex:
        theRdCtxt.pOS( u"""
        <td align="left" valign="baseline">
            &nbsp;
            <span class="formHelp">%(translated_type_description)s</span>
        </td>        
        """ % {
            'translated_type_description':           fCGIE( aSRES[ 'type_translations'][ 'translated_type_description']), 
        })
    else:
        theRdCtxt.pOS( u"""
        <td align="left" valign="baseline">
            &nbsp;
        </td>        
        """ )
        
                        
    unPermiteEditarColeccion = aSRES[ 'read_permission'] and aSRES[ 'write_permission'] 
    if unPermiteEditarColeccion:                                
        theRdCtxt.pOS( u"""
        <td width="%(CELL-width)d" align="center" valign="baseline">                                
            <a id="hidMDDTraversal_%(traversal_name)s_Elem_%(SRES-UID)s_Editar_Link"
                href="%(SRES-url)sEditar/'" 
                title="%(ModelDDvlPlone_editar_action_label)s %(translated_archetype_name)s %(SRES-title)s" >
                <img src="%(portal_url)s/edit.gif"
                    alt="%(ModelDDvlPlone_editar_action_label)s" 
                    title="%(ModelDDvlPlone_editar_action_label)s %(translated_archetype_name)s %(SRES-title)s" 
                    id="hidMDDTraversal_%(traversal_name)s_Elem_%(SRES-UID)s_Editar_Icon" />
        """ % {
            'CELL-width':                          (aPREFS_PRES.get( 'DisplayActionLabels', False) and 120) or 20,
            'ModelDDvlPlone_editar_action_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_editar_action_label'),
            'translated_archetype_name':           fCGIE( aSRES[ 'type_translations'][ 'translated_archetype_name']), 
            'SRES-title':                          fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
            'SRES-id':                             fCGIE( aSRES[ 'id']),
            'SRES-url':                            aSRES[ 'url'],
            'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
            'SRES-UID':                            fCGIE( aSRES[ 'UID']),
            'portal_url':                          aSRES[ 'portal_url'],
        })
        
        if aPREFS_PRES.get( 'DisplayActionLabels', False):
            theRdCtxt.pOS( u"""
            <span>%(ModelDDvlPlone_editar_action_label)s</span>        
            """ % {
                'ModelDDvlPlone_editar_action_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_editar_action_label'),
            })

        theRdCtxt.pOS( u"""
            </a>
        </td>
        """)

    unPermiteEliminarColeccion = aPARENT_SRES[ 'read_permission'] and aPARENT_SRES[ 'write_permission'] and \
        aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and aSRES[ 'delete_permission']
        
    if unPermiteEditarColeccion and unPermiteEliminarColeccion:
        theRdCtxt.pOS( u"""
        <td width="20" />
        """)


    if unPermiteEliminarColeccion:                                
        theRdCtxt.pOS( u"""
        <td width="%(CELL-width)d" align="center" valign="baseline" >                                
            <a id="hidMDDTraversal_%(traversal_name)s_Elem_%(SRES-UID)s_Eliminar_Link"
                href="%(SRES-url)sEliminar/'" 
                title="%(ModelDDvlPlone_eliminar_action_label)s %(translated_archetype_name)s %(SRES-title)s" >
                <img src="%(portal_url)s/delete_icon.gif"
                    alt="%(ModelDDvlPlone_eliminar_action_label)s" 
                    title="%(ModelDDvlPlone_eliminar_action_label)s %(translated_archetype_name)s %(SRES-title)s" 
                    id="hidMDDTraversal_%(traversal_name)s_Elem_%(SRES-UID)s_Eliminar_Icon" />
        """ % {
            'CELL-width':                          (aPREFS_PRES.get( 'DisplayActionLabels', False) and 120) or 20,
            'ModelDDvlPlone_eliminar_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_eliminar_action_label'),
            'translated_archetype_name':           fCGIE( aSRES[ 'type_translations'][ 'translated_archetype_name']), 
            'SRES-title':                          fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
            'SRES-id':                             fCGIE( aSRES[ 'id']),
            'SRES-url':                            aSRES[ 'url'],
            'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
            'SRES-UID':                            fCGIE( aSRES[ 'UID']),
            'portal_url':                          aSRES[ 'portal_url'],
        })
        if aPREFS_PRES.get( 'DisplayActionLabels', False):
            theRdCtxt.pOS( u"""
            <span>%(ModelDDvlPlone_eliminar_action_label)s</span>        
            """ % {
                'ModelDDvlPlone_eliminar_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_eliminar_action_label'),
            })
                               
        theRdCtxt.pOS( u"""
            </a>
        </td>
        """)
                    
    theRdCtxt.pOS( u"""
            </tr>
        </tbody>
    </table>
    """ )

        
    unaDescription = aSRES[ 'values_by_name'][ 'description'][ 'uvalue']
    if unaDescription:
        theRdCtxt.pOS( u"""
        <p>%s</p>
        """ % unaDescription)
                 
                
    return None

        












def _MDDRender_Tabular_Tabla( theRdCtxt):
    
  
    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return None
    
    #aPARENT_SRES = theRdCtxt.fGP( 'PARENT_SRES', {})
    #if not aPARENT_SRES:
        #return None
    
    
    aSRESIndex = theRdCtxt.fGP( 'index', 0)
    
    aTRAVRES = theRdCtxt.fGP( 'TRAVRES', {})
    if not aTRAVRES:
        return None
    
    aPARENT_TRAVRES = theRdCtxt.fGP( 'PARENT_TRAVRES', {})
    
    aTableTraversalName = ''
    if aPARENT_TRAVRES:
        aTableTraversalName = aPARENT_TRAVRES[ 'traversal_name']
    else:        
        aTableTraversalName = aTRAVRES[ 'traversal_name']
       
    if not aTableTraversalName:
        return None
    
    aPREFS_PRES = theRdCtxt.fGP( 'PREFS_PRES', {})
    #if not aTRAVRES:
        #return None
    
    someElements  = aTRAVRES.get( 'elements', [])
    unNumElements = len( someElements)
    unSiempre    = theRdCtxt.fGP( 'theSiempre', True)

    
    unIdTabla = 'hidMDDTraversal_%(traversal_name)s_Elem_%(SRES-id)s_Table' % {
        'traversal_name':                     aTableTraversalName,
        'SRES-id':                            aSRES[ 'id'],
    }
    
    theRdCtxt.pOS( u"""
    <table width="100%%" class="listing"  id="hidMDDTraversal_%(traversal_name)s_Elem_%(SRES-id)s_Table"
        summary="%(SRES-title)s">
        <tbody>
            <tr>
    """ % {
            'unIdTabla':                           fCGIE( unIdTabla),
            'ModelDDvlPlone_eliminar_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_eliminar_action_label'),
            'translated_archetype_name':           fCGIE( aSRES[ 'type_translations'][ 'translated_archetype_name']), 
            'SRES-title':                          fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
            'SRES-id':                             fCGIE( aSRES[ 'id']),
            'SRES-url':                            aSRES[ 'url'],
            'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
            'SRES-UID':                            fCGIE( aSRES[ 'UID']),
            'portal_url':                          aSRES[ 'portal_url'],
        })


    
    unPermiteModificarAlgunElemento = False
    for aERES in someElements:
        if aERES[ 'read_permission'] and ( aERES[ 'write_permission'] or aERES[ 'delete_permission']):
            unPermiteModificarAlgunElemento = True
            break
        
        
        
    unPermiteEliminarAlgunElemento = False
    unPermiteEliminarElementos = aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission'] and \
        not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))
    
    if unPermiteEliminarElementos:
        for aERES in someElements:
            if aERES[ 'read_permission'] and ( aERES[ 'write_permission'] or aERES[ 'delete_permission']):
                unPermiteEliminarAlgunElemento = True
                break
                
        
    theRdCtxt.pOS( u"""
    <col width="24" />
    """)
    
    if unPermiteModificarAlgunElemento:
        theRdCtxt.pOS( u"""
        <col width="%d" />
        """ % ( unPermiteEliminarAlgunElemento and 110) or 90 )
        
        
      
    unosColumnNames = aTRAVRES.get( 'column_names', [])
    
    unNumColumnNames =len( unosColumnNames)
    
    theRdCtxt.pOS( u"""
    <col/>
    """ * unNumColumnNames)


    theRdCtxt.pOS( u"""
    <thead>
        <tr>
    """)
    
    
    
    theRdCtxt.pOS( u"""
    <th class="nosort" align="left" >
        <input type="checkbox"  class="noborder"  value=""
            name="%(unIdTabla)s_SelectAll" id="%(unIdTabla)s_SelectAll" 
            onchange="pMDDToggleAllSelections('%(unIdTabla)s'); return true;"/>
    """ %{
    'unIdTabla':                           fCGIE( unIdTabla),
   })


    if not unPermiteModificarAlgunElemento:
        
        _MDDRender_Tabular_MenuAccionesGrupo_Agregaciones( theRdCtxt)
        
        theRdCtxt.pOS( u"""
        </th>
        """)
    else:
        theRdCtxt.pOS( u"""
        </th>
        <th class="nosort" align="left" > 
        """)
        
        _MDDRender_Tabular_MenuAccionesGrupo_Agregaciones( theRdCtxt)
        
        theRdCtxt.pOS( u"""
        </th>
        """)
        
        
        
        
        
    for unColumnName in unosColumnNames:
        theRdCtxt.pOS( u"""
        <th class="nosort" align="left">%s</th>
        """ % fCGIE( aTRAVRES[ 'column_translations'].get( unColumnName, {}).get( 'translated_label', unColumnName))
        )
            
    theRdCtxt.pOS( u"""
        </thead>
    <tbody>
    """ )
            
            
    for unIndexElemento in range( unNumElements):
        
        aERES = someElements[ unIndexElemento]
        aSubRdCtxt = theRdCtxt.fNewCtxt( {
            'ERES' : aERES,
        })
        
        aSubRdCtxt.pOS( u"""
        <tr class="%(Row-Class)s" id="%(unIdTabla)s_RowIndex_%(Row-Index)d" >
        """ % {
            'unIdTabla': fCGIE( unIdTabla),
            'Row-Class': cClasesFilas[ unIndexElemento % 2],
            'Row-Index': unIndexElemento,
        })
        

        aSubRdCtxt.pOS( u"""
        <td align="center" valign="baseline">
            <input type="checkbox"  class="noborder"  value=""
                name="%(unIdTabla)s_Select_%(Row-Index)d"
                id="%(unIdTabla)s_Select_%(Row-Index)d"  />
        </td>
        """ % {
            'Row-Index': unIndexElemento,
            'unIdTabla': fCGIE( unIdTabla),
        })
    
    
            
        if unPermiteModificarAlgunElemento:
            
            aSubRdCtxt.pOS( u"""
            <td align="center" valign="baseline" id="%(unIdTabla)s_%(ERES-UID)s_ChangesLinks_Cell">
            """ % {
                'unIdTabla':                fCGIE( unIdTabla),
                'ERES-UID':                 fCGIE( aERES[ 'UID']),
            })
            
            if aERES[ 'write_permission']:
            
                if aERES[ 'delete_permission']:
                    aSubRdCtxt.pOS( u"""
                    <a  id="%(unIdTabla)s_RowIndex_%(Row-Index)d_Delete_Link"
                        href="%(ERES-url)sEliminar/%(theExtraLinkHrefParams)s" 
                        title="%(ModelDDvlPlone_eliminar_action_label)s %(translated_archetype_name)s %(ERES-title)s" >
                        <img 
                            alt="%(ModelDDvlPlone_eliminar_action_label)s %(translated_archetype_name)s %(ERES-title)s" 
                            title="%(ModelDDvlPlone_eliminar_action_label)s %(translated_archetype_name)s %(ERES-title)s"  
                            id="icon-delete" src="%(portal_url)s/delete_icon.gif"  />
                    </a>
                    &nbsp;    
                                        
                    """ %{
                        'theExtraLinkHrefParams':              ( theRdCtxt.fGP( 'theExtraLinkHrefParams') and ('?%s' % theRdCtxt.fGP( 'theExtraLinkHrefParams'))) or '',
                        'Row-Index':                           unIndexElemento,
                        'unIdTabla':                           fCGIE( unIdTabla),
                        'ModelDDvlPlone_eliminar_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_eliminar_action_label'),
                        'translated_archetype_name':           fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                        'ERES-title':                          fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                        'ERES-url':                            aERES[ 'url'],
                        'portal_url':                          aERES[ 'portal_url'],
                    })
                
                else:
                    aSubRdCtxt.pOS( u"""
                        <img src="%s/blank_icon.gif"  alt="Blank" title="Blank" id="icon-blank" />
                    """ %  aERES[ 'portal_url']
                    )
                    
            
                if aERES[ 'write_permission']:
                    aSubRdCtxt.pOS( u"""
                    <a  id="%(unIdTabla)s_RowIndex_%(Row-Index)d_Edit_Link"
                        href="%(ERES-url)sEditar/%(theExtraLinkHrefParams)s" 
                        title="%(ModelDDvlPlone_editar_action_label)s %(translated_archetype_name)s %(ERES-title)s" >
                        <img 
                            alt="%(ModelDDvlPlone_editar_action_label)s %(translated_archetype_name)s %(ERES-title)s" 
                            title="%(ModelDDvlPlone_editar_action_label)s %(translated_archetype_name)s %(ERES-title)s"  
                            id="icon-edit" src="%(portal_url)s/edit.gif"  />
                    </a>
                    &nbsp;    
                                        
                    """ %{
                        'theExtraLinkHrefParams':              ( theRdCtxt.fGP( 'theExtraLinkHrefParams') and ('?%s' % theRdCtxt.fGP( 'theExtraLinkHrefParams'))) or '',
                        'Row-Index':                           unIndexElemento,
                        'unIdTabla':                           fCGIE( unIdTabla),
                        'ModelDDvlPlone_editar_action_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_editar_action_label'),
                        'translated_archetype_name':           fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                        'ERES-title':                          fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                        'ERES-url':                            aERES[ 'url'],
                        'portal_url':                          aERES[ 'portal_url'],
                    })
                
                else:
                    aSubRdCtxt.pOS( u"""
                        <img src="%s/blank_icon.gif"  alt="Blank" title="Blank" id="icon-blank" />
                    """ %  aERES[ 'portal_url']
                    )
                    
                      
                    
                if unNumElements > 1 and aSRES[ 'write_permission']:
                    
                    if  unIndexElemento:
                        aSubRdCtxt.pOS( u"""
                        <a  id="%(unIdTabla)s_RowIndex_%(Row-Index)d_Subir_Link"
                            href="%(SRES-url)sTabular/?theMovedElementID=%(ERES-id)s&theMoveDirection=Up&theTraversalName=%(traversal_name)s&dd=%(millis)d%(theExtraLinkHrefParams)s#hidMDDElemento_%(ERES-id)s" 
                            title="%(ModelDDvlPlone_subir_action_label)s %(translated_archetype_name)s %(ERES-title)s" >
                            <img 
                                alt="%(ModelDDvlPlone_subir_action_label)s %(translated_archetype_name)s %(ERES-title)s" 
                                title="%(ModelDDvlPlone_subir_action_label)s %(translated_archetype_name)s %(ERES-title)s"  
                                id="icon-edit" src="%(portal_url)s/arrowUp.gif"  />
                        </a>
                        &nbsp;    
                                            
                        """ %{
                            'theExtraLinkHrefParams':              ( theRdCtxt.fGP( 'theExtraLinkHrefParams') and ('&%s' % theRdCtxt.fGP( 'theExtraLinkHrefParams'))) or '',
                            'Row-Index':                           unIndexElemento,
                            'millis':                              theRdCtxt.fGP( 'theModelDDvlPloneTool', None).fMillisecondsNow(), 
                            'unIdTabla':                           fCGIE( unIdTabla),
                            'ModelDDvlPlone_subir_action_label':   theRdCtxt.fUITr( 'ModelDDvlPlone_subir_action_label'),
                            'translated_archetype_name':           fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                            'ERES-title':                          fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                            'ERES-id':                             fCGIE( aERES[ 'id']),
                            'ERES-UID':                            fCGIE( aERES[ 'UID']),
                            'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                            'SRES-url':                            aSRES[ 'url'],
                            'portal_url':                          aERES[ 'portal_url'],
                        })
                    
                    else:
                        aSubRdCtxt.pOS( u"""
                            <img src="%s/arrowBlank.gif"  alt="Blank" title="Blank" id="icon-blank" />
                        """ %  aERES[ 'portal_url']
                        )
                    
                     
                    
                    aSubRdCtxt.pOS( u"""
                    &nbsp;
                    """ )
                    
                       
                    
                    if  unIndexElemento < ( unNumElements -1):
                        aSubRdCtxt.pOS( u"""
                        <a  id="%(unIdTabla)s_RowIndex_%(Row-Index)d_Bajar_Link"
                            href="%(SRES-url)sTabular/?theMovedElementID=%(ERES-id)s&theMoveDirection=Down&theTraversalName=%(traversal_name)s&dd=%(millis)d%(theExtraLinkHrefParams)s#hidMDDElemento_%(ERES-id)s" 
                            title="%(ModelDDvlPlone_bajar_action_label)s %(translated_archetype_name)s %(ERES-title)s" >
                            <img 
                                alt="%(ModelDDvlPlone_bajar_action_label)s %(translated_archetype_name)s %(ERES-title)s" 
                                title="%(ModelDDvlPlone_bajar_action_label)s %(translated_archetype_name)s %(ERES-title)s"  
                                id="icon-edit" src="%(portal_url)s/arrowDown.gif"  />
                        </a>
                        &nbsp;    
                                            
                        """ %{
                            'theExtraLinkHrefParams':              ( theRdCtxt.fGP( 'theExtraLinkHrefParams') and ('&%s' % theRdCtxt.fGP( 'theExtraLinkHrefParams'))) or '',
                            'Row-Index':                           unIndexElemento,
                            'millis':                              theRdCtxt.fGP( 'theModelDDvlPloneTool', None).fMillisecondsNow(), 
                            'unIdTabla':                           fCGIE( unIdTabla),
                            'ModelDDvlPlone_bajar_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_bajar_action_label'),
                            'translated_archetype_name':           fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                            'ERES-title':                          fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                            'ERES-id':                             fCGIE( aERES[ 'id']),
                            'ERES-UID':                            fCGIE( aERES[ 'UID']),
                            'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                            'SRES-url':                            aSRES[ 'url'],
                            'portal_url':                          aERES[ 'portal_url'],
                        })
                    
                    else:
                        aSubRdCtxt.pOS( u"""
                        <img src="%s/arrowBlank.gif"  alt="Blank" title="Blank" id="icon-blank" />
                        """ %  aERES[ 'portal_url']
                        )
                                                                  
            aSubRdCtxt.pOS( u"""
            </td>
            """ )
        
        for unColumnName in unosColumnNames:
            
            aSubRdCtxt.pOS( u"""
            <td align="left" valign="baseline" >
            """ )
             
            if ( unColumnName == 'title') or ( unColumnName.lower().find('title') >= 0) or not ( 'title' in unosColumnNames) and  ( unColumnName == unosColumnNames[ 0]):
                
                unTitle = u'%s %s %s %s %s (%s)' % ( 
                    theRdCtxt.fUITr( 'ModelDDvlPlone_navegara_action_label'), 
                    fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']),
                    fCGIE( aERES[ 'values_by_name'][ unColumnName][ 'uvalue']), 
                    ( not ( unColumnName == 'title')       and  fCGIE( aERES[ 'values_by_name'].get( 'title', {}).get( 'uvalue', ''))) or '', 
                    ( not ( unColumnName == 'description') and  fCGIE( aERES[ 'values_by_name'].get( 'description', {}).get( 'uvalue', ''))) or '',
                    fCGIE( aERES[ 'type_translations'][ 'translated_type_description']),
                )
                
                
                aSubRdCtxt.pOS( u"""
                <a  class="state-visible" 
                    name="hidMDDElemento_%(ERES-UID)s"
                    id="%(unIdTabla)s_RowIndex_%(Row-Index)d_NavegarA_Link"
                    href="%(ERES-url)sTabular/%(theExtraLinkHrefParams)s" 
                    title="%(unTitle)s" >
                    <h4>
                        <img src="%(portal_url)s/%(content_icon)s" 
                            alt="%(unTitle)s" 
                            title="%(unTitle)s" />
                        <span  class="state-visible">%(column_value)s</span>
                    </h4>
                </a>
                &nbsp;    
                                    
                """ %{
                    'theExtraLinkHrefParams':              ( theRdCtxt.fGP( 'theExtraLinkHrefParams') and ('?%s' % theRdCtxt.fGP( 'theExtraLinkHrefParams'))) or '',
                    'Row-Index':                           unIndexElemento,
                    'unTitle':                             fCGIE( unTitle),
                    'millis':                              theRdCtxt.fGP( 'theModelDDvlPloneTool', None).fMillisecondsNow(), 
                    'unIdTabla':                           fCGIE( unIdTabla),
                    'ModelDDvlPlone_navegara_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_navegara_action_label'),
                    'translated_archetype_name':           fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                    'ERES-title':                          fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                    'ERES-id':                             fCGIE( aERES[ 'id']),
                    'ERES-UID':                            fCGIE( aERES[ 'UID']),
                    'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                    'SRES-url':                            aSRES[ 'url'],
                    'ERES-url':                            aSRES[ 'url'],
                    'content_icon':                        fCGIE( aERES[ 'content_icon']),
                    'portal_url':                          aERES[ 'portal_url'],
                    'column_value':                        fCGIE( aERES[ 'values_by_name'][ unColumnName][ 'uvalue']),
                    
                })
                
            else:
                
                unAttributeResult =  aERES[ 'values_by_name'].get( unColumnName, {})
                
                if unAttributeResult:
                    
                    if unAttributeResult[ 'type'] in [ 'selection', 'boolean']:
                        aSubRdCtxt.pOS( u"""
                        <span>%s</span>
                         </tal:block>
                        """ % fCGIE( unAttributeResult.get( 'translated_value', ''))
                        )
                    else:
                        if unAttributeResult[ 'uvalue'] and not ( unAttributeResult[ 'uvalue'] =='None'):
                            aSubRdCtxt.pOS( u"""
                            <span>%s</span>
                            """ % fCGIE( unAttributeResult.get( 'uvalue', '') ))

            aSubRdCtxt.pOS( u"""
            </td>
            """ )
                
                
                        
        aSubRdCtxt.pOS( u"""
        </tr>
        """ )
                                                                           

    theRdCtxt.pOS( u"""
    </tbody>
    """ )
   
    
    unPermiteCrearElementos = aSRES[ 'add_permission'] and aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission'] and ( not aTRAVRES[ 'max_multiplicity_reached']) and \
        not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))
    
    someFactories = aTRAVRES[ 'factories']
    aNumFactories = len( someFactories)

    if unPermiteCrearElementos and aNumFactories:

        theRdCtxt.pOS( u"""
        </tbody>
        <tfoot>
        """ )
    
        if aNumFactories == 1:

            unaFactoriaElemento = someFactories[ 0]
            
            unaVistaCreacion = ( aTRAVRES.get( 'factory_views', None) or {}).get( unaFactoriaElemento[ 'meta_type'], 'Crear')
            

            theRdCtxt.pOS( u"""
            <tr class="%(Row-Class)s" >
                <td colspan="%(theColspan)s" align="center" valign="baseline">
                    <a  id="hidMDDAggregation_%(traversal_name)s_Create_Link"
                        href="%(SRES-url)s%(unaVistaCreacion)s/?theNewTypeName=%(FACTORY-meta_type)s&theAggregationName=%(traversal_name)s"
                        title="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s" >
                        <img id="hidMDDAggregation_%(traversal_name)s_Create_Icon"
                            src="%(portal_url)s/add_icon.gif" 
                            alt="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s"
                            title="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s"/>
                    </a>
                </td>
            """ % {
                'Row-Class':                           cClasesFilas[ unNumElements % 2],    
                'theColspan':                          ( unPermiteModificarAlgunElemento and 2) or 1,
                'unaVistaCreacion':                    unaVistaCreacion,
                'FACTORY-meta_type':                   unaFactoriaElemento[ 'meta_type'],
                'ModelDDvlPlone_crear_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                'SRES-url':                            aSRES[ 'url'],
                'portal_url':                          aSRES[ 'portal_url'],
                'FACTORY-meta_type':                   fCGIE( unaFactoriaElemento[ 'meta_type']),
                'FACTORY-icon':                        fCGIE( unaFactoriaElemento[ 'content_icon']),
                'FACTORY-translated_archetype_name':   fCGIE( unaFactoriaElemento[ 'type_translations'][ 'translated_archetype_name']),
                'FACTORY-translated_type_description': fCGIE( unaFactoriaElemento[ 'type_translations'][ 'translated_type_description']),
            })
                
            theRdCtxt.pOS( u"""
                <td colspan="%(theColspan)s" align="left" valign="baseline">
                    <a  id="hidMDDAggregation_%(traversal_name)s_Create_Link"
                        href="%(SRES-url)s%(unaVistaCreacion)s/?theNewTypeName=%(FACTORY-meta_type)s&theAggregationName=%(traversal_name)s"
                        title="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s" >
                        <img id="hidMDDAggregation_%(traversal_name)s_Create_Icon"
                            src="%(portal_url)s/%(FACTORY-icon)s" 
                            alt="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s"
                            title="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s"/>
                        <span>%(FACTORY-translated_archetype_name)s</span>
                    </a>
                </td>
            </tr>
            """ % {
                'theColspan':                          len( unosColumnNames),
                'unaVistaCreacion':                    fCGIE( unaVistaCreacion),
                'FACTORY-meta_type':                   fCGIE( unaFactoriaElemento[ 'meta_type']),
                'FACTORY-icon':                        fCGIE( unaFactoriaElemento[ 'content_icon']),
                'FACTORY-translated_archetype_name':   fCGIE( unaFactoriaElemento[ 'type_translations'][ 'translated_archetype_name']),
                'FACTORY-translated_type_description': fCGIE( unaFactoriaElemento[ 'type_translations'][ 'translated_type_description']),
                'ModelDDvlPlone_crear_action_label':   theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                'SRES-url':                            aSRES[ 'url'],
                'portal_url':                          aSRES[ 'portal_url'],
                
            })

        else:
            theRdCtxt.pOS( u"""
            <tr class="%(Row-Class)s" >
                <td colspan="%(theColspan)s" align="left" valign="baseline">
            """ % {
                'Row-Class':                           cClasesFilas[ unNumElements % 2],    
                'theColspan':                          (( unPermiteModificarAlgunElemento and 2) or 1) + len( unosColumnNames),
                'ModelDDvlPlone_crear_action_label':   theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
            })
            
            if True or aPREFS_PRES.get( 'DisplayActionLabels', False):
                theRdCtxt.pOS( u"""
                <span>%(ModelDDvlPlone_crear_action_label)s</span>
                &emsp;
                """ % {
                    'ModelDDvlPlone_crear_action_label':   theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                })
            
            for unaFactoriaElemento in someFactories:
                unaVistaCreacion = ( aTRAVRES.get( 'factory_views', None) or {}).get( unaFactoriaElemento[ 'meta_type'], 'Crear')
                theRdCtxt.pOS( u"""
                &emsp;
                <a  id="hidMDDAggregation_%(traversal_name)s_Create_Link"
                    href="%(SRES-url)s%(unaVistaCreacion)s/?theNewTypeName=%(FACTORY-meta_type)s&theAggregationName=%(traversal_name)s"
                    title="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s" >
                    <img id="hidMDDAggregation_%(traversal_name)s_Create_Icon"
                        src="%(portal_url)s/%(FACTORY-icon)s" 
                        alt="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s"
                        title="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s"/>
                    <span>%(FACTORY-translated_archetype_name)s</span>
                </a>
                """ % {
                    'unaVistaCreacion':                    fCGIE( unaVistaCreacion),
                    'FACTORY-meta_type':                   fCGIE( unaFactoriaElemento[ 'meta_type']),
                    'FACTORY-icon':                        fCGIE( unaFactoriaElemento[ 'content_icon']),
                    'FACTORY-translated_archetype_name':   fCGIE( unaFactoriaElemento[ 'type_translations'][ 'translated_archetype_name']),
                    'FACTORY-translated_type_description': fCGIE( unaFactoriaElemento[ 'type_translations'][ 'translated_type_description']),
                    'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                    'SRES-url':                            aSRES[ 'url'],
                    'portal_url':                          aSRES[ 'portal_url'],
                    'ModelDDvlPlone_crear_action_label':   theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                })      

            theRdCtxt.pOS( u"""
                </td>
            </tr>
            """ ) 

    
            theRdCtxt.pOS( u"""
                </td>
            """)
    
    
        theRdCtxt.pOS( u"""
        </tfoot>
        """ )
    
    
    
    

    theRdCtxt.pOS( u"""
    </tr>
    </tfoot>
    </table>
    """ )
   
         
    return None











def _MDDRender_Tabular_MenuAccionesGrupo_Agregaciones( theRdCtxt):
  
    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return None    
    
    #aPARENT_SRES = theRdCtxt.fGP( 'PARENT_SRES', {})
    #if not aPARENT_SRES:
        #return None

    aTRAVRES = theRdCtxt.fGP( 'TRAVRES', {})
    if not aTRAVRES:
        return None
    
    someElements  = aTRAVRES.get( 'elements', [])

        
    unPermitePegarElementos = aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aSRES[ 'add_permission'] and  ( ( not aTRAVRES[ 'contains_collections']) or aSRES[ 'add_collection_permission']) and \
        aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission'] and \
        ( not aTRAVRES[ 'max_multiplicity_reached']) and \
        not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))  
        
    unPermiteOrdenarElementos = aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission'] and \
        not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))  
        
        
        
    unPermiteEliminarAlgunElemento = False
    unPermiteEliminarElementos = aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission'] and \
        not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))
    
    if unPermiteEliminarElementos:
        for anElement in someElements:
            if anElement[ 'read_permission'] and ( anElement[ 'write_permission'] or anElement[ 'delete_permission']):
                unPermiteEliminarAlgunElemento = True
                break
        
        
            
    if not  theRdCtxt.fGP( cAlreadyRendered_MenuAccionesGrupo_JavaScript_PropertyName, False):
        
        theRdCtxt.pOS( cMDDRenderTabular_MenuAccionesGrupo_JavaScript)

        theRdCtxt.pSPGlobal( cAlreadyRendered_MenuAccionesGrupo_JavaScript_PropertyName, True)

         
    theRdCtxt.pOS("""
    <dl class="actionMenu activated" id="%(unIdTabla)s_ActionsMenu" >
        <dt class="actionMenuHeader" style="display: inline">
            <a>%(plone-heading_actions)s</a>
        </dt>
        <dd class="actionMenuContent">
            <ul>
    """ % {
        'unIdTabla':            theRdCtxt.fGP(   'unIdTabla', ''),
        'plone-heading_actions': theRdCtxt.fUITr( 'heading_actions'),
    })
    
       
        
    
    if unPermiteEliminarAlgunElemento:
        theRdCtxt.pOS("""
        <li >
            <a title="%(plone-Cut)s" id="%(unIdTabla)s_MenuAction_Cut_Link"
                onclick="pMDDSubmit_varios( 'Cut', '%(unIdTabla)s'); return true;" >
                <img src="%(portal_url)s/cut_icon.gif"  alt="%(plone-Cut)s" title="%(plone-Cut)s"  />
                <span>%(plone-Cut)s</span>        
            </a>
        </li>
        """ % {
            'unIdTabla':             theRdCtxt.fGP(   'unIdTabla', ''),
            'plone-Cut':             theRdCtxt.fUITr( 'Cut'),
            'portal_url':            aSRES[ 'portal_url'],
        })
        
    if someElements:
        theRdCtxt.pOS("""
        <li >
            <a title="%(plone-Copy)s" id="%(unIdTabla)s_MenuAction_Copy_Link"
                onclick="pMDDSubmit_varios( 'Copy', '%(unIdTabla)s'); return true;" >
                <img src="%(portal_url)s/copy_icon.gif"  alt="%(plone-Copy)s" title="%(plone-Copy)s"  />
                <span>%(plone-Copy)s</span>        
            </a>
        </li>
        """ % {
            'unIdTabla':            theRdCtxt.fGP(   'unIdTabla', ''),
            'plone-Copy':            theRdCtxt.fUITr( 'Copy'),
            'portal_url':            aSRES[ 'portal_url'],
        })
        
        
        
        
    if unPermitePegarElementos:
         
        theRdCtxt.pOS("""
        <li >
            <a title="%(plone-Paste)s" id="%(unIdTabla)s_MenuAction_Paste_Link"
            href="%(SRES-url)sMDDPaste" >
                <img src="%(portal_url)s/paste_icon.gif"  alt="%(plone-Paste)s" title="%(plone-Paste)s"  />
                <span>%(plone-Paste)s</span>        
            </a>
        </li>
        """ % {
            'unIdTabla':            theRdCtxt.fGP(   'unIdTabla', ''),
            'plone-Paste':          theRdCtxt.fUITr( 'Paste'),
            'portal_url':           aSRES[ 'portal_url'],
            'SRES-url':             aSRES[ 'url'],
        })
        
    
    if unPermiteEliminarAlgunElemento:
        theRdCtxt.pOS("""
        <li >
            <a title="%(plone-Delete)s" id="%(unIdTabla)s_MenuAction_Delete_Link"
                onclick="pMDDSubmit_varios( 'Delete', '%(unIdTabla)s'); return true;" >
                <img src="%(portal_url)s/delete_icon.gif"  alt="%(plone-Delete)s" title="%(plone-Delete)s"  />
                <span>%(plone-Delete)s</span>        
            </a>
        </li>
        """ % {
            'unIdTabla':            theRdCtxt.fGP(   'unIdTabla', ''),
            'plone-Delete':          theRdCtxt.fUITr( 'Delete'),
            'portal_url':            aSRES[ 'portal_url'],
        })
        
        
    if unPermiteOrdenarElementos:
        theRdCtxt.pOS("""
        <li >
            <a title="%(plone-Reorder)s" id="%(unIdTabla)s_MenuAction_Reorder_Link"
            href="%(SRES-url)sMDDOrdenar/'" >
                <img src="%(portal_url)s/subirbajar.gif"  alt="%(plone-Reorder)s" title="%(plone-Reorder)s"  />
                <span>%(plone-Reorder)s</span>        
            </a>
        </li>
        """ % {
            'unIdTabla':            theRdCtxt.fGP(   'unIdTabla', ''),
            'plone-Reorder':           theRdCtxt.fUITr( 'Reorder'),
            'portal_url':            aSRES[ 'portal_url'],
            'SRES-url':              aSRES[ 'url'],
        })
        
    theRdCtxt.pOS("""
            </ul>
        </dd>
    </dl>
    """)
    
    
    return None




def _MDDRender_Tabular_ReferenciasEnTabla( theRdCtxt):
    
  
    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return None
    
    aTRAVRES = theRdCtxt.fGP( 'TRAVRES', {})
    if not aTRAVRES:
        return None
    
    theRdCtxt.pSP ( 'thePermiteEnlazarElementos',
        aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission'] and ( not aTRAVRES[ 'max_multiplicity_reached']) and \
        not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))
    )
    
    theRdCtxt.pSP ( 'thePermiteEditarElementos',
        aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission']
    )
    
    theRdCtxt.pSP ( 'thePermiteOrdenarElementos',
        aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission']
    )
    
    theRdCtxt.pSP ( 'thePermiteDesenlazarElementos',
        aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission'] and\
        not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True)) and \
        not (  aTRAVRES.get( 'dependency_supplier', False) == True)
    )
   
    theRdCtxt.pSP ( 'thePermiteModificarElementos', theRdCtxt.fGP ( 'thePermiteOrdenarElementos', False) or  theRdCtxt.fGP ( 'thePermiteDesenlazarElementos', False))

    unIdTabla = 'hidMDDTraversal_%(traversal_name)s_Table' % {
        'traversal_name':                      aTRAVRES[ 'traversal_name'],
    }
    
    
    someElements   = aTRAVRES.get( 'elements', [])
    unNumElements = len( someElements)
    
    unSiempre     = theRdCtxt.fGP( 'theSiempre', True)
         
    
    
    if someElements or unSiempre:
        
        theRdCtxt.pOS( u"""
        <h2 id="hidMDDTraversal_%(traversal_name)s_label" 
            <a  id="hidMDDTraversal_%(traversal_name)s_link"
                title="%(ModelDDvlPlone_recorrercursorrelacion_action_label)s %(traversal_label)s %(ModelDDvlPlone_deorigenrelacioncuandoenlazando)s %(SRES-title)s"
                href="%(SRES-url)sTabular/?theRelationCursorName=%(traversal_name)s%(theExtraLinkHrefParams)s" >
                <span class="state-visible" id="hidMDDTraversal_%(traversal_name)s_title" >%(traversal_label)s</span>
            </a>
        </h2>
        <p class="formHelp">%(traversal_description)s</p>
        """ % {
            'theExtraLinkHrefParams':              ( theRdCtxt.fGP( 'theExtraLinkHrefParams') and ('&%s' % theRdCtxt.fGP( 'theExtraLinkHrefParams'))) or '',
            'ModelDDvlPlone_recorrercursorrelacion_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_recorrercursorrelacion_action_label'),
            'ModelDDvlPlone_deorigenrelacioncuandoenlazando': theRdCtxt.fUITr( 'ModelDDvlPlone_deorigenrelacioncuandoenlazando'),
            'SRES-url':                 aSRES[ 'url'],
            'traversal_name':           fCGIE( aTRAVRES[ 'traversal_name']),        
            'traversal_label':          fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
            'traversal_description':    fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']),  
            'SRES-title':               fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
        })
        
        
        theRdCtxt.pOS( u"""
        <table width="100%%" id="%(unIdTabla)s" class="listing" summary="%(SRES-title)s"  >
        """ % {
            'unIdTabla':                fCGIE( unIdTabla),
            'SRES-title':               fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
        })

        
        theRdCtxt.pOS( u"""
        <col width="24" />
        """)
        
        unTotalColumns = 1
        
        if theRdCtxt.fGP( 'thePermiteModificarElementos', False):
            theRdCtxt.pOS( u"""
            <col width="%d" />
            """ % ( theRdCtxt.fGP ( 'thePermiteDesenlazarElementos', False) and 110 or 90))
            
            unTotalColumns += 1
                
            
        someColumnNames = aTRAVRES.get( 'column_names', [])
        unNumColumnNames =len( someColumnNames)
        
        theRdCtxt.pOS( u"""
        <col/>
        """ * unNumColumnNames)

            
        theRdCtxt.pOS( u"""
        <thead>
            <tr>
        """ )
        
        

    
        theRdCtxt.pOS( u"""
        <th class="nosort" align="left" >
            <input type="checkbox"  class="noborder"  value=""
                name="%(unIdTabla)s_SelectAll" id="%(unIdTabla)s_SelectAll" 
                onchange="pMDDToggleAllSelections('%(unIdTabla)s'); return true;"/>
        """ %{
        'unIdTabla':                           fCGIE( unIdTabla),
        })
    
        
        unPermiteModificarAlgunElemento = False
        for aERES in someElements:
            if aERES[ 'read_permission'] and ( aERES[ 'write_permission'] or aERES[ 'delete_permission']):
                unPermiteModificarAlgunElemento = True
                break
                
        
    
        if not unPermiteModificarAlgunElemento:
            
            _MDDRender_Tabular_MenuAccionesGrupo_Referencias( theRdCtxt)
            
            theRdCtxt.pOS( u"""
            </th>
            """)
        else:
            theRdCtxt.pOS( u"""
            </th>
            <th class="nosort" align="left" > 
            """)
            
            _MDDRender_Tabular_MenuAccionesGrupo_Referencias( theRdCtxt)
            
            theRdCtxt.pOS( u"""
            </th>
            """)
                    
        
        #if theRdCtxt.fGP( 'thePermiteModificarElementos', False):
            #theRdCtxt.pOS( u"""
                #<th align="center" >&ensp;%(ModelDDvlPlone_editar_action_label)s&ensp;</th>
            #""" % {
                #'ModelDDvlPlone_editar_action_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_editar_action_label'),        
            #})


        for unColumnName in someColumnNames:
            
            theRdCtxt.pOS( u"""
            <th class="nosort" align="left" >%s</th>
            """ % fCGIE( aTRAVRES[ 'column_translations'].get( unColumnName, {}).get( 'translated_label', unColumnName)),
            )
            
            unTotalColumns += 1
            
            
            
        if aTRAVRES[ 'traversal_name'] in cTraversalNames_GeneralReferences_WithTypeColumn:
            theRdCtxt.pOS( u"""
            <th class="nosort" width="120" align="left">%(ModelDDvlPlone_tipo_label)s</th>
            <th class="nosort" align="left">&nbsp;%(ModelDDvlPlone_path_label)s&nbsp;</th>
            """ % {
                'ModelDDvlPlone_tipo_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_tipo_label'),        
                'ModelDDvlPlone_path_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_path_label'),        
            })
            
            unTotalColumns += 2

        theRdCtxt.pOS( u"""
        </tr>
        </thead>
        <tbody>
        """ )
            
            
        for unIndexElemento in range( unNumElements):

            aERES = someElements[ unIndexElemento]
            aELEM = aERES.get( 'object', None)
            
            aSubRdCtxt = theRdCtxt.fNewCtxt( {
                'ERES' : aERES,
            })
            
            aSubRdCtxt.pOS( u"""
            <tr class="%(Row-Class)s" id="%(unIdTabla)s_RowIndex_%(Row-Index)d" >
            """ % {
                'unIdTabla': fCGIE( unIdTabla),
                'Row-Class': cClasesFilas[ unIndexElemento % 2],
                'Row-Index': unIndexElemento,
            })
            
    
            aSubRdCtxt.pOS( u"""
            <td align="center" valign="baseline">
                <input type="checkbox"  class="noborder"  value=""
                    name="%(unIdTabla)s_Select_%(Row-Index)d"
                    id="%(unIdTabla)s_Select_%(Row-Index)d"  />
            </td>
            """ % {
                'Row-Index': unIndexElemento,
                'unIdTabla': fCGIE( unIdTabla),
            })
    
            if theRdCtxt.fGP( 'thePermiteModificarElementos', False):
                theRdCtxt.pOS( u"""
                    <td align="center" valign="baseline" id="%(unIdTabla)s_%(ERES-UID)s_ChangesLinks_Cell">
                """ % {
                    'unIdTabla':                fCGIE( unIdTabla),
                    'ERES-UID':                 fCGIE( aERES[ 'UID']),
                })
                
                if theRdCtxt.fGP( 'thePermiteDesenlazarElementos', False):
                    theRdCtxt.pOS( u"""
                        <a id="hidMDDRelation_%(traversal_name)s_%(ERES-UID)s_Unlink_link" 
                            title="%(unActionTitle)s"
                            href="%(SRES-url)sEnlazar/?theReferenceFieldName=%(traversal_name)s&theUnlinkUID=%(ERES-UID)s%(theExtraLinkHrefParams)s" >
                            <img id="hidMDDRelation_%(traversal_name)s_Unlink_icon" 
                               alt="%(unActionTitle)s"
                               title="%(unActionTitle)s" 
                               src="%(portal_url)s/desenlazar.gif" />
                        </a>
                        &nbsp;
                    """ % {
                        'theExtraLinkHrefParams':   ( theRdCtxt.fGP( 'theExtraLinkHrefParams') and ('&%s' % theRdCtxt.fGP( 'theExtraLinkHrefParams'))) or '',
                        'unActionTitle': '%s %s %s %s %s'% ( 
                            theRdCtxt.fUITr( 'ModelDDvlPlone_desenlazar_action_label'),
                            fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),
                            fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                            theRdCtxt.fUITr( 'ModelDDvlPlone_desenlazar_DE'),
                            fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                        ),
                        'unIdTabla':                fCGIE( unIdTabla),
                        'ModelDDvlPlone_desenlazar_DE':  theRdCtxt.fUITr( 'ModelDDvlPlone_desenlazar_DE'),
                        'ModelDDvlPlone_desenlazar_action_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_desenlazar_action_label'),
                        'SRES-url':                 aSRES[ 'url'],
                        'traversal_name':           fCGIE( aTRAVRES[ 'traversal_name']),        
                        'traversal_label':          fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
                        'traversal_description':    fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']),  
                        'SRES-title':               fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                        'ERES-title':               fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                        'portal_url':               aERES[ 'portal_url'],
                        'ERES-UID':                 fCGIE( aERES[ 'UID']),
                    })
            
                
                if theRdCtxt.fGP( 'thePermiteEditarElementos', False)  and aERES[ 'write_permission']:
                    theRdCtxt.pOS( u"""
                        <a id="hidMDDRelation_%(traversal_name)s_%(ERES-UID)s_Edit_link" 
                            title="%(ModelDDvlPlone_editar_action_label)s %(SRES-title)s"
                            href="%(SRES-url)sEditar/%(theExtraLinkHrefParams)s" >
                            <img id="hidMDDRelation_%(traversal_name)s_Edit_icon" 
                               alt="%(ModelDDvlPlone_editar_action_label)s %(SRES-title)s"
                               title="%(ModelDDvlPlone_editar_action_label)s %(SRES-title)s" 
                               src="%(portal_url)s/edit.gif" />
                        </a>
                        &nbsp;
                    """ % {
                        'theExtraLinkHrefParams':   ( theRdCtxt.fGP( 'theExtraLinkHrefParams') and ('&%s' % theRdCtxt.fGP( 'theExtraLinkHrefParams'))) or '',
                        'ModelDDvlPlone_editar_action_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_editar_action_label'),
                        'SRES-url':                 aSRES[ 'url'],
                        'traversal_name':           fCGIE( aTRAVRES[ 'traversal_name']),        
                        'traversal_label':          fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
                        'traversal_description':    fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']),  
                        'SRES-title':               fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                        'portal_url':               aERES[ 'portal_url'],
                        'ERES-UID':                 fCGIE( aERES[ 'UID']),
                    })
                                            
                else:
                    theRdCtxt.pOS( u"""
                        <img src="%(portal_url)s/blank_icon.gif" alt="Blank" title="Blank" id="icon-blank" />
                        &nbsp;
                    """ % {
                        'portal_url':               aERES[ 'portal_url'],
                    })
                    
                                                                                                                    
                    
                if ( unNumElements > 1)  and theRdCtxt.fGP( 'thePermiteOrdenarElementos', False):
                   
                    
                    if unIndexElemento:
                        theRdCtxt.pOS( u"""
                            <a id="hidMDDRelation_%(traversal_name)s_%(ERES-UID)s_Up_link" 
                                title="%(ModelDDvlPlone_subir_action_label)s %(SRES-title)s"
                                href="%(SRES-url)sTabular/?theReferenceFieldName=%(traversal_name)s&theMovedReferenceUID=%(ERES-UID)s&theMoveDirection=Up&dd=%(millis)d%(theExtraLinkHrefParams)s#%(unIdTabla)s_%(ERES-id)s_ChangesLinks_Cell" >
                                <img id="hidMDDRelation_%(traversal_name)s_Up_icon" 
                                   alt="%(ModelDDvlPlone_subir_action_label)s %(SRES-title)s"
                                   title="%(ModelDDvlPlone_subir_action_label)s %(SRES-title)s" 
                                   src="%(portal_url)s/arrowUp.gif" />
                            </a>
                            &nbsp;
                        """ % {
                            'theExtraLinkHrefParams':   ( theRdCtxt.fGP( 'theExtraLinkHrefParams') and ('&%s' % theRdCtxt.fGP( 'theExtraLinkHrefParams'))) or '',
                            'unIdTabla':                fCGIE( unIdTabla),
                            'Row-Index':                unIndexElemento,
                            'millis':                   theRdCtxt.fGP( 'theModelDDvlPloneTool', None).fMillisecondsNow(), 
                            'ModelDDvlPlone_subir_action_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_subir_action_label'),
                            'SRES-url':                 aSRES[ 'url'],
                            'traversal_name':           fCGIE( aTRAVRES[ 'traversal_name']),        
                            'traversal_label':          fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),
                            'traversal_description':    fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']), 
                            'SRES-title':               fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                            'portal_url':               aERES[ 'portal_url'],
                            'ERES-UID':                 fCGIE( aERES[ 'UID']),
                            'ERES-id':                 fCGIE( aERES[ 'id']),
                        })
                        
                    else:

                        theRdCtxt.pOS( u"""
                        <img src="%(portal_url)s/arrowBlank.gif" alt="Blank" title="Blank" id="icon-blank" />
                        &nbsp;
                        """ % {
                            'portal_url':               aERES[ 'portal_url'],
                        })
                        
                        
                   
                    if unIndexElemento < ( unNumElements - 1):
                        theRdCtxt.pOS( u"""
                            <a id="hidMDDRelation_%(traversal_name)s_%(ERES-UID)s_Down_link" 
                                title="%(ModelDDvlPlone_bajar_action_label)s %(SRES-title)s"
                                href="%(SRES-url)sTabular/?theReferenceFieldName=%(traversal_name)s&theMovedReferenceUID=%(ERES-UID)s&theMoveDirection=Down&dd=%(millis)d%(theExtraLinkHrefParams)s#%(unIdTabla)s_%(ERES-id)s_ChangesLinks_Cell" >
                                <img id="hidMDDRelation_%(traversal_name)s_Down_icon" 
                                   alt="%(ModelDDvlPlone_bajar_action_label)s %(SRES-title)s"
                                   title="%(ModelDDvlPlone_bajar_action_label)s %(SRES-title)s" 
                                   src="%(portal_url)s/arrowDown.gif" />
                            </a>
                            &nbsp;
                        """ % {
                            'theExtraLinkHrefParams':   ( theRdCtxt.fGP( 'theExtraLinkHrefParams') and ('&%s' % theRdCtxt.fGP( 'theExtraLinkHrefParams'))) or '',
                            'unIdTabla':                fCGIE( unIdTabla),
                            'Row-Index':                unIndexElemento,
                            'millis':                   theRdCtxt.fGP( 'theModelDDvlPloneTool', None).fMillisecondsNow(), 
                            'ModelDDvlPlone_bajar_action_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_bajar_action_label'),
                            'SRES-url':                 aSRES[ 'url'],
                            'traversal_name':           fCGIE( aTRAVRES[ 'traversal_name']),        
                            'traversal_label':          fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
                            'traversal_description':    fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']),  
                            'SRES-title':               fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                            'portal_url':               aERES[ 'portal_url'],
                            'ERES-UID':                 fCGIE( aERES[ 'UID']),
                            'ERES-id':                  fCGIE( aERES[ 'id']),
                        })
                        
                    else:

                        theRdCtxt.pOS( u"""
                        <img src="%(portal_url)s/arrowBlank.gif" alt="Blank" title="Blank" id="icon-blank" />
                        &nbsp;
                        """ % {
                            'portal_url':               aERES[ 'portal_url'],
                        })
                        
                theRdCtxt.pOS( u"""
                </td>
                """ )
            
                                            
            for unColumnName in someColumnNames:
                
                theRdCtxt.pOS( u"""
                <td align="left" valign="baseline" >
                """)
                 
                if ( unColumnName == 'title') or ( unColumnName.lower().find('title') >= 0) or ( not ( 'title' in someColumnNames) and  ( unColumnName == someColumnNames[ 0])):
                    
                    unTitle = u'%s %s %s %s %s (%s)' % ( 
                        theRdCtxt.fUITr( 'ModelDDvlPlone_navegara_action_label'), 
                        fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']),
                        fCGIE( aERES[ 'values_by_name'][ unColumnName][ 'uvalue']), 
                        ( not ( unColumnName == 'title')       and  fCGIE( aERES[ 'values_by_name'].get( 'title', {}).get( 'uvalue', ''))) or '', 
                        ( not ( unColumnName == 'description') and  fCGIE( aERES[ 'values_by_name'].get( 'description', {}).get( 'uvalue', ''))) or '',
                        fCGIE( aERES[ 'type_translations'][ 'translated_type_description']),
                    )
                    
                    
                    theRdCtxt.pOS( u"""
                    <a  class="state-visible" 
                        name="hidMDDElemento_%(ERES-UID)s"
                        id="%(unIdTabla)s_RowIndex_%(Row-Index)d_NavegarA_Link"
                        href="%(SRES-url)sTabular/%(theExtraLinkHrefParams)s" 
                        title="%(unTitle)s" >
                        <h4>
                            <img src="%(portal_url)s/%(content_icon)s" 
                                alt="%(unTitle)s" 
                                title="%(unTitle)s" />
                            <span  id="hidMDDElemento_%(ERES-UID)s" class="state-visible">%(column_value)s</span>
                        </h4>
                    </a>
                    &nbsp;    
                                        
                    """ %{
                        'theExtraLinkHrefParams':   ( theRdCtxt.fGP( 'theExtraLinkHrefParams') and ('?%s' % theRdCtxt.fGP( 'theExtraLinkHrefParams'))) or '',
                        'Row-Index':                           unIndexElemento,
                        'unTitle':                             fCGIE( unTitle),
                        'millis':                              theRdCtxt.fGP( 'theModelDDvlPloneTool', None).fMillisecondsNow(), 
                        'unIdTabla':                           fCGIE( unIdTabla),
                        'ModelDDvlPlone_navegara_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_navegara_action_label'),
                        'translated_archetype_name':           fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                        'ERES-title':                          fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                        'ERES-id':                             fCGIE( aERES[ 'id']),
                        'ERES-UID':                            fCGIE( aERES[ 'UID']),
                        'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                        'SRES-url':                            aSRES[ 'url'],
                        'content_icon':                        fCGIE( aERES[ 'content_icon']),
                        'portal_url':                          aERES[ 'portal_url'],
                        'column_value':                        fCGIE( aERES[ 'values_by_name'][ unColumnName][ 'uvalue']),
                        
                    })
                    
                else:
                    
                    unAttributeResult =  aERES[ 'values_by_name'].get( unColumnName, {})
                    
                    if unAttributeResult:
                        
                        if unAttributeResult[ 'type'] in [ 'selection', 'boolean']:
                            theRdCtxt.pOS( u"""
                            <span>%s</span>
                            """ % fCGIE( unAttributeResult.get( 'translated_value', ''))
                            )
                        else:
                            if unAttributeResult[ 'uvalue'] and not ( unAttributeResult[ 'uvalue'] =='None'):
                                theRdCtxt.pOS( u"""
                                <span>%s</span>
                                """ % fCGIE( unAttributeResult.get( 'uvalue', '') ))

    
                theRdCtxt.pOS( u"""
                </td>
                """ )
                
            if aTRAVRES[ 'traversal_name'] in cTraversalNames_GeneralReferences_WithTypeColumn:
                theRdCtxt.pOS( u"""
                <td >%(ERES-tipo)s</td>
                <td >%(ERES-path)s</td>
                """ % {
                    'ERES-tipo': fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                    'ERES-path': fCGIE( aERES[ 'path']), 
                })
                
            theRdCtxt.pOS( u"""
            </tr>
            """ )
                        
            
        theRdCtxt.pOS( u"""
        </tbody>
        """ )
            
        if theRdCtxt.fGP( 'thePermiteEnlazarElementos', False) or theRdCtxt.fGP ( 'thePermiteDesenlazarElementos', False):
            
            theRdCtxt.pOS( u"""
            <tfoot>
                <tr class="%(Row-Class)s" >
                    <td colspan="%(colspan)d">
                        <a  id="hidMDDRelation_%(traversal_name)s_ChangeReferences_Link"
                            href="%(SRES-url)sEnlazar/?theReferenceFieldName=%(traversal_name)s%(theExtraLinkHrefParams)s"
                            title="%(ModelDDvlPlone_cambiar_referencias_action_label)s" >
                            <img id="hidMDDRelation_%(traversal_name)s_ChangeReferences_Icon"
                                src="%(portal_url)s/enlazar.gif" 
                                alt="%(ModelDDvlPlone_cambiar_referencias_action_label)s"
                                title="%(ModelDDvlPlone_cambiar_referencias_action_label)s"/>
                                &emsp;
                            <span>%(ModelDDvlPlone_cambiar_referencias_action_label)s</span>
                        </a>
                    </td>
                </tr>
            </tfoot>
            """ % {
                'theExtraLinkHrefParams':                          ( theRdCtxt.fGP( 'theExtraLinkHrefParams') and ('&%s' % theRdCtxt.fGP( 'theExtraLinkHrefParams'))) or '',
                'portal_url':                                      aSRES[ 'portal_url'],
                'SRES-url':                                        aSRES[ 'url'],
                'ModelDDvlPlone_cambiar_referencias_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_cambiar_referencias_action_label'),
                'traversal_name':                                  aTRAVRES[ 'traversal_name'],
                'colspan':                                         unTotalColumns,
                'unIdTabla':                                       fCGIE( unIdTabla),
                'Row-Class':                                       cClasesFilas[ unNumElements % 2],
            })
            
                

            
            
        theRdCtxt.pOS( u"""
        </tbody>
        </table>
        """ )
                        


    return None

        








def _MDDRender_Tabular_MenuAccionesGrupo_Referencias( theRdCtxt):
  
    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return None    
    
    #aPARENT_SRES = theRdCtxt.fGP( 'PARENT_SRES', {})
    #if not aPARENT_SRES:
        #return None

    aTRAVRES = theRdCtxt.fGP( 'TRAVRES', {})
    if not aTRAVRES:
        return None
    
    someElements  = aTRAVRES.get( 'elements', [])

        
    unPermitePegarElementos = aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aSRES[ 'add_permission'] and  ( ( not aTRAVRES[ 'contains_collections']) or aSRES[ 'add_collection_permission']) and \
        aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission'] and \
        ( not aTRAVRES[ 'max_multiplicity_reached']) and \
        not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))  
        
    unPermiteOrdenarElementos = aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission'] and \
        not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))  
        
        
        
    unPermiteDesenlazarAlgunElemento = False
    unPermiteDesenlazarElementos = aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission'] and \
        not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True)) and \
        not (  aTRAVRES.get( 'dependency_supplier', False) == True)
    
    if unPermiteDesenlazarElementos:
        for anElement in someElements:
            if anElement[ 'read_permission'] and ( anElement[ 'write_permission'] or anElement[ 'delete_permission']):
                unPermiteDesenlazarAlgunElemento = True
                break
        
        
            
    if not  theRdCtxt.fGP( cAlreadyRendered_MenuAccionesGrupo_JavaScript_PropertyName, False):
        
        theRdCtxt.pOS( cMDDRenderTabular_MenuAccionesGrupo_JavaScript)

        theRdCtxt.pSPGlobal( cAlreadyRendered_MenuAccionesGrupo_JavaScript_PropertyName, True)

         
    theRdCtxt.pOS("""
    <dl class="actionMenu activated" id="%(unIdTabla)s_ActionsMenu" >
        <dt class="actionMenuHeader" style="display: inline">
            <a>%(plone-heading_actions)s</a>
        </dt>
        <dd class="actionMenuContent">
            <ul>
    """ % {
        'unIdTabla':            theRdCtxt.fGP(   'unIdTabla', ''),
        'plone-heading_actions': theRdCtxt.fUITr( 'heading_actions'),
    })
    
       
        
    
    if unPermiteDesenlazarAlgunElemento:
        theRdCtxt.pOS("""
        <li >
            <a title="%(plone-Cut)s" id="%(unIdTabla)s_MenuAction_Cut_Link"
                onclick="pMDDSubmit_varios( 'CutToUnlink', '%(unIdTabla)s'); return true;" >
                <img src="%(portal_url)s/cut_icon.gif"  alt="%(plone-Cut)s" title="%(plone-Cut)s"  />
                <span>%(plone-Cut)s</span>        
            </a>
        </li>
        """ % {
            'unIdTabla':             theRdCtxt.fGP(   'unIdTabla', ''),
            'plone-Cut':             theRdCtxt.fUITr( 'Cut'),
            'portal_url':            aSRES[ 'portal_url'],
        })
        
    if someElements:
        theRdCtxt.pOS("""
        <li >
            <a title="%(plone-Copy)s" id="%(unIdTabla)s_MenuAction_Copy_Link"
                onclick="pMDDSubmit_varios( 'Copy', '%(unIdTabla)s'); return true;" >
                <img src="%(portal_url)s/copy_icon.gif"  alt="%(plone-Copy)s" title="%(plone-Copy)s"  />
                <span>%(plone-Copy)s</span>        
            </a>
        </li>
        """ % {
            'unIdTabla':            theRdCtxt.fGP(   'unIdTabla', ''),
            'plone-Copy':            theRdCtxt.fUITr( 'Copy'),
            'portal_url':            aSRES[ 'portal_url'],
        })
        
        
        
        
    if unPermitePegarElementos:
        
        theRdCtxt.pOS("""
        <li >
            <a title="%(plone-Paste)s" id="%(unIdTabla)s_MenuAction_Paste_Link"
            href="%(SRES-url)sMDDPasteReferences/?theReferenceFieldName=%(theReferenceFieldName)s" >
                <img src="%(portal_url)s/paste_icon.gif"  alt="%(plone-Paste)s" title="%(plone-Paste)s"  />
                <span>%(plone-Paste)s</span>        
            </a>
        </li>
        """ % {
            'theReferenceFieldName':  aTRAVRES.get( 'traversal_name', ''),
            'unIdTabla':              theRdCtxt.fGP(   'unIdTabla', ''),
            'plone-Paste':            theRdCtxt.fUITr( 'Paste'),
            'portal_url':             aSRES[ 'portal_url'],
            'SRES-url':               aSRES[ 'url'],
        })
        
    
    if unPermiteDesenlazarAlgunElemento:
        theRdCtxt.pOS("""
        <li >
            <a title="%(ModelDDvlPlone_desenlazar_action_label)s" id="%(unIdTabla)s_MenuAction_Unlink"
                onclick="pMDDSubmit_varios( 'Unlink', '%(unIdTabla)s'); return true;" >
                <img src="%(portal_url)s/desenlazar.gif"  alt="%(ModelDDvlPlone_desenlazar_action_label)s" title="%(ModelDDvlPlone_desenlazar_action_label)s"  />
                <span>%(ModelDDvlPlone_desenlazar_action_label)s</span>        
            </a>
        </li>
        """ % {
            'unIdTabla':            theRdCtxt.fGP(   'unIdTabla', ''),
            'ModelDDvlPlone_desenlazar_action_label':          theRdCtxt.fUITr( 'ModelDDvlPlone_desenlazar_action_label'),
            'portal_url':            aSRES[ 'portal_url'],
        })
        
        
    theRdCtxt.pOS("""
            </ul>
        </dd>
    </dl>
    """)
    
    
    return None






def _MDDRenderTabular_Plone( self, theRdCtxt):
    """

    <div metal:define-macro="tColeccionesEnTabla_ElementosPlone_i18n" >
        <tal:block tal:define="global pTrue python: True;
                               global pFalse python: False;
                                    pRetrievalStartTime  python: here.ModelDDvlPlone_tool.fMillisecondsNow();
                                    pProfilingResults python: (pPerformanceAnalysis or {}).get( 'profiling_results', None);
                                    unosArgs python: { 
                                        'theTimeProfilingResults'     :pProfilingResults,
                                        'theContainerElement'         :here, 
                                        'thePloneSubItemsParameters'  :None, 
                                        'theRetrievalExtents'         :[ 'traversals', ],
                                        'theWritePermissions'         :[ 'object', 'aggregations', 'add', 'plone', 'delete_plone', ],
                                        'theFeatureFilters'           :None, 
                                        'theInstanceFilters'          :None,
                                        'theTranslationsCaches'       :None,
                                        'theCheckedPermissionsCache'  :None,
                                        'theAdditionalParams'         :None};                                    
                                    PLONERES  python: here.ModelDDvlPlone_tool.fRetrievePloneContent( **unosArgs);
                                    pRetrievalEndTime  python: here.ModelDDvlPlone_tool.fMillisecondsNow();"
            tal:condition="PLONERES/traversals" > 
    
            <tal:block tal:repeat="TRAVRES PLONERES/traversals">
                <tal:block tal:define="            
                                    pPermiteOrdenarElementos    pPermiteOrdenarElementos | pTrue;
                                    pPermiteOrdenarElementos    python: pPermiteOrdenarElementos and PLONERES[ 'read_permission'] and PLONERES[ 'write_permission'] and TRAVRES[ 'read_permission'] and TRAVRES[ 'write_permission'];
                                    pPermiteCrearElementos      pPermiteCrearElementos | pTrue;
                                    pPermiteCrearElementos      python: pPermiteCrearElementos and PLONERES[ 'add_permission']  and PLONERES[ 'read_permission'] and PLONERES[ 'write_permission'] and TRAVRES[ 'read_permission'] and TRAVRES[ 'write_permission'];
                                    pPermiteEditarElementos     pPermiteEditarElementos | pTrue;
                                    pPermiteEditarElementos     python: pPermiteEditarElementos and PLONERES[ 'read_permission'] and PLONERES[ 'write_permission'] and TRAVRES[ 'read_permission'] and TRAVRES[ 'write_permission'];
                                    pPermiteEliminarElementos   pPermiteEliminarElementos | pTrue;
                                    pPermiteEliminarElementos   python: pPermiteEliminarElementos and PLONERES[ 'read_permission'] and PLONERES[ 'write_permission'] and TRAVRES[ 'read_permission'] and TRAVRES[ 'write_permission']">
            
            
                    <h2 id="#" tal:attributes="id string:aggregation-${TRAVRES/traversal_name}"
                        tal:content="TRAVRES/traversal_translations/translated_label" />
                        
                    <p class="formHelp" tal:content="TRAVRES/traversal_translations/translated_description" />
        
                    <table 
                        tal:define="
                           global unIndexClassFila python: 0;
                           unasClasesFilas  python: ('odd','even')"
                        width="100%%" id="hidColeccionesEnTabla_ElementosPlone" class="listing" summary="#"  tal:attributes="summary TRAVRES/traversal_translations/translated_label">
            
                        <thead>
                            <tr>
                                <th align="center" tal:condition="python: pPermiteOrdenarElementos or pPermiteEditarElementos or pPermiteEliminarElementos" 
                                    class="nosort" width="100" align="left">
                                    <span i18n:domain="ModelDDvlPlone"  i18n:translate="ModelDDvlPlone_editar_action_label">&nbsp;Editar&nbsp;</span>
                                </th>
                                <th class="nosort" width="80" align="left" i18n:domain="ModelDDvlPlone"  i18n:translate="ModelDDvlPlone_tipo_label">&nbsp;Tipo&nbsp;</th>
                                <th class="nosort"  align="left"  i18n:domain="ModelDDvlPlone" i18n:translate="ModelDDvlPlone_titulo_label">&nbsp;T&iacute;tulo&nbsp;</th>
                                <th class="nosort"  align="left"  i18n:domain="ModelDDvlPlone" i18n:translate="ModelDDvlPlone_descripcion_label">&nbsp;Descripci&oacute;n&nbsp;</th>
                                <th class="nosort"  align="left"  i18n:domain="ModelDDvlPlone" i18n:translate="ModelDDvlPlone_PloneContent_attr_details_label">&nbsp;Detalles&nbsp;</th>
                            </tr>
                        </thead>
                        <tbody>
                        
                        
                       
    <tal:block tal:replace="nothing">  
    <tal:block tal:replace="structure python: here.ModelDDvlPlone_tool.fPrettyPrintHTML( [ TRAVRES  , ], [ 'object',  'values_by_uid', 'values_by_name', 'elements_by_UID', 'elements_by_id',  'traversals_by_name', 'type_config', 'traversal_config', 'column_translations',   'vocabulary_translations', ], here.ModelDDvlPlone_tool.fPreferredResultDictKeysOrder() )" />
    </tal:block> 
                           
    
    
                            <tr tal:define="pNavegarALabel python: here.ModelDDvlPlone_tool.fTranslateI18N( here,  'ModelDDvlPlone', 'ModelDDvlPlone_navegara_action_label', 'Navegar a')"
                                tal:repeat="unElemento TRAVRES/elements"
                                class="#" tal:attributes="class python: unasClasesFilas[unIndexClassFila % 2]">
                                <td tal:condition="python: pPermiteOrdenarElementos or pPermiteEditarElementos or pPermiteEliminarElementos" align="center">
                                    <tal:block tal:condition="python: pPermiteEliminarElementos and unElemento[ 'write_permission'] and unElemento[ 'delete_permission']">
                                        <a tal:define="unTituloAccion python: u'%s %s %s' % ( here.ModelDDvlPlone_tool.fTranslateI18N( here,  'ModelDDvlPlone', 'ModelDDvlPlone_eliminar_action_label', 'Editar'), unElemento[ 'type_translations'][ 'translated_archetype_name'], unElemento[ 'values_by_name'][ 'title'][ 'uvalue'])"
                                            href="#" title="#" 
                                            tal:attributes="title unTituloAccion; href  python: u'%sEliminarPlone?theUIDToDelete=%s' % ( PLONERES[ 'url'], unElemento[ 'UID']) " >
                                            <img alt="#" title="#" id="icon-delete" src="#" 
                                                tal:attributes="src python: '%s/delete_icon.gif' % here.portal_url(); alt python: unTituloAccion; title python: unTituloAccion" />
                                        </a>
                                    </tal:block>
                                    <tal:block tal:condition="python: not( pPermiteEliminarElementos and unElemento[ 'write_permission'] and unElemento[ 'delete_permission'])">
                                        <img src="#" tal:attributes="src python: '%s/blank_icon.gif' % here.portal_url()" 
                                            alt="Blank" title="Blank" id="icon-blank" />
                                    </tal:block>   
                                    &nbsp;                                        
                                    <tal:block tal:condition="python: pPermiteEditarElementos and unElemento[ 'write_permission']">
                                        <a tal:define="unTituloAccion python: u'%s %s %s' % ( here.ModelDDvlPlone_tool.fTranslateI18N( here,  'ModelDDvlPlone', 'ModelDDvlPlone_editar_action_label', 'Editar'), unElemento[ 'type_translations'][ 'translated_archetype_name'], unElemento[ 'values_by_name'][ 'title'][ 'uvalue'])"
                                            href="#" title="#" 
                                            tal:attributes="title unTituloAccion; href  python: u'%sbase_edit' % unElemento[ 'url']" >
                                           <img src="#" tal:attributes="title unTituloAccion; src python: '%s/edit.gif' % here.portal_url()" alt="Editar" title="#" id="icon-edit"
                                                        i18n:domain="ModelDDvlPlone" i18n:attributes="alt ModelDDvlPlone_editar_action_label" >
                                        </a>
                                    </tal:block>
                                    <tal:block tal:condition="python: not ( pPermiteEliminarElementos  and unElemento[ 'write_permission'])" >
                                        <img src="#" tal:attributes="src python: '%s/blank_icon.gif' % here.portal_url()" 
                                            alt="Blank" title="Blank" id="icon-blank" />
                                    </tal:block>   
                                    <tal:block tal:condition="python: pPermiteOrdenarElementos and len( TRAVRES[ 'elements']) > 1">
                                        &nbsp;
                                        <tal:block tal:condition="python: not unElemento == TRAVRES[ 'elements'][ 0]">
                                            <a tal:define="unTituloAccion python: u'%s %s %s' % ( here.ModelDDvlPlone_tool.fTranslateI18N( here,  'ModelDDvlPlone', 'ModelDDvlPlone_subir_action_label', 'Subir'), unElemento[ 'type_translations'][ 'translated_archetype_name'], unElemento[ 'values_by_name'][ 'title'][ 'uvalue'])"
                                                href="#" title="#" 
                                                tal:attributes="title unTituloAccion; href python: '%sTabular/?theTraversalName=%s&theMovedObjectUID=%s&theMoveDirection=Up&dd=%d#elemento-%s' % ( PLONERES[ 'url'], TRAVRES[ 'traversal_name'], unElemento[ 'UID'], here.ModelDDvlPlone_tool.fMillisecondsNow(), unElemento[ 'UID'] )">                
                                                <img src="#" title="#" tal:attributes="title unTituloAccion; src python: '%s/arrowUp.gif' % here.portal_url()" 
                                                    alt="Subir" title="#" id="icon-up"
                                                    i18n:domain="ModelDDvlPlone" i18n:attributes="alt ModelDDvlPlone_subir_action_label">
                                            </a>
                                        </tal:block>
                                        <tal:block tal:condition="python: unElemento == TRAVRES[ 'elements'][ 0]">
                                            <img src="#" tal:attributes="src python: '%s/arrowBlank.gif' % here.portal_url()" 
                                                alt="Blank" title="Blank" id="icon-blank">
                                        </tal:block>   
                                        &nbsp;                                    
                                        <tal:block tal:condition="python: not unElemento == TRAVRES[ 'elements'][ len( TRAVRES[ 'elements']) - 1]">
                                            <a tal:define="unTituloAccion python: u'%s %s %s' % ( here.ModelDDvlPlone_tool.fTranslateI18N( here,  'ModelDDvlPlone', 'ModelDDvlPlone_bajar_action_label', 'Bajar'), unElemento[ 'type_translations'][ 'translated_archetype_name'], unElemento[ 'values_by_name'][ 'title'][ 'uvalue'])"
                                                href="#" title="#"
                                                tal:attributes="title unTituloAccion; href python: '%sTabular/?theTraversalName=%s&theMovedObjectUID=%s&theMoveDirection=Down&dd=%d#elemento-%s' % ( PLONERES[ 'url'], TRAVRES[ 'traversal_name'], unElemento[ 'UID'], here.ModelDDvlPlone_tool.fMillisecondsNow(), unElemento[ 'UID'] )">                
                                                <img src="#" tal:attributes="title unTituloAccion; src python: '%s/arrowDown.gif' % here.portal_url()" 
                                                    alt="Bajar" title="#" id="icon-down"
                                                    i18n:domain="ModelDDvlPlone" i18n:attributes="alt ModelDDvlPlone_bajar_action_label">
                                            </a>
                                        </tal:block>
                                        <tal:block tal:condition="python: unElemento == TRAVRES[ 'elements'][ len( TRAVRES[ 'elements']) - 1]">
                                            <img src="#" tal:attributes="src python: '%s/arrowBlank.gif' % here.portal_url()" 
                                                alt="Blank" title="Blank" id="icon-blank">
                                        </tal:block>                                       
                                    </tal:block>
                                </td>
    
                                <td  align="left" valign="baseline" tal:content="python: unElemento[ 'type_translations'][ 'translated_archetype_name']" />
    
                                <td align="left" valign="baseline" >
                                   <span class="visualIcon contenttype-xxx" tal:attributes="class python: 'visualIcon contenttype-%s' % unElemento[ 'portal_type'].lower().replace(' ', '-')">
                                       <h4>
                                           <a name="#" href="#" title="#"
                                               tal:define="
                                                   unTitle python: '%s %s %s (%s)' % ( 
                                                   pNavegarALabel, 
                                                   unElemento[ 'type_translations'][ 'translated_archetype_name'],
                                                   unElemento[ 'values_by_name'][ 'title'][ 'uvalue'], 
                                                   unElemento[ 'type_translations'][ 'translated_type_description'])"                          
                                               tal:attributes="title unTitle; name string:elemento-${unElemento/UID}; href python: (( unElemento[ 'meta_type'] in [ 'ATLink', 'ATDocument', 'ATFile', 'ATImage', 'ATNewsItem',]) and '%sview' % unElemento['url']) or unElemento['url']"
                                               class="state-visible visualIconPadding" title="">
                                               <span tal:content="unElemento/values_by_name/title/uvalue" />
                                           </a>
                                       </h4>
                                   </span>
                                </td>
                                <td align="left" valign="baseline" tal:content="unElemento/values_by_name/description/uvalue" />
                                <td align="left" valign="baseline">
                                    <tal:block tal:condition="python: unElemento[ 'meta_type'] == 'ATImage'">
                                        <a  href="#" alt="#" title="#" 
                                            tal:attributes="href string:${unElemento/url}/view; alt unElemento/title; title unElemento/title" > 
                                            <img src="#" alt="#" title="#" height="64" 
                                                tal:attributes="src unElemento/values_by_name/content_url/value; alt unElemento/title; title unElemento/title" />    
                                        </a>
                                    </tal:block>
                                    
                                    <tal:block tal:condition="python: unElemento[ 'meta_type'] == 'ATLink'">
                                        <a href="#" alt="#" title="#" 
                                            tal:attributes="href string:${unElemento/url}/view; alt unElemento/title; title unElemento/title"
                                            tal:content="unElemento/values_by_name/content_url/value" />    
                                    </tal:block>
        
                                    <tal:block tal:condition="python: unElemento[ 'meta_type'] == 'ATDocument'">
                                        <a  tal:condition="python: unElemento[ 'values_by_name'][ 'text'][ 'uvalue']"
                                            href="#" alt="#" title="#" 
                                            tal:attributes="href string:${unElemento/url}/view; alt unElemento/title; title unElemento/title"
                                            tal:content="python: unElemento[ 'values_by_name'][ 'text'][ 'uvalue'][:64]" />    
                                    </tal:block>
                                    
                                    <tal:block tal:condition="python: unElemento[ 'meta_type'] == 'ATNewsItem'">
                                        <a  tal:condition="python: unElemento[ 'values_by_name'][ 'text'][ 'uvalue']"
                                            href="#" alt="#" title="#" 
                                            tal:attributes="href string:${unElemento/url}/view; alt unElemento/title; title unElemento/title" > 
                                            <img src="#" alt="#" title="#" height="64" tal:condition="python: unElemento[ 'values_by_name'][ 'content_url'][ 'value']"
                                                tal:attributes="src unElemento/values_by_name/image_url/value; alt unElemento/title; title unElemento/title" />    
                                            <span tal:content="python: unElemento[ 'values_by_name'][ 'text'][ 'uvalue'][:64]" />
                                        </a>
                                    </tal:block>
        
                                    <tal:block tal:condition="python: unElemento[ 'meta_type'] == 'ATFile'">
                                        <a  href="#" alt="#" title="#" 
                                            tal:attributes="href string:${unElemento/url}/view; alt unElemento/title; title unElemento/title" 
                                            tal:content="unElemento/values_by_name/content_url/value" />   
                                    </tal:block>
        
                                </td>
                                <tal tal:define="global  unIndexClassFila   python: unIndexClassFila + 1" />
                            </tr>
                        </tbody>
                       
                        
                        <tfoot>
                            <tal:block tal:condition="pPermiteCrearElementos" >
                                <tal:block tal:condition="python: len( TRAVRES[ 'factories']) == 1">
                                    <tr tal:define="unaFactoriaElemento python: TRAVRES[ 'factories'][ 0]; 
                                                    unTituloAccion python: u'%s %s' % (  here.ModelDDvlPlone_tool.fTranslateI18N( here,  'ModelDDvlPlone', 'ModelDDvlPlone_crear_action_label', 'Crear'), unaFactoriaElemento['type_translations'][ 'translated_archetype_name'] );
                                                    unaHREF python: '%s/MDDCreatePloneElement/?type_name=%s' % ( PLONERES[ 'url'], unaFactoriaElemento[ 'archetype_name'])"
                                        class="#" tal:attributes="class python: unasClasesFilas[unIndexClassFila % 2]" >
                                        <td align="center"  >
                                            <a href="#" title="#"
                                                tal:attributes="
                                                    title unTituloAccion; 
                                                    href unaHREF" >
                                                <img src="#" title="#" alt="#"  id="icon-add"
                                                    tal:attributes="title unTituloAccion; src python: '%s/add_icon.gif' % here.portal_url()" />                                                  
                                            </a>
                                        </td>
                                        <td colspan="4" align="left">
                                            <a href="#"  title="#"
                                                tal:attributes="
                                                    title unTituloAccion;
                                                    href unaHREF">
                                                <tal:block  i18n:domain="ModelDDvlPlone" i18n:translate="ModelDDvlPlone_crear_action_label">Crear</tal:block> 
                                                    <img src="#" alt="" title="" 
                                                        tal:attributes="title unTituloAccion; alt unTituloAccion; src python: '%s/%s' % ( here.portal_url(),  unaFactoriaElemento[ 'content_icon'])" />
                                                    <span tal:content=" unaFactoriaElemento/type_translations/translated_archetype_name" />                                                   
                                            </a>
                                        </td>
                                    </tr>
                                </tal:block>
                                <tal:block tal:condition="python: len( TRAVRES[ 'factories']) > 1">
                                    <tr class="#" tal:attributes="class python: unasClasesFilas[unIndexClassFila % 2]" >                            
                                        <td colspan="5" align="left">
                                            <tal:block i18n:domain="ModelDDvlPlone"  i18n:translate="ModelDDvlPlone_crear_action_label">Crear</tal:block> ... &nbsp;
                                            <span tal:repeat="unaFactoriaElemento TRAVRES/factories" >      
                                                <a href="#" title="#"
                                                    tal:define="unTituloAccion python: u'%s %s' % (  here.ModelDDvlPlone_tool.fTranslateI18N( here,  'ModelDDvlPlone', 'ModelDDvlPlone_crear_action_label', 'Crear'), unaFactoriaElemento['type_translations'][ 'translated_archetype_name'] )"
                                                    tal:attributes="
                                                        title unTituloAccion;
                                                        href python: '%s/MDDCreatePloneElement/?type_name=%s' % ( PLONERES[ 'url'], unaFactoriaElemento[ 'archetype_name'])" >
                                                    <img src="#" alt="" title=""
                                                        tal:attributes="title unTituloAccion; alt unTituloAccion; src python: '%s/%s' % ( here.portal_url(),  unaFactoriaElemento[ 'content_icon'])">
                                                    <span tal:content=" unaFactoriaElemento/type_translations/translated_archetype_name" />
                                                </a>
                                                &nbsp; - &nbsp;
                                            </span>
                                        </td>
                                    </tr>
                                </tal:block>
                            </tal:block>
                        </tfoot> 
                        
                        
                        
                     </table>
                     <br/> 
                </tal:block>
             </tal:block>  
        </tal:block>  
    </div>
    
    
    
    
    
    """























cAlreadyRendered_MenuAccionesGrupo_JavaScript_PropertyName = 'AlreadyRendered_MenuAccionesGrupo'



cMDDRenderTabular_MenuAccionesGrupo_JavaScript = """
<script type="text/javascript">
    /* MDDRenderTabular_MenuAccionesGrupo_JavaScript */
    function pMDDToggleAllSelections( theIdTabla) {
        var unElementAllSelections = document.getElementById( theIdTabla+'_SelectAll');
        if ( !unElementAllSelections) {
            return false;
        }
        unNewValueForAllSelections = unElementAllSelections.checked;
        for( var unIdCounter=0; unIdCounter < 10000; unIdCounter++) {
    
            var unElement = document.getElementById( theIdTabla + '_Select_' +unIdCounter );
            if ( !unElement) {
                break;
            }
            unElement.checked = unNewValueForAllSelections;
        }  
    }
    

    
    function pMDDSubmit_varios( theGroupAction, theIdTabla ) {
        var unElementAllSelections = document.getElementById( theIdTabla+'_SelectAll');
        if ( !unElementAllSelections) {
            return false;
        }
        var unSomeSelected = false;
        for( var unIdCounter=0; unIdCounter < 10000; unIdCounter++) {
    
            var unElementCheckBox = document.getElementById( theIdTabla + '_Select_' +unIdCounter );
            if ( !unElementCheckBox) {
                break;
            }
            var unElementUID = document.getElementById( theIdTabla + '_Select_' +unIdCounter + '_UID' );
            if ( !unElementUID) {
                break;
            }
            if ( unElementCheckBox.checked) {
                unSomeSelected = true;
                unElementUID.disabled = false;
            }
            else {
                unElementUID.disabled = true;
            }
        }
        if (!unSomeSelected) {
            return false;
        }
        
        var unElementGroupAction = document.getElementById( theIdTabla +'_GroupAction');
        if ( !unElementGroupAction) {
            return false;
        }
        unElementGroupAction.value = theGroupAction;
        
        
        var unElementForm = document.getElementById( theIdTabla +'_Form');
        if ( !unElementForm) {
            return false;
        }
        
        if ( theGroupAction == 'Delete') {
            var unDeleteAction = unElementForm.action;
            if ( unDeleteAction) {
                unDeleteAction = unDeleteAction.replace( '/Tabular', '/MDDEliminarVarios');
                unElementForm.action = unDeleteAction;
            }
        }
        else { // Just in case the user manages to stay in the page, and use the form again
            var unDeleteAction = unElementForm.action;
            if ( unDeleteAction) {
                unDeleteAction = unDeleteAction.replace( '/MDDEliminarVarios', '/Tabular');
                unElementForm.action = unDeleteAction;
            }
         }
        
        unElementForm.submit();
    }
    
    

    function fMDDGetConstantValue( theConstantElementName) {
        if (!theConstantElementName) {
            return '';
        }
    
        var unElemento	= document.getElementById( theConstantElementName);
        if (!unElemento) {
            return '';
        }
    
        if ( !unElemento.firstChild) {
            return '';
        }
        
        return unElemento.firstChild.data;
    }

</script>
"""            










 

cDomainsStringsAndDefaults = [
    [ 'plone', [    
        [ 'heading_actions',           'Actions-' ,],    
        [ 'Cut',                       'Cut-' ,],    
        [ 'Copy',                      'Copy-' ,],    
        [ 'Paste',                     'Paste-' ,],    
        [ 'Delete',                    'Delete-' ,],    
        [ 'Reorder',                   'Reorder-' ,],    
        
    ]],
    [ 'ModelDDvlPlone', [    
        [ 'ModelDDvlPlone_NumElementsCopied',           'Number of elements Copied-' ,],    
        [ 'ModelDDvlPlone_No_items_copied',             'NO elements Copied-' ,],    
        [ 'ModelDDvlPlone_NumElementsCut',              'Number of elements Cut-' ,],         
        [ 'ModelDDvlPlone_No_items_cut',                'NO elements Cut-' ,],         
        [ 'ModelDDvlPlone_caracteristicas_tabletitle',  'Features-',],
        [ 'ModelDDvlPlone_valores_tabletitle',          'Values-',],
        [ 'ModelDDvlPlone_id_label',                    'Identity-',],
        [ 'ModelDDvlPlone_id_help',                     'Unique indentifier of the element in its container. Is included in the element URL address.-',],
        [ 'ModelDDvlPlone_navegara_action_label',       'Navigate To-',],
        [ 'ModelDDvlPlone_crear_action_label',          'Create-',],
        [ 'ModelDDvlPlone_editar_action_label',         'Edit-',],
        [ 'ModelDDvlPlone_eliminar_action_label',       'Delete',],
        [ 'ModelDDvlPlone_recorrercursorrelacion_action_label', 'Browse elements Related as-',],
        [ 'ModelDDvlPlone_deorigenrelacioncuandoenlazando', 'of',],
        [ 'ModelDDvlPlone_tipo_label',                   'Type-',],
        [ 'ModelDDvlPlone_path_label',                   'Path-',],
        [ 'ModelDDvlPlone_desenlazar_action_label',      'Unlink-',],
        [ 'ModelDDvlPlone_desenlazar_DE',                'from-',],
        [ 'ModelDDvlPlone_cambiar_referencias_action_label',  'Change References-',],
    ]],

]

