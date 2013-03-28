import pygame
import pygame.camera
import pygame.image
from pygame.locals import *
import os
pygame.init()
pygame.camera.init()

cam = pygame.camera.Camera("/dev/video0",(320,240))
cam.start()
img=cam.get_image()
# print img
pygame.image.save(img,"/tmp/1.jpeg")
cmd = 'curl --request POST --data-binary @"/tmp/1.jpeg" \
 		--header "U-ApiKey: b2e7a2f23387644abac884fd06045c3f" \
 		"http://api.yeelink.net/v1.0/device/1052/sensor/1333/photos"'
print cmd
os.popen(cmd)
os.popen("rm /tmp/1.jpeg")
print "finish!"

