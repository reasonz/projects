#!/usr/bin/env python
import sys,traceback

for line in sys.stdin:
    try:
        line = line.strip()
	if line.find("|")!=-1 and line.find('/mtudou')!=-1:
       	    w=line.split("|")
	    date = w[0].split(' ')
	    day=date[0]
	    hour = date[1].split(":")[0]
	    api=w[2].lower()
	    ver=w[3]
	    area=w[12][:2]
	    wapportal =w[13]
	    if api in ['play','down']:
	    	content=w[4]
	    	type=content.split(",")[0]
	    	channel=content.split(",")[1]
       	        print '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\t%s' % (day,hour,api,ver,area,wapportal,type,channel,1)	    
    except Exception,data:
        traceback.print_exc()
	

