#encoding=utf-8
__author__ = 'reason'
from lib.bottle import template,Bottle,request
from lib.cachewrap import cache
from dbsetting import dbsetting as db
import sys,hashlib
from setting import    SITE_DOMAIN
reload(sys)
sys.setdefaultencoding('utf-8')

app = Bottle()


def dest(password):
        m = hashlib.md5(password)
        return m.hexdigest()


def login(username):
    conn=db.getmysqlconn()
    sql="select id,username,password from gkgp_cms_user where username=%s"
    c = conn.cursor()
    c.execute(sql,(username))
    res = c.fetchone()
    if res :
        return res
    else:
        return res
    c.close()
    conn.close()


@app.route('/login')
@app.post('/login')
def report():
    username = request.forms.get('username')
    password =  request.forms.get('password')
    if not username and not password:
        return index()
    password = dest(password)
    res =login(username)
    if res and password == res[2] :
        menulist =getmenulist(res[0])
        menutype = getmenutype()
        return template('main',dict(mlist = menulist,uname= res[1],domain=SITE_DOMAIN,menutype=menutype))
    else :
        return template('login',dict(res=False,domain=SITE_DOMAIN))

@app.route('/home')
def index():
    return template('login',dict(res=True,domain=SITE_DOMAIN))

@app.route('/welcome')
def welcome ():
    return template('welcome',dict(res=True,domain=SITE_DOMAIN))

def getmenulist(userid) :
    conn= db.getmysqlconn()
    sql = "SELECT m.id,u.username,u.id,m.menuname,m.PATH,m.PARENT FROM  gkgp_cms_user u, gkgp_cms_menu m, gkgp_cms_menu_user mu \
            WHERE u.ID = mu.USERID and m.ID = mu.menuid and u.ID=%s ORDER BY m.PARENT ASC"
    c=conn.cursor()
    c.execute(sql,(userid))
    rs = c.fetchall()
    menu = {}
    for o in rs:
        if o[5]==-1:
            menu[o[0]]=[]
        else:
            l=menu.get(o[5])
            l.append(o)

    c.close()
    conn.close()
    return menu

def getmenutype():
    conn= db.getmysqlconn()
    sql = "select * from gkgp_cms_menu where parent=-1"
    c=conn.cursor()
    c.execute(sql)
    rs = c.fetchall()
    menutype = {}
    for o in rs:
        menutype[o[0]]=o[1]
    c.close()
    conn.close()
    return menutype

