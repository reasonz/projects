#-*- coding:utf-8 -*-
__author__ = 'hpwang'
from dbsetting import dbsetting
import sys,hashlib,datetime,utils
reload(sys)
sys.setdefaultencoding('utf-8')

def getUserByUsername(username):
    sql = "select * from gkgp_user where username=%s"
    return dbsetting.query_one(sql,username)

def getUserByNickname(nickname):
    sql = "select * from gkgp_user where nickname=%s"
    return dbsetting.query_one(sql,nickname)

def getUserByNameAndPass(username,password):
    sql = "select * from gkgp_user where username=%s and password=%s";
    return dbsetting.query_one(sql,(username,password))