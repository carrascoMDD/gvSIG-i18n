# -*- coding: utf-8 -*-
#
# File: TRAImportacion_Operaciones_Parse.py
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
from TRAImportarExportar_Constants_JavaProperties import *



from TRAColeccionSolicitudesCadenas_Operaciones import cEstadoSolicitudCadena_Pending

from TRAProcessErrorException import TRAProcessErrorException

from TRAImportacion_Operaciones_Parse_GNUgettextPO   import TRAImportacion_Operaciones_Parse_GNUgettextPO
from TRAImportacion_Operaciones_Parse_JavaProperties import TRAImportacion_Operaciones_Parse_JavaProperties


class TRAImportacion_Operaciones_Parse( \
    TRAImportacion_Operaciones_Parse_GNUgettextPO,\
    TRAImportacion_Operaciones_Parse_JavaProperties,\
    ):    
    """
    """
    security = ClassSecurityInfo()
     


     
    

    
    security.declarePrivate( 'fNewVoidImportCursor')    
    def fNewVoidImportCursor( self,):
        unCursor = {
            'file_kind':                '',
            'language':                 '',
            'content_lines':            [],
            'max_number_of_lines':      -1,
            'num_lines':                0,
            'next_line_index':          0,
            'num_possible_records':     0,
            'timestamp':                '',
            'error':                    '',
            'error_detail':             '',
            'charset':                  '',
            'exceeded_max_number_of_lines': False,
        }
        return unCursor
    
    
    

        
    
    
    security.declarePrivate( 'fNewVoidCursorRecord')    
    def fNewVoidCursorRecord( self):
        unRecord = {
            'syntax_error':         False,
            'syntax_error_recoverable': True,
            
            'symbol_error':         False, 
            'symbol_error_line':    None,
            
            'empty_symbol':         False, # As in the header of GNU gettext .PO files, with an initial comment line, empty msgid and msgstr lines, followed by quoted lines (as part of msgstr)
            'symbol_raw':           '',
            'symbol_unicode':       u'',
            'symbol_encoded':       '',
            
            'continuable_translation':    False, # As in the header of GNU gettext .PO files, with an initial comment line, empty msgid and msgstr lines, followed by quoted lines (as part of msgstr)
            
            'translation_raw':      '',
            'translation_unicode':  u'',
            'translation_encoded':  '',
            'translation_error':    '',
            
            'default_raw':          u'',
            'default_unicode':      u'',
            'default_encoded':      '',
            'default_error':        '',
            
            'modules_raw':          u'',
            'modules_unicode':      u'',
            'modules_encoded':      '',
            'modules_error':        '',

            'status_raw':          u'',
            'status_unicode':      u'',
            'status_encoded':      '',
            'status_error':        '',
                        
            'sources_raw':          u'',
            'sources_unicode':      u'',
            'sources_encoded':      '',
            'sources_error':        '',
            
            'flags_raw':          u'',
            'flags_unicode':      u'',
            'flags_encoded':      '',
            'flags_error':        '',
            
            'comment_raw':          u'',
            'comment_unicode':      u'',
            'comment_encoded':      '',
            'comment_error':        '',
            
            'creation_date_raw':          u'',
            'creation_date_unicode':      u'',
            'creation_date_encoded':      '',
            'creation_date_error':        '',
        
            'creator_raw':          u'',
            'creator_unicode':      u'',
            'creator_encoded':      '',
            'creator_error':        '',
        
            'translation_date_raw':          u'',
            'translation_date_unicode':      u'',
            'translation_date_encoded':      '',
            'translation_date_error':        '',
           
            'translator_raw':          u'',
            'translator_unicode':      u'',
            'translator_encoded':      '',
            'translator_error':        '',
        
            'review_date_raw':          u'',
            'review_date_unicode':      u'',
            'review_date_encoded':      '',
            'review_date_error':        '',
        
            'reviewer_raw':          u'',
            'reviewer_unicode':      u'',
            'reviewer_encoded':      '',
            'reviewer_error':        '',
            
            'definitive_date_raw':          u'',
            'definitive_date_unicode':      u'',
            'definitive_date_encoded':      '',
            'definitive_date_error':        '',
        
            'coordinator_raw':          u'',
            'coordinator_unicode':      u'',
            'coordinator_encoded':      '',
            'coordinator_error':        '',
        
        }
        return unRecord
    
    
 
    
    
    security.declarePrivate( 'fNewVoidInformeImportarContenidos')    
    def fNewVoidInformeImportarContenidos( self):
        unInforme = {
            'valid':                    True,
            'start_date':               '',
            'end_date':                 '',
            'fecha_informe':            '',
            'modules_to_create':        0,
            'module_creations':         0,
            'languages_to_create':      0,
            'language_creations':       0,
            'strings_to_process':       0,
            'processed_strings':        0,
            'translations_to_process':  0,
            'processed_translations':   0,
            'strings_to_create':        0,
            'string_creations':         0,
            'string_module_changes':    0,
            'string_sources_changes':    0,
            'translation_status_changes':    0,
            'translation_creations':    0,
            'translation_creations_as_pending':    0,
            'translation_changes':      0,
            'translations_unchanged':   0,
            'translations_ignored':     0,
            'strings_to_complete':      0,
            'strings_completed':        0,
            'translations_completed':   0,
            'total_changes':            0,
            'expected_operations':      0,
            'operations_done':          0,
            'error':                    '',
            'error_detail':             '',
            'translations_to_create_in_new_languages_for_preexisting_strings': 0,
            'translations_created_in_new_languages_for_preexisting_strings': 0,
            'missing_translations_creation':    self.fNewVoidInformeCrearTraduccionesQueFaltan(),
        }
        return unInforme

    

    
    
    
    security.declarePrivate( 'fNewVoidInformeCrearTraduccionesQueFaltan')    
    def fNewVoidInformeCrearTraduccionesQueFaltan( self):
        unInforme = {
            'valid':                    True,
            'fecha_informe':            '',
            'start_date':               '',
            'end_date':                 '',
            'strings_to_complete':      0,
            'strings_completed':        0,
            'translations_created':     0,
            'expected_operations':      0,
            'operations_done':          0,
            'error':                    '',
            'error_detail':             '',
        }
        return unInforme

            

    
        
                       

    
    security.declarePrivate( 'fContenidosDeUploadedFile')    
    def fContenidosDeUploadedFile( self,
        theParentExecutionRecord =None, 
        theUploadedFile         =None, 
        theDefaultLanguage      ='',
        theAdditionalParams     =None):
        """SCAN AND  ANALYZE CONTENT TO BE IMPORTED.
        
        """
         
        unExecutionRecord = self.fStartExecution( 'method',  'fContenidosDeUploadedFile', theParentExecutionRecord, False) 

        try:
            todosContenidos = [ ]

            
            if not theUploadedFile:
                return todosContenidos
                        
            
            
            # Determine if theUploadedFile is a zip or jar archive content
            unIsZip = False
            unZipFile = None
            try:
                unZipFile = ZipFile( theUploadedFile)  
            except:
                None
            if unZipFile:
                # Error if True
                if not( unZipFile.testzip()):
                    unIsZip = True
            
                    
                    
            if not unIsZip:
                
                return self.fContenidosDeUploadedFile_NoNestedZips( 
                    theParentExecutionRecord=unExecutionRecord, 
                    theUploadedFile         =theUploadedFile, 
                    theDefaultLanguage      =theDefaultLanguage,
                    theAdditionalParams     =theAdditionalParams)
            
            
            
            
            aMustProcessWholeZipAsSingleFile = False
            
            someFileNames = unZipFile.namelist()
            
            for aFullFileName in someFileNames:
                
                aBaseName = os.path.basename( aFullFileName)
                
                if aBaseName:
                    
                    aBaseNameLower = aBaseName.lower()
                    aBaseNamePostfix = os.path.splitext(  aBaseNameLower)[ 1]
                    
                    if not( aBaseNamePostfix == cZipFilePostfix.lower()):
                        
                        aMustProcessWholeZipAsSingleFile = True
                        
                    else:
                        
                        unContentData = unZipFile.read( aFullFileName)   
                        
                        if unContentData:
                            
                            unZipBuffer      = StringIO( unContentData)
                            
                            someContenidos = self.fContenidosDeUploadedFile_NoNestedZips( 
                                theParentExecutionRecord=unExecutionRecord, 
                                theUploadedFile         =unZipBuffer, 
                                theDefaultLanguage      =theDefaultLanguage,
                                theAdditionalParams     =theAdditionalParams)
                            
                            if someContenidos:
                                todosContenidos.extend( someContenidos)
                
                                
                                
                                
            if aMustProcessWholeZipAsSingleFile:
                
                someContenidos = self.fContenidosDeUploadedFile_NoNestedZips( 
                    theParentExecutionRecord=unExecutionRecord, 
                    theUploadedFile         =theUploadedFile, 
                    theDefaultLanguage      =theDefaultLanguage,
                    theAdditionalParams     =theAdditionalParams)
                
                if someContenidos:
                    todosContenidos.extend( someContenidos)
                            
            return todosContenidos
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()


                
                


                         

    
    security.declarePrivate( 'fContenidosDeUploadedFile_NoNestedZips')    
    def fContenidosDeUploadedFile_NoNestedZips( self,
        theParentExecutionRecord =None, 
        theUploadedFile         =None, 
        theDefaultLanguage      ='',
        theAdditionalParams     =None):
                                  
         
        unExecutionRecord = self.fStartExecution( 'method',  'fContenidosDeUploadedFile_NoNestedZips', theParentExecutionRecord, False) 

        try:
            unosContenidos = [ ]

            if not theUploadedFile:
                return unosContenidos
            
            aImportarNombreModuloDesdeDominioONombreFichero =  theAdditionalParams.get( 'theImportModuleNameFromDomainOrFilename', None) == True
            
                        
            # Determine if theUploadedFile is a zip or jar archive content
            unIsZip = False
            unZipFile = None
            try:
                unZipFile = ZipFile( theUploadedFile)  
            except:
                None
            if unZipFile:
                # True result indicates error
                if not( unZipFile.testzip()):
                    unIsZip = True
            
            someUploadedEntries = []
            
            if unIsZip:
                
                someUploadedEntries = self.fUploadedEntriesFromZipFileManifest(   
                    theParentExecutionRecord =theParentExecutionRecord, 
                    theZipFile              =unZipFile, 
                    theAdditionalParams     =theAdditionalParams                    
                )
                if not someUploadedEntries:
                    
                    someUploadedEntries = self.fUploadedEntriesFromZipFileLocalesCSV(  
                        theParentExecutionRecord =theParentExecutionRecord, 
                        theZipFile               =unZipFile, 
                        theAdditionalParams      =theAdditionalParams,
                    )
                    if not someUploadedEntries:
                        
                        someUploadedEntries = self.fUploadedEntriesFromZipFileDirectory( 
                            theParentExecutionRecord =theParentExecutionRecord, 
                            theZipFile              =unZipFile, 
                            theDefaultLanguage      =theDefaultLanguage,
                            theAdditionalParams     =theAdditionalParams ,
                        )
            else:        
                
                anUploadedEntry = self.fUploadedEntryFromNonZipFile( 
                    theParentExecutionRecord =theParentExecutionRecord, 
                    theUploadedFile          =theUploadedFile, 
                    theAdditionalParams      =theAdditionalParams ,
                )
                
                if anUploadedEntry:
                    
                    someUploadedEntries = [ anUploadedEntry, ]   
                    
                    
                    
                        
            for unUploadedEntry in someUploadedEntries:
                

                if unUploadedEntry[ 'file_kind'] == cPropertiesFilePostfix:
                    
                    
                    if  unUploadedEntry[ 'is_reference']:
                        continue
                    
                    
                    unUploadedContent = self.fNewVoidUploadedContent( )
                    unosContenidos.append( unUploadedContent)
                    
                    unUploadedContent [ 'uploaded_entries'].append( unUploadedEntry)                    
                    
                    unFileName = unUploadedEntry[ 'file_name']
                    unDirName  = os.path.dirname(  unFileName)
                    if unDirName:
                        unUploadedEntry[ 'module'] = unDirName
                    else:
                        unUploadedEntry[ 'module'] = unUploadedEntry.get( 'module', '')
                    
                    self.pScanTranslationsProperties( 
                        theParentExecutionRecord , 
                        theUploadedFile, 
                        unZipFile, 
                        unUploadedContent, 
                        unUploadedEntry, 
                        theAdditionalParams,
                    )

                    
                    
                    
                    
                elif unUploadedEntry[ 'file_kind'] == cPOFilePostfix:
                    
                    
                    unUploadedContent = self.fNewVoidUploadedContent( )
                    unosContenidos.append( unUploadedContent)
                    
                    unUploadedContent [ 'uploaded_entries'].append( unUploadedEntry)
                    
                    if aImportarNombreModuloDesdeDominioONombreFichero:
                        if unUploadedEntry[ 'domain']:
                            unUploadedEntry[ 'module'] = unUploadedEntry[ 'domain']     
                        
                    self.pScanTranslationsPO( 
                        theParentExecutionRecord, 
                        theUploadedFile, 
                        unZipFile, 
                        unUploadedContent, 
                        unUploadedEntry, 
                        theAdditionalParams,
                    )
                                         
            return unosContenidos
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()


                
                
                
            
                
    security.declarePrivate( 'fUploadedEntriesFromZipFileManifest')    
    def fUploadedEntriesFromZipFileManifest( self,
        theParentExecutionRecord =None, 
        theZipFile              =None, 
        theAdditionalParams     =None):
                
        unExecutionRecord = self.fStartExecution( 'method',  'fUploadedEntriesFromZipFileManifest', theParentExecutionRecord, False) 

        try:
                
            if not theZipFile:
                return []
            
            if not( cManifestFileFullName in theZipFile.namelist()):
                return []

            unContentData = None
            unReadError = False
            try:
                unContentData = theZipFile.read( cManifestFileFullName)
            except:
                return []
            
            if not unContentData:
                return []
        
            someLines = unContentData.splitlines()            
            unNumLines = len( someLines)
                    
            if unNumLines < 1:
                return []

            someUploadedEntries = []
            
            aDefaultModule = theAdditionalParams.get( 'theDefaultModule', '')
            
            unLineIndex = 0
            unUploadedEntry = None
            while unLineIndex < unNumLines:
                
                unaLine =  someLines[ unLineIndex].strip()
                unLineIndex += 1     
                if not unaLine:
                    unUploadedEntry = None
                    continue
         
                if unaLine.startswith( cManifestEntryStartLinePrefix):
                    
                    unFileName = unaLine[ len( cManifestEntryStartLinePrefix):].strip()
                    
                    if unFileName:
                        if not( unFileName.lower().endswith( cPropertiesFilePostfix.lower()) or unFileName.lower().endswith( cPOFilePostfix.lower()) or unFileName.lower().endswith( cPOTFilePostfix.lower())):
                            unUploadedEntry = None
                            
                        else:
                            
                            unUploadedEntry = self.fNewVoidUploadedEntry()
                            someUploadedEntries.append( unUploadedEntry)
                            unUploadedEntry[ 'file_name']       = unFileName
                            unUploadedEntry[ 'in_zip']          = True
                            
                            if unFileName.lower().endswith( cPropertiesFilePostfix.lower()):
                                
                                unUploadedEntry[ 'file_kind'] = cPropertiesFilePostfix
                                unModuleName, aVoidLanguage, aVoidCountry = self.fModuleLocaleLanguageAndCountryFromPropertiesFileName( unFileName, aDefaultModule, '')
                                
                                if  unModuleName:
                                    unUploadedEntry[ 'module'] = unModuleName
                                    
                                    
                            elif unFileName.lower().endswith( cPOFilePostfix.lower()):
                                
                                unUploadedEntry[ 'file_kind'] = cPOFilePostfix
                                
                                
                            elif unFileName.lower().endswith( cPOTFilePostfix.lower()):
                                
                                unUploadedEntry[ 'file_kind']   = cPOFilePostfix
                                unUploadedEntry[ 'is_pot_file'] = True
                                unUploadedEntry[ 'language']    = theAdditionalParams.get( 'theDefaultLanguage', '')
                                unUploadedEntry[ 'country']     = ''
                                unUploadedEntry[ 'language_and_country']  = theAdditionalParams.get( 'theDefaultLanguage', '')
                                
                                
                elif unUploadedEntry:
                    
                    if unaLine.startswith( cManifestLocaleLanguageStartLinePrefix):
                        
                        unLocaleLanguage = unaLine[ len( cManifestLocaleLanguageStartLinePrefix):].strip()
                        
                        if unLocaleLanguage:
                            
                            unUploadedEntry[ 'is_reference']    = False
                            unUploadedEntry[ 'language']        = unLocaleLanguage
                            
                            if unUploadedEntry[ 'country']:
                                unUploadedEntry[ 'language_and_country']         = '%s-%s' % ( unLocaleLanguage, unUploadedEntry[ 'country'], )
                            else:
                                unUploadedEntry[ 'language_and_country']         = unLocaleLanguage
                                
                                
                                
                    elif unaLine.startswith( cManifestLocaleCountryStartLinePrefix):
                        
                        unLocaleCountry = unaLine[ len( cManifestLocaleCountryStartLinePrefix):].strip()
                        
                        if unLocaleCountry:
                            
                            unUploadedEntry[ 'country'] = unLocaleCountry
                            if unUploadedEntry[ 'language']:
                                unUploadedEntry[ 'language_and_country']         = '%s-%s' % ( unUploadedEntry[ 'language'], unLocaleCountry, )
                            else:
                                unUploadedEntry[ 'language_and_country'] = '-%s' % unLocaleCountry
                                
                                
                    elif unaLine.startswith( cManifestReferenceLocaleLanguageStartLinePrefix):
                        
                        unReferenceLocaleLanguage = unaLine[ len( cManifestReferenceLocaleLanguageStartLinePrefix):].strip()
                        
                        if unReferenceLocaleLanguage:
                            
                            unUploadedEntry[ 'is_reference']    = True
                            unUploadedEntry[ 'language']        = unReferenceLocaleLanguage
                            if unUploadedEntry[ 'country']:
                                unUploadedEntry[ 'language_and_country']         = '%s-%s' % ( unReferenceLocaleLanguage, unUploadedEntry[ 'country'], )
                            else:
                                unUploadedEntry[ 'language_and_country'] = unReferenceLocaleLanguage
                            
                                
                    elif unaLine.startswith( cManifestReferenceLocaleCountryStartLinePrefix):
                        
                        unReferenceLocaleCountry = unaLine[ len( cManifestReferenceLocaleCountryStartLinePrefix):].strip()
                        
                        if unReferenceLocaleCountry:
                            
                            unUploadedEntry[ 'is_reference']    = True
                            unUploadedEntry[ 'country'] = unReferenceLocaleCountry
                            if unUploadedEntry[ 'language']:
                                unUploadedEntry[ 'language_and_country']         = '%s-%s' % ( unUploadedEntry[ 'language'], unReferenceLocaleCountry, )
                            else:
                                unUploadedEntry[ 'language_and_country'] = '-%s' % unReferenceLocaleCountry
                       
                    
            
            return someUploadedEntries
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()



               
            
                
    security.declarePrivate( 'fUploadedEntriesFromZipFileLocalesCSV')    
    def fUploadedEntriesFromZipFileLocalesCSV( self,
        theParentExecutionRecord =None, 
        theZipFile              =None, 
        theAdditionalParams     =None):
                
        unExecutionRecord = self.fStartExecution( 'method',  'fUploadedEntriesFromZipFileLocalesCSV', theParentExecutionRecord, False) 

        try:
                
            if not theZipFile:
                return []
            
            if not( cLocalesCSVFileFullName in theZipFile.namelist()):
                return []

            unContentData = None
            unReadError = False
            try:
                unContentData = theZipFile.read( cLocalesCSVFileFullName)
            except:
                return []
            
            if not unContentData:
                return []
        
            someLines = unContentData.splitlines()            
            unNumLines = len( someLines)
                    
            if unNumLines < 1:
                return []

            someUploadedEntries = []
            
            aDefaultModule = theAdditionalParams.get( 'theDefaultModule', '')
            
            unLineIndex = 0
            while unLineIndex < unNumLines:
                unaLine =  someLines[ unLineIndex].strip()
                unLineIndex += 1     
                if not unaLine:
                    continue
                
                unFileName        = ''
                unLocaleLanguage  = ''
                unLocaleCountry   =  ''
                unLocaleVariation = ''
                unIsReference     = False
                
                unosLineFields = unaLine.split( ',')
                unNumFields = len( unosLineFields)
                if unNumFields > 0:
                    unFileName = unosLineFields[ 0]
                    if unFileName:
                        if not( unFileName.lower().endswith( cPropertiesFilePostfix.lower()) or unFileName.lower().endswith( cPOFilePostfix.lower()) or unFileName.lower().endswith( cPOTFilePostfix.lower())):
                            continue
                        else:
                            
                            if unNumFields > 0:
                                unLocaleLanguage  = unosLineFields[ 1].lower()  
                            if unNumFields > 1:
                                unLocaleCountry  = unosLineFields[ 2].lower()  
                            if unNumFields > 2:
                                unLocaleVariation  = unosLineFields[ 3].lower()  
                            if unNumFields > 3:
                                unIsReferenceString  = unosLineFields[ 4]  
                                unIsReference = unIsReferenceString.lower() == cLocalesCSVIsReferenceFile.lower()
                            
                            if not unLocaleLanguage:
                                continue
                            else:
                                
                                # #############################################
                                """Determine if an entry for the file already exists, which may happen if there are CSV records for the same file as both a language to translate and a reference language.
                                
                                """
                                
                                for otherUploadedEntry in someUploadedEntries:
                                    
                                    otherFileName = otherUploadedEntry.get( 'file_name', '')
                                    if otherFileName == unFileName:
                                        
                                        otherIsReference = otherUploadedEntry.get( 'is_reference', False) 
                                        if otherIsReference:
                                            if not unIsReference:
                                                someUploadedEntries.remove( otherUploadedEntry)
                                            else:
                                                continue
                                        else:
                                            continue
                                
                                
                                        
                                # #############################################
                                """Create entry for the file.
                                
                                """
                                        
                                unUploadedEntry = self.fNewVoidUploadedEntry()
                                someUploadedEntries.append( unUploadedEntry)
                                
                                unModuleName, aVoidLanguage, aVoidCountry = self.fModuleLocaleLanguageAndCountryFromPropertiesFileName( unFileName, aDefaultModule, '')
                                
                                unUploadedEntry[ 'file_name']       = unFileName
                                unUploadedEntry[ 'in_zip']          = True
                                unUploadedEntry[ 'is_reference']    = unIsReference
                                unUploadedEntry[ 'language']        = unLocaleLanguage
                                unUploadedEntry[ 'country']         = unLocaleCountry
                                if unModuleName:
                                    unUploadedEntry[ 'module']      = unModuleName
                                
                                if unLocaleCountry:
                                    unUploadedEntry[ 'language_and_country']  = '%s-%s' % ( unLocaleLanguage, unLocaleCountry,)
                                else:
                                    unUploadedEntry[ 'language_and_country']  = '%s' % unLocaleLanguage
                                    
                                if unFileName.lower().endswith( cPropertiesFilePostfix.lower()):
                                    unUploadedEntry[ 'file_kind'] = cPropertiesFilePostfix
                                elif unFileName.lower().endswith( cPOFilePostfix.lower()):
                                    unUploadedEntry[ 'file_kind'] = cPOFilePostfix
                                elif unFileName.lower().endswith( cPOTFilePostfix.lower()):
                                    unUploadedEntry[ 'file_kind']   = cPOFilePostfix
                                    unUploadedEntry[ 'is_pot_file'] = True
                                    
                                
            
            return someUploadedEntries
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()



        
     
                
                
                
    security.declarePrivate( 'fUploadedEntriesFromZipFileDirectory')    
    def fUploadedEntriesFromZipFileDirectory( self,
        theParentExecutionRecord =None, 
        theZipFile              =None, 
        theDefaultLanguage      ='',
        theAdditionalParams     =None):
                
        unExecutionRecord = self.fStartExecution( 'method',  'fUploadedEntriesFromZipFileDirectory', theParentExecutionRecord, False) 

        try:
                
            if not theZipFile:
                return []
            
            aDefaultLanguage = theDefaultLanguage
            if not aDefaultLanguage:
                aDefaultLanguage = theAdditionalParams.get( 'theDefaultLanguage', '')
                            
            aDefaultModule   = theAdditionalParams.get( 'theDefaultModule',   '')

            someUploadedEntries = []
            
            someFileNames = theZipFile.namelist()
            for aFullFileName in someFileNames:
                
                unUploadedEntry = None
                unLocaleLanguage = ''
                unLocaleCountry = ''
                
                aBaseName = os.path.basename( aFullFileName)
                if aBaseName:
                    aBaseNameLower = aBaseName.lower()
                    aBaseNamePostfix = os.path.splitext(  aBaseNameLower)[ 1]
                    if not ( aBaseNameLower in [ cManifestFileFullName.lower(), cLocalesCSVFileFullName.lower(),]):
                         
                        if aBaseNamePostfix == cPropertiesFilePostfix.lower():

                            aModuleName, unLocaleLanguage, unLocaleCountry = self.fModuleLocaleLanguageAndCountryFromPropertiesFileName( aBaseName, aDefaultModule, aDefaultLanguage)
   
                            if unLocaleLanguage:
                                
                                unUploadedEntry = self.fNewVoidUploadedEntry()
                                unUploadedEntry[ 'in_zip']    = True
                                unUploadedEntry[ 'file_name'] = aFullFileName
                                unUploadedEntry[ 'file_kind'] = cPropertiesFilePostfix
                                
                                if aModuleName:
                                    unUploadedEntry[ 'module']    = aModuleName
                                    
                                unUploadedEntry[ 'language']  = unLocaleLanguage.lower()
                                
                                if unLocaleCountry:
                                    unUploadedEntry[ 'country']                 = unLocaleCountry.lower()
                                    unUploadedEntry[ 'language_and_country']    = '%s-%s' % ( unLocaleLanguage.lower(), unLocaleCountry.lower(), )
                                else:
                                    unUploadedEntry[ 'country']                 = ''
                                    unUploadedEntry[ 'language_and_country']    = unLocaleLanguage.lower()
                                      
                        elif aBaseNamePostfix in [  cPOFilePostfix.lower(), cPOTFilePostfix.lower(),]:
                      
                            unPOHeader = self.fPOHeaderFromZipPOFile( theParentExecutionRecord, theZipFile, aFullFileName) 
                            
                            if unPOHeader:
                                
                                unHeaderLastLineNumber = unPOHeader.get( 'last_line_number', -1)
                                unLocaleLanguage = unPOHeader.get( 'language_code', '')
                                unLocaleCountry  = unPOHeader.get( 'country', '')
                                unCharset        = unPOHeader.get( 'charset', '')
                                unIsFallbackFor  = unPOHeader.get( 'is_fallback_for', '')
                                unDomain         = unPOHeader.get( 'domain', '')
                                
                                if not unLocaleLanguage:
                                    unLocaleLanguage = aDefaultLanguage.lower()
                                    
                                if not unDomain:
                                    unDomain = theAdditionalParams.get( 'theDefaultModule', '')
                                    
                                if unCharset:
                                    unCharSetExists = True
                                    try:
                                        aVoid = ''.decode( unCharset )
                                    except:
                                        unCharSetExists = False
                                        
                                    if not unCharSetExists:
                                        unCharset = 'utf-8'
                                else:
                                    unCharset = 'utf-8'
                                    
                                if unLocaleLanguage:
                                    
                                    unUploadedEntry = self.fNewVoidUploadedEntry()
                                    unUploadedEntry[ 'in_zip']          = True                                
                                    unUploadedEntry[ 'file_name']       = aFullFileName
                                    unUploadedEntry[ 'file_kind']       = cPOFilePostfix
                                    unUploadedEntry[ 'charset']         = unCharset
                                    unUploadedEntry[ 'is_fallback_for'] = unIsFallbackFor
                                    unUploadedEntry[ 'domain']          = unDomain
                                    unUploadedEntry[ 'last_header_line_number']        = unHeaderLastLineNumber
                                    
                                    if unLocaleCountry:
                                        unUploadedEntry[ 'country']                 = unLocaleCountry
                                        unUploadedEntry[ 'language_and_country']    = '%s-%s' % ( unLocaleLanguage, unLocaleCountry, )
                                    else:
                                        unUploadedEntry[ 'country']                 = ''
                                        unUploadedEntry[ 'language_and_country']    = unLocaleLanguage

                                    if aBaseNamePostfix == cPOTFilePostfix.lower():
                                        unUploadedEntry[ 'is_pot_file'] = True
                                        unUploadedEntry[ 'language']    = self.getCodigoIdiomaPorDefecto()
                                        unUploadedEntry[ 'country']     = ''
                                        unUploadedEntry[ 'language_and_country']  = unLocaleLanguage or self.getCodigoIdiomaPorDefecto()
                                        
                                        
                        
                if unUploadedEntry:
                    someUploadedEntries.append( unUploadedEntry)
                        
            return someUploadedEntries
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

                

            
  
    
    
    security.declarePrivate( 'fZipFileElementContent')    
    def fZipFileElementContent( self, theZipFile, theFileName):
  
        if not theFileName or not theZipFile:
            return None
        
        unContent = None
        try:
            unContent = theZipFile.read( theFileName)
        except:
            return None
        return unContent
    
    
    

    
                
                
        
    security.declarePrivate( 'fUploadedEntryFromNonZipFile')    
    def fUploadedEntryFromNonZipFile( self,
        theParentExecutionRecord =None, 
        theUploadedFile         =None, 
        theAdditionalParams     =None):
                    
        unExecutionRecord = self.fStartExecution( 'method',  'fUploadedEntryFromNonZipFile', theParentExecutionRecord, False) 

        try:

            theUploadedFile.seek( 0)
            unContent = theUploadedFile.read()
            
            unPOHeader = self.fPOHeaderFromPOContent( theParentExecutionRecord, unContent)        
            if unPOHeader:
                unLocaleLanguage = unPOHeader.get( 'language_code', '')
                if not unLocaleLanguage:
                    unLocaleLanguage = theAdditionalParams.get( 'theDefaultLanguage', '')
                    
                unLocaleCountry  = unPOHeader.get( 'country', '')
                unCharset        = unPOHeader.get( 'charset', '')
                unCharSetExists = True
                try:
                    aVoid = ''.decode( unCharset )
                except:
                    unCharSetExists = False
                    
                if not unCharSetExists:
                    unCharset = 'utf-8'
                    
                
                unIsFallbackFor  = unPOHeader.get( 'is_fallback_for', '')
                unDomain         = unPOHeader.get( 'domain', '')
                unHeaderLastLineNumber = unPOHeader.get( 'last_line_number', -1)
                
                aFileName = ''
                try:
                    aFileName = theUploadedFile.filename
                except:
                    None
                if not aFileName:
                    aFileName = cPOUnknownFileName      
                
                                

                if unLocaleLanguage:
                    
                    unUploadedEntry = self.fNewVoidUploadedEntry()
                    
                    if aFileName.lower().endswith( cPOTFilePostfix.lower()):
                        unUploadedEntry[ 'is_pot_file'] = True

                    unUploadedEntry[ 'in_zip']          = False                                
                    unUploadedEntry[ 'file_name']       = aFileName
                    unUploadedEntry[ 'file_kind']       = cPOFilePostfix
                    unUploadedEntry[ 'charset']         = unCharset
                    unUploadedEntry[ 'is_fallback_for'] = unIsFallbackFor
                    unUploadedEntry[ 'domain']          = unDomain
                    unUploadedEntry[ 'language']        = unLocaleLanguage
                    unUploadedEntry[ 'last_header_line_number']        = unHeaderLastLineNumber
                    
                    if unLocaleCountry:
                        unUploadedEntry[ 'country']                 = unLocaleCountry
                        unUploadedEntry[ 'language_and_country']    = '%s-%s' % ( unLocaleLanguage, unLocaleCountry, )
                    else:
                        unUploadedEntry[ 'country']                 = ''
                        unUploadedEntry[ 'language_and_country']    = unLocaleLanguage
                    return unUploadedEntry
            
            
                
            aFileName = ''
            try:
                aFileName = theUploadedFile.filename
            except:
                None
            if not aFileName:
                aFileName = cPropertiesUnknownFileName  
            
            aDefaultModule   = theAdditionalParams.get( 'theDefaultModule',   '')
            aDefaultLanguage = theAdditionalParams.get( 'theDefaultLanguage', '')
                
                
            aModuleName, unLocaleLanguage, unLocaleCountry = self.fModuleLocaleLanguageAndCountryFromPropertiesFileName( aFileName, aDefaultModule, aDefaultLanguage)                
            if not unLocaleLanguage:
                unLocaleLanguage, unLocaleCountry = self.fLocaleLanguageAndCountryFromPropertiesContent( theParentExecutionRecord, unContent)   
            
            if not unLocaleLanguage:
                return None
                
            unUploadedEntry = self.fNewVoidUploadedEntry()
            unUploadedEntry[ 'in_zip']    = False
            unUploadedEntry[ 'file_name'] = aFileName
            unUploadedEntry[ 'file_kind'] = cPropertiesFilePostfix
            unUploadedEntry[ 'module']    = aModuleName
            unUploadedEntry[ 'language']  = unLocaleLanguage
            if unLocaleCountry:
                unUploadedEntry[ 'country']                 = unLocaleCountry
                unUploadedEntry[ 'language_and_country']    = '%s-%s' % ( unLocaleLanguage, unLocaleCountry, )
            else:
                unUploadedEntry[ 'country']                 = ''
                unUploadedEntry[ 'language_and_country']    = unLocaleLanguage
            return unUploadedEntry
    
              
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

       
                                 
