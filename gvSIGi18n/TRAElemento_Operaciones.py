# -*- coding: utf-8 -*-
#
# File: TRAElemento_Operaciones.py
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


import cgi

import sys
import traceback

import logging

from logging import ERROR as cLoggingLevel_ERROR


from codecs                     import lookup   as CODECS_Lookup

from time                       import time, localtime

from DateTime                   import DateTime

from StringIO                   import StringIO

from AccessControl              import ClassSecurityInfo
from Acquisition                import aq_inner, aq_parent


from OFS.CopySupport            import CopyContainer


from Products.Archetypes.utils  import shasattr

from Products.CMFCore           import permissions

from Products.CMFCore.utils     import getToolByName


from Products.Archetypes.atapi  import OrderedBaseFolder, BaseBTreeFolder

from Products.PloneLanguageTool import availablelanguages as PloneLanguageToolAvailableLanguages


from Products.ModelDDvlPloneTool.ModelDDvlPloneTool import cModelDDvlPloneToolId, ModelDDvlPloneTool

from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport import fReprAsString, fMillisecondsNow, fDateTimeNow


from TRAElemento_Constants              import *

from TRAElemento_Permission_Definitions import cTRAUsersGroup_AllLanguages_postfix
    
from TRAImportarExportar_Constants      import cUTFEncodingsForAllLanguages, cDefaultEncodingsSourceMap, cWesternLanguageMarkInSourceMap, cEncodingSeparatorSentinelName
        


from TRAElemento_Permissions import TRAElemento_Permissions
from TRAElemento_Credits     import TRAElemento_Credits





def cfEncodeLogString( theContextualObject, theChangeDescriptionString, theTranslationService=None):
    if not theChangeDescriptionString:
        return ''
    
    aString = theChangeDescriptionString
    
    aTranslationService = theTranslationService
    if not aTranslationService:
        aTranslationService = getToolByName( theContextualObject, 'translation_service', None)
        
    if aTranslationService:
        unUnicodeString = aTranslationService.asunicodetype( theChangeDescriptionString, errors="ignore")        
    else:
        try:
            unUnicodeString = unicode( aString)    
        except:
            None
    
    if not unUnicodeString:
        return ''
    
    unEncodedString = unUnicodeString
    if aTranslationService:    
        unEncodedString = aTranslationService.encode( unUnicodeString, cProgramTextEncoding)
    else:
        try:
            unEncodedString = unUnicodeString.encode( cProgramTextEncoding)    
        except:
            None
            
    if not unEncodedString:
        return ''
            
    return unEncodedString



cCollapsibleBlock_open = """
            
    <!-- ######### Start collapsible  section ######### 
    # positional parameters: id, title, content 
    --> 
    <dl id="%s" class="collapsible inline collapsedInlineCollapsible">
        <dt class="collapsibleHeader">
            <strong>%s</strong>
        </dt>
        <dd class="collapsibleContent">   
   \n"""  


cCollapsibleBlock_forTimeProfiling_open = """
            
    <!-- ######### Start collapsible  section ######### 
    # positional parameters: id, title, content 
    --> 
    <dl id="%s" class="collapsible inline collapsedInlineCollapsible TRA_timeProfileWithchildren_refinePlone_dt_collapsibleHeader">
        <dt class="collapsibleHeader">
            <strong>%s</strong>
        </dt>
        <dd class="collapsibleContent">   
   \n"""  

cCollapsibleBlock_close = """
       </dd>
    </dl>
    <!-- ######### End collapsible  section ######### --> 
    \n"""  

# positional parameters: id, title, content 
cCollapsibleBlock = '%s%%s%s' % ( cCollapsibleBlock_open, cCollapsibleBlock_close,) 


   






# ########################################################################################################
    
# ACV 20090328 still unused
#class TRAExecutionContext:
    #"""Keep a context shared over the execution to respond to a user request.
    
    #"""
    
    
    
    #def __init__( self, theContextualObject=None, theExecutedKind=None, theExecutedName=None, theConfigsByAspect=None):
        #"""Instantiate and initialize the context shared over the whole execution to respond to the current connected user request.
        
        #Flag as initialized.
        #Keep reference to the initial contextual object, and artefact invoked.
        #Keep configuration information about the configurable aspects weaved in the execution. This is an open ended set, including for example security, logging, and results caching.
        
        
        #"""
        
        #try:
            #self.vInitialized           = True
            
            #self.vContextualObject      = theContextualObject
            #self.vExecutedKind          = theExecutedKind # method or template
            #self.vExecutedName          = theExecutedName
            
            #self.vConfigsByAspect       = theConfigsByAspect
            
            #self.vForPermissions        = { 
                #'permissions_cache':    { },
                #'roles_cache':          { },
            #}                                        
                
            #unNewExecutionRecord = None            
            #if cTimeStampingEnabled or cTimeProfilingEnabled:
                #if theConfigsByAspect:
                    #aProfilingInitialConfig = theConfigsByAspect.get( cProfilingAspect, None)
                #else:
                    #aProfilingInitialConfig = None
                #unNewExecutionRecord = TRAExecutionRecord( theContextualObject, theExecutedKind, theExecutedName, aProfilingInitialConfig)
                
            #self.vForProfiling          =  {
                #'root_execution_record':    unNewExecutionRecord,
                #'current_execution_record': unNewExecutionRecord,
            #}

            #self.vUseCaseAssessmentResults   = { }
            
            #self.vTypeConfigRetrievalResults = [ ] 

            #return None
        
        #except:
            #None

        

            
            
            
            
            
            
            
# ########################################################################################################
            
class TRAExecutionRecord:
    """Record the execution of each relevant template or method.
        
    """
    
    def __init__( self, theContextualObject, theExecutedKind, theExecutedName, theParentExecutionRecord, theProfilingConfig={}, theExtraExecutionInfo=''):
        
        self.vIsExecutionLoggingEnabled = False
        self.vIsDetailedExecutionLoggingEnabled = False
        self.vInitialized           = False
        self.vIsExcluded            = False
        self.vExtraExecutionInfo    = None
        self.vContextualObject      = None
        self.vContextualObjectClassName = None
        self.vContextualObjectPath = None
        self.vContextualObjectTitle = None
        self.vExecutedKind          = None
        self.vExecutedName          = None
        self.vDetailLevel           = None
        self.vExecutionStartTime    = None
        self.vExecutionEndTime      = None
        self.vParent                = None
        
        self.vChildren              = None
        self.vProfilingConfig       = None
        self.vExceptions            = None
        self.vLogged                = False
        self.vExceptionsInChildren  = False
        
        
        
        
        try:
            
            if not ( theContextualObject == None):
                self.vIsExecutionLoggingEnabled = theContextualObject.getCatalogo().fIsExecutionLoggingEnabled()
                self.vIsDetailedExecutionLoggingEnabled = theContextualObject.getCatalogo().fIsDetailedExecutionLoggingEnabled()
            
            if cTimeStampingEnabled or cTimeProfilingEnabled:
                
                self.vInitialized           = True

                self.vIsExcluded            = False
                
                self.vExtraExecutionInfo    = []
                if theExtraExecutionInfo:
                    self.vExtraExecutionInfo.append( str( theExtraExecutionInfo))
                
                self.vContextualObject      = theContextualObject
                if not ( theContextualObject == None):
                    self.vContextualObjectClassName = theContextualObject.__class__.__name__
                    self.vContextualObjectPath      = theContextualObject.fDisplayPathString()
                    try:
                        self.vContextualObjectTitle = theContextualObject.Title()
                    except:
                        None
                else:
                    self.vContextualObjectClassName = 'unknown contextual object'
                    self.vContextualObjectPath      = 'unknown contextual object'
                    self.vContextualObjectTitle     = 'unknown contextual object'
                    
                self.vExecutedKind          = '' # method or template
                self.vExecutedName          = ''
                self.vDetailLevel           = -1
                self.vExecutionStartTime    = 0
                self.vExecutionEndTime      = 0
                self.vParent                = None
                
                self.vChildren              = [ ]
                self.vProfilingConfig       = { }
                self.vExceptions            = [ ]
                self.vLogged                = False
                self.vExceptionsInChildren  = False


            if cTimeStampingEnabled:
                self.vExecutionStartTime    = int( time() * 1000)
            
            if cTimeProfilingEnabled:
                
                if not theParentExecutionRecord or not theParentExecutionRecord.vIsExcluded:
                    
                    if theExecutedName in self.vProfilingConfig.get( 'excluded', []):
                        self.vIsExcluded = True       
                    else:
                        if theParentExecutionRecord and ( theParentExecutionRecord.__class__.__name__ == self.__class__.__name__):
                            theParentExecutionRecord.addChild( self)
                            if ( theParentExecutionRecord.vProfilingConfig or {}).get( 'log_what', ''):
                                self.vProfilingConfig[ 'log_what'] =  theParentExecutionRecord.vProfilingConfig[ 'log_what']   
                            
                        self.vExecutedKind          = theExecutedKind
                        self.vExecutedName          = theExecutedName
                        
                        if theProfilingConfig and ( theProfilingConfig.__class__.__name__ == 'dict'):
                            self.vProfilingConfig.update( theProfilingConfig)
                                 
            return None
        
        except:
            None
    
              
    
    def addExtraInfo( self, theExtraExecutionInfo):
        if not self.vInitialized or not theExtraExecutionInfo:
            return self
        
        if self.vExtraExecutionInfo == None:
            self.vExtraExecutionInfo = [ ]
        
        self.vExtraExecutionInfo.append( theExtraExecutionInfo)
        
        return self 
    

    
    
    def addChild( self, theChild):
        if not self.vInitialized or not theChild:
            return self
        
        if self.vChildren == None:
            self.vChildren = [ ]
        
        self.vChildren.append( theChild)
        theChild.vParent = self
        
        return self
    
        
        

    
        
    def pEndExecution( self,  ):
        """Pop stack and write log.
        """
        
        try:
            if not self.vInitialized:
                return self
            
            if cTimeStampingEnabled:
                self.vExecutionEndTime  =  int( time() * 1000)
            
            if cTimeProfilingEnabled:
                self.pLogPerformance( )
                    
            return self   
        
        except:
            None


    def pRecordExceptionInChildren( self):
        self.vExceptionsInChildren = True
        if self.vParent:
            self.vParent.pRecordExceptionInChildren()
        return self
    
        
    
    
    def pRecordException( self,  theExceptionReport):
        """Record an exception report trapped in this execution.
        """
        
        try:
            
            if self.vParent:
                self.vParent.pRecordExceptionInChildren()
            
            if not theExceptionReport:
                return None
            
            if not self.vExceptions:
                self.vExceptions = [ ]
                
            self.vExceptions.append( theExceptionReport)
            
            return self   
        
        except:
            None
          
        return self
    
    
            
          
    def pLogPerformance( self, ):
        """Write to the log a representation of this ExecutionRecord and its children.
        
        theWhenToLog optional values in [
            None or False == do not log,
            True == log now,
            'root' == log if element has no parent
        ]
        
        """
        
        try:
            if not self.vInitialized:
                return self
            
            if self.vIsExecutionLoggingEnabled:
                aWhenToLog = self.vProfilingConfig.get( 'log_when', False)
                if aWhenToLog == True or ( ( aWhenToLog == 'root') and not self.vParent):
                    
                    if self.vProfilingConfig.get( 'log_what', '') == 'details' and self.vIsDetailedExecutionLoggingEnabled:
                        unPrintString = self.fPrintStringDetails( True)
                        if unPrintString:
                            unPrintString = '\n' + unPrintString
                    elif self.vIsDetailedExecutionLoggingEnabled and self.vProfilingConfig.get( 'log_what', '') == 'dots':
                        unPrintString = self.fPrintStringDots( True)
                    else:
                        unPrintString = self.fPrintString( )
    
                    if not unPrintString:
                        return self
                    
                    unEncodedString = cfEncodeLogString( self.vContextualObject, unPrintString)
                    logging.getLogger( 'gvSIGi18n::execution').info( unEncodedString)
                    
                    self.setLoggedRecursive( True)
    
            return self
        
        except:
            None

    
    

    
    
    
    
    
    
    def setLoggedRecursive( self, theLogged=True):

        try:
            if not self.vInitialized:
                return self
            
            if self.vLogged:
                return self
            
            self.vLogged = theLogged == True
            for unChild in ( self.vChildren or []):
                unChild.setLoggedRecursive( theLogged == True)
            
            return self
        
        except:
            None

    
        
    
    
    def pClearLoggedAll( self,):

        try:
            if not self.vInitialized:
                return self
            
            self.vLogged = False
            for unChild in ( self.vChildren or []):
                unChild.pClearLoggedAll( )
            
            return self
        
        except:
            None

    


        

    def fPrintString(self, ):

        try:
            if self.vInitialized:
                return '%d ms %s %s %s %s %s %s %s' % (      
                    self.vExecutionEndTime - self.vExecutionStartTime, 
                    ( self.vExceptions and '!!!') or '',
                    self.vExecutedKind or 'unknown_executed_kind', 
                    self.vExecutedName or 'unknown_executed_name', 
                    self.vContextualObjectClassName or 'unknown_object_class_name',
                    self.vContextualObjectTitle or 'unknown_object_title',
                    self.vContextualObjectPath   or 'unknown_object_path',
                    ' '.join( self.vExtraExecutionInfo or []),
                )
        except:
            None    
        
        return 'exception printing execution record'
    

            

    
    def fPrintStringDots(self,):

        try:
            if not self.vInitialized:
                return self
            
            theOutput = StringIO()
            
            self.pPrintDotsOn( theOutput,)
       
            unString = theOutput.getvalue()
            return unString
        
        except:
            None

    
    
    
    
    
    def fPrintStringDetails(self, theIsForLog=False):

        try:
            if not self.vInitialized:
                return self
            
            theOutput = StringIO()
            
            unaTimeWidth = len( str( ( self.vExecutionEndTime or  self.vExecutionStartTime) - self.vExecutionStartTime))
            self.pPrintDetailsOn( theOutput, theIsForLog, '', unaTimeWidth)
       
            unString = theOutput.getvalue()
            return unString
        
        except:
            None

            
            

            
      
    
    

    def pPrintDotsOn(self, theOutput):
        if not self.vInitialized:
            return self
        
        theOutput.write( '.')
        for unChild in ( self.vChildren or []):
            unChild.pPrintDotsOn( theOutput)
        return self      
       
    
              
            
            
                 
    
    def pPrintDetailsOn(self, theOutput,  theIsForLog=False, theIndentString='', theMaxTimeWidth=0):
        if not self.vInitialized:
            return self
        
        if theIsForLog and self.vLogged:
            return self
       
        if theIndentString:
            theOutput.write(  theIndentString)
        
            
        unExecutedKind    = self.vExecutedKind or 'unknown_executed_kind'
        unExecutedName    = self.vExecutedName or 'unknown_executed_name'
        unExecTime        = self.vExecutionEndTime - self.vExecutionStartTime
        someSubResults    = self.vChildren or []

        unTimeFiller = ' ' * ( theMaxTimeWidth - len( str( unExecTime)))
            
        if not someSubResults:
            if not self.vExceptions:
                theOutput.write( '[%s%s]\n' % ( unTimeFiller, self.fPrintString())) 
            else:
                theOutput.write( '[%s%s\n' % ( unTimeFiller, self.fPrintString())) 
                for unaException in self.vExceptions:
                    theOutput.write( '%s%s%s\n' % ( theIndentString, str( unaException))) 
                    
                
        else:
            theOutput.write( '[%s%s\n' % ( unTimeFiller, self.fPrintString()))     
            
            if self.vExceptions:
                for unaException in self.vExceptions:
                    theOutput.write( '%s%s%s\n' % ( theIndentString, str( unaException))) 
                
            
            unAllChildrenAlreadyLogged = len( [ aChild for aChild in someSubResults if aChild.vLogged ]) == len( someSubResults)
            
            if unAllChildrenAlreadyLogged:
                theOutput.write( "Children already logged before")
                
            unosSubTiempos = [ unSub.vExecutionEndTime - unSub.vExecutionStartTime for unSub in someSubResults]
            unaSumaTiempos = sum( unosSubTiempos)
            unMaxSubTiempo = max( [ ( unExecTime - unaSumaTiempos),] + unosSubTiempos)
            unaLenSubTiempos = len( str( unMaxSubTiempo))
            
            unIndentString = theIndentString + ( ' ' * ( theMaxTimeWidth + 1))

            if unaSumaTiempos < unExecTime:
                theOutput.write(  unIndentString)
                unOwnTimeFiller = ' ' * (( theMaxTimeWidth - len( str( unExecTime - unaSumaTiempos))) + 1)
                theOutput.write( '%s%d ms -own-\n' % ( unOwnTimeFiller, unExecTime - unaSumaTiempos))            
                         
            for aSubProfilingResult in someSubResults:                       
                aSubProfilingResult.pPrintDetailsOn( theOutput, theIsForLog, unIndentString, unaLenSubTiempos)
                
            if theIndentString:
                theOutput.write(  theIndentString)
            theOutput.write( ']\n')            
        
        return self      
       
               
                     


    
    
    
    
    
    
    
            
# ########################################################################################################
    
class TRAElemento_Operaciones( TRAElemento_Permissions, TRAElemento_Credits):
    """CLASS: base class for all application elements, with commonly used behaviours aand service access points
        
    """
    
    security = ClassSecurityInfo()

    
    
   
    
    security.declarePrivate( 'fNewVoidRecatalogResult')
    def fNewVoidRecatalogResult( self, ):
        unResult = {
            'success':                  False,
            'total_elements_traversed': 0,
            'elements_by_type_dict':    { },
            'elements_by_type':         [ ],
        }
        return unResult
        
    
    
    

    security.declareProtected( permissions.ManagePortal, 'fRecatalogAllElements')
    def fRecatalogAllElements( self, theAdditionalParms=None):

        aRecatalogResult = self.fNewVoidRecatalogResult()
        
        if cLogRecatalogProgress:
            aRecatalogResultDump = self.fRecatalogResult_dump( aRecatalogResult)
            
            aLogger = logging.getLogger( 'gvSIGi18n')
            aLogger.info( '\n\nSTARTED %s' % aRecatalogResultDump)
            
        
        unPortalCatalog = getToolByName( self, 'portal_catalog')

         
        unCatalogoRaiz = self.getCatalogo()           
        unCatalogBusquedaCadenas       = unCatalogoRaiz.fCatalogBusquedaCadenas() 
        unCatalogFiltroCadenas         = unCatalogoRaiz.fCatalogFiltroCadenas() 
        unCatalogTextoCadenas          = unCatalogoRaiz.fCatalogTextoCadenas() 
        
        todosIdiomas = [ ]
        unasColeccionesIdiomas = self.fObtenerTodasColeccionesIdiomas()
        if unasColeccionesIdiomas:
            for unaColeccionIdiomas in unasColeccionesIdiomas:
                unosIdiomas = unaColeccionIdiomas.fObtenerTodosIdiomas()
                if unosIdiomas:
                    todosIdiomas.extend( unosIdiomas)
                
                
        unosCatalogsBusquedaTraduccionesPorIdioma = { }
        unosCatalogsFiltroTraduccionesPorIdioma   = { }
        unosCatalogsTextoTraduccionesPorIdioma    = { }
        for unIdioma in todosIdiomas:
            if not( unIdioma == None):
                unCodigoIdioma = unIdioma.getCodigoIdiomaEnGvSIG()
                if unCodigoIdioma:
                    unosCatalogsBusquedaTraduccionesPorIdioma[ unCodigoIdioma] = unCatalogoRaiz.fCatalogBusquedaTraduccionesParaIdioma( unIdioma)
                    unosCatalogsFiltroTraduccionesPorIdioma[   unCodigoIdioma] = unCatalogoRaiz.fCatalogFiltroTraduccionesParaIdioma(   unIdioma)
                    unosCatalogsTextoTraduccionesPorIdioma[    unCodigoIdioma] = unCatalogoRaiz.fCatalogTextoTraduccionesParaIdioma(    unIdioma)
            
                    
        unosCatalogs = {
            'PortalCatalog':        unPortalCatalog,
            'BusquedaCadenas':      unCatalogBusquedaCadenas,
            'FiltroCadenas':        unCatalogFiltroCadenas,
            'TextoCadenas':         unCatalogTextoCadenas,
            'BusquedaTraducciones': unosCatalogsBusquedaTraduccionesPorIdioma,
            'FiltroTraducciones':   unosCatalogsFiltroTraduccionesPorIdioma,
            'TextoTraducciones':    unosCatalogsTextoTraduccionesPorIdioma,
        }
            
        
        
        def fRecatalogElement_lambda( theElement, theRecatalogResult, theCatalogs, theAdditionalParmsHere):        
        
            theRecatalogResult [ 'total_elements_traversed'] += 1
            
            aMetaType = 'UnknownType'
            try:
                aMetaType = theElement.meta_type
            except:
                aMetaType = theElement.__class__.__name
            if not aMetaType:
                aMetaType = 'UnknownType'
                
            aNumElementsOfType = theRecatalogResult[ 'elements_by_type_dict'].get( aMetaType, 0)
            aNumElementsOfType += 1
            theRecatalogResult[ 'elements_by_type_dict'][ aMetaType] = aNumElementsOfType
            
            if aMetaType == cNombreTipoTRATraduccion:
                unCodigoIdioma = theElement.getCodigoIdiomaEnGvSIG()
                theElement.pAddToCatalogs( theCatalogs.get( 'BusquedaTraducciones', {}).get( unCodigoIdioma),  theCatalogs.get( 'FiltroTraducciones', {}).get( unCodigoIdioma),  theCatalogs.get( 'TextoTraducciones', {}).get( unCodigoIdioma), None)
            
            elif aMetaType == cNombreTipoTRACadena:
                theElement.pAddToCatalogs( theCatalogs.get( 'BusquedaCadenas', None),  theCatalogs.get( 'FiltroCadenas', None),  theCatalogs.get( 'TextoCadenas', None),)
                
            else:
                theElement.reindexObject()
                
                
            if cLogRecatalogProgress and not( theRecatalogResult [ 'total_elements_traversed'] % cLogRecatalogProgressInterval):
                aRecatalogResultDump = theElement.fRecatalogResult_dump( theRecatalogResult)
                
                aLogger = logging.getLogger( 'gvSIGi18n')
                aLogger.info( '\n\nPROGRESS of %s' % aRecatalogResultDump)
                
            
            return None        
        
        
        
        self.pForAllElementsDo( lambda theElement: fRecatalogElement_lambda( theElement, aRecatalogResult, unosCatalogs, theAdditionalParms))
        
        someMetaTypes =  aRecatalogResult[ 'elements_by_type_dict'].keys()
        someMetaTypes = sorted( someMetaTypes)
        for aMetaType in someMetaTypes:
            aRecatalogResult[ 'elements_by_type'].append( [ aMetaType, aRecatalogResult[ 'elements_by_type_dict'][ aMetaType],])
            
        aRecatalogResult [ 'success'] = True
        
        if cLogRecatalogResult:
            aRecatalogResultDump = self.fRecatalogResult_dump( aRecatalogResult)
            
            aLogger = logging.getLogger( 'gvSIGi18n')
            aLogger.info( '\n\nCOMPLETED %s' % aRecatalogResultDump)
    
        return aRecatalogResult
    
    
      


    security.declarePrivate( 'fRecatalogResult_dump')
    def fRecatalogResult_dump( self, theRecatalogResult):
        
        if not theRecatalogResult:
            return 'NO RecatalogResult'
        
        aStringIO = StringIO()
        
        aStringIO.write( """RecatalogResult\n""")
        aStringIO.write( """Success: %s\n""" % theRecatalogResult .get( 'success', False))
        aStringIO.write( """total_elements_traversed: %s\n""" % theRecatalogResult .get( 'total_elements_traversed', 0))

        aStringIO.write( """\nType: #elems.\n""")
        
        someElementsByTypeDict = theRecatalogResult.get( 'elements_by_type_dict', [])
        
        for aMetaType in sorted( someElementsByTypeDict.keys()):
            aNumElements = someElementsByTypeDict.get( aMetaType, 0)
            aStringIO.write( """%s : %d\n""" % (aMetaType, aNumElements))
            
        aStringIO.write( """\n\n""")
            
        aDumpString = aStringIO.getvalue()
        return aDumpString
      
        
    
    
   
    
    security.declarePrivate( 'fNewVoidInventoryResult')
    def fNewVoidInventoryResult( self, ):
        unResult = {
            'success':                  False,
            'total_elements_traversed': 0,
            'elements_by_type_dict':    { },
            'elements_by_type':         [ ],
        }
        return unResult
        
    
    
    

    security.declareProtected( permissions.ManagePortal, 'fInventory')
    def fInventory( self, theAdditionalParms=None):

        aInventoryResult = self.fNewVoidInventoryResult()
        
        if cLogInventoryProgress:
            aInventoryResultDump = self.fInventoryResult_dump( aInventoryResult)
            
            aLogger = logging.getLogger( 'gvSIGi18n')
            aLogger.info( '\n\nSTARTED %s' % aInventoryResultDump)
            
         
        def fInventoryElement_lambda( theElement, theInventoryResult, theAdditionalParmsHere):        
        
            theInventoryResult [ 'total_elements_traversed'] += 1
            
            aMetaType = 'UnknownType'
            try:
                aMetaType = theElement.meta_type
            except:
                aMetaType = theElement.__class__.__name
            if not aMetaType:
                aMetaType = 'UnknownType'
                
            aNumElementsOfType = theInventoryResult[ 'elements_by_type_dict'].get( aMetaType, 0)
            aNumElementsOfType += 1
            theInventoryResult[ 'elements_by_type_dict'][ aMetaType] = aNumElementsOfType
            
            if cLogInventoryProgress and not( theInventoryResult [ 'total_elements_traversed'] % cLogInventoryProgressInterval):
                aInventoryResultDump = theElement.fInventoryResult_dump( theInventoryResult)
                
                aLogger = logging.getLogger( 'gvSIGi18n')
                aLogger.info( '\n\nPROGRESS of %s' % aInventoryResultDump)
                
            
            return None        
        
        
        
        self.pForAllElementsDo( lambda theElement: fInventoryElement_lambda( theElement, aInventoryResult, theAdditionalParms))
        
        someMetaTypes =  aInventoryResult[ 'elements_by_type_dict'].keys()
        someMetaTypes = sorted( someMetaTypes)
        for aMetaType in someMetaTypes:
            aInventoryResult[ 'elements_by_type'].append( [ aMetaType, aInventoryResult[ 'elements_by_type_dict'][ aMetaType],])
            
        aInventoryResult [ 'success'] = True
        
        if cLogInventoryResult:
            aInventoryResultDump = self.fInventoryResult_dump( aInventoryResult)
            
            aLogger = logging.getLogger( 'gvSIGi18n')
            aLogger.info( '\n\nCOMPLETED %s' % aInventoryResultDump)
    
        return aInventoryResult
    
    
  
    

    security.declarePrivate( 'fInventoryResult_dump')
    def fInventoryResult_dump( self, theInventoryResult):
        
        if not theInventoryResult:
            return 'NO InventoryResult'
        
        aStringIO = StringIO()
        
        aStringIO.write( """InventoryResult\n""")
        aStringIO.write( """Success: %s\n""" % theInventoryResult .get( 'success', False))
        aStringIO.write( """total_elements_traversed: %s\n""" % theInventoryResult .get( 'total_elements_traversed', 0))

        aStringIO.write( """\nType: #elems.\n""")
        
        someElementsByTypeDict = theInventoryResult.get( 'elements_by_type_dict', [])
        
        for aMetaType in sorted( someElementsByTypeDict.keys()):
            aNumElements = someElementsByTypeDict.get( aMetaType, 0)
            aStringIO.write( """%s : %d\n""" % (aMetaType, aNumElements))
            
        aStringIO.write( """\n\n""")
            
        aDumpString = aStringIO.getvalue()
        return aDumpString
      
    
    
    
    
    
    security.declarePublic( 'fNewVoidExtraLink')    
    def fNewVoidExtraLink( self):
        unExtraLink = {
            'label'   : '',
            'href'    : '',
            'icon'    : '',
            'domain'  : '',
            'msgid'   : '',
        }
        return unExtraLink
        

    
    security.declarePublic( 'fExtraLinks')    
    def fExtraLinks( self):
        
        unosExtraLinks = [ ]
        
        unaURL = self.getCatalogo().absolute_url()
        if not unaURL:
            return unosExtraLinks
        
        unExtraLink = self.fNewVoidExtraLink()
        unExtraLink.update( {
            'label'   : self.fTranslateI18N( 'gvSIGi18n', 'gvSIGi18n_GoTo_Root', 'Go Root',),
            'href'    : '%s/TRACatalogo/' % unaURL,
            'icon'    : 'tra_root.gif',
            'domain'  : 'gvSIGi18n',
            'msgid'   : 'gvSIGi18n_GoTo_Root',
        })
        unosExtraLinks.append( unExtraLink)
                            
        return unosExtraLinks
    
    
    
    
    
    
    
    security.declarePrivate( 'fAllSubElements')    
    def fAllSubElements( self, theAdditionalParms=None):
        someSubElements = [ ]
        self.pAllSubElements_into( someSubElements, theAdditionalParms=None)
        return someSubElements
    
           
    
    
    
    security.declarePrivate( 'pForAllElementsDo')    
    def pForAllElementsDo( self, theLambda=None):
        if not theLambda:
            return self
        someSubElements = [ ]
        self.pForAllElementsDo_recursive( theLambda)
        return someSubElements
        
    


        
        
        

    
    security.declarePublic( 'fIsCollection')    
    def fIsCollection( self, theObject):
        if not theObject:
            return False
        return isinstance( theObject, type( [])) or isinstance( theObject, type( (1,2))) or isinstance( theObject, type( set())) 
    
    
    
    security.declarePublic( 'pLog')    
    def pLog( self, theMessage):
        
        logging.getLogger( 'gvSIGi18n').info( fReprAsString( theMessage))
        
        return self
    
    
 
      
    security.declarePrivate( 'fNewVoidLanguagesDetails')    
    def fNewVoidLanguagesDetails( self,):
        aLanguagesDetails = dict( [ [ aKey, '',] for aKey in cAcceptedLanguageDetailKeys])
        return aLanguagesDetails
    
    
    
      
    security.declarePrivate( 'fNewVoidUploadedContent')    
    def fNewVoidUploadedContent( self,):
        unUploadedContent = {
            'import_report':                          None,
            'uploaded_entries':                       [],
            # ############################################
            # languages is the list of language names to create 
            'languages':                              [],
            # ############################################
            # module is the module to which the included strings are associated.
            'module':                                 '',
            # ############################################
            # languages is a dict with language codes as keys, 
            # and values are a dict holding details about the language to create, including
            'languages_details':                      self.fNewVoidLanguagesDetails(),
            # ############################################
            # strings_and_translations is a dict
            #   where keys are string symbols, 
            #   and   values are dicts with languages a keys, and the values are the translations of the symbols for the key language.
            'strings_and_translations':               {},
            # ############################################
            # strings_with_encoding_errors is a dict
            #   where keys are string symbols, 
            #   and   values are lists of the languages for which there was encountered an encoding error while reading the translations interchange file.            
            'strings_with_encoding_errors':           {}, 
            'strings_sources':                        {},
        }
        return unUploadedContent
    
    
        
    
    security.declarePrivate( 'fNewVoidContenidoIntercambioReport')    
    def fNewVoidContenidoIntercambioReport( self):
        """Used by both TRAImportacion and TRAContenidoIntercambio to report a summary of translation interchange contents.
        
        """
        
        return {
            'num_strings':                      0,
            'languages':                        [],
            'language_names_and_flags':         {},
            'num_translated_by_language':       {},
            'num_pending_by_language':          {},
            'percent_pending_by_language':      {},
            'percent_translated_by_language':   {},
            'num_encoding_errors_by_language':  {},            
            'percent_encoding_errors_by_language':       {},
        }

    
        

    security.declarePrivate( 'fNewVoidChangeTranslationResult')
    def fNewVoidChangeTranslationResult( self,):
        aResult = {
            'success':                          False,
            'exception':                        '',
            'status':                           '',
            'condition':                         '',
            'found':                            False,
            'changed':                          False,
            'changed_comment':                  False,
            'simboloCadena':                    '',
            'idCadena':                         '',
            'memberid':                         '',
            'cadenaTraducida_previousValue':    '',
            'cadenaTraducida_newValue':         '',
            'estadoTraduccion_previousValue':   '',
            'estadoTraduccion_newValue':        '',
            'comentario_previousValue':         '',
            'comentario_newValue':              '',
        }
        return aResult
    

 

    # ######################################################################
    """METHODS: Execution context
    
    """
       
    # ACV 20090328 still unused
    #security.declarePublic( 'fNewExecutionContext')    
    #def fNewExecutionContext( self, theExecutedKind, theExecutedName, theParentExecutionRecord=None, theAllowRoot=False, theProfilingConfig={}):
        #"""Creates an instance of TRAExecutionContext taking the receiver as contextual object, to share information over the complete execution in response to the connected user request.
        
        #"""
        
        #return TRAExecutionContext( self, theExecutedKind, theExecutedName, theParentExecutionRecord, theProfilingConfig)

    
    
    
    

    
 

    # ######################################################################
    """METHODS: Time Profiling
    
    """
      
    
    security.declarePublic( 'fStartExecution')    
    def fStartExecution( self, 
        theExecutedKind, 
        theExecutedName, 
        theParentExecutionRecord=None, 
        theAllowRoot=False, 
        theProfilingConfig={},
        theExtraExecutionInfo=''):
        
        if not theParentExecutionRecord and not theAllowRoot:
            return None
            
        unExecutionRecord = TRAExecutionRecord( 
            self, 
            theExecutedKind             =theExecutedKind, 
            theExecutedName             =theExecutedName, 
            theParentExecutionRecord    =theParentExecutionRecord, 
            theProfilingConfig          =theProfilingConfig, 
            theExtraExecutionInfo       =theExtraExecutionInfo
        )
        if not unExecutionRecord or unExecutionRecord.vIsExcluded:
            return None
        
        return unExecutionRecord
     
    
    security.declarePublic( 'pEndExecution')    
    def pEndExecution( self, theExecutionRecord):
        if not theExecutionRecord:
            return self
        return theExecutionRecord.pEndExecution()
      
    
    security.declarePublic( 'pLogPerformance')    
    def pLogPerformance(self, theExecutionRecord):
        if not theExecutionRecord:
            return self
        return theExecutionRecord.pLogPerformance()
        

    security.declarePublic( 'fPrintString')    
    def fPrintString(self, theExecutionRecord):
        if not theExecutionRecord:
            return self
        return theExecutionRecord.fPrintString()
      
        
    security.declarePublic( 'fPrintStringDots')    
    def fPrintStringDots(self, theExecutionRecord):
        if not theExecutionRecord:
            return self
        return theExecutionRecord.fPrintStringDots()
      
    security.declarePublic( 'fPrintStringDetails')    
    def fPrintStringDetails(self, theExecutionRecord):
        if not theExecutionRecord:
            return self
        return theExecutionRecord.fPrintStringDetails()      
    
    
    security.declarePublic( 'fPrintStringDots_HTML')    
    def fPrintStringDots_HTML(self, theExecutionRecord):
        if not theExecutionRecord:
            return self
        return theExecutionRecord.fPrintStringDots_HTML()      
    
        
    security.declarePublic( 'fPrintStringDetails_HTML')    
    def fPrintStringDetails_HTML(self, theExecutionRecord):
        if not theExecutionRecord:
            return self
        return theExecutionRecord.fPrintStringDetails_HTML()      
    
  
    security.declarePublic( 'pClearLoggedAll')    
    def pClearLoggedAll(self, theExecutionRecord):
        if not theExecutionRecord:
            return self
        return theExecutionRecord.pClearLoggedAll()      
        
        
        
        

    security.declarePublic( 'fCGIescape')
    def fCGIescape(self, theString, quote=1):
        if not theString:
            return ''
        return cgi.escape( theString, quote=quote)
    
    
        
        
    # #############################################################
    # Prefered Encodings for known languages 
    #     
    # #############################################################


    
    
    
    
        
    security.declareProtected( permissions.View, 'fEncodingsForLanguage')
    def fEncodingsForLanguage(self, theCodigoIdioma):
        
        unCodigoIdioma, unCodigoCountry, unaVariation = self.fLanguageAndCountryAndVariationIdioma( theCodigoIdioma) 

        someEncodingsForAllLanguages = set( [ unE[ 0] for unE in cUTFEncodingsForAllLanguages])
        
        someEncodingsForAllLanguages.add( cEncodingUnicodeEscape)
        
        someEncodingsForLanguage     = [ unE[:] for unE in cUTFEncodingsForAllLanguages]

        if not theCodigoIdioma:
            return someEncodingsForLanguage
        
        someTitlesByEncodingName = { }
        someAliasesByEncodingName = { }
        
        todosEncodings = set()
        
        someSpecificEncodings = set()
        someWesternEncodings   = set()
        
        for unEncoding, unosAliasesString, unTitle, unosLanguageCodesString in cDefaultEncodingsSourceMap:
            unEncoding = unEncoding.strip().lower()
            if unEncoding and not ( unEncoding in someEncodingsForAllLanguages):
                if not (unEncoding in todosEncodings):
                    unCodecInfo = None
                    try:
                        unCodecInfo = CODECS_Lookup( unEncoding)
                    except:
                        None
                     
                    if unCodecInfo:
                        todosEncodings.add( unEncoding)
                        
                        if unTitle:
                            someTitlesByEncodingName[ unEncoding] = unTitle
                        
                        unosAliases = [ unAlias.strip() for unAlias in unosAliasesString.split( ',') if unAlias.strip()]
                        if unosAliases:
                            someAliasesByEncodingName[ unEncoding] = sorted( unosAliases)
                        
                        unosLanguageCodes = [ unLanguageCode.strip() for unLanguageCode in unosLanguageCodesString.split( ',') if unLanguageCode.strip()]
                        if unosLanguageCodes:
                            if cWesternLanguageMarkInSourceMap in unosLanguageCodes:
                                someWesternEncodings.add( unEncoding)   
                            if ( not ( unCodigoIdioma == cWesternLanguageMarkInSourceMap)) and ( ( theCodigoIdioma in unosLanguageCodes) or ( unCodigoIdioma in unosLanguageCodes)):
                                someSpecificEncodings.add( unEncoding)   
                        else:
                            someWesternEncodings.add( unEncoding)   
                    
        if someSpecificEncodings:
            someEncodingsForLanguage.append( [ cEncodingSeparatorSentinelName, '', [], ])
            for aEncoding in sorted( someSpecificEncodings):
                someEncodingsForLanguage.append( [ aEncoding, someTitlesByEncodingName.get( aEncoding, aEncoding), someAliasesByEncodingName.get( aEncoding, []), ])
            someEncodingsForLanguage.append( [ cEncodingSeparatorSentinelName, '', [], ])
            for aEncoding in sorted( todosEncodings.difference( someSpecificEncodings)):
                someEncodingsForLanguage.append( [ aEncoding, someTitlesByEncodingName.get( aEncoding, aEncoding), someAliasesByEncodingName.get( aEncoding, []), ])

        else:        
            someEncodingsForLanguage.append( [ cEncodingSeparatorSentinelName, '', [], ])
            for aEncoding in sorted( someWesternEncodings):
                someEncodingsForLanguage.append( [ aEncoding, someTitlesByEncodingName.get( aEncoding, aEncoding), someAliasesByEncodingName.get( aEncoding, []), ])
            someEncodingsForLanguage.append( [ cEncodingSeparatorSentinelName, '', [], ])
            for aEncoding in sorted( todosEncodings.difference( someWesternEncodings)):
                someEncodingsForLanguage.append( [ aEncoding, someTitlesByEncodingName.get( aEncoding, aEncoding), someAliasesByEncodingName.get( aEncoding, []), ])
        
        someEncodingsWithCompositeTitle = [ ]
        for unEncodingNameAndAliases in someEncodingsForLanguage:
            unCompositeTitle = ''
            if not ( unEncodingNameAndAliases[ 0] == cEncodingSeparatorSentinelName):
                unCompositeTitle = unEncodingNameAndAliases[ 0]
                if unEncodingNameAndAliases[ 1] and not( unEncodingNameAndAliases[ 1] == unEncodingNameAndAliases[ 0]):
                    unCompositeTitle = '%s %s ' % ( unCompositeTitle, unEncodingNameAndAliases[ 1],)
                unosAliases = ' '.join( unEncodingNameAndAliases[ 2])
                if unosAliases and not( unosAliases == unEncodingNameAndAliases[ 0]) and not( unosAliases == unEncodingNameAndAliases[ 1]):
                    unCompositeTitle = '%s %s ' % ( unCompositeTitle, unosAliases,)
             
            someEncodingsWithCompositeTitle.append( [ 
                unEncodingNameAndAliases[ 0],
                unEncodingNameAndAliases[ 1],
                unEncodingNameAndAliases[ 2],
                unCompositeTitle,
            ])
        return someEncodingsWithCompositeTitle 
                
          
    
    
        
        
    # #############################################################
    # Globally known languages 
    #     
    #   Key : Language code
    #   Value: Dictionary with keys: 'english' 'native' and optionally 'flag'
    # #############################################################
    
    security.declareProtected( permissions.View, 'fLanguagesNamesAndFlagsPorCodigo')
    def fLanguagesNamesAndFlagsPorCodigo(self,):
        
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
    
             
    
       
    
    
    
    
    
    
    # #################################################
    # Names for User Groups
    #
    
    # #################################################
    # Global User Groups
    #
       
    security.declarePrivate( 'fUserGroupIdEnCatalogoFor')
    def fUserGroupIdEnCatalogoFor(self, theGroupName):
        return '%s_%s' % ( self.fPrefijoUserGroupsEnCatalogo(), theGroupName, )
 
     
    
    security.declarePrivate( 'fPrefijoUserGroupsEnCatalogo')
    def fPrefijoUserGroupsEnCatalogo(self, ):
        return 'TRA_%s' % '_'.join( self.getCatalogo().getPhysicalPath()[2:])
 

    
    
    

   
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
   
    
    
    

    
    
    # #################################################
    # Parser for idioma codes
    #
    security.declarePrivate( 'fLanguageAndCountryAndVariationIdioma')    
    def fLanguageAndCountryAndVariationIdioma( self, theCodigoIdioma):
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
        
    
    
      
# ####################################
#  Portal root accessor
#
        
    security.declarePrivate('fPortalRoot')
    def fPortalRoot(self):
        aPortalTool = getToolByName( self, 'portal_url')
        unPortal = aPortalTool.getPortalObject()
        return unPortal       
    
    

        
    

    security.declarePrivate('fPortalURL')
    def fPortalURL(self, ):
        
        unPortalURLTool = getToolByName( self, 'portal_url', None)
        if not unPortalURLTool:
            return ''
        
        unPortalURL = ''
        try:
            unPortalURL = unPortalURLTool()
        except: 
            None
        if not unPortalURL:
            return ''
        
        return unPortalURL
           
        
    
      
# ####################################
#  Initialize after creation
#
        
    
    security.declarePrivate('pHandle_manage_afterAdd')
    def pHandle_manage_afterAdd(self, theItem, theContainer):   
        
        if self.__class__.__name__ == 'TRACadena':
            pass
        
        elif self.__class__.__name__ == 'TRATraduccion':
            pass
        
        elif self.__class__.__name__ == 'TRAColeccionCadenas':
            BaseBTreeFolder.manage_afterAdd(  self, theItem, theContainer)
        
        #elif self.__class__.__name__ == 'TRAColeccionSolicitudesCadenas':
            #BaseBTreeFolder.manage_afterAdd(  self, theItem, theContainer)

        else:
            OrderedBaseFolder.manage_afterAdd(  self, theItem, theContainer)
        
        self.pSetPermissions()
                
        return self
    
         
        
    

   
    # #############################################################
    # Intercepting modification method for re-ordering an OrderedBaseFolder specialization
    # used in to provide drag&drop functionality directly from Plone.
    # does not hit the ModelDDvlPlone framework presentation layer
    # and therefore the incalidation of cache entries must be triggered by intercepting the method
    #

    security.declareProtected(permissions.ModifyPortalContent, 'pHandle_moveObjectsByDelta')
    def pHandle_moveObjectsByDelta(self, ids, delta, subset_ids=None): 
        
        unResult = None
        
        if self.__class__.__name__ == 'TRAColeccionCadenas':
            
            unResult = BaseBTreeFolder.moveObjectsByDelta(   self,  ids, delta, subset_ids=subset_ids)
        
        else:
            unResult = OrderedBaseFolder.moveObjectsByDelta( self,  ids, delta, subset_ids=subset_ids)
        
        
        if not unResult:
            return self
        
        
        unaModelDDvlPloneTool = getToolByName( self, 'ModelDDvlPlone_tool', None)
        if not unaModelDDvlPloneTool:
            return self
        
        someImpactedUIDs = []
        
        unaOwnUID = self.UID()
        someImpactedUIDs.append( unaOwnUID)
        
        if shasattr( self, 'getContenedor'):
            unContenedor = None
            try:
                unContenedor = self.getContenedor()
            except:
                None
            if not ( unContenedor == None):
                unContenedorUID = ''
                if shasattr( self, 'UID'):
                    unContenedorUID = ''
                    try:
                        unContenedorUID = unContenedor.UID()
                    except:
                        None
                    if unContenedorUID and not ( unContenedorUID in someImpactedUIDs):
                        someImpactedUIDs.append( unContenedorUID)
            
        if shasattr( self, 'getPropietario'):
            unPropietario = None
            try:
                unPropietario = self.getPropietario()
            except:
                None
            if not ( unPropietario == None) and not ( unPropietario == unContenedor):
                unPropietarioUID = ''
                if shasattr( self, 'UID'):
                    unPropietarioUID = ''
                    try:
                        unPropietarioUID = unPropietario.UID()
                    except:
                        None
                if unPropietarioUID and not ( unPropietarioUID in someImpactedUIDs):
                    someImpactedUIDs.append( unPropietarioUID)
            
        someIds = ids
        if not ( someIds.__class__.__name__ in [ 'list', 'tuple', 'set',]):
            someIds = [ someIds,]

        aMovedNewPosition = -1
        someObjectValues = self.objectValues()
        for anObjectIndex in range( len( someObjectValues)):
            
            anObject = someObjectValues[ anObjectIndex]
            
            anObjectId = anObject.getId()
            if ( anObjectId in someIds):
                aMovedNewPosition = anObjectIndex
                
            anObjectUID = anObject.UID()
            if anObjectUID and not ( anObjectUID in someImpactedUIDs):
                someImpactedUIDs.append( anObjectUID)

                
        anElementToReportUpon = None
            
        for anId in someIds:
            for anObject in someObjectValues:
                if anObject.getId() == anId:
                    anElementToReportUpon = anObject
                    break
                
        anElementResult = None
        if not ( anElementToReportUpon == None):
            anElementResult = unaModelDDvlPloneTool.fNewResultForElement( anElementToReportUpon)
            
            
        unaModelDDvlPloneTool.pFlushCachedTemplatesForImpactedElementsUIDs( self, someImpactedUIDs)
        
        aMoveReport = {
            'effect':                  'moved', 
            'new_position':            aMovedNewPosition,
            'delta':                   delta,
            'moved_element':           anElementResult,
            'parent_traversal_name':   '',
            'impacted_objects_UIDs':   someImpactedUIDs,
        } 
        unaModelDDvlPloneTool._pSetAudit_Modification( self, 'Move Sub Object', aMoveReport)
        
        return unResult
            
        
    
        
      
# ####################################
#  Destroy before deletion
#
        
    
    security.declarePrivate('pHandle_manage_beforeDelete')
    def pHandle_manage_beforeDelete(self, theItem, theContainer):   
        """Disable ZCatalog logging while deleting contents to avoid flooding the log with catalog messages complaining about keys not found. 
        Note that instances of TRACadena and TRATraduccion are not catalogged in the global ZCatalog, and therefore there are thousands of ZCatalog log entries complaining.
        This excessive logging slows down the server.
        
        """
        unResult = None
        unDisableLevelChanged = False
        try:
            aLoggerManager = logging.getLogger('Zope.ZCatalog').manager
            aDisableLevel = aLoggerManager.disable
            
            if not ( aDisableLevel == cLoggingLevel_ERROR):
                if aLoggerManager:
                    aLoggerManager.disable = cLoggingLevel_ERROR
                    unDisableLevelChanged = True
                
            if isinstance( self, OrderedBaseFolder):
                OrderedBaseFolder.manage_beforeDelete(  self, theItem, theContainer)
            elif isinstance( self, BaseBTreeFolder):
                BaseBTreeFolder.manage_beforeDelete(  self, theItem, theContainer)
                            
        finally:
            if unDisableLevelChanged:
                if aLoggerManager:
                    aLoggerManager.disable = aDisableLevel

        return self
        
    
    
    
    
    
    
# #############################################################
# Basic accessor for contained element by id
#     

    security.declarePrivate( 'getElementoPorID')
    def getElementoPorID(self, theID):
        if not theID:
            return None

        unosExistingElements = self.objectValues()
        
        for unElement in unosExistingElements:
            unId = unElement.getId()
            if unId == theID:
                return unElement
             
        return None    
        
     

# #############################################################
# Utility tool accessor
#     
    
    
    security.declarePrivate( 'getPloneUtilsToolForNormalizeString')
    def getPloneUtilsToolForNormalizeString(self):
    
        aTool = getToolByName(self, 'plone_utils', None)
        if not shasattr( aTool, 'normalizeString'):
            return None 
        return aTool

    
    
           
    
    
    security.declarePrivate( 'getPloneUtilsToolForRoleAcquisition')
    def getPloneUtilsToolForRoleAcquisition(self):
    
        aTool = getToolByName(self, 'plone_utils', None)
        return aTool

    
    
           
 
    security.declarePrivate( 'getGroupsTool')
    def getGroupsTool(self):
    
        aTool = getToolByName(self, 'portal_groups', None)
        return aTool

    
    
           
    security.declarePrivate( 'getPloneLanguageTool')
    def getPloneLanguageTool(self):
    
        aTool = getToolByName(self, 'portal_languages', None)
        return aTool

    
    
           
     
     

    
    
    
    
# ####################################
#  Membership 
#
        
    
    
    security.declarePublic( 'fGetMemberId')
    def fGetMemberId(self ):
    
        aMembershipTool = getToolByName( self, 'portal_membership', None)
        if not aMembershipTool:
            return ''
        
        unMember = aMembershipTool.getAuthenticatedMember()   

        if not unMember:
            return ''
        
        if unMember.getUserName() == 'Anonymous User':
            unMemberId = unMember.getUserName()
        else:
            unMemberId = unMember.getMemberId()   

        return unMemberId
        
   
    

    

    
    
# #############################################################
# Owner accessors
# 



    security.declarePrivate('getRaiz')
    def getRaiz(self):
        if self.getEsRaiz():
            return self            
        unContenedor =  aq_parent( aq_inner( self))
        
        if not unContenedor:
            return None
        
        return unContenedor.getRaiz()

    
    
    
    
    security.declarePrivate( 'getCatalogo')
    def getCatalogo( self):
        unCatalogo = self.getRaiz()
        if not (unCatalogo.__class__.__name__ == cNombreTipoTRACatalogo):
            return None
        return unCatalogo
        





    # OJO ACV 20090609 
    # to use standard plone portal_catalog path index rather than 
    # the application specific getPathDelRaiz
    security.declarePrivate('fPathDelRaiz')
    def fPathDelRaiz(self):
        unRaiz = self.getRaiz()
        if not unRaiz:
            return ''
       
        unPathString = unRaiz.fPhysicalPathString( )
        return unPathString
        
    
    #security.declarePrivate('fPathDelRaiz')
    #def fPathDelRaiz(self):
        #unRaiz = self.getRaiz()
        #if not unRaiz:
            #return ''
       
        #unPathString = self.fPhysicalPathString( unRaiz)
        #return unPathString



    # ACV 20090913 Return the standard path, not the variation we were using before, without the root site name
    # Remove the parameter
    security.declarePrivate('fPhysicalPathString')
    def fPhysicalPathString(self, ):
        unPhysicalPath = self.getPhysicalPath()
        if not unPhysicalPath:
            return ''
     
        #if unPhysicalPath[ 0] == '':
            #unPhysicalPath = unPhysicalPath[1:]
        
        #unFoldersPath = unPhysicalPath[1:]
        #unPathString = '/' + '/'.join( unFoldersPath)
        unPathString = '/'.join( unPhysicalPath)
        return unPathString





    
    security.declarePrivate('fDisplayPathString')
    def fDisplayPathString(self):
        return '/'.join( self.getPhysicalPath()[2:])
    


    security.declarePublic('getPropietario')
    def getPropietario(self):
        if self.getEsRaiz():
            return self
            
        unContenedor = self.getContenedor()
        
        if not unContenedor:
            return None
        
        if unContenedor.getEsRaiz():
            return unContenedor
        
        if unContenedor.getEsColeccion():
            return unContenedor.getPropietario()
        
        return unContenedor



    
    
    
   


    # #############################################################
    # Date rounding for searches
    #

    security.declarePrivate( 'fFechaISOStringLastMonthDayInYear')
    def fFechaISOStringLastMonthDayInYear( self, theMonthNumber, theYearNumber):
        if not theMonthNumber:
            return 0
        
        if theMonthNumber in [ 1, 3, 5, 7, 8, 10, 12,]:
            return 31
        
        if theMonthNumber in [ 4, 6, 9, 11, ]:
            return 30
       
        if theYearNumber % 4:
            return 29
        
        return 28
    
            
    
    
            
    security.declarePrivate( 'fFechaISOStringDesdeStringParcial')
    def fFechaISOStringDesdeStringParcial( self, theISODatePartialString, theEarliest=True):
    
        if not theISODatePartialString:
            return ''
        
        unaFechaString = theISODatePartialString
            
        unosYearMonthDay = unaFechaString.split( cISOStringFechaYMDSeparator)
        if not unosYearMonthDay:
            return ''
        
        unYearString   = unosYearMonthDay[ 0]
        unMonthString = ''
        unDayString   = ''
        if len( unosYearMonthDay) > 1:
            unMonthString = unosYearMonthDay[ 1]
        if len( unosYearMonthDay) > 2:
            unDayString   = unosYearMonthDay[ 2]
            
            
            
        if not unYearString:
            return ''
        unYearInt = -1
        try:
            unYearInt = int( unYearString)
        except:
            None
        if not ( ( unYearInt >= cFirstYearForSearches) and ( unYearInt <= cLastYearForSearches)):
            return ''
        else:
            unYearString = '%04d' % unYearInt
        
            
            
        if not unMonthString:
            unMonthInt    = ( theEarliest and cFirstMonthForSearches) or cLastMonthForSearches
            unMonthString = '%02d' % unMonthInt
        else:
            unMonthInt = -1
            try:
                unMonthInt = int( unMonthString)
            except:
                None
            if ( unMonthInt >= cFirstMonthForSearches) and ( unMonthInt <= cLastMonthForSearches):
                unMonthString = '%02d' % unMonthInt
            else:
                unMonthInt    = ( theEarliest and cFirstMonthForSearches) or cLastMonthForSearches
                unMonthString = '%02d' % unMonthInt
            
            
        if not unDayString:
            unDayString = '%02d' % (( theEarliest and cFirstDayForSearches) or self.fFechaISOStringLastMonthDayInYear( unMonthInt, unYearInt))
        else:
            unDayInt = -1
            try:
                unDayInt = int( unDayString)
            except:
                None
            unLastDayForSearches = self.fFechaISOStringLastMonthDayInYear( unMonthInt, unYearInt)
            if ( unDayInt >= cFirstDayForSearches) and ( unDayInt <= unLastDayForSearches):
                unDayString = '%02d' % unDayInt
            else:
                unDayString = '%02d' % (( theEarliest and cFirstDayForSearches) or unLastDayForSearches)
            

        unNewDateString = '%s-%s-%s' % ( unYearString, unMonthString, unDayString,)
        return unNewDateString
    
    
    
        
    

            
    security.declarePrivate( 'fHoraISOStringDesdeStringParcial')
    def fHoraISOStringDesdeStringParcial( self, theISOTimePartialString, theEarliest=True):
    
        if not theISOTimePartialString:
            return ''
        
        unaHoraString = theISOTimePartialString
            
        unosHourMinuteSecond = unaHoraString.split( cISOStringHoraHMSSeparator)
        if not unosHourMinuteSecond:
            return ''
        
        unHourString   = unosHourMinuteSecond[ 0]
        unMinuteString = ''
        unSecondString   = ''
        if len( unosHourMinuteSecond) > 1:
            unMinuteString = unosHourMinuteSecond[ 1]
        if len( unosHourMinuteSecond) > 2:
            unSecondString   = unosHourMinuteSecond[ 2]
            
            
            
        if not unHourString:
            return ''
        unHourInt = -1
        try:
            unHourInt = int( unHourString)
        except:
            None
        if not ( ( unHourInt >= cFirstHourForSearches) and ( unHourInt <= cLastHourForSearches)):
            return ''
        else:
            unHourString = '%02d' % unHourInt
        
            
            
        if not unMinuteString:
            unMinuteInt    = ( theEarliest and cFirstMinuteForSearches) or cLastMinuteForSearches
            unMinuteString = '%02d' % unMinuteInt
        else:
            unMinuteInt = -1
            try:
                unMinuteInt = int( unMinuteString)
            except:
                None
            if ( unMinuteInt >= cFirstMinuteForSearches) and ( unMinuteInt <= cLastMinuteForSearches):
                unMinuteString = '%02d' % unMinuteInt
            else:
                unMinuteInt    = ( theEarliest and cFirstMinuteForSearches) or cLastMinuteForSearches
                unMinuteString = '%02d' % unMinuteInt
            
            
            
        if not unSecondString:
            unSecondString = '%02d' % (( theEarliest and cFirstSecondForSearches) or cLastSecondForSearches)
        else:
            unSecondInt = -1
            try:
                unSecondInt = int( unSecondString)
            except:
                None
            if ( unSecondInt >= cFirstSecondForSearches) and ( unSecondInt <= cLastSecondForSearches):
                unSecondString = '%02d' % unSecondInt
            else:
                unSecondString = '%02d' % (( theEarliest and cFirstSecondForSearches) or cLastSecondForSearches)
            

        unNewTimeString = '%s:%s:%s' % ( unHourString, unMinuteString, unSecondString,)
        return unNewTimeString
        

    
    
    
    
    security.declarePrivate( 'fFechaISOStringRounded')
    def fFechaISOStringRounded( self, theISODateString, theEarliest=True, theDefaultDate=None):
        if not theISODateString:
            return ''
        
        unFechaYHoraStrings = theISODateString.split( cISOStringFechaYHoraSeparator)
        if not unFechaYHoraStrings:
            return ''
         
        unaFechaStringCompleted = ''
        unaHoraStringCompleted  = ''
                
        if len( unFechaYHoraStrings) > 1:
            unaFechaStringCompleted =           self.fFechaISOStringDesdeStringParcial( unFechaYHoraStrings[ 0], theEarliest)
            if not unaFechaStringCompleted:
                unaFechaStringCompleted =       self.fFechaISOStringDesdeStringParcial( unFechaYHoraStrings[ 1], theEarliest)
            unaHoraStringCompleted  =       self.fHoraISOStringDesdeStringParcial(  unFechaYHoraStrings[ 0], theEarliest)
            if not unaHoraStringCompleted:
                unaHoraStringCompleted  =   self.fHoraISOStringDesdeStringParcial(  unFechaYHoraStrings[ 1], theEarliest)
                    
        else:
            unaFechaStringCompleted =           self.fFechaISOStringDesdeStringParcial( unFechaYHoraStrings[ 0], theEarliest)
            if not unaFechaStringCompleted:
                unaHoraStringCompleted  =       self.fHoraISOStringDesdeStringParcial(  unFechaYHoraStrings[ 0], theEarliest)
             
                
        if not ( unaFechaStringCompleted or unaHoraStringCompleted):
            return ''
        
        if not unaFechaStringCompleted:
            unaFechaStringCompleted = theDefaultDate.ISO()[:10]
        
        if not unaHoraStringCompleted:
            unaHoraStringCompleted = ( theEarliest and cISOStringEarliestDayTime) or cISOStringLatestDayTime        
            
        unFechaHoraResultado = '%s%s%s' % ( unaFechaStringCompleted, cISOStringFechaYHoraSeparator, unaHoraStringCompleted,)
        return unFechaHoraResultado
    

       




# ####################################################################
# Time accessors to minimize instantiation of DateTime while profiling
#
    
    
    
    security.declareProtected( permissions.View, 'fIsAcceptableMagicMilliseconds')
    def fIsAcceptableMagicMilliseconds(self, theString, theAllowedSeconds):   
        if not theString or not theAllowedSeconds:
            return False
        
        aDeMagicizedString =  self.fDeMagicizeString( theString)
        if not aDeMagicizedString:
            return False
        
        aMilliseconds = 0
        try:
            aMilliseconds = int( aDeMagicizedString)
        except:
            None
        if not aMilliseconds:
            return False
        
        aMillisecondsNow = fMillisecondsNow() 
        
        anAllowed = ( aMillisecondsNow > aMilliseconds) and  ( (aMillisecondsNow - aMilliseconds) <= ( theAllowedSeconds * 1000))
        return anAllowed
        
        
        
    security.declareProtected( permissions.View, 'fMagicMillisecondsNowString')
    def fMagicMillisecondsNowString(self):   
        someMilliseconds = fMillisecondsNow()
        unMillisecondsString = str( someMilliseconds)
        unMagicMillisecondsString = self.fMagicizeString( unMillisecondsString)
        return unMagicMillisecondsString
    
    
    
    
    security.declareProtected( permissions.View, 'fMagicizeString')
    def fMagicizeString(self, theString):   
        if not theString:
            return ''
        
        aMagicizedString = theString[:]
        
        return aMagicizedString 
             
    
    security.declareProtected( permissions.View, 'fDeMagicizeString')
    def fDeMagicizeString(self, theString):   
        if not theString:
            return ''
        
        aDeMagicizedString = theString[:]
        
        return aDeMagicizedString 
             

    
    #security.declareProtected( permissions.View, 'fMillisecondsNow')
    #def fMillisecondsNow(self):   
        #return int( time() * 1000)
    
    
    
    #security.declareProtected( permissions.View, 'fDateTimeNow')
    #def fDateTimeNow(self):   
        #return DateTime()
    
    
    
    security.declareProtected( permissions.View, 'fDateTimeNowString')
    def fDateTimeNowString(self):   
        return self.fDateTimeToString( fDateTimeNow())
    
    
    security.declareProtected( permissions.View, 'fDateTimeToString')
    def fDateTimeToString(self, theDateTime):  
        if not theDateTime:
            return ''
        return str( theDateTime)
    
    
    
    security.declareProtected( permissions.View, 'fDateTimeNowTextual')
    def fDateTimeNowTextual(self):   
        unYMDHMS = localtime()[:6]
        unDateStoreString = '%04d-%02d-%02d %02d:%02d:%02d' % unYMDHMS
        return self.fDateToStoreString( fDateTimeNow())





   
    
   
    # #################################################
    # Handling of Dates as strings to avoid catalog schema overhead
    # Using ISO format AAAA-MM-DD HH:MM:SS '2009-03-21 01:36:00'
    # No time zone is stored. 
    # It is encoded as the time in the Valencia zone 'GMT+1'
    #
    
    def fStoreStringToDate( self, theString):
        if not theString:
            return None
        
        unDate = None
        try:
            unDate = DateTime( theString)   
        except:
            None
        
        return unDate
    
    
    
    def fDateToStoreString( self, theDate):
        if not theDate:
            return None
        
        unString = theDate.ISO()
        return unString
    
    

  


    









 
# #############################################################
# Generic attribute accesor by name
# 

    security.declarePublic('getAttributeValueByName')
    def getAttributeValueByName( self, theName):
        if self.schema.has_key( theName):
            return self.schema[theName].getRaw(self) # , encoding="utf-8")
        else:
            if theName == 'title':
                return self.Title()
            elif theName == 'text':
                return self.getText()
            elif theName == 'description':
                return self.Description()
            elif theName == 'titleAndOwnerTitle':
                unPropietario = self.getPropietario()
                if unPropietario == self:
                    return self.Title()
                else:
                    return "%s [%s]" % (self.Title(), unPropietario.Title())
            else:
                return self.__getattribute__(theName)
        



# #############################################################
# Class metainfo accesor methods  
#
    security.declarePublic('getMetaValue')
    def getMetaValue( self , elNombreAttribute):
        if not elNombreAttribute:
            return None

        someStringMetaAttributes = [ 'archetype_name', 'meta_type',  'portal_type',  'content_icon',  'typeDescription',  'typeDescMsgId',  'immediate_view',  'default_view', ]
        someStringArrayMetaAttributes = [ 'allowed_content_types', 'suppl_views', ]
        
        if not( elNombreAttribute in someStringMetaAttributes + someStringArrayMetaAttributes):
            return None
            
        unValue = self.__getattribute__( elNombreAttribute)
        unResult = [ elNombreAttribute, unValue, elNombreAttribute, elNombreAttribute, elNombreAttribute, elNombreAttribute, 'string' ]
        
        if elNombreAttribute in someStringArrayMetaAttributes:
            unResult[ 6] = 'string[]'
        
        return unResult
            





# #############################################################
# Attribute accesor methods for combined info and metainfo 
#
    
    security.declarePublic('getAttributeMetaAndValue')    ###
    def getAttributeMetaAndValue(self , elNombreAttribute): ###
        if not elNombreAttribute:
            return None
            

        unSchema = self.schema
        if not unSchema.has_key( elNombreAttribute):
            return None
            
        unField             = unSchema[ elNombreAttribute]
        unWidget            = unField.widget
        unType              = unField.type
        unaLabel            = elNombreAttribute
        unaDescription      = elNombreAttribute
        unaLabelMsgId       = elNombreAttribute
        unaDescriptionMsgId = elNombreAttribute
        
        try:
            unaLabel            = unWidget.label            
        except:
            None
            
        try:
            unaDescription  = unWidget.description
        except:
            None
            
        try:
            unaLabelMsgId       = unWidget.label_msgid
        except:
            None
            
        try:
            unaDescriptionMsgId = unWidget.description_msgid
        except:
            None
        
        unVocabulary        = []
        unVocabularyMsgIds  = []
        
        if self.schema[ elNombreAttribute].widget.getType() == 'Products.Archetypes.Widget.SelectionWidget':
            if self.schema[ elNombreAttribute].__dict__.has_key('vocabulary'):
                unVocabulary = self.schema[ elNombreAttribute].vocabulary
                if unVocabulary:
                    unType = 'selection'
                    
                    unVocabularyMsgIds = unVocabulary[:]
                    try:
                        unVocabularyMsgIds = self.schema[ elNombreAttribute].vocabulary_msgids
                    except:
                        None
        
        unValue     = self.getAttributeValueByName( elNombreAttribute)    
        
        unResult = [ elNombreAttribute, unValue, unaLabel, unaLabelMsgId, unaDescription, unaDescriptionMsgId, unType, unVocabulary, unVocabularyMsgIds ]
        
        return unResult        





 
# #############################################################
# Generic attribute mutators by name
# 


    security.declareProtected( permissions.ModifyPortalContent, 'setAttributesValues')
    def setAttributesValues(self , losNombresYValoresAttributes=""):
        if not losNombresYValoresAttributes:
            return []

        someResults = []
        for unNombreYValorAttribute in losNombresYValoresAttributes:
            if unNombreYValorAttribute and len( unNombreYValorAttribute) > 1:
                unNombreAttribute = unNombreYValorAttribute[ 0]
                unNuevoValorAttribute  = unNombreYValorAttribute[ 1]
            
                unAttributeMetaAndValue = self.getAttributeMetaAndValue( unNombreAttribute)
                if unAttributeMetaAndValue:
                    unValorAttribute = unAttributeMetaAndValue[ 1]
                    if not ( unNuevoValorAttribute == unValorAttribute):
                        self.setAttributeValueByName( unNombreAttribute, unNuevoValorAttribute)  
                        someResults.append( [ unNombreAttribute, unNuevoValorAttribute,  unAttributeMetaAndValue] )                                      
        return someResults        




    security.declareProtected( permissions.ModifyPortalContent, 'setAttributeValueByName')
    def setAttributeValueByName( self, theName, theValue):
        if self.schema.has_key( theName):
            unField  = self.schema[theName]
            unMutator = unField.getMutator( self)
            unMutator( theValue) 
        else:
            if theName == 'title':
                return self.setTitle( theValue)
            elif theName == 'text':
                return self.setText( theValue)
            elif theName == 'description':
                return self.setDescription( theValue)
            else:
                return self.__setattribute__(theName, theValue)
        







    security.declarePublic('getAttributesMetaAndValues')
    def getAttributesMetaAndValues(self , losNombresAttributes=""):
        if not losNombresAttributes:
            return []

        unResult = [ ]
        
        for unNombreAttribute in losNombresAttributes:
            unAttributeMetaAndValue = self.getAttributeMetaAndValue( unNombreAttribute)
            if unAttributeMetaAndValue:
                unResult.append( unAttributeMetaAndValue)
            
        return unResult        








# #############################################################
# Relation metainfo accesor methods  
#
    
    security.declarePublic('getReferenceMeta')
    def getReferenceMeta(self , elNombreReference=""):
        if not elNombreReference:
            return []

        unSchema = self.schema
        if not unSchema.has_key( elNombreReference):
            return []
            
        unField             = unSchema[ elNombreReference]
        unWidget            = unField.widget
        unaLabel            = unWidget.label
        unaDescription      = unWidget.description
        unaDescriptionMsgId = unWidget.description_msgid
        unaLabelMsgId       = unWidget.label_msgid
        unEsMultiValued     = unField.multiValued
        
        unResult = [ elNombreReference, None , unaLabel, unaLabelMsgId, unaDescription, unaDescriptionMsgId, unEsMultiValued, unField, unWidget, ]
        
        return unResult        
        
    








# #############################################################
# Relation accesor methods for combined info and metainfo 
#
    
    security.declarePublic('getReferenceMetaAndValue')
    def getReferenceMetaAndValue(self , elNombreReference=""):
        if not elNombreReference:
            return []
            
        unReferenceMeta = self.getReferenceMeta( elNombreReference)
        if not unReferenceMeta:
            return []
            
        unField             = unReferenceMeta[ 7]
        unEsMultiValued     = unReferenceMeta[ 6]
        
        unAccessor  = unField.getAccessor( self)
        unValue     = unAccessor()    
        
        unResult = [] + unReferenceMeta
        
        if unEsMultiValued:
            unResult[ 1] =  unValue
        else:
            unResult[ 1] =  [ unValue]
        
        return unResult        
        
    


    security.declarePublic('getReferencesMetaAndValues')
    def getReferencesMetaAndValues(self , losNombresReferences=[]):
        if not losNombresReferences:
            return []

        unResult = [ ]
        
        for unNombreReference in losNombresReferences:
            unReferenceMetaAndValue = self.getReferenceMetaAndValue( unNombreReference)
            if unReferenceMetaAndValue:
                unResult.append( unReferenceMetaAndValue)
            
        return unResult        




      
        


               
                      
             
###########################
#  Traversal config accessors
###########################            
          


           

      
    security.declarePublic('getTraversalConfig')
    def getTraversalConfig(self):
        
        unEditableConfigScriptName = self.traversalConfigScriptName()
        if unEditableConfigScriptName:
            unaConfig = self.traversalConfig_FromScript( unEditableConfigScriptName)
            if unaConfig:
                return unaConfig

        unRaiz = self.getRaiz()
        if not unRaiz:
            return None
       
        unaConfig = None
        try:
            unaConfig = unRaiz.traversalConfig()
        except:
            None
        return unaConfig
           



   



    security.declarePublic('traversalConfigScriptName')
    def traversalConfigScriptName(self):
        unRaiz = self.getRaiz()
        if not unRaiz:
            return None
         
        unTraversalConfigScriptName =  "%s_TraversalConfig_FromScript" % unRaiz.meta_type
        return unTraversalConfigScriptName






    security.declarePublic('TraversalConfig_FromScript')
    def traversalConfig_FromScript( self, theTraversalConfigName):
        if theTraversalConfigName is None or len( theTraversalConfigName) < 1:
            return None        

        aScript   = None
        try:
            aScript = self.unrestrictedTraverse(theTraversalConfigName)
        except:
            None
            
        if not aScript:
            return None

        aContext          = aq_inner(self)  
        if not aContext:
            return None
                     
        aScriptInContext  = aScript.__of__(aContext)
        if not aScriptInContext:
            return None
        
        anTraversalConfig = aScriptInContext()       
        if anTraversalConfig is None or len( anTraversalConfig) < 1:
            return None 
                   
        return anTraversalConfig

    

          








    # #############################################################
    """Metainfo access methods not directly available on instances from templates or scripts.
    
    """


    security.declarePublic('getModule')
    def getModule(self):
        return __module__
        



    security.declarePublic('getClassName')
    def getClassName(self):
        return self.__class__.__name__
        
        
        
    security.declarePublic('getMethods')
    def getMethods(self):
        return dir(self)
        
        
    security.declarePublic('getDoc')
    def getDoc(self):
        return self.__doc__
        
        
        
        
    
    
 
    
    
    
    # #############################################################
    """Internationalization methods.
    
    """
    



    security.declarePublic( 'fTranslationServiceTool')
    def fTranslationServiceTool( self, ):
        return getToolByName( self, 'translation_service', None)
    
    
    
    
    


    security.declarePublic( 'fTranslateI18NManyIntoDict')
    def fTranslateI18NManyIntoDict( self, 
        theI18NDomainsStringsAndDefaults, 
        theResultDict                   =None):
        """Internationalization: build or update a dictionaty with the translations of all requested strings from the specified domain into the language preferred by the connected user, or return the supplied default.
        
        """
        
        unResultDict = theResultDict
        if ( unResultDict == None):
            unResultDict = { }
                
        if not theI18NDomainsStringsAndDefaults:
            return unResultDict
        
        aTranslationService = getToolByName( self, 'translation_service', None)
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

    


    security.declarePublic( 'fTranslateI18N')
    def fTranslateI18N( self, theI18NDomain, theString, theDefault, theTranslationService=None):
        """Internationalization: return the translated string from the specific domain into the language preferred by the connected user, or return the supplied default.
        
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
            aTranslationService = getToolByName( self, 'translation_service', None)
            
        aTranslation = theDefault
        if aTranslationService:
            aTranslation = aTranslationService.utranslate( aI18NDomain, theString, mapping=None, context=self , target_language= None, default=theDefault)            
           
        if not aTranslation:
            aTranslation = theDefault

        if not aTranslation:
            aTranslation = theString

        return aTranslation
        
           



    security.declarePublic( 'fAsUnicode')
    def fAsUnicode( self, theString):
        """Return the parameter, expected to be encoded in the plone site default encoding, decoded into a unicode string.
        
        """
        
        if not theString:
            return u''

        aTranslationService = getToolByName( self, 'translation_service', None)


        aUnicodeString = aTranslationService.asunicodetype( theString, errors="ignore")
        if not aUnicodeString:
            aUnicodeString = theString
        
        return aUnicodeString
        
                
                
                






  
    security.declarePrivate( 'fEsCreacionSimple')
    def fEsCreacionSimple(self, theFieldName, theTypeName):  
        unaFactoryView = self.fFactoryViewForType( theFieldName, theTypeName) 
        if not unaFactoryView:
            return False
        return True
        
        
     


    security.declarePrivate( 'fFactoryViewForType')
    def fFactoryViewForType(self, theFieldName, theTypeName, ):   
        unSchema = self.schema
        if not unSchema.has_key( theFieldName):
            return ''
            
        unField             = unSchema[ theFieldName]
         
        unosFactoryViews = {}
        try:
            unosFactoryViews = unField.factory_views
        except:
            None
            
        if not unosFactoryViews or not unosFactoryViews.has_key( theTypeName):
            return ''
            
        unaFactoryView = unosFactoryViews[ theTypeName]
 
        return unaFactoryView
                



            
            
#   fTFL stands for function for Translated Field Label
#   will be used in the context of expressions of computed archetype schema fields
#   the short name is to use less space
#   in the tagged value edition fields
#   of case tools            
    security.declarePrivate('fTFL')
    def fTFL(self, theFieldName):
        if not theFieldName:
            return ''
            
        aSchema = self.schema
        if not aSchema.has_key( theFieldName):
            return theFieldName
       
        aField = aSchema.get( theFieldName)
        if not aField:
            return theFieldName
            
        aWidget = aField.widget
        if not aWidget:
            return theFieldName
        
        aMsgId = aWidget.label_msgid
        if not aMsgId:
            return theFieldName
        
        anI18NDomain = self.getNombreProyecto()   
        if not anI18NDomain:
            return theFieldName

        aTranslationService = None
        try:
            aTranslationService = self.translation_service
        except:
            None
        if not aTranslationService:
            return theFieldName
            
        aTranslation = aTranslationService.utranslate( anI18NDomain, aMsgId, mapping=None, context=self , target_language= None, default=theFieldName)                       
        if not aTranslation:
            return theFieldName

        return aTranslation
    
 
 
#   fTFLVs stands for function for multiple  Translated Field Label and Value
#   will be used in the context of expressions of computed archetype schema fields
#   the short name is to use less space
#   in the tagged value edition fields
#   of case tools            
    security.declarePrivate('fTFLVs')
    def fTFLVs(self, theFieldNames):
        if not theFieldNames:
            return ''
        
        someFieldLabelsAndValues = []
        for unFieldName in theFieldNames:
            unFieldLabelAndValue = self.fTFLV( unFieldName)
            if unFieldLabelAndValue:
                someFieldLabelsAndValues.append( unFieldLabelAndValue)

        if not someFieldLabelsAndValues:
            return ''
            
        unResultString = '; '.join( someFieldLabelsAndValues)

        return unResultString
            

 
#   fTFLVsUnless stands for function for multiple  Translated Field Label and Value
#   will be used in the context of expressions of computed archetype schema fields
#   the short name is to use less space
#   in the tagged value edition fields
#   of case tools            
    security.declarePrivate('fTFLVs')
    def fTFLVsUnless(self, theFieldNamesAndExcludeValues):
        if not theFieldNames:
            return ''
        
        someFieldLabelsAndValues = []
        for unFieldName, unExcludeValue in theFieldNamesAndExcludeValues:
            unFieldLabelAndValue = self.fTFLVUnless( unFieldName, unExcludeValue)
            if unFieldLabelAndValue:
                someFieldLabelsAndValues.append( unFieldLabelAndValue)

        if not someFieldLabelsAndValues:
            return ''
            
        unResultString = '; '.join( someFieldLabelsAndValues)

        return unResultString
            

    
    
#   fTFLV stands for function for Translated Field Label and Value
#   will be used in the context of expressions of computed archetype schema fields
#   the short name is to use less space
#   in the tagged value edition fields
#   of case tools            
    security.declarePrivate('fTFLV')
    def fTFLV(self, theFieldName):
        if not theFieldName:
            return ''

        aTranslatedLabel = self.fTFL( theFieldName)
        if not aTranslatedLabel:
            aTranslatedLabel = ''         
    
        unValueString = self.fFV( theFieldName)
        if not unValueString:
            return ''
            
        return aTranslatedLabel + ' ' + unValueString
             

    

    
#   fTFLVUnless stands for function for Translated Field Label and Value
#   will be used in the context of expressions of computed archetype schema fields
#   the short name is to use less space
#   in the tagged value edition fields
#   of case tools            
    security.declarePrivate('fTFLV')
    def fTFLVUnless(self, theFieldName, theExcludeValueString):
        if not theFieldName:
            return ''

        unValueString = self.fFV( theFieldName)
        if not unValueString:
            return ''
        
        if unValueString == theExcludeValueString:
            return ''
            
        aTranslatedLabel = self.fTFL( theFieldName)
        if not aTranslatedLabel:
            aTranslatedLabel = ''         
    
        return aTranslatedLabel + ' ' + unValueString
             
    
    
#   fFV stands for function for  Field Value
#   will be used in the context of expressions of computed archetype schema fields
#   the short name is to use less space
#   in the tagged value edition fields
#   of case tools            
    security.declarePrivate('fFV')
    def fFV(self, theFieldName):
        if not theFieldName:
            return ''

        unSchema = self.schema
        if not unSchema.has_key( theFieldName):
            return ''
            
        unField  = unSchema[ theFieldName]
        if not unField:
            return ''

        unAccessor = unField.getAccessor( self)
        if not unAccessor:
            return ''

        unValue = unAccessor()
        if ( unValue == None):
            return ''
            
        if unField.__class__.__name__ in ( 'RelationField', 'ReferenceField'):
            unIsMultiValued = unField.multiValued
            if not unIsMultiValued: 
                if not unValue:
                    return ''
                unTitle = unValue.Title()
                if not unTitle:
                    return ''
                return unTitle
            else:
                unosTitulos = []
                if unValue:
                    for unElement in unValue:
                        unTitle = unElement.Title()
                        if unTitle:
                            unosTitulos.append( unTitle)
                if not unosTitulos:
                    return ''
                unosTitulosString = ', '.join( unosTitulos)
                return unosTitulosString
                                             
        
                        
        unElementFieldType      = unField.type
        
        if unElementFieldType == 'computed':
            unElementFieldType = 'string'
                    
        unValueString = ''
                            
        unWidget = unField.widget
        if unWidget and (unWidget.getType() == 'Products.Archetypes.Widget.SelectionWidget') and unField.__dict__.has_key('vocabulary'):    
            unValueString = unValue    
            someVocabularyOptions   = []
            try:
                someVocabularyOptions = unField.vocabulary   
            except:
                None
                
            someVocabularyMsgIds = []
            try:
                someVocabularyMsgIds = unField.vocabulary_msgids   
            except:
                None
                
            aTranslationService = None
            try:
                aTranslationService = self.translation_service
            except:
                None

            anI18NDomain = self.getNombreProyecto()   
                
            if someVocabularyOptions and someVocabularyMsgIds and aTranslationService and anI18NDomain:
                if unValue in someVocabularyOptions:
                    unValueIndex = someVocabularyOptions.index( unValue)
                    if (unValueIndex >= 0) and ( unValueIndex < len( someVocabularyMsgIds)):
                        unValueMsgId = someVocabularyMsgIds[ unValueIndex]
                        aTranslation = aTranslationService.utranslate( anI18NDomain, unValueMsgId, mapping=None, context=self , target_language= None, default=unValueString)                       
                        if aTranslation:
                            unValueString = aTranslation                                               
                   
        elif unElementFieldType in[  'string', 'text']:            
            unValueString = unValue
            
        elif unElementFieldType == 'boolean':
            unValueString = str( unValue)
        
            aTranslationService = None
            try:
                aTranslationService = self.translation_service
            except:
                None

            anI18NDomain = self.getNombreProyecto() 
              
            if aTranslationService and anI18NDomain:
                if unValue:
                    aTranslation = aTranslationService.utranslate( 'ModelDDvlPlone', 'ModelDDvlPlone_True', mapping=None, context=self , target_language= None, default=unValueString)                       
                    if aTranslation:
                        unValueString = aTranslation
                else:
                    aTranslation = aTranslationService.utranslate( 'ModelDDvlPlone', 'ModelDDvlPlone_False', mapping=None, context=self , target_language= None, default=unValueString)                       
                    if aTranslation:
                        unValueString = aTranslation
                        
        elif unElementFieldType == 'integer':
            unValueString  = str( unValue)
            
        elif unElementFieldType == 'float':
            unValueString  = str( unValue)

        elif unElementFieldType == 'fixedpoint':
            unValueString  = str( unValue)

        elif unElementFieldType == 'datetime':
            unValueString  = str( unValue)
        
        else:
            unValueString  = str( unValue)
    
        return unValueString
    
    
    

# ###################################
#   System encoding 
#         
# ###################################
     
    security.declarePrivate( 'fSystemTextFileEncoding')    
    def fSystemTextFileEncoding( self, ):
        return cSystemFileTextEncoding
    
     
    
    security.declarePrivate( 'fLogEncoding')    
    def fLogEncoding( self, ):
        return self.fSystemTextFileEncoding()
    
        
         
        
     
    

# ###################################
#   Application-specific logging methods
#         
# ###################################
     
    
   
    
    
    
    
    
    security.declarePrivate( 'pLogChange')    
    def pLogChange( self, theChangeDescriptionString, theEncoding='', theTranslationService=None):
        if not theChangeDescriptionString:
            return self
        
        unEncodedString = cfEncodeLogString( self, theChangeDescriptionString)
 
        logging.getLogger( 'gvSIGi18n::pLogChange').info( unEncodedString)
        return self
    
       

    
    
    
    
    security.declarePrivate( 'pLogHTTPRequest')    
    def pLogHTTPRequest( self, theLogRequesterLabel ):
        
        anHTTPRequest = self.REQUEST
        if not anHTTPRequest:
            return self
        
        unDumpBuffer = StringIO()
        unaForm = anHTTPRequest.form
        if not unaForm:
            logging.getLogger( theLogRequesterLabel).info( "theRequest: NO FORM\n")
            return self

        unasFormKeys = unaForm.keys()
        unMaxKeyLen = max( [ len( unaKey) for unaKey in unasFormKeys])
        for unaFormKey in unasFormKeys:
            unDumpBuffer.write( '%s%s %s\n' % ( unaFormKey, '' * ( unMaxKeyLen - len( unaFormKey)), unaForm.get( unaFormKey, ''),))

        logging.getLogger( theLogRequesterLabel).info( "theRequest:\n%s\n" % unDumpBuffer.getvalue())
        
        return self


    
    
    
    
 
    
    
    
       
       

       



# #################################
#  Rendering methods
# ###############################

  

# ###########################################
#  HTML formatting methods
# ###########################################

    
 
    security.declarePrivate( 'fText2HTML_collapsible')
    def fText2HTML_collapsible(self, theString, theCollapsibleTitle, theCollapsibleId, theCollapse=True):
        if not theString:
            return ''
        
        anOutput = StringIO()
        
        self.pRenderCollapsible_Lambda( anOutput, theCollapsibleTitle, theCollapsibleId, lambda : anOutput.write( self.fText2HTML( theString)), theCollapse)

        aResult = anOutput.getvalue()
        
        return aResult
        
    
    

    security.declarePrivate( 'fText2HTML')
    def fText2HTML(self, theString):
       
        if not theString:
            return ''
 
        anHTMLString = '<p>%s</p>' % theString.replace('\n', '\n<br/>\n').replace( cIndent, '&nbsp; ' * len( cIndent)).replace( ' ', '&nbsp;')
        return anHTMLString
        
    
    
 

     
    security.declarePrivate( 'fCRs2BRs')
    def fCRs2BRs(self, theString):
        if not theString:
            return theString
        if theString.__class__.__name__ == 'unicode':
            return theString.replace( u'\n', u'<br/>')
        
        return theString.replace( '\n', '<br/>')

    

    
    security.declarePrivate( 'fHTMLCollapsible')
    def fHTMLCollapsible(self, theString, theCollapsibleTitle, theCollapsibleId, theCollapse=True):
        if not theString:
            return ''
        
        anOutput = StringIO()
        
        self.pRenderCollapsible_Lambda( anOutput, theCollapsibleTitle, theCollapsibleId, lambda : anOutput.write(theString), theCollapse)

        aResult = anOutput.getvalue()
        
        return aResult
        
        
    
    def pRenderCollapsible_Lambda( self, anOutput, theCollapsibleTitle, theCollapsibleId, theLambda, theCollapse=True):
                
        unCollapsedOrExpanded = ( theCollapse and 'collapsed') or 'expanded'
            
        anOutput.write( u"""  
            
            <!-- ######### Start collapsible  section ######### --> 
            <dl id="%(pCollapsibleId)s" class="collapsible inline %(unCollapsedOrExpanded)sInlineCollapsible">
                <dt class="collapsibleHeader">
                    <strong>%(pCollapsibleTitle)s</strong>
                </dt>
                <dd class="collapsibleContent">    
                \n""" % {
            'unCollapsedOrExpanded':  unCollapsedOrExpanded,
            'pCollapsibleTitle':      theCollapsibleTitle,
            'pCollapsibleId':         theCollapsibleId,
        })
        
        theLambda()
         
        anOutput.write( u"""  
                </dd>
            </dl>
            <!-- ######### End collapsible  section ######### --> 
            \n"""
        )
        
        return None        
 
   
    
    
    
    
    security.declarePrivate( 'fUsersInGroupId')
    def fUsersInGroupId(self, theGroupId):
        if not theGroupId:
            return []
        
        unPortalGroupsTool = self.getGroupsTool()
        if not unPortalGroupsTool:
            return unInforme
        
        unosGroupMembers = unPortalGroupsTool.getGroupMembers( theGroupId)
        return unosGroupMembers
    
    
    
    
    
    
    
    
    
# ##################################################################
# Rendering of OLD STYLE of Time Profiling  (still used in ModelDDvlPlone
# ##################################################################
        
    
    security.declarePrivate( 'fPrettyPrintProfilingResultHTML')
    def fPrettyPrintProfilingResultHTML(self, theProfilingResult):
       
        if not theProfilingResult:
            return ''
    
        aResult = self.fPrettyPrintProfilingResult( theProfilingResult)
        if not aResult:
            return ''
        return self.fText2HTML( aResult)
    

        
        
        
    security.declarePrivate( 'fPrettyPrintProfilingResult')
    def fPrettyPrintProfilingResult(self, theProfilingResult):
    
        if not theProfilingResult:
            return ''

        anOutput = StringIO()
        
        self.pPrettyPrintProfilingResult( anOutput, theProfilingResult, 0)
        aResult = anOutput.getvalue()
        
        return aResult
 
 
        

        
        

    security.declarePrivate( 'pPrettyPrintProfilingResult')
    def pPrettyPrintProfilingResult(self, theOutput, theProfilingResult, theIndentLevel, theMaxTimeWidth=0):
        if not theProfilingResult:
            return self
            
        if theIndentLevel:
            theOutput.write(  cIndent *  theIndentLevel)
                    
        unMethodName    = theProfilingResult[ 0]
        unExecTime      = theProfilingResult[ 1]
        someSubResults  = theProfilingResult[ 2]

        unTimeFiller = ''
        unaLenTime = len( str( unExecTime))
        if unaLenTime < theMaxTimeWidth:
            unTimeFiller = ' ' * ( theMaxTimeWidth - unaLenTime)
            
        if not someSubResults:
            theOutput.write( '[%s%d %s]\n' % ( unTimeFiller, unExecTime, unMethodName))            
        else:
            theOutput.write( '[%s%d %s\n' % ( unTimeFiller, unExecTime, unMethodName)) 
            
            unosSubTiempos = [ unSub[ 1] for unSub in someSubResults]
            unaSumaTiempos = sum( unosSubTiempos)
            unMaxSubTiempo = max( [ ( unExecTime - unaSumaTiempos) > 0,] + unosSubTiempos)
            
            if unaSumaTiempos < unExecTime:
                if theIndentLevel:
                    theOutput.write(  cIndent *  ( theIndentLevel + 1))
                theOutput.write( ' %s%d -own-\n' % ( ' ' * ( theMaxTimeWidth - len( str( unExecTime - unaSumaTiempos))), unExecTime - unaSumaTiempos))            
             
            for aSubProfilingResult in someSubResults:                       
                self.pPrettyPrintProfilingResult( theOutput, aSubProfilingResult, theIndentLevel + 1, len( str( unMaxSubTiempo)))
                
            if theIndentLevel:
                theOutput.write(  cIndent *  theIndentLevel)
            theOutput.write( ']\n')            
        
        return self      
       
               
                     
         
    
 

    


   
    security.declarePrivate( 'fModelDDvlPloneTool')
    def fModelDDvlPloneTool( self, theAllowCreation=False):
        """Retrieve or create an instance of ModelDDvlPloneTool.
        
        """
        try:
    
            # ACV 2009092 Seems easier to use the getToolByName, otherwise the commented code works ok
            # Changed when eliminating arbitrary instantiations of ModelDDvlPloneTool, 
            # rather than looking up the tool singleton
            # Now, those cases retrieve the tool invoking this function
            #
           
            #aModelDDvlPloneTool = None
            #try:
                #aModelDDvlPloneTool = aq_get( unPortalRoot, cModelDDvlPloneToolId, None, 1)
            #except:
                #None  
            
            
            aModelDDvlPloneTool = getToolByName( self, 'ModelDDvlPlone_tool', None)
            
            if aModelDDvlPloneTool:
                return aModelDDvlPloneTool
            
            if not ( theAllowCreation and cLazyCreateModelDDvlPloneTool):
                return None
     
            unPortalRoot = self.fPortalRoot()
            if not unPortalRoot:
                return None
             
            unaNuevaTool = ModelDDvlPloneTool( ) 
            unPortalRoot._setObject( cModelDDvlPloneToolId,  unaNuevaTool)
            aModelDDvlPloneTool = None
            
            #try:
                #aModelDDvlPloneTool = aq_get( unPortalRoot, cModelDDvlPloneToolId, None, 1)
            #except:
                #None  
                
            aModelDDvlPloneTool = getToolByName( self, 'ModelDDvlPlone_tool', None)
            if not aModelDDvlPloneTool:
                return None
                        
            return aModelDDvlPloneTool
        
        except:
            unaExceptionInfo = sys.exc_info()
            unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
            
            unInformeExcepcion = 'Exception during Lazy Initialization operation fModelDDvlPloneTool\n' 
            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
            unInformeExcepcion += unaExceptionFormattedTraceback   
                     
     
            if cLogExceptions:
                logging.getLogger( 'gvSIGi18n').error( unInformeExcepcion)
    
            return None
             

        
            
        
        
        
    security.declarePrivate( 'pHandle_manage_pasteObjects')        
    def pHandle_manage_pasteObjects(self, cb_copy_data=None, REQUEST=None):
        """Trap and override behavior of manage_pasteObjects implementation in CopySupport.py 
        
        """
        return None
    
        # ACV 20091216 Should not paste nothing on no TRA element
        ## Get the list of objects to be copied into this (self) container
        ## Copied from class CopyContainer in file Zope lib python OFS  CopySupport.py
        #if cb_copy_data is not None:
            #cp = cb_copy_data
        #elif REQUEST is not None and REQUEST.has_key('__cp'):
            #cp = REQUEST['__cp']
        #else:
            #cp = None
        #if cp is None:
            #return CopyContainer.manage_objectPaste( self, cb_copy_data, REQUEST)
             
        #try:
            #op, mdatas = loads(decompress(unquote(cp))) # _cb_decode(cp)
        #except:
            #return CopyContainer.manage_objectPaste( self, cb_copy_data, REQUEST)

    
        #oblist = []
        #app = self.getPhysicalRoot()
        #for mdata in mdatas:
            #m = Moniker.loadMoniker(mdata)
            #try:
                #ob = m.bind(app)
            #except:
                #return CopyContainer.manage_objectPaste( self, cb_copy_data, REQUEST)
            ## Do not verify here
            ## self._verifyObjectPaste(ob, validate_src=op+1)
            #oblist.append(ob)
        ## End of code copied from class CopyContainer
            
        #someObjectsToPaste = oblist[:]
        
        #if not someObjectsToPaste:
            #return CopyContainer.manage_objectPaste( self, cb_copy_data, REQUEST)
        
        #someAwareObjects = []
        #for anObjectToPaste in someObjectsToPaste:
            #anExportConfig = None
            #try:
                #anExportConfig = anObjectToPaste.exportConfig()
            #except:
                #None
            #if anExportConfig:
                #someAwareObjects.append( anObjectToPaste)
                
        #if not someAwareObjects:
            #return CopyContainer.manage_objectPaste( self, cb_copy_data, REQUEST)
        
        
        #aRequest = REQUEST
        #if not aRequest:
            #try:
                #aRequest = self.REQUEST
            #except:
                #None
        #if not aRequest:
            #"""Default to Plone behavior.
            
            #"""
            #return CopyContainer.manage_pasteObjects( self, cb_copy_data, REQUEST)
        
        
        #unModelDDvlPloneTool = self.fModelDDvlPloneTool( True)
        #if not unModelDDvlPloneTool:
            #return CopyContainer.manage_pasteObjects( self, cb_copy_data, REQUEST)
        
        #return unModelDDvlPloneTool.fPaste( 
            #theTimeProfilingResults     =None,
            #theContainerObject          =self, 
            #theObjectsToPaste           =someObjectsToPaste,
            #theAdditionalParams         =None,
        #)
    
        ## return CopyContainer.manage_pasteObjects( self, cb_copy_data, REQUEST)
        ## aRequest.response.redirect( '%s/MDDpaste' % self.absolute_url())
        
        
        
       
        
    
        
        
    security.declarePrivate('pFlushCachedTemplates')
    def pFlushCachedTemplates(self,  theViewsToFlush=[]):
        unModelDDvlPloneTool = self.fModelDDvlPloneTool()
        if not unModelDDvlPloneTool:
            return self
        
        unModelDDvlPloneTool.pFlushCachedTemplatesForImpactedElementsUIDs( self, [ self.UID(),], theViewsToFlush=theViewsToFlush)

        return self

           
    
    

    security.declarePrivate('pFlushCachedTemplates_All')
    def pFlushCachedTemplates_All(self, theViewsToFlush=[]):
        
        unModelDDvlPloneTool = self.fModelDDvlPloneTool()
        if not unModelDDvlPloneTool:
            return self

        someUIDs = self.fAllElementUIDs()
        if someUIDs:        
            unModelDDvlPloneTool.pFlushCachedTemplatesForImpactedElementsUIDs( self, someUIDs, theViewsToFlush=theViewsToFlush)

        return self
        
    
    
   
        
    security.declarePrivate('fAllElementUIDs')
    def fAllElementUIDs(self,):
        
        someUIDs = [ ]
        
        unPortalCatalog = getToolByName( self, 'portal_catalog')
        
        unPhysicalPath = self.fPhysicalPathString()

        unaBusqueda = { 
            'path' :    unPhysicalPath,
        }
 
        unosResultadosBusqueda = unPortalCatalog.searchResults( **unaBusqueda)
        for unResultadoBusqueda in unosResultadosBusqueda:
            if unResultadoBusqueda:
                aFoundObject = unResultadoBusqueda.getObject()
                if not ( aFoundObject == None):
                    unaUID =  ''
                    try:
                        unaUID = aFoundObject.UID()
                    except:
                        None
                    if unaUID:
                        someUIDs.append( unaUID)        

        return someUIDs
        
      
            
    

    # ####################################################
    """Methods for safe evaluation of strings.
    
    """
        
    
    def fDefaultEvalStringGlobalsDict(self, ):
        return { '__builtins__':None, 'True': True, 'False': False, 'None': None, 'DateTime': DateTime,}.copy()
        
    
    
    def fEvalString(self, theString, theExtraGlobals={}):
        if not theString:
            return None
        
        unGlobalsDict = self.fDefaultEvalStringGlobalsDict()
        if not unGlobalsDict:
            unGlobalsDict = { '__builtins__':None, }
            
        unGlobalsDict = unGlobalsDict.copy()
        if theExtraGlobals:
            unGlobalsDict.update( theExtraGlobals)
            
        unValue = None
        try:
            unValue = eval( theString, unGlobalsDict)
        except:
            unGlobalsString = str( unGlobalsDict.keys()).replace( '[', '').replace( ']', '')
            logging.getLogger( 'ModelDDvlPlone').error( 'fEvalString( "%s", { %s })' % ( str( theString), unGlobalsString))
            
        return unValue
     