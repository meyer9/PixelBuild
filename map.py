#Handles the map parsing
import ConfigParser
import pygame
import time
from configobj import ConfigObj
class Level(object):
    def loadFile(self, filename="level.map"):
        self.map = []
        self.key = {}
        parser = ConfigParser.ConfigParser()
        parser.read(filename)
        self.tileset = parser.get("level", "tileset")
        self.map = parser.get("level", "map").replace('""', "").replace("'''","").split("\n")
        for section in parser.sections():
            if len(section)<4 and section.startswith("player")!=True:
                desc = dict(parser.items(section))
                self.key[section] = desc
            elif section.startswith("player"):
                print "Yeah"
        self.width = len(self.map[0])
        self.height = len(self.map)

    def getTile(self, x, y):
        try:
            char = self.map[y][x]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}

    def is_wall(self, x, y):
        if self.getTile(x, y)["name"]!="floor":
            return True
        else:
            return False
    
    
    def renderRow(self, row, spritesheet):
        index=0
        image = pygame.Surface((self.width*32, 32))
        for column in row:
            coord = self.key[column]["tile"].split(", ")
            tile = spritesheet.image_at(pygame.rect.Rect((int(coord[0])-1)*32, (int(coord[1])-1)*32, 32, 32))
            image.blit(tile, (index*32, 0))
            index+=1        
        return image

    def render(self, spritesheet):
        index = 0
        image = pygame.Surface((self.width*32, self.height*32))
        for y in self.map:
            image.blit(self.renderRow(y, spritesheet), (0, index*32))
            index+=1
        return image

    def setTile(self, x, y, id):
        if x<30 and x>=0 and y<40 and y>=0:
            self.map[y] = self.map[y][:x] + id + self.map[y][1+x:]

    def writeConfig(self, filename="level.map"):
        config = ConfigObj()
        config.filename=filename
        map1=""
        for y in self.map:
            map1=map1+y+"\n    "
        config["level"]={"tileset":"abc", "map":map1}
        config.write()
        level123 = open(filename, 'r').read()
        open(filename, 'w').write(level123[:level123.find("tileset = abc")]+"""tileset = abc


[d]
name = door
tile = 1, 4

[1]
name = wall
tile = 1, 1

[2]
name = wall
tile = 2, 1

[3]
name = wall
tile = 3, 1

[4]
name = wall
tile = 4, 1

[5]
name = pool
tile = 1, 2

[6]
name = wall
tile = 2, 2

[7]
name = floor
tile = 3, 2

[8]
name = wall
tile = 4, 2

[9]
name = wall
tile = 1, 3

[0]
name = wall
tile = 2, 3""")

