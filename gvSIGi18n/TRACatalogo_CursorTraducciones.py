# -*- coding: utf-8 -*-
#
# File: TRACatalogo_CursorTraducciones.py
#
# Copyright (c) 2009 by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.gvSIGi18n.config import *

##code-section module-header #fill in your manual code here



import sys
import traceback

import logging

import transaction

from math import floor

import time

from DateTime import DateTime

from StringIO import StringIO


from AccessControl      import ClassSecurityInfo

from Products.Archetypes.utils import shasattr

from Products.CMFCore.utils import getToolByName

from Products.CMFCore       import permissions



from TRAElemento_Constants import *

from TRAElemento_Permission_Definitions import cBoundObject, cUseCase_InvalidateStringTranslations
from TRAElemento_Permission_Definitions import cUseCase_BrowseTranslations, cUseCase_TRATraduccionStateChange, cUseCase_TRATraduccionComment
from TRAElemento_Permission_Definitions import cStateChangeActionRoles, cInvalidateStringTranslationsRoles,cDeactivateStringsRoles, cActivateStringsRoles






##/code-section module-header



##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema


##code-section after-schema #fill in your manual code here





cIgnoreIdiomaReferenciaString = '--'

cIgnoreNombreModuloString     = '--'




cCriterioBusquedaPorId      = { 'getEstadoCadena':cEstadoCadenaActiva, 'getId': ''}           
cCriterioEstadoCadena       = { 'getEstadoCadena':cEstadoCadenaActiva,  }           


cCriterioBusquedaBasica     = { 'getEstadoCadena':cEstadoCadenaActiva,  }           
cClavesBusquedaInformeTodas = ['getEstadoCadena',]
cCriterioBusquedaTodas      = { 'getEstadoCadena':cEstadoCadenaActiva,  }           

        

cCriterioBusqueda_RecuperarDatosTraduccionesPorSimbolos   = { 'getEstadoCadena': cEstadoCadenaActiva,  'getSimbolo': [], }           


cClavesBusquedaInformeTodasOSimbolos = cClavesBusquedaInformeTodas + [ 'getSimbolo',]

cClavesBusquedaInformeTodasOSimbolosOEstados = cClavesBusquedaInformeTodasOSimbolos + [ 'getEstadoTraduccion',]


cClavesAEliminarDeBusquedasParaInforme = [ 'sort_on', 'sort_order', 'sort_limit', ]

cEarliestFechaBusquedaTraducciones    = '1900-01-01%s%s' % ( cISOStringFechaYHoraSeparator, cISOStringEarliestDayTime,)


##/code-section after-schema

class TRACatalogo_CursorTraducciones:
    """
    """
    security = ClassSecurityInfo()


    ##code-section class-header #fill in your manual code here
    
    

  

    
    # ##############################################################################
    """The methods below construct Report Results structures serving both as factories and contract documentation
    
    """
    
           

    
    security.declarePrivate( 'fNewVoidInformeEstadosVacio')
    def fNewVoidInformeEstadosVacio(self):
        """Instantiate a status report.
        
        """
        
        unInforme = {
            'Total':        ['Total',     0, 100, None, ][:], 
        }
        unInforme.update( dict( [ ( aEstado, [ aEstado, 0, 0,   None, ][:], ) for aEstado in cTodosEstados]))
        return unInforme
        
    
    
    

    
       
    
 
    security.declarePrivate( 'fNewVoidChangeAndBrowseTraslationsResult')
    def fNewVoidChangeAndBrowseTraslationsResult( self,):
        unResult ={
            'success':                      False,
            'condition':                    '',
            'exception':                    '',
            'change_result':                self.fNewVoidChangeTranslationResult(),
            'browse_result':                self.fNewVoidBrowseTraslationsResult(),
            'languages_names_and_flags':    {},
        }
        return unResult
    
    

     
    
    security.declarePublic( 'fNewVoidChangeTranslationServiceResult')
    def fNewVoidChangeTranslationServiceResult( self,):
        unResult ={
            'success':                      False,
            'condition':                    '',
            'exception':                    '',
            'requested_change_kind':        '',                
            'codigo_idioma_a_traducir':     '',
            'simbolo_cadena_a_traducir':    '',
            'cadena_traducida_solicitada':  '',
            'change_result':                self.fNewVoidChangeTranslationResult(),
            'retrieval_result':             self.fNewVoidBrowseTraslationsResult(),
        }
        return unResult
    
         

    
    security.declarePrivate( 'fNewVoidBrowseTraslationsResult')
    def fNewVoidBrowseTraslationsResult(self):
        """Instantiate an empty TRATraduccion cursor report.
        
        """
        
        unResult = {
            'success'                    : False,
            'condition'                  : '',
            'exception'                  : '',
            'duration':                  0,
            'estadosIncluidos'           : cTodosEstados[:],
            'search_parameters'          : {},
            'informeEstadosTodasCadenas' : self.fNewVoidInformeEstadosVacio().copy(),
            'informeEstadosFiltrados'    : self.fNewVoidInformeEstadosVacio().copy(),
            'traduccionesPorPagina'      : str( self.fTraduccionesPorPaginaPorDefecto()),
            'datosTraducciones'          : [],
            'read_permission'            : False,
            'write_permission'           : False,            
            'use_case_query_results'     : [ ],        
            'allowed_state_transitions'  : {},
            'all_target_state_changes'   : [ ],
            'allow_invalidate_string_translations': False,
            'browsing_inactive_strings'  : False,
            'allow_deactivate_strings'   : False,
            'allow_activate_strings'     : False,
            'from_translation_index':    0,
            'to_translation_index':      0,
            'total_translations':        0,
        }
        return unResult
     

     

                    
    
    
    

            


  
    security.declarePublic( 'fService_ChangeTranslation')
    def fService_ChangeTranslation( self, 
        theChangeRequestParameters, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None): 
        """Process Asynchronous change request.
        
        """

        # ####################################################
        """Delay used only during debug to cause a number of translations left unsent in the client and test the close page action.
        
        """
        unSleepSecondsString = theChangeRequestParameters.get( 'sleep_seconds', '')
        if unSleepSecondsString:
            unSleepSeconds = 0.0
            try:
                unSleepSeconds = float( unSleepSecondsString)
            except:
                None
            if unSleepSeconds >= 0.01:
                time.sleep( unSleepSeconds)

        
        # ##################################################################
        """Record execution and chain in the trace and profiling history/stack.
        
        """
        unExecutionRecord = self.fStartExecution( 'method', 'fService_ChangeTranslation', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }, str( theChangeRequestParameters or 'no_parameters')) 

        try:
            if  ( self.REQUEST.HTTP_ACCEPT_CHARSET.lower().find( 'utf-8') >=0):
                if not ( self.REQUEST.response.headers[ 'content-type'].lower().find( 'utf-8') >=0):
                    self.REQUEST.response.headers[ 'content-type'] = self.REQUEST.response.headers[ 'content-type'] + ';charset=utf-8;'
            
            unResult = self.fNewVoidChangeTranslationServiceResult()
            
           
            # ##################################################################
            """Pass if no service request.
            
            """
            
            if not theChangeRequestParameters:
                return unResult

            
            # ##################################################################
            """Include service request parameters in service result.
            
            """
            
            unResult.update( {
                'change_counter':               theChangeRequestParameters.get( 'change_counter',            ''),   
                'requested_change_kind':        theChangeRequestParameters.get( 'requested_change_kind',     ''),                
                'codigo_idioma_a_traducir':     theChangeRequestParameters.get( 'codigo_idioma_a_traducir',  ''),
                'simbolo_cadena_a_traducir':    theChangeRequestParameters.get( 'simbolo_cadena_a_traducir', ''),
                'cadena_traducida_solicitada':  theChangeRequestParameters.get( 'cadena_traducida',          ''),
                'comentario_solicitado':        theChangeRequestParameters.get( 'comentario',                ''),     
            })
            
            
            
            # ##################################################################
            """Initialize permissions and roles cache if not already supplied by servicecaller.
            
            """
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
            
            from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fMillisecondsNow
            
            try: 
        
                unBrowseStart       = fMillisecondsNow()
                try:
                    try:
                    
                        # ##################################################################
                        """Process change request.
                        
                        """
                        unChangeResult = self.fChangeTranslations( theChangeRequestParameters, unPermissionsCache, unRolesCache, unExecutionRecord)
                        if unChangeResult:
                            unResult[ 'change_result'] = unChangeResult
                    
                                            
                    finally:
                        unResult[ 'change_duration']  = fMillisecondsNow() - unBrowseStart
    
                        
                        
                        
                    unRetrieveStart       = fMillisecondsNow()
                    try:
                        
                        # ##################################################################
                        """Search and retrieve.
                        
                        """
                        unaIdCadena = unChangeResult.get( 'idCadena', '')
                        if unaIdCadena:
                            
                            unosSearchParameters = {
                                'idioma':   theChangeRequestParameters.get( 'codigo_idioma_a_traducir',    ''),
                                'idCadena': unaIdCadena,
                            }
                            unRetrievalResult = unResult[ 'retrieval_result']      
                            self.pInformeYDatosTraducciones( 
                                unRetrievalResult,
                                unosSearchParameters, 
                                False, 
                                unPermissionsCache, 
                                unRolesCache,
                                unExecutionRecord
                            )
                                                    
                    finally:
                         
                        unResult[ 'retrieve_duration']   = fMillisecondsNow() - unBrowseStart
    
                finally:
                    unResult[ 'duration'] = fMillisecondsNow() - unBrowseStart
                    unResult[ 'success'] = ( unResult.get( 'change_result', None) and unResult.get( 'change_result', None).get('success', False)) and \
                         ( unResult.get( 'retrieval_result', None) and unResult.get( 'retrieval_result', None).get('success', False))
                     
                   
                    # ####################################################################
                    # ACV 20091209 We are now returning a response as HTML, which the client inserts into its DOM tree for inspection.
                    # This means that values are encoded property, and shall be decoded properly, as all TAL generated content does.
                    # Someday we may get back to using this with a JSON flavor, possibly the right decision for this communication (other than CORBA, but that's life ..., putting up with bad technological choices).
                    #
                    #unServiceSuccess    =       ( unResult or {}).get( 'success', False);
                    #unChangeResult      =       (( unServiceSuccess and unResult)or {}).get( 'change_result', {});
                    #unChangedSuccess    =       ( unChangeResult or {}).get( 'success', False);
                    #unChangedStatus     =       ( unChangeResult or {}).get( 'status', '');
                    #unRetrievalResult   =       (( unServiceSuccess and unResult)or {}).get( 'retrieval_result', {});
                    #unRetrievalSuccess  =       ( unRetrievalResult or {}).get( 'success', False);
                    #unDatosTraducciones =       (( unRetrievalSuccess and unRetrievalResult) or {}).get( 'datosTraducciones', []);
                    #unosDatosTraduccion =       ( unDatosTraducciones and unDatosTraducciones[ 0]) or {};
                    #unUsuarioTraduccion =       ( unosDatosTraduccion and unosDatosTraduccion[ 'getUsuarioTraductor']) or '';
                    #unaFechaTraduccion  =       ( unosDatosTraduccion and unosDatosTraduccion[ 'getFechaTraduccionTextual']) or '';
                    #unaNuevaCadenaTraducida =   ( unosDatosTraduccion and unosDatosTraduccion[ 'getCadenaTraducida']) or '';
                    #unNuevoEstadoTraduccion=    ( unosDatosTraduccion and unosDatosTraduccion[ 'getEstadoTraduccion']) or '';
                    #unNuevoContadorCambios   =  ( unosDatosTraduccion and unosDatosTraduccion[ 'getContadorCambios']) or 0;
                    #unosTargetStateChanges =    (( unRetrievalSuccess and unRetrievalResult) or {}).get( 'target_state_changes_firstTranslation', []);
                    #
                    #aResultString ="""
                    #[ 
                        #[ 'success',                        '%(success)s'], 
                        #[ 'theCodigoIdiomaATraducir',       '%(theCodigoIdiomaATraducir)s'],
                        #[ 'theSimboloCadenaATraducir',      '%(theSimboloCadenaATraducir)s'],
                        #[ 'theCadenaTraducida_solicitada',  '%(theCadenaTraducida_solicitada)s'],
                        #[ 'theComentario_solicitado',       '%(theComentario_solicitado)s'],
                        #[ 'changed',                        '%(changed)s'],
                        #[ 'theCadenaTraducida',             '%(theCadenaTraducida)s'],
                        #[ 'theEstadoTraduccion',            '%(theEstadoTraduccion)s'],
                        #[ 'theContadorCambios',             '%(theContadorCambios)s'],
                        #[ 'theTargetStateChanges',          [%(theTargetStateChanges)s]],
                    #];
                        #\n""" % {
                        #'success':                        ( unChangedSuccess and u'true') or u'false',    
                        #'theCodigoIdiomaATraducir':       self.fAsUnicode( unResult.get( 'codigo_idioma_a_traducir', u'')),
                        #'theSimboloCadenaATraducir':      self.fAsUnicode( unResult.get( 'simbolo_cadena_a_traducir', u'')),
                        #'theCadenaTraducida_solicitada':  self.fAsUnicode( unResult.get( 'cadena_traducida_solicitada', u'')),
                        #'theComentario_solicitado':       self.fAsUnicode( unResult.get( 'comentario_solicitado', u'')),
                        #'changed':                        (( unChangedSuccess and unChangeResult.get( 'changed',False)) and u'true') or u'false',
                        #'theCadenaTraducida':             self.fAsUnicode( unaNuevaCadenaTraducida),
                        #'theEstadoTraduccion':            self.fAsUnicode( unNuevoEstadoTraduccion),
                        #'theContadorCambios':             ( unNuevoContadorCambios and str( unNuevoContadorCambios)) or '0',
                        #'theTargetStateChanges':          u','.join( [ "'%s'" % unEstado for unEstado in unosTargetStateChanges]),
                    #}    
               
                    #unResult[ 'result_string']   = aResultString
                      
                    
                return unResult
    
            
                            
            except:
                # ################################################################
                """Handle and report conditions when something went exceptionally wrong.
                
                """
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fService_ChangeTranslation\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                unResult[ 'success']   = False
                unResult[ 'condition'] = cResultCondition_Internal_Exception
                unResult[ 'exception'] = unInformeExcepcion
                unResult[ 'result_string']   = """[ 'success', 'false']"""
                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n::fService_ChangeTranslation').error( unInformeExcepcion)
                
                    
                return unResult
            
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()
                      
                
                            
    

            


  
    security.declarePublic( 'fChangeAndBrowseTranslations')
    def fChangeAndBrowseTranslations( self, 
        theServiceRequest, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None): 
        """Process change request and retrieve translations to browse.
        
        """

        
        # ##################################################################
        """Record execution and chain in the trace and profiling history/stack.
        
        """
        unExecutionRecord = self.fStartExecution( 'method', 'fChangeAndBrowseTranslations', theParentExecutionRecord, False) 

        try:

            unResult = self.fNewVoidChangeAndBrowseTraslationsResult()
            
            
            
            # ##################################################################
            """Pass if no service request.
            
            """
            if not theServiceRequest:
                unResult[ 'condition'] = cResultCondition_Internal_MissingParameter
                return unResult
            
             
            
            # ##################################################################
            """Initialize permissions and roles cache if not already supplied by servicecaller.
            
            """
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
            
            
            try: 
        
                
                # ##################################################################
                """Process change request.
                
                """
                unChangeRequestParameters = theServiceRequest.get( 'change_parameters', {})
                if unChangeRequestParameters:

                    unChangeResult = self.fChangeTranslations( unChangeRequestParameters, unPermissionsCache, unRolesCache, unExecutionRecord)
                    if unChangeResult:
                        unResult[ 'change_result'] = unChangeResult
                                 
                    
                    
                    
                # ##################################################################
                """Process browse request.
                
                """
                unBrowseRequestParameters = theServiceRequest.get( 'browse_parameters', {})
                if unBrowseRequestParameters:

                    unBrowseResult = unResult[ 'browse_result']                    
                    self.pBrowseTranslations( unBrowseRequestParameters, unBrowseResult, unPermissionsCache, unRolesCache, unExecutionRecord)
     
                    
                    
                            
                # ##################################################################
                """Retrieve general information, like language names and flags
                
                """
                unosLanguagesNamesAndFlags = self.fLanguagesNamesAndFlagsPorCodigo()
                if unosLanguagesNamesAndFlags:
                    unResult[ 'languages_names_and_flags'] = unosLanguagesNamesAndFlags
                            
                    
                unResult[ 'success'] = True
                    
                return unResult
    
            
                            
            except:
                # ################################################################
                """Handle and report conditions when something went exceptionally wrong.
                
                """
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fChangeAndBrowseTranslations\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                unResult[ 'success']   = False
                unResult[ 'condition'] = cResultCondition_Internal_Exception
                unResult[ 'exception'] = unInformeExcepcion
                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n::fChangeAndBrowseTranslations').error( unInformeExcepcion)
                
                    
                return unResult
            
            
            
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
                      
                
                    
    



            
            
            
  
    security.declarePrivate( 'fChangeTranslations')
    def fChangeTranslations( self, 
        theChangeParameters, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None): 
        """Process change request.
        
        """

                                

        # ##################################################################
        """Record execution and chain in the trace and profiling history/stack.
        
        """
        unExecutionRecord = self.fStartExecution( 'method', 'fChangeTranslations', theParentExecutionRecord, False) 

        try:

            unResult = self.fNewVoidChangeTranslationResult()
            
            
            # ##################################################################
            """Pass if no parameters or result.
            
            """
            if not theChangeParameters:
                return unResult
            
                        
            # ##################################################################
            """Initialize permissions and roles cache if not already supplied by servicecaller.
            
            """
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
            
    
                
                
            unChangeCounter             = theChangeParameters.get( 'change_counter',       '')                    
            unRequestedChangeKind       = theChangeParameters.get( 'requested_change_kind',       '')                    
            unCodigoIdiomaATraducir     = theChangeParameters.get( 'codigo_idioma_a_traducir',    '')
            unSimboloCadenaATraducir    = theChangeParameters.get( 'simbolo_cadena_a_traducir',   '')
            unaCadenaTraducida          = theChangeParameters.get( 'cadena_traducida',            '')
            unComentario                = theChangeParameters.get( 'comentario',                  '')
            unBatchIds_Traducida        = theChangeParameters.get( 'batch_ids_traducida',         '')
            unBatchIds_Revisada         = theChangeParameters.get( 'batch_ids_revisada',          '')
            unBatchIds_Definitiva       = theChangeParameters.get( 'batch_ids_definitiva',        '')
            
            unChangeActionResult  = None

            if ( not unSimboloCadenaATraducir) or ( ( not unCodigoIdiomaATraducir) and not ( unRequestedChangeKind in [ cRequestedChangeKind_InvalidarTraduccionesCadena, cRequestedChangeKind_DesactivarCadena, cRequestedChangeKind_ActivarCadena,])):

                unResult[ 'success']   = False
                unResult[ 'condition'] = 'Missing_parameters'
                return unResult
            
            from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fMillisecondsNow
                
            try:
                unChangeStart       = fMillisecondsNow()
                
                
                # ##################################################################
                """Dispatch requested change action.
                
                """
                if unRequestedChangeKind == cRequestedChangeKind_IntentarTraducir:
                    unChangeActionResult = self.fIntentarTraducirCadena(            
                        theSimboloCadena         =unSimboloCadenaATraducir, 
                        theCodigoIdioma          =unCodigoIdiomaATraducir, 
                        theCadenaTraducida       =unaCadenaTraducida, 
                        theComentario            =unComentario, 
                        theAdditionalParams      ={ 'theContadorCambios': unChangeCounter, },
                        thePermissionsCache      =unPermissionsCache, 
                        theRolesCache            =unRolesCache, 
                        theParentExecutionRecord =unExecutionRecord,
                    )    

                elif unRequestedChangeKind == cRequestedChangeKind_Comentar:
                    unChangeActionResult = self.fComentarTraduccionCadena(          
                        theSimboloCadena         =unSimboloCadenaATraducir, 
                        theCodigoIdioma          =unCodigoIdiomaATraducir, 
                        theComentario            =unComentario, 
                        theAdditionalParams      ={ 'theContadorCambios': unChangeCounter, },
                        thePermissionsCache      =unPermissionsCache, 
                        theRolesCache            =unRolesCache, 
                        theParentExecutionRecord =unExecutionRecord,
                    )    
                    
                elif unRequestedChangeKind == cRequestedChangeKind_HacerPendiente:
                    unChangeActionResult = self.fHacerPendienteTraduccionCadena(    
                        theSimboloCadena         =unSimboloCadenaATraducir, 
                        theCodigoIdioma          =unCodigoIdiomaATraducir, 
                        theComentario            =unComentario, 
                        theAdditionalParams      ={ 'theContadorCambios': unChangeCounter, },
                        thePermissionsCache      =unPermissionsCache, 
                        theRolesCache            =unRolesCache, 
                        theParentExecutionRecord =unExecutionRecord,
                    )    

                elif unRequestedChangeKind == cRequestedChangeKind_HacerTraducida:
                    unChangeActionResult = self.fHacerTraducidaTraduccionCadena(    
                        theSimboloCadena         =unSimboloCadenaATraducir, 
                        theCodigoIdioma          =unCodigoIdiomaATraducir, 
                        theComentario            =unComentario, 
                        theAdditionalParams      ={ 'theContadorCambios': unChangeCounter, },
                        thePermissionsCache      =unPermissionsCache, 
                        theRolesCache            =unRolesCache, 
                        theParentExecutionRecord =unExecutionRecord,
                    )    

                elif unRequestedChangeKind == cRequestedChangeKind_HacerRevisada:
                    unChangeActionResult = self.fHacerRevisadaTraduccionCadena(     
                        theSimboloCadena         =unSimboloCadenaATraducir, 
                        theCodigoIdioma          =unCodigoIdiomaATraducir, 
                        theComentario            =unComentario, 
                        theAdditionalParams      ={ 'theContadorCambios': unChangeCounter, },
                        thePermissionsCache      =unPermissionsCache, 
                        theRolesCache            =unRolesCache, 
                        theParentExecutionRecord =unExecutionRecord,
                    )    
                    
                elif unRequestedChangeKind == cRequestedChangeKind_HacerDefinitiva:
                    unChangeActionResult = self.fHacerDefinitivaTraduccionCadena(   
                        theSimboloCadena         =unSimboloCadenaATraducir, 
                        theCodigoIdioma          =unCodigoIdiomaATraducir, 
                        theComentario            =unComentario, 
                        theAdditionalParams      ={ 'theContadorCambios': unChangeCounter, },
                        thePermissionsCache      =unPermissionsCache, 
                        theRolesCache            =unRolesCache, 
                        theParentExecutionRecord =unExecutionRecord,
                    )    
                elif unRequestedChangeKind == cRequestedChangeKind_BatchCambioEstado:
                    unChangeActionResult = self.fLoteCambiosEstadoTraduccionesCadenas(   
                        theBatchIds_Traducida       =unBatchIds_Traducida, 
                        theBatchIds_Revisada        =unBatchIds_Revisada,
                        theBatchIds_Definitiva      =unBatchIds_Definitiva,        
                        theCodigoIdioma             =unCodigoIdiomaATraducir,  
                        theAdditionalParams         ={ 'theContadorCambios': unChangeCounter, },
                        thePermissionsCache         =unPermissionsCache, 
                        theRolesCache               =unRolesCache, 
                        theParentExecutionRecord    =unExecutionRecord,
                        
                    )    

                elif unRequestedChangeKind == cRequestedChangeKind_InvalidarTraduccionesCadena:
                    unChangeActionResult = self.fInvalidarTraduccionesCadenas(   
                        theSimboloCadena            =unSimboloCadenaATraducir, 
                        theComentario               =unComentario, 
                        theAdditionalParams         ={ 'theContadorCambios': unChangeCounter, },
                        thePermissionsCache         =unPermissionsCache, 
                        theRolesCache               =unRolesCache, 
                        theParentExecutionRecord    =unExecutionRecord,
                    )    

                elif unRequestedChangeKind == cRequestedChangeKind_DesactivarCadena:
                    unChangeActionResult = self.fDesactivarCadena(   
                        theSimboloCadena            =unSimboloCadenaATraducir, 
                        theComentario               =unComentario, 
                        theAdditionalParams         ={ 'theContadorCambios': unChangeCounter, },
                        thePermissionsCache         =unPermissionsCache, 
                        theRolesCache               =unRolesCache, 
                        theParentExecutionRecord    =unExecutionRecord,
                    )    

                elif unRequestedChangeKind == cRequestedChangeKind_ActivarCadena:
                    unChangeActionResult = self.fActivarCadena(   
                        theSimboloCadena            =unSimboloCadenaATraducir, 
                        theComentario               =unComentario, 
                        theAdditionalParams         ={ 'theContadorCambios': unChangeCounter, },
                        thePermissionsCache         =unPermissionsCache, 
                        theRolesCache               =unRolesCache, 
                        theParentExecutionRecord    =unExecutionRecord,
                    )    

                if unChangeActionResult:
                    unChangeActionResult[ 'duration']    = fMillisecondsNow() - unChangeStart
                    
                    return unChangeActionResult

                unResult[ 'duration']   = fMillisecondsNow() - unChangeStart
                return unResult


                    
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fChangeTranslations\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                unResult[ 'success']   = False
                unResult[ 'condition'] = cResultCondition_Internal_Exception
                unResult[ 'exception'] = unInformeExcepcion
                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n::fChangeTranslations').error( unInformeExcepcion)
                             
                return self

            
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
                      
                
                    
    
                
            
            
            


  
    security.declarePrivate( 'pBrowseTranslations')
    def pBrowseTranslations( self, 
        theBrowseParameters, 
        theBrowseResult,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None): 
        """Search and Retrieve.
        
        """

        # ##################################################################
        """Record execution and chain in the trace and profiling history/stack.
        
        """
        unExecutionRecord = self.fStartExecution( 'method', 'pBrowseTranslations', theParentExecutionRecord, False) 

        try:

            # ##################################################################
            """Pass if no parameters or result.
            
            """
            if not theBrowseResult:
                return self
            
                        
            if not theBrowseParameters:
                unResult[ 'condition'] = cResultCondition_Internal_MissingParameter
                return self
            
                        
            # ##################################################################
            """Initialize permissions and roles cache if not already supplied by servicecaller.
            
            """
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
            from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fMillisecondsNow
           
            try:
                unBrowseStart       = fMillisecondsNow()
                
                try:
                    
                    # ##################################################################
                    """Search and retrieve.
                    
                    """
                    unosSearchParameters = theBrowseParameters.get( 'search_parameters', {})
                    unMostrarInforme     = theBrowseParameters.get( 'include_summary', False)
                          
                    self.pInformeYDatosTraducciones( 
                        theBrowseResult,
                        unosSearchParameters, 
                        unMostrarInforme, 
                        unPermissionsCache, 
                        unRolesCache,
                        unExecutionRecord
                    )
                                            
                    return self

                finally:
                    theBrowseResult[ 'duration']             = fMillisecondsNow() - unBrowseStart

                    
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during pBrowseTranslations\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                theBrowseResult[ 'success']   = False
                theBrowseResult[ 'condition'] = cResultCondition_Internal_Exception
                theBrowseResult[ 'exception'] = unInformeExcepcion
                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n::pBrowseTranslations').error( unInformeExcepcion)
                             
                return self

            
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
                      
                
                    
                
            
   
            
            
            
            

  
    security.declarePrivate( 'pInformeYDatosTraducciones')
    def pInformeYDatosTraducciones( self, 
        theReport,
        theSearchParameters, 
        theElaborarInforme          =False, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None): 
        """Retrieve a maximum number of TRATraduccion records starting from the supplied cursor symbol matching search criteria and optionally including a summary.
        
        REPORT A LIST WITH A SPECIFIED NUMBER OF TRANSLATIONS INTO A LANGUAGE
        IN SYMBOL ALPHABETICAL ORDER, STARTING IN THE ONE PROVIDED AS CURSOR,
        AND MATCHING SEARCH CONDITIONS
        OPTIONALLY INCLUDING A SUMMARY REPORT
        OPTIONALLY INCLUDING TRANSLATIONS OF SAME SYMBOLS INTO ADDITIONAL LANGUAGES

        This is the main access to translations retrieval for translation and reviewing effort.
        This is the most performance-critical application service !!!    
     
        """
        
        # ##################################################################
        """Record execution and chain in the trace and profiling history/stack.
        
        """
        unExecutionRecord = self.fStartExecution( 'method', 'pInformeYDatosTraducciones', theParentExecutionRecord, False) 

        try:
            if not theReport:
                return self     
                
            try:
                unCodigoIdiomaEnGvSIG = theSearchParameters.get( 'idioma', '')
                if not unCodigoIdiomaEnGvSIG:
                    theReport[ 'success']   = False
                    theReport[ 'condition'] = cResultCondition_MissingParameter_CodigoIdioma
                    return self    
                
                
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache

                try:
                    
                    # ##################################################################
                    """Check if the translations catalog allows modifications or is locked for writing.
                    
                    """
                    unAllowWrite = self.fAllowWrite()
                    
                    
    
                    # ##################################################################
                    """Retrieve languages and modules available for translation browsing by the connected user.
                    
                    """
                    unBrowseUseCaseQueryResult = self.fUseCaseAssessment(  
                        theUseCaseName          = cUseCase_BrowseTranslations, 
                        theElementsBindings     = { cBoundObject: self,},
                        theRulesToCollect       = [ 'languages', 'modules', 'changeable_languages', 'changeable_modules',], 
                        thePermissionsCache     = unPermissionsCache, 
                        theRolesCache           = unRolesCache, 
                        theParentExecutionRecord= unExecutionRecord
                    )    
                    if not ( unBrowseUseCaseQueryResult and unBrowseUseCaseQueryResult.get( 'success', False)):
                        theReport[ 'success']   = False
                        theReport[ 'condition'] = cResultCondition_UseCaseAssessmentFailure_BrowseTranslations
                        return self    
                
                    theReport[ 'use_case_query_results'].append( unBrowseUseCaseQueryResult)  
                    
                    
                    
                    
                    unosIdiomasAccesibles   = unBrowseUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'languages', {}).get( 'accepted_final_objects', [])
                    unosIdiomasModificables = []
                    if unAllowWrite:
                        unosIdiomasModificables = unBrowseUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'changeable_languages', {}).get( 'accepted_final_objects', [])
                        
                    # Nobody uses this, and is redundant with the use case assessment results above
                    #
                    # theReport[ 'writable_language_codes'] = [ unIdioma.getCodigoIdiomaEnGvSIG() for unIdioma in unosIdiomasModificables]
                    
    
                        
                        
                    # ##################################################################
                    """Check language selected for browsing is among the accesible ones.
                    
                    """                    
                    unIdiomaCursor = None
                     
                    for unIdioma in unosIdiomasAccesibles:
                        if unIdioma.getCodigoIdiomaEnGvSIG() == unCodigoIdiomaEnGvSIG:
                            unIdiomaCursor = unIdioma
                            break
                        
                    if not unIdiomaCursor:
                        theReport[ 'success']   = False
                        theReport[ 'condition'] = cResultCondition_LanguageNotAccessible
                        return self    
                    
                    
                    
                    
                     # ##################################################################
                    """Check language selected for browsing is among the modifiable ones.
                    
                    """  
                    unIdiomaCursorModifiable = unAllowWrite and ( unIdiomaCursor in unosIdiomasModificables)
                    theReport[ 'write_permission'] = unIdiomaCursorModifiable
 
                      
                    
                     # ##################################################################
                    """Get connected user roles at language to browse.
                    
                    """
                    unosRolesEnIdiomaCursor = self.fGetElementRoles( unIdiomaCursor, unRolesCache)
                    
                     
                     # ##################################################################
                    """Get connected user roles at root catalog. 
                    Relevant for the Invalidate String Translations use case, which is not language specific, but rather affects all languages.
                    
                    """
                    unCatalogo = unIdiomaCursor.getCatalogo()
                    
                    unosRolesEnCatalogo = self.fGetElementRoles( unCatalogo, unRolesCache)
                    
                     
                            
                            
                            
                    # ##################################################################
                    """Get accessible modules from use case assessment result.
                    
                    """
                    unosModulosAccesibles = unBrowseUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'modules', {}).get( 'accepted_final_objects', [])
                    unosModulosModificables = []
                    if unAllowWrite:
                        unosModulosModificables = unBrowseUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'changeable_modules', {}).get( 'accepted_final_objects', [])

                    # Nobody uses this, and is redundant with the use case assessment results above
                    #
                    #theReport[ 'writable_module_names'] = [ unModulo.Title() for unModulo in unosModulosModificables]
                    
                    
                    
                    
                    # ##################################################################
                    """Validate module rights access, if there is no module in translations catalog, or at least one module is accessible.
                    
                    """
                    todosModulosExistentes = self.fObtenerTodosModulos()
                    if todosModulosExistentes and not unosModulosAccesibles:
                        theReport[ 'success']   = False
                        theReport[ 'condition'] = cResultCondition_NoModulesAccessible
                        return self    
                    
                    
                    
                    # #################################################################
                    """Check for Roles for use case to invalidate string translations.
                    
                    """
                    if set( cInvalidateStringTranslationsRoles).intersection( unosRolesEnCatalogo):
                        if unAllowWrite:
                            theReport[ 'allow_invalidate_string_translations']  = True      
                     
                    
                    
                    
                    # #################################################################
                    """Report whether browsing only the translations for Strings in Inactive state.
                    
                    """
                    if theSearchParameters.get( 'cadenasInactivas', '').strip().lower() == "on":
                        theReport[ 'browsing_inactive_strings']  = True      
                            
                            
                    
                    
                    # #################################################################
                    """When not browsing Inactive Strings, Check for Roles for use case to invalidate string translations.
                    
                    """
                    if not( theSearchParameters.get( 'cadenasInactivas', '').strip().lower() == "on"):
                        if set( cDeactivateStringsRoles).intersection( unosRolesEnCatalogo):
                            if unAllowWrite:
                                theReport[ 'allow_deactivate_strings']  = True      
                            
                            
                    
                    # #################################################################
                    """If browsing Inacive Strings, Check for Roles for use case to invalidate string translations.
                    
                    """
                    if theSearchParameters.get( 'cadenasInactivas', '').strip().lower() == "on":
                        if set( cActivateStringsRoles).intersection( unosRolesEnCatalogo):
                            if unAllowWrite:
                                theReport[ 'allow_activate_strings']    = True      
                            
                            
                     
                    # #################################################################
                    """Unless the catalog or the language are not modifiable, determine state transitions permitted to the connected user for translations in the language requested to browse and accessible module.
                    
                    """
                    unasAllowedStateTransitions     = { }
                    unosAllTargetStateChanges       = set( )
                    
                    
                    """Get connected user roles at any of the accessible modules.
                    
                    """
                    unosRolesEnTodosModulos = set()
                    
                    for unModulo in unosModulosAccesibles:
                        unosRolesEnModulo   = unModulo.fGetElementRoles( unModulo, unRolesCache)
                        unosRolesEnTodosModulos.update( unosRolesEnModulo)
                    
                    
                    if unIdiomaCursorModifiable:
                    
                        for unEstado in cTodosEstados:
                
                            unasStateChangeRules = cStateChangeActionRoles.get( unEstado, None)
                            unosEstadosFinales = set( )
                
                            unasAllowedStateTransitions[ unEstado] = unosEstadosFinales
                            
                            if unasStateChangeRules:
                                unosEstadosFinalesInRule = unasStateChangeRules.keys()
                                if unosEstadosFinalesInRule:
                                    for unEstadoFinal in unosEstadosFinalesInRule:
                                        unosRolesRequeridosParaTransicion = unasStateChangeRules.get( unEstadoFinal, set())
                                        if unosRolesRequeridosParaTransicion:
                                            if set( unosRolesRequeridosParaTransicion).intersection( unosRolesEnIdiomaCursor).intersection( unosRolesEnTodosModulos):
                                                unosEstadosFinales.add( unEstadoFinal)
                                                unosAllTargetStateChanges.add( unEstadoFinal)
                        
                        theReport[ 'allowed_state_transitions'] = unasAllowedStateTransitions      
                        theReport[ 'all_target_state_changes']  = unosAllTargetStateChanges      
                    
                                            
                           
                                            
                    # ##############################################################            
                    """If requested browsing just one translation by its string id, 
                    retrieve the one TRATRaduccion in the Language for the TRACadena with the exact identifier (Plone id).
                    Optionally retrieve the TRATraducion to a number of reference Languages.
                     
                    """ 
                    if len( theSearchParameters.get( 'idCadena', '').strip()) > 0:
                        self.pEstrategiaBusqueda_PorIdCadena( 
                            theReport, 
                            unBrowseUseCaseQueryResult, 
                            unIdiomaCursor, 
                            unCodigoIdiomaEnGvSIG, 
                            theSearchParameters, 
                            theElaborarInforme, 
                            theParentExecutionRecord=unExecutionRecord
                        )
                        return self
                    
    
                    
                    
                    
                    
 
                    # ################################################################
                    """If requested browsing a batch of translations starting in the one with symbol suplied as cursor
                    Retrieve up to a number of TRATraduccion ordered by their string symbol.
                    Optionally filter  by additional constraints by module, text search, users involved and dates.
                    Optionally retrieve the TRATraducion to a number of reference Languages.
                    
                    """
                    
                    
                    # ################################################################
                    """Compose search criteria from constraints specified in the request.
                    
                    """
                    unCriterioSeleccionTraducciones = self.fComponerSeleccionTraducciones( 
                        unBrowseUseCaseQueryResult, 
                        unIdiomaCursor, 
                        unCodigoIdiomaEnGvSIG, 
                        theSearchParameters, 
                        theParentExecutionRecord    =unExecutionRecord
                    )
             
                    unCriterioBusquedaTraducciones  = self.fComponerBusquedaTraducciones(  
                        unBrowseUseCaseQueryResult, 
                        unIdiomaCursor, 
                        unCodigoIdiomaEnGvSIG, 
                        theSearchParameters, 
                        theParentExecutionRecord    =unExecutionRecord
                    )
                         
                    unCriterioFiltroTraducciones    = self.fComponerFiltroTraducciones(    
                        unBrowseUseCaseQueryResult, 
                        unIdiomaCursor, 
                        unCodigoIdiomaEnGvSIG, 
                        theSearchParameters, 
                        theParentExecutionRecord    =unExecutionRecord
                    )
                         
                    
                    
                    
                    
        
                    # ################################################################
                    """If requested a summary.
                    
                    """
                    if theElaborarInforme:
                        self.pEstrategiaBusqueda_ConInforme( 
                            theReport, 
                            unBrowseUseCaseQueryResult, 
                            unIdiomaCursor, 
                            unCodigoIdiomaEnGvSIG, 
                            theSearchParameters, 
                            unCriterioSeleccionTraducciones, 
                            unCriterioBusquedaTraducciones, 
                            unCriterioFiltroTraducciones, 
                            theParentExecutionRecord    =unExecutionRecord
                        )
                        
                        return self
                    
                    
                    
                    # ################################################################
                    """If no summary  requested.
                    
                    """
                    self.pEstrategiaBusqueda_SinInforme(     
                        theReport, 
                        unBrowseUseCaseQueryResult, 
                        unIdiomaCursor, 
                        unCodigoIdiomaEnGvSIG, 
                        theSearchParameters, 
                        unCriterioSeleccionTraducciones, 
                        unCriterioBusquedaTraducciones, 
                        unCriterioFiltroTraducciones, 
                        theParentExecutionRecord    =unExecutionRecord
                    )
                    return self
                
                
                finally:
                    theReport[ 'success'] = True

                    unosDatosTraducciones = theReport.get('datosTraducciones', [])
                    if unosDatosTraducciones:
                        
                        # ################################################################
                        """The first translation retrieved will be the one to edit or change state.
                        
                        """
                        
                        unosDatosTraduccionSeleccionada = unosDatosTraducciones[ 0]
                        if unosDatosTraduccionSeleccionada:

                             
                             
                            # ################################################################
                            """Report whether the connected user can request commenting the translation, even at the cost of launching another use case assessment.
                            Try and see if this can be determined from the assesments made on languages and modules, as it should.
                            
                            """
                            unaTraduccionSeleccionada = unosDatosTraduccionSeleccionada.getObject()
                            if unaTraduccionSeleccionada:
                                unCommentUseCaseQueryResult = self.fUseCaseAssessment(  
                                    theUseCaseName          = cUseCase_TRATraduccionComment, 
                                    theElementsBindings     = { cBoundObject: unaTraduccionSeleccionada,},
                                    theRulesToCollect       = None, 
                                    thePermissionsCache     = unPermissionsCache, 
                                    theRolesCache           = unRolesCache, 
                                    theParentExecutionRecord= unExecutionRecord) 
                                if unCommentUseCaseQueryResult:
                                    theReport[ 'use_case_query_results'].append( unCommentUseCaseQueryResult)
                             
                            
            except:
                # ################################################################
                """Handle and report conditions when something went exceptionally wrong.
                
                """
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during pInformeYDatosTraducciones\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                theReport[ 'success'] = False
                theReport[ 'condition'] = cResultCondition_Internal_Exception
                theReport[ 'exception'] = unInformeExcepcion
                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n::pInformeYDatosTraducciones').error( unInformeExcepcion)
                
                return self
            
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
                      
                
                
                

                
                
                
                
                
      


    security.declarePrivate( 'pEstrategiaBusqueda_PorIdCadena')
    def pEstrategiaBusqueda_PorIdCadena( self, 
        theReport, 
        theUseCaseQueryResult, 
        theIdioma, 
        theCodigoIdioma, 
        theSearchParameters, 
        theElaborarInforme=False, 
        theParentExecutionRecord=None):
        """Retrieve a single TRATraduccion records by lookup by TRACadena id.
    
        The simplest of these retrieval algorithms

        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'pEstrategiaBusqueda_PorIdCadena', theParentExecutionRecord, False) 

        try:
                       
            theSearchParameters.update( {
                'estadosAIncluir':      cTodosEstados[:],
                'simbolo':              '',
                'modoDesplazamiento':   '', 
                'cadenaTraducida':      '',
                'nombreModulo':         '',
                'usuarioCreador':       '',
                'fechaCreacionInicial': '',
                'fechaCreacionFinal':   '',
                'usuarioTraductor':     '',
                'fechaTraduccionInicial':'',
                'fechaTraduccionFinal': '',
                'usuarioRevisor':       '',
                'fechaRevisionInicial': '',
                'fechaRevisionFinal':   '',
                'usuarioCoordinador':   '',
                'fechaDefinitivoInicial':'',
                'fechaDefinitivoFinal': '',
            })
            
            theReport[ 'estadosIncluidos']      = cTodosEstados[:]
            theReport[ 'traduccionesPorPagina'] = str( self.fTraduccionesPorPagina( theSearchParameters))
    
            if not theCodigoIdioma:
                theReport[ 'condition'] = cResultCondition_MissingParameter_CodigoIdioma
                return theReport
            
            theReport[ 'read_permission']  = True
            
            anIdCadena = theSearchParameters.get( 'idCadena', '').strip()
            if not anIdCadena:
                theReport[ 'condition'] = cResultCondition_MissingParameter_IdCadena
                return theReport

            aTraduccionId =  self.fIdTraduccionDesdeIdCadenaYLenguage( anIdCadena, theCodigoIdioma)
            if not aTraduccionId:
                return theReport
            
            unaBusqueda = {}
            unaBusqueda.update( cCriterioBusquedaPorId)
            unaBusqueda[ 'getId'] = aTraduccionId 
            
            
            if theSearchParameters.get( 'cadenasInactivas', '').strip().lower() == "on":
                unCriterioBusqueda[ 'getEstadoCadena'] = cEstadoCadenaInactiva

            unosDatosTraducciones = self.fBuscarTraduccionesEnCatalogoConDatosDeIdioma( 
                theIdioma, 
                theCodigoIdioma, 
                unaBusqueda, 
                theParentExecutionRecord=unExecutionRecord
            )
            
            if len( unosDatosTraducciones) > 0:
                unosDatosTraduccion = unosDatosTraducciones[ 0]
                if unosDatosTraduccion:
                    
                    # #################################
                    """Validate module rights access.
                    
                    """
 
                    unaTraduccion = unosDatosTraduccion.getObject()
                    if unaTraduccion:
                        unaCadena = unaTraduccion.getCadena()
                        if unaCadena:
                            unosModulos = unaCadena.fObtenerModulos()
                            if unosModulos:
                                
                                unosModulosAccesibles = theUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'modules', {}).get( 'accepted_final_objects', [])
                             
                                if not set( unosModulos).intersection( set( unosModulosAccesibles)):
                                    return theReport
                                    
                                    
                # ACV to do 20090324 checks for visibility of the language and modules may have already been assessed before reaching here, produced elsewhere    
                unosDatosARetornar             = unosDatosTraducciones[0:1]                

                theReport[ 'datosTraducciones'] = unosDatosARetornar
                theReport[ 'total_translations'] = 1
                theReport[ 'from_translation_index'] = 1
                theReport[ 'to_translation_index'] = 1
                theReport[ 'success'] = True
                
                if theElaborarInforme:
                    
                    unosDatosTraduccion = unosDatosARetornar[ 0]
                    unEstadoTraduccion  = unosDatosTraduccion[ 'getEstadoTraduccion']
                    theReport[ 'informeEstadosTodasCadenas'][ 'Total'][ 1] = 1
                    theReport[ 'informeEstadosTodasCadenas'][ 'Total'][ 2] = 100
                    theReport[ 'informeEstadosTodasCadenas'][ unEstadoTraduccion][ 1] = 1    
                    theReport[ 'informeEstadosTodasCadenas'][ unEstadoTraduccion][ 2] = 100    
                    theReport[ 'informeEstadosTodasCadenas'][ unEstadoTraduccion][ 3] = unosDatosARetornar    
                    theReport[ 'informeEstadosFiltrados'   ] = theReport[ 'informeEstadosTodasCadenas'].copy()    
    
                self.pIncluirIdiomasReferencia( 
                    theUseCaseQueryResult       = theUseCaseQueryResult, 
                    theSearchParameters         = theSearchParameters, 
                    theReport                   = theReport, 
                    theParentExecutionRecord    = unExecutionRecord)
                        
            return theReport
    
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
    

     

    
    
    
  
    
    
    
    
    
    
    
    
    
    
    # ##############################################################################
    """Methods below apply different strategies to retrieve the required set of TRATraduccion.
    
    Attempt in each case to use the minimum processor resources, 
    with special care in accessing the smaller ZCatalogs possible
    
    """

    
    

    security.declarePrivate( 'pEstrategiaBusqueda_SinInforme')
    def pEstrategiaBusqueda_SinInforme( self, 
        theReport, 
        theUseCaseQueryResult, 
        theIdioma, 
        theCodigoIdioma, 
        theSearchParameters, 
        theCriterioSeleccionTraducciones, 
        theCriterioBusquedaTraducciones, 
        theCriterioFiltroTraducciones, 
        theParentExecutionRecord=None):
        """Retrieve a maximum number of TRATraduccion records starting from the supplied cursor symbol matching search criteria without including a summary.
    
        Can save the effort of determining how many matches
        have been found by each state, and in the unfiltered totals
        
        """
    
        unExecutionRecord = self.fStartExecution( 'method',  'pEstrategiaBusqueda_SinInforme', theParentExecutionRecord, False) 

        try:
            
            unCriterioBusqueda = cCriterioEstadoCadena.copy()
            unCriterioBusqueda.update( theCriterioSeleccionTraducciones)
            unCriterioBusqueda.update( theCriterioBusquedaTraducciones)
            unCriterioBusqueda.update( theCriterioFiltroTraducciones)
            
            if theSearchParameters.get( 'cadenasInactivas', '').strip().lower() == "on":
                unCriterioBusqueda[ 'getEstadoCadena'] = cEstadoCadenaInactiva

            
            theReport[ 'read_permission']  = True
               
            theReport[ 'estadosIncluidos']      = unCriterioBusqueda.get( 'getEstadoTraduccion', cTodosEstados)
                
            unosCodigosIdiomasReferencia = []
            unosCodigosIdiomasReferenciaSinValidar = set( self.fIdiomasReferenciaEnSearchParameters( theSearchParameters))
            if unosCodigosIdiomasReferenciaSinValidar:
                unosIdiomasAccesibles = theUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'languages', {}).get( 'accepted_final_objects', [])
                unosCodigosIdiomasReferencia = sorted( [ unosCodigosIdiomasReferenciaSinValidar.intersection( set( [ unResultadoIdioma[ 'getCodigoIdiomaEnGvSIG'] for unResultadoIdioma in unosIdiomasAccesibles]))])
            
            unNumIdiomasReferenciaSinIdiomaCursor = len( unosCodigosIdiomasReferencia)
            if theCodigoIdioma in unosCodigosIdiomasReferencia:
                unNumIdiomasReferenciaSinIdiomaCursor -= 1
                
            theReport[ 'traduccionesPorPagina'] = str( self.fTraduccionesPorPagina( theSearchParameters, unNumIdiomasReferenciaSinIdiomaCursor))
        
            if theCriterioSeleccionTraducciones.get( 'getSimbolo', None) == []: 
                # force empty results on account of module name or text search
                return theReport

            
            unRecuperandoEnPrimerPasoSoloInformacionDeBusqueda = False
            if self.fEsBusquedaTodasOSimbolosOEstados( unCriterioBusqueda):
                unRecuperandoEnPrimerPasoSoloInformacionDeBusqueda = True     
                unosDatosTraducciones = self.fBuscarTraduccionesEnCatalogoMinimo(           
                    theIdioma, 
                    theCodigoIdioma, 
                    unCriterioBusqueda, 
                    theParentExecutionRecord=unExecutionRecord
                )
            else:
                unRecuperandoEnPrimerPasoSoloInformacionDeBusqueda = False                                
                unosDatosTraducciones = self.fBuscarTraduccionesEnCatalogoConDatosDeIdioma( 
                    theIdioma, 
                    theCodigoIdioma, 
                    unCriterioBusqueda, 
                    theParentExecutionRecord=unExecutionRecord)
                
                    
            if len( unosDatosTraducciones) > 0:  
            
                unDictTraduccionesEncontradas = { }
            
                unDictTraduccionesEncontradas = self.fBuildDictBySimboloFromSearchResults( 
                    unosDatosTraducciones, 
                    theParentExecutionRecord=unExecutionRecord
                )
                
     
                self.pAplicarDesplazamientoYPaginado( 
                    theSearchParameters, 
                    theReport, 
                    unDictTraduccionesEncontradas, 
                    theParentExecutionRecord=unExecutionRecord
                )
            
                if unRecuperandoEnPrimerPasoSoloInformacionDeBusqueda:
                    self.pIncluirIdiomaBaseEIdiomasReferencia( 
                        theIdioma               = theIdioma, 
                        theUseCaseQueryResult   = theUseCaseQueryResult, 
                        theSearchParameters     = theSearchParameters, 
                        theReport               = theReport, 
                        theParentExecutionRecord=unExecutionRecord)
                else: 
                    self.pIncluirIdiomasReferencia(   
                        theUseCaseQueryResult, 
                        theSearchParameters, 
                        theReport, 
                        theParentExecutionRecord=unExecutionRecord)
               
            return theReport
            
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
 
      





  
    # ##############################################################################
    """Methods below determine the kind of constraints imposed on the search criteria
    to select the best performing algorithm for summary reporting

    """
    
    security.declarePrivate( 'fEsBusquedaTodas')
    def fEsBusquedaTodas( self, theCriterioBusqueda):
        if not theCriterioBusqueda:
            return False     
            
        return len( set( theCriterioBusqueda.keys()) - set( cClavesBusquedaInformeTodas) - set ( cClavesAEliminarDeBusquedasParaInforme ) ) == 0
        

    security.declarePrivate( 'fEsBusquedaTodasOSimbolos')
    def fEsBusquedaTodasOSimbolos( self, theCriterioBusqueda):
        if not theCriterioBusqueda:
            return False     
            
        return len( set( theCriterioBusqueda.keys()) - set( cClavesBusquedaInformeTodasOSimbolos) - set ( cClavesAEliminarDeBusquedasParaInforme ) ) == 0
        


   
    security.declarePrivate( 'fEsBusquedaTodasOSimbolosOEstados')
    def fEsBusquedaTodasOSimbolosOEstados( self, theCriterioBusqueda):
        if not theCriterioBusqueda:
            return False     
            
        return len( set( theCriterioBusqueda.keys()) - set( cClavesBusquedaInformeTodasOSimbolosOEstados) - set ( cClavesAEliminarDeBusquedasParaInforme ) ) == 0


                
                                

                
                
               
              
  
                
                
    security.declarePrivate( 'pEstrategiaBusqueda_ConInforme')
    def pEstrategiaBusqueda_ConInforme( self, 
        theReport, 
        theUseCaseQueryResult, 
        theIdioma, 
        theCodigoIdioma, 
        theSearchParameters, 
        theCriterioSeleccionTraducciones, 
        theCriterioBusquedaTraducciones, 
        theCriterioFiltroTraducciones, 
        theParentExecutionRecord=None):
        """Retrieve a maximum number of TRATraduccion records starting from the supplied cursor symbol matching search criteria and including a summary.
    
        Summary includes how many TRATraduccion have each of the possible statuses, from the set of all TRATraduccion in the Language.
        If constraints have been imposed, the a summary is produced from the set of matching TRATraduccion.
        
        """

        unExecutionRecord = self.fStartExecution( 'method',  'pEstrategiaBusqueda_ConInforme', theParentExecutionRecord, False) 

 
        try:
        
            unCriterioBusqueda = cCriterioEstadoCadena.copy()
            unCriterioBusqueda.update( theCriterioSeleccionTraducciones)
            unCriterioBusqueda.update( theCriterioBusquedaTraducciones)
            unCriterioBusqueda.update( theCriterioFiltroTraducciones)
            
            if theSearchParameters.get( 'cadenasInactivas', '').strip().lower() == "on":
                unCriterioBusqueda[ 'getEstadoCadena'] = cEstadoCadenaInactiva

                      
            theReport[ 'read_permission']  = True
    
            theReport[ 'estadosIncluidos']      = unCriterioBusqueda.get( 'getEstadoTraduccion', cTodosEstados)
            
            unosCodigosIdiomasReferencia = []
            unosCodigosIdiomasReferenciaSinValidar = set( self.fIdiomasReferenciaEnSearchParameters( theSearchParameters))
            if unosCodigosIdiomasReferenciaSinValidar:
                unosIdiomasAccesibles = theUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'languages', {}).get( 'accepted_final_objects', [])
                unosCodigosIdiomasReferencia = sorted( unosCodigosIdiomasReferenciaSinValidar.intersection( set( [ unIdioma.getCodigoIdiomaEnGvSIG() for unIdioma in unosIdiomasAccesibles])))
            
            unNumIdiomasReferenciaSinIdiomaCursor = len( unosCodigosIdiomasReferencia)
            if theCodigoIdioma in unosCodigosIdiomasReferencia:
                unNumIdiomasReferenciaSinIdiomaCursor -= 1
                
            theReport[ 'traduccionesPorPagina'] = str( self.fTraduccionesPorPagina( theSearchParameters, unNumIdiomasReferenciaSinIdiomaCursor)) 
             
            unInformeEstadosTodas = self.fInformeEstadosTodas( 
                theIdioma, 
                theCodigoIdioma, 
                theSearchParameters,
                theParentExecutionRecord=unExecutionRecord
            )
            theReport[ 'informeEstadosTodasCadenas'] = unInformeEstadosTodas
  
              
            unInformeEstadosFiltrados  = unInformeEstadosTodas.copy()
            theReport[ 'informeEstadosFiltrados']    = unInformeEstadosFiltrados
            
            if theCriterioSeleccionTraducciones.get( 'getSimbolo', None) == []: 
                # force empty results on account of module name or text search
                return theReport
            
 
            unRecuperandoEnPrimerPasoSoloInformacionDeBusqueda = True
           
            if self.fEsBusquedaTodas( unCriterioBusqueda):
                unRecuperandoEnPrimerPasoSoloInformacionDeBusqueda = True
            else:
                if self.fEsBusquedaTodasOSimbolos( unCriterioBusqueda):
                    
                    unRecuperandoEnPrimerPasoSoloInformacionDeBusqueda = True
                    unCriterioBusquedaSoloPorSimbolos = {}
                    unCriterioBusquedaSoloPorSimbolos.update( theCriterioSeleccionTraducciones)
                    
                    unInformeEstadosFiltrados  = self.fInformeEstadosRestringiendoSoloPorSimbolos( 
                        theIdioma, 
                        theCodigoIdioma, 
                        unCriterioBusqueda, 
                        theParentExecutionRecord=unExecutionRecord
                    )
                    theReport[ 'informeEstadosFiltrados']    = unInformeEstadosFiltrados
                    
                elif self.fEsBusquedaTodasOSimbolosOEstados( unCriterioBusqueda):
                    
                    unRecuperandoEnPrimerPasoSoloInformacionDeBusqueda = True
                    unInformeEstadosFiltrados  = self.fInformeEstadosRestringiendoSoloPorSimbolosYEstados( 
                        theIdioma, 
                        theCodigoIdioma, 
                        unCriterioBusqueda, 
                        theParentExecutionRecord=unExecutionRecord
                    )
                    theReport[ 'informeEstadosFiltrados']    = unInformeEstadosFiltrados

                else:
                    unRecuperandoEnPrimerPasoSoloInformacionDeBusqueda = False
                    unInformeEstadosFiltrados  = self.fInformeEstadosFiltrados( 
                        theIdioma, 
                        theCodigoIdioma, 
                        unCriterioBusqueda, 
                        theParentExecutionRecord=unExecutionRecord
                    )
                    theReport[ 'informeEstadosFiltrados']    = unInformeEstadosFiltrados
                    
                    
            if unInformeEstadosTodas[ 'Total'][ 1]:        
                unInformeEstadosFiltrados[ 'Total'][ 2] = int( floor( 100 * unInformeEstadosFiltrados[ 'Total'][ 1] / unInformeEstadosTodas[ 'Total'][ 1] ))
            else:
                unInformeEstadosTodas[ 'Total'][ 2] = 100                
    
            unDictTraduccionesEncontradas = { }
            
            for unEstado in cTodosEstados:
                unosResultadosEnUnEstado = theReport[ 'informeEstadosFiltrados'][ unEstado][ 3]
                unDictTraduccionesEncontradas.update( 
                    self.fBuildDictBySimboloFromSearchResults( 
                        unosResultadosEnUnEstado, 
                        theParentExecutionRecord=unExecutionRecord
                ))
                 
            if len( unDictTraduccionesEncontradas) > 0:  
                
                
                self.pAplicarDesplazamientoYPaginado( 
                    theSearchParameters, 
                    theReport, 
                    unDictTraduccionesEncontradas, 
                    theParentExecutionRecord=unExecutionRecord
                )    
                
                if unRecuperandoEnPrimerPasoSoloInformacionDeBusqueda:
                    self.pIncluirIdiomaBaseEIdiomasReferencia( 
                        theIdioma               = theIdioma, 
                        theUseCaseQueryResult   = theUseCaseQueryResult, 
                        theSearchParameters     = theSearchParameters, 
                        theReport               = theReport, 
                        theParentExecutionRecord=unExecutionRecord
                    )
                else: 
                    self.pIncluirIdiomasReferencia(            
                        theUseCaseQueryResult       = theUseCaseQueryResult, 
                        theSearchParameters         = theSearchParameters, 
                        theReport                   = theReport, 
                        theParentExecutionRecord    =unExecutionRecord
                    )
           
            return theReport
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
 
                
                
          
  
                
                
                
 

    security.declarePrivate( 'fBuildDictBySimboloFromSearchResults')
    def fBuildDictBySimboloFromSearchResults( self, theSearchResults, theParentExecutionRecord=None):
        """Prepare the records found matching the search criteria to be looked-up by the ordered pagination algorithm.
        
        If the records have not been already traversed, they will be traversed here, 
        which is often the most time consuming task in consulting a catalog index,
        when reading for first time immediately after a write operation.
        
        """

        unExecutionRecord = self.fStartExecution( 'method',  'fBuildDictBySimboloFromSearchResults', theParentExecutionRecord, False) 

 
        unDictTraduccionesEncontradas = {}
        try:
            if not theSearchResults:
                return {}
    
            for unosDatosTraduccion in  theSearchResults:
                unDictTraduccionesEncontradas[ unosDatosTraduccion[ 'getSimbolo']] = unosDatosTraduccion
                
            return unDictTraduccionesEncontradas
       
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()


               
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
  
            
    
    # ##############################################################################
    """The methods below pursue the ellaboration of the summary report.
    
    """
            
            

                
    security.declarePrivate( 'fInformeEstadosTodas')
    def fInformeEstadosTodas( self, theIdioma, theCodigoIdioma, theSearchParameters, theParentExecutionRecord=None):
        """Generate a Summary status report of ALL translations into the language.
        
        """

        unExecutionRecord = self.fStartExecution( 'method',  'fInformeEstadosTodas', theParentExecutionRecord, False) 

        
        try:
        
            unInformeEstados = self.fNewVoidInformeEstadosVacio()
            if not theCodigoIdioma:
                return unInformeEstados        
            
            unCriterioBusqueda = cCriterioBusquedaTodas.copy()
            
            if theSearchParameters.get( 'cadenasInactivas', '').strip().lower() == "on":
                unCriterioBusqueda[ 'getEstadoCadena'] = cEstadoCadenaInactiva

                    
            unTotalTraducciones = 0
            for unEstado in cTodosEstados:
                unCriterioBusquedaEstado = unCriterioBusqueda.copy()
                unCriterioBusquedaEstado[ 'getEstadoTraduccion'] = unEstado
        
                unosDatosTraducciones =self.fBuscarTraduccionesEnCatalogoMinimo( 
                    theIdioma, 
                    theCodigoIdioma, 
                    unCriterioBusquedaEstado, 
                    theParentExecutionRecord=unExecutionRecord
                )    
                unNumeroResultados = len( unosDatosTraducciones)
                
                unInformeEstados[ unEstado][ 1] = unNumeroResultados
                unInformeEstados[ unEstado][ 2] = None
                unInformeEstados[ unEstado][ 3] = unosDatosTraducciones
                unTotalTraducciones += unNumeroResultados
       
            unInformeEstados[ 'Total'][ 1] = unTotalTraducciones
            unInformeEstados[ 'Total'][ 2] = 100
            
            self.pCalcularPorcentajes( unInformeEstados)
                                
            return unInformeEstados

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

            
            
            
            
            
            

                

    security.declarePrivate( 'fInformeEstadosRestringiendoSoloPorSimbolos')
    def fInformeEstadosRestringiendoSoloPorSimbolos( self, theIdioma, theCodigoIdioma, theCriterioBusqueda, theParentExecutionRecord=None):
        """Generate a Summary status report of SOME translations into the language as selected just by their TRACadena symbol (simboloCadena).
        
        For example, by selecting only a few modules to be included
        in which case the list of symbols is obtained from 
        the sorted list of TRACAdena symbols of each module
        cached in the root TRACatalogo instance
       
        Pre-selection of candidate symbols also happen
        when searching by words conained in the text TRACadena symbol
        or the TRATraduccion translation
    
        """

        unExecutionRecord = self.fStartExecution( 'method',  'fInformeEstadosRestringiendoSoloPorSimbolos', theParentExecutionRecord, False) 
        
        try:
        
            unInformeEstados = self.fNewVoidInformeEstadosVacio()
            if not theCodigoIdioma:
                return unInformeEstados        
            
            unCriterioBusqueda = self.fBusquedaInformeSinFiltrar( theCriterioBusqueda)
                    
            unTotalTraducciones = 0
            for unEstado in cTodosEstados:
                unCriterioBusquedaEstado = unCriterioBusqueda.copy()
                unCriterioBusquedaEstado[ 'getEstadoTraduccion'] = unEstado
        
                unosDatosTraducciones =self.fBuscarTraduccionesEnCatalogoMinimo( 
                    theIdioma, 
                    theCodigoIdioma, 
                    unCriterioBusquedaEstado, 
                    theParentExecutionRecord=unExecutionRecord
                )    
                unNumeroResultados = len( unosDatosTraducciones)
                
                unInformeEstados[ unEstado][ 1] = unNumeroResultados
                unInformeEstados[ unEstado][ 2] = None
                unInformeEstados[ unEstado][ 3] = unosDatosTraducciones
                unTotalTraducciones += unNumeroResultados
       
            unInformeEstados[ 'Total'][ 1] = unTotalTraducciones
            unInformeEstados[ 'Total'][ 2] = 100
            
            self.pCalcularPorcentajes( unInformeEstados)
                                
            return unInformeEstados

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()



                
            

            
                

    security.declarePrivate( 'fInformeEstadosRestringiendoSoloPorSimbolosYEstados')
    def fInformeEstadosRestringiendoSoloPorSimbolosYEstados( self,  theIdioma, theCodigoIdioma, theCriterioBusqueda, theParentExecutionRecord=None):
        """Generate a Summary status report of SOME translations into the language as selected just by their TRACadena symbol (simboloCadena) and by the TRATRaduccion translation status.
        
        """
    
        unExecutionRecord = self.fStartExecution( 'method',  'fInformeEstadosRestringiendoSoloPorSimbolosYEstados', theParentExecutionRecord, False) 
        
        try:
        
            unInformeEstados = self.fNewVoidInformeEstadosVacio()
            if not theCodigoIdioma:
                return unInformeEstados        
            
            unCriterioBusqueda = self.fBusquedaInformeSinFiltrar( theCriterioBusqueda)
                    
            unTotalTraducciones = 0
            unosEstadosIncluidos = unCriterioBusqueda.get( 'getEstadoTraduccion', cTodosEstados)
                        
            for unEstado in cTodosEstados:
                if unEstado in unosEstadosIncluidos:
                    unCriterioBusquedaEstado = unCriterioBusqueda.copy()
                    unCriterioBusquedaEstado[ 'getEstadoTraduccion'] = unEstado
        
                    unosDatosTraducciones =self.fBuscarTraduccionesEnCatalogoMinimo( 
                        theIdioma, 
                        theCodigoIdioma, 
                        unCriterioBusquedaEstado, 
                        theParentExecutionRecord=unExecutionRecord
                    )    
                    unNumeroResultados = len( unosDatosTraducciones)
                
                    unInformeEstados[ unEstado][ 1] = unNumeroResultados
                    unInformeEstados[ unEstado][ 2] = None
                    unInformeEstados[ unEstado][ 3] = unosDatosTraducciones
        
                    unTotalTraducciones += unNumeroResultados                                
                else:
                    unInformeEstados[ unEstado][ 1] = 0
                    unInformeEstados[ unEstado][ 2] = 0
                    unInformeEstados[ unEstado][ 3] = []
       
            unInformeEstados[ 'Total'][ 1] = unTotalTraducciones
            unInformeEstados[ 'Total'][ 2] = 100
    
            self.pCalcularPorcentajes( unInformeEstados)
                             
            return unInformeEstados
    
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

                
                



            
            
            

            
    security.declarePrivate( 'fInformeEstadosFiltrados')
    def fInformeEstadosFiltrados( self,  theIdioma, theCodigoIdioma, theCriterioBusqueda, theParentExecutionRecord=None):
        """Generate aSummary status report of SOME translations into the language as selected by search over all filtering criteria.
        
        Filtering criteria include dates of translation, revision, lock, and the users that produced the change
        
        """

        unExecutionRecord = self.fStartExecution( 'method',  'fInformeEstadosFiltrados', theParentExecutionRecord, False) 
        
        try:
        
            unInformeEstados = self.fNewVoidInformeEstadosVacio()
            if not theCodigoIdioma:
                return unInformeEstados        
            
            unCriterioBusqueda = self.fBusquedaInformeFiltrando( theCriterioBusqueda)
                    
            unTotalTraducciones = 0
            unosEstadosIncluidos = unCriterioBusqueda.get( 'getEstadoTraduccion', cTodosEstados)
            
            for unEstado in cTodosEstados:
                if unEstado in unosEstadosIncluidos:
                    unCriterioBusquedaEstado = unCriterioBusqueda.copy()
                    unCriterioBusquedaEstado[ 'getEstadoTraduccion'] = unEstado
        
                    unosDatosTraducciones =self.fBuscarTraduccionesEnCatalogoConDatosDeIdioma( 
                        theIdioma, 
                        theCodigoIdioma, 
                        unCriterioBusquedaEstado, 
                        theParentExecutionRecord=unExecutionRecord,
                    )    
                    unNumeroResultados = len( unosDatosTraducciones)
                
                    unInformeEstados[ unEstado][ 1] = unNumeroResultados
                    unInformeEstados[ unEstado][ 2] = None
                    unInformeEstados[ unEstado][ 3] = unosDatosTraducciones
        
                    unTotalTraducciones += unNumeroResultados                                
                else:
                    unInformeEstados[ unEstado][ 1] = 0
                    unInformeEstados[ unEstado][ 2] = 0
                    unInformeEstados[ unEstado][ 3] = []
       
            unInformeEstados[ 'Total'][ 1] = unTotalTraducciones
            unInformeEstados[ 'Total'][ 2] = 100
    
            self.pCalcularPorcentajes( unInformeEstados)
                             
            return unInformeEstados
    
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()



       
            
 
  

    
    security.declarePrivate( 'fBusquedaInformeSinFiltrar')
    def fBusquedaInformeSinFiltrar( self, theCriterioBusqueda):
        """Assemble a catalog search criteria for the summary report when the supplied parameters only constrain identifying and status information.
        
        """
        
        if not theCriterioBusqueda:
            return True
                
        unaBusqueda = {}
        for unaKey in cClavesBusquedaInformeTodasOSimbolosOEstados:
            if theCriterioBusqueda.has_key( unaKey):
                unaBusqueda[ unaKey] = theCriterioBusqueda[ unaKey]
            
        return unaBusqueda
        
    
    
  
   
    
    security.declarePrivate( 'fBusquedaInformeFiltrando')
    def fBusquedaInformeFiltrando( self, theCriterioBusqueda):
        """Assemble a catalog search criteria for the summary report when the supplied parameters constrain by filtering on various  TRATraduccion attributes.
        
        """
        
        if not theCriterioBusqueda:
            return True
                
        unaBusqueda = theCriterioBusqueda.copy() 
    
        for unaKey in cClavesAEliminarDeBusquedasParaInforme:
            if unaBusqueda.has_key( unaKey):
                del unaBusqueda[ unaKey]
            
        return unaBusqueda
        

            

    
    
    

    security.declarePrivate( 'pCalcularPorcentajes')
    def pCalcularPorcentajes( self, theInformeEstados):
        """Calculate percentages in Summary reports of records found in each translation status.
        
        After fractional calculations, try to round-up the smallest non-zero percentages to make the total a 100%
        """
        
        if not theInformeEstados:
            return
            
        unosInformesEstado  = theInformeEstados.values()
        unTotalTraducciones = theInformeEstados[ 'Total'][ 1]
        
        if unTotalTraducciones == 0:
            for unInformeEstado in unosInformesEstado:
                unInformeEstado[ 2] = 0    
            return self
            
                    
        unTotalPorcentajes = 0
        for unInformeEstado in unosInformesEstado:
            if not unInformeEstado[ 0] == 'Total':
                if unTotalTraducciones:
                    unPorcentaje = int( floor( 100 * unInformeEstado[ 1] / unTotalTraducciones))
                else:
                    unPorcentaje = 100
                unInformeEstado[ 2] = unPorcentaje
                unTotalPorcentajes += unPorcentaje

            
        if unTotalPorcentajes == 100:
            return self            
            
        unosInformesExceptoTotal = [ unInformeEstado for unInformeEstado in unosInformesEstado if not ( unInformeEstado[ 0] == 'Total') ]
        
        aDifference = 100 - unTotalPorcentajes
        if aDifference > 0:
            someInformesEstadoCasiUnoPorCiento = [ unInformeEstado for unInformeEstado in unosInformesExceptoTotal if unInformeEstado[ 1] > 0 and unInformeEstado[ 2] < 1 ]
       
            for unInformeEstado in someInformesEstadoCasiUnoPorCiento:
                if aDifference > 0:
                    unInformeEstado[ 2] = 1
                    aDifference -= 1   
        
            if aDifference > 0:
                someSortedInformesEstado = sorted( unosInformesExceptoTotal, cmp=lambda unInformeEstado, otroInformeEstado: cmp(  unInformeEstado[ 1], otroInformeEstado[ 1]), reverse=True)
                for unInformeEstado in someSortedInformesEstado:
                    unInformeEstado[ 2] += 1
                    aDifference -= 1   
                    if aDifference == 0:
                        break       
                    
        return self
                    
            
            
            
    
    
    
    
    
    
    
            
            
            
            
            
            
    # ##############################################################################
    """The methods below pursue the actual searching for TRATraduccion in the indexed catalogs.
    
        parms: 
        theCriterioBusqueda constraining the set of TRATraducion.
        theIdioma, theCodigoIdioma (of theIdioma) to select the ZCatalog appropriate for theTRAidioma.
    """

    
    
    

    security.declarePrivate( 'fBuscarTraduccionesEnCatalogoMinimo')
    def fBuscarTraduccionesEnCatalogoMinimo( self, theIdioma, theCodigoIdioma, theCriterioBusqueda, theParentExecutionRecord=None):
        """Search in the fastest ZCatalog by identifier or status, retrieving just identifiers and status information for the TRATRaduccion found.
    
        parms: 
        theCriterioBusqueda constraining the set of TRATraducion.
        theIdioma, theCodigoIdioma (of theIdioma) to select the ZCatalog appropriate for theTRAidioma.

        """

        unExecutionRecord = self.fStartExecution( 'method',  'fBuscarTraduccionesEnCatalogoMinimo', theParentExecutionRecord, False) 
        
        try:
            if not theIdioma:
                return []
    
            unCatalog = self.getCatalogo().fCatalogBusquedaTraduccionesParaIdioma( theIdioma)
            if ( unCatalog == None):
                return []
            unosDatosTraducciones = unCatalog.searchResults( **theCriterioBusqueda)                
              
            return unosDatosTraducciones

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
 



  
                
    security.declarePrivate( 'fBuscarTraduccionesEnCatalogoConDatosDeIdioma')
    def fBuscarTraduccionesEnCatalogoConDatosDeIdioma( self, 
        theIdioma, 
        theCodigoIdioma, 
        theCriterioBusqueda, 
        theParentExecutionRecord=None):
        """Search in the  catalog allowing filtering, and retrieving most of the interesting information of TRATraduccion instances.
        
        parms: 
        theCriterioBusqueda constraining the set of TRATraducion.
        theIdioma, theCodigoIdioma (of theIdioma) to select the ZCatalog appropriate for theTRAidioma.
        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fBuscarTraduccionesEnCatalogoConDatosDeIdioma', theParentExecutionRecord, False) 
        
        try:
            if not theIdioma:
                return []
 
            unCatalog = self.getCatalogo().fCatalogFiltroTraduccionesParaIdioma( theIdioma)
            if ( unCatalog == None):
                return []
            unosDatosTraducciones = unCatalog.searchResults( **theCriterioBusqueda)                
              
            return unosDatosTraducciones

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
        
                
                
                
            
            
   
                
    security.declarePrivate( 'fBuscarSimbolosCadenasEnCatalogoTexto')
    def fBuscarSimbolosCadenasEnCatalogoTexto( self, 
        theTextoEnSimbolo, 
        theParentExecutionRecord=None):
        """Search in the catalog indexing as text the words in the TRACadena symbol.
        
        parms: 
        theCriterioBusqueda constraining the set of TRATraducion.
        theIdioma, theCodigoIdioma (of theIdioma) to select the ZCatalog appropriate for theTRAidioma.

        The identifiers obtained here will be used later
        to restrict the records retrieved 
        i.e., by looking up or filtering only TRATRaduccion with
        these ids in the data-rich catalog indexes
        
        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fBuscarSimbolosCadenasEnCatalogoTexto', theParentExecutionRecord, False) 
        
        try:
            if not theTextoEnSimbolo:
                return []
            unTextoABuscar = theTextoEnSimbolo.strip()
            if not unTextoABuscar:
                return []
            
            unCatalog = self.getCatalogo().fCatalogTextoCadenas()
            if ( unCatalog == None):
                return []
            unaBusqueda = { 'getSimboloEnPalabras': unTextoABuscar, }
            unosDatosTraducciones = []
            try:
                unosDatosTraducciones = unCatalog.searchResults( **unaBusqueda)   
            except:
                None
            
            unosSimbolos = []
            if unosDatosTraducciones:
                unosSimbolos = [ unResultado[ 'getSimbolo'] for unResultado in unosDatosTraducciones]
              
            return unosSimbolos

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
        
                
                
                
                

                
                
    security.declarePrivate( 'fBuscarSimbolosTraducionesEnCatalogoTextoParaIdioma')
    def fBuscarSimbolosTraducionesEnCatalogoTextoParaIdioma( self, 
        theIdioma, 
        theCodigoIdioma, 
        theTextoEnCadenaTraducida, 
        theParentExecutionRecord=None):
        """Search in the catalog indexing words in the TRATraduccion translation text.
         
        parms: 
        theCriterioBusqueda constraining the set of TRATraducion.
        theIdioma, theCodigoIdioma (of theIdioma) to select the ZCatalog appropriate for theTRAidioma.
        
        The identifiers obtained here will be used later to restrict the records retrieved 
        i.e., by looking up or filtering only TRATRaduccion with these ids in the data-rich catalog indexes

        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fBuscarSimbolosTraducionesEnCatalogoTextoParaIdioma', theParentExecutionRecord, False) 
        
        try:
            if not theIdioma or not theTextoEnCadenaTraducida:
                return None
            unTextoABuscar = theTextoEnCadenaTraducida.strip()
            if not unTextoABuscar:
                return None
            
            unCatalog = self.getCatalogo().fCatalogTextoTraduccionesParaIdioma( theIdioma)
            if ( unCatalog == None):
                return []
            unaBusqueda = { 'getCadenaTraducida': unTextoABuscar, }
            unosDatosTraducciones = []            
            try:
                unosDatosTraducciones = unCatalog.searchResults( **unaBusqueda)  
            except:
                None
            
            unosSimbolos = []
            if unosDatosTraducciones:
                unosSimbolos = [ unResultado[ 'getSimbolo'] for unResultado in unosDatosTraducciones]
              
            return unosSimbolos

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
        
                
                
            
            
            
            
            
            
            
            
                
            
            
            
            
                 
            
    # ######################################################
    """Paginated cursor access
    
    """
            
            


    
    security.declarePrivate( 'pAplicarDesplazamientoYPaginado')
    def pAplicarDesplazamientoYPaginado( self, 
        theSearchParameters, 
        theReport, 
        theDictResultadosTraducciones, 
        theParentExecutionRecord=None):
        """Paginate a block with a maximum number of records from the matching set of TRATraduccion, counting from the one with symbol to the supplied as cursor reference, or the next mathing one.
        
        """
        
                
        unExecutionRecord = self.fStartExecution( 'method',  'pAplicarDesplazamientoYPaginado', theParentExecutionRecord, False) 
        
        try:
            if not len( theDictResultadosTraducciones):
                return self
                
            if not theSearchParameters or not theReport:
                return self
            
            unModoDesplazamiento         = theSearchParameters.get( 'modoDesplazamiento', '')                    
                
            if unModoDesplazamiento == 'First':
                return self.pAplicarDesplazamientoYPaginado_First(    theSearchParameters, theReport, theDictResultadosTraducciones, None, unExecutionRecord)
            
            if unModoDesplazamiento == 'Last':
                return self.pAplicarDesplazamientoYPaginado_Last(     theSearchParameters, theReport, theDictResultadosTraducciones, None, unExecutionRecord)
                
            if unModoDesplazamiento == 'Next':
                return self.pAplicarDesplazamientoYPaginado_Next(     theSearchParameters, theReport, theDictResultadosTraducciones, None, unExecutionRecord)
            
            if unModoDesplazamiento == 'Previous':
                return self.pAplicarDesplazamientoYPaginado_Previous( theSearchParameters, theReport, theDictResultadosTraducciones, None, unExecutionRecord)

            if unModoDesplazamiento == 'SymbolIndex':
                return self.pAplicarDesplazamientoYPaginado_SymbolIndex( theSearchParameters, theReport, theDictResultadosTraducciones, None, unExecutionRecord)
            
            if unModoDesplazamiento == 'PageIndex':
                return self.pAplicarDesplazamientoYPaginado_PageIndex( theSearchParameters, theReport, theDictResultadosTraducciones, None, unExecutionRecord)
            
            if unModoDesplazamiento == 'SymbolStartingWith':
                return self.pAplicarDesplazamientoYPaginado_SymbolStartingWith( theSearchParameters, theReport, theDictResultadosTraducciones, None, unExecutionRecord)

            return self.pAplicarDesplazamientoYPaginado_Current(      theSearchParameters, theReport, theDictResultadosTraducciones, None, unExecutionRecord)
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

            
            
            

            
            

    security.declarePrivate( 'fIndiceSimboloCadenaCursor')
    def fIndiceSimboloCadenaCursor( self, theSearchParameters, theSimboloCadena, theSimbolosCadenasOrdenados = [], theParentExecutionRecord=None):
        """Locate the current cursor refrence symbol in the sorted list of all TRACadena symbols cached in the root TRACatalog.
    
        """
        
        if not theSimboloCadena or len( theSimboloCadena) < 1:
            return -1
            
        unosSimbolosCadenasOrdenados = theSimbolosCadenasOrdenados
        if not unosSimbolosCadenasOrdenados:
            if theSearchParameters.get( 'cadenasInactivas', '').strip().lower() == "on":
                unosSimbolosCadenasOrdenados = self.fListaSimbolosCadenasInactivasOrdenados( theParentExecutionRecord)
            else:
                unosSimbolosCadenasOrdenados = self.fListaSimbolosCadenasOrdenados( theParentExecutionRecord)
        
        unNumeroSimbolos = len( unosSimbolosCadenasOrdenados)
        
        unPrimerIndex = 0
        unUltimoIndex = unNumeroSimbolos - 1
        
        while unPrimerIndex <= unUltimoIndex:
            unIndexAComparar   = int( floor( ( unPrimerIndex + unUltimoIndex) / 2))
            unSimboloAComparar = unosSimbolosCadenasOrdenados[ unIndexAComparar]
        
            if theSimboloCadena == unSimboloAComparar:
                return unIndexAComparar
            
            if theSimboloCadena < unSimboloAComparar:
                unUltimoIndex = unIndexAComparar - 1
            else:
                unPrimerIndex = unIndexAComparar + 1
       
        return -1       
        
            
    

    

     
    security.declarePrivate( 'fTraduccionesPorPagina')
    def fTraduccionesPorPagina( self, theSearchParameters, theNumeroIdiomasReferencia=0):
        """Extract from parameters the umber of translations in the main language to return to the requester, 
        and calculate the actual number to retrieve
        such that product of multiplying it by the number of reference languages plus one
        does not exceed the configured maximum number of records to retrieve.
        
        """
        
        aTraduccionesPorPagina = -1
        try:
            aTraduccionesPorPagina = int(  theSearchParameters.get( 'traduccionesPorPagina', self.fTraduccionesPorPaginaPorDefecto())) 
        except:
            None
        if aTraduccionesPorPagina <= 0:
            aTraduccionesPorPagina = self.fTraduccionesPorPaginaPorDefecto()
            
        unMaximoRegistrosExplorados = self.fMaximoRegistrosExplorados()
        if not theNumeroIdiomasReferencia:
            return min( aTraduccionesPorPagina, unMaximoRegistrosExplorados)
        
        if ( aTraduccionesPorPagina * ( theNumeroIdiomasReferencia + 1)) > unMaximoRegistrosExplorados:
            aTraduccionesPorPagina = int( unMaximoRegistrosExplorados / ( 1 + theNumeroIdiomasReferencia))
            
        return aTraduccionesPorPagina
    

    

         
                        

   
    # ######################################################
    """Significant combinations of cases for pagination in blocks:
    One or many records requested
    First or last block, 
    Previous, Current or Next Block
    
    """
            
            
    
    
        
    security.declarePrivate( 'pAplicarDesplazamientoYPaginado_Current')
    def pAplicarDesplazamientoYPaginado_Current( self, theSearchParameters, theReport, theDictResultadosTraducciones, theSimbolosCadenasOrdenados=None, theParentExecutionRecord=None):
        """One of the cases to paginate a block with a maximum number of records from the matching set of TRATraduccion, counting from the one with symbol to the supplied as cursor reference, or the next mathing one.
        
        """
           
        if not len( theDictResultadosTraducciones):
            return self

        aTraduccionesPorPagina        = self.fTraduccionesPorPagina( theSearchParameters)
        if ( not aTraduccionesPorPagina) or ( aTraduccionesPorPagina <= 0):
            return self
        
        aSimboloCadenaCursor         = theSearchParameters.get( 'simboloCadenaCursor', '')
                
        if aSimboloCadenaCursor:
            
            unosSimbolosCadenasOrdenados = theSimbolosCadenasOrdenados
            if not unosSimbolosCadenasOrdenados:                
                if theSearchParameters.get( 'cadenasInactivas', '').strip().lower() == "on":
                    unosSimbolosCadenasOrdenados = self.fListaSimbolosCadenasInactivasOrdenados( theParentExecutionRecord)
                else:
                    unosSimbolosCadenasOrdenados = self.fListaSimbolosCadenasOrdenados(          theParentExecutionRecord)
    
            unIndiceSimboloCadenaCursor  = self.fIndiceSimboloCadenaCursor( theSearchParameters, aSimboloCadenaCursor, unosSimbolosCadenasOrdenados, theParentExecutionRecord)
            if unIndiceSimboloCadenaCursor >= 0:
            
                        
                unNumeroSimbolos       = len( unosSimbolosCadenasOrdenados) 
        
                unIndiceSimbolosCadena      = unIndiceSimboloCadenaCursor
                unosDatosTraduccionEncontrada = None
                while unIndiceSimbolosCadena < unNumeroSimbolos:
                    unSimboloCadena         = unosSimbolosCadenasOrdenados[ unIndiceSimbolosCadena]
                    unosDatosTraduccion     = theDictResultadosTraducciones.get( unSimboloCadena, None)
                    unIndiceSimbolosCadena  += 1
                    if unosDatosTraduccion:
                        unosDatosTraduccionEncontrada = unosDatosTraduccion 
                        break    
                    
                if unosDatosTraduccionEncontrada:
                    
                    unaPaginaDatosTraducciones = [ unosDatosTraduccionEncontrada]

                    unIndicePrimeraCadena = unIndiceSimbolosCadena
                    
                    unNumeroSimbolosAnteriores = 0
                    for unIndiceSimboloAnterior in range( unIndicePrimeraCadena):
                        if theDictResultadosTraducciones.get( unosSimbolosCadenasOrdenados[ unIndiceSimboloAnterior], None):
                            unNumeroSimbolosAnteriores += 1
                             
                    while ( unIndiceSimbolosCadena < unNumeroSimbolos) and len( unaPaginaDatosTraducciones) < aTraduccionesPorPagina:
                        unSimboloCadena = unosSimbolosCadenasOrdenados[ unIndiceSimbolosCadena]
                        unosDatosTraduccion = theDictResultadosTraducciones.get( unSimboloCadena, None)
                        unIndiceSimbolosCadena += 1
                        if unosDatosTraduccion:
                            unaPaginaDatosTraducciones.append( unosDatosTraduccion)  
                        
                    theReport[ 'datosTraducciones'] = unaPaginaDatosTraducciones
                    
                    theReport[ 'from_translation_index']    = unNumeroSimbolosAnteriores
                    theReport[ 'to_translation_index']      = unNumeroSimbolosAnteriores + len( unaPaginaDatosTraducciones) - 1
                    theReport[ 'total_translations']        = len( theDictResultadosTraducciones)
                    
                    return self                
            
        return self.pAplicarDesplazamientoYPaginado_First( theSearchParameters, theReport, theDictResultadosTraducciones, theSimbolosCadenasOrdenados, theParentExecutionRecord)
                    
        
    
    
    
    
   
    
    
    
    
       
    security.declarePrivate( 'pAplicarDesplazamientoYPaginado_First')
    def pAplicarDesplazamientoYPaginado_First( self, theSearchParameters, theReport, theDictResultadosTraducciones, theSimbolosCadenasOrdenados=None, theParentExecutionRecord=None):
        """One of the cases to paginate a block with a maximum number of records from the matching set of TRATraduccion, counting from the one with symbol to the supplied as cursor reference, or the next mathing one.
        
        """
           
        if not len( theDictResultadosTraducciones):
            return self

        aTraduccionesPorPagina        = self.fTraduccionesPorPagina( theSearchParameters)
        if ( not aTraduccionesPorPagina) or ( aTraduccionesPorPagina <= 0):
            return self
        
        unosSimbolosCadenasOrdenados = theSimbolosCadenasOrdenados
        if not unosSimbolosCadenasOrdenados:
            if theSearchParameters.get( 'cadenasInactivas', '').strip().lower() == "on":
                unosSimbolosCadenasOrdenados = self.fListaSimbolosCadenasInactivasOrdenados( theParentExecutionRecord)
            else:
                unosSimbolosCadenasOrdenados = self.fListaSimbolosCadenasOrdenados(          theParentExecutionRecord)
            
            
    
        unNumeroSimbolos              = len( unosSimbolosCadenasOrdenados) 
    
        unaPaginaDatosTraducciones = []
         
        unIndiceSimbolosCadena = 0
        while ( unIndiceSimbolosCadena < unNumeroSimbolos) and ( len( unaPaginaDatosTraducciones) < aTraduccionesPorPagina):
            unSimboloCadena = unosSimbolosCadenasOrdenados[ unIndiceSimbolosCadena]
            unIndiceSimbolosCadena += 1
            unosDatosTraduccion = theDictResultadosTraducciones.get( unSimboloCadena, None)
            if unosDatosTraduccion:
                unaPaginaDatosTraducciones.append( unosDatosTraduccion)  
       
                 
        theReport[ 'datosTraducciones']         = unaPaginaDatosTraducciones
        theReport[ 'from_translation_index']    = 1
        theReport[ 'to_translation_index']      = len( unaPaginaDatosTraducciones)
        theReport[ 'total_translations']        = len( theDictResultadosTraducciones)
        
        return self
                
       

    
  
        
 
    
        
    
    
    security.declarePrivate( 'pAplicarDesplazamientoYPaginado_Last')
    def pAplicarDesplazamientoYPaginado_Last( self, theSearchParameters, theReport, theDictResultadosTraducciones, theSimbolosCadenasOrdenados=None, theParentExecutionRecord=None):
        """One of the cases to paginate a block with a maximum number of records from the matching set of TRATraduccion, counting from the one with symbol to the supplied as cursor reference, or the next mathing one.
        
        """
           
        if not len( theDictResultadosTraducciones):
            return self

        aTraduccionesPorPagina        = self.fTraduccionesPorPagina( theSearchParameters)
        if ( not aTraduccionesPorPagina) or ( aTraduccionesPorPagina <= 0):
            return self
    
        unosSimbolosCadenasOrdenados = theSimbolosCadenasOrdenados
        if not unosSimbolosCadenasOrdenados:
            if theSearchParameters.get( 'cadenasInactivas', '').strip().lower() == "on":
                unosSimbolosCadenasOrdenados = self.fListaSimbolosCadenasInactivasOrdenados( theParentExecutionRecord)
            else:
                unosSimbolosCadenasOrdenados = self.fListaSimbolosCadenasOrdenados(          theParentExecutionRecord)
    
        unNumeroSimbolos              = len( unosSimbolosCadenasOrdenados) 
    
        unaPaginaDatosTraducciones = []
    
        unIndicePrimeraCadena = -1
        unIndiceSimbolosCadena = unNumeroSimbolos - 1
        while ( unIndiceSimbolosCadena >= 0) and ( len( unaPaginaDatosTraducciones) < aTraduccionesPorPagina):
            unSimboloCadena = unosSimbolosCadenasOrdenados[ unIndiceSimbolosCadena]
            unIndiceSimbolosCadena -= 1
            unosDatosTraduccion = theDictResultadosTraducciones.get( unSimboloCadena, None)
            if unosDatosTraduccion:
                unIndicePrimeraCadena = unIndiceSimbolosCadena + 1
                unaPaginaDatosTraducciones.append( unosDatosTraduccion) 
            
                
        unNumeroSimbolosAnteriores = 0
        for unIndiceSimboloAnterior in range( unIndicePrimeraCadena):
            if theDictResultadosTraducciones.get( unosSimbolosCadenasOrdenados[ unIndiceSimboloAnterior], None):
                unNumeroSimbolosAnteriores += 1
                
        unaPaginaDatosTraducciones.reverse()        
        theReport[ 'datosTraducciones'] = unaPaginaDatosTraducciones
        
        theReport[ 'from_translation_index']    = unNumeroSimbolosAnteriores + 1
        theReport[ 'to_translation_index']      = unNumeroSimbolosAnteriores + len( unaPaginaDatosTraducciones) 
        theReport[ 'total_translations']        = len( theDictResultadosTraducciones)
        
        return self
        
    
      
 
    

    
    
   
       
    security.declarePrivate( 'pAplicarDesplazamientoYPaginado_Next')
    def pAplicarDesplazamientoYPaginado_Next( self, theSearchParameters, theReport, theDictResultadosTraducciones, theSimbolosCadenasOrdenados=None, theParentExecutionRecord=None):
        """One of the cases to paginate a block with a maximum number of records from the matching set of TRATraduccion, counting from the one with symbol to the supplied as cursor reference, or the next mathing one.
        
        """
           
        if not len( theDictResultadosTraducciones):
            return self

        aTraduccionesPorPagina        = self.fTraduccionesPorPagina( theSearchParameters)
        if ( not aTraduccionesPorPagina) or ( aTraduccionesPorPagina <= 0):
            return self
    
        aSimboloCadenaCursor         = theSearchParameters.get( 'simboloCadenaCursor', '')
                
        if aSimboloCadenaCursor:
            
            unosSimbolosCadenasOrdenados = theSimbolosCadenasOrdenados
            if not unosSimbolosCadenasOrdenados:
                if theSearchParameters.get( 'cadenasInactivas', '').strip().lower() == "on":
                    unosSimbolosCadenasOrdenados = self.fListaSimbolosCadenasInactivasOrdenados( theParentExecutionRecord)
                else:
                    unosSimbolosCadenasOrdenados = self.fListaSimbolosCadenasOrdenados(          theParentExecutionRecord)

    
            unIndiceSimboloCadenaCursor  = self.fIndiceSimboloCadenaCursor( theSearchParameters, aSimboloCadenaCursor, unosSimbolosCadenasOrdenados, theParentExecutionRecord)
            if unIndiceSimboloCadenaCursor >= 0:
            
                unNumeroSimbolos       = len( unosSimbolosCadenasOrdenados) 
            
                # no skipping a whole page: symbol supplied is suposed to be the last of the current page
                unIndiceSimbolosCadena      = unIndiceSimboloCadenaCursor + 1
                unosDatosTraduccionEncontrada = None
                while unIndiceSimbolosCadena < unNumeroSimbolos:
                    unSimboloCadena         = unosSimbolosCadenasOrdenados[ unIndiceSimbolosCadena]
                    unosDatosTraduccion     = theDictResultadosTraducciones.get( unSimboloCadena, None)
                    unIndiceSimbolosCadena  += 1
                    if unosDatosTraduccion:
                        unosDatosTraduccionEncontrada = unosDatosTraduccion 
                        break    
        
                if unosDatosTraduccionEncontrada:
                    unIndicePrimeraCadena = unIndiceSimbolosCadena
                    
                    unNumeroSimbolosAnteriores = 0
                    for unIndiceSimboloAnterior in range( unIndicePrimeraCadena):
                        if theDictResultadosTraducciones.get( unosSimbolosCadenasOrdenados[ unIndiceSimboloAnterior], None):
                            unNumeroSimbolosAnteriores += 1
                    
         
                    unaPaginaDatosTraducciones = [ unosDatosTraduccionEncontrada]
        
                    while ( unIndiceSimbolosCadena < unNumeroSimbolos) and ( len( unaPaginaDatosTraducciones) < aTraduccionesPorPagina):
                        unSimboloCadena = unosSimbolosCadenasOrdenados[ unIndiceSimbolosCadena]
                        unosDatosTraduccion = theDictResultadosTraducciones.get( unSimboloCadena, None)
                        unIndiceSimbolosCadena += 1
                        if unosDatosTraduccion:
                            unaPaginaDatosTraducciones.append( unosDatosTraduccion)  
                        
                    theReport[ 'datosTraducciones'] = unaPaginaDatosTraducciones
                    
                    theReport[ 'from_translation_index']    = unNumeroSimbolosAnteriores
                    theReport[ 'to_translation_index']      = unNumeroSimbolosAnteriores + len( unaPaginaDatosTraducciones) - 1
                    theReport[ 'total_translations']        = len( theDictResultadosTraducciones)
                    
                    return self                
            
        self.pAplicarDesplazamientoYPaginado_First( theSearchParameters, theReport, theDictResultadosTraducciones, theSimbolosCadenasOrdenados, theParentExecutionRecord)
        
        return self
       
    

    
    
    security.declarePrivate( 'pAplicarDesplazamientoYPaginado_Previous')
    def pAplicarDesplazamientoYPaginado_Previous( self, theSearchParameters, theReport, theDictResultadosTraducciones, theSimbolosCadenasOrdenados=None, theParentExecutionRecord=None):
        """One of the cases to paginate a block with a maximum number of records from the matching set of TRATraduccion, counting from the one with symbol to the supplied as cursor reference, or the next mathing one.
        
        """
           
        if not len( theDictResultadosTraducciones):
            return self

        aTraduccionesPorPagina        = self.fTraduccionesPorPagina( theSearchParameters)
        if ( not aTraduccionesPorPagina) or ( aTraduccionesPorPagina <= 0):
            return self
     
        aSimboloCadenaCursor         = theSearchParameters.get( 'simboloCadenaCursor', '')
                
        if aSimboloCadenaCursor:
            
            unosSimbolosCadenasOrdenados = theSimbolosCadenasOrdenados
            if not unosSimbolosCadenasOrdenados:
                if theSearchParameters.get( 'cadenasInactivas', '').strip().lower() == "on":
                    unosSimbolosCadenasOrdenados = self.fListaSimbolosCadenasInactivasOrdenados( theParentExecutionRecord)
                else:
                    unosSimbolosCadenasOrdenados = self.fListaSimbolosCadenasOrdenados(          theParentExecutionRecord)
    
            unIndiceSimboloCadenaCursor  = self.fIndiceSimboloCadenaCursor( theSearchParameters, aSimboloCadenaCursor, unosSimbolosCadenasOrdenados, theParentExecutionRecord)
            if unIndiceSimboloCadenaCursor >= 0:
            
                unNumeroSimbolos       = len( unosSimbolosCadenasOrdenados) 
 
                unIndiceSimbolosCadena      = unIndiceSimboloCadenaCursor - 1
                
                unIndicePrimeraCadena = -1
                unaPaginaDatosTraducciones = []
                while ( unIndiceSimbolosCadena >= 0) and ( len( unaPaginaDatosTraducciones) < aTraduccionesPorPagina):
                    unSimboloCadena     = unosSimbolosCadenasOrdenados[ unIndiceSimbolosCadena]
                    unosDatosTraduccion     = theDictResultadosTraducciones.get( unSimboloCadena, None)
                    unIndiceSimbolosCadena  -= 1
                    if unosDatosTraduccion:
                        unaPaginaDatosTraducciones.append( unosDatosTraduccion)
                        unIndicePrimeraCadena = unIndiceSimbolosCadena + 1
                        
                if len( unaPaginaDatosTraducciones) > 0:
                    
                    unNumeroSimbolosAnteriores = 0
                    for unIndiceSimboloAnterior in range( unIndicePrimeraCadena):
                        if theDictResultadosTraducciones.get( unosSimbolosCadenasOrdenados[ unIndiceSimboloAnterior], None):
                            unNumeroSimbolosAnteriores += 1
                    
                    unaPaginaDatosTraducciones.reverse()        
                    theReport[ 'datosTraducciones'] = unaPaginaDatosTraducciones
                    
                    theReport[ 'from_translation_index']    = unNumeroSimbolosAnteriores + 1
                    theReport[ 'to_translation_index']      = unNumeroSimbolosAnteriores + len( unaPaginaDatosTraducciones) 
                    theReport[ 'total_translations']        = len( theDictResultadosTraducciones)
                    
                    return self    
              
            
        self.pAplicarDesplazamientoYPaginado_Last( theSearchParameters, theReport, theDictResultadosTraducciones, theSimbolosCadenasOrdenados, theParentExecutionRecord)
        
        return self
      
    
    
      

    
    
       
    security.declarePrivate( 'pAplicarDesplazamientoYPaginado_SymbolIndex')
    def pAplicarDesplazamientoYPaginado_SymbolIndex( self, theSearchParameters, theReport, theDictResultadosTraducciones, theSimbolosCadenasOrdenados=None, theParentExecutionRecord=None):
        """One of the cases to paginate a block with a maximum number of records from the matching set of TRATraduccion, starting at the symbol with index specified in the symbolIndex search parameter.
        
        """
           
        if not len( theDictResultadosTraducciones):
            return self

        aTraduccionesPorPagina        = self.fTraduccionesPorPagina( theSearchParameters)
        if ( not aTraduccionesPorPagina) or ( aTraduccionesPorPagina <= 0):
            return self
        
        unosSimbolosCadenasOrdenados = theSimbolosCadenasOrdenados
        if not unosSimbolosCadenasOrdenados:
            if theSearchParameters.get( 'cadenasInactivas', '').strip().lower() == "on":
                unosSimbolosCadenasOrdenados = self.fListaSimbolosCadenasInactivasOrdenados( theParentExecutionRecord)
            else:
                unosSimbolosCadenasOrdenados = self.fListaSimbolosCadenasOrdenados(          theParentExecutionRecord)
            
        
    
        unNumeroSimbolos              = len( unosSimbolosCadenasOrdenados) 
            
        unSymbolIndex = theSearchParameters.get( 'symbolIndex', 0)
        
        if unSymbolIndex < 1:
            self.pAplicarDesplazamientoYPaginado_First( theSearchParameters, theReport, theDictResultadosTraducciones, theSimbolosCadenasOrdenados, theParentExecutionRecord)
            return self
        
        if unSymbolIndex >= unNumeroSimbolos:
            self.pAplicarDesplazamientoYPaginado_Last( theSearchParameters, theReport, theDictResultadosTraducciones, theSimbolosCadenasOrdenados, theParentExecutionRecord)
            return self
        
        unaPaginaDatosTraducciones = []
         
        unIndiceSimbolosCadena = 0
        unNumeroSimbolosSkipped = 0
        while ( unNumeroSimbolosSkipped < ( unSymbolIndex - 1) ) and ( unIndiceSimbolosCadena < unNumeroSimbolos):
            unSimboloCadena = unosSimbolosCadenasOrdenados[ unIndiceSimbolosCadena]
            unIndiceSimbolosCadena += 1
            unosDatosTraduccion = theDictResultadosTraducciones.get( unSimboloCadena, None)
            if unosDatosTraduccion:
                unNumeroSimbolosSkipped += 1  
       
        while ( unIndiceSimbolosCadena < unNumeroSimbolos) and ( len( unaPaginaDatosTraducciones) < aTraduccionesPorPagina):
            unSimboloCadena = unosSimbolosCadenasOrdenados[ unIndiceSimbolosCadena]
            unIndiceSimbolosCadena += 1
            unosDatosTraduccion = theDictResultadosTraducciones.get( unSimboloCadena, None)
            if unosDatosTraduccion:
                unaPaginaDatosTraducciones.append( unosDatosTraduccion)  
                 
        theReport[ 'datosTraducciones']         = unaPaginaDatosTraducciones
        theReport[ 'from_translation_index']    = unSymbolIndex
        theReport[ 'to_translation_index']      = unSymbolIndex + len( unaPaginaDatosTraducciones) - 1
        theReport[ 'total_translations']        = len( theDictResultadosTraducciones)
        
        return self
                
       
    
    
    
    

    
    
       
    security.declarePrivate( 'pAplicarDesplazamientoYPaginado_PageIndex')
    def pAplicarDesplazamientoYPaginado_PageIndex( self, theSearchParameters, theReport, theDictResultadosTraducciones, theSimbolosCadenasOrdenados=None, theParentExecutionRecord=None):
        """One of the cases to paginate a block with a maximum number of records from the matching set of TRATraduccion, starting at the page index specified in the pageIndex search parameter.
        
        """
           
        if not len( theDictResultadosTraducciones):
            return self

        aTraduccionesPorPagina        = self.fTraduccionesPorPagina( theSearchParameters)
        if ( not aTraduccionesPorPagina) or ( aTraduccionesPorPagina <= 0):
            return self
        
        unosSimbolosCadenasOrdenados = theSimbolosCadenasOrdenados
        if not unosSimbolosCadenasOrdenados:
            if theSearchParameters.get( 'cadenasInactivas', '').strip().lower() == "on":
                unosSimbolosCadenasOrdenados = self.fListaSimbolosCadenasInactivasOrdenados( theParentExecutionRecord)
            else:
                unosSimbolosCadenasOrdenados = self.fListaSimbolosCadenasOrdenados(          theParentExecutionRecord)
            
        
    
        unNumeroSimbolos              = len( unosSimbolosCadenasOrdenados) 
            
        unPageIndex = theSearchParameters.get( 'pageIndex', 0)
        
        if unPageIndex < 1:
            self.pAplicarDesplazamientoYPaginado_First( theSearchParameters, theReport, theDictResultadosTraducciones, theSimbolosCadenasOrdenados, theParentExecutionRecord)
            return self
        
        unSymbolIndex = (( unPageIndex - 1) * aTraduccionesPorPagina) + 1
        
        if unSymbolIndex >= unNumeroSimbolos:
            self.pAplicarDesplazamientoYPaginado_Last( theSearchParameters, theReport, theDictResultadosTraducciones, theSimbolosCadenasOrdenados, theParentExecutionRecord)
            return self
        
        unaPaginaDatosTraducciones = []
         
        unIndiceSimbolosCadena = 0
        unNumeroSimbolosSkipped = 0
        while ( unNumeroSimbolosSkipped < ( unSymbolIndex - 1) ) and ( unIndiceSimbolosCadena < unNumeroSimbolos):
            unSimboloCadena = unosSimbolosCadenasOrdenados[ unIndiceSimbolosCadena]
            unIndiceSimbolosCadena += 1
            unosDatosTraduccion = theDictResultadosTraducciones.get( unSimboloCadena, None)
            if unosDatosTraduccion:
                unNumeroSimbolosSkipped += 1  
       
        while ( unIndiceSimbolosCadena < unNumeroSimbolos) and ( len( unaPaginaDatosTraducciones) < aTraduccionesPorPagina):
            unSimboloCadena = unosSimbolosCadenasOrdenados[ unIndiceSimbolosCadena]
            unIndiceSimbolosCadena += 1
            unosDatosTraduccion = theDictResultadosTraducciones.get( unSimboloCadena, None)
            if unosDatosTraduccion:
                unaPaginaDatosTraducciones.append( unosDatosTraduccion)  
                 
        theReport[ 'datosTraducciones']         = unaPaginaDatosTraducciones
        theReport[ 'from_translation_index']    = unSymbolIndex
        theReport[ 'to_translation_index']      = unSymbolIndex + len( unaPaginaDatosTraducciones) - 1
        theReport[ 'total_translations']        = len( theDictResultadosTraducciones)
        
        return self
             
    
    
    
    
       
    security.declarePrivate( 'pAplicarDesplazamientoYPaginado_SymbolStartingWith')
    def pAplicarDesplazamientoYPaginado_SymbolStartingWith( self, theSearchParameters, theReport, theDictResultadosTraducciones, theSimbolosCadenasOrdenados=None, theParentExecutionRecord=None):
        """One of the cases to paginate a block with a maximum number of records from the matching set of TRATraduccion, starting at the symbol with index specified in the symbolIndex search parameter.
        
        """
           
        if not len( theDictResultadosTraducciones):
            return self

        aTraduccionesPorPagina        = self.fTraduccionesPorPagina( theSearchParameters)
        if ( not aTraduccionesPorPagina) or ( aTraduccionesPorPagina <= 0):
            return self
        
        unosSimbolosCadenasOrdenados = theSimbolosCadenasOrdenados
        if not unosSimbolosCadenasOrdenados:
            if theSearchParameters.get( 'cadenasInactivas', '').strip().lower() == "on":
                unosSimbolosCadenasOrdenados = self.fListaSimbolosCadenasInactivasOrdenados( theParentExecutionRecord)
            else:
                unosSimbolosCadenasOrdenados = self.fListaSimbolosCadenasOrdenados(          theParentExecutionRecord)
            
        
    
        unNumeroSimbolos              = len( unosSimbolosCadenasOrdenados) 
            
        unSymbolStartingWith = theSearchParameters.get( 'symbolStartingWith', 0)
        
        if not unSymbolStartingWith:
            self.pAplicarDesplazamientoYPaginado_First( theSearchParameters, theReport, theDictResultadosTraducciones, theSimbolosCadenasOrdenados, theParentExecutionRecord)
            return self
        
        
        unaPaginaDatosTraducciones = []
         
        unPreviousIndiceSimboloCadena = 0
        unIndiceSimbolosCadena = 0
        unNumSkippedSimbolos = 0
        while unIndiceSimbolosCadena < unNumeroSimbolos:
            unSimboloCadena = unosSimbolosCadenasOrdenados[ unIndiceSimbolosCadena]
            unosDatosTraduccion = theDictResultadosTraducciones.get( unSimboloCadena, None)
            if unosDatosTraduccion:
                if unSimboloCadena.startswith( unSymbolStartingWith):
                    break
                elif unSimboloCadena > unSymbolStartingWith:
                    unIndiceSimbolosCadena = unPreviousIndiceSimboloCadena
                    break
                else:
                    unNumSkippedSimbolos += 1
            unPreviousIndiceSimboloCadena = unIndiceSimbolosCadena
            unIndiceSimbolosCadena += 1
                    
                    
                
        if not unIndiceSimbolosCadena:
            self.pAplicarDesplazamientoYPaginado_First( theSearchParameters, theReport, theDictResultadosTraducciones, theSimbolosCadenasOrdenados, theParentExecutionRecord)
            return self
                
        if unIndiceSimbolosCadena >= unNumeroSimbolos:
            self.pAplicarDesplazamientoYPaginado_Last( theSearchParameters, theReport, theDictResultadosTraducciones, theSimbolosCadenasOrdenados, theParentExecutionRecord)
            return self
                
        
        while ( unIndiceSimbolosCadena < unNumeroSimbolos) and ( len( unaPaginaDatosTraducciones) < aTraduccionesPorPagina):
            unSimboloCadena = unosSimbolosCadenasOrdenados[ unIndiceSimbolosCadena]
            unIndiceSimbolosCadena += 1
            unosDatosTraduccion = theDictResultadosTraducciones.get( unSimboloCadena, None)
            if unosDatosTraduccion:
                unaPaginaDatosTraducciones.append( unosDatosTraduccion)  
                 
        theReport[ 'datosTraducciones']         = unaPaginaDatosTraducciones
        theReport[ 'from_translation_index']    = unNumSkippedSimbolos + 1
        theReport[ 'to_translation_index']      = unNumSkippedSimbolos + len( unaPaginaDatosTraducciones)
        theReport[ 'total_translations']        = len( theDictResultadosTraducciones)
        
        return self
                 
    
    
    




    # ########################################################
    """Retrieval of the TRATranslation information
    compose the final record set to be delivered to the requester
    this is the final step in the lookup, search and retrieve algorithm
    
    """

    
    
    security.declarePrivate( 'pIncluirIdiomaBaseEIdiomasReferencia')
    def pIncluirIdiomaBaseEIdiomasReferencia( self, 
        theIdioma, 
        theUseCaseQueryResult, 
        theSearchParameters, 
        theReport, 
        theParentExecutionRecord=None):
        """Assemble the final result set of the block of matching TRATraduccion, including the records from the main language and all the requested reference languages.
        
        Retrieval of TRATranslation information for the
        already paginated set of maching translation ids.
       
        Retrieval of the information in the main language
        and in all selected reference languages.
       
        When previous lookup steps of the algorithm
        have searched only in the faster indexed catalogs
        that include a minimum of identifying and status information
        Then it is necessary to retrieve now the  information of the main language     
        
        """

        unExecutionRecord = self.fStartExecution( 'method',  'pIncluirIdiomaBaseEIdiomasReferencia', theParentExecutionRecord, False) 
        
        try:
        
            if not theIdioma or not theReport or not theSearchParameters or not theUseCaseQueryResult:
                return self
        
            unCodigoIdiomaBase = theSearchParameters.get( 'idioma', '')
            if not unCodigoIdiomaBase:
                return self
            
            unosDatosARetornar = theReport[ 'datosTraducciones']
            if not unosDatosARetornar:
                return self
     
            unosSimbolosARetornar = [ unosDatosTraduccion[ 'getSimbolo'] for  unosDatosTraduccion in unosDatosARetornar] 
            
            unaBusqueda = cCriterioBusqueda_RecuperarDatosTraduccionesPorSimbolos.copy()
            unaBusqueda[ 'getSimbolo'] =  unosSimbolosARetornar
            
            if theSearchParameters.get( 'cadenasInactivas', '').strip().lower() == "on":
                unaBusqueda[ 'getEstadoCadena'] = cEstadoCadenaInactiva
            
            unosDatosTraduccionesIdiomaBase = self.fBuscarTraduccionesEnCatalogoConDatosDeIdioma( 
                theIdioma, 
                unCodigoIdiomaBase, 
                unaBusqueda, 
                theParentExecutionRecord=unExecutionRecord
            )
            
            
            unDictTraduccionesIdiomaBase = { }
            for unDatosTraduccion in unosDatosTraduccionesIdiomaBase:
                unDictTraduccionesIdiomaBase[ unDatosTraduccion[ 'getSimbolo']] = unDatosTraduccion 
            unosDatosTraduccionesIdiomaBaseOrdenados = [ ]
            for unSimbolo in unosSimbolosARetornar:
                unResultado = unDictTraduccionesIdiomaBase.get( unSimbolo, None)
                if unResultado:
                    unosDatosTraduccionesIdiomaBaseOrdenados.append( unResultado)    
                
            
            theReport[ 'datosTraducciones']     = unosDatosTraduccionesIdiomaBaseOrdenados
 
            unosCodigosIdiomasReferencia = self.fIdiomasReferenciaEnSearchParameters( theSearchParameters)
            if not unosCodigosIdiomasReferencia:
                return self
            
            unosIdiomasAccesibles = theUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'languages', {}).get( 'accepted_final_objects', [])
            unosCodigosEIdiomasAccesibles = dict( [ ( unIdioma.getCodigoIdiomaEnGvSIG(), unIdioma, ) for unIdioma in unosIdiomasAccesibles])
            
            unosDictsIdiomaReferencia = {}
 
            for unCodigoIdiomaReferencia in unosCodigosIdiomasReferencia:
                if not ( unCodigoIdiomaReferencia == unCodigoIdiomaBase):
                    unIdiomaAccessible = unosCodigosEIdiomasAccesibles.get( unCodigoIdiomaReferencia, None)
                    if unIdiomaAccessible:
                        unDictTraduccionesIdiomaReferencia = { }
                        unosDictsIdiomaReferencia[ unCodigoIdiomaReferencia] = unDictTraduccionesIdiomaReferencia

                        unaBusqueda = cCriterioBusqueda_RecuperarDatosTraduccionesPorSimbolos.copy()
                        unaBusqueda[ 'getSimbolo'] =  unosSimbolosARetornar
                        
                        if theSearchParameters.get( 'cadenasInactivas', '').strip().lower() == "on":
                            unaBusqueda[ 'getEstadoCadena'] = cEstadoCadenaInactiva
                        
                        unosDatosTraducciones = self.fBuscarTraduccionesEnCatalogoConDatosDeIdioma( 
                            unIdiomaAccessible, 
                            unCodigoIdiomaReferencia, 
                            unaBusqueda, 
                            theParentExecutionRecord=unExecutionRecord
                        )
                        
                        for unDatosTraduccion in unosDatosTraducciones:
                            unDictTraduccionesIdiomaReferencia[ unDatosTraduccion[ 'getSimbolo']] = unDatosTraduccion 
                                 
            theReport[ 'dictsTraduccionesIdiomasReferencia']  = unosDictsIdiomaReferencia
            return self
 
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
      
        
    
            
            
            
            
    
    
    

    security.declarePrivate( 'pIncluirIdiomasReferencia')
    def pIncluirIdiomasReferencia( self, 
        theUseCaseQueryResult, 
        theSearchParameters, 
        theReport, 
        theParentExecutionRecord=None):
        """Assemble the final result set of the block of matching TRATraduccion, including the records from all the requested reference languages.
        
        Retrieval of TRATranslation information for the
        already paginated set of maching translation ids.
       
        Retrieval of the information in all selected reference languages.
       
        The previous lookup steps of the algorithm
        have searched in information rich indexed catalogs
        and not only in the faster indexed catalogs
        The  information of the main language has already been retrieved
        
        """

        unExecutionRecord = self.fStartExecution( 'method',  'pIncluirIdiomasReferencia', theParentExecutionRecord, False) 
        
        try:
        
            if not theReport or not theSearchParameters or not theUseCaseQueryResult:
                return self
        
            unosDatosARetornar = theReport[ 'datosTraducciones']
            if not unosDatosARetornar:
                return self
                
            unosCodigosIdiomasReferencia = self.fIdiomasReferenciaEnSearchParameters( theSearchParameters)
            if not unosCodigosIdiomasReferencia:
                return self
    
            unosSimbolosARetornar = [ unosDatosTraduccion[ 'getSimbolo'] for  unosDatosTraduccion in unosDatosARetornar] 
            
            unosIdiomasAccesibles = theUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'languages', {}).get( 'accepted_final_objects', [])
            unosCodigosEIdiomasAccesibles = dict( [ ( unIdioma.getCodigoIdiomaEnGvSIG(), unIdioma, ) for unIdioma in unosIdiomasAccesibles])
            
            unosDictsIdiomaReferencia = {}
            for unCodigoIdiomaReferencia in unosCodigosIdiomasReferencia:
                unIdiomaAccessible = unosCodigosEIdiomasAccesibles.get( unCodigoIdiomaReferencia, None)
                if unIdiomaAccessible:
                    unDictTraduccionesIdiomaReferencia = { }
                    unosDictsIdiomaReferencia[ unCodigoIdiomaReferencia] = unDictTraduccionesIdiomaReferencia
                    
                    unaBusqueda = { 
                        'getSimbolo':               unosSimbolosARetornar ,
                        'getEstadoTraduccion':      [ cEstadoTraduccionTraducida, cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva,],
                    }  
                    unosDatosTraducciones = self.fBuscarTraduccionesEnCatalogoConDatosDeIdioma( 
                        unIdiomaAccessible, 
                        unCodigoIdiomaReferencia, 
                        unaBusqueda, 
                        theParentExecutionRecord=unExecutionRecord)
                    
                    for unDatosTraduccion in unosDatosTraducciones:
                        unDictTraduccionesIdiomaReferencia[ unDatosTraduccion[ 'getSimbolo']] = unDatosTraduccion 
                                    
            theReport[ 'dictsTraduccionesIdiomasReferencia']  = unosDictsIdiomaReferencia
            return self
 
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
     
        
            
            
            
    security.declarePrivate( 'fIdiomasReferenciaEnSearchParameters')
    def fIdiomasReferenciaEnSearchParameters( self, theSearchParameters):
        """Extract from the search parameters the codes of the requested reference languages.
        
        """

        if not theSearchParameters:
            return []
    
        unosIdiomasReferencia = theSearchParameters.get( 'idiomasReferencia',  [])
        if not unosIdiomasReferencia:
            return []
        
        if not ( unosIdiomasReferencia.__class__.__name__ == 'list'):
            unosIdiomasReferencia = [  unosIdiomasReferencia, ]
            
        return unosIdiomasReferencia
     

    

    
    
    
    
    

    


    # ########################################################
    """Compose catalog search criteria for the various complexities of search parameters.
    
    """
    
    
    
     
    security.declarePrivate( 'fComponerSeleccionTraducciones')
    def fComponerSeleccionTraducciones( self, 
        theUseCaseQueryResult, 
        theIdioma, 
        theCodigoIdioma, 
        theSearchParameters, 
        theParentExecutionRecord=None):
        """Compose the Search criteria for the indexed catalogs from constraints supplied by the requester.
        
        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fComponerSeleccionTraducciones', theParentExecutionRecord, False) 
        
        try:

            unCriterioBusquedaNingunResultado = { 'getSimbolo' : [], }
            

            if not theCodigoIdioma or not theUseCaseQueryResult or not theUseCaseQueryResult.get( 'success', False):
                return unCriterioBusquedaNingunResultado
                 
            unosNombresModulos              = theSearchParameters.get( 'nombresModulos', '')
            if not unosNombresModulos:
                unosNombresModulos = []
            else:    
                if not ( unosNombresModulos.__class__.__name__ in [ 'list', 'tuple',]):
                    unosNombresModulos = [ unosNombresModulos,]
            
            
            aTextoEnSimbolo                 = theSearchParameters.get( 'simbolo', '').strip()
            aTextoEnCadenaTraducida         = theSearchParameters.get( 'cadenaTraducida', '').strip()
         
            unosSimbolosAFiltrar = set()
 
            unosModulosAccesibles = theUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'modules', {}).get( 'accepted_final_objects', [])
            todosModulos = self.fObtenerTodosModulos()
            unosNombresModulosAFiltrar = None
            if unosModulosAccesibles and not ( len( unosModulosAccesibles) == len( todosModulos)):
                unosNombresModulosAFiltrar = [ unModulo.Title() for unModulo in unosModulosAccesibles]
                       
        
            unIndexModuloNoEspecificado = (( cNombreModuloNoEspecificadoInputValue in unosNombresModulos) and unosNombresModulos.index( cNombreModuloNoEspecificadoInputValue)) or -1
            if unIndexModuloNoEspecificado >= 0:
                unosNombresModulos[ unIndexModuloNoEspecificado] = cNombreModuloNoEspecificadoSentinel 
                
            if unosNombresModulos:
                if not ( unosNombresModulosAFiltrar == None):
                    unosModulosSolicitadosYAFiltrar = set( unosNombresModulos).intersection( set( unosNombresModulosAFiltrar + [ cNombreModuloNoEspecificadoSentinel, ]))
                    if not unosModulosSolicitadosYAFiltrar:
                        return unCriterioBusquedaNingunResultado
                    else:
                        unosNombresModulosAFiltrar = sorted( unosModulosSolicitadosYAFiltrar)
                else:
                    unosNombresModulosAFiltrar = unosNombresModulos
                    
                unosSimbolosModulo = [ ]
                if theSearchParameters.get( 'cadenasInactivas', '').strip().lower() == "on":
                    unosSimbolosModulos = self.fListaSimbolosCadenasInactivasOrdenados( unExecutionRecord)
                else:
                    unosSimbolosModulos = self.fListaSimbolosCadenasOrdenadosEnVariosModulos( unosNombresModulosAFiltrar, unIndexModuloNoEspecificado >= 0, unExecutionRecord)

                if not unosSimbolosModulos:
                    return unCriterioBusquedaNingunResultado
                
                unosSimbolosAFiltrar = unosSimbolosModulos                
                
                
            if aTextoEnSimbolo:
                unosSimbolosPorTextoSimbolo = self.fBuscarSimbolosCadenasEnCatalogoTexto(  
                    aTextoEnSimbolo, 
                    theParentExecutionRecord=unExecutionRecord
                )
                if not unosSimbolosPorTextoSimbolo:
                    return unCriterioBusquedaNingunResultado
                if unosSimbolosAFiltrar:
                    unosSimbolosAFiltrar = set( unosSimbolosAFiltrar).intersection( set( unosSimbolosPorTextoSimbolo))
                else:
                    unosSimbolosAFiltrar = unosSimbolosPorTextoSimbolo
                    
                    
            if aTextoEnCadenaTraducida:
                unosSimbolosPorTextoCadenaTraducida = self.fBuscarSimbolosTraducionesEnCatalogoTextoParaIdioma(  
                    theIdioma, 
                    theCodigoIdioma, 
                    aTextoEnCadenaTraducida, 
                    theParentExecutionRecord=unExecutionRecord
                )
                if not unosSimbolosPorTextoCadenaTraducida:
                    return unCriterioBusquedaNingunResultado
                if unosSimbolosAFiltrar:
                    unosSimbolosAFiltrar = set( unosSimbolosAFiltrar).intersection( set( unosSimbolosPorTextoCadenaTraducida))
                else:
                    unosSimbolosAFiltrar = unosSimbolosPorTextoCadenaTraducida
       
                    
            if unosSimbolosAFiltrar:
                unCriterioBusqueda = { 'getSimbolo':  list( unosSimbolosAFiltrar), }
                return unCriterioBusqueda
                
            
            # do not restrict results on account of module name or text search
            return {}
            
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
        
    




    
    security.declarePrivate( 'fComponerBusquedaTraducciones')
    def fComponerBusquedaTraducciones( self, 
        theUseCaseQueryResult, 
        theIdioma, 
        theCodigoIdioma, 
        theSearchParameters, 
        theParentExecutionRecord=None):
        """Compose the Search criteria when constraints are imposed only on identifying and status information but does not filter on other TRATraduccion attributes.
        
        """
       
        unExecutionRecord = self.fStartExecution( 'method',  'fComponerBusquedaTraducciones', theParentExecutionRecord, False) 
        
        try:
            if not theCodigoIdioma or not theUseCaseQueryResult or not theUseCaseQueryResult.get( 'success', False):
                return {}
            
            unCriterioBusqueda = {}
                
            unosEstadosAIncluir             = theSearchParameters.get( 'estadosAIncluir', {} )
        
            unosEstadosIncluidos  = [ unEstado for unEstado in cTodosEstados if not unosEstadosAIncluir or ( unEstado in unosEstadosAIncluir) ]
            if not( len( unosEstadosIncluidos) == len( cTodosEstados)):
                unCriterioBusqueda[ 'getEstadoTraduccion'] = unosEstadosIncluidos
                   
            return unCriterioBusqueda
            
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
        

            
            
    
    security.declarePrivate( 'fComponerFiltroTraducciones')
    def fComponerFiltroTraducciones( self, 
        theUseCaseQueryResult, 
        theIdioma, 
        theCodigoIdioma, 
        theSearchParameters, 
        theParentExecutionRecord=None):
        """Compose the Search criteria when constraints are imposed filter on various  TRATraduccion attributes.
        
        """
       
        unExecutionRecord = self.fStartExecution( 'method',  'fComponerFiltroTraducciones', theParentExecutionRecord, False) 
        
        try:
            if not theCodigoIdioma or not theUseCaseQueryResult or not theUseCaseQueryResult.get( 'success', False):
                return {}
            
            from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fDateTimeNow
          
            unAhora = fDateTimeNow()

            aUsuarioCreador                   = theSearchParameters.get( 'usuarioCreador', '').strip()
            
            aFechaCreacionInicialNotRounded   = theSearchParameters.get( 'fechaCreacionInicial', '').strip()
            aFechaCreacionInicial             = self.fFechaISOStringRounded( aFechaCreacionInicialNotRounded, True, unAhora)
            if not ( aFechaCreacionInicial == aFechaCreacionInicialNotRounded):
                theSearchParameters[ 'fechaCreacionInicial'] = aFechaCreacionInicial   
                
            aFechaCreacionFinalNotRounded     = theSearchParameters.get( 'fechaCreacionFinal', '').strip()
            aFechaCreacionFinal               = self.fFechaISOStringRounded( aFechaCreacionFinalNotRounded, False, unAhora)
            if not ( aFechaCreacionFinal == aFechaCreacionFinalNotRounded):
                theSearchParameters[ 'fechaCreacionFinal'] = aFechaCreacionFinal   
                
            
            
            aUsuarioTraductor               = theSearchParameters.get( 'usuarioTraductor', '').strip()
            
            aFechaTraduccionInicialNotRounded   = theSearchParameters.get( 'fechaTraduccionInicial', '').strip()
            aFechaTraduccionInicial             = self.fFechaISOStringRounded( aFechaTraduccionInicialNotRounded, True, unAhora)
            if not ( aFechaTraduccionInicial == aFechaTraduccionInicialNotRounded):
                theSearchParameters[ 'fechaTraduccionInicial'] = aFechaTraduccionInicial   
                
            aFechaTraduccionFinalNotRounded     = theSearchParameters.get( 'fechaTraduccionFinal', '').strip()
            aFechaTraduccionFinal               = self.fFechaISOStringRounded( aFechaTraduccionFinalNotRounded, False, unAhora)
            if not ( aFechaTraduccionFinal == aFechaTraduccionFinalNotRounded):
                theSearchParameters[ 'fechaTraduccionFinal'] = aFechaTraduccionFinal   
                
            aUsuarioRevisor                 = theSearchParameters.get( 'usuarioRevisor', '').strip()
                        
            aFechaRevisionInicialNotRounded   = theSearchParameters.get( 'fechaRevisionInicial', '').strip()
            aFechaRevisionInicial             = self.fFechaISOStringRounded( aFechaRevisionInicialNotRounded, True, unAhora)
            if not ( aFechaRevisionInicial == aFechaRevisionInicialNotRounded):
                theSearchParameters[ 'fechaRevisionInicial'] = aFechaRevisionInicial   
                
            aFechaRevisionFinalNotRounded     = theSearchParameters.get( 'fechaRevisionFinal', '').strip()
            aFechaRevisionFinal               = self.fFechaISOStringRounded( aFechaRevisionFinalNotRounded, False, unAhora)
            if not ( aFechaRevisionFinal == aFechaRevisionFinalNotRounded):
                theSearchParameters[ 'fechaRevisionFinal'] = aFechaRevisionFinal   
            
            aFechaDefinitivoInicialNotRounded   = theSearchParameters.get( 'fechaDefinitivoInicial', '').strip()
            aFechaDefinitivoInicial             = self.fFechaISOStringRounded( aFechaDefinitivoInicialNotRounded, True, unAhora)
            if not ( aFechaDefinitivoInicial == aFechaDefinitivoInicialNotRounded):
                theSearchParameters[ 'fechaDefinitivoInicial'] = aFechaDefinitivoInicial   
                
            aFechaDefinitivoFinalNotRounded     = theSearchParameters.get( 'fechaDefinitivoFinal', '').strip()
            aFechaDefinitivoFinal               = self.fFechaISOStringRounded( aFechaDefinitivoFinalNotRounded, False, unAhora)
            if not ( aFechaDefinitivoFinal == aFechaDefinitivoFinalNotRounded):
                theSearchParameters[ 'fechaDefinitivoFinal'] = aFechaDefinitivoFinal   
                
            aUsuarioCoordinador             = theSearchParameters.get( 'usuarioCoordinador', '').strip()
         
            
            unCriterioBusqueda = { }
            
            if aUsuarioCreador:
                unCriterioBusqueda[ 'getUsuarioCreador'] = aUsuarioCreador
    
            if aFechaCreacionInicial or aFechaCreacionFinal:
                if aFechaCreacionInicial and aFechaCreacionFinal:
                    unCriterioBusqueda[ 'getFechaCreacionTextual'] = {'query': [ aFechaCreacionInicial, aFechaCreacionFinal,], 'range': 'minmax'}
                elif aFechaCreacionInicial:
                    unCriterioBusqueda[ 'getFechaCreacionTextual'] = {'query': aFechaCreacionInicial, 'range': 'min'}
                else:
                    unEarliestFechaCreacion = cEarliestFechaBusquedaTraduccioens
                    unCriterioBusqueda[ 'getFechaCreacionTextual'] = {'query': [ cEarliestFechaBusquedaTraducciones, aFechaCreacionFinal], 'range': 'minmax'}

            
            if aUsuarioTraductor:
                unCriterioBusqueda[ 'getUsuarioTraductor'] = aUsuarioTraductor
    
            if aFechaTraduccionInicial or aFechaTraduccionFinal:
                if aFechaTraduccionInicial and aFechaTraduccionFinal:
                    unCriterioBusqueda[ 'getFechaTraduccionTextual'] = {'query': [ aFechaTraduccionInicial, aFechaTraduccionFinal,], 'range': 'minmax'}
                elif aFechaTraduccionInicial:
                    unCriterioBusqueda[ 'getFechaTraduccionTextual'] = {'query': aFechaTraduccionInicial, 'range': 'min'}
                else:
                    unCriterioBusqueda[ 'getFechaTraduccionTextual'] = {'query': [ cEarliestFechaBusquedaTraducciones, aFechaTraduccionFinal], 'range': 'minmax'}

            if aUsuarioRevisor:
                unCriterioBusqueda[ 'getUsuarioRevisor'] = aUsuarioRevisor

            if aFechaRevisionInicial or aFechaRevisionFinal:
                if aFechaRevisionInicial and aFechaRevisionFinal:
                    unCriterioBusqueda[ 'getFechaRevisionTextual'] = {'query': [ aFechaRevisionInicial, aFechaRevisionFinal,], 'range': 'minmax'}
                elif aFechaRevisionInicial:
                    unCriterioBusqueda[ 'getFechaRevisionTextual'] = {'query': aFechaRevisionInicial, 'range': 'min'}
                else:
                    unCriterioBusqueda[ 'getFechaRevisionTextual'] = {'query': [ cEarliestFechaBusquedaTraducciones, aFechaRevisionFinal], 'range': 'minmax'}
                    

            if aUsuarioCoordinador:
                unCriterioBusqueda[ 'getUsuarioCoordinador'] = aUsuarioCoordinador

            if aFechaDefinitivoInicial or aFechaDefinitivoFinal:
                if aFechaRevisionInicial and aFechaDefinitivoFinal:
                    unCriterioBusqueda[ 'getFechaDefinitivoTextual'] = {'query': [ aFechaDefinitivoInicial, aFechaDefinitivoFinal,], 'range': 'minmax'}
                elif aFechaDefinitivoInicial:
                    unCriterioBusqueda[ 'getFechaDefinitivoTextual'] = {'query': aFechaDefinitivoInicial, 'range': 'min'}
                else:
                    unCriterioBusqueda[ 'getFechaDefinitivoTextual'] = {'query': [ cEarliestFechaBusquedaTraducciones, aFechaDefinitivoFinal], 'range': 'minmax'}
                        
            return unCriterioBusqueda
            
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
         


   
             
            
            
            
            
            
            

                
    security.declarePrivate( 'fLatestTimeWithHoursAndMinutes')
    def fLatestTimeWithHoursAndMinutes(self, theDate):
        """Calculate the latest date and time for a search interval.
        
        theDate may not include full detail of of the year, month, day, hour, minutes, seconds.
        the method will fill in teh remaining detail to the latest second of minute,
        last minute of hour, last hour of date, last date of month, last month of year.
        
        """
        if True:
            return theDate
    
        if not theDate:
            return None
        if ( theDate.hour() == 0) and ( theDate.minute() == 0) and ( int( theDate.second()) == 0):
            return DateTime( theDate.year(), theDate.month(), theDate.day(), 23, 59, 59.999)
        
        if not ( int( theDate.second()) == 0):
            return DateTime( theDate.year(), theDate.month(), theDate.day(), theDate.hour(), theDate.minute(), int( theDate.second()) + 0.999)

        if not ( theDate.minute() == 0):
            return DateTime( theDate.year(), theDate.month(), theDate.day(), theDate.hour(), theDate.minute(), 59.999)

        if not ( theDate.hour() == 0):
            return DateTime( theDate.year(), theDate.month(), theDate.day(), theDate.hour(), 59, 59.999)

        return DateTime( theDate.year(), theDate.month(), theDate.day(), 23, 59, 59.999)

                  

   
 

    
    
    
    
    
    ##/code-section class-header

    # Methods
# end of class TRACatalogo_CursorTraducciones

##code-section module-footer #fill in your manual code here
##/code-section module-footer



