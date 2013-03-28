#-*- coding:utf-8 -*-
__author__ = 'hpwang'
from lib.bottle import template,Bottle,request,view,response,redirect
from lib.cachewrap import cache
import sys,hashlib,datetime,utils,string
from dbsetting import dbsetting as db
from setting import    SITE_DOMAIN,SECRET_KEY,VREYCODE,UID
app = Bottle()

@app.route("/<id:int>")
@app.route("/<id:int>/<pn:int>")
@view("list")
def videolist(id,pn=1):
	pagesize = 5
	curNum = getItemCountByChannelId(1,id)[0]
	totalPages = (curNum+pagesize-1)/pagesize
	if totalPages<pn:
		pn = totalPages
	elif pn<=0:
		pn = 1

	startNum = (pn-1)*pagesize

	itemids = findItemIdByChannelId(id,startNum,pagesize)
	itemids = listutil(itemids)
	print "itemids is ",itemids
	videos = findItemByList(itemids)
	pg = createPage('list/'+str(id)+'/',totalPages,pn)
	pg = unicode(pg)
	return dict(domain=SITE_DOMAIN,videos=videos,pg=pg)


@app.route("/myvideos")
@view("list")
def myvideo():
	return dict(domain=SITE_DOMAIN);


def findItemByList(ids):
	sql = "select id,itemid,title,description,videotype,tags,itemcode,playurl,pics,\
			playtimes,status,queryurl,totaltime,addtime,outerplayurl,mpsurl,brif_desc,\
			digtimes,burytimes from gkgp_item where id in %s"
	sql = sql %  ids
	sql = string.replace(sql,"[","(")
	sql = string.replace(sql,"]",")")
	return db.query_list(sql,None)


def findItemIdByChannelId(chid,start,num):
	sql = "select item_id from gkgp_channel_item_link where item_type=1 and channel_id=%s and status=1 limit %s,%s"
	return db.query_list(sql,(chid,start,num))


#获取某个频道下的视频总数量,item_type=1表示视频2表示连接
def getItemCountByChannelId(item_type,chId):
	'''获取条件下视频的总条数'''
	sql = "select count(*) from gkgp_channel_item_link where item_type=%s and channel_id=%s and status=1"
	return db.query_one(sql,(item_type,chId))

#获取用户下的视频的数量,item_type=1表示视频2表示连接
def getItemCountByUid(item_type,Uid):
	sql="select count(*) from gkgp_channel_item_link where item_type=%s and uid=%s"
	return db.query_one(sql,(item_type,Uid))

def listutil(items):
	l = []
	for one in items:
		l.append(int(one[0]))
	return l

def createPage(link,totalPages,pn):
	page = "<div class=\"page-nav\"> <div class=\"page-nav-bar\">"
	test_page = '''
		<div class="page-nav">
						<div class="page-nav-bar">
							<span class="page-nav-prev">&lt;上一页</span>
							<ul>
								<li class="current">
									1
								</li>
								<li>
									<a href="">2</a>
								</li>
								
								<li class="dot">
									...
								</li>
								<li>
									<a href="" page="37">37</a>
								</li>
								<li>
									<a href="">38</a>
								</li>

							</ul>
							<a class="page-nav-next" href="">下一页&gt;</a>
						</div>
					</div>	

	'''
	if pn==1:
		page+="<span class=\"page-nav-prev\">&lt;上一页</span><ul>"
	else:
		page+="<a class=\"page-nav-prev\" href=\""+SITE_DOMAIN+"/"+link+str(pn-1)+"\">&lt;上一页</a> <ul>"

	for i in range(1,totalPages+1):
		if i==pn:
			page+="<li class=\"current\">"+str(i)+"</li>"
		else:
			page+="<li><a href=\""+SITE_DOMAIN+"/"+link+str(i)+"\">"+str(i)+"</a></li>"
	
	if totalPages==pn:
		page+="</ul><span class=\"page-nav-next\">下一页&gt;</span>"
	else:
		page+="</ul><a class=\"page-nav-next\" href=\""+SITE_DOMAIN+"/"+link+str(pn+1)+"\">下一页&gt;</a>"
	page+="</div> </div>"
	return page
