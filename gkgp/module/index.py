#encoding=utf-8
__author__ = 'reason'
from lib.bottle import template,Bottle,request
from lib.cachewrap import cache
import sys,hashlib
from setting import    SITE_DOMAIN
reload(sys)
sys.setdefaultencoding('utf-8')
app = Bottle()


@app.route('/main')
def route():
    l=[]
    for i in range(1,100):
        l.append(i)

    return template('index',dict(domain=SITE_DOMAIN,tlist=l))

@app.post('/login')
def report():
    username = request.forms.get('username')
    password =  request.forms.get('password')
    return template('welcome',dict(username=username,domain=SITE_DOMAIN))

@app.route('/test')
def test():
    request_uri =  str(request.environ.get('PATH_INFO'))+"?"+ str(request.environ.get('QUERY_STRING'))
    domain=  str(request.environ.get('HTTP_HOST'))
    print "request_uri is ",request_uri
    print "domain is ",domain
    return 'test'

@app.route('/index')
def index():
    return template("index",dict(domain=SITE_DOMAIN))

import json
@app.route('/testjson')
def testjson():
    l=['a','b','c']
    return json.dumps(l)

