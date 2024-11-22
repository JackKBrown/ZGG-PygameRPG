import pygame
from code.support import *
from code.sprites.tile import Tile

class Entity(pygame.sprite.Sprite):
    def __init__(self,groups,pos,game):
        super().__init__(groups)
        self.game = game
        self.frame_index = 0
        self.speed=2
        self.direction=pygame.math.Vector2()
        
        #movement
        self.pos = list(pos)
        self.destination = list(pos)
        self.dest_tile=None
        print(self.pos)
        self.animation_speed=DEF_ANIM_SPEED
        self.status = "idle"
        self.frame_index=0
        self.blink=False
        self.import_assets()
    
    def import_assets(self):
        character_path = 'graphics/player/'
        self.animations = {'idle': []}
        
        for animation in self.animations.keys():
            full_path=character_path+animation
            self.animations[animation] = import_folder(full_path)
            
        print(self.animations)    
    
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
            #This is a collide event
            self.game.current_screen.event_collide(future_rect)
            return pos #no collision tile this shouldn't cause issues?
        collision_tile = Tile(pos,pygame.Surface((self.image.get_rect().width, self.image.get_rect().height)),[self.game.current_screen.obstacle_sprites])
        self.dest_tile = collision_tile
        return pos
            
    def animate(self):
        animation = self.animations[self.status]
        #loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index =0
        
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(topleft=self.pos)
        
        if self.blink:
            alpha=wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    
    def update(self):
        self.move()
        self.animate()