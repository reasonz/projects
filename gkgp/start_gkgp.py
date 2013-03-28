#!/usr/bin/python
# -*- coding: utf-8 -*-
from module import app
from lib.bottle import run,static_file,debug,request
from gevent import monkey; monkey.patch_all()
from module import main
from setting import STATIC_PATH

@app.route('/static/<filename:path>')
def static(filename):
    return static_file(filename,STATIC_PATH)

@app.route('/')
def root_index():
    return main.index()


if __name__ == '__main__':
    debug(True)
    #run(app, host="0.0.0.0",port=9090,reloader=True)
    run(app, host="0.0.0.0",port=9090,reloader=True,server='gevent')

