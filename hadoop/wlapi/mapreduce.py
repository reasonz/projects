#encoding=utf-8
import os
import MySQLdb as mdb
logtype = ['wlapi','wlapi_pv']
logpath = '~/syncwlapilog/'
shellpath = '~/hadoop/wlapi/mp/'
conn= mdb.connect(host='wl-interface7',port=3306,user='ssx_dbmanage',passwd='ZAQ!4rfv',db='wldata',charset='utf8')

def runcmd(cmd):
    l=[]
    for one in  os.popen(cmd).readlines():
	l.append(one)
    return l	
    
def createshell(type):
    return 'python ' + shellpath + type + '/m.py | sort | python '+ shellpath + type +'/r.py'

#run shell 
def getres(fname,type):
    cmd = 'cat ' + logpath +'/' + fname + ' | ' + createshell(type)
    print cmd
    l=runcmd(cmd)
    #for o in l :
    #	print o
    return l


def method(day):
    l=getres('log.'+day,'wlapi')
    c=conn.cursor()
    delmethod="""delete from wl_api_all where day=%s"""
    delall="""delete from wl_api_method where day=%s"""
    param=(day)
    c.execute(delmethod,param)
    c.execute(delall,param)
    conn.commit()

    for one in l:
	w=one.split('\t')
	method=w[0]
	
	if method=='methodavgcount':
	    avg=w[1]
	    pv = w[2]
	    uv=w[3]
	    ip=w[4]
            sql = """insert into wl_api_all (avgcosttime,pv,uv,ip,day) values(%s,%s,%s,%s,%s)"""
            param=(avg,pv,uv,ip,day)
            c.execute(sql,param)
	    conn.commit()
	else:
	    count = w[1]
	    usetime = w[2]
	    preuse=w[3] 
            sql = """insert into wl_api_method (apiname,count,usetime,day,preusetime) values(%s,%s,%s,%s,%s)"""
            param=(method,count,usetime,day,preuse)
            c.execute(sql,param)
            conn.commit()
            #print keys
    c.close()



def run():
    import time,datetime
    t=datetime.datetime.now()-datetime.timedelta(days=1)
    day=str(t.date())
    print day
    method(day)
def runday():
   import time,datetime
   for d in range(2,7):
	t=datetime.datetime.now()-datetime.timedelta(days=d)
	day=str(t.date())
	print day
	method(day)
run()
#runday()
