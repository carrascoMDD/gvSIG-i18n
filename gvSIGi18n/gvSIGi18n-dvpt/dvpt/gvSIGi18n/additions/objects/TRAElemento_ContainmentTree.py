# -*- coding: utf-8 -*-
#
# File: TRAElemento_ContainmentTree.py
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




from AccessControl              import ClassSecurityInfo

from Acquisition                import aq_inner, aq_parent


from Products.CMFCore           import permissions

from Products.CMFCore.utils     import getToolByName





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
    
class TRAElemento_ContainmentTree:
    """Class with responsibility dealing with accesses to parent, root and children, recursively.
        
    """
    
    security = ClassSecurityInfo()

    

    
    
    security.declarePrivate( 'fObjectValues')    
    def fObjectValues( self, theTypeNames=None):
        
        someObjectValues = []
        
        if theTypeNames:
            someObjectValues = self.objectValues( theTypeNames)
        else:
            someObjectValues = self.objectValues( )
            
        return someObjectValues
    
           
    
    
    
    security.declarePrivate( 'fAllSubElements')    
    def fAllSubElements( self, theAdditionalParams=None):
        someSubElements = [ ]
        self.pAllSubElements_into( someSubElements, theAdditionalParams=None)
        return someSubElements
    
           
    
    
    
    security.declarePrivate( 'pForAllElementsDo')    
    def pForAllElementsDo( self, theLambda=None, thePloneLambda=None):
        if not ( theLambda or thePloneLambda):
            return self
        self.pForAllElementsDo_recursive( theLambda, thePloneLambda)
        
        return self
        
    

   
    
    security.declarePrivate( 'pForAllElementsPloneDo')    
    def pForAllElementsPloneDo( self, thePloneLambda=None,):
        if not thePloneLambda:
            return self
        
        unosElementosPlone = self.objectValues( cTRAPloneTypeNames)
        if not unosElementosPlone:
            return self
        
        for unElementoPlone in unosElementosPlone:
            self.pForAllElementsPloneDo_recursive( unElementoPlone, thePloneLambda)
            
        return self
        
        
    

    
    security.declarePrivate( 'pForAllElementsPloneDo_recursive')    
    def pForAllElementsPloneDo_recursive( self, thePloneElement=None, thePloneLambda=None,):
        
        if thePloneElement == None:
            return self
        
        if not thePloneLambda:
            return self
        
        thePloneLambda( thePloneElement)
        
        unMetaType = ''
        try:
            unMetaType = thePloneElement.meta_type
        except:
            None
        if not unMetaType:
            return self
        
        if not ( unMetaType == cTRAPloneTypeName_ATFolder):
            return self
        
        
        unosElementosPlone = None
        try:
            unosElementosPlone = thePloneElement.objectValues( cTRAPloneTypeNames)
        except:
            None
            
        if not unosElementosPlone:
            return self
        
        for unElementoPlone in unosElementosPlone:
            self.pForAllElementsPloneDo_recursive( unElementoPlone, thePloneLambda)
        
        return self
            
      
        
    security.declarePublic('fPortalRoot')
    def fPortalRoot(self):
        aPortalURLTool = self.getPortalURLTool()
        if not aPortalURLTool:
            return None
        
        unPortal = aPortalURLTool.getPortalObject()
        return unPortal       
    
    

        

    

    security.declarePublic('fPortalURL')
    def fPortalURL(self, ):
        
        unPortalURLTool = self.getPortalURLTool()
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
           
        
           
        
    
    security.declarePrivate( 'fElementoPorUID')
    def fElementoPorUID( self, theUID, theUIDCatalog=None):
        """Element access by UID.
        
        """
        if not theUID :
            return None
            
        unUIDCatalog = theUIDCatalog
        if unUIDCatalog == None:
            unUIDCatalog = self.getUIDCatalogTool()
            
        unaBusqueda = { 
            'UID' :            theUID, 
        }
        unosResultadosBusqueda = unUIDCatalog.searchResults( **unaBusqueda)
        if len( unosResultadosBusqueda) < 1:
            return None
            
        unElemento = unosResultadosBusqueda[ 0].getObject() 
        if ( unElemento == None):
            return None

        return unElemento    
    
    
        
    
    

    security.declarePublic( 'getElementoPorID')
    def getElementoPorID(self, theID):
        return self.getElementoPorID_scanning( theID)
    
    
    


    security.declarePrivate( 'getElementoPorID_byacquisition')
    def getElementoPorID_byacquisition(self, theID):
        """Basic accessor for contained element by id, by acquisition.
        
        """
        if not theID:
            return None

        anElement = None
        try:
            anElement = aq_get(self, theID,)
        except AttributeError:
            None
            
        return anElement
    
           

    
    
    
    
    security.declarePrivate( 'getElementoPorID_scanning')
    def getElementoPorID_scanning(self, theID):
        """Basic accessor for contained element by id, iterating over all contained elements.
        
        """
        if not theID:
            return None

        unosExistingElements = self.fObjectValues()
        
        for unElement in unosExistingElements:
            unId = unElement.getId()
            if unId == theID:
                return unElement
             
        return None    
        
     

 


    security.declarePublic('getRaiz')
    def getRaiz(self):
        
        if self.getEsRaiz():
            return self         
        
        unContenedor =  aq_parent( aq_inner( self))
        
        while not ( unContenedor == None):
            if unContenedor.getEsRaiz():
                return unContenedor
            else:
                unContenedor =  aq_parent( aq_inner( unContenedor))
                
        return self

    
    
   
 
    
    security.declarePublic( 'getCatalogo')
    def getCatalogo( self):
        unCatalogo = self.getRaiz()
        if not (unCatalogo.__class__.__name__ == cNombreTipoTRACatalogo):
            return None
        return unCatalogo
        


     


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

    
    

    
    
    
    


    security.declarePublic('fPathDelRaiz')
    def fPathDelRaiz(self):
        unRaiz = self.getRaiz()
        if not unRaiz:
            return ''
       
        unPathString = unRaiz.fPhysicalPathString( )
        return unPathString
        
    


    security.declarePublic('fPhysicalPathString')
    def fPhysicalPathString(self, ):
        unPhysicalPath = self.getPhysicalPath()
        if not unPhysicalPath:
            return ''
     
        unPathString = '/'.join( unPhysicalPath)
        return unPathString





    
    security.declarePublic('fDisplayPathString')
    def fDisplayPathString(self):
        return '/'.join( self.getPhysicalPath()[2:])
    



    
    
    
   






    
 
    
    
    
    security.declarePrivate('fAllElementUIDs')
    def fAllElementUIDs(self, theNombresTipos=None):
        
        someUIDs = None
        unExceptionInCatalog = False
        try:
            someUIDs = self.fAllElementUIDs_fromPortalCatalog( theNombresTipos)
        except:
            unExceptionInCatalog = True
        if not unExceptionInCatalog:
            return someUIDs
        
        someUIDs = self.fAllElementUIDs_fromVisitor( theNombresTipos)
       
        return someUIDs
        
      
            
    
    
    
    
    security.declarePrivate('fAllElementUIDs_fromPortalCatalog')
    def fAllElementUIDs_fromPortalCatalog(self, theNombresTipos=None):
        
        someUIDs = [ ]
        
        unPortalCatalog = self.getPortalCatalogTool()
        
        unPhysicalPath = self.fPhysicalPathString()

        unaBusqueda = { 
            'path' :    unPhysicalPath,
        }
        
        if theNombresTipos:
            unaBusqueda.update( {
                'meta_type' :    list( theNombresTipos),
            })
 
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
        
    
    
    
    
    
    security.declarePrivate('fAllElementUIDs_fromVisitor')
    def fAllElementUIDs_fromVisitor(self, theNombresTipos):
        
        
        someUIDs = [ ]
        
        self.pAllElementUIDs_fromVisitor_into( someUIDs, theNombresTipos)        
        
        return someUIDs
        
        
    
   
    security.declarePrivate('pAllElementUIDs_fromVisitor_into')
    def pAllElementUIDs_fromVisitor_into(self, theUIDs, theNombresTipos):
        
        if theUIDs == None:
            return self
        
        aMetaType = ''
        try:
            aMetaType = self.meta_type
        except:
            None
        if ( not aMetaType) or not ( aMetaType in theNombresTipos):
            return self
        
        anUID = self.UID()
        theUIDs.append( anUID)
        
        someElements = None
        if theNombresTipos:
            someElements = self.fObjectValues( theNombresTipos)
        else:
            someElements = self.fObjectValues( )
            
        for anElement in someElements:
            anElement.pAllElementUIDs_fromVisitor_into( theUIDs, theNombresTipos)
        
        return self
        
          
    