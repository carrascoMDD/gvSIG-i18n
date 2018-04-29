# -*- coding: utf-8 -*-
#
# File: TRAImportarExportar_Constants.py
#
# Copyright (c) 2008, 2009 by Conselleria de Infraestructuras y Transporte de la
# Generalidad Valenciana
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


from TRAElemento_Constants import *


# ##############################################
# Handling modes for of export encoding errors

cEncodingErrorHandleMode_CancelOnFirstError             = 'Cancelar al primer error'
cEncodingErrorHandleMode_CountAllErrorsAndCancel        = 'Contar todos los errores y cancelar'
cEncodingErrorHandleMode_IgnoreAndContinue              = 'Ignorar y continuar'
cEncodingErrorHandleMode_ReplaceAndContinue             = 'Sustituir y continuar'
cEncodingErrorHandleMode_XMLReplaceAndContinue          = 'Sustituir por XML y continuar'
cEncodingErrorHandleMode_BackslashReplaceAndContinue    = 'Sustituir por escape y continuar'


cPseudoSimboloError_Header = '--EncodingErrorWritingFileHeader--'

cEncodedFileErrorsModeByEncodingErrorHandleMode = {
    cEncodingErrorHandleMode_CancelOnFirstError:            'strict',
    cEncodingErrorHandleMode_CountAllErrorsAndCancel:       'strict',
    cEncodingErrorHandleMode_IgnoreAndContinue:             'ignore',
    cEncodingErrorHandleMode_ReplaceAndContinue:            'replace',
    cEncodingErrorHandleMode_XMLReplaceAndContinue:         'xmlcharrefreplace',
    cEncodingErrorHandleMode_BackslashReplaceAndContinue:   'backslashreplace',
}
cDefaultEncodedFileErrorsMode = 'strict'


cSystemToUnicodeErrorsModeByEncodingErrorHandleMode = {
    cEncodingErrorHandleMode_CancelOnFirstError:            'strict',
    cEncodingErrorHandleMode_CountAllErrorsAndCancel:       'strict',
    cEncodingErrorHandleMode_IgnoreAndContinue:             'ignore',
    cEncodingErrorHandleMode_ReplaceAndContinue:            'replace',
    cEncodingErrorHandleMode_XMLReplaceAndContinue:         'xmlcharrefreplace',
    cEncodingErrorHandleMode_BackslashReplaceAndContinue:   'backslashreplace',
}
cDefaultSystemToUnicodeErrorsMode = 'strict'


cUnicodeToUTF8ErrorsModeByEncodingErrorHandleMode = {
    cEncodingErrorHandleMode_CancelOnFirstError:            'strict',
    cEncodingErrorHandleMode_CountAllErrorsAndCancel:       'strict',
    cEncodingErrorHandleMode_IgnoreAndContinue:             'ignore',
    cEncodingErrorHandleMode_ReplaceAndContinue:            'replace',
    cEncodingErrorHandleMode_XMLReplaceAndContinue:         'xmlcharrefreplace',
    cEncodingErrorHandleMode_BackslashReplaceAndContinue:   'backslashreplace',
}
cDefaultUnicodeToUTF8ErrorsMode = 'strict'


# ##############################################
# Status names for export errors


cExportStatus_NoLanguagesRequestedForExport = 'gvSIGi18n_ExportStatus_NoLanguagesRequestedForExport'
cExportStatus_NoModulesRequestedForExport   = 'gvSIGi18n_ExportStatus_NoModulesRequestedForExport'
cExportStatus_Exception                     = 'gvSIGi18n_ExportStatus_Exception'
cExportStatus_UseCaseAssessmentFailed       = 'gvSIGi18n_ExportStatus_UseCaseAssessmentFailed'
cExportStatus_NoAvailableLanguagesToExport  = 'gvSIGi18n_ExportStatus_NoAvailableLanguagesToExport'
cExportStatus_NoAvailableModulesToExport    = 'gvSIGi18n_ExportStatus_NoAvailableModulesToExport'
cExportStatus_CanNotCreateZipFile           = 'gvSIGi18n_ExportStatus_CanNotCreateZipFile'



cUnicodeEscapeEncoding            = 'raw_unicode_escape'
cUnicodeEscapeEncodingFor255Chars = 'ISO-8859-1'


cModuloNoEspecificado_ValorNombre = 'mod-ModuloNoEspecificado'
cModuloNoEspecificado_msgid = 'gvSIGi18n_ModuloNoEspecificado_msgid'
cModuloNoEspecificado_ForArchiveFileName ='unspecified'

cExportFormatOption_JavaProperties = 'Java .properties'
cExportFormatOption_GNUgettextPO   = 'GNU gettext PO'


cZipFilePostfix  = '.zip'
cJarFilePostfix  = '.jar'
cOutputFilePostfixes = [ cZipFilePostfix, cJarFilePostfix, ]

cOutputFileNameLanguageSeparator = '-'

cOutputFileNameModuleSeparator = '-'

cMaxLenIdiomasOutputFileName = 40
cMaxLenModulosOutputFileName = 68

cExportZipFileNamePrefix = 'Export'



# ##############################################
# Java Properties file format constants


cPropertiesMaxLinesToScanTryingToGetCadena = 100


cFilenamePropertiesBase = 'text'
cPropertiesFilePostfix  = '.properties'

cDefaultLanguagePropertiesFileName = cFilenamePropertiesBase + cPropertiesFilePostfix

cPropertiesFileCharBeforeLanguage = '_'
cPropertiesFileCharBeforeCountry = '_'




cPrefixLineaLenguaje="#Translations for language ["
cPrefixLineaTimestamp = '#'
cIgnorePropertiesLinePrefix = '#'
cPropertyNameValueSeparator = '='


cManifestFolderName         = 'META-INF'
cManifestFileName           = 'MANIFEST.MF'
cZipPathSeparator  = '/'
cManifestFileFullName       = cManifestFolderName +  cZipPathSeparator + cManifestFileName


cManifestEntryStartLinePrefix                   = 'Name:'
cManifestLocaleLanguageStartLinePrefix          = 'locale-language:'
cManifestLocaleCountryStartLinePrefix           = 'locale-country:'
cManifestReferenceLocaleLanguageStartLinePrefix = 'reference-locale-language:'
cManifestReferenceLocaleCountryStartLinePrefix  = 'reference-locale-country:'



cLocalesCSVFileName           = 'locales.csv'
cLocalesCSVFileFullName       = cLocalesCSVFileName

cLocalesCSVIsReferenceFile    = 'true'


cDefaultExportEncodingName_JavaProperties       = 'ISO-8859-1'


cPropertiesUnknownFileName = 'unknown_filename.properties'


# ##############################################
# GNU gettext PO file format constants


cPOMaxLinesToScanTryingToGetCadena = 100
cPOMaxLinesToScanTryingToGetHeader = 100


cPOFilePostfix   = '.po'
cPOTFilePostfix  = '.pot'

cPOFileCharBeforeLanguage = '-'

cNoSeparateModulesFileNamePrefix = 'text'

cPOHeaderPrefix                 = '"'
cPOHeaderPrefix_ContentType     = '"Content-Type:'
cPOHeaderPrefix_Charset         = 'charset='
cPOHeaderPrefix_LanguageCode    = '"Language-Code:'
cPOHeaderPrefix_LanguageName    = '"Language-Name:'
cPOHeaderPrefix_Domain          = '"Domain:'
cPOHeaderPrefix_IsFallbackFor   = '"X-Is-Fallback-For:'

cTranslationEntryCommentPrefix  = "# "

cTranslationEntryDefaultPrefix  = "#. Default:"
cTranslationEntrySourcesPrefix  = "#:"
cTranslationEntryFlagsPrefix    = "#,"

cPOTranslationEntryMsgidPrefix    = "msgid"
cPOTranslationEntryMsgstrPrefix   = "msgstr"

cDefaultExportEncodingName_GNUgettextPO   = 'UTF-8'

cPOUnknownFileName = 'unknown_filename.po'


cGNUgettextPOHeaderTemplateString_Top = """# GNU gettext PO File generated by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana, Model Driven Development sl y Antonio Carrasco para el producto gvSIGi18n. http://gvsig.org and http://www.ModelDD.org
msgid ""
msgstr ""
"""
cGNUgettextPOHeaderLabel_ProjectIdVersion           = """"Project-Id-Version: """
cGNUgettextPOHeaderLabel_POTCreationDate            = """"POT-Creation-Date: """
cGNUgettextPOHeaderLabel_PORevisionDate             = """"PO-Revision-Date: """
cGNUgettextPOHeaderLabel_LastTranslator             = """"Last-Translator: """
cGNUgettextPOHeaderLabel_LanguageTeam               = """"Language-Team: """
cGNUgettextPOHeaderLabel_MIMEVersion                = """"MIME-Version: 1.0"""
cGNUgettextPOHeaderLabel_ContentType                = """"Content-Type: text/plain; charset="""
cGNUgettextPOHeaderLabel_ContentTransferEncoding    = """"Content-Transfer-Encoding: """
cGNUgettextPOHeaderLabel_PluralForms                = """"Plural-Forms: """
cGNUgettextPOHeaderLabel_LanguageCode               = """"Language-Code: """
cGNUgettextPOHeaderLabel_LanguageName               = """"Language-Name: """
cGNUgettextPOHeaderLabel_PreferredEncodings         = """"Preferred-Encodings: """
cGNUgettextPOHeaderLabel_Domain                     = """"Domain: """

cGNUgettextPOHeader_AfterValue                      = '\\n"\n'



cGNUgettextPOHeaderTemplateString = u"""# GNU gettext PO File generated by gvSIGi18n product by http://gvsig.org and http://www.ModelDD.org 
msgid ""
msgstr ""
"Project-Id-Version: %(Project-Id-Version)s\\n"
"POT-Creation-Date: %(POT-Creation-Date)s\\n"
"PO-Revision-Date: %(PO-Revision-Date)s\\n"
"Last-Translator: %(Last-Translator)s\\n"
"Language-Team: %(Language-Team)s\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=%(charset)s\\n"
"Content-Transfer-Encoding: %(Content-Transfer-Encoding)s\\n"
"Plural-Forms: %(Plural-Forms)s\\n"
"Language-Code: %(Language-Code)s\\n"
"Language-Name: %(Language-Name)s\\n"
"Preferred-Encodings: %(Preferred-Encodings)s\\n"
"Domain: %(Domain)s\\n"
"""

cGNUgettextPOFallbackTemplateString= u"""
"X-Is-Fallback-For: %(X-Is-Fallback-For)s\\n"
"""


cGNUgettextPOEntryLabel_Default            = '#. Default: "'
cGNUgettextPOEntryLabel_AfterDefault       = '"\n'
cGNUgettextPOEntryLabel_SourceFileNames    = '#: '
cGNUgettextPOEntryLabel_AfterSourceFileNames= '\n'
cGNUgettextPOEntryLabel_msgid              = 'msgid "'
cGNUgettextPOEntryLabel_AfterMsgid         = '"\n'
cGNUgettextPOEntryLabel_msgstr             = 'msgstr "'
cGNUgettextPOEntryLabel_AfterMsgstr        = '"\n'

cGNUgettextPOEntryTemplateString_Default            = """#. Default: "%(Default)s"\n"""
cGNUgettextPOEntryTemplateString_SourceFileNames    = """#: %(SourceFileNames)s\n"""
cGNUgettextPOEntryTemplateString_msgid              = """msgid "%(msgid)s"\n"""
cGNUgettextPOEntryTemplateString_msgstr             = """msgstr "%(msgstr)s"\n"""

cGNUgettextPOEntryLabel_AfterValue  = '"\n"'


cGNUgettextPOEntryTemplateString = cGNUgettextPOEntryTemplateString_Default + cGNUgettextPOEntryTemplateString_SourceFileNames + cGNUgettextPOEntryTemplateString_msgid + cGNUgettextPOEntryTemplateString_msgstr


cGNUgettextPOHeaderDefaultValuesDict = {
    'Project-Id-Version':           '',
    'POT-Creation-Date':            '',
    'PO-Revision-Date':             '',
    'Last-Translator':              '',
    'Language-Team':                '',
    'charset':                      'UTF-8',
    'Content-Transfer-Encoding':    '8bit',
    'Plural-Forms':                 'nplurals=1; plural=0',
    'Language-Code':                '',
    'Language-Name':                '',
    'Preferred-Encodings':          '',
    'Domain':                       '',
    'X-Is-Fallback-For':            '',
}
        








cGNUgettextPOformatDocumentation = """
3 The Format of PO Files

The GNU gettext toolset helps programmers and translators at producing, updating and using translation files, mainly those PO files which are textual, editable files. This chapter explains the format of PO files.

A PO file is made up of many entries, each entry holding the relation between an original untranslated string and its corresponding translation. All entries in a given PO file usually pertain to a single project, and all translations are expressed in a single target language. One PO file entry has the following schematic structure:

     white-space
     #  translator-comments
     #. extracted-comments
     #: reference...
     #, flag...
     #| msgid previous-untranslated-string
     msgid untranslated-string
     msgstr translated-string

The general structure of a PO file should be well understood by the translator. When using PO mode, very little has to be known about the format details, as PO mode takes care of them for her.

A simple entry can look like this:

     #: lib/error.c:116
     msgid "Unknown system error"
     msgstr "Error desconegut del sistema"

Entries begin with some optional white space. Usually, when generated through GNU gettext tools, there is exactly one blank line between entries. 
Then comments follow, on lines all starting with the character #. 
There are two kinds of comments: those which have some white space immediately following the # - the translator comments -, 
which comments are created and maintained exclusively by the translator, 
and those which have some non-white character just after the # - the automatic comments -, 
which comments are created and maintained automatically by GNU gettext tools. 
Comment lines starting with #. contain comments given by the programmer, directed at the translator; 
these comments are called extracted comments because the xgettext program extracts them from the program's source code. 
Comment lines starting with #: contain references to the program's source code. 
Comment lines starting with #, contain flags; more about these below. 
Comment lines starting with #| contain the previous untranslated string for which the translator gave a translation.

All comments, of either kind, are optional.

After white space and comments, entries show two strings, namely first the untranslated string as it appears in the original program sources, and then, the translation of this string. The original string is introduced by the keyword msgid, and the translation, by msgstr. The two strings, untranslated and translated, are quoted in various ways in the PO file, using " delimiters and \ escapes, but the translator does not really have to pay attention to the precise quoting format, as PO mode fully takes care of quoting for her.

The msgid strings, as well as automatic comments, are produced and managed by other GNU gettext tools, and PO mode does not provide means for the translator to alter these. The most she can do is merely deleting them, and only by deleting the whole entry. On the other hand, the msgstr string, as well as translator comments, are really meant for the translator, and PO mode gives her the full control she needs.

The comment lines beginning with #, are special because they are not completely ignored by the programs as comments generally are. The comma separated list of flags is used by the msgfmt program to give the user some better diagnostic messages. Currently there are two forms of flags defined: 
"""

cWesternLanguageMarkInSourceMap =  'en'

cEncodingSeparatorSentinelName  = '--encoding_separator--'

cUTFEncodingsForAllLanguages = [ 
    [ cEncodingUnicodeEscape, cEncodingUnicodeEscape, []], 
    [ cEncodingUTF8, cEncodingUTF8, []], 
    [ u'utf_7', u'U7,unicode-1-1-utf-7', []], 
     [ u'utf_8_sig', u'utf_8_sig', []], 
    [ cEncodingUTF16, cEncodingUTF16, []],
    [ u'utf_16_be', u'UTF-16BE', [ u'(BMP only)']], 
    [ u'utf_16_le', u'UTF-16LE', [ u'(BMP only)']], 
    [ u'utf_32_be', u'UTF-32BE', [ u'(BMP only)']], 
    [ u'utf_32_le', u'UTF-32LE', [ u'(BMP only)']], 
]


cDefaultEncodingsSourceMap = [
    [ u'ascii', u'646,us-ascii', u'English', u'',],
    [ u'big5', u'big5-tw,csbig5', u'Traditional Chinese', u'zh',],
    [ u'big5hkscs', u'big5-hkscs,hkscs', u'Traditional Chinese', u'zh',],
    [ u'cp037', u'IBM037,IBM039', u'English', u'',],
    [ u'cp424', u'EBCDIC-CP-HE,IBM424', u'Hebrew', u'he',],
    [ u'cp437', u'437,IBM437', u'English', u'',],
    [ u'cp500', u'EBCDIC-CP-BE,EBCDIC-CP-CH,IBM500', u'Western Europe', u'',],
    [ u'cp737', u'', u'Greek', u'el',],
    [ u'cp775', u'IBM775', u'Baltic languages', u'lv,lt',],
    [ u'cp850', u'850,IBM850', u'Western Europe', u'',],
    [ u'cp852', u'852,IBM852', u'Central and Eastern Europe', u'',],
    [ u'cp855', u'855,IBM855', u'Bulgarian,Byelorussian,Macedonian,Russian,Serbian', u'bg,be,mk,ru,sr',],
    [ u'cp856', u'cp856', u'Hebrew', u'he',],
    [ u'cp857', u'857,IBM857', u'Turkish', u'tr',],
    [ u'cp860', u'860,IBM860', u'Portuguese', u'pt',],
    [ u'cp861', u'861,CP-IS,IBM861', u'Icelandic', u'is',],
    [ u'cp862', u'862,IBM862', u'Hebrew', u'he',],
    [ u'cp863', u'863,IBM863', u'Canadian', u'en-ca',],
    [ u'cp864', u'IBM864', u'Arabic', u'ar',],
    [ u'cp865', u'865,IBM865', u'Danish,Norwegian', u'da,no,nn',],
    [ u'cp866', u'866,IBM866', u'Russian', u'ru',],
    [ u'cp869', u'869,CP-GR,IBM869', u'Greek', u'el',],
    [ u'cp874', u'cp874', u'Thai', u'th',],
    [ u'cp875', u'cp875', u'Greek', u'el',],
    [ u'cp932', u'932,ms932,mskanji,ms-kanji', u'Japanese', u'ja',],
    [ u'cp949', u'949,ms949,uhc', u'Korean', u'ko',],
    [ u'cp950', u'950,ms950', u'Traditional Chinese', u'zh',],
    [ u'cp1006', u'cp1006', u'Urdu', u'ur',],
    [ u'cp1026', u'ibm1026', u'Turkish', u'',],
    [ u'cp1140', u'ibm1140', u'Western Europe', u'',],
    [ u'cp1250', u'windows-1250', u'Central and Eastern Europe', u'',],
    [ u'cp1251', u'windows-1251', u'Bulgarian,Byelorussian,Macedonian,Russian,Serbian', u'bg,be,mk,ru,sr',],
    [ u'cp1252', u'windows-1252', u'Western Europe', u'',],
    [ u'cp1253', u'windows-1253', u'Greek', u'el',],
    [ u'cp1254', u'windows-1254', u'Turkish', u'tr',],
    [ u'cp1255', u'windows-1255', u'Hebrew', u'he',],
    [ u'cp1256', 'windows1256',   'Arabic', u'ar',],
    [ u'cp1257', u'windows-1257', u'Baltic languages', u'lv,lt',],
    [ u'cp1258', u'windows-1258', u'Vietnamese', u'vi',],
    [ u'euc_jp', u'eucjp,ujis,u-jis', u'Japanese', u'ja',],
    [ u'euc_jis_2004', u'jisx0213,eucjis2004', u'Japanese', u'ja',],
    [ u'euc_jisx0213', u'eucjisx0213', u'Japanese', u'ja',],
    [ u'euc_kr', u'euckr,korean,ksc5601,ks_c-5601,ks_c-5601-1987,ksx1001,ks_x-1001', u'Korean', u'ko',],
    [ u'gb2312', u'chinese,csiso58gb231280,euc-cn,euccn,eucgb2312-cn,gb2312-1980,gb2312-80,iso-ir-58', u'Simplified Chinese', u'zh',],
    [ u'gbk', u'936,cp936,ms936', u'Unified Chinese', u'zh',],
    [ u'gb18030', u'gb18030-2000', u'Unified Chinese', u'zh',],
    [ u'hz', u'hzgb,hz-gb,hz-gb-2312', u'Simplified Chinese', u'zh',],
    [ u'iso2022_jp', u'csiso2022jp,iso2022jp,iso-2022-jp', u'Japanese', u'ja',],
    [ u'iso2022_jp_1', u'iso2022jp-1,iso-2022-jp-1', u'Japanese', u'ja',],
    [ u'iso2022_jp_2', u'iso2022jp-2,iso-2022-jp-2', u'Japanese,Korean,Simplified Chinese,Western Europe,Greek', u'ja,ko,zh,el,en',],
    [ u'iso2022_jp_2004', u'iso2022jp-2004,iso-2022-jp-2004', u'Japanese', u'ja',],
    [ u'iso2022_jp_3', u'iso2022jp-3,iso-2022-jp-3', u'Japanese', u'ja',],
    [ u'iso2022_jp_ext', u'iso2022jp-ext,iso-2022-jp-ext', u'Japanese', u'ja',],
    [ u'iso2022_kr', u'csiso2022kr,iso2022kr,iso-2022-kr', u'Korean', u'ko',],
    [ u'latin_1', u'iso-8859-1,iso8859-1,8859,cp819,latin,latin1,L1', u'West Europe', u'',],
    [ u'iso8859_2', u'iso-8859-2,latin2,L2', u'Central and Eastern Europe', u'',],
    [ u'iso8859_3', u'iso-8859-3,latin3,L3', u'Esperanto,Maltese', u'eo,mt',],
    [ u'iso8859_4', u'iso-8859-4,latin4,L4', u'Baltic languages', u'lv,lt',],
    [ u'iso8859_5', u'iso-8859-5,cyrillic', u'Bulgarian,Byelorussian,Macedonian,Russian,Serbian', u'bg,be,mk,ru,sr',],
    [ u'iso8859_6', u'iso-8859-6,arabic', u'Arabic', u'ar',],
    [ u'iso8859_7', u'iso-8859-7,greek,greek8', u'Greek', u'el',],
    [ u'iso8859_8', u'iso-8859-8,hebrew', u'Hebrew', u'he',],
    [ u'iso8859_9', u'iso-8859-9,latin5,L5', u'Turkish', u'th',],
    [ u'iso8859_10', u'iso-8859-10,latin6,L6', u'Nordic languages', u'da,sv,no,nn,is,sv',],
    [ u'iso8859_13', u'iso-8859-13', u'Baltic languages', u'lv,lt',],
    [ u'iso8859_14', u'iso-8859-14,latin8,L8', u'Celtic languages', u'ga,gd,cy,br ',],
    [ u'iso8859_15', u'iso-8859-15', u'Western Europe', u'',],
    [ u'johab', u'cp1361,ms1361', u'Korean', u'ko',],
    [ u'koi8_r', u'koi8_r', u'Russian', u'ru',],
    [ u'koi8_u', u'koi8_u', u'Ukrainian', u'uk',],
    [ u'mac_cyrillic', u'maccyrillic', u'Bulgarian,Byelorussian,Macedonian,Russian,Serbian', u'bg,be,mk,ru,sr',],
    [ u'mac_greek', u'macgreek', u'Greek', u'el',],
    [ u'mac_iceland', u'maciceland', u'Icelandic', u'is',],
    [ u'mac_latin2', u'maclatin2,maccentraleurope', u'Central and Eastern Europe', u'',],
    [ u'mac_roman', u'macroman', u'Western Europe', u'',],
    [ u'mac_turkish', u'macturkish', u'Turkish', u'tr',],
    [ u'ptcp154', u'csptcp154,pt154,cp154,cyrillic-asian', u'Kazakh', u'kk',],
    [ u'shift_jis', u'csshiftjis,shiftjis,sjis,s_jis', u'Japanese', u'ja',],
    [ u'shift_jis_2004', u'shiftjis2004,sjis_2004,sjis2004', u'Japanese', u'ja',],
    [ u'shift_jisx0213', u'shiftjisx0213,sjisx0213,s_jisx0213', u'Japanese', u'ja',],
 ]

cDefaultEncodingsForLanguages = {
    
    
    
    
}

