# -*- coding: utf-8 -*-
#
# File: TRAIdioma_Operaciones.py
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

__author__ = """Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana <gvSIGi18n@gvSIG.org>, 
Model Driven Development sl <gvSIGi18n@ModelDD.org>, 
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo

##code-section module-header #fill in your manual code here


import logging

import transaction

from Products.Archetypes.public import DisplayList

from Products.CMFCore           import permissions



from TRAElemento_Constants          import *

from TRAElemento                    import TRAElemento 

from TRAImportarExportar_Constants  import cEncodingSeparatorSentinelName 




##/code-section module-header


##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema


##code-section after-schema #fill in your manual code here

# ACV20090519 removed
# cLogTimeProfileCrearTraduccionesQueFaltanEnIdioma = True


##/code-section after-schema

class TRAIdioma_Operaciones:
    """
    """
    security = ClassSecurityInfo()



    ##code-section class-header #fill in your manual code here
        
    security.declareProtected( permissions.View, 'getCatalogo')
    def getCatalogo( self):
        return self.getContenedorContenedor()
        

    

                   


        
        
    # #############################################################
    # Prefered Encodings for known languages 
    # A vocabulary for User Interface
    # #############################################################


    security.declareProtected( permissions.View, 'fEncodingsForLanguageVocabulary')
    def fEncodingsForLanguageVocabulary(self,):
        
        unDisplayList = DisplayList()
        
        unCodigoIdioma = self.getCodigoIdiomaEnGvSIG()
        if not unCodigoIdioma:
            return unDisplayList
        
        unosEncodings = self.fEncodingsForLanguage( unCodigoIdioma)

        for unEncoding in unosEncodings:
            unEncodingName = unEncoding[ 0]
            unEncodingTitle = unEncoding[ 1]
            unEncodingAliases = unEncoding[ 2]
            if not ( unEncodingName == cEncodingSeparatorSentinelName):
                unEncodingNamePart = self.fAsUnicode( unEncodingName)
                unTitlePart        = self.fAsUnicode( unEncodingTitle)
                unosAliasesPart = u', '.join( [ self.fAsUnicode( unEncodingAlias) for unEncodingAlias in unEncodingAliases])
                
                unEncodingDisplay  = unEncodingNamePart
                
                if unTitlePart and not ( unTitlePart == unEncodingNamePart):
                    unEncodingDisplay = u'%s %s' % ( unEncodingDisplay, unTitlePart,)
                    
                if unosAliasesPart and not ( unosAliasesPart == unEncodingNamePart) and not ( unosAliasesPart == unTitlePart):
                    unEncodingDisplay = u'%s %s' % ( unEncodingDisplay, unosAliasesPart,)

                unDisplayList.add( unEncodingNamePart, unEncodingDisplay)     
                
        return unDisplayList
    
    
    
    
    
    security.declareProtected( permissions.View, 'fDisplayTitleAsUnicode')
    def fDisplayTitleAsUnicode(self,):
        
        aCodigoIdioma                   = self.getCodigoIdiomaEnGvSIG()
        aCodigoInternacionalDeIdioma    = self.getCodigoInternacionalDeIdioma()
        
        aCodePart = u''
        if ( not aCodigoInternacionalDeIdioma) or ( aCodigoIdioma == aCodigoInternacionalDeIdioma):
            aCodePart =  self.fAsUnicode( aCodigoIdioma)
        else:
            aCodePart =  u'%s %s'  % ( self.fAsUnicode( aCodigoIdioma),  self.fAsUnicode( aCodigoInternacionalDeIdioma),)
            
        aTitle = self.Title()
        aNombreNativoDeIdioma = self.getNombreNativoDeIdioma()
        
        aTitlePart = u''
        if ( not aNombreNativoDeIdioma) or (aTitle  == aNombreNativoDeIdioma):
            aTitlePart = self.fAsUnicode( aTitle )
        else:
            aTitlePart = u'%s %s'  % (   self.fAsUnicode( aTitle ),  self.fAsUnicode( aNombreNativoDeIdioma),)    

        if aTitlePart == aCodePart:
            aTitlePart = ''
            
        aDisplayTitle = u''
        if not aTitlePart or ( aTitlePart == aCodePart):
            aDisplayTitle = aCodePart
        else:
            aDisplayTitle = u'%s %s' % ( aCodePart, aTitlePart,)

        return aDisplayTitle
    
     


  
    security.declareProtected( permissions.View, 'fIdiomasReferenciaVocabulary')
    def fIdiomasReferenciaVocabulary(self,):
        """Return a vocabulary for User Interface with the Languages that can be a reference for this language .
        
        """
        unDisplayList = DisplayList()
        
        unCatalogo = self.getCatalogo()
        if not unCatalogo:
            return unDisplayList
        
        unDisplayList.add( '', self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_sinIdiomaReferencia', 'No reference language-'))
        
        unosCodigosYDisplayNames = unCatalogo.fTodosIdiomasCodesAndDisplayNames()
        if not unosCodigosYDisplayNames:
            return unDisplayList
        
        unCodigoIdioma = self.getCodigoIdiomaEnGvSIG()
        
        for unCodigoIdiomaReferencia, unDisplayName in unosCodigosYDisplayNames:
            if unCodigoIdiomaReferencia and not ( unCodigoIdiomaReferencia == unCodigoIdioma):
                unDisplayList.add( 
                    unCodigoIdiomaReferencia,
                    unDisplayName,
                )     
                
        return unDisplayList
    
             
    
# ####################################
#  Complete initialization after creation
#
        
     
    
    security.declarePrivate('pHandle_manage_afterAdd')
    def pHandle_manage_afterAdd(self, theItem, theContainer):   
        
        TRAElemento.manage_afterAdd(  self, theItem, theContainer)
        
        if self.getCodigoIdiomaEnGvSIG():
            unInforme = self.getCatalogo().fLazyCrearCatalogosEIndicesParaIdioma( self)
        
        # Creation of TRATRaduccion for the TRAIdioma 
        # will be commanded by the caller, not here
        # as we don want that to happen at every instantiation.
        # I.e. Import process
        
        return self
    
         
    
  
    
    # ####################################
    #  Complete with pending translations
    #
        
    
    #security.declarePrivate('pCrearTraduccionesQueFaltanEnIdioma')
    #def pCrearTraduccionesQueFaltanEnIdioma(self, theParentExecutionRecord=None):   
        ## ACV 20090323 TODO
        #self.OJO_a_ver_quien_hace_esto()
        
        #unExecutionRecord = self.fStartExecution( 'method',  'pCrearTraduccionesQueFaltanEnIdioma', theParentExecutionRecord, False)  

        #unNumeroCreaciones = 0
        
        #try:
            #unCatalogoRaiz  = self.getCatalogo()
            #unCodigoIdioma  = self.getCodigoIdiomaEnGvSIG()
            #unMemberId      = self.fGetMemberId()
            #aPloneUtilsTool = self.getPloneUtilsToolForNormalizeString()
            
            #unCatalogBusquedaTraducciones = unCatalogoRaiz.fCatalogBusquedaTraduccionesParaIdioma( self)
            #unCatalogFiltroTraducciones   = unCatalogoRaiz.fCatalogFiltroTraduccionesParaIdioma(   self)
            #unCatalogTextoTraducciones    = unCatalogoRaiz.fCatalogTextoTraduccionesParaIdioma(    self)
                    
            #unasCadenas = self.getCatalogo().fObtenerTodasCadenas()
            
            #for unaCadena in unasCadenas:
                #unaConditionYTraduccion = unaCadena.fCrearTraduccionSiFalta( unCodigoIdioma, unMemberId, aPloneUtilsTool, unCatalogBusquedaTraducciones, unCatalogFiltroTraducciones, unCatalogTextoTraducciones)
                #if  unaConditionYTraduccion and ( unaConditionYTraduccion[ 0] =='created'):
                    #unNumeroCreaciones += 1    
                
            #return self
        
        #finally:
            #if unNumeroCreaciones:
                #transaction.commit()
                #logging.getLogger( 'gvSIGi18n').info( 'pCrearTraduccionesQueFaltanEnIdioma COMMIT added %d transactions.\n' % unNumeroCreaciones)
             
            #unExecutionRecord and unExecutionRecord.pEndExecution()

                 
            

    
    ##/code-section class-header

    # Methods
# end of class TRAIdioma_Operaciones

##code-section module-footer #fill in your manual code here
##/code-section module-footer





        


    


    

    
    
    
    
    
    
    
    
    
    





    
    