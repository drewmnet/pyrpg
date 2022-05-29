import pygame


class Selector:
    def __init__(self, ui, labels, geometry):
        self.ui = ui # replace ui with game
        self.labels = labels # a list strings
        
        self.font_height = ui.game.ui_basic_font.get_height()
        self.padding = ui.game.ui_padding
        height = len(self.labels) * self.font_height + self.padding + 2
        self.rect = geometry + tuple([height]) # (x, y, w) + (h)
        
        self.value = 0
        self.rvalue = None # return value
        
    def render_label(self, label, value):
        if value == self.value:
            colour = self.ui.game.ui_palette["light"]
        else:
            colour = self.ui.game.ui_palette["shade"]
        return self.ui.game.ui_basic_font.render(label, 0, colour)
        
    def render(self, surface):
        pygame.draw.rect(surface, self.ui.game.ui_palette["grey"], self.rect)
        for i, l in enumerate(self.labels):
            label = self.render_label(l, i)
            x = self.rect[0] + self.padding
            y = self.rect[1] + self.font_height * i + self.padding
            surface.blit(label, (x, y))
            
    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.value = (self.value + 1) % len(self.labels)
                elif event.key == pygame.K_UP:
                    self.value = (self.value - 1) % len(self.labels)
                elif event.key == pygame.K_RCTRL: # 'A' button
                    self.rvalue = self.value

