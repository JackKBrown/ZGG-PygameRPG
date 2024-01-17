import pygame
from code.support import *
from code.enemy import Enemy
from code.ally import Ally

class Battle():
    def __init__(self, game, overworld, enemies):
        self.game = game
        self.overworld = overworld 
        self.enemies=[]
        self.allies=[
            Ally("blargle"),
            Ally("blargle")
        ]
        # pass the overworld into the battle so it can give it back to the game loop when the encounter is over
        for monster in enemies:
            self.enemies.append(Enemy(f"data//enemies//{str(monster)}.json"))
        self.enemy_postition= [
            (0.6,0.4),
            (0.7,0.5),
            (0.7,0.3),
            (0.6,0.6),
            (0.6,0.2),
            (0.8,0.3),
            (0.9,0.6),
            (0.8,0.2)
        ]
        self.ally_position = [
            (0.3,0.4),
            (0.2,0.5),
            (0.2,0.3)
        ]
        #character info 
        self.info_width = self.game.display.get_size()[0] / 5 
        self.info_height = self.game.display.get_size()[1] * 0.2
        self.info_margin = self.info_width / 5
        self.info_top = self.game.display.get_size()[1] - (self.info_height + self.info_margin)
        self.create_character_info()
     
    def input(self):
        for event in self.game.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_battle()
        # if self.can_move:
        #     if keys[pygame.K_d]:
        #         self.select_index+=1
    
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_move:
            if current_time-self.select_time >= 300:
                self.can_move=True
         
    def exit_battle(self):
        self.game.current_screen = self.overworld
        
    def create_character_info(self):
        self.character_info_list = []
        for index, ally in enumerate(self.allies):
            left = (index * (self.info_width+ self.info_margin)) + self.info_margin
            item = CharacterInfo(self.game, ally, left, self.info_top, self.info_width, self.info_height)
            self.character_info_list.append(item)
            
    def display(self):
        floor_surface = pygame.image.load('graphics/test/battlefield.png').convert()
        floor_rect = floor_surface.get_rect(topleft=(0,0))
        self.game.display.blit(floor_surface, (0,0))
        for index,enemy in enumerate(self.enemies):
            x = self.game.display.get_size()[0] * self.enemy_postition[index][0]
            y = self.game.display.get_size()[1] * self.enemy_postition[index][1]
            self.game.display.blit(enemy.image, (x,y))
        for index,ally in enumerate(self.allies):
            x = self.game.display.get_size()[0] * self.ally_position[index][0]
            y = self.game.display.get_size()[1] * self.ally_position[index][1]
            self.game.display.blit(ally.image, (x,y))
        for index, item in enumerate(self.character_info_list):
            # get attributes
            item.display(self.game.display)
           
    def run(self):
        #self.cooldowns()
        self.input()
        self.display()
        #display background
        #display enemies
        #display players
        
class BattleMenu():
    def __init__(self, game, character, l, t, w, h):
        self.game = game
        
class CharacterInfo():
    def __init__(self, game, character, l, t, w, h):
        self.game = game
        self.character = character
        self.rect = pygame.Rect(l,t,w,h, border_radius=15)
        #load image / create rectangle
        #
    
    def display_bar(self, surface, current, max, bg_rect, colour):
        pygame.draw.rect(surface, UI_BG_COLOUR,bg_rect)
        ratio = current/max
        current_width = int(bg_rect.width*ratio)
        current_bar_rect = pygame.Rect(bg_rect.left,bg_rect.top,current_width,bg_rect.height)
        pygame.draw.rect(surface,colour,current_bar_rect)
        pygame.draw.rect(surface,UI_BORDER_COLOUR,bg_rect,2)
    
    #should pass in the currently active character? to highlight?
    def display(self, surface):
        pygame.draw.rect(surface, UI_BG_COLOUR, self.rect)
        pygame.draw.rect(surface,UI_BORDER_COLOUR,self.rect,1)
        #Name
        name_surf =  self.game.font.render("Zethe", False, TEXT_COLOUR)
        name_rect = name_surf.get_rect(midtop = self.rect.midtop +pygame.math.Vector2(0,SMALL_MARGIN))
        surface.blit(name_surf, name_rect)
        #HP
        hp_offset = pygame.math.Vector2(self.rect.left + SMALL_MARGIN, name_rect.bottom + SMALL_MARGIN)
        hp_string = f"HP{self.character.stats['hp']: 4d}/{self.character.stats['hp_max']: 4d}"
        hp_surf = self.game.small_font.render(hp_string, False, HEALTH_COLOUR)
        hp_rect = hp_surf.get_rect(topleft = hp_offset)
        surface.blit(hp_surf, hp_rect)
        
        hp_bar_rect = pygame.Rect(
            hp_offset.x + hp_rect.width +SMALL_MARGIN,
            hp_offset.y,
            (self.rect.right - hp_rect.right) - (2*SMALL_MARGIN),
            hp_rect.height
        )
        self.display_bar(surface, self.character.stats["hp"], self.character.stats["hp_max"], hp_bar_rect, HEALTH_COLOUR)
        
        #EP
        ep_offset = pygame.math.Vector2(self.rect.left + SMALL_MARGIN, hp_rect.bottom + SMALL_MARGIN)
        ep_string = f"EP{self.character.stats['ep']: 4d}/{self.character.stats['ep_max']: 4d}"
        ep_surf = self.game.small_font.render(ep_string, False, ENERGY_COLOUR)
        ep_rect = ep_surf.get_rect(topleft = ep_offset)
        surface.blit(ep_surf, ep_rect)
        
        ep_bar_rect = pygame.Rect(
            ep_offset.x + ep_rect.width +SMALL_MARGIN,
            ep_offset.y,
            (self.rect.right - ep_rect.right) - (2*SMALL_MARGIN),
            ep_rect.height
        )
        self.display_bar(surface, self.character.stats["ep"], self.character.stats["ep_max"], ep_bar_rect, ENERGY_COLOUR)
        
        