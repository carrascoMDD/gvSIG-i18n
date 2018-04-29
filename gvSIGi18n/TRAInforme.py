# -*- coding: utf-8 -*-
#
# File: TRAInforme.py
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

__author__ = """Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
<gvSIGi18n@gvSIG.org>, Model Driven Development sl <gvSIGi18n@ModelDD.org>,
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.gvSIGi18n.TRAArquetipo import TRAArquetipo
from TRAInforme_Operaciones import TRAInforme_Operaciones
from Products.gvSIGi18n.TRAConRegistroActividad import TRAConRegistroActividad
from Products.gvSIGi18n.config import *

# additional imports from tagged value 'import'
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    BooleanField(
        name='esAutoActualizable',
        widget=BooleanField._properties['widget'](
            label="Es Auto-Actualizable",
            label2="Is Auto-Updated",
            description="Si el informe se actualiza automaticamente bajo demanda, pero no mas frecuentemente que cierto intervalo de tiempo.",
            description2="Whether the report is automatically updated upon demand (but not more frequently than a certain time period).",
            label_msgid='gvSIGi18n_TRAInforme_attr_esAutoActualizable_label',
            description_msgid='gvSIGi18n_TRAInforme_attr_esAutoActualizable_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si el informe se actualiza automaticamente bajo demanda, pero no mas frecuentemente que cierto intervalo de tiempo.",
        duplicates="0",
        label2="Is Auto-Updated",
        ea_localid="857",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Whether the report is automatically updated upon demand (but not more frequently than a certain time period).",
        ea_guid="{6175A4D5-254D-4ef2-ADE5-E9AFC307B599}",
        scale="0",
        default="False",
        label="Es Auto-Actualizable",
        length="0",
        containment="Not Specified",
        position="1",
        owner_class_name="TRAInforme"
    ),

    #Inactivo
    StringField(
        name='estadoProceso',
        widget=SelectionWidget(
            label="Estado del Proceso",
            label2="Process State",
            description="""Inactivo
            El estado del proceso de importacion, como activo o inactivo.""",
            description2="Import process state, as active or inactive.",
            label_msgid='gvSIGi18n_TRAInforme_attr_estadoProceso_label',
            description_msgid='gvSIGi18n_TRAInforme_attr_estadoProceso_help',
            i18n_domain='gvSIGi18n',
        ),
        description="""Inactivo
        El estado del proceso de importacion, como activo o inactivo.""",
        vocabulary=['Inactivo','Activo', ],
        duplicates="0",
        vocabulary_msgids=['gvSIGi18n_TRAInforme_attr_estadoProceso_option_Inactivo', 'gvSIGi18n_TRAInforme_attr_estadoProceso_option_Activo'],
        label2="Process State",
        ea_localid="771",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Import process state, as active or inactive.",
        ea_guid="{548B9F5A-DEA3-4daa-82A4-FA62B7523978}",
        vocabulary2=['Inactive', 'Active', ],
        read_only="True",
        scale="0",
        label="Estado del Proceso",
        length="0",
        containment="Not Specified",
        position="3",
        owner_class_name="TRAInforme"
    ),

    BooleanField(
        name='haComenzado',
        widget=BooleanField._properties['widget'](
            label="Comenzo a ejecutar",
            label2="Begun execution",
            description="Si el proceso de importacion ha comenzado alguna vez a ejecutarse.",
            description2="Whether the import process has ever started to execute.",
            label_msgid='gvSIGi18n_TRAInforme_attr_haComenzado_label',
            description_msgid='gvSIGi18n_TRAInforme_attr_haComenzado_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si el proceso de importacion ha comenzado alguna vez a ejecutarse.",
        duplicates="0",
        label2="Begun execution",
        ea_localid="778",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Whether the import process has ever started to execute.",
        ea_guid="{C86A43EB-2E89-4e09-96A6-10557B82BB2F}",
        read_only="True",
        scale="0",
        default="False",
        label="Comenzo a ejecutar",
        length="0",
        containment="Not Specified",
        position="4",
        owner_class_name="TRAInforme"
    ),

    StringField(
        name='usuarioInformador',
        widget=StringWidget(
            label="Usuario Informador",
            label2="Reporting User",
            description="Usuario que ha solicitado creado el Informe.",
            description2="User who requested the ellaboration of the report.",
            label_msgid='gvSIGi18n_TRAInforme_attr_usuarioInformador_label',
            description_msgid='gvSIGi18n_TRAInforme_attr_usuarioInformador_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Usuario que ha solicitado creado el Informe.",
        duplicates="0",
        label2="Reporting User",
        ea_localid="782",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="User who requested the ellaboration of the report.",
        ea_guid="{8BD63B05-0F14-49b3-80A1-0222C34E3C8E}",
        read_only="True",
        scale="0",
        label="Usuario Informador",
        length="0",
        containment="Not Specified",
        position="6",
        owner_class_name="TRAInforme"
    ),

    BooleanField(
        name='haCompletadoConExito',
        widget=BooleanField._properties['widget'](
            label="Exito?",
            label2="Success?",
            description="Si el proceso de importacion ha completado exitosamente su ejecucion.",
            description2="Whether the import process has sucessfully completed execution.",
            label_msgid='gvSIGi18n_TRAInforme_attr_haCompletadoConExito_label',
            description_msgid='gvSIGi18n_TRAInforme_attr_haCompletadoConExito_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si el proceso de importacion ha completado exitosamente su ejecucion.",
        duplicates="0",
        label2="Success?",
        ea_localid="785",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Whether the import process has sucessfully completed execution.",
        ea_guid="{CA62E5F4-34EB-4d25-918A-DB1029ABAD35}",
        read_only="True",
        scale="0",
        default="False",
        label="Exito?",
        length="0",
        containment="Not Specified",
        position="5",
        owner_class_name="TRAInforme"
    ),

    DateTimeField(
        name='fechaComienzoProceso',
        widget=CalendarWidget(
            label="Fecha y Hora de Comienzo",
            label2="Startup Date and time",
            description="Fecha y hora en que se comenzo a elaborar el informe de estado.",
            description2="Date and time when the status report ellaboration started.",
            label_msgid='gvSIGi18n_TRAInforme_attr_fechaComienzoProceso_label',
            description_msgid='gvSIGi18n_TRAInforme_attr_fechaComienzoProceso_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Fecha y hora en que se comenzo a elaborar el informe de estado.",
        duplicates="0",
        label2="Startup Date and time",
        ea_localid="773",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Date and time when the status report ellaboration started.",
        ea_guid="{0EC44BD8-E02D-4521-93F1-36C0FB5F0872}",
        read_only="True",
        scale="0",
        label="Fecha y Hora de Comienzo",
        length="0",
        containment="Not Specified",
        position="7",
        owner_class_name="TRAInforme"
    ),

    DateTimeField(
        name='fechaFinProceso',
        widget=CalendarWidget(
            label="Fecha y Hora de Fin",
            label2="End Date and Time",
            description="Fecha y hora en que termino la elaboracion del informe de estado.",
            description2="Date and Time when the ellaboration of the status report was terminated.",
            label_msgid='gvSIGi18n_TRAInforme_attr_fechaFinProceso_label',
            description_msgid='gvSIGi18n_TRAInforme_attr_fechaFinProceso_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Fecha y hora en que termino la elaboracion del informe de estado.",
        duplicates="0",
        label2="End Date and Time",
        ea_localid="774",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Date and Time when the ellaboration of the status report was terminated.",
        ea_guid="{7BD0FCAF-EBFB-4e98-A55C-9EB75FACAA94}",
        read_only="True",
        scale="0",
        label="Fecha y Hora de Fin",
        length="0",
        containment="Not Specified",
        position="8",
        owner_class_name="TRAInforme"
    ),

    TextField(
        name='informeExcepcion',
        widget=TextAreaWidget(
            label="Informe de Excepcion",
            label2="Exception report",
            description="Cuando la elaboracion del informe de estado finaliza con una condicion de error, contiene el informe del error de la aplicacion.",
            description2="When the ellaboration of the status report terminates with an error, contains the applicacion exception report.",
            label_msgid='gvSIGi18n_TRAInforme_attr_informeExcepcion_label',
            description_msgid='gvSIGi18n_TRAInforme_attr_informeExcepcion_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Cuando la elaboracion del informe de estado finaliza con una condicion de error, contiene el informe del error de la aplicacion.",
        duplicates="0",
        label2="Exception report",
        ea_localid="772",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="When the ellaboration of the status report terminates with an error, contains the applicacion exception report.",
        ea_guid="{4CE08483-728C-4fe1-98A5-C6CF6FF8DD28}",
        read_only="True",
        scale="0",
        label="Informe de Excepcion",
        length="0",
        containment="Not Specified",
        position="9",
        owner_class_name="TRAInforme"
    ),

    TextField(
        name='informeIdiomas',
        widget=TextAreaWidget(
            label="Informe por Idiomas",
            label2="Languages Report",
            description="Informe del estado de traduccion por idiomas.",
            description2="Report or the translation status, summarized by languages.",
            label_msgid='gvSIGi18n_TRAInforme_attr_informeIdiomas_label',
            description_msgid='gvSIGi18n_TRAInforme_attr_informeIdiomas_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Informe del estado de traduccion por idiomas.",
        duplicates="0",
        label2="Languages Report",
        ea_localid="779",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Report or the translation status, summarized by languages.",
        ea_guid="{13808998-877C-4cb2-923E-77C93CEEB9EF}",
        read_only="True",
        scale="0",
        exclude_from_views="[ 'Textual',   'General', ]",
        label="Informe por Idiomas",
        length="0",
        containment="Not Specified",
        position="12",
        owner_class_name="TRAInforme",
        custom_presentation_view="TRAInformeIdiomas_i18n_view"
    ),

    TextField(
        name='informeExcepcionIdiomas',
        widget=TextAreaWidget(
            label="Excepcion en Informe Idiomas",
            label2="Exception report",
            description="Cuando la elaboracion del informe de estado por idiomas finaliza con una condicion de error, contiene el informe del error de la aplicacion.",
            description2="When the ellaboration of the Languages status report terminates with an error, contains the applicacion exception report.",
            label_msgid='gvSIGi18n_TRAInforme_attr_informeExcepcionIdiomas_label',
            description_msgid='gvSIGi18n_TRAInforme_attr_informeExcepcionIdiomas_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Cuando la elaboracion del informe de estado por idiomas finaliza con una condicion de error, contiene el informe del error de la aplicacion.",
        duplicates="0",
        label2="Exception report",
        ea_localid="1460",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="When the ellaboration of the Languages status report terminates with an error, contains the applicacion exception report.",
        ea_guid="{B0CD5D6A-FA31-43f0-B518-21FE7E9D268E}",
        read_only="True",
        scale="0",
        label="Excepcion en Informe Idiomas",
        length="0",
        containment="Not Specified",
        position="11",
        owner_class_name="TRAInforme"
    ),

    TextField(
        name='informeModulos',
        widget=TextAreaWidget(
            label="Informe por Modulos e Idiomas",
            label2="Modules and Languages Report",
            description="Informe del estado de traduccion por modulos y detallado por  idiomas.",
            description2="Report or the translation status, summarized by modules and detailed by languages.",
            label_msgid='gvSIGi18n_TRAInforme_attr_informeModulos_label',
            description_msgid='gvSIGi18n_TRAInforme_attr_informeModulos_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Informe del estado de traduccion por modulos y detallado por  idiomas.",
        duplicates="0",
        label2="Modules and Languages Report",
        ea_localid="806",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="Report or the translation status, summarized by modules and detailed by languages.",
        ea_guid="{F3179FE4-09FD-4ecb-929A-AE8CD4B5D418}",
        read_only="True",
        scale="0",
        exclude_from_views="[ 'Textual',   'General', ]",
        label="Informe por Modulos e Idiomas",
        length="0",
        containment="Not Specified",
        position="13",
        owner_class_name="TRAInforme",
        custom_presentation_view="TRAInformeModulos_i18n_view"
    ),

    TextField(
        name='informeExcepcionModulos',
        widget=TextAreaWidget(
            label="Excepcion en Informe por Modulos",
            label2="Exception report",
            description="Cuando la elaboracion del informe de estado por modulos finaliza con una condicion de error, contiene el informe del error de la aplicacion.",
            description2="When the ellaboration of the Modules status report terminates with an error, contains the applicacion exception report.",
            label_msgid='gvSIGi18n_TRAInforme_attr_informeExcepcionModulos_label',
            description_msgid='gvSIGi18n_TRAInforme_attr_informeExcepcionModulos_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Cuando la elaboracion del informe de estado por modulos finaliza con una condicion de error, contiene el informe del error de la aplicacion.",
        duplicates="0",
        label2="Exception report",
        ea_localid="1461",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="When the ellaboration of the Modules status report terminates with an error, contains the applicacion exception report.",
        ea_guid="{068E1D59-A5B9-4a5c-89DE-4DE7FCB02B9B}",
        read_only="True",
        scale="0",
        label="Excepcion en Informe por Modulos",
        length="0",
        containment="Not Specified",
        position="10",
        owner_class_name="TRAInforme"
    ),

    IntegerField(
        name='minimoIntervaloActualizacionEnMinutos',
        widget=IntegerField._properties['widget'](
            label="Intervalo minimo de actualizacion en Minutos",
            label2="Minimum Update Interval in Minutes",
            description="Si es Auto-Actualizable, es el Intervalo minimo de tiempo en minutos a esperar antes de actualizar automaticamente el informe. Si el valor es 0, el informe se actualizara en todas las solilcitudes de los usuarios, posiblemente sobrecargando el eistema.",
            description2="If the Report is set to be Auto-Updated, Minimum Time interval in minutes to wait before automatically updating the report. If 0, the report will be updated upon demand at every user request, possibly over-loading the system.",
            label_msgid='gvSIGi18n_TRAInforme_attr_minimoIntervaloActualizacionEnMinutos_label',
            description_msgid='gvSIGi18n_TRAInforme_attr_minimoIntervaloActualizacionEnMinutos_help',
            i18n_domain='gvSIGi18n',
        ),
        description="Si es Auto-Actualizable, es el Intervalo minimo de tiempo en minutos a esperar antes de actualizar automaticamente el informe. Si el valor es 0, el informe se actualizara en todas las solilcitudes de los usuarios, posiblemente sobrecargando el eistema.",
        duplicates="0",
        label2="Minimum Update Interval in Minutes",
        ea_localid="877",
        derived="0",
        precision=0,
        collection="false",
        styleex="volatile=0;",
        description2="If the Report is set to be Auto-Updated, Minimum Time interval in minutes to wait before automatically updating the report. If 0, the report will be updated upon demand at every user request, possibly over-loading the system.",
        ea_guid="{531CA267-DB73-4576-904E-6801AA70911E}",
        scale="0",
        default="30",
        label="Intervalo minimo de actualizacion en Minutos",
        length="0",
        containment="Not Specified",
        position="2",
        owner_class_name="TRAInforme"
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TRAInforme_schema = OrderedBaseFolderSchema.copy() + \
    getattr(TRAArquetipo, 'schema', Schema(())).copy() + \
    getattr(TRAInforme_Operaciones, 'schema', Schema(())).copy() + \
    getattr(TRAConRegistroActividad, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAInforme(OrderedBaseFolder, TRAArquetipo, TRAInforme_Operaciones, TRAConRegistroActividad):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(OrderedBaseFolder,'__implements__',()),) + (getattr(TRAArquetipo,'__implements__',()),) + (getattr(TRAInforme_Operaciones,'__implements__',()),) + (getattr(TRAConRegistroActividad,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'Informe de Estado'

    meta_type = 'TRAInforme'
    portal_type = 'TRAInforme'


    creation_date_field = 'fechaCreacion'
    creation_user_field = 'usuarioCreador'
    modification_date_field = 'fechaModificacion'
    modification_user_field = 'usuarioModificador'
    deletion_date_field = 'fechaEliminacion'
    deletion_user_field = 'usuarioEliminador'
    is_inactive_field = 'estaInactivo'
    change_counter_field = 'contadorCambios'
    change_log_field = 'registroDeCambios'
    use_folder_tabs = 0

    allowed_content_types = [] + list(getattr(TRAArquetipo, 'allowed_content_types', [])) + list(getattr(TRAInforme_Operaciones, 'allowed_content_types', [])) + list(getattr(TRAConRegistroActividad, 'allowed_content_types', []))
    filter_content_types = 1
    global_allow = 0
    content_icon = 'trainforme.gif'
    immediate_view = 'Tabular'
    default_view = 'Tabular'
    suppl_views = ['Tabular',]
    typeDescription = "Informe del estado en un momento determinado de Traducciones a Idiomas."
    typeDescMsgId =  'gvSIGi18n_TRAInforme_help'
    archetype_name2 = 'Status Report'
    typeDescription2 = '''Status at the Report time, of Translations to  Languages.'''
    archetype_name_msgid = 'gvSIGi18n_TRAInforme_label'
    factory_methods = None
    factory_enablers = None
    allow_discussion = False


    actions =  (


       {'action': "string:$object_url/Editar",
        'category': "object",
        'id': 'edit',
        'name': 'Edit',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fAllowWrite()"""
       },


       {'action': "string:${object_url}/TRAElaborarInforme_action",
        'category': "object_buttons",
        'id': 'informar',
        'name': 'Build Report',
        'permissions': ("Modify portal content",),
        'condition': """python:object.fAllowWrite() and ( ( True or not object.getHaComenzado()) or object.getEsAutoActualizable())"""
       },


       {'action': "string:${object_url}/Tabular",
        'category': "object",
        'id': 'view',
        'name': 'View',
        'permissions': ("View",),
        'condition': """python:1"""
       },


       {'action': "string:${object_url}/sharing",
        'category': "object",
        'id': 'local_roles',
        'name': 'Sharing',
        'permissions': ("Manage properties",),
        'condition': """python:0"""
       },


       {'action': "string:${object_url}/folder_listing",
        'category': "folder",
        'id': 'folderlisting',
        'name': 'Folder Listing',
        'permissions': ("View",),
        'condition': """python:0"""
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
        'condition': """python:1"""
       },


       {'action': "string:$object_url/content_status_history",
        'category': "object",
        'id': 'content_status_history',
        'name': 'State',
        'permissions': ("View",),
        'condition': """python:0"""
       },


    )

    _at_rename_after_creation = True

    schema = TRAInforme_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('manage_afterAdd')
    def manage_afterAdd(self,item,container):
        """
        """
        
        return TRAArquetipo.manage_afterAdd( self, item, container)

    security.declarePublic('manage_beforeDelete')
    def manage_beforeDelete(self,item,container):
        """
        """
        
        return TRAArquetipo.manage_beforeDelete( self, item, container)

    security.declarePublic('manage_pasteObjects')
    def manage_pasteObjects(self,cb_copy_data,REQUEST):
        """
        """
        
        return self.pHandle_manage_pasteObjects( cb_copy_data, REQUEST)

    security.declarePublic('cb_isMoveable')
    def cb_isMoveable(self):
        """
        """
        
        return False

    security.declarePublic('cb_isCopyable')
    def cb_isCopyable(self):
        """
        """
        
        return False

    security.declarePublic('displayContentsTab')
    def displayContentsTab(self):
        """
        """
        
        return False
def modify_fti(fti):
    # Hide unnecessary tabs (usability enhancement)
    for a in fti['actions']:
        if a['id'] in ['metadata', 'sharing', 'folderContents']:
            a['visible'] = 0
    return fti

registerType(TRAInforme, PROJECTNAME)
# end of class TRAInforme

##code-section module-footer #fill in your manual code here
##/code-section module-footer



