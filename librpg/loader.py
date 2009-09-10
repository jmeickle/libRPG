import os

class TemporalCache:

    def __init__(self):
        self.order = []

    def get(self, filename):
        return None

    def update_used(self, filename, resource):
        pass


class FrequencyCache:

    def __init__(self):
        self.order = {}

    def get(self, filename):
        return None

    def update_used(self, filename, resource):
        pass


class FileLoader:

    def __init__(self):
        self.caches = [FrequencyCache(), TemporalCache()]

    def load(self, filename, force_load=False):
        filename = os.path.abspath(filename)
        if not force_load:
            for cache in self.caches:
                temp = cache.get(filename)
                if temp is not None:
                    self.update_caches(filename, temp)
                    return temp

        temp = self.load_from_file(filename)
        self.update_caches(filename, temp)
        return temp

    def update_caches(self, filename, temp):
        for cache in self.caches:
            cache.update_used(filename, temp)

    def load_from_file(self, filename):
        raise NotImplementedError('FileLoader.load_from_file() is abstract')
