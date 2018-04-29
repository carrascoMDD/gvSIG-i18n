# -*- coding: utf-8 -*-
#
# File: TRAExecutionRecord.py
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


import cgi
import logging

import time  


from StringIO                   import StringIO

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

from TRACatalogo_Globales import TRACatalogo_Globales

            
    

            
# ########################################################################################################
            
class TRAExecutionRecord:
    """Record the execution of each relevant template or method.
        
    """
    
    def __init__( self,
        theEnablementConfiguration,
        theContextualObject, 
        theExecutedKind, 
        theExecutedName, 
        theParentExecutionRecord, 
        theProfilingConfig={}, 
        theExtraExecutionInfo=''):
        
        self.vEnablementConfiguration = theEnablementConfiguration
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
        
        
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
                
        
        try:
            if self.vEnablementConfiguration.get( 'execution_profiling_enabled', False) or self.vEnablementConfiguration.get( 'execution_timestamping_enabled', False):
                
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


            if self.vEnablementConfiguration.get( 'execution_timestamping_enabled', False):
                self.vExecutionStartTime    = int( time.time() * 1000)
            
            if self.vEnablementConfiguration.get( 'execution_profiling_enabled', False):
                
                if not theParentExecutionRecord or not theParentExecutionRecord.vIsExcluded:
                    
                    if theExecutedName in self.vProfilingConfig.get( 'excluded', []):
                        self.vIsExcluded = True       
                    else:
                        if theParentExecutionRecord:
                            aIsExecutionRecord = False
                            try:
                                aIsExecutionRecord = theParentExecutionRecord.fIsExecutionRecord()                            
                            except:
                                None
                                
                            if aIsExecutionRecord:
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
    

            
            
            
            
    def fIsExecutionRecord( self,):
        return True
    
    
    
    
    def addExtraInfo( self, theExtraExecutionInfo):
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        if not self.vInitialized or not theExtraExecutionInfo:
            return self
        
        if self.vExtraExecutionInfo == None:
            self.vExtraExecutionInfo = [ ]
        
        self.vExtraExecutionInfo.append( theExtraExecutionInfo)
        
        return self 
    

    
    
    def addChild( self, theChild):
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
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
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        
        try:
            if not self.vInitialized:
                return self
            
            if  self.vEnablementConfiguration.get( 'execution_timestamping_enabled', False):
                self.vExecutionEndTime  =  int( time.time() * 1000)
            
            if  self.vEnablementConfiguration.get( 'execution_profiling_enabled', False):
                self.pLogPerformance( )
                    
            return self   
        
        except:
            None


    def pRecordExceptionInChildren( self):
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        self.vExceptionsInChildren = True
        if self.vParent:
            self.vParent.pRecordExceptionInChildren()
        return self
    
        
    
    
    def pRecordException( self,  theExceptionReport):
        """Record an exception report trapped in this execution.
        """
        
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
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
        
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        try:
            if not self.vInitialized:
                return self
            
            unPrintString          = ''
            unTimestampPrintString = ''
            unLogPrintString       = ''
            
            if self.vEnablementConfiguration.get( 'execution_profiling_enabled', False):
                
                if self.vEnablementConfiguration.get( 'execution_timestamping_enabled', False):
                    aWhenToLog = self.vProfilingConfig.get( 'log_when', False)
                    if aWhenToLog == True or ( ( aWhenToLog == 'root') and not self.vParent):
                        unTimestampPrintString = self.fPrintExecutionTimestampString( )
                    
                    
                    
                if self.vEnablementConfiguration.get( 'execution_logging_enabled', False):
                    
                    aWhenToLog = self.vProfilingConfig.get( 'log_when', False)
                    if aWhenToLog == True or ( ( aWhenToLog == 'root') and not self.vParent):
                        
                        if self.vProfilingConfig.get( 'log_what', '') == 'details' and self.vEnablementConfiguration.get( 'execution_logging_detailed_enabled', False):
                            unLogPrintString = self.fPrintExecutionRecordStringDetails( True)
                            
                        elif self.vEnablementConfiguration.get( 'execution_logging_detailed_enabled', False) and self.vProfilingConfig.get( 'log_what', '') == 'dots':
                            unLogPrintString = self.fPrintExecutionRecordStringDots( True)
                            
                        else:
                            unLogPrintString = self.fPrintExecutionRecordString( )
        

                if unTimestampPrintString and unLogPrintString:
                    unPrintString = '\n%s\%s' %  ( unTimestampPrintString, unLogPrintString,)
                    
                elif unTimestampPrintString:
                    unPrintString = unTimestampPrintString
                    
                elif unLogPrintString:
                    unPrintString = unLogPrintString
                    
                    
                    
            if unPrintString:       
                unEncodedString = self.vContextualObject.fEncodeLogString( unPrintString)
                logging.getLogger( 'gvSIGi18n').info( unEncodedString)
                
                self.setLoggedRecursive( True)
                        
    
            return self
        
        except:
            None

    
    

    
    
    
    
    
    
    def setLoggedRecursive( self, theLogged=True):

        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
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

        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        try:
            if not self.vInitialized:
                return self
            
            self.vLogged = False
            for unChild in ( self.vChildren or []):
                unChild.pClearLoggedAll( )
            
            return self
        
        except:
            None

    

    def fPrintExecutionTimestampString( self,):
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        try:
            if self.vInitialized:
                return '%d ms (start %s  -  end %s) %s %s %s %s %s' % (      
                    self.vExecutionEndTime - self.vExecutionStartTime,
                    self.vContextualObject.fDateTimeFromMillisecondsTextual( self.vExecutionStartTime),
                    self.vContextualObject.fDateTimeFromMillisecondsTextual( self.vExecutionEndTime),                    
                    self.vExecutedKind or '', 
                    self.vExecutedName or '', 
                    self.vContextualObjectClassName or '',
                    self.vContextualObjectTitle or '',
                    self.vContextualObjectPath   or '',
                )
        except:
            return 'exception printing execution timestamp'
        
        return ''
    
    
    
    

    def fPrintExecutionRecordString(self, ):

        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        try:
            if self.vInitialized:
                return '%d ms  (start %s end %s) %s %s %s %s %s %s %s' % (      
                    self.vExecutionEndTime - self.vExecutionStartTime, 
                    self.vContextualObject.fDateTimeFromMillisecondsTextual( self.vExecutionStartTime),
                    self.vContextualObject.fDateTimeFromMillisecondsTextual( self.vExecutionEndTime),                    
                    ( self.vExceptions and '!!!') or '',
                    self.vExecutedKind or 'unknown_executed_kind', 
                    self.vExecutedName or 'unknown_executed_name', 
                    self.vContextualObjectClassName or 'unknown_object_class_name',
                    self.vContextualObjectTitle or 'unknown_object_title',
                    self.vContextualObjectPath   or 'unknown_object_path',
                    ' '.join( self.vExtraExecutionInfo or []),
                )
        except:
            return 'exception printing execution record'
    
        return ''
            

    
    def fPrintExecutionRecordStringDots(self,):

        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        try:
            if not self.vInitialized:
                return self
            
            theOutput = StringIO()
            
            self.pPrintExecutionRecordDotsOn( theOutput,)
       
            unString = theOutput.getvalue()
            return unString
        
        except:
            None

        return ''
    
    
    
    
    def fPrintExecutionRecordStringDetails(self, theIsForLog=False):

        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        try:
            if not self.vInitialized:
                return self
            
            theOutput = StringIO()
            
            unaTimeWidth = len( str( ( self.vExecutionEndTime or  self.vExecutionStartTime) - self.vExecutionStartTime))
            self.pPrintExecutionRecordDetailsOn( theOutput, theIsForLog, '', unaTimeWidth)
       
            unString = theOutput.getvalue()
            return unString
        
        except:
            None

        return '' 
            

            
      
    
    

    def pPrintExecutionRecordDotsOn(self, theOutput):
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
        if not self.vInitialized:
            return self
        
        theOutput.write( '.')
        for unChild in ( self.vChildren or []):
            unChild.pPrintExecutionRecordDotsOn( theOutput)
        return self      
       
    
              
            
            
                 
    
    def pPrintExecutionRecordDetailsOn(self, theOutput,  theIsForLog=False, theIndentString='', theMaxTimeWidth=0):
        
        if TRACatalogo_Globales.gTRAExecutionProfilingIgnored:
            return None
        
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
                theOutput.write( '[%s%s]\n' % ( unTimeFiller, self.fPrintExecutionRecordString())) 
            else:
                theOutput.write( '[%s%s\n' % ( unTimeFiller, self.fPrintExecutionRecordString())) 
                for unaException in self.vExceptions:
                    theOutput.write( '%s%s%s\n' % ( theIndentString, str( unaException))) 
                    
                
        else:
            theOutput.write( '[%s%s\n' % ( unTimeFiller, self.fPrintExecutionRecordString()))     
            
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
                aSubProfilingResult.pPrintExecutionRecordDetailsOn( theOutput, theIsForLog, unIndentString, unaLenSubTiempos)
                
            if theIndentString:
                theOutput.write(  theIndentString)
            theOutput.write( ']\n')            
        
        return self      
       
               
                     


 
            
     