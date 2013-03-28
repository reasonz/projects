#encoding=utf-8
__author__ = 'reason'
from lib.bottle import template,Bottle,request
from dbsetting import dbsetting as db
import sys
from setting import    SITE_DOMAIN
reload(sys)
sys.setdefaultencoding('utf-8')
app = Bottle()



@app.route('/home')
def index():
    return template('index',dict(domain=SITE_DOMAIN))

