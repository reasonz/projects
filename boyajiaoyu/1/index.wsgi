from bottle import Bottle,static_file
import sae
import urllib2
import MySQLdb as db
import sys,json
from module import app
reload(sys)
sys.setdefaultencoding('utf-8')

@app.route('/static/<filename:path>')
def static(filename):
    return static_file(filename,'./static/')


application = sae.create_wsgi_app(app,debug=True)