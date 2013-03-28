# import redis
# # init redis
# class MyRedis():
#     def __init__(self):
#         self.rd = redis.StrictRedis(host='10.151.20.49', port=6379, db=0)

#     # add tags when user upload vedios
#     def addtags(self,tags):
#         if tags :
#             pipe = self.rd.pipeline()
#             for tag in tags.split(','):
#                 if len(tag):
#                     pipe.zincrby('gkgp:tags',tag)
#             pipe.execute()
#             return True
#         else:
#             return False

#     # get tags by score
#     def sorttags(self,limit):
#         return self.rd.zrevrange('gkgp:tags',0,limit,True)

# if __name__ =='__main__':
#     r = MyRedis()
#     r.addtags('asdf,asdf,3df,3,fg,df,y,afa,df')
#     print r.sorttags(10)