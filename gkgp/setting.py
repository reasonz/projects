__author__ = 'reason'
import sys
from os.path import abspath, dirname, join
sys.path.insert(0, abspath(dirname(__file__)))
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

debug=True



project_path = dirname(__file__) 
print project_path
TEM_PATH = project_path + '/views/'
STATIC_PATH = project_path + '/static/'
if debug:
    SITE_DOMAIN = 'http://10.151.20.39:9090'
    PIC_DOMAIN = 'http://10.151.20.49:7070/static'
    # remote api setting
    username='gkgp_cmcc@163.com'
    pwd='ZAQ!xsw2'
    #username='wang-zhiqi@qq.com'
    #pwd='yocoyoco6798010'
    tudouuserId =119029329
    addvideoinfoUrl='http://wwwtest.tudou.com/my/programs/service/updateItem.action?'
    appkey='c58dad0ed452b2d3'
    open_api_url='http://api.tudou.com/v3/gw'
    SECRET_KEY="gkgp_tudou"
    UID="UID"
    VREYCODE = "VREYCODE"

    #db setting
    db_host='10.25.251.101'
    db_port=10040
    db_password='ZAQ!4rfv'
    db_username='ssx_dbmanage'
    dbname='gkgp'

    # memcache setting
    MEMCACHE_HOST=['10.151.20.49:11211']
else:
    SITE_DOMAIN='http://gkgp.m.tudou.com'
    PIC_DOMAIN = 'http://cms.gkgp.intra.tudou.com/static'

    # remote api setting
    # username='gkgp_cmcc@163.com'
    #pwd='ZAQ!xsw2'
    username='wang-zhiqi@qq.com'
    pwd='yocoyoco6798010'
    tudouuserId = 90345247
    addvideoinfoUrl='http://www.tudou.com/my/programs/service/updateItem.action?'
    appkey='c58dad0ed452b2d3'
    open_api_url='http://api.tudou.com/v3/gw'
    SECRET_KEY="gkgp_tudou"
    UID="UID"
    VREYCODE = "VREYCODE"

    # dbsetting
    db_host='wl-interface7'
    db_port=3306
    db_password='ZAQ!4rfv'
    db_username='ssx_dbmanage'
    dbname='gkgp'

    # memcache setting
    MEMCACHE_HOST=['wl-interface4:11211','wl-interface5:11211']




