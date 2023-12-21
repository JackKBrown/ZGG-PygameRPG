from random import choice
from typing import Iterable, Union
import pygame, sys
from pygame.sprite import AbstractGroup 
from code.support import *
from code.sprites.tile import Tile
from code.sprites.player import Player
from code.sprites.npc import NPC
from code.sprites.door import Door
# from debug import debug
from code.support import *
# from weapon import Weapon
# from ui import UI
# from enemy import Enemy
# from particles import ParticleEffect, AnimationPlayer
from code.menu import Menu
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
        self.event_sprites = pygame.sprite.Group()
        
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
        

        # cycle through all layers
        for layer in self.tmx_data.visible_layers:
            print(layer.name)
            if layer.name in ('walls', 'obstacles'):
                if hasattr(layer,'data'):
                    for x,y,surf in layer.tiles():
                        pos = (x * self.game.settings['TILESIZE'], y * self.game.settings['TILESIZE'])
                        Tile(pos, surf, [self.background_sprites,self.obstacle_sprites])
            elif layer.name in ("npcs"):
                if hasattr(layer, 'data'):
                    for x,y,surf in layer.tiles():
                        pos = (x * self.game.settings['TILESIZE'], y * self.game.settings['TILESIZE'])
                        NPC(self.game, pos, [self.visible_sprites, self.obstacle_sprites], "custom behaviour")
            elif layer.name in ("doors"):
                print(layer)
                print (layer.__dict__)
                print (layer[0].__dict__)
                for door in layer:
                    print(door)
                    name = door.name
                    x = door.x
                    y = door.y
                    h = door.height
                    w = door.width
                    if door.type == "passage":
                        link = door.properties['link'] #name of another door
                    else:
                        link = None
                    Door((x,y),pygame.Surface((w,h)), name, link, [self.visible_sprites, self.event_sprites])
            else:
                if hasattr(layer,'data'):
                    for x,y,surf in layer.tiles():
                        pos = (x * self.game.settings['TILESIZE'], y * self.game.settings['TILESIZE'])
                        Tile(pos, surf, self.background_sprites)
            print(self.level.start_pos)
            for location in self.event_sprites:
                print(location.name)
                if location.name == self.level.start_pos:
                    x = (location.rect.x // self.game.settings['TILESIZE']) * self.game.settings['TILESIZE']
                    y = (location.rect.y // self.game.settings['TILESIZE']) * self.game.settings['TILESIZE']
                    self.player = Player(self.game,(x,y),[self.visible_sprites,self.obstacle_sprites])
                    
        ##pygame.quit()
        #sys.exit()
    
    def begin_encounter(self):
        battle = Battle(self.game, self, ['enemy1', 'enemy2'])
        self.game.current_screen = battle
    
    def load_overworld(self, rect):
        for sprite in self.event_sprites:
            if rect.colliderect(sprite.rect):
                if hasattr(sprite, 'link') and sprite.link != None:
                    #start pos is a string tied to a location on the map
                    self.game.load_level(self.level.level_path, sprite.link)
    
    def open_menu(self):
        menu = Menu(self.game, self)
        self.game.current_screen = menu
        
    def collide_obstacle(self, rect):
        return self.collision(self.obstacle_sprites, rect)
    
    def collide_event(self, rect):
        return self.collision(self.event_sprites,rect)
    
    def collision(self, group, rect):
        for sprite in group:
            if sprite.rect.colliderect(rect):
                return True
    
    def input(self):
        for event in self.game.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.begin_encounter()
                if event.key == pygame.K_m:
                    self.open_menu()
    
    def run(self):
        self.background_sprites.custom_draw(self.player)
        self.visible_sprites.custom_draw(self.player)
        #self.ui.display(self.player)
        self.visible_sprites.update()
        self.input()
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
    
    def custom_draw(self,player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
            
    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
        