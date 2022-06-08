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

# This is the order of pyrpg

# 1. Instantiate Game object, initializing pygame and setting up display
game = pyrpg.core.Game(DISPLAYSIZE, TILESIZE, SCALE)
game.camera = pyrpg.core.Camera(game, (0, 0)+DISPLAYSIZE)
game.fader = pyrpg.core.Fader(DISPLAYSIZE)

# 2. Initialize user interface objects
game.ui = pyrpg.ui.UI(game)
labels = ["New Game", "Quit to Desktop"]
geometry = (230, 260, 180)  # (x, y, w)
game.ui["newexit"] = pyrpg.ui.Selector(game.ui, labels, geometry)

# 3. Setup basic game loops
game.titlescreen = pyrpg.core.TitleScreen(game)
game.gameplay = pyrpg.core.Gameplay(game)
#game.battle_handler = pyrpg.combat.BattleHandler(game)

# 4. Initialize statblocks; passed to player, mob, enemy, etc.,
#...

# 5. Initialize sprites, mobs, enemy battlers, etc.,
#...

# 6. Setup player and load a default map
game.player = pyrpg.scene.Player("spr_felix.png", game)
pyrpg.scene.Map2D("podunk.tmx", game)
pyrpg.scene.Map2D("house_interior.tmx", game)
game.camera.following = game.player

# 7. Enter the main game loop
game.active_object = game.titlescreen
game.active_object.start()

game.start()
