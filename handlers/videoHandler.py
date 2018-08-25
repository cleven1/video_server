# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import json
import logging
from baseHandler import BaseHandler
from utils.contants import *
from utils.response_code import RET
from utils.common import requife_logined
from bson.objectid import ObjectId
from Tools.MongoDBTool import MongoTool

# 列表数据
class VideoInfoHandler(BaseHandler):

    @requife_logined
    def get(self):

        offset_id = self.get_argument('id','0')
        ispullup = int(self.get_argument('ispullup','0').encode('utf-8'))
        video_category = int(self.get_argument('category','0').encode("utf-8"))
        limit_count = int(self.get_argument('limit_count','20').encode('utf-8'))

        # 创建数据库工具类
        mongo = MongoTool(self.db)

        # 返回查询结果
        result = mongo.get_video_list(offset_id,video_category,ispullup,limit_count)

        if result == -1:
            return self.write(dict(errno=RET.DBERR, errmsg='db error'))
        else:
            self.write(dict(error_code=RET.OK, error_msg='ok', data=result))


# 添加收藏
class AddVideoCollectHandler(BaseHandler):

    @requife_logined
    def post(self):
        user_id = self.session.data['user_id']
        video_id = self.json_args('video_id','0')


        if video_id == '0':
            return self.write(dict(error_code=RET.DATAERR,error_msg='video id error'))

        # 创建数据库工具类
        mongo = MongoTool(self.db)

        # 返回查询结果
        result = mongo.add_collect_data(video_id,user_id)

        if result == -1:
            return self.write(dict(error_code=RET.DBERR, error_msg='db error'))
        else:
            self.write(dict(error_code=RET.OK, error_msg='ok'))



# 取消收藏
class cancelMyCollectVideoHandler(BaseHandler):

    @requife_logined
    def post(self):

        user_id = self.session.data['user_id']
        video_id = self.json_args.get('video_id')

        if not video_id:
            return self.write(dict(error_code=RET.PARAMERR,error_msg='video_id empty'))

        # 创建数据库工具类
        mongo = MongoTool(self.db)

        # 返回查询结果
        result = mongo.delete_collect_data(video_id,user_id)

        if result == -1:
            return self.write(dict(error_code=RET.DBERR, error_msg='db error'))
        else:
            self.write(dict(error_code=RET.OK, error_msg='ok'))



# 获取我的收藏
class MyCollectVideoHandler(BaseHandler):

    @requife_logined
    def get(self):

        user_id = self.session.data['user_id']
        offset_id = self.get_argument('id', '0')
        ispullup = int(self.get_argument('ispullup', '0').encode('utf-8'))
        limit_count = int(self.get_argument('limit_count', '20').encode('utf-8'))

        # 创建数据库工具类
        mongo = MongoTool(self.db)

        # 返回查询结果
        result = mongo.get_collect_list(user_id,offset_id,limit_count,ispullup)

        if result == -1:
            return self.write(dict(error_code=RET.DBERR, error_msg='db error'))
        else:
            self.write(dict(error_code=RET.OK, error_msg='ok', data=result))


# 添加我看过的数据
class add_look_video(BaseHandler):

    @requife_logined
    def post(self):

        user_id = self.session.data["user_id"]
        video_id = self.json_args.get('video_id')

        mongo = MongoTool(self.db)

        result = mongo.add_look_video(user_id,video_id)

        if result == -1:
            return self.write(dict(error_code=RET.DBERR, error_msg='db error'))
        else:
            self.write(dict(error_code=RET.OK, error_msg='ok'))

# 获取我看过的数据
class get_look_video(BaseHandler):

    @requife_logined
    def get(self):

        user_id = self.session.data['user_id']
        offset_id = self.get_argument('id', '0')
        ispullup = int(self.get_argument('ispullup', '0').encode('utf-8'))
        limit_count = int(self.get_argument('limit_count', '20').encode('utf-8'))

        mongo = MongoTool(self.db)

        result = mongo.get_look_video(user_id,offset_id,ispullup,limit_count)

        if result == -1:
            return self.write(dict(error_code=RET.DBERR, error_msg='db error'))
        else:
            self.write(dict(error_code=RET.OK, error_msg='ok', data=result))
