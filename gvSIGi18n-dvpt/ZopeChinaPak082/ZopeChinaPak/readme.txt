What is ZopeChinaPak?

  This is a patch and extension for Zope, CMF, Plone and other products to support Chinese better. If you don't use Chinese, you need not to touch it.  

Feature

  * ZMI Chinese Support: set management_page_charset property of zope automatically if it is not exist

   - Name: management_page_charset 

   - type: string 

   - value: utf-8

  * Structured Text Chinese support

  * Zope Chinese Id support. Chinese Id support may cause other problems. But we think it is useful.

  * support Chinese file name when ftp. Note: you must change value of the 'LOCAL_FTP_ENCODING' value in conf.py to correct encoding

  * use plone2 cutomise policy and methods. You can select 'Default Chinese
    Plone' policy when you add a new plone site in ZMI. The policy uses CJKSplitter
    to support Chinese full text search.

  * easy to install and easy to upgrade.

  * add Chinese codecs aliases under windows: gb2312/gbk/gb18030

License:

    ZopeChinaPak is (C) by ZopeChina.com and published as open-source.
    See LICENSE.txt for the full text of the GPL license.

About ZopeChina

  ZopeChinaPak is contributed by "ZopeChina":http://www.zopechina.com .
ZopeChina is one of the leading Zope Service Providers in China. We also runs the famous "CZUG.org":http://CZUG.org (China Zope User Group). We are trying to make Zope/CMF/Plone works better for Chinese. 
  
