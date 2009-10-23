from librpg.state import *

s = State()

a = range(10)
b = range(3)
c = {"a": a, "b": b}
d = ["q", 7, 3.2, [9]]

s.save_local("c", c)
s.save_local("d", d)

s.save("statetest")

s2 = State()

s.load("statetest")

print s.load_local("d")
print s.load_local("c")
