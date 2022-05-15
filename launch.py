#!/usr/bin/env python3

# third party
import pygame

# built in

# locals
import pyrpg

DISPLAYSIZE = (640, 480)
TILESIZE = 16
SCALE = 3

pygame.init()

game = pyrpg.core.Game(DISPLAYSIZE, TILESIZE, SCALE)

# title menu
# if "New Game" is selected:
game.player = pyrpg.scene.Player("spr_felix.png", game)
# add a scene to Game.map_db...
pyrpg.scene.Map2D("cabin_exterior.tmx", game)
# ... and setup the camera for the scene
game.camera.setup("cabin_exterior.tmx", game)
# set the camera to follow game.player
game.camera.following = game.player

game.start()
