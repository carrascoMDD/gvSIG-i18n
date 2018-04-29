# -*- coding: utf-8 -*-
#
# File: TRACatalogo_Informes.py
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

import sys
import traceback

import logging

import transaction

from math import floor


from DateTime import DateTime



from AccessControl      import ClassSecurityInfo

from Products.Archetypes.utils import shasattr

from Products.CMFCore.utils import getToolByName

from Products.CMFCore       import permissions



from TRACatalogo_Globales import TRACatalogo_Globales

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

from TRAElemento_Permission_Definitions import cBoundObject

from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_EllaborateInformeLanguages, cUseCase_EllaborateInformeModulesAndLanguages
from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_CreateTRAInforme, cUseCase_EllaborateInformeActividad

from Products.Archetypes.public import DisplayList









class TRACatalogo_Informes:
    """
    """
    security = ClassSecurityInfo()






    security.declarePrivate( 'fNewVoidInformeModulos')
    def fNewVoidInformeModulos(self):
        """Instantiate Results  for Modules report.

        """

        unNuevoInforme = {
            'report_date':        None,
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



    security.declarePrivate( 'fNewVoidInformeActividad')
    def fNewVoidInformeActividad(self):
        """Instantiate Result for an Activity report.

        """
        unNuevoInforme = {
            'success':                         False,
            'report_date':                     None,
            'totals':                          self.fNewVoidInformeActividad_TodosPeriodos( 'total'),
            'activity_reports_by_language':    { },
            'period_keys':                     [ ],
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







    security.declarePublic( 'fInformeTitulosIdiomasConIdiomaReferenciaYModulosPermitidos')
    def fInformeTitulosIdiomasConIdiomaReferenciaYModulosPermitidos( self, 
        theUseCaseName          =None, 
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None): 

        unExecutionRecord = self.fStartExecution( 'method',  'fInformeTitulosIdiomasConIdiomaReferenciaYModulosPermitidos', theParentExecutionRecord, False) 

        try:

            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)

            unInforme = self.fInformeTitulosIdiomasYModulosPermitidos(
                theUseCaseName          =theUseCaseName, 
                thePermissionsCache     =unPermissionsCache, 
                theRolesCache           =unRolesCache, 
                theParentExecutionRecord=unExecutionRecord)

            if not unInforme:
                return self.fNewVoidInformeTitulosIdiomasYModulosPermitidos()

            unSinIdiomaReferencia = self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_sinIdiomaReferencia', 'No reference language-')
            
            unosInformesIdiomas = unInforme[ 'idiomas']
            for unInformeIdioma in unosInformesIdiomas:
                if unInformeIdioma:
                    unCodigoIdioma = unInformeIdioma.get( 'codigoIdiomaEnGvSIG', '')
                    if unCodigoIdioma:
                        unosCodigosYDisplayNamesReferencia = [ [ '', unSinIdiomaReferencia,],]
                        for unInformeIdiomaParaReferencia in unosInformesIdiomas:
                            unCodigoIdiomaReferencia = unInformeIdiomaParaReferencia.get( 'codigoIdiomaEnGvSIG', '')
                            if unCodigoIdiomaReferencia and not ( unCodigoIdiomaReferencia == unCodigoIdioma):
                                unosCodigosYDisplayNamesReferencia.append( [ unCodigoIdiomaReferencia, unInformeIdiomaParaReferencia.get( 'displayTitle', [ unCodigoIdioma,unCodigoIdioma,]),])

                        if unosCodigosYDisplayNamesReferencia:
                            unInformeIdioma[ 'idiomas_referencia_vocabulary'] = unosCodigosYDisplayNamesReferencia

            return unInforme

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()







    security.declarePublic( 'fInformeTitulosIdiomasYModulosPermitidos')
    def fInformeTitulosIdiomasYModulosPermitidos( self, 
        theUseCaseName           =None, 
        thePermissionsCache      =None, 
        theRolesCache            =None, 
        theParentExecutionRecord =None): 
        """Report the titles of all languages and modules for which the user has permission to involve in exercising theUseCaseName.

        Output Values of type string returned in unicode.
        """

        unExecutionRecord = self.fStartExecution( 'method',  'fInformeTitulosIdiomasYModulosPermitidos', theParentExecutionRecord, False) 

        try:
            unInforme = self.fNewVoidInformeTitulosIdiomasYModulosPermitidos()

            if not theUseCaseName:
                return unInforme

            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)


            # ##############################################################################
            """Query for languages and modules accessible in the UseCase.

            """
            unUseCaseQueryResult = self.fUseCaseAssessment(  
                theUseCaseName          = theUseCaseName, 
                theElementsBindings     = { cBoundObject: self,},
                theRulesToCollect       = [ 'languages', 'modules',], 
                thePermissionsCache     = unPermissionsCache, 
                theRolesCache           = unRolesCache, 
                theParentExecutionRecord= unExecutionRecord) 
            if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                return unInforme  

            unInforme[ 'success']               = True
            unInforme[ 'use_case_query_results'].append( unUseCaseQueryResult)

            unNumeroCadenas = self.fObtenerNumeroCadenas()

            unInforme[ 'numero_cadenas'] = unNumeroCadenas

            unInforme[ 'display_country_flags'] = self.fDisplayCountryFlags()


            unosLanguagesNamesAndFlagsPorCodigo = self.fLanguagesNamesAndFlagsPorCodigo()

            unosInformesIdiomas = [ ]

            unosIdiomasAccesibles = unUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'languages', {}).get( 'accepted_final_objects', [])
            for unIdioma in unosIdiomasAccesibles: 

                unInformeIdioma = self.fNewVoidInformeTitulosIdioma()

                unCodigoIdioma = unIdioma.getCodigoIdiomaEnGvSIG()
                unPermiteModificar = unIdioma.fAllowWrite()

                unInformeIdioma.update( {
                    'codigoIdiomaEnGvSIG':           self.fAsUnicode( unCodigoIdioma), 
                    'codigoInternacionalDeIdioma':   self.fAsUnicode( unIdioma.getCodigoInternacionalDeIdioma() or ''),
                    'nombreIdioma':                  self.fAsUnicode( unIdioma.Title() or ''),
                    'nombreNativoDeIdioma':          self.fAsUnicode( unIdioma.getNombreNativoDeIdioma() or ''),
                    'flag':                          self.fAsUnicode( unosLanguagesNamesAndFlagsPorCodigo.get( unCodigoIdioma, {}).get( 'flag', cTRAFlagIdiomaDesconocida)),
                    'flag_url':                      self.fAsUnicode( unosLanguagesNamesAndFlagsPorCodigo.get( unCodigoIdioma, {}).get( 'flag_url', '%s/%s' % ( self.fPortalURL(), cTRAFlagIdiomaDesconocida,))),
                    'codigo_idioma_referencia':         self.fAsUnicode( unIdioma.getCodigoIdiomaReferencia()),
                    'juego_caracteres_javaproperties':  self.fAsUnicode( unIdioma.getJuegoDeCaracteresParaJavaProperties()),
                    'juego_caracteres_po':              self.fAsUnicode( unIdioma.getJuegoDeCaracteresParaPO()),
                    'displayTitle':                 self.fAsUnicode( unIdioma.fDisplayTitleAsUnicode()),
                    'modifiable':                   ( unPermiteModificar and True) or False,
                })
                unosInformesIdiomas.append( unInformeIdioma)

            unosInformesIdiomasSorted = sorted( unosInformesIdiomas, lambda uno, otro: cmp( uno[ 'codigoIdiomaEnGvSIG'], otro[ 'codigoIdiomaEnGvSIG']))
            unInforme[ 'idiomas'] = unosInformesIdiomasSorted


            unosInformesModulos = [ ]

            unosModulosAccesibles = unUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'modules', {}).get( 'accepted_final_objects', [])

            for unModulo in unosModulosAccesibles: 
                unosInformesModulos.append( self.fAsUnicode( unModulo.Title()))

            unosInformesModulosSorted = sorted( unosInformesModulos)
            unInforme[ 'modulos'] = unosInformesModulosSorted 

            return unInforme

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()





























    # #############################################################
    """Ellaboration of reports by languages or modules

    """  



    security.declareProtected( permissions.View, 'fElaborarInformeIdiomas')
    def fElaborarInformeIdiomas(self, 
        theCheckPermissions         =True, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):
        """Generate Report By Languages

        """        

        unExecutionRecord = self.fStartExecution( 'method',  'fElaborarInformeIdiomas', theParentExecutionRecord, False) 

        try:
            try:   
                unInforme = self.fNewVoidInformeIdiomas()
                unInforme[ 'report_date'] = self.fDateTimeNowString()


                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)


                if theCheckPermissions :
                    unUseCaseQueryResult = self.fUseCaseAssessment(  
                        theUseCaseName                  = cUseCase_EllaborateInformeLanguages, 
                        theElementsBindings             = { cBoundObject: self,}, 
                        theRulesToCollect               = None,
                        thePermissionsCache             = unPermissionsCache, 
                        theRolesCache                   = unRolesCache, 
                        theParentExecutionRecord        = unExecutionRecord,
                    )
                    if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                        return unInforme

                unosLanguagesNamesAndFlagsPorCodigo = self.fLanguagesNamesAndFlagsPorCodigo()


                unosIdiomasAccesibles = self.getCatalogo().fObtenerTodosIdiomas()
                if not unosIdiomasAccesibles:
                    return unInforme
                
                unInforme[ 'modules'] = self.fTodosNombresModulos()

                unosIdiomasAccesiblesParaOrdenar = [ [ unIdioma.getCodigoIdiomaEnGvSIG(), unIdioma,] for unIdioma in unosIdiomasAccesibles]
                unosIdiomasAccesiblesOrdenados = sorted( unosIdiomasAccesiblesParaOrdenar, lambda unCodigoEIdioma, otroCodigoEIdioma: cmp( unCodigoEIdioma[ 0], otroCodigoEIdioma[ 0]))
                unosIdiomasAccesibles = [ unCodigoEIdioma[ 1] for unCodigoEIdioma in unosIdiomasAccesiblesOrdenados]

                unNumeroCadenas = self.fObtenerNumeroCadenas()
                unInforme[ 'numero_cadenas'] = unNumeroCadenas

                unosInformesIdiomas = unInforme[ 'informes_idiomas']

                for unIdioma in unosIdiomasAccesibles:                
                    unInformeIdioma = self.fNewVoidInformeIdioma()
                    unCodigoIdioma = unIdioma.getCodigoIdiomaEnGvSIG()
                    unPermiteModificar = unIdioma.fAllowWrite()
                    unInformeIdioma.update( {
                        'nombre_idioma':                unIdioma.Title(), 
                        'codigo_idioma_en_gvsig':       unCodigoIdioma, 
                        'codigo_internacional_idioma':  unIdioma.getCodigoInternacionalDeIdioma(),
                        'nombre_nativo_idioma':         unIdioma.getNombreNativoDeIdioma(),
                        'flag':                         unosLanguagesNamesAndFlagsPorCodigo.get( unCodigoIdioma, {}).get( 'flag', cTRAFlagIdiomaDesconocida),
                        'flag_url':                     self.fAsUnicode( unosLanguagesNamesAndFlagsPorCodigo.get( unCodigoIdioma, {}).get( 'flag_url', '%s/%s' % ( self.fPortalURL(), cTRAFlagIdiomaDesconocida,))),
                        'url_idioma':                   unIdioma.absolute_url(), 
                        'modifiable':                   ( unPermiteModificar and True) or False,
                    } )       
                    unosInformesIdiomas.append( unInformeIdioma)


                # ####
                # ACV 20091217 Should work and report languages even if no strings, but it is already propery filled with zeroes by the void result factory method
                if not unNumeroCadenas:
                    unInforme[ 'success'] = True
                    return unInforme        


                for unIndexIdioma in range( len( unosIdiomasAccesibles)):
                    unIdioma = unosIdiomasAccesibles[ unIndexIdioma]

                    unCatalogBusquedaTraducciones = self.getCatalogo().fCatalogBusquedaTraduccionesParaIdioma( unIdioma)

                    unInformeIdioma = unosInformesIdiomas[ unIndexIdioma]
                    unCodigoIdiomaEnGvSIG = unInformeIdioma[ 'codigo_idioma_en_gvsig']
                    unosInformesEstados   = unInformeIdioma[ 'informes_estados']

                    unTotalTraducciones = 0            

                    for unIndexEstado in range( len( unosInformesEstados)):
                        unInformeEstado = unosInformesEstados[ unIndexEstado]
                        unEstado        = unInformeEstado[ 'nombre_estado']
                        
                        # ###############################
                        """ACV 20100511 added query condition getEstadoCadena, to avoid including translations of inactive strings.
                        
                        """
                        unaBusqueda = {   
                            'getEstadoCadena': cEstadoCadenaActiva,
                            'getEstadoTraduccion' :     unEstado, 
                        }

                        unosResultadosBusqueda      = unCatalogBusquedaTraducciones.searchResults(**unaBusqueda)

                        unNumeroResultados           = len( unosResultadosBusqueda)
                        unInformeEstado[ 'cantidad'] = unNumeroResultados
                        unTotalTraducciones          += unNumeroResultados
                        unInformeIdioma[ 'total_traducciones'] += unNumeroResultados

                    # Calc percentages
                    unTotalPorcentajes = 0
                    for unIndexEstado in range( len( cTodosEstados)):
                        if unNumeroCadenas:
                            unPorcentaje = int( floor( 100 * unosInformesEstados[ unIndexEstado][ 'cantidad'] / unNumeroCadenas ))
                        else:
                            unPorcentaje = 100
                        unosInformesEstados[ unIndexEstado][ 'porcentaje'] =  unPorcentaje
                        unTotalPorcentajes += unPorcentaje                                 

                    aDifference = 100 - unTotalPorcentajes

                    if aDifference > 0:
                        someInformesEstadoNoVacios = [ unInformeEstado for unInformeEstado in unosInformesEstados if ( unInformeEstado[ 'cantidad'] > 0) ]
                        someSortedInformesEstadoNoVacios = sorted( someInformesEstadoNoVacios, cmp=lambda unInformeEstado, otroInformeEstado: cmp(  unInformeEstado[ 'cantidad'], otroInformeEstado[ 'cantidad'])) 
                        someSortedInformesEstadoCasiUnoPorCiento = [ unInformeEstado for unInformeEstado in someSortedInformesEstadoNoVacios if ( unInformeEstado[ 'porcentaje'] < 1) ]

                        for unInformeEstado in someSortedInformesEstadoCasiUnoPorCiento:
                            unInformeEstado[ 'porcentaje'] = 1
                            aDifference -= 1  
                            if aDifference < 1:
                                break

                        if aDifference > 0:
                            for unInformeEstado in someSortedInformesEstadoNoVacios:
                                unInformeEstado[ 'porcentaje'] += 1
                                aDifference -= 1   
                                if aDifference < 1:
                                    break    

                unInforme[ 'report_date'] = self.fDateTimeNowString()   
                unInforme[ 'success'] = True
                
                self.pStatusReportByLanguagesJustGenerated()
                                
                return unInforme

            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))

                unInformeExcepcion = 'Exception during fElaborarInformeIdiomas\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   

                unInforme[ 'success'] = False
                unInforme[ 'condition'] = 'exception'
                unInforme[ 'exception'] = unInformeExcepcion

                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)

                return unInforme

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()









    security.declarePrivate( 'fElaborarInformeModulos')
    def fElaborarInformeModulos(self, 
        theCheckPermissions         =True, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):                                
        """Generate Report By Modules and Languages

        """        


        unExecutionRecord = self.fStartExecution( 'method',  'fElaborarInformeModulos', theParentExecutionRecord, False) 

        try:
            try:
                unInforme = self.fNewVoidInformeModulos()
                unInforme[ 'report_date'] = self.fDateTimeNowString()

                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)

                if theCheckPermissions:
                    unUseCaseQueryResult = self.fUseCaseAssessment(  
                        theUseCaseName          = cUseCase_EllaborateInformeModulesAndLanguages, 
                        theElementsBindings     = { cBoundObject: self,},
                        theRulesToCollect       = [ 'languages', 'modules',], 
                        thePermissionsCache     = unPermissionsCache, 
                        theRolesCache           = unRolesCache, 
                        theParentExecutionRecord= unExecutionRecord
                    ) 

                    if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                        return unInforme

                
                unosIdiomasAccesibles = self.getCatalogo().fObtenerTodosIdiomas()
                # ACV 20101013
                #if not unosIdiomasAccesibles:
                    #return unInforme
                
                unosCatalogosParaIdioma = [ None,] * len( unosIdiomasAccesibles)   
                for unIndexIdioma in range( len( unosIdiomasAccesibles)):
                    unIdioma = unosIdiomasAccesibles[ unIndexIdioma]
                    unosCatalogosParaIdioma[ unIndexIdioma] = self.getCatalogo().fCatalogBusquedaTraduccionesParaIdioma( unIdioma)

                
                
                unosModulosAccesibles = self.getCatalogo().fObtenerTodosModulos()
                unosModulosAccesibles.append( cNombreModuloNoEspecificadoSentinel)

                unosLanguagesNamesAndFlagsPorCodigo = self.fLanguagesNamesAndFlagsPorCodigo()

                unasCabecerasIdiomas    = unInforme[ 'cabeceras_idiomas']        
                unosInformesModulos     = unInforme[ 'informes_modulos']        

                for unIdioma in unosIdiomasAccesibles:
                    unaCabeceraIdioma = self.fNewVoidCabeceraIdioma()
                    unCodigoIdioma = unIdioma.getCodigoIdiomaEnGvSIG()
                    unPermiteModificar = unIdioma.fAllowWrite()                    
                    unaCabeceraIdioma.update( {
                        'nombre_idioma':    unIdioma.Title(), 
                        'url_idioma':       unIdioma.absolute_url(), 
                        'nombre_nativo_idioma':         unIdioma.getNombreNativoDeIdioma(), 
                        'codigo_idioma_en_gvsig':       unCodigoIdioma,
                        'codigo_internacional_idioma':  unIdioma.getCodigoInternacionalDeIdioma(),
                        'flag':                         unosLanguagesNamesAndFlagsPorCodigo.get( unCodigoIdioma, {}).get( 'flag', cTRAFlagIdiomaDesconocida),
                        'flag_url':                      self.fAsUnicode( unosLanguagesNamesAndFlagsPorCodigo.get( unCodigoIdioma, {}).get( 'flag_url', '%s/%s' % ( self.fPortalURL(), cTRAFlagIdiomaDesconocida,))),
                        'modifiable':                   ( unPermiteModificar and True) or False,
                    })
                    unasCabecerasIdiomas.append( unaCabeceraIdioma)



                unNumeroCadenas = self.fObtenerNumeroCadenas()
                unInforme[ 'numero_cadenas'] =  unNumeroCadenas


                for unModulo in unosModulosAccesibles:
                    unNombreModulo = ''
                    unNombreModuloForSearch = ''
                    if unModulo == cNombreModuloNoEspecificadoSentinel:
                        unNombreModulo          = self.fTranslateI18N( 'gvSIGi18n', cNombreModuloNoEspecificadoLabel_MsgId, u'Unspecified module-').encode( cTRAEncodingUTF8)
                        unNombreModuloForSearch = cNombreModuloNoEspecificadoInputValue
                    else:
                        unNombreModulo          = unModulo.Title()
                        unNombreModuloForSearch = unNombreModulo

                    unInformeModulo = self.fNewVoidInformeModulo()
                    unInformeModulo[ 'nombre_modulo'] = unNombreModulo
                    unInformeModulo[ 'nombre_modulo_for_search'] = unNombreModuloForSearch
                    
                    unosInformesModulos.append( unInformeModulo)

                    unosInformesIdiomas = unInformeModulo[ 'informes_idiomas']

                    for unIndexIdioma in range( len( unosIdiomasAccesibles)):
                        unInformeIdioma = self.fNewVoidInformeIdioma()
                        
                        unIdioma = unosIdiomasAccesibles[ unIndexIdioma]
                        unCodigoIdioma = unIdioma.getCodigoIdiomaEnGvSIG()
                        unPermiteModificar = unIdioma.fAllowWrite()                    
                        
                        unInformeIdioma.update( {
                            'nombre_idioma':                unIdioma.Title(), 
                            'codigo_idioma_en_gvsig':       unCodigoIdioma, 
                            'codigo_internacional_idioma':  unIdioma.getCodigoInternacionalDeIdioma(),
                            'nombre_nativo_idioma':         unIdioma.getNombreNativoDeIdioma(), 
                            'url_idioma':                   unIdioma.absolute_url(), 
                            'flag':                         unosLanguagesNamesAndFlagsPorCodigo.get( unCodigoIdioma, {}).get( 'flag', cTRAFlagIdiomaDesconocida),
                            'flag_url':                     self.fAsUnicode( unosLanguagesNamesAndFlagsPorCodigo.get( unCodigoIdioma, {}).get( 'flag_url', '%s/%s' % ( self.fPortalURL(), cTRAFlagIdiomaDesconocida,))),
                            'list_contents_permission':     True,
                            'modifiable':                   ( unPermiteModificar and True) or False,
                            'modules':                      [ unNombreModulo, ],

                        } )
                        unosInformesIdiomas.append( unInformeIdioma)



                    if unNumeroCadenas:      
                        if unModulo == cNombreModuloNoEspecificadoSentinel:
                            unosSimbolosCadenasEnModulo = self.fListaSimbolosCadenasOrdenadosModuloNoEspecificado( unExecutionRecord)
                        else:                        
                            unosSimbolosCadenasEnModulo = self.fListaSimbolosCadenasOrdenadosEnModulo( unModulo.Title(), unExecutionRecord)
                        
                        unNumeroCadenasEnModulo = len( unosSimbolosCadenasEnModulo)
                        if unNumeroCadenasEnModulo:

                            unInformeModulo[ 'numero_cadenas'] = unNumeroCadenasEnModulo


                            for unIndexIdioma in range( len( unosInformesIdiomas)):

                                unInformeIdioma                 = unosInformesIdiomas[ unIndexIdioma]
                                unCodigoIdiomaEnGvSIG           = unInformeIdioma[ 'codigo_idioma_en_gvsig']

                                unCatalogBusquedaTraducciones   = unosCatalogosParaIdioma[ unIndexIdioma]

                                if unCodigoIdiomaEnGvSIG and unCatalogBusquedaTraducciones:
                                    
                                    unaBusqueda = { 
                                        'getEstadoCadena':          cEstadoCadenaActiva,
                                        'getSimbolo':               unosSimbolosCadenasEnModulo,
                                    }
                                    unosResultadosBusqueda = unCatalogBusquedaTraducciones.searchResults(**unaBusqueda)
                                    
                                    unosNumeroResultadosPorEstado = [ 0] * len( cTodosEstados)
                                    
                                    for unResultadoTraduccion in unosResultadosBusqueda:
                                        unEstadoResultadoTraduccion = unResultadoTraduccion[ 'getEstadoTraduccion']
                                        unIndexEstadoTraduccion = -1
                                        try:
                                            unIndexEstadoTraduccion = cTodosEstados.index( unEstadoResultadoTraduccion)
                                        except:
                                            None
                                        if unIndexEstadoTraduccion >= 0:
                                            unosNumeroResultadosPorEstado[ unIndexEstadoTraduccion] += 1

                                            
                                    for unIndexEstado in range( len( cTodosEstados)):
                                        unEstado = cTodosEstados[ unIndexEstado]
                        
                                        unNumeroResultados = unosNumeroResultadosPorEstado[ unIndexEstado]

                                        unInformeIdioma[ 'informes_estados'][ unIndexEstado][ 'cantidad'] = unNumeroResultados
                                        unInformeIdioma[ 'total_traducciones' ] += unNumeroResultados

                                        unInformeModulo[ 'totales_estados'][ unIndexEstado][ 'cantidad'] += unNumeroResultados
                                        unInformeModulo[ 'total_traducciones'] += unNumeroResultados

                                        unInforme[ 'totales_estados'][ unIndexEstado][ 'cantidad'] += unNumeroResultados
                                        unInforme[ 'total_traducciones' ] += unNumeroResultados

                                        unasCabecerasIdiomas[ unIndexIdioma][ 'totales_estados'][ unIndexEstado][ 'cantidad']  += unNumeroResultados
                                        unasCabecerasIdiomas[ unIndexIdioma][ 'numero_cadenas'] += unNumeroResultados

                                        
                                    # Calc percentages
                                    unTotalPorcentajes = 0
                                    for unIndexEstado in range( len( cTodosEstados)):
                                        if unNumeroCadenas:
                                            unPorcentaje = int( floor( 100 * unInformeIdioma[ 'informes_estados'][ unIndexEstado][ 'cantidad'] / unNumeroCadenasEnModulo ))
                                        else:
                                            unPorcentaje = 100
                                        unInformeIdioma[ 'informes_estados'][ unIndexEstado][ 'porcentaje'] =  unPorcentaje
                                        unTotalPorcentajes += unPorcentaje                                 
                
                                    aDifference = 100 - unTotalPorcentajes
                
                                    if aDifference > 0:
                                        someInformesEstadoNoVacios = [ unInformeEstado for unInformeEstado in unInformeIdioma[ 'informes_estados'] if ( unInformeEstado[ 'cantidad'] > 0) ]
                                        someSortedInformesEstadoNoVacios = sorted( someInformesEstadoNoVacios, cmp=lambda unInformeEstado, otroInformeEstado: cmp(  unInformeEstado[ 'cantidad'], otroInformeEstado[ 'cantidad'])) 
                                        someSortedInformesEstadoCasiUnoPorCiento = [ unInformeEstado for unInformeEstado in someSortedInformesEstadoNoVacios if ( unInformeEstado[ 'porcentaje'] < 1) ]
                
                                        for unInformeEstado in someSortedInformesEstadoCasiUnoPorCiento:
                                            unInformeEstado[ 'porcentaje'] = 1
                                            aDifference -= 1  
                                            if aDifference < 1:
                                                break
                
                                        if aDifference > 0:
                                            for unInformeEstado in someSortedInformesEstadoNoVacios:
                                                unInformeEstado[ 'porcentaje'] += 1
                                                aDifference -= 1   
                                                if aDifference < 1:
                                                    break    
                
                                                
                                                
                                                

                unInforme[ 'report_date'] = self.fDateTimeNowString()   
                unInforme[ 'success'] = True
                
                self.pStatusReportByModulesAndLanguagesJustGenerated()

                
                return unInforme

            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))

                unInformeExcepcion = 'Exception during fElaborarInformeModulos\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   

                unInforme[ 'success'] = False
                unInforme[ 'condition'] = 'exception'
                unInforme[ 'exception'] = unInformeExcepcion

                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)

                return unInforme

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()


















    # #############################################################
    """Ellaboration of activity report

    """  



    security.declareProtected( permissions.View, 'fElaborarInformeActividad')
    def fElaborarInformeActividad(self, 
        theCheckPermissions         =True, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):
        """Generate Activity Report

        """        

        unExecutionRecord = self.fStartExecution( 'method',  'fElaborarInformeActividad', theParentExecutionRecord, False) 
        
        try:
            try:   
                unInforme = self.fNewVoidInformeActividad()
                unInforme[ 'report_date'] = self.fDateTimeNowString()


                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)


                if theCheckPermissions:
                    unUseCaseQueryResult = self.fUseCaseAssessment(  
                        theUseCaseName                  = cUseCase_EllaborateInformeActividad, 
                        theElementsBindings             = { cBoundObject: self,}, 
                        theRulesToCollect               = [ 'languages', ],
                        thePermissionsCache             = unPermissionsCache, 
                        theRolesCache                   = unRolesCache, 
                        theParentExecutionRecord        = unExecutionRecord,
                    )
                    if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                        return unInforme

                    
                    
                unosLanguagesNamesAndFlagsPorCodigo = self.fLanguagesNamesAndFlagsPorCodigo()


                unosIdiomasAccesibles = self.getCatalogo().fObtenerTodosIdiomas()
                if not unosIdiomasAccesibles:
                    return unInforme

                unosIdiomasAccesiblesParaOrdenar = [ [ unIdioma.getCodigoIdiomaEnGvSIG(), unIdioma,] for unIdioma in unosIdiomasAccesibles]
                unosIdiomasAccesiblesOrdenados   = sorted( unosIdiomasAccesiblesParaOrdenar, lambda unCodigoEIdioma, otroCodigoEIdioma: cmp( unCodigoEIdioma[ 0], otroCodigoEIdioma[ 0]))
                unosIdiomasAccesibles            = [ unCodigoEIdioma[ 1] for unCodigoEIdioma in unosIdiomasAccesiblesOrdenados]
                unosCodigosIdiomasAccesibles     = [ unCodigoEIdioma[ 0] for unCodigoEIdioma in unosIdiomasAccesiblesOrdenados]
                unosIdiomasPorCodigo = dict( [ [ unIdioma.getCodigoIdiomaEnGvSIG(), unIdioma] for unIdioma in unosIdiomasAccesibles])
                
                
                
                # #############################################################
                """Retrieve recent activities for this Translations Catalog
            
                """  
                someActivities = self.fRecentActivitiesForRoot()
                
                
                
                
                unDateTimeNow         = self.fDateTimeNow()
                unDateTimeNowString   = self.fDateToStoreString( unDateTimeNow)
                unDateTimeTodayString = unDateTimeNowString[:10]
                
                unDateTimeYesterday   = unDateTimeNow - 1
                unDateTimeYesterdayString = self.fDateToStoreString( unDateTimeYesterday)
                unDateTimeYesterdayString = unDateTimeYesterdayString[:10]
                
                unDateTimeLast7Days   = unDateTimeNow - 7
                unDateTimeLast7DaysString = self.fDateToStoreString( unDateTimeLast7Days)
                unDateTimeLast7DaysString = unDateTimeLast7DaysString[:10]
                
                unDateTimeLast30Days   = unDateTimeNow - 30
                unDateTimeLast30DaysString = self.fDateToStoreString( unDateTimeLast30Days)
                unDateTimeLast30DaysString = unDateTimeLast30DaysString[:10]
        

               
                unInforme_Totals = unInforme.get( 'totals', None)
                unosInformesByLanguage = unInforme.get( 'activity_reports_by_language', None)
                unInforme[ 'period_keys'] = cActivityReport_Periods[:]
                
                if someActivities:
                    # #############################################################
                    """Accumulate all valid activities.
                
                    """  
                    for anActivity in someActivities:
                    
                        if anActivity:
                            anActivityDate     = anActivity.get( cRecentActivity_Date, None)
                            anActivityLanguage = anActivity.get( cRecentActivity_Language, None)
                            anActivityUser     = anActivity.get( cRecentActivity_User, None)
                            
                            if anActivityDate and anActivityLanguage and anActivityUser:
                                if anActivityLanguage in unosCodigosIdiomasAccesibles:
                                    
                                    # #############################################################
                                    """Accumulate Total number of activities, overall and for each language.
                                
                                    """  
                                    
                                    unInforme_Totals[ 'num_activities'] += 1
                                    
                                    
                                    unInforme_Language_TodosPeriodos = unosInformesByLanguage.get( anActivityLanguage, None)
                                    if unInforme_Language_TodosPeriodos == None:
                                        unInforme_Language_TodosPeriodos = self.fNewVoidInformeActividad_TodosPeriodos( anActivityLanguage)
                                        unosInformesByLanguage[ anActivityLanguage] = unInforme_Language_TodosPeriodos
                                    
                                    unInforme_Language_TodosPeriodos[ 'num_activities'] += 1
                                    
                                    
                                    
                                     
                                    # #############################################################
                                    """Accumulate number of activities by periods.
                                
                                    """  
                                    unPeriodKey_TodayOrYesterday = None
                                    if anActivityDate >= unDateTimeTodayString:
                                        unPeriodKey_TodayOrYesterday = cActivityReport_Period_Today
                                    elif anActivityDate >= unDateTimeYesterdayString:
                                        unPeriodKey_TodayOrYesterday = cActivityReport_Period_Yesterday
                                    if unPeriodKey_TodayOrYesterday:   
                                        self.pAcumularActividadEnPeriodoInforme( anActivity, unPeriodKey_TodayOrYesterday, unInforme)
                                    
                                        
                                        
                                    unPeriodKey_Last7Days = None
                                    if anActivityDate >= unDateTimeLast7DaysString:
                                        unPeriodKey_Last7Days = cActivityReport_Period_Last7Days
                                        self.pAcumularActividadEnPeriodoInforme( anActivity, unPeriodKey_Last7Days, unInforme)
                                        
                                        
                                        
                                    unPeriodKey_Last30DaysOrBefore = None
                                    if anActivityDate >= unDateTimeLast30DaysString:
                                        unPeriodKey_Last30DaysOrBefore =cActivityReport_Period_Last30Days
                                    else:
                                        unPeriodKey_Last30DaysOrBefore = cActivityReport_Period_Before30Days
                                    if unPeriodKey_Last30DaysOrBefore:
                                        self.pAcumularActividadEnPeriodoInforme( anActivity, unPeriodKey_Last30DaysOrBefore, unInforme)
                        
                                    
                                    
                # #############################################################
                """Sort user names by number of activities, for overall activity.
            
                """  
                for unPeriodKey in cActivityReport_Periods:
                    
                    unInforme_Totals_Periodos = unInforme_Totals.get( 'periods', None)
                    if not ( unInforme_Totals_Periodos == None):
                        unInforme_Totals_Periodo = unInforme_Totals_Periodos[ unPeriodKey]
                        if unInforme_Totals_Periodo:
                            unInforme_Totals_Periodo_ByUsers = unInforme_Totals_Periodo[ 'users_and_num_activities']
                            unInforme_Totals_Periodo_ByUsers_ToSort = [ ]
                            for unUserId in unInforme_Totals_Periodo_ByUsers.keys():
                                unNumActivities = unInforme_Totals_Periodo_ByUsers.get( unUserId, 0)
                                unInforme_Totals_Periodo_ByUsers_ToSort.append( [ unUserId, unNumActivities,])
                            
                            unInforme_Totals_Periodo_ByUsers_Sorted = sorted( unInforme_Totals_Periodo_ByUsers_ToSort, lambda aOne, anOther: cmp( aOne[ 1], anOther[ 1]), reverse=True)
                            unInforme_Totals_Periodo[ 'users_and_num_activities'] = unInforme_Totals_Periodo_ByUsers_Sorted
                        else:
                            unInforme_Totals_Periodo[ 'users_and_num_activities'] = []
                     
                    
                # #############################################################
                """Sort user names by number of activities, for each language.
            
                """  
                for unCodigoIdioma in unosInformesByLanguage.keys():
                    unInforme_Language = unosInformesByLanguage.get( unCodigoIdioma, None)
                    if unInforme_Language:
                        
                        unIdioma = unosIdiomasPorCodigo.get( unCodigoIdioma, None)
                        if not( unIdioma == None):
                            unInforme_Language.update( {
                                'nombre_idioma':               unIdioma.Title(),
                                'nombre_nativo_idioma':        unIdioma.getNombreNativoDeIdioma(),
                                'codigo_idioma_en_gvsig':      unIdioma.getCodigoIdiomaEnGvSIG(),
                                'codigo_internacional_idioma': unIdioma.getCodigoInternacionalDeIdioma(),
                                'flag':                        unosLanguagesNamesAndFlagsPorCodigo.get( unCodigoIdioma, {}).get( 'flag', cTRAFlagIdiomaDesconocida),
                                'flag_url':                    self.fAsUnicode( unosLanguagesNamesAndFlagsPorCodigo.get( unCodigoIdioma, {}).get( 'flag_url', '%s/%s' % ( self.fPortalURL(), cTRAFlagIdiomaDesconocida,))),
                                'url_idioma':                  unIdioma.absolute_url(), 
                                'modifiable':                  ( unIdioma.fAllowWrite() and True) or False,
                                
                            })
                                                  
    
                                
        
                                
                        unInforme_Language_Periods = unInforme_Language.get( 'periods', None)
                        if not ( unInforme_Language_Periods == None):
                            
                            for unPeriodKey in cActivityReport_Periods:
                                unInforme_Language_Periodo = unInforme_Language_Periods.get( unPeriodKey, None)
                                if not( unInforme_Language_Periodo == None):
                                    unInforme_Language_Periodo_ByUsers = unInforme_Language_Periodo[ 'users_and_num_activities']
                                    unInforme_Language_Periodo_ByUsers_ToSort = [ ]
                                    for unUserId in unInforme_Language_Periodo_ByUsers.keys():
                                        unNumActivities = unInforme_Language_Periodo_ByUsers.get( unUserId, 0)
                                        unInforme_Language_Periodo_ByUsers_ToSort.append( [ unUserId, unNumActivities,])
                                
                                        unInforme_Language_Periodo_ByUsers_Sorted = sorted( unInforme_Language_Periodo_ByUsers_ToSort, lambda aOne, anOther: cmp( aOne[ 1], anOther[ 1]), reverse=True)
                                        unInforme_Language_Periodo[ 'users_and_num_activities'] = unInforme_Language_Periodo_ByUsers_Sorted

                        
                        
                                    
                unInforme[ 'report_date'] = self.fDateTimeNowString()   
                unInforme[ 'success'] = True
                
                self.pActivityReportJustGenerated()
                                
                return unInforme

            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))

                unInformeExcepcion = 'Exception during fElaborarInformeActividad\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   

                unInforme[ 'success'] = False
                unInforme[ 'condition'] = 'exception'
                unInforme[ 'exception'] = unInformeExcepcion

                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)

                return unInforme

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()






    security.declarePrivate( 'pAcumularActividadEnPeriodoInforme')
    def pAcumularActividadEnPeriodoInforme(self, theActivity=None, thePeriodKey=None, theInforme=None):
        if not theActivity:
            return self
        if not thePeriodKey:
            return self
        if not theInforme:
            return self
    
        unInforme_Totals       = theInforme.get( 'totals', None)
        if unInforme_Totals == None:
            return self
        
        unosInformesByLanguage = theInforme.get( 'activity_reports_by_language', None)
        if unosInformesByLanguage == None:
            return self
       
        anActivityDate     = theActivity.get( cRecentActivity_Date, None)
        anActivityLanguage = theActivity.get( cRecentActivity_Language, None)
        anActivityUser     = theActivity.get( cRecentActivity_User, None)
        
        if not( anActivityDate and anActivityLanguage and anActivityUser):
            return self
        
                
        unInforme_Totals_Periodos = unInforme_Totals.get( 'periods', None)
        if not ( unInforme_Totals_Periodos == None):
            unInforme_Totals_Periodo = unInforme_Totals_Periodos.get( thePeriodKey, None)
            if not ( unInforme_Totals_Periodos == None):
                unInforme_Totals_Periodo[ 'num_activities'] += 1
            
            unInforme_Totals_Periodo_ByUsers = unInforme_Totals_Periodo[ 'users_and_num_activities']
            unNumActivities_User = unInforme_Totals_Periodo_ByUsers.get( anActivityUser, 0)
            unInforme_Totals_Periodo_ByUsers[ anActivityUser] = unNumActivities_User + 1
        
        
        unInforme_Language_TodosPeriodos = unosInformesByLanguage.get( anActivityLanguage, None)
        if unInforme_Language_TodosPeriodos == None:
            unInforme_Language_TodosPeriodos = self.fNewVoidInformeActividad_TodosPeriodos( anActivityLanguage)
            unosInformesByLanguage[ anActivityLanguage] = unInforme_Language_TodosPeriodos
            
        unInforme_Language_Periodos = unInforme_Language_TodosPeriodos.get( 'periods', {})
        unInforme_Language_Periodo = unInforme_Language_Periodos.get( thePeriodKey, None)
        if unInforme_Language_Periodo == None:
            return self
        
        unInforme_Language_Periodo[ 'num_activities'] += 1
        
        unInforme_Language_Periodo_ByUsers = unInforme_Language_Periodo[ 'users_and_num_activities']
        unNumActivities_User = unInforme_Language_Periodo_ByUsers.get( anActivityUser, 0)
        unInforme_Language_Periodo_ByUsers[ anActivityUser] = unNumActivities_User + 1
                                        
            
        return self
   
    
    
    
    
    
    

    
    
    # ############################################
    """Invalidation of reports, depending on generation dates and changes since, held in globals of TRACAtalogo_Globales.
            
    """
    

    
        

      
    security.declareProtected( permissions.View, 'fNewVoidReportInvalidateObsoleteStatusReports')
    def fNewVoidReportInvalidateObsoleteStatusReports( self,):
        aReport = {
            'invalidated':        False,
            'path_del_raiz':      '',
            'changes_recorded':   0,
            'changes_threshold': -1,
            'seconds_lapsed':     0,
            'seconds_threshold': -1,
        }
        return aReport
        
            
       
    
    security.declarePrivate( 'fInvalidateObsoleteStatusReportByLanguages')
    def fInvalidateObsoleteStatusReportByLanguages(self, ):
        """If the Status Report by Languages is too old, or enough changes have been applied to translations in the catalog, invalidate the status report by languages for the catalog.
        
        """
                
        aReport = self.fNewVoidReportInvalidateObsoleteStatusReports()
        
        unPathDelRaiz = self.fPathDelRaiz()
        if not unPathDelRaiz:
            return aReport        
        aReport[ 'path_del_raiz'] = unPathDelRaiz
        
        
        unMustInvalidate              = False
        unVoteMustInvalidateByNumbers = False
        unVoteMustInvalidateByTime    = False
            
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
                
                       
            # ####################################################################
            """Check if the counter of changes since the last time the status report by languages was generated, is bigger than the maximum configured for the catalog. 
            
            """
            unaConfiguracion = self.fObtenerConfiguracion( cTRAConfiguracionAspecto_AlmacenPaginas)
            
            unNumeroDeCambiosAnularInformeIdiomas = 0
            if not ( unaConfiguracion == None):
                unNumeroDeCambiosAnularInformeIdiomas = unaConfiguracion.getNumeroDeCambiosAnularInformeIdiomas()
            if not unNumeroDeCambiosAnularInformeIdiomas:
                unNumeroDeCambiosAnularInformeIdiomas = 0
                
            aReport[ 'changes_threshold'] = unNumeroDeCambiosAnularInformeIdiomas

            if TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByLanguages == None:
                TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByLanguages = { }
                
            unNumTranslationsStatusChangesForRoot = TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByLanguages.get( unPathDelRaiz, None)
            if unNumTranslationsStatusChangesForRoot == None:
                unNumTranslationsStatusChangesForRoot = 0
                
            aReport[ 'changes_recorded'] = unNumTranslationsStatusChangesForRoot
                
            if unNumTranslationsStatusChangesForRoot >= unNumeroDeCambiosAnularInformeIdiomas:
                unVoteMustInvalidateByNumbers = True
            
                        
            # ####################################################################
            """If not already decided to invalidate, and there was any change, Check if enough time has lapsed since the last time the status report by languages was generated. 
            
            """
            unSegundosMinimosRetencionInformeIdiomas = 0
            if not ( unaConfiguracion == None):
                unaConfiguracion.getSegundosMinimosRetencionInformeIdiomas()
            if not unSegundosMinimosRetencionInformeIdiomas:
                unSegundosMinimosRetencionInformeIdiomas = 0
                
            aReport[ 'seconds_threshold'] = unSegundosMinimosRetencionInformeIdiomas
                

            if TRACatalogo_Globales.gStatusReportByLanguagesTimeMillis == None:
                TRACatalogo_Globales.gStatusReportByLanguagesTimeMillis = { }
                
            unStatusReportByLanguagesTimeMillis = TRACatalogo_Globales.gStatusReportByLanguagesTimeMillis.get( unPathDelRaiz, None)
            if unStatusReportByLanguagesTimeMillis == None:
                unStatusReportByLanguagesTimeMillis = 0
                
            unosMillisecondsNow = self.fMillisecondsNow()
            
            unosSecondsLapsed =  int(( unosMillisecondsNow - unStatusReportByLanguagesTimeMillis) / 1000)
            aReport[ 'seconds_lapsed'] = unosSecondsLapsed

            if unosSecondsLapsed >= unSegundosMinimosRetencionInformeIdiomas:
                unVoteMustInvalidateByTime = True
                
            
            if unVoteMustInvalidateByNumbers:
                unMustInvalidate = True
            else:
                if unVoteMustInvalidateByTime and unNumTranslationsStatusChangesForRoot:
                    unMustInvalidate = True
                    
                
                
                
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            
            
        if unMustInvalidate:
            self.pFlushCachedTemplates( [ 'TRACatalogoInforme', 'TRACatalogoInforme_NoHeaderNoFooter',])
            aReport[ 'invalidated'] = True
            
        return aReport
            
    

    
    
    
    security.declarePrivate( 'pStatusReportByLanguagesJustGenerated')
    def pStatusReportByLanguagesJustGenerated(self, ):
        """Record the time now, and Reset the counter of changes since the report was generated.
        
        """
                
        unPathDelRaiz = self.fPathDelRaiz()
        if not unPathDelRaiz:
            return self
        
        unMustInvalidate = False
            
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
                        
            # ####################################################################
            """Record the current time as the status report generation time. 
            
            """
            if TRACatalogo_Globales.gStatusReportByLanguagesTimeMillis == None:
                TRACatalogo_Globales.gStatusReportByLanguagesTimeMillis = { }
                
            unosMillisecondsNow = self.fMillisecondsNow()

            TRACatalogo_Globales.gStatusReportByLanguagesTimeMillis[ unPathDelRaiz] = unosMillisecondsNow
                 
                
                
                       
            # ####################################################################
            """Reset the counter of changes since the status report was generated.
            
            """
              
            if TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByLanguages == None:
                TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByLanguages = { }
                
            TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByLanguages[ unPathDelRaiz] = 0
                
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


        return self
            
    
    
    
    
    
    
    

    
    security.declarePrivate( 'fInvalidateObsoleteStatusReportByModulesAndLanguages')
    def fInvalidateObsoleteStatusReportByModulesAndLanguages(self, ):
        """If the Status Report by Modules and Languages is too old, or enough changes have been applied to translations in the catalog, invalidate the status report by modules and languages for the catalog.
        
        """
                
        aReport = self.fNewVoidReportInvalidateObsoleteStatusReports()
        
        
        unPathDelRaiz = self.fPathDelRaiz()
        if not unPathDelRaiz:
            return aReport
        
        unMustInvalidate              = False
        unVoteMustInvalidateByNumbers = False
        unVoteMustInvalidateByTime    = False
            
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
                
                       
            # ####################################################################
            """Check if the counter of changes since the last time the status report by languages was generated, is bigger than the maximum configured for the catalog. 
            
            """
            unaConfiguracion = self.fObtenerConfiguracion( cTRAConfiguracionAspecto_AlmacenPaginas)
            
            unNumeroDeCambiosAnularInformeModulosEIdiomas = 0
            if not ( unaConfiguracion == None):
                unNumeroDeCambiosAnularInformeModulosEIdiomas = unaConfiguracion.getNumeroDeCambiosAnularInformeModulosEIdiomas()
            if not unNumeroDeCambiosAnularInformeModulosEIdiomas:
                unNumeroDeCambiosAnularInformeModulosEIdiomas = 0

            aReport[ 'changes_threshold'] = unNumeroDeCambiosAnularInformeModulosEIdiomas
                
            if TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByModulesAndLanguages == None:
                TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByModulesAndLanguages = { }
                
            unNumTranslationsStatusChangesForRoot = TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByModulesAndLanguages.get( unPathDelRaiz, None)
            if unNumTranslationsStatusChangesForRoot == None:
                unNumTranslationsStatusChangesForRoot = 0
                
            aReport[ 'changes_recorded'] = unNumTranslationsStatusChangesForRoot
                
            if unNumTranslationsStatusChangesForRoot >= unNumeroDeCambiosAnularInformeModulosEIdiomas:
                unVoteMustInvalidateByNumbers = True
            
                        
            # ####################################################################
            """If not already decided to invalidate, and there was any change, Check if enough time has lapsed since the last time the status report by languages was generated. 
            
            """
            unSegundosMinimosRetencionInformeIdiomas = 0
            if not ( unaConfiguracion == None):
                unSegundosMinimosRetencionInformeIdiomas = unaConfiguracion.getSegundosMinimosRetencionInformeModulosEIdiomas()
            if not unSegundosMinimosRetencionInformeIdiomas:
                unSegundosMinimosRetencionInformeIdiomas = 0
                
            aReport[ 'seconds_threshold'] = unSegundosMinimosRetencionInformeIdiomas

            if TRACatalogo_Globales.gStatusReportByModulesAndLanguagesTimeMillis == None:
                TRACatalogo_Globales.gStatusReportByModulesAndLanguagesTimeMillis = { }
                
            unStatusReportByModulesAndLanguagesTimeMillis = TRACatalogo_Globales.gStatusReportByModulesAndLanguagesTimeMillis.get( unPathDelRaiz, None)
            if unStatusReportByModulesAndLanguagesTimeMillis == None:
                unStatusReportByModulesAndLanguagesTimeMillis = 0
                
            unosMillisecondsNow = self.fMillisecondsNow()
            
            unosSecondsLapsed =  int(( unosMillisecondsNow - unStatusReportByModulesAndLanguagesTimeMillis) / 1000)
            aReport[ 'seconds_lapsed'] = unosSecondsLapsed

            if unosSecondsLapsed >= unSegundosMinimosRetencionInformeIdiomas:
                unVoteMustInvalidateByTime = True
                
            
            if unVoteMustInvalidateByNumbers:
                unMustInvalidate = True
            else:
                if unVoteMustInvalidateByTime and unNumTranslationsStatusChangesForRoot:
                    unMustInvalidate = True
                    
                
                
                
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            
            
        if unMustInvalidate:
            self.pFlushCachedTemplates( [ 'TRACatalogoDetalle', 'TRACatalogoDetalle_NoHeaderNoFooter',])
            aReport[ 'invalidated'] = True
            
        return aReport
            
    

    
    
    
    security.declarePrivate( 'pStatusReportByModulesAndLanguagesJustGenerated')
    def pStatusReportByModulesAndLanguagesJustGenerated(self, ):
        """Record the time now, and Reset the counter of changes since the report was generated.
        
        """
                
        unPathDelRaiz = self.fPathDelRaiz()
        if not unPathDelRaiz:
            return self
        
        unMustInvalidate = False
            
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
                        
            # ####################################################################
            """Record the current time as the status report generation time. 
            
            """
            if TRACatalogo_Globales.gStatusReportByModulesAndLanguagesTimeMillis == None:
                TRACatalogo_Globales.gStatusReportByModulesAndLanguagesTimeMillis = { }
                
            unosMillisecondsNow = self.fMillisecondsNow()

            TRACatalogo_Globales.gStatusReportByModulesAndLanguagesTimeMillis[ unPathDelRaiz] = unosMillisecondsNow
                 
                
                
                       
            # ####################################################################
            """Reset the counter of changes since the status report was generated.
            
            """
              
            if TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByModulesAndLanguages == None:
                TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByModulesAndLanguages = { }
                
            TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByModulesAndLanguages[ unPathDelRaiz] = 0
                
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


        return self
            
    
                        
    

    
    security.declarePrivate( 'fInvalidateObsoleteActivityReport')
    def fInvalidateObsoleteActivityReport(self, ):
        """If the Activity Report is too old, or enough activity has taken place in the catalog, invalidate the activity report for the catalog.
        
        """        
        aReport = self.fNewVoidReportInvalidateObsoleteStatusReports()
        
        unPathDelRaiz = self.fPathDelRaiz()
        if not unPathDelRaiz:
            return aReport        
        aReport[ 'path_del_raiz'] = unPathDelRaiz
        
        
        unMustInvalidate              = False
        unVoteMustInvalidateByNumbers = False
        unVoteMustInvalidateByTime    = False
            
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
                
                       
            # ####################################################################
            """Check if the counter of changes since the last time the activity report was generated, is bigger than the maximum configured for the catalog. 
            
            """
            unaConfiguracion = self.fObtenerConfiguracion( cTRAConfiguracionAspecto_AlmacenPaginas)
            
            unNumeroDeActividadesAnularInformeActividad = 0
            if not ( unaConfiguracion == None):
                unNumeroDeActividadesAnularInformeActividad = unaConfiguracion.fObtenerConfiguracion( cTRAConfiguracionAspecto_AlmacenPaginas).getNumeroDeActividadesAnularInformeActividad()
            if not unNumeroDeActividadesAnularInformeActividad:
                unNumeroDeActividadesAnularInformeActividad = 0
                
            aReport[ 'changes_threshold'] = unNumeroDeActividadesAnularInformeActividad

            if TRACatalogo_Globales.gNumActivitiesSinceActivityReport == None:
                TRACatalogo_Globales.gNumActivitiesSinceActivityReport = { }
                
            unNumActivitiesForRoot = TRACatalogo_Globales.gNumActivitiesSinceActivityReport.get( unPathDelRaiz, None)
            if unNumActivitiesForRoot == None:
                unNumActivitiesForRoot = 0
                
            aReport[ 'changes_recorded'] = unNumActivitiesForRoot
                
            if unNumActivitiesForRoot >= unNumeroDeActividadesAnularInformeActividad:
                unVoteMustInvalidateByNumbers = True
            
                        
            # ####################################################################
            """If not already decided to invalidate, and there was any change, Check if enough time has lapsed since the last time the status report by languages was generated. 
            
            """
            unSegundosMinimosRetencionInformeActividad = 0           
            if not ( unaConfiguracion == None):
                unSegundosMinimosRetencionInformeActividad = unaConfiguracion.getSegundosMinimosRetencionInformeActividad()
            if not unSegundosMinimosRetencionInformeActividad:
                unSegundosMinimosRetencionInformeActividad = 0
                
            aReport[ 'seconds_threshold'] = unSegundosMinimosRetencionInformeActividad
                

            if TRACatalogo_Globales.gActivityReportTimeMillis == None:
                TRACatalogo_Globales.gActivityReportTimeMillis = { }
                
            unActivityReportTimeMillis = TRACatalogo_Globales.gActivityReportTimeMillis.get( unPathDelRaiz, None)
            if unActivityReportTimeMillis == None:
                unActivityReportTimeMillis = 0
                
            unosMillisecondsNow = self.fMillisecondsNow()
            
            unosSecondsLapsed =  int(( unosMillisecondsNow - unActivityReportTimeMillis) / 1000)
            aReport[ 'seconds_lapsed'] = unosSecondsLapsed

            if unosSecondsLapsed >= unSegundosMinimosRetencionInformeActividad:
                unVoteMustInvalidateByTime = True
                
            
            if unVoteMustInvalidateByNumbers:
                unMustInvalidate = True
            else:
                if unVoteMustInvalidateByTime and unNumActivitiesForRoot:
                    unMustInvalidate = True
                    
                
                
                
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            
            
        if unMustInvalidate:
            self.pFlushCachedTemplates( [ 'TRACatalogoActividad', 'TRACatalogoActividad_NoHeaderNoFooter',])
            aReport[ 'invalidated'] = True
            
        return aReport
            
    

    
    
    
    security.declarePrivate( 'pActivityReportJustGenerated')
    def pActivityReportJustGenerated(self, ):
        """Record the time now, and Reset the counter of changes since the report was generated.
        
        """
               
        unPathDelRaiz = self.fPathDelRaiz()
        if not unPathDelRaiz:
            return self
        
        unMustInvalidate = False
            
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
                        
            # ####################################################################
            """Record the current time as the status report generation time. 
            
            """
            if TRACatalogo_Globales.gActivityReportTimeMillis == None:
                TRACatalogo_Globales.gActivityReportTimeMillis = { }
                
            unosMillisecondsNow = self.fMillisecondsNow()

            TRACatalogo_Globales.gActivityReportTimeMillis[ unPathDelRaiz] = unosMillisecondsNow
                 
                
                
                       
            # ####################################################################
            """Reset the counter of changes since the status report was generated.
            
            """
              
            if TRACatalogo_Globales.gNumActivitiesSinceActivityReport == None:
                TRACatalogo_Globales.gNumActivitiesSinceActivityReport = { }
                
            TRACatalogo_Globales.gNumActivitiesSinceActivityReport[ unPathDelRaiz] = 0
                
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


        return self
            
        