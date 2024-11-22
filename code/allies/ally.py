import pygame
import json
import random
from code.support import *

class Ally():
    def __init__(self,game,ally_path):
        self.game = game
        #print("loading level")
        #save_file = open(enemy_path, 'r')
        #self.data = json.load(save_file)
        #save_file.close()
        #self.level_path = enemy_path
        #self.name = self.data['name']
        #self.image_path = self.data['image_path']
        self.face_image = pygame.image.load("graphics/test/zethearmour.png").convert_alpha()
        self.name="def_ally"
        self.stats = {
            "hp_max":100,
            "hp":80,
            "ep_max":30,
            "ep":10,
            "speed": 5 + random.randint(1,20), #This needs changing
            "str": 10,
            "def": 10
        }
        self.actions={
            "attack":self.attack, 
            "item":self.fetch_item_list
        }
        self.action_stack = []
        self.action_stack.append(self.actions)
        self.in_inventory = False
        self.status="idle"
        self.blink=False
        self.animation_speed=DEF_ANIM_SPEED
        self.frame_index=0
        self.import_assets()
        self.pos=(0,0)
        self.consumable_actions = {
            "Potion": self.use_potion,
            "Grt Potion":self.use_great_potion,
            "Bomb":self.use_bomb,
            "Antidote": self.use_antidote
        }
    
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
        
    def select_action(self, action, battle):
        if action == "back" : 
            if len(self.action_stack) > 1:
                if self.in_inventory:
                    self.in_inventory=False
                battle.select_index=0
                self.action_stack.pop() # remove top of stack
        else:
            #must have at least one valid action
            if len(self.action_stack[-1]) != 0:
                proposed_action = self.action_stack[-1][action] # get top of stack
                if isinstance(proposed_action, dict):
                    battle.select_index=0
                    self.action_stack.append(proposed_action)
                elif self.in_inventory:
                    item_action = self.consumable_actions[proposed_action]
                    battle.player_action=item_action
                    item_action(battle)
                else:
                    battle.player_action=proposed_action
                    proposed_action(battle)
    
    def reset_action(self,battle):
        self.in_inventory=False
        self.action_stack = [] # reset action stack to base menu
        self.action_stack.append(self.actions)
        battle.state="Initiative"
        battle.target=None
        
    def fetch_item_list(self, battle):
        battle.proposed_action=None # reset this as you need to choose the item still
        self.in_inventory=True
        #get list of items which you have an inventory of and append it to action stack
        battle.select_index=0
        self.action_stack.append(self.game.inventory.get_item_list())
        print("fetching item list")
        
    def attack(self, battle):
        if battle.target == None:
            battle.set_target_state(battle.enemies)
        else:
            print("doing attack")
            self.reset_action(battle)
        
#ITEMS
  
    def use_potion(self,battle):
        if battle.target == None:
            battle.set_target_state(battle.allies)
        else:
            print("using potion")
            self.reset_action(battle)
    
    def use_great_potion(self, battle):
        pass
    
    def use_bomb(self,battle):
        pass
    
    def use_antidote(self, battle):
        pass