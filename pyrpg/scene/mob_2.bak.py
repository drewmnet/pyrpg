#

import pygame

import utilities

#class Sprite:
#    def __init__(self, game):
#        pygame.Rect.__init__(self, rect)
#        self.game = game
#        self.image = None

class Mob(pygame.Rect):

    directions = { "south": (0,1), "north": (0,-1), "east": (1,0), "west": (-1,0) }

    def __init__(self, filename, uid, game): # filename is for the sprite
        pygame.Rect.__init__(self, (0,0,16,16))
        self.uid = uid
        self.game = game
        self.facing = "south"
        self.direction = (0,0)
        self.steps = 0
        self.moving = False
        self.scene = None

        if filename not in self.game.sprite_db:
            self.game.sprite_db[filename] = utilities.load_sprite(filename, game)
            if self.game.verbose:
                print("spritesheet '{}' not found; loading".format(filename))
        #pygame.Rect.__init__(self, self.game.sprite_db[self.sprite].rect)
        self.spr_fn = filename
        self.game.mob_db[self.uid] = self
        
    def place(self, col, row):
        self.x = col * 16
        self.y = row * 16

    def spawn(self, filename): # filename = Scene.uid and dict key    
        self.scene = self.game.scene_db[filename]
        col, row = self.scene.defaults[self.uid]
        self.place(col, row)
        self.facing = "south"

    def tile_location(self):
        return (int(self.x/16), int(self.y/16))

    def move(self, direction):
        self.facing = direction
        
        cell = utilities.tupadd(self.directions[direction], self.tile_location()) # map grid cell (col,row)
        no_mob = True
        for uid in self.scene.mobs: # should 'mob' be 'uid'?
            m = self.game.mob_db[uid]
            if m != self and cell == m.tile_location():
                no_mob = False
        
        tile = self.game.scene.get_tile("collide", cell)        
        nocollide = tile == '0' and no_mob
        movable = not self.moving and not self.game.fader.fading
        
        if nocollide and movable:
            self.direction = self.directions[direction]
            self.moving = True
    
    def update(self):
        if self.moving:
            self.x += self.direction[0] * 2
            self.y += self.direction[1] * 2
            self.steps += 2 # all the 2s here are connected
            if self.steps >= 16:
                self.moving = False
                self.steps = 0
                self.direction = (0,0)

    def render(self, surface, x_off=0, y_off=0):
        x = self.x + x_off
        y = self.y + y_off
        surface.blit(self.game.sprite_db[self.spr_fn][self.facing], (x,y))

