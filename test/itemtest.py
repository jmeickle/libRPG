#! /usr/bin/env python

from librpg.item import *

def addTest(id, amount):
    a = i.addItem(UsableOrdinaryItem(id), amount)
    if a != amount:
        print "Item", id, ": Added", a, "trying to add", amount
    else:
        print "Item", id, ": Added", a

def removeTest(id, amount):
    r = i.removeItem(UsableOrdinaryItem(id), amount)
    if r != amount:
        print "Item", id, ": Removed", r, "trying to remove", amount
    else:
        print "Item", id, ": Removed", r
        
i = OrdinaryInventory()

addTest(19, 1)
addTest(42, 1)
addTest(19, 5)
addTest(66, 95)
addTest(66, 15)

removeTest(66, 17)
removeTest(19, 7)
removeTest(19, 1)

addTest(19, 1)
addTest(42, 1)
addTest(19, 5)
addTest(67, 95)
addTest(66, 15)

o = i.getOrderedList(lambda x: UsableOrdinaryItem(x), cmp, lambda x: x.id)
d = i.getItemsWithAmounts(lambda x: UsableOrdinaryItem(x))

print o
print d
