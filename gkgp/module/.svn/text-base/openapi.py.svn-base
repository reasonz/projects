#encoding=utf-8
import sys,base64,urllib2,urllib,json
reload(sys)
sys.setdefaultencoding('utf-8')
from setting import username,pwd,appkey,open_api_url

def uploaditem(title,tags,content,channelId,ipAddr):
    encoding = base64.b64encode(username+':'+pwd)
    req = urllib2.Request(open_api_url)
    req.add_header('Authorization','Basic '+encoding)
    param = {'appKey':appkey,'method':'item.upload','title':title,'tags':tags,'channelId':channelId,'ipAddr':ipAddr,'content':content}
    data = urllib.urlencode(param)  
    opener = urllib2.build_opener()  
    response = opener.open(req, data) 
    return response.read()

def id2code(id):
    url='http://api.tudou.com/v3/gw?method=transform.code.id&appKey=c58dad0ed452b2d3&format=json&itemCodes=%s' %(id)
    res = urllib2.urlopen(url,'')
    obj= json.load(res,encoding="utf-8")
    return obj.get('multiResult').get('results')[0].get('itemCode')


def getitem(itemcode):
    url='http://api.tudou.com/v3/gw?method=item.info.get&appKey=c58dad0ed452b2d3&format=json&itemCodes=%s' % (itemcode)
    res = urllib2.urlopen(url,'')
    obj= json.load(res,encoding="utf-8")
    return obj
    
