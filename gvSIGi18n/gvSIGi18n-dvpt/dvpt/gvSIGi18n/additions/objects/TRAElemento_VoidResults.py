# -*- coding: utf-8 -*-
#
# File: TRAElemento_VoidResults.py
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




from AccessControl              import ClassSecurityInfo

from Products.CMFCore           import permissions




from TRAElemento_Constants      import *

   
    
            
# ########################################################################################################
    
class TRAElemento_VoidResults:
    """Class with responsibility to instantiate new void result structures for various common actions and processes.
        
    """
    
    security = ClassSecurityInfo()

    
          
    
    security.declarePublic( 'fNewVoidExtraLink')    
    def fNewVoidExtraLink( self):
        unExtraLink = {
            'label'   : '',
            'href'    : '',
            'icon'    : '',
            'domain'  : '',
            'msgid'   : '',
        }
        return unExtraLink
        

    
      
    security.declarePublic( 'fNewVoidLanguagesDetails')    
    def fNewVoidLanguagesDetails( self,):
        aLanguagesDetails = dict( [ [ aKey, '',] for aKey in cAcceptedLanguageDetailKeys])
        return aLanguagesDetails
    
    
    
      
    security.declarePublic( 'fNewVoidUploadedContent')    
    def fNewVoidUploadedContent( self,):
        unUploadedContent = {
            'import_report':                          None,
            'uploaded_entries':                       [],
            # ############################################
            # languages is the list of language names to create 
            'languages':                              [],
            # ############################################
            # module is the module to which the included strings are associated.
            'module':                                 '',
            # ############################################
            # languages is a dict with language codes as keys, 
            # and values are a dict holding details about the language to create, including
            'languages_details':                      self.fNewVoidLanguagesDetails(),
            # ############################################
            # strings_and_translations is a dict
            #   where keys are string symbols, 
            #   and   values are dicts with languages a keys, and the values are the translations of the symbols for the key language.
            'strings_and_translations':               {},
            # ############################################
            # strings_with_encoding_errors is a dict
            #   where keys are string symbols, 
            #   and   values are lists of the languages for which there was encountered an encoding error while reading the translations interchange file.            
            'strings_with_encoding_errors':           {}, 
            'strings_sources':                        {},
        }
        return unUploadedContent
    
    
     
    
    security.declarePublic( 'fNewVoidExecutionProfilingConfig')    
    def fNewVoidExecutionProfilingConfig():
        aConfig = {
            'execution_profiling_enabled':           cTRAExecutionProfilingEnabled,
            'execution_logging_enabled':             cTRAExecutionLoggingEnabled,
            'execution_logging_detailed_enabled':    cTRAExecutionLoggingDetailedEnabled,
            'execution_rendering_enabled':           cTRAExecutionRenderingEnabled
        }
        return aConfig
        
    
    
    
    security.declarePublic( 'fNewVoidContenidoIntercambioReport')    
    def fNewVoidContenidoIntercambioReport( self):
        """Used by both TRAImportacion and TRAContenidoIntercambio to report a summary of translation interchange contents.
        
        """
        
        return {
            'num_strings':                      0,
            'languages':                        [],
            'modules':                          [],
            'language_names_and_flags':         {},
            'num_translated_by_language':       {},
            'num_pending_by_language':          {},
            'percent_pending_by_language':      {},
            'percent_translated_by_language':   {},
            'num_encoding_errors_by_language':  {},            
            'percent_encoding_errors_by_language':       {},
        }

    
        

    security.declarePublic( 'fNewVoidChangeTranslationResult')
    def fNewVoidChangeTranslationResult( self,):
        aResult = {
            'success':                          False,
            'exception':                        '',
            'status':                           '',
            'condition':                         '',
            'found':                            False,
            'changed':                          False,
            'changed_comment':                  False,
            'simboloCadena':                    '',
            'idCadena':                         '',
            'memberid':                         '',
            'cadenaTraducida_previousValue':    '',
            'cadenaTraducida_newValue':         '',
            'estadoTraduccion_previousValue':   '',
            'estadoTraduccion_newValue':        '',
            'comentario_previousValue':         '',
            'comentario_newValue':              '',
        }
        return aResult
    

     
    security.declarePublic( 'fNewVoidTranslationActivity')
    def fNewVoidTranslationActivity( self,):
        unTranslationActivity = { 
            cRecentActivity_Date:        None,
            cRecentActivity_Language:    None,
            cRecentActivity_User:        None,
            cRecentActivity_Commented:   None,
            cRecentActivity_Action:      None,
            cRecentActivity_Symbol:      None,
            cRecentActivity_Counter:     None,
        }
        return unTranslationActivity
     