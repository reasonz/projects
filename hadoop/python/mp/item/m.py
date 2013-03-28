#!/usr/bin/env python
import sys
sys.path.append('/home/app_admin/hadoop/python/mp/lib/')
import util
for line in sys.stdin:
    try:
        line = line.strip()
        w=line.split("|")
 	#ci = w[1]
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
	# 0: littl cdn 1:big cdn
	#f=w[11]
	#keyword=w[12]
	itemid=w[11]
	
        print '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\t%s' % (proj,pf,subpf,chid,ver,ua,net,area,itemid,1)
    except:
	print 'Error|ValueError!'
