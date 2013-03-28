#encoding=utf-8
__author__ = 'reason'
import codecs
import time
from pymongo import Connection
con = Connection("10.25.251.101",27018)
db = con.iplist
ipcollection = db.ipcoll



def ip2num(ip):
    ips=ip.strip().split('.')
    num = int(ips[0])*256*256*256 + int(ips[1])*256*256 + int(ips[2])*256+int(ips[3])-1
    return num

f = open(u'd://tt.txt','r')
c=0
for o in f.readlines():
    if o[:3] == codecs.BOM_UTF8:
        o = o[3:]
    #time.sleep(0.2)
    its = o.split()
    #print '%s__%s__%s' %  (ip2num(its[0]), ip2num(its[1]) ,its[2])
    d={"start":ip2num(its[0]),"end":ip2num(its[1]),"area":its[2],"s":its[0],"e":its[1]}
    ipcollection.insert(d)
    c+=1
    print c

