#encoding=utf-8
import urllib2
import json,time,os,sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pygame

class Sam():
    def speech2txt(self):
        FILE='C:/Users/reason/Downloads/1.flac'
        url = 'http://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=zh-CN'
        audio=open(FILE,'rb').read()
        headers = {'Content-Type' : 'audio/x-flac; rate=16000'}
        req = urllib2.Request(url, audio, headers)
        response = urllib2.urlopen(req)
        print response.read()

    def txt2speech(self,txt,filename):
        url = "http://translate.google.cn/translate_tts?ie=UTF-8&q="+txt+"&tl=zh&total=1&idx=0&textlen=6&prev=input&sa=N"
        print url
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11'}
        req= urllib2.Request(url,None,headers)
        res = urllib2.urlopen(req)
        f= open(filename,'wb')
        f.write(res.read())
        f.close()

    def getweather(self):
        url = "http://m.weather.com.cn/data/101020100.html"
        rs = urllib2.urlopen(url)
        # strres = json.dump(rs.read())
        
        res = json.loads(rs.read())
        weatherinfo = res['weatherinfo']
        city = weatherinfo['city'].encode('UTF-8')
        date_y= weatherinfo['date_y'].encode('UTF-8')
        week = weatherinfo['week'].encode('UTF-8')
        temp1 =weatherinfo['temp1'].encode('UTF-8')
        h_t = temp1.split('~')[1]
        l_t = temp1.split('~')[0]
        weather1 = weatherinfo['weather1'].encode('UTF-8')
        index_d = weatherinfo['index_d'].encode('UTF-8')
        wind1 = weatherinfo['wind1'].encode('UTF-8')
        return '早上好,可爱的小山同学,今天是' + date_y +'-'+week +'-'+ city + \
        '-最高温度'+h_t+'-最低温度'+l_t + '-'+ wind1 +'-'+ weather1 +'-'+index_d         

    def speek_weather(self):
        filename = str(time.time())+'.mp3'
        a = self.getweather()
        self.txt2speech(a,filename)
        self.speek(filename)

    def deletefile(self,filename):
        cmd = "rm "+filename
        print cmd
        os.popen(cmd)

    def speek(self,filename):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(1000.0/100.0)
        pygame.mixer.music.play()
        while 1:
            if not pygame.mixer.music.get_busy():
                self.deletefile(filename)
                return "finish"

    def saysomting(self,text):
        filename = str(time.time())+'.mp3'
        self.txt2speech(text,filename)
        self.speek(filename)
        
if __name__ =='__main__':

    s = Sam()
    s.saysomting(sys.argv[1])
    #s.speek_weather()
