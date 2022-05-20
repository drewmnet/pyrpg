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
game.camera = pyrpg.core.Camera(game, (0,0))
game.fader = pyrpg.core.Fader(game, DISPLAYSIZE)

game.ui = pyrpg.ui.UI(game)
game.ui["newexit"] = pyrpg.ui.Selector(game.ui, ["New Game", "Quit to Desktop"], 230, 260, 180)
#game.renderlist = [ game.titlescreen, game.fader ]

# titlescreen and gameplay are collections of objects stored within a single object
game.titlescreen = pyrpg.core.TitleScreen(game)
game.gameplay = pyrpg.core.Gameplay(game)

game.active_object = game.titlescreen
game.active_object.start()
#game.control = game.fader
#active_object

# title menu
# if "New Game" is selected:
game.player = pyrpg.scene.Player("spr_felix.png", game)
# add a scene to Game.map_db...
pyrpg.scene.Map2D("podunk.tmx", game)
# ... and setup the camera for the scene
#game.camera.setup("podunk.tmx", game)
# set the camera to follow game.player
game.camera.following = game.player

#game.focus = game.camera

game.start()
