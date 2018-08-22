# coding=utf-8

import logging
import hashlib
import os

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
            return self.write(dict(errno=2,errmsg='验证码错误'))

        # 密码加密
        password = hashlib.sha256(PASS_WORD_HASH_KEY + password).hexdigest()

        try:
            # sql =

            res = self.db.execute('insert into cl_user_profile(up_name,up_mobile,up_password) '
                                  'values(%(name)s,%(mobile)s,%(password)s)',
                                  name=mobile,mobile=mobile,password=password)

        except Exception as e:
            logging.error(e)
            return self.write(dict(error=RET.DATAEXIST,errmsg='手机号已注册'))

        try:
            self.session = Session(self)
            self.session.data['user_id'] = res
            self.session.data['name'] = mobile
            self.session.data['mobile'] = mobile
            self.session.save()
        except Exception as e:
            logging.error(e)

        self.write(dict(error=RET.OK,errmsg='ok'))


#  登录
class LoginHandler(BaseHandler):

    def post(self):

        mobile = self.json_args.get('mobile')
        password = self.json_args.get('pwd')

        if not all([mobile,password]):
            return self.write(dict(RET.PARAMERR,errmsg='参数错误'))

        res = None
        try:
            # select up_user_id,up_name,up_password from cl_user_profile where up_mobile=18909565563;
            res = self.db.get('select up_user_id,up_name,up_password from cl_user_profile where up_mobile=%(m)s',m=mobile)
        except Exception as e:
            logging.error(e)

        if not res:
            return self.write(dict(error=RET.PARAMERR,errmsg='手机号或密码错误'))

        password = hashlib.sha256(PASS_WORD_HASH_KEY+password).hexdigest()

        if res and res['up_password'] == unicode(password):
            try:
                self.session = Session(self)
                self.session.data['user_id'] = res['up_user_id']
                self.session.data['name'] = res['up_name']
                self.session.data['mobile'] = mobile
                self.session.save()

            except Exception as e:
                logging.error(e)

            return self.write(dict(error=RET.OK,errmsg='ok'))

        else:
            self.write(dict(error=RET.PARAMERR,errmsg='手机号或密码错误```'))


# 检查用户登录状态
class CheckLoginHandler(BaseHandler):

    def get(self):

        # 判断是否是登录状态
        if self.get_current_user():
            self.write(dict(error=RET.OK,errmsg='true',data={'name':self.session.data['name']}))

        else:
            self.write(dict(error=RET.SESSIONERR,errmsg='false'))