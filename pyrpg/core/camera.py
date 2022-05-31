import operator

import pygame

def y_sort(mobs):
    return sorted(mobs, key=operator.attrgetter('y'))

class Camera(pygame.Rect):
    def __init__(self, game, geometry):
        self.game = game
        self.tilesize = game.tilesize
        pygame.Rect.__init__(self, geometry)
        
        self.display_cols = 0
        self.display_rows = 0
        self.following = None
        self.scene = None

        self.scene_rect = pygame.Rect((0,0,0,0))
    
    def setup(self, filename, loc=None):
        if filename not in self.game.scene_db:
            print(f"'{filename}' not found")
            pygame.quit()
            exit()
            
        self.scene = self.game.scene_db[filename]
        self.following = self.game.player
        self.display_cols = self.w // self.tilesize + 2
        self.display_rows = self.h // self.tilesize + 2
        self.blank = pygame.Surface((self.tilesize,self.tilesize)).convert()
        self.blank.fill((0,0,0))
        self.scene_rect.w = (self.scene.cols) * self.tilesize
        self.scene_rect.h = (self.scene.rows) * self.tilesize
        # reset mobs in scene to default positions and facings
        for mob_fn in self.scene.mobs:
            if mob_fn != "player":
                self.game.mob_db[mob_fn].spawn(filename)
        
        if loc is not None:
            self.game.mob_db["player"].spawn(filename, loc)
        else:
            self.game.mob_db["player"].spawn(filename)
            
        self.game.player.is_moving = False
        self.center = self.following.center

    def prep_bottom_middle_tiles(self, col, row):
        x_offset = self.x % self.tilesize
        y_offset = self.y % self.tilesize

        c_index = self.x // self.tilesize + col
        r_index = self.y // self.tilesize + row
    
        bottom_index = self.scene.get_tile("bottom", (c_index,r_index))
        middle_index = self.scene.get_tile("middle", (c_index,r_index))

        x = col * self.tilesize - x_offset
        y = row * self.tilesize - y_offset

        bottom_tile = None
        middle_tile = None

        if middle_index != "0":
            middle_tile = self.scene.tileset[middle_index]
        if bottom_index != "0":
            bottom_tile = self.scene.tileset[bottom_index]

        return (bottom_tile, middle_tile, x, y)

    def prep_top_tile(self, col, row):
        x_offset = self.x % self.tilesize
        y_offset = self.y % self.tilesize

        c_index = self.x // self.tilesize + col
        r_index = self.y // self.tilesize + row
    
        top_index = self.scene.get_tile("top", (c_index,r_index))

        x = col * self.tilesize - x_offset
        y = row * self.tilesize - y_offset

        top_tile = None
        if top_index != "0":
            top_tile = self.scene.tileset[top_index]
        
        return (top_tile, x, y)
            
    def update(self, tick):
        self.scene.update(tick)
    
        self.center = self.following.center    
    
        if self.center[0] < self.following.center[0]:
            self.move_ip((2,0))
        elif self.center[0] > self.following.center[0]:
            self.move_ip((-2,0))
        
        if self.center[1] < self.following.center[1]:
            self.move_ip((0,2))
        elif self.center[1] > self.following.center[1]:
            self.move_ip((0,-2))
        
        self.clamp_ip(self.scene_rect)

    def render(self, surface):
        for drow in range(self.display_rows):
            for dcol in range(self.display_cols):
                bottom_tile, middle_tile, x, y = self.prep_bottom_middle_tiles(dcol, drow)
                
                if bottom_tile != None:
                    surface.blit(bottom_tile, (x,y))

                if middle_tile != None:
                    surface.blit(middle_tile, (x,y))

        if self.scene.mobs:
            sorted_mobs = y_sort(self.scene.get_mobs())
            for sprite in sorted_mobs:
                sprite.render(surface, self.x, self.y)
        
        for drow in range(self.display_rows):
            for dcol in range(self.display_cols):
                tile, x, y = self.prep_top_tile(dcol, drow)
                if tile != None: surface.blit(tile, (x, y))
