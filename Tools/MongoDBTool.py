#coding=utf-8
import uuid
import logging
from bson.objectid import ObjectId
from utils.common import requife_logined

class MongoTool:

    def __init__(self,db):
        # 切换到指定数据库
        self.db = db.XVideo

    # 创建video数据
    def create_video_data(self,video):
        data = {
            'title': video['video_title'],
            'imageUrl': video['video_image'],
            'category': video['category'],
            'videoUrl': video['video_url'],
            'size': video['video_size'],
            'duration': video['video_duration'],
            'id': str(video['_id']),
        }
        print '创建数据'
        print video['video_title']
        return data


    def get_video_list(self,offset_id,category,ispullup,limit_count):
        '''获取视频列表数据'''

        try:
            # 获取集合
            collection = self.db.video

            if offset_id == '0':
                cursor = collection.find({"category":category}).limit(limit_count)
            elif ispullup == 1: # 上拉
                cursor = collection.find({'_id': {'$gt': ObjectId(offset_id)},'category':category}).limit(limit_count)
            else: # 下拉
                cursor = collection.find({'_id': {'$lt': ObjectId(offset_id)},'category':category}).limit(limit_count)

        except Exception as e:
            logging.error(e)
            return -1

        video_list = []
        for r in cursor:
            print '==='
            print r['video_title']
            data = self.create_video_data(r)
            video_list.append(data)

        # print len(video_list)
        return video_list

    # 添加收藏
    def add_collect_data(self,video_id,user_id):
        '''添加收藏数据'''

        # 切换到指定集合
        collect = self.db.collect

        data = {
            "video_id":video_id,
            "user_id":user_id,
            "id":str(uuid.uuid4())
        }
        try:
            collect.insert_one(data)
        except Exception as e:
            logging.error(e)
            print '插入失败'
            return -1

        return 0

    def delete_collect_data(self,video_id,user_id):
        '''删除收藏数据'''

        collect = self.db.collect

        try:
            collect.delete_one({'video_id': video_id,'user_id':user_id})
        except Exception as e:
            logging.error(e)
            print "更新收藏数据错误"
            return -1

        return 0

    def get_collect_list(self,user_id,offset_id,limit_count,ispullup):
        '''获取收藏数据'''
        collect = self.db.collect

        try:

            if offset_id == '0':
                cursor = collect.find({"user_id": user_id}).limit(limit_count)
            elif ispullup == 1: # 上拉
                cursor = collect.find({'_id': {'$gt': ObjectId(offset_id)}, 'user_id': user_id}).limit(
                limit_count)
            else:  # 下拉
                cursor = collect.find({'_id': {'$lt': ObjectId(offset_id)}, 'user_id': user_id}).limit(
                limit_count)

        except Exception as e:
            logging.error(e)
            return -1

        video_list = []
        for r in cursor:
            video_id = r['video_id']
            try:
                video_collect = self.db.video
                video = video_collect.findOne({'video_id':video_id})
            except Exception as e:
                logging.error(e)
                return -1

            data = self.create_video_data(video)
            video_list.append(data)

        return video_list


    def add_look_video(self,user_id,video_id):
        '''添加我看过的数据'''

        # 切换到指定集合
        collect = self.db.look_video

        data = {
            "video_id": video_id,
            "user_id": user_id,
            "id": str(uuid.uuid4())
        }
        try:
            collect.insert_one(data)
        except Exception as e:
            logging.error(e)
            print '插入失败'
            return -1

        return 0


    def get_look_video(self,user_id,offset_id,ispullup,limit_count):
        '''获取我看过的内容'''

        collect = self.db.look_video

        try:
            if offset_id == '0':
                cursor = collect.find({"user_id": user_id}).limit(limit_count)
            elif ispullup == 1:  # 上拉
                cursor = collect.find({'_id': {'$gt': ObjectId(offset_id)}, 'user_id': user_id}).limit(
                    limit_count)
            else:  # 下拉
                cursor = collect.find({'_id': {'$lt': ObjectId(offset_id)}, 'user_id': user_id}).limit(
                    limit_count)

        except Exception as e:
            logging.error(e)
            return -1

        video_list = []
        for r in cursor:
            video_id = r['video_id']
            try:
                video_collect = self.db.video
                video = video_collect.findOne({'video_id': video_id})
            except Exception as e:
                logging.error(e)
                return -1

            data = self.create_video_data(video)
            video_list.append(data)

        return video_list
