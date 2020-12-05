import pygame
import tensorflow as tf
import numpy as np
import time
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

class Visual():
  def __init__(self):
    pygame.init()
    self.write_display = pygame.Surface((800,600))
    self.screen=pygame.display.set_mode((800,600))
    self.screen.blit(self.write_display,(0,0))
    self.screen.fill((255,255,255))
    self.write_display.fill((255,255,255))
    self.write_display.set_colorkey((255,255,255))
    pygame.display.flip()

    self.radius=5
    self.grass=pygame.image.load('./Image/grass.png')
    self.grass=pygame.transform.scale(self.grass,(100,100))
    self.road=pygame.image.load('./Image/road.png')
    self.road=pygame.transform.scale(self.road,(100,100))
    self.sprites={'swirl':[],'heart':[],'horizontal':[],'vertical':[],'normal':[],'fast':[],'aggressive':[]} #((위치 x, 위치 y), 스킬 쿨타임, HP)
    self.sprites_image={}
    for i in self.sprites.keys():
      self.sprites_image[i]=pygame.transform.scale(pygame.image.load('./Image/'+i+'.png'),(50,50))
    self.symbol_model=load_model('network.h5')

  def board(self):
    tiles=[]
    for i in range(8*6):
      if i in [3,4,11,12,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,35,36,43,44]:
        tiles.append(self.road.get_rect())
      else:
        tiles.append(self.grass.get_rect())
    for i in range(8*6):
      tiles[i].center=(50+(i%8)*100,50+(i//8)*100)
      if i in [3,4,11,12,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,35,36,43,44]:
        self.screen.blit(self.road,tiles[i])
      else:
        self.screen.blit(self.grass,tiles[i])

    pygame.display.flip()

  def show_sprites(self):
    character_rects=[]
    for characters in self.sprites.keys():
      for character in self.sprites[characters]:
        character_rects.append(self.sprites_image[characters].get_rect())
        character_rects[-1].center=character['location']
        self.screen.blit(self.sprites_image[characters], character_rects[-1])

    pygame.display.flip()

  def read(self):
    pv=np.array(pygame.PixelArray(self.write_display))
    pv=np.where(pv==16777215,0,1)
    pv_shrink=np.zeros((1,32,32,1))
    up=601
    down=0
    for i in range(800):
      flag=False
      for j in range(600):
        if pv[i][j]==1:
          down=max(down,j)
          if not flag:
            flag=True
            up=min(up,j)

    left=801
    right=0
    for i in range(600):
      flag=False
      for j in range(800):
        if pv[j][i]==1:
          right=max(right,j)
          if not flag:
            flag=True
            left=min(left,j)

    pv=pv[left:right,up:down]
    wanted_size=int(max(right-left,down-up)*1.5)
    pv=np.pad(pv,((((wanted_size-right+left)//2),((wanted_size-right+left)//2)),(((wanted_size-down+up)//2),((wanted_size-down+up)//2))),'constant',constant_values=0)

    for i in range(32):
      for j in range(32):
        pv_shrink[0,j,i,0]=np.mean(pv[i*wanted_size//32:(i+1)*wanted_size//32,j*wanted_size//32:(j+1)*wanted_size//32])

    percentage=self.symbol_model.predict(pv_shrink)
    
    symbols='ම ♡ ㅡ ㅣ △ ◁ ▽ ▷'
    symbols=symbols.split()
    mx=-1
    for i, per in enumerate(percentage[0]):
      if per>mx:
        mx=per
        mm=i

    return symbols[mm]