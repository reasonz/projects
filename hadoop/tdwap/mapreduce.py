#encoding=utf-8
import os
import MySQLdb as mdb
logtype = ['shunicom']
logpath = '~/syncshunionlog/'
shellpath = '~/hadoop/tdwap/mp/'
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


def visit(day):
    l=getres('tudou_sp.log_'+day+'.log','shunicom')
    for one in l:
        keys=one.split('\t\t')[0]
        count=one.split('\t\t')[1]
        w=keys.split('\t')
       	day=w[0]
	project=w[1]
	phone=w[2]
	#ip=w[3]
	wapver=w[3]
	net=w[4]

	c=conn.cursor() 
        sql = """insert into shunicom_visit (day,project,phone,wapver,net,count) values(%s,%s,%s,%s,%s,%s)"""
        param=(day,project,phone,wapver,net,count)
        c.execute(sql,param)
        conn.commit()
        #print keys
        c.close()

def run():
    import time,datetime
    t=datetime.datetime.now()-datetime.timedelta(days=1)
    day=str(t.date())
    print day
    visit(day)

def runday():
   import time,datetime
   for d in range(1,2):
	t=datetime.datetime.now()-datetime.timedelta(days=d)
	day=str(t.date())
	print day
	visit(day)
run()
#runday()
