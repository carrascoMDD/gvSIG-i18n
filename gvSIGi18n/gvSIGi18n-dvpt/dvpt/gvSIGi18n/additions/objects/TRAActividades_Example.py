# -*- coding: utf-8 -*-
#
# File: TRAActividades_Example.py
#
# Copyright (c) 2009, 2010 by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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



##code-section module-header #fill in your manual code here

from DateTime import DateTime

from Products.CMFCore               import permissions

from Products.CMFCore.utils         import SimpleRecord



##/code-section module-header

##code-section after-local-schema #fill in your manual code here

#cRecentActivity_Date      = 'Date'
#cRecentActivity_User      = 'User'
#cRecentActivity_Language  = 'Lang'
#cRecentActivity_Symbol    = 'Symb'
#cRecentActivity_Action    = 'Actn'
#cRecentActivity_Commented = 'Cmnt'
#cRecentActivity_Counter   = 'Cntr'


cActividades_Example_Template = [
    # ####################
    # Today: 14
    { 'Date': 0, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': '(escala_maxima)', 'Actn': 'Traducir',},
    { 'Date': 0, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': '(escala_minima)', 'Actn': 'Traducir',},
    { 'Date': 0, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'A0', 'Actn': 'Traducir',},  
    { 'Date': 0, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'A1', 'Actn': 'Traducir',},  
    { 'Date': 0, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'A2', 'Actn': 'Traducir',},  
    { 'Date': 0, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'A3', 'Actn': 'Traducir',},  
    { 'Date': 0, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': '1', 'Actn': 'Traducir',},
    { 'Date': 0, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': '10_paginas_delante', 'Actn': 'Traducir',},
    { 'Date': 0, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'A4', 'Actn': 'Traducir',},  
    { 'Date': 0, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'A5', 'Actn': 'Traducir',},  
    { 'Date': 0, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'A6', 'Actn': 'Traducir',},  
    { 'Date': 0, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'ARC', 'Actn': 'Traducir',},  
    { 'Date': 0, 'User': 'tratranslator5', 'Lang': 'en', 'Symb': 'A6', 'Actn': 'Traducir',},  
    { 'Date': 0, 'User': 'tratranslator5', 'Lang': 'en', 'Symb': 'ARC', 'Actn': 'Traducir',},  

    # ####################
    # Yesterday: 12
    { 'Date': 1, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': 'Abrir', 'Actn': 'Traducir',},
    { 'Date': 1, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': 'Abrir_Geoproceso', 'Actn': 'Traducir',},
    { 'Date': 1, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Abrir_Imagen', 'Actn': 'Traducir',},  
    { 'Date': 1, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Abrir_una_capa', 'Actn': 'Traducir',},  
    { 'Date': 1, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Accept', 'Actn': 'Traducir',},  
    { 'Date': 1, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Accion_Predefinida', 'Actn': 'Traducir',},  
    { 'Date': 1, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': 'Acciones', 'Actn': 'Traducir',},
    { 'Date': 1, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': 'Accumulated_distance', 'Actn': 'Traducir',},
    { 'Date': 1, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'Aceptar', 'Actn': 'Traducir',},  
    { 'Date': 1, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'Acres', 'Actn': 'Traducir',},  
    { 'Date': 1, 'User': 'tratranslator6', 'Lang': 'en', 'Symb': 'Action', 'Actn': 'Traducir',},  
    { 'Date': 1, 'User': 'tratranslator6', 'Lang': 'en', 'Symb': 'Actions', 'Actn': 'Traducir',}, 

    # ####################
    # Last 7 days 26 + 16 (2) + 18 (6) + 20 (7) = 80
    { 'Date': 2, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': 'Add_action', 'Actn': 'Traducir',},
    { 'Date': 2, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': 'Add_geometric_information_to_layer_process', 'Actn': 'Traducir',},
    { 'Date': 2, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Added_buffer_areas_to_TOC', 'Actn': 'Traducir',},  
    { 'Date': 2, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Added_layer_with_influence_areas_to_TOC', 'Actn': 'Traducir',},  
    { 'Date': 2, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Advanced_Hyperlink', 'Actn': 'Traducir',},  
    { 'Date': 2, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Aggregation', 'Actn': 'Traducir',},  
    { 'Date': 2, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': 'Agregacion_Desc', 'Actn': 'Traducir',},
    { 'Date': 2, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': 'Agudeza', 'Actn': 'Traducir',},
    { 'Date': 2, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'Aitoff', 'Actn': 'Traducir',},  
    { 'Date': 2, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'Ajustar_cobertura_wcs', 'Actn': 'Traducir',},  
    { 'Date': 2, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 2, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 2, 'User': 'tratranslator5', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 2, 'User': 'tratranslator5', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 2, 'User': 'tratranslator7', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 2, 'User': 'tratranslator7', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  

    { 'Date': 6, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': 'Add_action', 'Actn': 'Traducir',},
    { 'Date': 6, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': 'Add_geometric_information_to_layer_process', 'Actn': 'Traducir',},
    { 'Date': 6, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Added_buffer_areas_to_TOC', 'Actn': 'Traducir',},  
    { 'Date': 6, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Added_layer_with_influence_areas_to_TOC', 'Actn': 'Traducir',},  
    { 'Date': 6, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Advanced_Hyperlink', 'Actn': 'Traducir',},  
    { 'Date': 6, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Aggregation', 'Actn': 'Traducir',},  
    { 'Date': 6, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': 'Agregacion_Desc', 'Actn': 'Traducir',},
    { 'Date': 6, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': 'Agudeza', 'Actn': 'Traducir',},
    { 'Date': 6, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'Aitoff', 'Actn': 'Traducir',},  
    { 'Date': 6, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'Ajustar_cobertura_wcs', 'Actn': 'Traducir',},  
    { 'Date': 6, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 6, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 6, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 6, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 6, 'User': 'tratranslator8', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 6, 'User': 'tratranslator8', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 6, 'User': 'tratranslator8', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 6, 'User': 'tratranslator8', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  

    { 'Date': 7, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': 'Add_action', 'Actn': 'Traducir',},
    { 'Date': 7, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': 'Add_geometric_information_to_layer_process', 'Actn': 'Traducir',},
    { 'Date': 7, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Added_buffer_areas_to_TOC', 'Actn': 'Traducir',},  
    { 'Date': 7, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Added_layer_with_influence_areas_to_TOC', 'Actn': 'Traducir',},  
    { 'Date': 7, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Advanced_Hyperlink', 'Actn': 'Traducir',},  
    { 'Date': 7, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Aggregation', 'Actn': 'Traducir',},  
    { 'Date': 7, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': 'Agregacion_Desc', 'Actn': 'Traducir',},
    { 'Date': 7, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': 'Agudeza', 'Actn': 'Traducir',},
    { 'Date': 7, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'Aitoff', 'Actn': 'Traducir',},  
    { 'Date': 7, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'Ajustar_cobertura_wcs', 'Actn': 'Traducir',},  
    { 'Date': 7, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 7, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 7, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 7, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 7, 'User': 'tratranslator9', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 7, 'User': 'tratranslator9', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 7, 'User': 'tratranslator9', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 7, 'User': 'tratranslator9', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 7, 'User': 'tratranslator9', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 7, 'User': 'tratranslator9', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  

    # ####################
    # Last 30 days 80 + 16 (8) + 20 (9) + 16 (29) + 16 (30) = 148
    { 'Date': 8, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': 'Add_action', 'Actn': 'Traducir',},
    { 'Date': 8, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': 'Add_geometric_information_to_layer_process', 'Actn': 'Traducir',},
    { 'Date': 8, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Added_buffer_areas_to_TOC', 'Actn': 'Traducir',},  
    { 'Date': 8, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Added_layer_with_influence_areas_to_TOC', 'Actn': 'Traducir',},  
    { 'Date': 8, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Advanced_Hyperlink', 'Actn': 'Traducir',},  
    { 'Date': 8, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Aggregation', 'Actn': 'Traducir',},  
    { 'Date': 8, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': 'Agregacion_Desc', 'Actn': 'Traducir',},
    { 'Date': 8, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': 'Agudeza', 'Actn': 'Traducir',},
    { 'Date': 8, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'Aitoff', 'Actn': 'Traducir',},  
    { 'Date': 8, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'Ajustar_cobertura_wcs', 'Actn': 'Traducir',},  
    { 'Date': 8, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 8, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 8, 'User': 'tratranslator5', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 8, 'User': 'tratranslator5', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 8, 'User': 'tratranslator5', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 8, 'User': 'tratranslator5', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  

    { 'Date': 9, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': 'Add_action', 'Actn': 'Traducir',},
    { 'Date': 9, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': 'Add_geometric_information_to_layer_process', 'Actn': 'Traducir',},
    { 'Date': 9, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Added_buffer_areas_to_TOC', 'Actn': 'Traducir',},  
    { 'Date': 9, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Added_layer_with_influence_areas_to_TOC', 'Actn': 'Traducir',},  
    { 'Date': 9, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Advanced_Hyperlink', 'Actn': 'Traducir',},  
    { 'Date': 9, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Aggregation', 'Actn': 'Traducir',},  
    { 'Date': 9, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': 'Agregacion_Desc', 'Actn': 'Traducir',},
    { 'Date': 9, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': 'Agudeza', 'Actn': 'Traducir',},
    { 'Date': 9, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'Aitoff', 'Actn': 'Traducir',},  
    { 'Date': 9, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'Ajustar_cobertura_wcs', 'Actn': 'Traducir',},  
    { 'Date': 9, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 9, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 9, 'User': 'tratranslator9', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 9, 'User': 'tratranslator9', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 9, 'User': 'tratranslator9', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 9, 'User': 'tratranslator9', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 9, 'User': 'tratranslator9', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 9, 'User': 'tratranslator9', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 9, 'User': 'tratranslator9', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 9, 'User': 'tratranslator9', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  

    { 'Date': 29, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': 'Add_action', 'Actn': 'Traducir',},
    { 'Date': 29, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': 'Add_geometric_information_to_layer_process', 'Actn': 'Traducir',},
    { 'Date': 29, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Added_buffer_areas_to_TOC', 'Actn': 'Traducir',},  
    { 'Date': 29, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Added_layer_with_influence_areas_to_TOC', 'Actn': 'Traducir',},  
    { 'Date': 29, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Advanced_Hyperlink', 'Actn': 'Traducir',},  
    { 'Date': 29, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Aggregation', 'Actn': 'Traducir',},  
    { 'Date': 29, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': 'Agregacion_Desc', 'Actn': 'Traducir',},
    { 'Date': 29, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': 'Agudeza', 'Actn': 'Traducir',},
    { 'Date': 29, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'Aitoff', 'Actn': 'Traducir',},  
    { 'Date': 29, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'Ajustar_cobertura_wcs', 'Actn': 'Traducir',},  
    { 'Date': 29, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 29, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 29, 'User': 'tratranslator7', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 29, 'User': 'tratranslator7', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 29, 'User': 'tratranslator7', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 29, 'User': 'tratranslator7', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  

    { 'Date': 30, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': 'Add_action', 'Actn': 'Traducir',},
    { 'Date': 30, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': 'Add_geometric_information_to_layer_process', 'Actn': 'Traducir',},
    { 'Date': 30, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Added_buffer_areas_to_TOC', 'Actn': 'Traducir',},  
    { 'Date': 30, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Added_layer_with_influence_areas_to_TOC', 'Actn': 'Traducir',},  
    { 'Date': 30, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Advanced_Hyperlink', 'Actn': 'Traducir',},  
    { 'Date': 30, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Aggregation', 'Actn': 'Traducir',},  
    { 'Date': 30, 'User': 'tratranslator0', 'Lang': 'es', 'Symb': 'Advanced_Hyperlink', 'Actn': 'Traducir',},  
    { 'Date': 30, 'User': 'tratranslator0', 'Lang': 'es', 'Symb': 'Aggregation', 'Actn': 'Traducir',},  
    { 'Date': 30, 'User': 'tratranslator0', 'Lang': 'es', 'Symb': 'Advanced_Hyperlink', 'Actn': 'Traducir',},  
    { 'Date': 30, 'User': 'tratranslator0', 'Lang': 'es', 'Symb': 'Aggregation', 'Actn': 'Traducir',},  
    { 'Date': 30, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': 'Agregacion_Desc', 'Actn': 'Traducir',},
    { 'Date': 30, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': 'Agudeza', 'Actn': 'Traducir',},
    { 'Date': 30, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'Aitoff', 'Actn': 'Traducir',},  
    { 'Date': 30, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'Ajustar_cobertura_wcs', 'Actn': 'Traducir',},  
    { 'Date': 30, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 30, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  

    # ####################
    # Before 30 days 148 + 14 (31) + 24 (32) + 26 (33) + 26 (34) = 238 
    { 'Date': 31, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': 'Add_action', 'Actn': 'Traducir',},
    { 'Date': 31, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': 'Add_geometric_information_to_layer_process', 'Actn': 'Traducir',},
    { 'Date': 31, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Added_buffer_areas_to_TOC', 'Actn': 'Traducir',},  
    { 'Date': 31, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Added_layer_with_influence_areas_to_TOC', 'Actn': 'Traducir',},  
    { 'Date': 31, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Advanced_Hyperlink', 'Actn': 'Traducir',},  
    { 'Date': 31, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Aggregation', 'Actn': 'Traducir',},  
    { 'Date': 31, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': 'Agregacion_Desc', 'Actn': 'Traducir',},
    { 'Date': 31, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': 'Agudeza', 'Actn': 'Traducir',},
    { 'Date': 31, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'Aitoff', 'Actn': 'Traducir',},  
    { 'Date': 31, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'Ajustar_cobertura_wcs', 'Actn': 'Traducir',},  
    { 'Date': 31, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 31, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 31, 'User': 'tratranslator6', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 31, 'User': 'tratranslator6', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  


    { 'Date': 32, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': 'Add_action', 'Actn': 'Traducir',},
    { 'Date': 32, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': 'Add_geometric_information_to_layer_process', 'Actn': 'Traducir',},
    { 'Date': 32, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Added_buffer_areas_to_TOC', 'Actn': 'Traducir',},  
    { 'Date': 32, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Added_layer_with_influence_areas_to_TOC', 'Actn': 'Traducir',},  
    { 'Date': 32, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Advanced_Hyperlink', 'Actn': 'Traducir',},  
    { 'Date': 32, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Aggregation', 'Actn': 'Traducir',},  
    { 'Date': 32, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Advanced_Hyperlink', 'Actn': 'Traducir',},  
    { 'Date': 32, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Aggregation', 'Actn': 'Traducir',},  
    { 'Date': 32, 'User': 'tratranslator0', 'Lang': 'es', 'Symb': 'Advanced_Hyperlink', 'Actn': 'Traducir',},  
    { 'Date': 32, 'User': 'tratranslator0', 'Lang': 'es', 'Symb': 'Aggregation', 'Actn': 'Traducir',},  
    { 'Date': 32, 'User': 'tratranslator0', 'Lang': 'es', 'Symb': 'Advanced_Hyperlink', 'Actn': 'Traducir',},  
    { 'Date': 32, 'User': 'tratranslator0', 'Lang': 'es', 'Symb': 'Aggregation', 'Actn': 'Traducir',},  
    { 'Date': 32, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': 'Agregacion_Desc', 'Actn': 'Traducir',},
    { 'Date': 32, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': 'Agudeza', 'Actn': 'Traducir',},
    { 'Date': 32, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'Aitoff', 'Actn': 'Traducir',},  
    { 'Date': 32, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'Ajustar_cobertura_wcs', 'Actn': 'Traducir',},  
    { 'Date': 32, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 32, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 32, 'User': 'tratranslator8', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 32, 'User': 'tratranslator8', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 32, 'User': 'tratranslator8', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 32, 'User': 'tratranslator8', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 32, 'User': 'tratranslator8', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 32, 'User': 'tratranslator8', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  


    { 'Date': 33, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': 'Add_action', 'Actn': 'Traducir',},
    { 'Date': 33, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': 'Add_geometric_information_to_layer_process', 'Actn': 'Traducir',},
    { 'Date': 33, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Added_buffer_areas_to_TOC', 'Actn': 'Traducir',},  
    { 'Date': 33, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Added_layer_with_influence_areas_to_TOC', 'Actn': 'Traducir',},  
    { 'Date': 33, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Advanced_Hyperlink', 'Actn': 'Traducir',},  
    { 'Date': 33, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Aggregation', 'Actn': 'Traducir',},  
    { 'Date': 33, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Advanced_Hyperlink', 'Actn': 'Traducir',},  
    { 'Date': 33, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Aggregation', 'Actn': 'Traducir',},  
    { 'Date': 33, 'User': 'tratranslator0', 'Lang': 'es', 'Symb': 'Advanced_Hyperlink', 'Actn': 'Traducir',},  
    { 'Date': 33, 'User': 'tratranslator0', 'Lang': 'es', 'Symb': 'Aggregation', 'Actn': 'Traducir',},  
    { 'Date': 33, 'User': 'tratranslator0', 'Lang': 'es', 'Symb': 'Advanced_Hyperlink', 'Actn': 'Traducir',},  
    { 'Date': 33, 'User': 'tratranslator0', 'Lang': 'es', 'Symb': 'Aggregation', 'Actn': 'Traducir',},  
    { 'Date': 33, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': 'Agregacion_Desc', 'Actn': 'Traducir',},
    { 'Date': 33, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': 'Agudeza', 'Actn': 'Traducir',},
    { 'Date': 33, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'Aitoff', 'Actn': 'Traducir',},  
    { 'Date': 33, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'Ajustar_cobertura_wcs', 'Actn': 'Traducir',},  
    { 'Date': 33, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 33, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 33, 'User': 'tratranslator8', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 33, 'User': 'tratranslator8', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 33, 'User': 'tratranslator8', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 33, 'User': 'tratranslator8', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 33, 'User': 'tratranslator8', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 33, 'User': 'tratranslator8', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  


    { 'Date': 34, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': 'Add_action', 'Actn': 'Traducir',},
    { 'Date': 34, 'User': 'tratranslator1', 'Lang': 'es', 'Symb': 'Add_geometric_information_to_layer_process', 'Actn': 'Traducir',},
    { 'Date': 34, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Added_buffer_areas_to_TOC', 'Actn': 'Traducir',},  
    { 'Date': 34, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Added_layer_with_influence_areas_to_TOC', 'Actn': 'Traducir',},  
    { 'Date': 34, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Advanced_Hyperlink', 'Actn': 'Traducir',},  
    { 'Date': 34, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Aggregation', 'Actn': 'Traducir',},  
    { 'Date': 34, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Advanced_Hyperlink', 'Actn': 'Traducir',},  
    { 'Date': 34, 'User': 'tratranslator2', 'Lang': 'es', 'Symb': 'Aggregation', 'Actn': 'Traducir',},  
    { 'Date': 34, 'User': 'tratranslator0', 'Lang': 'es', 'Symb': 'Advanced_Hyperlink', 'Actn': 'Traducir',},  
    { 'Date': 34, 'User': 'tratranslator0', 'Lang': 'es', 'Symb': 'Aggregation', 'Actn': 'Traducir',},  
    { 'Date': 34, 'User': 'tratranslator0', 'Lang': 'es', 'Symb': 'Advanced_Hyperlink', 'Actn': 'Traducir',},  
    { 'Date': 34, 'User': 'tratranslator0', 'Lang': 'es', 'Symb': 'Aggregation', 'Actn': 'Traducir',},  
    { 'Date': 34, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': 'Agregacion_Desc', 'Actn': 'Traducir',},
    { 'Date': 34, 'User': 'tratranslator3', 'Lang': 'en', 'Symb': 'Agudeza', 'Actn': 'Traducir',},
    { 'Date': 34, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'Aitoff', 'Actn': 'Traducir',},  
    { 'Date': 34, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': 'Ajustar_cobertura_wcs', 'Actn': 'Traducir',},  
    { 'Date': 34, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 34, 'User': 'tratranslator4', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 34, 'User': 'tratranslator8', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 34, 'User': 'tratranslator8', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 34, 'User': 'tratranslator8', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 34, 'User': 'tratranslator8', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  
    { 'Date': 34, 'User': 'tratranslator8', 'Lang': 'en', 'Symb': '"Launcher', 'Actn': 'Traducir',},  
    { 'Date': 34, 'User': 'tratranslator8', 'Lang': 'en', 'Symb': '"Launcher.Dos_skin_extension', 'Actn': 'Traducir',},  

]








##/code-section after-local-schema


##code-section after-schema #fill in your manual code here



def fcActividadesExample( theBaseDate=None):

    from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import  fDateTimeNow

    aDateTimeNow = theBaseDate
    if not aDateTimeNow:
        aDateTimeNow = fDateTimeNow()

    aDateTimeNowString = aDateTimeNow.ISO()    
    aTodayString =  aDateTimeNowString[:10]
    aToday = DateTime( aTodayString)

    someActividades = [ ]

    for anActividad_Template in cActividades_Example_Template:
        aRelativeDate = anActividad_Template.get( 'Date', -1)
        if aRelativeDate >= 0:

            anActividad_Example = anActividad_Template.copy()

            if not aRelativeDate:
                anActividadDateString = aTodayString
            else:
                anActividadDate = aToday - aRelativeDate
                anActividadDateString = anActividadDate.ISO()

            anActividad_Example[ 'Date'] = anActividadDateString

            someActividades.append( anActividad_Example)

    return someActividades



##/code-section module-footer



