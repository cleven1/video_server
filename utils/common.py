# coding=utf-8

import time
import functools
from utils.response_code import RET

# 装饰器,判断用户有没有登录
def requife_logined(func):

    # @functools.wraps 可以保证装饰器不会对被装饰函数造成影响
    @functools.wraps(func)
    def wrapper(request_handler_obj,*args,**kwargs):

        #根据get_current_user方法进行判断，如果返回不是空字典，证明用户已经登录
        if request_handler_obj.get_current_user():

            func(request_handler_obj,*args,**kwargs)

        else: #用户未登录,没有保存用户的session数据

            return request_handler_obj.write(dict(error=RET.SESSIONERR,errmsg='用户未登录'))


    return wrapper

# 获取时间戳
def get_time_stamp(self):
    times = str(time.time()).split('.')
    time_stamp = ''.join(times)
    return time_stamp