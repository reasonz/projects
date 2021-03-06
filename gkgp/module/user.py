#-*- coding:utf-8 -*-
__author__ = 'hpwang'
from lib.bottle import template,Bottle,request,view,response,redirect
from lib.cachewrap import cache
import sys,hashlib,datetime,utils
from dbsetting import dbsetting
from setting import    SITE_DOMAIN,SECRET_KEY,VREYCODE,UID
import json,main

reload(sys)
sys.setdefaultencoding('utf-8')
app = Bottle()

userdata=dict(domain=SITE_DOMAIN,uerr="",nerr="",perr="",verr="",ref="")
refer = ""

@app.route("/index")
def index():
    return getUidFromCookie()

@app.route("/")
@app.route("/tologin")
@view('login')
def tologin():
    userdata=dict(domain=SITE_DOMAIN,uerr="",nerr="",perr="",verr="",ref="")
    return userdata

@app.route("/logout")
def logout(): 
    delUidFromCookie()
    return "logout"

@app.post("/login")
def login():
    userdata=dict(domain=SITE_DOMAIN,uerr="",nerr="",perr="",verr="",ref="")
    username = request.forms.get('username')
    password =  request.forms.get('password')
    ref = request.forms.get('ref')
    if(username.strip()==""):
        # userdata['uerr']="邮箱不能为空！"
        # return template('login',userdata)
        data = {"status":"0","msg":"邮箱不能为空！"}
        return json.dumps(data);

    if(not utils.ProcessMail(username)):
        # userdata['uerr']="邮箱格式不正确！"
        # return template('login',userdata)
        data = {"status":"0","msg":"邮箱格式不正确！"}
        return json.dumps(data);

    if(password.strip()==""):
        # userdata['perr']="密码不能为空！"
        # return template('login',userdata)
        data = {"status":"0","msg":"密码不能为空！"}
        return json.dumps(data);

    # varifycode = request.forms.get('varifycode')
    # sessionCode = getValInCookie(VREYCODE)

    # delValFromCookie(VREYCODE)
    # if(varifycode.strip()==""):
    #     userdata['verr']="验证码不能为空！"
    #     return template('login',userdata)

    # if(varifycode.upper()!=sessionCode.upper()):
    #     userdata['verr']="验证码输入不一致！"
    #     return template('login',userdata)

    user = getUserByNameAndPass(username,utils.dest(password))
    if(user==None):
        # userdata["uerr"]="账号不存在或账号密码错误！"
        # return template('login',userdata)
        data = {"status":"0","msg":"账号不存在或账号密码错误！"}
        return json.dumps(data);

    #response.set_cookie("UID",user[1],SECRET_KEY)
    addUidInCookie(user[0])
    data = {"status":"1","msg":"登录成功！"}
    return json.dumps(data)


@app.route("/curuser")
def curuser():
    uinfo = findCurUserInfo()
    return json.dumps(uinfo)


@app.route("/toreg")
def toReg():
    refer = request.get_header("Referer")
    userdata=dict(domain=SITE_DOMAIN,uerr="",nerr="",perr="",verr="",ref=refer)
    return template('reg',userdata)

@app.post("/reg")
def reg():
    userdata=dict(domain=SITE_DOMAIN,uerr="",nerr="",perr="",verr="",ref="")
    username = request.forms.get('username')
    password =  request.forms.get('password')
    nickname = request.forms.get('nickname')
    varifycode = request.forms.get('varifycode')
    ref = request.forms.get('ref')
    sessionCode = getValInCookie(VREYCODE)
    delValFromCookie(VREYCODE)
    if(username.strip()==""):
        userdata['uerr']="邮箱不能为空！"
        return template('reg',userdata)

    if(not utils.ProcessMail(username)):
        userdata['uerr']="邮箱格式不正确！"
        return template('reg',userdata)

    if(getUserByUsername(username)!=None):
        userdata['uerr']="该邮箱已经存在！"
        return template('reg',userdata)

    if(len(password)<4 or len(password)>20):
        userdata['perr']="密码的长度在4-20之间！"
        return template('reg',userdata)

    if(getUserByNickname(nickname)!=None):
        userdata['nerr']="昵称已经存在！"
        return template('reg',userdata)

    if(varifycode.strip()==""):
        userdata['verr']="验证码不能为空！"
        return template('reg',userdata)

    if(varifycode.upper()!=sessionCode.upper()):
        userdata['verr']="验证码输入不一致！"
        return template('reg',userdata)


    sql = '''insert into gkgp_user
    ( username,    password,
	nickname,
	create_time,
	last_login_time
	)
	values
	(%s,%s,%s,%s,%s)
    '''
    try:
        uid = dbsetting.update(sql,(username,utils.dest(password),nickname,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        print "uid is %d" % uid
        addUidInCookie(uid)
    except Exception,e:
        print e

    print "len(ref):",len(ref)
    print  "ref:",ref

    if (len(ref)>0 and SITE_DOMAIN in ref):
        return redirect(ref)
    else:
        return redirect(SITE_DOMAIN+"/main/index")

def findCurUserInfo():
    uid = getUidFromCookie()
    print "uid is ",uid
    if uid == None or uid == "":
        return None
    uinfo = getUserInfoById(uid)
    return  uinfo


def addUidInCookie(uid):
    response.set_cookie(UID,uid,secret=SECRET_KEY,path='/',max_age=30*24*60*60)

def getUidFromCookie():
    return request.get_cookie(UID, secret=SECRET_KEY)

def delUidFromCookie():
    print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    addUidInCookie(None)

def addValInCookie(name,val):
    response.set_cookie(name,val,secret=SECRET_KEY,path='/',max_age=30*24*60*60)

def getValInCookie(name):
    return request.get_cookie(name, secret=SECRET_KEY)

def delValFromCookie(name):
    addValInCookie(name,None)

def getUserInfoById(id):
    sql = "select * from gkgp_user where id=%s"
    return dbsetting.query_one(sql,id)

def getUserByUsername(username):
    sql = "select * from gkgp_user where username=%s"
    return dbsetting.query_one(sql,username)

def getUserByNickname(nickname):
    sql = "select * from gkgp_user where nickname=%s"
    return dbsetting.query_one(sql,nickname)

def getUserByNameAndPass(username,password):
    sql = "select * from gkgp_user where username=%s and password=%s";
    try:
        return dbsetting.query_one(sql,(username,password))
    except:
        traceback.print_exc()
        return None





