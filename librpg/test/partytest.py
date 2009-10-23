from librpg.party import *


def test_add(p, r, char):
    if p.add_char(char):
        print 'Added', char
    else:
        print 'Could not add', char
    print 'Party:', p
    print 'Reserve:', r
    print


def test_remove(p, r, char):
    if p.remove_char(char):
        print 'Removed', char
    else:
        print 'Could not remove', char
    print 'Party:', p
    print 'Reserve:', r
    print


def char_factory(name):
    return Character(name)

r = CharacterReserve(char_factory)
p = Party(r)
p.initial_state(3)
c = ['Andy', 'Bernie', 'Chris', 'Dylan', 'Emma']
for char in c:
    r.add_char(char)

test_add(p, r, c[0])
test_add(p, r, c[1])
test_add(p, r, c[2])
test_add(p, r, c[3])

test_remove(p, r, c[3])
test_remove(p, r, c[1])
test_remove(p, r, c[0])

test_add(p, r, c[4])

p.destroy()
print 'Party:', p
print 'Reserve:', r
