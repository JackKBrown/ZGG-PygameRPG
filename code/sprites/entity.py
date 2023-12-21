import pygame
from code.sprites.tile import Tile

class Entity(pygame.sprite.Sprite):
    def __init__(self,groups,pos,game):
        super().__init__(groups)
        self.game = game
        self.frame_index = 0
        self.animation_speed=0.2
        self.speed=2
        self.direction=pygame.math.Vector2()
        
        #movement
        self.pos = list(pos)
        self.destination = list(pos)
        self.dest_tile=None
        print(self.pos)
        
        
    
    def move(self):
        #print(self.direction)
        #print(self.destination)
        #print(self.pos)
        if self.dest_tile != None:
            if self.dest_tile.rect.topleft != self.rect.topleft:
                #self.rect=self.rect.move(self.direction.x*self.speed,self.direction.y*self.speed)
                #TODO currently speed needs to be a factor of TILESI
                self.pos[0]+=int(self.direction.x*self.speed)
                self.pos[1]+=int(self.direction.y*self.speed)
                return
            else:
                self.dest_tile.kill()
                self.dest_tile = None
                return
                
        if self.direction.y == 1: #up
            prospective_pos = (self.destination[0],self.destination[1] + self.game.settings["TILESIZE"])
            self.destination = self.check_destination(prospective_pos)
        elif self.direction.y == -1: #down
            prospective_pos = (self.destination[0],self.destination[1] - self.game.settings["TILESIZE"])
            self.destination = self.check_destination(prospective_pos)
        elif self.direction.x == 1: #right
            prospective_pos = (self.destination[0]+ self.game.settings["TILESIZE"],self.destination[1])
            self.destination = self.check_destination(prospective_pos)
        elif self.direction.x == -1: #left
            prospective_pos = (self.destination[0]- self.game.settings["TILESIZE"],self.destination[1])
            self.destination = self.check_destination(prospective_pos)
    
    def check_destination(self, pos):
        #check if the dest is free
        future_rect = self.image.get_rect().copy()
        future_rect.topleft=pos
        if(self.game.current_screen.collide_obstacle(future_rect)):
            return self.pos
        elif(self.game.current_screen.collide_event(future_rect)):
            self.game.current_screen.load_overworld(future_rect)
            return pos #no collision tile this shouldn't cause issues?
        collision_tile = Tile(pos,pygame.Surface((self.image.get_rect().width, self.image.get_rect().height)),[self.game.current_screen.obstacle_sprites])
        self.dest_tile = collision_tile
        return pos
            
    def animate(self):
        self.rect = self.image.get_rect(topleft=self.pos)
    
    def update(self):
        self.move()
        self.animate()