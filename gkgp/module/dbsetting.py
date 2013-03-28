__author__ = 'reason'
import MySQLdb   as db
from setting import db_host,db_port,db_username,db_password,dbname

class DBsetting(): 

    def __init__(self):
        self.host= db_host
        self.port=db_port
        self.username=db_username
        self.password=db_password
        self.dbname=dbname


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
        res = conn.insert_id()
        conn.commit()
        c.close()
        conn.close()
        return res

    

dbsetting = DBsetting()
