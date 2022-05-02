#!/usr/bin/env python3

# c6b7be

light = (0xfa, 0xfb, 0xf6)
shade = (0xc6, 0xb7, 0xbe)
grey = (0x56, 0x5a, 0x75)
dark = (0x0f, 0x0f, 0x1b)

import pygame

class SelectorBox:
    def __init__(self, labels, x, y, width):
        self.font = pygame.font.Font("dpcomic.ttf", 28)
        self.font_h = self.font.get_height()
        self.labels = labels # a list strings
        
        self.pad = 5
        height = len(self.labels) * self.font_h + self.pad + 2
        self.rect = (x, y, width, height)        
        
        self.value = 0        
        
    def render_label(self, label, value):
        if value == self.value:
            colour = light
        else:
            colour = shade
        return self.font.render(label, 0, colour)
        
    def render(self, surface):
        pygame.draw.rect(surface, grey, self.rect)
        for i, l in enumerate(self.labels):
            label = self.render_label(l, i)
            x = self.rect[0] + self.pad
            y = self.rect[1] + self.font_h * i + self.pad
            surface.blit(label, (x, y))
            
    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.value = (self.value + 1) % len(self.labels)
                elif event.key == pygame.K_UP:
                    self.value = (self.value - 1) % len(self.labels)
                elif event.key == pygame.K_RCTRL:
                    print(self.value)

pygame.init()
clock = pygame.time.Clock()

display = pygame.display.set_mode((500,500))

sb = SelectorBox(["Items", "Gear", "Status"], 10, 10, 100)

while 1:
    clock.tick(60)
    sb.get_input()

    sb.render(display)

    pygame.display.flip()

