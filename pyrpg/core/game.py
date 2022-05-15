import pygame

from . import camera

class Game:
    # colour palette; if a base ui class (UI_Base) emerges, the palette will be moved there [5/7/22]
    palette = { "light": (0xfa, 0xfb, 0xf6),
                "shade": (0xc6, 0xb7, 0xbe),
                "grey": (0x56, 0x5a, 0x75),
                "dark": (0x0f, 0x0f, 0x1b)
              }
              
    # system flags
    exiting = False # not sure what I'm going to do with this [5/7/22]
    
    # flags
    verbose = True
        
    def __init__(self, displaysize, tilesize, scale):
        # pygame genesis
        pygame.init()
        pygame.display.set_caption("pyrpg (drewmnet 2022)")
        
        # constructor argument assignment
        self.display = pygame.display.set_mode(displaysize)
        self.tilesize = tilesize * scale
        self.scale = scale
        if self.verbose:
            print(f"tilesize: {tilesize}")
            print(f"scale: {scale}")
        
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
        
        # peripherals
        self.camera = camera.Camera(displaysize, tilesize * scale, (0,0), self)
        #self.ui = 
        #self.fader =         

    def start(self):
        self.running = True
        self.main()
        
    def main(self):
        while self.running:
            self.update()
            self.render()
            
            self.running = not self.exiting
        
    def update(self):
        self.clock.tick(60)
        self.tick = (self.tick + 1) % 0xffffffff
        
        self.player.get_events()
        
        self.player.update()
        self.camera.update()
        # reset the flags
        #self.EXIT = False
        
    def render(self):
        self.camera.render(self)
        
        pygame.display.flip()
