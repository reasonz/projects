__author__ = 'reason'
import MySQLdb   as db
import cx_Oracle as cx

class DBsetting():
    host='wl-interface7'
    port=3306
    # host='10.25.251.101'
    # port=10040
    password='ZAQ!4rfv'
    username='ssx_dbmanage'
    dbname='wldata'
    cmsdbname='wlcms'
    nokiadbname='nokiadata'
    oraclehost='10.25.20.55:9003/TDWLP3.TUDOU.COM'
    # oraclehost='10.25.251.101:9003/TDWLP3.TUDOU.COM'
    oraclepassword='k!U99?268x'
    oracledbname='tdfwapdb'

    def getconn(__self__):
        return cx.connect(__self__.oracledbname,__self__.oraclepassword,__self__.oraclehost)

    def getmysqlconn(__self__):
        return db.connect(host=__self__.host,port=__self__.port,user=__self__.username,passwd=__self__.password,db=__self__.dbname,charset="utf8")

    def getcmsconn(__self__):
         return db.connect(host=__self__.host,port=__self__.port,user=__self__.username,passwd=__self__.password,db=__self__.cmsdbname,charset="utf8")

    def getnokiaconn(__self__):
         return db.connect(host=__self__.host,port=__self__.port,user=__self__.username,passwd=__self__.password,db=__self__.nokiadbname,charset="utf8")

dbsetting = DBsetting()
