#encoding=utf-8
import os
import MySQLdb as mdb
logtype = ['column','fee','item','search','signin','topkeyword','videostat']
logpath = '~/synclog/'
shellpath = '~/hadoop/python/mp/'
import sys
sys.path.append(shellpath +'lib/')
conn= mdb.connect(host='wl-interface7',port=3306,user='ssx_dbmanage',passwd='ZAQ!4rfv',db='nokiadata',charset='utf8')
 

def runcmd(cmd):
    l=[]
    for one in  os.popen(cmd).readlines():
	l.append(one)
    return l	
    
def createshell(type):
    return 'python ' + shellpath + type + '/m.py | sort | python '+ shellpath + type +'/r.py'

#run shell 
def getres(fname,type,projid):
    cmd = 'cat ' + logpath + projid + '/' + type +'/' + fname + ' | ' + createshell(type)
    print cmd
    l=runcmd(cmd)
    #for o in l :
    #	print o
    return l


def signin(day):
    l=getres('log.log.'+day,'signin','1041')
    c=conn.cursor() 
    for one in l:
        keys=one.split('\t\t')[0]
        count=one.split('\t\t')[1]
        w=keys.split('\t')
        #print len(w)	
        ci = w[0]
        proj=w[1]
        pf=w[2]
        subpf=w[3]
        chid=w[4]
        ver=w[5]
        ua=w[6]
        net=w[7]
        area=w[8]
        isnew=w[9]
        #print ci,area
        sql = """insert into signin (ci,proid,chid,ua,area,plat,sub,version,isnew,count,addtime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        param=(ci,int(proj),int(chid),ua,area,pf,subpf,ver,isnew,int(count),day)
        print param
        c.execute(sql,param)
        conn.commit()
        #print keys
    c.close()

def videostat(day):
    l=getres('log.log.'+day,'videostat','1041')
    c=conn.cursor() 
    for one in l:
        keys=one.split('\t\t')[0]
        count=one.split('\t\t')[1]
        w=keys.split('\t')
        #print len(w)	
        ci = w[0]
        proj=w[1]
        pf=w[2]
        subpf=w[3]
        chid=w[4]
        ver=w[5]
        ua=w[6]
        net=w[7]
        area=w[8]
        type=w[9]
	channel=w[10]
        #print ci,area
        sql = """insert into videostate(ci,proj,pf,subpf,chid,ver,ua,net,area,type,count,addtime,channel) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        param=(ci,proj,pf,subpf,chid,ver,ua,net,area,type,int(count),day,channel)
        print sql,param
        c.execute(sql,param)
        conn.commit()
        #print keys
    c.close()


def fee(day):
    l=getres('log.log.'+day,'fee','1041')
    c=conn.cursor() 
    for one in l:
        keys=one.split('\t\t')[0]
        count=one.split('\t\t')[1]
        w=keys.split('\t')
        #print len(w)	
        ci = w[0]
        proj=w[1]
        pf=w[2]
        subpf=w[3]
        chid=w[4]
        ver=w[5]
        ua=w[6]
        net=w[7]
        area=w[8]
        itemid=w[9]
	channel=w[10]
	feetype=w[11]
	feestat=w[12]
	price=w[13]
	support=w[14]
        #print ci,area
        sql = """insert into fee(ci,proj,pf,subpf,chid,ver,ua,net,area,itemid,channelid,feetype,feestat,price,support,addtime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        param=(ci,proj,pf,subpf,chid,ver,ua,net,area,itemid,channel,feetype,feestat,int(price),support,day)
        print sql,param
        c.execute(sql,param)
        conn.commit()
        #print keys
    c.close()


def search(day):
    l=getres('log.log.'+day,'search','1041')
    c=conn.cursor() 
    for one in l:
        keys=one.split('\t\t')[0]
        count=one.split('\t\t')[1]
        w=keys.split('\t')
        #print len(w)	
        proj=w[0]
        pf=w[1]
        subpf=w[2]
        chid=w[3]
        keyword=w[4]
        #print ci,area
        sql = """insert into search(proj,pf,subpf,chid,keyword,addtime,count) values(%s,%s,%s,%s,%s,%s,%s)"""
        param=(proj,pf,subpf,chid,keyword,day,count)
        print sql,param
        c.execute(sql,param)
        conn.commit()
        #print keys
    c.close()


def column(day):
    l=getres('log.log.'+day,'column','1041')
    c=conn.cursor() 
    for one in l:
        keys=one.split('\t\t')[0]
        count=one.split('\t\t')[1]
        w=keys.split('\t')
        #print len(w)	
	proj=w[0]
	pf=w[1]
	subpf=w[2]
	chid=w[3]
	ver=w[4]
	ua=w[5]
	net=w[6]
	area=w[7]
	channel=w[8]
	
        #print ci,area
        sql = """insert into channel(proj,pf,subpf,chid,ver,ua,net,area,channel,addtime,count) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        param=(proj,pf,subpf,chid,ver,ua,net,area,channel,day,int(count))
        print sql,param
        c.execute(sql,param)
        conn.commit()
        #print keys
    c.close()


def iteminfo(day):
    l=getres('log.log.'+day,'item','1041')
    c=conn.cursor() 
    for one in l:
        keys=one.split('\t\t')[0]
        count=one.split('\t\t')[1]
        w=keys.split('\t')
        #print len(w)	
	proj=w[0]
	pf=w[1]
	subpf=w[2]
	chid=w[3]
	ver=w[4]
	ua=w[5]
	net=w[6]
	area=w[7]
	itemid=w[8]
        #print ci,area
        sql = """insert into iteminfo(proj,pf,subpf,chid,ver,ua,net,area,itemid,addtime,count) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        param=(proj,pf,subpf,chid,ver,ua,net,area,itemid,day,int(count))
        print sql,param
        c.execute(sql,param)
        conn.commit()
        #print keys
    c.close()

def topkeyword(day):
    l=getres('log.log.'+day,'topkeyword','1041')
    c=conn.cursor() 
    for one in l:
        keys=one.split('\t\t')[0]
        count=one.split('\t\t')[1]
        w=keys.split('\t')
        #print len(w)	
        proj=w[0]
        pf=w[1]
        subpf=w[2]
        chid=w[3]
        #print ci,area
        sql = """insert into topkeyword(proj,pf,subpf,chid,addtime,count) values(%s,%s,%s,%s,%s,%s)"""
        param=(proj,pf,subpf,chid,day,count)
        print sql,param
        c.execute(sql,param)
        conn.commit()
        #print keys
    c.close()
def run():
    import time,datetime
    t=datetime.datetime.now()-datetime.timedelta(days=1)
    day=str(t.date())
    iteminfo(day)
    fee(day)
    column(day)
    search(day)
    signin(day)
    videostat(day)
    topkeyword(day)

def runday():
   import time,datetime
   for d in range(1,2):
	t=datetime.datetime.now()-datetime.timedelta(days=d)
	day=str(t.date())
	print day
	#signin(day)
	#fee(day)
	#column(day)
	#videostat(day)
	#iteminfo(day)
	search(day)
	topkeyword(day)

run()
#runday()
