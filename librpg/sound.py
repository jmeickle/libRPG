import atexit
import pygame

from librpg.loader import FileLoader

def init():
    pygame.mixer.init(buffer=1024)
    atexit.register(quit)

def quit():
    pygame.mixer.quit()


class SoundEffectLoader(FileLoader):

    def load_from_file(self, file):
        return pygame.mixer.Sound(file)


sfx_loader = SoundEffectLoader()

def play_sfx(sfx_name, times=1, force_load=False):
    s = sfx_loader.load(sfx_name, force_load)
    s.play(times-1)


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
