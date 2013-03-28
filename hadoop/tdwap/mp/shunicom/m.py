#!/usr/bin/env python
import sys
for line in sys.stdin:
    try:
        line = line.strip()
        w=line.split(",")
	date=w[0].split(' ')[0]
	projid=w[2]
	phone=w[3]
#	ip=w[4]
	wapver=w[5]
	net=w[6]
	#browser=w[7].split(' ')[0]
	print '%s\t%s\t%s\t%s\t%s\t\t%s' % (date,projid,phone,wapver,net,1)
    except:
	print 'Error|ValueError!'
