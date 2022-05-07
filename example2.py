import pygame

# pyrpg
import pyrpg                # including but not limited to; subject to change
from pyrpg.core import *    # Game, Camera, Fader...
from pyrpg.scene import *   # Map2D, Tileset, Sprite, Mob, Player...
from pyrpg.ui import *      # TitleScreen, Dialogue, Selector, PlayerMenu...

# initialize the game object
game = Game(scale=3) # pygame.init() and display.set_mode are called

# add sprites to Game.spr_db
#Sprite("spr_felix.png", game)
#Sprite("spr_skele.png", game)
#Sprite("spr_slime.png", game)

game.player = Player("spr_felix.png", game)

# add a scene to Game.map_db...
Map2D("cabin_exterior.tmx", game)
# ... and setup the camera for the scene
game.setup_scene("cabin_exterior.tmx")

# set the camera to follow game.player
game.camera.following = game.player

running = True
while running:
    game.player.get_events()
    
    if game.EXIT:
        print("exiting example2")
        pygame.quit()
        exit()

    game.update()
    game.player.update()
    game.camera.update()
    
    game.camera.render()

    pygame.display.flip()
    game.display.fill((0,0,0))
