#!/usr/bin/env python
import sys
for line in sys.stdin:
    try:
        line = line.strip()
        w=line.split("|")
        ci=w[0].split('>')[2]
	if len(ci)==0:
	    ci='empty_ci'
	ip=w[1]
	if len(ip)==0:
	    ip='empty_ip'
	method = w[2]
	if len(method)==0:
	    method='empty_name'
	usetime = w[3][:-2]
	
	print '%s\t%s\t%s\t\t%s' % (method,ci,ip,usetime)
    except:
	pass
