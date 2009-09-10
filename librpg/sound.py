import atexit
import pygame

def init():
    pygame.mixer.init()
    atexit.register(quit)

def quit():
    pygame.mixer.quit()

class SoundEffectLoader:
    pass

def play_sfx(sfx_name, times=1):
    pass

class MapMusic:

    def __init__(self, map_model):
        self.map = map_model
        self.music = None

    def update(self):
        if self.map.music != self.music:
            self.stop()
            if self.map.music != None:
                self.music = self.map.music
                pygame.mixer.music.load(self.music)
                pygame.mixer.music.play(-1)

    def stop(self):
        if self.music != None:
            pygame.mixer.music.stop()

    def fadeout(self, time):
        if self.music != None:
            pygame.mixer.music.fadeout(time)
