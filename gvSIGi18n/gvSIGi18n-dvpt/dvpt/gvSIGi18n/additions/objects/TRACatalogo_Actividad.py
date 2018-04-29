# -*- coding: utf-8 -*-
#
# File: TRACatalogo_Actividad.py
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

import sys

import traceback

import logging

import threading

from AccessControl                  import ClassSecurityInfo

from Products.CMFCore               import permissions


from TRACatalogo_Globales import TRACatalogo_Globales

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





class TRACatalogo_Actividad:
    """
    """
    security = ClassSecurityInfo()

    
    


       
    
    security.declarePrivate( 'fRecentActivitiesForRoot')
    def fRecentActivitiesForRoot(self, ):
        """Retrieve the recent activities occurred for the catalog root.
        
        """
        
        unPathDelRaiz = self.fPathDelRaiz()
        if not unPathDelRaiz:
            return None
        
      
        
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            
            if TRACatalogo_Globales.gRecentActivities == None:
                return None
                
            unosRecentActivitiesForRoot = TRACatalogo_Globales.gRecentActivities.get( unPathDelRaiz, None)
            if unosRecentActivitiesForRoot == None:                
                return None
                
            return unosRecentActivitiesForRoot[:]
            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        return self
            
    
       
    
    security.declarePrivate( 'pTranslationActivityOccurred')
    def pTranslationActivityOccurred(self, theTranslationChange):
        """Record recent change, and increment the counter of changes since last generation of the Status Report by Languages.
        
        """
        

        if not theTranslationChange:
            return self
        
        unMaxRecentActivitiesForRoot = 0
        
        unaConfiguracion = self.fObtenerConfiguracion( cTRAConfiguracionAspecto_Varios)
        if unaConfiguracion:        
            unMaxRecentActivitiesForRoot = unaConfiguracion.getMaximoNumeroCambiosRecientes()
        
        unPathDelRaiz = self.fPathDelRaiz()
        if not unPathDelRaiz:
            return self
        
        aTranslationChange = theTranslationChange.copy()
        
        aTranslationChange[ 'path_del_raiz'] = unPathDelRaiz
        
        
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
            
            
            
            # ####################################################################
            """Append change to the list of recent changes, discarding the oldest ones if the maximum is exceeded. 
            
            """
            if TRACatalogo_Globales.gRecentActivities == None:
                TRACatalogo_Globales.gRecentActivities = { }
                
            unosRecentActivitiesForRoot = TRACatalogo_Globales.gRecentActivities.get( unPathDelRaiz, None)
            if unosRecentActivitiesForRoot == None:
                unosRecentActivitiesForRoot = [ ]
                TRACatalogo_Globales.gRecentActivities[ unPathDelRaiz] = unosRecentActivitiesForRoot
                
            if unMaxRecentActivitiesForRoot:
                unExcessActivitiesForRoot = len( unosRecentActivitiesForRoot) - unMaxRecentActivitiesForRoot
                if unExcessActivitiesForRoot > 0:
                    unosRecentActivitiesForRoot = unosRecentActivitiesForRoot[ unExcessActivitiesForRoot:]
                    TRACatalogo_Globales.gRecentActivities[ unPathDelRaiz] = unosRecentActivitiesForRoot
                    
            unosRecentActivitiesForRoot.append( aTranslationChange)
            
            
            
            
                        
            # ####################################################################
            """Increment the counter of changes since the last time the status report by languages was generated. 
            
            """
            
            if TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByLanguages == None:
                TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByLanguages = { }
                
            unNumTranslationsStatusChangesForRootSinceReportByLanguages = TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByLanguages.get( unPathDelRaiz, None)
            if unNumTranslationsStatusChangesForRootSinceReportByLanguages == None:
                unNumTranslationsStatusChangesForRootSinceReportByLanguages = 0
                
            unNumTranslationsStatusChangesForRootSinceReportByLanguages += 1
            TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByLanguages[ unPathDelRaiz] = unNumTranslationsStatusChangesForRootSinceReportByLanguages
                  
            
            
            
            # ####################################################################
            """Increment the counter of changes since the last time the status report by  modules and languages were generated. 
            
            """
            
            if TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByModulesAndLanguages == None:
                TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByModulesAndLanguages = { }
                
            unNumTranslationsStatusChangesForRootSinceReportByModulesAndLanguages = TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByModulesAndLanguages.get( unPathDelRaiz, None)
            if unNumTranslationsStatusChangesForRootSinceReportByModulesAndLanguages == None:
                unNumTranslationsStatusChangesForRootSinceReportByModulesAndLanguages = 0
                
            unNumTranslationsStatusChangesForRootSinceReportByModulesAndLanguages += 1
            TRACatalogo_Globales.gNumTranslationsStatusChangesSinceReportByModulesAndLanguages[ unPathDelRaiz] = unNumTranslationsStatusChangesForRootSinceReportByModulesAndLanguages
            
            
            
             # ####################################################################
            """Increment the counter of changes since the last time the activity report were generated. 
            
            """
           
            if TRACatalogo_Globales.gNumActivitiesSinceActivityReport == None:
                TRACatalogo_Globales.gNumActivitiesSinceActivityReport = { }
                
            unNumActivitiesForRootSinceActivityReport = TRACatalogo_Globales.gNumActivitiesSinceActivityReport.get( unPathDelRaiz, None)
            if unNumActivitiesForRootSinceActivityReport == None:
                unNumActivitiesForRootSinceActivityReport = 0
                
            unNumActivitiesForRootSinceActivityReport += 1
            TRACatalogo_Globales.gNumActivitiesSinceActivityReport[ unPathDelRaiz] = unNumActivitiesForRootSinceActivityReport
                 
            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseGlobalsLock( )
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        return self
            
    
    
        

    
                        