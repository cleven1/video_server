# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-

from CCPRestSDK import REST
import ConfigParser

# ���ʺ�
accountSid = '8aaf070855b647ab0155be20ca750b23';

# ���ʺ�Token
accountToken = '15439173a31d410c955401e5042bdb79';

# Ӧ��Id
appId = '8aaf070855b647ab0155be20cae50b29';

# �����ַ����ʽ���£�����Ҫдhttp://
serverIP = 'app.cloopen.com';

# ����˿�
serverPort = '8883';

# REST�汾��
softVersion = '2013-12-26';


class _CCP(object):
    def __init__(self):
        # ��ʼ��REST SDK
        self.rest = REST(serverIP, serverPort, softVersion)
        self.rest.setAccount(accountSid, accountToken)
        self.rest.setAppId(appId)

    # ������������
    @classmethod
    def instance(cls):
        if not hasattr(cls,'_instacne'):
            cls._instance = cls()
        return cls._instance

    def sendTemplateSMS(self,to,datas,tempId):
        return self.rest.sendTemplateSMS(to,datas,tempId)


ccp = _CCP()
if __name__ == '__main__':
   #  ����1��Ҫ���͵��ֻ���
   # ����2�����͵���֤�����Ч��ʱ��
   # ����3��ʹ�õ�ģ��
   ccp.sendTemplateSMS('18909565563',['1234',3],1)
