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
            if len(ver)==0:
                ver=-1
            #content=w[4]
            cp = w[11]
            if len(cp)==0:
                cp=-1
            area=w[12][:2]
            if len(area)==0:
                area=-1
            wapportal =w[13]

            if api in ['index','catelist','view','search','navigate','showcommment','putcomment','userupload','register','login','logout','play','down']:
                   print '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\t%s' % ('all',day,hour,api,ver,area,wapportal,cp,1)        
            if api in ['play','down']:
                try:
                    content=w[4]
                    cvtype=content.split(",")[0]
                    if len(cvtype)==0 or not cvtype.isdigit():
                        cvtype=-1
                    print '%s\t%s\t%s\t%s\t%s\t%s\t%s\t\t%s' % ('cv',day,api,ver,area,wapportal,cvtype,1)        
                except:
                    pass
            if api =='navigate':
                try:
                    content=w[4]
                    print '%s\t%s\t%s\t%s\t%s\t\t%s' % ('navigate',day,ver,wapportal,content,1)        
                except:
                    traceback.print_exc()
            if api =='search':
                try:
                    keyword=w[4].split(",")[0]
                    if len(keyword)>0:
                        print '%s\t%s\t%s\t\t%s' % ('search',day,keyword,1)        
                except:
                    pass
            if api =='category':
                try:
                    channelid=w[4]
                    print '%s\t%s\t%s\t%s\t%s\t%s\t\t%s' % ('categroy',day,ver,wapportal,area,channelid,1)       
                except:
                    traceback.print_exc() 
                
    except Exception,data:
        #traceback.print_exc()
        pass
    

