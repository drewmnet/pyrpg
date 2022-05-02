print("importing Mob class")

import pygame

tupadd = lambda t1, t2: tuple(map(sum, zip(t1,t2)))

class Mob(pygame.Rect):
    pattern = [0,1,0,2]
    facings = { "south": 0, "north": 1, "east": 2, "west": 3 }
    directions = { "south": (0,1), "north": (0,-1), "east": (1,0), "west": (-1,0) }
    
    def __init__(self, sprite_uid, uid, game):
        if uid not in game.mob_db:
            self.sprite = game.sprite_db[sprite_uid]            
            pygame.Rect.__init__(self, pygame.Rect(self.sprite.rect)) # a deviation from the norm but it's shorter
            self.uid = uid # ?
            self.game = game # yes, this is needed
            
            #
            self.scene = None
            #
            self.facing = "south"
            self.frame = 0            
            #
            self.moving = False
            self.direction = (0,0)
            self.speed = 2 # pixel precision
            self.steps = 0
                
            game.mob_db[uid] = self
            
    #def base_update(self, tick):
    #    self.frame += self.moving & (tick % 12 == 0) * 1
    #    self.frame = self.frame % len(self.pattern) * self.moving
        
    #def update(self, tick): # overridden by classes derived
    #    self.base_update(tick)
    
    def place(self, col, row):
        self.x = col * self.game.tilesize
        self.y = row * self.game.tilesize
        
    def spawn(self, filename): # filename = Scene.uid and dict key    
        self.scene = self.game.scene_db[filename]
        col, row = self.scene.defaults[self.uid]
        self.place(col, row)
        self.facing = "south"
            
    def tile_location(self):
        return (int(self.x / self.game.tilesize), int(self.y / self.game.tilesize))

    # for tiles only
    def collision(self, direction):
        x_axis, y_axis = self.directions[direction]
        for c in range(4): # c for corner
            xm = int(self.x + x_axis + (c % 2) * (self.w-1))
            ym = int(self.y + y_axis + int(c / 2) * (self.h-1))

            col = int(xm / self.scene.tilesize) # is this slow?
            row = int(ym / self.scene.tilesize) # + y_axis?
            
            if self.scene.get_tile("collide", (col, row)) != "0":
                return True
        return False

    def move(self, direction): # will only move half the width of a tile
        self.facing = direction

        movable = not self.moving# and not self.game.fader.fading
        
        cell = tupadd(self.directions[direction], self.tile_location()) # map grid cell (col,row)
        mob = False
        for uid in self.scene.mobs:
            m = self.game.mob_db[uid]
            if m != self and cell == m.tile_location():
                mob = True
        
        tile = self.collision(direction)
        
        nocollide = not tile and not mob
        
        if movable and nocollide:
            self.direction = self.directions[direction]
            self.moving = True

    def update(self, tick):
        if self.moving:
            self.x += self.direction[0] * 2
            self.y += self.direction[1] * 2
            self.steps += 2 # all the 2s here are connected
            if self.steps >= self.game.tilesize / 2: # 16: half the distance of a tile (in this case, should be 8?) TODO
                self.moving = False
                self.steps = 0
                self.direction = (0,0)
                
            #self.frame += self.moving & (tick % 12 == 0) * 1
            #self.frame = self.frame % len(self.pattern) * self.moving
            if tick % 12 == 0:
                self.frame = ((self.frame + 1) % len(self.pattern))
        else:
            self.frame = 0

    def render(self, surface, x_off=0, y_off=0):
        x = (self.x - self.sprite.x_off) + x_off
        y = (self.y - self.sprite.y_off) + y_off
        frame = self.pattern[self.frame]
        facing = self.facings[self.facing]
        surface.blit(self.sprite.get_cell(frame, facing), (x,y))
