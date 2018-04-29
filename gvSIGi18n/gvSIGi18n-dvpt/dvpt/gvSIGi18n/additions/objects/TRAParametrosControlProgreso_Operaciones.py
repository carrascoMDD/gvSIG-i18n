# -*- coding: utf-8 -*-
#
# File: TRAParametrosControlProgreso_Operaciones.py
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




##code-section module-header #fill in your manual code here


import sys
import traceback
import logging
import transaction


from AccessControl          import ClassSecurityInfo

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



# ######################################
"""Allowed progess states.

"""
cTRAProgreso_EstadoProceso_Activo   = 'Activo'
cTRAProgreso_EstadoProceso_Inactivo = 'Inactivo'

cTRAProgreso_EstadoProcesos = [
    cTRAProgreso_EstadoProceso_Activo,
    cTRAProgreso_EstadoProceso_Inactivo,
]





class TRAParametrosControlProgreso_Operaciones:
    """Operations specifically defined on persistent elements that store the parametros to control the progress of a kind of long-lived process.
    
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

    
    
    
    
    
    security.declarePrivate( 'pInitDefaultProcessControlParms')    
    def pInitDefaultProcessControlParms( self, theProcessType, theProgressControlParms, theProgressSupportKinds):
        
        if not theProcessType:
            return self
        if theProgressControlParms == None:
            return self
        
        
        theProgressControlParms[ 'CreateReportBefore'] = self.getCrearInformeAntes()
        theProgressControlParms[ 'CreateReportAfter']  = self.getCrearInformeDespues()
        
        
        aProgressControlParms_StoreResults   = theProgressControlParms.get( cTRAProgress_SupportKind_StoreResults, None)
        if aProgressControlParms_StoreResults == None:
            aProgressControlParms_StoreResults = { }
            theProgressControlParms[ cTRAProgress_SupportKind_StoreResults] = aProgressControlParms_StoreResults

        aProgressControlParms_StoreResults[ 'enabled']                    = ( cTRAProgress_SupportKind_StoreResults in theProgressSupportKinds) and self.getGuardarResultados_habilitado()
        aProgressControlParms_StoreResults[ 'max_milliseconds']           = self.getGuardarResultados_maximoMilisegundos()
        aProgressControlParms_StoreResults[ 'max_elements_traversed']     = self.getGuardarResultados_maximoElementosLeidos()
        aProgressControlParms_StoreResults[ 'max_elements_changed']       = self.getGuardarResultados_maximoElementosModificados()
 
        
        
        aProgressControlParms_Transactional   = theProgressControlParms.get( cTRAProgress_SupportKind_Transactional, None)
        if aProgressControlParms_Transactional == None:
            aProgressControlParms_Transactional = { }
            theProgressControlParms[ cTRAProgress_SupportKind_Transactional] = aProgressControlParms_Transactional

        aProgressControlParms_Transactional[ 'enabled']                    = ( cTRAProgress_SupportKind_Transactional in theProgressSupportKinds) and self.getTransacciones_habilitado()
        aProgressControlParms_Transactional[ 'max_milliseconds']           = self.getTransacciones_maximoMilisegundos()
        aProgressControlParms_Transactional[ 'max_elements_traversed']     = self.getTransacciones_maximoElementosLeidos()
        aProgressControlParms_Transactional[ 'max_elements_changed']       = self.getTransacciones_maximoElementosModificados()
        
        
        
        aProgressControlParms_Logging        = theProgressControlParms.get( cTRAProgress_SupportKind_Logging, None)
        if aProgressControlParms_Logging == None:
            aProgressControlParms_Logging = { }
            theProgressControlParms[ cTRAProgress_SupportKind_Logging] = aProgressControlParms_Logging
            
        aProgressControlParms_Logging[ 'enabled']                    = ( cTRAProgress_SupportKind_Logging in theProgressSupportKinds) and self.getRegistro_habilitado()
        aProgressControlParms_Logging[ 'max_milliseconds']           = self.getRegistro_maximoMilisegundos()
        aProgressControlParms_Logging[ 'max_elements_traversed']     = self.getRegistro_maximoElementosLeidos()
        aProgressControlParms_Logging[ 'max_elements_changed']       = self.getRegistro_maximoElementosModificados()
        aProgressControlParms_Logging[ 'log_every_nth_transactions'] = self.getRegistro_maximoTransacciones()
        

        
        aProgressControlParms_YieldProcessor   = theProgressControlParms.get( cTRAProgress_SupportKind_YieldProcessor, None)
        if aProgressControlParms_YieldProcessor == None:
            aProgressControlParms_YieldProcessor = { }
            theProgressControlParms[ cTRAProgress_SupportKind_YieldProcessor] = aProgressControlParms_YieldProcessor

        aProgressControlParms_YieldProcessor[ 'enabled']                    = ( cTRAProgress_SupportKind_YieldProcessor in theProgressSupportKinds) and self.getCederProcesador_habilitado()
        aProgressControlParms_YieldProcessor[ 'max_milliseconds']           = self.getCederProcesador_maximoMilisegundos()
        aProgressControlParms_YieldProcessor[ 'max_elements_traversed']     = self.getCederProcesador_maximoElementosLeidos()
        aProgressControlParms_YieldProcessor[ 'max_elements_changed']       = self.getCederProcesador_maximoElementosModificados()
        aProgressControlParms_YieldProcessor[ 'percent_active_time']        = self.getCederProcesador_porcentajeTiempoActividad()
        
        return self
            
    
    
    
        
       