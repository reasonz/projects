__author__ = 'reason'
import MySQLdb   as db


class DBsetting(): 
    # host='wl-interface7'
    # port=3306
    host='10.68.49.11'
    port=3306
    password='tdwl'
    username='tdwl'
    dbname='hnsj'
   
    def getmysqlconn(__self__):
        return db.connect(host=__self__.host,port=__self__.port,user=__self__.username,passwd=__self__.password,db=__self__.dbname,charset="utf8")

    def query_list(__self__,sql,params):
        conn = __self__.getmysqlconn()
        c = conn.cursor()
        c.execute(sql,params)
        l=[]
        for one in c.fetchall():
            l.append(one)
        c.close()
        conn.close()
        return l

   

    def query_one(__self__,sql,params):
        conn = __self__.getmysqlconn()
        c = conn.cursor()
        c.execute(sql,params)
        
        res = c.fetchone()
        c.close()
        conn.close()
        return res

    def update(__self__,sql,params):
        conn = __self__.getmysqlconn()
        c = conn.cursor()
        c.execute(sql,params)
        res = c.fetchone()
        conn.commit()
        c.close()
        conn.close()
        return res

    

dbsetting = DBsetting()
