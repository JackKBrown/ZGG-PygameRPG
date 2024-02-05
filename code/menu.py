import pygame
from code.support import *

class Menu():
    def __init__(self, game, overworld):
        self.game = game
        self.allies = self.game.party
        self.overworld = overworld 
        self.display_surface = self.game.display
        self.font = pygame.font.Font(self.game.settings["UI_FONT"], self.game.settings["UI_FONT_SIZE"])
        
        #options
        self.options = {
            "items": 1, 
            "equip":2, 
            "party":3, 
            "setting":4
        }
        
        op_menu_width = (self.game.display.get_size()[0] / 3) - (LARGE_MARGIN)
        op_menu_height = self.game.display.get_size()[1] - (2* LARGE_MARGIN)
        sub_menu_l = op_menu_width + (2*LARGE_MARGIN)
        sub_menu_width = 2* op_menu_width
        
        self.option_menu = OptionMenu(
            game, 
            LARGE_MARGIN, 
            LARGE_MARGIN, 
            op_menu_width,
            op_menu_height)
        
        self.character_menu = CharacterMenu(
            game, 
            sub_menu_l, 
            LARGE_MARGIN, 
            sub_menu_width,
            op_menu_height
        )
        
        #selection system
        self.select_index = 0
        self.sub_select_index = -1
        self.sub_select = False
        
    
    def input(self):
        for event in self.game.events:
            if event.type == pygame.KEYDOWN:
                if self.sub_select:
                    pass
                else: 
                    if event.key == pygame.K_s:
                        if self.select_index < len(self.options)-1:
                            self.select_index += 1
                    if event.key == pygame.K_w:
                        if self.select_index > 0:
                            self.select_index -= 1
                    if event.key == pygame.K_RIGHT:
                        pass
                        #select current select_index
                    if event.key == pygame.K_LEFT:
                        pass
                        #go back or if on top menu exit_menu
                    if event.key == pygame.K_SPACE:
                        self.exit_menu()

    def exit_menu(self):
        self.game.current_screen = self.overworld
    
    def display(self):
        self.option_menu.display(self.display_surface,self.options,self.select_index)
        self.character_menu.display(self.display_surface,self.allies,self.sub_select_index) 
                
    def run(self):
        self.input()
        self.display()

class OptionMenu():
    def __init__(self, game, l, t, w, h):
        self.game = game
        self.rect = pygame.Rect(l,t,w,h, border_radius=15)
        self.top_of_list = 0
        
    def display_option(self, surface, top, name, hover):
        #action
        name_surf =  self.game.font.render(name, False, TEXT_COLOUR)
        box_rect = pygame.Rect(self.rect.left + 2, top, self.rect.width - 4, name_surf.get_height() + 4)
        name_rect = name_surf.get_rect(topleft = box_rect.topleft +pygame.math.Vector2(2,2))  
        surface.blit(name_surf, name_rect)
        if hover:
            pygame.draw.rect(surface,"#EEE000",box_rect,1)    
        return name_rect.bottom                      
        
    def display(self, surface, options, select_index):
        pygame.draw.rect(surface, UI_BG_COLOUR, self.rect)
        pygame.draw.rect(surface,UI_BORDER_COLOUR,self.rect,1)
        top = self.rect.top + SMALL_MARGIN
        #detirmine the range you're showing here then only look at options in that range? e.g for option in enumerate between index 5 and 8
        for index, option in enumerate(options):
            if index <= self.top_of_list+4:
                top = self.display_option(surface, top, option, index==select_index)
                
class CharacterMenu():
    def __init__(self, game, l, t, w, h):
        self.game = game
        self.rect = pygame.Rect(l,t,w,h, border_radius=15)
        self.top_of_list = 0
        
    def display_bar(self, surface, current, max, bg_rect, colour):
        pygame.draw.rect(surface, UI_BG_COLOUR,bg_rect)
        ratio = current/max
        current_width = int(bg_rect.width*ratio)
        current_bar_rect = pygame.Rect(bg_rect.left,bg_rect.top,current_width,bg_rect.height)
        pygame.draw.rect(surface,colour,current_bar_rect)
        pygame.draw.rect(surface,UI_BORDER_COLOUR,bg_rect,2)
        
    def display_character(self, surface, top, character, hover):
        #character image
        image_rect = character.face_image.get_rect(topleft = (self.rect.left + 2, top +MEDIUM_MARGIN))
        surface.blit(character.face_image, image_rect)
        pygame.draw.rect(surface,"#FF0044",image_rect,1) 
        
        name = character.name
        name_surf =  self.game.font.render(name, False, TEXT_COLOUR)
        box_rect = pygame.Rect(image_rect.right + 2, top, 
                               self.rect.width - 4, 
                               name_surf.get_height() + 4)
        name_rect = name_surf.get_rect(topleft = box_rect.topleft +pygame.math.Vector2(2,2))  
        surface.blit(name_surf, name_rect)
        #HP
        hp_offset = pygame.math.Vector2(image_rect.right + SMALL_MARGIN, name_rect.bottom + SMALL_MARGIN)
        hp_string = f"HP{character.stats['hp']: 4d}/{character.stats['hp_max']: 4d}"
        hp_surf = self.game.small_font.render(hp_string, False, HEALTH_COLOUR)
        hp_rect = hp_surf.get_rect(topleft = hp_offset)
        surface.blit(hp_surf, hp_rect)
        
        hp_bar_rect = pygame.Rect(
            hp_offset.x + hp_rect.width +SMALL_MARGIN,
            hp_offset.y,
            (self.rect.right - hp_rect.right) - (2*SMALL_MARGIN),
            hp_rect.height
        )
        self.display_bar(surface, character.stats["hp"], character.stats["hp_max"], hp_bar_rect, HEALTH_COLOUR)
        
        #EP
        ep_offset = pygame.math.Vector2(image_rect.right + SMALL_MARGIN, hp_rect.bottom + SMALL_MARGIN)
        ep_string = f"EP{character.stats['ep']: 4d}/{character.stats['ep_max']: 4d}"
        ep_surf = self.game.small_font.render(ep_string, False, ENERGY_COLOUR)
        ep_rect = ep_surf.get_rect(topleft = ep_offset)
        surface.blit(ep_surf, ep_rect)
        
        ep_bar_rect = pygame.Rect(
            ep_offset.x + ep_rect.width +SMALL_MARGIN,
            ep_offset.y,
            (self.rect.right - ep_rect.right) - (2*SMALL_MARGIN),
            ep_rect.height
        )
        self.display_bar(surface, character.stats["ep"], character.stats["ep_max"], ep_bar_rect, ENERGY_COLOUR)
        if hover:
            pygame.draw.rect(surface,"#EEE000",box_rect,1)    
        return ep_bar_rect.bottom                      
        
    def display(self, surface, characters, select_index):
        pygame.draw.rect(surface, UI_BG_COLOUR, self.rect)
        pygame.draw.rect(surface,UI_BORDER_COLOUR,self.rect,1)
        top = self.rect.top + SMALL_MARGIN
        #detirmine the range you're showing here then only look at options in that range? e.g for option in enumerate between index 5 and 8
        for index, character in enumerate(characters):
            top = self.display_character(surface, top, character, index==select_index)
         