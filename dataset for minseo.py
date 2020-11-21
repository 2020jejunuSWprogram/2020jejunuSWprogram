import pygame
import numpy as np

pygame.init()
screen=pygame.display.set_mode((256,256))
screen.fill((255,255,255))
pygame.display.flip()
flag=False
radius=5
while True:
    drawing=True
    while drawing:
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                flag=True
            if event.type==pygame.MOUSEBUTTONUP:
                flag=False
            if event.type==pygame.KEYDOWN:
                drawing=False

        if flag:
            x,y=pygame.mouse.get_pos()
            pygame.draw.circle(screen,(0,0,0),[x,y],radius)
            pygame.display.flip()

    pv=np.array(pygame.PixelArray(screen))
    pv=np.where(pv!=0,0,1)
    pv_shrink=np.zeros((32,32))
    for i in range(32):
        for j in range(32):
            pv_shrink[j,i]=np.mean(pv[i*8:(i+1)*8,j*8:(j+1)*8])
    f=open('class_swirl.txt','a')
    pv_shrink=pv_shrink.flatten()
    print(len(pv_shrink))
    for i in pv_shrink:
        f.write(str(i)+',')
    f.write('\n')
    screen.fill((255,255,255))
    pygame.display.flip()
