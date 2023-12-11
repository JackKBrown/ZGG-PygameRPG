import json
from csv import reader
from os import walk
import pygame

SETTINGS_FILEPATH = "settings.json"

def load_settings():
    print("loading settings")
    save_file = open(SETTINGS_FILEPATH, 'r')
    settings = json.load(save_file)
    save_file.close()
    return settings
    
def save_settings(settings):
    save_file = open(SETTINGS_FILEPATH, 'w')
    json.dump(settings, save_file)
    save_file.close()
    

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
    return terrain_map

def import_folder(path):
    surface_list=[]
    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf=pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list