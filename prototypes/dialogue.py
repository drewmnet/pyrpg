import pygame

# TODO first and second lines get cut off if 'A' button is pressed too early [05/07/22]

class DialogueBox:
    def __init__(self, font, block_sz=0):
        self.font = font
        self.block_sz = block_sz # in this example it is 3
        self.block = 0 # incremented by self.block_sz
        self.lines = []
        self.lines.append(DialogueLine("Prototype dialogue box.", self))
        self.lines.append(DialogueLine("Gets the job done for now.", self))
        self.lines.append(DialogueLine("More will be added eventually.", self))
        
        self.current = 0 # current line
        self.visible = True
        
        # flags
        self.COMPLETE = False # what to call the end of a line
                              # when there is text remaining? [05/07/22]
        
    def update(self, tick):        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL:
                    for line in self.lines:
                        line.cursor = line.text_length-1
                        line.update(tick, self)
                        self.current = -1 # so the next line will work
                    if self.COMPLETE:
                        self.visible = False
        if not self.lines[-1].ENDED:
            self.lines[self.current].update(tick, self)
            if self.lines[self.current].ENDED:# & self.current < len(self.lines):
                self.current += 1
        elif not self.COMPLETE and self.lines[-1].ENDED:
            print("complete") # debug; deprecate [05/07/22]
            self.COMPLETE = True
            
    def render(self, surface):
        if self.visible:
            for i, line in enumerate(self.lines):
                surface.blit(line.label, (10, 10 + 24 * i))

class DialogueLine:
    def __init__(self, text, parent): # parent=DialogueBox
        self.text = text
        self.text_length = len(self.text)+1
        
        self.cursor = 0
        self.label = parent.font.render("", 0, (0xff,0xff,0xff))
        
        # flags
        self.ENDED = False
        
    def update(self, tick, parent): # DialogueBox will pass itself as parent here
        if self.cursor == self.text_length:
            self.ENDED = True
        if tick % 2 == 0 and self.cursor <= self.text_length and not self.ENDED:
            self.cursor += 1
            self.label = parent.font.render(self.text[:self.cursor], 0, (0xff,0xff,0xff))

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

