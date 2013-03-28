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
    print visit
    d={}
    pv=0
    cv=0
    for one in visit:
        pv += one['pv']
        cv += one['cv']
    d['pvcount']=pv
    d['cvcount']=cv
    return d


@app.route('/allcount')
@app.route('/allcount/:start/:end/:area/:ver/:wap')
@view("tdwap/tdwap_allvisit")
def visitreport(start='start',end='end',area='all',ver='all',wap='all'):
    if start=='start' and end=='end':
        (start,end)=getdefaulttime()
    else:
        d = time.strptime(end, '%Y-%m-%d')
        temp=datetime.datetime(*d[:6])
        endtime = temp
        end = str(endtime.date())
   
    allcount=getall(start,end,area,ver,wap)
    scopecount = getvisitcount(allcount)
    allarea=getarea()
    selected = {'ver':ver,'wap':wap,'area':area}
    return dict(all=allcount,timescope=(start,end),jsonval=json.dumps(allcount),scopecount=scopecount,domain=SITE_DOMAIN,allarea=allarea,selected=selected)





def getall(start,end,area,ver,wap):
    qs = " and  day >='"+start+"' and day<=  '" + end + "'"
    if area !="all":
        qs +=" and area = " + area
    if ver != "all" :
        qs +=" and ver =" + ver
    if wap !='all' : 
        qs +=" and  wapportal=" + wap
    sql = "select pv.`day`,pv.pvcount,cv.cvcount from (select sum(count) pvcount ,day from tdwap_api where 1=1 "+ qs+ "  GROUP BY day)  pv \
     , (select sum(count) cvcount ,day from tdwap_api  where api in ('play','down') " + qs+ "  GROUP BY day) cv where pv.`day` = cv.`day`"
    print sql
    conn = db.getmysqlconn() 
    c = conn.cursor()
   
    c.execute(sql)
    l=[]
    for o in c.fetchall():
        d={}
        d['day']=str(o[0]).split(' ')[0]
        d['pv'] = int(o[1])
        d['cv'] = int(o[2])
        l.append(d)
    c.close()
    conn.close()
    return l

def getarea():
    conn = db.getmysqlconn() 
    c = conn.cursor()
    c.execute("select DISTINCT province_id , province_name from area")
    l=[]
    for o in c.fetchall():
        d={}
        d['id']=o[0]
        d['name']=o[1]
        l.append(d)
    c.close()
    conn.close()
    return l

#------------tdwap cv------------#


@app.route('/cv')
@app.route('/cv/:start/:end/:area/:ver/:wap/:api')
@view("tdwap/tdwap_cv")
def cvreport(start='start',end='end',area='all',ver='all',wap='all',api='all'):
    if start=='start' and end=='end':
        (start,end)=getdefaulttime()
    else:
        d = time.strptime(end, '%Y-%m-%d')
        temp=datetime.datetime(*d[:6])
        endtime = temp
        end = str(endtime.date())
   
    cv=getcvbycvtype(start,end,area,ver,wap,api)
    # scopecount = getvisitcount(allcount)
    allarea=getarea()
    selected = {'ver':ver,'wap':wap,'area':area,'api':api}
    return dict(all=cv,timescope=(start,end),jsonval=json.dumps(cv),\
        domain=SITE_DOMAIN,allarea=allarea,selected=selected) 


def getcvbycvtype(start,end,area,ver,wap,api):
    typedict = {1:"流畅(500)版",2:"清晰(51)版",3:"高清(52)版",4:"超清(53)版",5:"超清(54)版",6:"在线(FLV)版",-1:"其他"}
    qs = " and  day >='"+start+"' and day<=  '" + end + "'"
    if area !="all":
        qs +=" and area = " + area
    if ver != "all" :
        qs +=" and ver =" + ver
    if wap !='all' : 
        qs +=" and  wapportal=" + wap
    if api !='all' : 
        if api =='1':
            qs +=" and  api='play'"
        else:
            qs +=" and  api='down'"

    sql = "select sum(count) c ,day,cvtype from tdwap_cv t where 1=1 "+ qs +" GROUP BY t.`day`,t.cvtype ORDER BY day,cvtype"
    # print sql

    tsql = "select tt.day  ,\
            max(case when tt.cvtype =1 THEN tt.c else 0 end) as '500',\
            max(case when tt.cvtype =2 THEN tt.c else 0 END) as '51',\
            max(case when tt.cvtype =3 THEN tt.c else 0 END) as '52',\
            max(case when tt.cvtype =4 THEN tt.c else 0 END) as '53',\
            max(case when tt.cvtype =5 THEN tt.c else 0 END) as '54',\
            max(case when tt.cvtype =6 THEN tt.c else 0 END) as 'FLV',\
            max(case when tt.cvtype =-1 THEN tt.c else 0 END) as 'other',\
            sum(tt.c) as 'count' \
            from (" +sql + ")  tt GROUP BY tt.day"

    print tsql
    conn = db.getmysqlconn()
    c = conn.cursor()
    c.execute(tsql)

    pvsql = "select day,sum(count) c  from tdwap_api GROUP BY day"
    c1 = conn.cursor()
    c1.execute(pvsql)
    pd={}
    for p in c1.fetchall():
        pd[str(p[0]).split(' ')[0]]=int(p[1])

    c1.close()
    l=[]
    for o in c.fetchall():
        d={}
        d['day']=str(o[0]).split(' ')[0]
        d['_500']=int(o[1])
        d['_51']=int(o[2])
        d['_52']=int(o[3])
        d['_53']=int(o[4])
        d['_54']=int(o[5])
        d['FLV']=int(o[6])
        d['other']=int(o[7])
        d['count']=int(o[8])
        d['convert']=round(float(o[8]) / float(pd[str(o[0]).split(' ')[0]])*100,2)
        l.append(d)
    return l

    c.close()
    conn.close()


            



