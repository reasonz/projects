#encoding=utf-8
__author__ = 'reason'
from lib.bottle import template,Bottle,request,view
from lib.cachewrap import cache
from dbsetting import dbsetting as db
import sys,hashlib,traceback
from utils import getallchannel,getallmenu,getchannelnamebyid
from setting import    SITE_DOMAIN
reload(sys)
sys.setdefaultencoding('utf-8')

app = Bottle()

channel_type_dict={1:"普通频道",2:"特殊频道",3:"视频头条",4:"视频排行",5:"视频推荐",6:"海报",7:"精彩推荐"}

 
pagesize=10
@app.route('/getitems')
@view('channel/channel')
def getitems():
   
    channellist=getallchannel()
    menulist = getallmenu()
    return dict(domain=SITE_DOMAIN,channellist=channellist,channel_type_dict=channel_type_dict,menulist=menulist)
    
def getallchannel():
    conn = db.getmysqlconn()
    c=conn.cursor()
    sql = "select * from HNSJ_TDCMS_CHANNEL"
    c.execute(sql)
    l=[]
    for one in c.fetchall():
        l.append(one)
    c.close()
    conn.close()
    return l

@app.route('/add')
@view('channel/add_channel')
def goto_add_channel():
    return dict(domain=SITE_DOMAIN)

@app.post('/insert')
def insert():
    channel_name = request.params.get('channel_name')
    alias = request.params.get('alias')
    description = request.params.get('description')
    is_fee = request.params.get('is_fee')
    channel_type=request.params.get('channel_type')
    channel_status =request.params.get('channel_status')
    index_display =request.params.get('index_display')

    conn = db.getmysqlconn()
    c = conn.cursor()
    sql = "insert into HNSJ_TDCMS_CHANNEL(Name,Alias,description,status,channeltype,isfee,index_display) \
        values(%s,%s,%s,%s,%s,%s,%s)"
    c.execute(sql,(channel_name,alias,description,channel_status,channel_type,is_fee,index_display))
    conn.commit()
    c.close()
    conn.close()
    return getitems()


@app.route('/delete')
def delete():
    ids=request.query.get('ids')
    conn = db.getmysqlconn()
    c = conn.cursor()
    for one in ids.split('_'):
        print one 
        sql = "delete from HNSJ_TDCMS_CHANNEL where id = %s"
        c.execute(sql,(one))
        conn.commit()
    c.close()
    conn.close()
    return getitems()


@app.route('/tomenu')
def tomenu():
    try:
        menuid= request.query.get('menuid')
        channelids = request.query.get('channelids')

        for cid in channelids.split('_'):
            if cid != '':
                delete_sql = "delete from HNSJ_TDCMS_MENU where parent=%s and path=%s"
                db.update(delete_sql,(menuid,'/chanel/gotochannel?cid='+cid))

                insert_sql = "insert into HNSJ_TDCMS_MENU (menuname,path,parent) values(%s,%s,%s)"
                cname = getchannelnamebyid(cid)
                db.update(insert_sql,(cname,'/channel/gotochannel?cid='+cid,menuid))
        return 'ok'
    except Exception,data:
        traceback.print_exc()
        return 'error'
#---------channel--------------------

@app.route('/gotochannel')
@view('channel/subchannel')
def gotochannel():
    cid = request.query.get('cid')
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

    conn=db.getmysqlconn()
    c= conn.cursor()
    qs = ""
    querylist= []
    # if vid :
    #     qs += ' contentid=%s'
    #     querylist.append(vid)
    # if vtitle :
    #     qs += ' namecn=%s'
    #     querylist.append(vtitle)
    # if 
    print cid,start,end
    sql = "select id,title,cpid,addtime,picurl,itemid from HNSJ_TDCMS_CHANNEL_ITEM  where channelid=%s limit %s,%s"
    c.execute(sql,(cid,start,pagesize))
    l=[]
    for one in c.fetchall():
        l.append(one)
    sqlcount = "select count(*) from HNSJ_TDCMS_CHANNEL_ITEM where channelid=%s"
    c.execute(sqlcount,(cid))
    totalrecord = c.fetchone()[0]
    c.close()
    conn.close()
    totalpage=0
    if totalrecord/pagesize <1:
        totalpage=1
    else:
        totalpage=totalrecord/pagesize

    return dict(all=l,total=totalpage,domain=SITE_DOMAIN,startpage=page)

@app.route('/gotoedit')
@view('channel/edit_video')
def gotoedit():
    vid = request.query.get('id')
    sql = "select itemid,description,picurl,productid,status,title from HNSJ_TDCMS_CHANNEL_ITEM where itemid=%s"
    video = db.query_one(sql,(vid))
    print video
    #-----get product ---------
    sql = "select t1.id ,t1.item_id,t1.product_id,t.sp_productid from HNSJ_VAC_PROINFO t,HNSJ_TDCMS_ITEM_PRODUCT t1 where \
            t.sp_productid = t1.product_id and t1.id = %s"
    p = db.query_list(sql,(video[0]))


    #-----get support cpids----
    sql = "select column_value from HNSJ_SYS_CONFIG where column_name = %s"
    cpids = db.query_one(sql,('SUPPORT_CP_IDS'))[0]
    print cpids
    cpidsql = ','.join(cpids.split(','))
    print cpidsql

    #------get all product------
    sql = "select sp_productid,productname from HNSJ_VAC_PROINFO where spid in (%s)"
    allproductlist = db.query_list(sql,(cpidsql))


    return dict(v = video,domain=SITE_DOMAIN,allproductlist=allproductlist,p=p)


