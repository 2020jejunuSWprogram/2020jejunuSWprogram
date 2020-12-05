import Visual, Game, pygame, time

visual=Visual.Visual()
#visual.board()
game=Game.Game()
radius=5
flag=True
playing=True
symbol_to_direction={'△' : [0,-1], '◁' : [-1,0], '▽' : [0,1], '▷' : [1,0]}
direction=[-1,0]
symbol_to_character={'ම' : 'swirl', '♡' : 'heart', 'ㅡ' : 'horizontal', 'ㅣ' : 'vertical'}
visual.board()
drawing=False
start=time.time()
last_summon=time.time()
enemy_cooltime=5
while playing:
  visual.board()
  visual.show_sprites()
  if time.time()-last_summon>=enemy_cooltime:
    last_summon=time.time()
    game.summon('normal',[100,100],[0,0])
  for event in pygame.event.get():
    if event.type==pygame.MOUSEBUTTONDOWN:
      drawing=True
    elif event.type==pygame.MOUSEBUTTONUP:
      drawing=False
      symbol=visual.read()
      visual.write_display.fill((255,255,255))
      visual.screen.fill((255,255,255))
      visual.board()
      visual.show_sprites()
      pygame.display.flip()
      if symbol in ['△', '◁', '▽', '▷']:
        direction = symbol_to_direction[symbol]
      else:
        kind = symbol_to_character[symbol]
        game.summon(kind, [400, 300], direction)
      print(symbol)
    elif event.type==pygame.QUIT:
      playing=False
  
  if drawing:
    x,y=pygame.mouse.get_pos()
    pygame.draw.circle(visual.write_display,(252, 159, 246),[x,y],radius)
    visual.screen.blit(visual.write_display,(0,0))
    pygame.display.flip()

  game.skill()
  game.kill()
  game.where_should_we_go()
  game.move()

  for characters in game.good_characters.keys():
    visual.sprites[characters]=game.good_characters[characters]
  for characters in game.bad_characters.keys():
    visual.sprites[characters]=game.bad_characters[characters]
  
pygame.quit()

print(time.time()-start)