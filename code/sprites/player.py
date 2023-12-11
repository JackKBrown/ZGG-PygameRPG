import pygame 
#from code.support import *
from code.sprites.entity import Entity

class Player(Entity):
    def __init__(self, game, pos,groups):
        super().__init__(groups,pos,game)
        self.image = pygame.image.load('graphics/test/zethearmour.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        
        
    def input(self):
        #print(self.pos)
        keys = pygame.key.get_pressed()
        
        #movement input
        if self.destination == self.pos:
            if keys[pygame.K_w]:
                self.direction.x=0
                self.direction.y=-1
                self.facing='up'
            elif keys[pygame.K_s]:
                self.direction.x=0
                self.direction.y=1
                self.facing='down'
            elif keys[pygame.K_a]:
                self.direction.y=0
                self.direction.x=-1
                self.facing='left'
            elif keys[pygame.K_d]:
                self.direction.y=0
                self.direction.x=1
                self.facing='right'
            else:
                self.direction.x=0
                self.direction.y=0
    
    def update(self):
        super().update()
        self.input()
        #self.cooldowns()
        #happens before so can check status for attacking
        #self.get_status()
        