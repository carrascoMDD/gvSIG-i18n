# -*- coding: utf-8 -*-
#
# File: TRAParametrosControlProgreso_Operaciones.py
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

    
    
    
    
    
    security.declarePrivate( 'pInitDefaultProcessControlParms')    
    def pInitDefaultProcessControlParms( self, theProcessType, theProgressControlParms, theElement):
        if not theProcessType:
            return self
        if theProgressControlParms == None:
            return self
        
        someProgressSupportKinds = self.fProgressSupportKindsForProcessTypeOnTarget( theProcessType, theElement)
        
        aProgressControlParms_Logging        = theProgressControlParms.get( cTRAProgress_SupportKind_Logging, {})
        aProgressControlParms_Logging[ 'enabled']                    = ( cTRAProgress_SupportKind_Logging in someProgressSupportKinds) and ( self.getRegistro_habilitado() or True)
        aProgressControlParms_Logging[ 'max_milliseconds']           = self.getRegistro_maximoMilisegundos() or 120000
        aProgressControlParms_Logging[ 'max_elements_traversed']     = self.getRegistro_maximoElementosLeidos() or 10000
        aProgressControlParms_Logging[ 'max_elements_changed']       = self.getRegistro_maximoElementosModificados() or 1000
        aProgressControlParms_Logging[ 'log_every_nth_transactions'] = self.getRegistro_maximoTransacciones() or 10
        

        aProgressControlParms_StoreResults   = theProgressControlParms.get( cTRAProgress_SupportKind_StoreResults, {})
        aProgressControlParms_StoreResults[ 'enabled']                    = ( cTRAProgress_SupportKind_StoreResults in someProgressSupportKinds) and ( self.getGuardarResultados_habilitado() or True)
        aProgressControlParms_StoreResults[ 'max_milliseconds']           = self.getGuardarResultados_maximoMilisegundos() or 60000
        aProgressControlParms_StoreResults[ 'max_elements_traversed']     = self.getGuardarResultados_maximoElementosLeidos() or 5000
        aProgressControlParms_StoreResults[ 'max_elements_changed']       = self.getGuardarResultados_maximoElementosModificados() or 500
 
        
        aProgressControlParms_YieldProcessor = theProgressControlParms.get( cTRAProgress_SupportKind_YieldProcessor, {})
        aProgressControlParms_YieldProcessor[ 'enabled']                    = ( cTRAProgress_SupportKind_YieldProcessor in someProgressSupportKinds) and ( self.getCederProcesador_habilitado() or True)
        aProgressControlParms_YieldProcessor[ 'max_milliseconds']           = self.getCederProcesador_maximoMilisegundos() or 500
        aProgressControlParms_YieldProcessor[ 'max_elements_traversed']     = self.getCederProcesador_maximoElementosLeidos() or 100
        aProgressControlParms_YieldProcessor[ 'max_elements_changed']       = self.getCederProcesador_maximoElementosModificados() or 50
        aProgressControlParms_YieldProcessor[ 'percent_active_time']        = self.getCederProcesador_porcentajeTiempoActividad() or 50
        
        
        aProgressControlParms_Transactional  = theProgressControlParms.get( cTRAProgress_SupportKind_Transactional, {})
        aProgressControlParms_Transactional[ 'enabled']                    = ( cTRAProgress_SupportKind_Transactional in someProgressSupportKinds) and ( self.getTransacciones_habilitado() or True)
        aProgressControlParms_Transactional[ 'max_milliseconds']           = self.getTransacciones_maximoMilisegundos() or 1000
        aProgressControlParms_Transactional[ 'max_elements_traversed']     = self.getTransacciones_maximoElementosLeidos() or 1000
        aProgressControlParms_Transactional[ 'max_elements_changed']       = self.getTransacciones_maximoElementosModificados() or 100
        
        return self
            
    
    
    
        
       