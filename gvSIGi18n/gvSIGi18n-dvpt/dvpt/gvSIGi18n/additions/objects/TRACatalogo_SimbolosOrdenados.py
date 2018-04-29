# -*- coding: utf-8 -*-
#
# File: TRACatalogo_SimbolosOrdenados.py
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

from logging import ERROR as cLoggingLevel_ERROR

import transaction

from StringIO                       import StringIO

from Acquisition                    import aq_get

from AccessControl                  import ClassSecurityInfo

from Products.CMFCore               import permissions

from Products.Archetypes.utils      import shasattr
from Products.Archetypes.public     import DisplayList

from Products.CMFCore.utils         import getToolByName


from TRAArquetipo import TRAArquetipo


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






cBusquedaTodasCadenasOrdenadasPorSimbolo = { 
        'getEstadoCadena':  cEstadoCadenaActiva, 
        'sort_on':          'getSimbolo',  
        'sort_order':       'ascending',
}           

cBusquedaCadenasInactivasOrdenadasPorSimbolo = { 
        'getEstadoCadena':  cEstadoCadenaInactiva, 
        'sort_on':          'getSimbolo',  
        'sort_order':       'ascending',
}           

cModuleStartLine = '===---==='       



  



class TRACatalogo_SimbolosOrdenados:
    """
    """
    security = ClassSecurityInfo()

    
    
    

    
    
    security.declareProtected( permissions.View, 'fObtenerElementoSimbolosOrdenados')
    def fObtenerElementoSimbolosOrdenados( self,):
        
        unElemento = self.getElementoPorID( cTRASimbolosOrdenados_Id)
        
        return unElemento
    
            
    
    
    
    
        
    
    
        
    # #######################################################################

    security.declarePrivate( 'fListaSimbolosCadenasInactivasOrdenados')
    def fListaSimbolosCadenasInactivasOrdenados( self,theParentExecutionRecord=None):
        """Simbolos cadenas in Inactive state,  not cached.
    
        """
        

        unExecutionRecord = self.fStartExecution( 'method',  'fListaSimbolosCadenasInactivasOrdenados', theParentExecutionRecord, False) 

        if cLogInicializarSimbolosCadenasOrdenados:
            unStartTime = self.fMillisecondsNow()
        
        try:
            unaBusqueda = cBusquedaCadenasInactivasOrdenadasPorSimbolo.copy()

            unCatalogBusquedaCadenas = self.fCatalogBusquedaCadenas()
            if ( unCatalogBusquedaCadenas == None):
                return self
            unosDatosCadenas = unCatalogBusquedaCadenas.searchResults( **unaBusqueda ) 
            
            if not unosDatosCadenas or len( unosDatosCadenas) < 1:
                return [ ]
            
            unosSimbolos = [ ]
            
            for unosDatosCadena in unosDatosCadenas:
                unSimbolo =  unosDatosCadena[ 'getSimbolo']
                if unSimbolo:
                    unosSimbolos.append( unSimbolo)
                    
            return unosSimbolos

        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()


    
    
            
            
            
            
            
            
        
    # #######################################################################
    """Cached sorted simbolos cadenas, and another cache grouped by module and also sorted by simbolo cadena
    
    """

     

    security.declarePrivate( 'fListaSimbolosCadenasOrdenados')
    def fListaSimbolosCadenasOrdenados( self,theParentExecutionRecord=None):
        
        unElementoSimbolosOrdenados = self.fObtenerElementoSimbolosOrdenados()
        if unElementoSimbolosOrdenados== None:
            return []
        
        unTextoSimbolos = unElementoSimbolosOrdenados.getSimbolosCadenasOrdenados().strip()
        if not unTextoSimbolos:
            self.pInicializarModulosYSimbolosCadenasOrdenados( theParentExecutionRecord, unElementoSimbolosOrdenados)
            unTextoSimbolos = unElementoSimbolosOrdenados.getSimbolosCadenasOrdenados().strip()
            
        unosSimbolos = unTextoSimbolos.splitlines()
        return unosSimbolos
        
    
    
    
    
    
        
    security.declarePrivate( 'fListaSimbolosCadenasOrdenadosEnModulo')
    def fListaSimbolosCadenasOrdenadosEnModulo( self, theNombreModulo,  theParentExecutionRecord=None):
        if not theNombreModulo:
            return self.fListaSimbolosCadenasOrdenados( theParentExecutionRecord)
         
        unElementoSimbolosOrdenados = self.fObtenerElementoSimbolosOrdenados()
        if unElementoSimbolosOrdenados== None:
            return []
        
        unTextoModulosYSimbolos = unElementoSimbolosOrdenados.getModulosYSimbolosCadenasOrdenados()
        if not unTextoModulosYSimbolos:
            self.pInicializarModulosYSimbolosCadenasOrdenados(  theParentExecutionRecord, unElementoSimbolosOrdenados)
            unTextoModulosYSimbolos = unElementoSimbolosOrdenados.getModulosYSimbolosCadenasOrdenados()
            
        unosModulosYSimbolos = unTextoModulosYSimbolos.splitlines()
        unNumeroLineas = len( unosModulosYSimbolos)
        if not unNumeroLineas:
            return []        
        
        unIndexBusqueda = 0
        while unIndexBusqueda < unNumeroLineas:
            unIndexModuleStartLine = -1
            try:
                unIndexModuleStartLine = unosModulosYSimbolos.index( cModuleStartLine, unIndexBusqueda)
            except:
                return []
            if unIndexModuleStartLine < 0:
                return []
            if unIndexModuleStartLine >= ( unNumeroLineas - 2):
                return []
            unNombreModulo = unosModulosYSimbolos[ unIndexModuleStartLine + 1]            
            if unNombreModulo and ( unNombreModulo == theNombreModulo):
                unSiguienteIndexModuleStartLine = -1
                try:
                    unSiguienteIndexModuleStartLine = unosModulosYSimbolos.index( cModuleStartLine, unIndexModuleStartLine + 2)
                except:
                    None
                if unSiguienteIndexModuleStartLine < 0:
                    unosSimbolos = unosModulosYSimbolos[ unIndexModuleStartLine + 2:]
                    return unosSimbolos
                else:                
                    unosSimbolos = unosModulosYSimbolos[ unIndexModuleStartLine + 2:unSiguienteIndexModuleStartLine]
                    return unosSimbolos
            else:
                unIndexBusqueda = unIndexModuleStartLine + 2    

        return []
    
    
    
    
    
    
    
    security.declarePrivate( 'fListaSimbolosCadenasOrdenadosEnVariosModulos')
    def fListaSimbolosCadenasOrdenadosEnVariosModulos( self, theNombresModulos,  theIncludeModuloNoEspecificado, theParentExecutionRecord=None):
        if ( not theNombresModulos) and ( not theIncludeModuloNoEspecificado):
            return self.fListaSimbolosCadenasOrdenados( theParentExecutionRecord)
        
        if ( len( theNombresModulos) == 1) and ( not theIncludeModuloNoEspecificado):
            return self.fListaSimbolosCadenasOrdenadosEnModulo( theNombresModulos[ 0], theParentExecutionRecord)
        
        if not theNombresModulos:
            return self.fListaSimbolosCadenasOrdenadosModuloNoEspecificado( theParentExecutionRecord)
            
        unosNombresModulos = theNombresModulos[:]
        if theIncludeModuloNoEspecificado:
            unosNombresModulos.append( cNombreModuloNoEspecificadoSentinel)
            
        unosSimbolos = self.fListaSimbolosCadenasEnVariosModulos( unosNombresModulos,  theParentExecutionRecord)        

        unosSimbolosOrdenados = sorted( unosSimbolos)
        
        return unosSimbolos
    
   
    
    
    
    
    security.declarePrivate( 'fListaSimbolosCadenasEnVariosModulosStrictly')
    def fListaSimbolosCadenasEnVariosModulosStrictly( self, theNombresModulos,  theIncludeModuloNoEspecificado, theParentExecutionRecord=None):
        if ( not theNombresModulos) and ( not theIncludeModuloNoEspecificado):
            return []
        
        if ( len( theNombresModulos) == 1) and ( not theIncludeModuloNoEspecificado):
            return self.fListaSimbolosCadenasOrdenadosEnModulo( theNombresModulos[ 0], theParentExecutionRecord)
        
        if not theNombresModulos:
            return self.fListaSimbolosCadenasOrdenadosModuloNoEspecificado( theParentExecutionRecord)
        
        unosNombresModulos = theNombresModulos[:]
        if theIncludeModuloNoEspecificado:
            unosNombresModulos.append( cNombreModuloNoEspecificadoSentinel)
            
        unosSimbolos = self.fListaSimbolosCadenasEnVariosModulos( unosNombresModulos,  theParentExecutionRecord)  
        if not unosSimbolos:
            return []
        
        return list( unosSimbolos)
    
   
        
    
    
    security.declarePrivate( 'fListaSimbolosCadenasEnVariosModulos')
    def fListaSimbolosCadenasEnVariosModulos( self, theNombresModulos, theParentExecutionRecord=None):
        if not theNombresModulos:
            return self.fListaSimbolosCadenasOrdenados( theParentExecutionRecord)
        
        if len( theNombresModulos) == 1:
            return self.fListaSimbolosCadenasOrdenadosEnModulo( theNombresModulos[ 0], theParentExecutionRecord)
            
         
        unElementoSimbolosOrdenados = self.fObtenerElementoSimbolosOrdenados()
        if unElementoSimbolosOrdenados== None:
            return []
        
        unTextoModulosYSimbolos = unElementoSimbolosOrdenados.getModulosYSimbolosCadenasOrdenados()
        if not unTextoModulosYSimbolos:
            
            self.pInicializarModulosYSimbolosCadenasOrdenados( theParentExecutionRecord, unElementoSimbolosOrdenados)

            unTextoModulosYSimbolos = unElementoSimbolosOrdenados.getModulosYSimbolosCadenasOrdenados()
            
        unosModulosYSimbolos = unTextoModulosYSimbolos.splitlines()
        unNumeroLineas = len( unosModulosYSimbolos)
        if not unNumeroLineas:
            return []
        
        todosSimbolos = set()
        
        for unNombreModulo in theNombresModulos:
            
            unIndexBusqueda = 0
            while unIndexBusqueda < unNumeroLineas:
                unIndexModuleStartLine = -1
                try:
                    unIndexModuleStartLine = unosModulosYSimbolos.index( cModuleStartLine, unIndexBusqueda)
                except:
                    break
                if unIndexModuleStartLine < 0:
                    break
                if unIndexModuleStartLine >= ( unNumeroLineas - 2):
                    break
                unNombreModuloHere = unosModulosYSimbolos[ unIndexModuleStartLine + 1]            
                if unNombreModuloHere and ( unNombreModuloHere == unNombreModulo):
                    unSiguienteIndexModuleStartLine = -1
                    try:
                        unSiguienteIndexModuleStartLine = unosModulosYSimbolos.index( cModuleStartLine, unIndexModuleStartLine + 2)
                    except:
                        None
                    if unSiguienteIndexModuleStartLine < 0:
                        todosSimbolos.update( unosModulosYSimbolos[ unIndexModuleStartLine + 2:])
                        break
                    else:                
                        todosSimbolos.update( unosModulosYSimbolos[ unIndexModuleStartLine + 2:unSiguienteIndexModuleStartLine])
                        break
                else:
                    unIndexBusqueda = unIndexModuleStartLine + 2    
        
        return todosSimbolos
    
    
    
    
    security.declarePrivate( 'fListaSimbolosCadenasOrdenadosModuloNoEspecificado')
    def fListaSimbolosCadenasOrdenadosModuloNoEspecificado( self,  theParentExecutionRecord=None):
        return self.fListaSimbolosCadenasOrdenadosEnModulo( cNombreModuloNoEspecificadoSentinel,  theParentExecutionRecord)
    

        
    security.declarePrivate( 'pInicializarModulosYSimbolosCadenasOrdenados')
    def pInicializarModulosYSimbolosCadenasOrdenados( self, theParentExecutionRecord=None, theElementoSimbolosOrdenados=None):

        unExecutionRecord = self.fStartExecution( 'method',  'pInicializarModulosYSimbolosCadenasOrdenados', theParentExecutionRecord, False) 

        if cLogInicializarSimbolosCadenasOrdenados:
            unStartTime = self.fMillisecondsNow()
        
        try:
            aElementoSimbolosOrdenados = theElementoSimbolosOrdenados
            if aElementoSimbolosOrdenados == None:
                aElementoSimbolosOrdenados = self.fObtenerElementoSimbolosOrdenados()
                
            unaBusqueda = cBusquedaTodasCadenasOrdenadasPorSimbolo.copy()
            
            unCatalogFiltroCadenas = self.fCatalogFiltroCadenas()
            if ( unCatalogFiltroCadenas == None):
                return self
            unosDatosCadenas = unCatalogFiltroCadenas.searchResults( **unaBusqueda ) 
            
            if not unosDatosCadenas or len( unosDatosCadenas) < 1:
                aElementoSimbolosOrdenados.setSimbolosCadenasOrdenados( '')
                aElementoSimbolosOrdenados.setModulosYSimbolosCadenasOrdenados( '')
                return self
            
            
            unosSimbolosCadenasOrdenadosString  = '\n'.join( [ unosDatosCadena[ 'getSimbolo'] for unosDatosCadena in unosDatosCadenas ])
            
            unosModulosYSimbolosDict         = {}
            unosSimbolosModuloNoEspecificado = []

            for unosDatosCadena in unosDatosCadenas:
                unSimbolo =  unosDatosCadena[ 'getSimbolo']
                
                unosNombresModulosString = unosDatosCadena[ 'getNombresModulos']
                unosNombresModulosString = unosNombresModulosString.strip()
                unosNombresModulosString = unosNombresModulosString.replace( '\n', cTRAModuleNameSeparator)
                unosNombresModulosString = unosNombresModulosString.replace( '\r', cTRAModuleNameSeparator)
                unosNombresModulosString = unosNombresModulosString.strip()
                if unosNombresModulosString:
                    unosNombresModulos = unosNombresModulosString.split( cTRAModuleNameSeparator)
                    if unosNombresModulos:
                        for unNombreModulo in unosNombresModulos:
                            if unNombreModulo:
                                unosSimbolosModulo = unosModulosYSimbolosDict.get( unNombreModulo, None)
                                if not unosSimbolosModulo:
                                    unosModulosYSimbolosDict[ unNombreModulo] = [ unSimbolo,]
                                else:
                                    unosSimbolosModulo.append( unSimbolo)
                else:
                    unosSimbolosModuloNoEspecificado.append( unSimbolo)
    
            todosNombresModulos = unosModulosYSimbolosDict.keys()
            todosNombresModulosOrdenados = sorted( todosNombresModulos)
            
            anOutput = StringIO()

            if unosSimbolosModuloNoEspecificado:
                anOutput.write( '%s\n%s\n%s\n' % ( cModuleStartLine, cNombreModuloNoEspecificadoSentinel, '\n'.join( unosSimbolosModuloNoEspecificado), ))
            else:
                anOutput.write( '%s\n%s\n' % ( cModuleStartLine, cNombreModuloNoEspecificadoSentinel, ))
            
            for unNombreModulo in todosNombresModulosOrdenados:
                unosSimbolosModulo = unosModulosYSimbolosDict[ unNombreModulo]
                if unosSimbolosModulo:
                    anOutput.write( '%s\n%s\n%s\n' % ( cModuleStartLine, unNombreModulo, '\n'.join( unosSimbolosModulo), ))
                else:
                    anOutput.write( '%s\n%s\n' % ( cModuleStartLine, unNombreModulo,  ))
                    
                
            unosModulosYSimbolosCadenasOrdenadosString  = anOutput.getvalue()
            
            
            
            aElementoSimbolosOrdenados.setSimbolosCadenasOrdenados( unosSimbolosCadenasOrdenadosString)            
            aElementoSimbolosOrdenados.setModulosYSimbolosCadenasOrdenados( unosModulosYSimbolosCadenasOrdenadosString)

        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

            if cLogInicializarSimbolosCadenasOrdenados:
                unEndTime = self.fMillisecondsNow()
                logging.getLogger( 'gvSIGi18n').info( 'pInicializarModulosYSimbolosCadenasOrdenados::TOTAL milliseconds=%d' % ( unEndTime - unStartTime))
        
        
        return self
            
    
        
        
        
    
    
    security.declareProtected( permissions.ModifyPortalContent, 'pInvalidateSimbolosCadenasOrdenados')    
    def pInvalidateSimbolosCadenasOrdenados( self):
        unElementoSimbolosOrdenados = self.fObtenerElementoSimbolosOrdenados()
        if unElementoSimbolosOrdenados== None:
            return self

        unTextoSimbolos = unElementoSimbolosOrdenados.getSimbolosCadenasOrdenados().strip()
        if unTextoSimbolos:
            unElementoSimbolosOrdenados.setSimbolosCadenasOrdenados( '')

        unTextoModulosYSimbolos = unElementoSimbolosOrdenados.getModulosYSimbolosCadenasOrdenados().strip()
        if unTextoSimbolos:
            unElementoSimbolosOrdenados.setModulosYSimbolosCadenasOrdenados( '')
        return self
            
    
    
    

    
 