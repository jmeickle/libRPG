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

**test/itemtest.py**

.. literalinclude:: ../../../../test/itemtest.py
