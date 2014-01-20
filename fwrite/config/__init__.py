#!/usr/bin/env python
#encoding=utf-8
#by Fooying 2013-11-17 01:49:57
'''
配置读写相关方法
'''

import os
import sys
import ConfigParser
reload(sys)
sys.setdefaultencoding('utf-8') 
from ..utils import *

CONFIG = ConfigParser.ConfigParser()
FILE_PATH = os.path.join(os.path.dirname(__file__), 'config.fwrite')

def write_config(item, key, value):
    CONFIG.read(FILE_PATH)
    with open(FILE_PATH, 'w') as f: 
        if item not in CONFIG.sections(): 
            CONFIG.add_section(item) 
        value = str_encrypt(value)
        CONFIG.set(item, key, value)
        CONFIG.write(f)

def read_config(item, key):
    try:
        CONFIG.read(FILE_PATH)
        value = CONFIG.get(item, key)
        value = str_decrypt(value)
    except:
        value = ''
    return value 

if __name__ == '__main__':
    write_config('base', 'icp', '闽ICP备12005824号-5')
    print read_config('base', 'icp')
