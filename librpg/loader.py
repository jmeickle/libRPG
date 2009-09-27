import os

class Cache:

    """
    """

    def get(self, name):
        """
        Return a pre-loaded resource loaded from *name* or None if
        that resource is not pre-loaded.
        """
        return None

    def update_used(self, name, resource):
        """
        Notify the cache that *resource* was loaded from *name*.
        """
        pass


class TemporalCache(Cache):

    """
    """

    def __init__(self, capacity=5):
        self.capacity = capacity
        self.order = []
        self.last_name = None

    def get(self, name):
        for item in self.order:
            if item[0] == name:
                return item[1]
        return None

    def update_used(self, name, resource):
        for i, item in enumerate(self.order):
            if item[0] == name:
                del self.order[i]
                self.order.append((name, resource))
                return
        if len(self.order) >= self.capacity:
            del self.order[0]
        self.order.append((name, resource))


class FrequencyCache(Cache):

    """
    """

    def __init__(self, capacity=5):
        self.capacity = capacity
        self.order = {}


class InfiniteCache(Cache):

    """
    """

    def __init__(self):
        self.items = {}

    def get(self, name):
        return self.items.get(name, None)

    def update_used(self, name, resource):
        self.items[name] = resource


class Loader:

    """
    """

    def __init__(self, caches=None):
        if caches is None:
            self.caches = [FrequencyCache(), TemporalCache()]
        else:
            self.caches = [cache for cache in caches]

    def load(self, name, force_load=False):
        if not force_load:
            for cache in self.caches:
                temp = cache.get(name)
                if temp is not None:
                    self.update_caches(name, temp)
                    return temp

        temp = self.actual_load(name)
        self.update_caches(name, temp)
        return temp

    def update_caches(self, name, temp):
        for cache in self.caches:
            cache.update_used(name, temp)

    def actual_load(self, name):
        raise NotImplementedError('Loader.actual_load() is abstract')


class FileLoader(Loader):

    """
    """

    def load(self, name, force_load=False):
        filename = os.path.abspath(name)
        return Loader.load(self, filename, force_load)
