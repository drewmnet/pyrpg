from .game import Game
from .titlescreen import TitleScreen
from .gameplay import Gameplay
from .camera import Camera
from .fader import Fader

class Scene:
    def __init__(self, map2d, script):
        self.map2d = map2d
        self.script = script
        
    def update(self, tick):
        self.script(self, tick)
