"""
The :mod:`item` module contains inventory and item classes that provide
a generic inventory management system.

There are two types of inventory system. OrdinaryItems (stored in
OrdinaryInventories) are items that can be created from a single id,
therefore will appear stacked in the inventory.

UniqueItems (stored in UniquesInventories) are items that will not be
stacked, being stored in the inventory individually.
"""

class Inventory(object):

    """
    An inventory is a place to store items.
    """
    
    def __init__(self, max_weight = None):
        """
        *Constructor.*
        
        The inventory will be able to hold items totaling up to
        *max_weight*.
        
        :attr:`weight`
            Current total weight in the inventory.

        :attr:`max_weight`
            Maximum total weight the inventory can hold.
        """
        self.weight = 0
        self.max_weight = max_weight

    def initial_state(self):
        pass

    def save_state(self):
        """
        Return serializable data for rebuilding the inventory when the
        state is loaded.
        """
        return (self.class_save(), self.custom_save())

    def class_save(self):
        return (self.weight, self.max_weight)

    def custom_save(self):
        """
        *Virtual.*
        
        Return serializable data specific for a derived class for
        rebuilding the inventory when the state is loaded with
        load_state().
        """
        return None

    def load_state(self, state):
        """
        Rebuild the inventory based on the *state* returned by
        save_state() in another game instance.
        """
        self.class_load(state[0])
        self.custom_load(state[1])

    def class_load(self, state):
        self.weight = state[0]
        self.max_weight = state[1]

    def custom_load(self, state):
        """
        *Virtual.*
        
        Load data specific for a derived class from what a custom_save()
        call returned previously.
        """
        pass


class OrdinaryInventory(Inventory):

    # Read-Only Attributes:
    # items - dictionary mapping ids to their amounts contained
    # max_item_pile - maximum amount of identical items in a pile
    """
    An OrdinaryInventory holds OrdinaryItems.
    """

    def __init__(self, factory, max_weight=None, max_item_pile=None):
        """
        *Constructor.*
        
        Create an empty inventory, which holds up to *max_weight* in weight
        and *max_item_pile* items in each pile.
        
        *factory* should be an IdFactory with which all OrdinaryItems to
        be stored in this inventory have been registered.
        
        :attr:`items`
            Dict mapping item ids to the amount of that item in the
            inventory.

        :attr:`factory`
            IdFactory with which all OrdinaryItems to be stored in this
            inventory have been registered.

        :attr:`max_item_pile`
            Maximum number of items with the same id the inventory can
            hold.
        """
        Inventory.__init__(self, max_weight)
        self.items = {}
        self.max_item_pile = max_item_pile
        self.factory = factory

    def class_save(self):
        return Inventory.class_save(self) + (self.items, self.max_item_pile)

    def class_load(self, state):
        Inventory.class_load(self, state[:2])
        self.items = state[2]
        self.max_item_pile = state[3]

    def add_item(self, item, amount=1):
        """
        Add one or more copies of an item to the inventory.
        
        The *item* should be an OrdinaryItem. The *amount* of copies
        inserted defaults to 1.
        
        Return the amount of copies actually added to the inventory. A
        number smaller than *amount* means that there was not enough
        room (either because of weight constraints or pile constraints).
        """
        final_amount = amount
        
        #check for overweight problems
        if self.max_weight is not None:
            available_weight = self.max_weight - self.weight
            amount_that_fits = available_weight / item.weight
            final_amount = min(amount_that_fits, final_amount)

        #check for pile problems
        if self.max_item_pile is not None:
            pile_space = self.max_item_pile - self.get_amount(item)
            final_amount = min(pile_space, final_amount)

        self.__unchecked_add_item(item.id, final_amount, item.weight)
        return final_amount

    def remove_item(self, item, amount=1):
        """
        Remove one or more copies of an item from the inventory.
        
        The *item* should be an OrdinaryItem. The *amount* of copies
        removed defaults to 1.
        
        Return the amount of copies actually removed from the inventory. A
        number smaller than *amount* means that there were not enough
        items with the same id as the one given.
        """
        amount_contained = self.get_amount_by_id(item.id)
        if amount_contained > amount:
            self.items[item.id] -= amount
            self.weight -= amount * item.weight
            return amount
        elif amount_contained > 0:
            del self.items[item.id]
            self.weight -= amount_contained * item.weight
            return amount_contained
        else:
            return 0

    def add_item_by_id(self, item_id, amount=1):
        """
        Add one or more items fabricated by an id to the inventory.
        
        *item_id* should be a valid id that can be fabricated by the
        factory function into an OrdinaryItem. The *amount* of copies
        inserted defaults to 1.
        
        Return the amount of copies actually added to the inventory. A
        number smaller than *amount* means that there was not enough
        room (either because of weight constraints or pile constraints).
        """
        return self.add_item(self.factory.fabricate(item_id), amount)

    def remove_item_by_id(self, item_id, amount=1):
        """
        Remove one or more items fabricated by an id from the inventory.
        
        *item_id* should be a valid id that can be fabricated by the
        factory function into an OrdinaryItem. The *amount* of copies
        removed defaults to 1.
        
        Return the amount of copies actually removed from the inventory. A
        number smaller than *amount* means that there were not enough
        items with that id.
        """
        return self.remove_item(self.factory.fabricate(item_id), amount)

    # Private
    def __unchecked_add_item(self, id, amount, item_weight):
        if amount > 0:
            if self.contains_by_id(id):
                self.items[id] += amount
            else:
                self.items[id] = amount
            self.weight += amount * item_weight

    def contains(self, item):
        """
        Return whether there is at least one of the given *item* in
        th inventory.
        """
        return self.contains_by_id(item.id)

    def contains_by_id(self, id):
        """
        Return whether there is at least one item with the given *id* in
        th inventory.
        """
        return id in self.items

    def get_amount(self, item):
        """
        Return the amount of copies of an *item* in the inventory.
        """
        return self.get_amount_by_id(item.id)

    def get_amount_by_id(self, id):
        """
        Return the amount of items with the given *id* in the inventory.
        """
        return self.items.get(id, 0)

    def get_pile_count(self):
        """
        Return the number of different items (different id) in the
        inventory.
        """
        return len(self.items)

    def get_total_items(self):
        """
        Return the total number of items in the inventory.
        """
        return sum(self.items.values())

    def clear(self):
        """
        Remove all items in the inventory.
        """
        self.items = {}
        self.weight = 0

    def get_ordered_list(self, extract_function=lambda x: x.name,
                         comparison_function=cmp, reverse=False):
        """
        Return an ordered list of all different OrdinaryItems in the
        inventory.
        
        The default ordering is by ascending item ids. Different orders can
        be specified by passing *extract_function*, which should extract
        from the OrdinaryItem the field by which to order, and
        *comparison_function*, a function of two arguments which should
        return a negative, zero or positive number depending on whether
        the first argument is considered smaller than, equal to, or larger
        than the second argument. To order descending, pass *reverse*
        as True.
        """
        return sorted([self.factory.fabricate(id) for id in self.items.keys()],
                      comparison_function,
                      extract_function,
                      reverse)

    def get_items_with_amounts(self):
        """
        Return a dict mapping OrdinaryItems to the amount of each the
        inventory contains.
        """
        return dict((self.factory.fabricate(id), amount) for id, amount \
                    in self.items.iteritems())

    def fabricate(self, id):
        """
        Instantiate an OrdinaryItem from an id using the factory function.
        """
        return self.factory.fabricate(id)


class UniquesInventory(Inventory):

    """
    An UniquesInventory holds UniqueItems.

    :attr:`items`
        A list of the items in the inventory.
    """

    def __init__(self, max_weight=None, max_items=None):
        Inventory.__init__(self, max_weight)
        self.items = []
        self.max_items = max_items

    def class_save(self):
        return (self.items, self.max_items)

    def class_load(self, state):
        self.items = state[0]
        self.max_items = state[1]

    def add_item(self, item):
        """
        Add an *item* to the inventory.
        
        Return True if the item was inserted, False if that would have
        exceed the inventory weight or item limit.
        """
        #check for overweight problems
        if self.max_weight is not None \
           and self.max_weight - self.weight < item.weight:
            return False

        if self.max_items is not None \
           and len(self.items) >= self.max_items:
            return False

        self.__unchecked_add_item(item)
        return True

    def remove_item(self, item):
        """
        Remove an *item* from the inventory.
        
        Return True if the item was there and was removed, False if it
        was not in inventory.
        """
        if item in self.items:
            self.__unchecked_remove_item(item)
            return True
        else:
            return False

    # Private
    def __unchecked_add_item(self, item):
        self.items.append(item)
        self.weight += item.weight

    # Private
    def __unchecked_remove_item(self, item):
        self.items.remove(item)
        self.weight -= item.weight

    def get_ordered_list(self, comparison_function=None, reverse=False):
        """
        Return a list of all items in the inventory, ordered by the
        given *comparison_function* argument, reversed if *reverse* is
        True.
        """
        return sorted(self.items, comparison_function, reverse=reverse)

    def clear(self):
        """
        Remove all items from the inventory.
        """
        self.items = []
        self.weight = 0

    def get_total_items(self):
        """
        Return the amount of items in the inventory.
        """
        return len(self.items)


class Item(object):

    """
    Represents a basic Item that has a name and weight.

    :attr:`name`
        String with the item's name.

    :attr:`weight`
        Weight of the item, used to limit inventories' capacity.
    """

    def __init__(self, name, weight=0):
        self.name = name
        self.weight = weight


class OrdinaryItem(Item):

    """
    An OrdinaryItem is a stackable item.
    
    That means that the item can be uniquely represented by an id - which
    can be any hashable immutable object, typically an integer.
    
    :attr:`id`
        Unique identification for that item, so that it can be fabricated.
        May be any hashable type, but typically an integer.
    """

    def __init__(self, name, weight=0):
        Item.__init__(self, name, weight)
        try:
            self.id
        except AttributeError:
            raise Exception('Classes derived from OrdinaryItem must have an '\
                            'id as class attribute')

    def __repr__(self):
        #return "%s id=%s" % (self.name, str(self.id))
        return "%s" % (self.name)


class UniqueItem(Item):

    """
    A UniqueItem is an item that is not stackable.
    
    UniqueItems cannot be uniquely represented by an id like
    OrdinaryItems they are not stored stacked, but individually. A
    factory function is not necessary to use them.
    
    UniqueItems need to be serializable and should be carefully
    implemented, since to be saved they have to be pickled.
    """

    def __init__(self, name, weight=0):
        Item.__init__(self, name, weight)
        
    def __repr__(self):
        return "%s" % (self.name)


class UsableItem(Item):
    def use(self):
        raise NotImplementedError, 'UsableItem.use() is abstract' 


class UsableOrdinaryItem(UsableItem, OrdinaryItem):
    def __init__(self, name, weight=0):
        OrdinaryItem.__init__(self, name, weight)


class UsableUniqueItem(UsableItem, UniqueItem):
    def __init__(self, name, weight=0):
        UniqueItem.__init__(self, name, weight)
