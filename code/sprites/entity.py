import pygame

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
        print(self.pos)
        
        
    
    def move(self):
        #print(self.direction)
        #print(self.destination)
        #print(self.pos)
        if self.destination != self.pos:
            #self.rect=self.rect.move(self.direction.x*self.speed,self.direction.y*self.speed)
            #TODO currently speed needs to be a factor of TILESIZE fix
            
            self.pos[0]+=self.direction.x*self.speed
            self.pos[1]+=self.direction.y*self.speed
        else:
            if self.direction.y == 1: #up
                self.destination[1] += self.game.settings["TILESIZE"]
            elif self.direction.y == -1: #down
                self.destination[1] -= self.game.settings["TILESIZE"]
            elif self.direction.x == 1: #right
                self.destination[0] += self.game.settings["TILESIZE"]
            elif self.direction.x == -1: #left
                self.destination[0] -= self.game.settings["TILESIZE"]
        
    def animate(self):
        self.rect = self.image.get_rect(topleft=self.pos)
    
    def update(self):
        self.move()
        self.animate()