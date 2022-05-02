#!/usr/bin/env python

# scene example

# third party
import pygame

# built in

# locals
import srpge

game = srpge.core.Game(scale=3)

srpge.scene.Sprite("clyde_sprite.png", game)

game.player = srpge.scene.Player("clyde_sprite.png", game)

srpge.scene.Scene("cliff_test.tmx", game) # srpge.scene.load("example1.tmx", game)
game.setup_scene("cliff_test.tmx")

game.camera.following = game.player

running = True
while running:
    game.player.get_events()
    
    if game.EXIT:
        print("exiting example0")
        pygame.quit()
        exit()

    game.update()
    game.player.update(game.tick)
    game.camera.update()
    
    game.camera.render()

    pygame.display.flip()
    game.display.fill((0,0,0))
