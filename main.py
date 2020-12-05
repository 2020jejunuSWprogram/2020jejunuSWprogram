import Visualize
import Game

game=Game.Game()
visualize=Visualize.Visualize()


      
while True:
  drawing=True
  start=time.time()
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
      pygame.draw.circle(write_display,(252, 159, 246),[x,y],radius)
      screen.blit(write_display,(0,0))
      pygame.display.flip()

    if time.time()-start>=0.1:
      game.kill()
      visualize.show_sprites()
      game.skill()
      start=time.time()
      

  write_display.fill((255,255,255))
  screen.fill((255,255,255))
  #read()
  board()
  #summon()
  pygame.display.flip()
