import pygame

from . import mob

class Player(mob.Mob):
    def __init__(self, filename, game):
        self.uid = "player"
        mob.Mob.__init__(self, filename, self.uid, game)

    def get_events(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            self.move("south")
        elif keys[pygame.K_UP]:
            self.move("north")
        
        if keys[pygame.K_RIGHT]:
            self.move("east")
        elif keys[pygame.K_LEFT]:
            self.move("west")

