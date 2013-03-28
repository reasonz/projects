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
SITE_DOMAIN = 'http://61.158.153.25/cms'
# SITE_DOMAIN = 'http://10.151.20.48:9990'




