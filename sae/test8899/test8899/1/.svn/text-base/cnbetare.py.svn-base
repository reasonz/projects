#coding:utf-8
import re
import urllib2
import mydb,sys

host='http://www.cnbeta.com'
def gettitle():
    res= urllib2.urlopen('http://www.cnbeta.com/#1')
    pc= res.readlines()
    pc= ''.join(pc)
    pc=pc.decode('gbk')
    pstr=r'<dt\sclass=\"topic\"\s><a\shref=\"(\S+)\"\s+target=\"_blank\"><strong>(.+)</strong></a></dt>'
    l=[]
    for one in re.findall(pstr,pc):
        d={}
        d['url']=one[0]
        d['title']=one[1]
        l.append(d)
    #print l
    return l
def getdetail(url):
    url=host+url
    res=''.join(urllib2.urlopen(url).readlines()).decode('gbk')
    #print res
    tc=r'<div\sid=\"news_content\">([\s\S]*)'
    mc= re.findall(tc,res)[0]
    tsub=r'<div\sclass=\"digbox\">([\s\S]*)'
    return  re.sub(tsub,'',mc).strip()

def addpost():
    try:
        l=gettitle()
        print 'list len is ', str(len(l))
        for one in l:
            res = mydb.ishave(one.get('title'))
            print str(res)+'  left is res ,right is title   '+str(one.get('title').encode('utf-8'))
            if  res:
                c=getdetail(one.get('url'))
                d={}
                
                d['post_title']=one.get('title').encode('utf-8')
                print 'title is 2222 %s '% one.get('title').encode('utf-8')
                d['post_content']=c.encode('utf-8')
                d['type']=3
                print d.get('post_title'),d.get('post_url')
                if not d.get('post_title'):
                    d['post_title']='none'
                if not d.get('post_content'):
                    d['post_contetn']='none'
                mydb.insert(d)
                print 'insert ',d.get('post_title')
    except Exception,e:
        print 'error msg',e 
#def addtest():
#    d={"post_title":"1312231","post_content":"sdffsdf","type":3}
#    mydb.test(d)
#addtest()
addpost()
