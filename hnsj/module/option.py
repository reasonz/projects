#encoding=utf-8
__author__ = 'reason'
from lib.bottle import route,run,template,static_file,view,Bottle,request ,redirect
from dbsetting import dbsetting as db
import sys,json,hashlib
from setting import SITE_DOMAIN
from index import getmenutype as getmenudict
reload(sys)
sys.setdefaultencoding('utf-8')
app = Bottle()

def dest(password):
        m = hashlib.md5(password)
        return m.hexdigest()

def getallmenu(): 
    conn = db.getmysqlconn()
    sql = "select t.id,t.menuname,t.path,t.parent  from HNSJ_TDCMS_MENU t "
    c = conn.cursor()
    l=[]
    c.execute(sql)
    for o in c.fetchall():
        l.append(o)
    c.close()
    conn.close()
    return l

def getusermenu(userid):
    conn=  db.getmysqlconn()
    sql = "select menuid from HNSJ_TDCMS_MENU_USER where userid = " + userid
    c = conn.cursor()
    c.execute(sql)
    l=[]
    for o in c.fetchall():
        l.append(o[0])
    c.close()
    conn.close()
    return l
def getalluser():
    conn = db.getmysqlconn()
    sql = "select * from HNSJ_TDCMS_USER"
    c=conn.cursor()
    c.execute(sql)
    l=[]
    for o in c.fetchall():
        l.append(o)
    c.close()
    conn.close()
    return l

def getmenutype():
    conn=  db.getmysqlconn()
    sql = "select * from HNSJ_TDCMS_MENU where parent=-1"
    c = conn.cursor()
    c.execute(sql)
    l=[]
    for o in c.fetchall():
        l.append(o)
    c.close()
    conn.close()
    return l    

@app.route('/powermanage')
@view('options/option')
def option():
    alluser= getalluser()
    allmenu = getallmenu()
    return dict(alluser=alluser,allmenu=allmenu,domain=SITE_DOMAIN)

@app.route('/usermanage')
@view('options/usermanager')
def option():
    alluser= getalluser()
    return dict(alluser=alluser,domain=SITE_DOMAIN)

@app.route('/projectmanage')
@view('options/projectmanager')
def project():
    allproject = getmenutype()
    return dict(allproject=allproject,domain=SITE_DOMAIN)


@app.route('/getpower/:userid')
def getpower(userid):
    print userid
    powerlist = getusermenu(userid)
    return json.dumps(powerlist)

@app.route('/setpower/:userid/:menuids')
def getpower(userid,menuids):
    conn = db.getmysqlconn()
    c=conn.cursor()
    delsql = "delete from HNSJ_TDCMS_MENU_USER where userid="+userid
    c.execute(delsql)
    for menuid in menuids.split(','):
        if len(menuid)>0:
            sql = "insert into HNSJ_TDCMS_MENU_USER (userid,menuid) values(%s,%s)"
            c.execute(sql,(userid,menuid ))
    conn.commit()
    c.close()
    conn.close()

@app.post('/adduser')
def adduser():
    username = request.forms.get('username')
    password =  request.forms.get('password')
    conn=  db.getmysqlconn()
    c=conn.cursor()
    sql="insert into HNSJ_TDCMS_USER (username,password) values(%s,%s) "
    c.execute(sql,(username,dest(password.strip())))
    conn.commit()
    c.close()
    conn.close()
    redirect ('usermanage')

@app.route('/deluser/:userids')
def deluser(userids):
    conn=  db.getmysqlconn()
    c=conn.cursor()
    for one in userids.split(','):
        if len(one) > 0:
            sql="delete from HNSJ_TDCMS_USER where id=%s"
            c.execute(sql,(one))
            conn.commit()
    c.close()
    conn.close()


@app.route('/menumanage')
@view('options/menumanager')
def option():
    allmenu= getallmenu()
    allproject= getmenutype()
    return dict(allmenu=allmenu,allproject = allproject,domain=SITE_DOMAIN,menudict=getmenudict())

@app.post('/addmenu')
def adduser():
    menuname = request.forms.get('menuname')
    url =  request.forms.get('url')
    projectid = request.forms.get('projectid')
    conn=  db.getmysqlconn()
    c=conn.cursor()
    sql="insert into HNSJ_TDCMS_MENU (menuname,path,parent) values(%s,%s,%s) "
    c.execute(sql,(menuname,url,projectid))
    conn.commit()
    c.close()
    conn.close()
    redirect ('menumanage')

@app.route('/delmenu/:menuids')
def deluser(menuids):
    conn=  db.getmysqlconn()
    c=conn.cursor()
    for one in menuids.split(','):
        if len(one) > 0:
            sql="delete from HNSJ_TDCMS_MENU where id="+one
            c.execute(sql)
            conn.commit()
    c.close()
    conn.close()


@app.post('/addproject')
def addproject():
    projectname = request.forms.get('projectname')
    conn = db.getmysqlconn()
    c=conn.cursor()
    sql = "insert into HNSJ_TDCMS_MENU (menuname,parent) values(%s,%s)"
    c.execute(sql,(projectname,'-1'))
    conn.commit()
    c.close()
    conn.close()
    redirect('projectmanage')

@app.route('/delproject/:projectid')
def delproject(projectid):
    conn = db.getmysqlconn()
    c = conn.cursor()
    for one in projectid.split(','):
        if len(one)>0:
            sql = "delete from HNSJ_TDCMS_MENU where id = %s"
            c.execute(sql,(one))
            conn.commit()
    c.close()
    conn.close()







