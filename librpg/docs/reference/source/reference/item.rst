:mod:`item` -- Items and inventory management
=============================================

.. automodule:: librpg.item
   :members:
   :show-inheritance:

Usage
-----

    Items are held in inventories. When using Items, it is natural that the
    party have at least an Inventory.
    
    Items may be either unique or ordinary. Unique items are items stored
    that are not uniquely described by an id, and are not stacked in an
    inventory. Ordinary items are uniquely described by an id and are stacked
    when inserted in multiples in an inventory.
    
    For ordinary items:
    
        - To add items to an inventory use OrdinaryInventory.add_item() or
          OrdinaryInventory.add_item_by_id().
        - To remove items from an inventory use OrdinaryInventory.remove_item()
          or OrdinaryInventory.remove_item_by_id().
        - To remove all items from an inventory, call OrdinaryInventory.clear().
        - To check if an item is in the inventory, use
          OrdinaryInventory.contains() or OrdinaryInventory.contains_by_id().
        - To get the amount of an item, use OrdinaryInventory.get_amount() or
          OrdinaryInventory.get_amount_by_id().
        - To get the number of different items in an inventory, use
          OrdinaryInventory.get_pile_count().
        - To get the number of items (counting copies) in an inventory, use
          OrdinaryInventory.get_total_items().
        - To get a list with all different items in an inventory, use
          OrdinaryInventory.get_ordered_list().
        - To get a dict mapping all different items in an inventory to their
          respective amounts, use OrdinaryInventory.get_items_with_amounts().
        - To instantiate an item from an id, use OrdinaryInventory.fabricate().
          This is equivalent to calling the factory function passed in the
          OrdinaryInventory's constructor.

    For unique items:
    
        - To add items to an inventory use UniquesInventory.add_item().
        - To remove items from an inventory use UniquesInventory.remove_item().
        - To remove all items from an inventory, call UniquesInventory.clear().
        - To get a list with all items in an inventory, use
          UniquesInventory.get_ordered_list().
        - To get the number of items in an inventory, use
          UniquesInventory.get_total_items().

Example
-------

::

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

