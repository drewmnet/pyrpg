#

import pygame

import os

#import utilities

tupadd = lambda t1, t2: tuple(map(sum, zip(t1,t2)))

def load_sprite(filename, scale):
    filepath = os.path.join('data', 'sprites', filename)
    #print(filepath)
    ri = pygame.image.load(filepath) # raw image
    ri = pygame.transform.scale(ri, (ri.get_width() * scale, ri.get_height() * scale))
    #raw_image.set_colorkey((128,0,0), pygame.RLEACCEL)
    w = 16 * scale
    h = 16 * scale
    
    # strip format; single frame for each direction
    #  remove this and replace with animated sprite [05/08/22]
    sprite = { "south": None, "north": None, "west": None, "east": None }
    sprite["south"] = ri.subsurface((0,0,w,h))
    sprite["north"] = ri.subsurface((0,h*1,w,h))
    sprite["west"] = ri.subsurface((0,h*2,w,h))
    sprite["east"] = ri.subsurface((0,h*3,w,h))
    
    return sprite

class Mob(pygame.Rect):

    directions = { "south": (0,1), "north": (0,-1), "east": (1,0), "west": (-1,0) }

    def __init__(self, filename, uid, game): # filename is for the sprite
        pygame.Rect.__init__(self, (0,0,16*game.scale,16*game.scale))
        self.uid = uid
        self.game = game
        
        self.facing = "south"
        self.direction = (0,0)
        self.steps = 0
        self.moving = False
        self.scene = None

        if filename not in self.game.sprite_db:
            self.game.sprite_db[filename] = load_sprite(filename, game.scale)
            if self.game.verbose:
                print(f"spritesheet '{filename}' not found; loading")
        #pygame.Rect.__init__(self, self.game.sprite_db[self.sprite].rect)
        self.spr_fn = filename
        self.game.mob_db[self.uid] = self
        
    def place(self, col, row):
        self.x = col * self.game.tilesize
        self.y = row * self.game.tilesize

    def spawn(self, filename): # filename = Scene.uid and dict key    
        self.scene = self.game.scene_db[filename] # TODO deprecate [05/15/22]
        # these lines below are the key to this method
        col, row = self.scene.defaults[self.uid]
        self.place(col, row)
        self.facing = "south"

    def tile_location(self):
        return (self.x // self.game.tilesize, self.y // self.game.tilesize)
        # self.scene.tilesize?

    def move(self, direction):
        if not self.moving: # separate from line 78 so facing direction could change independently and
            self.facing = direction # ... prevents the facing direction change while moving
        
        cell = tupadd(self.directions[direction], self.tile_location()) # map grid cell (col,row)
        no_mob = True # what the hell is this? (March 17, 2022)
        for uid in self.scene.mobs: # should 'mob' be 'uid'?
            m = self.game.mob_db[uid]
            if m != self and cell == m.tile_location():
                no_mob = False
        
        tile = self.game.camera.scene.get_tile("collide", cell)        
        nocollide = tile == '0' and no_mob
        movable = not self.moving #and not self.game.fader.fading
        
        if nocollide and movable:
            self.direction = self.directions[direction]
            self.moving = True
    
    def update(self):
        if self.moving:
            self.x += self.direction[0] * 2
            self.y += self.direction[1] * 2
            self.steps += 2 # all the 2s here are connected
            if self.steps >= self.game.tilesize:
                self.moving = False
                self.steps = 0
                self.direction = (0,0)

    def render(self, surface, x_off=0, y_off=0):
        x = self.x + x_off
        y = self.y + y_off
        surface.blit(self.game.sprite_db[self.spr_fn][self.facing], (x,y))

