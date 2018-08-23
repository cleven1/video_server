# coding=utf-8

import logging
import hashlib
import os
from Tools.MongoDBTool import MongoTool

from utils.response_code import RET
from utils.contants import *
from baseHandler import BaseHandler
from utils.session import Session


class IndexHandler(BaseHandler):
    def get(self):

        logging.debug('debug msg')
        logging.warning('warning msg')
        logging.info('info msg')
        logging.error('error msg')
        print 'print msg'

        # self.write('hello cleven')


# 注册
class RegisterHandler(BaseHandler):

    def post(self):

        name = self.json_args.get('name')
        avatar = self.json_args.get('avatar')
        gender = int(self.json_args.get('gender','1').encode('utf-8'))
        mobile = self.json_args.get('mobile')
        sms_code = self.json_args.get('sms_code')
        password = self.json_args.get('pwd')

        if not all([mobile,sms_code,password]):
            return self.write(dict(error=RET.PARAMERR,errmsg='参数错误'))
        try:
            real_code = self.redis.get('sms_code_%s' % mobile)
        except Exception as e:
            logging.error(e)
            
        if real_code != str(sms_code):
            return self.write(dict(errno=RET.VERIFYERR,errmsg='验证码错误'))

        # 密码加密
        password = hashlib.sha256(PASS_WORD_HASH_KEY + password).hexdigest()

        mongo = MongoTool(self.db)

        result = mongo.user_register(name,mobile,password,avatar,gender)

        # 保存到session中
        try:
            self.session = Session(self)
            self.session.data['user_id'] = result['id']
            self.session.data['user_name'] = result['user_name']
            self.session.data['user_mobile'] = result['user_mobile']
            self.session.data['user_pwd'] = result['user_pwd']
            self.session.data['user_avatar'] = result['user_avatar']
            self.session.data['user_gender'] = result['user_gender']
            self.session.save()
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.SESSIONERR,errmsg='保存session 错误'))

        #-1 注册失败 1：手机号已经注册 0 注册成功
        if result == -1:
            return self.write(dict(errno=RET.DBERR,errmsg='注册失败'))
        elif result == 1:
            return self.write(dict(errno=RET.DATAEXIST,errmsg='手机号已经被注册'))
        else:
            self.write(dict(errno=RET.OK,errmsg='ok'))


#  登录
class LoginHandler(BaseHandler):

    def post(self):

        mobile = self.json_args.get('mobile')
        password = self.json_args.get('pwd')

        if not all([mobile,password]):
            return self.write(dict(RET.PARAMERR,errmsg='参数错误'))

        # 加密密码
        password = hashlib.sha256(PASS_WORD_HASH_KEY + password).hexdigest

        mongo = MongoTool(self.db)

        result = mongo.user_login(mobile,password)

        if result == -1:
            return self.write(dict(error=RET.PARAMERR, errmsg='手机号或密码错误'))
        else:
            # 保存到session中
            try:
                self.session = Session(self)
                self.session.data['user_id'] = result['id']
                self.session.data['user_name'] = result['user_name']
                self.session.data['user_mobile'] = result['user_mobile']
                self.session.data['user_pwd'] = result['user_pwd']
                self.session.data['user_avatar'] = result['user_avatar']
                self.session.data['user_gender'] = result['user_gender']
                self.session.save()
            except Exception as e:
                logging.error(e)
                return self.write(dict(errno=RET.SESSIONERR, errmsg='保存session 错误'))

            return self.write(dict(error=RET.OK, errmsg='ok'))


# 检查用户登录状态
class CheckLoginHandler(BaseHandler):

    def get(self):

        # 判断是否是登录状态
        if self.get_current_user():
            self.write(dict(error=RET.OK,errmsg='true',data={'name':self.session.data['name']}))

        else:
            self.write(dict(error=RET.SESSIONERR,errmsg='false'))