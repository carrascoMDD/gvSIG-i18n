from config import FTP_CLIENT_ENCODING
from types import UnicodeType
from ZServer.medusa.ftp_server import ftp_channel, xmit_channel, filesys
original_found_terminator = ftp_channel.found_terminator
def found_terminator(self):
    self.in_buffer = unicode(self.in_buffer, FTP_CLIENT_ENCODING).encode('utf8')
    result = ''
    return original_found_terminator(self)
ftp_channel.found_terminator = found_terminator

from asynchat import async_chat
original_push_with_producer = async_chat.push_with_producer

from ZServer.medusa.producers import file_producer, simple_producer

class encoding_wrapper_producer:
    def __init__(self, producer, fromEncoding='utf8', toEncoding=FTP_CLIENT_ENCODING):
        self.fromEncoding = fromEncoding
        self.toEncoding = toEncoding
        self.producer = producer

    def more(self):
        more_string = self.producer.more()
	if type(more_string) is UnicodeType:
	    return more_string.encode(self.toEncoding)
	else:
            return more_string.decode(self.fromEncoding).encode(self.toEncoding)

from types import StringType
def push(self, producer, encoding=True):
    fromEncoding = 'utf8'

    if encoding and type(producer) is StringType:
        # since simple_producer will split string, so i give unicode string to it
        producer = simple_producer(producer.decode(fromEncoding) )

    # don't do codec when upload a file
    if encoding and not isinstance(producer, file_producer):
        producer = encoding_wrapper_producer(producer, fromEncoding)
    return original_push_with_producer(self, producer)

ftp_channel.push_with_producer = push
xmit_channel.push_with_producer = push
ftp_channel.push  = push
xmit_channel.push = push

from ZServer.FTPServer import zope_ftp_channel
zope_ftp_channel.push_with_producer = push
zope_ftp_channel.push = push
import asynchat

# don't do codec when download files
def retr_completion(self, file, response):
        status=response.getStatus()
        if status==200:
            self.make_xmit_channel()
            if not response._wrote:
                # chrism: we explicitly use a large-buffered producer here to
                # increase speed.  Using "client_dc.push" with the body causes
                # a simple producer with a buffer size of 512 to be created
                # to serve the data, and it's very slow
                # (about 100 times slower than the large-buffered producer)
                self.client_dc.push_with_producer(
                    asynchat.simple_producer(response.body, 1<<16), False)
                # chrism: if the response has a bodyproducer, it means that
                # the actual body was likely an empty string.  This happens
                # typically when someone returns a StreamIterator from
                # Zope application code.
                if response._bodyproducer:
                    self.client_dc.push_with_producer(response._bodyproducer, False)
            else:
                for producer in self._response_producers:
                    self.client_dc.push_with_producer(producer, False)
            self._response_producers = None
            self.client_dc.close_when_done()
            self.respond(
                    "150 Opening %s mode data connection for file '%s'" % (
                        self.type_map[self.current_mode],
                        file
                        ))
        elif status in (401, 403):
            self.respond('530 Unauthorized.')
        else:
            self.respond('550 Error opening file.')
zope_ftp_channel.retr_completion = retr_completion

## fix zope bug
## should be removed when zope fixed this bug

def rnfr_completion(self,response):
    status=response.getStatus()
    if status==200:
        self.respond ('350 RNFR command successful.')
    else:
        self.respond ('550 %s: no such file or directory.' % self.fromfile)

from ZServer.FTPServer import zope_ftp_channel
zope_ftp_channel.rnfr_completion = rnfr_completion

old_cmd_cwd = zope_ftp_channel.cmd_cwd
def cmd_cwd (self, line):
    """ 当上传一个中文名文件夹的时候，windows自带的webfolder会发送带 ``??`` CWD命令::

    61.171.153.131 4205 <== opts utf8 on
    61.171.153.131 4205 ==> 500 'opts': command not understood.
    61.171.153.131 4205 <== PWD
    61.171.153.131 4205 ==> 257 "/" is the current directory.
    61.171.153.131 4205 <== CWD /nhd/gongsiziliao/danju/??/
    61.171.153.131 4205 ==> 550 No such directory.
    """

    if line[1].find('?') != -1:
        self.respond('250 ? in path, skip this command, hacked by zopen.cn.')
        return
    old_cmd_cwd (self, line)

zope_ftp_channel.cmd_cwd = cmd_cwd
