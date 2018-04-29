# -*- coding: utf-8 -*-
#
# File: TRASplitter.py
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



from StringIO import StringIO

from Products.ZCTextIndex.ISplitter import ISplitter
from Products.ZCTextIndex.PipelineFactory import element_factory


from types import UnicodeType 



from TRAUnicode           import fUnicodeReplacements
from TRAUnicode_Constants import cUnicode_Limit




cSplitterWildcards = [ u'*', u'?',]



def getSupportedEncoding(encodings):
    return 'utf-8'

# unichr ord hex  




class TRASplitter:
      
    
    default_encoding = "utf-8"

    
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
        if not theString:
            return []
        
        someUnicodeReplacements = fUnicodeReplacements( )
        if not someUnicodeReplacements:
            return [ theString,]
        
        someResultWordStrings = [ ]
        
        aStream = StringIO( u'')
        
        for aChar in theString:
            
            if ( aChar in cSplitterWildcards):
                if theIsGlob:
                    aCurrentWordString = aStream.getvalue()
                    if aCurrentWordString:
                        aWordWithWildcard = '%s%s' % ( aCurrentWordString, aChar,)
                        someResultWordStrings.append( aWordWithWildcard)
                        aStream.close()
                        aStream = StringIO( u'')
                        
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
    
        
    
    
    
    #def process_old(self, theStringsList, theIsGlob=False):
        #someResultWordStrings = []
        #if not theStringsList:
            #return someResultWordStrings
        
        #aDefaultEncoding = self.default_encoding
        #for aString in theStringsList:
            #if aString:
                #aUnicodeString = aString
                #if not isinstance( aString, UnicodeType):
                    #aUnicodeString = unicode( aString, aDefaultEncoding, 'replace')
                
                #if aUnicodeString:
                    #aReplacedString = self.fReplaceStringChars( aUnicodeString)
            
                    #if aReplacedString:
                        
                        #someWords = self.fSplitWords( aReplacedString, theIsGlob)
                        #if someWords:
                            #someResultWordStrings.extend( someWords)
                            
        #return someResultWordStrings
    
        
    
    #def fReplaceStringChars(self, theString):
        #if not theString:
            #return theString
        
        #aReplacementsMap = self.fSplitterCompiledReplacements()
        
        #aStream = StringIO( u'')
        
        #for aChar in theString:
            #anOrdValue = ord( aChar)
            #aReplacementOrdValue = aReplacementsMap.get( anOrdValue, 0)
            #if aReplacementOrdValue:
                #aReplacementChar = unichr( aReplacementOrdValue)
                #aStream.write( aReplacementChar)
            #else:
                #aStream.write( aChar)
         
        #aReplacedString = aStream.getvalue()
        #return aReplacedString
    

        
        
        
        
        
    #def fSplitterCompiledReplacements(self,):
        #if not(  TRASplitter.gSplitterCompiledReplacements == None):
            #return TRASplitter.gSplitterCompiledReplacements
        
        #TRASplitter.gSplitterCompiledReplacements = { }
        
        #someSplitterUnicodeRanges = cSplitterUnicodeRanges
        #for aSplitterUnicodeRange in someSplitterUnicodeRanges:
            #aReplacementsMap = aSplitterUnicodeRange.get( cSplitterKey_Replaced, None)
            #if aReplacementsMap:
                #someReplacementChars = aReplacementsMap.keys()
                #for aReplacementChar in someReplacementChars:
                    #someReplacedChars = aReplacementsMap.get( aReplacementChar, [])
                    #if someReplacedChars:
                        #aReplacementOrdValue = ord( aReplacementChar)                        
                        #for aReplacedChar in someReplacedChars:
                            #aReplacedOrdValue = 0
                            #try:
                                #aReplacedOrdValue = ord( aReplacedChar)
                            #except:
                                #None
                            #if aReplacedOrdValue:
                                #TRASplitter.gSplitterCompiledReplacements[ aReplacedOrdValue] = aReplacementOrdValue
            
        #return TRASplitter.gSplitterCompiledReplacements
        
    
       
    
    
    #def fSplitWords(self, theString, theIsGlob=False):
        #if not theString:
            #return []
        
        #someUnicodeRanges = self.fSplitterCompiledUnicodeRanges( )
        #someResultWordStrings = [ ]
        
        #aStream = StringIO( u'')
        
        #for aChar in theString:
            
            #if ( aChar in cSplitterWildcards):
                #if theIsGlob:
                    #aCurrentWordString = aStream.getvalue()
                    #if aCurrentWordString:
                        #aWordWithWildcard = '%s%s' % ( aCurrentWordString, aChar,)
                        #someResultWordStrings.append( aWordWithWildcard)
                        #aStream.close()
                        #aStream = StringIO( u'')
                        
                #else:
                    #aCurrentWordString = aStream.getvalue()
                    #if aCurrentWordString:
                        #someResultWordStrings.append( aCurrentWordString)
                        #aStream.close()
                        #aStream = StringIO( u'')
                    
            #else:   
                #anOrdValue = ord( aChar)
                #aUnicodeRange = self.fUnicodeRange( anOrdValue, someUnicodeRanges)
                
                #if ( not aUnicodeRange) or ( len( aUnicodeRange) < 3)  or (not aUnicodeRange[0]): # out of range
                    #aCurrentWordString = aStream.getvalue()
                    #if aCurrentWordString:
                        #someResultWordStrings.append( aCurrentWordString)
                        #aStream.close()
                        #aStream = StringIO( u'')
                    
                #elif not aUnicodeRange[1]: # Rejected
                    #aCurrentWordString = aStream.getvalue()
                    #if aCurrentWordString:
                        #someResultWordStrings.append( aCurrentWordString)
                        #aStream.close()
                        #aStream = StringIO( u'')
                    
                #elif aUnicodeRange[2]: # Concatenate in words
                    #aStream.write( aChar)
                        
                #else:  # Single Char symbol
                    #aCurrentWordString = aStream.getvalue()
                    #if aCurrentWordString:
                        #someResultWordStrings.append( aCurrentWordString)
                        #aStream.close()
                        #aStream = StringIO( u'')
                    #someResultWordStrings.append( aChar)
                
        #aCurrentWordString = aStream.getvalue()
        #if aCurrentWordString:
            #someResultWordStrings.append( aCurrentWordString)
                
        #aStream.close()
        
        #return someResultWordStrings
    
    
    
    
    #def fUnicodeRange( self, theOrdValue, theUnicodeRanges):
        #if ( not theOrdValue) or ( not theUnicodeRanges):
            #return None
        
        #aTopRange = theUnicodeRanges[ 0]
        #aTopOrdValue = aTopRange[ 0]
        #if theOrdValue < aTopOrdValue:
            #return None
        
        #aNumRanges = len( theUnicodeRanges)
        
        #aBottomRange = theUnicodeRanges[ aNumRanges - 1]
        #aBottomOrdValue = aBottomRange[ 0]
        #if theOrdValue >= aBottomOrdValue:
            #return aBottomRange
        
        #aTopRangeIndex = 0
        #aBottomRangeIndex = aNumRanges - 1
        
        #while ( aBottomRangeIndex - aTopRangeIndex) >= 0:
            
            #aMidRangeIndex = int( ( aTopRangeIndex + aBottomRangeIndex) / 2)
            #aMidRange = theUnicodeRanges[ aMidRangeIndex]
            #aRangeOrdValue = aMidRange[ 0]

            #if theOrdValue < aRangeOrdValue:
                #aBottomRangeIndex = aMidRangeIndex - 1
            
            #elif ( theOrdValue == aRangeOrdValue) or ( ( theOrdValue > aRangeOrdValue) and ( ( aMidRangeIndex < ( aNumRanges - 1)) and (  theOrdValue < ( theUnicodeRanges[ aMidRangeIndex + 1][ 0]) ))):
                #return aMidRange
            
            #else:
                #aTopRangeIndex = aMidRangeIndex + 1
            
        #return None
    
                
        
                
        
        
    #def fSplitterCompiledUnicodeRanges(self,):
        #if not ( TRASplitter.gSplitterCompiledUnicodeRanges == None):
            #return TRASplitter.gSplitterCompiledUnicodeRanges
        
        #return cSplitterCompiledUnicodeRanges_Example
    
    
    
    

try:
    element_factory.registerFactory('Word Splitter',
          'gvSIG-i18n splitter', TRASplitter)
except:# ValueError:
    # in case the splitter is already registered, ValueError is raised
    pass    

