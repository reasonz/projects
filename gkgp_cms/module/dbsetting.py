__author__ = 'reason'
import MySQLdb   as db
from setting import host,port,username,password,dbname
import traceback
class DBsetting(): 

    def __init__(self):
        self.host= host
        self.port=port
        self.username=username
        self.password=password
        self.dbname=dbname


    def getmysqlconn(self):
        return db.connect(host=self.host,port=self.port,user=self.username,passwd=self.password,db=self.dbname,charset="utf8")

    def query_list(self,sql,params):
        try:
            conn = self.getmysqlconn()
            c = conn.cursor()
            c.execute(sql,params)
            l=[]
            for one in c.fetchall():
                l.append(one)
            return l
        except:
            traceback.print_exc()
        finally:
            c.close()
            conn.close()
   

    def query_one(self,sql,params):
        try:
            conn = self.getmysqlconn()
            c = conn.cursor()
            c.execute(sql,params)
            res = c.fetchone()
            return res
        except:
            traceback.print_exc()
        finally:
            c.close()
            conn.close()

    def update(self,sql,params):
        try:
            conn = self.getmysqlconn()
            c = conn.cursor()
            c.execute(sql,params)
            res = c.fetchone()
            conn.commit()
            return res
        except:
            traceback.print_exc()

        finally:
            c.close()
            conn.close()

    def delete(self,sql,params):
        try:
            conn = self.getmysqlconn()
            c = conn.cursor()
            c.execute(sql,params)
            conn.commit()
        except:
            traceback.print_exc()
        finally:
            c.close()
            conn.close()

dbsetting = DBsetting()
