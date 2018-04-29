#!/usr/bin/python

# copyright reserved by: www.zopechina.com

win_runzeo_template = r"""@set PYTHON=%(python)s
@set ZODB3_HOME=%(zodb3_home)s
@set PYTHONPATH=%(zodb3_home)s
@set CONFIG_FILE=%(instance_home)s\etc\%(package)s.conf

"%(python)s" "%(zodb3_home)s\ZEO\runzeo.py" -C "%(instance_home)s\etc\%(package)s.conf"
pause
"""

win_zeo_service = r"""import os.path
from os.path import dirname
import sys

PYTHON=r'%(python)s'

PYTHONW = dirname(PYTHON) + r'\pythonw.exe'
SOFTWARE_HOME=r'%(zodb3_home)s'
INSTANCE_HOME = r'%(instance_home)s'

ZEO_RUN = SOFTWARE_HOME + r'\ZEO\runzeo.py'
CONFIG_FILE= os.path.join(INSTANCE_HOME, 'etc', 'zeo.conf')
PYTHONSERVICE_EXE=dirname(PYTHON) + r'\PythonService.exe'

sys.path.insert(0, SOFTWARE_HOME)

from nt_svcutils.service import Service

servicename = 'ZEO_' + str(hash(INSTANCE_HOME.lower()))

class InstanceService(Service):
    start_cmd = '"'+ PYTHONW + '" "' + ZEO_RUN + '" -C "' + CONFIG_FILE + '"'
    _svc_name_ = servicename
    _svc_display_name_ = 'ZEO instance at ' + INSTANCE_HOME
    _exe_name_ = PYTHONSERVICE_EXE

if __name__ == '__main__':
    import win32serviceutil
    win32serviceutil.HandleCommandLine(InstanceService)
"""

def create(self, home, params):
    original_create(self, home, params)
    makefile(win_runzeo_template, home, "bin", "runzeo.bat", **params)
    makefile(win_zeo_service, home, "bin", "zeoservice.py", **params)


######################################################
# copy from /zope/bin/mkzeoinstance.py
######################################################

import os
import sys

mydir = os.path.dirname(os.path.abspath(sys.argv[0]))
zopehome = os.path.dirname(mydir)
softwarehome = os.path.join(zopehome, "lib", "python")

if softwarehome not in sys.path:
    sys.path.insert(0, softwarehome)

from ZEO.mkzeoinst import ZEOInstanceBuilder, makefile
from ZEO import mkzeoinst

mkzeoinst.zeo_conf_template += """\

# include other zeo config files here
# %%include db.conf

"""

# Pack here
original_create = ZEOInstanceBuilder.create
ZEOInstanceBuilder.create = create

if __name__ == "__main__":
    ZEOInstanceBuilder().run()


