# -*- coding: utf-8 -*-
#
# File: TRACatalogo_Autorizaciones.py
#
# Copyright (c) 2009 by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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

__author__ = """Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
<gvSIGi18n@gvSIG.org>, Model Driven Development sl
<gvSIGi18n@ModelDD.org>, Antonio Carrasco Valero
<carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.gvSIGi18n.config import *

##code-section module-header #fill in your manual code here

from  TRAElemento_Permission_Definitions import cUseCase_ReviewUsersAuthorizations
from  TRAElemento_Permission_Definitions import cTRAUserGroups_AllIdiomas, cTRAUserGroups_Idioma



##/code-section module-header

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema



##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TRACatalogo_Autorizaciones:
    """
    """
    security = ClassSecurityInfo()
    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
# end of class TRACatalogo_Autorizaciones

##code-section module-footer #fill in your manual code here

    
    security.declarePrivate( 'fNewVoidInformeAutorizacionesUsuarioEnIdioma')
    def fNewVoidInformeAutorizacionesUsuarioEnIdioma(self,):
        unInforme = {
            'user_id':              '', 
            'user_name':            '', 
            'authorized_roles':     [ ],
         }
        return unInforme
    
 
    security.declarePrivate( 'fNewVoidInformeAutorizacionesIdioma')
    def fNewVoidInformeAutorizacionesIdioma(self,):
        unInforme = {
            'codigo_idioma_en_gvsig':           '', 
            'codigo_internacional_de_idioma':   '',
            'nombre':                           '',
            'nombre_nativo':                    '',
            'flag':                             '',
            'users_authorizations':             [],
        }
        return unInforme
    
     
    
   

    security.declarePrivate( 'fNewVoidInformeAutorizacionesIdiomas')
    def fNewVoidInformeAutorizacionesIdiomas(self,):
        unInforme = {
            'success':                                  False,
            'users_authorizations_all_idiomas':         None, 
            'idiomas':                                  [], 
            'display_country_flags':                    False,
        }
        return unInforme
       

    
    
    security.declarePrivate( 'fInformeAuthorizacionesIdiomas')
    def fInformeAuthorizacionesIdiomas(self, 
        thePermissionsCache=None, 
        theRolesCache=None, 
        theParentExecutionRecord=None): 
        """Report all languages and all the users authorized to play each role in each language.
        
        """
        
        unExecutionRecord = self.fStartExecution( 'method',  'fInformeAuthorizacionesIdiomas', theParentExecutionRecord, False) 

        try:       
            
            unPermissionsCache = (( thePermissionsCache == None) and { }) or thePermissionsCache
            unRolesCache       = (( theRolesCache == None) and { }) or theRolesCache
            
            
            unInforme = self.fNewVoidInformeAutorizacionesIdiomas()
            
            # ##############################################################################
            """Query for all languages .
            
            """
            unUseCaseQueryResult = self.fUseCaseAssessment(  
                theUseCaseName          = cUseCase_ReviewUsersAuthorizations, 
                theElementsBindings     = { cBoundObject: self,},
                theRulesToCollect       = [ 'languages',], 
                thePermissionsCache     = unPermissionsCache, 
                theRolesCache           = unRolesCache, 
                theParentExecutionRecord= unExecutionRecord) 
            if not unUseCaseQueryResult or not unUseCaseQueryResult.get( 'success', False):
                return unInforme  
             
            unInforme[ 'display_country_flags'] = self.fDisplayCountryFlags()
            
            unosLanguagesNamesAndFlagsPorCodigo = self.fLanguagesNamesAndFlagsPorCodigo()
            
            unosInformesIdiomas = [ ]
            
            unosIdiomasAccesibles = unUseCaseQueryResult.get( 'collected_rule_assessments_by_name', {}).get( 'languages', {}).get( 'accepted_final_objects', [])
            for unIdioma in unosIdiomasAccesibles: 

                unCodigoIdioma = unIdioma.getCodigoIdiomaEnGvSIG()
                
                unInformeIdioma = self.fNewVoidInformeAutorizacionesIdioma()
                unInformeIdioma.update( {
                    'codigoIdiomaEnGvSIG':           self.fAsUnicode( unCodigoIdioma), 
                    'codigoInternacionalDeIdioma':   self.fAsUnicode( unIdioma.getCodigoInternacionalDeIdioma() or ''),
                    'nombreIdioma':                  self.fAsUnicode( unIdioma.Title() or ''),
                    'nombreNativoDeIdioma':          self.fAsUnicode( unIdioma.getNombreNativoDeIdioma() or ''),
                    'flag':                          self.fAsUnicode( unosLanguagesNamesAndFlagsPorCodigo.get( unCodigoIdioma, {}).get( 'flag', cTRAFlagIdiomaDesconocida)),
                    'displayTitle':                  self.fAsUnicode( unIdioma.fDisplayTitleAsUnicode())
                })
                
                unosInformesUsuariosIdiomaByUserId = { }
                
                for unGroupSpec in cTRAUserGroups_Idioma:
                    
                    unGroupName     = unGroupSpec[ 0]
                    unGroupRoles    = unGroupSpec[ 1]
                    
                    unGroupId = self.fUserGroupIdIdiomaFor( unGroupName, theIdioma)
                    unosUsuariosEnGrupo = self.fUsersInGroupId( unGroupId)
                    
                    for unUserIdAndName in unosUsuariosEnGrupo:
                        unUserId   = unUserIdAndName[ 0]
                        unUserName = unUserIdAndName[ 1]
                        unInformeAutorizacionesUsuarioEnIdioma = unosInformesUsuariosIdiomaByUserId.get( unUserId, None)
                        if not unInformeAutorizacionesUsuarioEnIdioma:
                            unInformeAutorizacionesUsuarioEnIdioma = self.fNewVoidInformeAutorizacionesUsuarioEnIdioma()
                            unInformeAutorizacionesUsuarioEnIdioma[ 'user_id']   = unUserId
                            unInformeAutorizacionesUsuarioEnIdioma[ 'user_name'] = unUserName
                            unosInformesUsuariosIdiomaByUserId[ unUserId] = unInformeAutorizacionesUsuarioEnIdioma
                            
                        unosRolesUsuarioEnIdioma = unInformeAutorizacionesUsuarioEnIdioma.get( 'authorized_roles', [])
                        
                        for unRole in unGroupRoles:
                            if not ( unRole in unosRolesUsuarioEnIdioma):    
                                unosRolesUsuarioEnIdioma.append( unRole)
                                
                unInformeIdioma[ 'users_authorizations'] = unosInformesUsuariosIdiomaByUserId.values()
                unosInformesIdiomas.append( unInformeIdioma)
                
            unosInformesIdiomasSorted = sorted( unosInformesIdiomas, lambda uno, otro: cmp( uno[ 'codigoIdiomaEnGvSIG'], otro[ 'codigoIdiomaEnGvSIG']))
            
            unInforme[ 'idiomas'] = unosInformesIdiomasSorted
            
            
            
            unosInformesUsuariosAllIdiomasByUserId = { }

            for unGroupSpec in cTRAUserGroups_AllIdiomas:
                
                unGroupName     = unGroupSpec[ 0]
                unGroupRoles    = unGroupSpec[ 1]
                
                unGroupId = self.fUserGroupIdAllIdiomasFor( unGroupName)
                unosUsuariosEnGrupo = self.fUsersInGroupId( unGroupId)
                
                for unUserIdAndName in unosUsuariosEnGrupo:
                    unUserId   = unUserIdAndName[ 0]
                    unUserName = unUserIdAndName[ 1]
                    unInformeAutorizacionesUsuarioEnIdioma = unosInformesUsuariosAllIdiomasByUserId.get( unUserId, None)
                    if not unInformeAutorizacionesUsuarioAllIdiomas:
                        unInformeAutorizacionesUsuarioAllIdiomas = self.fNewVoidInformeAutorizacionesUsuarioEnIdioma()
                        unInformeAutorizacionesUsuarioAllIdiomas[ 'user_id']   = unUserId
                        unInformeAutorizacionesUsuarioAllIdiomas[ 'user_name'] = unUserName
                        unosInformesUsuariosAllIdiomasByUserId[ unUserId] = unInformeAutorizacionesUsuarioAllIdiomas
                        
                    unosRolesUsuarioAllIdiomas = unInformeAutorizacionesUsuarioEnIdioma.get( 'authorized_roles', [])
                    
                    for unRole in unGroupRoles:
                        if not ( unRole in unosRolesUsuarioAllIdiomas):    
                            unosRolesUsuarioAllIdiomas.append( unRole)
                            
            unInforme[ 'users_authorizations_all_idiomas'] = unosInformesUsuariosAllIdiomasByUserId.values()
            
               
            
        finally:
            unExecutionRecord and unExecutionRecord.pEndExecution()
                      
                
                  
        
##/code-section module-footer



