# -*- coding: utf-8 -*-
#
# File: TRAElemento_Constants_TypeNames.py
#
# Copyright (c) 2008, 2009, 2010, 2011  by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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








cNombreTipoTRACatalogo                  = "TRACatalogo"
cNombreTipoTRAIdioma                    = "TRAIdioma"
cNombreTipoTRAModulo                    = "TRAModulo"
cNombreTipoTRACadena                    = "TRACadena"
cNombreTipoTRATraduccion                = "TRATraduccion"
cNombreTipoTRAImportacion               = "TRAImportacion"
cNombreTipoTRAContenidoIntercambio      = "TRAContenidoIntercambio"
cNombreTipoTRAContenidoXML              = "TRAContenidoXML"
cNombreTipoTRAInforme                   = "TRAInforme"
cNombreTipoTRASolicitudCadena           = "TRASolicitudCadena"
cNombreTipoTRAProgreso                  = "TRAProgreso"
cNombreTipoTRAParametrosControlProgreso = "TRAParametrosControlProgreso"
cNombreTipoTRAConfiguracionImportacion  = "TRAConfiguracionImportacion"
cNombreTipoTRAConfiguracionExportacion  = "TRAConfiguracionExportacion"
cNombreTipoTRAConfiguracionSolicitudesCadenas  = "TRAConfiguracionSolicitudesCadenas"
cNombreTipoTRAConfiguracionInvalidacionInformes  = "TRAConfiguracionInvalidacionInformes"
cNombreTipoTRAConfiguracionPaginaTraducciones  = "TRAConfiguracionPaginaTraducciones"
cNombreTipoTRAConfiguracionPerfilEjecucion  = "TRAConfiguracionPerfilEjecucion"
cNombreTipoTRAConfiguracionVarios       = "TRAConfiguracionVarios"
cNombreTipoTRAConfiguracionPermisos     = "TRAConfiguracionPermisos"
cNombreTipoTRASimbolosOrdenados         = "TRASimbolosOrdenados"
cNombreTipoTRAContribuciones            = "TRAContribuciones"
cNombreTipoTRAColeccionIdiomas          = "TRAColeccionIdiomas"
cNombreTipoTRAColeccionModulos          = "TRAColeccionModulos"
cNombreTipoTRAColeccionCadenas          = "TRAColeccionCadenas"
cNombreTipoTRAColeccionInformes         = "TRAColeccionInformes"
cNombreTipoTRAColeccionImportaciones    = "TRAColeccionImportaciones"
cNombreTipoTRAColeccionSolicitudesCadenas= "TRAColeccionSolicitudesCadenas"
cNombreTipoTRAColeccionProgresos        = "TRAColeccionProgresos"
cNombreTipoTRAColeccionContribuciones   = "TRAColeccionContribuciones"


# cNombreTipo_cualquiera   = '--AnyType--'

cPreferredTypesOrder = [
    cNombreTipoTRACatalogo,               
    cNombreTipoTRAColeccionIdiomas,       
    cNombreTipoTRAIdioma,                 
    cNombreTipoTRAColeccionModulos,       
    cNombreTipoTRAModulo,                 
    cNombreTipoTRAColeccionCadenas,       
    cNombreTipoTRACadena,                 
    cNombreTipoTRATraduccion,             
    cNombreTipoTRAColeccionImportaciones, 
    cNombreTipoTRAImportacion, 
    cNombreTipoTRAContenidoIntercambio, 
    cNombreTipoTRAContenidoXML,
    cNombreTipoTRAColeccionInformes,      
    cNombreTipoTRAInforme,      
    cNombreTipoTRAColeccionSolicitudesCadenas,
    cNombreTipoTRASolicitudCadena,
    cNombreTipoTRAColeccionProgresos,
    cNombreTipoTRAColeccionContribuciones,
    cNombreTipoTRAContribuciones,
    cNombreTipoTRAProgreso,
    cNombreTipoTRAParametrosControlProgreso,
    cNombreTipoTRAConfiguracionImportacion,
    cNombreTipoTRAConfiguracionExportacion,
    cNombreTipoTRAConfiguracionSolicitudesCadenas,
    cNombreTipoTRAConfiguracionInvalidacionInformes,
    cNombreTipoTRAConfiguracionPaginaTraducciones,
    cNombreTipoTRAConfiguracionPerfilEjecucion,
    cNombreTipoTRAConfiguracionVarios,
    cNombreTipoTRAConfiguracionPermisos,
    cNombreTipoTRASimbolosOrdenados,
]




cTodosNombresTiposCacheables = [
    cNombreTipoTRACatalogo,               
    cNombreTipoTRAColeccionIdiomas,       
    cNombreTipoTRAIdioma,                 
    cNombreTipoTRAColeccionModulos,       
    cNombreTipoTRAModulo,                 
    cNombreTipoTRAColeccionCadenas,       
    cNombreTipoTRAColeccionImportaciones, 
    cNombreTipoTRAImportacion, 
    cNombreTipoTRAContenidoIntercambio,  
    cNombreTipoTRAContenidoXML,
    cNombreTipoTRAColeccionInformes,      
    cNombreTipoTRAInforme,      
    cNombreTipoTRAColeccionSolicitudesCadenas,
    cNombreTipoTRASolicitudCadena,
    cNombreTipoTRAColeccionProgresos,
    cNombreTipoTRAProgreso,
    cNombreTipoTRAParametrosControlProgreso,
    cNombreTipoTRAConfiguracionImportacion,
    cNombreTipoTRAConfiguracionExportacion,
    cNombreTipoTRAConfiguracionSolicitudesCadenas,
    cNombreTipoTRAConfiguracionInvalidacionInformes,
    cNombreTipoTRAConfiguracionPaginaTraducciones,
    cNombreTipoTRAConfiguracionPerfilEjecucion,
    cNombreTipoTRAConfiguracionVarios,
    cNombreTipoTRASimbolosOrdenados,
    cNombreTipoTRAColeccionContribuciones,
    cNombreTipoTRAContribuciones,
]


cTodosNombresTiposColecciones = [
    cNombreTipoTRAColeccionIdiomas,       
    cNombreTipoTRAColeccionModulos,       
    cNombreTipoTRAColeccionCadenas,       
    cNombreTipoTRAColeccionInformes,      
    cNombreTipoTRAColeccionImportaciones, 
    cNombreTipoTRAColeccionSolicitudesCadenas,
    cNombreTipoTRAColeccionProgresos,
    cNombreTipoTRAColeccionContribuciones,
]


cTodosNombresTiposConfiguracion = [
    cNombreTipoTRAConfiguracionImportacion,
    cNombreTipoTRAConfiguracionExportacion,
    cNombreTipoTRAConfiguracionSolicitudesCadenas,
    cNombreTipoTRAConfiguracionInvalidacionInformes,
    cNombreTipoTRAConfiguracionPaginaTraducciones,
    cNombreTipoTRAConfiguracionPerfilEjecucion,
    cNombreTipoTRAConfiguracionVarios,
    cNombreTipoTRAConfiguracionPermisos,
]


cTodosNombresTiposCompuestos = [
    cNombreTipoTRACatalogo,               
    cNombreTipoTRAIdioma,                 
    cNombreTipoTRAModulo,                 
    cNombreTipoTRACadena,                 
    cNombreTipoTRAImportacion, 
    cNombreTipoTRAProgreso,
]

cTodosNombresTiposWithChildren = cTodosNombresTiposColecciones + cTodosNombresTiposCompuestos

cTodosNombresTiposWithoutChildren = [
    cNombreTipoTRATraduccion,             
    cNombreTipoTRAContenidoIntercambio,   
    cNombreTipoTRAContenidoXML,
    cNombreTipoTRAInforme,    
    cNombreTipoTRAContribuciones,  
    cNombreTipoTRASolicitudCadena,
    cNombreTipoTRAParametrosControlProgreso,
    cNombreTipoTRAConfiguracionImportacion,
    cNombreTipoTRAConfiguracionExportacion,
    cNombreTipoTRAConfiguracionSolicitudesCadenas,
    cNombreTipoTRAConfiguracionInvalidacionInformes,
    cNombreTipoTRAConfiguracionPaginaTraducciones,
    cNombreTipoTRAConfiguracionPerfilEjecucion,
    cNombreTipoTRAConfiguracionVarios,
    cNombreTipoTRAConfiguracionPermisos,
    cNombreTipoTRASimbolosOrdenados,
 ]



cTodosNombresTipos = cPreferredTypesOrder


cTodosNombresTiposWithPotentiallyManyChildren = [
    cNombreTipoTRACatalogo,               
    cNombreTipoTRAColeccionCadenas,       
    cNombreTipoTRAColeccionImportaciones, 
]


cTodosNombresTiposWithoutPotentiallyManyChildren = [ aTypeName for aTypeName in cPreferredTypesOrder if not ( aTypeName in cTodosNombresTiposWithPotentiallyManyChildren)]


cTodosNombresTiposWithChildrenOrRelationsOrPloneElements = cTodosNombresTiposWithChildren + [
    cNombreTipoTRAContenidoIntercambio,   
    cNombreTipoTRAContenidoXML,
    cNombreTipoTRAInforme,    
    cNombreTipoTRASolicitudCadena,
    cNombreTipoTRAInforme,
    cNombreTipoTRAContribuciones,
    cNombreTipoTRAParametrosControlProgreso,
    cNombreTipoTRAConfiguracionImportacion,
    cNombreTipoTRAConfiguracionExportacion,
    cNombreTipoTRAConfiguracionSolicitudesCadenas,
    cNombreTipoTRAConfiguracionInvalidacionInformes,
    cNombreTipoTRAConfiguracionPaginaTraducciones,
    cNombreTipoTRAConfiguracionPerfilEjecucion,
    cNombreTipoTRAConfiguracionVarios,
    cNombreTipoTRAConfiguracionPermisos,
    cNombreTipoTRASimbolosOrdenados,
]


from Products.ModelDDvlPloneTool.PloneElement_TraversalConfig import cPloneTypes


cTodosNombresTiposPlone = [  aPloneTypeSpec.get( 'meta_type', '') for aPloneTypeSpec in cPloneTypes.values()]



cTodosNombresTiposCatalogables_ExcluidosDePortalCatalog = [ 
    cNombreTipoTRACadena,
    cNombreTipoTRATraduccion,
]

cTodosNombresTiposCatalogables_InPortalCatalog = [ unTipo for unTipo in ( cTodosNombresTipos + cTodosNombresTiposPlone) if not unTipo in cTodosNombresTiposCatalogables_ExcluidosDePortalCatalog]


cTodosNombresTiposDesCatalogables_DePortalCatalog = cTodosNombresTiposCatalogables_InPortalCatalog + [ 'ZCatalog',]


cTodosNombresTiposCatalogables_ChildrenExcluidosDePortalCatalog = [ 
    cNombreTipoTRAColeccionCadenas,
]


cTodosNombresTiposNODesCatalogables_DeUIDCatalog = [ 'ZCatalog',]



cTodosNombresTiposConfiguracion = [
    cNombreTipoTRAConfiguracionImportacion,
    cNombreTipoTRAConfiguracionExportacion,
    cNombreTipoTRAConfiguracionSolicitudesCadenas,
    cNombreTipoTRAConfiguracionInvalidacionInformes,
    cNombreTipoTRAConfiguracionPaginaTraducciones,
    cNombreTipoTRAConfiguracionPerfilEjecucion,
    cNombreTipoTRAConfiguracionVarios,
    cNombreTipoTRAConfiguracionPermisos,
]



cNombreTraversal_Importacion_ContenidosIntercambio = 'contenido'










cTRATypesToReuseIdsOnRestoreBackup = [ 
    cNombreTipoTRACatalogo,               
    cNombreTipoTRAColeccionIdiomas,       
    cNombreTipoTRAIdioma,                 
    cNombreTipoTRAColeccionModulos,       
    cNombreTipoTRAModulo,                 
    cNombreTipoTRAColeccionCadenas,       
    cNombreTipoTRAColeccionImportaciones, 
    cNombreTipoTRAImportacion, 
    cNombreTipoTRAContenidoIntercambio, 
    cNombreTipoTRAContenidoXML,
    cNombreTipoTRAColeccionInformes,      
    cNombreTipoTRAInforme,      
    cNombreTipoTRAColeccionSolicitudesCadenas,
    cNombreTipoTRASolicitudCadena,
    cNombreTipoTRAColeccionProgresos,
    cNombreTipoTRAProgreso,
    cNombreTipoTRAColeccionContribuciones,
    cNombreTipoTRAContribuciones,
    cNombreTipoTRAParametrosControlProgreso,
    cNombreTipoTRAConfiguracionImportacion,
    cNombreTipoTRAConfiguracionExportacion,
    cNombreTipoTRAConfiguracionSolicitudesCadenas,
    cNombreTipoTRAConfiguracionInvalidacionInformes,
    cNombreTipoTRAConfiguracionPaginaTraducciones,
    cNombreTipoTRAConfiguracionPerfilEjecucion,
    cNombreTipoTRAConfiguracionVarios,
    cNombreTipoTRAConfiguracionPermisos,
]




cTRAPloneTypeNames = [ 'ATDocument', 'ATNewsItem', 'ATLink', 'ATImage', 'ATFile', ]
cTRAPloneTypeName_ATFolder = 'ATFolder'

