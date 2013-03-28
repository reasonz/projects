#encoding=utf-8
__author__ = 'reason'
from lib.bottle import template,Bottle,request,view
from lib.cachewrap import cache
from dbsetting import dbsetting as db
import sys,hashlib
from setting import    SITE_DOMAIN
reload(sys)
sys.setdefaultencoding('utf-8')

app = Bottle()


@app.route('/setting')
@view('options/template')
def getsysconfig():
    return dict(sysconfig=getsys(),domain=SITE_DOMAIN)

def getsys():
    d={}
    sql = 'select * from HNSJ_SYS_CONFIG where table_name=%s'
    l = db.query_list(sql,('DESIGN'))    
    for one in l :
        sub  = {}
        sub['id']=one[0]
        sub['title']=one[4]
        sub['value']=one[3]
        d[one[2]] =sub
    
    return d


@app.post('/update')
def updatenote():
    config_id = request.params.get('config_id')
    config_value=request.params.get('config_value')
    print config_value
    sql = 'update HNSJ_SYS_CONFIG set column_value=%s where id=%s'
    params=(config_value,config_id)
    res = db.update(sql,params)
    print res
    return getsysconfig()
