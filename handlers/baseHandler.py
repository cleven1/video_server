# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import json

from tornado.web import RequestHandler,StaticFileHandler
from utils.session import Session

class BaseHandler(RequestHandler):
    '''handler基类'''

    @property
    def db(self):
        return self.application.db

    @property
    def redis(self):
        return self.application.redis

    def prepare(self):
        # self.xsrf_token
        print self.request.body
        if self.request.headers.get('Content-Type','').startswith('application/json'):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = {}

    def write_error(self, status_code, **kwargs):
        pass

    def set_default_headers(self):
        self.set_header('Content-Type','application/json;charset=utf-8')

    def initialize(self):
        pass


    def on_finish(self):
        pass

    # 判断用户数据是否为真
    def get_current_user(self):
        # 存储全局session
        self.session = Session(self)
        # 有值就为真
        return self.session.data

# 配置静态文件的xsrf
class StaticFileBaseHandler(StaticFileHandler):

    def __init__(self,*args,**kwargs):
        super(StaticFileBaseHandler,self).__init__(*args,**kwargs)
        # self.xsrf_token