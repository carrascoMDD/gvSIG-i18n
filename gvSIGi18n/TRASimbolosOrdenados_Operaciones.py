# -*- coding: utf-8 -*-
#
# File: TRASimbolosOrdenados_Operaciones.py
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

from StringIO import StringIO


from Products.CMFCore       import permissions
from Products.CMFCore.utils  import getToolByName



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



##/code-section module-header



##code-section after-local-schema #fill in your manual code here



##/code-section after-local-schema



##code-section after-schema #fill in your manual code here


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


##/code-section after-schema

class TRASimbolosOrdenados_Operaciones:
    # #######################################################################
    """Cached sorted simbolos cadenas, and another cache grouped by module and also sorted by simbolo cadena
    
    """

    security = ClassSecurityInfo()

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    
    

    security.declarePrivate( '_fGetOrInitializeSimbolosCadenasOrdenados')
    def _fGetOrInitializeSimbolosCadenasOrdenados( self, theParentExecutionRecord=None):
        
        unTextoSimbolos = self.getSimbolosCadenasOrdenados()
        if unTextoSimbolos:
            unTextoSimbolos = unTextoSimbolos.strip()
            
        if not unTextoSimbolos:
            
            self._pInicializarModulosYSimbolosCadenasOrdenados( theParentExecutionRecord,)
            
            unTextoSimbolos = self.getSimbolosCadenasOrdenados()
            if unTextoSimbolos:
                unTextoSimbolos = unTextoSimbolos.strip()
            
        unosSimbolos = unTextoSimbolos.splitlines()
        if not unosSimbolos:
            return []
        
        return unosSimbolos
    
    

    security.declarePrivate( '_fGetOrInitializeModulosYSimbolosCadenasOrdenados')
    def _fGetOrInitializeModulosYSimbolosCadenasOrdenados( self, theParentExecutionRecord=None):
        
        unTextoModulosYSimbolos = self.getModulosYSimbolosCadenasOrdenados()
        if unTextoModulosYSimbolos:
            unTextoModulosYSimbolos = unTextoModulosYSimbolos.strip()
            
        if not unTextoModulosYSimbolos:
            
            self._pInicializarModulosYSimbolosCadenasOrdenados( theParentExecutionRecord,)

            unTextoModulosYSimbolos = self.getModulosYSimbolosCadenasOrdenados()
            if unTextoModulosYSimbolos:
                unTextoModulosYSimbolos = unTextoModulosYSimbolos.strip()
                
            
        unosModulosYSimbolos = unTextoModulosYSimbolos.splitlines()
        if not unosModulosYSimbolos:
            return []
        
        return unosModulosYSimbolos
    
            
    

    
    
        
    security.declarePrivate( '_pInicializarModulosYSimbolosCadenasOrdenados')
    def _pInicializarModulosYSimbolosCadenasOrdenados( self, theParentExecutionRecord=None, ):

        unExecutionRecord = self.fStartExecution( 'method',  'pInicializarModulosYSimbolosCadenasOrdenados', theParentExecutionRecord, False) 

        if cLogInicializarSimbolosCadenasOrdenados:
            unStartTime = self.fMillisecondsNow()
        
        try:
                
            unCatalogo = self.getCatalogo()
            if unCatalogo == None:
                return self
            
            
            unaBusqueda = cBusquedaTodasCadenasOrdenadasPorSimbolo.copy()
            
            unCatalogFiltroCadenas = unCatalogo.fCatalogFiltroCadenas()
            if ( unCatalogFiltroCadenas == None):
                return self
            unosDatosCadenas = unCatalogFiltroCadenas.searchResults( **unaBusqueda ) 
            
            if not unosDatosCadenas or len( unosDatosCadenas) < 1:
                self.setSimbolosCadenasOrdenados( '')
                self.setModulosYSimbolosCadenasOrdenados( '')
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
            
            
            
            self.setSimbolosCadenasOrdenados( unosSimbolosCadenasOrdenadosString)            
            self.setModulosYSimbolosCadenasOrdenados( unosModulosYSimbolosCadenasOrdenadosString)

        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

            if cLogInicializarSimbolosCadenasOrdenados:
                unEndTime = self.fMillisecondsNow()
                logging.getLogger( 'gvSIGi18n').info( 'pInicializarModulosYSimbolosCadenasOrdenados::TOTAL milliseconds=%d' % ( unEndTime - unStartTime))
        
        
        return self
            
    
        
        
        
    
    
    security.declareProtected( permissions.ModifyPortalContent, 'pInvalidateSimbolosCadenasOrdenados')    
    def pInvalidateSimbolosCadenasOrdenados( self):

        unTextoSimbolos = self.getSimbolosCadenasOrdenados()
        if unTextoSimbolos:
            self.setSimbolosCadenasOrdenados( '')

        unTextoModulosYSimbolos = self.getModulosYSimbolosCadenasOrdenados()
        if unTextoModulosYSimbolos:
            self.setModulosYSimbolosCadenasOrdenados( '')
                
        return self
            
    
    
    
    
 
    
    
    
    
    
    

    security.declarePrivate( 'fListaSimbolosCadenasOrdenados')
    def fListaSimbolosCadenasOrdenados( self,theParentExecutionRecord=None):
        
        unosSimbolos = self._fGetOrInitializeSimbolosCadenasOrdenados( theParentExecutionRecord=theParentExecutionRecord)
        
        return unosSimbolos
        
    
    
    
    
    
    
    
        
    security.declarePrivate( 'fListaSimbolosCadenasOrdenadosEnModulo')
    def fListaSimbolosCadenasOrdenadosEnModulo( self, theNombreModulo,  theParentExecutionRecord=None):
        if not theNombreModulo:
            return self.fListaSimbolosCadenasOrdenados( theParentExecutionRecord)

        unosModulosYSimbolos = self._fGetOrInitializeModulosYSimbolosCadenasOrdenados( theParentExecutionRecord=theParentExecutionRecord)
        if not unosModulosYSimbolos:
            return []
        
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
            
        unosSimbolos = self._fListaSimbolosCadenasEnVariosModulos( unosNombresModulos,  theParentExecutionRecord)        

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
            
        unosSimbolos = self._fListaSimbolosCadenasEnVariosModulos( unosNombresModulos,  theParentExecutionRecord)  
        if not unosSimbolos:
            return []
        
        return list( unosSimbolos)
    
   
        
    
    
    security.declarePrivate( '_fListaSimbolosCadenasEnVariosModulos')
    def _fListaSimbolosCadenasEnVariosModulos( self, theNombresModulos, theParentExecutionRecord=None):
        if not theNombresModulos:
            return self.fListaSimbolosCadenasOrdenados( theParentExecutionRecord)
        
        if len( theNombresModulos) == 1:
            return self.fListaSimbolosCadenasOrdenadosEnModulo( theNombresModulos[ 0], theParentExecutionRecord)
            
         
        unosModulosYSimbolos = self._fGetOrInitializeModulosYSimbolosCadenasOrdenados( theParentExecutionRecord=theParentExecutionRecord)
        if not unosModulosYSimbolos:
            return []
            
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    security.declarePrivate( 'pAllSubElements_into')    
    def pAllSubElements_into( self, theCollection, theAdditionalParams=None):
        if theCollection == None:
            return self
        theCollection.append( self)
        
        
        return self
            
    
    



    security.declarePrivate( 'pForAllElementsDo_recursive')    
    def pForAllElementsDo_recursive( self, theLambda=None, thePloneLambda=None,):
        if not theLambda:
            return self
        
        theLambda( self)
                
        if thePloneLambda:
            self.pForAllElementsPloneDo( thePloneLambda)
        
        return self
            
            
        
        
        

                             
    
    
    
                                

# end of class TRASimbolosOrdenados_Operaciones

##code-section module-footer #fill in your manual code here
##/code-section module-footer



