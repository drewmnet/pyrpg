import pygame

class Theme:
    # colour palette; GameBoy style
    palette = { "light": (0xfa, 0xfb, 0xf6),
                "shade": (0xc6, 0xb7, 0xbe),
                "grey": (0x56, 0x5a, 0x75),
                "dark": (0x0f, 0x0f, 0x1b)
              }

    # dialogue attributes
    background = palette["grey"] # None for total transparency
    padding = 5

    # fonts
    basic_font = pygame.font.Font("dpcomic.ttf", 28)

