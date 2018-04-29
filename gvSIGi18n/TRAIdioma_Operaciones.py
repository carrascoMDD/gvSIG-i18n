# -*- coding: utf-8 -*-
#
# File: TRAIdioma_Operaciones.py
#
# Copyright (c) 2008, 2009, 2010 by Conselleria de Infraestructuras y Transporte de la
# Generalidad Valenciana
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

from AccessControl import ClassSecurityInfo

##code-section module-header #fill in your manual code here


import sys
import traceback
import logging
import transaction



from Products.Archetypes.public import DisplayList

from Products.CMFCore           import permissions




from TRAElemento_Constants                 import *
from TRAElemento_Constants_Activity        import *
from TRAElemento_Constants_Configurations  import *
from TRAElemento_Constants_Dates           import *
from TRAElemento_Constants_Encoding        import *
from TRAElemento_Constants_Import          import *
from TRAElemento_Constants_Languages       import *
from TRAElemento_Constants_Logging         import *
from TRAElemento_Constants_Modules         import *
from TRAElemento_Constants_Profiling       import *
from TRAElemento_Constants_Progress        import *
from TRAElemento_Constants_String          import *
from TRAElemento_Constants_StringRequests  import *
from TRAElemento_Constants_Translate       import *
from TRAElemento_Constants_Translation     import *
from TRAElemento_Constants_TypeNames       import *
from TRAElemento_Constants_Views           import *
from TRAElemento_Constants_Vocabularies    import *
from TRAUtils                              import *

from TRAArquetipo                    import TRAArquetipo 



from TRAImportarExportar_Constants_Encodings  import cTRAEncodingSeparatorSentinelName 

from TRAImportarExportar_Constants import cScannedKeys_String_Symbol, cScannedKeys_Translation_Translation, cScannedKeys_String_Translations


from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_Copy_Translations, cUseCase_LockTRAIdioma, cUseCase_UnlockTRAIdioma
from TRAElemento_Permission_Definitions import cBoundObject



##/code-section module-header


##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema


##code-section after-schema #fill in your manual code here

cModoSeleccionBandera_Plone      = 'Plone'
cModoSeleccionBandera_Especifica = 'Especifica'
cModoSeleccionBandera_Adjunta    = 'Adjunta'

# ACV20090519 removed
# cLogTimeProfileCrearTraduccionesQueFaltanEnIdioma = True


##/code-section after-schema

class TRAIdioma_Operaciones:
    """
    """
    security = ClassSecurityInfo()



    ##code-section class-header #fill in your manual code here
        

    security.declarePrivate( 'pAllSubElements_into')    
    def pAllSubElements_into( self, theCollection, theAdditionalParams=None):
        if theCollection == None:
            return self
        theCollection.append( self)
        
         
        return self
        
    


    security.declarePrivate( 'pForAllElementsDo_recursive')    
    def pForAllElementsDo_recursive( self, theLambda=None, thePloneLambda=None,):
        if not theLambda:
            return self
        
        theLambda( self)
                
        if thePloneLambda:
            self.pForAllElementsPloneDo( thePloneLambda)

        return self
        
    
    
    security.declarePublic( 'fFlagAndURL')    
    def fFlagAndURL( self,):
        """cTRAFlagIdiomaDesconocida
        
        """
        
        unModoSeleccionBandera = self.getModoSeleccionBandera()

        if ( unModoSeleccionBandera == cModoSeleccionBandera_Plone):
            return [ '', '',]
        
        
        unIconoBandera         = self.getIconoBanderaIdioma()

        aFlag = unIconoBandera
        aFlagURL = ''
        
        if ( unModoSeleccionBandera == cModoSeleccionBandera_Adjunta):
            if unIconoBandera:
                aFlagImage = self.getElementoPorID( unIconoBandera)
                
                if not ( aFlagImage == None):
                    aFlagURL = aFlagImage.absolute_url()
            
            if not aFlagURL:
                aFlag = ''
            
        if not aFlag:
            aFlag    = cTRAFlagIdiomaDesconocida
            aFlagURL = ''
        
        return [ aFlag, aFlagURL,]
    
    
                   
    
    security.declarePublic( 'fExtraLinks')    
    def fExtraLinks( self):
        
        unosExtraLinks = TRAArquetipo.fExtraLinks( self)
        if not unosExtraLinks:
            unosExtraLinks = [ ]
        
        unaURL = self.getCatalogo().absolute_url()
        if not unaURL:
            return unosExtraLinks
        
        unCodigoIdiomaEnGvSIG = self.getCodigoIdiomaEnGvSIG()
        if not unCodigoIdiomaEnGvSIG:
            return unosExtraLinks
        
        unExtraLink = self.fNewVoidExtraLink()
        unExtraLink.update( {
            'label'   : self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_Translate', 'Translate',),
            'href'    : '%s/TRATraducir/?theCodigoIdiomaCursor=%s&theMostrarInforme=on&theMostrarLista=on&theIdiomasReferencia=es&theIdiomasReferencia=en ' % ( unaURL, unCodigoIdiomaEnGvSIG,),
            'icon'    : 'tratraduccion.gif',
            'domain'  : 'gvSIGi18n',
            'msgid'   : 'gvSIGi18n_GoTo_Root',
        })
        unosExtraLinks.append( unExtraLink)
                            
        return unosExtraLinks
     
    

        
        
    # #############################################################
    # Prefered Encodings for known languages 
    # A vocabulary for User Interface
    # #############################################################


    security.declareProtected( permissions.View, 'fEncodingsForLanguageVocabulary')
    def fEncodingsForLanguageVocabulary(self,):
        
        unDisplayList = DisplayList()
        
        unCodigoIdioma = self.getCodigoIdiomaEnGvSIG()
        if not unCodigoIdioma:
            return unDisplayList
        
        unosEncodings = self.fEncodingsForLanguage( unCodigoIdioma)

        for unEncoding in unosEncodings:
            unEncodingName = unEncoding[ 0]
            unEncodingTitle = unEncoding[ 1]
            unEncodingAliases = unEncoding[ 2]
            if not ( unEncodingName == cTRAEncodingSeparatorSentinelName):
                unEncodingNamePart = self.fAsUnicode( unEncodingName)
                unTitlePart        = self.fAsUnicode( unEncodingTitle)
                unosAliasesPart = u', '.join( [ self.fAsUnicode( unEncodingAlias) for unEncodingAlias in unEncodingAliases])
                
                unEncodingDisplay  = unEncodingNamePart
                
                if unTitlePart and not ( unTitlePart == unEncodingNamePart):
                    unEncodingDisplay = u'%s %s' % ( unEncodingDisplay, unTitlePart,)
                    
                if unosAliasesPart and not ( unosAliasesPart == unEncodingNamePart) and not ( unosAliasesPart == unTitlePart):
                    unEncodingDisplay = u'%s %s' % ( unEncodingDisplay, unosAliasesPart,)

                unDisplayList.add( unEncodingNamePart, unEncodingDisplay)     
                
        return unDisplayList
    
    
    
    
    
    security.declareProtected( permissions.View, 'fDisplayTitleAsUnicode')
    def fDisplayTitleAsUnicode(self,):
        
        aCodigoIdioma                   = self.getCodigoIdiomaEnGvSIG()
        aCodigoInternacionalDeIdioma    = self.getCodigoInternacionalDeIdioma()
        
        aCodePart = u''
        if ( not aCodigoInternacionalDeIdioma) or ( aCodigoIdioma == aCodigoInternacionalDeIdioma):
            aCodePart =  self.fAsUnicode( aCodigoIdioma)
        else:
            aCodePart =  u'%s %s'  % ( self.fAsUnicode( aCodigoIdioma),  self.fAsUnicode( aCodigoInternacionalDeIdioma),)
            
        aTitle = self.Title()
        aNombreNativoDeIdioma = self.getNombreNativoDeIdioma()
        
        aTitlePart = u''
        if ( not aNombreNativoDeIdioma) or (aTitle  == aNombreNativoDeIdioma):
            aTitlePart = self.fAsUnicode( aTitle )
        else:
            aTitlePart = u'%s %s'  % (   self.fAsUnicode( aTitle ),  self.fAsUnicode( aNombreNativoDeIdioma),)    

        if aTitlePart == aCodePart:
            aTitlePart = ''
            
        aDisplayTitle = u''
        if not aTitlePart or ( aTitlePart == aCodePart):
            aDisplayTitle = aCodePart
        else:
            aDisplayTitle = u'%s %s' % ( aCodePart, aTitlePart,)

        return aDisplayTitle
    
     


  
    security.declareProtected( permissions.View, 'fIdiomasReferenciaVocabulary')
    def fIdiomasReferenciaVocabulary(self,):
        """Return a vocabulary for User Interface with the Languages that can be a reference for this language .
        
        """
        unDisplayList = DisplayList()
        
        unCatalogo = self.getCatalogo()
        if unCatalogo == None:
            return unDisplayList
        
        unDisplayList.add( '', self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_sinIdiomaReferencia', 'No reference language-'))
        
        unosCodigosYDisplayNames = unCatalogo.fTodosIdiomasCodesAndDisplayNames()
        if not unosCodigosYDisplayNames:
            return unDisplayList
        
        unCodigoIdioma = self.getCodigoIdiomaEnGvSIG()
        
        for unCodigoIdiomaReferencia, unDisplayName in unosCodigosYDisplayNames:
            if unCodigoIdiomaReferencia and not ( unCodigoIdiomaReferencia == unCodigoIdioma):
                unDisplayList.add( 
                    unCodigoIdiomaReferencia,
                    unDisplayName,
                )     
                
        return unDisplayList
    
             
    
    security.declareProtected( permissions.View, 'fOtrosIdiomasCodesAndDisplayNames')
    def fOtrosIdiomasCodesAndDisplayNames(self,):
        
        unCodigoIdioma = self.getCodigoIdiomaEnGvSIG()
        if not unCodigoIdioma:
            return []
        
        unCatalogo = self.getCatalogo()
        if unCatalogo == None:
            return []
        
        
        unosCodesAndDisplayNames = unCatalogo.fTodosIdiomasCodesAndDisplayNames()
        if not unosCodesAndDisplayNames:
            return []
        
        otrosCodesAndDisplayNames = [ ]
        for unCode, unDisplayName in unosCodesAndDisplayNames:
            if not ( unCode == unCodigoIdioma):
                otrosCodesAndDisplayNames.append( [ unCode, unDisplayName, ])
                
        return otrosCodesAndDisplayNames
    
     
    

    security.declareProtected( permissions.View, 'fObtenerOtrosIdiomas')
    def fObtenerOtrosIdiomas(self,):
        
        unCodigoIdioma = self.getCodigoIdiomaEnGvSIG()
        if not unCodigoIdioma:
            return []
        
        unCatalogo = self.getCatalogo()
        if unCatalogo == None:
            return []
        
        
        unosIdiomas = unCatalogo.fObtenerTodosIdiomas()
        if not unosIdiomas:
            return []
        
        otrosIdiomas = [ ]
        for unIdioma in unosIdiomas:
            if not ( unIdioma.getCodigoIdiomaEnGvSIG() == unCodigoIdioma):
                otrosIdiomas.append( unIdioma)
                
        return otrosIdiomas
    
       
     
    
    
    
    
    
    

    

            
    
    security.declarePrivate( 'fCreateProgressHandlerFor_CopyTranslations')    
    def fCreateProgressHandlerFor_CopyTranslations( self,
        theAdditionalParams     =None,
        thePermissionsCache     =None,
        theRolesCache           =None,
        theParentExecutionRecord=None):
        """Copy into this Language Translations from the Language with the specified code. If Source States is specified, only copy source translations on those states. If Target States is specified, only overwrite target translations on those states.
        
        """
    
        unExecutionRecord = self.fStartExecution( 'method',  'fCreateProgressHandlerFor_CopyTranslations', None, True, { 'log_what': 'details', 'log_when': True, })

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators import cModificationKind_CreateSubElement, cModificationKind_Create

        try:

            aResult = self.fNewVoidCreateProgressHandlerResult()

            try:
                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)
                
                
                
                
                
                # ##################################################
                """Check permissions to execute use case.
                
                """
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_Copy_Translations, 
                    theElementsBindings     = { cBoundObject: self,}, 
                    theRulesToCollect       = [ 'languages', ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord,
                )
              
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    aResult.update( {
                        'success':    False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_no_permission_ToCopyTranslations_msgid', "User does not have permission to copy Translations from other language.-"),
                    })
                    return aResult  
                               
                
                
                
                # ##################################################
                """Retrieve user request parameters.
                
                """
                aCopyFromLanguageCode         = theAdditionalParams.get( 'theCopyFromLanguageCode',        '')
                if aCopyFromLanguageCode and ( aCopyFromLanguageCode == '---'):
                    aCopyFromLanguageCode = ''
                aSourceStatesToCopyParam      = theAdditionalParams.get( 'theSourceStatesToCopy',          '')
                aTargetStatesToOverwriteParam = theAdditionalParams.get( 'theTargetStatesToOverwrite',     '')


                
                

                # ##################################################
                """Retrieve root translations catalog
                
                """
                unCatalogo = self.getCatalogo()
                
                if unCatalogo == None:
                    aResult.update( {
                        'success':    False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_internal_Missing_TRACatalogo_error_msgid', "Error internal: missing root translations catalog.-"),
                    })
                    return aResult  


                
                
                
                
                # ##################################################
                """Retrieve current language code (the language target of the translations to copy).
                
                """
                
                unCodigoIdioma = self.getCodigoIdiomaEnGvSIG()

                
                
                
                
                # ##################################################
                """Retrieve accesible languages.
                
                """
                
                unosIdiomasAccesibles = unUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'languages', {}).get( 'accepted_final_objects', [])
                if not unosIdiomasAccesibles:
                    aResult.update( {
                        'success':    False,
                        'condition':   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_action_warning_NoAvailableLanguagesToCopyFrom', "You can not copy Translations, there are no available Languages to copy from.-"),
                    })
                    return aResult  

                
                
                
                
                # ##################################################
                """Check validity of user request parameters: source language code must be supplied and different from the code of the current language. Source language must be accessible.
                
                """
                
                if ( not aCopyFromLanguageCode) or ( aCopyFromLanguageCode == '---'):
                    aResult.update( {
                        'success':    False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_action_warning_NoSourceLanguageCodeToCopyFrom', "You can not copy Translationn without supplying the code of a source language to copy translations from.-"),
                    })
                    return aResult  

                
               
                if aCopyFromLanguageCode == unCodigoIdioma:
                    aResult.update( {
                        'success':    False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_action_warning_CanNotCopyTranslationsFromSameLanguage', "You can not copy Translations from the same Language.-"),
                    })
                    return aResult  
                 
                unSourceIdioma = None
                for unIdioma in unosIdiomasAccesibles:
                    if unIdioma.getCodigoIdiomaEnGvSIG() == aCopyFromLanguageCode:
                        unSourceIdioma = unIdioma
                        break
                if unSourceIdioma == None:
                    aResult.update( {
                        'success':    False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_action_warning_SelectedSourceLanguageIsNotAvailable', "You can not copy Translations from the selected source Language because it is not available.-"),
                    })
                    return aResult  
                
                
                
                
                                
                # ##################################################
                """Consider user request parameters to filter by status the source and target translations. 
                If no source translations status specified by the user then shall retrieve translations in all non-pending status..
                Shall always overwrite target translations in the pending status.
                If no conditions requested by the user then shall overwrite translations in the pending and all non-pending status.
                
                """
                someSourceStatesToCopy = [ ]
                if aSourceStatesToCopyParam:
                    for unEstado in [ cEstadoTraduccionTraducida, cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva]:
                        if unEstado in aSourceStatesToCopyParam:
                            someSourceStatesToCopy.append( unEstado)
                            
                if not someSourceStatesToCopy:
                    someSourceStatesToCopy = [ cEstadoTraduccionTraducida, cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva]
                
                
                
                someTargetStatesToOverwrite = [ ]
                if aTargetStatesToOverwriteParam:
                    for unEstado in [ cEstadoTraduccionTraducida, cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva]:
                        if unEstado in aTargetStatesToOverwriteParam:
                            someTargetStatesToOverwrite.append( unEstado)
                            
                if not someTargetStatesToOverwrite:
                    someTargetStatesToOverwrite = cTodosEstados
                else:
                    someTargetStatesToOverwrite = [ cEstadoTraduccionPendiente, ] + someTargetStatesToOverwrite
                
                   
                
                    

                # ##################################################
                """Shall search source translations in the ZCatalog dedicated to the source language.
                
                """
                unCatalogBusquedaTraduccionesInSourceIdioma = unCatalogo.fCatalogBusquedaTraduccionesParaIdioma( unSourceIdioma)
                if ( unCatalogBusquedaTraduccionesInSourceIdioma == None):
                    aResult.update( {
                        'success':    False,
                        'condition': '%s %s' % (  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_internal_Missing_CatalogBusquedaTraducciones_SourceLanguage', "Missing ZCatalog BusquedaTraducciones SourceLanguage.-") , aCopyFromLanguageCode,),
                    })
                    return aResult  
               
                
                
                
                # ##################################################
                """Ignore translations of inactive strings. Filter by status. 
                
                """
                unaBusqueda = {   'getEstadoCadena' :     cEstadoCadenaActiva, }
                
                if someSourceStatesToCopy:
                    unaBusqueda.update( {   'getEstadoTraduccion' :     someSourceStatesToCopy, })
                
                
                    
                    
                # ##################################################
                """Search and retrieve translations found. 
                
                """
                unosResultadosBusqueda      = unCatalogBusquedaTraduccionesInSourceIdioma.searchResults(**unaBusqueda)
                
                unasTraduccionesACopiar = [ ]
                for unResultadoBusqueda in unosResultadosBusqueda:
                    
                    unaTraducccion = unResultadoBusqueda.getObject()
                    
                    if unaTraducccion:
                        
                        unaCadenaTraducida = unaTraducccion.getCadenaTraducida()
                        if unaCadenaTraducida:
                            
                            unasTraduccionesACopiar.append( unaTraducccion)
                        
                           
                            
                # ##################################################
                """Cancel if no translations to copy. 
                
                """
                if not unasTraduccionesACopiar:
                    if someSourceStatesToCopy:
                        aResult.update( {
                            'success':    False,
                            'condition': '%s %s' % (  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_warning_NoTranslationsInSourceLanguageInSpecifiedStates', "There are no Translations in the selected source Language in the specified states.-"), str( someSourceStatesToCopy),),
                        })
                    else:
                        aResult.update( {
                            'success':    False,
                            'condition': self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_warning_NoTranslationsInSourceLanguage', "There are no Translations in the selected source Language.-"),
                        })
                    return aResult  
                
                
                
                
                
                # ##################################################
                """Flush all cached pages in the translations catalog, such that new user requests to view pages reflect the elements about to be created.
                
                """
                unCatalogo.pFlushCachedTemplates_All()           

                
                

                             
                # ##################################################
                """Retrieve collections of TRAImportacion to create a new element into. 
                
                """
                unaColeccionImportaciones = unCatalogo.fObtenerColeccionImportaciones()
                if not unaColeccionImportaciones:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_internal_Missing_imports_collection', "Internal error: missing imports collection-."),
                    })
                    return aResult
                
                     
                
                
                # ##################################################
                """Create a new TRAImportacion element to hold the data for a long-living process. 
                
                """
                unMemberId = self.fGetMemberId()
                unaFechaYHora = self.fDateTimeNowTextual()

                aPloneUtilsTool = self.getPloneUtilsToolForNormalizeString()  
               
                
                
                
                unTitleImportacion = '%s %s->%s by %s on %s' % ( self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_Importacion_prefix', "To Copy Translations from Language to Language"), aCopyFromLanguageCode, unCodigoIdioma, unMemberId, unaFechaYHora)
                aNewIdImportacion = unTitleImportacion.lower().replace( ' ', '-')
                if aPloneUtilsTool:
                    aNewIdImportacion = aPloneUtilsTool.normalizeString( aNewIdImportacion)
 
                anAttrsDictImportacion = { 
                    'title':         unTitleImportacion,
                    'description':   '',
                }
                
                
                unaIdNuevaImportacion = unaColeccionImportaciones.invokeFactory( cNombreTipoTRAImportacion, aNewIdImportacion, **anAttrsDictImportacion)
                if not unaIdNuevaImportacion:
                    aResult.update( {
                        'success':    False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCopyingStrings_TRAImportacion_NotCreated_msgid', "Error creating strings: import not created.-"),
                    })
                    return aResult
                                
                unaNuevaImportacion = unaColeccionImportaciones.getElementoPorID( unaIdNuevaImportacion)
                if not unaNuevaImportacion:
                    aResult.update( {
                        'success':    False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCopyingStrings_TRAImportacion_Created_TRAImportacion_NotFound_msgid', "Could not find import just created-."),
                    })
                    return aResult
     
                
                

                # ##################################################
                """Configure the TRAImportacion element just created with system defaults. 
                
                """
                unaConfiguracionImport = self.getCatalogo().fObtenerConfiguracion( cTRAProgress_ProcessType_Import)
                if not( unaConfiguracionImport == None):
                    
                    unosSegundosParaConfirmarImportacion = unaConfiguracionImport.getSegundosParaConfirmarImportacion()                
                    unaNuevaImportacion.setSegundosParaConfirmarImportacion( unosSegundosParaConfirmarImportacion)
    
                    unNumeroMaximoLineasAExplorar = unaConfiguracionImport.getNumeroMaximoLineasAExplorar()                
                    unaNuevaImportacion.setNumeroMaximoLineasAExplorar( unNumeroMaximoLineasAExplorar)
                
                    
                    
                    
                # ##################################################
                """Configure the TRAImportacion element just created to perform a copy of translations, but not other changes like module names, sources or status. 
                
                """
                
                unaNuevaImportacion.setNombreModuloPorDefecto( '')
                unaNuevaImportacion.setCodigoIdiomaPorDefecto(                         unCodigoIdioma)
                unaNuevaImportacion.setImportarConNombreModuloConfigurado(             False)
                unaNuevaImportacion.setImportarFuentesDesdeComentarios(                False)
                unaNuevaImportacion.setImportarNombreModuloDesdeDominioONombreFichero( False)
                unaNuevaImportacion.setImportarNombresModulosDesdeComentarios(         False)
                unaNuevaImportacion.setImportarStatusDesdeComentarios(                 False)
                
                
                
                
                
                
                # ##################################################
                """Create TRAContenidoIntercambio element to hold the translations to copy translations from source language to target language. 
                
                """
                unTitleContenidoIntercambio = '%s' % ( self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_Importacion_prefix', "To Copy Translations from Language to Language"), )
                aNewIdContenidoIntercambio = unTitleContenidoIntercambio.lower().replace( ' ', '-')
                if aPloneUtilsTool:
                    aNewIdContenidoIntercambio = aPloneUtilsTool.normalizeString( aNewIdContenidoIntercambio)
 
                anAttrsDictContenidoIntercambio = { 
                    'title':         unTitleContenidoIntercambio,
                    'description':   '',
                }
                
                
                
                unaIdNuevoContenidoIntercambio = unaNuevaImportacion.invokeFactory( cNombreTipoTRAContenidoIntercambio, aNewIdContenidoIntercambio, **anAttrsDictContenidoIntercambio)
                if not unaIdNuevoContenidoIntercambio:
                    aResult.update( {
                        'success':    False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_TRAContenidoIntercambio_NotCreated_msgid', "Error: interchange contents not created.-"),
                    })
                    return aResult     
                                
                unNuevoContenidoIntercambio = unaNuevaImportacion.getElementoPorID( unaIdNuevoContenidoIntercambio)
                if not unNuevoContenidoIntercambio:
                    aResult.update( {
                        'success':    False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_Created_TRAContenidoIntercambio_NotFound_msgid', "Could not find interchange contents just created-."),
                    })
                    return aResult     
                
                
                
                
                # ##################################################
                """Initialize TRAContenidoIntercambio parameters from defaults taken from the container TRAImportacion element.
                
                """
                unNuevoContenidoIntercambio.pInitDefaultAttributesFromImport( unNuevoContenidoIntercambio, unaNuevaImportacion)
               
                
                
                
                
                # ##################################################
                """Add to the TRAContenidoIntercambio element just created the data from the retrieved translations to copy. 
                
                """
                
                aScannedData = self.fNewVoidScannedData()
                someScannedStrings = aScannedData[ 'symbols']
                                
                for unaTraduccion in unasTraduccionesACopiar:
                    
                    unSimboloCadena                     = unaTraduccion.getSimbolo()
                    unaCadenaTraducida                  = unaTraduccion.getCadenaTraducida()
                    
                    if unaCadenaTraducida:
                        
                        aScannedString = self.fNewVoidScannedString()
                        aScannedString[ cScannedKeys_String_Symbol] = unSimboloCadena
                        someScannedStrings.append( aScannedString)
                        
                        aScannedTranslation = self.fNewVoidScannedTranslation()
                        aScannedTranslation[ cScannedKeys_Translation_Translation] = unaCadenaTraducida                  
                        aScannedString[ cScannedKeys_String_Translations][ unCodigoIdioma] = aScannedTranslation
                        
                unUploadedContent = self.fNewVoidUploadedContent()
                unUploadedContent[ 'content_data'] = aScannedData
                

                unNuevoContenidoIntercambio.pSetContenido( unUploadedContent)
                
                
                                
                 
                
                
                # ##################################################
                """Create a TRAProgreso element to control the progress of the long living import process, and save the results. 
                
                """
                
                aProgressHandlerCreationResult = unaNuevaImportacion.fCreateProgressHandlerFor_Import( 
                    theAdditionalParams     ={},
                    thePermissionsCache     =unPermissionsCache,
                    theRolesCache           =unRolesCache,
                    theParentExecutionRecord=unExecutionRecord,
                )
                if ( not aProgressHandlerCreationResult) or not aProgressHandlerCreationResult.get( 'success', False):
                    aResult.update( {
                        'success':    False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_TRAProgress_not_created_for_TRAImportacion_msgid', "Error creating Progress element for Import element-."),
                    })
                    return aResult     
                
                
                aProgressElement = aProgressHandlerCreationResult.get( 'progress_element', None)
                if ( aProgressElement == None):
                    aResult = { 
                        'success':   False, 
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorProgressElementNotKnownByImportProcessElement', "Progress element is not known by import process element-"),
                    }
                    return aResult
                
                aProgressHandler = aProgressHandlerCreationResult.get( 'progress_handler', None)
                if not aProgressHandler:
                    aResult = { 
                        'success':   False, 
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorImportProgressHandlerNotFound', "Import Progress Handler has not been found-"),
                    }
                    return aResult

                aProgressHandlerKey = aProgressHandlerCreationResult.get( 'progress_handler_key', None)
                if not aProgressHandlerKey:
                    aResult = { 
                        'success':   False, 
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorImport_NoProgressHandlerKey', "Import has no Progress Handler Key-"),
                    }
                    return aResult

                
                aResult.update( {
                    'success':               True,
                    'progress_element':      aProgressElement,
                    'progress_handler':      aProgressHandler,
                    'progress_handler_key':  aProgressHandlerKey,
                })
                
                
                
                
                
                # ##################################################
                """Flush all cached pages in the translations catalog, such that new user requests to view pages reflect the elements about to be created.
                
                """
                unCatalogo.pFlushCachedTemplates_All()           
                

                
                

                # ##################################################
                """Retrieve information about the new TRAImportacion through traversal with the ModelDDvlPlone framework.
                
                """
                unResultadoNuevaImportacion = self.fModelDDvlPloneTool().fRetrieveTypeConfig( 
                    theTimeProfilingResults     ={ },
                    theElement                  =unaNuevaImportacion, 
                    theParent                   =None,
                    theParentTraversalName      ='',
                    theTypeConfig               =None, 
                    theAllTypeConfigs           =None, 
                    theViewName                 ='', 
                    theRetrievalExtents         =[ 'traversals', ],
                    theWritePermissions         =None,
                    theFeatureFilters           ={ 'attrs': [ 'title',], 'relations': [], 'do_not_recurse_collections': True,}, 
                    theInstanceFilters          =None,
                    theTranslationsCaches       =None,
                    theCheckedPermissionsCache  =None,
                    theAdditionalParams         =None                
                )
                if not unResultadoNuevaImportacion:
                    return aResult     
 
                    
                
                
                
            
                # ##################################################
                """Record changes on the new TRAImportacion and the contained TRAContenidoIntercambio.
                
                """
                aModelDDvlPloneTool_Mutators = self.fModelDDvlPloneTool().fModelDDvlPloneTool_Mutators( self)
                    
                aCreateElementReport = aModelDDvlPloneTool_Mutators.fNewVoidCreateElementReport()
                aCreateElementReport.update( { 'effect': 'created', 'new_object_result': unResultadoNuevaImportacion, })
                
                someFieldReports    = aCreateElementReport[ 'field_reports']
                aFieldReportsByName = aCreateElementReport[ 'field_reports_by_name']
                
                aReportForField = { 'attribute_name': 'id',    'effect': 'changed', 'new_value': unaIdNuevoContenidoIntercambio, 'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                
                aReportForField = { 'attribute_name': 'title', 'effect': 'changed', 'new_value': unTitleContenidoIntercambio,    'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                
                                   
                aModelDDvlPloneTool_Mutators.pSetAudit_Creation( self, cModificationKind_CreateSubElement, aCreateElementReport, theUseCounter=True)       
                aModelDDvlPloneTool_Mutators.pSetAudit_Creation( unaNuevaImportacion,       cModificationKind_Create,  aCreateElementReport)       
                
                
                aContenidoIntercambioTraversalResult = None
                for aTraversalResult in unResultadoNuevaImportacion.get( 'traversals', []):
                    if aTraversalResult.get( 'traversal_name', '') == cNombreTraversal_Importacion_ContenidosIntercambio:
                        aContenidoIntercambioTraversalResult = aTraversalResult
                        break
                if aContenidoIntercambioTraversalResult: 
                    someContenidoIntercambioResults = aContenidoIntercambioTraversalResult.get( 'elements', [])
                    
                    for aContenidoIntercambioResult in someContenidoIntercambioResults:
                        
                        unNuevoContenidoIntercambioElement = aContenidoIntercambioResult.get( 'object', None)
                        if not ( unNuevoContenidoIntercambioElement == None):
                                                    
                            aCreateElementReport = aModelDDvlPloneTool_Mutators.fNewVoidCreateElementReport()
                            aCreateElementReport.update( { 'effect': 'created', 'new_object_result': aContenidoIntercambioResult, })
                            
                            someFieldReports    = aCreateElementReport[ 'field_reports']
                            aFieldReportsByName = aCreateElementReport[ 'field_reports_by_name']
                            
                            aReportForField = { 'attribute_name': 'id',     'effect': 'changed', 'new_value': aContenidoIntercambioResult.get( 'id', ''),     'previous_value': '',}
                            someFieldReports.append( aReportForField)            
                            aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                            
                            aReportForField = { 'attribute_name': 'title',  'effect': 'changed', 'new_value': aContenidoIntercambioResult.get( 'title', ''),  'previous_value': '',}
                            someFieldReports.append( aReportForField)            
                            
                            aModelDDvlPloneTool_Mutators.pSetAudit_Creation( unaNuevaImportacion,                cModificationKind_CreateSubElement, aCreateElementReport, theUseCounter=True)       
                            aModelDDvlPloneTool_Mutators.pSetAudit_Creation( unNuevoContenidoIntercambioElement, cModificationKind_Create,           aCreateElementReport)       
                
                            
                # ##################################################
                """Flush all cached pages in the translations catalog, such that new user requests to view pages reflect the elements just created.
                
                """
                unCatalogo.pFlushCachedTemplates_All()           
                            
                
                return aResult
                
 
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fCreateProgressHandlerFor_CopyTranslations\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   
                                         
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                aResult = { 
                    'success':    False, 
                    'condition':  '%s\n%s' % (   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_Exception_msgid', "Exception.-"), unInformeExcepcion, ),
                }
                aResult = { 
                    'success':    False, 
                    'condition':  '%s\n%s' % (   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_Exception_msgid', "Exception.-"), unInformeExcepcion, ),
                }
                return aResult
              
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

        
            
            
     
            
            
            

    
    security.declareProtected( permissions.ModifyPortalContent, 'fBloquearIdioma')
    def fBloquearIdioma( self , 
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fBloquearIdioma', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators import cModificationKind_ChangeValues, cModificationKind_CreateSubElement, cModificationKind_Create
        
        try:
            
            try:
                
                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)
            
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_LockTRAIdioma, 
                    theElementsBindings     = { cBoundObject: self,},
                    theRulesToCollect       = [ ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord
                )
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    return False
                        
                                    
                unPermiteModificar = self.getPermiteModificar()
                
                if unPermiteModificar:
                    self.setPermiteModificar( False)
                    
                    unCatalogo = self.getCatalogo()
                    if not ( unCatalogo == None):
                        unCatalogo.pFlushCachedTemplates_All()
                    
                    
                    aModelDDvlPloneTool_Mutators = self.fModelDDvlPloneTool().fModelDDvlPloneTool_Mutators( self)
                   
                    aReport = aModelDDvlPloneTool_Mutators.fNewVoidChangeValuesReport()
                    someFieldReports    = aReport.get( 'field_reports')
                    aFieldReportsByName = aReport.get( 'field_reports_by_name')       

                    aReportForField = { 'attribute_name': 'permiteModificar', 'effect': 'changed', 'new_value': False, 'previous_value': True,}                                                                                                                        
                    
                    someFieldReports.append( aReportForField)
                    aFieldReportsByName[ 'permiteModificar'] = aReportForField
                    
                    aModelDDvlPloneTool_Mutators.pSetAudit_Modification( self, cModificationKind_ChangeValues, aReport)       
                    
                    transaction.commit()
                    logging.getLogger( 'gvSIGi18n').info( "COMMIT TRAIdioma::fBloquearIdioma %s" % '/'.join( self.getPhysicalPath()))
                    
                return True
            
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during TRAIdioma::fBloquearIdioma %s \n'  % '/'.join( self.getPhysicalPath())
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   

                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return False
        
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

            
 
            
            
            
                
    security.declareProtected( permissions.View, 'fExportarIdiomaParaGvSIG')    
    def fExportarIdiomaParaGvSIG( self, 
        theParametersInput               = None,
        thePermissionsCache              = None,
        theRolesCache                    = None,
        theParentExecutionRecord         = None):
        """Export Translations into this languages, in any Module, with the parameters prefered for gvSIG. 
        
        """
        
        
        unCatalogo = self.getCatalogo()
        if unCatalogo == None:
            return None
        
        return unCatalogo.fExportarIdiomaParaGvSIG( 
            self,
            theParametersInput,
            thePermissionsCache,
            theRolesCache,
            theParentExecutionRecord,
        )
    
    
    
   

    
    security.declareProtected( permissions.ModifyPortalContent, 'fDesbloquearIdioma')
    def fDesbloquearIdioma( self , 
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fDesbloquearIdioma', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators import cModificationKind_ChangeValues, cModificationKind_CreateSubElement, cModificationKind_Create

        try:
            
            try:
                
                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)
            
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_UnlockTRAIdioma, 
                    theElementsBindings     = { cBoundObject: self,},
                    theRulesToCollect       = [ ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord
                )
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    return False
                        
                                    
                unPermiteModificar = self.getPermiteModificar()
                
                if not unPermiteModificar:
                    self.setPermiteModificar( True)

                    
                    unCatalogo = self.getCatalogo()
                    if not ( unCatalogo == None):
                        unCatalogo.pFlushCachedTemplates_All()
                    
                    
                    
                    aModelDDvlPloneTool_Mutators = self.fModelDDvlPloneTool().fModelDDvlPloneTool_Mutators( self)
                   
                    aReport = aModelDDvlPloneTool_Mutators.fNewVoidChangeValuesReport()
                    someFieldReports    = aReport.get( 'field_reports')
                    aFieldReportsByName = aReport.get( 'field_reports_by_name')       

                    aReportForField = { 'attribute_name': 'permiteModificar', 'effect': 'changed', 'new_value': True, 'previous_value': False,}                                                                                                                        
                    
                    someFieldReports.append( aReportForField)
                    aFieldReportsByName[ 'permiteModificar'] = aReportForField
                    
                    aModelDDvlPloneTool_Mutators.pSetAudit_Modification( self, cModificationKind_ChangeValues, aReport)       
                    
                    transaction.commit()
                    logging.getLogger( 'gvSIGi18n').info( "COMMIT TRAIdioma::fDesbloquearIdioma %s" % '/'.join( self.getPhysicalPath()))
                    
                return True
            
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during TRAIdioma::fDesbloquearIdioma %s \n'  % '/'.join( self.getPhysicalPath())
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   

                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return False
        
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

                            
    
    
    
# ####################################
#  Complete initialization after creation
#
        
     
    
    security.declarePrivate('pHandle_manage_afterAdd')
    def pHandle_manage_afterAdd(self, theItem, theContainer):   
        
        TRAArquetipo.manage_afterAdd(  self, theItem, theContainer)
        
        if self.getCodigoIdiomaEnGvSIG():
            unInforme = self.getCatalogo().fLazyCrearCatalogosEIndicesParaIdioma( self)
        
        # Creation of TRATRaduccion for the TRAIdioma 
        # will be commanded by the caller, not here
        # as we don want that to happen at every instantiation.
        # I.e. Import process
        
        return self
    
         
    
  
            

    
    ##/code-section class-header

    # Methods
# end of class TRAIdioma_Operaciones

##code-section module-footer #fill in your manual code here
##/code-section module-footer





        


    


    

    
    
    
    
    
    
    
    
    
    





    
    