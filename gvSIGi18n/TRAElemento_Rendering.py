# -*- coding: utf-8 -*-
#
# File: TRAElemento_Rendering.py
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




from StringIO                   import StringIO


try:
    import simplejson as json
except:
    json=None
    

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


      
    
            
# ########################################################################################################
    
class TRAElemento_Rendering:
    """Class with responsibility dealing with rendering of elements as plain text or html.
        
    """
    
    security = ClassSecurityInfo()

 


 
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
 
   
    
    
    
               
                     
         
    
 
    security.declarePublic( 'fJSONdumps')
    def fJSONdumps(self, theObject):
        if not json:
            return ""
        
        aJSON=json.dumps(theObject)
        return aJSON
    

    
         
    
 
    security.declarePublic( 'fJSONloads')
    def fJSONloads(self, theString):
        if not json:
            return None
        anObject=json.loads(theString)
        return anObject
    

        
    
    
    

