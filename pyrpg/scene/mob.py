import pygame

import os

#tupadd = lambda t1, t2: tuple(map(sum, zip(t1,t2)))

def load_sprite(filename, scale): #(filename, scale, control_function)
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
        pygame.Rect.__init__(self, (0, 0, 16 * game.scale - 2 * game.scale, 16 * game.scale - 2 * game.scale))
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
        self.x = col * self.game.tilesize + (self.game.scale * 2) // 2
        self.y = row * self.game.tilesize + self.game.scale * 2

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

    def collision(self, direction):
        for c in range(4):
            x_axis, y_axis = direction
            xm = (self.x + x_axis * 2) + (c % 2) * self.w
            ym = (self.y + y_axis * 2) + (c // 2) * self.h

            col = xm // self.game.tilesize
            row = ym // self.game.tilesize
                
            if self.scene.get_tile("collide", (col, row)) != "0":
                return True

    def move(self, direction):
        x_axis, y_axis = self.directions[direction]
        self.facing = direction

        if x_axis != 0 or y_axis != 0:
            self.is_moving = True
        if x_axis == 0 and y_axis == 0:
            self.is_moving = False

        if self.is_moving:        
            if not self.collision((x_axis, 0)):
                self.move_ip(x_axis * 2, 0)
            if not self.collision((0, y_axis)):
                self.move_ip(0, y_axis * 2)
    
    def reset(self):
        self.is_moving = False
        self.steps = 0
        self.direction = (0,0)
    
    def update(self):
        if self.is_moving:
            self.x += self.direction[0] * 2
            self.y += self.direction[1] * 2
            self.steps += 2 # replace these 2s with a variable
            if self.steps >= self.game.tilesize // 2:
                self.reset()

    def render(self, surface, x_off, y_off):
        x = self.x - (self.game.scale * 2) // 2 - x_off
        y = self.y - (self.game.scale * 2) - y_off
        surface.blit(self.game.sprite_db[self.spr_fn][self.facing], (x, y))

