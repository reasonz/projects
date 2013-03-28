#encoding=utf-8
import os,traceback
import MySQLdb as mdb
logtype = ['mtudou']
logpath = '~/syncphonelog/'
# logpath='~/hadoop/mtudou/mp/wap/'
shellpath = '~/hadoop/mtudou/mp/'
def getconn():
    conn= mdb.connect(host='wl-interface7',port=3306,user='ssx_dbmanage',passwd='ZAQ!4rfv',db='wldata',charset='utf8')
    return conn
def runcmd(cmd):
    l=[]
    for one in  os.popen(cmd).readlines():
        l.append(one)
    return l    
    
def createshell(type):
    return 'python ' + shellpath + type + '/m.py  | python '+ shellpath + type +'/r.py'

#run shell 
def getres(fname,type):
    cmd = 'cat ' + logpath +'/' + fname + ' | ' + createshell(type)
    print cmd
    l=runcmd(cmd)
    #for o in l :
    #    print o
    return l

def add_all(one,c,conn): 
    
    try:
        keys=one.split('\t\t')[1]
        count=one.split('\t\t')[0]
        w=keys.split('\t')
        if w[0]!='all':
            return
        day=w[1]
        hour=w[2]
        api=w[3]
        ver=w[4]
        area=w[5]
        wapportal=w[6]
        cp=w[7]
        if len(wapportal)>2:
            return
        sql = """insert into tdwap_api (day,hour,api,ver,area,wapportal,cp,count) values(%s,%s,%s,%s,%s,%s,%s,%s)"""
        param=(day,hour,api,ver,area,wapportal,cp,count)
        c.execute(sql,param)
        conn.commit()
    except  Exception,data:
       traceback.print_exc()

def add_cv(one,c,conn): 
    try:    
        keys=one.split('\t\t')[1]
        count=one.split('\t\t')[0]
        w=keys.split('\t')
        if len(w)!=7:
            return
        if w[0]!='cv':
            return
        day=w[1]
        api=w[2]
        ver=w[3]
        area=w[4]
        wapportal=w[5]

        cvtype=w[6]
        sql = """insert into tdwap_cv (day,api,ver,area,wapportal,cvtype,count) values(%s,%s,%s,%s,%s,%s,%s)"""
        param=(day,api,ver,area,wapportal,cvtype,count)
        c.execute(sql,param)
        conn.commit()
    except  Exception,data:
        traceback.print_exc()

def add_search(one,c,conn): 
    
    try:    
        keys=one.split('\t\t')[1]
        count=one.split('\t\t')[0]
        w=keys.split('\t')
        if w[0]!='search':
            return
        day=w[1]
        keyword =w[2]
        
        sql = """insert into tdwap_search (day,keyword,count) values(%s,%s,%s)"""
        param=(day,keyword,count)
        c.execute(sql,param)
        conn.commit()
    except  Exception,data:
        traceback.print_exc()

def add_navigate(one,c,conn): 
    
    try:    
        keys=one.split('\t\t')[1]
        count=one.split('\t\t')[0]
        w=keys.split('\t')
        if w[0]!='navigate':
            return
        day=w[1]
        navigate =w[2]

        sql = """insert into tdwap_navigate (day,navigate,count) values(%s,%s,%s)"""
        param=(day,navigate,count)
        c.execute(sql,param)
        conn.commit()
    except  Exception,data:
        traceback.print_exc()

def add_categroy(one,c,conn): 
    
    try:    
        keys=one.split('\t\t')[1]
        count=one.split('\t\t')[0]
        w=keys.split('\t')
        if w[0]!='categroy':
            return
        day=w[1]
        ver=w[2]
        wap=w[3]
        area=w[4]
        channel =w[5]

        sql = """insert into tdwap_categroy (day,ver,area,wapportal,channel,count) values(%s,%s,%s,%s,%s,%s)"""
        param=(day,ver,area,wap,channel,count)
        c.execute(sql,param)
        conn.commit()
    except  Exception,data:
        traceback.print_exc()


def wap_visit(day):
    # l=getres('t1.log','wap')
    l=getres('access.log_'+day+'.log','wap')
    conn = getconn()
    c= conn.cursor()
    for one in l:
        try:    
            keys=one.split('\t\t')[1]
            count=one.split('\t\t')[0]    
            w=keys.split('\t')
            
            if w[0]=='all':
                add_all(one,c,conn)
            if w[0]=='cv':
                add_cv(one,c,conn)
            if w[0]=='search':
                add_search(one,c,conn)
            if w[0]=='navigate':
                add_navigate(one,c,conn)
            if w[0]=='categroy':
                add_categroy(one,c,conn)

        except  Exception,data:
            traceback.print_exc()
    c.close()
    conn.close()





def run():
    import time,datetime
    t=datetime.datetime.now()-datetime.timedelta(days=1)
    day=str(t.date())
    print day
    wap_visit(day)
def runday():
    import time,datetime
    for d in range(1,5):
        t=datetime.datetime.now()-datetime.timedelta(days=d)
        day=str(t.date())
        print day
        wap_visit(day)
run()
#runday()
