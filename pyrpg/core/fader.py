import pygame

clamp = lambda n, minn, maxn: max(min(maxn,n), minn)

class Fader:
    def __init__(self, game, geometry):
        self.game = game
        self.curtain = pygame.Surface(geometry)
        self.curtain.fill((0,0,0))
        self.opacity = 0
        self.curtain.set_alpha(self.opacity)
        
        self.speed = 0
        self.velocity = 0 # really?
        self.faded_in = False # as in a cycle
        self.faded_out = False
        self.fading = False
    
    def fade_out(self, speed=6, colour=(0,0,0)):
        self.opacity = 0
        self.curtain.fill(colour)
        self.curtain.set_alpha(self.opacity)
        self.speed = speed
        self.velocity = self.speed
        self.fading = True
        
    def fade_in(self, speed=6, colour=None):
        if colour != None:
            self.curtain.fill(colour)
        else:
            self.curtain.fill((0,0,0))        
        self.speed = speed
        self.opacity = 255
        self.curtain.set_alpha(self.opacity)
        self.fading = True
        self.velocity = -self.speed
        
    def update(self, _): # tick will be passed but not used    
        if self.faded_in:
            self.faded_in = False
        if self.faded_out:
            self.faded_out = False
        
        if self.fading:		
            self.opacity += self.velocity
            self.opacity = clamp(self.opacity, 0, 255) # rename clamp; it keeps the number within a range
            self.curtain.set_alpha(self.opacity)
            self.faded_in = self.opacity == 0
            self.faded_out = self.opacity == 255
            self.fading = not (self.faded_in or self.faded_out)            
                
    def render(self, surface):    
        surface.blit(self.curtain,(0,0))
