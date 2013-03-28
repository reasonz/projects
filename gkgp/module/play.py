#encoding=utf-8
__author__ = 'reason'

from lib.bottle import template,Bottle,request,view,response
from lib.cachewrap import cache
from dbsetting import dbsetting as db
import sys,hashlib,json,string,traceback,main
from utils import get_cookie,set_cookie
from datetime import datetime,date
from setting import    SITE_DOMAIN,SECRET_KEY,VREYCODE,UID,PIC_DOMAIN
reload(sys)
sys.setdefaultencoding('utf-8')
app = Bottle()

#http://www.tudou.com/programs/view/yCrBRo8UAuI/
@app.route('/view/:itemcode/')
@view('play')
def play(itemcode):
    item = db.query_one('select t1.id,t1.itemcode,t.username,t.id,t1.title,t1.addtime,t1.description,t1.playtimes,t1.digtimes,t1.burytimes \
      ,t1.pics from gkgp_user t,gkgp_item t1 ,gkgp_user_item t2 where t1.id = t2.videoid and t2.userid = t.id and \
       itemcode=%s',(itemcode))
    # put play history into cookie
    # key : playlist
    # value : {'itemcode1','itemcode3','itemcode4'}
    playlist = get_cookie('playlist')
    if playlist:
        l=json.loads(playlist)
        if itemcode not in l:
            if(len(l)>=10):
                del l[0]
                l.append(itemcode)
            else:
                l.append(itemcode)
            set_cookie('playlist',json.dumps(l))
    else:
        l=[]
        l.append(itemcode)
        set_cookie('playlist',json.dumps(l))
    # end

    if item is not None:
        playtime = 0
        if item[7] is not None and item[7]>=0:
            playtime = item[7]+1
        else:
             playtime =1
        db.update('update gkgp_item set playtimes=%s where id=%s',(playtime,item[0]))
    #首发
    firstvideo = main.changeVideo(main.findItem(8,5))
    # get user  other videos
    othervideos = db.query_list('select t.title,t.pics,t.itemcode from gkgp_item t, \
        gkgp_user_item t1 where t.id=t1.videoid and t1.userid=%s order by t.addtime desc limit 0,4 ',(item[3]))

    item = list(item)
    item[7] = beautifulDisPlay(str(item[7]))
    item[8] = beautifulDisPlay(str(item[8]))
    item[9] = beautifulDisPlay(str(item[9]))

    return dict(domain=SITE_DOMAIN,picdomain=PIC_DOMAIN,itemcode=itemcode,item=item,firstvideo=firstvideo,othervideos=othervideos)

@app.route('/delplaylist')
def delplaylist():
    try:
        itemcode = request.query.get('itemcode')
        playlist = get_cookie('playlist')
        l=json.loads(playlist)
        del l[l.index(itemcode)]
        set_cookie('playlist',json.dumps(l))
        return 'ok'
    except Exception:
        traceback.print_exc()
        return 'error'


@app.route("/playlist")
def playlist():
    plscodes = get_cookie('playlist')
    print "plscodes is ",plscodes
    if not plscodes:
        return json.dumps(None)

    l=json.loads(plscodes)
    if None==plscodes or len(l)==0:
        return json.dumps(None)
    pls = getPlayVideoByCodes(plscodes)
    if None==pls or len(pls)==0:
        return json.dumps(None)
    return json.dumps(pls,cls=CJsonEncoder)

def getPlayVideoByCodes(codes):
    sql = ''' select    id, 
    itemid, 
    title, 
    description, 
    videotype, 
    tags, 
    itemcode, 
    playurl, 
    pics, 
    playtimes, 
    status, 
    queryurl, 
    totaltime, 
    addtime, 
    outerplayurl, 
    mpsurl, 
    brif_desc
     
    from 
    gkgp_item  where itemcode in %s'''

    sql = sql %  codes
    sql = string.replace(sql,"[","(")
    sql = string.replace(sql,"]",")")
    return db.query_list(sql,None)

@app.route('/dig/:itemcode/')
def dig(itemcode):
    try:
        uid = get_cookie(UID)
        if uid is None:
            return 'noLogin'
        else:
            item = db.query_one('select t.id,t.itemcode,t.digtimes \
                  from gkgp_item t  where t.itemcode=%s',itemcode)
            if item is not None:
                digOrBuryHistory = get_cookie('DigOrBury_'+itemcode)
                if digOrBuryHistory is not None and len(digOrBuryHistory)>0:
                    if item[2] is not None:
                        return beautifulDisPlay(str(item[2]))
                    else:
                        return '0'
                else:
                    if item[2] is not None:
                        temp = item[2]+1
                        db.update('update gkgp_item set digtimes=%s where id=%s',(temp,item[0]))
                        set_cookie('DigOrBury_'+itemcode,itemcode)
                        return beautifulDisPlay(str(temp))
                    else:
                        return '0'
            else:
                return '0'
    except Exception:
        traceback.print_exc()
        return 'dig error'

@app.route('/bury/:itemcode/')
def bury(itemcode):
    try:

        uid = get_cookie(UID)
        if uid is None:
            return 'noLogin'
        else:
            item = db.query_one('select t.id,t.itemcode,t.burytimes \
                  from gkgp_item t  where t.itemcode=%s',itemcode)
            if item is not None:
                digOrBuryHistory = get_cookie('DigOrBury_'+itemcode)
                if digOrBuryHistory is not None and len(digOrBuryHistory)>0:
                    if item[2] is not None:
                        return beautifulDisPlay(str(item[2]))
                    else:
                        return '0'
                else:
                    if item[2] is not None:
                        temp = item[2]+1
                        db.update('update gkgp_item set burytimes=%s where id=%s',(temp,item[0]))
                        set_cookie('DigOrBury_'+itemcode,itemcode)
                        return beautifulDisPlay(str(temp))
                    else:
                        return '0'
            else:
                return '0'
    except Exception:
        traceback.print_exc()
        return 'bury error'

def beautifulDisPlay(strNum):
    display = ''
    if strNum is not None and len(strNum)>0:
        strNum = list(strNum)
        for i in range(len(strNum)-1,-1,-1):
            if (len(strNum)-i)%3==0:
                 if i==0 and len(strNum)%3==0:
                     display =strNum[i]+display
                 else:
                     display = ','+strNum[i]+display
            else:
                display = strNum[i]+display
        print display
    else:
        display = strNum
    return display

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
