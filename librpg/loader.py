class TemporalCache:

    def __init__(self):
        self.order = []

    def get(self, file):
        return None

    def update_used(self, file):
        pass


class FrequencyCache:

    def __init__(self):
        self.order = {}

    def get(self, file):
        return None

    def update_used(self, file):
        pass


class FileLoader:

    def __init__(self):
        self.caches = [FrequencyCache(), TemporalCache()]

    def load(self, file, force_load=False):
        if not force_load:
            for cache in self.caches:
                temp = cache.get(file)
                if temp is not None:
                    self.update_caches(file, temp)
                    return temp

        temp = self.load_from_file(file)
        self.update_caches(file, temp)
        return temp

    def update_caches(self, file, temp):
        for cache in self.caches:
            self.update_used(file, temp)

    def load_from_file(self, file):
        raise NotImplementedError('FileLoader.load_from_file() is abstract')
