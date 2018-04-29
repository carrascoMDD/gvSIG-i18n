CJKSplitter - Chinese, Japanese, Korean word splitter for ZCTextIndex

  CJKSplitter is a ZCTextIndex splitter for CJK (Chinese-Japenese-Korea) text
  stored as Unicode.  It uses a simple, but workable, "hack" instead of trying
  to do real word splitting from dictionaries.  Compared to a dictionary based
  word splitter, this results in a bigger index and more matches than necessary,
  but it is a cheap price to pay for the reduced complexity.

Feature

  - use regular expression to compatible with defualt English white space
    splitter

  - much simpler code, easy to install, easy to use

  - support multiple encodings: unicode/utf-8/gb18030/gbk/gb2312/mbcs/big5.
    provide 3 splitters(more to come):

    * 'CJK splitter' : support unicode/utf-8 encoding. this encoding is
      compatible with version 0.1

    * 'CJK GB splitter' : support unicode/gb18030/gbk/gb2312/mbcs encodings.

    * 'CJK BIG5 splitter' : support unicode/big5/mbcs encodings

  - smaller index storage for CJK: index stored as unicode(2 byts) but not
    utf-8(3 bytes)

  - support english globing

  - support single Chinese charactor search

About ZopeChina

  ZopeChina.com is a leading ZSP(Zope Service Provider) in China. We are also
the supporter for CZUG.org (China Zope User Group). We are trying to make
Zope/CMF/Plone works for the Chinese people. We wish all the Chinese Zope guys
can be together and make zope works better for Chinese:)

  Contact us with : pan_junyong@yahoo.com.cn

