import pygame

class DialogueBox:
    def __init__(self, font):
        self.font = font
        self.lines = []
        self.lines.append(DialogueLine("Prototype dialogue box.", self))
        self.lines.append(DialogueLine("Gets the job done for now.", self))
        self.lines.append(DialogueLine("More will be added eventually.", self))
        
        self.current = 0 # current line
        self.visible = True
        
        # flags
        self.COMPLETE = False
        
    def update(self, tick):        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL:
                    for line in self.lines:
                        line.cursor = line.text_length
                        line.update(tick)
                        self.current = len(self.lines)-1 # so the next line will work                        
                    if self.COMPLETE:
                        self.visible = False
        if not self.lines[-1].ENDED:
            self.lines[self.current].update(tick)
            if self.lines[self.current].ENDED:# & self.current < len(self.lines):
                self.current += 1
        elif not self.COMPLETE and self.lines[-1].ENDED:
            print("complete")
            self.COMPLETE = True
            
    def render(self, surface):
        if self.visible:
            for i, line in enumerate(self.lines):
                surface.blit(line.label, (10, 10 + 24 * i))

class DialogueLine:
    # do all methods here get called externally (via DialogueBox)?
    def __init__(self, text, parent): # parent will be DialogueBox
        self.text = text
        self.text_length = len(self.text)+1
        self.parent = parent
        
        self.cursor = 0
        self.label = self.parent.font.render("", 0, (0xff,0xff,0xff))
        
        # flags
        self.ENDED = False
        
    def update(self, tick, parent=None):
        #print("line update")
        if self.cursor == self.text_length:
            #if not self.ENDED: print("ENDED")
            self.ENDED = True
        if tick % 2 == 0 and self.cursor <= self.text_length and not self.ENDED:
            self.cursor += 1
            self.label = self.parent.font.render(self.text[:self.cursor], 0, (0xff,0xff,0xff))
            #self.label = parent.font.render(self.text[:self.cursor], 0, (0xff,0xff,0xff))
            
    def render(self, surface, parent=None):
        if self.cursor < self.text_length:
            self.label = self.parent.font.render(self.text[:self.cursor], 0, (0xff,0xff,0xff))
            surface.blit(self.label, (10,10))

pygame.init()

display = pygame.display.set_mode((400,400))
clock = pygame.time.Clock()

font = pygame.font.Font(None, 24)

dbox = DialogueBox(font)

tick = 0

while 1:
    clock.tick(60)
    tick = (tick + 1) % 4294967295
    
    dbox.update(tick)
    dbox.render(display)
    
    pygame.display.flip()
    display.fill((0,0,0))

