print("importing Player class")

import pygame

from .mob import Mob

class Player(Mob):
    def __init__(self, filename, game):
        self.uid = "player"
        Mob.__init__(self, filename, self.uid, game)

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.EXIT = True
        #pygame.event.get() #[1]
        keys = pygame.key.get_pressed() #[1] won't work without calling pygame.event.get()

        #if not self.game.fader.fading:
        if keys[pygame.K_DOWN]:
            self.move("south")
        elif keys[pygame.K_UP]:
            self.move("north")
        elif keys[pygame.K_RIGHT]:
            self.move("east")
        elif keys[pygame.K_LEFT]:
            self.move("west")
