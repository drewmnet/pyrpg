import os
import pygame
from . import filepaths
#from . import utilities

def load_sprite(filename, scale):
    filepath = os.path.join(filepaths.image_path, filename)
    raw_image = pygame.image.load(filepath)
    #raw_image.set_colorkey((128,0,0), pygame.RLEACCEL)
    w = 16 * scale
    h = 16 * scale
    sprite = { "south": None, "north": None, "west": None, "east": None }
    sprite["south"] = raw_image.subsurface((0,0,w,h))
    sprite["north"] = raw_image.subsurface((0,h*1,w,h))
    sprite["west"] = raw_image.subsurface((0,h*2,w,h))
    sprite["east"] = raw_image.subsurface((0,h*3,w,h))
    
    return sprite

class Sprite:
    def __init__(self, filename, game):
        self.filename = filename
        self.game = game
        self.game.sprite_db[self.filename] = self        
        data = load_sprite(os.path.join(filepaths.image_path, filename))        
        ###
        # Mob inherits from pygame.Rect;
        # pygame.Rect is instantiated using self.rect
        self.rect = pygame.Rect(data["rect"])
        self.cols = data["cols"]
        self.rows = data["rows"]
        self.cells = data["cells"]
        self.x_off, self.y_off = data["offsets"]
        ###
        self.pattern = [0,1,0,2]
        self.facings = { "south": 0, "north": 1, "east": 2, "west": 3 }
        
    def get_cell(self, col, row):
        if (col >= 0 and col < self.cols) and (row >= 0 and row < self.rows):
            return self.cells[self.cols*row+col]
        else:
            if self.verbose: print("col or row out of sprite's bounds")
            pygame.quit()
            exit()
