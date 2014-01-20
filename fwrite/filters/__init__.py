#!/usr/bin/env python
#encoding=utf-8
#by Fooying 2013-11-17 01:57:59

'''
过滤器
'''
import datetime
from ..config import read_config

FILTERS = ['get_base', 'get_url', 'get_version', 'get_year', 'get_this_site', 'get_icp']

def get_base(name):
    if name:
        value = read_config('base', name)
    else:
        value = ''
    return value

def get_url(name):
    value = read_config('system', 'office_url')
    return value

def get_version(name):
    value = read_config('system', 'version')
    return value

def get_year(name):
   return datetime.datetime.now().strftime('%Y')

def get_this_site(name):
    value = read_config('base', 'name')
    return value

def get_icp(name):
    value = read_config('base', 'icp')
    return value




