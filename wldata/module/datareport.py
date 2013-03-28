#encoding=utf-8
__author__ = 'reason'
from lib.bottle import view,Bottle
import sys
import datetime
from dbsetting import  dbsetting    as db
reload(sys)
sys.setdefaultencoding('utf-8')
from setting import SITE_DOMAIN

today = datetime.datetime.now()-datetime.timedelta(days=1)
date=str(today.date())
app = Bottle()

@app.route('/')
@view("data")
def report():
      all={}
      all['fee']=getfee()
      all['indexpv']=getindexpv()
      all['iteminfopv']=getiteminfopv()
      all['itemtop10']=getitemtop10()
      all['keywordtop10']=    getsearchtop10()
      all['keywordall']=    getsearchall()
      all['iteminfoorderbyfee']= getitemall()
      all['channelvisit']=getchannelvisit()
      all['areatop10']=getareatop10()
      return dict(alllist=all,domain=SITE_DOMAIN)

def getfee():
    conn=db.getnokiaconn()
    l=[]
    sql="select sum(t.price) ,t.addtime ,count(*) from fee t  where t.addtime > SUBDATE(now(),INTERVAL 10 DAY) GROUP BY t.addtime  order by t.addtime desc"
    c=conn.cursor()
    c.execute(sql)
    res=c.fetchall()
    for one in res:
        fee={}
        fee['date']=str(one[1]).split(' ')[0]
        fee['fee']=str(one[0])
        fee['num']=str(one[2])
        l.append(fee)
    c.close()
    conn.close()
    return l

def getindexpv():
    conn=db.getnokiaconn()
    sql="select sum(t.count),t.addtime from channel t where t.channel=-1  and t.addtime > SUBDATE(now(),INTERVAL 10 DAY)  GROUP BY t.addtime order by t.addtime desc"
    c=conn.cursor()
    c.execute(sql)
    l=[]
    for one in c.fetchall():
        indexpv={}
        indexpv['indexpv']=str(one[0])
        indexpv['date']=str(one[1]).split(' ')[0]
        l.append(indexpv)
    c.close()
    conn.close()
    return l

def getiteminfopv():
    conn=db.getnokiaconn()
    sql="select sum(t.count),t.addtime from iteminfo t where t.addtime > SUBDATE(now(),INTERVAL 10 DAY) GROUP BY t.addtime order by t.addtime desc"
    c=conn.cursor()
    c.execute(sql)
    l=[]
    for one in c.fetchall():
        obj={}
        obj['pv']=str(one[0])
        obj['date']=str(one[1]).split(' ')[0]
        l.append(obj)
    c.close()
    conn.close()
    return l

def getitemtop10():
    conn=db.getnokiaconn()
    sql="select itemid ,sum(price) p,addtime from fee t where  t.addtime = SUBDATE(CURDATE() ,INTERVAL 1 DAY)  GROUP BY itemid order by p desc  limit 0,10"
    c=conn.cursor()
    c.execute(sql)
    l=[]
    for one in c.fetchall():
        obj={}
        obj['itemid']=str(one[0])
        obj['title']=gettitle(str(one[0]))
        obj['fee']=str(one[1])
        obj['date']=str(one[2]).split(' ')[0]
        l.append(obj)
    c.close()
    conn.close()
    return l

def getitemall():
    conn=db.getnokiaconn()
    sql="select itemid ,sum(price) p from fee t    GROUP BY itemid order by p desc  limit 0,10"
    c=conn.cursor()
    c.execute(sql)
    l=[]
    num=1;
    for one in c.fetchall():
        obj={}
        obj['itemid']=str(one[0])
        obj['title']=gettitle(str(one[0]))
        obj['fee']=str(one[1])
        obj['num']= num
        num+=1
        l.append(obj)
    c.close()
    conn.close()
    return l


def getsearchtop10():
    conn=db.getnokiaconn()
    sql="select keyword ,count,addtime from search t where t.addtime = SUBDATE(CURDATE() ,INTERVAL 1 DAY) ORDER BY count desc  limit 0,10"
    c=conn.cursor()
    c.execute(sql)
    l=[]
    for one in c.fetchall():
        obj={}
        obj['keyword']=str(one[0])
        obj['count']=str(one[1])
        obj['date']=str(one[2]).split(' ')[0]
        l.append(obj)
    c.close()
    conn.close()
    return l

def getsearchall():
    conn=db.getnokiaconn()
    sql="select keyword ,sum(count) p from search t  GROUP BY keyword ORDER BY p desc  limit 0,10"
    c=conn.cursor()
    c.execute(sql)
    l=[]
    num=1
    for one in c.fetchall():
        obj={}
        obj['keyword']=str(one[0])
        obj['count']=str(one[1])
        obj['num']=num
        num+=1
        l.append(obj)
    c.close()
    conn.close()
    return l

def getchannelvisit():
    conn=db.getnokiaconn()
    sql="select sum(t.count) c, t.channel t from channel t where t.addtime >= SUBDATE(CURDATE(),INTERVAL 1 DAY) GROUP BY t.channel order by c desc limit 0,10"
    c=conn.cursor()
    c.execute(sql)
    l=[]
    num=1
    for one in c.fetchall():
        obj={}
        obj['count']=str(one[0])
        obj['num']=num
        obj['channel']=getchannelname(str(one[1]))
        num+=1
        l.append(obj)
    c.close()
    conn.close()
    return l


def getareatop10():
    sql="select sum(count) p ,area from signin where addtime = SUBDATE(CURDATE(),INTERVAL 1 DAY)   GROUP BY area ORDER BY p desc limit 0,10"
    conn=db.getnokiaconn()
    c=conn.cursor()
    c.execute(sql)
    l=[]
    num=1
    for one in c.fetchall():
        sub={}
        sub['num']=num
        sub['area']=one[1]
        sub['count']=one[0]
        l.append(sub)
        num+=1
    return l

def gettitle(itemid):
    cmsconn=db.getcmsconn()
    sql="select title from tdwl_cms_item where item_id="+str(itemid)
    c = cmsconn.cursor()
    c.execute(sql)
    res = c.fetchone()
    if not res :
        sql="select title from tdwl_cms_nokia_item where item_id="+str(itemid)
        c.execute(sql)
        res= c.fetchone()
    c.close()
    cmsconn.close()
    if not res:
        res=["无标题  itemid:"+str(itemid)]
    return res[0]



def getchannelname(channelid):
    if channelid=='-1':
        return "推荐页"
    cmsconn=db.getcmsconn()
    sql="select name from tdwl_cms_channel where id="+str(channelid)
    c = cmsconn.cursor()
    c.execute(sql)
    res = c.fetchone()
    c.close()
    cmsconn.close()
    print type(res)
    if res==None:
        return "-"
    else:
        return res[0]


