# -*- coding: utf-8 -*-
#
# File: TRAElemento_Encoding.py
#
# Copyright (c) 2008, 2009, 2010, 2011  by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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


import cgi

from codecs                     import lookup   as CODECS_Lookup


from AccessControl              import ClassSecurityInfo

from Products.CMFCore           import permissions


from Products.PloneLanguageTool import availablelanguages as PloneLanguageToolAvailableLanguages


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



from TRAImportarExportar_Constants_Encodings      import cUTFEncodingsForAllLanguages, cDefaultEncodingsSourceMap, cWesternLanguageMarkInSourceMap, cTRAEncodingSeparatorSentinelName
        



from TRACatalogo_Globales    import TRACatalogo_Globales




            
            
            
    
            
# ########################################################################################################
    
class TRAElemento_Encoding:
    """Class with responsibility to deal with encoding of character strings.
        
    """
    
    security = ClassSecurityInfo()



    security.declarePublic( 'fEncodeLogString')
    def fEncodeLogString( self, theChangeDescriptionString, theTranslationService=None):
        if not theChangeDescriptionString:
            return ''
        
        aString = theChangeDescriptionString
        
        aTranslationService = theTranslationService
        if not aTranslationService:
            aTranslationService = self.getTranslationServiceTool()
            
        if aTranslationService:
            unUnicodeString = aTranslationService.asunicodetype( theChangeDescriptionString, errors="ignore")        
        else:
            try:
                unUnicodeString = unicode( aString)    
            except:
                None
        
        if not unUnicodeString:
            return ''
        
        unEncodedString = unUnicodeString
        if aTranslationService:    
            unEncodedString = aTranslationService.encode( unUnicodeString, cProgramTextEncoding)
        else:
            try:
                unEncodedString = unUnicodeString.encode( cProgramTextEncoding)    
            except:
                None
                
        if not unEncodedString:
            return ''
                
        return unEncodedString
    
    
    
    security.declarePublic( 'fCGIescape')
    def fCGIescape(self, theString, quote=1):
        if not theString:
            return ''
        return cgi.escape( theString, quote=quote)
    
    
        
        
    
    
    security.declareProtected( permissions.View, 'fEncodingsCommonToLanguages')
    def fEncodingsCommonToLanguages(self, theCodigosIdiomas):
        if not theCodigosIdiomas:
            return []
        
        someEncodingsAndCounters = { }
        
        someEncodingNames = [ ]
        
        unNumEncodedIdiomas = 0
        
        for unCodigoIdioma in theCodigosIdiomas:

            unosEncodingsIdioma = self.fEncodingsForLanguage( unCodigoIdioma)
            if unosEncodingsIdioma:
                
                unNumEncodedIdiomas += 1

                for unEncodingIdioma in unosEncodingsIdioma:
                    
                    unNombreEncoding = unEncodingIdioma[ 0]
                    
                    if not ( unNombreEncoding in someEncodingNames):
                        someEncodingNames.append( unNombreEncoding)
                     
                    unCounterAndEncodingIdioma = someEncodingsAndCounters.get( unNombreEncoding, None)
                    if unCounterAndEncodingIdioma == None:
                        unCounterAndEncodingIdioma = [ 0, unEncodingIdioma,]
                        someEncodingsAndCounters[ unNombreEncoding] = unCounterAndEncodingIdioma
     
                    unCounterAndEncodingIdioma[ 0] += 1

        
        unosCommonEncodings = [ ]
        
        for unNombreEncoding in someEncodingNames:
            
            unCounterAndEncodingIdioma = someEncodingsAndCounters.get( unNombreEncoding, None)
            
            if len( unCounterAndEncodingIdioma) > 1:
                
                unCounter = unCounterAndEncodingIdioma[ 0]
                if unCounter == unNumEncodedIdiomas:
                    
                    unEncoding = unCounterAndEncodingIdioma[ 1]
                    unosCommonEncodings.append( unEncoding)
        
        return unosCommonEncodings
    
    
    
    
        
    security.declareProtected( permissions.View, 'fEncodingsForLanguage')
    def fEncodingsForLanguage(self, theCodigoIdioma):
        
        unCodigoIdioma, unCodigoCountry, unaVariation = self.fLanguageAndCountryAndVariationIdioma( theCodigoIdioma) 

        someEncodingsForAllLanguages = set( [ unE[ 0] for unE in cUTFEncodingsForAllLanguages])
        
        someEncodingsForAllLanguages.add( cTRAEncodingUnicodeEscape)
        
        someEncodingsForLanguage     = [ unE[:] for unE in cUTFEncodingsForAllLanguages]

        if not theCodigoIdioma:
            return someEncodingsForLanguage
        
        someTitlesByEncodingName = { }
        someAliasesByEncodingName = { }
        
        todosEncodings = set()
        
        someSpecificTRAEncodings = set()
        someWesternEncodings   = set()
        
        for unEncoding, unosAliasesString, unTitle, unosLanguageCodesString in cDefaultEncodingsSourceMap:
            unEncoding = unEncoding.strip().lower()
            if unEncoding and not ( unEncoding in someEncodingsForAllLanguages):
                if not (unEncoding in todosEncodings):
                    unCodecInfo = None
                    try:
                        unCodecInfo = CODECS_Lookup( unEncoding)
                    except:
                        None
                     
                    if unCodecInfo:
                        todosEncodings.add( unEncoding)
                        
                        if unTitle:
                            someTitlesByEncodingName[ unEncoding] = unTitle
                        
                        unosAliases = [ unAlias.strip() for unAlias in unosAliasesString.split( ',') if unAlias.strip()]
                        if unosAliases:
                            someAliasesByEncodingName[ unEncoding] = sorted( unosAliases)
                        
                        unosLanguageCodes = [ unLanguageCode.strip() for unLanguageCode in unosLanguageCodesString.split( ',') if unLanguageCode.strip()]
                        if unosLanguageCodes:
                            if cWesternLanguageMarkInSourceMap in unosLanguageCodes:
                                someWesternEncodings.add( unEncoding)   
                            if ( not ( unCodigoIdioma == cWesternLanguageMarkInSourceMap)) and ( ( theCodigoIdioma in unosLanguageCodes) or ( unCodigoIdioma in unosLanguageCodes)):
                                someSpecificTRAEncodings.add( unEncoding)   
                        else:
                            someWesternEncodings.add( unEncoding)   
                    
        if someSpecificTRAEncodings:
            someEncodingsForLanguage.append( [ cTRAEncodingSeparatorSentinelName, '', [], ])
            for aEncoding in sorted( someSpecificTRAEncodings):
                someEncodingsForLanguage.append( [ aEncoding, someTitlesByEncodingName.get( aEncoding, aEncoding), someAliasesByEncodingName.get( aEncoding, []), ])
            someEncodingsForLanguage.append( [ cTRAEncodingSeparatorSentinelName, '', [], ])
            for aEncoding in sorted( todosEncodings.difference( someSpecificTRAEncodings)):
                someEncodingsForLanguage.append( [ aEncoding, someTitlesByEncodingName.get( aEncoding, aEncoding), someAliasesByEncodingName.get( aEncoding, []), ])

        else:        
            someEncodingsForLanguage.append( [ cTRAEncodingSeparatorSentinelName, '', [], ])
            for aEncoding in sorted( someWesternEncodings):
                someEncodingsForLanguage.append( [ aEncoding, someTitlesByEncodingName.get( aEncoding, aEncoding), someAliasesByEncodingName.get( aEncoding, []), ])
            someEncodingsForLanguage.append( [ cTRAEncodingSeparatorSentinelName, '', [], ])
            for aEncoding in sorted( todosEncodings.difference( someWesternEncodings)):
                someEncodingsForLanguage.append( [ aEncoding, someTitlesByEncodingName.get( aEncoding, aEncoding), someAliasesByEncodingName.get( aEncoding, []), ])
        
        someEncodingsWithCompositeTitle = [ ]
        for unEncodingNameAndAliases in someEncodingsForLanguage:
            unCompositeTitle = ''
            if not ( unEncodingNameAndAliases[ 0] == cTRAEncodingSeparatorSentinelName):
                unCompositeTitle = unEncodingNameAndAliases[ 0]
                if unEncodingNameAndAliases[ 1] and not( unEncodingNameAndAliases[ 1] == unEncodingNameAndAliases[ 0]):
                    unCompositeTitle = '%s %s ' % ( unCompositeTitle, unEncodingNameAndAliases[ 1],)
                unosAliases = ' '.join( unEncodingNameAndAliases[ 2])
                if unosAliases and not( unosAliases == unEncodingNameAndAliases[ 0]) and not( unosAliases == unEncodingNameAndAliases[ 1]):
                    unCompositeTitle = '%s %s ' % ( unCompositeTitle, unosAliases,)
             
            someEncodingsWithCompositeTitle.append( [ 
                unEncodingNameAndAliases[ 0],
                unEncodingNameAndAliases[ 1],
                unEncodingNameAndAliases[ 2],
                unCompositeTitle,
            ])
        return someEncodingsWithCompositeTitle 
                
          
    

    
    


    security.declarePublic( 'fAsUnicode')
    def fAsUnicode( self, theString, theTranslationService=None):
        """Return the parameter, expected to be encoded in the plone site default encoding, decoded into a unicode string.
        
        """
        
        if not theString:
            return u''

        aTranslationService = theTranslationService
        if aTranslationService == None:
            aTranslationService = self.getTranslationServiceTool()

        if aTranslationService == None:
            return u'fAsUnicode() not svce'

        aUnicodeString = u''
        try:
            aUnicodeString = aTranslationService.asunicodetype( theString, errors="ignore")
        except:
            None
        
        return aUnicodeString
        
                
                
                




  
     
    security.declarePrivate( 'fSystemTextFileEncoding')    
    def fSystemTextFileEncoding( self, ):
        """System encoding.
        
        """
        return cSystemFileTextEncoding
    
     
    
    
    security.declarePrivate( 'fLogEncoding')    
    def fLogEncoding( self, ):
        return self.fSystemTextFileEncoding()
    
        
     
  