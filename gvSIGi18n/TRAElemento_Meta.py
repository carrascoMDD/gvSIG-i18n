
# Copyright (c) 2013 by 2008, 2009, 2010, 2011 Conselleria de Infraestructuras
# y Transporte de la Generalidad Valenciana
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
# Authors: 
# Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana, Model Driven Development sl, Antonio Carrasco Valero
#
#

__author__ = """Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
<gvSIGi18n@gvSIG.org>, Model Driven Development sl <gvSIGi18n@ModelDD.org>,
Antonio Carrasco Valero <carrasco@ModelDD.org>"""

__docformat__ = 'plaintext'

from AccessControl                  import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.gvSIGi18n.config import *


# Classes added here during runtime will be acceptable roots,
# after invocation of the fParentArchetypeClassNames_ResetCache method
#
gAdditionalParentArchetypeClassNames = [ ]



# Private Cache of class names
# 
gParentArchetypeClassNamesCache      = [ ]




class TRAElemento_Meta:            

    """
    """
    security = ClassSecurityInfo()


    



  
  
  
    security.declarePrivate('fParentArchetypeClassNames')
    def fParentArchetypeClassNames( self):
    
        if gParentArchetypeClassNamesCache:
            return gParentArchetypeClassNamesCache
        
        return self.fParentArchetypeClassNames_ResetCache()
        
        
        
        
        
        
        
    security.declarePrivate('fParentArchetypeClassNames_ResetCache')
    def fParentArchetypeClassNames_ResetCache( self):
    
        aWorkingCopy = self.fArchetypeClassNames()[:]
        
        # Thread safety to be assured here for cases when simultaneusly:
        #
        # Others may be adding to the gAdditionalParentArchetypeClassNames
        # Others may also invoke this method
        #
        if gAdditionalParentArchetypeClassNames:
            aWorkingCopy += gAdditionalParentArchetypeClassNames
        
        gParentArchetypeClassNamesCache = aWorkingCopy
        
        return gParentArchetypeClassNamesCache
        
            
    
    
    
    security.declarePrivate('fArchetypeSchemaByName')
    def fArchetypeSchemaByName( self, theMetaTypeName):
        if not theMetaTypeName:
            return None    
    
        aMetaType = self.fArchetypeClassByName( theMetaTypeName)
        if not aMetaType:
            return None
        return getattr( aMetaType, 'schema', None)
  

    security.declarePrivate('fArchetypeClassNames')
    def fArchetypeClassNames( self):
        return [ 
            'TRACadena',
            'TRACatalogo',
            'TRAColeccionCadenas',
            'TRAColeccionContribuciones',
            'TRAColeccionIdiomas',
            'TRAColeccionImportaciones',
            'TRAColeccionInformes',
            'TRAColeccionModulos',
            'TRAColeccionProgresos',
            'TRAColeccionSolicitudesCadenas',
            'TRAConfiguracionExportacion',
            'TRAConfiguracionImportacion',
            'TRAConfiguracionInvalidacionInformes',
            'TRAConfiguracionPaginaTraducciones',
            'TRAConfiguracionPerfilEjecucion',
            'TRAConfiguracionPermisos',
            'TRAConfiguracionSolicitudesCadenas',
            'TRAConfiguracionVarios',
            'TRAContenidoIntercambio',
            'TRAContenidoXML',
            'TRAContribuciones',
            'TRAIdioma',
            'TRAImportacion',
            'TRAInforme',
            'TRAModulo',
            'TRAParametrosControlProgreso',
            'TRAProgreso',
            'TRASimbolosOrdenados',
            'TRASolicitudCadena',
            'TRATraduccion',
 
        ]
        
        
                    
    security.declarePrivate('fArchetypeClassByName')
    def fArchetypeClassByName( self, theMetaTypeName):
        if not theMetaTypeName:
            return None    

        try:            
            
            if theMetaTypeName == 'TRACadena':
                from Products.gvSIGi18n.TRACadena         import TRACadena
                return TRACadena            

            if theMetaTypeName == 'TRACatalogo':
                from Products.gvSIGi18n.TRACatalogo         import TRACatalogo
                return TRACatalogo            

            if theMetaTypeName == 'TRAColeccionCadenas':
                from Products.gvSIGi18n.TRAColeccionCadenas         import TRAColeccionCadenas
                return TRAColeccionCadenas            

            if theMetaTypeName == 'TRAColeccionContribuciones':
                from Products.gvSIGi18n.TRAColeccionContribuciones         import TRAColeccionContribuciones
                return TRAColeccionContribuciones            

            if theMetaTypeName == 'TRAColeccionIdiomas':
                from Products.gvSIGi18n.TRAColeccionIdiomas         import TRAColeccionIdiomas
                return TRAColeccionIdiomas            

            if theMetaTypeName == 'TRAColeccionImportaciones':
                from Products.gvSIGi18n.TRAColeccionImportaciones         import TRAColeccionImportaciones
                return TRAColeccionImportaciones            

            if theMetaTypeName == 'TRAColeccionInformes':
                from Products.gvSIGi18n.TRAColeccionInformes         import TRAColeccionInformes
                return TRAColeccionInformes            

            if theMetaTypeName == 'TRAColeccionModulos':
                from Products.gvSIGi18n.TRAColeccionModulos         import TRAColeccionModulos
                return TRAColeccionModulos            

            if theMetaTypeName == 'TRAColeccionProgresos':
                from Products.gvSIGi18n.TRAColeccionProgresos         import TRAColeccionProgresos
                return TRAColeccionProgresos            

            if theMetaTypeName == 'TRAColeccionSolicitudesCadenas':
                from Products.gvSIGi18n.TRAColeccionSolicitudesCadenas         import TRAColeccionSolicitudesCadenas
                return TRAColeccionSolicitudesCadenas            

            if theMetaTypeName == 'TRAConfiguracionExportacion':
                from Products.gvSIGi18n.TRAConfiguracionExportacion         import TRAConfiguracionExportacion
                return TRAConfiguracionExportacion            

            if theMetaTypeName == 'TRAConfiguracionImportacion':
                from Products.gvSIGi18n.TRAConfiguracionImportacion         import TRAConfiguracionImportacion
                return TRAConfiguracionImportacion            

            if theMetaTypeName == 'TRAConfiguracionInvalidacionInformes':
                from Products.gvSIGi18n.TRAConfiguracionInvalidacionInformes         import TRAConfiguracionInvalidacionInformes
                return TRAConfiguracionInvalidacionInformes            

            if theMetaTypeName == 'TRAConfiguracionPaginaTraducciones':
                from Products.gvSIGi18n.TRAConfiguracionPaginaTraducciones         import TRAConfiguracionPaginaTraducciones
                return TRAConfiguracionPaginaTraducciones            

            if theMetaTypeName == 'TRAConfiguracionPerfilEjecucion':
                from Products.gvSIGi18n.TRAConfiguracionPerfilEjecucion         import TRAConfiguracionPerfilEjecucion
                return TRAConfiguracionPerfilEjecucion            

            if theMetaTypeName == 'TRAConfiguracionPermisos':
                from Products.gvSIGi18n.TRAConfiguracionPermisos         import TRAConfiguracionPermisos
                return TRAConfiguracionPermisos            

            if theMetaTypeName == 'TRAConfiguracionSolicitudesCadenas':
                from Products.gvSIGi18n.TRAConfiguracionSolicitudesCadenas         import TRAConfiguracionSolicitudesCadenas
                return TRAConfiguracionSolicitudesCadenas            

            if theMetaTypeName == 'TRAConfiguracionVarios':
                from Products.gvSIGi18n.TRAConfiguracionVarios         import TRAConfiguracionVarios
                return TRAConfiguracionVarios            

            if theMetaTypeName == 'TRAContenidoIntercambio':
                from Products.gvSIGi18n.TRAContenidoIntercambio         import TRAContenidoIntercambio
                return TRAContenidoIntercambio            

            if theMetaTypeName == 'TRAContenidoXML':
                from Products.gvSIGi18n.TRAContenidoXML         import TRAContenidoXML
                return TRAContenidoXML            

            if theMetaTypeName == 'TRAContribuciones':
                from Products.gvSIGi18n.TRAContribuciones         import TRAContribuciones
                return TRAContribuciones            

            if theMetaTypeName == 'TRAIdioma':
                from Products.gvSIGi18n.TRAIdioma         import TRAIdioma
                return TRAIdioma            

            if theMetaTypeName == 'TRAImportacion':
                from Products.gvSIGi18n.TRAImportacion         import TRAImportacion
                return TRAImportacion            

            if theMetaTypeName == 'TRAInforme':
                from Products.gvSIGi18n.TRAInforme         import TRAInforme
                return TRAInforme            

            if theMetaTypeName == 'TRAModulo':
                from Products.gvSIGi18n.TRAModulo         import TRAModulo
                return TRAModulo            

            if theMetaTypeName == 'TRAParametrosControlProgreso':
                from Products.gvSIGi18n.TRAParametrosControlProgreso         import TRAParametrosControlProgreso
                return TRAParametrosControlProgreso            

            if theMetaTypeName == 'TRAProgreso':
                from Products.gvSIGi18n.TRAProgreso         import TRAProgreso
                return TRAProgreso            

            if theMetaTypeName == 'TRASimbolosOrdenados':
                from Products.gvSIGi18n.TRASimbolosOrdenados         import TRASimbolosOrdenados
                return TRASimbolosOrdenados            

            if theMetaTypeName == 'TRASolicitudCadena':
                from Products.gvSIGi18n.TRASolicitudCadena         import TRASolicitudCadena
                return TRASolicitudCadena            

            if theMetaTypeName == 'TRATraduccion':
                from Products.gvSIGi18n.TRATraduccion         import TRATraduccion
                return TRATraduccion            

        except:
            None
       
        return None
            
