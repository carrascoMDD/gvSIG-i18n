# -*- coding: utf-8 -*-
#
# File: TRAConfiguracionAlmacenPaginas.py
#
# Copyright (c) 2011 by 2008, 2009, 2010 Conselleria de Infraestructuras y
# Transporte de la Generalidad Valenciana
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

__author__ = """Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
<gvSIGi18n@gvSIG.org>, Model Driven Development sl <gvSIGi18n@ModelDD.org>,
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.gvSIGi18n.TRAConfiguracion import TRAConfiguracion
from TRAConfiguracionAlmacenPaginas_Operaciones import TRAConfiguracionAlmacenPaginas_Operaciones
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from TRAElemento_Operaciones import TRAElemento_Operaciones

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    IntegerField(
        name='segundosMinimosRetencionInformeIdiomas',
        widget=IntegerField._properties['widget'](
            label="Minimo Tiempo en segundos que se retiene el Informe de Estado por Idiomas",
            label2="Minimum Time in seconds to retain Status Report by Languages",
            description="Tiempo en segundos que se retendra el Informe de Estado por Idiomas, aunque sus resultados sean inexactos por alguna modificacion del estado de traducciones, para evitar recalculo excesivo por cambios poco relevantes.",
            description2="Time in seconds that the Status Report by Languages shall be retained, even if the results have become inaccurate because of any modification of translations status. To avoid excessive recalculation for barely relevant changes.",
            label_msgid='gvSIGi18n_TRAConfiguracionAlmacenPaginas_attr_segundosMinimosRetencionInformeIdiomas_label',
            description_msgid='gvSIGi18n_TRAConfiguracionAlmacenPaginas_attr_segundosMinimosRetencionInformeIdiomas_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Tiempo en segundos que se retendra el Informe de Estado por Idiomas, aunque sus resultados sean inexactos por alguna modificacion del estado de traducciones, para evitar recalculo excesivo por cambios poco relevantes.",
        duplicates="0",
        label2="Minimum Time in seconds to retain Status Report by Languages",
        ea_localid="1944",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Time in seconds that the Status Report by Languages shall be retained, even if the results have become inaccurate because of any modification of translations status. To avoid excessive recalculation for barely relevant changes.",
        ea_guid="{8023B0D7-0568-4e4b-AFC5-1615DBE0C70D}",
        scale="0",
        default="120",
        label="Minimo Tiempo en segundos que se retiene el Informe de Estado por Idiomas",
        length="0",
        containment="Not Specified",
        position="28",
        owner_class_name="TRAConfiguracionAlmacenPaginas"
    ),

    IntegerField(
        name='numeroDeCambiosAnularInformeIdiomas',
        widget=IntegerField._properties['widget'](
            label="Cambios para Anular Informe Idiomas",
            label2="Changes to invalidate Report by Languages",
            description="Numero de cambios de estado de Traducciones que causan la anulacion del Informe de Estado por Idiomas, incluso aunque no haya expirado el plazo de retencion del informe.",
            description2="Number of Translation status changes that shall cause the invalidation of the Status Report by Languages, even if the minimum retention time has not lapsed yet.",
            label_msgid='gvSIGi18n_TRAConfiguracionAlmacenPaginas_attr_numeroDeCambiosAnularInformeIdiomas_label',
            description_msgid='gvSIGi18n_TRAConfiguracionAlmacenPaginas_attr_numeroDeCambiosAnularInformeIdiomas_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Numero de cambios de estado de Traducciones que causan la anulacion del Informe de Estado por Idiomas, incluso aunque no haya expirado el plazo de retencion del informe.",
        duplicates="0",
        label2="Changes to invalidate Report by Languages",
        ea_localid="1938",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Number of Translation status changes that shall cause the invalidation of the Status Report by Languages, even if the minimum retention time has not lapsed yet.",
        ea_guid="{DFFB139A-0711-49d1-94EE-8EFA6730A3F3}",
        scale="0",
        default="5",
        label="Cambios para Anular Informe Idiomas",
        length="0",
        containment="Not Specified",
        position="20",
        owner_class_name="TRAConfiguracionAlmacenPaginas"
    ),

    IntegerField(
        name='segundosMinimosRetencionInformeModulosEIdiomas',
        widget=IntegerField._properties['widget'](
            label="Minimo Tiempo en segundos que se retiene el Informe de Estado por Modulos e Idiomas",
            label2="Minimum Time in seconds to retain Status Report by Modules and Languages",
            description="Tiempo en segundos que se retendra el Informe de Estado por Modulos e Idiomas, aunque sus resultados sean inexactos por alguna modificacion del estado de traducciones, para evitar recalculo excesivo por cambios poco relevantes.",
            description2="Time in seconds that the Status Report by Modules and Languages shall be retained, even if the results have become inaccurate because of any modification of translations status. To avoid excessive recalculation for barely relevant changes.",
            label_msgid='gvSIGi18n_TRAConfiguracionAlmacenPaginas_attr_segundosMinimosRetencionInformeModulosEIdiomas_label',
            description_msgid='gvSIGi18n_TRAConfiguracionAlmacenPaginas_attr_segundosMinimosRetencionInformeModulosEIdiomas_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Tiempo en segundos que se retendra el Informe de Estado por Modulos e Idiomas, aunque sus resultados sean inexactos por alguna modificacion del estado de traducciones, para evitar recalculo excesivo por cambios poco relevantes.",
        duplicates="0",
        label2="Minimum Time in seconds to retain Status Report by Modules and Languages",
        ea_localid="1945",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Time in seconds that the Status Report by Modules and Languages shall be retained, even if the results have become inaccurate because of any modification of translations status. To avoid excessive recalculation for barely relevant changes.",
        ea_guid="{36338F92-0952-41a4-A609-AF9AD0ECB0A2}",
        scale="0",
        default="300",
        label="Minimo Tiempo en segundos que se retiene el Informe de Estado por Modulos e Idiomas",
        length="0",
        containment="Not Specified",
        position="29",
        owner_class_name="TRAConfiguracionAlmacenPaginas"
    ),

    IntegerField(
        name='numeroDeCambiosAnularInformeModulosEIdiomas',
        widget=IntegerField._properties['widget'](
            label="Cambios para Anular Informe Modulos e Idiomas",
            label2="Changes to invalidate Report by Modules and Languages",
            description="Numero de cambios de estado de Traducciones que causan la anulacion del Informe de Estado por Modulos e Idiomas, incluso aunque no haya expirado el plazo de retencion del informe.",
            description2="Number of Translation status changes that shall cause the invalidation of the Status Report by Modules and Languages, even if the minimum retention time has not lapsed yet.",
            label_msgid='gvSIGi18n_TRAConfiguracionAlmacenPaginas_attr_numeroDeCambiosAnularInformeModulosEIdiomas_label',
            description_msgid='gvSIGi18n_TRAConfiguracionAlmacenPaginas_attr_numeroDeCambiosAnularInformeModulosEIdiomas_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Numero de cambios de estado de Traducciones que causan la anulacion del Informe de Estado por Modulos e Idiomas, incluso aunque no haya expirado el plazo de retencion del informe.",
        duplicates="0",
        label2="Changes to invalidate Report by Modules and Languages",
        ea_localid="1939",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Number of Translation status changes that shall cause the invalidation of the Status Report by Modules and Languages, even if the minimum retention time has not lapsed yet.",
        ea_guid="{28A914EF-A2CD-4df0-BBBF-7C3BA43576AC}",
        scale="0",
        default="20",
        label="Cambios para Anular Informe Modulos e Idiomas",
        length="0",
        containment="Not Specified",
        position="21",
        owner_class_name="TRAConfiguracionAlmacenPaginas"
    ),

    IntegerField(
        name='numeroDeActividadesAnularInformeActividad',
        widget=IntegerField._properties['widget'](
            label="Cambios para Anular Informe Actividad",
            label2="Changes to invalidate Activity Report",
            description="Numero de Actividades que causan la anulacion del Informe de Actividad, incluso aunque no haya expirado el plazo de retencion del informe.",
            description2="Number of Activities that shall cause the invalidation of the Activity Report, even if the minimum retention time has not lapsed yet.",
            label_msgid='gvSIGi18n_TRAConfiguracionAlmacenPaginas_attr_numeroDeActividadesAnularInformeActividad_label',
            description_msgid='gvSIGi18n_TRAConfiguracionAlmacenPaginas_attr_numeroDeActividadesAnularInformeActividad_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Numero de Actividades que causan la anulacion del Informe de Actividad, incluso aunque no haya expirado el plazo de retencion del informe.",
        duplicates="0",
        label2="Changes to invalidate Activity Report",
        ea_localid="1937",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Number of Activities that shall cause the invalidation of the Activity Report, even if the minimum retention time has not lapsed yet.",
        ea_guid="{A36F9A3A-F26E-48a4-B91E-CCE6565C29E5}",
        scale="0",
        default="3",
        label="Cambios para Anular Informe Actividad",
        length="0",
        containment="Not Specified",
        position="19",
        owner_class_name="TRAConfiguracionAlmacenPaginas"
    ),

    IntegerField(
        name='segundosMinimosRetencionInformeActividad',
        widget=IntegerField._properties['widget'](
            label="Minimo Tiempo en segundos que se retiene el Informe de Actividad",
            label2="Minimum Time in seconds to retain the Activity Report",
            description="Tiempo en segundos que se retendra el Informe deActividad, aunque sus resultados sean inexactos por alguna modificacion del estado de traducciones, para evitar recalculo excesivo por cambios poco relevantes.",
            description2="Time in seconds that the Activity Report shall be retained, even if the results have become inaccurate because of any modification of translations status. To avoid excessive recalculation for barely relevant changes.",
            label_msgid='gvSIGi18n_TRAConfiguracionAlmacenPaginas_attr_segundosMinimosRetencionInformeActividad_label',
            description_msgid='gvSIGi18n_TRAConfiguracionAlmacenPaginas_attr_segundosMinimosRetencionInformeActividad_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Tiempo en segundos que se retendra el Informe deActividad, aunque sus resultados sean inexactos por alguna modificacion del estado de traducciones, para evitar recalculo excesivo por cambios poco relevantes.",
        duplicates="0",
        label2="Minimum Time in seconds to retain the Activity Report",
        ea_localid="1943",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Time in seconds that the Activity Report shall be retained, even if the results have become inaccurate because of any modification of translations status. To avoid excessive recalculation for barely relevant changes.",
        ea_guid="{52F747E1-A4EE-4bcb-AF38-2CCD6673E12F}",
        scale="0",
        default="60",
        label="Minimo Tiempo en segundos que se retiene el Informe de Actividad",
        length="0",
        containment="Not Specified",
        position="27",
        owner_class_name="TRAConfiguracionAlmacenPaginas"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAConfiguracionAlmacenPaginas_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAConfiguracion, 'schema', Schema(())).copy() + \
    getattr(TRAConfiguracionAlmacenPaginas_Operaciones, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAConfiguracionAlmacenPaginas(OrderedBaseFolder, TRAConfiguracion, TRAConfiguracionAlmacenPaginas_Operaciones):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAConfiguracion,'__implements__',()),) + (getattr(TRAConfiguracionAlmacenPaginas_Operaciones,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Configuracion Almacen Paginas'

    meta_type = 'TRAConfiguracionAlmacenPaginas'
    portal_type = 'TRAConfiguracionAlmacenPaginas'


    # Change Audit fields

    creation_date_field = 'fechaCreacion'
    creation_user_field = 'usuarioCreador'
    modification_date_field = 'fechaModificacion'
    modification_user_field = 'usuarioModificador'
    deletion_date_field = 'fechaEliminacion'
    deletion_user_field = 'usuarioEliminador'
    is_inactive_field = 'estaInactivo'
    change_counter_field = 'contadorCambios'
    change_log_field = 'registroDeCambios'



    allowed_content_types = [] + list(getattr(TRAConfiguracion, 'allowed_content_types', [])) + list(getattr(TRAConfiguracionAlmacenPaginas_Operaciones, 'allowed_content_types', []))
    filter_content_types             = 1
    global_allow                     = 0
    content_icon = 'traconfiguracion.gif'
    immediate_view                   = 'Tabular'
    default_view                     = 'Tabular'
    suppl_views                      = ['Tabular',]
    typeDescription                  = "Configuracion del catalogo de traducciones, con parametros controlando las operaciones del almacen de paginas del catalogo."
    typeDescMsgId                    =  'gvSIGi18n_TRAConfiguracionAlmacenPaginas_help'
    archetype_name2                  = 'Pages Cache Configuration'
    typeDescription2                 = '''Translations catalog configuration, with parameters controlling translations catalog cache operations.'''
    archetype_name_msgid             = 'gvSIGi18n_TRAConfiguracionAlmacenPaginas_label'
    factory_methods                  = None
    factory_enablers                 = None
    propagate_delete_impact_to       = None
    allow_discussion = False


    actions =  (


       {'action': "string:${object_url}/Editar",
        'category': "object_buttons",
        'id': 'TRA_configurar',
        'name': 'Configure',
        'permissions': ("Modify portal content",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Configure_TRAConfiguracion')"""
       },


       {'action': "string:$object_url/Editar",
        'category': "object",
        'id': 'edit',
        'name': 'Edit',
        'permissions': ("Modify portal content",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Configure_TRAConfiguracion')"""
       },


       {'action': "string:${object_url}/Tabular",
        'category': "object",
        'id': 'view',
        'name': 'View',
        'permissions': ("View",),
        'condition': """python:object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'View_any_TRA_element')"""
       },


       {'action': "string:${object_url}/MDDCacheStatus/",
        'category': "object_buttons",
        'id': 'mddcachestatus',
        'name': 'Cache',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'CacheStatus_on_any_TRA_element')"""
       },


       {'action': "string:${object_url}/MDDChanges",
        'category': "object_buttons",
        'id': 'mddchanges',
        'name': 'Changes',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Changes_on_any_TRA_element')"""
       },


       {'action': "string:$object_url/content_status_history",
        'category': "object",
        'id': 'content_status_history',
        'name': 'State',
        'permissions': ("View",),
        'condition': """python:0"""
       },


       {'action': "string:${object_url}/TRAFlushCache_action",
        'category': "object_buttons",
        'id': 'tra_flushcache',
        'name': 'FlushCache',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fRoleQuery_IsAnyRol( object, [ 'Manager', 'Owner', 'TRACreator', 'TRAManager', 'TRACoordinator',])"""
       },


       {'action': "string:${object_url}/folder_listing",
        'category': "folder",
        'id': 'folderlisting',
        'name': 'Folder Listing',
        'permissions': ("View",),
        'condition': """python:0"""
       },


       {'action': "string:${object_url}/TRAInventory_action",
        'category': "object_buttons",
        'id': 'TRA_inventario',
        'name': 'Inventory',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Inventory_TRAElemento')"""
       },


       {'action': "string:${object_url}/sharing",
        'category': "object",
        'id': 'local_roles',
        'name': 'Sharing',
        'permissions': ("Manage properties",),
        'condition': """python:0"""
       },


       {'action': "string:${object_url}/TRARecatalog_action",
        'category': "object_buttons",
        'id': 'TRA_recatalogar',
        'name': 'ReCatalog',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'ReCatalog_TRAElemento')"""
       },


       {'action': "string:${object_url}/TRAResetPermissions_action",
        'category': "object_buttons",
        'id': 'TRA_reestablecerpermisos',
        'name': 'Reset Permissions',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'ResetPermissions_TRAElemento')"""
       },


       {'action': "string:${object_url}/TRAVerifyPermissions_action",
        'category': "object_buttons",
        'id': 'TRA_verificarpermisos',
        'name': 'Verify Permissions',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'VerifyPermissions_TRAElemento')"""
       },


       {'action': "string:${object_url}/reference_graph",
        'category': "object",
        'id': 'references',
        'name': 'References',
        'permissions': ("Modify portal content",),
        'condition': """python:0"""
       },


       {'action': "string:${object_url}/TRASeguridadUsuarioConectado",
        'category': "object_buttons",
        'id': 'TRA_SeguridadUsuarioConectado',
        'name': 'Permissions',
        'permissions': ("View",),
        'condition': """python:object.fHasTRAtool() and object.TRAgvSIGi18n_tool.fUseCaseCheckDoable( object, 'Permissions_on_any_TRA_element')"""
       },


    )

    _at_rename_after_creation = True

    schema = TRAConfiguracionAlmacenPaginas_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata', 'sharing', 'folderContents']:
            a['visible'] = 0
    return fti

registerType(TRAConfiguracionAlmacenPaginas, PROJECTNAME)
# end of class TRAConfiguracionAlmacenPaginas

##code-section module-footer #fill in your manual code here
##/code-section module-footer



