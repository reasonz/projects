#!/usr/bin/env python
import sys
from time import clock as now
from pymongo import Connection
con = Connection("wl-push1",27018)
db=con.iplist
ipcoll = db.ipcoll

def ip2num(ip):
    ips=ip.strip().split(".")
    num = int(ips[0])*256*256*256 + int(ips[1])*256*256 + int(ips[2])*256 + int(ips[3])-1
    return num

def getarea(ip):
    num = ip2num(ip)
    res = ipcoll.find_one({"start":{"$lt":num},"end":{"$gt":num}})
    if res :
	return res['area']
    else:
        return "empty"

for line in sys.stdin:
    try:
        line = line.strip()
        w=line.split("\t\t")
	ip=w[0]
	start=now()
        area=getarea(ip)
	end = now()
	count=w[1]
	print '%s\t%s' % ("u'area",count)
    except Exception,data:
	print Exception,data
