# -*- coding: utf-8 -*-
#
# File: TRAElemento_VoidResults.py
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




from AccessControl              import ClassSecurityInfo

from Products.CMFCore           import permissions




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

from TRAImportarExportar_Constants import cScannedKeys_String_Symbol, cScannedKeys_String_Translations, cScannedKeys_Translation_Translation
   
    
            
# ########################################################################################################
    
class TRAElemento_VoidResults:
    """Class with responsibility to instantiate new void result structures for various common actions and processes.
        
    """
    
    security = ClassSecurityInfo()

    
    
    security.declarePublic( 'fNewVoidExportParametersCandidateValues')    
    def fNewVoidExportParametersCandidateValues(self,):
        someCandidateValues = {
            'theLanguagesToExport':                   [],
            'theExportFormat':                        '',
            'theExportFormat_vocabulary':             [],
            'theExportFormat_vocabulary_msgids':      [],
            'theIncludeManifest':                     '',
            'theIncludeManifest_vocabulary':          [],
            'theIncludeManifest_vocabulary_msgids':   [],
            'theIncludeLocalesCSV':                   '',
            'theIncludeLocalesCSV_vocabulary':        [],
            'theIncludeLocalesCSV_vocabulary_msgids': [],
            'theSeparatedModules':                    '',
            'theSeparatedModules_vocabulary':         [],
            'theSeparatedModules_vocabulary_msgids':  [],
            'theExportModuleNames':                   '',
            'theExportModuleNames_vocabulary':        [],
            'theExportModuleNames_vocabulary_msgids': [],
            'theExportContributions':                   '',
            'theExportContributions_vocabulary':        [],
            'theExportContributions_vocabulary_msgids': [],
            'theExportStringSources':                 '',
            'theExportStringSources_vocabulary':      [],
            'theExportStringSources_vocabulary_msgids': [],
            'theExportTranslationsStatus':            '',
            'theExportTranslationsStatus_vocabulary': [],
            'theExportTranslationsStatus_vocabulary_msgids': [],
            'theTipoArchivo':                         '',
            'theTipoArchivo_vocabulary':              [],
            'theTipoArchivo_vocabulary_msgids':       [],
            'theDefaultLanguageCode':                 '',
            'theDefaultModuleName':                   '',
            'theEncodingErrorHandleMode':             '',
            'theEncodingErrorHandleMode_vocabulary':  [],
            'theEncodingErrorHandleMode_vocabulary_msgids': [],
            'encodings_by_language_code':   { },
            'informe_idiomas_y_modulos':    { },
            'theFilenameForGvSIG':          '',
            'theFilenameForGvSIG_vocabulary':         [],
            'theFilenameForGvSIG_vocabulary_msgids':  [],
            'theProductName':               '',
            'theProductVersion':            '',
            'theL10NVersions':              { },
            
            'theExportarTRACatalogo':                   '',
            'theExportarTRACatalogo_vocabulary':        [],
            'theExportarTRACatalogo_vocabulary_msgids': [],

            'theExportarTRAConfiguraciones':                   '',
            'theExportarTRAConfiguraciones_vocabulary':        [],
            'theExportarTRAConfiguraciones_vocabulary_msgids': [],

            'theExportarTRAParametrosControlProgreso':                   '',
            'theExportarTRAParametrosControlProgreso_vocabulary':        [],
            'theExportarTRAParametrosControlProgreso_vocabulary_msgids': [],

            'theExportarTRAIdiomas':                   '',
            'theExportarTRAIdiomas_vocabulary':        [],
            'theExportarTRAIdiomas_vocabulary_msgids': [],

            'theExportarTRAModulos':                   '',
            'theExportarTRAModulos_vocabulary':        [],
            'theExportarTRAModulos_vocabulary_msgids': [],

            'theExportarTRAInformes':                   '',
            'theExportarTRAInformes_vocabulary':        [],
            'theExportarTRAInformes_vocabulary_msgids': [],

            'theExportarTRASolicitudesCadenas':                   '',
            'theExportarTRASolicitudesCadenas_vocabulary':        [],
            'theExportarTRASolicitudesCadenas_vocabulary_msgids': [],
            
        }
        return someCandidateValues




    security.declarePublic( 'fNewVoidChangeAndBrowseTraslationsRequest')    
    def fNewVoidChangeAndBrowseTraslationsRequest(self,):
        unaRequest = {
            'change_parameters':        self.fNewVoidChangeTraslationsRequest(),
            'browse_parameters':        self.fNewVoidBrowseTraslationsRequest(),
        }
        return unaRequest
        
              
    




    security.declarePublic( 'fNewVoidChangeTraslationsRequest')    
    def fNewVoidChangeTraslationsRequest(self,):
        unaRequest = {
            'change_counter':               0,
            'requested_change_kind':        '',
            'simbolo_cadena_a_traducir':    '',
            'codigo_idioma_a_traducir':     '',
            'cadena_traducida':             '',
            'comentario':                   '',
            'batch_ids_traducida':          [],
            'batch_ids_revisada':           [],
            'batch_ids_definitiva':         [],  
            'nombres_modulos_solicitados':  '',
        }
        return unaRequest
    



    
    

    security.declarePublic( 'fNewVoidBrowseTraslationsRequest')    
    def fNewVoidBrowseTraslationsRequest(self,):
        unaRequest = {
            'search_parameters':            {}, # self.fNewVoidSearchParametersRequest(),
            'include_summary':              False,
        }
        return unaRequest
    



    
    

    security.declarePublic( 'fNewVoidSearchParametersRequest')    
    def fNewVoidSearchParametersRequest(self,):
        unosSearchParameters = {
            'idioma':                       '', 
            
            'simboloCadenaCursor':          '', 

            'traduccionesPorPagina' :       0, 
            'modoDesplazamiento':           '', 
            'desplazarUnRegistroOPagina':   '',

            'idiomasReferencia':            [],         
            'estadosAIncluir':              [], 

            'symbolIndex':                  0,
            'pageIndex':                    0,
            'symbolStartingWith':           '',
            
            'idCadena':                     '', 

            'simbolo':                      '',
            'cadenaTraducida':              '',
            'nombresModulos':               '',
            
            'usuarioCreador':               '',
            'fechaCreacionInicial':         '',
            'fechaCreacionFinal':           '',
            
            'usuarioTraductor':             '',
            'fechaTraduccionInicial':       '',
            'fechaTraduccionFinal':         '',
            
            'usuarioRevisor':               '',
            'fechaRevisionInicial':         '',
            'fechaRevisionFinal':           '',
            
            'usuarioCoordinador':           '',
            'fechaDefinitivoInicial':       '',
            'fechaDefinitivoFinal':         '',

            'usuarioModificador':           '',
            'fechaModificacionInicial':     '',
            'fechaModificacionFinal':       '',

            'cadenasInactivas':             '',  
        }
        return unosSearchParameters
    


    
    
    
    security.declarePublic( 'fNewVoidExtraLink')    
    def fNewVoidExtraLink( self,):
        unExtraLink = {
            'label'   : '',
            'href'    : '',
            'icon'    : '',
            'domain'  : '',
            'msgid'   : '',
        }
        return unExtraLink
        

    
    
    
     
    
    security.declarePublic( 'fNewVoidExecutionProfilingConfig')    
    def fNewVoidExecutionProfilingConfig(self,):
        aConfig = {
            'execution_profiling_enabled':           cTRAExecutionProfilingEnabled,
            'execution_logging_enabled':             cTRAExecutionLoggingEnabled,
            'execution_logging_detailed_enabled':    cTRAExecutionLoggingDetailedEnabled,
            'execution_rendering_enabled':           cTRAExecutionRenderingEnabled
        }
        return aConfig
        
    
    
    
    

      
    security.declarePublic( 'fNewVoidLanguagesDetails')    
    def fNewVoidLanguagesDetails( self,):
        aLanguagesDetails = {
            'codigo_internacional_idioma':  '',
            'english_name':                 '',
            'nombre_nativo_de_idioma':      '',
        }
        return aLanguagesDetails
    

    
   
    security.declarePrivate( 'fNewVoidUploadedEntry')    
    def fNewVoidUploadedEntry( self,):
        unUploadedEntry = {
            'in_zip':                                  False,
            'module':                                  '',
            'file_name':                               '',
            'file_kind':                               '',
            'is_reference':                            False,
            'language':                                '',
            'country':                                 '',
            'language_and_country':                    '',
            'charset':                                 '',
            'is_fallback_for':                         '',
            'domain':                                  '',
            'is_pot_file':                             False,
            'exceeded_max_number_of_lines':           False,
        }
        return unUploadedEntry
    
    
    
    

      
    security.declarePublic( 'fNewVoidUploadedContent')    
    def fNewVoidUploadedContent( self,):
        unUploadedContent = {
            # ############################################
            # information about the original files read, if any
            # not available in imports to create languages, or strings, or copy translations between languages
            'uploaded_entries':                       [],
            
            # ############################################
            # scanned data to feed the import process 
            'content_data':                           None,
        }
        return unUploadedContent
    
      
    
                
    security.declarePrivate( 'fNewVoidScannedData')    
    def fNewVoidScannedData( self,):
        """Data structure to hold the all information read from one or more source files, whether a stand-alone file, or a file contained in an archive (i.e. a .zip).
        
        """
        aScannedData = {
            'modules':            [ ],   # list of module names referenced from the 'mod' field of each entry.
            'languages':          [ ],   # a list of language codes for which translations have been read in any entry
            # 'languages_details': { },  # optional: details for languages to create: used when creating a language under user demand, with non-well-known codes: a dict with language codes as key and value  a dict with keys codigo_internacional_idioma, english_name, nombre_nativo_de_idioma
            'symbols':            [ ],   # scanned strings in read order
            'num_symbol_errors':  0,     # number of errors in string symbols, by language
            'symbols_dict':       { },   # scanned strings by string symbol
        }
        return aScannedData
                                       

                
      
 
                
    security.declarePrivate( 'fNewVoidScannedString')    
    def fNewVoidScannedString( self,):
        """Data structure to hold the information read about each string symbol. Contained in the 'symbols' entry of fNewVoidScannedData().
        
        """
        aScannedString = {
            cScannedKeys_String_Symbol:       '',     # required.
            # cScannedKeys_String_Errors:     [ ],    # optional. error kinds occurred in the string (but not in translations): modules, sources (an error symbol prevents creation of a valid scanned string record)
            # cScannedKeys_String_Modules:    set(),  # optional. indexes of module names in the list 
            # cScannedKeys_String_Sources:    [ ],    # optional. sources 
            cScannedKeys_String_Translations: { },    # required. the dictionary of translations for the string symbol, indexed by the language code
        }
        return aScannedString
                
                
      
    
    
    
                    
    security.declarePrivate( 'fNewVoidScannedTranslation')    
    def fNewVoidScannedTranslation( self,):
        """Data structure to hold the information read about the translation of a  string symbol into a language. Contained in the cScannedKeys_String_Translations entry of fNewVoidScannedString().
        
        """
        aScannedTranslation = {
            cScannedKeys_Translation_Translation:   '',     # required. translation into the language
            # cScannedKeys_Translation_Errors:      [ ],    # optional. error kinds occurred in the translation: translation, status, comment, flags
            # cScannedKeys_Translation_Status:      3,      # optional. value 2 for Reviewed status, value 3 for Definitive status
            # cScannedKeys_Translation_Comment:     '',     # optional. comment
            # cScannedKeys_Translation_Flags:       '',     # optional. flags
            
            #cScannedKeys_Translation_CreationDate   
            #cScannedKeys_Translation_Creator        
            #cScannedKeys_Translation_TranslationDate
            #cScannedKeys_Translation_Translator        
            #cScannedKeys_Translation_ReviewDate     
            #cScannedKeys_Translation_Reviewer          
            #cScannedKeys_Translation_DefinitiveDate 
            #cScannedKeys_Translation_Coordinator       

        }
        return aScannedTranslation
                    
    
    
    
    
    
    security.declarePublic( 'fNewVoidCambiosInformacionReport')    
    def fNewVoidCambiosInformacionReport( self):
        """Contains information about the changes made during the execution of the import process.
        
        """
        
        return { }
    
    
    
    
    
    security.declarePublic( 'fNewVoidContenidoIntercambioReport')    
    def fNewVoidContenidoIntercambioReport( self):
        """Used by both TRAImportacion and TRAContenidoIntercambio to report a summary of translation interchange contents.
        
        """
        
        return {
            'title':                            '',
            'description':                      '',
            'absolute_url':                     '',
            'num_strings':                      0,
            'languages':                        [],
            'modules':                          [],
            'language_names_and_flags':         {},
            'num_translated_by_language':       {},
            'num_pending_by_language':          {},
            'percent_pending_by_language':      {},
            'percent_translated_by_language':   {},
            'num_symbol_errors':                0,            
            'num_string_errors':                0,            
            'percent_string_errors':            {},            
            'num_encoding_errors_by_language':  {},            
            'percent_encoding_errors_by_language':       {},
        }

    
    

    
    security.declarePublic( 'fNewVoidContenidoXMLReport')    
    def fNewVoidContenidoXMLReport( self):
        """Used by TRAContenidoXML to report a summary of XML contents.
        
        """
        
        return {
            'title':                            '',
            'description':                      '',
            'absolute_url':                     '',
            'expected_num_nodes':               0,
            'expected_num_nodes_by_type':       { },
            'binary_file_names':                [ ],
        }

    
    
    
        
    
    security.declarePublic( 'fNewVoidCreateProgressHandlerResult')
    def fNewVoidCreateProgressHandlerResult( self,):
        aResult = {
            'success':                          False,
            'condition':                        '',
            'progress_handler_key':             None,
            'progress_handler':                 None,
            'progress_element':                 None,
        }
        return aResult
        
    
    
        

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
     
    
    
    
    
    
    
    

    
                
    # ###########################################################
    """Results obtained periodically during the progress of long-lived processes, and at the end of the processes.
    
    """
    
    security.declarePrivate( 'fNewVoidProgressResult')
    def fNewVoidProgressResult( self, ):
        unResult = {
            'from_progress_handler':    False,
            'process_type':             '',
            'progress_support_kinds':   '',
            'member_id':                '',
            'success':                  False,
            'condition':                '',
            'error_message':            '',            
            'error_details':            '',            
            'error_traceback':          '',
            'exception_report':         '',   
            'exception_traceback':      '',
            'start_date_time':          None,
            'start_date_time_string':   '',
            'date_time_now':            None,
            'date_time_now_string':     '',
            'exception_date_time':      None,
            'exception_date_time_string':'',
            'end_date_time':            None,
            'end_date_time_string':     '',
            'TRACatalogo_title':        '',
            'TRACatalogo_path':         '',
            'TRACatalogo_UID':          '',
            'element_type':             '',
            'element_title':            '',
            'element_path':             '',
            'element_UID':              '',
            'last_element_type':        '',
            'last_element_title':       '',
            'last_element_path':        '',
            'last_element_UID':         '',
            'last_actions':             [],
            'total_elements_traversed': 0,
            'total_elements_changed':   0,
            'elements_by_type_dict':    { },
            'elements_by_type':         [ ],
            'elements_changed_by_type_dict': { },
            'elements_changed_by_type': [ ],
            'progress_parameters':      { },
            'progress_counters':        { },
        }
        return unResult
                
        
    
    
    
 
                
    # ###########################################################
    """Process control parameters and counters for the progress of long-lived processes.
    
    """
 
        
    security.declarePublic( 'fNewVoidProgressControlParms_All')
    def fNewVoidProgressControlParms_All( self,):
        """Parameters controlling capabilities serviced during the progress of long-lived processes.
        
        """  
        
        def fNewVoidProgressControlParms_General( ):
            someProcessControlParms = {
                'enabled':                  False,
                'max_milliseconds':         0,
                'max_elements_traversed':   0,
                'max_elements_changed':     0,            
            }
            
            return someProcessControlParms
        
        
        def fNewVoidProgressControlParms_Logging( ):
            someProcessControlParms = fNewVoidProgressControlParms_General()
            someProcessControlParms.update( {
                'log_every_nth_transactions':        0,
            })
            
            return someProcessControlParms
        
            
        
        def fNewVoidProgressControlParms_StoreResults( ):
            someProcessControlParms = fNewVoidProgressControlParms_General()
            
            return someProcessControlParms
        
        
        
        def fNewVoidProgressControlParms_YieldProcessor():
            someProcessControlParms = fNewVoidProgressControlParms_General()
            someProcessControlParms.update( {
                'only_between_transactions':          False,
                'percent_active_time':                0,
            })
                                    
            
            return someProcessControlParms
        
        
        
        def fNewVoidProgressControlParms_Transactional( ):
            someProcessControlParms = fNewVoidProgressControlParms_General()
            
            return someProcessControlParms
                
        
         
        
        someProcessControlParms = {
            cTRAProgress_Control_RunAfterPrevious:   False,
            cTRAProgress_SupportKind_Logging:        fNewVoidProgressControlParms_Logging(),
            cTRAProgress_SupportKind_StoreResults:   fNewVoidProgressControlParms_StoreResults(),
            cTRAProgress_SupportKind_YieldProcessor: fNewVoidProgressControlParms_YieldProcessor(),
            cTRAProgress_SupportKind_Transactional:  fNewVoidProgressControlParms_Transactional(),
        }
        
        return someProcessControlParms
    

    
    
    

    security.declarePublic( 'fNewVoidProgressControlParms_ToChange')
    def fNewVoidProgressControlParms_ToChange( self,):
        someProcessControlParms = {
            cTRAProgress_SupportKind_Logging:        {},
            cTRAProgress_SupportKind_StoreResults:   {},
            cTRAProgress_SupportKind_YieldProcessor: {},
            cTRAProgress_SupportKind_Transactional:  {},
        }
        
        return someProcessControlParms
    


                  
     
        
        

     
        
    
    security.declarePrivate( 'fNewVoidProgressControlCounters')
    def fNewVoidProgressControlCounters( self,):
        """Counters to control capabilities serviced during the progress of long-lived processes.
        
        """
        def fNewVoidProgressControlCounters_General( ):
            someProcessControlCounters = {
                'milliseconds_when_last':             0,
                'elements_traversed_since_last':      0,
                'elements_changed_since_last':        0,
                'total_actions':                      0,
                'milliseconds_since_last':            0,
            }
            
            return someProcessControlCounters
            
        
        
        
        def fNewVoidProgressControlCounters_Logging():
            someProcessControlCounters = fNewVoidProgressControlCounters_General()
            someProcessControlCounters.update( {
                'transactions_committed_since_last':        0,
            })
            
            return someProcessControlCounters
                  
         
        
        
        def fNewVoidProgressControlCounters_StoreResults( ):
            someProcessControlCounters = fNewVoidProgressControlCounters_General()
            
            return someProcessControlCounters
                  
         
            
        
        def fNewVoidProgressControlCounters_YieldProcessor( ):
            someProcessControlCounters = fNewVoidProgressControlCounters_General()
            someProcessControlCounters.update( {
                'total_activity_time':        0,
                'total_yield_time':           0,
            })
            
            return someProcessControlCounters
                  
         
            
        
        def fNewVoidProgressControlCounters_Transactional( ):
            someProcessControlCounters = fNewVoidProgressControlCounters_General()
            
            return someProcessControlCounters
                          
        
        someProcessControlCounters = {
            cTRAProgress_SupportKind_Logging:        fNewVoidProgressControlCounters_Logging(),
            cTRAProgress_SupportKind_StoreResults:   fNewVoidProgressControlCounters_StoreResults(),
            cTRAProgress_SupportKind_YieldProcessor: fNewVoidProgressControlCounters_YieldProcessor(),
            cTRAProgress_SupportKind_Transactional:  fNewVoidProgressControlCounters_Transactional(),
        }
        
        return someProcessControlCounters
    

    

    



    
    security.declarePrivate( "fNewVoidRegistroHistoria")
    def fNewVoidRegistroHistoria( self,):
        """Void and EMPTY declaration of ields to pack into a translation change history record string. Return an empty dict, to be populated minimally, to save storage space. 
        
        """
        unRegistroHistoria = {
            #cTRAHistory_ActionKind      : None,
            #cTRAHistory_ActionDate      : None,
            #cTRAHistory_User            : None,
            #cTRAHistory_Status          : None,
            #cTRAHistory_Translation     : None,
            #cTRAHistory_Comment         : None,
        }
        return unRegistroHistoria
    
            
    
    
    
    
    
    
    
    
    
    
    
    





    security.declarePrivate( 'fNewVoidInformeModulos')
    def fNewVoidInformeModulos(self):
        """Instantiate Results  for Modules report.

        """

        unNuevoInforme = {
            'success':              False,
            'generated':            False,
            'report_date':          None,
            'estados':              cTodosEstados[:],
            'cabeceras_idiomas':    [],
            'numero_cadenas':       0,
            'informes_modulos':     [],
            'totales_estados':      self.fNewVoidInformeTodosEstados(),
            'total_traducciones':   0,
            'error':                '',
            'exception':            '',
        }
        return  unNuevoInforme



    security.declarePrivate( 'fNewVoidInformeModulo')
    def fNewVoidInformeModulo(self):
        """Instantiate Results  for one module in a Modules report.

        """

        unNuevoInforme = {
            'nombre_modulo':       0,
            'numero_cadenas':      0,
            'total_traducciones':  0,
            'informes_idiomas':    [],
            'totales_estados':      self.fNewVoidInformeTodosEstados(),
        }
        return  unNuevoInforme



    security.declarePrivate( 'fNewVoidCabeceraIdioma')
    def fNewVoidCabeceraIdioma(self):
        """Instantiate language results for language header in Modules report.

        """

        unNuevoInforme = {
            'codigo_idioma_en_gvsig':           '',
            'codigo_internacional_idioma':      '',
            'nombre_idioma':                    '',
            'nombre_nativo_idioma':             '',
            'flag':                             '',
            'url_idioma':                       '',
            'list_contents_permission':         False,
            'numero_cadenas':                   0,
            'totales_estados':                  self.fNewVoidInformeTodosEstados(),       
            'modifiable':                       False,
        }
        return  unNuevoInforme









    

    security.declarePrivate( 'fNewVoidInformeIdiomas')
    def fNewVoidInformeIdiomas(self):
        """Instantiate Results  for Languages report.

        """

        unNuevoInforme = {
            'success':              False,
            'generated':            False,
            'report_date':          '',
            'numero_cadenas':       0,
            'estados':              cTodosEstados[:],
            'informes_idiomas':     [],
            'modules':              [],
            'error':                '',
            'exception':            '',
        }
        return  unNuevoInforme



    security.declarePrivate( 'fNewVoidInformeIdioma')
    def fNewVoidInformeIdioma(self):
        """Instantiate Result for one language in Languages report.

        """

        unNuevoInforme = {
            'nombre_idioma':                    '',
            'nombre_nativo_idioma':             '',
            'codigo_idioma_en_gvsig':           '',
            'codigo_internacional_idioma':      '',
            'flag':                             '',
            'flag_url':                         '',
            'url_idioma':                       '',
            'informes_estados':                 self.fNewVoidInformeTodosEstados(),
            'total_traducciones':               0,  # only used with modules report
            'list_contents_permission':         False,
            'modifiable':                       False,
        }
        return  unNuevoInforme



    security.declarePrivate( 'fNewVoidInformeEstado')
    def fNewVoidInformeEstado(self):
        """Instantiate Result for one translation status.

        """

        unNuevoInforme = {
            'nombre_estado':    '',
            'cantidad':         0,
            'porcentaje':       0,
        }
        return  unNuevoInforme


    security.declarePrivate( 'fNewVoidInformeTodosEstados')
    def fNewVoidInformeTodosEstados(self):
        """Instantiate Result for all translation statuses.

        """

        unNuevoInforme = [ ]
        for unEstado in cTodosEstados:
            unInformeEstado = self.fNewVoidInformeEstado()
            unInformeEstado[ 'nombre_estado'] = unEstado
            unNuevoInforme.append( unInformeEstado)
        return  unNuevoInforme







    security.declarePrivate( 'fNewVoidInformeTitulosIdiomasYModulosPermitidos')
    def fNewVoidInformeTitulosIdiomasYModulosPermitidos(self,):
        """Instantiate Result for Report of titles of allowed languages and modules.

        """
        unInforme = {
            'success':                  False,
            'idiomas':                  [], 
            'modulos':                  [], 
            'numero_cadenas':           0,
            'use_case_query_results':   [],
            'display_country_flags':    False,
        }
        return unInforme



    security.declarePrivate( 'fNewVoidInformeTitulosIdioma')
    def fNewVoidInformeTitulosIdioma(self,):
        unInforme = {
            'codigo_idioma_en_gvsig':           '', 
            'codigo_internacional_de_idioma':   '',
            'nombre':                           '',
            'nombre_nativo':                    '',
            'flag':                             '',
            'codigo_idioma_referencia':         '',
            'juego_caracteres_javaproperties':  '',
            'juego_caracteres_po':              '',
        }
        return unInforme

    
    
    
    
    
    
    

    security.declarePrivate( 'fNewVoidInformeContribuciones')
    def fNewVoidInformeContribuciones(self):
        """Instantiate Results  for Contributions report.

        """

        unNuevoInforme = {
            'success':                    False,
            'report_date':                '',
            'reporting_user':             '',
            'error':                      '',
            'exception':                  '',
            
            'period_keys':                cTRAContribucionesReport_Periods[:],
            'modes_keys':                 cTRAContribucion_Modos[:],

            'periods_dates':              dict( [ [ aPeriodKey, [ '', '',] ] for  aPeriodKey in cTRAContribucionesReport_Periods]),
            'periods_totals':             dict( [ [ aPeriodKey, self.fNewVoidInformeContribucionesYModos(), ] for  aPeriodKey in cTRAContribucionesReport_Periods]),
            
            'sorted_language_codes':      [ ],

            'total_contributions':        0,
            
            'total_contributions_by_mode': dict( [ [ aModeKey, 0 ] for  aModeKey in cTRAContribucion_Modos]),
           
            'contributions_by_language':  { },

            'contributions_by_user':      { },
            
            'alphabetical_user_ids':      [ ],
            
            'rank_user_ids_total':        [ ],
            'rank_user_ids_by_periods':   dict( [ [ aPeriodKey, [ ], ] for  aPeriodKey in cTRAContribucionesReport_Periods]),
            'rank_admin_user_ids_total':  [ ],
            'rank_admin_user_ids_by_periods': dict( [ [ aPeriodKey, [ ], ] for  aPeriodKey in cTRAContribucionesReport_Periods]),
            
            'admin_user_ids':             [ ],
            
            # to do
            'users_member_info':          { },
            
        }
        return  unNuevoInforme



    
    
    security.declarePrivate( 'fNewVoidInformeContribucionesIdioma')
    def fNewVoidInformeContribucionesIdioma(self):
        """Instantiate Results  for Contributions report for a specific Language.

        """

        unNuevoInforme = {
            'nombre_idioma':                    '',
            'nombre_nativo_idioma':             '',
            'codigo_idioma_en_gvsig':           '',
            'codigo_internacional_idioma':      '',
            'url_idioma':                       '',
            'flag':                             '',
            'flag_url':                         '',

            'total_contributions':              0,         
            'total_contributions_by_mode':      dict( [ [ aModeKey, 0 ] for  aModeKey in cTRAContribucion_Modos]),
            
            'periods_totals':                   dict( [ [ aPeriodKey, self.fNewVoidInformeContribucionesYModos(), ] for  aPeriodKey in cTRAContribucionesReport_Periods]),
            'contributions_by_periods':         dict( [ [ aPeriodKey, { }, ] for  aPeriodKey in cTRAContribucionesReport_Periods]),

            'contributions_by_user':            { },
            
            'rank_user_ids_total':              [ ],
            'rank_user_ids_by_periods':         dict( [ [ aPeriodKey, [ ], ] for  aPeriodKey in cTRAContribucionesReport_Periods]),
            'rank_admin_user_ids_total':        [ ],
            'rank_admin_user_ids_by_periods':   dict( [ [ aPeriodKey, [ ], ] for  aPeriodKey in cTRAContribucionesReport_Periods]),
        
        }
        return  unNuevoInforme

    
 
    security.declarePrivate( 'fNewVoidInformeContribucionesYModos')
    def fNewVoidInformeContribucionesYModos(self,):
        """Instantiate Result for the report of Contributions accumulated by contribution mode.

        """
        unNuevoInforme = { 
            'total_contributions':    0,
            'contributions_by_mode':  dict( [ [ aModeKey, 0 ] for  aModeKey in cTRAContribucion_Modos]),
        }  
        return  unNuevoInforme

    
 
    security.declarePrivate( 'fNewVoidInformeContribucionesTotalesUsuario')
    def fNewVoidInformeContribucionesUsuario(self, ):
        """Instantiate Result for the report of Contributions by one User.

        """
        unNuevoInforme = { 
            'total_contributions':        0,
            'contributions_by_mode':      dict( [ [ aModeKey, 0 ] for  aModeKey in cTRAContribucion_Modos]),
            'contributions_by_periods':   dict( [ [ aPeriodKey, self.fNewVoidInformeContribucionesUsuarioEnPeriodo(), ] for  aPeriodKey in cTRAContribucionesReport_Periods]),
            'contributed_language_codes': [ ],
        }  
        return  unNuevoInforme

    
    
    
    security.declarePrivate( 'fNewVoidInformeContribucionesUsuarioEnIdioma')
    def fNewVoidInformeContribucionesUsuarioEnIdioma(self, ):
        """Instantiate Result for the report of Contributions by one User in one language.

        """
        unNuevoInforme = { 
            'total_contributions':        0,
            'contributions_by_mode':      dict( [ [ aModeKey, 0 ] for  aModeKey in cTRAContribucion_Modos]),
            'contributions_by_periods':   dict( [ [ aPeriodKey, self.fNewVoidInformeContribucionesUsuarioEnPeriodo(), ] for  aPeriodKey in cTRAContribucionesReport_Periods]),
        }  
        return  unNuevoInforme
    

    
    
    
    security.declarePrivate( 'fNewVoidInformeContribucionesUsuarioEnPeriodo')
    def fNewVoidInformeContribucionesUsuarioEnPeriodo(self,):
        """Instantiate Result for the report of Contributions by one User.

        """
        unNuevoInforme = { 
            'total_contributions':    0,
            'contributions_by_mode':  dict( [ [ aModeKey, 0 ] for  aModeKey in cTRAContribucion_Modos]),
        }  
        return  unNuevoInforme

    
    


    
    


    security.declarePrivate( 'fNewVoidInformeActividad')
    def fNewVoidInformeActividad(self):
        """Instantiate Result for an Activity report.

        """
        unNuevoInforme = {
            'success':                         False,
            'startup_date':                    None,
            'report_date':                     None,
            'totals':                          self.fNewVoidInformeActividad_TodosPeriodos( 'total'),
            'activity_reports_by_language':    { },
            'period_keys':                     [ ],
            'last_contributions_report_title': '',
            'last_contributions_report_URL':   '',
            'member_infos':                    [ ],            
            'member_infos_by_user_id':         { },            
        }
        return  unNuevoInforme


    
    
    security.declarePrivate( 'fNewVoidInformeActividad_TodosPeriodos')
    def fNewVoidInformeActividad_TodosPeriodos(self, theLanguage=''):
        """Instantiate Result for an Activity report for all periods, used for each language, and for total of all languages.

        """
        unNuevoInforme = { } 
        unNuevoInforme[ 'periods'] = dict( [ [ aPeriodKey, self.fNewVoidInformeActividad_Periodo( aPeriodKey) ] for  aPeriodKey in cActivityReport_Periods])
        unNuevoInforme[ 'language'] = theLanguage
        unNuevoInforme[ 'num_activities'] = 0
            
        return  unNuevoInforme


    
    
    security.declarePrivate( 'fNewVoidInformeActividad_Periodo')
    def fNewVoidInformeActividad_Periodo(self, thePeriod=''):
        """Instantiate Result for an Activity report for a single period, used for each period, for each language, and for total of all languages.

        """
        unNuevoInforme = {
            'period':                    thePeriod,
            'num_activities':            0,
            'users_and_num_activities':  { }, # dict with kwy userid and value number of activities, to be later post-processed as a list with elements [ userid, number of activities], sorted descending by number of activities (most active users first)
        }
        return  unNuevoInforme
    
    
    


    security.declarePrivate( 'fNewVoidInformeActiveUsers')
    def fNewVoidInformeActiveUsers(self):
        """Instantiate Result for a report of recently active users.

        """
        unNuevoInforme = {
            'success':        False,
            'report_date':    None,
            'member_infos':   [ ],
            'admin_infos':    [ ],
            'last_contributions_report_title': '',
            'last_contributions_report_URL':   '',
        }
        return  unNuevoInforme
    
    

        