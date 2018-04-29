# -*- coding: utf-8 -*-
#
# File: TRAImportacion_Operaciones_Parse_GNUgettextPO.py
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



import sys
import traceback



import os
import logging

import time

import transaction

from math import floor

from DateTime import DateTime


from StringIO import StringIO

from zipfile import ZipFile


from Products.Archetypes.utils import shasattr

from Products.CMFCore.utils import getToolByName


from Products.CMFCore       import permissions

from Products.Archetypes.utils import getRelURL







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

from TRAImportarExportar_Constants                import *
from TRAImportarExportar_Constants_GNUgettextPO   import *
from TRAImportarExportar_Constants_Encodings      import *




class TRAImportacion_Operaciones_Parse_GNUgettextPO:
    """
    """
    security = ClassSecurityInfo()
     


    
    
        

    
    
            

    
    
    security.declarePrivate( 'fVoidPOHeader')    
    def fVoidPOHeader( self):
        unPOHeader = {
            'language_code':             '',
            'language_name':             '',
            'country':                   '',
            'language_and_country':      '',
            'charset':                   '',
            'is_fallback_for':           '',
            'domain':                    '',
            'last_line_number':          -1,
        }
        return unPOHeader
        
         
    
  
       
                
    
                
    security.declarePrivate( 'fPOHeaderFromZipPOFile')    
    def fPOHeaderFromZipPOFile( self, theParentExecutionRecord, theZipFile, theFileName):
        
        if not theFileName or not theZipFile:
            return self.fVoidPOHeader()
        
        if not ( theFileName.lower().endswith( cPOFilePostfix.lower()) or theFileName.lower().endswith( cPOTFilePostfix.lower())):
            return self.fVoidPOHeader()

        unContentData = self.fZipFileElementContent( theZipFile, theFileName)
        if not unContentData:
            return self.fVoidPOHeader()
        
        return self.fPOHeaderFromPOContent( theParentExecutionRecord, unContentData)
            
     
    
    

    
    
    security.declarePrivate( 'fPOHeaderFromPOContent')    
    def fPOHeaderFromPOContent( self, theParentExecutionRecord ,theContent):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fPOHeaderFromPOContent', theParentExecutionRecord, False) 

        try:

            if not theContent:
                return None
            
            someLines = theContent.splitlines()
            
            unNumLines = len( someLines)
                    
            if unNumLines < 1:
                return None
    
            unPOHeader = self.fVoidPOHeader()
            unKeysFound = set()
            unKeysToFind = set( [ 'language_code', 'language_name', 'charset', 'country', 'is_fallback_for', 'domain',])
            unLineIndex = 0
            while unLineIndex < unNumLines:
                unaLine =  someLines[ unLineIndex].strip()
                unLineIndex += 1  
                if not unaLine or unaLine.startswith( cPOTranslationEntryDefaultPrefix) or unaLine.startswith( cPOTranslationEntrySourcesPrefix) or unaLine.startswith( cPOTranslationEntryModulesPrefix) or unaLine.startswith( cPOTranslationEntryStatusPrefix) or unaLine.startswith( cPOTranslationEntryFlagsPrefix):
                    break
                
                if unLineIndex >= cPOMaxLinesToScanTryingToGetHeader:
                    break
                    
                unaLineLower = unaLine.lower()
                
                
                
                
                if unaLineLower.startswith( cPOHeaderPrefix_LanguageCode.lower()):
                    unPOHeader[ 'last_line_number'] = unLineIndex
                    unLocaleLanguage = ''
                    unLocaleCountry = ''
                    unValue = unaLine[ len( cPOHeaderPrefix_LanguageCode):].replace( '\\n', '').strip()
                    unQuoteIndex = unValue.find( '"', 0)  
                    if unQuoteIndex >= 0:
                        unValue = unValue[:unQuoteIndex] 
                        if unValue:
                            unIndexCharBeforeCountry = unValue.find( cLanguageSeparatorCountry, 0)
                            if unIndexCharBeforeCountry >= 0:
                                unLocaleLanguage = unValue[ :unIndexCharBeforeCountry]   
                                unLocaleCountry  = unValue[  unIndexCharBeforeCountry + len( cLanguageSeparatorCountry):] 
                            else:
                                unLocaleLanguage = unValue
                                unLocaleCountry  = '' 
                              
                    if unLocaleLanguage:
                        unPOHeader[ 'language_code'] = unLocaleLanguage.lower()
                        unKeysFound.add( 'language_code')
                    if unLocaleCountry:
                        unPOHeader[ 'country']       = unLocaleCountry.lower()
                        unKeysFound.add( 'country')
                            
                        
                        
                        
                        
                elif unaLineLower.startswith( cPOHeaderPrefix_LanguageName.lower()):
                    unPOHeader[ 'last_line_number'] = unLineIndex
                    unValue = unaLine[ len( cPOHeaderPrefix_LanguageName):].replace( '\\n', '').strip()
                    unQuoteIndex = unValue.find( '"', 0)  
                    if unQuoteIndex >= 0:
                        unValue = unValue[:unQuoteIndex] 
                    if unValue:
                        unPOHeader[ 'language_name'] = unValue.lower()
                        unKeysFound.add( 'language_name')
                        
                        
                        
                        
                        
                elif unaLineLower.startswith( cPOHeaderPrefix_ContentType.lower()):
                    unPOHeader[ 'last_line_number'] = unLineIndex
                    unCharset = ''
                    unValue = unaLine[ len( cPOHeaderPrefix_ContentType):].replace( '\\n', '').strip()
                    unQuoteIndex = unValue.find( '"', 0)  
                    if unQuoteIndex >= 0:
                        unValue = unValue[:unQuoteIndex] 
                    if unValue:
                        unIndexCharBeforeCharset = unValue.find( cPOHeaderPrefix_Charset, 0)
                        if unIndexCharBeforeCharset >= 0:
                            unCharset = unValue[ unIndexCharBeforeCharset + len( cPOHeaderPrefix_Charset):]   
                    if unCharset:
                        unCharset = unCharset.lower()
                        unCharSetExists = True
                        try:
                            aVoid = ''.decode( unCharset )
                        except:
                            unCharSetExists = False
                            
                        if not unCharSetExists:
                            unCharset = 'utf-8'
                        
                        unPOHeader[ 'charset'] = unCharset
                        unKeysFound.add( 'charset')
                        
                        
                        
                        
                        
                elif unaLineLower.startswith( cPOHeaderPrefix_IsFallbackFor.lower()):
                    unPOHeader[ 'last_line_number'] = unLineIndex
                    unValue = unaLine[ len( cPOHeaderPrefix_IsFallbackFor):].replace( '\\n', '').strip()
                    unQuoteIndex = unValue.find( '"', 0)  
                    if unQuoteIndex >= 0:
                        unValue = unValue[:unQuoteIndex] 
                    if unValue:
                        unPOHeader[ 'is_fallback_for'] = unValue.lower()
                        unKeysFound.add( 'is_fallback_for')
                        
                        
                        
                        
                        
                elif unaLineLower.startswith( cPOHeaderPrefix_Domain.lower()):
                    unPOHeader[ 'last_line_number'] = unLineIndex
                    unValue = unaLine[ len( cPOHeaderPrefix_Domain):].replace( '\\n', '').strip()
                    unQuoteIndex = unValue.find( '"', 0)  
                    if unQuoteIndex>= 0:
                        unValue = unValue[:unQuoteIndex] 
                    if unValue:
                        unPOHeader[ 'domain'] = unValue
                        unKeysFound.add( 'domain')
                        
                        
                        
                        
                elif unaLine.startswith( cPOTranslationEntryMsgidPrefix) or unaLine.startswith( cPOTranslationEntryMsgstrPrefix): 
                    
                    continue
                
                
                
                
                if unKeysFound == unKeysToFind:
                    return unPOHeader
                    

            if not unKeysFound.intersection( set( [ 'language_code', 'language_name', 'charset', ])):
                return None
            
            return unPOHeader
       
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()


    
                
                
    

    
                    
                
      
             
      
        
            

    security.declarePrivate( 'pScanTranslationsPO')    
    def pScanTranslationsPO( self,
        theParentExecutionRecord =None, 
        theUploadedFile         =None, 
        theZipFile              =None, 
        theUploadedContent      =None,
        theUploadedEntry        =None,
        theAdditionalParams     =None):
        
        """Parse a complete GNU gettext PO file, and produce a data structure with all information read.
        
        """
                
        unExecutionRecord = self.fStartExecution( 'method',  'pScanTranslationsPO', theParentExecutionRecord, False) 

        try:
                
            if not theUploadedContent or not theUploadedEntry:
                return self
           
            unFileName = theUploadedEntry[ 'file_name']
            if not unFileName:
                return self
            
            
            # ########################################
            """Get additional Import parameters.
            
            """
            aNombreModuloConfigurado                =  theAdditionalParams.get( 'theDefaultModule',                  '') 
            aImportarConNombreModuloConfigurado     =  theAdditionalParams.get( 'theImportWithConfiguredModuleName', False) == True
            aImportarNombreModuloDesdeDominioONombreFichero =  theAdditionalParams.get( 'theImportModuleNameFromDomainOrFilename', None) == True
            aImportarNombresModulosDesdeComentarios =  theAdditionalParams.get( 'theImportModuleNamesFromComment',   False) == True
            aImportarContribucionesDesdeComentarios =  theAdditionalParams.get( 'theImportContributionsFromComment', False) == True
            aImportarFuentesDesdeComentarios        =  theAdditionalParams.get( 'theImportSourcesFromComment',       False) == True
            aImportarStatusDesdeComentarios         =  theAdditionalParams.get( 'theImportStatusFromComment',        False) == True
            aNumeroMaximoLineasAExplorarString      =  theAdditionalParams.get( 'theMaxLinesToScan',                 '-1')
            aNumeroMaximoLineasAExplorar = -1
            try:
                aNumeroMaximoLineasAExplorar = int( aNumeroMaximoLineasAExplorarString)
            except:
                None

            
            
            # ###############################################################
            """Result Data structure.

            """            
            aScannedData = theUploadedContent.get( 'content_data', None)
            if aScannedData == None:
                aScannedData = self.fNewVoidScannedData()
                theUploadedContent[ 'content_data'] = aScannedData 
           
            
            
            # ###############################################################
            """Language for new scanned string translations supplied by caller (possibly taken from the GNUgettextPO file header, the file name, or from the containing archive's manifest.mf or locales.csv file")

            """
            unCodigoIdioma = theUploadedEntry[ 'language_and_country']
            if not unCodigoIdioma:
                return self
            
            if not unCodigoIdioma in aScannedData[ 'languages']:
                aScannedData[ 'languages'].append( unCodigoIdioma)
            
                
 
            unModuleImposedIndex = -1
            
            if aImportarConNombreModuloConfigurado:
                # ###############################################################
                """Use a module name supplied by caller  for the strings read.
    
                """
                if aNombreModuloConfigurado:
                    unModuleImposedIndex = -1
                    try:
                        unModuleImposedIndex = aScannedData[ 'modules'].index( aNombreModuloConfigurado)
                    except:
                        None
                    if unModuleImposedIndex < 0:
                        aScannedData[ 'modules'].append( aNombreModuloConfigurado)
                        unModuleImposedIndex = len(  aScannedData[ 'modules']) - 1
                
                
                
                        
            if aImportarNombreModuloDesdeDominioONombreFichero:
                # ###############################################################
                """Use a module name taken from the GNUgettextPO file header or the file name for the strings read.
    
                """
                unModuleFromUploadedContent = theUploadedEntry[ 'module']
                if unModuleFromUploadedContent:
                    
                    unModuleImposedIndex = -1
                    try:
                        unModuleImposedIndex = aScannedData[ 'modules'].index( unModuleFromUploadedContent)
                    except:
                        None
                    if unModuleImposedIndex < 0:
                        aScannedData[ 'modules'].append( unModuleFromUploadedContent)
                        unModuleImposedIndex = len(  aScannedData[ 'modules']) - 1
                
                    
                    
                    
                
            # ###############################################################
            """Read the text to parse, from a Zip archive, or a text file.

            """            
            unInZip = theUploadedEntry.get( 'in_zip', False)
            
            if unInZip:
                
                unContentData = None
                try:
                    if theZipFile:
                        unContentData = theZipFile.read( unFileName)
                except:
                    None
                if not unContentData:
                    return self
                
                unFicheroImportCursor = self.fFicheroImportCursorPO( theUploadedEntry, unContentData, aNumeroMaximoLineasAExplorar)
                if unFicheroImportCursor:
                    
                    if unFicheroImportCursor.get( 'exceeded_max_number_of_lines', False):
                        theUploadedEntry[ 'exceeded_max_number_of_lines'] = True
                        
            else:
                
                theUploadedFile.seek( 0)
                unContentData = theUploadedFile.read()
                if not unContentData:
                    return self
                
                unFicheroImportCursor = self.fFicheroImportCursorPO( theUploadedEntry, unContentData, aNumeroMaximoLineasAExplorar)
                if unFicheroImportCursor:
                    
                    if unFicheroImportCursor.get( 'exceeded_max_number_of_lines', False):
                        theUploadedEntry[ 'exceeded_max_number_of_lines'] = True
          
                        
                        
            
            # ###############################################################
            """Init file cursor with the language, and with the charset to be used to decode the file contents.

            """            
            unFicheroImportCursor[ 'language'] = unCodigoIdioma
            unFicheroImportCursor[ 'charset']  = theUploadedEntry[ 'charset']
            
            
            
                        
            # ###############################################################
            """Discard erroneus or empty files.

            """            
            if not ( unFicheroImportCursor and unFicheroImportCursor[ 'num_lines']):
                return self
            
            

            

            
            
            # ###############################################################
            """Determine whether the file is a template file, in which case the translations shall be taken from the Default translator comment, if any available in the data read.

            """            
            unEsPOTfile = theUploadedEntry[ 'is_pot_file']
            
            
            
            # ###############################################################
            """Iterate over .PO data.

            """            
            unCursorRecord = self.fNextCursorRecordPO( unFicheroImportCursor)
            
            while unCursorRecord:
                
                unSyntaxError            = unCursorRecord[ 'syntax_error']   
                unSyntaxErrorRecoverable = unCursorRecord[ 'syntax_error_recoverable']   
                unSymbolEncoded          = unCursorRecord[ 'symbol_encoded']
                unEmptySymbol            = unCursorRecord[ 'empty_symbol']
                unSymbolError            = unCursorRecord[ 'symbol_error']   

                
                
                if unSyntaxError:
                    # ###############################################################
                    """There is a syntax structure error on the file.
        
                    """            
                    if not unSyntaxErrorRecoverable:
                        break
                 
                    else:
                        pass
                    
                    
                    
                elif unEmptySymbol:
                    # ###############################################################
                    """An entry without symbol, as always happens with the GNU gettext PO file header.
        
                    """            
                    pass
                
                
                
                elif unSymbolError or not unSymbolEncoded:
                    # ###############################################################
                    """Count string symbol errors.
        
                    """            
                    aScannedData[ 'num_symbol_errors'] += 1
                           
                    

                else:
                    
                    # ###############################################################
                    """Look-up already existing data for string symbol just read, or create a new one and append to data read.
        
                    """            
                    aScannedString = aScannedData[ 'symbols_dict'].get( unSymbolEncoded, None)
                    
                    if aScannedString == None:
                        
                        aScannedString = self.fNewVoidScannedString()
                        aScannedString[ cScannedKeys_String_Symbol] = unSymbolEncoded
                        
                        aScannedData[ 'symbols'].append( aScannedString)
                        aScannedData[ 'symbols_dict'][ unSymbolEncoded] = aScannedString
                    
                    
                    
                        
                    # ###############################################################
                    """Add to string data the module imposed from the caller.
        
                    """                                    
                    if unModuleImposedIndex >= 0:
                        
                        someScannedModules = aScannedString.get( cScannedKeys_String_Modules, None)
                        
                        if someScannedModules == None:
                            someScannedModules = set()
                            aScannedString[ cScannedKeys_String_Modules] = someScannedModules
                            
                        someScannedModules.add( unModuleImposedIndex)
                    
                        
                        
                        
                    if aImportarNombresModulosDesdeComentarios:   
                        # ###############################################################
                        """Add to string data the indexes of the module names just read.
            
                        """                     
                        if unCursorRecord.get( 'modules_error', False):
                            # ###############################################################
                            """Record string modules error.
                
                            """                                    
                            someScannedStringErrors = aScannedString.get( cScannedKeys_String_Errors, None)
                            if someScannedStringErrors == None:
                                someScannedStringErrors = [ cScanError_String_Modules,]
                                aScannedString[ cScannedKeys_String_Errors] = someScannedStringErrors
                            else:
                                if not ( cScanError_String_Modules in someScannedStringErrors):
                                    someScannedStringErrors.append( cScanError_String_Modules)
                                                            
                        else:
                            unModuleNamesString = unCursorRecord.get( 'modules_encoded', '')
                            if unModuleNamesString:
                                
                                unosModuleNames = self.fParseNombresModulosString( unModuleNamesString)
                                if unosModuleNames:
    
                                    someScannedModules = aScannedString.get( cScannedKeys_String_Modules, None)
                                    
                                    if someScannedModules == None:
                                        someScannedModules = set()
                                        aScannedString[ cScannedKeys_String_Modules] = someScannedModules
                                        
                                    for unModuleName in unosModuleNames:
                                        
                                        aModuleIndex = -1
                                        try:
                                            aModuleIndex = aScannedData[ 'modules'].index( unModuleName)
                                        except:
                                            None
                                            
                                        if aModuleIndex >= 0:
                                            someScannedModules.add( aModuleIndex)
    
                                        else:
                                            aScannedData[ 'modules'].append( unModuleName)
                                            aModuleIndex = len(  aScannedData[ 'modules']) - 1
                                       
                                            someScannedModules.add( aModuleIndex)

                            
                                    
                    if aImportarFuentesDesdeComentarios:                                            
                        # ###############################################################
                        """Add to string data the sources just read.
            
                        """                                                                        
                        if unCursorRecord.get( 'sources_error', False):
                            # ###############################################################
                            """Record string sources error.
                
                            """                                    
                            someScannedStringErrors = aScannedString.get( cScannedKeys_String_Errors, None)
                            if someScannedStringErrors == None:
                                someScannedStringErrors = [ cScanError_String_Sources,]
                                aScannedString[ cScannedKeys_String_Errors] = someScannedStringErrors
                            else:
                                if not ( cScanError_String_Sources in someScannedStringErrors):
                                    someScannedStringErrors.append( cScanError_String_Sources)
                                
                        else:
                            unSourcesString = unCursorRecord.get( 'sources_encoded', '')
                            if unSourcesString:
                                
                                unaStringSources = aScannedString.get( cScannedKeys_String_Sources, None)
                                if not unaStringSources:
                                    aScannedString[ cScannedKeys_String_Sources] = [ unSourcesString, ]
                                else:
                                    if not unSourcesString in unaStringSources:
                                        unaStringSources.append( unSourcesString)

                                    
                                    

                                
                    # ###############################################################
                    """Create a new translation data to hold the translation just read, and add it to the string data
        
                    """            
                    aScannedTranslation = self.fNewVoidScannedTranslation()                    
                    aScannedString[ cScannedKeys_String_Translations][ unCodigoIdioma] = aScannedTranslation
                                    
                    
                               
                    
                    # ###############################################################
                    """For .POT (translation template) file, the translation, if any, is taken from the line with Default user comment.
        
                    """            
                    if unEsPOTfile:
                        unTranslationEncoded = unCursorRecord[ 'default_encoded']
                        unTranslationError   = unCursorRecord[ 'default_error']
                        
                    else:
                        unTranslationEncoded = unCursorRecord[ 'translation_encoded']
                        unTranslationError   = unCursorRecord[ 'translation_error']
                                    
                                    
                        
                        
                    # ###############################################################
                    """Add to translation data the translation just read.
        
                    """                                                                        
                    if unTranslationError:
                        # ###############################################################
                        """Record translation error.
            
                        """                                    
                        someScannedTranslationErrors = aScannedTranslation.get( cScannedKeys_Translation_Errors, None)
                        if someScannedTranslationErrors == None:
                            someScannedTranslationErrors = [ cScanError_Translation_Translation,]
                            aScannedTranslation[ cScannedKeys_Translation_Errors] = someScannedTranslationErrors
                        else:
                            if not ( cScanError_Translation_Translation in someScannedTranslationErrors):
                                someScannedTranslationErrors.append( cScanError_Translation_Translation)
                            
                    else:
                        
                        if unTranslationEncoded:
                            
                            aScannedTranslation[ cScannedKeys_Translation_Translation] = unTranslationEncoded
                    
                        
                        
                                
                    if aImportarStatusDesdeComentarios:
                        # ###############################################################
                        """Set translation data to the status just read.
            
                        """                                                                        
                        if unCursorRecord.get( 'status_error', False):
                            # ###############################################################
                            """Record translation status error.
                
                            """                                    
                            someScannedTranslationErrors = aScannedTranslation.get( cScannedKeys_Translation_Errors, None)
                            if someScannedTranslationErrors == None:
                                someScannedTranslationErrors = [ cScanError_Translation_Status,]
                                aScannedTranslation[ cScannedKeys_Translation_Errors] = someScannedTranslationErrors
                            else:
                                if not ( cScanError_Translation_Status in someScannedTranslationErrors):
                                    someScannedTranslationErrors.append( cScanError_Translation_Status)
                            
                        else:
                            unStatusString = unCursorRecord.get( 'status_encoded', '')
                            if unStatusString:
                                                                
                                if unStatusString in [ cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva,]:
                                    
                                    aStatusIndex = [ cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva,].index( unStatusString) + 2
                                    aScannedTranslation[ cScannedKeys_Translation_Status] = aStatusIndex
                                                      

                                

                                    
                                    
                                    
                    if aImportarContribucionesDesdeComentarios:
                        # ###############################################################
                        """Set translation data to the dates and user names that created, translated, reviewed or marked as definitive just read.
            
                        """       
                        
                        if unCursorRecord.get( 'creation_date_error', False):
                            # ###############################################################
                            """Record translation creation_date error.
                
                            """                                    
                            someScannedTranslationErrors = aScannedTranslation.get( cScannedKeys_Translation_Errors, None)
                            if someScannedTranslationErrors == None:
                                someScannedTranslationErrors = [ cScanError_Translation_CreationDate,]
                                aScannedTranslation[ cScannedKeys_Translation_Errors] = someScannedTranslationErrors
                            else:
                                if not ( cScanError_Translation_CreationDate in someScannedTranslationErrors):
                                    someScannedTranslationErrors.append( cScanError_Translation_CreationDate)
                            
                        else:
                            unCreationDateString = unCursorRecord.get( 'creation_date_encoded', '')
                            if unCreationDateString:
                                    
                                unCreationDate = None
                                try:
                                    unCreationDate = DateTime( unCreationDateString)
                                except:
                                    None
                                    
                                if unCreationDate:
                                    unCreationDateStoreString = self.fDateToStoreString( unCreationDate)
                                    
                                    if unCreationDateStoreString:
                                        aScannedTranslation[ cScannedKeys_Translation_CreationDate] = unCreationDateStoreString
                        
                                

                                        
                        if unCursorRecord.get( 'creator_error', False):
                            # ###############################################################
                            """Record translation creator error.
                
                            """                                    
                            someScannedTranslationErrors = aScannedTranslation.get( cScannedKeys_Translation_Errors, None)
                            if someScannedTranslationErrors == None:
                                someScannedTranslationErrors = [ cScanError_Translation_Creator,]
                                aScannedTranslation[ cScannedKeys_Translation_Errors] = someScannedTranslationErrors
                            else:
                                if not ( cScanError_Translation_Creator in someScannedTranslationErrors):
                                    someScannedTranslationErrors.append( cScanError_Translation_Creator)
                            
                        else:
                            unCreatorString = unCursorRecord.get( 'creator_encoded', '')
                            if unCreatorString:
                                aScannedTranslation[ cScannedKeys_Translation_Creator] = unCreatorString
                        
                                
                                         
                                        

                        if unCursorRecord.get( 'translation_date_error', False):
                            # ###############################################################
                            """Record translation translation_date error.
                
                            """                                    
                            someScannedTranslationErrors = aScannedTranslation.get( cScannedKeys_Translation_Errors, None)
                            if someScannedTranslationErrors == None:
                                someScannedTranslationErrors = [ cScanError_Translation_TranslationDate,]
                                aScannedTranslation[ cScannedKeys_Translation_Errors] = someScannedTranslationErrors
                            else:
                                if not ( cScanError_Translation_TranslationDate in someScannedTranslationErrors):
                                    someScannedTranslationErrors.append( cScanError_Translation_TranslationDate)
                            
                        else:
                            unTranslationDateString = unCursorRecord.get( 'translation_date_encoded', '')
                            if unTranslationDateString:
                                    
                                unTranslationDate = None
                                try:
                                    unTranslationDate = DateTime( unTranslationDateString)
                                except:
                                    None
                                    
                                if unTranslationDate:
                                    unTranslationDateStoreString = self.fDateToStoreString( unTranslationDate)
                                    
                                    if unTranslationDateStoreString:
                                        aScannedTranslation[ cScannedKeys_Translation_TranslationDate] = unTranslationDateStoreString
                        
                                        
                                

                        if unCursorRecord.get( 'translator_error', False):
                            # ###############################################################
                            """Record translation translator error.
                
                            """                                    
                            someScannedTranslationErrors = aScannedTranslation.get( cScannedKeys_Translation_Errors, None)
                            if someScannedTranslationErrors == None:
                                someScannedTranslationErrors = [ cScanError_Translation_Translator,]
                                aScannedTranslation[ cScannedKeys_Translation_Errors] = someScannedTranslationErrors
                            else:
                                if not ( cScanError_Translation_Translator in someScannedTranslationErrors):
                                    someScannedTranslationErrors.append( cScanError_Translation_Translator)
                            
                        else:
                            unTranslatorString = unCursorRecord.get( 'translator_encoded', '')
                            if unTranslatorString:
                                aScannedTranslation[ cScannedKeys_Translation_Translator] = unTranslatorString
                        
                                
                                                                             
                                
                        
                        if unCursorRecord.get( 'review_date_error', False):
                            # ###############################################################
                            """Record translation review_date error.
                
                            """                                    
                            someScannedTranslationErrors = aScannedTranslation.get( cScannedKeys_Translation_Errors, None)
                            if someScannedTranslationErrors == None:
                                someScannedTranslationErrors = [ cScanError_Translation_ReviewDate,]
                                aScannedTranslation[ cScannedKeys_Translation_Errors] = someScannedTranslationErrors
                            else:
                                if not ( cScanError_Translation_ReviewDate in someScannedTranslationErrors):
                                    someScannedTranslationErrors.append( cScanError_Translation_ReviewDate)
                            
                        else:
                            unReviewDateString = unCursorRecord.get( 'review_date_encoded', '')
                            if unReviewDateString:
                                    
                                unReviewDate = None
                                try:
                                    unReviewDate = DateTime( unReviewDateString)
                                except:
                                    None
                                    
                                if unReviewDate:
                                    unReviewDateStoreString = self.fDateToStoreString( unReviewDate)
                                    
                                    if unReviewDateStoreString:
                                        aScannedTranslation[ cScannedKeys_Translation_ReviewDate] = unReviewDateStoreString
                        
                                                                       
                                

                        if unCursorRecord.get( 'reviewer_error', False):
                            # ###############################################################
                            """Record translation reviewer error.
                
                            """                                    
                            someScannedTranslationErrors = aScannedTranslation.get( cScannedKeys_Translation_Errors, None)
                            if someScannedTranslationErrors == None:
                                someScannedTranslationErrors = [ cScanError_Translation_Reviewer,]
                                aScannedTranslation[ cScannedKeys_Translation_Errors] = someScannedTranslationErrors
                            else:
                                if not ( cScanError_Translation_Reviewer in someScannedTranslationErrors):
                                    someScannedTranslationErrors.append( cScanError_Translation_Reviewer)
                            
                        else:
                            unReviewerString = unCursorRecord.get( 'reviewer_encoded', '')
                            if unReviewerString:
                                aScannedTranslation[ cScannedKeys_Translation_Reviewer] = unReviewerString
                        
                                
                                 
                                
                        
                        if unCursorRecord.get( 'definitive_date_error', False):
                            # ###############################################################
                            """Record translation definitive_date error.
                
                            """                                    
                            someScannedTranslationErrors = aScannedTranslation.get( cScannedKeys_Translation_Errors, None)
                            if someScannedTranslationErrors == None:
                                someScannedTranslationErrors = [ cScanError_Translation_DefinitiveDate,]
                                aScannedTranslation[ cScannedKeys_Translation_Errors] = someScannedTranslationErrors
                            else:
                                if not ( cScanError_Translation_DefinitiveDate in someScannedTranslationErrors):
                                    someScannedTranslationErrors.append( cScanError_Translation_DefinitiveDate)
                            
                        else:
                            unDefinitiveDateString = unCursorRecord.get( 'definitive_date_encoded', '')
                            if unDefinitiveDateString:
                                    
                                unDefinitiveDate = None
                                try:
                                    unDefinitiveDate = DateTime( unDefinitiveDateString)
                                except:
                                    None
                                    
                                if unDefinitiveDate:
                                    unDefinitiveDateStoreString = self.fDateToStoreString( unDefinitiveDate)
                                    
                                    if unDefinitiveDateStoreString:
                                        aScannedTranslation[ cScannedKeys_Translation_DefinitiveDate] = unDefinitiveDateStoreString
                        
                                        
                                        
                                

                        if unCursorRecord.get( 'coordinator_error', False):
                            # ###############################################################
                            """Record translation coordinator error.
                
                            """                                    
                            someScannedTranslationErrors = aScannedTranslation.get( cScannedKeys_Translation_Errors, None)
                            if someScannedTranslationErrors == None:
                                someScannedTranslationErrors = [ cScanError_Translation_Coordinator,]
                                aScannedTranslation[ cScannedKeys_Translation_Errors] = someScannedTranslationErrors
                            else:
                                if not ( cScanError_Translation_Coordinator in someScannedTranslationErrors):
                                    someScannedTranslationErrors.append( cScanError_Translation_Coordinator)
                            
                        else:
                            unCoordinatorString = unCursorRecord.get( 'coordinator_encoded', '')
                            if unCoordinatorString:
                                aScannedTranslation[ cScannedKeys_Translation_Coordinator] = unCoordinatorString
                        
                                
                                                                          
                                    
                                
                                    
                    # ###############################################################
                    """Add to translation data the flags just read.
        
                    """                                                                        
                    if unCursorRecord.get( 'flags_error', False):
                        # ###############################################################
                        """Record translation flags error.
            
                        """                                    
                        someScannedTranslationErrors = aScannedTranslation.get( cScannedKeys_Translation_Errors, None)
                        if someScannedTranslationErrors == None:
                            someScannedTranslationErrors = [ cScanError_Translation_Flags,]
                            aScannedTranslation[ cScannedKeys_Translation_Errors] = someScannedTranslationErrors
                        else:
                            if not ( cScanError_Translation_Flags in someScannedTranslationErrors):
                                someScannedTranslationErrors.append( cScanError_Translation_Flags)
                        
                    else:
                        unFlagsString = unCursorRecord.get( 'flags_encoded', '')
                        if unFlagsString:
                            
                            unaTranslationFlags = aScannedString.get( cScannedKeys_Translation_Flags, None)
                            if not unaTranslationFlags:
                                aScannedTranslation[ cScannedKeys_Translation_Flags] = unFlagsString
                            else:
                                aScannedTranslation[ cScannedKeys_Translation_Flags] = '%s %s' ( unaTranslationFlags, unFlagsString, )
                                
                                                  
                                
                                 
                                
                        
                    # ###############################################################
                    """Add to translation data the comment just read.
        
                    """                                                                        
                    if unCursorRecord.get( 'comment_error', False):
                        # ###############################################################
                        """Record translation comment error.
            
                        """                                    
                        someScannedTranslationErrors = aScannedTranslation.get( cScannedKeys_Translation_Errors, None)
                        if someScannedTranslationErrors == None:
                            someScannedTranslationErrors = [ cScanError_Translation_Comment,]
                            aScannedTranslation[ cScannedKeys_Translation_Errors] = someScannedTranslationErrors
                        else:
                            if not ( cScanError_Translation_Comment in someScannedTranslationErrors):
                                someScannedTranslationErrors.append( cScanError_Translation_Comment)
                            
                    else:                        
                        unCommentString = unCursorRecord.get( 'comment_encoded', '')
                        if unCommentString:
                            
                            unaTranslationComment = aScannedTranslation.get( cScannedKeys_Translation_Comment, None)
                            if not unaTranslationComment:
                                aScannedTranslation[ cScannedKeys_Translation_Comment] = unCommentString
                            else:
                                aScannedTranslation[ cScannedKeys_Translation_Comment] = '%s %s' ( unaTranslationComment, unCommentString, )
                                
                                            
                                
                                
                            
                unCursorRecord = self.fNextCursorRecordPO( unFicheroImportCursor)
                 
                
            # ###############################################################
            """ Convert sets to list and  Remove redundant dictionary of strings read by string symbol,to reduce the lenght of the string representation of the scanned structure that shall be persisted in a field in a TRAContenidoElemento instance.

            """                                                                        
            aScannedData.pop( 'symbols_dict')
            
            for aScannedString in aScannedData[ 'symbols']:
                
                someModules = aScannedString.get( cScannedKeys_String_Modules, None)
                if not ( someModules == None):
                    if not someModules:
                        aScannedString.pop( cScannedKeys_String_Modules)
                    else:
                        aScannedString[ cScannedKeys_String_Modules] = list( someModules)
                            
                
            return self
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

                                           
                
            
            
            
            
   
    
    security.declarePrivate( 'fFicheroImportCursorPO')    
    def fFicheroImportCursorPO( self, theUploadedEntry, theContent, theMaxNumLinesToExplore):
        if not theContent:
            return None
        
        unCursor = self.fNewVoidImportCursor()
        unCursor[ 'file_kind'] = cPOFilePostfix
        
        aTranslationService = self.getTranslationServiceTool()
        unCursor[ 'translation_service'] = aTranslationService
 
        someLines = theContent.splitlines()
        unCursor[ 'content_lines']  = someLines
        
        unNumLines = len( someLines)
       
        unCursor[ 'max_number_of_lines'] = theMaxNumLinesToExplore
        
        if theMaxNumLinesToExplore >= 0:
            if unNumLines > theMaxNumLinesToExplore:
                unNumLines = theMaxNumLinesToExplore + cPOMaxLinesToScanTryingToGetCadena
                unCursor[ 'content_lines']  = someLines[:theMaxNumLinesToExplore]
                unCursor[ 'exceeded_max_number_of_lines'] = True
 
        unCursor[ 'num_lines']      = unNumLines
        unCursor[ 'next_line_index'] = 0
                
        if unNumLines < 1:
            unCursor[ 'error'] = "gvSIGi18n_NoContentLines_error_msgid"
            unCursor[ 'error_detail'] = theFileName                    
            return None

        # ACV 20101010 Scan also the PO header, which shall be ignored because it returns a cursor record with empty_symbol
        #unLastHeaderLineIndex = theUploadedEntry.get( 'last_header_line_number', -1)
        #unCursor[ 'next_line_index'] = unLastHeaderLineIndex
        unCursor[ 'next_line_index'] = 0
               
        unCursor[ 'num_possible_records'] = unNumLines / 2
        
        if unCursor[ 'next_line_index'] >= unCursor[ 'num_lines']:
            return None
        
        return unCursor
           

    
    
    
    
    
    
   
    security.declarePrivate( 'fNextCursorRecordPO')    
    def fNextCursorRecordPO( self, theCursor):
        """Return a cursor record for the next .PO entry, including - if present - module names, status, sources and flags. 
        
        """
        if not theCursor:
            return None
        
        if not theCursor[ 'file_kind'] == cPOFilePostfix:
            return None
        
        
        
        # ##############################################################
        """Obtain translation service and encoding to decode strings read from file.
        
        """
        aTranslationService = theCursor[ 'translation_service']
        if not aTranslationService:
            return None
        
        unImportedCharSet = theCursor[ 'charset']
        if not unImportedCharSet:
            unImportedCharSet = cTRAEncodingUTF8

            
        unMaxNumeroLineas = theCursor[ 'max_number_of_lines']
        
        unosDatosCadenaActual = None
        
        unNumeroLineasIntentadas = 0

        
        # ##############################################################
        """Loop to scan all lines.
        
        """
        while True:
            
            unNextLineIndex = theCursor[ 'next_line_index']
            
            unNumeroLineasIntentadas += 1
            
            # ##############################################################
            """Check for end of content or maximum of lines to explore.
            
            """
            if ( unNextLineIndex >= theCursor[ 'num_lines']) or ( ( unMaxNumeroLineas > 0) and ( unNextLineIndex >= unMaxNumeroLineas)) or ( unNumeroLineasIntentadas >= cPOMaxLinesToScanTryingToGetCadena):
                
                return unosDatosCadenaActual
                    
                    
            
                    
                    
            # ##############################################################
            """Advance cursor for next iteration or end of exploration.
            
            """
            theCursor[ 'next_line_index'] += 1
            
            
            
            
            
            # ##############################################################
            """Retrieve line to parse.
            
            """
            unaLinea = theCursor[ 'content_lines'][ unNextLineIndex].strip()
            
            
            
            
            
            # ##############################################################
            """When a blank line, return any string data already parsed, or continue scanning lines
            
            """
            if not unaLinea:
                
                if unosDatosCadenaActual:
                    return unosDatosCadenaActual
                
                else:
                    
                    continue
           
                    
                    
            # ##############################################################
            """Parse line according to the characters at the start of the line.
            
            """            
            if unaLinea.startswith( cPOTranslationEntryDefaultPrefix):
                
                if not unosDatosCadenaActual:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                    
                unosDatosCadenaActual[ 'continuable_translation']   = False
                    
                unDefaultString = unaLinea[ len( cPOTranslationEntryDefaultPrefix):]
                unDefaultString = unDefaultString.replace( '"', '').strip()
                
                if unDefaultString:
                    
                    unosDatosCadenaActual[ 'default_raw'] = unDefaultString
                    
                    unDefaultUnicode = u''
                    try:
                        unDefaultUnicode = unDefaultString.decode( unImportedCharSet)
                    except UnicodeDecodeError:
                        unosDatosCadenaActual[ 'default_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .PO' % unImportedCharSet  
                    
                    if unDefaultUnicode:
                        unosDatosCadenaActual[ 'default_unicode'] = unDefaultUnicode
                        unDefaultEncoded  = ''
                        try:
                            unDefaultEncoded =  aTranslationService.encode( unDefaultUnicode)      
                        except:
                            unosDatosCadenaActual[ 'default_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .PO'   
                        
                        if unDefaultEncoded:    
                            unosDatosCadenaActual[ 'default_encoded'] = unDefaultEncoded
                continue   
            
            
            
            
            elif unaLinea.startswith( cPOTranslationEntryModulesPrefix):
                                
                if not unosDatosCadenaActual:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()

                unosDatosCadenaActual[ 'continuable_translation']   = False
                    
                unosModulesString = unaLinea[ len( cPOTranslationEntryModulesPrefix):]
                unosModulesString = unosModulesString.replace( '"', '').strip()
                
                if unosModulesString:
                    
                    unosDatosCadenaActual[ 'modules_raw'] = unosModulesString
                    
                    unModulesStringUnicode = u''
                    try:
                        unModulesStringUnicode = unosModulesString.decode( unImportedCharSet )
                    except UnicodeDecodeError:
                        unosDatosCadenaActual[ 'modules_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .PO' % unImportedCharSet   
                    
                    if unModulesStringUnicode:

                        unosDatosCadenaActual[ 'modules_unicode'] = unModulesStringUnicode
                        unModulesStringEncoded  = ''
                        try:
                            unModulesStringEncoded =  aTranslationService.encode( unModulesStringUnicode)      
                        except:
                            unosDatosCadenaActual[ 'modules_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .PO'   
       
                        if unModulesStringEncoded:    
                            unosDatosCadenaActual[ 'modules_encoded'] = unModulesStringEncoded
                    
                continue    
            
            
            
            
            elif unaLinea.startswith( cPOTranslationEntryStatusPrefix):
                                
                if not unosDatosCadenaActual:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                        
                unosDatosCadenaActual[ 'continuable_translation']   = False
                    
                unStatusString = unaLinea[ len( cPOTranslationEntryStatusPrefix):]
                unStatusString = unStatusString.replace( '"', '').strip()
                
                if unStatusString:
                    
                    unosDatosCadenaActual[ 'status_raw'] = unStatusString
                    
                    unStatusStringUnicode = u''
                    try:
                        unStatusStringUnicode = unStatusString.decode( unImportedCharSet )
                    except UnicodeDecodeError:
                        unosDatosCadenaActual[ 'status_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .PO' % unImportedCharSet   
                    
                    if unStatusStringUnicode:

                        unosDatosCadenaActual[ 'status_unicode'] = unStatusStringUnicode
                        unStatusStringEncoded  = ''
                        try:
                            unStatusStringEncoded =  aTranslationService.encode( unStatusStringUnicode)      
                        except:
                            unosDatosCadenaActual[ 'status_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .PO'   
       
                        if unStatusStringEncoded:    
                            unosDatosCadenaActual[ 'status_encoded'] = unStatusStringEncoded
                    
                continue    
            
            
            
            
            
            
            elif unaLinea.startswith( cPOTranslationEntryCreationDatePrefix):
                
                if not unosDatosCadenaActual:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                        
                unosDatosCadenaActual[ 'continuable_translation']   = False
                    
                unCreationDateString = unaLinea[ len( cPOTranslationEntryCreationDatePrefix):]
                unCreationDateString = unCreationDateString.replace( '"', '').strip()
                
                if unCreationDateString:
                    
                    unosDatosCadenaActual[ 'creation_date_raw'] = unCreationDateString
                    
                    unCreationDateStringUnicode = u''
                    try:
                        unCreationDateStringUnicode = unCreationDateString.decode( unImportedCharSet )
                    except UnicodeDecodeError:
                        unosDatosCadenaActual[ 'creation_date_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .PO' % unImportedCharSet   
                    
                    if unCreationDateStringUnicode:

                        unosDatosCadenaActual[ 'creation_date_unicode'] = unCreationDateStringUnicode
                        unCreationDateStringEncoded  = ''
                        try:
                            unCreationDateStringEncoded =  aTranslationService.encode( unCreationDateStringUnicode)      
                        except:
                            unosDatosCadenaActual[ 'creation_date_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .PO'   
       
                        if unCreationDateStringEncoded:    
                            unosDatosCadenaActual[ 'creation_date_encoded'] = unCreationDateStringEncoded
                continue    
            
            
           
            
            elif unaLinea.startswith( cPOTranslationEntryCreatorPrefix):
                
                if not unosDatosCadenaActual:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                        
                unosDatosCadenaActual[ 'continuable_translation']   = False
                    
                unCreatorString = unaLinea[ len( cPOTranslationEntryCreatorPrefix):]
                unCreatorString = unCreatorString.replace( '"', '').strip()
                
                if unCreatorString:
                    
                    unosDatosCadenaActual[ 'creator_raw'] = unCreatorString
                    
                    unCreatorStringUnicode = u''
                    try:
                        unCreatorStringUnicode = unCreatorString.decode( unImportedCharSet )
                    except UnicodeDecodeError:
                        unosDatosCadenaActual[ 'creator_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .PO' % unImportedCharSet   
                    
                    if unCreatorStringUnicode:

                        unosDatosCadenaActual[ 'creator_unicode'] = unCreatorStringUnicode
                        unCreatorStringEncoded  = ''
                        try:
                            unCreatorStringEncoded =  aTranslationService.encode( unCreatorStringUnicode)      
                        except:
                            unosDatosCadenaActual[ 'creator_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .PO'   
       
                        if unCreatorStringEncoded:    
                            unosDatosCadenaActual[ 'creator_encoded'] = unCreatorStringEncoded
                continue    
            
            
            
            
            
            elif unaLinea.startswith( cPOTranslationEntryTranslationDatePrefix):
                
                if not unosDatosCadenaActual:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                        
                unosDatosCadenaActual[ 'continuable_translation']   = False
                    
                unTranslationDateString = unaLinea[ len( cPOTranslationEntryTranslationDatePrefix):]
                unTranslationDateString = unTranslationDateString.replace( '"', '').strip()
                
                if unTranslationDateString:
                    
                    unosDatosCadenaActual[ 'translation_date_raw'] = unTranslationDateString
                    
                    unTranslationDateStringUnicode = u''
                    try:
                        unTranslationDateStringUnicode = unTranslationDateString.decode( unImportedCharSet )
                    except UnicodeDecodeError:
                        unosDatosCadenaActual[ 'translation_date_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .PO' % unImportedCharSet   
                    
                    if unTranslationDateStringUnicode:

                        unosDatosCadenaActual[ 'translation_date_unicode'] = unTranslationDateStringUnicode
                        unTranslationDateStringEncoded  = ''
                        try:
                            unTranslationDateStringEncoded =  aTranslationService.encode( unTranslationDateStringUnicode)      
                        except:
                            unosDatosCadenaActual[ 'translation_date_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .PO'   
       
                        if unTranslationDateStringEncoded:    
                            unosDatosCadenaActual[ 'translation_date_encoded'] = unTranslationDateStringEncoded
                continue    
            
            
            
 
            
            elif unaLinea.startswith( cPOTranslationEntryTranslatorPrefix):
                
                if not unosDatosCadenaActual:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                        
                unosDatosCadenaActual[ 'continuable_translation']   = False
                    
                unTranslatorString = unaLinea[ len( cPOTranslationEntryTranslatorPrefix):]
                unTranslatorString = unTranslatorString.replace( '"', '').strip()
                
                if unTranslatorString:
                    
                    unosDatosCadenaActual[ 'translator_raw'] = unTranslatorString
                    
                    unTranslatorStringUnicode = u''
                    try:
                        unTranslatorStringUnicode = unTranslatorString.decode( unImportedCharSet )
                    except UnicodeDecodeError:
                        unosDatosCadenaActual[ 'translator_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .PO' % unImportedCharSet   
                    
                    if unTranslatorStringUnicode:

                        unosDatosCadenaActual[ 'translator_unicode'] = unTranslatorStringUnicode
                        unTranslatorStringEncoded  = ''
                        try:
                            unTranslatorStringEncoded =  aTranslationService.encode( unTranslatorStringUnicode)      
                        except:
                            unosDatosCadenaActual[ 'translator_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .PO'   
       
                        if unTranslatorStringEncoded:    
                            unosDatosCadenaActual[ 'translator_encoded'] = unTranslatorStringEncoded
                continue    
            
                        
            
            elif unaLinea.startswith( cPOTranslationEntryReviewDatePrefix):
                
                if not unosDatosCadenaActual:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                        
                unosDatosCadenaActual[ 'continuable_translation']   = False
                    
                unReviewDateString = unaLinea[ len( cPOTranslationEntryReviewDatePrefix):]
                unReviewDateString = unReviewDateString.replace( '"', '').strip()
                
                if unReviewDateString:
                    
                    unosDatosCadenaActual[ 'review_date_raw'] = unReviewDateString
                    
                    unReviewDateStringUnicode = u''
                    try:
                        unReviewDateStringUnicode = unReviewDateString.decode( unImportedCharSet )
                    except UnicodeDecodeError:
                        unosDatosCadenaActual[ 'review_date_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .PO' % unImportedCharSet   
                    
                    if unReviewDateStringUnicode:

                        unosDatosCadenaActual[ 'review_date_unicode'] = unReviewDateStringUnicode
                        unReviewDateStringEncoded  = ''
                        try:
                            unReviewDateStringEncoded =  aTranslationService.encode( unReviewDateStringUnicode)      
                        except:
                            unosDatosCadenaActual[ 'review_date_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .PO'   
       
                        if unReviewDateStringEncoded:    
                            unosDatosCadenaActual[ 'review_date_encoded'] = unReviewDateStringEncoded
                continue    
            
            
            
 
            
            elif unaLinea.startswith( cPOTranslationEntryReviewerPrefix):
                
                if not unosDatosCadenaActual:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                        
                unosDatosCadenaActual[ 'continuable_translation']   = False
                    
                unReviewerString = unaLinea[ len( cPOTranslationEntryReviewerPrefix):]
                unReviewerString = unReviewerString.replace( '"', '').strip()
                
                if unReviewerString:
                    
                    unosDatosCadenaActual[ 'reviewer_raw'] = unReviewerString
                    
                    unReviewerStringUnicode = u''
                    try:
                        unReviewerStringUnicode = unReviewerString.decode( unImportedCharSet )
                    except UnicodeDecodeError:
                        unosDatosCadenaActual[ 'reviewer_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .PO' % unImportedCharSet   
                    
                    if unReviewerStringUnicode:

                        unosDatosCadenaActual[ 'reviewer_unicode'] = unReviewerStringUnicode
                        unReviewerStringEncoded  = ''
                        try:
                            unReviewerStringEncoded =  aTranslationService.encode( unReviewerStringUnicode)      
                        except:
                            unosDatosCadenaActual[ 'reviewer_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .PO'   
       
                        if unReviewerStringEncoded:    
                            unosDatosCadenaActual[ 'reviewer_encoded'] = unReviewerStringEncoded
                continue    
            
                        
            
            elif unaLinea.startswith( cPOTranslationEntryDefinitiveDatePrefix):
                
                if not unosDatosCadenaActual:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                        
                unosDatosCadenaActual[ 'continuable_translation']   = False
                    
                unDefinitiveDateString = unaLinea[ len( cPOTranslationEntryDefinitiveDatePrefix):]
                unDefinitiveDateString = unDefinitiveDateString.replace( '"', '').strip()
                
                if unDefinitiveDateString:
                    
                    unosDatosCadenaActual[ 'definitive_date_raw'] = unDefinitiveDateString
                    
                    unDefinitiveDateStringUnicode = u''
                    try:
                        unDefinitiveDateStringUnicode = unDefinitiveDateString.decode( unImportedCharSet )
                    except UnicodeDecodeError:
                        unosDatosCadenaActual[ 'definitive_date_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .PO' % unImportedCharSet   
                    
                    if unDefinitiveDateStringUnicode:

                        unosDatosCadenaActual[ 'definitive_date_unicode'] = unDefinitiveDateStringUnicode
                        unDefinitiveDateStringEncoded  = ''
                        try:
                            unDefinitiveDateStringEncoded =  aTranslationService.encode( unDefinitiveDateStringUnicode)      
                        except:
                            unosDatosCadenaActual[ 'definitive_date_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .PO'   
       
                        if unDefinitiveDateStringEncoded:    
                            unosDatosCadenaActual[ 'definitive_date_encoded'] = unDefinitiveDateStringEncoded
                continue    
            
            
            
 
            
            elif unaLinea.startswith( cPOTranslationEntryCoordinatorPrefix):
                
                if not unosDatosCadenaActual:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                        
                unosDatosCadenaActual[ 'continuable_translation']   = False
                    
                unCoordinatorString = unaLinea[ len( cPOTranslationEntryCoordinatorPrefix):]
                unCoordinatorString = unCoordinatorString.replace( '"', '').strip()
                
                if unCoordinatorString:
                    
                    unosDatosCadenaActual[ 'coordinator_raw'] = unCoordinatorString
                    
                    unCoordinatorStringUnicode = u''
                    try:
                        unCoordinatorStringUnicode = unCoordinatorString.decode( unImportedCharSet )
                    except UnicodeDecodeError:
                        unosDatosCadenaActual[ 'coordinator_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .PO' % unImportedCharSet   
                    
                    if unCoordinatorStringUnicode:

                        unosDatosCadenaActual[ 'coordinator_unicode'] = unCoordinatorStringUnicode
                        unCoordinatorStringEncoded  = ''
                        try:
                            unCoordinatorStringEncoded =  aTranslationService.encode( unCoordinatorStringUnicode)      
                        except:
                            unosDatosCadenaActual[ 'coordinator_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .PO'   
       
                        if unCoordinatorStringEncoded:    
                            unosDatosCadenaActual[ 'coordinator_encoded'] = unCoordinatorStringEncoded
                continue    
            

            
            
            
            elif unaLinea.startswith( cPOTranslationEntrySourcesPrefix):
                                    
                if not unosDatosCadenaActual:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                        
                unosDatosCadenaActual[ 'continuable_translation']   = False
                    
                unosSourcesString = unaLinea[ len( cPOTranslationEntrySourcesPrefix):]
                unosSourcesString = unosSourcesString.replace( '"', '').strip()
                
                if unosSourcesString:
                    
                    unosDatosCadenaActual[ 'sources_raw'] = unosSourcesString
                    
                    unSourcesStringUnicode = u''
                    try:
                        unSourcesStringUnicode = unosSourcesString.decode( unImportedCharSet )
                    except UnicodeDecodeError:
                        unosDatosCadenaActual[ 'sources_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .PO' % unImportedCharSet   
                    
                    if unSourcesStringUnicode:

                        unosDatosCadenaActual[ 'sources_unicode'] = unSourcesStringUnicode
                        unSourcesStringEncoded  = ''
                        try:
                            unSourcesStringEncoded =  aTranslationService.encode( unSourcesStringUnicode)      
                        except:
                            unosDatosCadenaActual[ 'sources_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .PO'   
       
                        if unSourcesStringEncoded:    
                            unosDatosCadenaActual[ 'sources_encoded'] = unSourcesStringEncoded

                continue    
            
            
            
            
            elif unaLinea.startswith( cPOTranslationEntryFlagsPrefix):
                
                if not unosDatosCadenaActual:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                        
                unosDatosCadenaActual[ 'continuable_translation']   = False
                    
                unosFlagsString = unaLinea[ len( cPOTranslationEntryFlagsPrefix):]
                unosFlagsString = unosFlagsString.replace( '"', '').strip()
                
                if unosFlagsString:
                    
                    unosDatosCadenaActual[ 'flags_raw'] = unosFlagsString
                    
                    unFlagsStringUnicode = u''
                    try:
                        unFlagsStringUnicode = unosFlagsString.decode( unImportedCharSet )
                    except UnicodeDecodeError:
                        unosDatosCadenaActual[ 'flags_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .PO' % unImportedCharSet   
                    
                    if unFlagsStringUnicode:

                        unosDatosCadenaActual[ 'flags_unicode'] = unFlagsStringUnicode
                        unFlagsStringEncoded  = ''
                        try:
                            unFlagsStringEncoded =  aTranslationService.encode( unFlagsStringUnicode)      
                        except:
                            unosDatosCadenaActual[ 'flags_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .PO'   
       
                        if unFlagsStringEncoded:    
                            unosDatosCadenaActual[ 'flags_encoded'] = unFlagsStringEncoded
                continue    
            
            
            
                                    
            
            elif unaLinea.startswith( cPOTranslationEntryCommentPrefix):
                
                if not unosDatosCadenaActual:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                        
                unosDatosCadenaActual[ 'continuable_translation']   = False
                    
                unosCommentString = unaLinea[ len( cPOTranslationEntryCommentPrefix):]
                unosCommentString = unosCommentString.replace( '"', '').strip()
                
                if unosCommentString:
                    
                    unosDatosCadenaActual[ 'comment_raw'] = unosCommentString
                    
                    unCommentStringUnicode = u''
                    try:
                        unCommentStringUnicode = unosCommentString.decode( unImportedCharSet )
                    except UnicodeDecodeError:
                        unosDatosCadenaActual[ 'comment_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .PO' % unImportedCharSet   
                    
                    if unCommentStringUnicode:

                        unosDatosCadenaActual[ 'comment_unicode'] = unCommentStringUnicode
                        unCommentStringEncoded  = ''
                        try:
                            unCommentStringEncoded =  aTranslationService.encode( unCommentStringUnicode)      
                        except:
                            unosDatosCadenaActual[ 'comment_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .PO'   
       
                        if unCommentStringEncoded:    
                            unosDatosCadenaActual[ 'comment_encoded'] = unCommentStringEncoded
                continue    
                

            
            
            elif unaLinea.startswith( cPOTranslationEntryMsgidPrefix):
                
                if not unosDatosCadenaActual:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                        
                unosDatosCadenaActual[ 'continuable_translation']   = False
                    
                unMsgidString = unaLinea[ len( cPOTranslationEntryMsgidPrefix):]
                unMsgidString = unMsgidString.replace( '"', '').strip()
                
                if not unMsgidString:
                    unosDatosCadenaActual[ 'empty_symbol'] = True
                    
                else:
                                       
                    unosDatosCadenaActual[ 'symbol_raw'] = unMsgidString
                    
                    unMsgidStringUnicode = u''
                    try:
                        unMsgidStringUnicode = unMsgidString.decode( unImportedCharSet )
                    except UnicodeDecodeError:
                        unosDatosCadenaActual[ 'symbol_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .PO' % unImportedCharSet   
                        unosDatosCadenaActual[ 'symbol_error_line'] = unNextLineIndex
                        
                    if unMsgidStringUnicode:
                        
                        unosDatosCadenaActual[ 'symbol_unicode'] = unMsgidStringUnicode
                        unMsgidStringEncoded  = ''
                        try:
                            unMsgidStringEncoded =  aTranslationService.encode( unMsgidStringUnicode)      
                        except:
                            unosDatosCadenaActual[ 'symbol_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .PO'   
                            unosDatosCadenaActual[ 'symbol_error_line'] = unNextLineIndex
       
                        if unMsgidStringEncoded:    
                            unosDatosCadenaActual[ 'symbol_encoded'] = unMsgidStringEncoded
                continue    
            
            
            
            
            
            elif unaLinea.startswith( cPOTranslationEntryMsgstrPrefix):
                
                if not unosDatosCadenaActual:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                        
                unosDatosCadenaActual[ 'continuable_translation']   = False
                    
                unMsgstrString = unaLinea[ len( cPOTranslationEntryMsgstrPrefix):].replace( '"', '').strip()
                unMsgstrString = unMsgstrString.replace( '"', '').strip()
                
                if not unMsgstrString:
                    unosDatosCadenaActual[ 'continuable_translation']   = True
                    
                    unosDatosCadenaActual[ 'translation_raw']     = ''
                    unosDatosCadenaActual[ 'translation_unicode'] = u''
                    unosDatosCadenaActual[ 'translation_encoded'] = ''
                    
                    
                else:
                    
                    unosDatosCadenaActual[ 'translation_raw'] = unMsgstrString
                    
                    unaTraduccionUnicode = u''
                    try:
                        unaTraduccionUnicode = unMsgstrString.decode( unImportedCharSet)
                    except UnicodeDecodeError:
                        unosDatosCadenaActual[ 'translation_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .PO' % unImportedCharSet  
                    
                    if unaTraduccionUnicode:
                        unosDatosCadenaActual[ 'translation_unicode'] = unaTraduccionUnicode
                        
                        unaTraduccionEncoded  = ''
                        try:
                            unaTraduccionEncoded =  aTranslationService.encode( unaTraduccionUnicode)      
                        except:
                            unosDatosCadenaActual[ 'translation_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .PO'   
                        
                        if unaTraduccionEncoded:    
                            unosDatosCadenaActual[ 'translation_encoded'] = unaTraduccionEncoded
                            
                continue 
            
            
            elif unaLinea.startswith( cPOTranslationEntryMsgstrContinuationPrefix):
                
                if not unosDatosCadenaActual:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                    
                if not unosDatosCadenaActual.get( 'continuable_translation', False):
                    
                    unosDatosCadenaActual[ 'syntax_error'] = True
                    unosDatosCadenaActual[ 'syntax_error_recoverable'] = False
                    return unosDatosCadenaActual
                
                        
                unMsgstrString = unaLinea[ len( cPOTranslationEntryMsgstrContinuationPrefix):].replace( '"', '').strip()
                unMsgstrString = unMsgstrString.replace( '"', '').strip()
                
                if not unMsgstrString:
                    continue
                    
                else:
                    
                    unosDatosCadenaActual[ 'translation_raw'] = '%s%s' % ( unosDatosCadenaActual.get( 'translation_raw', ''), unMsgstrString)
                    
                    unaTraduccionUnicode = u''
                    try:
                        unaTraduccionUnicode = unMsgstrString.decode( unImportedCharSet)
                    except UnicodeDecodeError:
                        unosDatosCadenaActual[ 'translation_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .PO' % unImportedCharSet  
                    
                    if unaTraduccionUnicode:
                        unosDatosCadenaActual[ 'translation_unicode'] = u'%s%s' % ( unosDatosCadenaActual.get( 'translation_unicode', ''), unaTraduccionUnicode) 
                        
                        unaTraduccionEncoded  = ''
                        try:
                            unaTraduccionEncoded =  aTranslationService.encode( unaTraduccionUnicode)      
                        except:
                            unosDatosCadenaActual[ 'translation_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .PO'   
                        
                        if unaTraduccionEncoded:    
                            unosDatosCadenaActual[ 'translation_encoded'] = '%s%s' % ( unosDatosCadenaActual.get( 'translation_encoded', ''), unaTraduccionEncoded) 
                            
                continue 
            
            
            
            else:
                if not unosDatosCadenaActual:
                    return None
                
                unosDatosCadenaActual[ 'syntax_error'] = True
                unosDatosCadenaActual[ 'syntax_error_recoverable'] = False
                return unosDatosCadenaActual
                    
                
            
        return None
   
    
    
                    
 

                
                
                
                
                 
                
    
    
    
    
    