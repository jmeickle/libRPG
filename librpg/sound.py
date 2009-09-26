"""
The :mod:`sound` module provides music and sound effect utilities
wrapping pygame's mixer module.
"""

import atexit
import pygame

from librpg.loader import FileLoader

def init():
    try :
        pygame.mixer.init(buffer=1024)
    except pygame.error:
        print "no sound device available"
    else:
        atexit.register(quit)


def quit():
    pygame.mixer.quit()


class SoundEffectLoader(FileLoader):

    def actual_load(self, name):
        return pygame.mixer.Sound(name)


__sfx_loader = SoundEffectLoader()

def play_sfx(sfx_name, times=1, force_load=False):
    """
    Play a sound effect.
    
    *sfx_name* should be the name of the file containing the sound effect.
    
    *times*, if specified, will make the sound be played that many times.

    *force_load*, if specified, will force the sound to be loaded again
    from its file rather than searched in the cache.
    """
    s = __sfx_loader.load(sfx_name, force_load)
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
