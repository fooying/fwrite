#!/usr/bin/env python
#encoding=utf-8
#by Fooying 2013-11-18 23:58:45
'''
通用方法调用模块
'''

import base64
import urllib

def str_encrypt(text):
    text =  base64.b64encode(text)
    text = urllib.quote_plus(text)
    return text

def str_decrypt(text):
    text = urllib.unquote_plus(text)
    text = base64.b64decode(text)
    return text
