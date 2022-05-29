import os
import xml.etree.ElementTree as ET

import pygame

from . import tileset

tupadd = lambda t1, t2: tuple(map(sum, zip(t1,t2)))

def load_tileset(filename, width, height, scale, firstgid):
    image = pygame.image.load(filename)
    if scale > 1:
        w = image.get_width() * scale
        h = image.get_height() * scale
        image = pygame.transform.scale(image, (w, h))
    
    gid = int(firstgid)
    textures = {}
    cols = image.get_width() // width
    rows = image.get_height() // height
    for row in range(rows):
        for col in range(cols):
            x = col * width
            y = row * height
            textures[str(gid)] = image.subsurface((x, y, width, height))
            gid += 1
    
    return textures

def get_metadata(root, scene):
    scene.cols = int(root.attrib["width"])
    scene.rows = int(root.attrib["height"])
    scene.tile_w = int(root.attrib["tilewidth"])
    scene.tile_h = int(root.attrib["tileheight"])
    scene.tilesize = scene.game.tilesize
    scene.tileset = tileset.Tileset(scene.tilesize, scene.tilesize)

def get_scripts(root, scene):
    for propertie in root.iter("properties"):
        for script in propertie.iter("property"):
            if script.attrib['name'] == "script":
                scene.script = importlib.import_module("scripts."+script.attrib['value'])

def get_colourkey(hex_value):
    r = int(hex_value[:2],16)
    g = int(hex_value[2:4],16)
    b = int(hex_value[4:6],16)
    return (r,g,b)

def get_tileset(root, scene):
    for tilesettag in root.iter("tileset"):
        filename = tilesettag.attrib["source"]
        tsxtree = ET.parse(os.path.join("data", "scene", filename))
        tsxroot = tsxtree.getroot()
        for tsx in tsxroot.iter("tileset"):
            for i in tsx.iter("image"):
                filename = i.attrib["source"]
                firstgid = tilesettag.attrib["firstgid"]
                scene.tileset.update(filename, scene.game.scale, firstgid)
                
def get_layers(root, scene):
    for layer in root.iter("layer"):
        for data in layer.iter("data"):
            name = layer.attrib['name']
            rawdata = data.text.split(",")
            cleandata = []
            for tile in rawdata:
                cleandata.append(tile.strip())
            scene.layerdata[name] = cleandata

def get_objects(root, scene):            
    for layer in root.iter("objectgroup"):
        for rect in layer.iter("object"):
            rectattribs = {}
            for v in rect.attrib.keys():
                rectattribs[v] = rect.attrib[v]
            for proptag in rect.iter("properties"):
                for propchild in proptag.iter("property"):
                    index = propchild.attrib["name"]
                    value = propchild.attrib["value"]
                    rectattribs[index] = value
            
            col = float(rectattribs["x"]) // scene.tile_w
            row = float(rectattribs["y"]) // scene.tile_h
            if rectattribs["type"] == "player":
                if scene.game.player is None:
                    print("player object is not defined")
                    print("exiting")
                    pygame.quit()
                    exit()
                scene.mobs.append("player")
                scene.live_mobs["player"] = scene.game.player
                scene.defaults["player"] = (col,row)
            elif rectattribs["type"] == "mob":
                m = mob.Mob(rectattribs["Filename"], rectattribs["id"], scene.game)
                scene.mobs.append(m.uid)
                scene.defaults[m.uid] = (col,row)
                
            elif rectattribs["type"] == "switch":
                uid = rectattribs["id"]
                scenefile = rectattribs["Filename"]
                x = (float(rectattribs["x"]) // scene.tile_w) * scene.tile_w * scene.game.scale
                y = (float(rectattribs["y"]) // scene.tile_h) * scene.tile_h * scene.game.scale
                facing = rectattribs["facing"] # TODO
                c = int(rectattribs["col"])
                r = int(rectattribs["row"])
                scene.switches[uid] = [pygame.Rect((x,y,scene.tile_w,scene.tile_h)), scenefile, (c,r), facing]

def load_tmx(filename, scene):
    tree = ET.parse(os.path.join("data", "scene", filename))
    root = tree.getroot()
    get_metadata(root, scene)
    #get_scripts(root, scene)
    get_tileset(root, scene)
    get_layers(root, scene)
    get_objects(root, scene)

