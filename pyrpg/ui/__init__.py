import pygame

from . import theme
from .dialogue import Dialogue
from .selector import Selector

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

