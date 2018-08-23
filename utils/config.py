# coding=utf-8

import os

# application配置
setting = {
    'debug': True,
    'cookie_secret':'heihei',
    'xsrf_cookies':False,
}

# mongodb
mongo_options = dict(
    host='127.0.0.1',
    port=27017
)

# redis
redis_options = dict(
    host='127.0.0.1',
    port=6379
)

log_level = 'debug'
log_file = os.path.join(os.path.dirname(__file__),'logs/log')