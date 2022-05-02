print("importing Dialogue class") # ("importing srpge.ui.Dialogue")

import pygame

class Dialogue:
    def __init__(self, game, rect, vis_lines=3): # rect is a tuple of 4 integers
        self.game = game
        self.rect = pygame.Rect(rect)
        
        self.ui = None

        self.vis_lines = vis_lines # an integer; the number of visible lines (usually 2 or 3)
        self.txt_list = [] # a full list of text
        
        self.txt_block = 0 # which block of text from list to be put into queue
        self.txt_queue = [] # the lines to be iterated over
        
        self.txt_line = 0 # an int tracking which line in the queue is being iterated over
        self.txt_cursors = [] # the length of each line in the queue; starts at 0 and increments by 1
        
        self.eoq = False # end of queue
        self.eof = False # "End Of File"; end of list of text
        
        self.writing = False
        self.visible = False
        print("Dialogue instance")
    
    def backplate(self): # sets up the backplate of the dialogue box after being assigned to a ui object
        if self.ui:
            self.back = pygame.Surface(self.rect[2:]).convert_alpha()
            self.back.fill(tuple(list(self.ui.bgcolour)+[self.ui.alpha]))
        else:
            print("Dialogue.ui is None")
            pygame.quit()
            exit()
    
    def start(self, txt_list): # called externally
        self.txt_list = txt_list    
        self.txt_line = 0
        self.txt_block = 0
        self.txt_cursors = []
        
        self.visible = True
        self.eoq = False
        self.eof = False
        
        self.game.controller.flush() # to prevent any terminate signals from being sent
        self.next()
        
    def skip(self): # skip to the end of the current block; called internally
        for index, line in enumerate(self.txt_queue):
            self.txt_cursors[index] = len(line)
        self.writing = False

    def next(self): # called internally
        self.txt_queue = []
        self.txt_cursors = [0] * self.vis_lines
        self.txt_line = 0
        self.txt_queue = self.txt_list[self.txt_block:self.txt_block+self.vis_lines]

        if not self.txt_queue:
            self.eof = True
            return
        self.writing = True
        
    def get_input(self, a_button): # (a,b,x,y)    
        # invoke only when a button is pressed
        if a_button:
            # if end of queue then check for more text;
            # if there is no more text, signal eof
            if self.writing: # skip to the end of this block
                self.skip()
            elif self.eoq:
                self.txt_block += self.vis_lines
                self.next()
                
    def update(self, tick=0): # TODO tick doesn't do anything at the moment
        if not self.eof:
            # if dialogue is writing, increment the cursor by 1
            if self.writing and self.game.tick % 2 == 0:
                self.txt_cursors[self.txt_line] += 1
            
            # if the cursor is at the end of the current line,
            #  proceed to the next line
            if self.txt_cursors[self.txt_line] == len(self.txt_queue[self.txt_line]) \
               and self.txt_line < self.vis_lines-1:
                self.txt_line += 1
            
            # if at the end of the last line in the queue, stop writing and signal end of queue
            if self.txt_line == self.vis_lines-1 and self.txt_cursors[self.txt_line] == len(self.txt_queue[-1]):
                self.writing = False
                self.eoq = True
        
            # TODO put slow text here; the slow text is for dramatic effect
        
    def render(self):    
        if self.visible:        
            self.game.display.blit(self.back, self.rect[:2])
    
            for i, l in enumerate(self.txt_queue):
                txt = l[:self.txt_cursors[i]]
                #if ">" in text:	text = re.sub(">", "", text)
                txt_image = self.ui.font.render(txt, 0, (255,255,255))
                
                x,y = self.rect[:2]
                x += 5 # padding
                y += 5 * (i+1) + i * self.ui.font.get_height()
                self.game.display.blit(txt_image, (x,y))
