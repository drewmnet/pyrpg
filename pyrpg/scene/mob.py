import pygame

import os

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
        self.spr_fn = filename
        self.game.mob_db[self.uid] = self
        
    def place(self, col, row):
        self.x = col * self.game.tilesize
        self.y = row * self.game.tilesize

    def spawn(self, filename, loc=None):    
        self.scene = self.game.scene_db[filename]
        if loc is not None:
            col, row = loc
        else:
            col, row = self.scene.defaults[self.uid]
        self.place(col, row)
        self.facing = "south"

    def tile_location(self):
        return (self.x // self.game.tilesize, self.y // self.game.tilesize)

    def move(self, direction):
        if not self.is_moving:
            self.facing = direction
        
        cell = tupadd(self.directions[direction], self.tile_location())
        has_mob = False
        for uid in self.scene.mobs:
            m = self.game.mob_db[uid]
            if m != self and not cell == m.tile_location():
                has_mob = True
        
        tile = self.game.camera.scene.get_tile("collide", cell)        
        is_colliding = tile != '0' and not has_mob
        is_movable = not self.is_moving
        if not is_colliding and is_movable:
            self.direction = self.directions[direction]
            self.is_moving = True
    
    def reset(self):
        self.is_moving = False
        self.steps = 0
        self.direction = (0,0)
    
    def update(self):
        if self.is_moving:
            self.x += self.direction[0] * 2
            self.y += self.direction[1] * 2
            self.steps += 2 # replace these 2s with a variable
            if self.steps >= self.game.tilesize:
                self.reset()

    def render(self, surface, x_off, y_off):
        x = self.x - x_off
        y = self.y - y_off
        surface.blit(self.game.sprite_db[self.spr_fn][self.facing], (x, y))

