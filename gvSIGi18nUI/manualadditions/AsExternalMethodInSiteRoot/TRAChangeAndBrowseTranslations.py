# -*- coding: utf-8 -*-
#
# File: TRAChangeAndBrowseTranslations.py
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



from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fMillisecondsNow



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

from Products.gvSIGi18n.TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_BrowseTranslations, cUseCase_TRATraduccionComment





from Products.gvSIGi18nTool.TRAgvSIGi18nTool_Constants import cTRAgvSIGi18nToolId

from Products.ModelDDvlPloneTool.ModelDDvlPloneToolLoadConstants import cModelDDvlPloneToolId





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
    'theSearchFechaTraduccionInicial',     
    'theSearchFechaTraduccionFinal',     
    'theSearchUsuarioRevisor',      
    'theSearchFechaRevisionInicial',       
    'theSearchFechaRevisionFinal',       
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



def _fSizes_Display_FontSize( theCodigoIdioma):
    
    unasSizes = cLanguageSizes.get( theCodigoIdioma, None)
    if not unasSizes:
        unasSizes = cLanguageSizes.get( cLanguageSizes_DefaultKey, None)
        if not unasSizes:
            return 1
        

    return unasSizes.get( 'display_font_size', 1)





def _fSizes_Edit_FontSize( theCodigoIdioma):
    
    unosLanguageDimensionFactors = cLanguageDimension_SpecialLanguageFactors.get( theCodigoIdioma, None)
    if not unosLanguageDimensionFactors:
        return cLanguageDimension_Edit_FontSize_default
    
    unLanguage_Edit_FontSize = unosLanguageDimensionFactors[ 1]
    
    return unLanguage_Edit_FontSize







def TRAChangeAndBrowseTranslations( 
    theRequest, 
    theCatalogo, 
    thePermissionsCache     =None, 
    theRolesCache           =None,
    theParentExecutionRecord=None):
    """Main service for translations browsing, editing and state change.
    
    Entry point invoked from a template.
    
    """
    aPortalURL          = ''
    aCatalogoURL        = ''
    
    fCGIE               = lambda theString: theString
    mfCRs2BRs           = lambda theString: theString
    mfTranslateI18N     = lambda theDomain, theSymbol, theDefault: theDefault or theSymbol
    mfAsUnicode         = lambda theString: theString
    

    
    if theCatalogo == None:
        return _pEmptyPageContents(  
            unContextualObject      =theCatalogo,                                                                                                                          
            unHeader                =mfTranslateI18N( 'gvSIGi18n', cResultCondition_MissingParameter_Catalogo, cResultCondition_MissingParameter_Catalogo + '-'), 
            unMessage               ='theCatalogo',                                                                                                               
            aPortalURL              =aPortalURL,                                                                                                                  
            aCatalogoURL            =aCatalogoURL,                                                                                                                  
            fCGIE                   =fCGIE,                                                                                                                       
            mfCRs2BRs               =mfCRs2BRs,                                                                                                                   
            mfTranslateI18N         =mfTranslateI18N,                                                                                                                  
            mfAsUnicode             =mfAsUnicode,                                                                                                                  
            aTranslationsCache      =None,                                                                                                                         
        )    
   
    

    aTRAgvSIGi18n_tool = getToolByName( theCatalogo, cTRAgvSIGi18nToolId, None)
    if aTRAgvSIGi18n_tool == None:
        return _pEmptyPageContents(  
            unContextualObject      =theCatalogo,                                                                                                                          
            unHeader                =mfTranslateI18N( 'gvSIGi18n', cResultCondition_ErrorInternal_Missing_TRAgvSIGi18nTool, cResultCondition_ErrorInternal_Missing_TRAgvSIGi18nTool + '-'), 
            unMessage               =cTRAgvSIGi18nToolId,                                                                                                               
            aPortalURL              =aPortalURL,                                                                                                                  
            aCatalogoURL            =aCatalogoURL,                                                                                                                  
            fCGIE                   =fCGIE,                                                                                                                       
            mfCRs2BRs               =mfCRs2BRs,                                                                                                                   
            mfTranslateI18N         =mfTranslateI18N,                                                                                                                  
            mfAsUnicode             =mfAsUnicode,                                                                                                                  
            aTranslationsCache      =None,                                                                                                                         
        )
         
    
    
    unExecutionRecord = aTRAgvSIGi18n_tool.fStartExecution( 
        theContextualElement    =theCatalogo,
        theExecutedKind         ='external method', 
        theExecutedName         ='TRAChangeAndBrowseTranslations', 
        theParentExecutionRecord=theParentExecutionRecord,
    )
      
    
    fCGIE               = aTRAgvSIGi18n_tool.fCGIE
    mfCRs2BRs           = aTRAgvSIGi18n_tool.fCRs2BRs
    mfTranslateI18N     = lambda theDomain, theSymbol, theDefault: fCGIE( aTRAgvSIGi18n_tool.fTranslateI18N( theContextualElement=theCatalogo, theI18NDomain=theDomain, theString=theSymbol, theDefault=theDefault, theTranslationService=None))
    mfAsUnicode         = lambda theString: aTRAgvSIGi18n_tool.fAsUnicode( theContextualElement=theCatalogo, theString=theString, theTranslationService=aTranslationService)
    
        
    if not theRequest:
        return _pEmptyPageContents( 
            unContextualObject      =theCatalogo,                                                                                                                          
            unHeader                =mfTranslateI18N( 'gvSIGi18n', cResultCondition_MissingParameter_Request, cResultCondition_MissingParameter_Request + '-'), 
            unMessage               ='theRequest',                                                                                                               
            aPortalURL              =aPortalURL,                                                                                                                  
            aCatalogoURL            =aCatalogoURL,                                                                                                                  
            fCGIE                   =fCGIE,                                                                                                                       
            mfCRs2BRs               =mfCRs2BRs,                                                                                                                   
            mfTranslateI18N         =mfTranslateI18N,                                                                                                                  
            mfAsUnicode             =mfAsUnicode,                                                                                                                  
            aTranslationsCache      =None,                                                                                                                                     
        )
     
    
    aTranslationService = aTRAgvSIGi18n_tool.getTranslationServiceTool( theContextualElement=theCatalogo)
    if aTranslationService == None:
        return _pEmptyPageContents(  
            unContextualObject      =theCatalogo,                                                                                                                          
            unHeader                =mfTranslateI18N( 'gvSIGi18n', cResultCondition_ErrorInternal_Missing_TranslationServiceTool, cResultCondition_ErrorInternal_Missing_TranslationServiceTool + '-'), 
            unMessage               ='getTranslationServiceTool',                                                                                                               
            aPortalURL              =aPortalURL,                                                                                                                  
            aCatalogoURL            =aCatalogoURL,                                                                                                                  
            fCGIE                   =fCGIE,                                                                                                                       
            mfCRs2BRs               =mfCRs2BRs,                                                                                                                   
            mfTranslateI18N         =mfTranslateI18N,                                                                                                                  
            mfAsUnicode             =mfAsUnicode,                                                                                                                  
            aTranslationsCache      =None,                                                                                                                                     
        )
    
    
    aMDDModelDDvlPlone_tool = getToolByName( theCatalogo, cModelDDvlPloneToolId, None)
    if aMDDModelDDvlPlone_tool == None:
        return _pEmptyPageContents(  
            unContextualObject      =theCatalogo,                                                                                                                          
            unHeader                =mfTranslateI18N( 'gvSIGi18n', cResultCondition_MissingParameter_Missing_ModelDDvlPloneTool, cResultCondition_MissingParameter_Missing_ModelDDvlPloneTool + '-'), 
            unMessage               =cModelDDvlPloneToolId,                                                                                                               
            aPortalURL              =aPortalURL,                                                                                                                  
            aCatalogoURL            =aCatalogoURL,                                                                                                                  
            fCGIE                   =fCGIE,                                                                                                                       
            mfCRs2BRs               =mfCRs2BRs,                                                                                                                   
            mfTranslateI18N         =mfTranslateI18N,                                                                                                                  
            mfAsUnicode             =mfAsUnicode,                                                                                                                  
            aTranslationsCache      =None,                                                                                                                                     
        )
             
    
    
        
    
    aPortalURL   = aMDDModelDDvlPlone_tool.fPortalURL()   
    aCatalogoURL = aTRAgvSIGi18n_tool.fCatalogoAbsoluteURL( theContextualElement=theCatalogo)
    
    anOutput = StringIO()
    
    pRenderProfile    = theRequest.get( 'theRenderProfile', '') == 'on'
    
    
    try:
            
            
        
        pStartTime = fMillisecondsNow()
        
        
        # #################################################################
        """Initialize caches if not supplied by service caller

        """
        
        unPermissionsCache = fDictOrNew( thePermissionsCache)
        unRolesCache       = fDictOrNew( theRolesCache)
                
        
         
        
        
        # #################################################################
        """Cache some translations to be used in the rendering below

        """
        
        aTranslationsCache = {}
        _pInitTranslationsCache( 
            theCatalogo, 
            fCGIE,
            aTRAgvSIGi18n_tool,
            aTranslationService,    
            aTranslationsCache
        )
       
        
                
        
        unaConfiguracionPaginaTraduccionesDict = aTRAgvSIGi18n_tool.fObtenerConfiguracionDict( 
            theContextualElement     =theCatalogo, 
            theAspectoConfiguracion  =cTRAConfiguracionAspecto_PaginaTraducciones,
        )

        unasTraduccionesPorPagina = cDefaultTraduccionesPorPagina
        unModoInteraccion         = cInteractionMode_Asynchronous
        
        if not ( unaConfiguracionPaginaTraduccionesDict == None):
            unasTraduccionesPorPagina = unaConfiguracionPaginaTraduccionesDict.get( 'traduccionesPorPaginaPorDefecto', cDefaultTraduccionesPorPagina)
            unModoInteraccion         = unaConfiguracionPaginaTraduccionesDict.get( 'modoInteraccionPorDefecto',       cInteractionMode_Default)
        
        
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
        pTraduccionesPorPagina          = theRequest.get( 'theTraduccionesPorPagina',       str( unasTraduccionesPorPagina))    
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
        pRequestedNombresModulos        = theRequest.get( 'theNewModuleNames',              '')
        pChangeCounter                  = theRequest.get( 'theChgCtr',                      '')
        pComentario                     = theRequest.get( 'Comentario',                     '')        
        pInteractionMode                = theRequest.get( 'theInteractionMode',             unModoInteraccion)
        pShowStateTransitionColumns     = theRequest.get( 'theShowStateTransitionColumns',  '') == 'on'
        pBatchStatusChanges             = theRequest.get( 'theBatchStatusChanges',          '') == 'on'
        pNoConfirmTranslationChanges    = theRequest.get( 'theNoConfirmTranslationChanges', '') == 'on'
        pNoConfirmStatusChanges         = theRequest.get( 'theNoConfirmStatusChanges',      '') == 'on'
        pNoConfirmTranslationDelete     = theRequest.get( 'theNoConfirmTranslationDelete',  '') == 'on'
        pRenderFormSubmit               = theRequest.get( 'theRenderFormSubmit',            '') == 'on'
        pRenderRequest                  = theRequest.get( 'theRenderRequest',               '') == 'on'
        pRenderFullRequest              = theRequest.get( 'theRenderFullRequest',           '') == 'on'
        pRenderTimes                    = theRequest.get( 'theRenderTimes',                 '') == 'on'
        pRenderAsyncRequest             = theRequest.get( 'theRenderAsyncRequest',          '') == 'on'
        pRenderUserInterfaceEvents      = theRequest.get( 'theRenderUserInterfaceEvents',   '') == 'on'
        
        pGoToSymbolIndex = 0
        aGoToSymbolIndexStr             = theRequest.get( 'theGoToSymbolIndex',             '')
        if aGoToSymbolIndexStr:
            try:
                pGoToSymbolIndex = int( aGoToSymbolIndexStr)
            except:
                None
                
                
        pGoToPageIndex = 0
        aGoToPageIndexStr               = theRequest.get( 'theGoToPageIndex',               '')
        if aGoToPageIndexStr:
            try:
                pGoToPageIndex = int( aGoToPageIndexStr)
            except:
                None
        
        pGoToSymbolStartingWith         = theRequest.get( 'theGoToSymbolStartingWith',      '')

        
        
        
        pRequestedNuevoEstadoTraduccion = theRequest.get( 'theNuevoEstadoTraduccion',       '') 
     
        pEditorKeyCRAction               = theRequest.get( 'theKeyAction_CR',               cKeyAction_Default_CR)
        pEditorKeyTabAction              = theRequest.get( 'theKeyAction_Tab',              cKeyAction_Default_Tab)

        pBatchIdsAndCounters_Traducida   = [ ]
        pBatch_Traducida                 = theRequest.get( 'theBatch_Traducida',       '')
        if pBatch_Traducida:
            someIdsWithCounters = pBatch_Traducida.split( ',')
            if someIdsWithCounters:
                for anIdWithCounter in someIdsWithCounters:
                    anIdAndCounter = anIdWithCounter.split( ' ')
                    if len( anIdAndCounter) > 1:
                        anId     = anIdAndCounter[ 0]
                        aCounter = anIdAndCounter[ 1]
                        pBatchIdsAndCounters_Traducida.append( [ anId, aCounter,])
                        

        pBatchIdsAndCounters_Revisada   = [ ]
        pBatch_Revisada                 = theRequest.get( 'theBatch_Revisada',       '')
        if pBatch_Revisada:
            someIdsWithCounters = pBatch_Revisada.split( ',')
            if someIdsWithCounters:
                for anIdWithCounter in someIdsWithCounters:
                    anIdAndCounter = anIdWithCounter.split( ' ')
                    if len( anIdAndCounter) > 1:
                        anId     = anIdAndCounter[ 0]
                        aCounter = anIdAndCounter[ 1]
                        pBatchIdsAndCounters_Revisada.append( [ anId, aCounter,])

                        
        pBatchIdsAndCounters_Definitiva   = [ ]
        pBatch_Definitiva                 = theRequest.get( 'theBatch_Definitiva',       '')
        if pBatch_Definitiva:
            someIdsWithCounters = pBatch_Definitiva.split( ',')
            if someIdsWithCounters:
                for anIdWithCounter in someIdsWithCounters:
                    anIdAndCounter = anIdWithCounter.split( ' ')
                    if len( anIdAndCounter) > 1:
                        anId     = anIdAndCounter[ 0]
                        aCounter = anIdAndCounter[ 1]
                        pBatchIdsAndCounters_Definitiva.append( [ anId, aCounter,])
                        
        
        
        
        # ################################################################
        """Capture Request dump strings
        
        """
        aRequestDumpString      = ''
        aFullRequestDumpString  = ''
        if pRenderRequest or pRenderFullRequest:
            aRequestDumpString, aFullRequestDumpString = _pRequestStrings( 
                theCatalogo, 
                theRequest, 
                pRenderRequest, 
                pRenderFullRequest, 
                aPortalURL,
                aCatalogoURL,
                fCGIE,
                mfCRs2BRs,
                mfTranslateI18N,
                mfAsUnicode,
                aTranslationsCache,
            ) 
        
             
            
        
    
        
        
       # ################################################################
        """Prepare service request parameters for change and browse phases.
        
        """
        
        pServiceRequestParameters = aTRAgvSIGi18n_tool.fNewVoidChangeAndBrowseTraslationsRequest(
            theContextualElement = theCatalogo,
        )
    

        
        # #################################################################
        """Prepare service request parameters for change 
        
        """
            
        if pMayHaveChanged:
            
            if pBatchIdsAndCounters_Traducida or pBatchIdsAndCounters_Revisada or pBatchIdsAndCounters_Definitiva:
                aRequestedChangeKind = cRequestedChangeKind_BatchCambioEstado
                
            elif pRequestedNuevoEstadoTraduccion == cAccion_DesactivarCadena:
                aRequestedChangeKind = cRequestedChangeKind_DesactivarCadena
            
            elif pRequestedNuevoEstadoTraduccion == cAccion_ActivarCadena:
                aRequestedChangeKind = cRequestedChangeKind_ActivarCadena
            
            elif pRequestedNuevoEstadoTraduccion == cAccion_ChangeStringModules:
                aRequestedChangeKind = cRequestedChangeKind_ChangeStringModules
            
            
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

      
      
                

      
            pServiceRequestParameters[ 'change_parameters'].update( {
                'change_counter':               pChangeCounter,
                'requested_change_kind':        aRequestedChangeKind,
                'simbolo_cadena_a_traducir':    pSimboloCadenaATraducir,
                'codigo_idioma_a_traducir':     pCodigoIdiomaATraducir,
                'cadena_traducida':             pCadenaTraducida,
                'comentario':                   pComentario,
                'batch_ids_traducida':          pBatchIdsAndCounters_Traducida,
                'batch_ids_revisada':           pBatchIdsAndCounters_Revisada,
                'batch_ids_definitiva':         pBatchIdsAndCounters_Definitiva,  
                'nombres_modulos_solicitados':  pRequestedNombresModulos,
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
        if pGoToSymbolIndex > 0:
            pModoDesplazamiento = cTRABrowseTranslations_ModoDesplazamiento_SymbolIndex
            
        elif pGoToPageIndex > 0:
            pModoDesplazamiento = cTRABrowseTranslations_ModoDesplazamiento_PageIndex
            
        elif pGoToSymbolStartingWith:
            pModoDesplazamiento = cTRABrowseTranslations_ModoDesplazamiento_SymbolStartingWith
            
        elif ( pFormSubmit == 'GoToFirst')        or (pFormSubmit == aTranslationsCache[ 'gvSIGi18n_traducciones_iraprimero_label']) or ( pFormSubmit.find( 'alt="%s"' % aTranslationsCache[ 'gvSIGi18n_traducciones_iraprimero_label']) >= 0):
            pModoDesplazamiento = cTRABrowseTranslations_ModoDesplazamiento_First
            
        elif ( pFormSubmit == 'GoToPrevious')   or (pFormSubmit == aTranslationsCache[ 'gvSIGi18n_traducciones_iraanterior_label']) or ( pFormSubmit.find( 'alt="%s"' % aTranslationsCache[ 'gvSIGi18n_traducciones_iraanterior_label']) >= 0):
            pModoDesplazamiento = cTRABrowseTranslations_ModoDesplazamiento_Previous
            
        elif ( pFormSubmit == 'GoToNext')       or  (pFormSubmit == aTranslationsCache[ 'gvSIGi18n_traducciones_bloquesiguiente_label']) or (pFormSubmit == aTranslationsCache[ 'gvSIGi18n_traducciones_irasiguiente_label']) or ( pFormSubmit.find( 'alt="%s"' % aTranslationsCache[ 'gvSIGi18n_traducciones_irasiguiente_label']) >= 0):
            pModoDesplazamiento = cTRABrowseTranslations_ModoDesplazamiento_Next
            
        elif ( pFormSubmit == 'GoToLast')       or (pFormSubmit == aTranslationsCache[ 'gvSIGi18n_traducciones_iraultimo_label']) or ( pFormSubmit.find( 'alt="%s"' % aTranslationsCache[ 'gvSIGi18n_traducciones_iraultimo_label']) >= 0):
            pModoDesplazamiento = cTRABrowseTranslations_ModoDesplazamiento_Last
            
        elif ( pGoTo == 'GoToFirst'):
            pModoDesplazamiento = cTRABrowseTranslations_ModoDesplazamiento_First
            
        elif ( pGoTo == 'GoToPrevious'):
            pModoDesplazamiento = cTRABrowseTranslations_ModoDesplazamiento_Previous
            
        elif ( pGoTo == 'GoToNext'):
            pModoDesplazamiento = cTRABrowseTranslations_ModoDesplazamiento_Next
            
        elif ( pGoTo == 'GoToLast'):
            pModoDesplazamiento = cTRABrowseTranslations_ModoDesplazamiento_Last
            
            
    
            
          
    
    
     
        # #################################################################
        """Set the TRACadena.simbolo to be used to re-position the cursor
        Use the first record (the one to be edited if the editor opens)
        in case of no displacement, or Prev (First or Last do not care)
        Use the last record, for Next displacement when the editor is not used

        """
        if pModoDesplazamiento == cTRABrowseTranslations_ModoDesplazamiento_Next:  #  and not pMostrarEditor:
            pSimboloCadenaCursor = pSimboloUltimaCadenaEnBloque
    
    
            
            
        # #################################################################
        """Set the desplazarUnRegistroOPagina
        
        """
        
        pDesplazarUnRegistroOPagina = cTRABrowseTranslations_Desplazar_UnaPagina
             
                
            
            
                
     
        # #################################################################
        """Compose browse parameters, including cursor and filter and section information
        
        """
        
        pSearchParameters = { 
            'idioma':                       pCodigoIdiomaCursor, 
            
            'simboloCadenaCursor':          pSimboloCadenaCursor, 

            'traduccionesPorPagina' :       pTraduccionesPorPagina, 
            'modoDesplazamiento':           pModoDesplazamiento, 
            'desplazarUnRegistroOPagina':   pDesplazarUnRegistroOPagina,

            'idiomasReferencia':            pIdiomasReferencia,         
            'estadosAIncluir':              pEstadosAIncluir, 

            'symbolIndex':                  pGoToSymbolIndex,
            'pageIndex':                    pGoToPageIndex,
            'symbolStartingWith':           pGoToSymbolStartingWith,
            
            'idCadena':                     theRequest.get( 'theSearchIdCadena',               ''), 

            'simbolo':                      theRequest.get( 'theSearchSimbolo',                ''),
            'cadenaTraducida':              theRequest.get( 'theSearchCadenaTraducida',        ''),
            'nombresModulos':               theRequest.get( 'theSearchNombresModulos',         ''),
            
            'usuarioCreador':               theRequest.get( 'theSearchUsuarioCreador',         ''), 
            'fechaCreacionInicial':         theRequest.get( 'theSearchFechaCreacionInicial',   ''), 
            'fechaCreacionFinal':           theRequest.get( 'theSearchFechaCreacionFinal',     ''), 
            
            'usuarioTraductor':             theRequest.get( 'theSearchUsuarioTraductor',       ''), 
            'fechaTraduccionInicial':       theRequest.get( 'theSearchFechaTraduccionInicial', ''), 
            'fechaTraduccionFinal':         theRequest.get( 'theSearchFechaTraduccionFinal',   ''), 
            
            'usuarioRevisor':               theRequest.get( 'theSearchUsuarioRevisor',         ''),  
            'fechaRevisionInicial':         theRequest.get( 'theSearchFechaRevisionInicial',   ''),  
            'fechaRevisionFinal':           theRequest.get( 'theSearchFechaRevisionFinal',     ''),  
            
            'usuarioCoordinador':           theRequest.get( 'theSearchUsuarioCoordinador',     ''),  
            'fechaDefinitivoInicial':       theRequest.get( 'theSearchFechaDefinitivoInicial', ''),  
            'fechaDefinitivoFinal':         theRequest.get( 'theSearchFechaDefinitivoFinal',   ''),  

            'usuarioModificador':           theRequest.get( 'theSearchUsuarioModificador',     ''),  
            'fechaModificacionInicial':     theRequest.get( 'theSearchFechaModificacionInicial',''),  
            'fechaModificacionFinal':       theRequest.get( 'theSearchFechaModificacionFinal', ''),  

            'cadenasInactivas':             theRequest.get( 'theInactiveStrings',              ''),  
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
        
        pServiceResponse = aTRAgvSIGi18n_tool.fChangeAndBrowseTranslations( 
            theContextualElement        =theCatalogo,
            theServiceRequest           =pServiceRequestParameters, 
            thePermissionsCache         =unPermissionsCache, 
            theRolesCache               =unRolesCache, 
            theParentExecutionRecord    =unExecutionRecord,
        ) 

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
                return _pEmptyPageContents( 
                    unContextualObject      =theCatalogo,                                                                                                                          
                    unHeader                =aTranslationsCache[ 'gvSIGi18n_BrowseTranslationsFailure_Exception_msg'], 
                    unMessage               =aTranslationsCache[ 'gvSIGi18n_BrowseTranslationsFailure_MakeSureYouAreLoggedOrContactSiteAdministrator_msg'],                                                                                                               
                    aPortalURL              =aPortalURL,                                                                                                                  
                    aCatalogoURL            =aCatalogoURL,                                                                                                                  
                    fCGIE                   =fCGIE,                                                                                                                       
                    mfCRs2BRs               =mfCRs2BRs,                                                                                                                   
                    mfTranslateI18N         =mfTranslateI18N,                                                                                                                  
                    mfAsUnicode             =mfAsUnicode,                                                                                                                  
                    aTranslationsCache      =aTranslationsCache,                                                                                                                                     
                )
            else:
                return _pEmptyPageContents( theCatalogo,  
                    unContextualObject      =theCatalogo,                                                                                                                          
                    unHeader                =aTranslationsCache[ 'gvSIGi18n_BrowseTranslationsFailure_Condition_msg'], 
                    unMessage               =mfTranslateI18N( 'gvSIGi18n', pBrowseCondition, pBrowseCondition + '-' ),                                                                                                               
                    aPortalURL              =aPortalURL,                                                                                                                  
                    aCatalogoURL            =aCatalogoURL,                                                                                                                  
                    fCGIE                   =fCGIE,                                                                                                                       
                    mfCRs2BRs               =mfCRs2BRs,                                                                                                                   
                    mfTranslateI18N         =mfTranslateI18N,                                                                                                                  
                    mfAsUnicode             =mfAsUnicode,                                                                                                                  
                    aTranslationsCache      =aTranslationsCache,                                                                                                                                     
                 )
         
        
        pDatosTraducciones                  = pBrowseResult.get( 'datosTraducciones',           [])
        pEstadosIncluidos                   = pBrowseResult.get( 'estadosIncluidos',            [])
        pInformeEstadosTodasCadenas         = pBrowseResult.get( 'informeEstadosTodasCadenas',  cInformeEstadosVacio)
        pInformeEstadosFiltrados            = pBrowseResult.get( 'informeEstadosFiltrados',     cInformeEstadosVacio)
        pDictsTraduccionesIdiomasReferencia = pBrowseResult.get( 'dictsTraduccionesIdiomasReferencia',   { })
        pTraduccionesPorPagina              = pBrowseResult.get( 'traduccionesPorPagina',       unasTraduccionesPorPagina)
        pTotalTranslations                  = pBrowseResult.get( 'total_translations', 0)
        
        pUseCaseQueryResults                = pBrowseResult.get( 'use_case_query_results',      [])
        
        pAllowedStateTransitions            = pBrowseResult.get( 'allowed_state_transitions',   {}) 
        pAllTargetStatusChanges             = pBrowseResult.get( 'all_target_state_changes',    set()) 
        
        pAllowInvalidateStringTranslations  = pBrowseResult.get( 'allow_invalidate_string_translations',   False) 

        
        
        pBrowsingInactiveStrings            = pBrowseResult.get( 'browsing_inactive_strings',   False) 
        pAllowDeactivateStrings             = pBrowseResult.get( 'allow_deactivate_strings',    False) 
        pAllowActivateStrings               = pBrowseResult.get( 'allow_activate_strings',      False) 
        
        pAllowChangeStringsModules          = pBrowseResult.get( 'allow_change_strings_modules',False) 
        pAllowRemoveStringsModules          = pBrowseResult.get( 'allow_remove_strings_modules',False)
        pAllowRemoveStringsModulesString    = ( pAllowRemoveStringsModules and '1') or ''
        
        
        pWritePermission                    = pBrowseResult.get( 'write_permission',            False) 
        
        
        pShowStateTransitionColumnsOption = len( set( [ cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva,]).intersection( pAllTargetStatusChanges)) > 0
        pShowStateTransitionColumns       = pShowStateTransitionColumnsOption and pShowStateTransitionColumns
        
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
            return _pEmptyPageContents( 
                unContextualObject      =theCatalogo,                                                                                                                          
                unHeader                =aTranslationsCache[ 'gvSIGi18n_AccessFailedAndPromptYouHavePermission_label'], 
                unMessage               ='',                                                                                                               
                aPortalURL              =aPortalURL,                                                                                                                  
                aCatalogoURL            =aCatalogoURL,                                                                                                                  
                fCGIE                   =fCGIE,                                                                                                                       
                mfCRs2BRs               =mfCRs2BRs,                                                                                                                   
                mfTranslateI18N         =mfTranslateI18N,                                                                                                                  
                mfAsUnicode             =mfAsUnicode,                                                                                                                  
                aTranslationsCache      =aTranslationsCache,                                                                                                                                     
            )
    

        
        
        
       # #################################################################
        """Verify and gather security access to Languages
        
        """
        
        unosIdiomasAccesibles = pBrowseTranslationsUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'languages', {}).get( 'accepted_final_objects', [])
        if not unosIdiomasAccesibles:
            return _pEmptyPageContents( 
                unContextualObject      =theCatalogo,                                                                                                                          
                unHeader                =aTranslationsCache[ 'gvSIGi18n_NoAccessibleLanguages_label'], 
                unMessage               ='',                                                                                                               
                aPortalURL              =aPortalURL,                                                                                                                  
                aCatalogoURL            =aCatalogoURL,                                                                                                                  
                fCGIE                   =fCGIE,                                                                                                                       
                mfCRs2BRs               =mfCRs2BRs,                                                                                                                   
                mfTranslateI18N         =mfTranslateI18N,                                                                                                                  
                mfAsUnicode             =mfAsUnicode,                                                                                                                  
                aTranslationsCache      =aTranslationsCache,                                                                                                                                     
            )
               
        
        unIdiomaCursor          = None
        unosCodigosIdiomasEInternacionales    = [ ]
        
        for unIdioma in unosIdiomasAccesibles:
            unCodigoIdioma      = aTRAgvSIGi18n_tool.fCodigoIdiomaEnGvSIG( 
                theContextualElement=unIdioma,
            )
            unosCodigosIdiomasEInternacionales.append( [ unCodigoIdioma, unIdioma.getCodigoInternacionalDeIdioma(),])
            if unCodigoIdioma == pCodigoIdiomaCursor:
                unIdiomaCursor          = unIdioma
                
        if not unIdiomaCursor:
            return _pEmptyPageContents( 
                unContextualObject      =theCatalogo,                                                                                                                          
                unHeader                ='language: %s %s' % ( 
                    mfAsUnicode( pCodigoIdiomaCursor),
                    aTranslationsCache[ 'gvSIGi18n_LanguageNotAccessible_label'],
                ), 
                unMessage               ='',                                                                                                               
                aPortalURL              =aPortalURL,                                                                                                                  
                aCatalogoURL            =aCatalogoURL,                                                                                                                  
                fCGIE                   =fCGIE,                                                                                                                       
                mfCRs2BRs               =mfCRs2BRs,                                                                                                                   
                mfTranslateI18N         =mfTranslateI18N,                                                                                                                  
                mfAsUnicode             =mfAsUnicode,                                                                                                                  
                aTranslationsCache      =aTranslationsCache,                                                                                                                                     
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
                    if pRegistrosHistoria:
                        pRegistrosHistoria.reverse()
            
            
            
            
    
            

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
        """Render program constants: for Javascript behavior control
        
        """
        anOutput.write( u"""     
                        
            <!-- #################################################################
            SECTION: Internationalized constants 
            ################################################################# -->
            <font color="White"> 
                <span id="cTRAId_AllowRemoveStringsModules"        class="TRAstyle_NoDisplay">%(gvSIGi18n_AllowRemoveStringsModules)s</span>
            </font>
            \n""" % { 
            'gvSIGi18n_AllowRemoveStringsModules':       pAllowRemoveStringsModulesString,
            }
        )


    
        # #################################################################
        """Render program constants: portal URL for scripts to compose URLs for icons, and the URL for asynch requests
        
        """
        anOutput.write( u"""     
                        
            <!-- #################################################################
            SECTION: Portal URL 
            ################################################################# -->
            <font color="White"> 
                <span id="cTRAId_PortalURL" class="TRAstyle_NoDisplay">%(PortalURL)s</span>
                <span id="cTRAId_AsynchRequestURL" class="TRAstyle_NoDisplay">%(AsynchRequestURL)s</span>
            </font>
            \n""" % { 
            'PortalURL':        '%s'                   % aPortalURL,
            'AsynchRequestURL': '%s/TRATraducir_Async' % aCatalogoURL,
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
                    
                    
               
        _pRenderScripts( 
            anOutput, 
            theCatalogo,
        )   
        
        
        _pRenderStyles(            
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
     
                        
       
        if not aTRAgvSIGi18n_tool.fCatalogoAllowWrite( theContextualElement=theCatalogo):
            anOutput.write( u"""                 
          
            <!-- #################################################################
            SECTION: Notice: the catalog is locked against modifications
            ################################################################# -->
            <table width="100%%" noborder >
                <tr>
                    <td>
                         <div class="portalMessage" >
                            <span>%s</span>
                        </div>
                    </td>
                    <td width="80" />
                </tr>
            </table>
            """ %  aTranslationsCache[ 'gvSIGi18n_TranslationsCatalogIsLockedAgainstModifications']
            )
            
            
            
            
        if ( not aTRAgvSIGi18n_tool.fAllowWrite( theContextualElement=unIdiomaCursor)) and aTRAgvSIGi18n_tool.fCatalogoAllowWrite( theContextualElement=theCatalogo):
            anOutput.write( u"""                 
          
            <!-- #################################################################
            SECTION: Notice: the language is locked against modifications
            ################################################################# -->
            <table width="100%%" noborder >
                <tr>
                    <td>
                         <div class="portalMessage" >
                            <span>%s</span>
                        </div>
                    </td>
                    <td width="80" />
                </tr>
            </table>
            """ %  aTranslationsCache[ 'gvSIGi18n_SelectedLanguageIsLockedAgainstModifications']
            )
            
            
            
            

        _pRenderCabecera( 
            anOutput                =anOutput,               
            unContextualObject      =theCatalogo,            
            theBrowseResult         =pBrowseResult,          
            pLanguagesNamesAndFlags =pLanguagesNamesAndFlags,
            pTodosCodigosIdiomas    =pTodosCodigosIdiomas,   
            pCodigoIdiomaCursor     =pCodigoIdiomaCursor,    
            aPortalURL              =aPortalURL,             
            aCatalogoURL            =aCatalogoURL,           
            fCGIE                   =fCGIE,                  
            mfCRs2BRs               =mfCRs2BRs,              
            mfTranslateI18N         =mfTranslateI18N,        
            mfAsUnicode             =mfAsUnicode,            
            aTranslationsCache      =aTranslationsCache,      
        )
        
                
          
        
         
        _pRenderCollapsibleSelectorIdiomasReferencia( 
            anOutput                               =anOutput,                               
            unContextualObject                     =theCatalogo,                            
            pLanguagesNamesAndFlags                =pLanguagesNamesAndFlags,                
            pTodosCodigosIdiomasEInternacionales   =pTodosCodigosIdiomasEInternacionales,   
            pIdiomasReferencia                     =pIdiomasReferencia,                     
            unaConfiguracionPaginaTraduccionesDict =unaConfiguracionPaginaTraduccionesDict, 
            aPortalURL                             =aPortalURL,                             
            aCatalogoURL                           =aCatalogoURL,                           
            fCGIE                                  =fCGIE,                                  
            mfCRs2BRs                              =mfCRs2BRs,                              
            mfTranslateI18N                        =mfTranslateI18N,                        
            mfAsUnicode                            =mfAsUnicode,                            
            aTranslationsCache                     =aTranslationsCache                       
        )

        
        
        _pRenderCollapsibleControlPresentacion( 
            anOutput                               =anOutput,                              
            unContextualObject                     =theCatalogo,                           
            pTraduccionesPorPagina                 =pTraduccionesPorPagina,                
            pInteractionMode                       =pInteractionMode,                      
            pMostrarInforme                        =pMostrarInforme,                       
            pMostrarLista                          =pMostrarLista,                         
            pMostrarDetallesTraduccion             =pMostrarDetallesTraduccion,            
            pMostrarHistoria                       =pMostrarHistoria,                      
            pShowStateTransitionColumnsOption      =pShowStateTransitionColumnsOption,     
            pShowStateTransitionColumns            =pShowStateTransitionColumns,           
            pShowBatchStatusChangesOption          =pShowBatchStatusChangesOption,         
            pBatchStatusChanges                    =pBatchStatusChanges,  
            pNoConfirmTranslationChanges           =pNoConfirmTranslationChanges,
            pNoConfirmStatusChanges                =pNoConfirmStatusChanges,
            pNoConfirmTranslationDelete            =pNoConfirmTranslationDelete,
            pCanComment                            =pCanComment,                           
            pEditorKeyCRAction                     =pEditorKeyCRAction,                    
            pEditorKeyTabAction                    =pEditorKeyTabAction,                   
            pRenderFormSubmit                      =pRenderFormSubmit,                     
            pRenderRequest                         =pRenderRequest,                        
            pRenderFullRequest                     =pRenderFullRequest,                    
            pRenderTimes                           =pRenderTimes,                          
            pRenderProfile                         =pRenderProfile,                        
            pRenderAsyncRequest                    =pRenderAsyncRequest,                   
            pRenderUserInterfaceEvents             =pRenderUserInterfaceEvents,            
            unaConfiguracionPaginaTraduccionesDict =unaConfiguracionPaginaTraduccionesDict,
            aPortalURL                             =aPortalURL,                            
            aCatalogoURL                           =aCatalogoURL,                          
            fCGIE                                  =fCGIE,                                 
            mfCRs2BRs                              =mfCRs2BRs,                             
            mfTranslateI18N                        =mfTranslateI18N,                       
            mfAsUnicode                            =mfAsUnicode,                           
            aTranslationsCache                     =aTranslationsCache,                     
        )


        
        _pRenderCollapsibleFiltro( 
            anOutput              =anOutput,            
            unContextualObject    =theCatalogo,         
            pCodigoIdiomaCursor   =pCodigoIdiomaCursor, 
            pTodosNombresModulos  =pTodosNombresModulos,
            pEstadosIncluidos     =pEstadosIncluidos,   
            pSearchParameters     =pSearchParameters,   
            aPortalURL            =aPortalURL,          
            aCatalogoURL          =aCatalogoURL,        
            fCGIE                 =fCGIE,               
            mfCRs2BRs             =mfCRs2BRs,           
            mfTranslateI18N       =mfTranslateI18N,     
            mfAsUnicode           =mfAsUnicode,         
            aTranslationsCache    =aTranslationsCache,   
        )
        
        unasTraduccionesPorPagina = 1
        try:
            unasTraduccionesPorPagina = int( pTraduccionesPorPagina)
        except:
            None
            
        _pRenderCollapsibleGoTo( 
            anOutput           =anOutput,                                                                                                                
            unContextualObject =theCatalogo,                                                                                                             
            pNumberOfStrings   =pTotalTranslations,                                                                                                      
            pNumberOfPages     =int( pTotalTranslations / unasTraduccionesPorPagina)  + ((( pTotalTranslations % unasTraduccionesPorPagina) and 1) or 0),
            pSearchParameters  =pSearchParameters,                                                                                                       
            aPortalURL         =aPortalURL,                                                                                                              
            aCatalogoURL       =aCatalogoURL,                                                                                                            
            fCGIE              =fCGIE,                                                                                                                   
            mfCRs2BRs          =mfCRs2BRs,                                                                                                               
            mfTranslateI18N    =mfTranslateI18N,                                                                                                         
            mfAsUnicode        =mfAsUnicode,                                                                                                             
            aTranslationsCache =aTranslationsCache                                                                                                       
        )
                
        
          
        if pMostrarInforme:
            _pRenderCollapsibleInforme( 
                anOutput                    =anOutput,
                unContextualObject          =theCatalogo,
                pEstadosIncluidos           =pEstadosIncluidos,
                pInformeEstadosTodasCadenas =pInformeEstadosTodasCadenas,
                pInformeEstadosFiltrados    =pInformeEstadosFiltrados,
                pBrowsingInactiveStrings    =pBrowsingInactiveStrings,
                aPortalURL                  =aPortalURL,
                aCatalogoURL                =aCatalogoURL,
                fCGIE                       =fCGIE,
                mfCRs2BRs                   =mfCRs2BRs,
                mfTranslateI18N             =mfTranslateI18N,
                mfAsUnicode                 =mfAsUnicode,
                aTranslationsCache          =aTranslationsCache,
            )
        
        
                                               
                
        if pMostrarLista :
            unSimboloCadenaATraducirHolder = [ '',]
            _pRenderCollapsibleList( 
                anOutput                             =anOutput,                                    
                unContextualObject                   =theCatalogo,                                                         
                pBrowseResult                        =pBrowseResult,                                            
                pCodigoIdiomaCursor                  =pCodigoIdiomaCursor,                                
                pIdiomasReferencia                   =pIdiomasReferencia,                               
                pTodosNombresModulos                 =pTodosNombresModulos,                                
                pDatosTraducciones                   =pDatosTraducciones,                               
                pDictsTraduccionesIdiomasReferencia  =pDictsTraduccionesIdiomasReferencia,                                                
                pLanguagesNamesAndFlags              =pLanguagesNamesAndFlags,                                    
                theWritePermission                   =pWritePermission,                                
                pAllowedStateTransitions             =pAllowedStateTransitions,                                    
                pAllTargetStatusChanges              =pAllTargetStatusChanges,                                   
                pAllowInvalidateStringTranslations   =pAllowInvalidateStringTranslations,                                              
                pBrowsingInactiveStrings             =pBrowsingInactiveStrings,                                    
                pAllowDeactivateStrings              =pAllowDeactivateStrings,                                   
                pAllowActivateStrings                =pAllowActivateStrings,                                 
                pAllowChangeStringsModules           =pAllowChangeStringsModules,                                      
                unSimboloCadenaATraducirHolder       =unSimboloCadenaATraducirHolder,                                          
                pMostrarHistoria                     =pMostrarHistoria,                            
                pShowStateTransitionColumns          =pShowStateTransitionColumns,                                       
                pBatchStatusChanges                  =pBatchStatusChanges,                               
                aPortalURL                           =aPortalURL,                                                                         
                aCatalogoURL                         =aCatalogoURL,                        
                fCGIE                                =fCGIE,                              
                mfCRs2BRs                            =mfCRs2BRs,                          
                mfTranslateI18N                      =mfTranslateI18N,                           
                mfAsUnicode                          =mfAsUnicode,                        
                aTranslationsCache                   =aTranslationsCache,                              
                unRolesCache                         =unRolesCache,                       
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
            _pRenderEmpty( 
                anOutput           =anOutput,                                                                                           
                unContextualObject =theCatalogo,                                                                                                                 
                unHeader           =aTranslationsCache[ cResultCondition_NoMatchingTranslationsFound],                                                           
                unMessage          =aTranslationsCache[ 'gvSIGi18n_reviseLasCondicionesDeFiltroYBusqueda_message'],                                              
                aPortalURL         =aPortalURL,                                                                                                                  
                aCatalogoURL       =aCatalogoURL,                                                                                                                
                fCGIE              =fCGIE,                                                                                                                       
                mfCRs2BRs          =mfCRs2BRs,                                                                                                                   
                mfTranslateI18N    =mfTranslateI18N,                                                                                                             
                mfAsUnicode        =mfAsUnicode,                                                                                                                 
                aTranslationsCache =aTranslationsCache,                                                                                                           
            )
                
                   
        anOutput.write( u"""  
            </form>
            \n""" 
        )                    
            
            
        anOutput.write( u"""  
            <!-- #################################################################
            SECTION: Hidden elements to temporarily store the html content received in the asynchronous response
            ################################################################# -->
            
            <div class="TRAstyle_NoDisplay" id="cid_TRAAsyncResponseStore" >
                &ensp;
            </div>
            
            \n""" 
        )                    

    
        
        anOutput.write( u"""
            <!-- #####
            ## Hidden Field: the translation index number being edited
            ##########-->  
            
            <input type="hidden" id="theCadenaTraducida_index" name="theCadenaTraducida_index" value="" />
    
            \n""" 
        )
             
        
         
        
        _pRenderMessages( 
            anOutput           =anOutput,         
            unContextualObject =theCatalogo,                    
            aPortalURL         =aPortalURL,       
            aCatalogoURL       =aCatalogoURL,       
            fCGIE              =fCGIE,            
            mfCRs2BRs          =mfCRs2BRs,        
            mfTranslateI18N    =mfTranslateI18N,          
            mfAsUnicode        =mfAsUnicode,      
            aTranslationsCache =aTranslationsCache,
        )
            
        pEndTime = fMillisecondsNow()
            
            
        _pRenderCollapsibleTechnicalSections( 
            anOutput                   =anOutput,                  
            unContextualObject         =theCatalogo,                     
            pRenderFormSubmit          =pRenderFormSubmit,             
            pRenderRequest             =pRenderRequest,            
            pRenderFullRequest         =pRenderFullRequest,              
            pRenderTimes               =pRenderTimes,              
            pRenderProfile             =pRenderProfile, # to enable rendering of the placeholder for asynch execution profilings. Actual Rendering requested from the calling template. Sync execution profile is appended at the bottom of the rendered page.           
            pRenderAsyncRequest        =pRenderAsyncRequest,               
            pRenderUserInterfaceEvents =pRenderUserInterfaceEvents,                     
            pFormSubmit                =pFormSubmit,               
            pStartTime                 =pStartTime,                
            pEndTime                   =pEndTime,                  
            pBrowseDuration            =pBrowseDuration,           
            unHayCambio                =unHayCambio,               
            pChangeDuration            =pChangeDuration,           
            unExecutionRecord          =unExecutionRecord,             
            aRequestDumpString         =aRequestDumpString,              
            aFullRequestDumpString     =aFullRequestDumpString,                 
            aPortalURL                 =aPortalURL,                
            aCatalogoURL               =aCatalogoURL,              
            fCGIE                      =fCGIE,                     
            mfCRs2BRs                  =mfCRs2BRs,                 
            mfTranslateI18N            =mfTranslateI18N,           
            mfAsUnicode                =mfAsUnicode,               
            aTranslationsCache         =aTranslationsCache,                )
        
        
        anOutput.write( u"""
            <!-- #####
            ## Link to invoke a function that will hopefully open javascript debugger (i.e. causing an error)
            ##########-->  
            
            <br/>
            <p onclick="pTRAEnterDebugger(); return true;" ><font color="red"><strong><em>!</em></strong></font></p>
    
            \n""" 
        )
             
    
        aRendering = anOutput.getvalue()

        aStrippedRendering = _fStrippedRendering( aRendering)
            
        return aStrippedRendering
    
        
    finally:
        unExecutionRecord and unExecutionRecord.pEndExecution()
     
              
      


def _fStrippedRendering( theRendering):
    
    if not theRendering:
        return ''
    
    aSourceStream   = StringIO( theRendering)
    aStrippedStream = StringIO()
        
    aLine = aSourceStream.readline()
    while aLine:
        aStrippedStream.write( aLine.strip())
        aStrippedStream.write( '\n')
        
        aLine = aSourceStream.readline()
        
    aStripped = aStrippedStream.getvalue()
    
    return aStripped
        









def _pRequestStrings( 
    unContextualObject, 
    theRequest,
    pRenderRequest, 
    pRenderFullRequest, 
    aPortalURL,
    aCatalogoURL,
    fCGIE,
    mfCRs2BRs,
    mfTranslateI18N,
    mfAsUnicode,
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
                aKeyString = fCGIE( aRequestKey)
                unValueString = theRequest.get( aRequestKey, '!?')
                if unValueString.__class__.__name__ == "list":
                    unValueString = '[ %s ]' % ( ' '.join( unValueString))
                unValueString = fCGIE( unValueString)
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
    
    
    
    





   
def _pInitTranslationsCache( 
    unContextualObject, 
    fCGIE,
    aTRAgvSIGi18n_tool,
    aTranslationService,    
    aTranslationsCache):
    """Preload some translations into cache.
    
    """

    
    someDomainsStringsAndDefaultsToTranslate = [
        [ 'gvSIGi18n', [    
            
            [ 'gvSIGi18n_Confirmar_NavegarAIdiomaPrincipalYSimbolo_msgid', 'Please confirm that you want to navigate away from this language into the selected string in a different language-',],
            [ 'gvSIGi18n_AsyncPhase_RequestQueued_msgid',     'Request Queued.-',],
            [ 'gvSIGi18n_AsyncPhase_RequestSent_msgid',       'Request Sent.-',],
            [ 'gvSIGi18n_AsyncPhase_ResponseReceived_msgid',  'Response Received.-',],
            [ 'gvSIGi18n_AsyncPhase_ChangeSaved_msgid',       'Change Saved.-',],
            
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
            [ 'gvSIGi18n_TRATraduccion_attr_fechaModificacionTextual_label','Change Date-' ,],                                             
            [ 'gvSIGi18n_TRATraduccion_attr_usuarioModificador_label',  'Change User-' ,],  
            [ 'gvSIGi18n_Modificacion',                                 'Modification-' ,],  
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
            [ 'gvSIGi18n_TRATraduccion_attr_contadorCambios_label',     'Changes Counter-' ,],   
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
            [ 'gvSIGi18n_AppliesImmediatelyNoNeedToRefresh_help',       'Applies immediately, no need to refresh the page to make it effective.-',],
            [ 'gvSIGi18n_opcionesSection_title',                        'Options-',],
            [ 'gvSIGi18n_fecha_el',                                     'on-',],
            [ 'gvSIGi18n_usuario_por',                                  'by-',],
            [ 'gvSIGi18n_TRATraduccion_Creada',                         'Created-',],
            [ 'gvSIGi18n_ShowEditorDetails_label',                      'Display translation details in the editor',], 
            [ 'gvSIGi18n_PresentationOptions_NoNeedToRefresh_label',    'Options that do not require refreshing the page',],             
            [ 'gvSIGi18n_PresentationOptions_MustRefresh_label',        'Options that require refreshing the page',], 
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
            [ 'gvSIGi18n_Batch_ButtonLabel',                            'Batch-',],
            [ 'gvSIGi18n_TranslationAction_InvalidarTraduccionesCadena_label', 'Invalidate',],
            [ 'gvSIGi18n_TranslationAction_InvalidarTraduccionesCadena_help', 'Invalidate String Translations into all languages',],
            [ 'gvSIGi18n_ConfirmInvalidateStringTranslationsMsg',        'Do you want to INVALIDATE the String Translations into all languages',],
            [ 'gvSIGi18n_ReallyInvalidateStringTranslationsMsg',         'Do you REALLY want to INVALIDATE the String Translations into all languages',],
            [ 'gvSIGi18n_ConfirmTranslateMsg',                           'Do you want to CHANGE the string TRANSLATION',],
            [ 'gvSIGi18n_ReallyConfirmTranslateMsg',                     'Do you REALLY want to CHANGE the string TRANSLATION',],
            [ 'gvSIGi18n_ConfirmStatusChangeMsg',                        'Do you want to CHANGE STATUS of the Translation',],
            [ 'gvSIGi18n_ReallyConfirmStatusChangeMsg',                  'Do you REALLY want to CHANGE STATUS of the Translation',],
            [ 'gvSIGi18n_ConfirmDeleteMsg',                              'Do you want to DELETE string Translation',],
            [ 'gvSIGi18n_ReallyConfirmDeleteMsg',                        'Do you REALLY want to DELETE the string Translation',],
            [ 'gvSIGi18n_ConfirmBatchMsg',                               'Do you want to apply BATCH to ALL the SELECTED translations',],
            [ 'gvSIGi18n_ReallyConfirmBatchMsg',                         'Do you REALLY want to apply BATCH to ALL the SELECTED translations',],
            [ 'gvSIGi18n_InteracionStatusMessage',                       'Interaction Status Message-',],
            [ 'gvSIGi18n_TranslationAction_DesactivarCadena_label',      'Deactivate String-',],
            [ 'gvSIGi18n_TranslationAction_DesactivarCadena_help',       'Hide String symbol from all translation activity and all exports.-',],
            [ 'gvSIGi18n_TranslationAction_ActivarCadena_label',         'Activate String-',],
            [ 'gvSIGi18n_TranslationAction_ActivarCadena_help',          'Make String symbol available for translation activity and exports.-',],
            [ 'gvSIGi18n_ConfirmDeactivateStringMsg',                    'Do you want to DEACTIVATE the String, hiding it from all Translation activity and exports-',],
            [ 'gvSIGi18n_ReallyDeactivateStringMsg',                     'Do you REALLY want to DEACTIVATE the String, hiding it from all Translation activity and exports-',],
            [ 'gvSIGi18n_ConfirmActivateStringMsg',                      'Do you want to ACTIVATE the String, making it available for Translation and export-',],
            [ 'gvSIGi18n_ReallyActivateStringMsg',                       'Do you REALLY want to ACTIVATE the String, making it available for Translation and export-',],
            [ 'gvSIGi18n_BrowsingInactiveStrings_label',                 'Browsing Strings in Inactive State-',],
            [ 'gvSIGi18n_BrowsingInactive_collapsibleListLabel',         'Inactive-',],
            [ 'gvSIGi18n_ModulesEditor_Open',                            'Edit-',],
            [ 'gvSIGi18n_ModulesEditor_Close',                           'Cancel-',],
            [ 'gvSIGi18n_ModulesEditor_SaveStringModules',               'Save String Modules-',],
            [ 'gvSIGi18n_refrescar_action_label',                        'Refresh-',],
            [ 'gvSIGi18n_todas_label',                                   'All-',],
            [ 'gvSIGi18n_TranslationsFilter_help',                       'You may enter conditions for translations to match.\nAll conditions shall be met (AND logic, set intersection).\nClick Refresh button to update the list.-',],
            [ 'gvSIGi18n_TranslationsFilter_Reset_help',                 'You may retrieve all the translations\nresetting the filter, by clicking on the All button.-',],
            [ 'gvSIGi18n_TranslationHistoryAction_Desconocida',          'Unknown-',],
            [ 'gvSIGi18n_TranslationHistoryAction_Importar',             'Import-',],
            [ 'gvSIGi18n_TranslationHistoryAction_Ignorar',              'Ignore-',],
            [ 'gvSIGi18n_TranslationHistoryAction_Traducir',             'Translate-',],
            [ 'gvSIGi18n_TranslationHistoryAction_Comentar',             'Comment-',],
            [ 'gvSIGi18n_TranslationHistoryAction_HacerPendiente',       'Change to Pending-',],
            [ 'gvSIGi18n_TranslationHistoryAction_HacerTraducida',       'Change to Translated-',],
            [ 'gvSIGi18n_TranslationHistoryAction_HacerRevisada',        'Change to Reviewed-',],
            [ 'gvSIGi18n_TranslationHistoryAction_HacerDefinitiva',      'Change to Definitive (locked)-',],
            [ 'gvSIGi18n_TranslationHistoryAction_Invalidar',            'Invalidate-',],
            [ 'gvSIGi18n_TranslationHistoryAction_IntentarTraducirDifferentCounter',  'Collision with other simultaneus translation-',],
            [ 'gvSIGi18n_NoTranslationsHistory',                         'No History-',],
            [ 'gvSIGi18n_controlConfirmations_title',                    'Confirmation options-'],                
            [ 'gvSIGi18n_controlConfirmations_help',                      'You may optionally disable user interface dialog requests to confirm changes of translations or status.-'],
            [ 'gvSIGi18n_BrowseTranslationsFailure_Exception_msg',                         'An exception occurred while retrieving translations.-',],
            [ 'gvSIGi18n_BrowseTranslationsFailure_MakeSureYouAreLoggedOrContactSiteAdministrator_msg',  'Please make sure that you are properly logged as a user authorized for translations access, or contact your site administrator.-',],
            [ 'gvSIGi18n_BrowseTranslationsFailure_Condition_msg',           'Translations retrieval failed with condition:-',],
            [ 'gvSIGi18n_AccessFailedAndPromptYouHavePermission_label',      'Access to the translations catalog failed.\nDo you have permission ?\nIf so, you may want to login first.-',],
            [ 'gvSIGi18n_NoAccessibleLanguages_label',                       'There are no languages available or accessible.-\nDo you have permission ?\nIf so, you may want to login first.-',],
            [ 'gvSIGi18n_LanguageNotAccessible_label',                       'You are not allowed to access the selected language.-\nDo you have permission ?\nIf so, you may want to login first.-',],
            [ 'gvSIGi18n_TranslationsCatalogIsLockedAgainstModifications',   'The Translations Catalog Is Locked Against Modifications-',],
            [ 'gvSIGi18n_SelectedLanguageIsLockedAgainstModifications',      'The Selected Language Is Locked Against Modifications-',],
            [ cResultCondition_NoMatchingTranslationsFound,                  cResultCondition_NoMatchingTranslationsFound,],
            [ 'gvSIGi18n_reviseLasCondicionesDeFiltroYBusqueda_message',     'Please, review the filter and search criteria.-',],
            [ 'gvSIGi18n_catalogo_action_label',                             'Catalog-',],
            [ 'gvSIGi18n_selectorLenguagesReferencia_title',                  'Reference Languages Selector-',],
            [ 'gvSIGi18n_selectorLenguagesReferencia_help',                   'Select the languages you want to use as reference.\nA high number of languages will slow down page loading.-',],
            [ 'gvSIGi18n_limiteNumeroRegistrosExplorados_help',               'The maximum number of translations to explore in a single page is-',],
            [ 'gvSIGi18n_numeroRegistrosDivididoPorNumerolenguages_help',      'divided by the number of reference languages selected plus one-',],
            [ 'gvSIGi18n_todosPlus_action_label',                              '+',],
            [ 'gvSIGi18n_ningunMinus_action_label',                            '-',],
            [ 'gvSIGi18n_refrescar_action_label',                              'Refresh-',],
            [ 'gvSIGi18n_NoConfirmTranslationChanges_label',                   'Do Not Confirm Translation Changes-',],
            [ 'gvSIGi18n_NoConfirmStatusChanges_label',                        'Do Not Confirm Status Changes-',],
            [ 'gvSIGi18n_NoConfirmTranslationDelete_label',                    'Do Not Confirm Translation Delete-',],
            [ 'gvSIGi18n_controlEditorKeys_title',                             'Editor keys behaviour-',],
            [ 'gvSIGi18n_controlEditorKeys_help',                              'Choose the behaviour when pressing the CR and Tab keys in the translations editor text area.-',],
            [ 'gvSIGi18n_EditorKey_CR_label',                                  'Key Enter-',],
            [ 'gvSIGi18n_EditorKey_Tab_label',                                 'Key Tab-',],
            [ 'gvSIGi18n_EditorKeyActions_action_traducirYAvanzar_label',      'Translate and Advance-',],
            [ 'gvSIGi18n_EditorKeyActions_action_traducir_label',              'Translate-',],
            [ 'gvSIGi18n_EditorKeyActions_action_avanzar_label',               'Advance-',],
            [ 'gvSIGi18n_EditorKeyActions_action_nextTabIndex_label',          'Next Tab-',],
            [ 'gvSIGi18n_controlBusinessPresentacion_title',                   'Business sections-',],
            [ 'gvSIGi18n_controlPresentacion_help',                            'Control of presentation options,\nto show or hide page sections relevant to the business.-',],
            [ 'gvSIGi18n_ShowStateTransitionColumns_label',                    'Show columns with Status change Buttons-',],
            [ 'gvSIGi18n_BatchStatusChanges_label',                            'Batch Status changes-',],
            [ 'gvSIGi18n_mostrarSeccionInforme_section_label',                 'Show Summary section-',],
            [ 'gvSIGi18n_mostrarSeccionHistoria_section_label',                'Show translation History section-',],
            [ 'gvSIGi18n_mostrarSeccionLista_section_label',                   'Show List section-',],
            [ 'gvSIGi18n_controlTechnicalPresentacion_title',                  'Technical sections-',],
            [ 'gvSIGi18n_controlTechnicalPresentacion_help',                  'Control to show or hide page sections relevant to the technology.-',],
            [ 'gvSIGi18n_controlTechnicalPresentacion_title',                  'Technical sections-',],
            [ 'gvSIGi18n_TranslationsFilterLink_label',                        'Filter link (for results now shown in the list)-',],
            [ 'gvSIGi18n_TranslationsFilterLink_help',                         'The User may bookmark or save the link as Favorites in the Internet browser,\nor drop the link as a Shortcut on the desktop,\nor just copy the URL, to reproduce the filter later.-',],
            [ 'gvSIGi18n_filtro_section_label',                                'Filter-',],
            [ 'gvSIGi18n_todosEstados_action_label',                           'Any status-',],
            [ 'gvSIGi18n_BusquedasPorPalabrasContenidasEnSimboloOTraduccion_title','Filter by words in the symbol or the translation-',],
            [ 'gvSIGi18n_searchByWords_help',  'Wildcards (* and ?) are permitted, but not at the beginning of words. You may use AND OR NOT between strings or groups of strings. You may group a subcriteria between parenthesis. You may specify exact sentences by surrounding them in double-quotes.-',],
            [ 'gvSIGi18n_TRATraduccion_attr_simbolo_help',                           'The symbol of the string to translate.-',],
            [ 'gvSIGi18n_searchBySimbolo_help',                                      'Enter words to search for in the string symbols. Wildcards (* and ?) are permitted.-',],
            [ 'gvSIGi18n_TRATraduccion_attr_cadenaTraducida_help',                   'The translation of the string into the language.-',],
            [ 'gvSIGi18n_searchByTranslation_help',                                  'Enter words  to search for in the translations into this language. Wildcards (* and ?) are permitted.-',],
            [ 'gvSIGi18n_BusquedasPorEventos_formatoFechaISO_help',                  'Dates in ISO format YYYY-MM-DD HH:MM:SS-',],
            [ 'gvSIGi18n_BusquedasPorEventos_sePermitenFechasParciales_help',        'Incomplete dates and times are allowed--',],
            [ 'gvSIGi18n_BusquedasPorEventos_despuesDeFecha_title',                  'After-',],
            [ 'gvSIGi18n_BusquedasPorEventos_antesDeFecha_title',                    'Before-',],
            [ 'gvSIGi18n_BusquedasPorEventos_title',                                 'Filter by users and dates of status change events-',],
            [ 'gvSIGi18n_BusquedasPorEventos_usuario_title',                         'User-',],
            [ 'gvSIGi18n_BusquedasPorIdCadena_title',                                'Search by exact string symbol id-',],
            [ 'gvSIGi18n_TRACadena_attr_id_help',                                    'Unique identifier for a string, and its translations to any language.-',],
            [ 'gvSIGi18n_searchById_help',                                           'Enter the exact identifier of the string to search for.-',],
            [ 'gvSIGi18n_FiltroCadenasInactivas_title',                              'Show Only Inactive Strings-',],
            [ 'gvSIGi18n_FiltroCadenasInactivas_help',                               'The system shall present only Strings in the Inactive state.-',],
            [ 'gvSIGi18n_seleccionarTodos_label',                                    'All-',],
            [ 'gvSIGi18n_seleccionarNinguno_label',                                  'None-',],
            [ 'gvSIGi18n_modulesFilter_title',                                       'Modules filter-',],
            [ 'gvSIGi18n_modulesFilter_help',                                        'Select the modules with the translations you are interested in.\nIf no module is selected then there is no restriction on translation modules.\nThe --unspecified-- module represents those strings that are not associated with any module.--',],
            [ cNombreModuloNoEspecificadoLabel_MsgId,                                'Unspecified module-'],
            [ 'gvSIGi18n_seccionGoTo_title',                                         'Go To-',],
            [ 'gvSIGi18n_first_label',                                               'First-',],
            [ 'gvSIGi18n_GoToParameters_title',                                      'First symbol to show in the translations list-',],
            [ 'gvSIGi18n_TranslationsPage_GoTo_SymbolIndex_label',                   'Symbol at index #-',],
            [ 'gvSIGi18n_TranslationsPage_GoTo_SymbolIndex_of',                      'of-',],
            [ 'gvSIGi18n_TranslationsPage_GoTo_SymbolIndex_help',                    'The index number of the first symbol to show.-',],
            [ 'gvSIGi18n_TranslationsPage_GoTo_PageIndex_label',                     'Page number #-',],
            [ 'gvSIGi18n_TranslationsPage_GoTo_PageIndex_of',                      'of-',],
            [ 'gvSIGi18n_TranslationsPage_GoTo_PageIndex_help',                    'The index number of the page to show.-',],
            [ 'gvSIGi18n_TranslationsPage_GoTo_SymbolStartingWithChars_label',     'Symbol beginning with-',],
            [ 'gvSIGi18n_TranslationsPage_GoTo_SymbolStartingWithChars_help',      'Beginning letters of the first symbol to show in the translations list.-',],
            [ 'gvSIGi18n_informe_section_label',                                   'Summary-',],
            [ 'gvSIGi18n_total_label',                                             'Total-',],
            [ 'gvSIGi18n_Modulos_title',                                           'Modules-',],
            [ 'gvSIGi18n_seccionHistory_title',                                    'History-',],
        
        ]],
    ]
               

    someDomainsStringsAndDefaultsToTranslate.append( 
        [ 'gvSIGi18n', 
            [[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_%s' % unEstado,  unEstado] for unEstado in cTodosEstados]
        ]
    )        
    
    aTRAgvSIGi18n_tool.fTranslateI18NManyIntoDict(
        theContextualElement             =unContextualObject,
        theI18NDomainsStringsAndDefaults =someDomainsStringsAndDefaultsToTranslate, 
        theResultDict                    =aTranslationsCache,
        theTranslationService            =aTranslationService,
        )
    
    for aTranslationKey in aTranslationsCache.keys():
        
        aTranslation = aTranslationsCache.get( aTranslationKey, u'')
        anEncodedTranslation = fCGIE( aTranslation)
        aTranslationsCache[ aTranslationKey] = anEncodedTranslation
        
    return None













# #################################
"""Rendering methods.

"""
  

    
def _pRenderCollapsible_Lambda( 
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




def _pEmptyPageContents( 
    unContextualObject      =None,
    unHeader                =None,
    unMessage               =None,
    aPortalURL              =None,
    aCatalogoURL            =None,
    fCGIE                   =None,
    mfCRs2BRs               =None,
    mfTranslateI18N         =None,
    mfAsUnicode             =None,
    aTranslationsCache      =None,    ):
    """Render an empty translations browser.
        
    """
    
    anOutput = StringIO()
    
    _pRenderEmpty( 
        anOutput           =anOutput,                              
        unContextualObject =unContextualObject,                                             
        unHeader           =unHeader,                                                       
        unMessage          =unMessage,                                                      
        aPortalURL         =aPortalURL,                                                     
        aCatalogoURL       =aCatalogoURL,                                                   
        fCGIE              =fCGIE,                                                          
        mfCRs2BRs          =mfCRs2BRs,                                                      
        mfTranslateI18N    =mfTranslateI18N,                                                
        mfAsUnicode        =mfAsUnicode,                                                    
        aTranslationsCache =aTranslationsCache,                                              
    )
    
    return anOutput.getvalue()










def _pRenderEmpty( 
    anOutput           =None,             
    unContextualObject =None,                       
    unHeader           =None,             
    unMessage          =None,             
    aPortalURL         =None,              
    aCatalogoURL       =None,                
    fCGIE              =None,         
    mfCRs2BRs          =None,             
    mfTranslateI18N    =None,                   
    mfAsUnicode        =None,               
    aTranslationsCache =None, ):
    """Produce the content of an empty translations browser.
        
    """
    
    
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
        


      
def _pRenderStyles( anOutput, theContextualObject):
     
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









def _pRenderScripts( 
    anOutput, 
    unContextualObject,):
    """Render the scripts assisting in controling the translations browser form in the client internet browser.
        
    """

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














def _pRenderCabecera( 
    anOutput                =None,
    unContextualObject      =None,
    theBrowseResult         =None,
    pLanguagesNamesAndFlags =None,
    pTodosCodigosIdiomas    =None,
    pCodigoIdiomaCursor     =None,
    aPortalURL              =None,
    aCatalogoURL            =None,
    fCGIE                   =None,
    mfCRs2BRs               =None,
    mfTranslateI18N         =None,
    mfAsUnicode             =None,
    aTranslationsCache      =None, ):
    """Render the header of the  translations browser.
    
    """    
    
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
                <img src="%(pCatalogoAbsoluteURL)s/tra_root.gif" alt="%(gvSIGi18n_catalogo_action_label)s" title="%(gvSIGi18n_catalogo_action_label)s" id="icon-contenedor" />                                        
            </a>
        </td>
        <td align="right" valign="center" >
        \n""" % { 
    'pCatalogoAbsoluteURL':                 aCatalogoURL, 
    'gvSIGi18n_catalogo_action_label':      aTranslationsCache[ 'gvSIGi18n_catalogo_action_label'],  
    })
    
    
    
    _pRenderSelectorIdiomaPrincipal( 
        anOutput, 
        unContextualObject, 
        pLanguagesNamesAndFlags, 
        pTodosCodigosIdiomas, 
        pCodigoIdiomaCursor, 
        fCGIE,
        mfCRs2BRs,
        mfTranslateI18N,
        mfAsUnicode,
        aTranslationsCache,
    )
                   
    anOutput.write( u"""
        </td>
        <td align="right" valign="center" >
        \n"""
    )
   
    
    _pRenderCursorButtons( 
        anOutput, 
        unContextualObject, 
        9, 
        aPortalURL,
        aCatalogoURL,
        fCGIE,
        mfCRs2BRs,
        mfTranslateI18N,
        mfAsUnicode,
        aTranslationsCache)
         
    anOutput.write( u"""
                    </td>
                </tr>
            </tbody>
        </table>
        \n""" %  {
                          
    })   
 
        
    return None
        







def _pRenderSelectorIdiomaPrincipal( 
    anOutput, 
    unContextualObject, 
    pLanguagesNamesAndFlags, 
    pTodosCodigosIdiomas, 
    pCodigoIdiomaCursor, 
    fCGIE,
    mfCRs2BRs,
    mfTranslateI18N,
    mfAsUnicode,
    aTranslationsCache):
    """Render the selector of the main language in the translations browser.
    
    """    
            
    anOutput.write( u"""  
       <!-- #################################################################
        SECTION: Selector de Idioma principal 
        ################################################################# -->
           <select  style="font-size: 9pt;" name="theCodigoIdiomaCursor" id="theCodigoIdiomaCursor" onchange="document.getElementById( 'TranslationFormId').submit(); return true;">
           \n""" 
    )

                
    for unCodigoIdioma in pTodosCodigosIdiomas:
        anOutput.write( u"""         
            <option id="%(codigo-idioma)s_id" %(selected-selected)s value="%(codigo-idioma)s">
                %(codigo-idioma)s %(nombre-idioma)s %(nombre-nativo-idioma)s
            </option>
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









    
def _pRenderCollapsibleSelectorIdiomasReferencia( 
    anOutput                               =None,
    unContextualObject                     =None,
    pLanguagesNamesAndFlags                =None,
    pTodosCodigosIdiomasEInternacionales   =None,
    pIdiomasReferencia                     =None,
    unaConfiguracionPaginaTraduccionesDict =None,
    aPortalURL                             =None,
    aCatalogoURL                           =None,
    fCGIE                                  =None,
    mfCRs2BRs                              =None,
    mfTranslateI18N                        =None,
    mfAsUnicode                            =None,
    aTranslationsCache                     =None, ):
    """Render as collapsible the section to select the reference languages to display for each translation in the translations browser.
    
    """    
            
    _pRenderCollapsible_Lambda(  anOutput,
        aTranslationsCache[ 'gvSIGi18n_idiomasSection_title'],
        u'elid_SelectorIdiomasReferencia_collapsible_dl', 
        lambda : _pRenderSelectorIdiomasReferencia( 
            anOutput, 
            unContextualObject, 
            pLanguagesNamesAndFlags, 
            pTodosCodigosIdiomasEInternacionales, 
            pIdiomasReferencia,
            unaConfiguracionPaginaTraduccionesDict,
            aPortalURL,
            aCatalogoURL,
            fCGIE,
            mfCRs2BRs,
            mfTranslateI18N,
            mfAsUnicode,
            aTranslationsCache
        )
    )
    
    return None        







def _pRenderSelectorIdiomasReferencia( 
    anOutput, 
    unContextualObject, 
    pLanguagesNamesAndFlags, 
    pTodosCodigosIdiomasEInternacionales, 
    pIdiomasReferencia,
    unaConfiguracionPaginaTraduccionesDict,
    aPortalURL,
    aCatalogoURL,
    fCGIE,
    mfCRs2BRs,
    mfTranslateI18N,
    mfAsUnicode,
    aTranslationsCache):
    """Render  the section to select the reference languages to display for each translation in the translations browser.
    
    """    

    unDisplayContryFlags = unContextualObject.fDisplayCountryFlags()
    
    unMaximoRegistrosExplorados = cMaximoRegistrosExplorados
    if not ( unaConfiguracionPaginaTraduccionesDict == None):
        unMaximoRegistrosExplorados = unaConfiguracionPaginaTraduccionesDict.get( 'maximoRegistrosExplorados', cMaximoRegistrosExplorados)
            
    
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
        'colspan_head':                                               ( unDisplayContryFlags and 6) or 5,
        'colspan_labels':                                             ( unDisplayContryFlags and 5) or 4,
        'gvSIGi18n_selectorLenguagesReferencia_title':                 aTranslationsCache[ 'gvSIGi18n_selectorLenguagesReferencia_title'],
        'gvSIGi18n_limiteNumeroRegistrosExplorados_help':              aTranslationsCache[ 'gvSIGi18n_limiteNumeroRegistrosExplorados_help'],
        'max-numero-registros-explorados':                             unMaximoRegistrosExplorados,
        'gvSIGi18n_numeroRegistrosDivididoPorNumerolenguages_help':    aTranslationsCache[  'gvSIGi18n_numeroRegistrosDivididoPorNumerolenguages_help'],
        'gvSIGi18n_selectorLenguagesReferencia_help':                  mfCRs2BRs( aTranslationsCache[  'gvSIGi18n_selectorLenguagesReferencia_help']),
        'gvSIGi18n_todosPlus_action_label':                            aTranslationsCache[ 'gvSIGi18n_todosPlus_action_label'],
        'gvSIGi18n_ningunMinus_action_label':                          aTranslationsCache[  'gvSIGi18n_ningunMinus_action_label'],
        'gvSIGi18n_refrescar_action_label':                            aTranslationsCache[  'gvSIGi18n_refrescar_action_label'],
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
                        <img width="14" height="11" alt="Flag_%(nombre-idioma)s" src="%(flag-url)s" title="Flag_%(nombre-idioma)s" />
                    </td>
                \n""" % { 
                'index-idioma':         str( unIndexRowIdiomaReferencia),
                'codigo-idioma':        mfAsUnicode( unCodigoIdiomaEnGvSIG),
                'nombre-idioma':        mfAsUnicode( pLanguagesNamesAndFlags.get( unCodigoIdiomaEnGvSIG, {}).get( 'english', '')),        
                'flag-url':            pLanguagesNamesAndFlags.get( unCodigoIdiomaEnGvSIG, {}).get( 'flag_url', '%s/%s' % ( aPortalURL, cTRAFlagIdiomaDesconocida,)), 
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
        'gvSIGi18n_refrescar_action_label':             aTranslationsCache[ 'gvSIGi18n_refrescar_action_label'],                
    })

    return None
                
  









    






def _pRenderCollapsibleControlPresentacion( 
    anOutput                               =None,
    unContextualObject                     =None,
    pTraduccionesPorPagina                 =None,
    pInteractionMode                       =None,
    pMostrarInforme                        =None,
    pMostrarLista                          =None,
    pMostrarDetallesTraduccion             =None,
    pMostrarHistoria                       =None,
    pShowStateTransitionColumnsOption      =None,
    pShowStateTransitionColumns            =None,
    pShowBatchStatusChangesOption          =None,
    pBatchStatusChanges                    =None,
    pNoConfirmTranslationChanges           =None,
    pNoConfirmStatusChanges                =None,
    pNoConfirmTranslationDelete            =None,
    pCanComment                            =None,
    pEditorKeyCRAction                     =None,
    pEditorKeyTabAction                    =None,
    pRenderFormSubmit                      =None,
    pRenderRequest                         =None,
    pRenderFullRequest                     =None,
    pRenderTimes                           =None,
    pRenderProfile                         =None,
    pRenderAsyncRequest                    =None,
    pRenderUserInterfaceEvents             =None,
    unaConfiguracionPaginaTraduccionesDict =None,
    aPortalURL                             =None,
    aCatalogoURL                           =None,
    fCGIE                                  =None,
    mfCRs2BRs                              =None,
    mfTranslateI18N                        =None,
    mfAsUnicode                            =None,
    aTranslationsCache                     =None, ):
    """Render as collapsible the control to select presentation sections to include in the translations browser.
    
    """    
            
    _pRenderCollapsible_Lambda(  anOutput,
        aTranslationsCache[ 'gvSIGi18n_opcionesSection_title'],
        u'elid_ControlPresentacion_collapsible_dl', 
        lambda : _pRenderControlPresentacion( 
            anOutput                               =anOutput,
            unContextualObject                     =unContextualObject,
            pTraduccionesPorPagina                 =pTraduccionesPorPagina,
            pInteractionMode                       =pInteractionMode,
            pMostrarInforme                        =pMostrarInforme,
            pMostrarLista                          =pMostrarLista,
            pMostrarDetallesTraduccion             =pMostrarDetallesTraduccion,
            pMostrarHistoria                       =pMostrarHistoria,
            pShowStateTransitionColumnsOption      =pShowStateTransitionColumnsOption,
            pShowStateTransitionColumns            =pShowStateTransitionColumns,
            pShowBatchStatusChangesOption          =pShowBatchStatusChangesOption,
            pBatchStatusChanges                    =pBatchStatusChanges,
            pNoConfirmTranslationChanges           =pNoConfirmTranslationChanges,
            pNoConfirmStatusChanges                =pNoConfirmStatusChanges,
            pNoConfirmTranslationDelete            =pNoConfirmTranslationDelete,
            pCanComment                            =pCanComment,
            pEditorKeyCRAction                     =pEditorKeyCRAction,
            pEditorKeyTabAction                    =pEditorKeyTabAction,
            pRenderFormSubmit                      =pRenderFormSubmit,
            pRenderRequest                         =pRenderRequest,
            pRenderFullRequest                     =pRenderFullRequest,
            pRenderTimes                           =pRenderTimes,
            pRenderProfile                         =pRenderProfile,
            pRenderAsyncRequest                    =pRenderAsyncRequest,
            pRenderUserInterfaceEvents             =pRenderUserInterfaceEvents,
            unaConfiguracionPaginaTraduccionesDict =unaConfiguracionPaginaTraduccionesDict,
            aPortalURL                             =aPortalURL,
            aCatalogoURL                           =aCatalogoURL,
            fCGIE                                  =fCGIE,
            mfCRs2BRs                              =mfCRs2BRs,
            mfTranslateI18N                        =mfTranslateI18N,
            mfAsUnicode                            =mfAsUnicode,
            aTranslationsCache                     =aTranslationsCache,
        )
    )
    
    return None        




def _pRenderControlPresentacion( 
    anOutput                               =None,
    unContextualObject                     =None,
    pTraduccionesPorPagina                 =None,
    pInteractionMode                       =None,
    pMostrarInforme                        =None,
    pMostrarLista                          =None,
    pMostrarDetallesTraduccion             =None,
    pMostrarHistoria                       =None,
    pShowStateTransitionColumnsOption      =None,
    pShowStateTransitionColumns            =None,
    pShowBatchStatusChangesOption          =None,
    pBatchStatusChanges                    =None,
    pNoConfirmTranslationChanges           =None,
    pNoConfirmStatusChanges                =None,
    pNoConfirmTranslationDelete            =None,
    pCanComment                            =None,
    pEditorKeyCRAction                     =None,
    pEditorKeyTabAction                    =None,
    pRenderFormSubmit                      =None,
    pRenderRequest                         =None,
    pRenderFullRequest                     =None,
    pRenderTimes                           =None,
    pRenderProfile                         =None,
    pRenderAsyncRequest                    =None,
    pRenderUserInterfaceEvents             =None,
    unaConfiguracionPaginaTraduccionesDict =None,
    aPortalURL                             =None,
    aCatalogoURL                           =None,
    fCGIE                                  =None,
    mfCRs2BRs                              =None,
    mfTranslateI18N                        =None,
    mfAsUnicode                            =None,
    aTranslationsCache                     =None,):
    """Render the control to select presentation sections to include in the translations browser.
    
    """    
    
    anOutput.write( u"""  
        
        <!-- #################################################################
        SECTION: Presentation options control 
        ################################################################# -->   

        <!-- #################################################################
        SUBSECTION: Presentation options control without need to refresh  
        ################################################################# -->   
        
        <br/>
        <h2>%(gvSIGi18n_PresentationOptions_NoNeedToRefresh_label)s</h2>
        <br/>
        \n"""% {
        'gvSIGi18n_PresentationOptions_NoNeedToRefresh_label':  aTranslationsCache[ 'gvSIGi18n_PresentationOptions_NoNeedToRefresh_label'],                
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
        <span class="formHelp" ><font size="1">%(gvSIGi18n_AppliesOnSelectonForEditionNoNeedToRefresh_help)s</font></span>
        <br/>
        <br/>        
        
        \n"""% {
        'is-checked':                                  (( pMostrarDetallesTraduccion) and 'checked="checked"') or '',
        'gvSIGi18n_ShowEditorDetails_label':           aTranslationsCache[ 'gvSIGi18n_ShowEditorDetails_label'],  
        'gvSIGi18n_AppliesOnSelectonForEditionNoNeedToRefresh_help': aTranslationsCache[ 'gvSIGi18n_AppliesOnSelectonForEditionNoNeedToRefresh_help'],
    })

    
    

        
    pConfigParmsIndex = 0
    
    anOutput.write( u"""  
        <!-- ########################
        SubSection: Confirmation options
        #############################-->
        
        <table id="sct_PresentationOptions_ConfirmationOptions_control" class="listing nosort" summary="Control for Confirmations behaviour" >
            <thead>
                <tr>
                    <th align="left" colspan="2" >
                        <font size="2">                    
                            <strong>
                                %(gvSIGi18n_controlConfirmations_title)s
                            </strong>
                        </font>
                        <p class="formHelp">
                            %(gvSIGi18n_controlConfirmations_help)s
                            <br/>
                            %(gvSIGi18n_AppliesImmediatelyNoNeedToRefresh_help)s
                        </p>
                    </th>
                </tr>
             </head>
            <tbody>   
        \n""" % {
        'gvSIGi18n_controlConfirmations_title':      aTranslationsCache[ 'gvSIGi18n_controlConfirmations_title'],                
        'gvSIGi18n_controlConfirmations_help':       aTranslationsCache[ 'gvSIGi18n_controlConfirmations_help'],
        'gvSIGi18n_AppliesImmediatelyNoNeedToRefresh_help':     aTranslationsCache[ 'gvSIGi18n_AppliesImmediatelyNoNeedToRefresh_help'],                
    })
        
 
        
    anOutput.write( u"""  
       <tr class="%(row-class)s" >
           <td align="left"  valign="center" onclick="pTRApTRAToggleSeccionPresentacion( 'theNoConfirmTranslationChanges'); return true;" class="TRAstyle_Clickable"  >                
               <font size="1" >
                   <strong>
                       %(gvSIGi18n_NoConfirmTranslationChanges_label)s
                   </strong>
               </font>
           </td>
           <td align="center" valign="center" >                
               <input type="checkbox" class="noborder"  value="on"  %(is-checked)s 
                name="theNoConfirmTranslationChanges" id="theNoConfirmTranslationChanges" 
                onmouseup="fTRAEvtHlr_NoConfirmTranslationChanges_OnMouseUp()"/>
           </td>
        </tr>
        \n""" % { 
        'row-class':    cClasesFilas[ pConfigParmsIndex % 2],
        'gvSIGi18n_NoConfirmTranslationChanges_label': aTranslationsCache[ 'gvSIGi18n_NoConfirmTranslationChanges_label'],
        'is-checked': (( pNoConfirmTranslationChanges) and 'checked="checked"') or '',
    })
    pConfigParmsIndex += 1
                
            
    anOutput.write( u"""  
       <tr class="%(row-class)s"  >
           <td align="left"  valign="center" onclick="pTRApTRAToggleSeccionPresentacion( 'theNoConfirmStatusChanges'); return true;" class="TRAstyle_Clickable"  >                
               <font size="1" >
                   <strong>
                       %(gvSIGi18n_NoConfirmStatusChanges_label)s
                   </strong>
               </font>
           </td>
           <td align="center" valign="center" >                
               <input type="checkbox" class="noborder"  value="on"  %(is-checked)s 
                name="theNoConfirmStatusChanges" id="theNoConfirmStatusChanges" 
                onmouseup="fTRAEvtHlr_NoConfirmStatusChanges_OnMouseUp()"/>
           </td>
       </tr>
       \n""" % { 
        'row-class':    cClasesFilas[ pConfigParmsIndex % 2],
        'gvSIGi18n_NoConfirmStatusChanges_label': aTranslationsCache[ 'gvSIGi18n_NoConfirmStatusChanges_label'], 
        'is-checked': (( pNoConfirmStatusChanges) and 'checked="checked"') or '',
    })
    pConfigParmsIndex += 1
           
            
    anOutput.write( u"""  
       <tr class="%(row-class)s"  >
           <td align="left"  valign="center" onclick="pTRApTRAToggleSeccionPresentacion( 'theNoConfirmTranslationDelete'); return true;" class="TRAstyle_Clickable"  >                
               <font size="1" >
                   <strong>
                       %(gvSIGi18n_NoConfirmTranslationDelete_label)s
                   </strong>
               </font>
           </td>
           <td align="center" valign="center" >                
               <input type="checkbox" class="noborder"  value="on"  %(is-checked)s 
                name="theNoConfirmTranslationDelete" id="theNoConfirmTranslationDelete" 
                onmouseup="fTRAEvtHlr_NoConfirmTranslationDelete_OnMouseUp()"/>
           </td>
       </tr>
       \n""" % { 
        'row-class':    cClasesFilas[ pConfigParmsIndex % 2],
        'gvSIGi18n_NoConfirmTranslationDelete_label': aTranslationsCache[ 'gvSIGi18n_NoConfirmTranslationDelete_label'], 
        'is-checked': (( pNoConfirmTranslationDelete) and 'checked="checked"') or '',
    })
    pConfigParmsIndex += 1
             
    anOutput.write( u"""  
            </tboby>
        </table>
        <br/>
        <br/>
    """)
        
         
    
    
    anOutput.write( u"""  
        <!-- ########################
        SubSection: Editor keys options
        #############################-->
        
        <table id="sct_PresentationOptions_EditorKeysBehavior_control" class="listing nosort" summary="Control for Editor keys behaviour" >
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
            </tbody>
        </table>
        <br/>
        <br/>
        \n""" % {
        'gvSIGi18n_controlEditorKeys_title':      aTranslationsCache[ 'gvSIGi18n_controlEditorKeys_title'],                
        'gvSIGi18n_controlEditorKeys_help':       aTranslationsCache[ 'gvSIGi18n_controlEditorKeys_help'],
        'gvSIGi18n_AppliesImmediatelyNoNeedToRefresh_help':     aTranslationsCache[ 'gvSIGi18n_AppliesImmediatelyNoNeedToRefresh_help'],                
        'gvSIGi18n_EditorKey_CR_label':           aTranslationsCache[ 'gvSIGi18n_EditorKey_CR_label'],
        'gvSIGi18n_EditorKey_Tab_label':          aTranslationsCache[ 'gvSIGi18n_EditorKey_Tab_label'],
        'is-selected-Tab_action_traducirYAvanzar':       (( pEditorKeyTabAction == 'action_traducirYAvanzar' ) and 'selected="selected"') or '',
        'is-selected-Tab_action_traducir':               (( pEditorKeyTabAction == 'action_traducir' )       and 'selected="selected"') or '',
        'is-selected-Tab_action_avanzar':                (( pEditorKeyTabAction == 'action_avanzar' )        and 'selected="selected"') or '',
        'is-selected-Tab_action_nextTabIndex':           (( pEditorKeyTabAction == 'action_nextTabIndex' )   and 'selected="selected"') or '',
        'action_traducirYAvanzar_label':                 aTranslationsCache[ 'gvSIGi18n_EditorKeyActions_action_traducirYAvanzar_label'],
        'action_traducir_label':                         aTranslationsCache[ 'gvSIGi18n_EditorKeyActions_action_traducir_label'],
        'action_avanzar_label':                          aTranslationsCache[ 'gvSIGi18n_EditorKeyActions_action_avanzar_label'],
        'action_nextTabIndex_label':                     aTranslationsCache[ 'gvSIGi18n_EditorKeyActions_action_nextTabIndex_label'],
        'is-selected-CR_action_traducirYAvanzar':        (( pEditorKeyCRAction == 'action_traducirYAvanzar' ) and 'selected="selected"') or '',
        'is-selected-CR_action_traducir':                (( pEditorKeyCRAction == 'action_traducir' )       and 'selected="selected"') or '',
        'is-selected-CR_action_avanzar':                 (( pEditorKeyCRAction == 'action_avanzar' )        and 'selected="selected"') or '',
        'is-selected-CR_action_nextTabIndex':            (( pEditorKeyCRAction == 'action_nextCRIndex' )   and 'selected="selected"') or '',
    })
        
    

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
        SUBSECTION: Presentation options control that need to refresh
        ################################################################# -->   
        <br/>
        <h2>%(gvSIGi18n_PresentationOptions_MustRefresh_label)s</h2>
        <br/>

        
        <!-- #################################################################
        Subsection: Refresh button
        ################################################################# -->   
        
        <input name="form_submit" style="font-size: 10pt; font-style: italic"  value="%(gvSIGi18n_refrescar_action_label)s" type="submit"/>
        <br/>
        \n"""% {
        'gvSIGi18n_refrescar_action_label':                     aTranslationsCache[ 'gvSIGi18n_refrescar_action_label'],                
        'gvSIGi18n_PresentationOptions_MustRefresh_label':      aTranslationsCache[ 'gvSIGi18n_PresentationOptions_MustRefresh_label'],                
      })
    
    
    unMaximoRegistrosExplorados = cMaximoRegistrosExplorados
    if not ( unaConfiguracionPaginaTraduccionesDict == None):
        unMaximoRegistrosExplorados = unaConfiguracionPaginaTraduccionesDict.get( 'maximoRegistrosExplorados', cMaximoRegistrosExplorados)
        
        
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
        'gvSIGi18n_limiteNumeroRegistrosExplorados_help':           aTranslationsCache[ 'gvSIGi18n_limiteNumeroRegistrosExplorados_help'],
        'max-numero-registros-explorados':                          unMaximoRegistrosExplorados,
        'gvSIGi18n_numeroRegistrosDivididoPorNumerolenguages_help': aTranslationsCache[ 'gvSIGi18n_numeroRegistrosDivididoPorNumerolenguages_help'],
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
        'gvSIGi18n_controlBusinessPresentacion_title':  aTranslationsCache[ 'gvSIGi18n_controlBusinessPresentacion_title'],             
        'gvSIGi18n_controlPresentacion_help':           aTranslationsCache[ 'gvSIGi18n_controlPresentacion_help'],
    })
    
     
     
    pConfigParmsIndex = 0
     
     
    if pShowStateTransitionColumnsOption:
        anOutput.write( u"""  
            <tr class="%(row-class)s" >
                <td align="left"  valign="center" onclick="pTRApTRAToggleSeccionPresentacion( 'theShowStateTransitionColumns'); return true;" class="TRAstyle_Clickable"  >                
                    <font size="1" >
                        <strong>
                            %(gvSIGi18n_ShowStateTransitionColumns_label)s
                        </strong>
                    </font>
                </td>
                <td align="center" valign="center" >                
                    <input type="checkbox" class="noborder"  value="on"  %(is-checked)s name="theShowStateTransitionColumns" id="theShowStateTransitionColumns" />
                </td>
            </tr>
            \n""" % { 
            'row-class':    cClasesFilas[ pConfigParmsIndex % 2],
            'gvSIGi18n_ShowStateTransitionColumns_label': aTranslationsCache[ 'gvSIGi18n_ShowStateTransitionColumns_label'],
            'is-checked': (( pShowStateTransitionColumns) and 'checked="checked"') or '',
        })
        pConfigParmsIndex += 1
        
        
    if pShowBatchStatusChangesOption:
        anOutput.write( u"""  
           <tr class="%(row-class)s" >
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
            'row-class':    cClasesFilas[ pConfigParmsIndex % 2],
            'gvSIGi18n_BatchStatusChanges_label': aTranslationsCache[ 'gvSIGi18n_BatchStatusChanges_label'], 
            'is-checked': (( pBatchStatusChanges) and 'checked="checked"') or '',
        })
        pConfigParmsIndex += 1
    
        
    anOutput.write( u"""  
       <tr class="%(row-class)s" >
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
        'row-class':    cClasesFilas[ pConfigParmsIndex % 2],
        'gvSIGi18n_mostrarSeccionInforme_section_label': aTranslationsCache[ 'gvSIGi18n_mostrarSeccionInforme_section_label'], 
        'is-checked': (( pMostrarInforme) and 'checked="checked"') or '',
    })
    pConfigParmsIndex += 1
    

  
   
    anOutput.write( u"""  
       <tr class="%(row-class)s" >
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
        'row-class':    cClasesFilas[ pConfigParmsIndex % 2],
        'gvSIGi18n_mostrarSeccionHistoria_section_label': aTranslationsCache[ 'gvSIGi18n_mostrarSeccionHistoria_section_label'],
        'is-checked': (( pMostrarHistoria) and 'checked="checked"') or '',
    })
    pConfigParmsIndex += 1
    
    
    anOutput.write( u"""  
        <tr class="%(row-class)s" >
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
        'row-class':    cClasesFilas[ pConfigParmsIndex % 2],
        'gvSIGi18n_mostrarSeccionLista_section_label': aTranslationsCache[ 'gvSIGi18n_mostrarSeccionLista_section_label'],
        'is-checked': (( pMostrarLista) and 'checked="checked"') or '',
    })
    pConfigParmsIndex += 1

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
        'gvSIGi18n_refrescar_action_label':             aTranslationsCache[ 'gvSIGi18n_refrescar_action_label'],             
        'gvSIGi18n_controlTechnicalPresentacion_title': aTranslationsCache[ 'gvSIGi18n_controlTechnicalPresentacion_title'],
        'gvSIGi18n_controlTechnicalPresentacion_help':  aTranslationsCache[ 'gvSIGi18n_controlTechnicalPresentacion_help'],
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
        'gvSIGi18n_refrescar_action_label':             aTranslationsCache[ 'gvSIGi18n_refrescar_action_label'],                
    })
    
         
    return None
    
     

    
















    
def _pRenderCollapsibleFiltro( 
    anOutput              =None,
    unContextualObject    =None,
    pCodigoIdiomaCursor   =None,
    pTodosNombresModulos  =None,
    pEstadosIncluidos     =None,
    pSearchParameters     =None,
    aPortalURL            =None,
    aCatalogoURL          =None,
    fCGIE                 =None,
    mfCRs2BRs             =None,
    mfTranslateI18N       =None,
    mfAsUnicode           =None,
    aTranslationsCache    =None, ):
    """Render as collapsible the filter section of the translations browser.
    
    """    

    _pRenderCollapsible_Lambda(  anOutput,
        aTranslationsCache[ 'gvSIGi18n_seccionFiltro_title'],
        u'elid_Filter_collapsible_dl', 
        lambda : _pRenderFiltro( 
            anOutput              =anOutput,                
            unContextualObject    =unContextualObject,                          
            pCodigoIdiomaCursor   =pCodigoIdiomaCursor,                          
            pTodosNombresModulos  =pTodosNombresModulos,                            
            pEstadosIncluidos     =pEstadosIncluidos,                         
            pSearchParameters     =pSearchParameters,                         
            aPortalURL            =aPortalURL,                 
            aCatalogoURL          =aCatalogoURL,                   
            fCGIE                 =fCGIE,            
            mfCRs2BRs             =mfCRs2BRs,                
            mfTranslateI18N       =mfTranslateI18N,                      
            mfAsUnicode           =mfAsUnicode,                  
            aTranslationsCache    =aTranslationsCache,        
        ),
    )
    
    return None        






def _fRenderApplyOrCancelFiltro( 
    anOutput, 
    unContextualObject, 
    unTabIndex, 
    aPortalURL,
    aCatalogoURL,
    fCGIE,
    mfCRs2BRs,
    mfTranslateI18N,
    mfAsUnicode,
    aTranslationsCache):
    """Render a section with buttons to apply or cancel the filter.
    
    """    
    
    anOutput.write( u"""    
    
        <!-- #################################################################
        SECTION: Aplicar o Cancelar Filtro para busqueda de TRATraduccion
        ################################################################# -->
                
        <input tabindex=%(tabindex)d name="form_submit" style="font-size: 10pt; font-style: italic"  value="%(gvSIGi18n_refrescar_action_label)s" type="submit"/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <input tabindex=%(tabindex2)d type="button" name="todos" style="font-size: 9pt; "  value="%(gvSIGi18n_todas_label)s" onclick="pTRAResetFiltros(); return true;" class="TRAstyle_Clickable"  />
        <br/>
        \n""" % { 
        'tabindex':                                            unTabIndex,
        'tabindex2':                                           unTabIndex + 1,
        'gvSIGi18n_refrescar_action_label':                    aTranslationsCache[ 'gvSIGi18n_refrescar_action_label'],
        'gvSIGi18n_todas_label':                               aTranslationsCache[ 'gvSIGi18n_todas_label'],
    })
    
    return unTabIndex + 2






def _pRenderFiltro( 
    anOutput              =None,
    unContextualObject    =None,
    pCodigoIdiomaCursor   =None,
    pTodosNombresModulos  =None,
    pEstadosIncluidos     =None,
    pSearchParameters     =None,
    aPortalURL            =None,
    aCatalogoURL          =None,
    fCGIE                 =None,
    mfCRs2BRs             =None,
    mfTranslateI18N       =None,
    mfAsUnicode           =None,
    aTranslationsCache    =None, ):
    """Render the filter section of the translations browser.
    
    """    
 
    unTabIndex = 11
    
    anOutput.write( u"""    
    
        <!-- #################################################################
        SECTION: Ayuda acerca del uso del Filtro para busqueda de TRATraduccion
        ################################################################# -->
                
        <p class="formHelp">
            <span >%(gvSIGi18n_TranslationsFilter_help)s</span>
            <br/>
            <span >%(gvSIGi18n_TranslationsFilter_Reset_help)s</span>
        </p>
        \n""" % { 
        'gvSIGi18n_TranslationsFilter_help':                   mfCRs2BRs( aTranslationsCache[ 'gvSIGi18n_TranslationsFilter_help']),
        'gvSIGi18n_TranslationsFilter_Reset_help':             mfCRs2BRs( aTranslationsCache[ 'gvSIGi18n_TranslationsFilter_Reset_help']),                
    })
    
    unTabIndex = _fRenderApplyOrCancelFiltro( 
        anOutput, 
        unContextualObject, 
        unTabIndex, 
        aPortalURL,
        aCatalogoURL,
        fCGIE,
        mfCRs2BRs,
        mfTranslateI18N,
        mfAsUnicode,
        aTranslationsCache,
    )

    
    anOutput.write( u"""    

        <!-- #################################################################
        Subsection: Enlace para reproducir acceso con filtro 
        ################################################################# -->
        """
    )
                    
                    
    unParametrosFiltroStream = StringIO( u'')
    
    unHayParametrosFiltro = False
    for unEstadoTraduccion in cTodosEstados:
        if unEstadoTraduccion in pEstadosIncluidos:
            if unHayParametrosFiltro:
                unParametrosFiltroStream.write( '&')
            unHayParametrosFiltro = True    
            unParametrosFiltroStream.write( u"""theEstadosAIncluir=%s""" % fCGIE( unEstadoTraduccion))
                    
        
    if pSearchParameters.get( 'simbolo', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchSimbolo=%s""" % fCGIE( mfAsUnicode( pSearchParameters[ 'simbolo'])))
        unHayParametrosFiltro = True    
        
    if pSearchParameters.get( 'cadenaTraducida', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchCadenaTraducida=%s""" % fCGIE( mfAsUnicode( pSearchParameters[ 'cadenaTraducida'])))
        unHayParametrosFiltro = True    
        
    if pSearchParameters.get( 'usuarioCreador', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchUsuarioCreador=%s""" % fCGIE( mfAsUnicode( pSearchParameters[ 'usuarioCreador'])))
        unHayParametrosFiltro = True    
        
    if pSearchParameters.get( 'fechaCreacionInicial', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchFechaCreacionInicial=%s""" % fCGIE( mfAsUnicode( pSearchParameters[ 'fechaCreacionInicial'])))
        unHayParametrosFiltro = True    
        
    if pSearchParameters.get( 'fechaCreacionFinal', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchFechaCreacionFinal=%s""" % fCGIE( mfAsUnicode( pSearchParameters[ 'fechaCreacionFinal'])))
        unHayParametrosFiltro = True    
        
        
    if pSearchParameters.get( 'usuarioTraductor', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchUsuarioTraductor=%s""" % fCGIE( mfAsUnicode( pSearchParameters[ 'usuarioTraductor'])))
        unHayParametrosFiltro = True    
        
    if pSearchParameters.get( 'fechaTraduccionInicial', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchFechaTraduccionInicial=%s""" % fCGIE( mfAsUnicode( pSearchParameters[ 'fechaTraduccionInicial'])))
        
    if pSearchParameters.get( 'fechaTraduccionFinal', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchFechaTraduccionFinal=%s""" % fCGIE( mfAsUnicode( pSearchParameters[ 'fechaTraduccionFinal'])))
        unHayParametrosFiltro = True    

        
    if pSearchParameters.get( 'usuarioRevisor', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchUsuarioRevisor=%s""" % fCGIE( mfAsUnicode( pSearchParameters[ 'usuarioRevisor'])))
        unHayParametrosFiltro = True    
        
    if pSearchParameters.get( 'fechaRevisionInicial', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchFechaRevisionInicial=%s""" % fCGIE( mfAsUnicode( pSearchParameters[ 'fechaRevisionInicial'])))
        unHayParametrosFiltro = True    
        
    if pSearchParameters.get( 'fechaRevisionFinal', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchFechaRevisionFinal=%s""" % fCGIE( mfAsUnicode( pSearchParameters[ 'fechaRevisionFinal'])))
        unHayParametrosFiltro = True    

        
    if pSearchParameters.get( 'usuarioCoordinador', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchUsuarioCoordinador=%s""" % fCGIE( mfAsUnicode( pSearchParameters[ 'usuarioCoordinador'])))
        unHayParametrosFiltro = True    
        
    if pSearchParameters.get( 'fechaDefinitivoInicial', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchFechaDefinitivoInicial=%s""" % fCGIE( mfAsUnicode( pSearchParameters[ 'fechaDefinitivoInicial'])))
        unHayParametrosFiltro = True    
        
    if pSearchParameters.get( 'fechaDefinitivoFinal', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchFechaDefinitivoFinal=%s""" % fCGIE( mfAsUnicode( pSearchParameters[ 'fechaDefinitivoFinal'])))
        unHayParametrosFiltro = True    

        
    if pSearchParameters.get( 'usuarioModificador', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchUsuarioModificador=%s""" % fCGIE( mfAsUnicode( pSearchParameters[ 'usuarioModificador'])))
        unHayParametrosFiltro = True    
        
    if pSearchParameters.get( 'fechaModificacionInicial', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchFechaModificacionInicial=%s""" % fCGIE( mfAsUnicode( pSearchParameters[ 'fechaModificacionInicial'])))
        unHayParametrosFiltro = True    
        
    if pSearchParameters.get( 'fechaModificacionFinal', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchFechaModificacionFinal=%s""" % fCGIE( mfAsUnicode( pSearchParameters[ 'fechaModificacionFinal'])))
        unHayParametrosFiltro = True    
        
    unosNombresModulos = pSearchParameters.get( 'nombresModulos', '')
    if not unosNombresModulos:
        unosNombresModulos = []
    else:    
        if not ( unosNombresModulos.__class__.__name__ in [ 'list', 'tuple',]):
            unosNombresModulos = [ unosNombresModulos,]

    for unNombreModulo in unosNombresModulos:
        if unNombreModulo:
            if unHayParametrosFiltro:
                unParametrosFiltroStream.write( '&')
            unHayParametrosFiltro = True    
            unParametrosFiltroStream.write( u"""theSearchNombresModulos=%s""" % fCGIE( unNombreModulo))
             
            
    if pSearchParameters.get( 'idCadena', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchIdCadena=%s""" % fCGIE( mfAsUnicode( pSearchParameters[ 'idCadena'])))
        unHayParametrosFiltro = True    

    if pSearchParameters.get( 'cadenasInactivas', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theInactiveStrings=on""" )
        unHayParametrosFiltro = True    
                      

    if pSearchParameters.get( 'simboloCadenaCursor', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSimboloCadenaCursor=%s""" % fCGIE( mfAsUnicode( pSearchParameters[ 'simboloCadenaCursor'])))
        unHayParametrosFiltro = True    


    if pSearchParameters.get( 'traduccionesPorPagina', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theTraduccionesPorPagina=%s""" % fCGIE( mfAsUnicode( str( pSearchParameters[ 'traduccionesPorPagina']))))
        unHayParametrosFiltro = True    

    if pSearchParameters.get( 'symbolIndex', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theGoToSymbolIndex=%s""" % fCGIE( mfAsUnicode( str( pSearchParameters[ 'symbolIndex']))))
        unHayParametrosFiltro = True    

    if pSearchParameters.get( 'pageIndex', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theGoToPageIndex=%s""" % fCGIE( mfAsUnicode( str( pSearchParameters[ 'pageIndex']))))
        unHayParametrosFiltro = True    

    if pSearchParameters.get( 'symbolStartingWith', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theGoToSymbolStartingWith=%s""" % fCGIE( mfAsUnicode( pSearchParameters[ 'symbolStartingWith'])))
        unHayParametrosFiltro = True    

    unParametrosFiltroString = unParametrosFiltroStream.getvalue()    
    
    
    
    unParametrosFiltroStream.close()
    unParametrosRequestStream = StringIO( u'')
    
    if pCodigoIdiomaCursor:
        unParametrosRequestStream.write( '?theCodigoIdiomaCursor=%s'% fCGIE( mfAsUnicode( pCodigoIdiomaCursor)))
        
        unParametrosRequestStream.write( '&theMostrarInforme=on&theMostrarLista=on')
    
    pIdiomasReferencia = pSearchParameters.get( 'idiomasReferencia', [])
    for aReferenceLanguage in pIdiomasReferencia:
        unParametrosRequestStream.write( '&theIdiomasReferencia=%s' % fCGIE( mfAsUnicode( aReferenceLanguage)))
                   
    unParametrosRequestString = unParametrosRequestStream.getvalue()
    
    unURLEnlaceFiltroTraduccion = '%s/TRATraducir/%s&%s' % ( aCatalogoURL, unParametrosRequestString, unParametrosFiltroString,)
                   
                   
    anOutput.write( u"""    
        <br/>
        <a href="%(urlEnlaceFiltro)s">
            %(gvSIGi18n_TranslationsFilterLink_label)s
            <p class="formHelp">%(gvSIGi18n_TranslationsFilterLink_help)s</p>
        </a>
        <br/>
        """ % { 
            'urlEnlaceFiltro': unURLEnlaceFiltroTraduccion, 
            'gvSIGi18n_TranslationsFilterLink_label': aTranslationsCache[ 'gvSIGi18n_TranslationsFilterLink_label'],
            'gvSIGi18n_TranslationsFilterLink_help':  mfCRs2BRs( aTranslationsCache[ 'gvSIGi18n_TranslationsFilterLink_help'],),
    })

    unTabIndex += 1

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
        'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label': aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label'],
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
            'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label': aTranslationsCache.get( 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_%s' % unEstadoTraduccion, unEstadoTraduccion),
            'portal_url':               aPortalURL, 
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
        'gvSIGi18n_filtro_label':                               aTranslationsCache[ 'gvSIGi18n_filtro_section_label'],
        'gvSIGi18n_limpiarfiltro_action_label':                 aTranslationsCache[ 'gvSIGi18n_todas_label'],
        'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label':  aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label'],
        'gvSIGi18n_todosEstados_action_label':                  aTranslationsCache[ 'gvSIGi18n_todosEstados_action_label'],
        'gvSIGi18n_todosPlus_action_label':                     aTranslationsCache[ 'gvSIGi18n_todosPlus_action_label'],
        'portal_url':                                           aPortalURL, 
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
        
     
 

    
    unTabIndex = _fRenderApplyOrCancelFiltro( 
        anOutput, 
        unContextualObject, 
        unTabIndex, 
        aPortalURL,
        aCatalogoURL,
        fCGIE,
        mfCRs2BRs,
        mfTranslateI18N,
        mfAsUnicode,
        aTranslationsCache,
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
                        <p class="formHelp">
                            <span >%(gvSIGi18n_searchByWords_help)s</span>
                        </p>
                    </th>
                </tr>
            </thead>      
            <tbody>  
            \n""" % { 
        'gvSIGi18n_BusquedasPorPalabrasContenidasEnSimboloOTraduccion_title':  aTranslationsCache[ 'gvSIGi18n_BusquedasPorPalabrasContenidasEnSimboloOTraduccion_title'],
        'gvSIGi18n_searchByWords_help':  mfCRs2BRs( fCGIE( aTranslationsCache[ 'gvSIGi18n_searchByWords_help'])),
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
        'simbolo':                                      fCGIE( mfAsUnicode( pSearchParameters[ 'simbolo'])),
        'gvSIGi18n_TRATraduccion_attr_simbolo_label':   aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_simbolo_label'],
        'gvSIGi18n_TRATraduccion_attr_simbolo_help':    aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_simbolo_help'],
        'gvSIGi18n_searchBySimbolo_help':               aTranslationsCache[ 'gvSIGi18n_searchBySimbolo_help'],
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
        'cadenaTraducida':                                      fCGIE( mfAsUnicode( pSearchParameters[ 'cadenaTraducida'])),
        'gvSIGi18n_TRATraduccion_attr_cadenaTraducida_label':   aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_cadenaTraducida_label'], 
        'font-size':                                            unasSizesIdioma[ 'edit_font_size'],
        'field-size':                                           unasSizesIdioma[ 'filter_field_size'] / 2,
        'gvSIGi18n_TRATraduccion_attr_cadenaTraducida_help':    aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_cadenaTraducida_help'], 
        'gvSIGi18n_searchByTranslation_help':                   aTranslationsCache[ 'gvSIGi18n_searchByTranslation_help'], 
    })
        
    unTabIndex += 1    

    anOutput.write( u"""  
            </tbody>
        </table>
        \n""")                                 
     
    
    
    
    

    
    unTabIndex = _fRenderApplyOrCancelFiltro( 
        anOutput, 
        unContextualObject, 
        unTabIndex, 
        aPortalURL,
        aCatalogoURL,
        fCGIE,
        mfCRs2BRs,
        mfTranslateI18N,
        mfAsUnicode,
        aTranslationsCache,)
    
    
    
    
    
    
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
        'gvSIGi18n_BusquedasPorEventos_formatoFechaISO_help':   aTranslationsCache[ 'gvSIGi18n_BusquedasPorEventos_formatoFechaISO_help'],
        'gvSIGi18n_BusquedasPorEventos_sePermitenFechasParciales_help':  aTranslationsCache[ 'gvSIGi18n_BusquedasPorEventos_sePermitenFechasParciales_help'],
        'gvSIGi18n_BusquedasPorEventos_despuesDeFecha_title':   aTranslationsCache[ 'gvSIGi18n_BusquedasPorEventos_despuesDeFecha_title'],
        'gvSIGi18n_BusquedasPorEventos_antesDeFecha_title':     aTranslationsCache[ 'gvSIGi18n_BusquedasPorEventos_antesDeFecha_title'],
        'gvSIGi18n_BusquedasPorEventos_title':                  aTranslationsCache['gvSIGi18n_BusquedasPorEventos_title'],
        'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label':  aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label'],
        'gvSIGi18n_BusquedasPorEventos_usuario_title':          aTranslationsCache[ 'gvSIGi18n_BusquedasPorEventos_usuario_title'],
    })            
    
    
    anOutput.write( u"""     
                <tr class="odd">
                    <td align="left" valign="baseline" bgColor="white">
                        <strong>%(gvSIGi18n_Modificacion)s</strong>
                    </td>
                    <td align="left" valign="baseline" >
                        <input tabindex=%(tabindex_modificador)d  style="font-size: 8pt;" size="12"  name="theSearchUsuarioModificador" id="theSearchUsuarioModificador" value="%(usuarioModificador)s" />
                    </td>
                    <td align="left" valign="baseline" >
                        <input tabindex=%(tabindex_fechaModificacionInicial)d style="font-size: 8pt;" size="22"  name="theSearchFechaModificacionInicial" id="theSearchFechaModificacionInicial" value="%(fechaModificacionInicial)s" />
                        <input tabindex=%(tabindex_fechaModificacionFinal)d style="font-size: 8pt;" size="22"  name="theSearchFechaModificacionFinal"   id="theSearchFechaModificacionFinal"   value="%(fechaModificacionFinal)s" />
                    </td>
                </tr>
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
                <tr class="odd">
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
                <tr class="even">
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
                <tr class="odd">
                    <td align="left" valign="baseline" bgColor="%(pBGcolor-Definitiva)s">
                        <img  alt="TranslationStatus_%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Definitiva)s" src="%(portal_url)s/%(estado-icon-Definitiva)s" title="%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Definitiva)s" />                        
                        <font color="%(pFGcolor-Definitiva)s"><strong>%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Definitiva)s</strong></font>
                    </td>
                    <td align="left" valign="baseline" >
                        <input tabindex=%(tabindex_coordinador)d  style="font-size: 8pt;" size="12"  name="theSearchUsuarioCoordinador" id="theSearchUsuarioCoordinador" value="%(usuarioCoordinador)s" />
                    </td>
                    <td align="left" valign="baseline" >
                        <input tabindex=%(tabindex_fechaDefinitivoInicial)d style="font-size: 8pt;" size="22"  name="theSearchFechaDefinitivoInicial" id="theSearchFechaDefinitivoInicial" value="%(fechaDefinitivoInicial)s" />
                        <input tabindex=%(tabindex_fechaDefinitivoFinal)d style="font-size: 8pt;" size="22"  name="theSearchFechaDefinitivoFinal"   id="theSearchFechaDefinitivoFinal"   value="%(fechaDefinitivoFinal)s" />
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
            'tabindex_fechaDefinitivoInicial':      unTabIndex + 10,
            'tabindex_fechaDefinitivoFinal':        unTabIndex + 11,
            'tabindex_modificador':                 unTabIndex + 12,
            'tabindex_fechaModificacionInicial':    unTabIndex + 13,
            'tabindex_fechaModificacionFinal':      unTabIndex + 14,
            'portal_url':                           aPortalURL, 
            'gvSIGi18n_Modificacion':               aTranslationsCache['gvSIGi18n_Modificacion'],
            'gvSIGi18n_TRATraduccion_Creada':       aTranslationsCache['gvSIGi18n_TRATraduccion_Creada'],
            'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Traducida':  aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_%s' % cEstadoTraduccionTraducida],
            'estado-icon-Traducida':    cIconsDict.get( cEstadoTraduccionTraducida, 'tra_traducida.gif'), 
            'usuarioCreador':           mfAsUnicode( pSearchParameters[ 'usuarioCreador']),
            'fechaCreacionInicial':     mfAsUnicode( pSearchParameters[ 'fechaCreacionInicial']),
            'fechaCreacionFinal':       mfAsUnicode( pSearchParameters[ 'fechaCreacionFinal']),
            'usuarioTraductor':         mfAsUnicode( pSearchParameters[ 'usuarioTraductor']),
            'fechaTraduccionInicial':   mfAsUnicode( pSearchParameters[ 'fechaTraduccionInicial']),
            'fechaTraduccionFinal':     mfAsUnicode( pSearchParameters[ 'fechaTraduccionFinal']),
            'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Revisada':    aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_%s' % cEstadoTraduccionRevisada],
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
            'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Definitiva': aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_%s' % cEstadoTraduccionDefinitiva],
            'estado-icon-Definitiva':   cIconsDict.get( cEstadoTraduccionDefinitiva, 'tra_definitiva.gif'), 
            'usuarioCoordinador':       mfAsUnicode( pSearchParameters[ 'usuarioCoordinador']),
            'fechaDefinitivoInicial':   mfAsUnicode( pSearchParameters[ 'fechaDefinitivoInicial']),
            'fechaDefinitivoFinal':     mfAsUnicode( pSearchParameters[ 'fechaDefinitivoFinal']),
            'usuarioModificador':       mfAsUnicode( pSearchParameters[ 'usuarioModificador']),
            'fechaModificacionInicial': mfAsUnicode( pSearchParameters[ 'fechaModificacionInicial']),
            'fechaModificacionFinal':   mfAsUnicode( pSearchParameters[ 'fechaModificacionFinal']),
        })
     
     
   
    unTabIndex += 15  

    

    
    unTabIndex = _fRenderApplyOrCancelFiltro( 
        anOutput, 
        unContextualObject, 
        unTabIndex, 
        aPortalURL,
        aCatalogoURL,
        fCGIE,
        mfCRs2BRs,
        mfTranslateI18N,
        mfAsUnicode,
        aTranslationsCache,
    )
    
    

    
    
    
    
    _pRenderFiltroModulos(
        anOutput, 
        unContextualObject, 
        pTodosNombresModulos, 
        pSearchParameters,
        fCGIE,
        mfCRs2BRs,
        mfTranslateI18N,
        mfAsUnicode,
        aTranslationsCache,
    )
    
    
           
                    

    
    unTabIndex = _fRenderApplyOrCancelFiltro( 
        anOutput, 
        unContextualObject, 
        unTabIndex, 
        aPortalURL,
        aCatalogoURL,
        fCGIE,
        mfCRs2BRs,
        mfTranslateI18N,
        mfAsUnicode,
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
                <tr class="odd" >
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
        'gvSIGi18n_BusquedasPorIdCadena_title': aTranslationsCache[ 'gvSIGi18n_BusquedasPorIdCadena_title'],
        'gvSIGi18n_TRACadena_attr_id_label':    aTranslationsCache[ 'gvSIGi18n_TRACadena_attr_id_label'],
        'gvSIGi18n_TRACadena_attr_id_help':     aTranslationsCache[ 'gvSIGi18n_TRACadena_attr_id_help'],
        'gvSIGi18n_searchById_help':            aTranslationsCache[ 'gvSIGi18n_searchById_help'],
    })                                                

                           
           
      
    unTabIndex += 1
    
    

    

    
    unTabIndex = _fRenderApplyOrCancelFiltro( 
        anOutput, 
        unContextualObject, 
        unTabIndex, 
        aPortalURL,
        aCatalogoURL,
        fCGIE,
        mfCRs2BRs,
        mfTranslateI18N,
        mfAsUnicode,
        aTranslationsCache,
    )
    
    
    
    
    
   
    anOutput.write( u""" 

        <!-- ########################
        Subsection: Include only Inactive Strings (by default off) 
        #############################-->
                                             
        <table class="listing nosort" id="sct_Filter_InactiveStrings" >
            <thead>
                <tr>
                    <th  align="left"  >
                        <font size="2">
                            <strong>
                                %(gvSIGi18n_FiltroCadenasInactivas_title)s
                            </strong>
                        </font>
                    </th>
                    <th>
                        <input type="checkbox" class="noborder"  value="on"  %(is-checked)s name="theInactiveStrings" 
                            id="theInactiveStrings" />
                    </th>
                </tr>
            </thead>      
            <tbody>
                <tr>
                    <td colspan="2">
                        <p class="formHelp">
                            <font size="1">
                                <span>%(gvSIGi18n_FiltroCadenasInactivas_help)s</span>
                            </font>
                        </p>
                    </td>
                </tr>
            </tbody>
        </table>
        \n""" % { 
        'is-checked':                                ( pSearchParameters[ 'cadenasInactivas'] and 'checked="checked"') or '',
        'tabindex':                                  unTabIndex,
        'gvSIGi18n_FiltroCadenasInactivas_title':    aTranslationsCache[ 'gvSIGi18n_FiltroCadenasInactivas_title'],
        'gvSIGi18n_FiltroCadenasInactivas_help':     aTranslationsCache[ 'gvSIGi18n_FiltroCadenasInactivas_help'],
    })                                                

      
    unTabIndex += 1
    
     
    
    

    
    unTabIndex = _fRenderApplyOrCancelFiltro( 
        anOutput, 
        unContextualObject, 
        unTabIndex, 
        aPortalURL,
        aCatalogoURL,
        fCGIE,
        mfCRs2BRs,
        mfTranslateI18N,
        mfAsUnicode,
        aTranslationsCache,)
    
    
    anOutput.write( u"""<br/>""") 

    
    
    
       
    return None












def _pRenderFiltroModulos( 
    anOutput, 
    unContextualObject, 
    pTodosNombresModulos, 
    pSearchParameters,
    fCGIE,
    mfCRs2BRs,
    mfTranslateI18N,
    mfAsUnicode,
    aTranslationsCache):
    """Render  the section to filter by modules.
    
    """    

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
        'gvSIGi18n_seleccionarTodos_label':                 aTranslationsCache[ 'gvSIGi18n_seleccionarTodos_label'],
        'gvSIGi18n_seleccionarNinguno_label':               aTranslationsCache[ 'gvSIGi18n_seleccionarNinguno_label'],
        'gvSIGi18n_modulesFilter_title':                    aTranslationsCache[ 'gvSIGi18n_modulesFilter_title'],
        'gvSIGi18n_modulesFilter_help':                     mfCRs2BRs( aTranslationsCache[ 'gvSIGi18n_modulesFilter_help']),
        'gvSIGi18n_refrescar_action_label':                 aTranslationsCache[ 'gvSIGi18n_refrescar_action_label'],                
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
                            id="theNombreModulo_%(index-modulo)s" />
                    </td>
                </tr>
            </body>
        </table>
        <br/>
         \n""" % {
        'index-modulo':                                    str( unIndexRowModulo),
        'class-row-modulo':                                cClasesFilas[ unIndexRowModulo % 2],
        'no-especificado':                                 cNombreModuloNoEspecificadoInputValue,
        'nombre-modulo-NoEspecificado':                    aTranslationsCache[ cNombreModuloNoEspecificadoLabel_MsgId],                
        'modulo-checked':                                  (( cNombreModuloNoEspecificadoInputValue in unosNombresModulos) and 'checked="checked"') or '',
    })

    return None
                
  




















    
def _pRenderCollapsibleGoTo( 
    anOutput           =None,
    unContextualObject =None,
    pNumberOfStrings   =None,
    pNumberOfPages     =None,
    pSearchParameters  =None,
    aPortalURL         =None,
    aCatalogoURL       =None,
    fCGIE              =None,
    mfCRs2BRs          =None,
    mfTranslateI18N    =None,
    mfAsUnicode        =None,
    aTranslationsCache =None,):
    """Render as collapsible the go to section of the translations browser.
    
    """    
    
    _pRenderCollapsible_Lambda(  anOutput,
        aTranslationsCache[ 'gvSIGi18n_seccionGoTo_title'],
        u'elid_GoTo_collapsible_dl', 
        lambda : _pRenderGoTo( 
            anOutput           =anOutput, 
            unContextualObject =unContextualObject, 
            pNumberOfStrings   =pNumberOfStrings,
            pNumberOfPages     =pNumberOfPages,
            pSearchParameters  =pSearchParameters,
            aPortalURL         =aPortalURL,
            aCatalogoURL       =aCatalogoURL,
            fCGIE              =fCGIE, 
            mfCRs2BRs          =mfCRs2BRs, 
            mfTranslateI18N    =mfTranslateI18N, 
            mfAsUnicode        =mfAsUnicode, 
            aTranslationsCache =aTranslationsCache, 
        ),
    )
    
    return None        













def _pRenderGoTo( 
    anOutput, 
    unContextualObject, 
    pNumberOfStrings,
    pNumberOfPages,
    pSearchParameters, 
    aPortalURL,
    aCatalogoURL,
    fCGIE,
    mfCRs2BRs,
    mfTranslateI18N,
    mfAsUnicode,
    aTranslationsCache):
    """Render the filter section of the translations browser.
    
    """    

    unTabIndex = 11
    
    anOutput.write( u"""    

        <!-- #################################################################
        SECTION: Specify the first symbol to show in the list
        ################################################################# -->
                      
        <br/>
        <input tabindex=%(tabindex)d name="form_submit" style="font-size: 10pt; font-style: italic"  value="%(gvSIGi18n_refrescar_action_label)s" type="submit"/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <input tabindex=%(tabindex2)d type="button" name="todos" style="font-size: 9pt; "  value="%(gvSIGi18n_first_label)s" onclick="pTRAResetGoToParameters(); return true;" class="TRAstyle_Clickable"  />
        <br/>
        \n""" % { 
        'tabindex':                                                    unTabIndex,
        'tabindex2':                                                   unTabIndex + 1,
        'gvSIGi18n_refrescar_action_label':                            aTranslationsCache[ 'gvSIGi18n_refrescar_action_label'],
        'gvSIGi18n_first_label':                                       aTranslationsCache[ 'gvSIGi18n_first_label'],                
    })
    
    
    unTabIndex += 2


    anOutput.write( u""" 

        <!-- ########################
        SubSection: GoTo parameters: symbol index number, page index number, symbol starting with string
        #############################-->
                                             
        <table class="listing nosort" id="sct_GoTo_Parameters" >
            <thead>
                <tr>
                    <th  align="left"  colspan="2">
                        <font size="2">
                            <strong>
                                %(gvSIGi18n_GoToParameters_title)s
                            </strong>
                        </font>
                    </th>
                </tr>
            </thead>      
            <tbody>  
            \n""" % { 
        'gvSIGi18n_GoToParameters_title':  aTranslationsCache[ 'gvSIGi18n_GoToParameters_title'], 
    })            

             
    
              
    
    anOutput.write( u""" 

        <!-- ########################
        SubSection: GoTo Parameter by Symbol Index Number
        #############################-->   
                                   
        <tr class="even" >
            <td align="left" valign="baseline" >
                %(gvSIGi18n_TranslationsPage_GoTo_SymbolIndex_label)s
                %(gvSIGi18n_TranslationsPage_GoTo_SymbolIndex_of)s
                %(pNumberOfStrings)s
                <p class="formHelp">%(gvSIGi18n_TranslationsPage_GoTo_SymbolIndex_help)s</p>
            </td>
            <td align="left" valign="baseline"  >
                <input type="text" tabindex=%(tabindex)d name="theGoToSymbolIndex" id="theGoToSymbolIndex" style="font-size: 10pt;" size="6" maxlength="6" value="" /> 
            </td>
        </tr>
        \n""" % { 
        'tabindex':                                             unTabIndex,
        'pNumberOfStrings':                                     mfAsUnicode( str( pNumberOfStrings)),
        'gvSIGi18n_TranslationsPage_GoTo_SymbolIndex_label':    aTranslationsCache[ 'gvSIGi18n_TranslationsPage_GoTo_SymbolIndex_label'],
        'gvSIGi18n_TranslationsPage_GoTo_SymbolIndex_of':       aTranslationsCache[ 'gvSIGi18n_TranslationsPage_GoTo_SymbolIndex_of'],
        'gvSIGi18n_TranslationsPage_GoTo_SymbolIndex_help':     aTranslationsCache[ 'gvSIGi18n_TranslationsPage_GoTo_SymbolIndex_help'],
    })
    
    
    unTabIndex += 1
    
    
    
            
    
    anOutput.write( u""" 

        <!-- ########################
        SubSection: GoTo Parameter by Page Index Number
        #############################-->   
                                   
        <tr class="odd" >
            <td align="left" valign="baseline" >
                %(gvSIGi18n_TranslationsPage_GoTo_PageIndex_label)s
                %(gvSIGi18n_TranslationsPage_GoTo_PageIndex_of)s
                %(pNumberOfPages)s
                <p class="formHelp">%(gvSIGi18n_TranslationsPage_GoTo_PageIndex_help)s</p>
            </td>
            <td align="left" valign="baseline"  >
                <input type="text" tabindex=%(tabindex)d name="theGoToPageIndex" id="theGoToPageIndex" style="font-size: 10pt;" size="4" maxlength="4" value="" /> 
            </td>
        </tr>
        \n""" % { 
        'tabindex':                                             unTabIndex,
        'pNumberOfPages':                                     mfAsUnicode( str( pNumberOfPages)),
        'gvSIGi18n_TranslationsPage_GoTo_PageIndex_label':    aTranslationsCache[ 'gvSIGi18n_TranslationsPage_GoTo_PageIndex_label'],
        'gvSIGi18n_TranslationsPage_GoTo_PageIndex_of':       aTranslationsCache[ 'gvSIGi18n_TranslationsPage_GoTo_PageIndex_of'],
        'gvSIGi18n_TranslationsPage_GoTo_PageIndex_help':     aTranslationsCache[ 'gvSIGi18n_TranslationsPage_GoTo_PageIndex_help'],
    })
    
    
    unTabIndex += 1
    
    

    anOutput.write( u""" 

        <!-- ########################
        SubSection: GoTo Parameter by Symbol starting with characters
        #############################-->   
                                   
        <tr class="even" >
            <td align="left" valign="baseline" >
                %(gvSIGi18n_TranslationsPage_GoTo_SymbolStartingWithChars_label)s
                <p class="formHelp">%(gvSIGi18n_TranslationsPage_GoTo_SymbolStartingWithChars_help)s</p>
            </td>
            <td align="left" valign="baseline"  >
                <input type="text" tabindex=%(tabindex)d name="theGoToSymbolStartingWith" id="theGoToSymbolStartingWith" style="font-size: 9pt;" size="16" maxlength="64" value="" /> 
            </td>
        </tr>
        \n""" % { 
        'tabindex':                                           unTabIndex,
        'gvSIGi18n_TranslationsPage_GoTo_SymbolStartingWithChars_label':    aTranslationsCache[ 'gvSIGi18n_TranslationsPage_GoTo_SymbolStartingWithChars_label'], 
        'gvSIGi18n_TranslationsPage_GoTo_SymbolStartingWithChars_help':     aTranslationsCache[ 'gvSIGi18n_TranslationsPage_GoTo_SymbolStartingWithChars_help'], 
    })
    
    
    unTabIndex += 1
    
    

    anOutput.write( u"""  
            </tbody>
        </table>
        <br/>
        \n""")                                 
             
    
    anOutput.write( u"""     
        <input tabindex=%(tabindex)d name="form_submit" style="font-size: 10pt; font-style: italic"  value="%(gvSIGi18n_refrescar_action_label)s" type="submit"/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <input tabindex=%(tabindex2)d type="button" name="todos" style="font-size: 9pt; "  value="%(gvSIGi18n_first_label)s" onclick="pTRAResetGoToParameters(); return true;" class="TRAstyle_Clickable"  />
        <br/>
        <br/>
        \n""" % { 
        'tabindex':                                                    unTabIndex,
        'tabindex2':                                                   unTabIndex + 1,
        'gvSIGi18n_refrescar_action_label':                            aTranslationsCache[ 'gvSIGi18n_refrescar_action_label'],                
        'gvSIGi18n_first_label':                                       aTranslationsCache[ 'gvSIGi18n_first_label'],                
    })
    
    
       
    return None








    
def _pRenderCollapsibleInforme( 
    anOutput                    =None,
    unContextualObject          =None,
    pEstadosIncluidos           =None,
    pInformeEstadosTodasCadenas =None,
    pInformeEstadosFiltrados    =None,
    pBrowsingInactiveStrings    =None,
    aPortalURL                  =None,
    aCatalogoURL                =None,
    fCGIE                       =None,
    mfCRs2BRs                   =None,
    mfTranslateI18N             =None,
    mfAsUnicode                 =None,
    aTranslationsCache          =None, ):
    """Render as collapsible the summary section of the translations browser.
    
    """    
    
    _pRenderCollapsible_Lambda(  anOutput,
        aTranslationsCache[ 'gvSIGi18n_seccionInformeSumario_title'],
        u'elid_Summary_collapsible_dl', 
        lambda : _pRenderInforme( 
            anOutput                    =anOutput,
            unContextualObject          =unContextualObject,
            pEstadosIncluidos           =pEstadosIncluidos,
            pInformeEstadosTodasCadenas =pInformeEstadosTodasCadenas,
            pInformeEstadosFiltrados    =pInformeEstadosFiltrados,
            pBrowsingInactiveStrings    =pBrowsingInactiveStrings,
            aPortalURL                  =aPortalURL,
            aCatalogoURL                =aCatalogoURL,
            fCGIE                       =fCGIE  ,
            mfCRs2BRs                   =mfCRs2BRs,
            mfTranslateI18N             =mfTranslateI18N,
            mfAsUnicode                 =mfAsUnicode,
            aTranslationsCache          =aTranslationsCache,
        ),
        False,
    )
    
    return None        

















def _pRenderInforme( 
    anOutput, 
    unContextualObject, 
    pEstadosIncluidos, 
    pInformeEstadosTodasCadenas, 
    pInformeEstadosFiltrados,
    pBrowsingInactiveStrings,
    aPortalURL,
    aCatalogoURL,
    fCGIE,
    mfCRs2BRs,
    mfTranslateI18N,
    mfAsUnicode,
    aTranslationsCache):
    """Render the summary section of the translations browser.
    
    """    
       
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
        \n"""
    )
    
        
    
    if pBrowsingInactiveStrings:
        anOutput.write( u"""    
    
            <!-- #################################################################
            SubSECTION: Clearly state that the user is browsing translations for strings in Inactive state
            ################################################################# -->
                         
            <p>
                <font size="2" color="red">
                    <strong>%s</strong>
                </font>
            </p>
            \n""" % aTranslationsCache[ 'gvSIGi18n_BrowsingInactiveStrings_label']
        )
    
            
        
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
        'gvSIGi18n_ocultar_action_label'  : aTranslationsCache[ 'gvSIGi18n_ocultar_action_label'], 
        'gvSIGi18n_informe_section_label' : aTranslationsCache[ 'gvSIGi18n_informe_section_label'],  
        'gvSIGi18n_total_label':            aTranslationsCache[ 'gvSIGi18n_total_label'], 
        'cInformeBiggerFontSize':           cInformeBiggerFontSize,
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
            'portal_url':                                                  aPortalURL, 
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
                <td align="left" valign="baseline" >
                    <font size="%(cInformeBiggerFontSize)s" >%(gvSIGi18n_traduccionesfiltradasidioma_label)s</font>
                </td>
                \n""" % { 
            'gvSIGi18n_traduccionesfiltradasidioma_label': mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_traduccionesfiltradasidioma_label', 'Filtered-'),
            'cInformeBiggerFontSize':   cInformeBiggerFontSize,
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







































def _pRenderEditorDetail( 
    anOutput, 
    unContextualObject, 
    pMostrarHistoria,
    pAllowChangeStringsModules,
    pTodosNombresModulos,
    aPortalURL,
    aCatalogoURL,
    fCGIE,
    mfCRs2BRs,
    mfTranslateI18N,
    mfAsUnicode,
    aTranslationsCache):
    """Render the details subsection of the editor section of the translations browser.
    
    """
             
    pIndex  = 0     
    
    anOutput.write( u"""    
        <!-- #################################################################
        SECTION: Editor DETAILS for selected TRATraduccion
        ################################################################# -->
        <div id="cid_TRAEditorDetalle" class="TRAstyle_Display">
    
            <table width="100%%" cellspacing="0" cellpadding="0" frame="void" id="editor_TRATraduccion" >
                <tbody>
                \n"""
    )
          
    

    anOutput.write( u"""
        <!-- #####
        ## Fields: display TRATraduccion cadena symbol and id, and translation changes counter.
        ##########-->  
            <tr class="TRAstyle_NoDisplay" id="cid_TRAEditorDetalle_simboloCadena_row">
                <td align="left" valign="baseline" >                
                    <font size="1" ><strong>%(gvSIGi18n_Symbol_title)s</strong></font>
                    &emsp;
                </td>
                <td  align="left" valign="baseline"  colspan="2">                
                    <font size="1" ><span id="cid_TRAEditorDetalle_simboloCadena" ></span></font>
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
            <tr class="TRAstyle_NoDisplay" id="cid_TRAEditorDetalle_contadorCambios_row">            
                <td align="left" valign="baseline" >       
                    <font size="1" ><strong>%(gvSIGi18n_TRATraduccion_attr_contadorCambios_label)s</strong></font>
                    &emsp;
                </td>
                <td align="left" valign="baseline" colspan="2">       
                    <font size="1" ><span id="cid_TRAEditorDetalle_contadorCambios" ></span></font>
                </td>
            </tr>
        \n""" % { 
        'gvSIGi18n_Symbol_title':               aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_simbolo_label'], 
        'gvSIGi18n_TRACadena_attr_id_label':    aTranslationsCache[ 'gvSIGi18n_TRACadena_attr_id_label'], 
        'gvSIGi18n_TRATraduccion_attr_contadorCambios_label':    aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_contadorCambios_label'], 
        'pClassFila':                           cClasesFilas [pIndex %2],
    })
    
        
    
    
    if pAllowChangeStringsModules:
        
        anOutput.write( u"""
            <!-- #####
            ## Fields: display TRATraduccion nombresModulos and open string modules editor open button.
            ##########-->  
                <tr class="TRAstyle_NoDisplay" id="cid_TRAEditorDetalle_nombresModulos_row">
                    <td align="left" valign="baseline" >                
                        <font size="1" ><strong>%(gvSIGi18n_Modulos_title)s</strong></font>
                        &emsp;
                        <input  
                            onmouseup="fTRAEvtHlr_Editor_Button_EditModules_OnMouseUp( )"
                            onkeypress="fTRAEvtHlr_Editor_Button_EditModules_OnKeyPress( event)"
                            id="TRAEditModulesButton" 
                            class="TRAstyle_Display TRAstyle_Clickable" 
                            name="TRAEditModulesButton" 
                            value="%(action_name)s" 
                            type="button" 
                            style="color: Green; font-size: 8pt; font-style: italic; font-weight: 300" />                    
                        
                    </td>
                    <td  align="left" valign="baseline"  colspan="2">                
                        <font size="1" ><span id="cid_TRAEditorDetalle_nombresModulos" ></span></font>
                    </td>
                </tr>
            \n""" % { 
            'gvSIGi18n_Modulos_title':              aTranslationsCache[ 'gvSIGi18n_Modulos_title'], 
            'pClassFila':                           cClasesFilas [pIndex %2],
            'action_name':                          aTranslationsCache[ 'gvSIGi18n_ModulesEditor_Open'], 
        })
    
        _pRenderEditorModulos( 
            anOutput, 
            unContextualObject, 
            pTodosNombresModulos, 
            fCGIE,
            mfCRs2BRs,
            mfTranslateI18N,
            mfAsUnicode,
            aTranslationsCache,
        )
        
    else:
        anOutput.write( u"""
            <!-- #####
            ## Fields: display TRATraduccion nombresModulos 
            ##########-->  
                <tr class="TRAstyle_NoDisplay" id="cid_TRAEditorDetalle_nombresModulos_row">
                    <td align="left" valign="baseline" >                
                        <font size="1" ><strong>%(gvSIGi18n_Modulos_title)s</strong></font>                        
                    </td>
                    <td  align="left" valign="baseline"  colspan="2">                
                        <font size="1" ><span id="cid_TRAEditorDetalle_nombresModulos" ></span></font>
                    </td>
                </tr>
            \n""" % { 
            'gvSIGi18n_Modulos_title':              aTranslationsCache[ 'gvSIGi18n_Modulos_title'], 
            'pClassFila':                           cClasesFilas [pIndex %2],
        })
        
        

        
    
    pIndex  += 1
        

                

                
                
                                        
    anOutput.write( u"""

        <!-- ########################
        SubSection: Auditing information state change dates and member ids
        #############################-->  
        
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
  








def _pRenderEditorModulos( 
    anOutput, 
    unContextualObject, 
    pTodosNombresModulos, 
    fCGIE,
    mfCRs2BRs,
    mfTranslateI18N,
    mfAsUnicode,
    aTranslationsCache):
    """Render  the section to edit string modules.
    
    """    

    if not pTodosNombresModulos:
        return None
    
    
    anOutput.write( u"""  
        
        <!-- #################################################################
        SECTION: Edition of modules for a string
        ################################################################# -->                           
        <tr id="cid_TRAEditorDetalle_Modulos" class="TRAstyle_NoDisplay">
            <td/>
            <td id="cid_TRAEditorDetalle_Modulos_Editor" >
                <table align="left" valign="top" id="sct_Edit_Modules_String" summary="Edit string modules" cellspacing="0" cellpadding="0" frame="void">
                    <tbody>   
                \n""" 
    )
    
    unIndexRowModulo = 0 
    for unNombreModulo in pTodosNombresModulos:  
                                 
        anOutput.write( u"""                                                                                                                                                                     
                        <tr >
                            <td align="left" valign="center" class="TRAstyle_Clickable"  >                
                                <font size="1" >
                                    <strong>
                                        %(nombre-modulo)s
                                    </strong>
                                </font>
                            </td>
                            <td align="left" valign="center" >    
                                &emsp;
                                <input type="checkbox" class="noborder"  value="%(nombre-modulo)s" name="theEditNombresModulos" 
                                    id="cid_TRAEditorDetalle_Modulos_%(index-modulo)s" />
                            </td>
                        </tr>
            \n""" % { 
            'index-modulo':         str( unIndexRowModulo),
            'nombre-modulo':        mfAsUnicode( unNombreModulo),        
        } )
        
        unIndexRowModulo += 1
    
    anOutput.write( u"""                
                    </tbody>
                </table>
                <br/>
                <br/>
                <br/>
                <input  
                    onmouseup="fTRAEvtHlr_Editor_Button_SaveModules_OnMouseUp( )"
                    onkeypress="fTRAEvtHlr_Editor_Button_SaveModules_OnKeyPress( event)"
                    tabindex=5
                    id="TRAEditModulesSaveButton" 
                    class="TRAstyle_Display TRAstyle_Clickable" 
                    name="TRAEditModulesSaveButton" 
                    value="%(action_name)s" 
                    type="button" 
                    style="color: Red; font-size: 8pt; font-style: italic; font-weight: 700" />
                <br/>
                <br/>
            </td>
        </td>
        <td/>
    </tr>
    \n""" % {
        'action_name':  aTranslationsCache[ 'gvSIGi18n_ModulesEditor_SaveStringModules'], 
    })
    
    return None
                
  













    
def _pRenderCollapsibleHistory( 
    anOutput            =None,                        
    unContextualObject  =None,                                  
    pCodigoIdiomaCursor =None,                                   
    pRegistrosHistoria  =None,                                  
    aPortalURL          =None,                         
    aCatalogoURL        =None,                           
    fCGIE               =None,                    
    mfCRs2BRs           =None,                        
    mfTranslateI18N     =None,                              
    mfAsUnicode         =None,                          
    aTranslationsCache  =None, ):
    """Render as collapsible the selected translation history section of the translations browser.
    
    """
    
    _pRenderCollapsible_Lambda(  anOutput,
        aTranslationsCache[ 'gvSIGi18n_seccionHistory_title'],
        u'elid_History_collapsible_dl', 
        lambda : _pRenderHistory( 
            anOutput            =anOutput,                        
            unContextualObject  =unContextualObject,                                  
            pCodigoIdiomaCursor =pCodigoIdiomaCursor,                                   
            pRegistrosHistoria  =pRegistrosHistoria,                                  
            aPortalURL          =aPortalURL,                         
            aCatalogoURL        =aCatalogoURL,                           
            fCGIE               =fCGIE,                    
            mfCRs2BRs           =mfCRs2BRs,                        
            mfTranslateI18N     =mfTranslateI18N,                              
            mfAsUnicode         =mfAsUnicode,                          
            aTranslationsCache  =aTranslationsCache,                                 
        ),
        True,
    )
    
    return None        







def _pRenderHistory( 
    anOutput, 
    unContextualObject, 
    pCodigoIdiomaCursor,
    pRegistrosHistoria, 
    aPortalURL,
    aCatalogoURL,
    fCGIE,
    mfCRs2BRs,
    mfTranslateI18N,
    mfAsUnicode,
    aTranslationsCache):
    """Render the selected translation history section of the translations browser.
    
    """   

    pIndex =0

    anOutput.write( u"""  
    
        <!-- #################################################################
        SECTION: History of changes for selected TRATraduccion
        ################################################################# -->
                                      
        <table class="listing nosort" id="sct_SelectedTRATraduccion_History" >
            <thead>
                <tr>                        
                    <th/>
                    <th  align="left" valign="baseline" >   
                        <font size="1" >%(gvSIGi18n_historiafechaaccion_label)s</font>
                    </th>
                    <th  align="left" valign="baseline" >   
                        <font size="1" >%(gvSIGi18n_historiausuarioactor_label)s</font>
                    </th>
                    <th  align="left" valign="baseline" >   
                        <font size="1" >%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label)s</font>
                    </th>
                </tr>
            </thead>      
            <tbody>                    
            \n""" % {                                  
        'gvSIGi18n_historiafechaaccion_label':                      aTranslationsCache[ 'gvSIGi18n_historiafechaaccion_label'],
        'gvSIGi18n_historiausuarioactor_label':                     aTranslationsCache[ 'gvSIGi18n_historiausuarioactor_label'],
        'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label':      aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_label'], 
    })


    for pRegistroHistoria in pRegistrosHistoria:
        
        unaTraduccionHistoria = pRegistroHistoria.get(  cTRAHistory_Translation, '').strip()
        unComentarioHistoria  = pRegistroHistoria.get(  cTRAHistory_Comment, '').strip()
        
        unStyleToBorder_Infos = ""
        
        if ( not unaTraduccionHistoria) and ( ( not pRegistroHistoria.get(  cTRAHistory_ActionKind, '') == 'Comentar') or ( not unComentarioHistoria)):
            unStyleToBorder_Infos = 'style="border-bottom: 1px solid" '
            
        
        
        anOutput.write( u"""                     
            <tr class="%(pClassFila)s" >
                <td %(unStyleToBorder_Infos)s align="left" valign="baseline" >   
                    <font size="1" ><strong>%(accion)s</strong></font>
                </td>
                <td %(unStyleToBorder_Infos)s  align="left" valign="baseline" >   
                    <font size="1" >%(fechaAccion)s</font>
                </td>
                <td %(unStyleToBorder_Infos)s  align="left" valign="baseline" >   
                    <font size="1" >%(usuarioActor)s</font>
                </td>
                \n""" % { 
            'unStyleToBorder_Infos': unStyleToBorder_Infos,
            'pClassFila':       cClasesFilas [ pIndex %2], 
            'accion':           aTranslationsCache.get( 'gvSIGi18n_TranslationHistoryAction_%s' % ( pRegistroHistoria.get( cTRAHistory_ActionKind, '') or cTranslationHistoryAction_Desconocida), ( pRegistroHistoria.get( cTRAHistory_ActionKind, '') or cTranslationHistoryAction_Desconocida),), 
            'fechaAccion':      pRegistroHistoria.get( cTRAHistory_ActionDate, ''),  
            'usuarioActor':     mfAsUnicode( pRegistroHistoria.get( cTRAHistory_User, '')),  
        })
                                                
                                                
        if  pRegistroHistoria.get( cTRAHistory_Status, ''):
                            
            anOutput.write( u"""                                             
                    <td %(unStyleToBorder_Infos)s  align="center" valign="baseline" bgcolor="%(pBGColor)s">   
                        <font color="%(pFGColor)s" size="1"><strong>%(estadoTraduccion)s</strong></font>
                    </td>
                </tr>           
                \n""" % { 
                'unStyleToBorder_Infos': unStyleToBorder_Infos,
                'pBGColor':             cBGColorsDict.get( pRegistroHistoria.get( cTRAHistory_Status,'') , cFGColorsDict[ cEstadoTraduccionPendiente]), 
                'pFGColor':             cFGColorsDict.get( pRegistroHistoria.get( cTRAHistory_Status,'') , cFGColorsDict[ cEstadoTraduccionPendiente]),
                'estadoTraduccion':     aTranslationsCache.get( 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_%s' % pRegistroHistoria.get( cTRAHistory_Status, ''), pRegistroHistoria.get( cTRAHistory_Status, '')), 
            })
        else:
            anOutput.write( u"""                                                                                                                        
                    <td />
                </tr>           
                \n""" )

            
        if ( pRegistroHistoria.get(  cTRAHistory_ActionKind, '') == 'Comentar') and unComentarioHistoria:
            anOutput.write( u"""                                                                                                                                                      
                <tr class="%(pClassFila)s" >
                    <td style="border-bottom: 1px solid"  align="left" valign="baseline" colspan="4" >   
                        <font size="1" >%(comentario)s</font>
                    </td>
                </tr>
                \n""" % { 
                'pClassFila':                          cClasesFilas [ pIndex %2], 
                'comentario':                          fCGIE( mfAsUnicode( mfCRs2BRs( pRegistroHistoria.get(  cTRAHistory_Comment, '')))), 
                'gvSIGi18n_historiacomentario_label':  aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_comentario_label'], 
            }) 
        else:
            if unaTraduccionHistoria:
                anOutput.write( u"""                                                                                                                                                      
                    <tr class="%(pClassFila)s" >
                        <td  style="border-bottom: 1px solid" align="left" valign="baseline" colspan="4" >   
                            <font size="%(font-size)d" >%(cadenaTraducida)s</font>
                        </td>
                    </tr>
                    \n""" % { 
                    'pClassFila':                                      cClasesFilas [ pIndex %2], 
                    'font-size':                                       TRASizesIdioma( pCodigoIdiomaCursor)[ 'display_font_size'],
                    'cadenaTraducida':                                 fCGIE( mfAsUnicode( unaTraduccionHistoria)), 
                    'gvSIGi18n_TRATraduccion_attr_cadenaTraducida_label':  aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_cadenaTraducida_label'], 
                })
                          
                            
        pIndex = pIndex +1
                     
        
        
    anOutput.write( u"""                                                                                                                                                      
            </tbody>
        </table>                                          
        \n""" 
    )     
                
    return None
    






    
        
        
        
    

def _pRenderEditorTextAreaAndButtons( 
    anOutput, 
    unContextualObject,         
    unasSizesIdioma,
    unosAllowedTargetStates,
    pAllowInvalidateStringTranslations,
    pAllowDeactivateStrings,
    pAllowActivateStrings,
    unEstadoTraduccion,
    aPortalURL,
    aCatalogoURL,
    fCGIE,
    mfCRs2BRs,
    mfTranslateI18N,
    mfAsUnicode,
    aTranslationsCache):

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
        ## Hidden Field: the new string module names requested 
        ##########-->  
        
        <input type="hidden" id="theNewModuleNames" name="theNewModuleNames" value="" />

        \n""" 
    )
    
        
    anOutput.write( u"""
        <!-- #####
        ## Hidden Field: the original change counter retrieved or received in the last asynch response for this translation 
        ##########-->  
        
        <input type="hidden" id="theChgCtr" name="theChgCtr" value="" />

        \n""" 
    )
    
    anOutput.write( u"""
        <!-- #####
        ## Hidden Field: the relative navigation command 
        ##########-->  
        
        <input type="hidden" id="theGoTo" name="theGoTo" value="" />

        \n""" 
    )
    
    unNumColumns = 2
    
    if pAllowDeactivateStrings or pAllowActivateStrings:
        unNumColumns += 1
    
    if pAllowInvalidateStringTranslations:
        unNumColumns += 1
        
    unButtonsColumnsWidth = int( 100 / unNumColumns)
    unButtonsColumnsWidthString = '%d%%' % unButtonsColumnsWidth
    

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
                onmouseup="fTRAEvtHlr_Editor_Button_Traducir_OnMouseUp( )"
                onkeypress="fTRAEvtHlr_Editor_Button_Traducir_OnKeyPress( event)"
                alt="%(action_name)s" 
                title="%(action_name)s" 
                src="%(portal_url)s/%(estado-icon-Traducida)s" />
            <input  
                onmouseup="fTRAEvtHlr_Editor_Button_Traducir_OnMouseUp( )"
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
        'portal_url':             aPortalURL, 
        'class-Display':          ((( unEstadoTraduccion in [ cEstadoTraduccionPendiente, cEstadoTraduccionTraducida,]) and ( len( set( [ cEstadoTraduccionPendiente, cEstadoTraduccionTraducida,]).intersection( unosAllowedTargetStates)) > 0)) and 'TRAstyle_Display') or 'TRAstyle_NoDisplay',
    })
   
      
 

    
    if pAllowInvalidateStringTranslations:
        anOutput.write( u"""  
            <td align="center" valign"=center" width="%(unButtonsColumnsWidthString)s" >
                [
                <img class="TRAstyle_Display TRAstyle_Clickable"
                    id="TRAStatusChangeButton_InvalidarTraduccionesCadena_Icon1" 
                    onmouseup="fTRAEvtHlr_Editor_Button_InvalidarTraduccionesCadena_OnMouseUp( )"
                    onkeypress="fTRAEvtHlr_Editor_Button_InvalidarTraduccionesCadena_OnKeyPress( event)"
                    alt="%(gvSIGi18n_TranslationAction_InvalidarTraduccionesCadena_help)s" 
                    title="%(gvSIGi18n_TranslationAction_InvalidarTraduccionesCadena_help)s" 
                    src="%(portal_url)s/%(estado-icon-Pendiente)s" />
                *
                <img class="TRAstyle_Display TRAstyle_Clickable"
                    id="TRAStatusChangeButton_InvalidarTraduccionesCadena_Icon2" 
                    onmouseup="fTRAEvtHlr_Editor_Button_InvalidarTraduccionesCadena_OnMouseUp( )"
                    onkeypress="fTRAEvtHlr_Editor_Button_InvalidarTraduccionesCadena_OnKeyPress( event)"
                    alt="%(gvSIGi18n_TranslationAction_InvalidarTraduccionesCadena_help)s" 
                    title="%(gvSIGi18n_TranslationAction_InvalidarTraduccionesCadena_help)s" 
                    src="%(portal_url)s/flag-plone.gif" />
                ]
                <input  
                    onmouseup="fTRAEvtHlr_Editor_Button_InvalidarTraduccionesCadena_OnMouseUp( )"
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
            'portal_url':                                                    aPortalURL, 
            'class-Display':                                                 'TRAstyle_Display',
        })
            

    
    if pAllowDeactivateStrings:
        anOutput.write( u"""  
            <td align="center" valign"=center" width="%(unButtonsColumnsWidthString)s" >
                <img class="TRAstyle_Display TRAstyle_Clickable"
                    id="TRAStatusChangeButton_DesactivarCadena_Icon" 
                    onmouseup="fTRAEvtHlr_Editor_Button_DesactivarCadena_OnMouseUp( )"
                    onkeypress="fTRAEvtHlr_Editor_Button_DesactivarCadena_OnKeyPress( event)"
                    alt="%(gvSIGi18n_TranslationAction_DesactivarCadena_help)s" 
                    title="%(gvSIGi18n_TranslationAction_DesactivarCadena_help)s" 
                    src="%(portal_url)s/delete_icon.gif" />
                <input  
                    onmouseup="fTRAEvtHlr_Editor_Button_DesactivarCadena_OnMouseUp( )"
                    onkeypress="fTRAEvtHlr_Editor_Button_DesactivarCadena_OnKeyPress( event)"
                    tabindex=5
                    id="TRAStatusChangeButton_DesactivarCadena" 
                    class="TRAstyle_Display TRAstyle_Clickable" 
                    name="TRAStatusChangeButton_DesactivarCadena" 
                    value="%(action_name)s" 
                    type="button" 
                    style="color: Red; font-size: 9pt; font-style: italic; font-weight: 700" />
            </td>        
            \n""" % { 
            'unButtonsColumnsWidthString': unButtonsColumnsWidthString,
            'action_name':                                                   aTranslationsCache[ 'gvSIGi18n_TranslationAction_DesactivarCadena_label'], 
            'gvSIGi18n_TranslationAction_DesactivarCadena_help':             aTranslationsCache[ 'gvSIGi18n_TranslationAction_DesactivarCadena_help'],
            'portal_url':                                                    aPortalURL, 
            'class-Display':                                                 'TRAstyle_Display',
        })
            
        

    if pAllowActivateStrings:
        anOutput.write( u"""  
            <td align="center" valign"=center" width="%(unButtonsColumnsWidthString)s" >
                <img class="TRAstyle_Display TRAstyle_Clickable"
                    id="TRAStatusChangeButton_ActivarCadena_Icon" 
                    onmouseup="fTRAEvtHlr_Editor_Button_ActivarCadena_OnMouseUp( )"
                    onkeypress="fTRAEvtHlr_Editor_Button_ActivarCadena_OnKeyPress( event)"
                    alt="%(gvSIGi18n_TranslationAction_ActivarCadena_help)s" 
                    title="%(gvSIGi18n_TranslationAction_ActivarCadena_help)s" 
                    src="%(portal_url)s/add_icon.gif" />
                <input  
                    onmouseup="fTRAEvtHlr_Editor_Button_ActivarCadena_OnMouseUp( )"
                    onkeypress="fTRAEvtHlr_Editor_Button_ActivarCadena_OnKeyPress( event)"
                    tabindex=5
                    id="TRAStatusChangeButton_ActivarCadena" 
                    class="TRAstyle_Display TRAstyle_Clickable" 
                    name="TRAStatusChangeButton_ActivarCadena" 
                    value="%(action_name)s" 
                    type="button" 
                    style="color: Red; font-size: 9pt; font-style: italic; font-weight: 700" />
            </td>        
            \n""" % { 
            'unButtonsColumnsWidthString': unButtonsColumnsWidthString,
            'action_name':                                                aTranslationsCache[ 'gvSIGi18n_TranslationAction_ActivarCadena_label'], 
            'gvSIGi18n_TranslationAction_ActivarCadena_help':             aTranslationsCache[ 'gvSIGi18n_TranslationAction_ActivarCadena_help'],
            'portal_url':                                                 aPortalURL, 
            'class-Display':                                              'TRAstyle_Display',
        })
            
                
    anOutput.write( u"""  
        <td align="right" valign"=center" width="%(unButtonsColumnsWidthString)s" >
            <img class="TRAstyle_Display TRAstyle_Clickable"
                id="TRAStatusChangeButton_Pendiente_Icon" 
                onmouseup="fTRAEvtHlr_Editor_Button_Pendiente_OnMouseUp( )"
                onkeypress="fTRAEvtHlr_Editor_Button_Pendiente_OnKeyPress( event)"
                alt="%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Pendiente)s" 
                title="%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Pendiente)s" 
                src="%(portal_url)s/%(estado-icon-Pendiente)s" />
            <input  
                onmouseup="fTRAEvtHlr_Editor_Button_Pendiente_OnMouseUp( )"
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
        'action_name':                 aTranslationsCache[ 'gvSIGi18n_TranslationAction_Borrar'], 
        'estado-icon-Pendiente':       cIconsDict.get( cEstadoTraduccionPendiente, 'tra_pendiente.gif'),
        'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Pendiente':   aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Pendiente'],
        'portal_url':                  aPortalURL, 
        'class-Display':               ((( unEstadoTraduccion in [ cEstadoTraduccionPendiente, cEstadoTraduccionTraducida,]) and ( len( set( [ cEstadoTraduccionPendiente, cEstadoTraduccionTraducida,]).intersection( unosAllowedTargetStates)) > 0)) and 'TRAstyle_Display') or 'TRAstyle_NoDisplay',
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
    
         
        
    




    
def _pRenderCollapsibleList( 
    anOutput                             =None,          
    unContextualObject                   =None,                                  
    pBrowseResult                        =None,                       
    pCodigoIdiomaCursor                  =None,                 
    pIdiomasReferencia                   =None,               
    pTodosNombresModulos                 =None,                  
    pDatosTraducciones                   =None,               
    pDictsTraduccionesIdiomasReferencia  =None,                                                 
    pLanguagesNamesAndFlags              =None,                         
    theWritePermission                   =None,              
    pAllowedStateTransitions             =None,                          
    pAllTargetStatusChanges              =None,                        
    pAllowInvalidateStringTranslations   =None,                                              
    pBrowsingInactiveStrings             =None,                          
    pAllowDeactivateStrings              =None,                        
    pAllowActivateStrings                =None,                    
    pAllowChangeStringsModules           =None,                              
    unSimboloCadenaATraducirHolder       =None,                                      
    pMostrarHistoria                     =None,          
    pShowStateTransitionColumns          =None,                                
    pBatchStatusChanges                  =None,                
    aPortalURL                           =None,                                                 
    aCatalogoURL                         =None,  
    fCGIE                                =None,
    mfCRs2BRs                            =None,
    mfTranslateI18N                      =None,        
    mfAsUnicode                          =None,
    aTranslationsCache                   =None,              
    unRolesCache                         =None,  ):
    """Render as collapsible the matching translations list section of the translations browser.
    
    """

    unCursorPositionString = u''
    
    if pBrowsingInactiveStrings:
        unCursorPositionString = u'%s ' % (
            aTranslationsCache[ 'gvSIGi18n_BrowsingInactive_collapsibleListLabel'],
        )
        
    unCursorPositionString =  u'%s %s %d %s %d %s %d' % ( 
        unCursorPositionString,
        aTranslationsCache[ 'gvSIGi18n_fromToIn_from_label'],
        pBrowseResult.get( 'from_translation_index', 0),
        aTranslationsCache[ 'gvSIGi18n_fromToIn_to_label'],
        pBrowseResult.get( 'to_translation_index', 0),
        aTranslationsCache[ 'gvSIGi18n_fromToIn_in_label'],
        pBrowseResult.get( 'total_translations', 0),
    )        
    
          
 
    _pRenderCollapsible_Lambda(  anOutput,
        u'%s  %s' % ( aTranslationsCache[ 'gvSIGi18n_seccionList_title'], unCursorPositionString),
        u'elid_List_collapsible_dl', 
        lambda : _pRenderList( 
            anOutput                             =anOutput,                                  
            unContextualObject                   =unContextualObject,                                  
            pCodigoIdiomaCursor                  =pCodigoIdiomaCursor,                                  
            pIdiomasReferencia                   =pIdiomasReferencia,                                  
            pTodosNombresModulos                 =pTodosNombresModulos,                                 
            pDatosTraducciones                   =pDatosTraducciones,                                  
            pDictsTraduccionesIdiomasReferencia  =pDictsTraduccionesIdiomasReferencia,                                  
            pLanguagesNamesAndFlags              =pLanguagesNamesAndFlags,                                  
            theWritePermission                   =theWritePermission,                                 
            pAllowedStateTransitions             =pAllowedStateTransitions,                                 
            pAllTargetStatusChanges              =pAllTargetStatusChanges,                                 
            pAllowInvalidateStringTranslations   =pAllowInvalidateStringTranslations,                                 
            pBrowsingInactiveStrings             =pBrowsingInactiveStrings,                                 
            pAllowDeactivateStrings              =pAllowDeactivateStrings,                                 
            pAllowActivateStrings                =pAllowActivateStrings,                                 
            pAllowChangeStringsModules           =pAllowChangeStringsModules,                                 
            unSimboloCadenaATraducirHolder       =unSimboloCadenaATraducirHolder,                                 
            pMostrarHistoria                     =pMostrarHistoria,                                 
            pShowStateTransitionColumns          =pShowStateTransitionColumns,                                 
            pBatchStatusChanges                  =pBatchStatusChanges,                                 
            unCursorPositionString               =unCursorPositionString,                                 
            aPortalURL                           =aPortalURL,                                 
            aCatalogoURL                         =aCatalogoURL,                                 
            fCGIE                                =fCGIE,                                 
            mfCRs2BRs                            =mfCRs2BRs,                                 
            mfTranslateI18N                      =mfTranslateI18N,                                 
            mfAsUnicode                          =mfAsUnicode,                                 
            aTranslationsCache                   =aTranslationsCache,                                  
            unRolesCache                         =unRolesCache,                                                                 
        ),
        False,
    )
    
    return None        


            
            
            

def _pRenderList( 
    anOutput                             =None,
    unContextualObject                   =None,
    pCodigoIdiomaCursor                  =None,
    pIdiomasReferencia                   =None,
    pTodosNombresModulos                 =None,
    pDatosTraducciones                   =None,
    pDictsTraduccionesIdiomasReferencia  =None,
    pLanguagesNamesAndFlags              =None,
    theWritePermission                   =None,
    pAllowedStateTransitions             =None,
    pAllTargetStatusChanges              =None,
    pAllowInvalidateStringTranslations   =None,
    pBrowsingInactiveStrings             =None,
    pAllowDeactivateStrings              =None,
    pAllowActivateStrings                =None,
    pAllowChangeStringsModules           =None,
    unSimboloCadenaATraducirHolder       =None,
    pMostrarHistoria                     =None,
    pShowStateTransitionColumns          =None,
    pBatchStatusChanges                  =None,
    unCursorPositionString               =None,
    aPortalURL                           =None,
    aCatalogoURL                         =None,
    fCGIE                                =None,
    mfCRs2BRs                            =None,
    mfTranslateI18N                      =None,
    mfAsUnicode                          =None,
    aTranslationsCache                   =None,
    unRolesCache                         =None, ):
    """Render the matching translations list section of the translations browser in two columns.
    
    """

    aDictRenderValues = aTranslationsCache.copy()
    aDictRenderValues.update( {
        'portal_url':  aPortalURL, 
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
                        id="cid_ColumnaSimbolos" 
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
        
    
    if  pShowStateTransitionColumns and ( len( someEstadosConBotonesEnColumnas) > 0):
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

         
    if pShowStateTransitionColumns and ( len( someEstadosConBotonesEnColumnas) > 0) and pBatchStatusChanges:
        anOutput.write( u"""  
            <tr>
                <th colspan="5" />
                <th colspan="%(colspan)s" valign="bottom"  />
                    <input  
                        onmouseup="fTRAEvtHlr_BatchStatusChange_Apply_Button_OnMouseUp( )"
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
                        onmouseup="pTRAToggleAllBatchStatusChanges( '%(nombre_estado)s'); return true;"
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
                'portal_url':                               aPortalURL, 
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
    
    pNumTotalColumns  = 5 + ( ( pShowStateTransitionColumns and len( someEstadosConBotonesEnColumnas)) or 0)

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
     
    
    unColSpanTraduccionIdiomaReferencia   = 1
    unColSpanSimboloEnColumnaTraducciones = 1 + ( ( pShowStateTransitionColumns and len( someEstadosConBotonesEnColumnas)) or 0)


                        
    unYaRendereadoEditor = False
    
    for unosDatosTraduccion in pDatosTraducciones:
        
        unRendereadoEditorEnEstaFila = False
        
        
        pTradRow_getSimbolo             = unosDatosTraduccion[ 'getSimbolo']            or ''
        pTradRow_getIdCadena            = unosDatosTraduccion[ 'getIdCadena']           or ''
        pTradRow_getEstadoTraduccion    = unosDatosTraduccion[ 'getEstadoTraduccion']   or cEstadoTraduccionPendiente 
        pTradRow_getCadenaTraducida     = unosDatosTraduccion[ 'getCadenaTraducida']    or ''
        pTradRow_getNombresModulos      = unosDatosTraduccion[ 'getNombresModulos']     or '' 
        pTradRow_getContadorCambios     = unosDatosTraduccion[ 'getContadorCambios']    or 0
        pTradRow_getFechaDefinitivo     = unosDatosTraduccion[ 'getFechaDefinitivoTextual']    or ''
        pTradRow_getUsuarioCoordinador  = unosDatosTraduccion[ 'getUsuarioCoordinador']     or ''
        pTradRow_getFechaRevision       = unosDatosTraduccion[ 'getFechaRevisionTextual']      or ''
        pTradRow_getUsuarioRevisor      = unosDatosTraduccion[ 'getUsuarioRevisor']     or ''
        pTradRow_getFechaTraduccion     = unosDatosTraduccion[ 'getFechaTraduccionTextual']    or ''
        pTradRow_getUsuarioTraductor    = unosDatosTraduccion[ 'getUsuarioTraductor']   or ''
        pTradRow_getFechaCreacion       = unosDatosTraduccion[ 'getFechaCreacionTextual']    or ''
        pTradRow_getUsuarioCreador      = unosDatosTraduccion[ 'getUsuarioCreador']   or ''
        pTradRow_getFechaModificacion   = unosDatosTraduccion[ 'getFechaModificacionTextual']    or ''
        pTradRow_getUsuarioModificador  = unosDatosTraduccion[ 'getUsuarioModificador']   or ''
        
        if not isinstance( pTradRow_getContadorCambios, int):
            pTradRow_getContadorCambios = 0
            
                    
        unosAllowedTargetStates = pAllowedStateTransitions.get( pTradRow_getEstadoTraduccion, set())
         
        
        unPuedeEntrarEnEdicion = theWritePermission and \
            (( ( pTradRow_getEstadoTraduccion in [ cEstadoTraduccionPendiente, cEstadoTraduccionTraducida, ]) and \
            ( cEstadoTraduccionTraducida in unosAllowedTargetStates)) and 1) or 0
        
        unPermiteBotones = ( len( unosAllowedTargetStates) > 0 and 1) or pAllowInvalidateStringTranslations or pAllowDeactivateStrings or pAllowActivateStrings or False 

        unEntrarEnEdicionEventHandler = """
            onclick="fTRAEvtHlr_Row_OnClick( %(symbol_cell_counter)d); return true;"
            \n""" % { 
            'symbol_cell_counter':                                  pSymbolCellCounter,
        }
        
                 
        unasRowsToSpan = len( unosIdiomasIdiomasReferenciaSinElPrincipal) + 2
        if pMostrarHistoria:
            unasRowsToSpan += 1
        unRowSpanAttribute = ( 'rowspan="%d"' % (unasRowsToSpan)) or ''

        unSimboloCadenaUnicode          = mfAsUnicode( pTradRow_getSimbolo)   
        unSimboloCadenaCGIescaped       = fCGIE( unSimboloCadenaUnicode)   
        unSimboloCadenaForWrapLines     = fCGIE( _fWrapeableLinesString( unSimboloCadenaUnicode,           cSimboloCadenaLineWrapLen))

        unaCadenaTraducidaUnicode       = mfAsUnicode( pTradRow_getCadenaTraducida)
        unaCadenaTraducidaCGIescaped    = fCGIE( unaCadenaTraducidaUnicode)
        unaCadenaTraducidaForWrapLines  = fCGIE( _fWrapeableLinesString( unaCadenaTraducidaUnicode,   cCadenaTraducidaLineWrapLen))  
        
        
   
                    
        
        unDictRenderValues = { 
            'gvSIGi18n_TRATraduccion_attr_simbolo_label':          mfAsUnicode( aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_simbolo_label']),
            'portal_url':                                           aPortalURL, 
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
            'cadenaTraducida':                                      unaCadenaTraducidaCGIescaped,
            'cadenaTraducida-forWrapLines':                         unaCadenaTraducidaForWrapLines,
            'font-size':                                            unDisplayFontSize_IdiomaPrincipal,
            'pClassFila':                                           cClasesFilas [ pIndex %2], 
            'codigo-idioma':                                        mfAsUnicode( pCodigoIdiomaCursor), 
            'nombre-idioma':                                        mfAsUnicode( pLanguagesNamesAndFlags.get( pCodigoIdiomaCursor, {}).get( 'english', '')),        
            'flag-icon':                                            mfAsUnicode( pLanguagesNamesAndFlags.get( pCodigoIdiomaCursor, {}).get( 'flag', cTRAFlagIdiomaDesconocida)), 
            'flag-url':                                             mfAsUnicode( pLanguagesNamesAndFlags.get( pCodigoIdiomaCursor, {}).get( 'flag_url', '')), 
            'pBGColor':                                             cBGColorsDict.get( pTradRow_getEstadoTraduccion,  cBGColorsDict[ cEstadoTraduccionPendiente]),
            'pFGColor':                                             cFGColorsDict.get( pTradRow_getEstadoTraduccion,  cBGColorsDict[ cEstadoTraduccionPendiente]),
            'estado-icon':                                          cIconsDict.get( pTradRow_getEstadoTraduccion, 'tra_pendiente.gif'), 
            'pTradRow_getNombresModulos':                           fCGIE( mfAsUnicode( pTradRow_getNombresModulos)),
            'pTradRow_getContadorCambios':                          pTradRow_getContadorCambios,
            'pTradRow_getFechaDefinitivo':                          pTradRow_getFechaDefinitivo,
            'pTradRow_getUsuarioCoordinador':                       fCGIE(mfAsUnicode(pTradRow_getUsuarioCoordinador)),
            'pTradRow_getFechaRevision':                            pTradRow_getFechaRevision,
            'pTradRow_getUsuarioRevisor':                           fCGIE(mfAsUnicode(pTradRow_getUsuarioRevisor)),
            'pTradRow_getFechaTraduccion':                          pTradRow_getFechaTraduccion,
            'pTradRow_getUsuarioTraductor':                         fCGIE(mfAsUnicode(pTradRow_getUsuarioTraductor)),
            'pTradRow_getFechaCreacion':                            pTradRow_getFechaCreacion,
            'pTradRow_getUsuarioCreador':                           fCGIE(mfAsUnicode(pTradRow_getUsuarioCreador)),
            'colspan_SimboloEnColumnaTraducciones':                 unColSpanSimboloEnColumnaTraducciones,
        }
        

        anOutput.write( u"""  
            <tr class="%s TRAstyle_NoDisplay"  id="cid_TRAInteractionMessageHolder_%d">
                <td colspan="%d" class="TRAstyle_Clickable" %s   valign="top">
                    <font size="1">
                        <strong>%s</strong>
                        <span  id="cid_TRAInteractionMessage_%d" >
                    </font>
                </td>
            </tr>
            \n""" %  (  
            cClasesFilas [ pIndex %2],
            pSymbolCellCounter,
            pNumTotalColumns, 
            unDictRenderValues.get( 'entrar_en_edicion', ''),
            aTranslationsCache[ 'gvSIGi18n_InteracionStatusMessage'],
            pSymbolCellCounter
        ))
        
        
        
        
        # ACV 20110220
                
        anOutput.write( u"""  
            <tr class="%(pClassFila)s TRAstyle_NoDisplay"  id="cid_FilaParaSimboloSobreTraducciones_%(symbol_cell_counter)d">
                <td class="xxTRAstyle_NoDisplay" id="cid_ColumnaSimbolos_%(symbol_cell_counter)d_fillerForSymbol" />
                <td colspan="3" class="xxTRAstyle_NoDisplay" id="cid_ColumnaSimbolos_%(symbol_cell_counter)d_fillerForLanguageAndStatusColumns" >
                     %(gvSIGi18n_TRATraduccion_attr_simbolo_label)s
                <td/>
                <td colspan="%(colspan_SimboloEnColumnaTraducciones)d" 
                    id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_simboloCadena_SobreTraducciones"                    
                    class="TRAstyle_Clickable xxTRAstyle_NoDisplay"  valign="top" %(entrar_en_edicion)s >
                    <font size="1">
                        <span id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_simboloCadena_SobreTraducciones_Display" >%(simbolo-cadena-forWrapLines)s</span>
                    </font>
                </td>
            </tr>
            \n""" % unDictRenderValues
        )
         
        
        anOutput.write( u"""  
            <tr class="%(pClassFila)s"  id="cid_FilaPrimeraDeSimbolo_%(symbol_cell_counter)d">
                <td  class="TRAstyle_Display TRAstyle_Clickable" valign="top" %(row_span)s  
                    %(entrar_en_edicion)s 
                    id="cid_ColumnaSimbolos_%(symbol_cell_counter)d" >
                    <font size="1" class="TRAstyle_Display"  id="cid_ColumnaSimbolos_%(symbol_cell_counter)d_SymbolDisplay" >%(simbolo-cadena-forWrapLines)s</font>
                    <span class="TRAstyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_simboloCadena" >%(simbolo-cadena)s</span>
                </td>
                <td align="center" valign="top" class="TRAstyle_Clickable" onclick="pTRANavegarASimboloCadenaEnFilaNumero( '%(symbol_cell_counter)d')"  >                
                    <img width="14" height="11" alt="Flag_%(nombre-idioma)s" src="%(flag-url)s" title="%(nombre-idioma)s" />
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
                    <span class="TRAstyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_simboloCadena">%(simbolo-cadena)s</span>
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
                    <span class="TRAstyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_contadorCambios">%(pTradRow_getContadorCambios)d</span>
                    <span class="TRAstyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_interactionStatus"></span>
                    <span class="TRAstyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_interactionMessage"></span>
                    \n""" % 
            unDictRenderValues
        )
                
                                                 

       
        if  not unYaRendereadoEditor:
            unYaRendereadoEditor = True
            unRendereadoEditorEnEstaFila = True
            if unPuedeEntrarEnEdicion or unPermiteBotones:
                unSimboloCadenaATraducirHolder[ 0] = pTradRow_getSimbolo
            
            unasSizesIdioma = TRASizesIdioma( pCodigoIdiomaCursor)
            
            _pRenderEditorTextAreaAndButtons( 
                anOutput, 
                unContextualObject,         
                unasSizesIdioma,
                unosAllowedTargetStates,
                pAllowInvalidateStringTranslations,
                pAllowDeactivateStrings,
                pAllowActivateStrings,
                pTradRow_getEstadoTraduccion,
                aPortalURL,
                aCatalogoURL,
                fCGIE,
                mfCRs2BRs,
                mfTranslateI18N,
                mfAsUnicode,
                aTranslationsCache
            )
        
            
        anOutput.write( u"""  
            </td>
            """
        )

        # ################################################################
        """Render state change action buttons on their own column.
        
        """, 
        if pShowStateTransitionColumns:
            if ( cEstadoTraduccionTraducida in pAllTargetStatusChanges):
                anOutput.write( u"""  
                    <td  align="center"  valign="top"  id="cid_ColumnaStatusChangeButton_%(symbol_cell_counter)d_Traducida"                     
                        ><img
                            id="TRAStatusChangeButton_%(symbol_cell_counter)d_Traducida" 
                            class="%(class-Display)s TRAstyle_Clickable"    
                            onmouseup="fTRAEvtHlr_Editor_Button_StatusChange_OnMouseUp( '%(symbol_cell_counter)d', 'Traducida')"
                            alt="%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Traducida)s" 
                            title="%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Traducida)s" 
                            src="%(portal_url)s/%(estado-icon-Traducida)s" /></td>
                    \n""" % {
                    'class-Display':           (  (( cEstadoTraduccionTraducida in unosAllowedTargetStates) and not ( pTradRow_getEstadoTraduccion in [ cEstadoTraduccionPendiente,  cEstadoTraduccionTraducida, ])) and 'TRAstyle_Display') or 'TRAstyle_NoDisplay',
                    'symbol_cell_counter':     pSymbolCellCounter,
                    'estado-icon-Traducida':   cIconsDict.get( cEstadoTraduccionTraducida, 'tra_traducida.gif'),
                    'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Traducida':   aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Traducida'],
                    'portal_url':              aPortalURL, 
                })
                    
            if ( cEstadoTraduccionRevisada in pAllTargetStatusChanges):
                anOutput.write( u"""  
                    <td  align="center"  valign="top"  id="cid_ColumnaStatusChangeButton_%(symbol_cell_counter)d_Revisada"                     
                        ><img
                            id="TRAStatusChangeButton_%(symbol_cell_counter)d_Revisada" 
                            class="%(class-Display)s TRAstyle_Clickable"
                            onmouseup="fTRAEvtHlr_Editor_Button_StatusChange_OnMouseUp( '%(symbol_cell_counter)d', 'Revisada')"
                            alt="%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Revisada)s" 
                            title="%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Revisada)s" 
                            src="%(portal_url)s/%(estado-icon-Revisada)s" /></td>
                    \n""" % {
                    'class-Display':          (  ( cEstadoTraduccionRevisada in unosAllowedTargetStates) and 'TRAstyle_Display') or 'TRAstyle_NoDisplay',
                    'symbol_cell_counter':    pSymbolCellCounter,
                    'estado-icon-Revisada':   cIconsDict.get( cEstadoTraduccionRevisada, 'tra_revisada.gif'),
                    'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Revisada':   aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Revisada'],
                    'portal_url':             aPortalURL, 
                })
                    
            if ( cEstadoTraduccionDefinitiva in pAllTargetStatusChanges):
                anOutput.write( u"""  
                    <td  align="center"  valign="top" id="cid_ColumnaStatusChangeButton_%(symbol_cell_counter)d_Definitiva""                      
                        ><img 
                                class="%(class-Display)s TRAstyle_Clickable"
                                id="TRAStatusChangeButton_%(symbol_cell_counter)d_Definitiva" 
                                onmouseup="fTRAEvtHlr_Editor_Button_StatusChange_OnMouseUp( '%(symbol_cell_counter)d', 'Definitiva')"
                                alt="%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Definitiva)s" 
                                title="%(gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Definitiva)s" 
                                src="%(portal_url)s/%(estado-icon-Definitiva)s" /></td>
                    \n""" % {
                    'class-Display':           (  ( cEstadoTraduccionDefinitiva in unosAllowedTargetStates) and 'TRAstyle_Display') or 'TRAstyle_NoDisplay',
                    'symbol_cell_counter':     pSymbolCellCounter,
                    'estado-icon-Definitiva':  cIconsDict.get( cEstadoTraduccionDefinitiva, 'tra_definitiva.gif'),
                    'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Definitiva':   aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_Definitiva'],
                    'portal_url':              aPortalURL, 
                })
       
        anOutput.write( u"""  
            </tr>
            \n"""
        )

                                
       
        anOutput.write( u"""  
            <tr class="%s">
                <td  colspan="%d"  id="cid_TRAEditorDetalleHolder_%d" >
                \n""" %  (  cClasesFilas [ pIndex %2], 4 + len( someEstadosConBotonesEnColumnas), pSymbolCellCounter)
        )
        
        if unRendereadoEditorEnEstaFila:
            _pRenderEditorDetail( 
                anOutput, 
                unContextualObject,  
                pMostrarHistoria,
                pAllowChangeStringsModules,
                pTodosNombresModulos,
                aPortalURL,
                aCatalogoURL,
                fCGIE,
                mfCRs2BRs,
                mfTranslateI18N,
                mfAsUnicode,
                aTranslationsCache        
            )
    
        anOutput.write( u""" 
                </td>
            </tr>
            \n""" 
        )
                      


        if pMostrarHistoria :
            
            unosRegistrosHistoria = [ ]
            unElementoTraduccion       = unosDatosTraduccion.getObject()
            if unElementoTraduccion:
                
                anOutput.write( u"""  
                    <tr class="%s">
                        <td  colspan="%d"   >
                        \n""" %  (  cClasesFilas [ pIndex %2], 4 + len( someEstadosConBotonesEnColumnas),)
                )
                    
                
                unosRegistrosHistoria = unElementoTraduccion.getRegistrosHistoria()                
                if unosRegistrosHistoria:

                    unosRegistrosHistoria.reverse()
            
                    _pRenderCollapsibleHistory( 
                        anOutput            =anOutput,                         
                        unContextualObject  =unContextualObject,                                   
                        pCodigoIdiomaCursor =pCodigoIdiomaCursor,                                    
                        pRegistrosHistoria  =unosRegistrosHistoria,                                
                        aPortalURL          =aPortalURL,                          
                        aCatalogoURL        =aCatalogoURL,                            
                        fCGIE               =fCGIE,                     
                        mfCRs2BRs           =mfCRs2BRs,                         
                        mfTranslateI18N     =mfTranslateI18N,                               
                        mfAsUnicode         =mfAsUnicode,                           
                        aTranslationsCache  =aTranslationsCache                                   
                    )
                
                else:
                    anOutput.write( u"""<font size="1">%s</font>
                    """ % aTranslationsCache[ 'gvSIGi18n_NoTranslationsHistory']
                    )                    
                    
                    
                anOutput.write( u""" 
                        </td>
                    </tr>
                """
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
            unaCadenaTraducidaReferenciaCGIescaped    = fCGIE( unaCadenaTraducidaReferenciaUnicode)
            unaCadenaTraducidaReferenciaForWrapLines  = fCGIE( _fWrapeableLinesString( unaCadenaTraducidaReferenciaUnicode,   cCadenaTraducidaLineWrapLen))
            
            

                    
                        
            unDictRenderIdiomaReferenciaValues = { 
                'entrar_en_edicion':                        unEntrarEnEdicionEventHandler,
                'symbol_cell_counter':                      pSymbolCellCounter,
                'cadenaTraducidaReferencia':                unaCadenaTraducidaReferenciaCGIescaped,
                'cadenaTraducidaReferencia-forWrapLines':   unaCadenaTraducidaReferenciaForWrapLines,
                'font-size':                                unosDisplayFontSizes_IdiomasReferencia[ unIdiomaReferencia],
                'class-row-idioma':                         cClasesFilas[ pIndexRowIdioma % 2],
                'codigo-idioma':                            mfAsUnicode( unIdiomaReferencia),
                'nombre-idioma':                            mfAsUnicode( pLanguagesNamesAndFlags.get( unIdiomaReferencia, {}).get( 'english', '')),        
                'portal_url':                               aPortalURL, 
                'flag-icon':                                pLanguagesNamesAndFlags.get( unIdiomaReferencia, {}).get( 'flag', cTRAFlagIdiomaDesconocida), 
                'flag-url':                                 mfAsUnicode( pLanguagesNamesAndFlags.get( unIdiomaReferencia, {}).get( 'flag_url', '')), 
                'pBGColor':                                 cBGColorsDict.get( unEstadoTraduccion,  cBGColorsDict[ cEstadoTraduccionPendiente]),
                'pFGColor':                                 cFGColorsDict.get( unEstadoTraduccion,  cBGColorsDict[ cEstadoTraduccionPendiente]),
                'estadoTraduccion':                         unEstadoTraduccion,            
                'estadoTraduccion_label':                   ( unEstadoTraduccion and aTranslationsCache[ 'gvSIGi18n_TRATraduccion_attr_estadoTraduccion_option_%s' % unEstadoTraduccion]) or '?',            
                'estado-icon':                              cIconsDict.get( unEstadoTraduccion, 'tra_pendiente.gif'), 
                'colspan_translation':                      unColSpanTraduccionIdiomaReferencia,
            }
            
                        
            unNavegarAIdiomaYSimboloEventHandler = """
                onclick="pTRANavegarAIdiomaPrincipalYSimboloCadenaEnFilaNumero('%(codigo-idioma)s', '%(symbol_cell_counter)d', '%(estadoTraduccion)s'); return true;"
                \n""" % unDictRenderIdiomaReferenciaValues
            
            unDictRenderIdiomaReferenciaValues[ 'navegar_a_idioma_y_simbolo'] = unNavegarAIdiomaYSimboloEventHandler

            
            anOutput.write( u"""                                                                                                                                                                     
                <tr class="%(class-row-idioma)s" >
                    <td align="center" valign="baseline" class="TRAstyle_Clickable" 
                        %(entrar_en_edicion)s >  
                        <img width="14" height="11" alt="Flag_%(codigo-idioma)s" src="%(flag-url)s" title="%(codigo-idioma)s" />
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
                    <td  align="left" valign="baseline" class="TRAstyle_Clickable"  colspan="%(colspan_translation)d"
                        %(entrar_en_edicion)s >
                        <font size="%(font-size)d">%(cadenaTraducidaReferencia-forWrapLines)s</font>
                    </td>
                \n""" % unDictRenderIdiomaReferenciaValues
            )

            if pShowStateTransitionColumns and ( len( pAllTargetStatusChanges) > 0):
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
    
    _pRenderCursorButtons( 
        anOutput, 
        unContextualObject, 
        100, 
        aPortalURL,
        aCatalogoURL,
        fCGIE,
        mfCRs2BRs,
        mfTranslateI18N,
        mfAsUnicode,
        aTranslationsCache,
    )
    anOutput.write( u"""                                                                                                                                                                     
        <br/>
        \n""" 
    )
    
    return None





def _fWrapeableLinesString( theString, theMaxLength):
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




   
def _pRenderMessages( 
    anOutput, 
    unContextualObject,
    aPortalURL,
    aCatalogoURL,
    fCGIE,
    mfCRs2BRs,
    mfTranslateI18N,
    mfAsUnicode,
    aTranslationsCache) :
    

    anOutput.write( """
        <div id="cid_TRAMessages" class="TRAstyle_NoDisplay">
            <span id="TRAMessage_Confirmar_NavegarAIdiomaPrincipalYSimbolo">%(gvSIGi18n_Confirmar_NavegarAIdiomaPrincipalYSimbolo_msgid)s</span>
            <span id="TRAMessage_AsyncPhase_RequestQueued">%(gvSIGi18n_AsyncPhase_RequestQueued_msgid)s</span>
            <span id="TRAMessage_AsyncPhase_RequestSent">%(gvSIGi18n_AsyncPhase_RequestSent_msgid)s</span>
            <span id="TRAMessage_AsyncPhase_ResponseReceived">%(gvSIGi18n_AsyncPhase_ResponseReceived_msgid)s</span>
            <span id="TRAMessage_AsyncPhase_ChangeSaved">%(gvSIGi18n_AsyncPhase_ChangeSaved_msgid)s</span>
        </div>
        """ % aTranslationsCache
    )
    
    
    
    

    # #################################################################
    """Render internationalized constants for Javascript dialogs
    
    """
    anOutput.write( u"""     
                    
        <!-- #################################################################
        SECTION: Internationalized constants 
        ################################################################# -->
        <font color="White"> 
            <span id="cTRAId_ConfirmTranslateMsg"                    class="TRAstyle_NoDisplay">%(gvSIGi18n_ConfirmTranslateMsg)s</span>
            <span id="cTRAId_ReallyConfirmTranslateMsg"              class="TRAstyle_NoDisplay">%(gvSIGi18n_ReallyConfirmTranslateMsg)s</span>
            <span id="cTRAId_ConfirmStatusChangeMsg"                 class="TRAstyle_NoDisplay">%(gvSIGi18n_ConfirmStatusChangeMsg)s</span>
            <span id="cTRAId_ReallyConfirmStatusChangeMsg"           class="TRAstyle_NoDisplay">%(gvSIGi18n_ReallyConfirmStatusChangeMsg)s</span>
            <span id="cTRAId_ConfirmDeleteMsg"                       class="TRAstyle_NoDisplay">%(gvSIGi18n_ConfirmDeleteMsg)s</span>
            <span id="cTRAId_ReallyConfirmDeleteMsg"                 class="TRAstyle_NoDisplay">%(gvSIGi18n_ReallyConfirmDeleteMsg)s</span>
            <span id="cTRAId_ConfirmBatchMsg"                        class="TRAstyle_NoDisplay">%(gvSIGi18n_ConfirmBatchMsg)s</span>
            <span id="cTRAId_ReallyConfirmBatchMsg"                  class="TRAstyle_NoDisplay">%(gvSIGi18n_ReallyConfirmBatchMsg)s</span>
            <span id="cTRAId_ConfirmInvalidateStringTranslationsMsg" class="TRAstyle_NoDisplay">%(gvSIGi18n_ConfirmInvalidateStringTranslationsMsg)s</span>
            <span id="cTRAId_ReallyInvalidateStringTranslationsMsg"  class="TRAstyle_NoDisplay">%(gvSIGi18n_ReallyInvalidateStringTranslationsMsg)s</span>
            <span id="cTRAId_ConfirmDeactivateStringMsg"             class="TRAstyle_NoDisplay">%(gvSIGi18n_ConfirmDeactivateStringMsg)s</span>
            <span id="cTRAId_ReallyDeactivateStringMsg"              class="TRAstyle_NoDisplay">%(gvSIGi18n_ReallyDeactivateStringMsg)s</span>
            <span id="cTRAId_ConfirmActivateStringMsg"               class="TRAstyle_NoDisplay">%(gvSIGi18n_ConfirmActivateStringMsg)s</span>
            <span id="cTRAId_ReallyActivateStringMsg"                class="TRAstyle_NoDisplay">%(gvSIGi18n_ReallyActivateStringMsg)s</span>
            <span id="cTRAId_ModulesEditor_Open"                     class="TRAstyle_NoDisplay">%(gvSIGi18n_ModulesEditor_Open)s</span>
            <span id="cTRAId_ModulesEditor_Close"                    class="TRAstyle_NoDisplay">%(gvSIGi18n_ModulesEditor_Close)s</span>
        </font>
        \n""" % aTranslationsCache
    )
        
                     
    
    return None





    
def _pRenderCollapsibleTechnicalSections( 
    anOutput                   =None,
    unContextualObject         =None,      
    pRenderFormSubmit          =None,    
    pRenderRequest             =None,
    pRenderFullRequest         =None,      
    pRenderTimes               =None,
    pRenderProfile             =None,
    pRenderAsyncRequest        =None,        
    pRenderUserInterfaceEvents =None,                     
    pFormSubmit                =None,
    pStartTime                 =None,
    pEndTime                   =None,
    pBrowseDuration            =None,
    unHayCambio                =None,
    pChangeDuration            =None,
    unExecutionRecord          =None,    
    aRequestDumpString         =None,      
    aFullRequestDumpString     =None,             
    aPortalURL                 =None,
    aCatalogoURL               =None,
    fCGIE                      =None,
    mfCRs2BRs                  =None,
    mfTranslateI18N            =None,
    mfAsUnicode                =None,
    aTranslationsCache         =None, ):
    """Render as collapsible the technical sections of the translations browser.
    
    """
    
    
    if pRenderFormSubmit or  pRenderRequest or pRenderFullRequest or pRenderTimes or pRenderProfile or pRenderAsyncRequest or pRenderUserInterfaceEvents:
        _pRenderCollapsible_Lambda(  anOutput,
            'Technical',
            u'elid_Technical_collapsible_dl', 
            lambda : _pRenderTechnicalSections( 
                anOutput                   =anOutput,       
                unContextualObject         =unContextualObject,                 
                pRenderFormSubmit          =pRenderFormSubmit,                
                pRenderRequest             =pRenderRequest,             
                pRenderFullRequest         =pRenderFullRequest,                 
                pRenderTimes               =pRenderTimes,           
                pRenderProfile             =pRenderProfile,             
                pRenderAsyncRequest        =pRenderAsyncRequest,                  
                pRenderUserInterfaceEvents =pRenderUserInterfaceEvents,                        
                pFormSubmit                =pFormSubmit,          
                pStartTime                 =pStartTime,         
                pEndTime                   =pEndTime,       
                pBrowseDuration            =pBrowseDuration,              
                unHayCambio                =unHayCambio,          
                pChangeDuration            =pChangeDuration,              
                unExecutionRecord          =unExecutionRecord,                
                aRequestDumpString         =aRequestDumpString,                 
                aFullRequestDumpString     =aFullRequestDumpString,                    
                aPortalURL                 =aPortalURL,        
                aCatalogoURL               =aCatalogoURL,          
                fCGIE                      =fCGIE  ,   
                mfCRs2BRs                  =mfCRs2BRs,       
                mfTranslateI18N            =mfTranslateI18N,             
                mfAsUnicode                =mfAsUnicode,         
                aTranslationsCache         =aTranslationsCache,
            ),
            False,
        )
    
    return None        




           
 



def _pRenderTechnicalSections( 
    anOutput                   =None,
    unContextualObject         =None,      
    pRenderFormSubmit          =None,    
    pRenderRequest             =None,
    pRenderFullRequest         =None,      
    pRenderTimes               =None,
    pRenderProfile             =None,
    pRenderAsyncRequest        =None,        
    pRenderUserInterfaceEvents =None,                     
    pFormSubmit                =None,
    pStartTime                 =None,
    pEndTime                   =None,
    pBrowseDuration            =None,
    unHayCambio                =None,
    pChangeDuration            =None,
    unExecutionRecord          =None,    
    aRequestDumpString         =None,      
    aFullRequestDumpString     =None,             
    aPortalURL                 =None,
    aCatalogoURL               =None,
    fCGIE                      =None,
    mfCRs2BRs                  =None,
    mfTranslateI18N            =None,
    mfAsUnicode                =None,
    aTranslationsCache         =None, ):
    """Render the technical sections of the translations browser.
    
    """    
    
    anOutput.write("""
        <br/>
        \n"""
    )
    
    if pRenderUserInterfaceEvents:
        _pRenderCollapsible_Lambda(  anOutput,
            'User Interface Events',
            u'elid_UserInterfaceEvents_collapsible_dl', 
            lambda : _pRenderTechnical_UserInterfaceEvents( 
                anOutput, 
                unContextualObject, 
                aTranslationsCache,
            ),
            True,
        )
        anOutput.write("""
            <br/><br/>
            \n"""
        )
    
    
    if pRenderFormSubmit:
        _pRenderCollapsible_Lambda(  anOutput,
            'Form Submit',
            u'elid_FormSubmit_collapsible_dl', 
            lambda : _pRenderTechnical_FormSubmit( 
                anOutput, 
                unContextualObject, 
                pFormSubmit,
                aTranslationsCache,
            ),
            True,
        )
        anOutput.write("""
            <br/><br/>
            \n"""
        )
    
    if pRenderTimes:
        _pRenderCollapsible_Lambda(  anOutput,
            'Processing Times',
            u'elid_ProcessingTimes_collapsible_dl', 
            lambda : _pRenderTechnical_Times( 
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
        _pRenderCollapsible_Lambda(  anOutput,
            'Request Parameters',
            u'elid_RequestParameters_collapsible_dl', 
            lambda : _pRenderTechnical_Request( 
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
        _pRenderCollapsible_Lambda(  anOutput,
            'Full Request',
            u'elid_FullRequest_collapsible_dl', 
            lambda : _pRenderTechnical_Request( 
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
        _pRenderCollapsible_Lambda(  anOutput,
            'Async Request and Reply',
            u'elid_AsyncRequest_collapsible_dl', 
            lambda : _pRenderTechnical_AsyncRequest( 
                anOutput, 
                unContextualObject, 
                pRenderProfile,
                aTranslationsCache,
            ),
            True,
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






    
def _pRenderTechnical_AsyncRequest( 
    anOutput, 
    unContextualObject, 
    pRenderProfile,
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
         
    if pRenderProfile:
        anOutput.write( u""" 
            <span><strong>Last asynchcronous Execution Profile</strong> (if requested)</span>
            <br/>
            <div id="theTRAAsyncRequest_ExecutionProfile_Holder" />
            """
        )
    
    return None






    
def _pRenderTechnical_UserInterfaceEvents( 
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



 
    
def _pRenderTechnical_FormSubmit( 
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


        
        
def _pRenderTechnical_Times( 
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
            
           
            







def _pRenderTechnical_Request( 
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



















def _pRenderCursorButtons( 
    anOutput, 
    unContextualObject,  
    theFirstTabindex,
    aPortalURL,
    aCatalogoURL,
    fCGIE,
    mfCRs2BRs,
    mfTranslateI18N,
    mfAsUnicode,
    aTranslationsCache):
    """Render buttons to control the translations browser cursor.
    
    """
    
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
        'pAbsoluteURL':                                   aCatalogoURL,
        'gvSIGi18n_traducciones_bloquesiguiente_label' : aTranslationsCache[ 'gvSIGi18n_traducciones_bloquesiguiente_label'], 
        'gvSIGi18n_traducciones_iraprimero_label':       aTranslationsCache[ 'gvSIGi18n_traducciones_iraprimero_label'],
        'gvSIGi18n_traducciones_iraanterior_label':      aTranslationsCache[ 'gvSIGi18n_traducciones_iraanterior_label'],
        'gvSIGi18n_traducciones_irasiguiente_label':     aTranslationsCache[ 'gvSIGi18n_traducciones_irasiguiente_label'],
        'gvSIGi18n_traducciones_iraultimo_label':        aTranslationsCache[ 'gvSIGi18n_traducciones_iraultimo_label'],
        'gvSIGi18n_bloquesdea_parameter_label':          mfTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_bloquesdea_parameter_label', 'Block size-'), 
    })
            
    return None


     
            
            
  

        
