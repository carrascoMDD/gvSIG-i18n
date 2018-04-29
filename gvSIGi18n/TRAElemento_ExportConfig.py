# -*- coding: utf-8 -*-
#
# File: TRAElemento_ExportConfig.py
#
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



class TRAElemento_ExportConfig:            

    """
    """
    security = ClassSecurityInfo()

    # This name appears in the 'add' box
    archetype_name = 'TRAElemento_ExportConfig'
    
    meta_type = 'TRAElemento_ExportConfig'
    portal_type = 'TRAElemento_ExportConfig'

    
    
    security.declarePublic('exportConfig')
    def exportConfig( self):
        return [
    {   'portal_types': [ 'TRACadena', ],
        'attrs':        [
            {   'name': 'title',
                'type': 'String',
            },
            {   'name': 'description',
                'type': 'Text',
            },
            {   'name': 'text',
                'type': 'Text',
            },
            {   'name': 'simbolo',
                'type': 'string',
            },
            {   'name': 'estadoCadena',
                'type': 'selection',
            },
            {   'name': 'fechaCreacionTextual',
                'type': 'string',
            },
            {   'name': 'usuarioCreador',
                'type': 'string',
            },
            {   'name': 'fechaCancelacionTextual',
                'type': 'string',
            },
            {   'name': 'nombresModulos',
                'type': 'string',
            },
            {   'name': 'referenciasFuentes',
                'type': 'string',
            },
            {   'name': 'pathDelRaiz',
                'type': 'string',
            },
        ],
        'traversals':   [
            {   'aggregation_name': 'traducciones',
                'subitems':         [
                    {   'portal_types': [ 'TRATraduccion', ],
                    },
                ],
            },
            {   'aggregation_name': 'archivos',
                'subitems':         [
                    {   'portal_types': [ 'File', ],
                    },
                ],
            },
            {   'aggregation_name': 'documentos',
                'subitems':         [
                    {   'portal_types': [ 'Document', ],
                    },
                ],
            },
            {   'aggregation_name': 'enlaces',
                'subitems':         [
                    {   'portal_types': [ 'Link', ],
                    },
                ],
            },
            {   'aggregation_name': 'imagenes',
                'subitems':         [
                    {   'portal_types': [ 'Image', ],
                    },
                ],
            },
            {   'aggregation_name': 'noticias',
                'subitems':         [
                    {   'portal_types': [ 'News_Item', ],
                    },
                ],
            },
        ],
    },
    {   'portal_types': [ 'TRACatalogo', ],
        'attrs':        [
            {   'name': 'title',
                'type': 'String',
            },
            {   'name': 'description',
                'type': 'Text',
            },
            {   'name': 'text',
                'type': 'Text',
            },
            {   'name': 'nombreProducto',
                'type': 'string',
            },
            {   'name': 'codigoIdiomaPorDefecto',
                'type': 'string',
            },
            {   'name': 'nombreModuloPorDefecto',
                'type': 'string',
            },
            {   'name': 'dominioPorDefecto',
                'type': 'string',
            },
            {   'name': 'maximoRegistrosExplorados',
                'type': 'Number',
            },
            {   'name': 'traduccionesPorPaginaPorDefecto',
                'type': 'Number',
            },
            {   'name': 'modoInteraccionPorDefecto',
                'type': 'selection',
            },
            {   'name': 'segundosParaConfirmarImportacion',
                'type': 'Number',
            },
            {   'name': 'formatoExportacionPorDefecto',
                'type': 'selection',
            },
            {   'name': 'incluirLocalesCSVPorDefecto',
                'type': 'selection',
            },
            {   'name': 'incluirManifestPorDefecto',
                'type': 'selection',
            },
            {   'name': 'modulosPorSeparadoPorDefecto',
                'type': 'selection',
            },
            {   'name': 'tipoArchivoExportacionPorDefecto',
                'type': 'selection',
            },
            {   'name': 'modoGestionErrorCodificacionExportacionPorDefecto',
                'type': 'selection',
            },
            {   'name': 'modulosYSimbolosCadenasOrdenados',
                'type': 'Text',
            },
            {   'name': 'simbolosCadenasOrdenados',
                'type': 'Text',
            },
        ],
        'traversals':   [
            {   'aggregation_name': 'coleccionIdiomas',
                'subitems':         [
                    {   'portal_types': [ 'TRAColeccionIdiomas', ],
                    },
                ],
            },
            {   'aggregation_name': 'coleccionModulos',
                'subitems':         [
                    {   'portal_types': [ 'TRAColeccionModulos', ],
                    },
                ],
            },
            {   'aggregation_name': 'coleccionImportaciones',
                'subitems':         [
                    {   'portal_types': [ 'TRAColeccionImportaciones', ],
                    },
                ],
            },
            {   'aggregation_name': 'archivos',
                'subitems':         [
                    {   'portal_types': [ 'File', ],
                    },
                ],
            },
            {   'aggregation_name': 'coleccionCadenas',
                'subitems':         [
                    {   'portal_types': [ 'TRAColeccionCadenas', ],
                    },
                ],
            },
            {   'aggregation_name': 'coleccionInformes',
                'subitems':         [
                    {   'portal_types': [ 'TRAColeccionInformes', ],
                    },
                ],
            },
            {   'aggregation_name': 'coleccionSolicitudesCadenas',
                'subitems':         [
                    {   'portal_types': [ 'TRAColeccionSolicitudesCadenas', ],
                    },
                ],
            },
            {   'aggregation_name': 'documentos',
                'subitems':         [
                    {   'portal_types': [ 'Document', ],
                    },
                ],
            },
            {   'aggregation_name': 'enlaces',
                'subitems':         [
                    {   'portal_types': [ 'Link', ],
                    },
                ],
            },
            {   'aggregation_name': 'imagenes',
                'subitems':         [
                    {   'portal_types': [ 'Image', ],
                    },
                ],
            },
            {   'aggregation_name': 'noticias',
                'subitems':         [
                    {   'portal_types': [ 'News_Item', ],
                    },
                ],
            },
            {   'relation_name': 'ultimaImportacion',
                'related_types': [
                    {   'portal_types': [ 'TRAImportacion', ],
                    },
                ],
            },
            {   'relation_name': 'ultimoInforme',
                'related_types': [
                    {   'portal_types': [ 'TRAInforme', ],
                    },
                ],
            },
        ],
    },
    {   'portal_types': [ 'TRAColeccionCadenas', ],
        'attrs':        [
            {   'name': 'title',
                'type': 'String',
            },
            {   'name': 'description',
                'type': 'Text',
            },
            {   'name': 'text',
                'type': 'Text',
            },
        ],
        'traversals':   [
            {   'aggregation_name': 'archivos',
                'subitems':         [
                    {   'portal_types': [ 'File', ],
                    },
                ],
            },
            {   'aggregation_name': 'cadenas',
                'subitems':         [
                    {   'portal_types': [ 'TRACadena', ],
                    },
                ],
            },
            {   'aggregation_name': 'documentos',
                'subitems':         [
                    {   'portal_types': [ 'Document', ],
                    },
                ],
            },
            {   'aggregation_name': 'enlaces',
                'subitems':         [
                    {   'portal_types': [ 'Link', ],
                    },
                ],
            },
            {   'aggregation_name': 'imagenes',
                'subitems':         [
                    {   'portal_types': [ 'Image', ],
                    },
                ],
            },
            {   'aggregation_name': 'noticias',
                'subitems':         [
                    {   'portal_types': [ 'News_Item', ],
                    },
                ],
            },
        ],
    },
    {   'portal_types': [ 'TRAColeccionIdiomas', ],
        'attrs':        [
            {   'name': 'title',
                'type': 'String',
            },
            {   'name': 'description',
                'type': 'Text',
            },
            {   'name': 'text',
                'type': 'Text',
            },
        ],
        'traversals':   [
            {   'aggregation_name': 'archivos',
                'subitems':         [
                    {   'portal_types': [ 'File', ],
                    },
                ],
            },
            {   'aggregation_name': 'documentos',
                'subitems':         [
                    {   'portal_types': [ 'Document', ],
                    },
                ],
            },
            {   'aggregation_name': 'enlaces',
                'subitems':         [
                    {   'portal_types': [ 'Link', ],
                    },
                ],
            },
            {   'aggregation_name': 'idiomas',
                'subitems':         [
                    {   'portal_types': [ 'TRAIdioma', ],
                    },
                ],
            },
            {   'aggregation_name': 'imagenes',
                'subitems':         [
                    {   'portal_types': [ 'Image', ],
                    },
                ],
            },
            {   'aggregation_name': 'noticias',
                'subitems':         [
                    {   'portal_types': [ 'News_Item', ],
                    },
                ],
            },
        ],
    },
    {   'portal_types': [ 'TRAColeccionImportaciones', ],
        'attrs':        [
            {   'name': 'title',
                'type': 'String',
            },
            {   'name': 'description',
                'type': 'Text',
            },
            {   'name': 'text',
                'type': 'Text',
            },
        ],
        'traversals':   [
            {   'aggregation_name': 'archivos',
                'subitems':         [
                    {   'portal_types': [ 'File', ],
                    },
                ],
            },
            {   'aggregation_name': 'documentos',
                'subitems':         [
                    {   'portal_types': [ 'Document', ],
                    },
                ],
            },
            {   'aggregation_name': 'enlaces',
                'subitems':         [
                    {   'portal_types': [ 'Link', ],
                    },
                ],
            },
            {   'aggregation_name': 'imagenes',
                'subitems':         [
                    {   'portal_types': [ 'Image', ],
                    },
                ],
            },
            {   'aggregation_name': 'importaciones',
                'subitems':         [
                    {   'portal_types': [ 'TRAImportacion', ],
                    },
                ],
            },
            {   'aggregation_name': 'noticias',
                'subitems':         [
                    {   'portal_types': [ 'News_Item', ],
                    },
                ],
            },
        ],
    },
    {   'portal_types': [ 'TRAColeccionInformes', ],
        'attrs':        [
            {   'name': 'title',
                'type': 'String',
            },
            {   'name': 'description',
                'type': 'Text',
            },
            {   'name': 'text',
                'type': 'Text',
            },
        ],
        'traversals':   [
            {   'aggregation_name': 'archivos',
                'subitems':         [
                    {   'portal_types': [ 'File', ],
                    },
                ],
            },
            {   'aggregation_name': 'documentos',
                'subitems':         [
                    {   'portal_types': [ 'Document', ],
                    },
                ],
            },
            {   'aggregation_name': 'enlaces',
                'subitems':         [
                    {   'portal_types': [ 'Link', ],
                    },
                ],
            },
            {   'aggregation_name': 'imagenes',
                'subitems':         [
                    {   'portal_types': [ 'Image', ],
                    },
                ],
            },
            {   'aggregation_name': 'informes',
                'subitems':         [
                    {   'portal_types': [ 'TRAInforme', ],
                    },
                ],
            },
            {   'aggregation_name': 'noticias',
                'subitems':         [
                    {   'portal_types': [ 'News_Item', ],
                    },
                ],
            },
        ],
    },
    {   'portal_types': [ 'TRAColeccionModulos', ],
        'attrs':        [
            {   'name': 'title',
                'type': 'String',
            },
            {   'name': 'description',
                'type': 'Text',
            },
            {   'name': 'text',
                'type': 'Text',
            },
        ],
        'traversals':   [
            {   'aggregation_name': 'archivos',
                'subitems':         [
                    {   'portal_types': [ 'File', ],
                    },
                ],
            },
            {   'aggregation_name': 'documentos',
                'subitems':         [
                    {   'portal_types': [ 'Document', ],
                    },
                ],
            },
            {   'aggregation_name': 'enlaces',
                'subitems':         [
                    {   'portal_types': [ 'Link', ],
                    },
                ],
            },
            {   'aggregation_name': 'imagenes',
                'subitems':         [
                    {   'portal_types': [ 'Image', ],
                    },
                ],
            },
            {   'aggregation_name': 'modulos',
                'subitems':         [
                    {   'portal_types': [ 'TRAModulo', ],
                    },
                ],
            },
            {   'aggregation_name': 'noticias',
                'subitems':         [
                    {   'portal_types': [ 'News_Item', ],
                    },
                ],
            },
        ],
    },
    {   'portal_types': [ 'TRAColeccionSolicitudesCadenas', ],
        'attrs':        [
            {   'name': 'title',
                'type': 'String',
            },
            {   'name': 'description',
                'type': 'Text',
            },
            {   'name': 'text',
                'type': 'Text',
            },
        ],
        'traversals':   [
            {   'aggregation_name': 'archivos',
                'subitems':         [
                    {   'portal_types': [ 'File', ],
                    },
                ],
            },
            {   'aggregation_name': 'documentos',
                'subitems':         [
                    {   'portal_types': [ 'Document', ],
                    },
                ],
            },
            {   'aggregation_name': 'enlaces',
                'subitems':         [
                    {   'portal_types': [ 'Link', ],
                    },
                ],
            },
            {   'aggregation_name': 'imagenes',
                'subitems':         [
                    {   'portal_types': [ 'Image', ],
                    },
                ],
            },
            {   'aggregation_name': 'noticias',
                'subitems':         [
                    {   'portal_types': [ 'News_Item', ],
                    },
                ],
            },
            {   'aggregation_name': 'solicitudesCadenas',
                'subitems':         [
                    {   'portal_types': [ 'TRASolicitudCadena', ],
                    },
                ],
            },
        ],
    },
    {   'portal_types': [ 'TRAContenidoIntercambio', ],
        'attrs':        [
            {   'name': 'title',
                'type': 'String',
            },
            {   'name': 'description',
                'type': 'Text',
            },
            {   'name': 'text',
                'type': 'Text',
            },
            {   'name': 'excluirDeImportacion',
                'type': 'Boolean',
            },
            {   'name': 'nombreModulo',
                'type': 'string',
            },
            {   'name': 'usuarioContribuidor',
                'type': 'string',
            },
            {   'name': 'fechaContenido',
                'type': 'Date',
            },
            {   'name': 'contenido',
                'type': 'Text',
            },
        ],
        'traversals':   [
            {   'aggregation_name': 'archivos',
                'subitems':         [
                    {   'portal_types': [ 'File', ],
                    },
                ],
            },
            {   'aggregation_name': 'documentos',
                'subitems':         [
                    {   'portal_types': [ 'Document', ],
                    },
                ],
            },
            {   'aggregation_name': 'enlaces',
                'subitems':         [
                    {   'portal_types': [ 'Link', ],
                    },
                ],
            },
            {   'aggregation_name': 'imagenes',
                'subitems':         [
                    {   'portal_types': [ 'Image', ],
                    },
                ],
            },
            {   'aggregation_name': 'noticias',
                'subitems':         [
                    {   'portal_types': [ 'News_Item', ],
                    },
                ],
            },
        ],
    },
    {   'portal_types': [ 'TRAIdioma', ],
        'attrs':        [
            {   'name': 'title',
                'type': 'String',
            },
            {   'name': 'description',
                'type': 'Text',
            },
            {   'name': 'text',
                'type': 'Text',
            },
            {   'name': 'codigoIdiomaEnGvSIG',
                'type': 'string',
            },
            {   'name': 'codigoInternacionalDeIdioma',
                'type': 'string',
            },
            {   'name': 'nombreNativoDeIdioma',
                'type': 'string',
            },
            {   'name': 'codigoIdiomaReferencia',
                'type': 'selection',
            },
            {   'name': 'ambitoDelIdioma',
                'type': 'selection',
            },
            {   'name': 'fallbackDeIdiomas',
                'type': 'string',
            },
            {   'name': 'equipoTraductor',
                'type': 'string',
            },
            {   'name': 'juegoDeCaracteresParaJavaProperties',
                'type': 'selection',
            },
            {   'name': 'juegoDeCaracteresParaPO',
                'type': 'selection',
            },
            {   'name': 'codificacionTransferenciaContenido',
                'type': 'string',
            },
            {   'name': 'formasPlurales',
                'type': 'string',
            },
            {   'name': 'codificacionesPreferidas',
                'type': 'string',
            },
            {   'name': 'esIdiomaPrincipal',
                'type': 'Boolean',
            },
        ],
        'traversals':   [
            {   'relation_name': 'idiomasReferencia',
                'related_types': [
                    {   'portal_types': [ 'TRAIdioma', ],
                    },
                ],
            },
            {   'relation_name': 'referenciaDeIdiomas',
                'related_types': [
                    {   'portal_types': [ 'TRAIdioma', ],
                    },
                ],
            },
            {   'relation_name': 'idiomaBase',
                'related_types': [
                    {   'portal_types': [ 'TRAIdioma', ],
                    },
                ],
            },
            {   'relation_name': 'baseDeIdiomas',
                'related_types': [
                    {   'portal_types': [ 'TRAIdioma', ],
                    },
                ],
            },
            {   'aggregation_name': 'archivos',
                'subitems':         [
                    {   'portal_types': [ 'File', ],
                    },
                ],
            },
            {   'aggregation_name': 'documentos',
                'subitems':         [
                    {   'portal_types': [ 'Document', ],
                    },
                ],
            },
            {   'aggregation_name': 'enlaces',
                'subitems':         [
                    {   'portal_types': [ 'Link', ],
                    },
                ],
            },
            {   'aggregation_name': 'imagenes',
                'subitems':         [
                    {   'portal_types': [ 'Image', ],
                    },
                ],
            },
            {   'aggregation_name': 'noticias',
                'subitems':         [
                    {   'portal_types': [ 'News_Item', ],
                    },
                ],
            },
        ],
    },
    {   'portal_types': [ 'TRAImportacion', ],
        'attrs':        [
            {   'name': 'title',
                'type': 'String',
            },
            {   'name': 'description',
                'type': 'Text',
            },
            {   'name': 'text',
                'type': 'Text',
            },
            {   'name': 'versionDelProducto',
                'type': 'string',
            },
            {   'name': 'buildDelProducto',
                'type': 'string',
            },
            {   'name': 'codigoIdiomaPorDefecto',
                'type': 'string',
            },
            {   'name': 'nombreModuloPorDefecto',
                'type': 'string',
            },
            {   'name': 'maximoLineasAImportarGNUgettextPO',
                'type': 'Number',
            },
            {   'name': 'maximoLineasAImportarJavaProperties',
                'type': 'Number',
            },
            {   'name': 'intervaloRefrescoEnMinutos',
                'type': 'Number',
            },
            {   'name': 'intervaloRefrescoEnNumeroEscrituras',
                'type': 'Number',
            },
            {   'name': 'haComenzado',
                'type': 'Boolean',
            },
            {   'name': 'usuarioImportador',
                'type': 'string',
            },
            {   'name': 'estadoProceso',
                'type': 'selection',
            },
            {   'name': 'informeProgreso',
                'type': 'Text',
            },
            {   'name': 'haCompletadoConExito',
                'type': 'Boolean',
            },
            {   'name': 'fechaComienzoProceso',
                'type': 'Date',
            },
            {   'name': 'fechaFinProceso',
                'type': 'Date',
            },
            {   'name': 'informeFinal',
                'type': 'Text',
            },
            {   'name': 'informeExcepcion',
                'type': 'Text',
            },
            {   'name': 'debeCrearTraduccionesQueFaltan',
                'type': 'Boolean',
            },
            {   'name': 'fechaUltimoInformeProgreso',
                'type': 'Date',
            },
        ],
        'traversals':   [
            {   'aggregation_name': 'archivos',
                'subitems':         [
                    {   'portal_types': [ 'File', ],
                    },
                ],
            },
            {   'aggregation_name': 'contenido',
                'factory_views':                    {   'TRAContenidoIntercambio': 'TRACrear_ContenidoIntercambio',
                },
                'subitems':         [
                    {   'portal_types': [ 'TRAContenidoIntercambio', ],
                    },
                ],
            },
            {   'aggregation_name': 'documentos',
                'subitems':         [
                    {   'portal_types': [ 'Document', ],
                    },
                ],
            },
            {   'aggregation_name': 'enlaces',
                'subitems':         [
                    {   'portal_types': [ 'Link', ],
                    },
                ],
            },
            {   'aggregation_name': 'imagenes',
                'subitems':         [
                    {   'portal_types': [ 'Image', ],
                    },
                ],
            },
            {   'aggregation_name': 'informesEstado',
                'subitems':         [
                    {   'portal_types': [ 'TRAInforme', ],
                    },
                ],
            },
            {   'aggregation_name': 'noticias',
                'subitems':         [
                    {   'portal_types': [ 'News_Item', ],
                    },
                ],
            },
        ],
    },
    {   'portal_types': [ 'TRAInforme', ],
        'attrs':        [
            {   'name': 'title',
                'type': 'String',
            },
            {   'name': 'description',
                'type': 'Text',
            },
            {   'name': 'text',
                'type': 'Text',
            },
            {   'name': 'esAutoActualizable',
                'type': 'Boolean',
            },
            {   'name': 'estadoProceso',
                'type': 'selection',
            },
            {   'name': 'haComenzado',
                'type': 'Boolean',
            },
            {   'name': 'usuarioInformador',
                'type': 'string',
            },
            {   'name': 'haCompletadoConExito',
                'type': 'Boolean',
            },
            {   'name': 'fechaComienzoProceso',
                'type': 'Date',
            },
            {   'name': 'fechaFinProceso',
                'type': 'Date',
            },
            {   'name': 'informeExcepcion',
                'type': 'Text',
            },
            {   'name': 'informeIdiomas',
                'type': 'Text',
            },
            {   'name': 'informeExcepcionIdiomas',
                'type': 'Text',
            },
            {   'name': 'informeModulos',
                'type': 'Text',
            },
            {   'name': 'informeExcepcionModulos',
                'type': 'Text',
            },
            {   'name': 'minimoIntervaloActualizacionEnMinutos',
                'type': 'Number',
            },
        ],
        'traversals':   [
            {   'aggregation_name': 'archivos',
                'subitems':         [
                    {   'portal_types': [ 'File', ],
                    },
                ],
            },
            {   'aggregation_name': 'documentos',
                'subitems':         [
                    {   'portal_types': [ 'Document', ],
                    },
                ],
            },
            {   'aggregation_name': 'enlaces',
                'subitems':         [
                    {   'portal_types': [ 'Link', ],
                    },
                ],
            },
            {   'aggregation_name': 'imagenes',
                'subitems':         [
                    {   'portal_types': [ 'Image', ],
                    },
                ],
            },
            {   'aggregation_name': 'noticias',
                'subitems':         [
                    {   'portal_types': [ 'News_Item', ],
                    },
                ],
            },
        ],
    },
    {   'portal_types': [ 'TRAModulo', ],
        'attrs':        [
            {   'name': 'title',
                'type': 'String',
            },
            {   'name': 'description',
                'type': 'Text',
            },
            {   'name': 'text',
                'type': 'Text',
            },
            {   'name': 'dominio',
                'type': 'string',
            },
            {   'name': 'esModuloPrincipal',
                'type': 'Boolean',
            },
        ],
        'traversals':   [
            {   'aggregation_name': 'archivos',
                'subitems':         [
                    {   'portal_types': [ 'File', ],
                    },
                ],
            },
            {   'aggregation_name': 'documentos',
                'subitems':         [
                    {   'portal_types': [ 'Document', ],
                    },
                ],
            },
            {   'aggregation_name': 'enlaces',
                'subitems':         [
                    {   'portal_types': [ 'Link', ],
                    },
                ],
            },
            {   'aggregation_name': 'imagenes',
                'subitems':         [
                    {   'portal_types': [ 'Image', ],
                    },
                ],
            },
            {   'aggregation_name': 'noticias',
                'subitems':         [
                    {   'portal_types': [ 'News_Item', ],
                    },
                ],
            },
        ],
    },
    {   'portal_types': [ 'TRASolicitudCadena', ],
        'attrs':        [
            {   'name': 'title',
                'type': 'String',
            },
            {   'name': 'description',
                'type': 'Text',
            },
            {   'name': 'text',
                'type': 'Text',
            },
            {   'name': 'simbolo',
                'type': 'string',
            },
            {   'name': 'estadoSolicitudCadena',
                'type': 'selection',
            },
            {   'name': 'fechaCreacionTextual',
                'type': 'string',
            },
            {   'name': 'usuarioCreador',
                'type': 'string',
            },
            {   'name': 'fechaCancelacionTextual',
                'type': 'string',
            },
            {   'name': 'nombresModulos',
                'type': 'string',
            },
            {   'name': 'referenciasFuentes',
                'type': 'string',
            },
            {   'name': 'codigoIdiomaPrincipal',
                'type': 'string',
            },
            {   'name': 'cadenaTraducidaAIdiomaPrincipal',
                'type': 'string',
            },
            {   'name': 'codigoIdiomaReferencia',
                'type': 'string',
            },
            {   'name': 'cadenaTraducidaAIdiomaReferencia',
                'type': 'string',
            },
            {   'name': 'pathDelRaiz',
                'type': 'string',
            },
        ],
        'traversals':   [
            {   'aggregation_name': 'archivos',
                'subitems':         [
                    {   'portal_types': [ 'File', ],
                    },
                ],
            },
            {   'aggregation_name': 'documentos',
                'subitems':         [
                    {   'portal_types': [ 'Document', ],
                    },
                ],
            },
            {   'aggregation_name': 'enlaces',
                'subitems':         [
                    {   'portal_types': [ 'Link', ],
                    },
                ],
            },
            {   'aggregation_name': 'imagenes',
                'subitems':         [
                    {   'portal_types': [ 'Image', ],
                    },
                ],
            },
            {   'aggregation_name': 'noticias',
                'subitems':         [
                    {   'portal_types': [ 'News_Item', ],
                    },
                ],
            },
        ],
    },
    {   'portal_types': [ 'TRATraduccion', ],
        'attrs':        [
            {   'name': 'title',
                'type': 'String',
            },
            {   'name': 'description',
                'type': 'Text',
            },
            {   'name': 'text',
                'type': 'Text',
            },
            {   'name': 'simbolo',
                'type': 'string',
            },
            {   'name': 'codigoIdiomaEnGvSIG',
                'type': 'string',
            },
            {   'name': 'cadenaTraducida',
                'type': 'string',
            },
            {   'name': 'estadoTraduccion',
                'type': 'selection',
            },
            {   'name': 'fechaTraduccionTextual',
                'type': 'string',
            },
            {   'name': 'usuarioTraductor',
                'type': 'string',
            },
            {   'name': 'fechaRevisionTextual',
                'type': 'string',
            },
            {   'name': 'usuarioRevisor',
                'type': 'string',
            },
            {   'name': 'fechaDefinitivoTextual',
                'type': 'string',
            },
            {   'name': 'usuarioCoordinador',
                'type': 'string',
            },
            {   'name': 'idCadena',
                'type': 'string',
            },
            {   'name': 'estadoCadena',
                'type': 'selection',
            },
            {   'name': 'nombresModulos',
                'type': 'string',
            },
            {   'name': 'comentario',
                'type': 'Text',
            },
            {   'name': 'indicadoresPO',
                'type': 'string',
            },
            {   'name': 'historia',
                'type': 'Text',
            },
            {   'name': 'fechaCreacionTextual',
                'type': 'string',
            },
            {   'name': 'pathDelRaiz',
                'type': 'string',
            },
            {   'name': 'usuarioCreador',
                'type': 'string',
            },
        ],
        'traversals':   [
            {   'aggregation_name': 'archivos',
                'subitems':         [
                    {   'portal_types': [ 'File', ],
                    },
                ],
            },
            {   'aggregation_name': 'documentos',
                'subitems':         [
                    {   'portal_types': [ 'Document', ],
                    },
                ],
            },
            {   'aggregation_name': 'enlaces',
                'subitems':         [
                    {   'portal_types': [ 'Link', ],
                    },
                ],
            },
            {   'aggregation_name': 'imagenes',
                'subitems':         [
                    {   'portal_types': [ 'Image', ],
                    },
                ],
            },
            {   'aggregation_name': 'noticias',
                'subitems':         [
                    {   'portal_types': [ 'News_Item', ],
                    },
                ],
            },
        ],
    },
]
