import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
import os
from Products.ZopeChinaPak import config

class clientEncoding(ZopeTestCase.ZopeTestCase):

    def afterSetup(self):
        pass

    def beforeTearDown(self):
        pass

    def testClientEncoding(self):
        if os.name == 'nt':
            self.assertEqual(config.FTP_CLIENT_ENCODING, 'mbcs')
        else:
            self.assertEqual(config.FTP_CLIENT_ENCODING, 'gb18030')

if __name__ == '__main__':
    framework()

