from librpg.util import *

m = Matrix(3, 4)

def test_set(x, y, value):
    print 'Setting', str(x) + ',', str(y), 'to', value
    try:
        m.set(x, y, value)
    except:
        print 'Error setting', value, 'at x=' + str(x), 'y=' + str(y)
    print m
    print

def test_get(x, y):
    try:
        value = m.get(x, y)
        print 'Getting', str(x) + ',', str(y), 'as', value
    except:
        print 'Error getting x=' + str(x), 'y=' + str(y)
    print m
    print
    
test_set(1, 1, 'a')
test_set(1, 2, 'b')
test_set(0, 3, 'c')
test_set(3, 2, 'd')

test_get(0, 1)
test_get(1, 1)
test_get(2, 2)
test_get(0, 3)
test_get(3, 2)
