#! /usr/bin/env python

from librpg.log import *

class AddedEntry (LogEntry):
    def __init__(self, n):
        LogEntry.__init__(self, "AddedEntry")
        self.n = n
     
    def __str__(self):
        return "Added " + str(self.n)
    
    def __repr__(self):
        return "+" + str(self.n)
        
class SubtractedEntry(LogEntry):
    def __init__(self, n):
        LogEntry.__init__(self, "SubtractedEntry")
        self.n = n
     
    def __str__(self):
        return "Subtracted " + str(self.n)
    
    def __repr__(self):
        return "-" + str(self.n)
        
a = create_roll(["AddedEntry"])
b = create_roll(["SubtractedEntry"])
c = create_roll(["AddedEntry", "SubtractedEntry"])
d = create_roll()

a.log_to_file(file("logtest.added.log", "w"))
b.log_to_file(file("logtest.subtracted.log", "w"))

write(AddedEntry(1))
write(SubtractedEntry(2))
write(AddedEntry(3))
write(SubtractedEntry(4))
write(SubtractedEntry(5))
write(SubtractedEntry(6))

c.write_to_file(file("logtest.both.log", "w"))

write(AddedEntry(7))
write(AddedEntry(8))

print d
