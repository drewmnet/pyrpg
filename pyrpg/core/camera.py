import operator

import pygame

class Camera(pygame.Rect):
    def __init__(self, displaysize, tilesize, game, x=0, y=0):
        pygame.Rect.__init__(self, (x,y)+displaysize)
        self.tilesize = tilesize
        self.game = game
        
        self.cols = 0
        self.rows = 0
        self.blank = None
        self.following = None       

        self.scene_rect = pygame.Rect((0,0,0,0))
    
    def setup(self, filename): # scene setup
        self.following = self.game.player
        self.cols = self.w // self.tilesize + 2
        self.rows = self.h // self.tilesize + 2
        self.blank = pygame.Surface((self.tilesize,self.tilesize)).convert()
        self.blank.fill((0,0,0))
        self.scene_rect.w = (self.game.scene.cols) * self.tilesize
        self.scene_rect.h = (self.game.scene.rows) * self.tilesize
        # reset mobs in scene to default positions and facings
        for mob_fn in self.game.scene.mobs:
            self.game.mob_db[mob_fn].spawn(filename)
        
        self.game.player.moving = False
        #self.game.scene.script.init()
        #self.update() # centre camera on camera.following before fade_in begins
        # test this when fader is re-implemented [05/07/22]
        self.center = self.following.center #???

    def tile_prep(self, layer, col, row):
        x_offset = self.x % self.tilesize
        y_offset = self.y % self.tilesize

        c_index = self.x // self.tilesize + col
        r_index = self.y // self.tilesize + row
    
        index = self.game.scene.get_tile(layer, (c_index,r_index))

        x = col * self.tilesize - x_offset
        y = row * self.tilesize - y_offset

        if index != "0":
            tile = self.game.scene.tileset[index]
            return (tile, x, y)
        else:			
            return ("0", x, y)
    
    def y_sort(self):
        return sorted(self.game.scene.get_mobs(), key=operator.attrgetter('y'))
            
    def update(self): # this needn't be called every cycle
        #x,y = self.following.center
        if self.following: # clamp stuff        
            if self.center[0] < self.following.center[0]:
                self.move_ip((2,0))
            elif self.center[0] > self.following.center[0]:
                self.move_ip((-2,0))
            if self.center[1] < self.following.center[1]:
                self.move_ip((0,2))
            elif self.center[1] > self.following.center[1]:
                self.move_ip((0,-2))
            self.clamp_ip(self.scene_rect) # the good news: it's not this that's making the cpu jump to 20%

    def render(self):    
        for row in range(self.rows): # draw the bottom and middle tile layers
            for col in range(self.cols):
                bottom_t, x, y = self.tile_prep("bottom", col, row)
                middle_t, x, y = self.tile_prep("middle", col, row)
                # yes, the above line overrides the x and y values
                #  in the line above it
                
                if bottom_t != "0":
                    self.game.display.blit(bottom_t, (x,y))
                elif bottom_t == "0":
                    self.game.display.blit(self.blank, (x,y))

                if middle_t != "0":
                    self.game.display.blit(middle_t, (x,y))

        if self.game.scene.mobs: # draw the sprites
            #for sprite in self.game.scene.sprites.values():
            for sprite in self.y_sort():
                sprite.render(self.game.display, x_off = -self.x, y_off = -self.y)
        
        for row in range(self.rows): # draw the top layer
            for col in range(self.cols):
                tile, x, y = self.tile_prep("top", col, row)
                if tile != "0": self.game.display.blit(tile, (x, y))
