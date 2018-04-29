# -*- coding: utf-8 -*-
#
# File: TRACatalogo_Exportacion_JavaProperties.py
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

import sys
import traceback
import logging

from codecs                 import lookup           as CODECS_Lookup
from codecs                 import EncodedFile      as CODECS_EncodedFile


from AccessControl          import ClassSecurityInfo

from Products.CMFCore       import permissions

from Products.CMFCore.utils import getToolByName


##code-section module-header #fill in your manual code here


from StringIO import StringIO

from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED



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
from TRAImportarExportar_Constants import *
from TRAImportarExportar_Constants_Encodings import *
from TRAImportarExportar_Constants_GNUgettextPO import *
from TRAImportarExportar_Constants_JavaProperties import *

from TRAElemento_Permission_Definitions import cBoundObject

from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_ImportTRAImportacion, cUseCase_Export, cUseCase_Backup_TRACatalogo, cUseCase_ExportGvSIG_TRAIdioma

##/code-section module-header


##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema



##code-section after-schema #fill in your manual code here


##/code-section after-schema

class TRACatalogo_Exportacion_JavaProperties:
    """
    """
    security = ClassSecurityInfo()


    
    
    
    
    ##code-section class-header #fill in your manual code here
    

    

    security.declarePrivate( 'fPropertiesFilenameIdiomaPostfix')    
    def fPropertiesFilenameIdiomaPostfix( self, theCodigoIdioma, theCodigoIdiomaPorDefecto):
        if not theCodigoIdioma:
            return ''
        
        if theCodigoIdioma == theCodigoIdiomaPorDefecto:
            return  ''
        
        return '_' + theCodigoIdioma.replace( cLanguageSeparatorCountry, cPropertiesFileCharBeforeCountry)
        
    
    
    
    def fNewVoidResultFicheroExportacionProperties( self,):
        unResult = {
            'file_kind':                                        '.properties',
            'success':                                          False,
            'status':                                           '',
            'encoding':                                         '',
            'encoding_error_handle_mode':                       '',
            'encoded_file_errors_mode':                         '',
            'system_to_unicode_errors_mode':                    '',
            'unicode_to_utf8_errors_mode':                      '',
            'contenido':                                        '',
            'total_encoding_errors':                            0,
            'header_error_codificacion_SystemToUnicode':        False,
            'header_error_codificacion_UnicodeToUTF':           False,
            'header_error_codificacion_Export':                 False,
            'simbolos_error_codificacion_SystemToUnicode':      [],
            'simbolos_error_codificacion_UnicodeToUTF':         [],
            'simbolos_error_codificacion_Export':               [],
            'traducciones_error_codificacion_SystemToUnicode':  [],
            'traducciones_error_codificacion_UnicodeToUTF':     [],
            'traducciones_error_codificacion_Export':           [],
            'sources_error_codificacion_SystemToUnicode':       [],
            'sources_error_codificacion_UnicodeToUTF':          [],
            'sources_error_codificacion_Export':                [],
            'modules_error_codificacion_SystemToUnicode':       [],
            'modules_error_codificacion_UnicodeToUTF':          [],
            'modules_error_codificacion_Export':                [],
        }
        return unResult
    

    

    

    
    
    
    
    
    
    
    # ####################################################
    """Java Properties output

    """
    
    security.declarePrivate( 'fWriteHeader_JavaProperties')    
    def fWriteHeader_JavaProperties( self, 
        theBuffer, 
        theResult,
        theIdioma, 
        theNombreModulo, 
        theCodificacionCaracteres,
        theEncodingErrorHandleMode, 
        theSystemToUnicodeErrorsMode,
        theUnicodeToUTF8ErrorsMode,
        theTranslationService):

        if not theResult:
            return False

        if not theIdioma or not theBuffer:
            theResult[ 'status'] = cResultCondition_Internal_MissingParameter    
            return False

        unCodigoIdioma = theIdioma.getCodigoIdiomaEnGvSIG()
        
        from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fDateTimeNow

        unaStringToWrite  = '%s%s]\n%s%s\n' % ( 
            cPrefixLineaLenguaje,  
            unCodigoIdioma,
            cPrefixLineaTimestamp, 
            str( self.fDateTimeNow()),
        )
        
        if theCodificacionCaracteres == cTRAEncodingUnicodeEscape:
            unStringToWriteEncoded, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                unaStringToWrite, 
                theTranslationService, 
                theSystemToUnicodeErrorsMode, 
            )
            
            if unEncodingErrorCondition:
                if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                    theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
                return False
        else: 
            unStringToWriteEncoded, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                unaStringToWrite, 
                theTranslationService, 
                theSystemToUnicodeErrorsMode, 
                theUnicodeToUTF8ErrorsMode
            )
            
            if unEncodingErrorCondition:
                if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                    theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
                elif unEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                    theResult[ 'header_error_codificacion_UnicodeToUTF'] = True    
                return False
            
        
        try:    
            theBuffer.write( unStringToWriteEncoded)
        except:
            theResult[ 'header_error_codificacion_Export'] = True 
            return False
           
        return True
    
    
                
    
    
          
            
    security.declarePrivate( 'fWriteTranslationResults_JavaProperties')    
    def fWriteTranslationResults_JavaProperties( self, 
        theBuffer, 
        theResult,
        theResultadosTraducciones, 
        theSourcesCadenasPorSimbolo,
        theExportModuleNames,
        theExportStringSources,
        theExportTranslationsStatus,
        theModulosCadenasPorSimbolo,
        theCodificacionCaracteres,
        theEncodingErrorHandleMode, 
        theSystemToUnicodeErrorsMode, 
        theUnicodeToUTF8ErrorsMode, 
        theTranslationService):


        if not theResult:
            return False

        if not theBuffer:
            theResult[ 'status'] = cResultCondition_Internal_MissingParameter    
            return False
        
        unCatalogo = self.getCatalogo()

        someEncodedTranslationsStatus = { }
        
        if theExportTranslationsStatus:

            # ######################################################################
            """Encode translation statuses.
            
            """              
            for aTranslationStatusToEncode in cTodosEstados:
                
                unTranslationStatusEncoded = ''
                
                if theCodificacionCaracteres == cTRAEncodingUnicodeEscape:
                    unTranslationStatusEncoded, unTranslationStatusErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                        aTranslationStatusToEncode, 
                        theTranslationService, 
                        theSystemToUnicodeErrorsMode, 
                    )
                    
                    if unTranslationStatusErrorCondition or not unTranslationStatusEncoded:
                        if unTranslationStatusErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                            theResult[ 'simbolos_error_codificacion_SystemToUnicode'] = True    
                        return False
                else: 
                    unTranslationStatusEncoded, unTranslationStatusErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                        aTranslationStatusToEncode, 
                        theTranslationService, 
                        theSystemToUnicodeErrorsMode, 
                        theUnicodeToUTF8ErrorsMode, 
                    )
                    if unTranslationStatusErrorCondition or not unTranslationStatusEncoded:
                        
                        if unTranslationStatusErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                            theResult[ 'simbolos_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
                            
                        elif unTranslationStatusErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                            theResult[ 'simbolos_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                    
                        if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False 

                        
                if not unTranslationStatusEncoded:
                    unTranslationStatusEncoded = aTranslationStatusToEncode
                    
                someEncodedTranslationsStatus[ aTranslationStatusToEncode] = unTranslationStatusEncoded
                    
                
        if theExportStringSources:
            # ######################################################################
            """Retrieve sources and module names for string symbols to export.
            
            """
            if ( not theSourcesCadenasPorSimbolo) or ( not theModulosCadenasPorSimbolo):
                
                for otroResultadoTraduccion in theResultadosTraducciones:
                    otroSimboloCadena   = otroResultadoTraduccion[ 'getSimbolo']
                    if otroSimboloCadena:
                        unaCadena = unCatalogo.fGetCadenaPorSimbolo( otroSimboloCadena)
                        if unaCadena:
                            unosSourcesCadena = unaCadena.getReferenciasFuentes()
                            theSourcesCadenasPorSimbolo[ otroSimboloCadena] = unosSourcesCadena
    
                            unosNombresModulosCadena = unaCadena.getNombresModulos()
                            theModulosCadenasPorSimbolo[ otroSimboloCadena] = unosNombresModulosCadena
        
        
        unHayError = False
        
        # ######################################################################
        """Loop over all string symbols to export.
        
        """
        for unResultadoTraduccion in theResultadosTraducciones:

            unHayErrorSimbolo        = False
            unHayErrorTraduccion     = False
            unHayErrorSources        = False
            unHayErrorSimbolo2       = False
            unHayErrorNombresModulos = False
            unHayErrorSimbolo3       = False
            unHayErrorSimbolo4       = False
            
            
            unSimboloCadena   = unResultadoTraduccion[ 'getSimbolo']
            unSimboloCadenaEncoded = ''
            
            if not unSimboloCadena:
                unHayErrorSimbolo = True
                continue
            
            # ######################################################################
            """Encode string symbol.
            
            """              
            if theCodificacionCaracteres == cTRAEncodingUnicodeEscape:
                unSimboloCadenaEncoded, unSimboloCadenaEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                    unSimboloCadena, 
                    theTranslationService, 
                    theSystemToUnicodeErrorsMode, 
                )
                
                if unSimboloCadenaEncodingErrorCondition or not unSimboloCadenaEncoded:
                    if unSimboloCadenaEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                        theResult[ 'simbolos_error_codificacion_SystemToUnicode'] = True    
                    return False
            else: 
                unSimboloCadenaEncoded, unSimboloCadenaEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                    unSimboloCadena, 
                    theTranslationService, 
                    theSystemToUnicodeErrorsMode, 
                    theUnicodeToUTF8ErrorsMode, 
                )
                if unSimboloCadenaEncodingErrorCondition or not unSimboloCadenaEncoded:
                    
                    if unSimboloCadenaEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                        theResult[ 'simbolos_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
                        
                    elif unSimboloCadenaEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                        theResult[ 'simbolos_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                
                    if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                        return False 
                    else:
                        unHayErrorSimbolo = True
                        unHayError = True
                        
                        
            # ######################################################################
            """Encode translation into main language.
            
            """
            unaCadenaTraducida     = unResultadoTraduccion[ 'getCadenaTraducida']
            unaCadenaTraducidaEncoded = ''
            
            if unaCadenaTraducida:
                if theCodificacionCaracteres == cTRAEncodingUnicodeEscape:
                    unaCadenaTraducidaEncoded, unaCadenaTraducidaEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                        unaCadenaTraducida, 
                        theTranslationService, 
                        theSystemToUnicodeErrorsMode, 
                    )
                    
                    if unaCadenaTraducidaEncodingErrorCondition or not unaCadenaTraducidaEncoded:
                        if unaCadenaTraducidaEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                            theResult[ 'simbolos_error_codificacion_SystemToUnicode'] = True    
                        return False
                else: 
                    
                    unaCadenaTraducidaEncoded, unaCadenaTraducidaEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                        unaCadenaTraducida, 
                        theTranslationService, 
                        theSystemToUnicodeErrorsMode, 
                        theUnicodeToUTF8ErrorsMode, 
                    )
                    if unaCadenaTraducidaEncodingErrorCondition or not unaCadenaTraducidaEncoded:
                        
                        if unaCadenaTraducidaEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                            theResult[ 'traducciones_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
        
                        elif unaCadenaTraducidaEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                            theResult[ 'traducciones_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                    
                        if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False
                        else:
                            unHayErrorTraduccion = True
                            unHayError =  True
             
                
                            

            if theExportStringSources:
                # ######################################################################
                """Encode sources.
                
                """
                unosSources = ''
                unosSourcesEncoded = ''
                
                unosSources        = theSourcesCadenasPorSimbolo.get( unSimboloCadena, '')
                if unosSources:
                    
                    if theCodificacionCaracteres == cTRAEncodingUnicodeEscape:
                        unosSourcesEncoded, unosSourcesEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                            unosSources, 
                            theTranslationService, 
                            theSystemToUnicodeErrorsMode, 
                        )
                        
                        if unosSourcesEncodedEncodingErrorCondition or not unosSourcesEncoded:
                            if unosSourcesEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                                theResult[ 'sources_error_codificacion_SystemToUnicode'] = True    
                            return False
                    else: 
                    
                        unosSourcesEncoded, unosSourcesEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                            unosSources, 
                            theTranslationService, 
                            theSystemToUnicodeErrorsMode, 
                            theUnicodeToUTF8ErrorsMode, 
                        )
                        if unosSourcesEncodedEncodingErrorCondition:
                            
                            unHayErrorSources = True
                            unHayError =  True
                            
                            if unosSourcesEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                                theResult[ 'sources_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
            
                            elif unosSourcesEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                                theResult[ 'sources_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                        
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False                   
                                    
                
                
            if theExportModuleNames:
                # ######################################################################
                """Encode module names.
                
                """
                unosNombresModulos = ''
                unosNombresModulosEncoded = ''
                
                unosNombresModulos        = theModulosCadenasPorSimbolo.get( unSimboloCadena, '')
                if unosNombresModulos:
                    
                    if theCodificacionCaracteres == cTRAEncodingUnicodeEscape:
                        unosNombresModulosEncoded, unosNombresModulosEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                            unosNombresModulos, 
                            theTranslationService, 
                            theSystemToUnicodeErrorsMode, 
                        )
                        
                        if unosNombresModulosEncodedEncodingErrorCondition or not unosNombresModulosEncoded:
                            if unosNombresModulosEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                                theResult[ 'modules_error_codificacion_SystemToUnicode'] = True    
                            return False
                    else: 
                    
                        unosNombresModulosEncoded, unosNombresModulosEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                            unosNombresModulos, 
                            theTranslationService, 
                            theSystemToUnicodeErrorsMode, 
                            theUnicodeToUTF8ErrorsMode, 
                        )
                        if unosNombresModulosEncodedEncodingErrorCondition:
                            
                            unHayErrorNombresModulos = True
                            unHayError =  True
                            
                            if unosNombresModulosEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                                theResult[ 'modules_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
            
                            elif unosNombresModulosEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                                theResult[ 'modules_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                        
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False                   
                                    
                                            
                
                            
            # ######################################################################
            """Write line with string symbol and translation.
            
            """                        
            if ( not unHayErrorSimbolo) and unSimboloCadenaEncoded:
                
                try:    
                    theBuffer.write( unSimboloCadenaEncoded)
                except:
                    theResult[ 'simbolos_error_codificacion_Export'].append( unSimboloCadena)    
                    if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                        return False
                    else:
                        unHayErrorSimbolo = True
                        unHayError =  True
                    
                theBuffer.write( cPropertyNameValueSeparator )
                        
                if ( not unHayErrorTraduccion) and unaCadenaTraducidaEncoded:
                    try:    
                        theBuffer.write( unaCadenaTraducidaEncoded)
                    except:
                        theResult[ 'traducciones_error_codificacion_Export'].append( unSimboloCadena)    
                        if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False
                        else:
                            unHayErrorTraduccion = True
                            unHayError =  True
                
                theBuffer.write( cPropertyLineSeparator)
                
                
                    
                        
                if theExportTranslationsStatus:
                    # ######################################################################
                    """Write translations status line.
                    
                    """                        
                     
                    aTranslationStatus = unResultadoTraduccion[ 'getEstadoTraduccion']
                    if aTranslationStatus:
                        aTranslationStatusEncoded = someEncodedTranslationsStatus.get( aTranslationStatus, aTranslationStatus)
                    
                        if not unHayErrorSimbolo:
                            unHayErrorStatusLabel = False
                            try:    
                                theBuffer.write( cPropertiesStatusLinePrefix)
                                
                            except:
                                if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                    return False
                                else:
                                    unHayErrorStatusLabel = True
                                    unHayError =  True
                                    
                            if not unHayErrorStatusLabel:
                                
                                try:    
                                    theBuffer.write( unSimboloCadenaEncoded)
                                except:
                                    theResult[ 'simbolos_error_codificacion_Export'].append( unSimboloCadena)    
                                    if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                        return False
                                    else:
                                        unHayErrorSimbolo4 = True
                                        unHayError =  True
                                
                                        
                                if not unHayErrorSimbolo4:        
                                        
                                    theBuffer.write( cPropertyNameValueSeparator )
            
                                    
                                    try:    
                                        theBuffer.write( aTranslationStatusEncoded)
                                        
                                    except:
                                        unHayErrorNombresModulos = True
                                        if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                            return False
                                        else:
                                            unHayErrorNombresModulos = True
                                            unHayError =  True
                                            
                            theBuffer.write( cPropertyLineSeparator)             
                 
                
                

                if theExportModuleNames:
                    # ######################################################################
                    """Write modules line with module names.
                    
                    """                        
                    if ( not unHayErrorSimbolo) and ( not unHayErrorNombresModulos) and unosNombresModulosEncoded:
                        unHayErrorNombresModulosLabel = False
                        try:    
                            theBuffer.write( cPropertiesModulesLinePrefix)
                            
                        except:
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False
                            else:
                                unHayErrorNombresModulosLabel = True
                                unHayError =  True
                                
                        if not unHayErrorNombresModulosLabel:
                            
                            try:    
                                theBuffer.write( unSimboloCadenaEncoded)
                            except:
                                theResult[ 'simbolos_error_codificacion_Export'].append( unSimboloCadena)    
                                if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                    return False
                                else:
                                    unHayErrorSimbolo2 = True
                                    unHayError =  True
                            
                                    
                            if not unHayErrorSimbolo2:        
                                    
                                theBuffer.write( cPropertyNameValueSeparator )
        
                                
                                try:    
                                    theBuffer.write( unosNombresModulos)
                                    
                                except:
                                    unHayErrorNombresModulos = True
                                    if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                        return False
                                    else:
                                        unHayErrorNombresModulos = True
                                        unHayError =  True
                                        
                        theBuffer.write( cPropertyLineSeparator)
                           
                        
                        
                        
                if theExportStringSources:                                    
                    # ######################################################################
                    """Write sources line with source names.
                    
                    """                        
                    if ( not unHayErrorSimbolo) and ( not unHayErrorSources) and unosSourcesEncoded:
                        unHayErrorSourcesLabel = False
                        try:    
                            theBuffer.write( cPropertiesSourcesLinePrefix)
                            
                        except:
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False
                            else:
                                unHayErrorSourcesLabel = True
                                unHayError =  True
                                
                        if not unHayErrorSourcesLabel:
                            
                            try:    
                                theBuffer.write( unSimboloCadenaEncoded)
                            except:
                                theResult[ 'simbolos_error_codificacion_Export'].append( unSimboloCadena)    
                                if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                    return False
                                else:
                                    unHayErrorSimbolo3 = True
                                    unHayError =  True
                            
                            if not unHayErrorSimbolo3:     
                                
                                theBuffer.write( cPropertyNameValueSeparator )
        
                                
                                try:    
                                    theBuffer.write( unosSources)
                                    
                                except:
                                    unHayErrorSources = True
                                    if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                        return False
                                    else:
                                        unHayErrorSources = True
                                        unHayError =  True
                                
                        theBuffer.write( cPropertyLineSeparator)

        return not unHayError        
    
    
    
    
    

     
    security.declarePrivate( 'fContenidoFicheroExportacionIdiomaModulo_JavaProperties')    
    def fContenidoFicheroExportacionIdiomaModulo_JavaProperties( self, 
        theIdioma, 
        theNombreModulo, 
        theCodificacionCaracteres, 
        theResultadosTraducciones, 
        theSourcesCadenasPorSimbolo,
        theExportModuleNames,
        theExportStringSources,
        theExportTranslationsStatus,
        theModulosCadenasPorSimbolo,
        theEncodingErrorHandleMode,
        theEncodedFileErrorsMode,
        theSystemToUnicodeErrorsMode,
        theUnicodeToUTF8ErrorsMode,
        theTranslationService,
        theParentExecutionRecord    =None):
        

        unExecutionRecord = self.fStartExecution( 'method',  'fContenidoFicheroExportacionIdiomaModulo_JavaProperties', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True,}, 'Language %s     Module %s' % (((theIdioma and theIdioma.getCodigoIdiomaEnGvSIG()) or '?'),  theNombreModulo or '?'))
        try:
            unResult = self.fNewVoidResultFicheroExportacionProperties()
            unResult[ 'encoding']                       = theCodificacionCaracteres
            unResult[ 'encoding_error_handle_mode']     = theEncodingErrorHandleMode
            unResult[ 'encoded_file_errors_mode']       = theEncodedFileErrorsMode
            unResult[ 'system_to_unicode_errors_mode']  = theSystemToUnicodeErrorsMode
            unResult[ 'unicode_to_utf8_errors_mode']    = theUnicodeToUTF8ErrorsMode
            
            try:
                
                 
                if not theIdioma or not theCodificacionCaracteres:
                    unResult[ 'status'] = cResultCondition_Internal_MissingParameter
                    return unResult
                
                unBufferResultado = StringIO()
                        
                unaCodificacionCaracteres = theCodificacionCaracteres
                unaCodificacionEntrada    = cTRAEncodingUTF8
                
                if unaCodificacionCaracteres == cTRAEncodingUnicodeEscape:
                    unaCodificacionCaracteres = cTRAEncodingASCII
                    unaCodificacionEntrada    = cTRAEncodingASCII
                    
                
                unEncodedFile = None
                try:
                    unEncodedFile = CODECS_EncodedFile( unBufferResultado, unaCodificacionEntrada, unaCodificacionCaracteres, errors=theEncodedFileErrorsMode)
                except:
                    None
                
                if not unEncodedFile:
                    unResult[ 'status'] = cResultCondition_Encoding_NotAvailable
                    return unResult
        
                anErrorInFile = False
                
                if not self.fWriteHeader_JavaProperties( 
                    unEncodedFile, 
                    unResult,
                    theIdioma, 
                    theNombreModulo, 
                    theCodificacionCaracteres,
                    theEncodingErrorHandleMode, 
                    theSystemToUnicodeErrorsMode,
                    theUnicodeToUTF8ErrorsMode,
                    theTranslationService):
    
                    anErrorInFile = True
                    
                    unResult[ 'status'] = cResultCondition_Encoding_ErrorInHeader
                    if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                        unResult.update( {
                            'contenido':                    unBufferResultado.getvalue(),
                        })
                        return unResult
                    
                    
                if not theResultadosTraducciones:
                    unResult[ 'success'] = True
                    unResult[ 'status'] = cResultCondition_NoTranslationsToExport
                    unResult.update( {
                        'contenido':                    unBufferResultado.getvalue(),
                    })
                    return unResult
                
                
                if not self.fWriteTranslationResults_JavaProperties( 
                    unEncodedFile, 
                    unResult,
                    theResultadosTraducciones,
                    theSourcesCadenasPorSimbolo,
                    theExportModuleNames,
                    theExportStringSources,
                    theExportTranslationsStatus,
                    theModulosCadenasPorSimbolo,
                    theCodificacionCaracteres,
                    theEncodingErrorHandleMode,
                    theSystemToUnicodeErrorsMode,
                    theUnicodeToUTF8ErrorsMode,
                    theTranslationService):
                    
                    anErrorInFile = True
                    
                    if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                        unResult[ 'status'] = cResultCondition_Encoding_ErrorInTranslations
                        unResult.update( {
                            'contenido':                    unBufferResultado.getvalue(),
                        })
                        return unResult
                
                
                 
                unResult.update( {
                    'success':    ( not anErrorInFile) or ( theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_IgnoreAndContinue, cTRAEncodingErrorHandleMode_ReplaceAndContinue, cTRAEncodingErrorHandleMode_XMLReplaceAndContinue , cTRAEncodingErrorHandleMode_BackslashReplaceAndContinue,]), 
                    'contenido':  unBufferResultado.getvalue(),
                })

                
                return unResult  
            
            finally:
                unResult[ 'total_encoding_errors']  = \
                    (( unResult.get( 'header_error_codificacion_SystemToUnicode', False) and 1) or 0) + \
                    (( unResult.get( 'header_error_codificacion_UnicodeToUTF', False) and 1) or 0) + \
                    (( unResult.get( 'header_error_codificacion_Export', False) and 1) or 0) + \
                    len( unResult.get( 'simbolos_error_codificacion_SystemToUnicode', [])) + \
                    len( unResult.get( 'simbolos_error_codificacion_UnicodeToUTF', [])) + \
                    len( unResult.get( 'simbolos_error_codificacion_Export', [])) + \
                    len( unResult.get( 'traducciones_error_codificacion_SystemToUnicode', [])) + \
                    len( unResult.get( 'traducciones_error_codificacion_UnicodeToUTF', [])) + \
                    len( unResult.get( 'traducciones_error_codificacion_Export', []))
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

           



     
    security.declarePrivate( 'fContenidoFicheroExportacionIdiomaModuloNoEspecificado_JavaProperties')    
    def fContenidoFicheroExportacionIdiomaModuloNoEspecificado_JavaProperties( self, 
        theIdioma, 
        theNombreModulo, 
        theCodificacionCaracteres, 
        theResultadosTraducciones, 
        theSourcesCadenasPorSimbolo,
        theExportModuleNames,
        theExportStringSources,
        theExportTranslationsStatus,
        theModulosCadenasPorSimbolo,
        theEncodingErrorHandleMode,
        theEncodedFileErrorsMode,
        theSystemToUnicodeErrorsMode,
        theUnicodeToUTF8ErrorsMode,
        theTranslationService,
        theParentExecutionRecord    =None):

        unExecutionRecord = self.fStartExecution( 'method',  'fContenidoFicheroExportacionIdiomaModuloNoEspecificado_JavaProperties', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True,}, 'language %s    unspecified Module' % ((theIdioma and theIdioma.getCodigoIdiomaEnGvSIG()) or '?'))
        try:
            unResult = self.fContenidoFicheroExportacionIdiomaModulo_JavaProperties( 
                theIdioma, 
                theNombreModulo, 
                theCodificacionCaracteres, 
                theResultadosTraducciones, 
                theSourcesCadenasPorSimbolo,
                theExportModuleNames,
                theExportStringSources,
                theExportTranslationsStatus,
                theModulosCadenasPorSimbolo,
                theEncodingErrorHandleMode,
                theEncodedFileErrorsMode,
                theSystemToUnicodeErrorsMode,
                theUnicodeToUTF8ErrorsMode,
                theTranslationService,
                theParentExecutionRecord    =unExecutionRecord
            )
            return unResult  
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
        
            

     
    security.declarePrivate( 'fContenidoFicheroExportacionIdiomaTodosModulos_JavaProperties')    
    def fContenidoFicheroExportacionIdiomaTodosModulos_JavaProperties( self, 
        theIdioma, 
        theNombreModulo, 
        theCodificacionCaracteres, 
        theResultadosTraducciones, 
        theSourcesCadenasPorSimbolo,
        theExportModuleNames,
        theExportStringSources,
        theExportTranslationsStatus,
        theModulosCadenasPorSimbolo,
        theEncodingErrorHandleMode,
        theEncodedFileErrorsMode,
        theSystemToUnicodeErrorsMode,
        theUnicodeToUTF8ErrorsMode,
        theTranslationService,
        theParentExecutionRecord    =None):

        unExecutionRecord = self.fStartExecution( 'method',  'fContenidoFicheroExportacionIdiomaTodosModulos_JavaProperties', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True,}, 'idioma %s    all modules' % ((theIdioma and theIdioma.getCodigoIdiomaEnGvSIG()) or '?'))
        try:
            unResult = self.fContenidoFicheroExportacionIdiomaModulo_JavaProperties( 
                theIdioma, 
                theNombreModulo, 
                theCodificacionCaracteres, 
                theResultadosTraducciones, 
                theSourcesCadenasPorSimbolo,
                theExportModuleNames,
                theExportStringSources,
                theExportTranslationsStatus,
                theModulosCadenasPorSimbolo,
                theEncodingErrorHandleMode,
                theEncodedFileErrorsMode,
                theSystemToUnicodeErrorsMode,
                theUnicodeToUTF8ErrorsMode,
                theTranslationService,
                theParentExecutionRecord    =unExecutionRecord
            )
            return unResult  
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
        
                        
     
     
    

            
            
 

            
            
            
            
            
            
    
            
            
            
            
            
           
            
    
    ##/code-section class-header

    # Methods
# end of class TRACatalogo_Exportacion_JavaProperties

##code-section module-footer #fill in your manual code here






##/code-section module-footer



