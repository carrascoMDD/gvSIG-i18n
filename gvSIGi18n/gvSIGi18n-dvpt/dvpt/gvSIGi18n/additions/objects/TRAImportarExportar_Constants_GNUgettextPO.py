# -*- coding: utf-8 -*-
#
# File: TRAImportarExportar_Constants_GNUgettextPO.py
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





# ##############################################
"""GNU gettext PO file format constants

"""

cExportFormatOption_GNUgettextPO   = 'GNU gettext PO'


cPOMaxLinesToScanTryingToGetCadena = 100
cPOMaxLinesToScanTryingToGetHeader = 100


cPOFilePostfix   = '.po'
cPOTFilePostfix  = '.pot'

cPOFileCharBeforeLanguage = '-'

cPONoSeparateModulesFileNamePrefix = 'text'

cPOHeaderPrefix                 = '"'
cPOHeaderPrefix_ContentType     = '"Content-Type:'
cPOHeaderPrefix_Charset         = 'charset='
cPOHeaderPrefix_LanguageCode    = '"Language-Code:'
cPOHeaderPrefix_LanguageName    = '"Language-Name:'
cPOHeaderPrefix_Domain          = '"Domain:'
cPOHeaderPrefix_IsFallbackFor   = '"X-Is-Fallback-For:'

cPOTranslationEntryCommentPrefix  = "#"

cPOTranslationEntryDefaultPrefix  = "#. Default:"
cPOTranslationEntryModulesPrefix  = "#: --modules--"
cPOTranslationEntryStatusPrefix   = "#: --status--"
cPOTranslationEntrySourcesPrefix  = "#:"
cPOTranslationEntryFlagsPrefix    = "#,"

cPOTranslationEntryCreationDatePrefix            = '#: --creation-date--'
cPOTranslationEntryCreatorPrefix                 = '#: --creator--'
cPOTranslationEntryTranslationDatePrefix         = '#: --translation-date--'
cPOTranslationEntryTranslatorPrefix              = '#: --translator--'
cPOTranslationEntryReviewDatePrefix              = '#: --review-date--'
cPOTranslationEntryReviewerPrefix                = '#: --reviewer--'
cPOTranslationEntryDefinitiveDatePrefix          = '#: --definitive-date--'
cPOTranslationEntryCoordinatorPrefix             = '#: --coordinator--'


cPOTranslationEntryMsgidPrefix    = "msgid"
cPOTranslationEntryMsgstrPrefix   = "msgstr"
cPOTranslationEntryMsgstrContinuationPrefix   = '"'


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
cGNUgettextPOEntryLabel_Status             = '#: --status-- '
cGNUgettextPOEntryLabel_AfterStatus        = '\n'
cGNUgettextPOEntryLabel_SourceFileNames    = '#: '
cGNUgettextPOEntryLabel_AfterSourceFileNames='\n'
cGNUgettextPOEntryLabel_Modules            = '#: --modules-- '
cGNUgettextPOEntryLabel_AfterModules       = '\n'
cGNUgettextPOEntryLabel_msgid              = 'msgid "'
cGNUgettextPOEntryLabel_AfterMsgid         = '"\n'
cGNUgettextPOEntryLabel_msgstr             = 'msgstr "'
cGNUgettextPOEntryLabel_AfterMsgstr        = '"\n'

cGNUgettextPOEntryLabel_CreationDate            = '#: --creation-date-- '
cGNUgettextPOEntryLabel_AfterCreationDate       = '\n'
cGNUgettextPOEntryLabel_Creator                 = '#: --creator-- '
cGNUgettextPOEntryLabel_AfterCreator            = '\n'
cGNUgettextPOEntryLabel_TranslationDate         = '#: --translation-date-- '
cGNUgettextPOEntryLabel_AfterTranslationDate    = '\n'
cGNUgettextPOEntryLabel_Translator              = '#: --translator-- '
cGNUgettextPOEntryLabel_AfterTranslator         = '\n'
cGNUgettextPOEntryLabel_ReviewDate              = '#: --review-date-- '
cGNUgettextPOEntryLabel_AfterReviewDate         = '\n'
cGNUgettextPOEntryLabel_Reviewer                = '#: --reviewer-- '
cGNUgettextPOEntryLabel_AfterReviewer           = '\n'
cGNUgettextPOEntryLabel_DefinitiveDate          = '#: --definitive-date-- '
cGNUgettextPOEntryLabel_AfterDefinitiveDate     = '\n'
cGNUgettextPOEntryLabel_Coordinator             = '#: --coordinator-- '
cGNUgettextPOEntryLabel_AfterCoordinator        = '\n'



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





