#coding:utf-8
from bottle import Bottle,static_file
import sae
import urllib2
import MySQLdb as db
import sys,json
from bs4 import BeautifulSoup as bs
import cnbetare
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('bs4')
app = Bottle()

@app.route('/test')
def test():
    try:
        page = urllib2.urlopen('http://www.cnbeta.com/index.php#1') 
        soup = bs(page)
        d = soup.title
        return d
    except Excetion,e:
        print e
@app.route('/testurl/:p')
def testurl(p):
    return '<b>test.....sadfasdfa.zpzhang...</b>',p

@app.route('/testdb')
def testdb():
    try:
        conn = db.connect(host='w.rdc.sae.sina.com.cn',port=3307,user='w4z445j54z',passwd='jllx005li3l5j2jl12x35kmlk3mx34k0ijkmz0mx',db='app_reasonz',charset='utf8')
        c=conn.cursor()
        c.execute('select * from wp_posts')
        res=c.fetchall()
        l=[]
        for one in res:
            print type(one[0])
            for oo in one:
                l.append(str(oo))
        c.close()
        conn.close()
        return json.dumps(l,ensure_ascii=False)
    except Exception,e:
        print 'error'
        print e

@app.route('/insertpost')
def run():
    try:
        #return cnbeta.cnbetamain()
        return cnbetare.addpost()

    except:
        print sys.exc_info()[0],sys.exc_info()[1]
        print 'error'
application = sae.create_wsgi_app(app,debug=True)
 
