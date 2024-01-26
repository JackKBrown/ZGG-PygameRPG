import pygame
import json
import random
from code.support import *

class Enemy():
    def __init__(self, enemy_path):
        print("loading Enemy")
        save_file = open(enemy_path, 'r')
        self.data = json.load(save_file)
        save_file.close()
        self.level_path = enemy_path
        self.name = self.data['name']
        self.image_path = self.data['image_path']
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (0,0))
        self.stats = self.data["stats"]
        self.stats["speed"] + random.randint(1,20)
        self.blink = False
        self.status= "idle"
        self.animation_speed=DEF_ANIM_SPEED
        self.frame_index=0
        self.import_assets()
        self.pos=(0,0)
    
    def import_assets(self):
        character_path = 'graphics/player/'
        self.animations = {'idle': []}
        
        for animation in self.animations.keys():
            full_path=character_path+animation
            self.animations[animation] = import_folder(full_path)
        
    def animate(self):
        animation = self.animations[self.status]
        #loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index =0
        
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(topleft=self.pos)
        
        if self.blink:
            alpha=wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    
    def take_turn(self, battle):
        #return an action function that takes battle as input
        return self.attack
    
    def attack(self, battle):
        print("doing attack")
        battle.state="Initiative"