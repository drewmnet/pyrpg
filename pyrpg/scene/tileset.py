import os

from . import utilities

class Tileset:
    def __init__(self, width, height, scale=1):
        self.width = width
        self.height = height
        self.scale = scale
                    
        self.textures = {}
        
    def update(self, filename, scale=1, colourkey=None, firstgid=1):
        textures = utilities.load_tileset(os.path.join("data", "scene", filename),
                                          self.width,
                                          self.height,
                                          scale,
                                          colourkey,
                                          firstgid)
        print(textures)
        self.textures.update(textures)
                
    def __getitem__(self, key=-1):
        if key == -1:
            return self.textures
        if key != -1:
            return self.textures[key]
