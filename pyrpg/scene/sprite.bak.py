print("importing Sprite class")

import os

import pygame

def load_sprite(filename, scale=1):
    image = pygame.image.load(filename)
    image.convert()
    image.set_colorkey(image.get_at((0,0)), pygame.RLEACCEL)
    # [sprite format] size of cells; rectangle dimensions; x and y offsets
    cell_w, cell_h = image.get_at((0, image.get_height()-1))[:2]
    rect = pygame.Rect((0,0)+image.get_at((1, image.get_height()-1))[:2])
    padding = image.get_at((2, image.get_height()-1))[0]
    
    if scale > 1:
        cell_w = cell_w * scale
        cell_h = cell_h * scale
        rect.w = rect.w * scale
        rect.h = rect.h * scale
        padding = padding * scale
        w,h = image.get_size()
        image = pygame.transform.scale(image, (w*scale, h*scale))
    
    offsets = (int((cell_w - rect.w) / 2), (cell_h - rect.h) - padding)
    cols = int(image.get_width() / cell_w)
    rows = int(image.get_height() / cell_h)
    
    cells = {}
    for row in range(rows):
        for col in range(cols):
            cells[row*cols+col] = image.subsurface((col*cell_w, row*cell_h, cell_w, cell_h))

    return { "cols": cols, "rows": rows, "cells": cells, "rect": rect, "offsets": offsets }

class Sprite:
    def __init__(self, pngfile, game):
        if pngfile not in game.sprite_db:
            self.uid = pngfile
            data = load_sprite(os.path.join("data", "sprites", pngfile), game.scale)
            self.cols = data["cols"]
            self.rows = data["rows"]
            self.cells = data["cells"]
            self.rect = data["rect"]
            self.x_off, self.y_off = data["offsets"]
            
            game.sprite_db[pngfile] = self
    
    def get_cell(self, col, row):
        if (col >= 0 and col < self.cols) and (row >= 0 and row < self.rows):
            return self.cells[self.cols*row+col]
        else:
            print("col or row out of sprite's bounds")
            pygame.quit()
            exit()
