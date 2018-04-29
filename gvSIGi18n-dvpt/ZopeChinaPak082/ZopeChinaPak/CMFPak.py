#########################################################################
# patch CMFCalendar for plone portlet_calendar when use local zh_CN.utf8
#
# the original implemtation will use only first 2 charactors,
# but Chinese symbol in utf8 is at least 3 charactors.
#########################################################################
from Products.CMFCalendar.CalendarTool import CalendarTool

def getDays(self):
    """ get weekdays abr without any localizations """
    return ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']

CalendarTool.getDays = getDays

