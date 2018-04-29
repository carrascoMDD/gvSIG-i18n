# -*- coding: utf-8 -*-
#
# File: TRACatalogo_Retrieval.py
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



from TRACatalogo_Inicializacion import cNombreCatalogoBusquedaCadenas, cNombreCatalogoFiltroCadenas, cNombreCatalogoTextoCadenas, cNombreCatalogoBusquedaTraducciones, cNombreCatalogoFiltroTraducciones, cNombreCatalogoTextoTraducciones



class TRACatalogo_Retrieval:
    """
    """
    security = ClassSecurityInfo()

    
        

    
        
    # ####################################
    """TRAIdioma accessors
    
    """

    
    security.declareProtected( permissions.View, 'fObtenerColeccionIdiomas')
    def fObtenerColeccionIdiomas( self, ):
   
        unasColecciones = self.fObjectValues( cNombreTipoTRAColeccionIdiomas) #
        if not unasColecciones:
            return None
        return unasColecciones[ 0]
         
  
    
    security.declareProtected( permissions.View, 'fObtenerTodasColeccionesIdiomas')
    def fObtenerTodasColeccionesIdiomas( self, ):
   
        unasColecciones = self.fObjectValues( cNombreTipoTRAColeccionIdiomas) #
        if not unasColecciones:
            return []
        return unasColecciones
                 
    
    

    
    security.declarePrivate( 'fObtenerTodosIdiomas')
    def fObtenerTodosIdiomas( self, ):
   
        unaColeccion = self.fObtenerColeccionIdiomas()
        if not unaColeccion:
            return []
        
        unosElementos= unaColeccion.fObjectValues( cNombreTipoTRAIdioma)  #
        return unosElementos
           
     


        

    security.declarePrivate( 'fObtenerTodosIdiomasOrdenados')
    def fObtenerTodosIdiomasOrdenados( self, ):
   
        unosIdiomas = self.fObtenerTodosIdiomas()
        unosCodigosEIdiomasAOrdenar = [ [ unIdioma.getCodigoIdiomaEnGvSIG(), unIdioma, ] for unIdioma in unosIdiomas ]
        
        unosCodigosEIdiomasOrdenados = sorted ( unosCodigosEIdiomasAOrdenar, lambda unCeI, otroCeI: cmp( unCeI[ 0], otroCeI[ 0]))
        unosIdiomasOrdenados = [ unCeI[ 1] for unCeI in unosCodigosEIdiomasOrdenados]
        return unosIdiomasOrdenados
           
     
    
    
    
    
         
        

    security.declareProtected( permissions.View, 'fTodosIdiomasVocabulary')
    def fTodosIdiomasVocabulary(self,):
        
        unDisplayList = DisplayList()
        
        unosCodigosYDisplayNames = self.fTodosIdiomasCodesAndDisplayNames()
        if not unosCodigosYDisplayNames:
            return unDisplayList
        
        for unCodigoIdioma, unDisplayName in unosCodigosYDisplayNames:
            unDisplayList.add( 
                unCodigoIdioma,
                unDisplayName,
                
            )      
        return unDisplayList
    
         
    

    
    
    
    security.declareProtected( permissions.View, 'fTodosIdiomasCodesAndDisplayNames')
    def fTodosIdiomasCodesAndDisplayNames(self,):
        
        unosCodesAndDisplayNames = []
        
        unosIdiomas = self.fObtenerTodosIdiomasOrdenados()
        if not unosIdiomas:
            return unosCodesAndDisplayNames
        
        for unIdioma in unosIdiomas:
            unosCodesAndDisplayNames.append( [ 
                self.fAsUnicode( unIdioma.getCodigoIdiomaEnGvSIG()),
                unIdioma.fDisplayTitleAsUnicode(),
            ])      
        return unosCodesAndDisplayNames
    
         
    
    
    
    
    
    security.declareProtected( permissions.View, 'fGetIdiomaPorCodigo')
    def fGetIdiomaPorCodigo( self, theCodigoIdioma, thePloneUtilsTool=None):
        
        if not theCodigoIdioma:
            return None    

        unaIdIdioma = self.fIdiomaIdDesdeCodigo( theCodigoIdioma, thePloneUtilsTool)
        if not unaIdIdioma:
            return None    
        
        unIdioma = self.fGetIdiomaPorId( unaIdIdioma)
        return unIdioma


    
    
    security.declarePrivate( 'fIdiomaIdDesdeCodigo')
    def fIdiomaIdDesdeCodigo( self, theCodigoIdioma, thePloneUtilsTool=None):
        
        if not theCodigoIdioma:
            return None    

        unaIdIdioma = theCodigoIdioma.lower()
        unaIdIdioma.replace(" ", "-")
        unaIdIdioma.replace(".", "-")
        unaIdIdioma.replace("/", "-")
        unaIdIdioma.replace("\\", "-")
        unaIdIdioma ='%s%s' % ( cIdiomaIdPrefix, unaIdIdioma)
        
        aPloneUtilsTool = thePloneUtilsTool
        if not aPloneUtilsTool:
            aPloneUtilsTool = self.getPloneUtilsToolForNormalizeString()                
        if aPloneUtilsTool:
            unaIdIdioma = aPloneUtilsTool.normalizeString( unaIdIdioma)
            if not aPloneUtilsTool.good_id( unaIdIdioma):
                someBadChars = aPloneUtilsTool.bad_chars( unaIdIdioma)
                for aChar in someBadChars:
                    unaIdIdioma = unaIdIdioma.replace( aChar, '-')
        
        return unaIdIdioma

     
    
    
    
       
    security.declareProtected( permissions.View, 'fGetIdiomaPorId')    
    def fGetIdiomaPorId(self, theID):

        if not theID:
            return None

        unaColeccion = self.fObtenerColeccionIdiomas( )
        if not unaColeccion:
            return None
        
        unIdioma = None
        try:
            unIdioma = unaColeccion[ theID]
        except:
            None
        return unIdioma    
   
    
    
    
    
    
    
    
        
    # ####################################
    """TRAModulo accessors
    
    """


    
    security.declareProtected( permissions.View, 'fObtenerColeccionModulos')
    def fObtenerColeccionModulos( self, ):
   
        unasColecciones = self.fObjectValues( cNombreTipoTRAColeccionModulos) #
        if not unasColecciones:
            return None
        return unasColecciones[ 0]
         
    
    security.declareProtected( permissions.View, 'fObtenerTodasColeccionesModulos')
    def fObtenerTodasColeccionesModulos( self, ):
   
        unasColecciones = self.fObjectValues( cNombreTipoTRAColeccionModulos) #
        if not unasColecciones:
            return []
        return unasColecciones
         
           

    security.declareProtected( permissions.View, 'fObtenerTodosModulos')
    def fObtenerTodosModulos( self, ):
   
        unaColeccion = self.fObtenerColeccionModulos()
        if not unaColeccion:
            return []
        
        unosElementos= unaColeccion.fObjectValues( cNombreTipoTRAModulo) #
        return unosElementos
           
     

    security.declareProtected( permissions.View, 'fTodosNombresModulos')
    def fTodosNombresModulos( self, ):
        
        someModulos = self.fObtenerTodosModulos()
        if not someModulos:
            return []
        
        someNombresModulos = [ unModulo.Title() for unModulo in someModulos]
        return someNombresModulos
    
    
  

       
    
    security.declareProtected( permissions.View, 'fGetModuloPorNombre')
    def fGetModuloPorNombre( self, theNombreModulo, thePloneUtilsTool=None):
        
        if not theNombreModulo:
            return None    

        unaIdModulo = self.fModuloIdDesdeNombre( theNombreModulo, thePloneUtilsTool)
        if not unaIdModulo:
            return None    
        
        unModulo = self.fGetModuloPorId( unaIdModulo)
        return unModulo


    
    
    security.declarePrivate( 'fModuloIdDesdeNombre')
    def fModuloIdDesdeNombre( self, theNombreModulo, thePloneUtilsTool=None):
        
        if not theNombreModulo:
            return None    

        unaIdModulo = theNombreModulo.lower()
        unaIdModulo.replace(" ", "-")
        unaIdModulo.replace(".", "-")
        unaIdModulo.replace("/", "-")
        unaIdModulo.replace("\\", "-")
        unaIdModulo ='%s%s' % ( cModuloIdPrefix, unaIdModulo)
        
        aPloneUtilsTool = thePloneUtilsTool
        if not aPloneUtilsTool:
            aPloneUtilsTool = self.getPloneUtilsToolForNormalizeString()     
            
        if aPloneUtilsTool:
            unaIdModulo = aPloneUtilsTool.normalizeString( unaIdModulo)
            if not aPloneUtilsTool.good_id( unaIdModulo):
                someBadChars = aPloneUtilsTool.bad_chars( unaIdModulo)
                for aChar in someBadChars:
                    unaIdModulo = unaIdModulo.replace( aChar, '-')
        
        return unaIdModulo

    
    
        

    security.declareProtected( permissions.View, 'fGetModuloPorId')
    def fGetModuloPorId( self, theModuloId):

        if not theModuloId:
            return None    

        unaColeccionModulos = self.fObtenerColeccionModulos()
        if not unaColeccionModulos:
            return None
        
        unModulo = None
        try:
            unModulo = unaColeccionModulos[ theModuloId] 
        except:
            None
        return unModulo
  

    
    
    
    
    
    
         

    security.declareProtected( permissions.View, 'fTodosModulosVocabulary')
    def fTodosModulosVocabulary(self,):
        
        unDisplayList = DisplayList()
        
        unDisplayList.add( 
            '',
            self.fTranslateI18N(  'gvSIGi18n', cNombreModuloNoEspecificadoLabel_MsgId, cNombreModuloNoEspecificadoInputValue),
        )      
        
        unosNombresModulos = self.fTodosNombresModulos()
        if not unosNombresModulos:
            return unDisplayList
        
        for unNombreModulo in unosNombresModulos:
            unDisplayList.add( 
                unNombreModulo,
                unNombreModulo,
            )      
        return unDisplayList
    
           
    
    

    
    # ####################################
    """TRAColeccionSolicitudesCadenas accessors
    
    """

                    
    security.declareProtected( permissions.View, 'fObtenerColeccionSolicitudesCadenas')
    def fObtenerColeccionSolicitudesCadenas( self, ):
   
        unasColecciones = self.fObjectValues( cNombreTipoTRAColeccionSolicitudesCadenas)
        if not unasColecciones:
            return None
        return unasColecciones[ 0]
         
    
    
    
    
    security.declareProtected( permissions.View, 'fObtenerTodasColeccionesSolicitudesCadenas')
    def fObtenerTodasColeccionesSolicitudesCadenas( self, ):
   
        unasColecciones = self.fObjectValues( cNombreTipoTRAColeccionSolicitudesCadenas)
        if not unasColecciones:
            return []
        return unasColecciones
         
    
        
    # ####################################
    """TRAColeccionCadenas accessors
    
    """

        
    security.declareProtected( permissions.View, 'fObtenerColeccionCadenas')
    def fObtenerColeccionCadenas( self, ):
   
        unasColecciones = self.fObjectValues( cNombreTipoTRAColeccionCadenas)
        if not unasColecciones:
            return None
        return unasColecciones[ 0]
         
    
    
         
    security.declareProtected( permissions.View, 'fObtenerTodasColeccionesCadenas')
    def fObtenerTodasColeccionesCadenas( self, ):
   
        unasColecciones = self.fObjectValues( cNombreTipoTRAColeccionCadenas)
        if not unasColecciones:
            return []
        return unasColecciones
    
    
    
    

    
    
    security.declareProtected( permissions.View, 'fObtenerSimbolosTodasCadenasSinOrdenar')    
    def fObtenerSimbolosTodasCadenasSinOrdenar(self):
        unCatalog = self.fCatalogBusquedaCadenas()
        if ( unCatalog == None):
            return []
        unaBusqueda = { 
            'getEstadoCadena': cEstadoCadenaActiva,
        }
        unosResultadosBusqueda = unCatalog.searchResults( **unaBusqueda)
        unosSimbolos = [ unResultado[ 'getSimbolo'] for unResultado in unosResultadosBusqueda]
        return unosSimbolos 
    


    security.declareProtected( permissions.View, 'fObtenerNumeroCadenas')    
    def fObtenerNumeroCadenas( self):
        unCatalog = self.fCatalogBusquedaCadenas()
        if ( unCatalog == None):
            return 0
        unaBusqueda = { 
            'getEstadoCadena': cEstadoCadenaActiva,
        }
        unosResultadosBusqueda = unCatalog.searchResults( **unaBusqueda)
        return len( unosResultadosBusqueda)
     
    
    
        
    # ACV 20090404 was not used at the moment by anybody, 
    # but has been rewriten to use catalog search and avoid retrieving the collection contents    
    #security.declareProtected( permissions.View, 'getCadenaPorID')    
    #def getCadenaPorID(self, theID):
        #if not theID:
            #return None
        #unaColeccion = self.fObtenerColeccionCadenas()
        #unaCadena = None
        #try:
            #unaCadena = unaColeccion[ theID]
        #except:
            #None
        #return unaCadena    
            
    
        
        
    
    security.declareProtected( permissions.View, 'getCadenaPorID')    
    def getCadenaPorID(self, theID):
        if not theID:
            return None                   

        unCatalog = self.fCatalogBusquedaCadenas() 
        if ( unCatalog == None):
            return None
        unaBusqueda = { 
            'getId' :      theID,
        }
            
        unosResultadosBusqueda = unCatalog.searchResults(**unaBusqueda)
        if len( unosResultadosBusqueda) < 1:
            return None

        unaCadena = unosResultadosBusqueda[ 0].getObject() 
        return unaCadena

    
    
        
    security.declareProtected( permissions.View, 'fGetCadenaPorSimbolo')    
    def fGetCadenaPorSimbolo(self, theSimboloCadena):
        if not theSimboloCadena:
            return None                   

        unCatalog = self.fCatalogBusquedaCadenas() 
        if ( unCatalog == None):
            return None
        unaBusqueda = { 
            'getSimbolo' :      theSimboloCadena,
            'getEstadoCadena':  cEstadoCadenaActiva
        }
            
        unosResultadosBusqueda = unCatalog.searchResults(**unaBusqueda)
        if len( unosResultadosBusqueda) < 1:
            return None

        unaCadena = unosResultadosBusqueda[ 0].getObject() 
        return unaCadena
        
        

    
    
    
        
    security.declareProtected( permissions.View, 'fGetCadenaInactivaPorSimbolo')    
    def fGetCadenaInactivaPorSimbolo(self, theSimboloCadena):
        if not theSimboloCadena:
            return None                   

        unCatalog = self.fCatalogBusquedaCadenas() 
        if ( unCatalog == None):
            return None
        unaBusqueda = { 
            'getSimbolo' :      theSimboloCadena,
            'getEstadoCadena':  cEstadoCadenaInactiva
        }
            
        unosResultadosBusqueda = unCatalog.searchResults(**unaBusqueda)
        if len( unosResultadosBusqueda) < 1:
            return None

        unaCadena = unosResultadosBusqueda[ 0].getObject() 
        return unaCadena
                
    
    
    
    
            
    security.declarePrivate( 'getHighestCadenaIdNumber')    
    def getHighestCadenaIdNumber( self):
        
        unCatalog = self.fCatalogBusquedaCadenas() 
        if ( unCatalog == None):
            return 0
        unaBusqueda = {}
        unosResultadosBusqueda = unCatalog.searchResults(**unaBusqueda)
        if len( unosResultadosBusqueda) < 1:
            return 0
            
        unMaxIdNumber = 0
        for unResultadoBusqueda in unosResultadosBusqueda:
            unaId = unResultadoBusqueda.id
            if unaId.startswith( cCadenaIdPrefix):
                unNumberString = unaId[ len( cCadenaIdPrefix):]
                if len( unNumberString) > 0:
                    unNumber = 0
                    try:
                        unNumber = int( unNumberString)
                    except ValueError:
                        None
                    
                    if unNumber > unMaxIdNumber:
                        unMaxIdNumber = unNumber
        
        return unMaxIdNumber                        
    
 
    
    
    
    
    
    
    
    
    
    
        
    # ####################################
    """TRATraduccion accessors
    
    """

        
                     

    security.declareProtected( permissions.View, 'fObtenerDatosTodasTraduccionesAIdioma')    
    def fObtenerDatosTodasTraduccionesAIdioma(self, theCodigoIdioma):
        if not theCodigoIdioma:
            return []
        
        unIdioma = self.fGetIdiomaPorCodigo( theCodigoIdioma)
        if not unIdioma:
            return []
        aCatalog = self.fCatalogFiltroTraduccionesParaIdioma( unIdioma) 
        unaBusqueda = {}
        unosResultadosBusquedaTraducciones      = aCatalog.searchResults(**unaBusqueda)
        return unosResultadosBusquedaTraducciones    
      
  
    
   
    
    
    
    
    
    
    
    
           
    # ####################################
    """TRAInforme accessors
    
    """


     
    security.declareProtected( permissions.View, 'fObtenerColeccionInformes')
    def fObtenerColeccionInformes( self, ):
   
        unasColecciones = self.fObtenerTodasColeccionesInformes( ) #
        if not unasColecciones:
            return None
        return unasColecciones[ 0]
    


     
    security.declareProtected( permissions.View, 'fObtenerTodasColeccionesInformes')
    def fObtenerTodasColeccionesInformes( self, ):
   
        unasColecciones = self.fObjectValues( cNombreTipoTRAColeccionInformes) #
        if not unasColecciones:
            return []
        return unasColecciones
            

    security.declareProtected( permissions.View, 'fObtenerTodosInformes')
    def fObtenerTodosInformes( self, ):
   
        unaColeccion = self.fObtenerColeccionInformes()
        if not unaColeccion:
            return []
        
        unosElementos = unaColeccion.fObjectValues( cNombreTipoTRAInforme) #
        return unosElementos
           
     
    
   
           
    # ####################################
    """TRAProgreso accessors
    
    """    
    
    security.declareProtected( permissions.View, 'fObtenerColeccionProgresos')
    def fObtenerColeccionProgresos( self, ):
   
        unasColecciones = self.fObtenerTodasColeccionesProgresos( ) #
        if not unasColecciones:
            return None
        return unasColecciones[ 0]
    

    
     
    security.declareProtected( permissions.View, 'fObtenerTodasColeccionesProgresos')
    def fObtenerTodasColeccionesProgresos( self, ):
   
        unasColecciones = self.fObjectValues( cNombreTipoTRAColeccionProgresos) #
        if not unasColecciones:
            return []
        return unasColecciones
            

    security.declareProtected( permissions.View, 'fObtenerTodosProgresos')
    def fObtenerTodosProgresos( self, ):
   
        unaColeccion = self.fObtenerColeccionProgresos()
        if not unaColeccion:
            return []
        
        unosElementos = unaColeccion.fObjectValues( cNombreTipoTRAProgreso) #
        return unosElementos
           
         
    
    
    
    
    
    
    
    
           
    # ####################################
    """TRAImportacion accessors
    
    """


     
    security.declareProtected( permissions.View, 'fObtenerColeccionImportaciones')
    def fObtenerColeccionImportaciones( self, ):
   
        unasColecciones = self.fObjectValues( cNombreTipoTRAColeccionImportaciones) #
        if not unasColecciones:
            return None
        return unasColecciones[ 0]
    
             
    security.declareProtected( permissions.View, 'fObtenerTodasColeccionesImportaciones')
    def fObtenerTodasColeccionesImportaciones( self, ):
   
        unasColecciones = self.fObjectValues( cNombreTipoTRAColeccionImportaciones) #
        if not unasColecciones:
            return []
        return unasColecciones
    
        

    
    
    security.declareProtected( permissions.View, 'fObtenerTodasImportaciones')
    def fObtenerTodasImportaciones( self, ):
   
        unaColeccion = self.fObtenerColeccionImportaciones()
        if not unaColeccion:
            return []
        
        unosElementos = unaColeccion.fObjectValues( cNombreTipoTRAImportacion) #
        return unosElementos
           
     
    
        
  
            
    
    
    
    



 
    
    

   
        
    security.declareProtected( permissions.View, 'fObtenerTodosParametrosControlProgeso')
    def fObtenerTodosParametrosControlProgeso( self, ):
   
        unosParametrosControlProgreso = self.fObjectValues( cNombreTipoTRAParametrosControlProgreso)

        return unosParametrosControlProgreso
         
                  

        
    
    
    security.declareProtected( permissions.View, 'fObtenerTodasConfiguraciones')
    def fObtenerTodasConfiguraciones( self, ):
   
        unasConfiguraciones = self.fObjectValues( cTodosNombresTiposConfiguracion)

        return unasConfiguraciones
         
                
    
    
    
    security.declareProtected( permissions.View, 'fObtenerConfiguracion')
    def fObtenerConfiguracion( self, theAspectoConfiguracion):
        
        if not theAspectoConfiguracion:
            return None
        
        unaIdConfiguracion = cTRAConfiguracionElementIdsByAspect.get( theAspectoConfiguracion, None)
        unaConfiguracion = self.getElementoPorID( unaIdConfiguracion)
        
        return unaConfiguracion
    
    
    
    
    security.declareProtected( permissions.View, 'fObtenerConfiguracionDict')
    def fObtenerConfiguracionDict( self, theAspectoConfiguracion):
        
        if not theAspectoConfiguracion:
            return {}
        
        unaConfiguracion = self.fObtenerConfiguracion( theAspectoConfiguracion)
        if unaConfiguracion == None:
            return {}
        
        unaConfiguracionDict = unaConfiguracion.fConfigurationDict()
        
        return unaConfiguracionDict
    
    
    
    
    
    
    security.declareProtected( permissions.View, 'fObtenerConfigurationMetaAndValues')
    def fObtenerConfigurationMetaAndValues( self, theAspectoConfiguracion):
        
        if not theAspectoConfiguracion:
            return []
        
        unaConfiguracion = self.fObtenerConfiguracion( theAspectoConfiguracion)
        if unaConfiguracion == None:
            return []
        
        someConfiguracionMetaAndValues = unaConfiguracion.fConfigurationMetaAndValues()
        
        return someConfiguracionMetaAndValues    
    
    
    

    
    
    
    
     
            