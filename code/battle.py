import pygame
from code.enemy import Enemy
from code.ally import Ally

class Battle():
    def __init__(self, game, overworld, enemies):
        self.game = game
        self.overworld = overworld 
        self.enemies=[]
        self.allies=[
            Ally("blargle")
        ]
        # pass the overworld into the battle so it can give it back to the game loop when the encounter is over
        for monster in enemies:
            self.enemies.append(Enemy(f"data//enemies//{str(monster)}.json"))
        self.enemy_postition= [
            (0.6,0.6),
            (0.7,0.7),
            (0.7,0.5),
            (0.6,0.8),
            (0.6,0.4)
        ]
        self.ally_position = [
            (0.3,0.6),
            (0.2,0.7),
            (0.2,0.5)
        ]
     
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
           
    def run(self):
        #self.cooldowns()
        self.input()
        self.display()
        #display background
        #display enemies
        #display players
        #update entities
        