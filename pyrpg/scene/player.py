# Code and Chill

import pygame

from . import mob, utilities

class Player(mob.Mob):
    def __init__(self, filename, game):
        self.uid = "player"
        mob.Mob.__init__(self, filename, self.uid, game)

        self.a_button = 0 # TODO re/move this; only for testing; or should I?

    def get_events(self):
        for event in pygame.event.get(): #[1]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.exiting = True
                    #self.game.fader.fade_out()
                if event.key == pygame.K_RETURN:
                    if self.game.camera.following == None:
                        self.game.camera.following = self
                    else:
                        self.game.camera.following = None
                #if event.key == pygame.K_RSHIFT:
                #    self.game.text_hud.add("Placeholder text")

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

        if not self.moving: #TODO move this to event loop
            # priority of "A" button check:
            #  sprite check (mobs, furnis, etc.,)
            #  switch check (to switch to a different map;
            #  eg. interacting with the door of a house then switching to a Scene of the interior
            if keys[pygame.K_RCTRL] and self.a_button == 0:
                self.a_button = 1
                #pygame.draw.rect(app.display,(0xff,0,0),interact(mob0)+(12,12))
                #print(interact(x,y,facing)) # interact(x,y,facing)
                #print(interact(app.player))
                tile = utilities.tupadd(self.directions[self.facing], self.tile_location())
                for mob in self.scene.mobs: # should 'mob' be 'uid'?
                    if self.game.mob_db[mob] != self:
                        if tile == self.game.mob_db[mob].tile_location():
                            self.game.text_hud.add(self.game.mob_db[mob].spr_fn)
                            return
                c,r = utilities.interact(self)
                for switch in self.game.scene.switches.values():
                    # refactor to take Game.scale into account [05/07/22]
                    c_comp = switch[0].x // 16 == c
                    r_comp = switch[0].y // 16 == r
                    if c_comp and r_comp:
                        self.game.next_scene = switch[1]
                        self.game.switching = True
                        self.game.fader.fade_out()
            elif not keys[pygame.K_RCTRL] and self.a_button == 1:
                self.a_button = 0

