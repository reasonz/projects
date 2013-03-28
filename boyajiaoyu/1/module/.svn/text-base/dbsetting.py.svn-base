__author__ = 'reason'
import MySQLdb   as db


class DBsetting():
    host='192.168.1.6'
    port=3306
    password='root'
    username='root'
    dbname='boya'
    
    def getmysqlconn(__self__):
        return db.connect(host=__self__.host,port=__self__.port,user=__self__.username,passwd=__self__.password,db=__self__.dbname,charset="utf8")



    
dbsetting = DBsetting()
