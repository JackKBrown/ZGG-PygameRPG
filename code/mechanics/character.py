import pygame 

class Character():
    def __init__(self, name):
        #TODO load in character from a save file
        self.stats={"hp":100, "st":50}
        self.name=name