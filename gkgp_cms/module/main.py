#encoding=utf-8
# index page setting
__author__ = 'reason'
from lib.bottle import template,Bottle,request
from lib.cachewrap import cache
from dbsetting import dbsetting as db
import sys,hashlib,traceback,os,time
from setting import SITE_DOMAIN,STATIC_PATH
reload(sys)
sys.setdefaultencoding('utf-8')

app = Bottle()
moduledict = {'1':'焦点图','2':'热门影院','3':'G客盛典','4':'G客校园行','5':'排行','6':'G客特写','7':'G客联盟'}
itemdict = {'1':'视频','2':'链接'}
@app.route('/gotoindexsetting')
def gotoindexsetting():
    moduleid = request.query.get('moduleid')
    if not moduleid :
        moduleid = 1
    settings = db.query_list('select * from gkgp_main_setting where module=%s',(moduleid))

    return template('main/main_list',dict(moduledict=moduledict,domain=SITE_DOMAIN,index_settings=settings),selectmodule=moduleid,itemdict=itemdict)

@app.route('/gotoadd')
def gotoadd():
    moduleid = request.query.get('moduleid')
    print moduleid
    return template('main/main_add',dict(domain=SITE_DOMAIN,itemdict=itemdict,selectmodule=moduleid,moduledict=moduledict))

@app.route('/gotoedit')
def gotoedit():
    ids = request.query.get('id')
    moduleid = request.query.get('moduleid')
    id=ids.split('_')[0]
    item = db.query_one('select * from gkgp_main_setting where id = %s',(id))
    return template('main/main_edit',dict(domain=SITE_DOMAIN,itemdict=itemdict,selectmodule=moduleid,moduledict=moduledict,item=item))

@app.post('/add')
def add():
    try:
        title = request.params.get('title')
        brif_desc = request.params.get('brif_desc')
        description = request.params.get('description')
        item_type = request.params.get('item_type')
        item_code = request.params.get('item_code')
        link_url = request.params.get('link_url')
        position = request.params.get('position')
        small_pic = request.files.small_pic
        big_pic = request.files.big_pic
        module = request.params.get('module')
        timeflag = str(time.time())
        big_pic_url=""
        if  big_pic!='' and    big_pic.filename:
            row = big_pic.file.read()
            name, ext = os.path.splitext(big_pic.filename)
            
            if ext not in ('.png','.jpg','.jpeg','.gif'):
                return 'File extension not allowed.'
            # big_pic.save(STATIC_PATH+'/upload_img/'+big_pic.filename)
            f= open(STATIC_PATH+'upload_img/big_'+name+'_'+timeflag + ext,'wb')
            f.write(row)
            big_pic_url = "upload_img/big_"+name+'_'+timeflag + ext
            f.close()
       
        small_pic_url=""
        if  small_pic !=''  and  small_pic.filename:
            row = small_pic.file.read()
            name, ext = os.path.splitext(small_pic.filename)
            if ext not in ('.png','.jpg','.jpeg','.gif'):
                return 'File extension not allowed.'
            # small_pic.save(STATIC_PATH+'/upload_img/'+small_pic.filename)
            f= open(STATIC_PATH+'upload_img/small_'+name +'_'+ timeflag + ext,'wb')
            f.write(row)
            small_pic_url = "upload_img/small_"+name+'_'+timeflag + ext
            f.close()
        
        insert_sql = 'insert into gkgp_main_setting (title,brif_desc,description,item_type,item_code,link_url,position,small_pic,big_pic,module) \
                        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        db.update(insert_sql,(title,brif_desc,description,item_type,item_code,link_url,position,small_pic_url,big_pic_url,module))
        # request.query['typeid']=module
        return gotoindexsetting()
    except:
        traceback.print_exc()
        return "error"


@app.post('/edit')
def add():
    try:
        title = request.params.get('title')
        tid= request.params.get('id')
        brif_desc = request.params.get('brif_desc')
        description = request.params.get('description')
        item_type = request.params.get('item_type')
        item_code = request.params.get('item_code')
        link_url = request.params.get('link_url')
        position = request.params.get('position')
        smallpicname = request.params.get('smallpicname')
        bigpicname = request.params.get('bigpicname')
        small_pic = request.files.small_pic
        big_pic = request.files.big_pic
        module = request.params.get('module')
        print title
        big_pic_url=""
        timeflag = str(time.time())
        if  big_pic!='' and   big_pic.file:
            row = big_pic.file.read()
            name, ext = os.path.splitext(big_pic.filename)
            
            if ext not in ('.png','.jpg','.jpeg','.gif'):
                return 'File extension not allowed.'
            # big_pic.save(STATIC_PATH+'/upload_img/'+big_pic.filename)
            f= open(STATIC_PATH+'upload_img/big_'+name+'_'+timeflag + ext,'wb')
            f.write(row)
            big_pic_url = "upload_img/big_"+name+'_'+timeflag + ext
            f.close()
            try:
                os.remove(STATIC_PATH+ bigpicname)
            except:
                traceback.print_exc()
        else:
            big_pic_url = bigpicname

        small_pic_url=""
        if  small_pic !=''  and  small_pic.file:
            row = small_pic.file.read()
            name, ext = os.path.splitext(small_pic.filename)
            if ext not in ('.png','.jpg','.jpeg','.gif'):
                return 'File extension not allowed.'
            # small_pic.save(STATIC_PATH+'/upload_img/'+small_pic.filename)
            f= open(STATIC_PATH+'upload_img/small_'+name+'_'+timeflag + ext,'wb')
            f.write(row)
            small_pic_url = "upload_img/small_"+name+'_'+timeflag + ext
            f.close()
            try:
                os.remove(STATIC_PATH+ smallpicname)
            except:
                traceback.print_exc()
        else:
            small_pic_url=smallpicname
        print tid
        update_sql = 'update gkgp_main_setting set title=%s, brif_desc=%s,description=%s,item_type=%s,item_code=%s,link_url=%s,\
        position=%s,small_pic=%s,big_pic=%s,module=%s where id=%s'

        db.update(update_sql,(title,brif_desc,description,item_type,item_code,link_url,position,small_pic_url,big_pic_url,module,tid))
        request.query['moduleid']=module
        return gotoindexsetting()
    except:
        traceback.print_exc()
        return "修改错误"

@app.route('/delete')
def delete():
    id = request.query.get('id')
    try:

        if id.index(',')!=-1:
            id = id[0:-1]
        ids = id.split(',')
        #print ids
        if 0 < len(ids):
            for i in range(len(ids)):
                item = db.query_one('select id,small_pic,big_pic from gkgp_main_setting where id =%s',ids[i])
                #print item
                if item[1] is not  None and len(item[1])>0  and os.path.exists(STATIC_PATH+item[1]):
                    os.remove(STATIC_PATH+item[1])
                if  item[2] is not None and len(item[2])>0 and os.path.exists(STATIC_PATH+item[2]):
                    os.remove(STATIC_PATH+item[2])
                db.delete('delete from gkgp_main_setting where id = %s',item[0])
            return gotoindexsetting()
    except:
        traceback.print_exc()
        return "delete index setting error"
