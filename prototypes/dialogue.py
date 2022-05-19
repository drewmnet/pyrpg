import pygame

class DialogueBox:
    def __init__(self, font, x, y, block_size, background):
        self.font = font
        self.block_size = block_size # in this example it is 3
        self.block = 0 # incremented by self.block_size
        self.background = background
        
        self.lines = [ DialogueLine(self) for _ in range(block_size) ]
        
        self.text = []
        
        self._current = 0 # current line
        self._visible = True        
        self._blockended = False
        self._complete = False # what to call the end of a line
                               # when there is text remaining? [05/07/22]
        #self.load_block()
        
        self.rect = (x, y, 10,10) # TODO [05/13/22]
        self.pad = 5
    
    def load_block(self):
        self._current = 0 # future proofed for larger blocks of text
        self._complete = False
        #self._blockended = False
        # TODO error check for text list size > self.block_size [05/14/22]
        for l, text in enumerate(self.text[self.block:self.block+self.block_size]):
            self.lines[l].load_text(text, self)
        
    def update(self, tick):        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL: # 'A' button
                    if self._complete:
                        self._visible = False
                    else: # skip to the end of the dialogue block
                        for line in self.lines:
                            line.cursor = line.text_length-1
                            line.update(tick, self)
                            self.current = -1 # so the next line will work
        if not self.lines[-1].ended: # if the last line is not ended ...
            self.lines[self._current].update(tick, self) # ... update the dialogue boxes current line and ...
            if self.lines[self._current].ended:# & self.current < len(self.lines):
                self._current += 1 # ... if the current line is ended, switch to the next line in the block
        elif not self._complete and self.lines[-1].ended: # replace complete with self._blockended?
            self._complete = True
            
    def render(self, surface):
        if self._visible:
            #if self.background is not None:
                #pygame.draw.rect(surface, grey, self.rect)
            for i, line in enumerate(self.lines):
                x = self.rect[0] + self.pad
                y = self.rect[1] + self.font.get_height() * i + self.pad
                surface.blit(line.label, (x, y))

class DialogueLine:
    def __init__(self, parent):#text, parent): # parent=DialogueBox
        self.label = parent.font.render("", 0, (0xff,0xff,0xff))
        self.cursor = 0
        
        self.text = ""
        self.text_length = 0 #len(self.text)+1
                
        self.ended = False

    def load_text(self, text, parent):
        self.cursor = 0
        self.text = text
        self.text_length = len(self.text)+1
        self.label = parent.font.render("", 0, (0xff,0xff,0xff))
        
    def update(self, tick, parent): # DialogueBox will pass itself as parent here
        if tick % 2 == 0 and self.cursor < self.text_length:
            self.cursor += 1
        if not self.ended:
            self.label = parent.font.render(self.text[:self.cursor], 0, (0xff,0xff,0xff))
        if self.cursor == self.text_length:
            self.ended = True
        
pygame.init()

display = pygame.display.set_mode((400,400))
clock = pygame.time.Clock()

font = pygame.font.Font("../dpcomic.ttf", 24)

dbox = DialogueBox(font, 10, 10, 3, None)
dbox.text = ["This is line 1", "This is line 2", "This is line 3"]
dbox.load_block()

tick = 0

while 1:
    clock.tick(60)
    tick = (tick + 1) % 4294967295
    
    dbox.update(tick)
    dbox.render(display)
    
    pygame.display.flip()
    display.fill((0,0,0))

    #if dbox.complete:
    #    pygame.time.wait(1000)
    #    exit()
