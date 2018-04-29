# -*- coding: utf-8 -*-
#
# File: TRAContenidoXML_Operaciones.py
#
# Copyright (c) 2008, 2009, 2010 by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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





class TRAContenidoXML_Operaciones:
    """
    """
    security = ClassSecurityInfo()
 
    
    
    
    
    
    
    
    
    
    

    

    
    
    security.declarePrivate( 'fInformeXML')    
    def fInformeXML( self, theParentExecutionRecord=None):
        
        unExecutionRecord = self.fStartExecution( 'method',  'fInformeContenidoXML', theParentExecutionRecord,  False, ) 
        
        try:

            
            unInforme = self.fNewVoidContenidoXMLReport()

            
            unInforme.update( {
                'title':                            self.Title(),
                'description':                      self.Description(),
                'absolute_url':                     self.absolute_url(),
            })
           
            
            
            
            
            # ############################################
            """Report XML nodes to import.
            
            """
            aXMLSource = self.fContenidoXML()

            if aXMLSource:
      
                aModelDDvlPlone_tool = self.fModelDDvlPloneTool()
                if not ( aModelDDvlPlone_tool == None):
                    
                    aCatalogo = self.getCatalogo()
                    if not ( aCatalogo == None):
                    
                        aImportacion = self.getContenedor()
                        if not ( aImportacion == None):          
                            
                            aModelDDvlPloneTool_Retrieval = aModelDDvlPlone_tool.fModelDDvlPloneTool_Retrieval( self)
                            if not( aModelDDvlPloneTool_Retrieval == None):
                                            
                                aModelDDvlPloneTool_Import = aModelDDvlPlone_tool.fModelDDvlPloneTool_Import( self)
                                if not( aModelDDvlPloneTool_Import == None):
                                        
                                    someAllExportTypeConfigs =  aModelDDvlPloneTool_Retrieval.getAllTypeExportConfigs( self)        
                                    if someAllExportTypeConfigs:
                                         
                                        someExportTypeConfigsChosen = aImportacion.fImportTypeConfigsChosen( 
                                            theCatalogo                             =aCatalogo,
                                            theAllExportTypeConfigs                 =someAllExportTypeConfigs,
                                            theImportarTRACatalogo                  =aImportacion.getImportarXMLTRACatalogo(),
                                            theImportarTRAConfiguraciones           =aImportacion.getImportarXMLTRAConfiguraciones(),           
                                            theImportarTRAParametrosControlProgreso =aImportacion.getImportarXMLTRAParametrosControlProgreso(),
                                            theImportarTRAIdiomas                   =aImportacion.getImportarXMLTRAIdiomas(),                
                                            theImportarTRASolicitudesCadenas        =aImportacion.getImportarXMLTRASolicitudesCadenas(),
                                            theImportarTRAModulos                   =aImportacion.getImportarXMLTRAModulos(),                  
                                            theImportarTRAInformes                  =aImportacion.getImportarXMLTRAInformes(),                  
                                        )
                                        if someExportTypeConfigsChosen:
                                                                        
                                            someNombresTiposToCount = someExportTypeConfigsChosen.keys()[:]
                                                 
                                            # ############################################
                                            """Delegate on tool to parse and scan XML contents.
                                            
                                            """
                                            aXMLContentsSummary = aModelDDvlPloneTool_Import.fXMLContentSummary(
                                                theTimeProfilingResults        =None,
                                                theContextualElement           =aCatalogo, 
                                                theXMLSource                   =aXMLSource,
                                                theAcceptedXMLRootNodeName     =cNombreTipoTRACatalogo,
                                                theXMLNodeNamesToCount         =someNombresTiposToCount,
                                                theAdditionalParams            =None,
                                            )           
                                            if aXMLContentsSummary and aXMLContentsSummary.get( 'success', False):
                                                unInforme.update( {
                                                    'expected_num_nodes':         aXMLContentsSummary.get( 'num_nodes',         0),
                                                    'expected_num_nodes_by_type': aXMLContentsSummary.get( 'num_nodes_by_type', {}).copy(),
                                                })
                            
                    
                            
                                    
                                    
                                    
            
            # ############################################
            """Report binary file names.
            
            """
                
            someContenidosBinarios = self.fContenidoBinario()
            if someContenidosBinarios:
                someBinaryFileNames = [ ]
                
                for aContenidoBinario in someContenidosBinarios:
                    if aContenidoBinario:
                        aFileFullName  = aContenidoBinario.get( 'file_full_name',  '')
                        if aFileFullName:
                            someBinaryFileNames.append( aFileFullName)
                            
                unInforme[ 'binary_file_names'] =  someBinaryFileNames       
                
                     
            return unInforme
    
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
 

              

    
        
    
    
    
    
    
    
    

    
    security.declarePrivate('pHandle_manage_afterAdd')
    def pHandle_manage_afterAdd(self, theItem, theContainer):   
        """ Complete initialization after creation.
        
        """
        
        TRAArquetipo.manage_afterAdd(  self, theItem, theContainer)
        
        
        return self
    
    
    
    
    
    
    
    

    security.declarePrivate( 'pAllSubElements_into')    
    def pAllSubElements_into( self, theCollection, theAdditionalParams=None):
        if theCollection == None:
            return self
        theCollection.append( self)
        
         
        return self
        
        
    


    security.declarePrivate( 'pForAllElementsDo_recursive')    
    def pForAllElementsDo_recursive( self, theLambda):
        if not theLambda:
            return self
        
        theLambda( self)

        return self
    
    
    
    
    
    
    
    
    security.declareProtected( permissions.View, 'getImportacion')
    def getImportacion( self):
        return self.getContenedor()
   
    
    
    
    
    
    


    
    security.declarePrivate( 'pSetContenidoBinario')    
    def pSetContenidoBinario( self, theContenidoBinario):
        
        if not theContenidoBinario:
            self.setContenidoBinario( '')
            self.setFechaContenido( self.fDateTimeNow())
            return self
        
        if not ( isinstance( theContenidoBinario, list) or isinstance( theContenidoBinario, tuple) or isinstance( theContenidoBinario, set) ):
            self.setContenidoBinario( '')
            self.setFechaContenido( self.fDateTimeNow())
            return self
            
        someNewContenidosBinarios = [ ]
            
        someContenidosBinarios    = list( theContenidoBinario)

        for aContenidoBinario in someContenidosBinarios:
            if aContenidoBinario:
                
                aFileFullName  = aContenidoBinario.get( 'file_full_name',  '')
                aFileWholeData = aContenidoBinario.get( 'file_whole_data', '')
                
                if aFileFullName:
                    
                    aNewContenidoBinario = self.fNewVoidBinaryContent()
                    aNewContenidoBinario[ 'file_full_name'] = aFileFullName
                    
                    aBase64WholeData = ''
                    if aFileWholeData:
                        try:
                            aBase64WholeData = b64encode( aFileWholeData)
                        except:
                            None
                    aNewContenidoBinario[ 'file_whole_data'] = aBase64WholeData
                
                    someNewContenidosBinarios.append( aNewContenidoBinario)
                    
                    
                    
        unContenidoBinarioString = self.fStringFromContenidoBinario( someNewContenidosBinarios)
        
        
        unContenidoBinarioActual = self.getContenidoBinario()
        if not ( unContenidoBinarioString ==  unContenidoBinarioActual):
            self.setContenidoBinario( unContenidoBinarioString)
            self.setFechaContenido( self.fDateTimeNow())
        
        return self
    
    
            
            
    security.declarePrivate( 'fStringFromContenidoBinario')    
    def fStringFromContenidoBinario( self, theContenidoBinario):

        from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fReprAsString        
        
        unStringContenidoBinario = fReprAsString( theContenidoBinario)
        
        return unStringContenidoBinario
    




    
    security.declarePrivate( 'fNewVoidBinaryContents')    
    def fNewVoidBinaryContent( self, ):
        aBinaryContents = {
            'file_full_name':     '',
            'file_whole_data':    '',
        }
        return aBinaryContents


    
    
            
    security.declarePrivate( 'fContenidoBinario')    
    def fContenidoBinario( self, ):

        unContenidoBinarioString = self.getContenidoBinario()
        if not unContenidoBinarioString:
            return []
        
        
        someContenidosBinarios = self.fContenidoBinarioFromString( unContenidoBinarioString,)
        

        if not ( isinstance( someContenidosBinarios, list) or isinstance( someContenidosBinarios, tuple) or isinstance( someContenidosBinarios, set) ):
            return []
            
        someNewContenidosBinarios = [ ]
            
        for aContenidoBinario in someContenidosBinarios:
            if aContenidoBinario:
                
                aFileFullName    = aContenidoBinario.get( 'file_full_name',  '')
                aBase64WholeData = aContenidoBinario.get( 'file_whole_data', '')
                
                if aFileFullName:
                    
                    aNewContenidoBinario = self.fNewVoidBinaryContent()
                    aNewContenidoBinario[ 'file_full_name'] = aFileFullName
                    
                    aFileWholeData = ''
                    if aBase64WholeData:
                        try:
                            aFileWholeData = b64decode( aBase64WholeData)
                        except:
                            None
                    aNewContenidoBinario[ 'file_whole_data'] = aFileWholeData
                
                    someNewContenidosBinarios.append( aNewContenidoBinario)
                            
        return someNewContenidosBinarios
             

            
            
                                           

    security.declarePrivate( 'fContenidoBinarioFromString')    
    def fContenidoBinarioFromString( self, theContenidoBinarioString, ):
        
        if not theContenidoBinarioString:
            return None
        
        from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fEvalString
        
        aContenidoBinario = fEvalString( theContenidoBinarioString, theRaiseExceptions=False)
        
        return aContenidoBinario
    
            

        
    
    

    

    
    security.declarePrivate( 'pSetContenidoXML')    
    def pSetContenidoXML( self, theXMLSource):
        
        if not theXMLSource:
            self.setContenidoXML( '')
            self.setFechaContenido( self.fDateTimeNow())
            return self
        
        aBase64XMLSource = ''
        try:
            aBase64XMLSource = b64encode( theXMLSource)
        except:
            None
        
        
        unContenidoXMLActual = self.getContenidoXML()
        if not ( aBase64XMLSource ==  unContenidoXMLActual):
            self.setContenidoXML( aBase64XMLSource)
            self.setFechaContenido( self.fDateTimeNow())
        
        return self
    
    
            
            
    security.declarePrivate( 'fStringFromContenidoXML')    
    def fStringFromContenidoXML( self, theXMLSource):

        from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fReprAsString        
        
        unStringContenidoXML = fReprAsString( theXMLSource)
        
        return unStringContenidoXML
    



    
    
    
            
    security.declarePrivate( 'fContenidoXML')    
    def fContenidoXML( self, ):

        aBase64XMLSource = self.getContenidoXML()
        if not aBase64XMLSource:
            return ''
        
        aContenidoXMLString = self.fContenidoXMLStringFromBase64( aBase64XMLSource,)
        if not aContenidoXMLString:
            return ''
        
        return aContenidoXMLString
             

            
            
                                           

    security.declarePrivate( 'fContenidoXMLStringFromBase64')    
    def fContenidoXMLStringFromBase64( self, theBase64XMLSource, ):
        
        if not theBase64XMLSource:
            return ''
        
        unContenidoXMLString = ''
        try:
            unContenidoXMLString = b64decode( theBase64XMLSource)
        except:
            None
                    
        return unContenidoXMLString
    
            

        
    
        
    
    
    
    
    
            
    
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
            'label'   : self.fTranslateI18N( 'plone', 'XML Data', 'XML Data-',),
            'href'    : '%s/TRAContenidoXML/' % unaURL,
            'icon'    : '',
            'domain'  : 'plone',
            'msgid'   : 'XML Data',
        })
        unosExtraLinks.append( unExtraLink)      
        
        
        
        unImportacionURL = self.getContenedor().absolute_url()
        if not unImportacionURL:
            return unosExtraLinks
        
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
        
        
        
        unaImportacion = self.getContenedor()
        if not ( unaImportacion == None):
        
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
        
    
 

       
 
    
    
    
    



    
    