# -*- coding: utf-8 -*-
#
# File: TRAElemento_Internationalization.py
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

 

from AccessControl              import ClassSecurityInfo

from Products.CMFCore           import permissions



from TRAElemento_Constants                 import *
from TRAElemento_Constants_Activity        import *
from TRAElemento_Constants_Configurations  import *
from TRAElemento_Constants_Dates           import *
from TRAElemento_Constants_Encoding        import *
from TRAElemento_Constants_Import          import *
from TRAElemento_Constants_Languages       import *
from TRAElemento_Constants_Logging         import *
from TRAElemento_Constants_Modules         import *
from TRAElemento_Constants_Profiling       import *
from TRAElemento_Constants_Progress        import *
from TRAElemento_Constants_String          import *
from TRAElemento_Constants_StringRequests  import *
from TRAElemento_Constants_Translate       import *
from TRAElemento_Constants_Translation     import *
from TRAElemento_Constants_TypeNames       import *
from TRAElemento_Constants_Views           import *
from TRAElemento_Constants_Vocabularies    import *
from TRAUtils                              import *




    
            
# ########################################################################################################
    
class TRAElemento_Internationalization:
    """Class with responsibility to deal with the localization of internatiolalized strings.
        
    """
    
    security = ClassSecurityInfo()



    


    security.declarePublic( 'fTranslateI18N')
    def fTranslateI18N( self, 
        theI18NDomain, 
        theString, 
        theDefault, 
        theTranslationService=None):
        """Localization: return the translated string from the specific domain into the language preferred by the connected user, or return the supplied default.
        
        """
        
        if not theString:
            return ''

        aI18NDomain = theI18NDomain
        if not aI18NDomain:
            try:
                aI18NDomain = self.getNombreProyecto()
            except:
                None
                
        aI18NDomain = self.fTranslationI18NDomain( theI18NDomain)
        if not aI18NDomain:
            return unicode( theDefault)
                

        
        aTranslationService = theTranslationService
        if not aTranslationService:
            aTranslationService = self.getTranslationServiceTool()
            
        aTranslation = theDefault
        if aTranslationService:
            aTranslation = aTranslationService.utranslate( aI18NDomain, theString, mapping=None, context=self , target_language= None, default=theDefault)            
           
        if not aTranslation:
            aTranslation = theDefault

        if not aTranslation:
            aTranslation = theString

        return aTranslation
        
    
    

    security.declarePublic( 'fTranslateI18NManyIntoDict')
    def fTranslateI18NManyIntoDict( self, 
        theI18NDomainsStringsAndDefaults=[], 
        theResultDict                   =None,
        theTranslationService           =None,):
        """Internationalization: build or update a dictionaty with the translations of all requested strings from the specified domain into the language preferred by the connected user, or return the supplied default.
        
        """
        
        unResultDict = theResultDict
        if ( unResultDict == None):
            unResultDict = { }
                
        if not theI18NDomainsStringsAndDefaults:
            return unResultDict
        
        aTranslationService = theTranslationService
        if not aTranslationService:
            aTranslationService = self.getTranslationServiceTool()
            if not aTranslationService:
                return unResultDict
        
        for aDomainStringsAndDefaults in theI18NDomainsStringsAndDefaults:
            aI18NDomain             = aDomainStringsAndDefaults[ 0] or cI18NDomainDefault
            unasStringsAndDefaults  = aDomainStringsAndDefaults[ 1]
            
            for unaStringAndDefault in unasStringsAndDefaults:
                unaString = unaStringAndDefault[ 0]
                unDefault = unaStringAndDefault[ 1]
                if unaString:
                    aTranslation = u''
                    if aTranslationService:
                        aTranslation = aTranslationService.utranslate( aI18NDomain, unaString, mapping=None, context=self , target_language= None, default=unDefault)            
                    if not aTranslation:
                        aTranslation = self.fAsUnicode( unDefault)
                    unResultDict[ unaString] = aTranslation
                        
        return unResultDict
            
    
    
    
    

    
    security.declarePrivate( 'fTranslationI18NDomain')
    def fTranslationI18NDomain( self, theI18NDomain):

        aI18NDomain = theI18NDomain
        if not aI18NDomain:
            try:
                aI18NDomain = self.getNombreProyecto()
            except:
                None
            if not aI18NDomain:
                aI18NDomain = 'ModelDDvlPlone'
                
        if not aI18NDomain:
            aI18NDomain = "plone"
            
        return aI18NDomain

    
    
    
    
           