#coding=utf-8
import uuid
import time
import logging
import random
from bson.objectid import ObjectId
from utils.common import requife_logined
from utils.session import Session

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

    # 生产6-8位用户id
    def generate_gid(self):
        gids = []
        for number in range(100000, 10000000):
            gids.append(number)
        for gid in gids:
            index0 = random.randint(0, len(gids) - 1)
            index1 = len(gids) - 1
            tmp = gids[index0]
            gids[index0] = gids[index1]
            gids[index1] = tmp
        return gids.pop()

    def user_register(self,user_name,user_mobile,user_pwd,user_avatar,user_gender):
        '''用户注册'''
        user_collection = self.db.user

        # 查询手机号有没有注册过
        try:
            cursor = user_collection.findOne({'user_mobile':user_mobile})
        except Exception as e:
            logging.error(e)

        # 判断手机号是否已经注册过
        if cursor['user_mobile']:
            return 1

        # 没有注册,插入数据
        data = {
            "user_name": user_name,
            "user_mobile": user_mobile,
            "user_pwd":user_pwd,
            "user_avatar":user_avatar,
            "user_gender":user_gender, # 0：女 1：男
            "id": str(self.generate_gid()),
            "register_time":str(time.time())
        }

        try:
            user_collection.insert_one(data)
        except Exception as e:
            logging.error(e)
            print '插入失败'
            return -1

        return data


    def user_login(self,user_mobile,user_pwd):
        '''用户登录'''
        user_collection = self.db.user

        try:
            cursor = user_collection.findOne({"user_mobile":user_mobile,"user_pwd":user_pwd})
        except Exception as e:
            logging.error(e)
            return -1

        data = {
            "name": cursor['user_name'],
            "mobile": cursor['user_mobile'],
            "password": cursor['user_pwd'],
            "avatarUrl": cursor['user_avatar'],
            "gender": cursor['user_gender'],  # 0：女 1：男
            "id": cursor['id']
        }
        return data



