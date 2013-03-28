#encoding=utf-8
__author__ = 'reason'
from lib.bottle import view,Bottle
import sys
import datetime
from dbsetting import  dbsetting    as db

reload(sys)
sys.setdefaultencoding('utf-8')
today = datetime.datetime.now()-datetime.timedelta(days=1)
date=str(today.date())
app=Bottle()

@app.route('/:day')
@view("nokiareport")
def report(day):
    date=day
    all={}
    all['mix']=getmix(date)
    all['auchid']=getaugroupbychid(date)
    all['au7days']=getau7days(date)
    all['aubyua']=getaubyua(date)
    all['uadown']=getuadown(date)
    all['userchannel']=getuserbychannel(date)
    return dict(alllist=all)

def getmix(day):
    res={}
    #new au
    sql="select count(DISTINCT ci) from signin t where t.isnew=1 and t.addtime='"+day+"'"
    res['newau']=getone(sql)
    # au
    sql="select count(DISTINCT ci) from signin t where  t.addtime='"+day+"'"
    res['au']=getone(sql)
    # down users
    sql ="select count(distinct ci) from fee t where t.addtime='"+day+"'"
    res['downuser'] =getone(sql)
    #down times
    sql ="select count(id) from fee t where  t.addtime='"+day+"'"
    res['downtimes'] =getone(sql)
    #au30
    sql="select count(DISTINCT ci) from signin t where t.addtime >= SUBDATE('"+day+"',INTERVAL 30 DAY) and t.addtime <= '"+day+"'"
    res['au30']=getone(sql)
    #fee user
    sql="select count(DISTINCT ci) from fee  "
    res['feeuser']=getone(sql)
    #fee count
    sql="select count(id) from fee"
    res['feecount']=getone(sql)
    #fee bili
    sql="select count(DISTINCT ci) from signin"
    res['allusercount']=getone(sql)
    res['day']=day
    return res

def getaugroupbychid(day):
    res ={}
    sql1 = "select count(DISTINCT ci) p ,t.chid,t.addtime FROM signin t where  t.addtime='"+day+"' GROUP BY t.chid  order by p desc"
    auchid=getall(sql1)
    #new au-chid
    sql="select count(DISTINCT ci) p ,t.chid,t.addtime FROM signin t where t.isnew=1 and t.addtime='"+day+"' GROUP BY t.chid order by p desc"
    newauchid=getall(sql)
    for one in auchid:
        sub={}
        sub['chid']=one[1]
        sub['aucount']=one[0]
        sub['date']=str(one[2]).split(' ')[0]
        sub['newaucount']=0
        sub['qdname']=getchname(one[1])
        res[one[1]]=sub
    for one in newauchid:
        if res.get(one[1]) :
            res[one[1]]['newaucount']=one[0]
        else:
            sub={}
            sub['chid']=one[1]
            sub['newaucount']=one[0]
            sub['date']=str(one[2]).split(' ')[0]
            sub['qdname']=getchname(one[1])
            res[one[1]]=sub
    return res

def getau7days(day):
    sql="select count(DISTINCT ci) p,chid,addtime from signin t where t.addtime >= SUBDATE('"+day+"',INTERVAL 8 DAY)  and t.addtime <= '"+day+"' GROUP BY t.chid ORDER BY p desc"
    l=[]
    num=1
    for one in getall(sql):
        obj={}
        obj['count']=one[0]
        obj['chid']=one[1]
        obj['qdname']=getchname(one[1])
        obj['num']=num
        num+=1
        l.append(obj)
    return l

def getaubyua(day):
    sql="select count(DISTINCT ci) p,ua , addtime from signin t where t.addtime ='"+day+"' GROUP BY t.ua ORDER BY p desc"
    l1 = getall(sql)
    sql="select count(DISTINCT ci) p,ua , addtime from signin t where t.addtime ='"+day+"' and isnew=1 GROUP BY t.ua ORDER BY p desc"
    l2 = getall(sql)
    res ={}
    for one in l1:
        sub={}
        sub['ua']=one[1]
        sub['aucount']=one[0]
        sub['date']=str(one[2]).split(' ')[0]
        sub['newaucount']=0
        res[one[1]]=sub
    for one in l2:
        if res.get(one[1]) :
            res[one[1]]['newaucount']=one[0]
        else:
            sub={}
            sub['ua']=one[1]
            sub['newaucount']=one[0]
            sub['date']=str(one[2]).split(' ')[0]
            res[one[1]]=sub

    return res

def getuadown(day):
    sql="select count(*) p,ua , addtime from videostate t where t.addtime= '"+day+"' and t.type=4 GROUP BY t.ua ORDER BY p desc"
    l=getall(sql)
    return l

def getuserbychannel(day):
    sql="select c,u,t1.channel from  (select count(DISTINCT ci) c,channel from videostate t where t.addtime='"+day+"' GROUP BY channel ORDER BY c DESC) t1,(select sum(DISTINCT count) u,channel from videostate t where t.addtime='"+day+"'  GROUP BY channel ORDER BY u DESC) t2 where t1.channel = t2.channel"
    l=getall(sql)
    print sql
    res=[]
    for o in l:
        one={}
        one['date']=day
        one['channelid']=o[2]
        one['channelname']=getchannelname(o[2])
        one['usercount']=o[0]
        one['downcount']=o[1]
        res.append(one)
    return res

def getone(sql):
    conn = db.getnokiaconn()
    c = conn.cursor()
    c.execute(sql)
    result = c.fetchone()
    c.close()
    conn.close()
    return   result[0]

def getall(sql):
    conn = db.getnokiaconn()
    c = conn.cursor()
    c.execute(sql)
    l=[]
    for one in  c.fetchall():
        l.append(one)
    c.close()
    conn.close()
    return   l



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
    if channelid=='null':
        return "other"
    if channelid=='-1':
        return "推荐页"
    if channelid=='-2':
        return "搜索"
    cmsconn=db.getcmsconn()
    sql="select name from tdwl_cms_channel where id="+str(channelid)
    c = cmsconn.cursor()
    c.execute(sql)
    res = c.fetchone()
    c.close()
    cmsconn.close()
    if res==None:
        return "other"
    else:
        return res[0]
def getchname(chid):
    cmsconn=db.getcmsconn()
    sql="select qd_name from tdwl_cms_qd t where t.qd_id="+str(chid)
    c=cmsconn.cursor()
    c.execute(sql)
    res = c.fetchone()
    c.close()
    cmsconn.close()
    return res[0]

