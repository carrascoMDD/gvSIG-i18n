# -*- coding: utf-8 -*-
#
# File: TRAUnicode.py
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



"""Utility module to assist the TRASplitter in breaking source strings into constituent words, normalized in case, to become keys for text search indexes.

"""


"""gUnicodeReplacements is 
An array with an element for each Unicode character at the index given by the character ord()
with a value 0 if the character is to be ignored (and thus, if appears, shall break current word)
if non 0, then the value is a replacement value for the character
if possitive, then the char is accepted and its replacement appended to the current word
if negative, then the char is accepted and its replacement appended as a new word, closing previous word if any, and opening a new empty word afterwards

Shall be lazily initialized as an array of zeroes, for the whole supported Unicode set.
For narrow Python builds: array with 0x110000 ( 1,114,112) elements
For narrow Python builds: array with 0x10000 ( 65536) elements

Original replacement values shall be the same character value
and applying exclusions from each character class in the unicodedata.category() of the char
plus some extra exclussions customized in TRAUnicode_Constants
replacements from unicode data upper/lower/title equivalence taken from the original UnicodeData.txt from unicode.org
extra replacements customized in TRAUnicode_Constants
"""

import unicodedata


from TRAUnicode_Constants import *



    
# ##########################################
"""Holder for the mapings array

"""    
gUnicodeReplacements_Holder  = [ None,]





"""
# source http://www.unicode.org/reports/tr44/tr44-4.html
# Table 10. General_Category Values
# Abbr 	Long 	Description
Lu 	Uppercase_Letter 	an uppercase letter
Ll 	Lowercase_Letter 	a lowercase letter
Lt 	Titlecase_Letter 	a digraphic character, with first part uppercase
Lm 	Modifier_Letter 	a modifier letter
Lo 	Other_Letter 	other letters, including syllables and ideographs
Mn 	Nonspacing_Mark 	a nonspacing combining mark (zero advance width)
Mc 	Spacing_Mark 	a spacing combining mark (positive advance width)
Me 	Enclosing_Mark 	an enclosing combining mark
Nd 	Decimal_Number 	a decimal digit
Nl 	Letter_Number 	a letterlike numeric character
No 	Other_Number 	a numeric character of other type
Pc 	Connector_Punctuation 	a connecting punctuation mark, like a tie
Pd 	Dash_Punctuation 	a dash or hyphen punctuation mark
Ps 	Open_Punctuation 	an opening punctuation mark (of a pair)
Pe 	Close_Punctuation 	a closing punctuation mark (of a pair)
Pi 	Initial_Punctuation 	an initial quotation mark
Pf 	Final_Punctuation 	a final quotation mark
Po 	Other_Punctuation 	a punctuation mark of other type
Sm 	Math_Symbol 	a symbol of primarily mathematical use
Sc 	Currency_Symbol 	a currency sign
Sk 	Modifier_Symbol 	a non-letterlike modifier symbol
So 	Other_Symbol 	a symbol of other type
Zs 	Space_Separator 	a space character (of various non-zero widths)
Zl 	Line_Separator 	U+2028 LINE SEPARATOR only
Zp 	Paragraph_Separator 	U+2029 PARAGRAPH SEPARATOR only
Cc 	Control 	a C0 or C1 control code
Cf 	Format 	a format control character
Cs 	Surrogate 	a surrogate code point
Co 	Private_Use 	a private-use character
Cn 	Unassigned 	a reserved unassigned code point or a noncharacter
"""

gfUnicodeCategory_Handlers = {
    'Lu': lambda aCharIndex: aCharIndex,
    'Ll': lambda aCharIndex: aCharIndex,
    'Lt': lambda aCharIndex: aCharIndex,
    'Lm': lambda aCharIndex: aCharIndex,
    'Lo': lambda aCharIndex: aCharIndex,
    'Mn': lambda aCharIndex: aCharIndex,
    'Mc': lambda aCharIndex: 0x0000,
    'Me': lambda aCharIndex: 0 - aCharIndex,
    'Nd': lambda aCharIndex: aCharIndex,
    'Nl': lambda aCharIndex: aCharIndex,
    'No': lambda aCharIndex: aCharIndex,
    'Pc': lambda aCharIndex: 0x0000,
    'Pd': lambda aCharIndex: 0x0000,
    'Ps': lambda aCharIndex: 0x0000,
    'Pe': lambda aCharIndex: 0x0000,
    'Pi': lambda aCharIndex: 0x0000,
    'Pf': lambda aCharIndex: 0x0000,
    'Po': lambda aCharIndex: 0x0000,
    'Sm': lambda aCharIndex: 0 - aCharIndex,
    'Sk': lambda aCharIndex: 0x0000,
    'So': lambda aCharIndex: 0 - aCharIndex,
    'Zs': lambda aCharIndex: 0x0000,
    'Zl': lambda aCharIndex: 0x0000,
    'Zp': lambda aCharIndex: 0x0000,
    'Cc': lambda aCharIndex: 0x0000,
    'Cf': lambda aCharIndex: 0x0000,
    'Cs': lambda aCharIndex: 0x0000,
    'Co': lambda aCharIndex: 0x0000,
    'Cn': lambda aCharIndex: 0x0000,
}



    

def fUnicodeReplacements():
    aUnicodeReplacementsHolder = globals().get( 'gUnicodeReplacements_Holder', None)
    
    if aUnicodeReplacementsHolder == None:
        return None
    
    if len( aUnicodeReplacementsHolder) < 1:
        return None
    
    someUnicodeReplacements = aUnicodeReplacementsHolder[ 0]
    if not ( someUnicodeReplacements == None):
        return someUnicodeReplacements

    
    # ##########################################
    """Init array to maximum unicode size
    
    """      
    someUnicodeReplacements = [ 0x00] * ( cUnicode_Limit + 1)
    aUnicodeReplacementsHolder[ 0] = someUnicodeReplacements
    
    # ##########################################
    """Apply unicode data category mappings
    
    """
    for aCharIndex in xrange( 1, cUnicode_Limit):
        aUniChr = unichr( aCharIndex)
        aCategory = unicodedata.category( aUniChr)
        if aCategory:
            aCategoryHandler = gfUnicodeCategory_Handlers.get( aCategory, None)
            if aCategoryHandler:
                aCategorizedCharIndex = aCategoryHandler( aCharIndex)
                if aCategorizedCharIndex:
                    someUnicodeReplacements[ aCharIndex] = aCategorizedCharIndex
        
                
                
    # ##########################################
    """Apply standard unicode data uppercase mappings
    
    """
    for aUnicodeToUpperCase in cUnicode_ToUpperCase_Standard_Mappings:
        if len( aUnicodeToUpperCase) > 1:
            aLowercaseIndex = aUnicodeToUpperCase[ 0]
            aUppercaseIndex = aUnicodeToUpperCase[ 1]
            if aLowercaseIndex and aUppercaseIndex and ( aLowercaseIndex < cUnicode_Limit) and ( aUppercaseIndex < cUnicode_Limit):
                aCurrentReplacement = someUnicodeReplacements[ aLowercaseIndex]
                if aCurrentReplacement:
                    if aCurrentReplacement < 0:
                        someUnicodeReplacements[ aLowercaseIndex] = 0 - aUppercaseIndex
                    else:
                        someUnicodeReplacements[ aLowercaseIndex] = aUppercaseIndex
                        
                
    # ##########################################
    """Apply overrides to standard unicode data caterorizations
    
    """
    for aUnicodeOverride in cUnicode_Categorizations_Override_Mappings:
        if len( aUnicodeOverride) > 1:
            aOverriddenIndex = aUnicodeOverride[ 0]
            aOverridingIndex = aUnicodeOverride[ 1]
            if aOverriddenIndex and aOverridingIndex and ( aOverriddenIndex < cUnicode_Limit) and ( aOverridingIndex < cUnicode_Limit):
                someUnicodeReplacements[ aOverriddenIndex] = aOverridingIndex
                        
                        
    # ##########################################
    """Apply extra unicode data uppercase mappings
    
    """
    for someToUpperCase_Mappings in cUnicode_ToUpperCase_Extra_Mappings:
        
        if someToUpperCase_Mappings:
            
            someReplacementCharIndexes = someToUpperCase_Mappings.keys()
            for aReplacementCharIndex in someReplacementCharIndexes:
                someReplacedCharIndexes = someToUpperCase_Mappings.get( aReplacementCharIndex, [])
                if someReplacedCharIndexes:
                    for aReplacedCharIndex in someReplacedCharIndexes:

                        if aReplacedCharIndex:
                            aCurrentReplacement = someUnicodeReplacements[ aReplacedCharIndex]
                            if aCurrentReplacement:
                                if aCurrentReplacement < 0:
                                    someUnicodeReplacements[ aReplacedCharIndex] = 0 - aReplacementCharIndex
                                else:
                                    someUnicodeReplacements[ aReplacedCharIndex] = aReplacementCharIndex
                        
        
    return someUnicodeReplacements
        
        