
# Copyright (c) 2009 by Conselleria de Infraestructuras y Transporte de la
# Generalidad Valenciana
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

schema = Schema((

),
)

TRAElemento_Meta_schema = BaseSchema.copy() +     schema.copy()


class TRAElemento_Meta:            

    """
    """
    security = ClassSecurityInfo()

    # This name appears in the 'add' box
    archetype_name = 'TRAElemento_Meta'
    
    meta_type = 'TRAElemento_Meta'
    portal_type = 'TRAElemento_Meta'

    schema = TRAElemento_Meta_schema

    
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
            'TRAColeccionIdiomas',
            'TRAColeccionImportaciones',
            'TRAColeccionInformes',
            'TRAColeccionModulos',
            'TRAColeccionSolicitudesCadenas',
            'TRAContenidoIntercambio',
            'TRAIdioma',
            'TRAImportacion',
            'TRAInforme',
            'TRAModulo',
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

            if theMetaTypeName == 'TRAColeccionSolicitudesCadenas':
                from Products.gvSIGi18n.TRAColeccionSolicitudesCadenas         import TRAColeccionSolicitudesCadenas
                return TRAColeccionSolicitudesCadenas            

            if theMetaTypeName == 'TRAContenidoIntercambio':
                from Products.gvSIGi18n.TRAContenidoIntercambio         import TRAContenidoIntercambio
                return TRAContenidoIntercambio            

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

            if theMetaTypeName == 'TRASolicitudCadena':
                from Products.gvSIGi18n.TRASolicitudCadena         import TRASolicitudCadena
                return TRASolicitudCadena            

            if theMetaTypeName == 'TRATraduccion':
                from Products.gvSIGi18n.TRATraduccion         import TRATraduccion
                return TRATraduccion            

        except:
            None
       
        return None
            
