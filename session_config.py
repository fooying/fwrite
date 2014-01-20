#!/usr/bin/env python
#encoding=utf-8
#by Fooying 2013-11-24 21:33:04

session = {}
session['cookie_name'] = 'fwrite'
session['cookie_domain'] = None
session['timeout'] = 7200, #24 * 60 * 60, # 24 hours   in seconds
session['ignore_expiry'] = False
session['ignore_change_ip'] = True
session['secret_key'] = '2dcab869e0c789b87cb4f9549bf7dbf4'
session['expired_message'] = '登陆已过期'
