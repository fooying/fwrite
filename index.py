#coding=utf-8
'''
api主调用模块
'''
import web
import views
from url import urls
from session_config import session as session_config

web.config.debug = False
app = web.application(urls, locals())
web.config.session_parameters.update(session_config)
session = web.session.Session(app, web.session.DiskStore('sessions'))


if __name__ == "__main__":
	app.run()
else:
	application = app.wsgifunc()
