import logging,os

class Mylogger():
    def __init__(self,key,path):
        self.logger = logging.getLogger(key)
        if not os.path.exists(path):
            os.mkdir(path)
        logfile = path +key +'.log'
        hdlr = logging.FileHandler(logfile)
        formatter = logging.Formatter('%(asctime)s %(name)s  %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.NOTSET)

    def log(self, msg):
        print 'logname:' + self.logger.name
        if self.logger is not None:
            self.logger.info(msg)

