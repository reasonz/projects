#coding:gb2312
from bottle import run,route,response,request
import os,time,sys
import chardet
reload(sys)
sys.setdefaultencoding('gb2312')

@route('/myinfo')
def myinfo():
    html = "<html>"
    html +="<head></head>"
    html += "<h1>My raspberry PI sysinfo</h1>"
    html += "<h4>CPU INFO</h4><br>"
    html += cpuinfo()+"<br>"
    html += "<h4>MEM INFO</h4><br>"
    html += meminfo()+"<br>"
    html += "<h4>DF INFO</h4><br>"
    html += hdinfo()+"<br>"
    html +="</html>"
    return html



@route('/snap')
def  snap():
    jpgname = time.time()
    getpic(jpgname)
    response.set_header('content_type','image/jpg')
    f=open('/tmp/'+str(jpgname) +'.jpeg','rb')
    os.popen('rm /tmp/'+str(jpgname) + '.jpeg')
    return f


@route('/test')
def  test():
    s = request.query.get('title')
    print chardet.detect(s)
    return s



def getpic(name):
    
    cmd = "fswebcam -d /dev/video0 /tmp/" + str(name) + ".jpeg"
    os.popen(cmd)
def cpuinfo():
    cmd="cat /proc/cpuinfo"
    return os.popen(cmd).read().replace('\n','<br>')

def meminfo():
    memcmd = "free -m"
    return os.popen(memcmd).read().replace('\n','<br>')

def hdinfo():
    hdcmd="df -h"
    return os.popen(hdcmd).read().replace('\n','<br>')

if __name__ == "__main__":
    run(host="0.0.0.0",port=8888,reloader=True)
