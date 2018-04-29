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



##/code-section module-header

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema


##code-section after-schema #fill in your manual code here



cTRAInstallPath_PortalSkinsCustom = [ 'portal_skins', 'custom',]



# #############################################################
"""Control what to verify and initialize.

"""
cInitializeAllow_CreateExternalMethod       = True
# ACV 20091004 Moved to TRAElemento_Constants.py as it is used also from TRAElemento_Operaciones.py
# cInitializeAllow_CreateModelDDvlPloneTool   = True
cInitializeAllow_CreateCollections          = True
cInitializeAllow_CreateSingletons           = True
cInitializeAllow_CreateCatalogs             = True
cInitializeAllow_CreateIndexes              = True
cInitializeAllow_CreateLexicons             = True    
cInitializeAllow_CreateSchemaFields         = True
cInitializeAllow_CreateUserGroups           = True
cInitializeAllow_CreateSetLocalRoles        = True
cInitializeAllow_CreateSetAcquireRoleAssignments = True
cInitializeAllow_AddGroupToGroup            = True
cInitializeAllow_AddSchemaFields            = True






# #############################################################
"""Specification of the collection elements to create under the root catalog.

"""
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
cColeccionProgresos_Id   = "progresos"
cColeccionProgresos_Title= "Progresses"

cTRAEspecificacionesColecciones = [ 
    [ cNombreTipoTRAColeccionIdiomas,              cColeccionIdiomas_Id,       cColeccionIdiomas_Title, ],
    [ cNombreTipoTRAColeccionModulos,              cColeccionModulos_Id,       cColeccionModulos_Title, ],
    [ cNombreTipoTRAColeccionCadenas,              cColeccionCadenas_Id,       cColeccionCadenas_Title, ],
    [ cNombreTipoTRAColeccionImportaciones,        cColeccionImportaciones_Id, cColeccionImportaciones_Title, ],
    [ cNombreTipoTRAColeccionInformes,             cColeccionInformes_Id,      cColeccionInformes_Title, ],
    [ cNombreTipoTRAColeccionSolicitudesCadenas,   cColeccionSolicitudesCadenas_Id,      cColeccionSolicitudesCadenas_Title, ],
    [ cNombreTipoTRAColeccionProgresos,            cColeccionProgresos_Id,      cColeccionProgresos_Title, ],
]






# #############################################################
"""Specification of the singleton elements to create under the root catalog.

"""


cTRAEspecificacionesSingletons = [ 
    [ cNombreTipoTRAParametrosControlProgreso, cTRAParametrosControlProgreso_Inventario_Id,           cTRAParametrosControlProgreso_Inventario_Title, 
        {   'guardarResultados_habilitado':                   True,
            'guardarResultados_maximoMilisegundos':           60000,
            'guardarResultados_maximoElementosLeidos':        5000,
            'guardarResultados_maximoElementosModificados':   0,
            'transacciones_habilitado':                       True,
            'transacciones_maximoMilisegundos':               3000,
            'transacciones_maximoElementosLeidos':            5000,
            'transacciones_maximoElementosModificados':       0,
            'registro_habilitado':                            True,
            'registro_maximoMilisegundos':                    120000,
            'registro_maximoElementosLeidos':                 10000,
            'registro_maximoElementosModificados':            0,
            'registro_maximoTransacciones':                   10,
            'cederProcesador_habilitado':                     True,
            'cederProcesador_maximoMilisegundos':             1000,
            'cederProcesador_maximoElementosLeidos':          1000,
            'cederProcesador_maximoElementosModificados':     0,
            'cederProcesador_porcentajeTiempoActividad':      50,
        },
    ],
    [ cNombreTipoTRAParametrosControlProgreso, cTRAParametrosControlProgreso_Recatalogar_Id,          cTRAParametrosControlProgreso_Recatalogar_Title, 
        {   'guardarResultados_habilitado':                   True,
            'guardarResultados_maximoMilisegundos':           60000,
            'guardarResultados_maximoElementosLeidos':        5000,
            'guardarResultados_maximoElementosModificados':   5000,
            'transacciones_habilitado':                       True,
            'transacciones_maximoMilisegundos':               3000,
            'transacciones_maximoElementosLeidos':            5000,
            'transacciones_maximoElementosModificados':       5000,
            'registro_habilitado':                            True,
            'registro_maximoMilisegundos':                    120000,
            'registro_maximoElementosLeidos':                 10000,
            'registro_maximoElementosModificados':            10000,
            'registro_maximoTransacciones':                   10,
            'cederProcesador_habilitado':                     True,
            'cederProcesador_maximoMilisegundos':             1000,
            'cederProcesador_maximoElementosLeidos':          1000,
            'cederProcesador_maximoElementosModificados':     1000,
            'cederProcesador_porcentajeTiempoActividad':      50,
        },
    ],
    [ cNombreTipoTRAParametrosControlProgreso, cTRAParametrosControlProgreso_ReestablecerPermisos_Id, cTRAParametrosControlProgreso_ReestablecerPermisos_Title, 
        {   'guardarResultados_habilitado':                   True,
            'guardarResultados_maximoMilisegundos':           60000,
            'guardarResultados_maximoElementosLeidos':        5000,
            'guardarResultados_maximoElementosModificados':   5000,
            'transacciones_habilitado':                       True,
            'transacciones_maximoMilisegundos':               3000,
            'transacciones_maximoElementosLeidos':            5000,
            'transacciones_maximoElementosModificados':       5000,
            'registro_habilitado':                            True,
            'registro_maximoMilisegundos':                    120000,
            'registro_maximoElementosLeidos':                 10000,
            'registro_maximoElementosModificados':            10000,
            'registro_maximoTransacciones':                   10,
            'cederProcesador_habilitado':                     True,
            'cederProcesador_maximoMilisegundos':             1000,
            'cederProcesador_maximoElementosLeidos':          1000,
            'cederProcesador_maximoElementosModificados':     1000,
            'cederProcesador_porcentajeTiempoActividad':      50,
        },
    ],
    [ cNombreTipoTRAParametrosControlProgreso, cTRAParametrosControlProgreso_DeleteModule_Id,         cTRAParametrosControlProgreso_DeleteModule_Title, 
        {   'guardarResultados_habilitado':                   True,
            'guardarResultados_maximoMilisegundos':           60000,
            'guardarResultados_maximoElementosLeidos':        5000,
            'guardarResultados_maximoElementosModificados':   5000,
            'transacciones_habilitado':                       True,
            'transacciones_maximoMilisegundos':               3000,
            'transacciones_maximoElementosLeidos':            5000,
            'transacciones_maximoElementosModificados':       5000,
            'registro_habilitado':                            True,
            'registro_maximoMilisegundos':                    120000,
            'registro_maximoElementosLeidos':                 10000,
            'registro_maximoElementosModificados':            10000,
            'registro_maximoTransacciones':                   10,
            'cederProcesador_habilitado':                     True,
            'cederProcesador_maximoMilisegundos':             1000,
            'cederProcesador_maximoElementosLeidos':          1000,
            'cederProcesador_maximoElementosModificados':     1000,
            'cederProcesador_porcentajeTiempoActividad':      50,
        },
    ],
    [ cNombreTipoTRAParametrosControlProgreso, cTRAParametrosControlProgreso_DeleteLanguage_Id,       cTRAParametrosControlProgreso_DeleteLanguage_Title, 
        {   'guardarResultados_habilitado':                   True,
            'guardarResultados_maximoMilisegundos':           60000,
            'guardarResultados_maximoElementosLeidos':        5000,
            'guardarResultados_maximoElementosModificados':   5000,
            'transacciones_habilitado':                       True,
            'transacciones_maximoMilisegundos':               3000,
            'transacciones_maximoElementosLeidos':            5000,
            'transacciones_maximoElementosModificados':       5000,
            'registro_habilitado':                            True,
            'registro_maximoMilisegundos':                    120000,
            'registro_maximoElementosLeidos':                 10000,
            'registro_maximoElementosModificados':            10000,
            'registro_maximoTransacciones':                   10,
            'cederProcesador_habilitado':                     True,
            'cederProcesador_maximoMilisegundos':             1000,
            'cederProcesador_maximoElementosLeidos':          1000,
            'cederProcesador_maximoElementosModificados':     1000,
            'cederProcesador_porcentajeTiempoActividad':      50,
        },
    ],
    [ cNombreTipoTRAParametrosControlProgreso, cTRAParametrosControlProgreso_Backup_Id,               cTRAParametrosControlProgreso_Backup_Title, 
        {   'guardarResultados_habilitado':                   True,
            'guardarResultados_maximoMilisegundos':           60000,
            'guardarResultados_maximoElementosLeidos':        5000,
            'guardarResultados_maximoElementosModificados':   0,
            'transacciones_habilitado':                       True,
            'transacciones_maximoMilisegundos':               3000,
            'transacciones_maximoElementosLeidos':            5000,
            'transacciones_maximoElementosModificados':       0,
            'registro_habilitado':                            True,
            'registro_maximoMilisegundos':                    120000,
            'registro_maximoElementosLeidos':                 10000,
            'registro_maximoElementosModificados':            0,
            'registro_maximoTransacciones':                   10,
            'cederProcesador_habilitado':                     True,
            'cederProcesador_maximoMilisegundos':             1000,
            'cederProcesador_maximoElementosLeidos':          1000,
            'cederProcesador_maximoElementosModificados':     0,
            'cederProcesador_porcentajeTiempoActividad':      50,
        },
    ],
    [ cNombreTipoTRAParametrosControlProgreso, cTRAParametrosControlProgreso_ExportGvSIG_Id,          cTRAParametrosControlProgreso_ExportGvSIG_Title, 
        {   'guardarResultados_habilitado':                   True,
            'guardarResultados_maximoMilisegundos':           60000,
            'guardarResultados_maximoElementosLeidos':        5000,
            'guardarResultados_maximoElementosModificados':   0,
            'transacciones_habilitado':                       True,
            'transacciones_maximoMilisegundos':               3000,
            'transacciones_maximoElementosLeidos':            5000,
            'transacciones_maximoElementosModificados':       0,
            'registro_habilitado':                            True,
            'registro_maximoMilisegundos':                    120000,
            'registro_maximoElementosLeidos':                 10000,
            'registro_maximoElementosModificados':            0,
            'registro_maximoTransacciones':                   10,
            'cederProcesador_habilitado':                     True,
            'cederProcesador_maximoMilisegundos':             1000,
            'cederProcesador_maximoElementosLeidos':          1000,
            'cederProcesador_maximoElementosModificados':     0,
            'cederProcesador_porcentajeTiempoActividad':      50,
        },
    ],
    [ cNombreTipoTRAParametrosControlProgreso, cTRAParametrosControlProgreso_Export_Id,               cTRAParametrosControlProgreso_Export_Title, 
        {   'guardarResultados_habilitado':                   True,
            'guardarResultados_maximoMilisegundos':           60000,
            'guardarResultados_maximoElementosLeidos':        5000,
            'guardarResultados_maximoElementosModificados':   0,
            'transacciones_habilitado':                       True,
            'transacciones_maximoMilisegundos':               3000,
            'transacciones_maximoElementosLeidos':            5000,
            'transacciones_maximoElementosModificados':       0,
            'registro_habilitado':                            True,
            'registro_maximoMilisegundos':                    120000,
            'registro_maximoElementosLeidos':                 10000,
            'registro_maximoElementosModificados':            0,
            'registro_maximoTransacciones':                   10,
            'cederProcesador_habilitado':                     True,
            'cederProcesador_maximoMilisegundos':             1000,
            'cederProcesador_maximoElementosLeidos':          1000,
            'cederProcesador_maximoElementosModificados':     0,
            'cederProcesador_porcentajeTiempoActividad':      50,
        },
    ],
    [ cNombreTipoTRAParametrosControlProgreso, cTRAParametrosControlProgreso_Import_Id,               cTRAParametrosControlProgreso_Import_Title, 
        {   'guardarResultados_habilitado':                   True,
            'guardarResultados_maximoMilisegundos':           60000,
            'guardarResultados_maximoElementosLeidos':        1000,
            'guardarResultados_maximoElementosModificados':   1000,
            'transacciones_habilitado':                       True,
            'transacciones_maximoMilisegundos':               2000,
            'transacciones_maximoElementosLeidos':            1000,
            'transacciones_maximoElementosModificados':       1000,
            'registro_habilitado':                            True,
            'registro_maximoMilisegundos':                    60000,
            'registro_maximoElementosLeidos':                 1000,
            'registro_maximoElementosModificados':            1000,
            'registro_maximoTransacciones':                   10,
            'cederProcesador_habilitado':                     True,
            'cederProcesador_maximoMilisegundos':             1000,
            'cederProcesador_maximoElementosLeidos':          1000,
            'cederProcesador_maximoElementosModificados':     1000,
            'cederProcesador_porcentajeTiempoActividad':      50,
        },
    ],
]   









# #############################################################
"""Specification of ZCatalog instances specific to strings and translations.

"""
cNombreCatalogoBusquedaCadenas      = 'TRACadenaBusqueda'
cNombreCatalogoFiltroCadenas        = 'TRACadenaFiltro'
cNombreCatalogoTextoCadenas         = 'TRACadenaTexto'
cNombreCatalogoBusquedaTraducciones = 'TRATraduccionBusqueda'
cNombreCatalogoFiltroTraducciones   = 'TRATraduccionFiltro'
cNombreCatalogoTextoTraducciones    = 'TRATraduccionTexto'




cLanguagesWithSpecialLexiconPipelines = {
    'zh':  [ 'CJKSplitter', ],
    'ja':  [ 'CJKSplitter', ],
    'ko':  [ 'CJKSplitter', ],
    'en':  [ 'Splitter', 'CaseNormalizer', 'StopWordRemover', ],
}








cIndexesCatalogoBusquedaCadenas  = [ 
    [ 'getId',              'FieldIndex',  ],
    [ 'getSimbolo',         'FieldIndex',  ],
    [ 'getEstadoCadena',    'KeywordIndex',],
]


cSchemaFieldsCatalogoBusquedaCadenas  = [ aIdxSpec[ 0] for aIdxSpec in cIndexesCatalogoBusquedaCadenas]








cIndexesCatalogoFiltroCadenas  = cIndexesCatalogoBusquedaCadenas + [ 
    [ 'getFechaCreacionTextual',    'FieldIndex',   ],
    [ 'getUsuarioCreador',          'FieldIndex',  ],
    [ 'getFechaCancelacionTextual', 'FieldIndex',   ],
]


cSchemaFieldsCatalogoFiltroCadenas  = [ aIdxSpec[ 0] for aIdxSpec in cIndexesCatalogoFiltroCadenas] + \
                                    [ 'getNombresModulos',]





cIndexesCatalogoTextoCadenas  = [ 
    [ 'getSimboloEnPalabras',    'ZCTextIndex',   SimpleRecord( lexicon_id='plaintext_lexicon' , index_type='Okapi BM25 Rank')],
]
cSchemaFieldsCatalogoTextoCadenas  = [ 'getId', 'getSimbolo',]

cLexiconsCatalogoTextoCadenas  = [ 
    [ 'plaintext_lexicon', [ 'Splitter', 'CaseNormalizer', 'StopWordRemover', ], ],
]







cTRACatalogsDetailsParaCadenas = [
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
cSchemaFieldsCatalogoFiltroTraducciones  = [ 'Type', 'getCodigoIdiomaEnGvSIG', ] + \
                                         [ aIdxSpec[ 0] for aIdxSpec in cIndexesCatalogoFiltroTraducciones] + \
                                         [ 'getCadenaTraducida', 'getComentario', 'getNombresModulos', 'getContadorCambios',]





cIndexesCatalogoTextoTraducciones  = [ 
    [ 'getCadenaTraducida',  'ZCTextIndex',   SimpleRecord( lexicon_id='plaintext_lexicon' , index_type='Okapi BM25 Rank')],
]
cSchemaFieldsCatalogoTextoTraducciones  = [ 'getId', 'getIdCadena', 'getSimbolo', 'getCodigoIdiomaEnGvSIG',]


cLexiconsCatalogoTextoTraducciones  = [ 
    [ 'plaintext_lexicon', [ 'TRASplitter', ], ],
]








cTRACatalogsDetailsParaIdioma = [
    {   'name':             cNombreCatalogoBusquedaTraducciones,
        'indexes':          cIndexesCatalogoBusquedaTraducciones,
        'schema_fields':    cSchemaFieldsCatalogoBusquedaTraducciones,
        'lexicons':         [],
        },
    {   'name':             cNombreCatalogoFiltroTraducciones,
        'indexes':          cIndexesCatalogoFiltroTraducciones,
        'schema_fields':    cSchemaFieldsCatalogoFiltroTraducciones,
        'lexicons':         [],
        },   
    {   'name':             cNombreCatalogoTextoTraducciones,
        'indexes':          cIndexesCatalogoTextoTraducciones,
        'schema_fields':    cSchemaFieldsCatalogoTextoTraducciones,
        'lexicons':         cLexiconsCatalogoTextoTraducciones,
        },   
]







# #############################################################
"""External methods to create

"""
cTRAExtMethod_ChangeAndBrowseTranslations           = "TRAChangeAndBrowseTranslations"
cTRAExtMethod_SizesIdioma                           = "TRASizesIdioma"
cTRAExtModule_TRARenderSecurity                     = "TRARenderSecurity"
cTRAExtMethod_RenderPermissionDefinitions           = "TRARenderPermissionDefinitions"
cTRAExtMethod_RenderLoggedUsedAndRolesHere          = "TRARenderLoggedUsedHere"
cTRAExtMethod_RenderGroupsRolesHere                 = "TRARenderGroupsRolesHere"
cTRAExtModule_TRARenderProfiling                    = "TRARenderProfiling"
cTRAExtMethod_RenderExecutionDetails                = "TRARenderExecutionDetails"
cTRAExtMethod_ParametersCandidateValues             = "TRAExport_ParametersCandidateValues"
cTRAExtModule_TRAExport_ctrl                        = "TRAExport_ctrl"



cTRAExternalMetodDefinitions = [
    {
        'ext_method_module':         cTRAExtMethod_ChangeAndBrowseTranslations,
        'ext_method_function':       cTRAExtMethod_ChangeAndBrowseTranslations,
        'ext_method_id':             cTRAExtMethod_ChangeAndBrowseTranslations,
        'ext_method_title':          cTRAExtMethod_ChangeAndBrowseTranslations,
        'install_path':              cTRAInstallPath_PortalSkinsCustom,
        'required':                  True,
        },
    {
        'ext_method_module':         cTRAExtMethod_ChangeAndBrowseTranslations,
        'ext_method_function':       cTRAExtMethod_SizesIdioma,
        'ext_method_id':             cTRAExtMethod_SizesIdioma,
        'ext_method_title':          cTRAExtMethod_SizesIdioma,
        'install_path':              cTRAInstallPath_PortalSkinsCustom,
        'required':                  True,
        },
    {
        'ext_method_module':         cTRAExtModule_TRARenderSecurity,
        'ext_method_function':       cTRAExtMethod_RenderPermissionDefinitions,
        'ext_method_id':             cTRAExtMethod_RenderPermissionDefinitions,
        'ext_method_title':          cTRAExtMethod_RenderPermissionDefinitions,
        'install_path':              cTRAInstallPath_PortalSkinsCustom,
        'required':                  True,
        },
    {
        'ext_method_module':         cTRAExtModule_TRARenderSecurity,
        'ext_method_function':       cTRAExtMethod_RenderLoggedUsedAndRolesHere,
        'ext_method_id':             cTRAExtMethod_RenderLoggedUsedAndRolesHere,
        'ext_method_title':          cTRAExtMethod_RenderLoggedUsedAndRolesHere,
        'install_path':              cTRAInstallPath_PortalSkinsCustom,
        'required':                  True,
        },
    {
        'ext_method_module':         cTRAExtModule_TRARenderSecurity,
        'ext_method_function':       cTRAExtMethod_RenderGroupsRolesHere,
        'ext_method_id':             cTRAExtMethod_RenderGroupsRolesHere,
        'ext_method_title':          cTRAExtMethod_RenderGroupsRolesHere,
        'install_path':              cTRAInstallPath_PortalSkinsCustom,
        'required':                  True,
        },
    {
        'ext_method_module':         cTRAExtModule_TRARenderProfiling,
        'ext_method_function':       cTRAExtMethod_RenderExecutionDetails,
        'ext_method_id':             cTRAExtMethod_RenderExecutionDetails,
        'ext_method_title':          cTRAExtMethod_RenderExecutionDetails,
        'install_path':              cTRAInstallPath_PortalSkinsCustom,
        'required':                  True,
        },    
    {
        'ext_method_module':         cTRAExtModule_TRAExport_ctrl,
        'ext_method_function':       cTRAExtMethod_ParametersCandidateValues,
        'ext_method_id':             cTRAExtMethod_ParametersCandidateValues,
        'ext_method_title':          cTRAExtMethod_ParametersCandidateValues,
        'install_path':              cTRAInstallPath_PortalSkinsCustom,
        'required':                  True,
        },    
]


cTRAInitializationDefinitions_ExternalMethods = {
    'title':             'application gvSIG-i18n',
    'external_methods':  cTRAExternalMetodDefinitions,
    'tool_singletons':   [],
}


##/code-section module-footer



