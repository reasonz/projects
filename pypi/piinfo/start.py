import tornado.ioloop
import tornado.web
import  os,time
class SnapHandler(tornado.web.RequestHandler):
    def get(self):
        jpgname = time.time()
        self.getpic(jpgname)
        f=open('/tmp/'+str(jpgname) +'.jpeg','rb')
        os.popen('rm /tmp/'+str(jpgname) + '.jpeg')
        self.set_header('Content-Type', 'image/jpeg; charset=utf-8')
        self.write(f.read())

    def getpic(self,name):
        cmd = "fswebcam -d /dev/video0 /tmp/" + str(name) + ".jpeg"
        os.popen(cmd)

   


class InfoHandler(tornado.web.RequestHandler):
    def get(self):
        html = "<html>"
        html +="<head></head>"
        html += "<h1>My raspberry PI sysinfo</h1>"
        html += "<h4>CPU INFO</h4><br>"
        html += self.cpuinfo()+"<br>"
        html += "<h4>MEM INFO</h4><br>"
        html += self.meminfo()+"<br>"
        html += "<h4>DF INFO</h4><br>"
        html += self.hdinfo()+"<br>"
        html +="</html>"
        self.write(html)

 
    def cpuinfo(self):
        cmd="cat /proc/cpuinfo"
        return os.popen(cmd).read().replace('\n','<br>')

    def meminfo(self):
        memcmd = "free -m"
        return os.popen(memcmd).read().replace('\n','<br>')

    def hdinfo(self):
        hdcmd="df -h"
        return os.popen(hdcmd).read().replace('\n','<br>')



class MagicScreenHandler(tornado.web.RequestHandler):
    def get(self):
        items = ["item1","item2","item3"]  
        self.render("views/magicscreen.html", items=items)      

application = tornado.web.Application([
    (r"/snap", SnapHandler),
    (r"/info", InfoHandler),
    (r"/", MagicScreenHandler)
])

if __name__ == "__main__":
    application.listen(9999)
    loop=tornado.ioloop.IOLoop.instance() 
    loop.start()