#! /usr/bin/env python

from librpg.item import *
from librpg.util import IdFactory

item_factory = IdFactory()


class Item19(OrdinaryItem):

    id = 19

    def __init__(self):
        OrdinaryItem.__init__(self, 'Item19')

item_factory.register(Item19)


class Item42(OrdinaryItem):

    id = 42

    def __init__(self):
        OrdinaryItem.__init__(self, 'Item42')

item_factory.register(Item42)


class Item66(OrdinaryItem):

    id = 66

    def __init__(self):
        OrdinaryItem.__init__(self, 'Item66')

item_factory.register(Item66)


class Item67(OrdinaryItem):

    id = 67

    def __init__(self):
        OrdinaryItem.__init__(self, 'Item67')

item_factory.register(Item67)


def add_test(id, amount, by_id=False):
    if by_id:
        a = i.add_item_by_id(id, amount)
    else:
        a = i.add_item(item_factory.fabricate(id), amount)

    if a != amount:
        print "Item", id, ": Added", a, "trying to add", amount
    else:
        print "Item", id, ": Added", a


def remove_test(id, amount, by_id=False):
    if by_id:
        r = i.remove_item_by_id(id, amount)
    else:
        r = i.remove_item(item_factory.fabricate(id), amount)

    if r != amount:
        print "Item", id, ": Removed", r, "trying to remove", amount
    else:
        print "Item", id, ": Removed", r

i = OrdinaryInventory(item_factory, max_item_pile=99)

add_test(19, 1, True)
add_test(42, 1)
add_test(19, 5, True)
add_test(66, 95)
add_test(66, 15)

remove_test(66, 17, True)
remove_test(19, 7)
remove_test(19, 1, True)

add_test(19, 1)
add_test(42, 1)
add_test(19, 5, True)
add_test(67, 95)
add_test(66, 15)

print i.get_ordered_list()
print i.get_items_with_amounts()
