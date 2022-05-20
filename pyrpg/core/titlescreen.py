import pygame

class TitleScreen:
    def __init__(self, game):
        self.game = game
        self.splash = pygame.Surface((640, 480)).convert()
        self.splash.fill((0,0,0))
        
        self.titlelabel = game.ui.theme.basic_font.render("Skeleton Game", 0, (0xff,0xff,0xff))        
        self.exiting = False
    
    def start(self):
        self.game.fader.fade_in()
    
    def update(self, tick):
        """ Assumes game.ui["newexit"] has been instantiated """
        if not self.game.fader.fading:
            self.game.ui["newexit"].get_input()
            if self.game.ui["newexit"].rvalue == 0:
                # clear events
                self.game.camera.setup("podunk.tmx")
                #self.game.active_object = self.game.camera
                self.game.ui["newexit"].rvalue = None
                self.game.fader.fade_out()
            if self.game.ui["newexit"].rvalue == 1:
                self.exiting = True
                self.game.fader.fade_out()
                self.game.ui["newexit"].rvalue = None
                
        self.game.fader.update(tick)
        
        if self.game.fader.faded_out:
            if not self.exiting:
                print("monk")
                self.game.active_object = self.game.gameplay
                self.game.active_object.start()
            else:
                self.game.exiting = True
                
    def render(self, surface):
        x = (surface.get_width() - self.titlelabel.get_width()) / 2
        y = 90
        surface.blit(self.titlelabel, (x,y))
        self.game.ui["newexit"].render(surface)
        self.game.fader.render(surface)

