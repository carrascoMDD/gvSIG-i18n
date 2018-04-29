# -*- coding: utf-8 -*-
#
# File: TRAImportacion_Operaciones_Parse_JavaProperties.py
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

from TRAImportarExportar_Constants                  import *
from TRAImportarExportar_Constants_JavaProperties   import *
from TRAImportarExportar_Constants_Encodings        import *






class TRAImportacion_Operaciones_Parse_JavaProperties:
    """
    """
    security = ClassSecurityInfo()
     


    
    security.declarePrivate( 'fNewVoidImportCursor_JavaProperties')    
    def fNewVoidImportCursor_JavaProperties( self,):
        unCursor = self.fNewVoidImportCursor()
        unCursor.update( {
            'cursor_records_scanned':       False,
            'cursor_records_by_symbol':     { },
            'all_cursor_records':           [ ],
            'next_cursor_record_index':     0,
        })
        return unCursor
    
    
        
    
              

                         
            


    security.declarePrivate( 'fModuleLocaleLanguageAndCountryFromPropertiesFileName')    
    def fModuleLocaleLanguageAndCountryFromPropertiesFileName( self, theFileName, theDefaultModule, theDefaultLanguage):
        
        if not theFileName :
            return (  None, None, None, )
        
        aFileNameLower = theFileName.lower()
 
        if aFileNameLower in [ cManifestFileFullName.lower(), cLocalesCSVFileFullName.lower(),]:
            return (  None, None, None, )
             
        if aFileNameLower == cDefaultLanguagePropertiesFileName:
            return ( theDefaultModule, theDefaultLanguage, None)
        
        aFileNameWOPostfix, aFileNamePostfix = os.path.splitext(  theFileName)
        
        if not( aFileNamePostfix.lower() == cPropertiesFilePostfix.lower()):
            return (  None, None, None, )
        
        unModule = ''
        unLocaleLanguage = ''
        unLocaleCountry  = ''
        
        
        aFileNameWOPostfixLower = aFileNameWOPostfix.lower()

        if aFileNameWOPostfixLower.startswith( cFilenamePropertiesBase):
            
            unModule = theDefaultModule
            unIndexCharBeforeLanguage = len( cFilenamePropertiesBase)

        else:
            unIndexCharBeforeLanguage = aFileNameWOPostfixLower.find( cPropertiesFileCharBeforeLanguage, 0)
            if not ( unIndexCharBeforeLanguage >= 0):
                unModule = aFileNameWOPostfix
                return ( unModule, theDefaultLanguage, None)
            else:
                unModule = aFileNameWOPostfix[:unIndexCharBeforeLanguage]
            
                
                
        unIndexCharBeforeCountry = aFileNameWOPostfixLower.find( cPropertiesFileCharBeforeCountry, unIndexCharBeforeLanguage + 1)
        if unIndexCharBeforeCountry >= 0:
            unLocaleLanguage = aFileNameWOPostfixLower[ unIndexCharBeforeLanguage + len( cPropertiesFileCharBeforeLanguage):unIndexCharBeforeCountry].lower()   
            unLocaleCountry  = aFileNameWOPostfixLower[  unIndexCharBeforeCountry + len( cPropertiesFileCharBeforeCountry):].lower()   
        else:
            unLocaleLanguage = aFileNameWOPostfixLower[ unIndexCharBeforeLanguage + len( cPropertiesFileCharBeforeLanguage):].lower()   
            unLocaleCountry = ''
                
        return ( unModule, unLocaleLanguage, unLocaleCountry, )       
                
    
    
                            
   
                
                  
  
     

    
                
    security.declarePrivate( 'fLocaleLanguageAndCountryFromPropertiesContent')    
    def fLocaleLanguageAndCountryFromPropertiesContent( self, theParentExecutionRecord, theContent):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fLocaleLanguageAndCountryFromPropertiesContent', theParentExecutionRecord, False) 

        try:

            if not theContent:
                return ( None, None, )
            
            someLines = theContent.splitlines()
            
            unNumLines = len( someLines)
                    
            if unNumLines < 1:
                return ( None, None, )
    
            if not ( someLines[ 0].startswith( cPrefixLineaLenguaje)):
                return ( None, None, )
                
            unLocaleLanguage = ''
            unLocaleCountry  = ''
            
            unLenguage = someLines[0][len(cPrefixLineaLenguaje):]
            unBracketIndex = unLenguage.find( ']')
            if unBracketIndex >= 0:
                unLenguageAndCountry = unLenguage[:unBracketIndex]
                 
                unIndexCharBeforeCountry = unLenguageAndCountry.find( cLanguageSeparatorCountry, 0)
                if unIndexCharBeforeCountry >= 0:
                    unLocaleLanguage = unLenguageAndCountry[ :unIndexCharBeforeCountry].lower()  
                    unLocaleCountry  = unLenguageAndCountry[  unIndexCharBeforeCountry + len( cLanguageSeparatorCountry) :].lower()
                else:
                    unLocaleLanguage = unLenguageAndCountry.lower()
                    unLocaleCountry = ''
                     
            return ( unLocaleLanguage, unLocaleCountry, )
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

                     
                
                
    
                
        
        
        
        
        
        
            

    security.declarePrivate( 'pScanTranslationsProperties')    
    def pScanTranslationsProperties( self,
        theParentExecutionRecord =None, 
        theUploadedFile         =None, 
        theZipFile              =None, 
        theUploadedContent       =None,
        theUploadedEntry        =None,
        theAdditionalParams     =None):
        """Parse a complete Java .properties file, and produce a data structure with all information read.
        
        """
                
        unExecutionRecord = self.fStartExecution( 'method',  'pScanTranslationsProperties', theParentExecutionRecord, False) 

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
            aImportarContribucionesDesdeComentarios =  theAdditionalParams.get( 'theImportContributionsFromComment',   False) == True
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

                unFicheroImportCursor = self.fFicheroImportCursorProperties( theUploadedEntry, unContentData, aNumeroMaximoLineasAExplorar)
                if unFicheroImportCursor:
                    
                    if unFicheroImportCursor.get( 'exceeded_max_number_of_lines', False):
                        theUploadedEntry[ 'exceeded_max_number_of_lines'] = True
            else:
                theUploadedFile.seek( 0)
                unContentData = theUploadedFile.read()
                if not unContentData:
                    return self

                unFicheroImportCursor = self.fFicheroImportCursorProperties( theUploadedEntry, unContentData, aNumeroMaximoLineasAExplorar)
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
            """Iterate over .properties data.

            """            
            unCursorRecord = self.fNextCursorRecordProperties( unFicheroImportCursor)
            
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
                    """Add to translation data the translation just read.
        
                    """                                                                        

                    unTranslationEncoded = unCursorRecord[ 'translation_encoded']
                    unTranslationError   = unCursorRecord[ 'translation_error']
                    
                    
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
                                
                                            
                                
                                
                            
                unCursorRecord = self.fNextCursorRecordProperties( unFicheroImportCursor)
                 
                                
                

                
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

                                           
                
                
                

   
    
    security.declarePrivate( 'fFicheroImportCursorProperties')    
    def fFicheroImportCursorProperties( self, theUploadedEntry, theContent, theMaxNumLinesToExplore):
        if not theContent:
            return None
        
        unCursor = self.fNewVoidImportCursor_JavaProperties()
        unCursor[ 'file_kind'] = cPropertiesFilePostfix
        
        aTranslationService = self.getTranslationServiceTool()
        unCursor[ 'translation_service'] = aTranslationService
 
        someLines = theContent.splitlines()
        unCursor[ 'content_lines']  = someLines
        
        unNumLines = len( someLines)
        
        unCursor[ 'max_number_of_lines'] = theMaxNumLinesToExplore
        
        if theMaxNumLinesToExplore >= 0:
            if unNumLines > theMaxNumLinesToExplore:
                unNumLines = theMaxNumLinesToExplore + cPropertiesMaxLinesToScanTryingToGetCadena
                unCursor[ 'content_lines']  = someLines[:theMaxNumLinesToExplore]
                unCursor[ 'exceeded_max_number_of_lines'] = True        

         
        unCursor[ 'num_lines']      = unNumLines
        unCursor[ 'next_line_index'] = 0

                
        if unNumLines < 1:
            unCursor[ 'error'] = "gvSIGi18n_NoContentLines_error_msgid"
            unCursor[ 'error_detail'] = theFileName                    
            return None

        unCursor[ 'next_line_index'] = 0
        if ( someLines[ 0].startswith( cPrefixLineaLenguaje)):
            unCursor[ 'next_line_index'] += 1
            unLenguage = someLines[ 0][ len(  cPrefixLineaLenguaje):]
            unBracketIndex = unLenguage.find( ']')
            if unBracketIndex >= 0:
                unLenguage = unLenguage[:unBracketIndex]
            if unLenguage:
                unCursor[ 'language'] = unLenguage
        
        unaPosibleLineaTimestamp = someLines[ unCursor[ 'next_line_index']]
        if unaPosibleLineaTimestamp and ( unaPosibleLineaTimestamp[ 0] == cPrefixLineaTimestamp):
            unCursor[ 'next_line_index'] += 1
        
            
        # ACV 20101010 Scan also the properties header, which shall be ignored because it returns a cursor record with empty_symbol
        unCursor[ 'next_line_index'] = 0
            
        unCursor[ 'num_possible_records'] = unNumLines - unCursor[ 'next_line_index']
        
        if unCursor[ 'next_line_index'] >= unCursor[ 'num_lines']:
            return None
        
        return unCursor
           

    
    
    
    
    
    
   
    security.declarePrivate( 'fNextCursorRecordProperties')    
    def fNextCursorRecordProperties( self, theCursor):
        if not theCursor:
            return None
        
        if not theCursor[ 'file_kind'] == cPropertiesFilePostfix:
            return None


        # #################################3
        """Assemble all cursor records - if not already done so, and retrieve next cursor record.

        """
        
        if not theCursor.get( 'cursor_records_scanned', False):
            self.pAssembleAllCursorRecordsProperties( theCursor)
        
            if not theCursor.get( 'cursor_records_scanned', False):
                return None
        
        
        allCursorRecords = theCursor.get( 'all_cursor_records', [])
        if not allCursorRecords:
            return None
        
        aNextCursorRecordIndex = theCursor.get( 'next_cursor_record_index', -1)
        if aNextCursorRecordIndex < 0:
            return None
        
        if aNextCursorRecordIndex >= len( allCursorRecords):
            return None
        
        aCursorRecord = allCursorRecords[ aNextCursorRecordIndex]
        if not aCursorRecord:
            return None
        
        theCursor[ 'next_cursor_record_index'] = aNextCursorRecordIndex + 1
        
        return aCursorRecord
            

    
                    
                
    
    




   
    security.declarePrivate( 'pAssembleAllCursorRecordsProperties')    
    def pAssembleAllCursorRecordsProperties( self, theCursor):
        """Assemble cursor records with all information in the file for each symbol, including - if present - module names, status, sources and flags for each symbol.

        """
        if not theCursor:
            return self
        
        if not theCursor[ 'file_kind'] == cPropertiesFilePostfix:
            return self

        
        
        # ##############################################################
        """Obtain translation service and encoding to decode strings read from file.
        
        """
        aTranslationService = theCursor[ 'translation_service']
        if not aTranslationService:
            return self
        
        
        unImportedCharSet = theCursor[ 'charset']
        if not unImportedCharSet:
            unImportedCharSet = cRawUnicodeEscapeEncoding   
            
            
            
        
        # #################################3
        """Pass if all cursor records already assembled.

        """
        if theCursor.get( 'cursor_records_scanned', False):
            return self
                
        
        allCursorRecords = theCursor.get( 'all_cursor_records', None)
        if allCursorRecords == None:
            allCursorRecords = [ ]
            theCursor[ 'all_cursor_records'] = allCursorRecords
            
        theCursor[ 'next_cursor_record_index'] = 0

        someCursorRecordsBySymbol = theCursor.get( 'cursor_records_by_symbol', None)
        if someCursorRecordsBySymbol == None:
            someCursorRecordsBySymbol = { }
            theCursor[ 'cursor_records_by_symbol'] = someCursorRecordsBySymbol

            

                
        # ##############################################################
        """Loop to scan all lines.
        
        """
        
        theCursor[ 'cursor_records_scanned'] = True

        
        while True:

            
            unNextLineIndex = theCursor[ 'next_line_index']
            
            
            # ##############################################################
            """Check for end of content.
            
            """
            if  unNextLineIndex >= theCursor[ 'num_lines']:
                return self
                    
                    
            

            # ##############################################################
            """Advance cursor for next iteration or end of exploration.
            
            """
            theCursor[ 'next_line_index'] += 1
            
            
            
            
            
            # ##############################################################
            """Retrieve line to parse.
            
            """
            unaLinea = theCursor[ 'content_lines'][ unNextLineIndex].strip()
            
            
            
            # ##############################################################
            """Ignore blank lines.
            
            """
            if not unaLinea:
                continue
           
                    
            
                    
            # ##############################################################
            """Parse line according to the characters at the start of the line.
            
            """            
            
            if unaLinea.startswith( cPropertiesModulesLinePrefix):
                          
                unSymbolAndModulesString = unaLinea[ len( cPropertiesModulesLinePrefix):]
                
                unPropertyNameValueSeparatorIndex = unSymbolAndModulesString.find( cPropertyNameValueSeparator)
                if unPropertyNameValueSeparatorIndex <= 0:
                    continue
                
                unSymbolModules = unSymbolAndModulesString[:unPropertyNameValueSeparatorIndex]
                if not unSymbolModules:
                    continue
                
                unosModulesString = unSymbolAndModulesString[ unPropertyNameValueSeparatorIndex + 1:]
                if not unosModulesString:
                    continue
                
                unosDatosCadenaActual = someCursorRecordsBySymbol.get( unSymbolModules, None)
                if unosDatosCadenaActual == None:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                    allCursorRecords.append( unosDatosCadenaActual)
                    someCursorRecordsBySymbol[ unSymbolModules] = unosDatosCadenaActual


                unosDatosCadenaActual[ 'modules_raw'] = unosModulesString
                
                unModulesStringUnicode = u''
                try:
                    unModulesStringUnicode = unosModulesString.decode( unImportedCharSet )
                except UnicodeDecodeError:
                    unosDatosCadenaActual[ 'modules_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .properties' % unImportedCharSet   
                
                if unModulesStringUnicode:

                    unosDatosCadenaActual[ 'modules_unicode'] = unModulesStringUnicode
                    
                    unModulesStringEncoded  = ''
                    try:
                        unModulesStringEncoded =  aTranslationService.encode( unModulesStringUnicode)      
                    except:
                        unosDatosCadenaActual[ 'modules_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .properties'   
   
                    if unModulesStringEncoded:    
                        unosDatosCadenaActual[ 'modules_encoded'] = unModulesStringEncoded
                    
                continue    
            
            
            
            
            
            
            elif unaLinea.startswith( cPropertiesStatusLinePrefix):
                
                unSymbolAndStatusString = unaLinea[ len( cPropertiesStatusLinePrefix):]
                
                unPropertyNameValueSeparatorIndex = unSymbolAndStatusString.find( cPropertyNameValueSeparator)
                if unPropertyNameValueSeparatorIndex <= 0:
                    continue
                
                unSymbolStatus = unSymbolAndStatusString[:unPropertyNameValueSeparatorIndex]
                if not unSymbolStatus:
                    continue
                
                unStatusString = unSymbolAndStatusString[ unPropertyNameValueSeparatorIndex + 1:]
                if not unStatusString:
                    continue
                
                unosDatosCadenaActual = someCursorRecordsBySymbol.get( unSymbolStatus, None)
                if unosDatosCadenaActual == None:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                    allCursorRecords.append( unosDatosCadenaActual)
                    someCursorRecordsBySymbol[ unSymbolStatus] = unosDatosCadenaActual


                unosDatosCadenaActual[ 'status_raw'] = unStatusString
                
                unStatusStringUnicode = u''
                try:
                    unStatusStringUnicode = unStatusString.decode( unImportedCharSet )
                except UnicodeDecodeError:
                    unosDatosCadenaActual[ 'status_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .properties' % unImportedCharSet   
                
                if unStatusStringUnicode:

                    unosDatosCadenaActual[ 'modules_unicode'] = unStatusStringUnicode
                    
                    unStatusStringEncoded  = ''
                    try:
                        unStatusStringEncoded =  aTranslationService.encode( unStatusStringUnicode)      
                    except:
                        unosDatosCadenaActual[ 'status_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .properties'   
   
                    if unStatusStringEncoded:    
                        unosDatosCadenaActual[ 'status_encoded'] = unStatusStringEncoded
                    
                continue    
                           
                
                
                
                
            
            
            elif unaLinea.startswith( cPropertiesSourcesLinePrefix):
  
                unSymbolAndSourcesString = unaLinea[ len( cPropertiesSourcesLinePrefix):]
                
                unPropertyNameValueSeparatorIndex = unSymbolAndSourcesString.find( cPropertyNameValueSeparator)
                if unPropertyNameValueSeparatorIndex <= 0:
                    continue
                
                unSymbolSources = unSymbolAndSourcesString[:unPropertyNameValueSeparatorIndex]
                if not unSymbolSources:
                    continue
                
                unosSourcesString = unSymbolAndSourcesString[ unPropertyNameValueSeparatorIndex + 1:]
                if not unosSourcesString:
                    continue
                
                unosDatosCadenaActual = someCursorRecordsBySymbol.get( unSymbolSources, None)
                if unosDatosCadenaActual == None:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                    allCursorRecords.append( unosDatosCadenaActual)
                    someCursorRecordsBySymbol[ unSymbolSources] = unosDatosCadenaActual


                unosDatosCadenaActual[ 'sources_raw'] = unosSourcesString
                
                unSourcesStringUnicode = u''
                try:
                    unSourcesStringUnicode = unosSourcesString.decode( unImportedCharSet )
                except UnicodeDecodeError:
                    unosDatosCadenaActual[ 'sources_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .properties' % unImportedCharSet   
                
                if unSourcesStringUnicode:

                    unosDatosCadenaActual[ 'sources_unicode'] = unSourcesStringUnicode
                    
                    unSourcesStringEncoded  = ''
                    try:
                        unSourcesStringEncoded =  aTranslationService.encode( unSourcesStringUnicode)      
                    except:
                        unosDatosCadenaActual[ 'sources_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .properties'   
   
                    if unSourcesStringEncoded:    
                        unosDatosCadenaActual[ 'sources_encoded'] = unSourcesStringEncoded
                    
                continue    
            
            
                
            
            
            
            elif unaLinea.startswith( cPropertiesFlagsLinePrefix):
                
                unSymbolAndFlagsString = unaLinea[ len( cPropertiesFlagsLinePrefix):]
                
                unPropertyNameValueSeparatorIndex = unSymbolAndFlagsString.find( cPropertyNameValueSeparator)
                if unPropertyNameValueSeparatorIndex <= 0:
                    continue
                
                unSymbolFlags = unSymbolAndFlagsString[:unPropertyNameValueSeparatorIndex]
                if not unSymbolFlags:
                    continue
                
                unosFlagsString = unSymbolAndFlagsString[ unPropertyNameValueSeparatorIndex + 1:]
                if not unosFlagsString:
                    continue
                
                unosDatosCadenaActual = someCursorRecordsBySymbol.get( unSymbolFlags, None)
                if unosDatosCadenaActual == None:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                    allCursorRecords.append( unosDatosCadenaActual)
                    someCursorRecordsBySymbol[ unSymbolFlags] = unosDatosCadenaActual


                unosDatosCadenaActual[ 'flags_raw'] = unosFlagsString
                
                unFlagsStringUnicode = u''
                try:
                    unFlagsStringUnicode = unosFlagsString.decode( unImportedCharSet )
                except UnicodeDecodeError:
                    unosDatosCadenaActual[ 'flags_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .properties' % unImportedCharSet   
                
                if unFlagsStringUnicode:

                    unosDatosCadenaActual[ 'flags_unicode'] = unFlagsStringUnicode
                    
                    unFlagsStringEncoded  = ''
                    try:
                        unFlagsStringEncoded =  aTranslationService.encode( unFlagsStringUnicode)      
                    except:
                        unosDatosCadenaActual[ 'flags_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .properties'   
   
                    if unFlagsStringEncoded:    
                        unosDatosCadenaActual[ 'flags_encoded'] = unFlagsStringEncoded
                    
                continue    
                            

            
            
            
            
            
            elif unaLinea.startswith( cPropertiesCommentLinePrefix):

                unSymbolAndCommentString = unaLinea[ len( cPropertiesCommentLinePrefix):]
                
                unPropertyNameValueSeparatorIndex = unSymbolAndCommentString.find( cPropertyNameValueSeparator)
                if unPropertyNameValueSeparatorIndex <= 0:
                    continue
                
                unSymbolComment = unSymbolAndCommentString[:unPropertyNameValueSeparatorIndex]
                if not unSymbolComment:
                    continue
                
                unCommentString = unSymbolAndCommentString[ unPropertyNameValueSeparatorIndex + 1:]
                if not unCommentString:
                    continue
                
                unosDatosCadenaActual = someCursorRecordsBySymbol.get( unSymbolComment, None)
                if unosDatosCadenaActual == None:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                    allCursorRecords.append( unosDatosCadenaActual)
                    someCursorRecordsBySymbol[ unSymbolComment] = unosDatosCadenaActual


                unosDatosCadenaActual[ 'comment_raw'] = unCommentString
                
                unCommentStringUnicode = u''
                try:
                    unCommentStringUnicode = unCommentString.decode( unImportedCharSet )
                except UnicodeDecodeError:
                    unosDatosCadenaActual[ 'comment_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .properties' % unImportedCharSet   
                
                if unCommentStringUnicode:

                    unosDatosCadenaActual[ 'comment_unicode'] = unCommentStringUnicode
                    
                    unCommentStringEncoded  = ''
                    try:
                        unCommentStringEncoded =  aTranslationService.encode( unCommentStringUnicode)      
                    except:
                        unosDatosCadenaActual[ 'comment_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .properties'   
   
                    if unCommentStringEncoded:    
                        unosDatosCadenaActual[ 'comment_encoded'] = unCommentStringEncoded
                    
                continue    
            
                            
            

            
            elif unaLinea.startswith( cPropertiesCreationDateLinePrefix):

                unSymbolAndCreationDateString = unaLinea[ len( cPropertiesCreationDateLinePrefix):]
                
                unPropertyNameValueSeparatorIndex = unSymbolAndCreationDateString.find( cPropertyNameValueSeparator)
                if unPropertyNameValueSeparatorIndex <= 0:
                    continue
                
                unSymbolCreationDate = unSymbolAndCreationDateString[:unPropertyNameValueSeparatorIndex]
                if not unSymbolCreationDate:
                    continue
                
                unCreationDateString = unSymbolAndCreationDateString[ unPropertyNameValueSeparatorIndex + 1:]
                if not unCreationDateString:
                    continue
                
                unosDatosCadenaActual = someCursorRecordsBySymbol.get( unSymbolCreationDate, None)
                if unosDatosCadenaActual == None:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                    allCursorRecords.append( unosDatosCadenaActual)
                    someCursorRecordsBySymbol[ unSymbolCreationDate] = unosDatosCadenaActual


                unosDatosCadenaActual[ 'creation_date_raw'] = unCreationDateString
                
                unCreationDateStringUnicode = u''
                try:
                    unCreationDateStringUnicode = unCreationDateString.decode( unImportedCharSet )
                except UnicodeDecodeError:
                    unosDatosCadenaActual[ 'creation_date_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .properties' % unImportedCharSet   
                
                if unCreationDateStringUnicode:

                    unosDatosCadenaActual[ 'creation_date_unicode'] = unCreationDateStringUnicode
                    
                    unCreationDateStringEncoded  = ''
                    try:
                        unCreationDateStringEncoded =  aTranslationService.encode( unCreationDateStringUnicode)      
                    except:
                        unosDatosCadenaActual[ 'creation_date_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .properties'   
   
                    if unCreationDateStringEncoded:    
                        unosDatosCadenaActual[ 'creation_date_encoded'] = unCreationDateStringEncoded
                    
                continue    
            
                             
            

            
            elif unaLinea.startswith( cPropertiesCreatorLinePrefix):

                unSymbolAndCreatorString = unaLinea[ len( cPropertiesCreatorLinePrefix):]
                
                unPropertyNameValueSeparatorIndex = unSymbolAndCreatorString.find( cPropertyNameValueSeparator)
                if unPropertyNameValueSeparatorIndex <= 0:
                    continue
                
                unSymbolCreator = unSymbolAndCreatorString[:unPropertyNameValueSeparatorIndex]
                if not unSymbolCreator:
                    continue
                
                unCreatorString = unSymbolAndCreatorString[ unPropertyNameValueSeparatorIndex + 1:]
                if not unCreatorString:
                    continue
                
                unosDatosCadenaActual = someCursorRecordsBySymbol.get( unSymbolCreator, None)
                if unosDatosCadenaActual == None:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                    allCursorRecords.append( unosDatosCadenaActual)
                    someCursorRecordsBySymbol[ unSymbolCreator] = unosDatosCadenaActual


                unosDatosCadenaActual[ 'creator_raw'] = unCreatorString
                
                unCreatorStringUnicode = u''
                try:
                    unCreatorStringUnicode = unCreatorString.decode( unImportedCharSet )
                except UnicodeDecodeError:
                    unosDatosCadenaActual[ 'creator_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .properties' % unImportedCharSet   
                
                if unCreatorStringUnicode:

                    unosDatosCadenaActual[ 'creator_unicode'] = unCreatorStringUnicode
                    
                    unCreatorStringEncoded  = ''
                    try:
                        unCreatorStringEncoded =  aTranslationService.encode( unCreatorStringUnicode)      
                    except:
                        unosDatosCadenaActual[ 'creator_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .properties'   
   
                    if unCreatorStringEncoded:    
                        unosDatosCadenaActual[ 'creator_encoded'] = unCreatorStringEncoded
                    
                continue    
            
                             
            
            
            
           
            
            
            elif unaLinea.startswith( cPropertiesTranslationDateLinePrefix):

                unSymbolAndTranslationDateString = unaLinea[ len( cPropertiesTranslationDateLinePrefix):]
                
                unPropertyNameValueSeparatorIndex = unSymbolAndTranslationDateString.find( cPropertyNameValueSeparator)
                if unPropertyNameValueSeparatorIndex <= 0:
                    continue
                
                unSymbolTranslationDate = unSymbolAndTranslationDateString[:unPropertyNameValueSeparatorIndex]
                if not unSymbolTranslationDate:
                    continue
                
                unTranslationDateString = unSymbolAndTranslationDateString[ unPropertyNameValueSeparatorIndex + 1:]
                if not unTranslationDateString:
                    continue
                
                unosDatosCadenaActual = someCursorRecordsBySymbol.get( unSymbolTranslationDate, None)
                if unosDatosCadenaActual == None:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                    allCursorRecords.append( unosDatosCadenaActual)
                    someCursorRecordsBySymbol[ unSymbolTranslationDate] = unosDatosCadenaActual


                unosDatosCadenaActual[ 'translation_date_raw'] = unTranslationDateString
                
                unTranslationDateStringUnicode = u''
                try:
                    unTranslationDateStringUnicode = unTranslationDateString.decode( unImportedCharSet )
                except UnicodeDecodeError:
                    unosDatosCadenaActual[ 'translation_date_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .properties' % unImportedCharSet   
                
                if unTranslationDateStringUnicode:

                    unosDatosCadenaActual[ 'translation_date_unicode'] = unTranslationDateStringUnicode
                    
                    unTranslationDateStringEncoded  = ''
                    try:
                        unTranslationDateStringEncoded =  aTranslationService.encode( unTranslationDateStringUnicode)      
                    except:
                        unosDatosCadenaActual[ 'translation_date_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .properties'   
   
                    if unTranslationDateStringEncoded:    
                        unosDatosCadenaActual[ 'translation_date_encoded'] = unTranslationDateStringEncoded
                    
                continue    
            
                             
            

            
            elif unaLinea.startswith( cPropertiesTranslatorLinePrefix):

                unSymbolAndTranslatorString = unaLinea[ len( cPropertiesTranslatorLinePrefix):]
                
                unPropertyNameValueSeparatorIndex = unSymbolAndTranslatorString.find( cPropertyNameValueSeparator)
                if unPropertyNameValueSeparatorIndex <= 0:
                    continue
                
                unSymbolTranslator = unSymbolAndTranslatorString[:unPropertyNameValueSeparatorIndex]
                if not unSymbolTranslator:
                    continue
                
                unTranslatorString = unSymbolAndTranslatorString[ unPropertyNameValueSeparatorIndex + 1:]
                if not unTranslatorString:
                    continue
                
                unosDatosCadenaActual = someCursorRecordsBySymbol.get( unSymbolTranslator, None)
                if unosDatosCadenaActual == None:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                    allCursorRecords.append( unosDatosCadenaActual)
                    someCursorRecordsBySymbol[ unSymbolTranslator] = unosDatosCadenaActual


                unosDatosCadenaActual[ 'translator_raw'] = unTranslatorString
                
                unTranslatorStringUnicode = u''
                try:
                    unTranslatorStringUnicode = unTranslatorString.decode( unImportedCharSet )
                except UnicodeDecodeError:
                    unosDatosCadenaActual[ 'translator_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .properties' % unImportedCharSet   
                
                if unTranslatorStringUnicode:

                    unosDatosCadenaActual[ 'translator_unicode'] = unTranslatorStringUnicode
                    
                    unTranslatorStringEncoded  = ''
                    try:
                        unTranslatorStringEncoded =  aTranslationService.encode( unTranslatorStringUnicode)      
                    except:
                        unosDatosCadenaActual[ 'translator_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .properties'   
   
                    if unTranslatorStringEncoded:    
                        unosDatosCadenaActual[ 'translator_encoded'] = unTranslatorStringEncoded
                    
                continue    
            
                             
            
            
            
            
            
            elif unaLinea.startswith( cPropertiesReviewDateLinePrefix):

                unSymbolAndReviewDateString = unaLinea[ len( cPropertiesReviewDateLinePrefix):]
                
                unPropertyNameValueSeparatorIndex = unSymbolAndReviewDateString.find( cPropertyNameValueSeparator)
                if unPropertyNameValueSeparatorIndex <= 0:
                    continue
                
                unSymbolReviewDate = unSymbolAndReviewDateString[:unPropertyNameValueSeparatorIndex]
                if not unSymbolReviewDate:
                    continue
                
                unReviewDateString = unSymbolAndReviewDateString[ unPropertyNameValueSeparatorIndex + 1:]
                if not unReviewDateString:
                    continue
                
                unosDatosCadenaActual = someCursorRecordsBySymbol.get( unSymbolReviewDate, None)
                if unosDatosCadenaActual == None:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                    allCursorRecords.append( unosDatosCadenaActual)
                    someCursorRecordsBySymbol[ unSymbolReviewDate] = unosDatosCadenaActual


                unosDatosCadenaActual[ 'review_date_raw'] = unReviewDateString
                
                unReviewDateStringUnicode = u''
                try:
                    unReviewDateStringUnicode = unReviewDateString.decode( unImportedCharSet )
                except UnicodeDecodeError:
                    unosDatosCadenaActual[ 'review_date_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .properties' % unImportedCharSet   
                
                if unReviewDateStringUnicode:

                    unosDatosCadenaActual[ 'review_date_unicode'] = unReviewDateStringUnicode
                    
                    unReviewDateStringEncoded  = ''
                    try:
                        unReviewDateStringEncoded =  aTranslationService.encode( unReviewDateStringUnicode)      
                    except:
                        unosDatosCadenaActual[ 'review_date_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .properties'   
   
                    if unReviewDateStringEncoded:    
                        unosDatosCadenaActual[ 'review_date_encoded'] = unReviewDateStringEncoded
                    
                continue    
            
                             
            
                        

            elif unaLinea.startswith( cPropertiesReviewerLinePrefix):

                unSymbolAndReviewerString = unaLinea[ len( cPropertiesReviewerLinePrefix):]
                
                unPropertyNameValueSeparatorIndex = unSymbolAndReviewerString.find( cPropertyNameValueSeparator)
                if unPropertyNameValueSeparatorIndex <= 0:
                    continue
                
                unSymbolReviewer = unSymbolAndReviewerString[:unPropertyNameValueSeparatorIndex]
                if not unSymbolReviewer:
                    continue
                
                unReviewerString = unSymbolAndReviewerString[ unPropertyNameValueSeparatorIndex + 1:]
                if not unReviewerString:
                    continue
                
                unosDatosCadenaActual = someCursorRecordsBySymbol.get( unSymbolReviewer, None)
                if unosDatosCadenaActual == None:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                    allCursorRecords.append( unosDatosCadenaActual)
                    someCursorRecordsBySymbol[ unSymbolReviewer] = unosDatosCadenaActual


                unosDatosCadenaActual[ 'reviewer_raw'] = unReviewerString
                
                unReviewerStringUnicode = u''
                try:
                    unReviewerStringUnicode = unReviewerString.decode( unImportedCharSet )
                except UnicodeDecodeError:
                    unosDatosCadenaActual[ 'reviewer_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .properties' % unImportedCharSet   
                
                if unReviewerStringUnicode:

                    unosDatosCadenaActual[ 'reviewer_unicode'] = unReviewerStringUnicode
                    
                    unReviewerStringEncoded  = ''
                    try:
                        unReviewerStringEncoded =  aTranslationService.encode( unReviewerStringUnicode)      
                    except:
                        unosDatosCadenaActual[ 'reviewer_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .properties'   
   
                    if unReviewerStringEncoded:    
                        unosDatosCadenaActual[ 'reviewer_encoded'] = unReviewerStringEncoded
                    
                continue    
            
                                         
            
            
  
            elif unaLinea.startswith( cPropertiesDefinitiveDateLinePrefix):

                unSymbolAndDefinitiveDateString = unaLinea[ len( cPropertiesDefinitiveDateLinePrefix):]
                
                unPropertyNameValueSeparatorIndex = unSymbolAndDefinitiveDateString.find( cPropertyNameValueSeparator)
                if unPropertyNameValueSeparatorIndex <= 0:
                    continue
                
                unSymbolDefinitiveDate = unSymbolAndDefinitiveDateString[:unPropertyNameValueSeparatorIndex]
                if not unSymbolDefinitiveDate:
                    continue
                
                unDefinitiveDateString = unSymbolAndDefinitiveDateString[ unPropertyNameValueSeparatorIndex + 1:]
                if not unDefinitiveDateString:
                    continue
                
                unosDatosCadenaActual = someCursorRecordsBySymbol.get( unSymbolDefinitiveDate, None)
                if unosDatosCadenaActual == None:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                    allCursorRecords.append( unosDatosCadenaActual)
                    someCursorRecordsBySymbol[ unSymbolDefinitiveDate] = unosDatosCadenaActual


                unosDatosCadenaActual[ 'definitive_date_raw'] = unDefinitiveDateString
                
                unDefinitiveDateStringUnicode = u''
                try:
                    unDefinitiveDateStringUnicode = unDefinitiveDateString.decode( unImportedCharSet )
                except UnicodeDecodeError:
                    unosDatosCadenaActual[ 'definitive_date_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .properties' % unImportedCharSet   
                
                if unDefinitiveDateStringUnicode:

                    unosDatosCadenaActual[ 'definitive_date_unicode'] = unDefinitiveDateStringUnicode
                    
                    unDefinitiveDateStringEncoded  = ''
                    try:
                        unDefinitiveDateStringEncoded =  aTranslationService.encode( unDefinitiveDateStringUnicode)      
                    except:
                        unosDatosCadenaActual[ 'definitive_date_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .properties'   
   
                    if unDefinitiveDateStringEncoded:    
                        unosDatosCadenaActual[ 'definitive_date_encoded'] = unDefinitiveDateStringEncoded
                    
                continue    
            
                             
            
                        

            elif unaLinea.startswith( cPropertiesCoordinatorLinePrefix):

                unSymbolAndCoordinatorString = unaLinea[ len( cPropertiesCoordinatorLinePrefix):]
                
                unPropertyNameValueSeparatorIndex = unSymbolAndCoordinatorString.find( cPropertyNameValueSeparator)
                if unPropertyNameValueSeparatorIndex <= 0:
                    continue
                
                unSymbolCoordinator = unSymbolAndCoordinatorString[:unPropertyNameValueSeparatorIndex]
                if not unSymbolCoordinator:
                    continue
                
                unCoordinatorString = unSymbolAndCoordinatorString[ unPropertyNameValueSeparatorIndex + 1:]
                if not unCoordinatorString:
                    continue
                
                unosDatosCadenaActual = someCursorRecordsBySymbol.get( unSymbolCoordinator, None)
                if unosDatosCadenaActual == None:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                    allCursorRecords.append( unosDatosCadenaActual)
                    someCursorRecordsBySymbol[ unSymbolCoordinator] = unosDatosCadenaActual


                unosDatosCadenaActual[ 'coordinator_raw'] = unCoordinatorString
                
                unCoordinatorStringUnicode = u''
                try:
                    unCoordinatorStringUnicode = unCoordinatorString.decode( unImportedCharSet )
                except UnicodeDecodeError:
                    unosDatosCadenaActual[ 'coordinator_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .properties' % unImportedCharSet   
                
                if unCoordinatorStringUnicode:

                    unosDatosCadenaActual[ 'coordinator_unicode'] = unCoordinatorStringUnicode
                    
                    unCoordinatorStringEncoded  = ''
                    try:
                        unCoordinatorStringEncoded =  aTranslationService.encode( unCoordinatorStringUnicode)      
                    except:
                        unosDatosCadenaActual[ 'coordinator_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .properties'   
   
                    if unCoordinatorStringEncoded:    
                        unosDatosCadenaActual[ 'coordinator_encoded'] = unCoordinatorStringEncoded
                    
                continue    
            
                                                   
            
            
            
                
            elif unaLinea.startswith( cPropertiesLine_CommentPrefix):
                continue
                            
                
                
            
            
            
            else:
                
                unSeparatorIndex = unaLinea.find( cPropertyNameValueSeparator, 0) 
                if unSeparatorIndex < 0:
                    continue
                
                unSimboloCadena     = unaLinea[ : unSeparatorIndex].strip()
                if not unSimboloCadena:    
                    continue
                    
                
                unosDatosCadenaActual = someCursorRecordsBySymbol.get( unSimboloCadena, None)
                if unosDatosCadenaActual == None:
                    unosDatosCadenaActual = self.fNewVoidCursorRecord()
                    allCursorRecords.append( unosDatosCadenaActual)
                    someCursorRecordsBySymbol[ unSimboloCadena] = unosDatosCadenaActual
                
                    
                unosDatosCadenaActual[ 'symbol_raw'] = unSimboloCadena
                
                unSymbolStringUnicode = u''
                try:
                    unSymbolStringUnicode = unSimboloCadena.decode( unImportedCharSet )
                except UnicodeDecodeError:
                    unosDatosCadenaActual[ 'symbol_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .properties' % unImportedCharSet   
                    unosDatosCadenaActual[ 'symbol_error_line'] = unNextLineIndex
                    
                if unSymbolStringUnicode:
                    
                    unosDatosCadenaActual[ 'symbol_unicode'] = unSymbolStringUnicode
                    unSymbolStringEncoded  = ''
                    try:
                        unSymbolStringEncoded =  aTranslationService.encode( unSymbolStringUnicode)      
                    except:
                        unosDatosCadenaActual[ 'symbol_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .properties'   
                        unosDatosCadenaActual[ 'symbol_error_line'] = unNextLineIndex
   
                    if unSymbolStringEncoded:    
                        unosDatosCadenaActual[ 'symbol_encoded'] = unSymbolStringEncoded                
                
                
                unaCadenaTraducida  = unaLinea[ unSeparatorIndex + 1:].strip()
                
                
                if unaCadenaTraducida:
                    
                    unosDatosCadenaActual[ 'translation_raw'] = unaCadenaTraducida
                    
                    unaTraduccionUnicode = u''
                    try:
                        unaTraduccionUnicode = unaCadenaTraducida.decode( unImportedCharSet)
                    except UnicodeDecodeError:
                        unosDatosCadenaActual[ 'translation_error'] = 'gvSIGi18n ERROR: UnicodeDecodeError from charset %s: in .properties' % unImportedCharSet  
                    
                    if unaTraduccionUnicode:
                        unosDatosCadenaActual[ 'translation_unicode'] = unaTraduccionUnicode
                        
                        unaTraduccionEncoded  = ''
                        try:
                            unaTraduccionEncoded =  aTranslationService.encode( unaTraduccionUnicode)      
                        except:
                            unosDatosCadenaActual[ 'translation_error'] = 'gvSIGi18n ERROR: encode error to plone default charset in .properties'   
                        
                        if unaTraduccionEncoded:    
                            unosDatosCadenaActual[ 'translation_encoded'] = unaTraduccionEncoded
                                                    
                continue        
                        

                    
              
        return self
   
    
    
                        
    

    
    