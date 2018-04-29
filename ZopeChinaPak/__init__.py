# Copyright: ZopeChina Corp, Ltd. http://zopechina.com
# hack python's default encoding to 'utf-8'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
del sys.setdefaultencoding

import os
from encodings.aliases import aliases

# gb2312 is obsoleted, use gbk
for k,v in aliases.items():
    if v == 'cjkcodecs.gb2312':
        aliases[k] = 'cjkcodecs.gbk'
        
if os.name == 'nt':
    import encodings
    for ec in ['gb2312', 'gbk', 'gb18030', 'big5']:
        if not encodings.aliases.aliases.has_key(ec):
            encodings.aliases.aliases[ec] = 'mbcs'
            # clear cache
            if encodings._cache.has_key(ec):
                del encodings._cache[ec]


import ZopePak
import StructuredTextPak
import setup
try:
    import PlonePak
except ImportError:
    pass

try:
    import CMFPak
except ImportError:
    pass

try:
    import at_pak
except ImportError:
    pass

try:
    from Products.CMFPlone.interfaces import IPloneSiteRoot
    from Products.GenericSetup import EXTENSION, profile_registry
    HAS_GENERICSETUP = True
except ImportError:
    HAS_GENERICSETUP = False

def initialize(context):
    app = context._ProductContext__app
    if not app.hasProperty('management_page_charset'):
        app.manage_addProperty('management_page_charset', 'utf-8', 'string')

    if HAS_GENERICSETUP:
        profile_registry.registerProfile('ZopeChinaPak',
                'Chinese Plone Site',
                'Extension profile for default Chinese Plone setup',
                'profiles/default',
                'ZopeChinaPak',
                EXTENSION,
                for_=IPloneSiteRoot)

