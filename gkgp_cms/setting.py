__author__ = 'reason'
import sys
from os.path import abspath, dirname, join
sys.path.insert(0, abspath(dirname(__file__)))
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

pwd = dirname(__file__) 
print pwd
TEM_PATH = pwd + '/views/'
STATIC_PATH = pwd + '/static/'
# SITE_DOMAIN = 'http://61.158.153.25/cms' 		
SITE_DOMAIN = 'http://10.151.20.49:7070'
PLAY_VIDEO_DOMAIN = 'http://10.151.20.49:9090'



#db setting
host='10.25.251.101'
port=10040
password='ZAQ!4rfv'
username='ssx_dbmanage'
dbname='gkgp'
