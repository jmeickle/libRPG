import os

class Cache:

    def get(self, filename):
        """
        Return a pre-loaded resource loaded from *filename* or None if
        that resource is not pre-loaded.
        """
        return None

    def update_used(self, filename, resource):
        """
        Notify the cache that *resource* was loaded from *filename*.
        """
        pass


class TemporalCache(Cache):

    def __init__(self):
        self.order = []


class FrequencyCache(Cache):

    def __init__(self):
        self.order = {}


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
