#!/usr/bin/env python

import pygame

import pyrpg

SCREENSIZE = (640,480)
TILESIZE = 16
SCALE = 3

game = pyrpg.core.Game(SCREENSIZE, TILESIZE, SCALE)

dialogue = pyrpg.ui.Dialogue(pygame.font.Font(None, 24), 10, 10, 3, None)
dialogue.text = [ "Hello", "new", "dialogue test", "next block", " ", " " ]
dialogue.load_block()

while True:
    game.update()
    dialogue.update(game.tick)

    dialogue.render(game.display)

    pygame.display.flip()
    game.display.fill((0,0,0))
