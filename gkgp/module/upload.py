#-coding:utf-8-*-
#encoding=utf-8
__author__ = 'reason'
from lib.bottle import template,Bottle,request,view,response
import sys,hashlib,urllib2,urllib,json,traceback,httplib
from openapi import *
from utils import get_cookie,set_cookie
from dbsetting import dbsetting as db
from setting import SITE_DOMAIN,username,pwd,tudouuserId,addvideoinfoUrl
import logging
from user import getUidFromCookie
reload(sys)
sys.setdefaultencoding('utf-8')
app = Bottle()

host = 'http://ulpc.tudou.com/mps3/webupload'
    
@app.route('/toupload')
# @view('upload')
def route():
    # get item_type
    sql ='select id,channel_name from gkgp_channel'
    typelist = db.query_list(sql,())

    return template('upload',dict(domain=SITE_DOMAIN,typelist=typelist))

#  get upload file's itemid and upload status
@app.post('/upload2')
def up2():
    title = request.params.get('title')
    content=request.params.get('content')
    tags=request.params.get('tags')
    ipAddr =   request.environ.get('REMOTE_ADDR')
    channelId=99

    res = uploaditem(title,tags,content,channelId,ipAddr)
    return res

@app.route('/upload')
def upload():
    title = request.query.get('title')
    callback= request.query.get('callback')
    #username= 'gkgp_cmcc@163.com'
    #password='ZAQ!xsw2'
    content = title
    tags = title
    imake = 1
    channelId=99
    req = urllib2.Request(host+'?action=new')
    param = {'title':title,'tags':tags,'channelId':channelId,'imake':imake,'content':content,'user':username,'password':pwd}
    data = urllib.urlencode(param)  
    opener = urllib2.build_opener()  
    response = opener.open(req, data) 
    t= response.read()
    print t
    return callback +'('+ t + ')'
# 1.get form data
# 2.get itemcode by itemid
# 3.invoke addtime  
# @app.post('/addvideoinfo')
@app.route('/addvideoinfo')
def addvideoinfo():
    addurl =addvideoinfoUrl #'http://wwwtest.tudou.com/my/programs/service/updateItem.action?' #addvideoinfoUrl 
    itemid = request.query.get('itemid')
    title = request.query.get('title')
    comments = request.query.get('comments')
    tags = request.query.get('tags')
    videotype = request.query.get('videotype')
    queryurl = request.query.get('queryurl')
    mpsurl = request.query.get('mpsurl')
    callback = request.query.get('callback')
    # if request.get_cookie('uid'):
        # uid = request.get_cookie('uid')
    uid=getUidFromCookie()
    # else:
        # return json.dumps({'status':2,'msg':'please login first!'})
    #tudouuserId = 119029329
    title_ = title.decode('utf-8').encode('gbk')
    comments_ = comments.decode('utf-8').encode('gbk')
    tags_ = tags.decode('utf-8').encode('gbk')
    params={'itemId':itemid,'title':title_,'description':comments_,'tags':tags_,'userId':tudouuserId}

    print "title is ",title
    data = urllib.urlencode(params)
    print addurl+ data
    req = urllib2.Request(addurl)
    req.add_header("Content-Type","application/x-www-form-urlencoded;charset=gbk")
    #req.add_header("Connection","keep-alive")
    #req.add_header("User-Agent","tudou")
    #req.add_header("refere","http://www.tudou.com/")
    handler=urllib2.HTTPHandler(debuglevel=1)
    opener = urllib2.build_opener(handler)
    #opener = urllib2.build_opener() 
    res = opener.open(req,data)
    t= eval(res.read())
    #t= json.load(res.read(),encoding='gbk')
    print t 

    #if response.status==302:
    if t.get('result')=='1':
        # do add
        itemcode = id2code(itemid)
        additem(title,comments,tags,itemid,itemcode,videotype,queryurl,uid,mpsurl)
        return callback + '(' + json.dumps({'status':0,'msg':'success'}) + ')'
    else:
        # update video info error
        return callback + '(' + json.dumps({'status':1,'msg':'error'}) + ')'


# #########################################
#  insert video infomations to database
def additem(title,comments,tags,itemid,itemcode,videotype,queryurl,uid,mpsurl):
    conn = db.getmysqlconn()
    try:
        c = conn.cursor()
        sql = "insert into gkgp_item(itemid,title,description,videotype,tags,itemcode,queryurl,mpsurl) \
            values(%s,%s,%s,%s,%s,%s,%s,%s)"
        c.execute(sql,(itemid,title,comments,videotype,tags,itemcode,queryurl,mpsurl))
        videoid= conn.insert_id()
        conn.commit()
        sql = "insert into gkgp_user_item(userid,videoid) values(%s,%s)"
        c.execute(sql,(uid,videoid))

        sql = "insert into gkgp_channel_item_link (item_type,item_id,uid,channel_id) values(%s,%s,%s,%s)"
        c.execute(sql,(1,videoid,uid,videotype))
        conn.commit()
    except:
        conn.rollback()
        traceback.print_exc()
    finally:
        c.close()
        conn.close()