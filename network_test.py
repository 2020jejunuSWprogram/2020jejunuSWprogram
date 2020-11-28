from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np
import pygame

symbol_model=load_model('network.h5')

pygame.init()
screen=pygame.display.set_mode((256,256))
screen.fill((255,255,255))
pygame.display.flip()
flag=False
radius=5

def predict_symbol(percentage):
  symbols='ම ♡ ㅡ ㅣ △ ◁ ▽ ▷'
  symbols=symbols.split()
  mx=-1
  for i, per in enumerate(percentage):
    if per>mx:
      mx=per
      mm=i

  return symbols[mm]

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
  pv_shrink=np.zeros((1,32,32,1))
  for i in range(32):
    for j in range(32):
      pv_shrink[0,j,i,0]=np.mean(pv[i*8:(i+1)*8,j*8:(j+1)*8])
  predict_data=symbol_model.predict(pv_shrink)
  print(predict_symbol(predict_data[0]))
  screen.fill((255,255,255))
  pygame.display.flip()
