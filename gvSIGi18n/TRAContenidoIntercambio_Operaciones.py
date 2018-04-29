# -*- coding: utf-8 -*-
#
# File: TRAContenidoIntercambio_Operaciones.py
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


from AccessControl import ClassSecurityInfo




import logging

import transaction

from math import floor


from StringIO import StringIO

from zipfile import ZipFile

from Products.Archetypes.utils import shasattr

from Products.CMFCore.utils import getToolByName

from Products.CMFCore       import permissions

from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fMillisecondsNow, fDateTimeNow, fReprAsString, fEvalString


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
 
    
    
    
    
    
    security.declareProtected( permissions.View, 'getImportacion')
    def getImportacion( self):
        return self.getContenedor()
   


    
    security.declarePrivate( 'pSetContenido')    
    def pSetContenido( self, theContenido):

        unAhora = fDateTimeNow()
        
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
        
        aTranslationService = getToolByName( self, 'translation_service', None)

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
    




    
            
    #security.declarePrivate( 'fStringFromContenidoDeUploadedFile_ORIG')    
    #def fStringFromContenidoDeUploadedFile_ORIG( self, theContenidoUploadedFile):
        
        #aTranslationService = getToolByName( self, 'translation_service', None)

        #unStreamContenido = StringIO( u'')
        
        #unStreamContenido.write( u'%s\n' % cElementTranslationsInterchangeOpen)
        
        #someLanguages = theContenidoUploadedFile.get( 'languages', [])
        #unStreamContenido.write( u'%s\n' % cElementLanguagesOpen)
        #for unLenguage in someLanguages:
            #unStreamContenido.write( u'%s\n' % (cElementLanguage % unLenguage))
        #unStreamContenido.write( u'%s\n' % cElementLanguagesClose)

        
        
        #someLanguagesDetails = theContenidoUploadedFile.get( 'languages_details', [])
        #if someLanguagesDetails:
            #someUnicodeLanguagesDetails = {}
            
            #for unLenguage in someLanguagesDetails.keys():

                #someDetailsForLanguage = {}

                #unosDetailsForLanguage = someLanguagesDetails[ unLenguage]
                #if unosDetailsForLanguage:
                    
                    #unosDetailsKeys = unosDetailsForLanguage.keys()
                    #for unDetailKey in unosDetailsKeys:

                        #unDetailValue = unosDetailsKeys.get( unDetailKey)
                        #if unDetailValue:

                            #unUnicodeDetailValue = aTranslationService.asunicodetype( unDetailValue, errors="strict")
                            #if unUnicodeDetailValue:

                                #someDetailsForLanguage[ unDetailKey] = unUnicodeDetailValue
                    
                #if someDetailsForLanguage:
                    #someUnicodeLanguagesDetails[ unLenguage] = someDetailsForLanguage
            
            #if someUnicodeLanguagesDetails:
                    
                #aLanguagesDetailsString = fReprAsString( someUnicodeLanguagesDetails)
                #unStreamContenido.write( u'%s\n' % (cElementLanguageDetails % aLanguagesDetailsString))
            

            
            
        #unStreamContenido.write( u'%s\n' % (cElementLanguage % fReprAsString( someLanguagesDetails)))
        
        #someModules = theContenidoUploadedFile.get( 'modules', [])
        #unStreamContenido.write(  u'%s\n' % cElementModulesOpen)
        #for unModule in someModules:
            #unStreamContenido.write( u'%s%s%s\n' % ( cElementModuleOpen, unModule, cElementModuleClose, ) )
        #unStreamContenido.write( u'%s\n' % cElementModulesClose)
        
        #someStringsAndTranslations = theContenidoUploadedFile.get( 'strings_and_translations', {})
        #someStringsWithEncodingErrors = theContenidoUploadedFile.get( 'strings_with_encoding_errors', {})
        #someStringsSources = theContenidoUploadedFile.get( 'strings_sources', {})

        #unStreamContenido.write( u'%s\n' % cElementStringsOpen)
        
        #someSymbols = someStringsAndTranslations.keys()
        #for unSimbolo in someSymbols:
            #unStreamContenido.write( u'%s\n' %  ( cElementStringOpen % aTranslationService.asunicodetype( unSimbolo, errors="strict")))
            #unasTranslations = someStringsAndTranslations.get( unSimbolo, {})
            #unosLenguagesWithEncodingErrors = someStringsWithEncodingErrors.get( unSimbolo, [])
            #unosLanguages = unasTranslations.keys()
            #for unLenguage in unosLanguages:
                #unLenguageUnicode = aTranslationService.asunicodetype( unLenguage, errors="strict")
                #if ( unLenguage in unosLenguagesWithEncodingErrors):
                    #unStreamContenido.write( cElementEncodingError % unLenguageUnicode )
                #else:
                    #unaTranslation = unasTranslations.get( unLenguage, '')
                    #if unaTranslation:
                        #unaTranslation = unaTranslation.replace('\n', '').replace( '\t', '')
                        #unaTranslationUnicode = ''
                        #try:
                            #unaTranslationUnicode = aTranslationService.asunicodetype( unaTranslation, errors="strict")
                        #except:
                            #None
                        #if unaTranslationUnicode:
                            #try:
                                #unaStringElementTraduccion = cElementTranslation % ( unLenguageUnicode, unaTranslationUnicode,)
                                #unStreamContenido.write( u'%s\n' % unaStringElementTraduccion)
                            #except:
                                #None
            
            #unString_Sources = someStringsSources.get( unSimbolo, '').strip()
            #if unString_Sources:
                #try:
                    #unStreamContenido.write( u'%s%s%s\n' % ( cElementSourcesOpen, unString_Sources, cElementSourcesClose,))
                #except:
                    #None
                
            
                                
            #unStreamContenido.write( u'%s\n' % cElementStringClose)
                    
        #unStreamContenido.write( u'%s\n' % cElementStringsClose)
            
        #unStreamContenido.write( u'%s\n' % cElementTranslationsInterchangeClose)

        #unStringContenidoUnicode = unStreamContenido.getvalue()

        #unStringContenidoEncoded = aTranslationService.encode( unStringContenidoUnicode) 
        
        #return unStringContenidoEncoded
    


    
    
            
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
        
        if not theContenidoString:
            return None
        
        aContenido = fEvalString( theContenidoString)
        
        return aContenido
    
            

    #security.declarePrivate( 'fContenidoFromString')    
    #def fContenidoFromString( self, theContenidoString, theParentExecutionRecord=None):
        
        #unExecutionRecord = self.fStartExecution( 'method',  'fContenidoFromString', theParentExecutionRecord,  False, ) 
        
        #try:
            
            #unContenido = self.fNewVoidUploadedContent()
            
            #if not theContenidoString:
                #return unContenido
    
            #aTranslationService = getToolByName( self, 'translation_service', None)
            #unContenidoUnicodeString = ''
            #try:
                #unContenidoUnicodeString = aTranslationService.asunicodetype( theContenidoString, errors="strict")
            #except:
                #None
            #if not unContenidoUnicodeString:
                #return unContenido
    
            
            #someLines = unContenidoUnicodeString.split( '\n')
            #unNumLines = len( someLines)
            #unLineIndex = 0
            
            #unEstado = cEstadoExpectTranslationsInterchange
            #unEstadoError = ''
            #unCurrentLineIndex = -1
            #unCurrentSymbol = ''
            
            #while( unLineIndex < unNumLines):
                #unaLine = someLines[ unLineIndex].strip()
                #unCurrentLineIndex = unLineIndex
                #unLineIndex += 1
                #if unaLine:
    
                    #if unEstado == cEstadoExpectTranslationsInterchange:
                        #if unaLine.startswith( cElementTranslationsInterchangeOpen):
                            #unEstado = cEstadoExpectLanguagesOrModulesOrStringsOrTranslationsInterchangeClose    
                            #continue
     
                        #if unaLine.startswith( cElementTranslationsInterchangeClose):
                            #unEstado = cEstadoFinal    
                            #continue
    
                        #else:
                            #unEstadoError = unEstado
                            #break
    
                    #elif unEstado == cEstadoExpectLanguagesOrModulesOrStringsOrTranslationsInterchangeClose:
                        #if unaLine.startswith( cElementLanguagesOpen):
                            #unEstado = cEstadoExpectLanguageOrLanguagesClose    
                            #continue
                        
                        #elif unaLine.startswith( cElementModulesOpen):
                            #unEstado = cEstadoExpectModuleOrModulesClose    
                            #continue
                                           
                        #elif unaLine.startswith( cElementStringsOpen):
                            #unEstado = cEstadoExpectStringOrStringsClose    
                            #continue
                            
                        #else:
                            #unEstadoError = unEstado
                            #break
                     
                    #elif unEstado == cEstadoExpectLanguageOrLanguagesClose:
                        #if unaLine.startswith( cElementLanguagePrefix):
                            #unQuoteIndex = unaLine.find( cElementAttributeQuote, len( cElementLanguagePrefix))
                            #if unQuoteIndex:
                                #unLanguageCode = unaLine[ len( cElementLanguagePrefix): unQuoteIndex]
                                #if unLanguageCode:
                                    #unEncodedLanguageCode = aTranslationService.encode( unLanguageCode)
                                    #if unEncodedLanguageCode:
                                        #unContenido[ 'languages'].append( unEncodedLanguageCode)
                            #unEstado = cEstadoExpectLanguageOrLanguagesClose
                            #continue
    
                        #elif unaLine.startswith( cElementLanguagesClose):
                            #unEstado = cEstadoExpectLanguagesOrModulesOrStringsOrTranslationsInterchangeClose
                            #continue
                        
                    #elif unEstado == cEstadoExpectModuleOrModulesClose:
                        #if unaLine.startswith( cElementModuleOpen):
                            #unCloseIndex = unaLine.find( cElementModuleClose, len( cElementModuleOpen))
                            #if unCloseIndex:
                                #unModuleName = unaLine[ len( cElementModuleOpen): unCloseIndex]
                                #if unModuleName:
                                    #unEncodedModuleName = aTranslationService.encode( unModuleName)
                                    #if unEncodedModuleName:
                                        #unContenido[ 'modules'].append( unEncodedModuleName)
                            #unEstado = cEstadoExpectModuleOrModulesClose
                            #continue
    
                        #elif unaLine.startswith( cElementModulesClose):
                            #unEstado = cEstadoExpectLanguagesOrModulesOrStringsOrTranslationsInterchangeClose
                            #continue
    
                    #elif unEstado == cEstadoExpectStringOrStringsClose:
                        #if unaLine.startswith( cElementStringPrefix):
                            #unQuoteIndex = unaLine.find( '"', len( cElementStringPrefix))
                            #if unQuoteIndex:
                                #unSymbol = unaLine[ len( cElementStringPrefix): unQuoteIndex]
                                #if unSymbol:
                                    #unEncodedSymbol = aTranslationService.encode( unSymbol)
                                    #unCurrentSymbol = unEncodedSymbol
                                    #if not ( unContenido[ 'strings_and_translations'].has_key( unCurrentSymbol)):
                                        #unContenido[ 'strings_and_translations'][ unCurrentSymbol] = {}
                            #unEstado = cEstadoExpectTraduccionOrStringClose
                            #continue
    
                        #elif unaLine.startswith( cElementStringsClose):
                            #unEstado = cEstadoExpectLanguagesOrModulesOrStringsOrTranslationsInterchangeClose
                            #continue
    
                    #elif unEstado == cEstadoExpectTraduccionOrStringClose:
                        #if not unCurrentSymbol:
                            #unEstadoError = unEstado
                            #break
                             
                        #if unaLine.startswith( cElementTranslationPrefix):
                            #unQuoteIndex = unaLine.find( cElementAttributeQuote, len( cElementTranslationPrefix))
                            #if unQuoteIndex:
                                #unLanguage = unaLine[ len( cElementTranslationPrefix): unQuoteIndex]
                                #if unLanguage:
                                    #unEncodedLanguage = aTranslationService.encode( unLanguage)
                                    #unGTIndex = unaLine.find( cElementDelimiterGT, unQuoteIndex + 1)
                                    #if unGTIndex:
                                        #unCloseIndex = unaLine.find( cElementTranslationClose, unGTIndex + 1)
                                        #if unCloseIndex:
                                            #unaUnicodeTranslation = unaLine[ unGTIndex + 1: unCloseIndex]
                                            #if unaUnicodeTranslation:
                                                #unaEncodedTranslation = aTranslationService.encode( unaUnicodeTranslation)
                                                #if unaEncodedTranslation:
                                                    #unContenido[ 'strings_and_translations'][ unCurrentSymbol][ unEncodedLanguage] = unaEncodedTranslation
                                                
                            #unEstado = cEstadoExpectTraduccionOrStringClose
                            #continue
                        
                        #elif unaLine.startswith( cElementEncodingErrorPrefix):
                            
                            #unQuoteIndex = unaLine.find( cElementAttributeQuote, len( cElementEncodingErrorPrefix))
                            #if unQuoteIndex:
                                #unLanguage = unaLine[ len( cElementEncodingErrorPrefix): unQuoteIndex]
                                #if unLanguage:
                                    #if unContenido[ 'strings_with_encoding_errors'].has_key( unCurrentSymbol):
                                        #unContenido[ 'strings_with_encoding_errors'][ unCurrentSymbol].append( unLanguage)   
                                    #else:
                                        #unContenido[ 'strings_with_encoding_errors'][ unCurrentSymbol] = [  unLanguage, ]
                            #unEstado = cEstadoExpectTraduccionOrStringClose
                            #continue # ACV OJO 200904012058 (should not matter much having a continue or not, as there is nothing after this in the loop

                        
                        
                        
                        #elif unaLine.startswith( cElementSourcesOpen):
                            
                            #unCloseIndex = unaLine.find( cElementSourcesClose, len( cElementSourcesOpen))
                            #if unCloseIndex:
                                #unSources = unaLine[ len( cElementSourcesOpen): unCloseIndex]
                                #if unSources:
                                    #unStringSources = unContenido[ 'strings_sources'].get( unCurrentSymbol, '').strip()
                                    #if not unStringSources:
                                        #unStringSources = unSources
                                    #else:
                                        #if not ( unStringSources.find( unSources) >= 0):
                                            #unStringSources = '%s %s' % ( unStringSources, unSources, )
                                    #if unStringSources:
                                        #unContenido[ 'strings_sources'][ unCurrentSymbol] = unStringSources  
                                        
                            #unEstado = cEstadoExpectTraduccionOrStringClose
                            #continue 
                        
                        #elif unaLine.startswith( cElementStringClose):
                            #unEstado = cEstadoExpectStringOrStringsClose
                            #continue
    
                    #elif unEstado == cEstadoFinal:
                        #break
                    
                    #else:
                        #unEstadoError = unEstado
                        #break
                        
            #return unContenido
        #finally:
            #unExecutionRecord and unExecutionRecord.pEndExecution()
       
        
      
            
        
    
    
    
    
    
    
    
    
    
    
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
            if not unasStringsAndTranslations:
                return unInforme
            
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
        
    
 

       
 
    
    
    
    



    
    