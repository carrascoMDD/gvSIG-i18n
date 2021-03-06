# -*- coding: utf-8 -*-
#
# File: TRASplitter.py
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



from StringIO import StringIO

from Products.ZCTextIndex.ISplitter import ISplitter
from Products.ZCTextIndex.PipelineFactory import element_factory


from types import UnicodeType 


from TRAUnicode           import fUnicodeReplacements
from TRAUnicode_Constants import cUnicode_Limit






cTRASplitterDefaultEncoding = 'utf-8'


cTRASplitterWildcards = [ u'*', u'?',]


cTRASplitterParenthesis_Open  = [ u'(',]
cTRASplitterParenthesis_Close = [ u')',]

cTRASplitterParenthesis = cTRASplitterParenthesis_Open + cTRASplitterParenthesis_Close

cTRASplitterNegate = [ u'-',]


cTRASplitterDoubleQuote = [ u'"',]


cTRASplitterAllSpecialChars = cTRASplitterWildcards + cTRASplitterParenthesis + cTRASplitterNegate + cTRASplitterDoubleQuote


def getSupportedEncoding(encodings):
    return cTRASplitterDefaultEncoding

# unichr ord hex  




def fgReplaceCharsAndSplitWords_asUnicode( theString, theIsGlob=False):
    if not theString:
        return []
    
    someUnicodeReplacements = fUnicodeReplacements( )
    if not someUnicodeReplacements:
        return [ theString,]
    
    someResultWordStrings = [ ]
    
    aStream = StringIO( u'')
    
    for aChar in theString:
        
        
        if aChar in cTRASplitterAllSpecialChars:
            if theIsGlob:

                # BEGIN ACV 20110209 Fix bug preventing the use of wildcards in search criteria
                aStream.write( aChar)
                
                #aCurrentWordString = aStream.getvalue()
                #if aCurrentWordString:
                    #aWordWithWildcard = '%s%s' % ( aCurrentWordString, aChar,)
                    #someResultWordStrings.append( aWordWithWildcard)
                    #aStream.close()
                    #aStream = StringIO( u'')
                    
                # END ACV 20110209 Fix bug preventing the use of wildcards in search criteria
                    
            else:
                aCurrentWordString = aStream.getvalue()
                if aCurrentWordString:
                    someResultWordStrings.append( aCurrentWordString)
                    aStream.close()
                    aStream = StringIO( u'')
                    

                    
        else:   
            aCharIndex = ord( aChar)
            if aCharIndex and ( aCharIndex < cUnicode_Limit):
                
                aReplacementCharIndex = someUnicodeReplacements[ aCharIndex]
                
                if not aReplacementCharIndex: # out of range
                    aCurrentWordString = aStream.getvalue()
                    if aCurrentWordString:
                        someResultWordStrings.append( aCurrentWordString)
                        aStream.close()
                        aStream = StringIO( u'')
                   
                elif aReplacementCharIndex > 0: # Concatenate in words
                    aStream.write( unichr( aReplacementCharIndex))
                        
                else:  # Single Char symbol
                    aCurrentWordString = aStream.getvalue()
                    if aCurrentWordString:
                        someResultWordStrings.append( aCurrentWordString)
                        aStream.close()
                        aStream = StringIO( u'')
                    someResultWordStrings.append( unichr( 0 - aReplacementCharIndex))
            
    aCurrentWordString = aStream.getvalue()
    if aCurrentWordString:
        someResultWordStrings.append( aCurrentWordString)
            
    aStream.close()
    
    return someResultWordStrings

    



def fgReplaceCharsAndSplitWords_asDefaultEncoding( theString, theIsGlob=False):
    
    someUnicodeWordStrings = fgReplaceCharsAndSplitWords_asUnicode( theString, theIsGlob)
    
    if not someUnicodeWordStrings:
        return []
    
    someDefaultEncodingWordStrings = [ ]
    
    for aUnicodeWordString in someUnicodeWordStrings:
        if aUnicodeWordString:
            
            if not isinstance( aUnicodeWordString, UnicodeType):
                someDefaultEncodingWordStrings.append( aUnicodeWordString)
            else:
                
                aDefaultEncodingWordString = aUnicodeWordString.encode( cTRASplitterDefaultEncoding, 'replace')
                if aDefaultEncodingWordString:
                    someDefaultEncodingWordStrings.append( aDefaultEncodingWordString)
    
    return someDefaultEncodingWordStrings






class TRASplitter:
      
    __implements__ = ISplitter
    
    

    default_encoding = cTRASplitterDefaultEncoding

    
    def processGlob(self, theStringsList, theIsGlob=False):
        return self.process( theStringsList, True)
    
    
    def process(self, theStringsList, theIsGlob=False):
        someResultWordStrings = []
        if not theStringsList:
            return someResultWordStrings
        
        aDefaultEncoding = self.default_encoding
        for aString in theStringsList:
            if aString:
                aUnicodeString = aString
                if not isinstance( aString, UnicodeType):
                    aUnicodeString = unicode( aString, aDefaultEncoding, 'replace')
                
                if aUnicodeString:
                    someWords = self.fReplaceCharsAndSplitWords( aUnicodeString, theIsGlob)
                    if someWords:
                        someResultWordStrings.extend( someWords)
                            
        return someResultWordStrings
    
    
    
    
    

    
    def fReplaceCharsAndSplitWords(self, theString, theIsGlob=False):
        return fgReplaceCharsAndSplitWords_asUnicode( theString, theIsGlob)
    
    

    
    
    

try:
    element_factory.registerFactory('Word Splitter',
          'gvSIG-i18n splitter', TRASplitter)
except:# ValueError:
    # in case the splitter is already registered, ValueError is raised
    pass    

