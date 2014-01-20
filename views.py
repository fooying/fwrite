#!/usr/bin/python
#encoding=utf-8

import web
import os
import json
from web.net import htmlquote

from fwrite.template import template_render
from fwrite.db import *

PATH = os.path.join(os.path.dirname(__file__), 'templates')

class JSONDateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)

class index:
    def run(self):
        content = {}
        return template_render('index.html', PATH, content)

    def GET(self):
        return self.run()

    def POST(self):
        return self.run()

class article_show:
    def GET(self, key):
        if key:
            key = htmlquote(key)
            article = get_article(key)
            if article:
                column_key = article.get('column', '')
                columns = get_columns(column_key) 
                if columns:
                    article['column_name'] = columns[0].get('name', '')
                content = {'article':article}
                return template_render('article.html', PATH, content)
            else:
                raise web.seeother('/')
        else:
            raise web.seeother('/')

class ajax_columns:
    def GET(self):
        data = web.input()
        page = data.get('page', 1)
        try:
            int(page)
        except:
            page = 1
        columns = get_columns(page = 1)
        cs = {'columns':{}}
        for c in columns:
            key = str(c.get('key',''))
            name = str(c.get('name',''))
            if key and name:
                cs['columns'][key] = {'key':key, 'name':name}
        return json.dumps(cs,cls=JSONDateTimeEncoder)

class ajax_articles:
    def GET(self):
        data = web.input()
        page = data.get('page', 1)
        column_key = htmlquote(data.get('coumn_key', ''))
        try:
            int(page)
        except:
            page = 1
        articles = get_articles(column_key = column_key,page = page)
        arts = {'articles':{}}
        for c in articles:
            key = str(c.get('key',''))
            title = str(c.get('title',''))
            if key and title:
                arts['articles'][key] = {'key':key, 'title':title}
        return json.dumps(arts,cls=JSONDateTimeEncoder)

