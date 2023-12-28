import pygame
import json

class Enemy():
    def __init__(self, enemy_path):
        print("loading level")
        save_file = open(enemy_path, 'r')
        self.data = json.load(save_file)
        save_file.close()
        self.level_path = enemy_path
        self.name = self.data['name']
        self.image_path = self.data['image_path']
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (0,0))