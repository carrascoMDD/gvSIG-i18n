# -*- coding: utf-8 -*-
#
# File: TRAContenidoIntercambio_Operaciones.py
#
# Copyright (c) 2008, 2009,2010 by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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


from AccessControl import ClassSecurityInfo




import logging

import transaction

from math import floor


from StringIO import StringIO

from zipfile import ZipFile

from Products.Archetypes.utils import shasattr

from Products.CMFCore.utils import getToolByName

from Products.CMFCore       import permissions


from TRAElemento_Constants import *


from TRAElemento_Operaciones            import TRAElemento_Operaciones



cElementAttributeQuote          = u'"'
cElementDelimiterGT             = u'>'
cElementTranslationsInterchangeOpen           = u'<translationsinterchange>'   
cElementTranslationsInterchangeClose           = u'</translationsinterchange>'   
cElementLanguagesOpen           = u'<languages>'   
cElementLanguagesClose          = u'</languages>'
cElementLanguagePrefix          = u'<language code="'
cElementLanguagePostfix         = u'%s" />'
cElementLanguage                = cElementLanguagePrefix + cElementLanguagePostfix
cElementLanguageDetails         = u'<languagesdetails>%s</languagesdetails>'
cElementModulesOpen             = u'<modules>'
cElementModulesClose            = u'</modules>'
cElementModuleOpen              = u'<module>'
cElementModuleClose             = u'</module>'
cElementStringsOpen             = u'<strings>'
cElementStringsClose            = u'</strings>'
cElementStringPrefix            = u'<str sym="'
cElementStringPostfix           = u'%s" >'
cElementStringOpen              = cElementStringPrefix + cElementStringPostfix
cElementStringClose             = u'</str>'
cElementSourcesOpen             = u'<sou>'
cElementSourcesClose            = u'</sou>'
cElementEncodingErrorPrefix     = u'<tra err="'
cElementEncodingErrorPostfix    = u'%s"/>'
cElementEncodingError           = cElementEncodingErrorPrefix + cElementEncodingErrorPostfix
cElementTranslationPrefix       = u'<tra code="'
cElementTranslationClose      = u'</tra>'
cElementTranslation             = cElementTranslationPrefix + u'%s' + cElementAttributeQuote + cElementDelimiterGT + u'%s' + cElementTranslationClose
 

cEstadoExpectTranslationsInterchange        = 'ExpectTranslationsInterchange'
cEstadoExpectLanguagesOrModulesOrStringsOrTranslationsInterchangeClose    = 'ExpectLanguagesOrModulesOrStringsOrTranslationsInterchangeClose'
cEstadoExpectLanguageOrLanguagesClose       = 'ExpectLanguageOrLanguagesClose'
cEstadoExpectModuleOrModulesClose           = 'ExpectModuleOrModulesClose'
cEstadoExpectStringOrStringsClose           = 'ExpectStringOrStringsClose'
cEstadoExpectTraduccionOrStringClose        = 'ExpectTraduccionOrStringClose'
cEstadoFinal                                = 'Final'







class TRAContenidoIntercambio_Operaciones:
    """
    """
    security = ClassSecurityInfo()
 
    
    

    security.declarePrivate( 'pAllSubElements_into')    
    def pAllSubElements_into( self, theCollection, theAdditionalParms=None):
        if theCollection == None:
            return self
        theCollection.append( self)
        
         
        return self
        
        
    


    security.declarePrivate( 'pForAllElementsDo_recursive')    
    def pForAllElementsDo_recursive( self, theLambda):
        if not theLambda:
            return self
        
        theLambda( self)

        return self
    
    
    
    security.declareProtected( permissions.View, 'getImportacion')
    def getImportacion( self):
        return self.getContenedor()
   


    
    security.declarePrivate( 'pSetContenido')    
    def pSetContenido( self, theContenido):
        
        unAhora = self.fDateTimeNow()
        
        if not theContenido:
            self.setContenido( '')
            self.setFechaContenido( unAhora)
            return self
    
        unContenidoString = self.fStringFromContenidoDeUploadedFile( theContenido)
        unContenidoActual = self.getContenido()
        if not ( unContenidoString ==  unContenidoActual):
            self.setContenido( unContenidoString)
            self.setFechaContenido( unAhora)
        
        return self
    
    
            
            
    security.declarePrivate( 'fStringFromContenidoDeUploadedFile')    
    def fStringFromContenidoDeUploadedFile( self, theContenidoUploadedFile):

        from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fReprAsString        

        aTranslationService = self.getTranslationServiceTool()

        aContenidoStructureToConvert = self.fNewVoidUploadedContent()
        
        someLanguages = theContenidoUploadedFile.get( 'languages', [])
        if someLanguages:
            aContenidoStructureToConvert[ 'languages'].extend( someLanguages)
        
        someLanguagesDetails = theContenidoUploadedFile.get( 'languages_details', [])
        if someLanguagesDetails:
            
            someLanguagesDetailsToConvert = aContenidoStructureToConvert[ 'languages_details']
            
            for aLanguage, aLanguageDetails in someLanguagesDetails.items():
                
                if aLanguage and aLanguageDetails:
                    
                    someDetailsForLanguageToConvert = someLanguagesDetailsToConvert.get( aLanguage, {})
                    if not someDetailsForLanguageToConvert:
                        someDetailsForLanguageToConvert = {}
                        someLanguagesDetailsToConvert[ aLanguage] = someDetailsForLanguageToConvert
                        
                    for aDetailKey, aDetailValue in aLanguageDetails.items():
                        
                        if aDetailKey and ( aDetailKey in cAcceptedLanguageDetailKeys):

                            someDetailsForLanguageToConvert[ aDetailKey] = aDetailValue
                        
        
        someModules = theContenidoUploadedFile.get( 'modules', [])
        aContenidoStructureToConvert[ 'modules'] = someModules[:]
       
        
        
        someStringsAndTranslations    = theContenidoUploadedFile.get( 'strings_and_translations', {})
        someStringsWithEncodingErrors = theContenidoUploadedFile.get( 'strings_with_encoding_errors', {})
        someStringsSources            = theContenidoUploadedFile.get( 'strings_sources', {})

        someStringsAndTranslationsToConvert    = aContenidoStructureToConvert[ 'strings_and_translations']
        someStringsWithEncodingErrorsToConvert = aContenidoStructureToConvert[ 'strings_with_encoding_errors']
        someStringsSourcesToConvert            = aContenidoStructureToConvert[ 'strings_sources']

        
        someSymbols = someStringsAndTranslations.keys()
        for unSimbolo in someSymbols:
            
           
            unasTranslations                = someStringsAndTranslations.get( unSimbolo, {})
            unosLanguages                   = unasTranslations.keys()
            unosLenguagesWithEncodingErrors = someStringsWithEncodingErrors.get( unSimbolo, [])

            unasTranslationsToConvert = someStringsAndTranslationsToConvert.get( unSimbolo, {})
            if not unasTranslationsToConvert:
                unasTranslationsToConvert = { }
                someStringsAndTranslationsToConvert[ unSimbolo] = unasTranslationsToConvert
                
            unosLenguagesWithEncodingErrorsToConvert = someStringsWithEncodingErrorsToConvert.get( unSimbolo, [])
            if not unosLenguagesWithEncodingErrorsToConvert:
                unosLenguagesWithEncodingErrorsToConvert = [ ]
                someStringsWithEncodingErrorsToConvert[ unSimbolo] = unosLenguagesWithEncodingErrorsToConvert
                
            unosSourcesToConvert = someStringsSourcesToConvert.get( unSimbolo, [])
            if not unosSourcesToConvert:
                unosSourcesToConvert = [ ]
                someStringsSourcesToConvert[ unSimbolo] = unosSourcesToConvert
                
                
                
            for unLenguage in unosLanguages:
                
                if not ( unLenguage in unosLenguagesWithEncodingErrors):
                    
                    unaTranslation = unasTranslations.get( unLenguage, '')
                    if unaTranslation:
                        
                        unaTranslation = unaTranslation.replace('\n', '').replace( '\t', '')
                        if unaTranslation:
                            
                            unasTranslationsToConvert[ unLenguage] =  unaTranslation 
                           
                else:
                    if not ( unLenguage in unosLenguagesWithEncodingErrorsToConvert):
                        unosLenguagesWithEncodingErrorsToConvert.append( unLenguage)
            
            unString_Sources = someStringsSources.get( unSimbolo, [])
            if unString_Sources:
                unosSourcesToConvert.extend( unString_Sources)
                                


        unStringContenido = fReprAsString( aContenidoStructureToConvert)
        
        return unStringContenido
    




    
            


    
    
            
    security.declarePrivate( 'fContenido')    
    def fContenido( self, theParentExecutionRecord=None):

        unExecutionRecord = self.fStartExecution( 'method',  'fContenido', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 
        
        try:
            
            unContenidoString = self[ 'contenido']()
            if not unContenidoString:
                return self.fNewVoidUploadedContent()
            
            unContenido = self.fContenidoFromString( unContenidoString, unExecutionRecord)
            return unContenido
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

            
            
                                           

    security.declarePrivate( 'fContenidoFromString')    
    def fContenidoFromString( self, theContenidoString, theParentExecutionRecord=None):
        
        from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fEvalString
        
        if not theContenidoString:
            return None
        
        aContenido = fEvalString( theContenidoString)
        
        return aContenido
    
            

        
    
    
    
    
    
    
    
    
    
    
    security.declarePrivate( 'fInformeContenidoIntercambio')    
    def fInformeContenidoIntercambio( self, theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fInformeContenidoIntercambios', theParentExecutionRecord,  False, ) 
        
        try:
            unContenido = self.fContenido( unExecutionRecord)
    
            if not unContenido:
                return None
            
            unInforme = self.fNewVoidContenidoIntercambioReport()
            
            unInforme[ 'language_names_and_flags'] = self.fLanguagesNamesAndFlagsPorCodigo() 
            
            unasStringsAndTranslations = unContenido[ 'strings_and_translations']
            #if not unasStringsAndTranslations:
                #return unInforme
            
            unasStringsAndEncodingErrors = unContenido[ 'strings_with_encoding_errors']
            if not unasStringsAndEncodingErrors:
                unasStringsAndEncodingErrors = {}
                
    
            unasStrings = unasStringsAndTranslations.keys()
            unNumStrings = len( unasStrings)
            unInforme[ 'num_strings'] = unNumStrings
           
            unosNumTranslationsByLanguage = unInforme[ 'num_translated_by_language']
            unosNumEncodingErrorsByLanguage = unInforme[ 'num_encoding_errors_by_language']
            for unLanguage in unContenido[ 'languages']:
                unosNumTranslationsByLanguage[      unLanguage] = 0    
                unosNumEncodingErrorsByLanguage[    unLanguage] = 0    
    
            for unaString in unasStrings:
                unasTranslations = unasStringsAndTranslations[ unaString]
                unosLenguages = unasTranslations.keys()
                for unLenguage in unosLenguages:
                    unosNumTranslationsByLanguage[ unLenguage] = unosNumTranslationsByLanguage.get( unLenguage, 0) + 1  
                unosLenguajesConEncodingErrors = unasStringsAndEncodingErrors.get( unaString, [])
                for unLenguage in unosLenguajesConEncodingErrors:
                    if not (unLenguage in unosLenguages):
                        unosNumEncodingErrorsByLanguage[ unLenguage] = unosNumEncodingErrorsByLanguage.get( unLenguage, 0) + 1  
                    
            unosLenguages =  sorted( unContenido[ 'languages'])
            unInforme[ 'languages'] = unosLenguages
            
            for unLenguage in unosLenguages:
                unNumeroTraducciones = unosNumTranslationsByLanguage[ unLenguage]
                if not unNumeroTraducciones:
                    unPercentPending     = 100
                    unPercentTranslated  = 0
                    unPercentEncodingErrors = 0
                else:
                    unPercentTranslated = int( ( ( 0.0 + unNumeroTraducciones) / unNumStrings) * 100)
                    if not unPercentTranslated:
                        unPercentTranslated = 1
                    unPercentPending = 100 - unPercentTranslated
                    unPercentEncodingErrors = int( ( ( 0.0 + unosNumEncodingErrorsByLanguage[ unLenguage]) / unNumStrings) * 100)
                    
                unInforme[ 'num_pending_by_language'][        unLenguage] = unNumStrings - unNumeroTraducciones
                unInforme[ 'percent_pending_by_language'][    unLenguage] = unPercentPending
                unInforme[ 'percent_translated_by_language'][ unLenguage] = unPercentTranslated
                unInforme[ 'num_encoding_errors_by_language'][unLenguage] = unosNumEncodingErrorsByLanguage[ unLenguage]
                unInforme[ 'percent_encoding_errors_by_language'][ unLenguage] = unPercentEncodingErrors
                        

            unNombreModulo = self.getNombreModulo()
            if unNombreModulo:
                unInforme[ 'modules'] = [ unNombreModulo, ]
                
            return unInforme
         
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
       
        
      
    
    
    
    
    
    
   
    security.declarePrivate( 'fSumarioContenido')    
    def fSumarioContenido( self, theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fSumarioContenido', theParentExecutionRecord,  False, ) 
        
        try:
            unInformeContenido = self.fInformeContenido( unExecutionRecord)
            if not unInformeContenido:
                return ''
            
            unNumeroCadenas = unInformeContenido.get( 'num_strings', 0)
            unLanguageNames = ','.join( unInformeContenido.get( 'languages', []))
            
            unSumario = '#%d  %s' % (  unNumeroCadenas,  unLanguageNames)
            
            return unSumario
    
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
       
        
  
 

    
  
 
    
    
            
    
    security.declarePublic( 'fExtraLinks')    
    def fExtraLinks( self):
        
        unosExtraLinks = TRAElemento_Operaciones.fExtraLinks( self)
        if not unosExtraLinks:
            unosExtraLinks = [ ]
        
        unaURL = self.absolute_url()
        if not unaURL:
            return unosExtraLinks
        

        unExtraLink = self.fNewVoidExtraLink()
        unExtraLink.update( {
            'label'   : self.fTranslateI18N( 'plone', 'Data', 'Data-',),
            'href'    : '%s/TRAContenidoIntercambioDatos/' % unaURL,
            'icon'    : '',
            'domain'  : 'plone',
            'msgid'   : 'Data',
        })
        unosExtraLinks.append( unExtraLink)      
        
        
        unImportacionURL = self.getContenedor().absolute_url()
        if not unImportacionURL:
            return unosExtraLinks
        
        unExtraLink = self.fNewVoidExtraLink()
        unExtraLink.update( {
            'label'   : self.fTranslateI18N( 'plone', 'Summary', 'Summary-',),
            'href'    : '%s/TRAImportacionContenidosSumario/' % unImportacionURL,
            'icon'    : '',
            'domain'  : 'plone',
            'msgid'   : 'Summary',
        })
        unosExtraLinks.append( unExtraLink)
                            
        unExtraLink = self.fNewVoidExtraLink()
        unExtraLink.update( {
            'label'   : self.fTranslateI18N( 'plone', 'Details', 'Details-',),
            'href'    : '%s/TRAImportacionContenidosDetalle/' % unImportacionURL,
            'icon'    : '',
            'domain'  : 'plone',
            'msgid'   : 'Details',
        })
        unosExtraLinks.append( unExtraLink)
                                    

        return unosExtraLinks
        
    
 

       
 
    
    
    
    



    
    