# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-

from CCPRestSDK import REST
import ConfigParser

# 主帐号
accountSid = '8aaf070855b647ab0155be20ca750b23';

# 主帐号Token
accountToken = '15439173a31d410c955401e5042bdb79';

# 应用Id
appId = '8aaf070855b647ab0155be20cae50b29';

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com';

# 请求端口
serverPort = '8883';

# REST版本号
softVersion = '2013-12-26';


class _CCP(object):
    def __init__(self):
        # 初始化REST SDK
        self.rest = REST(serverIP, serverPort, softVersion)
        self.rest.setAccount(accountSid, accountToken)
        self.rest.setAppId(appId)

    # 创建单利方法
    @classmethod
    def instance(cls):
        if not hasattr(cls,'_instacne'):
            cls._instance = cls()
        return cls._instance

    def sendTemplateSMS(self,to,datas,tempId):
        return self.rest.sendTemplateSMS(to,datas,tempId)


ccp = _CCP()
if __name__ == '__main__':
   #  参数1：要发送的手机号
   # 参数2：发送的验证码和有效期时间
   # 参数3：使用的模板
   ccp.sendTemplateSMS('18909565563',['1234',3],1)
