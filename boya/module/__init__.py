__author__ = 'reason'
from lib.bottle import Bottle,TEMPLATE_PATH
import index
import  setting

TEMPLATE_PATH.insert(0,setting.TEM_PATH)

app=Bottle()

app.mount("/index",index.app)




