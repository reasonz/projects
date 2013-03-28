#!/usr/bin/env python
import sys
for line in sys.stdin:
    try:
        line = line.strip()
        w=line.split("|")
 	#ci = w[1]
	proj=w[2]
	pf=w[3]
	subpf=w[4]
	chid=w[5]
	#ver=w[7]
	#ua=w[8]
	#net=w[9]
	#area=w[10]
	# 0: littl cdn 1:big cdn
	#f=w[11]
	#keyword=w[12]
        print '%s\t%s\t%s\t%s\t\t%s' % (proj,pf,subpf,chid,1)
    except:
	print 'Error|ValueError!'
