#coding=utf-8
'''
后台路由模块
'''
from fwrite.config import read_config
admin = read_config('base', 'admin')

urls = (
    '/%s'%admin, 'admin.views.index',
    '/%s/login'%admin, 'admin.views.login',
    '/%s/logout'%admin, 'admin.views.logout',
    '/%s/base'%admin, 'admin.views.base',
    '/%s/columns'%admin, 'admin.views.columns',
    '/%s/columns/del'%admin, 'admin.views.colunms_del',
    '/%s/article'%admin, 'admin.views.article',
    '/%s/article/edit'%admin, 'admin.views.article_edit',
    '/%s/article/del'%admin, 'admin.views.article_del',
    )

