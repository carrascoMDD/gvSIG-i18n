from Products.CMFPlone.Portal import addPolicy
from Products.CMFPlone.CustomizationPolicy import DefaultCustomizationPolicy

##########################
# Chinese Policy
##########################
class ZopeChinaDefaultCustomizationPolicy(DefaultCustomizationPolicy):
    """ policy for Chinese Plone Site """

    def customize(self, portal):
        DefaultCustomizationPolicy.customize(self, portal)
        mi_tool = portal.portal_migration
        zcps = mi_tool._getWidget('ZopeChinaPak Setup')
        zcps.addItems(zcps.available())

addPolicy('Default Chinese Plone', ZopeChinaDefaultCustomizationPolicy())

##########################
# use Pinyin for id
##########################
from pinyin import PinYinDict
from Products.CMFPlone import UnicodeNormalizer

UnicodeNormalizer.mapping.update(PinYinDict)

del PinYinDict

####################
# make plone 2.1 can support chinese
#####################
from Products.CMFPlone import PloneTool
import re

PloneTool.BAD_CHARS = re.compile(r'[^a-zA-Z0-9-_~,.$\(\)# ]%').findall

