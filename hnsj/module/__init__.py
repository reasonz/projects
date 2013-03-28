__author__ = 'reason'
from lib.bottle import Bottle,TEMPLATE_PATH
import index,option,video,channel,notice,template
import  setting


TEMPLATE_PATH.insert(0,setting.TEM_PATH)

app=Bottle()

app.mount("/option",option.app)
app.mount("/index",index.app)
app.mount("/video",video.app)
app.mount("/channel",channel.app)
app.mount("/notice",notice.app)
app.mount("/template",template.app)
