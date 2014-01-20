#!/usr/bin/python
#encoding=utf-8

import web
import os
import time
import uuid
import base64
import urllib2
from PIL import Image
from  web.net  import  htmlquote

from fwrite.template import template_render
from fwrite.config import read_config,write_config
from fwrite.db import *

PATH = os.path.join(os.path.dirname(__file__), '../templates', 'admin')
UPLOAD_PATH = 'static/upload/' 

def wite_file(data, suffix):
    '''
    上传文件公共写函数
    '''
    file_name = str(uuid.uuid1())
    subfolder = time.strftime("%Y%m")
    if not os.path.exists(UPLOAD_PATH + subfolder):
        os.makedirs(UPLOAD_PATH + subfolder)
    path = str(subfolder + '/' + file_name + '.' + suffix)
    phisy_path = UPLOAD_PATH + path
    f = open(phisy_path, 'w')
    f.write(data)
    f.close()
    return phisy_path

def myuploadfile(file_obj, pic_title, s_file_name, file_type=''):
    '''
    文件上传公共处理函数
    '''
    file_path = file_obj.filename.replace('\\','/')
    source_file_name = file_path.split('/')[-1]
    suffix = source_file_name.split('.')[-1] 
    if suffix.lower() in ('jpg', 'jpeg', 'bmp', 'gif', 'png',"rar" ,"doc" ,"docx","zip","pdf","txt","swf","wmv"):
        phisy_path = wite_file(file_obj.file.read(), suffix)
        if file_type == 'pic' and suffix.lower() in ('jpg', 'jpeg', 'bmp', 'gif', 'png'):
            im = Image.open(phisy_path)
            im.thumbnail((720, 720))
            im.save(phisy_path) 
        real_url = '/' + phisy_path
        myresponse = "{'original':'%s','url':'%s','title':'%s','state':'%s'}" % (s_file_name, real_url, pic_title , 'SUCCESS')
        return myresponse

def listdir(path, file_list):
    '''
    递归所有图片文件信息 
    '''
    if os.path.isfile(path):
        return '[]' 
    allFiles=os.listdir(path)
    retlist=[]
    for cfile in allFiles:
        fileinfo={}
        filepath=(path+os.path.sep+cfile).replace("\\","/").replace('//','/')        
        
        if os.path.isdir(filepath):
            listdir(filepath,file_list)
        else:
            if cfile.endswith('.gif') or cfile.endswith('.png') or cfile.endswith('.jpg') or cfile.endswith('.bmp'):
                file_list.append(('/'+filepath).replace("//","/"))

class upload_img:
    def POST(self):
        data = web.input(upfile={}, _unicode=False)
        pic_title = data.get('pictitle', '')
        s_file_name = data.get('fileName', '')
        myresponse = myuploadfile(data.upfile, pic_title, s_file_name, 'pic')
        return myresponse

class upload_scraw:
    def POST(self):
        data = web.input(upfile={}, _unicode=False)
        param = data.get("action",'')
        if  param=='tmpImg':
            pic_title = data.get('pictitle', '')
            s_file_name = data.get('fileName', '')
            myresponse = myuploadfile(data.upfile, pic_title, s_file_name, 'pic')
            print myresponse
            myresponsedict = eval(myresponse)
            url = myresponsedict.get('url','')
            return "<script>parent.ue_callback('%s','%s')</script>" %(url,'SUCCESS') 
        else:
            base64_data = data.get('content', '')
            file_data = base64.decodestring(base64_data)
            phisy_path = wite_file(file_data, 'png')
            return "{'url':'%s',state:'%s'}" % ('/'+phisy_path,'SUCCESS')

class upload_file:
    def POST(self):
        data = web.input(upfile={}, _unicode=False)
        pic_title = data.get('pictitle', '')
        s_file_name = data.get('fileName', '')
        myresponse = myuploadfile(data.upfile, pic_title, s_file_name, 'file')
        return myresponse

class image_manager:
    def POST(self):
        file_list=[]
        listdir(UPLOAD_PATH, file_list)
        img_str="ue_separate_ue".join(file_list)
        return img_str

class get_movie:
    def POST(self):
        content ="";   
        data = web.input()
        search_key = data.get("searchKey");
        video_type = data.get("videoType");
        try:        
            url = "http://api.tudou.com/v3/gw?method=item.search&appKey=myKey&format=json&kw="+ search_key+"&pageNo=1&pageSize=20&channelId="+video_type+"&inDays=7&media=v&sort=s";
            content=urllib2.urlopen(url).read()
        except Exception,e:
            pass
        return content 

class get_remote_image:
    def POST(self):
        data  = web.input()
        urls = str(data.get('upfile'));
        url_list = urls.split('ue_separate_ue')
        out_list = []
        file_type = ['gif' , 'png' , 'jpg' , 'jpeg' , 'bmp']
        for url in url_list:
            suffix = url.split('.')[-1]
            if suffix in file_type:
                pic_data = urllib2.urlopen(url).read()
                phisy_path = wite_file(pic_data, suffix)
                out_list.append('/' + phisy_path)
        out_list='ue_separate_ue'.join(out_list)
        return "{'url':'%s','tip':'%s','srcUrl':'%s'}" % (out_list,'成功',urls)



