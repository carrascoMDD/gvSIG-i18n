# -*- coding: utf-8 -*-
#
# File: TRAColeccionProgresos_Operaciones.py
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
#

__author__ = """Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana <gvSIGi18n@gvSIG.org>, 
Model Driven Development sl <gvSIGi18n@ModelDD.org>,
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.gvSIGi18n.config import *

##code-section module-header #fill in your manual code here

import sys
import traceback
import logging

import transaction

from Products.CMFCore       import permissions
from Products.CMFCore.utils  import getToolByName



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


from TRAProgressHandler import TRAProgressHandler



##/code-section module-header



##code-section after-local-schema #fill in your manual code here



##/code-section after-local-schema



##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRAColeccionProgresos_Operaciones:
    """
    """
    security = ClassSecurityInfo()

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    
    
        

    security.declarePrivate( 'pAllSubElements_into')    
    def pAllSubElements_into( self, theCollection, theAdditionalParams=None):
        if theCollection == None:
            return self
        theCollection.append( self)
        
        
        unosElementos = self.fObtenerTodosProgresos()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pAllSubElements_into( theCollection,theAdditionalParams=theAdditionalParams)
        
        return self
            
    
    



    security.declarePrivate( 'pForAllElementsDo_recursive')    
    def pForAllElementsDo_recursive( self, theLambda):
        if not theLambda:
            return self
        
        theLambda( self)

        unosElementos = self.fObtenerTodosProgresos()
        if unosElementos:
            for unElemento in unosElementos:
                unElemento.pForAllElementsDo_recursive( theLambda)
        
        return self
            
            
        
        
        
    
    security.declareProtected( permissions.View, 'fObtenerTodosProgresos')
    def fObtenerTodosProgresos( self, ):
        """Retrieve all contained elements of type TRAProgreso.
        
        """
        unosElementos = self.fObjectValues( cNombreTipoTRAProgreso) 
        return unosElementos
         
          
    
                             
    
    
    
    
    
    
    
    
    
    

    
    
    # ###########################################################
    """Instantiate control object structures for the progress of a long-lived process.
    
    """      
    
    
    
    security.declarePrivate( 'fCreateNewProgressForElement')
    def fCreateNewProgressForElement( self, 
        theInitialElement       =None, 
        theProcessType          ='', 
        theInputParameters      =None,
        theTimestamp            ='',
        theResult               =None,     
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None,):
 
        return self.fCreateNewProgressAndOptionallyHandlerForElement(
            theCreateHandler        =False,
            theInitialElement       =theInitialElement, 
            theProcessType          =theProcessType, 
            theInputParameters      =theInputParameters,
            theTimestamp            =theTimestamp,
            theResult               =theResult,     
            theInitializeLambda     =None,
            theLoopLambda           =None,
            theElementLambda        =None,
            theFinalizeLambda       =None,
            theLockCatalog          =False,
            thePermissionsCache     =thePermissionsCache, 
            theRolesCache           =theRolesCache, 
            theParentExecutionRecord=theParentExecutionRecord,
        )
    

    
    
        
        
    security.declarePrivate( 'fCreateNewProgressAndHandlerForElement')
    def fCreateNewProgressAndHandlerForElement( self, 
        theInitialElement       =None, 
        theProcessType          ='', 
        theInputParameters      =None,
        theTimestamp            ='',
        theResult               =None,     
        theInitializeLambda     =None,
        theLoopLambda           =None,
        theElementLambda        =None,
        theFinalizeLambda       =None,
        theLockCatalog          =False,
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None,):
         

        return self.fCreateNewProgressAndOptionallyHandlerForElement(
            theCreateHandler        =True,
            theInitialElement       =theInitialElement, 
            theProcessType          =theProcessType, 
            theInputParameters      =theInputParameters,
            theTimestamp            =theTimestamp,
            theResult               =theResult,     
            theInitializeLambda     =theInitializeLambda,
            theLoopLambda           =theLoopLambda,
            theElementLambda        =theElementLambda,
            theFinalizeLambda       =theFinalizeLambda,
            theLockCatalog          =theLockCatalog,
            thePermissionsCache     =thePermissionsCache, 
            theRolesCache           =theRolesCache, 
            theParentExecutionRecord=theParentExecutionRecord,
        )
    

            
    
    
        
        
    security.declarePrivate( 'fCreateNewProgressAndOptionallyHandlerForElement')
    def fCreateNewProgressAndOptionallyHandlerForElement( self, 
        theCreateHandler        =False,
        theInitialElement       =None, 
        theProcessType          ='', 
        theInputParameters      =None,
        theTimestamp            ='',
        theResult               =None,     
        theInitializeLambda     =None,
        theLoopLambda           =None,
        theElementLambda        =None,
        theFinalizeLambda       =None,
        theLockCatalog          =False,
        thePermissionsCache     =None, 
        theRolesCache           =None, 
        theParentExecutionRecord=None,):
 

        unExecutionRecord = self.fStartExecution( 'method',  'fCreateNewProgressAndOptionallyHandlerForElement', theParentExecutionRecord,  False, None, ) 
        
        unPermissionsCache = fDictOrNew( thePermissionsCache)
        unRolesCache       = fDictOrNew( theRolesCache)

    
        try:
 
            unResult = self.fNewVoidCreateProgressHandlerResult()
            
            if theInitialElement == None:
                return unResult
            
            if not theProcessType:
                return unResult
            
            if not ( theProcessType in cTRAProgress_ProcessTypes):
                return unResult

            if not theResult:
                return unResult  
            
            
            unCatalogoRaiz = self.getCatalogo()           
            if unCatalogoRaiz == None:
                return unResult
        
            
            someProgressSupportKinds = self.fProgressSupportKindsForProcessTypeOnTarget( theProcessType, theInitialElement)
            if not someProgressSupportKinds:
                return unResult
            theResult[ 'progress_support_kinds'] = someProgressSupportKinds
            

            someProgressControlParms = self.fNewProgressControlParmsForProcessType( theProcessType, someProgressSupportKinds, theInitialElement)
            if not someProgressControlParms:
                return unResult
            theResult[ 'progress_parameters'] = someProgressControlParms
            
            
            someProgressControlCounters = self.fNewVoidProgressControlCounters( )
            theResult[ 'progress_counters'] = someProgressControlCounters

                
            
            unElementTitle = theInitialElement.Title()
            unElementPath  = theInitialElement.fPhysicalPathString()
            unElementUID   = theInitialElement.UID()
            
            unElementMetaType = 'UnknownType'
            try:
                unElementMetaType = theInitialElement.meta_type
            except:
                unElementMetaType = theInitialElement.__class__.__name
            if not unElementMetaType:
                unElementMetaType = 'UnknownType'
            
                
            aMemberId = self.fGetMemberId()
   
                
            unNuevoTitle       = '%s on %s by %s at %s' % ( theProcessType, unElementTitle, aMemberId, theTimestamp, )
            unNuevoDescription = 'Progress on %s process\n on element %s\n with path %s\n by %s\n started at %s' % ( theProcessType, unElementTitle, unElementPath.replace( '/', '/ '), aMemberId, theTimestamp, )
            
            unaNuevaId = unNuevoTitle.lower()
            unaNuevaId = unaNuevaId.replace(" ", "-")
            unaNuevaId = unaNuevaId.replace(":", "-")
    
            aPloneTool = self.getPloneUtilsToolForNormalizeString()
            if aPloneTool:
                unaNuevaId = aPloneTool.normalizeString( unaNuevaId)  
            
            unNuevoTitleACrear = unNuevoTitle
            unaNuevaIdACrear   = unaNuevaId
            
            
            
            aNewProgresoAttrsDict = { 
                'title':             unNuevoTitleACrear,
                'description':       unNuevoDescription,
                'tipoProceso':       theProcessType,
                'clasesSoporte':     ' '.join( someProgressSupportKinds),
                'comienzoTipo':      unElementMetaType,
                'comienzoTitulo':    unElementTitle,
                'comienzoUID':       unElementUID,
                'comienzoRuta':      unElementPath,
                'usuarioInformador': aMemberId,
                'estadoProceso':     cTRAProgreso_EstadoProceso_Inactivo,
                'haComenzado':       False,
                'haCompletadoConExito': False,
                'fechaComienzoProceso': None,
                'fechaUltimoInformeProgreso': None,
            }
            
               
            unProgresoExistente = self.getElementoPorID( unaNuevaIdACrear)
            unCountIds = 0
            while not ( unProgresoExistente == None):
                unCountIds += 1
                unNuevoTitleACrear = '%s-%d' % ( unNuevoTitle, unCountIds)
                unaNuevaIdACrear = '%s-%d'   % ( unaNuevaId, unCountIds)
                
                unProgresoExistente = self.getElementoPorID( unaNuevaIdACrear)
                
                
            aNewProgresoAttrsDict.update( { 
                'title':         unNuevoTitleACrear,
            })
            
            unaIdNuevoProgreso = self.invokeFactory( cNombreTipoTRAProgreso, unaNuevaIdACrear, **aNewProgresoAttrsDict)
            if not unaIdNuevoProgreso:
                return unResult
                     
            unNuevoProgreso = self.getElementoPorID( unaIdNuevoProgreso)
            if  unNuevoProgreso == None:
                return unResult

            
            unNuevoProgreso.manage_fixupOwnershipAfterAdd()
          
            unNuevoProgreso.pSetPermissions()
            
            
            
            unNuevoProgreso.pSetParametrosEntrada( theInputParameters)
            unNuevoProgreso.pSetDatosResultado(    theResult)
            unNuevoProgreso.pSetParametrosControl( someProgressControlParms)
            unNuevoProgreso.pSetContadoresControl( someProgressControlCounters)
            
                        
            transaction.commit()
            
            unCatalogoRaiz.pFlushCachedTemplates_All()

            if cTRAProgress_LogLongLivedProcess:                
                aLogger = logging.getLogger( 'gvSIGi18n')
                aLogger.info( '\n\nCreated %s %s (%s) UID=%s\n' % ( unNuevoProgreso.meta_type, unNuevoProgreso.Title(), unNuevoProgreso.fPhysicalPathString(), unNuevoProgreso.UID(),))
                
                
              
                
                
            if not theCreateHandler:    
                
                unResult.update( {
                    'success':                          True,
                    'condition':                        '',
                    'progress_element':                 unNuevoProgreso,
                })
                return unResult
                
            
            
            
            
            aProgressHandler = TRAProgressHandler( 
                theInitialElement, 
                unNuevoProgreso, 
                theInputParameters,
                someProgressControlParms, 
                someProgressControlCounters, 
                theResult,
                theInitializeLambda,
                theLoopLambda,
                theElementLambda,
                theFinalizeLambda,
                theLockCatalog,
                theTimestamp,
            )              
            if not aProgressHandler:
                return unResult
            
            aProgressHandlerKey = aProgressHandler.fKey()
            if not aProgressHandlerKey:
                return unResult
            
            if not unNuevoProgreso.fRegisterProgressHandler( aProgressHandler):
                return unResult
            
            unResult.update( {
                'success':                          True,
                'condition':                        '',
                'progress_handler_key':             aProgressHandlerKey,
                'progress_handler':                 aProgressHandler,
                'progress_element':                 unNuevoProgreso,
            })
            
            return unResult
   
                    
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
           
                
         
            
         

    
        
    
    
      
    security.declarePrivate( 'fProgressSupportKindsForProcessTypeOnTarget')
    def fProgressSupportKindsForProcessTypeOnTarget( self, theProcessType, theElement):
        """Determines which capabilities are serviced to the progress of a long-lived process.
        
        """
        
        if not theProcessType:
            return []
        
        if not ( theProcessType in cTRAProgress_ProcessTypes):
            return []
        
        if theElement == None:
            return []
        
        anElement_MetaType = ''
        try:
            anElement_MetaType = theElement.meta_type
        except:
            None
        if not anElement_MetaType:
            return []
        
        someElementTypesAndSupportKinds = cTRAProgress_SupportKinds_ForProcessTypes.get( theProcessType, None)
        if not someElementTypesAndSupportKinds:
            return []

        aSupportKindsSet = set( )
        
        for anElementTypesAndSupportKinds in someElementTypesAndSupportKinds:
            someTypes = anElementTypesAndSupportKinds.get( 'types', [])
            if anElement_MetaType in someTypes:
                aSupportKinds = anElementTypesAndSupportKinds.get( 'support_kinds', [])
                if aSupportKinds:
                    aSupportKindsSet = aSupportKindsSet.union( set( aSupportKinds))
                
        
        someSupportKinds = sorted( aSupportKindsSet)
        
        return someSupportKinds
    
        
    


        
        
    security.declarePrivate( 'fNewProgressControlParmsForProcessType')
    def fNewProgressControlParmsForProcessType( self, theProcessType, theProgressSupportKinds, theElement, ):
        if not theProcessType:
            return {}
        
        if theElement == None:
            return {}
        
        if not ( theProcessType in cTRAProgress_ProcessTypes_NonVoid):
            return {}
        
        unaIdElementoParametrosControlProgreso = cTRAParametrosControlProgresoIDs_forProcessTypes.get( theProcessType, '')
        if not unaIdElementoParametrosControlProgreso:
            return {}
        
        unCatalogoRaiz = self.getCatalogo()    
        if unCatalogoRaiz == None:
            return {}
        
        
        unElementoParametrosControlProgreso = unCatalogoRaiz.getElementoPorID( unaIdElementoParametrosControlProgreso)
        if unElementoParametrosControlProgreso == None:
            return {}
     
        someProgressControlParms = self.fNewVoidProgressControlParms_All()
        
        unElementoParametrosControlProgreso.pInitDefaultProcessControlParms( theProcessType, someProgressControlParms, theProgressSupportKinds,)
        
        return someProgressControlParms
        

    
                    

        
                                

# end of class TRAColeccionProgresos_Operaciones

##code-section module-footer #fill in your manual code here
##/code-section module-footer



