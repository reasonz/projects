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


@app.route('/getnotice')
@view('options/add_note')
def getnotice():
    d={}
    sql = 'select id,column_value from HNSJ_SYS_CONFIG WHERE column_name=%s'
    params=('MARQUEE_NOTE')
    res = db.query_one(sql,params)
    print res
    d['note_id'] = res[0]
    d['note_value'] =res[1]
    return dict(note=d,domain=SITE_DOMAIN)


@app.post('/updatenote')
def updatenote():
    note_id = request.params.get('note_id')
    note_value=request.params.get('note_value')
    print note_value
    sql = 'update HNSJ_SYS_CONFIG set column_value=%s where id=%s'
    params=(note_value,note_id)
    res = db.update(sql,params)
    print res
    return getnotice()


    