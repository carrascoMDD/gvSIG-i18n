# -*- coding: utf-8 -*-
#
# File: TRAElemento_LanguagesUtils.py
#
# Copyright (c) 2008, 2009,2010 by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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




from Products.PloneLanguageTool import availablelanguages as PloneLanguageToolAvailableLanguages


from TRAElemento_Constants              import *



    
            
# ########################################################################################################
    
class TRAElemento_LanguagesUtils:
    """Class with responsibility providing some utilities for languages and language codes.
        
    """
    
    security = ClassSecurityInfo()

    


    security.declarePrivate( 'fLanguageAndCountryAndVariationIdioma')    
    def fLanguageAndCountryAndVariationIdioma( self, theCodigoIdioma):
        """Parse language, country, variation codes.
        
        """
        
        if not theCodigoIdioma:
            return ( '', '', '',)
        
        unasParts = theCodigoIdioma.split( cLanguageSeparatorCountry, 2)
        if not unasParts:
            return ( '', '', '',)

        unCodigoIdioma  = unasParts[ 0]
            
        unCodigoCountry = ''
        if len( unasParts) > 1:
            unCodigoCountry = unasParts[ 1]

        unaVariation = ''
        if len( unasParts) > 2:
            unaVariation = unasParts[ 1]

        return ( unCodigoIdioma, unCodigoCountry, unaVariation, )
        
    
    
    
    
    security.declareProtected( permissions.View, 'fLanguagesNamesAndFlagsPorCodigo')
    def fLanguagesNamesAndFlagsPorCodigo(self,):
        """Globally known languages 
        Key : Language code
        Value: Dictionary with keys: 'english' 'native' and optionally 'flag'
        
        """
        
        aPloneLanguageTool = self.getPloneLanguageTool()
        unosLanguagesPorCodigo = aPloneLanguageTool.getAvailableLanguageInformation()
        
        unosLanguagesPorCodigo = dict( [ [ unosLanguagesPorCodigo_Key, unosLanguagesPorCodigo_Value.copy(),] for unosLanguagesPorCodigo_Key, unosLanguagesPorCodigo_Value in unosLanguagesPorCodigo.items()])
        
        someCountrySpecificLanguagesPorCodigo = PloneLanguageToolAvailableLanguages.getCombined()
        for aCountrySpecificLanguageCode in someCountrySpecificLanguagesPorCodigo.keys():
            if not ( unosLanguagesPorCodigo.has_key( aCountrySpecificLanguageCode)):
                unosLanguagesPorCodigo[ aCountrySpecificLanguageCode] = someCountrySpecificLanguagesPorCodigo[ aCountrySpecificLanguageCode].copy()   
                unosLanguagesPorCodigo[ 'selected'] = False
                
        unCatalogo = self.getCatalogo()
        unosIdiomas = unCatalogo.fObtenerTodosIdiomas()
        
        unPortalURL = self.fPortalURL()
        
        for unIdioma in unosIdiomas:
            unCodigoIdiomaEnGvSIG         = unIdioma.getCodigoIdiomaEnGvSIG()
            unCodigoInternacionalDeIdioma = unIdioma.getCodigoInternacionalDeIdioma()
            aTitle                        = unIdioma.Title()
            aNombreNativoDeIdioma         = unIdioma.getNombreNativoDeIdioma()
            unFlag, unFlagURL             = unIdioma.fFlagAndURL()
            
            unosDatosIdioma = unosLanguagesPorCodigo.get( unCodigoIdiomaEnGvSIG, {})
            
            unosDatosIdioma[ 'english'] = aTitle
            unosDatosIdioma[ 'native']  = aNombreNativoDeIdioma

            if unFlag:
                unosDatosIdioma[ 'flag'] = unFlag
                
                if unFlagURL:
                    unosDatosIdioma[ 'flag_url'] = unFlagURL
            
                
            unosLanguagesPorCodigo[ unCodigoIdiomaEnGvSIG] = unosDatosIdioma
            
        for unCodigoIdioma in unosLanguagesPorCodigo.keys():
            
            unosDatosIdioma = unosLanguagesPorCodigo.get( unCodigoIdioma, {})
            if unosDatosIdioma:
                
                unFlag = unosDatosIdioma.get( 'flag', '')
                
                if not unFlag:
                    unosDatosIdioma[ 'flag']     = cTRAFlagIdiomaDesconocida
                    unFlagURL                    = '%s/%s' % ( unPortalURL, cTRAFlagIdiomaDesconocida,)
                    unosDatosIdioma[ 'flag_url'] = unFlagURL
                else:
                    unFlagURL =  unosDatosIdioma.get( 'flag_url', '')
                    if not unFlagURL:
                        unFlagURL                    = '%s/%s' % ( unPortalURL, unFlag,)
                        unosDatosIdioma[ 'flag_url'] = unFlagURL

        return unosLanguagesPorCodigo.copy()
    
    
    
    
    
    security.declareProtected( permissions.View, 'fLanguagesNamesAndFlagsPorCodigo_AvailableInPlone')
    def fLanguagesNamesAndFlagsPorCodigo_AvailableInPlone(self,):
        
        aPloneLanguageTool = self.getPloneLanguageTool()
        unosLanguagesPorCodigo = aPloneLanguageTool.getAvailableLanguageInformation()
        
        someCountrySpecificLanguagesPorCodigo = PloneLanguageToolAvailableLanguages.getCombined()
        for aCountrySpecificLanguageCode in someCountrySpecificLanguagesPorCodigo.keys():
            if not ( unosLanguagesPorCodigo.has_key( aCountrySpecificLanguageCode)):
                unosLanguagesPorCodigo[ aCountrySpecificLanguageCode] = someCountrySpecificLanguagesPorCodigo[ aCountrySpecificLanguageCode]   
                unosLanguagesPorCodigo[ 'selected'] = False
         
        return unosLanguagesPorCodigo.copy()
    
    
    


    
    
    
    
             
    security.declareProtected( permissions.View, 'fDisplayCountryFlags')
    def fDisplayCountryFlags(self,):
        
        aPloneLanguageTool = self.getPloneLanguageTool()
          
        return ( aPloneLanguageTool.display_flags and True) or False
    
             
    
    
    
 
   
    security.declarePrivate( 'fIdTraduccionDesdeIdCadenaYLenguage')    
    def fIdTraduccionDesdeIdCadenaYLenguage( self, theIdCadena, theCodigoIdioma, thePloneUtilsTool=None):
        if not theIdCadena or not theCodigoIdioma:
            return ''
        
        aIdTraduccion = "%s-%s" % ( theIdCadena, theCodigoIdioma)
        aIdTraduccion= aIdTraduccion.lower()
        aIdTraduccion.replace(" ", "-")
    
        aPloneUtilsTool = thePloneUtilsTool
        if not aPloneUtilsTool:
            aPloneUtilsTool = self.getPloneUtilsToolForNormalizeString()
        if aPloneUtilsTool:
            aIdTraduccion = aPloneUtilsTool.normalizeString( aIdTraduccion)
                
        return aIdTraduccion
   
    
    
    
    
      

 
    
           
     
     

    
    
    

    