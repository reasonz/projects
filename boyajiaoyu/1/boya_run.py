#!/usr/bin/python
# -*- coding: utf-8 -*-
from module import app
from lib.bottle import run,static_file,debug,request

import setting


@app.route('/static/<filename:path>')
def static(filename):
    return static_file(filename,'./static/')

if __name__ == '__main__':
    debug(True)
    run(app, host="0.0.0.0",port=9990,reloader=True)
  