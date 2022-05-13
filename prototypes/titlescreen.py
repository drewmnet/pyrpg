import pygame

class TitleScreen:
    def __init__(self):
        self.splash = pygame.Surface((400,400)).convert()
        self.splash.fill((0,0,0))
        
        self.font = pygame.font.Font("../dpcomic.ttf", 40)
        self.titlelabel = self.font.render("Skeleton Game", 0, (0xff,0xff,0xff))
    
    def render(self, surface):
        x = (surface.get_width() - self.titlelabel.get_width()) / 2
        y = 30
        surface.blit(self.titlelabel, (x,y))

pygame.init()

display = pygame.display.set_mode((400,400))

titlescreen = TitleScreen()

titlescreen.render(display)
pygame.display.flip()
pygame.time.wait(3000)
