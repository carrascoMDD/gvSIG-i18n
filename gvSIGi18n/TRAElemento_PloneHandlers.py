# -*- coding: utf-8 -*-
#
# File: TRAElemento_PloneHandlers.py
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


import logging

from logging import ERROR as cLoggingLevel_ERROR

from AccessControl              import ClassSecurityInfo


from Products.Archetypes.utils  import shasattr

from Products.CMFCore           import permissions

from Products.CMFCore.utils     import getToolByName


from Products.Archetypes.atapi  import OrderedBaseFolder, BaseBTreeFolder



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


            
    
            
# ########################################################################################################
    
class TRAElemento_PloneHandlers:
    """Class with responsibility to handle certain Plone actions.
        
    """
    
    security = ClassSecurityInfo()

    
        
    
    security.declarePrivate('pHandle_manage_afterAdd')
    def pHandle_manage_afterAdd(self, theItem, theContainer):   
        
        if self.__class__.__name__ == 'TRACadena':
            pass
        
        elif self.__class__.__name__ == 'TRATraduccion':
            pass
        
        elif self.__class__.__name__ == 'TRAColeccionCadenas':
            BaseBTreeFolder.manage_afterAdd(  self, theItem, theContainer)
        
        else:
            OrderedBaseFolder.manage_afterAdd(  self, theItem, theContainer)
        
        self.pSetPermissions()
                
        return self
    
         
        
    



    security.declareProtected(permissions.ModifyPortalContent, 'pHandle_moveObjectsByDelta')
    def pHandle_moveObjectsByDelta(self, ids, delta, subset_ids=None): 
        """Intercept modification method for re-ordering an OrderedBaseFolder specialization
        used in to provide drag&drop functionality directly from Plone.
        does not hit the ModelDDvlPlone framework presentation layer
        and therefore the incalidation of cache entries must be triggered by intercepting the method.
        
        """

        unResult = None
        
        if self.__class__.__name__ == 'TRAColeccionCadenas':
            
            unResult = BaseBTreeFolder.moveObjectsByDelta(   self,  ids, delta, subset_ids=subset_ids)
        
        else:
            unResult = OrderedBaseFolder.moveObjectsByDelta( self,  ids, delta, subset_ids=subset_ids)
        
        
        if not unResult:
            return self
        
        
        unaModelDDvlPloneTool = self.fModelDDvlPloneTool()
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
        someObjectValues = self.fObjectValues()
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
            
        
    
        
    
    
      
    
    security.declarePrivate('pHandle_manage_beforeDelete')
    def pHandle_manage_beforeDelete(self, theItem, theContainer):   
        """Destroy before deletion.
        Disable ZCatalog logging while deleting contents to avoid flooding the log with catalog messages complaining about keys not found. 
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
        
    
    
    
        
        
    security.declarePrivate( 'pHandle_manage_pasteObjects')        
    def pHandle_manage_pasteObjects(self, cb_copy_data=None, REQUEST=None):
        """Trap and override behavior of manage_pasteObjects implementation in CopySupport.py 
        
        """
        return None
    
        
        
       
        
    