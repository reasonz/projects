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
#SITE_DOMAIN = 'http://wl.tudou.com/data'
SITE_DOMAIN = 'http://boyajiaoyu.sinaapp.com/'




