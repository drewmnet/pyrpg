import pygame

class Dialogue:
    def __init__(self, font, x, y, block_size, background):
        self.font = font
        self.block_size = block_size
        self.background = background
        
        self.lines = [ DialogueLine(self) for _ in range(block_size) ]
        
        self.current_line = 0
        self.current_block = 0
        self.is_visible = True        
        self.is_block_ended = False
        self.is_complete = False
        
        self.rect = (x, y, 10,10) # TODO [05/13/22]
        self.pad = 5
    
    def load_block(self):
        self.current_line = 0
        self.is_block_ended = False
        # TODO error check for text list size > self.block_size [05/14/22]
        for l, text in enumerate(self.text[self.current_block:self.current_block+self.block_size]):
            self.lines[l].load_text(text, self)
        for line in range(3):
            
        
    def update(self, tick):        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL: # 'A' button
                    if self.is_complete:
                        print("end of text")
                        exit()
                    elif self.is_block_ended: # move this [05/27/22]
                        nbi = self.current_block+self.block_size # next block index
                        next_block = self.text[nbi:nbi+self.block_size]
                        if not next_block:
                            print("end of block")
                            self.is_complete = True
                        else:
                            print("next block")
                            self.current_block += self.block_size
                            self.load_block()
                    else: # skip to the end of the dialogue block
                        for line in self.lines:
                            line.cursor = line.text_length-1
                            line.update(tick, self)
                            self.current = -1
        
        if not self.lines[-1].is_ended:
            self.lines[self.current_line].update(tick, self)
            if self.lines[self.current_line].is_ended:
                self.current_line += 1
        elif not self.is_complete and self.lines[-1].is_ended:
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
    def __init__(self, parent):
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
        
    def update(self, tick, parent):
        if tick % 2 == 0 and self.cursor < self.text_length:
            self.cursor += 1
        if not self.is_ended:
            self.label = parent.font.render(self.text[:self.cursor], 0, (0xff,0xff,0xff))
        if self.cursor == self.text_length:
            self.is_ended = True

