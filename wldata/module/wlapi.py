#encoding=utf-8
#encoding=utf-8

from lib.bottle import view,Bottle
import sys,json,datetime ,time
from dbsetting import  dbsetting    as db
reload(sys)
sys.setdefaultencoding('utf-8')
from setting import SITE_DOMAIN
app = Bottle()

def test():
    conn = db.getconn()
    c= conn.cursor()
    sql = "select * from TDCHARGE_SH_UNICOM_INFO"
    c.execute(sql)
    for o in c.fetchall():
        print o

def getdefaulttime():
    tstart = datetime.datetime.now()-datetime.timedelta(days=15)
    tend = datetime.datetime.now()
    start=str(tstart.date())
    end=str(tend.date())
    return (start,end)


def getvisitcount(visit):
    d={}
    pv=0
    uv=0
    ip=0
    usetime=0
    s=1
    for one in visit:
        pv += one['pv']
        uv += one['uv']
        ip += one['ip']
        usetime += one['usetime']
        s+=1
    d['pvcount']=pv
    d['uvcount']=uv
    d['ipcount']=ip
    d['usetime']=usetime/s
    return d

@app.route('/visit')
@app.route('/visit/:start/:end/:visittype')
@view("wlapi/wlapi_visit")
def visitreport(start='start',end='end',visittype='PV'):
    if start=='start' and end=='end':
        (start,end)=getdefaulttime()
    else:
        d = time.strptime(end, '%Y-%m-%d')
        temp=datetime.datetime(*d[:6])
        endtime = temp   +datetime.timedelta(days=1)
        end = str(endtime.date())
    visit=getvisit(start,end)
    allcount = getvisitcount(visit)
    return dict(all=visit,allcount=allcount,timescope=(start,end),jsonval=json.dumps(visit),domain=SITE_DOMAIN,vt=visittype)

def getvisit(start,end):
    sql = "select * from wl_api_all where  day >='"+start+"' and day<='"  +end  +"' order by day asc"
    print sql
    conn = db.getmysqlconn()
    c = conn.cursor()
    c.execute(sql)
    l=[]
    for o in c.fetchall():
        d={}
        d['pv']=int(o[1])
        d['uv']=int(o[2])
        d['ip']=int(o[3])
        d['usetime']=float(o[4])
        d['date']=str(o[5]).split(' ')[0][2:]
        l.append(d)
    c.close()
    conn.close()
    return l


@app.route('/method')
@app.route('/method/:start')
@view("wlapi/wlapi_method")
def methodreport(start='start'):
    if start=='start' :
         tstart = datetime.datetime.now()-datetime.timedelta(days=1)
         start=str(tstart.date())
    methodlist=getmethod(start)
    return dict(all=methodlist,timescope=(start),jsonval=json.dumps(methodlist),domain=SITE_DOMAIN)

@app.route('/method_usetime')
@app.route('/method_usetime/:start')
@view("wlapi/wlapi_method_usetime")
def usetimereport(start='start'):
    if start=='start' :
         tstart = datetime.datetime.now()-datetime.timedelta(days=1)
         start=str(tstart.date())
    usetimelist=getusetime(start)
    res=getmethodall(start)
    if not res:
        return "no data!"
    else:
        return dict(all=usetimelist,timescope=(start),jsonval=json.dumps(usetimelist),domain=SITE_DOMAIN,pv_avg=res)

def getusetime(start):
    sql = "select *  from wl_api_method where  preusetime >0 and  day ='"+start+"'  order by preusetime desc"
    print sql
    conn = db.getmysqlconn()
    c = conn.cursor()
    c.execute(sql)
    l=[]
    for o in c.fetchall():
        d={}
        d['apiname']=o[1][:15]
        d['count']=int(o[3])
        d['date']=str(o[4]).split(' ')[0][2:]
        d['usetime']=int(o[5])
        if d['apiname']!='download':
            l.append(d)
    c.close()
    conn.close()
    return l

def getmethod(start):
    sql = "select *  from wl_api_method where  count >10 and  day ='"+start+"'  order by count desc"
    print sql
    conn = db.getmysqlconn()
    c = conn.cursor()
    c.execute(sql)
    l=[]
    for o in c.fetchall():
        d={}
        d['apiname']=o[1][:15]
        d['count']=int(o[3])
        d['date']=str(o[4]).split(' ')[0][2:]
        d['usetime']=int(o[5])
        l.append(d)
    c.close()
    conn.close()
    return l

def getmethodall(start):
    sql = "select * from wl_api_all where  day ='"+start+"' "
    conn = db.getmysqlconn()
    c = conn.cursor()
    c.execute(sql)
    res = c.fetchone()
    if res :
        pv = res[1]
        avg= res[4]
        return (pv,avg)
    c.close()
    conn.close()





