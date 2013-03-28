#!/usr/bin/env python
import sys
import traceback
def getUA(s):
    ua=s.strip().lower()
    if ua.find("juc")!=-1:
        ua='juc'
    if ua.find("huawei")!=-1:
        ua='huawei'
    if ua.find(" ")!=-1 :
        ua= ua.split(" ")[0]
    if ua.find(" ")==-1 and  ua.find("/")!=-1:
	ua=ua.split("/")[0]
    if ua.find("-")!=-1 :
        ua = ua.split("-")[0]
    if ua.find("_")!=-1:
        ua = ua.split("_")[0]
    if ua.find(" ")==-1 and ua.find("/")==-1:
        ua=ua[:12]
    if ua.find("nokia")!=-1:
	ua='nokia'
    if len(ua)==0 :
        ua='empty'
    
    return ua

for line in sys.stdin:
    try:
        line = line.strip()
	if line.find("|")!=-1 and line.find('/mtudou')!=-1:
       	    w=line.split("|")
	    date = w[0].split(' ')[0]
	    ua=getUA(w[10])
            print '%s\t%s\t\t%s' % (date,ua,1)
    except :
	traceback.print_exc()
	

