import pygame

class Inventory:
    def __init__(self, inventory_path):
        #load inventory from json file
        self.inventory = {
            "Potion":4,
            "Grt Potion":1,
            "Bomb":0,
            "Antidote": 1
        }
        
    def use_item(self):
        pass
    
    def add_item(self):
        pass
        