#!/usr/bin/env python
import sys
sys.path.append('/home/app_admin/hadoop/python/mp/lib/')
import util
for line in sys.stdin:
    try:
        line = line.strip()
        w=line.split("|")
 	ci = w[1]
	proj=w[2]
	pf=w[3]
	subpf=w[4]
	chid=w[5]
	ver=w[7]
	ua=w[8]
        if len(ua)==0:
	    ua='other'
	else:
	    ua=util.getua(ua)
	    
	net=w[9]
	area=w[10]
	isnew=w[12]
        print '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\t%s' % (ci,proj,pf,subpf,chid,ver,ua,net,area,isnew,1)
    except Exception,data:
	print Exception,":",data
