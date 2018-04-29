# -*- coding: utf-8 -*-
#
# File: TRAContenidoIntercambio_Operaciones.py
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


from base64 import b64encode, b64decode

from AccessControl import ClassSecurityInfo




import logging

import transaction

from math import floor


from StringIO import StringIO

from zipfile import ZipFile

from Products.Archetypes.utils import shasattr

from Products.CMFCore.utils import getToolByName

from Products.CMFCore       import permissions


from TRAElemento_Constants                 import *
from TRAElemento_Constants_Activity        import *
from TRAElemento_Constants_Configurations  import *
from TRAElemento_Constants_Contributions   import *
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

from TRAImportarExportar_Constants import cScannedKeys_String_Symbol, cScannedKeys_String_Errors, cScannedKeys_String_Translations, cScannedKeys_Translation_Errors, cScannedKeys_Translation_Translation


from TRAArquetipo                   import TRAArquetipo





class TRAContenidoIntercambio_Operaciones:
    """
    """
    security = ClassSecurityInfo()
 
    

    
    security.declarePrivate('pHandle_manage_afterAdd')
    def pHandle_manage_afterAdd(self, theItem, theContainer):   
        """ Complete initialization after creation.
        
        """
        
        TRAArquetipo.manage_afterAdd(  self, theItem, theContainer)
        
        self.pInitDefaultAttributesFromImport( theItem, theContainer)
        
        return self
    
    
    

    
    
    security.declarePrivate('pInitDefaultAttributesFromImport')
    def pInitDefaultAttributesFromImport(self, theItem, theContainer):   

        unaImportacion = theContainer
        #try:
            #unaImportacion = self.getContenedor()
        #except:
            #None
        if unaImportacion == None:
            return self
        
        unValue = unaImportacion.getNombreModuloPorDefecto()        
        theItem.setNombreModuloPorDefecto( unValue)
        
        unValue = unaImportacion.getImportarConNombreModuloConfigurado()        
        theItem.setImportarConNombreModuloConfigurado( unValue)
        
        unValue = unaImportacion.getImportarFuentesDesdeComentarios()        
        theItem.setImportarFuentesDesdeComentarios( unValue)
        
        unValue = unaImportacion.getImportarNombreModuloDesdeDominioONombreFichero()        
        theItem.setImportarNombreModuloDesdeDominioONombreFichero( unValue)
        
        unValue = unaImportacion.getImportarNombresModulosDesdeComentarios()        
        theItem.setImportarNombresModulosDesdeComentarios( unValue)
        
        unValue = unaImportacion.getImportarContribucionesDesdeComentarios()        
        theItem.setImportarContribucionesDesdeComentarios( unValue)
        
        unValue = unaImportacion.getImportarStatusDesdeComentarios()        
        theItem.setImportarStatusDesdeComentarios( unValue)
        
        return self
        
    
    
    
    
    
    

    
    
    security.declarePrivate('fInitial_CrearInformeAntes')
    def fInitial_CrearInformeAntes(self, ):   

        unaImportacion = None
        try:
            unaImportacion = self.getContenedor()
        except:
            None
        if not unaImportacion:
            return False
        
        unValue = unaImportacion.getCrearInformeAntesPorDefecto()        
        return unValue
    
    
    
    
    
    security.declarePrivate('fInitial_CrearInformeDespues')
    def fInitial_CrearInformeDespues(self, ):   

        unaImportacion = None
        try:
            unaImportacion = self.getContenedor()
        except:
            None
        if not unaImportacion:
            return False
        
        unValue = unaImportacion.getCrearInformeDespuesPorDefecto()        
        return unValue
    
    
    
    
   
    security.declarePrivate('fInitial_CodigoIdiomaPorDefecto')
    def fInitial_CodigoIdiomaPorDefecto(self, ):   

        unaImportacion = None
        try:
            unaImportacion = self.getContenedor()
        except:
            None
        if not unaImportacion:
            return ''
        
        unValue = unaImportacion.getCodigoIdiomaPorDefecto()        
        return unValue
        
    
    
    
    security.declarePrivate('fInitial_NombreModuloPorDefecto')
    def fInitial_NombreModuloPorDefecto(self, ):   

        unaImportacion = None
        try:
            unaImportacion = self.getContenedor()
        except:
            None
        if not unaImportacion:
            return ''
        
        unValue = unaImportacion.getNombreModuloPorDefecto()        
        return unValue
    
    
    
    
    
    security.declarePrivate('fInitial_ImportarConNombreModuloConfigurado')
    def fInitial_ImportarConNombreModuloConfigurado(self, ):   

        unaImportacion = None
        try:
            unaImportacion = self.getContenedor()
        except:
            None
        if not unaImportacion:
            return False
        
        unValue = unaImportacion.getImportarConNombreModuloConfigurado()        
        return unValue
    
    

 
  
 
    
    security.declarePrivate('fInitial_ImportarNombreModuloDesdeDominioONombreFichero')
    def fInitial_ImportarNombreModuloDesdeDominioONombreFichero(self, ):   

        unaImportacion = None
        try:
            unaImportacion = self.getContenedor()
        except:
            None
        if not unaImportacion:
            return False
        
        unValue = unaImportacion.getImportarNombreModuloDesdeDominioONombreFichero()        
        return unValue
    
    

 
    
    security.declarePrivate('fInitial_ImportarNombresModulosDesdeComentarios')
    def fInitial_ImportarNombresModulosDesdeComentarios(self, ):   

        unaImportacion = None
        try:
            unaImportacion = self.getContenedor()
        except:
            None
        if not unaImportacion:
            return False
        
        unValue = unaImportacion.getImportarNombresModulosDesdeComentarios()        
        return unValue
    
    
    
    
  
    security.declarePrivate('fInitial_ImportarFuentesDesdeComentarios')
    def fInitial_ImportarFuentesDesdeComentarios(self, ):   

        unaImportacion = None
        try:
            unaImportacion = self.getContenedor()
        except:
            None
        if not unaImportacion:
            return False
        
        unValue = unaImportacion.getImportarFuentesDesdeComentarios()        
        return unValue
    
    

 
    
    security.declarePrivate('fInitial_ImportarStatusDesdeComentarios')
    def fInitial_ImportarStatusDesdeComentarios(self, ):   

        unaImportacion = None
        try:
            unaImportacion = self.getContenedor()
        except:
            None
        if not unaImportacion:
            return False
        
        unValue = unaImportacion.getImportarStatusDesdeComentarios()        
        return unValue
    
    

 
    
    security.declarePrivate('fInitial_ImportarContribucionesDesdeComentarios')
    def fInitial_ImportarContribucionesDesdeComentarios(self, ):   

        unaImportacion = None
        try:
            unaImportacion = self.getContenedor()
        except:
            None
        if not unaImportacion:
            return False
        
        unValue = unaImportacion.getImportarContribucionesDesdeComentarios()        
        return unValue
    
    
    
    
 
    
    security.declarePrivate('fInitial_NumeroMaximoLineasAExplorar')
    def fInitial_NumeroMaximoLineasAExplorar(self, ):   

        unaImportacion = None
        try:
            unaImportacion = self.getContenedor()
        except:
            None
        if not unaImportacion:
            return 0
        
        unValue = unaImportacion.getNumeroMaximoLineasAExplorar()        
        return unValue
    
    
     
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    

    security.declarePrivate( 'pAllSubElements_into')    
    def pAllSubElements_into( self, theCollection, theAdditionalParams=None):
        if theCollection == None:
            return self
        theCollection.append( self)
        
         
        return self
        
        
    


    security.declarePrivate( 'pForAllElementsDo_recursive')    
    def pForAllElementsDo_recursive( self, theLambda=None, thePloneLambda=None,):
        if not theLambda:
            return self
        
        theLambda( self)
                
        if thePloneLambda:
            self.pForAllElementsPloneDo( thePloneLambda)

        return self
    
    
    
    security.declareProtected( permissions.View, 'getImportacion')
    def getImportacion( self):
        return self.getContenedor()
   


    
    security.declarePrivate( 'pSetContenido')    
    def pSetContenido( self, theContenido):
        
        if not theContenido:
            self.setContenido( '')
            self.setFechaContenido( self.fDateTimeNow())
            return self
        
        unContenido = theContenido.copy()
        if unContenido:
            aScannedData = unContenido.get( 'content_data', None)
            if aScannedData:
                if aScannedData.has_key( 'symbols_dict'):
                    aScannedData.pop( 'symbols_dict')
                    
        unContenidoString = self.fStringFromContenidoDeUploadedFile( unContenido)
        
        aBase64XMLSource = ''
        try:
            aBase64XMLSource = b64encode( unContenidoString)
        except:
            None
        
        unContenidoActual = self.getContenido()
        if not ( aBase64XMLSource ==  unContenidoActual):
            self.setContenido( aBase64XMLSource)
            self.setFechaContenido( self.fDateTimeNow())
        
        
        return self
    
    
            
            
    security.declarePrivate( 'fStringFromContenidoDeUploadedFile')    
    def fStringFromContenidoDeUploadedFile( self, theContenidoUploadedFile):

        from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fReprAsString        
        
        unStringContenido = fReprAsString( theContenidoUploadedFile)
        
        return unStringContenido
    




    
            


    
    
            
    security.declarePrivate( 'fContenido')    
    def fContenido( self, ):

        unContenidoBase64 = self.getContenido()
        if not unContenidoBase64:
            return self.fNewVoidScannedData()
        
        unContenidoString = self.fContenidoStringFromBase64( unContenidoBase64,)
        if not unContenidoString:
            return self.fNewVoidScannedData()
        
        unContenido = self.fContenidoFromString( unContenidoString,)
        
        return unContenido
             

            
            
                                           

    security.declarePrivate( 'fContenidoFromString')    
    def fContenidoFromString( self, theContenidoString, ):
        
        if not theContenidoString:
            return None
        
        from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fEvalString
        
        aContenido = fEvalString( theContenidoString, theRaiseExceptions=False)
        
        return aContenido
    
            

    security.declarePrivate( 'fContenidoStringFromBase64')    
    def fContenidoStringFromBase64( self, theBase64String, ):
        
        if not theBase64String:
            return ''
        
        unContenidoString = ''
        try:
            unContenidoString = b64decode( theBase64String)
        except:
            None
                    
        return unContenidoString
        
    
    
    
    
    
    
    
    
    
    
    security.declarePrivate( 'fInformeContenidoIntercambio')    
    def fInformeContenidoIntercambio( self, theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fInformeContenidoIntercambios', theParentExecutionRecord,  False, ) 
        
        try:
            unContenido = self.fContenido()
            if not unContenido:
                return None
            
            
            unInforme = self.fNewVoidContenidoIntercambioReport()
            
            unInforme.update( {
                'title':                            self.Title(),
                'description':                      self.Description(),
                'absolute_url':                     self.absolute_url(),
            })

            
            
            
            aScannedData = unContenido.get( 'content_data', None)
            if not aScannedData:
                return None
            
            
            
            unasScannedStrings           = aScannedData[ 'symbols']
            unosScannedLanguages         = aScannedData[ 'languages']
                
 
            someLanguageNamesAndFlags = self.fLanguagesNamesAndFlagsPorCodigo().copy()
            
            unInforme[ 'language_names_and_flags'] = someLanguageNamesAndFlags
            
            
            someLanguagesDetails = aScannedData.get( 'languages_details', None)
            if someLanguagesDetails:
                
                for aLanguageDetailCode in someLanguagesDetails.keys():
                    
                    if not someLanguageNamesAndFlags.has_key( aLanguageDetailCode):
                        
                        aLanguageDetail = someLanguagesDetails.get( aLanguageDetailCode, None)
                        if aLanguageDetail:
                            unLanguageNamesAndFlag = {
                                'english'       :  aLanguageDetail.get( 'english_name', aLanguageDetailCode), 
                                'native'        :  aLanguageDetail.get(  'nombre_nativo_de_idioma', aLanguageDetail.get( 'english_name', aLanguageDetailCode)), 
                            }
                            someLanguageNamesAndFlags[ aLanguageDetailCode] = unLanguageNamesAndFlag
            
                            
                            
                            
            unInforme[ 'languages'] = sorted( unosScannedLanguages)
            unInforme[ 'modules']   = sorted( aScannedData[ 'modules'])            

           
            unInforme[ 'num_symbol_errors'] = aScannedData[ 'num_symbol_errors']
            
            
            
            unosNumTranslationsByLanguage   = unInforme[ 'num_translated_by_language']
            unosNumEncodingErrorsByLanguage = unInforme[ 'num_encoding_errors_by_language']
            
            
            
            
            for unLanguage in unosScannedLanguages:
                unosNumTranslationsByLanguage[      unLanguage] = 0    
                unosNumEncodingErrorsByLanguage[    unLanguage] = 0   
                   
                
                
            unNumStrings = 0   
                
            for unaScannedString in unasScannedStrings:
                
                if unaScannedString:
                    
                    unStringSymbol  = unaScannedString.get( cScannedKeys_String_Symbol, None)
                    if unStringSymbol:
                        
                        unNumStrings += 1
                        
                        unosStringErrors       = unaScannedString.get( cScannedKeys_String_Errors, None)
                        if unosStringErrors:
                            unInforme[ 'num_string_errors'] += 1
                            
        
                        unasScannedTranslations = unaScannedString[ cScannedKeys_String_Translations]
                        
                        unosStringLenguages    = unasScannedTranslations.keys()   
                        
                        for unLenguage in unosStringLenguages:
                            
                            unaScannedTranslation = unasScannedTranslations.get( unLenguage, None)
                            if unaScannedTranslation:
                                
                                aTranslation          = unaScannedTranslation.get( cScannedKeys_Translation_Translation, None)
                                unosTranslationErrors = unaScannedTranslation.get( cScannedKeys_Translation_Errors, None)
                                
                                if aTranslation:
                                    unosNumTranslationsByLanguage[ unLenguage]   = unosNumTranslationsByLanguage.get( unLenguage, 0) + 1
                            
                                if unosTranslationErrors:
                                    unosNumEncodingErrorsByLanguage[ unLenguage] = unosNumEncodingErrorsByLanguage.get( unLenguage, 0) + 1
               
                 
                            
            unInforme[ 'num_strings'] = unNumStrings
                            
            unPercentStringErrors = 100
            if unNumStrings:
                unPercentStringErrors =  int( ( ( 0.0 + unInforme[ 'num_string_errors']) / unNumStrings) * 100)
                
            unInforme[ 'percent_string_errors'] =  unPercentStringErrors   
                
            
            for unLenguage in unosScannedLanguages:
                
                unNumeroTraducciones = unosNumTranslationsByLanguage[ unLenguage]
                
                if not unNumeroTraducciones:
                    unPercentTranslated  = 0
                    unPercentPending     = 100
                    unPercentEncodingErrors = 0
                    
                else:
                    unPercentTranslated = int( ( ( 0.0 + unNumeroTraducciones) / unNumStrings) * 100)
                    if not unPercentTranslated:
                        unPercentTranslated = 1
                    unPercentPending = 100 - unPercentTranslated
                    unPercentEncodingErrors = int( ( ( 0.0 + unosNumEncodingErrorsByLanguage[ unLenguage]) / unNumStrings) * 100)
                    
                unInforme[ 'num_pending_by_language'][             unLenguage] = unNumStrings - unNumeroTraducciones
                unInforme[ 'percent_pending_by_language'][         unLenguage] = unPercentPending
                unInforme[ 'percent_translated_by_language'][      unLenguage] = unPercentTranslated
                unInforme[ 'percent_encoding_errors_by_language'][ unLenguage] = unPercentEncodingErrors
                        
            return unInforme
         
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
       
        
      
    
    
    
    
    
    
   
    security.declarePrivate( 'fSumarioContenido')    
    def fSumarioContenido( self, theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fSumarioContenido', theParentExecutionRecord,  False, ) 
        
        try:
            unInformeContenido = self.fInformeContenidoIntercambio( unExecutionRecord)
            if not unInformeContenido:
                return ''
            
            unNumeroCadenas = unInformeContenido.get( 'num_strings', 0)
            unLanguageNames = ','.join( unInformeContenido.get( 'languages', []))
            unModuleNames   = ','.join( sorted( unInformeContenido.get( 'modules', set())))
            
            unSumario = '#%d  %s  %s' % (  unNumeroCadenas,  unLanguageNames, unModuleNames)
            
            
            return unSumario
    
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
       
        
  
 

    
  
 
    
    
            
    
    security.declarePublic( 'fExtraLinks')    
    def fExtraLinks( self):
        
        unosExtraLinks = TRAArquetipo.fExtraLinks( self)
        if not unosExtraLinks:
            unosExtraLinks = [ ]
        
        unaURL = self.absolute_url()
        if not unaURL:
            return unosExtraLinks
        

        unExtraLink = self.fNewVoidExtraLink()
        unExtraLink.update( {
            'label'   : self.fTranslateI18N( 'plone', 'Data', 'Data-',),
            'href'    : '%s/TRAContenidoIntercambioDatos/' % unaURL,
            'icon'    : '',
            'domain'  : 'plone',
            'msgid'   : 'Data',
        })
        unosExtraLinks.append( unExtraLink)      
        
        unaImportacion = self.getContenedor()
        if not ( unaImportacion == None):
            
            unImportacionURL = unaImportacion.absolute_url()
            if unImportacionURL:
        
                unExtraLink = self.fNewVoidExtraLink()
                unExtraLink.update( {
                    'label'   : self.fTranslateI18N( 'plone', 'Summary', 'Summary-',),
                    'href'    : '%s/TRAImportacionContenidosSumario/' % unImportacionURL,
                    'icon'    : '',
                    'domain'  : 'plone',
                    'msgid'   : 'Summary',
                })
                unosExtraLinks.append( unExtraLink)
                                    
                unExtraLink = self.fNewVoidExtraLink()
                unExtraLink.update( {
                    'label'   : self.fTranslateI18N( 'plone', 'Details', 'Details-',),
                    'href'    : '%s/TRAImportacionContenidosDetalle/' % unImportacionURL,
                    'icon'    : '',
                    'domain'  : 'plone',
                    'msgid'   : 'Details',
                })
                unosExtraLinks.append( unExtraLink)
                                    
            unElementoContenidoXML = unaImportacion.fObtenerContenidoXML()
            if not ( unElementoContenidoXML == None):
                unExtraLink = self.fNewVoidExtraLink()
                unExtraLink.update( {
                    'label'   : self.fTranslateI18N( 'plone', 'XML Data', 'XML Data-',),
                    'href'    : '%s/Tabular/' % unElementoContenidoXML.absolute_url(),
                    'icon'    : 'tracontenidoxml.gif',
                    'domain'  : 'plone',
                    'msgid'   : 'XML Data',
                })
                unosExtraLinks.append( unExtraLink)        
                
            unElementoProgreso = unaImportacion.fDeriveElementoProgreso()
            if not ( unElementoProgreso == None):
                unExtraLink = self.fNewVoidExtraLink()
                unExtraLink.update( {
                    'label'   : self.fTranslateI18N( 'plone', 'Progress', 'Progress-',),
                    'href'    : '%s/TRAProgressResults/' % unElementoProgreso.absolute_url(),
                    'icon'    : 'traprogreso.gif',
                    'domain'  : 'plone',
                    'msgid'   : 'Progress',
                })
                unosExtraLinks.append( unExtraLink)        
                
            
        return unosExtraLinks
        
    
 

       
 
    
    
    
    



    
    