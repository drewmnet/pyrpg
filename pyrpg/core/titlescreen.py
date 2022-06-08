import pygame


class TitleScreen:
    def __init__(self, game):
        self.game = game
        self.splash = pygame.Surface(self.game.display.get_size()).convert()
        self.splash.fill((0,0,0))
        
        self.title_label = game.ui_basic_font.render("Skeleton Game", 0, (0xff,0xff,0xff))        
        self.is_exiting = False
    
    def start(self):
        self.game.fader.fade_in()
    
    def update(self, tick):
        if not self.game.fader.is_fading:
            self.game.ui["newexit"].get_input()
            if self.game.ui["newexit"].rvalue == 0: # 'New Game'
                self.game.camera.setup("podunk.tmx")
                self.game.ui["newexit"].rvalue = None
                self.game.fader.fade_out()
            if self.game.ui["newexit"].rvalue == 1: # 'Quit to Desktop'
                self.is_exiting = True
                self.game.fader.fade_out()
                self.game.ui["newexit"].rvalue = None
                
        if self.game.fader.is_faded_out:
            if not self.is_exiting:
                self.game.active_object = self.game.gameplay
                self.game.active_object.start()
            else:
                self.game.is_running = False
        
        self.game.fader.update(tick)
                
    def render(self, surface):
        x = (surface.get_width() - self.title_label.get_width()) / 2
        y = 90
        surface.blit(self.title_label, (x,y))
        self.game.ui["newexit"].render(surface)
        self.game.fader.render(surface)

