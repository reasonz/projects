#-*- coding:utf-8 -*-
__author__ = 'hpwang'
from lib.bottle import template,Bottle,request,view,response,redirect
from lib.cachewrap import cache
import sys,hashlib,datetime,utils,string
reload(sys)
sys.setdefaultencoding('utf-8')
from dbsetting import dbsetting as db
from setting import    SITE_DOMAIN,SECRET_KEY,VREYCODE,UID
app = Bottle()

@app.route("/<id:int>")
@view('home')
def myhome(id):
    print "id is ",id
    return dict(domain=SITE_DOMAIN)