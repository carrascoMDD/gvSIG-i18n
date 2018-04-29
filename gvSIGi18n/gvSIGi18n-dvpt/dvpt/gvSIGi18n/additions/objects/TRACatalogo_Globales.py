# -*- coding: utf-8 -*-
#
# File: TRACatalogo_Globales.py
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

from time                       import time

import logging

import threading


from AccessControl                  import ClassSecurityInfo

from Products.CMFCore               import permissions




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








class TRACatalogo_Globales:
    """
    """
    security = ClassSecurityInfo()

    
    # #######################################################
    """Globals that are not changed during execution of this Zope/Plone instance.
    
    """    

    """Used to XOR millisecond values to produce and test 'magic' HTTP request parameters to avoid triggering actions on requests confirmed long after the confirmation was prompted by the system.
    
    """    
    gTRAMagicLongMask = ~int( time() * 1000)

    
    
    
    
    
    
    # #######################################################
    """Globals shared among multiple execution threads.
    
    """    
    
    
    
    # #######################################################
    """To enforce Exclusive access to globals
    
    """
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    gTRACatalogoGlobalesMutex = threading.Lock()
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 
        
    
    
    # #######################################################
    """Global holding the dictionary of ProgressHandlers for all active long-lived processes, indexed by the progress control handler key (a unique string composed by the translations catalog root path, and  and the id of the progress element).
    
    """    
    gTRAProgressHandlers = { }
    
    
    
    
    
    # #######################################################
    """Global to control execution profiling and logging, for all root translations catalog, and for each root translations catalog. 
    Maintained through templates to change the enablemente state.
    Not maintained through thread-safe critical sections (this is not so critical)
    
    """
    
    
    gTRAExecutionProfilingIgnored     = cTRAExecutionProfilingIgnored

    
    
    gTRAExecutionProfilingEnablementConfigurationGlobal = None
    
    gTRAExecutionProfilingEnablementConfigurations      = { }
    

    
    




    # #######################################################
    """For each TRACatalogo root path, holds the milliseconds of the last time the Status Report by Languages, or by Modules and languages, was generated.
    
    """
    gStatusReportByLanguagesTimeMillis           = { }
    gStatusReportByModulesAndLanguagesTimeMillis = { }
    

    # #######################################################
    """For each TRACatalogo root path, holds the number of Translation status changes since the last time the Status Report by Languages, or by Modules and languages, was generated.
    
    """
    gNumTranslationsStatusChangesSinceReportByLanguages             = { }
    gNumTranslationsStatusChangesSinceReportByModulesAndLanguages   = { }

    
    
    
    
    
    # #######################################################
    """For each TRACatalogo root path, holds the milliseconds of the last time the Activity Report was generated.
    
    """    
    gActivityReportTimeMillis           = { }

    
    # #######################################################
    """For each TRACatalogo root path, holds the number activities since the last time the Activity Report was generated.
    
    """
    gNumActivitiesSinceActivityReport             = { }

        
    
        
    
    # #######################################################
    """For each TRACatalogo root path, holds information about the recent Translation status changes: time, language, user, symbol, change kind, new status.
    
    """
    gRecentActivities             = { }

    
    
          
    
    
    
    
    
    
    
    
    # #######################################################
    # #######################################################

   
    
 

 
   
    security.declarePrivate( 'pAcquireGlobalsLock')
    def pAcquireGlobalsLock(self,):
        """Reserve access to Globals and Globals control, by acquiring and releasing a lock on a mutual exclussion (mutex) semaphore, held here to protect critical sections and make them thread-safe.
        
        """
        
        # #################
        """MUTEX LOCK. 
        
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        TRACatalogo_Globales.gTRACatalogoGlobalesMutex.acquire()
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return self
    


    
    
    

    
    security.declarePrivate( 'pReleaseGlobalsLock')
    def pReleaseGlobalsLock(self, ):
        """Release access to Globals and Globals control, by acquiring and releasing a lock on a mutual exclussion (mutex) semaphore, held here to protect critical sections and make them thread-safe.
        
        """


        # #################
        """MUTEX UNLOCK. 
        
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        TRACatalogo_Globales.gTRACatalogoGlobalesMutex.release()
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return self
    

   


                        