import pygame

class TitleScreen:
    def __init__(self, game):
        self.game = game
        self.splash = pygame.Surface((640, 480)).convert()
        self.splash.fill((0,0,0))
        
        #self.font = pygame.font.Font("../dpcomic.ttf", 40)
        self.titlelabel = game.ui.theme.basic_font.render("Skeleton Game", 0, (0xff,0xff,0xff))        
    
    def update(self, tick):
        """ Assumes game.ui["newexit"] has been instantiated """
        self.game.ui["newexit"].get_input()
        if self.game.ui["newexit"].rvalue == 1:
            self.game.exiting = True
            print("kupo!")
    
    def render(self, surface):
        x = (surface.get_width() - self.titlelabel.get_width()) / 2
        y = 90
        surface.blit(self.titlelabel, (x,y))
        self.game.ui["newexit"].render(surface)

if __name__ == "__main__":
    pygame.init()

    display = pygame.display.set_mode((400,400))

    titlescreen = TitleScreen()

    titlescreen.render(display)
    pygame.display.flip()
    pygame.time.wait(3000)
