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

# 列表数据
class VideoInfoHandler(BaseHandler):

    def get(self):

        offset_id = self.get_argument('id','0')
        ispullup = int(self.get_argument('ispullup',0).encode('utf-8'))
        video_category = int(self.get_argument('category',0).encode("utf-8"))
	limit_count = int(self.get_argument('limit_count',20).encode('utf-8'))
	print '查看参数' 
	print offset_id
	print type(offset_id)
	print ispullup
	print type(ispullup)

        try:
            # 切换到指定数据库
            db = self.db.XVideo

            # 获取集合
            collection = db.video

            if offset_id == '0':
                cursor = collection.find({"category":video_category}).limit(limit_count)
		print '加载数据'
            elif ispullup == 1: # 上拉
                cursor = collection.find({'_id': {'$gt': ObjectId(offset_id)},'category':video_category}).limit(limit_count)
            else: # 下拉
                cursor = collection.find({'_id': {'$lt': ObjectId(offset_id)},'category':video_category}).limit(limit_count)

        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg='dbError'))


        video_list = []
        for r in cursor:
            data = {
                'title': r['video_title'],
                'imageUrl': r['video_image'],
                'category': r['category'],
                'videoUrl': r['video_url'],
                'size': r['video_size'],
                'duration': r['video_duration'],
                'id': str(r['_id']),
            }
            video_list.append(data)

        self.write(dict(errno=RET.OK, errmsg='ok', data=video_list))


# 添加收藏
class AddVideoCollectHandler(BaseHandler):

    @requife_logined
    def get(self):
        user_id = self.session.data['user_id']



# 获取我的收藏
class MyCollectVideoHandler(BaseHandler):

    @requife_logined
    def get(self):

        user_id = self.session.data['user_id']
