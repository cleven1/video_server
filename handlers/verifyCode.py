# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import logging
import re

from utils.contants import *
from baseHandler import BaseHandler
from utils.response_code import RET
from libs.yuntongxun.CCP import ccp

#导入random模块
import random
#导入Image,ImageDraw,ImageFont模块
from PIL import Image,ImageDraw,ImageFont


# 短信验证码
class smsCodeHandler(BaseHandler):

    def post(self):
        # 获取参数
        # mobile = self.json_args.get('mobile')
        # print mobile
        mobile = self.get_argument('mobile')
        print mobile
        # 判断有没有值
        if not any(mobile):
            print "mobile is empty"
            return self.write(dict(error_code=RET.PARAMERR,error_msg='参数不完整'))

        # 判断手机号格式
        if len(mobile) != 11:
            return self.write(dict(error_code=RET.PARAMERR,error_msg='手机号错误'))

        if not re.match(r'^1[3|4|5|7|8][0-9]\d{4,8}$',mobile):
            return self.write(dict(error_code=RET.PARAMERR,error_msg='手机号格式错误'))


        print "-"*40

        # 生产随机短信验证码
        sms_code = '%04d' % random.randint(0,9999)

        # 把生成的验证码code存入redis
        try:
            self.redis.set('sms_code_%s'%mobile,sms_code,SMS_CODE_EXPRIES_SECONDS * 60)
        except Exception as e:
            logging.error(e)
            return self.write(dict(error_code=RET.DBERR, error_msg='生产短信验证码错误'))

        # 发送短信
        try:
            ccp.sendTemplateSMS(mobile,[sms_code,SMS_CODE_EXPRIES_SECONDS],1)
        except Exception as e:
            logging.error(e)
            return self.write(dict(error_code=RET.THIRDERR, error_msg='发送短信验证码失败'))

        # 返回成功
        self.write(dict(error_code=RET.OK,error_msg='ok'))

