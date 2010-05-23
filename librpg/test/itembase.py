from librpg.util import IdFactory
from librpg.item import OrdinaryItem, Usable
from librpg.dialog import ChoiceDialog, MessageDialog
from librpg.path import tileset_path


item_factory = IdFactory()


class SinglePartyTargetItem(OrdinaryItem, Usable):
    
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

    def get_description(self):
        return 'A small log of ash wood.'
    
    def get_icon_location(self):
        return (tileset_path('world_upper.png'), 2)

item_factory.register(LogItem)


class LeafItem(OrdinaryItem):

    id = 'leaf'

    def __init__(self):
        OrdinaryItem.__init__(self, 'Leaf')

    def get_icon_location(self):
        return ('item_icons.png', 3)

    def get_description(self):
        return 'A big, green leaf.' 

item_factory.register(LeafItem)


class PotionItem(SinglePartyTargetItem):

    id = 'potion'

    def __init__(self):
        SinglePartyTargetItem.__init__(self, 'Potion')
        
    def get_description(self):
        return 'Restores 100 HP in a single target.' 

    def get_icon_location(self):
        return ('item_icons.png', 0)

    def use_on_party_member(self, character):
        msg = 'Using %s on %s' % (self.name, character)
        dialog = MessageDialog(msg, True)
        dialog.sync_open()

item_factory.register(PotionItem)


class ElixirItem(SinglePartyTargetItem):

    id = 'elixir'

    def __init__(self):
        SinglePartyTargetItem.__init__(self, 'Elixir')
        
    def get_description(self):
        return 'Restores all HP and MP in a single target.' 

    def use_on_party_member(self, character):
        msg = 'Using %s on %s' % (self.name, character)
        dialog = MessageDialog(msg, True)
        dialog.sync_open()

item_factory.register(ElixirItem)


class FeatherItem(SinglePartyTargetItem):

    id = 'feather'

    def __init__(self):
        SinglePartyTargetItem.__init__(self, 'Feather')
        
    def get_description(self):
        return 'An unknown bird\'s feather.' 

    def use_on_party_member(self, character):
        msg = 'Using %s on %s' % (self.name, character)
        dialog = MessageDialog(msg, True)
        dialog.sync_open()

item_factory.register(FeatherItem)


class EmptyVialItem(OrdinaryItem):

    id = 'empty vial'
        
    def get_description(self):
        return 'A small vial that can be filled with liquids. Leak-proof.' 

    def __init__(self):
        OrdinaryItem.__init__(self, 'Empty Vial')

item_factory.register(EmptyVialItem)


class LavenderItem(SinglePartyTargetItem):

    id = 'lavender'

    def __init__(self):
        SinglePartyTargetItem.__init__(self, 'Lavender')
        
    def get_description(self):
        return 'A bunch of lavender. Smells good.' 

    def use_on_party_member(self, character):
        msg = 'Using %s on %s' % (self.name, character)
        dialog = MessageDialog(msg, True)
        dialog.sync_open()

item_factory.register(LavenderItem)


class BasilItem(SinglePartyTargetItem):

    id = 'basil'

    def __init__(self):
        SinglePartyTargetItem.__init__(self, 'Basil')
        
    def get_description(self):
        return 'A handful of basil, enough for one pizza.' 

    def use_on_party_member(self, character):
        msg = 'Using %s on %s' % (self.name, character)
        dialog = MessageDialog(msg, True)
        dialog.sync_open()

item_factory.register(BasilItem)


class RosemaryItem(SinglePartyTargetItem):

    id = 'rosemary'

    def __init__(self):
        SinglePartyTargetItem.__init__(self, 'Rosemary')

    def get_description(self):
        return 'A twig of rosemary. It has a bitter, astringent taste and is \
                highly aromatic, which complements a wide variety of foods.' 

    def use_on_party_member(self, character):
        msg = 'Using %s on %s' % (self.name, character)
        dialog = MessageDialog(msg, True)
        dialog.sync_open()

item_factory.register(RosemaryItem)


class FangsItem(OrdinaryItem):

    id = 'fangs'

    def __init__(self):
        OrdinaryItem.__init__(self, 'Fangs')

    def get_description(self):
        return 'A wolf\'s canine.' 

item_factory.register(FangsItem)
