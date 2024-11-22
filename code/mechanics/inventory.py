import pygame

class Inventory:
    def __init__(self, consumable_dict, equipment_dict):
        #load inventory from json file
        self.consumables=consumable_dict
        self.equipment = equipment_dict
       
    def get_item_list(self):
        item_list={}
        for item in self.consumables:
            if self.consumables[item] > 0:
                new_name=f"{self.consumables[item]} {item}"
                item_list[new_name] = item
        return item_list
               
    def use_item(self):
        pass
    
    def add_item(self, item_name, quantity):
        pass
        