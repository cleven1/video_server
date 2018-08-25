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

        name = self.get_data('name')#self.json_args.get('name')
        avatar = self.get_data('avatar','http://')#self.json_args.get('avatar')
        gender = int(self.get_data('gender','1').encode('utf-8'))#int(self.json_args.get('gender','1').encode('utf-8'))
        mobile = self.get_data('mobile')#self.json_args.get('mobile')
        sms_code = self.get_data('sms_code')#self.json_args.get('sms_code')
        password = self.get_data('pwd')#self.json_args.get('pwd')
        identifier = self.get_data('identifier')#self.json_args.get('identifier')

        if not all([mobile,sms_code,password,identifier]):
            return self.write(dict(error_code=RET.PARAMERR,error_msg='参数错误'))

        try:
            real_code = self.redis.get('sms_code_%s' % mobile)
        except Exception as e:
            logging.error(e)
            
        if real_code != str(sms_code):
            return self.write(dict(error_code=RET.VERIFYERR,error_msg='验证码错误'))
        print real_code
        # 密码加密
        password = hashlib.sha256(PASS_WORD_HASH_KEY + password).hexdigest()

        mongo = MongoTool(self.db)

        result = mongo.user_register(name,mobile,password,avatar,gender,identifier)

        # -1 注册失败 1：手机号已经注册 0 注册成功
        if result == -1:
            return self.write(dict(error_code=RET.DBERR, error_msg='注册失败'))
        elif result == 1:
            return self.write(dict(error_code=RET.DATAEXIST, error_msg='手机号已经被注册'))
        else:
            # 保存到session中
            try:
                self.session = Session(self)
                self.session.data['user_id'] = result['id']
                self.session.data['user_name'] = result['user_name']
                self.session.data['user_mobile'] = result['user_mobile']
                self.session.data['user_pwd'] = result['user_pwd']
                self.session.data['user_avatar'] = result['user_avatar']
                self.session.data['user_gender'] = str(result['user_gender'])
                self.session.data['identifier'] = result['identifier']
                self.session.save()
            except Exception as e:
                print '保存session 失败'
                logging.error(e)
                try:
                    mongo.delete_user(result['id'])
                except Exception as e:
                    print '删除用户失败'
                    logging.error(e)
                return self.write(dict(error_code=RET.SESSIONERR,error_msg='保存session 错误'))

            # 注册成功
            self.write(dict(error_code=RET.OK, error_msg='ok aa'))



#  登录
class LoginHandler(BaseHandler):

    def post(self):

        mobile = self.get_data('mobile')
        password = self.get_data('pwd')
        identifier = self.get_data('identifier')

        if not all([mobile,password,identifier]):
            return self.write(dict(error_code=RET.PARAMERR, error_msg='参数错误'))

        print mobile
        print password
        # 加密密码
        password = hashlib.sha256(PASS_WORD_HASH_KEY + password).hexdigest()

        mongo = MongoTool(self.db)

        result = mongo.user_login(mobile,password)

        if result == -1:
            return self.write(dict(error_code=RET.PARAMERR, error_msg='手机号或密码错误'))
        else:
            print result
            # 保存到session中
            try:
                self.session = Session(self)
                self.session.data['user_id'] = result['id']
                self.session.data['user_name'] = result['name']
                self.session.data['user_mobile'] = mobile
                self.session.data['user_pwd'] = password
                self.session.data['user_avatar'] = result['avatarUrl']
                self.session.data['user_gender'] = str(result['gender'])
                self.session.data['identifier'] = identifier
                self.session.save()
            except Exception as e:
                logging.error(e)
                return self.write(dict(error_code=RET.SESSIONERR, error_msg='保存session 错误'))

            # 返回数据
            data = {
                'user_id':result['id'],
                'name':result['name'],
                'mobile':mobile,
                'avatar_url':result['avatarUrl'],
                'gender':result['gender']
            }

            return self.write(dict(error_code=RET.OK, error_msg='ok',data=data))


# 退出登录
class LogOffHandler(BaseHandler):

    def post(self):
        try:
            self.session = Session(self)
            self.session.clear()
        except Exception as e:
            logging.error(e)
            return self.write(dict(error_code=RET.SESSIONERR,error_msg="退出失败"))

        self.write(dict(error_code=RET.OK,error_msg="ok"))

# 检查用户登录状态
class CheckLoginHandler(BaseHandler):

    def get(self):

        # 判断是否是登录状态
        if self.get_current_user():
            self.write(dict(error_code=RET.OK,error_msg='true',data={'name':self.session.data['name']}))

        else:
            self.write(dict(error_code=RET.SESSIONERR,error_msg='false'))