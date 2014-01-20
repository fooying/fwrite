#!/usr/bin/env python
#encoding=utf-8
#by Fooying 2013-11-17 01:21:59
'''
模板相关方法
'''

import web
from jinja2 import Environment, FileSystemLoader

from .. import filters

def template_render(template_name, path, content):
    '''
    模板渲染方法
    '''
    extensions = content.pop('extensions', [])
    globals = content.pop('globals', {})

    env = Environment (
        loader = FileSystemLoader(path),
        extensions = extensions,
        )
    env.globals.update(globals)
    for method in filters.FILTERS:
        env.filters[method] = getattr(filters, method)
    return env.get_template(template_name).render(content)
