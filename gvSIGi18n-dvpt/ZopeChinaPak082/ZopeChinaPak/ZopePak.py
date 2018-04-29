#############################################################
# Support Chinese ID
############################################################
from OFS import ObjectManager
import re
ObjectManager.bad_id=re.compile(r'[^a-zA-Z0-9-_~,.$\(\)# ]%').search #TS 

import ftp_pak
# import dav_pak
