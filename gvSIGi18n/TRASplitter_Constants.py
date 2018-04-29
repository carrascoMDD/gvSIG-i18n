# -*- coding: utf-8 -*-
#
# File: TRASplitter_Constants.py
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




cSplitterWildcards = [ u'*', u'?',]


cSplitterKey_Active     = 'active'
cSplitterKey_Name       = 'name'
cSplitterKey_Accepted   = 'accepted'
cSplitterKey_CharSymbols= 'charsymbols'
cSplitterKey_Rejected   = 'rejected'
cSplitterKey_Replaced   = 'replaced'




# http://www.unicode.org/charts/PDF/U0000.pdf
# http://www.unicode.org/charts/PDF/U0080.pdf
# http://www.unicode.org/charts/PDF/U0100.pdf
# http://www.unicode.org/charts/PDF/U0180.pdf
# http://www.unicode.org/charts/PDF/U2C60.pdf
# http://www.unicode.org/charts/PDF/UA720.pdf
# http://www.unicode.org/charts/PDF/U1E00.pdf
#
cSplitterUnicodeRanges_BasicLatin = {
    cSplitterKey_Active:    True,
    cSplitterKey_Name:      'Basic Latin',
    cSplitterKey_Accepted:  [ [u'0',u'9'], [u'A',u'Z'], [u'a',u'z'], ],
    cSplitterKey_CharSymbols: [ [u'!',u')'], [u'+',u"""/"""], [u':',u'>'], [u'[',u"""`"""], [u'{',u'~']  ],
    cSplitterKey_Rejected:  [ ],
    cSplitterKey_Replaced:  { #Replacement char: replaced char or list of replaced chars
        u'\u0041': [ u'\u0061',u'\u00C0',u'\u00C1',u'\u00C2',u'\u00C3',u'\u00C4',u'\u00C5',u'\u00C6',u'\u00E0',u'\u00E1',u'\u00E2',u'\u00E3',u'\u00E4',u'\u00E5',u'\u00E6', u'\u00C6',u'\u00E6',u'\u0100',u'\u0101',u'\u0102',u'\u0103',u'\u0104',u'\u0105'],     # A
        u'\u0042': [ u'\u0062',],     # B
        u'\u0043': [ u'\u0063',u'\u00C7',u'\u00E7',u'\u0106',u'\u0107',u'\u0108',u'\u0109',u'\u010A',u'\u010B',u'\u010C',u'\u010D',],     # C
        u'\u0044': [ u'\u0064',u'\u00D0',u'\u010E',u'\u010F',u'\u0110',u'\u0111'],     # D
        u'\u0045': [ u'\u0065',u'\u00C8',u'\u00C9',u'\u00CA',u'\u00CB',u'\u00E8',u'\u00E9',u'\u00EA',u'\u00EB',u'\u0112',u'\u0113',u'\u0114',u'\u0115',u'\u0116',u'\u0117',u'\u0118',u'\u0119',u'\u011A',u'\u011B'],     # E
        u'\u0046': [ u'\u0066',u'\u017F'],     # F
        u'\u0047': [ u'\u0067',u'\u011C',u'\u011D',u'\u011E',u'\u011F',u'\u0120',u'\u0121',u'\u0122',u'\u0123'],     # G
        u'\u0048': [ u'\u0068',u'\u0124',u'\u0125',u'\u0126',u'\u0127',],     # H
        u'\u0049': [ u'\u0069',u'\u00CC',u'\u00CD',u'\u00CE',u'\u00CF',u'\u00EC',u'\u00ED',u'\u00EE',u'\u00EF',u'\u0128',u'\u0129',u'\u012A',u'\u012B',u'\u012C',u'\u012D',u'\u012E',u'\u012F',u'\u0130',u'\u0131',u'\u0132',u'\u0133',],     # I
        u'\u004A': [ u'\u006A',u'\u0134',u'\u0135',],     # J
        u'\u004B': [ u'\u006B',u'\u0136',u'\u0137',u'\u0138',],     # K
        u'\u004C': [ u'\u006C',u'\u0139',u'\u013A',u'\u013B',u'\u013C',u'\u013D',u'\u013E',u'\u013F',u'\u0140',u'\u0141',u'\u0142',],     # L
        u'\u004D': [ u'\u006D',],     # M
        u'\u004E': [ u'\u006E',u'\u00D1',u'\u00F1',u'\u0143',u'\u0144',u'\u0145',u'\u0146',u'\u0147',u'\u0148',u'\u0149',u'\u014A',u'\u014B'],     # N
        u'\u004F': [ u'\u006F',u'\u00D2',u'\u00D3',u'\u00D4',u'\u00D5',u'\u00D6',u'\u00F2',u'\u00F3',u'\u00F4',u'\u00F5',u'\u00F6',u'\u00D8',u'\u00F8',u'\u014C',u'\u014D',u'\u014E',u'\u014F',u'\u0150',u'\u0151',u'\u0152',u'\u0153'],     # O
        u'\u0050': [ u'\u0070',],     # P
        u'\u0051': [ u'\u0071',],     # Q
        u'\u0052': [ u'\u0072',u'\u0154',u'\u0155',u'\u0156',u'\u0157',u'\u0158',u'\u0159'],     # R
        u'\u0053': [ u'\u0073',u'\u015A',u'\u015B',u'\u015C',u'\u015D',u'\u015E',u'\u015F',u'\u0160',u'\u0161'],     # S
        u'\u0054': [ u'\u0074',u'\u0162',u'\u0163',u'\u0164',u'\u0165',u'\u0166',u'\u0167',],     # T
        u'\u0055': [ u'\u0075',u'\u00D9',u'\u00DA',u'\u00DB',u'\u00DC',u'\u00F9',u'\u00FA',u'\u00FB',u'\u00FC',u'\u0168',u'\u0168',u'\u0169',u'\u016A',u'\u016B',u'\u016C',u'\u016D',u'\u016E',u'\u016F',u'\u0170',u'\u0171',u'\u0172',u'\u0173'],     # U
        u'\u0056': [ u'\u0076',],     # V
        u'\u0057': [ u'\u0077',u'\u0174',u'\u0175'],     # W
        u'\u0058': [ u'\u0078',],     # X
        u'\u0059': [ u'\u0079',u'\u00DD',u'\u00FD',u'\u00FF',u'\u0176',u'\u0177',u'\u0178',],     # Y
        u'\u005A': [ u'\u007A',u'\u0179',u'\u017A',u'\u017B',u'\u017C',u'\u017D',u'\u017E'],     # Z
    },
}

# http://www.unicode.org/charts/PDF/U0370.pdf
cSplitterUnicodeRanges_Greek = {
    cSplitterKey_Active:    True,
    cSplitterKey_Name:      'Greek',
    cSplitterKey_Accepted:  [ [u'\u0370', u'\u03ff'], ],
    cSplitterKey_Rejected:  [ [u'\u0378', u'\u0385'],  u'\u0387', u'\u038B', u'\u038D', u'\u03A2', [u'\u03FD', u'\u03FF'] ],
    cSplitterKey_Replaced:  { #Replacement char: replaced char or list of replaced chars
        u'\u0370': [ u'\u0371',],     # HETA
        u'\u0372': [ u'\u0373',],     # ARCHAIC SAMPI
        u'\u0374': [ u'\u0375',],     # NUMERAL SIGN
        u'\u0376': [ u'\u0377',],     # ARCHAIC PAMPHILIAN DIGAMMA
        u'\u0391': [ u'\u0386',u'\u03AC',u'\u03B1'], # ALPHA
        u'\u0392': [ u'\u03B2', u'\u03D0'], # BETA
        u'\u0393': [ u'\u03B3',], # GAMMA
        u'\u0394': [ u'\u03B4',], # DELTA
        u'\u0395': [ u'\u0388',u'\u03AD',u'\u03B5', u'\u03F5', u'\u03F6'], # EPSILON
        u'\u0396': [ u'\u03B6',], # ZETA
        u'\u0397': [ u'\u0389',u'\u03AE',u'\u03B7'], # ETA
        u'\u0398': [ u'\u03B8',u'\u03D1',u'\u03F4'], # THETA
        u'\u0399': [ u'\u038A',u'\u0390',u'\u03AA',u'\u03AF',u'\u03B9',u'\u03CA'], # IOTA
        u'\u039A': [ u'\u03BA',u'\u03F0'], # KAPPA
        u'\u039B': [ u'\u03BB',], # LAMBDA
        u'\u039C': [ u'\u03BC',], # MU
        u'\u039D': [ u'\u03BD',], # NU
        u'\u039E': [ u'\u03BE',], # XI        
        u'\u039F': [ u'\u038C', u'\u03BF',u'\u03CC'], # OMICRON
        u'\u03A0': [ u'\u03C0', u'\u03D6'], # PI
        u'\u03A1': [ u'\u03C1',u'\u03F1',u'\u03FC'], # RHO
        u'\u03A3': [ u'\u03C2',u'\u03C3',u'\u03F2',u'\u03F9'], # SIGMA
        u'\u03A4': [ u'\u03C4',], # TAU
        u'\u03A5': [ u'\u038E',u'\u03AB',u'\u03B0',u'\u03C5',u'\u03CB',u'\u03CD', u'\u03D2', u'\u03D3', u'\u03D4'], # UPSILON
        u'\u03A6': [ u'\u03C6',u'\u03D5'], # PHI
        u'\u03A7': [ u'\u03C7',], # CHI
        u'\u03A8': [ u'\u03C8',], # PSI
        u'\u03A9': [ u'\u038F',u'\u03C9',u'\u03CE'], # OMEGA
        u'\u03CF': [ u'\u03D7',], # KAI SYMBOL
        u'\u03D8': [ u'\u03D9',], # ARCHAIC KOPPA
        u'\u03DA': [ u'\u03DB',], # ARCHAIC STIGMA
        u'\u03DC': [ u'\u03DD',], # ARCHAIC DIGAMMA
        u'\u03DE': [ u'\u03DF',], # KOPPA
        u'\u03E0': [ u'\u03E1',], # SAMPI
        u'\u03E2': [ u'\u03E3',],  # COPTIC SHEI
        u'\u03E4': [ u'\u03E5',],  # COPTIC FEI
        u'\u03E6': [ u'\u03E7',],  # COPTIC KHEI
        u'\u03E8': [ u'\u03E9',],  # COPTIC HORI
        u'\u03EA': [ u'\u03EB',],  # COPTIC GANGIA
        u'\u03EC': [ u'\u03ED',],  # COPTIC SHIMA
        u'\u03EE': [ u'\u03EF',],  # COPTIC DEI
        u'\u03F7': [ u'\u03F8',],  # BACTRIAN SHO
        u'\u03FA': [ u'\u03FB',], # ARCHAIC SAN
        
    },
}



# http://www.unicode.org/charts/PDF/U0400.pdf
cSplitterUnicodeRanges_Cyrillic = {
    cSplitterKey_Active:    True,
    cSplitterKey_Name:      'Cyrillic',
    cSplitterKey_Accepted:  [ [u'\u0400', u'\u04ff'], ],
    cSplitterKey_Rejected:  [ [u'\u0482', u'\u0489'] ],
    cSplitterKey_Replaced:  { #Replacement char: replaced char or list of replaced chars
    },
}



cSplitterUnicodeRanges = [ 
    cSplitterUnicodeRanges_BasicLatin,
    cSplitterUnicodeRanges_Greek,
    cSplitterUnicodeRanges_Cyrillic,    
]



# start of the range: ord() of first unicode char in range, Accepted, Concatenate in words, source range names
cSplitterCompiledUnicodeRanges_Example = [
    [ 0x0021, True,   False, [ 'Basic Latin',],], # accept from ! to ) as char symbols
    [ 0x002A, False,  False, [ 'Basic Latin',],], # reject *
    [ 0x002B, True,   False, [ 'Basic Latin',],], # accept from + to / as char symbols
    [ 0x0030, True,   True,  [ 'Basic Latin',],], # accept from 0 to 9 as word forming
    [ 0x003A, True,   False, [ 'Basic Latin',],], # accept from : to > as char symbols
    [ 0x003F, False,  False, [ 'Basic Latin',],], # reject ?
    [ 0x0040, True,   True,  [ 'Basic Latin',],], # accept from @ to Z as word forming
    [ 0x005B, True,   False, [ 'Basic Latin',],], # accept from [ to ` as char symbols
    [ 0x0061, True,   True,  [ 'Basic Latin',],], # accept from a to z as word forming
    [ 0x007B, True,   False, [ 'Basic Latin',],], # accept from { to ~ as char symbols
    [ 0x007F, False,  False, [ 'Basic Latin',],], # reject
    
    
    [ 0x00A1, True,   False, [ 'Latin-1 Supplement',],], # accept char symbols
    [ 0x00AD, False,  False, [ 'Latin-1 Supplement',],], # reject
    [ 0x00AE, True,   False, [ 'Latin-1 Supplement',],], # accept char symbols
    [ 0x00B4, False,  False, [ 'Latin-1 Supplement',],], # reject
    [ 0x00B5, True,   False, [ 'Latin-1 Supplement',],], # accept char symbols
    [ 0x00B7, False,  False, [ 'Latin-1 Supplement',],], # reject
    [ 0x00B9, True,   False, [ 'Latin-1 Supplement',],], # accept char symbols
    [ 0x00C0, True,   True,  [ 'Latin-1 Supplement',],], # accept as word forming
    [ 0x00D7, True,   False, [ 'Latin-1 Supplement',],], # accept char symbols
    [ 0x00D8, True,   True,  [ 'Latin-1 Supplement',],], # accept as word forming
    [ 0x00F7, True,   False, [ 'Latin-1 Supplement',],], # accept char symbols
    [ 0x00F8, True,   True,  [ 'Latin-1 Supplement',],], # accept as word forming
    
    [ 0x0100, True,   True,  [ 'Latin Extended A',],], # accept as word forming
      
    [ 0x0180, True,   True,  [ 'Latin Extended B',],], # accept as word forming
    [ 0x0250, False,  False, [ 'Latin Extended B',],], # reject
    
    [ 0x0370, True,   True,  [ 'Greek',],],       # accept as word forming
    [ 0x0378, False,  False, [ 'Greek',],],       # reject
    [ 0x0386, True,   True,  [ 'Greek',],],       # accept as word forming
    [ 0x0387, False,  False, [ 'Greek',],],       # reject
    [ 0x0388, True,   True,  [ 'Greek',],],       # accept as word forming
    [ 0x038D, False,  False, [ 'Greek',],],       # reject
    [ 0x038E, True,   True,  [ 'Greek',],],       # accept as word forming
    [ 0x03A2, False,  False, [ 'Greek',],],       # reject
    [ 0x03A3, True,   True,  [ 'Greek',],],       # accept as word forming
    [ 0x03FD, False,  False, [ 'Greek',],],       # reject
    
    
    [ 0x0400, True,   True,  [ 'Cyrillic',],],    # accept as word forming
    [ 0x0482, False,  False, [ 'Cyrillic',],],    # reject
    [ 0x048A, True,   True,  [ 'Cyrillic',],],    # accept as word forming
    [ 0x04FF, False,  False, [ 'Cyrillic',],],    # reject
    
    [ 0x1E00, True,   True,  [ 'Latin Extended Additional',],], # accept as word forming
    [ 0x1F00, False,  False, [ 'Latin Extended Additional',],], # reject
    
    [ 0x2C60, True,   True,  [ 'Latin Extended C',],], # accept as word forming
    [ 0x2C90, False,  False, [ 'Latin Extended C',],], # reject

    [ 0xA726, True,   True,  [ 'Latin Extended D',],], # accept as word forming
    [ 0xA788, False,  False, [ 'Latin Extended D',],], # reject

    
]


cSplitterCompiledReplacemens_Example = {
    0x0371: 0x0370,
    0x0373: 0x0372,
    0x0375: 0x0374,
    0x0377: 0x0376,
    0x0386: 0x0391,
    0x03AC: 0x0391,
    0x03B1: 0x0391,
    
    
}
