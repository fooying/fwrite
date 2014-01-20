#coding=utf-8
'''
路由模块，这是只是把路由地址分出来
'''
from admin import url as admin_url
from ueditor import url as ueditor_url

urls = (
    '/', 'views.index',
    '/article/(.*)', 'views.article_show',
    '/ajax/columns', 'views.ajax_columns',
    '/ajax/articles', 'views.ajax_articles',
    )
urls += admin_url.urls
urls += ueditor_url.urls

