__author__ = 'reason'
import urllib
import urllib2
import cookielib
import time
#response = urllib2.urlopen('http://10.151.20.48:9990/api/rptest/1000/2/21312312312313')
#html = response.read()
#print html

import logging
import logging.config
import dictconfig
log_setting = {
    'version': 1,
    'root': {
        'level':'debug' ,
        'hanlders': ['file']
    },
    'hanlders': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'detailed',
            'filename': '../MyProject.log',
            'mode': 'a',
            'maxBytes': 10485760,
            'backupCount': 5,
            }
    },
    'formatters': {
        'detailed': {
            'format': '%(asctime)s %(module)-17s line:%(lineno)-4d %(levelname)-8s %(message)s',
            }}
}
logging.config.dictConfig(log_setting)
#create logger
logging.debug("22")

