#! /usr/bin/env python

from librpg.item import *

def add_test(id, amount):
    a = i.add_item(UsableOrdinaryItem(id), amount)
    if a != amount:
        print "Item", id, ": Added", a, "trying to add", amount
    else:
        print "Item", id, ": Added", a

def remove_test(id, amount):
    r = i.remove_item(UsableOrdinaryItem(id), amount)
    if r != amount:
        print "Item", id, ": Removed", r, "trying to remove", amount
    else:
        print "Item", id, ": Removed", r
        
i = OrdinaryInventory()

add_test(19, 1)
add_test(42, 1)
add_test(19, 5)
add_test(66, 95)
add_test(66, 15)

remove_test(66, 17)
remove_test(19, 7)
remove_test(19, 1)

add_test(19, 1)
add_test(42, 1)
add_test(19, 5)
add_test(67, 95)
add_test(66, 15)

print i.get_ordered_list(lambda x: UsableOrdinaryItem(x), cmp, lambda x: x.id)
print i.get_items_with_amounts(lambda x: UsableOrdinaryItem(x))

