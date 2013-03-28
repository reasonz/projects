#encoding=utf-8
__author__ = 'reason'
from lib.bottle import template,Bottle,request,view
from lib.cachewrap import cache
from dbsetting import dbsetting as db 
import sys,hashlib,traceback,json
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
    sql = "select * from gkgp_channel"
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
    parent_channel = db.query_list('select id,channel_name from gkgp_channel where pid=-1',())
    return dict(domain=SITE_DOMAIN,parent_channel_list= parent_channel)

@app.route('/toupdate')
@view('channel/edit_channel')
def goto_edit_channel():
    parent_channel = db.query_list('select id,channel_name from gkgp_channel where pid=-1',())
    cid= request.query.get('id')
    conn=db.getmysqlconn()
    c = conn.cursor()
    sql = 'select * from gkgp_channel where id=%s'
    c.execute(sql,(cid))
    res = c.fetchone()
    c.close()
    conn.close()
    return dict(channel=res,domain=SITE_DOMAIN,cid=cid,parent_channel_list= parent_channel)

@app.post('/insert')
def insert():
    channel_name = request.params.get('channel_name')
    alias = request.params.get('alias')
    description = request.params.get('description')
    position = request.params.get('position')
    pid=request.params.get('pid')
    channel_type=request.params.get('channel_type')
    channel_status =request.params.get('channel_status')
    index_display =request.params.get('index_display')

    conn = db.getmysqlconn()
    c = conn.cursor()
    sql = "insert into gkgp_channel(channle_name,alias,description,status,channeltype,pid,index_display) \
        values(%s,%s,%s,%s,%s,%s,%s,%s)"
    c.execute(sql,(channel_name,alias,description,channel_status,channel_type,pid,index_display))
    conn.commit()
    c.close()
    conn.close()
    return getitems()

@app.post('/update')
def update():
    channel_name = request.params.get('channel_name')
    alias = request.params.get('alias')
    description = request.params.get('description')
    position = request.params.get('position')
    pid=request.params.get('pid')
    channel_type=request.params.get('channel_type')
    channel_status =request.params.get('channel_status')
    index_display =request.params.get('index_display')
    cid =request.params.get('cid')
    conn = db.getmysqlconn()
    c = conn.cursor()
    sql = "update gkgp_channel set channel_name=%s,alias=%s,description=%s,status=%s,channeltype=%s,pid=%s,index_display=%s where id=%s"
    c.execute(sql,(channel_name,alias,description,channel_status,channel_type,pid,index_display,cid))
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
        sql = "delete from gkgp_channel where id = %s"
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


        flag=False
        for cid in channelids.split('_'):
            if cid != '':
                select_sql = "select count(*) from gkgp_cms_menu where parent=%s and path=%s"
                res = db.query_one(select_sql,(menuid,'/channel/gotochannel?cid='+cid))
                if res[0]>0:
                    flag=True
                    continue
                # delete_sql = "delete from gkgp_cms_menu where parent=%s and path=%s"
                # db.update(delete_sql,(menuid,'/channel/gotochannel?cid='+cid))

                insert_sql = "insert into gkgp_cms_menu (menuname,path,parent) values(%s,%s,%s)"
                cname = getchannelnamebyid(cid)
                db.update(insert_sql,(cname,'/channel/gotochannel?cid='+cid,menuid))
        if flag :
            return "exist"
        else:
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
    qs = " and t.channel_id="+str(cid)
    querylist= []
    query_args={"title":'',"id":'',"start":'',"end":'',"channelid":str(cid)}
    if vid and len(vid)>0:
        qs += " and  itemid='"+vid + "'"
        query_args['id']=vid
        
    if vtitle and len(vtitle)>0:
        qs += " and title='"+ vtitle + "'"
        query_args['title']=vtitle
        
    if vstart and vend and len(vstart)>0 and len(vend)>0:
        qs += " and addtime >='"+vstart + "' and addtime <='" + vend +"'"
        query_args['start']=vstart
        query_args['end']=vend
    print cid,start,end

    sql = "select t1.id,t1.itemcode,t1.title,t1.addtime,t1.pics,t1.playtimes,t2.channel_name \
    from gkgp_channel_item_link t ,gkgp_item t1 ,gkgp_channel t2 \
    where t.item_id = t1.id and t.channel_id = t2.id  "+qs+"  limit %s,%s"
    print sql
    c.execute(sql,(start,pagesize))
    l=[]
    for one in c.fetchall():
        l.append(one)
    sqlcount = "select count(*) \
    from gkgp_channel_item_link t ,gkgp_item t1 ,gkgp_channel t2 \
    where t.item_id = t1.id and t.channel_id = t2.id "+qs
    c.execute(sqlcount,()) 
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
   
    return dict(all=l,total=totalpage,domain=SITE_DOMAIN,startpage=page,query_args=query_args)

@app.route('/gotoedit')
@view('channel/edit_video')
def gotoedit():
    vid = request.query.get('id')
    con = db.getmysqlconn()
    c = con.cursor()

    sql = "select itemid,description,picurl,productid,status,title,bigpicurl from gkgp_channel_ITEM where itemid=%s"
    c.execute(sql,(vid))
    video = c.fetchone()
    print video
    #-----get product ---------
    sql = "select t1.id ,t1.item_id,t1.product_id,t.sp_productid,t.ProductName from HNSJ_VAC_PROINFO t,HNSJ_TDCMS_ITEM_PRODUCT t1 where \
            t.sp_productid = t1.product_id and t1.item_id = %s"
    c.execute(sql,(video[0]))
    p=[]
    for one in c.fetchall():
        p.append(one)


    #-----get support cpids----
    sql = "select column_value from HNSJ_SYS_CONFIG where column_name = %s"
    c.execute(sql,('SUPPORT_CP_IDS'))
    cpids =  c.fetchone()[0]
    print cpids
    cpidsql = ','.join(cpids.split(','))
    print cpidsql

    #------get all product------
    sql = "select sp_productid,productname from HNSJ_VAC_PROINFO where spid in (%s)"
    c.execute(sql,(cpidsql))
    allproductlist=[]
    for one in c.fetchall():
        allproductlist.append(one)
    c.close()
    con.close()

    return dict(v = video,domain=SITE_DOMAIN,allproductlist=allproductlist,p=p,itemid=vid)

@app.post('/edit_video')
def edit_video():
    itemid=request.params.get('itemid') 
    title= request.params.get('title')
    description = request.params.get('description')
    status = request.params.get('status')
    productids=request.params.get('productids')
    #------load pic-------------
    bigpic = request.files.bigpic
    

    print itemid,title,description,status,productids
    conn = db.getmysqlconn()
    c = conn.cursor()
    imgurl=""
    
    if  bigpic and len(row)>0 and bigpic.filename:
        row = bigpic.file.read()
        print len(row),bigpic.filename
        f= open('/home/tdwl/pyserver/cms/static/upload_img/'+bigpic.filename,'wb')
        f.write(row)
        imgurl = "bigpicurl='/static/upload_img/"+bigpic.filename+"' ,"
        f.close()
    print imgurl
    #------------update channel_item-----------
    sql = "update gkgp_channel_ITEM set  title='"+title+"' , description='"+description+"', "+imgurl+" status=%s where itemid=%s"
    c.execute(sql,(status,itemid))

    sql = "delete from HNSJ_TDCMS_ITEM_PRODUCT where ITEM_ID=%s"
    print itemid
    c.execute(sql,(itemid)) 

    for one in productids.split('_'):
        if one =="":
            pass 
        else:
            sql="insert into HNSJ_TDCMS_ITEM_PRODUCT(item_id,product_id,p_status) values(%s,%s,%s)"
            c.execute(sql,(itemid,one,1))
    conn.commit()
    c.close()
    conn.close()
    
    request.query['id']=itemid
    return gotoedit()

@app.route('/publish')
def publish():
    ids = request.query.get('ids')
    cid = request.query.get('channelid')
    conn = db.getmysqlconn()
    c=conn.cursor()
    flag=False
    noproductvideo=[]
    for one in ids.split('_'):

        if len(one)==0:
            continue
        sql = "select item_id from HNSJ_TDCMS_ITEM_PRODUCT where item_id=%s"
        c.execute(sql,(one))
        res = c.fetchall() 
        print 'chaxun jieguo %s' % (len(res))
        if len(res)==0:
            noproductvideo.append(one)
            flag=True

    if flag: 
        d={}
        d['stat']='exist'
        d['data']=','.join(noproductvideo)
        c.close() 
        conn.close()

        return json.dumps(d)
    else:
        d={}
        try:
            for one in ids.split('_'):
                if len(one)==0:
                    continue
                sql = 'update gkgp_channel_ITEM set status=1 where itemid=%s and channelid=%s'
                c.execute(sql,(one,cid))
            conn.commit()
            d['stat']='ok'
            return json.dumps(d)
        except:
            return json.dumps({'stat':'error'})
        finally:
            c.close()
            conn.close()


@app.route('/unpublish')
def publish():
    ids = request.query.get('ids')
    cid = request.query.get('channelid')
    conn = db.getmysqlconn()
    c=conn.cursor()
    try:
        for one in ids.split('_'):
            if len(one)==0:
                pass
            sql = 'update gkgp_channel_ITEM set status=0 where itemid=%s and channelid=%s'
            c.execute(sql,(one,cid))
        conn.commit()
        d={}
        d['stat']='ok'
        return json.dumps(d)
    except:
        traceback.print_exc()
        return json.dumps({'stat':'error'})
    finally:
        c.close()
        conn.close()

