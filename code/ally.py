import pygame
import json

class Ally():
    def __init__(self, ally_path):
        #print("loading level")
        #save_file = open(enemy_path, 'r')
        #self.data = json.load(save_file)
        #save_file.close()
        #self.level_path = enemy_path
        #self.name = self.data['name']
        #self.image_path = self.data['image_path']
        if ally_path == "blargel":
            self.image = pygame.image.load('graphics/test/crabstill.png').convert_alpha()
        else:
            self.image = pygame.image.load('graphics/test/zethearmour.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (0,0))
        self.stats = {
            "hp_max":100,
            "hp":80,
            "ep_max":30,
            "ep":10
        }