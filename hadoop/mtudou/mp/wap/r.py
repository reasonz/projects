#!/usr/bin/evn python

import sys
import traceback
all={}
cv={}
search={}
navigate={}
categroy={}

error=0
for line in sys.stdin:
    line = line.strip()
    print line
    key,count=line.split('\t\t',1)
    try:
        flag = key.split('\t')[0]
        if flag =='all':
            count = int(count)
            all[key]=all.get(key,0)+count
        
        if flag=='cv':
            count = int(count)
            cv[key]=cv.get(key,0)+count
        if flag =='search':
            count = int(count)
            search[key]=search.get(key,0)+count
        if flag =='navigate':
            count = int(count)
            navigate[key]=navigate.get(key,0)+count
        if flag =='categroy':
            count = int(count)
            categroy[key]=categroy.get(key,0)+count
    except:
        pass
        
for key,count in all.items():
    print '%s\t\t%s' % (count,key)

for key,count in cv.items():
    print '%s\t\t%s' % (count,key)

for key,count in search.items():
    if count>100:
        print '%s\t\t%s' % (count,key)

for key,count in navigate.items():
    print '%s\t\t%s' % (count,key)

for key,count in categroy.items():
    print '%s\t\t%s' % (count,key)
