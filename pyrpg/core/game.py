print("importing Game class")

import pygame

from . import camera

class Game:
    # colour palette
    palette = { light: (0xfa, 0xfb, 0xf6),
                shade: (0xc6, 0xb7, 0xbe),
                grey: (0x56, 0x5a, 0x75),
                dark: (0x0f, 0x0f, 0x1b)
              }
              
    # system flags
    EXIT = False
    
    # flags
    verbose = True
        
    def __init__(self, displaysize=(640,480), tilesize=16, scale=1):
        # pygame genesis
        pygame.init()
        pygame.display.set_caption("pyrpg (drewmnet 2022)")
        
        # constructor argument assignment
        self.display = pygame.display.set_mode(displaysize)
        self.tilesize = tilesize * scale
        self.scale = scale
        if self.verbose:
            print("tilesize: {}".format(self.tilesize))
            print("scale: {}".format(self.scale))
        
        # internal components
        self.clock = pygame.time.Clock()
        self.tick = 0
        
        self.running = False
        self.ending = False # when True and self.fader.faded_out: end program
                
        # data dicts
        self.scene_db = {}
        self.sprite_db = {}
        self.mob_db = {}
        
        self.player = None
        
        # components
        self.camera = camera.Camera(displaysize, self.tilesize, self)
        #self.ui = 
        #self.fader =         

    # TODO deprecate
    def load_scene(self, filename): # filename needs to be an actual scene instance
        if filename not in self.scene_db:
            self.scene_db[filename] = scene.Scene(filename, self)
            if self.verbose:
                print("loading '{}'".format(filename))
    
    def setup_scene(self, filename):
        if filename not in self.scene_db:
            #self.load_scene(filename)
            print("{} not found".format(filename))
            pygame.quit()
            exit()
        self.scene = self.scene_db[filename]
        self.camera.setup(filename)
        
    def start(self):
        self.running = True
        self.main()
        
    def main(self):
        while self.running:
            self.update()
            self.render()
        
    def update(self):
        self.clock.tick(60)
        self.tick = (self.tick + 1) % 4294967295
        
        # reset the flags
        #self.EXIT = False
