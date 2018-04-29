# FTP_CLIENT_ENCODING
from encodings import search_function
FTP_CLIENT_ENCODINGS = ('gb18030', 'gbk', 'gb2312', 'big5')

FTP_CLIENT_ENCODING = 'utf8'
try:
    search_function('mbcs')   # windows
    FTP_CLIENT_ENCODING = 'mbcs'
except:
    for en in FTP_CLIENT_ENCODINGS:
        if search_function(en):
           FTP_CLIENT_ENCODING = en
           break
