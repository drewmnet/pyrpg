import pygame


def invert_colours(surface):
    image_neg = pygame.Surface(surface.get_size()).convert()
    for y in range(surface.get_height()):
        for x in range(surface.get_width()):
            pixel = surface.get_at((x, y))
            if pixel[3] == 0:
                image_neg.set_at((x, y), (0,0,0,0))
                image_neg.set_colorkey(image_neg.get_at((0, 0)))
            else:
                r = 255 - pixel[0]
                g = 255 - pixel[1]
                b = 255 - pixel[2]
                image_neg.set_at((x, y), (r, g, b, 255))
    return image_neg

class EnemyBattler:
    def __init__(self, filename):
        image = pygame.image.load(filename)
        image_neg = invert_colours(image)
        self.images = [image, image_neg]

class Enemy:
    def __init__(self, battler):
        self.battler = battler        
        self.is_flashing = False
        self.is_complete = False
        self.f_interval = 0
        self.frame = 0
        self.tick = 0
        
    def flash(self):
        self.is_flashing = True
        self.f_interval = pygame.time.get_ticks()
        
    def update(self):
        self.is_complete = False
        f = pygame.time.get_ticks() - self.f_interval
        if f // 125 == 1 and self.is_flashing:
            self.frame = (self.frame + 1) % 2
            self.tick += 1
            self.f_interval = pygame.time.get_ticks()
        
            if self.tick == 4:
                self.tick = 0
                self.frame = 0
                self.is_flashing = False
                self.is_complete = True
                
    def render(self, surface):
        display.blit(self.battler.images[self.frame], (10,10))

