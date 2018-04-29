# -*- coding: utf-8 -*-
#
# File: TRAColeccionIdiomas_Operaciones.py
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
#

__author__ = """Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana <gvSIGi18n@gvSIG.org>, 
Model Driven Development sl <gvSIGi18n@ModelDD.org>,
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.gvSIGi18n.config import *

##code-section module-header #fill in your manual code here


import sys
import traceback
import logging

from Products.CMFCore        import permissions
from Products.CMFCore.utils  import getToolByName





from TRAElemento_Constants                 import *
from TRAElemento_Constants_Activity        import *
from TRAElemento_Constants_Configurations  import *
from TRAElemento_Constants_Contributions   import *
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

from TRAImportarExportar_Constants import cScannedKeys_String_Symbol, cScannedKeys_Translation_Translation, cScannedKeys_String_Translations

from TRAElemento_Permission_Definitions import cBoundObject
from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_CreateTRAIdioma, cUseCase_DeleteTRAIdioma

from TRACatalogo_Inicializacion_Constants import cTRACatalogsDetailsParaIdioma

from TRAImportarExportar_Constants import cTRAReferenceLanguageCodesForLanguages, cTRADefaultReferenceLanguageCode

##/code-section module-header



##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAColeccionIdiomas_Operaciones:
    """
    """
    security = ClassSecurityInfo()


    ##code-section class-header #fill in your manual code here
    

    # ###################################################################
    #   Parent and children access
    # ###############################                  
    



    security.declarePrivate( 'pAllSubElements_into')    
    def pAllSubElements_into( self, theCollection, theAdditionalParams=None):
        if theCollection == None:
            return self
        theCollection.append( self)
        
        unosElementos = self.fObtenerTodosIdiomas()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pAllSubElements_into( theCollection, theAdditionalParams=theAdditionalParams)
        
        return self
        

        


    security.declarePrivate( 'pForAllElementsDo_recursive')    
    def pForAllElementsDo_recursive( self, theLambda=None, thePloneLambda=None,):
        if not theLambda:
            return self
        
        theLambda( self)
        
        unosElementos = self.fObtenerTodosIdiomas()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda, thePloneLambda)
                
        if thePloneLambda:
            self.pForAllElementsPloneDo( thePloneLambda)
        
        return self
        
                                
                
    security.declareProtected( permissions.View, 'fObtenerTodosIdiomas')
    def fObtenerTodosIdiomas( self, ):
        """Retrieve all contained elements of type TRAIdioma.
        
        """
        unosElementos = self.fObjectValues( cNombreTipoTRAIdioma) 
        return unosElementos
         
          
    
    

    

            
    
    security.declarePrivate( 'fCreateProgressHandlerFor_CreateLanguage')    
    def fCreateProgressHandlerFor_CreateLanguage( self,
        theAdditionalParams     =None,
        thePermissionsCache     =None,
        theRolesCache           =None,
        theParentExecutionRecord=None):
        """Create a new instance of TRAIdioma through an import process. Create an instance of TRAImportacion with a TRAContenidoIntercambio that will create the language when the import is executed.
        
        """
    
        unExecutionRecord = self.fStartExecution( 'method',  'fCreateProgressHandlerFor_CreateLanguage', None, True, { 'log_what': 'details', 'log_when': True, })
        

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators import cModificationKind_CreateSubElement, cModificationKind_Create

        try:
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
            
            aResult = self.fNewVoidCreateProgressHandlerResult()
            
            
            try:
                
                
                # ##################################################
                """Check permissions to execute use case.
                
                """
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_CreateTRAIdioma, 
                    theElementsBindings     = { cBoundObject: self,}, 
                    theRulesToCollect       = [ 'languages', ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord,
                )
              
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_no_permission_ToCreateLanguage_msgid', "You do not have permission to Create Language-."),
                    })
                    return aResult
                            
                
                 
                # ##################################################
                """Retrieve user request parameters.
                
                """
                aNewCodigoIdiomaEnGvSIG       = theAdditionalParams.get( 'theCodigoIdiomaEnGvSIG',          '')
                aCodigoInternacionalDeIdioma  = theAdditionalParams.get( 'theCodigoInternacionalDeIdioma',  '')
                aNewEnglishName               = theAdditionalParams.get( 'theEnglishName',                  '')
                aNewNombreNativoDeIdioma      = theAdditionalParams.get( 'theNombreNativoDeIdioma',         '')
                
                aCopyFromLanguageCode         = theAdditionalParams.get( 'theCopyFromLanguageCode',        '')
                if aCopyFromLanguageCode and ( aCopyFromLanguageCode == '---'):
                    aCopyFromLanguageCode = ''
                aSourceStatesToCopyParam      = theAdditionalParams.get( 'theSourceStatesToCopy',          '')
        

                
                

                # ##################################################
                """Retrieve root translations catalog
                
                """
                unCatalogo = self.getCatalogo()
                
                if unCatalogo == None:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_internal_Missing_RootCatalog', "Internal error: missing root translations catalog-."),
                    })
                    return aResult
                

               
                
                
                
                # ##################################################
                """Retrieve collections of TRAImportacion to create a new element into. 
                
                """
                unaColeccionImportaciones = unCatalogo.fObtenerColeccionImportaciones()
                if ( unaColeccionImportaciones == None):
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_internal_Missing_imports_collection', "Internal error: missing imports collection-."),
                    })
                    return aResult
                

                                
                
                # ##################################################
                """Retrieve languages accesible to the user, and  all languages.
                
                """
                
                unosIdiomasAccesibles = unUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'languages', {}).get( 'accepted_final_objects', [])
                          
                todosIdiomas = unCatalogo.fObtenerTodosIdiomas()
                
                
                
                # ##################################################
                """Check validity of user request parameters: new language code must be supplied. A language with such code must not already exist.
                
                """
                
                if not aNewCodigoIdiomaEnGvSIG:
                    aResult.update( {
                        'success':    False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Idioma_missingParameter_CodigoIdiomaEnGvSIG_warning_msgid', "The code in gvSIG for the new language is missing. Can not create a new language without a language code.-"),
                    })
                    return aResult 
                
                
                
                unIdiomaPorCodigo = None
                for unIdioma in todosIdiomas:
                    if unIdioma.getCodigoIdiomaEnGvSIG() == aNewCodigoIdiomaEnGvSIG:
                        unIdiomaPorCodigo = unIdioma
                        break                
                if not ( unIdiomaPorCodigo == None):
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Idioma_LanguageCodeAlreadyExists_warning_msgid', "A language with same code already exists in the translations catalog.-"),
                    })
                    return aResult
                                
                
                
                
                
                # ##################################################
                """If requested to copy translations from an existing language.
                The code of the source language must not be the same as the code for the new language.
                Consider user request parameters to filter by status the source and target translations.  If no source translations status specified by the user then shall retrieve translations in all non-pending status..
                
                """
                
                unSourceIdioma         = None
                unasTraduccionesACopiar = [ ]
                
                if aCopyFromLanguageCode:
                    
                    if aCopyFromLanguageCode == aNewCodigoIdiomaEnGvSIG:
                        aResult.update( {
                            'success':    False,
                            'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_action_warning_CanNotCopyTranslationsFromSameLanguage', "You can not copy Translations from the same Language.-"),
                        })
                        return aResult  

                
                    for unIdioma in unosIdiomasAccesibles:
                        if unIdioma.getCodigoIdiomaEnGvSIG() == aCopyFromLanguageCode:
                            unSourceIdioma = unIdioma
                            break
                    if unSourceIdioma == None:
                        aResult.update( {
                            'success':     False,
                            'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_action_warning_SelectedSourceLanguageIsNotAvailable', "You can not copy Translations from the selected source Language because it is not available.-"),
                        })
                        return aResult
 
                    
                    
                
                    # ##################################################
                    """Consider user request parameters to filter by status the source and target translations. 
                    If no conditions requested by the user then shall retrieve translations in all non-pending status.
                    
                    """
                    someSourceStatesToCopy = [ ]
                    if aSourceStatesToCopyParam:
                        for unEstado in [ cEstadoTraduccionTraducida, cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva]:
                            if unEstado in aSourceStatesToCopyParam:
                                someSourceStatesToCopy.append( unEstado)
                                
                    if not someSourceStatesToCopy:
                        someSourceStatesToCopy = [ cEstadoTraduccionTraducida, cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva]
                
                                
                    
                    
                    
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
                    
                    for unResultadoBusqueda in unosResultadosBusqueda:
                        
                        unaTraducccion = unResultadoBusqueda.getObject()
                        
                        if unaTraducccion:
                            
                            unaCadenaTraducida = unaTraducccion.getCadenaTraducida()
                            if unaCadenaTraducida:
                                
                                unasTraduccionesACopiar.append( unaTraducccion)
                            
                                
                                
                                
                                
                                
                # ##################################################
                """Retrieve names for the new language, if it is well known to the system.
                
                """
                
                aCodigoInternacionalDeIdioma = aNewCodigoIdiomaEnGvSIG
                unNombreInglesDeIdioma       = aNewCodigoIdiomaEnGvSIG
                unNombreNativoDeIdioma       = aNewCodigoIdiomaEnGvSIG
                
                someNonExistingKnownIdiomasCodesAndNames = unCatalogo.fNonExistingKnownIdiomasCodesAndNames()  
                for unCodigoIdioma, unNombreInglesDeIdioma, unNombreNativoDeIdioma in someNonExistingKnownIdiomasCodesAndNames:
                    if unCodigoIdioma == aNewCodigoIdiomaEnGvSIG:
                        aCodigoInternacionalDeIdioma    = unCodigoIdioma
                        aNewEnglishName                 = unNombreInglesDeIdioma
                        aNewNombreNativoDeIdioma        = unNombreNativoDeIdioma
                        break
                
               
                    
                
                # ##################################################
                """Flush all cached pages in the translations catalog, such that new user requests to view pages reflect the elements about to be created.
                
                """
                unCatalogo.pFlushCachedTemplates_All()           

                
                    
                
 
                
                # ##################################################
                """Create a new TRAImportacion element to hold the data for a long-living process. 
                
                """
                unMemberId = self.fGetMemberId()
                unaFechaYHora = self.fDateTimeNowTextual()

                aPloneUtilsTool = self.getPloneUtilsToolForNormalizeString()  
               
                
                
                
                unTitleImportacion = '%s %s %s %s %s' % ( self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_crearIdioma_Importacion_prefix', "To Create Language"), aNewCodigoIdiomaEnGvSIG, aNewEnglishName, unMemberId, unaFechaYHora, )
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
                """Configure the TRAImportacion element just created to perform a copy of translations, but not other changes like module names, sources or status. 
                
                """
                
                unaConfiguracionImport = self.getCatalogo().fObtenerConfiguracion( cTRAProgress_ProcessType_Import)
                if not( unaConfiguracionImport == None):
                    
                    unosSegundosParaConfirmarImportacion = unaConfiguracionImport.getSegundosParaConfirmarImportacion()                
                    unaNuevaImportacion.setSegundosParaConfirmarImportacion( unosSegundosParaConfirmarImportacion)
    
                    unNumeroMaximoLineasAExplorar = unaConfiguracionImport.getNumeroMaximoLineasAExplorar()                
                    unaNuevaImportacion.setNumeroMaximoLineasAExplorar( unNumeroMaximoLineasAExplorar)
                
                
                    

                # ##################################################
                """Configure the TRAImportacion element just created to perform a creation of the new language. 
                
                """
                
                unaNuevaImportacion.setNombreModuloPorDefecto(                         '')
                unaNuevaImportacion.setCodigoIdiomaPorDefecto(                         aNewCodigoIdiomaEnGvSIG)
                unaNuevaImportacion.setImportarConNombreModuloConfigurado(             False)
                unaNuevaImportacion.setImportarFuentesDesdeComentarios(                False)
                unaNuevaImportacion.setImportarNombreModuloDesdeDominioONombreFichero( False)
                unaNuevaImportacion.setImportarNombresModulosDesdeComentarios(         False)
                unaNuevaImportacion.setImportarContribucionesDesdeComentarios(         False)                
                unaNuevaImportacion.setImportarStatusDesdeComentarios(                 False)
                
                     
                
                
                
                
                # ##################################################
                """Create TRAContenidoIntercambio element to hold the new language information within the TRAImportacion just created. 
                
                """
                unTitleContenidoIntercambio = '%s %s by %s on %s' % ( self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_crearIdioma_Importacion_prefix', "To Create Language"), aNewCodigoIdiomaEnGvSIG, unMemberId, unaFechaYHora,)
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
                """Add to the TRAContenidoIntercambio element just created the data about the new language to create. 
                
                """
                
                aScannedData = self.fNewVoidScannedData()
                
                aScannedData.update( {
                    'languages':         [ aNewCodigoIdiomaEnGvSIG, ], 
                    'languages_details': { 
                        aNewCodigoIdiomaEnGvSIG: {
                            'codigo_internacional_idioma': aCodigoInternacionalDeIdioma, 
                            'english_name':                aNewEnglishName, 
                            'nombre_nativo_de_idioma':     aNewNombreNativoDeIdioma,
                        },
                    },
                })
 
                
               
                
                
                
                # ##################################################
                """If requested to copy to the new language the translations from an existing language, Add to the TRAContenidoIntercambio element just created the data from the retrieved translations to copy. 
                
                """
                if aCopyFromLanguageCode:
                    
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
                            aScannedString[ cScannedKeys_String_Translations][ theNewLanguageCode] = aScannedTranslation
              
                            

                            
                            
                # ##################################################
                """Store import data in the translations interchange element. 
                
                """
                            
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
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorProgressElementNotKnownByImportProcessElement', "Progress element is not known by progress handler-"),
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
                    'condition':             '',
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
                    theFeatureFilters           ={ 'attrs': [ 'title',], 'aggregations': [ cNombreTraversal_Importacion_ContenidosIntercambio,], 'relations': [], 'do_not_recurse_collections': True,}, 
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
                
                                   
                aModelDDvlPloneTool_Mutators.pSetAudit_Creation( unaColeccionImportaciones, cModificationKind_CreateSubElement, aCreateElementReport, theUseCounter=True)       
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
                
                unInformeExcepcion = 'Exception during fCreateProgressHandlerFor_CreateLanguage\n' 
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
                return aResult
              
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

        
            
            
            
            
            
            
            
            
            
            

    

                    
                            
            
        

    security.declarePrivate( 'fCrearIdioma')
    def fCrearIdioma( self, 
        theUseCaseQueryResult, 
        theCodigoIdiomaEnGvSIG, 
        theCodigoInternacionalDeIdioma='', 
        theTitle='', 
        theNombreInglesIdioma='', 
        theNombreNativoIdioma='',
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None):
        """TRAIdioma private factory method that does not check security constraints, that must have already been checked by caller.
        
        """
        unExecutionRecord = self.fStartExecution( 'method',  'fCrearIdioma', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }, 'codigo_idioma: %s' % ( theCodigoIdiomaEnGvSIG or 'unknown')) 

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators import cModificationKind_CreateSubElement, cModificationKind_Create, cModificationKind_ChangeValues

        try:
        
            if not theUseCaseQueryResult or not theUseCaseQueryResult.get( 'success', False):
                return None    
            
            if not theCodigoIdiomaEnGvSIG:
                return None    
    
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
            
            unCatalogo = self.getCatalogo()
            if unCatalogo == None:
                return None
            
            unaIdIdioma         = unCatalogo.fIdiomaIdDesdeCodigo( theCodigoIdiomaEnGvSIG)
            unIdiomaEncontrado  = unCatalogo.fGetIdiomaPorId( unaIdIdioma)
    
            if unIdiomaEncontrado:
                return unIdiomaEncontrado
                            

            unosCodigosIdioma = [ unIdioma.getCodigoIdiomaEnGvSIG() for unIdioma in self.fObjectValues( cNombreTipoTRAIdioma)]
            if theCodigoIdiomaEnGvSIG in unosCodigosIdioma:
                return None
    
            unTitle                       = theTitle              
            unNombreInglesIdioma          = theNombreInglesIdioma 
            unNombreNativoIdioma          = theNombreNativoIdioma
            unCodigoInternacionalDeIdioma = theCodigoInternacionalDeIdioma
            
            if not unTitle or not unNombreInglesIdioma or not unNombreNativoIdioma:
                unosIntlLanguagesNamesAndFlagsPorCodigo = unCatalogo.fLanguagesNamesAndFlagsPorCodigo()
                
                unosIntlDatosIdioma     = unosIntlLanguagesNamesAndFlagsPorCodigo.get( theCodigoIdiomaEnGvSIG, {})
                if unosIntlDatosIdioma:
                    unNombreInglesIdioma    = unosIntlDatosIdioma.get( 'english', '')
                    unNombreNativoIdioma    = unosIntlDatosIdioma.get( 'native', '')
            
    
            if not unCodigoInternacionalDeIdioma:
                unCodigoInternacionalDeIdioma = theCodigoIdiomaEnGvSIG
                
            unNombreInglesIdioma = unNombreInglesIdioma or theCodigoIdiomaEnGvSIG
            unNombreNativoIdioma = unNombreNativoIdioma or unNombreInglesIdioma
            unTitle              = unTitle              or unNombreInglesIdioma
                    
            unCodigoIdiomaReferencia = cTRAReferenceLanguageCodesForLanguages.get( theCodigoIdiomaEnGvSIG, cTRADefaultReferenceLanguageCode)
            
            aNewIdiomaAttrsDict = { 
                'codigoIdiomaEnGvSIG':          theCodigoIdiomaEnGvSIG,
                'codigoInternacionalDeIdioma':  theCodigoInternacionalDeIdioma,
                'codigoIdiomaReferencia':       unCodigoIdiomaReferencia,
                'title':                        unTitle,
                'nombreNativoDeIdioma':         unNombreNativoIdioma,
            }
            
            unaIdNuevoIdioma = self.invokeFactory( cNombreTipoTRAIdioma,  unaIdIdioma, **aNewIdiomaAttrsDict)
            if not unaIdNuevoIdioma:
                return None
            unNuevoIdioma = self.getElementoPorID( unaIdNuevoIdioma)
            if not unNuevoIdioma:
                return None
            
            unNuevoIdioma.manage_fixupOwnershipAfterAdd()
           
            unNuevoIdioma.pSetPermissions()
            
            
            
            unCatalogo.fVerifyOrInitializeCatalogsEIndicesParaIdioma( 
                theEspecificacionesCatalogs =cTRACatalogsDetailsParaIdioma,
                theAllowInitialization  = True, 
                theIdioma               = unNuevoIdioma,  
                theCheckPermissions     = False, 
                thePermissionsCache     = unPermissionsCache, 
                theRolesCache           = unRolesCache, 
                theParentExecutionRecord= unExecutionRecord
            )
           
    
            if not unCatalogo.fSetLocalRolesEnIdiomaForCatalogUserGroups( unNuevoIdioma):
                return None
            
            unNuevoIdioma.setPermiteLeer( True)
            unNuevoIdioma.setPermiteModificar( True)
            
            
            unResultadoNuevoIdioma = self.fModelDDvlPloneTool().fRetrieveTypeConfig( 
                theTimeProfilingResults     =None,
                theElement                  =unNuevoIdioma, 
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
                theCheckedPermissionsCache  =thePermissionsCache,
                theAdditionalParams         =None                
            )
            if unResultadoNuevoIdioma:
            
                aModelDDvlPloneTool_Mutators = self.fModelDDvlPloneTool().fModelDDvlPloneTool_Mutators( self)
                    
                aCreateElementReport = aModelDDvlPloneTool_Mutators.fNewVoidCreateElementReport()
                aCreateElementReport.update( { 'effect': 'created', 'new_object_result': unResultadoNuevoIdioma, })
                
                someFieldReports    = aCreateElementReport[ 'field_reports']
                aFieldReportsByName = aCreateElementReport[ 'field_reports_by_name']
                
                aReportForField = { 'attribute_name': 'id',          'effect': 'changed', 'new_value': unaIdIdioma, 'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                
                aReportForField = { 'attribute_name': 'title',       'effect': 'changed', 'new_value': unTitle,           'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                
                aReportForField = { 'attribute_name': 'codigoIdiomaEnGvSIG', 'effect': 'changed', 'new_value': theCodigoIdiomaEnGvSIG,    'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                                   
                aReportForField = { 'attribute_name': 'codigoInternacionalDeIdioma', 'effect': 'changed', 'new_value': theCodigoInternacionalDeIdioma,    'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                                   
                aReportForField = { 'attribute_name': 'nombreNativoDeIdioma', 'effect': 'changed', 'new_value': unNombreNativoIdioma,    'previous_value': '',}
                someFieldReports.append( aReportForField)            
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                                   
                aModelDDvlPloneTool_Mutators.pSetAudit_Creation( self,                cModificationKind_CreateSubElement, aCreateElementReport, theUseCounter=True)       
                aModelDDvlPloneTool_Mutators.pSetAudit_Creation( unNuevoIdioma,       cModificationKind_Create,           aCreateElementReport)       
             
                
                
            unosCodigosIdioma = [ unIdioma.getCodigoIdiomaEnGvSIG() for unIdioma in self.fObjectValues( cNombreTipoTRAIdioma)]            
            unNumIdiomas = len( unosCodigosIdioma)
                  
            unIndexIdiomaAnterior = -1
            for unIndexIdioma in range( unNumIdiomas):
                unCodigoIdioma = unosCodigosIdioma[ unIndexIdioma]
                if unCodigoIdioma < theCodigoIdiomaEnGvSIG:
                    unIndexIdiomaAnterior = unIndexIdioma    
                else:
                    break
                
            if unIndexIdiomaAnterior < 0:
                self.moveObjectsToTop( [ unaIdNuevoIdioma,])
            else:
                if not ( unIndexIdiomaAnterior == ( unNumIdiomas - 1)):
                    if unIndexIdiomaAnterior < ( unNumIdiomas - 1):
                        unDelta = ( unIndexIdiomaAnterior + 2) - unNumIdiomas 
                        self.moveObjectsByDelta( [ unaIdNuevoIdioma,], unDelta)
            
                
            return unNuevoIdioma
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
           
        
            
            
            
            
            
            
            
            

    

        

    security.declareProtected( permissions.ManagePortal, 'fCreateProgressHandlerFor_DeleteLanguage')
    def fCreateProgressHandlerFor_DeleteLanguage( self, 
        theAdditionalParams      =None,  
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None):
        """Request creation of a DeleteLanguage long-lived process control handler, to be executed later.
        
        """

        
        
        def fDeleteLanguageInitialize_lambda( theContextualElement, theProcessControlManager, theAdditionalParmsHere):  
        
            if theContextualElement == None:
                return None
            
            if not theProcessControlManager:
                return None
            
            someInputParameters = theProcessControlManager.vInputParameters
            if not someInputParameters:
                return None
            
            aLanguagesCollectionUID = someInputParameters.get( 'languages_collection_UID', '')
            if not aLanguagesCollectionUID:
                return None
            unaColeccionIdiomas = theContextualElement.fElementoPorUID( aLanguagesCollectionUID)
            if unaColeccionIdiomas == None:
                return None
            
            aLanguageUID = someInputParameters.get( 'language_UID', '')
            if not aLanguageUID:
                return None
            unIdioma = theContextualElement.fElementoPorUID( aLanguageUID)
            if unIdioma == None:
                return None
            
            aLanguageCode = unIdioma.getCodigoIdiomaEnGvSIG()
            someLanguageCodes = [ aLanguageCode,]
            
            unosInitializedObjects = {
                'languages_collection': unaColeccionIdiomas,
                'language':             unIdioma,
                'language_codes':       someLanguageCodes,
            }
                        
            theProcessControlManager.pAddInitializedObjects( unosInitializedObjects)
            
            return None        
                    
         
        
        
        
        
            
        def fDeleteLanguageLoop_lambda( theInitialElement, theProcessControlManager, theAdditionalParmsHere):  
            
            if theInitialElement == None:
                return None
            
            if not theProcessControlManager:
                return None
               
            if not theProcessControlManager.vInitializedObjects:
                return None
               
            unaColeccionIdiomas = theProcessControlManager.vInitializedObjects.get( 'languages_collection', None)
            if unaColeccionIdiomas == None:
                return None
            
            unIdioma = theProcessControlManager.vInitializedObjects.get( 'language', None)
            if unIdioma == None:
                return None
            
            unosCodigosIdiomas = theProcessControlManager.vInitializedObjects.get( 'language_codes', None)
            if not unosCodigosIdiomas:
                return None
            
            if theProcessControlManager.vCatalogoRaiz == None:
                return None            
            
            unasColeccionesCadenas = theProcessControlManager.vCatalogoRaiz.fObtenerTodasColeccionesCadenas()
            for unaColeccionCadenas in unasColeccionesCadenas:
                
                unasCadenas = unaColeccionCadenas.fObtenerTodasCadenas()
                for unaCadena in unasCadenas:
                    
                    theProcessControlManager.vElementLambda( unaCadena, theProcessControlManager, theAdditionalParmsHere)
            
                    
            aNumElementsOfType = { cNombreTipoTRAIdioma: 1, }
            theProcessControlManager.pProcessStep( unIdioma, aNumElementsOfType, aNumElementsOfType)
                    
            
            unaColeccionIdiomas.manage_delObjects( [ unIdioma.getId(), ])
            
            aNumElementsOfType = { cNombreTipoTRAColeccionIdiomas: 1, }
            theProcessControlManager.pProcessStep( unaColeccionIdiomas, aNumElementsOfType, aNumElementsOfType)
             
            
            theProcessControlManager.vCatalogoRaiz.pInvalidateSimbolosCadenasOrdenados()
                        
            return None        
                    
            
            
        
        
        
            
        def fDeleteLanguageElement_lambda( theElement, theProcessControlManager, theAdditionalParmsHere):  
            
            if theElement == None:
                return None
            
            if not theProcessControlManager:
                return None
            
            if not ( theElement.meta_type == cNombreTipoTRACadena):
                return None
            
            unosCodigosIdiomas = theProcessControlManager.vInitializedObjects.get( 'language_codes', None)
            if not unosCodigosIdiomas:
                return None
            
            unNumTranslationsRead = 0
            unNumTranslationsDeleted = 0
            for unCodigoIdioma in unosCodigosIdiomas:
                
                unaTraduccion = theElement.fObtenerTraduccionPorCodigoIdioma( unCodigoIdioma)
                if not ( unaTraduccion == None):
                    
                    unNumTranslationsRead += 1
                    unaTraduccionId = unaTraduccion.getId()
                    if unaTraduccionId:
                        
                        theElement.manage_delObjects( [ unaTraduccionId, ])
                        unNumTranslationsDeleted += 1
                        
            aNumElementsOfTypeRead = { 
                cNombreTipoTRACadena: 1,
                cNombreTipoTRATraduccion: unNumTranslationsRead,
            }
            aNumElementsOfTypeChanged = { 
                cNombreTipoTRACadena: ( unNumTranslationsDeleted and 1) or 0,
                cNombreTipoTRATraduccion: unNumTranslationsDeleted,
            }
            theProcessControlManager.pProcessStep( theElement, aNumElementsOfTypeRead, aNumElementsOfTypeChanged)
                
                
            return None        

        
        
        
        
        
        unExecutionRecord = self.fStartExecution( 'method',  'fCreateProgressHandlerFor_DeleteLanguage', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }, ) 
        
        aThereWasException = False
        
        try:
            
            
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
              
            aResult = self.fNewVoidCreateProgressHandlerResult()

            try:
                
                unCatalogoRaiz = self.getCatalogo()           
                if unCatalogoRaiz == None:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_internal_Missing_RootCatalog', "Internal error: missing root translations catalog-."),
                    })
                    return aResult
                
                unaColeccionProgresos = unCatalogoRaiz.fObtenerColeccionProgresos()
                if unaColeccionProgresos == None:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_internal_Missing_progresses_collection', "Internal error: missing progresses collection-."),
                    })
                    return aResult
                    
                aDeleteLanguageResult = self.fNewVoidProgressResult()
                
                
                aProgressElement = None
                aProgressHandler = None
                                
                aLanguageUID = theAdditionalParams.get( 'language_uid', '')
                if not aLanguageUID:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_Missing_Parameter_LanguageUID', "Required Parameter Missing: Language UID-."),
                    })
                    return aResult
                
                unIdioma = self.fElementoPorUID( aLanguageUID)
                if unIdioma == None:
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_error_Parameter_LanguageNoFoundByUID', "Language not found by UID-."),
                    })
                    return aResult
               
                aMetaType = 'UnknownType'
                try:
                    aMetaType = unIdioma.meta_type
                except:
                    aMetaType = unIdioma.__class__.__name
                if not aMetaType:
                    aMetaType = 'UnknownType'
                
                aStartDateTimeNowTextual = self.fDateTimeNowTextual()
                aDeleteLanguageResult[ 'process_type']           = cTRAProgress_ProcessType_DeleteLanguage
                aDeleteLanguageResult[ 'start_date_time_string'] = aStartDateTimeNowTextual
                aDeleteLanguageResult[ 'date_time_now_string']   = aStartDateTimeNowTextual
                aDeleteLanguageResult[ 'element_type']           = aMetaType
                aDeleteLanguageResult[ 'element_title']          = unIdioma.Title()
                aDeleteLanguageResult[ 'element_path' ]          = unIdioma.fPhysicalPathString()
                aDeleteLanguageResult[ 'element_UID' ]           = unIdioma.UID()
                aDeleteLanguageResult[ 'last_element_type']      = ''
                aDeleteLanguageResult[ 'last_element_title']     = ''
                aDeleteLanguageResult[ 'last_element_path']      = ''
                aDeleteLanguageResult[ 'last_element_UID']       = ''
                
                aMemberId = self.fGetMemberId()
                aDeleteLanguageResult[ 'member_id'] = aMemberId
                
                unCatalogoRaiz = self.getCatalogo()           
                aDeleteLanguageResult[ 'TRACatalogo_title']      = unCatalogoRaiz.Title()
                aDeleteLanguageResult[ 'TRACatalogo_path' ]      = unCatalogoRaiz.fPathDelRaiz()
                aDeleteLanguageResult[ 'TRACatalogo_UID' ]       = unCatalogoRaiz.UID()
                
                    
                # ##################################################
                """Check permissions to execute use case.
                
                """
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_DeleteTRAIdioma, 
                    theElementsBindings     = { cBoundObject: unIdioma,},
                    theRulesToCollect       = [ ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord
                )
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    aResult.update( {
                        'success':     False,
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_no_permission_ToDeleteLanguage', "You do not have permission to Delete Language-."),
                    })
                    return aResult

                 
                
                aLanguagesCollectionUID = self.UID()
                
                
                someInputParameters = { 
                    'languages_collection_UID':  aLanguagesCollectionUID,
                    'language_UID':              aLanguageUID,
                }

                aProgressHandlerCreationResult = unaColeccionProgresos.fCreateNewProgressAndHandlerForElement(  
                    theInitialElement       =unIdioma, 
                    theProcessType          =cTRAProgress_ProcessType_DeleteLanguage, 
                    theInputParameters      =someInputParameters,
                    theTimestamp            =aStartDateTimeNowTextual,
                    theResult               =aDeleteLanguageResult, 
                    theInitializeLambda     =fDeleteLanguageInitialize_lambda,
                    theElementLambda        =fDeleteLanguageElement_lambda,
                    theLoopLambda           =fDeleteLanguageLoop_lambda,
                    theFinalizeLambda       =None,
                    theLockCatalog          =True,
                    thePermissionsCache     =unPermissionsCache, 
                    theRolesCache           =unRolesCache, 
                    theParentExecutionRecord=unExecutionRecord,)
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
                        'condition':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorProgressElementNotKnownByImportProcessElement', "Progress element is not known by progress handler-"),
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
                    'condition':             '',
                    'progress_element':      aProgressElement,
                    'progress_handler':      aProgressHandler,
                    'progress_handler_key':  aProgressHandlerKey,
                })
                 
                return aResult
             
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                aThereWasException = True
                unInformeExcepcion = ''
                try:
                    unInformeExcepcion += 'Exception during fCreateProgressHandlerFor_DeleteLanguage of element %s %s at %s\n'  % (  self.meta_type(), self.Title(), self.fPhysicalPathString())
                except:
                    None
                try:
                    unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                except:
                    None
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                try:
                    unInformeExcepcion += unaExceptionFormattedTraceback   
                except:
                    None
                
                unInformeExcepcionWOResult = unInformeExcepcion[:]
                
                aDeleteLanguageResult[ 'success'] = False
                aDeleteLanguageResult[ 'exception_date_time_string'] = self.fDateTimeNowTextual()
                aDeleteLanguageResultDump = ''
                try:
                    aDeleteLanguageResultDump = self.fProgressResult_dump( aDeleteLanguageResult)
                except:
                    None
                if aDeleteLanguageResultDump:
                    unInformeExcepcion += aDeleteLanguageResultDump
                
                aDeleteLanguageResult[ 'exception_report'] = unInformeExcepcionWOResult

                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
    
                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                aResult = { 
                    'success':    False, 
                    'condition':  '%s\n%s' % (   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_Exception_msgid', "Exception.-"), unInformeExcepcion, ),
                }
                return aResult
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
           
                        
            
            
            
            
                
                    
    
    ##/code-section class-header

    # Methods

# end of class TRAColeccionIdiiomas_Operaciones

##code-section module-footer #fill in your manual code here
##/code-section module-footer



