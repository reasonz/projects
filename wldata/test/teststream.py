from lib.bottle import run,route,response,request
import urllib2

bufsize=2048
@route('/down')
def down():

    try:
        for one in  request.headers():
            print one+"----"+ request.headers().get(one)
        response.content_type='video/mp4'
        f=urllib2.urlopen("http://114.80.122.39/work/51/150/017/479/51.20120819122713.mp4")
        while True:
            buf = f.read(bufsize)
            if buf:
                yield buf
            else:
                break
    except Exception,data:
        print Exception,data
run(host="10.151.20.48",port=8080)
