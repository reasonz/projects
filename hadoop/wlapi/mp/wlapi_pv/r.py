#encoding=utf-8
#!/usr/bin/evn python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
ips={}
for line in sys.stdin:
    line = line.strip()    
    print line
    try:
	ip,c=line.split("\t",1)	        
        ip = ip.decode("gbk")
	print ip
	c=int(c)
	count = ips.get(ip,1)
	ips[ip]=count+c
    except Exception,data:
        print Exception,data
for one in ips:
   print '%s\t\t%s' % (one,ips[one])
