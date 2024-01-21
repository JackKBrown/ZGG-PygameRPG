import pygame
import json
import random
from code.support import *

class Ally():
    def __init__(self, ally_path):
        #print("loading level")
        #save_file = open(enemy_path, 'r')
        #self.data = json.load(save_file)
        #save_file.close()
        #self.level_path = enemy_path
        #self.name = self.data['name']
        #self.image_path = self.data['image_path']
        self.name="ally_path"
        self.stats = {
            "hp_max":100,
            "hp":80,
            "ep_max":30,
            "ep":10,
            "speed": random.randint(1,5)
        }
        self.actions={
            "attack":self.attack, 
            "item":self.item
        }
        self.action_stack = []
        self.action_stack.append(self.actions)
        self.status="idle"
        self.blink=False
        self.animation_speed=DEF_ANIM_SPEED
        self.frame_index=0
        self.import_assets()
    
    def import_assets(self):
        character_path = 'graphics/player/'
        self.animations = {'idle': []}
        
        for animation in self.animations.keys():
            full_path=character_path+animation
            self.animations[animation] = import_folder(full_path)
            
        print(self.animations)
    
    def animate(self):
        animation = self.animations[self.status]
        #loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index =0
        
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect()
        
        if self.blink:
            alpha=wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
        
    def select_action(self, action, battle):
        if action == "back" : 
            if len(self.action_stack) > 1:
                self.action_stack.pop() # remove top of stack
        else:
            proposed_action = self.action_stack[-1][action] # get top of stack
            if isinstance(proposed_action, dict):
                self.action_stack.append(proposed_action)
            else:
                self.action_stack = [] # reset action stack to base menu
                self.action_stack.append(self.actions)
                proposed_action(battle)
                
        
    def attack(self, battle):
        if battle.target == None:
            battle.set_target_state(battle.enemies)
        else:
            print("doing attack")
        
    def item(self, battle):
        print("using item")