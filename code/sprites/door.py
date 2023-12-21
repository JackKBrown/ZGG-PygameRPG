import pygame

class Door(pygame.sprite.Sprite):
    def __init__(self,pos,surf,name,link,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.name = name
        self.link = link 
        # the link ultimately is going to need to load up new maps and tell where the player needs to load 