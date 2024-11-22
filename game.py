import pygame, sys
from code.allies.ally import Ally
from code.allies.zethe import Zethe
from code.mechanics.inventory import Inventory
from code.support import *
from code.overworld import Overworld
from code.level import Level
#from code.menu import Menu

class Game:
    def __init__(self):
          
        # general setup
        pygame.init()
        self.settings = load_user_settings()
        self.screen = pygame.display.set_mode((self.settings["WIDTH"],self.settings["HEIGHT"]))
        self.display = pygame.Surface((int(self.settings["WIDTH"]/2),int(self.settings["HEIGHT"]/2)))
        pygame.display.set_caption('Zethe Game Game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.large_font = pygame.font.Font(UI_FONT, LARGE_FONT_SIZE)
        self.small_font = pygame.font.Font(UI_FONT, SMALL_FONT_SIZE)
        
        #load up game
        self.load_save("saves/T35T S4V3")
        
    def load_save(self, save_folder):
        print("loading save")
        self.save_folder = save_folder
        save_path = self.save_folder+"/save_file.json"
        save_file = open(save_path, 'r')
        self.save_data = json.load(save_file)
        save_file.close()
        self.load_level(self.save_data["current_level"])
        
        #TODO load party from save file
        self.party = []
        # this dict should be loaded from the save file
        members = {
            "Zethe":"path/to/zethe",
            "TestAlly":"path/to/testally"
        } 
        if "Zethe" in members:
            self.party.append(Zethe(self,members["Zethe"]))
        if "TestAlly" in members:
            self.party.append(Ally(self,members["TestAlly"]))
        #TODO load gear and money
        #This should be a complete dict of every item in the game 
        #load this from the save file
        self.inventory = Inventory(self.save_data["consumables"], self.save_data["equipment"])
        #TODO load events
    
    def load_level(self, current_level, start_pos=None):
        self.level = Level(current_level)
        if start_pos != None:
            self.level.start_pos=start_pos
        self.current_screen = Overworld(self,self.level)
        
    def overwrite_save(self):
        #TODO
        pass
    
    def run(self):
        while True:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display.fill('black')
            self.current_screen.run()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))#purpose of this is to make scaling small pixel art a lot easier
            pygame.display.update()
            self.clock.tick(self.settings["FPS"])

if __name__ == '__main__':
    game = Game()
    game.run()