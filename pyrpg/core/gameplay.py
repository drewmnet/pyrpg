

class Gameplay:
    def __init__(self, game):
        self.game = game
        
        self.is_switching = False
        self.switching_to = None
        self.facing = None
    
    def start(self):
        self.game.fader.fade_in()
    
    def update(self, tick):
        if not self.game.fader.is_fading:
            self.game.player.get_events()            
            self.game.camera.update(tick)
            
            if self.game.player.is_exiting and self.game.fader.is_faded_out:
                self.game.active_object = self.game.titlescreen
                self.game.active_object.start()
        self.game.fader.update(tick)
        
        for switch in self.game.camera.scene.switches.values():
            if self.game.player.colliderect(switch[0]) and not self.is_switching:
                self.is_switching = True
                self.switching_to = switch[1]
                self.spawning_at = switch[2]
                self.facing = switch[3]
                self.game.fader.fade_out()
                
        if self.is_switching and self.game.fader.is_faded_out:
            self.game.camera.setup(self.switching_to, self.spawning_at)
            self.game.player.facing = self.facing
            self.is_switching = False
            self.game.fader.fade_in()
            
        
    def render(self, surface):
        self.game.camera.render(surface)
        self.game.fader.render(surface)
