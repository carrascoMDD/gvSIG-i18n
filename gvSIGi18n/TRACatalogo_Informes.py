# -*- coding: utf-8 -*-
#
# File: Catalogo_operations.py
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


from TRAElemento_Constants import *

from TRAElemento_Permission_Definitions import cBoundObject, cUseCase_GenerateTRAInformeLanguages, cUseCase_GenerateTRAInformeModules


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
            'codigo_idioma_en_gvsig':           '',
            'codigo_internacional_idioma':      '',
            'url_idioma':                       '',
            'informes_estados':                 self.fNewVoidInformeTodosEstados(),
            'total_traducciones':               0,  # only used with modules report
            'list_contents_permission':         False,
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
    
        
    
    
    
            
            
            
            
      
    security.declarePublic( 'fInformeTitulosIdiomasConIdiomaReferenciaYModulosPermitidos')
    def fInformeTitulosIdiomasConIdiomaReferenciaYModulosPermitidos( self, 
        theUseCaseName, 
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None): 
        
        unExecutionRecord = self.fStartExecution( 'method',  'fInformeTitulosIdiomasConIdiomaReferenciaYModulosPermitidos', theParentExecutionRecord, False) 

        try:
            
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
            unInforme = self.fInformeTitulosIdiomasYModulosPermitidos(
                theUseCaseName, 
                thePermissionsCache     =unPermissionsCache, 
                theRolesCache           =unRolesCache, 
                theParentExecutionRecord=unExecutionRecord)
            
            if not unInforme:
                return self.fNewVoidInformeTitulosIdiomasYModulosPermitidos()
            
            unosInformesIdiomas = unInforme[ 'idiomas']
            for unInformeIdioma in unosInformesIdiomas:
                if unInformeIdioma:
                    unCodigoIdioma = unInformeIdioma.get( 'codigoIdiomaEnGvSIG', '')
                    if unCodigoIdioma:
                        unosCodigosYDisplayNamesReferencia = [ [ '', self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_sinIdiomaReferencia', 'No reference language-'),],]
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
        theUseCaseName, 
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None): 
        """Report the titles of all languages and modules for which the user has permission to involve in exercising theUseCaseName.
        
        Output Values of type string returned in unicode.
        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fInformeTitulosIdiomasYModulosPermitidos', theParentExecutionRecord, False) 

        try:
            unInforme = self.fNewVoidInformeTitulosIdiomasYModulosPermitidos()
            
            if not theUseCaseName:
                return unInforme
            
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
            
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

                unCodigoIdioma = unIdioma.getCodigoIdiomaEnGvSIG()
                
                unInformeIdioma = self.fNewVoidInformeTitulosIdioma()
                unInformeIdioma.update( {
                    'codigoIdiomaEnGvSIG':           self.fAsUnicode( unCodigoIdioma), 
                    'codigoInternacionalDeIdioma':   self.fAsUnicode( unIdioma.getCodigoInternacionalDeIdioma() or ''),
                    'nombreIdioma':                  self.fAsUnicode( unIdioma.Title() or ''),
                    'nombreNativoDeIdioma':          self.fAsUnicode( unIdioma.getNombreNativoDeIdioma() or ''),
                    'flag':                          self.fAsUnicode( unosLanguagesNamesAndFlagsPorCodigo.get( unCodigoIdioma, {}).get( 'flag', cTRAFlagIdiomaDesconocida)),
                    'codigo_idioma_referencia':         self.fAsUnicode( unIdioma.getCodigoIdiomaReferencia()),
                    'juego_caracteres_javaproperties':  self.fAsUnicode( unIdioma.getJuegoDeCaracteresParaJavaProperties()),
                    'juego_caracteres_po':              self.fAsUnicode( unIdioma.getJuegoDeCaracteresParaPO()),
                    'displayTitle':                 self.fAsUnicode( unIdioma.fDisplayTitleAsUnicode())
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
                      
                
                
                
                
       
            
            
                
            
            
            

    
    security.declarePrivate( 'fInformeAutoActualizable')
    def fInformeAutoActualizable(self):
        """Should the report updte itself automatically when a certain amount of time has lapsed since it was ellaborated ?.
        
        """
        unosInformes = self.fObtenerTodosInformes()
        if not unosInformes:
            return None
        
        for unInforme in unosInformes:
            if unInforme.getEsAutoActualizable():
                return unInforme
            
        return None
    
                        
                
            
                
   
    
    
    # #############################################################
    """Lazy report accessors

    """
    
    
    
    
     
    security.declarePrivate( 'fInformeIdiomas')
    def fInformeIdiomas(self,                     
        theForceEllaboration        =False, 
        theCheckPermissions         =False, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):
        """Lazy access the Languages report.
        
        If the report is auto-updating, and enough time has lapsed since the report was generated,
        then the report will be re-generated,
        
        Create report objects structure from the instance stored internally as the content of a string field.
        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fInformeIdiomas', theParentExecutionRecord, False) 
        
        try:
    
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache

            unInformeAutoActualizable = self.fInformeAutoActualizable()
            if unInformeAutoActualizable:
                unDummy = unInformeAutoActualizable.fAutoUpdateIfNeeded( 
                    theForceEllaboration        =theForceEllaboration, 
                    theCheckPermissions         =theCheckPermissions, 
                    thePermissionsCache         =unPermissionsCache, 
                    theRolesCache               =unRolesCache, 
                    theParentExecutionRecord    =unExecutionRecord
                )

            
            unUltimoInforme = self.getUltimoInforme()
            if not unUltimoInforme :
                return None
            
            return unUltimoInforme.fInformeIdiomas(
                theForceEllaboration        =theForceEllaboration, 
                theCheckPermissions         =theCheckPermissions, 
                thePermissionsCache         =unPermissionsCache, 
                theRolesCache               =unRolesCache, 
                theParentExecutionRecord    =unExecutionRecord            
            )
        
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
        
    
    
    
            
            
    
     
    security.declarePrivate( 'fInformeModulos')
    def fInformeModulos(self,
        theForceEllaboration        =False, 
        theCheckPermissions         =False, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):
        """Lazy access the Modules report.
        
        If the report is auto-updating, and enough time has lapsed since the report was generated,
        then the report will be re-generated,
        
        Create report objects structure from the instance stored internally as the content of a string field.
        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fInformeModulos', theParentExecutionRecord, False) 

        try:
    
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
            unInformeAutoActualizable = self.fInformeAutoActualizable()
            if unInformeAutoActualizable:
                unDummy = unInformeAutoActualizable.fAutoUpdateIfNeeded(
                    theForceEllaboration        =theForceEllaboration, 
                    theCheckPermissions         =theCheckPermissions, 
                    thePermissionsCache         =unPermissionsCache, 
                    theRolesCache               =unRolesCache, 
                    theParentExecutionRecord    =unExecutionRecord
                )
            
            unUltimoInforme = self.getUltimoInforme()
            if not unUltimoInforme :
                return None
            
            return unUltimoInforme.fInformeModulos(
                theForceEllaboration        =theForceEllaboration, 
                theCheckPermissions         =theCheckPermissions, 
                thePermissionsCache         =unPermissionsCache, 
                theRolesCache               =unRolesCache, 
                theParentExecutionRecord    =unExecutionRecord            
            )
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
        

                  
                

    
    
    
    
    
    
    
    
    
   
    
    
    # #############################################################
    """Ellaboration of reports by languages or modules

    """  
    

        
    security.declareProtected( permissions.View, 'fElaborarInformeIdiomas')
    def fElaborarInformeIdiomas(self, 
        theInformeIdiomasUseCaseQueryResult=None,
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
                
        
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                
                
                unUseCaseQueryResult = theInformeIdiomasUseCaseQueryResult
                if theCheckPermissions or not unUseCaseQueryResult or not ( unUseCaseQueryResult.get( 'use_case_name', '') == cUseCase_GenerateTRAInformeLanguages):
                    unUseCaseQueryResult = self.fUseCaseAssessment(  
                        theUseCaseName                  = cUseCase_GenerateTRAInformeLanguages, 
                        theElementsBindings             = { cBoundObject: self,}, 
                        theRulesToCollect               = [ 'languages', ],
                        thePermissionsCache             = unPermissionsCache, 
                        theRolesCache                   = unRolesCache, 
                        theParentExecutionRecord        = unExecutionRecord,
                    )
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    return unInforme
                
                unosLanguagesNamesAndFlagsPorCodigo = self.fLanguagesNamesAndFlagsPorCodigo()

                
                unosIdiomasAccesibles = unUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'languages', {}).get( 'accepted_final_objects', [])
                if not unosIdiomasAccesibles:
                    return unInforme
                
                unosIdiomasAccesiblesParaOrdenar = [ [ unIdioma.getCodigoIdiomaEnGvSIG(), unIdioma,] for unIdioma in unosIdiomasAccesibles]
                unosIdiomasAccesiblesOrdenados = sorted( unosIdiomasAccesiblesParaOrdenar, lambda unCodigoEIdioma, otroCodigoEIdioma: cmp( unCodigoEIdioma[ 0], otroCodigoEIdioma[ 0]))
                unosIdiomasAccesibles = [ unCodigoEIdioma[ 1] for unCodigoEIdioma in unosIdiomasAccesiblesOrdenados]
                
                unNumeroCadenas = self.fObtenerNumeroCadenas()
                unInforme[ 'numero_cadenas'] = unNumeroCadenas
        
                unosInformesIdiomas = unInforme[ 'informes_idiomas']
        
                for unIdioma in unosIdiomasAccesibles:                
                    unInformeIdioma = self.fNewVoidInformeIdioma()
                    unCodigoIdioma = unIdioma.getCodigoIdiomaEnGvSIG()
                    unInformeIdioma.update( {
                        'nombre_idioma':                unIdioma.Title(), 
                        'codigo_idioma_en_gvsig':       unIdioma.getCodigoIdiomaEnGvSIG(), 
                        'codigo_internacional_idioma':  unIdioma.getCodigoInternacionalDeIdioma(),
                        'nombre_nativo_idioma':         unIdioma.getNombreNativoDeIdioma(),
                        'flag':                         unosLanguagesNamesAndFlagsPorCodigo.get( unCodigoIdioma, {}).get( 'flag', 'tra_flag-ninguna.gif'),
                        'url_idioma':                   unIdioma.absolute_url(), 
                      } )       
                    unosInformesIdiomas.append( unInformeIdioma)
        
        
                if not unNumeroCadenas:
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
                        
                        unaBusqueda = {   'getEstadoTraduccion' :     unEstado, }
                        
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
                        someInformesEstadoCasiUnoPorCiento = [ unInformeEstado for unInformeEstado in unosInformesEstados if ( unInformeEstado[ 'cantidad'] > 0)  and ( unInformeEstado[ 'porcentaje'] < 1) ]
                        someSortedInformesEstadoCasiUnoPorCiento = sorted( someInformesEstadoCasiUnoPorCiento, cmp=lambda unInformeEstado, otroInformeEstado: cmp(  unInformeEstado[ 'cantidad'], otroInformeEstado[ 'cantidad']), reverse=True)
               
                        for unInformeEstado in someSortedInformesEstadoCasiUnoPorCiento:
                            if aDifference > 0:
                                unInformeEstado[ 'porcentaje'] = 1
                                aDifference -= 1   
                
                        if aDifference > 0:
                            someSortedInformesEstado = sorted( unosInformesEstados, cmp=lambda unInformeEstado, otroInformeEstado: cmp(  unInformeEstado[ 'cantidad'], otroInformeEstado[ 'cantidad']), reverse=True)
                            for unInformeEstado in someSortedInformesEstado:
                                unInformeEstado[ 'porcentaje'] += 1
                                aDifference -= 1   
                                if aDifference == 0:
                                    break                       
                    
                return unInforme

            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fElaborarInformeIdiomas\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
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
        theInformeModulosUseCaseQueryResult=None,
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
    
                unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
                unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
                
                unUseCaseQueryResult = theInformeModulosUseCaseQueryResult
                if not unUseCaseQueryResult or not ( unUseCaseQueryResult.get( 'use_case_name', '') == cUseCase_GenerateTRAInformeModules):
                    unUseCaseQueryResult = self.fUseCaseAssessment(  
                        theUseCaseName          = cUseCase_GenerateTRAInformeModules, 
                        theElementsBindings     = { cBoundObject: self,},
                        theRulesToCollect       = [ 'languages', 'modules',], 
                        thePermissionsCache     = unPermissionsCache, 
                        theRolesCache           = unRolesCache, 
                        theParentExecutionRecord= unExecutionRecord
                    ) 
                    
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    return unInforme
                
                
                unosIdiomasAccesibles = unUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'languages', {}).get( 'accepted_final_objects', [])
                if not unosIdiomasAccesibles:
                    return unInforme
                unosModulosAccesibles = unUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'modules', {}).get( 'accepted_final_objects', [])
                if not unosModulosAccesibles:
                    return unInforme
                
                unasCabecerasIdiomas    = unInforme[ 'cabeceras_idiomas']        
                unosInformesModulos     = unInforme[ 'informes_modulos']        
                
                for unIdioma in unosIdiomasAccesibles:
                        
                    unaCabeceraIdioma = self.fNewVoidCabeceraIdioma()
                    unaCabeceraIdioma.update( {
                        'nombre_idioma':    unIdioma.Title(), 
                        'url_idioma':       unIdioma.absolute_url(), 
                        'codigo_idioma_en_gvsig':       unIdioma.getCodigoIdiomaEnGvSIG(),
                        'codigo_internacional_idioma':  unIdioma.getCodigoInternacionalDeIdioma(),
                    })
                    unasCabecerasIdiomas.append( unaCabeceraIdioma)
                        
                    
                 
                unNumeroCadenas = self.fObtenerNumeroCadenas()
                unInforme[ 'numero_cadenas'] =  unNumeroCadenas
                    
                    
                for unModulo in unosModulosAccesibles:
                    
                    unNombreModulo = unModulo.Title()
        
                    unInformeModulo = self.fNewVoidInformeModulo()
                    unInformeModulo[ 'nombre_modulo'] = unNombreModulo
                    unosInformesModulos.append( unInformeModulo)
            
                    unosInformesIdiomas = unInformeModulo[ 'informes_idiomas']
                                    
                    for unIndexIdioma in range( len( unosIdiomasAccesibles)):
                        unIdioma = unosIdiomasAccesibles[ unIndexIdioma]
                        unInformeIdioma = self.fNewVoidInformeIdioma()
                        unInformeIdioma.update( {
                            'nombre_idioma':                unIdioma.Title(), 
                            'codigo_idioma_en_gvsig':       unIdioma.getCodigoIdiomaEnGvSIG(), 
                            'codigo_internacional_idioma':  unIdioma.getCodigoInternacionalDeIdioma(),
                            'url_idioma':                   unIdioma.absolute_url(), 
                            'list_contents_permission':     True,
                          } )
                        unosInformesIdiomas.append( unInformeIdioma)
                         
                    
                    
                    if unNumeroCadenas:      
                        unosCatalogosParaIdioma = [ None,] * len( unosIdiomasAccesibles)   
                        for unIndexIdioma in range( len( unosIdiomasAccesibles)):
                            unIdioma = unosIdiomasAccesibles[ unIndexIdioma]
                            unosCatalogosParaIdioma[ unIndexIdioma] = self.getCatalogo().fCatalogBusquedaTraduccionesParaIdioma( unIdioma)
                        
                        unosSimbolosCadenasEnModulo = self.fListaSimbolosCadenasOrdenadosEnModulo( unModulo.Title(), unExecutionRecord)
                        unNumeroCadenasEnModulo = len( unosSimbolosCadenasEnModulo)
                        if unNumeroCadenasEnModulo:
            
                            unInformeModulo[ 'numero_cadenas'] = unNumeroCadenasEnModulo
                            
                                     
                            for unIndexIdioma in range( len( unosInformesIdiomas)):
                                
                                unInformeIdioma                 = unosInformesIdiomas[ unIndexIdioma]
                                unCodigoIdiomaEnGvSIG           = unInformeIdioma[ 'codigo_idioma_en_gvsig']
    
                                unCatalogBusquedaTraducciones   = unosCatalogosParaIdioma[ unIndexIdioma]
                                
                                if unCodigoIdiomaEnGvSIG and unCatalogBusquedaTraducciones:
                                    
                                    unTotalTraduccionesEnIdioma = 0            
                
                                    for unIndexEstado in range( len( cTodosEstados)):
                                        unEstado = cTodosEstados[ unIndexEstado]
                                        unaBusqueda = { 
                                            'getEstadoTraduccion' :     unEstado, 
                                            'getSimbolo':               unosSimbolosCadenasEnModulo,
                                        }
                                        unosResultadosBusqueda = unCatalogBusquedaTraducciones.searchResults(**unaBusqueda)
                                        unNumeroResultados = len( unosResultadosBusqueda)
                                        
                                        unInformeIdioma[ 'informes_estados'][ unIndexEstado][ 'cantidad'] = unNumeroResultados
                                        unInformeIdioma[ 'total_traducciones' ] += unNumeroResultados
                                        
                                        unInformeModulo[ 'totales_estados'][ unIndexEstado][ 'cantidad'] += unNumeroResultados
                                        unInformeModulo[ 'total_traducciones'] += unNumeroResultados
            
                                        unInforme[ 'totales_estados'][ unIndexEstado][ 'cantidad'] += unNumeroResultados
                                        unInforme[ 'total_traducciones' ] += unNumeroResultados
            
                                        unasCabecerasIdiomas[ unIndexIdioma][ 'totales_estados'][ unIndexEstado][ 'cantidad']  += unNumeroResultados
                                        unasCabecerasIdiomas[ unIndexIdioma][ 'numero_cadenas'] += unNumeroResultados
                                
                     
                unInforme[ 'report_date'] = self.fDateTimeNowString()                        
                return unInforme

            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fElaborarInformeModulos\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
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
     
    
                
                
                

    
        
 