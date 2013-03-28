#__author__ = 'reason'
#from lib.bottle import Bottle,request
#from dbsetting import dbsetting as db
#import sys,logging
#from mylogger   import  Mylogger
#from setting import pwd
#reload(sys)
#sys.setdefaultencoding('utf-8')
#app = Bottle()
#loggers = {}
#apiproperties={}
#def initapiproperties():
#    conn = db.getmysqlconn()
#    sql = "select id,pid,bid,path,stat from apimanage"
#    c = conn.cursor()
#    c.execute(sql)
#    for one in c.fetchall():
#        key =  str(one[1])+'_'+str(one[2])
#        value = {'pid':str(one[1]),'bid':str(one[2]),'path':str(one[3]),'stat':str(one[4])}
#        apiproperties[key]=  value
#    c.close()
#    conn.close()
#
#initapiproperties()
#
#@app.post('/rp')
#def datarp():
#    pid = request.forms.get('pid')
#    bid =  request.forms.get('bid')
#    data= request.forms.get('data')
#    key = str(pid)+'_'+str(bid)
#    print key ,data
#    p = apiproperties.get(key,None)
#    if p and p.get('stat')=="1":
#        logger=  logging.getLogger(key)
#        print loggers
#        if logger:
#            print 'print log',logger
#            logger.info(data)
#        else:
#            logger = Mylogger(p.get('pid')+'_'+p.get('bid'),pwd+'/' + p.get('path'))
#
#            logger.info(data)
#            loggers[key]=logger
#
#for o in apiproperties:
#    p = apiproperties.get(o)
#
#    logger = Mylogger(p.get('pid')+'_'+p.get('bid'),pwd+'/' + p.get('path'))
#    logger.log("this is " +o )
#
#@app.route('/rptest/:pid/:bid/:data')
#def rptest(pid,bid,data):
#    log = logging.getLogger()
#    log.info(data + bid)
#
#
#
#
#
