# 处理IE中文件下载的乱码问题
# 目前暂未考虑繁体编码用户，另外，参考 /Archetypes/utils.py 中的contentDispositionHeader方法

# 暂时未启用

from types import UnicodeType 

def download(self, instance, REQUEST=None, RESPONSE=None):
    file = self.get(instance)
    if not REQUEST:
        REQUEST = instance.REQUEST
    if not RESPONSE:
        RESPONSE = REQUEST.RESPONSE
    RESPONSE.setHeader('Content-Type', self.getContentType(instance))
    filename = self.getFilename(instance, fromBaseUnit=False)
    if REQUEST.HTTP_USER_AGENT.find('MSIE') != -1:
        if type(filename) is UnicodeType:
            filename = filename.encode('gb18030')
        else:
            filename = filename.decode('utf8').encode('gb18030')
    RESPONSE.setHeader('Content-Disposition',
                       'attachment; filename="%s"' % filename)
    RESPONSE.setHeader('Content-Length', self.get_size(instance))
    return file.index_html(REQUEST, RESPONSE)

from Products.Archetypes.Field import FileField 
# 可取消下面的这行注释，启用
# FileField.download = download

