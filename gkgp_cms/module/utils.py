from dbsetting import dbsetting as db
import sys,hashlib
from setting import    SITE_DOMAIN
reload(sys)
from lib.cachewrap import cache_const,update_cache
sys.setdefaultencoding('utf-8')

# @cache_const
def getallchannel():
    sql = "select id,channel_name from gkgp_channel"
    return db.query_list(sql,())
# @cache_const
def getallmenu():
	sql = "select id,menuname from gkgp_cms_menu where parent=-1"
	return db.query_list(sql,())


def getchannelnamebyid(id):
	sql = "select channel_name from gkgp_channel where id = %s"
	return db.query_one(sql,(id))[0]



def update_cache():
	key=['getallchannel','getallmenu','getallcpid']
	for o in key:
		update_cache('cache'+o)

