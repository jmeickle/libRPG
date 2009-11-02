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


class AnimatedImage(object):

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
