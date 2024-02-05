import pygame

class Inventory:
    def __init__(self, consumable_dict, equipment_dict):
        #load inventory from json file
        self.consumables=consumable_dict
        self.equipment = equipment_dict
        
        
    def use_item(self):
        pass
    
    def add_item(self, item_name, quantity):
        pass
        