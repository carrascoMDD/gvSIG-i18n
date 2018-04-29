/*
# File: TRAProgressControl_javascripts.js
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
# Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana 
# Model Driven Development sl  Valencia (Spain) www.ModelDD.org 
# Antonio Carrasco Valero                       carrasco@ModelDD.org
#
#
*/

// $Id: TRAChangeAndBrowseTranslations_javascripts.js 30984 2009-04-06 18:00:00Z carrasco $



/* #################################################################
Scripts to be executed by user agent (WebBrowser)
################################################################# */




/* #################################################################
Aynchronous communication

*/




function fTRAIsAsyncRequestSupported() {
    
    
    var aIsAsyncRequestSupported = false;
    try {
        aIsAsyncRequestSupported = SupportsAjax();
    }
    catch ( unException) {
    }
    return aIsAsyncRequestSupported;
}


function pTRAMouseUpHandler_LaunchProcess( theRootCatalogPath, theProgressElementUID) {
    if( !theRootCatalogPath || ( theRootCatalogPath.length < 1)) {
        return false;
    }
    if( !theProgressElementUID || ( theProgressElementUID.length < 1)) {
        return false;
    }
    
    var unLaunchStringMsg = fTRA_GetConstantValue( 'cTRAId_ConfirmLaunchStringMsg');
    var unConfirmed = window.confirm( unLaunchStringMsg + '?');
    if (! unConfirmed) {
        return false;
    }

    var unReallyLaunchStringMsg = fTRA_GetConstantValue( 'cTRAId_ReallyLaunchStringMsg');
    unConfirmed = window.confirm( unReallyLaunchStringMsg + '?');
    if (! unConfirmed) {
        return false;
    }

    pTRAAsyncRequest_Service_LaunchProcess_Send( theRootCatalogPath, theProgressElementUID);

    return true;    
}




function pTRAMouseUpHandler_TerminateProcess( theRootCatalogPath, theProgressElementUID) {

    var anActionElement = document.getElementById( 'cid_TRAControlProgress_Action');
    if ( !anActionElement) {
        return false;
    }
    anActionElement.value = ''
    
    if( !theRootCatalogPath || ( theRootCatalogPath.length < 1)) {
        return false;
    }
    if( !theProgressElementUID || ( theProgressElementUID.length < 1)) {
        return false;
    }
    
    var unConfirmStringMsg = fTRA_GetConstantValue( 'cTRAId_ConfirmTerminateStringMsg');
    var unConfirmed = window.confirm( unConfirmStringMsg + '?');
    if (! unConfirmed) {
        return false;
    }

    var unReallyStringMsg = fTRA_GetConstantValue( 'cTRAId_ReallyTerminateStringMsg');
    unConfirmed = window.confirm( unReallyStringMsg + '?');
    if (! unConfirmed) {
        return false;
    }

    anActionElement.value = 'Terminate';
    
    document.forms[ 'TRAControlProgress_ActionsForm'].submit();

    return true;    
}




function pTRAMouseUpHandler_ControlProcess( theAction, theConfirmStringMsg, theReallyStringMsg) {

    var anActionElement = document.getElementById( 'cid_TRAControlProgress_Action');
    if ( !anActionElement) {
        return false;
    }
    anActionElement.value = ''
    
    if( !theAction || ( theAction.length < 1)) {
        return false;
    }
    if( !theConfirmStringMsg || ( theConfirmStringMsg.length < 1)) {
        return false;
    }
    if( !theReallyStringMsg || ( theReallyStringMsg.length < 1)) {
        return false;
    }
    
    var unConfirmed = window.confirm( theConfirmStringMsg + ' ?');
    if (! unConfirmed) {
        return false;
    }

    unConfirmed = window.confirm( theReallyStringMsg + ' ?');
    if (! unConfirmed) {
        return false;
    }

    anActionElement.value = theAction;
    
    document.forms[ 'TRAControlProgress_ActionsForm'].submit();

    return true;    
}




function pTRAAsyncRequest_Service_LaunchProcess_Send( theRootCatalogPath, theProgressElementUID) {

    if ( !fTRAIsAsyncRequestSupported()) {
        return false;
    }
    
    var unInteractionMessage = fTRA_GetContenidoTextoElementoWithId( 'cid_TRAInteractionMessage');
    if ( unInteractionMessage && ( unInteractionMessage.length > 0))  {
        return false;
    }
    
    /* need to use encodeURIComponent instead of encodeURI, to escape + */
    var someRequestParameters =                         '?theProcessControlAction=Execute';
    someRequestParameters = someRequestParameters + '&theRootCatalogPath='  + encodeURIComponent( theRootCatalogPath);
    someRequestParameters = someRequestParameters + '&theProgressElementUID=' + encodeURIComponent( theProgressElementUID);
    

    var aRequestString = fTRAAsyncRequestURL() + someRequestParameters;

    var unRequestDisplayField = document.getElementById( 'theTRAAsyncRequest_Display_Field');
    if (unRequestDisplayField) {
        unRequestDisplayField.value = aRequestString;
    }

    fTRA_SetContenidoTextoElementoWithId( 'cid_TRAInteractionMessage', fTRAMsg( 'AsyncPhase_RequestQueued'));        
    pTRAShowElementWithId(  'cid_TRAInteractionMessageHolder');

    pTRAAsyncRequest_Response_Display( 'no response yet');
    
    /* g_ajax_obj.CallXMLHTTPObjectGET( aRequestString, pTRAAsyncRequest_Response_Handler) */
    g_ajax_obj.CallXMLHTTPObjectGETParamPartialPhase( aRequestString, pTRAAsyncRequest_Response_Handler, theProgressElementUID, pTRAAsyncRequest_Sent_Handler, theProgressElementUID, 1 );
    return true;

}




function pTRAAsyncRequest_Response_Handler( theResponseText, theParamether) {
    if (!theResponseText) {
        return false;
    }

    pTRAAsyncRequest_Response_Display( theResponseText);
    
    fTRA_SetContenidoTextoElementoWithId( 'cid_TRAInteractionMessage', fTRAMsg( 'AsyncPhase_ResponseReceived'));        
    pTRAShowElementWithId(  'cid_TRAInteractionMessageHolder');

    return true;
}



function pTRAAsyncRequest_Sent_Handler( theResponseText, theParamether) {
    fTRA_SetContenidoTextoElementoWithId( 'cid_TRAInteractionMessage', fTRAMsg( 'AsyncPhase_RequestSent'));        
    pTRAShowElementWithId(  'cid_TRAInteractionMessageHolder' );

    if (!theResponseText) {
        return false;
    }

    pTRAAsyncRequest_StatusDisplay_Sent( theResponseText, theParamether);
              
    return true;
}


















function pTRAAsyncRequest_Response_Display( theResponseText, theParameter) {


    var unResponseDisplayField = document.getElementById( 'theTRAAsyncRequest_Response_Display_Field');
    if ( unResponseDisplayField) {
        unResponseDisplayField.value = theResponseText;
    }
    if ( !theResponseText) {
        return false;
    }
    


    var unResponseStoreField = document.getElementById( 'cid_TRAAsyncResponseStore');
    if ( !unResponseStoreField) {
        return false;
    }
    
    
    unResponseStoreField.innerHTML= '';
    unResponseStoreField.innerHTML=theResponseText;

    var unSuccess						= fTRAAsynchResponse_Content( 'success');
         

    
    if ( !( unSuccess == 'true')) {
        return false;
    }

    /* pTRAHideElementWithId(  'cid_TRAInteractionMessageHolder_' + unIndexTraduccion); */
 
    return true;
}








function pTRAAsyncRequest_StatusDisplay_Sent( theResponseText, theParameter) {

    var unResponseDisplayField = document.getElementById( 'theTRAAsyncRequest_Response_Display_Field');
    if ( unResponseDisplayField) {
        unResponseDisplayField.value = 'Sent ' + theParameter;
    }


            
    return true;
}













cTRAFGColor_Process_NotLaunched   = 'Black';
cTRAFGColor_Process_Launched      = 'White';
cTRAFGColor_Process_Terminated    = 'White';
cTRAFGColor_Process_Terminated    = 'Black';


cTRABGColor_Process_NotLaunched   = 'Yellow';
cTRABGColor_Process_Launched      = 'Blue';
cTRABGColor_Process_Terminated    = 'Green';
cTRABGColor_Process_Failed        = 'Red';








/* #################################################################
Async Request page name
################################################################# */

cAsyncRequestPage = 'TRAProcessControl_Async';





/* #################################################################
Enter the debugger by causing an error
################################################################# */

function pTRAEnterDebugger() {

    open_debugger_with_inexisting_function_invocation();
}












/* #################################################################
Page URL
################################################################# */


function fTRABaseRequestURL() {
    var unaWindowLocation = window.location;
    if ( !unaWindowLocation) {
        return '';
    }
    var unProtocol  = unaWindowLocation.protocol;
    var unHost      = unaWindowLocation.host;
    var unPath      = unaWindowLocation.pathname;

    var unosPathElements = unPath.split( '/');
    var unosPathElementsWithoutPage = "";
    
    if ( unosPathElements[ unosPathElements.length -1].length < 1) {
        unosPathElementsWithoutPage = unosPathElements.slice( 0, unosPathElements.length - 2);
    }
    else {
        unosPathElementsWithoutPage = unosPathElements.slice( 0, unosPathElements.length - 1) ;   
    }
    
    var unPathWithoutPage =  unosPathElementsWithoutPage.join( '/');

    var unaURL = unProtocol + '//' + unHost +  unPathWithoutPage ;

    return unaURL;
}



function fTRAAsyncRequestURL() {
    var unAsyncRequest = fTRA_GetConstantValue( 'cTRAId_AsynchRequestURL');
    if ( unAsyncRequest.length) {
        return unAsyncRequest;
    }

    var unaBaseURL = fTRABaseRequestURL();
    if ( !unaBaseURL) {
        return '';
    }

    var unaURL = unaBaseURL + '/' + cAsyncRequestPage;

    return unaURL;
}



function fTRAPortalURL() {
    var unPortalURL = fTRA_GetConstantValue( 'cTRAId_PortalURL');
    return unPortalURL;
}


function fTRAIconsBaseURL() {
    var unIconsBaseURL = fTRAPortalURL( );
    if ( unIconsBaseURL.length) {
        return unIconsBaseURL;
    }

    var unaBaseURL = fTRABaseRequestURL() + '////';
    return unaBaseURL;
}








function fTRAMsg( theMessage) {
    if ( !theMessage) {
        return '';
    }
    
    var unElementoTextoMensaje = document.getElementById( 'TRAMessage_' + theMessage);
    if ( (!unElementoTextoMensaje) || ( !unElementoTextoMensaje.firstChild)) {
        return theMessage;
    }

    var unMensaje = unElementoTextoMensaje.firstChild.data;
    return unMensaje;
}







/* #################################################################
Asynch request result property array access functions
################################################################# */





function fTRApropertyValue( theArrayOfProperties, thePropertyName) {
    if ( (!theArrayOfProperties) || !( thePropertyName.length)) {
        return new Array( '', '');
    }

    var unPropertyArray = fTRAproperty( theArrayOfProperties, thePropertyName);
    if ( (!unPropertyArray) || ( unPropertyArray.length < 2)) {
        return new Array( '', '');
    }
    return unPropertyArray[ 1];
}



function fTRAproperty( theArrayOfProperties, thePropertyName) {

    if ( (!theArrayOfProperties) || !( thePropertyName.length)) {
        return new Array( '', '');
    }

    var unNumProperties = theArrayOfProperties.length;

    for( unIndexProperty=0; unIndexProperty < unNumProperties; unIndexProperty++) {

        var unArrayProperty = theArrayOfProperties[ unIndexProperty];
    
        if ( unArrayProperty) {
            var unNombreProperty = unArrayProperty[ 0];
            if ( unNombreProperty == thePropertyName) {
                return unArrayProperty;
            }
        }
    }
    return new Array(  '', '');
}







function fTRA_GetConstantValue( theConstantElementName) {
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





function fTRA_GetContenidoTextoElemento( theElemento) {

    if ( !theElemento) {
        return '';
    }

    if ( !theElemento.firstChild) {
        return '';
    }

    
    var aTextString = theElemento.firstChild.data;
    return aTextString;
}




function fTRA_GetContenidoTextoElementoWithId( theElementId) {

    if ( !theElementId) {
        return '';
    }

    var unElement	= document.getElementById( theElementId);
    if ( !unElement) {
        return '';
    }
    return fTRA_GetContenidoTextoElemento( unElement);
}





function fTRA_SetContenidoTextoElemento( theElemento, theTextString) {

    if ( !theElemento) {
        return false;
    }

    if ( !theElemento.firstChild) {
        var unTextNode = document.createTextNode( theTextString);
        if ( unTextNode) {
            theElemento.appendChild( unTextNode);
            return true;
        }
        return false;
    }

    if ( !(  theElemento.firstChild.data == theTextString)) {
        theElemento.firstChild.data = theElemento.firstChild.data + ' ' + theTextString;
    }
    return true;
}



function fTRA_SetContenidoTextoElementoWithId( theElementId, theTextString) {

    if ( !theElementId) {
        return false;
    }

    var unElement	= document.getElementById( theElementId);
    if ( !unElement) {
        return false;
    }
    return fTRA_SetContenidoTextoElemento( unElement, theTextString);
}












function fTRAAsynchResponse_Content( thePropertyName) {

    var unElementoStoreSpan	= document.getElementById( 'cid_AsyncResponse_' + thePropertyName);

    if ( (!unElementoStoreSpan)  || (!unElementoStoreSpan.firstChild)) {
        return null;
    }

    var unValor= unElementoStoreSpan.firstChild.data;

    return unValor;
}







































function fTRAStringStrip( theString) {
    if ( !theString.length) {
        return '';
    }
    
    var unString = theString;
    while( unString.length && ( unString.charAt( 0) == ' ')) {
        unString = unString.slice( 1);
    }
    if ( !unString.length) {
        return '';
    }
    while( unString.length && ( unString.charAt( unString.length - 1) == ' ')) {
        unString = unString.slice( 0, unString.length - 1);
    }
    return unString;
}





/* #################################################################
    Submit function with Asynch request response without page reload

*/
function fTRASubmitLaunchProcess_Async( ) {  


    fTRA_SetContenidoTextoElementoWithId( 'cid_TRAProgressControl_StatusMessage', fTRAMsg( 'AsyncPhase_LaunchProcessRequested'));        
    
    pTRAAsyncRequest_Service_LaunchProcess_Send( );

    return true;
    
}












/* #################################################################
Form utility functions to change elements classes, i.e. to show/hide
################################################################# */




function fTRAIsVisibleElementWithId( theElementId) {
    if ( !theElementId) {
        return false;
    } 

    var unElement = document.getElementById( theElementId);
    if ( !unElement) {
        return false;
    } 
    return fTRAIsVisibleElement( unElement);
}





function pTRAHideElementWithId( theElementId) {
    if ( !theElementId) {
        return false;
    } 

    var unElement = document.getElementById( theElementId);
    if ( !unElement) {
        return false;
    } 

    return pTRAHideElement( unElement);
}




function pTRAShowElementWithId( theElementId) {
    if ( !theElementId) {
        return false;
    } 

    var unElement = document.getElementById( theElementId);
    if ( !unElement) {
        return false;
    } 

    return pTRAShowElement( unElement);
}





function fTRAIsVisibleElement( theElement) {
    if ( !theElement) {
        return false;
    }

    return hasClassName( theElement, 'TRAstyle_Display');
}





function pTRAHideElement( theElement) {
    if ( !theElement) {
        return false;
    }

    if ( hasClassName( theElement, 'TRAstyle_Display')) {
        replaceClassName( theElement, 'TRAstyle_Display', 'TRAstyle_NoDisplay');
        return true;
    }       

    return false;
}



function fTRAIsEnabledElementWithId( theElementId) {
    if ( !theElementId) {
        return false;
    } 

    var unElement = document.getElementById( theElementId);
    if ( !unElement) {
        return false;
    } 

    return fTRAIsEnabledElement( unElement);
}


function pTRADisableElementWithId( theElementId) {
    if ( !theElementId) {
        return false;
    } 

    var unElement = document.getElementById( theElementId);
    if ( !unElement) {
        return false;
    } 

    return pTRADisableElement( unElement);
}




function pTRAEnableElementWithId( theElementId) {
    if ( !theElementId) {
        return false;
    } 

    var unElement = document.getElementById( theElementId);
    if ( !unElement) {
        return false;
    } 

    return pTRAEnableElement( unElement);
}



function fTRAIsEnabledElement( theElement) {
    if ( !theElement) {
        return false;
    }
    return !theElement.hasAttribute ( "disabled");

}




function pTRADisableElement( theElement) {
    if ( !theElement) {
        return false;
    }
    theElement.disabled = true;

    return true;
}



function pTRADisableElement_Firefox( theElement) {
    if ( !theElement) {
        return false;
    }
    if ( !theElement.hasAttribute ( "disabled")) {
        theElement.setAttribute( "disabled",  1);
    }

    return true;
}


function pTRAEnableElement( theElement) {
    if ( !theElement) {
        return false;
    }

    theElement.disabled= false;
    
    return true;
}


function pTRAEnableElement_Firefox( theElement) {
    if ( !theElement) {
        return false;
    }

    var unDone = false;
    try { /* works in Firefox, crashes in IExplorer */
        if ( theElement.hasAttribute ( "disabled")) {
            theElement.removeAttribute( "disabled");
        }
        unDone = true;
    }
    catch( unaAException) {
    }
    /* IExplorer */
    if ( !unDone) {
        theElement.attributes.removeNamedItem( "disabled");
    }

    return true;
}



function pTRAShowElement( theElement) {
    if ( !theElement) {
        return false;
    }

    if ( hasClassName( theElement, 'TRAstyle_NoDisplay')) {
        replaceClassName( theElement, 'TRAstyle_NoDisplay', 'TRAstyle_Display');
        return true;
    }       

    return true;
}
