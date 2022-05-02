print("importing scene.utilities (local only)")

import os
import xml.etree.ElementTree as ET

import pygame

from . import tileset

def load_image(filename, colourkey=None):
    image = pygame.image.load(filename)
    if image != None:
        image = image.convert()
        if colourkey != None:
            if colourkey == -1:
                colourkey = image.get_at((0,0))
            image.set_colorkey(colourkey, pygame.RLEACCEL)

        return image
    else:
        print("failed to load image '{}' ".format(filename))

def load_tileset(filename, width, height, scale=1, colourkey=None, firstgid=1):
    image = pygame.image.load(filename)
    print("before scale", image)
    if scale > 1:
        image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
        print("after scale", image)
        #width = width * scale
        #height = height * scale
        
    print(width, height)
    
    gid = int(firstgid)
    textures = {}
    cols = int(image.get_width() / (width))
    rows = int(image.get_height() / (height))
    for row in range(rows):
        for col in range(cols):
            x = col * width
            y = row * height
            textures[str(gid)] = image.subsurface((x, y, width, height))
            gid += 1
    
    return textures

def get_metadata(root, scene):
    #
    scene.cols = int(root.attrib["width"])
    scene.rows = int(root.attrib["height"])
    #
    scene.tile_w = int(root.attrib["tilewidth"])
    scene.tile_h = int(root.attrib["tileheight"])
    scene.tilesize = scene.game.tilesize # assumes a square tile
    # TODO ^ this should be set to game.tilesize
    #scene.tilesize = scene.game.tilesize
    scene.tileset = tileset.Tileset(scene.tilesize, scene.tilesize)

def get_scripts(root, scene):
    for propertie in root.iter("properties"):
        for script in propertie.iter("property"):
            if script.attrib['name'] == "script":
                scene.script = importlib.import_module("scripts."+script.attrib['value'])
                #m.hi()

def get_colourkey(hex_string): # format: "ffffff"
    r = int(hex_string[:2],16)
    g = int(hex_string[2:4],16)
    b = int(hex_string[4:6],16)
    return (r,g,b)

def get_tileset(root, scene):
    for tilesettag in root.iter("tileset"):
        filename = tilesettag.attrib["source"]
        tsxtree = ET.parse(os.path.join("data", "scene", filename))
        tsxroot = tsxtree.getroot()
        for tsx in tsxroot.iter("tileset"):
            for i in tsx.iter("image"):
                filename = i.attrib["source"]
                try:
                    colourkey = get_colourkey(i.attrib["trans"])
                except:
                    colourkey = None
                    print("no colourkey")
                firstgid = tilesettag.attrib["firstgid"]
                scene.tileset.update(filename, scene.game.scale, colourkey, firstgid)
                
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
            
            col = int(float(rectattribs["x"]) / scene.tile_w)
            row = int(float(rectattribs["y"]) / scene.tile_h)
            if rectattribs["type"] == "player":
                if scene.game.player is None:
                    print("player object is not defined")
                    print("exiting")
                    pygame.quit()
                    exit()
                scene.mobs.append("player")
                scene.defaults["player"] = (col,row)
            elif rectattribs["type"] == "mob":
                #m = mob.Mob(scene.game, rectattribs["Filename"], rectattribs["id"])
                m = mob.Mob(rectattribs["Filename"], rectattribs["id"], scene.game)
                #m.dialogue = rectattribs["dialogue"] # TODO restore
                scene.mobs.append(m.uid) # scene.mobs is a list of ints (in str format)
                scene.defaults[m.uid] = (col,row)
                
            elif rectattribs["type"] == "switch":
                uid = rectattribs["id"]
                scenefile = rectattribs["Filename"]
                x = int(float(rectattribs["x"]) / scene.tile_w) * scene.tile_w
                y = int(float(rectattribs["y"]) / scene.tile_h) * scene.tile_h
                facing = rectattribs["facing"] # TODO
#               try:
                c = int(rectattribs["col"])
                r = int(rectattribs["row"])
                scene.switches[uid] = [pygame.Rect((x,y,scene.tile_w,scene.tile_h)), scenefile, (c,r), facing]
#                except:
                    #print("defaulting to map defined placement position")
#                    scene.switches[uid] = [pygame.Rect((x,y,scene.tile_w,scene.tile_h)), uid, None, facing]
            #elif rectattribs["type"] == "static":
            #	filepath = "content/image/" + rectattribs["Filename"]
            #	name = rectattribs["name"]
            #	scene.sprites[uid] = sprite.Static(filepath, name)
            #	scene.sprites[uid].scene = scene
            #	scene.sprites[uid].place(col,row)

def load_tmx(filename, scene):
    tree = ET.parse(os.path.join("data", "scene", filename))
    root = tree.getroot()
    get_metadata(root, scene)
    get_scripts(root, scene)
    get_tileset(root, scene)
    get_layers(root, scene)
    get_objects(root, scene)
    
    
    
