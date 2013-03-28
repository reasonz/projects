import time,urllib2,json
import logging,os,sys,traceback
import MySQLdb as db
import threading

reload(sys)
sys.setdefaultencoding('utf-8')

class Mylogger():
    def __init__(self,key,path):
        self.logger = logging.getLogger(key)
        project_path =os.getcwd()
        print project_path
        # file logger
        if not os.path.exists(project_path+path):
            os.mkdir(project_path+path)
        logfile = project_path+path +key +'.log'
        hdlr = logging.FileHandler(logfile)
        formatter = logging.Formatter('%(asctime)s %(name)s  %(message)s')
        hdlr.setLevel(logging.INFO)
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)

        # console logger
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def log(self, msg):
        if self.logger is not None:
            self.logger.info(msg)

class Myjob(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.db=DB    ()
        self.sleeptime=5*60
        self.logger  = Mylogger('gkgpjob','/log/')

    def run(self):
        while True:
            self.processVideo()
            time.sleep(self.sleeptime)
        
    def processVideo(self):
        try:
            sql = "select itemid,itemcode,queryurl  from gkgp_item where status=0"
            l = self.db.query_list(sql,())
            for one in l :
                itemid,itemcode,queryurl = one[0],one[1],one[2]
                print 'check itemid %s,%s,%s' % (itemid,itemcode,queryurl)
                self.logger.log('check itemid %s,%s,%s' % (itemid,itemcode,queryurl))
                if queryurl:
                    res = urllib2.urlopen(queryurl)
                    self.logger.log(res)
                    obj = json.load(res,encoding='utf-8')
                    print obj
                    if obj.get('status')=='finish':
                        iteminfo = self.getitem(itemcode)
                        print iteminfo
                        item= iteminfo.get('multiResult').get('results')
                        if len(item)>0 :
                            subitem = item[0]
                            totaltime=subitem.get('totalTime')
                            playtimes = subitem.get('playTimes')
                            picurl =subitem.get('picUrl')
                            itemurl=subitem.get('itemUrl')
                            outplayurl=subitem.get('outerPlayerUrl')
                            updatesql= 'update gkgp_item set status=1,totaltime=%s,playurl=%s,outerplayurl=%s,playtimes=%s,pics=%s where itemid=%s'
                           
                            params=(totaltime,itemurl,outplayurl,playtimes,picurl,itemid)
                            
                            self.db.update(updatesql,params)
                        else:
                            pass
        except:
            traceback.print_exc()
    def getitem(self,itemcode):
        url='http://api.tudou.com/v3/gw?method=item.info.get&appKey=c58dad0ed452b2d3&format=json&itemCodes=%s' % (itemcode)
        res = urllib2.urlopen(url,'')
        obj= json.load(res,encoding="utf-8")
        return obj
        
class DB    (): 
    def __init__(self):
        # self.host= '10.25.251.101'
        # self.port=10040
        self.host='wl-interface7'
        self.port =3306
        self.username='ssx_dbmanage'
        self.password='ZAQ!4rfv'
        self.dbname='gkgp'

    def getmysqlconn(self):
        return db.connect(host=self.host,port=self.port,user=self.username,passwd=self.password,db=self.dbname,charset="utf8")

    def query_list(self,sql,params):
        conn = self.getmysqlconn()
        c = conn.cursor()
        c.execute(sql,params)
        l=[]
        for one in c.fetchall():
            l.append(one)
        c.close()
        conn.close()
        return l

   

    def query_one(self,sql,params):
        conn = self.getmysqlconn()
        c = conn.cursor()
        c.execute(sql,params)
        
        res = c.fetchone()
        c.close()
        conn.close()
        return res

    def update(self,sql,params):
        conn = self.getmysqlconn()
        c = conn.cursor()
        c.execute(sql,params)
        res = c.fetchone()
        conn.commit()
        c.close()
        conn.close()
        return res

    


if __name__ =='__main__':
    job = Myjob()
    # job.setDaemon(True)
    job.start()