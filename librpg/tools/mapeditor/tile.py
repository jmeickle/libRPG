
import pygame
from pygame.locals import *
import pygame.time as Time

class AnimTile(object):
    def __init__(self, milisec):
        self.frames  = []
        self.current = 0
        self.nframes = 0
        self.milisec = milisec
        self.time    = Time.get_ticks()
        
    def addFrame(self,frame):
        self.frames.append(frame)
        self.nframes += 1
        
    def draw(self, surface,x,y):
        pygame.Surface.blit(surface, self.frames[self.current], (x,y))
        now = Time.get_ticks()
        if self.time+self.milisec < now:
            self.current = (self.current + 1) % self.nframes
            self.time = now
 
class Tile(object):
    def __init__(self,surface):
        self.surface = surface
        
    def draw(self, surface,x,y):
        pygame.Surface.blit(surface, self.surface, (x,y))
        
class TileSet(object):
    
    def __init__(self, name, surface, tilew, tileh):
        
        self.name = name
        self.tiles = []
        self.animtiles = []
        
        tmpimg = pygame.Surface((tilew,tileh))
        w,h = surface.get_width(), surface.get_height()
        
        for i in xrange(h/tileh):
            for j in xrange(w/tilew):
                tmpimg.blit(surface,(0,0), pygame.Rect(j*tilew, i*tileh, tilew, tileh))
                self.tiles.append(Tile(tmpimg.copy()))

    def defAnimTile(self,init,end,milisec):
        AT = AnimTile(milisec)
        for tile in self.tiles[init:end+1]:
            AT.addFrame(tile.surface)
        self.animtiles.append(AT)
        
