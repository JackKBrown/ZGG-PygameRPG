import pygame
from settings import *

class Menu():
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_nr=len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = player.max_stats
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        
        #Bar dimensions
        self.height = self.display_surface.get_size()[1] *0.8
        self.top_margin = self.display_surface.get_size()[1] *0.1
        
        self.width = self.display_surface.get_size()[0] // (self.attribute_nr + 1)
        self.left_margin = self.width//(self.attribute_nr + 1)
        self.create_items()
        #selection system
        self.select_index = 0
        self.select_time = None
        self.can_move = True
        
    def create_items(self):
        self.item_list = []
        for index in range(self.attribute_nr):
            left = self.left_margin + ((self.width+self.left_margin)*index)
            top = self.top_margin
            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)
    
    def input(self):
        keys = pygame.key.get_pressed()
        if self.can_move:
            if keys[pygame.K_d]:
                self.select_index+=1
                self.can_move=False
                self.select_time=pygame.time.get_ticks()
            elif keys[pygame.K_a]:
                self.select_index-=1
                self.can_move=False
                self.select_time=pygame.time.get_ticks()
            elif keys[pygame.K_SPACE]:
                self.can_move=False
                self.select_time=pygame.time.get_ticks()
                print(self.select_index)
            
            if self.select_index >= len(self.attribute_names):
                self.select_index=0
    
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_move:
            if current_time-self.select_time >= 300:
                self.can_move=True
    
    def display(self):
        self.input()
        for index, item in enumerate(self.item_list):
            # get attributes
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = list(self.max_values.values())[index]
            cost = self.player.get_cost_by_index(index)
            item.display(self.display_surface,self.select_index,name,value,max_value,cost)
        self.cooldowns()

class Item():
    def __init__(self, l, t, w, h, index, font):
        self.rect = pygame.Rect(l,t,w,h)
        self.index = index 
        self.font = font
    
    def display_names(self, surface, name, cost, selected):
        #title
        title_surf = self.font.render(name, False, TEXT_COLOUR)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop +pygame.math.Vector2(0,20))
        #costs
        cost_surf = self.font.render(f"{int(cost)}", False, TEXT_COLOUR)
        cost_rect = title_surf.get_rect(midbottom = self.rect.midbottom -pygame.math.Vector2(0,20))
        #draw
        surface.blit(title_surf,title_rect)
        surface.blit(cost_surf,cost_rect)
        
    def display(self, surface, selection_num,name, value, max_value, cost):
        pygame.draw.rect(surface,UI_BG_COLOUR,self.rect)
        self.display_names(surface, name,cost,False)
        