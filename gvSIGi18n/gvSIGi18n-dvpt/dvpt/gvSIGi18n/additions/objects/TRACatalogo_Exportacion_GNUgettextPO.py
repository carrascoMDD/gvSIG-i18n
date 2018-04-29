# -*- coding: utf-8 -*-
#
# File: TRACatalogo_Exportacion_GNUgettextPO.py
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

class TRACatalogo_Exportacion_GNUgettextPO:
    """
    """
    security = ClassSecurityInfo()


    
    
    
    
    ##code-section class-header #fill in your manual code here
    

    
    
    
    def fNewVoidResultFicheroExportacionGNUgettextPO( self,):
        unResult = self.fNewVoidResultFicheroExportacionProperties().copy()
        unResult.update({
            'file_kind':                                                 '.PO',
            'traduccionesReferencia_error_codificacion_SystemToUnicode':  [],
            'traduccionesReferencia_error_codificacion_UnicodeToUTF':     [],
            'traduccionesReferencia_error_codificacion_Export':           [],
        })
        return unResult
    
    
    
    
    

     
    
    
    
    # ####################################################
    """GNUgettextPO output.
    
    """
    
   
    security.declarePrivate( 'fWriteHeader_GNUgettextPO')    
    def fWriteHeader_GNUgettextPO( self, 
        theBuffer, 
        theResult,
        theIdioma, 
        theDomainName, 
        theEncodingName, 
        theEncodingErrorHandleMode, 
        theSystemToUnicodeErrorsMode,
        theUnicodeToUTF8ErrorsMode,
        theTranslationService):
        
        if theEncodingName == cTRAEncodingUnicodeEscape:
            return self.fWriteHeader_GNUgettextPO_UnicodeEscape( 
                theBuffer, 
                theResult,
                theIdioma, 
                theDomainName, 
                theEncodingName, 
                theEncodingErrorHandleMode, 
                theSystemToUnicodeErrorsMode,
                theUnicodeToUTF8ErrorsMode,
                theTranslationService,
            )
   
        return self.fWriteHeader_GNUgettextPO_Encoding( 
            theBuffer, 
            theResult,
            theIdioma, 
            theDomainName, 
            theEncodingName, 
            theEncodingErrorHandleMode, 
            theSystemToUnicodeErrorsMode,
            theUnicodeToUTF8ErrorsMode,
            theTranslationService,
        )

    
    
    
    
    security.declarePrivate( 'fWriteHeader_GNUgettextPO_Encoding')    
    def fWriteHeader_GNUgettextPO_Encoding( self, 
        theBuffer, 
        theResult,
        theIdioma, 
        theDomainName, 
        theEncodingName, 
        theEncodingErrorHandleMode, 
        theSystemToUnicodeErrorsMode,
        theUnicodeToUTF8ErrorsMode,
        theTranslationService):


        if not theResult:
            return False

        if not theIdioma or not theBuffer:
            theResult[ 'status'] = cResultCondition_Internal_MissingParameter    
            return False

        
        unErrorEnHeader = False
        
        unCodigoIdioma = theIdioma.getCodigoIdiomaEnGvSIG()
        
        
        unAhora = self.fDateTimeNow()
        unOffset = int( unAhora.tzoffset() / 3600)
        unOffsetSign = '+'
        if unOffset < 0:
            unOffsetSign = '-'
    
        unPOTimestampUTF8 = ''
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
            '%4.4d-%02d-%02d %02d:%02d%s%02d00' % ( unAhora.year(), unAhora.month(), unAhora.day(), unAhora.hour(), unAhora.minute(), unOffsetSign, unOffset, ), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
            theUnicodeToUTF8ErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            elif unEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                theResult[ 'header_error_codificacion_UnicodeToUTF'] = True    
            if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unPOTimestampUTF8 = unEncodedString
        
            
        unNombreProductoUTF8 = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
            self.fQuoteForGNUgettextPO( self.getNombreProducto()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
            theUnicodeToUTF8ErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            elif unEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                theResult[ 'header_error_codificacion_UnicodeToUTF'] = True    
            if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unNombreProductoUTF8 = unEncodedString
            
            
        unLastTranslatorUTF8 = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
            self.fQuoteForGNUgettextPO( theIdioma.getEquipoTraductor()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
            theUnicodeToUTF8ErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            elif unEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                theResult[ 'header_error_codificacion_UnicodeToUTF'] = True    
            if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unLastTranslatorUTF8 = unEncodedString
            
        unLanguageTeamUTF8 = unLastTranslatorUTF8
            
        unCharSetUTF8 = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
            self.fQuoteForGNUgettextPO( theEncodingName), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
            theUnicodeToUTF8ErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            elif unEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                theResult[ 'header_error_codificacion_UnicodeToUTF'] = True    
            if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unCharSetUTF8  = unEncodedString
            
                 
            
        unaCodificacionTransferenciaContenidoUTF8 = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
            self.fQuoteForGNUgettextPO( theIdioma.getCodificacionTransferenciaContenido()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
            theUnicodeToUTF8ErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            elif unEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                theResult[ 'header_error_codificacion_UnicodeToUTF'] = True    
            if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unaCodificacionTransferenciaContenidoUTF8 = unEncodedString
            
        unasFormasPluralesUTF8 = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
            self.fQuoteForGNUgettextPO( theIdioma.getFormasPlurales()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
            theUnicodeToUTF8ErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            elif unEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                theResult[ 'header_error_codificacion_UnicodeToUTF'] = True    
            if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unasFormasPluralesUTF8 = unEncodedString
            
        unCodigoIdiomaUTF8 = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
            unCodigoIdioma, 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
            theUnicodeToUTF8ErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            elif unEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                theResult[ 'header_error_codificacion_UnicodeToUTF'] = True    
            if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unCodigoIdiomaUTF8 = unEncodedString
            
        unNombreNativoIdiomaUTF8 = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
            self.fQuoteForGNUgettextPO( theIdioma.getNombreNativoDeIdioma()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
            theUnicodeToUTF8ErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            elif unEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                theResult[ 'header_error_codificacion_UnicodeToUTF'] = True    
            if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unNombreNativoIdiomaUTF8 = unEncodedString
            
             
        unasCodificacionesPreferidasUTF8 = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
            self.fQuoteForGNUgettextPO( theIdioma.getCodificacionesPreferidas()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
            theUnicodeToUTF8ErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            elif unEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                theResult[ 'header_error_codificacion_UnicodeToUTF'] = True    
            if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unasCodificacionesPreferidasUTF8 = unEncodedString
             
        unDominioUTF8 = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
            self.fQuoteForGNUgettextPO( theDomainName), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
            theUnicodeToUTF8ErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            elif unEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                theResult[ 'header_error_codificacion_UnicodeToUTF'] = True    
            if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unDominioUTF8 = unEncodedString
            
        unFallbackUTF8 = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
            self.fQuoteForGNUgettextPO( theIdioma.getFallbackDeIdiomas()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
            theUnicodeToUTF8ErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            elif unEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                theResult[ 'header_error_codificacion_UnicodeToUTF'] = True    
            if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unFallbackUTF8 = unEncodedString
               
            
            
        try:    
            theBuffer.write( cGNUgettextPOHeaderTemplateString_Top)
        except:
            theResult[ 'header_error_codificacion_Export'] = True    
            if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                return False
            
        
        theBuffer.write( cGNUgettextPOHeaderLabel_ProjectIdVersion)
        if unNombreProductoUTF8:
            try:    
                theBuffer.write( unNombreProductoUTF8)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
            
        theBuffer.write( cGNUgettextPOHeaderLabel_POTCreationDate)
        if unPOTimestampUTF8:
            try:    
                theBuffer.write( unPOTimestampUTF8)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)

        theBuffer.write( cGNUgettextPOHeaderLabel_PORevisionDate)
        if unPOTimestampUTF8:
            try:    
                theBuffer.write( unPOTimestampUTF8)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
        
        theBuffer.write( cGNUgettextPOHeaderLabel_LastTranslator)
        if unLastTranslatorUTF8:
            try:    
                theBuffer.write( unLastTranslatorUTF8)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
        
        theBuffer.write( cGNUgettextPOHeaderLabel_LanguageTeam)
        if unLanguageTeamUTF8:
            try:    
                theBuffer.write( unLanguageTeamUTF8)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
        
        theBuffer.write( cGNUgettextPOHeaderLabel_MIMEVersion)
        theBuffer.write( cGNUgettextPOHeader_AfterValue)

        theBuffer.write( cGNUgettextPOHeaderLabel_ContentType)
        if unCharSetUTF8:
            try:    
                theBuffer.write( unCharSetUTF8)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
             
        theBuffer.write( cGNUgettextPOHeaderLabel_ContentTransferEncoding)
        if unaCodificacionTransferenciaContenidoUTF8:
            try:    
                theBuffer.write( unaCodificacionTransferenciaContenidoUTF8)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
             
        theBuffer.write( cGNUgettextPOHeaderLabel_PluralForms)
        if unasFormasPluralesUTF8:
            try:    
                theBuffer.write( unasFormasPluralesUTF8)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
             
        theBuffer.write( cGNUgettextPOHeaderLabel_LanguageCode)
        if unCodigoIdiomaUTF8:
            try:    
                theBuffer.write( unCodigoIdiomaUTF8)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
             
        theBuffer.write( cGNUgettextPOHeaderLabel_LanguageName)
        if unNombreNativoIdiomaUTF8:
            try:    
                theBuffer.write( unNombreNativoIdiomaUTF8)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
             
        theBuffer.write( cGNUgettextPOHeaderLabel_PreferredEncodings)
        if unasCodificacionesPreferidasUTF8:
            try:    
                theBuffer.write( unasCodificacionesPreferidasUTF8)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
             
        theBuffer.write( cGNUgettextPOHeaderLabel_Domain)
        if unDominioUTF8:
            try:    
                theBuffer.write( unDominioUTF8)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)

        theBuffer.write( '\n')
             
        return not unErrorEnHeader

            

     

    security.declarePrivate( 'fWriteHeader_GNUgettextPO_UnicodeEscape')    
    def fWriteHeader_GNUgettextPO_UnicodeEscape( self, 
        theBuffer, 
        theResult,
        theIdioma, 
        theDomainName, 
        theEncodingName, 
        theEncodingErrorHandleMode, 
        theSystemToUnicodeErrorsMode,
        theUnicodeToUTF8ErrorsMode,
        theTranslationService):


        if not theResult:
            return False

        if not theIdioma or not theBuffer:
            theResult[ 'status'] = cResultCondition_Internal_MissingParameter    
            return False

        
        unErrorEnHeader = False
        
        unCodigoIdioma = theIdioma.getCodigoIdiomaEnGvSIG()
                
        unAhora = self.fDateTimeNow()
        unOffset = int( unAhora.tzoffset() / 3600)
        unOffsetSign = '+'
        if unOffset < 0:
            unOffsetSign = '-'
    
        unPOTimestampEncoded = ''
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
            '%4.4d-%02d-%02d %02d:%02d%s%02d00' % ( unAhora.year(), unAhora.month(), unAhora.day(), unAhora.hour(), unAhora.minute(), unOffsetSign, unOffset, ), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unPOTimestampEncoded = unEncodedString
        
            
        unNombreProductoEncoded = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
            self.fQuoteForGNUgettextPO( self.getNombreProducto()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unNombreProductoEncoded = unEncodedString
            
            
        unLastTranslatorEncoded = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
            self.fQuoteForGNUgettextPO( theIdioma.getEquipoTraductor()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unLastTranslatorEncoded = unEncodedString
            
        unLanguageTeamEncoded = unLastTranslatorEncoded
            
        #unCharSetEncoded = '' 
        #unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
            #self.fQuoteForGNUgettextPO( theEncodingName), 
            #theTranslationService, 
            #theSystemToUnicodeErrorsMode, 
        #)
        #if unEncodingErrorCondition:
            #unErrorEnHeader = True
            #if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                #theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            #if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                #return False
        #else:    
            #unCharSetEncoded  = unEncodedString
            
                 
            
        unaCodificacionTransferenciaContenidoEncoded = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
            self.fQuoteForGNUgettextPO( theIdioma.getCodificacionTransferenciaContenido()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unaCodificacionTransferenciaContenidoEncoded = unEncodedString
            
        unasFormasPluralesEncoded = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
            self.fQuoteForGNUgettextPO( theIdioma.getFormasPlurales()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unasFormasPluralesEncoded = unEncodedString
            
        unCodigoIdiomaEncoded = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
            unCodigoIdioma, 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unCodigoIdiomaEncoded = unEncodedString
            
        unNombreNativoIdiomaEncoded = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
            self.fQuoteForGNUgettextPO( theIdioma.getNombreNativoDeIdioma()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unNombreNativoIdiomaEncoded = unEncodedString
            
             
        unasCodificacionesPreferidasEncoded = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
            self.fQuoteForGNUgettextPO( theIdioma.getCodificacionesPreferidas()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unasCodificacionesPreferidasEncoded = unEncodedString
             
        unDominioEncoded = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
            self.fQuoteForGNUgettextPO( theNombreModulo), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unDominioEncoded = unEncodedString
            
        unFallbackEncoded = '' 
        unEncodedString, unEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
            self.fQuoteForGNUgettextPO( theIdioma.getFallbackDeIdiomas()), 
            theTranslationService, 
            theSystemToUnicodeErrorsMode, 
        )
        if unEncodingErrorCondition:
            unErrorEnHeader = True
            if unEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                theResult[ 'header_error_codificacion_SystemToUnicode'] = True    
            if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                return False
        else:    
            unFallbackEncoded = unEncodedString
               
            
            
        try:    
            theBuffer.write( cGNUgettextPOHeaderTemplateString_Top)
        except:
            theResult[ 'header_error_codificacion_Export'] = True    
            if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                return False
            
        
        theBuffer.write( cGNUgettextPOHeaderLabel_ProjectIdVersion)
        if unNombreProductoEncoded:
            try:    
                theBuffer.write( unNombreProductoEncoded)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
            
        theBuffer.write( cGNUgettextPOHeaderLabel_POTCreationDate)
        if unPOTimestampEncoded:
            try:    
                theBuffer.write( unPOTimestampEncoded)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)

        theBuffer.write( cGNUgettextPOHeaderLabel_PORevisionDate)
        if unPOTimestampEncoded:
            try:    
                theBuffer.write( unPOTimestampEncoded)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
        
        theBuffer.write( cGNUgettextPOHeaderLabel_LastTranslator)
        if unLastTranslatorEncoded:
            try:    
                theBuffer.write( unLastTranslatorEncoded)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
        
        theBuffer.write( cGNUgettextPOHeaderLabel_LanguageTeam)
        if unLanguageTeamEncoded:
            try:    
                theBuffer.write( unLanguageTeamEncoded)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
        
        theBuffer.write( cGNUgettextPOHeaderLabel_MIMEVersion)
        theBuffer.write( cGNUgettextPOHeader_AfterValue)

        theBuffer.write( cGNUgettextPOHeaderLabel_ContentType)
        try:    
            theBuffer.write( cTRAEncodingASCII)
        except:
            theResult[ 'header_error_codificacion_Export'] = True    
            if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
             
        theBuffer.write( cGNUgettextPOHeaderLabel_ContentTransferEncoding)
        if unaCodificacionTransferenciaContenidoEncoded:
            try:    
                theBuffer.write( unaCodificacionTransferenciaContenidoEncoded)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
             
        theBuffer.write( cGNUgettextPOHeaderLabel_PluralForms)
        if unasFormasPluralesEncoded:
            try:    
                theBuffer.write( unasFormasPluralesEncoded)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
             
        theBuffer.write( cGNUgettextPOHeaderLabel_LanguageCode)
        if unCodigoIdiomaEncoded:
            try:    
                theBuffer.write( unCodigoIdiomaEncoded)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
             
        theBuffer.write( cGNUgettextPOHeaderLabel_LanguageName)
        if unNombreNativoIdiomaEncoded:
            try:    
                theBuffer.write( unNombreNativoIdiomaEncoded)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
             
        theBuffer.write( cGNUgettextPOHeaderLabel_PreferredEncodings)
        if unasCodificacionesPreferidasEncoded:
            try:    
                theBuffer.write( unasCodificacionesPreferidasEncoded)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)
             
        theBuffer.write( cGNUgettextPOHeaderLabel_Domain)
        if unDominioEncoded:
            try:    
                theBuffer.write( unDominioEncoded)
            except:
                theResult[ 'header_error_codificacion_Export'] = True    
                if theEncodingErrorHandleMode == cTRAEncodingErrorHandleMode_CancelOnFirstError:
                    return False
        theBuffer.write( cGNUgettextPOHeader_AfterValue)

        theBuffer.write( '\n')
             
        return not unErrorEnHeader

    
    
    
    
    security.declarePrivate( 'fQuoteForGNUgettextPO')    
    def fQuoteForGNUgettextPO( self, theString):
        if not theString:
            return ''
        return theString.replace( '"', '\"')
    
   
    
  
    security.declarePrivate( 'fWriteTranslationResults_GNUgettextPO')    
    def fWriteTranslationResults_GNUgettextPO( self, 
        theBuffer, 
        theResult,
        theResultadosTraducciones, 
        theResultadosTraduccionesReferencia, 
        theSourcesCadenasPorSimbolo,
        theExportModuleNames,
        theExportStringSources,
        theExportTranslationsStatus,
        theExportContributions,
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
                            
        
        
        # ######################################################################
        """Retrieve translations to reference language for string symbols to export.
        
        """
        unosResultadosTraduccionesReferencia = { }
        if theResultadosTraduccionesReferencia:
            for unResultadoTraduccionReferencia in theResultadosTraduccionesReferencia:
                unSimboloCadena           = unResultadoTraduccionReferencia[ 'getSimbolo']
                unosResultadosTraduccionesReferencia[ unSimboloCadena] = unResultadoTraduccionReferencia

                
                
                
        # ######################################################################
        """Retrieve sources and module names for string symbols to export.
        
        """
        if theExportStringSources:
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

            unHayErrorSimbolo               = False
            unHayErrorTraduccion            = False
            unHayErrorTraduccionReferencia  = False
            unHayErrorSources               = False
            unHayErrorNombresModulos        = False
            
            unHayErrorCreationDate          = False
            unHayErrorCreator               = False
            unHayErrorTranslationDate       = False
            unHayErrorTranslator            = False
            unHayErrorReviewDate            = False
            unHayErrorReviewer              = False
            unHayErrorDefinitiveDate        = False
            unHayErrorCoordinator           = False
            
            
            
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
                    if cTRAEncodingUnicodeEscape == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
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
                    
                    unHayErrorSimbolo = True
                    unHayError        = True
                    
                    if unSimboloCadenaEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                        theResult[ 'simbolos_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
                        
                    elif unSimboloCadenaEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                        theResult[ 'simbolos_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                
                    if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                        return False 

                         
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
                        
                        unHayErrorTraduccion = True
                        unHayError =  True
                        
                        if unaCadenaTraducidaEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                            theResult[ 'traduccionesRefrencia_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
        
                        elif unaCadenaTraducidaEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                            theResult[ 'traduccionesReferencia_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                    
                        if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False

             
            # ######################################################################
            """Encode translation into reference language.
            
            """
            unaCadenaTraducidaReferencia = ''
            unaCadenaTraducidaReferenciaEncoded = ''
            
            unResultadoTraduccionReferencia  = unosResultadosTraduccionesReferencia.get( unSimboloCadena, {})
            if unResultadoTraduccionReferencia:
                unaCadenaTraducidaReferencia     = unResultadoTraduccionReferencia[ 'getCadenaTraducida']
                if unaCadenaTraducidaReferencia:
                    
                    if theCodificacionCaracteres == cTRAEncodingUnicodeEscape:
                        unaCadenaTraducidaReferenciaEncoded, unaCadenaTraducidaReferenciaEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                            unaCadenaTraducidaReferencia, 
                            theTranslationService, 
                            theSystemToUnicodeErrorsMode, 
                        )
                        
                        if unaCadenaTraducidaReferenciaEncodingErrorCondition or not unaCadenaTraducidaReferenciaEncoded:
                            if unaCadenaTraducidaReferenciaEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                                theResult[ 'traducciones_error_codificacion_SystemToUnicode'] = True    
                            return False
                    else: 
                    
                        unaCadenaTraducidaReferenciaEncoded, unaCadenaTraducidaReferenciaEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                            unaCadenaTraducidaReferencia, 
                            theTranslationService, 
                            theSystemToUnicodeErrorsMode, 
                            theUnicodeToUTF8ErrorsMode, 
                        )
                        if unaCadenaTraducidaReferenciaEncodingErrorCondition:
                            
                            unHayErrorTraduccionReferencia = True
                            unHayError =  True
                            
                            if unaCadenaTraducidaReferenciaEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                                theResult[ 'traducciones_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
            
                            elif unaCadenaTraducidaReferenciaEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                                theResult[ 'traducciones_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                        
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False                   
                        
                      
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
                                    
                
                            
                            
                            
                            
                            
            if theExportContributions:
                # ######################################################################
                """Encode dates and user names that created, translated, reviewed or marked as definitive the translation.
                
                """
                unCreationDate        = unResultadoTraduccion[ 'getFechaCreacionTextual']
                unCreationDateEncoded = ''
                unCreator             = unResultadoTraduccion[ 'getUsuarioCreador']
                unCreatorEncoded      = ''
                
                unTranslationDate     = unResultadoTraduccion[ 'getFechaTraduccionTextual']
                unTranslationDateEncoded  = ''
                unTranslator          = unResultadoTraduccion[ 'getUsuarioTraductor']
                unTranslatorEncoded   = ''
                
                unReviewDate          = unResultadoTraduccion[ 'getFechaRevisionTextual']
                unReviewDateEncoded   = ''
                unReviewer            = unResultadoTraduccion[ 'getUsuarioRevisor']
                unReviewerEncoded     = ''
                
                unDefinitiveDate      = unResultadoTraduccion[ 'getFechaDefinitivoTextual']
                unDefinitiveDateEncoded   = ''
                unCoordinator         = unResultadoTraduccion[ 'getUsuarioCoordinador']
                unCoordinatorEncoded  = ''
                
                if unCreationDate:
                    if theCodificacionCaracteres == cTRAEncodingUnicodeEscape:
                        unCreationDateEncoded, unCreationDateEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                            unCreationDate, 
                            theTranslationService, 
                            theSystemToUnicodeErrorsMode, 
                        )
                        
                        if unCreationDateEncodedEncodingErrorCondition or not unCreationDateEncoded:
                            if unCreationDateEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                                theResult[ 'contributions_error_codificacion_SystemToUnicode'] = True    
                            return False
                    else: 
                    
                        unCreationDateEncoded, unCreationDateEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                            unCreationDate, 
                            theTranslationService, 
                            theSystemToUnicodeErrorsMode, 
                            theUnicodeToUTF8ErrorsMode, 
                        )
                        if unCreationDateEncodedEncodingErrorCondition:
                            
                            unHayErrorCreationDate = True
                            unHayError =  True
                            
                            if unCreationDateEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                                theResult[ 'contributions_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
            
                            elif unCreationDateEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                                theResult[ 'contributions_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                        
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False                   
                                    
                
                            
                         
                if unCreator:
                    if theCodificacionCaracteres == cTRAEncodingUnicodeEscape:
                        unCreatorEncoded, unCreatorEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                            unCreator, 
                            theTranslationService, 
                            theSystemToUnicodeErrorsMode, 
                        )
                        
                        if unCreatorEncodedEncodingErrorCondition or not unCreatorEncoded:
                            if unCreatorEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                                theResult[ 'contributions_error_codificacion_SystemToUnicode'] = True    
                            return False
                    else: 
                    
                        unCreatorEncoded, unCreatorEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                            unCreator, 
                            theTranslationService, 
                            theSystemToUnicodeErrorsMode, 
                            theUnicodeToUTF8ErrorsMode, 
                        )
                        if unCreatorEncodedEncodingErrorCondition:
                            
                            unHayErrorCreator = True
                            unHayError =  True
                            
                            if unCreatorEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                                theResult[ 'contributions_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
            
                            elif unCreatorEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                                theResult[ 'contributions_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                        
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False                   
                                    
                                        
                if unTranslationDate:
                    if theCodificacionCaracteres == cTRAEncodingUnicodeEscape:
                        unTranslationDateEncoded, unTranslationDateEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                            unTranslationDate, 
                            theTranslationService, 
                            theSystemToUnicodeErrorsMode, 
                        )
                        
                        if unTranslationDateEncodedEncodingErrorCondition or not unTranslationDateEncoded:
                            if unTranslationDateEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                                theResult[ 'contributions_error_codificacion_SystemToUnicode'] = True    
                            return False
                    else: 
                    
                        unTranslationDateEncoded, unTranslationDateEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                            unTranslationDate, 
                            theTranslationService, 
                            theSystemToUnicodeErrorsMode, 
                            theUnicodeToUTF8ErrorsMode, 
                        )
                        if unTranslationDateEncodedEncodingErrorCondition:
                            
                            unHayErrorTranslationDate = True
                            unHayError =  True
                            
                            if unTranslationDateEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                                theResult[ 'contributions_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
            
                            elif unTranslationDateEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                                theResult[ 'contributions_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                        
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False                   
                                    
                
                            
                if unTranslator:
                    if theCodificacionCaracteres == cTRAEncodingUnicodeEscape:
                        unTranslatorEncoded, unTranslatorEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                            unTranslator, 
                            theTranslationService, 
                            theSystemToUnicodeErrorsMode, 
                        )
                        
                        if unTranslatorEncodedEncodingErrorCondition or not unTranslatorEncoded:
                            if unTranslatorEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                                theResult[ 'contributions_error_codificacion_SystemToUnicode'] = True    
                            return False
                    else: 
                    
                        unTranslatorEncoded, unTranslatorEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                            unTranslator, 
                            theTranslationService, 
                            theSystemToUnicodeErrorsMode, 
                            theUnicodeToUTF8ErrorsMode, 
                        )
                        if unTranslatorEncodedEncodingErrorCondition:
                            
                            unHayErrorTranslator = True
                            unHayError =  True
                            
                            if unTranslatorEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                                theResult[ 'contributions_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
            
                            elif unTranslatorEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                                theResult[ 'contributions_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                        
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False                   
                                    

                            
                                        
                if unReviewDate:
                    if theCodificacionCaracteres == cTRAEncodingUnicodeEscape:
                        unReviewDateEncoded, unReviewDateEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                            unReviewDate, 
                            theTranslationService, 
                            theSystemToUnicodeErrorsMode, 
                        )
                        
                        if unReviewDateEncodedEncodingErrorCondition or not unReviewDateEncoded:
                            if unReviewDateEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                                theResult[ 'contributions_error_codificacion_SystemToUnicode'] = True    
                            return False
                    else: 
                    
                        unReviewDateEncoded, unReviewDateEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                            unReviewDate, 
                            theTranslationService, 
                            theSystemToUnicodeErrorsMode, 
                            theUnicodeToUTF8ErrorsMode, 
                        )
                        if unReviewDateEncodedEncodingErrorCondition:
                            
                            unHayErrorReviewDate = True
                            unHayError =  True
                            
                            if unReviewDateEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                                theResult[ 'contributions_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
            
                            elif unReviewDateEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                                theResult[ 'contributions_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                        
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False                   
                                    
                
          
                            
                if unReviewer:
                    if theCodificacionCaracteres == cTRAEncodingUnicodeEscape:
                        unReviewerEncoded, unReviewerEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                            unReviewer, 
                            theTranslationService, 
                            theSystemToUnicodeErrorsMode, 
                        )
                        
                        if unReviewerEncodedEncodingErrorCondition or not unReviewerEncoded:
                            if unReviewerEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                                theResult[ 'contributions_error_codificacion_SystemToUnicode'] = True    
                            return False
                    else: 
                    
                        unReviewerEncoded, unReviewerEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                            unReviewer, 
                            theTranslationService, 
                            theSystemToUnicodeErrorsMode, 
                            theUnicodeToUTF8ErrorsMode, 
                        )
                        if unReviewerEncodedEncodingErrorCondition:
                            
                            unHayErrorReviewer = True
                            unHayError =  True
                            
                            if unReviewerEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                                theResult[ 'contributions_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
            
                            elif unReviewerEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                                theResult[ 'contributions_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                        
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False                   
                                    

         
                                        
                if unDefinitiveDate:
                    if theCodificacionCaracteres == cTRAEncodingUnicodeEscape:
                        unDefinitiveDateEncoded, unDefinitiveDateEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                            unDefinitiveDate, 
                            theTranslationService, 
                            theSystemToUnicodeErrorsMode, 
                        )
                        
                        if unDefinitiveDateEncodedEncodingErrorCondition or not unDefinitiveDateEncoded:
                            if unDefinitiveDateEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                                theResult[ 'contributions_error_codificacion_SystemToUnicode'] = True    
                            return False
                    else: 
                    
                        unDefinitiveDateEncoded, unDefinitiveDateEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                            unDefinitiveDate, 
                            theTranslationService, 
                            theSystemToUnicodeErrorsMode, 
                            theUnicodeToUTF8ErrorsMode, 
                        )
                        if unDefinitiveDateEncodedEncodingErrorCondition:
                            
                            unHayErrorDefinitiveDate = True
                            unHayError =  True
                            
                            if unDefinitiveDateEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                                theResult[ 'contributions_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
            
                            elif unDefinitiveDateEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                                theResult[ 'contributions_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                        
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False                   
                                    
                
          
       
                            
                if unCoordinator:
                    if theCodificacionCaracteres == cTRAEncodingUnicodeEscape:
                        unCoordinatorEncoded, unCoordinatorEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeEscape( 
                            unCoordinator, 
                            theTranslationService, 
                            theSystemToUnicodeErrorsMode, 
                        )
                        
                        if unCoordinatorEncodedEncodingErrorCondition or not unCoordinatorEncoded:
                            if unCoordinatorEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicodeEscape:
                                theResult[ 'contributions_error_codificacion_SystemToUnicode'] = True    
                            return False
                    else: 
                    
                        unCoordinatorEncoded, unCoordinatorEncodedEncodingErrorCondition = self.fFromSystemEncodingToUnicodeToUTF8( 
                            unCoordinator, 
                            theTranslationService, 
                            theSystemToUnicodeErrorsMode, 
                            theUnicodeToUTF8ErrorsMode, 
                        )
                        if unCoordinatorEncodedEncodingErrorCondition:
                            
                            unHayErrorCoordinator = True
                            unHayError =  True
                            
                            if unCoordinatorEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromSystemToUnicode:
                                theResult[ 'contributions_error_codificacion_SystemToUnicode'].append( unSimboloCadena)    
            
                            elif unCoordinatorEncodedEncodingErrorCondition == cResultCondition_Encoding_FailureFromUnicodeToUTF8:
                                theResult[ 'contributions_error_codificacion_UnicodeToUTF'].append( unSimboloCadena)    
                        
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False                   
                                    

         
                                                                                                                                                       
            
            # ######################################################################
            """Write Default line with translation into reference language.
            
            """                        
            unHayErrorDefaultLabel = False        
            try:    
                theBuffer.write( cGNUgettextPOEntryLabel_Default)
            except:
                unHayErrorDefaultLabel = True
                if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                    return False
                else:
                    unHayError =  True
                    
            if ( not unHayErrorDefaultLabel) and ( not unHayErrorTraduccionReferencia) and unaCadenaTraducidaReferenciaEncoded:
                try:    
                    theBuffer.write( unaCadenaTraducidaReferenciaEncoded)
                except:
                    theResult[ 'traduccionesReferencia_error_codificacion_Export'].append( unSimboloCadena)    
                    if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                        return False
                    else:
                        unHayErrorTraduccionReferencia = True
                        unHayError =  True
                     
            theBuffer.write( cGNUgettextPOEntryLabel_AfterDefault)
                  
            
            
            
            if theExportTranslationsStatus:
                # ######################################################################
                """Write translation status line.
                
                """    
                aTranslationStatus = unResultadoTraduccion[ 'getEstadoTraduccion']
                if aTranslationStatus:
                    aTranslationStatusEncoded = someEncodedTranslationsStatus.get( aTranslationStatus, aTranslationStatus)
                
                unHayErrorStatusLabel = False
                try:    
                    theBuffer.write( cGNUgettextPOEntryLabel_Status)
                    
                except:
                    if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                        return False
                    else:
                        unHayErrorStatusLabel = True
                        unHayError =  True
                        
                if not unHayErrorStatusLabel:
                    try:    
                        theBuffer.write( aTranslationStatusEncoded)
                        
                    except:
                        if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False
                        else:
                            unHayError =  True
                            
                    theBuffer.write( cGNUgettextPOEntryLabel_AfterStatus)                
                
            
            
            if theExportModuleNames:
                # ######################################################################
                """Write modules line with module names.
                
                """                        
                if ( not unHayErrorNombresModulos) and  unosNombresModulosEncoded:
                    unHayErrorNombresModulosLabel = False
                    try:    
                        theBuffer.write( cGNUgettextPOEntryLabel_Modules)
                        
                    except:
                        if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False
                        else:
                            unHayErrorNombresModulosLabel = True
                            unHayError =  True
                            
                    if not unHayErrorNombresModulosLabel:
                        try:    
                            theBuffer.write( unosNombresModulosEncoded)
                            
                        except:
                            unHayErrorNombresModulos = True
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False
                            else:
                                unHayErrorNombresModulos = True
                                unHayError =  True
                                
                        theBuffer.write( cGNUgettextPOEntryLabel_AfterModules)
                
                    
         
                            
            if theExportStringSources:
                # ######################################################################
                """Write sources line with module names.
                
                """                        
                if ( not unHayErrorSources) and unosSourcesEncoded:
                    unHayErrorSourcesLabel = False
                    try:    
                        theBuffer.write( cGNUgettextPOEntryLabel_SourceFileNames)
                        
                    except:
                        if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False
                        else:
                            unHayErrorSourcesLabel = True
                            unHayError =  True
                            
                    if not unHayErrorSourcesLabel:
                        try:    
                            theBuffer.write( unosSourcesEncoded)
                            
                        except:
                            unHayErrorSources = True
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False
                            else:
                                unHayErrorSources = True
                                unHayError =  True
                                
                    theBuffer.write( cGNUgettextPOEntryLabel_AfterSourceFileNames)
                                
            
                    
           
            
            if theExportContributions:
                # ######################################################################
                """Write contributions lines with dates and user names that created, translated, reviewed or marked as definitive the translation.
                
                """    
                
                
                if ( not unHayErrorCreationDate) and  unCreationDateEncoded:
                    unHayErrorCreationDateLabel = False
                    try:    
                        theBuffer.write( cGNUgettextPOEntryLabel_CreationDate)
                        
                    except:
                        if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False
                        else:
                            unHayErrorCreationDateLabel = True
                            unHayError =  True
                            
                    if not unHayErrorCreationDateLabel:
                        try:    
                            theBuffer.write( unCreationDateEncoded)
                            
                        except:
                            unHayErrorCreationDate = True
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False
                            else:
                                unHayErrorCreationDate = True
                                unHayError =  True
                                
                        theBuffer.write( cGNUgettextPOEntryLabel_AfterCreationDate)
                    

                
                if ( not unHayErrorCreator) and  unCreatorEncoded:
                    unHayErrorCreatorLabel = False
                    try:    
                        theBuffer.write( cGNUgettextPOEntryLabel_Creator)
                        
                    except:
                        if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False
                        else:
                            unHayErrorCreatorLabel = True
                            unHayError =  True
                            
                    if not unHayErrorCreatorLabel:
                        try:    
                            theBuffer.write( unCreatorEncoded)
                            
                        except:
                            unHayErrorCreator = True
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False
                            else:
                                unHayErrorCreator = True
                                unHayError =  True
                                
                        theBuffer.write( cGNUgettextPOEntryLabel_AfterCreator)
                    
                         

                
                if ( not unHayErrorTranslationDate) and  unTranslationDateEncoded:
                    unHayErrorTranslationDateLabel = False
                    try:    
                        theBuffer.write( cGNUgettextPOEntryLabel_TranslationDate)
                        
                    except:
                        if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False
                        else:
                            unHayErrorTranslationDateLabel = True
                            unHayError =  True
                            
                    if not unHayErrorTranslationDateLabel:
                        try:    
                            theBuffer.write( unTranslationDateEncoded)
                            
                        except:
                            unHayErrorTranslationDate = True
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False
                            else:
                                unHayErrorTranslationDate = True
                                unHayError =  True
                                
                        theBuffer.write( cGNUgettextPOEntryLabel_AfterTranslationDate)
                    
                        
                        
                        
                        

                
                if ( not unHayErrorTranslator) and  unTranslatorEncoded:
                    unHayErrorTranslatorLabel = False
                    try:    
                        theBuffer.write( cGNUgettextPOEntryLabel_Translator)
                        
                    except:
                        if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False
                        else:
                            unHayErrorTranslatorLabel = True
                            unHayError =  True
                            
                    if not unHayErrorTranslatorLabel:
                        try:    
                            theBuffer.write( unTranslatorEncoded)
                            
                        except:
                            unHayErrorTranslator = True
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False
                            else:
                                unHayErrorTranslator = True
                                unHayError =  True
                                
                        theBuffer.write( cGNUgettextPOEntryLabel_AfterTranslator)
                    
                         
                        
                        

                
                if ( not unHayErrorReviewDate) and  unReviewDateEncoded:
                    unHayErrorReviewDateLabel = False
                    try:    
                        theBuffer.write( cGNUgettextPOEntryLabel_ReviewDate)
                        
                    except:
                        if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False
                        else:
                            unHayErrorReviewDateLabel = True
                            unHayError =  True
                            
                    if not unHayErrorReviewDateLabel:
                        try:    
                            theBuffer.write( unReviewDateEncoded)
                            
                        except:
                            unHayErrorReviewDate = True
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False
                            else:
                                unHayErrorReviewDate = True
                                unHayError =  True
                                
                        theBuffer.write( cGNUgettextPOEntryLabel_AfterReviewDate)
                    
                        

                
                if ( not unHayErrorReviewer) and  unReviewerEncoded:
                    unHayErrorReviewerLabel = False
                    try:    
                        theBuffer.write( cGNUgettextPOEntryLabel_Reviewer)
                        
                    except:
                        if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False
                        else:
                            unHayErrorReviewerLabel = True
                            unHayError =  True
                            
                    if not unHayErrorReviewerLabel:
                        try:    
                            theBuffer.write( unReviewerEncoded)
                            
                        except:
                            unHayErrorReviewer = True
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False
                            else:
                                unHayErrorReviewer = True
                                unHayError =  True
                                
                        theBuffer.write( cGNUgettextPOEntryLabel_AfterReviewer)
                    
                         
                        
                        
    
                if ( not unHayErrorDefinitiveDate) and  unDefinitiveDateEncoded:
                    unHayErrorDefinitiveDateLabel = False
                    try:    
                        theBuffer.write( cGNUgettextPOEntryLabel_DefinitiveDate)
                        
                    except:
                        if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False
                        else:
                            unHayErrorDefinitiveDateLabel = True
                            unHayError =  True
                            
                    if not unHayErrorDefinitiveDateLabel:
                        try:    
                            theBuffer.write( unDefinitiveDateEncoded)
                            
                        except:
                            unHayErrorDefinitiveDate = True
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False
                            else:
                                unHayErrorDefinitiveDate = True
                                unHayError =  True
                                
                        theBuffer.write( cGNUgettextPOEntryLabel_AfterDefinitiveDate)
                    

                                        
                        

                
                if ( not unHayErrorCoordinator) and  unCoordinatorEncoded:
                    unHayErrorCoordinatorLabel = False
                    try:    
                        theBuffer.write( cGNUgettextPOEntryLabel_Coordinator)
                        
                    except:
                        if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                            return False
                        else:
                            unHayErrorCoordinatorLabel = True
                            unHayError =  True
                            
                    if not unHayErrorCoordinatorLabel:
                        try:    
                            theBuffer.write( unCoordinatorEncoded)
                            
                        except:
                            unHayErrorCoordinator = True
                            if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                                return False
                            else:
                                unHayErrorCoordinator = True
                                unHayError =  True
                                
                        theBuffer.write( cGNUgettextPOEntryLabel_AfterCoordinator)
                    
                         
                        
                        
                        
                        
                    
            # ######################################################################
            """Write string symbol line.
            
            """                        
            unHayErrorSimboloLabel = False   
            try:    
                theBuffer.write( cGNUgettextPOEntryLabel_msgid)
            except:
                unHayErrorSimboloLabel = True
                if  unHayErrorSimbolo in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                    return False
                else:
                    unHayError =  True

            if ( not unHayErrorSimboloLabel) and ( not unHayErrorSimbolo) and unSimboloCadenaEncoded:
                try:    
                    theBuffer.write( unSimboloCadenaEncoded)
                except:
                    theResult[ 'simbolos_error_codificacion_Export'].append( unSimboloCadena)    
                    if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                        return False
                    else:
                        unHayErrorSimbolo = True
                        unHayError =  True
                          
            theBuffer.write( cGNUgettextPOEntryLabel_AfterMsgid)
                        
            
            
            # ######################################################################
            """Write translation line.
            
            """                        
            unHayErrorCadenaTraducidaLabel = False        
            try:    
                theBuffer.write( cGNUgettextPOEntryLabel_msgstr)
            except:
                unHayErrorCadenaTraducidaLabel = True
                if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                    return False
                else:
                    unHayError =  True
                    
            if ( not unHayErrorCadenaTraducidaLabel) and  ( not unHayErrorTraduccion) and unaCadenaTraducidaEncoded:
                try:    
                    theBuffer.write( unaCadenaTraducidaEncoded)
                except:
                    theResult[ 'traducciones_error_codificacion_Export'].append( unSimboloCadena)    
                    if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                        return False
                    else:
                        unHayErrorTraduccion = True
                        unHayError =  True
            theBuffer.write( cGNUgettextPOEntryLabel_AfterMsgstr)
              
            try:    
                theBuffer.write( '\n')
            except:
                None
                
        return not unHayError        
    

        
        
        

    

    
    security.declarePrivate( 'fContenidoFicheroExportacionIdiomaModulo_GNUgettextPO')    
    def fContenidoFicheroExportacionIdiomaModulo_GNUgettextPO( self, 
        theIdioma, 
        theDomainName, 
        theCodificacionCaracteres, 
        theResultadosTraducciones,
        theResultadosTraduccionesReferencia, 
        theSourcesCadenasPorSimbolo,
        theExportModuleNames,
        theExportStringSources,
        theExportTranslationsStatus,
        theExportContributions,
        theModulosCadenasPorSimbolo,
        theEncodingErrorHandleMode,
        theEncodedFileErrorsMode,
        theSystemToUnicodeErrorsMode,
        theUnicodeToUTF8ErrorsMode,
        theTranslationService,
        theParentExecutionRecord    =None):
         
        unExecutionRecord = self.fStartExecution( 'method',  'fContenidoFicheroExportacionIdiomaModulo_GNUgettextPO', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True,},)
        try:
         
            unResult = self.fNewVoidResultFicheroExportacionGNUgettextPO()
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
                
                if not self.fWriteHeader_GNUgettextPO( 
                    unEncodedFile, 
                    unResult,
                    theIdioma, 
                    theDomainName, 
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
                    unResult[ 'success'] = not anErrorInFile
                    unResult[ 'status'] = cResultCondition_NoTranslationsToExport
                    unResult.update( {
                        'contenido':                    unBufferResultado.getvalue(),
                    })
                    return unResult
                
                
                if not self.fWriteTranslationResults_GNUgettextPO( 
                    theBuffer                           =unEncodedFile, 
                    theResult                           =unResult,
                    theResultadosTraducciones           =theResultadosTraducciones, 
                    theResultadosTraduccionesReferencia =theResultadosTraduccionesReferencia, 
                    theSourcesCadenasPorSimbolo         =theSourcesCadenasPorSimbolo,
                    theExportModuleNames                =theExportModuleNames,
                    theExportStringSources              =theExportStringSources,
                    theExportTranslationsStatus         =theExportTranslationsStatus,
                    theExportContributions              =theExportContributions,
                    theModulosCadenasPorSimbolo         =theModulosCadenasPorSimbolo,
                    theCodificacionCaracteres           =theCodificacionCaracteres,
                    theEncodingErrorHandleMode          =theEncodingErrorHandleMode, 
                    theSystemToUnicodeErrorsMode        =theSystemToUnicodeErrorsMode, 
                    theUnicodeToUTF8ErrorsMode          =theUnicodeToUTF8ErrorsMode, 
                    theTranslationService               =theTranslationService,):
                    
                    anErrorInFile = True
                    
                    if theEncodingErrorHandleMode in [ cTRAEncodingErrorHandleMode_CancelOnFirstError,]:
                        unResult[ 'status'] = cResultCondition_Encoding_ErrorInTranslations
                        unResult.update( {
                            'contenido':                    unBufferResultado.getvalue(),
                        })
                        return unResult
                
                
                 
                unResult.update( {
                    'success':    not anErrorInFile, 
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
    
 

    
    
    
    security.declarePrivate( 'fContenidoFicheroExportacionIdiomaModuloNoEspecificado_GNUgettextPO')    
    def fContenidoFicheroExportacionIdiomaModuloNoEspecificado_GNUgettextPO( self, 
        theIdioma, 
        theDomainName, 
        theCodificacionCaracteres, 
        theResultadosTraducciones,
        theResultadosTraduccionesReferencia, 
        theSourcesCadenasPorSimbolo,
        theExportModuleNames,
        theExportStringSources,
        theExportTranslationsStatus,
        theExportContributions,
        theModulosCadenasPorSimbolo,
        theEncodingErrorHandleMode,
        theEncodedFileErrorsMode,
        theSystemToUnicodeErrorsMode,
        theUnicodeToUTF8ErrorsMode,
        theTranslationService,
        theParentExecutionRecord    =None):
         
        unExecutionRecord = self.fStartExecution( 'method',  'fContenidoFicheroExportacionIdiomaModulo_GNUgettextPO', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True,},) 
        try:
         
            unResult = self.fContenidoFicheroExportacionIdiomaModulo_GNUgettextPO(  
                theIdioma, 
                theDomainName, 
                theCodificacionCaracteres, 
                theResultadosTraducciones,
                theResultadosTraduccionesReferencia, 
                theSourcesCadenasPorSimbolo,
                theExportModuleNames,
                theExportStringSources,
                theExportTranslationsStatus,
                theExportContributions,
                theModulosCadenasPorSimbolo,
                theEncodingErrorHandleMode,
                theEncodedFileErrorsMode,
                theSystemToUnicodeErrorsMode,
                theUnicodeToUTF8ErrorsMode,
                theTranslationService,
                unExecutionRecord)

            return unResult  

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
    
 

    

    
    security.declarePrivate( 'fContenidoFicheroExportacionIdiomaTodosModulos_GNUgettextPO')    
    def fContenidoFicheroExportacionIdiomaTodosModulos_GNUgettextPO( self, 
        theIdioma, 
        theDomainName, 
        theCodificacionCaracteres, 
        theResultadosTraducciones,
        theResultadosTraduccionesReferencia, 
        theSourcesCadenasPorSimbolo,
        theExportModuleNames,
        theExportStringSources,
        theExportTranslationsStatus,
        theExportContributions,
        theModulosCadenasPorSimbolo,
        theEncodingErrorHandleMode,
        theEncodedFileErrorsMode,
        theSystemToUnicodeErrorsMode,
        theUnicodeToUTF8ErrorsMode,
        theTranslationService,
        theParentExecutionRecord    =None):
         
        unExecutionRecord = self.fStartExecution( 'method',  'fContenidoFicheroExportacionIdiomaModulo_GNUgettextPO', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True,},)
        try:
         
            unResult = self.fContenidoFicheroExportacionIdiomaModulo_GNUgettextPO(  
                theIdioma                            =theIdioma,                           
                theDomainName                        =theDomainName,                       
                theCodificacionCaracteres            =theCodificacionCaracteres,           
                theResultadosTraducciones            =theResultadosTraducciones,           
                theResultadosTraduccionesReferencia  =theResultadosTraduccionesReferencia, 
                theSourcesCadenasPorSimbolo          =theSourcesCadenasPorSimbolo,         
                theExportModuleNames                 =theExportModuleNames,                
                theExportStringSources               =theExportStringSources,              
                theExportTranslationsStatus          =theExportTranslationsStatus,         
                theExportContributions               =theExportContributions,              
                theModulosCadenasPorSimbolo          =theModulosCadenasPorSimbolo,         
                theEncodingErrorHandleMode           =theEncodingErrorHandleMode,          
                theEncodedFileErrorsMode             =theEncodedFileErrorsMode,            
                theSystemToUnicodeErrorsMode         =theSystemToUnicodeErrorsMode,        
                theUnicodeToUTF8ErrorsMode           =theUnicodeToUTF8ErrorsMode,          
                theTranslationService                =theTranslationService,               
                theParentExecutionRecord             =unExecutionRecord,
            )

            return unResult  

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
    
 
            
            
    
            
            
            
            
            
            
            
    
    ##/code-section class-header

    # Methods
# end of class TRACatalogo_Exportacion_GNUgettextPO

##code-section module-footer #fill in your manual code here




    


##/code-section module-footer



