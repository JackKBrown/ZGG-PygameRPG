import pygame, sys
from code.support import *
from code.overworld import Overworld
from code.mechanics.character import Character
from code.level import Level
#from code.menu import Menu

class Game:
    def __init__(self):
          
        # general setup
        self.settings = load_settings()
        pygame.init()
        self.screen = pygame.display.set_mode((self.settings["WIDTH"],self.settings["HEIGHT"]))
        pygame.display.set_caption('Zethe Game Game')
        self.clock = pygame.time.Clock()
        self.display = pygame.Surface((int(self.settings["WIDTH"]/2),int(self.settings["HEIGHT"]/2)))
        self.level = Level("data/maps/petra_genis.json")
        self.current_screen = Overworld(self,self.level)
        self.party = {
            'zethe' : Character("Zethe")
        }
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.current_screen.begin_encounter()

            self.display.fill('black')
            self.current_screen.run()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))#purpose of this is to make scaling small pixel art a lot easier
            pygame.display.update()
            self.clock.tick(self.settings["FPS"])

if __name__ == '__main__':
    game = Game()
    game.run()