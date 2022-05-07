from . import utilities

class Map2D:
    def __init__(self, filename, game):
        if filename not in game.scene_db:
            self.filename = filename
            self.game = game
            # loading stuff
            game.scene_db[filename] = self

            self.defaults = {} # default positions of mobs
            self.mobs = []
            self.live_mobs = {}
            self.layerdata = { "bottom": None, "middle": None, "top": None, "collide": None }

            utilities.load_tmx(self.filename, self)
    
    # what if I pulled update into render so I wouldn't have to iterate twice? TODO        
    def update(self, tick):
        for mob in self.live_mobs.values():
            mob.update(tick)
            
    def render(self, surface):
        for mob in self.live_mobs.values():
            mob.render(surface)
            
    def get_tile(self, layername, tilep): # col, row (ie. tile precision)
        col, row = tilep
        index = int((row % self.rows) * self.cols + (col % self.cols))
        return self.layerdata[layername][index]

    def get_mobs(self):    
        l = [] # TODO what is l?
        for mob in self.mobs:
            #print(type(self.game.mob_db[mob]).__name__)
            l.append(self.game.mob_db[mob])
        return l
