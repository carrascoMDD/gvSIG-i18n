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
            'success':                          False,
            'report_date':                '',
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




    security.declareProtected( permissions.View, 'fElaborarInformeContribuciones')
    def fElaborarInformeContribuciones(self, 
        theProcessControlManager    =None,
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):
        """Generate Report By Languages

        """        

        unExecutionRecord = self.fStartExecution( 'method',  'fElaborarInformeContribuciones', theParentExecutionRecord, False) 

        try:
            try:   
                unInforme = self.fNewVoidInformeContribuciones()
                unInforme[ 'report_date']    = self.fDateTimeNowString()
                unInforme[ 'reporting_user'] = self.fGetMemberId()


                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)

                unosLanguagesNamesAndFlagsPorCodigo = self.fLanguagesNamesAndFlagsPorCodigo()


                unosIdiomasAccesibles = self.getCatalogo().fObtenerTodosIdiomas()
                if not unosIdiomasAccesibles:
                    return unInforme
                
                
                
                
                
                
                # #######################################
                """Retrieve from configuration the names of users that administer the translations catalog, and thus shall appear at the bottom of contributing users, even if they have performed a higher number of changes into the translations catalog.
                
                """
                unosUsuariosAdministradores = [ ]
                unaConfiguracionVarios = self.fObtenerConfiguracion( cTRAConfiguracionAspecto_Varios)
                if unaConfiguracionVarios:        
                    unosUsuariosAdministradoresString = unaConfiguracionVarios.getUsuariosAdministradores()
                    if unosUsuariosAdministradoresString:
                        unosUsuariosAdministradores = unosUsuariosAdministradoresString.split()
                        
                unInforme[ 'admin_user_ids'] = sorted( unosUsuariosAdministradores)        
                        
                
                
                
                
                
                # #######################################
                """Calculate significant period dates.
                
                """
                unDateTimeNow             = self.fDateTimeNow()
                unDateTimeNowString       = self.fDateToStoreString( unDateTimeNow )
                unDateTimeNowString       = unDateTimeNowString[:10]
                
                unDateTimeToday           = unDateTimeNow
                unDateTimeTodayString     = unDateTimeNowString
                unDateTimeTodayBeginString  = '%s 00:00:00' % unDateTimeTodayString
                unDateTimeTodayEndString    = '%s 23:59:59' % unDateTimeTodayString
                unInforme[ 'periods_dates'][ cTRAContribucionesReport_Period_Today] = [ unDateTimeTodayBeginString, unDateTimeTodayEndString,]
                
                unDateTimeTodayBegin      = DateTime( unDateTimeTodayBeginString)
                
                unDateTimeYesterday       = unDateTimeTodayBegin - 1
                unDateTimeYesterdayString = self.fDateToStoreString( unDateTimeYesterday)
                unDateTimeYesterdayString = unDateTimeYesterdayString[:10]
                unDateTimeYesterdayBeginString = '%s 00:00:00' % unDateTimeYesterdayString
                unDateTimeYesterdayEndString   = '%s 23:59:59' % unDateTimeYesterdayString
                unInforme[ 'periods_dates'][ cTRAContribucionesReport_Period_Yesterday] = [ unDateTimeYesterdayBeginString, unDateTimeYesterdayEndString,]

                
                unDateTimeLast7Days       = unDateTimeTodayBegin - 7
                unDateTimeLast7DaysString = self.fDateToStoreString( unDateTimeLast7Days)
                unDateTimeLast7DaysString = unDateTimeLast7DaysString[:10]
                unDateTimeLast7DaysBeginString = '%s 00:00:00' % unDateTimeLast7DaysString
                unDateTimeLast7DaysEndString   = unDateTimeTodayEndString
                unInforme[ 'periods_dates'][ cTRAContribucionesReport_Period_Last7Days] = [ unDateTimeLast7DaysBeginString, unDateTimeLast7DaysEndString,]
                                
                
                unDateTimeLast30Days       = unDateTimeTodayBegin - 30
                unDateTimeLast30DaysString = self.fDateToStoreString( unDateTimeLast30Days)
                unDateTimeLast30DaysString = unDateTimeLast30DaysString[:10]
                unDateTimeLast30DaysBeginString = '%s 00:00:00' % unDateTimeLast30DaysString
                unDateTimeLast30DaysEndString   = unDateTimeTodayEndString
                unInforme[ 'periods_dates'][ cTRAContribucionesReport_Period_Last30Days] = [ unDateTimeLast30DaysBeginString, unDateTimeLast30DaysEndString,]
                
                
                unDateTimeLast365Days       = unDateTimeTodayBegin - 365
                unDateTimeLast365DaysString = self.fDateToStoreString( unDateTimeLast365Days)
                unDateTimeLast365DaysString = unDateTimeLast365DaysString[:10]
                unDateTimeLast365DaysBeginString = '%s 00:00:00' %  unDateTimeLast365DaysString
                unDateTimeLast365DaysEndString  = unDateTimeTodayEndString
                unInforme[ 'periods_dates'][ cTRAContribucionesReport_Period_Last365Days] = [ unDateTimeLast365DaysBeginString, unDateTimeLast365DaysEndString,]
                
                
                unDateTimeBefore365Days       = unDateTimeTodayBegin - 366
                unDateTimeBefore365DaysString = self.fDateToStoreString( unDateTimeBefore365Days)
                unDateTimeBefore365DaysString = unDateTimeBefore365DaysString[:10]
                unDateTimeBefore365DaysEndString   = unDateTimeBefore365DaysString
                unDateTimeBefore365DaysBeginString = '1900-01-01 00:00:00' 
                unInforme[ 'periods_dates'][ cTRAContribucionesReport_Period_Before365Days] = [ unDateTimeBefore365DaysBeginString, unDateTimeBefore365DaysEndString,]
                
                
                
                
                
                

                # #######################################
                """Retrieve accessible languages.
                
                """

                unosIdiomasAccesiblesParaOrdenar = [ [ unIdioma.getCodigoIdiomaEnGvSIG(), unIdioma,] for unIdioma in unosIdiomasAccesibles]
                unosIdiomasAccesiblesOrdenados = sorted( unosIdiomasAccesiblesParaOrdenar, lambda unCodigoEIdioma, otroCodigoEIdioma: cmp( unCodigoEIdioma[ 0], otroCodigoEIdioma[ 0]))
                unosIdiomasAccesibles = [ unCodigoEIdioma[ 1] for unCodigoEIdioma in unosIdiomasAccesiblesOrdenados]


                
                
                
                
                
                
                # #######################################
                """Iterate on translations for all languages.
                
                """
                
                for unIdioma in unosIdiomasAccesibles:                
                    
                    
                    
                    # #######################################
                    """Add report entry for the language.
                    
                    """
                    unInformeIdioma = self.fNewVoidInformeContribucionesIdioma()
                    
                    unCodigoIdioma = unIdioma.getCodigoIdiomaEnGvSIG()
                    unInformeIdioma.update( {
                        'nombre_idioma':                unIdioma.Title(), 
                        'codigo_idioma_en_gvsig':       unCodigoIdioma, 
                        'codigo_internacional_idioma':  unIdioma.getCodigoInternacionalDeIdioma(),
                        'nombre_nativo_idioma':         unIdioma.getNombreNativoDeIdioma(),
                        'flag':                         unosLanguagesNamesAndFlagsPorCodigo.get( unCodigoIdioma, {}).get( 'flag', cTRAFlagIdiomaDesconocida),
                        'flag_url':                     self.fAsUnicode( unosLanguagesNamesAndFlagsPorCodigo.get( unCodigoIdioma, {}).get( 'flag_url', '%s/%s' % ( self.fPortalURL(), cTRAFlagIdiomaDesconocida,))),
                        'url_idioma':                   unIdioma.absolute_url(), 
                    } )       
                    unInforme[ 'contributions_by_language'][ unCodigoIdioma] = unInformeIdioma
                    unInforme[ 'sorted_language_codes'] = sorted(  unInforme[ 'contributions_by_language'].keys())

                    
                    theProcessControlManager.pProcessStep( self, { unIdioma.meta_type: 1, }, None)
                    
                    
                    
                    
                    
                    
                    
                    # #######################################
                    """Search for index records for the translations into the language.
                    
                    """
                    
                    unCatalogFiltroTraducciones = self.getCatalogo().fCatalogFiltroTraduccionesParaIdioma( unIdioma)


                    unTotalTraducciones = 0            

                    unaBusqueda = {   
                        #'getEstadoCadena':   cEstadoCadenaActiva, # ACV 20110207 Count contributions even if the string was later deactivated.
                    }

                    unosResultadosBusqueda      = unCatalogFiltroTraducciones.searchResults(**unaBusqueda)

                    
                    
                    
                        
                    # #######################################
                    """Scan all found translation index records for the language.
                    
                    """
                    for unResultadoTraduccion in unosResultadosBusqueda:
                        
                        unEstadoTraduccion = unResultadoTraduccion[ 'getEstadoTraduccion']
                        
                        unUsuarioCreador   = unResultadoTraduccion[ 'getUsuarioCreador']
                        unaFechaCreacion   = unResultadoTraduccion[ 'getFechaCreacionTextual']
                        
                        
                        
                        
                        # #######################################
                        """Accumulate for the user a translation creation contribution.
                        
                        """
                        if unUsuarioCreador and unaFechaCreacion:
                                
                            self.pAcumularContribucionDeUsuario( 
                                theProcessControlManager           =theProcessControlManager,
                                theInforme                         =unInforme, 
                                theCodigoIdioma                    =unCodigoIdioma,
                                theUsuario                         =unUsuarioCreador, 
                                theFecha                           =unaFechaCreacion,
                                theModoContribucion                =cTRAContribucion_Modo_Creacion,
                            )
                            
                    
                            
                        if unEstadoTraduccion in [ cEstadoTraduccionTraducida, cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva,]:
                            
                            
                            
                            
                            # #######################################
                            """Accumulate for the user a translation change contribution.
                            
                            """
                            unUsuarioTraductor = unResultadoTraduccion[ 'getUsuarioTraductor']
                            unaFechaTraduccion = unResultadoTraduccion[ 'getFechaTraduccionTextual']
                            if unUsuarioTraductor and unaFechaTraduccion:
                                
                                self.pAcumularContribucionDeUsuario( 
                                    theProcessControlManager           =theProcessControlManager,
                                    theInforme                         =unInforme, 
                                    theCodigoIdioma                    =unCodigoIdioma,
                                    theUsuario                         =unUsuarioTraductor, 
                                    theFecha                           =unaFechaTraduccion,
                                    theModoContribucion                =cTRAContribucion_Modo_Traduccion,
                                )

                                
                                
                                
                            if unEstadoTraduccion in [ cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva,]:
                                
                                # #######################################
                                """Accumulate for the user a translation review contribution.
                                
                                """
                                unUsuarioRevisor   = unResultadoTraduccion[ 'getUsuarioRevisor']
                                unaFechaRevision   = unResultadoTraduccion[ 'getFechaRevisionTextual']
                                if unUsuarioRevisor and unaFechaRevision:
                                    
                                    self.pAcumularContribucionDeUsuario( 
                                        theProcessControlManager           =theProcessControlManager,
                                        theInforme                         =unInforme, 
                                        theCodigoIdioma                    =unCodigoIdioma,
                                        theUsuario                         =unUsuarioRevisor, 
                                        theFecha                           =unaFechaRevision,
                                        theModoContribucion                =cTRAContribucion_Modo_Revision,
                                    )
                                    
                                
                                    
                                    
                                if unEstadoTraduccion in [ cEstadoTraduccionDefinitiva,]:
                                
                                    # #######################################
                                    """Accumulate for the user a translation lock (make definitive) contribution.
                                    
                                    """
                                    unUsuarioCoordinador   = unResultadoTraduccion[ 'getUsuarioCoordinador']
                                    unaFechaDefinitivo     = unResultadoTraduccion[ 'getFechaDefinitivoTextual']
                                    if unUsuarioCoordinador and unaFechaDefinitivo:
                                        
                                        self.pAcumularContribucionDeUsuario( 
                                            theProcessControlManager           =theProcessControlManager,
                                            theInforme                         =unInforme, 
                                            theCodigoIdioma                    =unCodigoIdioma,
                                            theUsuario                         =unUsuarioCoordinador, 
                                            theFecha                           =unaFechaDefinitivo,
                                            theModoContribucion                =cTRAContribucion_Modo_Definitiva,
                                        )
                                        
                
                
                
                        theProcessControlManager.pProcessStep( self, { cNombreTipoTRATraduccion: 1,}, None)
   
                                        
                
                                        
                                        
                # #######################################
                """Collect from all languages the number of contributions and id for each non-administrator user, and each administrator, to be ranked later by the number of their contributions.
                
                """
                                        
                unasContributionsByUsers = unInforme[ 'contributions_by_user']
                
                someTotalsAndUserIds                     = [ ]
                somePeriodsTotalsAndUserIds              = dict( [ [ aPeriodKey, [ ], ] for  aPeriodKey in cTRAContribucionesReport_Periods])
                someTotalsAndAdministratorUserIds        = [ ]
                somePeriodsTotalsAndAdministratorUserIds = dict( [ [ aPeriodKey, [ ], ] for  aPeriodKey in cTRAContribucionesReport_Periods])
                
                someUserIds = unasContributionsByUsers.keys()
                for aUserId in someUserIds:
                    
                    if not ( aUserId in unosUsuariosAdministradores):
                        
                        aUserContributions = unasContributionsByUsers.get( aUserId, {})
                        if aUserContributions:
                            
                            if aUserContributions.get( 'total_contributions', 0):
                                someTotalsAndUserIds.append( [ aUserContributions.get( 'total_contributions', 0), aUserId,])
                                
                                for  aPeriodKey in cTRAContribucionesReport_Periods:
                                    aUserContributionsInPeriod = aUserContributions[ 'contributions_by_periods'].get( aPeriodKey, {})
                                    if aUserContributionsInPeriod:
                                        
                                        if aUserContributionsInPeriod.get( 'total_contributions', 0):                                        
                                            somePeriodsTotalsAndUserIds[ aPeriodKey].append( [ aUserContributionsInPeriod.get( 'total_contributions', 0), aUserId,])                         
                    
                    else:                               
                        aUserContributions = unasContributionsByUsers.get( aUserId, {})
                        if aUserContributions:
                            
                            if aUserContributions.get( 'total_contributions', 0):
                                someTotalsAndAdministratorUserIds.append( [ aUserContributions.get( 'total_contributions', 0), aUserId,])
                                
                                for  aPeriodKey in cTRAContribucionesReport_Periods:
                                    aUserContributionsInPeriod = aUserContributions[ 'contributions_by_periods'].get( aPeriodKey, {})
                                    if aUserContributionsInPeriod:
                                        
                                        if aUserContributionsInPeriod.get( 'total_contributions', 0):
                                            somePeriodsTotalsAndAdministratorUserIds[ aPeriodKey].append( [ aUserContributionsInPeriod.get( 'total_contributions', 0), aUserId,])                         
                        
                                        
                                        
                # #######################################
                """Rank changes in all languages by administrator and non-administrator users according to the number of their contributions.
                
                """
                someSortedTotalsAndUserIds = sorted( someTotalsAndUserIds, lambda aCountAndId, otherCountAndId: cmp( aCountAndId[ 0], otherCountAndId[ 0]), reverse=True,)
                someSortedTotalsUserIds = [ aCountAndId[ 1] for aCountAndId in someSortedTotalsAndUserIds]

                unInforme[ 'rank_user_ids_total'] = someSortedTotalsUserIds
                
                
                someSortedTotalsAndAdministratorUserIds = sorted( someTotalsAndAdministratorUserIds, lambda aCountAndId, otherCountAndId: cmp( aCountAndId[ 0], otherCountAndId[ 0]), reverse=True,)
                someSortedTotalsAdministratorUserIds = [ aCountAndId[ 1] for aCountAndId in someSortedTotalsAndAdministratorUserIds]

                unInforme[ 'rank_admin_user_ids_total'] = someSortedTotalsAdministratorUserIds
                

                
                for  aPeriodKey in cTRAContribucionesReport_Periods:
                                            
                    someTotalsAndUserIdsInPeriod = somePeriodsTotalsAndUserIds[ aPeriodKey]                         
                    someSortedTotalsAndUserIdsInPeriod = sorted( someTotalsAndUserIdsInPeriod, lambda aCountAndId, otherCountAndId: cmp( aCountAndId[ 0], otherCountAndId[ 0]), reverse=True,)
                    someSortedUserIdsInPeriod = [ aCountAndId[ 1] for aCountAndId in someSortedTotalsAndUserIdsInPeriod]                     
                    unInforme[ 'rank_user_ids_by_periods'][ aPeriodKey] = someSortedUserIdsInPeriod
                
                    someTotalsAndAdministratorUserIdsInPeriod = somePeriodsTotalsAndAdministratorUserIds[ aPeriodKey]                         
                    someSortedTotalsAndAdministratorUserIdsInPeriod = sorted( someTotalsAndAdministratorUserIdsInPeriod, lambda aCountAndId, otherCountAndId: cmp( aCountAndId[ 0], otherCountAndId[ 0]), reverse=True,)
                    someSortedAdministratorUserIdsInPeriod = [ aCountAndId[ 1] for aCountAndId in someSortedTotalsAndAdministratorUserIdsInPeriod]                     
                    
                    unInforme[ 'rank_admin_user_ids_by_periods'][ aPeriodKey] = someSortedAdministratorUserIdsInPeriod
                
             
                    
                    
                    
                    
                    
                # #######################################
                """Loop through all languages, collecting from each language the number of contributions and id for each non-administrator user, and each administrator, to be ranked later by the number of their contributions.
                
                """
                for unCodigoIdioma in unInforme[ 'contributions_by_language'].keys():
                    
                    # #######################################
                    """Collect from one language the number of contributions and id for each non-administrator user, and each administrator, to be ranked later by the number of their contributions.
                    
                    """

                    unInformeIdioma = unInforme[ 'contributions_by_language'][ unCodigoIdioma]
                                        
                    someLanguageTotalsAndUserIdsDict                     = { }
                    someLanguagePeriodsTotalsAndUserIdsDict              = dict( [ [ aPeriodKey, { }, ] for  aPeriodKey in cTRAContribucionesReport_Periods])
                    someLanguageTotalsAndAdministratorUserIdsDict        = { }
                    someLanguagePeriodsTotalsAndAdministratorUserIdsDict = dict( [ [ aPeriodKey, { }, ] for  aPeriodKey in cTRAContribucionesReport_Periods])
                    
                    for aPeriodKey in cTRAContribucionesReport_Periods:
                        
                        unasContributionsByUsers = unInformeIdioma[ 'contributions_by_periods'][ aPeriodKey]
                        
                        for aUserId in unasContributionsByUsers.keys():
                            
                                            
                            if not ( aUserId in unosUsuariosAdministradores):
                                
                                aUserContributions = unasContributionsByUsers.get( aUserId, {})
                                if aUserContributions:
                                    
                                    if aUserContributions.get( 'total_contributions', 0):
                                        
                                        someLanguageTotalsAndUserIdsDict[ aUserId] = someLanguageTotalsAndUserIdsDict.get( aUserId, 0) + aUserContributions.get( 'total_contributions', 0)
                                                                                
                                        someLanguagePeriodsTotalsAndUserIdsDict[ aPeriodKey][ aUserId] = someLanguagePeriodsTotalsAndUserIdsDict[ aPeriodKey].get( aUserId, 0) + aUserContributions.get( 'total_contributions', 0)
                            
                                                    
                                                    
                            else:                               
                                aUserContributions = unasContributionsByUsers.get( aUserId, {})
                                if aUserContributions:
                                    
                                    if aUserContributions.get( 'total_contributions', 0):
                                        
                                        someLanguageTotalsAndAdministratorUserIdsDict[ aUserId] = someLanguageTotalsAndAdministratorUserIdsDict.get( aUserId, 0) + aUserContributions.get( 'total_contributions', 0)
                                                                                
                                        someLanguagePeriodsTotalsAndAdministratorUserIdsDict[ aPeriodKey][ aUserId] = someLanguagePeriodsTotalsAndAdministratorUserIdsDict[ aPeriodKey].get( aUserId, 0) + aUserContributions.get( 'total_contributions', 0)
                      
                                       
                                      
                                        
                                        
                    # #######################################
                    """Build from the info collected above, the arrays with number of contributions and user ids, to be sorted (ranked).
                    
                    """
                                        
                    someLanguageTotalsAndUserIds                     = [ [ someLanguageTotalsAndUserIdsDict[ aUserId], aUserId,] for aUserId in someLanguageTotalsAndUserIdsDict.keys()]
                    someLanguagePeriodsTotalsAndUserIds              = dict( [ [ aPeriodKey, [ ], ] for  aPeriodKey in cTRAContribucionesReport_Periods])
                    for  aPeriodKey in cTRAContribucionesReport_Periods:
                        someLanguagePeriodsTotalsAndUserIds[ aPeriodKey] = [ [ someLanguagePeriodsTotalsAndUserIdsDict[ aPeriodKey][ aUserId], aUserId,] for aUserId in someLanguagePeriodsTotalsAndUserIdsDict[ aPeriodKey].keys()]
                    
                        
                        
                    someLanguageTotalsAndAdministratorUserIds        = [ [ someLanguageTotalsAndAdministratorUserIdsDict[ aUserId], aUserId,] for aUserId in someLanguageTotalsAndAdministratorUserIdsDict.keys()]
                    someLanguagePeriodsTotalsAndAdministratorUserIds = dict( [ [ aPeriodKey, [ ], ] for  aPeriodKey in cTRAContribucionesReport_Periods])
                    for  aPeriodKey in cTRAContribucionesReport_Periods:
                        someLanguagePeriodsTotalsAndAdministratorUserIds[ aPeriodKey] = [ [ someLanguagePeriodsTotalsAndAdministratorUserIdsDict[ aPeriodKey][ aUserId], aUserId,] for aUserId in someLanguagePeriodsTotalsAndAdministratorUserIdsDict[ aPeriodKey].keys()]
                                        
                                            
                                   
                        
                        
                    # #######################################
                    """Rank changes in all languages by administrator and non-administrator users according to the number of their contributions.
                    
                    """
                    someSortedLanguageTotalsAndUserIds = sorted( someLanguageTotalsAndUserIds, lambda aCountAndId, otherCountAndId: cmp( aCountAndId[ 0], otherCountAndId[ 0]), reverse=True,)
                    someSortedLanguageTotalsUserIds = [ aCountAndId[ 1] for aCountAndId in someSortedLanguageTotalsAndUserIds]
    
                    unInformeIdioma[ 'rank_user_ids_total'] = someSortedLanguageTotalsUserIds
                    
                    
                    someSortedLanguageTotalsAndAdministratorUserIds = sorted( someLanguageTotalsAndAdministratorUserIds, lambda aCountAndId, otherCountAndId: cmp( aCountAndId[ 0], otherCountAndId[ 0]), reverse=True,)
                    someSortedLanguageTotalsAdministratorUserIds = [ aCountAndId[ 1] for aCountAndId in someSortedLanguageTotalsAndAdministratorUserIds]
    
                    unInformeIdioma[ 'rank_admin_user_ids_total'] = someSortedLanguageTotalsAdministratorUserIds
                    
    
                    
                    for  aPeriodKey in cTRAContribucionesReport_Periods:
                                                
                        someLanguageTotalsAndUserIdsInPeriod = someLanguagePeriodsTotalsAndUserIds[ aPeriodKey]                         
                        someSortedLanguageTotalsAndUserIdsInPeriod = sorted( someLanguageTotalsAndUserIdsInPeriod, lambda aCountAndId, otherCountAndId: cmp( aCountAndId[ 0], otherCountAndId[ 0]), reverse=True,)
                        someSortedLanguageUserIdsInPeriod = [ aCountAndId[ 1] for aCountAndId in someSortedLanguageTotalsAndUserIdsInPeriod]                     
                        unInformeIdioma[ 'rank_user_ids_by_periods'][ aPeriodKey] = someSortedLanguageUserIdsInPeriod
                    
                        someLanguageTotalsAndAdministratorUserIdsInPeriod = someLanguagePeriodsTotalsAndAdministratorUserIds[ aPeriodKey]                         
                        someSortedLanguageTotalsAndAdministratorUserIdsInPeriod = sorted( someLanguageTotalsAndAdministratorUserIdsInPeriod, lambda aCountAndId, otherCountAndId: cmp( aCountAndId[ 0], otherCountAndId[ 0]), reverse=True,)
                        someSortedLanguageAdministratorUserIdsInPeriod = [ aCountAndId[ 1] for aCountAndId in someSortedLanguageTotalsAndAdministratorUserIdsInPeriod]                     
                        
                        unInformeIdioma[ 'rank_admin_user_ids_by_periods'][ aPeriodKey] = someSortedLanguageAdministratorUserIdsInPeriod
                    
                                         
                        
                        
                # #######################################
                """Retrieve information about the members.
                
                """
                aModelDDvlPloneTool = self.fModelDDvlPloneTool()
                
                if not( aModelDDvlPloneTool == None):        
                    
                    unasContributionsByUsers = unInforme[ 'contributions_by_user']
                    someUserIds              = unasContributionsByUsers.keys()
                    
                    for aUserId in someUserIds:
                        aMemberInfo = aModelDDvlPloneTool.fGetMemberInfoForUserId( self, aUserId)
                        if aMemberInfo:
                            unInforme[ 'users_member_info'][ aUserId] = aMemberInfo
                    
                
                        
                        
                                            
                # #######################################
                """Report sucessfully completed.
                
                """
                unInforme[ 'report_date'] = self.fDateTimeNowString()   
                unInforme[ 'success'] = True
                
                                
                return unInforme

            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))

                unInformeExcepcion = 'Exception during fElaborarInformeContribuciones\n' 
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

            
            
            
            
            

    security.declareProtected( permissions.View, 'pAcumularContribucionDeUsuario')
    def pAcumularContribucionDeUsuario(self, 
        theProcessControlManager           =None,
        theInforme                         =None, 
        theCodigoIdioma                    =None,
        theUsuario                         =None, 
        theFecha                           =None,
        theModoContribucion                =None,):
        
        
        if theProcessControlManager == None:
            return self
        
        if theInforme == None:
            return self
        
        if not theCodigoIdioma:
            return self
        
        if not ( theUsuario and theFecha):
            return self
        
        if not theModoContribucion:
            return self
        
        if not ( theModoContribucion in cTRAContribucion_Modos):
            return self
        
        
        
        
        

        # #############################################################
        """Determine periods to accumulate into.
    
        """          
        somePeriodsToAccumulateInto = [ ]
        
        for aPeriodKey in cTRAContribucionesReport_Periods:
            if ( theFecha >= theInforme[ 'periods_dates'][ aPeriodKey][ 0]) and \
               ( theFecha <= theInforme[ 'periods_dates'][ aPeriodKey][ 1]):
                somePeriodsToAccumulateInto.append( aPeriodKey)
        
                
                
        
        
        # ########################################           
        """Accumulate total of all contributions made on any periods in all languages by all users in all modes.
        
        """
        theInforme[ 'total_contributions'] += 1
        
        theInforme[ 'total_contributions_by_mode'][ theModoContribucion] += 1
        
        
        
        
        
        # ########################################           
        """Accumulate totals for specific periods in all languages by all users in all modes and for each mode.
        
        """
        for aPeriodKey in somePeriodsToAccumulateInto:
            theInforme[ 'periods_totals'][ aPeriodKey][ 'total_contributions'] += 1
            theInforme[ 'periods_totals'][ aPeriodKey][ 'contributions_by_mode'][ theModoContribucion] += 1
        
            
            
            
            
        
        # ########################################           
        """Accumulate for the user totals in all languages, for each mode, and for each period totals and modes.
        
        """
        unasContribucionesTotalesUsuario = theInforme[ 'contributions_by_user'].get( theUsuario, None)
        if unasContribucionesTotalesUsuario == None:
            unasContribucionesTotalesUsuario = self.fNewVoidInformeContribucionesUsuario()
            theInforme[ 'contributions_by_user'][ theUsuario] = unasContribucionesTotalesUsuario
            theInforme[ 'alphabetical_user_ids'] = sorted( theInforme[ 'contributions_by_user'].keys())
            

            
        unasContribucionesTotalesUsuario[ 'total_contributions'] += 1
        unasContribucionesTotalesUsuario[ 'contributions_by_mode'][ theModoContribucion] += 1

        for aPeriodKey in somePeriodsToAccumulateInto:
            unasContribucionesTotalesUsuario[ 'contributions_by_periods'][ aPeriodKey][ 'total_contributions'] += 1
            unasContribucionesTotalesUsuario[ 'contributions_by_periods'][ aPeriodKey][ 'contributions_by_mode'][ theModoContribucion] += 1
            

            
            
        someContributedLanguages = unasContribucionesTotalesUsuario[ 'contributed_language_codes']
        if not ( theCodigoIdioma in someContributedLanguages):
            someContributedLanguages.append( theCodigoIdioma)
            unasContribucionesTotalesUsuario[ 'contributed_language_codes'] = sorted( someContributedLanguages)
        
            
            
            
            
        
        # ########################################           
        """Accumulate for translation language. Create structure if no results for language have been ellaborated yet.
        
        """
        unasContribucionesIdioma = theInforme[ 'contributions_by_language'].get( theCodigoIdioma, None)
        if unasContribucionesIdioma == None:
            unasContribucionesIdioma = self.fNewVoidInformeContribucionesIdioma()
            theInforme[ 'contributions_by_language'][ theCodigoIdioma] = unasContribucionesIdioma
        
        unasContribucionesIdioma[ 'total_contributions'] += 1
        unasContribucionesIdioma[ 'total_contributions_by_mode'][ theModoContribucion] += 1
        
        
        
        
        
        # ########################################           
        """Accumulate for the user in the translation language, for each mode, and for each period totals and modes.
        
        """
        unasContribucionesIdiomaUsuario = unasContribucionesIdioma[ 'contributions_by_user'].get( theUsuario, None)
        if unasContribucionesIdiomaUsuario == None:
            unasContribucionesIdiomaUsuario = self.fNewVoidInformeContribucionesUsuarioEnIdioma()
            unasContribucionesIdioma[ 'contributions_by_user'][ theUsuario] = unasContribucionesIdiomaUsuario

            
        unasContribucionesIdiomaUsuario[ 'total_contributions'] += 1
        unasContribucionesIdiomaUsuario[ 'contributions_by_mode'][ theModoContribucion] += 1

        
        for aPeriodKey in somePeriodsToAccumulateInto:
            unasContribucionesIdiomaUsuario[ 'contributions_by_periods'][ aPeriodKey][ 'total_contributions'] += 1
            unasContribucionesIdiomaUsuario[ 'contributions_by_periods'][ aPeriodKey][ 'contributions_by_mode'][ theModoContribucion] += 1
            
            
            
            
        
        # ########################################           
        """Accumulate totals for specific periods in current language by all users in all modes and for each mode.
        
        """
        for aPeriodKey in somePeriodsToAccumulateInto:
            
            unasContribucionesIdioma[ 'periods_totals'][ aPeriodKey][ 'total_contributions'] += 1
            unasContribucionesIdioma[ 'periods_totals'][ aPeriodKey][ 'contributions_by_mode'][ theModoContribucion] += 1
        
            
            
            
                
                
            # #############################################################
            """Accumulate number of contributions by periods.
        
            """  
            someContributionsByUsers = unasContribucionesIdioma[ 'contributions_by_periods'][ aPeriodKey]
        
        
            
            
            
            # ########################################           
            """Accumulate for user. Create structure if no results for user have been ellaborated yet.
            
            """
            unasContribucionesUsuario = someContributionsByUsers.get( theUsuario, None)
            if unasContribucionesUsuario == None:
                unasContribucionesUsuario = self.fNewVoidInformeContribucionesUsuarioEnPeriodo()
                someContributionsByUsers[ theUsuario] = unasContribucionesUsuario
                
                    
            unasContribucionesUsuario[ 'total_contributions'] += 1
             
            unasContribucionesUsuario[ 'contributions_by_mode'][ theModoContribucion] += 1

                
        
        return self
    
    
    
    
    
    
    
    
    

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
                
                unInforme[ 'startup_date']  = self.fStartupDateString()
                unInforme[ 'report_date']   = self.fDateTimeNowString()


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
                                        self.pAcumularActividadEnPeriodoInforme( anActivity, cActivityReport_Period_Last7Days, unInforme)
                                        
                                        
                                        
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

                        
                        
                # #############################################################
                """Retrieve last contributions report.
            
                """  
                  
                unaContribuciones = self.fObtenerUltimoContribuciones()
                if not ( unaContribuciones == None):
                    unInforme.update( {
                        'last_contributions_report_title': unaContribuciones.Title(),
                        'last_contributions_report_URL':   unaContribuciones.absolute_url(),
                    })     
                                            
                                        
                                    
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
            unaConfiguracion = self.fObtenerConfiguracion( cTRAConfiguracionAspecto_InvalidacionInformes)
            
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
            
    
    
    
    

       
    
    #security.declarePrivate( 'fInvalidateObsoleteContributionsReport')
    #def fInvalidateObsoleteContributionsReport(self, ):
        #"""If the Contributions Report is too old, or enough changes have been applied to translations in the catalog, invalidate the status report by languages for the catalog.
        
        #"""
                
        #aReport = self.fNewVoidReportInvalidateObsoleteStatusReports()
        
        #unPathDelRaiz = self.fPathDelRaiz()
        #if not unPathDelRaiz:
            #return aReport        
        #aReport[ 'path_del_raiz'] = unPathDelRaiz
        
        
        #unMustInvalidate              = False
        #unVoteMustInvalidateByNumbers = False
        #unVoteMustInvalidateByTime    = False
            
        #try:
            ## #################
            #"""MUTEX LOCK. 
            
            #"""
            ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #self.pAcquireGlobalsLock( )
            ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
                
                       
            ## ####################################################################
            #"""Check if the counter of changes since the last time the status report by languages was generated, is bigger than the maximum configured for the catalog. 
            
            #"""
            #unaConfiguracion = self.fObtenerConfiguracion( cTRAConfiguracionAspecto_InvalidacionInformes)
            
            #unNumeroDeCambiosAnularInformeIdiomas = 0
            #if not ( unaConfiguracion == None):
                #unNumeroDeCambiosAnularInformeIdiomas = unaConfiguracion.getNumeroDeCambiosAnularInformeIdiomas()
            #if not unNumeroDeCambiosAnularInformeIdiomas:
                #unNumeroDeCambiosAnularInformeIdiomas = 0
                
            #aReport[ 'changes_threshold'] = unNumeroDeCambiosAnularInformeIdiomas

            #if TRACatalogo_Globales.gNumTranslationsStatusChangesSinceContributionsReport == None:
                #TRACatalogo_Globales.gNumTranslationsStatusChangesSinceContributionsReport = { }
                
            #unNumTranslationsStatusChangesForRoot = TRACatalogo_Globales.gNumTranslationsStatusChangesSinceContributionsReport.get( unPathDelRaiz, None)
            #if unNumTranslationsStatusChangesForRoot == None:
                #unNumTranslationsStatusChangesForRoot = 0
                
            #aReport[ 'changes_recorded'] = unNumTranslationsStatusChangesForRoot
                
            #if unNumTranslationsStatusChangesForRoot >= unNumeroDeCambiosAnularInformeIdiomas:
                #unVoteMustInvalidateByNumbers = True
            
                        
                
                
                
            ## ####################################################################
            #"""Check if enough time has lapsed since the last time the user contributions report was generated. 
            
            #"""
            #unSegundosMinimosRetencionInformeIdiomas = 0
            #if not ( unaConfiguracion == None):
                #unaConfiguracion.getSegundosMinimosRetencionInformeIdiomas()
            #if not unSegundosMinimosRetencionInformeIdiomas:
                #unSegundosMinimosRetencionInformeIdiomas = 0
                
            #aReport[ 'seconds_threshold'] = unSegundosMinimosRetencionInformeIdiomas
                

            #if TRACatalogo_Globales.gContributionsReportTimeMillis == None:
                #TRACatalogo_Globales.gContributionsReportTimeMillis = { }
                
            #unStatusContributionsReportTimeMillis = TRACatalogo_Globales.gContributionsReportTimeMillis.get( unPathDelRaiz, None)
            #if unStatusContributionsReportTimeMillis == None:
                #unStatusContributionsReportTimeMillis = 0
                
            #unosMillisecondsNow = self.fMillisecondsNow()
            
            #unosSecondsLapsed =  int(( unosMillisecondsNow - unStatusContributionsReportTimeMillis) / 1000)
            #aReport[ 'seconds_lapsed'] = unosSecondsLapsed

            #if unosSecondsLapsed >= unSegundosMinimosRetencionInformeIdiomas:
                #unVoteMustInvalidateByTime = True
                
            
            #if unVoteMustInvalidateByNumbers:
                #unMustInvalidate = True
            #else:
                #if unVoteMustInvalidateByTime and unNumTranslationsStatusChangesForRoot:
                    #unMustInvalidate = True
                    
                
                
                
        #finally:
            ## #################
            #"""MUTEX UNLOCK. 
            
            #"""
            ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #self.pReleaseGlobalsLock( )
            ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            
            
        #if unMustInvalidate:
            #self.pFlushCachedTemplates( [ 'TRACatalogoContribuciones', 'TRACatalogoContribuciones_NoHeaderNoFooter',])
            #aReport[ 'invalidated'] = True
            
        #return aReport
            
    

    
    
        

    #security.declarePrivate( 'pContributionsReportJustGenerated')
    #def pContributionsReportJustGenerated(self, ):
        #"""Record the time now, and Reset the counter of changes since the report was generated.
        
        #"""
                
        #unPathDelRaiz = self.fPathDelRaiz()
        #if not unPathDelRaiz:
            #return self
        
        #unMustInvalidate = False
            
        #try:
            ## #################
            #"""MUTEX LOCK. 
            
            #"""
            ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #self.pAcquireGlobalsLock( )
            ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
                        
            ## ####################################################################
            #"""Record the current time as the status report generation time. 
            
            #"""
            #if TRACatalogo_Globales.gContributionsReportTimeMillis == None:
                #TRACatalogo_Globales.gContributionsReportTimeMillis = { }
                
            #unosMillisecondsNow = self.fMillisecondsNow()

            #TRACatalogo_Globales.gContributionsReportTimeMillis[ unPathDelRaiz] = unosMillisecondsNow
                 
                
                
                       
            ## ####################################################################
            #"""Reset the counter of changes since the status report was generated.
            
            #"""
              
            #if TRACatalogo_Globales.gNumTranslationsStatusChangesSinceContributionsReport == None:
                #TRACatalogo_Globales.gNumTranslationsStatusChangesSinceContributionsReport = { }
                
            #TRACatalogo_Globales.gNumTranslationsStatusChangesSinceContributionsReport[ unPathDelRaiz] = 0
                
        #finally:
            ## #################
            #"""MUTEX UNLOCK. 
            
            #"""
            ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #self.pReleaseGlobalsLock( )
            ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


        #return self
            
    
    
    
    
    
        
    

    
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
            unaConfiguracion = self.fObtenerConfiguracion( cTRAConfiguracionAspecto_InvalidacionInformes)
            
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
            unaConfiguracion = self.fObtenerConfiguracion( cTRAConfiguracionAspecto_InvalidacionInformes)
            
            unNumeroDeActividadesAnularInformeActividad = 0
            if not ( unaConfiguracion == None):
                unNumeroDeActividadesAnularInformeActividad = unaConfiguracion.fObtenerConfiguracion( cTRAConfiguracionAspecto_InvalidacionInformes).getNumeroDeActividadesAnularInformeActividad()
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
            
        