

class Gameplay:
    def __init__(self, game):
        self.game = game
    
    def start(self):
        print("starting gameplay")
        self.game.fader.fade_in()
    
    def update(self, tick):
        if not self.game.fader.fading:
            self.game.player.get_events()
            
            self.game.camera.update(tick)
            
            if self.game.player.exiting and self.game.fader.faded_out:
                self.game.player.exiting = False
                self.game.active_object = self.game.titlescreen
                self.game.active_object.start()
        self.game.fader.update(tick)
        
    def render(self, surface):
        self.game.camera.render(surface)
        self.game.fader.render(surface)
