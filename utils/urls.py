import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from handlers import passPort
from handlers import verifyCode
from handlers import videoHandler

handlers = [
    # (r'/',passPort.IndexHandler),
    (r'/api/smscode',verifyCode.smsCodeHandler),
    (r'/api/register',passPort.RegisterHandler),
    (r'/api/login',passPort.LoginHandler),
    (r'/api/checkloginstatus',passPort.CheckLoginHandler),
    (r'/api/video/info', videoHandler.VideoInfoHandler),
    (r'/api/video/collect', videoHandler.MyCollectVideoHandler),

]
