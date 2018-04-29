# -*- coding: utf-8 -*-
#
# File: TRAElemento_Credits.py
#
# Copyright (c) 2008, 2009 by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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



from AccessControl              import ClassSecurityInfo

from Products.CMFCore.utils     import getToolByName


cMustLocalizeSentinel = object()



gTRACredits_Constant = {
    'gvSIGi18n_credits_AuthorCITAbbreviated_PropertyValue': u"GVA/CIT",
    'gvSIGi18n_credits_ProjectTitle_PropertyValue': u"gvSIG-i18n",
    'gvSIGi18n_credits_Copyright_PropertyValue': u"(C) 2008, 2009 Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana",
    'gvSIGi18n_credits_License_PropertyValue': u"GNU General Public License (GPL)",
    'gvSIGi18n_credits_License_URL_PropertyValue': u"www.fsf.org/licensing/licenses/gpl.html",
    'gvSIGi18n_credits_License_FreeSoftwareFoundation_URL_PropertyValue': u"Free Software Foundation, Inc.",
    'gvSIGi18n_credits_License_FreeSoftwareFoundation_PropertyValue': u"Free Software Foundation, Inc.",
    'gvSIGi18n_credits_License_FreeSoftwareFoundation_URL_PropertyValue': u"www.fsf.org",
    'gvSIGi18n_credits_Author_Conselleria_Institucion_PropertyValue': u"Regional Ministry at Comunidad Valenciana in Spain, Europe",
    'gvSIGi18n_credits_Author_Conselleria_PropertyValue': u"Conselleria de Infraestructuras y Transporte de la Generalitat Valenciana",
    'gvSIGi18n_credits_Author_Conselleria_URL_PropertyValue': u"www.cit.gva.es",
    'gvSIGi18n_credits_Author_Conselleria_Logo_PropertyValue': u"CIT.gif",
    'gvSIGi18n_credits_Author_ModelDrivenDevelopmentSL_PropertyValue': u"Model Driven Development, sl",
    'gvSIGi18n_credits_Author_ModelDrivenDevelopmentSL_URL_PropertyValue': u"www.ModelDD.org",
    'gvSIGi18n_credits_Author_ModelDrivenDevelopmentSL_Logo_PropertyValue': u"ModelDrivenDevelopmenSL.gif",
    'gvSIGi18n_credits_Author_AntonioCarrascoValero_PropertyValue': u"Antonio Carrasco Valero",
    'gvSIGi18n_credits_Author_AntonioCarrascoValero_URL_PropertyValue': u"gvsig.org/web/author/tcarrasco",
    'gvSIGi18n_credits_Author_AntonioCarrascoValero_Photo_PropertyValue': u"ACV.jpg",
    'gvSIGi18n_credits_SponsorProjectTitle_PropertyValue': u"gvSIG project by Conselleria de Infraestructuras y Transporte de la Generalitat Valenciana",
    'gvSIGi18n_credits_SponsorProjectTitle_URL_PropertyValue': u"gvSIG.org",
    'gvSIGi18n_credits_SponsorProjectTitle_Logo_PropertyValue': u"gvSIG.gif",
    'gvSIGi18n_credits_Standards_MDA_PropertyValue': u"Model Driven Architecture (MDA)",    
    'gvSIGi18n_credits_Standards_MDA_URL_PropertyValue': u"www.omg.org/mda",    
    'gvSIGi18n_credits_Standards_OMG_PropertyValue': u"Object Management Group, inc",    
    'gvSIGi18n_credits_Standards_OMG_URL_PropertyValue': u"www.omg.org",    
    'gvSIGi18n_credits_RequirementsCoordination_Business_Name':u"Mario Carrera",
    'gvSIGi18n_credits_RequirementsCoordination_Business_URL':u"gvsig.org/web/author/mcarrera",
    'gvSIGi18n_credits_RequirementsCoordination_Organization_Name':u"Manuel Madrid",
    'gvSIGi18n_credits_RequirementsCoordination_Organization_URL':u"gvsig.org/web/author/mmadrid",
    'gvSIGi18n_credits_RequirementsCoordination_Platform_Name':u"Joaquin del Cerro",
    'gvSIGi18n_credits_RequirementsCoordination_Platform_URL':u"gvsig.org/web/author/jjdelcerro",
    'gvSIGi18n_credits_RequirementsCoordination_Administration_Name':u"Victor Acevedo",
    'gvSIGi18n_credits_RequirementsCoordination_Administration_URL':u"gvsig.org/web/author/vacevedo",
    'gvSIGi18n_credits_SponsorProjectTitle_Jefe_Name':u"Martin Garcia",
    'gvSIGi18n_credits_SponsorProjectTitle_CoordinadorGeneral_Name':u"Gabriel Carrion",
    'gvSIGi18n_credits_SponsorProjectTitle_CoordinadorTecnico_Name':u"",
    'gvSIGi18n_credits_Standards_UML_PropertyValue': u"Unified Modeling Language (UML)",   
    'gvSIGi18n_credits_Standards_UML_URL_PropertyValue':u"www.omg.org/technology/documents/modeling_spec_catalog.htm#UML",
    'gvSIGi18n_credits_Standards_MOF_PropertyValue': u"Meta Object Facility (MOF)",    
    'gvSIGi18n_credits_Standards_MOF_URL_PropertyValue':u"www.omg.org/technology/documents/modeling_spec_catalog.htm#MOF",
    'gvSIGi18n_credits_Standards_XMI_PropertyValue': u"XML Metadata Interchange (XMI)",    
    'gvSIGi18n_credits_Standards_XMI_URL_PropertyValue':u"www.omg.org/technology/documents/modeling_spec_catalog.htm#XMI",
    'gvSIGi18n_credits_Platform_Zope_PropertyValue': u"Zope v2.9",
    'gvSIGi18n_credits_Platform_Zope_URL_PropertyValue': u"www.zope.org",
    'gvSIGi18n_credits_Platform_Plone_PropertyValue': u"Plone v2.5",
    'gvSIGi18n_credits_Platform_Plone_URL_PropertyValue': u"www.plone.org",
    'gvSIGi18n_credits_Platform_Python_PropertyValue': u"Python v2.4",
    'gvSIGi18n_credits_Platform_Python_URL_PropertyValue': u"www.python.org",
    'gvSIGi18n_credits_Standards_GNUgettextPO_PropertyValue': u"GNU gettext PO",
    'gvSIGi18n_credits_Standards_GNUgettextPO_URL_PropertyValue': u"www.gnu.org/software/gettext/",
    'gvSIGi18n_credits_Standards_JavaProperties_PropertyValue': u"Java .properties",
    'gvSIGi18n_credits_Standards_JavaProperties_URL_PropertyValue': u"www.javasoft.com",
    
    
}


gTRACredits_I18N = {
    'gvSIGi18n_credits_por': 'by-',
    'gvSIGi18n_credits_Title': u"Credits-",
    'gvSIGi18n_credits_ProjectTitle_PropertyName': "Project-",
    'gvSIGi18n_credits_ProjectTitle_Description_PropertyValue': "Collaborative application for the translation of user interface texts in the gvSIG application, its extensions, and collaborative applications used by gvSIG, like this very same one.-",
    'gvSIGi18n_credits_Copyright_PropertyName': u"Copyright-",
    'gvSIGi18n_credits_License_PropertyName': u"License-",
    'gvSIGi18n_credits_Autores_PropertyName': u"Authors-",
    'gvSIGi18n_credits_Author_ModelDrivenDevelopmentSL_Empresa_PropertyValue': u"company-",
    'gvSIGi18n_credits_Author_AntonioCarrascoValero_Desarrollador_PropertyValue': u"developer-",
    'gvSIGi18n_credits_SponsorProjectTitle_PropertyName': u"Sponsor and Director-",
    'gvSIGi18n_credits_SponsorProjectTitle_Description_PropertyValue': u"gvSIG is a software application for the management of geospatial information. Released as Free Libre Open Source Software (FLOSS). Developed as a dektop application programmed in the Java language. Available in the free libre open source software operating system GNU/Linux, and the proprietary Apple Macintosh(R) and Microsoft Windows(R). Localized to many languages and countries. gvSIG now facilitates the availability for even more languages and countries, with this gvSIGtraducciones application for collaborative translations of user interface strings.-",
    'gvSIGi18n_credits_Standards_PropertyName': u"Standards-",
    'gvSIGi18n_credits_Warranty_PropertyName': u"Warranty-",
    'gvSIGi18n_credits_Warranty_PropertyValue':u"This program is distributed in the hope that it will be useful, but without any warraty; without even the implied warranty of merchantability or fitness for a particular purpose. See the GNU General Public License (GPL) for more details.-",
    'gvSIGi18n_credits_Standards_Intro_PropertyName':u"Developed following the recommendations in the-",
    'gvSIGi18n_credits_RequirementsCoordination_PropertyName':u"Requirements Coordination-",
    'gvSIGi18n_credits_RequirementsCoordination_Business_Title':u"Translation Domain Requirements-",
    'gvSIGi18n_credits_RequirementsCoordination_Organization_Title':u"Organization Requirements-",
    'gvSIGi18n_credits_RequirementsCoordination_Platform_Title':u"Platform Requirements-",
    'gvSIGi18n_credits_RequirementsCoordination_Administration_Title':u"Administration Requirements-",
    'gvSIGi18n_credits_SponsorProjectTitle_Jefe_Title':u"Chief Organization and Information Officer at CIT-",
    'gvSIGi18n_credits_SponsorProjectTitle_CoordinadorGeneral_Title':"gvSIG General Coordinator-",
    'gvSIGi18n_credits_SponsorProjectTitle_CoordinadorTecnico_Title': u"gvSIG Technical Coordinator-",
    'gvSIGi18n_credits_DevelopedBy_PropertyName': u"Developed by-",
    'gvSIGi18n_credits_PorLa': u"by the-",
    'gvSIGi18n_credits_por':   u"by-",
    'gvSIGi18n_credits_Platform_PropertyName': u"Platform-",
    'gvSIGi18n_credits_Standards_Interchange_Intro_PropertyName': u"Translations interchange according to-",
    'gvSIGi18n_credits_Components_PropertyName': u"Components-",
    'gvSIGi18n_credits_Components_ThirdParty_PropertyName': u"Third party-",
    'gvSIGi18n_credits_Components_DevelopedBy_PropertyName': u"Developed by-",
    'gvSIGi18n_credits_Components_Installed_PropertyName': u"Installed-",
    'gvSIGi18n_credits_Components_NotInstalled_PropertyName': u"Not Installed-",
    'gvSIGi18n_credits_Components_Missing_PropertyName': u"Missing-",
    'gvSIGi18n_credits_Components_Error_PropertyName':  u"Failed-",
    'gvSIGi18n_credits_Components_Optional_PropertyName': u"Optional-",
    'gvSIGi18n_credits_Platform_Intro_PropertyName': u"Application Server, Content Management System and Programming Language",
}


class TRAElemento_Credits:
    """
    """
    security = ClassSecurityInfo()

    

    security.declarePublic( 'fCredits')
    def fCredits( self):
        
        aCreditsDict = gTRACredits_I18N.copy()
        
        aTranslationService = getToolByName( self, 'translation_service', None)   
        if not aTranslationService:
            aCreditsDict.update( gTRACredits_Constant)
            return aCreditsDict
        
        someKeys = aCreditsDict.keys()
        for aKey in someKeys:
            aValue = aCreditsDict.get( aKey, u'')
            aTranslatedValue = self.fTranslateI18N( 'gvSIGi18n_credits', aKey, aValue, aTranslationService)
            aCreditsDict[ aKey] = aTranslatedValue
        
        aCreditsDict.update( gTRACredits_Constant)
        return aCreditsDict




