
import numpy
import cStringIO

import pygame
from pygame.locals import *
from xml.dom import minidom, Node

from tools import *

class MapData(object):
    def __init__(self):
        self.music = ""
        self.w = 0
        self.h = 0
        self.tw = 0
        self.th = 0
        self.nlayers = 0
        self.tiles = []
        self.collision = None
        self.tilesets = {}
        
class Map(object):
        
    def __init__(self,name, w, h, tilew, tileh, nlayers, data="", music=""):
        
        self.music = music
        self.w = w
        self.h = h
        self.tilew = tilew
        self.tileh = tileh
        self.tilesets = []
        
        self.nlayers   = nlayers
        self.layers    = None
        self.collision = None
        
        self.loadData(data)
        
    def addTileSet(self,tileset):
        self.tilesets.append(tileset)
        
    def loadData(self, data):
        
        buffer = cStringIO.StringIO(data)
        
        self.layer = [numpy.zeros((self.h,self.w),'uint32') for i in range(self.nlayers)]
        
        for c in xrange(self.nlayers):
            for i in xrange(self.h):
                for j in xrange(self.w):
                    self.layer[c][i][j] = uint32_str(buffer.read(4))
                    
        self.collision = numpy.zeros((self.h,self.w),'uint8')
        for i in xrange(self.h):
            for j in xrange(self.w):
                self.collision[i][j] = uint8_str(buffer.read(1))
                
    def generateData(self):
        
        s = ""
        
        for c in xrange(self.nlayers):
            for i in xrange(self.h):
                for j in xrange(self.w):
                    s += str_uint32(self.layer[c][i][j])
                    
        for i in xrange(self.h):
            for j in xrange(self.w):
                s += str_uint8(self.collision)
                
        return s
    
    def draw(self,screen, x, y):
        
        tw = self.tilew
        th = self.tileh
        h = self.h
        w = self.w
        tilesets = self.tilesets
        
        deltax = abs(x) % tw
        deltay = abs(y) % th        
        
        if x < 0:
            addx = abs(x)/tw
        else:
            addx = 0
            
        if y < 0:
            addy = abs(y)/th
        else:
            addy = 0

        w = min(w, (screen.get_width()-x)/tw + 1 )
        h = min(h, (screen.get_height()-y)/th + 1 )
        
        for l in xrange(self.nlayers):
            layer = self.layer[l]
            i = addy
            while i < h:
                j = addx
                while j < w:
                    v = layer[i][j]
                    tset   = 0xFF & v
                    tindex = 0xFFFF00 & v
                    tilesets[tset].tiles[tindex].draw(screen, j*tw+x, i*th+y)
                    j += 1
                i += 1
