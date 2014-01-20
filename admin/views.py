#!/usr/bin/python
#encoding=utf-8

import web
import os
import hashlib
import time
import datetime
from web.net import htmlquote

from fwrite.template import template_render
from fwrite.config import read_config,write_config
from fwrite.db import *
from index import session

PATH = os.path.join(os.path.dirname(__file__), '../templates', 'admin')
ADMIN = read_config('base', 'admin') 

def iflogin():
    login = session.get('login', False)
    if not login:
        raise web.seeother('/%s/login'%ADMIN)

class login:
    def POST(self):
        data = web.input()
        user = hashlib.md5(data.get('user', '')).hexdigest()
        passwd = hashlib.md5(data.get('passwd', '')).hexdigest()
        o_user = read_config('login', 'user')
        o_passwd = read_config('login', 'passwd')
        if user == o_user and passwd == o_passwd:
            session.login = True
            raise web.seeother('/%s'%ADMIN)
        else:
            session.login = False
            raise web.seeother('/%s/login'%ADMIN)

    def GET(self):
        content = {}
        return template_render('login.html', PATH, content)

class logout:
        def run(self):
            session.login = False
            raise web.seeother('/%s/login'%ADMIN)

        def POST(self):
            self.run()

        def GET(self):
            self.run()

class index:
    def run(self):
        iflogin()
        content = {}
        return template_render('index.html', PATH, content)

    def GET(self):
        return self.run()

    def POST(self):
        return self.run()

class base:
    def GET(self):
        iflogin()
        content = {}
        return template_render('admin_baseedit.html', PATH, content)
    
    def POST(self):
        iflogin()
        data = web.input()
        keys = {
                'site_title':'site_title',
                'site_keywords':'site_keywords',
                'site_descript':'site_descript',
                'site_icp':'icp',
                'site_count':'count_code',
                'site_comment':'comment_code',
                'site_admin':'admin',
                }
        for key in keys:
            value = data.get(key, '') 
            write_config('base', keys[key], value)
        user = data.get('user', 'admin')
        passwd = data.get('passwd', 'admin')
        write_config('login', 'user', hashlib.md5(user).hexdigest())
        write_config('login', 'passwd', hashlib.md5(passwd).hexdigest())
        raise web.seeother('/%s/base'%ADMIN)

class columns:
    def GET(self):
        iflogin()
        data = web.input()
        new_name = data.get('new_name', '')
        key = data.get('key', '')
        if new_name and key:
            value_dict = {'key':key, 'name':htmlquote(new_name)}
            update_column(key, value_dict)
            raise web.seeother('/%s/columns'%ADMIN)
        else:
            cs = get_columns()
            content = {'columns':cs}
            return template_render('admin_columns.html', PATH, content)
        
    def POST(slef):
        iflogin()
        data = web.input()
        column_name = data.get('column_name', '')
        if column_name:
            key = hashlib.md5(column_name+str(time.time())).hexdigest()
            value_dict = {'key':key, 'name':htmlquote(column_name)}
            update_column(key, value_dict)
        raise web.seeother('/%s/columns'%ADMIN)

class colunms_del:
    def GET(self):
        iflogin()
        data = web.input()
        del_key = data.get('key', '')
        if del_key:
            del_column(del_key)
        raise web.seeother('/%s/columns'%ADMIN)

    def POST(self):
        iflogin()
        data = web.input(columns = [])
        columns = data.get('columns', [])
        for c in columns:
            del_column(c)
        raise web.seeother('/%s/columns'%ADMIN)

class article:
    def GET(self):
        iflogin()
        data = web.input()
        column = data.get('column', '') 
        if column == 'all':
            column = ''
        articles = get_articles(column)
        cs = get_columns()
        content = {'columns':cs,'articles':articles}
        return template_render('admin_article.html', PATH, content)

class article_del:
    def GET(self):
        iflogin()
        data = web.input()
        key = data.get('key', '')
        if key:
            del_article(key)
        raise web.seeother('/%s/article'%ADMIN)

    def POST(self):
        iflogin()
        data = web.input(articles = [])
        articles = data.get('articles', [])
        for a in articles:
            del_article(a)
        raise web.seeother('/%s/article'%ADMIN)

class article_edit:
    def GET(self):
        iflogin()
        data = web.input()
        key = data.get('key', '')
        article = {}
        if key:
            article = get_article(key) 
            if not article:
                raise web.seeother('/%s/article'%ADMIN)
            article['column_name'] = ''
            article['key'] = key
            column_key = article.get('column', '')
            article['tag'] = ','.join(article.get('tag', []))
            if column_key:
                columns = get_columns(column_key) 
                if columns:
                    article['column_name'] = columns[0].get('name', '')
        cs = get_columns()
        content = {'article':article, 'columns':cs}
        return template_render('admin_article_edit.html', PATH, content)


    def POST(self):
        iflogin()
        data = web.input()
        title = data.get('title', '')
        content = data.get('content', '')
        column = data.get('column', '')
        tag = data.get('tag', '')
        c_time = datetime.datetime.now()
        key = data.get('key', '')
        if not key:
            key = hashlib.md5(title+str(time.time())).hexdigest()
        value_dict = {
            'key':key,
            'title':htmlquote(title),
            'content':content,
            'c_time':c_time,
            'column':htmlquote(column),
            'tag':[htmlquote(t) for t in tag.split(',')]
        }
        update_article(key, value_dict)
        raise web.seeother('/%s/article'%ADMIN)
