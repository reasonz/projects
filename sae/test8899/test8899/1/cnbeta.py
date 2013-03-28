#coding:gbk
from bs4 import BeautifulSoup as bt
import urllib2
import mydb
host='http://www.cnbeta.com'
def fetchtopic():
    res = urllib2.urlopen('http://www.cnbeta.com/#1')   
    #res = res.readlines()
    #print res

    soup = bt(res,from_encoding='gbk')
    r = soup.findAll(attrs={'class':'topic'})
    l=[]
    for one in r:
        d={}
        d['url']=host + one.a['href']
        d['title']=one.a.strong.string
        l.append(d)
    return l    
def fetchdetail(url):
    res = urllib2.urlopen(url)
    soup = bt(res,from_encoding='gbk')
    #r = soup.find(id='news_content')
    return soup

def cnbetamain():

    l=fetchtopic()
    for one in l:
        if not ishave(one.get('title')):
            d={}
            content=fetchdetail(one.get('url'))
            d['post_title']=one.get('title')
            d['post_content']=content
            d['type']=3
            insert(d)
            print 'insert one post!'
    return l
def test():
    return fetchtopic()
print test()
