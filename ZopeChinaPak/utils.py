'''
Copyright: ZopeChina Corp, Ltd. http://zopechina.com
'''

from Products.ZCTextIndex import ZCTextIndex
from Products.ZCatalog.ZCatalog import ZCatalog

class Empty: pass

def modifyCatalogTextIndexToSupportChinese(catalog, indexes=[]):

    if not indexes:
        for index in catalog.indexes():
            indexobj = catalog._catalog.getIndex(index)
            if indexobj.meta_type in ['TextIndex', 'ZCTextIndex']:
                indexes.append(index)

    # delete the TextIndex
    for index in indexes:
        catalog.delIndex(index)

    # add Lexicon
    elem = []
    wordSplitter = Empty()
    wordSplitter.group = 'Word Splitter'
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
    ZCTextIndex.manage_addLexicon(catalog, 'CJKLexicon', 'Default Lexicon', elem)

    # add indexes
    for index in indexes:
        title_extras = Empty()
        title_extras.doc_attr = index
        title_extras.index_type = 'Okapi BM25 Rank'
        title_extras.lexicon_id = 'CJKLexicon'
        catalog.addIndex(index, 'ZCTextIndex', title_extras)

