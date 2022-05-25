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
game.camera = pyrpg.core.Camera(game, (0,0)+DISPLAYSIZE)
game.fader = pyrpg.core.Fader(DISPLAYSIZE)

game.ui = pyrpg.ui.UI(game)
labels = ["New Game", "Quit to Desktop"]
geometry = (230, 260, 180) # (x, y, w)
game.ui["newexit"] = pyrpg.ui.Selector(game.ui, labels, geometry)

game.player = pyrpg.scene.Player("spr_felix.png", game)
pyrpg.scene.Map2D("podunk.tmx", game)
pyrpg.scene.Map2D("house_interior.tmx", game)
game.camera.following = game.player

game.titlescreen = pyrpg.core.TitleScreen(game)
game.gameplay = pyrpg.core.Gameplay(game)

for switch in game.scene_db["podunk.tmx"].switches.values():
    print(switch)

game.active_object = game.titlescreen
game.active_object.start()

game.start()
