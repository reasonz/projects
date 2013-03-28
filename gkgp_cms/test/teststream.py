import sys,hashlib
sys.path.append('../module')
reload(sys)
sys.setdefaultencoding('utf-8')

from dbsetting import DBsetting
d = DBsetting()
def dest(url):
        m = hashlib.md5(url)
        return m.hexdigest()


def cleanold():
    sqls=["delete from fee  where addtime>'2012-11-10'","delete from signin  where addtime>'2012-11-10'","delete from search  where addtime>'2012-11-10'","delete from channel  where addtime>'2012-11-10'","delete from topkeyword  where addtime>'2012-11-10'","delete from videostate  where addtime>'2012-11-10'","delete from iteminfo  where addtime>'2012-11-10'"]
    conn = d.getnokiaconn()

def change2md5():
    conn=d.getmysqlconn()
    sql = "select * from users"
    c = conn.cursor()
    c.execute(sql)
    for o in c.fetchall():
        password = str(o[2])
        dd = str(o[0])
        print dd,dest(password)
        sql = " update users set password=%s where id = %s"
        c.execute(sql,(dest(password),dd))
        conn.commit()
    c.close()
    conn.close()



def tt():
    ll = ['IWMCVWWYOZULS','J7YM3DUVDF5S4','KCZFO7CH74QTK','FM2MVUP5GENAY','CWTWO2YQUNDD4','25M7WAP7OQ','EZHKOS7HPPJNO','LEC7M4QUFINJC','OQC5UL7MCY6OC','NXKRLHUKLTSNY','CRCCPFHH2PADC','JJR36TJJV57B4','POIRMAX77Y','G63XP6ETQ5DGO','M6EGZRBOGD44W','O6G7DLV5ULIZI','JSEIOZAT3XTOK','L42MYH5YB337G','EZHKOS7HPPJNO','NDV2RQOENKFIM','KCZE7Y55HQJZW','K3QSJHXF4BC4W','DEXXPA2724S66','LEC7IT7NWQ3E6','JBPKYLLIDRCF4','G326CZCMQSM5M','HENLAND7VCEJM']
    
    conn = d.getnokiaconn()
    sql = "select ci from fee where chid=6501"
    c = conn.cursor()
    c.execute(sql)
    l=[]
    for o in c.fetchall():
        l.append(str(o[0]))
    ll.sort()
    l.sort()
    print ll
    print l

def getmtudoutop100():
    f = open('d://1222.txt','r')
    conn = d.getconn()
    c = conn.cursor()
    f1= open('d://temp.txt','w')
    dd={}
    for one in f.readlines():
        print one
    
        ss = one.replace('\n','').split('\t\t')
        id= ss[1].split('\t')
        # sql = "select TITLE from TDCMS_MOBILE_RECITEM  t where t.ITEM_ID="+id[1]
        dd[ss[0]]=id[1]
        # print id[1]
        # c.execute(sql)
        # t=c.fetchone()
        # f1.write(t[0])
    dd.sort()
    print d
    f1.close()
    c.close()
    conn.close()

print dest("admin")