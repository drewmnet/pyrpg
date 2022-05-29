import pygame

from . import camera

class Game:
    is_exiting = False
    is_verbose = True
        
    def __init__(self, displaysize, tilesize, scale):
        # pygame genesis
        pygame.init()
        pygame.display.set_caption("pyrpg (drewmnet 2022)")
        
        # constructor argument assignment
        self.display = pygame.display.set_mode(displaysize)
        self.tilesize = tilesize * scale
        self.scale = scale
        if self.is_verbose:
            print(f"tilesize: {tilesize}")
            print(f"scale: {scale}")
        
        # internal components
        self.clock = pygame.time.Clock()
        self.tick = 0
        
        # data dicts
        self.scene_db = {}
        self.sprite_db = {}
        self.mob_db = {}
        
        self.player = None
        
        # peripherals
        self.camera = None
        self.ui = None
        self.fader = None
        
        self.active_object = None
        self.is_running = False

    def start(self):
        self.is_running = True
        self.main()
        
    def main(self):
        while self.is_running:
            self.update()
            self.render()
        
    def update(self):
        self.clock.tick(60)
        self.tick = (self.tick + 1) % 0xffffffff
        
        if self.active_object is not None:
            self.active_object.update(self.tick)
        
    def render(self):
        if self.active_object is not None:
            self.active_object.render(self.display)
        
        pygame.display.flip()
        self.display.fill((0,0,0))
