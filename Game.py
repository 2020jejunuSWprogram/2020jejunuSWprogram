import time
class Game():
  def __init__(self):
    self.coin=20
    self.hp=5
    self.good_characters={'swirl':[],'heart':[],'horizontal':[],'vertical':[]}#(위치,속도,쿨타임,hp)
    self.good_cooltimes={'swirl':5,'heart':5,'horizontal':5,'vertical':10}
    self.good_summon_prices={'swirl':15,'heart':15,'horizontal':5,'vertical':5}
    self.bad_characters={'normal':[],'fast':[],'aggressive':[]}
    self.bad_cooltimes={'normal':5,'fast':5,'aggressive':5}
    self.bad_rewards={'normal':5,'fast':10,'aggressive':20}
    self.last_update_time=time.time()

  def kill(self):
    for characters in self.good_characters.keys():
      for i in range(len(self.good_characters[characters])):
        if self.good_characters[characters][i]['HP']<=0:
          del self.good_characters[characters][i]
    for characters in self.bad_characters.keys():
      for i in range(len(self.bad_characters[characters])):
        if self.bad_characters[characters][i]['HP']<=0:
          del self.bad_characters[characters][i]
          self.coin+=self.bad_rewards[characters]

  def skill(self):
    for characters in self.good_characters.keys():
      for i in range(len(self.good_characters[characters])):
        self.good_characters[characters][i]['Cooltime']-=(time.time()-self.last_update_time)
        if self.good_characters[characters][i]['Cooltime']<=0:
          self.good_characters[characters][i]['Cooltime']=self.good_cooltimes[characters]
          if characters=='swirl':
            skill_range=50
            skill_power=0.1
            lx,ly=self.good_characters[characters][i]['location']
            for opponents in self.bad_characters.keys():
              for j in range(len(self.bad_characters[opponents])):
                ox,oy=self.bad_characters[opponents][j]['location']
                if ((ox-lx)**2+(oy-ly)**2)**0.5<skill_range:
                  self.bad_characters[opponents][j]['location']=(ox+skill_power*(ox-lx),oy+skill_power*(oy-ly))
          elif characters=='heart':
            skill_range=50
            skill_power=0.1
            lx,ly=self.good_characters[characters][i]['location']
            for opponents in self.bad_characters.keys():
              for j in range(len(self.bad_characters[opponents])):
                ox,oy=self.bad_characters[opponents][j]['location']
                if ((ox-lx)**2+(oy-ly)**2)**0.5<skill_range:
                  self.bad_characters[opponents][j]['location']=(ox-skill_power*(ox-lx),oy-skill_power*(oy-ly))
          elif characters=='horizontal':
            skill_range=10
            lx,ly=self.good_characters[characters][i]['location']
            for opponents in self.bad_characters.keys():
              for j in range(len(self.bad_characters[opponents])):
                ox,oy=self.bad_characters[opponents][j]['location']
                if ((ox-lx)**2+(oy-ly)**2)**0.5<skill_range:
                  self.bad_characters[opponents][j]['HP']-=1
          elif characters=='vertical':
            self.good_characters[characters][i]['HP']+=1
    
    for characters in self.bad_characters.keys():
      for i in range(len(self.bad_characters[characters])):
        self.bad_characters[characters][i]['Cooltime']-=(time.time()-self.last_update_time)
        if self.bad_characters[characters][i]['Cooltime']<=0:
          self.bad_characters[characters][i]['Cooltime']=self.bad_cooltimes[characters]
          skill_range=10
          lx,ly=self.bad_characters[characters][i]['location']
          for opponents in self.good_characters.keys():
            for j in range(len(self.good_characters[opponents])):
              ox,oy=self.good_characters[opponents][j]['location']
              if ((ox-lx)**2+(oy-ly)**2)**0.5<skill_range:
                self.good_characters[opponents][j]['HP']-=1
  
    self.last_update_time=time.time()

  def summon(self,kind,loc,direction):
    if kind in self.good_characters.keys() and self.coin<self.good_summon_prices[kind]:
      return False
    if kind in self.good_characters.keys():
      self.coin-=self.good_summon_prices[kind]
    if kind in self.good_characters.keys():
      self.good_characters[kind].append({'location':loc,'velocity':direction,'Cooltime':self.good_cooltimes[kind],'HP':3})
    elif kind in self.bad_characters.keys():
      self.bad_characters[kind].append({'location':loc,'velocity':direction,'Cooltime':self.bad_cooltimes[kind],'HP':3})

  def move(self):
    move_constant=0.4
    for characters in self.good_characters.keys():
      for i in range(len(self.good_characters[characters])):
        vx,vy=self.good_characters[characters][i]['velocity']
        self.good_characters[characters][i]['location'][0]+=move_constant*vx
        self.good_characters[characters][i]['location'][1]+=move_constant*vy
    for characters in self.bad_characters.keys():
      for i in range(len(self.bad_characters[characters])):
        vx,vy=self.bad_characters[characters][i]['velocity']
        dum=0
        if characters=='fast':
          dum=0.05
        self.bad_characters[characters][i]['location'][0]+=(move_constant+dum)*vx
        self.bad_characters[characters][i]['location'][1]+=(move_constant+dum)*vy
  
  def normalize(self,vector):
    return [vector[0]/((vector[0]**2+vector[1]**2)**0.5),vector[1]/((vector[0]**2+vector[1]**2)**0.5)]

  def where_should_we_go(self):
    for characters in self.good_characters.keys():
      for i in range(len(self.good_characters[characters])):
        md=1001
        lx,ly=self.good_characters[characters][i]['location']
        flag=False
        for opponents in self.bad_characters.keys():
          for j in range(len(self.bad_characters[opponents])):
            ox,oy=self.bad_characters[opponents][j]['location']
            if ((ox-lx)**2+(oy-ly)**2)**0.5<md:
              md=((ox-lx)**2+(oy-ly)**2)**0.5
              mm=self.normalize([ox-lx,oy-ly])
              flag=True
        if flag:
          self.good_characters[characters][i]['velocity']=mm

    for characters in self.bad_characters.keys():
      for i in range(len(self.bad_characters[characters])):
        md=1001
        lx,ly=self.bad_characters[characters][i]['location']
        if characters!='aggressive':
          for opponents in self.good_characters.keys():
            for j in range(len(self.good_characters[opponents])):
              ox,oy=self.good_characters[opponents][j]['location']
              if ((ox-lx)**2+(oy-ly)**2)**0.5<md:
                mm=self.normalize([ox-lx,oy-ly])
        ox,oy=400,300
        if ((ox-lx)**2+(oy-ly)**2)**0.5<md:
          md=((ox-lx)**2+(oy-ly)**2)**0.5
          mm=self.normalize([ox-lx,oy-ly])
        self.bad_characters[characters][i]['velocity']=mm