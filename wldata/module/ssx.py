#encoding=utf-8
__author__ = 'reason'
from lib.bottle import view,Bottle
import sys,time
import datetime,json
from dbsetting import  dbsetting as db
reload(sys)
sys.setdefaultencoding('utf-8')

today = datetime.datetime.now()-datetime.timedelta(days=1)
date=str(today.date())
app = Bottle()

def getdefaulttime():
    tstart = datetime.datetime.now()-datetime.timedelta(days=15)
    tend = datetime.datetime.now() +datetime.timedelta(days=1)
    start=str(tstart.date())
    end=str(tend.date())
    return (start,end)

@app.route('/')
@view("ssx")
def report():
    return dict()

@app.route('/indexpv')
def getindexpv():
    conn=db.getnokiaconn()
    sql="select sum(t.count),t.addtime from channel t where t.channel=-1  and t.addtime > SUBDATE(now(),INTERVAL 30 DAY)  GROUP BY t.addtime order by t.addtime asc"
    c=conn.cursor()
    c.execute(sql)
    l=[]
    for one in c.fetchall():
        indexpv={}
        indexpv['indexpv']=str(one[0])
        indexpv['date']=str(one[1]).split(' ')[0][5:]
        l.append(indexpv)
    c.close()
    conn.close()
    return json.dumps(l)

@app.route('/fee')
def getfee(start='start',end='end'):
    if start=='start' and end=='end':
        (start,end)=getdefaulttime()
    else:
        d = time.strptime(end, '%Y-%m-%d')
        temp=datetime.datetime(*d[:6])
        endtime = temp   +datetime.timedelta(days=1)
        end = str(endtime.date())
        conn=db.getnokiaconn()
        l=[]
        sql="select sum(t.price) ,t.addtime ,count(*) from fee t  where t.addtime >="+start+" and t.addtime<="+end+"GROUP BY t.addtime  order by t.addtime asc"
        c=conn.cursor()
        c.execute(sql)
        res=c.fetchall()
        for one in res:
            fee={}
            fee['date']=str(one[1]).split(' ')[0][5:]
            fee['fee']=str(one[0])
            l.append(fee)
        c.close()
        conn.close()
        return json.dumps(l)




