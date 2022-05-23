import pygame

class Selector:
    def __init__(self, ui, labels, geometry):
        self.ui = ui
        #self.theme = ui.theme
        self.labels = labels # a list strings
        
        self.fontheight = ui.theme.basic_font.get_height()
        self.padding = ui.theme.padding
        height = len(self.labels) * self.fontheight + self.padding + 2
        self.rect = geometry + tuple([height]) # (x, y, w) + (h)
        
        self.value = 0
        self.rvalue = None # return value
        
    def render_label(self, label, value):
        if value == self.value:
            colour = self.ui.theme.palette["light"]
        else:
            colour = self.ui.theme.palette["shade"]
        return self.ui.theme.basic_font.render(label, 0, colour)
        
    def render(self, surface):
        pygame.draw.rect(surface, self.ui.theme.palette["grey"], self.rect)
        for i, l in enumerate(self.labels):
            label = self.render_label(l, i)
            x = self.rect[0] + self.padding
            y = self.rect[1] + self.fontheight * i + self.padding
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

