print("importing ui module")
print("importing UI class [EMPTY]")

import pygame

from . import theme
#from . import selector

class UI:
    def __init__(self, game):
        self.game = game
        
        # theme
        self.theme = theme.Theme()
        
        self.children = {}
        
    def __getitem__(self, key):
        return self.children[key]
    
    def __setitem__(self, key, value):
        self.children[key] = value
        
#from .dialogue import Dialogue
from .selector import Selector
