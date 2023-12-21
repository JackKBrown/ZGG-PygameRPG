import pygame
#from code.support import *
from code.sprites.entity import Entity

class NPC(Entity):
    def __init__(self, game, pos,groups,behavior):
        super().__init__(groups,pos,game)
        self.image = pygame.image.load('graphics/test/zethearmour.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.speed =1
        
    def update(self):
        super().update()
        if self.dest_tile == None:
            if self.pos[0] < 200:
                self.direction.x = 1
            elif self.pos[0] > 400:
                self.direction.x =-1
        
            