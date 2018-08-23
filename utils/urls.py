import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from handlers import passPort
from handlers import verifyCode
from handlers import videoHandler

handlers = [
    # (r'/',passPort.IndexHandler),
    (r'/api/user/smscode',verifyCode.smsCodeHandler),
    (r'/api/user/register',passPort.RegisterHandler),
    (r'/api/user/login',passPort.LoginHandler),
    (r'/api/user/checkloginstatus',passPort.CheckLoginHandler),
    (r'/api/video/info', videoHandler.VideoInfoHandler),
    (r'/api/video/addCollect',videoHandler.AddVideoCollectHandler),
    (r'/api/video/cancelCollect',videoHandler.cancelMyCollectVideoHandler),
    (r'/api/video/collect', videoHandler.MyCollectVideoHandler),
    (r'/api/video/addLook',videoHandler.add_look_video),
    (r'/api/video/look',videoHandler.get_look_video),

]
