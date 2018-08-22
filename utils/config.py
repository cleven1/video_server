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
    host='47.74.178.206',
    port=27017
)

# redis
redis_options = dict(
    host='47.74.178.20',
    port=6379
)

log_level = 'debug'
log_file = os.path.join(os.path.dirname(__file__),'logs/log')