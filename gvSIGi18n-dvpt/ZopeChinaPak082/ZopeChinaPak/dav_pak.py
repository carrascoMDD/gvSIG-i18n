from config import FTP_CLIENT_ENCODING

###############################################################################
# pak for better webdav encoding support
# also hack to trim windows xp auth hostname, which is hostname\username,
###############################################################################
from ZServer.HTTPServer import zhttp_handler
from base64 import decodestring, encodestring

# "Microsoft .* DAV 1.1" gb
# "(Microsoft .* DAV $)" UTF-8 gb18030 big5
# "Microsoft .* DAV" UTF-8 gb18030 big5
# "(Microsoft .* DAV 1.1)" gb18030 big5
# "Microsoft-WebDAV*" UTF-8 gb18030
# "RMA/*" gb18030
# cadaver/
import re
gb_agent_rex = re.compile('Microsoft .* DAV 1.1|Microsoft .* DAV$|cadaver/|RMA/*')

original_get_environment = zhttp_handler.get_environment

def get_environment(self, request):
    env = original_get_environment(self, request)

    if gb_agent_rex.search(env.get("HTTP_USER_AGENT", "")):
        try:
            unicode(env["PATH_INFO"], 'utf-8')
        except:
            env["PATH_INFO"] = env["PATH_INFO"].decode(FTP_CLIENT_ENCODING).encode('utf-8')
            env["PATH_TRANSLATED"] = env["PATH_TRANSLATED"].decode(FTP_CLIENT_ENCODING).encode('utf-8')

    # trim windows xp auth hostname
    if env.has_key('HTTP_AUTHORIZATION') and env['HTTP_AUTHORIZATION'][:6].lower() == 'basic ':
        [name,password] = decodestring(env['HTTP_AUTHORIZATION'][6:]).split(':')
        env['HTTP_AUTHORIZATION'] = 'Basic %s' % encodestring('%s:%s' % (name.split('\\')[-1], password))
    return env

zhttp_handler.get_environment = get_environment

#############################################################################
# hack zope if you wanto support windows webfolder
#############################################################################
from webdav.Collection import Collection
from webdav.Resource import Resource
from ZServer.HTTPResponse import ZServerHTTPResponse

original_resource_dave__init = Resource.dav__init
def resource_dav__init(self, request, response):
    response.setHeader('MS-Author-Via', 'DAV')
    # see: http://teyc.editthispage.com/2005/06/02
    response.setHeader('Public', ', '.join(self.__http_methods__))
    # response.setHeader('DAV/2', '')
    original_resource_dave__init(self, request, response)

Resource.dav__init = resource_dav__init

original_collection_dave__init = Collection.dav__init
def collection_dav__init(self, request, response):
    response.setHeader('MS-Author-Via', 'DAV')
    # see: http://teyc.editthispage.com/2005/06/02
    response.setHeader('Public', ', '.join(self.__http_methods__))
    # response.setHeader('DAV/2', '')
    original_collection_dave__init(self, request, response)

Collection.dav__init = collection_dav__init

original_response_str = ZServerHTTPResponse.__str__
def response_str(self, html_search=re.compile('<html>',re.I).search):
    if not self.headers.has_key("Etag"):
        self.setHeader('Etag','')
    self.setHeader('MS-Author-Via', 'DAV')
    # self.setHeader('DAV/2', '')
    return original_response_str(self, html_search)

ZServerHTTPResponse.__str__ = response_str
