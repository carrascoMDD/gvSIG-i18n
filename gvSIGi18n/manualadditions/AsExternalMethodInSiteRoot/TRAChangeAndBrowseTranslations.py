# -*- coding: utf-8 -*-
#
# File: TRAChangeAndBrowseTranslations.py
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


from codecs                 import lookup           as CODECS_Lookup
from codecs                 import EncodedFile      as CODECS_EncodedFile


from StringIO import StringIO


from Products.CMFCore.utils import getToolByName


from Products.gvSIGi18n.TRAElemento_Constants import *

from Products.gvSIGi18n.TRAElemento_Permission_Definitions import cBoundObject, cUseCase_BrowseTranslations, cUseCase_InvalidateStringTranslations
from Products.gvSIGi18n.TRAElemento_Permission_Definitions import cUseCase_TRATraduccionStateChange, cUseCase_TRATraduccionComment

from Products.gvSIGi18n.TRAElemento_Permission_Definitions import cStateChangeActionRoles



from Products.gvSIGi18n.TRAElemento_Constants import cNombreModuloNoEspecificadoLabel_MsgId

from Products.gvSIGi18n.TRAElemento_Constants import cInteractionMode_Default, cInteractionMode_Asynchronous, cInteractionMode_Synchronous
from Products.gvSIGi18n.TRAElemento_Constants import cAccion_Traducir, cAccion_InvalidarTraduccionesCadena
from Products.gvSIGi18n.TRAElemento_Constants import cRequestedChangeKind_IntentarTraducir, cRequestedChangeKind_Comentar
from Products.gvSIGi18n.TRAElemento_Constants import cRequestedChangeKind_HacerPendiente, cRequestedChangeKind_HacerTraducida
from Products.gvSIGi18n.TRAElemento_Constants import cRequestedChangeKind_HacerRevisada,  cRequestedChangeKind_HacerDefinitiva
from Products.gvSIGi18n.TRAElemento_Constants import cRequestedChangeKind_InvalidarTraduccionesCadena

cKeyAction_Traducir                 = "action_traducir"
cKeyAction_TraducirYAvanzar         = "action_traducirYAvanzar"
cKeyAction_Avanzar                  = "action_avanzar"
cKeyAction_NextTabIndex             = "action_nextTabIndex"

cKeyActions = [ cKeyAction_TraducirYAvanzar,  cKeyAction_Traducir, cKeyAction_Avanzar, cKeyAction_NextTabIndex]

cKeyAction_Default_CR  = cKeyAction_TraducirYAvanzar
cKeyAction_Default_Tab = cKeyAction_NextTabIndex


cSimboloCadenaLineWrapLen   = 32
                         

cCadenaTraducidaLineWrapLen = 32
      

cInformeEstadosVacio    = { 'Total': ['Total', 0, 0, ],  cEstadoTraduccionPendiente: [cEstadoTraduccionPendiente, 0, 0, ],  cEstadoTraduccionTraducida: [cEstadoTraduccionTraducida, 0, 0, ],  cEstadoTraduccionRevisada: [cEstadoTraduccionRevisada, 0, 0, ],  cEstadoTraduccionDefinitiva: [cEstadoTraduccionDefinitiva, 0, 0, ], }

cTodosEstados           = [ cEstadoTraduccionPendiente, cEstadoTraduccionTraducida, cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva,]
cBGColorsDict           = { cEstadoTraduccionPendiente : 'Red', cEstadoTraduccionTraducida : 'Yellow', cEstadoTraduccionRevisada  : 'Green', cEstadoTraduccionDefinitiva: 'Blue',}
cFGColorsDict           = { cEstadoTraduccionPendiente : 'Black', cEstadoTraduccionTraducida : 'Black', cEstadoTraduccionRevisada  : 'White', cEstadoTraduccionDefinitiva: 'White',}

cIconsDict              = { cEstadoTraduccionPendiente : 'tra_pendiente.gif', cEstadoTraduccionTraducida : 'tra_traducida.gif', cEstadoTraduccionRevisada  : 'tra_revisada.gif', cEstadoTraduccionDefinitiva: 'tra_definitiva.gif',}


cClasesFilas                  = [ 'even', 'odd',]
cOpcionesComparacionFechas   = [ 'Posterior', 'Anterior' , 'Igual', ];

cDesplazarUnaPagina  = 'Pagina'
cDesplazarUnRegistro = 'Registro'



"""HTTP request parameters used by the application.

"""
cInterestingRequestKeys = [
    'form_submit',         
    'theCodigoIdioma',
    'theCodigoIdiomaATraducir',
    'theCodigoIdiomaCursor',
    'theMayHaveChanged',            
    'theSimboloCadenaCursor',
    'theSimboloCadenaATraducir',    
    'theCadenaTraducida',           
    'Comentario',                   
    'theSimboloUltimaCadenaEnBloque',
    'theMostrarInforme',            
    'theMostrarFiltro',             
    'theMostrarLista',              
    'theMostrarHistoria',           
    'theTraduccionesPorPagina',     
    'theIdiomasReferencia',
    'Pendiente',                    
    'Traducida',                    
    'Revisada',                     
    'Definitiva', 
    'theEstadosAIncluir',
    'theSearchIdCadena',            
    'theSearchSimbolo',             
    'theSearchCadenaTraducida',     
    'theSearchNombreModulo',        
    'theSearchUsuarioTraductor',    
    'theSearchFechaTraduccion',     
    'theSearchFechaTraduccionCmp',  
    'theSearchFechaTraduccionInicial',     
    'theSearchFechaTraduccionFinal',     
    'theSearchUsuarioRevisor',      
    'theSearchFechaRevision',       
    'theSearchFechaRevisionCmp',    
    'theSearchFechaRevisionInicial',       
    'theSearchFechaRevisionFinal',       
    'theSearchFechaDefinitivo',     
    'theSearchFechaDefinitivoCmp',  
    'theSearchUsuarioCoordinador',      
    'theSearchFechaDefinitivoInicial',     
    'theSearchFechaDefinitivoFinal',     
    'theRenderFormSubmit',
    'theRenderRequest',
    'theRenderFullRequest',
    'theRenderTimes',
    'theRenderProfile',    
    'theRenderAsyncRequest',
]








cLanguageSizes_DefaultKey = 'default'

cLanguageSizes = {   
    cLanguageSizes_DefaultKey:  
                { 'display_font_size': 1, 'edit_font_size': 10, 'filter_field_size': 72, 'edit_chars_divider': 1, 'edit_chars_perline': 72, 'edit_line_height': 12, },
    'ml':       { 'display_font_size': 3, 'edit_font_size': 20, 'filter_field_size': 30, 'edit_chars_divider': 2, 'edit_chars_perline': 30, 'edit_line_height': 40, }, 
    'am':       { 'display_font_size': 3, 'edit_font_size': 20, 'filter_field_size': 30, 'edit_chars_divider': 2, 'edit_chars_perline': 30, 'edit_line_height': 40, },     
    'ar':       { 'display_font_size': 3, 'edit_font_size': 20, 'filter_field_size': 30, 'edit_chars_divider': 2, 'edit_chars_perline': 30, 'edit_line_height': 40, },     
    'as':       { 'display_font_size': 3, 'edit_font_size': 20, 'filter_field_size': 30, 'edit_chars_divider': 2, 'edit_chars_perline': 30, 'edit_line_height': 40, },    
    'mr':       { 'display_font_size': 3, 'edit_font_size': 20, 'filter_field_size': 30, 'edit_chars_divider': 2, 'edit_chars_perline': 30, 'edit_line_height': 40, }, 
    'ha':       { 'display_font_size': 3, 'edit_font_size': 20, 'filter_field_size': 30, 'edit_chars_divider': 2, 'edit_chars_perline': 30, 'edit_line_height': 40, },            
    'he':       { 'display_font_size': 2, 'edit_font_size': 14, 'filter_field_size': 40, 'edit_chars_divider': 2, 'edit_chars_perline': 40, 'edit_line_height': 30, },   
    'hi':       { 'display_font_size': 2, 'edit_font_size': 14, 'filter_field_size': 40, 'edit_chars_divider': 2, 'edit_chars_perline': 40, 'edit_line_height': 30, },   
    'ta':       { 'display_font_size': 2, 'edit_font_size': 14, 'filter_field_size': 40, 'edit_chars_divider': 2, 'edit_chars_perline': 40, 'edit_line_height': 30, },
    'ne':       { 'display_font_size': 3, 'edit_font_size': 20, 'filter_field_size': 30, 'edit_chars_divider': 2, 'edit_chars_perline': 30, 'edit_line_height': 40, }, 
    'te':       { 'display_font_size': 3, 'edit_font_size': 20, 'filter_field_size': 30, 'edit_chars_divider': 2, 'edit_chars_perline': 30, 'edit_line_height': 40, }, 
    'hy':       { 'display_font_size': 2, 'edit_font_size': 14, 'filter_field_size': 40, 'edit_chars_divider': 2, 'edit_chars_perline': 40, 'edit_line_height': 30, },         
    'th':       { 'display_font_size': 3, 'edit_font_size': 20, 'filter_field_size': 30, 'edit_chars_divider': 2, 'edit_chars_perline': 30, 'edit_line_height': 40, },
    'bn':       { 'display_font_size': 3, 'edit_font_size': 20, 'filter_field_size': 30, 'edit_chars_divider': 2, 'edit_chars_perline': 30, 'edit_line_height': 40, },
    'ti':       { 'display_font_size': 3, 'edit_font_size': 20, 'filter_field_size': 30, 'edit_chars_divider': 2, 'edit_chars_perline': 30, 'edit_line_height': 40, },
    'bo':       { 'display_font_size': 3, 'edit_font_size': 20, 'filter_field_size': 30, 'edit_chars_divider': 2, 'edit_chars_perline': 30, 'edit_line_height': 40, },     
    'or':       { 'display_font_size': 4, 'edit_font_size': 28, 'filter_field_size': 10, 'edit_chars_divider': 4, 'edit_chars_perline': 20, 'edit_line_height': 50, }, 
    'pa':       { 'display_font_size': 4, 'edit_font_size': 28, 'filter_field_size': 10, 'edit_chars_divider': 4, 'edit_chars_perline': 20, 'edit_line_height': 50, },          
    'ja':       { 'display_font_size': 4, 'edit_font_size': 28, 'filter_field_size': 10, 'edit_chars_divider': 4, 'edit_chars_perline': 20, 'edit_line_height': 50, },
    'ps':       { 'display_font_size': 3, 'edit_font_size': 20, 'filter_field_size': 30, 'edit_chars_divider': 2, 'edit_chars_perline': 30, 'edit_line_height': 40, },            
    'ka':       { 'display_font_size': 3, 'edit_font_size': 20, 'filter_field_size': 30, 'edit_chars_divider': 2, 'edit_chars_perline': 30, 'edit_line_height': 40, },   
    'dz':       { 'display_font_size': 3, 'edit_font_size': 20, 'filter_field_size': 30, 'edit_chars_divider': 2, 'edit_chars_perline': 30, 'edit_line_height': 40, },  
    'kk':       { 'display_font_size': 3, 'edit_font_size': 20, 'filter_field_size': 30, 'edit_chars_divider': 2, 'edit_chars_perline': 30, 'edit_line_height': 40, },   
    'ur':       { 'display_font_size': 3, 'edit_font_size': 20, 'filter_field_size': 30, 'edit_chars_divider': 2, 'edit_chars_perline': 30, 'edit_line_height': 40, },
    'kn':       { 'display_font_size': 3, 'edit_font_size': 20, 'filter_field_size': 30, 'edit_chars_divider': 2, 'edit_chars_perline': 30, 'edit_line_height': 40, },                    
    'ko':       { 'display_font_size': 3, 'edit_font_size': 20, 'filter_field_size': 30, 'edit_chars_divider': 2, 'edit_chars_perline': 30, 'edit_line_height': 40, }, 
    'sa':       { 'display_font_size': 4, 'edit_font_size': 28, 'filter_field_size': 10, 'edit_chars_divider': 4, 'edit_chars_perline': 20, 'edit_line_height': 50, },         
    'ks':       { 'display_font_size': 4, 'edit_font_size': 28, 'filter_field_size': 10, 'edit_chars_divider': 4, 'edit_chars_perline': 20, 'edit_line_height': 50, },                            
    'fa':       { 'display_font_size': 3, 'edit_font_size': 20, 'filter_field_size': 30, 'edit_chars_divider': 2, 'edit_chars_perline': 30, 'edit_line_height': 40, },
    'zh':       { 'display_font_size': 4, 'edit_font_size': 28, 'filter_field_size': 10, 'edit_chars_divider': 4, 'edit_chars_perline': 20, 'edit_line_height': 50, },                            
}                          





def TRASizesIdioma( theCodigoIdioma):
    if not theCodigoIdioma:
        return cLanguageSizes.get( cLanguageSizes_DefaultKey, None)
    
    unasSizes = cLanguageSizes.get( theCodigoIdioma, None)
    if unasSizes:
        return unasSizes

    unosCodigosIdioma = theCodigoIdioma.split( '-') 
    if len( unosCodigosIdioma) == 1:
        return cLanguageSizes.get( cLanguageSizes_DefaultKey, None)
     
    unCodigoIdioma = unosCodigosIdioma[ 0]
    unasSizes = cLanguageSizes.get( unCodigoIdioma, None)
    if unasSizes:
        return unasSizes
    
    return cLanguageSizes.get( cLanguageSizes_DefaultKey, None)



def fSizes_Display_FontSize( theCodigoIdioma):
    
    unasSizes = cLanguageSizes.get( theCodigoIdioma, None)
    if not unasSizes:
        unasSizes = cLanguageSizes.get( cLanguageSizes_DefaultKey, None)
        if not unasSizes:
            return 1
        

    return unasSizes.get( 'display_font_size', 1)





def fSizes_Edit_FontSize( theCodigoIdioma):
    
    unosLanguageDimensionFactors = cLanguageDimension_SpecialLanguageFactors.get( theCodigoIdioma, None)
    if not unosLanguageDimensionFactors:
        return cLanguageDimension_Edit_FontSize_default
    
    unLanguage_Edit_FontSize = unosLanguageDimensionFactors[ 1]
    
    return unLanguage_Edit_FontSize






def fNewVoidChangeTraslationsRequest():
    unResult = {
        'requested_change_kind':        '',
        'simbolo_cadena_a_traducir':    '',
        'codigo_idioma_a_traducir':     '',
        'cadena_traducida':             '',
        'comentario':                   '',
    }
    return unResult
    





def fNewVoidBrowseTraslationsRequest():
    unResult = {
    }
    return unResult
    





 
def fNewVoidChangeAndBrowseTraslationsRequest():
    unResult = {
        'change_parameters':        fNewVoidChangeTraslationsRequest(),
        'browse_parameters':        fNewVoidBrowseTraslationsRequest(),
    }
    return unResult
    




def TRAChangeAndBrowseTranslations( 
    theRequest, 
    theCatalogo, 
    thePermissionsCache     =None, 
    theRolesCache           =None,
    theParentExecutionRecord=None):
    """Main service for translations browsing, editing and state change.
    
    Entry point invoked from a template.
    
    """
    mfTranslateI18N     = theCatalogo.fTranslateI18N
    mfMillisecondsNow   = theCatalogo.fMillisecondsNow
    mfAsUnicode         = theCatalogo.fAsUnicode
    
    
    if not theRequest:
        return pEmptyPageContents(  
            theCatalogo, 
            mfTranslateI18N( 'gvSIGi18n', cResultCondition_MissingParameter, cResultCondition_MissingParameter + '-'),
            'theRequest',
            None
        )
     
    
    if not theRequest or not theCatalogo:
        return pEmptyPageContents(  
            theCatalogo, 
            mfTranslateI18N( 'gvSIGi18n', cResultCondition_MissingParameter, cResultCondition_MissingParameter + '-'),
            'theCatalogo',
            None
        )
    
        
    anOutput = StringIO()
    
    pRenderProfile    = theRequest.get( 'theRenderProfile', '') == 'on'
    
    unExecutionRecord = theCatalogo.fStartExecution( 'external method', 'TRAChangeAndBrowseTranslations', theParentExecutionRecord, False) 
    
    try:
            
            
        
        pStartTime = mfMillisecondsNow()
        
        
        # #################################################################
        """Initialize caches if not supplied by service caller

        """
        
        unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
        unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                
        
         
        
        
        # #################################################################
        """Cache some translations to be used in the rendering below

        """
        
        aTranslationsCache = {}
        pInitTranslationsCache( 
            theCatalogo, 
            aTranslationsCache
        )
       
        
                
        
        # ################################################################
        """Retrieve information of all existing and visible TRAIdioma.
        
        ACV OJO 200904010009 Should come with the service response....
        
        """
    

         
        
        
        # ################################################################
        """Retrieve Request parameter values.
        
        """
             

        pFormSubmit                     = theRequest.get( 'form_submit',                    '')
        pGoTo                           = theRequest.get( 'theGoTo',                        '')
        pMayHaveChanged                 = theRequest.get( 'theMayHaveChanged',              '0')
        pMostrarInforme                 = theRequest.get( 'theMostrarInforme',              '') == 'on'
        pMostrarLista                   = theRequest.get( 'theMostrarLista',                '') == 'on'
        pMostrarHistoria                = theRequest.get( 'theMostrarHistoria',             '') == 'on'        
        pMostrarDetallesTraduccion      = theRequest.get( 'theMostrarDetallesTraduccion',   '') == 'on'        
        pTraduccionesPorPagina          = theRequest.get( 'theTraduccionesPorPagina',       str( theCatalogo.fTraduccionesPorPaginaPorDefecto()))    
        pIncludePendiente               = theRequest.get( cEstadoTraduccionPendiente,       '0')
        pIncludeTraducida               = theRequest.get( cEstadoTraduccionTraducida,       '0')
        pIncludeRevisada                = theRequest.get( cEstadoTraduccionRevisada,        '0')
        pIncludeDefinitiva              = theRequest.get( cEstadoTraduccionDefinitiva,      '0')
        pIdiomasReferencia              = theRequest.get( 'theIdiomasReferencia',           []) or []
        pCodigoIdiomaATraducir          = theRequest.get( 'theCodigoIdiomaATraducir',       '')
        pCodigoIdiomaCursor             = theRequest.get( 'theCodigoIdiomaCursor',          '')
        pSimboloCadenaCursor            = theRequest.get( 'theSimboloCadenaCursor',         '')
        pSimboloCadenaATraducir         = theRequest.get( 'theSimboloCadenaATraducir',      '')
        pSimboloUltimaCadenaEnBloque    = theRequest.get( 'theSimboloUltimaCadenaEnBloque', '')
        pEstadosAIncluir                = theRequest.get( 'theEstadosAIncluir',             []) or []
        pCadenaTraducida                = theRequest.get( 'theCadenaTraducida',             '')
        pComentario                     = theRequest.get( 'Comentario',                     '')        
        pInteractionMode                = theRequest.get( 'theInteractionMode',             theCatalogo.fModoInteraccionPorDefecto())
        pHideStateTransitionColumns     = theRequest.get( 'theHideStateTransitionColumns',  '') == 'on'
        pBatchStatusChanges             = theRequest.get( 'theBatchStatusChanges',       '') == 'on'
        pRenderFormSubmit               = theRequest.get( 'theRenderFormSubmit',            '') == 'on'
        pRenderRequest                  = theRequest.get( 'theRenderRequest',               '') == 'on'
        pRenderFullRequest              = theRequest.get( 'theRenderFullRequest',           '') == 'on'
        pRenderTimes                    = theRequest.get( 'theRenderTimes',                 '') == 'on'
        pRenderAsyncRequest             = theRequest.get( 'theRenderAsyncRequest',          '') == 'on'
        pRenderUserInterfaceEvents      = theRequest.get( 'theRenderUserInterfaceEvents',   '') == 'on'

        pRequestedNuevoEstadoTraduccion = theRequest.get( 'theNuevoEstadoTraduccion',       '') 
     
        pEditorKeyCRAction               = theRequest.get( 'theKeyAction_CR',               cKeyAction_Default_CR)
        pEditorKeyTabAction              = theRequest.get( 'theKeyAction_Tab',              cKeyAction_Default_Tab)

        pBatch_Traducida                 = theRequest.get( 'theBatch_Traducida',       '')
        pBatchIds_Traducida              = ( pBatch_Traducida and pBatch_Traducida.split( ' '))   or []
        pBatch_Revisada                  = theRequest.get( 'theBatch_Revisada',        '')
        pBatchIds_Revisada               = ( pBatch_Revisada and pBatch_Revisada.split( ' '))     or []
        pBatch_Definitiva                = theRequest.get( 'theBatch_Definitiva',      '')
        pBatchIds_Definitiva             = ( pBatch_Definitiva and pBatch_Definitiva.split( ' ')) or []
        
        
        
        # ################################################################
        """Capture Request dump strings
        
        """
        aRequestDumpString      = ''
        aFullRequestDumpString  = ''
        if pRenderRequest or pRenderFullRequest:
            aRequestDumpString, aFullRequestDumpString = pRequestStrings( theCatalogo, theRequest, pRenderRequest, pRenderFullRequest, aTranslationsCache) 
        
             
            
        
    
        
        
       # ################################################################
        """Prepare service request parameters for change and browse phases.
        
        """
        
        pServiceRequestParameters = fNewVoidChangeAndBrowseTraslationsRequest()
    

        
        # #################################################################
        """Prepare service request parameters for change 
        
        """
            
        if pMayHaveChanged:
            
            if pBatchIds_Traducida or pBatchIds_Revisada or pBatchIds_Definitiva:
                aRequestedChangeKind = cRequestedChangeKind_BatchCambioEstado
            
            elif pRequestedNuevoEstadoTraduccion in cTodosEstados:
                
                if pRequestedNuevoEstadoTraduccion == cEstadoTraduccionPendiente:
                    aRequestedChangeKind = cRequestedChangeKind_HacerPendiente
                    
                elif pRequestedNuevoEstadoTraduccion == cEstadoTraduccionTraducida:
                    aRequestedChangeKind = cRequestedChangeKind_HacerTraducida
                    
                elif pRequestedNuevoEstadoTraduccion == cEstadoTraduccionRevisada:
                    aRequestedChangeKind = cRequestedChangeKind_HacerRevisada
                                        
                elif pRequestedNuevoEstadoTraduccion == cEstadoTraduccionDefinitiva:
                    aRequestedChangeKind = cRequestedChangeKind_HacerDefinitiva
                
            elif pRequestedNuevoEstadoTraduccion == cAccion_InvalidarTraduccionesCadena:
                aRequestedChangeKind = cRequestedChangeKind_InvalidarTraduccionesCadena

            elif pFormSubmit == cAccion_InvalidarTraduccionesCadena:
                aRequestedChangeKind = cRequestedChangeKind_InvalidarTraduccionesCadena

            elif pFormSubmit == cAccion_Traducir:
                aRequestedChangeKind = cRequestedChangeKind_IntentarTraducir
                
            elif pFormSubmit == aTranslationsCache[ 'gvSIGi18n_TranslationAction_Grabar']:
                aRequestedChangeKind = cRequestedChangeKind_IntentarTraducir
                
            elif pFormSubmit == aTranslationsCache[ 'gvSIGi18n_comentar_action_label']:
                aRequestedChangeKind = cRequestedChangeKind_Comentar
                
            elif pFormSubmit == cEstadoTraduccionPendiente:
                aRequestedChangeKind = cRequestedChangeKind_HacerPendiente
                
            elif pFormSubmit == aTranslationsCache[ 'gvSIGi18n_TranslationAction_Borrar']:
                aRequestedChangeKind = cRequestedChangeKind_HacerTraducida
                
            elif pFormSubmit == aTranslationsCache[ 'gvSIGi18n_TranslationAction_Abrir']:
                aRequestedChangeKind = cRequestedChangeKind_HacerTraducida
                
            elif pFormSubmit == cEstadoTraduccionTraducida:
                aRequestedChangeKind = cRequestedChangeKind_HacerTraducida
                
            elif pFormSubmit == cEstadoTraduccionRevisada:
                aRequestedChangeKind = cRequestedChangeKind_HacerRevisada
                
            elif pFormSubmit == cEstadoTraduccionDefinitiva:
                aRequestedChangeKind = cRequestedChangeKind_HacerDefinitiva
            else:
                aRequestedChangeKind = cRequestedChangeKind_IntentarTraducir

      
      
                
            #elif pFormSubmit == aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Pendiente']:
                #aRequestedChangeKind = cRequestedChangeKind_HacerPendiente
            #elif pFormSubmit == aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Traducida']:
                #aRequestedChangeKind = cRequestedChangeKind_HacerTraducida
            #elif pFormSubmit == aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Revisada']:
                #aRequestedChangeKind = cRequestedChangeKind_HacerRevisada
            #elif pFormSubmit == aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Definitiva']:
                #aRequestedChangeKind = cRequestedChangeKind_HacerDefinitiva
                
            #elif pFormSubmit == aTranslationsCache[ 'gvSIGi18n_TranslationAction_Grabar']:
                #aRequestedChangeKind = cRequestedChangeKind_IntentarTraducir
            #elif pFormSubmit == aTranslationsCache[ 'gvSIGi18n_TranslationAction_Borrar']:
                #aRequestedChangeKind = cRequestedChangeKind_HacerPendiente
            #elif pFormSubmit == aTranslationsCache[ 'gvSIGi18n_TranslationAction_Abrir']:
                #aRequestedChangeKind = cRequestedChangeKind_HacerTraducida
            #elif pFormSubmit == aTranslationsCache[ 'gvSIGi18n_TranslationAction_Revisar']:
                #aRequestedChangeKind = cRequestedChangeKind_HacerRevisada
            #elif pFormSubmit == aTranslationsCache[ 'gvSIGi18n_TranslationAction_Bloquear']:
                #aRequestedChangeKind = cRequestedChangeKind_HacerDefinitiva
      
            pServiceRequestParameters[ 'change_parameters'].update( {
                'requested_change_kind':        aRequestedChangeKind,
                'simbolo_cadena_a_traducir':    pSimboloCadenaATraducir,
                'codigo_idioma_a_traducir':     pCodigoIdiomaATraducir,
                'cadena_traducida':             pCadenaTraducida,
                'comentario':                   pComentario,
                'batch_ids_traducida':          pBatchIds_Traducida,
                'batch_ids_revisada':           pBatchIds_Revisada,
                'batch_ids_definitiva':         pBatchIds_Definitiva,                
            })
            
            
        # #################################################################
        """Prepare service request parameters for browse 
        
        """
        
        
        
        # ################################################################
        """If request parameters for languages and status are not already extracted from the request a list, make lists from them.
        
        """
         
        if pIdiomasReferencia:
            if not ( pIdiomasReferencia.__class__.__name__ == 'list'):
                pIdiomasReferencia = [ pIdiomasReferencia,]
        if not pCodigoIdiomaCursor in pIdiomasReferencia:
            pIdiomasReferencia.append( pCodigoIdiomaCursor)
            pIdiomasReferencia.sort()
        if pEstadosAIncluir:
            if not ( pEstadosAIncluir.__class__.__name__ == 'list'):
                pEstadosAIncluir = [ pEstadosAIncluir,]
        pEstadosAIncluir = [ unEstado for unEstado in pEstadosAIncluir if unEstado in cTodosEstados]
        
        
        

                
            
                
        # ################################################################
        """Analyse Request Parameters for Navigation 
        
        """
     
        pModoDesplazamiento = ''
        if ( pFormSubmit == 'GoToFirst')        or (pFormSubmit == aTranslationsCache[ 'gvSIGi18n_traducciones_iraprimero_label']) or ( pFormSubmit.find( 'alt="%s"' % aTranslationsCache[ 'gvSIGi18n_traducciones_iraprimero_label']) >= 0):
            pModoDesplazamiento = 'First'
        elif ( pFormSubmit == 'GoToPrevious')   or (pFormSubmit == aTranslationsCache[ 'gvSIGi18n_traducciones_iraanterior_label']) or ( pFormSubmit.find( 'alt="%s"' % aTranslationsCache[ 'gvSIGi18n_traducciones_iraanterior_label']) >= 0):
            pModoDesplazamiento = 'Previous'
        elif ( pFormSubmit == 'GoToNext')       or  (pFormSubmit == aTranslationsCache[ 'gvSIGi18n_traducciones_bloquesiguiente_label']) or (pFormSubmit == aTranslationsCache[ 'gvSIGi18n_traducciones_irasiguiente_label']) or ( pFormSubmit.find( 'alt="%s"' % aTranslationsCache[ 'gvSIGi18n_traducciones_irasiguiente_label']) >= 0):
            pModoDesplazamiento = 'Next'
        elif ( pFormSubmit == 'GoToLast')       or (pFormSubmit == aTranslationsCache[ 'gvSIGi18n_traducciones_iraultimo_label']) or ( pFormSubmit.find( 'alt="%s"' % aTranslationsCache[ 'gvSIGi18n_traducciones_iraultimo_label']) >= 0):
            pModoDesplazamiento = 'Last'
        elif ( pGoTo == 'GoToFirst'):
            pModoDesplazamiento = 'First'
        elif ( pGoTo == 'GoToPrevious'):
            pModoDesplazamiento = 'Previous'
        elif ( pGoTo == 'GoToNext'):
            pModoDesplazamiento = 'Next'
        elif ( pGoTo == 'GoToLast'):
            pModoDesplazamiento = 'Last'
            
            
    
            
          
    
    
     
        # #################################################################
        """Set the TRACadena.simbolo to be used to re-position the cursor
        Use the first record (the one to be edited if the editor opens)
        in case of no displacement, or Prev (First or Last do not care)
        Use the last record, for Next displacement when the editor is not used

        """
        if pModoDesplazamiento == 'Next':  #  and not pMostrarEditor:
            pSimboloCadenaCursor = pSimboloUltimaCadenaEnBloque
    
    
            
            
        # #################################################################
        """Set the desplazarUnRegistroOPagina
        
        """
        
        pDesplazarUnRegistroOPagina = cDesplazarUnaPagina
        #if pMostrarEditor:
            #pDesplazarUnRegistroOPagina = cDesplazarUnRegistro
    
        #if pMostrarEditor and not pMostrarLista:
            #pTraduccionesPorPagina = '1'
                
                
                
            
            
                
     
        # #################################################################
        """Compose browse parameters, including cursor and filter and section information
        
        """
        
        pSearchParameters = { 
            'idioma':                       pCodigoIdiomaCursor, 
            'idCadena':                     theRequest.get( 'theSearchIdCadena',               ''), 
            'simboloCadenaCursor':          pSimboloCadenaCursor, 
            'modoDesplazamiento':           pModoDesplazamiento, 
            'desplazarUnRegistroOPagina':   pDesplazarUnRegistroOPagina,
            'traduccionesPorPagina' :       pTraduccionesPorPagina, 
            'idiomasReferencia':            pIdiomasReferencia,         
            'estadosAIncluir':              pEstadosAIncluir, 
            'simbolo':                      theRequest.get( 'theSearchSimbolo',                ''),
            'cadenaTraducida':              theRequest.get( 'theSearchCadenaTraducida',        ''),
            'nombresModulos':               theRequest.get( 'theSearchNombresModulos',         ''),
            'usuarioCreador':               theRequest.get( 'theSearchUsuarioCreador',         ''), 
            'fechaCreacionInicial':         theRequest.get( 'theSearchFechaCreacionInicial',   ''), 
            'fechaCreacionFinal':           theRequest.get( 'theSearchFechaCreacionFinal',     ''), 
            'usuarioTraductor':             theRequest.get( 'theSearchUsuarioTraductor',       ''), 
            'fechaTraduccion':              theRequest.get( 'theSearchFechaTraduccion',        ''), 
            'fechaTraduccionInicial':       theRequest.get( 'theSearchFechaTraduccionInicial', ''), 
            'fechaTraduccionFinal':         theRequest.get( 'theSearchFechaTraduccionFinal',   ''), 
            'usuarioRevisor':               theRequest.get( 'theSearchUsuarioRevisor',         ''),  
            'fechaRevision':                theRequest.get( 'theSearchFechaRevision',          ''),  
            'fechaRevisionInicial':         theRequest.get( 'theSearchFechaRevisionInicial',   ''),  
            'fechaRevisionFinal':           theRequest.get( 'theSearchFechaRevisionFinal',     ''),  
            'fechaDefinitivo':              theRequest.get( 'theSearchFechaDefinitivo',        ''),  
            'fechaDefinitivoInicial':       theRequest.get( 'theSearchFechaDefinitivoInicial', ''),  
            'fechaDefinitivoFinal':         theRequest.get( 'theSearchFechaDefinitivoFinal',   ''),  
            'usuarioCoordinador':           theRequest.get( 'theSearchUsuarioCoordinador',     ''),  
        }
                  
        
        pServiceRequestParameters[ 'browse_parameters'].update( {
            'search_parameters':            pSearchParameters,
            'include_summary':              pMostrarInforme,
        })
            
        
        
        

        
        
        
        # #################################################################
        """SERVICE REQUEST : CHANGE STATE ACTION and RETRIEVAL
        
        Process TRATraduccion state change action request.   
        Retrieve TRATraducciones in the current TRAIdioma, applying filter parameters, if any
        will return summary information only if so specified

        """
        
        pServiceResponse = theCatalogo.fChangeAndBrowseTranslations( pServiceRequestParameters, unPermissionsCache, unRolesCache, unExecutionRecord)
        
        pServiceSuccess  = pServiceResponse and pServiceResponse.get( 'success', False)     
  
        
      
        
        # #################################################################
        """Extract and process general information like the dictionary of language names and flags
        
        """
        
        pLanguagesNamesAndFlags  = pServiceResponse.get( 'languages_names_and_flags', {})
        
        
        
        
        
        
        
        # #################################################################
        """Extract and process change results
        
        """
        
        pChangeResult    = pServiceResponse and pServiceResponse.get( 'change_result', {}) 
        
        pChangeDuration  = pChangeResult and pChangeResult.get( 'duration', False)
        
        pChangeSuccess   = pServiceSuccess and pChangeResult and pChangeResult.get( 'success', False)

        unHayCambio      = pChangeSuccess and pChangeResult and pChangeResult.get( 'changed', False)
        
        
         
        
        # #################################################################
        """Extract and process retrieved browse results
        
        """
        
        pBrowseResult        = pServiceResponse and  pServiceResponse.get( 'browse_result', {})  
 
        pBrowseDuration      = pBrowseResult and pBrowseResult and pBrowseResult.get( 'duration', False)
        
        pBrowseSuccess       = pServiceSuccess and pBrowseResult and pBrowseResult.get( 'success', False)
        pBrowseCondition     = pBrowseResult and pBrowseResult.get( 'condition', '')
        pBrowseException     = pBrowseResult and pBrowseResult.get( 'exception', '')
         
        
        
        
        
        if not pBrowseSuccess:
            
            if pBrowseCondition == cResultCondition_Internal_Exception:
                return pEmptyPageContents( theCatalogo,  
                    mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_BrowseTranslationsFailure_Exception_msg', 'An exception occurred while retrieving translations.-' ),
                    mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_BrowseTranslationsFailure_MakeSureYouAreLoggedOrContactSiteAdministrator_msg', \
                        'Please make sure that you are properly logged as a user authorized for translations access, or contact your site administrator.-' ),
                    aTranslationsCache
                )
            else:
                return pEmptyPageContents( theCatalogo,  
                    mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_BrowseTranslationsFailure_Condition_msg', \
                         'Translations retrieval failed with condition:-' ),
                    mfTranslateI18N( 'gvSIGi18n', pBrowseCondition, pBrowseCondition + '-' ),
                    aTranslationsCache
                 )
         
        
        pDatosTraducciones                  = pBrowseResult.get( 'datosTraducciones',           [])
        pEstadosIncluidos                   = pBrowseResult.get( 'estadosIncluidos',            [])
        pInformeEstadosTodasCadenas         = pBrowseResult.get( 'informeEstadosTodasCadenas',  cInformeEstadosVacio)
        pInformeEstadosFiltrados            = pBrowseResult.get( 'informeEstadosFiltrados',     cInformeEstadosVacio)
        pDictsTraduccionesIdiomasReferencia = pBrowseResult.get( 'dictsTraduccionesIdiomasReferencia',   { })
        pTraduccionesPorPagina              = pBrowseResult.get( 'traduccionesPorPagina',       theCatalogo.fTraduccionesPorPaginaPorDefecto())
        pUseCaseQueryResults                = pBrowseResult.get( 'use_case_query_results',      [])
        
        pAllowedStateTransitions            = pBrowseResult.get( 'allowed_state_transitions',   {}) 
        pAllTargetStatusChanges             = pBrowseResult.get( 'all_target_state_changes',    set()) 
        
        pAllowInvalidateStringTranslations = pBrowseResult.get( 'allow_invalidate_string_translations',   []) 

        pWritePermission                    = pBrowseResult.get( 'write_permission',            False) 
        
        
        pShowStateTransitionColumnsOption = len( set( [ cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva,]).intersection( pAllTargetStatusChanges)) > 0
        pHideStateTransitionColumns       = ( not pShowStateTransitionColumnsOption) or pHideStateTransitionColumns
        
        pShowBatchStatusChangesOption = pShowStateTransitionColumnsOption
        pBatchStatusChanges           = pShowBatchStatusChangesOption and pBatchStatusChanges
        
        pCommentUseCaseQueryResult          = None        
        for aUseCaseQueryResult in pUseCaseQueryResults:
            if aUseCaseQueryResult.get( 'use_case_name', '') == cUseCase_TRATraduccionComment:
                pCommentUseCaseQueryResult = aUseCaseQueryResult
                break
            
        pBrowseTranslationsUseCaseQueryResult          = None        
        for aUseCaseQueryResult in pUseCaseQueryResults:
            if aUseCaseQueryResult.get( 'use_case_name', '') == cUseCase_BrowseTranslations:
                pBrowseTranslationsUseCaseQueryResult = aUseCaseQueryResult
                break

 
        if not pBrowseTranslationsUseCaseQueryResult or not pBrowseTranslationsUseCaseQueryResult[ 'success']:
            return pEmptyPageContents( theCatalogo,  mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_AccessFailedAndPromptYouHavePermission_label',   \
                'Access to the translations catalog failed.\nDo you have permission ?\nIf so, you may want to login first.-' ),
                '',
                aTranslationsCache
            )
    
        # Redundant with pAllowInvalidateStringTranslations
        #pCanInvalidateStringTranslations = False
        #for aUseCaseQueryResult in pUseCaseQueryResults:
            #if aUseCaseQueryResult and aUseCaseQueryResult.get( 'use_case_name', '') == cUseCase_InvalidateStringTranslations:
                #if aUseCaseQueryResult.get( 'success', False):
                    #pCanInvalidateStringTranslations = True
        
        
        
       # #################################################################
        """Verify and gather security access to Languages
        
        """
        
        unosIdiomasAccesibles = pBrowseTranslationsUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'languages', {}).get( 'accepted_final_objects', [])
        if not unosIdiomasAccesibles:
            return pEmptyPageContents( theCatalogo,  mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_NoAccessibleLanguages_label', \
                'There are no languages available or accessible.-\nDo you have permission ?\nIf so, you may want to login first.-' ),
                '',
                aTranslationsCache
            )
               
        
        unIdiomaCursor          = None
        unosCodigosIdiomasEInternacionales    = [ ]
        
        for unIdioma in unosIdiomasAccesibles:
            unCodigoIdioma      = unIdioma.getCodigoIdiomaEnGvSIG()
            unosCodigosIdiomasEInternacionales.append( [ unCodigoIdioma, unIdioma.getCodigoInternacionalDeIdioma(),])
            if unCodigoIdioma == pCodigoIdiomaCursor:
                unIdiomaCursor          = unIdioma
                
        if not unIdiomaCursor:
            return pEmptyPageContents( theCatalogo,  
                'language: %s %s' % ( 
                    mfAsUnicode( pCodigoIdiomaCursor),
                    mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_LanguageNotAccessible_label', \
                        'You are not allowed to access the selected language.-\nDo you have permission ?\nIf so, you may want to login first.-' ),
                ),
                '',
                aTranslationsCache
            )
        
        pTodosCodigosIdiomasEInternacionales = sorted( unosCodigosIdiomasEInternacionales, lambda unCEI, otroCEI: cmp( unCEI[ 0], otroCEI[ 0]))
        
        pTodosCodigosIdiomas = [ unCEI[ 0] for unCEI in pTodosCodigosIdiomasEInternacionales]
        
        
        
        
        
        
        # #################################################################
        """Verify and gather security access to Modules
        
        """
             
        unosModulosAccesibles = pBrowseTranslationsUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'modules', {}).get( 'accepted_final_objects', [])
 
        pTodosNombresModulos = [ ]
        if unosModulosAccesibles:
            pTodosNombresModulos = sorted( [ unModulo.Title() for unModulo in unosModulosAccesibles])
            
            
            
            
        
                            
            
            

          
            
            
        # #################################################################
        """SECTION: Select the first  TRATraduccion search result for cursor,  edition and optionally history retrieval and display
        
        """
         
        pDatosTraduccionSeleccionada  = { }
        pSimboloCadenaCursor          = ''
        pSimboloCadenaATraducir       = ''
        pSimboloUltimaCadenaEnBloque  = ''  
        pTargetStatusChanges           = set()
        pCanComment                   = False
        pRegistrosHistoria            = {}
        
        pSimboloCadenaATraducir       = '' # To be set by list rendering method with the symbol of the first translation it finds worth for edition, currently just the first one
        
        
        
        
        if pDatosTraducciones and len( pDatosTraducciones) > 0:
            
            pDatosTraduccionSeleccionada  = pDatosTraducciones[ 0]
            pSimboloCadenaCursor          = pDatosTraduccionSeleccionada[ 'getSimbolo']
            pSimboloUltimaCadenaEnBloque  = pDatosTraducciones[ len( pDatosTraducciones) - 1][ 'getSimbolo']
            
            pTargetStatusChanges           = pAllowedStateTransitions.get( pDatosTraduccionSeleccionada[ 'getEstadoTraduccion'], set())
            pCanComment                   = pCommentUseCaseQueryResult and pCommentUseCaseQueryResult.get( 'success', False)
                          
            if pMostrarHistoria:
                unaTraduccionSeleccionada       = pDatosTraduccionSeleccionada.getObject()
                if unaTraduccionSeleccionada:
                    pRegistrosHistoria = unaTraduccionSeleccionada.getRegistrosHistoria()                
        
            
            
            
            
    
            

        # #################################################################
        """RENDERING of the various sections of the translations browser/editor
            
        Including:
        Summary report by status: total and filtered translations.
        Filter criteria editor.
        Selected Translation editor.
        History of the selected Translation.
        List of matching translations.
        
        """
        
        
        # #################################################################
        """Open Page
        
        """
        anOutput.write( u"""     
                        
            <!-- #################################################################
            PAGE WITH CONTENT
            ################################################################# -->
        """)
        
        
                        
        
        # #################################################################
        """Render internationalized cosntants for Javascript dialogs
        
        """
        anOutput.write( u"""     
                        
            <!-- #################################################################
            SECTION: Internationalized constants 
            ################################################################# -->
            <font style="font-color=white"> 
                <span id="cTRAId_ConfirmInvalidateStringTranslationsMsg" class="TRAstyle_NoDisplay">%(gvSIGi18n_ConfirmInvalidateStringTranslationsMsg)s</span>
                <span id="cTRAId_ReallyInvalidateStringTranslationsMsg" class="TRAstyle_NoDisplay">%(gvSIGi18n_ReallyInvalidateStringTranslationsMsg)s</span>
            </font>
            \n""" % { 
            'gvSIGi18n_ConfirmInvalidateStringTranslationsMsg': aTranslationsCache[ 'gvSIGi18n_ConfirmInvalidateStringTranslationsMsg'],
            'gvSIGi18n_ReallyInvalidateStringTranslationsMsg': aTranslationsCache[ 'gvSIGi18n_ReallyInvalidateStringTranslationsMsg'],
            }
        )
                    
        
           
        
              
        # #################################################################
        """Open FORM element
        
        """
        anOutput.write( u"""     
                        
            
            
            <!-- #################################################################
            PAGE WITH CONTENT
            ################################################################# -->

            
            <!-- #################################################################
            SECTION: Begin Form 
            ################################################################# -->
             
            <form id="TranslationFormId" method="POST">
            \n"""
        )
                    
                    
               
        pRenderScripts( 
            anOutput, 
            theCatalogo,
        )   
        
        
        pRenderStyles(            
            anOutput, 
            theCatalogo, 
        ) 
                
            
            
            
        anOutput.write( u"""                 
      
            <!-- #################################################################
            SECTION: Hidden fields to maintain and communicate whether the form may have hanged
            ################################################################# -->
                     

            <input type="hidden" name="theMayHaveChanged"               id="theMayHaveChanged"              value="%(can_change)s" /> 
            \n""" % { 
            'can_change':  (( pTargetStatusChanges or pCanComment) and '1') or '0', 
        } )
     
                        
       
      

        pRenderCabecera( 
            anOutput, 
            theCatalogo, 
            pBrowseResult,
            pLanguagesNamesAndFlags, 
            pTodosCodigosIdiomas, 
            pCodigoIdiomaCursor, 
            aTranslationsCache
        )
        # anOutput.write( u"""\n<br/>\n""" )  
        
                
          
        
         
        pRenderCollapsibleSelectorIdiomasReferencia( 
            anOutput, 
            theCatalogo, 
            pLanguagesNamesAndFlags, 
            pTodosCodigosIdiomasEInternacionales, 
            pIdiomasReferencia, 
            aTranslationsCache
        )

        
        
        pRenderCollapsibleControlPresentacion( 
            anOutput, 
            theCatalogo, 
            pTraduccionesPorPagina,
            pInteractionMode,
            pMostrarInforme, 
            pMostrarLista, 
            pMostrarDetallesTraduccion,
            pMostrarHistoria, 
            pShowStateTransitionColumnsOption,
            pHideStateTransitionColumns,
            pShowBatchStatusChangesOption,
            pBatchStatusChanges,            
            pCanComment, 
            pEditorKeyCRAction,
            pEditorKeyTabAction,
            pRenderFormSubmit, 
            pRenderRequest, 
            pRenderFullRequest, 
            pRenderTimes, 
            pRenderProfile, 
            pRenderAsyncRequest,  
            pRenderUserInterfaceEvents,
            aTranslationsCache
        )


        
        pRenderCollapsibleFiltro( 
            anOutput, 
            theCatalogo, 
            pCodigoIdiomaCursor, 
            pTodosNombresModulos, 
            pEstadosIncluidos, 
            pSearchParameters, 
            aTranslationsCache
        )
        
          
        if pMostrarInforme:
            pRenderCollapsibleInforme( 
                anOutput, 
                theCatalogo, 
                pEstadosIncluidos, 
                pInformeEstadosTodasCadenas, 
                pInformeEstadosFiltrados, 
                aTranslationsCache
            )
        
        
                                               
        if pMostrarHistoria :
            pRenderCollapsibleHistory( 
                anOutput, 
                theCatalogo, 
                pCodigoIdiomaCursor, 
                pRegistrosHistoria, 
                aTranslationsCache
            )
                 
            
            
                
        if pMostrarLista :
            unSimboloCadenaATraducirHolder = [ '',]
            pRenderCollapsibleList( 
                anOutput, 
                theCatalogo, 
                pBrowseResult,
                pCodigoIdiomaCursor, 
                pIdiomasReferencia, 
                pDatosTraducciones, 
                pDictsTraduccionesIdiomasReferencia, 
                pLanguagesNamesAndFlags, 
                pWritePermission,
                pAllowedStateTransitions,
                pAllTargetStatusChanges,
                pAllowInvalidateStringTranslations,
                unSimboloCadenaATraducirHolder,
                pMostrarHistoria,
                pHideStateTransitionColumns,
                pBatchStatusChanges,
                aTranslationsCache,
                unRolesCache,
            )
            if unSimboloCadenaATraducirHolder and unSimboloCadenaATraducirHolder[ 0]:
                pSimboloCadenaATraducir = unSimboloCadenaATraducirHolder[ 0]
       
             
       
            
                
                
        anOutput.write( u"""                 
            <!-- #################################################################
            SECTION: Hidden fields to maintain and communicate current translation and cursor,
                     and user permission to invalidate string translations
            ################################################################# -->
               
            <input type="hidden" name="theCodigoIdiomaATraducir"        id="theCodigoIdiomaATraducir"       value="%(pCodigoIdiomaCursor)s"/> 
            <input type="hidden" name="theSimboloCadenaATraducir"       id="theSimboloCadenaATraducir"      value="%(pSimboloCadenaATraducir)s" /> 
            <input type="hidden" name="theSimboloCadenaCursor"          id="theSimboloCadenaCursor"         value="%(pSimboloCadenaCursor)s" /> 
            <input type="hidden" name="theSimboloUltimaCadenaEnBloque"  id="theSimboloUltimaCadenaEnBloque" value="%(pSimboloUltimaCadenaEnBloque)s" /> 
            
            
            \n""" % { 
            'pSimboloUltimaCadenaEnBloque': mfAsUnicode( pSimboloUltimaCadenaEnBloque), 
            'pSimboloCadenaATraducir':      mfAsUnicode( pSimboloCadenaATraducir), 
            'pSimboloCadenaCursor':         mfAsUnicode( pSimboloCadenaCursor),
            'pCodigoIdiomaCursor':          mfAsUnicode( pCodigoIdiomaCursor),  
        } )
     
        
               
        anOutput.write( u"""                 
            <!-- #################################################################
            SECTION: Hidden fields to maintain and communicate Batch translation status changes
            ################################################################# -->
               
            <input type="hidden" name="theBatch_Traducida"   id="theBatch_Traducida"     value=""/> 
            <input type="hidden" name="theBatch_Revisada"    id="theBatch_Revisada"      value=""/> 
            <input type="hidden" name="theBatch_Definitiva"  id="theBatch_Definitiva"    value=""/> 
            \n"""
        )
            
        if pMostrarLista  and not len( pDatosTraducciones) > 0:
            pRenderEmpty( 
                anOutput, 
                theCatalogo, 
                mfTranslateI18N( 'gvSIGi18n',  cResultCondition_NoMatchingTranslationsFound, cResultCondition_NoMatchingTranslationsFound + '-' ),                    
                mfTranslateI18N( 'gvSIGi18n',  'gvSIGi18n_reviseLasCondicionesDeFiltroYBusqueda_message', 'Please, review the filter and search criteria.-' ),                    
                aTranslationsCache
            )
                
                   
        anOutput.write( u"""  
            </form>
            \n""" 
        )                    
            
            
        anOutput.write( u"""  
            <!-- #################################################################
            SECTION: Hidden elements to temporarily store the html content received in the asynchronous response
            ################################################################# -->
            
            <p class="TRAstyle_NoDisplay" id="cid_TRAAsyncResponseStore" >
                &ensp;
            </p>
            
            \n""" 
        )                    

    
        
        anOutput.write( u"""
            <!-- #####
            ## Hidden Field: the translation index number being edited
            ##########-->  
            
            <input type="hidden" id="theCadenaTraducida_index" name="theCadenaTraducida_index" value="" />
    
            \n""" 
        )
             
        
         
        
        pRenderMessages( 
            anOutput, 
            theCatalogo,             
            aTranslationsCache
        )
            
        pEndTime = mfMillisecondsNow()
            
            
        pRenderCollapsibleTechnicalSections( 
            anOutput, 
            theCatalogo, 
            pRenderFormSubmit, 
            pRenderRequest, 
            pRenderFullRequest, 
            pRenderTimes, 
            False, # pRenderProfile ACV 20090928 Removed. Now it is rendered when the method TRAChangeAndBrowseTranslations completes , 
            pRenderAsyncRequest,
            pRenderUserInterfaceEvents,
            pFormSubmit, 
            pStartTime, 
            pEndTime, 
            pBrowseDuration, 
            unHayCambio, 
            pChangeDuration, 
            unExecutionRecord, 
            aRequestDumpString, 
            aFullRequestDumpString, 
            aTranslationsCache
        )
        
        
        anOutput.write( u"""
            <!-- #####
            ## Link to invoke a function that will hopefully open javascript debugger (i.e. causing an error)
            ##########-->  
            
            <br/>
            <p onclick="pTRAEnterDebugger(); return true;" ><font color="red"><strong><em>!</em></strong></font></p>
    
            \n""" 
        )
             
    
        aRendering = anOutput.getvalue()
            
        return aRendering
    
        
    finally:
        unExecutionRecord and unExecutionRecord.pEndExecution()
     
              
      













def pRequestStrings( 
    unContextualObject, 
    theRequest,
    pRenderRequest, 
    pRenderFullRequest, 
    aTranslationsCache):
    """Capture Request dump strings.
    
    """
    if not unContextualObject or not theRequest:
        return ( '', '',)
    

    aRequestDumpString      = ''
    if pRenderRequest:
        aRequestOutput      = StringIO()
        
        unEncodedOutput = None
        try:
            unEncodedOutput = CODECS_EncodedFile( aRequestOutput, 'utf-8', 'ascii', errors='replace')
        except:
            None
        if unEncodedOutput:
            unEncodedOutput.write( u"""
                <!-- #################################################################
                SECTION: Request parameters relevant to the renderer script
                ################################################################# -->
                <br/>
                <h3>Request parameters relevant to the application in this page</h3> 
                <table>
                    <tbody>
                    \n"""
            )
            aMaxKeyLen = max( [ len( aRequestKey) for aRequestKey in cInterestingRequestKeys])
            for aRequestKey in cInterestingRequestKeys:
                aKeyString = unContextualObject.fCGIescape( aRequestKey)
                unValueString = theRequest.get( aRequestKey, '!?')
                if unValueString.__class__.__name__ == "list":
                    unValueString = '[ %s ]' % ( ' '.join( unValueString))
                unValueString = unContextualObject.fCGIescape( unValueString)
                unEncodedOutput.write( u"""
                    <tr><td >
                    \n""" 
                )
                unEncodedOutput.write( aKeyString)
                unEncodedOutput.write( '.' * ( aMaxKeyLen - len( aKeyString) + 1) )
                unEncodedOutput.write( unValueString)
                unEncodedOutput.write( u"""
                    </td></tr>
                    \n"""
                )
            
            unEncodedOutput.write( u"""
                    </tbody>
                </table>
                <br/>
                <br/>
                \n"""
            )
        else:
            aRequestOutput.write( 'Error creating backslashreplace stream to write the relevant request parameters.\n')    
            
        aRequestDumpString = aRequestOutput.getvalue()
         
        
        
    aFullRequestDumpString  = ''
    if pRenderFullRequest:
        aFullRequestOutput = StringIO()

        unEncodedFullRequesOutput = None
        try:
            unEncodedFullRequesOutput = CODECS_EncodedFile( aFullRequestOutput, 'utf-8', 'ascii', errors='replace')
        except:
            None
        if unEncodedFullRequesOutput:
            unEncodedFullRequesOutput.write( u"""
                <!-- #################################################################
                SECTION: All Request parameters
                ################################################################# -->
                <br/>
                <h3>Full Request </h3> 
                \n"""
            )
       
            unEncodedFullRequesOutput.write(  str( theRequest))
        else:
            aFullRequestOutput.write( 'Error creating backslashreplace stream to write the request.\n')    
            
        aFullRequestDumpString = aFullRequestOutput.getvalue()
        
    return ( aRequestDumpString, aFullRequestDumpString, )
    
    
    
    





   
def pInitTranslationsCache( 
    unContextualObject, 
    aTranslationsCache):
    """Preload some translations into cache.
    
    """

    
    someDomainsStringsAndDefaultsToTranslate = [
        [ 'gvSIGi18n', [    
            [ 'gvSIGi18n_traducciones_bloquesiguiente_label',           'Next-' ,],                                                               
            [ 'gvSIGi18n_editor_label',                                 'Editor-' ,],                                                                                   
            [ 'gvSIGi18n_detalle_label',                                'Detail-' ,],                                                                                  
            [ 'gvSIGi18n_noreadpermission_warning',                     'Warning: you do not have read permission.-' ,],                                    
            [ 'gvSIGi18n_extralangs_parameter_label',                   'Extra langs.-' ,],                                                               
            [ 'gvSIGi18n_traducciones_iraprimero_label',                'Go To First-' ,],                                                             
            [ 'gvSIGi18n_traducciones_iraanterior_label',               'Go To Previous-' ,],                                                         
            [ 'gvSIGi18n_traducciones_irasiguiente_label',              'Go To Next-' ,],                                                            
            [ 'gvSIGi18n_traducciones_iraultimo_label',                 'Go To Last-' ,],                                                               
            [ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label',    'State-' ,],                                                       
            [ 'gvSIGi18n_TRATraduccion_attr_fechaCreacionTextual_label','Creation Date-' ,],                                            
            [ 'gvSIGi18n_TRATraduccion_attr_usuarioCreador_label',     'Creator-' ,],                                                  
            [ 'gvSIGi18n_TRATraduccion_attr_fechaTraduccionTextual_label','Translation Date-' ,],                                            
            [ 'gvSIGi18n_TRATraduccion_attr_usuarioTraductor_label',    'Translator-' ,],                                                  
            [ 'gvSIGi18n_TRATraduccion_attr_fechaRevisionTextual_label','Revision Date-' ,],                                               
            [ 'gvSIGi18n_TRATraduccion_attr_usuarioRevisor_label',      'Reviewer-' ,],                                                    
            [ 'gvSIGi18n_TRATraduccion_attr_fechaDefinitivoTextual_label','Definitive Date-' ,],                                             
            [ 'gvSIGi18n_TRATraduccion_attr_usuarioCoordinador_label',  'Coordinator-' ,],                                                 
            [ 'gvSIGi18n_usuario_label',                                'User-' ,],                                                        
            [ 'gvSIGi18n_ocultar_action_label',                         'Hide-' ,],                                                       
            [ 'gvSIGi18n_TRATraduccion_attr_historia_label',            'History-' ,],                                                    
            [ 'gvSIGi18n_historiafechaaccion_label',                    'Action Date-' ,],                                                
            [ 'gvSIGi18n_historiausuarioactor_label',                   'Actor User-' ,],                                                 
            [ 'gvSIGi18n_editar_action_label',                          'Edit-' ,],                                                       
            [ 'gvSIGi18n_TRATraduccion_attr_simbolo_label',             'Symbol-' ,],                                                     
            [ 'gvSIGi18n_TRATraduccion_attr_cadenaTraducida_label',     'Translation-' ,],                                                
            [ 'gvSIGi18n_valoractualtraduccion_title',                  'Current-' ,],                                                  
            [ 'gvSIGi18n_nuevovalortraduccion_title',                   'New-' ,],                                                        
            [ 'gvSIGi18n_TRACadena_attr_id_label',                      'String Id-' ,],                                                  
            [ 'gvSIGi18n_TRATraduccion_attr_comentario_label',          'Comment-' ,],                                                    
            [ 'gvSIGi18n_comentar_action_label',                        'Comment-' ,],                                                                  
            [ 'gvSIGi18n_TRATraduccion_attr_nombresModulos_label',      'Modules-' ,],                                                    
            [ 'gvSIGi18n_nosehanencontradotraducciones_message',        'No translations have been found matching the specified criteria.-' ,], 
            [ 'gvSIGi18n_haHabidoCambioTraduccion_msg',                 'Translation has been changed.-' ,],  
            [ 'gvSIGi18n_lista_section_label',                          'List-' ,],
            [ 'gvSIGi18n_TranslationAction_Borrar',                     'Delete-',],
            [ 'gvSIGi18n_TranslationAction_Grabar',                     'Save-',],
            [ 'gvSIGi18n_TranslationAction_Revisar',                    'Review-',],
            [ 'gvSIGi18n_TranslationAction_Bloquear',                   'Lock-',],
            [ 'gvSIGi18n_TranslationAction_Abrir',                      'Open-',],
            [ 'gvSIGi18n_idioma_msgid',                                 'Language-',],
            [ 'gvSIGi18n_Estado_label',                                 'Status-',],
            [ 'gvSIGi18n_ColumnaSimboloColapsable_Action_Hide_help',    'Click to hide this column-',],
            [ 'gvSIGi18n_ColumnaSimboloColapsable_Action_Show_help',    'Click here to show the column with symbols',],
            [ 'gvSIGi18n_idiomasSection_title',                         'Reference Languages-', ],
            [ 'gvSIGi18n_seccionesSection_title',                       'Sections-', ],
            [ 'gvSIGi18n_seccionFiltro_title',                          'Filter-', ],
            [ 'gvSIGi18n_seccionInformeSumario_title',                  'Summary-', ],
            [ 'gvSIGi18n_seccionList_title',                            'List-', ],
            [ 'gvSIGi18n_AsynchronousTranslationMode_label',            'Send changes to server without refreshing the whole page-', ],
            [ 'gvSIGi18n_refrescar_action_label',                       'Refresh-', ],
            [ 'gvSIGi18n_TranslationsPerPage_label',                    'Number of translations in each page-',],
            [ 'gvSIGi18n_AppliesImmediatelyNoNeedToRefresh_help',      'Applies immediately, no need to refresh the page to make it effective.-',],
            [ 'gvSIGi18n_opcionesSection_title',                        'Options-',],
            [ 'gvSIGi18n_fecha_el',                                     'on-',],
            [ 'gvSIGi18n_usuario_por',                                  'by-',],
            [ 'gvSIGi18n_TRATraduccion_Creada',                         'Created-',],
            [ 'gvSIGi18n_ShowEditorDetails_label',                      'Display translation details in the editor',],   
            [ 'gvSIGi18n_InteractionMode_label',                        'Server interaction mode-',],                
            [ 'gvSIGi18n_InteractionMode_Asynchronous_label',           'Asynchronous-',],                
            [ 'gvSIGi18n_InteractionMode_Asynchronous_help',            'Send changes to server without refreshing the whole page, allowing continuation of work in the current page.',],                
            [ 'gvSIGi18n_InteractionMode_Synchronous_label',            'Synchronous',],                
            [ 'gvSIGi18n_InteractionMode_Synchronous_help',             'Send changes to server by loading a completely new page',],     
            [ 'gvSIGi18n_newStatus_title',                              'New Status-',],
            [ 'gvSIGi18n_AppliesOnSelectonForEditionNoNeedToRefresh_help', 'Applies as soon as you select a translation for edition, no need to refresh the page to make it effective.',],
            [ 'gvSIGi18n_fromToIn_from_label',                          'from-',],
            [ 'gvSIGi18n_fromToIn_to_label',                            'to-',],
            [ 'gvSIGi18n_fromToIn_in_label',                            'of-',],
            [ 'gvSIGi18n_BatchNewStatus_title',                         'Batch Status Change-',],
            # [ 'gvSIGi18n_BatchNewStatus_Apply_ButtonLabel',             'Apply-',],
            [ 'gvSIGi18n_Batch_ButtonLabel',                            'Batch-',],
            [ 'gvSIGi18n_TranslationAction_InvalidarTraduccionesCadena_label', 'Invalidate',],
            [ 'gvSIGi18n_TranslationAction_InvalidarTraduccionesCadena_help', 'Invalidate String Translations into all languages',],
            [ 'gvSIGi18n_ConfirmInvalidateStringTranslationsMsg', 'Do you want to Invalidate the String Translations into all languages',],
            [ 'gvSIGi18n_ReallyInvalidateStringTranslationsMsg', 'Do you REALLY want to Invalidate the String Translations into all languages',],
            
            
            
         ]],
    ]
        
    someDomainsStringsAndDefaultsToTranslate.append( 
        [ 'gvSIGi18n', 
            [[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_%s' % unEstado,  unEstado] for unEstado in cTodosEstados]
        ]
    )        
    
    
    unContextualObject.fTranslateI18NManyIntoDict( someDomainsStringsAndDefaultsToTranslate, aTranslationsCache)
        
    return None













# #################################
"""Rendering methods.

"""
  

    
def pRenderCollapsible_Lambda( 
    anOutput, 
    theCollapsibleTitle, 
    theCollapsibleId, 
    theLambda, 
    theCollapse=True):
    """Render the result of the lambda expression by encapsulating it in HTML/javascript producing a collapsible section in the connected user internet browser.
    
    """
    
    unCollapsedOrExpanded = ( theCollapse and 'collapsed') or 'expanded'
        
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
    
    theLambda()
     
    anOutput.write( u"""  
            </dd>
        </dl>
        <!-- ######### End collapsible  section ######### --> 
        \n"""
    )
    
    return None        

       














# #################################
#  Specific section renderers
# ###############################




def pEmptyPageContents( 
    unContextualObject, 
    unHeader,
    unMessage,
    aTranslationsCache=None):
    """Render an empty translations browser.
        
    """
    
    mfTranslateI18N     = unContextualObject.fTranslateI18N
    mfAsUnicode         = unContextualObject.fAsUnicode
    mfCRs2BRs           = unContextualObject.fCRs2BRs

    anOutput = StringIO()
    
    pRenderEmpty( 
        anOutput, 
        unContextualObject, 
        unHeader,
        unMessage,
        aTranslationsCache
    )
    
    return anOutput.getvalue()










def pRenderEmpty( 
    anOutput, 
    unContextualObject, 
    unHeader, 
    unMessage,
    aTranslationsCache=None):
    """Produce the content of an empty translations browser.
        
    """
    
    
    mfTranslateI18N     = unContextualObject.fTranslateI18N
    mfAsUnicode         = unContextualObject.fAsUnicode
    mfCRs2BRs           = unContextualObject.fCRs2BRs
    


    anOutput.write( u"""  
    
        <!-- #################################################################
        SECTION: EMPTY PAGE  with link back to catalog page
        ################################################################# -->

        \n"""
    )
              
    if unHeader:
        anOutput.write( u"""  
            <br/>
            <p><font color="red" size="3"><strong>%s</strong></font></p>
            <br/>
            \n""" % mfCRs2BRs( mfAsUnicode( unHeader))
        )

    if unMessage:
        anOutput.write( u"""  
            <br/>
            <p><font size="2">%s</font></p>
            <br/>
            \n""" % mfCRs2BRs( mfAsUnicode( unMessage))
        )

    anOutput.write( u"""  
        <br/>
        <br/>
        \n"""
    )
    
        
    return None
        


      
def pRenderStyles( anOutput, theContextualObject):
     
    anOutput.write( """
        
                   
        <!-- #################################################################
        SECTION: Styles to add presentation and behavior to the page elements
        ################################################################# -->

         <style type="text/css" >
            .TRAstyle_Clickable {
                cursor: pointer;
            }
            .TRAstyle_NoDisplay {
                display: none;
            }
            .TRAstyle_Display {
                display: run-in;
            }
            tr.TRAstyle_Display {
                display: table-row;
            }
        </style>
        \n"""
    )
    return None









def pRenderScripts( 
    anOutput, 
    unContextualObject):
    """Render the scripts assisting in controling the translations browser form in the client internet browser.
        
    """
    
    mfTranslateI18N     = unContextualObject.fTranslateI18N
    mfAsUnicode         = unContextualObject.fAsUnicode
    mfCRs2BRs           = unContextualObject.fCRs2BRs
    

    anOutput.write( u"""  
                    
        <!-- #################################################################
        SECTION: Scripts to be executed by user agent (WebBrowser)
        ################################################################# -->
        
       <!-- #################################################################
        Subsection: Translations form Script
        ################################################################# -->
        
        <script type="text/javascript" src="TRAChangeAndBrowseTranslations_javascripts.js"> </script>

       <!-- #################################################################
        Subsection: 3rd party AJAX queue Script
        ################################################################# -->
        <script type="text/javascript" src="ajax_queue.js"> </script>
        
        \n
    """
    )
    return None














def pRenderCabecera( 
    anOutput, 
    unContextualObject, 
    theBrowseResult,
    pLanguagesNamesAndFlags, 
    pTodosCodigosIdiomas, 
    pCodigoIdiomaCursor, 
    aTranslationsCache):
    """Render the header of the  translations browser.
    
    """    
        
    mfTranslateI18N     = unContextualObject.fTranslateI18N
    mfAsUnicode         = unContextualObject.fAsUnicode
    


  
    
    anOutput.write( u"""  
       <!-- #################################################################
             SECTION: PAGE HEADER with access and display control
             ################################################################# -->
             
        <table cellspacing="4" cellpadding="4" frame="void" >
           <tbody>   
                <tr>
                \n""" 
    )
    

   
    anOutput.write( u"""
        
        <!-- #################################################################
        Subsection: Link to navigate back to Catalogo container 
        ################################################################# -->
        <td align="left" valign="center" >
            <a href="%(pCatalogoAbsoluteURL)s" class="state-visible" title="%(gvSIGi18n_catalogo_action_label)s" >
                <img src="%(pCatalogoAbsoluteURL)s/contenedor.gif" alt="%(gvSIGi18n_catalogo_action_label)s" title="%(gvSIGi18n_catalogo_action_label)s" id="icon-contenedor" />                                        
            </a>
        </td>
        <td align="right" valign="center" >
        \n""" % { 
    'pCatalogoAbsoluteURL':                         unContextualObject.absolute_url(), 
    'gvSIGi18n_catalogo_action_label':      mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_catalogo_action_label', 'Catalog-'),  
    })
    
    
    
    pRenderSelectorIdiomaPrincipal( anOutput, unContextualObject, pLanguagesNamesAndFlags, pTodosCodigosIdiomas, pCodigoIdiomaCursor, aTranslationsCache)
                   
    anOutput.write( u"""
        </td>
        <td align="right" valign="center" >
        \n"""
    )
   
  
    #anOutput.write( u"""
        #</td>
        #<td align="center" valign="center" >
            #<img width="14" height="11" alt="Flag_%(codigo-idioma)s" src="%(portal_url)s/%(flag-icon)s" title="%(codigo-idioma)s" />
        #</td>
        #<td align="right" valign="center" >
        #\n"""% {
        #'portal_url':                           unContextualObject.absolute_url(), 
        #'flag-icon':                            pLanguagesNamesAndFlags.get( pCodigoIdiomaCursor, {}).get( 'flag', 'tra_flag-ninguna.gif'), 
        #'codigo-idioma':                        pCodigoIdiomaCursor,  
    #})
    
    pRenderCursorButtons( anOutput, unContextualObject, 9, aTranslationsCache)
         
    anOutput.write( u"""
                    </td>
                </tr>
            </tbody>
        </table>
        \n""" %  {
                          
    })   
 
        
    return None
        







def pRenderSelectorIdiomaPrincipal( 
    anOutput, 
    unContextualObject, 
    pLanguagesNamesAndFlags, 
    pTodosCodigosIdiomas, 
    pCodigoIdiomaCursor, 
    aTranslationsCache):
    """Render the selector of the main language in the translations browser.
    
    """    
    
    mfTranslateI18N     = unContextualObject.fTranslateI18N
    mfAsUnicode         = unContextualObject.fAsUnicode
    
            
    anOutput.write( u"""  
       <!-- #################################################################
        SECTION: Selector de Idioma principal 
        ################################################################# -->
           <select  style="font-size: 9pt;" name="theCodigoIdiomaCursor" id="theCodigoIdiomaCursor" onchange="document.getElementById( 'TranslationFormId').submit(); return true;">
           \n""" 
    )

                
    for unCodigoIdioma in pTodosCodigosIdiomas:
        anOutput.write( u"""         
            <option id="%(codigo-idioma)s_id" %(selected-selected)s value="%(codigo-idioma)s">%(codigo-idioma)s %(nombre-idioma)s %(nombre-nativo-idioma)s</option>
            \n""" % { 
            'codigo-idioma':        mfAsUnicode( unCodigoIdioma), 
            'nombre-idioma':        mfAsUnicode( pLanguagesNamesAndFlags.get( unCodigoIdioma, {}).get( 'english', unCodigoIdioma)),
            'nombre-nativo-idioma': mfAsUnicode( pLanguagesNamesAndFlags.get( unCodigoIdioma, {}).get( 'native',  unCodigoIdioma)),
            'selected-selected':    ( (unCodigoIdioma == pCodigoIdiomaCursor) and 'selected="selected"') or '',
        })
      
            
    anOutput.write( u"""
            </select>
        \n"""
    )
    
    return None









    
def pRenderCollapsibleSelectorIdiomasReferencia( 
    anOutput, 
    unContextualObject, 
    pLanguagesNamesAndFlags, 
    pTodosCodigosIdiomasEInternacionales, 
    pIdiomasReferencia, 
    aTranslationsCache):
    """Render as collapsible the section to select the reference languages to display for each translation in the translations browser.
    
    """    
    
    mfTranslateI18N     = unContextualObject.fTranslateI18N
    mfAsUnicode         = unContextualObject.fAsUnicode
    mfCRs2BRs           = unContextualObject.fCRs2BRs
            
    pRenderCollapsible_Lambda(  anOutput,
        aTranslationsCache[ 'gvSIGi18n_idiomasSection_title'],
        u'elid_SelectorIdiomasReferencia_collapsible_dl', 
        lambda : pRenderSelectorIdiomasReferencia( 
            anOutput, 
            unContextualObject, 
            pLanguagesNamesAndFlags, 
            pTodosCodigosIdiomasEInternacionales, 
            pIdiomasReferencia,
            aTranslationsCache
        )
    )
    
    return None        







def pRenderSelectorIdiomasReferencia( 
    anOutput, 
    unContextualObject, 
    pLanguagesNamesAndFlags, 
    pTodosCodigosIdiomasEInternacionales, 
    pIdiomasReferencia,
    aTranslationsCache):
    """Render  the section to select the reference languages to display for each translation in the translations browser.
    
    """    
    
    mfTranslateI18N     = unContextualObject.fTranslateI18N
    mfAsUnicode         = unContextualObject.fAsUnicode
    mfCRs2BRs           = unContextualObject.fCRs2BRs
    
    unDisplayContryFlags = unContextualObject.fDisplayCountryFlags()
    
    anOutput.write( u"""  
        
        <!-- #################################################################
        SECTION: Selection of reference languages 
        ################################################################# -->                           
    
        <br/>
        <input name="form_submit" style="font-size: 10pt; font-style: italic"  value="%(gvSIGi18n_refrescar_action_label)s" type="submit"/>
        <br/>
 
        <table id="sct_ReferenceLanguages_selector" class="listing nosort" summary="Selection of reference languages" >
            <thead>
                <tr>
                    <th colspan="%(colspan_head)d" align="left"   >
                        <span><font size="2"><strong>%(gvSIGi18n_selectorLenguagesReferencia_title)s</strong></font></span>
                        <br/>
                        <span class="formHelp">
                            %(gvSIGi18n_selectorLenguagesReferencia_help)s
                            <br/>
                            %(gvSIGi18n_limiteNumeroRegistrosExplorados_help)s
                            <br/>
                            %(max-numero-registros-explorados)s
                            <br/>
                            %(gvSIGi18n_numeroRegistrosDivididoPorNumerolenguages_help)s
                        </span>
                    </th>
                </tr>
                <tr>
                    <th colspan="%(colspan_labels)d"  />
                    <th align="center" >
                        <input type="checkbox"  class="noborder"  value=""  name="cid_TRAToggleAllReferenceLanguages" id="cid_TRAToggleAllReferenceLanguages" 
                            onchange="pTRAToggleAllReferenceLanguages(); return true;" />
                    </th>
                </tr>
            </head>
            <tbody>   
            \n""" % {
        'colspan_head':                                              ( unDisplayContryFlags and 6) or 5,
        'colspan_labels':                                           ( unDisplayContryFlags and 5) or 4,
        'portal_url':                                               unContextualObject.absolute_url(), 
        'gvSIGi18n_selectorLenguagesReferencia_title':      mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_selectorLenguagesReferencia_title', 'Reference Languages Selector'),
        'gvSIGi18n_limiteNumeroRegistrosExplorados_help':      mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_limiteNumeroRegistrosExplorados_help', 'The maximum number of translations to explore in a single page is'),
        'max-numero-registros-explorados':                          unContextualObject.fMaximoRegistrosExplorados(),
        'gvSIGi18n_numeroRegistrosDivididoPorNumerolenguages_help':      mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_numeroRegistrosDivididoPorNumerolenguages_help', 'divided by the number of reference languages selected plus one'),
        'gvSIGi18n_selectorLenguagesReferencia_help':       mfCRs2BRs( mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_selectorLenguagesReferencia_help', 'Select the languages you want to use as reference.\nA high number of languages will slow down page loading.')),
        'gvSIGi18n_todosLenguagesReferencia_action_label':  mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_todosLenguagesReferencia_action_label', '+'),
        'gvSIGi18n_ningunLenguagesReferencia_action_label': mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_ningunLenguagesReferencia_action_label', '+'),
        'gvSIGi18n_todosPlus_action_label':                 mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_todosPlus_action_label', '+'),
        'gvSIGi18n_ningunMinus_action_label':               mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_ningunMinus_action_label', '-'),
        'gvSIGi18n_refrescar_action_label':             mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_refrescar_action_label', 'Refresh-'),                
    })
    
    unIndexRowIdiomaReferencia = 0 
    for unCodigoIdiomaEInternacional in pTodosCodigosIdiomasEInternacionales:  
        unCodigoIdiomaEnGvSIG         = unCodigoIdiomaEInternacional[ 0]
        unCodigoInternacionalDeIdioma = unCodigoIdiomaEInternacional[ 1]
                
        unasSizesIdioma = TRASizesIdioma( unCodigoIdiomaEnGvSIG)
        
        if unCodigoIdiomaEnGvSIG == unCodigoInternacionalDeIdioma:        
            anOutput.write( u"""                                                                                                                                                                     
                <tr class="%(class-row-idioma)s" >
                    <td colspan="2" align="left"  valign="center"  onclick="pTRAToggleIdiomaReferencia( '%(index-idioma)s'); return true;" class="TRAstyle_Clickable"  >                
                        <font size="1" >
                            <strong>
                                %(codigo-idioma)s
                            </strong>
                        </font>
                    </td>
                \n""" % { 
                'index-idioma':         str( unIndexRowIdiomaReferencia),
                'class-row-idioma':     cClasesFilas[ unIndexRowIdiomaReferencia % 2],
                'codigo-idioma':        mfAsUnicode( unCodigoIdiomaEnGvSIG),
             } )
        else:
            anOutput.write( u"""                                                                                                                                                                     
                <tr class="%(class-row-idioma)s" >
                    <td align="left"  valign="center"  onclick="pTRAToggleIdiomaReferencia( '%(index-idioma)s'); return true;" class="TRAstyle_Clickable"  >                
                        <font size="1" >
                            <strong>
                                %(codigo-idioma)s
                            </strong>
                        </font>
                    </td>
                    <td align="left"  valign="center"  onclick="pTRAToggleIdiomaReferencia( '%(index-idioma)s'); return true;" class="TRAstyle_Clickable"  >                
                        <font size="1" >
                            <strong>
                                %(codigo-intl-idioma)s
                            </strong>
                        </font>
                    </td>
                \n""" % { 
                'index-idioma':         str( unIndexRowIdiomaReferencia),
                'class-row-idioma':     cClasesFilas[ unIndexRowIdiomaReferencia % 2],
                'codigo-idioma':        mfAsUnicode( unCodigoIdiomaEnGvSIG),
                'codigo-intl-idioma':   mfAsUnicode( unCodigoInternacionalDeIdioma),
            } )
                                
        anOutput.write( u"""                                                                                                                                                                     
                <td align="left" valign="center" onclick="pTRAToggleIdiomaReferencia( '%(index-idioma)s'); return true;" class="TRAstyle_Clickable"  >                
                    <font size="1" >
                        <strong>
                            %(nombre-idioma)s
                        </strong>
                    </font>
                </td>
                <td align="left" valign="center" onclick="pTRAToggleIdiomaReferencia( '%(index-idioma)s'); return true;" class="TRAstyle_Clickable"  >                
                    <font size="%(display_font_size)d" >
                        <strong>
                            %(nombre-nativo-idioma)s
                        </strong>
                    </font>
                </td>
             \n""" % { 
            'display_font_size':    unasSizesIdioma.get( 'display_font_size', 1),
            'index-idioma':         str( unIndexRowIdiomaReferencia),
            'class-row-idioma':     cClasesFilas[ unIndexRowIdiomaReferencia % 2],
            'codigo-idioma':        mfAsUnicode( unCodigoIdiomaEnGvSIG),
            'codigo-intl-idioma':   mfAsUnicode( unCodigoInternacionalDeIdioma),
            'nombre-idioma':        mfAsUnicode( pLanguagesNamesAndFlags.get( unCodigoIdiomaEnGvSIG, {}).get( 'english', '')),        
            'nombre-nativo-idioma': mfAsUnicode( pLanguagesNamesAndFlags.get( unCodigoIdiomaEnGvSIG, {}).get( 'native',  '')),
            'idioma-checked':       (( unCodigoIdiomaEnGvSIG in pIdiomasReferencia) and 'checked="checked"') or '',
        } )
        
        
        if unDisplayContryFlags:
            anOutput.write( u"""                                                                                                                                                                     
                    <td align="center" valign="center" onclick="pTRAToggleIdiomaReferencia( '%(index-idioma)s'); return true;" class="TRAstyle_Clickable"  >                
                        <img width="14" height="11" alt="Flag_%(nombre-idioma)s" src="%(portal_url)s/%(flag-icon)s" title="Flag_%(nombre-idioma)s" />
                    </td>
                \n""" % { 
                'index-idioma':         str( unIndexRowIdiomaReferencia),
                'codigo-idioma':        mfAsUnicode( unCodigoIdiomaEnGvSIG),
                'nombre-idioma':        mfAsUnicode( pLanguagesNamesAndFlags.get( unCodigoIdiomaEnGvSIG, {}).get( 'english', '')),        
                'portal_url':           unContextualObject.absolute_url(), 
                'flag-icon':            pLanguagesNamesAndFlags.get( unCodigoIdiomaEnGvSIG, {}).get( 'flag', 'tra_flag-ninguna.gif'), 
            } )
        
        anOutput.write( u"""                                                                                                                                                                     
                <td align="center" valign="center" >                
                    <input type="checkbox" class="noborder"  value="%(codigo-idioma)s"  %(idioma-checked)s name="theIdiomasReferencia" 
                        id="theIdiomasReferencia_%(index-idioma)s" />
                </td>
            </tr>
            \n""" % { 
            'index-idioma':         str( unIndexRowIdiomaReferencia),
            'codigo-idioma':        mfAsUnicode( unCodigoIdiomaEnGvSIG),
            'idioma-checked':       (( unCodigoIdiomaEnGvSIG in pIdiomasReferencia) and 'checked="checked"') or '',
        } )
        
        unIndexRowIdiomaReferencia += 1

    anOutput.write( u"""  
            </body>
        </table>
        <br/>
        <input name="form_submit" style="font-size: 10pt; font-style: italic"  value="%(gvSIGi18n_refrescar_action_label)s" type="submit"/>
        <br/>
        <br/>
         \n""" % {
        'gvSIGi18n_refrescar_action_label':             mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_refrescar_action_label', 'Refresh-'),                
    })

    return None
                
  









    






def pRenderCollapsibleControlPresentacion( 
    anOutput, 
    unContextualObject, 
    pTraduccionesPorPagina,
    pInteractionMode,
    pMostrarInforme, 
    pMostrarLista, 
    pMostrarDetallesTraduccion,
    pMostrarHistoria, 
    pShowStateTransitionColumnsOption,
    pHideStateTransitionColumns,
    pShowBatchStatusChangesOption,
    pBatchStatusChanges,            
    pCanComment, 
    pEditorKeyCRAction,
    pEditorKeyTabAction,
    pRenderFormSubmit, 
    pRenderRequest, 
    pRenderFullRequest, 
    pRenderTimes, 
    pRenderProfile,
    pRenderAsyncRequest,  
    pRenderUserInterfaceEvents,
    aTranslationsCache):
    """Render as collapsible the control to select presentation sections to include in the translations browser.
    
    """    
    
    mfTranslateI18N     = unContextualObject.fTranslateI18N
    mfAsUnicode         = unContextualObject.fAsUnicode
    mfCRs2BRs           = unContextualObject.fCRs2BRs
            
    pRenderCollapsible_Lambda(  anOutput,
        aTranslationsCache[ 'gvSIGi18n_opcionesSection_title'],
        u'elid_ControlPresentacion_collapsible_dl', 
        lambda : pRenderControlPresentacion( 
            anOutput, 
            unContextualObject, 
            pTraduccionesPorPagina,
            pInteractionMode,
            pMostrarInforme, 
            pMostrarLista, 
            pMostrarDetallesTraduccion,
            pMostrarHistoria, 
            pShowStateTransitionColumnsOption,
            pHideStateTransitionColumns,
            pShowBatchStatusChangesOption,
            pBatchStatusChanges,            
            pCanComment, 
            pEditorKeyCRAction,
            pEditorKeyTabAction,
            pRenderFormSubmit, 
            pRenderRequest, 
            pRenderFullRequest, 
            pRenderTimes, 
            pRenderProfile,
            pRenderAsyncRequest,  
            pRenderUserInterfaceEvents,
            aTranslationsCache
        )
    )
    
    return None        




def pRenderControlPresentacion( 
    anOutput, 
    unContextualObject,
    pTraduccionesPorPagina,
    pInteractionMode,
    pMostrarInforme, 
    pMostrarLista, 
    pMostrarDetallesTraduccion,
    pMostrarHistoria, 
    pShowStateTransitionColumnsOption,    
    pHideStateTransitionColumns,
    pShowBatchStatusChangesOption,
    pBatchStatusChanges,            
    pCanComment, 
    pEditorKeyCRAction,
    pEditorKeyTabAction,
    pRenderFormSubmit, 
    pRenderRequest, 
    pRenderFullRequest, 
    pRenderTimes, 
    pRenderProfile,
    pRenderAsyncRequest,
    pRenderUserInterfaceEvents,
    aTranslationsCache):
    """Render the control to select presentation sections to include in the translations browser.
    
    """    
    
    mfTranslateI18N     = unContextualObject.fTranslateI18N
    mfAsUnicode         = unContextualObject.fAsUnicode
    mfCRs2BRs           = unContextualObject.fCRs2BRs
    
    
    anOutput.write( u"""  
        
        <!-- #################################################################
        SECTION: Presentation options control 
        ################################################################# -->   
        
        <br/>
        \n"""
    )
    
  
    
    
    anOutput.write( u"""  
        
         <!-- #################################################################
        Subsection: Enable asynchronous interactions
        ################################################################# -->   
        
        <font size="2" >
            <strong>
                %(gvSIGi18n_InteractionMode_label)s
            </strong>
        </font>
        <br/>
        <font size="1" >
            <strong>
                %(gvSIGi18n_InteractionMode_Asynchronous_label)s
            </strong>
        </font>
        &ensp;
        <input type="radio" class="noborder"  value="%(interaction-mode-async)s"  %(is-checked-Async)s name="theInteractionMode" id="theInteractionMode_Async" />
        &emsp;
        &emsp;
        &emsp;
        <font size="1" >
            <strong>
                %(gvSIGi18n_InteractionMode_Synchronous_label)s
            </strong>
        </font>
       &ensp;
        <input onclick="gAsynchronousTranslationMode_CachedInVar=999; return true;"
            type="radio" class="noborder"  value="%(interaction-mode-sync)s"   
            %(is-checked-Sync)s name="theInteractionMode" id="theInteractionMode_Sync" />
        <div class="formHelp">
            <font size="1">
                %(gvSIGi18n_InteractionMode_Asynchronous_label)s&nbsp;%(gvSIGi18n_InteractionMode_Asynchronous_help)s
                <br/>
                %(gvSIGi18n_InteractionMode_Synchronous_label)s&nbsp;%(gvSIGi18n_InteractionMode_Synchronous_help)s
                <br/>
                %(gvSIGi18n_AppliesImmediatelyNoNeedToRefresh_help)s
            </font>
        </div>
        <br/>        
        
        \n"""% {
        'interaction-mode-async':                                       cInteractionMode_Asynchronous,
        'interaction-mode-sync':                                        cInteractionMode_Synchronous,
        'is-checked-Async':                                             (( pInteractionMode == cInteractionMode_Asynchronous) and 'checked="checked"') or '',
        'is-checked-Sync':                                              (( pInteractionMode == cInteractionMode_Synchronous)  and 'checked="checked"') or '',
        'gvSIGi18n_InteractionMode_label':                      aTranslationsCache[ 'gvSIGi18n_InteractionMode_label'],                
        'gvSIGi18n_InteractionMode_Asynchronous_label':         aTranslationsCache[ 'gvSIGi18n_InteractionMode_Asynchronous_label'],                
        'gvSIGi18n_InteractionMode_Asynchronous_help':          aTranslationsCache[ 'gvSIGi18n_InteractionMode_Asynchronous_help'],                
        'gvSIGi18n_InteractionMode_Synchronous_label':          aTranslationsCache[ 'gvSIGi18n_InteractionMode_Synchronous_label'],                
        'gvSIGi18n_InteractionMode_Synchronous_help':           aTranslationsCache[ 'gvSIGi18n_InteractionMode_Synchronous_help'],                
        'gvSIGi18n_AppliesImmediatelyNoNeedToRefresh_help':     aTranslationsCache[ 'gvSIGi18n_AppliesImmediatelyNoNeedToRefresh_help'],                
    })

 
    
    
    
    
   
    
    anOutput.write( u"""  
        
         <!-- #################################################################
        Subsection: Show translation details in editor
        ################################################################# -->   
        
        <font size="2" >
            <strong>
                %(gvSIGi18n_ShowEditorDetails_label)s
            </strong>
        </font>
        &emsp;
        <input type="checkbox" class="noborder"  value="on"  %(is-checked)s name="theMostrarDetallesTraduccion" id="theMostrarDetallesTraduccion" />
        <br/>
        <span class="formHelp"><font size="1">%(gvSIGi18n_AppliesOnSelectonForEditionNoNeedToRefresh_help)s</font></span>
        <br/>
        <br/>        
        
        \n"""% {
        'is-checked':                                                   (( pMostrarDetallesTraduccion) and 'checked="checked"') or '',
        'gvSIGi18n_ShowEditorDetails_label':                    aTranslationsCache[ 'gvSIGi18n_ShowEditorDetails_label'],                
        'gvSIGi18n_AppliesOnSelectonForEditionNoNeedToRefresh_help':    aTranslationsCache[ 'gvSIGi18n_AppliesOnSelectonForEditionNoNeedToRefresh_help'],                
    })

    
    
    
 
    
    anOutput.write( u"""  
        <!-- ########################
        SubSection: Editor keys options
        #############################-->
        
        <table id="sct_PresentationOptions_control" class="listing nosort" summary="Control for Editor keys behaviour" >
            <thead>
                <tr>
                    <th align="left" colspan="2" >
                        <font size="2">                    
                            <strong>
                                %(gvSIGi18n_controlEditorKeys_title)s
                            </strong>
                        </font>
                        <p class="formHelp">
                            %(gvSIGi18n_controlEditorKeys_help)s
                            <br/>
                            %(gvSIGi18n_AppliesImmediatelyNoNeedToRefresh_help)s
                        </p>
                    </th>
                </tr>
             </head>
            <tbody>   
            <tr class="even" >
                <td align="left" valign="center" >%(gvSIGi18n_EditorKey_CR_label)s</td>                
                <td align="left" valign="center" >                
                    <span class="field ArchetypesSelectionWidget"> 
                        <select  style="font-size: 9pt;" name="theKeyAction_CR" id="theKeyAction_CR" onchange="gKeyAction_CR_Cached='999';return true;" >
                            <option id="theKeyAction_CR_action_traducirYAvanzar" %(is-selected-CR_action_traducirYAvanzar)s    value="action_traducirYAvanzar">%(action_traducirYAvanzar_label)s</option>
                            <option id="theKeyAction_CR_action_traducir"         %(is-selected-CR_action_traducir)s            value="action_traducir">%(action_traducir_label)s</option>
                            <option id="theKeyAction_CR_action_avanzar"          %(is-selected-CR_action_avanzar)s             value="action_avanzar">%(action_avanzar_label)s</option>
                            <option id="theKeyAction_CR_action_nextTabIndex"     %(is-selected-CR_action_nextTabIndex)s        value="action_nextTabIndex">%(action_nextTabIndex_label)s</option>
                        </select>
                    </span>
                </td>
            </tr>
            <tr class="odd" >
                <td align="left" valign="center" >%(gvSIGi18n_EditorKey_Tab_label)s</td>                
                <td align="left" valign="center" >                
                    <span class="field ArchetypesSelectionWidget"> 
                        <select  style="font-size: 9pt;" name="theKeyAction_Tab" id="theKeyAction_Tab" onchange="gKeyAction_Tab_Cached='999';return true;" >
                            <option id="theKeyAction_Tab_action_traducirYAvanzar" %(is-selected-Tab_action_traducirYAvanzar)s    value="action_traducirYAvanzar">%(action_traducirYAvanzar_label)s</option>
                            <option id="theKeyAction_Tab_action_traducir"         %(is-selected-Tab_action_traducir)s            value="action_traducir">%(action_traducir_label)s</option>
                            <option id="theKeyAction_Tab_action_avanzar"          %(is-selected-Tab_action_avanzar)s             value="action_avanzar">%(action_avanzar_label)s</option>
                            <option id="theKeyAction_Tab_action_nextTabIndex"     %(is-selected-Tab_action_nextTabIndex)s        value="action_nextTabIndex">%(action_nextTabIndex_label)s</option>
                        </select>
                    </span>
                </td>
            </tr>
            </thead>
        </table>
        <br/>
        <br/>
        \n""" % {
        'gvSIGi18n_controlEditorKeys_title':      mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_controlEditorKeys_title', 'Editor keys behaviour-'),                
        'gvSIGi18n_controlEditorKeys_help':       mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_controlEditorKeys_help', 'Choose the behaviour when pressing the CR and Tab keys in the translations editor text area.-'),                
        'gvSIGi18n_AppliesImmediatelyNoNeedToRefresh_help':     aTranslationsCache[ 'gvSIGi18n_AppliesImmediatelyNoNeedToRefresh_help'],                
        'gvSIGi18n_EditorKey_CR_label':           mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_EditorKey_CR_label', 'Key Enter'), 
        'gvSIGi18n_EditorKey_Tab_label':          mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_EditorKey_Tab_label', 'Key Tab'), 
        'is-selected-Tab_action_traducirYAvanzar':       (( pEditorKeyTabAction == 'action_traducirYAvanzar' ) and 'selected="selected"') or '',
        'is-selected-Tab_action_traducir':               (( pEditorKeyTabAction == 'action_traducir' )       and 'selected="selected"') or '',
        'is-selected-Tab_action_avanzar':                (( pEditorKeyTabAction == 'action_avanzar' )        and 'selected="selected"') or '',
        'is-selected-Tab_action_nextTabIndex':           (( pEditorKeyTabAction == 'action_nextTabIndex' )   and 'selected="selected"') or '',
        'action_traducirYAvanzar_label':                 mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_EditorKeyActions_action_traducirYAvanzar_label', 'Translate and Advance'), 
        'action_traducir_label':                         mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_EditorKeyActions_action_traducir_label', 'Translate'), 
        'action_avanzar_label':                          mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_EditorKeyActions_action_avanzar_label', 'Advance'), 
        'action_nextTabIndex_label':                     mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_EditorKeyActions_action_nextTabIndex_label', 'NextTab'), 
        'is-selected-CR_action_traducirYAvanzar':        (( pEditorKeyCRAction == 'action_traducirYAvanzar' ) and 'selected="selected"') or '',
        'is-selected-CR_action_traducir':                (( pEditorKeyCRAction == 'action_traducir' )       and 'selected="selected"') or '',
        'is-selected-CR_action_avanzar':                 (( pEditorKeyCRAction == 'action_avanzar' )        and 'selected="selected"') or '',
        'is-selected-CR_action_nextTabIndex':            (( pEditorKeyCRAction == 'action_nextCRIndex' )   and 'selected="selected"') or '',
    })
        
    
    
    
    
    anOutput.write( u"""  
       <!-- #################################################################
        Subsection: Refresh button
        ################################################################# -->   
        
        <input name="form_submit" style="font-size: 10pt; font-style: italic"  value="%(gvSIGi18n_refrescar_action_label)s" type="submit"/>
        <br/>
        \n"""% {
         'gvSIGi18n_refrescar_action_label':                     aTranslationsCache[ 'gvSIGi18n_refrescar_action_label'],                
      })
    
    
    
    anOutput.write( u"""  
        <br/>
        <!-- #################################################################
        Subsection: Number of  translations per page
        ################################################################# -->   
        
        <font size="2">
            <strong>
                %(gvSIGi18n_TranslationsPerPage_label)s
            </strong>
        </font>
        &emsp;
        <input style="font-size: 8pt;" size="4"  name="theTraduccionesPorPagina" id="theTraduccionesPorPagina" value="%(pTraduccionesPorPagina)s" /> 
        <br/>
        <span class="formHelp">
            %(gvSIGi18n_limiteNumeroRegistrosExplorados_help)s
            &ensp;
            %(max-numero-registros-explorados)s
            &ensp;
            %(gvSIGi18n_numeroRegistrosDivididoPorNumerolenguages_help)s
        </span>
        <br/>
        \n""" % {
        'pTraduccionesPorPagina':                                           str( pTraduccionesPorPagina),
        'gvSIGi18n_TranslationsPerPage_label':                      aTranslationsCache[ 'gvSIGi18n_TranslationsPerPage_label'], 
        'gvSIGi18n_limiteNumeroRegistrosExplorados_help':           mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_limiteNumeroRegistrosExplorados_help', 'The maximum number of translations to explore in a single page is'),
        'max-numero-registros-explorados':                                  unContextualObject.fMaximoRegistrosExplorados(),
        'gvSIGi18n_numeroRegistrosDivididoPorNumerolenguages_help': mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_numeroRegistrosDivididoPorNumerolenguages_help', 'divided by the number of reference languages selected plus one'),
     })

    
    
    anOutput.write( u"""  
        <br/>
        <!-- ########################
        SubSection: Business presentation options
        #############################-->
        
        <table id="sct_PresentationOptions_control" class="listing nosort" summary="Control for Presentation options" >
            <thead>
                <tr>
                    <th align="left" colspan="2" >
                        <font size="2">                    
                            <strong>
                                %(gvSIGi18n_controlBusinessPresentacion_title)s
                            </strong>
                        </font>
                        <p class="formHelp">%(gvSIGi18n_controlPresentacion_help)s</p>
                    </th>
                </tr>
             </head>
            <tbody>   
            \n""" % {
        'gvSIGi18n_controlBusinessPresentacion_title':  mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_controlBusinessPresentacion_title', 'Business sections-'),                
        'gvSIGi18n_controlPresentacion_help':           mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_controlPresentacion_help', 'Control of presentation options,\nto show or hide page sections relevant to the business.-'),                
    })
    
     
     
     
     
    if pShowStateTransitionColumnsOption:
        anOutput.write( u"""  
           <tr class="even" >
               <td align="left"  valign="center" onclick="pTRApTRAToggleSeccionPresentacion( 'theHideStateTransitionColumns'); return true;" class="TRAstyle_Clickable"  >                
                   <font size="1" >
                       <strong>
                           %(gvSIGi18n_HideStateTransitionColumns_label)s
                       </strong>
                   </font>
               </td>
               <td align="center" valign="center" >                
                   <input type="checkbox" class="noborder"  value="on"  %(is-checked)s name="theHideStateTransitionColumns" id="theHideStateTransitionColumns" />
               </td>
           </tr>
           \n""" % { 
           'gvSIGi18n_HideStateTransitionColumns_label': mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_HideStateTransitionColumns_label', 'Hide columns with Status change Buttons-'), 
           'is-checked': (( pHideStateTransitionColumns) and 'checked="checked"') or '',
        })
    
    if pShowBatchStatusChangesOption:
        anOutput.write( u"""  
           <tr class="even" >
               <td align="left"  valign="center" onclick="pTRApTRAToggleSeccionPresentacion( 'theBatchStatusChanges'); return true;" class="TRAstyle_Clickable"  >                
                   <font size="1" >
                       <strong>
                           %(gvSIGi18n_BatchStatusChanges_label)s
                       </strong>
                   </font>
               </td>
               <td align="center" valign="center" >                
                   <input type="checkbox" class="noborder"  value="on"  %(is-checked)s name="theBatchStatusChanges" id="theBatchStatusChanges" />
               </td>
           </tr>
           \n""" % { 
           'gvSIGi18n_BatchStatusChanges_label': mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_BatchStatusChanges_label', 'Batch Status changes-'), 
           'is-checked': (( pBatchStatusChanges) and 'checked="checked"') or '',
        })
    
    
    anOutput.write( u"""  
       <tr class="even" >
           <td align="left"  valign="center" onclick="pTRAToggleSeccionPresentacion( 'theMostrarInforme'); return true;" class="TRAstyle_Clickable"  >                
               <font size="1" >
                   <strong>
                       %(gvSIGi18n_mostrarSeccionInforme_section_label)s
                   </strong>
               </font>
           </td>
           <td align="center" valign="center" >                
               <input type="checkbox" class="noborder"  value="on"  %(is-checked)s name="theMostrarInforme" id="theMostrarInforme" />
           </td>
       </tr>
       \n""" % { 
       'gvSIGi18n_mostrarSeccionInforme_section_label': mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_mostrarSeccionInforme_section_label', 'Show Summary section-'), 
       'is-checked': (( pMostrarInforme) and 'checked="checked"') or '',
    })
    

  
   
    anOutput.write( u"""  
       <tr class="even" >
           <td align="left"  valign="center" onclick="pTRAToggleSeccionPresentacion( 'theMostrarHistoria'); return true;" class="TRAstyle_Clickable"  >                
               <font size="1" >
                   <strong>
                       %(gvSIGi18n_mostrarSeccionHistoria_section_label)s
                   </strong>
               </font>
           </td>
           <td align="center" valign="center" >                
               <input type="checkbox" class="noborder"  value="on"  %(is-checked)s name="theMostrarHistoria" id="theMostrarHistoria" />
           </td>
       </tr>
       \n""" % { 
       'gvSIGi18n_mostrarSeccionHistoria_section_label': mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_mostrarSeccionHistoria_section_label', 'Show translation History section-'), 
       'is-checked': (( pMostrarHistoria) and 'checked="checked"') or '',
    })
    
    
    anOutput.write( u"""  
       <tr class="odd" >
           <td align="left"  valign="center" onclick="pTRAToggleSeccionPresentacion( 'theMostrarLista'); return true;" class="TRAstyle_Clickable"  >                
               <font size="1" >
                   <strong>
                       %(gvSIGi18n_mostrarSeccionLista_section_label)s
                   </strong>
               </font>
           </td>
           <td align="center" valign="center" >                
               <input type="checkbox" class="noborder"  value="on"  %(is-checked)s name="theMostrarLista" id="theMostrarLista" />
           </td>
       </tr>
       \n""" % { 
       'gvSIGi18n_mostrarSeccionLista_section_label': mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_mostrarSeccionLista_section_label', 'Show List section-'), 
       'is-checked': (( pMostrarLista) and 'checked="checked"') or '',
    })

    anOutput.write( u"""  
            </body>
        </table>
        \n""" 
    )
    
    
    
    
    
   
        
    
    
    
    
    anOutput.write( u"""  

        <!-- ########################
        SubSection: Technical presentation options
        #############################-->
        <br/>
        <table id="sct_TechnicalPresentationOptions_control" class="listing nosort" summary="Control for Technical Presentation options" >
            <thead>
                <tr>
                    <th align="left" colspan="2">
                        <font size="2">
                            <strong>
                                %(gvSIGi18n_controlTechnicalPresentacion_title)s
                            </strong>
                        </font>
                        <p class="formHelp">%(gvSIGi18n_controlTechnicalPresentacion_help)s</p>
                    </th>
                </tr>
             </head>
            <tbody>   
            \n""" % {
        'gvSIGi18n_refrescar_action_label':             mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_refrescar_action_label', 'Refresh-'),                
        'gvSIGi18n_controlTechnicalPresentacion_title': mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_controlTechnicalPresentacion_title', 'Technical sections-'),                
        'gvSIGi18n_controlTechnicalPresentacion_help':  mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_controlTechnicalPresentacion_help', 'Control to show or hide page sections relevant to the technology.-'),                
     })
    
 
 
 
    someTechnicalControlOptions = [
        [ 'theRenderUserInterfaceEvents', pRenderUserInterfaceEvents,  'User Interface Events',], 
        [ 'theRenderFormSubmit',    pRenderFormSubmit,  'Form Submit',], 
        [ 'theRenderRequest',       pRenderRequest,     'Request parameters',],         
        [ 'theRenderFullRequest',   pRenderFullRequest, 'Full HTTP Request',], 
        [ 'theRenderAsyncRequest',  pRenderAsyncRequest,'Asynchronous Request and Replies',], 
        [ 'theRenderTimes',         pRenderTimes,       'Processing Times (write, read, total)',],         
        [ 'theRenderProfile',       pRenderProfile,     'Time Profiling (write and read)',],         
    ]
        
    unIndex = 0
    for aTechnicalControlOption in someTechnicalControlOptions:
        unSectionControlFieldName = aTechnicalControlOption[ 0]
        unIsChecked               = aTechnicalControlOption[ 1]
        unTitle                   = aTechnicalControlOption[ 2]
    
        anOutput.write( u"""  
           <tr class="%(row-class)s" >
               <td align="left"  valign="center" onclick="pTRAToggleSeccionPresentacion( '%(unSectionControlFieldName)s'); return true;" class="TRAstyle_Clickable"  >                
                   <font size="1" >
                       <strong>
                           %(unTitle)s
                       </strong>
                   </font>
               </td>
               <td align="center" valign="center" >                
                   <input %(onchangehandler)s type="checkbox" class="noborder"  value="on"  %(is-checked)s name="%(unSectionControlFieldName)s" id="%(unSectionControlFieldName)s" />
               </td>
           </tr>
           \n""" % { 
            'unTitle':                      unTitle,
            'unSectionControlFieldName':    unSectionControlFieldName,   
            'is-checked':                   ( unIsChecked and 'checked="checked"') or '',
            'row-class':                    (( unIndex % 2) and 'odd') or 'even',
            'onchangehandler':              (( unSectionControlFieldName == 'theRenderUserInterfaceEvents') and 'onchange="gTRAMustRenderUserInterfaceEvents = 999; return true;"') or '',
        })
        unIndex += 1
            
        
    anOutput.write( u"""  
            </body>
        </table>
        \n""" 
    )
 
       
        
        
    anOutput.write( u"""  
        <br/>
        <input name="form_submit" style="font-size: 10pt; font-style: italic"  value="%(gvSIGi18n_refrescar_action_label)s" type="submit"/>
        <br/>
        <br/>
         \n""" % {
        'gvSIGi18n_refrescar_action_label':             mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_refrescar_action_label', 'Refresh-'),                
    })
    
         
    return None
    
     

    
















    
def pRenderCollapsibleFiltro( 
    anOutput, 
    unContextualObject, 
    pCodigoIdiomaCursor,
    pTodosNombresModulos, 
    pEstadosIncluidos, 
    pSearchParameters, 
    aTranslationsCache):
    """Render as collapsible the filter section of the translations browser.
    
    """    
           
    mfTranslateI18N     = unContextualObject.fTranslateI18N
    mfAsUnicode         = unContextualObject.fAsUnicode
            
    pRenderCollapsible_Lambda(  anOutput,
        mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_seccionFiltro_title', 'Filter-'),
        u'elid_Filter_collapsible_dl', 
        lambda : pRenderFiltro( 
            anOutput, 
            unContextualObject, 
            pCodigoIdiomaCursor,
            pTodosNombresModulos, 
            pEstadosIncluidos, 
            pSearchParameters, 
            aTranslationsCache
        ),
    )
    
    return None        







def pRenderFiltro( 
    anOutput, 
    unContextualObject, 
    pCodigoIdiomaCursor,
    pTodosNombresModulos, 
    pEstadosIncluidos, 
    pSearchParameters, 
    aTranslationsCache):
    """Render the filter section of the translations browser.
    
    """    
       
    
    mfTranslateI18N     = unContextualObject.fTranslateI18N
    mfAsUnicode         = unContextualObject.fAsUnicode
 
    unTabIndex = 11
    
    anOutput.write( u"""    

        <!-- #################################################################
        SECTION: Filtro para busqueda de TRATraduccion por status
        ################################################################# -->
                      
        <br/>
        <input tabindex=%(tabindex)d name="form_submit" style="font-size: 10pt; font-style: italic"  value="%(gvSIGi18n_refrescar_action_label)s" type="submit"/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <input tabindex=%(tabindex2)d type="button" name="todos" style="font-size: 9pt; "  value="%(gvSIGi18n_todas_label)s" onclick="pTRAResetFiltros(); return true;" class="TRAstyle_Clickable"  />
        <br/>
        \n""" % { 
        'tabindex':                                                    unTabIndex,
        'tabindex2':                                                   unTabIndex + 1,
        'gvSIGi18n_refrescar_action_label':                    mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_refrescar_action_label', 'Refresh-'),                
        'gvSIGi18n_todas_label':                               mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_todas_label', 'All-'),                
    })
    
    
    unTabIndex += 2

    anOutput.write( u"""    

        <!-- #################################################################
        Subsection: Filtro por estados 
        ################################################################# -->
        <table class="listing nosort" id="sct_Filter_Status" >
            <thead>
                <tr>
                    <th  valign="baseline" align="left" onclick="pTRAResetFiltrosEstados(); return true;" class="TRAstyle_Clickable"  >
                        <font size="2">
                            <strong>
                                %(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label)s
                            </strong>
                        </font>
                    </th>
            \n""" % { 
        'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label': mfTranslateI18N( 'gvSIGi18n',  'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label', 'Translation status-'),
    })

    
    for unEstadoTraduccion in cTodosEstados:                                  
        anOutput.write( u"""                 
            <th align="center" valign="baseline" onclick="pTRAToggleFiltroEstado( '%(unEstadoTraduccion)s'); return true;" class="TRAstyle_Clickable"  >
                <font size="1" >
                    <span>%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label)s</span>
                </font>
                <br/>
                <img  alt="TranslationStatus_%(unEstadoTraduccion)s" src="%(portal_url)s/%(estado-icon)s" title="%(unEstadoTraduccion)s" />                        
            </th>
            \n""" % { 
            'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label': mfTranslateI18N( 'gvSIGi18n',  'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_%s' % unEstadoTraduccion, unEstadoTraduccion),
            'portal_url':               unContextualObject.absolute_url(), 
            'unEstadoTraduccion':       unEstadoTraduccion,
            'estado-icon':              cIconsDict.get( unEstadoTraduccion, 'tra_pendiente.gif'), 
        })
        
    anOutput.write( u"""    
                </tr>
            </thead>      
            <tbody>  
                <tr>
                    <td align="center" onclick="pTRAResetFiltrosEstados(); return true;" class="TRAstyle_Clickable"  >
                        <img alt="%(gvSIGi18n_todosPlus_action_label)s"   src="%(portal_url)s/add_icon.gif" title="%(gvSIGi18n_todosPlus_action_label)s" />
                        %(gvSIGi18n_todosEstados_action_label)s
                    </td>
                    \n""" % { 
        'gvSIGi18n_filtro_label':                               mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_filtro_section_label', 'Filter-'),
        'gvSIGi18n_limpiarfiltro_action_label':                 mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_todas_label', 'All-'),
        'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label':  mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label', 'Status-'),
        'gvSIGi18n_todosEstados_action_label':                  mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_todosEstados_action_label', 'Any status-'),
        'gvSIGi18n_todosPlus_action_label':                     mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_todosPlus_action_label', '+'),
        'portal_url':                                                   unContextualObject.absolute_url(), 
    })
    
    for unEstadoTraduccion in cTodosEstados:
        anOutput.write( u"""                                                                     
            <td  align="center" bgcolor="%(pBGColor)s" >
                <input tabindex=%(tabindex)d type="checkbox" class="noborder" %(is-checked)s name="theEstadosAIncluir" id="theEstadosAIncluir_%(unEstadoTraduccion)s" value="%(unEstadoTraduccion)s" />
            </td>  
            \n""" % { 
            'tabindex':         unTabIndex,
            'unEstadoTraduccion': unEstadoTraduccion, 
            'is-checked' :      (( unEstadoTraduccion in pEstadosIncluidos) and 'checked="checked"') or '',
            'pBGColor':         cBGColorsDict.get( unEstadoTraduccion,  cBGColorsDict[ cEstadoTraduccionPendiente]),
            'pFGColor':         cFGColorsDict.get( unEstadoTraduccion,  cBGColorsDict[ cEstadoTraduccionPendiente]),
        })                                                                
    
        unTabIndex += 1
   
    anOutput.write( u""" 
                </tr> 
            </tbody>
        </table>
        \n""" 
    )
        
     
 

    
    
    
 
    anOutput.write( u""" 

        <!-- ########################
        SubSection: Filter  String symbol and Translation
        #############################-->
                                             
        <table class="listing nosort" id="sct_Filter_SymbolAndTranslation" >
            <thead>
                <tr>
                    <th  align="left"  colspan="2">
                        <font size="2">
                            <strong>
                                %(gvSIGi18n_BusquedasPorPalabrasContenidasEnSimboloOTraduccion_title)s
                            </strong>
                        </font>
                    </th>
                </tr>
            </thead>      
            <tbody>  
            \n""" % { 
        'gvSIGi18n_BusquedasPorPalabrasContenidasEnSimboloOTraduccion_title':  mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_BusquedasPorPalabrasContenidasEnSimboloOTraduccion_title',    'Filter by words in the symbol or the translation-'), 
    })            

             
    
              
    
    anOutput.write( u""" 

        <!-- ########################
        SubSection: Filter by String Symbol 
        #############################-->   
                                   
        <tr class="even" >
            <td align="left" valign="baseline" >
                %(gvSIGi18n_TRATraduccion_attr_simbolo_label)s
            </td>
            <td align="left" valign="baseline"  >
                <input tabindex=%(tabindex)d name="theSearchSimbolo" id="theSearchSimbolo" style="font-size: 10pt;" size="36" value="%(simbolo)s" /> 
                <p class="formHelp">
                    <span>%(gvSIGi18n_TRATraduccion_attr_simbolo_help)s</span>
                    <br>
                    <span >%(gvSIGi18n_searchBySimbolo_help)s</span>
                </p>
            </td>
        </tr>
        \n""" % { 
        'tabindex':                                             unTabIndex,
        'simbolo':                                              mfAsUnicode( pSearchParameters[ 'simbolo']),
        'gvSIGi18n_TRATraduccion_attr_simbolo_label':   aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_simbolo_label'],
        'gvSIGi18n_TRATraduccion_attr_simbolo_help':    mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_TRATraduccion_attr_simbolo_help',  'The symbol of the string to translate.-'), 
        'gvSIGi18n_searchBySimbolo_help':               mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_searchBySimbolo_help',             'Enter words to search for in the string symbols. Wildcards (* and ?) are permitted.-'), 
    })
    
    
    unTabIndex += 1
    
    
    
    unasSizesIdioma = TRASizesIdioma( pCodigoIdiomaCursor)

    
    anOutput.write( u""" 

        <!-- ########################
        SubSection: Filter by Translation 
        #############################-->  
        
        <tr class="odd" >
            <td align="left" valign="baseline" >
                %(gvSIGi18n_TRATraduccion_attr_cadenaTraducida_label)s
            </td>
            <td align="left" valign="baseline" >
                <input tabindex=%(tabindex)d  name="theSearchCadenaTraducida" id="theSearchCadenaTraducida" style="font-size: %(font-size)dpt;" size="%(field-size)d" value="%(cadenaTraducida)s" /> 
                <p class="formHelp">
                    <span >%(gvSIGi18n_TRATraduccion_attr_cadenaTraducida_help)s</span>
                    <br>
                    <span >%(gvSIGi18n_searchByTranslation_help)s</span>
                </p>
            </td>
        </tr>
        \n""" % { 
        'tabindex':                                             unTabIndex,
        'cadenaTraducida':                                              mfAsUnicode( pSearchParameters[ 'cadenaTraducida']),
        'gvSIGi18n_TRATraduccion_attr_cadenaTraducida_label':   mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_TRATraduccion_attr_cadenaTraducida_label', 'Translation-'), 
        'font-size':                                                    unasSizesIdioma[ 'edit_font_size'],
        'field-size':                                                   unasSizesIdioma[ 'filter_field_size'] / 2,
        'gvSIGi18n_TRATraduccion_attr_cadenaTraducida_help':    mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_TRATraduccion_attr_cadenaTraducida_help',  'The translation of the string into the language.-'), 
        'gvSIGi18n_searchByTranslation_help':                   mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_searchByTranslation_help',                 'Enter words  to search for in the translations into this language. Wildcards (* and ?) are permitted.-'), 
    })
        
    unTabIndex += 1    

    anOutput.write( u"""  
            </tbody>
        </table>
        \n""")                                 
     
    
    
    
    
    
    
    
    
    anOutput.write( u""" 

        <!-- ########################
        SubSection: Filter by Users and dates of state change 
        #############################-->  
        
        <table class="listing nosort" id="sct_Filter_UsersAndDates" >
            <thead>
                <tr>
                    <th align="left" colspan="3">
                        <font size="2">
                            <strong>
                                %(gvSIGi18n_BusquedasPorEventos_title)s
                            </strong>
                        </font>
                        <br/>
                        <font size="1">
                            <span class="formHelp" >
                                %(gvSIGi18n_BusquedasPorEventos_formatoFechaISO_help)s
                                &ensp;
                                %(gvSIGi18n_BusquedasPorEventos_sePermitenFechasParciales_help)s
                            </span>
                        </font>
                    </th>
                </tr>
                <tr>
                    <th align="center" >
                        <strong>%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label)s</strong>
                    </th>
                    <th align="left">
                        <strong>%(gvSIGi18n_BusquedasPorEventos_usuario_title)s</strong>
                    </th>
                    <th align="left">
                        <strong>%(gvSIGi18n_BusquedasPorEventos_despuesDeFecha_title)s
                            &ensp;-&ensp;
                            %(gvSIGi18n_BusquedasPorEventos_antesDeFecha_title)s</strong>
                    </th>
                </tr>
            </thead>      
            <tbody>  
            \n""" % { 
        'gvSIGi18n_BusquedasPorEventos_formatoFechaISO_help':   mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_BusquedasPorEventos_formatoFechaISO_help',     'Dates in ISO format YYYY-MM-DD HH:MM:SS'), 
        'gvSIGi18n_BusquedasPorEventos_sePermitenFechasParciales_help':   mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_BusquedasPorEventos_sePermitenFechasParciales_help',     'Incomplete dates and times are allowed-'), 
        'gvSIGi18n_BusquedasPorEventos_despuesDeFecha_title':   mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_BusquedasPorEventos_despuesDeFecha_title',     'After-'), 
        'gvSIGi18n_BusquedasPorEventos_antesDeFecha_title':     mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_BusquedasPorEventos_antesDeFecha_title',       'Before-'), 
        'gvSIGi18n_BusquedasPorEventos_title':                  mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_BusquedasPorEventos_title',                    'Filter by users and dates of status change events-'), 
        'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label':  mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label',    'Translation status-'), 
        'gvSIGi18n_BusquedasPorEventos_usuario_title':          mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_BusquedasPorEventos_usuario_title',            'User-'), 
    })            
    
    
    anOutput.write( u"""     
               <tr class="even">
                    <td align="left" valign="baseline" bgColor="%(pBGcolor-Pendiente)s">
                        <img  alt="TranslationStatus_%(gvSIGi18n_TRATraduccion_Creada)s" src="%(portal_url)s/add_icon.gif" title="%(gvSIGi18n_TRATraduccion_Creada)s" />                        
                        <font color="%(pFGcolor-Pendiente)s"><strong>%(gvSIGi18n_TRATraduccion_Creada)s</strong></font>
                    </td>
                    <td align="left" valign="baseline" >
                        <input tabindex=%(tabindex_creador)d style="font-size: 8pt;" size="12"  name="theSearchUsuarioCreador" id="theSearchUsuarioCreador" value="%(usuarioCreador)s" />
                    </td>
                    <td align="left" valign="baseline" >
                        <input tabindex=%(tabindex_fechaCreacionInicial)d style="font-size: 8pt;" size="22"  name="theSearchFechaCreacionInicial" id="theSearchFechaCreacionInicial" value="%(fechaCreacionInicial)s" />
                        <input tabindex=%(tabindex_fechaCreacionFinal)d style="font-size: 8pt;" size="22"  name="theSearchFechaCreacionFinal"   id="theSearchFechaCreacionFinal"   value="%(fechaCreacionFinal)s" />
                    </td>
                </tr>
                <tr class="even">
                    <td align="left" valign="baseline" bgColor="%(pBGcolor-Traducida)s">
                        <img  alt="TranslationStatus_%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Traducida)s" src="%(portal_url)s/%(estado-icon-Traducida)s" title="%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Traducida)s" />                        
                        <font color="%(pFGcolor-Traducida)s"><strong>%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Traducida)s</strong></font>
                    </td>
                    <td align="left" valign="baseline" >
                        <input tabindex=%(tabindex_traductor)d style="font-size: 8pt;" size="12"  name="theSearchUsuarioTraductor" id="theSearchUsuarioTraductor" value="%(usuarioTraductor)s" />
                    </td>
                    <td align="left" valign="baseline" >
                        <input tabindex=%(tabindex_fechaTraduccionInicial)d style="font-size: 8pt;" size="22"  name="theSearchFechaTraduccionInicial" id="theSearchFechaTraduccionInicial" value="%(fechaTraduccionInicial)s" />
                        <input tabindex=%(tabindex_fechaTraduccionFinal)d style="font-size: 8pt;" size="22"  name="theSearchFechaTraduccionFinal"   id="theSearchFechaTraduccionFinal"   value="%(fechaTraduccionFinal)s" />
                    </td>
                </tr>
                <tr class="odd">
                    <td align="left" valign="baseline" bgColor="%(pBGcolor-Revisada)s">
                        <img  alt="TranslationStatus_%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Revisada)s" src="%(portal_url)s/%(estado-icon-Revisada)s" title="%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Revisada)s" />                        
                        <font color="%(pFGcolor-Revisada)s"><strong>%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Revisada)s</strong></font>
                    </td>
                    <td align="left" valign="baseline" >
                        <input tabindex=%(tabindex_revisor)d  style="font-size: 8pt;" size="12"  name="theSearchUsuarioRevisor" id="theSearchUsuarioRevisor" value="%(usuarioRevisor)s" />
                    </td>
                    <td align="left" valign="baseline" >
                        <input tabindex=%(tabindex_fechaRevisionInicial)d  style="font-size: 8pt;" size="22"  name="theSearchFechaRevisionInicial" id="theSearchFechaRevisionInicial" value="%(fechaRevisionInicial)s" />
                        <input tabindex=%(tabindex_fechaRevisionFinal)d style="font-size: 8pt;" size="22"  name="theSearchFechaRevisionFinal"   id="theSearchFechaRevisionFinal"   value="%(fechaRevisionFinal)s" />
                    </td>
                </tr>
                <tr class="even">
                    <td align="left" valign="baseline" bgColor="%(pBGcolor-Definitiva)s">
                        <img  alt="TranslationStatus_%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Definitiva)s" src="%(portal_url)s/%(estado-icon-Definitiva)s" title="%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Definitiva)s" />                        
                        <font color="%(pFGcolor-Definitiva)s"><strong>%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Definitiva)s</strong></font>
                    </td>
                    <td align="left" valign="baseline" >
                        <input tabindex=%(tabindex_coordinador)d  style="font-size: 8pt;" size="12"  name="theSearchUsuarioCoordinador" id="theSearchUsuarioCoordinador" value="%(usuarioCoordinador)s" />
                    </td>
                    <td align="left" valign="baseline" >
                        <input tabindex=%(tabindex_fechaDefinitivaInicial)d style="font-size: 8pt;" size="22"  name="theSearchFechaDefinitivoInicial" id="theSearchFechaDefinitivoInicial" value="%(fechaDefinitivaInicial)s" />
                        <input tabindex=%(tabindex_fechaDefinitivaFinal)d style="font-size: 8pt;" size="22"  name="theSearchFechaDefinitivoFinal"   id="theSearchFechaDefinitivoFinal"   value="%(fechaDefinitivaFinal)s" />
                    </td>
                </tr>
            </tbody>
        </table>        
        \n""" % { 
            'tabindex_creador':                     unTabIndex,
            'tabindex_fechaCreacionInicial':        unTabIndex + 1,
            'tabindex_fechaCreacionFinal':          unTabIndex + 2,
            'tabindex_traductor':                   unTabIndex + 3,
            'tabindex_fechaTraduccionInicial':      unTabIndex + 4,
            'tabindex_fechaTraduccionFinal':        unTabIndex + 5,
            'tabindex_revisor':                     unTabIndex + 6,
            'tabindex_fechaRevisionInicial':        unTabIndex + 7,
            'tabindex_fechaRevisionFinal':          unTabIndex + 8,
            'tabindex_coordinador':                 unTabIndex + 9,
            'tabindex_fechaDefinitivaInicial':      unTabIndex + 10,
            'tabindex_fechaDefinitivaFinal':        unTabIndex + 11,
            'portal_url':               unContextualObject.absolute_url(), 
            'gvSIGi18n_TRATraduccion_Creada':  aTranslationsCache['gvSIGi18n_TRATraduccion_Creada'],
            'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Traducida':   mfTranslateI18N( 'gvSIGi18n',  'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_%s' % cEstadoTraduccionTraducida, cEstadoTraduccionTraducida),
            'estado-icon-Traducida':    cIconsDict.get( cEstadoTraduccionTraducida, 'tra_traducida.gif'), 
            'usuarioCreador':           mfAsUnicode( pSearchParameters[ 'usuarioCreador']),
            'fechaCreacionInicial':     mfAsUnicode( pSearchParameters[ 'fechaCreacionInicial']),
            'fechaCreacionFinal':       mfAsUnicode( pSearchParameters[ 'fechaCreacionFinal']),
            'usuarioTraductor':         mfAsUnicode( pSearchParameters[ 'usuarioTraductor']),
            'fechaTraduccionInicial':   mfAsUnicode( pSearchParameters[ 'fechaTraduccionInicial']),
            'fechaTraduccionFinal':     mfAsUnicode( pSearchParameters[ 'fechaTraduccionFinal']),
            'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Revisada':    mfTranslateI18N( 'gvSIGi18n',  'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_%s' % cEstadoTraduccionRevisada, cEstadoTraduccionRevisada),
            'estado-icon-Revisada':     cIconsDict.get( cEstadoTraduccionRevisada, 'tra_revisada.gif'), 
            'pBGcolor-Pendiente':       cBGColorsDict[ cEstadoTraduccionPendiente],  
            'pBGcolor-Traducida':       cBGColorsDict[ cEstadoTraduccionTraducida],  
            'pBGcolor-Revisada':        cBGColorsDict[ cEstadoTraduccionRevisada],  
            'pBGcolor-Definitiva':      cBGColorsDict[ cEstadoTraduccionDefinitiva],  
            'pFGcolor-Pendiente':       cFGColorsDict[ cEstadoTraduccionPendiente],  
            'pFGcolor-Traducida':       cFGColorsDict[ cEstadoTraduccionTraducida],  
            'pFGcolor-Revisada':        cFGColorsDict[ cEstadoTraduccionRevisada],  
            'pFGcolor-Definitiva':      cFGColorsDict[ cEstadoTraduccionDefinitiva],  
            'usuarioRevisor':           mfAsUnicode( pSearchParameters[ 'usuarioRevisor']),
            'fechaRevisionInicial':     mfAsUnicode( pSearchParameters[ 'fechaRevisionInicial']),
            'fechaRevisionFinal':       mfAsUnicode( pSearchParameters[ 'fechaRevisionFinal']),
            'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Definitiva':  mfTranslateI18N( 'gvSIGi18n',  'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_%s' % cEstadoTraduccionDefinitiva, cEstadoTraduccionDefinitiva),
            'estado-icon-Definitiva':   cIconsDict.get( cEstadoTraduccionDefinitiva, 'tra_definitiva.gif'), 
            'usuarioCoordinador':       mfAsUnicode( pSearchParameters[ 'usuarioCoordinador']),
            'fechaDefinitivaInicial':   mfAsUnicode( pSearchParameters[ 'fechaRevisionInicial']),
            'fechaDefinitivaFinal':     mfAsUnicode( pSearchParameters[ 'fechaRevisionFinal']),
        })
     
     
   
    unTabIndex += 12   

    
    
    
    pRenderFiltroModulos(
        anOutput, 
        unContextualObject, 
        pTodosNombresModulos, 
        pSearchParameters,
        aTranslationsCache,
    )
    
    
           
                    

    
    
    
    
    anOutput.write( u""" 

         <!-- ########################
        SubSection: Search exact String Id
        #############################-->
                                             
        <table class="listing nosort" id="sct_Filter_SymbolAndTranslation" >
            <thead>
                <tr>
                    <th  align="left"  colspan="2">
                        <font size="2">
                            <strong>
                                %(gvSIGi18n_BusquedasPorIdCadena_title)s
                            </strong>
                        </font>
                    </th>
                </tr>
            </thead>      
            <tbody>  
                <tr class="even" >
                    <td align="left" valign="baseline" >
                        %(gvSIGi18n_TRACadena_attr_id_label)s
                    </td>
                    <td align="left" valign="baseline" >
                        <input tabindex=%(tabindex)d style="font-size: 8pt;" size="12"  name="theSearchIdCadena" id="theSearchIdCadena" value="" />
                        <p class="formHelp">
                            <span>%(gvSIGi18n_TRACadena_attr_id_help)s</span>
                            <br>
                            <span>%(gvSIGi18n_searchById_help)s</span>
                        </p>
                    </td> 
                </tr>        
           </tbody>
        </table>
        \n""" % { 
        'tabindex':                                             unTabIndex,
        'gvSIGi18n_BusquedasPorIdCadena_title': mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_BusquedasPorIdCadena_title',    'Search by exact string symbol id-'), 
        'gvSIGi18n_TRACadena_attr_id_label':    mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_TRACadena_attr_id_label',    'String Id-'), 
        'gvSIGi18n_TRACadena_attr_id_help':     mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_TRACadena_attr_id_help',     'Unique identifier for a string, and its translations to any language.-'), 
        'gvSIGi18n_searchById_help':            mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_searchById_help',            'Enter the exact identifier of the string to search for.-'), 
    })                                                

                           
           
      
    unTabIndex += 1
    
    anOutput.write( u"""     
        <br/>
        <input tabindex=%(tabindex)d name="form_submit" style="font-size: 10pt; font-style: italic"  value="%(gvSIGi18n_refrescar_action_label)s" type="submit"/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <input  tabindex=%(tabindex2)d type="button" name="todos" style="font-size: 9pt"  value="%(gvSIGi18n_todas_label)s" onclick="pTRAResetFiltros(); return true;" class="TRAstyle_Clickable"  />
        <br/>
        <br/>
        \n""" % {
        'tabindex':                                             unTabIndex,
        'tabindex2':                                            unTabIndex + 1,
        'gvSIGi18n_refrescar_action_label':             mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_refrescar_action_label', 'Refresh-'),                
        'gvSIGi18n_todas_label':                        mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_todas_label', 'All-'),                
    })   
        
    
    
       
    return None












def pRenderFiltroModulos( 
    anOutput, 
    unContextualObject, 
    pTodosNombresModulos, 
    pSearchParameters,
    aTranslationsCache):
    """Render  the section to filter by modules.
    
    """    
    
    mfTranslateI18N     = unContextualObject.fTranslateI18N
    mfAsUnicode         = unContextualObject.fAsUnicode
    mfCRs2BRs           = unContextualObject.fCRs2BRs
    
    
    
    unosNombresModulos = pSearchParameters.get( 'nombresModulos', '')
    
    if not unosNombresModulos:
        unosNombresModulos = []
    else:    
        if not ( unosNombresModulos.__class__.__name__ in [ 'list', 'tuple',]):
            unosNombresModulos = [ unosNombresModulos,]
            
            
    
    anOutput.write( u"""  
        
        <!-- #################################################################
        SECTION: Selection of modules for translations to explore
        ################################################################# -->                           
    
   
        <table id="sct_Filter_Modules_Multi" class="listing nosort" summary="Filter by modules" >
            <thead>
                <tr>
                    <th colspan="2" align="left"   >
                        <span><font size="2"><strong>%(gvSIGi18n_modulesFilter_title)s</strong></font></span>
                        <br/>
                        <span class="formHelp">%(gvSIGi18n_modulesFilter_help)s</span>
                    </th>
                </tr>
                <tr>
                    <th align="center" >
                    </th>   
                    <th  align="center" >
                        <input type="checkbox"  class="noborder"  value=""  name="cid_TRAToggleAllModules" id="cid_TRAToggleAllModules" 
                            onchange="pTRAToggleAllModules(); return true;" />
                            
                    </th>
                </tr>
            </head>
            <tbody>   
            \n""" % {
        'portal_url':                                               unContextualObject.absolute_url(), 
        'gvSIGi18n_seleccionarTodos_label':                 mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_seleccionarTodos_label', 'All-'),
        'gvSIGi18n_seleccionarNinguno_label':               mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_seleccionarNinguno_label', 'None'),
        'gvSIGi18n_modulesFilter_title':                    mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_modulesFilter_title', 'Modules filter-'),
        'gvSIGi18n_modulesFilter_help':                     mfCRs2BRs( mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_modulesFilter_help', 'Select the modules with the translations you are interested in.\nIf no module is selected then there is no restriction on translation modules.\nThe --unspecified-- module represents those strings that are not associated with any module.-')),
        'gvSIGi18n_refrescar_action_label':                 mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_refrescar_action_label', 'Refresh-'),                
    })
    
    unIndexRowModulo = 0 
    for unNombreModulo in pTodosNombresModulos:  
                                 
        anOutput.write( u"""                                                                                                                                                                     
            <tr class="%(class-row-modulo)s" >
                <td align="left" valign="center" onclick="toggleModulo( '%(index-modulo)s'); return true;" class="TRAstyle_Clickable"  >                
                    <font size="1" >
                        <strong>
                            %(nombre-modulo)s
                        </strong>
                    </font>
                </td>
                <td align="center" valign="center" >                
                    <input type="checkbox" class="noborder"  value="%(nombre-modulo)s"  %(modulo-checked)s name="theSearchNombresModulos" 
                        id="theNombreModulo_%(index-modulo)s" />
                </td>
            </tr>
            \n""" % { 
            'index-modulo':         str( unIndexRowModulo),
            'class-row-modulo':     cClasesFilas[ unIndexRowModulo % 2],
            'nombre-modulo':        mfAsUnicode( unNombreModulo),        
            'modulo-checked':       (( unNombreModulo in unosNombresModulos) and 'checked="checked"') or '',
        } )
        
        unIndexRowModulo += 1

    anOutput.write( u"""  
                <tr class="%(class-row-modulo)s" >
                    <td align="left" valign="center" onclick="toggleModulo( '%(index-modulo)s'); return true;" class="TRAstyle_Clickable"  >                
                        <font size="1" >
                            <strong>
                                %(nombre-modulo-NoEspecificado)s
                            </strong>
                        </font>
                    </td>
                    <td align="center" valign="center" >                
                        <input type="checkbox" class="noborder"  value="%(no-especificado)s"  %(modulo-checked)s name="theSearchNombresModulos" 
                            id="theNombreModulo_NoEspecificado" />
                    </td>
                </tr>
            </body>
        </table>
        <br/>
         \n""" % {
        'index-modulo':                                    str( unIndexRowModulo),
        'class-row-modulo':                                cClasesFilas[ unIndexRowModulo % 2],
        'no-especificado':                                 cNombreModuloNoEspecificadoInputValue,
        'nombre-modulo-NoEspecificado':                     mfTranslateI18N( 'gvSIGi18n', cNombreModuloNoEspecificadoLabel_MsgId, 'Unspecified module-'),                
        'modulo-checked':                                  (( cNombreModuloNoEspecificadoInputValue in unosNombresModulos) and 'checked="checked"') or '',
        'nombre-modulo':                                   mfAsUnicode( unNombreModulo),        
    })

    return None
                
  

















    
def pRenderCollapsibleInforme( 
    anOutput, 
    unContextualObject, 
    pEstadosIncluidos, 
    pInformeEstadosTodasCadenas, 
    pInformeEstadosFiltrados,
    aTranslationsCache):
    """Render as collapsible the summary section of the translations browser.
    
    """    
    
    mfTranslateI18N     = unContextualObject.fTranslateI18N
    mfAsUnicode         = unContextualObject.fAsUnicode
            
    pRenderCollapsible_Lambda(  anOutput,
        aTranslationsCache[ 'gvSIGi18n_seccionInformeSumario_title'],
        u'elid_Summary_collapsible_dl', 
        lambda : pRenderInforme( 
            anOutput, 
            unContextualObject, 
            pEstadosIncluidos, 
            pInformeEstadosTodasCadenas,  
            pInformeEstadosFiltrados,
            aTranslationsCache
        ),
        False,
    )
    
    return None        











def pRenderInforme( 
    anOutput, 
    unContextualObject, 
    pEstadosIncluidos, 
    pInformeEstadosTodasCadenas, 
    pInformeEstadosFiltrados,
    aTranslationsCache):
    """Render the summary section of the translations browser.
    
    """    
       
    mfTranslateI18N     = unContextualObject.fTranslateI18N
    mfAsUnicode         = unContextualObject.fAsUnicode
    
    
    
    pNumeroCadenas           = pInformeEstadosTodasCadenas[ 'Total'][ 1]
    pNumeroCadenasFiltradas  = pInformeEstadosFiltrados[    'Total'][ 1]
    
    cInformeBiggerFontSize = '1'    
    
    anOutput.write( u"""    

        <!-- #################################################################
        SECTION: Informe de traducciones en TRAIdioma:
        Total de cadenas en catalogo, 
        y numero y porcentaje de Traducciones en cada estado
        con una barra coloreada mostrando los porcentajes en cada estado
        ################################################################# -->
                     
        <table cellspacing="2" cellpadding="2" frame="void" id="status_report" >
             <thead><tr><th  colspan="11" ></th></tr></thead>      
             <tbody>   
        \n"""
    )
    
    
    
    
        
    anOutput.write( u"""    

         <!-- ########################
        SubSection: All Cadenas percentages Colored horizontal Bar 
        #############################-->  
                                     
        <tr height="8">
            <td align="center" valign="center" colspan="11" >
                <table width="100%%" cellspacing="0" cellpadding="0"><tbody>
                    <tr height="8" >
                    \n""" 
    )  
    
    for unEstado in cTodosEstados:
        if pInformeEstadosTodasCadenas[ unEstado][ 2] > 0:
            anOutput.write( u"""                 
                 <td bgcolor="%(pBGColor)s" width="%(pWidth)d" />
                \n""" % { 
                'pBGColor': cBGColorsDict[ unEstado ], 
                'pWidth': pInformeEstadosTodasCadenas[ unEstado][2], 
            })
         
    anOutput.write( u"""                 
                    </tr>
                </tbody>
                </table>
            </td>
        </tr>
        \n""" 
    )

    
    
    
    
    
    
    
    anOutput.write( u"""                 
         <!-- ########################
        SubSection: Row with a column for each state with its coded color and name
        #############################-->  
                                                    
        <tr class="even" >
            <td/>
            <td align="center" valign="top" colspan="2">
                <font size="%(cInformeBiggerFontSize)s">%(gvSIGi18n_total_label)s</font>
            </td>
        \n""" % { 
        'gvSIGi18n_ocultar_action_label'  : mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_ocultar_action_label', 'Hide-'), 
        'gvSIGi18n_informe_section_label' : mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_informe_section_label', 'Summary-'),  
        'gvSIGi18n_total_label':            mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_total_label', 'Total-'), 
        'cInformeBiggerFontSize':                   cInformeBiggerFontSize,
    })

    for unEstado in cTodosEstados:                                  
        anOutput.write( u"""                 
            <td align="center" valign="top" colspan="2" >
                <font size="%(cInformeBiggerFontSize)s" >
                    <img  alt="TranslationStatus_%(unEstado)s" src="%(portal_url)s/%(estado-icon)s" title="%(unEstado)s" />                        
                    %(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label)s
                </font>
                <br/>  
                <table align="center" width="100%%" cellspacing="0" cellpadding="0" frame="void" >
                    <tr height="8" ><td valign="top" bgColor="%(pBGcolor)s" /></tr>
                </table>  
            </td>
            \n""" % { 
            'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label': mfTranslateI18N( 'gvSIGi18n','gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_%s' % unEstado, unEstado),
            'pBGcolor':                                                    cBGColorsDict[ unEstado],  
            'cInformeBiggerFontSize':                                      cInformeBiggerFontSize,
            'unEstado':                                                    unEstado,
            'estado-icon':                                                 cIconsDict.get( unEstado, 'tra_pendiente.gif'), 
            'portal_url':                                                  unContextualObject.absolute_url(), 
    })
                                                    
    anOutput.write( u"""                 
        </tr>   
        \n""" 
    )
                       
    
    


    anOutput.write( u"""                 
         <!-- ########################
        SubSection: Row for All Cadenas Total Number and percentage  of records in each state
        #############################-->  
                                     
        <tr class="odd" >
            <td align="left" valign="baseline" >
                <font size="%(cInformeBiggerFontSize)s" >%(gvSIGi18n_todastraduccionesidioma_label)s</font>
            </td>
            <td align="right" valign="baseline" >
                <font size="%(cInformeBiggerFontSize)s" >%(pNumeroCadenas)d</font>
            </td>
            <td align="right" valign="baseline" >
                &nbsp;
            </td>
            \n""" % { 
        'gvSIGi18n_todastraduccionesidioma_label': mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_todas_label', 'All-'),
        'pNumeroCadenas':                                  pNumeroCadenas,
        'cInformeBiggerFontSize':                          cInformeBiggerFontSize,
    })

    for unEstado in cTodosEstados:                                  
        anOutput.write( u"""                                                         
            <td align="right" valign="baseline" >
                <font size="%(cInformeBiggerFontSize)s" >%(pNumeroTraduccionesEstado)d</font>
            </td>
            <td align="right" valign="baseline" >
                <font size="1" >%(pPorcentajeTraduccionesEstado)d%%</font>
            </td>
            \n""" % { 
            'pNumeroTraduccionesEstado':      pInformeEstadosTodasCadenas[ unEstado][ 1], 
            'pPorcentajeTraduccionesEstado':  pInformeEstadosTodasCadenas[ unEstado][ 2],
            'cInformeBiggerFontSize':         cInformeBiggerFontSize,
        })

    anOutput.write( u"""                                                         
        </tr> 
        \n"""
    )
        
        
        
        
        
    unValoresInformeFiltradoIgualInformeTodos = [ pInformeEstadosFiltrados[ unTotalOEstado ][ 1] == pInformeEstadosTodasCadenas[ unTotalOEstado][ 1] for unTotalOEstado in pInformeEstadosTodasCadenas.keys()] == [True] * len( pInformeEstadosTodasCadenas.keys())
        
    if not unValoresInformeFiltradoIgualInformeTodos:
        anOutput.write( u"""                                                         
                                
            <!-- ########################
            SubSection: Row for Number and percentage  of Filtered records in each state
            #############################-->  
                             
            <tr height="4" bgcolor="silver" ><td colspan="11" /></tr>                                
            <tr class="odd" >
                <td align="left" valign="baseline" >%(gvSIGi18n_traduccionesfiltradasidioma_label)s</td>
                \n""" % { 
            'gvSIGi18n_traduccionesfiltradasidioma_label': mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_traduccionesfiltradasidioma_label', 'Filtered-'),
        })                                        

        anOutput.write( u"""                                                         
            <td align="right" valign="baseline" >
                 <font size="%(cInformeBiggerFontSize)s" >%(pNumeroCadenasFiltradas)d</font>
            </td>
            <td align="right" valign="baseline" >
                <font size="1" >%(pPorcentajeTotal)d%%</font>    
            </td>
            \n""" % { 
            'pNumeroCadenasFiltradas':  pNumeroCadenasFiltradas,
            'pPorcentajeTotal':         pInformeEstadosFiltrados[ 'Total'][ 2],
            'cInformeBiggerFontSize':   cInformeBiggerFontSize,
        })
                                            
        for unEstado in cTodosEstados:
            if unEstado in pEstadosIncluidos:
                anOutput.write( u"""                                                         
                    <td align="right" valign="baseline" >
                        <font size="%(cInformeBiggerFontSize)s" >%(pNumeroTraduccionesEstado)d</font>
                    </td>
                    <td align="right" valign="baseline" >
                        <font size="1" >%(pPorcentajeTraduccionesEstado)d%%</font>
                    </td>
                    \n""" % { 
                    'pNumeroTraduccionesEstado':        pInformeEstadosFiltrados[ unEstado][ 1], 
                    'pPorcentajeTraduccionesEstado':    pInformeEstadosFiltrados[ unEstado][ 2],
                    'cInformeBiggerFontSize':         cInformeBiggerFontSize,
                })
            else:
                anOutput.write( u"""                                                         
                    <td align="right" valign="baseline" >&nbsp;</td>
                    <td align="right" valign="baseline" >&nbsp;</td>
                    \n""" 
                )                        
        
    # ACV 20090315 save space: there is no need to waste a row to say "all"
    #else:
        #anOutput.write( u"""                                                                         
                #<td align="right" valign="baseline" ><font size="%(cInformeBiggerFontSize)s">%(gvSIGi18n_todas_label)s</font></td>
                #<td align="right" valign="baseline" >100%%</font></td>
                #<td  colspan="9">&nbsp;</td>
            #</tr> 
            #\n""" % { 
            #'gvSIGi18n_todas_label': mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_todas_label', 'All-'),
            #'cInformeBiggerFontSize':         cInformeBiggerFontSize,
        #})
    
        
        
        
        
        
    if not unValoresInformeFiltradoIgualInformeTodos:
        anOutput.write( u""" 
                    
            <!-- ########################
            SubSection: Filtered Cadenas percentages Colored horizontal Bar
            #############################-->  
                    
            <tr height="8"  >
                <td align="center" valign="center"  colspan="11" >
                    <table width="100%%" cellspacing="0" cellpadding="0" frame="void" >
                        <tr height="8" >
                        \n""" 
        )
        
        for unEstado in cTodosEstados:
            if pInformeEstadosFiltrados[ unEstado][ 2] > 0:
                anOutput.write( u"""                                                                             
                    <td bgcolor="%(pBGColor)s" width="%(pWidth)d" />
                    \n""" % { 
                    'pBGColor': cBGColorsDict[ unEstado ], 
                    'pWidth': pInformeEstadosFiltrados[ unEstado][2], 
                })  

                             
        anOutput.write( u"""                 
                        </tr>
                     </table>
                 </td>
             </tr>
            \n""" 
        )
                    
 
    anOutput.write( u"""                                                                                                                                 
            </tbody>
        </table>        
        \n"""
    )        

    return None







































def pRenderEditorDetail( 
    anOutput, 
    unContextualObject, 
    pMostrarHistoria, 
    aTranslationsCache):
    """Render the details subsection of the editor section of the translations browser.
    
    """
     
    mfTranslateI18N     = unContextualObject.fTranslateI18N
    mfAsUnicode         = unContextualObject.fAsUnicode
    
             
    pIndex  = 0     
    
    anOutput.write( u"""    
        <!-- #################################################################
        SECTION: Editor DETAILS for selected TRATraduccion
        ################################################################# -->
        <div id="cid_TRAEditorDetalle" class="TRAstyle_Display">
    
            <table cellspacing="0" cellpadding="0" frame="void" id="editor_TRATraduccion" >
                <tbody>
                \n"""
    )
          
    
            
            
        

    anOutput.write( u"""
        <!-- #####
        ## Fields: display TRATraduccion nombresModulos and cadena id 
        ##########-->  
            <tr class="TRAstyle_NoDisplay" id="cid_TRAEditorDetalle_nombresModulos_row">
                <td align="left" valign="baseline" >                
                    <font size="1" ><strong>%(gvSIGi18n_Modulos_title)s</strong></font>
                    &emsp;
                </td>
                <td  align="left" valign="baseline"  colspan="2">                
                    <font size="1" ><span id="cid_TRAEditorDetalle_nombresModulos" ></span></font>
                </td>
            </tr>
            <tr class="TRAstyle_NoDisplay" id="cid_TRAEditorDetalle_idCadena_row">            
                <td align="left" valign="baseline" >       
                    <font size="1" ><strong>%(gvSIGi18n_TRACadena_attr_id_label)s</strong></font>
                    &emsp;
                </td>
                <td align="left" valign="baseline" colspan="2">       
                    <font size="1" ><span id="cid_TRAEditorDetalle_idCadena" ></span></font>
                </td>
            </tr>
        \n""" % { 
        'gvSIGi18n_Modulos_title':              mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_Modulos_title', 'Modules-'), 
        'gvSIGi18n_TRACadena_attr_id_label':    aTranslationsCache[ 'gvSIGi18n_TRACadena_attr_id_label'], 
        'pClassFila': cClasesFilas [pIndex %2],
    })
    
    pIndex  += 1
        

                

                
                
                                        
    anOutput.write( u"""

        <!-- ########################
        SubSection: Auditing information state change dates and member ids
        #############################-->  
        
        <font size="1" >
        \n""" 
    )
                
    
               
    anOutput.write( u"""  
        <tr class="TRAstyle_NoDisplay" id="cid_TRAEditorDetalle_Definitiva" >
            <td align="left" valign="baseline"  >                
                <font size="1"><strong>%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Definitiva)s</strong></font>
            </td>
            <td align="left" valign="baseline"  >                
                <font size="1">
                    %(gvSIGi18n_fecha_el)s
                    &nbsp;
                    <span id="cid_TRAEditorDetalle_Definitiva_Fecha"      ></span>
                    &ensp;
                </font>
            </td>
            <td align="left" valign="baseline"  >  
                <font size="1">
                    %(gvSIGi18n_usuario_por)s
                    &nbsp;
                    <span id="cid_TRAEditorDetalle_Definitiva_Usuario"    ></span>
                </font>
            </td>
        </tr>
        \n""" % { 
        'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Definitiva': aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Definitiva'],
        'gvSIGi18n_fecha_el':                                              aTranslationsCache[ 'gvSIGi18n_fecha_el'],
        'gvSIGi18n_usuario_por':                                           aTranslationsCache[ 'gvSIGi18n_usuario_por'],
    })

                        
    pIndex = pIndex + 1              
      
    
    
    
    anOutput.write( u"""                
        <tr class="TRAstyle_NoDisplay" id="cid_TRAEditorDetalle_Revisada" >
            <td align="left" valign="baseline"  >                
                <font size="1"><strong>%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Revisada)s</strong>
            </td>
            <td align="left" valign="baseline"  >                
                <font size="1">
                    %(gvSIGi18n_fecha_el)s
                    &nbsp;
                    <span id="cid_TRAEditorDetalle_Revisada_Fecha"      ></span>
                    &ensp;
                </font>
            </td>
            <td align="left" valign="baseline"  >  
                <font size="1">
                    %(gvSIGi18n_usuario_por)s
                    &nbsp;
                    <span id="cid_TRAEditorDetalle_Revisada_Usuario"    ></span>
                </font>
            </td>
        </tr>
        \n""" % { 
        'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Revisada': aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Revisada'],
        'gvSIGi18n_fecha_el':                                            aTranslationsCache[ 'gvSIGi18n_fecha_el'],
        'gvSIGi18n_usuario_por':                                         aTranslationsCache[ 'gvSIGi18n_usuario_por'],
    })
    pIndex = pIndex + 1    
    
        
        
        
                                    
    anOutput.write( u"""                
        <tr class="TRAstyle_NoDisplay" id="cid_TRAEditorDetalle_Traducida" >
            <td align="left" valign="baseline"  >                
                <font size="1"><strong>%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Traducida)s</strong>
            </td>
            <td align="left" valign="baseline"  >                
                <font size="1">
                    %(gvSIGi18n_fecha_el)s
                    &nbsp;
                    <span id="cid_TRAEditorDetalle_Traducida_Fecha"      ></span>
                    &ensp;
                </font>
            </td>
            <td align="left" valign="baseline"  >  
                <font size="1">
                    %(gvSIGi18n_usuario_por)s
                    &nbsp;
                    <span id="cid_TRAEditorDetalle_Traducida_Usuario"    ></span>
                </font>
            </td>
        </tr>
        \n""" % { 
        'gvSIGi18n_fecha_el':                                          aTranslationsCache[ 'gvSIGi18n_fecha_el'],
        'gvSIGi18n_usuario_por':                                       aTranslationsCache[ 'gvSIGi18n_usuario_por'],
        'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Traducida': aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Traducida'],
    })

    pIndex = pIndex + 1              

        
    anOutput.write( u"""                
        <tr class="TRAstyle_NoDisplay" id="cid_TRAEditorDetalle_Creada" >
            <td align="left" valign="baseline"  >                
                <font size="1"><strong>%(gvSIGi18n_TRATraduccion_Creada)s</strong>
            </td>
            <td align="left" valign="baseline"  >                
                <font size="1">
                    %(gvSIGi18n_fecha_el)s
                    &nbsp;
                    <span id="cid_TRAEditorDetalle_Creada_Fecha"      ></span>
                    &ensp;
                </font>
            </td>
            <td align="left" valign="baseline"  >  
                <font size="1">
                    %(gvSIGi18n_usuario_por)s
                    &nbsp;
                    <span id="cid_TRAEditorDetalle_Creada_Usuario"    ></span>
                </font>
            </td>
        </tr>
         \n""" % { 
        'gvSIGi18n_fecha_el':               aTranslationsCache[ 'gvSIGi18n_fecha_el'],
        'gvSIGi18n_usuario_por':            aTranslationsCache[ 'gvSIGi18n_usuario_por'],
        'gvSIGi18n_TRATraduccion_Creada':   aTranslationsCache[ 'gvSIGi18n_TRATraduccion_Creada'],
    })

    anOutput.write( u"""                
            </td>
        </tr>
        \n"""
    )
        
    
    #anOutput.write( u"""
        #<!-- #####
        # ## Field: TRATraduccion comentario display and edit
        # ##########-->  
        #<tr>                        
        #\n"""
    #)

    #pReadOnly = ''
    #if pCanComment:
        #pReadOnly = ''
        #anOutput.write( u"""
            #<tr class="%(pClassFila)s">                        
                #<td   align="right" valign="top" >                
                    #<input name="form_submit" value="%(gvSIGi18n_comentar_action_label)s" type="submit" style="color: Red; font-size: 8pt; font-style: italic" />                                                
                #</td>
                #\n""" % { 
            #'gvSIGi18n_comentar_action_label':      aTranslationsCache[ 'gvSIGi18n_comentar_action_label'], 
            #'pClassFila': cClasesFilas [pIndex %2],
        #})
            
    #else:
        #pReadOnly = 'readonly="readonly"'
        #anOutput.write( u"""
            #<tr class="%(pClassFila)s">                        
                #<td  align="right" valign="top" >                
                    #<font size="1" ><strong>%(gvSIGi18n_comentar_action_label)s</strong><font/>                                                
                #</td>
                #\n""" % { 
            #'gvSIGi18n_comentar_action_label':      aTranslationsCache[ 'gvSIGi18n_comentar_action_label'], 
            #'pClassFila': cClasesFilas [pIndex %2],
        #})
            
            
    #anOutput.write( u"""
        #<td colspan="3" align="left" valign="top" >                
            #<textarea name="Comentario" %(pReadOnly)s style="font-size: 10pt;" cols="68" rows="%(rows)d" id="Comentario" >""" % { 
        #'gvSIGi18n_comentar_action_label':      aTranslationsCache[ 'gvSIGi18n_comentar_action_label'], 
        #'rows':                                         min( max( 1, len( pComentarioTraduccion.splitlines())), 12), 
        #'pReadOnly' : pReadOnly, 
    #}) 
        
    #for unaLinea in pComentarioTraduccion.splitlines():
        #anOutput.write( u"""%(unaLinea)s\n""" % { 'unaLinea': mfAsUnicode( unaLinea),} )
                
    #anOutput.write( u"""</textarea>
            #</td>
        #</tr>
        #\n""" 
    #)        
                
                
    #pIndex  += 1
   
    
        
    
    anOutput.write( u"""                
                </tbody>
            </table>
        </div>
        \n"""
    )
    
    return None          
  








    
def pRenderCollapsibleHistory( 
    anOutput, 
    unContextualObject, 
    pCodigoIdiomaCursor, 
    pRegistrosHistoria, 
    aTranslationsCache):
    """Render as collapsible the selected translation history section of the translations browser.
    
    """
    
    mfTranslateI18N     = unContextualObject.fTranslateI18N
    mfAsUnicode         = unContextualObject.fAsUnicode
    
            
    pRenderCollapsible_Lambda(  anOutput,
        mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_seccionHistory_title', 'History-'),
        u'elid_History_collapsible_dl', 
        lambda : pRenderHistory( 
            anOutput, 
            unContextualObject, 
            pCodigoIdiomaCursor,
            pRegistrosHistoria, 
            aTranslationsCache
        ),
        False,
    )
    
    return None        







def pRenderHistory( 
    anOutput, 
    unContextualObject, 
    pCodigoIdiomaCursor,
    pRegistrosHistoria, 
    aTranslationsCache):
    """Render the selected translation history section of the translations browser.
    
    """
    
    
    mfTranslateI18N     = unContextualObject.fTranslateI18N
    mfAsUnicode         = unContextualObject.fAsUnicode
    

    pIndex =0

    anOutput.write( u"""  
    
        <!-- #################################################################
        SECTION: History of changes for selected TRATraduccion
        ################################################################# -->
                                      
        <table class="listing nosort" id="sct_SelectedTRATraduccion_History" >
            <thead>
                <tr>                        
                    <th  align="center" valign="center" >   
                        <!-- ACV 20090315 show/hide informe only from sections control                    
                        <input name="form_submit" style="font-size: 8pt;"  value="%(gvSIGi18n_ocultar_action_label)s" type="submit" onclick="document.getElementById( 'theMostrarHistoria').value='0';  return true;" />
                        <br/>
                        <font size="1">%(gvSIGi18n_TRATraduccion_attr_historia_label)s</font>
                        -->
                    </th>
                    <th  align="left" valign="baseline" >   
                        <font size="1" >%(gvSIGi18n_historiafechaaccion_label)s</font>
                    </th>
                    <th  align="left" valign="baseline" >   
                        <font size="1" >%(gvSIGi18n_historiausuarioactor_label)s</font>
                    </th>
                    <th  align="left" valign="baseline" >   
                        <font size="1" >%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label)s</font>
                    </th>
                    <th  align="left" valign="baseline" >   
                        <font size="1" >%(gvSIGi18n_TRATraduccion_attr_fechaTraduccionTextual_label)s</font>
                    </th>
                    <th  align="left" valign="baseline" >   
                        <font size="1" >%(gvSIGi18n_TRATraduccion_attr_usuarioTraductor_label)s</font>
                    </th>
                    <th  align="left" valign="baseline" >   
                        <font size="1" >%(gvSIGi18n_TRATraduccion_attr_fechaRevisionTextual_label)s</font>
                    </th>
                    <th  align="left" valign="baseline" >   
                        <font size="1" >%(gvSIGi18n_TRATraduccion_attr_usuarioRevisor_label)s</font>
                    </th>
                    <th  align="left" valign="baseline" >   
                        <font size="1" >%(gvSIGi18n_TRATraduccion_attr_fechaDefinitivoTextual_label)s</font>
                    </th>
                    <th  align="left" valign="baseline" >   
                        <font size="1" >%(gvSIGi18n_TRATraduccion_attr_usuarioCoordinador_label)s</font>
                    </th>
                </tr>
            </thead>      
            <tbody>                    
            \n""" % {                                  
        'gvSIGi18n_ocultar_action_label':                           aTranslationsCache[ 'gvSIGi18n_ocultar_action_label'],
        'gvSIGi18n_TRATraduccion_attr_historia_label':              aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_historia_label'],
        'gvSIGi18n_historiafechaaccion_label':                      aTranslationsCache[ 'gvSIGi18n_historiafechaaccion_label'],
        'gvSIGi18n_historiausuarioactor_label':                     aTranslationsCache[ 'gvSIGi18n_historiausuarioactor_label'],
        'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label':      aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label'], 
        'gvSIGi18n_TRATraduccion_attr_fechaCreacionTextual_label':  aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_fechaCreacionTextual_label'],
        'gvSIGi18n_TRATraduccion_attr_usuarioCreador_label':        aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_usuarioCreador_label'],
        'gvSIGi18n_TRATraduccion_attr_fechaTraduccionTextual_label':aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_fechaTraduccionTextual_label'],
        'gvSIGi18n_TRATraduccion_attr_usuarioTraductor_label':      aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_usuarioTraductor_label'],
        'gvSIGi18n_TRATraduccion_attr_fechaRevisionTextual_label':  aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_fechaRevisionTextual_label'],
        'gvSIGi18n_TRATraduccion_attr_usuarioRevisor_label':        aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_usuarioRevisor_label'],
        'gvSIGi18n_TRATraduccion_attr_fechaDefinitivoTextual_label':aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_fechaDefinitivoTextual_label'], 
        'gvSIGi18n_TRATraduccion_attr_usuarioCoordinador_label':    aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_usuarioCoordinador_label'],
    })


    for pRegistroHistoria in pRegistrosHistoria:
        anOutput.write( u"""                     
            <tr class="%(pClassFila)s" >
                <td  align="left" valign="baseline" >   
                    <font size="1" ><strong>%(accion)s</strong></font>
                </td>
                <td  align="left" valign="baseline" >   
                    <font size="1" >%(fechaAccion)s</font>
                </td>
                <td  align="left" valign="baseline" >   
                    <font size="1" >%(usuarioActor)s</font>
                </td>
                \n""" % { 
            'pClassFila':       cClasesFilas [ pIndex %2], 
            'accion':           pRegistroHistoria[ 'accion'], 
            'fechaAccion':      pRegistroHistoria[ 'fechaAccion'], 
            'usuarioActor':     pRegistroHistoria[ 'usuarioActor'], 
        })
                                                
                                                
        if not (pRegistroHistoria[ 'accion'] == 'Comentar'):
                            
            anOutput.write( u"""                                             
                <td  align="center" valign="baseline" bgcolor="%(pBGColor)s">   
                    <font color="%(pFGColor)s" size="1"><strong>%(estadoTraduccion)s</strong></font>
                </td>
                \n""" % { 
                'pBGColor':             cBGColorsDict.get( pRegistroHistoria[ 'estadoTraduccion'] , cFGColorsDict[ cEstadoTraduccionPendiente]), 
                'pFGColor':             cFGColorsDict.get( pRegistroHistoria[ 'estadoTraduccion'] , cFGColorsDict[ cEstadoTraduccionPendiente]),
                'estadoTraduccion':     aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_%s' % pRegistroHistoria[ 'estadoTraduccion']] , 
            })
        else:
            anOutput.write( u"""                                                                                                                        
                <td  />
                \n""" )

            anOutput.write( u"""                                                                                                                                                      
                <td  align="left" valign="baseline" >   
                    <font size="1">%(fechaTraduccion)s</font>
                </td>
                <td  align="left" valign="baseline" >   
                    <font size="1">%(usuarioTraductor)s</font>
                </td>
                <td  align="left" valign="baseline" >   
                    <font size="1">%(fechaRevision)s</font>
                </td>
                <td  align="left" valign="baseline" >   
                    <font size="1">%(usuarioRevisor)s</font>
                </td>
                <td  align="left" valign="baseline" >   
                    <font size="1">%(fechaDefinitivo)s</font>
                </td>
            </tr>           
            \n""" % { 
            'fechaTraduccion':      pRegistroHistoria[ 'fechaCreacion'], 
            'usuarioTraductor':     pRegistroHistoria[ 'usuarioCreador'], 
            'fechaTraduccion':      pRegistroHistoria[ 'fechaTraduccion'], 
            'usuarioTraductor':     pRegistroHistoria[ 'usuarioTraductor'], 
            'fechaRevision':        pRegistroHistoria[ 'fechaRevision'], 
            'usuarioRevisor':       pRegistroHistoria[ 'usuarioRevisor'], 
            'fechaDefinitivo':      pRegistroHistoria[ 'fechaDefinitivo'], 
            'usuarioCoordinador':   pRegistroHistoria[ 'usuarioCoordinador'], 
        } )

                                            
        if not (pRegistroHistoria[ 'accion'] == 'Comentar') and len( pRegistroHistoria[ 'cadenaTraducida'].strip()) > 0:
            anOutput.write( u"""                                                                                                                                                      
                <tr class="%(pClassFila)s" >
                    <td  align="right" valign="baseline" >   
                        <font size="1" >%(gvSIGi18n_TRATraduccion_attr_historiaCadenaTraducida_label)s</font>
                    </td>
                    <td  align="left" valign="baseline" colspan="10" >   
                        <font size="%(font-size)d" >%(cadenaTraducida)s</font>
                    </td>
                </tr>
                \n""" % { 
                'pClassFila':                                      cClasesFilas [ pIndex %2], 
                'font-size':                                       TRASizesIdioma( pCodigoIdiomaCursor)[ 'display_font_size'],
                'cadenaTraducida':                                 mfAsUnicode( pRegistroHistoria[ 'cadenaTraducida'].strip()), 
                'gvSIGi18n_TRATraduccion_attr_historiaCadenaTraducida_label':  aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_cadenaTraducida_label'], 
            })
        else:                                        
            anOutput.write( u"""                                                                                                                                                      
                <tr class="%(pClassFila)s" >
                    <td  align="right" valign="baseline" >   
                        <font size="1" >%(gvSIGi18n_historiacomentario_label)s</font>
                    </td>
                    <td  align="left" valign="baseline" colspan="10" >   
                        <font size="1" >%(comentario)s</font>
                    </td>
                </tr>
                \n""" % { 
                'pClassFila':                                  cClasesFilas [ pIndex %2], 
                'comentario':                                  ''.join( pRegistroHistoria[ 'comentario'].splitlines()), 
                'gvSIGi18n_historiacomentario_label':  aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_comentario_label'], 
            }) 
                                        
        pIndex = pIndex +1
                     
        
        
    anOutput.write( u"""                                                                                                                                                      
            </tbody>
        </table>                                          
        \n""" 
    )     
                
    return None
    






    
        
        
        
    

def pRenderEditorTextAreaAndButtons( 
    anOutput, 
    unContextualObject,         
    unasSizesIdioma,
    unosAllowedTargetStates,
    pAllowInvalidateStringTranslations,
    unEstadoTraduccion,
    aTranslationsCache):
    
    mfTranslateI18N     = unContextualObject.fTranslateI18N
    mfAsUnicode         = unContextualObject.fAsUnicode


    anOutput.write( u"""
 
        <!-- #####
        ## SECTION: Editor area and buttons
        ##########-->  
    
        <div id="cid_TRAEditorAreaYBotones" class="TRAstyle_NoDisplay">
            \n"""
    )
    
    
    unNumeroLineas = 2
    unNumeroColumnas = unasSizesIdioma[ 'edit_chars_perline']
    

    unaLenCadena = 72 / unasSizesIdioma[ 'edit_chars_divider']
    if unaLenCadena > unasSizesIdioma[ 'edit_chars_perline']:
        unNumeroLineas     = int( unaLenCadena / unasSizesIdioma[ 'edit_chars_perline'])
        if unaLenCadena % unasSizesIdioma[ 'edit_chars_perline']:
            unNumeroLineas += 1
       
                
    anOutput.write( u"""
        <!-- #####
        ## Field: TRATraduccion cadenaTraducida edit
        ##########-->  

        <textarea 
            tabindex=1  
            class="%(class-Display)s"
            onkeypress="return fTRAEvtHlr_Editor_TextArea_OnKeyPress( event);"
            onblur="fTRAEvtHlr_Editor_TextArea_OnBlur();"
            id="theCadenaTraducida" 
            name="theCadenaTraducida" 
            style="font-size: %(font-size)dpt;" 
            cols="%(area-columns)d" 
            rows="%(area-rows)d" ></textarea>
        \n""" % { 
        'font-size':                                    unasSizesIdioma[ 'edit_font_size'],
        'area-columns':                                 unNumeroColumnas,    
        'area-rows':                                    unNumeroLineas,  
        'class-Display':                                ((( unEstadoTraduccion in [ cEstadoTraduccionPendiente, cEstadoTraduccionTraducida,]) and ( len( set( [ cEstadoTraduccionPendiente, cEstadoTraduccionTraducida,]).intersection( unosAllowedTargetStates)) > 0)) and 'TRAstyle_Display') or 'TRAstyle_NoDisplay',
    })

    
    
    anOutput.write( u"""
        <!-- #####
        ## Hidden Field: the new translation status requested 
        #  Alternative to using a button that submits form_submit with the new state as value)
        ##########-->  
        
        <input type="hidden" id="theNuevoEstadoTraduccion" name="theNuevoEstadoTraduccion" value="" />

        \n""" 
    )
    
    anOutput.write( u"""
        <!-- #####
        ## Hidden Field: the relative new position first previous next or last 
        #  Alternative to using a button that submits form_submit with the value of the desired movement)
        ##########-->  
        
        <input type="hidden" id="theGoTo" name="theGoTo" value="" />

        \n""" 
    )
    
    
    
    unButtonsColumnsWidthString = ( pAllowInvalidateStringTranslations and '33%') or '50%'

    anOutput.write( u"""    

        <!-- #################################################################
        SECTION: State change buttons
        ################################################################# -->
        
        <table width="100%" frame="void" cellpadding="4" cellspacing="4">
            <tbody>
                <tr>
        \n"""
     )

    anOutput.write( u"""                                                                                                                                               
        <td align="left" valign"=center" width="%(unButtonsColumnsWidthString)s" >
            <img class="%(class-Display)s TRAstyle_Clickable"
                id="TRAStatusChangeButton_Traducir_Icon" 
                onmousedown="fTRAEvtHlr_Editor_Button_Traducir_OnMouseUp( )"
                onkeypress="fTRAEvtHlr_Editor_Button_Traducir_OnKeyPress( event)"
                alt="%(action_name)s" 
                title="%(action_name)s" 
                src="%(portal_url)s/%(estado-icon-Traducida)s" />
            <input  
                onmousedown="fTRAEvtHlr_Editor_Button_Traducir_OnMouseUp( )"
                onkeypress="fTRAEvtHlr_Editor_Button_Traducir_OnKeyPress( event)"
                tabindex=2
                id="TRAStatusChangeButton_Traducir" 
                class="%(class-Display)s TRAstyle_Clickable"                
                name="TRAStatusChangeButton_Traducir" 
                value="%(action_name)s" 
                type="button" 
                style="color: red; font-size: 9pt; font-style: italic; font-weight: 700" />
        </td>        
        \n""" % { 
        'unButtonsColumnsWidthString': unButtonsColumnsWidthString,
        'accion-Traducir':        cAccion_Traducir,
        'action_name':            aTranslationsCache[ 'gvSIGi18n_TranslationAction_Grabar'], 
        'estado-icon-Traducida':  cIconsDict.get( cEstadoTraduccionTraducida, 'tra_traducida.gif'),
        'portal_url':             unContextualObject.absolute_url(), 
        'class-Display':          ((( unEstadoTraduccion in [ cEstadoTraduccionPendiente, cEstadoTraduccionTraducida,]) and ( len( set( [ cEstadoTraduccionPendiente, cEstadoTraduccionTraducida,]).intersection( unosAllowedTargetStates)) > 0)) and 'TRAstyle_Display') or 'TRAstyle_NoDisplay',
    })
   
      
 

    
    # ACV 20090926 Added in support of UC22 Use Case Invalidate String translations to all languages    
    if pAllowInvalidateStringTranslations:
        anOutput.write( u"""  
            <td align="center" valign"=center" width="%(unButtonsColumnsWidthString)s" >
                [
                <img class="TRAstyle_Display TRAstyle_Clickable"
                    id="TRAStatusChangeButton_InvalidarTraduccionesCadena_Icon1" 
                    onmousedown="fTRAEvtHlr_Editor_Button_InvalidarTraduccionesCadena_OnMouseUp( )"
                    onkeypress="fTRAEvtHlr_Editor_Button_InvalidarTraduccionesCadena_OnKeyPress( event)"
                    alt="%(gvSIGi18n_TranslationAction_InvalidarTraduccionesCadena_help)s" 
                    title="%(gvSIGi18n_TranslationAction_InvalidarTraduccionesCadena_help)s" 
                    src="%(portal_url)s/%(estado-icon-Pendiente)s" />
                *
                <img class="TRAstyle_Display TRAstyle_Clickable"
                    id="TRAStatusChangeButton_InvalidarTraduccionesCadena_Icon2" 
                    onmousedown="fTRAEvtHlr_Editor_Button_InvalidarTraduccionesCadena_OnMouseUp( )"
                    onkeypress="fTRAEvtHlr_Editor_Button_InvalidarTraduccionesCadena_OnKeyPress( event)"
                    alt="%(gvSIGi18n_TranslationAction_InvalidarTraduccionesCadena_help)s" 
                    title="%(gvSIGi18n_TranslationAction_InvalidarTraduccionesCadena_help)s" 
                    src="%(portal_url)s/flag-plone.gif" />
                ]
                <input  
                    onmousedown="fTRAEvtHlr_Editor_Button_InvalidarTraduccionesCadena_OnMouseUp( )"
                    onkeypress="fTRAEvtHlr_Editor_Button_InvalidarTraduccionesCadena_OnKeyPress( event)"
                    tabindex=5
                    id="TRAStatusChangeButton_InvalidarTraduccionesCadena" 
                    class="TRAstyle_Display TRAstyle_Clickable" 
                    name="TRAStatusChangeButton_InvalidarTraduccionesCadena" 
                    value="%(action_name)s" 
                    type="button" 
                    style="color: Red; font-size: 9pt; font-style: italic; font-weight: 700" />
            </td>        
            \n""" % { 
            'unButtonsColumnsWidthString': unButtonsColumnsWidthString,
            'action_name':                                                   aTranslationsCache[ 'gvSIGi18n_TranslationAction_InvalidarTraduccionesCadena_label'], 
            'estado-icon-Pendiente':                                         cIconsDict.get( cEstadoTraduccionPendiente, 'tra_pendiente.gif'),
            'gvSIGi18n_TranslationAction_InvalidarTraduccionesCadena_help':  aTranslationsCache[ 'gvSIGi18n_TranslationAction_InvalidarTraduccionesCadena_help'],
            'portal_url':                                                    unContextualObject.absolute_url(), 
            'class-Display':                                                 'TRAstyle_Display',
        })
            

        
        
    anOutput.write( u"""  
        <td align="right" valign"=center" width="%(unButtonsColumnsWidthString)s" >
            <img class="TRAstyle_Display TRAstyle_Clickable"
                id="TRAStatusChangeButton_Pendiente_Icon" 
                onmousedown="fTRAEvtHlr_Editor_Button_Pendiente_OnMouseUp( )"
                onkeypress="fTRAEvtHlr_Editor_Button_Pendiente_OnKeyPress( event)"
                alt="%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Pendiente)s" 
                title="%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Pendiente)s" 
                src="%(portal_url)s/%(estado-icon-Pendiente)s" />
            <input  
                onmousedown="fTRAEvtHlr_Editor_Button_Pendiente_OnMouseUp( )"
                onkeypress="fTRAEvtHlr_Editor_Button_Pendiente_OnKeyPress( event)"
                tabindex=5
                id="TRAStatusChangeButton_Pendiente" 
                class="TRAstyle_Display TRAstyle_Clickable" 
                name="TRAStatusChangeButton_Pendiente" 
                value="%(action_name)s" 
                type="button" 
                style="color: Red; font-size: 9pt; font-style: italic; font-weight: 700" />
        </td>        
        \n""" % { 
        'unButtonsColumnsWidthString': unButtonsColumnsWidthString,                  
        'action_name':                                                              aTranslationsCache[ 'gvSIGi18n_TranslationAction_Borrar'], 
        'estado-icon-Pendiente':                                                    cIconsDict.get( cEstadoTraduccionPendiente, 'tra_pendiente.gif'),
        'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Pendiente':   aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Pendiente'],
        'portal_url':                                                              unContextualObject.absolute_url(), 
        'class-Display':          ((( unEstadoTraduccion in [ cEstadoTraduccionPendiente, cEstadoTraduccionTraducida,]) and ( len( set( [ cEstadoTraduccionPendiente, cEstadoTraduccionTraducida,]).intersection( unosAllowedTargetStates)) > 0)) and 'TRAstyle_Display') or 'TRAstyle_NoDisplay',
    })
        


    
    
    anOutput.write( u""" 
                </tr>
            </body>
        </table>
        \n"""
    )
       
    anOutput.write( u""" 
        </div>
        \n"""
    )
    
    return None            
    
         
        
    




    
def pRenderCollapsibleList( 
    anOutput, 
    unContextualObject, 
    pBrowseResult,
    pCodigoIdiomaCursor, 
    pIdiomasReferencia, 
    pDatosTraducciones, 
    pDictsTraduccionesIdiomasReferencia, 
    pLanguagesNamesAndFlags, 
    theWritePermission,
    pAllowedStateTransitions,
    pAllTargetStatusChanges,
    pAllowInvalidateStringTranslations,
    unSimboloCadenaATraducirHolder,
    pMostrarHistoria,
    pHideStateTransitionColumns,
    pBatchStatusChanges,
    aTranslationsCache,
    unRolesCache):
    """Render as collapsible the matching translations list section of the translations browser.
    
    """
    
    mfTranslateI18N     = unContextualObject.fTranslateI18N
    mfAsUnicode         = unContextualObject.fAsUnicode
    
    unCursorPositionString =  u'%s %d %s %d %s %d' % ( 
        aTranslationsCache[ 'gvSIGi18n_fromToIn_from_label'],
        pBrowseResult.get( 'from_translation_index', 0),
        aTranslationsCache[ 'gvSIGi18n_fromToIn_to_label'],
        pBrowseResult.get( 'to_translation_index', 0),
        aTranslationsCache[ 'gvSIGi18n_fromToIn_in_label'],
        pBrowseResult.get( 'total_translations', 0),
    )        
    
    pRenderCollapsible_Lambda(  anOutput,
        u'%s  %s' % ( aTranslationsCache[ 'gvSIGi18n_seccionList_title'], unCursorPositionString),
        u'elid_List_collapsible_dl', 
        lambda : pRenderList( 
            anOutput, 
            unContextualObject, 
            pCodigoIdiomaCursor, 
            pIdiomasReferencia, 
            pDatosTraducciones, 
            pDictsTraduccionesIdiomasReferencia, 
            pLanguagesNamesAndFlags, 
            theWritePermission,
            pAllowedStateTransitions,
            pAllTargetStatusChanges,
            pAllowInvalidateStringTranslations,
            unSimboloCadenaATraducirHolder,
            pMostrarHistoria,
            pHideStateTransitionColumns,
            pBatchStatusChanges,
            unCursorPositionString,
            aTranslationsCache,
            unRolesCache,
        ),
        False,
    )
    
    return None        


            
            
            

def pRenderList( 
    anOutput, 
    unContextualObject, 
    pCodigoIdiomaCursor, 
    pIdiomasReferencia, 
    pDatosTraducciones, 
    pDictsTraduccionesIdiomasReferencia, 
    pLanguagesNamesAndFlags, 
    theWritePermission,
    pAllowedStateTransitions,
    pAllTargetStatusChanges,
    pAllowInvalidateStringTranslations,
    unSimboloCadenaATraducirHolder,
    pMostrarHistoria,
    pHideStateTransitionColumns,
    pBatchStatusChanges,
    unCursorPositionString,
    aTranslationsCache, 
    unRolesCache):
    """Render the matching translations list section of the translations browser in two columns.
    
    """

    mfTranslateI18N     = unContextualObject.fTranslateI18N
    mfAsUnicode         = unContextualObject.fAsUnicode
    


    aDictRenderValues = aTranslationsCache.copy()
    aDictRenderValues.update( {
        'portal_url':  unContextualObject.absolute_url(), 
        'gvSIGi18n_ColumnaSimboloColapsable_Action_Hide_help':              aTranslationsCache[ 'gvSIGi18n_ColumnaSimboloColapsable_Action_Hide_help'],
        'gvSIGi18n_ColumnaSimboloColapsable_Action_Show_help':              aTranslationsCache[ 'gvSIGi18n_ColumnaSimboloColapsable_Action_Show_help'],
    })
    anOutput.write( u"""  
        <!-- #################################################################
        SECTION: List of matching TRATraduccion
        ################################################################# -->
        
        <table width="100%%" id="matching_TRATraducion_list" cellspacing="2" cellpadding="2" frame="void"  summary="traducciones" >
            <thead>
                <tr>
                    <th width="25%%"  valign="bottom" align="left" class="TRAstyle_Display TRAstyle_Clickable" 
                        id="cid_ColumnaSimbolos_0" 
                        onclick="pTRAHideSymbolColumn(); return true;" >
                        <font size="1">%(gvSIGi18n_TRATraduccion_attr_simbolo_label)s</font>
                        <br/>
                        <span class="formHelp">
                            <font size="1" style="font-weight=200">
                                %(gvSIGi18n_ColumnaSimboloColapsable_Action_Hide_help)s
                            </font>
                        </span>
                    </th>
                    <th width="1%%" valign="bottom"  colspan="3" align="center" class="TRAstyle_Clickable" onclick="pTRAShowSymbolColumn(); return true;" >
                        <font size="1">%(gvSIGi18n_Estado_label)s&ensp;%(gvSIGi18n_idioma_msgid)s</font>
                    </th>
                    <th width="72%%" valign="bottom"  align="left"  class="TRAstyle_Clickable" onclick="pTRAShowSymbolColumn(); return true;" >
                        <font size="1">%(gvSIGi18n_TRATraduccion_attr_cadenaTraducida_label)s</font>
                        <br>
                        <span class="TRAstyle_NoDisplay"  id="cid_ColumnaSimbolos_show_help">
                            <span class="formHelp">
                                <font size="1" style="font-weight=200">
                                    %(gvSIGi18n_ColumnaSimboloColapsable_Action_Show_help)s
                                </font>
                            </span>
                        </span>
                    </th>
        \n""" % aDictRenderValues
    )
    
    
    someEstadosConBotonesEnColumnas = [ ]
    if cEstadoTraduccionTraducida in pAllTargetStatusChanges:
        someEstadosConBotonesEnColumnas.append( cEstadoTraduccionTraducida)
    if cEstadoTraduccionRevisada in pAllTargetStatusChanges:
        someEstadosConBotonesEnColumnas.append( cEstadoTraduccionRevisada)
    if cEstadoTraduccionDefinitiva in pAllTargetStatusChanges:
        someEstadosConBotonesEnColumnas.append( cEstadoTraduccionDefinitiva)
        
    
    if ( not pHideStateTransitionColumns) and ( len( someEstadosConBotonesEnColumnas) > 0):
        aStatusChangeColumnLabel = (pBatchStatusChanges and aTranslationsCache[ 'gvSIGi18n_BatchNewStatus_title']) or ( aTranslationsCache[ 'gvSIGi18n_newStatus_title'])
        
        anOutput.write( u"""  
            <th colspan="%(colspan)d" valign="bottom"  class="TRAstyle_Display" width="1%%"  align="center" >
                <font size="1"><strong>%(aStatusChangeColumnLabel)s</strong></font>
            </th>

            \n""" % {
            'colspan':                             len( someEstadosConBotonesEnColumnas),
            'aStatusChangeColumnLabel':   aStatusChangeColumnLabel,
        })
        
         
    anOutput.write( u"""  
        </tr>
        \n"""
    )

         
    if ( not pHideStateTransitionColumns) and ( len( someEstadosConBotonesEnColumnas) > 0) and pBatchStatusChanges:
        anOutput.write( u"""  
            <tr>
                <th colspan="5" />
                <th colspan="%(colspan)s" valign="bottom"  />
                    <input  
                        onmousedown="fTRAEvtHlr_BatchStatusChange_Apply_Button_OnMouseUp( )"
                        onkeypress="fTRAEvtHlr_BatchStatusChange_Apply_Button_OnKeyPress( event)"
                        id="TRABatchStatusChange_Apply_Button" 
                        class="TRAstyle_Display TRAstyle_Clickable" 
                        name="TRABatchStatusChange_Apply_Button" 
                        value="%(gvSIGi18n_Batch_ButtonLabel)s" 
                        type="button" 
                        style="color: Red; font-size: 9pt; font-style: italic; font-weight: 700" />
                </th>
            </tr>
            \n""" % {
            'colspan':   len( someEstadosConBotonesEnColumnas),
            # 'gvSIGi18n_BatchNewStatus_Apply_ButtonLabel':   aTranslationsCache[ 'gvSIGi18n_BatchNewStatus_Apply_ButtonLabel'],
            'gvSIGi18n_Batch_ButtonLabel':   aTranslationsCache[ 'gvSIGi18n_Batch_ButtonLabel'],
        })

        anOutput.write( u"""  
            <tr>
                <th colspan="5" />
            \n""" 
        )
        for unEstadoConBotonEnColumna in someEstadosConBotonesEnColumnas:
            anOutput.write( u"""  
                <th class="TRAstyle_Display" width="1%%"  align="center" >
                    <img
                        id="cid_TRAToggleAllBatchStatusChange_%(nombre_estado)s_Icon" 
                        class="TRAstyle_Clickable"    
                        onmousedown="pTRAToggleAllBatchStatusChanges( '%(nombre_estado)s'); return true;"
                        alt="%(nombre_estado)s" 
                        title="%(nombre_estado)s" 
                        src="%(portal_url)s/%(estado-icon)s" />
                    <br/>        
                    <input type="checkbox"  class="noborder"  value=""  name="cid_TRAToggleAllBatchStatusChange_%(nombre_estado)s" id="cid_TRAToggleAllBatchStatusChange_%(nombre_estado)s" 
                        onchange="pTRAToggleAllBatchStatusChanges('%(nombre_estado)s'); return true;" />
                </th>            
                 \n""" % {
                'nombre_estado':                            unEstadoConBotonEnColumna,
                'estado-icon':                              cIconsDict.get( unEstadoConBotonEnColumna, ''),
                'portal_url':                               unContextualObject.absolute_url(), 
            })
        anOutput.write( u"""  
            </tr>
            \n"""
        )
        
    anOutput.write( u"""  
        </thead>
        <tbody>
        \n"""
    )
    
    pNumTotalColumns  = 5 + ( (( not pHideStateTransitionColumns) and len( someEstadosConBotonesEnColumnas)) or 0)

    anOutput.write( u"""                                                                                                                                                                     
        <tr><td height="4" colspan="%(pNumTotalColumns)d" bgcolor="silver"></tr>
        \n""" % {
        'pNumTotalColumns': pNumTotalColumns,
    })
    
    
    unDisplayFontSize_IdiomaPrincipal = TRASizesIdioma( pCodigoIdiomaCursor)[ 'display_font_size']
    
    unosDisplayFontSizes_IdiomasReferencia = dict( [ ( unIdiomaReferencia, TRASizesIdioma( unIdiomaReferencia)[ 'display_font_size']) for unIdiomaReferencia in pIdiomasReferencia] )

    pIndex =0
    
    pSymbolCellCounter = 1
    
    unosIdiomasIdiomasReferenciaSinElPrincipal = [ unIdiomaReferencia for unIdiomaReferencia in pIdiomasReferencia if not ( unIdiomaReferencia ==  pCodigoIdiomaCursor) ]
     
    unYaRendereadoEditor = False
    
    for unosDatosTraduccion in pDatosTraducciones:
        
        unRendereadoEditorEnEstaFila = False
        
        
        pTradRow_getSimbolo             = unosDatosTraduccion[ 'getSimbolo']            or ''
        pTradRow_getIdCadena            = unosDatosTraduccion[ 'getIdCadena']           or ''
        pTradRow_getEstadoTraduccion    = unosDatosTraduccion[ 'getEstadoTraduccion']   or cEstadoTraduccionPendiente 
        pTradRow_getCadenaTraducida     = unosDatosTraduccion[ 'getCadenaTraducida']    or ''
        pTradRow_getNombresModulos      = unosDatosTraduccion[ 'getNombresModulos']     or '' 
        pTradRow_getFechaDefinitivo     = unosDatosTraduccion[ 'getFechaDefinitivoTextual']    or ''
        pTradRow_getUsuarioCoordinador  = unosDatosTraduccion[ 'getUsuarioCoordinador']     or ''
        pTradRow_getFechaRevision       = unosDatosTraduccion[ 'getFechaRevisionTextual']      or ''
        pTradRow_getUsuarioRevisor      = unosDatosTraduccion[ 'getUsuarioRevisor']     or ''
        pTradRow_getFechaTraduccion     = unosDatosTraduccion[ 'getFechaTraduccionTextual']    or ''
        pTradRow_getUsuarioTraductor    = unosDatosTraduccion[ 'getUsuarioTraductor']   or ''
        pTradRow_getFechaCreacion       = unosDatosTraduccion[ 'getFechaCreacionTextual']    or ''
        pTradRow_getUsuarioCreador      = unosDatosTraduccion[ 'getUsuarioCreador']   or ''
        
        
                    
        unosAllowedTargetStates = pAllowedStateTransitions.get( pTradRow_getEstadoTraduccion, set())
         
        
        unPuedeEntrarEnEdicion = theWritePermission and \
            (( ( pTradRow_getEstadoTraduccion in [ cEstadoTraduccionPendiente, cEstadoTraduccionTraducida, ]) and \
            ( cEstadoTraduccionTraducida in unosAllowedTargetStates)) and 1) or 0
        
        unPermiteBotones = ( len( unosAllowedTargetStates) > 0 and 1) or pAllowInvalidateStringTranslations or 0

        unEntrarEnEdicionEventHandler = ''
        # ACV 20091027 fix 
        # BUG UITR Translation details are not shown in editor, if the translations catalog is not modifiable (i.e. during an import process)
        if True or unPuedeEntrarEnEdicion or unPermiteBotones:
            unEntrarEnEdicionEventHandler = """
                onclick="fTRAEvtHlr_Row_OnClick( %(symbol_cell_counter)d); return true;"
                \n""" % { 
                'symbol_cell_counter':                                  pSymbolCellCounter,
            }
        
                 
        # ACV200904131333 fix
        # unRowSpanAttribute = ( unosIdiomasIdiomasReferenciaSinElPrincipal and ( 'rowspan="%d"' % ( len( unosIdiomasIdiomasReferenciaSinElPrincipal) + 1))) or ''
        unRowSpanAttribute = ( 'rowspan="%d"' % ( len( unosIdiomasIdiomasReferenciaSinElPrincipal) + 2)) or ''

        unSimboloCadenaUnicode          = mfAsUnicode( pTradRow_getSimbolo)   
        unSimboloCadenaCGIescaped       = unContextualObject.fCGIescape( unSimboloCadenaUnicode)   
        unSimboloCadenaForWrapLines     = unContextualObject.fCGIescape( fWrapeableLinesString( unSimboloCadenaUnicode,           cSimboloCadenaLineWrapLen))

        unaCadenaTraducidaUnicode       = mfAsUnicode( pTradRow_getCadenaTraducida)
        unaCadenaTraducidaCGIescaped    = unContextualObject.fCGIescape( unaCadenaTraducidaUnicode)
        unaCadenaTraducidaForWrapLines  = unContextualObject.fCGIescape( fWrapeableLinesString( unaCadenaTraducidaUnicode,   cCadenaTraducidaLineWrapLen))  
        
        
        unDictRenderValues = { 
            'entrar_en_edicion':                                    unEntrarEnEdicionEventHandler,
            'symbol_cell_counter':                                  pSymbolCellCounter,
            'row_span':                                             unRowSpanAttribute,
            'idCadena':                                             mfAsUnicode(  pTradRow_getIdCadena),
            'simbolo-cadena-forWrapLines':                          unSimboloCadenaForWrapLines,
            'simbolo-cadena':                                       unSimboloCadenaCGIescaped,
            'pClassCeldaSimbolo':                                   cClasesFilas [ pSymbolCellCounter %2], 
            'pClassFila':                                           cClasesFilas [ pIndex %2], 
            'estadoTraduccion':                                     pTradRow_getEstadoTraduccion,            
            'estadoTraduccion_label':                               ( pTradRow_getEstadoTraduccion and aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_%s' % pTradRow_getEstadoTraduccion]) or '?',            
            'targetStatusChanges':                                   ' '.join( unosAllowedTargetStates),  
            # ACV 20090927 Unused. Removedbefore even getting to use it
            # 'pAllowInvalidateStringTranslations':                   ( pAllowInvalidateStringTranslations and '1') or '0',
            'cadenaTraducida':                                      unaCadenaTraducidaCGIescaped,
            'cadenaTraducida-forWrapLines':                         unaCadenaTraducidaForWrapLines,
            'font-size':                                            unDisplayFontSize_IdiomaPrincipal,
            'pClassFila':                                           cClasesFilas [ pIndex %2], 
            'codigo-idioma':                                        mfAsUnicode( pCodigoIdiomaCursor), 
            'nombre-idioma':                                        mfAsUnicode( pLanguagesNamesAndFlags.get( pCodigoIdiomaCursor, {}).get( 'english', '')),        
            'portal_url':                                           unContextualObject.absolute_url(), 
            'flag-icon':                                            mfAsUnicode( pLanguagesNamesAndFlags.get( pCodigoIdiomaCursor, {}).get( 'flag', 'tra_flag-ninguna.gif')), 
            'pBGColor':                                             cBGColorsDict.get( pTradRow_getEstadoTraduccion,  cBGColorsDict[ cEstadoTraduccionPendiente]),
            'pFGColor':                                             cFGColorsDict.get( pTradRow_getEstadoTraduccion,  cBGColorsDict[ cEstadoTraduccionPendiente]),
            'estado-icon':                                          cIconsDict.get( pTradRow_getEstadoTraduccion, 'tra_pendiente.gif'), 
            'pTradRow_getNombresModulos':                           unContextualObject.fCGIescape( mfAsUnicode( pTradRow_getNombresModulos)),
            'pTradRow_getFechaDefinitivo':                          pTradRow_getFechaDefinitivo,
            'pTradRow_getUsuarioCoordinador':                       unContextualObject.fCGIescape(mfAsUnicode(pTradRow_getUsuarioCoordinador)),
            'pTradRow_getFechaRevision':                            pTradRow_getFechaRevision,
            'pTradRow_getUsuarioRevisor':                           unContextualObject.fCGIescape(mfAsUnicode(pTradRow_getUsuarioRevisor)),
            'pTradRow_getFechaTraduccion':                          pTradRow_getFechaTraduccion,
            'pTradRow_getUsuarioTraductor':                         unContextualObject.fCGIescape(mfAsUnicode(pTradRow_getUsuarioTraductor)),
            'pTradRow_getFechaCreacion':                            pTradRow_getFechaCreacion,
            'pTradRow_getUsuarioCreador':                           unContextualObject.fCGIescape(mfAsUnicode(pTradRow_getUsuarioCreador)),
        }
        
        
        anOutput.write( u"""  
            <tr class="%(pClassFila)s"  id="cid_FilaPrimeraDeSimbolo_%(symbol_cell_counter)d">
                <td  class="TRAstyle_Display TRAstyle_Clickable" valign="top" %(row_span)s  
                    %(entrar_en_edicion)s 
                    id="cid_ColumnaSimbolos_%(symbol_cell_counter)d" >
                    <font size="1" class="TRAstyle_Display"  id="cid_ColumnaSimbolos_%(symbol_cell_counter)d_SymbolDisplay" >%(simbolo-cadena-forWrapLines)s</font>
                    <span class="TRAstyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_simboloCadena" >%(simbolo-cadena)s</span>
                </td>
                <td align="center" valign="top" class="TRAstyle_Clickable" onclick="pTRANavegarASimboloCadenaEnFilaNumero( '%(symbol_cell_counter)d')"  >                
                    <img width="14" height="11" alt="Flag_%(nombre-idioma)s" src="%(portal_url)s/%(flag-icon)s" title="%(nombre-idioma)s" />
                </td>
                <td align="center" bgcolor="%(pBGColor)s" valign="top" class="TRAstyle_Clickable"
                    id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_estado_BGcolor"
                    %(entrar_en_edicion)s >                
                    <font color="%(pFGColor)s" size="1" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_estado_FGcolor">
                        <strong>
                            %(codigo-idioma)s
                        </strong>
                    </font>
                </td>
                <td align="center" valign="top"  class="TRAstyle_Clickable"
                    %(entrar_en_edicion)s >                
                    <img id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_estado_icon"
                        alt="Estado_%(estadoTraduccion)s" src="%(portal_url)s/%(estado-icon)s" title="%(estadoTraduccion)s" />
                </td>
                <td align="left" valign="top" bgcolor="white"
                    id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d" >
                    <span %(entrar_en_edicion)s
                        class="TRAstyle_Clickable" >
                        <font  size="%(font-size)d" >
                            <span id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_cadenaTraducidaDisplay" >%(cadenaTraducida-forWrapLines)s</span>
                        </font>
                        <span class="TRAstyle_NoDisplay" 
                            id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_cadenaTraducida_NewValue">%(cadenaTraducida)s</span>
                        <span class="TRAstyle_NoDisplay" 
                            id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_cadenaTraducida">%(cadenaTraducida)s</span>
                    </span>
                    <span class="TRAstyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_index">%(symbol_cell_counter)s</span>
                    <span class="TRAstyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_idCadena">%(idCadena)s</span>
                    <span class="TRAstyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_estadoTraduccion">%(estadoTraduccion)s</span>
                    <span class="TRAstyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_targetStatusChanges">%(targetStatusChanges)s</span>
                    <span class="TRAstyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_usuarioCreador">%(pTradRow_getUsuarioCreador)s</span>
                    <span class="TRAstyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_fechaCreacion">%(pTradRow_getFechaCreacion)s</span>
                    <span class="TRAstyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_usuarioTraductor">%(pTradRow_getUsuarioTraductor)s</span>
                    <span class="TRAstyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_fechaTraduccion">%(pTradRow_getFechaTraduccion)s</span>
                    <span class="TRAstyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_usuarioRevisor">%(pTradRow_getUsuarioRevisor)s</span>
                    <span class="TRAstyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_fechaRevision">%(pTradRow_getFechaRevision)s</span>
                    <span class="TRAstyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_usuarioCoordinador">%(pTradRow_getUsuarioCoordinador)s</span>
                    <span class="TRAstyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_fechaDefinitivo">%(pTradRow_getFechaDefinitivo)s</span>
                    <span class="TRAstyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_nombresModulos">%(pTradRow_getNombresModulos)s</span>
                    \n""" % 
            unDictRenderValues
        )
                
        if  not unYaRendereadoEditor:
            unYaRendereadoEditor = True
            unRendereadoEditorEnEstaFila = True
            if unPuedeEntrarEnEdicion or unPermiteBotones:
                unSimboloCadenaATraducirHolder[ 0] = pTradRow_getSimbolo
            
            unasSizesIdioma = TRASizesIdioma( pCodigoIdiomaCursor)
            
            pRenderEditorTextAreaAndButtons( 
                anOutput, 
                unContextualObject,         
                unasSizesIdioma,
                unosAllowedTargetStates,
                pAllowInvalidateStringTranslations,
                pTradRow_getEstadoTraduccion,
                aTranslationsCache
            )
        
            
        anOutput.write( u"""  
            </td>
            """
        )

        # ################################################################
        """Render state change action buttons on their own column.
        
        """, 
        if not pHideStateTransitionColumns:
            if ( cEstadoTraduccionTraducida in pAllTargetStatusChanges):
                anOutput.write( u"""  
                    <td  align="center"  valign="top"  id="cid_ColumnaStatusChangeButton_%(symbol_cell_counter)d_Traducida"                     
                        ><img
                            id="TRAStatusChangeButton_%(symbol_cell_counter)d_Traducida" 
                            class="%(class-Display)s TRAstyle_Clickable"    
                            onmousedown="fTRAEvtHlr_Editor_Button_StatusChange_OnMouseUp( '%(symbol_cell_counter)d', 'Traducida')"
                            alt="%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Traducida)s" 
                            title="%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Traducida)s" 
                            src="%(portal_url)s/%(estado-icon-Traducida)s" /></td>
                    \n""" % {
                    'class-Display':                                                           (  (( cEstadoTraduccionTraducida in unosAllowedTargetStates) and not ( pTradRow_getEstadoTraduccion in [ cEstadoTraduccionPendiente,  cEstadoTraduccionTraducida, ])) and 'TRAstyle_Display') or 'TRAstyle_NoDisplay',
                    'symbol_cell_counter':                                                     pSymbolCellCounter,
                    'estado-icon-Traducida':                                                    cIconsDict.get( cEstadoTraduccionTraducida, 'tra_traducida.gif'),
                    'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Traducida':   aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Traducida'],
                    'portal_url':                                                              unContextualObject.absolute_url(), 
                })
                    
            if ( cEstadoTraduccionRevisada in pAllTargetStatusChanges):
                anOutput.write( u"""  
                    <td  align="center"  valign="top"  id="cid_ColumnaStatusChangeButton_%(symbol_cell_counter)d_Revisada"                     
                        ><img
                            id="TRAStatusChangeButton_%(symbol_cell_counter)d_Revisada" 
                            class="%(class-Display)s TRAstyle_Clickable"
                            onmousedown="fTRAEvtHlr_Editor_Button_StatusChange_OnMouseUp( '%(symbol_cell_counter)d', 'Revisada')"
                            alt="%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Revisada)s" 
                            title="%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Revisada)s" 
                            src="%(portal_url)s/%(estado-icon-Revisada)s" /></td>
                    \n""" % {
                    'class-Display':                                                           (  ( cEstadoTraduccionRevisada in unosAllowedTargetStates) and 'TRAstyle_Display') or 'TRAstyle_NoDisplay',
                    'symbol_cell_counter':                                                     pSymbolCellCounter,
                    'estado-icon-Revisada':                                                    cIconsDict.get( cEstadoTraduccionRevisada, 'tra_revisada.gif'),
                    'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Revisada':   aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Revisada'],
                    'portal_url':                                                              unContextualObject.absolute_url(), 
                })
                    
            if ( cEstadoTraduccionDefinitiva in pAllTargetStatusChanges):
                anOutput.write( u"""  
                    <td  align="center"  valign="top" id="cid_ColumnaStatusChangeButton_%(symbol_cell_counter)d_Definitiva""                      
                        ><img 
                                class="%(class-Display)s TRAstyle_Clickable"
                                id="TRAStatusChangeButton_%(symbol_cell_counter)d_Definitiva" 
                                onmousedown="fTRAEvtHlr_Editor_Button_StatusChange_OnMouseUp( '%(symbol_cell_counter)d', 'Definitiva')"
                                alt="%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Definitiva)s" 
                                title="%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Definitiva)s" 
                                src="%(portal_url)s/%(estado-icon-Definitiva)s" /></td>
                    \n""" % {
                    'class-Display':                                                           (  ( cEstadoTraduccionDefinitiva in unosAllowedTargetStates) and 'TRAstyle_Display') or 'TRAstyle_NoDisplay',
                    'symbol_cell_counter':                                                       pSymbolCellCounter,
                    'estado-icon-Definitiva':                                                    cIconsDict.get( cEstadoTraduccionDefinitiva, 'tra_definitiva.gif'),
                    'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Definitiva':   aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Definitiva'],
                    'portal_url':                                                              unContextualObject.absolute_url(), 
                })
       
        anOutput.write( u"""  
            </tr>
            \n"""
        )
        
        
        anOutput.write( u"""  
            <tr class="%s">
                <td  colspan="%d"  id="cid_TRAEditorDetalleHolder_%d" >
                \n""" %  ( cClasesFilas [ 0], 4 + len( someEstadosConBotonesEnColumnas), pSymbolCellCounter)
        )
        
        if unRendereadoEditorEnEstaFila:
            pRenderEditorDetail( 
                anOutput, 
                unContextualObject,  
                pMostrarHistoria,
                aTranslationsCache        
            )
    
        anOutput.write( u""" 
                </td>
            </tr>
            \n""" 
        )
                      
        
        
        pIndex = pIndex +1                                
            
        
        
        pIndexRowIdioma = 0    
        for unIdiomaReferencia in unosIdiomasIdiomasReferenciaSinElPrincipal:
            unEstadoTraduccion                  = cEstadoTraduccionPendiente
            unaCadenaTraducidaIdiomaReferencia  = ''
            
            unasTraduccionesIdiomaReferencia   = pDictsTraduccionesIdiomasReferencia.get( unIdiomaReferencia, {})
            if unasTraduccionesIdiomaReferencia:
                unaTraduccionIdiomaReferencia      = unasTraduccionesIdiomaReferencia.get( pTradRow_getSimbolo, {})
                if unaTraduccionIdiomaReferencia:
                    unaCadenaTraducidaIdiomaReferencia = unaTraduccionIdiomaReferencia[ 'getCadenaTraducida']
                    unEstadoTraduccion                 = unaTraduccionIdiomaReferencia[ 'getEstadoTraduccion']   or cEstadoTraduccionPendiente 
            
                    
            unaCadenaTraducidaReferenciaUnicode       = mfAsUnicode( unaCadenaTraducidaIdiomaReferencia)
            unaCadenaTraducidaReferenciaCGIescaped    = unContextualObject.fCGIescape( unaCadenaTraducidaReferenciaUnicode)
            unaCadenaTraducidaReferenciaForWrapLines  = unContextualObject.fCGIescape( fWrapeableLinesString( unaCadenaTraducidaReferenciaUnicode,   cCadenaTraducidaLineWrapLen))
            
            unDictRenderIdiomaReferenciaValues = { 
                'entrar_en_edicion':                        unEntrarEnEdicionEventHandler,
                'symbol_cell_counter':                      pSymbolCellCounter,
                'cadenaTraducidaReferencia':                unaCadenaTraducidaReferenciaCGIescaped,
                'cadenaTraducidaReferencia-forWrapLines':   unaCadenaTraducidaReferenciaForWrapLines,
                'font-size':                                unosDisplayFontSizes_IdiomasReferencia[ unIdiomaReferencia],
                'class-row-idioma':                         cClasesFilas[ pIndexRowIdioma % 2],
                'codigo-idioma':                            mfAsUnicode( unIdiomaReferencia),
                'nombre-idioma':                            mfAsUnicode( pLanguagesNamesAndFlags.get( unIdiomaReferencia, {}).get( 'english', '')),        
                'portal_url':                               unContextualObject.absolute_url(), 
                'flag-icon':                                pLanguagesNamesAndFlags.get( unIdiomaReferencia, {}).get( 'flag', 'tra_flag-ninguna.gif'), 
                'pBGColor':                                 cBGColorsDict.get( unEstadoTraduccion,  cBGColorsDict[ cEstadoTraduccionPendiente]),
                'pFGColor':                                 cFGColorsDict.get( unEstadoTraduccion,  cBGColorsDict[ cEstadoTraduccionPendiente]),
                'estadoTraduccion':                         unEstadoTraduccion,            
                'estadoTraduccion_label':                   ( unEstadoTraduccion and aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_%s' % unEstadoTraduccion]) or '?',            
                'estado-icon':                              cIconsDict.get( unEstadoTraduccion, 'tra_pendiente.gif'), 
            }
            
                        
            unNavegarAIdiomaYSimboloEventHandler = """
                onclick="pTRANavegarAIdiomaPrincipalYSimboloCadenaEnFilaNumero('%(codigo-idioma)s', '%(symbol_cell_counter)d', '%(estadoTraduccion)s'); return true;"
                \n""" % unDictRenderIdiomaReferenciaValues
            
            unDictRenderIdiomaReferenciaValues[ 'navegar_a_idioma_y_simbolo'] = unNavegarAIdiomaYSimboloEventHandler
            
            anOutput.write( u"""                                                                                                                                                                     
                <tr class="%(class-row-idioma)s" >
                    <td align="center" valign="baseline" class="TRAstyle_Clickable" 
                        %(entrar_en_edicion)s >  
                        <img width="14" height="11" alt="Flag_%(codigo-idioma)s" src="%(portal_url)s/%(flag-icon)s" title="%(codigo-idioma)s" />
                    </td>
                    <td align="center"  valign="baseline" %(entrar_en_edicion)s class="TRAstyle_Clickable"  >                
                        <font  size="1" >
                            <strong>
                                %(codigo-idioma)s
                            </strong>
                        </font>
                    </td>
                    <td align="center" valign="baseline"   class="TRAstyle_Clickable"  
                        %(entrar_en_edicion)s  >                
                        <img alt="TranslationStatus_%(estadoTraduccion)s" src="%(portal_url)s/%(estado-icon)s" title="%(estadoTraduccion)s" />
                    </td>
                    <td  align="left" valign="baseline" class="TRAstyle_Clickable"  
                        %(entrar_en_edicion)s >
                        <font size="%(font-size)d">%(cadenaTraducidaReferencia-forWrapLines)s</font>
                    </td>
                \n""" % unDictRenderIdiomaReferenciaValues
            )

            if ( not pHideStateTransitionColumns) and ( len( pAllTargetStatusChanges) > 0):
                anOutput.write( u"""                                                                                                                                                                     
                    <td  colspan="%d" />  
                    """ % len( pAllTargetStatusChanges)
                )

                
            anOutput.write( u"""                                                                                                                                                                     
                </tr>
                \n"""
            )
            
            pIndexRowIdioma += 1                                
            

        anOutput.write( u"""                                                                                                                                                                     
            <tr id="cid_FilaUltimaDeSimbolo_%(symbol_cell_counter)d"><td height="4" colspan="%(pNumTotalColumns)d" bgcolor="silver"></tr>
            \n""" % { 
            'symbol_cell_counter':                      pSymbolCellCounter,
            'pNumTotalColumns':                         pNumTotalColumns,
        })

        pSymbolCellCounter += 1                                                                                                                                                                      
                                        
    anOutput.write( u"""                                                                                                                                                                     
            </tbody>
        </table>
        \n""" 
    )
    
    
    anOutput.write( u"""                                                                                                                                                                     
        <br/>
        <span><strong>%s</strong></span>
        \n""" % unCursorPositionString
    )
    
    pRenderCursorButtons( anOutput, unContextualObject, 100, aTranslationsCache,)
    anOutput.write( u"""                                                                                                                                                                     
        <br/>
        \n""" 
    )
    
    return None





def fWrapeableLinesString( theString, theMaxLength):
    if not theString:
        return ''
    
    if ( not theMaxLength):
        return theString
    
    if len( theString) <= theMaxLength:
        return theString
    
    

    unString = theString.replace('-', ' ').replace('_', ' ')
    unasLines = [ ]
    for unaLine in unString.split( ' '):
        while len( unaLine) > theMaxLength:
            unasLines.append( unaLine[ :theMaxLength])
            unaLine = unaLine[ theMaxLength:]
        if len( unaLine):
            unasLines.append( unaLine)
            
    return ' '.join( unasLines)   




   
def pRenderMessages( 
    anOutput, 
    unContextualObject,
    aTranslationsCache) :
    
    
    someDomainsStringsAndDefaultsToTranslate = [
        [ 'gvSIGi18n', [
            [ 'gvSIGi18n_Confirmar_NavegarAIdiomaPrincipalYSimbolo_msgid', 'Please confirm that you want to navigate away from this language into the selected string in a different language-',],
        ]],
    ]
    
    aMessagesDict = {}
    unContextualObject.fTranslateI18NManyIntoDict( someDomainsStringsAndDefaultsToTranslate, aMessagesDict)
    aTranslationsCache.update( aMessagesDict)
    
    anOutput.write( """
        <div id="cid_TRAMessages" class="TRAstyle_NoDisplay">
            <span id="TRAMessage_Confirmar_NavegarAIdiomaPrincipalYSimbolo">%(gvSIGi18n_Confirmar_NavegarAIdiomaPrincipalYSimbolo_msgid)s</span>
        </div>
        """ % aMessagesDict
    )
    return None





    
def pRenderCollapsibleTechnicalSections( 
    anOutput, 
    unContextualObject, 
    pRenderFormSubmit, 
    pRenderRequest, 
    pRenderFullRequest, 
    pRenderTimes, 
    pRenderProfile, 
    pRenderAsyncRequest, 
    pRenderUserInterfaceEvents,
    pFormSubmit, 
    pStartTime, 
    pEndTime, 
    pBrowseDuration, 
    unHayCambio, 
    pChangeDuration, 
    unExecutionRecord, 
    aRequestDumpString, 
    aFullRequestDumpString,
    aTranslationsCache):
    """Render as collapsible the technical sections of the translations browser.
    
    """
    
    
    mfTranslateI18N     = unContextualObject.fTranslateI18N
    mfAsUnicode         = unContextualObject.fAsUnicode
    
            
    if pRenderFormSubmit or  pRenderRequest or pRenderFullRequest or pRenderTimes or pRenderProfile or pRenderAsyncRequest or pRenderUserInterfaceEvents:
        pRenderCollapsible_Lambda(  anOutput,
            'Technical',
            u'elid_Technical_collapsible_dl', 
            lambda : pRenderTechnicalSections( 
                anOutput, 
                unContextualObject, 
                pRenderFormSubmit, 
                pRenderRequest, 
                pRenderFullRequest, 
                pRenderTimes, 
                pRenderProfile, 
                pRenderAsyncRequest, 
                pRenderUserInterfaceEvents,
                pFormSubmit, 
                pStartTime, 
                pEndTime, 
                pBrowseDuration, 
                unHayCambio, 
                pChangeDuration, 
                unExecutionRecord, 
                aRequestDumpString, 
                aFullRequestDumpString,
                aTranslationsCache,
            ),
            False,
        )
    
    return None        




           
 



def pRenderTechnicalSections( 
    anOutput, 
    unContextualObject, 
    pRenderFormSubmit, 
    pRenderRequest, 
    pRenderFullRequest, 
    pRenderTimes, 
    pRenderProfile, 
    pRenderAsyncRequest, 
    pRenderUserInterfaceEvents,
    pFormSubmit, 
    pStartTime, 
    pEndTime, 
    pBrowseDuration, 
    unHayCambio, 
    pChangeDuration, 
    unExecutionRecord, 
    aRequestDumpString, 
    aFullRequestDumpString,
    aTranslationsCache):
    """Render the technical sections of the translations browser.
    
    """    
    
    mfTranslateI18N     = unContextualObject.fTranslateI18N
    mfAsUnicode         = unContextualObject.fAsUnicode
    
    
    anOutput.write("""
        <br/>
        \n"""
    )
    
    if pRenderUserInterfaceEvents:
        pRenderCollapsible_Lambda(  anOutput,
            'User Interface Events',
            u'elid_UserInterfaceEvents_collapsible_dl', 
            lambda : pRenderTechnical_UserInterfaceEvents( 
                anOutput, 
                unContextualObject, 
                aTranslationsCache,
            ),
            False,
        )
        anOutput.write("""
            <br/><br/>
            \n"""
        )
    
    
    if pRenderFormSubmit:
        pRenderCollapsible_Lambda(  anOutput,
            'Form Submit',
            u'elid_FormSubmit_collapsible_dl', 
            lambda : pRenderTechnical_FormSubmit( 
                anOutput, 
                unContextualObject, 
                pFormSubmit,
                aTranslationsCache,
            ),
            False,
        )
        anOutput.write("""
            <br/><br/>
            \n"""
        )
    
    if pRenderTimes:
        pRenderCollapsible_Lambda(  anOutput,
            'Processing Times',
            u'elid_ProcessingTimes_collapsible_dl', 
            lambda : pRenderTechnical_Times( 
                anOutput, 
                unContextualObject, 
                pStartTime, 
                pEndTime, 
                pBrowseDuration, 
                unHayCambio, 
                pChangeDuration, 
                aTranslationsCache,
            ),
            True,
        )
        anOutput.write("""
            <br/><br/>
            \n"""
        )
 
        
    if pRenderRequest:
        pRenderCollapsible_Lambda(  anOutput,
            'Request Parameters',
            u'elid_RequestParameters_collapsible_dl', 
            lambda : pRenderTechnical_Request( 
                anOutput, 
                unContextualObject, 
                u"Business Request Parameters", 
                aRequestDumpString,
                aTranslationsCache
            ),
            True,
        )
        anOutput.write("""
            <br/><br/>
            \n"""
        )

    if pRenderFullRequest:
        pRenderCollapsible_Lambda(  anOutput,
            'Full Request',
            u'elid_FullRequest_collapsible_dl', 
            lambda : pRenderTechnical_Request( 
                anOutput, 
                unContextualObject, 
                u"Full Request", 
                aFullRequestDumpString,
                aTranslationsCache,
            ),
            True,
        )
        anOutput.write("""
            <br/><br/>
            \n"""
        )
        
        
    if pRenderAsyncRequest:
        pRenderCollapsible_Lambda(  anOutput,
            'Async Request and Reply',
            u'elid_AsyncRequest_collapsible_dl', 
            lambda : pRenderTechnical_AsyncRequest( 
                anOutput, 
                unContextualObject, 
                aTranslationsCache,
            ),
            False,
        )
        anOutput.write("""
            <br/><br/>
            \n"""
        )
        
    anOutput.write("""
        <br/>
        \n"""
    )
        
    return None






    
def pRenderTechnical_AsyncRequest( 
    anOutput, 
    unContextualObject, 
    aTranslationsCache):
    """Render the AsyncRequest technical section of the translations browser.
    
    """    
       
    anOutput.write( u""" 
        <br/>
         <span><strong>Last asynchronous Request</strong></span>
        <br/>
        <textarea
            readonly="readonly"
            rows="4"
            columns="72"
            name="theTRAAsyncRequest_Display_Field" 
            id="theTRAAsyncRequest_Display_Field" 
            style="font-size: 8pt;">-no request-</textarea> 
        <br/>
        <br/>
        <span><strong>Last asynchcronous Response</strong></span>
        <br/>
        <textarea
            readonly="readonly"
            rows="18"
            columns="72"
            name="theTRAAsyncRequest_Response_Display_Field" 
            id="theTRAAsyncRequest_Response_Display_Field" 
            style="font-size: 8pt;">-no request-</textarea> 
        <br/>
        <br/>
        \n""" 
    )
                
    return None






    
def pRenderTechnical_UserInterfaceEvents( 
    anOutput, 
    unContextualObject, 
    aTranslationsCache):
    """Render the _UserInterfaceEvents technical section of the translations browser.
    
    """    
       
    anOutput.write( u""" 
        <br/>
        <span><strong>User Interface Events</strong></span>
        &emsp;
        <button type="button" id="cid_TRAResetUserInterfaceEventsLog" name="cid_TRAResetUserInterfaceEventsLog" onclick="pTRAResetUserInterfaceEventsLog(); return true" >Clear</button>
        <br/>
        <textarea
            readonly="readonly"
            rows="12"
            columns="72"
            name="theUserInterfaceEvents_Display_Field" 
            id="theUserInterfaceEvents_Display_Field" 
            style="font-size: 8pt;"></textarea> 
        <br/>
        <br/>
        \n""" 
    )
                
    return None



 
    
def pRenderTechnical_FormSubmit( 
    anOutput, 
    unContextualObject, 
    pFormSubmit,
    aTranslationsCache):
    """Render the form submit technical section of the translations browser.
    
    """    
       
    anOutput.write( u""" 
        <br/>
        <p>pFormSubmit %s</p>
        \n""" % str( pFormSubmit).replace('<', '&lt;').replace('>', '&gt;') 
    )
                
    return None


        
        
def pRenderTechnical_Times( 
    anOutput, 
    unContextualObject,  
    pStartTime, 
    pEndTime, 
    pBrowseDuration, 
    unHayCambio, 
    pChangeDuration, 
    aTranslationsCache):
    """Render the processing times technical section of the translations browser.
    
    """           
        
    anOutput.write( u""" 
        <br/>
        <p >Write, Retrieval and Render %d ms</p>
        \n""" % ( pEndTime - pStartTime) 
    )
            
    if unHayCambio:
        anOutput.write( u"""                                   
            <br/>
            <p >Write %d ms</p>
            \n""" % int( pChangeDuration) 
        )                            
                                        
    anOutput.write( u"""                                   
        <br/>
        <p>Read %d ms</p>
        \n""" % int( pBrowseDuration) 
    )                            

    return None        
            
           
            



def pRenderTechnical_Profile( 
    anOutput, 
    unContextualObject,  
    theTitle, 
    theExecutionRecord,
    aTranslationsCache):
    """Render the detailed execution profiling technical section of the translations browser.
    
    """           

    if not theExecutionRecord:
        anOutput.write(  """
            <br/>
            <font size="2">
                <strong>
                    EMPTY  %(theTitle)s 
                </strong>
            </font>
            <br/>
            \n""" % { 
            'theTitle': theTitle, 
        })  
        
    else:
        anOutput.write(  """
            <br/>
            <font size="2">
                 <strong>
                    %(theTitle)s
                 </strong>
            </font>
            <br/>
            <font face="Courier,Courier-New,Courier New,Fixedsys" >
            \n""" % { 
            'theTitle': theTitle, 
        })        

        # ACV200903312200 until we manage to invoke the rendering external method, possibly not from here, but from the calling template
        # anOutput.write(  theExecutionRecord.fPrettyPrintProfilingResultHTML( theProfilingResult.get( 'root', [])))
        anOutput.write(  """
            </font>
            <br/>
            \n"""
        )
        
    return None
        
        




def pRenderTechnical_Request( 
    anOutput, 
    unContextualObject,  
    theTitle, 
    theRequestDumpString,
    aTranslationsCache):
    """Render the request technical section of the translations browser.
    
    """           
        
    if not theRequestDumpString:
        anOutput.write(  """
            <br/>
            <font size="2">
                <strong>
                    EMPTY  %(theTitle)s 
                </strong>
            </font>
            <br/>
            \n"""% { 
            'theTitle': theTitle, 
        })        
        
    else:
        anOutput.write(  """
            <br/>
            <font size="2">
                 <strong>
                    %(theTitle)s
                 </strong>
            </font>
            <br/>
            <font face="Courier,Courier-New,Courier New,Fixedsys" >
            \n""" % { 
            'theTitle': theTitle, 
        })        

        anOutput.write(  theRequestDumpString)
        anOutput.write(  """
            </font>
            <br/>
            \n"""
        )
            
    return None



















def pRenderCursorButtons( 
    anOutput, 
    unContextualObject,  
    theFirstTabindex,
    aTranslationsCache):
    """Render buttons to control the translations browser cursor.
    
    """
    
    mfTranslateI18N     = unContextualObject.fTranslateI18N
    mfAsUnicode         = unContextualObject.fAsUnicode
    
    
    anOutput.write( u"""  
    
        <!-- #################################################################
        SECTION: Buttons to navigate to first, prev, next and last
        ################################################################# -->

        <table cellspacing="0" cellpadding="0" frame="void" >
            <tbody>
                <tr>
                    <td align="right" valign="center" >   
                        <table width="120" cellspacing="0" cellpadding="0" frame="void" >
                            <tbody>
                                <tr>
                                    <td width="25%%" align="center" valign="center" >
                                        <img tabindex=%(tabindex_1)d class="TRAstyle_Clickable" onclick="fTRAGoTo_Sync( 'GoToFirst'); return true;" 
                                            src="%(pAbsoluteURL)s/tra_primero.gif" alt="%(gvSIGi18n_traducciones_iraprimero_label)s" title="%(gvSIGi18n_traducciones_iraprimero_label)s" id="icon-primero" />
                                    </td>                                            
                                    <td width="25%%" align="center" valign="center" >
                                        <img tabindex=%(tabindex_2)d  class="TRAstyle_Clickable" onclick="fTRAGoTo_Sync( 'GoToPrevious'); return true;" 
                                            src="%(pAbsoluteURL)s/tra_anterior.gif"  alt="%(gvSIGi18n_traducciones_iraanterior_label)s" title="%(gvSIGi18n_traducciones_iraanterior_label)s" id="icon-anterior" />
                                    </td>
                                    <td width="25%%" align="center" valign="center" >
                                        <img tabindex=%(tabindex_3)d class="TRAstyle_Clickable" onclick="fTRAGoTo_Sync( 'GoToNext'); return true;" 
                                            src="%(pAbsoluteURL)s/tra_siguiente.gif" alt="%(gvSIGi18n_traducciones_irasiguiente_label)s" title="%(gvSIGi18n_traducciones_irasiguiente_label)s" id="icon-siguiente" />
                                        </button>
                                    </td>
                                    <td width="25%%" align="center" valign="center" >
                                        <img tabindex=%(tabindex_4)d  class="TRAstyle_Clickable" onclick="fTRAGoTo_Sync( 'GoToLast'); return true;" 
                                            src="%(pAbsoluteURL)s/tra_ultimo.gif"  alt="%(gvSIGi18n_traducciones_iraultimo_label)s" title="%(gvSIGi18n_traducciones_iraultimo_label)s" id="icon-ultimo" />
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </td> 
                </tr>
            </tbody>
        </table>
        """ % {
        'tabindex_1':                                     theFirstTabindex,  
        'tabindex_2':                                     theFirstTabindex + 1,  
        'tabindex_3':                                     theFirstTabindex + 2,  
        'tabindex_4':                                     theFirstTabindex + 3,  
        'pAbsoluteURL':                                   unContextualObject.absolute_url(),
        'gvSIGi18n_traducciones_bloquesiguiente_label' : aTranslationsCache[ 'gvSIGi18n_traducciones_bloquesiguiente_label'], 
        'gvSIGi18n_traducciones_iraprimero_label':       aTranslationsCache[ 'gvSIGi18n_traducciones_iraprimero_label'],
        'gvSIGi18n_traducciones_iraanterior_label':      aTranslationsCache[ 'gvSIGi18n_traducciones_iraanterior_label'],
        'gvSIGi18n_traducciones_irasiguiente_label':     aTranslationsCache[ 'gvSIGi18n_traducciones_irasiguiente_label'],
        'gvSIGi18n_traducciones_iraultimo_label':        aTranslationsCache[ 'gvSIGi18n_traducciones_iraultimo_label'],
        'gvSIGi18n_bloquesdea_parameter_label':          mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_bloquesdea_parameter_label', 'Block size-'), 
    })
            
    return None


     
            
            
  



#def pRenderBackToCatalog( 
    #anOutput, 
    #unContextualObject):
    #"""Render a link to go back to the TRACatalogo.
    
    #"""
    
    #mfTranslateI18N     = unContextualObject.fTranslateI18N
    #mfAsUnicode         = unContextualObject.fAsUnicode
    


    #anOutput.write( u"""  

        #<!-- #################################################################
         #SECTION: Link to navigate back to Catalogo container 
         ################################################################## -->
         
        #<a href="%(pCatalogoAbsoluteURL)s" class="state-visible" title="%(gvSIGi18n_catalogo_action_label)s" >
            #<img src="%(pCatalogoAbsoluteURL)s/contenedor.gif" alt="%(gvSIGi18n_catalogo_action_label)s" title="%(gvSIGi18n_catalogo_action_label)s" id="icon-contenedor" />                                        
            #%(gvSIGi18n_catalogo_action_label)s
        #</a>
        #\n""" % { 
        #'pCatalogoAbsoluteURL':                                 unContextualObject.absolute_url(), 
        #'gvSIGi18n_catalogo_action_label':              mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_catalogo_action_label', 'Catalog-'),  
    #})

                
    #return None
        
