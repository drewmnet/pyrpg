import pygame

class Dialogue:
    def __init__(self, font, x, y, block_size, background):
        self.font = font
        self.block_size = block_size # in this example it is 3
        self.background = background
        
        self.lines = [ DialogueLine(self) for _ in range(block_size) ]
        
        self.text = []
        
        self.current_line = 0
        self.current_block = 0
        self.is_visible = True        
        self.is_block_ended = False
        self.is_complete = False # what to call the end of a line
                               # when there is text remaining? [05/07/22]
        #self.load_block()
        
        self.rect = (x, y, 10,10) # TODO [05/13/22]
        self.pad = 5
    
    def load_block(self):
        self.current_line = 0
        self.is_block_ended = False
        #self.is_complete = False
        # TODO error check for text list size > self.block_size [05/14/22]
        for l, text in enumerate(self.text[self.current_block:self.current_block+self.block_size]):
            self.lines[l].load_text(text, self)
        
    def update(self, tick):        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_RCTRL: # 'A' button
                    if self.is_complete:
                        print("end of text")
                        exit()
                    elif self.is_block_ended:
                        #self.is_visible = False
                        nbi = self.current_block+self.block_size # next block index
                        next_block = self.text[nbi:nbi+self.block_size]
                        if not next_block:
                            print("end of block")
                            self.is_complete = True
                        else:
                            print("next block")
                            self.current_block += self.block_size
                            self.load_block()
                        # self.next()
                    else: # skip to the end of the dialogue block
                        for line in self.lines:
                            line.cursor = line.text_length-1
                            line.update(tick, self)
                            self.current = -1 # so the next line will work
        
        if not self.lines[-1].is_ended: # if the last line is not ended ...
            self.lines[self.current_line].update(tick, self) # ... update the dialogue boxes current line and ...
            if self.lines[self.current_line].is_ended:# & self.current < len(self.lines):
                self.current_line += 1 # ... if the current line is ended, switch to the next line in the block
        elif not self.is_complete and self.lines[-1].is_ended: # replace complete with self._blockended?
            self.is_block_ended = True
            
    def render(self, surface):
        if self.is_visible:
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
                
        self.is_ended = False

    def load_text(self, text, parent):
        self.cursor = 0
        self.text = text
        self.text_length = len(self.text)+1
        self.is_ended = False
        self.label = parent.font.render("", 0, (0xff,0xff,0xff))
        
    def update(self, tick, parent): # DialogueBox will pass itself as parent here
        if tick % 2 == 0 and self.cursor < self.text_length:
            self.cursor += 1
        if not self.is_ended:
            self.label = parent.font.render(self.text[:self.cursor], 0, (0xff,0xff,0xff))
        if self.cursor == self.text_length:
            self.is_ended = True

