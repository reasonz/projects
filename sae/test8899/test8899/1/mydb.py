import MySQLdb as db
import sys
import traceback
def insert(p):
    try:
        print 'titel is %s' % p.get('post_title')
        print 'content is %s' % p.get('post_content')
        print 'type is %s' % p.get('type')
        conn = db.connect(host='w.rdc.sae.sina.com.cn',port=3307,user='w4z445j54z',passwd='jllx005li3l5j2jl12x35kmlk3mx34k0ijkmz0mx',db='app_reasonz',charset='utf8')
        c=conn.cursor()
        sql="INSERT INTO `wp_posts` (`post_author`, `post_date`, `post_date_gmt`, `post_content`, `post_title`, `post_excerpt`, `post_status`, `comment_status`, `ping_status`, `post_password`, `post_name`, `to_ping`, `pinged`, `post_modified`, `post_modified_gmt`, `post_content_filtered`, `post_parent`, `guid`, `menu_order`, `post_type`, `post_mime_type`, `comment_count`)  VALUES (1, now(), now(), '"+p.get('post_content')+"', '"+p.get('post_title')+"', '', 'publish', 'open', 'open', '', '"+p.get('post_title')+"', '', '', now(), now(), '', 0, '', 0, 'post', '', 0)"
        print sql
        c.execute(sql)
        lastid = int(conn.insert_id())
        print 'last id is ',str(lastid)
        conn.commit()
        sql1="INSERT INTO wp_term_relationships values("+str(lastid)+","+str(p.get('type'))+",0);"
        print sql1
        c.execute(sql1)
        
        c.close()
        conn.close()
    except Exception,e:
        print 'mydb ',e
        exstr = traceback.format_exc()
        print exstr
        print 'mydb insert exception ' , str(sys.exc_info()),str(exstr)
def ishave(title):
    try:
        conn = db.connect(host='w.rdc.sae.sina.com.cn',port=3307,user='w4z445j54z',passwd='jllx005li3l5j2jl12x35kmlk3mx34k0ijkmz0mx',db='app_reasonz',charset='utf8')
        c=conn.cursor()
        sql="select count(*) from wp_posts t where t.post_title='"+title+"'"
        c.execute(sql)
        res = c.fetchone()[0]
        print 'is have  res =',str(res)
        if res and int(res)>0:
            return False
        else:
            return True
    except Exception,e:
        print 'mydb is have ' ,e
#def test(p):
#    sql="INSERT INTO `wp_posts` (`post_author`, `post_date`, `post_date_gmt`, `post_content`, `post_title`, `post_excerpt`, `post_status`, `comment_status`, `ping_status`, `post_password`, `post_name`, `to_ping`, `pinged`, `post_modified`, `post_modified_gmt`, `post_content_filtered`, `post_parent`, `guid`, `menu_order`, `post_type`, `post_mime_type`, `comment_count`)  VALUES (1, now(), now(), '"+p.get('post_content')+"', '"+p.get('post_title')+"', '', 'publish', 'open', 'open', '', '"+p.get('post_title')+"', '', '', now(), now(), '', 0, '', 0, 'post', '', 0)"
#    print sql

