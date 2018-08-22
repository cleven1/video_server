# coding=utf-8

import pymongo
import redis
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define,options

from urls import handlers
from config import *

define('port',type=int,default=5000,help='run video on the given port')


class Application(tornado.web.Application):

    def __init__(self,*args,**kwargs):
        super(Application,self).__init__(*args,**kwargs)

        # 创建MongoDB
        self.db = pymongo.MongoClient(**mongo_options)

        # 创建redis
        self.redis = redis.StrictRedis(**redis_options)

def main():
    options.logging = log_level
    options.log_file_prefix = log_file
    app = Application(
        handlers,**setting
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':

    main()
