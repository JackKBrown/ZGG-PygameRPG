import pygame
from code.support import *
from code.enemy import Enemy
from code.allies.ally import Ally
from code.allies.zethe import Zethe

state_list = [
    "Initiative"
    "EnemyAction", 
    "PlayerAction",
    "PlayerSelect",
    "ChooseTarget"
]

class Battle():
    def __init__(self, game, overworld, enemies):
        self.game = game
        self.overworld = overworld 
        self.enemies=[]
        self.allies=[
            Zethe("blargle"),
            Ally("blargle")
        ]
        self.activate_character=self.allies[0]
        # pass the overworld into the battle so it can give it back to the game loop when the encounter is over
        for monster in enemies:
            self.enemies.append(Enemy(f"data//enemies//{str(monster)}.json"))
        
        self.initiative = self.allies + self.enemies
        self.initiative.sort(key=lambda x: x.stats["speed"], reverse=True)
        self.initiative_index = 0
        self.state= "Initiative"
        
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
        self.battle_menu = BattleMenu(
            self.game,
            (3 * (self.info_width+ self.info_margin)) + self.info_margin,
            self.info_top,
            self.info_width,
            self.info_height
            )
        #detirmine initiative order
        #action timer
        #input
        self.select_index = 0
        #choose target
        self.target_list = self.enemies
        self.target_index = 0
        self.can_swap_target_list = True
        self.target=None
        #UI
        self.topbar_text="hi"
     
    def set_target_state(self, target_list, can_swap = True):
        self.state="ChooseTarget"
        self.target_list = self.enemies
        self.can_swap_target_list = True
        self.target_index=0 
        self.topbar_text=self.target_list[self.target_index].name
     
    def input(self):
        for event in self.game.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_battle()
                if self.state == "PlayerSelect":
                    if event.key == pygame.K_s:
                        if self.select_index < len(self.activate_character.action_stack[-1])-1:
                            self.select_index += 1
                    if event.key == pygame.K_w:
                        if self.select_index > 0:
                            self.select_index -= 1
                    if event.key == pygame.K_RIGHT:
                        self.activate_character.select_action(list(self.activate_character.action_stack[-1])[self.select_index], self)
                    if event.key == pygame.K_LEFT:
                        self.activate_character.select_action("back", self)
                elif self.state == "ChooseTarget":
                    if event.key == pygame.K_s:
                        self.target_index += 1
                        if self.target_index == len(self.target_list): 
                            self.target_index = 0
                        self.topbar_text=self.target_list[self.target_index].name 
                    if event.key == pygame.K_w:
                        self.target_index -= 1
                        if self.target_index == -1: 
                            self.target_index = 0
                        self.topbar_text=self.target_list[self.target_index].name 
                    if event.key == pygame.K_a:
                        if self.can_swap_target_list:
                            self.target_index=0
                            self.target_list=self.allies
                        self.topbar_text=self.target_list[self.target_index].name 
                    if event.key == pygame.K_d:
                        if self.can_swap_target_list:
                            self.target_index=0
                            self.target_list=self.enemies
                        self.topbar_text=self.target_list[self.target_index].name 
                    if event.key == pygame.K_RIGHT:
                        #selects the target
                        pass
                    if event.key == pygame.K_LEFT:
                        #TODO need to change the state back to PlayerSelect and whatever was previously on the action stack
                        pass
    
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
            enemy.animate() 
            x = self.game.display.get_size()[0] * self.enemy_postition[index][0]
            y = self.game.display.get_size()[1] * self.enemy_postition[index][1]
            self.game.display.blit(enemy.image, (x,y))
        for index,ally in enumerate(self.allies):
            ally.animate()
            x = self.game.display.get_size()[0] * self.ally_position[index][0]
            y = self.game.display.get_size()[1] * self.ally_position[index][1]
            self.game.display.blit(ally.image, (x,y))
        for index, item in enumerate(self.character_info_list):
            # get attributes
            item.display(self.game.display)
        if self.activate_character != None:
            self.battle_menu.display(self.game.display, self.activate_character, self.select_index)
        self.display_topbar(self.game.display)
    
    def display_topbar(self, surface):
        if self.topbar_text != None:
            tb_surf = self.game.small_font.render(self.topbar_text, False, TEXT_COLOUR)
            tb_rect = tb_surf.get_rect(midtop = surface.get_rect().midtop + pygame.Vector2(0,10))
            tb_bg_rect = tb_rect.inflate(2,2)
            pygame.draw.rect(surface, UI_BG_COLOUR, tb_bg_rect)
            pygame.draw.rect(surface,UI_BORDER_COLOUR,tb_bg_rect,2)
            surface.blit(tb_surf, tb_rect)
            
            
    def run(self):
        #self.cooldowns()
        self.input()
        self.display()
        if self.state == "Initiative":
            # see who is next in initiative
            # if next is an enemy run the take turn function
            # elif next is pc set them as the active player and update the state
            self.state = "PlayerSelect"
            pass
        elif self.state == "EnemyAction":
            # Do action animation then callback the action to complete the effects
            pass
        elif self.state == "PlayerSelect":
            #wait for player to select action
            #can probably delete this elif as all the state stuff happens in the input
            pass
        elif self.state == "PlayerAction":
            #
            pass
        elif self.state == "ChooseTarget":
            #do the targetting things
            pass
        else:
            print("error state not in list")
        #display background
        #display enemies
        #display players
        
class BattleMenu():
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
        
    def display(self, surface, character, select_index):
        pygame.draw.rect(surface, UI_BG_COLOUR, self.rect)
        pygame.draw.rect(surface,UI_BORDER_COLOUR,self.rect,1)
        top = self.rect.top + SMALL_MARGIN
        #detirmine the range you're showing here then only look at options in that range? e.g for option in enumerate between index 5 and 8
        for index, option in enumerate(character.action_stack[-1]):
            if index <= self.top_of_list+4:
                top = self.display_option(surface, top, option, index==select_index)
            
        
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
        
        