# -*- coding: utf-8 -*-
#
# File: TRAIdioma_Operaciones.py
#
# Copyright (c) 2009 by Conselleria de Infraestructuras y Transporte de la
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



from Products.Archetypes.public import DisplayList

from Products.CMFCore           import permissions

from Products.ModelDDvlPloneTool.ModelDDvlPloneTool import ModelDDvlPloneTool


from TRAElemento_Constants          import *

from TRAElemento                    import TRAElemento 



from TRAImportarExportar_Constants  import cEncodingSeparatorSentinelName 


from TRAElemento_Permission_Definitions import cUseCase_Copy_Translations
from TRAElemento_Permission_Definitions import cBoundObject


##/code-section module-header


##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema


##code-section after-schema #fill in your manual code here

# ACV20090519 removed
# cLogTimeProfileCrearTraduccionesQueFaltanEnIdioma = True


##/code-section after-schema

class TRAIdioma_Operaciones:
    """
    """
    security = ClassSecurityInfo()



    ##code-section class-header #fill in your manual code here
        


    

                   


        
        
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
            if not ( unEncodingName == cEncodingSeparatorSentinelName):
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
        if not unCatalogo:
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
        if not unCatalogo:
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
        if not unCatalogo:
            return []
        
        
        unosIdiomas = unCatalogo.fObtenerTodosIdiomas()
        if not unosIdiomas:
            return []
        
        otrosIdiomas = [ ]
        for unIdioma in unosIdiomas:
            if not ( unIdioma.getCodigoIdiomaEnGvSIG() == unCodigoIdioma):
                otrosIdiomas.append( unIdioma)
                
        return otrosIdiomas
    
       
     
    
    
    

    
    security.declarePrivate( 'fCopiarTraducciones')    
    def fCopiarTraducciones( self,
        theCopyFromLanguageCode     = '',
        theSourceStatesToCopy       = [],
        theTargetStatesToOverwrite  = [],
        thePermissionsCache         =None,
        theRolesCache               =None,
        theParentExecutionRecord    =None):
        """Copy into this Language Translations from the Language with the specified code. If Source States is specified, only copy source translations on those states. If Target States is specified, only overwrite target translations on those states.
        
        """
    
        unExecutionRecord = self.fStartExecution( 'method',  'fCopiarTraducciones', None, True, { 'log_what': 'details', 'log_when': True, }) # invoked from ModelDDvlPloneTool still using previous style of time profiling, thus the parameter is not theParentExecutionRecord =None, 

        try:
            unasDescripcionesContenidosCreados = []
            try:
                
                if not theCopyFromLanguageCode:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_action_missingParameter_CopyFromLanguageCode', "Parameter Error: Missing parameter: source Language Code to copy Translations from.-"), }
                    return anActionReport  
                
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_Copy_Translations, 
                    theElementsBindings     = { cBoundObject: self,}, 
                    theRulesToCollect       = [ 'languages', ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord,
                )
              
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_no_permission_ToCopyTranslations_msgid', "User does not have permission to copy Translations from other language.-"), }
                    return anActionReport  
                                
                unosIdiomasAccesibles = unUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'languages', {}).get( 'accepted_final_objects', [])
                if not unosIdiomasAccesibles:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_action_warning_NoAvailableLanguagesToCopyFrom', "You can not copy Translations, there are no available Languages to copy from.-"), }
                    return anActionReport  
                            
                unCodigoIdioma = self.getCodigoIdiomaEnGvSIG()
                if unCodigoIdioma == theCopyFromLanguageCode:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_action_warning_CanNotCopyTranslationsFromSameLanguage', "You can not copy Translations from the same Language.-"), }
                    return anActionReport  
                 
                unSourceIdioma = None
                for unIdioma in unosIdiomasAccesibles:
                    if unIdioma.getCodigoIdiomaEnGvSIG() == theCopyFromLanguageCode:
                        unSourceIdioma = unIdioma
                        break
                if not unSourceIdioma:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_action_warning_SelectedSourceLanguageIsNotAvailable', "You can not copy Translations from the selected source Language because it is not available.-"), }
                    return anActionReport  
                
                unCatalogo = self.getCatalogo()
                if not unCatalogo:
                    anActionReport = { 'effect': 'error', 'failure':  'InternalError: gvSIGi18n_copyTranslations_internalError_Missing_TRACatalogo_error_msgid', }
                    return anActionReport  

                unCatalogBusquedaTraduccionesInSourceIdioma = unCatalogo.fCatalogBusquedaTraduccionesParaIdioma( unSourceIdioma)
                if ( unCatalogBusquedaTraduccionesInSourceIdioma == None):
                    anActionReport = { 'effect': 'error', 'failure':  'InternalError: gvSIGi18n_copyTranslations_internalError_Missing_CatalogBusquedaTraducciones_SourceLanguage', }
                    return anActionReport  
               
                
                unaBusqueda = {   'getEstadoCadena' :     cEstadoCadenaActiva, }
                
                someSourceStatesToCopy = [ ]
                if theSourceStatesToCopy:
                    for unEstado in [ cEstadoTraduccionTraducida, cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva]:
                        if unEstado in theSourceStatesToCopy:
                            someSourceStatesToCopy.append( unEstado)
                else:
                    someSourceStatesToCopy = [ cEstadoTraduccionTraducida, cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva]
                    
                if someSourceStatesToCopy:
                    unaBusqueda.update( {   'getEstadoTraduccion' :     someSourceStatesToCopy, })
                    
                           
                unosResultadosBusqueda      = unCatalogBusquedaTraduccionesInSourceIdioma.searchResults(**unaBusqueda)
                
                unasTraduccionesACopiar = [ ]
                for unResultadoBusqueda in unosResultadosBusqueda:
                    unaTraducccion = unResultadoBusqueda.getObject()
                    if unaTraducccion:
                        unaCadenaTraducida = unaTraducccion.getCadenaTraducida()
                        if unaCadenaTraducida:
                            unasTraduccionesACopiar.append( unaTraducccion)
                        
                if not unasTraduccionesACopiar:
                    if theSourceStatesToCopy:
                        anActionReport = { 'effect': 'warning', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_action_warning_NoTranslationsInSourceLanguageInSpecifiedStates', "There are no Translations in the selected source Language in the specified states.-"), }
                    else:
                        anActionReport = { 'effect': 'warning', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_action_warning_NoTranslationsInSourceLanguage', "There are no Translations in the selected source Language.-"), }
                    return anActionReport  

                        
                
                aModelDDvlPlone_tool = ModelDDvlPloneTool()
                             
                             
                unaColeccionImportaciones = unCatalogo.fObtenerColeccionImportaciones()
                if not unaColeccionImportaciones:
                    anActionReport = { 'effect': 'error', 'failure':  'InternalError: gvSIGi18n_errorCreating_Idioma_Missing_TRAColeccionImportaciones_error_msgid', }
                    return anActionReport  
                
                     
                unMemberId = self.fGetMemberId()
                unaFechaYHora = self.fDateTimeNowTextual()

                aPloneUtilsTool = self.getPloneUtilsToolForNormalizeString()  
               
                unTitleImportacion = '%s %s->%s by %s on %s' % ( self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_copyTranslations_Importacion_prefix', "To Copy Translations from Language to Language"), theCopyFromLanguageCode, unCodigoIdioma, unMemberId, unaFechaYHora)
                aNewIdImportacion = unTitleImportacion.lower().replace( ' ', '-')
                if aPloneUtilsTool:
                    aNewIdImportacion = aPloneUtilsTool.normalizeString( aNewIdImportacion)
 
                anAttrsDictImportacion = { 
                    'title':         unTitleImportacion,
                    'description':   '',
                }
                
                unaIdNuevaImportacion = unaColeccionImportaciones.invokeFactory( cNombreTipoTRAImportacion, aNewIdImportacion, **anAttrsDictImportacion)
                if not unaIdNuevaImportacion:
                    anActionReport = { 'effect': 'error', 'failure': '%s' %   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Strings_TRAImportacion_NotCreated_msgid', "Error creating strings: import not created.-"), }
                    return anActionReport     
                                
                unaNuevaImportacion = unaColeccionImportaciones.getElementoPorID( unaIdNuevaImportacion)
                if not unaNuevaImportacion:
                    anActionReport = { 'effect': 'error', 'failure': '%s' %  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Strings_TRAImportacion_Created_TRAImportacion_NotFound_msgid', "Could not find import just created-."), }
                    return anActionReport     

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
                    anActionReport = { 'effect': 'error', 'failure': '%s' %   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Idioma_TRAContenidoIntercambio_NotCreated_msgid', "Error creating language: import not created.-"), }
                    return anActionReport     
                                
                unNuevoContenidoIntercambio = unaNuevaImportacion.getElementoPorID( unaIdNuevoContenidoIntercambio)
                if not unNuevoContenidoIntercambio:
                    anActionReport = { 'effect': 'error', 'failure': '%s' %  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Idioma_Created_TRAContenidoIntercambio_NotFound_msgid', "Could not find interchange contents just created-."), }
                    return anActionReport     
                
                
                someStringsAndTranslations = { }
                
                for unaTraduccion in unasTraduccionesACopiar:
                    unSimboloCadena                     = unaTraduccion.getSimbolo()
                    unaCadenaTraducida                  = unaTraduccion.getCadenaTraducida()
                    if unaCadenaTraducida:
                        unasTraduccionesCadena = { unCodigoIdioma: unaCadenaTraducida,}
                        someStringsAndTranslations[ unSimboloCadena] = unasTraduccionesCadena
                                        
                
                unContenidoConCadenas = { 'strings_and_translations': someStringsAndTranslations, }
                unNuevoContenidoIntercambio.pSetContenido( unContenidoConCadenas)
                
                unTimeProfilingResults = { }
                unResultadoNuevaImportacion = aModelDDvlPlone_tool.fRetrieveTypeConfig( 
                    theTimeProfilingResults     =unTimeProfilingResults,
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
                    anActionReport = { 'effect': 'error', 'failure': 'retrieval_failure', }
                    return anActionReport     
 
                unStringsCreationReport = { 'effect': 'created', 'new_object_result': unResultadoNuevaImportacion, }
                        
                return unStringsCreationReport
                
 
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fCopiarTraducciones\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                                         
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                anActionReport = { 'effect': 'error', 'failure': '%s\n%s' % (   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorCreating_Cadeas_Exception_msgid', "Exception while creating Strings (as import process).-"), unInformeExcepcion, ) }
                return anActionReport     
              
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

                    
                
                    
            
            
            
                
    
    
    
# ####################################
#  Complete initialization after creation
#
        
     
    
    security.declarePrivate('pHandle_manage_afterAdd')
    def pHandle_manage_afterAdd(self, theItem, theContainer):   
        
        TRAElemento.manage_afterAdd(  self, theItem, theContainer)
        
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





        


    


    

    
    
    
    
    
    
    
    
    
    





    
    