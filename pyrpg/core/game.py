import pygame

from . import camera

class Game:
    exiting = False
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
        self.camera = None
        self.ui = None
        self.fader = None
        
        self.active_object = None

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
        
        if self.active_object is not None:
            self.active_object.update(self.tick)
        #self.player.get_events()
        
        #self.player.update()
        #self.camera.update()
        # reset the flags
        #self.exiting = False
        
    def render(self):
        #self.camera.render(self)
        if self.active_object is not None:
            self.active_object.render(self.display)
        
        pygame.display.flip()
        self.display.fill((0,0,0))
