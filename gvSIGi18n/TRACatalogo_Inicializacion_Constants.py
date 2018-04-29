# -*- coding: utf-8 -*-
#
# File: TRACatalogo_Inicializacion_Constants.py
#
# Copyright (c) 2009 by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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

##code-section module-header #fill in your manual code here


from Products.CMFCore               import permissions

from Products.CMFCore.utils         import SimpleRecord



from TRAElemento_Constants import *


from TRARoles       import *


from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Inicializacion_Constants import cExternalMetodDefinitions as cExternalMetodDefinitions_ModelDDvlPlone


##/code-section module-header

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema


##code-section after-schema #fill in your manual code here





cLazyCreateExternalMethod       = True
# ACV 20091004 Moved to TRAElemento_Constants.py as it is used also from TRAElemento_Operaciones.py
# cLazyCreateModelDDvlPloneTool   = True
cLazyCreateCollections          = True
cLazyCreateCatalogs             = True
cLazyCreateIndexes              = True
cLazyCreateLexicons             = True    
cLazyCreateSchemaFields         = True
cLazyCreateUserGroups           = True
cLazyCreateSetLocalRoles        = True
cLazyCreateSetAcquireRoleAssignments = True
cLazyAddGroupToGroup            = True
cLazyAddSchemaFields    = True




# #############################################################
# Especificacion de las colecciones de elementos del catalogo
#


cColeccionCadenas_Id    = "cadenas"
cColeccionCadenas_Title = "Strings"
cColeccionIdiomas_Id    = "idiomas"
cColeccionIdiomas_Title = "Languages"
cColeccionModulos_Id    = "modulos"
cColeccionModulos_Title = "Modules"
cColeccionInformes_Id   = "informes"
cColeccionInformes_Title= "Reports"
cColeccionImportaciones_Id    = "importaciones"
cColeccionImportaciones_Title = "Imports"
cColeccionSolicitudesCadenas_Id    = "solicitudescadenas"
cColeccionSolicitudesCadenas_Title = "String Requests"


cEspecificacionesColecciones = [ 
    [ cNombreTipoTRAColeccionIdiomas,        cColeccionIdiomas_Id,       cColeccionIdiomas_Title, ],
    [ cNombreTipoTRAColeccionModulos,        cColeccionModulos_Id,       cColeccionModulos_Title, ],
    [ cNombreTipoTRAColeccionCadenas,        cColeccionCadenas_Id,       cColeccionCadenas_Title, ],
    [ cNombreTipoTRAColeccionImportaciones,  cColeccionImportaciones_Id, cColeccionImportaciones_Title, ],
    [ cNombreTipoTRAColeccionInformes,       cColeccionInformes_Id,      cColeccionInformes_Title, ],
    [ cNombreTipoTRAColeccionSolicitudesCadenas,       cColeccionSolicitudesCadenas_Id,      cColeccionSolicitudesCadenas_Title, ],
]



# #############################################################
# Especificacion de los catalogos dedicados exclusivamente a cadenas y traducciones
#


cNombreCatalogoBusquedaCadenas      = 'TRACadenaBusqueda'
cNombreCatalogoFiltroCadenas        = 'TRACadenaFiltro'
cNombreCatalogoTextoCadenas         = 'TRACadenaTexto'
cNombreCatalogoBusquedaTraducciones = 'TRATraduccionBusqueda'
cNombreCatalogoFiltroTraducciones   = 'TRATraduccionFiltro'
cNombreCatalogoTextoTraducciones    = 'TRATraduccionTexto'




cLanguagesWithChineseJapaneseKoreanLexicon  = [ 'zh', 'ja', 'ko', ]

cLexiconPipelineChineseJapaneseKorean  = [ 'CJKSplitter', ]


    




cIndexesCatalogoBusquedaCadenas  = [ 
    [ 'getId',              'FieldIndex',  ],
    [ 'getSimbolo',         'FieldIndex',  ],
    [ 'getEstadoCadena',    'KeywordIndex',],
]
# ACV 20090814 
#   EATR01 Remove Attribute pathDelRaiz from all entities; 	
#   EATR02 Remove the Type attribute from catalog schemas
#cSchemaFieldsCatalogoBusquedaCadenas  = [ 'Type', 'getPathDelRaiz', ] + [ aIdxSpec[ 0] for aIdxSpec in cIndexesCatalogoBusquedaCadenas]

cSchemaFieldsCatalogoBusquedaCadenas  = [ aIdxSpec[ 0] for aIdxSpec in cIndexesCatalogoBusquedaCadenas]








cIndexesCatalogoFiltroCadenas  = cIndexesCatalogoBusquedaCadenas + [ 
    [ 'getFechaCreacionTextual',    'FieldIndex',   ],
    [ 'getUsuarioCreador',          'FieldIndex',  ],
    [ 'getFechaCancelacionTextual', 'FieldIndex',   ],
]
# ACV 20090814 
#   EATR01 Remove Attribute pathDelRaiz from all entities; 	
#   EATR02 Remove the Type attribute from catalog schemas
#cSchemaFieldsCatalogoFiltroCadenas  = [ 'Type', 'getPathDelRaiz', ] + \
#                                      [ aIdxSpec[ 0] for aIdxSpec in cIndexesCatalogoFiltroCadenas] + \
#                                      [ 'getNombresModulos',]

cSchemaFieldsCatalogoFiltroCadenas  = [ aIdxSpec[ 0] for aIdxSpec in cIndexesCatalogoFiltroCadenas] + \
                                      [ 'getNombresModulos',]





cIndexesCatalogoTextoCadenas  = [ 
    [ 'getSimboloEnPalabras',    'ZCTextIndex',   SimpleRecord( lexicon_id='plaintext_lexicon' , index_type='Okapi BM25 Rank')],
]
cSchemaFieldsCatalogoTextoCadenas  = [ 'getId', 'getSimbolo',]

cLexiconsCatalogoTextoCadenas  = [ 
    [ 'plaintext_lexicon', [ 'Splitter', 'CaseNormalizer', 'StopWordRemover', ], ],
]







cCatalogsDetailsParaCadenas = [
    {   'name':             cNombreCatalogoBusquedaCadenas,
        'indexes':          cIndexesCatalogoBusquedaCadenas,
        'schema_fields':    cSchemaFieldsCatalogoBusquedaCadenas,
        'lexicons':         [],
    },
    {   'name':             cNombreCatalogoFiltroCadenas,
        'indexes':          cIndexesCatalogoFiltroCadenas,
        'schema_fields':    cSchemaFieldsCatalogoFiltroCadenas,
        'lexicons':         [],
    },
    {   'name':             cNombreCatalogoTextoCadenas,
        'indexes':          cIndexesCatalogoTextoCadenas,
        'schema_fields':    cSchemaFieldsCatalogoTextoCadenas,
        'lexicons':         cLexiconsCatalogoTextoCadenas,
    },
]











cIndexesCatalogoBusquedaTraducciones  = [ 
    [ 'getId',                  'FieldIndex',  ],
    [ 'getSimbolo',             'FieldIndex',  ],
    [ 'getEstadoCadena',        'KeywordIndex',],
    [ 'getIdCadena',            'FieldIndex',  ],
    [ 'getEstadoTraduccion',    'KeywordIndex',],
]
# ACV 20090814 
#   EATR01 Remove Attribute pathDelRaiz from all entities; 	
#   EATR02 Remove the Type attribute from catalog schemas
#cSchemaFieldsCatalogoBusquedaTraducciones  = [ 'Type', 'getPathDelRaiz', 'getCodigoIdiomaEnGvSIG', ] + \
#                                             [ aIdxSpec[ 0] for aIdxSpec in cIndexesCatalogoBusquedaTraducciones]
cSchemaFieldsCatalogoBusquedaTraducciones  = [ 'getCodigoIdiomaEnGvSIG', ] + \
                                             [ aIdxSpec[ 0] for aIdxSpec in cIndexesCatalogoBusquedaTraducciones]






cIndexesCatalogoFiltroTraducciones  = cIndexesCatalogoBusquedaTraducciones + [ 
    [ 'getFechaCreacionTextual',        'FieldIndex',     ],
    [ 'getUsuarioCreador',              'FieldIndex',     ],
    [ 'getFechaTraduccionTextual',      'FieldIndex',     ],
    [ 'getUsuarioTraductor',            'FieldIndex',     ],
    [ 'getFechaRevisionTextual',        'FieldIndex',     ],
    [ 'getUsuarioRevisor',              'FieldIndex',     ],
    [ 'getFechaDefinitivoTextual',      'FieldIndex',     ],
    [ 'getUsuarioCoordinador',          'FieldIndex',     ],
]
cSchemaFieldsCatalogoFiltroTraducciones  = [ 'Type', 'getPathDelRaiz', 'getCodigoIdiomaEnGvSIG', ] + \
                                           [ aIdxSpec[ 0] for aIdxSpec in cIndexesCatalogoFiltroTraducciones] + \
                                           [ 'getCadenaTraducida', 'getComentario', 'getNombresModulos', 'getContadorCambios',]
       




cIndexesCatalogoTextoTraducciones  = [ 
    [ 'getCadenaTraducida',  'ZCTextIndex',   SimpleRecord( lexicon_id='plaintext_lexicon' , index_type='Okapi BM25 Rank')],
]
cSchemaFieldsCatalogoTextoTraducciones  = [ 'getId', 'getIdCadena', 'getSimbolo', 'getCodigoIdiomaEnGvSIG',]


cLexiconsCatalogoTextoTraducciones  = [ 
    [ 'plaintext_lexicon', [ 'Splitter', 'CaseNormalizer', 'StopWordRemover', ], ],
]








cCatalogsDetailsParaIdioma = [
    {   'name':             cNombreCatalogoBusquedaTraducciones,
        'indexes':          cIndexesCatalogoBusquedaTraducciones,
        'schema_fields':    cSchemaFieldsCatalogoBusquedaTraducciones,
        'lexicons':         '',
    },
    {   'name':             cNombreCatalogoFiltroTraducciones,
        'indexes':          cIndexesCatalogoFiltroTraducciones,
        'schema_fields':    cSchemaFieldsCatalogoFiltroTraducciones,
        'lexicons':         '',
   },   
    {   'name':             cNombreCatalogoTextoTraducciones,
        'indexes':          cIndexesCatalogoTextoTraducciones,
        'schema_fields':    cSchemaFieldsCatalogoTextoTraducciones,
        'lexicons':         cLexiconsCatalogoTextoTraducciones,
    },   
]







# #############################################################
# External methods to create
#

cExtMethod_ChangeAndBrowseTranslations           = "TRAChangeAndBrowseTranslations"
cExtMethod_SizesIdioma                           = "TRASizesIdioma"
cExtMethod_RenderPermissionDefinitions           = "TRARenderPermissionDefinitions"
cExtMethod_RenderLoggedUsedAndRolesHere          = "TRARenderLoggedUsedHere"
cExtMethod_RenderGroupsRolesHere                 = "TRARenderGroupsRolesHere"
cExtMethod_RenderExecutionDetails                = "TRARenderExecutionDetails"



cExternalMetodDefinitions = [
    [ cExtMethod_ChangeAndBrowseTranslations,                 # module  
        [ cExtMethod_ChangeAndBrowseTranslations,    ]   * 3, # function id title name
        [ cExtMethod_SizesIdioma,                    ]   * 3, # function id title name
    ],
    [ 'TRARenderSecurity',                                   # module  
       [ cExtMethod_RenderPermissionDefinitions,     ]   * 3, # function id title name
       [ cExtMethod_RenderLoggedUsedAndRolesHere,    ]   * 3, # function id title name
       [ cExtMethod_RenderGroupsRolesHere,           ]   * 3, # function id title name
    ],    
    [ 'TRARenderProfiling',                                  # module  
        [ cExtMethod_RenderExecutionDetails,            ]   * 3, # function id title name

    ],
    [ 'TRAExport_ctrl',                                  # module  
        [ 'TRAExport_ParametersCandidateValues',    ]   * 3, # function id title name
    ],
] + cExternalMetodDefinitions_ModelDDvlPlone


##/code-section module-footer



