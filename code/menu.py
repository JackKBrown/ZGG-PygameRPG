import pygame

class Menu():
    def __init__(self, game, overworld):
        self.game = game
        self.overworld = overworld 
        self.display_surface = self.game.display
        self.font = pygame.font.Font(self.game.settings["UI_FONT"], self.game.settings["UI_FONT_SIZE"])
        
        #options
        self.option_stack = []
        self.actions = {
            "attack": self.attack, 
            "magic":{
                "fire":self.fire
                }, 
            "utopic":{
                "VRO":self.vro
                }, 
            "item":self.item
        }
        self.action_stack.append(self.actions)
        
        self.options=["items", "equip", "party", "settings"]
        self.option_width = self.game.display.get_size()[0] / (len(self.options)+1)
        self.option_height = self.game.display.get_size()[1] * 0.1
        self.option_margin = self.option_width / (len(self.options)+1)
        
        self.create_options()
        #selection system
        self.select_index = 0
        self.select_time = None
        self.can_move = True
        
    def create_options(self):
        self.option_list = []
        for index in range(len(self.options)):
            left = self.option_margin + ((self.option_width+self.option_margin)*index)
            top = self.option_margin
            item = Option(self.game,left, top, self.option_width, self.option_height, index, self.font)
            self.option_list.append(item)
    
    def input(self):
        for event in self.game.events:
            if event.key == pygame.K_s:
                if self.select_index < len(self.option_stack[-1])-1:
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
            
            if self.select_index >= len(self.options):
                self.select_index=0

    def exit_menu(self):
        self.game.current_screen = self.overworld
    
    def display(self):
        self.input()
        for index, item in enumerate(self.option_list):
            # get attributes
            item.display(self.display_surface,self.select_index, 1,2,3,4)
        self.cooldowns()
                
    def run(self):
        self.input()
        self.display()

class Option():
    def __init__(self,game, l, t, w, h, index, font):
        self.game = game
        self.rect = pygame.Rect(l,t,w,h)
        self.index = index 
        self.font = font
    
    def display_names(self, surface, name, cost, selected):
        #title
        title_surf = self.font.render(str(name), False, self.game.settings['TEXT_COLOUR'])
        title_rect = title_surf.get_rect(midtop = self.rect.midtop +pygame.math.Vector2(0,20))
        #costs
        cost_surf = self.font.render(f"{int(cost)}", False, self.game.settings['TEXT_COLOUR'])
        cost_rect = title_surf.get_rect(midbottom = self.rect.midbottom -pygame.math.Vector2(0,20))
        #draw
        surface.blit(title_surf,title_rect)
        surface.blit(cost_surf,cost_rect)
        
    def display(self, surface, selection_num,name, value, max_value, cost):
        pygame.draw.rect(surface,self.game.settings['UI_BG_COLOUR'],self.rect)
        self.display_names(surface, name,cost,False)
        