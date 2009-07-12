#=================================================================================

class Inventory:

    # Read-Only Attributes:
    # weight - current total weight in inventory
    # maxWeight - maximum total weight the inventory can hold
    
    def __init__(self, maxWeight = None):
        self.weight = 0
        self.maxWeight = maxWeight

#=================================================================================

class OrdinaryInventory(Inventory):
    
    # Read-Only Attributes:
    # items - dictionary mapping itemIds to their amounts contained
    # maxItemPile - maximum amount of identical items in a pile
       
    def __init__(self, maxWeight = None, maxItemPile = 99):
        Inventory.__init__(self, maxWeight)
        self.items = {}
        self.maxItemPile = maxItemPile
        
    def addItem(self, item, amount = 1):
        #check for overweight problems
        if self.maxWeight != None:
            availableWeight = self.maxWeight - self.weight
            amountThatFits = availableWeight / item.weight
        else:
            amountThatFits = self.maxItemPile
        
        #check for pile problems
        pileSpace = self.maxItemPile - self.getAmount(item)
        
        finalAmount = min(amountThatFits, pileSpace, amount)
                
        self.uncheckedAddItem(item.id, finalAmount, item.weight)
        return finalAmount
        
    def removeItem(self, item, amount = 1):
        amountContained = self.getAmountById(item.id)
        if amountContained > amount:
            self.items[item.id] -= amount
            self.weight -= amount * item.weight
            return amount
        elif amountContained > 0:
            del self.items[item.id]
            self.weight -= amountContained * item.weight
            return amountContained
        else:
            return 0
        
    # Private
    def uncheckedAddItem(self, itemId, amount, itemWeight):
        if amount > 0:
            if self.containsById(itemId):
                self.items[itemId] += amount
            else:
                self.items[itemId] = amount
            self.weight += amount * itemWeight
        
    def contains(self, item):
        return self.containsById(item.id)
    
    def containsById(self, itemId):
        return itemId in self.items

    def getAmount(self, item):
        return self.getAmountById(item.id)
            
    def getAmountById(self, itemId):
        if self.containsById(itemId):
            return self.items[itemId]
        else:
            return 0

    def getPileCount(self):
        return len(self.items)
        
    def clear(self):
        self.items = {}
    
    def getOrderedList(self, itemFactory, comparisonFunction, extractFunction = None):
        return sorted(map(itemFactory, self.items.keys()), comparisonFunction, extractFunction)

    def getItemsWithAmounts(self, itemFactory):
        result = {}
        for itemId, amount in self.items.iteritems():
            result[itemFactory(itemId)] = amount
        return result
        
#=================================================================================

class UniquesInventory(Inventory):
    
    def __init__(self, maxWeight = None):
        Inventory.__init__(self, maxWeight)
        self.items = []
        
    def addItem(self, item):
        #check for overweight problems
        if self.maxWeight != None and self.maxWeight - self.weight >= item.weight:
            self.uncheckedAddItem(item)
            return True
        else:
            return False
            
    def removeItem(self, item):
        if item in self.items:
            self.uncheckeRemoveItem(item)
            return True
        else:
            return False
        
    # Private
    def uncheckedAddItem(self, item):
        self.items.append(item)
        self.weight += item.weight
        
    # Private
    def uncheckedRemoveItem(self, item):
        self.items.remove(item)
        self.weight -= item.weight
        
    def getOrderedList(self, comparisonFunction = None):
        return sorted(self.items, comparisonFunction)

    def clear(self):
        self.items = []
    
    def getItemCount(self):
        return len(self.items)

#=================================================================================

class Item:
    
    def __init__(self, weight = 0):
        self.weight = weight
    
#=================================================================================

class OrdinaryItem(Item):
    
    def __init__(self, id, weight = 0):
        Item.__init__(self, weight)
        self.id = id
    
    def __repr__(self):
        return "OrdinaryItem id=" + str(self.id)

#=================================================================================

class UniqueItem(Item):
    
    def __init__(self, weight = 0):
        Item.__init__(self, weight)

#=================================================================================

class UsableItem(Item):
    
    # Abstract
    def use(self):
        pass
    
#=================================================================================

class UsableOrdinaryItem(UsableItem, OrdinaryItem):
    
    def __init__(self, id, weight = 0):
        OrdinaryItem.__init__(self, id, weight)

#=================================================================================

class UsableUniqueItem(UsableItem, UniqueItem):
    
    def __init__(self, weight = 0):
        UniqueItem.__init__(self, weight)

#=================================================================================
