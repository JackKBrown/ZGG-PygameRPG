import pygame
import json

class Level():
    def __init__(self, level_path):
        print("loading level")
        save_file = open(level_path, 'r')
        self.data = json.load(save_file)
        save_file.close()
        self.level_path = level_path
        self.name = self.data['name']
        self.map_path = self.data['map_path']
        self.start_pos = self.data['start_pos']
        