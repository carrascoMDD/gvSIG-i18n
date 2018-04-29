# -*- coding: utf-8 -*-
#
# File: TRAProgreso_Operaciones.py
#
# Copyright (c) 2008, 2009,2010 by Conselleria de Infraestructuras y Transporte de la
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




##code-section module-header #fill in your manual code here


import sys
import traceback
import logging
import transaction


from AccessControl          import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName

from Products.CMFCore       import permissions


from TRAElemento_Constants  import *




from TRAElemento_Operaciones import TRAElemento_Operaciones


class TRAProgreso_Operaciones:
    """Operations specifically defined on persistent elements that store the progress information about a long-lived process.
    
    """
    security = ClassSecurityInfo()
     



    security.declarePrivate( 'pAllSubElements_into')    
    def pAllSubElements_into( self, theCollection, theAdditionalParms=None):
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

    
    
    
    

    
    security.declarePrivate( 'fDeriveElementoEspecificacionProceso')
    def fDeriveElementoEspecificacionProceso( self):
        
        unProcessElementId = self.getIdentificadorElementoProceso()
        if not unProcessElementId:
            return None
        
        unProcessElementType = self.getTipoElementoProceso()
        if not unProcessElementType:
            return None
        
        unCatalogo = self.getCatalogo()
        if ( unCatalogo == None):
            return None
        
        if unProcessElementType == cNombreTipoTRAImportacion:
            
            unaColeccionImportaciones = unCatalogo.fObtenerColeccionImportaciones()
            if ( unaColeccionImportaciones == None):
                return None
            
            unElementoProgreso = unaColeccionImportaciones.getElementoPorID( unProcessElementId)
            return unElementoProgreso
        
            
        return None
        
        
    
           
    
    security.declarePublic( 'fExtraLinks')    
    def fExtraLinks( self):
        
        unosExtraLinks = TRAElemento_Operaciones.fExtraLinks( self)
        if not unosExtraLinks:
            unosExtraLinks = [ ]
        
        unaURL = self.absolute_url()
        if not unaURL:
            return unosExtraLinks
        

        unExtraLink = self.fNewVoidExtraLink()
        unExtraLink.update( {
            'label'   : self.fTranslateI18N( 'plone', 'Results', 'Results-',),
            'href'    : '%s/TRAProgressResults_action/' % unaURL,
            'icon'    : '',
            'domain'  : 'plone',
            'msgid'   : 'Results',
        })
        unosExtraLinks.append( unExtraLink)
          
                            
        unElementoEspecificacionProgreso = self.fDeriveElementoEspecificacionProceso()
        if not ( unElementoEspecificacionProgreso == None):
            unExtraLink = self.fNewVoidExtraLink()
            unExtraLink.update( {
                'label'   : self.fTranslateI18N( 'plone', 'Process specification', 'Process specification-',),
                'href'    : '%s/Tabular/' % unElementoEspecificacionProgreso.absolute_url(),
                'icon'    : 'traimportacion.gif',
                'domain'  : 'plone',
                'msgid'   : 'ProcessSpecification',
            })
            unosExtraLinks.append( unExtraLink)

        return unosExtraLinks
    
            
    
    
    security.declareProtected( permissions.View, 'fEstadoControl')
    def fEstadoControl( self,):
        aProgressHandler = self.fObtenerProgressHandler( )
        if not aProgressHandler:
            return { }
        
        aEstadoControlProgreso = aProgressHandler.fEstadoControl()
        if not aEstadoControlProgreso:
            return aEstadoControlProgreso
        
        aEstadoControlProgreso = aEstadoControlProgreso.copy()
        aEstadoControlProgreso[ 'timestamp'] = self.fDateTimeNowTextual()
        
        return aEstadoControlProgreso
    
    
    
        
    
    security.declareProtected( permissions.View, 'fObtenerProgressHandler')
    def fObtenerProgressHandler( self,):
        aKey = self.fProgressHandlerKey()
        if not aKey:
            return None
        
        aProgressHandler = self.fObtenerProgressHandlerByKey( aKey)
        return aProgressHandler
    
    
        
    security.declareProtected( permissions.View, 'fHasProgressHandler')
    def fHasProgressHandler( self,):
        aProgressHandler = self.fObtenerProgressHandler( )
        aHasProgressHandler = not( aProgressHandler == None)
        return aHasProgressHandler
    
    
        
              
    
    #security.declareProtected( permissions.View, 'fObtenerProgressControlParameters')
    #def fObtenerProgressControlParameters( self,):
        #aKey = self.fProgressHandlerKey()
        #if not aKey:
            #return None
        
        #someProgressControlParameters = self.fObtenerProgressControlParametersByKey( aKey)
        #return someProgressControlParameters
    
    
    
    
    
    security.declareProtected( permissions.View, 'fProgressHandlerKey')
    def fProgressHandlerKey( self,):   

        aKey = self.fNewVoidProgressHandlerKey()
        aKey.update( {
            'translations_catalog_root_path':  self.fPathDelRaiz(),
            'progress_element_UID':            self.UID(),            
            'progress_element_title':          self.Title(),
            'progress_element_description':    self.Description(),
            'progress_element_URL':            self.absolute_url(), 
            'progress_element_id':             self.getId(),
        })
        return aKey  
    
    
    
       
        
    security.declareProtected( permissions.View, 'fDatosResultado')
    def fDatosResultado( self,):                        
        """Create objects structure from the runtime support object, of from the text representation stored as the content of a string field.
        
        """
        
        aProgressHandler = self.fObtenerProgressHandler( )
        if aProgressHandler:
            
            aProgressHandler.pAccumulateElementsByType()
            
            unResult = aProgressHandler.vResult
            if unResult:
                
                unosDatosResultadoString = None
                try:
                    unosDatosResultadoString = self.fReprAsString( unResult)
                except:
                    None
                if unosDatosResultadoString:
                    
                    unosDatosResultado = None
                    try:
                        unosDatosResultado = self.fEvalString( unosDatosResultadoString)
                    except:
                        None
                    if unosDatosResultado:
                        unosDatosResultado[ 'from_progress_handler'] = True
                        unosDatosResultado[ 'timestamp'] = self.fDateTimeNowTextual()
                        return unosDatosResultado

        unosDatosResultadoString = self.getDatosResultado()
        if not unosDatosResultadoString:
            return None
                
        unosDatosResultado = None
        try:
            unosDatosResultado = self.fEvalString( unosDatosResultadoString)
        except:
            None
            
        if not ( unosDatosResultado == None):
            unosDatosResultado[ 'from_progress_handler'] = False
            
        return unosDatosResultado
        
    

    

        
    security.declareProtected( permissions.ModifyPortalContent, 'pSetDatosResultado')
    def pSetDatosResultado( self, theResult):                        
        """Store string representation of objects structure as the content of a string field.
        
        """
        
        unosDatosResultadoString = None
        if theResult:
            unResult = theResult.copy()
            unResult[ 'from_progress_handler'] = False
            unResult[ 'timestamp'] = self.fDateTimeNowTextual()
                
            try:
                unosDatosResultadoString = self.fReprAsString( unResult)
            except:
                None
            
        self.setDatosResultado( unosDatosResultadoString)
                
        return self
        
    

    



        
    security.declareProtected( permissions.View, 'fParametrosEntrada')
    def fParametrosEntrada( self,):                        
        """Create objects structure from the text representation stored as the content of a string field.
        
        """
        
        unosParametrosEntradaString = self.getParametrosEntrada()
        if not unosParametrosEntradaString:
            return None
                
        unosParametrosEntrada = None
        try:
            unosParametrosEntrada = self.fEvalString( unosParametrosEntradaString)
        except:
            None
            
        return unosParametrosEntrada
        
    

    

        
    security.declareProtected( permissions.ModifyPortalContent, 'pSetParametrosEntrada')
    def pSetParametrosEntrada( self, theInputParameters):                        
        """Store string representation of objects structure as the content of a string field.
        
        """
        
        unosParametrosEntradaString = None
        if theInputParameters:
            try:
                unosParametrosEntradaString = self.fReprAsString( theInputParameters)
            except:
                None
            
        self.setParametrosEntrada( unosParametrosEntradaString)
                
        return self
        
    



        
    security.declareProtected( permissions.View, 'fParametrosControl')
    def fParametrosControl( self,):                        
        """Create objects structure from the text representation stored as the content of a string field.
        
        """
        
        aProgressHandler = self.fObtenerProgressHandler( )
        if aProgressHandler:
                        
            unosParameters = aProgressHandler.vProgressControlParameters
            if unosParameters:
                
                unosParametrosControlString = None
                try:
                    unosParametrosControlString = self.fReprAsString( unosParameters)
                except:
                    None
                if unosParametrosControlString:
                    
                    unosParametrosControl = None
                    try:
                        unosParametrosControl = self.fEvalString( unosParametrosControlString)
                    except:
                        None
                    if unosParametrosControl:
                        unosParametrosControl[ 'from_progress_handler'] = True
                        unosParametrosControl[ 'timestamp'] = self.fDateTimeNowTextual()
                        return unosParametrosControl
                    
                    
        unosParametrosControlString = self.getParametrosControl()
        if not unosParametrosControlString:
            return None
                
        unosParametrosControl = None
        try:
            unosParametrosControl = self.fEvalString( unosParametrosControlString)
        except:
            None
            
        if not ( unosParametrosControl == None):
            unosParametrosControl[ 'from_progress_handler'] = False
            
        return unosParametrosControl
        
    

    

        
    security.declareProtected( permissions.ModifyPortalContent, 'pSetParametrosControl')
    def pSetParametrosControl( self, theParameters):                        
        """Store string representation of objects structure as the content of a string field.
        
        """
        
        unosParametrosControlString = None
        if theParameters:
            someParameters = theParameters.copy()
            someParameters[ 'from_progress_handler'] = False
            someParameters[ 'timestamp'] = self.fDateTimeNowTextual()
            try:
                unosParametrosControlString = self.fReprAsString( someParameters)
            except:
                None
            
        self.setParametrosControl( unosParametrosControlString)
                
        return self
        
    
    
    

        
    security.declareProtected( permissions.View, 'fContadoresControl')
    def fContadoresControl( self,):                        
        """Create objects structure from the text representation stored as the content of a string field.
        
        """
        aProgressHandler = self.fObtenerProgressHandler( )
        if aProgressHandler:
                        
            uosCounters = aProgressHandler.vProgressControlCounters
            if uosCounters:
                
                unosContadoresControlString = None
                try:
                    unosContadoresControlString = self.fReprAsString( uosCounters)
                except:
                    None
                if unosContadoresControlString:
                    
                    unosContadoresControl = None
                    try:
                        unosContadoresControl = self.fEvalString( unosContadoresControlString)
                    except:
                        None
                    if unosContadoresControl:
                        unosContadoresControl[ 'from_progress_handler'] = True
                        unosContadoresControl[ 'timestamp'] = self.fDateTimeNowTextual()
                        return unosContadoresControl
        
        unosContadoresControlString = self.getContadoresControl()
        if not unosContadoresControlString:
            return None
                
        unosContadoresControl = None
        try:
            unosContadoresControl = self.fEvalString( unosContadoresControlString)
        except:
            None
            
        if not ( unosContadoresControl == None):
            unosContadoresControl[ 'from_progress_handler'] = False
            
        return unosContadoresControl
        
    

    

        
    security.declareProtected( permissions.ModifyPortalContent, 'pSetContadoresControl')
    def pSetContadoresControl( self, theCounters):                        
        """Store string representation of objects structure as the content of a string field.
        
        """
        
        unosContadoresControlString = None
        if theCounters:
            someCounters = theCounters.copy()
            someCounters[ 'from_progress_handler'] = False
            someCounters[ 'timestamp'] = self.fDateTimeNowTextual()
            try:
                unosContadoresControlString = self.fReprAsString( someCounters)
            except:
                None
            
        self.setContadoresControl( unosContadoresControlString)
                
        return self
            