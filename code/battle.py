import pygame

class Battle():
    def __init__(self, game, overworld, enemies):
        self.game = game
        self.overworld = overworld 
        # pass the overworld into the battle so it can give it back to the game loop when the encounter is over
        
    def input(self):
        for event in self.game.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
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
           
    def run(self):
        #self.cooldowns()
        self.input()
        floor_surface = pygame.image.load('graphics/test/battlefield.png').convert()
        floor_rect = floor_surface.get_rect(topleft=(0,0))
        self.game.display.blit(floor_surface, (0,0))
        #display background
        #display enemies
        #display players
        #update entities
        