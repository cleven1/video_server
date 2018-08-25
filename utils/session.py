# coding=utf-8

import uuid
import logging
import json
from contants import *

class Session(object):

    def __init__(self,request_handler):

        self.request_handler = request_handler

        # 获取sessionid
        self.session_id = self.request_handler.get_secure_cookie('session_id')

        if not self.session_id:
            # 用户第一次访问
            # 生成session——id
            print '生成session id'
            self.session_id = uuid.uuid4().get_hex()
            self.data = {}

        else:
            # 在redis中获取session_id
            try:
                data = request_handler.redis.get('sess_%s'%self.session_id)

            except Exception as e:
                logging.error(e)
                self.data = {}

            if not data:
                self.data = {}
            else:
                # 反序列化
                self.data = json.loads(data)


    # 登录  保存数据
    def save(self):
        # 进行序列化
        json_data = json.dumps(self.data)

        try:
            # 把json_data 存入redis中
            self.request_handler.redis.set('sess_%s'%self.session_id,json_data,SESSION_EXPIRES_SECONDS)

        except Exception as e:
            logging.error(e)
            print '保存redis 失败'
            raise Exception('save session failed')
        else:
            self.request_handler.set_secure_cookie('session_id',self.session_id)


    # 用户退出登陆，清除数据
    def clear(self):
        self.request_handler.clear_cookie('session_id')
        try:
            # 在redis中删除session_id
            self.request_handler.redis.delete('sess_%s',self.session_id)

        except Exception as e:
            logging.error(e)


