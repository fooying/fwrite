#!/usr/bin/env python
#encoding=utf-8
#by Fooying 2013-11-19 01:17:01

'''
数据处理模块
'''

import pymongo
from ..config import read_config

HOST = read_config('db', 'host')
PORT = read_config('db', 'port')
PORT = int(PORT) if int(PORT) else 27017
DB = read_config('db', 'db')

def get_columns(key = '', page = None):
    mongo = ''
    mongo = pymongo.Connection(HOST, PORT)
    db = mongo[DB]
    if key:
        spec = {'key':key}
    else:
        spec = {}
    if page:
        skip = (page - 1) * 20
        columns = db.columns.find(spec).skip(skip).limit(20)
    else:
        columns = db.columns.find(spec)
    if mongo:
        mongo.close()
    return list(columns)

def del_column(key):
    mongo = ''
    mongo = pymongo.Connection(HOST, PORT)
    db = mongo[DB]
    if key:
        db.columns.remove({'key':key})
    if mongo:
        mongo.close()
        
def update_column(key, value_dict):
    mongo = ''
    mongo = pymongo.Connection(HOST, PORT)
    db = mongo[DB]
    if key and value_dict:
        db.columns.update({'key':key}, value_dict, upsert=True)
    if mongo:
        mongo.close()

def get_articles(column_key = '', page = None):
    mongo = ''
    mongo = pymongo.Connection(HOST, PORT)
    db = mongo[DB]
    if column_key:
        spec = {'column':column_key}
    else:
        spec = {}

    if page:
        skip = (int(page) - 1) * 20
        articles = db.articles.find(spec,{'_id':False}).skip(skip).limit(20)
    else:
        articles = db.articles.find(spec,{'_id':False}).limit(20)

    if mongo:
        mongo.close()
    return list(articles)

def get_article(key):
    mongo = ''
    mongo = pymongo.Connection(HOST, PORT)
    db = mongo[DB]
    article = None
    if key:
        article = db.articles.find_one({'key':key},{'_id':False})
    if not article:
        article = {}
    if mongo:
        mongo.close()
    return article
 
def del_article(key):
    mongo = ''
    mongo = pymongo.Connection(HOST, PORT)
    db = mongo[DB]
    if key:
        db.articles.remove({'key':key})
    if mongo:
        mongo.close()

def update_article(key, value_dict):
    mongo = ''
    mongo = pymongo.Connection(HOST, PORT)
    db = mongo[DB]
    if key and value_dict:
        db.articles.update({'key':key}, value_dict, upsert=True)
    if mongo:
        mongo.close()

