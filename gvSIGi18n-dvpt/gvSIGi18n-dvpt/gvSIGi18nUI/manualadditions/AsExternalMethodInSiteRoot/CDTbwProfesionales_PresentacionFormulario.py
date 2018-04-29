# -*- coding: utf-8 -*-
#
# File: CDTbwProfesionales_PresentacionFormulario.py
#
# Copyright (c) 2011  by Instituto Nacional de las Artes Escenicas y la Musica (INAEM) del Ministerio de Cultura (MCU) de Spain
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
# Instituto Nacional de las Artes Escenicas y la Musica (INAEM) del Ministerio de Cultura (MCU) de Spain <centro.documentacion.teatral@inaem.mcu.es>  
# Antonio Carrasco Valero                       <carrasco@ModelDD.org>
#
#
__author__ = """Instituto Nacional de las Artes Escenicas y la Musica (INAEM) del Ministerio de Cultura (MCU) de Spain <centro.documentacion.teatral@inaem.mcu.es>, 
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'



import cgi



# from codecs                 import lookup           as CODECS_Lookup
from codecs                 import EncodedFile      as CODECS_EncodedFile


from StringIO import StringIO

from DateTime import DateTime


from Products.CMFCore.utils import getToolByName



# from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fMillisecondsNow





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





# ######################################
"""Utility methods.

"""
   
def fAsCollection( theObject):
    
    if theObject == None:
        return []
    
    if isinstance( theObject, list):
        return theObject
    
    if isinstance( theObject, tuple):
        return list ( theObject)
    
    if isinstance( theObject, set):
        return list ( theObject)
    
    return [ theObject,]        
    
    



def fCRs2BRs( theString):
    if not theString:
        return theString
    if theString.__class__.__name__ == 'unicode':
        return theString.replace( u'\n', u'<br/>')
    
    return theString.replace( '\n', '<br/>')

    





# ######################################
"""Encoding methods.

"""




def fCGIE(theString, quote=1):
    """ Utility to escape strings written as HTML.
    
    """
    if not theString:
        return theString
    return cgi.escape( theString, quote=quote)





def fAsUnicode( theContextualElement, theString, theTranslationService=None):
    """Return the parameter, expected to be encoded in the plone site default encoding, decoded into a unicode string.
    
    """
    
    if not theString:
        return u''
    
    if theContextualElement == None:
        return u''
    
    aTranslationService = theTranslationService
    if not aTranslationService:
        aTranslationService = getTranslationServiceTool( theContextualElement)
        if not aTranslationService:
            return u''
        

    aUnicodeString = u''
    try:
        aUnicodeString = aTranslationService.asunicodetype( theString, errors="ignore")
    except:
        None
    
    return aUnicodeString
    
      



# ######################################
"""Localization methods.

"""

def getTranslationServiceTool( theContextualElement, ):
    if theContextualElement == None:
        return None
    return getToolByName( theContextualElement, 'translation_service', None)
    

def fTranslateI18NCGIE( theContextualElement, theDomain, theSymbol, theDefault):
    """ Utility to translate symbols and scape for HTML
    
    """
    return fCGIE( 
        fTranslateI18N( 
            theContextualElement=theContextualElement, 
            theI18NDomain=theDomain, 
            theString=theSymbol, 
            theDefault=theDefault, 
            theTranslationService=None,
        )
    )







def fTranslateI18N( 
    theContextualElement,
    theI18NDomain, 
    theString, 
    theDefault, 
    theTranslationService=None):
    """Localization: return the translated string from the specific domain into the language preferred by the connected user, or return the supplied default.
    
    """
 
    if theContextualElement == None:
        return unicode( theDefault)
    
    if not theString:
        return unicode( theDefault)

    if not theI18NDomain:
        return unicode( theDefault)

    
    aTranslationService = theTranslationService
    if not aTranslationService:
        aTranslationService = getTranslationServiceTool( theContextualElement)
        if not aTranslationService:
            return unicode( theDefault)
        
        
    aTranslation = aTranslationService.utranslate( 
        theI18NDomain, 
        theString, 
        mapping=None, 
        context=theContextualElement , 
        target_language= None, 
        default=theDefault
    )            
    if not aTranslation:
        aTranslation = unicode( theDefault)

    if not aTranslation:
        aTranslation = unicode( theString)

    return aTranslation
        
    
    

def fTranslateI18NManyIntoDict( 
    theContextualElement,
    theI18NDomainsStringsAndDefaults=[], 
    theResultDict                   =None,
    theTranslationService           =None,):
    """Internationalization: build or update a dictionaty with the translations of all requested strings from the specified domain into the language preferred by the connected user, or return the supplied default.
    
    """
    
    unResultDict = theResultDict
    if ( unResultDict == None):
        unResultDict = { }
            
    if not theI18NDomainsStringsAndDefaults:
        return unResultDict
    
    if theContextualElement == None:
        return unResultDict
    
    
    
    aTranslationService = theTranslationService
    if not aTranslationService:
        aTranslationService = getTranslationServiceTool(theContextualElement)
        if not aTranslationService:
            return unResultDict
        
        

    
    for aDomainStringsAndDefaults in theI18NDomainsStringsAndDefaults:
        aI18NDomain             = aDomainStringsAndDefaults[ 0] or cI18NDomainDefault
        unasStringsAndDefaults  = aDomainStringsAndDefaults[ 1]
        
        for unaStringAndDefault in unasStringsAndDefaults:
            unaString = unaStringAndDefault[ 0]
            unDefault = unaStringAndDefault[ 1]
            if unaString:
                aTranslation = u''
                if aTranslationService:
                    aTranslation = aTranslationService.utranslate( 
                        aI18NDomain, 
                        unaString, 
                        mapping=None, 
                        context=theContextualElement, 
                        target_language= None, 
                        default=unDefault
                    )            
                if not aTranslation:
                    aTranslation = self.fAsUnicode( unDefault)
                unResultDict[ unaString] = aTranslation
                    
    return unResultDict
            
    








# ######################################
"""Portal and URL methods.

"""



def fPortalURL( theContextualElement, ):

    unPortalURLTool = getToolByName( theContextualElement, 'portal_url', None)
    if not unPortalURLTool:
        return ''
    
    unPortalURL = ''
    try:
        unPortalURL = unPortalURLTool()
    except: 
        None
    if not unPortalURL:
        return ''
    
    return unPortalURL
        


def fPortalRoot( theContextualElement,):
    unPortalTool = getToolByName( theContextualElement, 'portal_url', None)
    if not unPortalURLTool:
        return None
    
    unPortal = aPortalTool.unPortalTool()
    return unPortal       
    
    


    
def fElementoAbsoluteURL(self, 
    theContextualElement    =None,):
    
    if theContextualElement == None:
        return ''
    
    return theContextualElement.absolute_url()
        





# ######################################
"""Time methods.

"""


def fSecondsNow():   

    return int( time())


    
def fMillisecondsNow():   

    return int( time() * 1000)



def fDateTimeNow():   
    return DateTime()




def fDateTimeAfterSeconds( theDateTime, theSeconds):

    if not theDateTime:
        return None

    if not theSeconds:
        return theDateTime
    
    unaDateTimeAfter = DateTime( ( theDateTime.millis() / 1000) + int( theSeconds))
        
    return unaDateTimeAfter

         
    
def fMillisecondsToDateTime( theMilliseconds):
    
    if not theMilliseconds:
        return None
    
    if isinstance( theMilliseconds, DateTime):
        return theMilliseconds
    
    unDateTime = None
    try:
        unDateTime = DateTime( theMilliseconds / 1000)
    except:
        None
        
    return unDateTime





def fObtenerConfiguracionDict( 
    theContextualElement     =None, 
    theAspectoConfiguracion  =None):
    
    if theContextualElement == None:
        return {}
    
    unConfigurationDict =  {
    }
    return unConfigurationDict





cResultCondition_MissingParameter_CDTbwProfesionales          = "ResultCondition_MissingParameter_CDTbwProfesionales"
cResultCondition_MissingParameter_Request                     = "ResultCondition_MissingParameter_Request"
cResultCondition_ErrorInternal_Missing_TranslationServiceTool = "ResultCondition_ErrorInternal_Missing_TranslationServiceTool"

cDefaultResultadosPorPagina = 10

cConfiguracion_PaginaResultados = 'Configuracion_PaginaResultados'

cConfiguracion_PaginaResultados_ResultadosPorPaginaPorDefecto = 'ResultadosPorPaginaPorDefecto'




cRequestParameter_Generic_GoTo                      = 'elGoTo'
cRequestParameter_Generic_GoToResultIndex           = 'elGoToResultIndex'
cRequestParameter_Generic_GoToPageIndex             = 'elGoToPageIndex'
cRequestParameter_Generic_GoToStartingWith          = 'elGoToStartingWith'
cRequestParameter_Generic_SortOrder                 = 'elSortOrder'
cRequestParameter_Generic_ResultadosPorPagina       = 'elResultadosPorPagina'
cRequestParameter_Generic_RenderFormSubmit          = 'elRenderFormSubmit'
cRequestParameter_Generic_RenderRequest             = 'elRenderRequest'
cRequestParameter_Generic_RenderFullRequest         = 'elRenderFullRequest'
cRequestParameter_Generic_RenderTimes               = 'elRenderTimes'
cRequestParameter_Generic_RenderAsyncRequest        = 'elRenderAsyncRequest'
cRequestParameter_Generic_RenderUserInterfaceEvents = 'elRenderUserInterfaceEvents'




cRequestParameter_Profesionales_Nombres     = 'Profesionales_Nombres'
cRequestParameter_Profesionales_Profesiones = 'Profesionales_Profesiones'
cRequestParameter_Profesionales_Sexos       = 'Profesionales_Sexos'

cRequestParameters_specific = [
    cRequestParameter_Profesionales_Nombres,    
    cRequestParameter_Profesionales_Profesiones,
    cRequestParameter_Profesionales_Sexos,      
]



def CDTbwProfesionales_PresentacionFormulario( 
    theRequest, 
    theCDTbwProfesionales   =None, 
    theThruCtxt             =None, 
    theParentExecutionRecord=None):
    """Servicio principal para presentar el formulario de busquedas de Profesionales.
    
    Entry point invoked from a template.
    
    """
    if theThruCtxt == None:
        theThruCtxt = { }
        
        
    aPortalURL                    = ''
    aCDTbwProfesionalesURL        = ''
    
    
    if theCDTbwProfesionales == None:
        return _pEmptyPageContents(  
            unContextualObject      =theCDTbwProfesionales,                                                                                                                          
            unHeader                =fTranslateI18NCGIE( 'CDTbusquedasWeb', cResultCondition_MissingParameter_CDTbwProfesionales, cResultCondition_MissingParameter_CDTbwProfesionales + '-'), 
            unMessage               ='theCDTbwProfesionales',                                                                                                               
            aPortalURL              =aPortalURL,                                                                                                                  
            aCDTbwProfesionalesURL  =aCDTbwProfesionalesURL,                                                                                                                  
            theThruCtxt             =theThruCtxt,                                                                                                                   
        )    
   
    

    aPortalURL             = fPortalURL( theContextualElement)   
    aCDTbwProfesionalesURL = fElementoAbsoluteURL( theContextualElement=theCDTbwProfesionales)
            
    if not theRequest:
        return _pEmptyPageContents( 
            unContextualObject      =theCDTbwProfesionales,                                                                                                                          
            unHeader                =fTranslateI18NCGIE( 'CDTbusquedasWeb', cResultCondition_MissingParameter_Request, cResultCondition_MissingParameter_Request + '-'), 
            unMessage               ='theRequest',                                                                                                               
            aPortalURL              =aPortalURL,                                                                                                                  
            aCDTbwProfesionalesURL  =aCDTbwProfesionalesURL,                                                                                                                  
            theThruCtxt             =theThruCtxt,                                                                                                                                    
        )
     
    
    aTranslationService = getTranslationServiceTool( theContextualElement=theCDTbwProfesionales)
    if aTranslationService == None:
        return _pEmptyPageContents(  
            unContextualObject      =theCDTbwProfesionales,                                                                                                                          
            unHeader                =fTranslateI18NCGIE( 'CDTbusquedasWeb', cResultCondition_ErrorInternal_Missing_TranslationServiceTool, cResultCondition_ErrorInternal_Missing_TranslationServiceTool + '-'), 
            unMessage               ='getTranslationServiceTool',                                                                                                               
            aPortalURL              =aPortalURL,                                                                                                                  
            aCDTbwProfesionalesURL  =aCDTbwProfesionalesURL,                                                                                                                  
            theThruCtxt             =theThruCtxt,                                                                                                                                    
        )
    
    

    
    
        
    
    anOutput = StringIO()
    
    pRenderProfile    = theRequest.get( 'theRenderProfile', '') == 'on'
    
    
    try:
            
            
        
        pStartTime = fMillisecondsNow()
        

         
        
        
        # #################################################################
        """Cache some translations to be used in the rendering below

        """
        
        aTranslationsCache = {}
        _pInitTranslationsCache( 
            theCDTbwProfesionales, 
            aTranslationService,    
            aTranslationsCache
        )
       
        
                
        
        unaConfiguracionPaginaResultadosDict = fObtenerConfiguracionDict( 
            theContextualElement     =theCDTbwProfesionales, 
            theAspectoConfiguracion  =cConfiguracion_PaginaResultados,
        )
        #unaConfiguracionPaginaResultadosDict = theCDTbwProfesionales.fObtenerConfiguracionDict( 
            #theContextualElement     =theCDTbwProfesionales, 
            #theAspectoConfiguracion  =cConfiguracion_PaginaResultados,
        #)

        unosResultadosPorPagina = cDefaultResultadosPorPagina
        
        if not ( unaConfiguracionPaginaResultadosDict == None):
            unosResultadosPorPagina = unaConfiguracionPaginaResultadosDict.get( cConfiguracion_PaginaResultados_ResultadosPorPaginaPorDefecto, cDefaultResultadosPorPagina)
        
            
            
            
        
        # ################################################################
        """Retrieve generic Request parameter values.
        
        """

        pRequestParameters = { }

        pRequestParameters[ cRequestParameter_Generic_GoTo]                         = theRequest.get( cRequestParameter_Generic_GoTo,                      '')
        pRequestParameters[ cRequestParameter_Generic_GoToStartingWith]             = theRequest.get( cRequestParameter_Generic_GoToStartingWith,          '')
        pRequestParameters[ cRequestParameter_Generic_SortOrder]                    = theRequest.get( cRequestParameter_Generic_SortOrder,                 '')
        pRequestParameters[ cRequestParameter_Generic_ResultadosPorPagina]          = theRequest.get( cRequestParameter_Generic_ResultadosPorPagina,       str( unosResultadosPorPagina)) 
        pRequestParameters[ cRequestParameter_Generic_RenderFormSubmit]             = theRequest.get( cRequestParameter_Generic_RenderFormSubmit,          '') == 'on'
        pRequestParameters[ cRequestParameter_Generic_RenderRequest]                = theRequest.get( cRequestParameter_Generic_RenderRequest,             '') == 'on'
        pRequestParameters[ cRequestParameter_Generic_RenderFullRequest]            = theRequest.get( cRequestParameter_Generic_RenderFullRequest,         '') == 'on'
        pRequestParameters[ cRequestParameter_Generic_RenderTimes]                  = theRequest.get( cRequestParameter_Generic_RenderTimes,               '') == 'on'
        pRequestParameters[ cRequestParameter_Generic_ResultadosPorPagina]          = theRequest.get( cRequestParameter_Generic_RenderAsyncRequest,        '') == 'on'
        pRequestParameters[ cRequestParameter_Generic_RenderUserInterfaceEvents]    = theRequest.get( cRequestParameter_Generic_RenderUserInterfaceEvents, '') == 'on'




        aGoToResultIndex = 0
        aGoToResultIndexStr      = theRequest.get( cRequestParameter_Generic_GoToResultIndex, '')
        if aGoToResultIndexStr:
            try:
                aGoToResultIndex = int( aGoToResultIndexStr)
            except:
                None                
        pRequestParameters[ cRequestParameter_Generic_GoToResultIndex] = aGoToResultIndex
                
        aGoToPageIndex = 0
        aGoToPageIndexStr       = theRequest.get( cRequestParameter_Generic_GoToPageIndex,  '')
        if aGoToPageIndexStr:
            try:
                aGoToPageIndex = int( aGoToPageIndexStr)
            except:
                None
        pRequestParameters[ cRequestParameter_Generic_GoToPageIndex] = aGoToPageIndex

        
        
        
                
                   
                
        # ################################################################
        """Retrieve specific Request parameter values.
        
        """        
        pRequestParameters[ cRequestParameter_Profesionales_Nombres]          = fAsCollection( theRequest.get( cRequestParameter_Profesionales_Nombres,     []) or [])        
        pRequestParameters[ cRequestParameter_Profesionales_Profesiones]      = fAsCollection( theRequest.get( cRequestParameter_Profesionales_Profesiones, []) or [])
        pRequestParameters[ cRequestParameter_Profesionales_Sexos]            = fAsCollection( theRequest.get( cRequestParameter_Profesionales_Sexos,       []) or [])
                
                
     
        
        
        # ################################################################
        """Capture Request dump strings
        
        """
        aRequestDumpString      = ''
        aFullRequestDumpString  = ''
        if pRenderRequest or pRenderFullRequest:
            aRequestDumpString, aFullRequestDumpString = _pRequestStrings( 
                theCDTbwProfesionales, 
                theRequest, 
                pRenderRequest, 
                pRenderFullRequest, 
                aPortalURL,
                aCDTbwProfesionalesURL,
                theThruCtxt,
            ) 
        
      
     
      
        
        # #################################################################
        """Extract and process general information like the dictionary of language names and flags
        
        """
        
        pLanguagesNamesAndFlags  = pServiceResponse.get( 'languages_names_and_flags', {})
        

        
                            
            

        # #################################################################
        """RENDERING of the various sections of the translations browser/editor
            
        Including:
        Filter criteria editor.
        Query Progress indicator.
        Summary report.
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
            <div class="CDTbwStyle_NoDisplay"> 
                <span id="cId_AllowRemoveStringsModules"        class="CDTbwStyle_NoDisplay">%(CDTbusquedasWeb_AllowRemoveStringsModules)s</span>
            </div>
            \n""" % { 
            'CDTbusquedasWeb_AllowRemoveStringsModules':       '',
            }
        )


    
        # #################################################################
        """Render program constants: portal URL for scripts to compose URLs for icons, and the URL for asynch requests
        
        """
        anOutput.write( u"""     
                        
            <!-- #################################################################
            SECTION: Portal URL and URL for Asynch requests
            ################################################################# -->
            <div class="CDTbwStyle_NoDisplay"> 
                <span id="cId_PortalURL" class="CDTbwStyle_NoDisplay">%(PortalURL)s</span>
                <span id="cId_AsynchRequestURL" class="CDTbwStyle_NoDisplay">%(AsynchRequestURL)s</span>
            </div>
            \n""" % { 
            'PortalURL':        '%s'                          % aPortalURL,
            'AsynchRequestURL': '%s/CDTbwProfesionales_async' % aCDTbwProfesionalesURL,
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
            theCDTbwProfesionales,
            theThruCtxt             =theThruCtxt,                                                                                                                                    
        )   
        
        
        _pRenderStyles(            
            anOutput, 
            theCDTbwProfesionales, 
            theThruCtxt             =theThruCtxt,                                                                                                                                    
        ) 
                
            
            
            
        anOutput.write( u"""                 
      
            <!-- #################################################################
            SECTION: Hidden fields to maintain and communicate whether the form may have hanged
            ################################################################# -->
                     

            <input type="hidden" name="theMayHaveChanged"               id="theMayHaveChanged"              value="%(can_change)s" /> 
            \n""" % { 
            'can_change':  (( pTargetStatusChanges or pCanComment) and '1') or '0', 
        } )
     
                        
       
        _pRenderCabecera( 
            anOutput                =anOutput,               
            unContextualObject      =theCDTbwProfesionales,            
            aPortalURL              =aPortalURL,             
            aCDTbwProfesionalesURL  =aCDTbwProfesionalesURL,           
            theThruCtxt             =theThruCtxt,                                                                                                                                       
        )
        
                


        
        _pRenderCollapsibleFiltro( 
            anOutput                =anOutput,            
            unContextualObject      =theCDTbwProfesionales,         
            pSearchParameters       =pRequestParameters,   
            aPortalURL              =aPortalURL,          
            aCDTbwProfesionalesURL  =aCDTbwProfesionalesURL,        
            theThruCtxt             =theThruCtxt,
        )
        
        unosResultadosPorPagina = 1
        try:
            unosResultadosPorPagina = int( pResultadosPorPagina)
        except:
            None
            
        _pRenderCollapsibleGoTo( 
            anOutput               =anOutput,                                                                                                                
            unContextualObject     =theCDTbwProfesionales,                                                                                                             
            pSearchParameters      =pRequestParameters,                                                                                                       
            aPortalURL             =aPortalURL,                                                                                                              
            aCDTbwProfesionalesURL =aCDTbwProfesionalesURL,                                                                                                            
            theThruCtxt            =theThruCtxt,                                                                                                                   
        )
                
        
          
        _pRenderCollapsibleInforme( 
            anOutput                    =anOutput,
            unContextualObject          =theCDTbwProfesionales,
            aPortalURL                  =aPortalURL,
            aCDTbwProfesionalesURL      =aCDTbwProfesionalesURL,
            theThruCtxt                 =theThruCtxt,                                                                                                                   
        )
    
        
                                               
                
        _pRenderCollapsibleList( 
            anOutput                 =anOutput,                                    
            unContextualObject       =theCDTbwProfesionales,                                                         
            pSearchParameters        =pRequestParameters,                                                                                                       
            aPortalURL               =aPortalURL,                                                                         
            aCDTbwProfesionalesURL   =aCDTbwProfesionalesURL,                        
            theThruCtxt              =theThruCtxt,                                                                                                                   
        )
   
             
       
            
                
                
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
            'pSimboloUltimaCadenaEnBloque': fAsUnicode( ''), 
            'pSimboloCadenaATraducir':      fAsUnicode( ''), 
            'pSimboloCadenaCursor':         fAsUnicode( ''),
            'pCodigoIdiomaCursor':          fAsUnicode( ''),  
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
            

                   
        anOutput.write( u"""  
            </form>
            \n""" 
        )                    
            
            
        anOutput.write( u"""  
            <!-- #################################################################
            SECTION: Hidden elements to temporarily store the html content received in the asynchronous response
            ################################################################# -->
            
            <div class="CDTbwStyle_NoDisplay" id="cid_CDTbwAsyncResponseStore" >
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
            unContextualObject =theCDTbwProfesionales,                    
            aPortalURL         =aPortalURL,       
            aCDTbwProfesionalesURL       =aCDTbwProfesionalesURL,       
            fCGIE              =theThruCtxt,            
            fCRs2BRs          =fCRs2BRs,        
            fTranslateI18NCGIE    =fTranslateI18NCGIE,          
            fAsUnicode        =fAsUnicode,      
            aTranslationsCache =aTranslationsCache,
        )
            
        pEndTime = fMillisecondsNow()
            
            
        _pRenderCollapsibleTechnicalSections( 
            anOutput                   =anOutput,                  
            unContextualObject         =theCDTbwProfesionales,                     
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
            aCDTbwProfesionalesURL               =aCDTbwProfesionalesURL,              
            fCGIE                      =theThruCtxt,                     
            fCRs2BRs                  =fCRs2BRs,                 
            fTranslateI18NCGIE            =fTranslateI18NCGIE,           
            fAsUnicode                =fAsUnicode,               
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
    aCDTbwProfesionalesURL,
    theThruCtxt,):
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
    aTranslationService,    
    aTranslationsCache):
    """Preload some translations into cache.
    
    """

    
    someDomainsStringsAndDefaultsToTranslate = [
        [ 'CDTbusquedasWeb', [    
            
            [ 'CDTbusquedasWeb_Confirmar_NavegarAIdiomaPrincipalYSimbolo_msgid', 'Please confirm that you want to navigate away from this language into the selected string in a different language-',],
            [ 'CDTbusquedasWeb_AsyncPhase_RequestQueued_msgid',     'Request Queued.-',],
            [ 'CDTbusquedasWeb_AsyncPhase_RequestSent_msgid',       'Request Sent.-',],
            [ 'CDTbusquedasWeb_AsyncPhase_ResponseReceived_msgid',  'Response Received.-',],
            [ 'CDTbusquedasWeb_AsyncPhase_ChangeSaved_msgid',       'Change Saved.-',],
            
            [ 'CDTbusquedasWeb_traducciones_bloquesiguiente_label',           'Next-' ,],                                                               
            [ 'CDTbusquedasWeb_editor_label',                                 'Editor-' ,],                                                                                   
            [ 'CDTbusquedasWeb_detalle_label',                                'Detail-' ,],                                                                                  
            [ 'CDTbusquedasWeb_noreadpermission_warning',                     'Warning: you do not have read permission.-' ,],                                    
            [ 'CDTbusquedasWeb_extralangs_parameter_label',                   'Extra langs.-' ,],                                                               
            [ 'CDTbusquedasWeb_traducciones_iraprimero_label',                'Go To First-' ,],                                                             
            [ 'CDTbusquedasWeb_traducciones_iraanterior_label',               'Go To Previous-' ,],                                                         
            [ 'CDTbusquedasWeb_traducciones_irasiguiente_label',              'Go To Next-' ,],                                                            
            [ 'CDTbusquedasWeb_traducciones_iraultimo_label',                 'Go To Last-' ,],                                                               
            [ 'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_label',    'State-' ,],                                                       
            [ 'CDTbusquedasWeb_TRATraduccion_attr_fechaCreacionTextual_label','Creation Date-' ,],                                            
            [ 'CDTbusquedasWeb_TRATraduccion_attr_usuarioCreador_label',     'Creator-' ,],                                                  
            [ 'CDTbusquedasWeb_TRATraduccion_attr_fechaTraduccionTextual_label','Translation Date-' ,],                                            
            [ 'CDTbusquedasWeb_TRATraduccion_attr_usuarioTraductor_label',    'Translator-' ,],                                                  
            [ 'CDTbusquedasWeb_TRATraduccion_attr_fechaRevisionTextual_label','Revision Date-' ,],                                               
            [ 'CDTbusquedasWeb_TRATraduccion_attr_usuarioRevisor_label',      'Reviewer-' ,],                                                    
            [ 'CDTbusquedasWeb_TRATraduccion_attr_fechaDefinitivoTextual_label','Definitive Date-' ,],                                             
            [ 'CDTbusquedasWeb_TRATraduccion_attr_usuarioCoordinador_label',  'Coordinator-' ,],                                                 
            [ 'CDTbusquedasWeb_TRATraduccion_attr_fechaModificacionTextual_label','Change Date-' ,],                                             
            [ 'CDTbusquedasWeb_TRATraduccion_attr_usuarioModificador_label',  'Change User-' ,],  
            [ 'CDTbusquedasWeb_Modificacion',                                 'Modification-' ,],  
            [ 'CDTbusquedasWeb_usuario_label',                                'User-' ,],                                                        
            [ 'CDTbusquedasWeb_ocultar_action_label',                         'Hide-' ,],                                                       
            [ 'CDTbusquedasWeb_TRATraduccion_attr_historia_label',            'History-' ,],                                                    
            [ 'CDTbusquedasWeb_historiafechaaccion_label',                    'Action Date-' ,],                                                
            [ 'CDTbusquedasWeb_historiausuarioactor_label',                   'Actor User-' ,],                                                 
            [ 'CDTbusquedasWeb_editar_action_label',                          'Edit-' ,],                                                       
            [ 'CDTbusquedasWeb_TRATraduccion_attr_simbolo_label',             'Symbol-' ,],                                                     
            [ 'CDTbusquedasWeb_TRATraduccion_attr_cadenaTraducida_label',     'Translation-' ,],                                                
            [ 'CDTbusquedasWeb_valoractualtraduccion_title',                  'Current-' ,],                                                  
            [ 'CDTbusquedasWeb_nuevovalortraduccion_title',                   'New-' ,],                                                        
            [ 'CDTbusquedasWeb_TRACadena_attr_id_label',                      'String Id-' ,],   
            [ 'CDTbusquedasWeb_TRATraduccion_attr_contadorCambios_label',     'Changes Counter-' ,],   
            [ 'CDTbusquedasWeb_TRATraduccion_attr_comentario_label',          'Comment-' ,],                                                    
            [ 'CDTbusquedasWeb_comentar_action_label',                        'Comment-' ,],                                                                  
            [ 'CDTbusquedasWeb_TRATraduccion_attr_nombresModulos_label',      'Modules-' ,],                                                    
            [ 'CDTbusquedasWeb_nosehanencontradotraducciones_message',        'No translations have been found matching the specified criteria.-' ,], 
            [ 'CDTbusquedasWeb_haHabidoCambioTraduccion_msg',                 'Translation has been changed.-' ,],  
            [ 'CDTbusquedasWeb_lista_section_label',                          'List-' ,],
            [ 'CDTbusquedasWeb_TranslationAction_Borrar',                     'Delete-',],
            [ 'CDTbusquedasWeb_TranslationAction_Grabar',                     'Save-',],
            [ 'CDTbusquedasWeb_TranslationAction_Revisar',                    'Review-',],
            [ 'CDTbusquedasWeb_TranslationAction_Bloquear',                   'Lock-',],
            [ 'CDTbusquedasWeb_TranslationAction_Abrir',                      'Open-',],
            [ 'CDTbusquedasWeb_idioma_msgid',                                 'Language-',],
            [ 'CDTbusquedasWeb_Estado_label',                                 'Status-',],
            [ 'CDTbusquedasWeb_ColumnaSimboloColapsable_Action_Hide_help',    'Click to hide this column-',],
            [ 'CDTbusquedasWeb_ColumnaSimboloColapsable_Action_Show_help',    'Click here to show the column with symbols',],
            [ 'CDTbusquedasWeb_idiomasSection_title',                         'Reference Languages-', ],
            [ 'CDTbusquedasWeb_seccionesSection_title',                       'Sections-', ],
            [ 'CDTbusquedasWeb_seccionFiltro_title',                          'Filter-', ],
            [ 'CDTbusquedasWeb_seccionInformeSumario_title',                  'Summary-', ],
            [ 'CDTbusquedasWeb_seccionList_title',                            'List-', ],
            [ 'CDTbusquedasWeb_AsynchronousTranslationMode_label',            'Send changes to server without refreshing the whole page-', ],
            [ 'CDTbusquedasWeb_refrescar_action_label',                       'Refresh-', ],
            [ 'CDTbusquedasWeb_TranslationsPerPage_label',                    'Number of translations in each page-',],
            [ 'CDTbusquedasWeb_AppliesImmediatelyNoNeedToRefresh_help',       'Applies immediately, no need to refresh the page to make it effective.-',],
            [ 'CDTbusquedasWeb_opcionesSection_title',                        'Options-',],
            [ 'CDTbusquedasWeb_fecha_el',                                     'on-',],
            [ 'CDTbusquedasWeb_usuario_por',                                  'by-',],
            [ 'CDTbusquedasWeb_TRATraduccion_Creada',                         'Created-',],
            [ 'CDTbusquedasWeb_ShowEditorDetails_label',                      'Display translation details in the editor',], 
            [ 'CDTbusquedasWeb_PresentationOptions_NoNeedToRefresh_label',    'Options that do not require refreshing the page',],             
            [ 'CDTbusquedasWeb_PresentationOptions_MustRefresh_label',        'Options that require refreshing the page',], 
            [ 'CDTbusquedasWeb_InteractionMode_label',                        'Server interaction mode-',],                
            [ 'CDTbusquedasWeb_InteractionMode_Asynchronous_label',           'Asynchronous-',],                
            [ 'CDTbusquedasWeb_InteractionMode_Asynchronous_help',            'Send changes to server without refreshing the whole page, allowing continuation of work in the current page.-',],                
            [ 'CDTbusquedasWeb_InteractionMode_Synchronous_label',            'Synchronous-',],                
            [ 'CDTbusquedasWeb_InteractionMode_Synchronous_help',             'Send changes to server by loading a completely new page-',],     
            [ 'CDTbusquedasWeb_newStatus_title',                              'New Status-',],
            [ 'CDTbusquedasWeb_AppliesOnSelectonForEditionNoNeedToRefresh_help', 'Applies as soon as you select a translation for edition, no need to refresh the page to make it effective.-',],
            [ 'CDTbusquedasWeb_fromToIn_from_label',                          'from-',],
            [ 'CDTbusquedasWeb_fromToIn_to_label',                            'to-',],
            [ 'CDTbusquedasWeb_fromToIn_in_label',                            'of-',],
            [ 'CDTbusquedasWeb_BatchNewStatus_title',                         'Batch Status Change-',],
            [ 'CDTbusquedasWeb_Batch_ButtonLabel',                            'Batch-',],
            [ 'CDTbusquedasWeb_TranslationAction_InvalidarResultadosCadena_label', 'Invalidate',],
            [ 'CDTbusquedasWeb_TranslationAction_InvalidarResultadosCadena_help', 'Invalidate String Translations into all languages-',],
            [ 'CDTbusquedasWeb_ToAvoidConfirmationDialogsCheckDoNotConfirmOptionMsg', 'To avoid confirmation dialogs, check the Do not confirm ... box in Options-',],
            [ 'CDTbusquedasWeb_ConfirmInvalidateStringTranslationsMsg',        'Do you want to INVALIDATE the String Translations into all languages-',],
            [ 'CDTbusquedasWeb_ReallyInvalidateStringTranslationsMsg',         'Do you REALLY want to INVALIDATE the String Translations into all languages-',],
            [ 'CDTbusquedasWeb_ConfirmTranslateMsg',                           'Do you want to CHANGE the string TRANSLATION-',],
            [ 'CDTbusquedasWeb_ReallyConfirmTranslateMsg',                     'Do you REALLY want to CHANGE the string TRANSLATION-',],
            [ 'CDTbusquedasWeb_ConfirmStatusChangeMsg',                        'Do you want to CHANGE STATUS of the Translation-',],
            [ 'CDTbusquedasWeb_ReallyConfirmStatusChangeMsg',                  'Do you REALLY want to CHANGE STATUS of the Translation-',],
            [ 'CDTbusquedasWeb_ConfirmDeleteMsg',                              'Do you want to DELETE string Translation-',],
            [ 'CDTbusquedasWeb_ReallyConfirmDeleteMsg',                        'Do you REALLY want to DELETE the string Translation-',],
            [ 'CDTbusquedasWeb_ConfirmBatchMsg',                               'Do you want to apply BATCH to ALL the SELECTED translations-',],
            [ 'CDTbusquedasWeb_ReallyConfirmBatchMsg',                         'Do you REALLY want to apply BATCH to ALL the SELECTED translations-',],
            [ 'CDTbusquedasWeb_InteracionStatusMessage',                       'Interaction Status Message-',],
            [ 'CDTbusquedasWeb_TranslationAction_DesactivarCadena_label',      'Deactivate String-',],
            [ 'CDTbusquedasWeb_TranslationAction_DesactivarCadena_help',       'Hide String symbol from all translation activity and all exports.-',],
            [ 'CDTbusquedasWeb_TranslationAction_ActivarCadena_label',         'Activate String-',],
            [ 'CDTbusquedasWeb_TranslationAction_ActivarCadena_help',          'Make String symbol available for translation activity and exports.-',],
            [ 'CDTbusquedasWeb_ConfirmDeactivateStringMsg',                    'Do you want to DEACTIVATE the String, hiding it from all Translation activity and exports-',],
            [ 'CDTbusquedasWeb_ReallyDeactivateStringMsg',                     'Do you REALLY want to DEACTIVATE the String, hiding it from all Translation activity and exports-',],
            [ 'CDTbusquedasWeb_ConfirmActivateStringMsg',                      'Do you want to ACTIVATE the String, making it available for Translation and export-',],
            [ 'CDTbusquedasWeb_ReallyActivateStringMsg',                       'Do you REALLY want to ACTIVATE the String, making it available for Translation and export-',],
            [ 'CDTbusquedasWeb_BrowsingInactiveStrings_label',                 'Browsing Strings in Inactive State-',],
            [ 'CDTbusquedasWeb_BrowsingInactive_collapsibleListLabel',         'Inactive-',],
            [ 'CDTbusquedasWeb_ModulesEditor_Open',                            'Edit-',],
            [ 'CDTbusquedasWeb_ModulesEditor_Close',                           'Cancel-',],
            [ 'CDTbusquedasWeb_ModulesEditor_SaveStringModules',               'Save String Modules-',],
            [ 'CDTbusquedasWeb_refrescar_action_label',                        'Refresh-',],
            [ 'CDTbusquedasWeb_todas_label',                                   'All-',],
            [ 'CDTbusquedasWeb_TranslationsFilter_help',                       'You may enter conditions for translations to match.\nAll conditions shall be met (AND logic, set intersection).\nClick Refresh button to update the list.-',],
            [ 'CDTbusquedasWeb_TranslationsFilter_Reset_help',                 'You may retrieve all the translations\nresetting the filter, by clicking on the All button.-',],
            [ 'CDTbusquedasWeb_TranslationHistoryAction_Desconocida',          'Unknown-',],
            [ 'CDTbusquedasWeb_TranslationHistoryAction_Importar',             'Import-',],
            [ 'CDTbusquedasWeb_TranslationHistoryAction_Ignorar',              'Ignore-',],
            [ 'CDTbusquedasWeb_TranslationHistoryAction_Traducir',             'Translate-',],
            [ 'CDTbusquedasWeb_TranslationHistoryAction_Comentar',             'Comment-',],
            [ 'CDTbusquedasWeb_TranslationHistoryAction_HacerPendiente',       'Change to Pending-',],
            [ 'CDTbusquedasWeb_TranslationHistoryAction_HacerTraducida',       'Change to Translated-',],
            [ 'CDTbusquedasWeb_TranslationHistoryAction_HacerRevisada',        'Change to Reviewed-',],
            [ 'CDTbusquedasWeb_TranslationHistoryAction_HacerDefinitiva',      'Change to Definitive (locked)-',],
            [ 'CDTbusquedasWeb_TranslationHistoryAction_Invalidar',            'Invalidate-',],
            [ 'CDTbusquedasWeb_TranslationHistoryAction_IntentarTraducirDifferentCounter',  'Collision with other simultaneus translation-',],
            [ 'CDTbusquedasWeb_NoTranslationsHistory',                         'No History-',],
            [ 'CDTbusquedasWeb_controlConfirmations_title',                    'Confirmation options-'],                
            [ 'CDTbusquedasWeb_controlConfirmations_help',                     'You may optionally disable user interface dialog requests to confirm changes of translations or status.-'],
            [ 'CDTbusquedasWeb_BrowseTranslationsFailure_Exception_msg',       'An exception occurred while retrieving translations.-',],
            [ 'CDTbusquedasWeb_BrowseTranslationsFailure_MakeSureYouAreLoggedOrContactSiteAdministrator_msg',  'Please make sure that you are properly logged as a user authorized for translations access, or contact your site administrator.-',],
            [ 'CDTbusquedasWeb_BrowseTranslationsFailure_Condition_msg',       'Translations retrieval failed with condition:-',],
            [ 'CDTbusquedasWeb_AccessFailedAndPromptYouHavePermission_label',  'Access to the translations catalog failed.\nDo you have permission ?\nIf so, you may want to login first.-',],
            [ 'CDTbusquedasWeb_NoAccessibleLanguages_label',                   'There are no languages available or accessible.-\nDo you have permission ?\nIf so, you may want to login first.-',],
            [ 'CDTbusquedasWeb_LanguageNotAccessible_label',                   'You are not allowed to access the selected language.-\nDo you have permission ?\nIf so, you may want to login first.-',],
            [ 'CDTbusquedasWeb_TranslationsCatalogIsLockedAgainstModifications', 'The Translations Catalog Is Locked Against Modifications-',],
            [ 'CDTbusquedasWeb_SelectedLanguageIsLockedAgainstModifications',    'The Selected Language Is Locked Against Modifications-',],
            [ cResultCondition_NoMatchingTranslationsFound,               cResultCondition_NoMatchingTranslationsFound,],
            [ 'CDTbusquedasWeb_reviseLasCondicionesDeFiltroYBusqueda_message', 'Please, review the filter and search criteria.-',],
            [ 'CDTbusquedasWeb_catalogo_action_label',                         'Catalog-',],
            [ 'CDTbusquedasWeb_selectorLenguagesReferencia_title',             'Reference Languages Selector-',],
            [ 'CDTbusquedasWeb_selectorLenguagesReferencia_help',              'Select the languages you want to use as reference.\nA high number of languages will slow down page loading.-',],
            [ 'CDTbusquedasWeb_limiteNumeroRegistrosExplorados_help',          'The maximum number of translations to explore in a single page is-',],
            [ 'CDTbusquedasWeb_numeroRegistrosDivididoPorNumerolenguages_help','divided by the number of reference languages selected plus one-',],
            [ 'CDTbusquedasWeb_todosPlus_action_label',                              '+',],
            [ 'CDTbusquedasWeb_ningunMinus_action_label',                            '-',],
            [ 'CDTbusquedasWeb_refrescar_action_label',                              'Refresh-',],
            [ 'CDTbusquedasWeb_NoConfirmTranslationChanges_label',                   'Do Not Confirm Translation Changes-',],
            [ 'CDTbusquedasWeb_NoConfirmStatusChanges_label',                        'Do Not Confirm Status Changes-',],
            [ 'CDTbusquedasWeb_NoConfirmTranslationDelete_label',                    'Do Not Confirm Translation Delete-',],
            [ 'CDTbusquedasWeb_controlEditorKeys_title',                             'Editor keys behaviour-',],
            [ 'CDTbusquedasWeb_controlEditorKeys_help',                              'Choose the behaviour when pressing the CR and Tab keys in the translations editor text area.-',],
            [ 'CDTbusquedasWeb_EditorKey_CR_label',                                  'Key Enter-',],
            [ 'CDTbusquedasWeb_EditorKey_Tab_label',                                 'Key Tab-',],
            [ 'CDTbusquedasWeb_EditorKeyActions_action_traducirYAvanzar_label',      'Translate and Advance-',],
            [ 'CDTbusquedasWeb_EditorKeyActions_action_traducir_label',              'Translate-',],
            [ 'CDTbusquedasWeb_EditorKeyActions_action_avanzar_label',               'Advance-',],
            [ 'CDTbusquedasWeb_EditorKeyActions_action_nextTabIndex_label',          'Next Tab-',],
            [ 'CDTbusquedasWeb_controlBusinessPresentacion_title',                   'Business sections-',],
            [ 'CDTbusquedasWeb_controlPresentacion_help',                            'Control of presentation options,\nto show or hide page sections relevant to the business.-',],
            [ 'CDTbusquedasWeb_ShowStateTransitionColumns_label',                    'Show columns with Status change Buttons-',],
            [ 'CDTbusquedasWeb_BatchStatusChanges_label',                            'Batch Status changes-',],
            [ 'CDTbusquedasWeb_mostrarSeccionInforme_section_label',                 'Show Summary section-',],
            [ 'CDTbusquedasWeb_mostrarSeccionHistoria_section_label',                'Show translation History section-',],
            [ 'CDTbusquedasWeb_mostrarSeccionLista_section_label',                   'Show List section-',],
            [ 'CDTbusquedasWeb_controlTechnicalPresentacion_title',                  'Technical sections-',],
            [ 'CDTbusquedasWeb_controlTechnicalPresentacion_help',                  'Control to show or hide page sections relevant to the technology.-',],
            [ 'CDTbusquedasWeb_controlTechnicalPresentacion_title',                  'Technical sections-',],
            [ 'CDTbusquedasWeb_TranslationsFilterLink_label',                        'Filter link (for results now shown in the list)-',],
            [ 'CDTbusquedasWeb_TranslationsFilterLink_help',                         'The User may bookmark or save the link as Favorites in the Internet browser,\nor drop the link as a Shortcut on the desktop,\nor just copy the URL, to reproduce the filter later.-',],
            [ 'CDTbusquedasWeb_filtro_section_label',                                'Filter-',],
            [ 'CDTbusquedasWeb_todosEstados_action_label',                           'Any status-',],
            [ 'CDTbusquedasWeb_BusquedasPorPalabrasContenidasEnSimboloOTraduccion_title','Filter by words in the symbol or the translation-',],
            [ 'CDTbusquedasWeb_searchByWords_help',  'Wildcards (* and ?) are permitted, but not at the beginning of words. You may use AND OR NOT between strings or groups of strings. You may group a subcriteria between parenthesis. You may specify exact sentences by surrounding them in double-quotes.-',],
            [ 'CDTbusquedasWeb_TRATraduccion_attr_simbolo_help',                           'The symbol of the string to translate.-',],
            [ 'CDTbusquedasWeb_searchBySimbolo_help',                                      'Enter words to search for in the string symbols. Wildcards (* and ?) are permitted.-',],
            [ 'CDTbusquedasWeb_TRATraduccion_attr_cadenaTraducida_help',                   'The translation of the string into the language.-',],
            [ 'CDTbusquedasWeb_searchByTranslation_help',                                  'Enter words  to search for in the translations into this language. Wildcards (* and ?) are permitted.-',],
            [ 'CDTbusquedasWeb_BusquedasPorEventos_formatoFechaISO_help',                  'Dates in ISO format YYYY-MM-DD HH:MM:SS-',],
            [ 'CDTbusquedasWeb_BusquedasPorEventos_sePermitenFechasParciales_help',        'Incomplete dates and times are allowed--',],
            [ 'CDTbusquedasWeb_BusquedasPorEventos_despuesDeFecha_title',                  'After-',],
            [ 'CDTbusquedasWeb_BusquedasPorEventos_antesDeFecha_title',                    'Before-',],
            [ 'CDTbusquedasWeb_BusquedasPorEventos_title',                                 'Filter by users and dates of status change events-',],
            [ 'CDTbusquedasWeb_BusquedasPorEventos_usuario_title',                         'User-',],
            [ 'CDTbusquedasWeb_BusquedasPorIdCadena_title',                                'Search by exact string symbol id-',],
            [ 'CDTbusquedasWeb_TRACadena_attr_id_help',                                    'Unique identifier for a string, and its translations to any language.-',],
            [ 'CDTbusquedasWeb_searchById_help',                                           'Enter the exact identifier of the string to search for.-',],
            [ 'CDTbusquedasWeb_FiltroCadenasInactivas_title',                              'Show Only Inactive Strings-',],
            [ 'CDTbusquedasWeb_FiltroCadenasInactivas_help',                               'The system shall present only Strings in the Inactive state.-',],
            [ 'CDTbusquedasWeb_seleccionarTodos_label',                                    'All-',],
            [ 'CDTbusquedasWeb_seleccionarNinguno_label',                                  'None-',],
            [ 'CDTbusquedasWeb_modulesFilter_title',                                       'Modules filter-',],
            [ 'CDTbusquedasWeb_modulesFilter_help',                                        'Select the modules with the translations you are interested in.\nIf no module is selected then there is no restriction on translation modules.\nThe --unspecified-- module represents those strings that are not associated with any module.--',],
            [ cNombreModuloNoEspecificadoLabel_MsgId,                                'Unspecified module-'],
            [ 'CDTbusquedasWeb_seccionGoTo_title',                                         'Go To-',],
            [ 'CDTbusquedasWeb_first_label',                                               'First-',],
            [ 'CDTbusquedasWeb_GoToParameters_title',                                      'First symbol to show in the translations list-',],
            [ 'CDTbusquedasWeb_TranslationsPage_GoTo_SymbolIndex_label',                   'Symbol at index #-',],
            [ 'CDTbusquedasWeb_TranslationsPage_GoTo_SymbolIndex_of',                      'of-',],
            [ 'CDTbusquedasWeb_TranslationsPage_GoTo_SymbolIndex_help',                    'The index number of the first symbol to show.-',],
            [ 'CDTbusquedasWeb_TranslationsPage_GoTo_PageIndex_label',                     'Page number #-',],
            [ 'CDTbusquedasWeb_TranslationsPage_GoTo_PageIndex_of',                      'of-',],
            [ 'CDTbusquedasWeb_TranslationsPage_GoTo_PageIndex_help',                    'The index number of the page to show.-',],
            [ 'CDTbusquedasWeb_TranslationsPage_GoTo_SymbolStartingWithChars_label',     'Symbol beginning with-',],
            [ 'CDTbusquedasWeb_TranslationsPage_GoTo_SymbolStartingWithChars_help',      'Beginning letters of the first symbol to show in the translations list.-',],
            [ 'CDTbusquedasWeb_informe_section_label',                                   'Summary-',],
            [ 'CDTbusquedasWeb_total_label',                                             'Total-',],
            [ 'CDTbusquedasWeb_Modulos_title',                                           'Modules-',],
            [ 'CDTbusquedasWeb_Fuentes_title',                                           'Sources-',],            
            [ 'CDTbusquedasWeb_seccionHistory_title',                                    'History-',],
        
        ]],
    ]
               

    someDomainsStringsAndDefaultsToTranslate.append( 
        [ 'CDTbusquedasWeb', 
            [[ 'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_%s' % unEstado,  unEstado] for unEstado in cTodosEstados]
        ]
    )        
    
    fTranslateI18NManyIntoDict(
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
    aCDTbwProfesionalesURL  =None,
    theThruCtxt             =None,):
    """Presenta un formulario de busqueda vacio.
        
    """
    
    anOutput = StringIO()
    
    _pRenderEmpty( 
        anOutput           =anOutput,                              
        unContextualObject =unContextualObject,                                             
        unHeader           =unHeader,                                                       
        unMessage          =unMessage,                                                      
        aPortalURL         =aPortalURL,                                                     
        aCDTbwProfesionalesURL       =aCDTbwProfesionalesURL,                                                   
        theThruCtxt        =theThruCtxt,                                               
    )
    
    return anOutput.getvalue()










def _pRenderEmpty( 
    anOutput           =None,             
    unContextualObject =None,                       
    unHeader           =None,             
    unMessage          =None,             
    aPortalURL         =None,              
    aCDTbwProfesionalesURL       =None,                
    theThruCtxt        =None,   ):
    """Produce el contenido de un formulario de busqueda vacio..
        
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
            \n""" % fCRs2BRs( fAsUnicode( unHeader))
        )

    if unMessage:
        anOutput.write( u"""  
            <br/>
            <p><font size="2">%s</font></p>
            <br/>
            \n""" % fCRs2BRs( fAsUnicode( unMessage))
        )

    anOutput.write( u"""  
        <br/>
        <br/>
        \n"""
    )
    
        
    return None
        


      
def _pRenderStyles(
    anOutput, 
    unContextualObject,
    theThruCtxt             =None,):
     
    anOutput.write( """
        
                   
        <!-- #################################################################
        SECTION: Styles to add presentation and behavior to the page elements
        ################################################################# -->

         <style type="text/css" >
            .CDTbwStyle_Clickable {
                cursor: pointer;
            }
            .CDTbwStyle_NoDisplay {
                display: none;
            }
            .CDTbwStyle_Display {
                display: run-in;
            }
            tr.CDTbwStyle_Display {
                display: table-row;
            }
        </style>
        \n"""
    )
    return None









def _pRenderScripts( 
    anOutput, 
    unContextualObject,
    theThruCtxt             =None,):                                                                                                                                    
    """Render the scripts assisting in controling the translations browser form in the client internet browser.
        
    """

    anOutput.write( u"""  
                    
        <!-- #################################################################
        SECTION: Scripts to be executed by user agent (WebBrowser)
        ################################################################# -->
        
       <!-- #################################################################
        Subsection: Translations form Script
        ################################################################# -->
        
        <script type="text/javascript" src="CDTbwProfesionales_PresentacionFormulario_javascripts.js"> </script>

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
    aPortalURL              =None,
    aCDTbwProfesionalesURL   =None,
    theThruCtxt             =None,):
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
        Subsection: Link to navigate back to CDTbwProfesionales container 
        ################################################################# -->
        <td align="left" valign="center" >
            <a href="%(pCDTbwProfesionalesAbsoluteURL)s" class="state-visible" title="%(CDTbusquedasWeb_catalogo_action_label)s" >
                <img src="%(pCDTbwProfesionalesAbsoluteURL)s/tra_root.gif" alt="%(CDTbusquedasWeb_catalogo_action_label)s" title="%(CDTbusquedasWeb_catalogo_action_label)s" id="icon-contenedor" />                                        
            </a>
        </td>
        <td align="right" valign="center" >
        \n""" % { 
    'pCDTbwProfesionalesAbsoluteURL':                 aCDTbwProfesionalesURL, 
    'CDTbusquedasWeb_catalogo_action_label':      aTranslationsCache[ 'CDTbusquedasWeb_catalogo_action_label'],  
    })
    
    
    
    _pRenderSelectorIdiomaPrincipal( 
        anOutput, 
        unContextualObject, 
        pLanguagesNamesAndFlags, 
        pTodosCodigosIdiomas, 
        pCodigoIdiomaCursor, 
        theThruCtxt,
        fCRs2BRs,
        fTranslateI18NCGIE,
        fAsUnicode,
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
        aCDTbwProfesionalesURL,
        theThruCtxt,
        fCRs2BRs,
        fTranslateI18NCGIE,
        fAsUnicode,
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
    theThruCtxt,
    fCRs2BRs,
    fTranslateI18NCGIE,
    fAsUnicode,
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
            'codigo-idioma':        fAsUnicode( unCodigoIdioma), 
            'nombre-idioma':        fAsUnicode( pLanguagesNamesAndFlags.get( unCodigoIdioma, {}).get( 'english', unCodigoIdioma)),
            'nombre-nativo-idioma': fAsUnicode( pLanguagesNamesAndFlags.get( unCodigoIdioma, {}).get( 'native',  unCodigoIdioma)),
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
    pProfesionales_Nombres                     =None,
    unaConfiguracionPaginaResultadosDict =None,
    aPortalURL                             =None,
    aCDTbwProfesionalesURL                           =None,
    fCGIE                                  =None,
    fCRs2BRs                              =None,
    fTranslateI18NCGIE                        =None,
    fAsUnicode                            =None,
    aTranslationsCache                     =None, ):
    """Render as collapsible the section to select the reference languages to display for each translation in the translations browser.
    
    """    
            
    _pRenderCollapsible_Lambda(  anOutput,
        aTranslationsCache[ 'CDTbusquedasWeb_idiomasSection_title'],
        u'elid_SelectorIdiomasReferencia_collapsible_dl', 
        lambda : _pRenderSelectorIdiomasReferencia( 
            anOutput, 
            unContextualObject, 
            pLanguagesNamesAndFlags, 
            pTodosCodigosIdiomasEInternacionales, 
            pProfesionales_Nombres,
            unaConfiguracionPaginaResultadosDict,
            aPortalURL,
            aCDTbwProfesionalesURL,
            theThruCtxt,
            fCRs2BRs,
            fTranslateI18NCGIE,
            fAsUnicode,
            aTranslationsCache
        )
    )
    
    return None        







def _pRenderSelectorIdiomasReferencia( 
    anOutput, 
    unContextualObject, 
    pLanguagesNamesAndFlags, 
    pTodosCodigosIdiomasEInternacionales, 
    pProfesionales_Nombres,
    unaConfiguracionPaginaResultadosDict,
    aPortalURL,
    aCDTbwProfesionalesURL,
    theThruCtxt,
    fCRs2BRs,
    fTranslateI18NCGIE,
    fAsUnicode,
    aTranslationsCache):
    """Render  the section to select the reference languages to display for each translation in the translations browser.
    
    """    

    unDisplayContryFlags = unContextualObject.fDisplayCountryFlags()
    
    unMaximoRegistrosExplorados = cMaximoRegistrosExplorados
    if not ( unaConfiguracionPaginaResultadosDict == None):
        unMaximoRegistrosExplorados = unaConfiguracionPaginaResultadosDict.get( 'maximoRegistrosExplorados', cMaximoRegistrosExplorados)
            
    
    anOutput.write( u"""  
        
        <!-- #################################################################
        SECTION: Selection of reference languages 
        ################################################################# -->                           
    
        <br/>
        <input name="form_submit" style="font-size: 10pt; font-style: italic"  value="%(CDTbusquedasWeb_refrescar_action_label)s" type="submit"/>
        <br/>
 
        <table id="sct_ReferenceLanguages_selector" class="listing nosort" summary="Selection of reference languages" >
            <thead>
                <tr>
                    <th colspan="%(colspan_head)d" align="left"   >
                        <span><font size="2"><strong>%(CDTbusquedasWeb_selectorLenguagesReferencia_title)s</strong></font></span>
                        <br/>
                        <span class="formHelp">
                            %(CDTbusquedasWeb_selectorLenguagesReferencia_help)s
                            <br/>
                            %(CDTbusquedasWeb_limiteNumeroRegistrosExplorados_help)s
                            <br/>
                            %(max-numero-registros-explorados)s
                            <br/>
                            %(CDTbusquedasWeb_numeroRegistrosDivididoPorNumerolenguages_help)s
                        </span>
                    </th>
                </tr>
                <tr>
                    <th colspan="%(colspan_labels)d"  />
                    <th align="center" >
                        <input type="checkbox"  class="noborder"  value=""  name="cid_CDTbwToggleAllReferenceLanguages" id="cid_CDTbwToggleAllReferenceLanguages" 
                            onchange="pTRAToggleAllReferenceLanguages(); return true;" />
                    </th>
                </tr>
            </head>
            <tbody>   
            \n""" % { 
        'colspan_head':                                               ( unDisplayContryFlags and 6) or 5,
        'colspan_labels':                                             ( unDisplayContryFlags and 5) or 4,
        'CDTbusquedasWeb_selectorLenguagesReferencia_title':                 aTranslationsCache[ 'CDTbusquedasWeb_selectorLenguagesReferencia_title'],
        'CDTbusquedasWeb_limiteNumeroRegistrosExplorados_help':              aTranslationsCache[ 'CDTbusquedasWeb_limiteNumeroRegistrosExplorados_help'],
        'max-numero-registros-explorados':                             unMaximoRegistrosExplorados,
        'CDTbusquedasWeb_numeroRegistrosDivididoPorNumerolenguages_help':    aTranslationsCache[  'CDTbusquedasWeb_numeroRegistrosDivididoPorNumerolenguages_help'],
        'CDTbusquedasWeb_selectorLenguagesReferencia_help':                  fCRs2BRs( aTranslationsCache[  'CDTbusquedasWeb_selectorLenguagesReferencia_help']),
        'CDTbusquedasWeb_todosPlus_action_label':                            aTranslationsCache[ 'CDTbusquedasWeb_todosPlus_action_label'],
        'CDTbusquedasWeb_ningunMinus_action_label':                          aTranslationsCache[  'CDTbusquedasWeb_ningunMinus_action_label'],
        'CDTbusquedasWeb_refrescar_action_label':                            aTranslationsCache[  'CDTbusquedasWeb_refrescar_action_label'],
    })
    
    unIndexRowIdiomaReferencia = 0 
    for unCodigoIdiomaEInternacional in pTodosCodigosIdiomasEInternacionales:  
        unCodigoIdiomaEnGvSIG         = unCodigoIdiomaEInternacional[ 0]
        unCodigoInternacionalDeIdioma = unCodigoIdiomaEInternacional[ 1]
                
        unasSizesIdioma = TRASizesIdioma( unCodigoIdiomaEnGvSIG)
        
        if unCodigoIdiomaEnGvSIG == unCodigoInternacionalDeIdioma:        
            anOutput.write( u"""                                                                                                                                                                     
                <tr class="%(class-row-idioma)s" >
                    <td colspan="2" align="left"  valign="center"  onclick="pTRAToggleIdiomaReferencia( '%(index-idioma)s'); return true;" class="CDTbwStyle_Clickable"  >                
                        <font size="1" >
                            <strong>
                                %(codigo-idioma)s
                            </strong>
                        </font>
                    </td>
                \n""" % { 
                'index-idioma':         str( unIndexRowIdiomaReferencia),
                'class-row-idioma':     cClasesFilas[ unIndexRowIdiomaReferencia % 2],
                'codigo-idioma':        fAsUnicode( unCodigoIdiomaEnGvSIG),
             } )
        else:
            anOutput.write( u"""                                                                                                                                                                     
                <tr class="%(class-row-idioma)s" >
                    <td align="left"  valign="center"  onclick="pTRAToggleIdiomaReferencia( '%(index-idioma)s'); return true;" class="CDTbwStyle_Clickable"  >                
                        <font size="1" >
                            <strong>
                                %(codigo-idioma)s
                            </strong>
                        </font>
                    </td>
                    <td align="left"  valign="center"  onclick="pTRAToggleIdiomaReferencia( '%(index-idioma)s'); return true;" class="CDTbwStyle_Clickable"  >                
                        <font size="1" >
                            <strong>
                                %(codigo-intl-idioma)s
                            </strong>
                        </font>
                    </td>
                \n""" % { 
                'index-idioma':         str( unIndexRowIdiomaReferencia),
                'class-row-idioma':     cClasesFilas[ unIndexRowIdiomaReferencia % 2],
                'codigo-idioma':        fAsUnicode( unCodigoIdiomaEnGvSIG),
                'codigo-intl-idioma':   fAsUnicode( unCodigoInternacionalDeIdioma),
            } )
                                
        anOutput.write( u"""                                                                                                                                                                     
                <td align="left" valign="center" onclick="pTRAToggleIdiomaReferencia( '%(index-idioma)s'); return true;" class="CDTbwStyle_Clickable"  >                
                    <font size="1" >
                        <strong>
                            %(nombre-idioma)s
                        </strong>
                    </font>
                </td>
                <td align="left" valign="center" onclick="pTRAToggleIdiomaReferencia( '%(index-idioma)s'); return true;" class="CDTbwStyle_Clickable"  >                
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
            'codigo-idioma':        fAsUnicode( unCodigoIdiomaEnGvSIG),
            'codigo-intl-idioma':   fAsUnicode( unCodigoInternacionalDeIdioma),
            'nombre-idioma':        fAsUnicode( pLanguagesNamesAndFlags.get( unCodigoIdiomaEnGvSIG, {}).get( 'english', '')),        
            'nombre-nativo-idioma': fAsUnicode( pLanguagesNamesAndFlags.get( unCodigoIdiomaEnGvSIG, {}).get( 'native',  '')),
            'idioma-checked':       (( unCodigoIdiomaEnGvSIG in pProfesionales_Nombres) and 'checked="checked"') or '',
        } )
        
        
        if unDisplayContryFlags:
            anOutput.write( u"""                                                                                                                                                                     
                    <td align="center" valign="center" onclick="pTRAToggleIdiomaReferencia( '%(index-idioma)s'); return true;" class="CDTbwStyle_Clickable"  >                
                        <img width="14" height="11" alt="Flag_%(nombre-idioma)s" src="%(flag-url)s" title="Flag_%(nombre-idioma)s" />
                    </td>
                \n""" % { 
                'index-idioma':         str( unIndexRowIdiomaReferencia),
                'codigo-idioma':        fAsUnicode( unCodigoIdiomaEnGvSIG),
                'nombre-idioma':        fAsUnicode( pLanguagesNamesAndFlags.get( unCodigoIdiomaEnGvSIG, {}).get( 'english', '')),        
                'flag-url':            pLanguagesNamesAndFlags.get( unCodigoIdiomaEnGvSIG, {}).get( 'flag_url', '%s/%s' % ( aPortalURL, cFlagIdiomaDesconocida,)), 
            } )
        
        anOutput.write( u"""                                                                                                                                                                     
                <td align="center" valign="center" >                
                    <input type="checkbox" class="noborder"  value="%(codigo-idioma)s"  %(idioma-checked)s name="theIdiomasReferencia" 
                        id="theIdiomasReferencia_%(index-idioma)s" />
                </td>
            </tr>
            \n""" % { 
            'index-idioma':         str( unIndexRowIdiomaReferencia),
            'codigo-idioma':        fAsUnicode( unCodigoIdiomaEnGvSIG),
            'idioma-checked':       (( unCodigoIdiomaEnGvSIG in pProfesionales_Nombres) and 'checked="checked"') or '',
        } )
        
        unIndexRowIdiomaReferencia += 1

    anOutput.write( u"""  
            </body>
        </table>
        <br/>
        <input name="form_submit" style="font-size: 10pt; font-style: italic"  value="%(CDTbusquedasWeb_refrescar_action_label)s" type="submit"/>
        <br/>
        <br/>
         \n""" % {
        'CDTbusquedasWeb_refrescar_action_label':             aTranslationsCache[ 'CDTbusquedasWeb_refrescar_action_label'],                
    })

    return None
                
  









    






def _pRenderCollapsibleControlPresentacion( 
    anOutput                               =None,
    unContextualObject                     =None,
    pResultadosPorPagina                 =None,
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
    unaConfiguracionPaginaResultadosDict =None,
    aPortalURL                             =None,
    aCDTbwProfesionalesURL                           =None,
    fCGIE                                  =None,
    fCRs2BRs                              =None,
    fTranslateI18NCGIE                        =None,
    fAsUnicode                            =None,
    aTranslationsCache                     =None, ):
    """Render as collapsible the control to select presentation sections to include in the translations browser.
    
    """    
            
    _pRenderCollapsible_Lambda(  anOutput,
        aTranslationsCache[ 'CDTbusquedasWeb_opcionesSection_title'],
        u'elid_ControlPresentacion_collapsible_dl', 
        lambda : _pRenderControlPresentacion( 
            anOutput                               =anOutput,
            unContextualObject                     =unContextualObject,
            pResultadosPorPagina                 =pResultadosPorPagina,
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
            unaConfiguracionPaginaResultadosDict =unaConfiguracionPaginaResultadosDict,
            aPortalURL                             =aPortalURL,
            aCDTbwProfesionalesURL                           =aCDTbwProfesionalesURL,
            fCGIE                                  =theThruCtxt,
            fCRs2BRs                              =fCRs2BRs,
            fTranslateI18NCGIE                        =fTranslateI18NCGIE,
            fAsUnicode                            =fAsUnicode,
            aTranslationsCache                     =aTranslationsCache,
        )
    )
    
    return None        




def _pRenderControlPresentacion( 
    anOutput                               =None,
    unContextualObject                     =None,
    pResultadosPorPagina                 =None,
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
    unaConfiguracionPaginaResultadosDict =None,
    aPortalURL                             =None,
    aCDTbwProfesionalesURL                           =None,
    fCGIE                                  =None,
    fCRs2BRs                              =None,
    fTranslateI18NCGIE                        =None,
    fAsUnicode                            =None,
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
        <h2>%(CDTbusquedasWeb_PresentationOptions_NoNeedToRefresh_label)s</h2>
        <br/>
        \n"""% {
        'CDTbusquedasWeb_PresentationOptions_NoNeedToRefresh_label':  aTranslationsCache[ 'CDTbusquedasWeb_PresentationOptions_NoNeedToRefresh_label'],                
    })
  
    
    
    

   
    
    anOutput.write( u"""  
        
         <!-- #################################################################
        Subsection: Show translation details in editor
        ################################################################# -->   
        
        <font size="2" >
            <strong>
                %(CDTbusquedasWeb_ShowEditorDetails_label)s
            </strong>
        </font>
        &emsp;
        <input type="checkbox" class="noborder"  value="on"  %(is-checked)s name="theMostrarDetallesTraduccion" id="theMostrarDetallesTraduccion" />
        <br/>
        <span class="formHelp" ><font size="1">%(CDTbusquedasWeb_AppliesOnSelectonForEditionNoNeedToRefresh_help)s</font></span>
        <br/>
        <br/>        
        
        \n"""% {
        'is-checked':                                  (( pMostrarDetallesTraduccion) and 'checked="checked"') or '',
        'CDTbusquedasWeb_ShowEditorDetails_label':           aTranslationsCache[ 'CDTbusquedasWeb_ShowEditorDetails_label'],  
        'CDTbusquedasWeb_AppliesOnSelectonForEditionNoNeedToRefresh_help': aTranslationsCache[ 'CDTbusquedasWeb_AppliesOnSelectonForEditionNoNeedToRefresh_help'],
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
                                %(CDTbusquedasWeb_controlConfirmations_title)s
                            </strong>
                        </font>
                        <p class="formHelp">
                            %(CDTbusquedasWeb_controlConfirmations_help)s
                            <br/>
                            %(CDTbusquedasWeb_AppliesImmediatelyNoNeedToRefresh_help)s
                        </p>
                    </th>
                </tr>
             </head>
            <tbody>   
        \n""" % {
        'CDTbusquedasWeb_controlConfirmations_title':      aTranslationsCache[ 'CDTbusquedasWeb_controlConfirmations_title'],                
        'CDTbusquedasWeb_controlConfirmations_help':       aTranslationsCache[ 'CDTbusquedasWeb_controlConfirmations_help'],
        'CDTbusquedasWeb_AppliesImmediatelyNoNeedToRefresh_help':     aTranslationsCache[ 'CDTbusquedasWeb_AppliesImmediatelyNoNeedToRefresh_help'],                
    })
        
 
        
    anOutput.write( u"""  
       <tr class="%(row-class)s" >
           <td align="left"  valign="center" onclick="pTRApTRAToggleSeccionPresentacion( 'theNoConfirmTranslationChanges'); return true;" class="CDTbwStyle_Clickable"  >                
               <font size="1" >
                   <strong>
                       %(CDTbusquedasWeb_NoConfirmTranslationChanges_label)s
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
        'CDTbusquedasWeb_NoConfirmTranslationChanges_label': aTranslationsCache[ 'CDTbusquedasWeb_NoConfirmTranslationChanges_label'],
        'is-checked': (( pNoConfirmTranslationChanges) and 'checked="checked"') or '',
    })
    pConfigParmsIndex += 1
                
            
    anOutput.write( u"""  
       <tr class="%(row-class)s"  >
           <td align="left"  valign="center" onclick="pTRApTRAToggleSeccionPresentacion( 'theNoConfirmStatusChanges'); return true;" class="CDTbwStyle_Clickable"  >                
               <font size="1" >
                   <strong>
                       %(CDTbusquedasWeb_NoConfirmStatusChanges_label)s
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
        'CDTbusquedasWeb_NoConfirmStatusChanges_label': aTranslationsCache[ 'CDTbusquedasWeb_NoConfirmStatusChanges_label'], 
        'is-checked': (( pNoConfirmStatusChanges) and 'checked="checked"') or '',
    })
    pConfigParmsIndex += 1
           
            
    anOutput.write( u"""  
       <tr class="%(row-class)s"  >
           <td align="left"  valign="center" onclick="pTRApTRAToggleSeccionPresentacion( 'theNoConfirmTranslationDelete'); return true;" class="CDTbwStyle_Clickable"  >                
               <font size="1" >
                   <strong>
                       %(CDTbusquedasWeb_NoConfirmTranslationDelete_label)s
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
        'CDTbusquedasWeb_NoConfirmTranslationDelete_label': aTranslationsCache[ 'CDTbusquedasWeb_NoConfirmTranslationDelete_label'], 
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
                                %(CDTbusquedasWeb_controlEditorKeys_title)s
                            </strong>
                        </font>
                        <p class="formHelp">
                            %(CDTbusquedasWeb_controlEditorKeys_help)s
                            <br/>
                            %(CDTbusquedasWeb_AppliesImmediatelyNoNeedToRefresh_help)s
                        </p>
                    </th>
                </tr>
             </head>
            <tbody>   
                <tr class="even" >
                    <td align="left" valign="center" >%(CDTbusquedasWeb_EditorKey_CR_label)s</td>                
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
                    <td align="left" valign="center" >%(CDTbusquedasWeb_EditorKey_Tab_label)s</td>                
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
        'CDTbusquedasWeb_controlEditorKeys_title':      aTranslationsCache[ 'CDTbusquedasWeb_controlEditorKeys_title'],                
        'CDTbusquedasWeb_controlEditorKeys_help':       aTranslationsCache[ 'CDTbusquedasWeb_controlEditorKeys_help'],
        'CDTbusquedasWeb_AppliesImmediatelyNoNeedToRefresh_help':     aTranslationsCache[ 'CDTbusquedasWeb_AppliesImmediatelyNoNeedToRefresh_help'],                
        'CDTbusquedasWeb_EditorKey_CR_label':           aTranslationsCache[ 'CDTbusquedasWeb_EditorKey_CR_label'],
        'CDTbusquedasWeb_EditorKey_Tab_label':          aTranslationsCache[ 'CDTbusquedasWeb_EditorKey_Tab_label'],
        'is-selected-Tab_action_traducirYAvanzar':       (( pEditorKeyTabAction == 'action_traducirYAvanzar' ) and 'selected="selected"') or '',
        'is-selected-Tab_action_traducir':               (( pEditorKeyTabAction == 'action_traducir' )       and 'selected="selected"') or '',
        'is-selected-Tab_action_avanzar':                (( pEditorKeyTabAction == 'action_avanzar' )        and 'selected="selected"') or '',
        'is-selected-Tab_action_nextTabIndex':           (( pEditorKeyTabAction == 'action_nextTabIndex' )   and 'selected="selected"') or '',
        'action_traducirYAvanzar_label':                 aTranslationsCache[ 'CDTbusquedasWeb_EditorKeyActions_action_traducirYAvanzar_label'],
        'action_traducir_label':                         aTranslationsCache[ 'CDTbusquedasWeb_EditorKeyActions_action_traducir_label'],
        'action_avanzar_label':                          aTranslationsCache[ 'CDTbusquedasWeb_EditorKeyActions_action_avanzar_label'],
        'action_nextTabIndex_label':                     aTranslationsCache[ 'CDTbusquedasWeb_EditorKeyActions_action_nextTabIndex_label'],
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
                %(CDTbusquedasWeb_InteractionMode_label)s
            </strong>
        </font>
        <br/>
        <font size="1" >
            <strong>
                %(CDTbusquedasWeb_InteractionMode_Asynchronous_label)s
            </strong>
        </font>
        &ensp;
        <input type="radio" class="noborder"  value="%(interaction-mode-async)s"  %(is-checked-Async)s name="theInteractionMode" id="theInteractionMode_Async" />
        &emsp;
        &emsp;
        &emsp;
        <font size="1" >
            <strong>
                %(CDTbusquedasWeb_InteractionMode_Synchronous_label)s
            </strong>
        </font>
       &ensp;
        <input onclick="gAsynchronousTranslationMode_CachedInVar=999; return true;"
            type="radio" class="noborder"  value="%(interaction-mode-sync)s"   
            %(is-checked-Sync)s name="theInteractionMode" id="theInteractionMode_Sync" />
        <div class="formHelp">
            <font size="1">
                %(CDTbusquedasWeb_InteractionMode_Asynchronous_label)s&nbsp;%(CDTbusquedasWeb_InteractionMode_Asynchronous_help)s
                <br/>
                %(CDTbusquedasWeb_InteractionMode_Synchronous_label)s&nbsp;%(CDTbusquedasWeb_InteractionMode_Synchronous_help)s
                <br/>
                %(CDTbusquedasWeb_AppliesImmediatelyNoNeedToRefresh_help)s
            </font>
        </div>
        <br/>        
        <br/>
        
        
        \n"""% {
        'interaction-mode-async':                                       cInteractionMode_Asynchronous,
        'interaction-mode-sync':                                        cInteractionMode_Synchronous,
        'is-checked-Async':                                             (( pInteractionMode == cInteractionMode_Asynchronous) and 'checked="checked"') or '',
        'is-checked-Sync':                                              (( pInteractionMode == cInteractionMode_Synchronous)  and 'checked="checked"') or '',
        'CDTbusquedasWeb_InteractionMode_label':                      aTranslationsCache[ 'CDTbusquedasWeb_InteractionMode_label'],                
        'CDTbusquedasWeb_InteractionMode_Asynchronous_label':         aTranslationsCache[ 'CDTbusquedasWeb_InteractionMode_Asynchronous_label'],                
        'CDTbusquedasWeb_InteractionMode_Asynchronous_help':          aTranslationsCache[ 'CDTbusquedasWeb_InteractionMode_Asynchronous_help'],                
        'CDTbusquedasWeb_InteractionMode_Synchronous_label':          aTranslationsCache[ 'CDTbusquedasWeb_InteractionMode_Synchronous_label'],                
        'CDTbusquedasWeb_InteractionMode_Synchronous_help':           aTranslationsCache[ 'CDTbusquedasWeb_InteractionMode_Synchronous_help'],                
        'CDTbusquedasWeb_AppliesImmediatelyNoNeedToRefresh_help':     aTranslationsCache[ 'CDTbusquedasWeb_AppliesImmediatelyNoNeedToRefresh_help'],                
    })

 
        

        
    
    anOutput.write( u"""  
        <!-- #################################################################
        SUBSECTION: Presentation options control that need to refresh
        ################################################################# -->   
        <br/>
        <h2>%(CDTbusquedasWeb_PresentationOptions_MustRefresh_label)s</h2>
        <br/>

        
        <!-- #################################################################
        Subsection: Refresh button
        ################################################################# -->   
        
        <input name="form_submit" style="font-size: 10pt; font-style: italic"  value="%(CDTbusquedasWeb_refrescar_action_label)s" type="submit"/>
        <br/>
        \n"""% {
        'CDTbusquedasWeb_refrescar_action_label':                     aTranslationsCache[ 'CDTbusquedasWeb_refrescar_action_label'],                
        'CDTbusquedasWeb_PresentationOptions_MustRefresh_label':      aTranslationsCache[ 'CDTbusquedasWeb_PresentationOptions_MustRefresh_label'],                
      })
    
    
    unMaximoRegistrosExplorados = cMaximoRegistrosExplorados
    if not ( unaConfiguracionPaginaResultadosDict == None):
        unMaximoRegistrosExplorados = unaConfiguracionPaginaResultadosDict.get( 'maximoRegistrosExplorados', cMaximoRegistrosExplorados)
        
        
    anOutput.write( u"""  
        <br/>
        <!-- #################################################################
        Subsection: Number of  translations per page
        ################################################################# -->   
        
        <font size="2">
            <strong>
                %(CDTbusquedasWeb_TranslationsPerPage_label)s
            </strong>
        </font>
        &emsp;
        <input style="font-size: 8pt;" size="4"  name="theResultadosPorPagina" id="theResultadosPorPagina" value="%(pResultadosPorPagina)s" /> 
        <br/>
        <span class="formHelp">
            %(CDTbusquedasWeb_limiteNumeroRegistrosExplorados_help)s
            &ensp;
            %(max-numero-registros-explorados)s
            &ensp;
            %(CDTbusquedasWeb_numeroRegistrosDivididoPorNumerolenguages_help)s
        </span>
        <br/>
        \n""" % {
        'pResultadosPorPagina':                                           str( pResultadosPorPagina),
        'CDTbusquedasWeb_TranslationsPerPage_label':                      aTranslationsCache[ 'CDTbusquedasWeb_TranslationsPerPage_label'], 
        'CDTbusquedasWeb_limiteNumeroRegistrosExplorados_help':           aTranslationsCache[ 'CDTbusquedasWeb_limiteNumeroRegistrosExplorados_help'],
        'max-numero-registros-explorados':                          unMaximoRegistrosExplorados,
        'CDTbusquedasWeb_numeroRegistrosDivididoPorNumerolenguages_help': aTranslationsCache[ 'CDTbusquedasWeb_numeroRegistrosDivididoPorNumerolenguages_help'],
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
                                %(CDTbusquedasWeb_controlBusinessPresentacion_title)s
                            </strong>
                        </font>
                        <p class="formHelp">%(CDTbusquedasWeb_controlPresentacion_help)s</p>
                    </th>
                </tr>
             </head>
            <tbody>   
            \n""" % {
        'CDTbusquedasWeb_controlBusinessPresentacion_title':  aTranslationsCache[ 'CDTbusquedasWeb_controlBusinessPresentacion_title'],             
        'CDTbusquedasWeb_controlPresentacion_help':           aTranslationsCache[ 'CDTbusquedasWeb_controlPresentacion_help'],
    })
    
     
     
    pConfigParmsIndex = 0
     
     
    if pShowStateTransitionColumnsOption:
        anOutput.write( u"""  
            <tr class="%(row-class)s" >
                <td align="left"  valign="center" onclick="pTRApTRAToggleSeccionPresentacion( 'theShowStateTransitionColumns'); return true;" class="CDTbwStyle_Clickable"  >                
                    <font size="1" >
                        <strong>
                            %(CDTbusquedasWeb_ShowStateTransitionColumns_label)s
                        </strong>
                    </font>
                </td>
                <td align="center" valign="center" >                
                    <input type="checkbox" class="noborder"  value="on"  %(is-checked)s name="theShowStateTransitionColumns" id="theShowStateTransitionColumns" />
                </td>
            </tr>
            \n""" % { 
            'row-class':    cClasesFilas[ pConfigParmsIndex % 2],
            'CDTbusquedasWeb_ShowStateTransitionColumns_label': aTranslationsCache[ 'CDTbusquedasWeb_ShowStateTransitionColumns_label'],
            'is-checked': (( pShowStateTransitionColumns) and 'checked="checked"') or '',
        })
        pConfigParmsIndex += 1
        
        
    if pShowBatchStatusChangesOption:
        anOutput.write( u"""  
           <tr class="%(row-class)s" >
               <td align="left"  valign="center" onclick="pTRApTRAToggleSeccionPresentacion( 'theBatchStatusChanges'); return true;" class="CDTbwStyle_Clickable"  >                
                   <font size="1" >
                       <strong>
                           %(CDTbusquedasWeb_BatchStatusChanges_label)s
                       </strong>
                   </font>
               </td>
               <td align="center" valign="center" >                
                   <input type="checkbox" class="noborder"  value="on"  %(is-checked)s name="theBatchStatusChanges" id="theBatchStatusChanges" />
               </td>
           </tr>
           \n""" % { 
            'row-class':    cClasesFilas[ pConfigParmsIndex % 2],
            'CDTbusquedasWeb_BatchStatusChanges_label': aTranslationsCache[ 'CDTbusquedasWeb_BatchStatusChanges_label'], 
            'is-checked': (( pBatchStatusChanges) and 'checked="checked"') or '',
        })
        pConfigParmsIndex += 1
    
        
    anOutput.write( u"""  
       <tr class="%(row-class)s" >
           <td align="left"  valign="center" onclick="pTRAToggleSeccionPresentacion( 'theMostrarInforme'); return true;" class="CDTbwStyle_Clickable"  >                
               <font size="1" >
                   <strong>
                       %(CDTbusquedasWeb_mostrarSeccionInforme_section_label)s
                   </strong>
               </font>
           </td>
           <td align="center" valign="center" >                
               <input type="checkbox" class="noborder"  value="on"  %(is-checked)s name="theMostrarInforme" id="theMostrarInforme" />
           </td>
       </tr>
       \n""" % { 
        'row-class':    cClasesFilas[ pConfigParmsIndex % 2],
        'CDTbusquedasWeb_mostrarSeccionInforme_section_label': aTranslationsCache[ 'CDTbusquedasWeb_mostrarSeccionInforme_section_label'], 
        'is-checked': (( pMostrarInforme) and 'checked="checked"') or '',
    })
    pConfigParmsIndex += 1
    

  
   
    anOutput.write( u"""  
       <tr class="%(row-class)s" >
           <td align="left"  valign="center" onclick="pTRAToggleSeccionPresentacion( 'theMostrarHistoria'); return true;" class="CDTbwStyle_Clickable"  >                
               <font size="1" >
                   <strong>
                       %(CDTbusquedasWeb_mostrarSeccionHistoria_section_label)s
                   </strong>
               </font>
           </td>
           <td align="center" valign="center" >                
               <input type="checkbox" class="noborder"  value="on"  %(is-checked)s name="theMostrarHistoria" id="theMostrarHistoria" />
           </td>
        </tr>
        \n""" % { 
        'row-class':    cClasesFilas[ pConfigParmsIndex % 2],
        'CDTbusquedasWeb_mostrarSeccionHistoria_section_label': aTranslationsCache[ 'CDTbusquedasWeb_mostrarSeccionHistoria_section_label'],
        'is-checked': (( pMostrarHistoria) and 'checked="checked"') or '',
    })
    pConfigParmsIndex += 1
    
    
    anOutput.write( u"""  
        <tr class="%(row-class)s" >
            <td align="left"  valign="center" onclick="pTRAToggleSeccionPresentacion( 'theMostrarLista'); return true;" class="CDTbwStyle_Clickable"  >                
                <font size="1" >
                    <strong>
                        %(CDTbusquedasWeb_mostrarSeccionLista_section_label)s
                    </strong>
                </font>
            </td>
            <td align="center" valign="center" >                
                <input type="checkbox" class="noborder"  value="on"  %(is-checked)s name="theMostrarLista" id="theMostrarLista" />
            </td>
        </tr>
        \n""" % { 
        'row-class':    cClasesFilas[ pConfigParmsIndex % 2],
        'CDTbusquedasWeb_mostrarSeccionLista_section_label': aTranslationsCache[ 'CDTbusquedasWeb_mostrarSeccionLista_section_label'],
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
                                %(CDTbusquedasWeb_controlTechnicalPresentacion_title)s
                            </strong>
                        </font>
                        <p class="formHelp">%(CDTbusquedasWeb_controlTechnicalPresentacion_help)s</p>
                    </th>
                </tr>
             </head>
            <tbody>   
            \n""" % {
        'CDTbusquedasWeb_refrescar_action_label':             aTranslationsCache[ 'CDTbusquedasWeb_refrescar_action_label'],             
        'CDTbusquedasWeb_controlTechnicalPresentacion_title': aTranslationsCache[ 'CDTbusquedasWeb_controlTechnicalPresentacion_title'],
        'CDTbusquedasWeb_controlTechnicalPresentacion_help':  aTranslationsCache[ 'CDTbusquedasWeb_controlTechnicalPresentacion_help'],
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
               <td align="left"  valign="center" onclick="pTRAToggleSeccionPresentacion( '%(unSectionControlFieldName)s'); return true;" class="CDTbwStyle_Clickable"  >                
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
        <input name="form_submit" style="font-size: 10pt; font-style: italic"  value="%(CDTbusquedasWeb_refrescar_action_label)s" type="submit"/>
        <br/>
        <br/>
         \n""" % {
        'CDTbusquedasWeb_refrescar_action_label':             aTranslationsCache[ 'CDTbusquedasWeb_refrescar_action_label'],                
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
    aCDTbwProfesionalesURL          =None,
    fCGIE                 =None,
    fCRs2BRs             =None,
    fTranslateI18NCGIE       =None,
    fAsUnicode           =None,
    aTranslationsCache    =None, ):
    """Render as collapsible the filter section of the translations browser.
    
    """    

    _pRenderCollapsible_Lambda(  anOutput,
        aTranslationsCache[ 'CDTbusquedasWeb_seccionFiltro_title'],
        u'elid_Filter_collapsible_dl', 
        lambda : _pRenderFiltro( 
            anOutput              =anOutput,                
            unContextualObject    =unContextualObject,                          
            pCodigoIdiomaCursor   =pCodigoIdiomaCursor,                          
            pTodosNombresModulos  =pTodosNombresModulos,                            
            pEstadosIncluidos     =pEstadosIncluidos,                         
            pSearchParameters     =pSearchParameters,                         
            aPortalURL            =aPortalURL,                 
            aCDTbwProfesionalesURL          =aCDTbwProfesionalesURL,                   
            fCGIE                 =theThruCtxt,            
            fCRs2BRs             =fCRs2BRs,                
            fTranslateI18NCGIE       =fTranslateI18NCGIE,                      
            fAsUnicode           =fAsUnicode,                  
            aTranslationsCache    =aTranslationsCache,        
        ),
    )
    
    return None        






def _fRenderApplyOrCancelFiltro( 
    anOutput, 
    unContextualObject, 
    unTabIndex, 
    aPortalURL,
    aCDTbwProfesionalesURL,
    theThruCtxt,
    fCRs2BRs,
    fTranslateI18NCGIE,
    fAsUnicode,
    aTranslationsCache):
    """Render a section with buttons to apply or cancel the filter.
    
    """    
    
    anOutput.write( u"""    
    
        <!-- #################################################################
        SECTION: Aplicar o Cancelar Filtro para busqueda de TRATraduccion
        ################################################################# -->
                
        <input tabindex=%(tabindex)d name="form_submit" style="font-size: 10pt; font-style: italic"  value="%(CDTbusquedasWeb_refrescar_action_label)s" type="submit"/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <input tabindex=%(tabindex2)d type="button" name="todos" style="font-size: 9pt; "  value="%(CDTbusquedasWeb_todas_label)s" onclick="pTRAResetFiltros(); return true;" class="CDTbwStyle_Clickable"  />
        <br/>
        \n""" % { 
        'tabindex':                                            unTabIndex,
        'tabindex2':                                           unTabIndex + 1,
        'CDTbusquedasWeb_refrescar_action_label':                    aTranslationsCache[ 'CDTbusquedasWeb_refrescar_action_label'],
        'CDTbusquedasWeb_todas_label':                               aTranslationsCache[ 'CDTbusquedasWeb_todas_label'],
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
    aCDTbwProfesionalesURL          =None,
    fCGIE                 =None,
    fCRs2BRs             =None,
    fTranslateI18NCGIE       =None,
    fAsUnicode           =None,
    aTranslationsCache    =None, ):
    """Render the filter section of the translations browser.
    
    """    
 
    unTabIndex = 11
    
    anOutput.write( u"""    
    
        <!-- #################################################################
        SECTION: Ayuda acerca del uso del Filtro para busqueda de TRATraduccion
        ################################################################# -->
                
        <p class="formHelp">
            <span >%(CDTbusquedasWeb_TranslationsFilter_help)s</span>
            <br/>
            <span >%(CDTbusquedasWeb_TranslationsFilter_Reset_help)s</span>
        </p>
        \n""" % { 
        'CDTbusquedasWeb_TranslationsFilter_help':                   fCRs2BRs( aTranslationsCache[ 'CDTbusquedasWeb_TranslationsFilter_help']),
        'CDTbusquedasWeb_TranslationsFilter_Reset_help':             fCRs2BRs( aTranslationsCache[ 'CDTbusquedasWeb_TranslationsFilter_Reset_help']),                
    })
    
    unTabIndex = _fRenderApplyOrCancelFiltro( 
        anOutput, 
        unContextualObject, 
        unTabIndex, 
        aPortalURL,
        aCDTbwProfesionalesURL,
        theThruCtxt,
        fCRs2BRs,
        fTranslateI18NCGIE,
        fAsUnicode,
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
        unParametrosFiltroStream.write( u"""theSearchSimbolo=%s""" % fCGIE( fAsUnicode( pSearchParameters[ 'simbolo'])))
        unHayParametrosFiltro = True    
        
    if pSearchParameters.get( 'cadenaTraducida', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchCadenaTraducida=%s""" % fCGIE( fAsUnicode( pSearchParameters[ 'cadenaTraducida'])))
        unHayParametrosFiltro = True    
        
    if pSearchParameters.get( 'usuarioCreador', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchUsuarioCreador=%s""" % fCGIE( fAsUnicode( pSearchParameters[ 'usuarioCreador'])))
        unHayParametrosFiltro = True    
        
    if pSearchParameters.get( 'fechaCreacionInicial', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchFechaCreacionInicial=%s""" % fCGIE( fAsUnicode( pSearchParameters[ 'fechaCreacionInicial'])))
        unHayParametrosFiltro = True    
        
    if pSearchParameters.get( 'fechaCreacionFinal', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchFechaCreacionFinal=%s""" % fCGIE( fAsUnicode( pSearchParameters[ 'fechaCreacionFinal'])))
        unHayParametrosFiltro = True    
        
        
    if pSearchParameters.get( 'usuarioTraductor', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchUsuarioTraductor=%s""" % fCGIE( fAsUnicode( pSearchParameters[ 'usuarioTraductor'])))
        unHayParametrosFiltro = True    
        
    if pSearchParameters.get( 'fechaTraduccionInicial', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchFechaTraduccionInicial=%s""" % fCGIE( fAsUnicode( pSearchParameters[ 'fechaTraduccionInicial'])))
        
    if pSearchParameters.get( 'fechaTraduccionFinal', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchFechaTraduccionFinal=%s""" % fCGIE( fAsUnicode( pSearchParameters[ 'fechaTraduccionFinal'])))
        unHayParametrosFiltro = True    

        
    if pSearchParameters.get( 'usuarioRevisor', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchUsuarioRevisor=%s""" % fCGIE( fAsUnicode( pSearchParameters[ 'usuarioRevisor'])))
        unHayParametrosFiltro = True    
        
    if pSearchParameters.get( 'fechaRevisionInicial', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchFechaRevisionInicial=%s""" % fCGIE( fAsUnicode( pSearchParameters[ 'fechaRevisionInicial'])))
        unHayParametrosFiltro = True    
        
    if pSearchParameters.get( 'fechaRevisionFinal', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchFechaRevisionFinal=%s""" % fCGIE( fAsUnicode( pSearchParameters[ 'fechaRevisionFinal'])))
        unHayParametrosFiltro = True    

        
    if pSearchParameters.get( 'usuarioCoordinador', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchUsuarioCoordinador=%s""" % fCGIE( fAsUnicode( pSearchParameters[ 'usuarioCoordinador'])))
        unHayParametrosFiltro = True    
        
    if pSearchParameters.get( 'fechaDefinitivoInicial', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchFechaDefinitivoInicial=%s""" % fCGIE( fAsUnicode( pSearchParameters[ 'fechaDefinitivoInicial'])))
        unHayParametrosFiltro = True    
        
    if pSearchParameters.get( 'fechaDefinitivoFinal', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchFechaDefinitivoFinal=%s""" % fCGIE( fAsUnicode( pSearchParameters[ 'fechaDefinitivoFinal'])))
        unHayParametrosFiltro = True    

        
    if pSearchParameters.get( 'usuarioModificador', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchUsuarioModificador=%s""" % fCGIE( fAsUnicode( pSearchParameters[ 'usuarioModificador'])))
        unHayParametrosFiltro = True    
        
    if pSearchParameters.get( 'fechaModificacionInicial', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchFechaModificacionInicial=%s""" % fCGIE( fAsUnicode( pSearchParameters[ 'fechaModificacionInicial'])))
        unHayParametrosFiltro = True    
        
    if pSearchParameters.get( 'fechaModificacionFinal', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSearchFechaModificacionFinal=%s""" % fCGIE( fAsUnicode( pSearchParameters[ 'fechaModificacionFinal'])))
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
        unParametrosFiltroStream.write( u"""theSearchIdCadena=%s""" % fCGIE( fAsUnicode( pSearchParameters[ 'idCadena'])))
        unHayParametrosFiltro = True    

    if pSearchParameters.get( 'cadenasInactivas', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theInactiveStrings=on""" )
        unHayParametrosFiltro = True    
                      

    if pSearchParameters.get( 'simboloCadenaCursor', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theSimboloCadenaCursor=%s""" % fCGIE( fAsUnicode( pSearchParameters[ 'simboloCadenaCursor'])))
        unHayParametrosFiltro = True    


    if pSearchParameters.get( 'traduccionesPorPagina', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theResultadosPorPagina=%s""" % fCGIE( fAsUnicode( str( pSearchParameters[ 'traduccionesPorPagina']))))
        unHayParametrosFiltro = True    

    if pSearchParameters.get( 'symbolIndex', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theGoToResultIndex=%s""" % fCGIE( fAsUnicode( str( pSearchParameters[ 'symbolIndex']))))
        unHayParametrosFiltro = True    

    if pSearchParameters.get( 'pageIndex', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theGoToPageIndex=%s""" % fCGIE( fAsUnicode( str( pSearchParameters[ 'pageIndex']))))
        unHayParametrosFiltro = True    

    if pSearchParameters.get( 'symbolStartingWith', None):
        if unHayParametrosFiltro:
            unParametrosFiltroStream.write( '&')
        unParametrosFiltroStream.write( u"""theGoToSymbolStartingWith=%s""" % fCGIE( fAsUnicode( pSearchParameters[ 'symbolStartingWith'])))
        unHayParametrosFiltro = True    

    unParametrosFiltroString = unParametrosFiltroStream.getvalue()    
    
    
    
    unParametrosFiltroStream.close()
    unParametrosRequestStream = StringIO( u'')
    
    if pCodigoIdiomaCursor:
        unParametrosRequestStream.write( '?theCodigoIdiomaCursor=%s'% fCGIE( fAsUnicode( pCodigoIdiomaCursor)))
        
        unParametrosRequestStream.write( '&theMostrarInforme=on&theMostrarLista=on')
    
    pProfesionales_Nombres = pSearchParameters.get( 'idiomasReferencia', [])
    for aReferenceLanguage in pProfesionales_Nombres:
        unParametrosRequestStream.write( '&theIdiomasReferencia=%s' % fCGIE( fAsUnicode( aReferenceLanguage)))
                   
    unParametrosRequestString = unParametrosRequestStream.getvalue()
    
    unURLEnlaceFiltroTraduccion = '%s/TRATraducir/%s&%s' % ( aCDTbwProfesionalesURL, unParametrosRequestString, unParametrosFiltroString,)
                   
                   
    anOutput.write( u"""    
        <br/>
        <a href="%(urlEnlaceFiltro)s">
            %(CDTbusquedasWeb_TranslationsFilterLink_label)s
            <p class="formHelp">%(CDTbusquedasWeb_TranslationsFilterLink_help)s</p>
        </a>
        <br/>
        """ % { 
            'urlEnlaceFiltro': unURLEnlaceFiltroTraduccion, 
            'CDTbusquedasWeb_TranslationsFilterLink_label': aTranslationsCache[ 'CDTbusquedasWeb_TranslationsFilterLink_label'],
            'CDTbusquedasWeb_TranslationsFilterLink_help':  fCRs2BRs( aTranslationsCache[ 'CDTbusquedasWeb_TranslationsFilterLink_help'],),
    })

    unTabIndex += 1

    anOutput.write( u"""    

        <!-- #################################################################
        Subsection: Filtro por estados 
        ################################################################# -->
        <table class="listing nosort" id="sct_Filter_Status" >
            <thead>
                <tr>
                    <th  valign="baseline" align="left" onclick="pTRAResetFiltrosEstados(); return true;" class="CDTbwStyle_Clickable"  >
                        <font size="2">
                            <strong>
                                %(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_label)s
                            </strong>
                        </font>
                    </th>
            \n""" % { 
        'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_label': aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_label'],
    })

       
    
    for unEstadoTraduccion in cTodosEstados:                                  
        anOutput.write( u"""                 
            <th align="center" valign="baseline" onclick="pTRAToggleFiltroEstado( '%(unEstadoTraduccion)s'); return true;" class="CDTbwStyle_Clickable"  >
                <font size="1" >
                    <span>%(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_label)s</span>
                </font>
                <br/>
                <img  alt="TranslationStatus_%(unEstadoTraduccion)s" src="%(portal_url)s/%(estado-icon)s" title="%(unEstadoTraduccion)s" />                        
            </th>
            \n""" % { 
            'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_label': aTranslationsCache.get( 'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_%s' % unEstadoTraduccion, unEstadoTraduccion),
            'portal_url':               aPortalURL, 
            'unEstadoTraduccion':       unEstadoTraduccion,
            'estado-icon':              cIconsDict.get( unEstadoTraduccion, 'tra_pendiente.gif'), 
        })
        
    anOutput.write( u"""    
                </tr>
            </thead>      
            <tbody>  
                <tr>
                    <td align="center" onclick="pTRAResetFiltrosEstados(); return true;" class="CDTbwStyle_Clickable"  >
                        <img alt="%(CDTbusquedasWeb_todosPlus_action_label)s"   src="%(portal_url)s/add_icon.gif" title="%(CDTbusquedasWeb_todosPlus_action_label)s" />
                        %(CDTbusquedasWeb_todosEstados_action_label)s
                    </td>
                    \n""" % { 
        'CDTbusquedasWeb_filtro_label':                               aTranslationsCache[ 'CDTbusquedasWeb_filtro_section_label'],
        'CDTbusquedasWeb_limpiarfiltro_action_label':                 aTranslationsCache[ 'CDTbusquedasWeb_todas_label'],
        'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_label':  aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_label'],
        'CDTbusquedasWeb_todosEstados_action_label':                  aTranslationsCache[ 'CDTbusquedasWeb_todosEstados_action_label'],
        'CDTbusquedasWeb_todosPlus_action_label':                     aTranslationsCache[ 'CDTbusquedasWeb_todosPlus_action_label'],
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
        aCDTbwProfesionalesURL,
        theThruCtxt,
        fCRs2BRs,
        fTranslateI18NCGIE,
        fAsUnicode,
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
                                %(CDTbusquedasWeb_BusquedasPorPalabrasContenidasEnSimboloOTraduccion_title)s
                            </strong>
                        </font>
                        <p class="formHelp">
                            <span >%(CDTbusquedasWeb_searchByWords_help)s</span>
                        </p>
                    </th>
                </tr>
            </thead>      
            <tbody>  
            \n""" % { 
        'CDTbusquedasWeb_BusquedasPorPalabrasContenidasEnSimboloOTraduccion_title':  aTranslationsCache[ 'CDTbusquedasWeb_BusquedasPorPalabrasContenidasEnSimboloOTraduccion_title'],
        'CDTbusquedasWeb_searchByWords_help':  fCRs2BRs( fCGIE( aTranslationsCache[ 'CDTbusquedasWeb_searchByWords_help'])),
    })            

             
    
              
    
    anOutput.write( u""" 

        <!-- ########################
        SubSection: Filter by String Symbol 
        #############################-->   
                                   
        <tr class="even" >
            <td align="left" valign="baseline" >
                %(CDTbusquedasWeb_TRATraduccion_attr_simbolo_label)s
            </td>
            <td align="left" valign="baseline"  >
                <input tabindex=%(tabindex)d name="theSearchSimbolo" id="theSearchSimbolo" style="font-size: 10pt;" size="36" value="%(simbolo)s" /> 
                <p class="formHelp">
                    <span>%(CDTbusquedasWeb_TRATraduccion_attr_simbolo_help)s</span>
                    <br>
                    <span >%(CDTbusquedasWeb_searchBySimbolo_help)s</span>
                </p>
            </td>
        </tr>
        \n""" % { 
        'tabindex':                                             unTabIndex,
        'simbolo':                                      fCGIE( fAsUnicode( pSearchParameters[ 'simbolo'])),
        'CDTbusquedasWeb_TRATraduccion_attr_simbolo_label':   aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_simbolo_label'],
        'CDTbusquedasWeb_TRATraduccion_attr_simbolo_help':    aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_simbolo_help'],
        'CDTbusquedasWeb_searchBySimbolo_help':               aTranslationsCache[ 'CDTbusquedasWeb_searchBySimbolo_help'],
    })
    
    
    unTabIndex += 1
    
    
    
    unasSizesIdioma = TRASizesIdioma( pCodigoIdiomaCursor)

    
    anOutput.write( u""" 

        <!-- ########################
        SubSection: Filter by Translation 
        #############################-->  
        
        <tr class="odd" >
            <td align="left" valign="baseline" >
                %(CDTbusquedasWeb_TRATraduccion_attr_cadenaTraducida_label)s
            </td>
            <td align="left" valign="baseline" >
                <input tabindex=%(tabindex)d  name="theSearchCadenaTraducida" id="theSearchCadenaTraducida" style="font-size: %(font-size)dpt;" size="%(field-size)d" value="%(cadenaTraducida)s" /> 
                <p class="formHelp">
                    <span >%(CDTbusquedasWeb_TRATraduccion_attr_cadenaTraducida_help)s</span>
                    <br>
                    <span >%(CDTbusquedasWeb_searchByTranslation_help)s</span>
                </p>
            </td>
        </tr>
        \n""" % { 
        'tabindex':                                             unTabIndex,
        'cadenaTraducida':                                      fCGIE( fAsUnicode( pSearchParameters[ 'cadenaTraducida'])),
        'CDTbusquedasWeb_TRATraduccion_attr_cadenaTraducida_label':   aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_cadenaTraducida_label'], 
        'font-size':                                            unasSizesIdioma[ 'edit_font_size'],
        'field-size':                                           unasSizesIdioma[ 'filter_field_size'] / 2,
        'CDTbusquedasWeb_TRATraduccion_attr_cadenaTraducida_help':    aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_cadenaTraducida_help'], 
        'CDTbusquedasWeb_searchByTranslation_help':                   aTranslationsCache[ 'CDTbusquedasWeb_searchByTranslation_help'], 
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
        aCDTbwProfesionalesURL,
        theThruCtxt,
        fCRs2BRs,
        fTranslateI18NCGIE,
        fAsUnicode,
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
                                %(CDTbusquedasWeb_BusquedasPorEventos_title)s
                            </strong>
                        </font>
                        <br/>
                        <font size="1">
                            <span class="formHelp" >
                                %(CDTbusquedasWeb_BusquedasPorEventos_formatoFechaISO_help)s
                                &ensp;
                                %(CDTbusquedasWeb_BusquedasPorEventos_sePermitenFechasParciales_help)s
                            </span>
                        </font>
                    </th>
                </tr>
                <tr>
                    <th align="center" >
                        <strong>%(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_label)s</strong>
                    </th>
                    <th align="left">
                        <strong>%(CDTbusquedasWeb_BusquedasPorEventos_usuario_title)s</strong>
                    </th>
                    <th align="left">
                        <strong>%(CDTbusquedasWeb_BusquedasPorEventos_despuesDeFecha_title)s
                            &ensp;-&ensp;
                            %(CDTbusquedasWeb_BusquedasPorEventos_antesDeFecha_title)s</strong>
                    </th>
                </tr>
            </thead>      
            <tbody>  
            \n""" % { 
        'CDTbusquedasWeb_BusquedasPorEventos_formatoFechaISO_help':   aTranslationsCache[ 'CDTbusquedasWeb_BusquedasPorEventos_formatoFechaISO_help'],
        'CDTbusquedasWeb_BusquedasPorEventos_sePermitenFechasParciales_help':  aTranslationsCache[ 'CDTbusquedasWeb_BusquedasPorEventos_sePermitenFechasParciales_help'],
        'CDTbusquedasWeb_BusquedasPorEventos_despuesDeFecha_title':   aTranslationsCache[ 'CDTbusquedasWeb_BusquedasPorEventos_despuesDeFecha_title'],
        'CDTbusquedasWeb_BusquedasPorEventos_antesDeFecha_title':     aTranslationsCache[ 'CDTbusquedasWeb_BusquedasPorEventos_antesDeFecha_title'],
        'CDTbusquedasWeb_BusquedasPorEventos_title':                  aTranslationsCache['CDTbusquedasWeb_BusquedasPorEventos_title'],
        'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_label':  aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_label'],
        'CDTbusquedasWeb_BusquedasPorEventos_usuario_title':          aTranslationsCache[ 'CDTbusquedasWeb_BusquedasPorEventos_usuario_title'],
    })            
    
    
    anOutput.write( u"""     
                <tr class="odd">
                    <td align="left" valign="baseline" bgColor="white">
                        <strong>%(CDTbusquedasWeb_Modificacion)s</strong>
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
                        <img  alt="TranslationStatus_%(CDTbusquedasWeb_TRATraduccion_Creada)s" src="%(portal_url)s/add_icon.gif" title="%(CDTbusquedasWeb_TRATraduccion_Creada)s" />                        
                        <font color="%(pFGcolor-Pendiente)s"><strong>%(CDTbusquedasWeb_TRATraduccion_Creada)s</strong></font>
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
                        <img  alt="TranslationStatus_%(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Traducida)s" src="%(portal_url)s/%(estado-icon-Traducida)s" title="%(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Traducida)s" />                        
                        <font color="%(pFGcolor-Traducida)s"><strong>%(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Traducida)s</strong></font>
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
                        <img  alt="TranslationStatus_%(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Revisada)s" src="%(portal_url)s/%(estado-icon-Revisada)s" title="%(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Revisada)s" />                        
                        <font color="%(pFGcolor-Revisada)s"><strong>%(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Revisada)s</strong></font>
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
                        <img  alt="TranslationStatus_%(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Definitiva)s" src="%(portal_url)s/%(estado-icon-Definitiva)s" title="%(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Definitiva)s" />                        
                        <font color="%(pFGcolor-Definitiva)s"><strong>%(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Definitiva)s</strong></font>
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
            'CDTbusquedasWeb_Modificacion':               aTranslationsCache['CDTbusquedasWeb_Modificacion'],
            'CDTbusquedasWeb_TRATraduccion_Creada':       aTranslationsCache['CDTbusquedasWeb_TRATraduccion_Creada'],
            'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Traducida':  aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_%s' % cEstadoTraduccionTraducida],
            'estado-icon-Traducida':    cIconsDict.get( cEstadoTraduccionTraducida, 'tra_traducida.gif'), 
            'usuarioCreador':           fAsUnicode( pSearchParameters[ 'usuarioCreador']),
            'fechaCreacionInicial':     fAsUnicode( pSearchParameters[ 'fechaCreacionInicial']),
            'fechaCreacionFinal':       fAsUnicode( pSearchParameters[ 'fechaCreacionFinal']),
            'usuarioTraductor':         fAsUnicode( pSearchParameters[ 'usuarioTraductor']),
            'fechaTraduccionInicial':   fAsUnicode( pSearchParameters[ 'fechaTraduccionInicial']),
            'fechaTraduccionFinal':     fAsUnicode( pSearchParameters[ 'fechaTraduccionFinal']),
            'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Revisada':    aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_%s' % cEstadoTraduccionRevisada],
            'estado-icon-Revisada':     cIconsDict.get( cEstadoTraduccionRevisada, 'tra_revisada.gif'), 
            'pBGcolor-Pendiente':       cBGColorsDict[ cEstadoTraduccionPendiente],  
            'pBGcolor-Traducida':       cBGColorsDict[ cEstadoTraduccionTraducida],  
            'pBGcolor-Revisada':        cBGColorsDict[ cEstadoTraduccionRevisada],  
            'pBGcolor-Definitiva':      cBGColorsDict[ cEstadoTraduccionDefinitiva],  
            'pFGcolor-Pendiente':       cFGColorsDict[ cEstadoTraduccionPendiente],  
            'pFGcolor-Traducida':       cFGColorsDict[ cEstadoTraduccionTraducida],  
            'pFGcolor-Revisada':        cFGColorsDict[ cEstadoTraduccionRevisada],  
            'pFGcolor-Definitiva':      cFGColorsDict[ cEstadoTraduccionDefinitiva],  
            'usuarioRevisor':           fAsUnicode( pSearchParameters[ 'usuarioRevisor']),
            'fechaRevisionInicial':     fAsUnicode( pSearchParameters[ 'fechaRevisionInicial']),
            'fechaRevisionFinal':       fAsUnicode( pSearchParameters[ 'fechaRevisionFinal']),
            'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Definitiva': aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_%s' % cEstadoTraduccionDefinitiva],
            'estado-icon-Definitiva':   cIconsDict.get( cEstadoTraduccionDefinitiva, 'tra_definitiva.gif'), 
            'usuarioCoordinador':       fAsUnicode( pSearchParameters[ 'usuarioCoordinador']),
            'fechaDefinitivoInicial':   fAsUnicode( pSearchParameters[ 'fechaDefinitivoInicial']),
            'fechaDefinitivoFinal':     fAsUnicode( pSearchParameters[ 'fechaDefinitivoFinal']),
            'usuarioModificador':       fAsUnicode( pSearchParameters[ 'usuarioModificador']),
            'fechaModificacionInicial': fAsUnicode( pSearchParameters[ 'fechaModificacionInicial']),
            'fechaModificacionFinal':   fAsUnicode( pSearchParameters[ 'fechaModificacionFinal']),
        })
     
     
   
    unTabIndex += 15  

    

    
    unTabIndex = _fRenderApplyOrCancelFiltro( 
        anOutput, 
        unContextualObject, 
        unTabIndex, 
        aPortalURL,
        aCDTbwProfesionalesURL,
        theThruCtxt,
        fCRs2BRs,
        fTranslateI18NCGIE,
        fAsUnicode,
        aTranslationsCache,
    )
    
    

    
    
    
    
    _pRenderFiltroModulos(
        anOutput, 
        unContextualObject, 
        pTodosNombresModulos, 
        pSearchParameters,
        theThruCtxt,
        fCRs2BRs,
        fTranslateI18NCGIE,
        fAsUnicode,
        aTranslationsCache,
    )
    
    
           
                    

    
    unTabIndex = _fRenderApplyOrCancelFiltro( 
        anOutput, 
        unContextualObject, 
        unTabIndex, 
        aPortalURL,
        aCDTbwProfesionalesURL,
        theThruCtxt,
        fCRs2BRs,
        fTranslateI18NCGIE,
        fAsUnicode,
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
                                %(CDTbusquedasWeb_BusquedasPorIdCadena_title)s
                            </strong>
                        </font>
                    </th>
                </tr>
            </thead>      
            <tbody>  
                <tr class="odd" >
                    <td align="left" valign="baseline" >
                        %(CDTbusquedasWeb_TRACadena_attr_id_label)s
                    </td>
                    <td align="left" valign="baseline" >
                        <input tabindex=%(tabindex)d style="font-size: 8pt;" size="12"  name="theSearchIdCadena" id="theSearchIdCadena" value="" />
                        <p class="formHelp">
                            <span>%(CDTbusquedasWeb_TRACadena_attr_id_help)s</span>
                            <br>
                            <span>%(CDTbusquedasWeb_searchById_help)s</span>
                        </p>
                    </td> 
                </tr>        
           </tbody>
        </table>
        \n""" % { 
        'tabindex':                                             unTabIndex,
        'CDTbusquedasWeb_BusquedasPorIdCadena_title': aTranslationsCache[ 'CDTbusquedasWeb_BusquedasPorIdCadena_title'],
        'CDTbusquedasWeb_TRACadena_attr_id_label':    aTranslationsCache[ 'CDTbusquedasWeb_TRACadena_attr_id_label'],
        'CDTbusquedasWeb_TRACadena_attr_id_help':     aTranslationsCache[ 'CDTbusquedasWeb_TRACadena_attr_id_help'],
        'CDTbusquedasWeb_searchById_help':            aTranslationsCache[ 'CDTbusquedasWeb_searchById_help'],
    })                                                

                           
           
      
    unTabIndex += 1
    
    

    

    
    unTabIndex = _fRenderApplyOrCancelFiltro( 
        anOutput, 
        unContextualObject, 
        unTabIndex, 
        aPortalURL,
        aCDTbwProfesionalesURL,
        theThruCtxt,
        fCRs2BRs,
        fTranslateI18NCGIE,
        fAsUnicode,
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
                                %(CDTbusquedasWeb_FiltroCadenasInactivas_title)s
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
                                <span>%(CDTbusquedasWeb_FiltroCadenasInactivas_help)s</span>
                            </font>
                        </p>
                    </td>
                </tr>
            </tbody>
        </table>
        \n""" % { 
        'is-checked':                                ( pSearchParameters[ 'cadenasInactivas'] and 'checked="checked"') or '',
        'tabindex':                                  unTabIndex,
        'CDTbusquedasWeb_FiltroCadenasInactivas_title':    aTranslationsCache[ 'CDTbusquedasWeb_FiltroCadenasInactivas_title'],
        'CDTbusquedasWeb_FiltroCadenasInactivas_help':     aTranslationsCache[ 'CDTbusquedasWeb_FiltroCadenasInactivas_help'],
    })                                                

      
    unTabIndex += 1
    
     
    
    

    
    unTabIndex = _fRenderApplyOrCancelFiltro( 
        anOutput, 
        unContextualObject, 
        unTabIndex, 
        aPortalURL,
        aCDTbwProfesionalesURL,
        theThruCtxt,
        fCRs2BRs,
        fTranslateI18NCGIE,
        fAsUnicode,
        aTranslationsCache,)
    
    
    anOutput.write( u"""<br/>""") 

    
    
    
       
    return None












def _pRenderFiltroModulos( 
    anOutput, 
    unContextualObject, 
    pTodosNombresModulos, 
    pSearchParameters,
    theThruCtxt,
    fCRs2BRs,
    fTranslateI18NCGIE,
    fAsUnicode,
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
                        <span><font size="2"><strong>%(CDTbusquedasWeb_modulesFilter_title)s</strong></font></span>
                        <br/>
                        <span class="formHelp">%(CDTbusquedasWeb_modulesFilter_help)s</span>
                    </th>
                </tr>
                <tr>
                    <th align="center" >
                    </th>   
                    <th  align="center" >
                        <input type="checkbox"  class="noborder"  value=""  name="cid_CDTbwToggleAllModules" id="cid_CDTbwToggleAllModules" 
                            onchange="pTRAToggleAllModules(); return true;" />
                            
                    </th>
                </tr>
            </head>
            <tbody>   
            \n""" % {
        'CDTbusquedasWeb_seleccionarTodos_label':                 aTranslationsCache[ 'CDTbusquedasWeb_seleccionarTodos_label'],
        'CDTbusquedasWeb_seleccionarNinguno_label':               aTranslationsCache[ 'CDTbusquedasWeb_seleccionarNinguno_label'],
        'CDTbusquedasWeb_modulesFilter_title':                    aTranslationsCache[ 'CDTbusquedasWeb_modulesFilter_title'],
        'CDTbusquedasWeb_modulesFilter_help':                     fCRs2BRs( aTranslationsCache[ 'CDTbusquedasWeb_modulesFilter_help']),
        'CDTbusquedasWeb_refrescar_action_label':                 aTranslationsCache[ 'CDTbusquedasWeb_refrescar_action_label'],                
    })
    
    unIndexRowModulo = 0
    for unNombreModulo in pTodosNombresModulos:  
                                 
        anOutput.write( u"""                                                                                                                                                                     
            <tr class="%(class-row-modulo)s" >
                <td align="left" valign="center" onclick="toggleModulo( '%(index-modulo)s'); return true;" class="CDTbwStyle_Clickable"  >                
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
            'nombre-modulo':        fAsUnicode( unNombreModulo),        
            'modulo-checked':       (( unNombreModulo in unosNombresModulos) and 'checked="checked"') or '',
        } )
        
        unIndexRowModulo += 1

    anOutput.write( u"""  
                <tr class="%(class-row-modulo)s" >
                    <td align="left" valign="center" onclick="toggleModulo( '%(index-modulo)s'); return true;" class="CDTbwStyle_Clickable"  >                
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
    aCDTbwProfesionalesURL       =None,
    fCGIE              =None,
    fCRs2BRs          =None,
    fTranslateI18NCGIE    =None,
    fAsUnicode        =None,
    aTranslationsCache =None,):
    """Render as collapsible the go to section of the translations browser.
    
    """    
    
    _pRenderCollapsible_Lambda(  anOutput,
        aTranslationsCache[ 'CDTbusquedasWeb_seccionGoTo_title'],
        u'elid_GoTo_collapsible_dl', 
        lambda : _pRenderGoTo( 
            anOutput           =anOutput, 
            unContextualObject =unContextualObject, 
            pNumberOfStrings   =pNumberOfStrings,
            pNumberOfPages     =pNumberOfPages,
            pSearchParameters  =pSearchParameters,
            aPortalURL         =aPortalURL,
            aCDTbwProfesionalesURL       =aCDTbwProfesionalesURL,
            fCGIE              =theThruCtxt, 
            fCRs2BRs          =fCRs2BRs, 
            fTranslateI18NCGIE    =fTranslateI18NCGIE, 
            fAsUnicode        =fAsUnicode, 
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
    aCDTbwProfesionalesURL,
    theThruCtxt,
    fCRs2BRs,
    fTranslateI18NCGIE,
    fAsUnicode,
    aTranslationsCache):
    """Render the filter section of the translations browser.
    
    """    

    unTabIndex = 11
    
    anOutput.write( u"""    

        <!-- #################################################################
        SECTION: Specify the first symbol to show in the list
        ################################################################# -->
                      
        <br/>
        <input tabindex=%(tabindex)d name="form_submit" style="font-size: 10pt; font-style: italic"  value="%(CDTbusquedasWeb_refrescar_action_label)s" type="submit"/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <input tabindex=%(tabindex2)d type="button" name="todos" style="font-size: 9pt; "  value="%(CDTbusquedasWeb_first_label)s" onclick="pTRAResetGoToParameters(); return true;" class="CDTbwStyle_Clickable"  />
        <br/>
        \n""" % { 
        'tabindex':                                                    unTabIndex,
        'tabindex2':                                                   unTabIndex + 1,
        'CDTbusquedasWeb_refrescar_action_label':                            aTranslationsCache[ 'CDTbusquedasWeb_refrescar_action_label'],
        'CDTbusquedasWeb_first_label':                                       aTranslationsCache[ 'CDTbusquedasWeb_first_label'],                
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
                                %(CDTbusquedasWeb_GoToParameters_title)s
                            </strong>
                        </font>
                    </th>
                </tr>
            </thead>      
            <tbody>  
            \n""" % { 
        'CDTbusquedasWeb_GoToParameters_title':  aTranslationsCache[ 'CDTbusquedasWeb_GoToParameters_title'], 
    })            

             
    
              
    
    anOutput.write( u""" 

        <!-- ########################
        SubSection: GoTo Parameter by Symbol Index Number
        #############################-->   
                                   
        <tr class="even" >
            <td align="left" valign="baseline" >
                %(CDTbusquedasWeb_TranslationsPage_GoTo_SymbolIndex_label)s
                %(CDTbusquedasWeb_TranslationsPage_GoTo_SymbolIndex_of)s
                %(pNumberOfStrings)s
                <p class="formHelp">%(CDTbusquedasWeb_TranslationsPage_GoTo_SymbolIndex_help)s</p>
            </td>
            <td align="left" valign="baseline"  >
                <input type="text" tabindex=%(tabindex)d name="theGoToResultIndex" id="theGoToResultIndex" style="font-size: 10pt;" size="6" maxlength="6" value="" /> 
            </td>
        </tr>
        \n""" % { 
        'tabindex':                                             unTabIndex,
        'pNumberOfStrings':                                     fAsUnicode( str( pNumberOfStrings)),
        'CDTbusquedasWeb_TranslationsPage_GoTo_SymbolIndex_label':    aTranslationsCache[ 'CDTbusquedasWeb_TranslationsPage_GoTo_SymbolIndex_label'],
        'CDTbusquedasWeb_TranslationsPage_GoTo_SymbolIndex_of':       aTranslationsCache[ 'CDTbusquedasWeb_TranslationsPage_GoTo_SymbolIndex_of'],
        'CDTbusquedasWeb_TranslationsPage_GoTo_SymbolIndex_help':     aTranslationsCache[ 'CDTbusquedasWeb_TranslationsPage_GoTo_SymbolIndex_help'],
    })
    
    
    unTabIndex += 1
    
    
    
            
    
    anOutput.write( u""" 

        <!-- ########################
        SubSection: GoTo Parameter by Page Index Number
        #############################-->   
                                   
        <tr class="odd" >
            <td align="left" valign="baseline" >
                %(CDTbusquedasWeb_TranslationsPage_GoTo_PageIndex_label)s
                %(CDTbusquedasWeb_TranslationsPage_GoTo_PageIndex_of)s
                %(pNumberOfPages)s
                <p class="formHelp">%(CDTbusquedasWeb_TranslationsPage_GoTo_PageIndex_help)s</p>
            </td>
            <td align="left" valign="baseline"  >
                <input type="text" tabindex=%(tabindex)d name="theGoToPageIndex" id="theGoToPageIndex" style="font-size: 10pt;" size="4" maxlength="4" value="" /> 
            </td>
        </tr>
        \n""" % { 
        'tabindex':                                             unTabIndex,
        'pNumberOfPages':                                     fAsUnicode( str( pNumberOfPages)),
        'CDTbusquedasWeb_TranslationsPage_GoTo_PageIndex_label':    aTranslationsCache[ 'CDTbusquedasWeb_TranslationsPage_GoTo_PageIndex_label'],
        'CDTbusquedasWeb_TranslationsPage_GoTo_PageIndex_of':       aTranslationsCache[ 'CDTbusquedasWeb_TranslationsPage_GoTo_PageIndex_of'],
        'CDTbusquedasWeb_TranslationsPage_GoTo_PageIndex_help':     aTranslationsCache[ 'CDTbusquedasWeb_TranslationsPage_GoTo_PageIndex_help'],
    })
    
    
    unTabIndex += 1
    
    

    anOutput.write( u""" 

        <!-- ########################
        SubSection: GoTo Parameter by Symbol starting with characters
        #############################-->   
                                   
        <tr class="even" >
            <td align="left" valign="baseline" >
                %(CDTbusquedasWeb_TranslationsPage_GoTo_SymbolStartingWithChars_label)s
                <p class="formHelp">%(CDTbusquedasWeb_TranslationsPage_GoTo_SymbolStartingWithChars_help)s</p>
            </td>
            <td align="left" valign="baseline"  >
                <input type="text" tabindex=%(tabindex)d name="theGoToSymbolStartingWith" id="theGoToSymbolStartingWith" style="font-size: 9pt;" size="16" maxlength="64" value="" /> 
            </td>
        </tr>
        \n""" % { 
        'tabindex':                                           unTabIndex,
        'CDTbusquedasWeb_TranslationsPage_GoTo_SymbolStartingWithChars_label':    aTranslationsCache[ 'CDTbusquedasWeb_TranslationsPage_GoTo_SymbolStartingWithChars_label'], 
        'CDTbusquedasWeb_TranslationsPage_GoTo_SymbolStartingWithChars_help':     aTranslationsCache[ 'CDTbusquedasWeb_TranslationsPage_GoTo_SymbolStartingWithChars_help'], 
    })
    
    
    unTabIndex += 1
    
    

    anOutput.write( u"""  
            </tbody>
        </table>
        <br/>
        \n""")                                 
             
    
    anOutput.write( u"""     
        <input tabindex=%(tabindex)d name="form_submit" style="font-size: 10pt; font-style: italic"  value="%(CDTbusquedasWeb_refrescar_action_label)s" type="submit"/>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <input tabindex=%(tabindex2)d type="button" name="todos" style="font-size: 9pt; "  value="%(CDTbusquedasWeb_first_label)s" onclick="pTRAResetGoToParameters(); return true;" class="CDTbwStyle_Clickable"  />
        <br/>
        <br/>
        \n""" % { 
        'tabindex':                                                    unTabIndex,
        'tabindex2':                                                   unTabIndex + 1,
        'CDTbusquedasWeb_refrescar_action_label':                            aTranslationsCache[ 'CDTbusquedasWeb_refrescar_action_label'],                
        'CDTbusquedasWeb_first_label':                                       aTranslationsCache[ 'CDTbusquedasWeb_first_label'],                
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
    aCDTbwProfesionalesURL                =None,
    fCGIE                       =None,
    fCRs2BRs                   =None,
    fTranslateI18NCGIE             =None,
    fAsUnicode                 =None,
    aTranslationsCache          =None, ):
    """Render as collapsible the summary section of the translations browser.
    
    """    
    
    _pRenderCollapsible_Lambda(  anOutput,
        aTranslationsCache[ 'CDTbusquedasWeb_seccionInformeSumario_title'],
        u'elid_Summary_collapsible_dl', 
        lambda : _pRenderInforme( 
            anOutput                    =anOutput,
            unContextualObject          =unContextualObject,
            pEstadosIncluidos           =pEstadosIncluidos,
            pInformeEstadosTodasCadenas =pInformeEstadosTodasCadenas,
            pInformeEstadosFiltrados    =pInformeEstadosFiltrados,
            pBrowsingInactiveStrings    =pBrowsingInactiveStrings,
            aPortalURL                  =aPortalURL,
            aCDTbwProfesionalesURL                =aCDTbwProfesionalesURL,
            fCGIE                       =fCGIE  ,
            fCRs2BRs                   =fCRs2BRs,
            fTranslateI18NCGIE             =fTranslateI18NCGIE,
            fAsUnicode                 =fAsUnicode,
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
    aCDTbwProfesionalesURL,
    theThruCtxt,
    fCRs2BRs,
    fTranslateI18NCGIE,
    fAsUnicode,
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
        y numero y porcentaje de Resultados en cada estado
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
            \n""" % aTranslationsCache[ 'CDTbusquedasWeb_BrowsingInactiveStrings_label']
        )
    
            
        
    anOutput.write( u"""    

        <!-- #################################################################
        SECTION: Informe de traducciones en TRAIdioma:
        Total de cadenas en catalogo, 
        y numero y porcentaje de Resultados en cada estado
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
                <font size="%(cInformeBiggerFontSize)s">%(CDTbusquedasWeb_total_label)s</font>
            </td>
        \n""" % { 
        'CDTbusquedasWeb_ocultar_action_label'  : aTranslationsCache[ 'CDTbusquedasWeb_ocultar_action_label'], 
        'CDTbusquedasWeb_informe_section_label' : aTranslationsCache[ 'CDTbusquedasWeb_informe_section_label'],  
        'CDTbusquedasWeb_total_label':            aTranslationsCache[ 'CDTbusquedasWeb_total_label'], 
        'cInformeBiggerFontSize':           cInformeBiggerFontSize,
    })

    for unEstado in cTodosEstados:                                  
        anOutput.write( u"""                 
            <td align="center" valign="top" colspan="2" >
                <font size="%(cInformeBiggerFontSize)s" >
                    <img  alt="TranslationStatus_%(unEstado)s" src="%(portal_url)s/%(estado-icon)s" title="%(unEstado)s" />                        
                    %(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_label)s
                </font>
                <br/>  
                <table align="center" width="100%%" cellspacing="0" cellpadding="0" frame="void" >
                    <tr height="8" ><td valign="top" bgColor="%(pBGcolor)s" /></tr>
                </table>  
            </td>
            \n""" % { 
            'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_label': fTranslateI18NCGIE( 'CDTbusquedasWeb','CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_%s' % unEstado, unEstado),
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
                <font size="%(cInformeBiggerFontSize)s" >%(CDTbusquedasWeb_todastraduccionesidioma_label)s</font>
            </td>
            <td align="right" valign="baseline" >
                <font size="%(cInformeBiggerFontSize)s" >%(pNumeroCadenas)d</font>
            </td>
            <td align="right" valign="baseline" >
                &nbsp;
            </td>
            \n""" % { 
        'CDTbusquedasWeb_todastraduccionesidioma_label': fTranslateI18NCGIE( 'CDTbusquedasWeb', 'CDTbusquedasWeb_todas_label', 'All-'),
        'pNumeroCadenas':                                  pNumeroCadenas,
        'cInformeBiggerFontSize':                          cInformeBiggerFontSize,
    })

    for unEstado in cTodosEstados:                                  
        anOutput.write( u"""                                                         
            <td align="right" valign="baseline" >
                <font size="%(cInformeBiggerFontSize)s" >%(pNumeroResultadosEstado)d</font>
            </td>
            <td align="right" valign="baseline" >
                <font size="1" >%(pPorcentajeResultadosEstado)d%%</font>
            </td>
            \n""" % { 
            'pNumeroResultadosEstado':      pInformeEstadosTodasCadenas[ unEstado][ 1], 
            'pPorcentajeResultadosEstado':  pInformeEstadosTodasCadenas[ unEstado][ 2],
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
                    <font size="%(cInformeBiggerFontSize)s" >%(CDTbusquedasWeb_traduccionesfiltradasidioma_label)s</font>
                </td>
                \n""" % { 
            'CDTbusquedasWeb_traduccionesfiltradasidioma_label': fTranslateI18NCGIE( 'CDTbusquedasWeb', 'CDTbusquedasWeb_traduccionesfiltradasidioma_label', 'Filtered-'),
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
                        <font size="%(cInformeBiggerFontSize)s" >%(pNumeroResultadosEstado)d</font>
                    </td>
                    <td align="right" valign="baseline" >
                        <font size="1" >%(pPorcentajeResultadosEstado)d%%</font>
                    </td>
                    \n""" % { 
                    'pNumeroResultadosEstado':        pInformeEstadosFiltrados[ unEstado][ 1], 
                    'pPorcentajeResultadosEstado':    pInformeEstadosFiltrados[ unEstado][ 2],
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
    aCDTbwProfesionalesURL,
    theThruCtxt,
    fCRs2BRs,
    fTranslateI18NCGIE,
    fAsUnicode,
    aTranslationsCache):
    """Render the details subsection of the editor section of the translations browser.
    
    """
             
    pIndex  = 0     
    
    anOutput.write( u"""    
        <!-- #################################################################
        SECTION: Editor DETAILS for selected TRATraduccion
        ################################################################# -->
        <div id="cid_CDTbwEditorDetalle" class="CDTbwStyle_Display">
    
            <table width="100%%" cellspacing="0" cellpadding="0" frame="void" id="editor_TRATraduccion" >
                <tbody>
                \n"""
    )
          
    

    anOutput.write( u"""
        <!-- #####
        ## Fields: display TRATraduccion cadena symbol and id, and translation changes counter.
        ##########-->  
            <tr class="CDTbwStyle_NoDisplay" id="cid_CDTbwEditorDetalle_simboloCadena_row">
                <td align="left" valign="baseline" >                
                    <font size="1" ><strong>%(CDTbusquedasWeb_Symbol_title)s</strong></font>
                    &emsp;
                </td>
                <td  align="left" valign="baseline"  colspan="2">                
                    <font size="1" ><span id="cid_CDTbwEditorDetalle_simboloCadena" ></span></font>
                </td>
            </tr>
            <tr class="CDTbwStyle_NoDisplay" id="cid_CDTbwEditorDetalle_idCadena_row">            
                <td align="left" valign="baseline" >       
                    <font size="1" ><strong>%(CDTbusquedasWeb_TRACadena_attr_id_label)s</strong></font>
                    &emsp;
                </td>
                <td align="left" valign="baseline" colspan="2">       
                    <font size="1" ><span id="cid_CDTbwEditorDetalle_idCadena" ></span></font>
                </td>
            </tr>
            <tr class="CDTbwStyle_NoDisplay" id="cid_CDTbwEditorDetalle_contadorCambios_row">            
                <td align="left" valign="baseline" >       
                    <font size="1" ><strong>%(CDTbusquedasWeb_TRATraduccion_attr_contadorCambios_label)s</strong></font>
                    &emsp;
                </td>
                <td align="left" valign="baseline" colspan="2">       
                    <font size="1" ><span id="cid_CDTbwEditorDetalle_contadorCambios" ></span></font>
                </td>
            </tr>
        \n""" % { 
        'CDTbusquedasWeb_Symbol_title':               aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_simbolo_label'], 
        'CDTbusquedasWeb_TRACadena_attr_id_label':    aTranslationsCache[ 'CDTbusquedasWeb_TRACadena_attr_id_label'], 
        'CDTbusquedasWeb_TRATraduccion_attr_contadorCambios_label':    aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_contadorCambios_label'], 
        'pClassFila':                           cClasesFilas [pIndex %2],
    })
    
        
    
    
    if pAllowChangeStringsModules:
        
        anOutput.write( u"""
            <!-- #####
            ## Fields: display TRATraduccion nombresModulos and open string modules editor open button.
            ##########-->  
                <tr class="CDTbwStyle_NoDisplay" id="cid_CDTbwEditorDetalle_nombresModulos_row">
                    <td align="left" valign="baseline" >                
                        <font size="1" ><strong>%(CDTbusquedasWeb_Modulos_title)s</strong></font>
                        &emsp;
                        <input  
                            onmouseup="fTRAEvtHlr_Editor_Button_EditModules_OnMouseUp( )"
                            onkeypress="fTRAEvtHlr_Editor_Button_EditModules_OnKeyPress( event)"
                            id="TRAEditModulesButton" 
                            class="CDTbwStyle_Display CDTbwStyle_Clickable" 
                            name="TRAEditModulesButton" 
                            value="%(action_name)s" 
                            type="button" 
                            style="color: Green; font-size: 8pt; font-style: italic; font-weight: 300" />                    
                        
                    </td>
                    <td  align="left" valign="baseline"  colspan="2">                
                        <font size="1" ><span id="cid_CDTbwEditorDetalle_nombresModulos" ></span></font>
                    </td>
                </tr>
            \n""" % { 
            'CDTbusquedasWeb_Modulos_title':              aTranslationsCache[ 'CDTbusquedasWeb_Modulos_title'], 
            'pClassFila':                           cClasesFilas [pIndex %2],
            'action_name':                          aTranslationsCache[ 'CDTbusquedasWeb_ModulesEditor_Open'], 
        })
    
        _pRenderEditorModulos( 
            anOutput, 
            unContextualObject, 
            pTodosNombresModulos, 
            theThruCtxt,
            fCRs2BRs,
            fTranslateI18NCGIE,
            fAsUnicode,
            aTranslationsCache,
        )
        
    else:
        anOutput.write( u"""
            <!-- #####
            ## Fields: display TRATraduccion nombresModulos 
            ##########-->  
                <tr class="CDTbwStyle_NoDisplay" id="cid_CDTbwEditorDetalle_nombresModulos_row">
                    <td align="left" valign="baseline" >                
                        <font size="1" ><strong>%(CDTbusquedasWeb_Modulos_title)s</strong></font>                        
                    </td>
                    <td  align="left" valign="baseline"  colspan="2">                
                        <font size="1" ><span id="cid_CDTbwEditorDetalle_nombresModulos" ></span></font>
                    </td>
                </tr>
            \n""" % { 
            'CDTbusquedasWeb_Modulos_title':              aTranslationsCache[ 'CDTbusquedasWeb_Modulos_title'], 
            'pClassFila':                           cClasesFilas [pIndex %2],
        })
        
        

        
    
    pIndex  += 1
        

                
    anOutput.write( u"""
        <!-- #####
        ## Fields: display TRATraduccion referenciasFuentes 
        ##########-->  
            <tr class="CDTbwStyle_NoDisplay" id="cid_CDTbwEditorDetalle_referenciasFuentes_row">
                <td align="left" valign="baseline" >                
                    <font size="1" ><strong>%(CDTbusquedasWeb_Fuentes_title)s</strong></font>                        
                </td>
                <td  align="left" valign="baseline"  colspan="2">                
                    <font size="1" ><span id="cid_CDTbwEditorDetalle_referenciasFuentes" ></span></font>
                </td>
            </tr>
        \n""" % { 
        'CDTbusquedasWeb_Fuentes_title':              aTranslationsCache[ 'CDTbusquedasWeb_Fuentes_title'], 
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
        <tr class="CDTbwStyle_NoDisplay" id="cid_CDTbwEditorDetalle_Definitiva" >
            <td align="left" valign="baseline"  >                
                <font size="1"><strong>%(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Definitiva)s</strong></font>
            </td>
            <td align="left" valign="baseline"  >                
                <font size="1">
                    %(CDTbusquedasWeb_fecha_el)s
                    &nbsp;
                    <span id="cid_CDTbwEditorDetalle_Definitiva_Fecha"      ></span>
                    &ensp;
                </font>
            </td>
            <td align="left" valign="baseline"  >  
                <font size="1">
                    %(CDTbusquedasWeb_usuario_por)s
                    &nbsp;
                    <span id="cid_CDTbwEditorDetalle_Definitiva_Usuario"    ></span>
                </font>
            </td>
        </tr>
        \n""" % { 
        'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Definitiva': aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Definitiva'],
        'CDTbusquedasWeb_fecha_el':                                              aTranslationsCache[ 'CDTbusquedasWeb_fecha_el'],
        'CDTbusquedasWeb_usuario_por':                                           aTranslationsCache[ 'CDTbusquedasWeb_usuario_por'],
    })

                        
    pIndex = pIndex + 1              
      
    
    
    
    anOutput.write( u"""                
        <tr class="CDTbwStyle_NoDisplay" id="cid_CDTbwEditorDetalle_Revisada" >
            <td align="left" valign="baseline"  >                
                <font size="1"><strong>%(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Revisada)s</strong>
            </td>
            <td align="left" valign="baseline"  >                
                <font size="1">
                    %(CDTbusquedasWeb_fecha_el)s
                    &nbsp;
                    <span id="cid_CDTbwEditorDetalle_Revisada_Fecha"      ></span>
                    &ensp;
                </font>
            </td>
            <td align="left" valign="baseline"  >  
                <font size="1">
                    %(CDTbusquedasWeb_usuario_por)s
                    &nbsp;
                    <span id="cid_CDTbwEditorDetalle_Revisada_Usuario"    ></span>
                </font>
            </td>
        </tr>
        \n""" % { 
        'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Revisada': aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Revisada'],
        'CDTbusquedasWeb_fecha_el':                                            aTranslationsCache[ 'CDTbusquedasWeb_fecha_el'],
        'CDTbusquedasWeb_usuario_por':                                         aTranslationsCache[ 'CDTbusquedasWeb_usuario_por'],
    })
    pIndex = pIndex + 1    
    
        
        
        
                                    
    anOutput.write( u"""                
        <tr class="CDTbwStyle_NoDisplay" id="cid_CDTbwEditorDetalle_Traducida" >
            <td align="left" valign="baseline"  >                
                <font size="1"><strong>%(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Traducida)s</strong>
            </td>
            <td align="left" valign="baseline"  >                
                <font size="1">
                    %(CDTbusquedasWeb_fecha_el)s
                    &nbsp;
                    <span id="cid_CDTbwEditorDetalle_Traducida_Fecha"      ></span>
                    &ensp;
                </font>
            </td>
            <td align="left" valign="baseline"  >  
                <font size="1">
                    %(CDTbusquedasWeb_usuario_por)s
                    &nbsp;
                    <span id="cid_CDTbwEditorDetalle_Traducida_Usuario"    ></span>
                </font>
            </td>
        </tr>
        \n""" % { 
        'CDTbusquedasWeb_fecha_el':                                          aTranslationsCache[ 'CDTbusquedasWeb_fecha_el'],
        'CDTbusquedasWeb_usuario_por':                                       aTranslationsCache[ 'CDTbusquedasWeb_usuario_por'],
        'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Traducida': aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Traducida'],
    })

    pIndex = pIndex + 1              

        
    anOutput.write( u"""                
        <tr class="CDTbwStyle_NoDisplay" id="cid_CDTbwEditorDetalle_Creada" >
            <td align="left" valign="baseline"  >                
                <font size="1"><strong>%(CDTbusquedasWeb_TRATraduccion_Creada)s</strong>
            </td>
            <td align="left" valign="baseline"  >                
                <font size="1">
                    %(CDTbusquedasWeb_fecha_el)s
                    &nbsp;
                    <span id="cid_CDTbwEditorDetalle_Creada_Fecha"      ></span>
                    &ensp;
                </font>
            </td>
            <td align="left" valign="baseline"  >  
                <font size="1">
                    %(CDTbusquedasWeb_usuario_por)s
                    &nbsp;
                    <span id="cid_CDTbwEditorDetalle_Creada_Usuario"    ></span>
                </font>
            </td>
        </tr>
         \n""" % { 
        'CDTbusquedasWeb_fecha_el':               aTranslationsCache[ 'CDTbusquedasWeb_fecha_el'],
        'CDTbusquedasWeb_usuario_por':            aTranslationsCache[ 'CDTbusquedasWeb_usuario_por'],
        'CDTbusquedasWeb_TRATraduccion_Creada':   aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_Creada'],
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
                    #<input name="form_submit" value="%(CDTbusquedasWeb_comentar_action_label)s" type="submit" style="color: Red; font-size: 8pt; font-style: italic" />                                                
                #</td>
                #\n""" % { 
            #'CDTbusquedasWeb_comentar_action_label':      aTranslationsCache[ 'CDTbusquedasWeb_comentar_action_label'], 
            #'pClassFila': cClasesFilas [pIndex %2],
        #})
            
    #else:
        #pReadOnly = 'readonly="readonly"'
        #anOutput.write( u"""
            #<tr class="%(pClassFila)s">                        
                #<td  align="right" valign="top" >                
                    #<font size="1" ><strong>%(CDTbusquedasWeb_comentar_action_label)s</strong><font/>                                                
                #</td>
                #\n""" % { 
            #'CDTbusquedasWeb_comentar_action_label':      aTranslationsCache[ 'CDTbusquedasWeb_comentar_action_label'], 
            #'pClassFila': cClasesFilas [pIndex %2],
        #})
            
            
    #anOutput.write( u"""
        #<td colspan="3" align="left" valign="top" >                
            #<textarea name="Comentario" %(pReadOnly)s style="font-size: 10pt;" cols="68" rows="%(rows)d" id="Comentario" >""" % { 
        #'CDTbusquedasWeb_comentar_action_label':      aTranslationsCache[ 'CDTbusquedasWeb_comentar_action_label'], 
        #'rows':                                         min( max( 1, len( pComentarioTraduccion.splitlines())), 12), 
        #'pReadOnly' : pReadOnly, 
    #}) 
        
    #for unaLinea in pComentarioTraduccion.splitlines():
        #anOutput.write( u"""%(unaLinea)s\n""" % { 'unaLinea': fAsUnicode( unaLinea),} )
                
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
    theThruCtxt,
    fCRs2BRs,
    fTranslateI18NCGIE,
    fAsUnicode,
    aTranslationsCache):
    """Render  the section to edit string modules.
    
    """    

    if not pTodosNombresModulos:
        return None
    
    
    anOutput.write( u"""  
        
        <!-- #################################################################
        SECTION: Edition of modules for a string
        ################################################################# -->                           
        <tr id="cid_CDTbwEditorDetalle_Modulos" class="CDTbwStyle_NoDisplay">
            <td/>
            <td id="cid_CDTbwEditorDetalle_Modulos_Editor" >
                <table align="left" valign="top" id="sct_Edit_Modules_String" summary="Edit string modules" cellspacing="0" cellpadding="0" frame="void">
                    <tbody>   
                \n""" 
    )
    
    unIndexRowModulo = 0 
    for unNombreModulo in pTodosNombresModulos:  
                                 
        anOutput.write( u"""                                                                                                                                                                     
                        <tr >
                            <td align="left" valign="center" class="CDTbwStyle_Clickable"  >                
                                <font size="1" >
                                    <strong>
                                        %(nombre-modulo)s
                                    </strong>
                                </font>
                            </td>
                            <td align="left" valign="center" >    
                                &emsp;
                                <input type="checkbox" class="noborder"  value="%(nombre-modulo)s" name="theEditNombresModulos" 
                                    id="cid_CDTbwEditorDetalle_Modulos_%(index-modulo)s" />
                            </td>
                        </tr>
            \n""" % { 
            'index-modulo':         str( unIndexRowModulo),
            'nombre-modulo':        fAsUnicode( unNombreModulo),        
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
                    class="CDTbwStyle_Display CDTbwStyle_Clickable" 
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
        'action_name':  aTranslationsCache[ 'CDTbusquedasWeb_ModulesEditor_SaveStringModules'], 
    })
    
    return None
                
  













    
def _pRenderCollapsibleHistory( 
    anOutput            =None,                        
    unContextualObject  =None,                                  
    pCodigoIdiomaCursor =None,                                   
    pRegistrosHistoria  =None,                                  
    aPortalURL          =None,                         
    aCDTbwProfesionalesURL        =None,                           
    fCGIE               =None,                    
    fCRs2BRs           =None,                        
    fTranslateI18NCGIE     =None,                              
    fAsUnicode         =None,                          
    aTranslationsCache  =None, ):
    """Render as collapsible the selected translation history section of the translations browser.
    
    """
    
    _pRenderCollapsible_Lambda(  anOutput,
        aTranslationsCache[ 'CDTbusquedasWeb_seccionHistory_title'],
        u'elid_History_collapsible_dl', 
        lambda : _pRenderHistory( 
            anOutput            =anOutput,                        
            unContextualObject  =unContextualObject,                                  
            pCodigoIdiomaCursor =pCodigoIdiomaCursor,                                   
            pRegistrosHistoria  =pRegistrosHistoria,                                  
            aPortalURL          =aPortalURL,                         
            aCDTbwProfesionalesURL        =aCDTbwProfesionalesURL,                           
            fCGIE               =theThruCtxt,                    
            fCRs2BRs           =fCRs2BRs,                        
            fTranslateI18NCGIE     =fTranslateI18NCGIE,                              
            fAsUnicode         =fAsUnicode,                          
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
    aCDTbwProfesionalesURL,
    theThruCtxt,
    fCRs2BRs,
    fTranslateI18NCGIE,
    fAsUnicode,
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
                        <font size="1" >%(CDTbusquedasWeb_historiafechaaccion_label)s</font>
                    </th>
                    <th  align="left" valign="baseline" >   
                        <font size="1" >%(CDTbusquedasWeb_historiausuarioactor_label)s</font>
                    </th>
                    <th  align="left" valign="baseline" >   
                        <font size="1" >%(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_label)s</font>
                    </th>
                </tr>
            </thead>      
            <tbody>                    
            \n""" % {                                  
        'CDTbusquedasWeb_historiafechaaccion_label':                      aTranslationsCache[ 'CDTbusquedasWeb_historiafechaaccion_label'],
        'CDTbusquedasWeb_historiausuarioactor_label':                     aTranslationsCache[ 'CDTbusquedasWeb_historiausuarioactor_label'],
        'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_label':      aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_label'], 
    })


    for pRegistroHistoria in pRegistrosHistoria:
        
        unaTraduccionHistoria = pRegistroHistoria.get(  cHistory_Translation, '').strip()
        unComentarioHistoria  = pRegistroHistoria.get(  cHistory_Comment, '').strip()
        
        unStyleToBorder_Infos = ""
        
        if ( not unaTraduccionHistoria) and ( ( not pRegistroHistoria.get(  cHistory_ActionKind, '') == 'Comentar') or ( not unComentarioHistoria)):
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
            'accion':           aTranslationsCache.get( 'CDTbusquedasWeb_TranslationHistoryAction_%s' % ( pRegistroHistoria.get( cHistory_ActionKind, '') or cTranslationHistoryAction_Desconocida), ( pRegistroHistoria.get( cHistory_ActionKind, '') or cTranslationHistoryAction_Desconocida),), 
            'fechaAccion':      pRegistroHistoria.get( cHistory_ActionDate, ''),  
            'usuarioActor':     fAsUnicode( pRegistroHistoria.get( cHistory_User, '')),  
        })
                                                
                                                
        if  pRegistroHistoria.get( cHistory_Status, ''):
                            
            anOutput.write( u"""                                             
                    <td %(unStyleToBorder_Infos)s  align="center" valign="baseline" bgcolor="%(pBGColor)s">   
                        <font color="%(pFGColor)s" size="1"><strong>%(estadoTraduccion)s</strong></font>
                    </td>
                </tr>           
                \n""" % { 
                'unStyleToBorder_Infos': unStyleToBorder_Infos,
                'pBGColor':             cBGColorsDict.get( pRegistroHistoria.get( cHistory_Status,'') , cFGColorsDict[ cEstadoTraduccionPendiente]), 
                'pFGColor':             cFGColorsDict.get( pRegistroHistoria.get( cHistory_Status,'') , cFGColorsDict[ cEstadoTraduccionPendiente]),
                'estadoTraduccion':     aTranslationsCache.get( 'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_%s' % pRegistroHistoria.get( cHistory_Status, ''), pRegistroHistoria.get( cHistory_Status, '')), 
            })
        else:
            anOutput.write( u"""                                                                                                                        
                    <td />
                </tr>           
                \n""" )

            
        if ( pRegistroHistoria.get(  cHistory_ActionKind, '') == 'Comentar') and unComentarioHistoria:
            anOutput.write( u"""                                                                                                                                                      
                <tr class="%(pClassFila)s" >
                    <td style="border-bottom: 1px solid"  align="left" valign="baseline" colspan="4" >   
                        <font size="1" >%(comentario)s</font>
                    </td>
                </tr>
                \n""" % { 
                'pClassFila':                          cClasesFilas [ pIndex %2], 
                'comentario':                          fCGIE( fAsUnicode( fCRs2BRs( pRegistroHistoria.get(  cHistory_Comment, '')))), 
                'CDTbusquedasWeb_historiacomentario_label':  aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_comentario_label'], 
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
                    'cadenaTraducida':                                 fCGIE( fAsUnicode( unaTraduccionHistoria)), 
                    'CDTbusquedasWeb_TRATraduccion_attr_cadenaTraducida_label':  aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_cadenaTraducida_label'], 
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
    aCDTbwProfesionalesURL,
    theThruCtxt,
    fCRs2BRs,
    fTranslateI18NCGIE,
    fAsUnicode,
    aTranslationsCache):

    anOutput.write( u"""
 
        <!-- #####
        ## SECTION: Editor area and buttons
        ##########-->  
    
        <div id="cid_CDTbwEditorAreaYBotones" class="CDTbwStyle_NoDisplay">
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
        'class-Display':                                ((( unEstadoTraduccion in [ cEstadoTraduccionPendiente, cEstadoTraduccionTraducida,]) and ( len( set( [ cEstadoTraduccionPendiente, cEstadoTraduccionTraducida,]).intersection( unosAllowedTargetStates)) > 0)) and 'CDTbwStyle_Display') or 'CDTbwStyle_NoDisplay',
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
            <img class="%(class-Display)s CDTbwStyle_Clickable"
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
                class="%(class-Display)s CDTbwStyle_Clickable"                
                name="TRAStatusChangeButton_Traducir" 
                value="%(action_name)s" 
                type="button" 
                style="color: red; font-size: 9pt; font-style: italic; font-weight: 700" />
        </td>        
        \n""" % { 
        'unButtonsColumnsWidthString': unButtonsColumnsWidthString,
        'accion-Traducir':        cAccion_Traducir,
        'action_name':            aTranslationsCache[ 'CDTbusquedasWeb_TranslationAction_Grabar'], 
        'estado-icon-Traducida':  cIconsDict.get( cEstadoTraduccionTraducida, 'tra_traducida.gif'),
        'portal_url':             aPortalURL, 
        'class-Display':          ((( unEstadoTraduccion in [ cEstadoTraduccionPendiente, cEstadoTraduccionTraducida,]) and ( len( set( [ cEstadoTraduccionPendiente, cEstadoTraduccionTraducida,]).intersection( unosAllowedTargetStates)) > 0)) and 'CDTbwStyle_Display') or 'CDTbwStyle_NoDisplay',
    })
   
      
 

    
    if pAllowInvalidateStringTranslations:
        anOutput.write( u"""  
            <td align="center" valign"=center" width="%(unButtonsColumnsWidthString)s" >
                [
                <img class="CDTbwStyle_Display CDTbwStyle_Clickable"
                    id="TRAStatusChangeButton_InvalidarResultadosCadena_Icon1" 
                    onmouseup="fTRAEvtHlr_Editor_Button_InvalidarResultadosCadena_OnMouseUp( )"
                    onkeypress="fTRAEvtHlr_Editor_Button_InvalidarResultadosCadena_OnKeyPress( event)"
                    alt="%(CDTbusquedasWeb_TranslationAction_InvalidarResultadosCadena_help)s" 
                    title="%(CDTbusquedasWeb_TranslationAction_InvalidarResultadosCadena_help)s" 
                    src="%(portal_url)s/%(estado-icon-Pendiente)s" />
                *
                <img class="CDTbwStyle_Display CDTbwStyle_Clickable"
                    id="TRAStatusChangeButton_InvalidarResultadosCadena_Icon2" 
                    onmouseup="fTRAEvtHlr_Editor_Button_InvalidarResultadosCadena_OnMouseUp( )"
                    onkeypress="fTRAEvtHlr_Editor_Button_InvalidarResultadosCadena_OnKeyPress( event)"
                    alt="%(CDTbusquedasWeb_TranslationAction_InvalidarResultadosCadena_help)s" 
                    title="%(CDTbusquedasWeb_TranslationAction_InvalidarResultadosCadena_help)s" 
                    src="%(portal_url)s/flag-plone.gif" />
                ]
                <input  
                    onmouseup="fTRAEvtHlr_Editor_Button_InvalidarResultadosCadena_OnMouseUp( )"
                    onkeypress="fTRAEvtHlr_Editor_Button_InvalidarResultadosCadena_OnKeyPress( event)"
                    tabindex=5
                    id="TRAStatusChangeButton_InvalidarResultadosCadena" 
                    class="CDTbwStyle_Display CDTbwStyle_Clickable" 
                    name="TRAStatusChangeButton_InvalidarResultadosCadena" 
                    value="%(action_name)s" 
                    type="button" 
                    style="color: Red; font-size: 9pt; font-style: italic; font-weight: 700" />
            </td>        
            \n""" % { 
            'unButtonsColumnsWidthString': unButtonsColumnsWidthString,
            'action_name':                                                   aTranslationsCache[ 'CDTbusquedasWeb_TranslationAction_InvalidarResultadosCadena_label'], 
            'estado-icon-Pendiente':                                         cIconsDict.get( cEstadoTraduccionPendiente, 'tra_pendiente.gif'),
            'CDTbusquedasWeb_TranslationAction_InvalidarResultadosCadena_help':  aTranslationsCache[ 'CDTbusquedasWeb_TranslationAction_InvalidarResultadosCadena_help'],
            'portal_url':                                                    aPortalURL, 
            'class-Display':                                                 'CDTbwStyle_Display',
        })
            

    
    if pAllowDeactivateStrings:
        anOutput.write( u"""  
            <td align="center" valign"=center" width="%(unButtonsColumnsWidthString)s" >
                <img class="CDTbwStyle_Display CDTbwStyle_Clickable"
                    id="TRAStatusChangeButton_DesactivarCadena_Icon" 
                    onmouseup="fTRAEvtHlr_Editor_Button_DesactivarCadena_OnMouseUp( )"
                    onkeypress="fTRAEvtHlr_Editor_Button_DesactivarCadena_OnKeyPress( event)"
                    alt="%(CDTbusquedasWeb_TranslationAction_DesactivarCadena_help)s" 
                    title="%(CDTbusquedasWeb_TranslationAction_DesactivarCadena_help)s" 
                    src="%(portal_url)s/delete_icon.gif" />
                <input  
                    onmouseup="fTRAEvtHlr_Editor_Button_DesactivarCadena_OnMouseUp( )"
                    onkeypress="fTRAEvtHlr_Editor_Button_DesactivarCadena_OnKeyPress( event)"
                    tabindex=5
                    id="TRAStatusChangeButton_DesactivarCadena" 
                    class="CDTbwStyle_Display CDTbwStyle_Clickable" 
                    name="TRAStatusChangeButton_DesactivarCadena" 
                    value="%(action_name)s" 
                    type="button" 
                    style="color: Red; font-size: 9pt; font-style: italic; font-weight: 700" />
            </td>        
            \n""" % { 
            'unButtonsColumnsWidthString': unButtonsColumnsWidthString,
            'action_name':                                                   aTranslationsCache[ 'CDTbusquedasWeb_TranslationAction_DesactivarCadena_label'], 
            'CDTbusquedasWeb_TranslationAction_DesactivarCadena_help':             aTranslationsCache[ 'CDTbusquedasWeb_TranslationAction_DesactivarCadena_help'],
            'portal_url':                                                    aPortalURL, 
            'class-Display':                                                 'CDTbwStyle_Display',
        })
            
        

    if pAllowActivateStrings:
        anOutput.write( u"""  
            <td align="center" valign"=center" width="%(unButtonsColumnsWidthString)s" >
                <img class="CDTbwStyle_Display CDTbwStyle_Clickable"
                    id="TRAStatusChangeButton_ActivarCadena_Icon" 
                    onmouseup="fTRAEvtHlr_Editor_Button_ActivarCadena_OnMouseUp( )"
                    onkeypress="fTRAEvtHlr_Editor_Button_ActivarCadena_OnKeyPress( event)"
                    alt="%(CDTbusquedasWeb_TranslationAction_ActivarCadena_help)s" 
                    title="%(CDTbusquedasWeb_TranslationAction_ActivarCadena_help)s" 
                    src="%(portal_url)s/add_icon.gif" />
                <input  
                    onmouseup="fTRAEvtHlr_Editor_Button_ActivarCadena_OnMouseUp( )"
                    onkeypress="fTRAEvtHlr_Editor_Button_ActivarCadena_OnKeyPress( event)"
                    tabindex=5
                    id="TRAStatusChangeButton_ActivarCadena" 
                    class="CDTbwStyle_Display CDTbwStyle_Clickable" 
                    name="TRAStatusChangeButton_ActivarCadena" 
                    value="%(action_name)s" 
                    type="button" 
                    style="color: Red; font-size: 9pt; font-style: italic; font-weight: 700" />
            </td>        
            \n""" % { 
            'unButtonsColumnsWidthString': unButtonsColumnsWidthString,
            'action_name':                                                aTranslationsCache[ 'CDTbusquedasWeb_TranslationAction_ActivarCadena_label'], 
            'CDTbusquedasWeb_TranslationAction_ActivarCadena_help':             aTranslationsCache[ 'CDTbusquedasWeb_TranslationAction_ActivarCadena_help'],
            'portal_url':                                                 aPortalURL, 
            'class-Display':                                              'CDTbwStyle_Display',
        })
            
                
    anOutput.write( u"""  
        <td align="right" valign"=center" width="%(unButtonsColumnsWidthString)s" >
            <img class="CDTbwStyle_Display CDTbwStyle_Clickable"
                id="TRAStatusChangeButton_Pendiente_Icon" 
                onmouseup="fTRAEvtHlr_Editor_Button_Pendiente_OnMouseUp( )"
                onkeypress="fTRAEvtHlr_Editor_Button_Pendiente_OnKeyPress( event)"
                alt="%(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Pendiente)s" 
                title="%(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Pendiente)s" 
                src="%(portal_url)s/%(estado-icon-Pendiente)s" />
            <input  
                onmouseup="fTRAEvtHlr_Editor_Button_Pendiente_OnMouseUp( )"
                onkeypress="fTRAEvtHlr_Editor_Button_Pendiente_OnKeyPress( event)"
                tabindex=5
                id="TRAStatusChangeButton_Pendiente" 
                class="CDTbwStyle_Display CDTbwStyle_Clickable" 
                name="TRAStatusChangeButton_Pendiente" 
                value="%(action_name)s" 
                type="button" 
                style="color: Red; font-size: 9pt; font-style: italic; font-weight: 700" />
        </td>        
        \n""" % { 
        'unButtonsColumnsWidthString': unButtonsColumnsWidthString,                  
        'action_name':                 aTranslationsCache[ 'CDTbusquedasWeb_TranslationAction_Borrar'], 
        'estado-icon-Pendiente':       cIconsDict.get( cEstadoTraduccionPendiente, 'tra_pendiente.gif'),
        'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Pendiente':   aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Pendiente'],
        'portal_url':                  aPortalURL, 
        'class-Display':               ((( unEstadoTraduccion in [ cEstadoTraduccionPendiente, cEstadoTraduccionTraducida,]) and ( len( set( [ cEstadoTraduccionPendiente, cEstadoTraduccionTraducida,]).intersection( unosAllowedTargetStates)) > 0)) and 'CDTbwStyle_Display') or 'CDTbwStyle_NoDisplay',
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
    pProfesionales_Nombres                   =None,               
    pTodosNombresModulos                 =None,                  
    pDatosResultados                   =None,               
    pDictsResultadosIdiomasReferencia  =None,                                                 
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
    aCDTbwProfesionalesURL                         =None,  
    fCGIE                                =None,
    fCRs2BRs                            =None,
    fTranslateI18NCGIE                      =None,        
    fAsUnicode                          =None,
    aTranslationsCache                   =None,              
    unRolesCache                         =None,  ):
    """Render as collapsible the matching translations list section of the translations browser.
    
    """

    unCursorPositionString = u''
    
    if pBrowsingInactiveStrings:
        unCursorPositionString = u'%s ' % (
            aTranslationsCache[ 'CDTbusquedasWeb_BrowsingInactive_collapsibleListLabel'],
        )
        
    unCursorPositionString =  u'%s %s %d %s %d %s %d' % ( 
        unCursorPositionString,
        aTranslationsCache[ 'CDTbusquedasWeb_fromToIn_from_label'],
        pBrowseResult.get( 'from_translation_index', 0),
        aTranslationsCache[ 'CDTbusquedasWeb_fromToIn_to_label'],
        pBrowseResult.get( 'to_translation_index', 0),
        aTranslationsCache[ 'CDTbusquedasWeb_fromToIn_in_label'],
        pBrowseResult.get( 'total_translations', 0),
    )        
    
          
 
    _pRenderCollapsible_Lambda(  anOutput,
        u'%s  %s' % ( aTranslationsCache[ 'CDTbusquedasWeb_seccionList_title'], unCursorPositionString),
        u'elid_List_collapsible_dl', 
        lambda : _pRenderList( 
            anOutput                             =anOutput,                                  
            unContextualObject                   =unContextualObject,                                  
            pCodigoIdiomaCursor                  =pCodigoIdiomaCursor,                                  
            pProfesionales_Nombres                   =pProfesionales_Nombres,                                  
            pTodosNombresModulos                 =pTodosNombresModulos,                                 
            pDatosResultados                   =pDatosResultados,                                  
            pDictsResultadosIdiomasReferencia  =pDictsResultadosIdiomasReferencia,                                  
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
            aCDTbwProfesionalesURL                         =aCDTbwProfesionalesURL,                                 
            fCGIE                                =theThruCtxt,                                 
            fCRs2BRs                            =fCRs2BRs,                                 
            fTranslateI18NCGIE                      =fTranslateI18NCGIE,                                 
            fAsUnicode                          =fAsUnicode,                                 
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
    pProfesionales_Nombres                   =None,
    pTodosNombresModulos                 =None,
    pDatosResultados                   =None,
    pDictsResultadosIdiomasReferencia  =None,
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
    aCDTbwProfesionalesURL                         =None,
    fCGIE                                =None,
    fCRs2BRs                            =None,
    fTranslateI18NCGIE                      =None,
    fAsUnicode                          =None,
    aTranslationsCache                   =None,
    unRolesCache                         =None, ):
    """Render the matching translations list section of the translations browser in two columns.
    
    """

    aDictRenderValues = aTranslationsCache.copy()
    aDictRenderValues.update( {
        'portal_url':  aPortalURL, 
        'CDTbusquedasWeb_ColumnaSimboloColapsable_Action_Hide_help':              aTranslationsCache[ 'CDTbusquedasWeb_ColumnaSimboloColapsable_Action_Hide_help'],
        'CDTbusquedasWeb_ColumnaSimboloColapsable_Action_Show_help':              aTranslationsCache[ 'CDTbusquedasWeb_ColumnaSimboloColapsable_Action_Show_help'],
    })
    anOutput.write( u"""  
        <!-- #################################################################
        SECTION: List of matching TRATraduccion
        ################################################################# -->
        
        <table width="100%%" id="matching_TRATraducion_list" cellspacing="2" cellpadding="2" frame="void"  summary="traducciones" >
            <thead>
                <tr>
                    <th width="25%%"  valign="bottom" align="left" class="CDTbwStyle_Display CDTbwStyle_Clickable" 
                        id="cid_ColumnaSimbolos_header" 
                        onclick="pTRAHideSymbolColumn(); return true;" >
                        <font size="1">%(CDTbusquedasWeb_TRATraduccion_attr_simbolo_label)s</font>
                        <br/>
                        <span class="formHelp">
                            <font size="1" style="font-weight=200">
                                %(CDTbusquedasWeb_ColumnaSimboloColapsable_Action_Hide_help)s
                            </font>
                        </span>
                    </th>
                    <th width="1%%" valign="bottom"  colspan="3" align="center" class="CDTbwStyle_Clickable" onclick="pTRAShowSymbolColumn(); return true;" >
                        <font size="1">%(CDTbusquedasWeb_Estado_label)s&ensp;%(CDTbusquedasWeb_idioma_msgid)s</font>
                    </th>
                    <th width="72%%" valign="bottom"  align="left"  class="CDTbwStyle_Clickable" onclick="pTRAShowSymbolColumn(); return true;" >
                        <font size="1">%(CDTbusquedasWeb_TRATraduccion_attr_cadenaTraducida_label)s</font>
                        <br>
                        <span class="CDTbwStyle_NoDisplay formHelp"  id="cid_ColumnaSimbolos_show_help">
                            <font size="1" style="font-weight=200">
                                %(CDTbusquedasWeb_ColumnaSimboloColapsable_Action_Show_help)s
                            </font>
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
        aStatusChangeColumnLabel = (pBatchStatusChanges and aTranslationsCache[ 'CDTbusquedasWeb_BatchNewStatus_title']) or ( aTranslationsCache[ 'CDTbusquedasWeb_newStatus_title'])
        
        anOutput.write( u"""  
            <th colspan="%(colspan)d" valign="bottom"  class="CDTbwStyle_Display" width="1%%"  align="center" >
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
                <th id="TRABatchStatusChange_fillerForSymbolColumn1" class="CDTbwStyle_Display" />
                <th colspan="4" />
                <th colspan="%(colspan)s" valign="bottom"  />
                    <input  
                        onmouseup="fTRAEvtHlr_BatchStatusChange_Apply_Button_OnMouseUp( )"
                        onkeypress="fTRAEvtHlr_BatchStatusChange_Apply_Button_OnKeyPress( event)"
                        id="TRABatchStatusChange_Apply_Button" 
                        class="CDTbwStyle_Display CDTbwStyle_Clickable" 
                        name="TRABatchStatusChange_Apply_Button" 
                        value="%(CDTbusquedasWeb_Batch_ButtonLabel)s" 
                        type="button" 
                        style="color: Red; font-size: 9pt; font-style: italic; font-weight: 700" />
                </th>
            </tr>
            \n""" % {
            'colspan':   len( someEstadosConBotonesEnColumnas),
            # 'CDTbusquedasWeb_BatchNewStatus_Apply_ButtonLabel':   aTranslationsCache[ 'CDTbusquedasWeb_BatchNewStatus_Apply_ButtonLabel'],
            'CDTbusquedasWeb_Batch_ButtonLabel':   aTranslationsCache[ 'CDTbusquedasWeb_Batch_ButtonLabel'],
        })

        
        anOutput.write( u"""  
            <tr>
                <th id="TRABatchStatusChange_fillerForSymbolColumn2" class="CDTbwStyle_Display" />
                <th colspan="4" />
            \n""" 
        )
        for unEstadoConBotonEnColumna in someEstadosConBotonesEnColumnas:
            anOutput.write( u"""  
                <th class="CDTbwStyle_Display" width="1%%"  align="center" >
                    <img
                        id="cid_CDTbwToggleAllBatchStatusChange_%(nombre_estado)s_Icon" 
                        class="CDTbwStyle_Clickable"    
                        onmouseup="pTRAToggleAllBatchStatusChanges( '%(nombre_estado)s'); return true;"
                        alt="%(nombre_estado)s" 
                        title="%(nombre_estado)s" 
                        src="%(portal_url)s/%(estado-icon)s" />
                    <br/>        
                    <input type="checkbox"  class="noborder"  value=""  name="cid_CDTbwToggleAllBatchStatusChange_%(nombre_estado)s" id="cid_CDTbwToggleAllBatchStatusChange_%(nombre_estado)s" 
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
    
    unosDisplayFontSizes_IdiomasReferencia = dict( [ ( unIdiomaReferencia, TRASizesIdioma( unIdiomaReferencia)[ 'display_font_size']) for unIdiomaReferencia in pProfesionales_Nombres] )

    pIndex =0
    
    pSymbolCellCounter = 1
    
    unosIdiomasIdiomasReferenciaSinElPrincipal = [ unIdiomaReferencia for unIdiomaReferencia in pProfesionales_Nombres if not ( unIdiomaReferencia ==  pCodigoIdiomaCursor) ]
     
    
    unColSpanTraduccionIdiomaReferencia   = 1
    unColSpanSimboloEnColumnaResultados = 1 + ( ( pShowStateTransitionColumns and len( someEstadosConBotonesEnColumnas)) or 0)


                        
    unYaRendereadoEditor = False
    
    for unosDatosTraduccion in pDatosResultados:
        
        unRendereadoEditorEnEstaFila = False
        
        
        pTradRow_getSimbolo             = unosDatosTraduccion[ 'getSimbolo']            or ''
        pTradRow_getIdCadena            = unosDatosTraduccion[ 'getIdCadena']           or ''
        pTradRow_getEstadoTraduccion    = unosDatosTraduccion[ 'getEstadoTraduccion']   or cEstadoTraduccionPendiente 
        pTradRow_getCadenaTraducida     = unosDatosTraduccion[ 'getCadenaTraducida']    or ''
        pTradRow_getNombresModulos      = unosDatosTraduccion[ 'getNombresModulos']     or '' 
        pTradRow_getReferenciasFuentes  = unosDatosTraduccion[ 'getReferenciasFuentes']     or '' 
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

        unSimboloCadenaUnicode          = fAsUnicode( pTradRow_getSimbolo)   
        unSimboloCadenaCGIescaped       = fCGIE( unSimboloCadenaUnicode)   
        unSimboloCadenaForWrapLines     = fCGIE( _fWrapeableLinesString( unSimboloCadenaUnicode,           cSimboloCadenaLineWrapLen))

        unaCadenaTraducidaUnicode       = fAsUnicode( pTradRow_getCadenaTraducida)
        unaCadenaTraducidaCGIescaped    = fCGIE( unaCadenaTraducidaUnicode)
        unaCadenaTraducidaForWrapLines  = fCGIE( _fWrapeableLinesString( unaCadenaTraducidaUnicode,   cCadenaTraducidaLineWrapLen))  
        
        
   
                    
        
        unDictRenderValues = { 
            'CDTbusquedasWeb_TRATraduccion_attr_simbolo_label':          fAsUnicode( aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_simbolo_label']),
            'portal_url':                                           aPortalURL, 
            'entrar_en_edicion':                                    unEntrarEnEdicionEventHandler,
            'symbol_cell_counter':                                  pSymbolCellCounter,
            'row_span':                                             unRowSpanAttribute,
            'idCadena':                                             fAsUnicode(  pTradRow_getIdCadena),
            'simbolo-cadena-forWrapLines':                          unSimboloCadenaForWrapLines,
            'simbolo-cadena':                                       unSimboloCadenaCGIescaped,
            'pClassCeldaSimbolo':                                   cClasesFilas [ pSymbolCellCounter %2], 
            'pClassFila':                                           cClasesFilas [ pIndex %2], 
            'estadoTraduccion':                                     pTradRow_getEstadoTraduccion,            
            'estadoTraduccion_label':                               ( pTradRow_getEstadoTraduccion and aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_%s' % pTradRow_getEstadoTraduccion]) or '?',            
            'targetStatusChanges':                                   ' '.join( unosAllowedTargetStates),  
            'cadenaTraducida':                                      unaCadenaTraducidaCGIescaped,
            'cadenaTraducida-forWrapLines':                         unaCadenaTraducidaForWrapLines,
            'font-size':                                            unDisplayFontSize_IdiomaPrincipal,
            'pClassFila':                                           cClasesFilas [ pIndex %2], 
            'codigo-idioma':                                        fAsUnicode( pCodigoIdiomaCursor), 
            'nombre-idioma':                                        fAsUnicode( pLanguagesNamesAndFlags.get( pCodigoIdiomaCursor, {}).get( 'english', '')),        
            'flag-icon':                                            fAsUnicode( pLanguagesNamesAndFlags.get( pCodigoIdiomaCursor, {}).get( 'flag', cFlagIdiomaDesconocida)), 
            'flag-url':                                             fAsUnicode( pLanguagesNamesAndFlags.get( pCodigoIdiomaCursor, {}).get( 'flag_url', '')), 
            'pBGColor':                                             cBGColorsDict.get( pTradRow_getEstadoTraduccion,  cBGColorsDict[ cEstadoTraduccionPendiente]),
            'pFGColor':                                             cFGColorsDict.get( pTradRow_getEstadoTraduccion,  cBGColorsDict[ cEstadoTraduccionPendiente]),
            'estado-icon':                                          cIconsDict.get( pTradRow_getEstadoTraduccion, 'tra_pendiente.gif'), 
            'pTradRow_getNombresModulos':                           fCGIE( fAsUnicode( pTradRow_getNombresModulos)),
            'pTradRow_getReferenciasFuentes':                       fCGIE( fAsUnicode( pTradRow_getReferenciasFuentes)),            
            'pTradRow_getContadorCambios':                          pTradRow_getContadorCambios,
            'pTradRow_getFechaDefinitivo':                          pTradRow_getFechaDefinitivo,
            'pTradRow_getUsuarioCoordinador':                       fCGIE(fAsUnicode(pTradRow_getUsuarioCoordinador)),
            'pTradRow_getFechaRevision':                            pTradRow_getFechaRevision,
            'pTradRow_getUsuarioRevisor':                           fCGIE(fAsUnicode(pTradRow_getUsuarioRevisor)),
            'pTradRow_getFechaTraduccion':                          pTradRow_getFechaTraduccion,
            'pTradRow_getUsuarioTraductor':                         fCGIE(fAsUnicode(pTradRow_getUsuarioTraductor)),
            'pTradRow_getFechaCreacion':                            pTradRow_getFechaCreacion,
            'pTradRow_getUsuarioCreador':                           fCGIE(fAsUnicode(pTradRow_getUsuarioCreador)),
            'colspan_SimboloEnColumnaResultados':                 unColSpanSimboloEnColumnaResultados,
        }
        

        anOutput.write( u"""  
            <tr class="%s CDTbwStyle_NoDisplay"  id="cid_CDTbwInteractionMessageHolder_%d">
                <td colspan="%d" class="CDTbwStyle_Clickable" %s   valign="top">
                    <font size="1">
                        <strong>%s</strong>
                        <span  id="cid_CDTbwInteractionMessage_%d" >
                    </font>
                </td>
            </tr>
            \n""" %  (  
            cClasesFilas [ pIndex %2],
            pSymbolCellCounter,
            pNumTotalColumns, 
            unDictRenderValues.get( 'entrar_en_edicion', ''),
            aTranslationsCache[ 'CDTbusquedasWeb_InteracionStatusMessage'],
            pSymbolCellCounter
        ))
        
        
        
        
        # ACV 20110220
                
        anOutput.write( u"""  
            <tr class="%(pClassFila)s CDTbwStyle_NoDisplay"  id="cid_FilaParaSimboloSobreResultados_%(symbol_cell_counter)d">
                <td class="CDTbwStyle_NoDisplay" id="cid_FilaParaSimboloSobreResultados_%(symbol_cell_counter)d_fillerForSymbol" />
                <td colspan="3" class="CDTbwStyle_NoDisplay" id="cid_FilaParaSimboloSobreResultados_%(symbol_cell_counter)d_fillerForLanguageAndStatusColumns" >
                    <font size="1">
                        <strong>%(CDTbusquedasWeb_TRATraduccion_attr_simbolo_label)s</strong>
                    </font>
                </td>
                <td colspan="%(colspan_SimboloEnColumnaResultados)d" 
                    id="cid_FilaParaSimboloSobreResultados_%(symbol_cell_counter)d_simboloCadena_SobreResultados"                    
                    class="CDTbwStyle_Clickable CDTbwStyle_NoDisplay"  valign="top" %(entrar_en_edicion)s >
                    <font size="1">
                        <span>%(simbolo-cadena-forWrapLines)s</span>
                    </font>
                </td>
            </tr>
            \n""" % unDictRenderValues
        )
         
        
        anOutput.write( u"""  
            <tr class="%(pClassFila)s"  id="cid_FilaPrimeraDeSimbolo_%(symbol_cell_counter)d">
                <td  class="CDTbwStyle_Display CDTbwStyle_Clickable" valign="top" %(row_span)s  
                    %(entrar_en_edicion)s 
                    id="cid_ColumnaSimbolos_%(symbol_cell_counter)d" >
                    <font size="1" class="CDTbwStyle_Display"  id="cid_ColumnaSimbolos_%(symbol_cell_counter)d_SymbolDisplay" >%(simbolo-cadena-forWrapLines)s</font>
                    <span class="CDTbwStyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_simboloCadena" >%(simbolo-cadena)s</span>
                </td>
                <td align="center" valign="top" class="CDTbwStyle_Clickable" onclick="pTRANavegarASimboloCadenaEnFilaNumero( '%(symbol_cell_counter)d')"  >                
                    <img width="14" height="11" alt="Flag_%(nombre-idioma)s" src="%(flag-url)s" title="%(nombre-idioma)s" />
                </td>
                <td align="center" bgcolor="%(pBGColor)s" valign="top" class="CDTbwStyle_Clickable"
                    id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_estado_BGcolor"
                    %(entrar_en_edicion)s >                
                    <font color="%(pFGColor)s" size="1" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_estado_FGcolor">
                        <strong>
                            %(codigo-idioma)s
                        </strong>
                    </font>
                </td>
                <td align="center" valign="top"  class="CDTbwStyle_Clickable"
                    %(entrar_en_edicion)s >                
                    <img id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_estado_icon"
                        alt="Estado_%(estadoTraduccion)s" src="%(portal_url)s/%(estado-icon)s" title="%(estadoTraduccion)s" />
                </td>
                <td align="left" valign="top" bgcolor="white"
                    id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d" >
                    <span %(entrar_en_edicion)s
                        class="CDTbwStyle_Clickable" >
                        <font  size="%(font-size)d" >
                            <span id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_cadenaTraducidaDisplay" >%(cadenaTraducida-forWrapLines)s</span>
                        </font>
                        <span class="CDTbwStyle_NoDisplay" 
                            id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_cadenaTraducida_NewValue">%(cadenaTraducida)s</span>
                        <span class="CDTbwStyle_NoDisplay" 
                            id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_cadenaTraducida">%(cadenaTraducida)s</span>
                    </span>
                    <span class="CDTbwStyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_index">%(symbol_cell_counter)s</span>
                    <span class="CDTbwStyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_simboloCadena">%(simbolo-cadena)s</span>
                    <span class="CDTbwStyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_idCadena">%(idCadena)s</span>
                    <span class="CDTbwStyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_estadoTraduccion">%(estadoTraduccion)s</span>
                    <span class="CDTbwStyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_targetStatusChanges">%(targetStatusChanges)s</span>
                    <span class="CDTbwStyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_usuarioCreador">%(pTradRow_getUsuarioCreador)s</span>
                    <span class="CDTbwStyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_fechaCreacion">%(pTradRow_getFechaCreacion)s</span>
                    <span class="CDTbwStyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_usuarioTraductor">%(pTradRow_getUsuarioTraductor)s</span>
                    <span class="CDTbwStyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_fechaTraduccion">%(pTradRow_getFechaTraduccion)s</span>
                    <span class="CDTbwStyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_usuarioRevisor">%(pTradRow_getUsuarioRevisor)s</span>
                    <span class="CDTbwStyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_fechaRevision">%(pTradRow_getFechaRevision)s</span>
                    <span class="CDTbwStyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_usuarioCoordinador">%(pTradRow_getUsuarioCoordinador)s</span>
                    <span class="CDTbwStyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_fechaDefinitivo">%(pTradRow_getFechaDefinitivo)s</span>
                    <span class="CDTbwStyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_nombresModulos">%(pTradRow_getNombresModulos)s</span>
                    <span class="CDTbwStyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_referenciasFuentes">%(pTradRow_getReferenciasFuentes)s</span>
                    <span class="CDTbwStyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_contadorCambios">%(pTradRow_getContadorCambios)d</span>
                    <span class="CDTbwStyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_interactionStatus"></span>
                    <span class="CDTbwStyle_NoDisplay" id="cid_ColumnaCadenasTraducidas_%(symbol_cell_counter)d_interactionMessage"></span>
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
                aCDTbwProfesionalesURL,
                theThruCtxt,
                fCRs2BRs,
                fTranslateI18NCGIE,
                fAsUnicode,
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
                            class="%(class-Display)s CDTbwStyle_Clickable"    
                            onmouseup="fTRAEvtHlr_Editor_Button_StatusChange_OnMouseUp( '%(symbol_cell_counter)d', 'Traducida')"
                            alt="%(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Traducida)s" 
                            title="%(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Traducida)s" 
                            src="%(portal_url)s/%(estado-icon-Traducida)s" /></td>
                    \n""" % {
                    'class-Display':           (  (( cEstadoTraduccionTraducida in unosAllowedTargetStates) and not ( pTradRow_getEstadoTraduccion in [ cEstadoTraduccionPendiente,  cEstadoTraduccionTraducida, ])) and 'CDTbwStyle_Display') or 'CDTbwStyle_NoDisplay',
                    'symbol_cell_counter':     pSymbolCellCounter,
                    'estado-icon-Traducida':   cIconsDict.get( cEstadoTraduccionTraducida, 'tra_traducida.gif'),
                    'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Traducida':   aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Traducida'],
                    'portal_url':              aPortalURL, 
                })
                    
            if ( cEstadoTraduccionRevisada in pAllTargetStatusChanges):
                anOutput.write( u"""  
                    <td  align="center"  valign="top"  id="cid_ColumnaStatusChangeButton_%(symbol_cell_counter)d_Revisada"                     
                        ><img
                            id="TRAStatusChangeButton_%(symbol_cell_counter)d_Revisada" 
                            class="%(class-Display)s CDTbwStyle_Clickable"
                            onmouseup="fTRAEvtHlr_Editor_Button_StatusChange_OnMouseUp( '%(symbol_cell_counter)d', 'Revisada')"
                            alt="%(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Revisada)s" 
                            title="%(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Revisada)s" 
                            src="%(portal_url)s/%(estado-icon-Revisada)s" /></td>
                    \n""" % {
                    'class-Display':          (  ( cEstadoTraduccionRevisada in unosAllowedTargetStates) and 'CDTbwStyle_Display') or 'CDTbwStyle_NoDisplay',
                    'symbol_cell_counter':    pSymbolCellCounter,
                    'estado-icon-Revisada':   cIconsDict.get( cEstadoTraduccionRevisada, 'tra_revisada.gif'),
                    'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Revisada':   aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Revisada'],
                    'portal_url':             aPortalURL, 
                })
                    
            if ( cEstadoTraduccionDefinitiva in pAllTargetStatusChanges):
                anOutput.write( u"""  
                    <td  align="center"  valign="top" id="cid_ColumnaStatusChangeButton_%(symbol_cell_counter)d_Definitiva""                      
                        ><img 
                                class="%(class-Display)s CDTbwStyle_Clickable"
                                id="TRAStatusChangeButton_%(symbol_cell_counter)d_Definitiva" 
                                onmouseup="fTRAEvtHlr_Editor_Button_StatusChange_OnMouseUp( '%(symbol_cell_counter)d', 'Definitiva')"
                                alt="%(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Definitiva)s" 
                                title="%(CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Definitiva)s" 
                                src="%(portal_url)s/%(estado-icon-Definitiva)s" /></td>
                    \n""" % {
                    'class-Display':           (  ( cEstadoTraduccionDefinitiva in unosAllowedTargetStates) and 'CDTbwStyle_Display') or 'CDTbwStyle_NoDisplay',
                    'symbol_cell_counter':     pSymbolCellCounter,
                    'estado-icon-Definitiva':  cIconsDict.get( cEstadoTraduccionDefinitiva, 'tra_definitiva.gif'),
                    'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Definitiva':   aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_Definitiva'],
                    'portal_url':              aPortalURL, 
                })
       
        anOutput.write( u"""  
            </tr>
            \n"""
        )

                                
       
        anOutput.write( u"""  
            <tr class="%s">
                <td  colspan="%d"  id="cid_CDTbwEditorDetalleHolder_%d" >
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
                aCDTbwProfesionalesURL,
                theThruCtxt,
                fCRs2BRs,
                fTranslateI18NCGIE,
                fAsUnicode,
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
                        aCDTbwProfesionalesURL        =aCDTbwProfesionalesURL,                            
                        fCGIE               =theThruCtxt,                     
                        fCRs2BRs           =fCRs2BRs,                         
                        fTranslateI18NCGIE     =fTranslateI18NCGIE,                               
                        fAsUnicode         =fAsUnicode,                           
                        aTranslationsCache  =aTranslationsCache                                   
                    )
                
                else:
                    anOutput.write( u"""<font size="1">%s</font>
                    """ % aTranslationsCache[ 'CDTbusquedasWeb_NoTranslationsHistory']
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
            
            unasResultadosIdiomaReferencia   = pDictsResultadosIdiomasReferencia.get( unIdiomaReferencia, {})
            if unasResultadosIdiomaReferencia:
                unaTraduccionIdiomaReferencia      = unasResultadosIdiomaReferencia.get( pTradRow_getSimbolo, {})
                if unaTraduccionIdiomaReferencia:
                    unaCadenaTraducidaIdiomaReferencia = unaTraduccionIdiomaReferencia[ 'getCadenaTraducida']
                    unEstadoTraduccion                 = unaTraduccionIdiomaReferencia[ 'getEstadoTraduccion']   or cEstadoTraduccionPendiente 
            
                    
            unaCadenaTraducidaReferenciaUnicode       = fAsUnicode( unaCadenaTraducidaIdiomaReferencia)
            unaCadenaTraducidaReferenciaCGIescaped    = fCGIE( unaCadenaTraducidaReferenciaUnicode)
            unaCadenaTraducidaReferenciaForWrapLines  = fCGIE( _fWrapeableLinesString( unaCadenaTraducidaReferenciaUnicode,   cCadenaTraducidaLineWrapLen))
            
            

                    
                        
            unDictRenderIdiomaReferenciaValues = { 
                'entrar_en_edicion':                        unEntrarEnEdicionEventHandler,
                'symbol_cell_counter':                      pSymbolCellCounter,
                'cadenaTraducidaReferencia':                unaCadenaTraducidaReferenciaCGIescaped,
                'cadenaTraducidaReferencia-forWrapLines':   unaCadenaTraducidaReferenciaForWrapLines,
                'font-size':                                unosDisplayFontSizes_IdiomasReferencia[ unIdiomaReferencia],
                'class-row-idioma':                         cClasesFilas[ pIndexRowIdioma % 2],
                'codigo-idioma':                            fAsUnicode( unIdiomaReferencia),
                'nombre-idioma':                            fAsUnicode( pLanguagesNamesAndFlags.get( unIdiomaReferencia, {}).get( 'english', '')),        
                'portal_url':                               aPortalURL, 
                'flag-icon':                                pLanguagesNamesAndFlags.get( unIdiomaReferencia, {}).get( 'flag', cFlagIdiomaDesconocida), 
                'flag-url':                                 fAsUnicode( pLanguagesNamesAndFlags.get( unIdiomaReferencia, {}).get( 'flag_url', '')), 
                'pBGColor':                                 cBGColorsDict.get( unEstadoTraduccion,  cBGColorsDict[ cEstadoTraduccionPendiente]),
                'pFGColor':                                 cFGColorsDict.get( unEstadoTraduccion,  cBGColorsDict[ cEstadoTraduccionPendiente]),
                'estadoTraduccion':                         unEstadoTraduccion,            
                'estadoTraduccion_label':                   ( unEstadoTraduccion and aTranslationsCache[ 'CDTbusquedasWeb_TRATraduccion_attr_estadoTraduccion_option_%s' % unEstadoTraduccion]) or '?',            
                'estado-icon':                              cIconsDict.get( unEstadoTraduccion, 'tra_pendiente.gif'), 
                'colspan_translation':                      unColSpanTraduccionIdiomaReferencia,
            }
            
                        
            unNavegarAIdiomaYSimboloEventHandler = """
                onclick="pTRANavegarAIdiomaPrincipalYSimboloCadenaEnFilaNumero('%(codigo-idioma)s', '%(symbol_cell_counter)d', '%(estadoTraduccion)s'); return true;"
                \n""" % unDictRenderIdiomaReferenciaValues
            
            unDictRenderIdiomaReferenciaValues[ 'navegar_a_idioma_y_simbolo'] = unNavegarAIdiomaYSimboloEventHandler

            
            anOutput.write( u"""                                                                                                                                                                     
                <tr class="%(class-row-idioma)s" >
                    <td align="center" valign="baseline" class="CDTbwStyle_Clickable" 
                        %(entrar_en_edicion)s >  
                        <img width="14" height="11" alt="Flag_%(codigo-idioma)s" src="%(flag-url)s" title="%(codigo-idioma)s" />
                    </td>
                    <td align="center"  valign="baseline" %(entrar_en_edicion)s class="CDTbwStyle_Clickable"  >                
                        <font  size="1" >
                            <strong>
                                %(codigo-idioma)s
                            </strong>
                        </font>
                    </td>
                    <td align="center" valign="baseline"   class="CDTbwStyle_Clickable"  
                        %(entrar_en_edicion)s  >                
                        <img alt="TranslationStatus_%(estadoTraduccion)s" src="%(portal_url)s/%(estado-icon)s" title="%(estadoTraduccion)s" />
                    </td>
                    <td  align="left" valign="baseline" class="CDTbwStyle_Clickable"  colspan="%(colspan_translation)d"
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
        aCDTbwProfesionalesURL,
        theThruCtxt,
        fCRs2BRs,
        fTranslateI18NCGIE,
        fAsUnicode,
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
    aCDTbwProfesionalesURL,
    theThruCtxt,
    fCRs2BRs,
    fTranslateI18NCGIE,
    fAsUnicode,
    aTranslationsCache) :
    

    anOutput.write( """
        <div id="cid_CDTbwMessages" class="CDTbwStyle_NoDisplay">
            <span id="TRAMessage_Confirmar_NavegarAIdiomaPrincipalYSimbolo">%(CDTbusquedasWeb_Confirmar_NavegarAIdiomaPrincipalYSimbolo_msgid)s</span>
            <span id="TRAMessage_AsyncPhase_RequestQueued">%(CDTbusquedasWeb_AsyncPhase_RequestQueued_msgid)s</span>
            <span id="TRAMessage_AsyncPhase_RequestSent">%(CDTbusquedasWeb_AsyncPhase_RequestSent_msgid)s</span>
            <span id="TRAMessage_AsyncPhase_ResponseReceived">%(CDTbusquedasWeb_AsyncPhase_ResponseReceived_msgid)s</span>
            <span id="TRAMessage_AsyncPhase_ChangeSaved">%(CDTbusquedasWeb_AsyncPhase_ChangeSaved_msgid)s</span>
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
            <span id="cId_ConfirmTranslateMsg"                    class="CDTbwStyle_NoDisplay">%(CDTbusquedasWeb_ConfirmTranslateMsg)s</span>
            <span id="cId_ReallyConfirmTranslateMsg"              class="CDTbwStyle_NoDisplay">%(CDTbusquedasWeb_ReallyConfirmTranslateMsg)s</span>
            <span id="cId_ConfirmStatusChangeMsg"                 class="CDTbwStyle_NoDisplay">%(CDTbusquedasWeb_ConfirmStatusChangeMsg)s</span>
            <span id="cId_ReallyConfirmStatusChangeMsg"           class="CDTbwStyle_NoDisplay">%(CDTbusquedasWeb_ReallyConfirmStatusChangeMsg)s</span>
            <span id="cId_ConfirmDeleteMsg"                       class="CDTbwStyle_NoDisplay">%(CDTbusquedasWeb_ConfirmDeleteMsg)s</span>
            <span id="cId_ReallyConfirmDeleteMsg"                 class="CDTbwStyle_NoDisplay">%(CDTbusquedasWeb_ReallyConfirmDeleteMsg)s</span>
            <span id="cId_ConfirmBatchMsg"                        class="CDTbwStyle_NoDisplay">%(CDTbusquedasWeb_ConfirmBatchMsg)s</span>
            <span id="cId_ReallyConfirmBatchMsg"                  class="CDTbwStyle_NoDisplay">%(CDTbusquedasWeb_ReallyConfirmBatchMsg)s</span>
            <span id="cId_ToAvoidConfirmationDialogsCheckDoNotConfirmOptionMsg" class="CDTbwStyle_NoDisplay">%(CDTbusquedasWeb_ToAvoidConfirmationDialogsCheckDoNotConfirmOptionMsg)s</span>
            <span id="cId_ConfirmInvalidateStringTranslationsMsg" class="CDTbwStyle_NoDisplay">%(CDTbusquedasWeb_ConfirmInvalidateStringTranslationsMsg)s</span>
            <span id="cId_ReallyInvalidateStringTranslationsMsg"  class="CDTbwStyle_NoDisplay">%(CDTbusquedasWeb_ReallyInvalidateStringTranslationsMsg)s</span>
            <span id="cId_ConfirmDeactivateStringMsg"             class="CDTbwStyle_NoDisplay">%(CDTbusquedasWeb_ConfirmDeactivateStringMsg)s</span>
            <span id="cId_ReallyDeactivateStringMsg"              class="CDTbwStyle_NoDisplay">%(CDTbusquedasWeb_ReallyDeactivateStringMsg)s</span>
            <span id="cId_ConfirmActivateStringMsg"               class="CDTbwStyle_NoDisplay">%(CDTbusquedasWeb_ConfirmActivateStringMsg)s</span>
            <span id="cId_ReallyActivateStringMsg"                class="CDTbwStyle_NoDisplay">%(CDTbusquedasWeb_ReallyActivateStringMsg)s</span>
            <span id="cId_ModulesEditor_Open"                     class="CDTbwStyle_NoDisplay">%(CDTbusquedasWeb_ModulesEditor_Open)s</span>
            <span id="cId_ModulesEditor_Close"                    class="CDTbwStyle_NoDisplay">%(CDTbusquedasWeb_ModulesEditor_Close)s</span>
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
    aCDTbwProfesionalesURL               =None,
    fCGIE                      =None,
    fCRs2BRs                  =None,
    fTranslateI18NCGIE            =None,
    fAsUnicode                =None,
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
                aCDTbwProfesionalesURL               =aCDTbwProfesionalesURL,          
                fCGIE                      =fCGIE  ,   
                fCRs2BRs                  =fCRs2BRs,       
                fTranslateI18NCGIE            =fTranslateI18NCGIE,             
                fAsUnicode                =fAsUnicode,         
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
    aCDTbwProfesionalesURL               =None,
    fCGIE                      =None,
    fCRs2BRs                  =None,
    fTranslateI18NCGIE            =None,
    fAsUnicode                =None,
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
        <button type="button" id="cid_CDTbwResetUserInterfaceEventsLog" name="cid_CDTbwResetUserInterfaceEventsLog" onclick="pTRAResetUserInterfaceEventsLog(); return true" >Clear</button>
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
    aCDTbwProfesionalesURL,
    theThruCtxt,
    fCRs2BRs,
    fTranslateI18NCGIE,
    fAsUnicode,
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
                                        <img tabindex=%(tabindex_1)d class="CDTbwStyle_Clickable" onclick="fTRAGoTo_Sync( 'GoToFirst'); return true;" 
                                            src="%(pAbsoluteURL)s/tra_primero.gif" alt="%(CDTbusquedasWeb_traducciones_iraprimero_label)s" title="%(CDTbusquedasWeb_traducciones_iraprimero_label)s" id="icon-primero" />
                                    </td>                                            
                                    <td width="25%%" align="center" valign="center" >
                                        <img tabindex=%(tabindex_2)d  class="CDTbwStyle_Clickable" onclick="fTRAGoTo_Sync( 'GoToPrevious'); return true;" 
                                            src="%(pAbsoluteURL)s/tra_anterior.gif"  alt="%(CDTbusquedasWeb_traducciones_iraanterior_label)s" title="%(CDTbusquedasWeb_traducciones_iraanterior_label)s" id="icon-anterior" />
                                    </td>
                                    <td width="25%%" align="center" valign="center" >
                                        <img tabindex=%(tabindex_3)d class="CDTbwStyle_Clickable" onclick="fTRAGoTo_Sync( 'GoToNext'); return true;" 
                                            src="%(pAbsoluteURL)s/tra_siguiente.gif" alt="%(CDTbusquedasWeb_traducciones_irasiguiente_label)s" title="%(CDTbusquedasWeb_traducciones_irasiguiente_label)s" id="icon-siguiente" />
                                        </button>
                                    </td>
                                    <td width="25%%" align="center" valign="center" >
                                        <img tabindex=%(tabindex_4)d  class="CDTbwStyle_Clickable" onclick="fTRAGoTo_Sync( 'GoToLast'); return true;" 
                                            src="%(pAbsoluteURL)s/tra_ultimo.gif"  alt="%(CDTbusquedasWeb_traducciones_iraultimo_label)s" title="%(CDTbusquedasWeb_traducciones_iraultimo_label)s" id="icon-ultimo" />
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
        'pAbsoluteURL':                                   aCDTbwProfesionalesURL,
        'CDTbusquedasWeb_traducciones_bloquesiguiente_label' : aTranslationsCache[ 'CDTbusquedasWeb_traducciones_bloquesiguiente_label'], 
        'CDTbusquedasWeb_traducciones_iraprimero_label':       aTranslationsCache[ 'CDTbusquedasWeb_traducciones_iraprimero_label'],
        'CDTbusquedasWeb_traducciones_iraanterior_label':      aTranslationsCache[ 'CDTbusquedasWeb_traducciones_iraanterior_label'],
        'CDTbusquedasWeb_traducciones_irasiguiente_label':     aTranslationsCache[ 'CDTbusquedasWeb_traducciones_irasiguiente_label'],
        'CDTbusquedasWeb_traducciones_iraultimo_label':        aTranslationsCache[ 'CDTbusquedasWeb_traducciones_iraultimo_label'],
        'CDTbusquedasWeb_bloquesdea_parameter_label':          fTranslateI18NCGIE( 'CDTbusquedasWeb', 'CDTbusquedasWeb_bloquesdea_parameter_label', 'Block size-'), 
    })
            
    return None


     
            
            
  

        
