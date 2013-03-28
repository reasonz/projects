#encoding=utf-8
__author__ = 'reason'
from lib.bottle import template,Bottle,request,view
from lib.cachewrap import cache
from dbsetting import dbsetting as db
import sys,hashlib
from utils import getallchannel
from setting import SITE_DOMAIN,PLAY_VIDEO_DOMAIN
reload(sys)
sys.setdefaultencoding('utf-8')

app = Bottle()



# l=[]
# for i in xrange(0,200):
#     one=[]
#     one.append(str(i))
#     one.append("name"+str(i))
#     one.append('http://i2.tdimg.com/159/007/051/p.jpg')
#     l.append(one)

pagesize=10
@app.route('/getitems')
@view('video/video_item')
def getitems():
    page = request.query.get('page',1)
    vid = request.query.get('id')
    vtitle = request.query.get('title')
    vproduct = request.query.get('product')
    vcp = request.query.get('cp')
    vstart=request.query.get('start')
    vend=request.query.get('end')
    page = int(page)
    start = (page-1)*pagesize
    end = (page)*pagesize
    print start,end
    channellist=getallchannel()

   
    conn=db.getmysqlconn()
    c= conn.cursor()
    qs = " 1=1"
    querylist= []
    query_args={"title":'',"id":'',"start":'',"end":''}
    if vid and len(vid)>0:
        qs += " and  itemid='"+vid + "'"
        query_args['itemid']=vid
        
    if vtitle and len(vtitle)>0:
        qs += " and title='"+ vtitle + "'"
        query_args['title']=vtitle
        
    if vstart and vend and len(vstart)>0 and len(vend)>0:
        qs += " and addtime >='"+vstart + "' and addtime <='" + vend +"'"
        query_args['start']=vstart
        query_args['end']=vend

    sql = "select * from gkgp_item where "+qs+" limit %s,%s"
    c.execute(sql,(start,pagesize)) 

    l=[]
    for one in c.fetchall():
        l.append(one)
    print len(l)
    sqlcount = "select count(*) from gkgp_item where " + qs
    c.execute(sqlcount)
    totalrecord = c.fetchone()[0]
    c.close()
    conn.close()
    totalpage=0
    if totalrecord/pagesize <1:
        totalpage=1
    else:
        if totalrecord % pagesize ==0:
            totalpage=totalrecord/pagesize
        else:
            totalpage = totalrecord/pagesize + 1
    return dict(all=l,total=totalpage,domain=SITE_DOMAIN,startpage=page,channellist=channellist,query_args=query_args,play_domain=PLAY_VIDEO_DOMAIN)

@app.route('/ishaveitem')
def ishaveitem():
    ids=request.query.get('ids')
    channelid=request.query.get('channelid')
    # ignore=request.query.get('ignore')
    conn = db.getmysqlconn()
    c = conn.cursor()
    exist_flag=False
    for id in ids.split('_'):
        sql = 'select count(*) from gkgp_channel_item_link where item_id = %s and  channel_id=%s'
        c.execute(sql,(id,channelid))
        if c.fetchone()[0] > 0:
            exist_flag = True
    c.close()
    conn.close()      
    if exist_flag:
        return "exist"
    else:
        return "none"


@app.route('/changechannel')
def changechannel():
    ids=request.query.get('ids')
    channelid=request.query.get('channelid')    
    ignore=request.query.get('ignore')
    conn = db.getmysqlconn()
    c = conn.cursor()
    for id in ids.split('_'):
        if id=='':
            break
        if ignore =='1':
            sql = 'select count(*) from HNSJ_TDCMS_CHANNEL_ITEM WHERE ITEMID=%s AND CHANNELID=%s'
            c.execute(sql,(id,channelid))
            if c.fetchone()[0] > 0:
                exist_flag = True
            else:
                insert_item(conn,c,id,channelid)
        elif ignore=='0':
            #delete item in table channel_item
            delete_sql = 'delete from HNSJ_TDCMS_CHANNEL_ITEM WHERE itemid=%s and channelid=%s'
            c.execute(delete_sql,(id,channelid))
            insert_item(conn,c,id,channelid)
    c.close()
    conn.close()
    return 'ok'


def insert_item(conn,c,id,channelid):
    #get item by item id
    select_sql = 'select id,contentid,namecn,cpid,still,Description from HNSJ_TDCMS_ITEM where id = %s'
    c.execute(select_sql,(id))
    item = c.fetchone()
    contentid = item[1]
    title = item[2]
    cpid = item[3]
    picurl= item[4]
    desc = item[5]
    insert_sql = "insert into HNSJ_TDCMS_CHANNEL_ITEM (contentid,itemid,channelid,title,cpid,picurl,Description) values(%s,%s,%s,%s,%s,%s,%s)"
    c.execute(insert_sql,(contentid,id,channelid,title,cpid,picurl,desc))
    print 'add %s ' % (id)
    conn.commit()








