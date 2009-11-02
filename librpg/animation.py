"""
The :mod:`animation` module provides the AnimatedImage class, an Image
that wraps animation funcionalities for easy usage by other modules
or applications.
"""


from librpg.image import Image


class Metronome(object):

    def __init__(self):
        self.n = 0

    def step(self):
        self.n += 1

    def get(self):
        return self.n


metronome = Metronome()


def get_metronome():
    return metronome


def get_tick():
    return metronome.get()


class AnimatedImage(Image):

    """
    An AnimatedImage is an Image that returns various Surfaces through
    get_surface(), causing the illusion of animation.

    *surfaces* should be a list or tuple of the pygame Surfaces that
    compose the animation.

    *frame_duration* should be an integer indicating the number of frames
    for which each Surface will be displayed before switching to the next.

    Note that::

        AnimatedImage([a, b, c])

    is equavalent to::

        AnimatedImage([a, a, b, b, c, c], 2)
    """

    def __init__(self, surfaces, frame_duration=1):
        assert surfaces, 'First paramater has to be a list of Surfaces'
        self.surfaces = surfaces

        self.frames = len(self.surfaces)
        self.frame_duration = frame_duration
        self.period = self.frames * self.frame_duration

        self.phase = get_tick()

    def get_surface(self):
        frame = self.calc_frame()
        return self.surfaces[frame]

    def calc_frame(self):
        n = get_tick()
        return ((n - self.phase) % self.period) / self.frame_duration

    def get_width(self):
        return self.get_surface().get_width()

    def get_height(self):
        return self.get_surface().get_height()
