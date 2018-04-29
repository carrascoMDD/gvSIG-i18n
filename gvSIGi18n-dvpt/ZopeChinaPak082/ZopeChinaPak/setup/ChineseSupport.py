from OFS.PropertyManager import PropertyManager
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.Expression import Expression
from Products.ExternalMethod.ExternalMethod import manage_addExternalMethod
from Products.CMFPlone.migrations.migration_util import safeEditProperty
from Acquisition import aq_get

from Products.SiteErrorLog.SiteErrorLog import manage_addErrorLog

from zLOG import INFO, ERROR
from Products.CMFPlone.setup.SetupBase import SetupWidget
from Products.ZCTextIndex import ZCTextIndex

def updateCatalogIndice(self, portal):
    """update date and text indice"""
    catalog = getToolByName(portal, 'portal_catalog')
    textIndice = ['Title', 'Description', 'SearchableText']

    class Empty: pass

    elem = []
    wordSplitter = Empty()
    wordSplitter.group = 'Word Splitter'
    #wordSplitter.name = 'Whitespace splitter'
    # For Chinese, Use: 'CJK splitter'
    wordSplitter.name = 'CJK splitter'

    caseNormalizer = Empty()
    caseNormalizer.group = 'Case Normalizer'
    caseNormalizer.name = 'Case Normalizer'

    stopWords = Empty()
    stopWords.group = 'Stop Words'
    stopWords.name = 'Remove listed and single char words'

    elem.append(wordSplitter)
    elem.append(caseNormalizer)
    elem.append(stopWords)

    if hasattr(catalog, 'CJKLexicon'):
         catalog.manage_delObjects(ids=['CJKLexicon'])
    ZCTextIndex.manage_addLexicon(catalog, 'CJKLexicon', 'CJK Lexicon', elem)

    # add index
    extras = Empty()
    extras.index_type = 'Okapi BM25 Rank'
    extras.lexicon_id = 'CJKLexicon'

    for indexName in textIndice:
        try:
	   # maybe not exist
           catalog.delIndex(indexName)
	except:
	   pass
        catalog.manage_addIndex(indexName, 'ZCTextIndex', extras)

    # reindex
    catalog.manage_reindexIndex(ids=textIndice)
    
def changePortalSettings(self, portal):
    p=portal.portal_properties.site_properties
    safeEditProperty(p, 'default_language', 'zh', 'string')
    # safeEditProperty(p, 'default_charset', 'utf-8', 'string')
    # safeEditProperty(p, 'localLongTimeFormat', '%Y-%m-%d %H:%M', 'string')

    #p=portal.portal_properties.navtree_properties
    #safeEditProperty(p, 'croppingLength', '10', 'int')

functions = {
    'updateCatalogIndice':updateCatalogIndice,
    'changePortalSettings':changePortalSettings,
    }

class ChineseSupportSetup(SetupWidget):
    type = 'ZopeChinaPak Setup'

    description = """This tries make Plone support Chinese better. can NOT be uninstall right now!"""

    def setup(self):
        pass

    def delItems(self, fns):
        out = []
        out.append(('Currently there is no way to remove a function', INFO))
        return out

    def addItems(self, fns):
        out = []
        for fn in fns:
            functions[fn](self, self.portal)
            out.append(('Function %s has been applied' % fn, INFO))
        return out

    def installed(self):
        return []

    def available(self):
        """ Go get the functions """
        return functions.keys()
