#

import pygame

import os

#import utilities

tupadd = lambda t1, t2: tuple(map(sum, zip(t1,t2)))

def load_sprite(filename, scale):
    filepath = os.path.join('data', 'sprites', filename)
    
    raw_image = pygame.image.load(filepath)
    ri_width = raw_image.get_width() * scale
    ri_height = raw_image.get_height() * scale
    raw_image = pygame.transform.scale(raw_image, (ri_width, ri_height))
    
    w = 16 * scale
    h = 16 * scale
    sprite = { "south": None, "north": None, "west": None, "east": None }
    sprite["south"] = raw_image.subsurface((0, 0, w, h))
    sprite["north"] = raw_image.subsurface((0, h*1, w, h))
    sprite["west"] = raw_image.subsurface((0, h*2, w, h))
    sprite["east"] = raw_image.subsurface((0, h*3, w, h))
    
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
        self.is_moving = False
        self.scene = None

        if filename not in self.game.sprite_db:
            self.game.sprite_db[filename] = load_sprite(filename, game.scale)
            if self.game.is_verbose:
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
        if not self.is_moving: # separate from line 78 so facing direction could change independently and
            self.facing = direction # ... prevents the facing direction change while is_moving
        
        cell = tupadd(self.directions[direction], self.tile_location()) # map grid cell (col,row)
        no_mob = True # what the hell is this? (March 17, 2022)
        for uid in self.scene.mobs: # should 'mob' be 'uid'?
            m = self.game.mob_db[uid]
            if m != self and cell == m.tile_location():
                no_mob = False
        
        tile = self.game.camera.scene.get_tile("collide", cell)        
        nocollide = tile == '0' and no_mob
        movable = not self.is_moving #and not self.game.fader.fading
        
        if nocollide and movable:
            self.direction = self.directions[direction]
            self.is_moving = True
    
    def update(self):
        if self.is_moving:
            self.x += self.direction[0] * 2
            self.y += self.direction[1] * 2
            self.steps += 2 # all the 2s here are connected
            if self.steps >= self.game.tilesize:
                self.is_moving = False
                self.steps = 0
                self.direction = (0,0)

    def render(self, surface, x_off, y_off):
        x = self.x - x_off
        y = self.y - y_off
        surface.blit(self.game.sprite_db[self.spr_fn][self.facing], (x, y))

