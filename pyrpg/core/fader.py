import pygame


class Fader:
    def __init__(self, geometry):
        self.curtain = pygame.Surface(geometry)
        self.curtain.fill((0, 0, 0))
        self.opacity = 0
        self.curtain.set_alpha(self.opacity)
        self.speed = 0
        self.is_faded_in = False  # as in a cycle
        self.is_faded_out = False
        self.is_fading = False

    def fade(self, speed, colour):
        self.speed = speed
        self.curtain.fill(colour)
        self.opacity = (speed < 0) * 255
        self.curtain.set_alpha(self.opacity)
        self.is_fading = True
        
    def fade_out(self): self.fade(6, (0, 0, 0))
    def fade_in(self): self.fade(-6, (0, 0, 0))

    def update(self, _):  # tick will be passed but not used
        if self.is_faded_in:
            self.is_faded_in = False
        if self.is_faded_out:
            self.is_faded_out = False
        if self.is_fading:
            self.opacity += self.speed
            self.opacity = max(min(255, self.opacity), 0)
            self.curtain.set_alpha(self.opacity)
            self.is_faded_in = self.opacity == 0
            self.is_faded_out = self.opacity == 255
            self.is_fading = not (self.is_faded_in or self.is_faded_out)

    def render(self, surface):
        surface.blit(self.curtain, (0, 0))
