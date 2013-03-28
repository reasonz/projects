#encoding=utf-8
__author__ = 'reason'
from lib.bottle import route,run,template,static_file,view,Bottle,request ,redirect
from dbsetting import dbsetting as db
import sys,json
from setting import SITE_DOMAIN
reload(sys)
sys.setdefaultencoding('utf-8')
app = Bottle()


def getallmenu():
    conn = db.getmysqlconn()
    sql = "select t.id,t.menuname,t.url,t1.projectname  from menulist t ,project t1 where t.projectid = t1.id  ORDER BY t1.projectname desc"
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
    sql = "select menuid from usermenu where userid = " + userid
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
    sql = "select * from users"
    c=conn.cursor()
    c.execute(sql)
    l=[]
    for o in c.fetchall():
        l.append(o)
    c.close()
    conn.close()
    return l

def getproject():
    conn=  db.getmysqlconn()
    sql = "select * from project"
    c = conn.cursor()
    c.execute(sql)
    l=[]
    for o in c.fetchall():
        l.append(o)
    c.close()
    conn.close()
    return l    

@app.route('/powermanage')
@view('option')
def option():
    alluser= getalluser()
    allmenu = getallmenu()
    return dict(alluser=alluser,allmenu=allmenu,domain=SITE_DOMAIN)

@app.route('/usermanage')
@view('usermanager')
def option():
    alluser= getalluser()
    return dict(alluser=alluser,domain=SITE_DOMAIN)

@app.route('/projectmanage')
@view('projectmanager')
def project():
    allproject = getproject()
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
    delsql = "delete from usermenu where userid="+userid
    c.execute(delsql)
    for menuid in menuids.split(','):
        if len(menuid)>0:
            sql = "insert into usermenu (userid,menuid) values("+userid+","+menuid + ")"
            print sql
            c.execute(sql)
    conn.commit()
    c.close()
    conn.close()

@app.post('/adduser')
def adduser():
    username = request.forms.get('username')
    password =  request.forms.get('password')
    conn=  db.getmysqlconn()
    c=conn.cursor()
    sql="insert into users (username,password) values('"+username+"','"+password+"') "
    c.execute(sql)
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
            sql="delete from users where id="+one
            c.execute(sql)
            conn.commit()
    c.close()
    conn.close()


@app.route('/menumanage')
@view('menumanager')
def option():
    allmenu= getallmenu()
    allproject= getproject()
    return dict(allmenu=allmenu,allproject = allproject,domain=SITE_DOMAIN)

@app.post('/addmenu')
def adduser():
    menuname = request.forms.get('menuname')
    url =  request.forms.get('url')
    projectid = request.forms.get('projectid')
    conn=  db.getmysqlconn()
    c=conn.cursor()
    sql="insert into menulist (menuname,url,projectid) values(%s,%s,%s) "
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
            sql="delete from menulist where id="+one
            c.execute(sql)
            conn.commit()
    c.close()
    conn.close()


@app.post('/addproject')
def addproject():
    projectname = request.forms.get('projectname')
    conn = db.getmysqlconn()
    c=conn.cursor()
    sql = "insert into project (projectname) values(%s)"
    c.execute(sql,(projectname))
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
            sql = "delete from project where id = %s"
            c.execute(sql,(one))
            conn.commit()
    c.close()
    conn.close()







