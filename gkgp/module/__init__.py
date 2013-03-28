__author__ = 'reason'
from lib.bottle import Bottle,TEMPLATE_PATH
import main,user,code,upload,setting,play,vlist,playlist,home
import logging
# import redis
from setting import project_path

TEMPLATE_PATH.insert(0,setting.TEM_PATH)

app=Bottle()

# init path
app.mount("/main",main.app)
app.mount("/code",code.app)
app.mount("/user",user.app)
app.mount("/upload",upload.app)
app.mount("/programs",play.app)
app.mount("/list",vlist.app)
app.mount("/zh",playlist.app)
app.mount("/home",home.app)


# init log config
log_file = project_path + "/log/gkgp.log" 
logging.basicConfig(filename = log_file, level = logging.DEBUG,format = '%(asctime)s - %(levelname)s: %(message)s') 

