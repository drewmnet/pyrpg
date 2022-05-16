import operator

import pygame

class Camera(pygame.Rect):
    def __init__(self, game, location):
        self.game = game
        pygame.Rect.__init__(self, location+game.display.get_size())
        self.tilesize = game.tilesize
        
        self.cols = 0
        self.rows = 0
        self.blank = None
        self.following = None       

        self.scene_rect = pygame.Rect((0,0,0,0))
    
    def setup(self, filename): # get filename from game.scene_db
        if filename not in self.game.scene_db:
            #self.load_scene(filename)
            print(f"'{filename}' not found")
            pygame.quit()
            exit()
        self.scene = self.game.scene_db[filename]
    
        self.following = self.game.player
        self.cols = self.w // self.tilesize + 2 # for the display
        self.rows = self.h // self.tilesize + 2 # not to be confused with the cols/rows of Map2D
        self.blank = pygame.Surface((self.tilesize,self.tilesize)).convert()
        self.blank.fill((0,0,0))
        self.scene_rect.w = (self.scene.cols) * self.tilesize
        self.scene_rect.h = (self.scene.rows) * self.tilesize
        # reset mobs in scene to default positions and facings
        for mob_fn in self.scene.mobs:
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
    
        index = self.scene.get_tile(layer, (c_index,r_index))

        x = col * self.tilesize - x_offset
        y = row * self.tilesize - y_offset

        if index != "0":
            tile = self.scene.tileset[index]
            return (tile, x, y)
        else:			
            return ("0", x, y)
    
    def y_sort(self): # TODO move this back to utilities [05/14/22]
        return sorted(self.scene.get_mobs(), key=operator.attrgetter('y'))
            
    def update(self, tick): # this needn't be called every cycle
        #x,y = self.following.center
        self.scene.update(tick)
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

    def render(self, surface):    
        for row in range(self.rows): # draw the bottom and middle tile layers
            for col in range(self.cols):
                bottom_t, x, y = self.tile_prep("bottom", col, row)
                middle_t, x, y = self.tile_prep("middle", col, row)
                # yes, the above line overrides the x and y values
                #  in the line above it
                
                if bottom_t != "0":
                    surface.blit(bottom_t, (x,y))
                elif bottom_t == "0":
                    surface.blit(self.blank, (x,y))

                if middle_t != "0":
                    surface.blit(middle_t, (x,y))

        if self.scene.mobs: # draw the sprites
            #for sprite in game.scene.sprites.values():
            for sprite in self.y_sort():
                sprite.render(surface, x_off = -self.x, y_off = -self.y)
        
        for row in range(self.rows): # draw the top layer
            for col in range(self.cols):
                tile, x, y = self.tile_prep("top", col, row)
                if tile != "0": surface.blit(tile, (x, y))
