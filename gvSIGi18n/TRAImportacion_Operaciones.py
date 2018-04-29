# -*- coding: utf-8 -*-
#
# File: TRAImportacion_Operaciones.py
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


from AccessControl import ClassSecurityInfo



import sys
import traceback



import os
import logging

import time

import transaction

from Products.CMFCore       import permissions





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

from TRAImportarExportar_Constants import *

from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_CreateTRAContenidoXML, cUseCase_ReuseTRAImportacion, cUseCase_CreateTRAContenidoIntercambio, cUseCase_DeleteTRAContenidoIntercambio
from TRAElemento_Permission_Definitions import cBoundObject

from TRAArquetipo import TRAArquetipo


from TRAImportacion_Operaciones_Import               import TRAImportacion_Operaciones_Import
from TRAImportacion_Operaciones_Parse                import TRAImportacion_Operaciones_Parse
from TRAImportacion_Operaciones_Progress             import TRAImportacion_Operaciones_Progress



class TRAImportacion_Operaciones( \
    TRAImportacion_Operaciones_Import, \
    TRAImportacion_Operaciones_Parse,\
    TRAImportacion_Operaciones_Progress,\
    ):
    """
    """
    security = ClassSecurityInfo()
     


    
    
    security.declarePrivate('pHandle_manage_afterAdd')
    def pHandle_manage_afterAdd(self, theItem, theContainer):   
        """ Complete initialization after creation.
        
        """
        
        TRAArquetipo.manage_afterAdd(  self, theItem, theContainer)
        
        # Check for Premature_initialization (may not not yet be hooked under TRACatalog instance)
        #if not self.Title(): # 'portal_factory' in self.getPhysicalPath(): 
            #return self
        
        self.pInitDefaultAttributesFromConfiguration( theItem, theContainer)
        
        return self
    
    
    
    
    
    
    
    
    
    
    
    
    
    security.declarePrivate('fAspectoConfiguracion')
    def fAspectoConfiguracion(self, theItem=None, theContainer=None):   
    
    
        unEsRecuperacion = self.getEsRecuperacion()
        unAspectoConfiguracion = cTRAConfiguracionAspecto_Importacion
        
        if unEsRecuperacion:
            unAspectoConfiguracion = cTRAConfiguracionAspecto_Recuperar 
    
     
        return unAspectoConfiguracion
        
        
        
        
        
    
    
    security.declarePrivate('pInitDefaultAttributesFromConfiguration')
    def pInitDefaultAttributesFromConfiguration(self, theItem=None, theContainer=None):   

        unCatalog = None
        try:
            unCatalog = self.getCatalogo()
        except:
            None
        if unCatalog == None:
            return self
        
        unaConfiguracion = unCatalog.fObtenerConfiguracion( self.fAspectoConfiguracion())
        if unaConfiguracion == None:
            return self
        
                
        unValue = unaConfiguracion.getNombreModuloPorDefecto()        
        self.setNombreModuloPorDefecto( unValue)
        
        unValue = unaConfiguracion.getCodigoIdiomaPorDefecto()        
        self.setCodigoIdiomaPorDefecto( unValue)
        
        unValue = unaConfiguracion.getImportarConNombreModuloConfiguradoPorDefecto()        
        self.setImportarConNombreModuloConfigurado( unValue)
        
        unValue = unaConfiguracion.getImportarFuentesDesdeComentariosPorDefecto()        
        self.setImportarFuentesDesdeComentarios( unValue)
        
        unValue = unaConfiguracion.getImportarNombreModuloDesdeDominioONombreFicheroPorDefecto()        
        self.setImportarNombreModuloDesdeDominioONombreFichero( unValue)
        
        unValue = unaConfiguracion.getImportarNombresModulosDesdeComentariosPorDefecto()        
        self.setImportarNombresModulosDesdeComentarios( unValue)
        
        unValue = unaConfiguracion.getImportarStatusDesdeComentariosPorDefecto()        
        self.setImportarStatusDesdeComentarios( unValue)
        
        unValue = unaConfiguracion.getNumeroMaximoLineasAExplorar()        
        self.setNumeroMaximoLineasAExplorar( unValue)
        
        
        
        
        unValue = unaConfiguracion.getImportarXMLTRACatalogoPorDefecto()        
        self.setImportarXMLTRACatalogo( unValue)
        
        unValue = unaConfiguracion.getImportarXMLTRAConfiguracionesPorDefecto()        
        self.setImportarXMLTRAConfiguraciones( unValue)
        
        unValue = unaConfiguracion.getImportarXMLTRAParametrosControlProgresoPorDefecto()        
        self.setImportarXMLTRAParametrosControlProgreso( unValue)
        
        unValue = unaConfiguracion.getImportarXMLTRAIdiomasPorDefecto()        
        self.setImportarXMLTRAIdiomas( unValue)
        
        unValue = unaConfiguracion.getImportarXMLTRASolicitudesCadenasPorDefecto()        
        self.setImportarXMLTRASolicitudesCadenas( unValue)
                            
        unValue = unaConfiguracion.getImportarXMLTRAModulosPorDefecto()        
        self.setImportarXMLTRAModulos( unValue)
                            
        unValue = unaConfiguracion.getImportarXMLTRAInformesPorDefecto()        
        self.setImportarXMLTRAInformes( unValue)
                            
        #unValue = unaConfiguracion.getImportarXMLTRAImportacionesPorDefecto()        
        #self.setImportarXMLTRAImportaciones( unValue)
                            
        #unValue = unaConfiguracion.getImportarXMLTRAProgresosPorDefecto()        
        #self.setImportarXMLTRAProgresos( unValue)
                            
        return self
        
    
        
    
    
    
    security.declarePrivate('fInitial_CrearInformeAntes')
    def fInitial_CrearInformeAntes(self, ):   

        unCatalog = None
        try:
            unCatalog = self.getCatalogo()
        except:
            None
        if unCatalog == None:
            return False
        
        unaConfiguracion = unCatalog.fObtenerConfiguracion( self.fAspectoConfiguracion())
        if unaConfiguracion == None:
            return False
        
        unValue = unaConfiguracion.getCrearInformeAntesPorDefecto()        
        return unValue
    
    
    
    
    
    security.declarePrivate('fInitial_CrearInformeDespues')
    def fInitial_CrearInformeDespues(self, ):   

        unCatalog = None
        try:
            unCatalog = self.getCatalogo()
        except:
            None
        if unCatalog == None:
            return False
        
        unaConfiguracion = unCatalog.fObtenerConfiguracion( self.fAspectoConfiguracion())
        if unaConfiguracion == None:
            return False
        
        unValue = unaConfiguracion.getCrearInformeDespuesPorDefecto()        
        return unValue
    
    
    
    
    security.declarePrivate('fInitial_CodigoIdiomaPorDefecto')
    def fInitial_CodigoIdiomaPorDefecto(self, ):   

        unCatalog = None
        try:
            unCatalog = self.getCatalogo()
        except:
            None
        if unCatalog == None:
            return ''
        
        unaConfiguracion = unCatalog.fObtenerConfiguracion( self.fAspectoConfiguracion())
        if unaConfiguracion == None:
            return ''
        
        unValue = unaConfiguracion.getCodigoIdiomaPorDefecto()        
        return unValue
    
    
    
    
    security.declarePrivate('fInitial_NombreModuloPorDefecto')
    def fInitial_NombreModuloPorDefecto(self, ):   

        unCatalog = None
        try:
            unCatalog = self.getCatalogo()
        except:
            None
        if unCatalog == None:
            return ''
        
        unaConfiguracion = unCatalog.fObtenerConfiguracion( self.fAspectoConfiguracion())
        if unaConfiguracion == None:
            return ''
        
        unValue = unaConfiguracion.getNombreModuloPorDefecto()        
        return unValue
    
    
    
    

    
    
    security.declarePrivate('fInitial_NumeroMaximoLineasAExplorar')
    def fInitial_NumeroMaximoLineasAExplorar(self, ):   

        unCatalog = None
        try:
            unCatalog = self.getCatalogo()
        except:
            None
        if unCatalog == None:
            return ''
        
        unaConfiguracion = unCatalog.fObtenerConfiguracion( self.fAspectoConfiguracion())
        if unaConfiguracion == None:
            return ''
        
        unValue = unaConfiguracion.getNumeroMaximoLineasAExplorar()        
        return unValue
    
    
    
    
    security.declarePrivate('fInitial_ImportarConNombreModuloConfigurado')
    def fInitial_ImportarConNombreModuloConfigurado(self, ):   

        unCatalog = None
        try:
            unCatalog = self.getCatalogo()
        except:
            None
        if unCatalog == None:
            return False
        
        unaConfiguracion = unCatalog.fObtenerConfiguracion( self.fAspectoConfiguracion())
        if unaConfiguracion == None:
            return False
        
        unValue = unaConfiguracion.getImportarConNombreModuloConfiguradoPorDefecto()        
        return unValue
    
    

 
    
    security.declarePrivate('fInitial_ImportarFuentesDesdeComentarios')
    def fInitial_ImportarFuentesDesdeComentarios(self, ):   

        unCatalog = None
        try:
            unCatalog = self.getCatalogo()
        except:
            None
        if unCatalog == None:
            return False
        
        unaConfiguracion = unCatalog.fObtenerConfiguracion( self.fAspectoConfiguracion())
        if unaConfiguracion == None:
            return False
        
        unValue = unaConfiguracion.getImportarFuentesDesdeComentariosPorDefecto()        
        return unValue
    
    

 
    
    security.declarePrivate('fInitial_ImportarNombreModuloDesdeDominioONombreFichero')
    def fInitial_ImportarNombreModuloDesdeDominioONombreFichero(self, ):   

        unCatalog = None
        try:
            unCatalog = self.getCatalogo()
        except:
            None
        if unCatalog == None:
            return False
        
        unaConfiguracion = unCatalog.fObtenerConfiguracion( self.fAspectoConfiguracion())
        if unaConfiguracion == None:
            return False
        
        unValue = unaConfiguracion.getImportarNombreModuloDesdeDominioONombreFicheroPorDefecto()        
        return unValue
    
    

 
    
    security.declarePrivate('fInitial_ImportarNombresModulosDesdeComentarios')
    def fInitial_ImportarNombresModulosDesdeComentarios(self, ):   

        unCatalog = None
        try:
            unCatalog = self.getCatalogo()
        except:
            None
        if unCatalog == None:
            return False
        
        unaConfiguracion = unCatalog.fObtenerConfiguracion( self.fAspectoConfiguracion())
        if unaConfiguracion == None:
            return False
        
        unValue = unaConfiguracion.getImportarNombresModulosDesdeComentariosPorDefecto()        
        return unValue
    
    

 
    
    security.declarePrivate('fInitial_ImportarStatusDesdeComentarios')
    def fInitial_ImportarStatusDesdeComentarios(self, ):   

        unCatalog = None
        try:
            unCatalog = self.getCatalogo()
        except:
            None
        if unCatalog == None:
            return False
        
        unaConfiguracion = unCatalog.fObtenerConfiguracion( self.fAspectoConfiguracion())
        if unaConfiguracion == None:
            return False
        
        unValue = unaConfiguracion.getImportarStatusDesdeComentariosPorDefecto()        
        return unValue
    

 
    
    security.declarePrivate('fInitial_ImportarContribucionesDesdeComentarios')
    def fInitial_ImportarContribucionesDesdeComentarios(self, ):   

        unCatalog = None
        try:
            unCatalog = self.getCatalogo()
        except:
            None
        if unCatalog == None:
            return False
        
        unaConfiguracion = unCatalog.fObtenerConfiguracion( self.fAspectoConfiguracion())
        if unaConfiguracion == None:
            return False
        
        unValue = unaConfiguracion.getImportarContribucionesDesdeComentariosPorDefecto()        
        return unValue
        

     
    
    
    security.declarePrivate('fInitial_ImportarXMLTRACatalogo')
    def fInitial_ImportarXMLTRACatalogo(self, ):   

        unCatalog = None
        try:
            unCatalog = self.getCatalogo()
        except:
            None
        if unCatalog == None:
            return False
        
        unaConfiguracion = unCatalog.fObtenerConfiguracion( self.fAspectoConfiguracion())
        if unaConfiguracion == None:
            return False
        
        unValue = unaConfiguracion.getImportarXMLTRACatalogoPorDefecto()        
        return unValue
    
    

    
    
     
    
    security.declarePrivate('fInitial_ImportarXMLTRAConfiguraciones')
    def fInitial_ImportarXMLTRAConfiguraciones(self, ):   

        unCatalog = None
        try:
            unCatalog = self.getCatalogo()
        except:
            None
        if unCatalog == None:
            return False
        
        unaConfiguracion = unCatalog.fObtenerConfiguracion( self.fAspectoConfiguracion())
        if unaConfiguracion == None:
            return False
        
        unValue = unaConfiguracion.getImportarXMLTRAConfiguracionesPorDefecto()        
        return unValue
    
    
    

     
    
    security.declarePrivate('fInitial_ImportarXMLTRAParametrosControl')
    def fInitial_ImportarXMLTRAParametrosControl(self, ):   

        unCatalog = None
        try:
            unCatalog = self.getCatalogo()
        except:
            None
        if unCatalog == None:
            return False
        
        unaConfiguracion = unCatalog.fObtenerConfiguracion( self.fAspectoConfiguracion())
        if unaConfiguracion == None:
            return False
        
        unValue = unaConfiguracion.getImportarXMLTRAParametrosControlProgresoPorDefecto()        
        return unValue
    
            
    

    security.declarePrivate('fInitial_ImportarXMLTRAIdiomas')
    def fInitial_ImportarXMLTRAIdiomas(self, ):   

        unCatalog = None
        try:
            unCatalog = self.getCatalogo()
        except:
            None
        if unCatalog == None:
            return False
        
        unaConfiguracion = unCatalog.fObtenerConfiguracion( self.fAspectoConfiguracion())
        if unaConfiguracion == None:
            return False
        
        unValue = unaConfiguracion.getImportarXMLTRAIdiomasPorDefecto()        
        return unValue
    
                
    
    


    security.declarePrivate('fInitial_ImportarXMLTRASolicitudesCadenas')
    def fInitial_ImportarXMLTRASolicitudesCadenas(self, ):   

        unCatalog = None
        try:
            unCatalog = self.getCatalogo()
        except:
            None
        if unCatalog == None:
            return False
        
        unaConfiguracion = unCatalog.fObtenerConfiguracion( self.fAspectoConfiguracion())
        if unaConfiguracion == None:
            return False
        
        unValue = unaConfiguracion.getImportarXMLTRASolicitudesCadenasPorDefecto()        
        return unValue
    
                
        
    
       
    

    security.declarePrivate('fInitial_ImportarXMLTRAModulos')
    def fInitial_ImportarXMLTRAModulos(self, ):   

        unCatalog = None
        try:
            unCatalog = self.getCatalogo()
        except:
            None
        if unCatalog == None:
            return False
        
        unaConfiguracion = unCatalog.fObtenerConfiguracion( self.fAspectoConfiguracion())
        if unaConfiguracion == None:
            return False
        
        unValue = unaConfiguracion.getImportarXMLTRAModulosPorDefecto()        
        return unValue
    
                
        
    
    
    

    security.declarePrivate('fInitial_ImportarXMLTRAModulos')
    def fInitial_ImportarXMLTRAModulos(self, ):   

        unCatalog = None
        try:
            unCatalog = self.getCatalogo()
        except:
            None
        if unCatalog == None:
            return False
        
        unaConfiguracion = unCatalog.fObtenerConfiguracion( self.fAspectoConfiguracion())
        if unaConfiguracion == None:
            return False
        
        unValue = unaConfiguracion.getImportarXMLTRAModulosPorDefecto()        
        return unValue
    
                    
    
    

    security.declarePrivate('fInitial_ImportarXMLTRAInformes')
    def fInitial_ImportarXMLTRAInformes(self, ):   

        unCatalog = None
        try:
            unCatalog = self.getCatalogo()
        except:
            None
        if unCatalog == None:
            return False
        
        unaConfiguracion = unCatalog.fObtenerConfiguracion( self.fAspectoConfiguracion())
        if unaConfiguracion == None:
            return False
        
        unValue = unaConfiguracion.getImportarXMLTRAInformesPorDefecto()        
        return unValue
    
                        
    
    
    

    #security.declarePrivate('fInitial_ImportarXMLTRAImportaciones')
    #def fInitial_ImportarXMLTRAImportaciones(self, ):   

        #unCatalog = None
        #try:
            #unCatalog = self.getCatalogo()
        #except:
            #None
        #if unCatalog == None:
            #return False
        
        #unaConfiguracion = unCatalog.fObtenerConfiguracion( self.fAspectoConfiguracion())
        #if unaConfiguracion == None:
            #return False
        
        #unValue = unaConfiguracion.getImportarXMLTRAImportacionesPorDefecto()        
        #return unValue
    
                        
        
    
    

    

    #security.declarePrivate('fInitial_ImportarXMLTRAProgresos')
    #def fInitial_ImportarXMLTRAProgresos(self, ):   

        #unCatalog = None
        #try:
            #unCatalog = self.getCatalogo()
        #except:
            #None
        #if unCatalog == None:
            #return False
        
        #unaConfiguracion = unCatalog.fObtenerConfiguracion( self.fAspectoConfiguracion())
        #if unaConfiguracion == None:
            #return False
        
        #unValue = unaConfiguracion.getImportarXMLTRAProgresosPorDefecto()        
        #return unValue
    
                        
        
        
    
    
    
    
    
    
    
    security.declarePrivate( 'pAllSubElements_into')    
    def pAllSubElements_into( self, theCollection, theAdditionalParams=None):
        if theCollection == None:
            return self
        theCollection.append( self)
        
        
        unosElementos = self.fObtenerTodosContenidosIntercambio()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pAllSubElements_into( theCollection, theAdditionalParams=theAdditionalParams)
        
        unosElementos = self.fObtenerTodosInformes()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pAllSubElements_into( theCollection, theAdditionalParams=theAdditionalParams)
        
        return self
           
    
    
    


    security.declarePrivate( 'pForAllElementsDo_recursive')    
    def pForAllElementsDo_recursive( self, theLambda=None, thePloneLambda=None,):
        if not theLambda:
            return self
        
        theLambda( self)        
    
        unosElementos = self.fObtenerTodosContenidosIntercambio()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda, thePloneLambda)
        
        unosElementos = self.fObtenerTodosInformes()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda, thePloneLambda)
                
        if thePloneLambda:
            self.pForAllElementsPloneDo( thePloneLambda)
        
        return self
           
    
        
    

    
         
    
  
       
        
    

    security.declarePrivate( 'fInitialParameters_CrearContenidoIntercambio')    
    def fInitialParameters_CrearContenidoIntercambio( self,):    
        """Parameters to initialize the dialog with the user when creating a translations interchange contents element.
        
        """
        someParameters = {
            'nombreModuloPorDefecto':             self.getNombreModuloPorDefecto(),
            'codigoIdiomaPorDefecto':             self.getCodigoIdiomaPorDefecto(),
            'importarConNombreModuloConfigurado': self.getImportarConNombreModuloConfigurado(),
            'importarNombreModuloDesdeDominioONombreFichero': self.getImportarNombreModuloDesdeDominioONombreFichero(),
            'importarNombresModulosDesdeComentarios': self.getImportarNombresModulosDesdeComentarios(),
            'importarContribucionesDesdeComentarios': self.getImportarContribucionesDesdeComentarios(),
            'importarFuentesDesdeComentarios':    self.getImportarFuentesDesdeComentarios(),
            'importarStatusDesdeComentarios':     self.getImportarStatusDesdeComentarios(),
            'numeroMaximoLineasAExplorar':        self.getNumeroMaximoLineasAExplorar(),
        }
        return someParameters
    
    
       
     
    
    
    
    
        
    # ###################################################################
    """Contenidos intercambio access.
    
    """
                
    security.declareProtected( permissions.View, 'fObtenerContenidoXML')
    def fObtenerContenidoXML( self, ):
   
        unContenidoXMLEncontrado = self.getElementoPorID( cTRAIdContenidoXML)
        return unContenidoXMLEncontrado
         
    
                
    security.declareProtected( permissions.View, 'fHasContenidoXML')
    def fHasContenidoXML( self, ):
        
        unElementoContenidoXML = self.fObtenerContenidoXML()
        if unElementoContenidoXML == None:
            return False
        
        return True
    
    
    
                
    security.declareProtected( permissions.View, 'fHasNoContenidoXML')
    def fHasNoContenidoXML( self, ):
   
        return not self.fHasContenidoXML()
    
             
        
      
                
    security.declareProtected( permissions.View, 'fObtenerTodosContenidosIntercambio')
    def fObtenerTodosContenidosIntercambio( self, ):
   
        unosElementos = self.fObjectValues( cNombreTipoTRAContenidoIntercambio) 
        return unosElementos
         
  
    
    
    
    
    security.declareProtected( permissions.View, 'fObtenerTodosContenidosIntercambioNoExcluidos')
    def fObtenerTodosContenidosIntercambioNoExcluidos( self, ):
               
        unosContenidosIntercambio = self.fObtenerTodosContenidosIntercambio()
        unosContenidosIntercambioNoExcluidos = [ unContenidoIntercambio for unContenidoIntercambio in unosContenidosIntercambio if not unContenidoIntercambio.getExcluirDeImportacion()]
        return unosContenidosIntercambioNoExcluidos   
             
                
    
               
    security.declareProtected( permissions.View, 'fObtenerTodosInformes')
    def fObtenerTodosInformes( self, ):
   
        unosElementos = self.fObjectValues( cNombreTipoTRAInforme) 
        return unosElementos
         
  
   
    
    
    
    # ################################################################
    """Add and remove content to be imported.
    
    """
            

    
    
    
    
    
    

    
    security.declarePrivate( 'fCrearContenidoXML')    
    def fCrearContenidoXML( self,
        theTimeProfilingResults =None,
        theModelDDvlPloneTool_Mutators   =None, 
        theFileName             = '',
        theXMLSource            =None,
        theContenidoBinario     =None,
        theAdditionalParams     =None,
        thePermissionsCache     =None,
        theRolesCache           =None,
        theParentExecutionRecord=None):
    
    
        unExecutionRecord = self.fStartExecution( 'method',  'fCrearContenidoXML', None, True, { 'log_what': 'details', 'log_when': True, }) 

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators  import cModificationKind_CreateSubElement, cModificationKind_Create, cModificationKind_ChangeValues

        try:
            unasDescripcionesContenidosCreados = []
            try:
                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)
                
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_CreateTRAContenidoXML, 
                    theElementsBindings     = { cBoundObject: self,}, 
                    theRulesToCollect       = None, 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord,
                )
              
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_no_permission_msgid', "User does not have permission to create XML contents.-"), }
                    return anActionReport  
                            
                aModelDDvlPlone_tool = self.fModelDDvlPloneTool()
                             
                aPloneUtilsTool = self.getPloneUtilsToolForNormalizeString()  
                
                unTitle        = ''
                unaDescripcion = ''
                unTexto        = ''
                
                        
                unElementoContenidoXML = self.fObtenerContenidoXML()
                
                if not ( unElementoContenidoXML == None):
                    
                    unTitle        = unElementoContenidoXML.Title()
                    unaDescripcion = unElementoContenidoXML.Description()
                    unTexto        = unElementoContenidoXML.getText()
                    
                    unElementoContenidoXML.pSetContenidoBinario( None)
                    unElementoContenidoXML.setContenidoXML(      None)
                    
                else:
                    unBaseTitle    = 'XML %s' % self.Title()
                    unaDescripcion = '%s XML with properties of backed-up translations catalog' % self.Description()
                    unTexto        = '%s XML with properties of backed-up translations catalog' % self.getText()
                               
                    
                    
                    
                    
                    unTitle        = unBaseTitle
                    
                    someObjectValues = self.fObjectValues()
                    
                    someTitles = [ unObjectValue.Title() for unObjectValue in someObjectValues]
                                            
                    aNewId = cTRAIdContenidoXML
                    
                    if aPloneUtilsTool:
                        aNewId = aPloneUtilsTool.normalizeString( aNewId)
                        
                    unCounter = 0 
                    
                    while unTitle in someTitles:
                        unCounter += 1
                        unTitle = '%s-%d' % ( unBaseTitle, unCounter, )
     
                             
                    unMemberId = self.fGetMemberId()
    
                    anAttrsDict = { 
                        'title':                    unTitle,
                        'description':              unaDescripcion,
                        'text':                     unTexto,
                        'usuarioContribuidor':      unMemberId,
                        'excluirDeImportacion':     False,
                    }
                    
                    unaIdNuevoContenidoXML = self.invokeFactory( cNombreTipoTRAContenidoXML, aNewId, **anAttrsDict)
                    if not unaIdNuevoContenidoXML:
                        anActionReport = { 'effect': 'error', 'failure': '%s' % self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorcreacioncontenidoXML_errorencreacion', "No se ha podido crear Contenido XML." ) }
                        return anActionReport     
                                    
                    unElementoContenidoXML = self.getElementoPorID( unaIdNuevoContenidoXML)
                    if ( unElementoContenidoXML == None):
                        anActionReport = { 'effect': 'error', 'failure': '%s module %s' % (   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorcreacioncontenidointercambio_newelementnotfound', "No se ha encuentra el Contenido de Intercambio recien creado."), unModulo, ) }
                        return anActionReport     

                    
                unElementoContenidoXML.setFicheroLeido(      theFileName)
                        
                unElementoContenidoXML.pSetContenidoXML(     theXMLSource)
                unElementoContenidoXML.pSetContenidoBinario( theContenidoBinario)
                

                unResultadoElementoContenidoXML = aModelDDvlPlone_tool.fRetrieveTypeConfig( 
                    theTimeProfilingResults     =None,
                    theElement                  =unElementoContenidoXML, 
                    theParent                   =None,
                    theParentTraversalName      ='',
                    theTypeConfig               =None, 
                    theAllTypeConfigs           =None, 
                    theViewName                 ='', 
                    theRetrievalExtents         =[ 'traversals', ],
                    theWritePermissions         =None,
                    theFeatureFilters           ={ 'attrs': [ 'title',], 'relations': [], 'do_not_recurse_collections': True,}, 
                    theInstanceFilters          =None,
                    theTranslationsCaches       =None,
                    theCheckedPermissionsCache  =thePermissionsCache,
                    theAdditionalParams         =None                
                )
                if not unResultadoElementoContenidoXML:
                    anActionReport = { 'effect': 'error', 'failure': 'retrieval_failure', }
                    return anActionReport     
 
                unContenidoXMLCreationReport = { 'effect': 'created', 'new_object_result': unResultadoElementoContenidoXML, }
                     
                aModelDDvlPloneTool_Mutators = theModelDDvlPloneTool_Mutators
                if not aModelDDvlPloneTool_Mutators:
                    aModelDDvlPloneTool_Mutators = self.fModelDDvlPloneTool().fModelDDvlPloneTool_Mutators( self)
                    
                aCreateElementReport = aModelDDvlPloneTool_Mutators.fNewVoidCreateElementReport()
                aCreateElementReport.update( { 'effect': 'created', 'new_object_result': unResultadoElementoContenidoXML, })
                                                           
                aModelDDvlPloneTool_Mutators.pSetAudit_Creation( self,                        cModificationKind_CreateSubElement, aCreateElementReport, theUseCounter=True)       
                aModelDDvlPloneTool_Mutators.pSetAudit_Creation( unElementoContenidoXML,      cModificationKind_Create,           aCreateElementReport)       

                self.pFlushCachedTemplates_All()                            
                
                transaction.commit()
                
                
                logging.getLogger( 'gvSIGi18n').info("COMMIT new %s %s with description\n%s\nand text:\n%s\n" % ( cNombreTipoTRAContenidoXML, unTitle,  unaDescripcion, unTexto, )) 
        

                        
                if unContenidoXMLCreationReport:
                    return unContenidoXMLCreationReport
                
                anActionReport = { 'effect': 'error', 'failure': 'Error after already created %s\n%s' % ( '\n'.join( unasDescripcionesContenidosCreados), self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorcreacioncontenidointercambio_ningunocreado', "No se ha creado ningun Contenido de Intercambio."), ) }
                return anActionReport     

            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fCrearContenidoXML\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   
                                         
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                anActionReport = { 'effect': 'error', 'failure': 'Error after already created %s\n%s' % ( '\n'.join( unasDescripcionesContenidosCreados), self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorcreacioncontenidointercambio_ningunocreado', "No se ha creado ningun Contenido de Intercambio."), ) }
                return anActionReport     
              
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

        
                
                
                
                
    
    
    
    
    
    
    
    
    

    
    security.declarePrivate( 'fCrearContenidoIntercambio')    
    def fCrearContenidoIntercambio( self,
        theTimeProfilingResults =None,
        theModelDDvlPloneTool_Mutators   =None, 
        theNewTypeName          ='', 
        theNewOneTitle          ='', 
        theNewOneDescription    ='', 
        theAdditionalParams     =None,
        thePermissionsCache     =None,
        theRolesCache           =None,
        theParentExecutionRecord=None):
    
    
        unExecutionRecord = self.fStartExecution( 'method',  'fCrearContenidoIntercambio', None, True, { 'log_what': 'details', 'log_when': True, }) 

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators  import cModificationKind_CreateSubElement, cModificationKind_Create, cModificationKind_ChangeValues

        try:
            unasDescripcionesContenidosCreados = []
            try:
                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)
                
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_CreateTRAContenidoIntercambio, 
                    theElementsBindings     = { cBoundObject: self,}, 
                    theRulesToCollect       = None, 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord,
                )
              
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_no_permission_msgid', "User does not have permission to create interchange contents.-"), }
                    return anActionReport  
                            
                aModelDDvlPlone_tool = self.fModelDDvlPloneTool()
                             
                aDefaultLanguage       = theAdditionalParams.get( 'theDefaultLanguage', None)
                unUploadedFile         = theAdditionalParams.get( 'theUploadedFile',    None)
        
                
                if not unUploadedFile:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorcreacioncontenidointercambio_faltafichero_warning_msgid', "Can not create an interchange contents element without an uploaded file.-"), }
                    return anActionReport  
                
                unosContenidos = self.fContenidosDeUploadedFile( 
                    theParentExecutionRecord =theParentExecutionRecord, 
                    theUploadedFile         =unUploadedFile, 
                    theDefaultLanguage      =aDefaultLanguage,
                    theAdditionalParams     =theAdditionalParams,
                )
                
                if not unosContenidos:
                    anActionReport = { 'effect': 'error', 'failure':  self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorcreacioncontenidointercambio_ficherosincontenidovalido_warning_msgid', "Invalid interchange file contents. Can not create an interchange contents element without an uploaded file with valid contents.-"), }
                    return anActionReport  
                
                unContenidoIntercambioCreationReport = None
                 
                unosClavesYContenidosParaOrdenar = [ [ '%s|||%s' % (  '|'.join( sorted( unUploadedContent.get( 'content_data', {}).get('languages',[]))), ' '.join( sorted( unUploadedContent.get( 'content_data', {}).get( 'modules', []))),), unUploadedContent] for unUploadedContent in unosContenidos]
                unosClavesYContenidosOrdenados = sorted( unosClavesYContenidosParaOrdenar, lambda unC, otroC : cmp( unC[ 0] , otroC[ 0]) )
                
                aPloneUtilsTool = self.getPloneUtilsToolForNormalizeString()  
                
                for unaClavesYUploadedContent in unosClavesYContenidosOrdenados:  
                    
                    unUploadedContent = unaClavesYUploadedContent[ 1]
                    
                    unSubExecutionRecord = self.fStartExecution( 'method',  'fCrearContenidoIntercambio::subSection for one Uploaded Content with module|||languages:', unExecutionRecord, False, { 'log_what': 'details', 'log_when': True, }, unaClavesYUploadedContent[ 0]) 
                    
                    try:
                        unasUploadedEntries = unUploadedContent.get( 'uploaded_entries', [])
                        unosLenguages = sorted( unUploadedContent.get( 'content_data', {}).get( 'languages', []))

                        unLenguagesString = ', '.join( [ ('[%s]' % unLenguage) for unLenguage in unosLenguages ])
                        
                        unModulosString = ''
                        unosNombresModulo    = sorted( unUploadedContent.get( 'content_data', {}).get( 'modules', []))
                        if unosNombresModulo:
                            unModulosString = ' '.join( unosNombresModulo)
                        if not unModulosString:
                            unModulosString = cNombreModuloNoEspecificadoInputValue
                        
                        unosFileNamesPossiblyDuplicated = [ unUploadedEntry[ 'file_name'] for unUploadedEntry in unasUploadedEntries]

                        unosFileNames = [ ]
                        for aFileName in unosFileNamesPossiblyDuplicated:
                            if not ( aFileName in unosFileNames):
                                unosFileNames.append( aFileName)
                            
                        unosFileNamesString = ' '.join( unosFileNames)
                         
                        unasDescripciones = [ 'file: %(file_name)s, kind: %(file_kind)s, ref: %(is_reference)d, language: %(language)s, country: %(country)s, charset: %(charset)s, fallback for: %(is_fallback_for)s, domain: %(domain)s,'  % unUploadedEntry for unUploadedEntry in unasUploadedEntries]

                        
                        unBaseTitle    = '%s %s %s' % ( unosFileNamesString, unLenguagesString, unModulosString, )
                        unaDescripcion = 'Languages %s with Modules %s from Files %s' % ( unLenguagesString, unModulosString, unosFileNamesString,)
                        unTexto        = 'Languages %s with Modules %s\nFrom file entries:\n%s' % ( unLenguagesString, unModulosString, '\n'.join( unasDescripciones),)
                               
                        
                        
                        
                        
                        unTitle = unBaseTitle
                        
                        someObjectValues = self.fObjectValues()
                        
                        someTitles = [ unObjectValue.Title() for unObjectValue in someObjectValues]
                        someIds    = [ unObjectValue.getId() for unObjectValue in someObjectValues]
                        
                        aNewId = unTitle.lower().replace( ' ', '-')
                        if aPloneUtilsTool:
                            aNewId = aPloneUtilsTool.normalizeString( aNewId)
                            
                        unCounter = 0 
                        
                        while ( unTitle in someTitles) or ( aNewId in someIds):
                            unCounter += 1
                            unTitle = '%s-%d' % ( unBaseTitle, unCounter, )
                            aNewId = unTitle.lower().replace( ' ', '-')
                            if aPloneUtilsTool:
                                aNewId = aPloneUtilsTool.normalizeString( aNewId)
        
                            
                        unMemberId = self.fGetMemberId()
        
                        anAttrsDict = { 
                            'title':                    unTitle,
                            'description':              unaDescripcion,
                            'text':                     unTexto,
                            'usuarioContribuidor':      unMemberId,
                            'excluirDeImportacion':     False,
                        }
                        
                        unaIdNuevoContenidoIntercambio = self.invokeFactory( cNombreTipoTRAContenidoIntercambio, aNewId, **anAttrsDict)
                        if not unaIdNuevoContenidoIntercambio:
                            anActionReport = { 'effect': 'error', 'failure': '%s module %s' % (   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorcreacioncontenidointercambio_errorencreacion', "No se ha podido crear Contenido de Intercambio."), unModulo, ) }
                            return anActionReport     
                                        
                        unNuevoContenidoIntercambio = self.getElementoPorID( unaIdNuevoContenidoIntercambio)
                        if unNuevoContenidoIntercambio == None:
                            anActionReport = { 'effect': 'error', 'failure': '%s module %s' % (   self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorcreacioncontenidointercambio_newelementnotfound', "No se ha encuentra el Contenido de Intercambio recien creado."), unModulo, ) }
                            return anActionReport     
    
                        
                        unNuevoContenidoIntercambio.pSetContenido( unUploadedContent)   

                        unNuevoContenidoIntercambio.setFicheroLeido( unosFileNamesString)

                        unNuevoContenidoIntercambio.setCodigoIdiomaPorDefecto( aDefaultLanguage) 
                        unNuevoContenidoIntercambio.setNombreModuloPorDefecto( theAdditionalParams.get( 'theDefaultModule', None)) 
                        unNuevoContenidoIntercambio.setImportarConNombreModuloConfigurado( theAdditionalParams.get( 'theImportWithConfiguredModuleName', False) == True) 
                        unNuevoContenidoIntercambio.setImportarNombreModuloDesdeDominioONombreFichero( theAdditionalParams.get( 'theImportModuleNameFromDomainOrFilename', False) == True) 
                        unNuevoContenidoIntercambio.setImportarNombresModulosDesdeComentarios( theAdditionalParams.get( 'theImportModuleNamesFromComment',  False) == True) 
                        unNuevoContenidoIntercambio.setImportarContribucionesDesdeComentarios( theAdditionalParams.get( 'theImportContributionsFromComment',  False) == True) 
                        unNuevoContenidoIntercambio.setImportarFuentesDesdeComentarios( theAdditionalParams.get( 'theImportSourcesFromComment',  False) == True) 
                        unNuevoContenidoIntercambio.setImportarStatusDesdeComentarios( theAdditionalParams.get( 'theImportStatusFromComment',  False) == True) 
                        aNumeroMaximoLineasAExplorarString = theAdditionalParams.get( 'theMaxLinesToScan', '-1')
                        aNumeroMaximoLineasAExplorar = -1
                        try:
                            aNumeroMaximoLineasAExplorar = int( aNumeroMaximoLineasAExplorarString)
                        except:
                            None
                        unNuevoContenidoIntercambio.setNumeroMaximoLineasAExplorar( aNumeroMaximoLineasAExplorar) 
                        
                        
                        unasDescripcionesContenidosCreados.append( unaDescripcion)
                        
                        unResultadoNuevoContenidoIntercambio = aModelDDvlPlone_tool.fRetrieveTypeConfig( 
                            theTimeProfilingResults     =None,
                            theElement                  =unNuevoContenidoIntercambio, 
                            theParent                   =None,
                            theParentTraversalName      ='',
                            theTypeConfig               =None, 
                            theAllTypeConfigs           =None, 
                            theViewName                 ='', 
                            theRetrievalExtents         =[ 'traversals', ],
                            theWritePermissions         =None,
                            theFeatureFilters           ={ 'attrs': [ 'title',], 'relations': [], 'do_not_recurse_collections': True,}, 
                            theInstanceFilters          =None,
                            theTranslationsCaches       =None,
                            theCheckedPermissionsCache  =thePermissionsCache,
                            theAdditionalParams         =None                
                        )
                        if not unResultadoNuevoContenidoIntercambio:
                            anActionReport = { 'effect': 'error', 'failure': 'retrieval_failure', }
                            return anActionReport     
         
                        unContenidoIntercambioCreationReport = { 'effect': 'created', 'new_object_result': unResultadoNuevoContenidoIntercambio, }
                             
                        aModelDDvlPloneTool_Mutators = theModelDDvlPloneTool_Mutators
                        if not aModelDDvlPloneTool_Mutators:
                            aModelDDvlPloneTool_Mutators = self.fModelDDvlPloneTool().fModelDDvlPloneTool_Mutators( self)
                            
                        aCreateElementReport = aModelDDvlPloneTool_Mutators.fNewVoidCreateElementReport()
                        aCreateElementReport.update( { 'effect': 'created', 'new_object_result': unResultadoNuevoContenidoIntercambio, })
                                                                   
                        aModelDDvlPloneTool_Mutators.pSetAudit_Creation( self,                        cModificationKind_CreateSubElement, aCreateElementReport, theUseCounter=True)       
                        aModelDDvlPloneTool_Mutators.pSetAudit_Creation( unNuevoContenidoIntercambio, cModificationKind_Create,           aCreateElementReport)       

                        self.pFlushCachedTemplates_All()                            
                        
                        transaction.commit()
                        
                        
                        logging.getLogger( 'gvSIGi18n').info("COMMIT new %s %s with description\n%s\nand text:\n%s\n" % ( cNombreTipoTRAContenidoIntercambio, unTitle,  unaDescripcion, unTexto, )) 
        
                    finally:
                        unSubExecutionRecord and unSubExecutionRecord.pEndExecution()
                        unSubExecutionRecord and unSubExecutionRecord.pClearLoggedAll()
                        
                        
                if unContenidoIntercambioCreationReport:
                    return unContenidoIntercambioCreationReport
                
                anActionReport = { 'effect': 'error', 'failure': 'Error after already created %s\n%s' % ( '\n'.join( unasDescripcionesContenidosCreados), self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorcreacioncontenidointercambio_ningunocreado', "No se ha creado ningun Contenido de Intercambio."), ) }
                return anActionReport     

            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fCrearContenidoIntercambio\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   
                                         
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                anActionReport = { 'effect': 'error', 'failure': 'Error after already created %s\n%s' % ( '\n'.join( unasDescripcionesContenidosCreados), self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_errorcreacioncontenidointercambio_ningunocreado', "No se ha creado ningun Contenido de Intercambio."), ) }
                return anActionReport     
              
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

        
                
                
                
            
            
            
    security.declareProtected( permissions.DeleteObjects, 'fEliminarContenidoIntercambio')    
    def fEliminarContenidoIntercambio( self, theContenidoIntercambio, theUseCaseQueryResult=None, thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fEliminarContenidoIntercambio', theParentExecutionRecord, False) 
        
        try:
            if not theContenidoIntercambio:
                return False
            
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
                
            unUseCaseQueryResult = theUseCaseQueryResult
            if not theUseCaseQueryResult or not ( theUseCaseQueryResult.get( 'use_case_name', '') == cUseCase_DeleteTRAContenidoIntercambio):
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_DeleteTRAContenidoIntercambio,             
                    theElementsBindings     = { cBoundObject: self,},                    
                    theRulesToCollect       = None,                                      
                    thePermissionsCache     = unPermissionsCache,    
                    theRolesCache           = unRolesCache,                
                    theParentExecutionRecord= unExecutionRecord,
                )
            if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                return False
                                                
            unosContenidosIntercambio = self.fObtenerTodosContenidosIntercambio()
            
            if not ( theContenidoIntercambio in unosContenidosIntercambio):
                return False
            
            self.manage_delObjects( [ theContenidoIntercambio.getId(), ])
                
            return True
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()

        
     
    
            
            
            
            
            
            
                
                                
        
        
                
                 
                    
       
    
                
    security.declarePrivate( 'fCombinedContenidosIntercambio')    
    def fCombinedContenidosIntercambio( self, theParentExecutionRecord=None):
        
        if cLogEachExecution_fCombinedContenidosIntercambio:
            unExecutionRecord = self.fStartExecution( 'method',  'fCombinedContenidosIntercambio', theParentExecutionRecord,  True, { 'log_what': 'details', 'log_when': True, }) 
        else:
            unExecutionRecord = self.fStartExecution( 'method',  'fCombinedContenidosIntercambio', theParentExecutionRecord,  False) 
        
        try:
            
            unCombinedUploadedContent = self.fNewVoidUploadedContent()
            
            unCombinedScannedData = self.fNewVoidScannedData()
            unCombinedUploadedContent[ 'content_data'] = unCombinedScannedData
            
            unosContenidosIntercambio = self.fObtenerTodosContenidosIntercambioNoExcluidos()
            
            if not unosContenidosIntercambio:
                return unCombinedUploadedContent
            
            
            
            unasCombinedStrings       = unCombinedScannedData[ 'symbols']
            unasCombinedStringsDict   = unCombinedScannedData[ 'symbols_dict']
            
            for unaCombinedString in unasCombinedStrings:
                unSymbol = unaCombinedString.get( cScannedKeys_String_Symbol, '')
                if unSymbol:
                    unasCombinedStringsDict[ unSymbol] = unaCombinedString
            
            unosCombinedLanguages                      = set()
            unosCombinedModules                        = set()    
            
      
            for unContenidoIntercambio in unosContenidosIntercambio:
                
                unContenido = unContenidoIntercambio.fContenido()
                
                if unContenido:
                    
                    aScannedData = unContenido.get( 'content_data', None)
                    if aScannedData:
                        
                        unosLenguages         = aScannedData[ 'languages']
                        unosModules           = aScannedData[ 'modules']
                        unasScannedStrings    = aScannedData[ 'symbols']
    
                        unosCombinedLanguages.update( unosLenguages)
                        unosCombinedModules.update(   unosModules)
                        
                        unCombinedScannedData[ 'num_symbol_errors'] += aScannedData.get( 'num_symbol_errors', 0)     
                        
                        
                        someLanguagesDetails = aScannedData.get( 'languages_details', None)
                        if someLanguagesDetails:
                            
                            someCombinedLanguagesDetails = unCombinedScannedData.get( 'languages_details', None)
                            
                            if someCombinedLanguagesDetails == None:
                                someCombinedLanguagesDetails = { }
                                unCombinedScannedData[ 'languages_details'] = someCombinedLanguagesDetails
                            
                            for aLanguageDetailCode in someLanguagesDetails.keys():
                                
                                aLanguageDetail = someLanguagesDetails.get( aLanguageDetailCode, None)
                                
                                if not someCombinedLanguagesDetails.has_key( aLanguageDetailCode):
                                    
                                    someCombinedLanguagesDetails[ aLanguageDetailCode] = aLanguageDetail.copy()
                                                            
                         
                        
                        
                        if unasScannedStrings:
                                               
                            for unaScannedString in unasScannedStrings:
                                
                                unaStringSymbol = unaScannedString.get( cScannedKeys_String_Symbol, None)
                                
                                if unaStringSymbol:
                                    
                                    unosScannedModules       = unaScannedString.get( cScannedKeys_String_Modules, None) or set()
                                    unosScannedSources       = unaScannedString.get( cScannedKeys_String_Sources, None) or []
                                    unosScannedStringErrors  = unaScannedString.get( cScannedKeys_String_Errors,  None) or []
                                    
                                    unaCombinedString = unasCombinedStringsDict.get( unaStringSymbol, None)
                                    
                                    if unaCombinedString == None:
                                        
                                        unaCombinedString = self.fNewVoidScannedString()
                                        
                                        unosScannedStringNombresModulos = set( )
                                        for aScannedModuleIndex in unosScannedModules:
                                            if aScannedModuleIndex < len( unosModules):
                                                unosScannedStringNombresModulos.add( unosModules[ aScannedModuleIndex])
                                                
                                        unosCombinedModules.update( unosScannedStringNombresModulos)
                                                
                                        unaCombinedString[ cScannedKeys_String_Symbol]  = unaStringSymbol
                                        unaCombinedString[ cScannedKeys_String_Modules] = unosScannedStringNombresModulos
                                        unaCombinedString[ cScannedKeys_String_Sources] = unosScannedSources[:] 
                                        unaCombinedString[ cScannedKeys_String_Errors]  = unosScannedStringErrors[:]  
                                        
                                        unasCombinedStrings.append( unaCombinedString)
                                        unasCombinedStringsDict[ unaStringSymbol] = unaCombinedString
                                        
                                    else:
                                        
                                        if unosScannedModules:
                                            
                                            unosScannedStringNombresModulos = set( )
                                            for aScannedModuleIndex in unosScannedModules:
                                                if aScannedModuleIndex < len( unosModules):
                                                    unosScannedStringNombresModulos.add( unosModules[ aScannedModuleIndex])
                                            
                                            unosCombinedModules.update( unosScannedStringNombresModulos)
                                            
                                            unosStringCombinedModules = unaCombinedString.get( cScannedKeys_String_Modules, None)
                                            if unosStringCombinedModules == None:
                                                unaCombinedString[ cScannedKeys_String_Modules] = unosScannedStringNombresModulos.copy()
                                            else:
                                                unosStringCombinedModules.update( unosScannedStringNombresModulos)
                                                
                                        if unosScannedSources:
                                            unosStringCombinedSources = unaCombinedString.get( cScannedKeys_String_Sources, None)
                                            if unosStringCombinedSources == None:
                                                unaCombinedString[ cScannedKeys_String_Sources] = unosScannedSources[:]
                                            else:
                                                for aStringSource in unosScannedSources:
                                                    if not ( aStringSource in unosStringCombinedSources):
                                                        unosStringCombinedSources.append( aStringSource)
                                                        
                                        if unosScannedStringErrors:
                                            unosStringCombinedErrors = unaCombinedString.get( cScannedKeys_String_Errors, None)
                                            if unosStringCombinedErrors == None:
                                                unaCombinedString[ cScannedKeys_String_Errors] = unosScannedStringErrors[:]
                                            else:
                                                for aStringError in unosScannedStringErrors:
                                                    if not ( aStringError in unosStringCombinedErrors):
                                                        unosStringCombinedErrors.append( aStringError)
                                                
                                        
                                        
                                    someScannedStringTranslations   = unaScannedString.get(  cScannedKeys_String_Translations, None)
                                            
                                    someCombinedStringTranslations  = unaCombinedString.get( cScannedKeys_String_Translations, None)
                                    
                                    unosLenguagesInScannedString = someScannedStringTranslations.keys()
                                    
                                    
                                    
                                    if unosLenguagesInScannedString:
                                        
                                        unosCombinedLanguages.update( unosLenguagesInScannedString)
                                        
                                        for unScannedLenguage in unosLenguagesInScannedString:
                                                 
                                            unaScannedTranslation = someScannedStringTranslations.get( unScannedLenguage, None)
                                            if unaScannedTranslation:
                                                
                                                unScannedTranslationTranslation = unaScannedTranslation.get( cScannedKeys_Translation_Translation, None) or ''
                                                unScannedTranslationStatus      = unaScannedTranslation.get( cScannedKeys_Translation_Status,      None) or ''
                                                unScannedTranslationFlags       = unaScannedTranslation.get( cScannedKeys_Translation_Flags,       None) or ''
                                                unScannedTranslationComment     = unaScannedTranslation.get( cScannedKeys_Translation_Comment,     None) or ''
                                                unScannedTranslationErrors      = unaScannedTranslation.get( cScannedKeys_Translation_Errors,      None) or []
                                                
                                                unScannedTranslationCreationDate     = unaScannedTranslation.get( cScannedKeys_Translation_CreationDate,     None) or ''
                                                unScannedTranslationCreator          = unaScannedTranslation.get( cScannedKeys_Translation_Creator,          None) or ''
                                                unScannedTranslationTranslationDate  = unaScannedTranslation.get( cScannedKeys_Translation_TranslationDate,  None) or ''
                                                unScannedTranslationTranslator       = unaScannedTranslation.get( cScannedKeys_Translation_Translator,       None) or ''
                                                unScannedTranslationReviewDate       = unaScannedTranslation.get( cScannedKeys_Translation_ReviewDate,       None) or ''
                                                unScannedTranslationReviewer         = unaScannedTranslation.get( cScannedKeys_Translation_Reviewer,         None) or ''
                                                unScannedTranslationDefinitiveDate   = unaScannedTranslation.get( cScannedKeys_Translation_DefinitiveDate,   None) or ''
                                                unScannedTranslationCoordinator      = unaScannedTranslation.get( cScannedKeys_Translation_Coordinator,      None) or ''
                                                
                                                
                                                unaCombinedTranslation = someCombinedStringTranslations.get( unScannedLenguage, None)
                                                
                                                if unaCombinedTranslation == None:
                                                    unaCombinedTranslation = self.fNewVoidScannedTranslation()
                                                    unaCombinedTranslation[ cScannedKeys_Translation_Translation] = unScannedTranslationTranslation
                                                    unaCombinedTranslation[ cScannedKeys_Translation_Status]      = unScannedTranslationStatus
                                                    unaCombinedTranslation[ cScannedKeys_Translation_Flags]       = unScannedTranslationFlags
                                                    unaCombinedTranslation[ cScannedKeys_Translation_Comment]     = unScannedTranslationComment
                                                    unaCombinedTranslation[ cScannedKeys_Translation_Errors]      = unScannedTranslationErrors

                                                    if unScannedTranslationCreationDate and unScannedTranslationCreator:
                                                        unaCombinedTranslation[ cScannedKeys_Translation_CreationDate   ]      = unScannedTranslationCreationDate
                                                        unaCombinedTranslation[ cScannedKeys_Translation_Creator        ]      = unScannedTranslationCreator
                                                        
                                                    if unScannedTranslationTranslationDate and unScannedTranslationTranslator:
                                                        unaCombinedTranslation[ cScannedKeys_Translation_TranslationDate]      = unScannedTranslationTranslationDate
                                                        unaCombinedTranslation[ cScannedKeys_Translation_Translator     ]      = unScannedTranslationTranslator

                                                    if unScannedTranslationReviewDate and unScannedTranslationReviewer:
                                                        unaCombinedTranslation[ cScannedKeys_Translation_ReviewDate     ]      = unScannedTranslationReviewDate
                                                        unaCombinedTranslation[ cScannedKeys_Translation_Reviewer       ]      = unScannedTranslationReviewer

                                                    if unScannedTranslationDefinitiveDate and unScannedTranslationCoordinator:
                                                        unaCombinedTranslation[ cScannedKeys_Translation_DefinitiveDate ]      = unScannedTranslationDefinitiveDate
                                                        unaCombinedTranslation[ cScannedKeys_Translation_Coordinator    ]      = unScannedTranslationCoordinator
                                                   
                                                    someCombinedStringTranslations[ unScannedLenguage] = unaCombinedTranslation
                                                    
                                                else:
                                                    
                                                    unaCombinedTranslationTranslation = unaCombinedTranslation.get( cScannedKeys_Translation_Translation, None) or ''
                                                    unaCombinedTranslationStatus      = unaCombinedTranslation.get( cScannedKeys_Translation_Status, None) or ''
                                                    unaCombinedTranslationErrors      = unaCombinedTranslation.get( cScannedKeys_Translation_Errors, None) or []
                                                    
                                                    if unScannedTranslationTranslation and not unaCombinedTranslationTranslation:
                                                        
                                                        someCombinedStringTranslations[ unScannedLenguage] = unaScannedTranslation.copy()
                                                    
                                                    elif ( not unScannedTranslationTranslation) and unaCombinedTranslationTranslation:
                                                        
                                                        pass
                                                
                                                    else:
                                                        
                                                        if ( not unScannedTranslationErrors) and unaCombinedTranslationErrors:
                                                            
                                                            someCombinedStringTranslations[ unScannedLenguage] = unaScannedTranslation.copy()
                                                        
                                                        elif unScannedTranslationErrors and not unaCombinedTranslationErrors:
                                                            
                                                            pass
                                                        
                                                        else:         
                                                            
                                                            if unScannedTranslationStatus and not unaCombinedTranslationStatus:
                                                                
                                                                someCombinedStringTranslations[ unScannedLenguage] = unaScannedTranslation.copy()
                                                            
                                                            elif ( not unScannedTranslationStatus) and unaCombinedTranslationStatus:
                                                                
                                                                pass
                                                            
                                                            else:
                                                                
                                                                unIndexScannedTranslationStatus = -1
                                                                if unScannedTranslationStatus in [ cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva,]:
                                                                    unIndexScannedTranslationStatus = [ cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva,].index( unScannedTranslationStatus)
                                                                
                                                                unIndexCombinedTranslationStatus = -1
                                                                if unIndexCombinedTranslationStatus in [ cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva,]:
                                                                    unIndexCombinedTranslationStatus = [ cEstadoTraduccionRevisada, cEstadoTraduccionDefinitiva,].index( unScannedTranslationStatus)
                                                        
                                                                if unIndexScannedTranslationStatus > unIndexCombinedTranslationStatus:
                                                                    
                                                                    someCombinedStringTranslations[ unScannedLenguage] = unaScannedTranslation.copy()
                                                                    
                                                                elif unIndexScannedTranslationStatus < unIndexCombinedTranslationStatus:
                                                                    
                                                                    pass
                                                                
                                                                else: 
                                                                
                                                                    someCombinedStringTranslations[ unScannedLenguage] = unaScannedTranslation.copy()
                                                            
   
                                                    unaCombinedTranslationCreationDate     = unaCombinedTranslation.get( cScannedKeys_Translation_CreationDate,     None) or ''
                                                    unaCombinedTranslationCreator          = unaCombinedTranslation.get( cScannedKeys_Translation_Creator,          None) or ''
                                                    unaCombinedTranslationTranslationDate  = unaCombinedTranslation.get( cScannedKeys_Translation_TranslationDate,  None) or ''
                                                    unaCombinedTranslationTranslator       = unaCombinedTranslation.get( cScannedKeys_Translation_Translator,       None) or ''
                                                    unaCombinedTranslationReviewDate       = unaCombinedTranslation.get( cScannedKeys_Translation_ReviewDate,       None) or ''
                                                    unaCombinedTranslationReviewer         = unaCombinedTranslation.get( cScannedKeys_Translation_Reviewer,         None) or ''
                                                    unaCombinedTranslationDefinitiveDate   = unaCombinedTranslation.get( cScannedKeys_Translation_DefinitiveDate,   None) or ''
                                                    unaCombinedTranslationCoordinator      = unaCombinedTranslation.get( cScannedKeys_Translation_Coordinator,      None) or ''
            
                                                    if ( unScannedTranslationCreationDate and unScannedTranslationCreator) and ( ( not unaCombinedTranslationCreationDate) or ( not unaCombinedTranslationCreator)):
                                                        unaCombinedTranslation[ cScannedKeys_Translation_CreationDate   ]      = unScannedTranslationCreationDate
                                                        unaCombinedTranslation[ cScannedKeys_Translation_Creator        ]      = unScannedTranslationCreator
                                                        
                                                    if ( unScannedTranslationTranslationDate and unScannedTranslationTranslator) and ( ( not unaCombinedTranslationTranslationDate) or ( not unaCombinedTranslationTranslator)):
                                                        unaCombinedTranslation[ cScannedKeys_Translation_TranslationDate]      = unScannedTranslationTranslationDate
                                                        unaCombinedTranslation[ cScannedKeys_Translation_Translator     ]      = unScannedTranslationTranslator

                                                    if ( unScannedTranslationReviewDate and unScannedTranslationReviewer) and ( ( not unaCombinedTranslationReviewDate) or ( not unaCombinedTranslationCreator)):
                                                        unaCombinedTranslation[ cScannedKeys_Translation_ReviewDate     ]      = unScannedTranslationReviewDate
                                                        unaCombinedTranslation[ cScannedKeys_Translation_Reviewer       ]      = unScannedTranslationReviewer

                                                    if ( unScannedTranslationDefinitiveDate and unScannedTranslationCoordinator) and ( ( not unaCombinedTranslationDefinitiveDate) or ( not unaCombinedTranslationCoordinator)):
                                                        unaCombinedTranslation[ cScannedKeys_Translation_DefinitiveDate ]      = unScannedTranslationDefinitiveDate
                                                        unaCombinedTranslation[ cScannedKeys_Translation_Coordinator    ]      = unScannedTranslationCoordinator
                                    
                       
                                                        
            unCombinedScannedData[ 'languages'] = sorted( unosCombinedLanguages)
            unCombinedScannedData[ 'modules']   = sorted( unosCombinedModules)
            
            for unaCombinedString in unasCombinedStrings:
                
                unosNombresModulos = unaCombinedString.get( cScannedKeys_String_Modules, set())
                if unosNombresModulos:
                    unosNombresModulos = sorted( unosNombresModulos)
                unaCombinedString[ cScannedKeys_String_Modules]  = unosNombresModulos  
            
                         
            return unCombinedUploadedContent
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            if cLogEachExecution_fCombinedContenidosIntercambio:
                unExecutionRecord and unExecutionRecord.pClearLoggedAll()

                                           
                                

    
    
                
                

    security.declareProtected( permissions.View, 'fInformesTodosContenidosIntercambio')
    def fInformesTodosContenidosIntercambio( self, theParentExecutionRecord=None):
   
        unExecutionRecord = self.fStartExecution( 'method',  'fInformesTodosContenidosIntercambio', theParentExecutionRecord,  False, ) 
           
        try:
            unosInformesContenidosIntercambio = [ ]
            
            unosContenidosIntercambio = self.fObtenerTodosContenidosIntercambio()
            if not unosContenidosIntercambio:
                return unosInformesContenidosIntercambio
            
            for unContenidoIntercambio in unosContenidosIntercambio:
                unInformeContenidoIntercambio = unContenidoIntercambio.fInformeContenidoIntercambio( theParentExecutionRecord)
                if unInformeContenidoIntercambio:
                    unosInformesContenidosIntercambio.append( unInformeContenidoIntercambio)
                    
            return unosInformesContenidosIntercambio
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
       
        
                  
  
    
    

                
                
    
    security.declareProtected( permissions.View, 'fInformeContenidosImportacion')    
    def fInformeContenidosImportacion( self, theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fInformeContenidosImportacion', theParentExecutionRecord,  False, ) 
           
        try:
            unInforme = self.fNewVoidContenidoIntercambioReport()
            
            unInforme.update( {
                'title':                            self.Title(),
                'description':                      self.Description(),
                'absolute_url':                     self.absolute_url(),
            })

             
            
            unContenido = self.fCombinedContenidosIntercambio( unExecutionRecord)
            if not unContenido:
                return unInforme
            
            aScannedData = unContenido.get( 'content_data', None)
            if not aScannedData:
                return None
            
                        
            unasScannedStrings           = aScannedData[ 'symbols']
            unosScannedLanguages         = aScannedData[ 'languages']
                
 
            someLanguageNamesAndFlags = self.fLanguagesNamesAndFlagsPorCodigo().copy()
            
            unInforme[ 'language_names_and_flags'] = someLanguageNamesAndFlags
            
            
            someLanguagesDetails = aScannedData.get( 'languages_details', None)
            if someLanguagesDetails:
                
                for aLanguageDetailCode in someLanguagesDetails.keys():
                    
                    if not someLanguageNamesAndFlags.has_key( aLanguageDetailCode):
                        
                        aLanguageDetail = someLanguagesDetails.get( aLanguageDetailCode, None)
                        if aLanguageDetail:
                            unLanguageNamesAndFlag = {
                                'english'       :  aLanguageDetail.get( 'english_name', aLanguageDetailCode), 
                                'native'        :  aLanguageDetail.get(  'nombre_nativo_de_idioma', aLanguageDetail.get( 'english_name', aLanguageDetailCode)), 
                            }
                            someLanguageNamesAndFlags[ aLanguageDetailCode] = unLanguageNamesAndFlag
            
            
            
            
            
            unInforme[ 'languages'] = sorted( unosScannedLanguages)
            unInforme[ 'modules']   = sorted( aScannedData[ 'modules'])            

           
            unInforme[ 'num_symbol_errors'] = aScannedData[ 'num_symbol_errors']
            
            
            
            unosNumTranslationsByLanguage   = unInforme[ 'num_translated_by_language']
            unosNumEncodingErrorsByLanguage = unInforme[ 'num_encoding_errors_by_language']
            
            
            
            
            for unLanguage in unosScannedLanguages:
                unosNumTranslationsByLanguage[      unLanguage] = 0    
                unosNumEncodingErrorsByLanguage[    unLanguage] = 0   
                   
                
                
            unNumStrings = 0   
                
            for unaScannedString in unasScannedStrings:
                
                if unaScannedString:
                    
                    unStringSymbol  = unaScannedString.get( cScannedKeys_String_Symbol, None)
                    if unStringSymbol:
                        
                        unNumStrings += 1
                        
                        unosStringErrors       = unaScannedString.get( cScannedKeys_String_Errors, None)
                        if unosStringErrors:
                            unInforme[ 'num_string_errors'] += 1
                            
        
                        unasScannedTranslations = unaScannedString[ cScannedKeys_String_Translations]
                        
                        unosStringLenguages    = unasScannedTranslations.keys()   
                        
                        for unLenguage in unosStringLenguages:
                            
                            unaScannedTranslation = unasScannedTranslations.get( unLenguage, None)
                            if unaScannedTranslation:
                                
                                aTranslation          = unaScannedTranslation.get( cScannedKeys_Translation_Translation, None)
                                unosTranslationErrors = unaScannedTranslation.get( cScannedKeys_Translation_Errors, None)
                                
                                if aTranslation:
                                    unosNumTranslationsByLanguage[ unLenguage]   = unosNumTranslationsByLanguage.get( unLenguage, 0) + 1
                            
                                if unosTranslationErrors:
                                    unosNumEncodingErrorsByLanguage[ unLenguage] = unosNumEncodingErrorsByLanguage.get( unLenguage, 0) + 1
               
                 
                            
            unInforme[ 'num_strings'] = unNumStrings
                            
            unPercentStringErrors = 100
            if unNumStrings:
                unPercentStringErrors =  int( ( ( 0.0 + unInforme[ 'num_string_errors']) / unNumStrings) * 100)
                
            unInforme[ 'percent_string_errors'] =  unPercentStringErrors   
                
            
            for unLenguage in unosScannedLanguages:
                
                unNumeroTraducciones = unosNumTranslationsByLanguage[ unLenguage]
                
                if not unNumeroTraducciones:
                    unPercentTranslated  = 0
                    unPercentPending     = 100
                    unPercentEncodingErrors = 0
                    
                else:
                    unPercentTranslated = int( ( ( 0.0 + unNumeroTraducciones) / unNumStrings) * 100)
                    if not unPercentTranslated:
                        unPercentTranslated = 1
                    unPercentPending = 100 - unPercentTranslated
                    unPercentEncodingErrors = int( ( ( 0.0 + unosNumEncodingErrorsByLanguage[ unLenguage]) / unNumStrings) * 100)
                    
                unInforme[ 'num_pending_by_language'][             unLenguage] = unNumStrings - unNumeroTraducciones
                unInforme[ 'percent_pending_by_language'][         unLenguage] = unPercentPending
                unInforme[ 'percent_translated_by_language'][      unLenguage] = unPercentTranslated
                unInforme[ 'percent_encoding_errors_by_language'][ unLenguage] = unPercentEncodingErrors
                        
            return unInforme
         
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
       
        
                          
                
                
                
                
    
    #security.declareProtected( permissions.View, 'fInformeCambios')    
    #def fInformeCambios( self, theParentExecutionRecord=None):
                        
                
        #unExecutionRecord = self.fStartExecution( 'method',  'fInformeCambios', theParentExecutionRecord,  False, ) 
           
        #try:
                
            #unInforme = self.fNewVoidCambiosInformacionReport()
                
            #return unInforme
         
        #finally:
            #unExecutionRecord and unExecutionRecord.pEndExecution()
       
        
            
            
            
                         
                
    
    security.declareProtected( permissions.View, 'fInformeContenidosImportacion')    
    def fInformeContenidosImportacion( self, theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fInformeContenidosImportacion', theParentExecutionRecord,  False, ) 
           
        try:
            unInforme = self.fNewVoidContenidoIntercambioReport()
            
            unInforme.update( {
                'title':                            self.Title(),
                'description':                      self.Description(),
                'absolute_url':                     self.absolute_url(),
            })

             
            
            unContenido = self.fCombinedContenidosIntercambio( unExecutionRecord)
            if not unContenido:
                return unInforme
            
            aScannedData = unContenido.get( 'content_data', None)
            if not aScannedData:
                return None
            
                        
            unasScannedStrings           = aScannedData[ 'symbols']
            unosScannedLanguages         = aScannedData[ 'languages']
                
 
            someLanguageNamesAndFlags = self.fLanguagesNamesAndFlagsPorCodigo().copy()
            
            unInforme[ 'language_names_and_flags'] = someLanguageNamesAndFlags
            
            
            someLanguagesDetails = aScannedData.get( 'languages_details', None)
            if someLanguagesDetails:
                
                for aLanguageDetailCode in someLanguagesDetails.keys():
                    
                    if not someLanguageNamesAndFlags.has_key( aLanguageDetailCode):
                        
                        aLanguageDetail = someLanguagesDetails.get( aLanguageDetailCode, None)
                        if aLanguageDetail:
                            unLanguageNamesAndFlag = {
                                'english'       :  aLanguageDetail.get( 'english_name', aLanguageDetailCode), 
                                'native'        :  aLanguageDetail.get(  'nombre_nativo_de_idioma', aLanguageDetail.get( 'english_name', aLanguageDetailCode)), 
                            }
                            someLanguageNamesAndFlags[ aLanguageDetailCode] = unLanguageNamesAndFlag
            
            
            
            
            
            unInforme[ 'languages'] = sorted( unosScannedLanguages)
            unInforme[ 'modules']   = sorted( aScannedData[ 'modules'])            

           
            unInforme[ 'num_symbol_errors'] = aScannedData[ 'num_symbol_errors']
            
            
            
            unosNumTranslationsByLanguage   = unInforme[ 'num_translated_by_language']
            unosNumEncodingErrorsByLanguage = unInforme[ 'num_encoding_errors_by_language']
            
            
            
            
            for unLanguage in unosScannedLanguages:
                unosNumTranslationsByLanguage[      unLanguage] = 0    
                unosNumEncodingErrorsByLanguage[    unLanguage] = 0   
                   
                
                
            unNumStrings = 0   
                
            for unaScannedString in unasScannedStrings:
                
                if unaScannedString:
                    
                    unStringSymbol  = unaScannedString.get( cScannedKeys_String_Symbol, None)
                    if unStringSymbol:
                        
                        unNumStrings += 1
                        
                        unosStringErrors       = unaScannedString.get( cScannedKeys_String_Errors, None)
                        if unosStringErrors:
                            unInforme[ 'num_string_errors'] += 1
                            
        
                        unasScannedTranslations = unaScannedString[ cScannedKeys_String_Translations]
                        
                        unosStringLenguages    = unasScannedTranslations.keys()   
                        
                        for unLenguage in unosStringLenguages:
                            
                            unaScannedTranslation = unasScannedTranslations.get( unLenguage, None)
                            if unaScannedTranslation:
                                
                                aTranslation          = unaScannedTranslation.get( cScannedKeys_Translation_Translation, None)
                                unosTranslationErrors = unaScannedTranslation.get( cScannedKeys_Translation_Errors, None)
                                
                                if aTranslation:
                                    unosNumTranslationsByLanguage[ unLenguage]   = unosNumTranslationsByLanguage.get( unLenguage, 0) + 1
                            
                                if unosTranslationErrors:
                                    unosNumEncodingErrorsByLanguage[ unLenguage] = unosNumEncodingErrorsByLanguage.get( unLenguage, 0) + 1
               
                 
                            
            unInforme[ 'num_strings'] = unNumStrings
                            
            unPercentStringErrors = 100
            if unNumStrings:
                unPercentStringErrors =  int( ( ( 0.0 + unInforme[ 'num_string_errors']) / unNumStrings) * 100)
                
            unInforme[ 'percent_string_errors'] =  unPercentStringErrors   
                
            
            for unLenguage in unosScannedLanguages:
                
                unNumeroTraducciones = unosNumTranslationsByLanguage[ unLenguage]
                
                if not unNumeroTraducciones:
                    unPercentTranslated  = 0
                    unPercentPending     = 100
                    unPercentEncodingErrors = 0
                    
                else:
                    unPercentTranslated = int( ( ( 0.0 + unNumeroTraducciones) / unNumStrings) * 100)
                    if not unPercentTranslated:
                        unPercentTranslated = 1
                    unPercentPending = 100 - unPercentTranslated
                    unPercentEncodingErrors = int( ( ( 0.0 + unosNumEncodingErrorsByLanguage[ unLenguage]) / unNumStrings) * 100)
                    
                unInforme[ 'num_pending_by_language'][             unLenguage] = unNumStrings - unNumeroTraducciones
                unInforme[ 'percent_pending_by_language'][         unLenguage] = unPercentPending
                unInforme[ 'percent_translated_by_language'][      unLenguage] = unPercentTranslated
                unInforme[ 'percent_encoding_errors_by_language'][ unLenguage] = unPercentEncodingErrors
                        
            return unInforme
         
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
       
        
                          
            
    
    


    
    

    
    security.declareProtected( permissions.ModifyPortalContent, 'fReutilizarImportacion')
    def fReutilizarImportacion( self , thePermissionsCache=None, theRolesCache=None, theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fReutilizarImportacion', theParentExecutionRecord, True, { 'log_what': 'details', 'log_when': True, }) 

        from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators  import cModificationKind_CreateSubElement, cModificationKind_Create, cModificationKind_ChangeValues

        try:
            
            try:
                
                unPermissionsCache = fDictOrNew( thePermissionsCache)
                unRolesCache       = fDictOrNew( theRolesCache)
            
                unUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_ReuseTRAImportacion, 
                    theElementsBindings     = { cBoundObject: self,},
                    theRulesToCollect       = [ ], 
                    thePermissionsCache     = unPermissionsCache, 
                    theRolesCache           = unRolesCache, 
                    theParentExecutionRecord= unExecutionRecord
                )
                if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                    return False
                        
                                    
                aIdentificadorElementoProgreso = self.getIdentificadorElementoProgreso()
                if aIdentificadorElementoProgreso:
                    
                    self.setIdentificadorElementoProgreso( '')
                    
                    
                    aModelDDvlPloneTool_Mutators = self.fModelDDvlPloneTool().fModelDDvlPloneTool_Mutators( self)
                   
                    aReport = aModelDDvlPloneTool_Mutators.fNewVoidChangeValuesReport()
                    someFieldReports    = aReport.get( 'field_reports')
                    aFieldReportsByName = aReport.get( 'field_reports_by_name')       

                    aReportForField = { 'attribute_name': 'identificadorElementoProgreso', 'effect': 'changed', 'new_value': '', 'previous_value': aIdentificadorElementoProgreso,}                                                                                                                        
                    
                    someFieldReports.append( aReportForField)
                    aFieldReportsByName[ 'identificadorElementoProgreso'] = aReportForField
                    
                    aModelDDvlPloneTool_Mutators.pSetAudit_Modification( self, cModificationKind_ChangeValues, aReport)  
                    
                    self.getCatalogo().pFlushCachedTemplates_All()                            
                
                    transaction.commit()
                    logging.getLogger( 'gvSIGi18n').info( "COMMIT TRAImportacion::fReutilizarImportacion %s" % self.fPhysicalPathString())
                    
                return True
            
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during TRAImportacion::fReutilizarImportacion %s \n'  % self.fPhysicalPathString()
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   

                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return False
        
             
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
            unExecutionRecord and unExecutionRecord.pClearLoggedAll()

                            
        
            
    
    security.declarePublic( 'fExtraLinks')    
    def fExtraLinks( self):
        
        unosExtraLinks = TRAArquetipo.fExtraLinks( self)
        if not unosExtraLinks:
            unosExtraLinks = [ ]
        
        unaURL = self.absolute_url()
        if not unaURL:
            return unosExtraLinks
        

        unExtraLink = self.fNewVoidExtraLink()
        unExtraLink.update( {
            'label'   : self.fTranslateI18N( 'plone', 'Summary', 'Summary-',),
            'href'    : '%s/TRAImportacionContenidosSumario/' % unaURL,
            'icon'    : '',
            'domain'  : 'plone',
            'msgid'   : 'Summary',
        })
        unosExtraLinks.append( unExtraLink)
                            
        unExtraLink = self.fNewVoidExtraLink()
        unExtraLink.update( {
            'label'   : self.fTranslateI18N( 'plone', 'Details', 'Details-',),
            'href'    : '%s/TRAImportacionContenidosDetalle/' % unaURL,
            'icon'    : '',
            'domain'  : 'plone',
            'msgid'   : 'Details',
        })
        unosExtraLinks.append( unExtraLink)
                            
            
        unElementoContenidoXML = self.fObtenerContenidoXML()
        if not ( unElementoContenidoXML == None):
            unExtraLink = self.fNewVoidExtraLink()
            unExtraLink.update( {
                'label'   : self.fTranslateI18N( 'plone', 'XML Data', 'XML Data-',),
                'href'    : '%s/TRAContenidoXML/' % unElementoContenidoXML.absolute_url(),
                'icon'    : 'tracontenidoxml.gif',
                'domain'  : 'plone',
                'msgid'   : 'XML Data',
            })
            unosExtraLinks.append( unExtraLink)        
            
                                        
        unElementoProgreso = self.fDeriveElementoProgreso()
        if not ( unElementoProgreso == None):
            unExtraLink = self.fNewVoidExtraLink()
            unExtraLink.update( {
                'label'   : self.fTranslateI18N( 'plone', 'Progress', 'Progress-',),
                'href'    : '%s/TRAProgressResults/' % unElementoProgreso.absolute_url(),
                'icon'    : 'traprogreso.gif',
                'domain'  : 'plone',
                'msgid'   : 'Progress',
            })
            unosExtraLinks.append( unExtraLink)        
            


        return unosExtraLinks
    
    
    
    
    
    
    
    