import pygame


class Mob:
    def __init__(self, colour, cm): # control method
        self.colour = colour
        self.cm = cm
        self.rect = pygame.Rect((10,10,32,32))
        
    def update(self):
        self.cm(self)
        
    def render(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)

def cm_player(mob):
    pygame.event.get()
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP]:
        mob.rect.y -= 2
    elif keys[pygame.K_DOWN]:
        mob.rect.y += 2
        
    if keys[pygame.K_LEFT]:
        mob.rect.x -= 2
    elif keys[pygame.K_RIGHT]:
        mob.rect.x += 2

pygame.init()

display = pygame.display.set_mode((500,500))

player_mob = Mob((0xff,0,0), cm_player)

running = True
while running:
    player_mob.update()
    player_mob.render(display)
    
    pygame.display.flip()
    display.fill((0,0,0))
