#!/usr/bin/evn python

import sys
wc={}
ut={}
calltime=0
costtime=0
methodavgcount=0

ips={}
uvs={}

ip=1
uv=1
pv=1

for line in sys.stdin:
    line = line.strip()
    pv+=1
    try:	
        key,count=line.split('\t\t',1)
	subkey=key.split('\t')
	tci=subkey[1]
	tip=subkey[2]
	if not uvs.get(tci):
	    uv+=1
   	    uvs[tci]=1
        if not ips.get(tip):
	    ip+=1
	    ips[tip]=1

	count = int(count)
	api = subkey[0]
	wc[api]=wc.get(api,0)+1 
	ut[api]=ut.get(api,0)+ count
    except Exception,data:
	print Exception,":",data
        wc['error']=wc.get('error',0)+1
for key,count in wc.items():
    if key != 'error':
        usetime = ut[key]
	calltime+=int(count)
	costtime+=int(usetime)
    	print '%s\t%s\t%s\t%s' % (key,count,usetime,int(usetime)/int(count))
    else:
	print '%s\t\t%s' %(key,count)
	pass

print '%s\t%s\t%s\t%s\t%s' % ('methodavgcount',float(costtime)/float(calltime),pv,uv,ip)

