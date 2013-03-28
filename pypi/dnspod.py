#!/usr/bin/env python
#-*- coding:utf-8 -*-
import httplib, urllib
import socket
import time
params = dict(
    login_email="543588696@qq.com", # replace with your email
    login_password="198388", # replace with your password
    format="json",
    domain_id=2273039, # replace with your domain_od, can get it by API Domain.List
    record_id=16378827, # replace with your record_id, can get it by API Record.List
    sub_domain="home", # replace with your sub_domain
  record_line="默认",
)

def getcurrent_ip():
    try:
        cip = open("/tmp/current_ip",'r').readlines()[0]
        return cip
    except Exception,e:
        return None
def setcurrent_ip(ip):
    f=open("/tmp/current_ip",'w')
    f.write(ip)
    f.close()

current_ip = None
def ddns(ip):
    params.update(dict(value=ip))
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
    conn = httplib.HTTPSConnection("dnsapi.cn")
    conn.request("POST", "/Record.Ddns", urllib.urlencode(params), headers)
    response = conn.getresponse()
    print response.status, response.reason
    data = response.read()
    print data
    conn.close()
    return response.status == 200
def getip():
    sock = socket.create_connection(('ns1.dnspod.net', 6666))
    ip = sock.recv(16)
    sock.close()
    return ip
def update():
    
    try:
        ip = getip()
        print ip
        if getcurrent_ip() != ip:
            if ddns(ip):
                setcurrent_ip(ip)
    except Exception, e:
        print e
        pass
    #time.sleep(600)
if __name__ == '__main__':
    update()
    #ddns("10.151.23.44")
    
