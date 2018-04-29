# -*- coding: utf-8 -*-
#
# File: TRAElemento_DatesAndTime.py
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



import time  


from DateTime                   import DateTime

from AccessControl              import ClassSecurityInfo

from Products.CMFCore           import permissions




from TRAElemento_Constants              import *


from TRACatalogo_Globales    import TRACatalogo_Globales


            
    
            
# ########################################################################################################
    
class TRAElemento_DatesAndTime:
    """Class with responsibility dealing with dates and times, and their representations.
        
    """
    
    security = ClassSecurityInfo()

    

    security.declarePublic( 'fFechaISOStringLastMonthDayInYear')
    def fFechaISOStringLastMonthDayInYear( self, theMonthNumber, theYearNumber):
        """Date rounding for searches.
        
        """
        
        if not theMonthNumber:
            return 0
        
        if theMonthNumber in [ 1, 3, 5, 7, 8, 10, 12,]:
            return 31
        
        if theMonthNumber in [ 4, 6, 9, 11, ]:
            return 30
       
        if theYearNumber % 4:
            return 29
        
        return 28
    
            
    
    
            
    security.declarePublic( 'fFechaISOStringDesdeStringParcial')
    def fFechaISOStringDesdeStringParcial( self, theISODatePartialString, theEarliest=True):
    
        if not theISODatePartialString:
            return ''
        
        unaFechaString = theISODatePartialString
            
        unosYearMonthDay = unaFechaString.split( cISOStringFechaYMDSeparator)
        if not unosYearMonthDay:
            return ''
        
        unYearString   = unosYearMonthDay[ 0]
        unMonthString = ''
        unDayString   = ''
        if len( unosYearMonthDay) > 1:
            unMonthString = unosYearMonthDay[ 1]
        if len( unosYearMonthDay) > 2:
            unDayString   = unosYearMonthDay[ 2]
            
            
            
        if not unYearString:
            return ''
        unYearInt = -1
        try:
            unYearInt = int( unYearString)
        except:
            None
        if not ( ( unYearInt >= cFirstYearForSearches) and ( unYearInt <= cLastYearForSearches)):
            return ''
        else:
            unYearString = '%04d' % unYearInt
        
            
            
        if not unMonthString:
            unMonthInt    = ( theEarliest and cFirstMonthForSearches) or cLastMonthForSearches
            unMonthString = '%02d' % unMonthInt
        else:
            unMonthInt = -1
            try:
                unMonthInt = int( unMonthString)
            except:
                None
            if ( unMonthInt >= cFirstMonthForSearches) and ( unMonthInt <= cLastMonthForSearches):
                unMonthString = '%02d' % unMonthInt
            else:
                unMonthInt    = ( theEarliest and cFirstMonthForSearches) or cLastMonthForSearches
                unMonthString = '%02d' % unMonthInt
            
            
        if not unDayString:
            unDayString = '%02d' % (( theEarliest and cFirstDayForSearches) or self.fFechaISOStringLastMonthDayInYear( unMonthInt, unYearInt))
        else:
            unDayInt = -1
            try:
                unDayInt = int( unDayString)
            except:
                None
            unLastDayForSearches = self.fFechaISOStringLastMonthDayInYear( unMonthInt, unYearInt)
            if ( unDayInt >= cFirstDayForSearches) and ( unDayInt <= unLastDayForSearches):
                unDayString = '%02d' % unDayInt
            else:
                unDayString = '%02d' % (( theEarliest and cFirstDayForSearches) or unLastDayForSearches)
            

        unNewDateString = '%s-%s-%s' % ( unYearString, unMonthString, unDayString,)
        return unNewDateString
    
    
    
        
    

            
    security.declarePublic( 'fHoraISOStringDesdeStringParcial')
    def fHoraISOStringDesdeStringParcial( self, theISOTimePartialString, theEarliest=True):
    
        if not theISOTimePartialString:
            return ''
        
        unaHoraString = theISOTimePartialString
            
        unosHourMinuteSecond = unaHoraString.split( cISOStringHoraHMSSeparator)
        if not unosHourMinuteSecond:
            return ''
        
        unHourString   = unosHourMinuteSecond[ 0]
        unMinuteString = ''
        unSecondString   = ''
        if len( unosHourMinuteSecond) > 1:
            unMinuteString = unosHourMinuteSecond[ 1]
        if len( unosHourMinuteSecond) > 2:
            unSecondString   = unosHourMinuteSecond[ 2]
            
            
            
        if not unHourString:
            return ''
        unHourInt = -1
        try:
            unHourInt = int( unHourString)
        except:
            None
        if not ( ( unHourInt >= cFirstHourForSearches) and ( unHourInt <= cLastHourForSearches)):
            return ''
        else:
            unHourString = '%02d' % unHourInt
        
            
            
        if not unMinuteString:
            unMinuteInt    = cFirstMinuteForSearches
            if not theEarliest:
                unMinuteInt = cLastMinuteForSearches
            unMinuteString = '%02d' % unMinuteInt
        else:
            unMinuteInt = -1
            try:
                unMinuteInt = int( unMinuteString)
            except:
                None
            if ( unMinuteInt >= cFirstMinuteForSearches) and ( unMinuteInt <= cLastMinuteForSearches):
                unMinuteString = '%02d' % unMinuteInt
            else:
                unMinuteInt    = cFirstMinuteForSearches
                if not theEarliest:
                    unMinuteInt = cLastMinuteForSearches
                unMinuteString = '%02d' % unMinuteInt
            
            
            
        if not unSecondString:
            unSecondInt    = cFirstSecondForSearches
            if not theEarliest:
                unSecondInt = cLastSecondForSearches
            unSecondString = '%02d' % unSecondInt            
        else:
            unSecondInt = -1
            try:
                unSecondInt = int( unSecondString)
            except:
                None
            if ( unSecondInt >= cFirstSecondForSearches) and ( unSecondInt <= cLastSecondForSearches):
                unSecondString = '%02d' % unSecondInt
            else:
                unSecondInt    = cFirstSecondForSearches
                if not theEarliest:
                    unSecondInt = cLastSecondForSearches
                unSecondString = '%02d' % unSecondInt            
            

        unNewTimeString = '%s:%s:%s' % ( unHourString, unMinuteString, unSecondString,)
        return unNewTimeString
        

    
    
    
    
    security.declarePublic( 'fFechaISOStringRounded')
    def fFechaISOStringRounded( self, theISODateString, theEarliest=True, theDefaultDate=None):
        if not theISODateString:
            return ''
        
        unFechaYHoraStrings = theISODateString.split( cISOStringFechaYHoraSeparator)
        if not unFechaYHoraStrings:
            return ''
         
        unaFechaStringCompleted = ''
        unaHoraStringCompleted  = ''
                
        if len( unFechaYHoraStrings) > 1:
            unaFechaStringCompleted = self.fFechaISOStringDesdeStringParcial( unFechaYHoraStrings[ 0], theEarliest)
            unaHoraStringCompleted  = self.fHoraISOStringDesdeStringParcial(  unFechaYHoraStrings[ 1], theEarliest)
                     
        else:
            unaFechaStringCompleted =           self.fFechaISOStringDesdeStringParcial( unFechaYHoraStrings[ 0], theEarliest)
            if not unaFechaStringCompleted:
                unaHoraStringCompleted  =       self.fHoraISOStringDesdeStringParcial(  unFechaYHoraStrings[ 0], theEarliest)
             
                
        if not ( unaFechaStringCompleted or unaHoraStringCompleted):
            return ''
        
        if not unaFechaStringCompleted:
            unaFechaStringCompleted = theDefaultDate.ISO()[:10]
        
        if not unaHoraStringCompleted:
            unaHoraStringCompleted = cISOStringEarliestDayTime
            if not theEarliest:
                unaHoraStringCompleted = cISOStringLatestDayTime        
            
        unFechaHoraResultado = '%s%s%s' % ( unaFechaStringCompleted, cISOStringFechaYHoraSeparator, unaHoraStringCompleted,)
        return unFechaHoraResultado
    

       




    # ####################################################################
    """Magic numbers to uses as HTTP request parameters, to avoid triggering of confirmed actions long time after the confirmation was requested.
    
    """

    
    
    security.declarePublic( 'fIsAcceptableMagicMilliseconds')
    def fIsAcceptableMagicMilliseconds(self, theString, theAllowedSeconds):   
                
        if not theString or not theAllowedSeconds:
            return False
        
        aLong = 0
        try:
            aLong = long( theString)
        except:
            None
        
        aDeMagicizedLong =  self.fDeMagicizeLong( aLong)

        
        aMilliseconds = aDeMagicizedLong
        if not aMilliseconds:
            return False
        
        aMillisecondsNow = self.fMillisecondsNow() 
        
        anAllowed = ( aMillisecondsNow > aMilliseconds) and  ( (aMillisecondsNow - aMilliseconds) <= ( theAllowedSeconds * 1000))
        return anAllowed
        
        
    
    
        
    security.declarePublic( 'fMagicMillisecondsNowString')
    def fMagicMillisecondsNowString(self):   
        
        someMilliseconds = self.fMillisecondsNow()
        
        aMagicizedMilliseconds = self.fMagicizeLong( someMilliseconds)
        
        unMagicMillisecondsString = str( aMagicizedMilliseconds)
        
        return unMagicMillisecondsString
    
    
    
    
    security.declarePublic( 'fMagicizeLong')
    def fMagicizeLong(self, theLong):   

        aLong = long( theLong)
        
        aMagicMask = TRACatalogo_Globales.gTRAMagicLongMask
        if not aMagicMask:
            return aLong

        aMagicizedLong = aLong ^ aMagicMask
        
        return aMagicizedLong 
             
    
    
    
    security.declarePublic( 'fDeMagicizeLong')
    def fDeMagicizeLong(self, theLong):   
        aLong = long( theLong)
        
        aMagicMask = TRACatalogo_Globales.gTRAMagicLongMask
        if not aMagicMask:
            return str( theString)
        
        aDeMagicizedLong = aLong ^ aMagicMask
                    
        return aDeMagicizedLong 
             



    
    
    
    
    
    # ####################################################################
    """Time accessors.
   
    """
  

    security.declarePublic( 'fDateTimeNow')
    def fDateTimeNow(self, ):   
        return DateTime()    
    
    
    security.declarePublic( 'fMillisecondsNow')
    def fMillisecondsNow(self, ):   
        """Time accessor to minimize instantiation of DateTime while profiling.
       
        """
   
        return int( time.time() * 1000)
    
        
    
    
    security.declarePublic( 'fDateTimeFromMilliseconds')
    def fDateTimeFromMilliseconds(self, theMilliseconds):   
        return DateTime( float( theMilliseconds / 1000))
    
    
    
    security.declarePublic( 'fDateTimeFromMillisecondsTextual')
    def fDateTimeFromMillisecondsTextual(self, theMilliseconds):   
        return DateTime( float( theMilliseconds / 1000)).ISO()
            
    
    
    security.declarePublic( 'fDateTimeFromMillisecondsTextual')
    def fDateTimeFromMillisecondsTextual(self, theMilliseconds): 
        return self.fDateToStoreString( self.fDateTimeFromMilliseconds( theMilliseconds))
    
    
    
    
    
    security.declarePublic( 'fDateTimeNowString')
    def fDateTimeNowString(self):   
        
        return self.fDateTimeToString( self.fDateTimeNow())
    
    
    
    
    security.declarePublic( 'fDateTimeToString')
    def fDateTimeToString(self, theDateTime):  
        if not theDateTime:
            return ''
        return str( theDateTime)
    
    
    
    
    
    security.declarePublic( 'fDateTimeNowTextual')
    def fDateTimeNowTextual(self):   
        return self.fDateToStoreString( self.fDateTimeNow())







   
    
   
    # #################################################
    """Handling of Dates as strings to avoid catalog schema overhead
    Using ISO format AAAA-MM-DD HH:MM:SS '2009-03-21 01:36:00'
    No time zone is stored. 
    It is encoded as the time in the server zone  (i.e. Valencia: Madrid Spain GMT+1)
    
    """
    
    
    security.declarePublic( 'fStoreStringToDate')
    def fStoreStringToDate( self, theString):
        if not theString:
            return None
        
        unDate = None
        try:
            unDate = DateTime( theString)   
        except:
            None
        
        return unDate
    
    
    
    security.declarePublic( 'fDateToStoreString')
    def fDateToStoreString( self, theDate):
        if not theDate:
            return None
        #%04d-%02d-%02d %02d:%02d:%02d YMDHMS
        unString = theDate.ISO()
        return unString
    
    

  


    

    security.declarePrivate( 'pSleepMilliseconds')
    def pSleepMilliseconds( self, theMilliseconds):
        if not cTRAYieldProcessorEnabled:
            return self
        
        if not theMilliseconds:
            return self
        
        unosSecondsToSleep = float( theMilliseconds) / 1000
        self.pSleepSeconds( unosSecondsToSleep)
        
        return self
    

        

    security.declarePrivate('pSleepSeconds')
    def pSleepSeconds( self, theSeconds):
        if not cTRAYieldProcessorEnabled:
            return self
        
        if not theSeconds:
            return self
        
        unosSecondsToSleep = float( theSeconds) 
        time.sleep( unosSecondsToSleep )
        
        return self
    

    

