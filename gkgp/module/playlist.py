#encoding=utf-8
__author__ = 'wanghp'
from lib.bottle import template,Bottle,request
import sys,hashlib,json,urllib,urllib2
from dbsetting import dbsetting as db
from setting import    SITE_DOMAIN,SECRET_KEY
reload(sys)
sys.setdefaultencoding('utf-8')
app = Bottle()


@app.route("/playlist")
def playlist():
    plscodes = getPlayCodeFromCookie()
    return plscodes


@app.route('/cn')
def mycn():
    title='中文'
    url='http://home.reasonzz.net:8888/test?'
    title = title.decode('utf-8')#.encode('GBK')
    param={"title":title}
    
    data = urllib.urlencode(param)
    print "url=",url+data
    res = urllib2.urlopen(url+data)

    #t = json.load(res,encoding='utf-8')
    print res
    return 'ok'

@app.route('/cnn')
def postcn():
    app='wlapp'
    ts='1364353099'
    sn = '231231332'
    addurl='http://vos.app.intra.tudou.com/vos/video!space'
    params={'app':app,'ts':ts,'sn':sn}
    data = urllib.urlencode(params)
    req = urllib2.Request(addurl)
    req.add_header("Content-Type","application/x-www-form-urlencoded")
    #req.add_header("Connection","keep-alive")
    #req.add_header("User-Agent","tudou")
    #req.add_header("refere","http://www.tudou.com/")
    handler=urllib2.HTTPHandler(debuglevel=1)
    opener = urllib2.build_opener(handler)
    res = opener.open(req,data)
    t= eval(res.read())
    print t 
    return t

def getPlayCodeFromCookie():
    return request.get_cookie("playlist", secret=SECRET_KEY)

