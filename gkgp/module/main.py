#encoding=utf-8
__author__ = 'reason'
from lib.bottle import template,Bottle,request
from lib.cachewrap import cache_index
import sys,hashlib,json
from dbsetting import dbsetting
from setting import    SITE_DOMAIN,PIC_DOMAIN,project_path
from play import CJsonEncoder
reload(sys)
sys.setdefaultencoding('utf-8')
app = Bottle()


@app.route('/index')
@cache_index
def index():
    #print "项目的目录是在：",project_path
    #画廊 module=1
    hualang = findItem(1,8)
    #print changeVideo(hualang)
    #G客盛典 module=3
    gksd = changeVideo(findItem(3,5))
    #热门影院 module=2
    hotvideo = changeVideo(findItem(2,9))
    #排行 module=5
    ranking = changeVideo(findItem(5,10))
    #G客校园行 module=4
    gkschool = changeVideo(findItem(4,5))
    #G客联盟 module = 7
    gktxfootTop = changeVideo(findItem(7,6,0))
    gktxfootMiddle = changeVideo(findItem(7,6,6))
    gktxfootDown = changeVideo(findItem(7,6,12))
    #G客特写 module = 6
    gktxleft = changeVideo(findItem(6,3,0))
    gktxmiddle = changeVideo(findItem(6,3,3))
    gktxright = changeVideo(findItem(6,3,6))
    #广告位 module=9
    adwords = changeVideo(findItem(9,2))
    #首发 module = 8
    firstvideo = changeVideo(findItem(8,5))
    #日韩 module=21
    rihan = changeVideo(findItem(21,5))
    #港台 module=23
    gangtai = changeVideo(findItem(23,5))
    #内地 module=22
    neidi = changeVideo(findItem(22,5))
    #欧美 module=19
    oumei = changeVideo(findItem(19,5))
    #中间广告位 module=24
    middleads = findItem(24,5)
    #G客G拍 module=
    gkgp = changeVideo(findItem(25,5))
    #广告位三 module=26
    thirdads = findItem(26,1)
    #右栏顶部广告位 module=27
    righttopads = findItem(27,1)


    return template('index',dict(domain=SITE_DOMAIN,picdomain=PIC_DOMAIN,hualang=hualang,\
        gksd=gksd,hotvideo=hotvideo,ranking=ranking,gkschool=gkschool,gktxfootTop=gktxfootTop,\
        gktxfootMiddle=gktxfootMiddle,gktxfootDown=gktxfootDown,gktxleft=gktxleft,gktxmiddle=gktxmiddle,\
        gktxright=gktxright,adwords=adwords,firstvideo=firstvideo,rihan=rihan,gangtai=gangtai,neidi=neidi,oumei=oumei,middleads=middleads,gkgp=gkgp,\
        thirdads=thirdads,righttopads=righttopads)) 
    #return template('index',dict(domain=SITE_DOMAIN)) 


@app.route("/navi")
def navi():
	#导航 module=10
	navi = changeVideo(findItem(10,10))
	for nav in navi:
		if nav[6].startswith("http://"):
			pass
		else:
			nav[6] = SITE_DOMAIN+nav[6]

	return json.dumps(navi,cls=CJsonEncoder)


@app.route('/upload.html')
def upload():
    return template('upload',dict(domain=SITE_DOMAIN))

@app.route('/reg.html')
def reg():
    return template('reg',dict(domain=SITE_DOMAIN))

@app.route('/play.html')
def play():
    return template('play',dict(domain=SITE_DOMAIN))


def findItem(module,num,begin=0):
    sql='''select id, title, brif_desc, description, item_type, item_code, link_url, position, small_pic, big_pic, module, addTime, status, updateTime from 
        gkgp_main_setting  where status=1 and  module=%s order by position asc,updateTime desc limit %s,%s '''
    return dbsetting.query_list(sql,(module,begin,num))


def changeVideo(ls):
    newls = []
    if None!=ls and len(ls)>0:
        for v in ls:
            newsubls = []
            newsubls.append(v[0])
            newsubls.append(v[1])
            newsubls.append(v[2])
            newsubls.append(v[3])
            newsubls.append(v[4])
            newsubls.append(v[5])
            newsubls.append(v[6])
            newsubls.append(v[7])
            newsubls.append(v[8])
            newsubls.append(v[9])
            newsubls.append(v[10])
            newsubls.append(v[11])
            newsubls.append(v[12])
            newsubls.append(v[13])
            if newsubls[4]==1:
                newsubls[6] = SITE_DOMAIN+"/programs/view/"+newsubls[5]+"/"
            newls.append(newsubls)
    return newls







