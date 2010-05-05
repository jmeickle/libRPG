from librpg.util import IdFactory
from librpg.item import OrdinaryItem, UsableOrdinaryItem
from librpg.dialog import ChoiceDialog, MessageDialog


item_factory = IdFactory()


class SinglePartyTargetItem(UsableOrdinaryItem):
    
    def use(self, party):
        dialog = ChoiceDialog('Use on whom?', party.chars)
        dialog.sync_open()
        
        target = party.chars[dialog.result]
        self.use_on_party_member(party.get_char(target))
        
    def use_on_party_member(self, character):
        raise NotImplementedError('SinglePartyTargetItem.\
                                   use_on_party_member() is abstract')


class LogItem(OrdinaryItem):

    id = 'log'

    def __init__(self):
        OrdinaryItem.__init__(self, 'Log')
item_factory.register(LogItem)


class LeafItem(OrdinaryItem):

    id = 'leaf'

    def __init__(self):
        OrdinaryItem.__init__(self, 'Leaf')
item_factory.register(LeafItem)


class PotionItem(SinglePartyTargetItem):

    id = 'potion'

    def __init__(self):
        SinglePartyTargetItem.__init__(self, 'Potion')

    def use_on_party_member(self, character):
        msg = 'Using %s on %s' % (self.name, character)
        dialog = MessageDialog(msg, True)
        dialog.sync_open()

item_factory.register(PotionItem)


class ElixirItem(SinglePartyTargetItem):

    id = 'elixir'

    def __init__(self):
        SinglePartyTargetItem.__init__(self, 'Elixir')
        
    def use_on_party_member(self, character):
        msg = 'Using %s on %s' % (self.name, character)
        dialog = MessageDialog(msg, True)
        dialog.sync_open()

item_factory.register(ElixirItem)


class FeatherItem(SinglePartyTargetItem):

    id = 'feather'

    def __init__(self):
        SinglePartyTargetItem.__init__(self, 'Feather')
        
    def use_on_party_member(self, character):
        msg = 'Using %s on %s' % (self.name, character)
        dialog = MessageDialog(msg, True)
        dialog.sync_open()

item_factory.register(FeatherItem)


class EmptyVialItem(OrdinaryItem):

    id = 'empty vial'

    def __init__(self):
        OrdinaryItem.__init__(self, 'Empty Vial')
item_factory.register(EmptyVialItem)


class LavenderItem(SinglePartyTargetItem):

    id = 'lavender'

    def __init__(self):
        SinglePartyTargetItem.__init__(self, 'Lavender')
        
    def use_on_party_member(self, character):
        msg = 'Using %s on %s' % (self.name, character)
        dialog = MessageDialog(msg, True)
        dialog.sync_open()

item_factory.register(LavenderItem)


class BasilItem(SinglePartyTargetItem):

    id = 'basil'

    def __init__(self):
        SinglePartyTargetItem.__init__(self, 'Basil')
        
    def use_on_party_member(self, character):
        msg = 'Using %s on %s' % (self.name, character)
        dialog = MessageDialog(msg, True)
        dialog.sync_open()

item_factory.register(BasilItem)


class RosemaryItem(SinglePartyTargetItem):

    id = 'rosemary'

    def __init__(self):
        SinglePartyTargetItem.__init__(self, 'Rosemary')
        
    def use_on_party_member(self, character):
        msg = 'Using %s on %s' % (self.name, character)
        dialog = MessageDialog(msg, True)
        dialog.sync_open()

item_factory.register(RosemaryItem)


class FangsItem(OrdinaryItem):

    id = 'fangs'

    def __init__(self):
        OrdinaryItem.__init__(self, 'Fangs')
item_factory.register(FangsItem)
