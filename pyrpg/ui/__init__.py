print("importing ui module")
print("importing UI class [EMPTY]")

import pygame

class UI:
    def __init__(self, game):
        self.game = game
        
        # theme
        self.bgcolour
        self.alpha
        self.font
        
        
        self.children = { "DLG": None,
                          "YN": None,
                          "MNU": None,
                          "HUD": None
                        }
        
    def __getitem__(self, key=-1):
        if key == -1:
            return self.textures
        else:
            return self.textures[key]

from .dialogue import Dialogue
