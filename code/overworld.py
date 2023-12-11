from random import choice
from typing import Iterable, Union
import pygame
from pygame.sprite import AbstractGroup 
from code.support import *
from code.sprites.tile import Tile
from code.sprites.player import Player
# from debug import debug
from code.support import *
# from weapon import Weapon
# from ui import UI
# from enemy import Enemy
# from particles import ParticleEffect, AnimationPlayer
#from menu import Menu
from pytmx.util_pygame import load_pygame
from code.battle import Battle


class Overworld:
    def __init__(self, game, level):
        self.game = game
        self.level = level
        #TODO load level through designated json file
        self.entities_path="data/maps/map_Entities.csv"
        self.tmx_data = load_pygame(self.level.map_path)

        # get the display surface 
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup(self.game.display) 
        self.background_sprites = YSortCameraGroup(self.game.display) 
        self.obstacle_sprites = pygame.sprite.Group()
        self.interactable_sprites = pygame.sprite.Group()
        
        # sprite setup
        self.create_map()
        #self.current_attack=None
        
        #UI
        #self.ui=UI()
        self.game_paused=False
        #self.menu = Menu(self.player)#needs to come after create map()
        
        #particles
        #self.animation_player = AnimationPlayer()

    def create_map(self):
        layouts = {
            #'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
            #'grass': import_csv_layout('../map/map_Grass.csv'),
            #'object': import_csv_layout('../map/map_LargeObjects.csv'),
            'entities': import_csv_layout(self.entities_path),
        }
        
        # graphics = {
        #     'grass': import_folder('../graphics/grass'),
        #     'objects': import_folder('../graphics/objects')
        # }
        
        for style,layout in layouts.items():       
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col == '-1':
                        continue # -1 means nothing exists here so skip
                    x = col_index * self.game.settings['TILESIZE']
                    y = row_index * self.game.settings['TILESIZE']
                    # if style == 'boundary':
                    #     if col == '395':
                    #         Tile((x,y),[self.obstacle_sprites],'boundary') #no visible sprites group so it doesn't draw
                    # if style == 'grass':
                    #     random_grass = choice(graphics['grass'])
                    #     Tile((x,y),[self.visible_sprites,self.obstacle_sprites,self.attackable_sprites], 'grass', random_grass)
                    # if style == 'object':
                    #     surf = graphics['objects'][int(col)]
                    #     Tile((x,y),[self.visible_sprites,self.obstacle_sprites], 'object', surf)
                    if style =='entities':
                        if col == '394':
                            self.player = Player(self.game,(x,y),[self.visible_sprites,self.obstacle_sprites])

        # cycle through all layers
        for layer in self.tmx_data.visible_layers:
            # if layer.name in ('Floor', 'Plants and rocks', 'Pipes')
            if hasattr(layer,'data'):
                for x,y,surf in layer.tiles():
                    pos = (x * self.game.settings['TILESIZE'], y * self.game.settings['TILESIZE'])
                    Tile(pos, surf, self.background_sprites)
    
    def begin_encounter(self):
        battle = Battle(self.game, self, ['enemy1', 'enemy2'])
        self.game.current_screen = battle
    
    def run(self):
        self.background_sprites.custom_draw(self.player)
        self.visible_sprites.custom_draw(self.player)
        #self.ui.display(self.player)
        if self.game_paused:
            #do the menu
            self.menu.display()
        else:
            # update and draw the game
            self.visible_sprites.update()
            #self.visible_sprites.enemy_update(self.player)
            #self.player_attack_logic()
            #debug(self.player.status)
  
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, display):
        super().__init__()
        self.display_surface = display
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2(0,0)
        
        #creating the floor
        #self.floor_surface = pygame.image.load('graphics/test/ground.png').convert()
        #self.floor_rect = self.floor_surface.get_rect(topleft=(0,0))
    
    def custom_draw(self,player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        #floor_offset = self.floor_rect.topleft - self.offset
        #self.display_surface.blit(self.floor_surface, floor_offset)
        
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
            
    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
        