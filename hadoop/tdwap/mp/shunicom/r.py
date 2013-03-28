#!/usr/bin/evn python

import sys
wc={}
error=0
for line in sys.stdin:
    line = line.strip()
    if line[0] == 'Error':
	wc['error']=wc.get('error',0)+1
    else:
	key,count=line.split('\t\t',1)
	try:
	    count = int(count)
	    wc[key]=wc.get(key,0)+count
	except:
	    pass
for key,count in wc.items():
    print '%s\t\t%s' % (key,count)

