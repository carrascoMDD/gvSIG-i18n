# -*- coding: utf-8 -*-
#
# File: TRAInforme_Operaciones.py
#
# Copyright (c) 2008, 2009 by Conselleria de Infraestructuras y Transporte de la
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



from AccessControl import ClassSecurityInfo



##code-section module-header #fill in your manual code here


import sys
import traceback


import logging

import transaction

from math import floor


from StringIO import StringIO


from Products.CMFCore.utils import getToolByName


from Products.CMFCore       import permissions




from TRAElemento_Constants              import *

from TRATraduccion_Operaciones          import cMarcaDeComentarioSinCambios

from TRAElemento_Permission_Definitions import cUseCase_GenerateTRAInformeLanguages, cUseCase_GenerateTRAInformeModules, cBoundObject




class TRAInforme_Operaciones:
    """
    """
    security = ClassSecurityInfo()
     



    
    security.declareProtected( permissions.ModifyPortalContent, 'fElaborarInforme')
    def fElaborarInforme( self, 
        theForceEllaboration        =False, 
        theCheckPermissions         =False, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):
        """Generate the report by delegating in the TRACatalogo.
        
        """
        
       
        unExecutionRecord = self.fStartExecution( 'method',  'fElaborarInforme', theParentExecutionRecord, False) 
        
        try:
            if ( not theForceEllaboration) and self.getHaComenzado():
                return False
            
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
               
            unInformeIdiomasUseCaseQueryResult = None
            unInformeModulosUseCaseQueryResult = None
            if theCheckPermissions:
                unInformeIdiomasUseCaseQueryResult = self.fUseCaseAssessment(  
                    theUseCaseName          = cUseCase_GenerateTRAInformeLanguages,        
                    theElementsBindings     = { cBoundObject: self,},                                    
                    theRulesToCollect       = None,                                                      
                    thePermissionsCache     = unPermissionsCache,                                        
                    theRolesCache           = unRolesCache,                                              
                    theParentExecutionRecord= unExecutionRecord,                                          
                )
                 
                unInformeModulosUseCaseQueryResult = self.fUseCaseAssessment( 
                    theUseCaseName          = cUseCase_GenerateTRAInformeModules,        
                    theElementsBindings     = { cBoundObject: self,},                                    
                    theRulesToCollect       = None,                                                      
                    thePermissionsCache     = unPermissionsCache,                                        
                    theRolesCache           = unRolesCache,                                              
                    theParentExecutionRecord= unExecutionRecord,                                          
                )
    
            unCatalogo = self.getCatalogo()
            if not unCatalogo:
                self.setInformeExcepcion( "No containing Catalog found - possibly an instance of TRAInforme that has not been properly created")
                return False
    
     
            unMemberId = self.fGetMemberId()                
            unAhora    = self.fDateTimeNow()
            
            self.setHaComenzado( True)
            self.setEstadoProceso( 'Activo')
            self.setUsuarioInformador( unMemberId)
            self.setFechaComienzoProceso( unAhora)
            self.setHaCompletadoConExito( False)
            
            self.setInformeExcepcion( '')
            self.setInformeExcepcionIdiomas( '')
            self.setInformeExcepcionModulos( '')
             
                    
            transaction.commit( )
    
            logging.getLogger( 'gvSIGi18n::fElaborarInforme').info("COMMIT") 
    
            unInformeIdiomasEllaborated = False
            unInformeModulosEllaborated = False
            
            unFechaFinProceso = None
            unaException = None
            try:     
                
                try:
    
                    if unInformeIdiomasUseCaseQueryResult and unInformeIdiomasUseCaseQueryResult.get( 'success', False):
                        unInformeIdiomas = unCatalogo.fElaborarInformeIdiomas( 
                            unInformeIdiomasUseCaseQueryResult, 
                            unPermissionsCache, 
                            unRolesCache, 
                            unExecutionRecord
                        )
                        if not unInformeIdiomas:
                            unInformeExceptionIdiomas = "No Languages Report produced from Catalog - possibly an error in the reporting process."
                        unInformeExceptionIdiomas = unInformeIdiomas.get( 'exception', '')
                        if unInformeExceptionIdiomas:
                            self.setInformeExcepcionIdiomas( unInformeExceptionIdiomas)
                            self.setInformeExcepcion( "Exception during Languages Report Generation")
                             
                        if unInformeIdiomas.get( 'success', False):
                            unInformeIdiomas[ 'report_date'] = self.fDateTimeToString( self.fDateTimeNow())
                            unInformeIdiomasString = ''
                            try:
                                unInformeIdiomasString = str( unInformeIdiomas)
                            except:
                                None
                            if not unInformeIdiomasString:
                                self.setInformeExcepcionIdiomas( "Error converting Report to a String representation")
                                self.setInformeExcepcion( "Exception during Languages Report storage")
                                return False
                            
                            self.setInformeIdiomas( unInformeIdiomasString)
                            unInformeIdiomasEllaborated = True

                    
                    if unInformeModulosUseCaseQueryResult and unInformeModulosUseCaseQueryResult.get( 'success', False):
                        unInformeModulos = unCatalogo.fElaborarInformeModulos( 
                            unInformeModulosUseCaseQueryResult, 
                            unPermissionsCache, 
                            unRolesCache, 
                            unExecutionRecord
                        )
                        if not unInformeModulos:
                            unInformeExceptionModulos = "No Modules Report produced from Catalog - possibly an error in the reporting process."
                        unInformeExceptionModulos = unInformeModulos.get( 'exception', '')
                        if unInformeExceptionModulos:
                            self.setInformeExcepcionModulos( unInformeExceptionModulos)
                            self.setInformeExcepcion( "Exception during Modules Report Generation")
                             
                        if unInformeModulos.get( 'success', False):
                            unInformeModulos[ 'report_date'] = self.fDateTimeToString( self.fDateTimeNow())
                            unInformeModulosString = ''
                            try:
                                unInformeModulosString = str( unInformeModulos)
                            except:
                                None
                            if not unInformeModulosString:
                                self.setInformeExcepcionModulos( "Error converting Report to a String representation")
                                self.setInformeExcepcion( "Exception during Languages Report storage")
                                return False
                      
                        
                            self.setInformeModulos( unInformeModulosString)
                            unInformeModulosEllaborated = True
                    
                    return True
                
                except:
                    unaExceptionInfo = sys.exc_info()
                    unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                    
                    unInformeExcepcion = 'Exception during fElaborarInforme\n' 
                    unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                    unInformeExcepcion += unaExceptionFormattedTraceback   
                             
                       
                    unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)
    
                    if cLogExceptions:
                        logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                    
                    return False
    
            finally:
                self.setEstadoProceso( 'Inactivo')

                self.setFechaFinProceso( self.fDateTimeNow())
                self.setHaCompletadoConExito( unInformeIdiomasEllaborated and unInformeModulosEllaborated)
                
                unCatalogo.setUltimoInforme( self)
    
                transaction.commit( )
    
                logging.getLogger( 'gvSIGi18n::fElaborarInforme').info("COMMIT") 
            return True
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
 
             
       
    
    

    security.declareProtected( permissions.View, 'fAutoUpdateIfNeeded')
    def fAutoUpdateIfNeeded( self, 
        theForceEllaboration        =False, 
        theCheckPermissions         =False, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):
        """Generate the report if it has never been generated, or if it is auto-updatable and enough time has lapsed.
        
        """
        unExecutionRecord = self.fStartExecution( 'method',  'fAutoUpdateIfNeeded', theParentExecutionRecord, False) 
        
        try:
        
            if ( self.getEstadoProceso() == 'Activo') and not theForceEllaboration:
                return False
            
            unaUltimaFechaInforme = None
            if self.getHaComenzado() and self.getHaCompletadoConExito():
                unaUltimaFechaInforme =  self.getFechaFinProceso()
                
            if unaUltimaFechaInforme:
                unMinimoIntervaloActualizacionEnMinutos = self.getMinimoIntervaloActualizacionEnMinutos()
                if unMinimoIntervaloActualizacionEnMinutos and ( int(( self.fMillisecondsNow() - unaUltimaFechaInforme.millis()) / 60000) < unMinimoIntervaloActualizacionEnMinutos):
                    return False
                
            self.fElaborarInforme( 
                theForceEllaboration        = True, 
                theCheckPermissions         = theCheckPermissions, 
                thePermissionsCache         = thePermissionsCache, 
                theRolesCache               = theRolesCache, 
                theParentExecutionRecord    = unExecutionRecord)
        
            return True
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
             
        
        

    
    
        
        
    security.declareProtected( permissions.View, 'fInformeIdiomas')
    def fInformeIdiomas( self, 
        theForceEllaboration        =False, 
        theCheckPermissions         =False, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):
        """Lazy access the Languages report.
        
        Generate if never generated, or give a chance to update if auto-updatable.
        
        Create report objects structure from the instance stored internally as the content of a string field.
        """
                         
        unExecutionRecord = self.fStartExecution( 'method',  'fInformeIdiomas', theParentExecutionRecord, False) 
        
        try:
        
            unDummy = self.fAutoUpdateIfNeeded( 
                theForceEllaboration, 
                theCheckPermissions, 
                thePermissionsCache, 
                theRolesCache, 
                unExecutionRecord,
            )
    
            unInformeIdiomasString = self.getInformeIdiomas()
            if not unInformeIdiomasString:
                return None
                
            unInformeIdiomas = None
            try:
                unInformeIdiomas = eval( unInformeIdiomasString)
            except:
                None
            return unInformeIdiomas
        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
             
                 
    
    
    
    
       
        
    security.declareProtected( permissions.View, 'fInformeModulos')
    def fInformeModulos( self,
        theForceEllaboration        =False, 
        theCheckPermissions         =False, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):                        
        """Lazy access the Modules report.
        
        Generate if never generated, or give a chance to update if auto-updatable.
        
        Create report objects structure from the instance stored internally as the content of a string field.
        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fInformeModulos', theParentExecutionRecord, False) 
        
        try:
        
            unDummy = self.fAutoUpdateIfNeeded( 
                theForceEllaboration, 
                theCheckPermissions, 
                thePermissionsCache, 
                theRolesCache, 
                unExecutionRecord,
            )
    
            unInformeModulosString = self.getInformeModulos()
            if not unInformeModulosString:
                return None
                
            unInformeModulos = None
            try:
                unInformeModulos = eval( unInformeModulosString)
            except:
                None
            return unInformeModulos
             

        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
             
        

    



