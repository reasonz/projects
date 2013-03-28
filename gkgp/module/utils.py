#-*-coding:utf-8 -*-
from dbsetting import dbsetting as db
from lib.bottle import template,Bottle,request,response
import sys,hashlib,re
from setting import    SITE_DOMAIN,SECRET_KEY,VREYCODE,UID
reload(sys)
from lib.cachewrap import cache_const,update_cache
sys.setdefaultencoding('utf-8')


def getallchannel():
    sql = "select id,name from HNSJ_TDCMS_CHANNEL"
    return db.query_list(sql,())


def getallmenu():
    sql = "select id,menuname from HNSJ_TDCMS_MENU where parent=-1"
    return db.query_list(sql,())


def getchannelnamebyid(id):
    sql = "select name from HNSJ_TDCMS_CHANNEL where id = %s"
    return db.query_one(sql,(id))[0]

def getallcpid():
    sql = "select SPID,SPNAME from HNSJ_VAC_SPINFO"
    l= db.query_list(sql,())
    d={}
    for o in l:
        d[str(o[0])]=o[1]
    return d

def update_cache():
    key=['getallchannel','getallmenu','getallcpid']
    for o in key:
        update_cache('cache'+o)

#MD5
def dest(password):
    m = hashlib.md5(password)
    return m.hexdigest()

#邮箱合法性验证
def ProcessMail(inputMail):
    isMatch = bool(re.match(r"^[a-zA-Z0-9](([a-zA-Z0-9]*\.[a-zA-Z0-9]*)|[a-zA-Z0-9]*)[a-zA-Z0-9]@([a-z0-9A-Z]+\.)+[a-zA-Z]{2,}$", inputMail,re.VERBOSE));
    return isMatch


def set_cookie(name,value):
    response.set_cookie(name,value,secret=SECRET_KEY,path='/',max_age=30*24*60*60)

def get_cookie(name):
    return request.get_cookie(name, secret=SECRET_KEY)


def has_hz(text):
    hz_yes = False
    for ch in text:
        if isinstance(ch, unicode):
            if unicodedata.east_asian_width(ch)!= 'Na':
                hz_yes = True
                break
            else:
                continue
    return hz_yes

if __name__ == '__main__':
    print has_hz('666666')