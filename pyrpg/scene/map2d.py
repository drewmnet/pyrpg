from . import utilities

class Map2D:
    def __init__(self, filename, game):
        if filename not in game.scene_db:
            self.filename = filename
            self.game = game
            game.scene_db[filename] = self

            self.defaults = {} # default positions of mobs
            self.mobs = []
            self.live_mobs = {}
            self.layerdata = { "bottom": None, "middle": None, "top": None, "collide": None }
            self.switches = {}

            utilities.load_tmx(self.filename, self)
    
    def get_tile(self, layername, tilep): # col, row (ie. tile precision)
        col, row = tilep
        index = int((row % self.rows) * self.cols + (col % self.cols))
        return self.layerdata[layername][index]

    def get_mobs(self):    
        l = []
        for mob in self.mobs:
            l.append(self.game.mob_db[mob])
        return l
    
    def update(self, _):
        for mob in self.live_mobs.values():
            mob.update()
    
