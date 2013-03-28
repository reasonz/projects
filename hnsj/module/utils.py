from dbsetting import dbsetting as db
import sys,hashlib
from setting import    SITE_DOMAIN
reload(sys)
sys.setdefaultencoding('utf-8')

def getallchannel():
    sql = "select id,name from HNSJ_TDCMS_CHANNEL"
    return db.query_list(sql,())

def getallmenu():
	sql = "select id,menuname from HNSJ_TDCMS_MENU where parent=-1"
	return db.query_list(sql,())

def getchannelnamebyid(id):
	sql = "select name from HNSJ_TDCMS_CHANNEL where id = %s"
	return db.query_one(sql,(id))[0]
