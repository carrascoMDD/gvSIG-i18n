/*
# File: TRAChangeAndBrowseTranslations_javascripts.js
#
# Copyright (c) 2008, 2009, 2010, 2011  by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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





cTRABGColor_Translation_IgnoredSave        = '#D0D0D0';
cTRABGColor_Translation_ChangedTranslation = '#00E0F0';
cTRABGColor_Translation_ChangedStatus      = '#00F0E0';
cTRABGColor_Translation_NotChangedInServer = '#F0E000';

cTRABGColor_Translation_BatchStatusChangeRecorded = cTRABGColor_Translation_ChangedStatus;


cTRAMaxRowsToLoopForRowElements      = 30000;
cTRAMaxRowsToLoopForOtherElements    = 500



/* #################################################################
Scripts to be executed upon loading of the page:
Open editor on the first translation row.
################################################################# */

/* Changing to adding a listener, through the plone registerPloneFunction
window.onload = function(){

    pTRAResetCachedGlobals();

    pTRAAbrirEditorEnFilaNumero( 1);
}
*/



function pTRAWindowOnLoad() {

    pTRAResetCachedGlobals();

    pTRAAbrirEditorEnFilaNumero( 1);
}


registerPloneFunction( pTRAWindowOnLoad);



function pTRAResetCachedGlobals() {
    
    gUserInterfaceInTransition          = false;


    gTRAIsAsyncRequestSupported_Cached  = 999;
    
    gAsynchronousTranslationMode_Cached = 999;

    gKeyAction_CR_Cached                = '999';
    gKeyAction_Tab_Cached               = '999';
    gKeyAction_Escape_Cached            = '999';
    
    gTRAMustRenderUserInterfaceEvents   = 999;
    
    gTRANoConfirmTranslationChanges     = 999;
    gTRANoConfirmStatusChanges          = 999;
    gTRANoConfirmTranslationDelete      = 999;
}




/* #################################################################
Async Request page name
################################################################# */

cAsyncRequestPage = 'TRATraducir_Async';





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

    var unaURL = unaBaseURL + '//////' + cAsyncRequestPage;

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






/* #################################################################
Maps from status to colors and icons
################################################################# */


function fEstado_BGcolor( theEstado ) {    

    if ( ! theEstado) {
        return "White";
    }
    if ( theEstado == "Pendiente") {
        return "Red";
    }
    if ( theEstado == "Traducida") {
        return "Yellow";
    }
    if ( theEstado == "Revisada") {
        return "Green";
    }
    if ( theEstado == "Definitiva") {
        return "Blue";
    }
    return "White";
}



function fEstado_FGcolor( theEstado ) {    

    if ( ! theEstado) {
        return "Black";
    }
    if ( theEstado == "Pendiente") {
        return "Black";
    }
    if ( theEstado == "Traducida") {
        return "Black";
    }
    if ( theEstado == "Revisada") {
        return "White";
    }
    if ( theEstado == "Definitiva") {
        return "White";
    }
    return "Black";
}


function fEstado_icon( theEstado ) {    

    if ( ! theEstado) {
        return "tra_pendiente.gif";
    }
    if ( theEstado == "Pendiente") {
        return "tra_pendiente.gif";
    }
    if ( theEstado == "Traducida") {
        return "tra_traducida.gif";
    }
    if ( theEstado == "Revisada") {
        return "tra_revisada.gif";
    }
    if ( theEstado == "Definitiva") {
        return "tra_definitiva.gif";
    }
    return "tra_pendiente.gif";
}









/* #################################################################
Submit functions with full HTTP / HTML roundtrip and page reload
################################################################# */


/* changes the main language and symbol to edit and submits the form */
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





/* changes the main language and symbol to edit and submits the form */
function pTRANavegarAIdiomaPrincipalYSimboloCadenaEnFilaNumero( pCodigoIdiomaCursor, theTranslationRowIndex, theEstadoTraduccion) {

    if ( ! ( window.confirm( fTRAMsg( 'Confirmar_NavegarAIdiomaPrincipalYSimbolo') + ' ' + pCodigoIdiomaCursor))) {
        return false;
    }
    if ( ! ( document.getElementById( 'theCodigoIdiomaCursor').value == pCodigoIdiomaCursor)) {

        document.getElementById( 'theCodigoIdiomaCursor').value = pCodigoIdiomaCursor;
    
        if ( !( document.getElementById( 'theEstadosAIncluir_' + theEstadoTraduccion).checked)) {
            document.getElementById( 'theEstadosAIncluir_'+theEstadoTraduccion).checked = 1;
        }
    }

    pTRANavegarASimboloCadenaEnFilaNumero( theTranslationRowIndex);

    return true;
}




/* changes the symbol to edit and submits the form */
function pTRANavegarASimboloCadenaEnFilaNumero( theTranslationRowIndex ) {

    /* get data in the translation to edit */
    var unosDatosEnFila = fTRA_GetDatosEnFilaNumero( theTranslationRowIndex);
    if ( !unosDatosEnFila) {
        return false;
    }

    var unFieldSimboloCadena	= fTRA_FieldDatosEnFila( unosDatosEnFila, 'simboloCadena');
    if ( !unFieldSimboloCadena) {
        return false;
    }

    var unSimboloCadena = unFieldSimboloCadena[ 1];
    if ( !unSimboloCadena) {
        return false;
    }


    document.getElementById( 'theSimboloCadenaCursor').value = unSimboloCadena;

    document.forms[ 'TranslationFormId'].submit();
    return true;
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




/* #################################################################
Translation record access functions
################################################################# */



function fTRA_NewVoidDatosEnFila( ) {
    var unResult = new Array(
        /*			name,				value, originalValue, type */
        new Array( 'index',					'',		'',		'numberstring'),	
        new Array( 'simboloCadena',			'',		'',		'string'),	
        new Array( 'idCadena',			    '',		'',		'string'),	
        new Array( 'cadenaTraducida',		'',		'',		'string'),	
        new Array( 'cadenaTraducida_NewValue','',	'',		'string'),	
        new Array( 'estadoTraduccion',		'',		'',		'string'),	
        new Array( 'targetStatusChanges',	'',	    '',		'string'),	
        new Array( 'nombresModulos',		'',		'',		'string'),	
        new Array( 'referenciasFuentes',	'',		'',		'string'),	
        new Array( 'contadorCambios',		'',		'',		'numberstring'),	
        new Array( 'usuarioCreador',		'',		'',		'string'),	
        new Array( 'fechaCreacion',		    '',		'',		'string'),	
        new Array( 'usuarioTraductor',		'',		'',		'string'),	
        new Array( 'fechaTraduccion',		'',		'',		'string'),	
        new Array( 'usuarioRevisor',		'',		'',		'string'),	
        new Array( 'fechaRevision',		    '',		'',		'string'),	
        new Array( 'usuarioCoordinador',	'',		'',		'string'),	
        new Array( 'fechaDefinitivo',		'',		'',		'string')	
    );
    return unResult;
}







function fTRA_FieldDatosEnFila( theDatosEnFila, theFieldName) {
    if (!theDatosEnFila) {
        return new Array( '', '', '', '');
    }

    var unNumProperties = theDatosEnFila.length;

    for( unIndexProperty=0; unIndexProperty < unNumProperties; unIndexProperty++) {

        var unDatoEnFila = theDatosEnFila[ unIndexProperty];
    
        if ( unDatoEnFila) {
            var unNombreProperty = unDatoEnFila[ 0];
            if ( unNombreProperty == theFieldName) {
                return unDatoEnFila;
            }
        }
    }
    return new Array(  '', '', '', '');
}




function fTRA_GetIndexFilaConSimboloCadena( theSimboloCadena) {

    if ( (!theSimboloCadena) || ( theSimboloCadena.length < 1)) {
        return -1;
    }

    for ( unIndexFila = 1; unIndexFila < cTRAMaxRowsToLoopForRowElements; unIndexFila++) {

        var unaIdElementoSimboloCadena = 'cid_ColumnaCadenasTraducidas_' + unIndexFila + '_simboloCadena';
    
        var unElementoSimboloCadena	= document.getElementById( unaIdElementoSimboloCadena);
    
        if ( unElementoSimboloCadena && unElementoSimboloCadena.firstChild) {
    
            var unSimboloCadena = unElementoSimboloCadena.firstChild.data;
            if ( unSimboloCadena == theSimboloCadena) {
                 return unIndexFila;
            }
        }
    }
    return -1;
}


// ACV 20110220 stop loop if element not found by id
function fTRA_GetIndexFilaConSimboloCadena( theSimboloCadena) {

    if ( (!theSimboloCadena) || ( theSimboloCadena.length < 1)) {
        return -1;
    }

    for ( unIndexFila = 1; unIndexFila < cTRAMaxRowsToLoopForRowElements; unIndexFila++) {

        var unaIdElementoSimboloCadena = 'cid_ColumnaCadenasTraducidas_' + unIndexFila + '_simboloCadena';
    
        var unElementoSimboloCadena	= document.getElementById( unaIdElementoSimboloCadena);
        
        if ( ! unElementoSimboloCadena) {
            break;
        }
        
        var unFirstChild = unElementoSimboloCadena.firstChild;
        if ( unFirstChild) {
    
            var unSimboloCadena = unFirstChild.data;
            if ( unSimboloCadena == theSimboloCadena) {
                 return unIndexFila;
            }
        }
    }
    return -1;
}



function fTRA_GetSimboloCadenaEIndexEnFilaNumero( theTranslationRowIndex) {

    var unSimboloCadena = '';
    var unElementoSimboloCadenaProperty	= document.getElementById( 'cid_ColumnaCadenasTraducidas_' + theTranslationRowIndex + '_simboloCadena');
    if ( unElementoSimboloCadenaProperty && unElementoSimboloCadenaProperty.firstChild) {
        unSimboloCadena =  unElementoSimboloCadenaProperty.firstChild.data;
    }

    var unIndex = '';
    var unElementoIndexProperty	= document.getElementById( 'cid_ColumnaCadenasTraducidas_' + theTranslationRowIndex + '_index');
    if ( unElementoIndexProperty && unElementoIndexProperty.firstChild) {
        unIndex =  unElementoIndexProperty.firstChild.data;
    }

    return [ unSimboloCadena, unIndex];  
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





function fTRA_GetDatosEnFilaNumero( theTranslationRowIndex) {

    var unosDatosEnFila = fTRA_NewVoidDatosEnFila();

    var unNumProperties = unosDatosEnFila.length;
    
    for( unIndexProperty=0; unIndexProperty < unNumProperties; unIndexProperty++) {

        var unDatoEnFila = unosDatosEnFila[ unIndexProperty];
        if ( unDatoEnFila) {
        
            var unNombreProperty		= unDatoEnFila[ 0];
            var unTipoProperty			= ( unDatoEnFila[ 0].length > 3) ?  unDatoEnFila[ 3]: 'string';
            var unaIdElementoProperty	= 'cid_ColumnaCadenasTraducidas_' + theTranslationRowIndex + '_' + unNombreProperty;
            var unElementoProperty	= document.getElementById( unaIdElementoProperty);
        
            if ( unElementoProperty && unElementoProperty.firstChild) {
        
                var aData = unElementoProperty.firstChild.data;
                if ( unTipoProperty == 'boolchar') {
                    aData = ( aData == '1') ? 1 : 0;
                }
                unDatoEnFila[ 1] = aData; /* value */
                unDatoEnFila[ 2] = aData; /* originalValue */
            }		
        }
    }
    return unosDatosEnFila;
}



function fTRA_SetPropiedadEnFilaNumero( theTranslationRowIndex, theNombrePropiedad, theValorPropiedad) {

    var unaIdElementoProperty	= 'cid_ColumnaCadenasTraducidas_' + theTranslationRowIndex + '_' + theNombrePropiedad;
    var unElementoProperty		= document.getElementById( unaIdElementoProperty);

    if ( !unElementoProperty) {
        return false;
    }

    if ( !unElementoProperty.firstChild) {
        var unTextNode = document.createTextNode( theValorPropiedad);
        if ( unTextNode) {
            unElementoProperty.appendChild( unTextNode);
            return true;
        }
        return false;
    }

    if ( !(  unElementoProperty.firstChild.data == theValorPropiedad)) {
        unElementoProperty.firstChild.data = theValorPropiedad;
    }
    return true;
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
        theElemento.firstChild.data = theTextString;
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
    var unChanged						= fTRAAsynchResponse_Content( 'changed');
    var unChangeStatus		     		= fTRAAsynchResponse_Content( 'theChangeStatus');
    var unChangeMessage		     		= fTRAAsynchResponse_Content( 'theChangeMessage');
    var unCodigoIdioma					= fTRAAsynchResponse_Content( 'theCodigoIdiomaATraducir'); 
    var unSimboloCadena					= fTRAAsynchResponse_Content( 'theSimboloCadenaATraducir');    
    var unaCadenaTraducida				= fTRAAsynchResponse_Content( 'theCadenaTraducida');    
    var unEstadoTraduccion				= fTRAAsynchResponse_Content( 'theEstadoTraduccion');   
    var unosTargetStatusChangesString	= fTRAAsynchResponse_Content( 'theTargetStateChanges');   
    var unContadorCambios             	= fTRAAsynchResponse_Content( 'theChangesCounter');   
       
    var unosNombresModulos             	= fTRAAsynchResponse_Content( 'theModuleNames');   
    var unasReferenciasFuentes        	= fTRAAsynchResponse_Content( 'theSourceReferences');   
       
    var unaFechaTraduccion             	= fTRAAsynchResponse_Content( 'theFechaTraduccion');   
    var unUsuarioTraductor             	= fTRAAsynchResponse_Content( 'theUsuarioTraductor');   
    var unaFechaRevision             	= fTRAAsynchResponse_Content( 'theFechaRevision');   
    var unUsuarioRevisor             	= fTRAAsynchResponse_Content( 'theUsuarioRevisor');   
    var unaFechaDefinitivo             	= fTRAAsynchResponse_Content( 'theFechaDefinitivo');   
    var unUsuarioCoordinador            = fTRAAsynchResponse_Content( 'theUsuarioCoordinador');   


    var unIndexTraduccion = fTRA_GetIndexFilaConSimboloCadena( unSimboloCadena);
    if ( unIndexTraduccion < 0) {
        return false;
    }

    fTRA_SetContenidoTextoElementoWithId( 'cid_TRAInteractionMessage_' + unIndexTraduccion, fTRAMsg( 'AsyncPhase_ResponseReceived'));        
    
    if ( !( unSuccess == 'true')) {
        fTRA_SetBGColorEnCadenaTraducidaFilaNumero(   unIndexTraduccion, cTRABGColor_Translation_NotChangedInServer);
        if ( unChangeStatus == 'DifferentChangeCounter') { 
            fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'interactionStatus',    unChangeStatus);
            fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'interactionMessage',   unChangeMessage);
            fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'cadenaTraducida',      unaCadenaTraducida);
            fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'cadenaTraducidaDisplay', unaCadenaTraducida);
            fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'estadoTraduccion',     unEstadoTraduccion);
            fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'contadorCambios',      unContadorCambios);
            fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'targetStatusChanges',  unosTargetStatusChangesString);
            
            fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'nombresModulos',       unosNombresModulos);
            fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'referenciasFuentes',   unasReferenciasFuentes);
            
            fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'fechaTraduccion',      unaFechaTraduccion);
            fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'usuarioTraductor',     unUsuarioTraductor);
            fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'fechaRevision',        unaFechaRevision);
            fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'usuarioRevisor',       unUsuarioRevisor);
            fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'fechaDefinitivo',      unaFechaDefinitivo);
            fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'usuarioCoordinador',   unUsuarioCoordinador);
            
            fTRA_SetContenidoTextoElementoWithId( 'cid_TRAInteractionMessage_' + unIndexTraduccion, unChangeMessage);        
            pTRAShowElementWithId(  'cid_TRAInteractionMessageHolder_' + unIndexTraduccion);
            
        }
        return false;
    }

    /* pTRAHideElementWithId(  'cid_TRAInteractionMessageHolder_' + unIndexTraduccion); */
    
    fTRA_SetBGColorEnCadenaTraducidaFilaNumero(   unIndexTraduccion,'');
    fTRA_SetBGColorEnBotonesEstadoFilaNumero(     unIndexTraduccion,'');


    fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'interactionStatus',    unChangeStatus);
    fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'interactionStatus',    unChangeStatus);
    fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'cadenaTraducida',      unaCadenaTraducida);
    fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'cadenaTraducidaDisplay',unaCadenaTraducida);
    fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'estadoTraduccion',     unEstadoTraduccion);
    fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'contadorCambios',      unContadorCambios);
    fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'targetStatusChanges',  unosTargetStatusChangesString);
    
    fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'nombresModulos',       unosNombresModulos);
    fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'referenciasFuentes',   unasReferenciasFuentes);
    
    fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'fechaTraduccion',      unaFechaTraduccion);
    fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'usuarioTraductor',     unUsuarioTraductor);
    fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'fechaRevision',        unaFechaRevision);
    fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'usuarioRevisor',       unUsuarioRevisor);
    fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'fechaDefinitivo',      unaFechaDefinitivo);
    fTRA_SetPropiedadEnFilaNumero( unIndexTraduccion, 'usuarioCoordinador',   unUsuarioCoordinador);


    var unElementoEstadoBGColor= document.getElementById( 'cid_ColumnaCadenasTraducidas_' + unIndexTraduccion + '_estado_BGcolor');        
    if ( unElementoEstadoBGColor) {
        var unBGcolor = fEstado_BGcolor( unEstadoTraduccion);
        unElementoEstadoBGColor.setAttribute( 'bgcolor' , unBGcolor);
    }
    var unElementoEstadoFGColor= document.getElementById( 'cid_ColumnaCadenasTraducidas_' + unIndexTraduccion + '_estado_FGcolor');        
    if ( unElementoEstadoFGColor) {
        var unFGcolor = fEstado_FGcolor( unEstadoTraduccion);
        unElementoEstadoFGColor.setAttribute( 'color' , unFGcolor);
    }
    var unElementoEstadoIcon= document.getElementById( 'cid_ColumnaCadenasTraducidas_' + unIndexTraduccion + '_estado_icon');        
    if ( unElementoEstadoIcon) {
        var unIcon = fEstado_icon( unEstadoTraduccion);
        unElementoEstadoIcon.setAttribute( 'src' , fTRAIconsBaseURL() + '/' + unIcon);
    }

    pTRAShowOrHideColumnStateTransitionButtonsEnFilaNumero( unIndexTraduccion);
    
    var unElementoCadenaTraducidaIndex = document.getElementById( 'theCadenaTraducida_index');
    if ( unElementoCadenaTraducidaIndex) {

        var unCadenaTraducidaIndex = unElementoCadenaTraducidaIndex.value;
        if ( ( unCadenaTraducidaIndex.length) &&  (  !( unCadenaTraducidaIndex == '-1'))) {
    
            if ( unCadenaTraducidaIndex == unIndexTraduccion) {
        
                pTRAShowOrHideEditorTextAreaEnFilaNumero( unIndexTraduccion);
                
                pTRAShowOrHideEditorButtonsEnFilaNumero(  unIndexTraduccion);
                
                pTRAMostrarDetallesTraduccionEnFilaNumero( unIndexTraduccion);
                
                pTRASetModulesEditorValues();
            }  
        }
    }

    
    var unExecutionProfileResult = document.getElementById( 'cid_AsyncResponse_theExecutionProfileResult');
    if ( unExecutionProfileResult) {
        var unExecutionProfileHolder = document.getElementById( 'theTRAAsyncRequest_ExecutionProfile_Holder');
        if ( unExecutionProfileHolder) {
        
            var unFirstChild = unExecutionProfileHolder.firstChild;
            while ( unFirstChild) {
                unExecutionProfileHolder.removeChild( unFirstChild);
                unFirstChild = unExecutionProfileHolder.firstChild;
            }
            
            unExecutionProfileHolder.appendChild( unExecutionProfileResult);
        }
    }
        

    return true;
}








function pTRAAsyncRequest_StatusDisplay_Sent( theResponseText, theParameter) {

    var unResponseDisplayField = document.getElementById( 'theTRAAsyncRequest_Response_Display_Field');
    if ( unResponseDisplayField) {
        unResponseDisplayField.value = 'Sent ' + theParameter;
    }

    var unIndexTraduccion = '' + theParameter;
    unIndexTraduccion = parseInt( unIndexTraduccion);
    if ( !unIndexTraduccion) {
        return false;
    }  
              
    fTRA_SetContenidoTextoElementoWithId( 'cid_TRAInteractionMessage_' + unIndexTraduccion, fTRAMsg( 'AsyncPhase_RequestSent'));        
    pTRAShowElementWithId(  'cid_TRAInteractionMessageHolder_' + unIndexTraduccion);
            
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









function fTRAHideElementWithId( theElementId) {
    if ( !theElementId) {
        return false;
    } 

    var unElement = document.getElementById( theElementId);
    if ( !unElement) {
        return false;
    } 

    pTRAHideElement( unElement);
    
    return true;
}




function fTRAShowElementWithId( theElementId) {
    if ( !theElementId) {
        return false;
    } 

    var unElement = document.getElementById( theElementId);
    if ( !unElement) {
        return false;
    } 

    pTRAShowElement( unElement);
    
    return true;
    
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



function pTRAHideSymbolColumn( ) {
    
    fTRAHideElementWithId( 'TRABatchStatusChange_fillerForSymbolColumn1');
    fTRAHideElementWithId( 'TRABatchStatusChange_fillerForSymbolColumn2');
    fTRAHideElementWithId( 'cid_ColumnaSimbolos_header');
    fTRAShowElementWithId( 'cid_ColumnaSimbolos_show_help');

    for( var unIdCounter=1; unIdCounter <= cTRAMaxRowsToLoopForRowElements; unIdCounter++) {
     
        if ( ! fTRAHideElementWithId( 'cid_FilaParaSimboloSobreTraducciones_' + unIdCounter + '_fillerForSymbol'))                    { break; };
        if ( ! fTRAHideElementWithId( 'cid_ColumnaSimbolos_' + unIdCounter))                                                          { break; };

        if ( ! fTRAShowElementWithId( 'cid_FilaParaSimboloSobreTraducciones_' + unIdCounter ))                                        { break; };
        if ( ! fTRAShowElementWithId( 'cid_FilaParaSimboloSobreTraducciones_' + unIdCounter + '_fillerForLanguageAndStatusColumns'))  { break; };
        if ( ! fTRAShowElementWithId( 'cid_FilaParaSimboloSobreTraducciones_' + unIdCounter + '_simboloCadena_SobreTraducciones'))    { break; };      
     }  
    return true;
}



function pTRAShowSymbolColumn( ) {
    
    fTRAShowElementWithId( 'TRABatchStatusChange_fillerForSymbolColumn1');
    fTRAShowElementWithId( 'TRABatchStatusChange_fillerForSymbolColumn2');
    fTRAShowElementWithId( 'cid_ColumnaSimbolos_header');
    fTRAHideElementWithId( 'cid_ColumnaSimbolos_show_help');


    for( var unIdCounter=1; unIdCounter <= cTRAMaxRowsToLoopForRowElements; unIdCounter++) {
     
        if ( ! fTRAShowElementWithId( 'cid_FilaParaSimboloSobreTraducciones_' + unIdCounter + '_fillerForSymbol'))                    { break; };
        if ( ! fTRAShowElementWithId( 'cid_ColumnaSimbolos_' + unIdCounter))                                                          { break; };

        if ( ! fTRAHideElementWithId( 'cid_FilaParaSimboloSobreTraducciones_' + unIdCounter ))                                        { break; };
        if ( ! fTRAHideElementWithId( 'cid_FilaParaSimboloSobreTraducciones_' + unIdCounter + '_fillerForLanguageAndStatusColumns'))  { break; };
        if ( ! fTRAHideElementWithId( 'cid_FilaParaSimboloSobreTraducciones_' + unIdCounter + '_simboloCadena_SobreTraducciones'))    { break; };      
     }  
    return true;
}






/* #################################################################
Focus functions
################################################################# */

function setFocusToCadenaTraducida() {

    document.getElementById("theCadenaTraducida").focus();
}



function setFocusToGoToNext() {

    document.getElementById("theGoToNext").focus();
}










/* #################################################################
Maintenance of current element functions
################################################################# */




/* holds the state of being in edition in a hidden field */
function setEnEdicion( theSimboloCadena) {

    document.getElementById( 'theSimboloCadenaCursor').value = theSimboloCadena;
    return true;
}











/* #################################################################
Application specific show/hide element functions
################################################################# */




/* cleans all the filter parameters */
function pTRAResetFiltros( ) {

    document.getElementById( 'theSearchSimbolo').value = "";
    document.getElementById( 'theSearchCadenaTraducida').value = "";
    document.getElementById( 'theSearchUsuarioCreador').value = "";
    document.getElementById( 'theSearchFechaCreacionInicial').value = "";
    document.getElementById( 'theSearchFechaCreacionFinal').value = "";
    document.getElementById( 'theSearchUsuarioTraductor').value = "";
    document.getElementById( 'theSearchFechaTraduccionInicial').value = "";
    document.getElementById( 'theSearchFechaTraduccionFinal').value = "";
    document.getElementById( 'theSearchUsuarioRevisor').value = "";
    document.getElementById( 'theSearchFechaRevisionInicial').value = "";
    document.getElementById( 'theSearchFechaRevisionFinal').value = "";
    document.getElementById( 'theSearchUsuarioCoordinador').value = "";
    document.getElementById( 'theSearchFechaDefinitivoInicial').value = "";
    document.getElementById( 'theSearchFechaDefinitivoFinal').value = "";
    document.getElementById( 'theSearchIdCadena').value = "";
    document.getElementById( 'theSearchUsuarioModificador').value = "";
    document.getElementById( 'theSearchFechaModificacionInicial').value = "";
    document.getElementById( 'theSearchFechaModificacionFinal').value = "";
    document.getElementById( 'theSearchIdCadena').value = "";

    pTRAResetFiltrosEstados();

    pTRAResetFiltroNombresModulos(); 
    
    document.getElementById( 'theInactiveStrings').checked = 0;

    return true;
}


/* cleans all the GoTo parameters */
function pTRAResetGoToParameters( ) {

    document.getElementById( 'theGoToSymbolIndex').value = "";
    document.getElementById( 'theGoToPageIndex').value = "";
    document.getElementById( 'theGoToSymbolStartingWith').value = "";

    return true;
}


/* changes from true to false and back a filter by translation status */
function pTRAToggleFiltroEstado( pEstadoTraduccion ) {
    if (document.getElementById( 'theEstadosAIncluir_' + pEstadoTraduccion).checked == 0) {
        document.getElementById( 'theEstadosAIncluir_' + pEstadoTraduccion).checked = 1;
    }
    else {
        document.getElementById( 'theEstadosAIncluir_' + pEstadoTraduccion).checked = 0;
    }
    return true;
}




/* changes from true to false and back the inclussion of a reference language */
function pTRAToggleIdiomaReferencia( theIndexIdioma ) {
    if (document.getElementById( 'theIdiomasReferencia_' + theIndexIdioma).checked  == 0) {
        document.getElementById( 'theIdiomasReferencia_' + theIndexIdioma).checked = 1;
    }
    else {
        document.getElementById( 'theIdiomasReferencia_' + theIndexIdioma).checked = 0;
    }
    return true;
}




/* cleans  the NombresModulos filter parameter */
function pTRAResetFiltroNombresModulos( ) {

    for( var unIdCounter=0; unIdCounter < cTRAMaxRowsToLoopForOtherElements; unIdCounter++) {

        var unElement = document.getElementById( 'theNombreModulo_' + unIdCounter );
    
        if ( !unElement) {
            break;
        }
        unElement.checked = 0;
    }  
    
    var unElement = document.getElementById( 'theNombreModulo_NoEspecificado');    
    if ( unElement) {
        unElement.checked = 0;
    }
    unElement = document.getElementById( 'cid_TRAToggleAllModules');    
    if ( unElement) {
        unElement.checked = 0;
    }    
}





/* selects to retrieve and make visible all the sections in the page */
function pTRATodasSeccionesPresentacion( ) {
    document.getElementById( 'theMostrarInforme' ).checked = 1;
    document.getElementById( 'theMostrarHistoria').checked = 1;
    document.getElementById( 'theMostrarLista'   ).checked = 1;
}




/* selects to retrieve and make visible all the sections in the page */
function pTRATodasSeccionesTechnicalPresentacion( ) {
    document.getElementById( 'theRenderFormSubmit' ).checked = 1;
    document.getElementById( 'theRenderRequest'  ).checked = 1;
    document.getElementById( 'theRenderFullRequest').checked = 1;
    document.getElementById( 'theRenderAsyncRequest').checked = 1;
    document.getElementById( 'theRenderTimes'   ).checked = 1;
    document.getElementById( 'theRenderProfile'   ).checked = 1;
}




/* toggles the selection of a presentacion seccion 
 used by onclick event handlers on the section names
*/
function pTRAToggleSeccionPresentacion( theNombreSeccion ) {
    if (document.getElementById( theNombreSeccion).checked  == 0) {
        document.getElementById( theNombreSeccion).checked = 1;
    }
    else {
        document.getElementById( theNombreSeccion).checked = 0;
    }
    return true;
}



/* cleans  the EstadoTraduccion filter parameters */
function pTRAResetFiltrosEstados( ) {

    document.getElementById( 'theEstadosAIncluir_Pendiente').checked = 1;
    document.getElementById( 'theEstadosAIncluir_Traducida').checked = 1;
    document.getElementById( 'theEstadosAIncluir_Revisada').checked = 1;
    document.getElementById( 'theEstadosAIncluir_Definitiva').checked = 1;
    return true;
}






/* #################################################################
General utility functions for check boxes
################################################################# */


/* turns a checkbox into a radio button... sort of */
function toggle_boolean(visibleCheckbox, hiddenBoolean) {

    var vis = document.getElementById(visibleCheckbox);
    var hidden = document.getElementById(hiddenBoolean);
    if (vis.checked) {
        hidden.value = 1;
    } else {
        hidden.value = 0;
    }
    return true;
}






















function pTRAResetUserInterfaceEventsLog( ) {
    var unElementoUserInterfaceEventsDisplay = document.getElementById( 'theUserInterfaceEvents_Display_Field');
    if ( !unElementoUserInterfaceEventsDisplay) {
        return false;
    }

    unElementoUserInterfaceEventsDisplay.value = '';
    
    return true;
}


cUserInterfaceLogIndent = '    ';
 

function pLogUserInterfaceEvent_IGNORED( theEventName, theExtraInfo) {
    if ( !fTRAMustRenderUserInterfaceEvents()) {
        return false;
    }
    var unElementoUserInterfaceEventsDisplay = document.getElementById( 'theUserInterfaceEvents_Display_Field');
    if ( !unElementoUserInterfaceEventsDisplay) {
        return false;
    }
    var unCurrentEventsLog = unElementoUserInterfaceEventsDisplay.value;
    unElementoUserInterfaceEventsDisplay.value = 'IGNORED ' + theEventName + ' ' + theExtraInfo + '\n\n' + unCurrentEventsLog;
    
    return true;
 }

  

function pLogUserInterfaceEvent_BEGIN( theEventName, theExtraInfo) {
    if ( !fTRAMustRenderUserInterfaceEvents()) {
        return false;
    }
    var unElementoUserInterfaceEventsDisplay = document.getElementById( 'theUserInterfaceEvents_Display_Field');
    if ( !unElementoUserInterfaceEventsDisplay) {
        return false;
    }
    var unCurrentEventsLog = unElementoUserInterfaceEventsDisplay.value;
    unElementoUserInterfaceEventsDisplay.value = 'BEGIN ' + theEventName + ' ' + theExtraInfo + '\n\n' + unCurrentEventsLog;
    
    return true;
 }

 
 
 
function pLogUserInterfaceEvent( theEventName, theExtraInfo) {
    if ( !fTRAMustRenderUserInterfaceEvents()) {
        return false;
    }
    var unElementoUserInterfaceEventsDisplay = document.getElementById( 'theUserInterfaceEvents_Display_Field');
    if ( !unElementoUserInterfaceEventsDisplay) {
        return false;
    }
    var unCurrentEventsLog = unElementoUserInterfaceEventsDisplay.value;
    unElementoUserInterfaceEventsDisplay.value = cUserInterfaceLogIndent + '  ' + theEventName + ' ' + theExtraInfo + '\n' + unCurrentEventsLog;
    
    return true;
 }
 
 
 

function pLogUserInterfaceEvent_END( theEventName, theExtraInfo) {
    if ( !fTRAMustRenderUserInterfaceEvents()) {
        return false;
    }
    var unElementoUserInterfaceEventsDisplay = document.getElementById( 'theUserInterfaceEvents_Display_Field');
    if ( !unElementoUserInterfaceEventsDisplay) {
        return false;
    }
    var unCurrentEventsLog = unElementoUserInterfaceEventsDisplay.value
    unElementoUserInterfaceEventsDisplay.value = 'END   ' + theEventName + ' ' + theExtraInfo + '\n' + unCurrentEventsLog;
    
    return true;
 }




/* #################################################################
Top event handlers
################################################################# */




function fTRAEvtHlr_Editor_TextArea_OnKeyPress( event) {

    try {
        pLogUserInterfaceEvent_BEGIN( 'fTRAEvtHlr_Editor_TextArea_OnKeyPress', '');
        
        if ( gUserInterfaceInTransition) {
            pLogUserInterfaceEvent_IGNORED( 'fTRAEvtHlr_Editor_TextArea_OnKeyPress', '');
            return false;
        }
        gUserInterfaceInTransition = true;
    
        if ( !event) {
            return false;
        }

        try {
            var unKeyNumber = fTRAKeyNumberFromEvent( event);
            
            pLogUserInterfaceEvent( 'fTRAEvtHlr_Editor_TextArea_OnKeyPress', 'keyNumber:' + unKeyNumber);
                    
            if ( unKeyNumber == cKeyNumberEscape) {
    
                try {
     
                    var unKeyActionEscape = fTRAKeyAction_Escape();
                    if ( unKeyActionEscape == cKeyAction_Escape_Escape) {
                    
                        pLogUserInterfaceEvent( 'fTRAEvtHlr_Editor_TextArea_OnKeyPress', 'action: ' + unKeyActionEscape);
                        
                        /* pTRADisableElementWithId( 'theCadenaTraducida'); */
                        
                        pTRAShutdownEditor();
                        pTRAResetCurrentEditorIndex();

                        return false;
                    }
                    else {
                        return true;
                    }
                }
                finally {
                    /* pTRAEnableElementWithId( 'theCadenaTraducida'); */
                }
            }
                
            if ( unKeyNumber == cKeyNumberTab) {
                try {
                    var unEditorRowIndex = fTRACadenaTraducidaIndexNumber();
                    if ( !unEditorRowIndex) {
                        return true;
                    }
                    
                    var unKeyActionTab = fTRAKeyAction_Tab();
                                    
                    if (( unKeyActionTab == cKeyAction_Traducir) || ( unKeyActionTab == cKeyAction_TraducirYAvanzar))  {
                    
                        if ( ! fTRANoConfirmTranslationChanges()) {
                        
                            var unAvoidConfirmation  = fTRA_GetConstantValue( 'cTRAId_ToAvoidConfirmationDialogsCheckDoNotConfirmOptionMsg');
                            var unConfirmTranslateMsg = fTRA_GetConstantValue( 'cTRAId_ConfirmTranslateMsg');
                            var unConfirmed          = window.confirm( unConfirmTranslateMsg + '?\n' + unAvoidConfirmation);                        
                            if (! unConfirmed) {
                                return false;
                            }
                        
                            var unReallyConfirmTranslateMsg = fTRA_GetConstantValue( 'cTRAId_ReallyConfirmTranslateMsg');
                            unConfirmed = window.confirm( unReallyConfirmTranslateMsg + '?\n' + unAvoidConfirmation);
                            if (! unConfirmed) {
                                return false;
                            }   
                        }
                    
                        pLogUserInterfaceEvent( 'fTRAEvtHlr_Editor_TextArea_OnKeyPress', 'action: ' + unKeyActionTab + ' phase: traducir');
                                
                        /* pTRADisableElementWithId( 'theCadenaTraducida'); */
                        
                        fTRA_FromEditorToDatosEnFila();
                        
                        if ( fTRA_HayCambiosPendientesFilaNumero( unEditorRowIndex)) {
                            
                            fTRA_SetBGColorEnCadenaTraducidaFilaNumero( unEditorRowIndex, cTRABGColor_Translation_ChangedTranslation);  
    
                            if ( fAsynchronousTranslationMode()) {
                                
                                fTRASubmitCadenaTraducida_Async(    unEditorRowIndex);
                                fTRA_UpdateSavedCadenaTraducidaFilaNumero( unEditorRowIndex);
                            }
                            else {
                                
                                fTRASubmitCadenaTraducida_Sync();
                                return false;
                            }
                        }
                        else {                    
                            pLogUserInterfaceEvent( '      fTRAEvtHlr_Editor_TextArea_OnKeyPress', 'action: ' + unKeyActionTab + 'ignored: same_value');
                        }
                        if (  unKeyActionTab == cKeyAction_Traducir) {
                            fSetFocusToEditorTextArea();
                            return false;
                        }
                    }
                    
                    if (( unKeyActionTab == cKeyAction_Avanzar) || ( unKeyActionTab == cKeyAction_TraducirYAvanzar))  {
                    
                        pLogUserInterfaceEvent( 'fTRAEvtHlr_Editor_TextArea_OnKeyPress', 'action: ' + unKeyActionTab + ' phase: avanzar');
                        
                        /* pTRADisableElementWithId( 'theCadenaTraducida'); */
    
                        if ( !( unKeyActionTab == cKeyAction_TraducirYAvanzar)) {
                        
                            fTRA_FromEditorToDatosEnFila();
                        }
                                
                        if (!unEditorRowIndex) {
                            unEditorRowIndex = 1;
                        }
                        else {
                            unEditorRowIndex += 1
                        }
    
                        pTRAShutdownEditor();
                        
                        pTRAAbrirEditorEnFilaNumero( unEditorRowIndex);
                        
                        return false;
                    }
                     
                    
                    if ( unKeyActionTab == cKeyAction_NextTabIndex)  {
                    
                        pLogUserInterfaceEvent( 'fTRAEvtHlr_Editor_TextArea_OnKeyPress', 'action: ' + unKeyActionTab);
                        
                        /* pTRADisableElementWithId( 'theCadenaTraducida'); */
                        
                        fTRA_FromEditorToDatosEnFila();

                        fTRAMoveFocus_AfterEditorTextArea();
                        
                        return false;
                    }
                    
                    /* allow continuation of processing of tab keystroke */
                    return true;
                }
                finally {
                    /*pTRAEnableElementWithId( 'theCadenaTraducida'); */
                }
            }
            
                
            if ( unKeyNumber == cKeyNumberCR) {
                try {                       
     
                    var unEditorRowIndex = fTRACadenaTraducidaIndexNumber();
                    if ( !unEditorRowIndex) {
                        return true;
                    }
                    var unKeyActionCR = fTRAKeyAction_CR();
                    
                    
                    
                    if (( unKeyActionCR == cKeyAction_Traducir) || ( unKeyActionCR == cKeyAction_TraducirYAvanzar))  {
                                
                        pLogUserInterfaceEvent( 'fTRAEvtHlr_Editor_TextArea_OnKeyPress', 'action: ' + unKeyActionCR + ' phase: traducir');
                        
                        if ( ! fTRANoConfirmTranslationChanges()) {
                        
                            var unAvoidConfirmation    = fTRA_GetConstantValue( 'cTRAId_ToAvoidConfirmationDialogsCheckDoNotConfirmOptionMsg');
                            var unConfirmTranslateMsg  = fTRA_GetConstantValue( 'cTRAId_ConfirmTranslateMsg');
                            var unConfirmed            = window.confirm( unConfirmTranslateMsg + '?\n' + unAvoidConfirmation);                                                
                            if (! unConfirmed) {
                                return false;
                            }
                        
                            var unReallyConfirmTranslateMsg = fTRA_GetConstantValue( 'cTRAId_ReallyConfirmTranslateMsg');
                            unConfirmed = window.confirm( unReallyConfirmTranslateMsg + '?\n' + unAvoidConfirmation);
                            if (! unConfirmed) {
                                return false;
                            }  
                        }
                        
                        /* pTRADisableElementWithId( 'theCadenaTraducida'); */
                        
                        fTRA_FromEditorToDatosEnFila();
                        
                        if ( fTRA_HayCambiosPendientesFilaNumero( unEditorRowIndex)) {
                                                    
                            if ( fAsynchronousTranslationMode()) {                        
        
                                fTRASubmitCadenaTraducida_Async(   unEditorRowIndex);
                                fTRA_UpdateSavedCadenaTraducidaFilaNumero( unEditorRowIndex);
                            }
                            else {
                            
                                fTRASubmitCadenaTraducida_Sync();
                                return false;
                            }
                        }
                        else {                    
                            pLogUserInterfaceEvent( '      fTRAEvtHlr_Editor_TextArea_OnKeyPress', 'action: ' + unKeyActionCR + 'ignored: same_value');
                        }
                        if (  unKeyActionCR == cKeyAction_Traducir) {
                        
                            fSetFocusToEditorTextArea();

                            return false;
                        }
                    }
                    
                    if (( unKeyActionCR == cKeyAction_Avanzar) || ( unKeyActionCR == cKeyAction_TraducirYAvanzar))  {
                    
                        /* pTRADisableElementWithId( 'theCadenaTraducida'); */
                        
                        pLogUserInterfaceEvent( 'fTRAEvtHlr_Editor_TextArea_OnKeyPress', 'action: ' + unKeyActionCR + ' phase: avanzar');
                        
                        if ( !( unKeyActionCR == cKeyAction_TraducirYAvanzar)) {
                        
                            fTRA_FromEditorToDatosEnFila();
                        }
                                
                        if (!unEditorRowIndex) {
                            unEditorRowIndex = 1;
                        }
                        else {
                            unEditorRowIndex += 1
                        }
                        
                        pTRAShutdownEditor( );
                        
                        pTRAAbrirEditorEnFilaNumero( unEditorRowIndex);
                        
                        return false;
                    }
                    
                    if ( unKeyActionCR == cKeyAction_NextTabIndex)  {
                        pLogUserInterfaceEvent( 'fTRAEvtHlr_Editor_TextArea_OnKeyPress', 'action: ' + unKeyActionCR);
                        
                        /* pTRADisableElementWithId( 'theCadenaTraducida'); */
            
                        fTRA_FromEditorToDatosEnFila();
                        
                        fTRAMoveFocus_AfterEditorTextArea( );
                        
                        return false;
                    }
                    /* allow continuation of processing of CR keystroke */
                    return true;
                }
                finally {
                    /* pTRAEnableElementWithId( 'theCadenaTraducida'); */
                }
            }            
            /* allow continuation of processing of non tab, non CR keystroke */
            return true;
                
         }
        catch( unaException) {
            throw unaException;
        }
    }
    finally {
        gUserInterfaceInTransition = false;
        pLogUserInterfaceEvent_END( 'fTRAEvtHlr_Editor_TextArea_OnKeyPress', '');
    }
}




function fTRAEvtHlr_Editor_TextArea_OnBlur( ) {

    try {
        pLogUserInterfaceEvent_BEGIN( 'fTRAEvtHlr_Editor_TextArea_OnBlur', '');
        
        if ( gUserInterfaceInTransition) {
            pLogUserInterfaceEvent_IGNORED( 'fTRAEvtHlr_Editor_TextArea_OnBlur', '');
            return false;
        }
        gUserInterfaceInTransition = true;
            
        try {
            try {
            
                /* pTRADisableElementWithId( 'theCadenaTraducida'); */
                
                fTRA_FromEditorToDatosEnFila();
                
            }
            finally {
                /* pTRAEnableElementWithId( 'theCadenaTraducida'); */
            }
        }
        catch( unaException) {
            throw unaException;
        }
    }
    finally {
        gUserInterfaceInTransition = false;
        pLogUserInterfaceEvent_END( 'fTRAEvtHlr_Editor_TextArea_OnBlur', '');
    }
}




function fTRAEvtHlr_Editor_Button_Traducir_OnMouseUp() {

    try {
        if ( gUserInterfaceInTransition) {
            pLogUserInterfaceEvent_IGNORED( 'fTRAEvtHlr_Editor_Button_Traducir_OnMouseUp', '');
            return false;
        }
        gUserInterfaceInTransition = true;

        pLogUserInterfaceEvent_BEGIN( 'fTRAEvtHlr_Editor_Button_Traducir_OnMouseUp', '');
        
        try {
                
            pTRADisableElementWithId( 'TRAStatusChangeButton_Traducir');


            try {
                  
                if ( ! fTRANoConfirmTranslationChanges()) {
                
                    var unAvoidConfirmation    = fTRA_GetConstantValue( 'cTRAId_ToAvoidConfirmationDialogsCheckDoNotConfirmOptionMsg');
                    var unConfirmTranslateMsg  = fTRA_GetConstantValue( 'cTRAId_ConfirmTranslateMsg');
                    var unConfirmed            = window.confirm( unConfirmTranslateMsg + '?\n' + unAvoidConfirmation);                                                
                    if (! unConfirmed) {
                        return false;
                    }
                
                    var unReallyConfirmTranslateMsg = fTRA_GetConstantValue( 'cTRAId_ReallyConfirmTranslateMsg');
                    unConfirmed = window.confirm( unReallyConfirmTranslateMsg + '?\n' + unAvoidConfirmation);
                    if (! unConfirmed) {
                        return false;
                    }    
                }
                        
                var unDatosAceptados = fTRA_FromEditorToDatosEnFila();
            
                var unEditorRowIndex =  fTRACadenaTraducidaIndexNumber();
                if ( unEditorRowIndex) {
                
                    if ( !unDatosAceptados) {
                        fTRA_BlinkBGColorEnCadenaTraducidaFilaNumero( unEditorRowIndex, cTRABGColor_Translation_IgnoredSave);  
                    }
                
                    if ( fTRA_HayCambiosPendientesFilaNumero( unEditorRowIndex)) {
                    
                        if ( fAsynchronousTranslationMode()) {
                        
                            fTRASubmitCadenaTraducida_Async(    unEditorRowIndex);
                            fTRA_UpdateSavedCadenaTraducidaFilaNumero( unEditorRowIndex);
                        }
                        else {
                            fTRASubmitCadenaTraducida_Sync();
                        }
                    }
                    else {                    
                        fTRA_BlinkBGColorEnCadenaTraducidaFilaNumero( unEditorRowIndex, cTRABGColor_Translation_IgnoredSave);  
                        pLogUserInterfaceEvent( '     fTRAEvtHlr_Editor_Button_Traducir_OnMouseUp', 'ignored: same_value');
                    }
                }
            }
            catch( unaException) {
                throw unaException;
            }
        }
        finally {
            pTRAEnableElementWithId( 'TRAStatusChangeButton_Traducir');
        }
    }
    finally {
        gUserInterfaceInTransition = false;
        pLogUserInterfaceEvent_END( 'fTRAEvtHlr_Editor_Button_Traducir_OnMouseUp', '');
    }
}





function fTRAEvtHlr_Editor_Button_Traducir_OnKeyPress( event) {

    try {
        pLogUserInterfaceEvent_BEGIN( 'fTRAEvtHlr_Editor_Button_Traducir_OnKeyPress', '');
        
        if ( gUserInterfaceInTransition) {
            pLogUserInterfaceEvent_IGNORED( 'fTRAEvtHlr_Editor_Button_Traducir_OnKeyPress', '');
            return false;
        }
        gUserInterfaceInTransition = true;

        if ( !event) {
            return false;
        }
        try {
    
            pTRADisableElementWithId( 'TRAStatusChangeButton_Traducir');

            try {            
                            
                var unKeyNumber = fTRAKeyNumberFromEvent( event);
                
                pLogUserInterfaceEvent( 'fTRAEvtHlr_Editor_Button_Traducir_OnKeyPress', 'keyNumber: ' + unKeyNumber);
                
                if ( unKeyNumber == cKeyNumberCR) {
                
                    if ( ! fTRANoConfirmTranslationChanges()) {
                        var unAvoidConfirmation    = fTRA_GetConstantValue( 'cTRAId_ToAvoidConfirmationDialogsCheckDoNotConfirmOptionMsg');
                        var unConfirmTranslateMsg  = fTRA_GetConstantValue( 'cTRAId_ConfirmTranslateMsg');
                        var unConfirmed            = window.confirm( unConfirmTranslateMsg + '?\n' + unAvoidConfirmation);                                                
                        if (! unConfirmed) {
                            return false;
                        }
                    
                        var unReallyConfirmTranslateMsg = fTRA_GetConstantValue( 'cTRAId_ReallyConfirmTranslateMsg');
                        unConfirmed = window.confirm( unReallyConfirmTranslateMsg + '?\n' + unAvoidConfirmation);
                        if (! unConfirmed) {
                            return false;
                        } 
                    }
                
                    fTRA_FromEditorToDatosEnFila();
                
                    var unEditorRowIndex =  fTRACadenaTraducidaIndexNumber()
                    if ( unEditorRowIndex) {
                    
                        if ( fTRA_HayCambiosPendientesFilaNumero( unEditorRowIndex)) {  
    
                            if ( fAsynchronousTranslationMode()) {
                            
                                fTRASubmitCadenaTraducida_Async( unEditorRowIndex);
                                fTRA_UpdateSavedCadenaTraducidaFilaNumero( unEditorRowIndex);
                            }
                            else {
                                fTRASubmitCadenaTraducida_Sync();
                            }
                        }
                        else {                    
                            pLogUserInterfaceEvent( '     fTRAEvtHlr_Editor_Button_Traducir_OnKeyPress', 'ignored: same_value');
                        }
                    }
                    return false;
                }
                else {
                    return true;
                }
            }
            catch( unaException) {
                throw unaException;
            }
        }
        finally {
            pTRAEnableElementWithId( 'TRAStatusChangeButton_Traducir');
        }
    }
    finally {
        gUserInterfaceInTransition = false;
        pLogUserInterfaceEvent_END( 'fTRAEvtHlr_Editor_Button_Traducir_OnKeyPress', '');
    }
}






function fTRAEvtHlr_Editor_Button_Pendiente_OnMouseUp() {

    try {
        pLogUserInterfaceEvent_BEGIN( 'fTRAEvtHlr_Editor_Button_Pendiente_OnMouseUp', '');

        if ( gUserInterfaceInTransition) {
            pLogUserInterfaceEvent_IGNORED( 'fTRAEvtHlr_Editor_Button_Pendiente_OnMouseUp', '');
            return false;
        }
        gUserInterfaceInTransition = true;

        try {
            pTRADisableElementWithId( 'TRAStatusChangeButton_Pendiente');
            pTRADisableElementWithId( 'TRAStatusChangeButton_Pendiente_Icon');

            try {
                if ( ! fTRANoConfirmTranslationDelete()) {
                
                    var unAvoidConfirmation    = fTRA_GetConstantValue( 'cTRAId_ToAvoidConfirmationDialogsCheckDoNotConfirmOptionMsg');
                    var unConfirmDeleteMsg     = fTRA_GetConstantValue( 'cTRAId_ConfirmDeleteMsg');
                    var unConfirmed            = window.confirm( unConfirmDeleteMsg + '?\n' + unAvoidConfirmation);                                                
                    if (! unConfirmed) {
                        return false;
                    }
                
                    var unReallyConfirmDeleteMsg = fTRA_GetConstantValue( 'cTRAId_ReallyConfirmDeleteMsg');
                    unConfirmed = window.confirm( unReallyConfirmDeleteMsg + '?\n' + unAvoidConfirmation);
                    if (! unConfirmed) {
                        return false;
                    } 
                }
                            
                var unEditorRowIndex =  fTRACadenaTraducidaIndexNumber();
                if ( unEditorRowIndex) {
                
                    fTRA_DeleteSavedAndNewCadenaTraducidaFilaNumero( unEditorRowIndex);
                    fTRA_ResetValorTextAreaFilaNumero( unEditorRowIndex);
                    
                    if ( fAsynchronousTranslationMode()) {
                            
                        fTRASubmitStatusChange_Async( unEditorRowIndex, 'Pendiente');
                     }
                    else {
                        fTRASubmitStatusChange_Sync( 'Pendiente');
                    }
                }
            }
            catch( unaException) {
                throw unaException;
            }
        }
        finally {
            pTRAEnableElementWithId( 'TRAStatusChangeButton_Pendiente');
            pTRAEnableElementWithId( 'TRAStatusChangeButton_Pendiente_Icon');
        }
    }
    finally {
        gUserInterfaceInTransition = false;
        pLogUserInterfaceEvent_END( 'fTRAEvtHlr_Editor_Button_Pendiente_OnMouseUp', '');
    }
}





function fTRAEvtHlr_Editor_Button_Pendiente_OnKeyPress( event) {

    try {
        pLogUserInterfaceEvent_BEGIN( 'fTRAEvtHlr_Editor_Button_Pendiente_OnKeyPress', '');
        
        if ( gUserInterfaceInTransition) {
            pLogUserInterfaceEvent_IGNORED( 'fTRAEvtHlr_Editor_Button_Pendiente_OnKeyPress', '');
            return false;
        }
        gUserInterfaceInTransition = true;

        if ( !event) {
            return false;
        }
        try {
    
            if ( ! fTRANoConfirmTranslationDelete()) {
                var unAvoidConfirmation    = fTRA_GetConstantValue( 'cTRAId_ToAvoidConfirmationDialogsCheckDoNotConfirmOptionMsg');
                var unConfirmDeleteMsg     = fTRA_GetConstantValue( 'cTRAId_ConfirmDeleteMsg');
                var unConfirmed            = window.confirm( unConfirmDeleteMsg + '?\n' + unAvoidConfirmation);                                                
                if (! unConfirmed) {
                    return false;
                }
            
                var unReallyConfirmDeleteMsg = fTRA_GetConstantValue( 'cTRAId_ReallyConfirmDeleteMsg');
                unConfirmed = window.confirm( unReallyConfirmDeleteMsg + '?\n' + unAvoidConfirmation);
                if (! unConfirmed) {
                    return false;
                } 
            }        
            
            pTRADisableElementWithId( 'TRAStatusChangeButton_Pendiente');
            pTRADisableElementWithId( 'TRAStatusChangeButton_Pendiente_Icon');

            try {
            
                var unKeyNumber = fTRAKeyNumberFromEvent( event);
                    
                pLogUserInterfaceEvent( 'fTRAEvtHlr_Editor_Button_Pendiente_OnKeyPress', 'key:' + unKeyNumber);
                
                if ( unKeyNumber == cKeyNumberCR) {
                
                    var unEditorRowIndex =  fTRACadenaTraducidaIndexNumber();
                    if ( unEditorRowIndex) {
                    
                        fTRA_DeleteSavedAndNewCadenaTraducidaFilaNumero( unEditorRowIndex);
                        fTRA_ResetValorTextAreaFilaNumero(               unEditorRowIndex);

                        if ( fAsynchronousTranslationMode()) {
                                   
                            fTRASubmitStatusChange_Async( unEditorRowIndex, 'Pendiente');
                        }
                        else {
                            pTRASubmitStatusChange_Sync( 'Pendiente');
                        }

                    }
                    return false;
                }
                else {
                    return true;
                }
            }
            catch( unaException) {
                throw unaException;
            }
        }
        finally {
            pTRAEnableElementWithId( 'TRAStatusChangeButton_Pendiente');
            pTRAEnableElementWithId( 'TRAStatusChangeButton_Pendiente_Icon');
        }
    }
    finally {
        gUserInterfaceInTransition = false;
        pLogUserInterfaceEvent_END( 'fTRAEvtHlr_Editor_Button_Pendiente_OnKeyPress', '');
    }
}




function fTRAEvtHlr_Editor_Button_InvalidarTraduccionesCadena_OnMouseUp() {

    try {
        pLogUserInterfaceEvent_BEGIN( 'fTRAEvtHlr_Editor_Button_InvalidarTraduccionesCadena_OnMouseUp', '');

        if ( gUserInterfaceInTransition) {
            pLogUserInterfaceEvent_IGNORED( 'fTRAEvtHlr_Editor_Button_InvalidarTraduccionesCadena_OnMouseUp', '');
            return false;
        }
        gUserInterfaceInTransition = true;

        try {
            pTRADisableElementWithId( 'TRAStatusChangeButton_InvalidarTraduccionesCadena');
            pTRADisableElementWithId( 'TRAStatusChangeButton_InvalidarTraduccionesCadena_Icon1');
            pTRADisableElementWithId( 'TRAStatusChangeButton_InvalidarTraduccionesCadena_Icon2');

            try {
            
                var unInvalidateStringTranslationsMsg = fTRA_GetConstantValue( 'cTRAId_ConfirmInvalidateStringTranslationsMsg');
                var unConfirmed = window.confirm( unInvalidateStringTranslationsMsg + '?');
                if (! unConfirmed) {
                    return false;
                }
            
                var unReallyInvalidateStringTranslationsMsg = fTRA_GetConstantValue( 'cTRAId_ReallyInvalidateStringTranslationsMsg');
                unConfirmed = window.confirm( unReallyInvalidateStringTranslationsMsg + '?');
                if (! unConfirmed) {
                    return false;
                }
                
                var unEditorRowIndex =  fTRACadenaTraducidaIndexNumber();
                if ( unEditorRowIndex) {
                
                    fTRA_DeleteSavedAndNewCadenaTraducidaFilaNumero( unEditorRowIndex);
                    fTRA_ResetValorTextAreaFilaNumero( unEditorRowIndex);
                    

                    /* ACV 20090927 Error Does not refresh properly because the response is not structured as expected
                     Known limitation: Invalidate in Synch Mode

                    if ( fAsynchronousTranslationMode()) {
                               
                        fTRASubmitInvalidateStringTranslations_Async( unEditorRowIndex);
                    }
                    else {
                        fTRASubmitInvalidateStringTranslations_Sync( );
                    }
                    */
                    fTRASubmitInvalidateStringTranslations_Sync( );
                }
            }
            catch( unaException) {
                throw unaException;
            }
        }
        finally {
            pTRAEnableElementWithId( 'TRAStatusChangeButton_InvalidarTraduccionesCadena');
            pTRAEnableElementWithId( 'TRAStatusChangeButton_InvalidarTraduccionesCadena_Icon1');
            pTRAEnableElementWithId( 'TRAStatusChangeButton_InvalidarTraduccionesCadena_Icon2');
        }
    }
    finally {
        gUserInterfaceInTransition = false;
        pLogUserInterfaceEvent_END( 'fTRAEvtHlr_Editor_Button_InvalidarTraduccionesCadena_OnMouseUp', '');
    }
}





function fTRAEvtHlr_Editor_Button_InvalidarTraduccionesCadena_OnKeyPress( event) {

    try {
        pLogUserInterfaceEvent_BEGIN( 'fTRAEvtHlr_Editor_Button_InvalidarTraduccionesCadena_OnKeyPress', '');
        
        if ( gUserInterfaceInTransition) {
            pLogUserInterfaceEvent_IGNORED( 'fTRAEvtHlr_Editor_Button_InvalidarTraduccionesCadena_OnKeyPress', '');
            return false;
        }
        gUserInterfaceInTransition = true;

        if ( !event) {
            return false;
        }
        try {
    
            pTRADisableElementWithId( 'TRAStatusChangeButton_InvalidarTraduccionesCadena');
            pTRADisableElementWithId( 'TRAStatusChangeButton_InvalidarTraduccionesCadena_Icon1');
            pTRADisableElementWithId( 'TRAStatusChangeButton_InvalidarTraduccionesCadena_Icon2');
            try {
            
                var unKeyNumber = fTRAKeyNumberFromEvent( event);
                    
                pLogUserInterfaceEvent( 'fTRAEvtHlr_Editor_Button_InvalidarTraduccionesCadena_OnKeyPress', 'key:' + unKeyNumber);
                
                if ( unKeyNumber == cKeyNumberCR) {
                
                    var unInvalidateStringTranslationsMsg = fTRA_GetConstantValue( 'cTRAId_ConfirmInvalidateStringTranslationsMsg');
                    var unConfirmed = window.confirm( unInvalidateStringTranslationsMsg + '?');
                    if (! unConfirmed) {
                        return false;
                    }
                
                    var unReallyInvalidateStringTranslationsMsg = fTRA_GetConstantValue( 'cTRAId_ReallyInvalidateStringTranslationsMsg');
                    unConfirmed = window.confirm( unReallyInvalidateStringTranslationsMsg + '?');
                    if (! unConfirmed) {
                        return false;
                    }
                
                    var unEditorRowIndex =  fTRACadenaTraducidaIndexNumber();
                    if ( unEditorRowIndex) {
                    
                        fTRA_DeleteSavedAndNewCadenaTraducidaFilaNumero( unEditorRowIndex);
                        fTRA_ResetValorTextAreaFilaNumero(               unEditorRowIndex);

                        /* ACV 20090927 Error Does not refresh properly because the response is not structured as expected
                         Known limitation: Invalidate in Synch Mode 

                        if ( fAsynchronousTranslationMode()) {
                                   
                            fTRASubmitInvalidateStringTranslations_Async( unEditorRowIndex);
                        }
                        else {
                            fTRASubmitInvalidateStringTranslations_Sync( );
                        }
                        */
                        fTRASubmitInvalidateStringTranslations_Sync( );

                    }
                    return false;
                }
                else {
                    return true;
                }
            }
            catch( unaException) {
                throw unaException;
            }
        }
        finally {
            pTRAEnableElementWithId( 'TRAStatusChangeButton_InvalidarTraduccionesCadena');
            pTRAEnableElementWithId( 'TRAStatusChangeButton_InvalidarTraduccionesCadena_Icon1');
            pTRAEnableElementWithId( 'TRAStatusChangeButton_InvalidarTraduccionesCadena_Icon2');
        }
    }
    finally {
        gUserInterfaceInTransition = false;
        pLogUserInterfaceEvent_END( 'fTRAEvtHlr_Editor_Button_InvalidarTraduccionesCadena_OnKeyPress', '');
    }
}










function fTRAEvtHlr_Editor_Button_DesactivarCadena_OnMouseUp() {

    try {
        pLogUserInterfaceEvent_BEGIN( 'fTRAEvtHlr_Editor_Button_DesactivarCadena_OnMouseUp', '');

        if ( gUserInterfaceInTransition) {
            pLogUserInterfaceEvent_IGNORED( 'fTRAEvtHlr_Editor_Button_DesactivarCadena_OnMouseUp', '');
            return false;
        }
        gUserInterfaceInTransition = true;

        try {
            pTRADisableElementWithId( 'TRAStatusChangeButton_DesactivarCadena');
            pTRADisableElementWithId( 'TRAStatusChangeButton_DesactivarCadena_Icon');

            try {
            
                var unAvoidConfirmation  = fTRA_GetConstantValue( 'cTRAId_ToAvoidConfirmationDialogsCheckDoNotConfirmOptionMsg');
                var unDeactivateStringMsg = fTRA_GetConstantValue( 'cTRAId_ConfirmDeactivateStringMsg');
                var unConfirmed = window.confirm( unDeactivateStringMsg + '?\n' + unAvoidConfirmation);
                if (! unConfirmed) {
                    return false;
                }
            
                var unReallyDeactivateStringMsg = fTRA_GetConstantValue( 'cTRAId_ReallyDeactivateStringMsg');
                unConfirmed = window.confirm( unReallyDeactivateStringMsg + '?\n' + unAvoidConfirmation);
                if (! unConfirmed) {
                    return false;
                }
                
                var unEditorRowIndex =  fTRACadenaTraducidaIndexNumber();
                if ( unEditorRowIndex) {
                
                    fTRA_DeleteSavedAndNewCadenaTraducidaFilaNumero( unEditorRowIndex);
                    fTRA_ResetValorTextAreaFilaNumero( unEditorRowIndex);
                    

                    fTRASubmitDeactivateString_Sync( );
                }
            }
            catch( unaException) {
                throw unaException;
            }
        }
        finally {
            pTRAEnableElementWithId( 'TRAStatusChangeButton_DesactivarCadena');
            pTRAEnableElementWithId( 'TRAStatusChangeButton_DesactivarCadena_Icon');
        }
    }
    finally {
        gUserInterfaceInTransition = false;
        pLogUserInterfaceEvent_END( 'fTRAEvtHlr_Editor_Button_DesactivarCadena_OnMouseUp', '');
    }
}





function fTRAEvtHlr_Editor_Button_DesactivarCadena_OnKeyPress( event) {

    try {
        pLogUserInterfaceEvent_BEGIN( 'fTRAEvtHlr_Editor_Button_DesactivarCadena_OnKeyPress', '');
        
        if ( gUserInterfaceInTransition) {
            pLogUserInterfaceEvent_IGNORED( 'fTRAEvtHlr_Editor_Button_DesactivarCadena_OnKeyPress', '');
            return false;
        }
        gUserInterfaceInTransition = true;

        if ( !event) {
            return false;
        }
        try {
    
            pTRADisableElementWithId( 'TRAStatusChangeButton_DesactivarCadena');
            pTRADisableElementWithId( 'TRAStatusChangeButton_DesactivarCadena_Icon');
            try {
            
                var unKeyNumber = fTRAKeyNumberFromEvent( event);
                    
                pLogUserInterfaceEvent( 'fTRAEvtHlr_Editor_Button_DesactivarCadena_OnKeyPress', 'key:' + unKeyNumber);
                
                if ( unKeyNumber == cKeyNumberCR) {
                
                    var unAvoidConfirmation  = fTRA_GetConstantValue( 'cTRAId_ToAvoidConfirmationDialogsCheckDoNotConfirmOptionMsg');
                    var unDeactivateStringMsg = fTRA_GetConstantValue( 'cTRAId_ConfirmDeactivateStringMsg');
                    var unConfirmed = window.confirm( unDeactivateStringMsg + '?\n' + unAvoidConfirmation);
                    if (! unConfirmed) {
                        return false;
                    }
                
                    var unReallyDeactivateStringMsg = fTRA_GetConstantValue( 'cTRAId_ReallyDeactivateStringMsg');
                    unConfirmed = window.confirm( unReallyDeactivateStringMsg + '?\n' + unAvoidConfirmation);
                    if (! unConfirmed) {
                        return false;
                    }
                
                    var unEditorRowIndex =  fTRACadenaTraducidaIndexNumber();
                    if ( unEditorRowIndex) {
                    
                        fTRA_DeleteSavedAndNewCadenaTraducidaFilaNumero( unEditorRowIndex);
                        fTRA_ResetValorTextAreaFilaNumero(               unEditorRowIndex);

                        fTRASubmitDeactivateString_Sync( );

                    }
                    return false;
                }
                else {
                    return true;
                }
            }
            catch( unaException) {
                throw unaException;
            }
        }
        finally {
            pTRAEnableElementWithId( 'TRAStatusChangeButton_DesactivarCadena');
            pTRAEnableElementWithId( 'TRAStatusChangeButton_DesactivarCadena_Icon');
        }
    }
    finally {
        gUserInterfaceInTransition = false;
        pLogUserInterfaceEvent_END( 'fTRAEvtHlr_Editor_Button_DesactivarCadena_OnKeyPress', '');
    }
}










function fTRAEvtHlr_Editor_Button_ActivarCadena_OnMouseUp() {

    try {
        pLogUserInterfaceEvent_BEGIN( 'fTRAEvtHlr_Editor_Button_ActivarCadena_OnMouseUp', '');

        if ( gUserInterfaceInTransition) {
            pLogUserInterfaceEvent_IGNORED( 'fTRAEvtHlr_Editor_Button_ActivarCadena_OnMouseUp', '');
            return false;
        }
        gUserInterfaceInTransition = true;

        try {
            pTRADisableElementWithId( 'TRAStatusChangeButton_ActivarCadena');
            pTRADisableElementWithId( 'TRAStatusChangeButton_ActivarCadena_Icon');

            try {
                var unAvoidConfirmation  = fTRA_GetConstantValue( 'cTRAId_ToAvoidConfirmationDialogsCheckDoNotConfirmOptionMsg');
                var unActivateStringMsg = fTRA_GetConstantValue( 'cTRAId_ConfirmActivateStringMsg');
                var unConfirmed = window.confirm( unActivateStringMsg + '?\n' + unAvoidConfirmation);
                if (! unConfirmed) {
                    return false;
                }
            
                var unReallyActivateStringMsg = fTRA_GetConstantValue( 'cTRAId_ReallyActivateStringMsg');
                unConfirmed = window.confirm( unReallyActivateStringMsg + '?\n' + unAvoidConfirmation);
                if (! unConfirmed) {
                    return false;
                }
                
                var unEditorRowIndex =  fTRACadenaTraducidaIndexNumber();
                if ( unEditorRowIndex) {
                
                    fTRA_DeleteSavedAndNewCadenaTraducidaFilaNumero( unEditorRowIndex);
                    fTRA_ResetValorTextAreaFilaNumero( unEditorRowIndex);
                    

                    fTRASubmitActivateString_Sync( );
                }
            }
            catch( unaException) {
                throw unaException;
            }
        }
        finally {
            pTRAEnableElementWithId( 'TRAStatusChangeButton_ActivarCadena');
            pTRAEnableElementWithId( 'TRAStatusChangeButton_ActivarCadena_Icon');
        }
    }
    finally {
        gUserInterfaceInTransition = false;
        pLogUserInterfaceEvent_END( 'fTRAEvtHlr_Editor_Button_ActivarCadena_OnMouseUp', '');
    }
}





function fTRAEvtHlr_Editor_Button_ActivarCadena_OnKeyPress( event) {

    try {
        pLogUserInterfaceEvent_BEGIN( 'fTRAEvtHlr_Editor_Button_ActivarCadena_OnKeyPress', '');
        
        if ( gUserInterfaceInTransition) {
            pLogUserInterfaceEvent_IGNORED( 'fTRAEvtHlr_Editor_Button_ActivarCadena_OnKeyPress', '');
            return false;
        }
        gUserInterfaceInTransition = true;

        if ( !event) {
            return false;
        }
        try {
    
            pTRADisableElementWithId( 'TRAStatusChangeButton_ActivarCadena');
            pTRADisableElementWithId( 'TRAStatusChangeButton_ActivarCadena_Icon');
            try {
            
                var unKeyNumber = fTRAKeyNumberFromEvent( event);
                    
                pLogUserInterfaceEvent( 'fTRAEvtHlr_Editor_Button_ActivarCadena_OnKeyPress', 'key:' + unKeyNumber);
                
                if ( unKeyNumber == cKeyNumberCR) {
                
                var unAvoidConfirmation  = fTRA_GetConstantValue( 'cTRAId_ToAvoidConfirmationDialogsCheckDoNotConfirmOptionMsg');
                var unActivateStringMsg = fTRA_GetConstantValue( 'cTRAId_ConfirmActivateStringMsg');
                var unConfirmed = window.confirm( unActivateStringMsg + '?\n' + unAvoidConfirmation);
                    if (! unConfirmed) {
                        return false;
                    }
                
                    var unReallyActivateStringMsg = fTRA_GetConstantValue( 'cTRAId_ReallyActivateStringMsg');
                    unConfirmed = window.confirm( unReallyActivateStringMsg + '?\n' + unAvoidConfirmation);
                    if (! unConfirmed) {
                        return false;
                    }
                
                    var unEditorRowIndex =  fTRACadenaTraducidaIndexNumber();
                    if ( unEditorRowIndex) {
                    
                        fTRA_DeleteSavedAndNewCadenaTraducidaFilaNumero( unEditorRowIndex);
                        fTRA_ResetValorTextAreaFilaNumero(               unEditorRowIndex);

                        fTRASubmitActivateString_Sync( );

                    }
                    return false;
                }
                else {
                    return true;
                }
            }
            catch( unaException) {
                throw unaException;
            }
        }
        finally {
            pTRAEnableElementWithId( 'TRAStatusChangeButton_ActivarCadena');
            pTRAEnableElementWithId( 'TRAStatusChangeButton_ActivarCadena_Icon');
        }
    }
    finally {
        gUserInterfaceInTransition = false;
        pLogUserInterfaceEvent_END( 'fTRAEvtHlr_Editor_Button_ActivarCadena_OnKeyPress', '');
    }
}







function fTRAEvtHlr_Editor_Button_StatusChange_OnMouseUp( theEditorIndex, theNewTranslationStatus) {

    try {
        pLogUserInterfaceEvent_BEGIN( 'fTRAEvtHlr_Editor_Button_StatusChange_OnMouseUp', 'editorIndex:' + theEditorIndex + ' newStatus:' + theNewTranslationStatus);
        
        if ( gUserInterfaceInTransition) {
            pLogUserInterfaceEvent_IGNORED( 'fTRAEvtHlr_Editor_Button_StatusChange_OnMouseUp',  'editorIndex:' + theEditorIndex + ' newStatus:' + theNewTranslationStatus);
            return false;
        }
        gUserInterfaceInTransition = true;

         if ( !theEditorIndex) {
            return false;
        }
        if ( !theNewTranslationStatus) {
            return false;
        }
        
        var unEditorIndex = '' + theEditorIndex;
        unEditorIndex = parseInt( unEditorIndex)
        if ( !unEditorIndex) {
            return false;
        }
        
        try {
        
        
            if ( ! fTRANoConfirmStatusChanges()) {
                var unAvoidConfirmation  = fTRA_GetConstantValue( 'cTRAId_ToAvoidConfirmationDialogsCheckDoNotConfirmOptionMsg');
                var unConfirmStatusMsg = fTRA_GetConstantValue( 'cTRAId_ConfirmStatusChangeMsg');
                var unConfirmed = window.confirm( unConfirmStatusMsg + '?\n' + unAvoidConfirmation);
                if (! unConfirmed) {
                    return false;
                }
            
                var unReallyConfirmStatusMsg = fTRA_GetConstantValue( 'cTRAId_ReallyConfirmStatusChangeMsg');
                unConfirmed = window.confirm( unReallyConfirmStatusMsg + '?\n' + unAvoidConfirmation);
                if (! unConfirmed) {
                    return false;
                }   
            }
        
        
            pTRADisableElementWithId( 'TRAStatusChangeButton_' + unEditorIndex + '_' + theNewTranslationStatus);
            try {
            
                var unCurrentlyOpenEditorRowIndex = fTRACadenaTraducidaIndexNumber();
                if ( unCurrentlyOpenEditorRowIndex) {
                    fTRA_FromEditorToDatosEnFila();                
                    if ( fTRA_HayCambiosPendientesFilaNumero( unCurrentlyOpenEditorRowIndex)) {  
                        if ( fAsynchronousTranslationMode()) {
                        
                            fTRASubmitCadenaTraducida_Async(            unCurrentlyOpenEditorRowIndex);
                        }
                    }
                }
                

                if ( fTRABatchStatusChanges()) {
                    fTRARecordBatchStatusChange( unEditorIndex, theNewTranslationStatus)
                }
                else {
                    if ( fAsynchronousTranslationMode()) {                
                        fTRA_SetBGColorEnCadenaTraducidaFilaNumero( unEditorIndex, cTRABGColor_Translation_ChangedStatus);  
                        fTRA_SetBGColorEnBotonEstadoFilaNumero(     unEditorIndex, theNewTranslationStatus, cTRABGColor_Translation_ChangedStatus);  
            
                        fTRASubmitStatusChange_Async( unEditorIndex, theNewTranslationStatus);
                    }
                    else {
                        pTRASetSimboloCadenaATraducirYEditorIndexAFilaNumero( unEditorIndex);
                        fTRASubmitStatusChange_Sync( theNewTranslationStatus);
                    }
                }
                
            }
            catch( unaException) {
                throw unaException;
            }
        }
        finally {
            pTRAEnableElementWithId( 'TRAStatusChangeButton_' + unEditorIndex + '_' + theNewTranslationStatus);
        }
    }
    finally {
        gUserInterfaceInTransition = false;
        pLogUserInterfaceEvent_END( 'fTRAEvtHlr_Editor_Button_StatusChange_OnMouseUp', 'editorIndex:' + theEditorIndex + ' newStatus:' + theNewTranslationStatus);
    }
}




function fTRAEvtHlr_BatchStatusChange_Apply_Button_OnMouseUp() {

    try {
        pLogUserInterfaceEvent_BEGIN( 'fTRAEvtHlr_BatchStatusChange_Apply_Button_OnMouseUp', '' );
        
        if ( gUserInterfaceInTransition) {
            pLogUserInterfaceEvent_IGNORED( 'fTRAEvtHlr_BatchStatusChange_Apply_Button_OnMouseUp',  '');
            return false;
        }

        var unAvoidConfirmation  = fTRA_GetConstantValue( 'cTRAId_ToAvoidConfirmationDialogsCheckDoNotConfirmOptionMsg');
        var unConfirmBatchMsg    = fTRA_GetConstantValue( 'cTRAId_ConfirmBatchMsg');
        var unConfirmed          = window.confirm( unConfirmBatchMsg + '?\n' + unAvoidConfirmation);
        if (! unConfirmed) {
            return false;
        }
    
        var unReallyConfirmBatchMsg = fTRA_GetConstantValue( 'cTRAId_ReallyConfirmBatchMsg');
        unConfirmed = window.confirm( unReallyConfirmBatchMsg + '?\n' + unAvoidConfirmation);
        if (! unConfirmed) {
            return false;
        }           
        
        gUserInterfaceInTransition = true;

        
        try {
            pTRADisableElementWithId( 'TRABatchStatusChange_Apply_Button');
            try {
                fTRASubmitBatchStatusChanges_Sync();
            }
            catch( unaException) {
                throw unaException;
            }
        }
        finally {
            pTRAEnableElementWithId( 'TRABatchStatusChange_Apply_Button');
        }
    }
    finally {
        gUserInterfaceInTransition = false;
        pLogUserInterfaceEvent_END( 'fTRAEvtHlr_BatchStatusChange_Apply_Button_OnMouseUp', '');
    }
}





function fTRAEvtHlr_Row_OnClick( theEditorIndex) {
   try {
        pLogUserInterfaceEvent_BEGIN( 'fTRAEvtHlr_Row_OnClick', 'editorIndex:' + theEditorIndex);
        
        if ( gUserInterfaceInTransition) {
            pLogUserInterfaceEvent_IGNORED( 'fTRAEvtHlr_Row_OnClick', 'editorIndex:' + theEditorIndex);
            return false;
        }
        gUserInterfaceInTransition = true;
        
        var unEditorIndex       = '' + theEditorIndex;
        var unEditorIndexNumber = parseInt( unEditorIndex);
        var unCurrentEditorIndex = fTRACurrentEditorIndexInt();
        if ( unCurrentEditorIndex && ( unCurrentEditorIndex == unEditorIndexNumber)) {
            return false;        
        }
        
        try {

            pTRAAbrirEditorEnFilaNumero( theEditorIndex);
        }
        catch( unaException) {
            throw unaException;
        }
    }
    finally {
        gUserInterfaceInTransition = false;
        pLogUserInterfaceEvent_END( 'fTRAEvtHlr_Row_OnClick', 'editorIndex:' + theEditorIndex);
    }
}



function pTRAShowOrHideModulesEditor( ) {

    var unElementModulesEditor = document.getElementById( 'cid_TRAEditorDetalle_Modulos');
    if ( !unElementModulesEditor) {
        return false;
    }

    if ( fTRAIsVisibleElement( unElementModulesEditor)) {
    
        pTRAOcultarModulesEditor();    
    }
    else {
    
        pTRAMostrarModulesEditor( unElementModulesEditor);    
    }
}




function pTRAMostrarModulesEditor( theElementModulesEditor) {

    if ( !theElementModulesEditor) {
        return false;
    }
    
    try {

        pLogUserInterfaceEvent_BEGIN( '        ->pTRAMostrarModulesEditor', '');

        pTRASetModulesEditorValues();
        
        pTRAShowElement( theElementModulesEditor);
        
    }
    finally {
        pLogUserInterfaceEvent_END( '        ->pTRAMostrarModulesEditor', '');
    }         
}




function pTRAOcultarModulesEditor( ) {

   try {

        pLogUserInterfaceEvent_BEGIN( '        ->pTRAOcultarModulesEditor', '');

        
        /* get modules editor */
        var unElementModulesEditor = document.getElementById( 'cid_TRAEditorDetalle_Modulos');
        if ( !unElementModulesEditor) {
            return false;
        }
        
        var unEditModulesButton = document.getElementById( 'TRAEditModulesButton');
        if ( unEditModulesButton) {
            var unModulesEditorOpenMsg = fTRA_GetConstantValue( 'cTRAId_ModulesEditor_Open');
            unEditModulesButton.value = unModulesEditorOpenMsg
        }
        
        pTRAHideElement( unElementModulesEditor);
    }
    finally {
        pLogUserInterfaceEvent_END( '        ->pTRAOcultarModulesEditor', '');
    }         
}





function pTRASetModulesEditorValues( ) {

   try {

        pLogUserInterfaceEvent_BEGIN( '        ->pTRASetModulesEditorValues', '');

        var unElementoCadenaTraducidaIndex = fTRACadenaTraducidaIndexNumber()
        if ( !unElementoCadenaTraducidaIndex) {
            return false;
        }
                
        /* get modules editor */
        var unElementModulesEditor = document.getElementById( 'cid_TRAEditorDetalle_Modulos');
        if ( !unElementModulesEditor) {
            return false;
        }

    
        /* get data in the translation to edit */
        var unosDatosEnFila = fTRA_GetDatosEnFilaNumero( unElementoCadenaTraducidaIndex);
        if ( !unosDatosEnFila) {
            return false;
        }
    
    
        var unAllowRemoveStringsModules = fTRA_GetConstantValue( 'cTRAId_AllowRemoveStringsModules');

        
        /* retrieve value for string modules */           
        var unosNombresModulosString = fTRA_FieldDatosEnFila( unosDatosEnFila, 'nombresModulos')[ 1];
        var unosNombresModulos       = unosNombresModulosString.split( ' ');
        
        var aAnyModulesAvailableForEdition = false;
        
        /* select check boxes for string modules */
        for ( var unIndexModulo=0; unIndexModulo < 1000; unIndexModulo++) {
        
            var unElementModulo = document.getElementById( 'cid_TRAEditorDetalle_Modulos_' + unIndexModulo);
            if ( !unElementModulo) {
                break;
            }
            var unValorElementModulo = unElementModulo.value;
            var unIndexValorModuloInNombresModulos = unosNombresModulos.indexOf( unValorElementModulo);
            
            if ( unIndexValorModuloInNombresModulos >= 0 ) {
            
                unElementModulo.checked = 1;
                
                if ( unAllowRemoveStringsModules) {
                    pTRAEnableElement( unElementModulo);
                    
                    aAnyModulesAvailableForEdition = true;
                }
                else {
                    pTRADisableElement( unElementModulo);
                }
            }
            else {
            
                unElementModulo.checked = 0;       
                
                pTRAEnableElement( unElementModulo);
                
                aAnyModulesAvailableForEdition = true;
            }
            
        }
        
        
        
        var unEditModulesButton = document.getElementById( 'TRAEditModulesButton');
        if ( unEditModulesButton) {
            var unModulesEditorCloseMsg = fTRA_GetConstantValue( 'cTRAId_ModulesEditor_Close');
            unEditModulesButton.value = unModulesEditorCloseMsg;
        }
        
        if ( aAnyModulesAvailableForEdition) {
            pTRAShowElementWithId( 'TRAEditModulesSaveButton')
        }
        else {
            pTRAHideElementWithId( 'TRAEditModulesSaveButton')
        }
                
        fTRA_SetBGColorEnModulesEditor( "white")
    }
    finally {
        pLogUserInterfaceEvent_END( '        ->pTRASetModulesEditorValues', '');
    }         
}






function fTRAAnyModulesAvailableForEdition( ) {

    var unElementoCadenaTraducidaIndex = fTRACadenaTraducidaIndexNumber()
    if ( !unElementoCadenaTraducidaIndex) {
        return false;
    }
            
    /* get modules editor */
    var unElementModulesEditor = document.getElementById( 'cid_TRAEditorDetalle_Modulos');
    if ( !unElementModulesEditor) {
        return false;
    }


    /* get data in the translation to edit */
    var unosDatosEnFila = fTRA_GetDatosEnFilaNumero( unElementoCadenaTraducidaIndex);
    if ( !unosDatosEnFila) {
        return false;
    }


    var unAllowRemoveStringsModules = fTRA_GetConstantValue( 'cTRAId_AllowRemoveStringsModules');

    var aAnyModulesAvailableForEdition = false;
    
    
    /* retrieve value for string modules */           
    var unosNombresModulosString = fTRA_FieldDatosEnFila( unosDatosEnFila, 'nombresModulos')[ 1];
    var unosNombresModulos       = unosNombresModulosString.split( ' ');
    
    /* select check boxes for string modules */
    for ( var unIndexModulo=0; unIndexModulo < 1000; unIndexModulo++) {
    
        var unElementModulo = document.getElementById( 'cid_TRAEditorDetalle_Modulos_' + unIndexModulo);
        if ( !unElementModulo) {
            break;
        }
        var unValorElementModulo = unElementModulo.value;
        var unIndexValorModuloInNombresModulos = unosNombresModulos.indexOf( unValorElementModulo);
        
        if ( unIndexValorModuloInNombresModulos >= 0) {
        
            if ( unAllowRemoveStringsModules) {
                aAnyModulesAvailableForEdition = true;
                break;
            }
        }
        else {
            aAnyModulesAvailableForEdition = true;
            break;
        }
    }
    
    return aAnyModulesAvailableForEdition;

}






function fTRAEvtHlr_Editor_Button_EditModules_OnMouseUp() {

    try {
        if ( gUserInterfaceInTransition) {
            pLogUserInterfaceEvent_IGNORED( 'fTRAEvtHlr_Editor_Button_EditModules_OnMouseUp', '');
            return false;
        }
        gUserInterfaceInTransition = true;

        pLogUserInterfaceEvent_BEGIN( 'fTRAEvtHlr_Editor_Button_EditModules_OnMouseUp', '');
        
        try {
                
            pTRADisableElementWithId( 'TRAEditModulesButton');

            try {
                pTRAShowOrHideModulesEditor();                
            }
            catch( unaException) {
                throw unaException;
            }
        }
        finally {
            pTRAEnableElementWithId( 'TRAEditModulesButton');
        }
    }
    finally {
        gUserInterfaceInTransition = false;
        pLogUserInterfaceEvent_END( 'fTRAEvtHlr_Editor_Button_EditModules_OnMouseUp', '');
    }
}





function fTRAEvtHlr_Editor_Button_EditModules_OnKeyPress( event) {

    try {
        pLogUserInterfaceEvent_BEGIN( 'fTRAEvtHlr_Editor_Button_EditModules_OnKeyPress', '');
        
        if ( gUserInterfaceInTransition) {
            pLogUserInterfaceEvent_IGNORED( 'fTRAEvtHlr_Editor_Button_EditModules_OnKeyPress', '');
            return false;
        }
        gUserInterfaceInTransition = true;

        if ( !event) {
            return false;
        }
        try {
    
            pTRADisableElementWithId( 'TRAEditModulesButton');

            try {            
                
                var unKeyNumber = fTRAKeyNumberFromEvent( event);
                
                pLogUserInterfaceEvent( 'fTRAEvtHlr_Editor_Button_EditModules_OnKeyPress', 'keyNumber: ' + unKeyNumber);
                
                if ( unKeyNumber == cKeyNumberCR) {
                    try {
                        pTRAShowOrHideModulesEditor();                
                    }
                    catch( unaException) {
                        throw unaException;
                    }
                        
                    return false;
                }
                else {
                    return true;
                }
            }
            catch( unaException) {
                throw unaException;
            }
        }
        finally {
            pTRAEnableElementWithId( 'TRAEditModulesButton');
        }
    }
    finally {
        gUserInterfaceInTransition = false;
        pLogUserInterfaceEvent_END( 'fTRAEvtHlr_Editor_Button_EditModules_OnKeyPress', '');
    }
}











function fTRAEvtHlr_Editor_Button_SaveModules_OnMouseUp() {

    try {
        pLogUserInterfaceEvent_BEGIN( 'fTRAEvtHlr_Editor_Button_SaveModules_OnMouseUp', '');

        if ( gUserInterfaceInTransition) {
            pLogUserInterfaceEvent_IGNORED( 'fTRAEvtHlr_Editor_Button_SaveModules_OnMouseUp', '');
            return false;
        }
        gUserInterfaceInTransition = true;

        try {
            pTRADisableElementWithId( 'TRAEditModulesSaveButton');

            try {
                            
                var unEditorRowIndex =  fTRACadenaTraducidaIndexNumber();
                if ( unEditorRowIndex) {                
                    
                    fTRA_SetBGColorEnModulesEditor( cTRABGColor_Translation_ChangedStatus);
                    
                    if ( fAsynchronousTranslationMode()) {
                            
                        fTRASubmitStringModulesChange_Async( unEditorRowIndex);
                     }
                    else {
                        fTRASubmitStringModulesChange_Sync( );
                    }
                }
            }
            catch( unaException) {
                throw unaException;
            }
        }
        finally {
            pTRAEnableElementWithId( 'TRAEditModulesSaveButton');
        }
    }
    finally {
        gUserInterfaceInTransition = false;
        pLogUserInterfaceEvent_END( 'fTRAEvtHlr_Editor_Button_SaveModules_OnMouseUp', '');
    }
}





function fTRAEvtHlr_Editor_Button_SaveModules_OnKeyPress( event) {

    try {
        pLogUserInterfaceEvent_BEGIN( 'fTRAEvtHlr_Editor_Button_SaveModules_OnKeyPress', '');
        
        if ( gUserInterfaceInTransition) {
            pLogUserInterfaceEvent_IGNORED( 'fTRAEvtHlr_Editor_Button_SaveModules_OnKeyPress', '');
            return false;
        }
        gUserInterfaceInTransition = true;

        if ( !event) {
            return false;
        }
        try {
    
            pTRADisableElementWithId( 'TRAEditModulesSaveButton');

            try {
            
                var unKeyNumber = fTRAKeyNumberFromEvent( event);
                    
                pLogUserInterfaceEvent( 'fTRAEvtHlr_Editor_Button_Pendiente_OnKeyPress', 'key:' + unKeyNumber);
                
                if ( unKeyNumber == cKeyNumberCR) {
                
                    var unEditorRowIndex =  fTRACadenaTraducidaIndexNumber();
                    if ( unEditorRowIndex) {
                    
                        fTRA_SetBGColorEnModulesEditor( cTRABGColor_Translation_ChangedStatus);
                    
                        if ( fAsynchronousTranslationMode()) {
                                
                            fTRASubmitStringModulesChange_Async( unEditorRowIndex);
                         }
                        else {
                            fTRASubmitStringModulesChange_Sync( );
                        }

                    }
                    return false;
                }
                else {
                    return true;
                }
            }
            catch( unaException) {
                throw unaException;
            }
        }
        finally {
            pTRAEnableElementWithId( 'TRAEditModulesSaveButton');
        }
    }
    finally {
        gUserInterfaceInTransition = false;
        pLogUserInterfaceEvent_END( 'fTRAEvtHlr_Editor_Button_SaveModules_OnKeyPress', '');
    }
}










function fTRAEvtHlr_Window_OnLoad( event) {
}






function fSetFocusToEditorTextArea( ) {

    pLogUserInterfaceEvent( '      -> fSetFocusToEditorTextArea', '');

    var unEditorTextArea = document.getElementById( 'theCadenaTraducida');
    if ( !unEditorTextArea) {
        return false;
    }
    
    pTRAEnableElement( unEditorTextArea);
    if ( fTRAIsVisibleElement( unEditorTextArea)) {
        unEditorTextArea.focus();
    }
    /* unEditorTextArea.select(); */
     
}



function fTRACurrentEditorIndexInt() {
    var unElementoCadenaTraducidaIndex = document.getElementById( 'theCadenaTraducida_index');
    if ( !unElementoCadenaTraducidaIndex) {
        return 0;
    }
    var unCurrentEditorIndex = unElementoCadenaTraducidaIndex.value ; 
    unCurrentEditorIndex = '' + unCurrentEditorIndex;
    var unCurrentEditorIndexNumber = parseInt( unCurrentEditorIndex);

    return unCurrentEditorIndexNumber;
}





function pTRAResetCurrentEditorIndex() {
    var unElementoCadenaTraducidaIndex = document.getElementById( 'theCadenaTraducida_index');
    if ( !unElementoCadenaTraducidaIndex) {
        return false;
    }
    unElementoCadenaTraducidaIndex.value = 0 ; 
    return true;
}




function pTRAShutdownEditor() {

    pLogUserInterfaceEvent( '      -> pTRAShutdownEditor', '');

    pTRAHideElementWithId(      'cid_TRAEditorAreaYBotones');
    
    var unElementoCadenaTraducidaIndex = document.getElementById( 'theCadenaTraducida_index');
    if ( !unElementoCadenaTraducidaIndex) {
        return false;
    }
    
    var unCurrentEditorIndex = unElementoCadenaTraducidaIndex.value ; 
    unCurrentEditorIndex = '' + unCurrentEditorIndex;
    unCurrentEditorIndexNumber = parseInt( unCurrentEditorIndex);
    if ( !unCurrentEditorIndexNumber) {
        pLogUserInterfaceEvent( '      -> pTRAShutdownEditor', ' editorIndex: unknown');
        return false;
    }
    
    pLogUserInterfaceEvent( '      -> pTRAShutdownEditor', ' editorIndex:' + unCurrentEditorIndexNumber);

    
    pTRAHideElementWithId(      'theCadenaTraducida');
    pTRADisableElementWithId(   'theCadenaTraducida');
    pTRAHideElementWithId(      'TRAStatusChangeButton_Traducir');
    pTRAHideElementWithId(      'TRAStatusChangeButton_Traducir_Icon');
    pTRADisableElementWithId(   'TRAStatusChangeButton_Traducir');
    pTRADisableElementWithId(   'TRAStatusChangeButton_Traducir_Icon');
    pTRAHideElementWithId(      'TRAStatusChangeButton_Pendiente');
    pTRAHideElementWithId(      'TRAStatusChangeButton_Pendiente_Icon');
    pTRADisableElementWithId(   'TRAStatusChangeButton_Pendiente');
    pTRADisableElementWithId(   'TRAStatusChangeButton_Pendiente_Icon');
    
    pTRAHideElementWithId(      'cid_TRAEditorDetalle');

    var unElementoSimboloCadenaATraducir = document.getElementById( 'theSimboloCadenaATraducir');
    if ( unElementoSimboloCadenaATraducir) {
        unElementoSimboloCadenaATraducir.value          = '';
        unElementoSimboloCadenaATraducir.defaultValue   = '';
    }
    
    var unElementoCadenaTraducida = document.getElementById( 'theCadenaTraducida');
    if ( unElementoCadenaTraducida) {
        unElementoSimboloCadenaATraducir.value          = '';
        unElementoSimboloCadenaATraducir.defaultValue   = '';
    }
    
    var unElementoNuevoEstadoTraduccion = document.getElementById( 'theNuevoEstadoTraduccion');
    if ( unElementoNuevoEstadoTraduccion) {
        unElementoNuevoEstadoTraduccion.value			= '';
        unElementoNuevoEstadoTraduccion.defaultValue	= '';
    }
}
    






function fTRACadenaTraducidaIndexNumber() {

    var unElementoCadenaTraducidaIndex = document.getElementById( 'theCadenaTraducida_index');
    if ( !unElementoCadenaTraducidaIndex) {
        return 0;
    }

    var unCadenaTraducidaIndex = unElementoCadenaTraducidaIndex.value;
    unCadenaTraducidaIndex = '' + unCadenaTraducidaIndex;
    if ( (! (unCadenaTraducidaIndex.length)) || ( unCadenaTraducidaIndex.length < 1) || ( unCadenaTraducidaIndex == '-1')) {
        return 0;
    }
    return parseInt( unCadenaTraducidaIndex);
}



function pTRASetCadenaTraducidaIndexNumber( theEditorIndex) {
    if ( !theEditorIndex) {
        return false;
    }

    var unElementoCadenaTraducidaIndex = document.getElementById( 'theCadenaTraducida_index');
    if ( !unElementoCadenaTraducidaIndex) {
        return false;
    }

    var unCadenaTraducidaIndex = '' + theEditorIndex;
    
    unElementoCadenaTraducidaIndex.value = unCadenaTraducidaIndex;
    
    return true;
}


function fTRA_ResetCambiosPendientesFilaNumero( theEditorIndex) {
    if ( !theEditorIndex) {
        return false;
    }
    
    var unEditorIndex = '' + theEditorIndex;
    if ( ! unEditorIndex.length) {
        return false;
    }
     
    unEditorIndex = parseInt( unEditorIndex);
    
    unEditorIndex = '' + theEditorIndex;
    if ( !unEditorIndex) {
        return false;
    }
    
   /* get data in the translation to edit */
    var unosDatosEnFila = fTRA_GetDatosEnFilaNumero( unEditorIndex);
    if ( !unosDatosEnFila) {
        return false;
    }

    var unValorCadenaTraducida      = fTRA_FieldDatosEnFila( unosDatosEnFila, 'cadenaTraducida')[ 1];
    
    fTRA_SetPropiedadEnFilaNumero( unEditorIndex, 'cadenaTraducida_NewValue', unValorCadenaTraducida);
    fTRA_SetPropiedadEnFilaNumero( unEditorIndex, 'cadenaTraducidaDisplay',   unValorCadenaTraducida);

    fTRA_SetBGColorEnCadenaTraducidaFilaNumero( unEditorIndex, 'white');  
    
    return true;
}




function fTRA_HayCambiosPendientesFilaNumero( theEditorIndex) {
    if ( !theEditorIndex) {
        return false;
    }
    
    unEditorIndex = '' + theEditorIndex;
    if ( ! unEditorIndex.length) {
        return false;
    }
     
    var unEditorIndex = parseInt( unEditorIndex);
    
    unEditorIndex = '' + theEditorIndex;
    if ( !unEditorIndex) {
        return false;
    }
    
   /* get data in the translation to edit */
    var unosDatosEnFila = fTRA_GetDatosEnFilaNumero( unEditorIndex);
    if ( !unosDatosEnFila) {
        return false;
    }
    
    var unValorCadenaTraducida      = fTRA_FieldDatosEnFila( unosDatosEnFila, 'cadenaTraducida')[ 1];
    var unNuevoValorCadenaTraducida = fTRA_FieldDatosEnFila( unosDatosEnFila, 'cadenaTraducida_NewValue')[ 1];
    
    if ( unNuevoValorCadenaTraducida == unValorCadenaTraducida) {
        return false;
    }
    
    if ( !unNuevoValorCadenaTraducida.length) {
        return false;
    }
    
    return true;
}








function fTRA_UpdateSavedCadenaTraducidaFilaNumero( theEditorIndex) {
    if ( !theEditorIndex) {
        return false;
    }
    
    unEditorIndex = '' + theEditorIndex;
    if ( ! unEditorIndex.length) {
        return false;
    }
     
    var unEditorIndex = parseInt( unEditorIndex);
    
    unEditorIndex = '' + theEditorIndex;
    if ( !unEditorIndex) {
        return false;
    }
    
    var unElementoCadenaTraducida = document.getElementById( 'theCadenaTraducida');
    if ( !unElementoCadenaTraducida) {
        return false;
    }

   /* get data in the translation to edit */
    var unosDatosEnFila = fTRA_GetDatosEnFilaNumero( unEditorIndex);
    if ( !unosDatosEnFila) {
        return false;
    }
    
    var unNuevoValorCadenaTraducida = fTRA_FieldDatosEnFila( unosDatosEnFila, 'cadenaTraducida_NewValue')[ 1];

    fTRA_SetPropiedadEnFilaNumero( unEditorIndex, 'cadenaTraducida', unNuevoValorCadenaTraducida);
   
    return true;
}





function fTRA_DeleteSavedAndNewCadenaTraducidaFilaNumero( theEditorIndex) {
    if ( !theEditorIndex) {
        return false;
    }
    
    var unEditorIndex = '' + theEditorIndex;
    if ( ! unEditorIndex.length) {
        return false;
    }
     
    unEditorIndex = parseInt( unEditorIndex);
    
    unEditorIndex = '' + theEditorIndex;
    if ( !unEditorIndex) {
        return false;
    }
    
    var unElementoCadenaTraducida = document.getElementById( 'theCadenaTraducida');
    if ( !unElementoCadenaTraducida) {
        return false;
    }

   /* get data in the translation to edit */
    var unosDatosEnFila = fTRA_GetDatosEnFilaNumero( unEditorIndex);
    if ( !unosDatosEnFila) {
        return false;
    }
    
    fTRA_SetPropiedadEnFilaNumero( unEditorIndex, 'cadenaTraducida', '');
    fTRA_SetPropiedadEnFilaNumero( unEditorIndex, 'cadenaTraducida_NewValue', '');
    fTRA_SetPropiedadEnFilaNumero( unEditorIndex, 'cadenaTraducidaDisplay', '');
   
    return true;
}






function fTRA_ResetValorTextAreaFilaNumero( theEditorIndex) {
    if ( !theEditorIndex) {
        return false;
    }
    
    unEditorIndex = '' + theEditorIndex;
    if ( ! unEditorIndex.length) {
        return false;
    }
     
    var unEditorIndex = parseInt( unEditorIndex);
    
    unEditorIndex = '' + theEditorIndex;
    if ( !unEditorIndex) {
        return false;
    }
    
    var unElementoCadenaTraducida = document.getElementById( 'theCadenaTraducida');
    if ( !unElementoCadenaTraducida) {
        return false;
    }

   /* get data in the translation to edit */
    var unosDatosEnFila = fTRA_GetDatosEnFilaNumero( unEditorIndex);
    if ( !unosDatosEnFila) {
        return false;
    }
    
    var unValorCadenaTraducida = fTRA_FieldDatosEnFila( unosDatosEnFila, 'cadenaTraducida_NewValue')[ 1];
    
    unElementoCadenaTraducida.value         = unValorCadenaTraducida;
    unElementoCadenaTraducida.defaultValue  = unValorCadenaTraducida;
    
    return true;
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
    If the editor was in a row,
        and if there is data in the editor
        and the data is different from the stored in the row
    then return the index of the row containing the editor (which is always > 0),
    else return 0
    
*/
function fTRA_FromEditorToDatosEnFila() {


    var unCadenaTraducidaIndex = fTRACadenaTraducidaIndexNumber();
    if ( !unCadenaTraducidaIndex) {
        pLogUserInterfaceEvent( '         ->fTRA_FromEditorToDatosEnFila', 'failed: no unCadenaTraducidaIndex');
        return 0;
    }

    /* get data in the translation to edit */
    var unosDatosEnFila = fTRA_GetDatosEnFilaNumero( unCadenaTraducidaIndex);
    if ( !unosDatosEnFila) {
        pLogUserInterfaceEvent( '         ->fTRA_FromEditorToDatosEnFila', 'failed: no unosDatosEnFila');
        return 0;
    }

    var unElementoCadenaTraducida = document.getElementById( 'theCadenaTraducida');
    if ( !unElementoCadenaTraducida) {
        pLogUserInterfaceEvent( '         ->fTRA_FromEditorToDatosEnFila', 'failed: no unElementoCadenaTraducida');
        return 0;
    }

    var unNuevoValorCadenaTraducida = unElementoCadenaTraducida.value;
    if ( !unNuevoValorCadenaTraducida.length) {
        pLogUserInterfaceEvent( '         ->fTRA_FromEditorToDatosEnFila', 'ignored: empty new value');
        return 0;
    }
    unNuevoValorCadenaTraducida = fTRAStringStrip( unNuevoValorCadenaTraducida);
    if ( !unNuevoValorCadenaTraducida.length) {
        pLogUserInterfaceEvent( '         ->fTRA_FromEditorToDatosEnFila', 'ignored: empty new value');
        return 0;
    }

    var unFieldCadenaTraducidaNewValue	= fTRA_FieldDatosEnFila( unosDatosEnFila, 'cadenaTraducida_NewValue');
    var unValorCadenaTraducida	        = unFieldCadenaTraducidaNewValue[ 1];

    if ( unNuevoValorCadenaTraducida == unValorCadenaTraducida) {
        pLogUserInterfaceEvent( '         ->fTRA_FromEditorToDatosEnFila', 'ignored: same new value');
        return 0;
    }
    
    fTRA_SetPropiedadEnFilaNumero( unCadenaTraducidaIndex, 'cadenaTraducida_NewValue', unNuevoValorCadenaTraducida);
    fTRA_SetPropiedadEnFilaNumero( unCadenaTraducidaIndex, 'cadenaTraducidaDisplay',   unNuevoValorCadenaTraducida);

    fTRA_SetBGColorEnCadenaTraducidaFilaNumero( unCadenaTraducidaIndex, cTRABGColor_Translation_ChangedTranslation);  
    
    pLogUserInterfaceEvent( '         ->fTRA_FromEditorToDatosEnFila', 'stored_value=' + unNuevoValorCadenaTraducida);
    
    return parseInt( unCadenaTraducidaIndex);
}








/* #################################################################
    Submit function with Asynch request response without page reload

*/
function fTRASubmitCadenaTraducida_Async( theCadenaTraducidaIndex) {  

   try {

        pLogUserInterfaceEvent_BEGIN( '        ->fTRASubmitCadenaTraducida_Async', 'editorIndex: ' + theCadenaTraducidaIndex);
        
        if ( !theCadenaTraducidaIndex) {
            return false;
        }
        
    
        var unElementoCodigoIdiomaCursor        = document.getElementById( 'theCodigoIdiomaCursor');
        if ( !unElementoCodigoIdiomaCursor) {
            return false;
        }
        unCodigoIdiomaCursor = unElementoCodigoIdiomaCursor.value;
        if ( !unCodigoIdiomaCursor.length) {
            return false;
        }
    
    
        /* get data in the translation to edit */
        var unosDatosEnFila = fTRA_GetDatosEnFilaNumero( theCadenaTraducidaIndex);
        if ( !unosDatosEnFila) {
            return false;
        }
    
        var unFieldSimboloCadena	    = fTRA_FieldDatosEnFila( unosDatosEnFila, 'simboloCadena');
        if ( !unFieldSimboloCadena) {
            return false;
        }
        var unSimboloCadenaATraducir = unFieldSimboloCadena[ 1];
        if ( !unSimboloCadenaATraducir) {
            return false;
        }
    
        var unFieldNuevaCadenaTraducida		= fTRA_FieldDatosEnFila( unosDatosEnFila, 'cadenaTraducida_NewValue');
        if ( !unFieldNuevaCadenaTraducida) {
            return false;
        }
        var unNuevoValorCadenaTraducida	= unFieldNuevaCadenaTraducida[ 1];
        if (!unNuevoValorCadenaTraducida) {
            return false;
        }
     
        var unFieldContadorCambios		= fTRA_FieldDatosEnFila( unosDatosEnFila, 'contadorCambios');
        if ( !unFieldContadorCambios) {
            return false;
        }
        var unContadorCambios	= unFieldContadorCambios[ 1];
        if (!unContadorCambios) {
            return false;
        }
     
        fTRA_SetContenidoTextoElementoWithId( 'cid_TRAInteractionMessage_' + theCadenaTraducidaIndex, fTRAMsg( 'AsyncPhase_RequestQueued'));        
        pTRAShowElementWithId(  'cid_TRAInteractionMessageHolder_' + theCadenaTraducidaIndex);
        
        pLogUserInterfaceEvent( '            ->fTRASubmitCadenaTraducida_Async', 'editorIndex: ' + theCadenaTraducidaIndex + ' QUEUED');
        pTRAAsyncRequest_Service_TranslationChange_Send( unCodigoIdiomaCursor, unSimboloCadenaATraducir, unNuevoValorCadenaTraducida, unContadorCambios, theCadenaTraducidaIndex);
    
        return true;
    }
    finally {
        pLogUserInterfaceEvent_END( '        ->fTRASubmitCadenaTraducida_Async', 'editorIndex: ' + theCadenaTraducidaIndex);
    }    
}




function fTRASubmitStatusChange_Async( theCadenaTraducidaIndex, theNewTranslationStatus) {  

    try {

        pLogUserInterfaceEvent_BEGIN( '        ->fTRASubmitStatusChange_Async', 'editorIndex: ' + theCadenaTraducidaIndex + ' theNewTranslationStatus: ' + theNewTranslationStatus);

        if ( !theNewTranslationStatus) {
            return false;
        }
    
        var unElementoCodigoIdiomaCursor        = document.getElementById( 'theCodigoIdiomaCursor');
        if ( !unElementoCodigoIdiomaCursor) {
            return false;
        }
        var unCodigoIdiomaCursor = unElementoCodigoIdiomaCursor.value;
        if ( !unCodigoIdiomaCursor.length) {
            return false;
        }
    
    
        /* get data in the translation to edit */
        var unosDatosEnFila = fTRA_GetDatosEnFilaNumero( theCadenaTraducidaIndex);
        if ( !unosDatosEnFila) {
            return false;
        }
    
        var unFieldSimboloCadena	    = fTRA_FieldDatosEnFila( unosDatosEnFila, 'simboloCadena');
        if ( !unFieldSimboloCadena) {
            return false;
        }
        var unSimboloCadenaATraducir = unFieldSimboloCadena[ 1];
        if ( !unSimboloCadenaATraducir) {
            return false;
        }
    
        var unFieldContadorCambios		= fTRA_FieldDatosEnFila( unosDatosEnFila, 'contadorCambios');
        if ( !unFieldContadorCambios) {
            return false;
        }
        var unContadorCambios	= unFieldContadorCambios[ 1];
        if (!unContadorCambios) {
            return false;
        }
        
        fTRA_SetContenidoTextoElementoWithId( 'cid_TRAInteractionMessage_' + theCadenaTraducidaIndex, fTRAMsg( 'AsyncPhase_RequestQueued'));        
        pTRAShowElementWithId(  'cid_TRAInteractionMessageHolder_' + theCadenaTraducidaIndex);
        
        pLogUserInterfaceEvent( '            ->fTRASubmitStatusChange_Async', 'editorIndex: ' + theCadenaTraducidaIndex + ' theNewTranslationStatus: ' + theNewTranslationStatus + ' SENDING');
        pTRAAsyncRequest_Service_StatusChange_Send( unCodigoIdiomaCursor, unSimboloCadenaATraducir, theNewTranslationStatus, unContadorCambios, theCadenaTraducidaIndex);
    
        return true;
    }
    finally {
        pLogUserInterfaceEvent_END( '        ->fTRASubmitStatusChange_Async', 'editorIndex: ' + theCadenaTraducidaIndex + 'theNewTranslationStatus: ' + theNewTranslationStatus);
    }    
}




function fTRASubmitInvalidateStringTranslations_Async( theCadenaTraducidaIndex) {  
    /* ACV 20090927 Error Does not refresh properly because the response is not structured as expected
     Known limitation: Invalidate in Synch Mode
     */

    try {

        pLogUserInterfaceEvent_BEGIN( '        ->fTRASubmitInvalidateStringTranslations_Async', 'editorIndex: ' + theCadenaTraducidaIndex);

        var unElementoCodigoIdiomaCursor        = document.getElementById( 'theCodigoIdiomaCursor');
        if ( !unElementoCodigoIdiomaCursor) {
            return false;
        }
        var unCodigoIdiomaCursor = unElementoCodigoIdiomaCursor.value;
        if ( !unCodigoIdiomaCursor.length) {
            return false;
        }
        
        /* get data in the translation to edit */
        var unosDatosEnFila = fTRA_GetDatosEnFilaNumero( theCadenaTraducidaIndex);
        if ( !unosDatosEnFila) {
            return false;
        }
    
        var unFieldSimboloCadena	    = fTRA_FieldDatosEnFila( unosDatosEnFila, 'simboloCadena');
        if ( !unFieldSimboloCadena) {
            return false;
        }
        var unSimboloCadenaATraducir = unFieldSimboloCadena[ 1];
        if ( !unSimboloCadenaATraducir) {
            return false;
        }
        
        fTRA_SetContenidoTextoElementoWithId( 'cid_TRAInteractionMessage_' + theCadenaTraducidaIndex, fTRAMsg( 'AsyncPhase_RequestQueued'));        
        pTRAShowElementWithId(  'cid_TRAInteractionMessageHolder_' + theCadenaTraducidaIndex);
                
        pLogUserInterfaceEvent( '            ->fTRASubmitInvalidateStringTranslations_Async', 'editorIndex: ' + theCadenaTraducidaIndex + ' SENDING');
        pTRAAsyncRequest_Service_InvalidateStringTranslations_Send( unCodigoIdiomaCursor, unSimboloCadenaATraducir, theCadenaTraducidaIndex);
    
        return true;
    }
    finally {
        pLogUserInterfaceEvent_END( '        ->fTRASubmitInvalidateStringTranslations_Async', 'editorIndex: ' + theCadenaTraducidaIndex);
    }    
}






function fTRASubmitStringModulesChange_Async( theCadenaTraducidaIndex) {  

    try {

        pLogUserInterfaceEvent_BEGIN( '        ->fTRASubmitStringModulesChange_Async', 'editorIndex: ' + theCadenaTraducidaIndex );

    
        var unElementoCodigoIdiomaCursor        = document.getElementById( 'theCodigoIdiomaCursor');
        if ( !unElementoCodigoIdiomaCursor) {
            return false;
        }
        var unCodigoIdiomaCursor = unElementoCodigoIdiomaCursor.value;
        if ( !unCodigoIdiomaCursor.length) {
            return false;
        }
    
    
        /* get data in the translation to edit */
        var unosDatosEnFila = fTRA_GetDatosEnFilaNumero( theCadenaTraducidaIndex);
        if ( !unosDatosEnFila) {
            return false;
        }
    
        var unFieldSimboloCadena	    = fTRA_FieldDatosEnFila( unosDatosEnFila, 'simboloCadena');
        if ( !unFieldSimboloCadena) {
            return false;
        }
        var unSimboloCadenaATraducir = unFieldSimboloCadena[ 1];
        if ( !unSimboloCadenaATraducir) {
            return false;
        }
    
        var unFieldNombresModulos	    = fTRA_FieldDatosEnFila( unosDatosEnFila, 'nombresModulos');
        if ( !unFieldNombresModulos) {
            return false;
        }
        
        var unosOriginalNombresModulosString = unFieldNombresModulos[ 1];
        var unosOriginalNombresModulos       = unosOriginalNombresModulosString.split( ' ');
        
        var unosNuevosNombresModulos = '';
        var unosNombresModulosMustChange = false;
        
        /* determine new module names by checking the selection state of check boxes for string modules */
        for ( var unIndexModulo=0; unIndexModulo < 1000; unIndexModulo++) {
        
            var unElementModulo = document.getElementById( 'cid_TRAEditorDetalle_Modulos_' + unIndexModulo);
            if ( !unElementModulo) {
                break;
            }
            var unValorElementModulo = unElementModulo.value;
            
            var unIndexValorModuloInNombresModulos = unosOriginalNombresModulos.indexOf( unValorElementModulo);
            
            if ( unElementModulo.checked) {
            
                unosNuevosNombresModulos = unosNuevosNombresModulos + ' ' + unValorElementModulo;
                
                if ( unIndexValorModuloInNombresModulos < 0 ) {
                    unosNombresModulosMustChange = true;
                }
            }
            else {
            
                if ( unIndexValorModuloInNombresModulos >= 0 ) {
                    unosNombresModulosMustChange = true;
                }
            }
        }
        
         
        fTRA_SetContenidoTextoElementoWithId( 'cid_TRAInteractionMessage_' + theCadenaTraducidaIndex, fTRAMsg( 'AsyncPhase_RequestQueued'));        
        pTRAShowElementWithId(  'cid_TRAInteractionMessageHolder_' + theCadenaTraducidaIndex);
                
        pLogUserInterfaceEvent( '            ->fTRASubmitStringModulesChange_Async', 'editorIndex: ' + theCadenaTraducidaIndex  + ' SENDING');
        pTRAAsyncRequest_Service_StringModulesChange_Send( unCodigoIdiomaCursor, unSimboloCadenaATraducir, unosNuevosNombresModulos, theCadenaTraducidaIndex);
    
        return true;
    }
    finally {
        pLogUserInterfaceEvent_END( '        ->fTRASubmitStringModulesChange_Async', 'editorIndex: ' + theCadenaTraducidaIndex);
    }    
}









function fTRA_BlinkBGColorEnCadenaTraducidaFilaNumero( theTranslationRowIndex, theBGColor) {
    var unaCelda = document.getElementById( 'cid_ColumnaCadenasTraducidas_' + theTranslationRowIndex);
    if ( !unaCelda) {
        return false;
    }
    /* Firefox ok, not working in IE
     unaCelda.setAttribute( "bgcolor", theBGColor)
    */
    unPrevBGColor = unaCelda.bgColor;
    unaCelda.bgColor = '';
    setTimeout("document.getElementById( 'cid_ColumnaCadenasTraducidas_" + theTranslationRowIndex + "').bgColor = '" + theBGColor + "'",300);
    setTimeout("document.getElementById( 'cid_ColumnaCadenasTraducidas_" + theTranslationRowIndex + "').bgColor = '" + unPrevBGColor + "'",600);
    return true;
}





function fTRA_SetBGColorEnCadenaTraducidaFilaNumero( theTranslationRowIndex, theBGColor) {
    var unaCelda = document.getElementById( 'cid_ColumnaCadenasTraducidas_' + theTranslationRowIndex);
    if ( !unaCelda) {
        return false;
    }
    /* Firefox ok, not working in IE
     unaCelda.setAttribute( "bgcolor", theBGColor)
    */
    unaCelda.bgColor = theBGColor;
    return true;
}






function fTRA_SetBGColorEnModulesEditor( theBGColor) {
    var unaCelda = document.getElementById( 'cid_TRAEditorDetalle_Modulos_Editor');
    if ( !unaCelda) {
        return false;
    }
    /* Firefox ok, not working in IE
     unaCelda.setAttribute( "bgcolor", theBGColor)
    */
    unaCelda.bgColor = theBGColor;
    return true;
}




function fTRA_SetBGColorEnBotonesEstadoFilaNumero( theTranslationRowIndex, theBGColor) {
    /* Firefox ok, not working in IE
     unaCelda.setAttribute( "bgcolor", theBGColor)
    */
    var unaCeldaRevisada = document.getElementById( 'cid_ColumnaStatusChangeButton_' + theTranslationRowIndex + '_Traducida');
    if ( unaCeldaRevisada) {
        unaCeldaRevisada.bgColor = theBGColor;
    }
    else {
        return false;
    }
    var unaCeldaRevisada = document.getElementById( 'cid_ColumnaStatusChangeButton_' + theTranslationRowIndex + '_Revisada');
    if ( unaCeldaRevisada) {
        unaCeldaRevisada.bgColor = theBGColor;
    }
    else {
        return false;
    }
    var unaCeldaRevisada = document.getElementById( 'cid_ColumnaStatusChangeButton_' + theTranslationRowIndex + '_Definitiva');
    if ( unaCeldaRevisada) {
        unaCeldaRevisada.bgColor = theBGColor;
    }
    else {
        return false;
    }
    
    return true;
}


function fTRA_SetBGColorEnBotonEstadoFilaNumero( theTranslationRowIndex, theNewTranslationStatus, theBGColor) {
    /* Firefox ok, not working in IE
     unaCelda.setAttribute( "bgcolor", theBGColor)
    */
    
    if ( !theTranslationRowIndex) {
        return false;
    }
    if ( !theNewTranslationStatus) {
        return false;
    }
    
    var unaCeldaRevisada = document.getElementById( 'cid_ColumnaStatusChangeButton_' + theTranslationRowIndex + '_' + theNewTranslationStatus);
    if ( unaCeldaRevisada) {
        unaCeldaRevisada.bgColor = theBGColor;
    }
    return true;
}




function fTRAGoTo_Sync( theGoTo) {
    if ( !theGoTo) {
        return self;
    }

    try {

        pLogUserInterfaceEvent_BEGIN( 'fTRAGoTo_Sync', 'goTo: ' + theGoTo);
        
        var unElementoGoTo = document.getElementById( 'theGoTo');
        if ( !unElementoGoTo) {
            return false;
        }
        
        unElementoGoTo.value			= theGoTo;
        unElementoGoTo.defaultValue	    = theGoTo;

        var unElementoNuevoEstadoTraduccion = document.getElementById( 'theNuevoEstadoTraduccion');
        if ( unElementoNuevoEstadoTraduccion) {
            unElementoNuevoEstadoTraduccion.value			= '';
            unElementoNuevoEstadoTraduccion.defaultValue	= '';
        }
        document.forms[ 'TranslationFormId'].submit();
        return true;
    }
    finally {
        pLogUserInterfaceEvent_END( 'fTRAGoTo_Sync', 'goTo: ' + theGoTo);
    }    
}


function fTRASubmitCadenaTraducida_Sync( ) {

    try {

        pLogUserInterfaceEvent_BEGIN( '        ->fTRASubmitCadenaTraducida_Sync', '');
        
        if ( !fTRACadenaTraducidaIndexNumber()) {
            return false;
        }
        var unElementoNuevoEstadoTraduccion = document.getElementById( 'theNuevoEstadoTraduccion');
        if ( unElementoNuevoEstadoTraduccion) {
            unElementoNuevoEstadoTraduccion.value			= '';
            unElementoNuevoEstadoTraduccion.defaultValue	= '';
        }
        var unElementoGoTo = document.getElementById( 'theGoTo');
        if ( unElementoGoTo) {
            unElementoGoTo.value			= '';
            unElementoGoTo.defaultValue	    = '';
        }
        document.forms[ 'TranslationFormId'].submit();
        return true;
    }
    finally {
        pLogUserInterfaceEvent_END( '        ->fTRASubmitCadenaTraducida_Sync', '');
    }    
}



function fTRASubmitStatusChange_Sync( theNewTranslationStatus) {

    try {

        pLogUserInterfaceEvent_BEGIN( '        ->fTRASubmitStatusChange_Sync', '');
        
         if ( !theNewTranslationStatus) {
            return false;
        }
    
        if ( !fTRACadenaTraducidaIndexNumber()) {
            return false;
        }
    
        var unElementoNuevoEstadoTraduccion = document.getElementById( 'theNuevoEstadoTraduccion');
        if ( !unElementoNuevoEstadoTraduccion) {
            return false;
        }
        unElementoNuevoEstadoTraduccion.value			= theNewTranslationStatus;
        unElementoNuevoEstadoTraduccion.defaultValue	= theNewTranslationStatus;
      
        
        var unElementoCadenaTraducida = document.getElementById( 'theCadenaTraducida');
        if ( unElementoCadenaTraducida) {
            unElementoCadenaTraducida.value			= '';
            unElementoCadenaTraducida.defaultValue	= '';
        }
        var unElementoGoTo = document.getElementById( 'theGoTo');
        if ( unElementoGoTo) {
            unElementoGoTo.value			= '';
            unElementoGoTo.defaultValue	    = '';
        }
         
        document.forms[ 'TranslationFormId'].submit();
        return true;
    }
    finally {
        pLogUserInterfaceEvent_END( '        ->fTRASubmitStatusChange_Sync', '');
    }    
}




function fTRASubmitInvalidateStringTranslations_Sync( ) {

    try {

        pLogUserInterfaceEvent_BEGIN( '        ->fTRASubmitInvalidateStringTranslations_Sync', '');
        
        if ( !fTRACadenaTraducidaIndexNumber()) {
            return false;
        }
    
        var unElementoNuevoEstadoTraduccion = document.getElementById( 'theNuevoEstadoTraduccion');
        if ( !unElementoNuevoEstadoTraduccion) {
            return false;
        }
        unElementoNuevoEstadoTraduccion.value			= 'InvalidarTraduccionesCadena';
        unElementoNuevoEstadoTraduccion.defaultValue	= 'InvalidarTraduccionesCadena';
        /*
        unElementoNuevoEstadoTraduccion.value			= '';
        unElementoNuevoEstadoTraduccion.defaultValue	= '';
        */
        
        var unElementoCadenaTraducida = document.getElementById( 'theCadenaTraducida');
        if ( unElementoCadenaTraducida) {
            unElementoCadenaTraducida.value			= '';
            unElementoCadenaTraducida.defaultValue	= '';
        }
        var unElementoGoTo = document.getElementById( 'theGoTo');
        if ( unElementoGoTo) {
            unElementoGoTo.value			= '';
            unElementoGoTo.defaultValue	    = '';
        }
         
        document.forms[ 'TranslationFormId'].submit();
        return true;
    }
    finally {
        pLogUserInterfaceEvent_END( '        ->fTRASubmitInvalidateStringTranslations_Sync', '');
    }    
}






function fTRASubmitDeactivateString_Sync( ) {

    try {

        pLogUserInterfaceEvent_BEGIN( '        ->fTRASubmitDeactivateString_Sync', '');
        
        if ( !fTRACadenaTraducidaIndexNumber()) {
            return false;
        }
    
        var unElementoNuevoEstadoTraduccion = document.getElementById( 'theNuevoEstadoTraduccion');
        if ( !unElementoNuevoEstadoTraduccion) {
            return false;
        }
        unElementoNuevoEstadoTraduccion.value	    	= 'DesactivarCadena';
        unElementoNuevoEstadoTraduccion.defaultValue	= 'DesactivarCadena';
        /*
        unElementoNuevoEstadoTraduccion.value	    	= '';
        unElementoNuevoEstadoTraduccion.defaultValue	= '';
        */      
        var unElementoCadenaTraducida = document.getElementById( 'theCadenaTraducida');
        if ( unElementoCadenaTraducida) {
            unElementoCadenaTraducida.value		    = '';
            unElementoCadenaTraducida.defaultValue	= '';
        }
        var unElementoGoTo = document.getElementById( 'theGoTo');
        if ( unElementoGoTo) {
            unElementoGoTo.value			= '';
            unElementoGoTo.defaultValue	    = '';
        }
         
        document.forms[ 'TranslationFormId'].submit();
        return true;
    }
    finally {
        pLogUserInterfaceEvent_END( '        ->fTRASubmitDeactivateString_Sync', '');
    }    
}







function fTRASubmitActivateString_Sync( ) {

    try {

        pLogUserInterfaceEvent_BEGIN( '        ->fTRASubmitActivateString_Sync', '');
        
        if ( !fTRACadenaTraducidaIndexNumber()) {
            return false;
        }
    
        var unElementoNuevoEstadoTraduccion = document.getElementById( 'theNuevoEstadoTraduccion');
        if ( !unElementoNuevoEstadoTraduccion) {
            return false;
        }
        
        unElementoNuevoEstadoTraduccion.value	     	= 'ActivarCadena';
        unElementoNuevoEstadoTraduccion.defaultValue	= 'ActivarCadena';        
        /* 
        unElementoNuevoEstadoTraduccion.value	     	= '';
        unElementoNuevoEstadoTraduccion.defaultValue	= '';
        */

        
        var unElementoCadenaTraducida = document.getElementById( 'theCadenaTraducida');
        if ( unElementoCadenaTraducida) {
            unElementoCadenaTraducida.value		    = '';
            unElementoCadenaTraducida.defaultValue	= '';
        }
        var unElementoGoTo = document.getElementById( 'theGoTo');
        if ( unElementoGoTo) {
            unElementoGoTo.value			= '';
            unElementoGoTo.defaultValue   	= '';
        }
         
        document.forms[ 'TranslationFormId'].submit();
        return true;
    }
    finally {
        pLogUserInterfaceEvent_END( '        ->fTRASubmitActivateString_Sync', '');
    }    
}





function fTRASubmitBatchStatusChanges_Sync() {

    try {

        pLogUserInterfaceEvent_BEGIN( '        ->fTRASubmitBatchStatusChanges_Sync', '');
        
        var unElementoNuevoEstadoTraduccion = document.getElementById( 'theNuevoEstadoTraduccion');
        if ( unElementoNuevoEstadoTraduccion) {
            unElementoNuevoEstadoTraduccion.value			= '';
            unElementoNuevoEstadoTraduccion.defaultValue	= '';
        }
        
        var unElementoCadenaTraducida = document.getElementById( 'theCadenaTraducida');
        if ( unElementoCadenaTraducida) {
            unElementoCadenaTraducida.value			= '';
            unElementoCadenaTraducida.defaultValue	= '';
        }
        var unElementoGoTo = document.getElementById( 'theGoTo');
        if ( unElementoGoTo) {
            unElementoGoTo.value			= '';
            unElementoGoTo.defaultValue	    = '';
        }
         
      
        document.forms[ 'TranslationFormId'].submit();
        return true;
    }
    finally {
        pLogUserInterfaceEvent_END( '        ->fTRASubmitBatchStatusChanges_Sync', '');
    }    
}





function fTRASubmitStringModulesChange_Sync( ) {

    try {

        pLogUserInterfaceEvent_BEGIN( '        ->fTRASubmitStringModulesChange_Sync', '');
        
        if ( !fTRACadenaTraducidaIndexNumber()) {
            return false;
        }

        var unElementoNewModuleNames = document.getElementById( 'theNewModuleNames');
        if ( !unElementoNewModuleNames) {
            return false;
        }        
        
        var unosNuevosNombresModulos = '';
        var unosNombresModulosMustChange = false;
        
        /* determine new module names by checking the selection state of check boxes for string modules */
        for ( var unIndexModulo=0; unIndexModulo < 1000; unIndexModulo++) {
        
            var unElementModulo = document.getElementById( 'cid_TRAEditorDetalle_Modulos_' + unIndexModulo);
            if ( !unElementModulo) {
                break;
            }
            
            if ( unElementModulo.checked) {
                var unValorElementModulo = unElementModulo.value;
                unosNuevosNombresModulos = unosNuevosNombresModulos + ' ' + unValorElementModulo;
            }
        }
        unElementoNewModuleNames.value = unosNuevosNombresModulos;
                
        
        var unElementoNuevoEstadoTraduccion = document.getElementById( 'theNuevoEstadoTraduccion');
        if ( !unElementoNuevoEstadoTraduccion) {
            return false;
        }
        unElementoNuevoEstadoTraduccion.value	    	= 'ChangeStringModules';
        unElementoNuevoEstadoTraduccion.defaultValue	= 'ChangeStringModules';
      
        var unElementoCadenaTraducida = document.getElementById( 'theCadenaTraducida');
        if ( unElementoCadenaTraducida) {
            unElementoCadenaTraducida.value		    = '';
            unElementoCadenaTraducida.defaultValue	= '';
        }
        var unElementoGoTo = document.getElementById( 'theGoTo');
        if ( unElementoGoTo) {
            unElementoGoTo.value			= '';
            unElementoGoTo.defaultValue	    = '';
        }
         
        document.forms[ 'TranslationFormId'].submit();
        return true;
    }
    finally {
        pLogUserInterfaceEvent_END( '        ->fTRASubmitStringModulesChange_Sync', '');
    }    
}




/* #################################################################
General key even access function to isolate from platform dependencies

*/
function fTRAKeyNumberFromEvent( theEvent) {

    var unKeyNumber = 0

    try {
        if( window.event) {       /* IE */
            unKeyNumber = theEvent.keyCode;
            if ( !unKeyNumber) {
            
            }
            return unKeyNumber;
        }
        else {
            if(theEvent.which || theEvent.keyCode) { /* Netscape/Firefox/Opera */
                unKeyNumber = theEvent.which;
                if ( unKeyNumber) {
                    return unKeyNumber;
                }
                unKeyNumber = theEvent.keyCode;
                return unKeyNumber;
            }
        }
    }
    catch( anException) {
    }
    return unKeyNumber;
}




function fTRAEvtHlr_NoConfirmTranslationChanges_OnMouseUp() {
    gTRANoConfirmTranslationChanges = 999;
    return true;
}


function fTRAEvtHlr_NoConfirmStatusChanges_OnMouseUp() {
    gTRANoConfirmStatusChanges = 999;
    return true;
}


function fTRAEvtHlr_NoConfirmTranslationDelete_OnMouseUp() {
    gTRANoConfirmTranslationDelete = 999;
    return true;
}



function fTRANoConfirmTranslationChanges() {
    if ( !( gTRANoConfirmTranslationChanges == 999)) {
        return gTRANoConfirmTranslationChanges;
    }
    
    var unElementoConfirmTranslationChanges = document.getElementById( 'theNoConfirmTranslationChanges')
    if ( !unElementoConfirmTranslationChanges) {
    
        gTRANoConfirmTranslationChanges = false;
        return gTRANoConfirmTranslationChanges;
    }
    
    if ( unElementoConfirmTranslationChanges.checked) {
    
        gTRANoConfirmTranslationChanges = true;
    }
    else {
        gTRANoConfirmTranslationChanges = false;
    }
    return gTRANoConfirmTranslationChanges;
}





function fTRANoConfirmStatusChanges() {
    if ( !( gTRANoConfirmStatusChanges == 999)) {
        return gTRANoConfirmStatusChanges;
    }
    
    var unElementoConfirmStatusChanges = document.getElementById( 'theNoConfirmStatusChanges')
    if ( !unElementoConfirmStatusChanges) {
    
        gTRANoConfirmStatusChanges = false;
        return gTRANoConfirmStatusChanges;
    }
    
    if ( unElementoConfirmStatusChanges.checked) {
    
        gTRANoConfirmStatusChanges = true;
    }
    else {
        gTRANoConfirmStatusChanges = false;
    }
    return gTRANoConfirmStatusChanges;
}






function fTRANoConfirmTranslationDelete() {
    if ( !( gTRANoConfirmTranslationDelete == 999)) {
        return gTRANoConfirmTranslationDelete;
    }
    
    var unElementoConfirmTranslationDelete = document.getElementById( 'theNoConfirmTranslationDelete')
    if ( !unElementoConfirmTranslationDelete) {
    
        gTRANoConfirmTranslationDelete = false;
        return gTRANoConfirmTranslationDelete;
    }
    
    if ( unElementoConfirmTranslationDelete.checked) {
    
        gTRANoConfirmTranslationDelete = true;
    }
    else {
        gTRANoConfirmTranslationDelete = false;
    }
    return gTRANoConfirmTranslationDelete;
}





/* #################################################################
Escape key in editor text area config access function

*/

cKeyAction_Escape_Escape = "action_escape";




cKeyNumberEscape = 27;
cKeyNumberCR     = 13;
cKeyNumberTab    = 9;


function fTRAKeyAction_Escape() {
    if ( !( gKeyAction_Escape_Cached == '999')) {
        return gKeyAction_Escape_Cached;
    }
    
    var unElementoKeyActionConfig = document.getElementById( 'theKeyAction_Escape')
    if ( !unElementoKeyActionConfig) {
    
        gKeyAction_Escape_Cached = cKeyAction_Escape_Escape;
        return gKeyAction_Escape_Cached;
    }
    
    if ( unElementoInteractionMode_Async.checked) {
    
        gKeyAction_Escape_Cached = cKeyAction_Escape_Escape;
    }
    else {
        gKeyAction_Escape_Cached = "";
    }
    return gKeyAction_Escape_Cached;
}





/* #################################################################
Tab key in editor text area config access function

*/

cKeyAction_Traducir                 = "action_traducir";
cKeyAction_TraducirYAvanzar         = "action_traducirYAvanzar";
cKeyAction_Avanzar                  = "action_avanzar";
cKeyAction_NextTabIndex             = "action_nextTabIndex";

cKeyActions = [ cKeyAction_TraducirYAvanzar,  cKeyAction_Traducir, cKeyAction_Avanzar, cKeyAction_NextTabIndex];

cKeyAction_Default_CR  = cKeyAction_TraducirYAvanzar;
cKeyAction_Default_Tab = cKeyAction_NextTabIndex;



function fTRAKeyAction_Tab() {
    if ( !( gKeyAction_Tab_Cached == '999')) {
        return gKeyAction_Tab_Cached;
    }
    
    var unElementoKeyActionConfig = document.getElementById( 'theKeyAction_Tab');
    
    var unKeyActionindex = unElementoKeyActionConfig.selectedIndex;
    
    if ( ( unKeyActionindex < 0) || ( unKeyActionindex >= cKeyActions.length)) {
    
        gKeyAction_Tab_Cached = cKeyAction_NextTabIndex;
        return cKeyAction_Default_Tab;
    }
    
    gKeyAction_Tab_Cached = cKeyActions[ unKeyActionindex]
    return gKeyAction_Tab_Cached;
    
}



/* #################################################################
CR key in editor text area config access function

*/



function fTRAKeyAction_CR() {
    if ( !( gKeyAction_CR_Cached == '999')) {
        return gKeyAction_CR_Cached;
    }
    
    var unElementoKeyActionConfig = document.getElementById( 'theKeyAction_CR');
    
    var unKeyActionindex = unElementoKeyActionConfig.selectedIndex;
    
    if ( ( unKeyActionindex < 0) || ( unKeyActionindex >= cKeyActions.length)) {
    
        gKeyAction_CR_Cached = cKeyAction_NextTabIndex;
        return cKeyAction_Default_CR;
    }
    
    gKeyAction_CR_Cached = cKeyActions[ unKeyActionindex];
    return gKeyAction_CR_Cached;
    
}






/* #################################################################
Aynchronous mode config access function

*/

function fAsynchronousTranslationMode() {
    

    if ( !gAsynchronousTranslationMode_Cached == 999) {
        return gAsynchronousTranslationMode_Cached;
    }
    
    if ( !fTRAIsAsyncRequestSupported()) {
        gAsynchronousTranslationMode_Cached = false;
        return gAsynchronousTranslationMode_Cached;
    }
    
    var unElementoInteractionMode_Async = document.getElementById( 'theInteractionMode_Async');
    if ( !unElementoInteractionMode_Async) {
        gAsynchronousTranslationMode_Cached = false;
        return gAsynchronousTranslationMode_Cached;
    }
    
    gAsynchronousTranslationMode_Cached = unElementoInteractionMode_Async.checked;

    return gAsynchronousTranslationMode_Cached;
}



function fTRAIsAsyncRequestSupported() {
    if ( !(gTRAIsAsyncRequestSupported_Cached = 999)){
        return gTRAIsAsyncRequestSupported_Cached;
    }
    
    gTRAIsAsyncRequestSupported_Cached = false;
    try {
        gTRAIsAsyncRequestSupported_Cached = SupportsAjax();
    }
    catch ( unException) {
    }
    return gTRAIsAsyncRequestSupported_Cached;
}





/* #################################################################
Instrumentation functions: must render user interface events
################################################################# */


function fTRAMustRenderUserInterfaceEvents() {
    if ( !(gTRAMustRenderUserInterfaceEvents = 999)){
        return gTRAMustRenderUserInterfaceEvents;
    }
    var unElementoRenderUserInterfaceEvents = document.getElementById( 'theRenderUserInterfaceEvents');
    if ( !unElementoRenderUserInterfaceEvents) {
        gTRAMustRenderUserInterfaceEvents = false;
    }
    
    gTRAMustRenderUserInterfaceEvents = unElementoRenderUserInterfaceEvents.checked;
    return gTRAMustRenderUserInterfaceEvents;
}




/* #################################################################
Edition functions
################################################################# */


function fTRAMostrarDetallesTraduccion() {
    var unElement = document.getElementById( 'theMostrarDetallesTraduccion');
    if ( !unElement) {
        return false;
    }
    return unElement.checked;
}







function pTRASetSimboloCadenaATraducirYEditorIndexAFilaNumero( theNewParentRowIndex) {

    try {

        pLogUserInterfaceEvent_BEGIN( '        ->pTRASetSimboloCadenaATraducirYEditorIndexAFilaNumero', 'editorIndex: ' + theNewParentRowIndex);

        var unElementoCadenaTraducidaIndex = document.getElementById( 'theCadenaTraducida_index');
        if ( !unElementoCadenaTraducidaIndex) {
            return false;
        }
    
        /* get simboloCadena e index to set them as soon as possible */
        var unSimboloCadenaEIndex = fTRA_GetSimboloCadenaEIndexEnFilaNumero( theNewParentRowIndex);
        if ( !unSimboloCadenaEIndex) {
            return false;
        }
        var unSimboloCadena		= unSimboloCadenaEIndex[ 0];   
        var unIndexTraduccion   = unSimboloCadenaEIndex[ 1];
    
        if ( (!unSimboloCadena) || (!unIndexTraduccion)) {
            return false;
        }
    
        /* keep track of the symbol under edition, storing it in a (hidden) field value */
        var unElementoSimboloCadenaATraducir = document.getElementById( 'theSimboloCadenaATraducir');
        if ( unElementoSimboloCadenaATraducir) {
            unElementoSimboloCadenaATraducir.value = unSimboloCadena;
        }
    
        /* setindex of translation being edited*/
        unElementoCadenaTraducidaIndex.value = unIndexTraduccion;
    }
    finally {
        pLogUserInterfaceEvent_END( '        ->pTRASetSimboloCadenaATraducirYEditorIndexAFilaNumero', 'editorIndex: ' + theNewParentRowIndex);
    }    
    
}
 



function pTRAAbrirEditorEnFilaNumero( theNewParentRowIndex) {

    try {

        pLogUserInterfaceEvent_BEGIN( '        ->pTRAAbrirEditorEnFilaNumero', 'editorIndex: ' + theNewParentRowIndex);

        var unElementoCadenaTraducidaIndex = document.getElementById( 'theCadenaTraducida_index');
        if ( !unElementoCadenaTraducidaIndex) {
            return false;
        }
    
        pTRAHideElementWithId( 'cid_TRAEditorDetalle');
        
        pTRAOcultarModulesEditor();
     
       /* get new parent: the cell of the translation to edit */
        var unNewParent = document.getElementById( 'cid_ColumnaCadenasTraducidas_' + theNewParentRowIndex);
        if ( !unNewParent) {
            return false;
        }
    
        /* get simboloCadena e index to set them as soon as possible */
        var unSimboloCadenaEIndex = fTRA_GetSimboloCadenaEIndexEnFilaNumero( theNewParentRowIndex);
        if ( !unSimboloCadenaEIndex) {
            return false;
        }
        var unSimboloCadena		= unSimboloCadenaEIndex[ 0];    
        var unIndexTraduccion   = unSimboloCadenaEIndex[ 1];
    
        if ( (!unSimboloCadena) || (!unIndexTraduccion)) {
            return false;
        }
    
        /* keep track of the symbol under edition, storing it in a (hidden) field value */
        var unElementoSimboloCadenaATraducir = document.getElementById( 'theSimboloCadenaATraducir');
        if ( unElementoSimboloCadenaATraducir) {
            unElementoSimboloCadenaATraducir.value = unSimboloCadena;
        }
    
        /* setindex of translation being edited */
        unElementoCadenaTraducidaIndex.value = unIndexTraduccion;
    
        /* get data in the translation to edit */
        var unosDatosEnFila = fTRA_GetDatosEnFilaNumero( theNewParentRowIndex);
        if ( !unosDatosEnFila) {
            return false;
        }
    
        /* get editor */
        var unElementEditorAreaYBotones = document.getElementById( 'cid_TRAEditorAreaYBotones');
        if ( !unElementEditorAreaYBotones) {
            return false;
        }
        
        pTRAHideElement( unElementEditorAreaYBotones);
    
        /* move editor to new translation cell */
        unNewParent.appendChild( unElementEditorAreaYBotones);
    
    
        /* set translation edit value  */
        var unEditorTextArea = document.getElementById( 'theCadenaTraducida');
        if ( unEditorTextArea) {
            var unValorCadenaTraducida		= fTRA_FieldDatosEnFila( unosDatosEnFila, 'cadenaTraducida_NewValue')[ 1];
            unEditorTextArea.value			= unValorCadenaTraducida;
            unEditorTextArea.defaultValue	= unValorCadenaTraducida;
        }
    
    
        /* set translation change counter to be sent to server to figure out if somebody else changed the translation since this user got the translation. */
        var unChangeCounter = document.getElementById( 'theChgCtr');
        if ( unChangeCounter) {
            var unValorChangeCounter		= fTRA_FieldDatosEnFila( unosDatosEnFila, 'contadorCambios')[ 1];
            unChangeCounter.value			= unValorChangeCounter;
            unChangeCounter.defaultValue	= unValorChangeCounter;
        }
    
        pTRAShowOrHideColumnStateTransitionButtonsEnFilaNumero( theNewParentRowIndex);
        
        pTRAShowOrHideEditorTextAreaEnFilaNumero(               theNewParentRowIndex);
        
        pTRAShowOrHideEditorButtonsEnFilaNumero(                theNewParentRowIndex);
     
        pTRAMostrarDetallesTraduccionEnFilaNumero(              theNewParentRowIndex);
              
        if ( fTRAAnyModulesAvailableForEdition()) {
            pTRAShowElementWithId( 'TRAEditModulesButton')
        }
        else {
            pTRAHideElementWithId( 'TRAEditModulesButton')
        }
        
        
        pTRAShowElement( unElementEditorAreaYBotones);
        
    
        /* mover focus to edit text area */
        fSetFocusToEditorTextArea();
        

        var unElementoFilaPrimera = document.getElementById( 'cid_FilaPrimeraDeSimbolo_' + unIndexTraduccion);
        if ( unElementoFilaPrimera) {
            var unElementoFilaUltima = document.getElementById( 'cid_FilaUltimaDeSimbolo_' + unIndexTraduccion);
            pTRAScrollToShow( unElementoFilaPrimera, unElementoFilaUltima);
        }		
        
    }
    finally {
        pLogUserInterfaceEvent_END( '        ->pTRAAbrirEditorEnFilaNumero', 'editorIndex: ' + theNewParentRowIndex);
    }    
    
}








function pTRAShowOrHideEditorTextAreaEnFilaNumero( theTranslationIndex) {

    if ( (!theTranslationIndex)) {
        return false;
    }

    var unEditorTextArea = document.getElementById( 'theCadenaTraducida');
    if ( !unEditorTextArea) {
        return false;
    }

    /* get data in the translation to edit */
    var unosDatosEnFila = fTRA_GetDatosEnFilaNumero( theTranslationIndex);
    if ( !unosDatosEnFila) {
        return false;
    }
    
    var unEstadoTraduccion  = fTRA_FieldDatosEnFila( unosDatosEnFila, 'estadoTraduccion')[ 1];
    
    var unosTargetStatusChanges  = fTRA_FieldDatosEnFila( unosDatosEnFila, 'targetStatusChanges')[ 1];
        
    if (( ( unEstadoTraduccion == 'Pendiente') || ( unEstadoTraduccion == 'Traducida')) && ( unosTargetStatusChanges.indexOf( 'Traducida') >= 0)) {
    
        pTRAShowElementWithId( 'theCadenaTraducida');
    }
    else{
        pTRAHideElementWithId( 'theCadenaTraducida');
    }
    
    return true;
     
}







function pTRAShowOrHideEditorButtonsEnFilaNumero( theTranslationIndex) {

    if ( (!theTranslationIndex)) {
        return false;
    }


     /* get data in the translation to edit */
    var unosDatosEnFila = fTRA_GetDatosEnFilaNumero( theTranslationIndex);
    if ( !unosDatosEnFila) {
        return false;
    }
     
    var unEstadoTraduccion  = fTRA_FieldDatosEnFila( unosDatosEnFila, 'estadoTraduccion')[ 1];
    
    var unosTargetStatusChanges  = fTRA_FieldDatosEnFila( unosDatosEnFila, 'targetStatusChanges')[ 1];
        

    if ( unosTargetStatusChanges.indexOf( 'Pendiente') >= 0) {
        pTRAShowElementWithId( 'TRAStatusChangeButton_Pendiente');
        pTRAShowElementWithId( 'TRAStatusChangeButton_Pendiente_Icon');
    }
    else {
        pTRAHideElementWithId( 'TRAStatusChangeButton_Pendiente');			
        pTRAHideElementWithId( 'TRAStatusChangeButton_Pendiente_Icon');		
    }

    if ( unosTargetStatusChanges.indexOf( 'Traducida') >= 0) {
        if ( unEstadoTraduccion == 'Traducida') {
            pTRAShowElementWithId( 'TRAStatusChangeButton_Traducir');
            pTRAShowElementWithId( 'TRAStatusChangeButton_Traducir_Icon');
        }
        else {
            if ( unEstadoTraduccion == 'Revisada') {
                pTRAHideElementWithId( 'TRAStatusChangeButton_Traducir');
                pTRAHideElementWithId( 'TRAStatusChangeButton_Traducir_Icon');
            }
            else {
                if ( unEstadoTraduccion == 'Pendiente') {
                    pTRAShowElementWithId( 'TRAStatusChangeButton_Traducir');
                    pTRAShowElementWithId( 'TRAStatusChangeButton_Traducir_Icon');
                }
                else {
                    pTRAHideElementWithId( 'TRAStatusChangeButton_Traducir');
                    pTRAHideElementWithId( 'TRAStatusChangeButton_Traducir_Icon');
                }
            }
        }
    }
    else {
        pTRAHideElementWithId( 'TRAStatusChangeButton_Traducir');				
        pTRAHideElementWithId( 'TRAStatusChangeButton_Traducir_Icon');				
    }

    pTRAEnableElementWithId( 'TRAStatusChangeButton_Pendiente' );
    pTRAEnableElementWithId( 'TRAStatusChangeButton_Pendiente_Icon' );
    pTRAEnableElementWithId( 'TRAStatusChangeButton_Traducir' );
    pTRAEnableElementWithId( 'TRAStatusChangeButton_Traducir_Icon' );
     
}
    
    




function pTRAShowOrHideColumnStateTransitionButtonsEnFilaNumero( theTranslationIndex) {

    if ( (!theTranslationIndex)) {
        return false;
    }

    /* get data in the translation to edit */
    var unosDatosEnFila = fTRA_GetDatosEnFilaNumero( theTranslationIndex);
    if ( !unosDatosEnFila) {
        return false;
    }
     
    var unEstadoTraduccion  = fTRA_FieldDatosEnFila( unosDatosEnFila, 'estadoTraduccion')[ 1];
    
    var unosTargetStatusChanges  = fTRA_FieldDatosEnFila( unosDatosEnFila, 'targetStatusChanges')[ 1];
        
    
    if ( unosTargetStatusChanges.indexOf( 'Traducida') >= 0) {
        if ( unEstadoTraduccion == 'Traducida') {
            pTRAHideElementWithId(          'TRAStatusChangeButton_' + theTranslationIndex + '_Traducida');
        }
        else {
            if ( unEstadoTraduccion == 'Revisada') {
                pTRAShowElementWithId(      'TRAStatusChangeButton_' + theTranslationIndex + '_Traducida');
            }
            else {
                if ( unEstadoTraduccion == 'Pendiente') {
                    pTRAHideElementWithId(  'TRAStatusChangeButton_' + theTranslationIndex + '_Traducida');
                }
                else {
                    pTRAShowElementWithId(  'TRAStatusChangeButton_' + theTranslationIndex + '_Traducida');
                }
            }
        }
    }
    else {
        pTRAHideElementWithId( 'TRAStatusChangeButton_' + theTranslationIndex + '_Traducida');				
    }
    

    if ( unosTargetStatusChanges.indexOf( 'Revisada') >= 0) {
        pTRAShowElementWithId( 'TRAStatusChangeButton_' + theTranslationIndex + '_Revisada');
    }
    else {
        pTRAHideElementWithId( 'TRAStatusChangeButton_' + theTranslationIndex + '_Revisada');
    }

    if ( unosTargetStatusChanges.indexOf( 'Definitiva') >= 0) {
        pTRAShowElementWithId( 'TRAStatusChangeButton_' + theTranslationIndex + '_Definitiva');
    }
    else {
        pTRAHideElementWithId( 'TRAStatusChangeButton_' + theTranslationIndex + '_Definitiva');
    }
    
    pTRAEnableElementWithId( 'TRAStatusChangeButton_' + theTranslationIndex + '_Traducida' );
    pTRAEnableElementWithId( 'TRAStatusChangeButton_' + theTranslationIndex + '_Revisada' );
    pTRAEnableElementWithId( 'TRAStatusChangeButton_' + theTranslationIndex + '_Definitiva' );
    
    return true;
}   






function pTRAMostrarDetallesTraduccionEnFilaNumero( theNewParentRowIndex) {

    pTRAHideElementWithId( 'cid_TRAEditorDetalle');
    
    if ( !fTRAMostrarDetallesTraduccion()) {
        return false;				

    }
    
    if ( (!theNewParentRowIndex)) {
        return false;
    }

    /* get editor detail */
    var unElementEditorDetalle = document.getElementById( 'cid_TRAEditorDetalle');
    if ( !unElementEditorDetalle) {
        return false;
    }
    
     /* get data in the translation to edit */
    var unosDatosEnFila = fTRA_GetDatosEnFilaNumero( theNewParentRowIndex);
    if ( !unosDatosEnFila) {
        return false;
    }

    var unElementEditorDetalleContainerEnFila = document.getElementById( 'cid_TRAEditorDetalleHolder_' + theNewParentRowIndex);
    if ( !unElementEditorDetalleContainerEnFila) {
        return false;
    }
    /* move editor detail to new translation cell */
    unElementEditorDetalleContainerEnFila.appendChild( unElementEditorDetalle);


    fTRA_SetContenidoTextoElementoWithId( 'cid_TRAEditorDetalle_simboloCadena',      fTRA_FieldDatosEnFila( unosDatosEnFila, 'simboloCadena')[ 1]);
    fTRA_SetContenidoTextoElementoWithId( 'cid_TRAEditorDetalle_nombresModulos',     fTRA_FieldDatosEnFila( unosDatosEnFila, 'nombresModulos')[ 1]);
    fTRA_SetContenidoTextoElementoWithId( 'cid_TRAEditorDetalle_referenciasFuentes', fTRA_FieldDatosEnFila( unosDatosEnFila, 'referenciasFuentes')[ 1]);
    fTRA_SetContenidoTextoElementoWithId( 'cid_TRAEditorDetalle_idCadena',		     fTRA_FieldDatosEnFila( unosDatosEnFila, 'idCadena')[ 1]);
    fTRA_SetContenidoTextoElementoWithId( 'cid_TRAEditorDetalle_contadorCambios',    fTRA_FieldDatosEnFila( unosDatosEnFila, 'contadorCambios')[ 1]);

    pTRAShowElementWithId( 'cid_TRAEditorDetalle_simboloCadena_row');
    pTRAShowElementWithId( 'cid_TRAEditorDetalle_idCadena_row');
    pTRAShowElementWithId( 'cid_TRAEditorDetalle_contadorCambios_row');
    pTRAShowElementWithId( 'cid_TRAEditorDetalle_nombresModulos_row');
    pTRAShowElementWithId( 'cid_TRAEditorDetalle_referenciasFuentes_row');

    unEstadoTraduccionFila = fTRA_FieldDatosEnFila( unosDatosEnFila, 'estadoTraduccion')[ 1];

    fTRA_SetContenidoTextoElementoWithId( 'cid_TRAEditorDetalle_Definitiva_Fecha',   fTRA_FieldDatosEnFila( unosDatosEnFila, 'fechaDefinitivo')[ 1]);
    fTRA_SetContenidoTextoElementoWithId( 'cid_TRAEditorDetalle_Definitiva_Usuario', fTRA_FieldDatosEnFila( unosDatosEnFila, 'usuarioCoordinador')[ 1]);
    fTRA_SetContenidoTextoElementoWithId( 'cid_TRAEditorDetalle_Revisada_Fecha',     fTRA_FieldDatosEnFila( unosDatosEnFila, 'fechaRevision')[ 1]);
    fTRA_SetContenidoTextoElementoWithId( 'cid_TRAEditorDetalle_Revisada_Usuario',   fTRA_FieldDatosEnFila( unosDatosEnFila, 'usuarioRevisor')[ 1]);
    fTRA_SetContenidoTextoElementoWithId( 'cid_TRAEditorDetalle_Traducida_Fecha',    fTRA_FieldDatosEnFila( unosDatosEnFila, 'fechaTraduccion')[ 1]);
    fTRA_SetContenidoTextoElementoWithId( 'cid_TRAEditorDetalle_Traducida_Usuario',  fTRA_FieldDatosEnFila( unosDatosEnFila, 'usuarioTraductor')[ 1]);
    
    if ( unEstadoTraduccionFila == 'Definitiva') {
        /* fTRA_SetContenidoTextoElementoWithId( 'cid_TRAEditorDetalle_Definitiva_Fecha',   fTRA_FieldDatosEnFila( unosDatosEnFila, 'fechaDefinitivo')[ 1]);
        fTRA_SetContenidoTextoElementoWithId( 'cid_TRAEditorDetalle_Definitiva_Usuario', fTRA_FieldDatosEnFila( unosDatosEnFila, 'usuarioCoordinador')[ 1]);
        */ 
        
        pTRAShowElementWithId( 'cid_TRAEditorDetalle_Definitiva');

    }
    else {
        pTRAHideElementWithId( 'cid_TRAEditorDetalle_Definitiva');
    }

    if ( ( unEstadoTraduccionFila == 'Definitiva') || ( unEstadoTraduccionFila == 'Revisada')) {					
        /* fTRA_SetContenidoTextoElementoWithId( 'cid_TRAEditorDetalle_Revisada_Fecha',   fTRA_FieldDatosEnFila( unosDatosEnFila, 'fechaRevision')[ 1]);
        fTRA_SetContenidoTextoElementoWithId( 'cid_TRAEditorDetalle_Revisada_Usuario', fTRA_FieldDatosEnFila( unosDatosEnFila, 'usuarioRevisor')[ 1]);
        */
        
        pTRAShowElementWithId( 'cid_TRAEditorDetalle_Revisada');
    }
    else {
        pTRAHideElementWithId( 'cid_TRAEditorDetalle_Revisada');
    }	

    if ( ( unEstadoTraduccionFila == 'Definitiva') || ( unEstadoTraduccionFila == 'Revisada') || ( unEstadoTraduccionFila == 'Traducida')) {
        /* fTRA_SetContenidoTextoElementoWithId( 'cid_TRAEditorDetalle_Traducida_Fecha',   fTRA_FieldDatosEnFila( unosDatosEnFila, 'fechaTraduccion')[ 1]);
        fTRA_SetContenidoTextoElementoWithId( 'cid_TRAEditorDetalle_Traducida_Usuario', fTRA_FieldDatosEnFila( unosDatosEnFila, 'usuarioTraductor')[ 1]);
        */
        
        pTRAShowElementWithId( 'cid_TRAEditorDetalle_Traducida');
    }
    else {
        pTRAHideElementWithId( 'cid_TRAEditorDetalle_Traducida');
    }		
    
    fTRA_SetContenidoTextoElementoWithId( 'cid_TRAEditorDetalle_Creada_Fecha',   fTRA_FieldDatosEnFila( unosDatosEnFila, 'fechaCreacion')[ 1]);
    fTRA_SetContenidoTextoElementoWithId( 'cid_TRAEditorDetalle_Creada_Usuario', fTRA_FieldDatosEnFila( unosDatosEnFila, 'usuarioCreador')[ 1]);
    pTRAShowElementWithId( 'cid_TRAEditorDetalle_Creada');

    
    pTRAShowElementWithId( 'cid_TRAEditorDetalle');	
    
    return true;
}



/* #################################################################
Scrolling functions
################################################################# */

cMinOffsetMismatchToAllowScroll = 16;


function pTRAScrollToShow( theFirstElement, theAfterLastElement) {
/* see res javascript htmltooltip.js */


    if ( (!theFirstElement) || ( !theAfterLastElement)) {
        return false;
    }

    var unFirstTop		= fAbsoluteTop( theFirstElement);
    var unAfterLastTop  = fAbsoluteTop( theAfterLastElement);


    if ( unAfterLastTop <= unFirstTop) {
        /* invisible ? error ? */
        return false;
    }

    var aCurrentScroll = -1;
    try { /* firefox, opera, safari*/
        aCurrentScroll = window.pageYOffset;
    }
    catch( anException) {
    }
    if ( aCurrentScroll < 0) {
        try { /* IE */
            aCurrentScroll = document.body.scrollTop; 
        }
        catch( anException) {
            /* can not process without browser support, but will give it a try .... */
        }
    }
    if ( aCurrentScroll < 0) {
        aCurrentScroll = 0;
    }

    var unViewportHeight = 0;
    try { /* firefox, opera, safari */
        unViewportHeight = window.innerHeight; 
    }
    catch( anException) {
    }
    if ( !unViewportHeight) {
        try { /*  IE */
            unViewportHeight = document.body.clientHeight; 
        }
        catch( anException) {
        }
    }
    if ( !unViewportHeight) {
        /* can not process without browser support */
        return false;
    }


    if( ( aCurrentScroll <= unFirstTop) && ( ( aCurrentScroll + unViewportHeight) >= ( unAfterLastTop - 1))) {
        /* No need to scroll if elements from top to the one before last are shown */
        return false;
    }

    if ( ( unAfterLastTop - unFirstTop) >= unViewportHeight)  {
        /* if the height from the top of first element to the top of after last element 
         is bigger than the viewport height
        then scroll to show the top of the first element just at the top of the vieport */

    window.scrollTo( 0, unFirstTop);
    return true;
}

    if( !( Math.abs( aCurrentScroll - unFirstTop) >= cMinOffsetMismatchToAllowScroll)) {
        /* No need to scroll if already close enough to the top of the vieport  */
        return false;
    }


    /* because the editors are opened in sequence from top to bottom
    if scroll is needed, scroll just enough to bring up
    the last element to display just above the bottom of the viewport  */


    window.scrollTo( 0, unAfterLastTop - unViewportHeight - 1);

}


function fAbsoluteTop( theElement) {
    if ( !theElement) {
        return 0;
    }

    var unTop = theElement.offsetTop;
    var unElement = theElement.offsetParent;
    while( unElement) {
        unTop += unElement.offsetTop;
        unElement = unElement.offsetParent;
    }
    return unTop
}





function fTRAMoveFocus_AfterEditorTextArea() {

    var unElementoBotonTraducir = document.getElementById( 'TRAStatusChangeButton_Traducir');
    if ( unElementoBotonTraducir) {
        if ( fTRAIsVisibleElement( unElementoBotonTraducir) && fTRAIsEnabledElement( unElementoBotonTraducir)) {
            unElementoBotonTraducir.focus();
            return unElementoBotonTraducir;
        }
    }

    var unElementoBotonPendiente = document.getElementById( 'TRAStatusChangeButton_Pendiente');
    if ( unElementoBotonPendiente) {
        if ( fTRAIsVisibleElement( unElementoBotonPendiente) && fTRAIsEnabledElement( unElementoBotonPendiente)) {
            unElementoBotonPendiente.focus();
            return unElementoBotonPendiente;
        }
    }

    var unCadenaTraducidaIndex = fTRACadenaTraducidaIndexNumber();
    if ( !unCadenaTraducidaIndex) {
        return null;
    }
    
    var unElementoBotonTraducida    = document.getElementById( 'TRAStatusChangeButton_'+ unCadenaTraducidaIndex + '_Traducida');
    if ( unElementoBotonTraducida) {
        if ( fTRAIsVisibleElement( unElementoBotonTraducida)    && fTRAIsEnabledElement( unElementoBotonTraducida)) {
            unElementoBotonTraducida.focus();
            return unElementoBotonTraducida;
        }
    }
    var unElementoBotonRevisada     = document.getElementById( 'TRAStatusChangeButton_'+ unCadenaRevisadaIndex + '_Revisada');
    if ( unElementoBotonRevisada) {
        if ( fTRAIsVisibleElement( unElementoBotonRevisada)     && fTRAIsEnabledElement( unElementoBotonRevisada)) {
            unElementoBotonRevisada.focus();
            return unElementoBotonRevisada;
        }
    }
    var unElementoBotonDefinitiva   = document.getElementById( 'TRAStatusChangeButton_'+ unCadenaDefinitivaIndex + '_Definitiva');
    if ( unElementoBotonDefinitiva) {
        if ( fTRAIsVisibleElement( unElementoBotonDefinitiva)   && fTRAIsEnabledElement( unElementoBotonDefinitiva)) {
            unElementoBotonDefinitiva.focus();
            return unElementoBotonDefinitiva;
        }
    }
    
    var unElementoBotonSiguiente   = document.getElementById( 'theGoToNext');
    if ( unElementoBotonSiguiente) {
        if ( fTRAIsVisibleElement( unElementoBotonSiguiente)   && fTRAIsEnabledElement( unElementoBotonSiguiente)) {
            unElementoBotonSiguiente.focus();
            return unElementoBotonSiguiente;
        }
    }
    
    var unElementoBotonPrimero   = document.getElementById( 'theGoToFirst');
    if ( unElementoBotonPrimero) {
        if ( fTRAIsVisibleElement( unElementoBotonPrimero)   && fTRAIsEnabledElement( unElementoBotonPrimero)) {
            unElementoBotonPrimero.focus();
            return unElementoBotonPrimero;
        }
    }

    return null;
}





function fTRAIsTimeProfileRequested() {
    var unElementRenderProfile = document.getElementById( 'theRenderProfile');
    if ( !unElementRenderProfile) {
        return false;
    }
    var unIsTimeProfileRequested = unElementRenderProfile.checked;
    return unIsTimeProfileRequested;
}



/* #################################################################
Aynchronous communication

*/
function pTRAAsyncRequest_Service_TranslationChange_Send( theCodigoIdiomaATraducir, theSimboloCadenaATraducir, theCadenaTraducida, theContadorCambios, theCadenaTraducidaIndex) {

    if ( !fTRAIsAsyncRequestSupported()) {
        return false;
    }
    
    /* need to use encodeURIComponent instead of encodeURI, to escape + */
    var someRequestParameters =                         '?theCodigoIdiomaATraducir='  + encodeURIComponent( theCodigoIdiomaATraducir);
    someRequestParameters = someRequestParameters + '&theSimboloCadenaATraducir=' + encodeURIComponent( theSimboloCadenaATraducir);
    someRequestParameters = someRequestParameters + '&theCadenaTraducida='        + encodeURIComponent( theCadenaTraducida);
    someRequestParameters = someRequestParameters + '&theChgCtr='                 + encodeURIComponent( theContadorCambios);
    
    var aIsTimeProfileRequested = fTRAIsTimeProfileRequested();
    if ( aIsTimeProfileRequested) {
        someRequestParameters = someRequestParameters + '&theRenderProfileAsync=on';
    }

    var aRequestString = fTRAAsyncRequestURL() + someRequestParameters;

    var unRequestDisplayField = document.getElementById( 'theTRAAsyncRequest_Display_Field');
    if (unRequestDisplayField) {
        unRequestDisplayField.value = aRequestString;
    }

    g_ajax_obj.CallXMLHTTPObjectGETParamPartial( aRequestString, pTRAAsyncRequest_Response_Handler, theCadenaTraducidaIndex, pTRAAsyncRequest_Sent_Handler, theCadenaTraducidaIndex );
    return true;

}


function pTRAAsyncRequest_Service_StatusChange_Send( theCodigoIdiomaATraducir, theSimboloCadenaATraducir, theNewTranslationStatus, theContadorCambios, theCadenaTraducidaIndex) {
    
    if ( !fTRAIsAsyncRequestSupported()) {
        return false;
    }

    /* need to use encodeURIComponent instead of encodeURI, to escape +  */
    var someRequestParameters =                         '?theCodigoIdiomaATraducir='  + encodeURIComponent( theCodigoIdiomaATraducir);
    someRequestParameters = someRequestParameters + '&theSimboloCadenaATraducir=' + encodeURIComponent( theSimboloCadenaATraducir);
    someRequestParameters = someRequestParameters + '&theChgCtr='                 + encodeURIComponent( theContadorCambios);
    someRequestParameters = someRequestParameters + '&form_submit='				  + encodeURIComponent( theNewTranslationStatus);

    var aIsTimeProfileRequested = fTRAIsTimeProfileRequested();
    if ( aIsTimeProfileRequested) {
        someRequestParameters = someRequestParameters + '&theRenderProfileAsync=on';
    }
    
    var aRequestString = fTRAAsyncRequestURL() + someRequestParameters;

    var unRequestDisplayField = document.getElementById( 'theTRAAsyncRequest_Display_Field');
    if (unRequestDisplayField) {
        unRequestDisplayField.value = aRequestString;
    }

    g_ajax_obj.CallXMLHTTPObjectGETParamPartial( aRequestString, pTRAAsyncRequest_Response_Handler, theCadenaTraducidaIndex, pTRAAsyncRequest_Sent_Handler, theCadenaTraducidaIndex );

    return true;

}



function pTRAAsyncRequest_Service_InvalidateStringTranslations_Send( theCodigoIdiomaATraducir, theSimboloCadenaATraducir, theCadenaTraducidaIndex) {
    
    if ( !fTRAIsAsyncRequestSupported()) {
        return false;
    }

    /* need to use encodeURIComponent instead of encodeURI, to escape +
    
    theCodigoIdiomaATraducir is sent as the current language, to retrieve results from
    */
    var someRequestParameters = '?theCodigoIdiomaATraducir='  + encodeURIComponent( theCodigoIdiomaATraducir);
    someRequestParameters = someRequestParameters + '&theSimboloCadenaATraducir=' + encodeURIComponent( theSimboloCadenaATraducir);
    someRequestParameters = someRequestParameters + '&form_submit=InvalidarTraduccionesCadena';

    var aIsTimeProfileRequested = fTRAIsTimeProfileRequested();
    if ( aIsTimeProfileRequested) {
        someRequestParameters = someRequestParameters + '&theRenderProfileAsync=on';
    }
    
    var aRequestString = fTRAAsyncRequestURL() + someRequestParameters;

    var unRequestDisplayField = document.getElementById( 'theTRAAsyncRequest_Display_Field');
    if (unRequestDisplayField) {
        unRequestDisplayField.value = aRequestString;
    }

    g_ajax_obj.CallXMLHTTPObjectGETParamPartial( aRequestString, pTRAAsyncRequest_Response_Handler, theCadenaTraducidaIndex, pTRAAsyncRequest_Sent_Handler, theCadenaTraducidaIndex );

    return true;

}




function pTRAAsyncRequest_Service_StringModulesChange_Send( theCodigoIdiomaATraducir, theSimboloCadenaATraducir, theNewModuleNames, theCadenaTraducidaIndex) {
    
    if ( !fTRAIsAsyncRequestSupported()) {
        return false;
    }

    /* need to use encodeURIComponent instead of encodeURI, to escape +  */
    var someRequestParameters =                         '?theCodigoIdiomaATraducir='   + encodeURIComponent( theCodigoIdiomaATraducir);
    someRequestParameters = someRequestParameters + '&theSimboloCadenaATraducir='      + encodeURIComponent( theSimboloCadenaATraducir);
    someRequestParameters = someRequestParameters + '&theNewModuleNames='              + encodeURIComponent( theNewModuleNames);
    someRequestParameters = someRequestParameters + '&form_submit=ChangeStringModules';

    var aIsTimeProfileRequested = fTRAIsTimeProfileRequested();
    if ( aIsTimeProfileRequested) {
        someRequestParameters = someRequestParameters + '&theRenderProfileAsync=on';
    }
    
    var aRequestString = fTRAAsyncRequestURL() + someRequestParameters;

    var unRequestDisplayField = document.getElementById( 'theTRAAsyncRequest_Display_Field');
    if (unRequestDisplayField) {
        unRequestDisplayField.value = aRequestString;
    }

    g_ajax_obj.CallXMLHTTPObjectGETParamPartial( aRequestString, pTRAAsyncRequest_Response_Handler, theCadenaTraducidaIndex, pTRAAsyncRequest_Sent_Handler, theCadenaTraducidaIndex );

    return true;

}



function pTRAAsyncRequest_Response_Handler( theResponseText, theParamether) {
    if (!theResponseText) {
        return false;
    }

    pTRAAsyncRequest_Response_Display( theResponseText);

    return true;
}



function pTRAAsyncRequest_Sent_Handler( theResponseText, theParamether) {
    if (!theResponseText) {
        return false;
    }

    pTRAAsyncRequest_StatusDisplay_Sent( theResponseText, theParamether);

    return true;
}



/* toggles all of the Languages for translator's reference */
function pTRAToggleAllReferenceLanguages( ) {

    var unElementAllReferenceLanguages = document.getElementById( 'cid_TRAToggleAllReferenceLanguages');
    if ( !unElementAllReferenceLanguages) {
        return false;
    }
    var unNewValueForAllReferenceLanguages = unElementAllReferenceLanguages.checked;
    for( var unIdCounter=0; unIdCounter < cTRAMaxRowsToLoopForOtherElements; unIdCounter++) {

        var unElement = document.getElementById( 'theIdiomasReferencia_' + unIdCounter );
    
        if ( !unElement) {
            break;
        }
        unElement.checked = unNewValueForAllReferenceLanguages;
    }  
}





/* selects all of the Languages for translator's reference */
function pTRASelectAllReferenceLanguages( ) {

    for( var unIdCounter=0; unIdCounter < cTRAMaxRowsToLoopForOtherElements; unIdCounter++) {

        var unElement = document.getElementById( 'theIdiomasReferencia_' + unIdCounter );
    
        if ( !unElement) {
            break;
        }
        unElement.checked = 1;
    }  
}




/* deselects the Languages for translator's reference */
function pTRASelectNoReferenceLanguages( ) {

    for( var unIdCounter=0; unIdCounter < cTRAMaxRowsToLoopForOtherElements; unIdCounter++) {

        var unElement = document.getElementById( 'theIdiomasReferencia_' + unIdCounter );
    
        if ( !unElement) {
            break;
        }
        unElement.checked = 0;
    }  
}




/* selects all of the Modules for translator's reference  */
function pTRAToggleAllModules( ) {

    unElementAllModules = document.getElementById( 'cid_TRAToggleAllModules')
    if ( !unElementAllModules) {
        return false;
    }
    unNewValueForAllModules = unElementAllModules.checked;
    for( var unIdCounter=0; unIdCounter < cTRAMaxRowsToLoopForOtherElements; unIdCounter++) {

        var unElement = document.getElementById( 'theNombreModulo_' + unIdCounter );
    
        if ( !unElement) {
            break;
        }
        unElement.checked = unNewValueForAllModules;
    }  
}




/* selects all the Modules in the filter  */
function pTRASelectAllModules( ) {

    for( var unIdCounter=0; unIdCounter < cTRAMaxRowsToLoopForOtherElements; unIdCounter++) {

        var unElement = document.getElementById( 'theNombreModulo_' + unIdCounter );
    
        if ( !unElement) {
            break;
        }
        unElement.checked = 1;
    }  
}




/* deselects the Modules in the filter  */
function pTRASelectNoModules( ) {

    for( var unIdCounter=0; unIdCounter < 1000; unIdCounter++) {

        var unElement = document.getElementById( 'theNombreModulo_' + unIdCounter );
    
        if ( !unElement) {
            break;
        }
        unElement.checked = 0;
    }  
}








function fTRABatchStatusChanges() {

    var unElementoBatchStatusChanges = document.getElementById( 'theBatchStatusChanges');
    if ( !unElementoBatchStatusChanges) {
        return false;
    }

    var unBatchStatusChanges = unElementoBatchStatusChanges.checked;
    return unBatchStatusChanges;
}






function fTRARecordBatchStatusChange( theCadenaTraducidaIndex, theNewTranslationStatus) {  

    try {

        pLogUserInterfaceEvent_BEGIN( '        ->fTRARecordBatchStatusChange', 'editorIndex: ' + theCadenaTraducidaIndex + ' theNewTranslationStatus: ' + theNewTranslationStatus);

        if ( !theNewTranslationStatus) {
            return false;
        }
    
        var unElementoCodigoIdiomaCursor        = document.getElementById( 'theCodigoIdiomaCursor');
        if ( !unElementoCodigoIdiomaCursor) {
            return false;
        }
        var unCodigoIdiomaCursor = unElementoCodigoIdiomaCursor.value;
        if ( !unCodigoIdiomaCursor.length) {
            return false;
        }
    
    
        /* get data in the translation to edit */
        var unosDatosEnFila = fTRA_GetDatosEnFilaNumero( theCadenaTraducidaIndex);
        if ( !unosDatosEnFila) {
            return false;
        }
    
        var unFieldIdCadena	    = fTRA_FieldDatosEnFila( unosDatosEnFila, 'idCadena');
        if ( !unFieldIdCadena) {
            return false;
        }
        var unIdCadena = unFieldIdCadena[ 1];
        if ( !unIdCadena ) {
            return false;
        }
    
        var unFieldContadorCambios	    = fTRA_FieldDatosEnFila( unosDatosEnFila, 'contadorCambios');
        if ( !unFieldContadorCambios) {
            return false;
        }
        var unContadorCambios = unFieldContadorCambios[ 1];
        if ( !unContadorCambios ) {
            return false;
        }
    
        pLogUserInterfaceEvent( '            ->fTRARecordBatchStatusChange', 'idCadena: ' + unIdCadena );
        
        fTRARemoveIdFromOtherBatchStatusChanges( unIdCadena, theNewTranslationStatus);
        fTRA_SetBGColorEnBotonesEstadoFilaNumero( theCadenaTraducidaIndex, '');          

        if ( fTRAAddOrRemoveIdFromBatchStatusChange(  unIdCadena, theNewTranslationStatus, unContadorCambios)) {
            fTRA_SetBGColorEnBotonEstadoFilaNumero(   theCadenaTraducidaIndex, theNewTranslationStatus, cTRABGColor_Translation_BatchStatusChangeRecorded);  
        }
        return true;
    }
    finally {
        pLogUserInterfaceEvent_END( '        ->fTRARecordBatchStatusChange', 'editorIndex: ' + theCadenaTraducidaIndex + 'theNewTranslationStatus: ' + theNewTranslationStatus);
    }    
}



function fTRARemoveIdFromOtherBatchStatusChanges( theIdCadena, theNewTranslationStatus) {  
    if ( !theNewTranslationStatus) {
        return false;
    }

    if ( !theIdCadena) {
        return false;
    }

    if ( theNewTranslationStatus == 'Traducida') {
        fTRARemoveIdFromBatchStatusChange( theIdCadena, 'Revisada');
        fTRARemoveIdFromBatchStatusChange( theIdCadena, 'Definitiva');
        return true;
    }
    if ( theNewTranslationStatus == 'Revisada') {
        fTRARemoveIdFromBatchStatusChange( theIdCadena, 'Traducida');
        fTRARemoveIdFromBatchStatusChange( theIdCadena, 'Definitiva');
        return true;
    }
    if ( theNewTranslationStatus == 'Definitiva') {
        fTRARemoveIdFromBatchStatusChange( theIdCadena, 'Traducida');
        fTRARemoveIdFromBatchStatusChange( theIdCadena, 'Revisada');
        return true;
    }
    return false;
}



function fTRAAddOrRemoveIdFromBatchStatusChange( theIdCadena, theNewTranslationStatus, theContadorCambios) {  

    try {

        pLogUserInterfaceEvent_BEGIN( '               ->fTRAAddOrRemoveIdFromBatchStatusChange',  'idCadena: ' + theIdCadena + ' status: ' + theNewTranslationStatus);

        if ( !theNewTranslationStatus) {
            return false;
        }

        if ( !theIdCadena) {
            return false;
        }
        
        var unElementoBatchStatusChangeIds   = document.getElementById( 'theBatch_' + theNewTranslationStatus);
        if ( !unElementoBatchStatusChangeIds) {
            return false;
        }
        var unosBatchStatusChangeIds = unElementoBatchStatusChangeIds.value;
        if ( unosBatchStatusChangeIds.length == 0) {
        
            var unNuevoBatchStatusChangeIds           = theIdCadena + ' ' + theContadorCambios + ',';
            unElementoBatchStatusChangeIds.value = unNuevoBatchStatusChangeIds;
            return true;
        }
        else {
        
            var unIdIndex = unosBatchStatusChangeIds.indexOf( theIdCadena + ' ');
            if ( unIdIndex >= 0) {
            
                var unNuevoBatchStatusChangeIds = '';
                if ( unIdIndex > 0) {
                    unLastEntryIndex = unosBatchStatusChangeIds.indexOf( ',', unIdIndex + 1);
                    if ( unLastEntryIndex >=0) {
                        unNuevoBatchStatusChangeIds = unosBatchStatusChangeIds.substring( 0, unIdIndex) + unosBatchStatusChangeIds.substring( unLastEntryIndex + 1);
                    }
                    else {
                        unNuevoBatchStatusChangeIds = unosBatchStatusChangeIds.substring( 0, unIdIndex) + unosBatchStatusChangeIds.substring( unIdIndex + theIdCadena.length + 1);
                    }
                }
                else {
                    unLastEntryIndex = unosBatchStatusChangeIds.indexOf( ',', 1);
                    if ( unLastEntryIndex >=0) {
                        unNuevoBatchStatusChangeIds = unosBatchStatusChangeIds.substring( unLastEntryIndex, 1); 
                    }
                    else {
                        unNuevoBatchStatusChangeIds = unosBatchStatusChangeIds.substring( theIdCadena.length + 1); 
                    }
                }
                unElementoBatchStatusChangeIds.value = unNuevoBatchStatusChangeIds;
                
                return false;
            }
            else {
            
                var unNuevoBatchStatusChangeIds = unosBatchStatusChangeIds +  theIdCadena + ' ' + theContadorCambios + ',';
                unElementoBatchStatusChangeIds.value = unNuevoBatchStatusChangeIds;
                
                return true;
            }
            return true;
            
        }
        return false;
    }
    finally {
        pLogUserInterfaceEvent_END( '               ->fTRAAddOrRemoveIdFromBatchStatusChange',  'idCadena: ' + theIdCadena + ' status: ' + theNewTranslationStatus);
    }  
}











function fTRARemoveIdFromBatchStatusChange( theIdCadena, theNewTranslationStatus) {  

    try {

        pLogUserInterfaceEvent_BEGIN( '               ->fTRARemoveIdFromBatchStatusChange',  'idCadena: ' + theIdCadena + ' status: ' + theNewTranslationStatus);

        if ( !theNewTranslationStatus) {
            return false;
        }

        if ( !theIdCadena) {
            return false;
        }
        
        var unElementoBatchStatusChangeIds   = document.getElementById( 'theBatch_' + theNewTranslationStatus);
        if ( !unElementoBatchStatusChangeIds) {
            return false;
        }
        
        var unosBatchStatusChangeIds = unElementoBatchStatusChangeIds.value;
        if ( unosBatchStatusChangeIds.length == 0) {
        
            return false;            
        }
       else {
       
            var unIdIndex = unosBatchStatusChangeIds.indexOf( theIdCadena + ' ');
            if ( unIdIndex >= 0) {
                
                var unNuevoBatchStatusChangeIds = '';
                if ( unIdIndex > 0) {
                    unLastEntryIndex = unosBatchStatusChangeIds.indexOf( ',', unIdIndex + 1);
                    if ( unLastEntryIndex >=0) {
                        unNuevoBatchStatusChangeIds = unosBatchStatusChangeIds.substring( 0, unIdIndex) + unosBatchStatusChangeIds.substring( unLastEntryIndex + 1);
                    }
                    else {
                        unNuevoBatchStatusChangeIds = unosBatchStatusChangeIds.substring( 0, unIdIndex) + unosBatchStatusChangeIds.substring( unIdIndex + theIdCadena.length + 1);
                    }
                }
                else {
                    unLastEntryIndex = unosBatchStatusChangeIds.indexOf( ',', 1);
                    if ( unLastEntryIndex >=0) {
                        unNuevoBatchStatusChangeIds = unosBatchStatusChangeIds.substring( unLastEntryIndex, 1); 
                    }
                    else {
                        unNuevoBatchStatusChangeIds = unosBatchStatusChangeIds.substring( theIdCadena.length + 1); 
                    }
                }

                unElementoBatchStatusChangeIds.value = unNuevoBatchStatusChangeIds;
                return true;
            }
            else {
                return false; 
            }
        }
        return false;
    
    }
    finally {
        pLogUserInterfaceEvent_END( '        ->fTRARemoveIdFromBatchStatusChange',  'idCadena: ' + theIdCadena + ' status: ' + theNewTranslationStatus);
    }    
}




/* marks all the strings to be changed in batch mode to the specified new status  */
function pTRAToggleAllBatchStatusChanges( theTranslationStatus) {

    if ( !theTranslationStatus) {
        return true;
    }

    var unElementAllBatchStatusChanges = document.getElementById( 'cid_TRAToggleAllBatchStatusChange_' + theTranslationStatus);
    if ( !unElementAllBatchStatusChanges) {
        return true;
    }
    var unNewValueForAllBatchStatusChanges = unElementAllBatchStatusChanges.checked;
    
    var unElementoBatchStatusChangeIds   = document.getElementById( 'theBatch_' + theTranslationStatus);
    if ( !unElementoBatchStatusChangeIds) {
        return true;
    }
    
    if ( !unNewValueForAllBatchStatusChanges) {
        unElementoBatchStatusChangeIds.value = ''
        for( var unIdCounter=1; unIdCounter < cTRAMaxRowsToLoopForRowElements; unIdCounter++) {
            if (!fTRA_SetBGColorEnBotonEstadoFilaNumero( unIdCounter, theTranslationStatus, '')) {
                break;
            }
        }
        return true;
    }
    var aToggleButton = null;
    if ( theTranslationStatus == 'Traducida') {
        aToggleButton = document.getElementById( 'cid_TRAToggleAllBatchStatusChange_Revisada');
        if ( aToggleButton) {
            aToggleButton.checked = false;
        }
        aToggleButton = document.getElementById( 'cid_TRAToggleAllBatchStatusChange_Definitiva');
        if ( aToggleButton) {
            aToggleButton.checked = false;
        }
    }
    if ( theTranslationStatus == 'Revisada') {
        aToggleButton = document.getElementById( 'cid_TRAToggleAllBatchStatusChange_Traducida');
        if ( aToggleButton) {
            aToggleButton.checked = false;
        }
        aToggleButton = document.getElementById( 'cid_TRAToggleAllBatchStatusChange_Definitiva');
        if ( aToggleButton) {
            aToggleButton.checked = false;
        }
    }
    if ( theTranslationStatus == 'Definitiva') {
        aToggleButton = document.getElementById( 'cid_TRAToggleAllBatchStatusChange_Traducida');
        if ( aToggleButton) {
            aToggleButton.checked = false;
        }
        aToggleButton = document.getElementById( 'cid_TRAToggleAllBatchStatusChange_Revisada');
        if ( aToggleButton) {
            aToggleButton.checked = false;
        }
    }


    var unosBatchStatusChangeIds = '';
     
    for( var unIdCounter=1; unIdCounter < cTRAMaxRowsToLoopForRowElements; unIdCounter++) {

        var unosDatosEnFila = fTRA_GetDatosEnFilaNumero( unIdCounter);
        if ( !unosDatosEnFila) {
            break;
        }
    
        var unFieldIdCadena	    = fTRA_FieldDatosEnFila( unosDatosEnFila, 'idCadena');
        if ( !unFieldIdCadena) {
            break;
        }
        var unIdCadena = unFieldIdCadena[ 1];
        if ( !unIdCadena ) {
            break;
        }
        
        var unFieldContadorCambios	    = fTRA_FieldDatosEnFila( unosDatosEnFila, 'contadorCambios');
        if ( !unFieldContadorCambios) {
            return false;
        }
        var unContadorCambios = unFieldContadorCambios[ 1];
        if ( !unContadorCambios ) {
            return false;
        }
        
        var unFieldTargetStatusChanges	    = fTRA_FieldDatosEnFila( unosDatosEnFila, 'targetStatusChanges');
        if ( !unFieldTargetStatusChanges) {
            break;
        }
        var unTargetStatusChanges = unFieldTargetStatusChanges[ 1];
        if ( !unTargetStatusChanges ) {
            break;
        }
        var unFieldEstadoTraduccion	    = fTRA_FieldDatosEnFila( unosDatosEnFila, 'estadoTraduccion');
        if ( !unFieldEstadoTraduccion) {
            break;
        }
        var unEstadoTraduccion = unFieldEstadoTraduccion[ 1];
        if ( !unEstadoTraduccion ) {
            break;
        }
       if( ( unTargetStatusChanges.indexOf( theTranslationStatus) >= 0) && ( !( unEstadoTraduccion == 'Pendiente' )) && ( !( unEstadoTraduccion == theTranslationStatus ))) {
            unosBatchStatusChangeIds = unosBatchStatusChangeIds + unIdCadena + ' ' + unContadorCambios + ',';   
            fTRARemoveIdFromOtherBatchStatusChanges(   unIdCadena, theTranslationStatus);
            
            fTRA_SetBGColorEnBotonesEstadoFilaNumero(  unIdCounter, '');  
            fTRA_SetBGColorEnBotonEstadoFilaNumero(    unIdCounter, theTranslationStatus, cTRABGColor_Translation_BatchStatusChangeRecorded);  
        }
    }  
    unElementoBatchStatusChangeIds.value = unosBatchStatusChangeIds;
    
}





function fTRABeforeUnload( theEvent) {

    if ( g_ajax_obj) {
        aNumQueueds = g_ajax_obj._dm_queue.length;
        
        if ( aNumQueueds) {
            
            return   aNumQueueds + ' requests queued and pending to be sent to the server.\nIf you click the OK button you shall abandon the page, and loose the pending changes.\nIf you click the Cancel button, you shall stay on the current page, and will give time for the queued requests to be sent to the server.';
        }
    }
}


window.onbeforeunload=fTRABeforeUnload;



/*
function fTRAUnload( theEvent) {

    if ( g_ajax_obj) {
        while( g_ajax_obj._dm_queue.length > 0) {
            g_ajax_obj.Dequeue_NoCallbacks();
        }
    }
}


window.onunload=fTRAUnload

*/

