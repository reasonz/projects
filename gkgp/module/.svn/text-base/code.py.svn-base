#-*- coding:utf-8 -*-
__author__ = 'hpwang'
from lib.bottle import Bottle,response
import sys,hashlib,traceback,StringIO
#导入三个模块
import Image,ImageDraw,ImageFont,ImageFilter
import random,math
import verifycode
from setting import    SITE_DOMAIN,SECRET_KEY,VREYCODE

reload(sys)
sys.setdefaultencoding('utf-8')
app = Bottle()

def createCode(w,h):
  #图片宽度  
  width = w 
  #图片高度  
  height = h  
  #背景颜色  
  bgcolor = (255,255,255) 
  #生成背景图片
  image = Image.new("RGB",(width,height),bgcolor)
  #加载字体
  font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf",30)
  #字体颜色
  fontcolor = (0,0,0)
  #产生draw对象，draw是一些算法的集合
  draw = ImageDraw.Draw(image)
  #画字体,(0,0)是起始位置
  draw.text((0,0),'1234',font=font,fill=fontcolor)
  #释放draw
  del draw
  #保存原始版本
  return image



@app.route('/')
@app.route('/code')
def get_code():
  try: 
    stringio = StringIO.StringIO()
    code_img = verifycode.create_validate_code()
    img = code_img[0]
    img.save(stringio, "GIF") 
    print code_img[1]
    addValInCookie(VREYCODE,code_img[1])
    response.headers['Content-Type'] = 'image/jpeg'
    return stringio.getvalue()
    #response.body=stringio.getvalue()
    #return response
  except:
    traceback.print_exc() 





def addValInCookie(name,val):
    response.set_cookie(name,val,secret=SECRET_KEY,path='/')