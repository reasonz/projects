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

@app.route('/order')
@app.route('/order/:start/:end')
@view("shunicom/shunion")
def report(start='start',end='end'):
    if start=='start' or end=='end':
        (start,end)=getdefaulttime()
    else:
        d = time.strptime(end, '%Y-%m-%d')
        temp=datetime.datetime(*d[:6])
        endtime = temp   +datetime.timedelta(days=1)
        end = str(endtime.date())
    fee=getfee(start,end)
    allcount = getallcount(fee)
    count = getcount()
    return dict(all=fee,allcount=allcount,timescope=(start,end),count = count,jsonval=json.dumps(fee),domain=SITE_DOMAIN)

def getdefaulttime():
    tstart = datetime.datetime.now()-datetime.timedelta(days=15)
    tend = datetime.datetime.now() +datetime.timedelta(days=1)
    start=str(tstart.date())
    end=str(tend.date())
    return (start,end)

def getfee(start,end):
    conn=  db.getconn() 
    c = conn.cursor()
    d= wapperVisit(start,end)
    print d
    sql1 = "SELECT * FROM (SELECT  TO_CHAR(T .CREATE_TIME, 'yyyy-mm-dd') D, COUNT(T .UPDATE_TYPE) c  FROM TDCHARGE_SH_UNICOM_INFO T WHERE T .UPDATE_TYPE = 1  and t.CREATE_TIME  BETWEEN to_date('"+start+"', 'yyyy-mm-dd') and to_date('"+end+"', 'yyyy-mm-dd')  GROUP BY TO_CHAR(T .CREATE_TIME, 'yyyy-mm-dd') ) t1 LEFT JOIN(SELECT TO_CHAR(T .CREATE_TIME, 'yyyy-mm-dd') D, COUNT(T .UPDATE_TYPE) c FROM TDCHARGE_SH_UNICOM_INFO T WHERE T .UPDATE_TYPE = 2  and t.CREATE_TIME  BETWEEN to_date('"+start+"', 'yyyy-mm-dd') and to_date('"+end+"', 'yyyy-mm-dd') GROUP BY TO_CHAR(T .CREATE_TIME, 'yyyy-mm-dd'))t2 ON t1.D=t2.D ORDER BY T1.D"
    c.execute(sql1)
    l=[]
    for o in c.fetchall():
        one = {}
        one['date']=o[0]

        t  = d.get(o[0])
        if not t:
            one['pv']=0
            one['uv']=0
            one['pvconvert']=0
            one['uvconvert']=0
        else: 
            one['pv']=t['pv']
            one['uv']=t['uv']
            one['pvconvert']=round(float(o[1])/float(one['pv'])*100,2)
            one['uvconvert']=round(float(o[1])/float(one['uv'])*100,2)
        one['dinggou']=o[1]
        if o[3] : 
            one['tuiding']= o[3]
        else:
            one['tuiding']=0
        #one['jingdinggou']=int(one['tuiding'])/int(one['dinggou']) * 100
        l.append(one)
    c.close()
    conn.close()
    return l

def getcount():
    conn = db.getconn()
    c = conn.cursor()
    sql = "select UPDATE_TYPE ,count(ID) from TDCHARGE_SH_UNICOM_INFO GROUP BY UPDATE_TYPE"
    c.execute(sql)
    res = c.fetchall()
    d={}
    for one in res:
        if one[0]==1:
            d['dinggou']=one[1]
        else:
            d['tuiding']= one[1]

    c.close()
    conn.close()
    return d


def getallcount(fee):
    d={}
    dinggou=0
    tuiding=0
    pv = 0
    uv = 0
    for one in fee:
        dinggou += one['dinggou']
        tuiding += one['tuiding']
        pv +=one['pv']
        uv +=one['uv'] 

    d['dinggou']=dinggou
    d['tuiding']=tuiding
    d['pv']=pv
    d['uv']=uv
    d['pvconvert']=round(float(dinggou)/float(pv)*100,2)
    d['uvconvert']=round(float(dinggou)/float(uv)*100,2)
    return d

def getvisitcount(visit):
    print visit
    d={}
    pv=0
    uv=0
    for one in visit:
        pv += one['pv']
        uv += one['uv']
    d['pvcount']=pv
    d['uvcount']=uv
    return d

@app.route('/visit')
@app.route('/visit/:start/:end/:nettype/:wapver')
@view("shunicom/shunionvisit")
def visitreport(start='start',end='end',nettype='None',wapver='None'):
    if start=='start' or end=='end':
        (start,end)=getdefaulttime()
    else:
        d = time.strptime(end, '%Y-%m-%d')
        temp=datetime.datetime(*d[:6])
        endtime = temp   +datetime.timedelta(days=1)
        end = str(endtime.date())
    visit=getvisit(start,end,nettype,wapver)
    allcount = getvisitcount(visit)
    return dict(all=visit,allcount=allcount,timescope=(start,end),jsonval=json.dumps(visit),domain=SITE_DOMAIN)

def getvisit(start,end,nettype,wapver):
    querystr=""
    if nettype!='None':
        querystr = querystr + ' and net=\'"' + nettype + '"\' '
    if wapver!='None':
        querystr = querystr + ' and wapver=\'"' + wapver + '"\' '
    sql = "select * from (select  sum(count),day as pvday from shunicom_visit t where 1=1 "+querystr+" GROUP BY t.`day`) as  pv,(select COUNT(DISTINCT phone) ,day as uvday from shunicom_visit t where 1=1 "+querystr+" GROUP BY day) as  uv  where pv.pvday = uv.uvday  and  pv.pvday >='"+start+"' and pv.pvday <='"+end+"'  ORDER BY pv.pvday asc "
    print sql
    conn = db.getmysqlconn()
    c = conn.cursor()
    c.execute(sql)
    l=[]
    for o in c.fetchall():
        d={}
        d['pv']=int(o[0])
        d['uv']=int(o[2])
        d['date']=o[1]
        l.append(d)
    c.close()
    conn.close()
    return l

def wapperVisit(start,end):
    v = getvisit(start,end,'None','None')
    d={}
    for o in v :
        t={'pv':o['pv'],'uv':o['uv']}
        d[str(o['date'])]=t
       
    return d