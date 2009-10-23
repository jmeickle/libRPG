from librpg.util import *


def test_set(x, y, value):
    print 'Setting', str(x) + ',', str(y), 'to', value
    try:
        m[x, y] = value
    except:
        print 'Error setting', value, 'at x=' + str(x), 'y=' + str(y)
    print m
    print


def test_get(x, y):
    try:
        value = m[x, y]
        print 'Getting', str(x) + ',', str(y), 'as', value
    except:
        print 'Error getting x=' + str(x), 'y=' + str(y)
    print m
    print


if __name__ == '__main__':
    m = Matrix(3, 4)

    test_set(1, 1, 'a')
    test_set(1, 2, 'b')
    test_set(0, 3, 'c')
    test_set(3, 2, 'd')

    test_get(0, 1)
    test_get(1, 1)
    test_get(2, 2)
    test_get(0, 3)
    test_get(3, 2)

    m.resize(100, 100)
    test_get(99, 99)

    m.resize(4, 5)
    test_get(4, 0)
