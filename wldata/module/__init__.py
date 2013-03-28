__author__ = 'reason'
from lib.bottle import Bottle,TEMPLATE_PATH
import index,shunion,option ,datareport ,nokiareport,ssx,wlapi,tdwap
import  setting

TEMPLATE_PATH.insert(0,setting.TEM_PATH)

app=Bottle()
app.mount("/nokiadata",nokiareport.app)
app.mount("/data",datareport.app)
app.mount("/index",index.app)
app.mount("/shunion",shunion.app)
app.mount("/option",option.app)
app.mount("/ssx",ssx.app)
app.mount("/wlapi",wlapi.app)
app.mount("/tdwap",tdwap.app)



