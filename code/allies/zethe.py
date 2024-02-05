from code.allies.ally import Ally
import pygame

class Zethe(Ally):
    def __init__(self,game, ally_path):
        super().__init__(game, ally_path)
        self.name="Zethe Wayright"
        self.action_stack.pop()
        self.actions = {
            "attack": self.attack, 
            "magic":{
                "fire":self.fire
                }, 
            "utopic":{
                "VRO":self.vro
                }, 
            "item":self.fetch_item_list
        }
        self.action_stack.append(self.actions)
        
    def fire(self, battle):
        print("fire")
        
    def vro(self, battle):
        print("vro")
