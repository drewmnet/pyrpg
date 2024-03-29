import os

import pygame

from . import utilities

class Tileset:
    def __init__(self, width, height, scale=1):
        self.width = width
        self.height = height
        self.scale = scale
                    
        self.textures = {}
        
    def update(self, filename, scale=1, firstgid=1):
        textures = utilities.load_tileset(os.path.join("data", "scene", filename),
                                          self.width,
                                          self.height,
                                          scale,
                                          firstgid)
        self.textures.update(textures)
        
        self.textures['0'] = pygame.Surface((self.width, self.height)).convert()
        self.textures['0'].fill((0,0,0))

    def __getitem__(self, key=None):
        if key is not None:
            return self.textures[key]
        else:
            return self.textures
