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
        
a = Log().create_roll(["AddedEntry"])
b = Log().create_roll(["SubtractedEntry"])
c = Log().create_roll(["AddedEntry", "SubtractedEntry"])
d = Log().create_roll()

a.log_to_file(file("logtest.added.log", "w"))
b.log_to_file(file("logtest.subtracted.log", "w"))

l=Log()

Log().write(AddedEntry(1))
Log().write(SubtractedEntry(2))
Log().write(AddedEntry(3))
Log().write(SubtractedEntry(4))
Log().write(SubtractedEntry(5))
Log().write(SubtractedEntry(6))

c.write_to_file(file("logtest.both.log", "w"))

Log().write(AddedEntry(7))
Log().write(AddedEntry(8))

print d
