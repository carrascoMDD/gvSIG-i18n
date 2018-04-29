# -*- coding: utf-8 -*-
#
# File: TRAgvSIGi18nTool_Dates.py
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


from AccessControl import ClassSecurityInfo

from DateTime import DateTime


from Products.CMFCore                    import permissions


from TRAgvSIGi18nTool_Constants import *

   


# ##########################################################
"""Dates and Times Boundary methods (facade).

"""    


class TRAgvSIGi18nTool_Dates:
    """Dates services: Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations..
    
    """

    security = ClassSecurityInfo()
        
    
      
    security.declarePublic( 'fMagicMillisecondsNowString')
    def fMagicMillisecondsNowString(self, 
        theContextualElement    =None,):
        
        if theContextualElement == None:
            return ''
        
        return theContextualElement.fMagicMillisecondsNowString()
    
    
    
    
        
     
    security.declarePublic( 'fIsAcceptableMagicMilliseconds')
    def fIsAcceptableMagicMilliseconds(self, 
        theContextualElement    =None,
        theString               =None, 
        theAllowedSeconds       =None,):   
        
        if theContextualElement == None:
            return False
        
        return theContextualElement.fIsAcceptableMagicMilliseconds(
            theString               =theString, 
            theAllowedSeconds       =theAllowedSeconds,
        )
       
    
    
    

            
    security.declarePublic( 'fDateTimeFromMillisecondsTextual')
    def fDateTimeFromMillisecondsTextual(self, theMilliseconds):   
        return DateTime( float( theMilliseconds / 1000)).ISO()
      
    
        
    