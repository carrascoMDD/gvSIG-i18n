# -*- coding: utf-8 -*-
#
# File: TRAInforme_Operaciones.py
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

from TRAElemento_Permission_Definitions import cBoundObject
from TRAElemento_Permission_Definitions_UseCaseNames import cUseCase_EllaborateInformeModulesAndLanguages, cUseCase_CreateTRAInforme

from TRAArquetipo import TRAArquetipo


class TRAInforme_Operaciones:
    """
    """
    security = ClassSecurityInfo()
     



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
            'label'   : self.fTranslateI18N( 'plone', 'By Languages', 'By Languages-',),
            'href'    : '%s/TRAInforme_Idiomas/' % unaURL,
            'icon'    : '',
            'domain'  : 'plone',
            'msgid'   : 'By Languages',
        })
        unosExtraLinks.append( unExtraLink)
                            
        unExtraLink = self.fNewVoidExtraLink()
        unExtraLink.update( {
            'label'   : self.fTranslateI18N( 'plone', 'By Modules', 'By Modules-',),
            'href'    : '%s/TRAInforme_Modulos/' % unaURL,
            'icon'    : '',
            'domain'  : 'plone',
            'msgid'   : 'By Modules',
        })
        unosExtraLinks.append( unExtraLink)
                            

        return unosExtraLinks
    
    
        
    
    
    
    
    
    
    
    
    
    security.declareProtected( permissions.ModifyPortalContent, 'fElaborarInforme')
    def fElaborarInforme( self, 
        theUseCaseQueryResult       =None,
        theForceEllaboration        =False, 
        theCheckPermissions         =False, 
        thePermissionsCache         =None, 
        theRolesCache               =None, 
        theParentExecutionRecord    =None):
        """Generate the report by delegating in the TRACatalogo.
        
        """
        
       
        unExecutionRecord = self.fStartExecution( 'method',  'fElaborarInforme', theParentExecutionRecord, False) 
        
        from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import  fReprAsString, fDateTimeNow

        try:
            if ( not theForceEllaboration) and self.getHaComenzado():
                return False
            
            unPermissionsCache = fDictOrNew( thePermissionsCache)
            unRolesCache       = fDictOrNew( theRolesCache)
               
            
            if theCheckPermissions:
                if ( not theUseCaseQueryResult) or ( not theUseCaseQueryResult.get( 'success', False)) or not ( theUseCaseQueryResult.get( 'use_case_name', '') in [ cUseCase_EllaborateInformeModulesAndLanguages, cUseCase_CreateTRAInforme, ]):
                    
                    unUseCaseQueryResult = self.fUseCaseAssessment(  
                        theUseCaseName          = cUseCase_EllaborateInformeModulesAndLanguages,        
                        theElementsBindings     = { cBoundObject: self,},                                    
                        theRulesToCollect       = None,
                        thePermissionsCache     = unPermissionsCache,                                        
                        theRolesCache           = unRolesCache,                                              
                        theParentExecutionRecord= unExecutionRecord,                                          
                    )
                    if ( not unUseCaseQueryResult) or not unUseCaseQueryResult.get( 'success', False):
                        return False
                 
    
            unCatalogo = self.getCatalogo()
            if unCatalogo == None:
                self.setInformeExcepcion( "No containing Catalog found - possibly an instance of TRAInforme that has not been properly created")
                return False
    
     
            unMemberId = self.fGetMemberId()                
            unAhora    = fDateTimeNow()
            
            self.setHaComenzado( True)
            self.setEstadoProceso( 'Activo')
            self.setUsuarioInformador( unMemberId)
            self.setFechaComienzoProceso( unAhora)
            self.setHaCompletadoConExito( False)
            
            self.setInformeExcepcion( '')
            self.setInformeExcepcionIdiomas( '')
            self.setInformeExcepcionModulos( '')
             
            unInformeIdiomasEllaborated = False
            unInformeModulosEllaborated = False
                            
            try:

                unInformeIdiomas = unCatalogo.fElaborarInformeIdiomas( 
                    theCheckPermissions         =False, 
                    thePermissionsCache         =unPermissionsCache, 
                    theRolesCache               =unRolesCache, 
                    theParentExecutionRecord    =unExecutionRecord,
                )

                if not unInformeIdiomas:
                    unInformeExceptionIdiomas = "No Languages Report produced from Catalog - possibly an error in the reporting process."
                else:
                    unInformeExceptionIdiomas = unInformeIdiomas.get( 'exception', '')
                    
                if unInformeExceptionIdiomas:
                    self.setInformeExcepcionIdiomas( unInformeExceptionIdiomas)
                    self.setInformeExcepcion( "Exception during Languages Report Generation")
                     
                if unInformeIdiomas.get( 'success', False):
                    unInformeIdiomas[ 'report_date'] = self.fDateTimeToString( fDateTimeNow())
                    unInformeIdiomasString = ''
                    try:
                        unInformeIdiomasString = fReprAsString( unInformeIdiomas)
                    except:
                        None
                    if not unInformeIdiomasString:
                        self.setInformeExcepcionIdiomas( "Error converting Report to a String representation")
                        self.setInformeExcepcion( "Exception during Languages Report storage")
                        return False
                    
                    self.setInformeIdiomas( unInformeIdiomasString)
                    unInformeIdiomasEllaborated = True

                    
                    
                
                unInformeModulos = unCatalogo.fElaborarInformeModulos( 
                    theCheckPermissions         =False, 
                    thePermissionsCache         =unPermissionsCache, 
                    theRolesCache               =unRolesCache, 
                    theParentExecutionRecord    =unExecutionRecord,
                )

                if not unInformeModulos:
                    unInformeExceptionModulos = "No Modules Report produced from Catalog - possibly an error in the reporting process."
                else:
                    unInformeExceptionModulos = unInformeModulos.get( 'exception', '')

                if unInformeExceptionModulos:
                    self.setInformeExcepcionModulos( unInformeExceptionModulos)
                    self.setInformeExcepcion( "Exception during Modules Report Generation")
                     
                if unInformeModulos.get( 'success', False):
                    unInformeModulos[ 'report_date'] = self.fDateTimeToString( fDateTimeNow())
                    unInformeModulosString = ''
                    try:
                        unInformeModulosString = fReprAsString( unInformeModulos)
                    except:
                        None
                    if not unInformeModulosString:
                        self.setInformeExcepcionModulos( "Error converting Report to a String representation")
                        self.setInformeExcepcion( "Exception during Languages Report storage")
                        return False
              
                
                    self.setInformeModulos( unInformeModulosString)
                    unInformeModulosEllaborated = True
                
                    
                    
                self.setEstadoProceso( 'Inactivo')

                self.setFechaFinProceso( fDateTimeNow())
                
                self.pFlushCachedTemplates()
                
                unHaCompletadoConExito = unInformeIdiomasEllaborated and unInformeModulosEllaborated
                self.setHaCompletadoConExito( unHaCompletadoConExito)
                    
                return True
            
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fElaborarInforme\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                   
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
                
                return False

        
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
 
             
       
    
    
        
        

    
    
        
        
    security.declareProtected( permissions.View, 'fInformeIdiomas')
    def fInformeIdiomas( self,):
        """Create report objects structure from the instance stored internally as the content of a string field.
        
        """
                         
        unInformeString = self.getInformeIdiomas()
                
        unInforme = self.fEvalString( unInformeString)
        return unInforme
        
             
                 
    
    
    
    
       
        
    security.declareProtected( permissions.View, 'fInformeModulos')
    def fInformeModulos( self,):                        
        """Create report objects structure from the instance stored internally as the content of a string field.
        
        """
        
        unInformeString = self.getInformeModulos()
                
        unInforme = self.fEvalString( unInformeString)
        return unInforme
        
    

    



