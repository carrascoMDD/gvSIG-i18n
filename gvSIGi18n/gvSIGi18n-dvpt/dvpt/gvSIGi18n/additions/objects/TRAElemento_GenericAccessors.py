# -*- coding: utf-8 -*-
#
# File: TRAElemento_GenericAccessors.py
#
# Copyright (c) 2008, 2009,2010 by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
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



from Products.CMFCore           import permissions

from Products.CMFCore.utils     import getToolByName





from TRAElemento_Constants              import *
 
            
            
            
    
            
# ########################################################################################################
    
class TRAElemento_GenericAccessors:
    """Class with responsibility dealing with generic accessors to attributes by attribute name.
        
    """
    
    security = ClassSecurityInfo()

    

    security.declarePublic('getAttributeValueByName')
    def getAttributeValueByName( self, theName):
        """Generic attribute accesor by name.
        
        """
        if self.schema.has_key( theName):
            return self.schema[theName].getRaw(self) # , encoding="utf-8")
        else:
            if theName == 'title':
                return self.Title()
            elif theName == 'text':
                return self.getText()
            elif theName == 'description':
                return self.Description()
            elif theName == 'titleAndOwnerTitle':
                unPropietario = self.getPropietario()
                if unPropietario == self:
                    return self.Title()
                else:
                    return "%s [%s]" % (self.Title(), unPropietario.Title())
            else:
                return self.__getattribute__(theName)
        




    security.declarePublic('getMetaValue')
    def getMetaValue( self , elNombreAttribute):
        """Class metainfo accesor methods .
        
        """
        
        if not elNombreAttribute:
            return None

        someStringMetaAttributes = [ 'archetype_name', 'meta_type',  'portal_type',  'content_icon',  'typeDescription',  'typeDescMsgId',  'immediate_view',  'default_view', ]
        someStringArrayMetaAttributes = [ 'allowed_content_types', 'suppl_views', ]
        
        if not( elNombreAttribute in someStringMetaAttributes + someStringArrayMetaAttributes):
            return None
            
        unValue = self.__getattribute__( elNombreAttribute)
        unResult = [ elNombreAttribute, unValue, elNombreAttribute, elNombreAttribute, elNombreAttribute, elNombreAttribute, 'string' ]
        
        if elNombreAttribute in someStringArrayMetaAttributes:
            unResult[ 6] = 'string[]'
        
        return unResult
            






    security.declarePublic('getAttributeMetaAndValue')    ###
    def getAttributeMetaAndValue(self , elNombreAttribute): ###
        """Attribute accesor methods for combined info and metainfo.
        
        """
        if not elNombreAttribute:
            return None
            

        unSchema = self.schema
        if not unSchema.has_key( elNombreAttribute):
            return None
            
        unField             = unSchema[ elNombreAttribute]
        unWidget            = unField.widget
        unType              = unField.type
        unaLabel            = elNombreAttribute
        unaDescription      = elNombreAttribute
        unaLabelMsgId       = elNombreAttribute
        unaDescriptionMsgId = elNombreAttribute
        
        try:
            unaLabel            = unWidget.label            
        except:
            None
            
        try:
            unaDescription  = unWidget.description
        except:
            None
            
        try:
            unaLabelMsgId       = unWidget.label_msgid
        except:
            None
            
        try:
            unaDescriptionMsgId = unWidget.description_msgid
        except:
            None
        
        unVocabulary        = []
        unVocabularyMsgIds  = []
        
        if self.schema[ elNombreAttribute].widget.getType() == 'Products.Archetypes.Widget.SelectionWidget':
            if self.schema[ elNombreAttribute].__dict__.has_key('vocabulary'):
                unVocabulary = self.schema[ elNombreAttribute].vocabulary
                if unVocabulary:
                    unType = 'selection'
                    
                    unVocabularyMsgIds = unVocabulary[:]
                    try:
                        unVocabularyMsgIds = self.schema[ elNombreAttribute].vocabulary_msgids
                    except:
                        None
        
        unValue     = self.getAttributeValueByName( elNombreAttribute)    
        
        unResult = [ elNombreAttribute, unValue, unaLabel, unaLabelMsgId, unaDescription, unaDescriptionMsgId, unType, unVocabulary, unVocabularyMsgIds ]
        
        return unResult        





 


    security.declareProtected( permissions.ModifyPortalContent, 'setAttributesValues')
    def setAttributesValues(self , losNombresYValoresAttributes=""):
        """Generic attribute mutators by name.
        
        """
        
        if not losNombresYValoresAttributes:
            return []

        someResults = []
        for unNombreYValorAttribute in losNombresYValoresAttributes:
            if unNombreYValorAttribute and len( unNombreYValorAttribute) > 1:
                unNombreAttribute = unNombreYValorAttribute[ 0]
                unNuevoValorAttribute  = unNombreYValorAttribute[ 1]
            
                unAttributeMetaAndValue = self.getAttributeMetaAndValue( unNombreAttribute)
                if unAttributeMetaAndValue:
                    unValorAttribute = unAttributeMetaAndValue[ 1]
                    if not ( unNuevoValorAttribute == unValorAttribute):
                        self.setAttributeValueByName( unNombreAttribute, unNuevoValorAttribute)  
                        someResults.append( [ unNombreAttribute, unNuevoValorAttribute,  unAttributeMetaAndValue] )                                      
        return someResults        




    security.declareProtected( permissions.ModifyPortalContent, 'setAttributeValueByName')
    def setAttributeValueByName( self, theName, theValue):
        if self.schema.has_key( theName):
            unField  = self.schema[theName]
            unMutator = unField.getMutator( self)
            unMutator( theValue) 
        else:
            if theName == 'title':
                return self.setTitle( theValue)
            elif theName == 'text':
                return self.setText( theValue)
            elif theName == 'description':
                return self.setDescription( theValue)
            else:
                return self.__setattribute__(theName, theValue)
        







    security.declarePublic('getAttributesMetaAndValues')
    def getAttributesMetaAndValues(self , losNombresAttributes=""):
        if not losNombresAttributes:
            return []

        unResult = [ ]
        
        for unNombreAttribute in losNombresAttributes:
            unAttributeMetaAndValue = self.getAttributeMetaAndValue( unNombreAttribute)
            if unAttributeMetaAndValue:
                unResult.append( unAttributeMetaAndValue)
            
        return unResult        









    security.declarePublic('getReferenceMeta')
    def getReferenceMeta(self , elNombreReference=""):
        """Relation metainfo accesor methods .
        
        """
        
        if not elNombreReference:
            return []

        unSchema = self.schema
        if not unSchema.has_key( elNombreReference):
            return []
            
        unField             = unSchema[ elNombreReference]
        unWidget            = unField.widget
        unaLabel            = unWidget.label
        unaDescription      = unWidget.description
        unaDescriptionMsgId = unWidget.description_msgid
        unaLabelMsgId       = unWidget.label_msgid
        unEsMultiValued     = unField.multiValued
        
        unResult = [ elNombreReference, None , unaLabel, unaLabelMsgId, unaDescription, unaDescriptionMsgId, unEsMultiValued, unField, unWidget, ]
        
        return unResult        
        
    








 
    security.declarePublic('getReferenceMetaAndValue')
    def getReferenceMetaAndValue(self , elNombreReference=""):
        """Relation accesor methods for combined info and metainfo .
        
        """
        
        if not elNombreReference:
            return []
            
        unReferenceMeta = self.getReferenceMeta( elNombreReference)
        if not unReferenceMeta:
            return []
            
        unField             = unReferenceMeta[ 7]
        unEsMultiValued     = unReferenceMeta[ 6]
        
        unAccessor  = unField.getAccessor( self)
        unValue     = unAccessor()    
        
        unResult = [] + unReferenceMeta
        
        if unEsMultiValued:
            unResult[ 1] =  unValue
        else:
            unResult[ 1] =  [ unValue]
        
        return unResult        
        
    


    security.declarePublic('getReferencesMetaAndValues')
    def getReferencesMetaAndValues(self , losNombresReferences=[]):
        if not losNombresReferences:
            return []

        unResult = [ ]
        
        for unNombreReference in losNombresReferences:
            unReferenceMetaAndValue = self.getReferenceMetaAndValue( unNombreReference)
            if unReferenceMetaAndValue:
                unResult.append( unReferenceMetaAndValue)
            
        return unResult        




          




            
            
    security.declarePrivate('fTFL')
    def fTFL(self, theFieldName):
        """fTFL stands for function for Translated Field Label
        will be used in the context of expressions of computed archetype schema fields
        the short name is to use less space
        in the tagged value edition fields
        of case tools            
   
        """
        
        if not theFieldName:
            return ''
            
        aSchema = self.schema
        if not aSchema.has_key( theFieldName):
            return theFieldName
       
        aField = aSchema.get( theFieldName)
        if not aField:
            return theFieldName
            
        aWidget = aField.widget
        if not aWidget:
            return theFieldName
        
        aMsgId = aWidget.label_msgid
        if not aMsgId:
            return theFieldName
        
        anI18NDomain = self.getNombreProyecto()   
        if not anI18NDomain:
            return theFieldName

        aTranslationService = None
        try:
            aTranslationService = self.getTranslationServiceTool()
        except:
            None
        if not aTranslationService:
            return theFieldName
            
        aTranslation = aTranslationService.utranslate( anI18NDomain, aMsgId, mapping=None, context=self , target_language= None, default=theFieldName)                       
        if not aTranslation:
            return theFieldName

        return aTranslation
    
 
 
    security.declarePrivate('fTFLVs')
    def fTFLVs(self, theFieldNames):
        """fTFLVs stands for function for multiple  Translated Field Label and Value
        will be used in the context of expressions of computed archetype schema fields
        the short name is to use less space
        in the tagged value edition fields
        of case tools.
        
        """
   
        if not theFieldNames:
            return ''
        
        someFieldLabelsAndValues = []
        for unFieldName in theFieldNames:
            unFieldLabelAndValue = self.fTFLV( unFieldName)
            if unFieldLabelAndValue:
                someFieldLabelsAndValues.append( unFieldLabelAndValue)

        if not someFieldLabelsAndValues:
            return ''
            
        unResultString = '; '.join( someFieldLabelsAndValues)

        return unResultString
            

 
    security.declarePrivate('fTFLVs')
    def fTFLVsUnless(self, theFieldNamesAndExcludeValues):
        """fTFLVsUnless stands for function for multiple  Translated Field Label and Value
        will be used in the context of expressions of computed archetype schema fields
        the short name is to use less space
        in the tagged value edition fields
        of case tools   
        
        """
        
        if not theFieldNames:
            return ''
        
        someFieldLabelsAndValues = []
        for unFieldName, unExcludeValue in theFieldNamesAndExcludeValues:
            unFieldLabelAndValue = self.fTFLVUnless( unFieldName, unExcludeValue)
            if unFieldLabelAndValue:
                someFieldLabelsAndValues.append( unFieldLabelAndValue)

        if not someFieldLabelsAndValues:
            return ''
            
        unResultString = '; '.join( someFieldLabelsAndValues)

        return unResultString
            

    
    
    security.declarePrivate('fTFLV')
    def fTFLV(self, theFieldName):
        """fTFLV stands for function for Translated Field Label and Value
        will be used in the context of expressions of computed archetype schema fields
        the short name is to use less space
        in the tagged value edition fields
        of case tools    
        
        """
        
        if not theFieldName:
            return ''

        aTranslatedLabel = self.fTFL( theFieldName)
        if not aTranslatedLabel:
            aTranslatedLabel = ''         
    
        unValueString = self.fFV( theFieldName)
        if not unValueString:
            return ''
            
        return aTranslatedLabel + ' ' + unValueString
             

    

    
    security.declarePrivate('fTFLV')
    def fTFLVUnless(self, theFieldName, theExcludeValueString):
        """fTFLVUnless stands for function for Translated Field Label and Value
        will be used in the context of expressions of computed archetype schema fields
        the short name is to use less space
        in the tagged value edition fields
        of case tools    
        
        """

        if not theFieldName:
            return ''

        unValueString = self.fFV( theFieldName)
        if not unValueString:
            return ''
        
        if unValueString == theExcludeValueString:
            return ''
            
        aTranslatedLabel = self.fTFL( theFieldName)
        if not aTranslatedLabel:
            aTranslatedLabel = ''         
    
        return aTranslatedLabel + ' ' + unValueString
             
    
    
    security.declarePrivate('fFV')
    def fFV(self, theFieldName):
        """fFV stands for function for  Field Value
        will be used in the context of expressions of computed archetype schema fields
        the short name is to use less space
        in the tagged value edition fields
        of case tools            
        
        """
        
        if not theFieldName:
            return ''

        unSchema = self.schema
        if not unSchema.has_key( theFieldName):
            return ''
            
        unField  = unSchema[ theFieldName]
        if not unField:
            return ''

        unAccessor = unField.getAccessor( self)
        if not unAccessor:
            return ''

        unValue = unAccessor()
        if ( unValue == None):
            return ''
            
        if unField.__class__.__name__ in ( 'RelationField', 'ReferenceField'):
            unIsMultiValued = unField.multiValued
            if not unIsMultiValued: 
                if not unValue:
                    return ''
                unTitle = unValue.Title()
                if not unTitle:
                    return ''
                return unTitle
            else:
                unosTitulos = []
                if unValue:
                    for unElement in unValue:
                        unTitle = unElement.Title()
                        if unTitle:
                            unosTitulos.append( unTitle)
                if not unosTitulos:
                    return ''
                unosTitulosString = ', '.join( unosTitulos)
                return unosTitulosString
                                             
        
                        
        unElementFieldType      = unField.type
        
        if unElementFieldType == 'computed':
            unElementFieldType = 'string'
                    
        unValueString = ''
                            
        unWidget = unField.widget
        if unWidget and (unWidget.getType() == 'Products.Archetypes.Widget.SelectionWidget') and unField.__dict__.has_key('vocabulary'):    
            unValueString = unValue    
            someVocabularyOptions   = []
            try:
                someVocabularyOptions = unField.vocabulary   
            except:
                None
                
            someVocabularyMsgIds = []
            try:
                someVocabularyMsgIds = unField.vocabulary_msgids   
            except:
                None
                
            aTranslationService = None
            try:
                aTranslationService = self.getTranslationServiceTool()
            except:
                None

            anI18NDomain = self.getNombreProyecto()   
                
            if someVocabularyOptions and someVocabularyMsgIds and aTranslationService and anI18NDomain:
                if unValue in someVocabularyOptions:
                    unValueIndex = someVocabularyOptions.index( unValue)
                    if (unValueIndex >= 0) and ( unValueIndex < len( someVocabularyMsgIds)):
                        unValueMsgId = someVocabularyMsgIds[ unValueIndex]
                        aTranslation = aTranslationService.utranslate( anI18NDomain, unValueMsgId, mapping=None, context=self , target_language= None, default=unValueString)                       
                        if aTranslation:
                            unValueString = aTranslation                                               
                   
        elif unElementFieldType in[  'string', 'text']:            
            unValueString = unValue
            
        elif unElementFieldType == 'boolean':
            unValueString = str( unValue)
        
            aTranslationService = None
            try:
                aTranslationService = self.getTranslationServiceTool()
            except:
                None

            anI18NDomain = self.getNombreProyecto() 
              
            if aTranslationService and anI18NDomain:
                if unValue:
                    aTranslation = aTranslationService.utranslate( 'ModelDDvlPlone', 'ModelDDvlPlone_True', mapping=None, context=self , target_language= None, default=unValueString)                       
                    if aTranslation:
                        unValueString = aTranslation
                else:
                    aTranslation = aTranslationService.utranslate( 'ModelDDvlPlone', 'ModelDDvlPlone_False', mapping=None, context=self , target_language= None, default=unValueString)                       
                    if aTranslation:
                        unValueString = aTranslation
                        
        elif unElementFieldType == 'integer':
            unValueString  = str( unValue)
            
        elif unElementFieldType == 'float':
            unValueString  = str( unValue)

        elif unElementFieldType == 'fixedpoint':
            unValueString  = str( unValue)

        elif unElementFieldType == 'datetime':
            unValueString  = str( unValue)
        
        else:
            unValueString  = str( unValue)
    
        return unValueString
    
    