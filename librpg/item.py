class Inventory(object):

    # Read-Only Attributes:
    # weight - current total weight in inventory
    # max_weight - maximum total weight the inventory can hold

    def __init__(self, max_weight = None):
        self.weight = 0
        self.max_weight = max_weight


class OrdinaryInventory(Inventory):

    # Read-Only Attributes:
    # items - dictionary mapping item_ids to their amounts contained
    # max_item_pile - maximum amount of identical items in a pile

    def __init__(self, max_weight=None, max_item_pile=99):
        Inventory.__init__(self, max_weight)
        self.items = {}
        self.max_item_pile = max_item_pile

    def add_item(self, item, amount=1):
        #check for overweight problems
        if self.max_weight is not None:
            available_weight = self.max_weight - self.weight
            amount_that_fits = available_weight / item.weight
        else:
            amount_that_fits = self.max_item_pile

        #check for pile problems
        pile_space = self.max_item_pile - self.get_amount(item)
        final_amount = min(amount_that_fits, pile_space, amount)

        self._unchecked_add_item(item.id, final_amount, item.weight)
        return final_amount

    def remove_item(self, item, amount=1):
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

    # Private
    def _unchecked_add_item(self, item_id, amount, item_weight):
        if amount > 0:
            if self.contains_by_id(item_id):
                self.items[item_id] += amount
            else:
                self.items[item_id] = amount
            self.weight += amount * item_weight

    def contains(self, item):
        return self.contains_by_id(item.id)

    def contains_by_id(self, item_id):
        return item_id in self.items

    def get_amount(self, item):
        return self.get_amount_by_id(item.id)

    def get_amount_by_id(self, item_id):
        if self.contains_by_id(item_id):
            return self.items[item_id]
        else:
            return 0

    def get_pile_count(self):
        return len(self.items)

    def clear(self):
        self.items = {}

    def get_ordered_list(self, item_factory, comparison_function,
                       extract_function=None):
        return sorted(map(item_factory, self.items.keys()), comparison_function,
                      extract_function)

    def get_items_with_amounts(self, item_factory):
        result = {}
        for item_id, amount in self.items.iteritems():
            result[item_factory(item_id)] = amount
        return result


class UniquesInventory(Inventory):

    def __init__(self, max_weight = None):
        Inventory.__init__(self, max_weight)
        self.items = []

    def add_item(self, item):
        #check for overweight problems
        if self.max_weight is not None \
           and self.max_weight - self.weight >= item.weight:
            self._unchecked_add_item(item)
            return True
        else:
            return False

    def remove_item(self, item):
        if item in self.items:
            self.unchecked_remove_item(item)
            return True
        else:
            return False

    # Private
    def _unchecked_add_item(self, item):
        self.items.append(item)
        self.weight += item.weight

    # Private
    def unchecked_remove_item(self, item):
        self.items.remove(item)
        self.weight -= item.weight

    def get_ordered_list(self, comparison_function=None):
        return sorted(self.items, comparison_function)

    def clear(self):
        self.items = []

    def get_item_count(self):
        return len(self.items)


class Item(object):
    def __init__(self, weight=0):
        self.weight = weight


class OrdinaryItem(Item):
    def __init__(self, iid, weight=0):
        Item.__init__(self, weight)
        self.id = iid

    def __repr__(self):
        return "OrdinaryItem id=" + str(self.id)


class UniqueItem(Item):
    def __init__(self, weight=0):
        Item.__init__(self, weight)


class UsableItem(Item):
    def use(self):
        pass


class UsableOrdinaryItem(UsableItem, OrdinaryItem):
    def __init__(self, id, weight=0):
        OrdinaryItem.__init__(self, id, weight)


class UsableUniqueItem(UsableItem, UniqueItem):
    def __init__(self, weight=0):
        UniqueItem.__init__(self, weight)

