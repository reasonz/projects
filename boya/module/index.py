#encoding=utf-8
__author__ = 'reason'
from lib.bottle import template,Bottle,request
from dbsetting import dbsetting as db
import sys
from setting import    SITE_DOMAIN
reload(sys)
sys.setdefaultencoding('utf-8')
app = Bottle()


def login(username):
    conn=db.getmysqlconn()
    sql="select id,username,password from users where username='"+username+"'"
    c = conn.cursor()
    c.execute(sql)
    res = c.fetchone()
    if res :
        return res
    else:
        return res
    c.close()
    conn.close()

@app.post('/login')
def report():
    username = request.forms.get('username')
    password =  request.forms.get('password')
    res =login(username)
    if res and password == res[2] :
        menulist =getmenulist(res[0])
        
        return template('main',dict(mlist = menulist,uname= res[1],domain=SITE_DOMAIN))
    else :
        return template('index',dict(res=False,domain=SITE_DOMAIN))

@app.route('/home')
def index():
    return template('index',dict(res=True,domain=SITE_DOMAIN))

@app.route('/welcome')
def index():
    return template('welcome',dict(res=True,domain=SITE_DOMAIN))

def getmenulist(userid) :
    conn= db.getmysqlconn()
    sql = "select users.username,users.id,menulist.menuname,project.projectname,menulist.url "\
    "from users,menulist,usermenu,project where menulist.projectid = project.id and  users.id = usermenu.userid and menulist.id = usermenu.menuid and users.id= "+str(userid) + \
    " order by projectid desc"
    c=conn.cursor()
    c.execute(sql)
    rs = c.fetchall()
    projects = {}
    for o in rs:
        l = projects.get(o[3])
        if l :
            l.append(o)
        else:
            projects[o[3]]=[o]

    c.close()
    conn.close()
    return projects

