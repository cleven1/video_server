# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import json
import logging
import time
from baseHandler import BaseHandler
from utils.contants import *
from utils.response_code import RET
from utils.common import requife_logined
from bson.objectid import ObjectId
from Tools.MongoDBTool import MongoTool
from utils.common import get_time_stamp

class UploadFile(BaseHandler):

    def post(self):
        # 获取当前目录的上级目录
        base_path = os.path.dirname(os.path.dirname(__file__))
        print '路径'
        print base_path
        files = self.request.files
        img_files = files.get('img') #img_files是一个列表
        print img_files
        if img_files:
            img_file = img_files[0]["body"]#取列表的第一个元素
            path = os.path.join(base_path,'static')
            path = os.path.join(path,'avatar')
            print path
            avatar_name = get_time_stamp() + '.png'
            file = open(path + '/' + avatar_name, 'w+') #以写方式打开一个文件
            file.write(img_file)
            print avatar_name
            file.close()
            self.write(dict(error_code=RET.OK,error_msg='ok',file_name=avatar_name))
        else:
            print '获取文件失败'
            self.write(dict(error_code=RET.PARAMERR,error_msg='获取文件失败'))