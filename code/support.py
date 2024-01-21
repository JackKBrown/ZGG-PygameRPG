import json
from math import sin
from csv import reader
from os import walk
import pygame

DEF_ANIM_SPEED=0.1
USER_SETTINGS_FILEPATH = "settings.json"
WIDTH= 1280
HEIGHT= 720
FPS= 60
TILESIZE= 32
SMALL_MARGIN=2
MEDIUM_MARGIN = 5
LARGE_MARGIN = 10
UI_FONT= "graphics/font/joystix.ttf"
UI_FONT_SIZE=11
SMALL_FONT_SIZE=8
LARGE_FONT_SIZE=18
MENU_TEXT= "#665544"
WATER_COLOUR= "#71ddee"
UI_BG_COLOUR= "#222222"
UI_BORDER_COLOUR= "#111111"
TEXT_COLOUR= "#EEEEEE"
HEALTH_COLOUR= "red"
ENERGY_COLOUR= "blue"
UI_BORDER_COLOUR_ACTIVE= "gold"
TEXT_COLOUR_SELECTED= "#111111"
BAR_COLOUR= "#EEEEEE"
BAR_COLOUR_SELECTED= "#111111"
UPGRADE_BG_COLOUR_SELECTED= "#EEEEEE"

def load_user_settings():
    print("loading settings")
    save_file = open(USER_SETTINGS_FILEPATH, 'r')
    settings = json.load(save_file)
    save_file.close()
    return settings
    
def save_user_settings(settings):
    save_file = open(USER_SETTINGS_FILEPATH, 'w')
    json.dump(settings, save_file)
    save_file.close()
 
def wave_value():
    value = sin(pygame.time.get_ticks())
    if value >= 0 :
        return 255
    else:
        return 25   

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