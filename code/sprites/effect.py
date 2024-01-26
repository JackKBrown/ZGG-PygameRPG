import pygame
from code.support import *

class Effect(pygame.sprite.Sprite):
    def __init__(self,game,groups,pos,effect_path, blink=False):
        super().__init__(groups)
        self.pos = list(pos)
        self.animation_speed = 0.1
        self.frame_index = 0
        self.animation = import_folder(effect_path)
        self.blink = blink
        self.animate() # this just initialises the image and rect
        
    def animate(self):
        #loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animation):
            self.frame_index =0
        
        self.image = self.animation[int(self.frame_index)]
        self.rect = self.image.get_rect(topleft=self.pos)
        
        if self.blink:
            alpha=wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    
    def update(self):
        self.animate()