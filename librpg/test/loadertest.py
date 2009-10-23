from librpg.loader import Loader, TemporalCache


class StringResource(object):

    def __init__(self, key, val):
        self.key = key
        self.val = val

    def load(self):
        print 'StringResource "%s" was not cached' % self.key
        return self.val

strings = {'0': StringResource('0', 'aaaa'),
           '1': StringResource('1', 'bbbb'),
           '2': StringResource('2', 'cccc'),
           '3': StringResource('3', 'dddd')}


class StringLoader(Loader):

    def actual_load(self, name):
        s = strings[name]
        return s.load()

    def test(self, s):
        print 'Requested to load %s.' % s
        self.load(s)
        print


def test_battery(name, caches, sequence):
    print '-' * 60
    print 'Testing %s' % name
    loader = StringLoader(caches)
    for s in sequence:
        loader.test(str(s))

if __name__ == '__main__':

    test_battery('TemporalCache(1)', [TemporalCache(1)],
                 [0, 1, 2, 3, 0, 1, 1, 1])

    test_battery('TemporalCache(2)', [TemporalCache(2)],
                 [0, 1, 2, 3, 0, 1, 0, 1, 1, 2])

    test_battery('TemporalCache(4)', [TemporalCache(4)],
                 [0, 1, 2, 3, 0, 1, 2, 3, 3, 2, 1])
