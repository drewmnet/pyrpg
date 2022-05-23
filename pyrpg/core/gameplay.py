

class Gameplay:
    def __init__(self, game):
        self.game = game
    
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
        
    def render(self, surface):
        self.game.camera.render(surface)
        self.game.fader.render(surface)
